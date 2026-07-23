# Design: adopt-subject-tenant-domain-vocabulary

## Decision provenance

Brett selected **Subject / Tenant / Domain** on 2026-07-22 after reviewing
three alternatives per slot. Alternatives considered and rejected:

- Tenant layer: **Operator** (names the running role, but collides with the
  human operator role word inside OpsxFactory) and **Organization** (projects
  well — Medx already says Care-Organization — but bland and encodes nothing
  about the platform relationship).
- Subject layer: **Case** (idiomatic in every domain but names the work
  envelope, not the party that holds consent) and **Principal** (fits
  consent/authority semantics but strains for non-person subjects and collides
  with IAM "principal" in Ops contexts).

"Subject" and "Tenant" won partly because the repository had already converged
on them organically: `per_tenant` isolation keys, "tenant administrators" and
"served subject" in the avatar-first UI standard, "subject / tenant-operator /
expert-domain" in the canonical gloss, and a literal `subject` key in three of
five DomainxFactories.

## Why staged rather than a wholesale rename

The legacy spellings are load-bearing in released, evidence-backed machine
surfaces: `contracts/hermes-runtime/` encodes role kinds
`customer|client|domain`, `customer_subject` / `customer_subject_ref`, and
schema `$id`s, all published as a digest-inventoried bundle that
`installs/hermes-install` pins (Track 2 is mid-realization against pin
`28277b7`). Renaming those identifiers now would break the pinned
compatibility bridge that `add-hermes-customer-subject-runtime-contract`
deliberately built, and would churn hundreds of conformance-test IDs in its
evidence register. The versioning policy already reserves identifier breaks
for major bundle versions, so the machine migration waits for one; prose and
new surfaces adopt immediately.

## Collision analysis (review §A1)

The reserved-terms rule is written against the observed failure, not just
style: Ledgerx uses "Client Hermes" for its served-subject layer because its
subjects *are* client companies. Under the new vocabulary that layer is
Subject Hermes with a domain alias of Client Company Hermes — the alias model
makes the previously colliding name legal again as an explicitly declared,
one-layer-bound specialization instead of an ambiguous canonical term.

## Non-goals

- No semantic change to any layer's responsibility boundary.
- No change to the Customer-instance cardinality/isolation model ratified by
  `add-hermes-customer-subject-runtime-contract` (that spec's "Customer
  instance" reads as "Subject instance" via the mapping; its machine surface
  is frozen until the next major).
