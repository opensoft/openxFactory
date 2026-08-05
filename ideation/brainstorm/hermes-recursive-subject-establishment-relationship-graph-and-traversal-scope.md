# Subject Relationship Graph and Traversal Scope — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive establishment should build a subject-scoped relationship graph with quarantined identity matches and purpose-bound traversal limits instead of expanding into unbounded counterparty or provider dossiers.
Topics: hermes-recursive-subject-establishment, relationship-graph, entity-resolution, traversal-scope, subject-isolation
Repository context: openxFactory neutral subject graph with Ledgerx counterparty and Medx provider-network specializations
Captured: 2026-07-30

## Possible feats

- **Subject relationship graph** — connect the subject to organizations,
  people, accounts, encounters, agreements, locations, and sources with
  temporal and provenance-bearing edges.
- **Relationship traversal policy** — bound recursive expansion by purpose,
  materiality, relationship type, sensitivity, and maximum depth.

## Focus

Company and patient establishment are both graph problems. A company is
understood partly through vendors, customers, owners, banks, accounts, and
agreements. A patient is understood partly through providers, clinics,
insurers, pharmacies, encounters, referrals, and studies.

The same graph traversal that finds missing evidence can also cause scope
explosion, false identity joins, or cross-subject leakage.

## Proposed model

Relationship nodes may include:

```text
subject
person or organization
location
account or policy
contract or encounter
document, message, transaction, study, or claim source
```

Edges carry:

- relationship type and direction;
- subject-relative purpose;
- effective period and observation period;
- source-claim and evidence refs;
- identity confidence and resolution state;
- authority and visibility;
- materiality or clinical relevance;
- review and supersession state.

Uncertain entity matches enter an identity quarantine:

```text
candidate identity
  -> anchors compared
  -> conflicting identifiers preserved
  -> authorized review
  -> linked | rejected | remains ambiguous
```

No claim attaches to a resolved subject, provider, or counterparty solely
because a name resembles one already in the graph.

The default traversal policy should remain one relationship hop from the
subject. Deeper traversal requires a material, authorized question. A company
vendor's supplier or a physician's unrelated patients are outside scope merely
because they are discoverable.

## Interfaces and boundaries

The graph is subject-scoped. A counterparty or provider representation explains
its relationship to this subject; it does not establish a globally shared
profile.

If the same real-world entity is independently served as another xFactory
subject, that subject receives a separate runtime and evidence boundary.
Cross-subject correlation requires an exact governed binding and must not
silently merge memory.

The graph emits source leads and model context but cannot grant access to a
related party's systems or infer consent from the relationship.

## Alternatives and tensions

- Global entity resolution reduces duplicate work but creates a high-risk
  cross-tenant and cross-subject correlation surface.
- Fully isolated entity records protect scope but make corrections and
  sanctions or registry updates harder to reuse.
- Pseudonymous global identity hints could support matching without sharing
  claims, but the privacy and error consequences need explicit design.

## Open questions

- Which identity anchors are safe to compare across subjects?
- When does a counterparty representation become a governed derived model?
- How are household, caregiver, beneficial-owner, and affiliated-entity
  relationships represented without overexposure?
- Which domain-defined materiality tests permit a second traversal hop?

## Relationships

The graph is expanded by the [recursive evidence frontier](hermes-recursive-subject-establishment-recursive-evidence-frontier.md),
grounded through [claim lineage and reconciliation](hermes-recursive-subject-establishment-claim-lineage-and-reconciliation.md),
and supplies [subject-model assembly](hermes-recursive-subject-establishment-subject-model-assembly-and-admission.md).

