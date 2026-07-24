# Core Omnigent + Per-Domain Install Portions — Brainstorm

Status: superseded
Superseded by: openspec/changes/archive/2026-07-24-add-omnigent-domain-overlay (its supporting-docs/ holds the staged successor of this brainstorm; canonical specs `omnigent-domain-overlay` + `omnigent-install-manifest`, contracts registered at contract-v1.16)
Kind: architecture
Summary: The Hermes installs solved "one neutral core, per-domain content by
pinned overlay" — a core runtime repo, domain knowledge authored once in each
DomainxFactory repo under `hermes/domain/`, digest-pinned in a compatibility
manifest, declared in a layers registry, and activated by a fail-closed
seeding step. `installs/omnigent-install` needs the same split and today has
only two of the three tiers: a domain-neutral core (worker runtime, Hermes
integration, generic validators) and a per-client instantiation tree
(`clients/opensoft/`) — but **no domain layer at all**. There is no place
where "Software Engineering Omnigent" content lives and no mechanism to stand
up a "MedxFactory Omnigent". This doc frames the core-omnigent / domain-portion
split by direct analogy to the Hermes pattern, maps every Hermes mechanism to
its Omnigent analog, and lists the decisions and open questions.
Topics: omnigent-install, core-omnigent, domain-overlay, domain-installation-overlay,
worker-profiles, compatibility-manifest, layers-registry, activation-path,
gitops-activation, clients-tree, dartwing, three-layer-hermes-runtime,
xfactory-domain-factory-model, stricter-rule-wins
Repository context: openxFactory (spans installs/omnigent-install,
installs/hermes-install, and every DomainxFactory repo)
Captured: 2026-07-21
Provenance note (2026-07-24): committed as the historical source brainstorm
after full realization — every mechanism proposed below shipped (neutral
overlay + install-manifest contracts, codexFactory + MedxFactory overlays,
the live install manifest with shared stack identity, byte-equivalent
rendered profiles, and the pilot readiness retirement). Retained verbatim
for provenance; the decisions record lives in the archived change.

## The gap this closes

`installs/omnigent-install` is mid-way through formalizing a generic-vs-client
split (`add-client-install-tree`, ratified) and migrating its first real
product workload (Dartwing) onto the governed opensoft QA platform
(`migrate-dartwing-to-platform-qa`, ratified). What exists:

- **Core (domain-neutral) land** — `hermes_service/`, `memory_service/`,
  `workers/` (10 role-generic profiles, prompts, scaleout policy),
  `containers/`, `compose/`, ~90 generic `scripts/validate_*.py` +
  `smoke-*.sh`, pinned copies of openxFactory contracts under `schemas/` and
  `policies/`, and the pin itself: `contracts/openxfactory-contract-ref.yaml`
  (exact-commit + per-file `mode: exact` mirror list — the compatibility-manifest
  analog already exists).
- **Client land** — `clients/opensoft/` quarantines everything
  client-concrete: Terraform QA root, Flux cluster root, workload manifests
  (ideation-dashboard, hermes-readiness, dartwing-gatekeeper), SOPS shadows,
  client-scoped validators. Verified: no domain names leak into generic land
  (one stray: `tests/test_dartwing_validator_modes.py` lives in core `tests/`).

What does NOT exist: the **domain tier**. The worker profiles are role
archetypes (coder, reviewer, tester, integrator…), not domain interpretations.
The only domain-flavored content in the repo — Dartwing — is actually
*customer/project-level* content (a specific .NET service for a specific
tenant), not domain knowledge. "Software engineering domain Omnigent" content
(toolchains, domain QA gates, domain prompt packs, domain lane policy) has no
home, and there is no path to a medical/accounting/ops/marketing Omnigent
beyond copy-fork.

The prescription already exists in draft:
`openxFactory/docs/xfactory-domain-factory-model.md` defines
`DomainxFactory = xFactory + Domain Hermes + Client Hermes + Customer Hermes +
**Omnigent overlay**` — the Omnigent overlay is named as a first-class part of
every domain repo, but its shape and consumption mechanism were never
designed. This doc is that design's brainstorm.

## The Hermes precedent — five mechanisms to mirror

From `installs/hermes-install` + the seeding brainstorm set
(`hermes-layer-content-seeding.md`, `hermes-layer-seeding-mechanism.md`):

1. **Ownership lines** (`docs/architecture/repository-ownership.md`): the
   install repo owns runtime + generic config schemas; openxFactory owns
   neutral contracts (consumed by pin, never forked); each DomainxFactory repo
   owns its domain overlay (consumed by pin). Contradiction stops work and
   raises an openxFactory change.
2. **Digest-pinned composition** (`config/compatibility-manifest.yaml`):
   consumed contracts AND `domain_overlays[]` each pinned by
   `source_archive_sha256`; verification is fail-closed.
3. **One neutral template, domains by parameters**
   (`config/templates/xfactory-stack.template.yaml` + `params/*.params.yaml`):
   adding MedxFactory was a params-only delta; generation is deterministic
   (same template revision + params ⇒ byte-identical manifest).
4. **A layers registry with enforced cardinality** (runtime manifest
   `layers[]`: exactly one `client`, exactly one `domain`, one-or-more
   `customer`; each layer row carries `policy_namespace` + an `overlay` pin).
5. **Explicit activation as a separate, gated step** (`seed-layer-content`
   verb, proposed): resolve → fetch → digest-verify (fail-closed) → validate
   (stricter-only, no raw secrets) → materialize the enforceable slice / bind
   memory / keep reference content behind the pin. Structural-only is the safe
   default state.

## Proposed shape: the Hermes → Omnigent mapping

| Hermes mechanism | Omnigent analog | Status |
| --- | --- | --- |
| `hermes-install` core runtime repo | `omnigent-install` generic land (worker runtime, hermes_service, containers, generic validators) | exists |
| openxFactory contract pin (`compatibility-manifest.yaml`) | `contracts/openxfactory-contract-ref.yaml` | exists; extend with `domain_overlays[]` digest pins |
| Domain content in DomainxFactory `hermes/domain/` | Domain content in DomainxFactory `omnigent/` | **missing — the core of this brainstorm** |
| Stack template + params → runtime manifest `layers[]` | An Omnigent stack/install manifest declaring client + domain + customer workloads — OR consume the Hermes runtime manifest as the single source of stack identity (see Decision B) | missing |
| `seed-layer-content` runtime verb (fail-closed) | GitOps activation: dormant foundation → Flux workload-root inclusion, validator-mode ladder `render → activation → cluster → public`, two-PR (foundation, then activation) | exists for Dartwing; generalize + align vocabulary |
| `config/clients/<client>/` records | `clients/<client>/` install trees | exists |
| Cardinality validator (1 client, 1 domain, N customers) | Same rule per Omnigent install stack | missing |

### What a DomainxFactory `omnigent/` overlay contains (candidate inventory)

Authored once in the domain repo, install-invariant, consumed by pin:

- **Worker profile deltas** — specializations of the core role archetypes
  (coder/reviewer/tester/integrator…) with the domain's toolchain, review
  standards, and gate expectations. Override semantics should reuse the
  existing neutral contract's operations: `supplement` / `replace` /
  `constrain` / `veto` with `stricter_rule_wins: true`
  (`openxFactory/contracts/schemas/domain-installation-overlay.schema.yaml`).
- **Prompt packs** — domain overlays on `workers/prompts/`.
- **Toolchain container layers** — e.g. a .NET/TypeScript build image family
  for codexFactory vs clinical-document tooling for MedxFactory, layered on
  the core `containers/omnigent-worker/` base.
- **Domain QA validators** — the missing middle tier between core
  `scripts/validate_*.py` (mechanism-level) and client-tree
  `validate-dartwing-gatekeeper.sh` (customer-instance-level). E.g. ".NET
  service admission gates" belongs to the domain, parameterized per customer.
- **Spec Kit preseed packs** — domain deltas on `speckit/preseed-manifest.yaml`.
- **Lane / scaleout policy deltas** — domain constraints on
  `workers/scaleout/` job-assignment and lane policy.
- **Merge-council / review-council configuration** — the Omnigent-side (Plane-2)
  counterpart of the Hermes-side deciders described in
  `codexfactory-domain-hermes-content.md` ("MoA advises, Hermes roles decide,
  openxFactory enforces the rail").

### Layer mapping for the first consumer (today's install)

- **client** = opensoft (exists: `clients/opensoft/`)
- **domain** = codexFactory / Software Engineering (**absent** — nothing in
  the repo says this install is a software-engineering Omnigent; it's implicit
  in the worker profiles' bias)
- **customer** = Dartwing, ideation-dashboard, hermes-readiness, Project Alfa
  (exist, but only as k8s trees / demo fixtures — no registry row declares
  them as customer workloads)

Naming/placement insight: Dartwing looked like "the domain" but is a customer
workload of the software-engineering domain. The core/domain split makes this
legible: `clients/<client>/` keeps infra instantiation; the domain overlay
keeps what makes any .NET-gatekeeper-shaped workload reviewable; the manifest
registry declares which customer workloads exist and their activation state.

## Decisions to take

- **A. Domain content home.** (1) DomainxFactory repo under `omnigent/`
  (recommended — mirrors `hermes/domain/`, matches
  `xfactory-domain-factory-model.md`, keeps all of a domain's layer content in
  one ratifiable repo); (2) separate `omnigent-<domain>` repos (more pins, no
  benefit found); (3) per-domain dirs inside omnigent-install (violates the
  ownership line — install repo would fork domain policy).
- **B. One stack identity or two.** Should the Omnigent install *consume the
  Hermes runtime manifest* as the source of truth for client/domain/customer
  identity (one stack document shared by both installs — Omnigent adds only
  its overlay-resolution + workload sections), or carry its own parallel
  manifest generated from the same neutral template family? A shared identity
  document eliminates layer-drift between the two installs of the same stack;
  a parallel manifest keeps the installs independently deployable. Leaning:
  shared identity, separate install manifests that both pin it.
- **C. Overlay contract.** Reuse
  `domain-installation-overlay.schema.yaml` (its `stage_overrides` operations
  and stricter-rule-wins invariant fit) vs. author a new
  `omnigent-domain-overlay` contract for worker-profile/toolchain semantics.
  Likely: keep the neutral overlay envelope, add an Omnigent-specific payload
  schema under it. Also decide against which contract generation: hermes-install
  pins the v1 `contracts/schemas/` set while the v2 `contracts/hermes-runtime/`
  set (incl. `overlay-manifest.schema.yaml` — file inventory + sha256 +
  `git_overlay_pin`, exactly the machine-readable overlay shape needed) sits
  unpinned. A new Omnigent consumer could adopt v2 first.
- **D. Cardinality.** Mirror Hermes: one Omnigent install stack = exactly one
  client + exactly one domain + N customer workloads. Multi-domain hosting on
  one worker fleet is tempting for cost but breaks the policy_namespace
  isolation story; reject for now, note as future federation.
- **E. Activation semantics.** Hermes activates content with a runtime verb;
  Omnigent activates workloads via GitOps (Flux workload-root inclusion +
  validator-mode ladder + two-PR human gate). Keep GitOps as the enforcement
  plane — it IS the external enforcement layer in the model — but adopt the
  seeding pipeline's *evidence vocabulary* (resolve/fetch/digest-verify/
  validate/activate, fail-closed, idempotent evidence records) so both
  installs' activation stories audit the same way. Dormant-foundation ≙
  structural-only; activation-PR ≙ seed.
- **F. Registry for customer workloads.** Add `customer` entries (with
  activation state + validator-mode) to the Omnigent manifest so "what is
  installed and how live is it" is machine-readable, not inferred from Flux
  tree diffs.

## Possible feats

- **Neutral Omnigent overlay contract** (openxFactory) — envelope reuse of
  `domain_installation_overlay` + an Omnigent payload schema (worker-profile
  deltas, toolchain bindings, domain validators, preseed packs).
- **Omnigent install manifest + compatibility extension** (omnigent-install) —
  layers/workloads registry, `domain_overlays[]` digest pins in
  `openxfactory-contract-ref.yaml` (or a sibling compatibility manifest),
  cardinality validator, deterministic generation from a neutral template.
- **codexFactory `omnigent/` authoring** — first real domain overlay:
  worker-profile deltas for the software-engineering domain, .NET/TS toolchain
  bindings, domain QA gates (fold the Dartwing validator's domain-generic
  parts up into it).
- **Overlay compose + verify step** (omnigent-install) — the GitOps-side
  analog of `seed-layer-content`: resolve overlay pins, digest-verify
  fail-closed, compose core→domain→client→customer, render the effective
  worker profiles + validator set, emit evidence.
- **Relocate the stray** — `tests/test_dartwing_validator_modes.py` out of
  core `tests/` into the client tree (or the future domain overlay's test
  pack).
- **Second-domain proof** — a MedxFactory params + overlay-pin fixture that
  renders a medical Omnigent install manifest without touching core (the
  Omnigent equivalent of `medxfactory-example.params.yaml`).

## Open questions

- Does the Omnigent overlay live at DomainxFactory repo root as `omnigent/`
  (sibling of `hermes/`), and does `xfactory-domain-factory-model.md` need a
  MODIFIED requirement to prescribe its internal shape?
- If Decision B lands on "shared stack identity": which install owns manifest
  generation, and how does the other verify it consumes the same revision
  (digest pin of the manifest itself?)?
- How do worker-profile deltas compose at runtime — pre-rendered effective
  profiles committed to the install (auditable, diffable) vs. composed at
  worker launch (fresher, less legible)? Hermes chose materialize-the-
  enforceable-slice; the analog here is probably pre-rendered effective
  profiles with provenance annotations.
- Customer-workload archetypes: is there an Omnigent analog of the
  project-type template library (`project-type-template-library-draft.md`) —
  e.g. "dotnet-gatekeeper-service" as a deployable customer archetype the
  Dartwing tree instantiates?
- Naming skew inherited from Hermes: customer vs subject vs project — adopt
  whatever `add-hermes-customer-subject-runtime-contract` lands on.
- Does Project Alfa (synthetic demo) become a customer archetype fixture in
  core, or a customer entry under a test client tree?
- Papertrail/observability bindings in the Dartwing validator: client-level,
  domain-level, or core policy?

## Exit path

Organize into an `ideation/staging/` topic (`omnigent-core-domain-split/`)
once the A–F decisions have positions, then split into OpenSpec changes:
(1) openxFactory — Omnigent overlay payload contract + domain-factory-model
amendment; (2) omnigent-install — manifest/registry + compatibility pins +
compose-and-verify step; (3) codexFactory — author `omnigent/` first consumer.
Second-domain proof (MedxFactory fixture) gates calling the pattern real.
