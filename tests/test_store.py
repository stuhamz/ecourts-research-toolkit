import json
from pathlib import Path

from ecourts_research.store import SourceStore


def test_ingest_file_preserves_hash_and_text(tmp_path: Path):
    source = tmp_path / "order.txt"
    source.write_text("WhatsApp impersonation and bank transaction", encoding="utf-8")

    store = SourceStore(tmp_path / "research")
    metadata = store.ingest_file(source, source_url="https://example.test/order")

    folder = tmp_path / "research" / "sources" / metadata.source_id
    assert (folder / "metadata.json").exists()
    assert (folder / "extracted.txt").exists()
    assert (folder / source.name).exists()

    loaded = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
    assert loaded["sha256"] == metadata.sha256
    assert loaded["source_url"] == "https://example.test/order"
