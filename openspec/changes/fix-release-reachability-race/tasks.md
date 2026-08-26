# Tasks: fix-release-reachability-race

NO IMPLEMENTATION here is discharged. This packet is a PROPOSAL: it carries the
delta, the measurement, and the plan, and it changes no code. § 1.1 and § 1.2
ARE discharged — Brett commissioned the filing on 2026-08-26, and the same day
cleared all four flagged decisions as authored. § 1.3 is NOT: Q1 and Q3 stay
open, Q4 stays declined rather than ruled, and Q2's measurement half stands
undischarged even though its mechanism half is now ruled.

**AS FIRST WRITTEN this paragraph said "§ 1.2 is not: Q1 through Q4 and the four
flagged decisions all stand open, uncovered by that commissioning."** That was
true for a matter of hours. The four decisions are now cleared; the questions are
not, and splitting the two is the point of the § 1.2 / § 1.3 division below.

**§ 6 is deliberately OPEN and stays open.** Two adjacent gaps are recorded
there rather than implied, and one of them is the sweep this packet declines to
claim it performed.

## 1. Admission

- [x] 1.1 **DONE 2026-08-26 — the filing was commissioned, and the commission
      is the approval act.** `.openspec.yaml` records `kind: ad_hoc` with
      `approved_by` quoting Brett verbatim ("file the release-inventory CI race
      fix change") and `approved_on: 2026-08-26`, following
      `add-family-enumeration-check` ("in-session commissioning of the check
      itself") and `implement-keycloak-install-repo` (a session instruction
      cited as the approval act). This is NOT the blank-pair shape
      `harden-ideation-readiness-check` was raised under, and the difference was
      judged rather than assumed: that packet had no instruction behind it at
      all — it came out of an autonomous triage — so there was no act to
      record and inventing one was refused. This packet has the instruction.
      `proposal.md` carries `Status: ratified` with a single record-citing
      `Ratified:` line clearing the three-way floor on approver and date.
- [x] 1.2 **DONE 2026-08-26 — the four decisions in `proposal.md`
      § Orchestrator decisions are CLEARED, all four as authored, none
      vetoed.** A four-question multi-choice was put to Brett by the
      orchestrating session and he selected the recommended "keep" option on
      each: OD-1 the ADDED-in-`shared-contract-ownership` shape, OD-2
      fetch-before-check, OD-3 the archive gate on the bundle cut, OD-4
      real-fixture-first with the monkeypatch fallback. No verbatim wording
      reached the authoring session, so none is quoted — approver, date,
      mechanism and selected option are stated instead. NOTHING IN THE PACKET
      MOVED: every decision stands as authored, so no requirement, delta, task
      or design entry changed, the shape openxFactory PR #307 recorded when
      Brett cleared the two codex dispositions. `.openspec.yaml`'s origin block
      is deliberately left byte-identical — see the clearance block in
      `proposal.md` for why the retention rule makes that the correct choice.
- [x] 1.3 **CLOSED AT REALIZATION — see the note at the end of this item.**
      AS AUTHORED: STILL OPEN, and NOT covered by 1.2: Q1 (the fetch's narrowness and
      whether a ref fetch is an authorized fallback) and Q3 (whether reconciled
      skew should be observable). Q4 remains a scope this change DECLINES rather
      than one that has been ruled. Q2 is split — OD-4 ruled its MECHANISM half
      (real fixture first, monkeypatch fallback authorized) and left its
      MEASUREMENT half entirely undischarged, which is § 3.3 below. Only Q1
      still changes the work in § 2.
      **RESOLVED AT REALIZATION, 2026-08-26.** Q1 is DECIDED ON MEASUREMENT
      and the decision is NO ref-fetch fallback — evidence in § 2.1. Q2's
      measurement half is DISCHARGED, and it CORRECTED the fixture — § 3.3.
      Q3 resolved by doing nothing, which is what its recommendation asked
      for: the implementation emits no log line for reconciled skew and canon
      still mandates none. Q4 stays DECLINED and lives at § 6.1.

## 2. Implementation — the resolution step

- [x] 2.1 `scripts/hermes_runtime_validation/release.py`: add a single helper
      that takes a repository, a remote, and an object id, and returns once that
      object is locally resolvable — a `git cat-file -e <oid>^{commit}` probe
      first, and only on absence a fetch from the named remote. It raises
      `ReleaseDependencyError` when the object cannot be made available, with a
      reason naming the retrieval rather than the candidate. Per Q1, try
      `git fetch <remote> <oid>` and fall back to `git fetch <remote>
      refs/heads/main` (or the tag ref) when the remote declines to serve an
      unadvertised object; treat only the failure of BOTH as unavailable.
      **DONE.** `_resolve_remote_object(repo, remote, object_id)` at
      `release.py:195-253`, placed immediately above `_is_ancestor` so a reader
      meets the resolution before the comparison. Probe `git cat-file -e
      <oid>^{object}` first — MEASURED at 0.006s with no network on an
      already-current clone — then, only on absence, `git fetch --no-tags
      --no-write-fetch-head <remote> <oid>`. `^{object}` rather than `^{type}`:
      `^{type}` is not git syntax (`git cat-file -e <oid>^{type}` exits 128 with
      "Not a valid object name"), and `^{object}` is the type-agnostic form,
      which the tag path needs. `--no-write-fetch-head` and `--no-tags` keep the
      mutation to the object store alone — VERIFIED on a live stale clone: after
      the verifier's fetch, `for-each-ref` still listed only `refs/heads/main`
      and `FETCH_HEAD` still named the setup fetch's commit, not the fetched
      tip.
      **Q1 DECIDED ON MEASUREMENT: NO REF-FETCH FALLBACK.** The task as
      authored asked for object-then-ref; the orchestrator's ruling of
      2026-08-26 made the fallback conditional on measurement showing the narrow
      fetch insufficient. It is sufficient. Against the canonical remote
      (`git@github.com:opensoft/openxFactory.git`): a bare-oid fetch of a commit
      25 behind the tip, under no ref a depth-1 clone tracked, returned 0 in
      4.80s; bare-oid fetches of the current tip from non-shallow stale clones 1,
      3 and 8 commits behind returned 0 in 8.13s, 8.49s and 6.55s (cost is the
      SSH handshake and ref negotiation, not the object count). A remote that
      declines to serve an object it advertises is therefore the fail-closed case
      of requirement 2, not a case for a wider fetch nobody has needed — and a
      speculative ref fetch would have brought unrequested history and mutated
      remote-tracking refs to buy nothing measured.

- [x] 2.2 `verify_promotion`: call the helper on `main_oid` immediately after
      `:718` reads it, before `_is_ancestor` at `:723`. This also covers
      `_surface_drift` at `:732`, which is the point — see 2.4.
      **DONE.** `verify_promotion` resolves `main_oid` at `:784`,
      immediately after `:780` reads it and before both readers: `_is_ancestor`
      at `:786` and `_surface_drift` at `:795`.

- [x] 2.3 `verify_tag`: call the helper on `main_oid` after `:803`, and on
      `peeled_commit` after it is derived from the `:781` advertisement, before
      `_is_ancestor` at `:807` and before `_verify_release_at` at `:816`. The
      tag object has the same exposure as main's tip for the same reason: a tag
      published since the clone was taken is not in the clone.
      **DONE.** `verify_tag` resolves `peeled_commit` at `:868`, right
      after `:864` derives it from the advertisement, and `main_oid` at `:874`,
      right after `:873` reads it — so both are resolved before `_is_ancestor`
      at `:875` and before `_verify_release_at` at `:884`.

- [x] 2.4 Do NOT patch `_is_ancestor` at `:195-202`. Its 128-branch refusal is
      correct and stays exactly as written — it is the last line of defence if
      the resolution step is ever bypassed, and the regression in 3.4 depends on
      it still being there. Widening it to treat 128 as "not reachable" is
      refused on the record in `design.md` § 2.
      **DONE — `_is_ancestor` is BYTE-UNCHANGED**, 128-branch refusal
      included. Confirmed twice over: `git diff` shows no hunk inside
      `:195-202`-as-was (now `:255-262`), and the § 3.4 mutation proof asserts
      the exact string `commit reachability could not be determined` still
      arrives when the resolution step is removed, which it could not do if the
      guard had been widened.

- [x] 2.4b **MIND THE 30-SECOND BUDGET ON THE ONLINE PATH.** This change adds a
      network fetch to a path that is already capped twice over: `_run_git` runs
      every git invocation with `timeout=30` (`:135-156`), and
      `tests/hermes_runtime_contracts/test_validator_cli.py`'s `_run_cli` at
      `:104-113` caps the WHOLE CLI invocation at `timeout=30` — including
      `--require-realization`, which is the online realization path. That cap was
      breached once during this packet's own authoring: the full suite reported
      `subprocess.TimeoutExpired` after 30 seconds on
      `test_release_mode_field_is_preserved_on_the_real_repository[--require-realization-realization]`
      (§ 5.5). That was almost certainly machine load — three other sessions'
      pytest suites were running concurrently on the same box — and it is NOT
      evidence of a defect in the validator. It is evidence that the budget is
      already tight, and this change spends more of it. Two consequences for
      2.1: prefer the NARROW object fetch over a ref fetch on cost grounds as
      well as precision grounds (Q1), and probe with `git cat-file -e` FIRST so
      the common case of an already-current clone costs nothing. If the budget
      turns out to be genuinely insufficient after the fix, raising it is a
      separate decision with its own evidence — do not raise it silently as part
      of this change.
      **DONE, and the budget is not raised.** Neither cap moves.
      MEASURED marginal cost of the resolution step: 0.006s and NO NETWORK when
      the clone already holds the object (the common case, because the probe
      short-circuits), and 6.55–8.49s for the narrow fetch when it does not —
      inside `_run_git`'s per-invocation 30s cap with room to spare. Full
      `--require-realization` through the CLI on a current clone: 7.99s against
      `_run_cli`'s 30s whole-invocation cap. The one number worth watching is the
      end-to-end live realization on a STALE clone, 24.87s (§ 5.3), because a
      stale clone pays the fetch on top; in continuous integration the checkout
      is taken at run start and `main` advances by a commit or two, so the fetch
      is the small one measured above. Recorded rather than acted on: if the cap
      proves insufficient after this lands, raising it is its own decision with
      its own evidence.

- [x] 2.5 Confirm by reading, not by assuming, that `_surface_drift`'s two
      remote-object reads are now covered: `_CommitSource(repo_root,
      main_oid).list_release_inventories()` at `:686` (a `git ls-tree` that
      raises `"Git command failed"` on an absent commit, because `_run_git`
      runs it without `allow_failure`) and `_blob_object_id(repo_root,
      main_oid, path)` at `:689` (which swallows `ContentResolutionError` and
      returns `None`, so an absent commit there would compare a real blob
      against nothing and emit a FALSE `HGR-RELEASE-SURFACE-DRIFT`). Both are
      masked today by `:723` raising first. If either still has a path to an
      unresolved object after 2.2, the resolution step is in the wrong place.
      **DONE, by reading and then by grep rather than by assumption.**
      Every remote-derived object id and every local reader of one:
      `verify_promotion` — `:780` reads `main_oid`, `:784` resolves it, `:786`
      `_is_ancestor`, `:795` `_surface_drift` (whose `:745` `git ls-tree` and
      `:748` `_blob_object_id` are the two masked reads). `verify_tag` — `:864`
      derives `peeled_commit`, `:868` resolves it, `:873` reads `main_oid`,
      `:874` resolves it, `:875` `_is_ancestor`, `:884` `_verify_release_at`.
      `_surface_drift` has exactly ONE caller (`:795`) and `_verify_release_at`
      exactly two (`:796` with the LOCAL `commit_oid` from `_full_commit`, and
      `:884` with the resolved `peeled_commit`). The `:768` `_ls_remote` for
      `refs/tags/<tag>` tests only whether a row exists and reads no object. No
      path to an unresolved remote object survives.

## 3. Implementation — the proofs

Fixtures follow the pattern this module already establishes:
`_bare_origin(tmp_path)` at `:128-133`, `_repo_with_committed_inventory`, and
`_git(repo, "remote", "add", "origin", str(origin))` — the local-directory
"remote" used by `test_verify_tag_rejects_a_tag_off_published_main` and
`test_verify_tag_reports_a_missing_remote_tag`.

- [x] 3.1 **The skew regression.** Build the repository and its bare origin as
      today, push `main`, then clone the origin a SECOND time into a separate
      directory, commit there, and push — so the origin's `main` advances while
      the first repository's object store does not. Assert `verify_promotion`
      and `verify_tag` from the FIRST repository complete and return the same
      codes they return against a current clone. Today, before 2.2/2.3, this
      test raises `ReleaseDependencyError("commit reachability could not be
      determined")`, which is the point of writing it first.
      **DONE, and it failed first.** `test_verify_promotion_completes_
      when_remote_main_advanced_past_the_clone` and `test_verify_tag_completes_
      when_the_tag_and_main_are_newer_than_the_clone`, over a new
      `_advance_remote_main_from_a_peer_clone` helper that clones the bare origin
      a SECOND time, commits, and pushes — so the origin's `main` moves while the
      verifying repository's object store does not. Both assert the condition is
      real before asserting the verdict (`_ls_remote` names the advanced oid AND
      the local store cannot resolve it), and both then assert the same `== []`
      the current-clone tests assert. The tag case is the stronger one: BOTH of
      `verify_tag`'s operands are absent, the published tag's commit as well as
      main's tip. Written before the fix, they failed exactly as predicted at
      `release.py:200` with `ReleaseDependencyError: commit reachability could
      not be determined`.

- [x] 3.2 **The masked second site.** A skew fixture that exercises
      `_surface_drift` specifically — remote `main` advanced AND a
      release-surface path differing between the candidate and the advanced
      main — asserting the drift verdict is the one the surface actually
      warrants and not an artefact of an unresolved object. This is the
      assertion that would have caught the `None`-comparison hazard in 2.5.
      **DONE.** `test_surface_drift_is_computed_against_a_resolved_
      advanced_main`: the peer clone edits `contracts/manifest.yaml`, a
      `RELEASE_SURFACE_PATHS` member, so remote `main` is both AHEAD of the
      candidate and genuinely drifted from it. The assertion is an exact
      equality on the whole finding list — ONE
      `HGR-RELEASE-SURFACE-DRIFT` on `contracts/manifest.yaml` — which is the
      assertion that would catch the `None`-comparison hazard: an unresolved
      `main_oid` makes `_blob_object_id` return `None` for EVERY surface path, so
      the false verdict is drift on all of them, and an `in` assertion would have
      passed on it.

- [x] 3.3 **The unavailable-object proof, mechanism per Q2.** First choice:
      after `ls-remote` is known to work, make the bare origin's `objects/`
      directory unreadable (`chmod 000`) so refs still advertise while a fetch
      cannot be served, and assert a `ReleaseDependencyError` whose message
      names the retrieval. THIS IS NOT MEASURED — if `git upload-pack` needs
      object access during advertisement, the fixture instead proves the
      pre-existing "remote main is unavailable" path and must be discarded.
      Fallback: monkeypatch `_run_git` (or the helper from 2.1) to fail only
      the fetch invocation. Measure before choosing, and do not keep a fixture
      that passes for the wrong reason.
      **RULED 2026-08-26 (Brett, OD-4): this ordering is authorized — real
      fixture first, monkeypatch fallback permitted.** THE RULING DOES NOT
      DISCHARGE THIS TASK. It settles which mechanism may be used; it supplies
      no measurement, and the `chmod 000` behaviour of `git upload-pack` during
      advertisement over a local path remains unobserved. Measure it, and
      discard the fixture for the fallback if it turns out to prove the
      pre-existing "remote main is unavailable" path instead.
      **DONE — MEASURED FIRST, AND THE MEASUREMENT CORRECTED THE
      FIXTURE.** The mechanism as authored does not work: `chmod 000` on the bare
      origin's whole `objects/` directory makes git refuse the path as a
      repository at all, so `git ls-remote` itself exits 128 with "does not
      appear to be a git repository". A fixture built that way would have proved
      the pre-existing "remote main is unavailable" path — exactly the wrong
      thing this task warned about. THE REAL FIXTURE IS KEPT, one step narrower:
      revoke read on the single loose object FILE
      (`objects/<xx>/<rest>`, with a pack-file fallback and a
      `receive.unpackLimit` setting to keep pushed objects loose). MEASURED:
      `ls-remote` exits 0 and still advertises the advanced oid, while `git fetch
      <remote> <oid>` exits 128 — `upload-pack: not our ref`. That is precisely
      the wanted condition, a remote that advertises an object it will not serve,
      so the monkeypatch fallback OD-4 authorized was NOT needed and is not used.
      `test_verify_promotion_fails_closed_naming_the_fetch_it_could_not_perform`
      asserts the fixture's soundness inline (`_ls_remote` still returns the
      advanced oid, so the test cannot silently degrade into the
      remote-unavailable path), then asserts a `ReleaseDependencyError` whose
      message contains `fetch` and the oid and does NOT contain "could not be
      determined". The message measured: `remote object fetch failed: origin
      would not serve <oid>`.

- [x] 3.4 **Pin the proofs to the defect.** Remove the resolution step alone and
      re-run 3.1 and 3.2: both must fail, reproducing the 128 refusal. A proof
      that still passes with the step removed is unpinned and gets rewritten —
      the discipline `test_mutation_reverting_parse_header_alone_reproduces_the_f5_divergence`
      established, and the reason 2.4 keeps `_is_ancestor`'s guard intact.
      **DONE, twice, because an in-process mutation can be
      platform-inert.** (a) IN-PROCESS, as a kept test:
      `test_mutation_removing_the_resolution_step_alone_reproduces_the_refusal`,
      parametrized `[skew]` and `[surface-drift]`, rebinds
      `release._resolve_remote_object` to a no-op and asserts the exact string
      `commit reachability could not be determined` comes back. (b)
      SOURCE-LEVEL, run once by hand: all three `_resolve_remote_object(...)`
      call sites commented out in `release.py`, whereupon ALL FOUR new proofs
      failed — the three skew proofs at `release.py:200`, and the
      unavailable-object proof on `assert 'fetch' in message` with the message
      reading `commit reachability could not be determined`. Source restored and
      digest-checked afterwards. The proofs are pinned to the defect, not to the
      shape of the fix.

- [x] 3.5 Confirm no existing assertion loosens. `test_verify_tag_rejects_a_tag_off_published_main`
      and `test_verify_promotion_rejects_an_already_published_tag` must keep
      their exact codes: a resolution step that made a genuinely off-main tag
      look reachable would be this change committing the sin it exists to
      prevent.
      **DONE.** `python3 -m pytest
      tests/hermes_runtime_contracts/test_release_inventory.py -q -m "not
      postgres"` → **44 passed** (0:01:18), which is the 38 that existed plus the
      6 added. No existing assertion was edited: `git diff` on the test file is
      insertion-only. `test_verify_tag_rejects_a_tag_off_published_main`,
      `test_verify_promotion_rejects_an_already_published_tag` and
      `test_verify_promotion_rejects_a_candidate_absent_from_remote_main` keep
      their exact codes — in the last one the resolution step short-circuits on
      the probe, because the remote's `main` is already local, and the refusal
      still fires on rc 1.

- [x] 3.6 Bind the new proofs into `contracts/hermes-runtime/evidence-register.yaml`
      under the `SCO-002` scenarios they serve — `SCO-002-S02` (published-tag
      verify) and `SCO-002-S04` (offline verification) are the closest fits, and
      the register already lists the sibling tests there. Adding test node ids
      to an existing scenario is an in-place edit; do NOT add scenario ids, which
      the T011/T012 parity tests will reject.
      **DONE, in place, no scenario id added.** Test node ids appended
      to three existing `SCO-002` scenarios rather than the two the task named,
      because a third fits better than a forced fit: `S02` (published-tag verify)
      takes the tag-skew proof, the promotion-skew proof and the `[skew]`
      mutation case; `S03` (pinned file drifts) takes the release-surface proof
      and the `[surface-drift]` mutation case, alongside the
      `test_verify_promotion_rejects_a_drifted_release_surface` it already
      carries; `S04` (verification without a usable network) takes the
      unavailable-object proof. `tests/hermes_runtime_contracts/
      test_acceptance_parity.py -q` → **9 passed**, so every appended node id
      collects and none is skipped.

## 4. Realization — the contract bundle

This change cannot land its code without re-cutting the bundle that describes
it. `scripts/hermes_runtime_validation/release.py` is a non-editorial member of
`contracts/releases/contract-v1.43.digests.yaml` (`:993-996`), and the recorded
digest `sha256:d149a34b...` is what the tree carries today — verified 2026-08-26
by `git cat-file blob HEAD:scripts/hermes_runtime_validation/release.py |
sha256sum`. The realization order is the one `contract-v1.10` used for this same
file (`contracts/CHANGELOG.md:2170-2185`) and the one recorded in the release
finishing recipe.

- [x] 4.1 Allocate the bundle number at realization, NOT here. `contract-v1.43`
      is current; merge order decides the next minor, and the
      `contract-v1.28` renumber sweep is the precedent for why a proposal must
      not reserve one.
      **DONE — `contract-v1.44`, allocated here and not in the
      proposal.** Collision check first, both ways the recipe asks for: `git
      ls-tree origin/main contracts/releases/` ends at
      `contract-v1.43.digests.yaml`; `git ls-remote --tags origin
      'refs/tags/contract-v1.4*'` ends at `contract-v1.43`; and the only open
      pull request, #176, touches one `ideation/dashboard/intents/` gate-intent
      file and no release surface. No other session has claimed 1.44.

- [x] 4.2 `contracts/manifest.yaml` — advance `contract_bundle_version`.
      **DONE.** `contracts/manifest.yaml:3`
      `contract_bundle_version: contract-v1.43` → `contract-v1.44`, the only
      manifest edit — no schema row digest moves, because this change touches no
      schema. The three prose mentions of `contract-v1.43` deeper in the file are
      historical consumption-rule text about when a shape was registered and are
      correctly left alone.

- [x] 4.3 `contracts/CHANGELOG.md` — an additive entry stating the class and
      why the cut exists: a validator member's bytes moved, no schema changed,
      `contract_schema_version` unchanged, no instance valid at
      `contract-v1.43` narrowed, consumers pinned there remain conformant until
      they upgrade.
      **DONE.** `contracts/CHANGELOG.md:12` — a new
      `## contract-v1.44 — 2026-08-26 (additive; the release verifier resolves
      its remote operand before it compares)` section stating the class
      (ADDITIVE/minor, no schema bytes, `contract_schema_version` unchanged, no
      instance valid at `contract-v1.43` narrowed, consumers pinned there
      conformant until they upgrade), why membership forced the cut, what moved,
      and the `contract-v1.10` precedent for this same file.

- [x] 4.4 `scripts/validate-contract-release.py build --tag contract-v<next>
      --output contracts/releases/contract-v<next>.digests.yaml` — deterministic
      from manifest plus contract index, and RERUN after any further edit to an
      inventory member. Never hand-edit an inventory to match a tree; that is
      the shortcut `release-surface-integrity` forbids by name.
      **DONE, and it reproduces byte-for-byte.** `python3
      scripts/validate-contract-release.py build --tag contract-v1.44 --output
      contracts/releases/contract-v1.44.digests.yaml` → `release build: pass`,
      `entries=192` (the same membership count as `contract-v1.43`: nothing
      joined or left the bundle). Run a second time to a scratch path, both
      outputs and the committed file share one digest,
      `sha256:4373259689f53699929ac462fde10466902887b7e8c20d0f68e538c9655d4100`,
      and `cmp` reports them identical. The inventory's new entry for the
      verifier reads `digest: sha256:2160dc3b745261481c450aef6aa50f8eeeff6ed4d4b
      88daf7b1138013b6d9d33`, which is exactly `sha256sum` of the tree's
      `scripts/hermes_runtime_validation/release.py` and no longer the
      `d149a34b...` the frozen `contract-v1.43` inventory records. NO INVENTORY
      WAS HAND-EDITED at any point.

- [ ] 4.5 `verify-commit --commit HEAD` after committing, then
      `verify-promotion --commit <candidate> --remote origin --tag <tag>` BEFORE
      tagging. Note the fortunate property: this runs the NEW code, so the fix
      is exercised by the cut that carries it. `HGR-RELEASE-TAG-EXISTS` after
      the tag is pushed is the expected later state, not a failure.
      **PARTIALLY DISCHARGED, DELIBERATELY. `verify-commit` is done here;
      `verify-promotion` is not, and cannot be.** `python3
      scripts/validate-contract-release.py verify-commit --commit HEAD` on the
      realization branch → recorded in the pull request body. `verify-promotion`
      requires the candidate to be reachable from the remote's `main`, which by
      definition it is not before the merge, so it belongs to the post-merge cut
      along with the tag — and per the orchestrating session's instruction of
      2026-08-26 the tag is NOT this session's act. The fortunate property this
      task names holds either way: the cut runs the NEW code, and this pull
      request's own continuous-integration run already exercises it against the
      live remote.

- [ ] 4.6 Annotated tag on the merge commit on `main`, message style
      `contract-v<next> — additive: <summary>`. Then `verify-tag`.
      **NOT DONE, and not this session's to do.** The annotated
      `contract-v1.44` tag goes on the MERGE COMMIT on `main`, message style
      `contract-v1.44 — additive: the release verifier resolves its remote
      operand before it compares`, followed by `verify-tag`. Deferred to the
      post-merge cut on the orchestrating session's instruction.

- [ ] 4.7 Sync the aggregation-repo submodule pointer. The shared openxFactory
      checkout usually holds other sessions' uncommitted work — stage the
      gitlink directly with `git update-index --cacheinfo 160000,<sha>,openxFactory`,
      verify `git diff --cached --name-only` shows exactly that entry, and
      commit inside that verified window.
      **NOT DONE, and blocked on 4.6.** The aggregation-repo submodule
      pointer can only be synced to a merge commit that exists. Stage the gitlink
      with `git update-index --cacheinfo 160000,<sha>,openxFactory`, verify `git
      diff --cached --name-only` shows exactly that entry, and commit inside that
      verified window.

## 5. Verification

- [x] 5.1 `python3 -m pytest tests/hermes_runtime_contracts -q` green. **Measured
      2026-08-26 on this branch, and it was NOT green — the defect fired here.**
      `-m "not postgres"` (the marker set continuous integration uses):
      **1 failed, 498 passed, 338 deselected in 276.63s**, the single failure
      being `test_validate_candidate_passes_on_the_realized_repository` at
      `release.py:200`, because the remote's `main` had moved to `c1c9c0dc`
      while this worktree sat still. `git fetch origin c1c9c0dc` then returned
      0 and the same test passed in isolation (`1 passed in 44.44s`) with no
      other change. Record that as the authoring baseline honestly: this packet
      changes no code, so the failure is the defect in flight, exactly as the
      sibling packet's `1 failed, 895 passed` was.
      **GREEN AT REALIZATION, 2026-08-26.** `python3 -m pytest
      tests/hermes_runtime_contracts -q -m "not postgres"` → **505 passed, 338
      deselected in 253.05s (0:04:13)**, exit 0. The arithmetic is the evidence:
      the authoring baseline was `1 failed, 498 passed`, so 499 collected became
      505 — the six new proofs — and the one failure is gone. `test_validate_
      candidate_passes_on_the_realized_repository`, the test the defect fired
      through, passes. Also green on the way: `test_release_inventory.py` alone →
      **44 passed** (0:01:18); `test_validator_cli.py` → **21 passed**
      (0:02:17), no `_run_cli` timeout despite a load average of 26 on the box;
      `test_acceptance_parity.py` → **9 passed**.

- [x] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate fix-release-reachability-race --strict`
      and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` both green.
      **BOTH GREEN, 2026-08-26.** `openspec validate
      fix-release-reachability-race --strict` → `Change
      'fix-release-reachability-race' is valid`, exit 0. `openspec validate --all
      --strict` → **Totals: 78 passed, 0 failed (78 items)**, exit 0.

- [x] 5.3 **DONE 2026-08-26 — the original failure was reproduced under
      control, and the fix's mechanism was exercised by hand.** Not in a scratch
      clone: in THIS worktree, which fell into the defect on its own while the
      packet was being written. `git ls-remote origin refs/heads/main` gave
      `c1c9c0dcd721b8597bea4462e22721d7e03d3ab3`; `git cat-file -e
      c1c9c0dc^{commit}` exited 128 locally; the realization test failed at
      `release.py:200`. Then `git fetch origin c1c9c0dc` exited 0, `cat-file`
      exited 0, and the same test passed. Resolve the operand, then answer —
      performed manually against the real remote. What remains for the
      implementation is to do it in the code, at the four operand sites, with
      the taxonomy of § 3 of the delta.
- [ ] 5.4 Re-run the full suite three times with a commit landing on the remote
      `main` inside each window, and confirm three identical verdicts. That is
      the property PR #372's three attempts did not have.
      **NOT DONE, and it is not performable on demand — see the substitute,
      which is stronger.** Three full-suite runs each with a commit landing on
      the remote `main` inside its window would require arranging three merges to
      `main` during three eleven-minute windows; this session cannot cause them
      and waiting for them is not a proof. TWO substitutes were measured instead,
      and between them they cover the property this task wanted. (a)
      DETERMINISTIC, and kept as regressions: the § 3.1/3.2 fixtures DRIVE the
      skew rather than waiting for it, so the property is asserted on every run
      instead of on a lucky one. (b) LIVE, against the canonical remote, once:
      § 5.3's stale-full-clone probe, where the published validator refuses and
      the new one completes with zero findings on the same tree and the same
      remote. What remains genuinely unproven is only the many-runs-identical
      claim, and it is unprovable by construction — recorded honestly rather than
      ticked.

- [x] 5.5 **DONE — authoring-time baselines, measured 2026-08-26 in this
      worktree**, so a later reader can tell what moved:
      - `python3 -m pytest tests/hermes_runtime_contracts -q -m "not postgres"`
        → **1 failed, 498 passed, 338 deselected** (0:04:36). The one failure is
        this change's own defect, firing live; see § 5.1.
      - the same single test after `git fetch origin <remote main oid>` →
        **1 passed** (44.44s), tree unchanged.
      - the FULL `python3 -m pytest tests/hermes_runtime_contracts -q` (postgres
        markers INCLUDED, run concurrently with three other sessions' suites on
        the same machine) → **1 failed, 836 passed in 2980.75s (0:49:40)**, and
        the failure was a DIFFERENT one:
        `test_validator_cli.py::test_release_mode_field_is_preserved_on_the_real_repository[--require-realization-realization]`
        raising `subprocess.TimeoutExpired` after 30 seconds. Recorded because a
        reader running the full suite will see it and should not mistake it for
        this defect. It is a load artifact against the `_run_cli` cap, not a
        finding about the validator — but it is why § 2.4b exists.
      - `python3 -m pytest tests/doc-health -q` → **896 passed**, 1 warning
        (0:42.91). The known agent-worktree hazard —
        `test_derivation_reproduces_the_real_bootstrap_clusters`, defect A of
        `harden-ideation-readiness-check` — did NOT fire on this run; it is
        noted rather than chased either way, because it is already filed and
        merged and nothing here touches it.
      - `OPENSPEC_TELEMETRY=0 openspec validate fix-release-reachability-race
        --strict` → valid; `--all --strict` → **78 passed, 0 failed**.
- [ ] 5.6 ARCHIVE AFTER REALIZATION. This change ships ACTIVE and archives only
      on merged-plus-green PLUS the bundle cut of § 4, following
      `add-family-enumeration-check` for the merge half and `contract-v1.10` for
      the cut half. The archive act is its own commit after the release.
      **NOT DONE, correctly: this is the archive act and it is deliberately
      not performed here.** The gate is merged-plus-green PLUS the § 4 cut, and
      the tag (4.6) is outstanding. Per the orchestrating session's instruction
      of 2026-08-26 this session does not merge, does not tag, and does not
      archive.

## 6. Open — deliberately not closed by this change

- [ ] 6.1 THE SWEEP, NAMED AND NOT PERFORMED: does the same live-read /
      local-resolve mixing exist elsewhere in
      `scripts/hermes_runtime_validation/`? `consumer_handoff.py` verifies a
      receipt's tag and commit and is the obvious next candidate. This change
      fixes the sites it measured on PR #372 and claims nothing about the
      others, because a sweep asserted without measurement is the same species
      of unearned answer this packet is about.
- [ ] 6.2 The exposure window itself. The suite runs about eleven minutes and
      every minute is exposed to `main` moving, because the checkout that seeds
      the object store is taken at the start. Sharding, or exercising the
      realization path against a pinned fetch rather than the live remote,
      would shrink it. Both are `pytest-suite.yml` questions rather than
      obligations about the verifier, and neither is proposed here.
- [ ] 6.3 Adjacent and also not this change: `_blob_object_id` at `:204-209`
      converts every `ContentResolutionError` into `None`, so "the blob is
      absent at this commit" and "this commit does not exist" are the same
      value to its callers. § 2.5 removes the reachable path to the second
      case; the conflation itself survives, and it is the kind of thing that
      makes the next defect in this file hard to read.

- [ ] 6.4 **NAMED HERE BECAUSE IT WAS MEASURED HERE, and it is the one thing
      in this realization that may want a ruling before the tag: A SHALLOW CLONE
      STILL CANNOT ANSWER, AND NOW ANSWERS WRONGLY.** Resolving the operand makes
      the object present; it does not make the ANCESTRY present. MEASURED
      2026-08-26 against the canonical remote, in a `--depth 1` clone of `main`:
      the published validator refuses with `commit reachability could not be
      determined` (128, the object absent), and the NEW validator fetches the
      object, reaches `git merge-base --is-ancestor`, and gets rc **1** from a
      grafted history — reporting a FALSE `HGR-RELEASE-TAG-UNREACHABLE` on a tag
      that is perfectly reachable. That is a verdict invented from an absence,
      which is the shape requirement 2's third scenario forbids, so it is stated
      plainly rather than buried.
      WHY IT IS NOT FIXED HERE, and why that is defensible: this repository's
      continuous integration checks out at `fetch-depth: 0`
      (`.github/workflows/pytest-suite.yml:206`, and `doc-health-reusable.yml:813`
      likewise), so no measured run of this suite is shallow — the faithful
      reproduction of the real defect needed a NON-shallow stale clone, and there
      the new validator completes with zero findings. The hazard also pre-exists
      this change in kind: a shallow clone holding the object but not the
      connecting history already got a false rc 1. What this change does is widen
      how often the comparison is REACHED in a truncated store. Fixing it means
      new mechanism nobody asked for, on a population nobody measured failing,
      which is exactly the unearned sweep this packet's § Named follow-ups
      declines to perform — and the four orchestrator decisions were ruled
      narrowly enough that taking a fifth unbidden would be the wrong move.
      THE NARROW RULE, if it is wanted: a POSITIVE ancestor verdict is
      trustworthy in any store, because a path git found is a path that exists; a
      NEGATIVE verdict in a shallow store is not. So refuse — as a dependency
      refusal naming the truncated history — only when `_is_ancestor` returns
      false AND `git rev-parse --is-shallow-repository` says true, at the two call
      sites rather than inside `_is_ancestor` (which § 2.4 protects). One local
      git call, no network, no widening. Its own packet, on this measurement.