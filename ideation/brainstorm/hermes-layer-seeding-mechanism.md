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

- **`seed-layer-content` lifecycle verb** (hermes-install) — increment 1
  (read-only resolve→fetch→verify→validate→evidence, single layer, no compose/
  materialize) is **proposed**: hermes-install `add-seed-layer-content` +
  Speckit `002-seed-layer-content`.
- **Layer-content record schema** (the materialized enforceable slice).
- **Deterministic overlay-compose + digest-pin** (reuse the render/pin discipline).
- **Seeding evidence record** (pins, digests, what materialized) — increment 1
  emits it as the runtime's existing redacted `LifecycleEvidence`.
- **Neutral overlay contract** (openxFactory): a `hermes_domain_overlay` schema
  + a machine-readable per-pin `overlay_path`, so validation and the role→path
  rule stop being convention.

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

1. resolve   → read the layer's overlay_ref (git+repo@rev); join (repo, rev) to the
               compatibility manifest's recorded source_archive_sha256 pin
               (no matching pin → FAIL-CLOSED, never a silent skip)
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

Pin precision (matters to step 1): the digest pins live in the install's
**compatibility manifest** (`domain_overlays[]` + `contract_repository`) — not
on the layer row, and the runtime manifest's per-layer `overlay` block carries
repository + revision only. And `overlay_ref` names a repo, not a file, so the
loader needs a **role→overlay-path rule** (domain: `hermes/domain/overlay.yaml`)
until openxFactory carries a machine-readable `overlay_path`.

Steps 2–4 reuse the discipline the runtime already proved in the release
realization (digest verify, deterministic render, no-secret scan, pin-
equivalence) — seeding is the same shape applied to *content* instead of
deployment manifests. One honesty note: the runtime *records* archive digests
today but never *recomputes* one (it verifies per-file `file_content_sha256` of
consumed artifacts); step 2 is the first actual archive-level verify, built
from the existing digest helpers.

**Increment 1 (proposed)** covers steps 1–2 plus per-kind validation and the
evidence record, for a **single layer's overlay** — no compose (3), no split/
materialize/bind (5–7). A layer whose role has no seedable overlay at its pin
(client/customer today) fails closed per-layer; on the live stack only the
Domain layer seeds until later increments land.

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

Each run emits a `seeding_evidence` record (which layer, from which pins +
digests, what materialized, when) — the content analog of the release
realization packet. Increment 1 emits it as the runtime's existing redacted
`LifecycleEvidence` (JSON output, exit code reflects outcome — there is no
evidence store); once materialization lands, the evidence should persist
alongside the materialized records. An idempotency key `(layer_id, pin)` makes
re-runs converge (re-seed is safe to repeat); the evidence is what an audit or
a later re-pin reads.

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
- **Client/project overlay source** — client and project content is wizard- and
  archetype-produced, not repo-overlay-authored; do those layers ever get a
  seedable `overlay_ref` document, or does seeding for them consume the
  per-client tree / archetype directly (with its own digest discipline)?
- **Digest pins for future overlays** — when a client/project overlay does
  become seedable, where does its `source_archive_sha256` get recorded (the
  compatibility manifest today covers only the domain overlay + contract repo)?
