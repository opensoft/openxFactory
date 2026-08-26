# Design: fix-release-reachability-race

Four decisions needed recording. The first is where the obligation lives; the
second is the shape of the fix and is the one this packet exists to argue; the
third is how one error message becomes three honest outcomes; the fourth is why
a validator bug fix drags a contract bundle behind it. Everything else in this
change is mechanical.

## 1. Where the requirements land — `shared-contract-ownership`, all ADDED

**Chosen.** Three ADDED requirements in `shared-contract-ownership`. No
requirement is MODIFIED.

The promoted capability that already governs this surface is
`shared-contract-ownership`, and specifically its "Contract version pinning"
requirement (`SCO-002`). Two facts settle it rather than one:

- **Its text draws the exact line this defect crosses.** As modified by the
  active ratified change `add-hermes-customer-subject-runtime-contract`:
  "Online Gate verification SHALL prove the annotated tag on the canonical
  remote; offline runtime verification SHALL resolve exact commit/tree/blob
  objects already present locally." The defect is a verifier standing with one
  foot on each side of that sentence — an ONLINE read of `refs/heads/main`,
  resolved against objects that are only sometimes "already present locally".
- **Its scenarios are already bound to the code in question.**
  `contracts/hermes-runtime/evidence-register.yaml` binds `SCO-002-S02`
  (published-tag verify), `SCO-002-S03` (pinned file drifts) and `SCO-002-S04`
  (offline verification) to `test_verify_tag_accepts_an_annotated_reachable_tag`,
  `test_verify_tag_rejects_a_tag_off_published_main`,
  `test_cli_verify_promotion_and_verify_tag` and
  `test_verify_promotion_rejects_a_drifted_release_surface`. The tests that
  exercise the two hazardous functions are this capability's evidence already.

The requirements are ADDED and not MODIFIED for the same reason the sibling
packet gave and one more that is specific to this case. The general reason:
OpenSpec's `MODIFIED` replaces a requirement wholesale, so every restatement is
a chance to truncate it — a hazard this repository hit three times in three days
and closed with `add-family-enumeration-check`. The specific reason: `SCO-002`
is ALREADY under an active `MODIFIED` block in
`add-hermes-customer-subject-runtime-contract`, so a second wholesale
replacement would make the two changes order-dependent at their archive gates,
and `release-realization`'s ordered-deltas rule would then require this proposal
to declare its deltas relative to that change's outcome. ADDED requirements
compose in either order, and none of them restates a line of `SCO-002`. The
sequencing note is recorded in the proposal's § Impact rather than being
engineered around.

**Rejected — `release-surface-integrity`.** The most tempting home, and wrong on
its own terms. That capability was created 2026-08-25 to hold the OBLIGATION
that a declared bundle describes its release surface, and it says in its own
text that "whether and how it is CHECKED is `doc-health`'s to define". Its
single requirement is about drift between an inventory and the blobs it names —
a different question from whether a candidate is on published main, and asked
of a different reader. Putting verification mechanics there would contradict the
scoping the capability just declared about itself.

**Rejected — `MODIFIED` against `hermes-governed-record-integrity`'s "Published
bundle identity is reproducible" (`HGR-009`).** This is where the underlying
obligation genuinely lives: "the exact reviewed commit MUST be reachable from
published `origin/main`", and the release verifier's own mandate to "validate
candidate bytes before commit and derive exact bytes from the pinned Git commit
after commit/tag". Three things rule it out. It is NOT PROMOTED — the capability
exists only as a delta inside the active change
`add-hermes-customer-subject-runtime-contract`, so a `MODIFIED` block here would
edit text that is not yet canon. It is a large, dense requirement whose
wholesale restatement is exactly the truncation hazard above. And this change
does not want to touch that obligation at all: the reachability requirement it
states is the one thing we are promising not to weaken.

**Rejected — a new capability of its own.** "Release verification mechanics"
would be a fourth capability in a neighbourhood that already has three, would
duplicate `shared-contract-ownership`'s evidence bindings, and would have to
import the online/offline distinction from `SCO-002` in order to say anything.
A capability whose first act is to restate another capability's sentence is a
section, not a capability.

## 2. The fix — resolve the operand before comparing, not retry after failing

**Chosen.** Before the reachability comparison is made, the object named by the
remote read is made locally available: if the clone does not already hold it,
the verifier fetches it from the remote it just consulted, and only then
compares.

The argument that decides this is not elegance, it is COVERAGE, and it comes
from a hazard site that is currently invisible. `verify_promotion` uses the live
`main_oid` twice:

```python
    if not _is_ancestor(repo_root, commit_oid, main_oid):        # :723
        ...
    findings.extend(_surface_drift(repo_root, commit_oid, main_oid))   # :732
```

and `_surface_drift` reads that same object id out of the same local store:

```python
    surfaces.update(_CommitSource(repo_root, main_oid).list_release_inventories())  # :686
    ...
        if _blob_object_id(repo_root, commit, path) != _blob_object_id(
            repo_root, main_oid, path                                              # :689
```

Today `_is_ancestor` raises at `:723`, so `:686` is never reached with an absent
object and the second hazard is MASKED rather than absent. `_CommitSource`'s
`git ls-tree` runs through `_run_git` with `allow_failure` unset, so an absent
commit there raises `ReleaseDependencyError("Git command failed")` — a message
strictly less informative than the one this change is replacing. And
`_blob_object_id` swallows `ContentResolutionError` and returns `None`, so any
path where the tree read did NOT raise would compare a real blob against `None`
and emit a false `HGR-RELEASE-SURFACE-DRIFT`.

`verify_tag` has the same structure with one more operand: `peeled_commit`
arrives from the remote's tag advertisement at `:781` and is read locally at
`:807` and again at `:816`, where `_verify_release_at` walks the tag's tree and
blobs.

So the question "where does the fix go?" has a measurable answer. A repair
placed at the point of comparison covers one of four uses. A repair placed at
the point the operand ENTERS the local world covers all four, and it covers
them by construction rather than by having remembered them.

**The mechanism was measured, not assumed.** On 2026-08-26 this branch's own
worktree fell into the defect — the remote's `main` had advanced to `c1c9c0dc`,
`git cat-file -e c1c9c0dc^{commit}` exited 128 locally, and the realization test
failed with the exact message this change is about. One `git fetch origin
c1c9c0dc` returned 0, `cat-file` then returned 0, and the same test passed with
no other change to the tree. That is the chosen fix, performed by hand, on the
real remote: resolve the operand, then answer. It also settles the primary half
of Q1 — the canonical remote serves a bare object id that no tracked ref points
at.

**Rejected — retry once on a 128 from `merge-base`.** The obvious minimal fix,
and it is minimal in the wrong dimension. It repairs `_is_ancestor` and leaves
`_surface_drift`, `_verify_release_at` and the tag read to meet the same absent
object with worse messages — trading one honest-but-misdirected error for a
different, vaguer one, and doing it at the moment the operator is closest to
publishing a tag. It also puts the recovery inside a general-purpose predicate
that does not know which remote its operands came from, so the fetch would need
the remote threaded down into it for no reason other than the retry.

**Rejected — fetch unconditionally at the top of each verify function.** Simpler
to write, and it makes a network round trip on every call including the common
case where the clone is already current. It also fetches when the answer is
already knowable, which is precisely the property that makes a verification slow
enough to be skipped. The cost is not hypothetical: the online realization path
is capped at 30 seconds twice over — `_run_git`'s per-invocation `timeout=30` at
`:135-156`, and `_run_cli`'s whole-invocation `timeout=30` at
`tests/hermes_runtime_contracts/test_validator_cli.py:104-113`, which governs
`--require-realization` — and that cap was breached once under machine load
during this packet's authoring (`tasks.md` § 5.5). Probe with `git cat-file -e`
first, so the already-current case spends nothing.

**Rejected — stop reading the remote; compare against the local
`refs/remotes/<remote>/main`.** This removes the mixing by removing the live
half, and with it the guarantee the check exists for. A local remote-tracking
ref is as old as the last fetch, so a candidate could be declared reachable from
a "main" that no longer exists, or unreachable from one it landed on ten minutes
ago. `SCO-002` requires the online mode to prove state on the CANONICAL REMOTE;
answering from a cached ref would be offline verification wearing the online
mode's name.

**Rejected — widen `_is_ancestor` to treat 128 as "not reachable".** Recorded
only to be refused explicitly, because it is the shortest diff and it is the one
genuinely dangerous option. It converts "I could not tell" into "no", which is
the same class of error as converting it into "yes" — a verdict invented from an
absence — and it would fire the refusal findings on candidates that are
perfectly reachable. Requirement 4 of this packet exists to make this
unavailable.

## 3. Three outcomes from one error message

**Chosen.** The reachability step reports three distinguishable outcomes, and
the reported reason names the one observed.

| observation | outcome | what changes |
| --- | --- | --- |
| the object resolves and the candidate is NOT an ancestor | the existing refusal finding, unchanged | nothing |
| the object was absent and became available | the comparison proceeds; no finding | this case reds today |
| the object was absent and cannot be made available | fail closed, as today, with a reason naming the fetch that failed | the message |

The middle row is the whole defect. The bottom row is the part worth being
careful about: it must stay a refusal. An unresolvable operand means the
question was not answered, and a verification that cannot answer must not report
a pass — that is the fail-closed floor `SCO-002` already sets for this family
("Both modes SHALL fail closed for ... missing bundle members, traversal,
symlink escape, version mismatch, or digest drift") and it is untouched here.
What changes is the diagnosis. "Commit reachability could not be determined" is
a statement about the verifier's own confusion; "the remote would not serve
object X" or "the remote could not be reached" is a statement about the world,
and it is the one that tells a reader whether to check their network, their
credentials, or their candidate.

**Rejected — a new finding code for the unfetchable case.** Findings are the
verifier's verdicts about the RELEASE. An environment that cannot serve an
object is not a fact about the release, and encoding it as a finding would put
it in a list that gates on content, where a caller could then be tempted to
filter it. `ReleaseDependencyError` with CLI exit code 2 already means exactly
"the dependency was unavailable", distinct from exit 1 for findings, and that
distinction is correct as it stands.

**Rejected — distinguishing the transient case by comparing timestamps or
re-reading the remote.** "Did main move during this run?" can be answered by
reading `refs/heads/main` a second time and comparing, and the answer is not
worth its cost: it adds a round trip, it can itself be raced, and nothing in the
requirement needs the verifier to KNOW that skew occurred. Resolving the operand
makes skew a non-event, which is a better outcome than detecting it.

## 4. Why a contract bundle rides this change

`scripts/hermes_runtime_validation/release.py` is a member of the release digest
inventory it helps verify. `contracts/releases/contract-v1.43.digests.yaml`
records it at `:993-996` as `type: validator`, `git_mode: '100644'`,
`digest: sha256:d149a34b9964ba2e7e7cf8aea63beaedcfd09bcaf7065b1cc2ac4385d1269704`
— and that is exactly what the tree hashes to today, so the declared bundle
currently describes the release surface correctly. Editing the file breaks that
agreement.

`release-surface-integrity` names the resulting state a defect for any member
outside the editorial three (changelog, manifest, README), and names the remedy:
"a release cut through the bundle realization order, never a hand-edit of the
inventory to match the tree". `doc-health`'s release-inventory drift family
reports non-editorial drift at `error`. The verifier itself would report
`HGR-RELEASE-DIGEST-MISMATCH` against its own bytes.

The precedent is not an argument by analogy; it is the same file for the same
reason. `contract-v1.10` was cut as a "superseding additive re-realization"
because finding F-U3 hardened release membership and thereby changed
`scripts/hermes_runtime_validation/release.py`, so the frozen `contract-v1.9`
inventory stopped reproducing the tree
(`contracts/CHANGELOG.md:2170-2185`). That release refreshed the inventory over
the current bytes and re-established manifest/changelog/tag/inventory agreement,
with no contract shape change and no consumer invalidated.

This change takes the same path. The class is additive: no schema moves,
`contract_schema_version` is unchanged, no instance valid at `contract-v1.43` is
narrowed, and a consumer pinned there stays conformant until it chooses to
upgrade. The bundle NUMBER is not reserved here — merge order allocates it, per
`docs/contract-versioning-policy.md` and the `contract-v1.28` renumber
precedent — and the cut may fold in with any other change reaching the same
`Unreleased` section.

One consequence deserves stating rather than discovering: the verifier's fix
will be verified BY the verifier, at the candidate commit, as part of its own
cut. `verify-promotion` runs before the tag; if the fix is wrong, the release
that carries it is the first thing it fails. That is a fortunate property of
this particular file and it is the reason § 4 of `tasks.md` insists the cut be
performed with the new code rather than around it.

## 5. Recorded at realization, 2026-08-26 — the two measurements that were owed

This section is appended by the realizing session. It changes no decision above;
it discharges the two places § 2 and the proposal's Open Questions left a claim
resting on an assumption, and it records one thing that was measured and NOT
acted on.

### Q1 — the fetch is narrowed to the object, with NO ref-fetch fallback

**Decided on measurement.** `tasks.md` § 2.1 as authored asked for
object-then-ref; the orchestrating session's ruling of 2026-08-26 made the
fallback conditional on a measurement showing the narrow fetch insufficient. It
is sufficient, so no fallback ships.

Measured against the canonical remote, `git@github.com:opensoft/openxFactory.git`:

| clone | object asked for | result |
| --- | --- | --- |
| `--depth 1` of `main` | a commit 25 behind the tip, under no tracked ref | rc 0, 4.80s |
| non-shallow, 1 commit behind | the current tip | rc 0, 8.13s |
| non-shallow, 3 commits behind | the current tip | rc 0, 8.49s |
| non-shallow, 8 commits behind | the current tip | rc 0, 6.55s |

Two things fall out. The remote serves a bare object id that no ref the clone
tracks points at — which was the entire doubt in Q1 — and the cost is the SSH
handshake and ref negotiation rather than the object count, so a ref fetch would
have bought nothing on cost either while bringing unrequested history and
mutating remote-tracking refs. A remote that declines to serve an object it
advertises is therefore requirement 2's fail-closed case, reached with a reason
that names the fetch, and not a case for a wider request nobody has needed.

The already-current case, which is the common one, costs **0.006 seconds and no
network at all**: `git cat-file -e <oid>^{object}` short-circuits before any
fetch is attempted. `^{object}` and not `^{type}` — the latter is not git
syntax, and the former is the type-agnostic form the tag path needs.

The narrowness is verified rather than asserted. After the verifier's own fetch
on a live stale clone, `git for-each-ref` still listed only `refs/heads/main` and
`FETCH_HEAD` still named the setup fetch's commit: `--no-tags
--no-write-fetch-head` confines the mutation to the object store, which is the
narrowest form the "a verifier that now writes" risk in § Impact can take.

### Q2 — the offline fixture works, one step narrower than proposed

**The mechanism as authored does not work, and the measurement caught it.**
`chmod 000` on the bare origin's whole `objects/` directory makes git refuse the
path as a repository at all: `git ls-remote` itself exits 128 with "does not
appear to be a git repository". A fixture built that way proves the pre-existing
"remote main is unavailable" path — the exact wrong-reason pass § 3.3 warned
about.

Revoking read on the single object FILE instead gives the wanted condition
exactly: `ls-remote` exits 0 and still advertises the advanced oid, while `git
fetch <remote> <oid>` exits 128 with `upload-pack: not our ref`. A remote that
advertises an object it will not serve. So the real fixture is KEPT and the
monkeypatch fallback OD-4 authorized is not used. The proof asserts the fixture's
own soundness inline, so it cannot silently degrade into the remote-unavailable
path later.

### Measured and deliberately not acted on — the shallow-clone verdict

Resolving the operand makes the object present. It does not make the ANCESTRY
present, and in a `--depth 1` clone the new code fetches the object, reaches
`git merge-base --is-ancestor`, and gets rc 1 out of a grafted history — a FALSE
`HGR-RELEASE-TAG-UNREACHABLE` where the published code refused with 128. That is
a verdict invented from an absence, and it is recorded in `tasks.md` § 6.4 with
the narrow rule that would close it, rather than closed here: this repository
checks out at `fetch-depth: 0`, the faithful reproduction of the measured defect
needed a NON-shallow stale clone (where the new code completes with zero
findings), and the hazard pre-exists this change in kind. Adding mechanism for a
population nobody has measured failing is the unearned sweep this packet
declines to perform everywhere else.
