# Production policy coverage

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](spec.md)

This index maps every requirement and scenario in the [ratified qualification policy](../../openspec/changes/qualify-private-connectivity-production/specs/private-connectivity-production-qualification/spec.md). It describes planned acceptance coverage, not executed tests or passed gates.

T005 reviews and freezes this complete mapping for owner acceptance with the [task evidence contract](contracts/task-evidence.md#t005-review-freeze). All 18 requirements and 39 scenarios remain represented; drafting or publishing successor proposals does not close a production gate.

US identifiers refer to user stories in [spec.md](spec.md); FR identifiers refer to its functional requirements. L/H/D cases are in the [local](local-headscale.md), [Hosted Headscale](standalone-hosted-headscale.md) and [hosted domain](hosted-domainxfactories.md) documents. C identifiers are [commissioning decisions](commissioning.md); Q identifiers are [rollout gates](rollout-gates.md).

## Requirement coverage

| Governing requirement | Feature requirements | Planned acceptance |
| --- | --- | --- |
| Production decisions are separate from lab acceptance | FR-001, FR-026, FR-030 | US1 / Q0–Q5 |
| Owner commissioning precedes realization | FR-002, FR-003, FR-028, FR-029 | US1 / owner scopes / C-01–C-02 |
| Deployment follows the managed-subject boundary | FR-004 | L-05 / C-03 / Q1 and Q3 |
| Release candidates identify supported immutable artifacts | FR-005, FR-006 | C-05 / Q1–Q2 |
| Local Headscale supports customer operation | FR-007, FR-008, FR-012, FR-027 | L-01, L-02, L-06 |
| Local packages qualify HTTPS and state lifecycle | FR-008, FR-009, FR-024 | L-03, L-04 |
| Hosted Headscale uses qualified production integrations | FR-010, FR-012 | H-01, H-03 |
| Hosted network and factory lifetimes remain independent | FR-011, FR-013 | H-02, H-04, H-05 |
| Hosted domains qualify their actual profile | FR-012, FR-013, FR-014 | D-01, D-03, D-04, D-05 |
| Production profiles are protected and validated | FR-015, FR-022 | D-02, D-06 |
| Staging entry fixes the qualification scope | FR-002, FR-003, FR-016, FR-018 | C-01–C-08 / Q1 |
| Staging exit proves the offering paths and operations | FR-017, FR-027 | US5 / L-01–L-06 / H-01–H-06 / D-01–D-06 / Q2 |
| Production operating objectives are approved and measured | FR-018, FR-020 | C-06 / H-06 / Q2 and Q4 |
| Production canary entry requires bounded release authority | FR-004, FR-019 | L-05 / C-09 / Q3 |
| Canary exit requires production evidence and owner acceptance | FR-020 | C-10 / US6–US7 / Q4 |
| Expansion is a separate per-wave decision | FR-021, FR-022 | D-06 / C-11–C-12 / Q5 |
| A failed control halts and contains the affected rollout | FR-023, FR-024 | L-03 / H-06 / C-13 |
| Acceptance evidence is immutable and scoped | FR-025, FR-026 | C-08 / every gate |

## Scenario coverage

| Governing scenario | Feature requirements | Planned acceptance |
| --- | --- | --- |
| A source merge is offered as production permission | FR-001, FR-030 | US1 / Q3 |
| A policy is ratified | FR-001, FR-026 | US1 / Q0 |
| A proposed runtime surface lacks owner authority | FR-002, FR-028, FR-029 | US1 / C-01 |
| Staging is a registered managed target | FR-004 | C-03 / Q1 |
| A managed production canary lacks an accepted request | FR-004, FR-019 | L-05 / Q3 |
| A managed production canary lacks a required execution grant | FR-004, FR-019 | L-05 / Q3 |
| A managed canary uses governed pull reconciliation | FR-004 | L-05 / Q1 and Q3 |
| A consumer uses the pilot schema directly | FR-005, FR-030 | C-05 / Q1 |
| Running configuration differs from the candidate | FR-006, FR-022 | US5 / Q2–Q5 |
| A customer selects its own Headscale | FR-007, FR-008 | L-01, L-02 |
| A local factory selects Hosted Headscale | FR-007, FR-012, FR-013, FR-027 | L-06 |
| A certificate renews or an endpoint changes | FR-008, FR-009, FR-024 | L-03 |
| An instance restores older state | FR-009 | L-04 |
| The only adapter is the Eagle lab adapter | FR-010, FR-030 | H-01 |
| A customer or environment crosses a boundary | FR-010, FR-012, FR-017 | H-03 |
| A factory subscription ends | FR-011, FR-013 | H-04 |
| A stale operation retries after authority changes | FR-012, FR-013 | H-05 |
| A synthetic profile is proposed for customer release | FR-014, FR-030 | D-01 |
| Network access succeeds without application permission | FR-012, FR-014 | D-04 |
| Hosted onboarding fails after partial provisioning | FR-013, FR-014 | D-03 |
| A new profile escapes required validation | FR-015 | D-02 |
| Catalog evidence has the wrong scope | FR-015, FR-022, FR-025 | D-02, D-06 |
| A required decision is absent | FR-002, FR-003, FR-016, FR-018 | C-01–C-08 / Q1 |
| Denial is observed against a broken service | FR-017 | H-03 / US5 |
| Staging lacks a required path or drill | FR-017, FR-027 | US5 / Q2 / all tracks |
| A recovery exceeds the approved limit | FR-009, FR-018, FR-020 | L-04, H-06 / Q2 and Q4 |
| Monitoring misses part of the observation window | FR-018, FR-020 | H-06 / Q4 |
| A customer-operated local canary is an unmanaged target | FR-004, FR-019 | L-05 / Q3 |
| An unmanaged local canary lacks customer authority | FR-004, FR-019 | L-05 / Q3 |
| A canary exceeds its approved scope | FR-019, FR-021 | C-09 / Q3 |
| Staging approval is reused as canary permission | FR-001, FR-019 | US7 / Q3 |
| An incident remains unresolved | FR-020, FR-024 | US6–US7 / C-10 / Q4 |
| A fault drill lacks customer scope | FR-020, FR-023 | US6 / C-09 / Q3–Q4 |
| One domain's canary succeeds | FR-014, FR-021, FR-022 | D-06 / Q5 |
| A candidate changes after acceptance | FR-006, FR-022 | D-06 / Q2–Q5 |
| Rollback encounters an unauthorized prior binding | FR-009, FR-024 | L-03 |
| One tenant fails qualification | FR-023, FR-024 | H-06 / US6 / C-13 |
| A local fixture is offered as deployed evidence | FR-025, FR-030 | US5 / Q2 and Q4 |
| Gate evidence changes scope | FR-025, FR-026 | C-08 / Q0–Q5 |

## Disposition

All 18 requirements and 39 scenarios have planned coverage. No scenario is waived, relabeled as a lab pass or claimed executed. The [implementation plan](plan.md), [validation matrix](validation-matrix.md) and [task coverage](tasks.md#task-coverage) preserve this mapping through owner workstreams and Q0–Q5. Tasks require exact accepted owner file/command scope and decision dependencies before their consumers execute. Runtime realization and live acceptance remain blocked on those decisions.
