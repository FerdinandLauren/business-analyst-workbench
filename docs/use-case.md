# Use Case — Submit Purchase Request

**Primary actor:** Requester  
**Supporting actors:** Procurement Officer, Approver  
**Preconditions:** User is authenticated; request categories and required fields are configured.

## Main flow
1. Requester opens the purchase-request form.
2. Requester enters item, business justification, department, cost center, and estimated amount.
3. System validates required fields and formats.
4. Requester submits the request.
5. System assigns a unique request reference and records the submission event.
6. System routes the request to the authorized approver based on the approved matrix.
7. Requester sees the submitted status.

## Alternative flows
- **A1 — Missing field:** System identifies missing data and asks requester to correct it.
- **A2 — Invalid reference data:** System explains which value is invalid and how to correct it.
- **A3 — Approver unavailable:** Workflow follows a business-approved delegation or escalation rule.
- **A4 — Technical failure:** Submission is not falsely reported as successful; user receives a safe retry message.

## Postconditions
- A successfully submitted request has a unique reference and recorded event.
- No approval decision is made autonomously by the AI assistant.
