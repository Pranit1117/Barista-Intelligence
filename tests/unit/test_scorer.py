"""Unit tests for the complexity scorer."""
import pytest
from core.scorer.complexity_scorer import (
    DrinkSpec,
    score_drink,
    score_all_presets,
    PRESET_DRINKS,
)


class TestScoreDrink:
    def test_simple_espresso_is_low(self):
        drink = DrinkSpec("Espresso", base="espresso", milk="none", shots=1)
        result = score_drink(drink)
        assert result.total < 4.0
        assert result.tier == "low"
        assert result.concurrent_slots_needed == 1

    def test_matcha_latte_is_high(self):
        drink = DrinkSpec("Matcha latte", base="filter", milk="oat", shots=0, extras=["matcha"])
        result = score_drink(drink)
        assert result.total > 7.0
        assert result.tier == "high"
        assert result.concurrent_slots_needed == 3

    def test_oat_adds_more_than_whole_milk(self):
        whole = score_drink(DrinkSpec("Latte", base="espresso", milk="whole", shots=2))
        oat = score_drink(DrinkSpec("Oat latte", base="espresso", milk="oat", shots=2))
        assert oat.total > whole.total

    def test_extras_increase_score(self):
        plain = score_drink(DrinkSpec("Latte", base="espresso", milk="whole", shots=2))
        fancy = score_drink(DrinkSpec("Fancy latte", base="espresso", milk="whole", shots=2,
                                      extras=["vanilla", "hazelnut", "caramel"]))
        assert fancy.total > plain.total

    def test_score_capped_at_10(self):
        drink = DrinkSpec("Max drink", base="ristretto", milk="oat", shots=4,
                          extras=["vanilla", "hazelnut", "caramel", "matcha", "syrup"])
        result = score_drink(drink)
        assert result.total <= 10.0

    def test_score_non_negative(self):
        drink = DrinkSpec("Min drink", base="cold_brew", milk="none", shots=0)
        result = score_drink(drink)
        assert result.total >= 0.0

    def test_iced_reduces_temp_score(self):
        hot = score_drink(DrinkSpec("Hot latte", base="espresso", milk="whole", shots=2, iced=False))
        iced = score_drink(DrinkSpec("Iced latte", base="espresso", milk="whole", shots=2, iced=True))
        assert iced.temp_score < hot.temp_score

    def test_ristretto_scores_higher_extraction_than_espresso(self):
        rist = score_drink(DrinkSpec("R", base="ristretto", milk="none", shots=1))
        esp = score_drink(DrinkSpec("E", base="espresso", milk="none", shots=1))
        assert rist.extraction_score > esp.extraction_score

    def test_shot_count_affects_score(self):
        single = score_drink(DrinkSpec("Single", base="espresso", milk="none", shots=1))
        double = score_drink(DrinkSpec("Double", base="espresso", milk="none", shots=2))
        quad = score_drink(DrinkSpec("Quad", base="espresso", milk="none", shots=4))
        assert single.total < double.total < quad.total

    def test_label_matches_tier(self):
        drink = DrinkSpec("Latte", base="espresso", milk="oat", shots=2)
        result = score_drink(drink)
        if result.total > 8.5:
            assert result.label == "Very complex"
        elif result.total > 7.0:
            assert result.label == "Complex"
        elif result.total > 5.0:
            assert result.label == "Moderate"


class TestAllPresets:
    def test_all_presets_score(self):
        results = score_all_presets()
        assert len(results) == len(PRESET_DRINKS)
        for name, result in results.items():
            assert 0 <= result.total <= 10, f"{name} out of range: {result.total}"

    def test_cold_brew_lowest(self):
        results = score_all_presets()
        scores = {k: v.total for k, v in results.items()}
        assert scores["cold_brew"] < scores["oat_latte"]
        assert scores["espresso"] < scores["matcha_latte"]

    def test_concurrent_slots_range(self):
        results = score_all_presets()
        for name, r in results.items():
            assert r.concurrent_slots_needed in (1, 2, 3), (
                f"{name} has unexpected slot count: {r.concurrent_slots_needed}"
            )
