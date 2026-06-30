from __future__ import annotations

import argparse
import sys

from cache.simulator import run_simulation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cache memory simulator")
    parser.add_argument("--input", required=True, help="CSV file containing the access trace")
    parser.add_argument(
        "--policy",
        required=True,
        choices=["fifo", "lru", "lfu"],
        help="Replacement policy: fifo, lru, or lfu",
    )
    parser.add_argument(
        "--capacity",
        required=True,
        type=int,
        help="Maximum number of items stored in cache",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = run_simulation(args.input, args.policy, args.capacity)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Policy: {result.policy}")
    print(f"Capacity: {result.capacity}")
    print(f"Total accesses: {result.total_accesses}")
    print(f"Hits: {result.hits}")
    print(f"Misses: {result.misses}")
    print(f"Hit ratio: {result.hit_ratio:.2f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
