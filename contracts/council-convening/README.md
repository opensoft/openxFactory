# Council-Convening Contract Family

Status: draft

Governed by `add-resolved-council-seats` and realized by Speckit feature
`026-add-resolved-council-seats`.

## Orientation

This domain-neutral family defines the portable producer-to-consumer boundary for
one resolved council roster. It publishes the closed convening schema, an indexed
standing/conditional roster corpus, and deterministic provenance resolvers. The
resolver data is fixture evidence only; production consumers provide independent
immutable-rule and authoritative-head adapters.

## Ownership Boundary

openxFactory owns the neutral contract shape, fixture index, portable validator,
and conformance expectations. A DomainxFactory owns its candidate classes,
condition vocabulary, authoritative candidate facts, and roster production.
Hermes owns admission, independent validation, snapshot freezing, job issuance,
return admission, and completion against the frozen roster. This family creates
no authority and performs no network lookup or runtime orchestration.

## Provider And Successor Responsibilities

openxFactory is the neutral provider. It owns this schema, fixture corpus,
portable validator, acceptance map, and provider-local conformance results. It
does not implement downstream admission or producer workflow behavior.

The Hermes consumer is `xFactory-Hermes-Install`. It owns independent immutable
rule evaluation, candidate-head comparison, atomic roster/provenance freeze
before jobs, exactly one job per frozen seat, frozen-mapping return admission,
missing-return parking, unlisted-return refusal, outcome-only unanimity for rich
returns, persistence, verdict-less failure, and open-run recovery.

The domain producer is `codexFactory`. It owns authoritative candidate facts,
immutable governed-rule loading, standing and conditional roster resolution,
complete convening provenance, shared-corpus parity independent from Hermes,
and one ephemeral job-local Ed25519 signing key per admitted seat. Only the
public key is registered; private key material is neither persisted nor shared,
and no convening-wide root/shared-key path survives activation.

The exact governed reusable-workflow OIDC subject is:

`opensoft/codexFactory/.github/workflows/council-lane-reusable.yml@refs/heads/main`

Naming these owners and obligations does not claim that either successor feature
has landed or that deployment, live OIDC, or runtime evidence exists.

## Coordinated Activation And Paired Rollback

Activation is a hard cutover after the provider bundle and both independently
validated successors are ready. Producer emission and consumer requirement are
enabled in one coordinated window. Mixed-protocol traffic is forbidden; an
ordering failure parks convenings rather than invoking a legacy parser,
reconstructing membership, or restoring seeded roster content.

Rollback restores the prior compatible producer and consumer versions together.
It never enables a compatibility parser, roster reconstruction, or root/shared
signing key path. Activation and rollback evidence belongs to the coordinated
operators and remains open until those operators perform and verify the acts.

## Evidence Ownership

| Evidence | Owner | Provider-local work may claim it? |
|---|---|---:|
| Neutral schema, fixtures, validator, acceptance map, focused tests | openxFactory | yes, only after execution |
| Published bundle and exact main-line commit | openxFactory release operator | no |
| Snapshot, jobs, returns, parking, persistence, recovery | xFactory-Hermes-Install | no |
| Candidate facts, roster production, job-local signing | codexFactory | no |
| Governed reusable-workflow OIDC behavior | codexFactory operator | no |
| Coordinated activation and paired rollback | coordinated operators | no |

External evidence is not inferred from local conformance. Missing downstream,
release, deployment, OIDC, or rollback proof remains explicitly open and blocks
any claim of end-to-end realization.

## Required Convening Shape

A convening carries `schema_version`, `kind`, `convening_id`, a non-empty unique
`required_seats` list, and `required_seats_provenance`. Provenance identifies the
candidate repository, pull request, exact head revision, exact governed-rule
repository/path/revision/matched class, normalized consumed facts, standing
seats, and producer-recorded conditional-seat evaluations.

Each fixture also supplies a resolver with the authoritative candidate head and
either one exact governed rule or `null` when that immutable object is
unavailable. A conditional rule declares its seat, condition reference, and a
closed predicate. Contract version 1 supports `boolean_equals`, whose `fact` is
looked up in normalized facts and compared with its boolean `expected` value.

## Artifact Inventory

- `README.md`: orientation, ownership, inventory, and prohibited-data rules.
- `fixtures/index.yaml`: ordered fixture catalog and exact fixture-file parity
  authority.
- `scripts/validate-council-convening.py`: repository-local conformance CLI.
- `tests/council_convening/test_contract.py`: index and path contract tests.
- `tests/council_convening/test_validator_cli.py`: executable CLI protocol tests.

- `resolved-council-convening.schema.yaml`: closed Draft 2020-12 convening shape.
- `fixtures/positive/` and `fixtures/negative/`: accepted and refused cases.

## Independent Validation Sequence

The validator first checks the closed schema, while assigning stable findings to
an absent roster or conclusion-only provenance. It then requires the fixture
resolver to return the exact cited rule identity, compares the authoritative
candidate head, checks every predicate-consumed fact, evaluates each predicate
without using the producer result, and compares that result with the producer's
`required` value. Only then does it perform declared-seat closure, standing-seat
completeness, and set equality against the independently reproduced roster.

This sequence fixes primary-finding precedence: `provenance_opaque`,
`rule_revision_unavailable`, `candidate_head_stale`, `fact_missing`, and
`condition_result_drift` are decided before roster arithmetic.

## Refusal Semantics

Validation refuses rather than defaults, infers, or refreshes when provenance is
opaque, the immutable rule is unavailable or does not match exactly, the current
candidate head has changed, a consumed fact is absent or non-boolean, a producer
condition result differs from independent evaluation, or the final roster is
invalid or differs from the reproduced set.

## Fixture Index Rules

The index declares `schema_version`, `kind`, `contract_version`, and an ordered
`cases` list. Case identifiers and paths are unique. Paths are repository
relative, resolve beneath `contracts/council-convening/fixtures/`, and match the
packaged fixture YAML files exactly in both directions. Accept expectations name
no primary finding; refusal expectations name one stable finding code.

The validator supports `--strict`, exact `--case` selection, and deterministic
`--json` output. Exit 0 means every requested indexed expectation matches, exit
1 means conformance or expectation mismatch, and exit 2 means invocation,
dependency, or harness failure.

## Prohibited Data And Behavior

No artifact in this family may contain private signing keys, credentials, OIDC
tokens, provider tokens, raw webhook/provider payloads, tenant data, or
host-absolute paths. The neutral harness does not fetch mutable provider state,
infer a missing roster, reconstruct an obsolete payload, authorize work, issue
seat jobs, persist snapshots, sign returns, publish releases, or claim downstream
evidence.

## Non-Goals

This family does not standardize domain candidate classes beyond the fixture
predicate vocabulary, fetch provider or rule data, authorize work, freeze a
production snapshot, issue jobs, validate returns, manage signing keys, publish
releases, or prove downstream deployment and live OIDC behavior.
