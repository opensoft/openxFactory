# Checklist: Release Cut and Versioning — 033-add-consent-custody-rederivation-record

**Purpose**: Release-gate validation that § 5 (the contract cut) is planned to
the letter of `docs/contract-versioning-policy.md` — the five coordinated
Version Identity values, the atomic one-candidate-commit rule, late
allocation with no reservation, re-measurement at every merge-from-main, a
CHANGELOG entry naming the whole bundle (not this session's intention) with
attribution, an ADDITIVE-minor justification that is actually measured, an
inventory that is BUILT rather than hand-edited, all five gates run against
the exact unchanged candidate, the tag left OWED, and the landing contract
(merge commit, re-run on the landed commit, repeat-integration-on-drift). This
checklist interrogates the WRITTEN PLAN for completeness, internal
consistency and fidelity to the ratified policy — not whether the cut has
been taken (it has not: see the Evaluation section).

**Artifacts under review**: `spec.md` (FR-030 through FR-036, User Story 4,
SC-002, SC-005, SC-006, the Out of scope section), `plan.md` (THE LANDING
CONTRACT, Phase H of the Implementation sequence, the Risks table),
`tasks.md` (T060–T066), `research.md` (R2, R3, R6), `clarify-questions.md`
(Q1, Q5, Q6, Q11), `docs/contract-versioning-policy.md` (§§ Version Identity,
Release Digest Inventory, Bundle Realization Order, Change Classes), the
ratified packet's `tasks.md` § 5, and `contracts/CHANGELOG.md`'s
`contract-v3.4` entry (the precedent this cut's entry must match in shape).

**Date**: 2026-09-09

---

## A. Version Identity — the five coordinated values

- [x] CHK001 Are all FIVE values `docs/contract-versioning-policy.md` §
      *Version Identity* names — (1) `contract_schema_version`, (2)
      `contract_bundle_version`, (3) the annotated tag, (4) the exact release
      commit plus per-file digests, (5) the CHANGELOG entry — each assigned to
      a specific requirement or task in this feature, with none left
      unaddressed? [Completeness, policy lines 12–26] — mapped: (1) FR-004/
      T012 (§2); (2) FR-031/T061; (3) FR-035/T066 (left OWED); (4) FR-031/
      FR-033/T061/T063; (5) FR-032/T062. All five covered.
- [x] CHK002 Does the plan correctly resolve the apparent tension between
      policy's "the manifest and changelog update SHALL be committed
      ATOMICALLY WITH THE CONTRACT FILES" (line 29) and Q5a's ruling that the
      schema edit (§ 2, T010–T017) lands in an EARLIER, SEPARATE commit from
      the manifest/changelog/inventory cut (§ 5.2, T061–T063)? [Consistency,
      policy line 29, clarify-questions.md Q5] — verified against the
      `contract-v3.4` precedent's own CHANGELOG entry (table row: "M
      `contracts/manifest.yaml` | ... AND THIS CUT (the `contract_bundle_version`
      line, and nothing else)"): "committed atomically with the contract
      files" is satisfied by the per-file DIGEST re-derivation moving in the
      SAME commit as the bundle-version bump and CHANGELOG entry — not by
      re-committing the contract file's bytes, which may have landed earlier.
      Q5a's "NO SPLIT" ruling and FR-031's "ALL THREE manifest edits...
      included, with NO split" implement exactly this reading, matching
      established practice.
- [x] CHK003 Is the digest re-derivation, the bundle-version bump, and the
      APPENDED `consumption_rule` paragraph explicitly required to be THREE
      edits to `contracts/manifest.yaml` inside the SAME single commit (T061),
      rather than split across the § 2 and § 5.2 commits or left ambiguous
      about which commit each rides? [Measurability, spec.md FR-031, tasks.md
      T061]
- [x] CHK004 Does T017 (the § 2 schema commit) require the commit MESSAGE
      itself to state that the manifest digest is now deliberately stale and
      to NAME T060 as the commit that closes it — creating a self-documenting
      audit trail a reviewer can follow without cross-referencing this
      Speckit tree? [Traceability, tasks.md T017, FR-031]
- [x] CHK005 Is `consent-instrument-class-registry`'s manifest row explicitly
      required to stay UNTOUCHED by the cut (FR-031, T061 — "untouched"
      stated twice), guarding against an over-broad edit that re-derives a
      digest for a file this feature never modifies? [Scope boundary, spec.md
      FR-031, tasks.md T061]

## B. Atomicity: one pull request, one candidate commit

- [x] CHK006 Is "§§ 2–5 land in ONE pull request" (FR-030, Q1a) distinguished
      from "the manifest/changelog/inventory land in ONE candidate commit"
      (FR-031, Q5a) as two SEPARATE atomicity claims at two different
      granularities (PR vs. commit), so a reader cannot satisfy one and
      assume the other is thereby satisfied? [Consistency, spec.md FR-030,
      FR-031]
- [x] CHK007 Is the landing-is-a-MERGE-COMMIT rule (plan.md THE LANDING
      CONTRACT point 4, FR-036) grounded in a stated, checkable fact — "there
      is no linear-history rule on this repository" — rather than asserted
      bare? [Measurability, plan.md THE LANDING CONTRACT] — independently
      verified against this worktree's own `git log`: the last 15 commits on
      `main` include BOTH one-parent (squash) commits and two-parent (real
      merge) commits, so "no linear-history rule" is a true, checkable
      statement and the chosen merge-commit shape for THIS cut does not
      contradict repository practice even though `contract-v3.4` itself
      landed as a squash.
- [x] CHK008 Is § 2's schema commit (T010–T017) required to be a SINGLE
      commit ("One commit" — tasks.md Phase B header), rather than left free
      to split across several, so T017's staleness-disclosure commit message
      has exactly one commit to attach to? [Measurability, tasks.md Phase B
      header, T017]

## C. Late allocation, the ban on reserving, and re-measurement

- [x] CHK009 Is version allocation explicitly deferred to "the final
      integration point after a re-check of availability on all three
      surfaces," and explicitly "never read from this document" (FR-030),
      consistent with policy's Bundle Realization Order step 1? [Completeness,
      spec.md FR-030, policy lines 305–306]
- [x] CHK010 Is the PR body's naming of `contract-v3.5` required to be
      EXPLICITLY PROVISIONAL ("a MEASURED CANDIDATE, never a reservation" —
      plan.md THE LANDING CONTRACT point 2), rather than stated as though
      final, so a reader of the open PR is not misled into treating the
      number as settled before the claim is posted? [Ambiguity, spec.md
      FR-030, plan.md landing contract]
- [x] CHK011 Is re-measurement required at EVERY merge-from-main — not once,
      at branch creation — matching "the orchestrator re-measures at every
      merge-from-main and reports" (FR-030) and T060's "Re-measure at EVERY
      merge-from-main"? [Completeness, spec.md FR-030, tasks.md T060]
- [x] CHK012 Is the CLAIM on openxFactory issue #630 row 4 explicitly scoped
      to the LANE, timed to "the last merge-from-main before the merge — at
      cut time and not before," and explicitly named as this feature's
      OUT-OF-SCOPE act (not this feature's to post)? [Scope boundary, spec.md
      FR-030, Out of scope section, plan.md landing contract point 3]
- [x] CHK013 Does T060 keep MEASURING (and reporting to the lane) separate
      from POSTING the claim — "Report the result to the lane... **Do not
      post the claim**" — so a builder cannot conflate "I measured the
      number" with "I claimed the number," which would violate the
      no-reservation-before-merge-order-is-known rule? [Ambiguity, tasks.md
      T060, policy line 31]
- [x] CHK014 Is the ban on reserving a minor grounded in a NAMED historical
      cost rather than an abstract rule — does the plan or its cited policy
      document the `contract-v2.3` episode (declared-and-untagged for ~19
      hours, then CONSUMED as a spent number by a sibling `contract-v2.4` cut
      inside that window) as the reason the ban exists? [Traceability, policy
      lines 105–125 (§ Untagged Bundles, `contract-v2.3` row), research.md] —
      **the plan itself does not cite this episode** — `research.md` R2 states
      only that `contract-v3.5` is "free on all three surfaces" and that
      "a sibling lane takes it first" is the named risk (plan.md Risks table),
      without pointing to the `contract-v2.3` precedent as the concrete case
      that risk already happened. Not a defect (the ban is still stated and
      obeyed), but the plan's own risk table would be stronger citing the
      precedent it is implicitly guarding against.
- [x] CHK015 Does `spec.md`'s Assumptions section correctly hedge the
      measured `contract-v3.5` figure — "free at the integration point
      UNLESS a sibling lane takes it first; the allocation step re-measures
      rather than trusting this document" — so the document does not
      contradict its own re-measurement requirement by treating R2's finding
      as settled? [Consistency, spec.md Assumptions, research.md R2]

## D. The CHANGELOG: naming the whole bundle, with attribution

- [x] CHK016 Does T062 require the CHANGELOG entry to name ALL 4 additions
      AND ALL 14 modifications under `contracts/` since `contract-v3.4` (18
      paths total), matching `research.md` R6's table exactly rather than a
      subset or a paraphrase? [Completeness, spec.md FR-032, tasks.md T062,
      research.md R6]
- [x] CHK017 Is each of the 18 paths required to be attributed to "its
      originating change/PR" (FR-032), and does `research.md` R6's table
      already carry a concrete PR/lane attribution for every row, so T062 has
      a ready-made source rather than requiring fresh archaeology at cut
      time? [Traceability, research.md R6 table]
- [x] CHK018 Is the `publish-openspec-cli-pin-as-contract-member` A-defer
      registration explicitly singled out as the case "this bundle is what
      finally publishes" (T062, R6), rather than silently folded in as an
      undistinguished modification among the fourteen? [Completeness, spec.md
      line 79, tasks.md T062]
- [ ] CHK019 Is the CHANGELOG discipline required to RE-MEASURE the 18-path
      diff (`git diff --name-status contract-v3.4 HEAD -- contracts/`) AT CUT
      TIME — the same discipline FR-030/T060 impose on the VERSION NUMBER —
      given the Landing Contract itself anticipates `main` moving under
      `contracts/` between integration and merge ("If `main` advanced under
      `contracts/` between integration and merge, the lane REPEATS the
      integration")? [Gap, spec.md FR-032, tasks.md T062, plan.md landing
      contract point 6] — **FINDING:** FR-032 and T062 both state the figure
      as a fact ("the four `contracts/` additions and fourteen modifications
      since `contract-v3.4`") taken from `research.md` R6, itself measured at
      branch creation (`main` `6df21737`). Nothing in `tasks.md` T060–T062
      instructs re-running the `git diff --name-status` sweep at the FINAL
      integration point the way the version-number surfaces are explicitly
      re-measured; if `main` gains further `contracts/` commits before this
      cut lands, the 18-path list named in the CHANGELOG could be stale by
      the time T062 is executed, and nothing in the plan catches that drift
      the way it catches a version-number collision.
- [ ] CHK020 Does the plan require the CHANGELOG entry to argue additivity
      for the FULL bundle (all 18 paths), the way the `contract-v3.4`
      precedent's own entry does ("every edit to a schema that WAS published
      at `contract-v3.3` was checked for narrowing individually"), or only
      for the consent-instrument schema this session authored? [Coverage,
      tasks.md T062, CHANGELOG.md `contract-v3.4` entry "Change class"
      section] — **FINDING:** T062's stated justification ("one new optional
      property, one `contract_schema_version` bump, nothing removed, no
      enumeration narrowed, every existing instrument valid unchanged")
      addresses ONLY the consent-instrument schema growth. The four ADDED
      files are additive by construction (new contracts) and need no
      argument, but the plan does not require re-checking the FOURTEEN
      pre-existing modifications (e.g., the `hermes-domain-overlay` and
      `omnigent` fixture edits) for narrowing before asserting the BUNDLE's
      overall class is ADDITIVE — the precedent this feature is meant to
      match performed that check "clause by clause" across its own full
      diff.
- [x] CHK021 Is the CHANGELOG entry's required SHAPE (a heading naming the
      bundle date and theme, a "Change class" subsection with a per-path
      attribution table, an inventory note on which members re-baseline)
      pointed at the `contract-v3.4` precedent as the template to follow,
      either explicitly in `tasks.md`/`plan.md` or implicitly by this
      checklist's own citation, so a builder is not left to invent the
      entry's structure from FR-032's prose alone? [Gap, tasks.md T062] —
      not explicitly named in `tasks.md`, but the requirement to attribute
      every path "each attributed to its originating change/PR" (T062) is
      specific enough that following the immediately-preceding `contract-v3.4`
      entry in the same file is the obvious and only reasonable model; this
      checklist records the citation so the builder does not have to
      rediscover it.

## E. Change-class justification: ADDITIVE (minor)

- [x] CHK022 Does the stated justification match policy's own "Additive
      (minor)" definition verbatim in substance — "new optional fields, new
      contracts, new validator warnings. Domain repos on the same major
      version remain conformant without changes" (policy § Change Classes)?
      [Consistency, tasks.md T062, policy lines 462–464]
- [x] CHK023 Is the measurement list T062 cites (one new optional property,
      one `contract_schema_version` bump, nothing removed, no enumeration
      narrowed, every existing instrument valid unchanged) each independently
      VERIFIABLE against the § 2 schema diff, rather than asserted as a
      conclusion with no component measurements? [Measurability, spec.md
      FR-001–FR-004, tasks.md T062]
- [x] CHK024 Is the `contract_schema_version` bump (2→3, a number that in
      isolation LOOKS like a breaking-change signal) explicitly reconciled
      with an ADDITIVE (minor) bundle classification, citing the
      `contract-v1.33` precedent (which also bumped a `contract_schema_version`
      1→2 under an additive bundle) so a reviewer does not read the per-schema
      version bump as contradicting the bundle's minor number? [Consistency,
      spec.md FR-004, research.md, manifest.yaml `contract-v1.33` consumption
      rule text]

## F. The digest inventory: BUILT, never hand-edited

- [x] CHK025 Does T063 require the inventory to be produced by EXACTLY
      `python3 scripts/validate-contract-release.py build --tag <version>
      --output contracts/releases/<version>.digests.yaml`, matching the
      script's own subcommand and required flags (`--tag`, `--output`)?
      [Measurability, tasks.md T063, script `build` subparser]
- [x] CHK026 Is "never hand-edited" traced to the policy's own stated reason —
      "editing one so that a check passes destroys the only evidence that the
      release surface moved" (§ *What a red `verify-commit` at HEAD means*) —
      rather than stated as an unexplained prohibition? [Traceability, policy
      lines 292–296, tasks.md T063]
- [x] CHK027 Is T063 required to record the new inventory's ENTRY COUNT and
      its delta against `contract-v3.4`'s 283, giving a measurable, auditable
      size assertion rather than "the inventory was built" alone?
      [Measurability, tasks.md T063]
- [x] CHK028 Does the plan correctly anticipate that building the inventory
      will add NO new row for the consent-instrument schema (it is not a
      release-inventory member per `research.md` R4), so an entry-count
      INCREASE, if any, is attributable only to other bundle members and not
      misread as a missed registration? [Consistency, research.md R4, spec.md
      measured-baseline table]

## G. The five § 5.4 gates against the exact unchanged candidate

- [x] CHK029 Does T064 enumerate exactly the FIVE gates FR-034 names —
      `release-tag-gate` (`validate-release-tag-gate.py`), the pytest set CI
      runs, `validate-manifest-digests.py`, `validate-contract-release.py`
      [verify-commit], `validate-consent-instruments.py --strict` — in the
      same order and with no sixth gate silently added or one silently
      dropped? [Completeness, spec.md FR-034, tasks.md T064]
- [x] CHK030 Is "against the exact unchanged candidate" made operational —
      does the plan require the five gates to run WITHOUT any intervening
      edit between them, so a defect fixed after gate 2 does not leave gates
      1's stale-pass result standing as evidence for the fixed tree?
      [Measurability, tasks.md T064]
- [x] CHK031 Does Q11's ruling — "§ 5.4 is ticked on the LOCAL run of all
      five gates... the workflow's own green is the lane's PR-open
      observation, not this feature's tick condition" — get carried into
      FR-034/T064 precisely, so the plan does not conflate a local pass with
      a GitHub Actions workflow result this feature cannot observe (it opens
      no PR)? [Consistency, clarify-questions.md Q11, spec.md FR-034]
- [x] CHK032 Is `scripts/validate-contract-release.py`'s exact subcommand and
      required flag named correctly — `verify-commit --commit <candidate>`,
      matching the script's own `verify_commit.add_argument("--commit",
      required=True)` — rather than a paraphrase that could be misread as a
      different subcommand (`verify-promotion`, which needs `--remote` and
      `--tag` too)? [Measurability, spec.md SC-005, script `verify-commit`
      subparser]
- [x] CHK033 Are the EXACT local-invocation arguments for `release-tag-gate`
      (which base/head pair substitutes for the PR diff this feature never
      opens) left to the sibling `tooling-and-gates.md` checklist rather than
      silently absent from this file — i.e., is the omission here a deliberate
      cross-reference rather than a gap in EITHER checklist? [Scope boundary]
      — confirmed deliberate: this file covers WHAT the five gates are and
      WHEN they must pass; `tooling-and-gates.md` covers the exact command
      line for each, including `validate-release-tag-gate.py`'s `--head`/
      `--base` arguments.

## H. The tag: left OWED

- [x] CHK034 Is FR-035 ("the annotated tag MUST be left OWED. This feature
      does not tag") unambiguous about WHO tags — § 5.6 named `[OPERATOR]` in
      the ratified packet and T066, Brett Heap's act alone? [Ambiguity,
      spec.md FR-035, packet tasks.md 5.6, tasks.md T066]
- [x] CHK035 Is "OWED" used consistently with its DEFINED meaning in
      `docs/contract-versioning-policy.md` § *Bundle Realization Order* —
      "The gate records it as OWED instead, and step 5 remains an obligation
      on the person who lands step 4" — rather than as a loose synonym for
      "skipped" or "deferred with no owner"? [Consistency, policy lines
      321–325, spec.md FR-035]
- [x] CHK036 Does the plan require the annotated tag, when eventually
      published, to target the LANDED MERGE COMMIT (not the reviewed
      pre-merge candidate), per FR-036 and plan.md landing contract point 7 —
      so a reader of FR-035 alone (which says only "left OWED") is not
      missing the target-commit rule that FR-036 supplies? [Completeness,
      spec.md FR-035, FR-036, plan.md landing contract point 7]

## I. The landing contract (recorded in `plan.md`)

- [x] CHK037 Does `plan.md`'s "THE LANDING CONTRACT" section carry all EIGHT
      numbered points the Q1 ruling establishes (one PR; measured-not-reserved
      with re-measurement at every merge-from-main; the lane claims at the
      last merge-from-main; landing is a merge commit; gates re-run on the
      merge commit before merging; repeat integration if `main` advanced;
      the tag targets the landed merge commit; § 5.5 is the lane's follow-up
      tick), with none of the eight silently dropped? [Completeness, plan.md
      THE LANDING CONTRACT, clarify-questions.md Q1]
- [x] CHK038 Does `spec.md` FR-036 restate the SAME landing contract
      word-consistently with `plan.md`'s section — merge commit, re-run
      against that merge commit as policy step 4's "a different commit,"
      repeat integration on drift — so a reader consulting either document
      alone gets the identical rule? [Consistency, spec.md FR-036, plan.md
      landing contract]
- [x] CHK039 Is the merge-commit re-run requirement grounded explicitly in
      policy's own step 4 language — "If promotion creates a different
      commit, that commit becomes the new candidate and every gate and review
      reruns before tagging" — with the plan's own gloss ("the merge commit
      IS 'a different commit'") citing that exact clause rather than
      inventing a new rule? [Traceability, policy lines 311–313, plan.md
      landing contract point 5]
- [x] CHK040 Is "repeat the integration" (landing contract point 6) given a
      concrete trigger condition — `main` advancing under `contracts/`
      specifically, not any advance of `main` at all — so a builder does not
      over-trigger a full re-integration for an unrelated `main` commit (say,
      a documentation-only change outside `contracts/`)? [Ambiguity, plan.md
      landing contract point 6, FR-036]
- [x] CHK041 Is § 5.5 (landing the exact reviewed commit and the post-merge
      gate re-run it forces) correctly scoped as the LANE's act "in a
      follow-up bookkeeping commit while the packet is still live" — distinct
      from § 5.4 (this feature's own gate run against the PRE-merge
      candidate) — so the two gate-running obligations are not conflated
      into one tick? [Consistency, spec.md Out of scope § 5.5, tasks.md T065,
      plan.md landing contract point 8]

## J. The NOT-OWED-HERE classification of 5.1, 5.5, 5.6

- [x] CHK042 Does `tasks.md`'s BOX ACCOUNTING table (line 16–21) classify
      exactly THREE boxes — 5.1, 5.5, 5.6 — as NOT-OWED-HERE, distinct from
      the EIGHT §§ 6–7 boxes classified as NOT-OWED, matching the Measured
      Baseline table in `spec.md` (line 65: "3 NOT-OWED-HERE... ; 8
      NOT-OWED...")? [Consistency, tasks.md line 18–20, spec.md line 65]
- [ ] CHK043 Does `spec.md` FR-040 — the requirement governing which boxes get
      ticked vs. take a NOT-OWED line — correctly enumerate ALL of 5.1, 5.5
      and 5.6 among "boxes owned elsewhere," or does its parenthetical list
      omit some of them? [Consistency, spec.md FR-040] — **FINDING:** FR-040
      reads: *"every box in §§ 0–5 whose act is verifiably DONE MUST be
      ticked... boxes owned elsewhere (§§ 6, 7 and § 5.6) MUST take dated
      NOT-OWED lines."* The parenthetical names only §§ 6, 7 and § 5.6 — it
      OMITS § 5.1 and § 5.5, even though both are boxes in the §§ 0–5 range
      that are NOT verifiably done (this feature only measures/reports for
      5.1, and only the lane ticks 5.5 later) and are NOT ticked by this
      feature. As written, FR-040 supplies no explicit disposition for 5.1
      or 5.5: they are neither "verifiably done" (so the first clause does
      not tick them) nor named in the "owned elsewhere" parenthetical (so the
      second clause does not require a NOT-OWED line for them either). Every
      OTHER part of `spec.md` (the Measured Baseline table, the Out of scope
      section, SC-002) and all of `tasks.md` (T060, T065, T066, the box
      accounting table) correctly treat 5.1 and 5.5 as NOT-OWED-HERE — so the
      plan's OPERATIVE behavior is correct, but FR-040's own requirement text
      has an internal gap relative to the rest of the same document, and a
      builder implementing FR-040 literally (rather than cross-referencing
      the rest of `spec.md`) could miss writing the NOT-OWED-HERE lines for
      5.1 and 5.5.
- [x] CHK044 Do T060, T065 and T066 each independently supply the dated
      NOT-OWED-HERE disposition FR-040's gap (CHK043) leaves unstated for
      5.1/5.5, and the explicit NOT-OWED-HERE disposition for 5.6 — so the
      TASK LIST closes the gap even though the FR text does not? [Gap
      mitigation, tasks.md T060, T065, T066] — confirmed: T065 and T066 are
      each headed "**NOT-OWED-HERE.**" with an explicit instruction to write
      "Dated NOT-OWED line, no tick," and T060 is scoped to measurement/
      reporting only ("Do not post the claim"), so all three boxes receive a
      disposition in practice regardless of FR-040's own incompleteness.
- [x] CHK045 Is the terminology used in the TASK TEXT for T065/T066
      ("**NOT-OWED-HERE**" as the heading, "Dated NOT-OWED line" as the note
      text to write) internally consistent — i.e., is the NOTE ITSELF meant
      to literally read "NOT-OWED" even though the box's CLASS is
      "NOT-OWED-HERE," or should the written note also say "NOT-OWED-HERE"?
      [Ambiguity, tasks.md T065, T066] — read as intentional shorthand: the
      class label distinguishes WHO owns the act (here vs. elsewhere) for
      this feature's own bookkeeping, while the NOTE WRITTEN INTO the
      packet's `tasks.md` is the general "NOT-OWED" vocabulary FR-040 and the
      packet's own convention use for any unticked box regardless of class;
      `spec.md` FR-040 supports this reading ("MUST take dated NOT-OWED
      lines" for the owned-elsewhere class too). Not a defect, but worth
      recording since the two terms are easy to conflate mid-implementation.

## Evaluation — 2026-09-09

**State of the underlying cut at evaluation time**: PRE-CUT. `contracts/manifest.yaml`
line 3 still reads `contract-v3.4`; the highest tag is `contract-v3.4`
(`807a4f47`, a squash merge); `contracts/releases/contract-v3.4.digests.yaml`
(283 entries) is still the newest inventory; no `contract-v3.5.digests.yaml`
exists; `contracts/CHANGELOG.md` carries no `contract-v3.5` entry. This
checklist evaluates the PLAN's completeness, internal consistency and policy
fidelity — not whether the cut has been taken — against `spec.md`, `plan.md`,
`tasks.md`, `research.md`, `clarify-questions.md`, the ratified packet, the
live `docs/contract-versioning-policy.md`, and the `contract-v3.4` CHANGELOG
entry as precedent, each cited individually above.

**Tally**: 42 passed / 3 open (unticked) / 0 dispositioned (45 total).

**Open findings**: CHK019, CHK020, CHK043. CHK043's gap (FR-040's text omits
5.1/5.5 from its "owned elsewhere" parenthetical) is functionally mitigated
in practice by T060/T065/T066 (see CHK044) — the plan's OPERATIVE behavior is
correct — but FR-040 is the artifact under test for CHK043 and its own text
carries the gap, so it is left unticked rather than credited by proximity to
a task list that happens to compensate for it.
