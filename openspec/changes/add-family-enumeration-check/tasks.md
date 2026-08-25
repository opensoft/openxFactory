# Tasks: add-family-enumeration-check

The commissioning ruling (Brett, in-session, 2026-08-25, verbatim: "commission
the §5.5 enumeration check") covers §1 and §2. §3's four design decisions were
taken by the orchestrating session under standing patterns and are flagged for
veto in `proposal.md` § Orchestrator Decisions — reverting any one of them is an
edit to this change, not a new one.

**§5 is deliberately OPEN and stays open.** The family ships advisory, and the
two adjacent gaps it does not close are recorded there rather than implied.

## 1. Ratification

- [x] 1.1 Brett commissioned the check on 2026-08-25, in the terms
      `add-duplicate-packet-check` § 5.5 recorded and left named: derive the
      enumeration and the counts from `FAMILIES` rather than re-typing them
      into canon.
- [x] 1.2 NO `document-lifecycle` delta, and the absence is deliberate. The
      three sibling families each added a lifecycle obligation before their
      checker enforced it, because each checked a rule about DOCUMENTS. This
      one checks `doc-health`'s own requirement about ITSELF — the agreement
      between a promoted sentence and the code that satisfies it — so the
      obligation belongs in `doc-health` and nowhere else. Inventing a
      lifecycle rule to host it would put a rule in a capability that has no
      stake in it.
- [x] 1.3 `doc-health` gains the family and its own requirement, MODIFYING the
      family count to twenty-one and the "other seventeen" arithmetic that
      goes with it. The count is DERIVED at authoring time by the very check
      this change adds — see §4.1 — rather than re-typed and hoped over.

## 2. Implementation

- [x] 2.1 `scripts/doc_health/family_enumeration.py`: the requirement-prose
      reader (`requirement_prose`), the whitespace-flattening statement parser
      (`parse_statement`), the enumeration splitter (`split_enumeration`), the
      prose-name normalization with its declared alias set
      (`normalize_family_name`, `ALIASES`), the number-word table
      (`word_to_int`, `WORD_FOR`), the divergence checks (`_check`), the
      canon/active-delta source selection, and the reporting-list direction
      check (`_check_reporting_list`).
- [x] 2.2 THE WHITESPACE FLATTENING IS LOAD-BEARING AND WAS FOUND BY FAILING.
      The first cut matched the numeral sentences against the requirement's raw
      prose. Canon wraps this requirement mid-phrase across six lines, so the
      total regex matched nothing and the family would have reported the
      requirement as UNREADABLE rather than as correct — a false positive on a
      healthy corpus, caught on the first run against the real tree. Sentences
      are now matched against whitespace-flattened prose, because where a line
      break falls is an editing artefact nobody should have to preserve for a
      numeral to be legible.
- [x] 2.3 Registration: one import and one `FAMILIES` line in `families.py`
      with the note recording the deliberate `FAMILY_RESOLUTION` absence, one
      `FAMILY_IDS` entry in `__init__.py`, and the `families.py` module
      docstring's owner list.
- [x] 2.4 `tests/doc-health/test_lifecycle_scan_set.py`: the family classified
      as a non-reader, and `len(NON_READERS) == len(FAMILIES) - 4` moved from
      16 to 17. That test FAILED loudly on the unclassified family before the
      edit, which is what it was built to do.
- [ ] 2.5 ARCHIVE AFTER REALIZATION. This change ships ACTIVE and archives only
      on merged-plus-green, following `add-duplicate-packet-check` and
      `govern-openspec-corpus-membership`: `python3 -m pytest tests/doc-health`
      green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and
      a single-repo doc-health run whose severity counts move by exactly the
      amount the proposal predicts. The archive act is its own commit after the
      merge. **AT THAT GATE, RE-VERIFY THE MODIFIED BLOCK SCENARIO-BY-SCENARIO
      AGAINST THE CANON OF THE DAY** — three sibling archives needed exactly
      that check and two of them halted on it. This delta was written against
      canon at `fe34b73c`; if another family archives first, canon moves and
      this block must be re-derived against the new text rather than merged.

## 3. Orchestrator decisions, flagged for veto

- [x] 3.1 D1 — the canon half: the family NAME-SET and all three numerals, each
      divergence class reported separately and named precisely. The scan-set
      reader count (`Four`) is canon's own claim and is deliberately NOT
      derived here — no runtime registry of scan-set readers exists, and that
      boundary is already pinned structurally by `test_lifecycle_scan_set.py`.
      This family verifies the arithmetic AROUND that number rather than
      inventing a second authority for it.
- [x] 3.2 D2 — the active-delta half as the real prevention, with canon exempt
      from the count comparison while an active delta restates the requirement.
      Without that exemption the family would fire on every legitimate
      in-flight family branch — including this one.
- [x] 3.3 D3 — advisory at launch in both halves: `warning` severity AND
      absence from `FAMILY_RESOLUTION`. Both pinned by test. Kept even though
      the corpus measures clean.
- [x] 3.4 D4 — acceptance both directions, with the SELF-GATE as one of the
      directions. Evidence in §4.

## 4. Evidence

- [x] 4.1 THE SELF-GATE, run as two steps and recorded as such. This change
      registers the twenty-first family, so it had to restate the very
      requirement it polices.
      **STEP 1 — family registered, delta not yet written.** The check reported
      THREE findings against `openspec/specs/doc-health/spec.md`, each naming
      exactly what diverged:
      - "the promoted requirement omits 1 of the 21 registered check families:
        `'family-enumeration'`"
      - "the promoted requirement says `'twenty'` check families, but 21 are
        registered — expected `'twenty-one'`"
      - "the promoted requirement says `'Four'` of `'twenty'`, but 21 families
        are registered"
      **STEP 2 — this change's delta written.** The same call reports **0
      findings**. The restatement was verified by the check it adds, before the
      change could be committed. `test_the_real_corpus_reads_zero_on_both_halves`
      asserts the zero and
      `test_this_changes_own_delta_is_the_statement_under_test` asserts the
      delta half actually READ this delta, so the first cannot pass vacuously.
- [x] 4.2 THE REAL CORPUS, CANON HALF, at branch point `fe34b73c`: canon's
      enumeration names TWENTY families, every one of them resolves to a
      registered family id, and all three numerals are true of a twenty-family
      registry — total `twenty`, split `Four of the twenty`, remainder
      `sixteen` (20 − 4). **0 findings** before this change registers anything.
- [x] 4.3 THE REAL CORPUS, DELTA HALF: exactly one active change delta restates
      the requirement — this change's own — parsed as total `twenty-one`, 21
      names, split `Four of the twenty-one`, remainder `seventeen`. **0
      findings.**
- [x] 4.4 THE MODIFIED BLOCK IS SCENARIO-COMPLETE, verified rather than
      asserted: canon's requirement carries EIGHT scenarios and this delta
      restates all eight, SEVEN of them byte-identical, the eighth differing by
      exactly one `AND` bullet — this change's own. The three notes canon
      already carries about its own past repairs are restated verbatim, because
      dropping them would be the same destruction class in a new coat.
- [x] 4.5 EACH DIVERGENCE CLASS FIRES ON ITS OWN FIXTURE, asserted on the rule
      text rather than on a count: a missing family name; a stale total with
      the names complete (proving the two halves are independent); an
      unregistered name reported rather than approximated; an arithmetically
      impossible remainder; an unreadable numeral reported rather than treated
      as zero.
- [x] 4.6 THE PREVENTION FIRES: a THIN active delta naming two of twenty-one
      families reports against the DELTA's own path, and canon — complete in
      that fixture — is not reported.
- [x] 4.7 THE LAWFUL PATTERNS STAY QUIET: a correct enumeration with no active
      delta, and the PENDING case (canon at twenty while a complete active
      delta already states twenty-one) which is the one that would otherwise
      make this family fire on every new family's branch.
- [x] 4.8 THE ALIAS SET IS MINIMAL, BY TEST. Nineteen of canon's twenty prose
      names normalize to their registry ids mechanically. ONE does not —
      "client identity roster composition" is registered
      `client-identity-composition`, without `roster` — and it is a declared
      alias rather than an absorbed looseness.
      `test_every_alias_is_load_bearing` asserts each entry still fails to
      normalize mechanically, so a rename that makes it redundant fails loudly
      instead of leaving a private dictionary of forgiveness behind.
- [x] 4.9 `FAMILY_IDS` MEASURED, NOT REPAIRED. The reporting list carries
      NINETEEN entries against a registry of TWENTY-ONE: `proposal-origin` and
      `staged-topic-template` run and report findings with no report section of
      their own. The first is a defect that capability already records. This
      family checks only the other direction — no section promised for a family
      that does not run, which measures clean — and
      `test_the_two_families_absent_from_the_reporting_list_are_measured` pins
      the count at exactly those two so a THIRD cannot join them silently. Box:
      §5.2.
- [x] 4.10 THE SUITE. `python3 -m pytest tests/doc-health` reads **888 passed,
      7 skipped** on this branch against **868 passed, 7 skipped** re-measured
      on a clean `fe34b73c` worktree — +20, all in
      `test_family_enumeration.py`.
- [x] 4.11 THE REPORT MOVES BY NOTHING. `python3 scripts/doc-health.py
      --single-repo .` differs from the same run on a clean `fe34b73c` worktree
      by exactly four lines, all of them the new family's own empty section.
      Headline unchanged both runs.
- [x] 4.12 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` reads **76
      passed, 0 failed (76 items)** on this branch against **75 passed, 0
      failed (75 items)** at the branch point — +1, this change being one item.

## 5. Open

- [ ] 5.1 RULE on raising this family from advisory to enforcing — severity
      above `warning` AND the `FAMILY_RESOLUTION` entry, never one without the
      other, because a `contested` finding that resolves without a citation
      becomes an `error` under the uncited-resolution rule. Prerequisite
      evidence, on the precedent this campaign has now set twice: a measured
      population the gate would red, taken on the basis the family reads.
      Today's measurement is one repository's canon and one active delta; the
      population that matters is every future family-adding branch, which by
      construction cannot be measured in advance.
- [ ] 5.2 REPAIR `FAMILY_IDS`, or rule that the two absences are deliberate.
      `proposal-origin` and `staged-topic-template` are registered families
      with no report section, so their findings publish into the ranked plan
      with no heading of their own. The `proposal-origin` omission is already
      recorded by its owning capability as a known defect; `staged-topic-template`
      appears not to be recorded anywhere. Deliberately not fixed here —
      repairing another capability's registration inside this change would put
      unrelated report output on this feature's evidence, the same reasoning
      that has kept it open twice already. Measured in §4.9 and pinned by test
      so it cannot grow.
- [ ] 5.3 THE SCENARIO-COMPLETENESS HALF, which is the half that actually
      destroyed text. This check derives the ENUMERATION and the COUNTS, which
      is what §5.5 commissioned. A `MODIFIED` block that restates the
      enumeration perfectly and still drops scenarios would pass it — and
      dropping scenarios is exactly what all three siblings did. The rule is
      mechanical and cheap to state: a `MODIFIED` requirement must restate
      every scenario its promoted counterpart carries, because `MODIFIED`
      replaces wholesale. Measured today: every active `doc-health` delta
      restating this requirement is scenario-complete (§4.4), so the class is
      currently clean and the box is prevention rather than backlog. NOT folded
      into this change: it is a different comparison against a different
      document pair, and the commission named the enumeration.
