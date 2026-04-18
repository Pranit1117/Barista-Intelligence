"""Scheduler routes — GET /schedule, POST /complete"""
import time
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ScheduleResponse(BaseModel):
    action_main: str
    action_sub: str
    concurrent_main: str
    concurrent_sub: str
    total_time_secs: int
    concurrency_ratio: float
    time_saved_vs_serial_secs: int


@router.get("/", response_model=ScheduleResponse)
def get_schedule() -> ScheduleResponse:
    """
    Returns the current optimal action for the barista.
    Pulls from the live order queue and runs the scheduler.
    """
    from api.routes.orders import _queue
    from core.scheduler.concurrent_scheduler import (
        ConcurrentScheduler, Order, make_action_text
    )
    from core.scorer.complexity_scorer import DrinkSpec

    orders = [
        Order(
            order_id=o["order_id"],
            customer_name=o["customer_name"],
            drinks=[DrinkSpec(name=d["name"], base=d["base"], milk=d["milk"],
                              shots=d["shots"], temp_celsius=d["temp_celsius"],
                              extras=d["extras"], iced=d["iced"])
                    for d in o["drinks"]],
            received_at=o["received_at"],
        )
        for o in _queue
    ]

    scheduler = ConcurrentScheduler()
    result = scheduler.schedule(orders)
    action_main, action_sub, conc_main, conc_sub = make_action_text(result)

    return ScheduleResponse(
        action_main=action_main,
        action_sub=action_sub,
        concurrent_main=conc_main,
        concurrent_sub=conc_sub,
        total_time_secs=result.total_time_secs,
        concurrency_ratio=result.concurrency_ratio,
        time_saved_vs_serial_secs=result.time_saved_vs_serial_secs,
    )


@router.post("/complete/{order_id}")
def mark_complete(order_id: str, time_taken_secs: float = 0.0) -> dict:
    """
    Signal order completion — triggers RL reward update.
    """
    # TODO: compute actual reward, call agent.update()
    return {
        "status": "ok",
        "order_id": order_id,
        "rl_reward_signal": round(1.5 + time_taken_secs * 0.01, 3),
    }
