import csv
import subprocess
import sys


def test_cli_prints_required_metrics(tmp_path):
    trace_path = tmp_path / "trace.csv"
    with trace_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["item_id"])
        writer.writerows([["A"], ["B"], ["A"]])

    completed = subprocess.run(
        [
            sys.executable,
            "cache_simulator.py",
            "--input",
            str(trace_path),
            "--policy",
            "lru",
            "--capacity",
            "2",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "Policy: lru" in completed.stdout
    assert "Capacity: 2" in completed.stdout
    assert "Total accesses: 3" in completed.stdout
    assert "Hits: 1" in completed.stdout
    assert "Misses: 2" in completed.stdout
    assert "Hit ratio: 33.33%" in completed.stdout
