# Staged: Tier-2 Council-Clearance Pattern — a reusable per-repo gate rule beyond the doc-health sweep

Status: staged
Kind: staging-fragment
Summary: Generalize the ratified nightly-sweep tier-2 council-clearance rule (codexFactory `add-nightly-sweep-council-clearance`) into a neutral, instantiable per-repo gate-rule pattern — template, council exercise, activation gate, and anti-normalization rule — so the next autonomous sweep or repo instantiates the pattern through its own Gate-Rules Council exercise instead of re-deriving a one-off carve-out.
Topics: gate-rules-council, merge-readiness-council, autonomous-approval, auto-clear-envelope, tier-2, merge-master, doc-health-sweep, activation-gate, codexfactory
Repository context: openxFactory (the neutral pattern template); codexFactory (first instantiation, ratified + implemented 2026-07-23); the second consumer instantiates from the template
Captured: 2026-08-05
Staging ID: `openxFactory:staging:tier2-council-clearance-pattern`
Source possible: `pos-derived-reusable-tier-2-council-clearance-pattern-beyond` (accepted by Brett 2026-07-23; promoted to staging by Brett 2026-08-05, gate record `ideation/dashboard/gate-records/pos-derived-reusable-tier-2-council-clearance-pattern-beyond/promote-to-staging-20260805T024711Z.gate-action.yaml`)

## Target capability

ADDED — a neutral openxFactory pattern contract (working name
`council-clearance-gate-rule`): the template a repo instantiates when it wants
a tier-2 council-clearance path on an autonomous-approval envelope. The
first instantiation already exists and stays untouched — codexFactory's
nightly doc-health rolling PR rule, ratified as amended by the Gate-Rules
Council 2026-07-23 and implemented as rule YAML + `council_clearance.py`
composing tier 1 with `envelope.py` untouched. The pattern extraction is
additive: no change to `workflow-gate-contract`, no change to the ratified
codexFactory rule.

## Claims

1. The tier-2 shape is repo-agnostic. Every element of the ratified rule
   generalizes cleanly: a conjunctive tier-1 envelope; a declared
   *council-clearable* condition set; a convened council whose unanimous
   `ready` verdict is pinned to the exact head SHA; a never-clearable floor
   (security-touching failures, check failures, identity mismatches always
   park for the human); an anti-normalization rule (a condition cleared
   repeatedly stops being clearable and parks with a fix-the-generator flag);
   and a `configured_but_inactive` activation gate until council
   orchestration exists in the executing lane.
2. Ratifying a clearable set IS a per-repo gate rule, so each instantiation
   is a Gate-Rules Council exercise, not a code drop. The codexFactory
   rehearsal (recorded at
   `hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`)
   is the worked example the template cites: seat verifications, an LQ
   amendment narrowing the docs-class allowlist, and the authority
   acknowledgement are the moves every future instantiation repeats with its
   own nouns.
3. Rules-as-code with owned allowlists survives generalization. The
   first exercise decided the clearable-set boundary must be a static,
   owner-attributed allowlist (Lead Quality owned the docs-class list) —
   deterministic, auditable, amendable only by recorded events. The template
   carries that as a structural requirement, not a codex convention.
4. The pattern must ship dormant. `configured_but_inactive` behind an
   activation gate was not incidental: a clearance path with no orchestrated
   council is a bypass. The template makes the activation gate a required
   element of any instantiation.

## Open questions — resolved for staging (2026-08-05)

- When does the template get extracted? DECIDED at accept (Brett,
  2026-07-23): rule-of-three discipline — the neutral contract is authored
  when a second sweep or repo wants a tier-2 rule, not before. Staging this
  fragment organizes the pattern's content; the exit below carries the
  trigger.
- Who owns a clearable-set allowlist in the neutral shape? DECIDED by the
  first exercise (Q1, 2026-07-23): a static allowlist with a named owning
  seat; changes are owner-accepted recorded events.
- How wide is a v1 clearable set? DECIDED by the first exercise (Q4,
  2026-07-23): start with the single lowest-risk condition class
  (codexFactory: docs-only overflow alone); widening is a normal rule
  amendment through the same council.

## Exit path

One OpenSpec change (working name `add-council-clearance-rule-template`)
authoring the neutral pattern contract plus the instantiation checklist,
citing the codexFactory rule as the conforming first instance. The exit is
gated on the rule-of-three trigger: a SECOND consumer (another nightly lane,
another repo's rolling PR, or a DomainxFactory sweep) names itself and wants
a tier-2 rule. Until that trigger fires, this fragment holds the organized
pattern so the second consumer starts from a template, not from archaeology
of the codexFactory carve-out.
