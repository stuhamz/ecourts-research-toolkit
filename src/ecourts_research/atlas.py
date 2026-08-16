from __future__ import annotations

import csv
from pathlib import Path

from .screen import screen_text
from .store import SourceStore


ATLAS_SCREENING_FIELDS = [
    "candidate_id",
    "discovered_date",
    "discovery_method",
    "search_query_or_source",
    "source_title",
    "source_url",
    "incident_year",
    "state",
    "preliminary_attack_category",
    "decision",
    "exclusion_reason",
    "duplicate_of_case_id",
    "linked_case_id",
    "reviewer",
    "notes",
]

ATLAS_SOURCE_FIELDS = [
    "source_id",
    "case_id",
    "source_tier",
    "source_stage",
    "source_type",
    "title",
    "publisher_or_authority",
    "court_or_body",
    "case_number",
    "publication_date",
    "accessed_date",
    "url",
    "archive_url",
    "claim_scope",
    "notes",
]


def export_atlas_candidates(
    store: SourceStore,
    output: str | Path,
    *,
    reviewer: str = "Hamzah",
) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for idx, metadata in enumerate(store.list_sources(), start=1):
        result = screen_text(metadata.source_id, store.get_text(metadata.source_id))
        matches = "; ".join(
            f"{group}: {', '.join(terms)}"
            for group, terms in sorted(result.matched_groups.items())
        )
        rows.append(
            {
                "candidate_id": f"CAND-TO-REVIEW-{idx:04d}",
                "discovered_date": metadata.accessed_at[:10],
                "discovery_method": "ecourts-research-toolkit",
                "search_query_or_source": metadata.source_id,
                "source_title": metadata.title,
                "source_url": metadata.source_url or "",
                "incident_year": "",
                "state": "",
                "preliminary_attack_category": result.suggested_attack_category,
                "decision": "pending",
                "exclusion_reason": "",
                "duplicate_of_case_id": "",
                "linked_case_id": "",
                "reviewer": reviewer,
                "notes": f"screen_score={result.score}; {matches}".strip("; "),
            }
        )

    _write_csv(output, ATLAS_SCREENING_FIELDS, rows)
    return output


def export_atlas_sources(store: SourceStore, output: str | Path) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for metadata in store.list_sources():
        rows.append(
            {
                "source_id": metadata.source_id,
                "case_id": "",
                "source_tier": "",
                "source_stage": "",
                "source_type": metadata.source_type,
                "title": metadata.title,
                "publisher_or_authority": metadata.publisher_or_authority or "",
                "court_or_body": metadata.court_or_body or "",
                "case_number": metadata.case_number or "",
                "publication_date": "",
                "accessed_date": metadata.accessed_at[:10],
                "url": metadata.source_url or "",
                "archive_url": "",
                "claim_scope": "",
                "notes": (
                    f"sha256={metadata.sha256}; bytes={metadata.byte_size}"
                    + (f"; {metadata.notes}" if metadata.notes else "")
                ),
            }
        )

    _write_csv(output, ATLAS_SOURCE_FIELDS, rows)
    return output


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
