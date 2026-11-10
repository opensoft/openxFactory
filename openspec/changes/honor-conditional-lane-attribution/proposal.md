---
Status: draft
Kind: governance
Authored: 2026-11-10
code_surface: openxFactory — .github/workflows/lane-line.yml, tests/lane_line/test_conditional_lane_line.py and the generated new-packet row in tests/sequenced_after/corpus-ledger.yaml
target_release: implemented — repository CI on main; archive only after merged-and-green realization; no product contract release
---

# Honor Conditional Lane Attribution

## Why

The current required lane-line check refuses every human-authored PR without a first-line lane declaration. This contradicts the in-force conditional attribution rule and blocks the wallet/MFA design capture.

## What Changes

- Permit an absent lane declaration for work produced outside a lane.
- Validate a supplied declaration using the existing first-nonempty-line format; reject malformed, duplicate, or misplaced declarations.
- Preserve existing bot exemptions, event triggers, permissions, check name, review requirements and branch protections.
- Execute the exact workflow shell in deterministic regression cases with untrusted body content passed through the environment.

## Capabilities

### New Capabilities

- `conditional-lane-attribution`: conditional lane declaration validation for this repository's required lane-line check.

### Modified Capabilities

None. Domain workflow contracts and merge-authority grants are unchanged.

## Authority and scope

Brett Heap's in-force lane-collision Amendment 21, directed 2026-09-30, already supplies the policy: sessions outside a lane need no tag; lane-bound sessions retain their obligations. On 2026-11-10 the owner commissioned realization: "Go ahead and fix the lane-check mismatch through the governed process, finish landing the design PRs, and prepare the OpenSpec proposal and Speckit feature for the first codeXfactory pilot."

This packet records realization of that existing decision; it does not claim a new ratification of this prose. CI cannot independently establish the author's launch/binding. An absent declaration is not proof of non-membership. Authors remain responsible for actual membership, overlapping-work checks and existing holds. No lane is invented and no register is changed.

## Impact

Repository-local workflow and tests only. No credentials, product runtime, auto-approval envelope, CODEOWNERS, protected-branch rule, or review-authority floor changes. The codeXfactory tracked-file probe must be remeasured when this packet adds files.

## Implementation handoff

Exactly one feature owns this repository's execution list: [feature specification](../../../specs/041-conditional-lane-check/spec.md) and [tasks](../../../specs/041-conditional-lane-check/tasks.md). Its evidence records exact checks and landing; the packet remains active until merged-and-green realization is recorded.
