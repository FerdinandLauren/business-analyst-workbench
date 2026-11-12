"""Draft UAT scenarios derived from candidate requirements.

Steps depend on the requirement category, so an approval test does not read the
same as a reporting test.
"""
from __future__ import annotations

from src.i18n import t
from src.requirements import Requirement

FALLBACK_CATEGORY = "unclassified"


def _key(category: str, prefix: str) -> str:
    """Return a localized key that exists, falling back to the generic case."""
    candidate = f"uat.{prefix}_{category}"
    try:
        t(candidate, "en")
    except KeyError:
        return f"uat.{prefix}_{FALLBACK_CATEGORY}"
    return candidate


def make_uat_cases(reqs: list[Requirement], lang: str = "en") -> list[dict[str, str]]:
    """Create one draft UAT case per requirement."""
    cases = []
    for index, req in enumerate(reqs, 1):
        cases.append({
            "test_id": f"UAT-{index:03d}",
            "requirement_id": req.id,
            "scenario": t("uat.scenario", lang, statement=req.statement),
            "preconditions": t(_key(req.category, "precondition"), lang),
            "steps": t(_key(req.category, "steps"), lang),
            "expected_result": t(_key(req.category, "expected"), lang),
            "priority": req.priority,
            "status": t("uat.status_not_run", lang),
        })
    return cases
