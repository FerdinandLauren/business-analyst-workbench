# Functional Requirements Catalogue

| ID | Requirement | Actor | Trigger | Acceptance criteria (draft) |
|---|---|---|---|---|
| FR-01 | Create purchase request | Requester | User selects New Request | A draft request is saved with a unique ID and creator identity. |
| FR-02 | Validate mandatory fields | System | User submits request | Missing required fields are identified and submission is blocked until corrected. |
| FR-03 | Route approval | System | Valid request is submitted | Request is assigned to an approver determined by the approved matrix. |
| FR-04 | View status | Requester / Procurement | User opens request details | Current status and permitted history are displayed. |
| FR-05 | Notify users | System | Status changes or action is needed | Relevant users receive a notification containing a request reference, not unnecessary sensitive data. |
| FR-06 | Record audit events | System | Key action occurs | Actor, timestamp, event type, and request ID are recorded. |
| FR-07 | View dashboard | Procurement Manager | User opens dashboard | Authorized manager can filter pending requests by status, department, and age. |

These are candidate requirements. Confirm edge cases and detailed rules with stakeholders.
