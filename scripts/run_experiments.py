from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cache.simulator import SimulationResult, run_simulation


DEFAULT_POLICIES = ["fifo", "lru", "lfu"]
DEFAULT_CAPACITIES = [100, 500, 1000]


def write_results(results: list[SimulationResult], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        fieldnames = ["policy", "capacity", "total_accesses", "hits", "misses", "hit_ratio"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result.as_dict())


def plot_results(results: list[SimulationResult], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    capacities = sorted({result.capacity for result in results})

    plt.figure(figsize=(9, 5.5))
    for policy in DEFAULT_POLICIES:
        policy_results = sorted(
            [result for result in results if result.policy == policy],
            key=lambda result: result.capacity,
        )
        policy_capacities = [result.capacity for result in policy_results]
        hit_ratios = [result.hit_ratio for result in policy_results]
        plt.plot(policy_capacities, hit_ratios, marker="o", linewidth=2, label=policy.upper())

    plt.title("Hit ratio por politica e capacidade")
    plt.xlabel("Capacidade do cache")
    plt.ylabel("Hit ratio (%)")
    plt.xticks(capacities)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def run_experiments(input_path: Path, capacities: list[int]) -> list[SimulationResult]:
    results: list[SimulationResult] = []
    for policy in DEFAULT_POLICIES:
        for capacity in capacities:
            results.append(run_simulation(input_path, policy, capacity))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run cache policy experiments")
    parser.add_argument("--input", default="data/trace.csv")
    parser.add_argument("--output", default="results/experiment_results.csv")
    parser.add_argument("--chart", default="results/hit_ratio_by_policy.png")
    parser.add_argument("--capacities", nargs="+", type=int, default=DEFAULT_CAPACITIES)
    args = parser.parse_args()

    results = run_experiments(Path(args.input), args.capacities)
    write_results(results, Path(args.output))
    plot_results(results, Path(args.chart))
    for result in results:
        print(
            f"{result.policy.upper()} capacity={result.capacity} "
            f"hits={result.hits} misses={result.misses} hit_ratio={result.hit_ratio:.2f}%"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
