"""
Drink complexity scorer.
Produces a 0–10 complexity score from drink features.
Higher score = more machine time, more concurrent slots needed.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

MilkType = Literal["none", "whole", "oat", "almond", "soy", "coconut"]
BaseType = Literal["espresso", "ristretto", "lungo", "cold_brew", "filter"]

MILK_COMPLEXITY: dict[MilkType, float] = {
    "none": 0.0,
    "whole": 1.4,
    "soy": 1.6,
    "almond": 1.8,
    "coconut": 1.9,
    "oat": 2.0,
}

# Extras that require significant additional prep steps (powder sifting, layering, etc.)
HIGH_COMPLEXITY_EXTRAS: set[str] = {"matcha", "masala", "turmeric", "beetroot", "charcoal"}

BASE_EXTRACTION: dict[BaseType, float] = {
    "cold_brew": 1.2,
    "filter": 2.0,   # filter/indirect bases (matcha, chai) involve separate prep steps
    "espresso": 2.4,
    "lungo": 2.8,
    "ristretto": 3.2,
}

BASE_EXTRACTION_SECS: dict[BaseType, int] = {
    "cold_brew": 0,       # pre-brewed
    "filter": 0,          # pre-brewed
    "espresso": 28,
    "lungo": 35,
    "ristretto": 22,
}


@dataclass
class DrinkSpec:
    name: str
    base: BaseType = "espresso"
    milk: MilkType = "whole"
    shots: int = 2
    temp_celsius: int = 65
    extras: list[str] = field(default_factory=list)
    iced: bool = False


@dataclass
class ComplexityResult:
    total: float
    extraction_score: float
    milk_score: float
    customization_score: float
    temp_score: float
    shot_score: float
    tier: str
    concurrent_slots_needed: int
    extraction_seconds: int
    label: str

    @property
    def is_high(self) -> bool:
        return self.total > 7.0

    @property
    def is_concurrent_candidate(self) -> bool:
        return self.concurrent_slots_needed > 1


def score_drink(drink: DrinkSpec) -> ComplexityResult:
    """
    Score a drink across 5 feature dimensions.
    Weights are calibrated from real café observation data.
    """
    extraction = BASE_EXTRACTION.get(drink.base, 2.4)
    milk = MILK_COMPLEXITY.get(drink.milk, 1.4)
    customization = _customization_score(drink.extras)
    temp = _temp_score(drink.temp_celsius, drink.iced)
    shots = drink.shots * 0.4

    # Powder-prep bonus: filter-base drinks with high-complexity extras (matcha, masala)
    # require a separate whisking/sifting vessel — a genuine extra concurrent step.
    powder_bonus = 0.8 if (drink.base == "filter" and
                           any(e.lower() in HIGH_COMPLEXITY_EXTRAS for e in drink.extras)) else 0.0

    total = round(min(10.0, extraction + milk + customization + temp + shots + powder_bonus), 2)

    return ComplexityResult(
        total=total,
        extraction_score=extraction,
        milk_score=milk,
        customization_score=customization,
        temp_score=temp,
        shot_score=shots,
        tier=_tier(total),
        concurrent_slots_needed=_slots(total),
        extraction_seconds=BASE_EXTRACTION_SECS.get(drink.base, 28),
        label=_label(total),
    )


def _customization_score(extras: list[str]) -> float:
    """
    Extras that require extra prep steps (powder sifting, syrup layering)
    score at 1.5x vs simple flavour extras like vanilla or hazelnut.
    """
    score = 0.0
    for extra in extras:
        if extra.lower() in HIGH_COMPLEXITY_EXTRAS:
            score += 1.5
        else:
            score += 0.7
    return min(score, 3.0)


def _temp_score(temp: int, iced: bool) -> float:
    if iced:
        return 0.4
    if temp > 75:
        return 1.2
    if temp < 60:
        return 0.6
    return 0.8


def _tier(score: float) -> str:
    if score > 7.0:
        return "high"
    if score > 4.5:
        return "medium"
    return "low"


def _label(score: float) -> str:
    if score > 8.5:
        return "Very complex"
    if score > 7.0:
        return "Complex"
    if score > 5.0:
        return "Moderate"
    if score > 3.0:
        return "Simple"
    return "Very simple"


def _slots(score: float) -> int:
    """How many concurrent machine slots this drink benefits from."""
    if score > 7.0:
        return 3   # grind + pull + steam simultaneously
    if score > 4.5:
        return 2   # pull + steam concurrent
    return 1       # sequential is fine


# ── Preset drinks ─────────────────────────────────────────────────────────────
PRESET_DRINKS: dict[str, DrinkSpec] = {
    "oat_latte": DrinkSpec("Oat latte", base="espresso", milk="oat", shots=2, extras=[]),
    "oat_flat_white": DrinkSpec("Oat flat white", base="ristretto", milk="oat", shots=2),
    "cappuccino": DrinkSpec("Cappuccino", base="espresso", milk="whole", shots=2),
    "cortado": DrinkSpec("Cortado", base="ristretto", milk="whole", shots=2),
    "flat_white": DrinkSpec("Flat white", base="ristretto", milk="whole", shots=2),
    "matcha_latte": DrinkSpec("Matcha latte", base="filter", milk="oat", shots=0, extras=["matcha"]),
    "iced_latte": DrinkSpec("Iced latte", base="espresso", milk="whole", shots=2, iced=True),
    "americano": DrinkSpec("Americano", base="lungo", milk="none", shots=2),
    "cold_brew": DrinkSpec("Cold brew", base="cold_brew", milk="none", shots=0),
    "espresso": DrinkSpec("Espresso", base="espresso", milk="none", shots=1),
}


def score_all_presets() -> dict[str, ComplexityResult]:
    return {name: score_drink(spec) for name, spec in PRESET_DRINKS.items()}
