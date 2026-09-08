# Tasks: bump-openspec-cli-pin-to-1.12

Status: draft

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in
`evidence/pin-bump-1.12-2026-09-05.md`. Group 5 is DRAFTED-NOT-DONE work and
group 6 is OWED work; neither is ticked and each names why. **AMENDED 2026-09-08: EVERY BOX IN THIS PACKET IS NOW
TICKED.** Group 6 was discharged in four separate pull requests, each with its
own evidence beside it — 6.1 (the ratification record) and 6.2 (the
`pytest-suite.yml` literal) on 2026-09-05, 6.3 (the three remaining consuming
repositories) and 6.4 (the dependency closure, by
`pin-openspec-cli-dependency-closure`) on 2026-09-08 — and 5.1's upstream draft
was filed with group 5. Was: **AMENDED 2026-09-05:** two of group 6 have since
been discharged in their own pull requests and are ticked with the evidence
beside them — 6.1 (the ratification record) and 6.2 (the `pytest-suite.yml`
literal). 5.1, 6.3 and 6.4 are untouched and still owed.

**RATIFICATION HAS NOT HAPPENED.** Brett Heap ruled *"take exit 2"* on
2026-09-05, deciding WHICH of the three exits #673 enumerated is taken. That
settles the substance of the approach and does not ratify this text. Task 6.1
records ratification when it happens; nothing below decides it.

**THIS PULL REQUEST IS HUMAN-ONLY** under the ratified requirement *"A pinned
CLI version bump is one human-only act…"*. It moves the pin, and a council or
other automated authority MUST NOT clear it: the candidate would otherwise
repoint the very tool that judges its own change.

---

## 1. The referent, recomputed rather than copied

- [x] 1.1 `npm pack @fission-ai/openspec@1.12.0` fetched the real published
      tarball (477,381 bytes, 389 files) and BOTH hashes were recomputed over
      those bytes by this lane, as #667 did for `1.2.0`:
      `sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrNiozOwv++CQhW+MG0kuP1XLZ/uQrrWw==`
      and `c844543999f673cdd72445879b86a4abea4c07ef`. Both equal the values the
      registry publishes; had they differed the lane was instructed to refuse
      and would have.
- [x] 1.2 `contracts/openspec-cli-pin.yaml`: `version`, `integrity`, `shasum`
      and `tarball` moved TOGETHER. The `version` string is still a LABEL and
      the SHA-512 is still the referent; the header's tag-versus-referent
      argument is kept and only its worked example is re-cut.
- [x] 1.3 The previous referent recorded as `rollback:`, in the pin's own
      grammar rather than in prose, with `superseded_on`, `superseded_by`, and
      the fact that a rollback must DROP the dispositions with the version
      (they exist only because `1.12.0` raises findings `1.2.0` does not).
- [x] 1.4 The header's factual claims re-derived at the new version rather
      than carried: 389 files rather than 270, and the dependency-closure
      shortfall restated with the real numbers — TEN dependencies, nine caret
      and one (`cross-spawn 7.0.6`) exact, where `1.2.0` declared nine all
      caret. Two stale `1.2.0` mentions outside the pin corrected in the same
      pass: one npx example in the validator's docstring, and one comment in
      `.github/workflows/openspec-cli-pin-gate.yml` naming the old artifact's
      `engines.node` floor. Neither is logic; the gate still carries no copy of
      the version, which its own test asserts.

## 2. The disposition mechanism

- [x] 2.1 `scripts/validate-openspec-cli-pin.py`: check 6. The pinned CLI runs
      with `--json`, `parse_report` reads the verdict (both array shapes),
      `collect_findings` flattens it, `reconcile` matches ERROR-level findings
      to in-scope dispositions in BOTH directions.
- [x] 2.2 `pinned_dispositions` refuses `pin-disposition-malformed` for a
      missing `repo`/`item`/`path`/`finding`/`why`, an absent or EMPTY
      `cited_to:`, no `ratified_by:`/`recorded_by:`, a declared `level:` the
      matcher could never reconcile, or two entries covering one finding —
      evaluated in check 1, BEFORE any registry round trip.
- [x] 2.3 `pin-disposition-stale`, exit 2, for a disposition matched by no
      finding in a WHOLE-CORPUS run, with the asymmetry argued in the code and
      in `design.md` § 2. A NARROWED (`--change`) run applies its dispositions
      and decides no staleness, and says so in its output — found by running
      `--change add-composed-view-authoring` against the real corpus and
      watching it refuse over the other, untouched entry.
- [x] 2.4 `repository_identity` reads `git config --get remote.origin.url`, so
      a disposition is scoped to one repository and a worktree named for its
      branch is not mistaken for a different tree. `pin-repo-unidentified`
      where it cannot be read AND dispositions are declared.
- [x] 2.5 `report_dispositions` PRINTS every applied exception by name, with
      its `why`, its citations and the human who granted it, before any verdict
      is announced; and the success line says `THIS IS NOT A CLEAN TREE`.
- [x] 2.6 The narrow pin reader widened by exactly two admitted forms — a
      one-level nested list and the folded `>-` scalar — with `|`, `|-`, `>+`
      refused as `pin-unreadable`.
- [x] 2.7 The 1.2.0-era behaviour is a BRANCH, not a promise: a pin with an
      absent or empty `dispositions:` takes the original streaming path with no
      `--json`, no parsing and no git call. Pinned by a test that asserts the
      absence of both.
- [x] 2.8 Unchanged and re-asserted by the tests that already pinned them: the
      five original checks and their ORDER, integrity-before-install, the
      PATH-version refusal, the no-target refusal, the absence of a
      `--verify-only` mode, the fixed remediation trailer, exit-code semantics.

## 3. The two dispositions

- [x] 3.1 `add-chain-attestation` / `signed-execution-chain/spec.md`, cited to
      the promoted marker requirement (`openspec/specs/doc-health/spec.md:1770`),
      council LA-A1, #673's evidence record, and the marker in the block itself.
- [x] 3.2 `add-composed-view-authoring` / `ideation-dashboard/spec.md`, cited to
      canon's worked example (which IS this rename), PR #444, council LA-A1 and
      #673's evidence record.
- [x] 3.3 Both carry `ratified_by: Brett Heap, 2026-09-05, "take exit 2"`, a
      one-line `why:`, and a `retires_when:` naming the archive that makes them
      stale.
- [x] 3.4 The pin's `finding:` strings reconciled OFFLINE against the CAPTURED
      real report bytes by a test, so a transcription slip surfaces on a
      developer's machine rather than as a red gate.

## 4. Evidence and tests

- [x] 4.1 81 tests in `tests/openspec_cli_pin/` (was 41), green.
- [x] 4.2 Two CAPTURED REAL `1.12.0` reports committed as fixtures, covering
      both array keys the tool emits.
- [x] 4.3 `evidence/pin-bump-1.12-2026-09-05.md`, `Status: record`: the
      recomputed hashes, BEFORE at the `1.2.0` pin, AFTER at the `1.12.0` pin,
      the RAW `88 passed, 2 failed` shown verbatim beside the reconciled
      `0 undispositioned`, the PATH-mode refusal demonstrated, and the
      consuming-repository measurement.
- [x] 4.4 OpsxFactory measured through the NEW entrypoint at `origin/main`
      `3ca4925f` (read-only worktree; nothing committed there):
      **47 passed / 0 failed (47 items)**, exit 0, no disposition in scope.
- [x] 4.5 The stale path is exercised by a test that runs the SAME pin against a
      corpus in which the finding no longer occurs — the state the day
      `add-composed-view-authoring` archives — and asserts exit 2; and its
      counterpart asserts that a NARROWED run applies its dispositions, decides
      no staleness, and declares that it did not.

## 5. Exit 3 — drafted, NOT taken

- [x] 5.1 File `evidence/upstream-issue-draft-merged-into-marker.md` with
      `fission-ai/openspec`. **AMENDED 2026-09-06:** filed 2026-09-05 as
      Fission-AI/OpenSpec#1793
      (https://github.com/Fission-AI/OpenSpec/issues/1793), open, under
      Brett Heap's GitHub account on his word "file the upstream issue", by
      lane codexfactory-0d; recorded in the evidence file by openxFactory
      #682 (`ff31fc7f`). The box is ticked 2026-09-06 by lane codexfactory-1
      on Brett Heap's word "go" (2026-09-06), which admitted the tick as
      part of the pin-consumer work. Was: **DELIBERATELY NOT DONE.** The
      draft is complete and carries the minimal reproduction; filing it is
      Brett's act. Exit 2 and exit 3 are not exclusive — exit 2 is what this
      estate does about its own gate, exit 3 is what it asks of the tool —
      and if upstream lands a fix the dispositions go STALE on the next bump
      and the mechanism removes them.

## 6. Owed, and named rather than discovered later

- [x] 6.1 **(DONE 2026-09-05 — `review/ratification-2026-09-05.md`, verbatim "ratify 677"
      heard first-hand by opsXfactory-1; the merge preceded the record on Brett's word
      in the authoring lane, and the record says so.)** Ratification of this packet's text by Brett Heap, recorded as a
      `Ratified by:` line and a `review/` record. *"take exit 2"* settled the
      approach and not the text.
- [x] 6.2 **(DONE 2026-09-05, PR #687 — the disagreement is closed.)**
      `.github/workflows/pytest-suite.yml` no longer installs by literal: it runs
      `scripts/install-pinned-openspec-cli.py`, which resolves the artifact
      through THIS pin's own verifier (`read_pin` → `resolve_pinned` →
      `assert_reported_version`) and puts the verified executable on
      `$GITHUB_PATH`. `tests/proposal-support/` therefore drives the same
      `1.12.0` bytes the gate verifies, and the version is written in one place.
      Proved before landing: with that binary on PATH,
      `tests/proposal-support` reports **36 passed, 0 skipped**, so the three
      `skipUnless(shutil.which("openspec"))` tests RUN and `EXPECT_SKIPPED: "21"`
      does not move. The stale prose is corrected in the same diff, dated, in the
      pin header, the verifier's docstring and the gate's comment. Was: the
      literal now DISAGREES with the pin; this is #667's open task 5.1 and its
      own diff, over this repository's most load-bearing required check; it is
      not ridden on this pull request. Until it lands,
      `tests/proposal-support/` drives a `1.2.0` binary while the gate validates
      at `1.12.0` — which is the two-copies-of-a-pin defect #667 named, now
      visible rather than latent.
- [x] 6.3 **(DONE 2026-09-08, via two landings apiece in three repositories.)**
      The remaining consuming repositories named by this task — MedxFactory,
      LedgerxFactory, AdxFactory — are now wired to this entrypoint, and
      codexFactory already was (see the `AMENDED 2026-09-06` note below), so
      every repository this task names is wired and the box ticks.
      MedxSoft/MedxFactory #25 `prepare-openspec-1.12-readiness` (`3d8cef76`,
      merged) and #28 `adopt-openspec-cli-pin-gate` (`9884668d`, merged) took
      MedxFactory's gate reading from `9 passed, 4 failed` to `14 passed, 0
      failed` and then wired `.github/workflows/validate.yml`; CI's gate at
      the pin: `Totals: 15 passed, 0 failed`. ledgerXfactory/LedgerxFactory
      #32 `prepare-openspec-1.12-readiness` (`8c2ffe29`, merged while the
      repository still lived at `opensoft/LedgerxFactory` — it has since
      moved to `LedgerXcorp/LedgerxFactory` and then to
      `ledgerXfactory/LedgerxFactory`, both moves on 2026-09-07, both old
      paths redirecting) and #34 `adopt-openspec-cli-pin-gate` (`0f265d8c`,
      merged) took LedgerxFactory's gate reading from `5 passed, 11 failed`
      to `17 passed, 0 failed` and then wired the repository's FIRST
      workflow; CI's gate at the pin: `18 passed, 0 failed`, all 19 of its
      validators now running in CI. opensoft/AdxFactory #7
      `prepare-openspec-1.12-readiness` (`fea04fee`, merged) and #8
      `adopt-openspec-cli-pin-gate` (`a9deb245`, merged) took AdxFactory's
      gate reading from `1 passed, 2 failed` to `4 passed, 0 failed` and then
      wired the repository's FIRST workflow; CI's gate at the pin: `5
      passed, 0 failed`. Each of the three pins `stack.yaml`'s
      `xfactory.contract_ref` at `724a2a4fb3dc0fb996bb5f3736634eecc8f829c3`.
      All six PRs ticked in full at `add-openspec-cli-pin` tasks 6.3, 6.4 and
      6.5. The three readiness packets were admitted to the queue on Brett
      Heap's 2026-09-06 word "go" and ratified and merged on his 2026-09-07
      word "ratify and merge"; the three wiring packets merged on his
      first-hand 2026-09-08 word "merge all 3" (~13:14Z), heard by lane
      codeXfactory-1. None of the three owed a disposition in
      `contracts/openspec-cli-pin.yaml`. Was: The remaining consuming
      repositories (codexFactory, MedxFactory, LedgerxFactory, AdxFactory)
      still have no wiring to this entrypoint. Named by #667 as
      per-repository successor work; unchanged by this bump. **AMENDED
      2026-09-06:** codexFactory is now wired — codexFactory #227
      `adopt-openspec-cli-pin-gate` (`bb66d85c`), ticked at
      `add-openspec-cli-pin` task 6.1. MedxFactory, LedgerxFactory and
      AdxFactory remain; the box stays UNTICKED for them.
- [x] 6.4 **(DONE 2026-09-08, by `pin-openspec-cli-dependency-closure`.)** The
      pinned artifact's DEPENDENCY CLOSURE is PINNED. An authored
      `contracts/openspec-cli-pin.1.12.0.package-lock.json` — 80 packages, every
      one resolved and addressed — is committed beside the pin at the version
      THIS packet moved the referent to, its SHA-512 recorded in the pin as
      `lockfile_integrity:`, its entry for `@fission-ai/openspec` asserted equal
      to the `integrity:` this packet re-cut, and the install running through it
      with `npm ci --ignore-scripts` rather than resolving nine caret ranges.
      The pin's header no longer says the closure is open; the old paragraph is
      kept as `Was:` history there, because the shortfall is the argument for the
      mechanism. Ruled by Brett Heap, 2026-09-08T14:14:49Z, first-hand, verbatim
      *"Vendor a lockfile (Recommended)"*, on a four-option packet. THE
      REGENERATION OBLIGATION THIS ADDS TO A BUMP: five things now move together
      and not four — `version`, `integrity`, `shasum`, `tarball` AND a
      regenerated lockfile with its digest and count re-recorded — and the
      verifier refuses `pin-lockfile-mismatch` on the first run after a bump that
      forgets, so the obligation is met by the gate rather than by memory. Was:
      The pinned artifact's DEPENDENCY CLOSURE is still unpinned. Declared in the
      pin's header, unchanged by the version move, still successor work.
