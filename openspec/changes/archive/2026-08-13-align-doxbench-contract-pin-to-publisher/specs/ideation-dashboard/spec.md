# ideation-dashboard

## ADDED Requirements

### Requirement: doxBench resolves its released contract from the checkout it runs in
The dashboard runtime SHALL resolve the pinned doxBench wire schemas from the repository it is running in whenever that repository is itself a publisher release, and MUST NOT reach a sibling checkout in preference to its own tree. Resolution precedence SHALL be, highest first: an explicitly supplied checkout; the `OPENXFACTORY_ROOT` operator override; the hosting repository when it carries the publisher markers; then the existing walk up to an aggregation-relative `openxFactory/`; and a refusal when none of those yields a checkout. Only the third rung is new, and no rung above or below it moves.

A serve MUST verify contracts against the tree it was launched from. The path this replaces searched one level below where it stood, so from inside the publisher it walked past itself every time and landed on the aggregation's submodule checkout — a shared tree that sessions move between branches — which meant a serve started from one worktree could verify its wire shapes against another session's working state. That this has so far been harmless is a property of two files not having changed, not a guarantee anything makes.

The runtime's pinned release SHALL name the release the repository currently publishes, and a repin MUST carry the digests that release's own manifest records. Where the schema bytes are unchanged across the releases spanned, the repin SHALL be digest-neutral: it re-declares which release is read and changes no verified byte, so no conformance question reopens.

The two model routes SHALL keep their current refusal shape and their current gate order. A route that cannot read the contract MUST still refuse before consulting any port, MUST still emit only the fixed catalog code, and MUST NOT let a pin diagnostic — which names checkout paths and digests — reach the wire. Recovery comes from the resolution beneath the routes succeeding, never from a route relaxing what it refuses.

The honest empty-catalog posture SHALL remain distinct from a contract failure. A plane with no configured model provider MUST receive a conformant empty catalog as a SUCCESS, and MUST NOT be served the refusal that means the contract could not be read — the two say different things to an operator and MUST NOT be collapsed.

#### Scenario: The model routes are served from a publisher checkout
- **WHEN** the dashboard serves from an openxFactory checkout carrying the publisher markers
- **THEN** the released schema validators MUST resolve from that same checkout
- **AND** the model catalog and chat-turn routes MUST NOT refuse for want of a declared consumption pin

#### Scenario: A sibling checkout is not preferred over the running tree
- **WHEN** the hosting repository is a publisher release and an aggregation-relative `openxFactory/` checkout also exists
- **THEN** the hosting repository MUST be resolved
- **AND** the sibling checkout's branch or working state MUST NOT affect the verdict

#### Scenario: An operator names a checkout explicitly
- **WHEN** a checkout is supplied directly or through `OPENXFACTORY_ROOT`
- **THEN** that checkout MUST be used in preference to the hosting repository

#### Scenario: The pinned bytes have drifted
- **WHEN** a pinned schema in the resolved checkout no longer matches its digest or its manifest entry
- **THEN** both model routes MUST refuse with the fixed catalog code
- **AND** the refusal MUST NOT disclose the checkout path or digest

#### Scenario: No model provider is configured
- **WHEN** the contract resolves and no provider port is available
- **THEN** the catalog route MUST return a conformant empty catalog as a success
- **AND** it MUST NOT return the contract-unavailable refusal

#### Scenario: The released rung runs without an environment override
- **WHEN** the dashboard test suite runs from a publisher checkout with no `OPENXFACTORY_ROOT` set
- **THEN** the released-contract probes MUST execute rather than skip
- **AND** a pin that a serve would refuse on MUST surface as a test failure
