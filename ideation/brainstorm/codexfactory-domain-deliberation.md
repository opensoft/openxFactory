# codexFactory Domain Deliberation: agent-mixes, escalation, and review councils — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Drafts the three roster-adjacent pieces of domain stored content — how
the Plane-1 deciders *deliberate* (MoA agent-mix profiles), *escalate*
(routing + stop conditions), and *convene* (review councils). The mantra holds
throughout: Mixture of Agents advises, Hermes roles decide, openxFactory
enforces the workflow rail. The review-lane multi-model ensemble that already
exists in code becomes a declared `panel_synthesis` mix; the escalation routing
already in the Omnigent overlay is elevated and remapped onto the roster
personas; and the two councils (per-PR merge-readiness vs. cross-layer
gate-rules) are given concrete membership. Parent:
`codexfactory-domain-hermes-content.md`; roster: `codexfactory-domain-roster-draft.md`.
Topics: codexfactory, domain-hermes, agent-mixes, moa, mixture-of-agents,
escalation-rules, review-councils, gate-rules-council, merge-readiness-council,
deliberation, plane-3
Repository context: openxFactory (targets codexFactory hermes/domain/{agent-mixes,escalation-rules}.yaml + review-councils/)
Captured: 2026-07-21
Updated: 2026-07-22 (two-tier councils; enumerated triggers; roster governance; distinct-councils confirmed)

## Decided (2026-07-22)

- **Two council tiers, enumerated triggers.** `deliberative_council` splits
  into `council_small` (flagship default — a few seats, cheap) and
  `council_large` (full bench), convened by a **declared trigger list** per
  mix, not a numeric risk score (checkable, no fake precision; revisit scoring
  once council history exists to calibrate against). Mirrors the roster-draft
  decision.
- **Panel roster changes are Lead-accepted recorded events.** Changing
  `REVIEW_MODELS` is proposed by whoever, accepted by the owning persona (Lead
  Quality for the review lane), and recorded as evidence — the same weight as
  memory writes, lighter than policy ratification.
- **The two councils are permanently distinct.** Merge-readiness (per-PR,
  domain-only) never absorbs gate-rules (per-repo, cross-layer + human ack).
  Rationale, one line: **a body that sets the rules must not also apply
  them.**

## Possible feats

- **`hermes/domain/agent-mixes.yaml`** declaring the MoA profiles + persona bindings.
- **`hermes/domain/escalation-rules.yaml`** elevating routing + stop conditions.
- **`hermes/domain/review-councils/`** with the two council objects.
- **Neutral mix-profile + council schemas** in openxFactory.

## Agent-mixes (Plane 3, Hermes side)

Resolves where Plane 3 lives: the mix *profile* is declared here in the Domain
Hermes; the ensemble *execution* stays in Omnigent (`scripts/review_lane/
ensemble.py`) — the same advises/decides seam as the mantra. Three modes from
the domain-factory model:

```yaml
schema_version: 1
kind: hermes_domain_agent_mixes
mixes:
  - id: panel_synthesis            # default native mode
    mode: panel_synthesis
    default: true
    description: independent panelists; findings unioned + deduped; cross-model agreement annotated
    execution_binding: review_lane_ensemble     # omnigent scripts/review_lane/ensemble.py
    roster: config                               # via REVIEW_MODELS — roster is config, not code
  - id: scored_vote
    mode: scored_vote
    description: panelists score against a rubric; weighted/threshold vote
  - id: council_small               # flagship default — a few seats, cheap
    mode: deliberative_council
    seats: 3
    description: small bench deliberates to a single reasoned recommendation
  - id: council_large               # full bench — convened only on declared triggers
    mode: deliberative_council
    seats: full_bench
    triggers:                       # enumerated, checkable — never a computed score
      - security_ambiguity_parked   # LS has already parked; council deliberates the parked item
      - standard_contested
      - architecture_commitment     # hard-to-reverse design commitments
      - gate_weakening_change       # any change that would weaken a gate
      - spend_over_envelope         # cost-accountability hook
usage:                              # which decider convenes which mix, and when
  - {persona: lead-architect, convenes: council_small, when: architecture_ambiguity}
  - {persona: lead-architect, convenes: council_large, when: architecture_commitment}
  - {persona: lead-security,  convenes: council_large, when: security_ambiguity_parked}  # park FIRST (roster escalation audit), deliberate after
  - {persona: lead-quality,   convenes: council_large, when: standard_contested}
  - {persona: "*",            convenes: panel_synthesis, when: routine_review}
guardrails:
  advisory_only: true               # MoA advises; Hermes decides; openxFactory enforces
  context_via: governed_context_packet
  no_standing_credentials: true
  roster_change: lead_accepted_recorded   # REVIEW_MODELS change = Lead Quality accepts + evidence record
```

The cost/rigor tradeoff is now structural: small council by default,
large council only on the declared triggers (decided 2026-07-22, with the
roster draft). A council convening is itself a **spend event** — it clocks in
like any worker action (`cost-accountability-and-efficiency-model.md`), so
habitual large-council convening shows up in the efficiency audit.

### Council failure semantics (fail closed, never drift)

- **Split vote / no consensus:** the council's output is `split` and the item
  **parks for the human liaison** — the convening persona may NOT break the
  tie by fiat (that would silently turn an advisory body into a decider).
- **Missing seat:** a council convened without a required seat is REFUSED —
  it never proceeds with defaults. A gate-rules council without its client
  seat cannot set rules for that repo.
- **Advisory boundary:** a council output is always a *recommendation*; the
  convening persona's decision record must name the recommendation it
  accepted or rejected (rejecting is allowed, silently ignoring is not).

### The governed context packet (stub)

Named in the guardrails, defined nowhere — minimal fields:

```yaml
kind: governed_context_packet
scope_ref: <approved_scope_ref>          # what this deliberation is about
content_refs: [<git+repo@rev#path>...]   # pinned reference slices (never raw dumps)
memory_grants: [<gateway consent-scoped read grants>]
spend_budget: {credits: <n>, hard: true} # clock-in integration
emitted_by: <convening persona>
```

The packet is how "no standing credentials" and consent-gated memory stay true
inside an ensemble: panelists see the packet, not the world.

## Escalation rules

Elevates the `routing:` + `stop_conditions:` from `omnigent/domain-overlay.yaml`
and remaps the routing targets onto the roster personas (they currently name
undefined roles). Cross-layer targets are flagged.

```yaml
schema_version: 1
kind: hermes_domain_escalation_rules
routing:
  - {ambiguity: architecture_ambiguity,   to: lead-architect}
  - {ambiguity: security_ambiguity,       to: lead-security}
  - {ambiguity: quality_ambiguity,        to: lead-quality}
  - {ambiguity: implementation_ambiguity, to: lead-coder}       # was: lead_engineer (undefined role)
  - {ambiguity: scope_ambiguity,          to: lead-engineer}
  - {ambiguity: release_ambiguity,        to: lead-release}
  - {ambiguity: process_deadlock,         to: scrum-coordinator}
  - {ambiguity: product_ambiguity,        to: product_owner,      cross_layer: customer_project}  # NOT domain-owned
  - {ambiguity: policy_ambiguity,         to: company-policy-lead, cross_layer: client}           # governance is client/xFactory, not domain
stop_conditions:                  # a worker halts and escalates — never proceeds past these
  # elevates the omnigent overlay's six (missing_approved_scope, required_check_failed,
  # branch_review_failed, secret_detected, unapproved_scope_detected,
  # repository_policy_conflict) — same conditions, persona-era names, one addition
  - approved_scope_missing_or_exceeded   # missing_approved_scope + unapproved_scope_detected
  - security_finding_open                # secret_detected generalized
  - required_check_failed
  - branch_review_failed
  - repository_policy_conflict
  - credential_required_not_held         # new: no credential improvisation, ever
  - human_gate_reached
on_stop: park_fail_closed
```

The remap covers **all** of `omnigent/domain-overlay.yaml`'s current `routing:`
targets (which name undefined roles like `hermes_governance_owner` /
`engineering_architect`) — nothing silently dropped: `policy_ambiguity` routes
cross-layer to the client's Company Policy Lead, and `implementation_ambiguity`
lands on the Lead Coder, who bounds the coding workers.

`product_ambiguity` deliberately routes *out* of the domain to the
customer/project layer's Product Owner — the domain never answers "should we
build this?", only "how, and is it sound?".

## Review councils

Two councils, kept distinct (the content doc flagged the current docs blur them):

```yaml
schema_version: 1
kind: hermes_domain_review_councils
councils:
  - id: merge_readiness_council       # per-PR readiness review body
    scope: per_pull_request
    purpose: "is THIS change ready?"
    members: [lead-quality, lead-security, lead-integration]   # domain seats
    output: merge_readiness_packet     # ready | blocked | needs_human_review
  - id: gate_rules_council            # cross-layer rule-setting body (the user's model)
    scope: per_repository_rule_setting
    purpose: "what are the merge/gate rules for this repo?"
    members:
      domain:  [lead-architect, lead-security, lead-quality]
      client:  [company_policy_seat]
      project: [project_seat]
    human_step: acknowledgement_of_notice   # a notice to the human on the project, not a blocking approval
    output: per_repo_gate_rules              # mechanically enforced by the Merge Master operator (GitHub App)
```

The Merge Master (a mechanical GitHub-App operator, not a decider) enforces
whatever the gate-rules council + human acknowledgement produce; the
merge-readiness council is the per-PR body whose verdict the deciders act on.

## Open questions

- ~~**Deliberation threshold**~~ — DECIDED 2026-07-22: two tiers with an
  enumerated trigger list (§Decided; trigger list drafted in the mixes YAML).
  `spend_over_envelope` RESOLVED (B-gating round, 2026-07-22): the domain
  declares only the TRIGGER; the threshold value is client-owned (FAO budget
  envelope, per the facts rule); an un-tuned client parks.
- ~~**Panel roster governance**~~ — DECIDED 2026-07-22: Lead-accepted recorded
  change (§Decided).
- ~~**Gate-rules council seats**~~ — DECIDED 2026-07-22 (B-gating round):
  client seat = **Company Policy Lead** (the CSC/LS conjunction rule pulls
  the Client Security & Compliance Officer in when a rule touches security
  posture); project seat = the neutral skeleton's **intent-owner role-slot,
  symbolic** — binds to a real persona when the project roster lands; the
  human acknowledgement stays the separate final step.
- ~~**Merge-readiness vs. gate-rules overlap**~~ — CONFIRMED distinct,
  permanently (§Decided).
- ~~**Council seat sourcing**~~ — DECIDED 2026-07-22 (B-gating round):
  **drawn by trigger** — `council_small` = convener + 2 seats from a
  trigger→seats table in `agent-mixes.yaml` (security triggers always seat
  LS, quality LQ, architecture LA).
