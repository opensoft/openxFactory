---
code_surface: openxFactory (a NEW `governance/factory-identity/` register family — `register.yaml` plus `wallets/`, `grants/`, and `attestations/` records mirroring the review-authority intake register's four-file shape and its deliberately-kindless register discipline, with `holder_class: organisation` and NO seat-council spelling — its reader invocation, and a DISJOINTNESS RULE asserting that no `key_id`, identifier, or public-key fingerprint appears in both register families. NO contract schema is added: OQ2 is resolved to REFERENCE, so the sealed-request manifest stays the ten fields `add-clearing-dispatch-boundary` already declares and no `contracts/` artifact moves. The xFactory clearing workflow, the codexFactory hosted packaging and sign-on-return workflows, the openXwallet reader scoping, and the codexFactory floor-file exact-set update are dependent realizations named in the impact map, NOT this change's surface.
target_release: implemented (no contract-bundle involvement — this adds a governance register family and a spec delta, not a `contracts/schemas/` artifact; no digest set moves and no release tag is owed. The archive gate is merged-plus-green realization evidence per `release-realization`, and it is ORDERED AFTER `add-clearing-dispatch-boundary` archives, this packet's MODIFIED block being written over that packet's addition)
Status: ratified
Proposed: 2026-09-01
Ratified: 2026-09-02 by Brett Heap (repository owner) — in-session, on the
recorded word *"Ratify + merge openxFactory #560"*, ratified head `33fa2b54`;
record at `openspec/changes/add-cpc-clearing-boundary/review/ratification-2026-09-02.md`.
Origin: Operator ruling, Brett Heap, 2026-09-01, recorded in the operator workspace as `cpc-clearing-boundary-ruling-2026-09-01.md` and on `opensoft/codexFactory` issue #156 — specifically its SAME-DAY EXTENSION comment, which is the half `add-clearing-dispatch-boundary` does not carry: seat-return signing resolved to option (b) sign-on-return, and per-factory Ed25519 origin keys registered in openxFactory and verified at clearing alongside provider provenance.
---

# Proposal: add-cpc-clearing-boundary

## Standing and relationship to `add-clearing-dispatch-boundary`

**THIS PACKET IS AN EXTENSION DELTA, NOT A SECOND CLEARING CONTRACT.**
`add-clearing-dispatch-boundary` (openxFactory PR #555) was RATIFIED 2026-09-01
by Brett Heap on the recorded word *"merge #192 and ratify #555"*, promotes the
capability `clearing-dispatch-boundary` with TEN requirements drawn from the
same operator ruling, and its realization is live on xFactory main
(`.github/workflows/clearing-dispatch.yml` and
`.github/clearing/grandfather-enumeration.yaml`). An earlier draft of this
packet re-authored roughly seven of those requirements in divergent vocabulary
without citing the basis at all. That draft is withdrawn and replaced by this
one.

**WHAT THIS PACKET NOW CONTAINS IS THE MEASURED DELTA.** The ruling's same-day
extension on issue #156 adds two things the ratified basis does not reach — a
registered per-repository ORIGIN KEY verified at clearing, and SIGN-ON-RETURN
attestation — and those are the only grounds on which this packet touches the
capability. THREE of the basis's ten requirements are MODIFIED, each carried
VERBATIM with its additions marked in place and every original scenario
retained — 177 basis units, none lost — and each carrying its OWN
`Modified over` marker IN ITS REQUIREMENT BODY, which is where
`govern-sibling-added-modified-deltas` (ratified 2026-08-31) requires the marker
of a MODIFIED requirement whose definition exists only as an active sibling's
addition. The marker is PER REQUIREMENT, not per section: a section-level
paragraph leaves each requirement declaring nothing, and the pairing arm reports
every one of them as unmarked. THREE requirements are ADDED to the same
capability because the basis has no counterpart to them at all. One new
capability is ADDED for the register.

**#555 MERGED 2026-09-02, AND THAT ORDER WAS LOAD-BEARING, NOT COURTESY.** This
packet's MODIFIED blocks resolve against the basis's `## ADDED Requirements`
block. While #555 is unmerged that block is not in the tree, so
`modified-block-currency` raises THREE contested warnings, one per MODIFIED
requirement (cited in tasks § 1.9).
If THIS packet merged first, those warnings would enter the nightly baseline and
#555 landing would make them vanish — a contested finding resolved without a
citation, which the uncited-resolution rule re-emits as ERRORs. The order is
the primary control; the three disposition rows in the aggregation repo's
`health/dispositions.yaml` (tasks § 1.10 and § 5.3) are the belt behind it.

**WHAT THE BASIS ALREADY RATIFIES IS CITED, NOT RE-AUTHORED.** The single door
and its append-never, shrink-only grandfather enumeration; the ten-field sealed
request and its refusal of any second digest or envelope vocabulary; the
re-seal, by which the clearing side admits the producer's object with its own
scoped read-only credential and serves the host from its own sealed object; the
producer's dispatch credential scoped to dispatching the clearing workflow
alone; the closed permitted-operations register with `readiness-diagnostic` as
entry number one; the hosted finalizer; the authoring-time guard; and the
periodic single-door attestation — all of that is the basis's, and this packet
adds nothing to it and restates none of it.

## Why

The ratified basis makes field (10) of the sealed request a DISJUNCTION: "a
signature or trusted hosted-workflow provenance". That was the right shape for
a contract that had no register of signing identities to verify against, and it
is exactly what the ruling's extension then closed — by ruling that each factory
holds one Ed25519 origin key, private half in its hosted environment, public
half registered in openxFactory, verified at clearing ALONGSIDE and never
INSTEAD OF the provider checks.

The gap the disjunction leaves is narrow and real. Trusted hosted-workflow
provenance establishes WHICH RUN produced a sealed object. It does not
establish that the originating repository's hosted environment INTENDED THAT
MANIFEST, because a run's identity and a manifest's authorship are different
facts: any workflow in the admitted repository that can reach the packaging
step inherits the provenance of the repository, and the provider has no answer
to the question of which of them meant to send this bundle. A signature over
all ten fields answers it. So this packet tightens field (10) for a repository
that HOLDS a registered identity, leaves it exactly as ratified for one that
does not — registering a key tightens a producer and never loosens one — and
adds the verification as a THIRD class beside the basis's provider-verified and
policy-checked sets, reported as its own outcome rather than folded into
either.

The second half is sign-on-return. Where a returned result must be attested by
the originating repository, the tempting shape is to give the execution host a
signing key so results are signed where they are produced. The ruling refused
it. Sign-on-return costs one hosted verification hop and buys the property that
attestation keys never leave the originating repository — which also means the
existing key placement needs no re-mint and no relocation. The basis validates
returned OUTPUT on hosted infrastructure; it says nothing about who may hold an
attestation key or where a result may be signed, and that silence is what this
packet fills.

The third item is smaller and is included because the basis has no counterpart:
a governed execution host's workspace disposal. The basis requires a dispatch
record for every dispatch and attests the completeness of that audit; making
disposal evidence a FIELD of that record puts the obligation on a surface that
already exists and is already read, rather than inventing a reporting path for
it.

## What Changes

- **MODIFIED `clearing-dispatch-boundary` — three requirements**, each carried
  verbatim from the ratified text with additions marked in place, and each
  carrying its own `Modified over` marker in its requirement body naming
  `add-clearing-dispatch-boundary` as basis:

  - *Work crosses the boundary only as a sealed bounded request* — field (10)
    ceases to be a free disjunction for a repository holding a registered
    origin identity: the signature branch becomes required and must cover all
    ten declared fields including the per-file hashes. NO ELEVENTH FIELD, and
    no second digest, envelope, or handling-classification vocabulary — the
    signature is computed over the ten already declared, with the one digest
    construction `signed-execution-chain` puts in force. TWO CONSTRUCTIONS ARE
    NAMED so that neither reads as a new one: the manifest is a JSON value and
    takes the canonical `xfc-jcs-sha256-1` construction — which first requires a
    TRANCHE-3 widening of that construction's closed `digest_subject`
    enumeration to admit a manifest subject, a widening of SUBJECTS and never a
    second construction (tasks § 2.9), until which the requirement is reported
    UNREALIZABLE rather than satisfied — while per-file content hashes are plain
    algorithm-tagged SHA-256 over file BYTES, canonical JSON having nothing to
    canonicalize in a byte stream.
  - *Every verifiable field is verified against the provider's authoritative
    API* — the origin signature becomes a THIRD verification class, verified
    conjunctively with the provider resolution (a verifying signature over
    contradicted provenance refuses; confirmed provenance with no verifying
    signature refuses) and reported as its own outcome. AND the policy-checked
    fields are RESOLVED FROM the permitted-operations register rather than read
    from the bundle: class constraints, worker profile, permitted lanes, and
    output schema come from the register entry, the bundle's copies are claims
    compared against it, and on disagreement the register governs and the
    request is refused. `deliberation` is not a register entry today; adding it
    is a governed contract change and is named as codexFactory's task, not
    assumed here.
  - *Every dispatch is recorded, and the single door is attested rather than
    assumed* — the periodic attestation's READ SET grows by one field: a
    dispatch record whose workspace-disposal field is absent or empty is
    reported as an UNATTESTED DISPOSAL and is not counted clean. Declared as a
    MODIFIED block rather than left as an implicit extension reaching into a
    ratified requirement from outside it. Nothing the attestation AUTHORIZES
    changes — the completeness claim, the expected-set comparison, and the
    closed refusal-ground enumeration are untouched.

- **ADDED to `clearing-dispatch-boundary` — three requirements** the basis has
  no counterpart to:

  - *Result attestation on the originating repository's hosted infrastructure
    after the return verifies* — the host returns UNSIGNED results, no
    attestation private key reaches a governed host, and verification strictly
    precedes signing so the hosted signer cannot become an oracle.
  - *Workspace disposal evidence as a recorded field of the dispatch record* —
    disposal on every terminal state including failure and timeout, evidenced
    in the record the basis already requires and already attests.
  - *Returned output re-served to the originator from the clearing side's own
    sealed object* — the INBOUND half of the re-seal the basis states only
    outbound. The originator never fetches an artifact belonging to the
    execution host's run and holds no credential scoped to the execution
    estate; the return crosses the way the request did. Stated rather than
    left to symmetry, which is how codexFactory PR #165 currently takes it.

- **NEW capability `factory-origin-identity` — six requirements**: one Ed25519
  origin identity per originating repository in a SIBLING register at
  `governance/factory-identity/` (design D1, which the operator has since
  confirmed); public key references only; custody in the originating
  repository's hosted packaging environment, declared and capped when
  unattested; `holder_class: organisation` with the seat-council spelling and
  per-seat key-block shape explicitly NOT inherited; a CHECKED DISJOINTNESS
  RULE over the two register families as the enforceable half of act
  distinctness, with the read-time refusal declared NOT YET IN FORCE and its
  reader dependency named; the register's OWN staleness bound and ceiling, with
  at-clearing revocation declared unrealizable until a projection path exists;
  and a permanently human-only surface entered into floors by name, landed in
  the same governed act as any consuming exact-set floor file.

- **NOT in this change**: the clearing workflow, the packaging and
  sign-on-return workflows, the openXwallet reader scoping, the codexFactory
  floor-file update, any register row, any key, and any authorization entry.

## Capabilities

### New Capabilities

- `factory-origin-identity`: the neutral contract for per-repository origin
  keys — one registered Ed25519 identity in a sibling register,
  hosted-environment custody, checked disjointness from the review-authority
  register family, an own staleness bound with at-clearing revocation held
  honestly out of force, and a permanently human-only register surface.

### Modified Capabilities

- `clearing-dispatch-boundary`: field (10) tightened for registered
  originators; origin-signature verification added as a third, conjunctive
  verification class; policy-checked fields resolved from the register rather
  than read from the bundle; the periodic attestation's read set widened by the
  disposal field; sign-on-return, workspace-disposal evidence, and inbound
  re-seal of the return added.

## Impact

- **New surface (this change)**: the `governance/factory-identity/` register
  family, its reader invocation, and the disjointness rule. No schema, no
  workflow, no key, no row.
- **Affected existing capabilities**: `clearing-dispatch-boundary` (the basis,
  as above); `credential-contracts` (the origin key's custody record, and the
  basis's two credential records unchanged); `signed-execution-chain` (its
  digest construction is used and no second one is defined);
  `roles-authority-model` (the human-only surface and its accountable issuer).
- **Correction to the withdrawn draft's impact map**: `review-authority-intake`
  is NOT a promoted capability — it is an `## ADDED` delta on the ACTIVE change
  `add-wallet-carried-review-authority`, and any dependency on it is a
  dependency on an unlanded sibling, stated as such. `specs/014-register-and-reader`
  is a Speckit feature directory, not a capability, and is not cited as one.
- **Ordering obligation**: this packet's MODIFIED block is written over an
  active sibling's addition, so its archive is ordered AFTER
  `add-clearing-dispatch-boundary` archives, per `release-realization`'s ordered
  deltas rule and the marker this delta carries.
- **Dependent realizations** (named as exit criteria, authored elsewhere):
  1. **xFactory** — origin-signature verification and register-resolved
     operation constraints in the live clearing workflow; disposal evidence as
     a dispatch-record field.
  2. **codexFactory** — the hosted packaging workflow signing manifests with the
     origin key; the hosted sign-on-return workflow verifying before signing;
     the floor-file exact-set update; and the governed register change that
     would add a `deliberation` operation, which draft PR #165
     (`adopt-bundle-shaped-deliberation`) needs and which does not exist yet.
  3. **xFactory aggregation repo** — the three `modified-block-currency`
     disposition rows in `health/dispositions.yaml`, which lives at the
     aggregation root and cannot be added from this repository.
  4. **openXwallet** — scoping the review-authority reader's wallet and grant
     resolution to its own register, which is the only thing that can make the
     read-time refusal true in both directions (OQ3).
- **Unblocks**: nothing on its own; it closes the identity half of a boundary
  whose other half is already ratified and live.
