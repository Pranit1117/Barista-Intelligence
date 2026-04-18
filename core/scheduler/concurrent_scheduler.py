"""
Concurrent greedy scheduler.
Assigns drinks to machine slots in priority order,
maximising parallel execution to reduce total queue time.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4

from core.scorer.complexity_scorer import ComplexityResult, score_drink, DrinkSpec


@dataclass
class Order:
    order_id: str
    customer_name: str
    drinks: list[DrinkSpec]
    received_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None

    @property
    def wait_seconds(self) -> float:
        return time.time() - self.received_at

    @property
    def wait_minutes(self) -> float:
        return round(self.wait_seconds / 60, 1)

    @property
    def is_complete(self) -> bool:
        return self.completed_at is not None


@dataclass
class ScheduledDrink:
    order_id: str
    customer_name: str
    drink: DrinkSpec
    complexity: ComplexityResult
    priority_score: float
    machine_slot: str           # "group1", "group2", "steamer", "assemble"
    start_offset_secs: int      # seconds from now
    duration_secs: int
    concurrent_with: list[str] = field(default_factory=list)  # other order_ids


@dataclass
class ScheduleResult:
    scheduled: list[ScheduledDrink]
    total_time_secs: int
    concurrency_ratio: float    # >1.0 means concurrent work happening
    time_saved_vs_serial_secs: int
    action_now: Optional[ScheduledDrink]
    action_concurrent: Optional[ScheduledDrink]


class ConcurrentScheduler:
    """
    Greedy scheduler with concurrent slot optimisation.

    Priority score = w_wait × wait_min + w_complexity × complexity + w_machine × machine_fit

    Concurrent pairing rules:
    - While a shot pulls (28s), steam milk for the NEXT milk-based drink
    - While steaming, grind for the drink after that
    - Assembly can run on any concurrent slot
    """

    def __init__(
        self,
        wait_weight: float = 0.70,
        complexity_weight: float = 0.20,
        machine_weight: float = 0.10,
        max_concurrent_slots: int = 3,
        group1_shot_secs: int = 28,
        group2_shot_secs: int = 27,
        steamer_warmup_secs: int = 8,
        assemble_secs: int = 15,
        milk_steam_secs: dict[str, int] | None = None,
    ):
        self.wait_weight = wait_weight
        self.complexity_weight = complexity_weight
        self.machine_weight = machine_weight
        self.max_slots = max_concurrent_slots
        self.shot_secs = {"group1": group1_shot_secs, "group2": group2_shot_secs}
        self.steamer_warmup = steamer_warmup_secs
        self.assemble_secs = assemble_secs
        self.milk_steam_secs = milk_steam_secs or {
            "whole": 24, "oat": 32, "almond": 30, "soy": 28, "coconut": 30
        }

    def schedule(self, orders: list[Order]) -> ScheduleResult:
        """Return an optimised execution schedule for the current queue."""
        if not orders:
            return ScheduleResult([], 0, 1.0, 0, None, None)

        # 1. Score and sort all drinks from all orders
        scored: list[tuple[Order, DrinkSpec, ComplexityResult, float]] = []
        for order in orders:
            if order.is_complete:
                continue
            for drink in order.drinks:
                complexity = score_drink(drink)
                priority = self._priority(order, complexity)
                scored.append((order, drink, complexity, priority))

        scored.sort(key=lambda x: x[3], reverse=True)

        # 2. Assign to machine slots greedily
        machine_cursors: dict[str, int] = {
            "group1": 0, "group2": 0, "steamer": 0, "assemble": 0
        }
        scheduled: list[ScheduledDrink] = []

        for order, drink, complexity, priority in scored:
            steps = self._steps_for_drink(drink, complexity)
            for step_machine, step_duration in steps:
                start = machine_cursors[step_machine]
                scheduled.append(ScheduledDrink(
                    order_id=order.order_id,
                    customer_name=order.customer_name,
                    drink=drink,
                    complexity=complexity,
                    priority_score=priority,
                    machine_slot=step_machine,
                    start_offset_secs=start,
                    duration_secs=step_duration,
                ))
                machine_cursors[step_machine] = start + step_duration + 2  # 2s buffer

        # 3. Tag concurrent pairs
        self._tag_concurrent(scheduled)

        total_time = max(
            (s.start_offset_secs + s.duration_secs for s in scheduled), default=0
        )
        serial_time = sum(s.duration_secs for s in scheduled)
        concurrency = round(serial_time / max(total_time, 1), 2)

        action_now = scheduled[0] if scheduled else None
        action_concurrent = next(
            (s for s in scheduled[1:] if s.start_offset_secs < (action_now.duration_secs if action_now else 0)),
            None
        )

        return ScheduleResult(
            scheduled=scheduled,
            total_time_secs=total_time,
            concurrency_ratio=concurrency,
            time_saved_vs_serial_secs=max(0, serial_time - total_time),
            action_now=action_now,
            action_concurrent=action_concurrent,
        )

    def _priority(self, order: Order, complexity: ComplexityResult) -> float:
        wait_score = self.wait_weight * order.wait_minutes
        complexity_score = self.complexity_weight * complexity.total
        machine_score = self.machine_weight * (complexity.concurrent_slots_needed / 3)
        return round(wait_score + complexity_score + machine_score, 3)

    def _steps_for_drink(
        self, drink: DrinkSpec, complexity: ComplexityResult
    ) -> list[tuple[str, int]]:
        """Return ordered (machine, duration_secs) pairs for one drink."""
        steps: list[tuple[str, int]] = []

        if drink.base in ("espresso", "ristretto", "lungo"):
            # Grind is on group1 by default; group2 if group1 busy
            steps.append(("group1", complexity.extraction_seconds))

        if drink.milk != "none":
            steam_secs = self.milk_steam_secs.get(drink.milk, 28)
            steps.append(("steamer", steam_secs))

        steps.append(("assemble", self.assemble_secs))
        return steps

    def _tag_concurrent(self, scheduled: list[ScheduledDrink]) -> None:
        """Find drinks whose execution windows overlap and mark them."""
        for i, a in enumerate(scheduled):
            a_end = a.start_offset_secs + a.duration_secs
            for b in scheduled[i + 1:]:
                b_end = b.start_offset_secs + b.duration_secs
                overlap = (
                    b.start_offset_secs < a_end
                    and a.start_offset_secs < b_end
                    and a.machine_slot != b.machine_slot
                )
                if overlap:
                    if b.order_id not in a.concurrent_with:
                        a.concurrent_with.append(b.order_id)
                    if a.order_id not in b.concurrent_with:
                        b.concurrent_with.append(a.order_id)


def make_action_text(result: ScheduleResult) -> tuple[str, str, str, str]:
    """
    Return (action_main, action_sub, concurrent_main, concurrent_sub)
    for the barista tablet display.
    """
    if not result.action_now:
        return "Queue is clear", "Well done!", "", ""

    now = result.action_now
    action_main = f"{_verb(now.machine_slot)} {now.drink.name} → {now.customer_name}"
    action_sub = f"{now.duration_secs}s · {now.machine_slot.replace('_', ' ').title()}"

    if result.action_concurrent:
        c = result.action_concurrent
        conc_main = f"While that runs — {_verb(c.machine_slot)} {c.drink.name}"
        conc_sub = f"For {c.customer_name} · {c.machine_slot.replace('_', ' ').title()}"
    else:
        conc_main, conc_sub = "", ""

    return action_main, action_sub, conc_main, conc_sub


def _verb(machine: str) -> str:
    return {
        "group1": "Pull shot →",
        "group2": "Pull shot →",
        "steamer": "Steam milk →",
        "assemble": "Assemble",
    }.get(machine, "Prepare")
