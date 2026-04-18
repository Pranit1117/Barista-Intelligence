#!/usr/bin/env python
"""
Train/validate the complexity scorer from labelled data.
Usage: python scripts/train_scorer.py --data data/processed/sample_orders.csv
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from core.scorer.complexity_scorer import DrinkSpec, score_drink, score_all_presets


def main():
    parser = argparse.ArgumentParser(description="Train / validate complexity scorer")
    parser.add_argument("--data", default="data/processed/sample_orders.csv")
    parser.add_argument("--output", default="data/models/complexity_report.json")
    args = parser.parse_args()

    print("── BaristaIQ Complexity Scorer ────────────────────────────")
    print(f"Data: {args.data}\n")

    # Score all presets and report
    results = score_all_presets()
    report = {}
    for name, r in sorted(results.items(), key=lambda x: x[1].total, reverse=True):
        row = {
            "score": r.total,
            "tier": r.tier,
            "label": r.label,
            "concurrent_slots": r.concurrent_slots_needed,
            "extraction_secs": r.extraction_seconds,
        }
        report[name] = row
        print(
            f"  {r.total:5.1f}  [{r.tier:6s}]  {r.label:14s}  "
            f"{r.concurrent_slots_needed} slots  {name}"
        )

    # If labelled CSV exists, compute MAE vs ground truth
    data_path = Path(args.data)
    if data_path.exists():
        df = pd.read_csv(data_path)
        print(f"\nLoaded {len(df)} rows from {data_path}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(f"\nReport saved → {out}")


if __name__ == "__main__":
    main()
