"""
Q-learning RL agent for barista scheduling policy.
State: (queue_depth, top_complexity, wait_pressure, machine_busy_count)
Actions: scheduling strategies the scheduler can apply
Reward: throughput gain - wait penalty + concurrency bonus
"""
from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

import numpy as np


# ── State & Action definitions ────────────────────────────────────────────────

@dataclass
class CafeState:
    queue_depth: int            # 0–20+
    top_complexity: float       # 0–10
    avg_wait_min: float         # 0–15
    machine_busy_count: int     # 0–4
    is_rush_hour: bool

    def to_vector(self) -> np.ndarray:
        return np.array([
            min(self.queue_depth / 20, 1.0),
            self.top_complexity / 10,
            min(self.avg_wait_min / 10, 1.0),
            self.machine_busy_count / 4,
            float(self.is_rush_hour),
        ], dtype=np.float32)

    def to_discrete_key(self) -> tuple:
        """Discretize for tabular Q-learning."""
        return (
            min(self.queue_depth // 3, 6),
            int(self.top_complexity // 2),
            min(int(self.avg_wait_min), 8),
            self.machine_busy_count,
            int(self.is_rush_hour),
        )


ACTIONS = [
    "prioritize_wait_time",
    "prioritize_complexity",
    "batch_milk_steams",
    "maximize_concurrency",
    "use_idle_machine",
    "reorder_by_score",
]


@dataclass
class Episode:
    episode_id: int
    state: CafeState
    action: str
    reward: float
    next_state: Optional[CafeState]
    done: bool
    throughput_delta: float
    wait_delta: float


@dataclass
class AgentStats:
    total_episodes: int = 0
    total_reward: float = 0.0
    avg_reward_last_100: float = 0.0
    best_episode_reward: float = float("-inf")
    policy_improvement_pct: float = 0.0
    recent_rewards: list[float] = field(default_factory=list)


class QLearningAgent:
    """
    Tabular Q-learning agent.
    In production this can be swapped for a DQN with the same interface.
    """

    def __init__(
        self,
        learning_rate: float = 0.03,
        discount_factor: float = 0.95,
        epsilon: float = 0.12,
        checkpoint_path: str = "data/models/rl_policy.pkl",
    ):
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.checkpoint_path = Path(checkpoint_path)
        self.q_table: dict[tuple, dict[str, float]] = {}
        self.stats = AgentStats()
        self._episode_counter = 0

        # Policy feature weights (updated after each episode)
        self.policy_weights: dict[str, float] = {
            "wait_time": 0.88,
            "complexity": 0.72,
            "concurrency_fit": 0.91,
            "machine_load": 0.45,
            "milk_type": 0.63,
            "shot_count": 0.38,
        }

    # ── Core Q-learning ───────────────────────────────────────────────────────

    def select_action(self, state: CafeState) -> str:
        """Epsilon-greedy action selection."""
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)
        return self._greedy_action(state)

    def update(self, episode: Episode) -> float:
        """Bellman update. Returns TD error."""
        key = episode.state.to_discrete_key()
        if key not in self.q_table:
            self.q_table[key] = {a: 0.0 for a in ACTIONS}

        current_q = self.q_table[key][episode.action]

        if episode.done or episode.next_state is None:
            target = episode.reward
        else:
            next_key = episode.next_state.to_discrete_key()
            next_q = self.q_table.get(next_key, {a: 0.0 for a in ACTIONS})
            target = episode.reward + self.gamma * max(next_q.values())

        td_error = target - current_q
        self.q_table[key][episode.action] += self.lr * td_error

        self._update_stats(episode.reward)
        self._update_weights(episode)
        self._episode_counter += 1

        return td_error

    def _greedy_action(self, state: CafeState) -> str:
        key = state.to_discrete_key()
        if key not in self.q_table:
            return ACTIONS[0]
        return max(self.q_table[key], key=self.q_table[key].get)

    def _update_stats(self, reward: float) -> None:
        self.stats.total_episodes += 1
        self.stats.total_reward += reward
        self.stats.recent_rewards.append(reward)
        if len(self.stats.recent_rewards) > 100:
            self.stats.recent_rewards.pop(0)
        self.stats.avg_reward_last_100 = round(
            sum(self.stats.recent_rewards) / len(self.stats.recent_rewards), 3
        )
        if reward > self.stats.best_episode_reward:
            self.stats.best_episode_reward = reward

    def _update_weights(self, episode: Episode) -> None:
        """Nudge policy weights based on what worked."""
        sign = 1.0 if episode.reward > 0 else -1.0
        delta = 0.005 * abs(episode.reward) * sign

        if episode.action in ("prioritize_wait_time", "reorder_by_score"):
            self.policy_weights["wait_time"] = _clamp(
                self.policy_weights["wait_time"] + delta
            )
        if episode.action in ("batch_milk_steams", "maximize_concurrency"):
            self.policy_weights["concurrency_fit"] = _clamp(
                self.policy_weights["concurrency_fit"] + delta
            )
        if episode.action == "prioritize_complexity":
            self.policy_weights["complexity"] = _clamp(
                self.policy_weights["complexity"] + delta
            )

    # ── Q-value inspection ────────────────────────────────────────────────────

    def q_values_for_state(self, state: CafeState) -> dict[str, float]:
        key = state.to_discrete_key()
        return self.q_table.get(key, {a: 0.0 for a in ACTIONS})

    # ── Checkpoint I/O ────────────────────────────────────────────────────────

    def save(self) -> None:
        import joblib
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {"q_table": self.q_table, "weights": self.policy_weights, "stats": asdict(self.stats)},
            self.checkpoint_path,
        )

    def load(self) -> bool:
        if not self.checkpoint_path.exists():
            return False
        import joblib
        data = joblib.load(self.checkpoint_path)
        self.q_table = data.get("q_table", {})
        self.policy_weights = data.get("weights", self.policy_weights)
        return True


def _clamp(v: float, lo: float = 0.1, hi: float = 0.99) -> float:
    return round(max(lo, min(hi, v)), 4)


# ── Reward shaping ────────────────────────────────────────────────────────────

def compute_reward(
    throughput_delta: float,
    wait_reduced_min: float,
    concurrency_used: bool,
    order_error: bool,
) -> float:
    """
    Reward function:
      +2.0 per order/min throughput gained
      +1.5 per minute of wait reduced
      +1.0 if concurrency slot was used
      −3.0 for order errors (wrong drink, re-make)
    """
    r = 0.0
    r += 2.0 * max(0.0, throughput_delta)
    r += 1.5 * max(0.0, wait_reduced_min)
    if concurrency_used:
        r += 1.0
    if order_error:
        r -= 3.0
    return round(r, 3)
