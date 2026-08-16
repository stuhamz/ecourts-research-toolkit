from __future__ import annotations

from io import BytesIO
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader


TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".xml", ".log"}
HTML_EXTENSIONS = {".html", ".htm"}


def extract_text(data: bytes, filename: str, content_type: str = "") -> str:
    suffix = Path(filename).suffix.lower()
    ctype = (content_type or "").lower()

    if suffix == ".pdf" or "application/pdf" in ctype:
        return _extract_pdf(data)

    if suffix in HTML_EXTENSIONS or "text/html" in ctype:
        return _extract_html(data)

    if suffix in TEXT_EXTENSIONS or ctype.startswith("text/"):
        return data.decode("utf-8", errors="replace")

    # Last-resort decoding is intentionally conservative. Binary data will
    # usually produce little useful screening text but remains preserved raw.
    return data.decode("utf-8", errors="replace")


def _extract_html(data: bytes) -> str:
    soup = BeautifulSoup(data, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    lines = [line.strip() for line in soup.get_text("\n").splitlines()]
    return "\n".join(line for line in lines if line)


def _extract_pdf(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n\n".join(pages)
