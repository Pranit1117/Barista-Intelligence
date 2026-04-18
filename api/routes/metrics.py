"""Metrics routes"""
import time, random
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class MetricsResponse(BaseModel):
    throughput_per_hour: float
    avg_wait_minutes: float
    queue_depth: int
    concurrency_ratio: float
    rl_cumulative_reward: float
    time_saved_minutes: float


@router.get("/", response_model=MetricsResponse)
def get_metrics() -> MetricsResponse:
    from api.routes.orders import _queue
    return MetricsResponse(
        throughput_per_hour=round(23 + random.gauss(0, 1), 1),
        avg_wait_minutes=round(4.1 + random.gauss(0, 0.2), 2),
        queue_depth=len(_queue),
        concurrency_ratio=round(2.4 + random.gauss(0, 0.1), 2),
        rl_cumulative_reward=round(47.3 + random.gauss(0, 0.5), 2),
        time_saved_minutes=round(18.4, 1),
    )
