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

- [ ] 1.10 **`design.md` D1 — THE HOME OF THE REPORT.** RECOMMENDED: **(b)** a
      report CLI outside doc-health, which is #1053's own recommendation.
      Against **(a)** a twenty-fourth doc-health family NOW — cost: a
      `## MODIFIED` block restating the whole twenty-three-family enumeration,
      a `families.py` registry edit, a numeral, and a severity decision canon
      says must FOLLOW a population measurement; against **(c)** nothing —
      cost: the posture that let #840's dangling `cited_to` citations go
      unnoticed, now measured at 81 tokens nobody looks at.
- [ ] 1.11 **`design.md` D2 — THE SURFACE.** RECOMMENDED: a sibling
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
- [ ] 1.12 **`design.md` D3 — THE RECIPE.** RECOMMENDED: the stated file
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
- [ ] 1.13 **`design.md` D4 — THE CLASSES.** RECOMMENDED: the classes the report
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
- [ ] 1.14 **`design.md` D5 — THE NIGHTLY WIRING.** RECOMMENDED: **artifact-only**,
      one step in `.github/workflows/doc-health-reusable.yml`, committing
      nothing. The reason is measured and is not merely merge conflicts:
      `health/` is INSIDE the file population and carries **0** citation tokens
      today, so a committed report would be the first file there to carry them
      — one per remainder line — and the next run would count its own output.
      Against a date-partitioned commit-back on a lane branch (the
      derive-possibles shape; named as the promotion step, its real advantage
      being that D6's series is then read with one `git log`); against a
      committed rolling `health/citation-remainder.md`, **REFUSED BY NAME**.
- [ ] 1.15 **`design.md` D6 — WHAT "STABLE" MEANS** before option (a) becomes
      takeable: three conditions on the nightly series over `N = 14` runs —
      `unclassified` identities not growing; at most **3** new remainder
      identities, each attributable to a named pull request; the mechanical
      classes at zero net growth. **`N = 14` and the 3 are proposed numbers and
      are the most vetoable figures in this packet.** Against "the count is
      unchanged" (cost: unmeetable — the count moves on every archive) and
      against no condition at all (cost: "later" becomes "never").
- [ ] 1.16 **`design.md` D7 — THE SCOPE FENCES.** RECOMMENDED: four, each named
      with the file it protects — no citation edited anywhere by anything; no
      cross-repository reference resolved (only suspected);
      `scripts/validate-pin-registrations.py`'s `check_citations` untouched by
      name; no file under `scripts/doc_health/` or
      `openspec/specs/doc-health/spec.md` moved.
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
      **LANDED, 2026-09-17, realization slice R1.**
      `scripts/report-citation-remainder.py` (NEW, 1,580 lines) and
      `tests/citation_remainder/test_report_citation_remainder.py` (NEW, 1,852
      lines, 96 tests, all green). ONE TEST PER SCENARIO, its docstring naming
      the scenario verbatim: 63 of 63 across the five requirements, counted
      mechanically against `specs/packet-citation-report/spec.md` rather than
      by hand. `scripts/packet_reference.py` is imported UNCHANGED and the D7
      fences are each empty.
      **AND THE INSTRUMENT IS THE ONE THIS PACKET MEASURED WITH, PROVED AT
      `b1df95ee` RATHER THAN ASSERTED.** Run against a worktree at
      `b1df95ee80633339907c9e661164a783885a5d30`, the shipped CLI reproduces
      `evidence/measurement-b1df95ee.md`'s § 2.1 reading to the token: 2,973
      tracked entries in scope, 2,969 files read, 571 distinct tokens, 151
      raw-path-absent holding NOT-A-PACKET-REFERENCE out, 73 repaired by the
      identity rule, INCLUSIVE remainder 78 — 72 identity half, 6 file half, 0
      AMBIGUOUS — and 4 NOT-A-PACKET-REFERENCE. It is the NORMALIZED
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
      block reads identically at this branch's merge base and at its head — 602
      distinct tokens, 154 raw-path-absent, 81 inclusive remainder on both
      sides. Δ = 0.
- [ ] 2.2 **THE NIGHTLY WIRING**, at the size D5 rules. Under the recommended
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
- [ ] 2.3 **THE FIRST MEASUREMENT THE REPORT ITSELF PRODUCES, AS EVIDENCE.**
      § 1.9's `evidence/measurement-b1df95ee.md` is the HAND-INSTRUMENTED
      reading and it is already committed; what § 2.3 owes is the first reading
      the SHIPPED CLI produces, taken at the realization head and checked
      AGAINST § 1.9's figures at the same commit. **The two must agree or the
      CLI is not the instrument this packet measured with**, and a disagreement
      is a defect in the CLI rather than a new fact about the corpus. It is what
      D6's series starts from.
- [ ] 2.4 **THE REALIZATION EVIDENCE IS GREEN BEFORE IT IS CLAIMED.** The
      realization pull request merged into `main`, and a `pytest-suite` run at
      the tree that merge carries GREEN. That pair is what § 3.4 archives on
      and nothing less is read as realization.

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
- [ ] 3.2 **#1053 IS COMMENTED ON AT RATIFICATION**, naming the word, its
      timestamp, and which of D1 through D7 it took or vetoed. The issue is
      NOT closed there.
- [ ] 3.3 **#1053 IS COMMENTED ON AT REALIZATION**, naming the realization pull
      request, its merge sha, and the first report the nightly produced.
- [ ] 3.4 **THE ARCHIVE IS A SEPARATE ACT ON A SEPARATE WORD AND IT IS NOT
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
- [ ] 3.5 **openxFactory #1053 CLOSES AT THE ARCHIVE AND NOWHERE EARLIER**, by
      a closing keyword written in the ARCHIVE pull request — never in a commit
      message on this branch and never in the ratification comment.

## 4. Residue — named here, taken nowhere

- [ ] 4.1 **NOT TAKEN — THE TWENTY-FOURTH DOC-HEALTH FAMILY.** D1 option (a),
      sized in `design.md` D1 to four items so the successor does not re-derive
      the cost. Its trigger is D6's three-part condition; filing it is a
      separate act with its own sibling search, and this packet does not file
      it.
- [ ] 4.2 **NOT TAKEN — A CROSS-REPOSITORY SWEEP.** OpsxFactory's,
      LedgerxFactory's, AdxFactory's and codexFactory's own corpora each need
      their own reading, in their own repository, by whoever owns it.
      `packet_reference.py` states why this tree cannot do it: it *"holds NO
      repository vocabulary and NO module-level root"*, so *"the same reference
      answers differently against two roots"*. No issue is filed here.
- [ ] 4.3 **NOT TAKEN — REPAIRING ONE CITATION.** All 81 are characterized and
      none is repaired, which is `add-declared-former-id` D4's posture
      inherited deliberately. Several are dangling BY THEIR OWN FILE'S DESIGN
      (scope-isolation fixtures, docstring examples) and repairing them would
      break the file.
- [ ] 4.4 **NOT TAKEN — THE RESOLVER DOCSTRING'S OWN STALE EXAMPLE.**
      `scripts/packet_reference.py` offers `openspec/changes/README.md` as its
      canonical `NOT_A_PACKET_REFERENCE` case and that file does not exist in
      this tree, so the example resolves DANGLING(identity-half) — measured in
      `design.md` D0(iii). Correcting a ratified packet's shipped docstring is
      an edit to somebody else's record and is exactly the repair D4 refuses to
      make from a report. Recorded so a reader finds the question rather than
      rediscovering it.
