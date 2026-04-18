"""
Integration tests — full pipeline: POS → scorer → scheduler → RL.
"""
import time
import pytest
from core.pos.mock_stream import generate_order, generate_rush_batch
from core.scorer.complexity_scorer import score_drink
from core.scheduler.concurrent_scheduler import ConcurrentScheduler, make_action_text
from core.rl.agent import QLearningAgent, CafeState, Episode, compute_reward, ACTIONS


class TestFullPipeline:
    def test_rush_batch_end_to_end(self):
        """Generate a rush, score it, schedule it, extract actions."""
        orders = generate_rush_batch(12)
        assert len(orders) == 12

        # Score all drinks
        for order in orders:
            for drink in order.drinks:
                result = score_drink(drink)
                assert 0 <= result.total <= 10

        # Schedule
        scheduler = ConcurrentScheduler()
        result = scheduler.schedule(orders)

        assert result.action_now is not None
        assert result.concurrency_ratio >= 1.0
        assert result.total_time_secs > 0

        # Get action text
        action_main, action_sub, _, _ = make_action_text(result)
        assert len(action_main) > 0

    def test_rl_learns_from_completion(self):
        """Simulate completing orders and verify RL updates."""
        agent = QLearningAgent(checkpoint_path="/tmp/integration_test.pkl")

        orders = generate_rush_batch(5)
        scheduler = ConcurrentScheduler()
        result = scheduler.schedule(orders)

        state = CafeState(
            queue_depth=len(orders),
            top_complexity=result.scheduled[0].complexity.total if result.scheduled else 5.0,
            avg_wait_min=sum(o.wait_minutes for o in orders) / len(orders),
            machine_busy_count=2,
            is_rush_hour=True,
        )

        action = agent.select_action(state)
        assert action in ACTIONS

        # Simulate completion
        reward = compute_reward(
            throughput_delta=1.2,
            wait_reduced_min=0.8,
            concurrency_used=result.concurrency_ratio > 1.5,
            order_error=False,
        )

        ep = Episode(
            episode_id=1,
            state=state,
            action=action,
            reward=reward,
            next_state=None,
            done=True,
            throughput_delta=1.2,
            wait_delta=0.8,
        )

        td_error = agent.update(ep)
        assert agent.stats.total_episodes == 1
        assert isinstance(td_error, float)

    def test_concurrency_improves_with_milk_drinks(self):
        """Orders with milk-based drinks should trigger concurrent steaming."""
        from core.scorer.complexity_scorer import DrinkSpec, PRESET_DRINKS

        orders = []
        for i, key in enumerate(["oat_latte", "cappuccino", "flat_white"]):
            spec = PRESET_DRINKS[key]
            from core.scheduler.concurrent_scheduler import Order
            orders.append(Order(
                order_id=f"#{i+1}",
                customer_name=f"Customer {i+1}",
                drinks=[spec],
                received_at=time.time() - (3 - i) * 60,
            ))

        scheduler = ConcurrentScheduler()
        result = scheduler.schedule(orders)

        # At least some concurrent tagging should occur for milk drinks
        all_concurrent = [s for s in result.scheduled if s.concurrent_with]
        assert len(all_concurrent) > 0

    def test_mock_stream_generates_valid_orders(self):
        for i in range(20):
            order = generate_order(i)
            assert order.order_id
            assert order.customer_name
            assert len(order.drinks) >= 1
            for drink in order.drinks:
                assert drink.name
                assert drink.base in ("espresso", "ristretto", "lungo", "cold_brew", "filter")
                assert drink.milk in ("none", "whole", "oat", "almond", "soy", "coconut")
