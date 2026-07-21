# Hermes Layer Seeding Mechanism: making the content live (the central seam, detailed) — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Details the umbrella's central seam — the runtime `seed-layer-content`
step that turns the drafted layer content from inert git into live governance.
Following the hybrid decision: after a layer is registered, seeding resolves its
pinned `overlay_ref`, verifies the digest (fail-closed), composes the overlay
stack (Core → xfactory → domain → client → project) into a deterministic,
digest-pinned bundle, validates it (schemas + stricter-only + no-raw-secrets +
source-authority), then splits it into **three destinations**: the enforceable
slice materializes into runtime records so gates check it at write time; memory/
knowledge binds to the gateway (federated, not copied); and reference content
(persona prose) stays addressable behind the pin. Idempotent, re-seeds on re-pin
(a client-consented event), and fails closed — an unseeded layer stays
structural-only, which is safe. Runs in hermes-install. Parent:
`hermes-layer-content-seeding.md`.
Topics: seeding-mechanism, seed-layer-content, overlay-ref, hybrid-seam,
materialization, digest-pinning, determinism, fail-closed, memory-gateway,
runtime-records, hermes-install, lifecycle-verb
Repository context: hermes-install runtime (consumes openxFactory/domain/client/project content)
Captured: 2026-07-21

## Possible feats

- **`seed-layer-content` lifecycle verb** (hermes-install).
- **Layer-content record schema** (the materialized enforceable slice).
- **Deterministic overlay-compose + digest-pin** (reuse the render/pin discipline).
- **Seeding evidence record** (pins, digests, what materialized).

## Recap of the seam decision

From the umbrella: **hybrid**. Materialize the *enforceable* slice (the things
gates must check) into runtime records; leave *reference* content (persona
prose) behind the pin; keep *memory* in the gateway. Store-the-delta and the
runtime hybrid are the same line — the enforceable slice *is* the stored delta.

## When it runs

After the structural layer exists: `register-stack` (Client/Domain/Customer) and
`provision-project` (each new Customer layer) create the `hermes_layers` rows
with their `overlay_ref` + pins. **Seeding is the missing next step** that loads
what those pointers point at. Today `overlay_ref` is inert; seeding activates it.

## The `seed-layer-content` pipeline

```text
seed-layer-content [--layer <id> | --all] [--reseed]

1. resolve   → read the layer's overlay_ref (git+repo@rev) + template_revision + parameter_digest
2. fetch+verify → fetch the pinned overlay archive; verify sha256 == pin      (FAIL-CLOSED on mismatch)
3. compose   → apply the overlay stack (Core → xfactory → domain → client → project)
               into a rendered content bundle; compute the bundle digest       (deterministic, like generate-manifest)
4. validate  → schemas + stricter-only invariant + no-raw-secrets scan
               + source-authority present                                      (FAIL-CLOSED)
5. split     → enforceable slice   vs   reference slice   vs   memory/knowledge
6. materialize → enforceable → runtime records; memory → gateway bindings; reference → addressable-behind-pin
7. bind      → attach to the layer (layer_id FK); register gateway provider-bindings + (client) KB adapters
8. record    → seeding_evidence {layer, pins, digests, materialized_kinds, at}; idempotency key
```

Steps 2–4 reuse the discipline the runtime already proved in the release
realization (digest verify, deterministic render, no-secret scan, pin-
equivalence) — seeding is the same shape applied to *content* instead of
deployment manifests.

## The three destinations

| Content | Destination | Enforced / used how |
| --- | --- | --- |
| policies, layer boundaries, auto-clear envelopes, escalation rules, authority (owns/decides), practice-catalog adoption profiles, consent models | **runtime records** (materialized) | gates check at write time (the `layer_id`-scoped tables; approvals already earmarked) |
| memory & knowledge base | **gateway bindings** (federated) | retrieval primitives, consent-gated — never copied into records |
| persona prose / character frames / role narrative | **pinned reference** (git+repo@rev) | loaded by agents at job time (interpret-at-use) |

This is the hybrid made concrete: the persona's *authority* (owns/decides/
escalates + disposition + guardrail) materializes and is enforced; the persona's
*character frame* stays behind the pin and is read when the agent speaks.

## Determinism, digest-pinning, re-seed

The composed bundle is digest-pinned (the `parameter_digest` analog); re-seeding
the same pins is byte-identical (pin-equivalence). **Re-pinning** a layer (e.g. a
domain content upgrade) = re-compose + re-seed the enforceable slice — a
**client-consented pin-range event** (the umbrella's open question resolved this
way): the client consents to a pin *range*, the domain moves within it, and a
move outside the range requires fresh consent.

## Fail-closed

Any failure — digest mismatch, schema-invalid, a client policy that would weaken
a domain gate (stricter-only violation), a raw secret in the bundle, missing
source-authority — **fails the seeding closed**. The layer stays structural-only:
registered but content-blank, which is the safe default (everything parks for
the human liaison, nothing auto-clears). A half-seeded layer is never left live.

## Evidence & idempotency

Each run writes a `seeding_evidence` record (which layer, from which pins +
digests, what materialized, when) — the content analog of the release
realization packet. An idempotency key makes re-runs converge (re-seed is safe
to repeat); the evidence is what an audit or a later re-pin reads.

## Where this sits in the bigger path

Seeding is **P1** of the omnigent-lane activation path
(`omnigent-lane-activation-path.md`): it is the step that makes the Hermes layer
content enforceable, which is the prerequisite for a Hermes-*managed* omnigent
lane. It is hand-built (the lane cannot build the content loader it depends on).

## Ownership / plane

Seeding is a **hermes-install runtime lifecycle verb** (the umbrella's "Where it
lives" table: the runtime is what materializes content into the live stack). The
*content* is authored elsewhere (domain in codexFactory by pin, client by wizard,
project by archetype); the *mechanism* is hermes-install. It composes the Core
ops tier below it (deploy) and the content overlays above it (govern).

## Open questions

- **Record shape** — one generic `layer_content` table keyed by (layer_id,
  content_kind, enforceable_payload, provenance), or specialized tables per kind
  (policies, escalation, personas-authority, practice-catalog)? (Leaning: a
  generic kernel + specialized views where gates need structured queries; the
  approvals tables already exist.)
- **Compose location** — render the bundle at build time (pre-pinned, like the
  deploy manifest) or at seed time in-runtime? (Leaning build-time render +
  seed-time verify, matching the realization flow.)
- **Reference-slice loading** — how do agents fetch pinned persona prose at job
  time — a governed read primitive, or a mounted pinned checkout?
- **Partial re-seed** — can one content kind re-seed (e.g. just the practice
  catalog) without a full layer re-seed?
- **Seeding order** — domain before client before project (dependencies:
  stricter-only needs the domain gate present first)?
