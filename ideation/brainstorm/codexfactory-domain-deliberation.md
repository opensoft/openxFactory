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
  - id: deliberative_council
    mode: deliberative_council
    description: panelists deliberate to a single reasoned recommendation for a decider
usage:                              # which decider convenes which mix, and when
  - {persona: lead-architect, convenes: deliberative_council, when: architecture_ambiguity}
  - {persona: lead-security,  convenes: deliberative_council, when: security_ambiguity}
  - {persona: lead-quality,   convenes: deliberative_council, when: standard_contested}
  - {persona: "*",            convenes: panel_synthesis,      when: routine_review}
guardrails:
  advisory_only: true               # MoA advises; Hermes decides; openxFactory enforces
  context_via: governed_context_packet
  no_standing_credentials: true
```

Note the cost/rigor tradeoff (open question): flagship deciders convene a
`deliberative_council` only above a risk threshold, not on every call.

## Escalation rules

Elevates the `routing:` + `stop_conditions:` from `omnigent/domain-overlay.yaml`
and remaps the routing targets onto the roster personas (they currently name
undefined roles). Cross-layer targets are flagged.

```yaml
schema_version: 1
kind: hermes_domain_escalation_rules
routing:
  - {ambiguity: architecture_ambiguity, to: lead-architect}
  - {ambiguity: security_ambiguity,     to: lead-security}
  - {ambiguity: quality_ambiguity,      to: lead-quality}
  - {ambiguity: scope_ambiguity,        to: lead-engineer}
  - {ambiguity: release_ambiguity,      to: lead-release}
  - {ambiguity: process_deadlock,       to: scrum-coordinator}
  - {ambiguity: product_ambiguity,      to: product_owner, cross_layer: customer_project}  # NOT domain-owned
stop_conditions:                  # a worker halts and escalates — never proceeds past these
  - approved_scope_exceeded
  - security_finding_open
  - required_check_failed
  - credential_required_not_held
  - human_gate_reached
on_stop: park_fail_closed
```

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

- **Deliberation threshold** — the risk level above which a flagship convenes a
  `deliberative_council` vs. accepting a `panel_synthesis` verdict.
- **Panel roster governance** — the ensemble roster is config (`REVIEW_MODELS`);
  is changing it a domain-ratified event, or free operational config?
- **Gate-rules council seats** — exact client/project seat definitions, and
  whether the human step is ever escalated to approval for high-risk repos.
- **Merge-readiness vs. gate-rules overlap** — confirm the two councils never
  collapse into one in practice.
