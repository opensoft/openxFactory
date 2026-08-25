# Tasks: add-standing-policy-compliance-contract

Governance-level and dependency-ordered. This change is proposed, not yet
ratified or realized. Section 1 is complete in this packet; Sections 2–5 are
the post-ratification contract realization and evidence gates.

## 1. Proposal and capability delta

- [x] 1.1 Author the `intent-compliance` ADDED requirement set covering
      authority-bound veto vocabulary, decision evidence, revocable policy
      allowances, governed registry resolution, permanent deterministic floor,
      bounded classifier escalation and cross-gate lockstep.
- [x] 1.2 Encode Brett Heap's 2026-08-24 D1–D5 rulings in proposal and design:
      neutral-first, gated classifier escalation, permanent floor, loud
      evidence and central revocable allowance registry.
- [x] 1.3 Name codexFactory `add-intent-compliance-gate` as the first conformer
      and keep council/merge-review concerns out of the capability boundary.

## 2. Contract schemas and templates

- [ ] 2.1 Create `contracts/intent-compliance/` with schema-versioned
      `veto-class-vocabulary`, `policy-allowance`,
      `policy-allowance-registry` and `compliance-decision` schemas.
- [ ] 2.2 Encode closed decision outcomes, class-ID uniqueness within a
      vocabulary, registry-qualified allowance references, immutable approval
      facts, additive revocation facts and deterministic registry revisions.
- [ ] 2.3 Require bindings/decisions to carry `(registry_id,
      registry_version, allowance_id)` only and reject embedded allowance
      payloads as authority evidence.
- [ ] 2.4 Add `.template.yaml` files for all four record kinds and ensure every
      contract file carries `contract_schema_version`, `schema_version` and
      `kind`, with their version relationship documented and validated.
- [ ] 2.5 Add shape-only neutral examples with placeholder classes; keep the
      five concrete codexFactory standing-policy classes and their evidence in
      successor `add-intent-compliance-gate`.

## 3. Canonical validator and corpus

- [ ] 3.1 Implement `scripts/validate-intent-compliance.py` with parse-once
      typed validation for all four record kinds.
- [ ] 3.2 Validate source-reference/digest presence, class-ID uniqueness,
      issuer closure, registry-qualified reference uniqueness, allowance
      validity, immutable approval facts and additive revocation fields.
- [ ] 3.3 Validate decision/content + vocabulary/policy digest binding,
      registry revision, allowance-record digests, domain scope-verdict
      evidence, closed outcomes and bounded opaque correlation facts.
- [ ] 3.4 Enforce evidence redaction/bounds: reject raw intent, provider
      prompt/response, tenant content, credentials and unbounded rationale or
      identifiers.
- [ ] 3.5 Enforce classifier hard caps (one invocation/turn, 65,536 input
      bytes, 8,192 output bytes, 4,096 output tokens, 60 seconds) and the
      `needs_human_review` outcome for absent limits, breach, timeout or error.
- [ ] 3.6 Add packaged positive examples for no-class allow, current-allowance
      allow, ambiguous-reference review and revoked-allowance block.
- [ ] 3.7 Add negative examples for duplicate class/allowance IDs, ambiguous
      registry references, embedded allowance payloads, unauthorized issuers,
      stale policy/vocabulary digests, undefined scope verdicts, raw evidence,
      missing `contract_schema_version`, unbounded classifiers and classifier
      override of a deterministic finding.
- [ ] 3.8 Prove every negative fixture fails for its intended reason and every
      positive fixture passes through the canonical validator.

## 4. Contract registration and release

- [ ] 4.1 Register the family in `contracts/manifest.yaml` with explicit
      artifact paths and the codexFactory first-consumer pointer.
- [ ] 4.2 Add the contract-family README/doc-index entry and document that
      registry instances live in consuming tenant/runtime repositories, never
      in openxFactory.
- [ ] 4.3 Allocate the next additive contract bundle fresh at realization and
      record the family in `contracts/CHANGELOG.md` per versioning policy.
- [ ] 4.4 Run the family validator, contract manifest validator, doc-health and
      all repository validators with zero new errors.

## 5. First-conformer evidence and archive gate

- [ ] 5.1 Raise codexFactory `add-intent-compliance-gate` against the released
      openxFactory bundle, adding allowance references and compliance evidence
      to the approved-intent binding and instantiating the five concrete
      standing-policy classes in codexFactory's own corpus.
- [ ] 5.2 Realize binding-approval compliance validation and the permanent
      deterministic pre-dispatch recheck before coding-worker invocation.
- [ ] 5.3 Realize bounded classifier escalation only for declared ambiguity or
      sensitive paths, with hard limits and separate evidence.
- [ ] 5.4 Re-run FEAT-003: no allowance blocks before dispatch; a current valid
      allowance passes; revocation blocks the next dispatch and admission.
- [ ] 5.5 Archive this change only after the contract release is merged and
      green, the first-conformer change is linked, and realization evidence
      names the bundle version and validation results.
