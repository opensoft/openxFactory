# Checklist: Fixture Corpus Completeness — 033-add-consent-custody-rederivation-record

**Purpose**: Release-gate validation that the § 4 fixture corpus is planned
completely and precisely enough that a builder cannot land it short — every
named refusal has exactly one fixture and one `T###`, the four positive
shapes are all accounted for, the third WITHHELD bucket is a first-class
expectation table rather than a bolt-on, the detail-pinning discipline closes
every place a bare finding code is too coarse to prove anything, and the three
corpus-count surfaces move together under a re-measure-never-increment rule.
This checklist interrogates the WRITTEN PLAN (`spec.md`, `tasks.md`,
`research.md`, the ratified packet) against itself and against the current
repository state — not whether the corpus has been built yet (it has not: see
the Evaluation section).

**Artifacts under review**: `spec.md` (FR-020 through FR-024, User Story 3),
`tasks.md` (Phase D, T030–T049), `research.md` (R7), `clarify-questions.md`
(Q3, Q9, A1), the ratified delta
(`openspec/changes/add-consent-custody-rederivation-record/specs/consent-instrument/spec.md`),
the ratified packet's own `tasks.md` §§ 4, the canonical validator
(`scripts/validate-consent-instruments.py`), the packaged corpus
(`examples/consent-instrument/`, `.../negative/`), and
`examples/consent-instrument/README.md`.

**Date**: 2026-09-09

---

## A. The named refusals, one fixture each, traced to a task

- [x] CHK001 Does `tasks.md` assign at least one `T###` to each of the six
      INTERNAL-LEG finding codes Q10 adopts (`custody-chain-unanchored`,
      `custody-chain-broken-link`, `custody-chain-locator-gap`,
      `custody-chain-out-of-order`, `custody-pin-rewritten`,
      `custody-path-class-digests-differ`)? [Completeness,
      clarify-questions.md Q10, tasks.md T034–T037/T041/T043]
- [x] CHK002 `custody-chain-unanchored` names TWO distinct anchor failures in
      FR-010 (`e₁.previous_sha256 != custody.sha256` **OR**
      `e₁.previous_locator != custody.locator`) — does T037 give each half its
      OWN fixture rather than one fixture standing for both, per its own
      "detail-pinned so each tests its own half"? [Coverage, spec.md FR-010,
      FR-021, tasks.md T037]
- [x] CHK003 `custody-chain-broken-link` — exactly one fixture, T034, and does
      its description name the precise pair compared
      (`eᵢ.previous_sha256 != eᵢ₋₁.observed_sha256`) rather than "a broken
      link" left generic? [Measurability, tasks.md T034, packet tasks.md 4.3]
- [x] CHK004 `custody-chain-locator-gap` — exactly one fixture, T035, and does
      it explicitly state the digests link CORRECTLY (isolating the locator
      leg from the digest leg) so a reader cannot mistake it for a
      broken-link duplicate? [Isolation, tasks.md T035]
- [ ] CHK005 Is the SAME isolation discipline T035 states for itself
      ("digests linking correctly") also stated for T034 (does the broken-link
      fixture keep its locator pair sound?) and T036 (does the out-of-order
      fixture keep both digest and locator legs sound?) — or is fixture
      isolation a rule applied ad hoc to one fixture rather than a stated
      general discipline for the negative corpus? [Consistency, tasks.md
      T034, T036] — **FINDING:** T035 alone states its isolation condition
      ("digests linking correctly"); T034 and T036 give no equivalent
      assurance, and `self_test`'s `codes_of()` check (validator line 692,
      `elif code not in codes_of(local.errors)`) only requires the expected
      code to be PRESENT among findings, not that it be the ONLY one — so an
      insufficiently isolated fixture (e.g., one that is simultaneously
      out-of-order AND locator-gapped) would still pass self-test without
      testing the invariant its filename claims.
- [x] CHK006 `custody-chain-out-of-order` — exactly one fixture, T036, mapped
      to the packet's own box 4.3c ("so § 4's 'one per named refusal' is true
      of that refusal too")? [Traceability, tasks.md T036, packet tasks.md
      4.3c]
- [ ] CHK007 `custody-pin-rewritten` (T041) — FR-011 names TWO forms: (i)
      `custody.sha256` equal to an entry's `observed_sha256` **while a later
      entry exists**, and (ii) "more generally any state in which the pin has
      been advanced to a value the chain itself records as observed." Does
      T041's single fixture specify a MULTI-entry chain so the sharper form
      (i) — the rewrite masked by a still-later entry — is actually exercised,
      or does the task leave the entry count unstated and risk a
      single-entry fixture that only tests form (ii)? [Ambiguity, spec.md
      FR-011, tasks.md T041] — **FINDING:** T041 ("`custody.sha256` advanced
      to an observed digest while the chain still claims the original
      anchor") does not state the fixture's entry count; FR-011's "while a
      LATER entry exists" clause is the harder, more specific case and is not
      pinned to the fixture design.
- [x] CHK008 `custody-path-class-digests-differ` — exactly one fixture, T043
      (box 4.8d), and is it kept distinct from the SCHEMA-layer `path_only`
      checks (FR-002's pattern/enum constraints) by asserting the schema
      accepts the shape and only the CROSS-FIELD comparison (FR-015) refuses
      it? [Isolation, spec.md FR-015, tasks.md T043]
- [x] CHK009 Is the SCHEMA-layer refusal family (unknown `diff_class`, unknown
      `reason`, missing `ruling_ref`, missing `recorded_by`, an eleventh
      property) enumerated as FIVE distinct named refusals rather than
      collapsed into "schema errors" as one bucket, per FR-021's own
      itemization? [Completeness, spec.md FR-021, tasks.md T038–T040]
- [x] CHK010 Is `embedded-original-content` — reused, not minted — given TWO
      distinct fixtures (blob-shaped `ruling_ref`, blob-shaped `recorded_by`)
      under T042, matching FR-002/FR-016's "both locators, `ruling_ref` and
      `recorded_by` are walked" and the task's own note that this is "the
      fixture pair that proves T026 landed"? [Traceability, tasks.md T042,
      T026]
- [x] CHK011 Total named-refusal count: summing A-side items above (2 + 1 + 1
      + 1 + 1 + 1 + 5 + 2 = 14) — does this reconcile with the ten `T###`
      identifiers in Phase D's negative section (T034, T035, T036, T037,
      T038, T039, T040, T041, T042, T043), where four of them (T037, T038,
      T039, T042) are explicitly "TWO fixtures" each? [Consistency, tasks.md
      Phase D negatives]
- [x] CHK012 Does T044 require EVERY new negative fixture to be registered in
      `EXPECTED_NEGATIVE_FINDINGS` (the table `self_test` reads, validator
      lines 155–169), so that "one fixture per named refusal" is not merely a
      file on disk but a fixture the harness actually asserts against?
      [Completeness, tasks.md T044, validator lines 649–705]
- [x] CHK013 Is the git-dependent half of the ratified delta's refusal
      scenarios — "A locator pair that resolves at neither path," "A chain on
      a commit that is not an ancestor of HEAD," "A HEAD digest matching no
      terminus," "A chain that cannot be re-derived," and "A header_only claim
      contradicted by the diff" — explicitly kept OUT of this feature's
      fixture set, consistent with FR-012's no-git prohibition and § 6/§ 7's
      consumer-owned scope, rather than silently omitted without a stated
      reason? [Scope boundary, delta spec.md scenarios, spec.md FR-012,
      packet tasks.md §§ 6–7]

## B. The four positive shapes

- [x] CHK014 Shape 1 — a two-entry unbroken chain, `header_only` /
      `lifecycle_header_edit`, admitted by the internal legs: assigned to
      T030 (box 4.1)? [Traceability, spec.md FR-020, tasks.md T030]
- [x] CHK015 Shape 2 — an EXISTING example left byte-unchanged and
      re-validated: assigned to T033 (box 4.2), and does the task's own
      language ("Evidence: the diff shows the file untouched and the
      self-test still passes it") commit to a measurable proof rather than an
      assertion? [Measurability, tasks.md T033]
- [x] CHK016 Shape 3 — an `archive_move` / `path_only` entry whose locator
      pair DIFFERS and whose digests are EQUAL: assigned to T031 (box 4.1b),
      citing design C-6a / `proposal.md` Example B? [Traceability, spec.md
      FR-020, tasks.md T031]
- [x] CHK017 Shape 4 — the two-entry `archive_move`→`lifecycle_header_edit`
      chain "the real repair needs": assigned to T032 (box 4.1c), citing
      "prescription I in `design.md` § The consumer handoff"? [Traceability,
      tasks.md T032]
- [x] CHK018 Does the citation in CHK017 resolve to real content — does
      `design.md` § *The consumer handoff* actually contain a labelled
      "I." prescription whose shape (e1 `archive_move`/`path_only`, e2
      `lifecycle_header_edit`/`header_only`) matches what T032 describes,
      rather than pointing at a section that does not exist or does not
      match? [Silently-passes class, design.md lines 429–483] — verified:
      design.md's numbered item 3, sub-item **"I."** (`opensoft-exchange-monitor-reader-consent.yaml`)
      is exactly the two-entry `path_only`→`header_only` shape T032 names.
- [x] CHK019 Are Shapes 1, 3 and 4 mutually distinguishable by which internal
      legs each is built to exercise (chain continuity; path-move digest
      equality; a mixed two-reason chain), so no two of the three positive
      fixtures are redundant proofs of the same leg? [Coverage, spec.md
      FR-020]
- [x] CHK020 Is Shape 2 (T033) kept as a VERIFICATION over an existing file
      rather than counted as a new corpus addition, so the corpus-count
      arithmetic in § F below does not double-count it? [Consistency,
      tasks.md T033, T047]

## C. The third bucket: WITHHELD, and its fail-closed-both-ways table

- [x] CHK021 Is the WITHHELD fixture's directory named explicitly —
      `examples/consent-instrument/withheld/` — as a THIRD, NEW directory
      distinct from the positive and negative trees, per Q3a? [Completeness,
      clarify-questions.md Q3, tasks.md T045]
- [x] CHK022 Is the WITHHELD fixture's shape fully specified — LAST entry
      `diff_class: content`, ALL internal legs sound — so a builder cannot
      satisfy T045 with a fixture that also trips an unrelated internal-leg
      refusal? [Measurability, packet tasks.md 4.8c, tasks.md T045]
- [x] CHK023 Is `EXPECTED_WITHHELD_OUTCOMES` required to be FAIL-CLOSED BOTH
      WAYS — a fixture on disk with no table entry, AND a table entry with no
      fixture on disk, are each errors — explicitly mirroring
      `EXPECTED_NEGATIVE_FINDINGS`'s existing discipline (validator lines
      672–682) rather than a weaker one-directional check? [Completeness,
      clarify-questions.md Q3a, tasks.md T046]
- [x] CHK024 Does the plan require the self-test's note line to report THREE
      bucket counts (valid / negative / withheld) rather than the current
      TWO, so a missing or duplicated withheld fixture is visible in the
      summary line and not only in a raised error? [Measurability, spec.md
      SC-001, tasks.md T046, validator lines 726–730]
- [x] CHK025 Is the PACKAGED withheld fixture's exemption from the new exit
      status (FR-014, "an expected withholding is to the third bucket what an
      expected failure is to a negative") stated as a property of the
      SELF-TEST'S invocation specifically, so the self-test can still exit 0
      while a REAL withheld instrument exits under the new status? [Ambiguity,
      spec.md FR-014, tasks.md T024]
- [x] CHK026 Is `repo_scan` (layer 2) explicitly EXEMPT from the
      fail-closed-both-ways bucket discipline — "reports WITHHELD as it finds
      it," no registration required — consistent with its existing exclusion
      of `EXAMPLES_DIR` (validator line 747)? [Consistency, clarify-questions.md
      Q3b, tasks.md T028]
- [ ] CHK027 Is it stated what happens if the withheld fixture is
      ACCIDENTALLY also schema-invalid or internal-leg-broken (e.g., a typo
      breaks the anchor) — does the plan require the self-test to distinguish
      "yielded WITHHELD" from "yielded an unrelated ERROR" for the withheld
      bucket, the way `EXPECTED_NEGATIVE_FINDINGS` distinguishes
      "negative-should-fail" from "negative-wrong-reason"? [Gap, tasks.md T046]
      — **FINDING:** T046 says the withheld table is "fail-closed BOTH ways
      exactly as `EXPECTED_NEGATIVE_FINDINGS` is," but names only the
      disk/table-entry symmetry, not an outcome-mismatch check analogous to
      `negative-wrong-reason` (validator lines 692–702) — nothing in
      `tasks.md` commits to asserting that a withheld fixture actually
      WITHHELDS (as opposed to erroring or passing) the way a negative
      fixture's finding CODE is checked, not merely its failure.

## D. Detail-pinning where the code alone is too coarse

- [x] CHK028 Does T044 restate the file's own detail-pinning rule verbatim —
      "`schema` is satisfied by any schema error — the existing rule" — as the
      governing discipline for every new `schema`-coded fixture? [Consistency,
      tasks.md T044, validator lines 151–154]
- [x] CHK029 Are ALL FIVE `schema`-coded fixtures (unknown `diff_class`,
      unknown `reason`, missing `ruling_ref`, missing `recorded_by`, eleventh
      property) individually flagged for detail-pinning in `tasks.md`
      ("each detail-pinned on its field" / "detail-pinned on
      `additionalProperties`"), rather than only some of the five? [Coverage,
      tasks.md T038, T039, T040]
- [ ] CHK030 Is there a stated rule that the FIVE `schema`-coded fixtures'
      detail substrings must be MUTUALLY EXCLUSIVE — so that, for instance, the
      missing-`ruling_ref` fixture's error message cannot also satisfy the
      eleventh-property fixture's expected detail by coincidence — or is
      cross-fixture substring collision left unaddressed? [Gap, tasks.md
      T038–T040, validator lines 696–702] — **FINDING:** neither `tasks.md`
      nor `spec.md` states a uniqueness rule across the five `schema`-detail
      substrings; the self-test's own detail check (validator line 696,
      `elif detail and not any(detail in line ...)`) only verifies the
      registered detail appears SOMEWHERE in the errors for that one
      fixture — it does not guard against two fixtures whose chosen
      substrings happen to overlap.
- [x] CHK031 Is `embedded-original-content`'s detail-pinning need addressed —
      given the code is REUSED (already fires for custody-block blobs), do
      the two new blob fixtures (T042) need a detail substring distinguishing
      "found in `custody_rederivations[].ruling_ref`" from "found in
      `.recorded_by`" from the SIX existing custody-block occurrences, or is
      "the code alone" here judged fine-grained enough already (the walked
      path is embedded in every finding message per validator lines 417–421)?
      [Ambiguity, tasks.md T042] — verified: `check_custody`'s
      `embedded-original-content` message (validator line 418, `f"{label}:
      {loc}: value carries..."`) already embeds the exact walked PATH
      (`custody_rederivations[N].ruling_ref` etc.) in every finding, so the
      code is NOT too coarse here and T042 needs no extra detail pin —
      `tasks.md` does not say this explicitly, but the validator's own
      message format makes it true regardless.
- [x] CHK032 Are the schema-layer negatives (T038–T040) kept distinct from the
      one EXISTING `schema`-coded negative already in the corpus
      (`amendment-as-child-instrument.yaml`, detail `parent_ref`), so the new
      fixtures' chosen detail substrings cannot collide with that pre-existing
      entry's? [Consistency, validator line 159, tasks.md T038–T040]

## E. The byte-unchanged existing example

- [x] CHK033 Is FR-003's "the `custody` object MUST be byte-identical" (a
      schema-level requirement, § 2) kept distinct from FR-020/T033's "an
      EXISTING example left byte-unchanged" (a fixture-level requirement,
      § 4), so the two byte-identity claims are not conflated into one task?
      [Consistency, spec.md FR-003, FR-020]
- [x] CHK034 Does T033 require the diff over the CHOSEN existing example file
      to be empty (not merely "the example still validates"), so an edit that
      happens to re-validate is still caught as a violation? [Measurability,
      tasks.md T033]
- [x] CHK035 Is it acceptable that the plan does not name WHICH of the four
      existing instrument examples is chosen for T033 — is this deliberately
      left open (any one suffices to prove additivity) rather than an
      omission the plan should have closed? [Ambiguity, spec.md FR-020] —
      judged NOT a gap: FR-020 says "an existing example," never "a named
      one," and the requirement's purpose (prove growth is additive) is
      satisfied by any choice.
- [x] CHK036 Do the OTHER THREE existing instrument examples (not chosen for
      T033) also stay untouched by this feature's task list — is there any
      task in Phase B–D that edits an existing instrument example other than
      through T033's read-only verification? [Scope boundary, tasks.md Phase
      B–D] — verified: no task in T010–T049 names an edit to any existing
      `*.example.yaml`; all new content is additive (T030–T032, T045) or
      read-only verification (T033).

## F. The three corpus-count surfaces, and re-measure-never-increment

- [x] CHK037 Surface 1 — `examples/consent-instrument/README.md`: assigned to
      T047 (box 4.9), with counts to be obtained "by listing the directories,
      never by arithmetic"? [Traceability, tasks.md T047]
- [x] CHK038 Surface 2 — `contracts/manifest.yaml`'s `consent-instrument`
      corpus comment: assigned to T048 (box 4.9), explicitly warned that it
      "is already false at 6/7 before this feature adds a byte — do not
      increment it, re-count it"? [Traceability, tasks.md T048, research.md
      R7]
- [x] CHK039 Surface 3 — `contracts/README.md`'s row for
      `scripts/validate-consent-instruments.py` +
      `examples/consent-instrument/`: assigned to T049, carried as an
      ADDITIONAL realization act under clarify A1 rather than silently folded
      into T047/T048's scope? [Traceability, clarify-questions.md A1,
      tasks.md T049]
- [x] CHK040 Is the CURRENT (pre-feature) falsity of all three surfaces
      independently measured and cited, rather than assumed — README/manifest
      say "5 valid + 5 invalid" or "5 positives, 5 indexed negatives" against
      a measured 6 valid / 7 negative on disk? [Measurability, research.md
      R7] — verified against the live tree: `contracts/README.md:102` reads
      "self-testing over 5 positives, 5 indexed negatives, and 2 purpose
      probes" and `examples/consent-instrument/{*.example.yaml,negative/*.yaml}`
      count 6 and 7 respectively — the citation is accurate today.
- [x] CHK041 Is a FOURTH possible corpus-count surface ruled out or covered —
      does any OTHER document in the tree (beyond the three named) state a
      packaged-corpus count for this family that this feature's task list
      does not touch? [Completeness, research.md R7] — research.md R7 names
      exactly three documents and states they are the ones affected; no
      fourth surface is identified in `research.md`, `spec.md` or
      `clarify-questions.md`.
- [x] CHK042 Does the re-measure-never-increment rule apply symmetrically to
      ALL THREE surfaces (not only the two the ratified packet names), given
      clarify A1 extends it to the `contracts/README.md` row using "the same
      're-measured rather than adjusted by arithmetic' discipline task 4.9
      sets"? [Consistency, clarify-questions.md A1]
- [x] CHK043 After the corpus grows (per §§ A–C above: +3 new positive
      instrument fixtures, +14 new negative fixtures, +1 withheld fixture,
      6 unchanged examples), do the THREE surfaces' target counts reconcile
      to the SAME arithmetic — 9 positive `*.example.yaml`, 21 negative, 1
      withheld — or does any one document's planned wording imply a
      different total? [Consistency, tasks.md T030–T046] — computed: 6
      existing + 3 new (T030, T031, T032) = 9 `*.example.yaml`; 7 existing +
      14 new (T034–T043, counting T037/T038/T039/T042 as two fixtures each)
      = 21 `negative/*.yaml`; 1 `withheld/*.yaml` (T045). No task text
      contradicts this total.

## G. The example README's growth: tree, third column, nine Named-cases bullets

- [x] CHK044 Is the Layout tree required to be COMPLETE over the grown corpus
      (every new file gets a one-line annotation), matching the existing
      tree's per-file annotation convention (README.md Layout section)?
      [Completeness, clarify-questions.md Q9, tasks.md T047]
- [x] CHK045 Is the *Schema → example map* table required to gain a THIRD
      COLUMN specifically for the withheld bucket, rather than folding the
      withheld fixture into the existing "Negative example(s)" column?
      [Completeness, clarify-questions.md Q9, tasks.md T047]
- [x] CHK046 Is *Named cases from the spec* required to grow by exactly NINE
      bullets, and is the composition of those nine stated as "one bullet per
      refusal code (7) + one positive chain-shapes bullet + one withheld
      bullet"? [Measurability, clarify-questions.md Q9]
- [ ] CHK047 Does the "(7)" in Q9's "one bullet per refusal code (7)"
      reconcile against Q10's list of SEVEN adopted codes — which INCLUDES
      `custody-content-class-withheld` — given Q9 ALSO calls for a separate
      "one withheld bullet" on top of the seven? If withheld is one of the
      seven, the sum double-counts it; if it is not, the seven must be a
      DIFFERENT set (the six chain/pin/path codes plus one more) that no
      document names. [Ambiguity, clarify-questions.md Q9 vs Q10] —
      **FINDING:** Q10 lists exactly seven codes, one of which is
      `custody-content-class-withheld`; Q9's arithmetic (7 + 1 positive + 1
      withheld = 9) only reconciles if the withheld code is EXCLUDED from
      the "(7)" and a seventh NON-withheld code is substituted in its place
      — the most likely candidate being `embedded-original-content` under
      its newly-extended reach (T026/T042) — but no document states this
      substitution; a builder following Q9 literally could read "(7)" as
      Q10's seven codes verbatim and produce a Named-cases section with
      withheld represented twice and `embedded-original-content` not
      represented at all.
- [x] CHK048 Is the *Validating locally* section left untouched (Q9 answers
      "tree and table complete" for growth, naming only those two sections
      plus Named cases — not *Validating locally*), so the plan does not
      silently expect a fourth section to grow with no stated content?
      [Scope boundary, clarify-questions.md Q9]
- [x] CHK049 For the "one positive chain-shapes bullet," does the plan make
      clear this ONE bullet is meant to cover ALL FOUR positive shapes (§ B
      above) collectively, rather than expecting four separate bullets that
      Q9's arithmetic (which totals to 9, not 12) would not support?
      [Ambiguity, clarify-questions.md Q9] — read as consolidated: Q9's own
      sum (7 + 1 + 1 = 9) only closes if "chain-shapes" is a single
      collective bullet; consistent with the existing README's style of one
      bullet per THEME rather than one per fixture file.

## H. Cross-document consistency

- [x] CHK050 Do `spec.md` FR-020–FR-024 and the ratified packet's `tasks.md`
      §4 (4.1–4.9, 4.1b, 4.1c, 4.3b, 4.3c, 4.8b–4.8d) name the SAME set of
      fixtures with no ratified box left uncovered by a Speckit `T###`?
      [Traceability, spec.md, packet tasks.md §4, $FD tasks.md Phase D] —
      cross-checked box-by-box: 4.1→T030, 4.1b→T031, 4.1c→T032, 4.2→T033,
      4.3→T034, 4.3b→T035, 4.3c→T036, 4.4→T037, 4.5→T038, 4.6→T039,
      4.7→T040, 4.8→T041, 4.8b→T042, 4.8c→T045/T046, 4.8d→T043, 4.9→T047/T048
      (+T049 additional). All thirteen ratified § 4 boxes are covered.
- [x] CHK051 Does the BOX ACCOUNTING table at the top of `tasks.md` (line 18)
      list all of 4.1–4.9 including the lettered sub-boxes (4.1b, 4.1c, 4.3b,
      4.3c, 4.8b, 4.8c, 4.8d) among the 35 TICKED boxes, with none of them
      appearing a second time under NOT-OWED or NOT-OWED-HERE? [Consistency,
      tasks.md line 18–21]
- [x] CHK052 Does `research.md` R7's "6 valid + 7 negative + 2 purpose probes"
      MEASURED baseline agree with the validator's own printed self-test note
      format (validator lines 726–730), so the checklist's arithmetic in § F
      is built on the tool's own vocabulary rather than a paraphrase?
      [Consistency, research.md R7, validator lines 726–730]
- [x] CHK053 Is the WITHHELD bucket's existence reflected consistently across
      `spec.md` (User Story 3, FR-022), `tasks.md` (T045/T046), and
      `clarify-questions.md` (Q3) with no document describing a different
      shape (e.g., a fourth bucket, or withheld folded into negatives)?
      [Consistency]

## Evaluation — 2026-09-09

**State of the underlying corpus at evaluation time**: PRE-IMPLEMENTATION.
`contracts/schemas/consent-instrument.schema.yaml` still declares
`contract_schema_version: 2` with no `custody_rederivations` property;
`examples/consent-instrument/withheld/` does not exist;
`examples/consent-instrument/negative/` holds the original 7 files only. This
checklist evaluates the PLAN's completeness and internal consistency, not
whether the corpus has been built — the items above are checked against
`spec.md`, `tasks.md`, `research.md`, `clarify-questions.md`, the ratified
packet, the current validator source, and the current corpus/README bytes,
each cited individually.

**Tally**: 48 passed / 5 open (unticked) / 0 dispositioned (53 total).

**Open findings**: CHK005, CHK007, CHK027, CHK030, CHK047 (5 findings; CHK047
is the load-bearing one — the Named-cases bullet arithmetic in Q9 does not
close against Q10's code list without an unstated substitution).
