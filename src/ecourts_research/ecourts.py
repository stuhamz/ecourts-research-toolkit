from __future__ import annotations

import re
import webbrowser


PORTALS = {
    "district": "https://services.ecourts.gov.in/ecourtindia_v6/",
    "case-status": "https://services.ecourts.gov.in/ecourtindia_v6/",
    "cause-list": (
        "https://services.ecourts.gov.in/ecourtindia_v6/"
        "?p=cause_list%2Findex"
    ),
    "high-court": "https://hcservices.ecourts.gov.in/hcservices/",
}

CNR_PATTERN = re.compile(r"^[A-Z0-9]{16}$")


def normalize_cnr(value: str) -> str:
    return re.sub(r"[-\s]", "", value.upper())


def is_valid_cnr(value: str) -> bool:
    return bool(CNR_PATTERN.fullmatch(normalize_cnr(value)))


def portal_url(name: str) -> str:
    if name not in PORTALS:
        raise KeyError(f"Unknown portal {name!r}. Choose from: {', '.join(PORTALS)}")
    return PORTALS[name]


def open_portal(name: str) -> str:
    url = portal_url(name)
    webbrowser.open(url)
    return url
