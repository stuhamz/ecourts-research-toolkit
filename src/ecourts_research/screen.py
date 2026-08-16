from __future__ import annotations

import re
from collections import defaultdict

from .models import ScreenResult


VOCABULARY: dict[str, tuple[int, tuple[str, ...]]] = {
    "social_engineering": (
        4,
        (
            "impersonat", "pretend", "posed as", "posing as", "phishing", "vishing",
            "smishing", "social engineering", "digital arrest", "fake police",
            "fake bank", "customer care", "tech support", "investment", "job offer",
            "task fraud", "matrimonial", "romance", "sextortion", "blackmail",
            "video call", "whatsapp call", "telegram group",
        ),
    ),
    "manipulation": (
        3,
        (
            "threat", "arrest", "urgent", "urgency", "fear", "secrecy", "do not tell",
            "do not disclose", "isolate", "authority", "trust", "verification",
            "profit", "guaranteed return", "emergency", "customs", "police officer",
        ),
    ),
    "digital_evidence": (
        2,
        (
            "call detail record", "cdr", "imei", "sim", "subscriber", "ip address",
            "login", "mobile phone", "seized phone", "forensic", "device",
            "whatsapp", "telegram", "email", "chat", "cctv", "bank account",
            "transaction", "upi", "wallet", "atm", "beneficiary account",
        ),
    ),
    "cybercrime": (
        2,
        (
            "cyber fraud", "cybercrime", "online fraud", "identity theft",
            "money laundering", "unauthorised access", "unauthorized access",
            "otp", "apk", "remote access", "malware", "computer resource",
        ),
    ),
    "legal": (
        1,
        (
            "information technology act", "section 66-d", "section 66d",
            "section 66-c", "section 66c", "bharatiya nyaya sanhita",
            "indian penal code", "bns", "ipc", "fir", "charge sheet", "chargesheet",
        ),
    ),
}

CATEGORY_HINTS: dict[str, tuple[str, ...]] = {
    "digital_arrest": ("digital arrest", "fake police", "police officer", "arrest"),
    "phishing": ("phishing", "fake link", "sms link"),
    "vishing": ("vishing", "phone call", "whatsapp call"),
    "customer_support_fraud": ("customer care", "tech support", "remote access"),
    "investment_fraud": ("investment", "guaranteed return", "profit"),
    "job_fraud": ("job offer", "work from home", "task fraud"),
    "romance_or_matrimonial_fraud": ("romance", "matrimonial"),
    "sextortion": ("sextortion", "sexual", "blackmail"),
    "impersonation": ("impersonat", "pretend", "posed as", "posing as"),
}


def screen_text(source_id: str, text: str, max_snippets: int = 6) -> ScreenResult:
    lowered = _normalize(text)
    matched: dict[str, list[str]] = defaultdict(list)
    score = 0

    for group, (weight, terms) in VOCABULARY.items():
        for term in terms:
            if term in lowered:
                matched[group].append(term)
                score += weight

    category = _suggest_category(lowered)
    matched_terms = sorted({t for values in matched.values() for t in values})
    snippets = _snippets(text, matched_terms, max_snippets)

    return ScreenResult(
        source_id=source_id,
        score=score,
        matched_groups=dict(matched),
        suggested_attack_category=category,
        snippets=snippets,
    )


def _suggest_category(lowered: str) -> str:
    ranked: list[tuple[int, str]] = []
    for category, terms in CATEGORY_HINTS.items():
        hits = sum(1 for term in terms if term in lowered)
        if hits:
            ranked.append((hits, category))
    if not ranked:
        return "unclear"
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return ranked[0][1]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _snippets(text: str, terms: list[str], limit: int) -> list[str]:
    if not terms:
        return []

    clean = re.sub(r"\s+", " ", text)
    lower = clean.lower()
    results: list[str] = []
    used: set[tuple[int, int]] = set()

    for term in terms:
        start = lower.find(term)
        if start < 0:
            continue
        left = max(0, start - 110)
        right = min(len(clean), start + len(term) + 160)
        key = (left, right)
        if key in used:
            continue
        used.add(key)
        snippet = clean[left:right].strip()
        results.append(snippet)
        if len(results) >= limit:
            break
    return results
