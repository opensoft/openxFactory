# Authority Conservation and Consent for Crystallized Capabilities — Brainstorm

Status: staged
Kind: architecture
Summary: Crystallization must never widen authority: a capability's
permission binding is a subset of the AI configuration it replaces, the
constitutional falses (`execute_final_action`, `access_secrets`) persist,
and the capability enters the Omnigent permission matrix as a bounded
executor class; consent is three separately-grantable tiers (episode use,
automation, pooling) defaulting to deny; approvals braid across the three
Hermes layers (Domain fitness, Tenant money and policy, Subject
transparency); audit shape is identical across AI and crystallized paths;
and young capabilities carry correlated-failure throttles because
deterministic bugs fail at scale.
Topics: crystallization, authority-conservation, consent, omnigent,
permission-matrix, credential-contracts, audit-continuity, blast-radius,
layer-vocabulary, feat-request
Repository context: openxFactory (extends omnigent-domain-overlay permission
matrix and consent contracts)
Captured: 2026-07-28
Organized: 2026-07-29 into the
[recurrence-crystallization staged topic](../staging/recurrence-crystallization/recurrence-crystallization.md)
(staged); kept as design history.

## Possible feats

- **Crystallized-executor profile class** — a worker-archetype-shaped entry
  in the omnigent permission matrix with constitutional rows intact.
- **Authority-conservation validator** — mechanical check: binding ⊆
  replaced configuration's effective permissions.
- **Three-tier consent contract** — `episode_use | automation | pooling`,
  separately grantable, default deny, subject-visible where
  subject-affecting.
- **Young-capability throttles** — rate/output/spend caps that relax with
  tenure and proof.

## Position in the packet

Fifth document of the invest/build arc, and the packet's constitutional
layer: its conservation rule binds the
[build pipeline](crystallization-build-pipeline.md)'s permission review,
its ceilings feed the [ladder](crystallization-automation-ladder.md), its
consent tiers gate the [episode ledger](crystallization-episode-ledger.md)
and [cross-tenant pooling](crystallization-cross-tenant.md).

## Authority conservation

The nightmare shape: an expensive AI path that required approvals gets
"optimized" into code that silently does more than the agents were ever
allowed to. The rule that forecloses it:

> A crystallized capability's effective permissions are a **subset** of the
> effective permissions of the AI configuration whose work it absorbs.
> The constitutional falses — `execute_final_action`, `access_secrets` —
> persist at every rung, including L6.

Mechanically: the capability enters the same generalized permission matrix
the Omnigent overlay already defines — a **crystallized executor** class
rather than a novel privilege domain. Credentials ride the existing
credential-contracts (grant/binding templates, short-lived grants); code
holds no secrets, exactly like workers. Widening scope is possible only
through ordinary role-change governance on the *replaced configuration*,
never as a side effect of crystallizing. External enforcement (branch
protection, ledger, chart, DNS) remains the final backstop, unchanged.

## Three consent tiers

- **T1 episode use** — may this tenant's solved runs be mined into
  families, forecasts, and corpora? (Gates the ledger's downstream uses at
  capture — EL-C5.)
- **T2 automation** — may this workflow run without fresh AI judgment?
  Some tenants and domains will require judgment retained for categories of
  work regardless of economics; T2 is per-family-category, not global.
- **T3 pooling** — may de-identified evidence aggregate cross-tenant?
  (Owned by [cross-tenant](crystallization-cross-tenant.md); listed here
  because the tiers must be granted separately and default deny.)

Where the work is subject-affecting, the subject-facing consent path
(subject-recall-and-consent-path) applies: the subject can see that
automation served them and what it was allowed to do.

## The approval braid

Each Hermes layer gates what it owns — a clean trisection on the ratified
layer vocabulary:

| Layer | Approves | Instrument |
| --- | --- | --- |
| Domain | fitness: spec quality, corpus adequacy, rung ceiling | micro-spec ratification; domain gates |
| Tenant | money and policy: budget, T1/T2/T3, clearance | crystallization budget; auto-clear envelope / liaison |
| Subject | transparency (and consent where subject-affecting) | provenance visibility; subject consent path |

## Blast radius: determinism fails correlated

An AI path fails stochastically — one bad run. A code path fails
**systematically** — one bug × every instance until caught. Controls:

- young capabilities carry throttles (rate, output, spend caps) relaxing
  with tenure and proof freshness;
- post-conditions (DS-C3) bound per-instance damage;
- an incident auto-demotes and files the counterexample into the corpus —
  the failure is captured as future spec content, closing the loop.

Audit continuity: run records have the same shape on either path — same
gates, same evidence discipline — differing only in the provenance field.
An auditor replays the chain run → capability → spec → corpus → episodes →
original AI runs without a seam.

## Claims

- **AU-C1** — Authority conservation is constitutional: binding ⊆ replaced
  configuration, constitutional falses persist at every rung, and the check
  is mechanical, not judgment.
- **AU-C2** — Consent is three separately-grantable tiers defaulting to
  deny; T2 automation consent is per-category, and subject-affecting work
  is subject-visible.
- **AU-C3** — Audit shape is path-invariant; provenance is the only
  difference an auditor sees between AI-solved and crystal-served runs.
- **AU-C4** — Correlated-failure throttles are mandatory on young
  capabilities and relax only with tenure and proof freshness.
- **AU-C5** — Domain overlays own rung ceilings per task category; the
  regulatory posture (e.g., Medx SaMD-adjacent caution) lives there, not in
  neutral defaults.

## Open questions

- **AU-Q1** — Legal status of automated decisions per domain/jurisdiction:
  where does a crystallized capability change the regulatory
  classification of the work (the FDA-rationale thread in the
  proposal-origin staging is the model for how to hold this)?
- **AU-Q2** — Who signs permission bindings — mapping onto
  roles-authority-model: domain Lead proposes, tenant authority
  countersigns?
- **AU-Q3** — Is "crystallized executor" one matrix class or one per rung
  band (playbooks vs. programs have different failure physics)?
- **AU-Q4** — Can T2 be granted with a human-spot-check condition (an
  approval-rate contract) rather than binary yes/no?
- **AU-Q5** — Throttle schedule defaults: neutral table by rung and
  authority class, or wholly domain policy?

## Related

- `contracts/omnigent/omnigent-domain-overlay.schema.yaml` — the permission
  matrix this extends.
- `openspec/specs/credential-contracts/` and
  `openspec/specs/roles-authority-model/` — the custody and signing rails.
- [Cross-Tenant Pooling](crystallization-cross-tenant.md) — tier T3's
  owner.
