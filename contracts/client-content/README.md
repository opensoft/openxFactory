# client-content Contracts

Status: draft
Ratified by: add-client-layer-tuning-contracts (on ratification)

The neutral tenant-layer content contracts: what the client policy wizard
writes and the seeding runtime validates.

- `client-policy-overrides.schema.yaml` — the client's stored delta
  (`relation_to_domain: stricter_only`), including budget envelopes, the
  tracking-granularity contract, and the human-ratified auto-clear envelope.
- `client-memory-boundaries.schema.yaml` — the four per-tenant buckets with
  the `tenant_isolated` invariant, in the gateway vocabulary.
- `client-integration-boundaries.schema.yaml` — allowed integration classes;
  credential bindings are references only.
- `client-overlay.schema.yaml` — **`hermes_client_overlay`**, the seedable
  per-client document (canonical path
  `config/clients/<client_ref>/overlay.yaml` in the install repo, declared
  via the repo's `hermes_overlay_descriptor`, digest-pinned in the install's
  `client_overlays[]`). Composes the three content kinds as the enforceable
  tenant slice.
- `client.policy_namespace` + `client.policies` (inside
  `client-overlay.schema.yaml`, declared by
  `declare-client-standing-policy-contract`) — the OPTIONAL standing-policy
  block: a Tenant layer's FREESTANDING company-wide policy, keyed by policy
  id, addressable as `<policy_namespace>/<policy_id>` and materializing to
  `policy_position`. Mirrors `subject.policies` in
  `../hermes-domain-overlay/hermes-subject-overlay.schema.yaml` one layer up,
  and declares no `relation_to_*` field because a position is not a deviation.
  Declared inline rather than as a fourth sibling file: these entries carry no
  inner `kind:` to dispatch on. `client.required` is unchanged, so an overlay
  that omits the block is unaffected. The rules the shape cannot express —
  the conditional namespace requirement, address self-consistency and
  uniqueness, the declared-but-empty refusal, and a prohibited-block /
  credential scan over the `client.policies` subtree ONLY — live in the
  canonical validator.
- `examples/` — the positive overlays + domain baseline + intended-reason
  negatives the canonical validator self-tests against. Every packaged
  `*.example.yaml` other than the baseline is swept as a positive, so a new
  example cannot be added and silently never run.

Canonical validator: `scripts/validate-client-content.py` — structural
checks + the stricter-only comparability spec (allowlists ⊆, denylists ⊇,
ceilings ≤, envelope conjuncts add-only, ordered enums at-or-above; no
partial order → `review_required`, never a silent pass). One implementation,
two enforcement points: the wizard at write time, the seeder at validation.

Provenance: staged topic `openxFactory:staging:client-layer-tuning`;
brainstorm cluster Decided sections 2026-07-22.
