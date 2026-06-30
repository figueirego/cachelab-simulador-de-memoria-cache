from __future__ import annotations

from collections import OrderedDict, deque
from dataclasses import dataclass
from typing import Deque, Dict, Hashable, Protocol, Set


class CachePolicy(Protocol):
    capacity: int

    def access(self, item: Hashable) -> bool:
        """Return True for hit and False for miss."""

    def contains(self, item: Hashable) -> bool:
        """Return whether the item is currently stored."""


@dataclass
class FIFOCache:
    capacity: int

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self._items: Set[Hashable] = set()
        self._order: Deque[Hashable] = deque()

    def access(self, item: Hashable) -> bool:
        if item in self._items:
            return True
        if len(self._items) >= self.capacity:
            evicted = self._order.popleft()
            self._items.remove(evicted)
        self._items.add(item)
        self._order.append(item)
        return False

    def contains(self, item: Hashable) -> bool:
        return item in self._items


@dataclass
class LRUCache:
    capacity: int

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self._items: OrderedDict[Hashable, None] = OrderedDict()

    def access(self, item: Hashable) -> bool:
        if item in self._items:
            self._items.move_to_end(item)
            return True
        if len(self._items) >= self.capacity:
            self._items.popitem(last=False)
        self._items[item] = None
        return False

    def contains(self, item: Hashable) -> bool:
        return item in self._items


@dataclass
class LFUCache:
    capacity: int

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be a positive integer")
        self._frequencies: Dict[Hashable, int] = {}
        self._insert_order: Dict[Hashable, int] = {}
        self._clock = 0

    def access(self, item: Hashable) -> bool:
        if item in self._frequencies:
            self._frequencies[item] += 1
            return True
        if len(self._frequencies) >= self.capacity:
            evicted = min(
                self._frequencies,
                key=lambda cached_item: (
                    self._frequencies[cached_item],
                    self._insert_order[cached_item],
                ),
            )
            del self._frequencies[evicted]
            del self._insert_order[evicted]
        self._clock += 1
        self._frequencies[item] = 1
        self._insert_order[item] = self._clock
        return False

    def contains(self, item: Hashable) -> bool:
        return item in self._frequencies


def create_policy(policy_name: str, capacity: int) -> CachePolicy:
    policies = {
        "fifo": FIFOCache,
        "lru": LRUCache,
        "lfu": LFUCache,
    }
    try:
        return policies[policy_name](capacity=capacity)
    except KeyError as exc:
        valid = ", ".join(sorted(policies))
        raise ValueError(f"unknown policy '{policy_name}'. Use one of: {valid}") from exc
