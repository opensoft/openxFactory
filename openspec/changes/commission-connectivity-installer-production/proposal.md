---
code_surface: openxFactory, xFactory-Installer
target_release: implemented — planned owner main-line realization; no implementation or release completion claimed
sequenced_after: [qualify-private-connectivity-production, implement-private-connectivity-binding]
---

# Proposal: Commission the production private-connectivity installer

Status: ratified
Ratified: 2026-11-14 by Brett Heap. [Ratification record](review/ratification.md)
Kind: proposal
Proposed: 2026-11-14

## Why

The installer has qualified pilot selection and migration semantics, but no production package/backend or customer command. Production needs a usable install/connect workflow against supported package and hosted-service releases, without forcing hosted enrollment.

## What Changes

- Commission Brett Heap as installer/source/distribution maintainer for the exact adapter, CLI/package, validation and release surfaces in the design, subject to his acceptance.
- Implement real local install-new/connect-existing/unbound and managed selection using verified supported neutral/package/service content, preserving independent customer-operated use.
- Add the actual private-connectivity command and deterministic wheel/package build surface. Refine T026 by the two explicitly listed CLI/test files instead of burying a new entry point in an unapproved path.
- Retain original request/cleanup subjects, durable retry/migration state, target cleanup before prior-binding reauthorization, and refusal of revoked/expired/unentitled rollback.
- Keep workstation-intake, Store publication, unrelated installer features, repository visibility and a new public package registry outside this scope.
- Use the exact per-task scope and source/custody obligations in [design](design.md). Implementation stays in the single [043 task list](../../../specs/043-private-connectivity-production/tasks.md), after dependencies and consumed choices pass.

## Capabilities

### New Capabilities

- connectivity-installer-production: the owner-specific production source, release and qualification boundary described in this packet.

### Modified Capabilities

None. The existing neutral binding, managed-subject, release, source-evidence and Q0–Q5 requirements remain in force.

## Impact

Proposed runtime owner: opensoft/xFactory-Installer; admitted estate identifier: xFactory-Installer. Proposed accountable maintainer: Brett Heap, subject to explicit role and exact-scope acceptance. Source tasks: T024, T025, T026, T034, T035; coordinating owner acceptance: T012. The additional or directory-refined files are explicit in the design, never a broad prefix grant.

Source/CI custody is proposed as reviewed, redacted exports and genuine decision references retained in the private owning Git repository for project lifetime under existing permissions, bound to exact commits/content, actual run/job/command identities and owner review. The existing accepted receipt paths may contain sealed original source-output payloads; no unlisted export tree is granted. The coordinator authenticates the whole reviewed receipt before interpreting contained data. Missing provenance remains blocked. Target/customer/provider/live data requires its own protected C-08 decision before use.

This ratification accepts the exact source owner/file/command/custody scope and listed task-file refinements in the [ratification record](review/ratification.md). Implementation still requires its dependencies, consumed choices and a reviewed freeze. No target effect, resource spend, customer enrollment, commercial eligibility, merge or archive is granted. T012 still requires T010 and actual consumed decisions; source approval can be recorded early without marking its receipt/task complete. Full program Q0 and Q1–Q5 remain pending. Publication is in draft [PR #1310](https://github.com/opensoft/openXfactory/pull/1310).
