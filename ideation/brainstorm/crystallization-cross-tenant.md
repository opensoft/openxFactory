# Cross-Tenant Pooling and Neutral Promotion of Crystallized Capabilities — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recurrence evidence should pool across tenants as statistics
(fingerprints and counts, never payloads — payload movement requires the
de-identify gate and T3 consent), because a family recurring across k
tenants transforms the build economics (build once, amortize everywhere)
and turns the platform's observed demand into its product roadmap;
platform-funded capabilities are owned and priced as product features with
per-tenant configuration and hardened leak scans (generated code must not
memorize one tenant's constants), and proven capabilities promote toward
neutral contracts through the existing DTN register — DTN-015's learned
handling rule is the nearest seed.
Topics: crystallization, cross-tenant, pooling, consent, de-identification,
platform-capabilities, dtn-register, demand-derived-roadmap, data-leakage,
neutral-promotion
Repository context: openxFactory (pooling and platform-capability contracts;
DTN register extension)
Captured: 2026-07-28

## Possible feats

- **Statistical pooling contract** — cross-tenant family aggregation over
  fingerprints/counts/outcome stats under T3 consent; payloads only via the
  de-identify gate.
- **Platform capability class** — platform-funded, platform-owned registry
  entries offered to tenants as product features with per-tenant config.
- **Hardened leak-scan profile** — the BP data-leak gate strengthened for
  pooled corpora (memorized-constant detection across tenant boundaries).
- **DTN candidate kind for capabilities** — crystallized capabilities enter
  the existing neutralization register as a new artifact kind.

## Position in the packet

Sixth document of the run/renew arc and the packet's strategic horizon:
extends [families](crystallization-task-families.md) with pooled twins,
multiplies the [economics](crystallization-economics.md) numerator, adds
tier T3 to [consent](crystallization-authority-and-consent.md), hardens the
[build pipeline](crystallization-build-pipeline.md)'s leak gate, and gives
[accounting](crystallization-accounting.md) the demand-derived roadmap
feed.

## Pool statistics, not data

Two very different flows, one word:

- **Evidence pooling (statistics)** — family fingerprints, instance counts,
  cost distributions, outcome rates. De-identified by construction if
  fingerprints are structural/semantic types rather than content. This is
  what recurrence detection across tenants needs, and T3 consent covers it.
- **Corpus pooling (payloads)** — episodes from multiple tenants feeding
  one acceptance corpus. This crosses the knowledge lifecycle's de-identify
  gate, per contributing tenant, and is needed only when a platform build
  actually proceeds — so it is deferred consent, requested with the build
  decision on the table, not harvested speculatively.

Tenant-scoped families link to a **pooled twin** (TF-Q4): the twin holds
statistics and membership, never payloads.

## Platform builds: the economics phase-change

A family recurring across k tenants divides build cost by the pooled
volume — capabilities that will never clear a single tenant's threshold
clear the platform's easily. New questions arrive with the money:

- **Ownership and pricing** — platform-funded → platform-owned, offered as
  a product feature (per-tenant config on a shared core; per-tenant fences
  where policy differs). Chargeback/pricing is open (EC-Q5).
- **The strategic output** — the pooled register IS a demand-derived
  product roadmap: the platform literally watches what expert work the
  world repeatedly buys and grows features from evidence. This deserves to
  be a deliberate deliverable of the accounting surface, not a side effect
  someone notices.

## The leakage hazard

Generated code can memorize its evidence: a "constant" in a pooled build
that is actually one tenant's account number, hostname, or price list is a
cross-tenant data leak with a compiler for an accomplice. Controls:
corpus-mixing rules (pooled builds prefer synthesized/parameterized
fixtures over raw tenant episodes), the BP leak-scan gate hardened for
pooled provenance (any literal traceable to a single tenant's episodes is a
finding), and per-tenant fence review before a shared capability activates
for a new tenant.

## Neutral promotion: the DTN rhyme

A capability proven in one domain often reveals a domain-neutral core —
exactly the movement the DTN register already governs for contracts and
schemas. Crystallized capabilities should enter the same register as a new
candidate kind rather than growing a parallel process; DTN-015 ("learned
handling rule / correction-promotion loop", still `seed`) is the nearest
existing candidate and arguably this packet's ancestor entry. Path:
tenant capability → pooled platform capability → neutral contract/spec in
openxFactory with domain overlays.

## Claims

- **XT-C1** — Evidence pools as statistics under T3; payloads move only
  through the de-identify gate, per contributing tenant, and only when a
  build decision is actually on the table.
- **XT-C2** — Platform builds require T3 from every contributing tenant and
  carry the hardened leak-scan profile; a single-tenant-traceable literal
  in a pooled artifact is a gate failure.
- **XT-C3** — Platform capabilities are owned and priced as product
  features with per-tenant configuration and fences.
- **XT-C4** — Neutral promotion rides the existing DTN register as a new
  candidate kind; no parallel promotion process.
- **XT-C5** — The demand-derived roadmap is a named deliverable of the
  portfolio surface — observed recurrence is product strategy evidence.

## Open questions

- **XT-Q1** — The k threshold and whether it is count-of-tenants,
  pooled-volume, or pooled-EV based.
- **XT-Q2** — Who is the platform actor in the Subject/Tenant/Domain
  vocabulary — the operator as a distinguished tenant, or a fourth party
  the layer model should name?
- **XT-Q3** — Chargeback: subscription (feature tier), metered per
  instance, or contribution credits for tenants whose evidence seeded the
  build?
- **XT-Q4** — IP/licensing posture for artifacts generated from pooled
  evidence (feeds BP-Q5).
- **XT-Q5** — Can a tenant exit pooling retroactively — what happens to a
  shared capability built partly on their (statistical) evidence?

## Related

- [Authority and Consent](crystallization-authority-and-consent.md) — tier
  T3's constitutional home.
- `docs/domain-neutralization-candidate-register.md` — the register this
  extends (DTN-015 the seed).
- `docs/knowledge-lifecycle-model.md` — the de-identify gate reused here.
