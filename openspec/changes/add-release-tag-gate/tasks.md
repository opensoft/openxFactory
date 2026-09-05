# Tasks: add-release-tag-gate

Status: ratified
Ratified by: add-release-tag-gate — 2026-09-05, Brett Heap, "ratify 668, land it when green" (record `review/ratification-2026-09-05.md`)
Kind: tasks

**THE GATE THAT IS NOT OURS: § 4.** Making `release-tag-gate` a REQUIRED status
check on `main` is a branch-protection ruleset act in Brett's console. No agent
performs it, and an agent-reported "ruleset created" without the console act is
not evidence. It gates ARCHIVE, not ratification — the packet may be ratified
and merged while § 4 is open, and it may not archive until § 4.2 reads back the
ruleset id and one green run.

## 1. Ratification

- [x] 1.1 **RATIFIED 2026-09-05 by Brett Heap** (openxFactory operator
      authority), in session, verbatim: **_"ratify 668, land it when green"_**.
      Issue #664's *"do your recommendation"* was the ORIGIN and the admission
      to the queue and is NOT this; ratification was a separate act, and
      `proposal.md`, `design.md` and this file now carry `Status: ratified`
      against ONE citation line each. Record:
      `review/ratification-2026-09-05.md`; verification:
      `review/verification-2026-09-05.md`.
- [x] 1.2 **RATIFIED AS DESIGNED — the four orchestrator decisions were put
      forward for veto and NONE was vetoed.** The word was given with **D1**
      (the cutting pull request cannot be required to carry its own tag, so the
      obligation is RECORDED — the packet's veto point) and **D2**
      (`gate-version-reuse`, the one arm beyond the admitting ruling's text)
      standing in front of the ratifier, so both are ratified KNOWINGLY rather
      than by silence; **D3** (no pull-request comment) and **D4** (a `warning`
      refuses too) likewise. The framing each was ratified under is
      `review/ratification-2026-09-05.md` § 3.
- [x] 1.3 **NOT TAKEN — D2 was not vetoed, so the deletion below was not
      performed.** It is kept as written because it is the shape of the
      remedy if the arm is ever withdrawn, and because a ratified decision
      should carry the cost of reversing it beside it. IF D2 IS EVER VETOED:
      remove the `gate-version-reuse` arm from
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
- [x] 3.4 `tests/doc-health/test_release_tag_gate.py`: twenty-four tests over real
      git repositories with real origins — the short-circuit with its positive
      control, the path classification, the clean cut with its recorded
      obligation, the stale bundle, the in-window release-surface edit, the
      misplaced tag, version reuse, pre-publication, the below-floor bundle,
      four fail-closed refusals (two of them driven by fault injection at the
      git seam so the refusal table can be asserted as an EQUALITY rather than a
      subset), the two rename cases, the retired pin's own absence, the closed
      refusal set, and the workflow's wiring.
- [x] 3.5 `docs/contract-versioning-policy.md` § Bundle Realization Order names
      the gate and the post-merge tag obligation. `Status: ratified` unchanged,
      the edit minimal — one paragraph, inserted where the realization order
      already ends.
  - *2026-09-04 — DISCLOSED RATHER THAN DISCOVERED.* That document is a DIGESTED
      MEMBER of the published `contract-v3.4` bundle and is NOT one of the three
      EDITORIAL members (`contracts/CHANGELOG.md`, `contracts/manifest.yaml`,
      `contracts/README.md`) allowed to move between cuts, so the edit raises one
      `release-inventory-drift` `error` — the designed, transient signal that a
      cut is owed, cleared by the next cut re-digesting the member. Hand-editing
      `contracts/releases/contract-v3.4.digests.yaml` instead is FORBIDDEN: that
      bundle is published, tagged and immutable provenance. Precedent for the
      same document moving between cuts: `95c2cf6a` (PR #622) and `2898b104`.
- [x] 3.5a `openspec/changes/add-release-tag-gate/.openspec.yaml` carries the
      `proposal-origin` declaration — `kind: ad_hoc`, id
      `openxFactory:adhoc:2026-09-04-add-release-tag-gate`, the reason with the
      measurement in it, and Brett's admitting word with its date. Without it the
      family reports the packet as carrying no origin declaration.
- [x] 3.6 README § OpenSpec Records carries this change's row.
- [x] 3.7 The corpus-sweep ledger row.
  - *2026-09-04 — DONE, with the real number.*
      `validate-sequenced-after.py . --seed-ledger --moved-by '#668' --moved-on
      2026-09-04` wrote 166 rows and moved exactly ONE:
      `add-release-tag-gate: {state: active, class: co-modifier, declares:
      absent, prose: false, moved_by: "#668", moved_on: "2026-09-04"}`. No
      partner row moved — both other writers of this requirement
      (`add-release-tag-publication-check`, `declare-spent-bundle-state`) were
      already `co-modifier` — so NO MOVEMENT LOG entry is owed: the diff states
      everything. `--ledger-diff` exits 0.

## 4. Bound follow-on — the required status check (GATES ARCHIVE)

**A check that is not REQUIRED enforces nothing.** Until § 4.1 is performed, the
obligation this packet moves out of `pytest-suite` is enforced by a workflow
anyone can merge past, which is strictly weaker than the state before this
change. Ratification does NOT wait on this group; **ARCHIVE DOES.** The precedent
is `create-medxchart-overlay-boundary` § 5.3/5.4 (`pin-validation`, ruleset
`22272824`), and before it LedgerxWallet's `21701436`.

- [x] 4.1 **[OPERATOR]** Make `release-tag-gate` a REQUIRED status check on
      `opensoft/openxFactory`'s `main`. **THE REAL NEIGHBOURS, READ FROM THE
      API RATHER THAN ASSUMED** — this repository has NO `pin-validation`
      ruleset, which an earlier draft of this task named by carrying the
      MedxChart precedent across: the required contexts here live in ruleset
      **`21538893`** ("openxFactory wallet-gate", contexts `wallet-validation`,
      `pytest-suite`, `lane-line`) and ruleset **`21957695`** ("openxFactory
      chain-gate", contexts `signed-execution-chain-gate`, `lane-line`), both
      `enforcement: active`. Adding the context to `21538893` puts it beside
      `pytest-suite`, which is where the assertion this packet moves came from.
      This half is Brett's console act; no agent performs it. (`pin-validation`
      / ruleset `22272824` is `opensoft/MedxChart`'s and is cited only as the
      SHAPE precedent for an `[OPERATOR]` task with evidence before archive.)
  - *2026-09-05 — DONE BY THE OPERATOR, AND READ BACK RATHER THAN REPORTED.*
      Brett's word: **_"ruleset updated, do the evidence and archive it"_**.
      Ruleset **`21538893`** ("openxFactory wallet-gate", Organization-sourced,
      `enforcement: active`, `~DEFAULT_BRANCH`) now lists **FOUR** required
      contexts — `wallet-validation`, `pytest-suite`, `lane-line` and
      **`release-tag-gate`** — with `strict_required_status_checks_policy:
      false`. Its `updated_at` is **2026-09-05T00:36:49.902-04:00 (04:36:49Z)**
      against a `created_at` of 2026-08-26, which is the console act. Confirmed
      from the branch's own side too, because the two can disagree:
      `gh api repos/opensoft/openxFactory/rules/branches/main` lists
      `release-tag-gate` among the contexts `main` enforces. **NO NEW RULESET
      WAS CREATED** — the context joined the one already carrying
      `pytest-suite`, so the gate sits beside the suite the assertion left.
      Full JSON: `review/realization-evidence-2026-09-05.md` § 2–3.
- [x] 4.2 **EVIDENCE, READ BACK RATHER THAN REPORTED.** Record here the ruleset
      id and the API reading that confirms it
      (`gh api repos/opensoft/openxFactory/rulesets/<id>`), plus ONE green
      `release-tag-gate` run naming its pull request and run id. A guessed
      ruleset id is not evidence; the API is authoritative.
  - *2026-09-05 — HALF DONE, AND THE OPEN HALF IS THE POINT OF THE BOX.* The
      ruleset half is § 4.1 above and is complete. The RUN half is **not**: every
      `release-tag-gate` run to date (`33927889060`, `33932616773`,
      `33933031517`, `33937403224`, `33938798720`) is green but was taken while
      the check was ADVISORY, and **a green advisory run is not evidence that a
      REQUIRED context reports** — a required context that fails to report
      blocks the merge forever, which is exactly what § 3.2's missing `paths:`
      filter is designed against. No run has occurred since 04:36:49Z, so the
      first green run under the required regime is **this archive pull
      request's own**, and it is cited rather than borrowed.
  - *2026-09-05 — THE RUN HALF IS NOW DONE, AND IT IS CONFIRMED REQUIRED RATHER
      THAN ASSUMED REQUIRED.* **Run `33945259576`**, openxFactory **PR #672**,
      head `ac3d4502`, started 04:41:54Z, completed 04:42:08Z,
      **`conclusion: success`** — five minutes after the console act and the
      first run of that workflow anywhere since it. A green tick does not say
      whether a context is enforced, so the GraphQL `statusCheckRollup` was
      asked per pull request and answers **`release-tag-gate isRequired: true,
      SUCCESS`**. It short-circuited, as it must — *"no release surface change:
      none of the 2 changed path(s) … is contracts/manifest.yaml or under
      contracts/releases/"* — and its log's `Complete job name:
      release-tag-gate` confirms the check surfaces under exactly the literal
      token the ruleset pins.
### 4.3 — SUCCESSOR, NAMED AND NOT DRAFTED. Deliberately not a checkbox.

**This packet does not own the event, so it does not carry an open box for it.**
The FIRST pull request this gate judges for real is the next one that touches
`contracts/manifest.yaml` or `contracts/releases/**` — which is a future cut by
whoever cuts it, not work this change can perform, and an open checkbox would
either sit forever or be ticked by someone who did not do it. **PR #653 is NOT
it**: the `contract-v3.4` cut merged 2026-09-04 at 19:56Z, before this packet
was authored, and is used here only as REPLAY evidence (`--head 807a4f47` exits
0, through the PRE-PUBLISHED arm rather than the `TAG OWED` arm a live cut
takes). **Archive does not wait on it**, and the first real judgement is
recorded by the pull request that receives it, in its own lane.

The same applies to the accepted `release-inventory-drift` `error` on
`docs/contract-versioning-policy.md`: it persists until the next contract cut
re-digests that member. An archive does not clear it and nothing here claims it
does.

## 5. Verification

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate add-release-tag-gate --strict`
      and `--all --strict` green.
- [x] 5.2 `python3 -m pytest tests/doc-health tests/sequenced_after -q` green.
- [x] 5.3 `python3 scripts/validate-sequenced-after.py .` green;
      `--ledger-diff` green after § 3.7.
- [x] 5.4 `python3 scripts/doc-health.py --single-repo .` against a SAME-CLOCK
      CONTROL, not a stale baseline. **The first measurement of this was taken
      hours before the branch's last run and was therefore wrong in the
      `warning` column**: this report ages by the calendar, and three `warning`s
      (two routing records and one staged topic) crossed the 30-day threshold
      during authoring, which a before/after taken at two clocks reports as
      movement this change caused. Re-measured with a worktree at `origin/main`
      (`9420472e`) run minutes apart from the branch: **main 6 critical / 4
      error / 30 warning / 13 info → branch 6 critical / 5 error / 30 warning /
      13 info**, and a line-by-line diff of the two reports differs by EXACTLY
      ONE finding — the `release-inventory-drift` `error` on
      `docs/contract-versioning-policy.md` predicted in § 3.5. Everything else
      is identical but for the repo-name prefix the two checkout directories
      give it. The `## MODIFIED` block raises NO `modified-block-currency`
      finding — a `--family modified-block-currency` run names this change zero
      times.
- [x] 5.5 The new workflow's FIRST PROOF is this packet's own pull request: it
      touches no release-surface path, so `release-tag-gate` must report green
      by short-circuit.
  - *2026-09-04 — RECORDED WITH ITS RUN ID.* PR **#668**, run
      **`33927889060`** (job `101200264376`), **pass in 9s**, printing
      `no release surface change: none of the 12 changed path(s) between
      9420472ea and a396c97bd is contracts/manifest.yaml or under
      contracts/releases/`. The job log's `Complete job name: release-tag-gate`
      confirms the check surfaces under the literal token a ruleset pins. Run
      `33926838509` is the same proof on the branch's first head.
- [x] 5.6 `actionlint` on the new workflow where available.
  - *2026-09-04 — RUN, WITH ITS OUTPUT.* `actionlint
      .github/workflows/release-tag-gate.yml` → **no output, exit 0** (clean).
- [x] 5.7 INDEPENDENT REVIEW, recorded including its absence. **Codex REFUSED
      on usage limits** (requested 2026-09-04 22:45:52Z, refused 22:46:02Z); no
      Codex round ran. Sourcery is the private-repo upsell stub. **Copilot ran
      and found ONE real defect**, fixed in the same branch: `_run` documented
      itself as degrading to None on failure, but `subprocess.run` RAISES
      `OSError` when git cannot be executed at all, which would have exited the
      tool with an uncontrolled code and broken its own "0 or 2, never 1"
      contract — turning a fail-closed refusal into a crash. Caught, and
      `test_an_unrunnable_git_refuses_rather_than_crashing` now pins it with a
      positive control on the same tree. **Copilot round 2 on the fixed head:
      ZERO new comments**, verdict *"Needs a closer look … warrants final human
      verification of process implications"* — which is this packet's own
      pointer: the process implications are D1, D2 and the `[OPERATOR]` act in
      § 4, all three of them the convener's and none of them claimed as done.
  - *2026-09-04 — AND THE BENCH'S OWN SCORE, RECORDED BECAUSE IT IS THE POINT.*
      An INDEPENDENT ADVERSARIAL REVIEW found the defect NEITHER bot did: with
      git's default rename detection a pure `git mv` of a release inventory or
      of the manifest OUT of `contracts/` printed only the destination path, so
      the gate short-circuited green on a pull request that had REMOVED a
      release member (P2-1, fixed with `--no-renames` plus two tests). It also
      caught the wrong `release-surface-integrity` citation in D8, a FOUR/SIX
      scenario miscount, an unenforced scenario, and six count and citation
      errors. **Codex refused on quota; two Copilot rounds did not find P2-1;
      the adversarial review did.** That is the reading of record for how much
      the bot bench is worth on this packet.
  - *2026-09-05 — COPILOT ROUND 3, on the fix round's head: FOUR comments, all
      taken, one of them NOT AT ITS OWN FRAMING.* Two were a real miss of mine —
      the `contract-v3.4` gap still read 68s in two test docstrings after the
      other five sites moved to 69s. The other two said the bundle name printed
      in the `::notice` is author-controlled and could carry `%0A::error::…`,
      Actions decoding it into a forged workflow command. **The escaping was
      added (`workflow_command_safe`) and the reach was CORRECTED rather than
      accepted:** the `::error` prints only a refusal code and its meaning from
      this module's closed table, and the `::notice` is reached only past
      `_at_or_above_floor`, whose `^contract-v<major>.<minor>$` grammar admits
      no `%` — so a crafted name is refused as out of scope before it can be
      printed, which a test now pins alongside the escaping itself. It is
      DEFENCE IN DEPTH, and it earns its place because the guard that makes it
      unreachable lives in another module answering a different question.
- [x] 5.8 A POSITIVE CONTROL ON THE `## MODIFIED` BLOCK ITSELF. The
      `modified-block-currency` family reports nothing about this change, which
      alone cannot be distinguished from a block it never read. One promoted
      scenario title was deliberately mutated and the family re-run: it fired
      (*"omits 1 of the 24 scenarios … 'The published tag is lightweight rather
      than annotated'"*), the delta was restored and the family re-run silent.
      All 24 promoted scenario titles and every body unit are carried, verified
      by a probe shown capable of firing.
