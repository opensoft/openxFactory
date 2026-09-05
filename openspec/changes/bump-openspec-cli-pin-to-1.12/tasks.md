# Tasks: bump-openspec-cli-pin-to-1.12

Status: draft

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in
`evidence/pin-bump-1.12-2026-09-05.md`. Group 5 is DRAFTED-NOT-DONE work and
group 6 is OWED work; neither is ticked and each names why.

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
- [x] 1.4 The header's factual claims re-derived at the new version: 389 files
      rather than 270, and the dependency-closure shortfall restated as
      UNCHANGED by the bump rather than silently carried.

## 2. The disposition mechanism

- [x] 2.1 `scripts/validate-openspec-cli-pin.py`: check 6. The pinned CLI runs
      with `--json`, `parse_report` reads the verdict (both array shapes),
      `collect_findings` flattens it, `reconcile` matches ERROR-level findings
      to in-scope dispositions in BOTH directions.
- [x] 2.2 `pinned_dispositions` refuses `pin-disposition-malformed` for a
      missing `repo`/`item`/`path`/`finding`/`why`, an absent or EMPTY
      `cited_to:`, no `ratified_by:`/`recorded_by:`, or two entries covering
      one finding — evaluated in check 1, BEFORE any registry round trip.
- [x] 2.3 `pin-disposition-stale`, exit 2, for a disposition matched by no
      finding in the run, with the asymmetry argued in the code and in
      `design.md` § 2.
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

- [x] 4.1 78 tests in `tests/openspec_cli_pin/` (was 41), green.
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
      `add-composed-view-authoring` archives — and asserts exit 2.

## 5. Exit 3 — drafted, NOT taken

- [ ] 5.1 File `evidence/upstream-issue-draft-merged-into-marker.md` with
      `fission-ai/openspec`. **DELIBERATELY NOT DONE.** The draft is complete
      and carries the minimal reproduction; filing it is Brett's act. Exit 2 and
      exit 3 are not exclusive — exit 2 is what this estate does about its own
      gate, exit 3 is what it asks of the tool — and if upstream lands a fix the
      dispositions go STALE on the next bump and the mechanism removes them.

## 6. Owed, and named rather than discovered later

- [ ] 6.1 Ratification of this packet's text by Brett Heap, recorded as a
      `Ratified by:` line and a `review/` record. *"take exit 2"* settled the
      approach and not the text.
- [ ] 6.2 `.github/workflows/pytest-suite.yml`'s literal
      `npm install -g @fission-ai/openspec@1.2.0` now DISAGREES with the pin.
      This is #667's open task 5.1 and its own diff, over this repository's most
      load-bearing required check; it is not ridden on this pull request. Until
      it lands, `tests/proposal-support/` drives a `1.2.0` binary while the gate
      validates at `1.12.0` — which is the two-copies-of-a-pin defect #667 named,
      now visible rather than latent.
- [ ] 6.3 The remaining consuming repositories (codexFactory, MedxFactory,
      LedgerxFactory, AdxFactory) still have no wiring to this entrypoint. Named
      by #667 as per-repository successor work; unchanged by this bump.
- [ ] 6.4 The pinned artifact's DEPENDENCY CLOSURE is still unpinned. Declared
      in the pin's header, unchanged by the version move, still successor work.
