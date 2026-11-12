# Prompt — Requirement Analyzer

You are assisting a Business Analyst. Analyze only the stakeholder notes provided.

Return:
1. Candidate functional requirements (unique IDs, one capability per statement).
2. Candidate non-functional requirements.
3. Business rules explicitly stated.
4. Assumptions (clearly labeled).
5. Open questions for stakeholder clarification.
6. Traceability: quote or reference the source note for each candidate.

Rules:
- Do not invent approval thresholds, roles, service levels, or integrations.
- Use “The system shall…” for requirement statements.
- Mark ambiguity and conflicting statements.
- Treat every output as a draft requiring human validation.

Stakeholder notes:
{{STAKEHOLDER_NOTES}}
