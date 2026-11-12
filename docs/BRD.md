# Business Requirements Document

**Project:** Procurement Process Improvement  
**Version:** 0.1  
**Status:** Draft — fictional portfolio case

## 1. Executive summary
The project proposes a centralized workflow for internal purchase requests to reduce incomplete submissions and improve approval visibility and traceability.

## 2. Business problem
Requests currently arrive through email and spreadsheets. Procurement checks them manually, approval conversations are distributed, and requesters have limited visibility into status.

## 3. Objectives
- Standardize purchase-request intake.
- Validate required information before submission.
- Make approval status visible to authorized users.
- Maintain an audit history of key status changes.
- Provide a dashboard for operational monitoring.

## 4. Scope
**In scope:** request form, mandatory-field validation, status tracking, approval routing, notifications, audit history, dashboard.

**Out of scope:** payment execution, supplier negotiations, autonomous approval decisions, ERP replacement.

## 5. Business rules (draft)
- Only authenticated users may create or view requests.
- Approval authority must follow a business-approved matrix.
- A requester must not approve their own request unless policy explicitly permits it.
- Changes to request status must be attributable to an authenticated actor.
- Missing or invalid mandatory fields must be returned for correction before submission.

## 6. Candidate functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | The system shall allow an authenticated requester to create a purchase request. | Must |
| FR-02 | The system shall validate mandatory fields before accepting submission. | Must |
| FR-03 | The system shall route submitted requests to an authorized approver based on an approved matrix. | Must |
| FR-04 | The system shall display the current status to authorized users. | Must |
| FR-05 | The system shall notify relevant users when an action is required or a status changes. | Should |
| FR-06 | The system shall retain a history of key request and approval events. | Must |
| FR-07 | The system shall provide a dashboard of pending requests and aging. | Should |

## 7. Candidate non-functional requirements
| ID | Requirement | Validation approach |
|---|---|---|
| NFR-01 | The system shall enforce role-based access to requests and approval actions. | Access-control test |
| NFR-02 | The system shall record actor, timestamp, action, and affected request for key events. | Audit-log inspection |
| NFR-03 | The system shall protect data in transit using approved secure transport. | Security review |
| NFR-04 | The system shall provide recoverable backups according to an agreed recovery policy. | Recovery test |

## 8. Assumptions
- The company has an identity-management mechanism.
- An authorized business owner will provide the approval matrix.
- ERP integration is not included in the first prototype.
- Data retention requirements will be confirmed by IT and Audit.

## 9. Open questions
1. What request categories and mandatory fields apply?
2. What approval thresholds and delegation rules apply?
3. Can a request be edited after submission?
4. What happens when an approver is unavailable?
5. Which ERP/finance master data must be referenced?
6. What are the data retention and recovery requirements?

## 10. Acceptance
The business owner reviews each requirement, confirms priority and business rules, and approves UAT scenarios before execution.
