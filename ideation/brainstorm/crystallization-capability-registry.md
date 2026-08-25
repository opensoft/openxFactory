# The Crystallized-Capability Registry — Brainstorm

Status: staged
Kind: architecture
Summary: The registry is the packet's data spine — a governed contract
artifact (YAML with `schema_version` + `kind`, git as source of truth,
runtime lookup index derived from it) holding one record per capability:
identity, family refs, fence ref, rung, version + artifact digest,
provenance manifest, permission binding, consent scope, measured cost
profile, health snapshot, and a status spine
(candidate → building → shadow → canary → active → degraded → retired) that
deliberately mirrors the document lifecycle; dispatch reads only this,
installs consume it digest-pinned, and records reference evidence by digest
without ever embedding episode payloads.
Topics: crystallization, capability-registry, register, contract,
digest-pinning, status-lifecycle, dispatch, governed-derived-model
Repository context: openxFactory (neutral registry schema; per-domain
registries as content)
Captured: 2026-07-28
Organized: 2026-07-29 into the
[recurrence-crystallization staged topic](../staging/recurrence-crystallization/recurrence-crystallization.md)
(staged); kept as design history.

## Possible feats

- **`crystallized_capability` record schema** — the neutral record shape
  with authority-scoped field ownership.
- **Registry status spine** — controlled vocabulary aligned to the document
  lifecycle's promotion instincts.
- **Derived dispatch index** — hot-path lookup structure regenerated from
  the git registry (governed-derived-model discipline).
- **Digest-pinned install consumption** — installs pin the registry version
  they serve, runtime-manifest style.

## Position in the packet

The shared spine of the run/renew arc: written by the
[build pipeline](crystallization-build-pipeline.md), advanced by
[parity](crystallization-parity-and-cutover.md) gates, read by
[dispatch](crystallization-dispatch-and-fences.md) exclusively, annotated by
[capability-health](crystallization-drift-and-lifecycle.md), rolled up by
[accounting](crystallization-accounting.md).

## The record

Sketch of one entry:

```yaml
kind: crystallized_capability
schema_version: 0.1.0
capability_id: codex.submodule-pointer-sync   # example shape only
family_refs: [fam:codex:submodule-sync]        # TF register keys
rung: L3                                       # AL vocabulary
version: 4
artifact: {digest: sha256:..., packaging: playbook}
fence_ref: {digest: sha256:...}                # RQ artifact, verbatim
provenance_ref: {digest: sha256:...}           # BP manifest: spec, corpus,
                                               # episodes, builder, reviews
permission_binding_ref: ...                    # AU: ⊆ replaced config
consent_scope: {episode_use: true, automation: true, pooling: false}
cost_profile: {measured_marginal: ..., baseline_ai: ...}   # CA-maintained
health: {status: active, sentinel_epsilon: 0.05, last_proof: 2026-07-21}
status: active        # candidate|building|shadow|canary|active|degraded|retired
owner: {fitness: codexFactory, budget: tenant:opensoft}
dry_run: supported
```

Field ownership is an authority matrix: build writes identity/artifact/
provenance once; parity gates advance `status`; the steward writes `health`;
accounting writes `cost_profile`; nobody hand-edits another's fields.

## One spine, one mental model

The status vocabulary deliberately mirrors the document lifecycle spine
(brainstorm → staged → ratified → promoted ≈ candidate → building →
shadow/canary → active; superseded/retired on both sides). The team already
thinks in governed promotion pipelines — capabilities should feel like the
executable siblings of documents, not a new ontology. Same instinct as the
DTN register's compact aliases over the lifecycle spine.

## Git truth, derived speed

The registry is reviewable governance (git YAML, validated, history) AND a
hot-path lookup (dispatch runs per job). Resolve the tension the way the
repo already does — cross-reference.yaml → generated .md, runtime-manifest →
digest-pinned consumers: **git is the source of truth; the dispatch index
is a governed derived projection**, regenerated on registry change, never
hand-edited. Installs pin the registry digest they serve and re-pin
deliberately.

Privacy rule: records carry digests and refs — never episode payloads, never
corpus content. A registry leak must leak no tenant data.

## Claims

- **CR-C1** — The registry is a governed contract artifact: git-resident
  YAML with schema and validators; the runtime lookup index is a derived
  projection of it.
- **CR-C2** — Dispatch reads only the registry; a capability absent from it
  does not exist operationally (no shadow registries, no side lists).
- **CR-C3** — Records reference evidence by digest and never embed episode
  or corpus payloads.
- **CR-C4** — The status spine deliberately mirrors the document lifecycle;
  one promotion mental model governs docs and capabilities alike.
- **CR-C5** — Install consumption is digest-pinned with deliberate re-pin,
  runtime-manifest style; field writes follow a declared authority matrix.

## Open questions

- **CR-Q1** — Schema residence: neutral schema in openxFactory now, or
  domain-first in codexFactory then neutralized through the DTN process
  once a second domain conforms (the proven pattern)?
- **CR-Q2** — Registry granularity: per domain, per install, per tenant —
  and how does the platform registry for pooled capabilities
  ([cross-tenant](crystallization-cross-tenant.md)) federate with them?
- **CR-Q3** — Does `degraded` deserve to be a status, or is it health
  annotation on `active` (status = authority, health = condition)?
- **CR-Q4** — Version semantics on regeneration: same capability_id with
  version++, or new id when the fence materially changes?
- **CR-Q5** — Who validates — extend an existing `validate-*.py` or a
  dedicated registry validator with the field-authority matrix encoded?

## Related

- [Dispatch and Fences](crystallization-dispatch-and-fences.md) — the sole
  reader that matters for safety.
- [Build Pipeline](crystallization-build-pipeline.md) — the writer of
  record.
- `openspec/specs/governed-derived-model/` — the derived-projection
  discipline reused twice here (index, and the record's own provenance).
