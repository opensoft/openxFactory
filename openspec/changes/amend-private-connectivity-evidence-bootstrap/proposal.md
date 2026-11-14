---
code_surface: openxFactory
target_release: deferred-allocation
sequenced_after: [commission-private-connectivity-production-evidence]
---

# Proposal: Bind the private-connectivity evidence bootstrap

Status: ratified
Ratified: 2026-11-14 by Brett Heap. [Ratification record](review/ratification.md)
Kind: proposal
Proposed: 2026-11-14

## Why

Feature 043 T007–T009 implement the read-only evidence controls, but T010's frozen file list contains only its workflow and receipt. It omits a durable reviewed commissioning input and the declaration/census promotion needed when the first real evidence pins arrive. Inventing bootstrap receipts, treating a generated manifest as approval, or silently expanding T010 would violate the accepted evidence contract.

## What Changes

- Add exactly specs/043-private-connectivity-production/evidence/commissioning.json for reviewed source-only E control inputs and original authenticated bootstrap/CI exports, plus the exact authentication review record named in [design](design.md). Keep source Git custody, project-lifetime retention, existing repository access and Brett Heap's custodian responsibility.
- Bind in-container objects to their containing immutable commissioning commit/path/SHA-256. References to original source/governance artifacts remain exact Git-object references. Reject free-standing object references, missing objects, cycles, fabricated pass outputs and live/customer evidence under this source-only format.
- Refine T010's exact file list to include those two records and the already commissioned declaration/census paths needed for first-record promotion. Refresh the review freeze only after actual owner acceptance; preserve all 68 task identities, owners, cases, dependencies and Q0–Q5 gates.
- Keep T009's currently empty production members FUTURE until actual T010 evidence exists; promote from a real measured population, without rolling/exclusion workarounds or invented census values. Add only the exact commissioning JSON to the production pin paths.
- Continue implementation and validation through the single [043 task list](../../../specs/043-private-connectivity-production/tasks.md). This proposal supplies no second executable implementation list.

## Capabilities

### New Capabilities

- private-connectivity-evidence-bootstrap-custody: exact source-only commissioning storage, authenticated contained-object references and deliberate first-record pin promotion.

### Modified Capabilities

None. The existing evidence, rollout, release, reachability and managed-subject requirements continue to apply.

## Impact

The exact files, input format and T010 refinement are in [design](design.md). Existing verifier/inventory helpers and their tests remain inside the already accepted E source scope; shared changes stay inside the commissioned pin reader, affected census/regressions and required pytest workflow. No published contract or bundle version is changed.

The accepted accountable owner and source-evidence custodian is Brett Heap; see the ratification record. This proposal's ratification authorizes only the bounded source-control repair and subsequent preparation of authentic exports. It does not authenticate unseen outputs: the actual commissioning data and original output/human-decision provenance still need the separate recorded custodian review before T010 can pass.

Full program Q0 and Q1–Q5 remain unaccepted/unentered. No provider operation, resource spend, customer enrollment, commercial admission, merge or archive is authorized. [PR #1310](https://github.com/opensoft/openXfactory/pull/1310) remains draft.
