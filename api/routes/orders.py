"""Orders routes — POST /orders, GET /queue"""
import time
from typing import Annotated
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# In-memory queue (replace with Redis in production)
_queue: list[dict] = []


class DrinkIn(BaseModel):
    name: str
    base: str = "espresso"
    milk: str = "whole"
    shots: int = 2
    temp_celsius: int = 65
    extras: list[str] = []
    iced: bool = False


class OrderIn(BaseModel):
    order_id: str | None = None
    customer_name: str
    drinks: list[DrinkIn] = Field(min_length=1)


class OrderOut(BaseModel):
    order_id: str
    customer_name: str
    drinks: list[DrinkIn]
    received_at: float
    wait_seconds: float
    complexity_score: float


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(body: OrderIn) -> OrderOut:
    from core.scorer.complexity_scorer import score_drink, DrinkSpec
    import uuid

    order_id = body.order_id or f"#{str(uuid.uuid4())[:6].upper()}"
    received_at = time.time()

    # Score complexity
    scores = [
        score_drink(DrinkSpec(
            name=d.name, base=d.base, milk=d.milk,  # type: ignore[arg-type]
            shots=d.shots, temp_celsius=d.temp_celsius,
            extras=d.extras, iced=d.iced
        ))
        for d in body.drinks
    ]
    avg_complexity = sum(s.total for s in scores) / len(scores)

    entry = {
        "order_id": order_id,
        "customer_name": body.customer_name,
        "drinks": [d.model_dump() for d in body.drinks],
        "received_at": received_at,
        "complexity_score": avg_complexity,
    }
    _queue.append(entry)

    return OrderOut(
        **entry,
        wait_seconds=0.0,
    )


@router.get("/queue", response_model=list[OrderOut])
def get_queue() -> list[OrderOut]:
    now = time.time()
    return [
        OrderOut(
            **o,
            wait_seconds=round(now - o["received_at"], 1),
        )
        for o in _queue
    ]


@router.delete("/{order_id}")
def complete_order(order_id: str) -> dict:
    global _queue
    before = len(_queue)
    _queue = [o for o in _queue if o["order_id"] != order_id]
    if len(_queue) == before:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return {"status": "completed", "order_id": order_id}
