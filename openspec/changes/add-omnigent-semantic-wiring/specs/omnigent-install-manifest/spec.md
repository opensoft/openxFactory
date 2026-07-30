# omnigent-install-manifest — add-omnigent-semantic-wiring deltas

## ADDED Requirements

### Requirement: Install-pinned worker semantic contexts
An install manifest whose pinned domain overlay declares worker semantic-context profiles SHALL carry a `semantic_contexts` section pinning the exact kernel and domain ontology packages and one compiled context per declaring worker.
Each entry SHALL name the worker class, the compiled `context_id`, the
artifact's `content_digest`, and its install-relative path. Completeness
SHALL fail closed in both directions: a declaring worker without a pinned
compiled context, and a context entry naming no declaring worker, are
each validation failures — a worker never runs without the bounded
meaning its overlay declares, and no context rides an install unclaimed.
Every committed artifact SHALL be the ratified `xfactory_semantic_context`
kind whose embedded kernel and package pins equal the section's pins,
whose declared `content_digest` equals the entry's, and whose
`worker_scope` matches the declaring worker; deeper context semantics —
closure, authority firewall, privacy — remain the canonical ontology
validator's jurisdiction over the same artifact bytes. An install whose
overlay declares no semantic context MAY omit the section entirely.

#### Scenario: A wired install validates
- **WHEN** the pinned overlay declares semantic context for two worker classes and the manifest pins kernel and package digests plus two compiled artifacts whose embedded pins, digests, and worker scopes agree
- **THEN** the install manifest validates and each worker receives exactly its profile's compiled subset

#### Scenario: A declaring worker has no pinned context
- **WHEN** the pinned overlay declares `semantic_context` for a worker class and the manifest's `semantic_contexts` section carries no entry for it
- **THEN** validation MUST fail naming the worker — the worker never launches without its bounded context

#### Scenario: A pinned artifact disagrees with the section pins
- **WHEN** a committed context artifact embeds a kernel or package digest different from the section's pins, or a `content_digest` different from its entry, or a worker scope that matches neither the worker's archetype nor its class
- **THEN** validation MUST fail closed naming the disagreement
