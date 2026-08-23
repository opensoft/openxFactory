# Tasks: govern-openspec-corpus-membership

**§1 is COMPLETE — ratified 2026-08-23.** Nothing below §1 could start before
it: this change proposes a measurement rule and a scope boundary, and until
the six open questions were ruled there was no way to know which of three
options the code implements. The ruling is recorded question by question in
`proposal.md` § Open Questions; the six read-backs are in §1.1 below.

The ordering constraint that is easy to get wrong: **§5 discharges all 68
standing violations, and §2's landing commit MUST NOT merge before §5
reaches zero.** A gate that goes red on the commit that introduces it teaches
everyone to route around the gate. The 2026-08-23 ruling made this constraint
stricter, not looser: the draft allowed "complete OR explicitly
dispositioned", and with the grandfather refused there is nothing left to
disposition — §5 is discharge or nothing.

## 1. Ratification (Brett)

- [x] 1.1 Brett read `proposal.md` — the measurement section especially,
      since the recommendation rested on numbers rather than on principle —
      and ruled OQ-1 through OQ-6 in one in-session multiple-choice round on
      2026-08-23. Read-backs, in the order ruled:
      - **OQ-1 → (b), the scoped lifecycle scan set.** As recommended, but
        not as first leaned: Brett's opening position was (a) full
        membership, and the measured costs — the 121-of-123 `duplicate
        inventory key` collision, the 12.2-point fall in the six-repo
        canon-share headline — moved him. Recorded in the RULED note because
        a measurement that changes a ruling is the evidence that it was read.
      - **OQ-2 → the two globs**, `openspec/changes/**/proposal.md` and
        `openspec/changes/**/review/*.md`. Unopposed in prose.
      - **OQ-3 → the four families**, `status-validity`, `standard-backing`,
        `ratified-provenance`, `succession-integrity`. Unopposed in prose.
      - **OQ-4 → rewrite ALL 17, NOT the recommended split.** Prefix respell
        `Ratified by:` → `Ratified:`, content verbatim, each of the 17
        justified from its own record; the archived eleven under the B1/B2
        append-correction discipline with a bookkeeping note each.
      - **OQ-5 → add a conforming `Ratified:` line to the 3 review records.**
        As recommended. No third spelling enters the rule.
      - **OQ-6 → backfill ALL 47, NOT the recommended grandfather.** Every
        headerless proposal gets a `Status:` derived from its own record, and
        a floor-satisfying citation wherever that status is `ratified`. Where
        a record cannot support one, the campaign stops and reports rather
        than inventing.
- [x] 1.2 Brett ratified. `proposal.md` front matter now reads
      `Status: ratified` with a `Ratified:` citation on the next line — the
      record-citing spelling, because no approving OpenSpec change exists to
      name, which is exactly the condition of use
      `docs/document-lifecycle.md` § Status Claim Rules sets for it. The line
      clears the three-way floor on all three axes rather than the one it
      needs (approver `by Brett Heap`, date `2026-08-23`, and a resolvable
      record path), and sits at real line 5 — well inside the fifteen-line
      window, because this change of all changes must not repeat the
      roster-device defect.
- [x] 1.3 **N/A — OQ-1 was not ruled (a).** The spec deltas describe the
      ruling as authored; no `GOVERNED_ROOTS` widening, and none of the
      573-finding, 13-point, 123-test cost is carried into §5.
- [x] 1.4 **N/A — OQ-1 was not ruled (c).** Both spec deltas stay; §2 is the
      full realization, not a single test module.
- [x] 1.5 **N/A — OQ-3 ruled the four families as proposed.** The three
      places the family list appears in `specs/doc-health/spec.md` are
      already correct and are left untouched.
- [x] 1.6 **N/A — OQ-6 REFUSED the pre-contract-legacy grandfather.** There
      is no contract date to record, because there is no reduced-severity
      class in this change. The removal has three consequences, each
      discharged where it lands: §2.4 is rewritten below, the
      `document-lifecycle` delta's pre-contract-legacy paragraph and its
      "A packet predates the contract date" scenario are replaced by the
      stop-and-report rule the ruling actually took, and §5 grows from 24
      hand-discharges to 68.

## 2. Realization (openxFactory main line) — LANDS LAST

**Numbered second, merged last.** §2 is written here because it is what the
change is about, but under the 2026-08-23 ruling its landing commit is the
FINAL slice: it merges only after §5A–§5C have taken the scan set to zero
CRITICAL and zero ERROR, verified by §5D.2. Building §2 early is fine;
merging it early is the failure mode the whole ordering exists to prevent.

- [ ] 2.1 `scripts/doc_health/corpus.py`: add `LIFECYCLE_SCAN`, a tuple of
      explicit glob patterns (`openspec/changes/**/proposal.md`,
      `openspec/changes/**/review/*.md` as ruled), and
      `load_lifecycle_docs(repo_name, repo_path)` beside `load_docs`. Reuse
      `_excluded`, `parse_status` and `parse_kind` — do not write a second
      header reader; `align-status-reader-to-real-lines` exists because the
      corpus grew seven of those.
- [ ] 2.2 `scripts/doc_health/runner.py`: one new `Context` field,
      `lifecycle_docs`, populated in `build_context` for every repo in scope
      by the same loop that builds `docs`. It MUST NOT feed
      `inventory`, `catalog_root`, the per-stage census, or the canon-share
      computation.
- [ ] 2.3 `scripts/doc_health/families.py`: `fam_status_validity`,
      `fam_standard_backing`, `fam_ratified_provenance` and
      `fam_succession_integrity` iterate `ctx.docs` plus
      `ctx.lifecycle_docs`. Introduce one shared accessor rather than four
      copies of the concatenation, so a fifth reader is a one-line opt-in
      and an audit can find every reader by call site.
- [ ] 2.4 **No severity special-casing of any kind.** OQ-6 refused the
      pre-contract-legacy grandfather, so the draft's reduced-severity rule
      string, its contract date and its date table are all deleted work: a
      headerless proposal is a `status-validity` ERROR whenever it was
      authored, and an uncited `ratified` header is a `ratified-provenance`
      CRITICAL whenever it was written. This box exists as a NEGATIVE
      instruction because the deleted version was specific enough to be
      re-derived by a builder reading `proposal-origin` for a pattern — if
      you find yourself adding a legacy tier here, the ruling says not to.
      The population that would have taken the reduced tier is discharged by
      §5C instead, and §5D's zero-finding gate is what replaces the tier.
- [ ] 2.5 `docs/document-lifecycle.md` § Status Claim Rules: state that a
      change packet's `proposal.md` and its `review/` ratification records
      are governance documents, that the rest of the packet is not ruled,
      and that a `Ratifier:`/`Decision date:` pair accompanies a sanctioned
      citation rather than replacing it. Authors read this file, not the
      family source.
- [ ] 2.6 Update `corpus.py`'s module docstring, which today says governance
      Markdown "lives under docs/, templates/, contracts/, examples/, and
      ideation/" and stops there. After this change that sentence is true of
      the governed corpus and incomplete about what the pass reads.

## 3. Tests (mutation-validated)

- [ ] 3.1 Membership: the scan set contains a packet's `proposal.md` and its
      `review/*.md`, and does NOT contain `tasks.md`, `design.md`,
      `specs/*/spec.md`, `supporting-docs/**` (including
      `source-snapshots/**`), or `evidence/**`. Assert on the resolved path
      list, not on a count — a count passes for the wrong set.
- [ ] 3.2 Each of the four families fires over a scan-set document, with a
      fixture per rule: uncited `ratified`, out-of-window `Status:`,
      free-form status, unbacked `standard`, `superseded` without successor.
- [ ] 3.3 Each of the other twelve families does NOT fire over a scan-set
      document. Drive this from `FAMILIES` itself so a family added later is
      covered by construction, and fail loudly if a new family appears in
      neither list. This is the test that makes §2.3's "one-line opt-in"
      safe.
- [ ] 3.4 The invariance test, which is the load-bearing one: over a fixture
      corpus with a non-empty scan set, `ctx.docs`, the per-stage counts, the
      governance and canon word totals, the canon-share string, the shared
      inventory entries and the catalog snapshot bytes are identical to the
      same run with an empty scan set. Compare rendered bytes, not summed
      integers.
- [ ] 3.5 The two historical defects, as regression fixtures rather than as
      prose: phase-b's uncited `ratified` header must produce a
      `ratified-provenance` finding, and roster-device's line-41 header must
      produce a `status-validity` missing-header finding and NOT a
      `ratified-provenance` one. Both were replayed against the real pre-fix
      blobs (`02a71d6` and `280fc8b`) while authoring this proposal; the
      fixtures freeze that result.
- [ ] 3.6 Mutation-validate 3.1 through 3.5. At minimum: flip the scan set to
      the empty tuple (3.1–3.3, 3.5 must fail), flip it to bare `("openspec",)`
      (3.1 must fail — the glob boundary is the claim), remove one family from
      the reader list (3.2 must fail), and add one family to it (3.3 must
      fail). Record which mutation each test caught. Beware the platform-inert
      class: a mutation that leaves observable values unchanged on this
      platform proves nothing, so pin the boundary with a structural assertion
      on the declared pattern set, not only on the resulting counts.
- [ ] 3.7 Confirm `tests/doc-health` is 724 + N and that no pre-existing test
      changed meaning. If any existing test needs editing, that is a finding
      about the design, not a chore: say so before editing it.

## 4. Gates, index, archive

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate govern-openspec-corpus-membership --strict`
      and `--all --strict` green (69 items at authoring; re-check the total
      against whatever else has landed).
- [ ] 4.2 `python3 -m pytest tests/doc-health` green;
      `python3 -m pytest tests/ideation-dashboard -k workbench` at 140.
- [ ] 4.3 A doc-health single-repo run whose severity counts move by exactly
      the predicted amount and in no other line. There is now exactly ONE
      prediction, because OQ-6 removed the dispositioned branch: **the
      unchanged baseline, 4 critical / 6 error / 68 warning / 4 info.** Any
      other number is a defect in §2 or an incomplete §5, not a surprise to
      accept. The draft's second branch (24 / 54 / 68 / 4, §5
      dispositioned rather than discharged) is void, and so is the third the
      grandfather would have produced (4 / 6 / 112 / 4, the 44 archived
      headerless proposals reported as reduced-severity warnings).
- [ ] 4.4 Re-run the corpus-shape measurement and assert the canon-share
      headline, documents examined, and governance word total are UNCHANGED
      from baseline. This is the claim that distinguishes the ruled option
      from the one that was rejected, so it is measured rather than asserted.
- [ ] 4.5 README Active row updated when the change lands, moved to the
      archived block on archive.
- [ ] 4.6 Archive on merged-plus-green per `target_release: implemented` —
      no contract bundle is cut, so no release tag is owed.
- [ ] 4.7 Tick `sanction-ratified-record-spelling` task 5.1 with a pointer to
      this change and to the option ruled, under the append discipline that
      change's own §5.2 established. That box is the reason this change
      exists and closing it is part of finishing.

## 5. The discharge campaign — all 68, to zero

**Blocks §2's merge.** Every item below is a ruling to execute, not a
judgement to make here.

### The arithmetic this section owes, recounted after the ruling

The draft's "68 standing violations" figure survives the ruling as a count of
FINDINGS and does not survive it as a count of WORK. Re-measured over the
scan set at this branch's head — 119 documents, `openspec/changes/**/proposal.md`
plus `openspec/changes/**/review/*.md`, the four ruled families:

| axis | findings | what discharges them under the ruling |
| --- | --- | --- |
| `ratified-provenance` | **20 CRITICAL** | 17 prefix respells (11 archived + 6 active) + 3 review-record conforming lines |
| `status-validity` | **48 ERROR** | 47 header backfills (44 archived + 3 active) + 1 free-form split |
| `standard-backing` | 0 | — |
| `succession-integrity` | 0 | — |
| **total** | **68** | **all 68 by edit; none by grandfather, none by disposition** |

Three things the recount changes, none of which the draft's arithmetic
carried:

1. **Hand-discharges go from 24 to 68.** The draft discharged 20 + 3 + 1 by
   edit and sent 44 to a reduced-severity tier. That tier is refused, so the
   44 are work.
2. **The two axes are COUPLED across the 47 backfills, so the edit count is
   larger than the finding count.** Measured: **not one of the 47 headerless
   proposals carries a ratification citation anywhere in its file**, in
   either spelling, inside the header window or out. Every backfill whose
   derived status is `ratified` therefore needs a `Status:` line AND a
   floor-clearing citation line in the same edit — up to 2 header lines per
   document, ~88 lines across the archived 44. Writing the status first and
   the citation later does not reduce the count, it just converts an ERROR
   into a CRITICAL in between.
3. **The evidence base for the 44 is thinner than "add a line" implies.**
   Of the 44 archived headerless proposals, 43 carry an `.openspec.yaml` and
   only **21 of those carry an `approved_by`/`approved_on` pair** — and C2
   already ruled that an `origin:`-nested pair records permission to author,
   not ratification. So for the other 23 the derivation must come from the
   archive or ratification commit, the change's own `tasks.md`, or the README
   row, one record at a time. This is the long pole, and it is why 5C is its
   own slice.

### Slices, in dependency order

Four mergeable slices. Each is a commit or a small series; each leaves the
tree green; the count in the slice title is the findings it clears.

- [x] **5A — active-record edits (13 documents, clears 9C + 4E).** Twelve of
      the thirteen are live documents, so no archive discipline is engaged
      and no bookkeeping note is owed on them; the thirteenth (5A.2's third
      review record) sits under `archive/` and takes 5B's discipline even
      though it is grouped here. First because it is the cheapest proof that
      the respell and backfill shapes are right before they are applied to
      the remaining 55 findings.

      **DONE 2026-08-23**, branched from `origin/main` at `eb12aa5`. Thirteen
      documents edited, and all thirteen are ACTIVE — the slice took every
      finding on a non-archive document, which is what "active-record edits"
      means, rather than the thirteen names the draft listed. The one
      substitution: 5A.2's third record is under `archive/` and was LEFT for
      5B, and a review record that did not exist when the proposal was
      measured (`add-notebook-projection-identity/review/ratification-2026-08-23.md`)
      took its place. The count is unchanged at 13 documents / 9C + 4E; only
      the membership moved, and it moved in the direction the slice boundary
      says it should.

      **Scan-set census, measured through the real helpers in
      `scripts/doc_health/` over the ruled globs and the four ruled families**
      (`openspec/changes/**/proposal.md` + `openspec/changes/**/review/*.md`;
      `status-validity`, `standard-backing`, `ratified-provenance`,
      `succession-integrity`):

      | | before 5A | after 5A | delta |
      | --- | --- | --- | --- |
      | scan set documents | 121 | 121 | 0 |
      | `ratified-provenance` | 21 CRITICAL | **12 CRITICAL** | −9 |
      | `status-validity` | 48 ERROR | **44 ERROR** | −4 |
      | `standard-backing` | 0 | 0 | 0 |
      | `succession-integrity` | 0 | 0 | 0 |
      | **total** | **69** | **56** | **−13** |
      | of which on ACTIVE documents | 13 | **0** | −13 |

      Two honest corrections to the arithmetic §5 opened with. The pre-slice
      figure is **69, not 68**: the scan set has grown from the 119 documents
      the proposal measured to 121, and one of the two new documents is
      `add-notebook-projection-identity`'s ratification record, which carries
      the same third-vocabulary shape OQ-5 ruled on and so added a 21st
      CRITICAL. The proposal's 68 was correct when taken and is not
      retro-edited; this is the number a re-measurement returns today, and
      5D.1's re-measure is the one §4.3 checks against. Second: the remaining
      **56 are every one of them under `archive/`** — 12 CRITICAL (5B's eleven
      respells plus the archived review record 5A.2 handed over) and 44 ERROR
      (5C's backfills). Zero active findings remain in the scan set.

      **Whole-repo run unmoved, verified by byte comparison rather than by
      eye.** `python3 scripts/doc-health.py --single-repo . --as-of 2026-08-23`
      produces a report BYTE-IDENTICAL to the pre-edit baseline — 4 critical /
      6 error / 68 warning / 4 info, canon share 31.2%, 327 documents. That is
      the predicted result and it is also the thing worth checking: the scan
      set is not yet enforced (§2 has not landed), so an edit inside
      `openspec/` that moved the whole-repo report would mean something else
      had changed. Nothing did. (The 31.2% reads against the proposal's
      31.3% because main has moved since that measurement, not because of
      this slice — the before and after runs here agree to the byte.)

      **[Provenance of "327 documents", added 2026-08-23 (review N2).** The
      report prints no documents-examined field, so that figure was cited as
      though quoted when it is DERIVED — the Per-Stage Counts table's Docs
      column sums to 327 (2 + 127 + 69 + 1 + 22 + 29 + 1 + 68 + 6 + 2). The
      number is right; only its provenance was missing, and it is recorded
      now so the next reader can check it in the report rather than take it on
      trust. `4 critical / 6 error / 68 warning / 4 info` and `canon share
      31.2%` are quoted from the Headline block and were always checkable.**]

      **RE-MEASURED 2026-08-23 on the fix lap, after merging `origin/main`
      into this branch.** The merge brought in another session's MedxChart and
      MedxPractice boundary work (`origin/main` at `7431f03`, six commits),
      and the fix lap corrected `add-dispatch-credential-contract`. Both move
      the numbers, in opposite directions and for unrelated reasons, so the
      census is restated rather than patched:

      | | after 5A | + merge + fix lap | delta |
      | --- | --- | --- | --- |
      | scan set documents | 121 | **123** | +2 |
      | `ratified-provenance` | 12 CRITICAL | **12 CRITICAL** | 0 |
      | `status-validity` | 44 ERROR | **46 ERROR** | +2 |
      | `standard-backing` | 0 | 0 | 0 |
      | `succession-integrity` | 0 | 0 | 0 |
      | **total** | **56** | **58** | **+2** |
      | of which on ACTIVE documents | 0 | **2** | +2 |
      | scan-set documents `ratified` AND cited | 64 | **65** | +1 |

      Reading the three moves honestly:

      - **+2 documents, +2 ERROR, and both on ACTIVE documents:**
        `openspec/changes/create-medxchart-overlay-boundary/proposal.md` and
        `openspec/changes/create-medxpractice-overlay-boundary/proposal.md`,
        both headerless, both landed on `main` from another session while 5A
        was in flight. **This slice does not edit them** — see 5D's
        moving-target note. 5A's "zero findings left on any active document"
        was true of the tree 5A measured and is no longer true of `main`;
        that is the gate moving, not the slice being wrong.
      - **+1 ratified-and-cited document, +0 findings:**
        `add-dispatch-credential-contract` moved from an uncited `draft` to a
        cited `ratified`. Neither state emits a finding, which is precisely
        why no gate caught the wrong value.
      - **12 CRITICAL unchanged**, and every one of the 58 that is not one of
        the two new actives is under `archive/` — 12 for 5B (now 12 of 28
        documents, the other 16 being latent) and 44 for 5C.

      Measured through the same real helpers over the same ruled globs and
      the same four ruled families. The census taken on the merged tree BEFORE
      this lap's edits and the one taken AFTER are byte-identical, which is
      the point: the whole +2 is the merge's and none of it is the fix's.

      **Whole-repo run on the merged base: `4 critical / 8 error / 68 warning
      / 4 info`, canon share 31.2%.** The two extra errors against 5A's
      recorded `4 / 6 / 68 / 4` are the merge's, not this lap's: they are
      `proposal-origin` "proposal carries no origin declaration" errors on the
      same two new MedxChart/MedxPractice packets. This lap's edits leave that
      report unmoved — measured before and after, not assumed. §4.3's
      "unchanged baseline" prediction is therefore against `4 / 8 / 68 / 4` as
      of this merge, and against whatever 5D.1 measures at enforcement time.

      **Gates.** `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` →
      **70 passed, 0 failed (70 items)**. `python3 -m pytest tests/doc-health`
      → **724 passed**. `python3 -m pytest tests/ideation-dashboard -k
      workbench` → **140 passed**, 3858 deselected — and no upper-cased HTTP
      write verb enters any prose this slice writes, the substring the
      workbench's no-write-path assertion trips on.

      **Gates re-run on the 2026-08-23 fix lap, after the merge:**
      `openspec validate --all --strict` → **72 passed, 0 failed (72 items)**
      (70 plus the two changes the merge brought in);
      `pytest tests/doc-health` → **724 passed**;
      `pytest tests/ideation-dashboard -k workbench` → **140 passed**, 3858
      deselected; the whole-repo doc-health report **byte-identical** to the
      merged base; no upper-cased HTTP write verb in any added line.
  - [x] 5A.1 The 6 ACTIVE proposals whose `Ratified by:` names a record
        rather than a change (`add-composed-view-authoring`,
        `add-lens-document-selection`, `add-trust-anchor`,
        `admit-install-repos-to-aggregation`,
        `implement-keycloak-install-repo`, `implement-openxpki-install-repo`):
        respell the prefix to `Ratified:`, carry the content after the colon
        VERBATIM, and record in each change's own `tasks.md` which record
        justifies its line. Do NOT rewrite the content — a respell that also
        improves the prose is two edits wearing one name.

        **DONE.** All six respelled, all six at real line 5, inside the
        window. The verbatim rule was enforced mechanically rather than by
        care: the edit asserted that the bytes following the prefix are
        IDENTICAL before and after, and `git diff --word-diff` shows one
        changed token per file — `Ratified by:` → `Ratified:` — and nothing
        else. Per-record justification, consolidated HERE rather than into
        each of the six changes' own `tasks.md` (one slice, one record, and
        each of these six lines carries its justification on its own face):

        | change | the record that justifies the line | floor |
        | --- | --- | --- |
        | `add-composed-view-authoring` | Brett's 2026-08-08 in-session direction, quoted on the line — "yes, we need to draft from a project view" — given when the hand-off was found unavailable on every project-scoped view | date |
        | `add-lens-document-selection` | Brett's three annotations of 2026-08-08, all three quoted on the line (the unreadable relationship tiles and their unlabelled count, "this is taking up too much space. what value does it bring?", and the hover/checkbox instruction) | date |
        | `add-trust-anchor` | Brett Heap's 2026-08-21 in-session ruling, quoted — "ratify both proposals" — with OQ1 and OQ2 both ruled as recommended on the same line | date |
        | `admit-install-repos-to-aggregation` | Brett Heap's 2026-08-21 session instruction, quoted — "do the aggregation admission change, the two repos are added to openXfactory github app" | date |
        | `implement-keycloak-install-repo` | Brett Heap's 2026-08-21 session instruction, quoted — "do both install repos" — following his same-day rulings on the install-repo naming and the identity/PKI workstream | date |
        | `implement-openxpki-install-repo` | the same 2026-08-21 instruction and the same same-day rulings, recorded on its own line in its own words | date |

        **CORRECTED 2026-08-23 (review S3): the consolidation above did not
        satisfy the box, and the six per-change notes have now been written.**
        This box directs "record in each change's own `tasks.md` which record
        justifies its line", and the slice recorded them here instead. The
        table is a fine index and a poor substitute: a reader of
        `implement-openxpki-install-repo` who wonders why its citation was
        rewritten has to know that a different change's tasks file holds the
        answer. On the fix lap each of the six gained its own one-line
        justification note, quoting the same record this table names —
        five as a trailing `## Ratification-citation respell (2026-08-23)`
        section, and `add-trust-anchor` inline under its task 3.2, which is
        the box that set the `Ratified by:` header in the first place and is
        the least invasive home in that file. The table above stays as the
        index it always was; the tick is now honest.

        **Two measured notes a later reader will otherwise re-derive.**
        First, the latent-eighteenth check OQ-4 asks for came back clean:
        none of the six names a resolvable OpenSpec change. That is not an
        eyeball reading — `fam_ratified_provenance`'s primary-spelling branch
        had already run change-id resolution and `_resolves` against each of
        the six and rejected all six, which is why they were findings at all.
        `add-identity-brokering` remains the only member of that class and
        stays unrespelled, as ruled.

        **NARROWED 2026-08-23 (review S4).** The check above covered THE SIX
        and only the six; it was never a corpus-wide sweep, and the slice had
        no standing for the sentence "the only member of that class". It is
        not. Replaying the same primary-spelling resolution over the whole
        scan set finds **16 self-citing lines** that pass the family only by
        naming their OWN change id, plus **4 more** that pass by naming some
        other change in passing prose. The 16 are ruled into 5B by OQ-4's
        RULED-extension note of the same date; the 4 are measured and
        deliberately out. The corpus-wide finding and its ruling live there,
        not here. What this box can honestly claim is narrower and still
        useful: none of ITS six names a resolvable change, so none of the six
        was a false positive.

        Second, **each of the six clears the three-way floor on the DATE axis
        alone, not on approver-plus-date**, and that is correct rather than
        thin. Every one of them names its approver in prose (`Brett,
        2026-08-08`, `Brett Heap, 2026-08-21`), and `_CITATION_APPROVER`
        recognizes only the `by <Name>` form — the disclosed narrowing
        `families.py` documents at the pattern. Inserting `by` would rephrase
        content the ruling requires be carried VERBATIM, so the lines stand as
        written and clear on the date. The floor is disjunctive precisely so a
        narrow axis costs nothing; this is the case it was made disjunctive
        for.
  - [x] 5A.2 **(2 of the 3 listed here + 1 substitute; the archived third was
        HANDED TO 5B — see the read-back and 5B's handover block)**
        The 3 `review/` ratification records on the third vocabulary
        (`add-roster-directory-admission-surface/review/ratification-2026-08-22.md`,
        `add-substantive-review-lane/review/ratification-2026-08-22.md`,
        `archive/2026-08-22-add-roster-device-admission-surface/review/ratification-2026-08-19.md`):
        execute OQ-5 — add a conforming `Ratified:` line derived from the
        `Ratifier:`/`Decision date:` pair already on the page. Leave that
        pair standing. The third of these lives under `archive/`, so it takes
        5B's bookkeeping note even though it is grouped here for shape.

        **DONE, and the membership of this box changed under it.** The
        archived record named third above was NOT edited here: it takes 5B's
        bookkeeping discipline, and the honest place to apply that discipline
        is the commit that applies it to the other eleven archived records.
        It is handed to 5B, where it is now the twelfth archived CRITICAL.
        In its place this box took a review record that did not exist when the
        proposal was measured. The three edited, each line derived from the
        page's own two headers and inventing nothing, each inserted directly
        beneath the `Ratifier:` line it derives from and each landing at real
        line 6:

        | record | derived line | floor |
        | --- | --- | --- |
        | `add-notebook-projection-identity/review/ratification-2026-08-23.md` | `Ratified: 2026-08-23 by Brett Heap (repository owner) — in-session via question prompts` | approver + date |
        | `add-roster-directory-admission-surface/review/ratification-2026-08-22.md` | `Ratified: 2026-08-22 by Brett (repository owner)` | approver + date |
        | `add-substantive-review-lane/review/ratification-2026-08-22.md` | `Ratified: 2026-08-22 by Brett Heap (repository owner) — in-session via question prompts` | approver + date |

        The `Ratifier:` and `Decision date:` lines stay exactly as written on
        all three — OQ-5 ruled that they stop being the ONLY thing that says
        it, not that they stop saying it. `add-notebook-projection-identity`'s
        record is why the pre-slice census reads 21 CRITICAL rather than the
        proposal's 20: it landed on main after the measurement and carried the
        identical third-vocabulary shape, which is a small piece of evidence
        that OQ-5 ruled on a live convention and not on a closed legacy set of
        three. A `Ratified baseline:` line sits two lines below each new
        citation on all three pages and is NOT a second citation — the two
        sanctioned prefixes are read with `startswith`, and `Ratified
        baseline:` starts with neither. Verified rather than assumed: each of
        the three reports exactly ONE citation line through
        `families._header_lines`, so the one-total rule holds.
  - [x] 5A.3 The 3 ACTIVE headerless proposals
        (`add-dispatch-credential-contract`, `add-ideation-intent-plane`,
        `add-worker-enrollment-broker`): derive and write a `Status:` header,
        plus a citation if and only if the derived value is `ratified`. Two
        of the three carry no `.openspec.yaml` at all; that is a
        `proposal-origin` matter and is NOT fixed here.

        **DONE. Two ratified, one draft — and the draft is the point of the
        exercise.** Active does not mean ratified, and one of these three
        proves it. Each status was derived by hunting the sources C2
        established (the packet's `.openspec.yaml`, the change's own
        `tasks.md`, the README `OpenSpec Records` row, the archive and
        ratification commits) and by a repo-wide grep for the change id. All
        three headers went INSIDE the front matter, directly beneath
        `target_release:`, which is where every already-conforming proposal in
        this corpus carries them and which keeps `code_surface` and
        `target_release` where `ideation_dashboard.generator._header_value`
        already reads them.

        **`add-ideation-intent-plane` → `Status: ratified`** plus
        `Ratified: 2026-07-23 by Brett — "we are there, this is ready now to
        lock", recorded in the proposal commit cf1c3d0 and in the README
        OpenSpec Records row`. Evidence: the proposal commit `cf1c3d0`
        (2026-07-23) states in its body "Ratified by Brett 2026-07-23 ('we are
        there, this is ready now to lock')", and the README row says "ratified
        2026-07-23". What was deliberately NOT used: this packet's
        `.openspec.yaml` carries an `origin:`-nested
        `approved_by: Brett (openxFactory operator authority)` /
        `approved_on: 2026-07-23` pair, and C2 already ruled that such a pair
        records permission to AUTHOR. It happens to agree with the date here,
        which is exactly why it is worth saying it was not the source — a
        coincidence is not a citation. Floor: approver + date.

        **`add-worker-enrollment-broker` → `Status: ratified`** plus
        `Ratified: 2026-07-26 by Brett Heap — D1-D10 recommendations adopted
        as decided; phase-1 contract realization authorized, recorded in
        commit e535a3a and on the Approved line below`. Evidence: commit
        `e535a3a` (2026-07-26) is titled "Record Brett's approval of
        add-worker-enrollment-broker (D1-D10 adopted)" and is the commit that
        wrote the `Approved: 2026-07-26 by Brett Heap — D1-D10
        recommendations adopted as decided; phase-1 contract realization
        authorized.` line the proposal already carried in its body; the README
        row says the contract was "ratified BEFORE its three realizations are
        built". This is a decision ON CONTENT (D1-D10 adopted, realization
        authorized), not an `origin:`-nested permission to author, so it is a
        ratification and C2's distinction is respected rather than stretched.
        The `Approved:` line stays exactly where it was. Floor: approver +
        date.

        **`add-dispatch-credential-contract` → `Status: draft`, no citation
        written, because none is owed and none exists.** This is the honest
        answer and it took the most looking. Everything the record carries
        points AWAY from ratified: the authoring commit `4e4190c`
        (2026-08-13) calls it "the add-dispatch-credential-contract **draft**";
        the README row says "authored 2026-08-13" and never says ratified;
        its own task 4.2 lists ratification as a step still ahead ("current
        through ratification, realization, and archive"); it carries no
        `.openspec.yaml`; and a repo-wide grep for the change id across every
        `.md` and `.yaml` returns no ratifier and no ratification date
        anywhere. A `draft` header needs no citation, so nothing was invented
        to accompany it.

        **One flag raised — and RESOLVED on 2026-08-23, see the correction
        below.** `docs/openxdox-naming.md` carries `Status: ratified` /
        `Ratified by: add-dispatch-credential-contract`. When this box was
        written that read as a governed document whose primary-spelling
        citation names a change that is, on its own record, still a draft, and
        it was flagged as somebody's future problem. It was not a future
        problem and it was not somebody else's: it was the strongest single
        piece of evidence AGAINST the derivation this box had just made, and
        the box treated it as a downstream consequence instead of reading it
        as a record. Under the correction below the citation names a change
        that IS ratified, on the very date the naming record states. **The
        flag is closed, not pending.** No family ever fired on it — the change
        id resolves, which is all `fam_ratified_provenance` asks of the
        primary spelling — so nothing in the census moves either way; what
        changes is that the document is no longer depending on an act that
        had not happened.

        Nothing stopped and reported in this box. All three records supported
        a status; the one that could not support `ratified` supported `draft`,
        which is a derivation and not a fallback.

        ---

        **CORRECTION, 2026-08-23 (appended, nothing above struck): the
        `add-dispatch-credential-contract` derivation was WRONG, and the
        paragraph that argued for it was false at the sentence level.**
        Slice 5A's read-back is left standing verbatim above because the
        append discipline this change enforces on other people's records
        applies first to its own; what follows is the correction, not a
        rewrite.

        An adversarial review of the slice demonstrated that the hunt missed
        the record. The claim "everything the record carries points AWAY from
        ratified" was false. What the review found, none of which the slice
        looked at:

        - **PR `#168`**, merged **2026-08-13T18:46:52Z** (merge commit
          `4e4190c` — the SAME commit the slice cited as the authoring commit
          for "the add-dispatch-credential-contract **draft**"), whose body
          states in bold: "**Merging this ratifies the openXdox naming
          record** (`draft` to `ratified`, its task 1.2)". The slice read the
          commit and did not read the pull request that landed it.
        - **This change's own task 1.2 is TICKED** — "Ratify the openXdox
          naming on approval" — which is the act that PR body says merging
          performs. A ticked task conditioned on approval is a record that the
          approval happened.
        - **`docs/openxdox-naming.md` line 11**: "Ratified by
          `add-dispatch-credential-contract` (2026-08-13) … landing that
          change is its lifecycle ratification." The slice READ this document
          — it is the flag raised in the paragraph above — and treated it as a
          dangling dependency rather than as the sentence that says what the
          landing means.
        - **Realization PRs `#171` (merged 2026-08-13) and `#172` (merged
          2026-08-14)** are on `main`. Realization of an unratified contract
          change is not a thing this corpus does.

        **The one ground the slice did cite is not evidence at all (review
        S1).** The box argued that "its own task 4.2 lists ratification as a
        step still ahead ('current through ratification, realization, and
        archive')". That sentence is house boilerplate for a README-currency
        task, and the SAME slice, in the SAME box, ruled
        `add-ideation-intent-plane` **ratified** while its task 5.2 carries
        the identical unticked line ("Keep the README 'OpenSpec Records' entry
        current through ratification, realization, and archive"). A ground
        that the slice itself treated as non-evidence one document earlier
        cannot carry a derivation one document later. Four further archived
        changes carry the same sentence, ticked at archive with a realization
        summary — `2026-07-29-add-ideation-dashboard`,
        `2026-08-04-add-ideation-cross-reference-readiness`,
        `2026-08-04-add-possibles-derivation-lane` and
        `2026-08-06-add-proposal-origin-contract`. All four are themselves
        headerless and belong to 5C's backfill population, so they are cited
        for what they DO show and nothing more: the sentence is a
        README-currency chore whose lifetime spans the whole change, not a
        marker that ratification is still ahead.

        **Superseded by Brett's ruling (2026-08-23, in-session).** The landing
        of PR `#168` WAS the approval act this change's own task 1.2
        conditioned on, so `add-dispatch-credential-contract` is **ratified
        2026-08-13**. `proposal.md` now reads `Status: ratified` with a
        record-citing `Ratified:` line at real line 5 — the record-citing
        spelling because no approving OpenSpec change exists to name — citing
        all four record points above and stating plainly that the value was
        first derived `draft` by slice 5A on an incomplete hunt and corrected
        under this ruling. Measured through the real helpers: the line clears
        the three-way floor on **all three axes** (approver `by Brett Heap`,
        date `2026-08-13`, resolvable record path `docs/openxdox-naming.md`),
        it is the document's only citation line, and it sits at real line 5,
        inside `corpus.STATUS_SCAN_LINES`.

        **The census does not move.** A `draft` proposal with no citation
        emits nothing from either ruled family, and a `ratified` proposal with
        a floor-clearing citation emits nothing either. The correction
        therefore adds one ratified-and-cited document to the scan set and
        zero findings to the count — which is worth stating, because "no
        finding moved" is exactly what let the wrong value sit unchallenged in
        the first place. A gate cannot catch a derivation error; only a reader
        can, and one did.

        **Two further corrections to the 5A commit message, which is pushed
        and therefore cannot be edited (review S2, N3).** They are recorded
        here because this read-back is the record that can be appended to:

        - The commit message states "all thirteen report exactly one citation
          line via `families._header_lines`". **That was false when it was
          written — twelve did.** `add-dispatch-credential-contract` was
          given `Status: draft` and no citation, so it reported ZERO. The
          verification was run and its result was over-reported by one.
          **After this fix all thirteen genuinely do**, re-measured through
          `families._header_lines` over the same thirteen documents:
          13/13 exactly one, every citation inside the window (real line 5 on
          eleven, line 6 on the three review records, line 9 on
          `add-wallet-carried-review-authority`).
        - The commit message states "both pairs stay standing" of the
          `Ratifier:`/`Decision date:` pairs left untouched by 5A.2. There are
          **three** such records and therefore three pairs, which is what the
          5A.2 read-back above says correctly ("stay exactly as written on all
          three"). The commit message undercounts; the tree is right.
  - [x] 5A.4 The 1 free-form status
        (`add-wallet-carried-review-authority/proposal.md`, whose `Status:`
        value at real line 7 runs on into a ratification clause): split the
        value from the clause. The taxonomy value and the citation are two
        headers. The resulting `Ratified:` line clears the floor on its date
        and on `by <Name>` if the approver is written in the recognized form
        — `Brett Heap (openxFactory operator authority)` is not read as an
        approver unless `by` precedes the name.

        **DONE.** The document is
        `openspec/changes/add-wallet-carried-review-authority/proposal.md`,
        the only free-form status in the scan set and an ACTIVE one, so it
        belongs to this slice. Its `Status:` at real line 8 read
        `ratified — Brett Heap (openxFactory operator authority),
        2026-08-23,` — `STATUS_RE` is `^Status:\s*(.+?)\s*$`, so it swallowed
        the whole first physical line of a three-line ratification sentence
        and handed `TAXONOMY` a value no taxonomy contains. Split into two
        headers, nothing dropped:

        ```
        Status: ratified
        Ratified: 2026-08-23 by Brett Heap (openxFactory operator authority) — in-session
        ruling (the same mechanism that ratified add-substantive-review-lane on
        2026-08-22). Realization proceeds per tasks.md, S1 first.
        ```

        `by` was written before the name, as this box directs, so the
        approver axis reads it; date and approver both clear, and only the
        FIRST real line of the citation is read for the floor, which is why
        both axes sit on it. The citation lands at real line 9, in window.

        **The coupling this box demonstrates, stated because it is the
        general case and not a quirk of this document.** Before the edit
        `fam_ratified_provenance` never looked at this file at all — it
        guards on `doc.status != "ratified"`, and a free-form status is not
        `"ratified"`. Fixing the `status-validity` ERROR is therefore the act
        that makes the document VISIBLE to the citation rule for the first
        time. Had the split landed without the citation, this slice would have
        traded one ERROR for one CRITICAL and discharged nothing — the exact
        arithmetic §5's recount warns about for the 47 backfills. Both lines
        landed in one edit; re-measured, the document emits nothing from
        either family.
- [ ] **5B — the respells: 12 live CRITICALs plus the 16 latent self-citers
      (28 documents; clears 12C).** Same prefix respell as
      5A.1, same verbatim content, plus the discipline archived records take.
      Blocked on 5A only in the sense that the shape should be settled first.
      The eleven: `2026-07-30-add-ontology-stewardship-hardening`,
      `2026-08-04-adopt-neutral-utility-pack`,
      `2026-08-06-add-opendox-project-header`,
      `2026-08-06-add-project-scoped-selection`,
      `2026-08-07-add-project-merged-projection`,
      `2026-08-07-add-register-edit-lane`, `2026-08-08-add-openxwallet`,
      `2026-08-09-add-project-visible-set`, `2026-08-09-add-repository-lens`,
      `2026-08-13-add-session-notebook-reconciliation`,
      `2026-08-15-add-subject-overlay-contract`.

      **HANDED OVER BY 5A (2026-08-23): a twelfth archived document, and it
      is not a respell.**
      `archive/2026-08-22-add-roster-device-admission-surface/review/ratification-2026-08-19.md`
      is 5A.2's third record — the archived member of the three-vocabulary
      review set. Its EDIT is 5A.2's (a conforming `Ratified:` line derived
      from its own `Ratifier:`/`Decision date:` pair, the pair left standing),
      but its DISCIPLINE is 5B's, and the honest place to apply 5B's
      discipline is the commit that applies it to the other eleven. So 5B
      clears **12 CRITICAL, not 11**: eleven prefix respells and one derived
      review-record line, each under 5B.2's in-place-overwrite discipline with
      5B.3's travelling bookkeeping note, and 5B.4's register entry should
      account for twelve rather than eleven.

      **GROWN BY OQ-4's RULED EXTENSION (2026-08-23): the 16 self-citing
      `Ratified by:` lines join this slice.** The slice-5A adversarial review
      found 16 documents whose `Ratified by:` line names the document's OWN
      change id and so passes `fam_ratified_provenance` by self-reference. A
      change is not its own approving change; the lines are substantively
      record-citing, and Brett ruled them the same class with the same remedy.
      The enumeration and its measured boundary are in proposal.md's OQ-4
      RULED-extension note. Split: **1 ACTIVE**
      (`add-hermes-customer-subject-runtime-contract`, which takes no archive
      discipline) and **15 archived** (`2026-07-23-add-hermes-domain-overlay-contract`,
      `2026-07-23-adopt-subject-tenant-domain-vocabulary`,
      `2026-07-24-add-client-layer-tuning-contracts`,
      `2026-07-24-add-hermes-domain-content-manifest`,
      `2026-07-24-add-omnigent-domain-overlay`,
      `2026-07-29-add-crystallizer-contracts`, `2026-07-29-add-pattern-ledger`,
      `2026-07-30-add-capability-steward`,
      `2026-07-30-add-deployment-handoff-boundary`,
      `2026-07-30-add-domain-ontology-layer`,
      `2026-08-01-add-dashboard-repo-selector`,
      `2026-08-01-add-workbench-branch-sessions`,
      `2026-08-05-add-neutrality-drift-lane`,
      `2026-08-05-adopt-neutral-tooling-home`,
      `2026-08-06-add-consent-instrument`).

      **These 16 are LATENT, and 5B must say so at its own tick.** They fire
      NOTHING today — the family accepts them — so their respell **clears no
      finding**, does not move 5D.1's census by one, and is not what makes
      5D.2 read zero. It is a corrective edit made because the ruling says the
      spelling is wrong, not a discharge. A tick that reports "28 documents,
      28 discharges" would be the same overstatement this whole change exists
      to make impossible.

      **The counts this slice now owes**, kept apart on purpose:
      documents edited **28** (12 finding-driven + 16 corrective);
      findings cleared **12 CRITICAL** (11 archived respells + 1 archived
      review record); archived records touched **27** (12 + 15), which is what
      5B.4's register entry accounts for; active records touched **1**
      (`add-hermes-customer-subject-runtime-contract`).
  - [ ] 5B.1 For each of the eleven, name the record that justifies its line
        — the line's own approver-and-date is the substance, and the task is
        to say where that came from. Eleven justifications, not one block
        ruling: OQ-4 rejected the block form on the grounds that it records a
        class decision rather than per-record backing. **Extended to 28**
        (2026-08-23): the twelfth live document (5A.2's handed-over archived
        review record) and each of the 16 self-citers take the same per-record
        justification. The block form stays rejected for them too — a self-
        citer's line names an approver and a date on its own face, and the
        task is to say which record that approver-and-date came from, one
        document at a time. Record each justification the way 5A.1 did, in
        each change's OWN `tasks.md`, per the review's S3 adjudication.
  - [ ] 5B.2 Each respell is an **in-place overwrite and an extension of
        Brett's 2026-08-10 append ruling, named as one**, for the mechanical
        reason B1 states: `doc_health.corpus.STATUS_RE` is
        `^Status:\s*(.+?)\s*$` and swallows any trailing annotation, so an
        append on a single-valued header is impossible. Preserve the original
        line VERBATIM in the bookkeeping note, so a reader still finds what
        the record said before.
  - [ ] 5B.3 Each bookkeeping note travels with the change it corrects —
        `split-ideation-book-per-repo` 4.3's inline-suffix shape or B1's
        trailing `##` section, whichever fits the document; the invariant is
        that the correction never lands silently, not that the shape matches.
  - [ ] 5B.4 Append an entry to `docs/archive-record-discrepancies.md`
        recording the block, its 2026-08-23 authority, and the eleven
        per-record justifications. The register is where archived-record
        edits are accounted for; eleven of them going unrecorded there would
        be the same defect the register exists to report.
        **Scope revised 2026-08-23: the entry accounts for 27 archived
        records, not eleven** — the 11 archived respells, the 1 archived
        review record 5A.2 handed over, and the 15 archived self-citers from
        OQ-4's extension. It must distinguish the two grounds plainly: 12 were
        live CRITICAL findings and 15 were latent lines that no family
        reported, corrected because the ruling says the spelling is wrong. The
        active self-citer
        (`add-hermes-customer-subject-runtime-contract`) is NOT a register
        entry — it is a live document and no archive rule is engaged.
- [ ] **5C — the 44 archived backfills (clears 44E). The long pole.** Do not
      start this before 5A and 5B have settled the two edit shapes. Expect
      per-record research, not mechanical application.
  - [ ] 5C.1 For each of the 44, hunt the ratification evidence in the order
        C2 established: the packet's `.openspec.yaml` (43 have one; only 21
        carry an `approved_by`/`approved_on` pair), `Ratified`-style lines
        elsewhere in its record, the archive and ratification commits, the
        change's own `tasks.md`, the README row. Record per document what was
        found and what it supports.
  - [ ] 5C.2 Where the record supports it, write `Status:` and — where the
        derived value is `ratified` — a citation line in the same edit, in
        whichever sanctioned spelling honestly fits. Same append-correction
        discipline as 5B.2/5B.3: in-place, named as an extension, original
        state preserved in prose, note travelling with the change.
  - [ ] 5C.3 **STOP AND REPORT, do not invent.** Where a record genuinely
        cannot support a status, or supports a status but not a citation the
        floor accepts, the campaign leaves that document alone and reports it
        BY NAME with what its record does and does not carry. It does not get
        a plausible-looking header, and it does not get skipped in silence.
        The anti-invented-provenance principle survives OQ-6's widening
        intact — C2's "no invented provenance anywhere" and C7's "nothing was
        inferred, and nothing was discovered" are still the rule; only the
        population they apply to grew.
  - [ ] 5C.4 Five of the 44 are ALREADY-ADJUDICATED stop-and-report
        candidates and are the first place to look, because a 2026-08-22
        ruling hunted their records and left them headerless:
        `add-propose-verb` (record names no ratifier and no ratification date
        at all), `add-staging-workbench`, `add-workbench-bullseye-and-create`
        and `add-wheel-action-verbs` (each has an `origin:`-nested
        `approved_by`/`approved_on` recording permission to author, dated six
        to eleven days before archive, plus a task sign-off — two
        near-misses, neither a ratification), and
        `add-workbench-integrated-editor-chat`, which was raised to Brett as
        5D.2a and **RULED 2026-08-23: backfill it too** — see 5D.2a for the
        supersession discipline. Its history: its archive commit `354ded9`
        records a decision AGAINST
        writing a status value, register entry A2 verifies that decision as
        deliberate, and a `Status: ratified` beside its existing lowercase
        `status: proposed` would put two status fields on one proposal and
        overturn a ruling nobody revisited. Re-opening any of the five needs
        evidence C2 did not have, not a second reading of the evidence it
        did.
  - [ ] 5C.5 The other 39 are the pre-convention population C2 explicitly put
        out of scope ("The thirty-nine pre-convention headerless proposals
        were out of scope for this ruling and stay exactly as they were").
        Nobody has examined them one by one. Budget accordingly; this is the
        slice most likely to need its own session.
  - [ ] 5C.6 Record the campaign's outcome in
        `docs/archive-record-discrepancies.md` as C2's successor entry,
        stating plainly that the 2026-08-23 ruling supersedes C2's class
        decision ("The forty-six-wide option was not taken") while leaving
        C2's per-record FINDINGS standing word for word. C2's execution table
        is evidence, not a decision, and the append discipline protects it.
- [ ] **5D — re-measure to zero, then release §2.**

      **THE ZERO GATE IS A MOVING TARGET, and the campaign must be planned
      around that rather than surprised by it (review S5, 2026-08-23).** The
      scan set is `openspec/changes/**` — the busiest directory in the
      repository — so every session that lands a new change adds a document to
      the set, and a new proposal authored without a `Status:` header adds a
      `status-validity` ERROR the moment it merges. This is not hypothetical
      and it is not a forecast: it happened DURING 5A. Two headerless ACTIVE
      proposals landed on `main` from another session's MedxChart/MedxPractice
      boundary work while 5A was in flight —
      `openspec/changes/create-medxchart-overlay-boundary/proposal.md` and
      `openspec/changes/create-medxpractice-overlay-boundary/proposal.md` —
      and merging `origin/main` into this branch carried both in. 5A's
      read-back had just recorded ZERO findings left on any active document;
      the merge made that two. **Neither file is edited by this change.** They
      are another session's in-flight work, they are `status-validity`
      stragglers of exactly the shape 5D exists to catch, and editing another
      session's uncommitted-in-spirit packet to make a gate green is the
      wrong remedy for the right finding.

      Three consequences, stated so nobody re-derives them at the gate:
      **(1)** every census in this file is a measurement with a timestamp, not
      a standing fact — 68 at proposal, 69 at 5A's start, 56 at 5A's close, 58
      after the merge; **(2)** 5D.1's re-measure at enforcement time is the
      number that BINDS, and it is the only one §4.3 checks against; **(3)**
      discharging whatever stragglers exist at that moment belongs to whoever
      lands §2, not to 5A/5B/5C — the discharge slices own the population they
      enumerated, and the enforcement slice owns the delta. The durable fix is
      the enforcement itself: once §2 lands, a headerless proposal is a red
      gate on the PR that writes it, which is the whole point.
  - [ ] 5D.1 Re-run the scan-set measurement after 5A–5C and record the
        resulting counts in this file. The number §4.3 checks against is
        whatever this task measures, not whatever the proposal predicted.
        Re-measure the ACTIVE stragglers too, by name, and discharge whatever
        the set has accumulated since 5A/5B/5C closed — see 5D's moving-target
        note. As of the 2026-08-23 merge of `origin/main` that is the two
        MedxChart/MedxPractice proposals, and the honest expectation is that
        it will be a different list by the time §2 is ready.
  - [ ] 5D.2 **The merge gate, stated as a number: the scoped scan over
        `openspec/changes/**/proposal.md` + `openspec/changes/**/review/*.md`
        MUST report ZERO CRITICAL and ZERO ERROR across all four ruled
        families at the moment §2 merges**, and the whole-repo single-repo
        run MUST read its unchanged baseline of 4 critical / 6 error / 68
        warning / 4 info. Any stop-and-report document from 5C.3 is a
        NON-ZERO result and blocks the merge until it is ruled — it does not
        get waved through as a known exception, because a known exception is
        the grandfather OQ-6 refused, re-entering by the back door.
  - [ ] 5D.2a **One such ruling is foreseeable NOW and should be raised early
        rather than discovered at the gate.**
        `add-workbench-integrated-editor-chat` must stay headerless (5C.4),
        which means it stays a `status-validity` ERROR, which means 5D.2 can
        never read zero while the scan set reaches it. That is a real
        conflict between two correct rules and not a defect in either. Three
        shapes could resolve it — a recorded disposition for the one
        document, a ruling that overturns register entry A2, or a scan-set
        carve-out for a packet whose archive record refuses a status — and
        which one is right is Brett's call, not this change's. Do NOT pick
        one silently in order to make the gate green; a green gate bought
        that way measures the carve-out, not the corpus. Verify the chosen
        route actually suppresses the finding before relying on it:
        `health/dispositions.yaml` does not silence every family, so
        assuming it silences this one is the kind of unmeasured claim this
        change exists to stop.
        **RULED (2026-08-23, Brett, in-session): BACKFILL IT TOO.** The
        2026-08-02 decision's stated reason — "no post-archive vocabulary
        owns that field" — is dissolved by the promoted rule that now does
        own it, so the decision is superseded on its own terms rather than
        overturned. The supersession is recorded on the change (its
        bookkeeping note quotes the original decision word for word and
        leaves it standing) and in the register (entry A2 gains a dated
        supersession addendum; its original text stands). 5C.4's "must stay
        headerless" is amended accordingly, and no carve-out or disposition
        route is taken — the gate reads zero because the corpus satisfies
        the rule, not because a document was excused from it.
  - [ ] 5D.3 Only then does §2 land. §2 is the LAST slice of this change, not
        the first: the enforcement code merges onto a corpus that already
        satisfies it.

## 6. Explicitly out of scope

- [ ] 6.1 Whether `tasks.md`, `design.md`, spec delta files,
      `supporting-docs/` or `evidence/` are governance documents. 488 of the
      536 `status-validity` fires under full membership are these files, so
      this is the largest single question in the area and it deserves its own
      measurement rather than a ride on this one.
- [ ] 6.2 Widening `STATUS_SCAN_LINES` beyond fifteen real lines. Shared by
      `corpus.parse_status`, `families._header_lines` and
      `ideation_dashboard.generator._header_value`; moving it moves all three.
- [ ] 6.3 `record-immutability` over `openspec/`. Zero fires over the scan
      set today, and the family's "revert the content edit" remedy
      contradicts the archived-record append discipline, so wiring it is a
      ruling rather than a freebie. See design.md Decision 3.
- [ ] 6.4 The `location-conformance` and `tag-hygiene` false positives
      measured under full membership. They are not defects to fix here —
      under the ruled option those families never see the documents — but
      they are on the record in `proposal.md` for whoever revisits option (a).
