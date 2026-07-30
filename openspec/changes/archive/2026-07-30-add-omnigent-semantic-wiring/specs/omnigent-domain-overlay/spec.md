# omnigent-domain-overlay — add-omnigent-semantic-wiring deltas

## ADDED Requirements

### Requirement: Worker semantic-context declaration
A worker class MAY declare the worker-scoped semantic-context profile it runs under, and a declaration SHALL name identity only — `profile_id` plus the domain ontology `package_id` — never a digest.
Package pins belong to consumers and compiled artifacts, so an overlay
declaration stays valid across compatible ontology releases. When the
domain repository carries an ontology package tree, the canonical
omnigent validator SHALL resolve every declared profile to an inventoried
`xfactory_semantic_context_profile` document whose `package_id` equals
the declared one and whose `worker_scope` matches the declaring worker —
either `worker_archetype` equal to the worker's archetype or
`worker_class` equal to the worker's id — and SHALL fail an unresolved or
scope-mismatched declaration. The declaration SHALL NOT change any
permission: the block carries no permission field, the six-boolean matrix
is unchanged, and `execute_final_action`/`access_secrets` remain
constitutionally false for every class with or without semantic context.

#### Scenario: A verify worker declares its profile
- **WHEN** a worker class with archetype `verify` declares `semantic_context` naming a profile whose `worker_scope.worker_archetype` is `verify` in the domain's ontology package
- **THEN** the overlay validates, and the worker's compiled context is bounded to that profile's term subset with the permission matrix untouched

#### Scenario: A declared profile does not resolve
- **WHEN** a worker class declares a `profile_id` that is not an inventoried profile of the declared package in the domain repository's ontology tree, or whose `worker_scope` names a different archetype and a different worker class
- **THEN** repo-mode validation MUST fail naming the worker and the profile

#### Scenario: A declaration attempts to carry authority
- **WHEN** a `semantic_context` declaration carries any field beyond the profile and package identity
- **THEN** schema validation MUST reject it — semantic context never widens a permission or credential surface
