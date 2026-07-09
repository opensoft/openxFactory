# Design: Promote Workflow Gate Contract

## Decision 1: One change for two candidates

DTN-001 and DTN-002 promote together: gate records exist only inside
workflow contracts, every consumer overlaps, and a gate vocabulary without
its host schema would be unenforceable. The register keeps both entries;
both track this change.

## Decision 2: Admit both blocking styles, don't migrate

The evidence shows two live idioms — declarative `blocks_on_failure` and
conditional `blocks_when[]`. Forcing either onto the other would fail the
neutrality test (origin domains must consume with zero content change).
The schema requires at least one; convergence, if ever desired, becomes a
later delta with data from the health reports.

## Decision 3: Envelope repair is adoption work, not schema laxity

codexFactory's missing `schema_version`/`kind` is drift, not a style. The
schema requires the envelope; the fix lands as codexFactory's adoption task
rather than weakening the contract to match the drift.

## Decision 4: Warnings for unknown owner layers, errors for structure

Structural violations (missing envelope, no blocking declaration) are
errors; unknown `owner_layer` values are warnings because intermediate
layers with `role: extension` are legal in stacks and naming conventions
still vary. The doc-health run surfaces warning trends before any
tightening delta.

## Decision 5: Archive on artifact landing; adoption tracked by register

Schema + validator + docs are this change's artifacts. Domain adoption
(cross-repo re-validation, provenance declarations) gates the register's
`adopted` status, not this change's archival — exactly the mid-promotion
authority rule ratified by refine-promotion-provenance. The health checker's
register-consistency family watches the tail.
