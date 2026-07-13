code_surface: openxFactory
target_release: implemented

## Why

xFactories need one provider-neutral avatar protocol before a reusable client,
reference broker, or domain overlay can be implemented safely. The original
`define-avatar-client-runtime` proposal combined that protocol with a live API
spike, executable reference broker, and avatar-first UI migration. Its 25
requirements and 97 scenarios formed a program rather than one independently
realizable change.

This change preserves the staged origin and reviewed architecture but narrows
realization to the canonical AVC contract kernel. Three sibling changes own
F0 feasibility, the non-deployable reference runtime, and UI-standard
alignment. Their implementations may proceed in parallel against the frozen
interface baseline; only final publication and compatibility pins are ordered.

## What Changes

- Publish eight neutral, YAML-serialized JSON Schema draft 2020-12 contracts
  under `contracts/avatar-client/`: AVC-01 session request, AVC-02 discriminated
  session result, AVC-04 session event, AVC-06 structured confirmation, AVC-07
  retention profile, AVC-08 persona profile, AVC-11 session command, and AVC-12
  state snapshot. AVC-03 and AVC-05 remain absorbed; AVC-09 and AVC-10 remain
  reserved.
- Publish shared definitions and closed registries for result reasons, events,
  commands, retention classes, capabilities, and the neutral consent purposes
  `avatar.media_capture`, `avatar.provider_processing`, and
  `avatar.structured_record`.
- Define authenticated and purpose-bound session semantics, exact-offer retry
  identity, credential-free non-grant outcomes, sideband-before-answer media
  authorization, leases and epochs, one sequenced log, snapshot recovery,
  confirmation authority, consent revocation, retention, telemetry redaction,
  model-profile indirection, and fail-closed deferred features.
- Add canonical valid, invalid, boundary, compatibility, redaction, and
  adversarial fixtures plus `scripts/validate-avatar-client.py` and a complete
  acceptance map using stable `ACR-*`, `SCO-*`, and `RBG-*` identifiers.
- Ratify openxFactory ownership, content-addressed consumer pinning, the future
  private `xfactory-avatar-client` boundary, and the separation between neutral
  contracts, server trust, client presentation, and DomainxFactory overlays.
- Allocate the contract bundle version only at realization, update manifest and
  changelog atomically, publish the matching annotated tag from the release
  commit, and record per-file digests.
- Consume the sibling F0 result as a publication gate. Contract implementation
  may proceed concurrently, but `FAIL` or `INCONCLUSIVE` evidence, or an
  undisposed interface variance, blocks the bundle tag.
- Use the registered parallel-workstream plan: this change alone owns
  `contracts/avatar-client/` and `scripts/validate-avatar-client.py`. It owns
  shared contract metadata for the kernel release; the UI sibling touches those
  integration files only in its later, rebased profile-schema release.

## Capabilities

### New Capabilities

- `avatar-client-runtime`: Defines the neutral AVC protocol and authority
  semantics consumed by clients, brokers, workflow services, and domains. It
  does not itself provide an executable broker or UI implementation.

### Modified Capabilities

- `shared-contract-ownership`: Makes openxFactory the canonical AVC owner;
  releases have one matching manifest version, changelog entry, annotated tag,
  exact commit, and digest set; consumers pin content and run canonical
  conformance fixtures.
- `repo-boundary-governance`: Defines the future private
  `xfactory-avatar-client` boundary, internal-live evidence gate, and separately
  approved aggregation, web-console, and production-runtime integrations.

## Impact

- **openxFactory contract surface:** `contracts/avatar-client/`,
  `scripts/validate-avatar-client.py`, `contracts/manifest.yaml`,
  `contracts/CHANGELOG.md`, `contracts/README.md`, and contract-versioning
  guidance.
- **F0 feasibility sibling:** reads the provisional interface baseline and
  reports evidence and variances; it cannot change canonical contracts.
- **Reference-runtime sibling:** implements against the baseline in exclusive
  runtime/test paths, then proves conformance against the released commit and
  digests.
- **UI-standard sibling:** consumes purpose, capability, outcome, and state
  registries without modifying them.
- **xfactory-avatar-client:** not created here; `implement-avatar-client-lab`
  creates it in a separately approved private repository.
- **DomainxFactories:** later author profiles and consent-purpose mappings.
  This change does not modify any DomainxFactory repository; domain adoption
  requires separately approved changes in each owning repository.
- **Hermes and live operations:** authority ports are defined, but live Hermes
  integration, deployment, provider qualification, and pilot operations remain
  in successor changes.
- **Compatibility:** existing static avatar-first profiles remain valid; the
  AVC family is additive and has no released consumer yet.
