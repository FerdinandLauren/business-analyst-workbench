"""Compare As-Is and To-Be descriptions area by area.

Every row cites the term that triggered it, so an analyst can check the claim
instead of trusting a black box.
"""
from __future__ import annotations

from src.i18n import t
from src.text import has_term, matched_terms

AREA_KEYS = ("visibility", "validation", "approval", "notification", "auditability")

AREA_TERMS: dict[str, tuple[str, ...]] = {
    "visibility": (
        "status", "track", "tracking", "lacak", "pelacakan", "dashboard",
        "dasbor", "visibilitas",
    ),
    "validation": (
        "validate", "validation", "validasi", "verifikasi", "mandatory", "wajib",
        "kelengkapan",
    ),
    "approval": ("approval", "approve", "persetujuan", "menyetujui", "otorisasi"),
    "notification": (
        "notification", "notify", "notifikasi", "pemberitahuan", "reminder",
        "pengingat",
    ),
    "auditability": ("log", "audit", "jejak", "history", "riwayat", "rekam"),
}

MANUAL_MARKERS = (
    "manual", "email", "spreadsheet", "excel", "buku", "kertas", "telepon",
    "whatsapp", "input ulang", "retype",
)

HANDOFF_MARKERS = ("email", "whatsapp", "telepon", "chat", "rapat", "meeting")


def _first_term(text: str, terms: tuple[str, ...]) -> str:
    matches = matched_terms(text, terms)
    return matches[0] if matches else ""


def _severity(as_is_term: str, to_be_term: str) -> str:
    if as_is_term and to_be_term:
        return "clarify"
    if to_be_term:
        return "improve"
    if as_is_term:
        return "regression"
    return "unspecified"


def analyze_process(as_is: str, to_be: str, lang: str = "en") -> dict:
    """Return per-area severity, observation, evidence plus a summary."""
    rows = []
    for key in AREA_KEYS:
        terms = AREA_TERMS[key]
        as_is_term = _first_term(as_is, terms)
        to_be_term = _first_term(to_be, terms)
        severity = _severity(as_is_term, to_be_term)
        rows.append({
            "area": key,
            "severity": severity,
            "observation": t(
                f"proc.obs_{severity}",
                lang,
                area=t(f"proc.area_{key}", lang),
            ),
            "evidence": f"as-is: {as_is_term or '-'} | to-be: {to_be_term or '-'}",
        })

    return {
        "rows": rows,
        "summary": {
            "manual_steps": len(matched_terms(as_is, MANUAL_MARKERS)),
            "handoffs": len(matched_terms(as_is, HANDOFF_MARKERS)),
            "areas_to_improve": sum(1 for row in rows if row["severity"] == "improve"),
        },
    }
