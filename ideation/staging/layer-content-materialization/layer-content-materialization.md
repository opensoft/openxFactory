# Staged: Layer Content Materialization (seeding increment 2 + the neutral overlay contract)

Status: superseded
Superseded by: openspec/changes/archive/2026-07-23-add-hermes-domain-overlay-contract (openxFactory) and [hermes-install 2026-07-23-add-layer-content-materialization](https://github.com/opensoft/xFactory-Hermes-Install/tree/main/openspec/changes/archive/2026-07-23-add-layer-content-materialization)
Kind: architecture
Summary: Take the proven read-only load path (seeding increment 1, realized
and archived 2026-07-22) to enforcement: a neutral `hermes_domain_overlay`
schema + machine-readable `overlay_path` in openxFactory contracts, and
hermes-install seeding increment 2 materializing the enforceable slice into
`layer_content` records that gates check at write time. Increments 3–6
(gateway binding, composition, re-pin flow, job-time reference loading) stay
behind it on the recorded roadmap.
Topics: layer-content-seeding, seed-layer-content, materialization,
hermes-domain-overlay, neutral-contract, layer-content-records, hybrid-seam,
hermes-install
Repository context: openxFactory (neutral schema) + installs/hermes-install (increment 2)
Staging ID: openxFactory:staging:layer-content-materialization
Source: ideation/brainstorm/ — hermes-layer-content-seeding.md (umbrella),
hermes-layer-seeding-mechanism.md; decisions recorded 2026-07-22; increment 1
evidence at hermes-install `openspec/specs/layer-content-seeding/spec.md`.

## Outcome (recorded 2026-08-28)

COMPLETE. Both exit changes were ratified, realized and ARCHIVED on
2026-07-23, and both archives were verified at their own trees on
2026-08-28:

| Exit | Repository | Archived packet |
| --- | --- | --- |
| Neutral `hermes_domain_overlay` contract + `overlay_path` | openxFactory | `openspec/changes/archive/2026-07-23-add-hermes-domain-overlay-contract` (`contract-v1.15`) |
| Seeding increment 2 (materialization) | xFactory-Hermes-Install | `openspec/changes/archive/2026-07-23-add-layer-content-materialization` (PR #6, `696ec48`) |

The hermes-install capability spec carries increments 1 + 2; increments
3–6 and the gate wiring are recorded THERE as the live roadmap, which is
why closing this topic parks no work. The topic folder is retained as
PROVENANCE — the reason this document is `superseded` rather than
deleted.

## Claims (decided 2026-07-22)

1. **The seam is hybrid — decided.** Enforceable slice → runtime records;
   reference content behind the pin; memory through the gateway. The
   field-level cut list (overlay field → `content_kind` → reading gate) is
   drafted in the mechanism brainstorm.
2. **Record shape: generic `layer_content` kernel** keyed
   `(layer_id, content_kind, enforceable_payload, provenance)` + specialized
   views where gates need structured queries.
3. **Compose site: build-time render + seed-time verify** (the proven
   realization discipline); the runtime never templates.
4. **Seeding order is an invariant:** domain → client → project,
   REFUSED-with-reason on missing prerequisite, never a silent skip.
5. **Client/project content unifies into this path:** the wizard commits a
   per-client overlay that seeds through the same pipeline (client-tuning
   topic), so the schema work here is shared, not domain-only.
6. **Increment 1 is realized** (merged PR #5, archived
   `2026-07-22-add-seed-layer-content`) — digest verify, role→path REFUSE,
   per-layer independence, idempotent evidence are tested behavior.

## Exit path

- **openxFactory change — `add-hermes-domain-overlay-contract`:** the neutral
  `hermes_domain_overlay` schema (replacing the runtime's minimal structural
  check) + a machine-readable per-pin `overlay_path` (role→path stops being
  convention). Unblocks every domain, not just codex.
- **hermes-install change — seeding increment 2:** `layer_content` kernel
  migration + materialization step in `seed-layer-content` + the stricter-only
  mechanical check hook (comparability spec, from the client cluster).
  **Gated on domain increment A landing** (real content to materialize) and
  the neutral schema.

## Open questions (carried to the proposals)

- Exact `enforceable_payload` schema per `content_kind` (cut list is the draft).
- Who owns the build-time render (release pipeline vs. a compose verb in the
  domain repo).
- Digest-pin home for wizard-written overlays, and who signs them.
- Re-pin range recording (compatibility manifest vs. consent record) —
  increment 5.
- Partial re-seed (one content kind without a full layer re-seed).

## Readiness

Schema change is ready to propose now (independent). Increment 2 proposes
against domain change A's landed content — sequence:
`add-hermes-domain-overlay-contract` ∥ domain A → increment 2.
