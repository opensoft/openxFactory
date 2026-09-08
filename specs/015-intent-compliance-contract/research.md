# Research: Intent Compliance Contract

## Contract-family shape

**Decision**: Follow the closed record-envelope conventions used by
`contracts/worker-enrollment/` and `contracts/trust-anchor/`, with one schema per
record kind and `additionalProperties: false` at every object boundary.

**Rationale**: These are the closest multi-record, authority-bearing families
and already define repository expectations for schema identity, examples, and
manifest registration.

**Alternatives considered**: One aggregate schema was rejected because each
record has an independent lifecycle and digest. A free-form payload envelope
was rejected because it defeats closed authority validation.

## Validator architecture

**Decision**: Combine the self-testing fixture discipline of
`validate-trust-anchor.py`, the compact CLI/exit-code contract of
`validate-client-infrastructure.py`, and the shared multi-kind schema registry
of `validate-ideation-dashboard-contracts.py`.

**Rationale**: This supports schema validation, cross-record rules, deterministic
finding codes, positive/negative coverage closure, and consumer-repository scan
without introducing a new framework.

**Alternatives considered**: A schema-only validator cannot prove authority,
chain, digest, outcome, or race semantics. A new validation package would add
unnecessary abstraction to a repository of standalone canonical validators.

## Templates and examples

**Decision**: Publish one `.template.yaml` per record kind beside the schemas,
and keep executable examples under `examples/positive` and
`examples/negative`.

**Rationale**: The ratified change explicitly requires templates for all five
kinds, while the corpus needs clear machine-oriented positive/negative roles.

**Alternatives considered**: Top-level `templates/` was rejected because the
family is easier to consume and release as one closed surface.

## Release allocation

**Decision**: Tentatively use `contract-v1.44`, but allocate it only after the
final branch is refreshed from `origin/main` and remote tags confirm v1.43 is
still latest.

**Rationale**: The versioning policy forbids reservation in proposals and
requires late, collision-free allocation.

**Alternatives considered**: Reusing v1.43 would mutate released bytes;
pre-allocating a later number would race concurrent release work.

## Static dispatch evidence boundary

**Decision**: Validate a static dispatch-evidence record conditioned on the
evaluated registry revision, without shipping a credential consumer.

**Rationale**: openxFactory owns the neutral observable contract, not a runtime
service. Issuance, replay prevention, atomic consumption, and invocation are
domain-owned runtime properties that static neutral records cannot prove.

**Alternatives considered**: A fake in-process token consumer would overstate
the neutral contract and provide green tests for guarantees no runtime implements.
