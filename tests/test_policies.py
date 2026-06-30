from cache.policies import FIFOCache, LFUCache, LRUCache


def test_fifo_evicts_oldest_inserted_item():
    cache = FIFOCache(capacity=2)

    assert cache.access("A") is False
    assert cache.access("B") is False
    assert cache.access("A") is True
    assert cache.access("C") is False

    assert cache.contains("A") is False
    assert cache.contains("B") is True
    assert cache.contains("C") is True


def test_lru_evicts_least_recently_used_item():
    cache = LRUCache(capacity=2)

    assert cache.access("A") is False
    assert cache.access("B") is False
    assert cache.access("A") is True
    assert cache.access("C") is False

    assert cache.contains("A") is True
    assert cache.contains("B") is False
    assert cache.contains("C") is True


def test_lfu_evicts_least_frequently_used_item():
    cache = LFUCache(capacity=2)

    assert cache.access("A") is False
    assert cache.access("B") is False
    assert cache.access("A") is True
    assert cache.access("C") is False

    assert cache.contains("A") is True
    assert cache.contains("B") is False
    assert cache.contains("C") is True


def test_lfu_breaks_frequency_ties_by_oldest_insertion():
    cache = LFUCache(capacity=2)

    assert cache.access("A") is False
    assert cache.access("B") is False
    assert cache.access("C") is False

    assert cache.contains("A") is False
    assert cache.contains("B") is True
    assert cache.contains("C") is True
