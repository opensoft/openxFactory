# Tasks: fix-content-resolution-conflation

Every measurement quoted below was taken 2026-08-28 in a fresh worktree off
`origin/main` at `6612d3239cbc99b73eb32cf76a861929aa901276`. A task that cites a
number owes a re-measurement at realization, not a copy of the number.

## 1. Admission

- [x] 1.1 Land the packet as an ACTIVE change with `Status: ratified`
      (the admission spelling: an approval act exists and is cited, per
      `sanction-ratified-record-spelling`), its
      `.openspec.yaml` recording the 2026-08-28 ad-hoc origin — Brett's verbatim
      selection "lets do all 3 in order" of the orchestrating session's
      recommended "the measured-latents bundle" — with the two voices kept
      apart, and the sibling `fix-pin-value-boundary-and-sentinel-split` named
      in `related:` as citing the same act.
      **DONE at filing.** The packet landed active with `Status: ratified` and
      its `.openspec.yaml` recording the 2026-08-28 ad-hoc origin, both voices kept
      apart, with the sibling named in `related:`. Filing evidence: pull request
      #463, merged 2026-08-28 as `5314fac5`.
- [x] 1.2 README "OpenSpec Records" active entry, stating the defect, the two
      ADDED requirements, the two-packet split, and — first, because it is what
      a reader needs to plan around — that a contract bundle cut rides the
      realization.
      **DONE at filing** (README `:505`), leading with the contract bundle cut
      that rides the realization, then the defect, the two ADDED requirements and
      the two-packet split. Landed by #463.
- [x] 1.3 `OPENSPEC_TELEMETRY=0 openspec validate fix-content-resolution-conflation --strict`
      and `--all --strict` green. Baseline before the pair: **76 passed, 0
      failed**.
      **DONE, re-measured at realization on this branch rather than copied.**
      `validate fix-content-resolution-conflation --strict` reports the change valid,
      exit 0. `--all --strict`: **80 passed, 0 failed**, exit 0 — the filing's
      baseline read 76 and the pre-realization baseline on this branch read 79; the
      item count moves as `main` lands changes, and the failure count is what this
      task asserts.
- [x] 1.4 § Orchestrator decisions OD-1 … OD-6 and § Open Questions Q1 … Q4 are
      open at filing. **OD-1 is the one that changes what was approved**; put it
      to Brett first, because merging the two packets back into one is cheapest
      before either is reviewed.
      **DONE — RULED 2026-08-28, ALL TEN, AND NOT ONE OF THEM MOVED DELTA
      TEXT.** A four-question multi-choice put to Brett by the orchestrating
      session over pull request #463 and relayed the same day: all six
      orchestrator decisions CLEARED AS AUTHORED, **including OD-1's
      re-sequencing of the approved 1, 2, 3 into {1, 3} then {2}, accepted on
      the record**, and all four questions RULED on the packet's own
      recommendation — Q1 `ReleaseDependencyError` wrapping the original with
      `from`, Q2 one declared code rather than fifteen, Q3 reuse of the existing
      fixture pair plus `test_content_resolution.py`, Q4 driving the failing
      condition by argument. `specs/shared-contract-ownership/spec.md` is
      byte-unchanged from the filing, which is checked rather than assumed.
      The mechanism, the date, the approver and the selections are recorded;
      no verbatim wording of the ruling reached this session, so none is
      quoted. Full record at `proposal.md` § Orchestrator decisions and
      § Open Questions.
      **WHAT THE SAME ACT ALSO SETTLED, and none of it is this session's to
      perform:** merge on green is APPROVED and is the ORCHESTRATING SESSION'S
      act; both realizations are PRE-COMMISSIONED TO DISPATCH IN ORDER once the
      filing lands — `fix-pin-value-boundary-and-sentinel-split` FIRST, then
      THIS PACKET, with its realization and its CANDIDATE inventory built in the
      realization pull request and `verify-promotion` plus the annotated tag
      left to the post-merge act exactly as the `contract-v1.44` precedent
      discharged them (§ 4.5); and the bundle state was RE-AFFIRMED at the
      ruling rather than carried from the filing — `contract-v2.0` is current
      and the cut allocates the NEXT number at merge order, so § 4.1's
      collision check still runs before any number is claimed. The conditional
      branch § 2.3 carried is settled and does not fire.

## 2. Implementation — the distinction

- [x] 2.1 Re-measure before editing. Confirm the raise-site count in
      `content.py` (**15 sites, 14 distinct messages** at filing), confirm that
      `content.py:125` is still the only one meaning "the tree was read and the
      path was not in it", and re-run the six-condition table from
      `proposal.md` § What was measured 2 against the tree as it then stands. If
      another session has already narrowed the catch, say so and re-scope
      rather than re-applying.
      **DONE, and the numbers hold.** `grep -c "raise ContentResolutionError"
      scripts/hermes_runtime_validation/content.py` → **15 sites**, and the distinct
      message set is **14** (`repository path is not canonical` is raised at `:47`
      and `:55`). `content.py:125` is still the only site reached after `rev-parse`
      resolved the commit AND its tree AND `ls-tree` ran — so still the only one
      meaning "the tree was read and the path was not in it". No other session had
      narrowed the catch: `_blob_object_id` was byte-identical to the filing's
      quotation and `_CommitSource.exists` to its.
      
      The six-condition table re-run against this repository at `6ce295c2`, with the
      underlying refusal captured beside each result, and **widened to seven** —
      the filing's "repository path is not a repository" row is split, because a
      path INSIDE a repository is not that condition at all and the honest drive
      needs a directory that is not one and a path that is not there:
      
      | condition | underlying refusal | code | `_blob_object_id` | `exists` |
      | --- | --- | --- | --- | --- |
      | blob genuinely absent at this commit | `exact Git path is unavailable` | `HRC-CONTENT-DEPENDENCY` | `None` | `False` |
      | the COMMIT does not exist | `exact Git object is unavailable` | `HRC-CONTENT-DEPENDENCY` | `None` | `False` |
      | a directory that is not a repository | `exact Git object is unavailable` | `HRC-CONTENT-DEPENDENCY` | `None` | `False` |
      | a repository path that does not exist | `Git repository is unavailable` | `HRC-CONTENT-DEPENDENCY` | `None` | `False` |
      | the path is a DIRECTORY, not a regular file | `Git path is not a supported regular file` | `HRC-CONTENT-DEPENDENCY` | `None` | `False` |
      | the path is not canonical | `repository path contains a forbidden segment` | `HRC-CONTENT-DEPENDENCY` | `None` | `False` |
      | the revision is not a full object id | `revision must be a full Git object ID` | `HRC-CONTENT-DEPENDENCY` | `None` | `False` |
      | **a real member** | — | — | `e8c0afa5…` | `True` |
      
      **Six failing conditions, one value, one code.** The first row is the only one
      that means anything about the release.
- [x] 2.2 `content.py:125` gains a declared code naming the absent-path
      condition. Purely additive: swept at filing, **nothing in this repository
      reads `ContentResolutionError.code` and the string
      `HRC-CONTENT-DEPENDENCY` occurs nowhere but its own default**. Re-sweep
      before relying on that.
      **DONE, and the sweep was re-run rather than relied on.** `content.py` now
      declares its vocabulary as two module constants — `CONTENT_DEPENDENCY =
      "HRC-CONTENT-DEPENDENCY"` (the unchanged default, now named rather than
      inlined) and `CONTENT_PATH_ABSENT = "HRC-CONTENT-PATH-ABSENT"` — and `:125`
      alone raises with the second.
      
      **THE RE-SWEEP CORRECTS THE FILING'S WORDING WITHOUT CHANGING ITS CONCLUSION.**
      The filing said the string `HRC-CONTENT-DEPENDENCY` "occurs nowhere but its own
      default". Measured now with `git grep`, it occurs in **five tracked files**:
      its own default, this packet's `proposal.md`, `design.md` and `tasks.md`, and
      `specs/005-customer-subject-runtime/us3-swarm-handoff/briefs/brief-validation-tooling.md:126`,
      which DOCUMENTS the default for a future consumer. That brief stays true,
      because the default's value is unchanged.
      
      **Nothing reads the code, and that is the load-bearing half.** Four `.code`
      readers exist in `scripts/` — `hermes-runtime-dataset-digest.py:109`,
      `validate-hermes-runtime-contracts.py:939`, `:1002` and `:1072` — and each was
      opened rather than counted: they read `MigrationContractError`,
      `DomainRegressionDependencyError`, `release.ReleaseDependencyError` and
      `ConsumerHandoffDependencyError` respectively. **Not one reads
      `ContentResolutionError.code`.** So the declaration is purely additive.
- [x] 2.3 `_blob_object_id` (`release.py:312-316`) returns `None` for that code
      alone and fails closed for everything else, with a reason naming the
      condition observed rather than a conclusion about the release. Per Q1's
      recommendation the refusal is `ReleaseDependencyError` wrapping the
      original with `from`; if Brett rules otherwise, record the ruling here.
      **DONE, on Q1's ruling.** The refusal is `ReleaseDependencyError`, wrapping the
      original with `from`, and its reason names the condition observed rather than a
      conclusion about the release: `release content could not be resolved at
      <commit>: <path>: <the resolver's own refusal>`. It takes the EXISTING
      `HGR-RELEASE-DEPENDENCY` default code — measured, not assumed: that code already
      occurs in `release.py` and `validate-hermes-runtime-contracts.py:974`/`:985`
      for exactly this class of refusal, so no finding code is added or re-scoped.
      
      **The distinction is made in ONE place, deliberately.** Both sites call a new
      `_resolution_established_absence(exc, commit, path)`, which returns `True` for
      `CONTENT_PATH_ABSENT` and raises for everything else. One site is what makes
      the § 3.7 mutation a single-token source edit rather than a rewrite.
- [x] 2.4 `_CommitSource.exists` (`release.py:401-405`) gets the same treatment
      (OD-5). Its four callers — `:519`, `:532`, `:611`, `:621` — decide release
      membership and whether `contracts/manifest.yaml` is present at the commit,
      so a `False` manufactured from an environment failure is a verdict about
      the release.
      **DONE.** Same helper, same rule: an established absence still returns `False`,
      every other condition refuses. Its four callers are unchanged. The `:611`
      consequence is proven rather than argued — see § 3.2's
      `test_an_unreadable_manifest_is_not_reported_as_a_release_without_one`, which
      drives `contracts/manifest.yaml` to a directory at a commit and asserts that
      `resolve_committed_inventory` refuses instead of answering `None`, which is what
      the committed module does (it is one of the ten RED failures).
- [x] 2.5 `HGR-RELEASE-PATH-UNRESOLVABLE` (`:713-719`) is NOT touched, and the
      requirement is scoped so that leaving it is conforming rather than a
      self-violation (OD-3, `design.md` § 4). Confirm at realization that the
      promoted wording still excludes it; if the wording moved in review, this
      task becomes a scope question rather than a silent inconsistency.
      **DONE — confirmed, and it is untouched.** `git diff` over
      `scripts/hermes_runtime_validation/release.py` shows no line inside `:713-719`
      changed; the `except ContentResolutionError:` there still emits the finding it
      always emitted. The promoted wording still excludes it: the requirement governs
      a resolution "reduced to a presence answer or a blob identity", and that site is
      reduced to neither — it emits a named finding. `specs/shared-contract-ownership/spec.md`
      is byte-unchanged from the filing, so this is not a scope question.
      The helper's docstring records the exclusion and cites OD-3 and § 7.1, so the
      next reader finds the decision at the site rather than only in the packet.
- [x] 2.6 Nothing about a successful resolution moves. Same return value, same
      comparison at `:796-798`, same finding codes, same severities, same exit
      codes, `_is_ancestor` byte-unchanged as `fix-release-reachability-race`
      § 2.4 protected it.

      **DONE, checked line by line rather than asserted.** `resolve_git_object`'s
      return value and `ResolvedGitContent` are untouched; the only `content.py`
      edits are the two new constants, the default rendered as a constant reference,
      and `code=CONTENT_PATH_ABSENT` at `:125`. In `release.py` the comparison at
      `_surface_drift` is byte-unchanged, no finding code, severity or exit code
      moves, and `_is_ancestor` is byte-unchanged as `fix-release-reachability-race`
      § 2.4 protected it (`git diff` touches neither its body nor its callers).
      The proof that the ordinary path did not move is § 3.1's pair plus the 63 of
      73 pre-existing tests in the two modules that pass identically before and
      after.
## 3. Implementation — the proofs

- [x] 3.1 The absent-path proof: a commit whose tree does not contain a
      release-surface path still reaches the release answer it reaches today,
      unchanged. This is the proof that catches an over-eager refusal, which is
      this fix's real failure mode.
      **DONE — two proofs, because absence has two directions and only the pair shows
      the answer is unchanged.**
      `test_a_release_surface_path_absent_at_both_commits_still_reports_clean`
      commits a tree without `contracts/hermes-runtime/README.md`, and asserts
      `_blob_object_id` is still `None`, `_surface_drift` still `[]`, and
      `verify_promotion` still `[]`.
      `test_a_release_surface_path_absent_on_one_side_alone_still_drifts` removes it
      at the published side only and asserts `HGR-RELEASE-SURFACE-DRIFT` is still
      emitted — absence still FEEDS the comparison as the release fact it is.
      **Both pass identically before and after the fix**, which is the point: they
      are the proofs that catch an over-eager refusal, so they are the two of twelve
      that are NOT in the RED set.
- [x] 3.2 The unavailable-store proof: a resolution failing for a reason other
      than absence produces a fail-closed refusal whose reason names the
      condition, not the release.
      **DONE — three proofs.**
      `test_an_unresolvable_content_question_refuses_instead_of_answering` drives
      three conditions by argument (an absent repository, a revision that is not an
      object id, a path with a forbidden segment) and asserts for each: a
      `ReleaseDependencyError`, `exit_code == 2`, the resolver's OWN condition
      quoted in the reason, the original preserved as `__cause__`, and — the half
      that matters — that the reason contains neither "drift" nor "unreachable", so
      it names the condition and not the release.
      `test_commit_source_exists_reports_absence_and_refuses_everything_else` does
      the same at the presence answer, asserting `True`/`False` unchanged for the
      two established cases.
      `test_an_unreadable_manifest_is_not_reported_as_a_release_without_one` carries
      it to the `:611` consumer.
- [x] 3.3 **The quiet-direction proof, which is the one that matters.** BOTH
      sides of a `_surface_drift` comparison fail; the verification must refuse,
      not report the surface undrifted. Today two `None`s compare equal and the
      surface reports clean having been read on neither side — assert the
      refusal, and assert that no `HGR-RELEASE-SURFACE-DRIFT` finding is emitted
      either, because the failure has two wrong answers and only one of them is
      loud.
      **DONE — two proofs, one per drive, and the committed behaviour is recorded.**
      `test_a_comparison_that_resolved_neither_side_refuses_rather_than_passing`
      commits a DIRECTORY at the release-surface path
      `contracts/hermes-runtime/README.md` and compares that commit against itself —
      the ordinary shape of a promotion check for a candidate already on `main` — so
      BOTH reads take the same safety refusal. **Against the committed module
      `_surface_drift` returns `[]` and `verify_promotion` reports the surface clean,
      having read it on neither side.** The proof asserts the refusal, asserts the
      reason names `Git path is not a supported regular file` and the path, and
      asserts the refusal is NOT an `HGR-RELEASE-SURFACE-DRIFT` finding either —
      the failure has two wrong answers and only one of them is loud.
      `test_the_quiet_direction_driven_by_argument_refuses_on_both_sides` drives the
      same failure by ARGUMENT at the exact expression `_surface_drift:796-798`
      evaluates, asserting each of the two operands refuses rather than returning a
      `None` that could compare equal to the other.
- [x] 3.4 The safety-refusal proof: a release-surface path that is a directory
      or a nested repository link at one commit is refused, not read as absence.
      Reachable from committed data rather than only from a broken environment,
      which is why it is a proof and not a note.
      **DONE, parametrized over both committed shapes.**
      `test_an_unsafe_release_surface_object_is_refused_not_read_as_absence[directory]`
      and `[gitlink]` commit a directory and a nested repository link respectively at
      the release-surface path on the PUBLISHED side, leaving the candidate reading
      cleanly — asserted in the proof before the hazard is applied. Against the
      committed module each produces `HGR-RELEASE-SURFACE-DRIFT`: a drift verdict
      manufactured from a deliberate safety refusal. Both now refuse, and neither is
      softened because the other commit resolves. **Reachable from committed data,
      with no broken environment anywhere in the fixture**, which is why the spec
      states it as a scenario rather than a note.
- [x] 3.5 Per Q3, the release-surface proofs reuse the `_bare_origin` /
      `_repo_with_committed_inventory` fixture pair already in
      `tests/hermes_runtime_contracts/test_release_inventory.py`, and the
      resolver proofs go in `test_content_resolution.py`, beside the fifteen
      refusals they distinguish.
      **DONE.** The ten release-surface and membership proofs live in
      `tests/hermes_runtime_contracts/test_release_inventory.py` on the
      `_bare_origin` / `_repo_with_committed_inventory` pair. The pair was REUSED
      rather than copied: `_repo_with_committed_inventory` gained one optional
      keyword-only `hazard` hook that runs AFTER the inventory is built, so the
      committed inventory stays the one the ordinary fixture produces and only the
      release SURFACE carries the condition. Its four existing callers are
      unchanged. The two resolver proofs are in `test_content_resolution.py`, beside
      the fifteen refusals they distinguish.
- [x] 3.6 Per Q4, the failing conditions are driven by ARGUMENT (a non-canonical
      path, an absent repository) rather than by a real timeout, and each proof
      says so. The requirement is about the distinction, not about any one way
      of failing.
      **DONE, and each proof says which drive it uses.** No proof waits on a real
      timeout. The argument drives are an absent repository, a revision that is not
      a full object id, and a path with a forbidden segment; the committed-data
      drives are a directory, a nested repository link and a genuinely absent path.
      **The distinction between the two drives is stated rather than blurred**: the
      committed-data hazards are used where the requirement's own scenario is about
      committed state (§ 3.4, and the quiet direction reached through
      `verify_promotion`), and the argument drives where the condition is the
      environment (§ 3.2, and the quiet direction at the comparison expression).
      Both are mechanism-independent under § 3.7's pinning rule, which is Q4's
      argument.
- [x] 3.7 Mutation-pin at SOURCE level: flatten the distinction back to a single
      value and every refusal proof must fail, while the absent-path proof must
      still pass. A proof that survives the flattening is unpinned and gets
      rewritten rather than accepted — the rule the sibling family's third
      requirement states in its own third scenario.
      **DONE — THREE mutations at source level, and every one of the twelve proofs is
      pinned by at least one.** Each mutation replaces the single line
      `if exc.code == CONTENT_PATH_ABSENT:` in `_resolution_established_absence` and
      runs the twelve new node ids; the file is restored from a byte-copy after each.
      
      | mutation | what it does | proofs that fail |
      | --- | --- | --- |
      | **M1** `if True:` | flattens every refusal back to absence — the committed defect exactly | **all 7 refusal proofs**; both absent-path proofs still PASS |
      | **M2** `if False:` | flattens the one data answer into a refusal | **both absent-path proofs**, and the `exists` proof that asserts both directions |
      | **M3** `if "exact Git path is unavailable" in str(exc):` | substitutes the REJECTED mechanism (OD-4) — a matched message for a declared code | **the structural proof, and nothing else** |
      
      **M3 IS THE MEASUREMENT OD-4 WAS ARGUED FROM, AND IT WAS ARGUED BEFORE IT WAS
      MEASURED.** Under M3 all nine behavioural proofs stay green, because the
      message matches TODAY. Only
      `test_the_distinction_is_carried_by_the_declared_code_not_by_the_message` — a
      structural assertion over `release.py`'s source, that it names
      `CONTENT_PATH_ABSENT` and does not carry the resolver's prose — reddens. So a
      future editor improving that message would break nothing a behavioural suite
      could see, which is exactly the silent reclassification OD-4 rejected the
      mechanism for. The same shape the sibling packet reported for its prose
      patterns (#478, M3/M4).
      
      **And the RED baseline, taken separately from the mutations:** with the two
      source files restored from `HEAD` and the new tests left in place, **10 of the
      12 fail**. The 2 that pass are § 3.1's pair, which must pass — they assert the
      answer is unchanged. No proof was accepted that survived every mutation.
- [x] 3.8 If the new scenarios are bound in
      `contracts/hermes-runtime/evidence-register.yaml` alongside the existing
      `SCO-002-S03` binding to
      `test_verify_promotion_rejects_a_drifted_release_surface`, note that the
      register is ITSELF an inventory member (`type: evidence-register`) — so
      the binding rides the same cut, and § 4 must be rebuilt after it, not
      before.

      **DONE, and the ordering it warns about was honoured.** Twelve node ids are
      bound in `contracts/hermes-runtime/evidence-register.yaml` under the `SCO-002`
      scenarios they serve — six under `S03` (pinned file drifts: the two absence
      proofs, both quiet-direction proofs and both unsafe-object parameters) and six
      under `S04` (verification without a usable network: the three unavailable-store
      proofs, the structural proof and the two resolver proofs). Test node ids added
      to EXISTING scenarios; no scenario id added, on the `contract-v1.44` pattern.
      The register is an inventory member (`type: evidence-register`, confirmed by
      parse) and **its digest moved**, so § 4's build ran AFTER this edit, not
      before — the three moved non-editorial digests are `release.py`, `content.py`
      and this file.
## 4. Realization — the contract bundle

This change cannot land its code without re-cutting the bundle that describes
it. Measured at filing by PARSE:
`contracts/releases/contract-v2.0.digests.yaml`, 192 entries,
`scripts/hermes_runtime_validation/release.py` present as `type: validator`,
`digest: sha256:660e55ca7e6896ea24106483b926e1919a0cb195ef8b9a700a3522f1f393f6b0`,
which is exactly `sha256sum` of the tree's copy; `content.py` present on the
same terms; the editorial set is three files and neither is in it. The
realization order is the one `contract-v1.44` used for this same file, two days
before this filing, and the one recorded in the release finishing recipe.

- [x] 4.1 **Allocate the bundle number at realization, NOT here.**
      `contract-v2.0` is current; merge order decides the next minor, and the
      `contract-v1.28` renumber sweep is the precedent for why a proposal must
      not reserve one. Collision-check both ways the recipe asks for before
      claiming a number: `git ls-tree origin/main contracts/releases/` and
      `git ls-remote --tags origin 'refs/tags/contract-v2.*'`, plus a scan of
      open pull requests for any that touches a release surface.
      **DONE — `contract-v2.1`, and the collision check ran both ways the recipe asks
      for, twice: at cut time and again immediately before the final push.**
      `git ls-tree origin/main contracts/releases/` → the highest inventory present
      is `contract-v2.0.digests.yaml`. `git ls-remote --tags origin
      'refs/tags/contract-v2.*'` → `contract-v2.0` and nothing else; the full
      `contract-v*` list ends `…v1.45, v1.46, v1.47, v2.0`. And every open pull
      request was enumerated and its changed-file list read: **none of the seven
      touches `contracts/releases/`, `contracts/manifest.yaml` or
      `contracts/CHANGELOG.md`**, so no other branch is racing for a minor. The
      `contract-v1.28` renumber sweep is why the second check happens at push rather
      than only here.
- [x] 4.2 `contracts/manifest.yaml` — advance `contract_bundle_version` (`:3`).
      Expect this to be the only manifest edit: this change touches no schema,
      so no schema row digest moves. The historical prose mentions of earlier
      bundles deeper in the file are consumption-rule text and are left alone.
      **DONE, and it was the only manifest edit**, as expected: this change touches
      no schema, so no schema row digest moved. `git diff` over
      `contracts/manifest.yaml` is **one line** — `:3`, `contract-v2.0` →
      `contract-v2.1`. The historical prose mentions of earlier bundles deeper in the
      file are consumption-rule text and were left alone.
- [x] 4.3 `contracts/CHANGELOG.md` — an additive entry stating the class and why
      the cut exists: two validator members' bytes moved, no schema changed,
      `contract_schema_version` unchanged, no instance valid at `contract-v2.0`
      narrowed, consumers pinned there conformant until they upgrade. Name the
      `contract-v1.44` and `contract-v1.10` precedents for this same file.
      **DONE.** The `contract-v2.1` entry states the class and discharges each of its
      clauses: no schema bytes move, `contract_schema_version` unchanged, no instance
      valid at `contract-v2.0` narrowed, consumers pinned there conformant until they
      upgrade, and no finding code added, removed, renamed or re-severitied — the new
      refusals take the existing `HGR-RELEASE-DEPENDENCY` class. It names the cause as
      MEMBERSHIP rather than preference, with the parse evidence, and names the
      `contract-v1.44` and `contract-v1.10` precedents for this same file.
- [x] 4.4 `scripts/validate-contract-release.py build --tag contract-v<next>
      --output contracts/releases/contract-v<next>.digests.yaml` — deterministic
      from manifest plus contract index, and RERUN after ANY further edit to an
      inventory member, including the evidence register (§ 3.8). Build twice to
      distinct paths and prove the outputs byte-identical. **Never hand-edit an
      inventory to match a tree**; that is the shortcut `release-surface-integrity`
      forbids by name. Expect `entries=192` unchanged — nothing joins or leaves
      the bundle — and expect the two moved digests to be exactly `sha256sum` of
      the edited files.
      **DONE, built THREE times and never hand-edited.** Two builds to distinct
      scratch paths are byte-identical under `cmp`; a third build to the tree path is
      byte-identical to the first, which also shows the candidate's own presence in
      `contracts/releases/` does not perturb the build. Rerun AFTER the evidence
      register edit, per § 3.8.
      
      **`entries=192`, unchanged — nothing joined or left the bundle**, and the
      membership sets are equal path-for-path by parse, not by count alone.
      **Exactly five digests moved**: the two editorial members re-baselined
      (`contracts/manifest.yaml`, `contracts/CHANGELOG.md`) and the three
      non-editorial members this change edited
      (`scripts/hermes_runtime_validation/release.py`,
      `scripts/hermes_runtime_validation/content.py`,
      `contracts/hermes-runtime/evidence-register.yaml`). Each of the five equals
      `sha256sum` of the edited file.
- [x] 4.5 `verify-commit --commit HEAD` after committing. Then
      `verify-promotion --commit <candidate> --remote origin --tag <tag>` BEFORE
      tagging — which cannot be done before the merge, because it requires the
      candidate to be reachable from the remote's `main`. Per the
      `contract-v1.44` precedent this arm discharges PARTIALLY at the pull
      request and completes post-merge, and the annotated tag is not the
      authoring session's act unless it is explicitly given.
      Note the fortunate property that precedent also records: the cut runs the
      NEW code, so the fix is exercised by the release that carries it.

      **PARTIALLY DISCHARGED, on the `contract-v1.44` precedent, and the remainder is
      deliberately not this session's.** `python3 scripts/validate-contract-release.py
      verify-commit --commit HEAD` → `release verify-commit: pass`,
      `inventory=contracts/releases/contract-v2.1.digests.yaml`, **exit 0**.
      
      `verify-promotion --commit <merge> --remote origin --tag contract-v2.1` CANNOT
      run before the merge, because it requires the candidate to be reachable from
      the remote's `main`, and the annotated tag is not the authoring session's act.
      Both are left to the orchestrating session; § 6.2 is where they are recorded.
      
      And the fortunate property the precedent records holds again: **the cut runs the
      NEW code.** `verify-commit` above executed the fixed `_blob_object_id` and
      `_CommitSource.exists`, and `verify-promotion` will too — so the fix is
      exercised by the release that carries it before that release is tagged.
## 5. Verification

- [x] 5.1 `set -o pipefail; python3 -m pytest tests/hermes_runtime_contracts -q`
      — exit code READ, never inferred from the tail of the output. This
      repository has merged two pull requests red by inferring it.
      **DONE. Exit code READ from `$?` and written to the log file, never inferred
      from a tail.** The selection is the one CI runs — `-m "not postgres"`, which
      `tests/conftest.py:8` names as the repository's own invocation — because the
      `postgres` marker drives a Docker Compose harness that no local run here can
      serve.
      
      | | before (branch at `6ce295c2`, no edits) | after |
      | --- | --- | --- |
      | result | **1 failed, 509 passed**, 338 deselected | **522 passed, 0 failed**, 338 deselected |
      | exit | **1** | **0** |
      | wall | 432.38s | 319.12s |
      
      **+12 collected is exactly this packet's twelve new node ids** — two in
      `test_content_resolution.py`, ten in `test_release_inventory.py` (nine
      functions, one of them parametrized into two).
      
      **THE ONE BASELINE FAILURE IS THE KNOWN ENVIRONMENT ARTIFACT, AND IT IS NOT
      WAVED AT.** `test_validator_cli.py::test_release_mode_field_is_preserved_on_the_real_repository[--require-realization-realization]`
      is a 30-second `subprocess.TimeoutExpired` on
      `scripts/validate-hermes-runtime-contracts.py`. It was reproduced IN ISOLATION
      on the UNEDITED tree before a single character was changed (1 failed, 1 passed),
      and the cause was measured rather than guessed: the CLI itself takes **~40s
      wall** on this machine against a 30s allowance, under contention from other
      sessions' concurrent pytest runs. The sibling packet reported the same failure
      on its own branch (#478) and proved it pre-existing at the merge base. It
      PASSES on the after-run, on the same tree that carries this fix, which is the
      strongest available statement that it is load and not code.
- [x] 5.2 `set -o pipefail; python3 -m pytest tests/doc-health -q` green too:
      the release-inventory-drift family reads the inventory this change
      re-cuts, so a mis-built inventory shows up here as well as in the release
      verifier. Baseline at filing: **1249 passed, 0 failed, exit 0**.
      **DONE. Before: 1330 passed, 0 failed, exit 0** (208.75s). **After: 1333
      passed, 0 failed, exit 0** (211.99s). The **+3 is `origin/main`**, not this
      packet: the baseline was taken before this branch merged `origin/main`, which
      landed `settle-aging-staging-topics`' staged-topic-outcome fixtures. This
      packet adds no doc-health test and edits no doc-health module.
      
      **And the family this task exists for was run directly on this head, not merely
      inferred from the suite:** `python3 scripts/doc-health.py --single-repo .
      --family release-inventory-drift` reports **No findings, exit 0** — before the
      cut and after it. That family reports at `error` when a NON-EDITORIAL member's
      bytes differ from the declared inventory, which is exactly the state this
      change would have left behind without the cut, and exactly why the cut rides
      in this pull request rather than following it.
- [x] 5.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
      **DONE. 80 passed, 0 failed, exit 0**, and
      `validate fix-content-resolution-conflation --strict` reports the change valid,
      exit 0. The item count reads 80 here against 79 at this branch's pre-edit
      baseline and 76 at filing; `main` lands changes between measurements, and the
      assertion this task carries is the **0 failed**.
- [x] 5.4 Re-affirm by PARSE that the rebuilt inventory reproduces the COMMITTED
      tree, not just the working tree — which is what `verify-commit` answers
      and what a `sha256sum` of the working file does not.

      **DONE, against the COMMITTED tree rather than the working one, and by parse
      rather than by `sha256sum` of a working file.** At the cut commit
      `7b1e9291`: the committed `contracts/releases/contract-v2.1.digests.yaml` was
      read out of the object store with `git cat-file`, loaded with a YAML parser
      (`bundle_tag: contract-v2.1`, **192 entries**), and an inventory was REBUILT
      from `_CommitSource(repo, HEAD)` — the exact-commit source, which never reads
      the working tree. `dump_inventory(rebuilt) == committed bytes` → **True**.
      
      Then every entry independently: each of the **192** declared digests was
      compared against `sha256` of that path's blob AT THE COMMIT, read with
      `git cat-file blob HEAD:<path>`. **192 of 192 match, 0 mismatches.**
      `verify-commit --commit HEAD` answers the same question through the shipped
      verifier and reports `pass`, exit 0.
## 6. Archive gate

- [ ] 6.1 Merged to `origin/main` with both required checks green, the merge
      commit re-verified an ancestor of `origin/main` and a real two-parent
      merge read out of `git cat-file -p` rather than off the pull request page.
- [ ] 6.2 The cut complete: manifest, changelog, digest inventory and a verified
      annotated tag all agreeing on the new bundle, `verify-tag --remote origin
      --tag contract-v<next>` exit 0, and the aggregation submodule pointer
      synced.
- [ ] 6.3 On the merged tree: both suites green under `set -o pipefail`,
      `openspec validate --all --strict` green, and the release-inventory-drift
      family reporting no `error` for either moved member.
- [ ] 6.4 Every § 7 follow-up carries a disposition rather than a blank box, and
      every OD and Q carries a ruling or an explicit carry-forward.

## 7. Open — deliberately not closed by this change

- [ ] 7.1 **`HGR-RELEASE-PATH-UNRESOLVABLE` (`release.py:713-719`) CONVERTS
      EVERY `ContentResolutionError` FROM `read_member` INTO A FINDING ABOUT THE
      INVENTORY PATH.** Measured here, not inherited. Milder than the two sites
      this packet fixes — it emits a named finding rather than silence — but it
      still turns an environment failure into a verdict about the release. Left
      because changing it changes what a PUBLISHED finding code means to
      consumers reading verifier output, which is a contract question rather
      than a defect fix. The requirement is scoped so that leaving it is
      conforming (OD-3), which is a decision and not an oversight.
      **DISPOSITION: STILL OPEN, DELIBERATELY, AND NOW WRITTEN DOWN AT THE SITE.**
      Confirmed untouched at realization: no line of `release.py:713-719` changed,
      and the finding it emits fires on exactly the population it fired on before.
      What this packet ADDS to the item is a note the next reader will find without
      this file: `_resolution_established_absence`'s docstring records the exclusion
      and cites OD-3 and this task, so the boundary is legible from the code rather
      than only from the packet. The reason for leaving it is unchanged and is a
      contract question, not a defect judgement — that site reduces to a NAMED
      FINDING rather than to a value, so a reader sees it; changing it changes what
      a published code means to consumers reading verifier output. The promoted
      requirement's scope ("reduced to a presence answer or a blob identity") still
      excludes it, so leaving it is conforming.
- [ ] 7.2 **THE SWEEP OF `scripts/hermes_runtime_validation/` FOR THE SAME
      PATTERN.** `fix-release-reachability-race` § 6.1 opened this for the
      reachability layer and named `consumer_handoff.py` as the obvious next
      candidate; the content layer owes the same sweep. This packet measured
      `release.py` and claims nothing about the rest, on that packet's own rule:
      a sweep asserted without measurement is the same species of unearned
      answer these packets are about.
      **DISPOSITION: STILL OPEN, AND THIS PACKET STILL CLAIMS NOTHING ABOUT THE REST
      OF THE PACKAGE.** `release.py` and `content.py` were measured and fixed;
      `consumer_handoff.py`, `migration.py`, `domain_regression.py` and the rest were
      NOT measured here and no assertion about them is made — on the inherited
      packet's own rule, a sweep asserted without measurement is the same species of
      unearned answer these packets exist to close. One thing the realization DID
      establish incidentally, and it is a measurement rather than a claim about
      behaviour: `consumer_handoff.py:41` and `migration.py:139` both define their own
      `.code` attribute, so the mechanism this packet used — a declared code read by
      the caller — is available to them unchanged if that sweep is ever run. The
      sweep still owes its own packet with its own measurement.
- [ ] 7.3 **THE ELEVEN-MINUTE EXPOSURE WINDOW**, § 6.2 of the same packet.
      Sharding, or exercising the realization path against a pinned fetch rather
      than the live remote, would shrink it. Both are `pytest-suite.yml`
      questions rather than obligations about the verifier.
      **DISPOSITION: STILL OPEN, UNMOVED, AND OUT OF THIS PACKET'S REACH.** Both
      remedies named — sharding, and exercising the realization path against a pinned
      fetch rather than the live remote — are `pytest-suite.yml` questions rather than
      obligations about the verifier, and this packet edited no workflow. Measured
      here only in passing, and worth recording because it is adjacent: the local
      `tests/hermes_runtime_contracts` selection CI runs takes about seven minutes on
      this machine, so the window is a property of the workflow's shape rather than
      of any one suite's length.
- [ ] 7.4 **WHETHER `content.py` SHOULD DECLARE A CODE PER CONDITION RATHER THAN
      ONE.** Q2 recommends one, on the ground that the remaining fourteen are
      all "the question could not be asked" and a vocabulary nothing consumes is
      the drift the sentinel declaration's second direction exists to report. If
      a second caller ever needs to distinguish two of the fourteen, that is the
      evidence a wider vocabulary would need, and this item is where the next
      reader should find that said.

      **DISPOSITION: RULED FOR NOW (Q2, 2026-08-28) AND THE ITEM STAYS OPEN AS THE
      PLACE THE EVIDENCE WOULD LAND.** Realized as ONE code: `CONTENT_PATH_ABSENT`
      for the absent-path condition, with the remaining fourteen keeping the
      unchanged `CONTENT_DEPENDENCY` default. The ruling's ground held at
      realization rather than only at filing — the two callers fixed here need
      exactly one distinction between them, and a code per raise site would have
      been a vocabulary nothing consumes, which is the drift the sentinel
      declaration's second direction exists to report. **WHAT WOULD REOPEN IT,
      stated so the next reader can recognize it:** a second caller needing to tell
      two of the fourteen apart — most plausibly telling a genuine store timeout
      (`Git content dependency is unavailable`, `content.py:82`) from a malformed
      argument, because those two want different operator actions. That evidence
      does not exist yet, and the constants are module-level, so adding a third is
      additive when it does.