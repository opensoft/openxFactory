# Staged: A dedicated `manager_review` approval-scope kind

Status: staged
Kind: staging-packet
Summary: The governed-approval vocabulary's `approval_scope_kinds` enum has
no dedicated kind for manager-review jobs, so the three governed
manager-review jobs the 011 gate commissions per candidate admission packet
currently type their approvals under the `engineering_intent` fallback. This
topic registers the upstream openxFactory vocabulary extension the gate's own
implementation plan raised and deferred.
Topics: governed-approval, approval-scope-kinds, hermes-domain-overlay, job-envelope, manager-review, contract-fidelity, hermes-install
Repository context: openxFactory owns the neutral `hermes-domain-overlay`
contract family that defines `approval_scope_kinds` (schema:
`contracts/hermes-domain-overlay/hermes-domain-overlay.schema.yaml`,
canonical spec `openspec/specs/hermes-domain-overlay/spec.md`); the seeded
overlay instance that admits the new kind lands wherever each domain's
overlay is materialized (e.g. `xFactory-Hermes-Install` seeding); the
motivating consumer is `xFactory-Hermes-Install` feature
`011-three-layer-manager-review-gate`.
Staging ID: openxFactory:staging:manager-review-approval-scope-kind
Captured: 2026-08-10
Source: `xFactory-Hermes-Install` feature `011-three-layer-manager-review-gate`
implementation plan (`specs/011-three-layer-manager-review-gate/plan.md`,
Complexity Tracking entry T2, recorded 2026-08-10); ruled "register now" by
Brett Heap 2026-08-10.
Target capabilities: `hermes-domain-overlay` (MODIFIED — additive vocabulary
extension to `approval_scope_kinds`)

## Context

The governing OpenSpec change `add-three-layer-manager-review-gate` (ratified
2026-07-29) commissions three governed manager-review jobs per candidate
admission packet in the three-layer Hermes install. Typing those jobs'
approvals honestly — so clearance policy and audit can tell a manager-review
approval apart from an intent approval — needs the seeded domain overlay's
`approval_scope_kinds` to admit a dedicated `manager_review` kind. That
vocabulary lives upstream in openxFactory, not in the install repo, so under
the Hermes install constitution's Contract Fidelity principle (stop-and-raise
on a neutral-policy gap, never fork or shadow it locally) the install cannot
add the kind itself.

The 011 gate's implementation plan recorded this as tension T2 and chose to
proceed for v1 on the existing `engineering_intent` fallback rather than
block the gate on an upstream contract change. This topic is the deferred
vocabulary tightening that fallback owes.

## Claims

1. **Manager-review approvals currently ride `engineering_intent`, which is
   honest-but-loose typing.** The fallback is not wrong — `engineering_intent`
   is a real member of the enum and the approval genuinely is one — but it
   collapses a distinct approval class (a manager reviewing a candidate
   admission packet) into the same bucket as ordinary intent approvals, so
   nothing downstream can tell the two apart by scope kind alone.
2. **A dedicated `manager_review` kind lets clearance policy and audit
   discriminate manager reviews from intent approvals.** Once the kind
   exists, overlay authors can write clearance rules and audit queries that
   target manager-review approvals specifically, instead of pattern-matching
   on job metadata to recover a distinction the vocabulary should carry
   directly.
3. **This is additive, not corrective.** `approval_scope_kinds` is an open
   array (`minItems: 1`, string items, no fixed enum) per domain overlay, so
   adding `manager_review` as an admitted member is a vocabulary extension a
   domain overlay opts into — it does not invalidate any overlay that keeps
   using `engineering_intent` for jobs it has not migrated.

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

No conflicts recorded.

## Open questions

1. **Envelope vs. overlay home**: does `manager_review` belong in the neutral
   job envelope's approval-scope vocabulary (if one is centrally enumerated
   there) or purely as a per-domain `hermes-domain-overlay` addition that the
   engineering overlay (and any other domain running manager-review gates)
   opts into independently? Leans toward the overlay-local addition given
   `approval_scope_kinds` is already an open per-overlay array, but the
   neutral-job-envelope capability should be checked for any shared
   approval-scope enumeration this would need to stay consistent with.
2. **Naming and scope precision**: whether `manager_review` alone is
   sufficiently precise, or whether the three distinct governed jobs the 011
   gate commissions per packet warrant finer-grained kinds (e.g. distinct
   review stages) rather than one shared kind — deferred until the live
   gate's evidence shows whether one kind or several is the right grain.

## Exit

An OpenSpec change in openxFactory extending `hermes-domain-overlay`
(`approval_scope_kinds`) with the `manager_review` kind, raised when the live
011 three-layer manager-review gate's operating evidence justifies the
tightening (i.e. once the v1 `engineering_intent` fallback has run for real
candidate admission packets and the discrimination gap is felt, not merely
anticipated). `code_surface`: openxFactory contract + spec deltas; the
engineering domain overlay's adoption of the new kind is a follow-on
realization in the consuming domain repo, not part of this exit.
