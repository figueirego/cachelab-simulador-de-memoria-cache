import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scripts.generate_report import best_policy, build_report, load_results


def write_results(path):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["policy", "capacity", "total_accesses", "hits", "misses", "hit_ratio"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "policy": "fifo",
                "capacity": "100",
                "total_accesses": "10",
                "hits": "4",
                "misses": "6",
                "hit_ratio": "40.0",
            }
        )
        writer.writerow(
            {
                "policy": "lfu",
                "capacity": "100",
                "total_accesses": "10",
                "hits": "7",
                "misses": "3",
                "hit_ratio": "70.0",
            }
        )


def write_chart(path):
    plt.figure(figsize=(2, 1.5))
    plt.plot([100], [70], marker="o")
    plt.tight_layout()
    plt.savefig(path, dpi=80)
    plt.close()


def test_load_results_and_best_policy(tmp_path):
    results_path = tmp_path / "results.csv"
    write_results(results_path)

    rows = load_results(results_path)

    assert len(rows) == 2
    assert best_policy(rows).startswith("LFU")


def test_build_report_creates_pdf(tmp_path):
    results_path = tmp_path / "results.csv"
    chart_path = tmp_path / "chart.png"
    output_path = tmp_path / "report.pdf"
    write_results(results_path)
    write_chart(chart_path)

    build_report(results_path, chart_path, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0
