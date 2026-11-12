"""Draft document generation with optional AI and safe local fallback."""
from __future__ import annotations

import os
from typing import Any

from src.brd import brd_markdown as _brd_markdown
from src.requirements import Requirement


def generate_with_ai(prompt: str) -> str | None:
    """Return AI response when configured; otherwise None. Never logs secrets."""
    key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    if not key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": (
                    "You are a careful junior business-analysis assistant. "
                    "Produce concise structured drafts. Do not invent stakeholder facts. "
                    "Mark assumptions and questions clearly. Human review is mandatory."
                )},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or None
    except Exception:
        return None


def _as_requirement(item: Any) -> Requirement:
    """Accept both Requirement objects and the legacy display dictionaries."""
    if isinstance(item, Requirement):
        return item
    status = "needs_review" if "review" in str(item.get("theme", "")).lower() else "draft"
    return Requirement(
        id=item["id"],
        type=item.get("type", "Functional"),
        category=item.get("category", "unclassified"),
        statement=item["statement"],
        priority=item.get("priority", "Medium"),
        status=status,
        clarification="",
        source_sentence=item.get("source_sentence", item["statement"]),
    )


def brd_markdown(project_name: str, problem: str, objective: str,
                 stakeholders: str, scope_in: str, scope_out: str,
                 requirements: list, lang: str = "en", process: dict | None = None) -> str:
    """Delegate to the generic BRD builder, keeping the old call signature."""
    reqs = [_as_requirement(item) for item in requirements]
    return _brd_markdown(
        project_name, problem, objective, stakeholders, scope_in, scope_out,
        reqs, lang=lang, process=process,
    )


def ai_or_fallback(prompt: str, fallback: str) -> tuple[str, str]:
    result = generate_with_ai(prompt)
    return (result, "AI-assisted draft — human review required") if result else (
        fallback, "Local rule-based draft — human review required"
    )
