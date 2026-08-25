# Synthesis: Client Authority and Policy Tuning — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The client scaffold, house-team roster, stored content, policy
wizard, and assurance bench combine into a conservative tenant-governance
layer whose authority remains human-set.
Topics: client, client-hermes, company-policy, authority-personas, synthesis
Repository context: openxFactory neutral Client Hermes layer exploration
Captured: 2026-07-28

## Possible feats

- **Client-layer tuning flow** — scaffold a tenant, elicit bounded decisions,
  validate stricter-only policy, and publish a reviewable client overlay.
- **Client authority coverage check** — prove that stored policy and release
  risks have a named decider, escalation target, and fail-closed default.

## Members and their joints

Atomic members:
[Client Layer Scaffold](client-layer-scaffold.md),
[Client Layer Roster](client-layer-roster-draft.md),
[Client Layer Content](client-layer-content-draft.md),
[Client Policy Wizard](client-policy-wizard.md),
and [Client Risk and Assurance Model](client-risk-and-assurance-model.md).

### Scaffold and roster define who may decide

The scaffold establishes the client layer's object and plane boundaries. The
roster assigns tenant policy, operational, security, communication, and risk
perspectives without transferring domain or project authority into the
company layer.

### The wizard materializes human decisions

The wizard turns bounded answers into policy, memory, integration, and
auto-clearance records. It proposes conservative defaults and parks unknown
answers; it does not invent company policy.

### Assurance constrains tuning

Legal, reputation, and liability concerns shape the questions, validation,
and escalation paths. A tuned overlay may become stricter than domain
defaults but cannot quietly weaken non-overridable protections.

## Emergent behavior

Together the atomics describe a repeatable client-onboarding and retuning
process that produces inspectable authority and policy artifacts rather than
an opaque prompt.

## Tensions to hold

- A short wizard improves adoption but risks hiding consequential defaults.
- A coherent house voice helps operators while distinct roles need visible
  disagreement.
- Stricter-only inheritance needs an explicit model for rare justified
  project exceptions.

## Recombination opportunities

The tuned layer can feed the
[Hermes layer-runtime packet](hermes-overview.md) and the
[practice-adoption packet](practice-adoption-overview.md).

## Open questions

- Which client decisions require multi-role concurrence?
- How are retuning changes diffed, consented, and rolled back?
- Which policy values are non-overridable versus client-selectable?
