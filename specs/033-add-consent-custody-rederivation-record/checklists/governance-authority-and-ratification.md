# Checklist: Governance Authority and Ratification — 033-add-consent-custody-rederivation-record

**Purpose**: Release-gate audit of the §§ 0/1 bookkeeping claims this feature
makes or plans to make — whether every act named as "verifiably DONE" truly
is, whether every evidence note is anchored to a record and a timestamp,
whether Brett Heap's verbatim is quoted exactly and never extended, whether
the measured absence of a GitHub approving review on PR #774 is stated rather
than glossed, whether the eleven veto points are cited from the ratification
record rather than re-argued, whether the `3b530009` amendment form is
correctly specified for the packet preamble, whether ratified prose stays
frozen except the one permitted note, and whether the note-class arithmetic
(35 + 3 + 8 = 46) holds. This interrogates the WRITTEN requirements and the
CURRENT state of the cited artifacts — no §§ 2–5 realization act has been
taken yet, so no packet box is yet ticked; the check is whether the plan for
ticking is sound and whether every present-tense claim already in the tree is
true today.

**Artifacts under review**: `spec.md`, `plan.md`, `tasks.md`, `research.md`
(Speckit tree, `specs/033-add-consent-custody-rederivation-record/`);
`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`review/ratification-2026-09-08.md` (packet,
`openspec/changes/add-consent-custody-rederivation-record/`);
`tests/sequenced_after/corpus-ledger.yaml`; `README.md`.

**Date**: 2026-09-09. No-argument invocation — maximum coverage, no item cap.

## § 0.1 and § 1.1–1.3 — Evidentiary Sufficiency of "Verifiably DONE"

- [x] CHK001 Is "verifiably DONE" (FR-040) given an operational test — a note
      citing the record AND the timestamp — rather than left as a bare
      adjective an implementer must interpret unaided? [Clarity, spec.md
      FR-040]
- [x] CHK002 Is box 0.1's cited evidence (`tests/sequenced_after/corpus-ledger.yaml:82`
      reading `moved_by: "#774"`) actually present on this branch today, not
      merely asserted? MEASURED: `grep` over the ledger confirms the row reads
      exactly `{state: active, class: co-modifier, declares:
      [add-consent-instrument], depth: 1, prose: false, moved_by: "#774",
      moved_on: "2026-09-07"}`. [Traceability, research.md R11, tasks.md T070]
- [x] CHK003 Is box 1.1's cited evidence (`Status: ratified` on `proposal.md`,
      `design.md` and the packet's `tasks.md`, plus the `Ratified:`/`Ratified
      by:` line) actually present today? MEASURED: all three files carry
      `Status: ratified` and a ratification line naming 2026-09-08, Brett
      Heap, and the record path. [Traceability, research.md R11, tasks.md T071]
- [x] CHK004 Is the README OpenSpec Records row's "already flipped" claim
      (`README.md:848`) verifiably true today, not a forward reference to work
      this feature has not yet done? MEASURED: `README.md:847-848` reads
      `**\`Status: ratified\`** (2026-09-08, Brett Heap...`. [Traceability,
      research.md R11, tasks.md T071]
- [x] CHK005 Is a DISTINCT evidentiary standard given for each of boxes 0.1,
      1.1, 1.2 and 1.3 individually (a ledger row, a status/ratified-line
      triple, a veto-list citation, an operator-veto-section citation), rather
      than one generic "cite a record" instruction applied uniformly with no
      per-box specificity? [Completeness, tasks.md T070-T073]
- [ ] CHK006 Does the Speckit tree's own execution-order documentation agree on
      WHEN §0.1/§1.1–1.3 are ticked relative to the rest of the realization?
      `spec.md`'s "Primary flow, in one ordered narrative" states as step 1
      "§ 0.1 and § 1.1–1.3 are TICKED with evidence" — BEFORE step 2 (the
      schema grows) — while `tasks.md`'s Dependencies graph places Phase H
      (T070–T074, which perform those exact ticks) strictly AFTER Phase G
      (T060–T066, the cut), the last phase in the chain. — **FINDING:**
      `spec.md`'s Primary Flow step 1 and `tasks.md`'s Dependencies graph
      disagree on whether §0.1/§1.1–1.3 are ticked before or after §§2–5 are
      realized; an implementer following the numbered narrative would tick
      early, one following the phase graph would tick last, and nothing
      reconciles the two orderings. [Consistency, spec.md "Primary flow"
      step 1 / tasks.md Dependencies graph]
- [x] CHK007 Is a box's evidence permitted to be a citation of an act performed
      in an EARLIER commit (6cfe9ba6 for 0.1; the ratification record's own
      commit for 1.1–1.3) while the tick itself lands in a LATER commit,
      without that being read as violating FR-041's "same commit as its
      evidence"? Read together with FR-042 (the evidence NOTE is written to
      `evidence/` at tick time) the rule binds the WRITTEN NOTE and the tick,
      not the underlying act's own historical commit. [Ambiguity, spec.md
      FR-041/FR-042]

## Ratification Citation Fidelity

- [x] CHK008 Does the ratification citation identify the SAME baseline commit
      (`6cfe9ba6628b21649953c83c5b4fe1ade1eda76c`) everywhere it recurs —
      `spec.md` header, `review/ratification-2026-09-08.md`? MEASURED:
      identical in both. [Consistency, spec.md header / ratification record]
- [x] CHK009 Is the PR number (#774) and its head sha (`ab27744b`) cited
      identically in `spec.md`, `research.md` R12 and the ratification
      record's "Review this record rests on" table (round 4, head `ab27744b`)?
      [Consistency, spec.md/research.md R12/ratification record]
- [x] CHK010 Does `spec.md` distinguish the TWO CLAUSES of the ratifier's word
      ("ratify 774" vs "merge it and land it") the same way the ratification
      record does — one as the approval, one as an order to proceed, not
      part of the approval — rather than treating the whole sentence as a
      single undifferentiated act? [Precision, spec.md header / ratification
      record "Decision" section]
- [x] CHK011 Is the packet's own "RATIFICATION HYGIENE" claim ("heard and
      recorded by the same lane, nothing relayed") carried into `spec.md`'s
      citation in substance, so a reader of `spec.md` alone knows the record
      is first-hand and not a relayed summary? MEASURED: `spec.md` line
      27-28 states this explicitly. [Traceability, spec.md/ratification
      record "Ratification hygiene"]
- [x] CHK012 Is "THE RATIFIED PACKET IS THE AUTHORITY, NOT THIS FILE" backed
      by an operational consequence (the packet governs on conflict, and this
      file is the defect), rather than asserted once with no stated
      resolution procedure? [Gap, spec.md Preamble]

## Verbatim Quotation Discipline — Never Extended

- [x] CHK013 Is the ratifier's verbatim — *"ratify 774, merge it and land
      it"* — byte-identical across every citing document? MEASURED: `grep`
      confirms identical text (modulo line-wrap) in `spec.md:13`,
      `proposal.md:11`, `design.md:4`, `tasks.md:4` (packet),
      `review/ratification-2026-09-08.md:9,32`, and `README.md:850`. No
      citation adds or drops a word. [Precision, all cited files]
- [x] CHK014 Does any citation of the ratifier's word extend it with words the
      record does not carry — for example, appending an unquoted
      justification inside the quotation marks? MEASURED: every citation
      closes the quotation at "land it" with no appended text inside the
      quote marks. [Precision, all cited files]
- [x] CHK015 Is the F.1 origin ruling's verbatim — *"Bump the openxFactory
      instrument schema first"* plus its second sentence — quoted
      identically in `proposal.md`, `design.md`/`.openspec.yaml`'s `origin`
      block, and `README.md`, with no citing document inventing a clause the
      OpsxFactory PR #248 comment does not carry? [Consistency,
      proposal.md/.openspec.yaml/README.md]
- [x] CHK016 Where `spec.md` and `tasks.md` (Speckit) reference the
      ratification record's own sentences (*"no veto was exercised on any of
      the eleven"*, *"Task 1.3's operator veto was NOT exercised"*) via T072
      and T073, are those reproduced as EXACT quotations of the record's
      wording rather than paraphrase presented as quotation? MEASURED:
      `review/ratification-2026-09-08.md` line 101-102 reads "no veto was
      exercised on any of the eleven" and the heading at line 88 reads
      "Task 1.3's operator veto was NOT exercised" — both match T072/T073
      word-for-word. [Precision, tasks.md T072/T073, ratification record]
- [x] CHK017 Is there a stated prohibition against a future note attributing
      to Brett Heap words he did not say — analogous to the sibling feature's
      "MUST NOT quote a word" rule for an empty approval body — given here as
      "A note that cites a GitHub approval where none was given would be a
      false record, so no note in this feature does" (spec.md line 36-37)?
      [Gap-closure, spec.md Preamble]

## The Measured Absence of a GitHub Approving Review (research.md R12)

- [x] CHK018 Is the absence of an `APPROVED` review on PR #774 stated as a
      MEASUREMENT (a named command and its exact returned state) rather than
      an inference or a gloss? MEASURED: `spec.md` lines 18-21 name the exact
      command (`gh api repos/opensoft/openxFactory/pulls/774/reviews`) and
      its exact return (one review, `sourcery-ai[bot]`, `COMMENTED`,
      `2026-09-08T03:26:05Z`, head `ab27744b`), matching research.md R12
      verbatim. [Measurability, spec.md Preamble / research.md R12]
- [x] CHK019 Is the CONTRAST with the immediately preceding realization
      (`specs/032`, which COULD cite a CLI approval) drawn explicitly, so a
      reader cannot mistake this feature's citation gap for an oversight
      rather than a measured difference? MEASURED: `spec.md` lines 21-24 and
      `research.md` R12 both draw the contrast with review `5141756427`,
      APPROVED `2026-09-08T12:38:36Z`. [Consistency, spec.md/research.md R12]
- [x] CHK020 Is the SUBSTITUTE evidentiary chain (the in-repo ratification
      record, Brett Heap's own merge `merged_by: brettheap`, `merged_at:
      2026-09-08T03:48:44Z`, merge commit `543d47a9…` over head `0d541576`,
      and the LANDING/LANDED comments) named as what every § 1 note actually
      cites, closing the gap left by the absent approval rather than leaving
      it unaddressed? [Completeness, spec.md lines 25-34]
- [x] CHK021 Does the "operator's act, not a self-merge" reasoning (the PR was
      authored by `openxfactory[bot]`, so Brett Heap's merge is not a
      self-merge of his own authorship) appear wherever the merge is cited as
      evidence, so the substitution is not merely asserted but justified?
      [Precision, spec.md lines 29-32]
- [x] CHK022 Is task 1.1's planned tick-note (T071) required to carry the
      SAME "measured absence" framing as `spec.md`'s Preamble, so the
      eventual packet-tasks.md note does not silently drop the distinction
      and read as though an approval existed? MEASURED: T071 states "The
      citation states the MEASURED absence of a GitHub approving review
      (`research.md` R12)". [Traceability, tasks.md T071]

## Veto-Point Citation Discipline — Cited From the Record, Not Re-Decided

- [x] CHK023 Are the eleven veto points (C-1 through C-10 plus C-6a) counted
      identically in the packet's own `tasks.md` § 1.2, the ratification
      record's "What was ratified" section, and this feature's Speckit
      `tasks.md` T072/T073? MEASURED: all three name exactly eleven —
      C-1, C-2, C-3, C-4, C-5, C-6, C-6a, C-7, C-8, C-9, C-10. [Consistency,
      packet tasks.md § 1.2 / ratification record / Speckit tasks.md]
- [x] CHK024 Does T072's tick note CITE the ratification record's veto-list
      conclusion rather than RE-STATE the eleven decisions' substance in the
      implementer's own words (which would risk re-arguing a settled
      question)? MEASURED: T072 reads "TICK with evidence: the ratification
      record's '...no veto was exercised on any of the eleven' rules all
      eleven veto points as written. Quote it exactly — never more." — this
      is a citation instruction, not a re-decision. [Precision, tasks.md T072]
- [x] CHK025 Does T073's tick note likewise cite (rather than re-derive) the
      ratification record's specific finding that C-10's supersession of the
      F.1 ruling clause was NOT vetoed, so the default (no `amendments`
      entry, three instruments stay `executed`) stands on the record's own
      words? [Precision, tasks.md T073, ratification record lines 88-102]
- [x] CHK026 Is there anywhere in `spec.md`, `plan.md` or the Speckit
      `tasks.md` a clause that ADDS a NEW justification for one of the eleven
      decisions not present in `design.md` or the ratification record — which
      would be a re-decision rather than a citation? MEASURED: no such
      addition found; every reference to C-1..C-10/C-6a in the Speckit tree
      points back to the packet's `design.md`/ratification record rather than
      arguing the point independently. [Completeness, cross-document review]
- [x] CHK027 Is it stated that a VETO exercised after this feature's ticks
      land would require a correction, and is the mechanism for that named
      (an amendment in the `3b530009` form, per FR-044's general rule) rather
      than left silent? [Recovery, spec.md FR-044]

## The `3b530009` Amendment Form and Same-Commit Discipline

- [x] CHK028 Does FR-044's stated form (block-quote the superseded sentence,
      name the un-superseded neighbour, marker `AMENDED <UTC date>`, tick
      marker `**TICKED <UTC date>`) match the actual shape of precedent
      commit `3b530009`? MEASURED: `git show 3b530009` shows exactly this
      shape — a restated header naming "ONE NAMED SENTENCE ABOVE IS
      SUPERSEDED", the superseded sentence block-quoted, and the sentence
      before it explicitly declared NOT superseded. [Precision, spec.md
      FR-044, commit 3b530009]
- [x] CHK029 Does T074 (the packet preamble amendment) correctly incorporate
      the LESSON of `3b530009` — naming the un-superseded neighbour
      explicitly, which is the exact defect that commit was written to fix
      (a prior round's amendment omitted naming which sentence was
      superseded) — rather than repeating the omission the precedent
      corrects? MEASURED: T074 requires "block-quote the superseded
      sentence, name the un-superseded neighbour, marker AMENDED 2026-09-09".
      [Traceability, tasks.md T074, commit 3b530009's own commit message]
- [x] CHK030 Is "the SAME commit as the first tick" (T074) unambiguous about
      WHICH tick is "first"? Given Speckit `tasks.md` lists T070 (box 0.1)
      before T071–T073 (boxes 1.1–1.3) inside the same Phase H section, and
      §0 numerically precedes §1 in the packet's own list, "the first tick"
      resolves to box 0.1's tick unless all four (0.1, 1.1, 1.2, 1.3) land in
      one combined commit, in which case the amendment rides that same
      combined commit. [Ambiguity, tasks.md T074/T070-T073]
- [x] CHK031 Is the SPECIFIC preamble sentence T074 targets — *"NOTHING BELOW
      IS DONE. EVERY BOX IS UNTICKED, AND THAT IS THE STATE OF THE PACKET
      RATHER THAN AN OVERSIGHT."* — quoted precisely enough in T074 that an
      implementer could not amend a neighbouring sentence (*"This is a
      PROPOSAL. No schema byte moves..."*) by mistake? MEASURED: T074 quotes
      the opening clause verbatim. [Precision, tasks.md T074, packet
      tasks.md line 7-8]
- [ ] CHK032 Is the "un-superseded neighbour" for the packet preamble amendment
      itself named anywhere in the Speckit tree, the way `3b530009` named
      *"NOTHING IS TICKED THAT DID NOT LAND"* as its neighbour? — **FINDING:**
      neither `spec.md` nor `tasks.md` names which sentence of the packet
      preamble (the "This is a PROPOSAL..." sentence, or some clause within
      it) is the un-superseded neighbour for T074's amendment; T074 restates
      the FORM's requirement ("name the un-superseded neighbour") but does
      not itself do the naming, leaving that judgment call for execution
      time. [Gap, tasks.md T074]

## Frozen Ratified Prose and the One Permitted Note

- [x] CHK033 Is the frozen set (`proposal.md`, `design.md`, `.openspec.yaml`,
      the spec delta) enumerated IDENTICALLY in `spec.md` FR-043, `plan.md`'s
      Constitution Check table, and Speckit `tasks.md` T077? MEASURED: all
      three name the same four items. [Consistency, spec.md FR-043/plan.md/
      tasks.md T077]
- [x] CHK034 Is the ONE permitted exception (a single additive dated
      realization note after `proposal.md`'s `Lane:` line) reconciled with
      the general freeze rule rather than reading as a self-contradiction —
      FR-043's first sentence freezes `proposal.md`, its second sentence
      carves out exactly one permitted edit to it? MEASURED: the two
      sentences are read together consistently (freeze except the one named
      exception), matching `plan.md`'s Constitution Check phrasing "untouched
      except ONE additive dated realization note". [Conflict, spec.md
      FR-043]
- [x] CHK035 Is the CONTENT the permitted note may correct scoped precisely
      (an enumeration this realization falsifies — specifically the "every
      box in `tasks.md` stays unticked" sentence) rather than left open to
      any correction an author judges convenient? [Precision, spec.md
      FR-043, tasks.md T077]
- [x] CHK036 Is it explicit that `design.md`, `.openspec.yaml` and the spec
      delta receive NO edit under any circumstance in this realization — not
      even the one permitted note's mechanism — distinguishing them from
      `proposal.md`? MEASURED: T077 states "`design.md`, `.openspec.yaml` and
      the delta stay frozen" immediately after describing the one permitted
      proposal.md note. [Precision, tasks.md T077]
- [x] CHK037 Is `tasks.md` (the packet's) correctly EXCLUDED from the "frozen
      ratified prose" set, given it is the one document this realization is
      expressly licensed to tick and amend (FR-043's "tasks.md, the evidence
      file, and ONE additive dated realization note... are the only
      permitted edits")? [Consistency, spec.md FR-043]

## Note-Class Arithmetic (35 + 3 + 8 = 46)

- [x] CHK038 Does the packet's own box count (46, by section: §0:1, §1:3,
      §2:5, §3:7, §4:16, §5:6, §6:5, §7:3) sum correctly? MEASURED:
      1+3+5+7+16+6+5+3 = 46, matching `spec.md`'s Measured baseline table and
      an independent count of the packet's own `tasks.md` checkbox lines.
      [Measurability, spec.md Measured baseline / packet tasks.md]
- [x] CHK039 Does the TICKED-here set (35: §0.1; §1.1–1.3; §2.1–2.5;
      §3.1–3.5 incl. 3.4b/3.4c; §4.1–4.9 incl. 4.1b/4.1c/4.3b/4.3c/4.8b/4.8c/
      4.8d; §5.2–5.4) sum to exactly 35? MEASURED: 1+3+5+7+16+3 = 35,
      matching the Speckit `tasks.md` Box Accounting table exactly.
      [Measurability, tasks.md Box Accounting table]
- [x] CHK040 Does the NOT-OWED-HERE set (§5.1, §5.5, §5.6 = 3) and the
      NOT-OWED set (§6.1, §6.2, §6.2b, §6.3, §6.4, §7.1, §7.2, §7.3 = 8) each
      sum correctly and sum together with the 35 TICKED to exactly 46?
      MEASURED: 3 + 8 = 11; 35 + 11 = 46. [Measurability, tasks.md Box
      Accounting table]
- [x] CHK041 Is the arithmetic assertion required to be RE-VERIFIED in the
      evidence file at execution time (T076: "Assert the arithmetic in the
      evidence file"), rather than trusted once at planning time and never
      re-checked against the actual ticked state? [Measurability, tasks.md
      T076, spec.md SC-002]
- [x] CHK042 Is the distinction between "NOT-OWED-HERE" (owed by the SAME
      lane, later — §5.1, §5.5, §5.6) and "NOT-OWED" (owed by a DIFFERENT
      party entirely — §§6-7) maintained consistently everywhere the two
      classes are named, so a reader cannot mistake one class for the other?
      MEASURED: `spec.md` Measured baseline table, Out of scope section, and
      `tasks.md` Box Accounting table all preserve the distinction. [Clarity,
      spec.md/tasks.md]

## False-Record Class

- [x] CHK043 Could any planned tick note, as specified, be satisfied by an
      agent's own unverified assertion with no independent durable record
      (a commit sha, a review id, a ledger row) behind it? MEASURED: every
      one of T070–T073's planned notes names an independently checkable
      artifact (a commit sha, a file's `Status:` line, a named record's
      heading) rather than an assertion alone. [Completeness, tasks.md
      T070-T073]
- [x] CHK044 Is there a standing rule (not only the Preamble's one-line
      assertion) preventing a future note from inventing a GitHub approval,
      a veto, or a quotation that the cited record does not carry? MEASURED:
      spec.md's Preamble states the rule in terms broad enough to cover any
      note in the feature ("no note in this feature does"), and FR-040
      requires every note to cite "the record and the timestamp", which
      forecloses an uncited assertion by construction. [Gap-closure, spec.md
      Preamble/FR-040]
