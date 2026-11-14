---
code_surface: openxFactory, Headscale-Install
target_release: implemented — planned owner main-line realization; no implementation or release completion claimed
sequenced_after: [qualify-private-connectivity-production, establish-headscale-install-ownership]
---

# Proposal: Commission the supported Headscale package

Status: ratified
Ratified: 2026-11-14 by Brett Heap. [Ratification record](review/ratification.md)
Kind: proposal
Proposed: 2026-11-14

## Why

The existing install repository is an accepted synthetic pilot. Customer-operated and managed production need a supported package with real HTTPS identity, protected persistent state and qualified recovery, while preserving independent local operation.

## What Changes

- Commission Brett Heap as package/source/release maintainer for the exact production files, source commands and custody in the design, subject to his acceptance.
- Build the supported Linux Docker package with explicit immutable server/helper inputs, deny-before-enrollment, customer-controlled HTTPS identity and renewal checks, and guarded real-client qualification.
- Preserve single-writer fencing, protected backup/upgrade/quarantined restore and authoritative current revocations before activation. Keep all fixed 040 pilot guards and evidence intact.
- Prepare the proposed Linux Docker server plus Windows/macOS/Linux client matrix. The observed upstream stable v0.29.7 is a candidate to evaluate, not a reserved release or qualified image pin.
- Publish and independently read back the package candidate through the owner's reviewed release process; retain Q1–Q5 and target-appropriate execution authority before use.
- Use the exact per-task scope and source/custody obligations in [design](design.md). Implementation stays in the single [043 task list](../../../specs/043-private-connectivity-production/tasks.md), after dependencies and consumed choices pass.

## Capabilities

### New Capabilities

- headscale-production-package: the owner-specific production source, release and qualification boundary described in this packet.

### Modified Capabilities

None. The existing neutral binding, managed-subject, release, source-evidence and Q0–Q5 requirements remain in force.

## Impact

Proposed runtime owner: opensoft/Headscale-Install; admitted estate identifier: Headscale-Install. Proposed accountable maintainer: Brett Heap, subject to explicit role and exact-scope acceptance. Source tasks: T020, T021, T022, T023; coordinating owner acceptance: T011. The additional or directory-refined files are explicit in the design, never a broad prefix grant.

Source/CI custody is proposed as reviewed, redacted exports and genuine decision references retained in the private owning Git repository for project lifetime under existing permissions, bound to exact commits/content, actual run/job/command identities and owner review. The existing accepted receipt paths may contain sealed original source-output payloads; no unlisted export tree is granted. The coordinator authenticates the whole reviewed receipt before interpreting contained data. Missing provenance remains blocked. Target/customer/provider/live data requires its own protected C-08 decision before use.

This ratification accepts the exact source owner/file/command/custody scope and listed task-file refinements in the [ratification record](review/ratification.md). Implementation still requires its dependencies, consumed choices and a reviewed freeze. No target effect, resource spend, customer enrollment, commercial eligibility, merge or archive is granted. T011 still requires T010 and actual consumed decisions; source approval can be recorded early without marking its receipt/task complete. Full program Q0 and Q1–Q5 remain pending. Publication is in draft [PR #1310](https://github.com/opensoft/openXfactory/pull/1310).
