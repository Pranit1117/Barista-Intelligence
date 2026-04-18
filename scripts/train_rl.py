#!/usr/bin/env python
"""
Train the RL agent via simulated rush episodes.
Usage: python scripts/train_rl.py --episodes 2000 --save
"""
import argparse
import random
import time

from core.rl.agent import (
    QLearningAgent, CafeState, Episode, ACTIONS, compute_reward
)
from core.pos.mock_stream import generate_rush_batch
from core.scheduler.concurrent_scheduler import ConcurrentScheduler


def simulate_episode(agent: QLearningAgent, scheduler: ConcurrentScheduler,
                     episode_id: int) -> Episode:
    orders = generate_rush_batch(random.randint(4, 14))

    state = CafeState(
        queue_depth=len(orders),
        top_complexity=max(
            (s.complexity.total for o in orders for d in o.drinks
             for s in [__import__('core.scorer.complexity_scorer', fromlist=['score_drink']).score_drink(d)]),
            default=5.0
        ),
        avg_wait_min=sum(o.wait_minutes for o in orders) / len(orders),
        machine_busy_count=random.randint(0, 4),
        is_rush_hour=True,
    )

    action = agent.select_action(state)
    result = scheduler.schedule(orders)

    # Simulate outcome
    throughput_delta = result.concurrency_ratio * 0.8 + random.gauss(0, 0.3)
    wait_reduced = max(0, result.time_saved_vs_serial_secs / 60)
    concurrency_used = result.concurrency_ratio > 1.5
    order_error = random.random() < 0.05

    reward = compute_reward(throughput_delta, wait_reduced, concurrency_used, order_error)

    next_state = CafeState(
        queue_depth=max(0, len(orders) - 2),
        top_complexity=state.top_complexity * 0.9,
        avg_wait_min=max(0, state.avg_wait_min - wait_reduced),
        machine_busy_count=random.randint(0, 3),
        is_rush_hour=True,
    )

    return Episode(
        episode_id=episode_id,
        state=state,
        action=action,
        reward=reward,
        next_state=next_state,
        done=False,
        throughput_delta=throughput_delta,
        wait_delta=wait_reduced,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=500)
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--checkpoint", default="data/models/rl_policy.pkl")
    args = parser.parse_args()

    agent = QLearningAgent(checkpoint_path=args.checkpoint)
    scheduler = ConcurrentScheduler()

    print("── BaristaIQ RL Training ──────────────────────────────────")
    print(f"Episodes: {args.episodes}  |  Checkpoint: {args.checkpoint}\n")

    best_avg = float("-inf")
    for ep_id in range(1, args.episodes + 1):
        episode = simulate_episode(agent, scheduler, ep_id)
        agent.update(episode)

        if ep_id % 100 == 0:
            avg = agent.stats.avg_reward_last_100
            print(
                f"  ep {ep_id:5d}  avg_reward={avg:+.3f}  "
                f"ε={agent.epsilon:.3f}  best={agent.stats.best_episode_reward:+.2f}"
            )
            if avg > best_avg:
                best_avg = avg
                if args.save:
                    agent.save()
                    print(f"           ↳ checkpoint saved (new best: {avg:+.3f})")

        # Epsilon decay
        agent.epsilon = max(0.05, agent.epsilon * 0.9995)

    print(f"\nTraining complete. Final avg reward: {agent.stats.avg_reward_last_100:+.3f}")
    print(f"Policy weights: {agent.policy_weights}")

    if args.save:
        agent.save()
        print(f"Final model saved → {args.checkpoint}")


if __name__ == "__main__":
    main()
