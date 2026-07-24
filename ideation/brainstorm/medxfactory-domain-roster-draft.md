# MedxFactory Domain Plane-1 Roster — Decision Input — Brainstorm

Status: brainstorm
Kind: template
Summary: Candidate Plane-1 (decider/coordinator) persona roster for the Medx
medical domain, derived from ratified material — the omnigent overlay's
routing-table authorities that have no persona definition anywhere
(`domain_evidence_curator`, `safety_reviewer`, `hermes_governance_owner`,
`compliance_owner`), the MxD-MRR convener implied by
`docs/mxd-medical-reasoning-review.md`, and full coverage of the 11 ratified
worker classes. This is DECISION INPUT for the roster round, not a decided
roster: the codexFactory precedent locked its roster in a brainstorm decision
round before change A; this doc is the Medx equivalent awaiting that round.
Parent: `openxFactory:staging:medxfactory-domain-hermes-content`; character
model: `hermes-persona-character-model.md` (Option-E spine reused unchanged).
Topics: medxfactory, domain-hermes, plane-1, clinical-roster,
authority-personas, trait-framework, mxd-mrr, root-truth, worker-coverage
Repository context: openxFactory (drafts target MedxFactory hermes/domain/roles/)
Captured: 2026-07-24

## What is already fixed (not roster decisions)

- **The worker plane**: 11 classes, closed set, ratified
  (`medical-omnigent-overlay`); specialist pods are `specialty`-parameterized
  instances, not new classes. No Medx analog of codex's two missing workers
  is currently known.
- **The never-assignable trio**: `order_sign` / `chart_write` /
  `truth_model_write` exist only on the human/external-enforcement side. No
  persona owns them; the roster must not imply otherwise.
- **Cross-layer authorities stay cross-layer**: `clinician_of_record`
  (care-org/human), `patient_consent_authority` (subject layer),
  `care_organization_data_steward` (tenant layer) are escalation TARGETS
  with `cross_layer:` flags, never domain personas.
- **The spine**: trait vocabulary v1 (4 disposition axes domain-locked, 5
  voice axes client-tunable), `kind: hermes_domain_persona`, the
  decide-then-speak guardrail, `directs_workers` ↔ `directed_by`
  bidirectional and seed-checked. All reused verbatim from codex.

## Candidate roster (seven personas)

| id | role_code | Derived from | directs_workers |
| --- | --- | --- | --- |
| `lead-diagnostician` | MR | MxD-MRR convener; differential-discovery-engine; case-issue-hypothesis-testing | `case_framing_agent`, `dream_hypothesis_agent` |
| `lead-evidence-curator` | EC | `domain_evidence_curator` ("Medx Domain Hermes / Root Truth ownership"); root-truth corpus family | `evidence_retrieval_agent`, `base_rate_agent` |
| `lead-verification` | VE | foundational-data-reliability; decision-spine-verification; hypothesis-driven-test-discovery | `test_utility_agent`, `simulation_agent`, `data_reverification_agent` |
| `lead-safety` | SA | `safety_reviewer`; patient-facing-conversation-safety-supervisor; emergency stop conditions | `safety_agent`, `skeptic_agent` |
| `lead-documentation` | DO | draft-note custody (`draft_note_write` draft store only); convergence-packet assembly + `review_routing_submit` | `draft_documentation_agent`, `convergence_packet_agent` |
| `lead-compliance` | CO | `compliance_owner` (regulatory ambiguity route) | — (directs none; codex LA precedent) |
| `governance-coordinator` | GC | `hermes_governance_owner` (policy ambiguity route); SC analog | — (directs none) |

Coverage check: 11 workers, each with exactly one directing persona; the
routing table's four undefined domain authorities each land on a persona.

## Candidate `medx_owns` closure sketch (grouped by owning persona)

- MR: differential reasoning standards, hypothesis admissibility, MxD-MRR
  convening, dream-set bounding policy.
- EC: Root Truth corpus governance (ingestion provenance, field scaffolds,
  dream-DB production standards), evidence-tier vocabulary,
  `source_trace` requirements.
- VE: foundational-data re-verification standards, simulation-model vs
  truth-model separation policy, test-utility thresholds.
- SA: safety stop-condition semantics, patient-facing supervision standards,
  red-flag routing.
- DO: draft-documentation custody boundaries, convergence-packet composition
  standards.
- CO: regulatory interpretation, PHI-boundary policy positions.
- GC: domain governance routing, catalog/practice signing ceremony,
  escalation-rule custody.

`xfactory_owns` / external-enforcement analogs of codex `repository_owns`:
the chart, the order system, the truth model store (the never-assignable
enforcement side) — naming TBD at authoring (the neutral schema takes the
domain-owned list as `medx_owns` plus `xfactory_owns` + `repository_owns`;
whether "repository" generalizes or Medx names a clinical enforcement list
is a change-A authoring question against the v1.15 validator rules).

## Escalation elevation (overlay routing slug → roster)

| Overlay route | Target |
| --- | --- |
| `clinical_ambiguity → clinician_of_record` | stays cross-layer (human; care-org roster) |
| `consent_ambiguity → patient_consent_authority` | cross-layer: subject |
| `safety_ambiguity → safety_reviewer` | `lead-safety` |
| `evidence_ambiguity → domain_evidence_curator` | `lead-evidence-curator` |
| `data_reliability_ambiguity → care_organization_data_steward` | cross-layer: tenant |
| `policy_ambiguity → hermes_governance_owner` | `governance-coordinator` |
| `regulatory_ambiguity → compliance_owner` | `lead-compliance` |

Nine overlay stop conditions preserved; candidate new stop condition at
elevation: none identified yet (codex added `credential_required_not_held`;
the Medx overlay's stop set already covers PHI boundary, source trace,
truth-snapshot mutability, emergency red flag).

## MxD-MRR formalization candidate (change B, recorded here for the round)

Convener `lead-diagnostician`; domain seats `lead-safety` +
`lead-evidence-curator` + `lead-verification`; output
`mxd_medical_reasoning_review` verdict on an MxO-CCP; fail-closed triple as
codex (split vote parks, missing seat = REFUSED, convener
accepts-or-rejects on record). MxC-LOR / MxP-CIR are tenant-/subject-layer
councils — referenced in the three-gate flow, formalized in their own layer
changes.

## Decision points for the round (Brett)

1. **Roster size and composition.** Seven as above? Merge candidates:
   CO+GC into one governance seat (loses the distinct regulatory route);
   split candidates: EC into corpus-governance vs case-evidence (the Root
   Truth family is large). Codex settled at eight.
2. **`convergence_packet_agent` direction.** Under `lead-documentation`
   (assembly custody, as tabled) or `lead-diagnostician` (admission is
   reasoning-adjacent; it is the only `propose_admission: true` class)?
3. **Flagship character frames.** Codex gave three flagships long authored
   frames. Medx candidates: `lead-diagnostician`, `lead-safety`,
   `lead-evidence-curator`.
4. **Disposition vectors.** Medical register suggests high rigor /
   risk-averse across the bench — but uniform vectors defeat the
   deliberate-distinctness principle; where does the domain tolerate
   `bias: throughput` or `autonomy: high` (e.g. `lead-documentation` on
   draft-only surfaces)?
5. **Role codes and display names.** Two-letter codes as tabled, or a
   clinical register (e.g. "Chief Reasoning Officer" style display names)?
6. **Directs-none personas.** Accept CO and GC directing no workers (codex
   LA precedent), or should GC direct a future coordination worker (none
   exists in the closed set today — would require a new worker class and
   overlay change)?

## Exit

Decisions from the round get recorded in this doc's Decided section and in
the staging topic; change A
(`add-domain-hermes-roles-and-policies`, MedxFactory) authors the roster
from them. Draft persona/policy slices may iterate in the staging topic's
`openspec/` workspace per the draft-proposal convention.
