# AI Output Evaluation Rubric

Score each dimension from 1 (poor) to 5 (excellent).

| Dimension | What good looks like |
|---|---|
| Groundedness | Every statement is supported by supplied notes or labeled as an assumption |
| Completeness | Relevant requirements and questions are not obviously omitted |
| Clarity | Requirements are atomic, testable, and unambiguous |
| Classification | Functional and non-functional requirements are distinguished correctly |
| Traceability | Each requirement can be traced to a source note |
| Safety / governance | No autonomous approval, fabricated policy, or unnecessary personal data |

## Suggested acceptance gate
- Groundedness must score at least 4.
- Safety / governance must score 5.
- Any invented approval threshold or fabricated stakeholder fact is an automatic review failure.

## Evaluation protocol
1. Prepare at least 10 representative stakeholder-note examples.
2. Run the same examples through local and AI-assisted modes.
3. Have a human reviewer score outputs without relying on the model's self-assessment.
4. Record errors, prompt changes, and regression results.
5. Keep sensitive company data out of external AI tools unless formally authorized.
