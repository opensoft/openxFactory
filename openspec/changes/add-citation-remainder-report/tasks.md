# Tasks: add-citation-remainder-report

Status: draft
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
and every one of them is EMPTY:

```text
$ git diff origin/main..HEAD -- scripts/packet_reference.py | wc -l
0
$ git diff origin/main..HEAD -- scripts/validate-pin-registrations.py | wc -l
0
$ git diff origin/main..HEAD -- scripts/doc_health | wc -l
0
$ git diff origin/main..HEAD -- openspec/specs | wc -l
0
$ git diff origin/main..HEAD -- .github/workflows | wc -l
0
$ git diff --name-only origin/main..HEAD
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
commissions the CLAIM and decides no wording. Every document carries
`Status: draft`.

**§ 2 (REALIZATION) IS ENTIRELY OPEN.** **§ 3 (RECORDS AND ARCHIVE) IS ENTIRELY
OPEN.**

## 1. The packet, and the ratification word it is held for

### What landed in this pull request

- [x] 1.1 **THE CORPUS WAS RE-MEASURED, NOT QUOTED.** Fresh clone at
      `origin/main` `b1df95ee80633339907c9e661164a783885a5d30`; #1053's own
      recipe re-run through the LANDED `packet_reference.resolve()`: **5,466**
      tracked files, **2,973** in scope, **586** distinct
      `openspec/changes/…` tokens, **498** `RESOLVED` (**76** relocated),
      **74** `DANGLING`(identity-half), **7** `DANGLING`(file-half), **0**
      `AMBIGUOUS`, **7** `NOT_A_PACKET_REFERENCE` — **inclusive remainder 81
      tokens**, carried by **65** distinct citing files. `design.md` D0 carries
      the table and the commands. **AND THE SAME RECIPE WAS RE-RUN ON THIS
      BRANCH, AFTER THE PACKET EXISTED**: 2,979 files in scope, 594 tokens, 504
      RESOLVED, **remainder 82 — UP BY ONE**, and the one is
      `openspec/changes/foo/`, minted by the COMMITTED EVIDENCE REPORT's own
      enumeration of the resolver's docstring examples and then carried by this
      packet's own paragraphs about it too. `design.md` D0(iv)
      carries all five readings, each at the commit it was taken at. **That is D5's argument stopping being a
      prediction**: one report, committed once, +1 remainder.
- [x] 1.2 **THREE FACTS #1053 DOES NOT CARRY WERE FOUND AND EACH MOVED A
      DECISION.** (i) the 74 identity-half tokens collapse to **48 DISTINCT
      IDENTITIES**, 18 identities cited more than once — which is why D3
      requires both counts; (ii) the token grammar manufactures remainder in
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
      house form the neighbouring bullets use, marked **DRAFT and HELD**.
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
      classification JSON are NOT committed and are cited by their path in this
      lane's handoff attachments: a packet needs the reading, not the dump.

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
      (`validate-pin-registrations.py`) imports it. Exit code **always 0** and
      **no `--fail-on`**, which is reserved for D1 option (a).
- [ ] 1.12 **`design.md` D3 — THE RECIPE.** RECOMMENDED: the stated file
      population (three exclusions, each with a reason, plus the report's own
      output path the moment D5 ever changes), the stated token grammar with
      its four normalizations PRINTED rather than hidden, and — the decision
      that matters — a suspected cross-repository citation **FLAGGED
      `possibly-cross-repo` and left IN the count**. Against dropping it
      silently (cost: an unauditable window sets the headline number); against
      counting it unflagged (cost: the largest known class hides inside a
      number that reads as a defect count).
- [ ] 1.13 **`design.md` D4 — THE CLASSES.** RECOMMENDED: four MECHANICAL
      classes (`possibly-cross-repo`, `truncated`, `punctuation-stripped`,
      `fixture-path`) and an honest `unclassified` for the five that need a
      reading of INTENT. Against mechanizing all nine (cost: a machine
      asserting "never existed" from a `git log` miss puts a wrong guess into
      D6's series); against classifying nothing (cost: hands the reader the
      list they already have). **And the rule that governs all nine: NOTHING IS
      REPAIRED** — a dangling reference owes the citing record no edit from
      this tool, which is the other half of the sentence
      `add-declared-former-id` D4 wrote.
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
- [ ] 1.17 **THE RATIFICATION RECORD IS CUT WHEN THE WORD IS GIVEN**, and not
      before: `.openspec.yaml` gains `approved_by` and `approved_on` as a pure
      ADDITION beside a byte-unmoved drafting provenance (`kind` and `id` never
      move — the shape `add-drafted-proposal-origin` defined), and
      `proposal.md`, `design.md` and this file flip to `Status: ratified` with
      ONE citation each, the ruling comment URL. **THE FLIP IS NOT
      HEADER-ONLY**: the draft-voiced prose in all three moves with it.

## 2. Realization — A LATER PULL REQUEST, ON A LATER WORD

**NONE OF § 2 IS IN THIS PULL REQUEST.** No script, no workflow and no test is
added, edited, renamed or deleted here.

- [ ] 2.1 **THE REPORT CLI AND ITS UNIT TESTS.**
      `scripts/report-citation-remainder.py` (NEW), importing
      `scripts/packet_reference.py` UNCHANGED: under D2's recommended option 1
      its docstring sentence *"Run: this module is a library and has no CLI"*
      stays true and no line of that module moves. The one-line docstring
      correction is owed ONLY if D2 is vetoed for option 2.
      Argument surface exactly as D2 fixes it (`[REPO_ROOT] [--json] [--all]
      [--tokens] [--history] [--include] [--exclude]` — grouping is by IDENTITY
      by default and `--tokens` ungroups it; `--history` is OPT-IN on D2's
      measured cost), exit code always 0, no `--fail-on`. `tests/citation_remainder/` (NEW): unit tests over a
      THROWAWAY FIXTURE CORPUS built in a `tmp_path` git tree — the shape
      `add-declared-former-id` used for `tests/packet_reference/`, so the tests
      assert against a corpus they construct rather than against the live one,
      which moves under them. Fixtures must cover, at minimum: each of the four
      normalizations; a cross-repository qualifier at each of the four
      adjacency positions AND one three lines above; an identity cited by two
      tokens; a file-half dangler; a deliberately-absent scope-isolation
      fixture; and the `README.md`-shaped case where the raw path's presence
      decides the outcome.
- [ ] 2.2 **THE NIGHTLY WIRING**, at the size D5 rules. Under the recommended
      option: ONE step in `.github/workflows/doc-health-reusable.yml` that runs
      the report and uploads it as a workflow artifact, committing nothing,
      adding no branch and asking no write permission. Under D5 option 2 it is
      instead a date-partitioned commit-back on a lane-owned branch in the
      derive-possibles shape, and D3(a)'s output-path exclusion becomes LIVE
      rather than structural and MUST land in the same pull request.
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

- [ ] 3.1 **THE SWEEP-LEDGER ROW IS RE-SEEDED WITH THE REAL PULL REQUEST
      NUMBER AT OPEN.** The row seeded in § 1.6 carries the GOVERNING ISSUE
      `#1053` in `moved_by`, because this packet was authored by a writer that
      opens no pull request and invents no number, and the field's grammar
      (`^#[0-9]+$`) admits no `#TBD-…` spelling to mark the gap with. **Whoever opens the pull request runs
      `python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
      '#<the real PR>'` and commits the one-line diff.** The ledger's own
      contract makes this safe rather than urgent — the field is
      author-supplied, shape-checked only, and *"a pointer for a human reading
      the history, not evidence"* — but an issue number left standing where a
      pull request number belongs points a reader at the commission rather than
      at the act.
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
