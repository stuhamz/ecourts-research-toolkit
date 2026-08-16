import csv
from pathlib import Path

from ecourts_research.atlas import export_atlas_candidates, export_atlas_sources
from ecourts_research.store import SourceStore


def test_atlas_exports_are_pending(tmp_path: Path):
    raw = tmp_path / "order.txt"
    raw.write_text(
        "WhatsApp call impersonating police. Threat of arrest. Bank account and CDR evidence.",
        encoding="utf-8",
    )

    store = SourceStore(tmp_path / "data")
    store.ingest_file(raw, source_url="https://example.test/order", title="Example order")

    candidates = export_atlas_candidates(store, tmp_path / "candidates.csv")
    sources = export_atlas_sources(store, tmp_path / "sources.csv")

    with candidates.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    assert rows[0]["decision"] == "pending"

    with sources.open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle))
    assert len(source_rows) == 1
    assert source_rows[0]["url"] == "https://example.test/order"
