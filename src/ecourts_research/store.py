from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from urllib.parse import urlparse

import requests

from .extract import extract_text
from .models import SourceMetadata
from .provenance import sha256_bytes, utc_now_iso


DEFAULT_USER_AGENT = (
    "ecourts-research-toolkit/1.0 "
    "(public-record research; contact repository maintainer)"
)


class SourceStore:
    def __init__(self, root: str | Path = "data"):
        self.root = Path(root)
        self.sources_dir = self.root / "sources"
        self.sources_dir.mkdir(parents=True, exist_ok=True)

    def ingest_file(
        self,
        path: str | Path,
        *,
        source_url: str | None = None,
        title: str | None = None,
        source_type: str = "court_record",
        publisher_or_authority: str | None = None,
        court_or_body: str | None = None,
        case_number: str | None = None,
        notes: str | None = None,
    ) -> SourceMetadata:
        src = Path(path)
        data = src.read_bytes()
        content_type = mimetypes.guess_type(src.name)[0] or "application/octet-stream"
        return self._persist(
            data=data,
            filename=src.name,
            content_type=content_type,
            source_url=source_url,
            title=title or src.stem,
            source_type=source_type,
            publisher_or_authority=publisher_or_authority,
            court_or_body=court_or_body,
            case_number=case_number,
            notes=notes,
        )

    def ingest_url(
        self,
        url: str,
        *,
        title: str | None = None,
        source_type: str = "court_record",
        publisher_or_authority: str | None = None,
        court_or_body: str | None = None,
        case_number: str | None = None,
        notes: str | None = None,
        timeout: int = 30,
        max_bytes: int = 25 * 1024 * 1024,
    ) -> SourceMetadata:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Only http:// and https:// URLs are supported.")

        with requests.get(
            url,
            timeout=timeout,
            stream=True,
            headers={"User-Agent": DEFAULT_USER_AGENT},
        ) as response:
            response.raise_for_status()
            chunks: list[bytes] = []
            size = 0
            for chunk in response.iter_content(chunk_size=65536):
                if not chunk:
                    continue
                size += len(chunk)
                if size > max_bytes:
                    raise ValueError(
                        f"Source exceeds the {max_bytes} byte safety limit."
                    )
                chunks.append(chunk)

            data = b"".join(chunks)
            content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
            filename = _filename_from_response(url, response.headers.get("Content-Disposition"))
            if not Path(filename).suffix:
                guessed = mimetypes.guess_extension(content_type) or ".html"
                filename = filename + guessed

        return self._persist(
            data=data,
            filename=filename,
            content_type=content_type or "application/octet-stream",
            source_url=url,
            title=title or Path(filename).stem,
            source_type=source_type,
            publisher_or_authority=publisher_or_authority,
            court_or_body=court_or_body,
            case_number=case_number,
            notes=notes,
        )

    def _persist(
        self,
        *,
        data: bytes,
        filename: str,
        content_type: str,
        source_url: str | None,
        title: str,
        source_type: str,
        publisher_or_authority: str | None,
        court_or_body: str | None,
        case_number: str | None,
        notes: str | None,
    ) -> SourceMetadata:
        digest = sha256_bytes(data)
        source_id = f"SRC-{digest[:12].upper()}"
        folder = self.sources_dir / source_id
        folder.mkdir(parents=True, exist_ok=True)

        safe_name = Path(filename).name
        raw_path = folder / safe_name
        raw_path.write_bytes(data)

        text = extract_text(data, safe_name, content_type)
        (folder / "extracted.txt").write_text(text, encoding="utf-8", errors="replace")

        metadata = SourceMetadata(
            source_id=source_id,
            title=title,
            source_url=source_url,
            source_type=source_type,
            publisher_or_authority=publisher_or_authority,
            court_or_body=court_or_body,
            case_number=case_number,
            accessed_at=utc_now_iso(),
            sha256=digest,
            byte_size=len(data),
            filename=safe_name,
            content_type=content_type,
            notes=notes,
        )
        (folder / "metadata.json").write_text(
            json.dumps(metadata.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return metadata

    def list_sources(self) -> list[SourceMetadata]:
        sources = []
        for metadata_path in sorted(self.sources_dir.glob("SRC-*/metadata.json")):
            data = json.loads(metadata_path.read_text(encoding="utf-8"))
            sources.append(SourceMetadata(**data))
        return sources

    def get_metadata(self, source_id: str) -> SourceMetadata:
        path = self.sources_dir / source_id / "metadata.json"
        if not path.exists():
            raise KeyError(f"Unknown source_id: {source_id}")
        return SourceMetadata(**json.loads(path.read_text(encoding="utf-8")))

    def get_text(self, source_id: str) -> str:
        path = self.sources_dir / source_id / "extracted.txt"
        if not path.exists():
            raise KeyError(f"Unknown source_id: {source_id}")
        return path.read_text(encoding="utf-8", errors="replace")


def _filename_from_response(url: str, content_disposition: str | None) -> str:
    if content_disposition and "filename=" in content_disposition:
        value = content_disposition.split("filename=", 1)[1].strip().strip('"\'')
        if value:
            return Path(value).name

    name = Path(urlparse(url).path).name
    return name or "source"
