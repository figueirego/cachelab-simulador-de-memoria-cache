import csv

import pytest

from cache.simulator import read_trace, run_simulation


def write_trace(path, values):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["item_id"])
        for value in values:
            writer.writerow([value])


def test_read_trace_reads_item_id_column(tmp_path):
    trace_path = tmp_path / "trace.csv"
    write_trace(trace_path, ["10", "15", "10"])

    assert read_trace(trace_path) == ["10", "15", "10"]


def test_read_trace_rejects_missing_item_id_column(tmp_path):
    trace_path = tmp_path / "trace.csv"
    trace_path.write_text("id\n1\n", encoding="utf-8")

    with pytest.raises(ValueError, match="item_id"):
        read_trace(trace_path)


def test_run_simulation_counts_fifo_metrics(tmp_path):
    trace_path = tmp_path / "trace.csv"
    write_trace(trace_path, ["A", "B", "A", "C", "A"])

    result = run_simulation(trace_path, "fifo", 2)

    assert result.total_accesses == 5
    assert result.hits == 1
    assert result.misses == 4
    assert result.hit_ratio == 20.0


def test_run_simulation_rejects_empty_trace(tmp_path):
    trace_path = tmp_path / "trace.csv"
    trace_path.write_text("item_id\n", encoding="utf-8")

    with pytest.raises(ValueError, match="at least one access"):
        run_simulation(trace_path, "lru", 10)
