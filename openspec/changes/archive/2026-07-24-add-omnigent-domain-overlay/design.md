# Design: add-omnigent-domain-overlay

## Decision provenance

Architecture settled through the staged topic
`ideation/staging/omnigent-core-domain-split/` (source brainstorm captured
2026-07-21; decisions settled with Brett Heap 2026-07-22): domain content
home in the DomainxFactory `omnigent/` tree (Decision A), shared stack
identity (B), cardinality mirroring Hermes with multi-domain fleets rejected
(D), GitOps activation with the seeding evidence vocabulary (E),
subject-workload registry (F), openxFactory-contract-first sequencing,
readiness port to hermes-install, and manifest + verify as the first
realization increment. The neutral worker vocabulary (archetypes, permission
matrix, `never_assignable`) was absorbed from
`ideation/brainstorm/medical-omnigent-harness-adaptation.md` at proposal
authoring — it exists because the second domain (medical) was designed
concretely enough (11 drafted worker classes in
`MedxFactory/ideation/staging/medical-omnigent-overlay/`) to prove which
parts of codexFactory's overlay shape are domain-neutral and which are
engineering aliases.

## Positions taken at proposal authoring

- **v2 adoption (Decision C tail).** The family consumes
  `contracts/hermes-runtime/` (v2) as its first install-side consumer.
  `overlay-manifest.schema.yaml` already defines the machine-readable
  overlay shape (file inventory, sha256, `git_overlay_pin`); pinning the
  frozen v1 `contracts/schemas/` set would recreate that shape by hand and
  add a second migration later.
- **Pre-rendered effective profiles.** Materialize-the-enforceable-slice,
  as Hermes seeding chose: composed values are committed with provenance
  annotations, diffable and auditable before any worker runs. Launch-time
  composition was rejected as fresher-but-illegible for governed work.
- **Canonical vocabulary from birth.** Under
  `adopt-subject-tenant-domain-vocabulary`, a new contract family must use
  `subject`/`tenant`/`domain` machine spellings from v1. The pinned Hermes
  runtime manifest keeps its frozen `customer|client` spellings; the
  boundary is explicit: legacy spellings live only inside pinned upstream
  artifacts, interpreted via `contracts/policies/layer-vocabulary.yaml`.

## Open questions carried (realization-phase)

- **Shared-identity generation ownership.** Leaning: hermes-install owns
  generation (it already renders the runtime manifest from template +
  params); omnigent-install verifies revision equality by digest-pinning the
  rendered manifest itself. Binds task 3.1/3.2 realizations, not this
  contract — the contract requires only "digest-pin, no parallel identity".
- **Readiness cutover shape.** Whether worker-readiness enters
  hermes-install as new API surface on existing worker primitives, and
  dual-serve vs hard cut for `HERMES_READINESS_URL`. Binds task 3.2.

## Why five archetypes and two constitutional booleans

codexFactory's nine agent classes and MedxFactory's specialist-pod prose
describe the same pipeline: frame → generate → verify → challenge →
assemble-for-admission, with the terminal action (merge; order signing)
owned by external enforcement plus a human authority. Fixing that vocabulary
neutrally lets routing, validation, and review tooling operate cross-domain,
and reconciles codexFactory's two disconnected role vocabularies (machine
agent-class enum vs prose lead roles) by anchoring both to archetypes.

The permission matrix generalizes codexFactory's six repo-specific booleans.
Two are constitutional rather than configurable because they *are* the
Omnigent authority boundary from `docs/omnigent-constitution.md` and
`docs/architecture.md` ("MUST NOT own final decisions or final external
enforcement controls"; workers "never receive raw credentials") — this
change makes an existing prose boundary machine-checkable, it does not add
policy. Likewise `never_assignable` encodes MedxFactory's existing hard
invariants (no order signing, no chart write, no truth-model mutation by any
agent) as a schema tier instead of prose.

## Non-goals

- No realization in install or domain repos (tasks 3.x are separate gated
  changes; Track 1's active omnigent-install lane is untouched).
- No worker-host mutation verbs (register-worker, rotate-auth-profile) and
  no host provisioning — provisioning stays with OpsxFactory.
- No multi-domain worker fleets (rejected; revisit as federation later).
- No change to the neutral job envelope; the overlay declares domain
  `job_type` vocabularies the envelope already permits.
