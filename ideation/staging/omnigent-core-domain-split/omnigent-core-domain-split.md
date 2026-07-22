# Staged: Core Omnigent + Per-Domain Install Portions

Status: staged
Kind: architecture
Summary: Split `installs/omnigent-install` into the three tiers the Hermes
installs already have — a domain-neutral core, per-domain overlay content
authored in each DomainxFactory repo under `omnigent/` and consumed by digest
pin, and per-client instantiation trees — plus the install-manifest mechanics
(shared stack identity with the Hermes install, cardinality, compose+verify
with evidence) that make a second domain a params-only delta. Sequencing
settled 2026-07-22: the neutral contract ratifies here FIRST; install-repo
realization changes follow.
Topics: omnigent-install, core-omnigent, domain-overlay, worker-profiles,
compatibility-manifest, install-manifest, shared-stack-identity,
worker-readiness, hermes-install, codexFactory, activation-path
Repository context: openxFactory (neutral overlay + install-manifest
contracts); realizations in `installs/omnigent-install` (manifest + verify),
`installs/hermes-install` (worker-readiness port), `xFactories/codexFactory`
(first `omnigent/` overlay authoring)
Staging ID: openxFactory:staging:omnigent-core-domain-split
Source: `ideation/brainstorm/omnigent-core-domain-split.md` (captured
2026-07-21); the omnigent-install ↔ hermes-install ↔ codexFactory review and
Option A/B decisions settled with Brett Heap 2026-07-22; parent roadmap
`ideation/brainstorm/omnigent-lane-activation-path.md` (this is P3-adjacent
structure).

## Target capability and delta

- ADDED `omnigent-domain-overlay` (neutral): the contract for per-domain
  Omnigent content — envelope reuse of
  `domain-installation-overlay.schema.yaml` (`supplement/replace/constrain/
  veto`, `stricter_rule_wins: true`) with an Omnigent payload schema
  (worker-profile deltas, prompt packs, toolchain container bindings, domain
  QA validators, Spec Kit preseed deltas, lane/scaleout policy deltas).
- ADDED or MODIFIED install-manifest contract: the Omnigent install manifest
  consumes the Hermes runtime manifest as the single source of
  client/domain/customer stack identity (digest-pinned), adding only
  overlay-resolution and customer-workload registry sections; cardinality
  mirrors Hermes (exactly one client, exactly one domain, N customer
  workloads).
- MODIFIED `xfactory-domain-factory-model` guidance: prescribe the
  DomainxFactory `omnigent/` tree shape (sibling of `hermes/domain/`).

## Claims

1. **The Hermes install pattern is the template.** An install is a template +
   parameter set + deterministically generated manifest + compatibility
   manifest with per-artifact digest pins, verified fail-closed; a second
   domain (MedxFactory) must be a params-plus-overlay-pin delta, never a
   copy-fork.
2. **Domain content lives in the DomainxFactory repo** under `omnigent/`
   (Decision A of the source brainstorm), consumed by pin, never forked into
   the install repo — the same ownership line hermes-install ratified.
3. **Shared stack identity** (Decision B — settled 2026-07-22): the Hermes
   runtime manifest is the identity source; the Omnigent install manifest
   digest-pins it, eliminating layer drift between the two installs of one
   stack while both remain independently deployable.
4. **GitOps stays the activation plane** (Decision E), adopting the seeding
   pipeline's evidence vocabulary (resolve/fetch/digest-verify/validate/
   activate, fail-closed, idempotent evidence records) so both installs
   audit identically.
5. **The pilot Hermes service retires into hermes-install.** The
   worker-readiness heartbeat API (today the pilot's `/api/readiness`,
   deployed as `hermes-readiness.xforge.us`) ports to the hermes-install
   runtime via its own OpenSpec change (settled 2026-07-22); the runtime
   already freezes the pilot's seven governed primitives as compatibility
   fixtures. The pilot `hermes_service/` and the standalone readiness
   deployment retire when that lands.
6. **First realization increment is manifest + verify only** (settled
   2026-07-22): the manifest quartet, `domain_overlays[]` digest pins,
   cardinality validation, and a read-only compose+verify step emitting
   hermes-install-style evidence records; worker-host mutation verbs
   (register-worker, rotate-auth-profile) fold in later. Host provisioning
   stays with OpsxFactory — install verbs validate prepared hosts, never
   provision them.
7. **codexFactory is the first overlay author**: software-engineering
   worker-profile deltas, .NET/TypeScript toolchain bindings, and domain QA
   gates (folding the domain-generic parts of the Dartwing validator up out
   of the client tree). The live execution-lane binding (coding-patch-worker
   profile v1, proven 2026-07-13) becomes a rendered consequence of the
   overlay + params, not hand-maintained state.

## Decisions record

From the source brainstorm: A (domain content home = DomainxFactory
`omnigent/`), D (cardinality mirrors Hermes; multi-domain fleets rejected for
now), E (GitOps activation + seeding evidence vocabulary), F (customer
workloads become registry entries with activation state).

Settled with Brett Heap 2026-07-22: sequencing (openxFactory contract first,
realizations after), B (shared stack identity), readiness-API disposition
(port to hermes-install), first-increment scope (manifest + verify).

## Open questions

- **Overlay contract generation** (Decision C tail): pin the v1
  `contracts/schemas/` set or adopt the v2 `contracts/hermes-runtime/` set
  (incl. `overlay-manifest.schema.yaml`) as its first consumer?
- **Effective-profile composition**: pre-rendered effective worker profiles
  committed with provenance annotations (the materialize-the-enforceable-
  slice analog, leaning) vs. composed at worker launch.
- **Manifest generation ownership**: with shared identity, which install owns
  generation of the identity document and how does the other verify revision
  equality (digest pin of the manifest itself)?
- **Readiness port shape**: does worker-readiness enter hermes-install as new
  API surface on the existing worker primitives, and what happens to the
  execution lane's `HERMES_READINESS_URL` cutover (dual-serve window vs.
  hard cut)?

## Exit

One openxFactory OpenSpec change ratifying the neutral overlay +
install-manifest contracts (`code_surface: openxFactory`), followed by
gated realization changes: `installs/omnigent-install` (manifest + verify
increment), `installs/hermes-install` (worker-readiness port),
`xFactories/codexFactory` (first `omnigent/` overlay). The topic archives
only when the codexFactory overlay renders the live execution-lane binding
byte-equivalently and a second-domain params fixture renders without
touching core.
