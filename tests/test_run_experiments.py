import csv
import subprocess
import sys

from scripts.run_experiments import plot_results, run_experiments, write_results


def write_trace(path):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["item_id"])
        writer.writerows([["A"], ["B"], ["A"], ["C"], ["A"], ["B"]])


def test_run_experiments_returns_policy_capacity_matrix(tmp_path):
    trace_path = tmp_path / "trace.csv"
    write_trace(trace_path)

    results = run_experiments(trace_path, capacities=[1, 2])

    assert len(results) == 6
    assert sorted({result.policy for result in results}) == ["fifo", "lfu", "lru"]
    assert sorted({result.capacity for result in results}) == [1, 2]


def test_write_results_and_plot_create_output_files(tmp_path):
    trace_path = tmp_path / "trace.csv"
    results_path = tmp_path / "results.csv"
    chart_path = tmp_path / "chart.png"
    write_trace(trace_path)
    results = run_experiments(trace_path, capacities=[1, 2])

    write_results(results, results_path)
    plot_results(results, chart_path)

    assert results_path.exists()
    assert chart_path.exists()
    assert results_path.stat().st_size > 0
    assert chart_path.stat().st_size > 0


def test_run_experiments_script_can_be_executed_directly(tmp_path):
    trace_path = tmp_path / "trace.csv"
    results_path = tmp_path / "results.csv"
    chart_path = tmp_path / "chart.png"
    write_trace(trace_path)

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_experiments.py",
            "--input",
            str(trace_path),
            "--output",
            str(results_path),
            "--chart",
            str(chart_path),
            "--capacities",
            "1",
            "2",
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "FIFO capacity=1" in completed.stdout
    assert results_path.exists()
    assert chart_path.exists()
