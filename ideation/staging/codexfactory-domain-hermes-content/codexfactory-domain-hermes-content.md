# Staged: codexFactory Domain Hermes Content (roles, policies, councils, memory, catalog)

Status: superseded
Superseded by: [codexFactory 2026-07-22-add-domain-hermes-roles-and-policies](https://github.com/opensoft/codexFactory/tree/main/openspec/changes/archive/2026-07-22-add-domain-hermes-roles-and-policies) and [codexFactory 2026-07-23-add-domain-hermes-councils-and-memory](https://github.com/opensoft/codexFactory/tree/main/openspec/changes/archive/2026-07-23-add-domain-hermes-councils-and-memory)
Kind: architecture
Summary: Author the codexFactory Domain Hermes content — the Plane-1 persona
roster, the stored policy delta, the review councils and agent mixes, the
domain memory boundaries, and the practice catalog — into `hermes/domain/`
per the prescribed shape, in two codexFactory OpenSpec increments plus a
lockstep Omnigent overlay extension. This is the critical-path topic: the
runtime's seeding increment 2 (materialization) is content-starved until
increment A lands.
Topics: codexfactory, domain-hermes, plane-1, roster, policies, review-councils,
agent-mixes, escalation-rules, memory-boundaries, practice-catalog,
layer-content-seeding
Repository context: codexFactory (hermes/domain/ + omnigent/domain-overlay.yaml); persona/mix/council schemas neutral in openxFactory later
Staging ID: openxFactory:staging:codexfactory-domain-hermes-content
Source: ideation/brainstorm/ — codexfactory-domain-hermes-content.md (umbrella),
codexfactory-domain-roster-draft.md, codexfactory-domain-policy-model.md,
codexfactory-domain-deliberation.md, codexfactory-domain-memory-and-practices.md,
hermes-persona-character-model.md; decisions recorded 2026-07-22.

## Outcome (recorded 2026-08-28)

COMPLETE. Both exit changes were ratified, realized and ARCHIVED, and both
archives were verified at the codexFactory tree on 2026-08-28:

| Exit | Repository | Archived packet |
| --- | --- | --- |
| Change A — roles + policies + `codex_owns` closure + Omnigent lockstep | codexFactory | `openspec/changes/archive/2026-07-22-add-domain-hermes-roles-and-policies` |
| Change B — councils, mixes, escalation, memory, catalog | codexFactory | `openspec/changes/archive/2026-07-23-add-domain-hermes-councils-and-memory` |

The canonical codexFactory spec `domain-hermes-content` carries all nine
requirements, and the Omnigent overlay extension rode change A's
realization. The topic folder and its `openspec/` drafts are retained as
PROVENANCE — the reason this document is `superseded` rather than deleted
— and the open questions listed below were carried into those proposals
and answered there.

## Claims (decided 2026-07-22 in the brainstorm cluster)

1. **Content model settled.** Option E personas (trait vocabulary v1: 4
   disposition + 5 voice axes, 3-level scale, per-axis tunable ranges); no
   domain house style; decide-then-speak guardrail; fixed character with
   versioned re-authoring; proportional authoring ceremony
   (disposition/authority = ratified, prose/voice-defaults = Lead-accepted).
2. **Roster settled.** Seven Leads + Scrum Coordinator; scrum
   changes-vs-operates boundary; deploy execution is never a domain authority;
   two council tiers (`council_small` default, `council_large` on enumerated
   triggers); councils permanently distinct; escalation-target audit applied
   at promotion (stop overloading `gate_rules_council`).
3. **Policy model settled.** Store the delta, not the textbook; the filled
   position table is write-ready; coverage ratchet (no absolute floor);
   contested positions carry `rationale` + `review_by`; memory writes =
   worker-proposes/Lead-accepts; catalog signing proportional; de-id =
   structural schema + Lead attestation.
4. **The harvest is mapped and verified.** Every target file has named source
   artifacts (harvest map in the umbrella brainstorm); genuine voids are the
   Gate-Rules Council seat, `memory-boundaries.yaml`, and the catalog
   structure.
5. **Lockstep Omnigent obligations.** Promotion must extend
   `overlay.yaml` `codex_owns` (closure matrix shows the roster claims scope
   the overlay doesn't stake), add the two referenced-but-missing workers
   (`scrum_master_worker`, `release_note_agent`), and declare the
   bidirectional persona↔worker references the seeder consistency-checks.

## Exit path

- **Change A — `add-domain-hermes-roles-and-policies` (codexFactory):**
  `hermes/domain/roles/*.yaml` (8 personas, escalation audit applied) +
  `hermes/domain/policies/` (position table, contested-position schema) +
  `overlay.yaml` `codex_owns` extension. Draft workspace: this topic's
  `openspec/`.
- **Change B — councils, mixes, escalation, memory, catalog (codexFactory):**
  `review-councils/`, `agent-mixes.yaml` (two tiers + triggers + context
  packet), `escalation-rules.yaml`, `memory-boundaries.yaml`, practice
  catalog (`promoted_in` + `owning_lead` fields). After A.
- **Omnigent extension (codexFactory `omnigent/`):** the two missing workers +
  upward persona references. With A or B, whichever first needs it.

## Open questions (carried to the proposals)

- ~~Gate-Rules Council seats~~ — DECIDED 2026-07-22 (B-gating round): client
  seat = Company Policy Lead (CSC pulled in by the conjunction rule on
  security-touching rules); project seat = the intent-owner role-slot,
  symbolic until the project roster lands; human ack stays the final step.
- ~~`council_small` seat sourcing~~ — DECIDED 2026-07-22: drawn by trigger —
  convener + 2 from a trigger→seats table (security→LS, quality→LQ,
  architecture→LA).
- ~~`spend_over_envelope` home~~ — DECIDED 2026-07-22: domain declares only
  the trigger; the value is client-owned (FAO budget envelope); un-tuned
  client parks.
- ~~`finding_class` vocabulary~~ — DECIDED 2026-07-22: seed small in change B
  (five starter classes); Lead-accepted extensions; neutralize later.
- Efficiency-audit ownership (Scrum Coordinator vs. Lead Engineer) — from
  `cost-accountability-and-efficiency-model.md`; not B-gating (the clock-in
  duty rides the bidirectional references; ownership lands with the cost
  model).
- Neutral persona/mix/council schemas in openxFactory: with the neutral
  `hermes_domain_overlay` schema (materialization topic) or a later change.

## Readiness

**Change A COMPLETE** — ratified + archived 2026-07-22
(`archive/2026-07-22-add-domain-hermes-roles-and-policies`; canonical spec
`domain-hermes-content`). **Change B author-ready** — all four gating
decisions made (above); drafted in `openspec/` here (proposal-b + tasks-b);
sole remaining gate: the `add-omnigent-domain-overlay` codexFactory
realization (ratified 2026-07-22), since B's `escalation-rules.yaml`
elevates from the overlay that change restructures — author B against the
archetype-shaped overlay once it lands.
