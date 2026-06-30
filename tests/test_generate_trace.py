import csv

from scripts.generate_trace import generate_items, write_trace


def test_generate_items_returns_requested_number_of_accesses():
    items = generate_items(rows=10000, seed=42)

    assert len(items) == 10000
    assert all(item for item in items)


def test_write_trace_creates_item_id_csv(tmp_path):
    output_path = tmp_path / "trace.csv"

    write_trace(output_path, rows=10000, seed=42)

    with output_path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert reader.fieldnames == ["item_id"]
    assert len(rows) == 10000
