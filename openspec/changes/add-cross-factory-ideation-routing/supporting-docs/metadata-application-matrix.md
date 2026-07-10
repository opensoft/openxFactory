# Ideation Routing Metadata Application Matrix

Status: draft
Proposed by: add-cross-factory-ideation-routing
Kind: architecture
Repository context: openxFactory
Staging ID: openxFactory:staging:ideation-routing
Target capabilities: `ideation-routing` (ADDED) and
`document-lifecycle` (MODIFIED)

## Decision

The full routing YAML record does not belong on every document. It is created
once per unclassified, mixed, or cross-domain idea and remains the canonical
source for routing state. Other documents carry only the minimum provenance
needed to resolve that record. Every governed catalog document may have an
external document-catalog entry without acquiring routing metadata or source
frontmatter.

## Application Matrix

| Artifact | Required metadata |
|---|---|
| Ordinary governance or domain document | Existing `Status`, `Kind`, and `Repository context`; external catalog entry, but no routing YAML |
| Known-owner domain brainstorm | Normal brainstorm headers; `Idea ID` optional until routing is needed |
| Clearly neutral brainstorm | Normal brainstorm headers; `Idea ID` recommended when later splitting is plausible |
| Unclassified, mixed, or cross-domain idea | One canonical `routing.yaml` plus paired `idea.md` |
| Domain-origin idea that expands across domains | Original source remains; one openxFactory routing record references it |
| Destination staged artifact | `Source Idea IDs`, selected `Claim IDs`, and routing-record references |
| OpenSpec proposal | Staging origin plus routed idea/claim provenance in proposal support manifest |
| Canonical promoted document | Proposal provenance; no live routing sidecar unless it remains an active routing hub |

## Canonical Routed-Idea Layout

```text
openxFactory/ideation/brainstorm/inbox/XFI-2026-001/
  idea.md
  routing.yaml
```

`idea.md` contains the human-readable problem, observations, questions, and
discussion. `routing.yaml` contains identity, scope, domains, claims,
dispositions, destinations, transitions, and successors.

For a domain-origin idea, the canonical brainstorm may remain in the domain:

```text
MedxFactory/ideation/brainstorm/omni-clinic-hosting.md

openxFactory/ideation/brainstorm/cross-domain/XFI-2026-001/
  routing.yaml
  routing-summary.md
```

The openxFactory record references the domain source. It does not copy the
entire domain brainstorm.

## Lightweight Destination Headers

A staged document derived from routed claims uses compact headers:

```text
Source Idea IDs: XFI-2026-001
Claim IDs: XFI-2026-001-C01, XFI-2026-001-C03
Routing records: [{"repository":"openxFactory","path":"ideation/brainstorm/cross-domain/XFI-2026-001/routing.yaml","revision":"<full commit>"}]
```

These headers are provenance pointers, not a second routing record. The staged
document may explain its local interpretation and exclusions without copying
the routing transitions or other destinations. `Routing records:` is a compact
JSON array of the same structured reference objects used in YAML contracts; it
is not a separate string-reference grammar.

## OpenSpec Provenance

At the proposal gate, the supporting-document manifest records:

```yaml
ideation_provenance:
  - idea_id: XFI-2026-001
    claim_ids:
      - XFI-2026-001-C01
    routing_record:
      repository: openxFactory
      path: ideation/brainstorm/cross-domain/XFI-2026-001/routing.yaml
      revision: <full commit>
```

This supplements, but does not replace, the proposal's staging origin.

## Creation Rules

- Do not create an empty routing sidecar “just in case” for every document.
- Create the sidecar when scope is `unclassified`, `cross_domain`, `mixed`, or
  when claim splitting/routing begins.
- A source brainstorm has at most one canonical Idea ID. A routing record may contain
  many claim IDs and destinations.
- Several source documents may contribute to one routing record only when the
  record lists every source and deduplication rationale.
- A destination document may cite several `Source Idea IDs` when it
  intentionally consolidates related routed claims; it does not use a
  misleading singular `Idea ID` header.
- Full routing YAML copied into destination documents is a drift defect.

## Validation Requirements

- every Idea ID and Claim ID is unique in the governed repository set;
- every lightweight pointer resolves to exactly one routing record;
- routing records and paired idea documents agree on Idea ID;
- routed claims resolve to a destination or explicit unresolved blocker;
- staged claim references exist in the routing record;
- proposal manifests pin the routing record revision; and
- ordinary documents are not reported merely because they lack routing
  metadata.

All routing references use canonical repository IDs, POSIX
repository-relative paths, and full committed revisions. `pending_capture` is
valid only for an intake source, never a destination or proposal provenance
record.

## Document Catalog Relationship

The external document catalog records discovery classifications for every
governed catalog document. It does not change this routing matrix:

- catalog tags never create an Idea ID, Claim ID, routing sidecar, owner, or
  destination;
- current catalog tags may enqueue an ideation-organizer recommendation;
- stale catalog entries are ignored by routing;
- a reviewed catalog override is not destination-owner acceptance; and
- ordinary documents remain valid without any routing metadata or inferred
  YAML in the source file.

See the sibling
[`add-document-cataloging`](../../add-document-cataloging/) proposal for the
catalog and controlled-tagging contracts.
