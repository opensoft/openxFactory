# Contract: Resolved Council-Seats Successor Handoff

Status: draft planning contract

## Provider Exit Gate: openxFactory

The provider feature may hand off only when:

- schema meta-validation and closed-shape tests pass;
- fixture index parity and all positive/negative expectations pass;
- acceptance-map counts are exactly 3 governed requirements and 11 scenarios,
  with all 14 FRs and 7 SCs mapped;
- manifest, contracts README, changelog, and digest inventory agree on the exact
  realized family and next available bundle;
- strict OpenSpec validation passes;
- local evidence names only acts actually performed.

The handoff pins an exact published bundle. Planning does not reserve its version
or claim that a commit, tag, merge, image, deployment, or live OIDC run exists.

## Consumer Successor: xFactory-Hermes-Install

Hermes owns:

- parsing the new envelope with no obsolete-payload branch;
- resolving and independently evaluating the cited immutable governed rule;
- comparing the admitted head to the provenance head;
- atomically freezing roster and provenance before allocating jobs;
- issuing exactly one job per frozen seat;
- admitting returns only from the frozen seat/job mapping;
- counting substantive rich-return outcome fields without comparing signature or
  unrelated provenance fields;
- parking on missing required returns and retaining verdict-less failure and
  open-run recovery behavior;
- PostgreSQL persistence/race/recovery proof and shared-corpus parity.

Hermes must not author candidate-class rules, call codexFactory evaluator code,
or derive membership from obsolete seeded council content.

## Producer Successor: codexFactory

codexFactory owns:

- authoritative GitHub candidate fact collection bound to exact PR head SHA;
- loading the governed candidate-class rule at an immutable revision;
- resolving standing and conditional seats before submission;
- emitting complete provenance and the new `required_seats` roster;
- running the shared corpus through an implementation independent from Hermes;
- assigning only admitted seats to worker jobs;
- generating one Ed25519 key inside each seat job, registering only its public
  key under the runtime seat-job identity and governed OIDC subject, signing that
  job's return, and discarding the private key without persistence or sharing;
- removing the convening-wide shared/root-key path at activation.

The governed first-domain OIDC workflow subject is:

`opensoft/codexFactory/.github/workflows/council-lane-reusable.yml@refs/heads/main`

## Coordinated Activation

1. Publish and pin the neutral provider bundle.
2. Land both downstream implementations and their local/shared-corpus evidence
   without enabling mixed-protocol traffic.
3. Verify producer output and consumer admission against the same bundle and
   exact candidate/rule test objects.
4. Activate producer emission and consumer requirement in one coordinated
   window. If ordering fails, park convenings rather than accepting old payloads.
5. Roll back producer and consumer together to the prior pair. Do not roll back
   by enabling a compatibility parser or reconstructing membership.
6. Record live OIDC, deployment, image, merged-commit, and release proof only
   after an authorized operator actually performs and verifies those acts.

## Evidence Ownership

| Evidence | Owner | Local planning may claim? |
|---|---|---:|
| Neutral schema, fixtures, validator, tests | openxFactory | yes, after run |
| Published bundle tag and exact main-line commit | openxFactory release operator | no |
| Snapshot/job/return/PostgreSQL behavior | Hermes successor | no |
| GitHub fact collection and job-local signing | codexFactory successor | no |
| Live GitHub OIDC subject/token behavior | codexFactory operator | no |
| Coordinated deployment and rollback rehearsal | joint operators | no |

Unavailable external evidence remains explicitly open and blocks any claim of
full end-to-end realization, but does not invalidate honestly scoped local proof.
