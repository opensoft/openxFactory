# Tasks: add-promotion-fidelity-check

The commissioning ruling (Brett, in-session, 2026-08-24, verbatim: "commission
the archived-delta-vs-promoted-spec check") covers §1 and §2. §3's four design
decisions were taken by the orchestrating session under standing patterns and
are flagged for veto in `proposal.md` § Orchestrator Decisions — reverting any
one of them is an edit to this change, not a new one.

**§4 WAS deliberately open, and it closed the way it was meant to.** The family
shipped advisory; flipping it to enforcing was a ruling, and leaving the boxes
unticked is what kept that visible until Brett made it (2026-08-24, task 4.1)
instead of letting it become a silent later commit. All three boxes are now
ticked, in the ruled order: the ruling (4.1), the discharge of the standing
population (4.3), and only then the both-halves flip (4.2).

## 1. Ratification

- [x] 1.1 Brett commissioned the check on 2026-08-24, in the terms
      `docs/archive-record-discrepancies.md` § FU-DOM-CODEX left open: "no
      check yet compares archived deltas to promoted specs, so the class
      stays unreported. That prevention question is scoped to openxFactory's
      neutral tooling."
- [x] 1.2 The obligation is stated before the checker enforces it —
      `document-lifecycle` gains "Ratified spec deltas reach the promoted
      specification". A checker with no promoted rule behind it is a rule
      invented in Python, which is the shape this corpus reads
      `tag-hygiene`'s by-reference relationship to avoid.
- [x] 1.3 `doc-health` gains the eighteenth family and its own requirement,
      MODIFYING the family count and the "other thirteen" arithmetic that
      goes with it. The count sentence had already drifted once
      (`staged-topic-template`, registered 2026-08-15, uncounted until
      2026-08-23), so it is re-derived here rather than copied.

## 2. Implementation

- [x] 2.1 `scripts/doc_health/promotion_fidelity.py`: the archived-delta
      parser (`## <OP> Requirements` sections, `### Requirement:` titles,
      `#### Scenario:` titles, `RENAMED` FROM/TO pairs), the promoted-spec
      reader sharing the same two heading regexes, the latest-writer
      resolution with its tie-break, the ratification exemption, the
      disposition read, and the family function.
      **REVISED under 4.1's rulings (PR #315).** The exemption is now
      `_is_exempt_from_promotion` and asks the opposite question — archiving
      is presumed to be ratification, and only an explicitly declared
      `draft`-or-lower standing exempts a delta (`declared_standing` reads the
      header's leading token, symmetrically in both directions, so an
      annotation cannot change what a standing says). The delta and canon
      readers now go through a TREE (`WorkingTree` / `GitRefTree`) rather than
      through `Path`, which is what lets the live-main basis be a second
      reader of one set of rules rather than a second copy of them.
- [x] 2.2 `scripts/doc_health/corpus.py`: `RealGit.first_commit_timestamp`.
      `first_commit_date` answers the same question to DAY resolution, which
      is exactly the resolution that cannot break a same-day tie — and 19
      (capability, requirement) pairs in this repository are written twice or
      more on their latest date.
      **EXTENDED under 4.1's live-mains ruling (PR #315):**
      `first_commit_timestamp` takes an optional `ref` (a tie decided from
      HEAD's history about statements read from `origin/main` is two readers
      of two trees agreeing by accident), and `resolve_ref` / `ls_tree_paths`
      / `show_blob` read a named ref without touching the checkout.
      `ls_tree_paths` passes `--full-name` and a `:(top)` pathspec: `ls-tree`
      resolves and prints against the CURRENT PREFIX while `git show
      <ref>:<path>` always reads from the tree ROOT, so the untuned pair
      lists one subtree and reads another. Caught live — the fixture repos
      sit inside this repository, and the first cut of the CLI test listed
      the fixture's `openspec/` and read openxFactory's, reporting a clean
      run for it.
- [x] 2.3 Registration: `FAMILIES` in `families.py`, `FAMILY_IDS` in
      `__init__.py` (so the family gets its own report section — the
      omission that left `proposal-origin` sectionless is a known defect,
      not a pattern to copy), and NOT `FAMILY_RESOLUTION`, with the reason
      recorded at the registration site.
      **EXTENDED under 4.1's live-mains ruling (PR #315):**
      `families.FAMILY_NOTES` (one entry, this family's `basis_notes`),
      `RunResult.notes` filled beside the family call in `run_suite`, and
      `report.render(family_notes=...)` rendering a family's notes under its
      own heading BEFORE its findings and on a clean run too — "No findings."
      is a verdict, and a verdict about an unnamed tree is what the ruling
      forbids. The `--promotion-fidelity-basis` flag and the
      `Context.promotion_fidelity_basis` field live in `runner.py`; a test
      greps the package to prove no other module can name the option.
- [x] 2.4 `tests/doc-health/conftest.py`: `FakeGit.first_commit_timestamp`,
      answering `None` where no stamp is supplied — the same degradation
      `RealGit` performs when git cannot answer, which is the fallback path
      §3.4's test exercises deliberately.
      **EXTENDED under 4.1's live-mains ruling (PR #315):** `refs` answers
      `resolve_ref` and one `ref_trees` map serves BOTH `ls_tree_paths` and
      `show_blob`, because a shim whose listing and whose bodies could
      disagree would let a test pass over a reader that never reads what it
      lists. `first_commit_timestamp` keys ref-scoped stamps separately, so a
      fall-back run cannot accidentally be handed the ref's history.
- [x] 2.5 `tests/doc-health/test_lifecycle_scan_set.py`: the eighteenth
      family classified as a NON-reader of the lifecycle scan set, and the
      `len(NON_READERS) == len(FAMILIES) - 4` arithmetic advanced from 13 to
      14. This test failed loudly on the registration commit, by name, which
      is exactly what it was built to do.
- [x] 2.6 **The nightly's live-mains basis, realized in this repository.**
      `.github/workflows/doc-health-reusable.yml` — the reusable workflow the
      aggregation's thin `doc-health-nightly.yml` calls — gains a "Fetch each
      governed submodule's live origin/main" step before "Run doc-health
      suite", and the reporting invocation gains
      `--promotion-fidelity-basis live-main`. **NO AGGREGATION-SIDE EDIT IS
      OWED**: the caller passes inputs only and owns no run step, so both
      halves belong here. The fetch moves no file (it updates
      `refs/remotes/origin/main` and the object store; HEAD, index and working
      tree are untouched), which is what keeps the ruling's "other families
      keep measuring the pinned tree" true STRUCTURALLY rather than by
      convention — and `test_workflow_contract` asserts both the ordering and
      the absence of any checkout/reset/merge verb in that step.

## 3. Acceptance evidence, both directions

- [x] 3.1 **The historical true positive fires.**
      `tests/doc-health/fixtures/promotion-fidelity/` reconstructs the SHAPE
      of codexFactory's pre-PR-#85 gap — an archived ratified change whose
      MODIFIED delta states six scenarios against a promoted spec carrying
      two — and the family reports it, naming all four absent scenarios. A
      reconstruction rather than a dependency: this repository cannot read
      the codex checkout, so the shape is frozen here and the real instance
      stays recorded in the register.
- [x] 3.2 **The real live instance fires, in this repository.** Run against
      openxFactory's own archive the family reports two findings, both
      against `2026-08-01-add-workbench-branch-sessions`: ADDED
      `Branch-session notebooks` absent from
      `openspec/specs/lifecycle-notebook-projection/spec.md` entirely, and
      MODIFIED `Corpus scan scope` arrived without 1 of its 4 ratified
      scenarios. Reported, deliberately NOT fixed — see §5.1.
- [x] 3.3 **C5 stays quiet.** The fixture's `Status: draft` packet declares
      four requirements across a capability with no promoted spec at all —
      the loudest possible shape — and the family says nothing. The mutation
      guard flips that header to `ratified` in a `tmp_path` copy and asserts
      the findings appear, so the exemption is what is doing the silencing.
      Against the real archive the exemption suppresses 12 would-be findings,
      all four of C5's capabilities, and nothing else.
      **STILL TRUE AFTER 4.1's RELAXATION (PR #315), and that is the point:**
      C5 is kept quiet by its own `Status: draft` header, not by the spelling
      of the rule around it, so narrowing the exemption to
      explicit-draft-or-lower left it exactly where it stood — measured, not
      assumed. hermes-install's archived
      `2026-08-14-add-governed-job-approval-request` is the live instance of
      the same shape in another repository, and it also stays exempt.
- [x] 3.4 **A requirement legitimately modified by a LATER archived change
      stays quiet**, and so does one RENAMED by a later change.
      `test_latest_writer_wins_is_load_bearing` measures the delta rather
      than asserting the silence: it computes what per-writer checking would
      report on the same fixture and asserts the two disagree.
- [x] 3.5 **The tie-break is proven load-bearing** by running one fixture
      twice — with archive-commit order available, and without — and
      asserting the two runs disagree.
- [x] 3.6 **The advisory launch is pinned structurally**: every finding
      `warning`, and `promotion-fidelity` absent from `FAMILY_RESOLUTION`.
      Both, because enforcement can arrive through either.
      **RE-AIMED BY §4.2, NOT DELETED.** These two tests now pin the
      ENFORCING state — `error`, and a `contested` entry PRESENT — because
      the flip was ruled and taken. The claim in this line is the historical
      one and is kept as written; the tests that carry it forward are
      `test_enforcement_by_severity` and
      `test_enforcement_by_resolution_class`, and the reason there are still
      exactly two of them is unchanged: enforcement can arrive through
      either half, so each is pinned separately.
- [x] 3.7 Full suite green: `python3 -m pytest tests/doc-health` →
      764 passed, 7 skipped (baseline 737/7, +27 new).
      `python3 -m pytest tests/ideation-dashboard -k workbench` → 140 passed.
      Every test module importing `doc_health` across
      `tests/ideation-dashboard`, `tests/client-identity-roster` and
      `tests/notebooklm` → 781 passed. `OPENSPEC_TELEMETRY=0 openspec
      validate --all --strict` → green.
      **RE-RUN on 4.1's realization (PR #315's rulings), from the branch base
      `1274b9bf`:** `pytest tests/doc-health` → **802 passed** (baseline on
      that base, same environment: 771 passed; +31 new — 29 in
      `test_promotion_fidelity.py`, 2 in `test_workflow_contract.py`).
      `pytest tests/ideation-dashboard -k workbench` → **140 passed**,
      unmoved. `openspec validate --all --strict` → **75 passed, 0 failed**.
      **Whole-repo `doc-health --single-repo .` before and after: 4 critical,
      8 error, 75 warning, 4 info — IDENTICAL, and the ranked plans compare
      line-for-line identical too.** Nothing to explain, which is what the
      relaxation's measured-zero cost on this repository predicted.
      (The 764/7 line above was recorded in a different environment; this
      base reports the same suite as 771 passed, 0 skipped. Both are kept
      rather than reconciled — a skip count is a fact about a machine.)
- [x] 3.8 **The presumption's own evidence** (4.1's exemption ruling, PR
      #315). `tests/doc-health/fixtures/promotion-fidelity-presumption/`
      carries the two shapes the ruling's measurement named — an ANNOTATED
      ratification (hermes-install's three-layer-runtime packet, 23
      requirements) and a HEADERLESS archive (medx-roottruth-install's two
      plus hermes-install's seed-layer packet, 31 more) — plus a packet with
      no `proposal.md` at all, an explicit `draft` and an ANNOTATED `draft`.
      Three fire, two stay quiet. Both mutation directions are killed by
      test: restoring the original `== "ratified"` spelling loses all three
      findings, and dropping the explicit-draft check makes both drafts fire.
      A ninth taxonomy standing cannot be forgotten either —
      `PRE_RATIFICATION | RATIFIED_OR_BEYOND == TAXONOMY` is asserted.
      The alphaFactory fixture is deliberately NOT extended with these:
      its "fires exactly four times" assertion is the evidence that the
      relaxation moved NOTHING for packets that read exactly `ratified` or
      exactly `draft`.
- [x] 3.9 **The measurement basis is proven load-bearing and proven narrow**
      (4.1's live-mains ruling, PR #315). ONE fixture is run twice — pinned,
      and live with an `origin/main` whose promoted spec carries what the
      checkout's does not — and the two runs DISAGREE (4 findings vs 3),
      which is what makes the basis a basis rather than a label. The
      degradation is asserted in all three of its shapes (ref unresolvable,
      ref unreadable, a git shim that cannot read refs at all): the run
      measures the checkout and the report NAMES the repository as having
      fallen back. Narrowness is structural, not asserted in prose — a test
      greps `scripts/doc_health/*.py` and requires that only
      `promotion_fidelity.py` and `runner.py` can even NAME the option, so no
      other family can read it by accident. Two end-to-end `runner.main`
      runs prove the flag arrives: the live one puts the deviation in the
      headline and the basis in the family's section, the default one does
      neither and says "pinned".
- [x] 3.10 **Measured across every repository this session could reach**,
      old exemption vs new, both read from live `origin/main`s so the
      comparison is of rules rather than of checkouts. Requirements EXAMINED,
      then findings: openxFactory 541 → 541, **2 → 2** (the ruling's
      predicted zero cost, confirmed); hermes-install 37 → **64**, 0 → 0;
      medx-roottruth-install 0 → **27**, 0 → 0; codexFactory 113 → 113,
      LedgerxFactory 136 → 136, MedxFactory 110 → 110, OpsxFactory 77 → 77,
      omnigent-install 29 → 29, AdxFactory 12 → 12, HealthLinc 7 → 7,
      MedxEHR 7 → 7 — every one unchanged, 0 findings each. MedxChart and
      MedxPractice carry no archive. **+54 requirements examined, +0
      findings anywhere.** The relaxation bought coverage and cost no noise.
      Four packets were un-exempted, and they are exactly the shapes 3.8
      freezes: hermes-install's annotated
      `2026-07-19-implement-three-layer-hermes-runtime-foundation` (23) and
      headerless `2026-07-22-add-seed-layer-content` (4), and
      medx-roottruth-install's headerless `2026-08-10-add-runtime-scaffold`
      (16) and `2026-08-11-add-tiered-ingestion-and-probe` (11).
      **THE openxFactory PAIR IS NOW ZERO, and not because of anything here.**
      This branch was cut at `1274b9bf`, where §3.2's two findings still
      stood. `042df4e7` landed on main mid-session and discharged them —
      5.1's ruled "apply via a proper change", archived as
      `2026-08-25-apply-branch-sessions-deltas`. Merged in, this repository
      reports **0 findings under BOTH exemption spellings**, which is the
      same equality measured at the base and is what a discharged gap should
      look like. The 2 → 2 figures above are kept as the measurement at the
      base rather than restated, because the claim they support is about the
      RULE and not about today's canon.

## 4. The flip to enforcing — RULED, SEQUENCED, and taken

- [x] 4.1 **Decide whether this family gates.** It ships advisory because
      nobody has measured what the pinned domain factories' archives will
      say, and because the standing ruling for domain findings is that they
      are ADVISORY. The evidence a decision needs is one aggregation run's
      per-repo finding counts.
      **THE EVIDENCE ARRIVED AND THE RULING IS MADE (2026-08-24, Brett,
      in-session four-question round; measurement by a parallel session
      running THE LANDED FAMILY corpus-wide, live mains fetched fresh).**
      Per-repo, live `origin/main`s: openxFactory **2 true gaps**
      (§3.2/§5.1's own two — the only standing findings anywhere) from 20
      naive hits, 12 exempt (C5); codexFactory 0 (1 naive); LedgerxFactory
      0 (3); OpsxFactory 0 (3); MedxFactory 0 (1); omnigent-install 0 (2);
      Adx / HealthLinc / MedxEHR / MedxChart 0/0; hermes-install 0 found
      but **30 requirements exempt-invisible, coverage 57.8%**;
      medx-roottruth-install **27 exempt-invisible, coverage 0%**. Class
      distribution: 2 true, 32 legitimately superseded (the resolution
      rules validated corpus-wide — naive 34 → tuned 2 with zero true
      positives lost), 12 known-legal, 0 cosmetic. TWO OPERATIONAL
      FINDINGS THAT SHAPED THE RULING: (1) against the aggregation's
      committed PINS coverage collapses — 0% in three repos, and the
      family misses the #301 gap itself while the codex pin lags — so
      **Brett ruled the nightly measures LIVE MAINS for this family**
      (other families keep the pinned tree); (2) the ratified-only
      exemption is a false-negative channel — annotated-ratified and
      headerless archives are silently unexamined (the 57 requirements
      above) — and keying on "explicitly draft-or-lower" costs MEASURED
      ZERO on openxFactory (both shapes give exactly 2; C5 stays
      suppressed by its own draft header), so **Brett ruled the exemption
      relaxes to explicit-draft-only**. **The gate ruling: ENFORCING,
      SEQUENCED** — close the hermes-install and medx-roottruth header
      gaps first (the campaign pattern), then 4.2's both-halves flip; the
      domain backlogs' zero result is recorded as a one-time
      verified-clean statement rather than standing findings.
      **BOTH NON-GATE RULINGS ARE REALIZED (PR #315's rulings, built here).**
      The exemption relaxation lands in `promotion_fidelity.
      _is_exempt_from_promotion` / `declared_standing` (§2.1, evidence §3.8,
      corpus-wide measurement §3.10); the live-mains basis lands as
      `--promotion-fidelity-basis live-main` plus the reusable workflow's
      fetch step (§2.6, evidence §3.9). The gate ruling itself is NOT
      realized here and must not be: its own text sequences it behind the
      hermes-install and medx-roottruth header discharges, which is 4.3, and
      the flip is 4.2. Both boxes stay open deliberately.
      ONE NUMBER MOVED against the ruling's record, and it moved because the
      measurements were taken from different reference points: this session
      measured **+54** requirements newly examined (hermes-install +27,
      medx-roottruth-install +27) where the ruling recorded 57 (30 + 27). The
      shapes and the packets are the same four; the count is re-derived in
      §3.10 from live `origin/main`s on 2026-08-24 rather than copied.
- [x] 4.2 **If ruled enforcing, both halves move together**: severity
      `warning` → `error` in `promotion_fidelity._LAUNCH_SEVERITY`, AND a
      `"promotion-fidelity": CONTESTED` entry in `families.FAMILY_RESOLUTION`.
      Taking either alone produces a half-enforcing family nobody chose —
      severity alone gates without the disposition discipline; the contested
      class alone gates through `uncited-resolution` under a family name that
      does not say what happened.
      **DONE — BOTH HALVES, ONE COMMIT, after 4.3's discharge was verified by
      measurement rather than assumed.** `_LAUNCH_SEVERITY = ERROR` (the
      identifier keeps its name: it records where the value STARTED, and a
      rename would have cost the grep that ties every reader of the launch
      decision together) and `FAMILY_RESOLUTION` gains one row. Both site
      comments now cite the ruling and supersede what they used to say —
      honestly, not by deletion: 2.3's recorded reason for the ABSENCE from
      `FAMILY_RESOLUTION` was correct for an advisory family and is wrong for
      an enforcing one, so the registration site says that in those words
      rather than pretending the absence was never argued for. The
      `contested` class routing a resolved finding into
      `report.uncited_resolutions` as an ERROR is the SAME mechanism in both
      states; what changed is whether it is a back door or the point.
      **THE TESTS CHANGED MEANING, and that is a design fact rather than a
      weakening** (§3.7's discipline). `test_launch_is_advisory_by_severity`
      and `test_launch_is_advisory_by_resolution_class` — 3.6's structural
      pins — are now `test_enforcement_by_severity` and
      `test_enforcement_by_resolution_class`, asserting `ERROR` and
      `FAMILY_RESOLUTION[FAMILY] == CONTESTED`. They pin the opposite of what
      they pinned yesterday. That is the flip, and it is the only honest way
      to hold it: a test that still asserted `warning` would have had to be
      deleted, and a deleted pin is how a ruled state quietly stops being
      pinned. TWO NEW END-TO-END PINS were added rather than relying on the
      constants, because the declaration and the application are different
      facts: `test_both_halves_reach_the_emitted_findings` runs `runner.main`
      over the fixture and reads `severity=error` and `class="contested"` off
      the emitted report lines (`runner.main` is the ONLY thing that applies
      `FAMILY_RESOLUTION` — the family function still labels its findings
      `auto-fixable`, so a table row some refactor stopped reading would pass
      the declaration test and fail this one), and
      `test_an_enforcing_run_reds_a_fail_on_error_gate` measures the point of
      the flip: the same fixture that returned 0 under `--fail-on error`
      through the whole advisory launch now returns non-zero, while
      `--fail-on critical` still returns 0 — the family rose to ERROR, not to
      CRITICAL. Three further assertions moved with the severity (the
      presumption fixture's severity set, the report-ordering test's
      `- [error]` marker, and the module docstring's item 3).
      **THE BOTH-HALVES INVARIANT IS PINNED BY MUTATION, both directions,
      measured on the mutant.** Reverting `_LAUNCH_SEVERITY` to `WARNING`
      while KEEPING the resolution row → **5 failures**
      (`test_enforcement_by_severity`,
      `test_both_halves_reach_the_emitted_findings`,
      `test_an_enforcing_run_reds_a_fail_on_error_gate`,
      `test_the_presumption_fixture_fires_exactly_three_times`,
      `test_the_report_states_the_basis_under_the_family_heading`). Removing
      the `FAMILY_RESOLUTION` row while KEEPING `ERROR` → **2 failures**
      (`test_enforcement_by_resolution_class`,
      `test_both_halves_reach_the_emitted_findings`). Neither half can move
      alone and land green, which is what task 4.2 asked for structurally
      rather than by convention.
      **NO FINDING MOVED IN THIS REPOSITORY, as predicted.** Whole-repo
      `doc-health --single-repo .` before and after the flip: 4 critical, 8
      error, 73 warning, 4 info — and the two reports are BYTE-IDENTICAL, not
      merely equal in their totals. The flip changes what a finding COSTS, and
      openxFactory has none in this family to cost anything.
      **THE DELTA WAS AMENDED TO MATCH, because a flip that left the promoted
      requirement saying `warning` would have made this family's own canon the
      next instance of the class it checks.** The `doc-health` delta's
      advisory-at-launch paragraph now states the enforcing rule in both
      halves and keeps the launch as recorded history rather than replacing
      it; the two scenarios that named a severity now say `error` ("A ratified
      delta did not reach canon" also gains the `--fail-on` direction and the
      resolution class it must carry, replacing the line that said the finding
      must NOT fail an `--fail-on error` run); and `document-lifecycle`'s
      "advisory finding" becomes "reported finding", since that capability
      owns the OBLIGATION and never owned doc-health's severity. **Every
      scenario was restated — 12 before, 12 after, across the same three
      requirements** — the dropped-scenarios lesson this family exists to
      catch being exactly the failure available to a careless edit here.
      `openspec validate add-promotion-fidelity-check --strict`: valid.
- [x] 4.3 **If ruled enforcing, the standing population is discharged
      FIRST.** `govern-openspec-corpus-membership` established the ordering
      and the reason: "A gate that goes red on the commit that introduces it
      teaches everyone to route around the gate."
      **DISCHARGED, AND VERIFIED BY RE-MEASUREMENT ON THE DAY OF THE FLIP —
      not by trusting the discharging PRs' own claims.** The standing
      population 4.1 named had three parts, and each was re-run today from
      the merged state rather than read out of a PR body:
      1. **openxFactory's two true gaps** — the only standing FINDINGS
         anywhere in 4.1's corpus-wide evidence. Discharged by **openxFactory
         PR #316**, merge `51a875ab`, which ratified and archived
         `2026-08-25-apply-branch-sessions-deltas` (the §5.1 ruling; drift
         checked before applying, fidelity proven by sha256). Re-measured
         here at `700c1a19`: **0 findings, on BOTH bases** — pinned and
         `--promotion-fidelity-basis live-main`.
      2. **hermes-install's coverage gap** (4.1: 0 found but 30 requirements
         exempt-invisible, coverage 57.8%). Discharged by **hermes-install
         PR #42**, merge `2a4d719c`. Re-measured today against that live
         `origin/main`: **0 findings**, the newly examined population clean.
      3. **medx-roottruth-install's coverage gap** (4.1: 27 exempt-invisible,
         coverage 0%). Discharged by **medx-roottruth-install PR #1**, merge
         `89dca824`. Re-measured against that live `origin/main`: **0
         findings**.
      **The domain backlogs' zero** is the fourth part, and the ruling did
      not ask for PRs for it — it ruled the zero "recorded as a one-time
      verified-clean statement rather than standing findings". That statement
      lives in THIS packet: §4.1's per-repo counts (landed by PR #315,
      `1274b9bf`) and §3.10's corpus-wide re-derivation from live mains
      (landed by PR #320, `055a514b`). It is deliberately NOT a set of
      register addenda — `docs/archive-record-discrepancies.md` records the
      commissioning and the family's first live catch, and its per-domain
      FU-DOM entries are the LIFECYCLE-HEADER campaign's, a different class.
      Cite the four rows above and this paragraph; a reader looking for four
      domain register addenda for this family will not find them, because
      they were never owed.
      **CORPUS-WIDE RE-MEASUREMENT, today, live mains fetched fresh** (14
      governed submodules, `git fetch origin main` only — no checkout, reset,
      merge or pull anywhere): **0 findings, 0 critical, 0 error, 0 warning,
      0 info.** The gate goes green on the commit that introduces it, which
      is the whole ordering rule.
      **TWO HONEST FACTS THE RE-MEASUREMENT SURFACED**, recorded because a
      later reader will otherwise re-derive them:
      - **The same run on the PINNED basis reports 2 findings, and they are
        openxFactory's already-discharged pair.** The aggregation's committed
        `openxFactory` pin is 22 commits behind `origin/main` and predates
        `042df4e7`, so the pinned tree still holds the pre-discharge canon.
        This is not a standing gap; it is D5's argument reproducing itself on
        demand — the exact reason Brett ruled this family measures live mains.
        The nightly passes `--promotion-fidelity-basis live-main` (§2.6), so
        the enforcing gate reads the 0, not the 2. A run that did NOT pass it
        would red on a gap that no longer exists.
      - **`corpus.discover_repos` scans `openxFactory` plus `xFactories/*`
        only; `installs/` is never scanned.** So hermes-install and
        medx-roottruth-install — the two repositories whose discharge this
        task sequenced the flip behind — are not in an AGGREGATION run's repo
        set at all, and their zeros above were measured by direct
        `--single-repo` runs. This is pre-existing behaviour shared by all
        eighteen families, not something the flip introduces and not this
        change's to alter; it means the ruled prerequisite was discharged for
        the repositories' own sake and the nightly cannot red on them today
        either way. Named here rather than left for the next reader to trip
        over.

## 5. Recorded, not fixed

- [x] 5.1 **openxFactory's own two findings** (§3.2) are unpromoted ratified
      deltas of exactly the commissioned class, and applying a ratified delta
      to canon is a governance act belonging to its own change — which is
      what codexFactory PR #85 was. Needs the same decision that gap needed:
      apply the ratified delta via a proper change, or record the
      non-promotion as deliberate.
      **RULED (2026-08-24, Brett, the same four-question round): APPLY VIA
      A PROPER CHANGE** — the PR #85 equivalent, with its
      drift-check-before-apply discipline (the requirement region's history
      verified untouched before the ratified text lands). Box stays open
      until that change lands; this note records the ruling so the
      executing slice needs no new one.
      **LANDED AND TICKED 2026-08-24 local time (2026-08-25 UTC — the same
      instant the archive folder's UTC stamp records).**
      `apply-branch-sessions-deltas`
      (archived `2026-08-25-apply-branch-sessions-deltas`) carries the ruling: `code_surface: none`, ratified
      on it with one in-window record-citing `Ratified:` line clearing
      approver and date, its delta a byte-for-byte copy of the 2026-08-01
      one (identical SHA-256 `f6ffd39a…`), archived on landing. Drift was
      checked BEFORE applying — the `Corpus scan scope` region hashes to
      `bbb402c4…` at its 2026-07-12 introduction (`1efa5756`), at the source
      archive (`a0ea7666`), and at all three later commits touching the
      promoted spec (`d5e6d428`, `e9a4be6e`, `18a4ffc3`), which touched other
      requirements only, and `Branch-session notebooks` had never been in
      canon at any commit — so the ratified text clobbered no later work.
      Fidelity proven by sha256, not asserted: each promoted block hashes
      identical to the ratified delta's (`99fa2a84…`, `107ede78…`). This
      family now reads **0 findings** in openxFactory, down from the 2 §3.2
      records — measured, not assumed.
- [ ] 5.2 **`docs/doc-health.md`'s check-family table stops at twelve.**
      Families 13 through 17 were added by spec delta and never reached the
      table; this change adds the eighteenth and does not repair the table
      either. Deliberate: repairing another capability's registration inside
      this change would put unrelated families' output on this feature's
      evidence, which is the reasoning `scripts/doc_health/__init__.py`
      already records for the sectionless `proposal-origin` family. It is a
      pre-existing gap, named here so the next reader does not have to
      re-discover it.
      **THE SAME RULE KEPT 4.1's REALIZATION OUT OF THAT DOCUMENT.** The
      report's new per-family basis note is a report-contract addition, and
      `docs/doc-health.md` is `Status: standard` — backed by the PROMOTED
      spec, not by an active change's delta. Putting the note there now would
      put the standard ahead of its canon. It rides this change's
      `doc-health` delta ("The promotion fidelity measurement basis is
      declared") and reaches the document when that delta is promoted, which
      is the same door the eighteenth family itself is waiting at.
      **AND THE SAME RULE KEEPS §4.2's FLIP OUT OF IT.** That document's
      severity table illustrates `error` as "Malformed/unresolved marker;
      free-form status; aging past escalation" — a list this family now
      belongs on. Adding it would put a `standard` document ahead of the
      promoted spec that backs it, exactly as the family table and the basis
      note would. All three arrive together when this change's `doc-health`
      delta is promoted. Box stays open: the table is still twelve rows and
      the gap is still real.
- [x] 5.3 **`python3 -m pytest tests` (the whole directory at once) fails
      collection on a duplicate test basename**, `test_header_value_readers.py`
      in both `tests/doc-health/` and `tests/ideation-dashboard/`. Verified
      pre-existing on a clean `origin/main` checkout with no working-tree
      changes. Not this change's to fix; recorded because a reviewer running
      the obvious command will hit it.
      **CLOSED ELSEWHERE, AND TICKED SO THE PACKET STOPS SAYING SOMETHING
      UNTRUE.** `74af6cc4` (PR #304, "Test infra: whole-suite pytest collects
      again and runs on every PR", #292) removed the `tests/doc-health/`
      duplicate. Re-verified at `700c1a19` on the §4.2 flip: `python3 -m
      pytest tests --collect-only` collects **6418 tests** clean. The box is
      ticked as DISCHARGED-BY-ANOTHER-CHANGE, not as work done here — this
      change never owned it, and the reviewer this note was written for no
      longer hits the defect.

## 6. Archive

- [ ] 6.1 Archive ONLY after merge with green realization evidence.
      `code_surface` is real, so the release-realization rule applies and the
      precedent is `govern-openspec-corpus-membership`: its enforcement landed
      in `7157fa3e`/`bf0bda01` and its archive act was a separate later
      commit, `01ff3434`, titled for the merge it followed. This change
      therefore ships ACTIVE.
