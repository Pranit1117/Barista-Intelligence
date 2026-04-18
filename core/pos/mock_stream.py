"""
Mock POS stream — generates realistic synthetic orders for demo and dev mode.
Simulates rush-hour demand curves, drink distribution, and occasional errors.
"""
from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass
from typing import AsyncIterator, Callable

from core.scheduler.concurrent_scheduler import Order
from core.scorer.complexity_scorer import DrinkSpec, PRESET_DRINKS

CUSTOMER_NAMES = [
    "Priya M.", "Rohan K.", "Aisha T.", "Dev S.", "Meera V.",
    "Arjun P.", "Sana R.", "Kiran L.", "Rahul G.", "Neha D.",
    "Vikram S.", "Pooja A.", "Shreya N.", "Amit B.", "Tanya C.",
]

# Drink weights — mimics real Mumbai café mix
DRINK_WEIGHTS: list[tuple[str, float]] = [
    ("oat_latte", 0.18),
    ("cappuccino", 0.16),
    ("flat_white", 0.13),
    ("americano", 0.11),
    ("cold_brew", 0.09),
    ("oat_flat_white", 0.08),
    ("cortado", 0.08),
    ("iced_latte", 0.07),
    ("matcha_latte", 0.06),
    ("espresso", 0.04),
]

DRINK_NAMES = [d for d, _ in DRINK_WEIGHTS]
DRINK_PROBS = [w for _, w in DRINK_WEIGHTS]


def _pick_drink() -> DrinkSpec:
    key = random.choices(DRINK_NAMES, weights=DRINK_PROBS, k=1)[0]
    base = PRESET_DRINKS[key]
    # Small random customizations
    extras = []
    if random.random() < 0.25:
        extras.append(random.choice(["vanilla", "hazelnut", "oat milk", "extra shot"]))
    return DrinkSpec(
        name=base.name,
        base=base.base,
        milk=base.milk,
        shots=base.shots + (1 if random.random() < 0.1 else 0),
        temp_celsius=random.choice([60, 65, 70, 75]) if random.random() < 0.2 else 65,
        extras=extras,
        iced=base.iced,
    )


def _demand_multiplier(hour: float) -> float:
    """Returns orders/minute at a given decimal hour (e.g. 8.5 = 8:30 AM)."""
    # Rush curve: peaks around 8:45 AM
    if 7.75 <= hour <= 9.25:
        peak = 8.75
        distance = abs(hour - peak)
        return max(1.0, 9.0 - distance * 6.0)
    if 12.0 <= hour <= 13.5:
        return 4.5
    return 1.2


def generate_order(order_num: int) -> Order:
    name = random.choice(CUSTOMER_NAMES)
    num_drinks = random.choices([1, 2, 3], weights=[0.65, 0.28, 0.07])[0]
    drinks = [_pick_drink() for _ in range(num_drinks)]
    return Order(
        order_id=f"#{str(order_num).zfill(3)}",
        customer_name=name,
        drinks=drinks,
        received_at=time.time(),
    )


async def mock_order_stream(
    on_order: Callable[[Order], None],
    on_error: Callable[[str], None] | None = None,
    error_rate: float = 0.03,
    speed_multiplier: float = 1.0,
) -> AsyncIterator[Order]:
    """
    Async generator that yields orders at realistic rush-hour rates.
    speed_multiplier > 1 compresses time for testing.
    """
    order_counter = 100
    while True:
        import datetime
        now = datetime.datetime.now()
        hour = now.hour + now.minute / 60

        rate = _demand_multiplier(hour)          # orders per minute
        interval = 60 / (rate * speed_multiplier)

        await asyncio.sleep(interval)

        if random.random() < error_rate:
            msg = random.choice([
                "PARSE ERROR: malformed payload on order field",
                "TIMEOUT: POS response took >2s",
                "DUPLICATE order_id detected — skipping",
            ])
            if on_error:
                on_error(msg)
            continue

        order_counter += 1
        order = generate_order(order_counter)
        on_order(order)
        yield order


def generate_rush_batch(n: int = 12) -> list[Order]:
    """Generate a batch of orders simulating a rush spike."""
    orders = []
    for i in range(n):
        order = generate_order(200 + i)
        # Stagger received_at to simulate different wait times
        order.received_at = time.time() - random.uniform(0, 7 * 60)
        orders.append(order)
    return orders
