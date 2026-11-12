"""Core business-analysis helpers. All outputs are drafts for human review."""
from __future__ import annotations
import re
from typing import Dict, List

KEYWORDS = {
    "approval": ["approve", "approval", "persetujuan", "menyetujui"],
    "tracking": ["track", "tracking", "status", "lacak", "pelacakan"],
    "validation": ["validate", "validation", "validasi", "mandatory", "wajib"],
    "notification": ["notify", "notification", "notifikasi", "email", "reminder"],
    "reporting": ["report", "dashboard", "laporan", "monitor"],
    "integration": ["integrate", "integration", "integrasi", "erp", "sap"],
}

def classify_requirement(text: str) -> str:
    """Classify a requirement using transparent keyword rules."""
    s = text.lower()
    if any(k in s for k in ["secure", "security", "performance", "availability",
                            "backup", "audit", "response time", "enkripsi"]):
        return "Non-functional"
    return "Functional"

def extract_candidate_requirements(problem: str) -> List[Dict[str, str]]:
    """Turn problem statements into candidate requirements; not NLP extraction."""
    sentences = [x.strip(" .;\n\t") for x in re.split(r"[\n.!?]+", problem) if x.strip()]
    candidates = []
    for i, sentence in enumerate(sentences, 1):
        lower = sentence.lower()
        matched = [name for name, words in KEYWORDS.items() if any(w in lower for w in words)]
        candidates.append({
            "id": f"REQ-{i:03d}",
            "type": classify_requirement(sentence),
            "statement": sentence[0].upper() + sentence[1:] if sentence else sentence,
            "theme": ", ".join(matched) if matched else "Needs analyst review",
            "status": "Draft - validate with stakeholder",
        })
    if not candidates:
        candidates.append({
            "id": "REQ-001", "type": "Functional",
            "statement": "The system shall support the business need described by the stakeholder.",
            "theme": "Needs analyst review",
            "status": "Draft - clarify before approval",
        })
    return candidates

def analyze_process(as_is: str, to_be: str) -> List[Dict[str, str]]:
    """Provide simple comparison prompts, not a definitive process assessment."""
    a = as_is.lower()
    b = to_be.lower()
    checks = [
        ("Visibility", ["status", "track", "tracking", "dashboard", "lacak"]),
        ("Validation", ["validate", "validation", "mandatory", "validasi", "wajib"]),
        ("Approval control", ["approval", "approve", "persetujuan"]),
        ("Notifications", ["notification", "notify", "notifikasi", "reminder"]),
        ("Auditability", ["log", "audit", "history", "riwayat"]),
    ]
    result = []
    for label, terms in checks:
        in_a = any(t in a for t in terms)
        in_b = any(t in b for t in terms)
        if not in_a and in_b:
            observation = f"Potential improvement: {label.lower()} is explicitly mentioned in the proposed process."
        elif in_a and in_b:
            observation = f"{label} appears in both descriptions; clarify what changes in the To-Be design."
        elif in_a and not in_b:
            observation = f"Potential regression or omission: {label.lower()} appears in As-Is but not To-Be."
        else:
            observation = f"{label} is not explicit in either description; confirm whether it is required."
        result.append({"area": label, "observation": observation})
    return result

def make_uat_cases(requirements: List[Dict[str, str]]) -> List[Dict[str, str]]:
    cases = []
    for i, req in enumerate(requirements, 1):
        cases.append({
            "test_id": f"UAT-{i:03d}",
            "requirement_id": req["id"],
            "scenario": f"Verify the system supports: {req['statement']}",
            "preconditions": "User has an authorized account and the relevant test data is available.",
            "steps": "1. Sign in. 2. Navigate to the relevant function. 3. Perform the business action.",
            "expected_result": "The system behaves according to the approved requirement and records the outcome.",
            "priority": "Medium",
            "status": "Not run",
        })
    return cases
