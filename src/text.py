"""Deterministic text helpers: sentence splitting and dictionary matching.

Matching is word-boundary based so that a keyword can never match inside an
unrelated word (``WhatsApp`` must not match ``sap``). Indonesian and English
inflections are tolerated through an optional suffix group.

Nothing here imports Streamlit or touches session state.
"""
from __future__ import annotations

import re

MIN_SENTENCE_CHARS = 10

GREETINGS = (
    "halo", "hai", "hi", "hello", "selamat pagi", "selamat siang",
    "selamat malam", "terima kasih", "thanks", "thank you",
)

# Machine keys are stable English identifiers; display labels live in i18n.
CATEGORY_TERMS: dict[str, tuple[str, ...]] = {
    "scheduling": (
        "schedule", "scheduling", "appointment", "booking", "reschedule",
        "queue", "slot", "rota",
        "jadwal", "penjadwalan", "antrean", "antrian", "kuota",
    ),
    "intake": (
        "form", "intake", "submit", "submission", "registration", "register",
        "request form",
        "formulir", "pendaftaran", "pengajuan", "permohonan", "isi data",
    ),
    "approval": (
        "approval", "approve", "approver", "sign-off", "authorization",
        "escalation",
        "persetujuan", "menyetujui", "otorisasi", "eskalasi", "tanda tangan",
    ),
    "payment": (
        "payment", "pay", "billing", "invoice", "receipt", "refund",
        "checkout", "cashier",
        "pembayaran", "bayar", "tagihan", "struk", "kuitansi", "kasir",
        "transaksi",
    ),
    "reporting": (
        "report", "reporting", "dashboard", "analytics", "statistics", "kpi",
        "recap",
        "laporan", "rekap", "dasbor", "analitik", "statistik",
    ),
    "tracking": (
        "track", "tracking", "progress", "visibility", "status",
        "lacak", "pelacakan", "progres", "riwayat status", "visibilitas",
    ),
    "notification": (
        "notification", "notify", "reminder", "alert", "email", "sms",
        "broadcast", "whatsapp",
        "notifikasi", "pemberitahuan", "pengingat", "pengumuman",
    ),
    "validation": (
        "validation", "validate", "verify", "verification", "mandatory",
        "completeness",
        "validasi", "verifikasi", "wajib", "kelengkapan", "cek data",
    ),
    "integration": (
        "integration", "integrate", "sync", "synchronization", "middleware",
        "erp", "sap",
        "integrasi", "terintegrasi", "sinkronisasi", "sambungan sistem", "api",
    ),
    "audit": (
        "audit", "audit trail", "trace", "retention", "compliance",
        "jejak audit", "rekam", "retensi", "kepatuhan", "regulasi",
    ),
    "search": (
        "search", "filter", "sort", "query", "find",
        "pencarian", "cari", "saring", "urutkan",
    ),
    "access": (
        "access", "role", "permission", "authentication",
        "akses", "hak akses", "peran", "otentikasi",
    ),
    "inventory": (
        "inventory", "stock", "warehouse", "asset", "goods",
        "inventaris", "stok", "gudang", "aset", "barang", "persediaan",
    ),
    "support": (
        "complaint", "ticket", "helpdesk", "support", "incident",
        "keluhan", "komplain", "tiket", "dukungan", "gangguan", "insiden",
    ),
}

# Five pain groups. Statement verbs compose with the category noun, which is why
# ten narrow pain keys were collapsed into these groups.
PAIN_TERMS: dict[str, tuple[str, ...]] = {
    "consolidation": (
        "bentrok", "benturan", "tumpang tindih", "dobel jadwal",
        "double booked", "conflict", "overlapping",
    ),
    "visibility": (
        "tidak tahu", "tidak ada yang tahu", "tidak jelas", "tidak terlacak",
        "tidak ada kabar", "unknown", "unclear", "no visibility",
        "hilang", "tercecer", "tidak tercatat", "lost", "missing record",
        "tidak ada bukti",
    ),
    "accuracy": (
        "salah", "keliru", "error", "kesalahan", "typo", "tidak akurat",
        "incorrect", "mistake",
        "dobel", "duplikat", "ganda", "duplikasi", "duplicate", "re-entry",
        "tidak konsisten", "beda-beda", "tidak seragam", "inconsistent",
        "tidak standar",
        "tidak lengkap", "kurang lengkap", "kosong", "belum diisi", "missing",
        "incomplete",
    ),
    "automation": (
        "manual", "manualnya", "tulis tangan", "spreadsheet", "excel", "buku",
        "kertas", "ulang", "retype", "input ulang",
        "lambat", "lama", "tertunda", "delay", "slow", "antre panjang",
        "susah", "sulit", "ribet", "merepotkan", "membingungkan", "confusing",
    ),
    "none": (),
}

NFR_TERMS: dict[str, tuple[str, ...]] = {
    "security": (
        "keamanan", "security", "enkripsi", "terenkripsi", "encryption", "encrypt",
        "kerahasiaan", "confidentiality",
    ),
    "performance": (
        "performa", "performance", "response time", "waktu respons",
        "throughput", "detik", "second",
    ),
    "availability": (
        "ketersediaan", "availability", "uptime", "downtime", "backup",
        "cadangan", "pemulihan", "recovery",
    ),
    "compliance": (
        "kepatuhan", "compliance", "regulasi", "regulation", "gdpr", "uu pdp",
    ),
    "usability": (
        "kemudahan", "usability", "user friendly", "ramah pengguna",
        "aksesibilitas", "accessibility",
    ),
    "maintainability": (
        "maintainability", "pemeliharaan", "maintenance", "modular", "scalable",
        "skalabilitas", "terdokumentasi", "documented",
    ),
}

# Optional inflections only; the core term must still sit between boundaries.
_SUFFIX = r"(?:nya|kan|lah|pun|s|es|ed|ing|d)?"
_PATTERNS: dict[str, re.Pattern[str]] = {}


def normalize(text: str) -> str:
    """Lowercase, collapse whitespace, strip."""
    return " ".join(text.lower().split())


def _pattern(term: str) -> re.Pattern[str]:
    cached = _PATTERNS.get(term)
    if cached is None:
        cached = re.compile(rf"(?<!\w){re.escape(term.lower())}{_SUFFIX}(?!\w)", re.IGNORECASE)
        _PATTERNS[term] = cached
    return cached


def split_sentences(text: str) -> list[str]:
    """Split on sentence punctuation and newlines, dropping empty fragments."""
    if not text:
        return []
    parts = re.split(r"[.!?;\n]+", text)
    return [part.strip() for part in parts if part.strip()]


def has_term(text: str, term: str) -> bool:
    """True when ``term`` appears as a whole word (case-insensitive)."""
    if not text or not term:
        return False
    return _pattern(term).search(text) is not None


def matched_terms(text: str, terms: tuple[str, ...] | list[str]) -> list[str]:
    """Return the terms from ``terms`` that occur in ``text``, in input order."""
    return [term for term in terms if has_term(text, term)]


def detect_categories(text: str) -> list[str]:
    """Return matched category keys in dictionary order (order breaks ties)."""
    return [key for key, terms in CATEGORY_TERMS.items() if matched_terms(text, terms)]


def detect_pain(text: str) -> str:
    """Return the first matched pain group, or ``"none"``."""
    for key, terms in PAIN_TERMS.items():
        if key == "none":
            continue
        if matched_terms(text, terms):
            return key
    return "none"


def detect_nfr(text: str) -> str | None:
    """Return the first matched non-functional key, or ``None``."""
    for key, terms in NFR_TERMS.items():
        if matched_terms(text, terms):
            return key
    return None
