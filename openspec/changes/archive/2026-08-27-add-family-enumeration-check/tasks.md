# Tasks: add-family-enumeration-check

The commissioning ruling (Brett, in-session, 2026-08-25, verbatim: "commission
the §5.5 enumeration check") covers §1 and §2. §3's four design decisions were
taken by the orchestrating session under standing patterns and are flagged for
veto in `proposal.md` § Orchestrator Decisions — reverting any one of them is an
edit to this change, not a new one.

**§5 was deliberately OPEN, and ONE box is still open at the archive.** The
family ships advisory, and the two adjacent gaps it does not close were recorded
there rather than implied. 5.2 was RULED and repaired on 2026-08-25; 5.3 was
DISCHARGED by `add-modified-block-currency-check` on 2026-08-27 and is ticked as
discharged-elsewhere, not as work done here. **5.1 — the flip to enforcing —
stays UNTICKED**, because it is owed on a measured population that by
construction cannot be taken in advance, and leaving the box open is what keeps
that visible instead of letting it become a silent later commit.

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
- [x] 2.5 ARCHIVE AFTER REALIZATION. This change ships ACTIVE and archives only
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
      **DONE — ARCHIVED 2026-08-27, on the merge-plus-green rule this packet
      declared and on the precondition `add-modified-block-currency-check`
      priced.** WHY NOW: that change (ratified 2026-08-27, PR #407, merge
      `d03c03c2`) registers doc-health's TWENTY-SECOND family, and its D5 plus
      its `tasks.md` § 2.1 price this archive as a precondition — `fam_family_
      enumeration` checks every ACTIVE change's restatement of "Deterministic
      check families" against the live registry, and a proposal that registers
      no family cannot lawfully restate the requirement at twenty-two. So the
      twenty-second family's own enumeration block is owed at ITS realization,
      relative to THIS packet's outcome, which is what this act fixes at
      8 → 8.
      **REALIZATION RE-VERIFIED FROM `main` AT THIS GATE, not read out of a PR
      body.** Both merges were re-confirmed ancestors of `origin/main` with
      `git merge-base --is-ancestor`:
      1. **PR #340 → `253c5e87`** — the family itself, advisory at launch
         (§1, §2.1-§2.4, §3, §4.1-§4.8, §4.10-§4.12). Its own commit is
         `bc779dcc`, "Derive the family enumeration instead of trusting it: the
         check that verified itself".
      2. **PR #343 → `1bf16533`** — §5.2's ruled `FAMILY_IDS` repair, "Two
         registered families had no report section: 61 findings rendered
         nowhere".
      The live tree carries the advisory launch in both halves, re-read here
      rather than assumed: `family-enumeration` is registered in `FAMILIES`
      (21 entries), present in `FAMILY_IDS` (21 entries, §5.2's repair intact),
      and ABSENT from `FAMILY_RESOLUTION` — so §5.1's flip is still owed and
      still unticked.
      **THE GATE NUMBERS, all measured in this worktree at base `501a3ae0`.**
      Before the archive act: `python3 -m pytest tests/doc-health -q` →
      **980 passed, 0 failed**; `OPENSPEC_TELEMETRY=0 openspec validate --all
      --strict` → **76 passed, 0 failed (76 items)** = 24 active + 52 promoted
      specs; `python3 scripts/doc-health.py --single-repo .` → **5 critical, 8
      error, 42 warning, 6 info. New regressions vs previous report: 0**; the
      family alone (`--family family-enumeration`) → **0 critical, 0 error, 0
      warning, 0 info**. After the archive act: pytest **980 passed, 0
      failed**; validate **75 passed, 0 failed (75 items)** = 23 active + 52
      specs, −1 exactly as promotion of one change predicts; the single-repo
      run's severity headline **byte-identical — 5 critical, 8 error, 42
      warning, 6 info, 0 new regressions**. The whole report diff is EIGHT
      lines and none of them is a finding: canon words 203344 → 204720 (+1376,
      the promoted block), governance words 656227 → 657603 (+1376, the same
      words moving from active-change prose to promoted prose), canon share
      31.0% → 31.1%, and the promoted-specs row of the per-source table.
      **THE MODIFIED BLOCK WAS RE-VERIFIED PER-REQUIREMENT BEFORE THE ACT, as
      this box demanded and as the sibling archives paid for.** Canon's
      "Deterministic check families" requirement is byte-IDENTICAL between
      `fe34b73c` — the branch point the delta was written against — and
      `501a3ae0`: extracted from both trees and diffed, **0 hunks**. So canon
      did NOT move under this packet and the block reverts nothing; the one
      commit touching the promoted spec since `fe34b73c` (`ad2f2c5a`,
      `harden-ideation-readiness-check`'s archive) added requirements at the
      end of the file and left this one alone.
      **SCENARIO-BY-SCENARIO, 8 → 8.** Titles: identical set, identical order,
      nothing dropped and nothing added. Bullets: `A run executes the check
      families` 11 → 12, the twelfth being this change's own `**AND** family
      enumeration MUST verify this requirement's own family enumeration and
      counts against the code registry as its owning requirement below
      defines`; the other SEVEN scenarios byte-identical bullet for bullet
      (`Lifecycle conformance checks fire` 2/2, `A register carries staged
      status` 2/2, `Drift checks fire` 2/2, `Catalog conformance checks fire`
      2/2, `Routing conformance checks fire` 2/2, `Origin conformance checks
      fire` 2/2, `Roster composition is checked across domains` 3/3).
      **TWO CANON BODY UNITS DIFFER, AND BOTH ARE THIS PACKET'S DECLARED
      REWORDING — named rather than glossed**, because the whole point of the
      per-requirement pass is that a difference gets a disposition instead of a
      shrug. Whitespace-normalized sentence comparison over the requirement
      body found exactly two canon sentences absent from the block, and each is
      present in the block with the numerals moved:
      (1) the total sentence — canon `SHALL implement twenty check families …
      release-inventory drift, and duplicate packet.` → block `SHALL implement
      twenty-one check families … release-inventory drift, duplicate packet,
      and family enumeration.`; and
      (2) the scan-set arithmetic sentence — canon `Four of the twenty … the
      other sixteen families` → block `Four of the twenty-one … the other
      seventeen families`.
      That is the count chain § 1.3 declares this change moves, verified
      against the LIVE registry rather than re-typed: `len(FAMILIES)` = 21, the
      block's total reads `twenty-one`, its enumeration carries 21 names of
      which **0 fail to resolve** to a registered id (one declared alias,
      `client-identity-roster-composition` → `client-identity-composition`, per
      §4.8), `Four of the twenty-one` agrees, and `the other seventeen` equals
      21 − 4. Five block-only sentences and no others: the family's own
      "reads THIS REQUIREMENT and the code registry" figure sentence, and the
      four sentences of the appended FOURTH RESTATEMENT note. Canon's three
      existing self-repair notes are restated verbatim.
      **CANON AFTER THE ACT IS WHAT THE BLOCK IMPLIES AND NOTHING ELSE.**
      `git diff openspec/specs/doc-health/spec.md` → **1 file changed, 128
      insertions(+), 6 deletions(-)**; all six deletions are the re-wrapped
      lines of the two numeral sentences plus the one continuation line the
      new figure sentence extends. Requirements 32 → 33 (the ADDED one),
      file-level scenarios 133 → 141 (+8, the ADDED requirement's own eight),
      and per-requirement counts unchanged everywhere else — `Deterministic
      check families` **8 → 8**, no requirement lost.
      **ONE TEST WAS RE-AIMED BY THIS ACT, NOT DELETED, and it is recorded
      because it is a consequence of the act rather than a defect.**
      `test_this_changes_own_delta_is_the_statement_under_test` was the
      anti-vacuity guard on §4.1's self-gate: it asserted the DELTA half found
      this change's own active delta. The archive act promoted that block, so
      no active change restates the requirement and `_delta_statements`
      legitimately returns nothing — the guard's subject moved into canon with
      the statement. It is now `test_canon_is_the_statement_under_test`, the
      same three assertions one document over (canon parses, total reads
      `twenty-one`, 21 names against 21 families), with the history in its
      docstring; the delta half's own discovery stays covered by §1's fixture
      tests, which is where it always belonged. The neighbouring
      `test_the_real_corpus_reads_zero_on_both_halves` keeps its historical
      claim as written and carries an appended line saying it now reads canon
      alone. Both figures above (980 → 980) are with that re-aim in place.
      **§5 STAYS OPEN WHERE IT WAS OPEN.** 5.1's flip to enforcing is still
      owed on a measured population and is deliberately not taken here. 5.3 is
      DISCHARGED ELSEWHERE — see its own box.

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
- [x] 5.2 REPAIR `FAMILY_IDS`, or rule that the two absences are deliberate.
      `proposal-origin` and `staged-topic-template` are registered families
      with no report section, so their findings publish into the ranked plan
      with no heading of their own. The `proposal-origin` omission is already
      recorded by its owning capability as a known defect; `staged-topic-template`
      appears not to be recorded anywhere. Deliberately not fixed here —
      repairing another capability's registration inside this change would put
      unrelated report output on this feature's evidence, the same reasoning
      that has kept it open twice already. Measured in §4.9 and pinned by test
      so it cannot grow.
      **RULED AND DONE 2026-08-25 — Brett, in-session, verbatim: "fix the
      FAMILY_IDS drift".** Both entries added in `FAMILIES`' own order
      (`staged-topic-template` after `status-validity`, `proposal-origin` after
      `ideation-routing`), which happens to make the two lists order-identical
      today though only MEMBERSHIP is pinned — order is the sequence
      `report.render` emits sections in, so it is a layout choice, and pinning
      it would constrain something nobody has decided.
      **THE CLASS IS CLOSED, NOT THE INSTANCE.**
      `test_the_reporting_list_mirrors_the_registry_exactly` now pins
      `set(FAMILY_IDS) == set(FAMILIES)` in both directions plus
      no-duplicates, so a twenty-second family omitted from the reporting list
      fails by name instead of quietly losing its section. That equality does
      NOT promote the reporting list to a second authority — `FAMILIES` remains
      the sole one, per its own module docstring — it makes the reporting list
      that authority's COMPLETE PROJECTION onto the report.
      **THE MEASURED CONSEQUENCE, which is larger than §4.9 implied.** §4.9
      recorded the two absences as a registration gap. It did not measure what
      they were hiding: `report.render` iterates `FAMILY_IDS` to emit
      "## Findings By Family", so those two families' findings counted in the
      headline and appeared in the ranked plan while rendering under NO SECTION.
      On this repository that was **61 findings — 28 `staged-topic-template`
      warnings and 33 `proposal-origin` (3 ERRORS, 30 warnings)** — invisible in
      the per-family view for as long as the omission stood. Adding the entries
      moves nothing and hides nothing; it renders 61 already-counted findings
      where a reader can see them, in two new sections.
      **THIS CHANGE'S OWN DELTA WAS AMENDED IN THE SAME BREATH**, because it
      had been written from the state of the code rather than from what the code
      should be: it said the reporting list "is allowed to be a subset" and that
      the missing direction MUST NOT be reported. Promoting that would have
      ratified the defect. Amended before promotion, with the original wording
      quoted in the amendment rather than deleted.
- [x] 5.3 THE SCENARIO-COMPLETENESS HALF, which is the half that actually
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
      **DISCHARGED BY ANOTHER CHANGE, NOT BY WORK HERE — ratified 2026-08-27.**
      `add-modified-block-currency-check` (PR #407, merge `d03c03c2`) is exactly
      this half: doc-health's TWENTY-SECOND family compares every ACTIVE
      change's `## MODIFIED Requirements` block against CURRENT canon in three
      arms, and the first of them — scenario-title completeness — is the gate.
      It also adds the authoring obligation to `document-lifecycle` (a MODIFIED
      block restates the requirement as canon currently states it; currency is
      owed continuously while the change is active; a deliberate deletion is
      declared by a reserved marker), which is the promoted rule this box said
      was "mechanical and cheap to state". Its spike measured the class across
      all 23 MODIFIED requirements in the active corpus and read **1
      scenario-arm finding, 14 ledger units across 10 requirements, 0
      title-resolution findings** — and TWO of those ledger units are on THIS
      packet's own block, which this archive gate then examined one by one and
      dispositioned as the declared numeral rewording (§2.5). The box is
      ticked as DISCHARGED-ELSEWHERE rather than as work done here: this change
      never built it, and the reason it did not — a different comparison
      against a different document pair — is the reason the other change
      exists. What remains owed is that packet's own enumeration block at ITS
      realization, relative to this outcome, 8 → 8.
