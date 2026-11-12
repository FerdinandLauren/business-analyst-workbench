"""Draft document generation with optional AI and safe local fallback."""
from __future__ import annotations
import os
from typing import Dict, List

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

def brd_markdown(project_name: str, problem: str, objective: str,
                 stakeholders: str, scope_in: str, scope_out: str,
                 requirements: List[Dict[str, str]]) -> str:
    req_lines = "\n".join(
        f"| {r['id']} | {r['type']} | {r['statement']} | Draft |" for r in requirements
    )
    return f"""# Business Requirements Document (Draft)

**Project:** {project_name}  
**Version:** 0.1  
**Status:** Draft for stakeholder validation

## 1. Executive summary
{objective}

## 2. Business problem
{problem}

## 3. Business objectives
- Reduce manual handoffs and improve process visibility.
- Standardize required information and approval records.
- Provide a traceable view of request status.

## 4. Stakeholders
{stakeholders}

## 5. Scope
### In scope
{scope_in}

### Out of scope
{scope_out}

## 6. Candidate requirements
| ID | Type | Requirement | Status |
|---|---|---|---|
{req_lines}

## 7. Assumptions and constraints
- The scenario is fictional and requires stakeholder validation.
- Approval rules, thresholds, and role permissions must be confirmed by the business owner.
- Any integration with an ERP is subject to API, security, and data-governance review.

## 8. Open questions
1. What approval matrix and monetary thresholds apply?
2. Which fields are mandatory for each request category?
3. What service-level targets should be measured?
4. Which system is the source of truth for suppliers and cost centers?

## 9. Acceptance approach
Business representatives review each requirement, agree acceptance criteria, and execute UAT in a controlled test environment.

---
*Generated as a draft by AI Business Analyst Workbench. Review and approve before use.*
"""

def ai_or_fallback(prompt: str, fallback: str) -> tuple[str, str]:
    result = generate_with_ai(prompt)
    return (result, "AI-assisted draft — human review required") if result else (
        fallback, "Local rule-based draft — human review required"
    )
