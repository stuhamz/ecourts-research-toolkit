from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class SourceMetadata:
    source_id: str
    title: str
    source_url: str | None
    source_type: str
    publisher_or_authority: str | None
    court_or_body: str | None
    case_number: str | None
    accessed_at: str
    sha256: str
    byte_size: int
    filename: str
    content_type: str
    notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ScreenResult:
    source_id: str
    score: int
    matched_groups: dict[str, list[str]] = field(default_factory=dict)
    suggested_attack_category: str = "unclear"
    snippets: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
