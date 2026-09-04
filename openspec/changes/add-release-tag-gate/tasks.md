# Tasks: add-release-tag-gate

Status: draft
Kind: tasks
Draft slice of: openspec/changes/add-release-tag-gate/proposal.md

**THE GATE THAT IS NOT OURS: § 4.** Making `release-tag-gate` a REQUIRED status
check on `main` is a branch-protection ruleset act in Brett's console. No agent
performs it, and an agent-reported "ruleset created" without the console act is
not evidence. It gates ARCHIVE, not ratification — the packet may be ratified
and merged while § 4 is open, and it may not archive until § 4.2 reads back the
ruleset id and one green run.

## 1. Ratification

- [ ] 1.1 RATIFICATION IS OWED AND HAS NOT HAPPENED. Issue #664's *"do your
      recommendation"* is the ORIGIN and the admission to the queue; it is not
      a ratification of this packet's content. `proposal.md`, `design.md` and
      this file carry `Status: draft` until a separate act.
- [ ] 1.2 THE FOUR ORCHESTRATOR DECISIONS ARE FLAGGED FOR VETO and this box
      stays open until Brett has read `design.md`. **D1** (the cutting pull
      request cannot be required to carry its own tag, so the obligation is
      RECORDED — the packet's veto point) and **D2** (`gate-version-reuse`, the
      one arm beyond the ruling's text; deleting it is one `if` block, two
      tests, one scenario and one table row) are the two to read first. **D3**
      (no pull-request comment) and **D4** (a `warning` refuses too) follow.
- [ ] 1.3 IF D2 IS VETOED: remove the `gate-version-reuse` arm from
      `scripts/validate-release-tag-gate.py` and its entry from `REFUSALS`,
      delete `test_a_declaration_moved_onto_an_already_published_bundle_is_refused`
      and `test_a_tag_already_peeling_to_the_tree_under_judgment_is_pre_published`,
      and drop the scenario *A cutting pull request moves the declaration onto a
      bundle that is already published* from the delta. Nothing else moves.

## 2. The spec delta

- [x] 2.1 `specs/doc-health/spec.md` carries ONE `## MODIFIED Requirements`
      block over the promoted *Release-tag publication*, restating it in full —
      every body unit and all 24 promoted scenario titles, byte-faithful — and
      adding seven body paragraphs plus six scenarios.
  - *2026-09-04 — DONE.* 506 lines, 30 scenarios (24 promoted + 6 added). The
      block DROPS NO CANON UNIT, which is why no `Removed from canon by` and no
      `Merged into` marker is owed; the added preamble says so in terms, on
      `add-per-change-sweep-ledger`'s § D1 practice of stating the marker
      reading rather than leaving it to be inferred.
- [x] 2.2 NO FILE IS ADDED UNDER `openspec/specs/`. A new promoted capability
      file would owe a codexFactory floor advance; this packet modifies an
      existing requirement and adds none.
- [x] 2.3 `release-surface-integrity` is CITED AND NOT MODIFIED. Its own text
      says a published annotated tag "is NOT the reference point, deliberately",
      so that its drift obligation stays evaluable in the window before a tag
      exists — which is the same window this packet is about, answered by a
      different capability, and nothing in this change forces its text.

## 3. Realization

- [x] 3.1 `scripts/validate-release-tag-gate.py`: the base/head resolution, the
      release-surface short-circuit, the `MergeTreeGit` one-method seam
      override, the family run, the `gate-version-reuse` arm (after the family),
      the recorded obligation, and the closed `REFUSALS` set. Exit 0 or 2.
- [x] 3.2 `.github/workflows/release-tag-gate.yml`: `on: pull_request` against
      `main`, NO `paths:` filter, NOT on `push`, job id and check name
      `release-tag-gate` with no display name, `fetch-depth: 0`,
      `permissions: contents: read`, `timeout-minutes: 15`.
- [x] 3.3 `tests/doc-health/test_release_tag_publication.py`: the zero-findings
      half of the pinned test is REMOVED; the positive control is KEPT and the
      test renamed `test_the_probe_can_fire_over_a_tree_constructed_to_be_untagged`,
      its docstring carrying the move, the measurement and where the assertion
      went.
- [x] 3.4 `tests/doc-health/test_release_tag_gate.py`: sixteen tests over real
      git repositories with real origins — the short-circuit with its positive
      control, the path classification, the clean cut with its recorded
      obligation, the stale bundle, the in-window release-surface edit, the
      misplaced tag, version reuse, pre-publication, the below-floor bundle,
      three fail-closed refusals, the closed refusal set, and the workflow's
      wiring.
- [x] 3.5 `docs/contract-versioning-policy.md` § Bundle Realization Order names
      the gate and the post-merge tag obligation. `Status: ratified` unchanged,
      the edit minimal.
- [x] 3.6 README § OpenSpec Records carries this change's row.
- [ ] 3.7 The corpus-sweep ledger row: run
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
      '#<PR>' --moved-on 2026-09-04` after the pull request is opened, with the
      REAL number, and read the diff as the list of rows this change moved.

## 4. Bound follow-on — the required status check (GATES ARCHIVE)

**A check that is not REQUIRED enforces nothing.** Until § 4.1 is performed, the
obligation this packet moves out of `pytest-suite` is enforced by a workflow
anyone can merge past, which is strictly weaker than the state before this
change. Ratification does NOT wait on this group; **ARCHIVE DOES.** The precedent
is `create-medxchart-overlay-boundary` § 5.3/5.4 (`pin-validation`, ruleset
`22272824`), and before it LedgerxWallet's `21701436`.

- [ ] 4.1 **[OPERATOR]** Add `release-tag-gate` to the branch-protection ruleset
      on `opensoft/openxFactory`'s `main` as a REQUIRED status check, beside
      `pytest-suite` and `pin-validation`. This half is Brett's console act; no
      agent performs it.
- [ ] 4.2 **EVIDENCE, READ BACK RATHER THAN REPORTED.** Record here the ruleset
      id and the API reading that confirms it
      (`gh api repos/opensoft/openxFactory/rulesets/<id>`), plus ONE green
      `release-tag-gate` run naming its pull request and run id. A guessed
      ruleset id is not evidence; the API is authoritative.
- [ ] 4.3 The FIRST pull request this gate judges for real is the next one that
      touches `contracts/manifest.yaml` or `contracts/releases/**`. **PR #653 is
      NOT it** — the `contract-v3.4` cut merged 2026-09-04 at 19:56Z, before
      this packet was authored; it is used here only as REPLAY evidence
      (`--head 807a4f47` exits 0). Record the first real judgement when it
      happens.

## 5. Verification

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate add-release-tag-gate --strict`
      and `--all --strict` green.
- [x] 5.2 `python3 -m pytest tests/doc-health tests/sequenced_after -q` green.
- [x] 5.3 `python3 scripts/validate-sequenced-after.py .` green;
      `--ledger-diff` green after § 3.7.
- [x] 5.4 `python3 scripts/doc-health.py --single-repo .` at parity with main
      except this change's own expected effects, counted before and after; the
      `## MODIFIED` block raises NO `modified-block-currency` finding.
- [x] 5.5 The new workflow's FIRST PROOF is this packet's own pull request: it
      touches no release-surface path, so `release-tag-gate` must report green
      by short-circuit. Record the run.
- [x] 5.6 `actionlint` on the new workflow where available.
