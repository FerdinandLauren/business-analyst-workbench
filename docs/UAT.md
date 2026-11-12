# User Acceptance Testing Plan

## Objective
Confirm that the proposed procurement workflow supports agreed business requirements and controls.

## Entry criteria
- Requirements and business rules reviewed by the business owner.
- Test environment and synthetic test data prepared.
- Test roles and access permissions configured.
- Expected results agreed before execution.

## Exit criteria
- All critical scenarios pass or have an approved disposition.
- Defects are recorded, prioritized, and assigned.
- Business owner accepts outstanding risks and signs off.

## UAT scenarios
| Test ID | Requirement | Scenario | Expected result | Priority |
|---|---|---|---|---|
| UAT-001 | FR-01 | Submit a complete request | Unique reference is created and status is Submitted | High |
| UAT-002 | FR-02 | Submit with a mandatory field missing | Submission is blocked and missing field is identified | High |
| UAT-003 | FR-03 | Submit a valid request | Request routes to approver from approved matrix | High |
| UAT-004 | FR-04 | Requester views own request | Current status is visible to requester | High |
| UAT-005 | FR-05 | Status changes | Relevant user receives an appropriate notification | Medium |
| UAT-006 | FR-06 | Approver takes action | Actor, timestamp, action, and request reference are logged | High |
| UAT-007 | FR-07 | Manager opens dashboard | Pending requests and aging are displayed to authorized manager | Medium |
| UAT-008 | NFR-01 | Unauthorized user attempts access | Access is denied and event is handled according to policy | High |
| UAT-009 | NFR-02 | Audit event is reviewed | Required audit fields are present and attributable | High |
| UAT-010 | FR-03 | Approver is unavailable | Approved delegation/escalation rule is followed | High |

## Execution record
Record tester, date, environment, actual result, pass/fail, defect ID, and evidence for each scenario.
