"""Optional user-supplied OpenAI key.

The engine works without this module. When a visitor brings their own key, the
UI can ask for an AI-assisted draft; every failure silently falls back to the
local rule-based output. The key is never logged or written to disk.
"""
from __future__ import annotations

import os
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "ai" / "prompts"

SYSTEM_PROMPT = (
    "You are a careful business-analysis assistant. Produce concise structured "
    "drafts. Do not invent stakeholder facts. Mark assumptions and open "
    "questions clearly. Human review is mandatory."
)


def load_prompt(name: str) -> str:
    """Return the prompt template from ``ai/prompts`` or an empty string."""
    path = PROMPTS_DIR / f"{name}.md"
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def resolve_api_key(session_key: str | None = None) -> str:
    """Priority: value typed in the UI -> environment variable -> empty."""
    candidate = (session_key or "").strip()
    if candidate:
        return candidate
    return os.getenv("OPENAI_API_KEY", "").strip()


def generate_with_key(prompt: str, api_key: str, model: str = "gpt-4.1-mini") -> str | None:
    """Return a draft or ``None``. Never raises, never logs the key."""
    key = (api_key or "").strip()
    if not key or not (prompt or "").strip():
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model=(model or "gpt-4.1-mini").strip(),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        return content.strip() if content and content.strip() else None
    except Exception:
        return None
