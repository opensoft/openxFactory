code_surface: codexFactory
target_release: implemented

## Why

The proposal-supporting-document lifecycle records provenance only after a
staged folder moves: `origin_path` appears in the support manifest, but the
OpenSpec proposal packet itself never identifies a staging source and never
declares when a proposal was intentionally created ad hoc. A proposal can
therefore bypass brainstorm and staging without a machine-checkable exception
— exactly as the bootstrap `add-proposal-supporting-doc-lifecycle` change did.
The routing change explicitly deferred general proposal-origin policy to this
topic (its task 1.3).

## What Changes

- Require every OpenSpec change proposal to declare exactly one origin in its
  `.openspec.yaml` — `staged` (durable `<repo>:staging:<topic-slug>` id plus
  the original staging path) or `ad_hoc` (durable id, reason, approving
  authority, approval date) — fixed at creation and immutable after
  ratification.
- Extend the supporting-document manifest to repeat the origin declaration;
  manifest and packet values must match.
- Extend the proposal gate to reject a missing origin, an unknown or
  malformed kind or id, an unresolvable staged id/path, disagreement among
  staging header, packet, and manifest, incomplete ad-hoc approval
  provenance, or both origin kinds declared at once.
- Extend the archive gate to verify the origin declaration survives
  unchanged: staged origins retained in the compressed support manifest,
  ad-hoc reason and approval provenance retained even when no support bundle
  exists.
- Add the fifteenth deterministic doc-health family, `proposal-origin`,
  enforcing the above by reference; implementation follows the
  `add-cross-factory-ideation-routing` realization, and this change's
  doc-health enumeration delta is declared relative to that change's outcome
  per the ordered-deltas rule.
- Migrate history without fabricating it: amend the archived bootstrap
  supporting-doc-lifecycle packet with an explicit ad-hoc origin, backfill
  proposals that carry staged support manifests as `staged`, classify the
  rest `ad_hoc`, and keep migration provenance reviewable.
- Self-application: this change's own `.openspec.yaml` declares the
  `openxFactory:staging:proposal-origin-contract` staged origin — the
  acceptance proof that the contract works.
- Establish proposal provenance only. This change MUST NOT claim FDA/SaMD
  compliance; the regulatory rationale remains staged for a future
  regulated-traceability profile.

## Capabilities

### Modified Capabilities

- `document-lifecycle`: Adds the proposal-origin declaration (staged and
  ad-hoc kinds, durable ids, proposal-gate rejections) and extends the
  supporting-document manifest to repeat the origin.
- `release-realization`: Adds origin retention to the archive gate — the
  declaration must survive archive unchanged, with or without a support
  bundle.
- `doc-health`: Adds the `proposal-origin` deterministic check family as the
  fifteenth family, declared relative to the ideation-routing change's
  outcome.

## Impact

- **openxFactory:** proposal packets gain an origin block; the migration
  backfills archived and active changes with recorded, reviewable provenance;
  transition tooling guidance updated.
- **codexFactory:** the fifteenth deterministic family, transition-tool
  origin writing, strict-gate wiring, fixtures, and tests; implementation
  follows the ideation-routing realization.
- **Compatibility:** pre-contract changes receive backfilled origins from
  recorded evidence only — no staging folders or source history are
  fabricated; existing staged topics and manifests remain valid.
