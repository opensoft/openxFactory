# Design: add-standing-policy-compliance-contract

Status: draft
Kind: design

## Context

codexFactory's FEAT-003 pilot encoded unconditional external egress in an
approved intent. Deterministic checks passed, the worker built it, governed
review admitted it with conditions and all three managers initially deferred
to the approved intent. The ratified back-end standing-policy veto now blocks
the same candidate, but only after worker cost and candidate creation.

The consuming pipeline has two prevention seams: binding approval before
`status: approved`, and the reusable execution workflow immediately before
worker dispatch. Today no executable pre-dispatch path consumes standing-
policy vocabulary or allowance evidence.

Five decisions were ruled by Brett Heap on 2026-08-24: neutral-first ownership;
deterministic scan with bounded-classifier escalation; permanent deterministic
floor beneath Hermes; loud evidence for every outcome; and a central revocable
allowance registry referenced by ID.

## Goals / Non-Goals

**Goals:**

- Define domain-neutral records and obligations for intent compliance.
- Keep veto-class definitions machine-readable but subordinate to declared
  ratified policy authority.
- Make allowance revocation effective at every later evaluation point.
- Preserve one decision vocabulary and one allowance citation from intent
  approval through dispatch and admission.
- Require a permanent deterministic floor regardless of higher-order reviewer
  or Hermes availability.

**Non-Goals:**

- Standardize detector keywords, AST rules, classifier prompts or models.
- Implement a registry service or store tenant allowance instances.
- Modify codexFactory binding/runtime files in this neutral change.
- Define council clearance, merge readiness or substantive PR review.
- Permit a model classifier to replace the deterministic floor.

## Decisions

### D1 — Neutral-first contract, domain-owned realization

openxFactory owns the closed record shapes and cross-domain obligations now;
codexFactory becomes the first conformer. Every domain still owns its concrete
veto classes, detectable signals, issuer mapping and runtime evaluator.

**Alternative rejected:** wait for a second domain consumer. Brett ruled the
universal hazard family too load-bearing to leave local; egress, secret
handling and privilege changes recur anywhere agents dispatch external work.

### D2 — Deterministic floor plus bounded escalation

Every dispatch runs a deterministic evaluator. A consuming domain may invoke
one bounded classifier only when deterministic rules mark ambiguity or a
declared sensitive surface. The classifier is fail-closed and token-capped;
its output is evidence, never authority to erase a deterministic finding.

**Alternatives rejected:** deterministic-only accepts avoidable paraphrase
evasion; classifier-on-every-dispatch puts probabilistic cost in the hot path.

### D3 — Permanent floor beneath Hermes

Live Hermes intake adds contextual judgment but never disables the
deterministic gate. The floor survives deployment, outage and model changes.

**Alternative rejected:** retiring the floor at Hermes cutover removes cheap
defense in depth and ties basic refusal to a higher-order service.

### D4 — Loud evidence for every outcome

Every evaluation emits a compliance-decision record, including `allow`. The
record binds outcome, class findings, bounded rationale codes/redacted detail,
policy/vocabulary digests, registry revision, resolved allowance-record
digests, evaluator version, evaluated-content digest, bounded opaque
correlation references and evaluation time. Raw intent, provider payloads,
tenant content and credentials are prohibited. This supports audit, drift
detection and aggregate policy demand without turning evidence into a second
content store.

**Alternatives rejected:** quiet passes or rejects make later dispatch and
admission unable to prove they evaluated the same intent under the same rules.

### D5 — Central revocable allowance registry

Allowances are first-class records; bindings carry a registry-qualified
reference `(registry_id, registry_version, allowance_id)`, never copied
payloads. Registry revisions and resolved allowance-record digests bind every
decision to the state it actually evaluated.
Approval fields are immutable. Revocation is additive and immediately controls
the next evaluation. A missing/unreadable reference produces
`needs_human_review`; a resolved revoked allowance produces `block`.

**Alternative rejected:** embedded allowance objects cannot reflect revocation;
free-text citations cannot be resolved deterministically.

### Record family

The realization produces four interoperable artifacts:

1. `veto-class-vocabulary` — policy-source reference/digest, class identifiers,
   unique-within-vocabulary class identifiers, owner/issuer roles and
   domain-declared detection metadata.
2. `policy-allowance` — stable ID, class/scope, policy approval reference,
   issuer identity/authority, approval time and additive revocation state.
3. `policy-allowance-registry` — registry identity/version and allowance
   collection, with a monotonically identified revision, unique IDs and
   deterministic resolution semantics.
4. `compliance-decision` — evaluated-content digest, evaluator/version,
   policy/vocabulary digest, registry revision, findings, resolved allowance
   record digests, scope-resolution verdicts, outcome and bounded/redacted
   correlation evidence.

Allowance scope semantics remain domain-owned. A neutral scope reference binds
`scope_kind`, `scope_ref`, operations and a scope digest; a domain resolver
emits `covers | does_not_cover | indeterminate` bound to the evaluated-content
and scope digests. The neutral outcome mapping is fixed: `covers` may satisfy
that class, `does_not_cover` blocks, and `indeterminate` needs human review.

Classifier escalation has a machine-checkable limit envelope: exactly one
invocation and one turn, at most 65,536 input bytes, 8,192 output bytes, 4,096
output tokens and 60 seconds. It receives a redacted bounded excerpt, never the
raw evidence corpus. Missing limits, limit breach, timeout or invocation error
produces `needs_human_review` and no dispatch.

The vocabulary schema constrains shape, not universal class membership. The
codexFactory first conformer will instantiate its ratified five classes.

## Risks / Trade-offs

- **[Neutral contract outruns consumers]** → codexFactory is a named first
  conformer and its FEAT-003 regression is the realization gate.
- **[Prose and machine vocabulary drift]** → vocabulary records declare and
  digest the ratified source; mismatched digest is a finding and blocks release.
- **[Registry unavailable]** → missing/unreadable resolution fails closed to
  `needs_human_review`; cached allowance payloads never substitute.
- **[Revocation race]** → every dispatch and admission re-resolves allowance
  IDs; earlier `allow` evidence does not authorize later execution.
- **[Classifier becomes authority]** → contract requires deterministic floor
  and records classifier contribution separately under closed hard limits.
- **[Evidence volume]** → consumers may tier retention, but may not omit the
  bounded/redacted decision record or its opaque join keys; raw content and
  provider payloads are validation failures.

## Migration Plan

1. Ratify this neutral requirement set.
2. Realize and release the four record schemas/templates, validator and corpus
   in the next additive openxFactory contract bundle.
3. Propose/realize codexFactory `add-intent-compliance-gate` against that
   release: instantiate the five classes, grow the binding by allowance refs
   and evidence, gate approval, and recheck before dispatch.
4. Re-run FEAT-003: no allowance blocks before worker dispatch; a valid
   allowance passes; revoking it blocks the next dispatch and admission.
5. Additional domains adopt only after declaring their own vocabulary source,
   class owners and allowance issuers.

Rollback never means permitting unevaluated dispatch. A consumer unable to
read the contract parks work for human review while returning to the prior
released bundle.

## Open Questions

None. D1-D5 were ruled by Brett Heap on 2026-08-24.
