# Document Tag Application Matrix

Status: draft
Proposed by: add-document-cataloging
Kind: architecture
Repository context: openxFactory
Target capabilities: `document-cataloging` (ADDED)

## Decision

Every governed catalog document receives an external catalog entry. Only
routed ideation receives a routing sidecar. Source Markdown is not rewritten
with inferred YAML or classification tags.

## Application Matrix

| Artifact | Catalog treatment | Source-document treatment |
|---|---|---|
| Ordinary governance Markdown | One mechanical entry plus suggested controlled tags | Existing headers only; no catalog YAML |
| Promoted OpenSpec specification | One entry with `artifact_type: promoted_spec` | No source edit |
| `Status: record` evidence | Mechanical entry plus external controlled tags | Immutable source remains unchanged |
| Known-owner domain brainstorm | Cataloged and tagged; routing signal normally `none` | No Idea ID or sidecar unless routing begins |
| Unknown, mixed, or cross-domain idea | Cataloged; tags may enqueue organizer review | One canonical routing record under the routing contract |
| Destination staged artifact | Cataloged like any other governed document | Lightweight Source Idea/Claim/routing pointers only |
| Catalog snapshot | Excluded from catalog recursion | Immutable `status: record` projection |
| Cataloger recommendation | Excluded from catalog recursion | Immutable evidence, merged only by a later main run |
| Policy-restricted document | Mechanical entry uses an allowed path or opaque locator; semantic facets may be `policy_blocked` | Content is dispatched only to an authorized host; source remains unchanged |
| Archived OpenSpec change | Excluded from the live v1 catalog corpus | Historical record remains unchanged |
| Install/runtime repository document | Outside v1 catalog corpus | May still be a resolvable routing destination |

## Metadata Boundaries

Mechanical source metadata consists of `Status`, `Kind`, `Repository context`,
source-declared handling, repository/path/revision, content hash, and artifact
type. The deterministic inventory copies these values; the classifier cannot
change them.

Semantic catalog facets are `factory_scope`, `domain_contexts`,
`capability_refs`, `topic_tags`, `document_role`, and
`sensitivity_signal`. They live only in the generated catalog and carry
per-facet confidence, evidence, effective taxonomy digest, `state_since`,
transition history, and review state.

Routing metadata consists of Idea IDs, Claim IDs, routing status, claim
disposition, owners, destinations, transitions, and acceptance. It lives only
in canonical routing records and lightweight destination pointers.

`xspec:candidate` and `xspec:supersedes` are lifecycle markers selected by a
human or gate. Neither the cataloger nor routing organizer may create them.

## Handoff Rules

- A current catalog tag may recommend ideation-organizer review.
- A stale tag whose content hash or effective taxonomy digest differs from the current
  inventory is ignored by routing.
- Several domain contexts can raise a cross-domain signal but cannot set
  routing scope or ownership.
- A suggested topic or capability cannot become effective if it is unknown to
  the controlled registry or OpenSpec capability set.
- A reviewed catalog override does not count as destination-owner acceptance.
- A routing decision may cite a catalog snapshot as supporting evidence, but
  the routing record remains the canonical routing state.

## Backfill Rule

The first catalog run creates external entries for the entire governed catalog
corpus. It does not add headers, frontmatter, Idea IDs, Claim IDs, routing
transitions, or invented historical tags to source documents. Historical
snapshots begin at the backfill date.
