# Proposal (draft): add-domain-hermes-councils-and-memory

Status: draft
Draft slice of: ../codexfactory-domain-hermes-content.md
Target repo at promotion: codexFactory `openspec/changes/add-domain-hermes-councils-and-memory/`
code_surface: codexFactory (hermes/domain/ — governed content, no runtime code)
Gate: author AFTER the `add-omnigent-domain-overlay` codexFactory realization
lands (its archetype-shaped overlay is what escalation-rules elevates from).

## Why

Change A (`archive/2026-07-22-add-domain-hermes-roles-and-policies`) landed
the deciders and the stored policy delta; the domain still cannot *deliberate*
(no declared MoA mixes), *escalate* (routing lives only in the Omnigent
overlay, naming pre-roster role slugs), *convene* (no council objects), or
*learn* (no memory boundaries, no practice catalog). This change authors the
second half of the Domain Hermes content. All gating decisions are made
(2026-07-22 B-gating round + the brainstorm cluster's dated Decided sections).

## What Changes

- **`hermes/domain/agent-mixes.yaml`** — MoA profiles: `panel_synthesis`
  (default, execution binding `review_lane_ensemble`), `scored_vote`,
  `council_small` (convener + 2 seats drawn from the trigger→seats table:
  security→lead-security, quality→lead-quality, architecture→lead-architect),
  `council_large` (full bench) with the enumerated triggers
  (`security_ambiguity_parked`, `standard_contested`,
  `architecture_commitment`, `gate_weakening_change`, `spend_over_envelope` —
  the last wired to the client's FAO budget envelope; the domain declares
  only the trigger, an un-tuned client parks). Guardrails: advisory-only,
  governed context packet, no standing credentials, Lead-accepted roster
  changes (`REVIEW_MODELS` → Lead Quality accepts + evidence record).
- **`hermes/domain/review-councils/`** — the two permanently distinct
  councils: `merge-readiness.yaml` (per-PR; members lead-quality,
  lead-security, lead-integration; output `merge_readiness_packet`) and
  `gate-rules.yaml` (per-repo rule-setting; domain seats lead-architect,
  lead-security, lead-quality; client seat **company-policy-lead** with the
  CSC conjunction pull-in on security-touching rules; project seat the
  **intent-owner role-slot (symbolic)** until the project roster lands;
  `human_step: acknowledgement_of_notice`; output `per_repo_gate_rules`,
  mechanically enforced by the Merge Master operator via
  `scripts/merge_master/envelope.py`). Failure semantics: split → park for
  liaison; missing required seat → REFUSED, never defaults.
- **`hermes/domain/escalation-rules.yaml`** — elevate `routing:` +
  `stop_conditions:` from the (archetype-shaped) Omnigent overlay onto roster
  persona ids; cross-layer targets flagged (`product_ambiguity` →
  customer/project intent-owner; `policy_ambiguity` → company-policy-lead);
  stop conditions gain `credential_required_not_held`; `on_stop:
  park_fail_closed`.
- **`hermes/domain/memory-boundaries.yaml`** — cross-client domain learning
  vs. client-private denial, in the ratified gateway vocabulary; write
  authority worker-proposes/owning-Lead-accepts (no ratification); the
  de-identification contract (structural schema + Lead attestation) with the
  seeded `finding_class` starter vocabulary: `recurring_review_finding`,
  `known_bad_pattern`, `flaky_regression`, `practice_effectiveness_signal`,
  `efficiency_finding` (extensions Lead-accepted; neutralize with the DTN
  batch later).
- **`hermes/domain/practice-catalog.yaml`** — the four verified adoption
  profiles (doc-health-sweep, conformance-gate, governed-review-lane,
  credential-contracts) with `promoted_in` + `owning_lead`; proportional
  signing (new/removed practice = codex OpenSpec change; parameter tweaks =
  owning-Lead-accepted).

## Impact

- Content-only YAML under `hermes/domain/`; gated by `scripts/validate-docs.sh`.
- Consumes change A's persona ids (landed) and the archetype-shaped Omnigent
  overlay (gate above).
- Completes the seedable Domain Hermes content set — after B, seeding
  increment 2 has the full enforceable slice to materialize.
