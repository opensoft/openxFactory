---
code_surface: openxFactory, openXsoft-Hosted-Services
target_release: implemented — planned owner main-line realization; no implementation or release completion claimed
sequenced_after: [qualify-private-connectivity-production, establish-openxsoft-hosted-connectivity]
---

# Proposal: Commission Hosted Headscale and hosted-factory service production

Status: ratified
Ratified: 2026-11-14 by Brett Heap. [Ratification record](review/ratification.md)
Kind: proposal
Proposed: 2026-11-14

## Why

The hosted repository currently provides pilot service cores and synthetic effects. Offering Hosted Headscale separately and hosting real DomainxFactories requires a deployable authenticated API, actual provider/identity/custody integration and durable lifecycle/catalog behavior.

## What Changes

- Commission Brett Heap as hosted-product/source/release maintainer for the exact service/API/provider/identity/custody/catalog/onboarding files in the design, subject to his acceptance.
- Propose the existing Opensoft Azure AKS estate as the intended provider platform: QA in West US, production in Central US. Source approval does not deploy to either cluster or authorize new resource spend.
- Implement the real authenticated HTTP service, selected identity/entitlement/custody adapters and managed-subject request/readback integration. Add the exact API/test and pinned dependency/container entry points to T030/T033 for owner review.
- Provide standalone network service without a factory; dedicated boundary/state/endpoint/key/policy per customer/environment; original-subject durable retry, sharing, detachment and separately authorized network termination.
- Integrate the selected real domain/profile through trusted exact identity and independent application authorization; keep network availability and catalog/commercial eligibility distinct and fail closed on missing configuration.
- Use the exact per-task scope and source/custody obligations in [design](design.md). Implementation stays in the single [043 task list](../../../specs/043-private-connectivity-production/tasks.md), after dependencies and consumed choices pass.

## Capabilities

### New Capabilities

- hosted-headscale-production: the owner-specific production source, release and qualification boundary described in this packet.

### Modified Capabilities

None. The existing neutral binding, managed-subject, release, source-evidence and Q0–Q5 requirements remain in force.

## Impact

Proposed runtime owner: opensoft/openXsoft-Hosted-Services; admitted estate identifier: openXsoft-Hosted-Services. Proposed accountable maintainer: Brett Heap, subject to explicit role and exact-scope acceptance. Source tasks: T028, T029, T030, T031, T032, T033, T039, T040, T041; coordinating owner acceptance: T013. The additional or directory-refined files are explicit in the design, never a broad prefix grant.

Source/CI custody is proposed as reviewed, redacted exports and genuine decision references retained in the private owning Git repository for project lifetime under existing permissions, bound to exact commits/content, actual run/job/command identities and owner review. The existing accepted receipt paths may contain sealed original source-output payloads; no unlisted export tree is granted. The coordinator authenticates the whole reviewed receipt before interpreting contained data. Missing provenance remains blocked. Target/customer/provider/live data requires its own protected C-08 decision before use.

This ratification accepts the exact source owner/file/command/custody scope and listed task-file refinements in the [ratification record](review/ratification.md). Implementation still requires its dependencies, consumed choices and a reviewed freeze. No target effect, resource spend, customer enrollment, commercial eligibility, merge or archive is granted. T013 still requires T010 and actual consumed decisions; source approval can be recorded early without marking its receipt/task complete. Full program Q0 and Q1–Q5 remain pending. Publication is in draft [PR #1310](https://github.com/opensoft/openXfactory/pull/1310).
