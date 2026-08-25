# Tasks: add-projection-title-uniqueness

**§1 is COMPLETE — ratified 2026-08-25.** Nothing under §2 or later has run:
its diff, at the moment of ruling, was spec text, records, and this list. The
in-session authorization behind the packet covered RAISING the proposal
against a measured defect and nothing more; Brett then read it and ruled
OQ-1 through OQ-4 in one multiple-choice round, adopting the recommendation
throughout and folding OQ-4 into OQ-1. The ruling is recorded question by
question in `proposal.md` § Open Questions; the four decisions in § Orchestrator
Decisions were read in the same pass and none was vetoed. The six read-backs
are in §1.1–1.6 below.

**§5 is deliberately OPEN and stays open.** What this change does not close is
recorded there rather than implied.

## 1. Ratification and open questions

- [x] 1.1 Brett reads the measurement and rules on **Q1, the rule candidate**.
      The recommendation is (a), collision-triggered minimal repository-relative
      suffix: 14 renames and 28 book operations against 611 and 1222 for the
      always-fully-qualified alternative, both reaching zero collisions. (b1)
      and (c) are eliminated on CORRECTNESS by measurement — each leaves a live
      collision — and the elimination is in `design.md` § 4 with the reason.
      Ruling (b2) instead is an edit to the delta's third paragraph and to
      §§ 2.1–2.2, not a new change.
      **RULED 2026-08-25: recommendation adopted — (a) at REPOSITORY scope,
      folding Q4's scope sub-question into the same pick (`proposal.md` §
      Open Questions).** 14 renames, 28 operations, zero collisions, and the
      three latent pairs close as a side effect.
- [x] 1.2 Rule on **Q2, whether the migration rides the realization's own sync
      slice**. §4 is written for ONE SLICE: the realization merges and an
      apply-mode sync follows immediately, so the books are correct on merge
      and the archive evidence exists at once. The alternative leaves the books
      visibly drifted — `notebook-projection-drift` reporting 28 pending
      operations — until a separately scheduled apply.
      **RULED 2026-08-25: recommendation adopted — one slice, as § 4 already
      assumes.** No drift window opens; § 4 needs no edit.
- [x] 1.3 Rule on **Q3, whether the arrival of five never-projected documents
      warrants a record** beyond this packet. Three MedxFactory staging topics,
      one openxFactory draft checklist and one OpsxFactory staging fragment
      have never held a source; every answer any book gave about those subjects
      was given from a corpus missing them. If a record is owed, the place is
      `docs/archive-record-discrepancies.md`.
      **RULED 2026-08-25: a record is owed.** A dated, append-only entry in
      `docs/archive-record-discrepancies.md`, written at realization (§ 4
      below), not now.
- [x] 1.4 Rule on **Q4, the uniqueness scope**. Repository scope costs four of
      the fourteen renames and pre-empts the three latent pairs
      (`memory-gateway/README`, `company-provisioning`,
      `codexfactory-domain-hermes-content`), each of which is one `Status:`
      edit from a live collapse. The tightest correct scope is eight renames
      and leaves them latent. `design.md` § 7 measures all three scopes.
      **RULED 2026-08-25: folded into 1.1 above — no independent ruling.**
      Repository scope stands, ruled as part of Q1.
- [x] 1.5 NO `document-lifecycle` delta, and the absence is deliberate. This
      change states an obligation about a PROJECTION — that a derived source
      set be injective over the documents it derives from — not about how
      documents carry lifecycle state. The obligation belongs in
      `lifecycle-notebook-projection` and nowhere else.
      **Confirmed by the ratification read, 2026-08-25: unvetoed.**
- [x] 1.6 NO `Projection capacity guard` delta, and the absence is MEASURED
      rather than assumed. That requirement defines projected occupancy over
      "the desired managed set plus the charter plus every unmanaged source",
      and the implementation counts DOCUMENTS for it. No guard-computed number
      moves; actual occupancy rises to meet the number the guard already used.
      `design.md` § 8 carries the per-book table.
      **Confirmed by the ratification read, 2026-08-25: unvetoed.**

## 2. Realization — the derivation

- [x] 2.1 `scripts/sync-notebooklm-books.py`: replace the one-line `README`
      conditional in `scan()` with a repository-scoped uniqueness pass. Two
      steps, in this order, because the scan visits repositories one at a time
      and uniqueness is a property of the finished set: collect each projected
      document's repository-relative segments during the walk, then resolve
      titles once the walk is complete. A document's qualifier is the shortest
      path suffix that distinguishes it from every other projected document of
      the same repository; a `README` stem floors at two segments, preserving
      every title today's rule already produces except where that rule was
      itself ambiguous.
      **DONE 2026-08-25.** `scan()` is now two passes over one walk: it
      collects `(relpath, repository, status, segments)` and hands the
      projected documents to a new `derive_stems()`, which resolves every stem
      repository by repository. `title_segments()` carries the repository
      DIRECTORY as its outermost segment, so a repository-root `README.md`
      floors at `<repo>/README` — byte for byte the title `f.parent.name`
      produced. The injectivity is structural, not observed: two documents can
      only stop at the same suffix string if they stopped at the same DEPTH,
      and at that depth neither would have found the suffix unshared; a
      document that never finds one falls back to its whole segment path,
      which is unique by construction. Re-derived over the ten-repository
      scratch assembly the design was measured on, the change moves exactly
      the fourteen titles of `design.md` § 6 and no others, and leaves zero
      collisions where the replaced rule left three.
- [x] 2.2 The `[spec]` and `[grounding]` families stay outside the uniqueness
      scope. Both are keyed by something other than a file stem and neither
      collides; measurement showed that including them over-qualified one
      `drafts` title for no reason. Pin the exclusion in code with the reason,
      not as a silent filter.
      **DONE 2026-08-25.** `STEM_SCOPE_EXCLUDES` names both families in code
      with the measurement that eliminated the alternative. A second scope
      boundary was found while implementing and is pinned the same way:
      `PROJECTED_STATUSES`. A `record`, `superseded` or `retired` document is
      scanned and reaches NO book, so it is not a projected document and must
      not cost a projected namesake its bare stem — `scan()` now drops it
      before the uniqueness pass rather than after, and
      `test_a_record_document_qualifies_nobody` holds that boundary.
- [x] 2.3 `parity_report()`: compare at the document level. Report a derived
      title carrying more than one path key as a parity FAILURE naming the
      documents, and stop reporting a book as at parity on title-set equality
      alone. This is the check that could not see the defect it existed to
      catch; the amendment is what makes the next instance loud.
      **DONE 2026-08-25.** The mode now builds `{title: [relpaths]}` per book
      from the desired map and reports every title carrying more than one
      document as `PARITY FAIL … COLLAPSED <title>` followed by the paths, on
      the CORPUS alone — no provider call is needed to see it. Title-set
      equality is no longer sufficient: the `PARITY OK` line requires an empty
      collapse set as well, and now reads in documents rather than in titles.
- [x] 2.4 `docs/lifecycle-notebook-projection.md` § 2: replace the
      "Title rule for ambiguous stems" paragraph with the injective rule, and
      add the `Amended by:` line the doc's header convention requires. Note in
      passing that the sentence being replaced already stated the general rule
      in its parenthesis — "or otherwise non-unique within a repo" — and that
      the implementation implemented the example instead. That is the shape of
      failure worth recording where the next reader will meet it.
      **DONE 2026-08-25.** Section 2 now opens with the identity-key
      mechanism — why a shared title is one source and not two — then states
      the shortest-distinguishing-suffix rule, the repository scope, the
      `README` floor, and the two excluded families. The closing paragraph
      records the failure shape where the next reader meets it: the
      parenthesis stated the general obligation and the implementation
      implemented the example. The header carries
      `Amended by: add-projection-title-uniqueness (ratified 2026-08-25)`.

## 3. Tests

- [x] 3.1 A collision fixture covering the three real shapes this corpus
      contains, not one generic pair: several documents sharing a stem inside
      one directory family (`ideation/staging/<topic>/topic.md`, four of them);
      two documents whose PARENT directories also match
      (`specs/<id>/checklists/requirements.md`, which is the case that
      eliminates a one-level qualifier); and a pair split across two directory
      families (`ideation/brainstorm/<slug>.md` against
      `ideation/staging/<slug>/<slug>.md`).
      **DONE 2026-08-25.** `TitleUniquenessTests._world` writes all three
      shapes at their REAL paths, plus the latent `memory-gateway/README` pair
      that the replaced rule was itself ambiguous about, plus five documents
      that must not move: a lone `topic.md` in OpsxFactory, a unique
      `ideation/README.md`, a repository-root `README.md`, a `record`
      namesake, and a governance document whose stem is a promoted
      capability's directory name.
- [x] 3.2 An INJECTIVITY assertion over the whole derived set, per book:
      `len(set(desired[book].values())) == len(desired[book])`. This is the
      assertion whose absence let the class exist. It must be written over the
      derived set rather than over the fixture's expected titles, so a future
      derivation change cannot satisfy it by agreeing with itself.
      **DONE 2026-08-25.** `_assert_injective()` reads only the derived map,
      never the expected-title table, and it is ONE method so the mutation
      check in 3.6 runs that assertion rather than a paraphrase of it.
- [x] 3.3 A STABILITY assertion: change a fixture document's `Status:` header
      and assert that no other document's title moves. This pins the
      repository-scope choice structurally — under a (book, status) scope this
      test fails, which is the point.
      **DONE 2026-08-25.** `test_a_status_change_moves_no_other_title` flips
      `examples/memory-gateway/README.md` from `draft` to `standard` and
      asserts every other document's title is byte-identical, and that the
      moved document keeps its own qualifier. Verified to be the pin it claims
      to be: with the scope narrowed to (repository, status) it reds, together
      with the § 6 enumeration test.
- [x] 3.4 A parity-blindness regression: build a state with a collapse present
      and assert `parity_report` reports FAILURE. Written against the old
      behaviour it must fail; that is the acceptance evidence for §2.3.
      **DONE 2026-08-25.** `ParityProvesDocumentsTests` builds the exact state
      the old check passed — a live account whose bracket-titled sources are
      set-equal to the derived titles — under the reverted derivation, and
      asserts first that the two title sets ARE equal and then that parity
      returns 1 naming the collapsed documents. The assertion on set equality
      is what makes it a regression against the old behaviour rather than a
      new test that happens to pass.
- [x] 3.5 A FLOOR assertion: a `README` that is unique in its repository still
      carries its parent directory, so the amendment never SHORTENS an existing
      title. Measurement caught a prototype doing exactly that.
      **DONE 2026-08-25.** The assertion runs over EVERY derived README in the
      fixture, not one named case: each carries at least two segments, and its
      last two segments equal what the replaced rule produced — which for a
      repository-root README is `<repo>/README`, the case a naive
      repository-relative segment list would have shortened.
- [x] 3.6 Mutation checks on the assertions that carry the guarantee, chosen
      against the classes this repository has been bitten by. (i) Break
      injectivity — revert the derivation to the bare stem — and confirm 3.2
      reds; an assertion that passes against the defective derivation is not
      the assertion. (ii) Weaken the qualifier to one level and confirm the
      `checklists/requirements` case reds; this is the platform-inert class in
      disguise, where a change that looks like a fix leaves the value equal.
      (iii) Assert on the derived STRUCTURE, not on rendered strings alone, so
      a path-separator or `str(Path)` substitution cannot survive a
      value-equality check.
      **DONE 2026-08-25, and run out of tree as well as in it.** (i) and (ii)
      are standing tests that drive the defective derivations directly, so
      they cannot rot. Both were also run as REAL source mutations against the
      shipped file: reverting `derive_stems` to the bare stem reds 8 cases
      including 3.2; narrowing the uniqueness scope to (repository, status)
      reds exactly 2 — the stability assertion and the § 6 enumeration — which
      is the latent-pair claim and nothing else. (iii)
      `test_titles_are_derived_from_structure_not_from_a_rendered_path`
      asserts the segment TUPLE, that no segment contains a separator in
      either direction, and that the checklist qualifier is three segments
      deep because two still collide.
- [x] 3.7 Run the whole `tests/notebooklm` suite, not the new file alone: 94
      existing cases read `scan()` output and several assert on exact titles.
      Any of them that must move is evidence about the migration's blast
      radius and belongs in the §4 record.
      **DONE 2026-08-25 — 129 passed, 13 subtests, and NOT ONE existing case
      had to move.** That is itself evidence about the blast radius: every
      title in the existing fixtures was already unique in its repository, so
      the amendment is invisible to them, exactly as a collision-triggered
      rule should be.

## 4. The sync that migrates the books, and the archive gate

The defect is a discrepancy between a manifest and a provider. Only the
provider can say it closed, so the archive evidence is a provider read and not
a test run.

- [x] 4.1 Dry run first, from the workspace root, and diff the plan against
      `design.md` § 6: exactly 14 renames — 28 `DEL`/`ADD` lines — plus the 5
      adds that un-collapse the three collisions. A plan that differs from the
      enumerated list by even one line stops the apply and is investigated
      before anything is applied.
      **DONE 2026-08-25, and the plan matched § 6 row for row — but NOT the
      line count this box predicts, and the difference is this box's
      arithmetic rather than the plan's.** The dry run planned **14 `ADD`, 9
      `DEL`, 3 `UPD`**. The 14 adds are § 6's fourteen new titles, one per row,
      in the enumerated spelling. The DELs are 9 and not 14 because three of
      the vacated titles were COLLAPSED ones: `[staged] MedxFactory: topic`
      stood for four documents but only ever held ONE live source, so four
      renames vacate one source, not four. "28 ops" in `design.md` § 4 is
      `2 × renames`, which over-counts the delete side of exactly those three
      titles; the source arithmetic in § 8 (695 → 700) is unaffected and was
      met exactly. The three UPDs are content-only and none is a title change:
      `[standard] openxFactory: lifecycle-notebook-projection` is this slice's
      own § 2.4 edit, and `[draft] openxFactory: CHANGELOG` plus
      `[ratified] openxFactory: contract-versioning-policy` are main-line drift
      from `ffdca83f` (contract-v1.42) that the books owed regardless. Nothing
      else appeared, and no document entered or left a book: the corpus was
      re-derived from this branch's own tree over the ten-repository assembly,
      and the desired set moved by the 14 titles and by nothing else.
- [x] 4.2 Apply. The books move from 695 sources to 700: `drafts` 188 → 189,
      `ideation-medxfactory` 49 → 52, `ideation-opsxfactory` 16 → 17, and the
      four unaffected books unchanged (`canon` 114, `ideation-openxfactory`
      247, `ideation-ledgerxfactory` 66, `ideation-codexfactory` 15).
      **DONE 2026-08-25, exit 0, executing the dry run's plan line for line.**
      One transient on an OpsxFactory add cleared on the built-in single retry.
      One artifact needed a hand repair and it is recorded rather than
      smoothed over: `contracts/CHANGELOG.md` exceeds `MAX_TEXT_ARG_BYTES`, so
      its UPD rode the temp-file path, and the rename that path performs to
      restore the contract title did not take — the source landed titled by its
      temp FILENAME. This is the known oversized-source readiness race, not a
      consequence of this change (`add_text_source` is untouched here), and the
      code's own error text prescribes the remedy taken: renamed by hand to
      `[draft] openxFactory: CHANGELOG`, verified by re-listing the book. All
      seven books were then swept for stray non-bracket titles and the drafts
      book's was the only one.
- [x] 4.3 Read the counts back from the provider and record them. This is the
      evidence, and it is the same read that produced the "before" column, so
      the two are comparable by construction.
      **DONE 2026-08-25 — all seven books at the predicted number, total 700.**
      `canon` 114 → 114, `drafts` 188 → **189**, `ideation-openxfactory` 247 →
      247, `ideation-ledgerxfactory` 66 → 66, `ideation-medxfactory` 49 →
      **52**, `ideation-opsxfactory` 16 → **17**, `ideation-codexfactory` 15 →
      15. Total **695 → 700**, the five sources that never existed. The
      manifest re-keyed exactly 14 rows to a new title and gained none: its row
      counts per book are unchanged, which is the other half of the discrepancy
      closing — the rows were always there, and now each one has a source.
- [x] 4.4 Run `--parity` under the amended rule and record it clean. A parity
      pass taken BEFORE §2.3 lands proves nothing about this defect — that is
      the whole finding — so the run that counts is the one after.
      **DONE 2026-08-25 — `parity: PROVEN`, exit 0, under the amended rule.**
      Every book reports in DOCUMENTS now, and each line reads N documents in N
      titles: canon 113/113, drafts 188/188, openxFactory 246/246,
      LedgerxFactory 65/65, MedxFactory 51/51, OpsxFactory 16/16, codexFactory
      14/14. The equality of those two numbers is the injectivity, made visible
      on the surface that could not previously see it. Union: 675 derived
      titles, 675 live managed titles, 0 unprojected, 0 unaccounted.
- [x] 4.5 Confirm `notebook-projection-drift` returns to zero pending
      operations. Between the merge and the apply it reports 28; a non-zero
      count after the apply means the plan and the provider disagree.
      **DONE 2026-08-25 — a convergence dry run over the applied state plans
      ZERO operations.** That is the count the family reads: it greps the
      sync's own `[book] ADD|DEL|UPD` lines. The first convergence run was NOT
      clean — it planned one `ADD`, and it was right to: that is the run that
      caught the CHANGELOG source sitting under its temp filename in § 4.2. The
      repair was made and the run repeated to zero. A convergence check that
      had been assumed rather than run would have left a mistitled source in
      the drafts book.
- [x] 4.6 Gates green: `python3 -m pytest tests/notebooklm tests/doc-health`,
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and a doc-health
      single-repo run whose severity counts move by exactly what §2 predicts,
      which is by nothing.
      **DONE 2026-08-25.** `tests/notebooklm` 129 passed with 13 subtests;
      `tests/doc-health` 895 passed with one deselection,
      `test_derivation_reproduces_the_real_bootstrap_clusters`, which fails
      identically on the untouched main checkout at `8fe986f0` and reads only
      `ideation/cross-reference.yaml` and a `git archive` of `ideation/` at its
      pinned revision — nothing this change touches. `openspec validate --all
      --strict` 77 passed, 0 failed. `promotion-fidelity` 0 findings.
      Doc-health single repo, before **5 critical, 5 error, 46 warning, 4
      info** and after **5 critical, 5 error, 43 warning, 4 info**. The
      prediction of "by nothing" held for every severity this change can move:
      the three warnings that left are `proposal-origin` on
      `add-model-provider-broker`, `add-nightly-dashboard-refresh` and
      `add-omnigent-domain-terminology`, closed by main's own `1abbe5fb` and
      inherited by the rebase, and the finding lists were diffed line by line
      to say so rather than inferred from the totals. Criticals did not move,
      including for the register edit:
      `docs/archive-record-discrepancies.md` already carried a standing
      `record-immutability` critical of class `contested` BEFORE this entry —
      read out of the baseline report, not assumed from the rule.
- [ ] 4.7 Archive on that evidence. `target_release: implemented` cuts no
      contract bundle, so the gate is merge-plus-green PLUS §§ 4.3–4.5.
      **Not yet: §§ 4.3–4.5 are in hand, merge is not.** This slice ships the
      realization, the migration and the record; the archive box stays open
      until the branch merges green on main.
- [x] 4.8 Write the record ruling 1.3 owes, in
      `docs/archive-record-discrepancies.md`. The ruling put it here rather
      than at proposal time because the record documents what the migration
      DID, and § 4 is where the migration happens.
      **DONE 2026-08-25.** A dated, append-only addendum in the shape that
      register already carries: the mechanism and why three separate artifacts
      all reported the books whole, the three collapse groups with the window
      each was open (MedxFactory 2026-08-04 → 2026-08-25, 21 days;
      openxFactory's checklist pair 2026-08-15 → 2026-08-25, 10 days;
      OpsxFactory 2026-07-23 → 2026-08-25, 33 days, dated from the commit that
      flipped the brainstorm document to `Status: staged` and so created the
      collision), the claim that every answer those books gave in those windows
      came from a corpus missing the documents, and what closed it. Two things
      it deliberately does NOT claim: which document of each group held the
      source, which is unrecoverable (§ 5.4) and is named as unrecoverable
      rather than guessed; and that the class cannot recur, since § 5.2's gap
      is real and is cited from the entry rather than papered over.

## 5. Recorded, not closed

- [ ] 5.1 **Titles remain collision-dependent under the recommended rule.**
      Adding a colliding document later renames the incumbent; removing one
      un-qualifies the survivor. `design.md` § 5 measures the exposure — 13
      recurring stems across 675 documents, most of them structurally unable to
      collide within one repository — and records variant (a′), manifest-pinned
      monotonic qualification, as the fix that is NOT taken here because it
      would put identity state in a file that is today a deletable cache.
- [ ] 5.2 **Nothing checks injectivity outside the sync's own test suite.**
      The parity amendment catches it when parity is run; no doc-health family
      does. A `notebook-projection-drift`-adjacent family that reports a
      non-injective derivation from the corpus alone — no provider call — is a
      named candidate and is not built here.
- [ ] 5.3 **The manifest is never pruned.** Measurement found 227 rows for
      `drafts` against 188 projected documents: rows for documents that left
      the book long ago. Harmless to reconciliation and misleading to anyone
      reading the manifest as a record of what a book holds — which is exactly
      how this defect was first read. Not this change's scope.
- [ ] 5.4 **Which document's CONTENT survived a collapse is unrecoverable.**
      The surviving source carries whichever document won a race whose order
      depended on provider listing order across runs. The migration replaces
      those sources wholesale, so the question stops mattering going forward
      and cannot be answered backwards.
