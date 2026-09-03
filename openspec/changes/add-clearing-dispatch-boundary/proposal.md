---
code_surface: xFactory (the aggregation repository) — ONE new workflow `.github/workflows/clearing-dispatch.yml` that PHYSICALLY CONTAINS every governed-host job, the RETIREMENT of `.github/workflows/runner-readiness-diagnostic.yml` (`opensoft/xFactory#188`, merged `4fffb6e5`, 2026-09-01) in the same change that lands the clearing lane's first operation, and the AUTHORING-TIME CONFORMANCE GUARD with its test in `tests/`. THIS PACKET AUTHORS NO CONTRACT BYTE. The neutral openxFactory artifacts are DECLARED here and REALIZED POST-RATIFICATION at their own additive cut, because ratification authorizes realization and does not perform it — `contracts/clearing/` gains the SEALED-BUNDLE MANIFEST record (the ten declared fields), the CLOSED PERMITTED-OPERATIONS REGISTER as a schema-plus-instance pair on the `openxwallet-custody` convention, the OPERATION REPORT schema for `readiness-diagnostic`, the DISPATCH LEDGER record (cleared dispatches and refusals alike), the SINGLE-DOOR ATTESTATION record, packaged positive and negative examples, and the canonical `scripts/validate-clearing-dispatch.py`; registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at that cut. NOT THIS CHANGE'S SURFACE, each for a stated reason — the FACTORY-SIDE PACKAGING realization (a codexFactory hosted workflow that produces a conformant sealed bundle) is the named successor `realize-factory-bundle-packaging`; the CODING operation and the HOSTED FINALIZER that validates a patch-returning operation's output are named successors gated on that packaging, since `readiness-diagnostic` returns no repository-affecting output and would not exercise a finalizer; the operator's ONE console act per runner group is an operator act recorded in `tasks.md`, not a committed artifact; and NO runner, group, label, host, or credential is created here.
target_release: THE NEXT ADDITIVE MINOR, DELIBERATELY NOT NUMBERED HERE — allocated AT REALIZATION by merge order per `docs/contract-versioning-policy.md`, which forbids a proposal reserving a minor before merge order is known. The count was taken at this branch's tip rather than remembered: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v2.5` and `contracts/releases/contract-v2.5.digests.yaml` is a cut inventory in the tree. A NUMBER IS NOT WRITTEN HERE BECAUSE THE TWO CUTS AHEAD OF THIS PACKET ARE ALREADY CLAIMED: the in-flight realization of `add-chain-attestation` takes the next additive cut, and the in-flight realization of `add-chain-anchoring` allocates after it. This packet claims neither and names none; its realization reads the manifest at ITS OWN tip. THE CLASS IS ADDITIVE and nothing narrows: a new neutral contract family, no existing schema changes, no consumer pinned at the current bundle made non-conformant, and no domain obliged to own a governed execution host.
Status: ratified
Proposed: 2026-09-01
Ratified: 2026-09-01 by Brett Heap (repository owner) — in-session, on the
recorded word *"merge #192 and ratify #555"*, ratified head `15b14bb3`;
record at `openspec/changes/add-clearing-dispatch-boundary/review/ratification-2026-09-01.md`.
Origin: `cpc-clearing-boundary-ruling-2026-09-01.md`, WRITTEN AND PUSHED to the root of `opensoft/xFactory` as `opensoft/xFactory#192` (https://github.com/opensoft/xFactory/pull/192, branch `record/cpc-clearing-boundary-ruling`, head `5b6a9fdf`) — MERGED 2026-09-01T11:47:21Z at `faee7a96ae6e06c15b6c2122947c62356e96f71d`, on the same recorded word as this packet's own ratification, discharging the gate ratification was held on (`tasks.md` §2.3) — Brett Heap's in-session operator ruling of 2026-09-01, which is the whole substance of this packet, PLUS his OPTION-1 SUPERSESSION of that same day recorded in its "Immediate consequences" section: NO per-path allowlist addition for readiness, the readiness test becomes THE CLEARING LANE'S FIRST OPERATION, the workflow allowlist converges to ONE PERMANENT ENTRY PER GROUP added by the operator once, and `opensoft/xFactory#188`'s standalone diagnostic workflow retires into that operation. Requirements 1–7 trace to that written record; requirements 8–10 EXTEND it and are DECLARED EXTENSIONS ruled in the same session on Brett's verbatim instruction "fold 1-5 in and fan out", their provenance recorded in that record's append-only addendum — requirement 9 (the authoring-time guard) wholly absent from the record, requirement 8's general rule a generalization of the one retirement the record names, and requirement 10's periodic attestation an addition to the dispatch recording the record does state (the per-requirement split is in "Why"). Its immediate consequence is also on the record: stuck run `33381257642` (a codexFactory-path council smoke queued about eighteen hours, unclaimable by design) cancelled, recorded on codexFactory issue #156.
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

Origin: the operator ruling named in the front matter — and the trace is a
SPLIT, which this packet states rather than smooths.

**Requirements 1–7 trace to the WRITTEN ruling.** The single door, the sealed
bounded request and its ten declared fields, API-side verification, the one
sanctioned producer exit, hosted validation before any repository effect, the
closed permitted-operations register, and `readiness-diagnostic` as entry #1
are each in the record's own text, verbatim in substance.

**Requirements 8–10 EXTEND the written record, and the extension is stated
per requirement rather than in bulk** — because two of the three have a
partial written footing and one has none, and lumping them together would
trade one imprecision for another:

- **Requirement 8, route retirement.** The record names ONE retirement,
  verbatim: *"PR #188's standalone workflow is retired into the clearing
  operation."* So the specific act is on the record. THE GENERAL RULE IS NOT:
  that ANY change routing an existing direct route through the clearing lane
  retires it in the same change, in BOTH the live allowlist and the in-repo
  enumeration, and that the grandfather enumeration is append-never and
  shrink-only, is this packet's generalization of that one instance.
- **Requirement 9, the authoring-time conformance guard.** WHOLLY ABSENT from
  the record. Nothing in it speaks of pull-request-time refusal, a required
  check, or structural resolution of a job's declared group. This requirement
  is the largest of the three extensions and the one a ratifier should read
  most carefully.
- **Requirement 10, the ledger and the attestation.** The DISPATCH RECORD is
  on the record — the clearing workflow *"records the dispatch"*, and
  xFactory is named as the one place for provenance, policy and audit. THE
  PERIODIC SINGLE-DOOR ATTESTATION IS NOT: the word does not appear in the
  record, and conditioning the ledger's completeness claim on a green
  attestation is this packet's addition.

All three were ruled in the SAME SESSION, on Brett's verbatim instruction —
*"fold 1-5 in and fan out"* — and they are carried here as DECLARED
EXTENSIONS submitted for ratification, not as encodings of text already on
the record. Saying "nothing below extends the ruling" would have been false,
and an extension is better named than hidden inside a claim of fidelity.

**Their provenance is verifiable in one place** — the origin record's
APPEND-ONLY ADDENDUM, which captures that instruction. The record has been
WRITTEN AND PUSHED to `opensoft/xFactory` at the repository root as
`cpc-clearing-boundary-ruling-2026-09-01.md`, as `opensoft/xFactory#192`
(https://github.com/opensoft/xFactory/pull/192, branch
`record/cpc-clearing-boundary-ruling`, head `5b6a9fdf`) — MERGED
2026-09-01T11:47:21Z at `faee7a96ae6e06c15b6c2122947c62356e96f71d`.
Ratification, gated on that merge (`tasks.md` §2.3), was taken the same day:
an extension whose provenance a reader cannot open would have been an
extension taken on trust, and the merge closed that gap before the
ratifying word.

## What Changes

- **ADD the neutral `clearing-dispatch-boundary` capability** — ten
  requirements, organized as the FIVE ENFORCEMENT LAYERS plus the sealed
  request they enforce:

  - **THE SINGLE DOOR (L1).** The clearing repository is the only repository
    authorized to originate execution on a governed execution host. The
    provider-side runner group restricts BOTH repository access and the
    workflow allowlist, and the allowlist CONVERGES to exactly ONE PERMANENT
    ENTRY per group — the clearing workflow's exact path. The neutral
    property is that the host-touching job is DECLARED IN THE ARTIFACT THE
    PROVIDER EVALUATES ITS ALLOWLIST AGAINST; on the estate's provider that
    artifact is the workflow file directly containing the job, so the
    realization is that every host-touching job lives physically inside the
    clearing workflow file and reusable-workflow indirection for a host job
    is non-conformant (design D2 carries the provider-specific evidence). A bypass attempt does not execute ungoverned: it
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
    there. THE PRODUCER'S DISPATCH CREDENTIAL IS SCOPED TO DISPATCHING THE
    CLEARING WORKFLOW ALONE, and the residual is stated rather than
    implied: a compromised producer holding that credential can still
    dispatch REGISTERED operations. The closed register and each entry's
    per-operation constraints are the containment — not the credential.

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
    no writes, no token scopes — constraints of THIS OPERATION'S register
    entry and not of the clearing workflow forever, since the clearing side
    acquires its admission credential at the first bundle-carrying
    operation — and a STRUCTURED OPERATION REPORT rather than a log a human
    reads. Its checks are `opensoft/xFactory#188`'s,
    verbatim in substance, which is why `opensoft/xFactory#188`'s workflow
    retires into it.

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
    proves it. TWO CAPABILITY GAPS ARE DECLARED, not assumed closed. First,
    the clearing repository has NO required status check today — measured
    2026-09-01: none of `opensoft/xFactory`'s five active rulesets declares
    `required_status_checks`, and its Tier-1 main protection (ruleset
    `18962101`) carries `pull_request`, `non_fast_forward` and `deletion`
    only — so an operator act creates that rule (`tasks.md` §4.5), and even
    then that ruleset's `bypass_actors` (`OrganizationAdmin`, mode
    `always`) leaves a required check OPERATOR-BYPASSABLE. Second, the
    guard's refusal of an ADDITION to the grandfather enumeration is a
    frozen-ORIGIN comparison — the test holds the nine names and asserts the
    live enumeration's members are a SUBSET of them, so an addition turns
    the suite red — and an in-repo guard can itself be edited, which makes
    the mechanical refusal a TRIPWIRE BACKED BY REVIEW of any diff touching
    the enumeration or the guard, not an unforgeable refusal.

  - **THE DISPATCH LEDGER AND THE SINGLE-DOOR ATTESTATION (L5).** Every
    cleared dispatch is recorded with its VERIFIED provenance, and so is
    every refusal — a refusal's ground drawn from a NAMED, CLOSED
    enumeration, seeded now with `unregistered_operation` and
    `unknown_lane_selector`. Because the door is single, that ledger is the
    complete record of everything that ever reached the host — a claim TRUE
    ONLY WHILE THE DOOR IS SINGLE, so a periodic attestation reads the
    groups from the provider API and compares them to an expected set
    computed PER GROUP: the clearing workflow's path, plus the members
    enumerated FOR THAT GROUP whose allowlist entry is `present`. THE TWO
    DIVERGENCE DIRECTIONS ARE NOT THE SAME FINDING. An allowlist entry not
    derivable from that group's expected set is a WIDENING — a single-door
    breach, reported as a finding. An enumerated member with NO allowlist
    entry is ALREADY FAILING CLOSED and is a DARK-LANE DISPOSITION ITEM
    (`tasks.md` §8.3), not a breach; conflating the two would have made the
    attestation red on day one over two lanes that cannot reach the host at
    all. The residual dependence on console-side settings the estate cannot
    version is DECLARED, not assumed away.

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

- None. Nothing existing is restated or narrowed. Three capabilities are
  COMPOSED WITH by reference and left untouched — TWO PROMOTED,
  `ideation-routing` (xFactory hosts dispatch; the readiness-result
  non-competition clause, design D9) and `document-cataloging` (handling
  class, host attestation, and the same non-competition clause), plus ONE
  RATIFIED BUT NOT YET PROMOTED, `worker-enrollment-broker` (runner group,
  label, trust tier, and the enrollment audit record, whose subject is who
  may BE a runner and not what was CLEARED to one). That third is the ACTIVE
  change `openspec/changes/add-worker-enrollment-broker` — realized at
  `contract-v1.29`, and deliberately NOT under `openspec/specs/`, so this
  packet consumes its vocabulary as ratified-but-unpromoted rather than as
  promoted canon.

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

**A grandfather list that only shrinks, and it is DATA** (L1/L3). Nine
existing worker workflows reach the host today. Declaring them
non-conformant would break the estate; leaving them undeclared would make
the single door a fiction. They are ENUMERATED, append-never, in a GOVERNED
DATA FILE the L4 guard and the L5 attestation both read —
`.github/clearing/grandfather-enumeration.yaml` in `opensoft/xFactory` —
rather than as a constant inside a test module, because two consumers of the
same list must not each carry their own copy. Each member declares its
workflow filename, its GOVERNED RUNNER GROUP, the governed-host job ids in
that file, and its ALLOWLIST-ENTRY STATUS (`present` or `absent`). The group
attribution is what makes the attestation's expected set computable per
group, and the status field is what keeps a dark lane from reading as a
breach. As measured 2026-09-01: group `xfactory-execution-lane-workers`
allowlists exactly `execution-lane-coding-worker.yml`; group
`xfactory-artifact-workers` allowlists six —
`council-deliberation-worker`, `dashboard-image-worker`, and the four
doc-health workers (`analysis`, `cataloger`, `derive-possibles`,
`readiness`); and `review-lane-worker.yml` and `ideation-organizer-worker.yml`
sit in NEITHER allowlist, so they enumerate as `absent`.

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

**OQ3 is no longer open.** Where the grandfather enumeration physically
lives is SETTLED AT REALIZATION AND PENDING RATIFICATION: the governed data
file `.github/clearing/grandfather-enumeration.yaml` in the clearing
repository, read by both the L4 guard and the L5 attestation, with the
neutral contract requiring only that such an enumeration exist, be closed,
carry per-member group attribution and allowlist status, and shrink. The
question's history and its rejected candidates stay in `design.md` rather
than being deleted, because a settled question with its alternatives erased
reads like a question nobody asked. OQ4 (attestation cadence and finding
surface) remains open with its recommendation.

## Ratification

**RATIFIED 2026-09-01** by Brett Heap (repository owner) — in-session, on
the recorded word *"merge #192 and ratify #555"* — ratified head
`15b14bb3`; record at
`openspec/changes/add-clearing-dispatch-boundary/review/ratification-2026-09-01.md`.
Ratification authorizes the realization sequence in `tasks.md` and performs
none of it — no workflow, no console act, no contract byte follows from
this document's approval alone; #555's own merge stays gated on the
inherited pytest-suite failure recorded at `tasks.md` §9.2.

**CORRECTION, 2026-09-02 — the gate this paragraph names has since
cleared, and the PR it named has since merged.** #555 MERGED as squash
`ab0bb2dd2e642fce43bee3d02128bafd664d3be3` on 2026-09-02T09:16:29Z, admin
squash with provenance on Brett Heap's recorded word (PR #555 comment,
2026-09-02T09:16:26Z), at head `8d6f091d` — reached after both inherited
reds this packet did not cause were fixed (PR #557, squash `5383e72c`; PR
#568, squash `d308c012`) and this packet's own `sequenced_after` live-pin
move landed in the same branch, per `tasks.md` §9.2's own dated
corrections. This paragraph's "stays gated" clause is therefore historical,
not current — filed forward rather than reworded, per this repository's
correction convention.
