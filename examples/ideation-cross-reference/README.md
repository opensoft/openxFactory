# Ideation Cross-Reference Examples

Status: draft

Reference examples for `contracts/schemas/ideation-cross-reference.schema.yaml`
(the `add-ideation-cross-reference-readiness` change, task 2.2 — the readiness
index). These are static reference material, not runtime state — see
`../README.md` for the placement policy. The index's source of truth is the
structured `ideation/cross-reference.yaml`; `ideation/cross-reference.md` is a
generated projection (worker wave).

The strict index validator is task 2.3 (`validate-ideation-cross-reference.py`,
NOT YET REALIZED — wave 2). Until it lands, these fixtures are checked at the
schema layer with `python-jsonschema` co-loading the four schemas below; the
two negatives are split into a schema-layer failure and a validator-layer
failure (noted per file).

## Four-schema co-load

Instance validation resolves cross-file `$ref`s into four schemas in one
registry (this extends review condition C3's named two — kernel + snapshot — to
four):

| Schema | Provides |
| --- | --- |
| `ideation-cross-reference.schema.yaml` | the index envelope + topic entries + scores |
| `ideation-possibles-register.schema.yaml` | `#/$defs/possibles_register` (the embedded register section) |
| `ideation-dashboard-snapshot.schema.yaml` | `generation`, `lifecycle_status`, and (via the kernel) `evidence_pin` |
| `xfactory-idea-routing-reference.schema.yaml` | structured member/score references (`repository_id`, `posix_relative_path`, `full_commit_revision`, `passage_sha256`) |

## Layout

```text
ideation-cross-reference/
├── README.md                              # this index
├── ideation-cross-reference.example.yaml  # comprehensive VALID index (see case map)
└── negative/                              # one violation per file
    ├── score-out-of-range.yaml            #   tier score 11 > 10 (SCHEMA-layer failure)
    └── archive-pointer-only-fit.yaml      #   fit note names an archive folder (VALIDATOR-layer failure)
```

## Case map (task 2.2)

The single comprehensive valid example carries one topic entry per case:

| Case | Where | Expected |
| --- | --- | --- |
| Multi-stage cluster | `cl-ideation-dashboard` (brainstorm + staged + ratified members) | valid |
| Promoted-fit citation | `cl-ideation-dashboard` (`extension_fit.promoted_spec: doc-health`) | valid |
| Gated recommendation (min >= 8) | `cl-ideation-dashboard` (tiers 9/8/9, `flagged: true`, `pending_review`) | valid |
| Spread conflict below threshold | `cl-keyword-lens` (tiers 9/8/2, `conflict_flags: tier-spread`) | valid |
| Missing tier with reason | `cl-semantic-health` (project tier `unscored_reason`) | valid |
| Explicit no-promoted-fit | `cl-semantic-health` (`has_promoted_fit: false` + statement) | valid |
| Human-seen recommendation entry | `cl-human-seen-onboarding` (`origin: human-seen` + `human_seen`) | valid |
| Embedded possibles_register section | top-level `possibles_register` (reuses the register example content) | valid |
| Score out of range | `negative/score-out-of-range.yaml` | invalid (schema layer) |
| Archive-pointer-only fit note | `negative/archive-pointer-only-fit.yaml` | invalid (validator layer, task 2.3) |

## The two negatives fail at different layers

- **`score-out-of-range.yaml`** violates `tier_assessment.score` `maximum: 10`,
  so `python-jsonschema` rejects it at the schema layer today.
- **`archive-pointer-only-fit.yaml`** is schema-VALID (a non-empty string
  satisfies `promoted_spec`). The spec's "a pointer to an archived change folder
  alone does not satisfy the citation" rule is a corpus-resolving check the
  strict index validator (task 2.3) and the doc-health readiness lane enforce —
  they resolve `promoted_spec` against the promoted spec set and emit an
  `ideation-readiness` finding. JSON Schema cannot express it, so the wave-1
  check accepts this fixture by design; it is here to pin the wave-2 validator's
  obligation.

## Evidence contract

Every tier score and the human-seen submission carry the ORGANIZER recommendation
evidence shape — `source_ref` (repository + POSIX path + FULL committed revision +
section + passage hash) + rationale + numeric confidence + `alternatives` +
`disposition: pending_review` — reused (documented structural mirror, byte-identical
pins) from `xfactory-ideation-organizer-recommendations.schema.yaml`, not the
lighter cataloger/snapshot `evidence_pin`.

## Cross-file consistency

The embedded `possibles_register` reuses `../ideation-dashboard/possibles-register.example.yaml`
verbatim; its `claiming_clusters` reference `cl-ideation-dashboard` and
`cl-keyword-lens`, both present as topic entries, and its `supporting_evidence`
pins resolve through the snapshot schema's `evidence_pin` (the four-schema
co-load).
