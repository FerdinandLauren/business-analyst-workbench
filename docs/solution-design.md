# Solution Design (Conceptual)

## Components
- Web interface for request creation and status views
- Application service for validation and workflow state
- Identity and role management
- Notification service
- Audit-event store
- Reporting layer
- Optional ERP integration through controlled APIs

## Design principles
1. Human approvers retain decision authority.
2. AI may assist with classification or drafting, but may not approve spend.
3. Use least-privilege access.
4. Maintain traceable state changes.
5. Validate reference data at system boundaries.
6. Design for recoverable errors and duplicate-submission prevention.

## Integration questions
- Which ERP is the source of truth?
- Are APIs available for cost centers, suppliers, and purchase orders?
- What authentication method is supported?
- What data can be transferred to third-party AI services?
- What are the retention and audit requirements?

See `../diagrams/system-architecture.mmd`.
