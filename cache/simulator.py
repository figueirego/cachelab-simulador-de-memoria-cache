from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

from .policies import create_policy


@dataclass(frozen=True)
class SimulationResult:
    policy: str
    capacity: int
    total_accesses: int
    hits: int
    misses: int
    hit_ratio: float

    def as_dict(self) -> dict[str, object]:
        return {
            "policy": self.policy,
            "capacity": self.capacity,
            "total_accesses": self.total_accesses,
            "hits": self.hits,
            "misses": self.misses,
            "hit_ratio": round(self.hit_ratio, 4),
        }


def read_trace(input_path: str | Path) -> List[str]:
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"input file not found: {path}")

    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None or "item_id" not in reader.fieldnames:
            raise ValueError("CSV input must contain an item_id column")

        items: List[str] = []
        for row in reader:
            value = (row.get("item_id") or "").strip()
            if value:
                items.append(value)
        return items


def run_simulation(input_path: str | Path, policy_name: str, capacity: int) -> SimulationResult:
    if capacity <= 0:
        raise ValueError("capacity must be a positive integer")

    normalized_policy = policy_name.lower()
    trace = read_trace(input_path)
    if not trace:
        raise ValueError("CSV input must contain at least one access")

    policy = create_policy(normalized_policy, capacity)
    hits = 0
    misses = 0

    for item in trace:
        if policy.access(item):
            hits += 1
        else:
            misses += 1

    total_accesses = hits + misses
    hit_ratio = (hits / total_accesses) * 100
    return SimulationResult(
        policy=normalized_policy,
        capacity=capacity,
        total_accesses=total_accesses,
        hits=hits,
        misses=misses,
        hit_ratio=hit_ratio,
    )
