"""Turn a free-text problem statement into candidate requirements.

Rules are deterministic: sentence split -> category detection -> pain group ->
statement template. No model, no network, no Streamlit.
"""
from __future__ import annotations

from dataclasses import dataclass

from src.i18n import t
from src.text import (
    CATEGORY_TERMS,
    GREETINGS,
    MIN_SENTENCE_CHARS,
    detect_categories,
    detect_nfr,
    detect_pain,
    matched_terms,
    normalize,
    split_sentences,
)

# Categories that produce a non-functional requirement when nothing functional
# matched. ``audit`` keeps the legacy rule: "audit logs" is non-functional.
NONFUNCTIONAL_CATEGORIES = frozenset({"audit"})

HIGH_PRIORITY_CATEGORIES = frozenset({"approval", "payment", "audit", "integration"})
HIGH_PRIORITY_NFR = frozenset({"nfr_security", "nfr_compliance"})

CATEGORY_NOUN: dict[str, dict[str, str]] = {
    "en": {
        "scheduling": "appointment scheduling",
        "intake": "the request intake form",
        "approval": "the approval workflow",
        "payment": "payment and billing records",
        "reporting": "management reports",
        "tracking": "request status tracking",
        "notification": "notifications to users",
        "validation": "input validation rules",
        "integration": "integration with existing systems",
        "audit": "the audit trail",
        "search": "search and filtering",
        "access": "role-based access control",
        "inventory": "inventory records",
        "support": "complaint handling",
    },
    "id": {
        "scheduling": "penjadwalan",
        "intake": "formulir permohonan",
        "approval": "alur persetujuan",
        "payment": "pencatatan pembayaran",
        "reporting": "laporan manajemen",
        "tracking": "pelacakan status",
        "notification": "notifikasi ke pengguna",
        "validation": "aturan validasi input",
        "integration": "integrasi dengan sistem yang ada",
        "audit": "jejak audit",
        "search": "pencarian dan penyaringan",
        "access": "kontrol akses berbasis peran",
        "inventory": "pencatatan stok",
        "support": "penanganan keluhan",
    },
}

PAIN_VERB: dict[str, dict[str, str]] = {
    "en": {
        "automation": "automate",
        "accuracy": "standardise",
        "consolidation": "consolidate",
        "visibility": "make visible",
        "none": "provide",
    },
    "id": {
        "automation": "mengotomatiskan",
        "accuracy": "menstandarkan",
        "consolidation": "menyatukan",
        "visibility": "menampilkan",
        "none": "menyediakan",
    },
}

PAIN_OUTCOME: dict[str, dict[str, str]] = {
    "en": {
        "automation": "manual re-entry is removed",
        "accuracy": "the same rule applies to every case",
        "consolidation": "one source of truth is used",
        "visibility": "users no longer ask for status by message",
        "none": "the process is clear and measurable",
    },
    "id": {
        "automation": "pekerjaan manual berkurang",
        "accuracy": "aturan yang sama berlaku untuk semua kasus",
        "consolidation": "hanya ada satu sumber data",
        "visibility": "pengguna tidak perlu bertanya status lewat pesan",
        "none": "prosesnya jelas dan terukur",
    },
}

STATEMENT_PATTERN = {
    "en": "The system shall {verb} {noun} so that {outcome}.",
    "id": "Sistem harus {verb} {noun} agar {outcome}.",
}


@dataclass(frozen=True)
class Requirement:
    id: str
    type: str
    category: str
    statement: str
    priority: str
    status: str
    clarification: str
    source_sentence: str


def _fragment(sentence: str, limit: int = 8) -> str:
    words = sentence.strip().rstrip(".!?;").split()
    return " ".join(words[:limit])


def _is_skipped(sentence: str) -> bool:
    stripped = sentence.strip()
    if len(stripped) < MIN_SENTENCE_CHARS:
        return True
    lowered = stripped.lower()
    return any(lowered.startswith(greeting) for greeting in GREETINGS)


def _choose_category(categories: list[str], sentence: str) -> str:
    if len(categories) == 1:
        return categories[0]
    counts = {
        key: len(matched_terms(sentence, CATEGORY_TERMS[key]))
        for key in categories
    }
    best = max(counts.values())
    return next(key for key in categories if counts[key] == best)


def _statement(lang: str, category: str, pain: str) -> str:
    return STATEMENT_PATTERN[lang].format(
        verb=PAIN_VERB[lang][pain],
        noun=CATEGORY_NOUN[lang][category],
        outcome=PAIN_OUTCOME[lang][pain],
    )


def _priority(category: str, status: str) -> str:
    if status == "needs_review":
        return "Medium"
    if category in HIGH_PRIORITY_CATEGORIES or category in HIGH_PRIORITY_NFR:
        return "High"
    return "Medium"


def _build(sentence: str, req_id: str, lang: str) -> Requirement:
    categories = detect_categories(sentence)
    if categories:
        category = _choose_category(categories, sentence)
        req_type = "Non-functional" if set(categories) <= NONFUNCTIONAL_CATEGORIES else "Functional"
        pain = detect_pain(sentence)
        return Requirement(
            id=req_id,
            type=req_type,
            category=category,
            statement=_statement(lang, category, pain),
            priority=_priority(category, "draft"),
            status="draft",
            clarification="",
            source_sentence=sentence,
        )

    nfr = detect_nfr(sentence)
    if nfr:
        category = f"nfr_{nfr}"
        return Requirement(
            id=req_id,
            type="Non-functional",
            category=category,
            statement=t(f"req.{category}", lang),
            priority=_priority(category, "draft"),
            status="draft",
            clarification="",
            source_sentence=sentence,
        )

    fragment = _fragment(sentence)
    return Requirement(
        id=req_id,
        type="Functional",
        category="unclassified",
        statement=t("req.statement_unclassified", lang, fragment=fragment),
        priority="Medium",
        status="needs_review",
        clarification=t("req.clarification", lang, fragment=fragment),
        source_sentence=sentence,
    )


def extract_requirements(problem: str, lang: str = "en") -> list[Requirement]:
    """Convert a problem statement into candidate requirements."""
    if not problem or not problem.strip():
        return []

    seen: set[str] = set()
    requirements: list[Requirement] = []
    for sentence in split_sentences(problem):
        if _is_skipped(sentence):
            continue
        key = normalize(sentence)
        if key in seen:
            continue
        seen.add(key)
        requirements.append(_build(sentence, f"REQ-{len(requirements) + 1:03d}", lang))
    return requirements


def requirements_to_rows(reqs: list[Requirement], lang: str = "en") -> list[dict[str, str]]:
    """Localized rows for tables and CSV downloads."""
    type_label = {
        "Functional": "req.type_functional",
        "Non-functional": "req.type_nonfunctional",
    }
    status_label = {
        "draft": "req.status_draft",
        "needs_review": "req.status_needs_review",
    }
    priority_label = {
        "High": "req.priority_high",
        "Medium": "req.priority_medium",
        "Low": "req.priority_low",
    }
    headers = {
        "id": t("req.col_id", lang),
        "type": t("req.col_type", lang),
        "category": t("req.col_category", lang),
        "statement": t("req.col_statement", lang),
        "priority": t("req.col_priority", lang),
        "status": t("req.col_status", lang),
    }
    rows = []
    for req in reqs:
        rows.append({
            headers["id"]: req.id,
            headers["type"]: t(type_label[req.type], lang),
            headers["category"]: t(f"cat.{req.category}", lang),
            headers["statement"]: req.statement,
            headers["priority"]: t(priority_label[req.priority], lang),
            headers["status"]: t(status_label[req.status], lang),
        })
    return rows
