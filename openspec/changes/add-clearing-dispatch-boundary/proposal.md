---
code_surface: xFactory (the aggregation repository) — ONE new workflow `.github/workflows/clearing-dispatch.yml` that PHYSICALLY CONTAINS every governed-host job, the RETIREMENT of `.github/workflows/runner-readiness-diagnostic.yml` (PR #188, merged `4fffb6e5`, 2026-09-01) in the same change that lands the clearing lane's first operation, and the AUTHORING-TIME CONFORMANCE GUARD with its test in `tests/`. THIS PACKET AUTHORS NO CONTRACT BYTE. The neutral openxFactory artifacts are DECLARED here and REALIZED POST-RATIFICATION at their own additive cut, because ratification authorizes realization and does not perform it — `contracts/clearing/` gains the SEALED-BUNDLE MANIFEST record (the ten declared fields), the CLOSED PERMITTED-OPERATIONS REGISTER as a schema-plus-instance pair on the `openxwallet-custody` convention, the OPERATION REPORT schema for `readiness-diagnostic`, the DISPATCH LEDGER record (cleared dispatches and refusals alike), the SINGLE-DOOR ATTESTATION record, packaged positive and negative examples, and the canonical `scripts/validate-clearing-dispatch.py`; registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at that cut. NOT THIS CHANGE'S SURFACE, each for a stated reason — the FACTORY-SIDE PACKAGING realization (a codexFactory hosted workflow that produces a conformant sealed bundle) is the named successor `realize-factory-bundle-packaging`; the CODING operation and the HOSTED FINALIZER that validates a patch-returning operation's output are named successors gated on that packaging, since `readiness-diagnostic` returns no repository-affecting output and would not exercise a finalizer; the operator's ONE console act per runner group is an operator act recorded in `tasks.md`, not a committed artifact; and NO runner, group, label, host, or credential is created here.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`, which forbids a proposal reserving a minor before merge order is known. The count was taken at this branch's tip rather than remembered: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v2.5` and `contracts/releases/contract-v2.5.digests.yaml` is a cut inventory in the tree. A NUMBER IS NOT WRITTEN HERE BECAUSE THE TWO CUTS AHEAD OF THIS PACKET ARE ALREADY CLAIMED: the in-flight realization of `add-chain-attestation` takes the next additive cut, and the in-flight realization of `add-chain-anchoring` allocates after it. This packet claims neither and names none; its realization reads the manifest at ITS OWN tip. THE CLASS IS ADDITIVE and nothing narrows: a new neutral contract family, no existing schema changes, no consumer pinned at the current bundle made non-conformant, and no domain obliged to own a governed execution host.
Status: draft
Proposed: 2026-09-01
Origin: `xFactory/cpc-clearing-boundary-ruling-2026-09-01.md` — Brett Heap's in-session operator ruling of 2026-09-01, which is the whole substance of this packet, PLUS his OPTION-1 SUPERSESSION of that same day recorded in its "Immediate consequences" section: NO per-path allowlist addition for readiness, the readiness test becomes THE CLEARING LANE'S FIRST OPERATION, the workflow allowlist converges to ONE PERMANENT ENTRY PER GROUP added by the operator once, and PR #188's standalone diagnostic workflow retires into that operation. The five ENFORCEMENT LAYERS the requirements below carry were ruled in the same session ("fold 1-5 in"). Its immediate consequence is also on the record: stuck run `33381257642` (a codexFactory-path council smoke queued about eighteen hours, unclaimable by design) cancelled, recorded on codexFactory issue #156.
---

# Proposal: add-clearing-dispatch-boundary

## Why

The estate has a governed execution host that more than one repository wants
to reach, and no contract that says who may reach it or how. What it has
instead is a runner-group configuration in a web console, and the first time
that configuration was asked a real question it answered correctly for a
reason nobody had written down.

**A job sat queued for eighteen hours because the door held.** Run
`33381257642` was a council smoke test dispatched from a codexFactory path.
The Cloud PC runner group it targeted permits `opensoft/codexFactory` as a
repository but lists only xFactory workflow paths in its workflow allowlist,
so the job could never be claimed by any runner. It did not run
ungoverned; it queued, forever, and was cancelled by hand. **That is the
right outcome produced by an accident of configuration**, and the difference
between those two things is the whole reason for this packet: a fail-closed
property that exists in a console and in nobody's contract is one console
edit away from not existing, and nothing would report that it had stopped.

**The obvious repair is the wrong one.** The reflex is to add the
originating repository's workflow path to the allowlist — the job runs, the
smoke test passes, and the estate has quietly acquired a second door. Repeat
that reflex once per lane per factory and the allowlist becomes the union of
everything anyone ever wanted, which is to say it becomes nothing. Worse,
each such entry grants a whole workflow file in a repository whose review
rules the host's owner does not control: a compromised or merely careless
change to that file executes on the governed host.

**So the boundary is the contract, and the aggregation repository is where
it lives.** xFactory already hosts dispatch for the estate's existing worker
lanes — `ideation-routing` states it outright: *"xFactory SHALL host dispatch
and durable reporting"* — and those lanes already move work to the host the
way this contract generalizes: a parent packages a self-contained bundle on
hosted infrastructure, dispatches a child with a run id, a source SHA and a
bundle digest, and the child validates the parent against the provider's API
before it downloads anything. The mechanics are proven in-repo. What is
missing is the RULE that makes them the only way in, and the enforcement
that notices when they stop being.

Origin: the operator ruling named in the front matter. Every requirement
below traces to it; nothing below extends it.

## What Changes

- **ADD the neutral `clearing-dispatch-boundary` capability** — ten
  requirements, organized as the FIVE ENFORCEMENT LAYERS plus the sealed
  request they enforce:

  - **THE SINGLE DOOR (L1).** The clearing repository is the only repository
    authorized to originate execution on a governed execution host. The
    provider-side runner group restricts BOTH repository access and the
    workflow allowlist, and the allowlist CONVERGES to exactly ONE PERMANENT
    ENTRY per group — the clearing workflow's exact path. Because the
    provider evaluates the allowlist against the workflow file that
    DIRECTLY CONTAINS the host job, every host-touching job lives
    physically inside that file; reusable-workflow indirection for a host
    job is non-conformant. A bypass attempt does not execute ungoverned: it
    queues unclaimable, which is fail-closed AND observable. A later
    widening, if ever ruled, is a SINGLE EXACT WORKFLOW PATH on a protected
    default branch — never repository-wide.

  - **THE SEALED BOUNDED REQUEST, and its ten declared fields.** Work
    crosses the boundary as a short-lived sealed job object carrying
    originating repository and workflow, source commit, unique job id and
    expiration, selected-file manifest with hashes, permitted operation,
    required worker profile, exact runner group and unique dispatch label,
    output schema, data-handling classification, and signature or trusted
    hosted-workflow provenance. The clearing surface is a sealed job object
    with an expiry — NEVER a committed folder of copied data.

  - **VERIFICATION IS API-SIDE, NEVER BUNDLE-TRUSTED.** The clearing
    workflow resolves originating repository, workflow path, source commit
    and dispatch identity from the provider's authoritative API and
    compares; a field inside the bundle is a CLAIM to be corroborated, and
    a self-consistent bundle is not evidence of anything. An unreadable API
    refuses; it does not pass.

  - **ONE SANCTIONED EXIT for producers (L2).** The only conformant way a
    factory expresses "this needs governed-host execution" is: package on
    hosted infrastructure, then dispatch the clearing workflow with the
    bundle handle. The host never clones the originating repository and
    never receives a credential scoped to it — so the boundary RE-SEALS,
    admitting the bundle into the clearing run and serving the host from
    there.

  - **OUTPUT IS VALIDATED BEFORE IT CAN AFFECT ANY REPOSITORY.** An
    operation whose register entry declares repository-affecting output has
    that output validated and tested by a hosted finalizer in the clearing
    repository first; the host's return is untrusted input against the
    register entry's declared output schema.

  - **THE PERMITTED-OPERATIONS REGISTER IS CLOSED.** An operation exists
    only as a register entry; a bundle naming an unregistered operation is
    refused; adding an operation is a governed contract change, not a
    workflow edit.

  - **`readiness-diagnostic` IS ENTRY #1** — a strictly read-only probe
    asserting only what the host can state about itself: runner identity
    against the expected identity, group, dispatch label, service account,
    host identity, heartbeat and clock, a NAME-ALLOWLIST-ONLY environment
    echo, and a fixed-digest compute round trip. No secrets, no checkout,
    no writes, no token scopes, and a STRUCTURED OPERATION REPORT rather
    than a log a human reads. Its checks are PR #188's, verbatim in
    substance, which is why #188's workflow retires into it.

  - **ROUTE RETIREMENT (L3).** A change that routes an existing direct
    route through the clearing lane RETIRES the old route in the same
    change. No dormant second doors — including for the grandfathered
    lanes, whose enumeration only ever SHRINKS.

  - **THE AUTHORING-TIME CONFORMANCE GUARD (L4).** A required check refuses
    a workflow file that targets a governed runner group and is neither the
    clearing workflow nor an enumerated grandfather, so a bypass is red at
    pull-request time rather than discovered as an eighteen-hour queued
    run. The guard resolves the job's declared group STRUCTURALLY; a text
    search is non-conformant, and the estate already contains the case that
    proves it.

  - **THE DISPATCH LEDGER AND THE SINGLE-DOOR ATTESTATION (L5).** Every
    cleared dispatch is recorded with its VERIFIED provenance, and so is
    every refusal. Because the door is single, that ledger is the complete
    record of everything that ever reached the host — a claim TRUE ONLY
    WHILE THE DOOR IS SINGLE, so a periodic attestation reads the groups
    from the provider API and compares them to the expected entries, and a
    divergence is a finding naming what it found. The residual dependence
    on console-side settings the estate cannot version is DECLARED, not
    assumed away.

- **NO SECOND VOCABULARY.** Runner groups, labels, leases and trust tiers
  are `worker-enrollment-broker`'s; digests are computed by
  `signed-execution-chain`'s one digest construction; scoped tokens are
  `credential-contracts` records; job scope references are
  `neutral-job-envelope`'s; handling class and tenant/data-boundary
  attestation are `document-cataloging`'s and `ideation-routing`'s. This
  capability adds the boundary and nothing those own (design D8).

- **NO CONTRACT BYTE, NO CONSOLE CHANGE, NO RUNNER.** Text only. The
  realization sequence is `tasks.md`.

## Capabilities

### New Capabilities

- `clearing-dispatch-boundary`: the neutral contract for the clearing and
  dispatch boundary in front of a governed execution estate — the single
  door and its convergence model, the sealed bounded request and its ten
  declared fields, API-side verification, the one sanctioned producer exit
  with re-sealing, hosted validation of returned output, the closed
  permitted-operations register with `readiness-diagnostic` as entry #1,
  route retirement, the authoring-time conformance guard, and the dispatch
  ledger with the periodic single-door attestation that keeps the ledger's
  completeness claim honest.

### Modified Capabilities

- None. Nothing existing is restated or narrowed. Three promoted
  capabilities are COMPOSED WITH by reference and left untouched —
  `ideation-routing` (xFactory hosts dispatch; the readiness-result
  non-competition clause, design D9), `document-cataloging` (handling class,
  host attestation, and the same non-competition clause), and
  `worker-enrollment-broker` (runner group, label, trust tier, and the
  enrollment audit record, whose subject is who may BE a runner and not what
  was CLEARED to one).

## Impact

- **New code (this change)**: none in this repository. The xFactory
  realization is one workflow, one retirement and one guard; the neutral
  `contracts/clearing/` family, its examples and its validator land
  POST-RATIFICATION at their own additive cut.
- **Composes with, and does not duplicate**: `worker-enrollment-broker`
  (runner-group and trust-tier vocabulary, and the enrollment audit trail),
  `signed-execution-chain` (the one digest construction, and the
  transparency log a dispatch REFERENCES rather than a second ledger
  format), `credential-contracts` (the scoped, short-lived credential the
  hosted clearing side uses to admit a producer's bundle),
  `neutral-job-envelope` (the sealed request seals a job; it is not a second
  job envelope), and `release-surface-integrity` (the neutral family's cut
  is measured by the declared inventory like any other).
- **Obliges the aggregation repository, and only it.** No DomainxFactory
  must own a host, a group, or a clearing workflow. A factory that wants
  governed-host execution acquires ONE obligation — package and dispatch
  per L2 — and gains a route it does not have today.
- **Named successors** (each its own change, none in this slice):
  1. `realize-factory-bundle-packaging` — the codexFactory hosted packaging
     workflow producing a conformant sealed bundle, and the register entry
     for the CODING operation it exists to feed.
  2. The HOSTED FINALIZER for patch-returning operations, gated on (1),
     because `readiness-diagnostic` returns nothing a finalizer would
     validate and a finalizer written against no returning operation is a
     finalizer written against a guess.
  3. The GRANDFATHER RETIREMENTS — each of the nine enumerated worker
     workflows retiring into a clearing operation, one change at a time,
     shrinking the enumeration each time.
  4. The neutral INFRASTRUCTURE-READINESS RESULT that `ideation-routing`
     and `document-cataloging` both await, if and when it is proposed: the
     `readiness-diagnostic` operation report is a candidate INPUT to it and
     is deliberately not that contract (design D9).
- **The two live measurements this packet rests on** (taken 2026-09-01
  against the provider API, recorded so a reader can re-take them rather
  than trust them): group `xfactory-artifact-workers` restricts to six
  workflow paths and admits TWO repositories — `opensoft/xFactory` and
  `opensoft/codexFactory`; group `xfactory-execution-lane-workers`
  restricts to one workflow path and admits ONE repository. The
  codexFactory admission is the residual the ruling closes, and it is why
  run `33381257642` could queue at all.

## Decisions carried into this proposal

**The boundary is a repository, not a policy document** (the ruling). The
clearing repository is the aggregation repository because that is where
provenance, policy, audit, throttling and emergency shutdown can be one
place instead of one place per factory.

**Convergence, not accumulation** (Brett, option 1, 2026-09-01). The
allowlist's terminal state is ONE entry per group. Every per-path addition
is a permanent widening bought for a temporary convenience, which is why
readiness became an OPERATION rather than an entry.

**A grandfather list that only shrinks** (L1/L3). Nine existing worker
workflows reach the host today. Declaring them non-conformant would break
the estate; leaving them undeclared would make the single door a fiction.
They are ENUMERATED, and the enumeration is append-never.

**Verification is API-side because a bundle is a claim** (the ruling,
verbatim in substance). The estate's own coding worker already validates its
parent against the runs API; this contract states the stance the code
already takes.

**Declare the residual honestly** (L5). Runner-group membership and
allowlists live in a console, outside version control, editable by an
administrator with no pull request. This contract cannot make that
versioned. It can make a change to it OBSERVABLE, and it says so rather
than implying an enforcement it does not have.

## Open questions carried to ratification

Recorded with a recommendation each in `design.md`. The two that must settle
before schemas are authored: **who signs a sealed bundle in the interim**
(trusted hosted-workflow provenance versus a `trust-anchor` certificate,
OQ1) and **whether the dispatch ledger is a new record or a
`signed-execution-chain` transparency-log entry** (OQ2). Both are field-10
and L5 shape decisions, and the `openxwallet` custody enumeration is the
precedent for how quietly a wrong set re-opens the hole the rule was written
to close.

## Ratification

Unratified. `Status: draft`. Ratification authorizes the realization
sequence in `tasks.md` and performs none of it — no workflow, no console
act, no contract byte follows from this document's approval alone.
