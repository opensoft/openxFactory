# codexFactory Domain Memory & Practice Catalog: what the domain remembers and recommends — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Drafts the two "learning" pieces of domain stored content — the
memory boundaries (what the domain remembers across all clients vs. what it may
never touch) and the practice catalog (the adoption profiles over promoted
capabilities that let the Domain Hermes recommend practices). Both are stored
because they are *learned or staked*, not because a model would know them:
domain memory is this domain's accumulated history, and the catalog is the
domain putting its name on "subjects of kind K should adopt capability C." The
memory side feeds the ratified customer memory gateway (never a parallel store);
the catalog side is the generation input to the practice-adoption pipeline.
Parent: `codexfactory-domain-hermes-content.md`; consumes the memory gateway
(ratified) and feeds `domain-practice-suggestion-generation.md`.
Topics: codexfactory, domain-hermes, domain-memory, memory-boundaries,
memory-gateway, practice-catalog, adoption-profile, promoted-capabilities,
domain-learning, layer-content-seeding
Repository context: openxFactory (targets codexFactory hermes/domain/memory-boundaries.yaml + practice catalog)
Captured: 2026-07-21

## Possible feats

- **`hermes/domain/memory-boundaries.yaml`** — the domain's remember/never-touch
  boundary, expressed in the gateway's vocabulary.
- **Domain practice catalog** — `adoption_profile`s over the promoted codex
  capabilities (schema neutral in openxFactory, content domain-owned).
- **Memory write-authority contract** — who proposes and who accepts a domain
  memory entry.

## Memory boundaries

The domain remembers *cross-client* learning and must never reach into any
client's private memory. Expressed in the ratified gateway's bucket/promotion
vocabulary (`openxFactory/contracts/memory-gateway/`), never a parallel store.

```yaml
schema_version: 1
kind: hermes_domain_memory_boundaries
domain_learning:                 # cross-client, domain-owned
  scope: cross_client
  remembers:
    - recurring_review_findings   # the "we keep seeing X" register
    - known_bad_patterns          # anti-patterns this domain was burned by
    - flaky_regression_history
    - practice_effectiveness      # which adopted practices actually paid off
  promotion:
    gateway: customer_memory_gateway        # ratified
    candidate_kind: promotion-candidate     # promoted only through the gateway gate
    consent_required: true
client_private:                  # the domain may NOT read this
  access: denied
  note: domain learning is generalized, never a copy of a client's private context
write_authority:
  proposer: worker                # a worker proposes a memory entry from evidence
  accepter: relevant_lead         # e.g. Lead Security accepts a security pattern — OPEN
```

The key invariant: the domain *learns in general* (a de-identified pattern
promoted through the gateway), it never *accumulates a client's specifics*. This
is what keeps a multi-client domain from becoming a cross-tenant leak.

## Practice catalog

The domain's expertise made actionable: each promoted capability MAY carry an
`adoption_profile` declaring "subjects of kind K in state S should realize
capability C via realization R." This is the generation input the Domain Hermes
reads to autonomously *suggest* practices (`domain-practice-suggestion-
generation.md`) — the domain may only ever suggest; the client clears.
Ownership split: **catalog content is codex-owned; the `adoption_profile` schema
is neutral (openxFactory)** so every domain's suggestions look the same to every
client's policy layer.

Seeded from the real promoted codex capabilities:

```yaml
schema_version: 1
kind: codex_practice_catalog
practices:
  - id: doc-health-sweep
    capability_ref: doc-health-checker           # promoted spec
    subject_kind: repository
    applicability: holds governed docs with Status headers
    realization: thin caller workflow pinned to the reusable at a released ref; runs green within N days
    maturity_gate: standard
    risk_class: low
  - id: conformance-gate
    capability_ref: conformance-gate              # promoted spec
    subject_kind: repository
    applicability: is a registered factory repo
    realization: conformance-gate workflow present and passing
    maturity_gate: standard
    risk_class: low
  - id: governed-review-lane
    capability_ref: governed-review-lane          # promoted spec
    subject_kind: repository
    applicability: opens PRs through the factory
    realization: review lane wired; verdicts recorded as governed review records
    maturity_gate: standard
    risk_class: medium                            # touches review authority
  - id: credential-contracts
    capability_ref: credential-contracts          # promoted spec
    subject_kind: repository
    applicability: requires scoped credentials
    realization: credential requirements + bindings declared; no standing prod/deploy capability
    maturity_gate: standard
    risk_class: medium                            # credential surface
```

Each profile's `risk_class` and any `credential_implications` feed the client
policy layer's auto-clear envelope — the higher the risk, the more likely a
suggestion parks for the human liaison rather than auto-clearing.

## Why these are stored (per the delta principle)

Both pass the store-vs-improvise test (`codexfactory-domain-policy-model.md`)
squarely on the "learned / staked" criteria: a model cannot know *this* domain's
recurring findings or history (memory), and putting the domain's name on a
practice recommendation is a staked position with a maturity gate, not a
generic opinion (catalog). Neither is textbook the model supplies on the fly.

## Open questions

- **Memory write-authority** — worker-proposes / Lead-accepts, and does a memory
  entry need ratification like policy, or a lighter evidence bar?
- **Catalog signing** — is adding a practice a codex OpenSpec change (the domain
  staking its reputation), matching the "who signs the catalog" question in the
  suggestion-generation brainstorm?
- **Practice ownership by Lead** — does each Lead own the adoption profiles in
  its area (Lead Security owns security-practice profiles, etc.)?
- **Memory de-identification** — the mechanism that guarantees a promoted
  `domain_learning` item carries no client-specific residue.
