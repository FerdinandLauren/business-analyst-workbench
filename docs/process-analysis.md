# Process Analysis — As-Is vs To-Be

## As-Is
1. Requester prepares an email or spreadsheet.
2. Procurement checks the request manually.
3. Incomplete requests are returned through email.
4. Approval is coordinated through separate messages.
5. Requester contacts procurement to ask for status.
6. Records are distributed across inboxes and files.

## To-Be (proposed)
1. Requester signs in and creates a request using a standardized form.
2. The system validates mandatory fields.
3. The request is submitted and assigned a unique reference.
4. The workflow routes the request to an authorized approver using a business-approved matrix.
5. Approver makes the decision; the system records the outcome.
6. Requester and procurement view permitted status information.
7. Key actions are recorded in an audit history.
8. Managers review operational metrics.

## Gap observations
- Standardized intake addresses inconsistent input.
- Mandatory-field validation may reduce preventable rework.
- Central status tracking may reduce status enquiries.
- Centralized event history may improve auditability.
- Approval routing must be based on approved policy, not AI inference.

## Risks and controls
| Risk | Proposed control |
|---|---|
| Incorrect approval routing | Business owner signs off approval matrix; test boundary cases |
| Excessive access | Role-based access review and periodic recertification |
| Poor data quality | Field validation and reference-data governance |
| Notification leakage | Minimize personal/confidential data in notifications |
| AI-generated incorrect requirements | Human review, source traceability, evaluation cases |
