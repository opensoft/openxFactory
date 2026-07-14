# Ideation-Routing Examples

Status: draft

Reference examples for the four `ideation-routing` contract schemas under
`contracts/schemas/` (`add-cross-factory-ideation-routing` change, task 2.2).
These are static reference material, not runtime state — see `../README.md` for
the placement policy this directory follows. No committed validator ships in
this change slice; strict openxFactory validation (central ID allocation,
unique definitions, paired documents, legal transitions, accepted destinations,
structured-reference resolution, prospective legacy compatibility) is change
task 2.3, and the fourteenth deterministic doc-health family is codexFactory
task 4.x. These examples are the GATES self-test surface: every `*.example.yaml`
must validate against the schema its `kind` (or documented fragment `$def`)
names, and every file under `negative/` must fail for its single documented
reason.

## Layout

```text
ideation-routing/
├── README.md                                              # this index
├── routing-record-unknown-owner-intake.example.yaml        # intake; pending_capture source; unresolved+blocker
├── routing-record-domain-origin-expansion.example.yaml     # cross_domain hub over a retained domain source
├── routing-record-multi-source.example.yaml                # 2 sources + dedup; neutral/domain/installer/aggregation split
├── routing-record-destination-acceptance.example.yaml      # fully routed; acceptance blocks; deferred claim
├── routing-index.example.yaml                              # populated central allocation ledger
├── repository-reference.example.yaml                       # committed_reference fragments (SHA-1 and SHA-256)
├── proposal-provenance.example.yaml                        # ideation_provenance_entry fragments
├── organizer-recommendations.example.yaml                  # non-mutating organizer run; confidence 0..1; pending_review
└── negative/                                               # one documented violation per file
    ├── routing-record-intake-pending-capture-misuse.yaml    # pending_capture at non-intake status
    ├── routing-record-source-path-traversal.yaml            # ".." traversal in a structured reference path
    ├── routing-record-multi-source-missing-dedup.yaml       # 2 sources, deduplication_rationale null
    ├── routing-record-unresolved-missing-blocker.yaml       # unresolved claim, blocker null
    ├── routing-record-routed-without-acceptance.yaml         # routed claim, acceptance null
    ├── proposal-provenance-pending-capture.yaml              # proposal provenance pinned to pending_capture
    ├── organizer-confidence-out-of-range.yaml               # confidence 1.4 (outside 0..1)
    └── organizer-mutation-request.yaml                       # recommendation carries a mutation verb
```

## Schema → example map

| Schema | Valid example(s) | Negative example(s) |
| --- | --- | --- |
| `xfactory-idea-routing-record.schema.yaml` (`kind: xfactory_idea_routing_record`) | `routing-record-unknown-owner-intake`, `routing-record-domain-origin-expansion`, `routing-record-multi-source`, `routing-record-destination-acceptance` | `routing-record-intake-pending-capture-misuse`, `routing-record-source-path-traversal`, `routing-record-multi-source-missing-dedup`, `routing-record-unresolved-missing-blocker`, `routing-record-routed-without-acceptance` |
| `xfactory-ideation-routing-index.schema.yaml` (`kind: xfactory_ideation_routing_index`) | `routing-index` | — |
| `xfactory-ideation-organizer-recommendations.schema.yaml` (`kind: ideation_organizer_recommendations`) | `organizer-recommendations` | `organizer-confidence-out-of-range`, `organizer-mutation-request` |
| `xfactory-idea-routing-reference.schema.yaml` (`#/$defs/committed_reference`) | `repository-reference` (`references[]`) | — |
| `xfactory-idea-routing-reference.schema.yaml` (`#/$defs/ideation_provenance_entry`) | `proposal-provenance` (`ideation_provenance[]`) | `proposal-provenance-pending-capture` |

## Task-2.2 scenario coverage

Each of the six required scenarios has a valid and an invalid example; the
`source_reference` and `path_reference` kernel `$defs` are exercised
transitively by the record and index examples (as the catalog examples exercise
the opaque-locator kernel both standalone and embedded).

| Scenario | Valid | Invalid (single documented defect) |
| --- | --- | --- |
| Unknown-owner intake | `routing-record-unknown-owner-intake` | `routing-record-intake-pending-capture-misuse` (pending_capture after intake) |
| Domain-origin expansion | `routing-record-domain-origin-expansion` | `routing-record-source-path-traversal` (escaping source path) |
| Multi-source routing | `routing-record-multi-source` | `routing-record-multi-source-missing-dedup` (no dedup rationale) |
| Unresolved blockers | `routing-record-unknown-owner-intake` (C01), `routing-record-multi-source` (C02/C03) | `routing-record-unresolved-missing-blocker` (blocker null) |
| Destination acceptance | `routing-record-destination-acceptance` | `routing-record-routed-without-acceptance` (acceptance null) |
| Routed proposal provenance | `proposal-provenance` | `proposal-provenance-pending-capture` (pending_capture revision) |

## Fragment-only files

`repository-reference.example.yaml` and `proposal-provenance.example.yaml` wrap
their values under a plain `references:` / `ideation_provenance:` list key — that
wrapper is a container for those files only, not part of any schema.
`xfactory-idea-routing-reference.schema.yaml` is a pure `$defs` kernel (mirroring
`xfactory-document-opaque-locator.schema.yaml`): it is always consumed by `$ref`
from the record/index/organizer schemas and the Markdown `Routing records:`
provenance header, never validated as a whole top-level document, so it carries
no `schema_version`/`kind` envelope. `negative/proposal-provenance-pending-capture.yaml`
is an unwrapped single `ideation_provenance_entry` instance (no envelope), like
the catalog family's `negative/opaque-locator-*.yaml` fragments. Every other
file here **is** a top-level record and carries the `schema_version`/`kind`
envelope.

## `Routing records:` header note

The `committed_reference` object exercised by `repository-reference.example.yaml`
is exactly the object a Markdown destination serializes (as a compact JSON array
element) into its `Routing records:` provenance header (spec "Organize gate and
lightweight destination provenance"). The routing capability introduces no
separate string-reference grammar for that header.

## Validating locally

These examples were checked with `jsonschema`'s `Draft202012Validator` plus
`referencing.Registry` for cross-file `$ref` resolution (the same approach
`scripts/validate-document-catalog.py` and `scripts/validate-avatar-client.py`
use). Repository-ID gitlink resolution, revision-belongs-to-repository, unique
Idea/Claim IDs, paired-document identity, append-only transition history, and
aging are deterministic-validator concerns (task 2.3), not shapes these schemas
or examples assert.
