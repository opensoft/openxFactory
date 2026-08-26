# Subject-Model Assembly and Admission — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Hermes should assemble purpose-specific subject views from a shared evidence graph while keeping inferred models non-authoritative and admitting durable current state or memory only through existing Subject Hermes gates.
Topics: hermes-recursive-subject-establishment, subject-model-assembly, governed-derived-model, current-state-snapshot, memory-gateway
Repository context: openxFactory neutral Subject Hermes epistemic model and admission boundary
Captured: 2026-07-30

## Possible feats

- **Derived subject-model candidate** — create an immutable,
  provenance-complete, non-authoritative model for one subject and purpose.
- **Subject-model admission decision** — record which claims or projections
  may update evidence, timeline, current state, memory, or follow-up objects.

## Focus

"Build a model of the subject" can accidentally imply one authoritative,
all-purpose dossier. The safer and more useful shape is a shared evidence
graph plus purpose-bound projections with different authority and lifecycle.

## Proposed model

The epistemic stack is:

| Layer | Contents | Recursive inference authority |
| --- | --- | --- |
| Identity and consent anchors | verified subject identity, declarations, grants, delegates | may inspect under policy; cannot invent or silently change |
| Source claims | small, cited observations and statements | may propose with extraction evidence |
| Evidence and relationship graphs | support, conflict, supersession, entities, events, sources | may construct candidate relations |
| Governed derived subject model | patterns, hypotheses, inferred relationships, risks, needs | permanently non-authoritative |
| Purpose-bound current state | what Hermes presently accepts for a declared workflow | admitted through policy and review |
| Durable memory and follow-up | reusable subject knowledge and obligations | written only through the memory gateway |

One subject can have several projections:

```text
company legal-entity view
company accounting-readiness view
vendor-relationship view
patient longitudinal-care view
patient medication-reconciliation view
patient imaging-history view
```

Each projection declares purpose, source snapshot, included facets, freshness,
uncertainty, open questions, and permitted consumers. It references rather than
flattens contradictory evidence.

The governed-derived-model invariants remain load-bearing: immutable
`non_authoritative` status, full provenance, read-only truth-store access, zero
action authority, subject isolation, and human-gated promotion into a
different object kind.

## Interfaces and boundaries

The model assembler consumes accepted source claims, evidence relations,
domain semantics, and authorized context. It emits a candidate model and
admission packet, not a chart, ledger, diagnosis, contract interpretation, or
external action.

Subject Hermes decides which candidate outputs become evidence graph edges,
timeline events, current-state items, memory candidates, or follow-up
obligations. Domain and accountable-human review remain required where the
subject matter demands it.

Subject-scoped learning never becomes tenant or domain learning merely because
many establishment episodes exhibit the same pattern. Promotion uses existing
consent, de-identification, review, and provenance gates.

## Alternatives and tensions

- One canonical subject model simplifies retrieval but creates purpose creep,
  overcollection, and stale-field ambiguity.
- Many independent projections minimize scope but may produce inconsistent
  views and duplicate computation.
- A shared evidence graph with versioned projections provides a middle path,
  provided cross-projection disagreement remains visible.

## Open questions

- Is every projection a governed-derived-model family or only those containing
  inference?
- Which admitted current-state fields may be generated automatically from
  high-authority deterministic sources?
- How does the subject inspect or contest an inference without seeing
  restricted third-party information?
- What triggers full rebuild versus incremental projection refresh?

## Relationships

Assembly consumes [claim lineage and reconciliation](hermes-recursive-subject-establishment-claim-lineage-and-reconciliation.md)
and the [subject relationship graph](hermes-recursive-subject-establishment-relationship-graph-and-traversal-scope.md),
obeys [authority, consent, and subject rights](hermes-recursive-subject-establishment-authority-consent-and-subject-rights.md),
and supplies [coverage and readiness](hermes-recursive-subject-establishment-coverage-gaps-and-readiness.md).
The canonical invariant source is the
[Governed Derived Model](../../docs/governed-derived-model.md).

