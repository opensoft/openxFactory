# Tasks: add-duplicate-packet-check

The commissioning ruling (Brett, in-session, 2026-08-24, verbatim: "commission
the duplicate-packet check") covers §1 and §2. §3's four design decisions were
taken by the orchestrating session under standing patterns and are flagged for
veto in `proposal.md` § Orchestrator Decisions — reverting any one of them is
an edit to this change, not a new one.

**§5 is deliberately OPEN and stays open.** The family ships advisory.
Flipping it to enforcing is a ruling, and leaving the box unticked is how that
stays visible rather than becoming a silent later commit.

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
      family count and the "other fifteen" arithmetic that goes with it. The
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
      as a non-reader, and `len(NON_READERS) == len(FAMILIES) - 4` moved from
      14 to 15. That test FAILED loudly on the unclassified family before the
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

- [x] 4.1 THE REAL CORPUS READS ZERO. At branch point `700c1a19`, openxFactory's
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
      **821 passed, 7 skipped** on this branch against **796 passed, 7
      skipped** re-measured on clean `700c1a19` — +25, all in
      `test_duplicate_packet.py`.
- [x] 4.8 THE REPORT MOVES BY NOTHING. `python3 scripts/doc-health.py
      --single-repo .` on this branch differs from the same run at the branch
      point by exactly four lines, all of them the new family's own empty
      section. Headline unchanged both runs: `4 critical, 8 error, 73 warning,
      4 info. New regressions vs previous report: 0.`
- [x] 4.9 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` reads
      **77 passed, 0 failed (77 items)** on this branch against **76 passed,
      0 failed (76 items)** at the branch point — +1, this change being one
      item however many capability deltas it carries. Measured rather than
      assumed: the first cut of this line predicted +2 and was wrong.

## 5. Open: the flip to enforcing

- [ ] 5.1 RULE on raising this family from advisory to enforcing. The flip
      raises severity above `warning` AND adds the `FAMILY_RESOLUTION` entry
      TOGETHER — never one without the other, because a `contested` finding
      that resolves without a citation becomes an `error` under the
      uncited-resolution rule, which is enforcement arriving through the back
      door. Prerequisite evidence: at least one aggregation run across every
      pinned domain factory, so the decision is taken against a measured
      population rather than against openxFactory's own archive.
- [ ] 5.2 CONSIDER, only by ruling, whether this family should join the
      promotion fidelity family on the live-`main` basis. Today it reads the
      pinned checkout, structurally, because the 2026-08-24 ruling scoped that
      basis to one family and the report says so on every run. The argument for
      moving it is that a lagging aggregation pin delays a duplicate's report;
      the argument against is that the catch point that matters is the pull
      request adding the second packet, which a repository's own self-gate run
      already reads. Not decided here.
- [ ] 5.3 THE COUNT SENTENCE'S ORDERING HAZARD, named rather than fixed. Three
      active changes now MODIFY `doc-health`'s "Deterministic check families",
      each restating the whole requirement with its own cumulative list. The
      archive order therefore decides which list canon keeps, and a packet
      archiving out of order silently drops a family from the enumeration. This
      change declares `Sequenced-after:` both of the others; a structural fix —
      making the count derived rather than restated — belongs to its own
      change.
