# Recursive Evidence Frontier — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Subject establishment should advance through a typed frontier of unresolved facets, relationships, time intervals, contradictions, and missing sources rather than recursively partitioning files alone.
Topics: hermes-recursive-subject-establishment, recursive-evidence-frontier, subject-establishment, evidence-discovery, rlm
Repository context: openxFactory neutral recursive planning over subject-scoped evidence
Captured: 2026-07-30

## Possible feats

- **Typed frontier item** — represent the next bounded subject question with
  scope, discovery basis, materiality, authorization, expected evidence, and
  completion criteria.
- **Frontier scheduler** — prioritize items by risk, value of information,
  blocking status, cost, and expected evidence yield.

## Focus

The original RLM pattern recursively selects and analyzes portions of a large
externalized context. Subject establishment needs a broader recursion: the
partial model itself reveals new entities, missing periods, uncollected
records, and contradictions. The corpus is being discovered while it is being
understood.

## Proposed model

A frontier item can represent:

```text
subject facet       ownership, medications, accounting policy
relationship        vendor account, treating clinic, insurer
time interval       missing fiscal quarter, undocumented care period
source family       mailbox, ledger, EHR, imaging archive
contradiction       two payment terms, conflicting pathology labels
missing artifact    contract amendment, CT study, discharge packet
review question     professional interpretation or identity match
```

Each bounded Hermes pass:

1. selects one or more authorized frontier items;
2. inspects available evidence programmatically;
3. asks bounded child questions or delegates typed work;
4. emits claims, relationships, source leads, or review findings;
5. marks the item resolved, narrowed, blocked, or still open;
6. enqueues only justified descendant items.

A descendant must cite its discovery basis and stay within the episode's
purpose, relationship depth, sensitivity, and spend limits. Recursion can
increase knowledge, not authority.

## Interfaces and boundaries

The frontier consumes subject-model gaps, coverage requirements, source
manifests, and contradictions. It emits work selection, not source access.
Actual reads and actions still require governed bindings.

The frontier is distinct from:

- an evidence-estate manifest, which records what exists or is known;
- an acquisition ledger, which tracks attempts to obtain missing evidence;
- a task queue, which records executable work;
- a subject model, which records claims and relationships.

It links these surfaces without collapsing them.

## Alternatives and tensions

- A static intake checklist is predictable and easy to audit but cannot follow
  evidence into unknown providers, counterparties, amendments, or prior
  studies.
- A free-form agent plan is adaptive but difficult to bound and replay.
- A typed frontier constrains recursion, but too rigid a vocabulary could lose
  the exploratory advantage of RLMs.

The frontier should support domain-defined item kinds within neutral identity,
authority, lineage, state, and stop envelopes.

## Open questions

- Which priority function balances materiality, risk, information gain, cost,
  and subject burden?
- Can multiple frontier items be processed in parallel without corrupting
  shared coverage state?
- What descendant-expansion limits apply by domain and subject kind?
- How is a frontier item crystallized into a deterministic recurring intake
  step after repeated stable episodes?

## Relationships

The frontier reads the [evidence-estate manifest](hermes-recursive-subject-establishment-evidence-estate-manifest.md),
creates [source leads and acquisition obligations](hermes-recursive-subject-establishment-source-leads-and-acquisition-obligations.md),
traverses the [subject relationship graph](hermes-recursive-subject-establishment-relationship-graph-and-traversal-scope.md),
and is closed by [coverage and readiness](hermes-recursive-subject-establishment-coverage-gaps-and-readiness.md).

