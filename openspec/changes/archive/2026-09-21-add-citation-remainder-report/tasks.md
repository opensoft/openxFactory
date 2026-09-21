# Tasks: add-citation-remainder-report

Status: ratified
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 2 and it is **NOT IN THIS PULL REQUEST**: this filing carries the
PACKET ONLY. The tasks are individually executable, so under
`release-realization`'s decomposition rule this packet realizes through its own
task list rather than through a feature DAG — in a LATER pull request, on a
LATER word.

**THE TICK RULE, IN THE HOUSE FORM. NOTHING IS TICKED THAT DID NOT LAND.** A
`[x]` below is either a diff in THIS pull request or a measurement recorded
verbatim in this packet and reproducible from the command named beside it.
Nothing is ticked against an intention, against a plan, or against work another
pull request will do.

**AND `design.md` D7'S SCOPE FENCES ARE PROVED MECHANICALLY RATHER THAN
ASSERTED.** Every fence is a `git diff` anybody can re-run against this branch,
and every one of them is EMPTY. **THE BASE IS PINNED TO THIS BRANCH'S MERGE
BASE RATHER THAN SPELLED `origin/main`**, because `origin/main` is a moving ref:
spelled literally, the file-list proof below reads worse every time `main`
advances past this branch, and reads right again the moment the branch takes a
merge — which is a property of the ref and not of the fences. `$(git merge-base
origin/main HEAD)` names the same tree on both sides of that.

```text
$ BASE=$(git merge-base origin/main HEAD)
$ git diff $BASE..HEAD -- scripts/packet_reference.py | wc -l
0
$ git diff $BASE..HEAD -- scripts/validate-pin-registrations.py | wc -l
0
$ git diff $BASE..HEAD -- scripts/doc_health | wc -l
0
$ git diff $BASE..HEAD -- openspec/specs | wc -l
0
$ git diff $BASE..HEAD -- .github/workflows | wc -l
0
$ git diff --name-only $BASE..HEAD
README.md
openspec/changes/add-citation-remainder-report/.openspec.yaml
openspec/changes/add-citation-remainder-report/design.md
openspec/changes/add-citation-remainder-report/evidence/measurement-b1df95ee.md
openspec/changes/add-citation-remainder-report/proposal.md
openspec/changes/add-citation-remainder-report/specs/packet-citation-report/spec.md
openspec/changes/add-citation-remainder-report/tasks.md
tests/sequenced_after/corpus-ledger.yaml
```

EIGHT FILES: the packet's five documents, its committed evidence report, the
README bullet, and the machine-seeded ledger row. No script, no workflow, no test, no promoted byte. A reviewer does
not have to take "nothing is realized" on trust, and neither does a later
reader of the archived packet.

**§ 1 IS OPEN WHERE IT DEPENDS ON A WORD AND TICKED WHERE IT DEPENDS ON A
DIFF.** No word of Brett Heap's ratifies any wording in this packet: #1053 was
filed AS A ROUTING RECORD and NOT CLAIMED, and the word that commissioned this
lane's claim — 2026-09-16, verbatim **"claim #1053 and #1013, fan out wide"** —
commissions the CLAIM and decides no wording. Every document carried
`Status: draft` until Brett Heap's ratification of 2026-09-17, recorded at
[PR #1069, comment
5714138459](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5714138459),
and now carries `Status: ratified`.

**§ 2 (REALIZATION) IS ENTIRELY OPEN.** **§ 3 (RECORDS AND ARCHIVE) IS ENTIRELY
OPEN.**

## 1. The packet, and the ratification word it is held for

### What landed in this pull request

- [x] 1.1 **THE CORPUS WAS RE-MEASURED, NOT QUOTED.** Fresh clone at
      `origin/main` `b1df95ee80633339907c9e661164a783885a5d30`; #1053's own
      recipe re-run through the LANDED `packet_reference.resolve()`: **5,466**
      tracked entries, **2,973** entries in scope (**2,969** files read),
      **586** distinct `openspec/changes/…` tokens, **498** `RESOLVED`
      (**76** relocated), **74** `DANGLING`(identity-half), **7**
      `DANGLING`(file-half), **0** `AMBIGUOUS`, **7**
      `NOT_A_PACKET_REFERENCE` — **inclusive remainder 81 tokens**, carried by
      **65** distinct citing files. `design.md` D0 carries
      the table and the commands. **AND THE SAME RECIPE WAS RE-RUN ON THIS
      BRANCH, AFTER THE PACKET EXISTED**, against the base its head merges —
      at the pair this reading was last taken over (`origin/main` `4cef77af`):
      **2,995** entries in scope, **608** tokens, **518** RESOLVED,
      **remainder 82 — UP BY ONE** from that base's 81
      (`+6 / +8 / +6 / +1`, the delta D0(iv) shows unmoved across five bases;
      the absolutes carry their base because they move with it), and the one is
      `openspec/changes/foo/`, minted by the COMMITTED EVIDENCE REPORT's own
      enumeration of the resolver's docstring examples and then carried by this
      packet's own paragraphs about it too. `design.md` D0(iv)
      carries all five readings, each at the commit it was taken at. **That is D5's argument stopping being a
      prediction**: one report, committed once, +1 remainder.
- [x] 1.2 **THREE FACTS #1053 DOES NOT CARRY WERE FOUND AND EACH MOVED A
      DECISION.** (i) the 74 identity-half tokens collapse to **48 DISTINCT
      IDENTITIES** and all 81 remainder tokens onto **53** (the other 5 are the
      file-half tokens, which resolved their packet), 18 of the 48 cited more
      than once — which is why D3 requires both counts and why every identity
      count in this packet names its scope; (ii) the token grammar manufactures remainder in
      **four** shapes (15 trailing `/`, 2 trailing `-`, 1 trailing `.`, 1
      `/./`), where #1053 names one — which is why D3's normalization is stated
      and printed; (iii) `openspec/changes/README.md`, the resolver docstring's
      own canonical `NOT_A_PACKET_REFERENCE` example, resolves
      `DANGLING`(identity-half) here because the file does not exist in this
      tree — which is why D4 keeps `unclassified` honest.
- [x] 1.3 **THE COST OF THE ALTERNATIVE HOME WAS SIZED FROM THE PROMOTED TEXT,
      NOT ESTIMATED.** `openspec/specs/doc-health/spec.md` *Deterministic check
      families* reads *"twenty-three check families"*;
      `scripts/doc_health/families.py` registers exactly **23** (counted from
      the live registry). *The family enumeration is derived, not restated on
      trust* refuses a restatement that *"omits a registered family, names an
      unregistered one, or carries a numeral inconsistent with the registry in
      its own tree"*, and the advisory-launch rule requires a severity decision
      to *"follow a measurement of the population the gate would red rather
      than precede it"*. `design.md` D1 carries all four items.
- [x] 1.4 **THE DELTA IS ALL-`ADDED` IN A NEW CAPABILITY DIRECTORY.**
      `specs/packet-citation-report/spec.md` carries FIVE `## ADDED`
      requirements over titles that appear nowhere else in the corpus
      (`grep -rn` over `openspec/specs/` and `openspec/changes/*/specs/`), so
      no promoted byte moves, no `## MODIFIED` block is written, no marker is
      owed, and `sequenced_after:` is the POSITIVE root claim `[]` rather than
      a dependency.
- [x] 1.5 **THE ORIGIN IS DECLARED BY THE SANCTIONED WRITER AND `kind: ad_hoc`
      IS CHECKED RATHER THAN ASSUMED.** `.openspec.yaml` was produced by
      `python3 scripts/proposal-support.py <root> declare-adhoc` — the id
      `openxFactory:adhoc:2026-09-16-citation-remainder-report` is the tool's,
      not a hand spelling. `ideation/staging/` was enumerated on 2026-09-16
      (**30** topic folders) and `INDEX.md` read: no topic names the citation
      remainder, a packet-reference report, a reporting CLI or the doc-health
      family set, and the seven staged files whose prose contains "citation",
      "remainder" or "dangling" were opened and every hit is about a different
      subject. Drafting provenance only — no `approved_by`, no `approved_on`.
- [x] 1.6 **THE PER-CHANGE SWEEP-LEDGER ROW IS SEEDED BY THE MACHINE.**
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by …`
      wrote the `add-citation-remainder-report` row in
      `tests/sequenced_after/corpus-ledger.yaml`; the row was not hand-written
      and no other row moved. **THE `moved_by` VALUE IS THE GOVERNING ISSUE
      `#1053`, NOT A PLACEHOLDER** — and it could not be one: the ledger's
      grammar is `MOVED_BY = re.compile(r"^#[0-9]+$")`
      (`scripts/sequenced_after.py:1211`) and the validator refuses anything
      else, so a `#TBD-<what>` spelling is inadmissible here. An issue number
      stands in until § 3.1 re-seeds the row with the pull request that actually
      moves it. The ledger's own contract is why that is safe rather than
      urgent: the field is *"AUTHOR-SUPPLIED AND UNVERIFIED: only its SHAPE is
      checked (`#<digits>`)… a pointer for a human reading the history, not
      evidence."*
- [x] 1.7 **THE README *OpenSpec Records* ACTIVE BULLET IS WRITTEN**, in the
      house form the neighbouring bullets use, marked **DRAFT and HELD** —
      THE STATE AT FILING, 2026-09-16, NOT THE CURRENT ONE (PR #1069, Copilot
      review thread `PRRT_kwDOTAvnrs6jXaQ2`). Brett Heap ratified this packet
      2026-09-17, verbatim **"ratify #1069"** (§ 1.17 below; PR #1069 comment
      [5714138459](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5714138459)),
      and the README bullet now reads **`Status: ratified`**, matching
      `proposal.md`, `design.md` and this file's own header flip. This tick
      records what landed at filing; it does not restate the packet's later
      lifecycle, which § 1.17 and the README itself carry.
- [x] 1.8 **THE FRONT-MATTER `code_surface:` HEAD IS THE BARE REPOSITORY
      IDENTIFIER, VERIFIED AGAINST THE READER AND NOT AGAINST THE PROSE.**
      `gate-code-surface-declarations` is ratified and its realization is in
      flight as openxFactory PR #1029, absent from `main` at `b1df95ee`; a
      sibling writer in this lane ran this packet's declaration through
      `scripts/code_surface.py` on that realization branch at `48bc7de7`. Head
      `openxFactory`, gloss opened by a whitespace-preceded em dash, which
      `_GLOSS_OPENER_RE` (`code_surface.py:166`) admits. **No register entry is
      owed and none is requested.** `design.md` D7 records it.

- [x] 1.9 **THE DEEP RE-MEASUREMENT IS TAKEN AND COMMITTED AS EVIDENCE.**
      `evidence/measurement-b1df95ee.md`, by a sibling writer in this lane at
      the same head `b1df95ee`, is IN this pull request. **INCLUSIVE remainder
      78** (#1053: 80), **THIS-TREE-ONLY 57** (59), **TRUE in-tree remainder by
      manual read 39** ("about 48"), **`AMBIGUOUS` still 0**. **THE
      METHODOLOGY IS PROVED NOT TO BE THE VARIABLE**: run against a control
      clone at `8944758c`, the same instrument reproduces ALL TWELVE of #1053's
      published figures exactly, so every delta is corpus movement and the whole
      −2 is PR #1064's archive of `add-declared-former-id` moving its M1/M2
      fixture citations under the excluded `archive/` path. **ALL 57 ARE
      CLASSIFIED and none is left `unclassified`** — cross-repository 14,
      tokenization artifact 4, self-referential 10, synthetic fixture 18,
      never-existed 6, pre-tracking rename 1, file-half fixture 2, file-half
      stale draft 2 — so #1053's two unclassified tokens are resolved and its
      "≥10" cross-repository lower bound becomes a complete enumeration. The
      run record, the instrument `measure.py`, the 1.5 MB per-token JSON and the
      classification JSON are NOT committed and are cited by repository and
      repo-relative path (`opensoft/brett-wip`,
      `handoffs/xFactory/attachments/openxfactory-1-2026-09-13/1053/`): a packet
      needs the reading, not the dump. **AND WHAT A CLEAN CHECKOUT REPRODUCES
      WITHOUT THE INSTRUMENT IS STATED IN THE EVIDENCE'S OWN HEADER RATHER THAN
      LEFT TO BE ASSUMED** — D0's outcome counts, twice, by independent
      re-implementations of the stated recipe; the § 1.2 and § 1.3 readings, from
      rules those committed sections state; and the § 5 CLASSIFICATION not at
      all, because it is a hand read of INTENT and D4's whole recommendation is
      that no machine may assert it.

### What is held for Brett Heap's word — SEVEN DECISIONS, EACH VETOABLE ALONE

**ALL SEVEN TICK AT THE ARCHIVE, ON THE RATIFICATION ALREADY RECORDED IN THIS
PACKET, AND ON NO NEW DECISION.** Brett Heap ratified this packet
2026-09-17T12:12:06Z, verbatim **"ratify #1069"** ([PR #1069, comment
5714138459](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5714138459)).
**THE WORD IS BARE** — it ratifies the PACKET and names no option individually
— and `design.md`'s own bare-word paragraph, written in advance of any ruling
over this packet, says what that means: *"a bare ratifying word takes the
RECOMMENDED option at all seven; a veto NAMES the decision, and costs that
section alone."* No veto was named, so each of D1 through D7 stands at the
RECOMMENDED option, which is the option this packet already encodes. That
reading is recorded three times over in this packet already and is not minted
here: `.openspec.yaml`'s `approved_by:` block names all seven, `proposal.md`'s
ratification paragraph names all seven, and § 1.17 above records the flip.
**WHY THE BOXES MOVE HERE RATHER THAN AT THE RATIFYING COMMIT.** The
realization plan assigned §§ 1.10–1.16 to that commit; the commit ticked § 1.17
and left these seven standing, which reads as an omission rather than a
reservation — nothing anywhere in the record holds any of them back, and every
one of the seven already carries its own note saying the box is *"unmoved"* by
the folds that landed after the word. The archive is the first act that MAY NOT
leave them open: `scripts/proposal-support.py`'s archive gate refuses outright
while any `- [ ]` stands in this file — `raise SupportError("change has
incomplete tasks")`, and the refusal was taken live at 2026-09-21T20:37:12Z
before these ticks were written — so an archive with them open is not reachable
through the sanctioned path at all. **NOTHING IS DECIDED HERE AND NO OPTION
MOVES.** Each record below names the option the bare word took and, where the
realization has since shipped it, the merge sha that proves it.

- [x] 1.10 **`design.md` D1 — THE HOME OF THE REPORT.** RECOMMENDED: **(b)** a
      report CLI outside doc-health, which is #1053's own recommendation.
      Against **(a)** a twenty-fourth doc-health family NOW — cost: a
      `## MODIFIED` block restating the whole twenty-three-family enumeration,
      a `families.py` registry edit, a numeral, and a severity decision canon
      says must FOLLOW a population measurement; against **(c)** nothing —
      cost: the posture that let #840's dangling `cited_to` citations go
      unnoticed, now measured at 81 tokens nobody looks at.
      **TICKED AT THE ARCHIVE — D1 = (b), THE RECOMMENDED OPTION: A REPORT CLI
      OUTSIDE DOC-HEALTH**, which is #1053's own recommendation. No veto named it.
      **AND (b) IS WHAT SHIPPED**: `scripts/report-citation-remainder.py`, realization
      slice R1, PR [#1100](https://github.com/opensoft/openxFactory/pull/1100) →
      `83166366d499d58b5e8801e0bb17e346c73fc8e6`. Option (a), the twenty-fourth
      doc-health family, is NOT taken and is recorded as residue at § 4.1 below;
      `scripts/doc_health/` and `openspec/specs/doc-health/spec.md` are untouched by
      every one of the four realization landings (D7 fence 4, § 1.16).
- [x] 1.11 **`design.md` D2 — THE SURFACE.** RECOMMENDED: a sibling
      `scripts/report-citation-remainder.py` importing the library, so the
      library's contract stays a library's. Against giving
      `scripts/packet_reference.py` a `__main__` — cost: its own docstring says
      *"this module is a library and has no CLI"*, and a gate
      (`validate-pin-registrations.py`) imports it. **Exit 0 WHATEVER IT FINDS,
      and no `--fail-on`** — which is reserved for D1 option (a). The only
      non-zero exit is the ordinary one for a tool that CANNOT RUN (an
      unreadable tree, a root that is not a repository it can walk), which the
      spec requires and which is a different fact from a finding: "A NON-ZERO
      EXIT SHALL MEAN THE REPORT COULD NOT RUN, never that it found something."
      **AND THREE OF D2'S OWN RULES ARE NOW IN THE REQUIREMENT, ON A SECOND
      WORD.** PR #1069, Copilot threads `PRRT_kwDOTAvnrs6jWmQn`,
      `PRRT_kwDOTAvnrs6jXaN3` and `PRRT_kwDOTAvnrs6jX4Yv` read D2's OUTPUT
      MODEL, its HEADER and its REFINEMENT SEMANTICS; Brett Heap ruled
      2026-09-17T13:33:12Z, verbatim **"fold them in before landing"** ([PR
      #1069, comment
      5715211687](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5715211687)).
      The delta now fixes the REMAINDER ENTRY as a TOKEN, has the report DECLARE
      THE TREE STATE beside the head so an uncommitted edit cannot move the
      counts under a head that did not move, and states the refinement rules —
      segment-boundary matching, admission re-admitting rather than replacing,
      removal applied last and winning. None of the three moves this box: the
      surface is the same sibling script, its flags keep the names, defaults and
      precedence they were ratified with, and **THE EXIT CONTRACT QUOTED ABOVE
      IS UNCHANGED** — a modified tree is DECLARED and never refused, so the only
      non-zero exit is still the report that could not run.
      **TICKED AT THE ARCHIVE — D2 = THE RECOMMENDED OPTION: A SIBLING SCRIPT
      IMPORTING THE LIBRARY, EXIT 0 WHATEVER IT FINDS, AND NO `--fail-on`.** No veto
      named it. **AND IT IS WHAT SHIPPED, WITH THE LIBRARY'S CONTRACT INTACT**:
      `scripts/packet_reference.py` is byte-unmoved across the whole realization (D7
      fence 1, an empty `git diff` proved in § 2.1's own record), so its docstring
      sentence *"this module is a library and has no CLI"* is still true and the
      one-line correction a D2 veto would have owed is not owed. The exit contract
      this box quotes is instrumented rather than asserted:
      `tests/citation_remainder/test_report_citation_remainder.py` carries
      `test_there_is_no_fail_on_flag` — the `tests/former_id_arrival/` instrument that
      enumerates every option string the parser returns and asserts none of them
      converts a finding into a failure — beside `test_a_remainder_of_any_size_still_exits_zero`
      and `test_a_root_that_is_not_a_git_work_tree_exits_non_zero_and_says_it_did_not_run`.
- [x] 1.12 **`design.md` D3 — THE RECIPE.** RECOMMENDED: the stated file
      population (three exclusions, each with a reason, plus the report's own
      output path the moment D5 ever changes), the stated token grammar with
      its four normalizations PRINTED rather than hidden, and — the decision
      that matters — a suspected cross-repository citation **FLAGGED
      `possibly-cross-repo` and left IN the count**. Against dropping it
      silently (cost: an unauditable window sets the headline number); against
      counting it unflagged (cost: the largest known class hides inside a
      number that reads as a defect count).
      **AND D3(c)'S OWN NAMED PROMOTION STEP HAS BEEN TAKEN, ON A SECOND WORD
      AND NOT ON A BENCH WRITER'S.** D3(c) held the THREE-line window and the
      FIVE cross-repository signals in `design.md` and named the step that would
      move them; Brett Heap asked for it, 2026-09-17T12:32:38Z, verbatim **"fold
      it in before landing"** ([PR #1069, comment
      5714405516](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5714405516)).
      They now stand as normative text in the delta's *A suspected
      cross-repository citation is flagged and never dropped* — the window, the
      five signals in D3(c)'s order and closed at five, a scenario per signal
      and two for the window's edges. The DECISION this box holds is unmoved:
      FLAG-never-drop, the inclusive headline and the advisory verdict read as
      they read before, so this box stays open on the same recommendation and
      the same alternatives.
      **AND TWO MORE OF THIS SECTION'S RULES HAVE LANDED ON A WORD OF THEIR
      OWN.** PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jYkwR` reads D3(c)'s
      promoted signals and finds them named with examples rather than with
      grammars. The grammar drafted against it — a CLOSED repository-name
      vocabulary stated in the requirement because this repository carries none
      to read, case-insensitive matching on the measured spellings, the forge
      URL's REPOSITORY segment rather than its owner, name-boundary matching for
      the path-joined form, `validate-pin-registrations.py`'s decoration set
      widened for Markdown, and the parenthetical's whitespace rule — is NEW
      GRAMMAR and not a clarification. Thread `PRRT_kwDOTAvnrs6jafy6` reads
      D3(a) and finds the promoted population arithmetic short a term: an entry
      skipped for leaving the repository root is a tracked FILE that reaches no
      decoder, so it falls in neither of the two skip buckets the closure names
      and the identity does not close. The delta drafted against it adds a THIRD
      term, printed even at zero, and declines folding it into the non-file
      term. Both landed on the word that names them: Brett Heap, 2026-09-17,
      verbatim **"fold B as drafted"** ([PR #1069, comment
      5717459330](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5717459330)).
      This box is unmoved either
      way: the three exclusions, the containment rule, FLAG-never-drop, the
      inclusive headline and the advisory verdict are untouched by any of it.
      **TICKED AT THE ARCHIVE — D3 = THE RECOMMENDED OPTION: THE STATED
      POPULATION, THE STATED GRAMMAR WITH ITS NORMALIZATIONS PRINTED, AND A SUSPECTED
      CROSS-REPOSITORY CITATION FLAGGED `possibly-cross-repo` AND LEFT IN THE COUNT.**
      No veto named it, and neither of the two alternatives — dropping it silently,
      counting it unflagged — was taken. **FLAG-NEVER-DROP IS MEASURED AND NOT MERELY
      SHIPPED**: the first committed reading the report itself produced
      (`evidence/first-report-89d7975d.md`, realization slice R3) prints the INCLUSIVE
      remainder as the headline — 86 tokens over 57 identities at `main`
      `89d7975d` — with the FILTERED count beside it at 47 / 30 and never in place of
      it, which is exactly the arithmetic this decision exists to protect.
      **AND D3(c)'S OWN PROMOTION STEP WAS TAKEN ON A FURTHER WORD OF BRETT HEAP'S,
      WHICH THIS TICK NAMES RATHER THAN FOLDING INTO THE BARE ONE.** The three-line
      window and the five signals moved out of `design.md` and into the requirement
      on his word of 2026-09-17T12:32:38Z, verbatim **"fold it in before landing"**
      ([PR #1069, comment
      5714405516](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5714405516)),
      executed at commit `c6ef48b1` (*"Fold D3(c)'s window and five signals into the
      requirement…"*) and landed with the packet at `ef2b8734` on 2026-09-17T15:57Z
      ([#1053 comment
      5717384931](https://github.com/opensoft/openxFactory/issues/1053#issuecomment-5717384931)).
      That word moved TEXT into canon; it moved no decision, and this box's own
      FLAG-never-drop recommendation is the one the bare word took.
- [x] 1.13 **`design.md` D4 — THE CLASSES.** RECOMMENDED: the classes the report
      ASSERTS are the three the tool can evidence from a path or from its own
      normalization — `truncated`, `punctuation-stripped`, `fixture-path` — and
      the vocabulary is CLOSED at those three plus `unclassified`. A DANGLING
      entry's FAILING HALF is reported too — free, being `Resolution.half`, and
      measured 5 of 5 with no false positives — but as the RESOLVER'S OWN
      OUTCOME, which the delta's first requirement itemizes, and NOT as a fifth
      asserted label: every file-half entry is still named, counted and
      itemized, and its class is whatever its own evidence supports. **RULE
      OTHERWISE AND D4 TAKES IT** — a named `file-half` class counted in the
      class totals — because minting a member of a closed vocabulary is a
      decision for the word and not for a review round. And
      `possibly-cross-repo` ships BESIDE them as an ADVISORY FLAG and NEVER as a
      class, measured at 13 of 14 caught with 2 false positives among the other
      43, which is a reason for a reader to look rather than a verdict. The
      `--json` object carries `class` and every flag as SEPARATE fields (D2), so
      a suspicion never enters a class count and D6's series never counts one.
      And an honest `unclassified` for the five that need a reading of INTENT. Against mechanizing all nine (cost: a machine
      asserting "never existed" from a `git log` miss puts a wrong guess into
      D6's series); against classifying nothing (cost: hands the reader the
      list they already have). **And the rule that governs all nine: NOTHING IS
      REPAIRED** — a dangling reference owes the citing record no edit from
      this tool, which is the other half of the sentence
      `add-declared-former-id` D4 wrote.
      **AND TWO OF D4'S OWN RULES ARE NOW IN THE REQUIREMENT, ON THE SAME SECOND
      WORD.** PR #1069, Copilot threads `PRRT_kwDOTAvnrs6jWmRM` and
      `PRRT_kwDOTAvnrs6jX4Zh`: the promoted precedence settled a normalization
      class against a LOCATION class but not two normalization classes against
      each other, so the delta now states the order D3(b) already fixes —
      `truncated` WINS over `punctuation-stripped`, a token stripped of a
      trailing full stop that still resolves to nothing being SEVERED; and
      `fixture-path` carried a DESCRIPTION where a PREDICATE was owed, so the
      delta now carries D4's own measured probe — EVERY occurrence under the
      top-level `examples/` tree, under `ideation/dashboard/gate-records/`,
      under an `examples/` directory below `contracts/`, or under a `tests/`
      directory nested beneath the population's top-level `tests/` exclusion.
      **THE VOCABULARY IS UNTOUCHED AND STILL CLOSED AT FOUR** — no label is
      minted, renamed, widened or dropped, and the unit those class totals are
      counted in is now stated as the TOKEN — and the `file-half` ruling this
      box holds reads exactly as it reads above.
      **AND THIS SECTION'S TOKENIZATION-ARTIFACT PROBES HAVE LANDED ON A WORD OF
      THEIR OWN.** PR #1069, Copilot thread `PRRT_kwDOTAvnrs6jbfFz` reads the
      closed vocabulary and finds two of its four labels DESCRIBED where
      `fixture-path` is now PREDICATED: "the extraction severed mid-path" is
      semantic, and `punctuation-stripped` names no firing condition at all,
      while D4's three measured sub-probes live only in `design.md`. The text
      drafted against it promotes those probes verbatim — a longer existing path
      on the line ending with the token, a following `<`, and a split string
      literal whose rejoined path resolves — as a union with the trailing-hyphen
      arm under the occurrence rule ALL, and gives `punctuation-stripped` the
      only condition a class asserted on a REMAINDER entry can have. It landed
      on the word that names it: Brett Heap, 2026-09-17, verbatim **"fold B as
      drafted"** ([PR #1069, comment
      5717459330](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5717459330)).
      The box is unmoved either way: the
      vocabulary is the same four labels, the precedence reads as before, and
      the `file-half` ruling this box holds is untouched.
      **TICKED AT THE ARCHIVE — D4 = THE RECOMMENDED OPTION: THE CLASS
      VOCABULARY CLOSED AT `truncated`, `punctuation-stripped`, `fixture-path` AND
      `unclassified`, `possibly-cross-repo` SHIPPING BESIDE THEM AS AN ADVISORY FLAG
      AND NEVER AS A CLASS, AND NOTHING REPAIRED.** No veto named it. **THE ONE
      RULING THIS BOX RESERVED WAS NOT TAKEN**: *"RULE OTHERWISE AND D4 TAKES IT"* — a
      named `file-half` class counted in the class totals — and the bare word ruled
      nothing otherwise, so no fifth member was minted and the vocabulary shipped
      closed at four. The DANGLING entry's failing half is reported as the resolver's
      own outcome, which is where this box put it. Nothing is repaired anywhere: see
      § 4.3 below, and `test_a_dangling_citation_names_its_half_identity_and_citing_files_and_proposes_no_spelling`.
- [x] 1.14 **`design.md` D5 — THE NIGHTLY WIRING.** RECOMMENDED: **artifact-only**,
      one step in `.github/workflows/doc-health-reusable.yml`, committing
      nothing. The reason is measured and is not merely merge conflicts:
      `health/` is INSIDE the file population and carries **0** citation tokens
      today, so a committed report would be the first file there to carry them
      — one per remainder line — and the next run would count its own output.
      Against a date-partitioned commit-back on a lane branch (the
      derive-possibles shape; named as the promotion step, its real advantage
      being that D6's series is then read with one `git log`); against a
      committed rolling `health/citation-remainder.md`, **REFUSED BY NAME**.
      **TICKED AT THE ARCHIVE — D5 = THE RECOMMENDED OPTION: ARTIFACT-ONLY,
      ONE STEP IN `.github/workflows/doc-health-reusable.yml`, COMMITTING NOTHING.**
      No veto named it; the date-partitioned commit-back was not taken and the rolling
      committed file this box REFUSES BY NAME was not taken either. **SHIPPED at
      realization slice R2, PR [#1111](https://github.com/opensoft/openxFactory/pull/1111)
      → `89d7975d9e042ae6987131633bc0dd91226ea6f2`**, reaching the live nightly through
      the aggregation pin-sync opensoft/xFactory PR
      [#467](https://github.com/opensoft/xFactory/pull/467) →
      `d9a0c2b6e4fa82911af443d463cb167e35797bac`. **AND THE WIRING IS PROVED BY RUNS
      RATHER THAN BY A WORKFLOW FILE** — three consecutive artifacts in
      `opensoft/xFactory`, `citation-remainder-2026-09-19` (run 35415908738),
      `citation-remainder-2026-09-20` (run 35484284057) and
      `citation-remainder-2026-09-21` (run 35554784920), 10,682 bytes each — with
      NOTHING committed into the corpus by any of them, which is the whole of what
      this decision bought.
- [x] 1.15 **`design.md` D6 — WHAT "STABLE" MEANS** before option (a) becomes
      takeable: three conditions on the nightly series over `N = 14` runs —
      `unclassified` identities not growing; at most **3** new remainder
      identities, each attributable to a named pull request; the mechanical
      classes at zero net growth. **`N = 14` and the 3 are proposed numbers and
      are the most vetoable figures in this packet.** Against "the count is
      unchanged" (cost: unmeetable — the count moves on every archive) and
      against no condition at all (cost: "later" becomes "never").
      **TICKED AT THE ARCHIVE — D6 = THE RECOMMENDED FIGURES: `N = 14` RUNS,
      AT MOST 3 NEW REMAINDER IDENTITIES EACH ATTRIBUTABLE TO A NAMED PULL REQUEST,
      AND THE MECHANICAL CLASSES AT ZERO NET GROWTH.** The bare word took the numbers
      this box itself calls *"the most vetoable figures in this packet"*, and no veto
      named them. **NOTHING IS MEASURED AGAINST D6 HERE, AND THAT IS NOT AN OMISSION:
      THE SERIES IS THREE RUNS OLD.** The nightly has produced 2026-09-19, 2026-09-20
      and 2026-09-21; `N = 14` is eleven nights away at this archive. Reading the
      condition is the twenty-fourth-family successor's act, and § 4.1 below records
      that successor as NOT FILED by this packet.
- [x] 1.16 **`design.md` D7 — THE SCOPE FENCES.** RECOMMENDED: four, each named
      with the file it protects — no citation edited anywhere by anything; no
      cross-repository reference resolved (only suspected);
      `scripts/validate-pin-registrations.py`'s `check_citations` untouched by
      name; no file under `scripts/doc_health/` or
      `openspec/specs/doc-health/spec.md` moved.
      **TICKED AT THE ARCHIVE — D7 = THE RECOMMENDED OPTION: FOUR FENCES,
      EACH NAMED WITH THE FILE IT PROTECTS AND EACH PROVED BY AN EMPTY `git diff`.**
      No veto named it, and all four held across all four realization landings — the
      proofs stand in §§ 2.1–2.3's own records: no citation was edited anywhere by
      anything, no cross-repository reference was resolved (only suspected, § 1.12),
      `scripts/validate-pin-registrations.py`'s `check_citations` is untouched by name,
      and no file under `scripts/doc_health/` or `openspec/specs/doc-health/spec.md`
      moved. **AND THE FIFTH `git diff` THIS PACKET PROVED EMPTY THROUGHOUT —
      `openspec/specs` — STOPS AT THIS ARCHIVE AND NOWHERE EARLIER.** It was a fence on
      the FILING and on the REALIZATION, both of which promoted nothing; the promotion
      of this packet's five `## ADDED` requirements into
      `openspec/specs/packet-citation-report/` is the act canon requires OF THE
      ARCHIVE — `release-realization`'s *Realization completes*: *"the change archives
      and its deltas promote, exactly as doc-only changes do on landing"* — and it is
      performed in the archive pull request that carries this tick and in no pull
      request before it.
- [x] 1.17 **THE RATIFICATION RECORD IS CUT: THE WORD WAS GIVEN 2026-09-17.**
      Brett Heap ratified this packet, verbatim **"ratify #1069"**, recorded at
      [PR #1069, comment
      5714138459](https://github.com/opensoft/openxFactory/pull/1069#issuecomment-5714138459).
      `.openspec.yaml` gains `approved_by` and `approved_on` as a pure ADDITION
      beside a byte-unmoved drafting provenance (`kind` and `id` never move —
      the shape `add-drafted-proposal-origin` defined), and `proposal.md`,
      `design.md` and this file flip to `Status: ratified`, each citing this
      same comment. **THE FLIP IS NOT HEADER-ONLY IN `proposal.md`**: its
      draft-voiced prose moves with it. `design.md`'s and this file's flip is
      header-only, which is where `docs/document-lifecycle.md`'s own Status
      Claim Rules leave them: *"the REST of the packet is not ruled …
      `tasks.md`, `design.md` … are working files of the change rather than
      documents making a standing claim, and no finding is emitted against
      them under these rules."*

## 2. Realization — A LATER PULL REQUEST, ON A LATER WORD

**NONE OF § 2 IS IN THIS PULL REQUEST.** No script, no workflow and no test is
added, edited, renamed or deleted here.

**REALIZATION HAS SINCE OPENED, IN THE LATER PULL REQUEST THIS SECTION'S OWN
HEADING NAMES, ON THE LATER WORD § 1.17 RECORDS** (2026-09-17, lane
`openxfactory-1`, realization slice R1). The sentence above is the PROPOSAL pull
request's scope statement and is left exactly as it was ratified; this note is
an addendum beside it and moves no decision. § 2.1 is ticked below because its
diff lands in the realization pull request that carries this tick, which is the
tick rule's own first clause. §§ 2.2, 2.3 and 2.4 stay open: the nightly wiring
is a later slice, the committed reading is the slice after that, and the green
evidence is a fact about a merge that has not happened.

- [x] 2.1 **THE REPORT CLI AND ITS UNIT TESTS.**
      `scripts/report-citation-remainder.py` (NEW), importing
      `scripts/packet_reference.py` UNCHANGED: under D2's recommended option 1
      its docstring sentence *"Run: this module is a library and has no CLI"*
      stays true and no line of that module moves. The one-line docstring
      correction is owed ONLY if D2 is vetoed for option 2.
      Argument surface exactly as D2 fixes it (`[REPO_ROOT] [--json] [--all]
      [--tokens] [--history] [--include PREFIX ...] [--exclude PREFIX ...]` — grouping is by IDENTITY
      by default and `--tokens` ungroups it; `--history` is OPT-IN on D2's
      measured cost); exit 0 whatever it finds — *"the report SHALL exit
      successfully whatever it finds, and SHALL NOT provide an option that
      makes a finding fail a run"*, and *"A NON-ZERO EXIT SHALL MEAN THE REPORT
      COULD NOT RUN, never that it found something"* (`design.md` D2) — no
      `--fail-on`. **TWO FIELDS D2 OWES A TEST EACH**: every occurrence's
      `raw` field (the spelling exactly as extracted at that occurrence's
      line, before normalization — carried per occurrence, never a singular
      field on the token; `raw == token` at an occurrence where none fired)
      and, under `--history`, each identity's
      `history` object (`probed`, `ever_tracked`, `first_commit`,
      `last_commit`) — ABSENT, never `null`, when `--history` is not given,
      which is its own test. `tests/citation_remainder/` (NEW): unit tests over a
      THROWAWAY FIXTURE CORPUS built in a `tmp_path` git tree — the shape
      `add-declared-former-id` used for `tests/packet_reference/`, so the tests
      assert against a corpus they construct rather than against the live one,
      which moves under them. Fixtures must cover, at minimum: each of the four
      normalizations; a cross-repository qualifier for each of the five
      signals — a path-joined prefix, a GitHub blob or tree URL, a bare
      qualifier word immediately before the token, the `opsx:opensoft/…`
      custody-locator scheme, and a trailing `(RepoName)` parenthetical — AND
      one at the window's own far edge, the citing LINE plus the three lines
      above it; an identity cited by two tokens; a file-half
      dangler; a deliberately-absent scope-isolation fixture; and the
      `README.md`-shaped case where the raw path's presence decides the
      outcome. **AND THE FIVE FOLDED RULES ARE FIXTURE CASES OF THEIR OWN**, on
      the second fold-in word: a token that is BOTH stripped and severed, which
      must land `truncated` and not `punctuation-stripped`; one identity whose
      two tokens carry different classes, which must stay two entries with two
      classes; a refinement pair exercising segment-boundary matching,
      admission-beside-not-instead-of, and removal-applied-last; a
      `fixture-path` entry every occurrence of which stands in a named fixture
      location, beside one with a single occurrence outside them that must NOT
      take the class; and a reading taken over a modified tree, which must
      declare the tree state beside the head.
      **AND THE ROUND-NINE CLARIFICATIONS ADD THREE MORE**: a citation token
      ending in `.` that RESOLVES exactly as extracted, which must be reported
      resolved and must take neither a normalization record nor a normalization
      class; a token ending in `/`, whose strip stays unconditional and which
      must dedup onto its unslashed sibling; and one identity whose two
      remainder tokens are one flagged and one not, which must keep the identity
      in the FILTERED identity count while only the unflagged token stays in the
      filtered token count — with the arithmetic row asserted in TOKENS against
      the number of REMAINDER ENTRIES carrying the flag and never against the
      corpus-wide flagged figure.
      **AND ROUND ONE ON PR #1097 ADDS THREE POPULATION CASES**, each a tracked
      LINK, because the population arithmetic is now closed by the skip terms'
      EXTENTS rather than by their names: a link that dangles or is otherwise
      unreadable INSIDE the root — a missing target whose lexically resolved
      path still stands inside the root, a looping chain, or a chain that
      cannot be read — which must land in the NON-FILE term and in neither of
      the other two; a link resolving to a DIRECTORY inside the root, which
      must land in the non-file term too and contribute no token; and a link
      resolving OUTSIDE the root, which must land in the out-of-root term
      alone. **AND ROUND TWO ON THE SAME PULL REQUEST ADDS A FOURTH**
      (Copilot thread `PRRT_kwDOTAvnrs6jdWK1`): a dangling link whose target is
      missing but whose lexically resolved path still stands OUTSIDE the
      root — an absolute path elsewhere, say — which must land in the
      out-of-root term alone precisely as a resolving one does, because the
      term is a path predicate and not an existence one. **AND ROUND THREE ON
      THE SAME PULL REQUEST ADDS A FIFTH** (Copilot thread
      `PRRT_kwDOTAvnrs6jsmQR`): a tracked REGULAR FILE, not itself a link,
      standing under a PARENT directory component that is a link whose
      lexically resolved path leaves the root — which must land in the
      out-of-root term alone and must not be read, because the term now owns
      every tracked entry whose resolved path leaves the root and not only an
      entry that is itself a link. The identity is asserted in every one of
      the five — the tracked ENTRIES in scope equalling the FILES read plus
      all three skip terms — and the four links and the fifth's symlinked
      parent are built in the throwaway `tmp_path` tree like every other
      case, this repository tracking no symbolic link at any head this packet
      has measured.
      **LANDED, 2026-09-18, realization slice R1.**
      `scripts/report-citation-remainder.py` and
      `tests/citation_remainder/test_report_citation_remainder.py`, both NEW.
      ONE TEST PER SCENARIO, its docstring naming the scenario verbatim: 72 of
      72 across the five requirements, counted mechanically against
      `specs/packet-citation-report/spec.md` rather than by hand — 43 scenarios
      the ratified delta carried plus the 29 Patch B adds, which have LANDED
      (PR #1097, `main` at `c32749c3`), so the count is taken against the spec
      as it stands in this tree and not against a branch. **THE MECHANICAL
      COUNT IS WHAT MAKES IT WORTH TAKING**: every `#### Scenario:` title is
      searched for in a test docstring, so a scenario a later round REWORDS
      reads as a gap rather than passing silently — which is exactly what
      happened twice, at 63 -> 69 and again at 69 -> 72, and once more on a
      RENAME that moved no behaviour at all
      (*The out-of-root term takes only the links that resolve outside the
      root* -> *...takes exactly the entries whose resolved path leaves the
      root*).
      `scripts/packet_reference.py` is imported UNCHANGED and the D7 fences are
      each empty. **THE LINE AND TEST COUNTS ARE NOT RESTATED HERE**: they moved
      on every review round of the pull request that landed them, a figure
      restated in a frozen record is a figure that goes stale, and the diffstat
      of the merge commit is the place a reader gets them right.
      **AND THE INSTRUMENT IS THE ONE THIS PACKET MEASURED WITH, PROVED AT
      `b1df95ee` RATHER THAN ASSERTED.** Run against a worktree at
      `b1df95ee80633339907c9e661164a783885a5d30`, the shipped CLI reproduces
      `evidence/measurement-b1df95ee.md`'s § 2.1 reading: 2,973
      tracked entries in scope, 2,969 files read, 151
      raw-path-absent holding NOT-A-PACKET-REFERENCE out, 73 repaired by the
      identity rule, INCLUSIVE remainder 78 — 72 identity half, 6 file half, 0
      AMBIGUOUS. **TWO OF THE EVIDENCE'S FIGURES MOVE BY ONE APIECE, BOTH FOR
      THE SAME FIX AND BOTH STATED RATHER THAN SMOOTHED**: distinct tokens read
      572 where the evidence reads 571, and NOT-A-PACKET-REFERENCE 5 where it
      reads 4. The one extra token is `openspec/changes/archive/..` at
      `scripts/validate-ideation-cross-reference.py:31`, which the hand
      instrument folds onto `openspec/changes/archive` by stripping a dot off a
      `..` segment. The CLI refuses to, because rewriting a path that walks UP
      into a citation OF what it walks up from is inventing the citation
      (Copilot `PRRT_kwDOTAvnrs6jsy7w` on PR #1100); the remainder is unmoved at
      78 either way, the token being NOT-A-PACKET-REFERENCE and outside it. It
      is the NORMALIZED
      `issue-native` reading, which is what this delta's three fixed choices
      produce; the 586/162/81 and 586/162/86 figures beside it in the evidence
      are the unnormalized recipe and literal readings, which choice (1)
      forecloses. The three mechanical probes reproduce the hand
      classification's own precision: `truncated` lands on EXACTLY the 4 tokens
      the hand read classed tokenization artifacts, `fixture-path` on 19 — the
      17 of 18 synthetic-fixture entries D4's precision table measures plus the
      2 nested file-half fixtures D4 assigns to it — and the cross-repository
      flag catches 13 of the 14 hand-found cross-repository tokens with 2 false
      positives among the other 43, which is D3(c)'s measured figure, the one
      miss being the token D3(c) already names as reachable by no adjacency
      rule at all.
      **AND THE CLI MINTS NO REMAINDER OF ITS OWN**, which is the acceptance
      check this packet uniquely owes: the hand instrument's `issue-native`
      block reads identically at this branch's merge base and at its head. **THE
      FIGURES ARE PINNED TO THE RUN THAT PRODUCED THEM**, because they are a
      reading of a MOVING corpus and not a property of this packet — taken
      2026-09-18 at head `e170372d`, merge base `4ee21c40`: 604 distinct tokens,
      158 raw-path-absent, 82 inclusive remainder, on both sides, line for line.
      Δ = 0. **AND THE SHIPPED CLI IS RUN AS ITS OWN CONTROL BESIDE THE HAND
      INSTRUMENT**, which is the stronger form of the same check: run over the
      merge-base tree, where it is untracked and therefore unread, and over this
      head, where it is tracked and read, it gives 605 distinct tokens, 82
      inclusive, 43 filtered, 55 and 28 identities on BOTH — only `FILES read`
      moves, by the one file, which is the whole claim. Earlier drafts of this
      record carried 602/154, then 600/157, from runs at earlier heads against
      earlier merge bases; every one of them was Δ = 0 and none was wrong, but
      only one of them is the run this record names, and a record naming
      figures no named run produced is a record a reader cannot check.
      (Copilot `PRRT_kwDOTAvnrs6jdTOB` on PR #1100.)
- [x] 2.2 **THE NIGHTLY WIRING**, at the size D5 rules. Under the recommended
      option: ONE step in `.github/workflows/doc-health-reusable.yml` that runs
      the report and uploads it as a workflow artifact, committing nothing,
      adding no branch and asking no write permission. **AND THE STEP RUNS IN
      THE AGGREGATION CHECKOUT, NOT IN THIS ONE, SO THE PATHS ARE NAMED HERE
      RATHER THAN LEFT TO A DEFAULT.** That workflow is REUSABLE: the caller is
      the xFactory aggregation repository's thin nightly, the checkout is the
      AGGREGATION tree, and this repository is a SUBMODULE inside it. Every
      existing step already spells it out and the new one spells it the same
      way — `python3 openxFactory/scripts/<script>.py` from the aggregation
      root (`doc-health-reusable.yml:582`, `:1045`, `:2233`, `:2498`, `:2875`,
      `:3152` …), never a bare `scripts/…`. So the step is
      `python3 openxFactory/scripts/report-citation-remainder.py openxFactory
      --json > citation-remainder.json`, and **THE REDIRECT IS PART OF THE STEP
      RATHER THAN SHELL DECORATION**: `--json` is a BOOLEAN output-format flag
      on D2's fixed surface and TAKES NO PATH, so the spelling this item first
      carried — `--json <out>` — would hand the CLI a second positional, or, run
      literally by a shell, redirect into a file called `out`; either way the
      artifact-only step has no report to upload. The report writes to STDOUT
      and the step redirects it to ONE named file; the upload step names that
      same path, and the RUN'S DATE belongs in the artifact NAME, not in the
      file name, which is the house convention next door
      (`doc-health-reusable.yml:2251`: `name: doc-health-report-${{ steps.run.outputs.run_date }}`,
      `path:` a plain output path). The SCRIPT path is submodule-qualified and the `REPO_ROOT`
      POSITIONAL IS `openxFactory` — a default of `cwd` would scan the
      aggregation tree, which is a different corpus with a different remainder
      and would read as this repository's. (Contrast `doc-health.py --repo-root .`
      at `:583`, which is multi-repo and MEANS the aggregation root; this report
      is single-repo and does not.) **AND THE OUTPUT IS WRITTEN AT THE
      AGGREGATION ROOT, OUTSIDE `openxFactory/`** — `citation-remainder.json`
      beside the submodule checkout and never inside it — which is D3(a)'s output-path
      fence holding STRUCTURALLY under the recommended option: a file that never
      enters the scanned root cannot be read by the next night's run, whatever
      the exclusion list says. Under D5 option 2 it is instead a
      date-partitioned commit-back on a lane-owned branch in the
      derive-possibles shape, the output moves INSIDE the scanned root, and
      D3(a)'s output-path exclusion becomes LIVE rather than structural and MUST
      land in the same pull request.
      **LANDED, 2026-09-18, realization slice R2.**
      `.github/workflows/doc-health-reusable.yml`, two steps in the `finalize`
      job immediately after `Upload report artifact` — the reading and its
      upload — and `tests/citation_remainder/test_report_wiring.py`, NEW, which
      parses the shipped workflow and pins them. **WHAT THIS TICK CLAIMS IS THE
      DIFF AND NOT A RUN**, which is the tick rule's own first clause: the
      wiring this item describes is in the pull request that carries this tick.
      **THE FIRST `doc-health-nightly` RUN THAT PRODUCES THE ARTIFACT IS OWED
      SEPARATELY AND IS NOT CLAIMED HERE** — cited by run id and artifact name
      (`citation-remainder-<YYYY-MM-DD>`), arriving within 24 hours of the merge
      on the aggregation's own cron (`17 2 * * *`) or immediately by
      `workflow_dispatch`, and landing in § 3.3's realization comment and the
      archive pull request's own evidence list. A merged workflow file is not
      evidence that a step ran, which is the parent packet's § 4.5 lesson one
      notch down, and the distance between the two is exactly this paragraph.
      **THE STEP IS THE ONE THIS ITEM PRESCRIBES, NOT A NEIGHBOUR OF IT**:
      ONE invocation, ONE file, `--json` with no operand, the script path
      submodule-qualified, the `REPO_ROOT` positional `openxFactory`, and the
      redirect target at the aggregation root — each asserted against the
      parsed YAML rather than read, and each proved to BITE by breaking the
      shipped step sixteen ways and watching a named test catch every one.
      **TWO DECISIONS THIS ITEM LEFT OPEN WERE TAKEN IN THAT PULL REQUEST
      RATHER THAN IN A YAML COMMENT.** Q6 — whether a cannot-run of an
      advisory report reds the governance nightly — takes the house's own
      habit over the realization plan's recommendation: `continue-on-error:
      true` plus an explicit `::warning::` on every failure path, because this
      capability's own requirement rules that *"PROMOTING THE REPORT TO A GATE
      SHALL BE A SEPARATE ACT ON A SEPARATE WORD"* and this is not that word,
      because every other optional lane in that file records a graceful skip,
      and because the nightly has concluded `failure` on each of its last eight
      scheduled runs for reasons owned elsewhere, so a ninth way to red it
      carries no signal a reader could act on. NOTHING IS SWALLOWED: the
      warning annotates and the upload's `outcome` gate leaves the artifact
      absent, so a night without a reading is a VISIBLE hole in D6's series
      rather than a false point in it. And the tree-state check the step makes
      of its own checkout is FOLDED under that same posture rather than split
      out to red unconditionally, on a fact measured in the workflow rather
      than assumed: the neutrality lane's merge inside `Run doc-health suite`
      can persist writes under `openxFactory/health/neutrality-drift/` — the
      step immediately after this one exists to commit them back, and
      `baseline/codexFactory.yaml` is already tracked — so a modified checkout
      at this point is a foreseeable state of another lane doing its work and
      not a defect to fail a nightly for. The step is ordered ahead of both
      commit-backs so the reading is taken while the checkout still stands at
      its pinned commit, and that ORDER is itself asserted.
      **AND D6 IS MEASURABLE UNDER D5 OPTION 1, WHICH WAS AN OPEN QUESTION AND
      IS NOW A MEASUREMENT.** The series lives only in artifacts under this
      option, so the retention was read rather than guessed — and read in the
      right repository: a reusable workflow's artifacts belong to the CALLER,
      so they live in `opensoft/xFactory`, which holds every artifact this
      nightly has ever produced while `opensoft/openxFactory` holds none of its
      own. Sixty consecutive artifacts there expire exactly 90 days after their
      run starts (`doc-health-report-2026-09-18`, run `35299844095`, started
      `2026-09-18T02:33:56Z`, expires `2026-12-17T02:33:57Z`). D6's `N = 14`
      window fits six times over, `retention-days: 90` matches that effective
      maximum rather than raising it, and D5 option 2 is not forced.
      **THE SCENARIOS THIS WIRING IS EVIDENCE FOR, BY NAME, AND THE ONE IT IS
      NOT.** R2 realizes no requirement of its own — all five are R1's — but
      the wiring and its test are a DIFFERENT KIND of evidence for three
      scenarios R1 covers at the CLI level, and naming them keeps a reader from
      reading R2 as contributing nothing toward the spec. *The tree read is not
      clean at the head printed* (**The citation remainder is reported**):
      R1's fixtures cover the CLI's own declaration; the step's assertion is
      that fact ENFORCED on the live nightly checkout, pinned by
      `test_the_tree_state_of_the_reading_is_checked_and_not_merely_printed`
      and by
      `test_the_reading_is_taken_before_any_step_that_writes_in_the_submodule`.
      *A reading is compared against an earlier reading* (**The reported
      population is derived from a stated recipe**): a FIXED, non-drifting argv
      is what keeps each night's reading a later point in the SAME series
      rather than a differently defined one, pinned by
      `test_the_argv_is_the_fixed_one_and_carries_no_refinement`,
      `test_the_nightly_runs_the_report_exactly_once`,
      `test_the_script_path_is_submodule_qualified`,
      `test_the_repo_root_positional_is_this_submodule_and_never_a_default` and
      `test_the_json_flag_is_passed_with_no_operand`. *The report's own output
      is committed into the corpus* (same requirement): under D5 option 1 the
      nightly commits nothing, so the scenario's antecedent never fires on this
      path — R2 makes it INAPPLICABLE by construction rather than making it
      pass, the output standing outside the scanned root by
      `test_the_reading_is_written_outside_the_scanned_root`, and D3(a)'s
      exclusion machinery staying dormant until D5 option 2 would make it live.
      **NOT CLAIMED**: *A caller's refinement names the report's own output* —
      the step passes no `--include` and no `--exclude`, so that scenario is
      exercised by R1's fixtures alone; what this slice adds is the assertion
      that the nightly never starts passing one.
      **ADDENDUM, 2026-09-19, realization slice R3 — THE FIRST PRODUCING
      NIGHTLY, WHICH THIS ITEM'S OWN RECORD NAMES AS OWED AND DOES NOT CLAIM.**
      `opensoft/xFactory` `doc-health-nightly` run `35415908738`, event
      `schedule`, started 2026-09-19T02:31:31Z at aggregation commit
      `e7af336fcf0256d21688fe26e341a4781a9f4f50`, uploaded
      `citation-remainder-2026-09-19` — artifact id `10575838648`, 10,682 bytes
      zipped, `retention-days: 90`, expiring 2026-12-18T02:31:31Z. The reading
      step ran to `success` and emitted no `::warning::` on any of its three
      failure paths; the upload step ran to `success` after it. **THE RUN'S
      OVERALL CONCLUSION IS `failure` AND THAT IS NOT A FACT ABOUT THIS
      ARTIFACT**: it died 75 seconds later at *Open regression issue* on
      `GraphQL: Body is too long (maximum is 65536 characters) (createIssue)`
      — openxFactory #1118, a fix in flight — which is exactly the night
      `if: always()` was written for, and the reason this record looks for the
      ARTIFACT rather than for a green run. **AND THE FACT THAT MADE THE NIGHT
      POSSIBLE IS INVISIBLE FROM THE ARTIFACT ALONE**: the aggregation
      initializes its submodules AT THE RECORDED GITLINK and never at the
      submodule's `main`, so the run read the report from
      `89d7975d9e042ae6987131633bc0dd91226ea6f2` only because `opensoft/xFactory`
      PR #467 (merge `d9a0c2b6e4fa82911af443d463cb167e35797bac`,
      2026-09-18T20:19:14Z) moved that gitlink there — a pin-sync in a
      DIFFERENT repository, owed and taken between this item's merge and this
      addendum, and named by no earlier document in this packet. What the
      artifact carries: `head` `89d7975d9e042ae6987131633bc0dd91226ea6f2`,
      `tree_unmodified_at_head: true`, 620 distinct tokens over 2,989 files
      read, INCLUSIVE remainder **86 TOKENS / 57 IDENTITIES**, FILTERED 47 / 30.
      **THIS ADDENDUM DISCHARGES THE HALF THIS ITEM'S OWN RECORD NAMED AS OWED
      AND MOVES NO DECISION OF R2'S**: the tick above still claims the diff and
      not the run, Q6's folded posture and Q2's 90-day measurement stand exactly
      as R2 wrote them, and nothing here re-words them.
- [x] 2.3 **THE FIRST MEASUREMENT THE REPORT ITSELF PRODUCES, AS EVIDENCE.**
      § 1.9's `evidence/measurement-b1df95ee.md` is the HAND-INSTRUMENTED
      reading and it is already committed; what § 2.3 owes is the first reading
      the SHIPPED CLI produces, taken at the realization head and checked
      AGAINST § 1.9's figures at the same commit. **The two must agree or the
      CLI is not the instrument this packet measured with**, and a disagreement
      is a defect in the CLI rather than a new fact about the corpus. It is what
      D6's series starts from.
      **LANDED, 2026-09-19, realization slice R3.**
      `evidence/first-report-89d7975d.md`, NEW, carried by commit `42735d3a` of
      this pull request. **THE READING WAS TAKEN AT THE REALIZATION HEAD**
      `89d7975d9e042ae6987131633bc0dd91226ea6f2` — § 2.2's own merge commit,
      the commit at which both earlier realization slices stand landed and the
      one the aggregation's `openxFactory` gitlink pins — in a dedicated
      detached worktree, `python3 scripts/report-citation-remainder.py . --json`,
      **exit 0**, no refinement passed and `--history` left off because § 2.3
      asks for a reading of a TREE and not of a history. The reading declares
      its own tree state beside its own head: `tree_unmodified_at_head: true`,
      `tree_state: the tracked content read stands UNMODIFIED at this head`,
      which is what makes it a point in D6's series rather than a number.
      **THE FIGURES**: 5,536 tracked entries, 2,993 in scope, 2,989 files read,
      620 distinct tokens, INCLUSIVE remainder **86 TOKENS / 57 IDENTITIES**,
      FILTERED 47 TOKENS / 30 IDENTITIES, `AMBIGUOUS` **0**, classes 5
      `truncated` / 0 `punctuation-stripped` / 19 `fixture-path` / 62
      `unclassified`. Both arithmetic rows close in the report's own output:
      `2,993 = 2,989 + 4 + 0 + 0` and `86 = 47 + 39` remainder entries carrying
      the cross-repository flag, the corpus-wide flagged figure of 83 being the
      larger and different quantity it is printed as.
      **THE REPRODUCTION GATE PASSES ON THE INCLUSIVE READING, FIELD BY
      FIELD**, against § 1.9's hand instrument run over the SAME worktree at
      the SAME commit: tracked entries 5,536, entries in scope 2,993,
      raw-path-absent under choice (2) 165, repaired by the identity rule 79,
      DANGLING identity half 80, file half 6, AMBIGUOUS 0 and the INCLUSIVE
      remainder 86 all agree TO THE TOKEN. **ONE FIGURE-PAIR MOVES AND IT IS
      THE DIVERGENCE R1 ALREADY RECORDED**, re-found here independently at a
      different head and in the same direction: distinct tokens 620 where the
      hand instrument reads 619, and NOT-A-PACKET-REFERENCE 6 where it reads 5,
      for the single token `openspec/changes/archive/..`, which the hand
      instrument folds by stripping a dot off a `..` segment and the report
      refuses to fold. The two token sets were DIFFERENCED rather than
      estimated: that one token is the whole of it, its raw path is present and
      its outcome is NOT-A-PACKET-REFERENCE, so it stands outside the remainder
      population twice over and the remainder is unmoved at 86 either way.
      Nothing else disagrees, so § 2.3's defect clause is not reached.
      **AND THE INSTRUMENT IS PROVED TO BE § 1.9'S OWN, AT § 1.9'S OWN HEAD.**
      Run over a detached worktree at
      `b1df95ee80633339907c9e661164a783885a5d30`, whose
      `scripts/packet_reference.py` is byte-identical to this head's, the
      shipped report reads 572 / 151 / 73 / **78** against the committed
      evidence's published 571 / 151 / 73 / **78** — the same one token apart,
      the remainder identical, 2,973 entries in scope and 2,969 files read as
      R1's record also found. So the movement from 78 there to 86 here is
      CORPUS movement read by one unchanged instrument and not a change of
      instrument.
      **THE HEADLINE DIFFERS FROM D0'S TABLE BY THE THREE FIXED CHOICES, AND
      THIS RECORD SAYS SO BEFORE A REVIEWER ASKS.** Three readings of this one
      tree: `issue-native`, 620 tokens and **86** remainder, which is the
      shipped report because those three choices are what the delta FIXES; the
      prose regex as written with DANGLING + AMBIGUOUS only, 636 and 90, which
      is D0(iv)'s and § 1.1's reading; and `literal`, 636 and 96. Two
      identities re-derived rather than quoted: `636 − 619 = 17` raw spellings
      absorbed by normalize-before-dedup, and `96 − 6 = 90`, the six
      NOT-A-PACKET-REFERENCE tokens the literal reading holds inside its
      remainder. **THE GAP TO WEIGH IS 86 AGAINST 90 AT ONE COMMIT**, not 86
      against the published 82, which was taken at an earlier head; the rest of
      that distance is corpus movement and § 1.9's control already proved the
      methodology is not the variable.
      **AND THE READING WAS TAKEN A SECOND TIME, BY THE NIGHTLY, ON A MACHINE
      NOBODY IN THIS LANE TOUCHED.** Run `35415908738`'s artifact
      `citation-remainder-2026-09-19` (§ 2.2's addendum above) and the local run
      agree in `head`, `tree_unmodified_at_head`, `tree_state`, `reading`,
      `population`, `counts`, `grouping`, `listed` and all 57 listed
      identities; the single field that differs is `root`, the absolute path of
      the checkout each read, which is a fact about where the tree stood and
      not about the tree. D6's series has its first point.
      **WHAT IS NOT COMMITTED, AND WHY IT IS A DECISION.** The `--json` dump and
      the itemized per-identity table are NOT in this pull request; they stand
      in the repository `opensoft/brett-wip` at
      `handoffs/xFactory/attachments/openxfactory-1-2026-09-13/1053/`, cited by
      repository and repo-relative path exactly as § 1.9 cites its own 1.5 MB
      dump. This packet's `evidence/` directory is INSIDE the scanned
      population and the itemized table writes one citation token per remainder
      line, so committing it would be the largest single act of self-counting
      this packet could perform — the mechanism D5 exists to refuse — and it
      would FIRE the delta's own *The report's own output is committed into the
      corpus* antecedent, whose THENs pull the output-path exclusion into a
      slice the realization plan sized as documents. **THIS IS THAT PLAN'S Q3
      RECOMMENDATION, TAKEN UNDER THE AUTHORIZATION IT GIVES R3's AUTHOR, WITH
      CONFIRMATION OUTSTANDING.**
      **AND THE COMMITTED NOTE MINTS NO REMAINDER OF ITS OWN**, which is the
      acceptance check this packet uniquely owes, taken in two clean detached
      worktrees rather than by restoring a dirty tree: at this branch's merge
      base `b0329d65` and at its head, 619 distinct tokens, 86 inclusive, 57
      identities and 47 filtered on BOTH sides; only FILES read moves, 2,978 to
      2,979, by the one file this slice adds, which is the whole claim. Δ = 0.
      **THE FIGURES ARE PINNED TO THE RUN THAT PRODUCED THEM**, because they
      are a reading of a MOVING corpus and not a property of this packet.
- [x] 2.4 **THE REALIZATION EVIDENCE IS GREEN BEFORE IT IS CLAIMED.** The
      realization pull request merged into `main`, and a `pytest-suite` run at
      the tree that merge carries GREEN. That pair is what § 3.4 archives on
      and nothing less is read as realization.
      **DISCHARGED — THE PAIR IS MERGED AND IT IS GREEN, AND BOTH HALVES ARE
      CITED BY NAME RATHER THAN INFERRED.**
      **MERGED.** The realization landed as four pull requests, each by number and
      merge sha: R1, the report CLI and its tests, PR
      [#1100](https://github.com/opensoft/openxFactory/pull/1100) →
      `83166366d499d58b5e8801e0bb17e346c73fc8e6`, merged 2026-09-18T15:22:14Z on Brett
      Heap's word **"land it when green"** ([#1100 comment
      5728210143](https://github.com/opensoft/openxFactory/pull/1100#issuecomment-5728210143));
      R2, the nightly wiring, PR
      [#1111](https://github.com/opensoft/openxFactory/pull/1111) →
      `89d7975d9e042ae6987131633bc0dd91226ea6f2`, merged 2026-09-18T20:03:40Z on **"land
      #1111 when green"** ([#1111 comment
      5735511925](https://github.com/opensoft/openxFactory/pull/1111#issuecomment-5735511925));
      the aggregation pin-sync that makes the wired step run the shipped script rather
      than a stale gitlink, opensoft/xFactory PR
      [#467](https://github.com/opensoft/xFactory/pull/467) →
      `d9a0c2b6e4fa82911af443d463cb167e35797bac`, merged 2026-09-18T20:19:14Z; and R3,
      the first committed reading, PR
      [#1126](https://github.com/opensoft/openxFactory/pull/1126) →
      `93a5ce2b50924e0bda75ab94b2b42e1339c7b8da`, merged 2026-09-21T20:25:03Z on **"land
      #1126 when green"** ([#1126 comment
      5766996007](https://github.com/opensoft/openxFactory/pull/1126#issuecomment-5766996007)).
      **GREEN — AND THE RUN CITED IS NOT THE ONE THIS BOX WOULD FIRST HAVE REACHED
      FOR, WHICH IS RECORDED RATHER THAN QUIETLY SUBSTITUTED.** The `pytest-suite` run
      started on R3's own merge commit `93a5ce2b` — run
      [35650930794](https://github.com/opensoft/openxFactory/actions/runs/35650930794),
      queued 2026-09-21T20:25:06Z — **was CANCELLED at 2026-09-21T20:34:12Z, and by
      the workflow's own concurrency group rather than by any person**: PR #1121 merged
      into `main` at 20:33:37Z and superseded it. A cancelled run is not a green run,
      so this box does not cite it. **THE RUN THIS BOX CITES IS
      [35651829217](https://github.com/opensoft/openxFactory/actions/runs/35651829217)**,
      `pytest-suite` on `main` commit
      `80c68da6081282225b54cfdb06b99bc93129d3cf` — the NEXT commit on `main` after
      R3's merge, and one that carries `93a5ce2b` as an ancestor (`git merge-base
      --is-ancestor 93a5ce2b 80c68da6` → true), so it is a green run at a tree the
      realization merge is IN. Conclusion **`success`**, started 2026-09-21T20:34:15Z
      and completed 2026-09-21T20:56:31Z. **THE RUN'S OWN COUNTS LINE, IN ITS OWN
      WORDS**: `selected=8697 passed=8691 skipped=6 failures=0 errors=0`, over
      `8287 passed, 6 skipped, 338 deselected, 9 warnings, 404 subtests passed in
      1302.37s (0:21:42)`.
      **BOTH READINGS ARE STATED, THE MERGE BASE AND THE MERGE, SO THE DELTA IS
      VISIBLE AND SO IT IS NOT MIS-ATTRIBUTED.** At R3's merge base `b0329d65` the
      decided `pytest-suite` was run
      [35415554303](https://github.com/opensoft/openxFactory/actions/runs/35415554303),
      `success`, `selected=8686 passed=8680 skipped=6 failures=0 errors=0`. The
      delta is **+11 selected, +11 passed, 0 failures either side** — and it is NOT
      this packet's: R3 added no test module, and the only test file added anywhere
      in `b0329d65..80c68da6` is `tests/doc-health/test_regression_issue_body_cap.py`
      (+228 lines), which belongs to the intervening PR #1121. The tests R1 added
      entered the suite at R1's own merge, long before either reading here.
      **AND A SECOND, INDEPENDENT PROOF IS CITED, BECAUSE THE FIRST ONE READS AT A
      LATER COMMIT THAN THE MERGE.** #1126's own pre-merge run,
      [35418896466](https://github.com/opensoft/openxFactory/actions/runs/35418896466),
      `pytest-suite` on `ef2baffbd3bc5a7deb2fdfa17a800c3cb718e4d5`, conclusion
      `success`, `selected=8686 passed=8680 skipped=6 failures=0 errors=0` — and that
      head is **TREE-IDENTICAL to the merge commit `93a5ce2b`**, measured rather than
      assumed: `git rev-parse ef2baffb^{tree} 93a5ce2b^{tree}` returns the same object
      `63f22e16dfee4fac809fcd300aecb3ad485f9f49` on both sides. So a green
      `pytest-suite` ran over the exact tree R3's merge carries, which is the
      house fallback `add-declared-former-id`'s own archive used for two of its four
      merges, and it is cited here beside the `main` run rather than instead of it.
      **THAT IS THE MERGED-PLUS-GREEN PAIR § 3.4 ARCHIVES ON**, and nothing less was
      read as realization.

## 3. Records, and the archive

- [x] 3.1 **THE SWEEP-LEDGER ROW IS RE-SEEDED WITH THE REAL PULL REQUEST
      NUMBER — DONE AT OPEN, `moved_by: "#1069"`.** The row seeded in § 1.6
      carried the GOVERNING ISSUE `#1053`, because this packet was authored by
      a writer that opens no pull request and invents no number, and the field's
      grammar (`^#[0-9]+$`) admits no `#TBD-…` spelling to mark the gap with.
      The pull request is [#1069](https://github.com/opensoft/openxFactory/pull/1069)
      and the row now names it. **AND THE RECIPE THIS ITEM ORIGINALLY GAVE DOES
      NOT WORK, WHICH IS WORTH RECORDING RATHER THAN QUIETLY REPLACING**: a bare
      `--seed-ledger --moved-by '#1069'` stamps only the rows that MOVED, and a
      row already present and already agreeing with the live corpus has not
      moved — the run reports `217 rows, 0 moved by #1069` and writes no diff.
      The row must therefore be REMOVED from the ledger first, so the seeder
      re-derives it as a move and stamps it:
      `python3 - <<< "remove the one row"` then
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#1069'`
      → `wrote tests/sequenced_after/corpus-ledger.yaml (217 rows, 1 moved by
      #1069)`, a ONE-LINE diff changing `moved_by` alone, and
      `--ledger-diff` → `per-change sweep ledger consistent with the corpus (217
      rows)`, exit 0. **NO VALUE IS HAND-WRITTEN**: the machine re-derives every
      field of the row, which is what the house rule against hand-editing the
      ledger protects. The ledger's own contract makes this a pointer rather
      than evidence — the field is author-supplied, shape-checked only, and
      *"a pointer for a human reading the history, not evidence"* — but an issue
      number left standing where a pull request number belongs points a reader
      at the commission rather than at the act.
- [x] 3.2 **#1053 IS COMMENTED ON AT RATIFICATION**, naming the word, its
      timestamp, and which of D1 through D7 it took or vetoed. The issue is
      NOT closed there.
      **DONE — THE COMMENT IS POSTED AND THIS BOX TICKS ON IT.** openxFactory
      [#1053, comment
      5714153263](https://github.com/opensoft/openxFactory/issues/1053#issuecomment-5714153263),
      2026-09-17T12:13:24Z. It names the word (**"ratify #1069"**), its timestamp
      (2026-09-17T12:12:06Z), where the word itself is recorded (PR #1069 comment
      5714138459), and what it took: *"ratified with D1–D7 at their recommended
      options — option (b) of this issue: a `packet_reference` report CLI run nightly
      outside doc-health, with the twenty-fourth doc-health family sequenced as the
      later step"*, naming no veto. **AND THE ISSUE WAS NOT CLOSED THERE**, which is
      the second half of what this box requires: #1053 was open at that comment, has
      been open at every act since, and is open at this archive.
- [x] 3.3 **#1053 IS COMMENTED ON AT REALIZATION**, naming the realization pull
      request, its merge sha, and the first report the nightly produced.
      **DONE — THE REALIZATION IS RECORDED ON #1053 IN FOUR COMMENTS, ONE PER
      LANDING, AND THE LAST OF THEM CARRIES THE WHOLE CHAIN.** R1: [comment
      5732160060](https://github.com/opensoft/openxFactory/issues/1053#issuecomment-5732160060),
      2026-09-18, PR #1100 → `83166366`. R2: [comment
      5735536261](https://github.com/opensoft/openxFactory/issues/1053#issuecomment-5735536261),
      2026-09-18, PR #1111 → `89d7975d`. The aggregation pin-sync beside it: [comment
      5735700537](https://github.com/opensoft/openxFactory/issues/1053#issuecomment-5735700537),
      opensoft/xFactory#467 → `d9a0c2b6`. R3: [comment
      5767019747](https://github.com/opensoft/openxFactory/issues/1053#issuecomment-5767019747),
      2026-09-21, PR #1126 → `93a5ce2b`, which names all four merge shas together and
      carries the third thing this box asks for — **THE FIRST REPORT THE NIGHTLY
      PRODUCED**, `opensoft/xFactory` `doc-health-nightly` run 35415908738, artifact
      `citation-remainder-2026-09-19`, in its own words: *"§ 2.2 carrying the addendum
      that names the first producing nightly (run 35415908738, artifact
      `citation-remainder-2026-09-19`)"*, and *"the nightly has since produced three
      consecutive artifacts (09-19, 09-20, 09-21)"*. A merged workflow file is not
      evidence that a step ran; that run id and that artifact name are.
      **WHICH READING OF THIS BOX IS TAKEN IS STATED RATHER THAN LEFT TO A READER.**
      The box names the three facts in the singular — *"the realization pull request,
      its merge sha, and the first report the nightly produced"* — and the realization
      was FOUR landings rather than one, so no single comment could name it in that
      grammar. This tick is taken against **the four comments named above, read
      together**, which the tick rule's own first clause admits: a `[x]` is *"a
      measurement recorded verbatim … and reproducible from the command named beside
      it"*, and four comment URLs are as reproducible as one. The alternative — posting
      one fresh consolidated comment on #1053 and ticking against that — is equally
      lawful and was NOT taken here, because posting to #1053 is the orchestrator's
      act and not this writer's, which `brief-R3-ticks.md` had already ruled for
      this same box (*"NOT YOURS TO POST"*). If a single consolidated comment is
      wanted, it costs one comment and no re-tick.
- [x] 3.4 **THE ARCHIVE IS A SEPARATE ACT ON A SEPARATE WORD AND IT IS NOT
      PERFORMED HERE.** `code_surface` is NON-EMPTY, so under
      `release-realization` — *Realization archive gate* — this packet SHALL
      NOT archive on landing and SHALL NOT archive on ratification. **THIS
      PACKET'S OWN WORD ON ITS OWN ARCHIVE, WRITTEN HERE SO NO LATER READER HAS
      TO INFER IT: it archives only when § 2's realization pull request has
      MERGED into `main` AND a `pytest-suite` run at the tree that merge
      carries is GREEN — merged-plus-green at canon's grain — and not before.**
      The archive act moves the packet to
      `openspec/changes/archive/<YYYY-MM-DD>-add-citation-remainder-report/`
      through `python3 scripts/proposal-support.py . archive`, re-seeds the
      ledger row to `state: archived`, and takes its own word.
      **TAKEN — AND THE TASK TEXT ABOVE IS THE FILING PULL REQUEST'S OWN
      RECORD OF 2026-09-16, WHICH WAS TRUE THEN AND IS KEPT AS HISTORY.** The separate
      word this box holds the archive for is Brett Heap's, given 2026-09-21T20:28Z
      first-hand in session to lane `openxfactory-1`, verbatim **"archive it"** —
      recorded at openxFactory [#1053, comment
      5767056479](https://github.com/opensoft/openxFactory/issues/1053#issuecomment-5767056479).
      The merged-plus-green condition this box states in its own words — *"§ 2's
      realization pull request has MERGED into `main` AND a `pytest-suite` run at the
      tree that merge carries is GREEN"* — is discharged and cited at § 2.4 above, and
      the archive was not opened before it held.
      **PERFORMED BY `python3 scripts/proposal-support.py . archive
      add-citation-remainder-report --yes`** — NEVER bare `openspec` — which printed
      **`ORIGIN RETAINED add-citation-remainder-report (declaration unchanged since
      the ratifying commit 96f66fe9f148)`** and moved the packet to
      `openspec/changes/archive/2026-09-21-add-citation-remainder-report/`. The
      wrapper owns the clock and named that date from its own UTC reading; the commit
      carrying this tick is the archive act that name states, which is what
      `scripts/validate-sequenced-after.py`'s `archive-date-vs-commit` arm measures.
      **THE LEDGER ROW IS RE-SEEDED BY THE MACHINE AND NOT BY HAND**, `active` →
      `archived`, the way § 3.1 above records the recipe: the row is removed from
      `tests/sequenced_after/corpus-ledger.yaml` first, because a bare re-seed stamps
      only rows that MOVED, then
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
      '#<this archive pull request>'` re-derives every field of it from the corpus,
      and `--ledger-diff` reads consistent.
      **AND THE PROMOTION THIS BOX DOES NOT SPELL IS PERFORMED HERE TOO**, because
      canon does spell it: the five `## ADDED` requirements and their 72 scenarios
      reach `openspec/specs/packet-citation-report/spec.md`, a capability directory
      that did not exist in canon before this act.
- [x] 3.5 **openxFactory #1053 CLOSES AT THE ARCHIVE AND NOWHERE EARLIER**, by
      a closing keyword written in the ARCHIVE pull request — never in a commit
      message on this branch and never in the ratification comment.
      **THE MOMENT THIS BOX PROTECTS IS UNMOVED AND THE INSTRUMENT IS
      AMENDED, ON A MEASURED HAZARD RATHER THAN ON A PREFERENCE.** #1053 closes on
      this archive and on nothing earlier — which is what this box is for, and which
      every pull request on this packet honoured: the filing #1069, the fold-in #1097,
      and the four realization landings #1100, #1111, opensoft/xFactory#467 and #1126
      each carry `Refs #1053.` and no closing keyword, and no commit message on any
      branch of this work carries one either.
      **WHAT CHANGES IS THE INSTRUMENT.** This box names *"a closing keyword written
      in the ARCHIVE pull request"*; the archive pull request carries `Refs #1053.`
      instead, and the lane SHUTS #1053 by hand in a separate act immediately after
      the ARCHIVED record. The reason is measured on this packet's own history rather
      than argued: GitHub parses a keyword-then-number pair wherever it stands,
      INCLUDING inside a sentence saying the pull request does not close the issue,
      and a sentence of exactly that shape in PR #1100's body — a realization slice
      with no business closing anything — linked #1100 as the pull request that would
      shut #1053. A keyword in the archive body would re-open the same hazard for the
      sake of saving one deliberate act.
      **AND IT IS THE FORM THE ESTATE'S MOST RECENT CODE-SURFACE ARCHIVE TOOK**, PR
      [#1114](https://github.com/opensoft/openxFactory/pull/1114) → `cd6439f6`, whose
      body reads: *"openxFactory #1045 closes by the lane's hand after the ARCHIVED
      record, not by a keyword"*, and whose `closingIssuesReferences` is `[]`.

## 4. Residue — named here, taken nowhere

- [x] 4.1 **NOT TAKEN — THE TWENTY-FOURTH DOC-HEALTH FAMILY.** D1 option (a),
      sized in `design.md` D1 to four items so the successor does not re-derive
      the cost. Its trigger is D6's three-part condition; filing it is a
      separate act with its own sibling search, and this packet does not file
      it.
      **STILL NOT TAKEN AT THE ARCHIVE — RECORDED, NEVER DONE, AND RE-READ
      HERE RATHER THAN RESTATED FROM THE FILING.** No twenty-fourth doc-health family
      is filed by this packet or by any of its four realization landings:
      `scripts/doc_health/` is byte-unmoved across the whole realization (D7 fence 4,
      § 1.16 above), `openspec/specs/doc-health/spec.md` carries the same *"twenty-three
      check families"* enumeration it carried at filing, and `scripts/doc_health/families.py`
      still registers twenty-three. **AND ITS TRIGGER IS NOT MERELY UNMET, IT IS NOT
      YET MEASURABLE**: D6's three-part condition runs over `N = 14` consecutive
      nightly runs and the series is THREE runs old at this archive (2026-09-19,
      2026-09-20, 2026-09-21). Filing the successor is a separate act with its own
      sibling search and its own word; no issue is filed here, and this packet is the
      population measurement doc-health's own advisory-launch rule says that severity
      decision must FOLLOW.
- [x] 4.2 **NOT TAKEN — A CROSS-REPOSITORY SWEEP.** OpsxFactory's,
      LedgerxFactory's, AdxFactory's and codexFactory's own corpora each need
      their own reading, in their own repository, by whoever owns it.
      `packet_reference.py` states why this tree cannot do it: it *"holds NO
      repository vocabulary and NO module-level root"*, so *"the same reference
      answers differently against two roots"*. No issue is filed here.
      **STILL NOT TAKEN, AND THE ARCHIVE TAKES IT NO FURTHER.** No
      cross-repository sweep was performed by any realization slice and none is filed
      here; no issue is opened in OpsxFactory, LedgerxFactory, AdxFactory or
      codexFactory by this packet. **WHAT SHIPPED INSTEAD IS THE SUSPICION D3
      RECOMMENDS**: the report FLAGS `possibly-cross-repo` and resolves nothing, on
      the reason `scripts/packet_reference.py` states about itself and which this
      archive re-read rather than quoted from memory — it holds no repository
      vocabulary and no module-level root, so the same reference answers differently
      against two roots. The first committed reading prints the filtered count beside
      the inclusive one (47 / 30 beside 86 / 57 at `89d7975d`) rather than in place of
      it, which is that suspicion made auditable instead of acted on.
- [x] 4.3 **NOT TAKEN — REPAIRING ONE CITATION.** All 81 are characterized and
      none is repaired, which is `add-declared-former-id` D4's posture
      inherited deliberately. Several are dangling BY THEIR OWN FILE'S DESIGN
      (scope-isolation fixtures, docstring examples) and repairing them would
      break the file.
      **STILL NOT TAKEN — AND MEASURED AGAIN AT THE SHIPPED READING RATHER
      THAN ASSERTED FROM THE FILING.** Not one citation is repaired by this packet or
      by any of its four realization landings. The figure this box states was 81
      inclusive tokens at the packet's own re-measurement at `b1df95ee`; the shipped
      report's first committed reading at `89d7975d` reads 86 tokens over 57
      identities — **the corpus moved and the posture did not**, which is the whole
      point of a report that gates nothing. The refusal is instrumented rather than
      promised: `scripts/report-citation-remainder.py` proposes no spelling for any
      dangling entry and writes no file it read, pinned by
      `test_a_dangling_citation_names_its_half_identity_and_citing_files_and_proposes_no_spelling`
      and `test_the_report_writes_no_file_it_read`. Several of the remainder are
      dangling BY THEIR OWN FILE'S DESIGN and repairing them would break the file,
      which is why the tool is a reader.
- [x] 4.4 **NOT TAKEN — THE RESOLVER DOCSTRING'S OWN STALE EXAMPLE.**
      `scripts/packet_reference.py` offers `openspec/changes/README.md` as its
      canonical `NOT_A_PACKET_REFERENCE` case and that file does not exist in
      this tree, so the example resolves DANGLING(identity-half) — measured in
      `design.md` D0(iii). Correcting a ratified packet's shipped docstring is
      an edit to somebody else's record and is exactly the repair D4 refuses to
      make from a report. Recorded so a reader finds the question rather than
      rediscovering it.
      **STILL NOT TAKEN — AND RE-READ IN THIS ARCHIVE'S OWN TREE TO CONFIRM
      IT IS STILL TRUE RATHER THAN CARRIED FORWARD ON TRUST.** `scripts/packet_reference.py`
      still offers `openspec/changes/README.md` as its canonical
      `NOT_A_PACKET_REFERENCE` example (`:50` and `:605`); that file still does not
      exist in this tree, measured at this head; and the docstring is unedited by the
      realization, D7 fence 1 having read an empty `git diff` over that file at every
      one of the four landings. So the example still resolves DANGLING(identity-half),
      and correcting it would be an edit to somebody else's ratified record made from
      a report — exactly the repair D4 refuses. Recorded so a reader finds the
      question rather than rediscovering it.
