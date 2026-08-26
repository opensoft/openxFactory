---
code_surface: openxFactory (`scripts/hermes_runtime_validation/release.py` — `_is_ancestor` at `:195-202` and its 128-branch raise at `:200`; `_ls_remote` at `:184-193`, the helper that produces the live object id; `verify_promotion`'s remote read at `:718` and its ancestor check at `:723`; `_surface_drift` at `:682-698`, reached from `:732`, whose `_CommitSource(repo_root, main_oid).list_release_inventories()` at `:686` and `_blob_object_id(repo_root, main_oid, path)` at `:689` read the SAME live object id out of the same local store; `verify_tag`'s remote reads at `:781` and `:803`, its ancestor check at `:807`, and `_verify_release_at(repo_root, peeled_commit, tag)` at `:816`, which reads the remote-derived TAG object locally the same way. Plus `tests/hermes_runtime_contracts/test_release_inventory.py` — new regression cases over the established `_bare_origin` / `_repo_with_committed_inventory` fixture pair at `:116-133` and `:462`. NO change to the finding codes, the inventory schema, the membership closure, the digest rule, the mode comparison, the CLI's exit codes, or what counts as reachable.)
target_release: implemented — realized on the openxFactory main line as pull request #390 (merged 2026-08-26T21:21:13Z, merge commit `8894901c192a231dcf77bf9360764ce98a12a822`, re-verified an ancestor of `origin/main` at the archive) and green there — `pytest-suite` and `wallet-validation` both concluded `success` on the final head `d548d04d`, with the local full suite at 6497 passed / 0 failed and `tests/hermes_runtime_contracts` at 508 passed — AND cut as the additive **`contract-v1.44`** bundle the same day: inventory built twice byte-identical (`entries=192`, unchanged membership), `verify-commit` pass, `verify-promotion --commit 8894901c --remote origin --tag contract-v1.44` pass on the merge commit before the tag, the annotated tag `contract-v1.44` published on `8894901c` with the message "contract-v1.44 — additive: the release verifier resolves its remote operand before it compares", `verify-tag --remote origin --tag contract-v1.44` pass (re-run at the archive, exit 0), and the aggregation submodule pointer synced at `901bd04a`, whose gitlink reads that same sha. REWRITTEN AT THE ARCHIVE, 2026-08-26, from the forward-looking value that follows, under the `implemented — <evidence>` correction shape ruled 2026-08-22 for register C1 of `docs/archive-record-discrepancies.md`: a value naming a release still to be allocated is self-contradicting on an archived change, because the archive gate admits a change only on the evidence such a value says is still owed. The authored text is kept verbatim rather than discarded, because it is the argument for why a bundle was owed at all. AS AUTHORED: next additive contract bundle (allocated at realization per `docs/contract-versioning-policy.md`; `contract-v1.43` is the declared bundle and a proposal MUST NOT reserve a minor number before merge order is known). A BUNDLE IS OWED, and this is the one thing that separates this change from its doc-only siblings: `scripts/hermes_runtime_validation/release.py` is itself a NON-EDITORIAL member of the declared bundle's release digest inventory (`contracts/releases/contract-v1.43.digests.yaml:993-996`, `type: validator`, `digest: sha256:d149a34b...`, which is exactly what the tree carries today — verified 2026-08-26). Editing it without cutting a bundle leaves the declared inventory describing bytes the repository no longer holds, which `release-surface-integrity` names a defect in any non-editorial member and doc-health's release-inventory drift family reports at `error`. The precedent is exact rather than argued: `contract-v1.10` was cut as a superseding additive re-realization for PRECISELY this cause — finding F-U3 hardened release membership and changed this same file, so the frozen `contract-v1.9` inventory stopped reproducing the tree (`contracts/CHANGELOG.md:2170-2185`). The class is additive: no schema moves, `contract_schema_version` is unchanged, no contract instance valid at `contract-v1.43` is narrowed, and every consumer pinned there stays conformant until it upgrades. The archive gate is therefore merge-plus-green PLUS the cut: `python3 -m pytest tests/hermes_runtime_contracts` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and manifest / changelog / digest inventory / verified annotated tag agreeing on the new bundle. The change ships ACTIVE and archives only after that.
Status: ratified
Ratified: 2026-08-26 by Brett — in-session commissioning of the filing, verbatim: "file the release-inventory CI race fix change". The citation covers the DECISION TO FILE THIS CHANGE and nothing else; the four decisions in § Orchestrator decisions below were taken by the authoring session under standing patterns and are NOT covered by this citation. AS FIRST WRITTEN this line ended "and are flagged there for veto" — that was true at authoring and is now historical: Brett cleared all four the same day, as authored, by a separate ruling recorded in full at § Orchestrator decisions. The two acts stay distinct on purpose, because they authorized different things: this citation authorized the FILING, the clearance closed the VETO WINDOW, and neither reaches Q1, Q3 or Q4. No approving OpenSpec change exists to name for either, so both cite the record in the spelling `sanction-ratified-record-spelling` sanctioned for exactly that case, clearing its three-way floor on two axes rather than the one it needs: approver (`by Brett`) and date (`2026-08-26`).
Proposed: 2026-08-26
Origin: The 2026-08-26 triage of openxFactory PR #372's continuous-integration history. The red had nothing to do with the branch under test — the same tree failed twice and passed once, and what changed between the three runs was what else merged to `main` while the suite was running.
---

# Proposal: fix-release-reachability-race

## Why

**The release verifier asks the remote a live question and answers it out of a
static object store.** Reachability — "is this candidate on published main?" —
is decided in two steps that do not belong together:

```python
    main_rows = _ls_remote(repo_root, remote, "refs/heads/main")   # the network
    ...
    if not _is_ancestor(repo_root, commit_oid, main_oid):          # the clone
```

`_ls_remote` returns the object id `refs/heads/main` points at ON THE REMOTE,
right now. `_is_ancestor` then runs `git merge-base --is-ancestor` INSIDE the
local clone, against an object the clone may never have seen. When main has
advanced since the clone was taken, that object is simply absent locally, and
`git merge-base` says so the only way it can:

```python
def _is_ancestor(repo: Path, ancestor: str, descendant: str) -> bool:
    result = _run_git(
        repo, "merge-base", "--is-ancestor", ancestor, descendant, allow_failure=True
    )
    if result.returncode not in (0, 1):
        raise ReleaseDependencyError("commit reachability could not be determined")
    return result.returncode == 0
```

Exit 0 means reachable, 1 means not reachable, and 128 means the question could
not be asked. The guard is correct to refuse on 128 — a verification that
cannot resolve its own operands must not resolve to a pass, and nothing in this
change weakens that. What is wrong is that the verifier walks into 128 on
purpose, by mixing an operand it fetched over the network with a store it never
updated.

**The consequence is a verification whose verdict depends on other people's
merges.** `tests/hermes_runtime_contracts/test_release_inventory.py::test_validate_candidate_passes_on_the_realized_repository`
runs `validate_realization(ROOT, ...)` against the real repository, which
reaches `verify_tag` and therefore the ancestor check. Any run — pull request or
`main` — that has a commit land on `main` inside its window reds, on a tree that
is otherwise perfectly healthy.

## What was measured

All of it on 2026-08-26, from openxFactory PR #372's own runs. That pull request
was a doc-only change and touched neither the verifier nor its test. Run
`32934803039`, three attempts, ONE head commit — `5c10ce6de8a127866667ccbd53ef2509205d2951`
for all three:

| attempt | window | merged to `main` inside it | verdict |
| --- | --- | --- | --- |
| 1 | 05:37:56Z -> 05:49:18Z (10:56 of pytest) | **#365 at 05:46:00Z** (`02477d40`) | **failed** |
| 2 | 05:52:35Z -> 06:04:47Z (11:50 of pytest) | **#374 at 05:54:06Z** (`26e1e021`) | **failed** |
| 3 | 06:07:45Z -> 06:20:21Z | none | **passed** |

Both failures are the same single test and the same single line:

```text
>           raise ReleaseDependencyError("commit reachability could not be determined")
E           scripts.hermes_runtime_validation.release.ReleaseDependencyError: commit reachability could not be determined
FAILED tests/hermes_runtime_contracts/test_release_inventory.py::test_validate_candidate_passes_on_the_realized_repository
1 failed, 6205 passed, 18 skipped, 338 deselected, 15 subtests passed in 656.42s (0:10:56)
```

Attempt 2's tail is identical but for its clock: `1 failed, 6205 passed, 18
skipped, 338 deselected, 15 subtests passed in 710.13s (0:11:50)`. Attempt 3,
same tree, no merge in the window, green.

**Then it reproduced on this branch, under control, while this packet was being
authored.** This is the measurement that turns the timeline above from a strong
inference into a demonstration, and it was not planned — the worktree simply sat
still long enough for `main` to move:

```text
$ python3 -m pytest tests/hermes_runtime_contracts -q -m "not postgres"
1 failed, 498 passed, 338 deselected in 276.63s (0:04:36)
FAILED tests/hermes_runtime_contracts/test_release_inventory.py::test_validate_candidate_passes_on_the_realized_repository
scripts/hermes_runtime_validation/release.py:200: ReleaseDependencyError

$ git ls-remote origin refs/heads/main
c1c9c0dcd721b8597bea4462e22721d7e03d3ab3	refs/heads/main
$ git cat-file -e c1c9c0dcd721b8597bea4462e22721d7e03d3ab3^{commit}
fatal: Not a valid object name ...        # exit 128 — the object is not here

$ git fetch origin c1c9c0dcd721b8597bea4462e22721d7e03d3ab3
 * branch              c1c9c0dc... -> FETCH_HEAD          # exit 0
$ git cat-file -e c1c9c0dcd721b8597bea4462e22721d7e03d3ab3^{commit}
                                          # exit 0 — now it is

$ python3 -m pytest ...::test_validate_candidate_passes_on_the_realized_repository -q
1 passed in 44.44s
```

Nothing between the red and the green touched the working tree. The only edit
was to the object store, and the edit was one `git fetch` of one object id. That
sequence is simultaneously the reproduction, the diagnosis, and a working proof
of the fix this proposal chooses — which is also why Q1's recommendation below is
now backed by a measurement rather than a guess: `git fetch <remote> <oid>`
against the canonical remote returned 0 for an object advertised under no ref
the clone tracked.

So "it passes locally" is true only of a clone that has fetched recently. The
defect is not a property of continuous integration; continuous integration is
merely where clones are always exactly as old as the run.

The window is not a narrow one. The suite takes about eleven minutes, and the
checkout that seeds the object store is taken at its start, so the exposure is
the whole run. On a day when this repository merged five changes to `main`
between 05:12Z and 06:21Z, two of three attempts hit it.

## The mechanism, stated exactly

Three places read a REMOTE-DERIVED object id out of the LOCAL store, and every
one of them can meet the same absence:

1. **`verify_promotion`, the candidate-review path.** `main_oid` comes from
   `:718` and is used at `:723` by `_is_ancestor`. This is the site the finding
   `HGR-RELEASE-CANDIDATE-UNREACHABLE` hangs off.
2. **`verify_promotion`, the release-surface comparison.** The same `main_oid`
   is passed to `_surface_drift` at `:732`, which builds a `_CommitSource` over
   it at `:686` — `git ls-tree` on an absent commit — and reads blobs from it at
   `:689`. Today `_is_ancestor` raises first, so this site is MASKED rather than
   safe. It matters for the choice of fix, and § 2 of `design.md` turns on it.
3. **`verify_tag`, both operands.** `main_oid` comes from `:803` and is used at
   `:807`; `peeled_commit` comes from the remote tag advertisement at `:781` and
   is used at `:807` and again at `:816`, where `_verify_release_at` reads the
   tag's tree and blobs locally. A tag published since the clone was taken is
   absent for exactly the same reason main's new tip is.

The two failures measured above came through path 3, because
`validate_realization` calls `verify_tag`. Path 1 is the one a release operator
meets at promotion time, and it carries the identical hazard.

## What this changes

1. **The compared object is made locally available before the comparison is
   made.** Reachability stops being answered against whatever the clone
   happened to hold. Where the object is absent, the verifier fetches it from
   the remote it just consulted and then answers.
2. **The three outcomes are told apart, and named.** A candidate genuinely not
   on published main is the existing refusal, unchanged, with its existing
   finding code. An object that cannot be made available — no network, no
   permission, a remote that will not serve it — is still the existing
   fail-closed error, but its reason names the FETCH that failed instead of
   announcing that reachability "could not be determined". Transient skew is
   neither: it resolves in the fetch and produces no finding at all.
3. **The two states are pinned by tests.** A fixture whose local "remote" has
   advanced beyond the clone is the regression for the skew; a fixture whose
   objects cannot be fetched is the regression for the fail-closed path. Both
   use the `_bare_origin` pattern this test module already establishes.

## What this deliberately does not change

- **Reachability keeps its meaning.** A candidate must still be reachable from
  the remote's `main`, and a tagged commit from published `main`. Only the
  mechanics of answering change. No finding code is added, removed, renamed or
  re-severitied, and `HGR-RELEASE-CANDIDATE-UNREACHABLE` and
  `HGR-RELEASE-TAG-UNREACHABLE` continue to fire on exactly the population they
  fire on today.
- **Fail-closed stays fail-closed.** An unanswerable question must never
  resolve to a pass. This change narrows the set of questions that are
  unanswerable; it does not soften what happens to the ones that remain.
- **No retry loop, no polling, no tolerance window.** The fix is one fetch of
  one named object, not a "try again later" that would make the verifier's
  runtime a function of the network.
- **The verifier's other refusals are untouched.** `remote main is
  unavailable`, `Git command is unavailable`, `exact commit is unavailable` and
  the whole digest/mode/membership family keep their current behaviour.
- **The test's existing tolerance is untouched.** `test_validate_candidate_passes_on_the_realized_repository`
  deliberately does not assert `== []`, because release members legitimately
  drift between cuts; that stays exactly as it is. This change is about the
  test being able to REACH its assertion, not about what it asserts.

## Family relation — the same defect, one surface over

This is the second instance in two days of ONE defect family: **a verification
that answers a question about LIVE state using PINNED or STALE state, and
reports the mismatch as a fact about the subject rather than about itself.**

`harden-ideation-readiness-check` (openxFactory PR #372, merged 2026-08-26) is
the sibling, and the two are worth reading together:

| | the sibling | this change |
| --- | --- | --- |
| live operand | the corpus and index as they sit in a working tree | the remote's current `refs/heads/main` |
| stale operand | an index pin (`source_revision`) no ref reaches | a clone's object store, fixed at checkout |
| what it produced | a `pytest.skip` whose stated reason was a guess | a `ReleaseDependencyError` blaming reachability |
| how it presented | a proof that never ran, invisibly green | a healthy tree, intermittently red |

The shapes are mirror images. The sibling made a verification honest by
REFUSING to answer from state it could not resolve; this change makes one honest
by RESOLVING the state before it answers. Both replace a message that guessed
at the cause with one that names the condition observed — the sibling's
`"(shallow clone?)"` conjecture and this one's `"could not be determined"` are
the same failure of diagnosis, and they send a reader to the same wrong place.

The family relation is not decoration. It is the argument for the requirement
below being about the MECHANICS of a verification rather than about release
semantics, and it is the reason § Named follow-ups asks whether the family has
more members.

## Orchestrator decisions, cleared 2026-08-26 (authored: flagged for veto)

**ALL FOUR CLEARED 2026-08-26, THE SAME DAY THEY WERE FLAGGED — Brett approved
every one as authored, and none was vetoed.** The ruling came as a four-question
multi-choice put to Brett by the orchestrating session on 2026-08-26 and relayed
to the authoring session the same day; on each question Brett selected the
recommended "keep" option: **OD-1** keep the ADDED-in-`shared-contract-ownership`
shape, **OD-2** keep fetch-before-check, **OD-3** keep the archive gate on the
bundle cut, **OD-4** keep real-fixture-first with the monkeypatch fallback. No
verbatim wording of the ruling reached the authoring session, so none is quoted —
the approver, the date, the mechanism and the option selected on each question
are stated instead, which is what this repository's own precedent asks for and
how `harden-ideation-readiness-check`'s admission is recorded. OD-1 through OD-4
are items 1 through 4 below, in that order.

**Nothing in the packet moves as a result.** All four decisions stand exactly as
authored, so the clearance required no edit to a requirement, a delta, a task, or
a design entry — the same shape openxFactory PR #307 recorded when Brett cleared
the two codex dispositions there ("the approval required no repo edit"). This
record exists so that the veto window is legibly CLOSED rather than merely
un-exercised: an unrecorded clearance and an unnoticed flag look identical six
weeks later.

**`.openspec.yaml`'s ORIGIN BLOCK IS DELIBERATELY NOT EDITED, and that is a
ruling-respecting choice rather than an oversight.** Its `approved_by` still ends
by saying the four decisions "are flagged for veto in the proposal's
§ Orchestrator decisions" — a pointer that now lands the reader on this
clearance, which is why leaving it costs nothing. What editing it would cost is
real: `release-realization`'s "Origin retention at archive" requires the archive
gate to verify that the origin declaration is UNCHANGED from ratification and to
FAIL on a mutation, making any rewrite a contested-class act. The sibling packet
did edit its origin, and the difference is the whole point — it was COMPLETING a
required field that stood blank, which the origin requirement demands be filled,
whereas this would be appending commentary to a pair that is already complete and
correct. A veto clearance is not origin provenance, so it is recorded where the
flagging lives instead.

**THE CLEARANCE COVERS EXACTLY THESE FOUR DECISIONS AND NOTHING ELSE.** Q1 (the
fetch's narrowness and its fallback) and Q3 (whether reconciled skew should be
observable) stay OPEN. Q4 stays a scope this change DECLINES rather than one that
has been ruled. Q2 is split by OD-4: its MECHANISM half is resolved — measure the
real fixture first, the monkeypatch fallback is authorized — and its MEASUREMENT
half is not discharged at all, because a ruling that a fixture may be used is not
a measurement that the fixture works. `tasks.md` § 3.3 stands undischarged.

**HISTORY, KEPT SO THE RESOLUTION IS LEGIBLE.** The paragraph below is the
section's original preamble, unchanged. It was true when written and is now
superseded by the clearance above; it is preserved rather than erased for the
same reason `.openspec.yaml`'s `approval_note` preserves why its approval pair
once stood blank.

> Authored by a delegated session against a commission to file. Brett's
> instruction authorized the FILING; every decision below was taken by the
> authoring session, is uncovered by that authorization, and is flagged for
> reversal. Reverting any one of them is an edit to this change, not a new one.

1. **The delta lands in `shared-contract-ownership`, all ADDED, nothing
   MODIFIED.** The reasoning and the two rejected homes are in `design.md`
   § 1. The short form: the promoted requirement that already governs this
   surface is "Contract version pinning" (`SCO-002`), whose text draws exactly
   the line this defect crosses — "Online Gate verification SHALL prove the
   annotated tag on the canonical remote; offline runtime verification SHALL
   resolve exact commit/tree/blob objects already present locally" — and whose
   scenarios `SCO-002-S02`/`S03`/`S04` are bound in
   `contracts/hermes-runtime/evidence-register.yaml` to the very tests that
   exercise `verify_tag` and `verify_promotion`. It is ALSO under `MODIFIED` by
   the active ratified change `add-hermes-customer-subject-runtime-contract`,
   which is why these are ADDED requirements rather than a second wholesale
   replacement of it.
2. **Fetch before the check, not retry on 128.** Recorded with its rejected
   alternatives in `design.md` § 2. The decisive fact is hazard site 2 above:
   retry-on-128 repairs `merge-base` and leaves `_surface_drift` to fail on the
   same absent object with a strictly worse message.
3. **A contract bundle is owed and the change archives only after the cut.**
   Stated in `target_release` above with the `contract-v1.10` precedent. The
   alternative — land the verifier fix and let the declared inventory describe
   bytes the tree no longer holds until some later cut re-baselines it — is
   precisely the state `release-surface-integrity` calls a defect, and its
   remedy clause forbids the shortcut of hand-editing the inventory to match.
4. **The offline case is proved by making the remote's objects unreadable
   rather than by patching the module.** `tasks.md` § 3.3 carries both the
   mechanism and its fallback, because the mechanism is the one part of this
   plan that has not been measured — see Q2.

## Open Questions

**Q1 — should the fetch be narrowed to the object, or may it be a ref fetch?**
Fetching the single object id (`git fetch <remote> <oid>`) is the precise
request and requires the remote to serve an unadvertised object, which many
configurations refuse; fetching the ref (`git fetch <remote> refs/heads/main`)
always works but brings history the verifier did not ask for and mutates the
clone's remote-tracking refs. **MEASURED 2026-08-26 against the canonical
remote**: `git fetch origin c1c9c0dcd721b8597bea4462e22721d7e03d3ab3` returned 0
for an object under no ref this clone tracked, and the previously-failing test
then passed (§ What was measured). So the narrow request works where it matters
most. **Recommendation: try the object, fall back to the ref, treat only the
failure of BOTH as the fail-closed case** — the measurement removes the doubt
about the primary path without asserting anything about remotes nobody has
tested, and the taxonomy requirement is written to permit exactly that without
naming a git incantation in canon. Ruling still wanted, because the fallback is
the part that decides whether a hardened or mirrored remote can be verified
against at all. **A cost argument points the same way**: the online realization
path is capped at 30 seconds twice over — `_run_git`'s per-invocation `timeout=30`
and `_run_cli`'s whole-invocation `timeout=30` in
`tests/hermes_runtime_contracts/test_validator_cli.py:104-113` — and that cap was
breached once under machine load while this packet was being authored
(`tasks.md` § 5.5). A single object is cheaper than a ref's history, and probing
with `git cat-file -e` first makes the already-current case free.

**Q2 — is the offline fixture mechanism sound?** `tasks.md` § 3.3 proposes
making the bare origin's `objects/` directory unreadable so that `ls-remote`
still advertises refs while `fetch` cannot serve them. That is a guess about how
`git upload-pack` behaves during advertisement over a local path, and it has NOT
been measured. If advertisement also fails, the fixture proves the wrong thing —
the "remote main is unavailable" path rather than the fetch-impossible path —
and the fallback is to monkeypatch `_run_git` to fail the fetch invocation only.
**Recommendation: measure first, monkeypatch second, and do not ship a fixture
that passes for the wrong reason.**

**MECHANISM HALF RULED (2026-08-26, Brett, via OD-4): the recommendation stands
— real fixture first, monkeypatch fallback authorized.** So the CHOICE between
the two mechanisms is no longer open. **THE MEASUREMENT HALF IS NOT DISCHARGED**,
and the ruling does not touch it: nobody has yet observed whether `git
upload-pack` can advertise refs over a local path whose `objects/` directory is
unreadable, and a ruling that a fixture MAY be used is not evidence that it
WORKS. `tasks.md` § 3.3 stands undischarged, including its instruction to
discard the fixture if it turns out to prove the "remote main is unavailable"
path instead.

**Q3 — should the mid-run-skew case be observable at all?** Requirement 2 makes
transient skew produce no finding, which is right for a verifier whose output is
a findings list. But a run that silently fetched a newer main is a run whose
answer is about a `main` different from the one it started with, and that is
worth a line in a log even if it is not worth a finding. **Recommendation: leave
it unspecified here.** Canon should not mandate a log line, and the
implementation is free to emit one.

**Q4 — does the same hazard exist in `consumer_handoff.py`?** Named as a
follow-up below rather than answered. This change fixes the sites it measured
and does not claim to have swept the module family.

## Named follow-ups, out of scope here

- **The rest of the family, unswept.** `scripts/hermes_runtime_validation/`
  carries other modules that compare recorded state against resolved objects —
  `consumer_handoff.py` most obviously, which verifies a receipt's tag and
  commit. Whether any of them mixes a live remote read with a local resolve has
  not been measured, and a claim either way would be unearned. A sweep is its
  own packet, on its own evidence.
- **The eleven-minute exposure window itself.** The deeper reason this defect is
  loud is that a whole-repository suite takes about eleven minutes and every
  minute of it is exposed to `main` moving. Sharding, or running the
  realization-validating test against a pinned fetch rather than the live
  remote, would shrink the window. Both are engineering-lane questions about
  `pytest-suite.yml`, not obligations about the verifier, and neither is
  proposed here.
- **Whether a verification may consult the network at all.** `SCO-002` already
  splits online Gate verification from offline runtime verification, and this
  change works within that split. The larger question — whether the
  repository's own test suite should ever exercise the ONLINE path, given that
  it makes a test's verdict a function of the world — is a real one and is
  deliberately left alone. Answering it by deleting the online assertion would
  be the sibling packet's defect B in a new place: a proof that stops running
  in order to stop failing.

## Impact

- Affected capability: `shared-contract-ownership` — three ADDED requirements,
  nine scenarios, no requirement MODIFIED.
- Affected code: `scripts/hermes_runtime_validation/release.py`,
  `tests/hermes_runtime_contracts/test_release_inventory.py`.
- Affected artifacts at realization: `contracts/manifest.yaml`,
  `contracts/CHANGELOG.md`, and a new
  `contracts/releases/contract-v<next>.digests.yaml` — because the verifier is
  a member of its own inventory, this change cannot land its code without
  re-cutting the bundle that describes it.
- Risk: LOW on semantics, MODERATE on mechanics. Nothing about what counts as
  reachable moves. The mechanical risk is that a verifier which previously
  performed no writes now fetches, so it touches the clone's object store — and
  Q1 is exactly the question of how narrowly.
- Sequencing: `add-hermes-customer-subject-runtime-contract` holds an active
  `MODIFIED` block for `SCO-002`. These requirements are ADDED and therefore
  compose with that outcome in either archive order; no delta here restates a
  line of `SCO-002`, which is what would make the order matter.
