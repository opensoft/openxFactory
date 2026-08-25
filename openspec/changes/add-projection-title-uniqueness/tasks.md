# Tasks: add-projection-title-uniqueness

This packet is PROPOSAL-ONLY. Nothing under §2 or later has run: its diff is
spec text, records, and this list. The authorization behind it covers RAISING
the proposal against a measured defect and nothing more — `Status: draft`,
Brett rules after reading, and the four decisions in `proposal.md`
§ Orchestrator Decisions plus the four questions in § Open Questions are the
subject of that read.

**§5 is deliberately OPEN and stays open.** What this change does not close is
recorded there rather than implied.

## 1. Ratification and open questions

- [ ] 1.1 Brett reads the measurement and rules on **Q1, the rule candidate**.
      The recommendation is (a), collision-triggered minimal repository-relative
      suffix: 14 renames and 28 book operations against 611 and 1222 for the
      always-fully-qualified alternative, both reaching zero collisions. (b1)
      and (c) are eliminated on CORRECTNESS by measurement — each leaves a live
      collision — and the elimination is in `design.md` § 4 with the reason.
      Ruling (b2) instead is an edit to the delta's third paragraph and to
      §§ 2.1–2.2, not a new change.
- [ ] 1.2 Rule on **Q2, whether the migration rides the realization's own sync
      slice**. §4 is written for ONE SLICE: the realization merges and an
      apply-mode sync follows immediately, so the books are correct on merge
      and the archive evidence exists at once. The alternative leaves the books
      visibly drifted — `notebook-projection-drift` reporting 28 pending
      operations — until a separately scheduled apply.
- [ ] 1.3 Rule on **Q3, whether the arrival of five never-projected documents
      warrants a record** beyond this packet. Three MedxFactory staging topics,
      one openxFactory draft checklist and one OpsxFactory staging fragment
      have never held a source; every answer any book gave about those subjects
      was given from a corpus missing them. If a record is owed, the place is
      `docs/archive-record-discrepancies.md`.
- [ ] 1.4 Rule on **Q4, the uniqueness scope**. Repository scope costs four of
      the fourteen renames and pre-empts the three latent pairs
      (`memory-gateway/README`, `company-provisioning`,
      `codexfactory-domain-hermes-content`), each of which is one `Status:`
      edit from a live collapse. The tightest correct scope is eight renames
      and leaves them latent. `design.md` § 7 measures all three scopes.
- [ ] 1.5 NO `document-lifecycle` delta, and the absence is deliberate. This
      change states an obligation about a PROJECTION — that a derived source
      set be injective over the documents it derives from — not about how
      documents carry lifecycle state. The obligation belongs in
      `lifecycle-notebook-projection` and nowhere else.
- [ ] 1.6 NO `Projection capacity guard` delta, and the absence is MEASURED
      rather than assumed. That requirement defines projected occupancy over
      "the desired managed set plus the charter plus every unmanaged source",
      and the implementation counts DOCUMENTS for it. No guard-computed number
      moves; actual occupancy rises to meet the number the guard already used.
      `design.md` § 8 carries the per-book table.

## 2. Realization — the derivation

- [ ] 2.1 `scripts/sync-notebooklm-books.py`: replace the one-line `README`
      conditional in `scan()` with a repository-scoped uniqueness pass. Two
      steps, in this order, because the scan visits repositories one at a time
      and uniqueness is a property of the finished set: collect each projected
      document's repository-relative segments during the walk, then resolve
      titles once the walk is complete. A document's qualifier is the shortest
      path suffix that distinguishes it from every other projected document of
      the same repository; a `README` stem floors at two segments, preserving
      every title today's rule already produces except where that rule was
      itself ambiguous.
- [ ] 2.2 The `[spec]` and `[grounding]` families stay outside the uniqueness
      scope. Both are keyed by something other than a file stem and neither
      collides; measurement showed that including them over-qualified one
      `drafts` title for no reason. Pin the exclusion in code with the reason,
      not as a silent filter.
- [ ] 2.3 `parity_report()`: compare at the document level. Report a derived
      title carrying more than one path key as a parity FAILURE naming the
      documents, and stop reporting a book as at parity on title-set equality
      alone. This is the check that could not see the defect it existed to
      catch; the amendment is what makes the next instance loud.
- [ ] 2.4 `docs/lifecycle-notebook-projection.md` § 2: replace the
      "Title rule for ambiguous stems" paragraph with the injective rule, and
      add the `Amended by:` line the doc's header convention requires. Note in
      passing that the sentence being replaced already stated the general rule
      in its parenthesis — "or otherwise non-unique within a repo" — and that
      the implementation implemented the example instead. That is the shape of
      failure worth recording where the next reader will meet it.

## 3. Tests

- [ ] 3.1 A collision fixture covering the three real shapes this corpus
      contains, not one generic pair: several documents sharing a stem inside
      one directory family (`ideation/staging/<topic>/topic.md`, four of them);
      two documents whose PARENT directories also match
      (`specs/<id>/checklists/requirements.md`, which is the case that
      eliminates a one-level qualifier); and a pair split across two directory
      families (`ideation/brainstorm/<slug>.md` against
      `ideation/staging/<slug>/<slug>.md`).
- [ ] 3.2 An INJECTIVITY assertion over the whole derived set, per book:
      `len(set(desired[book].values())) == len(desired[book])`. This is the
      assertion whose absence let the class exist. It must be written over the
      derived set rather than over the fixture's expected titles, so a future
      derivation change cannot satisfy it by agreeing with itself.
- [ ] 3.3 A STABILITY assertion: change a fixture document's `Status:` header
      and assert that no other document's title moves. This pins the
      repository-scope choice structurally — under a (book, status) scope this
      test fails, which is the point.
- [ ] 3.4 A parity-blindness regression: build a state with a collapse present
      and assert `parity_report` reports FAILURE. Written against the old
      behaviour it must fail; that is the acceptance evidence for §2.3.
- [ ] 3.5 A FLOOR assertion: a `README` that is unique in its repository still
      carries its parent directory, so the amendment never SHORTENS an existing
      title. Measurement caught a prototype doing exactly that.
- [ ] 3.6 Mutation checks on the assertions that carry the guarantee, chosen
      against the classes this repository has been bitten by. (i) Break
      injectivity — revert the derivation to the bare stem — and confirm 3.2
      reds; an assertion that passes against the defective derivation is not
      the assertion. (ii) Weaken the qualifier to one level and confirm the
      `checklists/requirements` case reds; this is the platform-inert class in
      disguise, where a change that looks like a fix leaves the value equal.
      (iii) Assert on the derived STRUCTURE, not on rendered strings alone, so
      a path-separator or `str(Path)` substitution cannot survive a
      value-equality check.
- [ ] 3.7 Run the whole `tests/notebooklm` suite, not the new file alone: 94
      existing cases read `scan()` output and several assert on exact titles.
      Any of them that must move is evidence about the migration's blast
      radius and belongs in the §4 record.

## 4. The sync that migrates the books, and the archive gate

The defect is a discrepancy between a manifest and a provider. Only the
provider can say it closed, so the archive evidence is a provider read and not
a test run.

- [ ] 4.1 Dry run first, from the workspace root, and diff the plan against
      `design.md` § 6: exactly 14 renames — 28 `DEL`/`ADD` lines — plus the 5
      adds that un-collapse the three collisions. A plan that differs from the
      enumerated list by even one line stops the apply and is investigated
      before anything is applied.
- [ ] 4.2 Apply. The books move from 695 sources to 700: `drafts` 188 → 189,
      `ideation-medxfactory` 49 → 52, `ideation-opsxfactory` 16 → 17, and the
      four unaffected books unchanged (`canon` 114, `ideation-openxfactory`
      247, `ideation-ledgerxfactory` 66, `ideation-codexfactory` 15).
- [ ] 4.3 Read the counts back from the provider and record them. This is the
      evidence, and it is the same read that produced the "before" column, so
      the two are comparable by construction.
- [ ] 4.4 Run `--parity` under the amended rule and record it clean. A parity
      pass taken BEFORE §2.3 lands proves nothing about this defect — that is
      the whole finding — so the run that counts is the one after.
- [ ] 4.5 Confirm `notebook-projection-drift` returns to zero pending
      operations. Between the merge and the apply it reports 28; a non-zero
      count after the apply means the plan and the provider disagree.
- [ ] 4.6 Gates green: `python3 -m pytest tests/notebooklm tests/doc-health`,
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and a doc-health
      single-repo run whose severity counts move by exactly what §2 predicts,
      which is by nothing.
- [ ] 4.7 Archive on that evidence. `target_release: implemented` cuts no
      contract bundle, so the gate is merge-plus-green PLUS §§ 4.3–4.5.

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
