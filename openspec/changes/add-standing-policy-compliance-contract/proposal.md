---
code_surface: openxFactory (a NEW `contracts/intent-compliance/` family — machine-readable veto-class vocabulary, compliance-decision record, policy-allowance record and registry manifest, plus templates and packaged positive/negative examples — with a canonical `scripts/validate-intent-compliance.py`; registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle cut). No domain-specific detector, classifier prompt, workflow implementation, binding schema, or runtime registry service is added here. codexFactory is the first conformer through the named successor `add-intent-compliance-gate`.
target_release: next additive contract bundle (allocated at realization per `docs/contract-versioning-policy.md`)
Status: draft
Proposed: 2026-08-24
Origin: `opensoft/codexFactory:ideation/staging/front-end-compliance-gates/front-end-compliance-gates.md@2fae181` + codexFactory issue #3; decisions D1-D5 ruled by Brett Heap 2026-08-24
---

# Proposal: add-standing-policy-compliance-contract

## Why

A policy-violating intent can be approved, dispatched, built, reviewed and
only then vetoed because approved intent is not itself evidence of standing-
policy compliance. codexFactory's FEAT-003 reject pilot proved the waste and
the back-end fix; Brett ruled the prevention contract neutral-first because
egress, secret handling, external dependencies, privilege changes and safety-
control weakening are not engineering-only hazards.

## What Changes

- Add a neutral `intent-compliance` contract family defining:
  - a machine-readable standing-policy veto-class vocabulary with declared
    prose authority and digest;
  - a fail-closed compliance-decision record for `allow`, `block`, and
    `needs_human_review` outcomes;
  - first-class, revocable policy-allowance records in a governed registry;
  - reference-by-ID allowance consumption, with resolution repeated at the
    point of dispatch and admission;
  - loud evidence recording for every evaluation outcome.
- Require every consuming dispatch pathway to keep a deterministic compliance
  floor before worker invocation, even when a higher-order intake reviewer or
  Hermes manager is present.
- Name codexFactory's `add-intent-compliance-gate` as the first conforming
  realization: binding-approval validation plus a deterministic recheck with
  bounded-classifier escalation immediately before coding-worker dispatch.
- Preserve domain ownership: openxFactory defines the neutral record and gate
  obligations; each domain declares its veto classes, detectable signals,
  allowance issuers and enforcement realization.

## Capabilities

### New Capabilities

- `intent-compliance`: neutral standing-policy vocabulary, compliance-decision
  evidence, revocable policy-allowance registry, reference-resolution and
  permanent pre-dispatch floor obligations.

### Modified Capabilities

None. The existing `workflow-gate-contract` and `roles-authority-model`
remain unchanged; this capability composes with them rather than widening
their requirement sets.

## Impact

- **openxFactory contracts:** new `contracts/intent-compliance/` family,
  templates/examples, canonical validator, manifest and changelog entries.
- **codexFactory successor:** `approved-intent-binding` grows allowance
  references and compliance evidence; the reusable execution workflow gains
  the mandatory pre-dispatch evaluation; back-end managers resolve the same
  allowance references.
- **Hermes:** live intake managers remain judgment layers above the permanent
  deterministic floor; they do not subsume or disable it.
- **Governance:** tenant/company-policy authority issues allowances for its
  declared classes; domain authority issues domain-owned allowances. Revocation
  is additive and immediately effective at the next evaluation.
- **Non-goals:** no universal detector terms, classifier model, runtime service,
  tenant allowance instance, domain binding schema, or merge/council-clearance
  mechanism is implemented by this change.
