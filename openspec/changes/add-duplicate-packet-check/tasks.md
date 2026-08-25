# Tasks: add-duplicate-packet-check

The commissioning ruling (Brett, in-session, 2026-08-24, verbatim: "commission
the duplicate-packet check") covers §1 and §2. §3's four design decisions were
taken by the orchestrating session under standing patterns and are flagged for
veto in `proposal.md` § Orchestrator Decisions — reverting any one of them is
an edit to this change, not a new one.

**§5.1 IS NOW CLOSED BY RULING (2026-08-25) — the family ENFORCES.** It shipped
advisory, exactly as this section said it would, and the flip came as its own
ruling rather than a silent later commit. §5.2 and §5.3 stay open, and §5.4 is
new: the flip's one unmeasured exposure, recorded rather than left implicit.

## 1. Ratification

- [x] 1.1 Brett commissioned the check on 2026-08-24, in the terms the night's
      near miss produced: nothing detects two archived packets promoting the
      same delta content, i.e. one ruling discharged twice.
- [x] 1.2 The obligation is stated before the checker enforces it —
      `document-lifecycle` gains "A ruling is discharged once". A checker with
      no promoted rule behind it is a rule invented in Python, which is the
      shape this corpus reads `tag-hygiene`'s by-reference relationship to
      avoid. Checked first whether the obligation was already stated broadly
      enough: it is NOT. "Explicit delta rule" governs prose restating promoted
      policy "in differing words" outside `ideation/brainstorm/`, which is the
      opposite failure (different words, same policy) in a different document
      class; "Ratified spec deltas reach the promoted specification" governs
      arrival in canon and reads clean when a delta arrives twice. Neither
      reaches two archived packets restating one ruling identically.
- [x] 1.3 `doc-health` gains the family and its own requirement, MODIFYING the
      family count to twenty and the "other sixteen" arithmetic that goes with
      it — stacked on `add-release-inventory-drift-check`'s nineteen, which is
      still ACTIVE, as is `add-promotion-fidelity-check`'s eighteen. The
      count is re-derived rather than copied — that sentence has drifted before
      (`staged-topic-template`, registered 2026-08-15, uncounted until
      2026-08-23).

## 2. Implementation

- [x] 2.1 `scripts/doc_health/duplicate_packet.py`: the content fingerprint
      (`fingerprint`), the identity grouping (`collect_statements`), the
      pairwise walk with the lineage exemption (`duplicate_pairs`,
      `_Proposals`), the whole-token change-id matcher (`_mention`), the
      bare-id reader (`change_id`), the pinned-basis tree selection
      (`_repo_trees`), the disposition read, and the family function.
- [x] 2.2 `scripts/doc_health/promotion_fidelity.py` gains three ADDITIVE
      seams and no behaviour change: `DeltaRequirement.body` filled by
      `parse_delta` with the block's raw lines (requirement heading excluded,
      scenario headings included); `declares_pre_ratification` naming the C5
      exemption so a sibling can call it and a monkeypatch of
      `_is_exempt_from_promotion` still moves both callers; and
      `load_dispositions(ctx, family)` / `disposed` made public and
      family-parameterized so `health/dispositions.yaml` has one reader
      between the two families rather than two.
- [x] 2.3 Registration: one import and one `FAMILIES` line in `families.py`
      with the note recording the deliberate `FAMILY_RESOLUTION` absence, one
      `FAMILY_IDS` entry in `__init__.py` so the family gets its own report
      section, and the `families.py` module docstring's owner list.
- [x] 2.4 `tests/doc-health/test_lifecycle_scan_set.py`: the family classified
      as a non-reader, and `len(NON_READERS) == len(FAMILIES) - 4` moved to 16
      (15 on main after #324's nineteenth family, 14 before it). That test FAILED loudly on the unclassified family before the
      edit, which is what it was built to do.
- [ ] 2.5 ARCHIVE AFTER REALIZATION. This change ships ACTIVE and archives only
      on merged-plus-green, following `add-promotion-fidelity-check` and
      `govern-openspec-corpus-membership`: `python3 -m pytest tests/doc-health`
      green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and
      a single-repo doc-health run whose severity counts move by exactly the
      amount the proposal predicts. The archive act is its own commit after the
      merge.

## 3. Orchestrator decisions, flagged for veto

- [x] 3.1 D1 — what fires: content identity, never resemblance. Trailing
      whitespace only (per-line trailing spaces, trailing blank lines); every
      other difference is a different statement. Pairwise per identity.
- [x] 3.2 D2 — the lineage exemption: either proposal naming the other's
      change id, in the bare-id or archived-folder spelling, matched as a whole
      token. Plus the borrowed C5 and `health/dispositions.yaml` exemptions.
      The naming records lineage, not authority — stated in the module, the
      proposal and BOTH spec deltas, because a reader who takes it for an
      authority claim would read this family as adjudicating standing.
- [x] 3.3 D3 — advisory at launch in both halves: `warning` severity AND
      absence from `FAMILY_RESOLUTION`. Both pinned by test.
- [x] 3.4 D4 — acceptance both directions, with the real corpus as one of the
      directions. Evidence in §4.

## 4. Evidence

- [x] 4.1 THE REAL CORPUS READS ZERO. Re-measured at `44505d1e` after merging
      main (the branch point was `700c1a19`; #316, #320, #322, #323, #324 and
      #325 landed in between), openxFactory's
      91 archived packets yield 543 distinct (capability, requirement, content)
      identities. TWO are restated by more than one packet, and both are
      `2026-08-01-add-workbench-branch-sessions` with its landed remedial
      `2026-08-25-apply-branch-sessions-deltas`:
      `lifecycle-notebook-projection` / "Branch-session notebooks" and
      `lifecycle-notebook-projection` / "Corpus scan scope". The remedial's
      `proposal.md` names the original SIX times, in both spellings, so both
      pairs clear the lineage exemption and the family reports **0 findings**.
- [x] 4.2 THE COUNTERFACTUAL, measured beside it. The same corpus with the
      lineage exemption disabled reports **2 findings** — the two pairs above.
      The exemption is the only thing between this family and a false positive
      on the remedy the eighteenth family's action line prescribes.
- [x] 4.3 The two archived delta files are byte-identical, verified
      independently of the family:
      `git hash-object` returns `63e615aa4119b6bba62685fb539660badf9ba73d` for
      both. PR #317's close comment records the same fact from a different
      derivation (delta file sha256 `f6ffd39a…`, block digests `99fa2a84…` and
      `107ede78…`).
- [x] 4.4 THE FIXTURE FIRES, once. `fixtures/duplicate-packet/` carries one
      original and TWO byte-faithful remedials, each naming the original and
      neither naming the other. Three pairs, two exempt, one finding — against
      the later remedial's delta path, never against the original's.
- [x] 4.5 THE FIXTURE STAYS QUIET on every lawful pattern: the codexFactory
      PR #85 shape (original plus one naming remedial), successive MODIFIEDs
      with different content, and two pre-ratification packets restating one
      block with no lineage between them.
- [x] 4.6 THE TOKEN BOUNDARY IS LOAD-BEARING, proven the way the eighteenth
      family proved its tie-break — two runs of one fixture that DISAGREE.
      `add-session-telemetry` is a strict prefix of
      `add-session-telemetry-extended`, whose proposal names only itself; the
      real matcher fires on the pair and the substring test a first draft
      reaches for silences it.
- [x] 4.7 THE SUITE. `python3 -m pytest tests/doc-health` reads
      **862 passed, 7 skipped** on this branch against **837 passed, 7
      skipped** re-measured on a clean `44505d1e` worktree — +25, all in
      `test_duplicate_packet.py`. (The pre-merge figures were 821 against a
      796 baseline; main gained 41 tests across #320/#324/#325 while this
      branch was down, and both numbers were re-measured rather than carried.)
- [x] 4.8 THE REPORT MOVES BY NOTHING. `python3 scripts/doc-health.py
      --single-repo .` on this branch differs from the same run on a clean
      `44505d1e` worktree by exactly four lines, all of them the new family's
      own empty section, with the repository label normalized between the two
      checkout directories. Headline unchanged both runs: `5 critical, 8 error,
      73 warning, 4 info. New regressions vs previous report: 0.`
- [x] 4.9 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` reads
      **77 passed, 0 failed (77 items)** on this branch against **76 passed,
      0 failed (76 items)** on a clean `44505d1e` worktree — +1, this change
      being one item however many capability deltas it carries. Measured rather
      than assumed: the first cut of this line predicted +2 and was wrong. The
      single-change gate is green too: `openspec validate
      add-duplicate-packet-check --strict` reports valid, exit 0.

- [x] 4.10 THE NEIGHBOUR'S FLIP DOES NOT REACH THIS FAMILY. `promotion-fidelity`
      became `error` + `CONTESTED` in PR #325 while this branch was down, and
      PR #324 realized `release-inventory-drift` as the nineteenth family
      (this one is now the twentieth). Re-derived rather than mechanically
      kept: `runner` applies `FAMILY_RESOLUTION.get(f.family, f.resolution)`
      on the finding's OWN family, so a `duplicate-packet` finding cannot
      inherit the contested class even when both families report against the
      same archived delta — the #325 skip-path hazard class. Asserted by
      `test_launch_is_advisory_by_resolution_class` and
      `test_a_disposition_for_the_neighbouring_family_disposes_nothing`, and
      confirmed by the report diff above: this branch's single-repo run adds
      zero `error` findings and zero `uncited-resolution` findings.

## 5. The flip to enforcing — RULED and taken; the rest still open

- [x] 5.1 RULE on raising this family from advisory to enforcing. The flip
      raises severity above `warning` AND adds the `FAMILY_RESOLUTION` entry
      TOGETHER — never one without the other, because a `contested` finding
      that resolves without a citation becomes an `error` under the
      uncited-resolution rule, which is enforcement arriving through the back
      door. Prerequisite evidence: at least one aggregation run across every
      pinned domain factory, so the decision is taken against a measured
      population rather than against openxFactory's own archive.
      **RULED AND TAKEN, 2026-08-25 — Brett, in-session, verbatim: "flip the
      duplicate-packet check to enforcing".** Both halves in one commit, on
      the `add-promotion-fidelity-check` §4.2 precedent (PR #325):
      `duplicate_packet._LAUNCH_SEVERITY = ERROR` and
      `families.FAMILY_RESOLUTION` gains `"duplicate-packet": CONTESTED`. The
      identifier keeps its `_LAUNCH_` name deliberately — it records where the
      value STARTED, and a rename would cost the grep that ties every reader of
      the launch decision together. Both site comments now cite the ruling and
      SUPERSEDE what they used to say, in those words rather than by deletion:
      the recorded reason for the absence from `FAMILY_RESOLUTION` was correct
      for an advisory family and is wrong for an enforcing one.
      **THE SEQUENCING PRECONDITION, measured on the basis this family
      ENFORCES ON (the pinned checkout), not on some other tree.** At the exact
      sha the flip lands on, `d5f447e89cf619fd12113bcf03525468ece4470d`:
      openxFactory carries 91 archived packets and 543 distinct (capability,
      requirement, content) identities, 2 of them restated by more than one
      packet — both the `2026-08-01-add-workbench-branch-sessions` original
      with its landed remedial `2026-08-25-apply-branch-sessions-deltas` — and
      the lineage exemption clears both pairs. **0 findings.** The gate goes
      green on the commit that introduces it.
      **CORROBORATED ON FOUR MORE GOVERNED ARCHIVES**, read-only, at the shas
      they sat at (other sessions' scratch checkouts, left untouched — `git
      status` clean on each, and none is a fresh fetch): codexFactory
      `dff2a3e9f0af` 24 packets / 112 identities / 1 restated / **0**;
      openxFactory at the aggregation pin `ebf87c34f4e6` 89 / 541 / 0 / **0**;
      HealthLinc `52860649ad80` 1 / 7 / **0**; AdxFactory `d302d27b519b`
      1 / 12 / **0**; MedxEHR `004486ac704d` 1 / 7 / **0**. Five governed
      repositories, 206 archived packets, **0 findings**.
      **THE codexFactory RESULT IS THE ONE THAT MATTERS**, and it is the
      lineage exemption proving itself on a real corpus rather than a fixture.
      codexFactory's single restated identity is
      `merge-master-approval` / "Tier-2 ships inactive with report-only
      classification", restated by `2026-08-24-apply-nightly-sweep-activation-
      delta` — **PR #85, the canonical remedial this whole exemption exists to
      keep legal**. Its proposal names the original 4 times, so the pair is
      exempt and the repository reads zero. Had the exemption been wrong, the
      flip would have turned the archetype of the lawful remedy into a gating
      error in another repository.
      **THE PREREQUISITE WAS SHORT WHEN THE FLIP WAS TAKEN, AND IS NOW MET.**
      This box asked for "at least one aggregation run across every pinned
      domain factory". The flip did not have that: five repositories were
      measured, not the full population, and four of the five from scratch
      checkouts at their own shas rather than at the aggregation's pins. That
      shortfall was recorded as §5.4 rather than folded in here — and §5.4 is
      now DISCHARGED. The complete pinned population reads zero: **19
      repositories, 207 archived packets, 1124 identities, 3 restated groups,
      0 findings**, each repository read at the exact sha the aggregation
      pins. The ruling no longer rests on a superseded prerequisite; the
      prerequisite is satisfied. Table and method: §5.4.
- [ ] 5.2 CONSIDER, only by ruling, whether this family should join the
      promotion fidelity family on the live-`main` basis. Today it reads the
      pinned checkout, structurally, because the 2026-08-24 ruling scoped that
      basis to one family and the report says so on every run. The argument for
      moving it is that a lagging aggregation pin delays a duplicate's report;
      the argument against is that the catch point that matters is the pull
      request adding the second packet, which a repository's own self-gate run
      already reads. Not decided here, and NOT decided by the 5.1 flip either:
      enforcing on a tree is not an argument for enforcing on a different one.
      The 5.1 measurement was deliberately taken on the pinned basis for
      exactly that reason — it is the basis the family reads and now gates on.
- [ ] 5.3 THE COUNT SENTENCE'S ORDERING HAZARD, named rather than fixed. Three
      active changes now MODIFY `doc-health`'s "Deterministic check families",
      each restating the whole requirement with its own cumulative list. The
      archive order therefore decides which list canon keeps, and a packet
      archiving out of order silently drops a family from the enumeration. This
      change declares `Sequenced-after:` both of the others; a structural fix —
      making the count derived rather than restated — belongs to its own
      change.

- [x] 5.4 THE FLIP'S UNMEASURED EXPOSURE — OPENED BY THE 5.1 TICK, AND CLOSED
      2026-08-25 BY MEASURING THE WHOLE PINNED POPULATION AT ZERO.
      When the flip was taken, nine of the pinned repositories were unmeasured,
      so a duplicate discharge standing in one of them would have surfaced as a
      gating `error` on the first aggregation nightly rather than as an
      advisory warning. That is a real difference from
      `add-promotion-fidelity-check` §4.3, which discharged its population
      across the full submodule set BEFORE its own flip, and it was recorded
      here rather than left implicit in §5.1.
      **THE GAP IS NOW CLOSED ON THE SAME TERMS §4.3 SET.** The population was
      enumerated from the aggregation repository's own `origin/main` — its
      `.gitmodules` and its gitlinks, read-only — giving **19 pinned
      repositories**. Every one was cloned FRESH and checked out at the EXACT
      SHA the aggregation pins (asserted per repository: the measurement aborts
      if a checked-out HEAD does not equal its pin), and the family was run
      over each on the PINNED BASIS — the basis it enforces on.
      **THE COMPLETE TABLE. No repository is omitted, and a repository with no
      archive is recorded as a zero rather than skipped.**

      | pinned repository | pinned sha | packets | identities | restated | findings |
      | --- | --- | --- | --- | --- | --- |
      | `openxFactory` | `d5f447e89cf6` | 91 | 543 | 2 | **0** |
      | `xFactories/codexFactory` | `dff2a3e9f0af` | 24 | 112 | 1 | **0** |
      | `xFactories/LedgerxFactory` | `a64585865066` | 24 | 136 | 0 | **0** |
      | `xFactories/MedxFactory` | `7577431aa5b4` | 24 | 110 | 0 | **0** |
      | `installs/hermes-install` | `2a4d719c4a40` | 17 | 64 | 0 | **0** |
      | `xFactories/OpsxFactory` | `bf79a9b0b7a4` | 13 | 77 | 0 | **0** |
      | `installs/omnigent-install` | `e1d94db9e4b0` | 9 | 29 | 0 | **0** |
      | `installs/medx-roottruth-install` | `89dca824de6c` | 2 | 27 | 0 | **0** |
      | `xFactories/AdxFactory` | `403ac272f446` | 1 | 12 | 0 | **0** |
      | `xFactories/HealthLinc` | `ce844c14f78b` | 1 | 7 | 0 | **0** |
      | `xFactories/MedxEHR` | `7a1427c41498` | 1 | 7 | 0 | **0** |
      | `xFactories/MedxChart` | `68d2f1f5db93` | 0 | 0 | 0 | **0** (archive directory present and empty) |
      | `xFactories/MedxPractice` | `d8d73195609d` | 0 | 0 | 0 | **0** (no `openspec/`) |
      | `installs/agenttower` | `8a27d21613fc` | 0 | 0 | 0 | **0** (no `openspec/`) |
      | `installs/cloudpc-install` | `344439e93192` | 0 | 0 | 0 | **0** (no `openspec/`) |
      | `installs/keycloak-install` | `ddfb007982b3` | 0 | 0 | 0 | **0** (no `openspec/`) |
      | `installs/openxpki-install` | `3ee98d63dcb5` | 0 | 0 | 0 | **0** (no `openspec/`) |
      | `installs/xfactory-installer` | `4b3a14b95442` | 0 | 0 | 0 | **0** (no `openspec/`) |
      | `openAvatar` | `1998dcf80e99` | 0 | 0 | 0 | **0** (no `openspec/`) |
      | **TOTAL** | **19 repositories** | **207** | **1124** | **3** | **0** |

      **ALL THREE RESTATED GROUPS ARE RECORDED LINEAGE, which is the exemption
      carrying the entire population rather than a fixture.** codexFactory's is
      `merge-master-approval` / "Tier-2 ships inactive with report-only
      classification", restated by `2026-08-24-apply-nightly-sweep-activation-
      delta` — PR #85, the archetype of the lawful remedy — whose proposal names
      its original 4 times. openxFactory's two are
      `lifecycle-notebook-projection` / "Branch-session notebooks" and
      "Corpus scan scope", restated by `2026-08-25-apply-branch-sessions-deltas`,
      whose proposal names its original 6 times. Nothing else in 1124
      identities is restated at all.
      **THREE SHAS MOVED against the pre-flip corroboration**, and they are
      re-stated rather than carried: AdxFactory, HealthLinc and MedxEHR were
      previously read from another session's scratch checkouts at
      `d302d27b519b`, `52860649ad80` and `004486ac704d`, which are NOT the
      aggregation's pins. Re-measured at the pins above; the counts happen to be
      identical, and the earlier figures are superseded by these.
      **THE AGGREGATION CHECKOUT WAS NEVER TOUCHED** — its `origin/main` was
      read with `ls-tree` and `show`, never checked out, and every measured tree
      is a fresh clone in this session's own scratch area.
