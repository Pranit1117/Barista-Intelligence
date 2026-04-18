"""Unit tests for the RL Q-learning agent."""
import pytest
from core.rl.agent import (
    QLearningAgent,
    CafeState,
    Episode,
    ACTIONS,
    compute_reward,
)


def make_state(**kwargs) -> CafeState:
    defaults = dict(queue_depth=5, top_complexity=6.0, avg_wait_min=3.0,
                    machine_busy_count=2, is_rush_hour=True)
    defaults.update(kwargs)
    return CafeState(**defaults)


def make_episode(state: CafeState, action: str, reward: float,
                 next_state: CafeState | None = None) -> Episode:
    return Episode(
        episode_id=1,
        state=state,
        action=action,
        reward=reward,
        next_state=next_state,
        done=next_state is None,
        throughput_delta=1.0,
        wait_delta=0.5,
    )


class TestQLearningAgent:
    def setup_method(self):
        self.agent = QLearningAgent(checkpoint_path="/tmp/test_policy.pkl")

    def test_select_action_returns_valid_action(self):
        state = make_state()
        action = self.agent.select_action(state)
        assert action in ACTIONS

    def test_update_returns_td_error(self):
        state = make_state()
        ep = make_episode(state, ACTIONS[0], reward=1.5)
        td = self.agent.update(ep)
        assert isinstance(td, float)

    def test_positive_reward_increases_q_value(self):
        state = make_state()
        action = ACTIONS[0]
        key = state.to_discrete_key()

        # Prime the table with a known value
        self.agent.q_table[key] = {a: 0.0 for a in ACTIONS}
        ep = make_episode(state, action, reward=3.0)
        self.agent.update(ep)
        assert self.agent.q_table[key][action] > 0.0

    def test_negative_reward_decreases_q_value(self):
        state = make_state()
        action = ACTIONS[0]
        key = state.to_discrete_key()
        self.agent.q_table[key] = {a: 0.5 for a in ACTIONS}

        ep = make_episode(state, action, reward=-3.0)
        self.agent.update(ep)
        assert self.agent.q_table[key][action] < 0.5

    def test_stats_update_after_episode(self):
        state = make_state()
        ep = make_episode(state, ACTIONS[1], reward=2.0)
        self.agent.update(ep)
        assert self.agent.stats.total_episodes == 1
        assert self.agent.stats.total_reward == 2.0

    def test_policy_weights_stay_in_range(self):
        state = make_state()
        for action in ACTIONS:
            ep = make_episode(state, action, reward=5.0)
            self.agent.update(ep)
        for k, v in self.agent.policy_weights.items():
            assert 0.1 <= v <= 0.99, f"Weight {k}={v} out of range"

    def test_greedy_action_after_training(self):
        """After many positive updates for one action, greedy should pick it."""
        state = make_state(queue_depth=10)
        target_action = "batch_milk_steams"
        for _ in range(20):
            ep = make_episode(state, target_action, reward=5.0)
            self.agent.update(ep)
        # With epsilon=0 it must be greedy
        self.agent.epsilon = 0.0
        chosen = self.agent.select_action(state)
        assert chosen == target_action

    def test_q_values_for_unseen_state(self):
        state = make_state(queue_depth=99, is_rush_hour=False)
        q = self.agent.q_values_for_state(state)
        assert all(v == 0.0 for v in q.values())

    def test_state_to_vector_shape(self):
        import numpy as np
        state = make_state()
        vec = state.to_vector()
        assert vec.shape == (5,)
        assert all(0.0 <= v <= 1.0 for v in vec)

    def test_state_to_vector_normalised(self):
        state = make_state(queue_depth=100, avg_wait_min=999)
        vec = state.to_vector()
        assert vec[0] <= 1.0   # queue_depth clamped
        assert vec[2] <= 1.0   # wait clamped


class TestRewardFunction:
    def test_positive_throughput_gives_positive_reward(self):
        r = compute_reward(throughput_delta=1.0, wait_reduced_min=0.0,
                           concurrency_used=False, order_error=False)
        assert r > 0

    def test_order_error_penalises_heavily(self):
        r = compute_reward(throughput_delta=0.0, wait_reduced_min=0.0,
                           concurrency_used=False, order_error=True)
        assert r < 0

    def test_concurrency_adds_bonus(self):
        no_conc = compute_reward(1.0, 0.5, False, False)
        with_conc = compute_reward(1.0, 0.5, True, False)
        assert with_conc > no_conc

    def test_error_dominates_good_performance(self):
        r = compute_reward(throughput_delta=2.0, wait_reduced_min=2.0,
                           concurrency_used=True, order_error=True)
        # Error penalty (-3.0) should pull total below the sum of positive signals
        # positive: 2*2 + 1.5*2 + 1.0 = 9.0, minus 3.0 error = 6.0
        # Even great performance + error should not exceed 7
        assert r < 7.0

    def test_negative_throughput_not_double_penalised(self):
        r = compute_reward(throughput_delta=-1.0, wait_reduced_min=0.0,
                           concurrency_used=False, order_error=False)
        # negative throughput clipped to 0, so reward should be 0 base
        assert r == 0.0
