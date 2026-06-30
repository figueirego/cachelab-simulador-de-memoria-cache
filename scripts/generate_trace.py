from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path


def generate_items(rows: int, seed: int) -> list[str]:
    random.seed(seed)
    hot_items = [f"hot_{number}" for number in range(1, 101)]
    warm_items = [f"warm_{number}" for number in range(1, 901)]
    cold_items = [f"cold_{number}" for number in range(1, 4001)]
    items: list[str] = []

    for index in range(rows):
        if index % 250 == 0:
            items.extend(hot_items[:20])
            continue
        bucket = random.random()
        if bucket < 0.70:
            items.append(random.choice(hot_items))
        elif bucket < 0.92:
            items.append(random.choice(warm_items))
        else:
            items.append(random.choice(cold_items))

    return items[:rows]


def write_trace(output_path: Path, rows: int, seed: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["item_id"])
        for item in generate_items(rows, seed):
            writer.writerow([item])


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a synthetic cache access trace")
    parser.add_argument("--output", default="data/trace.csv")
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.rows < 10000:
        parser.error("--rows must be at least 10000 for the assignment")

    write_trace(Path(args.output), args.rows, args.seed)
    print(f"Generated {args.rows} accesses at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
