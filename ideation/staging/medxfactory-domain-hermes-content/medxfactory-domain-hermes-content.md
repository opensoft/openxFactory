# Staged: MedxFactory Domain Hermes Content (clinical roster, policies, councils, memory, catalog)

Status: superseded
Superseded by: [MedxFactory 2026-07-29-add-domain-hermes-roles-and-policies](https://github.com/MedxSoft/MedxFactory/tree/main/openspec/changes/archive/2026-07-29-add-domain-hermes-roles-and-policies) and [MedxFactory 2026-07-30-add-domain-hermes-councils-and-memory](https://github.com/MedxSoft/MedxFactory/tree/main/openspec/changes/archive/2026-07-30-add-domain-hermes-councils-and-memory)
Kind: architecture
Summary: Author the Medx Domain Hermes content — the clinical Plane-1 persona
roster directing the 11 ratified worker classes, the stored medical policy
delta, the domain review council (MxD-MRR formalized), escalation elevation,
domain memory boundaries, and the practice catalog — into
`hermes/domain/` per the prescribed shape proven by codexFactory (canonical
codex spec `domain-hermes-content`), in two MedxFactory OpenSpec increments
plus a lockstep Omnigent `directed_by` extension. Makes MedxFactory the
second domain complete on both layers; with the existing omnigent-install
second-domain fixture, one params file from a deployable medical stack.
Topics: medxfactory, domain-hermes, plane-1, clinical-roster, policies,
review-councils, mxd-mrr, escalation-rules, memory-boundaries,
practice-catalog, layer-content-seeding
Repository context: MedxFactory (`hermes/domain/` + `omnigent/domain-overlay.yaml` + `omnigent/overlay-manifest.yaml` digest re-pin in lockstep)
Staging ID: openxFactory:staging:medxfactory-domain-hermes-content
Source: team001 omnigent-program handoff next-unit mapping (2026-07-24);
MedxFactory `docs/` corpus (27 drafts — esp. mxd-medical-reasoning-review,
differential-discovery-engine, the Root Truth family, the patient-facing
safety pair, foundational-data-reliability); the codexFactory pattern
(archived `add-domain-hermes-roles-and-policies` +
`add-domain-hermes-councils-and-memory`); material inventory + pattern map
verified against both trees 2026-07-24.

## Outcome (recorded 2026-08-28)

COMPLETE. Both exit changes were ratified, realized and ARCHIVED, and both
archives were verified at the MedxFactory tree on 2026-08-28 — including
change B, which the staging INDEX row still described as outstanding:

| Exit | Repository | Archived packet |
| --- | --- | --- |
| Change A — roles + policies + `medx_owns` closure + Omnigent `directed_by` lockstep | MedxFactory | `openspec/changes/archive/2026-07-29-add-domain-hermes-roles-and-policies` |
| Change B — councils, mixes, escalation, memory, catalog | MedxFactory | `openspec/changes/archive/2026-07-30-add-domain-hermes-councils-and-memory` |

The residual non-gating items recorded in the decision round below
(practice-catalog seed set, client-layer-defaults analog timing) exited
WITH change B or sit in the MedxFactory capability spec; none is carried
here. The topic folder is retained as PROVENANCE — the reason this
document is `superseded` rather than deleted.

## Claims (verified 2026-07-24 against the trees; no roster decision yet)

1. **The prescribed shape exists and is proven.** codexFactory's
   `domain-hermes-content` capability (9 requirements from changes A+B, a
   10th from client-layer defaults) plus the neutral contracts:
   `hermes_domain_overlay` schema (contract-v1.15, canonical validator
   `openxFactory/scripts/validate-hermes-domain-overlay.py`) and the
   optional `hermes_domain_content_manifest` (contract-v1.18, 7-kind
   vocabulary, convention fallback). The hermes-install seeder consumes the
   conventional content set fail-closed and consistency-checks authority
   closure and persona↔worker bidirectionality at seed time.
2. **The worker plane is closed and ratified.** 11 clinical worker classes
   (`medical-omnigent-overlay` spec: neutral conformance, hypothesis-only
   output stance, never-assignable `order_sign`/`chart_write`/
   `truth_model_write`); specialist pods are `specialty`-parameterized
   instances of the same closed set. Unlike codex (which added two workers
   in lockstep), no new Medx worker class is currently expected — verify
   during change-A closure authoring.
3. **The roster derivation base is already named in ratified content.** The
   omnigent overlay's ambiguity routing table names domain-side authorities
   with no persona definition anywhere: `domain_evidence_curator`
   (annotated "Medx Domain Hermes / Root Truth ownership"),
   `safety_reviewer`, `hermes_governance_owner`, `compliance_owner` — plus
   the MxD-MRR convener role implied by
   `docs/mxd-medical-reasoning-review.md`. Cross-layer routes
   (`clinician_of_record`, `patient_consent_authority`,
   `care_organization_data_steward`) stay cross-layer, per the codex
   `cross_layer:` flag pattern.
4. **The existing `hermes/domain/` files are pre-contract stubs.**
   `overlay.yaml` (5-item prose `owns:` list) does not satisfy the v1.15
   schema (no `approval_scope_kinds`, `required_approval_fields`, or
   `authority_boundaries` with a `medx_owns` closure);
   `escalation-rules.yaml` / `memory-boundaries.yaml` carry pre-pattern
   kinds (`hermes_escalation_rules`, `hermes_memory_boundaries` — codex
   pattern is `hermes_domain_*`). Upgrade in place preserving the existing
   semantics: the four `requires_domain_review` items become policy/council
   material; the de-identification and consent-promotion booleans map onto
   the ratified memory-gateway vocabulary.
5. **Lockstep Omnigent obligations are mechanical but digest-coupled.**
   Change A must add `directed_by` to all 11 worker classes AND re-pin
   `omnigent/overlay-manifest.yaml` (sha256 over the overlay); check
   whether omnigent-install's `config/fixtures/medx-second-domain.manifest.yaml`
   pins the same digest and needs a lockstep refresh.
6. **The policy harvest is rich but undistilled.** Store-the-delta filter
   over the safety/root-truth corpus: foundational-data-reliability
   (charted data = fallible evidence), omnigent-trigger-boundary,
   patient-truth-and-simulation (immutable truth vs simulation models),
   decision-spine-verification, the patient-facing safety pair,
   root-truth-corpus-ingestion (legal-corpus provenance). Candidate `why`
   values reuse the codex controlled vocabulary; `gate` values will lean on
   admission/review gates rather than branch protection.
7. **Validator gap is known.** Medx `make validate` checks only generic
   `schema_version`+`kind` on `hermes/domain/*`; the canonical overlay
   validator must be invoked explicitly (and ideally wired into the Medx
   validate chain as part of change A).

## Exit path

- **Change A — `add-domain-hermes-roles-and-policies` (MedxFactory):**
  `hermes/domain/roles/*.yaml` (clinical personas, trait vocabulary v1,
  decide-then-speak guardrail, `directs_workers` over the 11 classes) +
  `hermes/domain/policies/` (medical position table, contested-position
  fields, store-the-delta) + `overlay.yaml` upgraded to the neutral schema
  with two-way `medx_owns` closure + the Omnigent lockstep (`directed_by`
  + manifest digest re-pin). Gated on the roster decision (open question 1).
- **Change B — councils, mixes, escalation, memory, catalog (MedxFactory):**
  `review-councils/` (MxD-MRR formalized with the convening-record
  pattern), `agent-mixes.yaml`, `escalation-rules.yaml` elevated onto the
  roster (nothing silently dropped; overlay stop conditions preserved),
  `memory-boundaries.yaml` in the gateway vocabulary (patient-derived
  de-identification), `medx_practice_catalog`. After A.
- **Care-organization / patient layer analogs (MxC-LOR, MxP-CIR):** NOT this
  topic's exit — see open question 2; formalization rides their own layer
  changes if so decided.

## Open questions

1. **Roster composition (change-A gating; needs a decision round).** How
   many clinical personas and which ones. Derived candidate set from the
   routing table + MxD-MRR + Root Truth governance claims, offered as
   decision input, NOT decided: a medical-reasoning lead (MxD-MRR convener;
   case framing + hypothesis workers), an evidence curator
   (`domain_evidence_curator`; Root Truth corpus governance; retrieval +
   base-rate workers), a verification lead (data reliability; simulation /
   test-utility / re-verification workers), a safety lead
   (`safety_reviewer`; safety + skeptic workers), a compliance lead
   (`compliance_owner`), a documentation lead (draft-documentation +
   convergence-packet workers), a governance coordinator
   (`hermes_governance_owner`; SC analog). Every one of the 11 workers
   needs exactly one directing persona; every `medx_owns` item an owning
   persona.
2. **Council placement across layers.** Only MxD-MRR is domain-owned;
   MxC-LOR belongs to the care-organization (tenant) layer and MxP-CIR to
   the patient (subject) layer. Leaning: change B formalizes MxD-MRR in
   `hermes/domain/review-councils/` and declares the three-gate
   convergence-packet flow with cross-layer references (codex gate-rules
   council precedent for cross-layer seats); MxC-LOR/MxP-CIR machine
   surfaces ride care-organization/patient layer changes.
3. **Specialist pods vs deliberation mixes.** Do `specialty`-parameterized
   pods map onto the codex two-tier mix model (`council_small`/
   `council_large`), or does Medx's deliberation live in the
   convergence-packet flow with mixes reserved for review ensembles?
4. **Practice catalog seed set.** Which promoted capabilities count as Medx
   practices (governed-derived-model conformance `governed` tier,
   decision-foundation-loop workflow, medical-omnigent-overlay itself?);
   kind name `medx_practice_catalog` per the domain-named-kind precedent.
5. **Content manifest.** Rely on the increment-4a convention like codex, or
   declare `hermes/domain/content-manifest.yaml` explicitly (contract-v1.18)
   — relevant if Medx deviates from the conventional file set.
6. **Client-layer defaults analog (10th requirement).** Care-organization
   defaults under the facts rule — this topic or a follow-on change once
   A+B land.

## Decision record (round with Brett, 2026-07-29)

The change-A gating decisions, ruled:

1. **Roster (open question 1) — DECIDED: the derived seven personas PLUS a
   dedicated ontology steward; eight total.** Medical-reasoning lead
   (MxD-MRR convener), evidence curator (`domain_evidence_curator`, Root
   Truth corpus), verification lead, safety lead (`safety_reviewer`),
   compliance lead (`compliance_owner`), documentation lead, governance
   coordinator (`hermes_governance_owner`), and — ruled over the
   merge-into-evidence-curator recommendation — a dedicated
   **ontology-steward persona** as the accountable ontology steward per the
   ratified `add-domain-ontology-layer` (replacing the pilot placeholder).
   Constraint holds: each of the 11 clinical workers gets exactly one
   directing persona from the seven; the ontology steward directs no
   Plane-2 worker today (its anchor is the `medx_owns` ontology items and
   the release-record `decided_by` line; the brainstormed
   ontology-maintenance micro-agent fleet is its future candidate-producing
   staff, advisory only).
   *Leanings carried to the change-A gate, not ruled:* the ontology review
   council is MxD-MRR wearing ontology seats (no fourth council), and
   `high_impact_requires: [licensed_human]` for clinical semantic change —
   both consistent with the round but confirmable at authoring.
2. **Council placement (open question 2) — DECIDED as the leaning:** change
   B formalizes MxD-MRR in `hermes/domain/review-councils/` with the
   convening-record pattern and the three-gate convergence-packet flow via
   cross-layer references; MxC-LOR and MxP-CIR machine surfaces ride the
   care-organization and patient layer changes.
3. **Pods vs mixes (open question 3) — DECIDED as recommended:** Medx
   deliberation IS the ratified convergence-packet flow with
   specialty-parameterized pods inside it; `agent-mixes.yaml` reserves
   `council_small`/`council_large` for review ensembles (MxD-MRR seats,
   contested positions). The ratified worker plane stays untouched.
4. **Content manifest (open question 5) — RESOLVED by ratified contract:**
   Medx declares `hermes/domain/content-manifest.yaml` explicitly
   (contract-v1.18 shape) including `domain_ontology`; the ontology-aware
   starter's STARTER marker makes the declaration mandatory under the
   generated-domain completeness rule.

Still open (non-gating): practice-catalog seed set (question 4, change-B
authoring input) and the care-organization defaults analog (question 6,
follow-on change).

## Readiness

**Change A UNBLOCKED (2026-07-29)** — the roster decision round is done
(see the decision record); pattern and material verified 2026-07-24;
everything else derives from ratified material. Change B follows A per the
codex sequence; no external gates (the omnigent overlay realization Medx
depends on is archived at `add-omnigent-domain-overlay`, contract-v1.16).
The ontology adoption steps ride change A per
[docs/domain-ontology-adoption-handoff.md](../../../docs/domain-ontology-adoption-handoff.md).
