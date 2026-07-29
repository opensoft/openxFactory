# Synthesis: codexFactory Domain Authority and Deliberation — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The codexFactory roster, domain content map, and deliberation
profiles combine into a Plane-1 authority system that directs workers without
collapsing review councils into execution agents.
Topics: codexfactory-domain, codexfactory, domain-hermes, authority-personas, synthesis
Repository context: openxFactory exploration for codexFactory Domain Hermes
Captured: 2026-07-28

## Possible feats

- **codexFactory authority graph** — validate personas, owned decisions,
  directed workers, escalation targets, and council participation.
- **Deliberation-profile registry** — pin agent mixes, stop conditions, and
  synthesis rules by review purpose.

## Members and their joints

Atomic members:
[Domain Hermes Content](codexfactory-domain-hermes-content.md),
[Domain Roster](codexfactory-domain-roster-draft.md),
and [Domain Deliberation](codexfactory-domain-deliberation.md).

### Personas carry decision authority

The content map establishes which software-engineering decisions belong in
the domain layer. The roster names the deciders and coordinators that own
those decisions, while keeping coding and review workers in Plane 2.

### Deliberation is a governed method

Deliberation profiles define which perspectives convene, what evidence they
consume, when they stop, and how disagreement is synthesized. A council
verdict remains distinct from the artifacts produced by workers.

## Emergent behavior

The domain can issue explainable recommendations and verdicts whose authority,
participants, evidence, and escalation path are all inspectable.

## Tensions to hold

- Rich personas improve consistency but must not turn character into policy.
- Reusable agent mixes reduce setup cost while each decision still needs
  scope-appropriate evidence.
- A Merge Master operator cannot approve outside a separately granted
  envelope.

## Recombination opportunities

The authority graph combines with the
[policy and memory synthesis](codexfactory-domain-synthesis-policy-and-memory.md)
and the [worker execution packet](worker-execution-overview.md).

## Open questions

- Which councils require unanimous versus synthesized verdicts?
- How are persona and deliberation revisions pinned to a decision record?
- Which roles are neutral archetypes versus codexFactory-specific?
