# Staged: codexFactory Domain Hermes Content (roles, policies, councils, memory, catalog)

Status: staged
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

- Gate-Rules Council: exact client/project seat definitions.
- `council_small` seat sourcing (fixed per persona vs. drawn by trigger kind).
- Efficiency-audit ownership (Scrum Coordinator vs. Lead Engineer) — from
  `cost-accountability-and-efficiency-model.md`; the clock-in duty rides the
  bidirectional references.
- Neutral persona/mix/council schemas in openxFactory: with the neutral
  `hermes_domain_overlay` schema (materialization topic) or a later change?
- Controlled `finding_class` vocabulary for de-identified domain learning.

## Readiness

Ready to propose — decisions settled 2026-07-22; sources verified against the
codexFactory tree; change A is drafted in `openspec/` here.
