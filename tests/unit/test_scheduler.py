"""Unit tests for the concurrent scheduler."""
import time
import pytest
from core.scheduler.concurrent_scheduler import (
    ConcurrentScheduler,
    Order,
    make_action_text,
)
from core.scorer.complexity_scorer import DrinkSpec


def make_order(order_id: str, drinks: list[DrinkSpec], wait_minutes: float = 2.0) -> Order:
    order = Order(
        order_id=order_id,
        customer_name="Test Customer",
        drinks=drinks,
        received_at=time.time() - wait_minutes * 60,
    )
    return order


def latte() -> DrinkSpec:
    return DrinkSpec("Latte", base="espresso", milk="oat", shots=2)


def americano() -> DrinkSpec:
    return DrinkSpec("Americano", base="lungo", milk="none", shots=2)


def matcha() -> DrinkSpec:
    return DrinkSpec("Matcha", base="filter", milk="oat", shots=0, extras=["matcha"])


class TestConcurrentScheduler:
    def setup_method(self):
        self.scheduler = ConcurrentScheduler()

    def test_empty_queue_returns_empty_result(self):
        result = self.scheduler.schedule([])
        assert result.scheduled == []
        assert result.action_now is None

    def test_single_order_schedules(self):
        orders = [make_order("#1", [latte()])]
        result = self.scheduler.schedule(orders)
        assert len(result.scheduled) > 0
        assert result.action_now is not None

    def test_high_wait_order_prioritized(self):
        low_wait = make_order("#1", [americano()], wait_minutes=0.5)
        high_wait = make_order("#2", [latte()], wait_minutes=5.0)
        result = self.scheduler.schedule([low_wait, high_wait])
        # High wait should surface first
        first_order_id = result.scheduled[0].order_id
        assert first_order_id == "#2"

    def test_concurrency_ratio_above_one_for_complex_orders(self):
        orders = [
            make_order("#1", [latte()], wait_minutes=3.0),
            make_order("#2", [matcha()], wait_minutes=2.5),
            make_order("#3", [latte()], wait_minutes=2.0),
        ]
        result = self.scheduler.schedule(orders)
        assert result.concurrency_ratio >= 1.0

    def test_completed_orders_excluded(self):
        done = make_order("#1", [latte()])
        done.completed_at = time.time()
        pending = make_order("#2", [americano()])
        result = self.scheduler.schedule([done, pending])
        order_ids = {s.order_id for s in result.scheduled}
        assert "#1" not in order_ids
        assert "#2" in order_ids

    def test_no_machine_slot_collision(self):
        """Two drinks should never occupy the same machine at the same time."""
        orders = [make_order(f"#{i}", [latte()], wait_minutes=float(i)) for i in range(5)]
        result = self.scheduler.schedule(orders)
        slots_by_machine: dict[str, list[tuple[int, int]]] = {}
        for s in result.scheduled:
            machine = s.machine_slot
            start = s.start_offset_secs
            end = start + s.duration_secs
            if machine not in slots_by_machine:
                slots_by_machine[machine] = []
            for prev_start, prev_end in slots_by_machine[machine]:
                overlap = start < prev_end and prev_start < end
                assert not overlap, (
                    f"Machine {machine} collision: [{start},{end}] vs [{prev_start},{prev_end}]"
                )
            slots_by_machine[machine].append((start, end))

    def test_time_saved_non_negative(self):
        orders = [make_order(f"#{i}", [latte(), americano()]) for i in range(4)]
        result = self.scheduler.schedule(orders)
        assert result.time_saved_vs_serial_secs >= 0

    def test_custom_weights_change_order(self):
        """Changing weights to pure complexity should reorder vs pure wait-time."""
        wait_scheduler = ConcurrentScheduler(wait_weight=1.0, complexity_weight=0.0, machine_weight=0.0)
        cplx_scheduler = ConcurrentScheduler(wait_weight=0.0, complexity_weight=1.0, machine_weight=0.0)

        orders = [
            make_order("#high-wait", [americano()], wait_minutes=6.0),   # simple but old
            make_order("#high-cplx", [matcha()], wait_minutes=0.5),       # complex but new
        ]
        wait_result = wait_scheduler.schedule(orders)
        cplx_result = cplx_scheduler.schedule(orders)

        wait_first = wait_result.scheduled[0].order_id if wait_result.scheduled else None
        cplx_first = cplx_result.scheduled[0].order_id if cplx_result.scheduled else None

        # They should differ in prioritization strategy
        assert wait_first == "#high-wait"
        assert cplx_first == "#high-cplx"


class TestMakeActionText:
    def test_action_text_nonempty_for_active_queue(self):
        orders = [make_order("#1", [latte()], wait_minutes=3.0)]
        scheduler = ConcurrentScheduler()
        result = scheduler.schedule(orders)
        action_main, action_sub, conc_main, conc_sub = make_action_text(result)
        assert len(action_main) > 0
        assert len(action_sub) > 0

    def test_clear_queue_message(self):
        from core.scheduler.concurrent_scheduler import ScheduleResult
        empty = ScheduleResult([], 0, 1.0, 0, None, None)
        action_main, _, _, _ = make_action_text(empty)
        assert "clear" in action_main.lower() or "queue" in action_main.lower()
