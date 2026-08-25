# Tasks: add-promotion-fidelity-check

The commissioning ruling (Brett, in-session, 2026-08-24, verbatim: "commission
the archived-delta-vs-promoted-spec check") covers §1 and §2. §3's four design
decisions were taken by the orchestrating session under standing patterns and
are flagged for veto in `proposal.md` § Orchestrator Decisions — reverting any
one of them is an edit to this change, not a new one.

**§4 is deliberately OPEN and stays open.** The family ships advisory. Flipping
it to enforcing is a ruling, and leaving the box unticked is how that stays
visible rather than becoming a silent later commit.

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
- [x] 2.2 `scripts/doc_health/corpus.py`: `RealGit.first_commit_timestamp`.
      `first_commit_date` answers the same question to DAY resolution, which
      is exactly the resolution that cannot break a same-day tie — and 19
      (capability, requirement) pairs in this repository are written twice or
      more on their latest date.
- [x] 2.3 Registration: `FAMILIES` in `families.py`, `FAMILY_IDS` in
      `__init__.py` (so the family gets its own report section — the
      omission that left `proposal-origin` sectionless is a known defect,
      not a pattern to copy), and NOT `FAMILY_RESOLUTION`, with the reason
      recorded at the registration site.
- [x] 2.4 `tests/doc-health/conftest.py`: `FakeGit.first_commit_timestamp`,
      answering `None` where no stamp is supplied — the same degradation
      `RealGit` performs when git cannot answer, which is the fallback path
      §3.4's test exercises deliberately.
- [x] 2.5 `tests/doc-health/test_lifecycle_scan_set.py`: the eighteenth
      family classified as a NON-reader of the lifecycle scan set, and the
      `len(NON_READERS) == len(FAMILIES) - 4` arithmetic advanced from 13 to
      14. This test failed loudly on the registration commit, by name, which
      is exactly what it was built to do.

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
- [x] 3.7 Full suite green: `python3 -m pytest tests/doc-health` →
      764 passed, 7 skipped (baseline 737/7, +27 new).
      `python3 -m pytest tests/ideation-dashboard -k workbench` → 140 passed.
      Every test module importing `doc_health` across
      `tests/ideation-dashboard`, `tests/client-identity-roster` and
      `tests/notebooklm` → 781 passed. `OPENSPEC_TELEMETRY=0 openspec
      validate --all --strict` → green.

## 4. The flip to enforcing — OPEN, and a ruling not a judgement call

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
- [ ] 4.2 **If ruled enforcing, both halves move together**: severity
      `warning` → `error` in `promotion_fidelity._LAUNCH_SEVERITY`, AND a
      `"promotion-fidelity": CONTESTED` entry in `families.FAMILY_RESOLUTION`.
      Taking either alone produces a half-enforcing family nobody chose —
      severity alone gates without the disposition discipline; the contested
      class alone gates through `uncited-resolution` under a family name that
      does not say what happened.
- [ ] 4.3 **If ruled enforcing, the standing population is discharged
      FIRST.** `govern-openspec-corpus-membership` established the ordering
      and the reason: "A gate that goes red on the commit that introduces it
      teaches everyone to route around the gate."

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
- [ ] 5.3 **`python3 -m pytest tests` (the whole directory at once) fails
      collection on a duplicate test basename**, `test_header_value_readers.py`
      in both `tests/doc-health/` and `tests/ideation-dashboard/`. Verified
      pre-existing on a clean `origin/main` checkout with no working-tree
      changes. Not this change's to fix; recorded because a reviewer running
      the obvious command will hit it.

## 6. Archive

- [ ] 6.1 Archive ONLY after merge with green realization evidence.
      `code_surface` is real, so the release-realization rule applies and the
      precedent is `govern-openspec-corpus-membership`: its enforcement landed
      in `7157fa3e`/`bf0bda01` and its archive act was a separate later
      commit, `01ff3434`, titled for the merge it followed. This change
      therefore ships ACTIVE.
