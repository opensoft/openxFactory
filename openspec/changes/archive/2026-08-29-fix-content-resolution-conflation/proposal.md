---
code_surface: openxFactory (`scripts/hermes_runtime_validation/release.py` — `_blob_object_id` at `:312-316`, four lines converting every `ContentResolutionError` into `None`; its only caller `_surface_drift` at `:790-806`, whose comparison is `:796-798` and which is reached from `verify_promotion` at `:845`; and the sibling conflation `_CommitSource.exists` at `:401-405`, whose `False` is consumed at `:519`, `:532`, `:611` and `:621` to decide release membership and whether `contracts/manifest.yaml` is present at the commit. `scripts/hermes_runtime_validation/content.py` — `ContentResolutionError` at `:19-26`, whose `code` keyword already exists, defaults to `HRC-CONTENT-DEPENDENCY` and is read by NOTHING in this repository; and the one raise site among fifteen that means the path is absent from the tree, `:125` "exact Git path is unavailable". Plus regressions under `tests/hermes_runtime_contracts/` — `test_release_inventory.py` and `test_content_resolution.py`, over the established fixture pairs. NO change to the finding codes, their severities or their meanings; to the inventory schema, the membership closure, the digest rule or the mode comparison; to the CLI's exit codes; to what counts as reachable; or to any successful resolution's return value. `scripts/validate-contract-release.py:173` already catches `ContentResolutionError` alongside `ReleaseDependencyError`, so no CLI edit is required for either to fail closed.)
target_release: next additive contract bundle, allocated AT REALIZATION per `docs/contract-versioning-policy.md` and NOT reserved here — `contract-v2.0` is the declared bundle (`contracts/manifest.yaml:3`) and the `contract-v1.28` renumber sweep is the precedent for why a proposal must not claim a minor before merge order is known. **A BUNDLE IS OWED, AND THAT IS THE CONDITION THIS FIELD EXISTS TO NAME.** Established by PARSE rather than by `grep`: `contracts/releases/contract-v2.0.digests.yaml` loaded, its 192 entries walked, and `scripts/hermes_runtime_validation/release.py` present as `artifact_id: scripts-hermes_runtime_validation-release.py`, `type: validator`, `git_mode: 100644`, `digest: sha256:660e55ca7e6896ea24106483b926e1919a0cb195ef8b9a700a3522f1f393f6b0` — which is EXACTLY what the tree carries today, re-verified here by `sha256sum` of the working file. `scripts/hermes_runtime_validation/content.py` is a member on the same terms, so a fix that touches both files still owes ONE cut rather than two. Neither file is in the editorial set, which `scripts/doc_health/release_inventory.py:62-66` declares as exactly `contracts/CHANGELOG.md`, `contracts/manifest.yaml` and `contracts/README.md`; editing a non-editorial member without cutting leaves the declared inventory describing bytes the repository no longer holds, which `release-surface-integrity` names a defect and doc-health's release-inventory-drift family reports at `error`. THE PRECEDENT IS EXACT RATHER THAN ARGUED: `contract-v1.44` was cut on 2026-08-26 as an additive re-realization for PRECISELY this cause, on PRECISELY this file, by `fix-release-reachability-race` — the packet whose § 6.3 recorded the defect this change fixes — and `contract-v1.10` before it for the same reason (`contracts/CHANGELOG.md:2170-2185`). The class is additive: no schema moves, `contract_schema_version` is unchanged, no contract instance valid at `contract-v2.0` is narrowed, and every consumer pinned there stays conformant until it upgrades. The archive gate is therefore merge-plus-green PLUS the cut: `python3 -m pytest tests/hermes_runtime_contracts` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and manifest / changelog / digest inventory / verified annotated tag agreeing on the new bundle. The change ships ACTIVE and archives only after that. THIS COUPLING IS WHY THE PACKET IS SEPARATE FROM ITS SIBLING (OD-1): `fix-pin-value-boundary-and-sentinel-split` touches no inventory member at all and can archive on a green suite alone.
Status: ratified
Ratified: 2026-08-28 by Brett — in-session selection of the orchestrating session's recommended option, verbatim: "lets do all 3 in order". The recommendation this selected was the orchestrating session's own wording, "the measured-latents bundle", and the two voices are kept apart deliberately rather than merged into one quotation. THE SAME ACT IS CITED BY `fix-pin-value-boundary-and-sentinel-split`: one selection admitted all three defects, and the two packets exist because of a decision the authoring session took afterwards. THE CITATION COVERS THE DECISION TO FILE AND NOTHING ELSE. AS FIRST WRITTEN this line continued "the six decisions in § Orchestrator decisions below were taken by the authoring session under standing patterns, are NOT covered by this citation, and are flagged there for veto, as are the four questions in § Open Questions" — true at authoring and now historical: **A SECOND ACT LATER THE SAME DAY CLOSED THE VETO WINDOW.** All six § Orchestrator decisions were CLEARED AS AUTHORED and all four § Open Questions RULED on 2026-08-28, by a four-question multi-choice put to Brett by the orchestrating session over pull request #463 and relayed the same day; he took the packet's recommendation on every question, the re-sequencing OD-1 flagged was accepted on the record, the merge was approved on green to be performed by the orchestrating session rather than this one, and BOTH realizations were pre-commissioned to dispatch in order with the sibling first and this packet second. THE TWO ACTS STAY DISTINCT ON PURPOSE, because they authorized different things: this citation ADMITTED the packet, and the later ruling CLOSED the veto window and moved no delta text. No approving OpenSpec change exists to name, so the citation takes the record spelling `sanction-ratified-record-spelling` sanctioned for exactly that case, and clears its three-way floor on all three axes: approver (`by Brett`), date (`2026-08-28`), and a resolvable record path (this file, § Orchestrator decisions and § Open Questions).
Proposed: 2026-08-28
Origin: Follow-up § 6.3 of the archived `2026-08-26-fix-release-reachability-race`, recorded there as measured-and-deliberately-not-fixed: "`_blob_object_id` … converts every `ContentResolutionError` into `None`, so 'the blob is absent at this commit' and 'this commit does not exist' are the same value to its callers … the conflation itself survives, and it is the kind of thing that makes the next defect in this file hard to read." Re-measured on the day of filing, the conflation is wider than two conditions and its caller turns it into a verdict.
---

# Proposal: fix-content-resolution-conflation

## Why

**The release verifier can report a release surface clean without having read
it.**

```python
def _blob_object_id(repo: Path, commit: str, path: str) -> str | None:
    try:
        return resolve_git_object(repo, commit, path).blob_oid
    except ContentResolutionError:
        return None
```

`resolve_git_object` reaches fifteen distinct refusals. Exactly one of them —
"the path is not in this commit's tree" — is a fact about the release, and it is
the only one for which `None` is the right answer. The other fourteen say the
commit is not in the store, the repository will not open, git will not run, the
read timed out, the argument was malformed, or the resolver refused an unsafe
read. All fifteen become `None`.

Its only caller compares two of those answers:

```python
        if _blob_object_id(repo_root, commit, path) != _blob_object_id(
            repo_root, main_oid, path
        ):
```

So a failure on ONE side manufactures a `HGR-RELEASE-SURFACE-DRIFT` finding out
of an environment fact, and a failure on BOTH sides makes two `None`s compare
equal and reports the surface **undrifted** — a pass reached by reading neither
blob. The quiet direction is the dangerous one: it emits nothing, so nothing
notices.

The same file already carries promoted canon forbidding exactly this reasoning
one layer up. `shared-contract-ownership`'s "The reachability outcome names
which condition was observed" says a verdict invented from an absence is wrong
in both directions, and that "a reason that guesses is worse than a reason that
names". That requirement governs the ANCESTRY question. Nothing governs the
CONTENT question, and the content question is answered by flattening fifteen
conditions into one value.

## What was measured

All measurements taken 2026-08-28 in a fresh worktree off `origin/main` at
`6612d3239cbc99b73eb32cf76a861929aa901276`.

### 1. Fifteen raise sites, one of them the data answer

`grep -n "raise ContentResolutionError" scripts/hermes_runtime_validation/content.py`
→ **15 sites, 14 distinct messages** (two share "repository path is not
canonical"). Every one is reachable from `resolve_git_object`, which calls
`_repository`, `normalize_repository_path` and `_git` in turn. Exactly one,
`content.py:125` "exact Git path is unavailable", is reached when `ls-tree`
resolved the commit's tree and the path was not in it.

### 2. Six conditions, one value, run against this repository

`_blob_object_id` called directly, with the underlying resolver's message
captured beside each result:

| condition | underlying refusal | `_blob_object_id` |
| --- | --- | --- |
| blob genuinely absent at this commit | `exact Git path is unavailable` | `None` |
| the COMMIT does not exist | `exact Git object is unavailable` | `None` |
| the repository path is not a repository | `Git repository is unavailable` | `None` |
| the path is a DIRECTORY, not a regular file | `Git path is not a supported regular file` | `None` |
| the path is not canonical | `repository path contains a forbidden segment` | `None` |
| the revision is not a full object id | `revision must be a full Git object ID` | `None` |
| **a real member** | — | `47dc4022e2f7…` |

The first row is the only one that means anything about the release.

### 3. What the caller does with it

`_surface_drift` (`release.py:790-806`) builds its path set from
`RELEASE_SURFACE_PATHS` — `contracts/manifest.yaml`, `contracts/CHANGELOG.md`,
`contracts/README.md`, `contracts/hermes-runtime/README.md`,
`docs/contract-versioning-policy.md` — plus every release inventory listed at
either commit, and compares the two blob identities at `:796-798`. Two failures
therefore compare equal. **A clean surface report is indistinguishable from two
unread surfaces.**

**HOW REACHABLE IS IT, HONESTLY.** § 6.3 of the archived race packet noted that
its own § 2.5 removed the reachable path to the "commit does not exist" case, by
resolving the remote operand before anything reads it. That is still true, and
this packet does not claim otherwise. What remains reachable is not
hypothetical:

* **Environment.** `content._git` runs with `timeout=30` and converts `OSError`
  and `TimeoutExpired` into `ContentResolutionError`. A slow or contended store
  fails BOTH sides and reports the surface clean.
* **Committed data.** A release-surface path replaced at one of the two commits
  by a directory or a nested repository link takes the "not a supported regular
  file" refusal — a deliberate safety refusal — and it is silently read as
  absence. No environment failure is required for this one.

### 4. A sibling conflation of the identical shape

`_CommitSource.exists` (`release.py:401-405`) returns `False` for every
`ContentResolutionError`. Its four callers use that answer as data: `:519` and
`:532` decide whether a validator or an extra is a release member, `:611`
decides whether `contracts/manifest.yaml` exists at the commit, `:621` decides
membership for a listed path. **An environment failure at `:611` reports the
manifest ABSENT** — a verdict about the release from a fact about the machine.
Measured here rather than inherited; § 6.3 named only `_blob_object_id`.

### 5. The mechanism the fix can use, and the one it cannot

`ContentResolutionError.__init__` already takes a `code` keyword, defaulting to
`HRC-CONTENT-DEPENDENCY`. Swept: **no code in this repository reads
`ContentResolutionError.code`, and the string `HRC-CONTENT-DEPENDENCY` appears
nowhere but its own default.** So declaring a distinct code at `content.py:125`
is purely additive and changes no observed surface. Matching the error MESSAGE
instead was considered and rejected (OD-4) — a message is prose, and a near-miss
match silently reclassifies a safety refusal as release data, which is the same
hazard the sentinel vocabulary refuses near-miss spellings for.

`ReleaseDependencyError` and `ContentResolutionError` are both `RuntimeError`
with `exit_code = 2`, and `scripts/validate-contract-release.py:173` catches
both, so either fails closed through the CLI with no CLI edit.

### 6. The bundle, by parse

`contracts/releases/contract-v2.0.digests.yaml` loaded with a YAML parser, 192
entries walked. `scripts/hermes_runtime_validation/release.py`: **present**,
`type: validator`, `digest: sha256:660e55ca…`, which is exactly `sha256sum` of
the tree's copy today. `scripts/hermes_runtime_validation/content.py`:
**present**, same terms. The editorial set is three files and neither is in it.
**A cut is owed**, and the minor is not reserved here.

## What this changes

1. **Two ADDED requirements on `shared-contract-ownership`**: a content
   resolution reduced to presence or identity names the condition it observed
   (four scenarios), and each distinguished condition is pinned by an executable
   proof (three scenarios). The second mirrors the sibling family's own proof
   requirement, which exists because the reachability defect was invisible to
   the suite — and so is this one.
2. **`content.py:125` gains a declared code** naming the absent-path condition.
   Additive; nothing reads codes today.
3. **`_blob_object_id` returns `None` for that condition alone** and fails closed
   for the rest, with a reason naming what failed rather than what it concluded.
4. **`_CommitSource.exists` gets the same treatment**, because leaving it would
   ship a requirement its own file violates four lines away (OD-3, OD-5).
5. **An additive contract bundle cut rides the realization** — manifest bump,
   changelog entry, rebuilt inventory, `verify-commit`, and the post-merge
   `verify-promotion` plus annotated tag, on the `contract-v1.44` order.

## What this deliberately does not change

* **No successful resolution moves.** Same return value, same comparison, same
  finding codes, same severities, same exit codes.
* **No finding code is added, removed or re-scoped.** The refusals are
  dependency refusals, which is where unavailable dependencies already go.
* **`_is_ancestor` stays byte-unchanged**, as `fix-release-reachability-race`
  § 2.4 protected it.
* **`HGR-RELEASE-PATH-UNRESOLVABLE` at `:713-719` is NOT touched** — see the
  named follow-up below, and OD-3 for why the requirement is scoped so that
  leaving it is conforming rather than a self-violation.
* **No schema moves**, so the cut is additive rather than a major.

### Named follow-ups, out of scope here

1. **`HGR-RELEASE-PATH-UNRESOLVABLE` (`release.py:713-719`) converts every
   `ContentResolutionError` from `read_member` into a finding about the
   inventory path.** Measured here, not inherited. It is a milder shape than the
   two this packet fixes — it emits a named finding rather than silence — but it
   still turns an environment failure into a verdict about the release. It is
   left because changing it changes what a PUBLISHED finding code means to
   consumers reading verifier output, which is a contract question rather than a
   defect fix, and folding it in would make a four-line fix into a compatibility
   discussion.
2. **The wider sweep of `scripts/hermes_runtime_validation/` for the same
   pattern**, which `fix-release-reachability-race` § 6.1 opened for the
   reachability layer and named `consumer_handoff.py` as the next candidate.
   This packet measured `release.py` and claims nothing about the rest, on that
   packet's own rule: a sweep asserted without measurement is the same species
   of unearned answer these packets are about.
3. **The eleven-minute exposure window** of § 6.2, unmoved.

## Orchestrator decisions, cleared 2026-08-28 (authored: flagged for veto)

**ALL SIX CLEARED AS AUTHORED — Brett, 2026-08-28.** Ruled by a four-question
multi-choice put to him by the orchestrating session over pull request #463 and
relayed the same day; on every question he took the packet's own recommendation.
OD-1 (the two-packet split, **with the re-sequencing of 1, 2, 3 into {1, 3} then
{2} accepted on the record**), OD-2 (the capability home and the all-ADDED
two-requirement shape), OD-3 (the obligation scoped to presence-and-identity
reductions), OD-4 (a declared code rather than a matched message), OD-5 (fixing
`_CommitSource.exists` alongside the named surface) and OD-6 (the cut declared
without a minor reserved) all stand exactly as written below. No verbatim
wording of the ruling reached this session, so none is quoted — the approver,
the date, the mechanism and the selections are recorded instead, which is what
the origin requirement asks for.

**THE CLEARANCE MOVED NOTHING.** Every ruling took the recommendation as
authored, so not one word of `specs/shared-contract-ownership/spec.md` changed,
neither requirement was added, removed or reworded, and no scenario moved. This
is stated rather than left to inference, because a clearance that is silent
about delta text is indistinguishable from a clearance nobody checked.

**THE ORIGINAL FLAGGED TEXT IS KEPT BELOW AS MARKED HISTORY** rather than
rewritten, because what was flagged and why is the part a later reader needs;
the per-decision clearance markers say which act closed each one. **THIS ACT IS
DISTINCT FROM THE COMMISSION RECORDED IN § Ratified**: that one admitted the
packet, this one closed the veto window.

**THREE FURTHER THINGS THE SAME ACT SETTLED, recorded here because they govern
what happens next rather than what the packet says.** (1) **MERGE ON GREEN IS
APPROVED, and the merge is the ORCHESTRATING SESSION'S act, not the authoring
session's** — this session pushes and stops. (2) **BOTH REALIZATIONS ARE
PRE-COMMISSIONED TO DISPATCH IN ORDER once the filing lands:
`fix-pin-value-boundary-and-sentinel-split` FIRST, realized and archived on its
own green, and THIS PACKET SECOND** — with its realization and its CANDIDATE
inventory built in the realization pull request, and `verify-promotion` plus the
annotated tag left to the post-merge act, exactly as the `contract-v1.44`
precedent discharged them. That ordering is OD-1 doing what it was argued for.
(3) **THE BUNDLE STATE WAS RE-AFFIRMED AT THE RULING RATHER THAN CARRIED FROM
THE FILING: `contract-v2.0` is current, and the cut allocates the NEXT number at
merge order** — no minor is reserved by this act any more than by OD-6, and the
collision check of `tasks.md` § 4.1 still runs before a number is claimed.

**OD-1 — THIS PACKET IS ONE OF TWO, SPLIT FROM THE APPROVED THREE-DEFECT SET ON
THE CONTRACT-BUNDLE BOUNDARY.**
**CLEARED 2026-08-28 AS AUTHORED, AND THE RE-SEQUENCING WAS ACCEPTED WITH IT** —
which is the half that mattered, because it is the only part of this decision
that changed what was approved. Full argument at
`fix-pin-value-boundary-and-sentinel-split`'s OD-1 and its `design.md` § 1,
where the rejected one-packet alternative is argued in full. The half that
belongs here: this packet's surface is an inventory member at the digest the
tree holds, its sibling's three files are members of nothing, and the
`contract-v1.44` precedent records that a cut's final acts — `verify-promotion`
and the annotated tag — are not the authoring session's to perform. Bundling
would hold two zero-cost fixes behind a human-gated contract tag. **The cost is
stated rather than buried:** Brett said "in order", and the split re-sequences
the approved 1, 2, 3 as {1, 3} then {2}.

**OD-2 — THE DELTA LANDS ON `shared-contract-ownership`, ALL ADDED, TWO
REQUIREMENTS.** **CLEARED 2026-08-28 as authored.** That capability owns the release verifier surface — SCO-002 and
the three requirements `fix-release-reachability-race` added there — and it
stands at 10 requirements; this makes 12. No active change carries a
`shared-contract-ownership` delta — checked across the 24 active changes that
predate this pair, by enumerating every `specs/<capability>/` directory in the
active set rather than by reading a list — so there is no collision in either
direction. The two-requirement shape copies the
sibling family deliberately: it separated the mechanics from the proofs
precisely because the defect it closed was invisible to the suite, and this one
is invisible to the suite today. **Rejected:** a `MODIFIED` block over "The
reachability outcome names which condition was observed", which would restate
promoted prose wholesale to widen it from ancestry to content, and put canon at
the mercy of archive order. **Also rejected:** one requirement with the proof
obligations folded in as scenarios, which would leave the proofs as a
consequence of the mechanics rather than part of the obligation — the exact
distinction the sibling family drew and gave its reason for.

**OD-3 — THE OBLIGATION IS SCOPED TO RESOLUTIONS REDUCED TO PRESENCE OR
IDENTITY, WHICH IS NARROWER THAN "EVERY CONTENT RESOLUTION".**
**CLEARED 2026-08-28 as authored**, so `HGR-RELEASE-PATH-UNRESOLVABLE` stays a
named follow-up (`tasks.md` § 7.1) and the requirement's scope is unchanged.
The requirement
governs the places where a resolution collapses into a boolean or a blob
identity — `_blob_object_id` and `exists` — and does not reach a resolution that
already produces a named finding, which is what `:713-719` does. THE REASON IS
THAT A PACKET MUST NOT SHIP CANON ITS OWN FILE VIOLATES. Written broadly, the
requirement would be breached by `:713-719` on the day it promoted, and a
requirement whose first reader can find a live counterexample in the same file
teaches that canon here is aspirational. **Rejected:** the broad wording plus a
disposition, which would make an unfixed site a paperwork problem instead of a
scoping decision.

**OD-4 — THE DISTINCTION IS CARRIED BY A DECLARED CODE ON THE RESOLVER, NOT BY
MATCHING ITS MESSAGE.** **CLEARED 2026-08-28 as authored**, and Q2 below settles
that it is ONE code rather than fifteen. `ContentResolutionError` already takes a `code`; nothing
reads it; `content.py:125` gains a distinct one. **Rejected: matching the string
"exact Git path is unavailable".** It would work today and fail silently the
first time somebody improves the message — reclassifying a safety refusal as
release data, in the direction that produces no output. It is also the exact
hazard the promoted sentinel canon names for near-miss spellings: "a near-miss
spelling is precisely the condition under which every consumer guarding on the
exact string already fails". **Also rejected:** a separate probe — resolve the
commit first, then the path — which doubles the git invocations on the ordinary
path and still cannot separate the twelve remaining conditions.

**OD-5 — `_CommitSource.exists` IS FIXED HERE ALTHOUGH § 6.3 DID NOT NAME IT.**
**CLEARED 2026-08-28 as authored**, so the widening of the inherited follow-up
stands and `tasks.md` § 2.4 is in scope.
Identical shape, same file, four lines away, and one of its four callers decides
whether `contracts/manifest.yaml` is present at the commit. Leaving it would
ship a requirement with a live counterexample beside the site it was written
for. **Rejected:** deferring it to its own packet, which is how a two-line fix
becomes a second bundle cut. **Recorded rather than smoothed over:** this widens
the inherited follow-up, and the widening is the authoring session's, on a
measurement § 6.3 did not make.

**OD-6 — THE BUNDLE CUT IS DECLARED AT FILING AND NO MINOR IS RESERVED.**
**CLEARED 2026-08-28 as authored, and re-affirmed by the same act**, which
restated that `contract-v2.0` is current and that the cut allocates the next
number at merge order.
`target_release` states the cut, its cause, the parsed evidence of membership,
the additive class and the precedent; it names no number, because merge order
decides the next minor and the `contract-v1.28` renumber sweep is the precedent
for why a proposal must not reserve one. **Rejected:** naming `contract-v2.1`,
which is the collision this repository has already paid for once.

## Open Questions, all four ruled 2026-08-28

All four were ruled by the same four-question multi-choice recorded in
§ Orchestrator decisions, and on all four Brett took the packet's recommendation.
No verbatim wording of the ruling reached this session, so none is quoted —
approver, date, mechanism and the option selected are stated instead.

**NONE OF THE FOUR MOVED DELTA TEXT**, and that is a measurement rather than an
assumption: all four ruled answers are realization mechanics — which exception
class carries the refusal, how many codes the resolver declares, which fixtures
the proofs reuse, and how the failing condition is driven — and both
requirements were written to govern the OUTCOME rather than the mechanism. The
delta is byte-unchanged from the filing. **Each question's original text is kept
verbatim beneath its ruling**, because a recommendation that was accepted is the
argument for the rule now standing.

**Q1 — RULED 2026-08-28: THE REFUSAL IS `ReleaseDependencyError`, WRAPPING THE
ORIGINAL WITH `from`.** The recommendation was taken as authored. **WHAT MOVED:
nothing.** The requirement asks for a fail-closed dependency refusal whose reason
names the condition observed and does not name a class, so the ruling settles the
mechanism `tasks.md` § 2.3 carried as conditional and leaves the obligation as
written. Both classes already exit 2 and both are already caught at
`validate-contract-release.py:173`, so no CLI edit follows from it either.
*Question as authored:* Should the refusal be `ReleaseDependencyError` or the `ContentResolution
Error` re-raised unwrapped? Both are `RuntimeError` with `exit_code = 2` and
`validate-contract-release.py:173` catches both, so both fail closed.
**RECOMMENDATION: `ReleaseDependencyError`, wrapping the original with `from`.**
The promoted sibling requirement puts the fail-closed refusal in the dependency
class by name and asks that the reason name the retrieval; wrapping keeps the
release verifier's refusals in one class while `from` preserves the resolver's
own message for the reader.

**Q2 — RULED 2026-08-28: ONE CODE FOR THE ABSENT-PATH CONDITION, NOT FIFTEEN.**
The recommendation was taken as authored. **WHAT MOVED: nothing.** The
requirement treats the other fourteen as one outcome by design — "the question
could not be asked" — so a single declared code is exactly what it needs, and
`tasks.md` § 7.4 keeps the open item for the day a second caller needs to
distinguish two of the fourteen. That is the evidence a wider vocabulary would
require, and it does not exist yet.
*Question as authored:* Should `content.py` declare one absent-path code, or a code per
condition? A code per condition would let every caller distinguish everything.
**RECOMMENDATION: one code for the absent-path condition, and nothing more.**
That is the only distinction the requirement needs; the remaining fourteen are
all "the question could not be asked", which the requirement treats as one
outcome by design. A code per raise site would be a vocabulary nothing consumes,
which is the drift the sentinel declaration's second direction exists to report.

**Q3 — RULED 2026-08-28: REUSE THE EXISTING FIXTURES**, with the release-surface
proofs on the `_bare_origin` / `_repo_with_committed_inventory` pair and the
resolver proofs in `test_content_resolution.py`. The recommendation was taken as
authored. **WHAT MOVED: nothing** — the proof requirement names the conditions a
proof must establish and deliberately names no fixture, so the ruling settles
`tasks.md` § 3.5 without touching canon.
*Question as authored:* Should the offline and unavailable-store proofs reuse the race packet's
`_bare_origin` / `_repo_with_committed_inventory` fixture pair? They already
exist in `tests/hermes_runtime_contracts/test_release_inventory.py`.
**RECOMMENDATION: reuse them for the release-surface proofs and add the resolver
proofs to `test_content_resolution.py`, which is where the fifteen refusals
already live.** Two homes, each beside the code it proves.

**Q4 — RULED 2026-08-28: DRIVE THE CONDITION BY ARGUMENT, AND SAY SO IN THE
PROOF.** The recommendation was taken as authored. **WHAT MOVED: nothing.** The
requirement's third scenario asks for a refusal when both sides fail and is
silent on how they are made to fail, which is deliberate — and the pinning rule
it carries (remove the distinction, watch the proof fail) is
mechanism-independent, so a proof driven by argument is pinned exactly as
tightly as one driven by a timeout. Settles `tasks.md` § 3.6.
*Question as authored:* Does the "both sides fail" proof need a real slow or broken store, or may
it drive the condition by argument? A genuine timeout is slow and flaky; a
non-canonical path or an absent repository reaches the same branch instantly.
**RECOMMENDATION: drive it by argument, and say so in the proof.** The
requirement is about the DISTINCTION, not about any one way of failing, and the
sibling family's rule — a proof must be able to fail for the right reason — is
satisfied by removing the distinction and watching the proof fail, which is
mechanism-independent.

## Impact

* **Capability:** `shared-contract-ownership` 10 → 12 requirements.
* **Consumers:** none for the code path. The bundle cut is additive, so every
  consumer pinned at `contract-v2.0` stays conformant until it upgrades.
* **Release surface:** an additive cut is owed and is part of the archive gate,
  not of the merge (OD-6).
* **Risk:** the fix converts silent Nones into refusals, so its failure mode is
  a NOISIER verifier rather than a quieter one — which is the right direction,
  and is bounded by the requirement's insistence that a successful resolution
  moves not at all.
* **Sibling:** `fix-pin-value-boundary-and-sentinel-split`, defects 1 and 3 of
  the same commissioned set (OD-1).
