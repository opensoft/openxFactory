---
code_surface: openxFactory (`contracts/omnigent/omnigent-domain-overlay.schema.yaml` + `omnigent-install-manifest.schema.yaml` semantic blocks, `scripts/validate-omnigent-contracts.py` cross-checks + repo mode, `scripts/ontology-compile-context.py` hardening, `scripts/validate-domain-ontology.py` truncation completeness, omnigent examples/fixtures, `scripts/test-omnigent-semantic-wiring.py`); MedxFactory first-consumer adoption (two ontology profiles + overlay declarations + overlay-manifest re-pin); codexFactory/install repos adopt through their own governed changes
target_release: next additive contract bundle (contract-v1.23; the two omnigent schema files change bytes)
Status: ratified
Ratified by: Brett's direction on 2026-07-30 ("do omnigent runtime-wiring change"), realizing the follow-up recorded at add-domain-ontology-layer task 6.7 / design decision 13; strict validation green
---

# Proposal: add-omnigent-semantic-wiring

## Why

The ontology layer ratified the Omnigent consumption seam (design decision
13 of `add-domain-ontology-layer`): a worker-scoped semantic-context
profile per archetype or class, compiled to one small digest-pinned
context per worker — "a `verify` worker sees the classification terms it
checks, not the full generation vocabulary." The profile artifact,
compilation tool, gateway packet carriage, and pilot proof all shipped at
contract-v1.22; the two surfaces deliberately deferred to "the follow-up
omnigent change" are still missing: WHICH surface declares a profile for
a live worker, and how an install pins the compiled artifact a worker
actually receives. Until they exist, the seam is exercisable by fixture
but not wireable in a real stack. Two carried-forward review findings
also live on this exact path and become load-bearing with it: the compile
tool does not verify package bytes before compiling (F20), and truncation
itemizes only the first closure ring while the validator never checks a
truncated context's completeness (F19).

## What Changes

- **The overlay declares the seam** (`omnigent-domain-overlay`): a worker
  class MAY carry `semantic_context: {profile_id, package_id}` naming the
  worker-scoped profile in the domain's own ontology package — identity
  only, never a digest (consumers pin packages; compiled contexts carry
  the exact digests). The canonical omnigent validator gains a repo mode:
  when the domain repository carries `hermes/domain/ontology/`, every
  declared profile must resolve to an inventoried
  `xfactory_semantic_context_profile` with the declared `package_id`
  whose `worker_scope` matches the worker (archetype equality or
  worker_class equality). The permission matrix is untouched: the block
  carries no permission field and the constitutional booleans stay
  schema-`const` false.
- **The install pins the compiled artifacts**
  (`omnigent-install-manifest`): an optional `semantic_contexts` section
  with the exact kernel and domain package pins and one entry per
  declaring worker — `{worker_class, context_id, content_digest, path}`.
  Completeness is fail-closed in BOTH directions against the pinned
  overlay (a declaring worker without a pinned context, or a context
  entry naming no declaring worker, fails), and each committed artifact's
  embedded kernel/package pins and worker scope must agree with the
  section and the worker. Deep context semantics (closure, authority
  firewall, privacy) remain the ontology validator's jurisdiction — the
  artifact is the ratified `xfactory_semantic_context` kind unchanged.
- **The seam's tool becomes trustworthy at runtime**: F20 —
  `ontology-compile-context.py` verifies kernel and package bytes against
  their recorded digests before compiling and refuses drift; F19 —
  truncation itemization becomes transitive (every omitted closure member
  named, not the first ring), and the canonical ontology validator
  rejects a truncated context whose itemization is incomplete (new
  negative; ratchet 49 → 50).
- **First consumer**: MedxFactory adds two worker-scoped profiles to its
  draft ontology package (an archetype-scoped verify profile and a
  class-scoped frame profile), declares them on
  `data_reverification_agent` and `case_framing_agent`, and re-pins its
  overlay manifest. codexFactory (no in-repo ontology package yet) and
  install repositories adopt through their own governed changes.

## Impact

- Affected specs: `omnigent-domain-overlay` (ADDED requirement),
  `omnigent-install-manifest` (ADDED requirement),
  `xfactory-semantic-kernel` (MODIFIED `Bounded semantic context` —
  drifted-bytes refusal + transitive truncation scenarios).
- Affected contract bytes: the two omnigent schemas → next additive
  bundle (contract-v1.23) with refreshed manifest digests.
- Affected code: the omnigent validator (semantic checks + repo mode +
  wired examples/fixtures + new test suite), the compile tool, the
  ontology validator's truncated-context completeness rule.
- NOT affected: worker permission matrices and constitutional booleans,
  the job envelope and memory-gateway packet contracts (the packet
  `semantic_context` block already carries the artifact), Subject/Tenant
  Hermes surfaces, and the retired omnigent-install pilot.
