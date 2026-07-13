# Document-Cataloging Examples

Status: draft

Reference examples for the six `document-cataloging` contract schemas under
`contracts/schemas/` (`add-document-cataloging` change, task 2.2). These are
static reference material, not runtime state — see `../README.md` for the
placement policy this directory follows.

## Layout

```text
document-cataloging/
├── README.md                                          # this index
├── document-catalog-snapshot-complete.example.yaml     # complete snapshot
├── document-catalog-snapshot-deletion-before.example.yaml  # deletion (pair, 1/2)
├── document-catalog-snapshot-deletion-after.example.yaml   # deletion (pair, 2/2)
├── document-catalog-protected-evidence.example.yaml     # protected evidence + opaque locator
├── document-catalog-pending-transitions.example.yaml    # pending-state transitions
├── cataloger-recommendation-suggested.example.yaml       # suggested classification
├── document-tag-registry.example.yaml
├── document-tag-overrides.example.yaml                   # owner override
├── document-opaque-locator.example.yaml                  # reusable locator fragments (both variants)
├── document-handling-gate.example.yaml                   # reusable dispatch-decision fragments (both variants)
└── negative/                                              # one violation per file
    ├── snapshot-ambiguous-locator.yaml
    ├── snapshot-bad-facet-value.yaml
    ├── snapshot-reviewed-without-review-block.yaml
    ├── snapshot-suggested-missing-provenance.yaml
    ├── recommendation-not-suggested.yaml
    ├── tag-registry-bad-status.yaml
    ├── tag-overrides-missing-values.yaml
    ├── opaque-locator-both-present.yaml
    ├── opaque-locator-neither.yaml
    ├── handling-gate-blocked-missing-reference.yaml
    └── handling-gate-allowed-missing-attestation.yaml
```

## Schema → example map

| Schema | Valid example(s) | Negative example(s) |
| --- | --- | --- |
| `xfactory-document-catalog-snapshot.schema.yaml` | `document-catalog-snapshot-complete`, `-deletion-before`, `-deletion-after`, `-protected-evidence`, `-pending-transitions` | `snapshot-ambiguous-locator`, `snapshot-bad-facet-value`, `snapshot-reviewed-without-review-block`, `snapshot-suggested-missing-provenance` |
| `xfactory-document-cataloger-recommendation.schema.yaml` | `cataloger-recommendation-suggested` | `recommendation-not-suggested` |
| `xfactory-document-tag-registry.schema.yaml` | `document-tag-registry` | `tag-registry-bad-status` |
| `xfactory-document-tag-overrides.schema.yaml` | `document-tag-overrides` | `tag-overrides-missing-values` |
| `xfactory-document-opaque-locator.schema.yaml` (`#/$defs/document_locator`) | `document-opaque-locator` (`locators[]`, both variants) | `opaque-locator-both-present`, `opaque-locator-neither` |
| `xfactory-document-handling-gate.schema.yaml` (`#/$defs/dispatch_decision`) | `document-handling-gate` (`decisions[]`, both variants) | `handling-gate-blocked-missing-reference`, `handling-gate-allowed-missing-attestation` |

## Fragment-only files

`document-opaque-locator.example.yaml` and `document-handling-gate.example.yaml`
wrap their example values under a plain `locators:`/`decisions:` list key —
that wrapper key is a container for this file only, not part of either
schema. Both underlying schemas are pure `$defs` kernels (mirroring
`contracts/avatar-client/shared-definitions.schema.yaml`): they are always
consumed by `$ref` from an entry's locator fields or `dispatch_policy`, never
validated as a whole top-level document, so they carry no `schema_version`/
`kind` envelope of their own. Every other example file here **is** a
top-level record and does carry that envelope.

## Deletion pair

`document-catalog-snapshot-deletion-before.example.yaml` and
`-deletion-after.example.yaml` are two independently valid snapshots for the
same repository. The "after" snapshot demonstrates deletion structurally: it
simply has no entry for `docs/legacy-runbook.md`, which the "before" snapshot
carried. There is no tombstone field — a later run's snapshot omitting a
locator key already lands as required.

## Cross-schema consistency

`document-catalog-protected-evidence.example.yaml`'s entry and
`document-opaque-locator.example.yaml`'s second locator describe the same
document (`xFactories/MedxFactory`, `docs/patient-consent-protocol.md`) with
matching `document_ref`/`path_sha256`, so the opaque-locator kernel's shape
can be checked once in isolation and once embedded in a full snapshot.
Likewise, `document-tag-overrides.example.yaml`'s first override and
`document-catalog-snapshot-complete.example.yaml`'s `document_role`
disposition share the same document, content hash, and evidence reference.

## Validating locally

These examples were checked with `jsonschema`'s `Draft202012Validator` plus
`referencing.Registry` for cross-file `$ref` resolution (the same approach
`scripts/validate-avatar-client.py` uses for the avatar-client kernel). No
committed validator ships in this change slice — deterministic validation
(coverage, freshness, taxonomy resolution, override standing) is change task
2.3.
