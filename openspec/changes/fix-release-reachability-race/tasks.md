# Tasks: fix-release-reachability-race

NO IMPLEMENTATION here is discharged. This packet is a PROPOSAL: it carries the
delta, the measurement, and the plan, and it changes no code. § 1.1 IS
discharged — Brett commissioned the filing on 2026-08-26 and that instruction is
the origin act — and § 1.2 is not: Q1 through Q4 and the four flagged decisions
all stand open, uncovered by that commissioning.

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
- [ ] 1.2 Rule the four decisions in `proposal.md` § Orchestrator decisions and
      the four questions Q1-Q4. Q1 (object fetch or ref fetch) and Q2 (the
      offline fixture mechanism) both change work below if reversed; Q3 changes
      nothing structural; Q4 is a scope question this change already answers by
      declining.

## 2. Implementation — the resolution step

- [ ] 2.1 `scripts/hermes_runtime_validation/release.py`: add a single helper
      that takes a repository, a remote, and an object id, and returns once that
      object is locally resolvable — a `git cat-file -e <oid>^{commit}` probe
      first, and only on absence a fetch from the named remote. It raises
      `ReleaseDependencyError` when the object cannot be made available, with a
      reason naming the retrieval rather than the candidate. Per Q1, try
      `git fetch <remote> <oid>` and fall back to `git fetch <remote>
      refs/heads/main` (or the tag ref) when the remote declines to serve an
      unadvertised object; treat only the failure of BOTH as unavailable.
- [ ] 2.2 `verify_promotion`: call the helper on `main_oid` immediately after
      `:718` reads it, before `_is_ancestor` at `:723`. This also covers
      `_surface_drift` at `:732`, which is the point — see 2.4.
- [ ] 2.3 `verify_tag`: call the helper on `main_oid` after `:803`, and on
      `peeled_commit` after it is derived from the `:781` advertisement, before
      `_is_ancestor` at `:807` and before `_verify_release_at` at `:816`. The
      tag object has the same exposure as main's tip for the same reason: a tag
      published since the clone was taken is not in the clone.
- [ ] 2.4 Do NOT patch `_is_ancestor` at `:195-202`. Its 128-branch refusal is
      correct and stays exactly as written — it is the last line of defence if
      the resolution step is ever bypassed, and the regression in 3.4 depends on
      it still being there. Widening it to treat 128 as "not reachable" is
      refused on the record in `design.md` § 2.
- [ ] 2.5 Confirm by reading, not by assuming, that `_surface_drift`'s two
      remote-object reads are now covered: `_CommitSource(repo_root,
      main_oid).list_release_inventories()` at `:686` (a `git ls-tree` that
      raises `"Git command failed"` on an absent commit, because `_run_git`
      runs it without `allow_failure`) and `_blob_object_id(repo_root,
      main_oid, path)` at `:689` (which swallows `ContentResolutionError` and
      returns `None`, so an absent commit there would compare a real blob
      against nothing and emit a FALSE `HGR-RELEASE-SURFACE-DRIFT`). Both are
      masked today by `:723` raising first. If either still has a path to an
      unresolved object after 2.2, the resolution step is in the wrong place.

## 3. Implementation — the proofs

Fixtures follow the pattern this module already establishes:
`_bare_origin(tmp_path)` at `:128-133`, `_repo_with_committed_inventory`, and
`_git(repo, "remote", "add", "origin", str(origin))` — the local-directory
"remote" used by `test_verify_tag_rejects_a_tag_off_published_main` and
`test_verify_tag_reports_a_missing_remote_tag`.

- [ ] 3.1 **The skew regression.** Build the repository and its bare origin as
      today, push `main`, then clone the origin a SECOND time into a separate
      directory, commit there, and push — so the origin's `main` advances while
      the first repository's object store does not. Assert `verify_promotion`
      and `verify_tag` from the FIRST repository complete and return the same
      codes they return against a current clone. Today, before 2.2/2.3, this
      test raises `ReleaseDependencyError("commit reachability could not be
      determined")`, which is the point of writing it first.
- [ ] 3.2 **The masked second site.** A skew fixture that exercises
      `_surface_drift` specifically — remote `main` advanced AND a
      release-surface path differing between the candidate and the advanced
      main — asserting the drift verdict is the one the surface actually
      warrants and not an artefact of an unresolved object. This is the
      assertion that would have caught the `None`-comparison hazard in 2.5.
- [ ] 3.3 **The unavailable-object proof, mechanism per Q2.** First choice:
      after `ls-remote` is known to work, make the bare origin's `objects/`
      directory unreadable (`chmod 000`) so refs still advertise while a fetch
      cannot be served, and assert a `ReleaseDependencyError` whose message
      names the retrieval. THIS IS NOT MEASURED — if `git upload-pack` needs
      object access during advertisement, the fixture instead proves the
      pre-existing "remote main is unavailable" path and must be discarded.
      Fallback: monkeypatch `_run_git` (or the helper from 2.1) to fail only
      the fetch invocation. Measure before choosing, and do not keep a fixture
      that passes for the wrong reason.
- [ ] 3.4 **Pin the proofs to the defect.** Remove the resolution step alone and
      re-run 3.1 and 3.2: both must fail, reproducing the 128 refusal. A proof
      that still passes with the step removed is unpinned and gets rewritten —
      the discipline `test_mutation_reverting_parse_header_alone_reproduces_the_f5_divergence`
      established, and the reason 2.4 keeps `_is_ancestor`'s guard intact.
- [ ] 3.5 Confirm no existing assertion loosens. `test_verify_tag_rejects_a_tag_off_published_main`
      and `test_verify_promotion_rejects_an_already_published_tag` must keep
      their exact codes: a resolution step that made a genuinely off-main tag
      look reachable would be this change committing the sin it exists to
      prevent.
- [ ] 3.6 Bind the new proofs into `contracts/hermes-runtime/evidence-register.yaml`
      under the `SCO-002` scenarios they serve — `SCO-002-S02` (published-tag
      verify) and `SCO-002-S04` (offline verification) are the closest fits, and
      the register already lists the sibling tests there. Adding test node ids
      to an existing scenario is an in-place edit; do NOT add scenario ids, which
      the T011/T012 parity tests will reject.

## 4. Realization — the contract bundle

This change cannot land its code without re-cutting the bundle that describes
it. `scripts/hermes_runtime_validation/release.py` is a non-editorial member of
`contracts/releases/contract-v1.43.digests.yaml` (`:993-996`), and the recorded
digest `sha256:d149a34b...` is what the tree carries today — verified 2026-08-26
by `git cat-file blob HEAD:scripts/hermes_runtime_validation/release.py |
sha256sum`. The realization order is the one `contract-v1.10` used for this same
file (`contracts/CHANGELOG.md:2170-2185`) and the one recorded in the release
finishing recipe.

- [ ] 4.1 Allocate the bundle number at realization, NOT here. `contract-v1.43`
      is current; merge order decides the next minor, and the
      `contract-v1.28` renumber sweep is the precedent for why a proposal must
      not reserve one.
- [ ] 4.2 `contracts/manifest.yaml` — advance `contract_bundle_version`.
- [ ] 4.3 `contracts/CHANGELOG.md` — an additive entry stating the class and
      why the cut exists: a validator member's bytes moved, no schema changed,
      `contract_schema_version` unchanged, no instance valid at
      `contract-v1.43` narrowed, consumers pinned there remain conformant until
      they upgrade.
- [ ] 4.4 `scripts/validate-contract-release.py build --tag contract-v<next>
      --output contracts/releases/contract-v<next>.digests.yaml` — deterministic
      from manifest plus contract index, and RERUN after any further edit to an
      inventory member. Never hand-edit an inventory to match a tree; that is
      the shortcut `release-surface-integrity` forbids by name.
- [ ] 4.5 `verify-commit --commit HEAD` after committing, then
      `verify-promotion --commit <candidate> --remote origin --tag <tag>` BEFORE
      tagging. Note the fortunate property: this runs the NEW code, so the fix
      is exercised by the cut that carries it. `HGR-RELEASE-TAG-EXISTS` after
      the tag is pushed is the expected later state, not a failure.
- [ ] 4.6 Annotated tag on the merge commit on `main`, message style
      `contract-v<next> — additive: <summary>`. Then `verify-tag`.
- [ ] 4.7 Sync the aggregation-repo submodule pointer. The shared openxFactory
      checkout usually holds other sessions' uncommitted work — stage the
      gitlink directly with `git update-index --cacheinfo 160000,<sha>,openxFactory`,
      verify `git diff --cached --name-only` shows exactly that entry, and
      commit inside that verified window.

## 5. Verification

- [ ] 5.1 `python3 -m pytest tests/hermes_runtime_contracts -q` green. Baseline
      on this branch off `origin/main` at `23be0998`, measured 2026-08-26 in a
      fresh worktree: recorded in § 5.5 below. The suite passes at authoring
      because this packet changes no code, and because the object store of a
      fresh worktree holds the remote tip it was created from — which is
      precisely why the defect is invisible locally and only fires when the
      remote moves under a running suite.
- [ ] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate fix-release-reachability-race --strict`
      and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` both green.
- [ ] 5.3 THE GATE THAT MATTERS: reproduce the original failure deliberately.
      In a scratch clone, note the remote tip, advance the remote by one commit
      from a second clone, and run `validate_realization` from the first — it
      must refuse before 2.2/2.3 and complete after. A fix for a race that has
      never been observed failing under control is a fix on trust.
- [ ] 5.4 Re-run the full suite three times with a commit landing on the remote
      `main` inside each window, and confirm three identical verdicts. That is
      the property PR #372's three attempts did not have.
- [ ] 5.5 Record the authoring-time baselines in this file when measured, so a
      later reader can tell what moved: `tests/hermes_runtime_contracts` counts,
      `tests/doc-health` counts, and the two `openspec validate` totals. Note
      the known worktree hazard: `tests/doc-health`'s
      `test_derivation_reproduces_the_real_bootstrap_clusters` may red from an
      agent worktree for reasons this change does not touch — that is defect A
      of `harden-ideation-readiness-check`, already filed and merged, and it is
      noted rather than chased.
- [ ] 5.6 ARCHIVE AFTER REALIZATION. This change ships ACTIVE and archives only
      on merged-plus-green PLUS the bundle cut of § 4, following
      `add-family-enumeration-check` for the merge half and `contract-v1.10` for
      the cut half. The archive act is its own commit after the release.

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
