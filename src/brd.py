"""Build a BRD draft from the same input the other tabs use.

Every section is derived from the given problem statement, requirements, and
optional process analysis. Nothing is hardcoded to a procurement scenario.
"""
from __future__ import annotations

from src.i18n import t
from src.requirements import Requirement, display_fields
from src.text import CATEGORY_TERMS, PAIN_TERMS, matched_terms
from src.uat import make_uat_cases

PAIN_GROUPS = tuple(key for key in PAIN_TERMS if key != "none")


def _pains(text: str) -> list[str]:
    return [group for group in PAIN_GROUPS if matched_terms(text, PAIN_TERMS[group])]


def _categories(reqs: list[Requirement], problem: str) -> list[str]:
    found = {req.category for req in reqs if not req.category.startswith("nfr_")}
    found.update(
        key for key, terms in CATEGORY_TERMS.items() if matched_terms(problem, terms)
    )
    return [key for key in CATEGORY_TERMS if key in found]


def _body(text: str, lang: str) -> str:
    stripped = (text or "").strip()
    return stripped if stripped else t("brd.empty_section", lang)


def _table(header: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(header) + " |",
             "| " + " | ".join("---" for _ in header) + " |"]
    lines.extend("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def _assumptions(reqs: list[Requirement], problem: str, lang: str) -> list[str]:
    items = [t(f"brd.assumption_{key}", lang) for key in _categories(reqs, problem)]
    if any(req.category.startswith("nfr_") for req in reqs):
        items.append(t("brd.assumption_nfr", lang))
    if not items:
        items.append(t("brd.assumption_general", lang))
    return items


def _questions(reqs: list[Requirement], process: dict | None, lang: str) -> list[str]:
    items = [req.clarification for req in reqs if req.status == "needs_review" and req.clarification]
    if process:
        for row in process.get("rows", []):
            if row.get("severity") == "unspecified":
                area = t(f"proc.area_{row['area']}", lang)
                items.append(t("brd.question_area", lang, area=area))
    if not items:
        items.append(t("brd.question_general", lang))
    return items


def brd_markdown(
    project: str,
    problem: str,
    objective: str,
    stakeholders: str,
    scope_in: str,
    scope_out: str,
    reqs: list[Requirement],
    lang: str = "en",
    process: dict | None = None,
) -> str:
    """Return a Markdown BRD draft."""
    language = t("brd.lang_indonesian" if lang == "id" else "brd.lang_english", lang)
    cases = make_uat_cases(reqs, lang)
    pain_groups = _pains(problem or "")
    derived = [t(f"brd.objective_derived_{group}", lang) for group in pain_groups]

    parts = [
        f"# BRD — {project or t('ui.sidebar_project', lang)}",
        "",
        t("brd.status_line", lang),
        "",
        f"## 1. {t('brd.section_summary', lang)}",
        "",
        t("brd.summary_text", lang, project=project or "-", count=len(reqs),
          uat_count=len(cases), language=language),
        "",
        f"## 2. {t('brd.section_problem', lang)}",
        "",
        _body(problem, lang),
        "",
        f"## 3. {t('brd.section_objectives', lang)}",
        "",
        _body(objective, lang),
    ]
    if derived:
        parts.append("")
        parts.extend(f"- {item}" for item in derived)

    parts += [
        "",
        f"## 4. {t('brd.section_stakeholders', lang)}",
        "",
        _body(stakeholders, lang),
        "",
        f"## 5. {t('brd.section_scope_in', lang)}",
        "",
        _body(scope_in, lang),
        "",
        f"## 6. {t('brd.section_scope_out', lang)}",
        "",
        _body(scope_out, lang),
        "",
        f"## 7. {t('brd.section_requirements', lang)}",
        "",
    ]

    if reqs:
        rows = []
        for req in reqs:
            display = display_fields(req, lang)
            rows.append([
                req.id, display["type"], display["category"],
                req.statement, display["priority"], display["status"],
            ])
        parts.append(_table(
            [t("req.col_id", lang), t("req.col_type", lang), t("req.col_category", lang),
             t("req.col_statement", lang), t("req.col_priority", lang), t("req.col_status", lang)],
            rows,
        ))
    else:
        parts.append(t("brd.empty_requirements", lang))

    parts += [
        "",
        f"## 8. {t('brd.section_traceability', lang)}",
        "",
    ]
    if cases:
        trace_rows = [[req.id, case["test_id"]] for req, case in zip(reqs, cases)]
        parts.append(_table(
            [t("req.col_id", lang), t("uat.col_test_id", lang)],
            trace_rows,
        ))
    else:
        parts.append(t("brd.empty_section", lang))

    parts += ["", f"## 9. {t('brd.section_assumptions', lang)}", ""]
    parts.extend(f"- {item}" for item in _assumptions(reqs, problem or "", lang))

    parts += ["", f"## 10. {t('brd.section_questions', lang)}", ""]
    parts.extend(f"- {item}" for item in _questions(reqs, process, lang))

    parts += [
        "",
        f"## 11. {t('brd.section_acceptance', lang)}",
        "",
        t("brd.acceptance_text", lang, count=len(cases)),
        "",
        "---",
        "",
        t("brd.footer", lang),
        "",
    ]
    return "\n".join(parts)
