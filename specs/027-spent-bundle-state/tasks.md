# Tasks: the third state — a SPENT bundle

**Feature**: `027-spent-bundle-state`, re-scoped onto
`fix/spent-state-containment-hardening` | **Branch point**: `origin/main` at or
after `3fa222f3`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## RE-SCOPED — PHASES 1 TO 5 ARE LANDED WORK, PHASE 6 IS THIS BRANCH'S

**The realization landed as PR #587, squash `3fa222f3`**, from a sibling
session's branch while the parallel `027-spent-bundle-state` (PR #584) was in
bot round 5. **T001–T035 below are therefore a RECORD, not a plan**: their ticks
describe work that is on `main`, measured by the evidence files they cite, and
they are kept unedited so the numbers in those files have something to be the
numbers OF. The one correction owed to that record is stated in
[`evidence/test-counts.md`](./evidence/test-counts.md)'s own terms and repeated
here: PR #584's family-file count was **66** (65 passed + 1 deselected), not the
69/70 published in its round-5 comment.

**PHASE 6 IS THIS BRANCH'S WORK** — the containment hardening PR #584's five bot
rounds found and `main` does not carry.

## Phase 6 — the containment hardening (this branch)

- [x] **T036** MEASURE FIRST, against `main`'s code and not against a
      description of it: each of the ten escapes probed through
      `parse_spent_declarations` / `check_repo` at `origin/main`, with the
      accepted-or-wrong answer recorded per escape.
      [`evidence/hardening-red-first.md`](./evidence/hardening-red-first.md) § A
- [x] **T037** ONE structural-boundary function. `_entry_boundary(line,
      previous, in_fence) -> (closes, opens)`, TOTAL over the fence state so a
      second caller cannot reintroduce the escape by forgetting to skip fenced
      lines; `_fence_state` and `_setext_content` beside it, each answering one
      question. (FR-H01)
- [x] **T038** ATX boundaries: H1 and H2 close, H3+ do not, one to three leading
      spaces are a heading and four are not, an empty heading is a boundary, and
      `#550 example` is not a heading at all. (FR-H02, FR-H04, FR-H05, FR-H08)
- [x] **T039** A complete version token opens an entry — `## contract-v3.0.1`
      and `## contract-v3.0-notes` open none, `## contract-v3.01` opens its own.
      (FR-H03)
- [x] **T040** Fences are OPAQUE to headings AND to the reserved opener, with
      the closer required to be the same character, at least as long, and
      followed only by whitespace. (FR-H06)
- [x] **T041** Setext headings close and never open; a thematic break and a
      table rule close nothing. (FR-H07)
- [x] **T042** The changelog guard moves BELOW `parse_bundle` and `cut_bundles`
      and is gated on in-scope-ness; a below-floor repository with no changelog
      is answered as it always was. (FR-H09)
- [x] **T043** The batch-read skip names both members. (FR-H10)
- [x] **T044** Below-floor SUBJECTS leave the orphan sweep; wrong-SHAPE subjects
      stay in it. (FR-H11)
- [x] **T045** THE RULE AS ONE TABLE — 21 parametrized rows carrying the
      stays-open cases beside the closes cases, so it cannot be satisfied by a
      reader that closes on everything any more than by one that closes on
      nothing — plus six scenario tests, each with a positive control per this
      file's convention. Family file **46 → 73**.
- [x] **T046** THE LIVE READ, from disk, pinning `entry == contract-v3.0` for
      this repository's own declaration, with a spliced-heading control over the
      same bytes. (FR-H12)
- [x] **T047** `docs/doc-health.md` gains one paragraph saying what "inside the
      entry" means. Family counts untouched.
- [x] **T048** Gates, and the after-measurement per escape.
      [`evidence/hardening-red-first.md`](./evidence/hardening-red-first.md) § B

**Realizes**: `openspec/changes/declare-spent-bundle-state` § 2, boxes
**2.1–2.9**. Every task below cites the packet box it realizes. These are the
EXECUTABLE steps; they are not a re-typing of the packet's list, whose boxes
are ticked with evidence in the same PR.

**Tests ARE requested, RED-FIRST.** The packet requires *"the RED-FIRST proof
for 2.1's verification: the declaration removed, the `error` returns"* and the
constitution's deterministic-evidence principle requires the rest.

## THE RED GATE — AND IT WAS NOT MET IN THE ORDER IT ASKS FOR

`T004`–`T018e` are the RED tests, and the gate as written requires every one to
be seen failing for its stated reason before `T019`, the first module task.

**THAT IS NOT THE ORDER THIS SESSION WORKED IN, AND THE GATE IS LEFT STANDING
RATHER THAN REWORDED TO MATCH WHAT HAPPENED.** The module and the tests were
authored in one pass, module first; the red was then demonstrated by REVERTING
the module against the landed tests, where not one of the 32 new tests can even
be collected. That is weaker than a true test-first order, it is recorded in
[`evidence/red-log.md`](./evidence/red-log.md) § A rather than smoothed over,
and the gate stays as written so the deviation has something to be a deviation
FROM. What IS red-first in the strict sense is the one the packet requires by
name: T014's declaration-removal control, which is a permanent test and is
re-taken over the real repository in
[`evidence/post-merge-proof.md`](./evidence/post-merge-proof.md) § B.

## Phase 1 — the declaration, FIRST and not silently (packet 2.1)

- [x] **T001** Write ONE reserved-form line into the EXISTING
      `### \`contract-v2.6\` disposition …` subsection under `## contract-v3.0`
      in `contracts/CHANGELOG.md`. Elements from the record that already
      exists: superseding `contract-v3.0`; cause the ADDITIVE-class-over-a-
      refusing-tree defect plus never-verifiable-at-`bbbbeda9`; ruled by Brett
      Heap, 2026-09-02; measurement PR #565 comment `5502452624`.
- [x] **T002** Confirm NOTHING ELSE in the changelog moved, and that
      `contracts/manifest.yaml`,
      `contracts/releases/contract-v2.6.digests.yaml` and the
      `## contract-v2.6` entry are untouched. `git diff --stat` on the
      changelog: **2 insertions, 0 deletions**.
- [x] **T003** Confirm `contract-v3.0`'s tag IS published, so the declaration
      lands in the `info` band and not OD-4's `warning` band:
      `git ls-remote origin refs/tags/contract-v3.0` → `59f4f51f…` peeling to
      `ff9ed815…`. Checked, not assumed.

## Phase 2 — RED tests (packet 2.6, 2.7)

### The reader, with no repository (14 tests)

- [x] **T004** the reserved form parses into its four elements, and the
      backticks are the form's rather than the name's.
- [x] **T005** the reader takes BYTES (`blobs_at`'s contract) and str
      identically; a mis-encoded byte elsewhere does not crash the read.
- [x] **T006** empty/absent bytes read as NO declaration, and the SKIP is the
      caller's job — pinned so the two can never become one function.
- [x] **T007** the reserved opener on a line that does not complete the form is
      MALFORMED, keyed under `None`, never prose.
- [x] **T008** an omitted element is NAMED (three elements, three names).
- [x] **T009** an EMPTY element counts as missing, not as present.
- [x] **T010** a ruling without a date reports the `ruling date` specifically.
- [x] **T011** the ` — ` separator is reserved WITHIN the line.
- [x] **T012** a declaration outside every release entry carries no entry.
- [x] **T013** two declarations naming one bundle are COUNTED, and the count
      alone is a refusal.
- [x] **T013a** an EMPTY backtick pair carries a `defect` and not a bare
      `None` — **found in self-review, before the bots**: the `None`-keyed
      finding INTERPOLATES the defect string, so a None there would print the
      word "None" into a finding a human has to act on.
- [x] **T013b** a misspelt keyword is not read as the keyword: `RULED BYE …`
      must not match `RULED BY` and yield the value `E …`. Also self-review.
- [x] **T013c** elements OUT OF ORDER are MALFORMED rather than reported
      missing — the cause is right there, and saying it is absent would send a
      reader looking for text the line already carries.

### The ladder, over real git fixtures (15 tests covering 13 scenarios, + 3 report proofs)

- [x] **T014** ACCEPTED → one `info`, on the inventory path, classed
      `contested`, naming spent bundle + successor + where the record is + the
      ruling; and **THE RED-FIRST CONTROL IN THE SAME TEST**: the same fixture
      with the declaration removed returns the superseded `error` on `MANIFEST`.
- [x] **T015** PROVISIONAL → ONE `warning`, not two; and the successor still
      graded on its own account.
- [x] **T016** successor never cut → `error` + superseded `error` stands.
- [x] **T017** successor not STRICTLY LATER (OD-9, the backwards case) →
      `error` + superseded `error` stands.
- [x] **T018** SUBJECT never cut → `warning` on the changelog + the real
      bundle still reported; element omitted → `error` in its own words, not
      the absent-tag words; outside the successor's entry → `error`; a bundle
      cannot declare ITSELF spent; two declarations naming one bundle accept
      NEITHER; two different bundles → two `info`s with two identities; names
      the currently declared bundle → `error` AND still distance-graded; does
      not quiet a MISPLACED tag; does not quiet a LIGHTWEIGHT ref; an
      unreadable changelog SKIPS naming that read (with its positive control);
      the state is not read backwards onto published or legacy bundles.
- [x] **T018d** OQ-3: a contested `info` vanishing raises an
      `uncited-resolution` ERROR on that bundle's path — PROVED, not inherited.
- [x] **T018e** the Codex repair with TWO bundles: two `info`s, two match keys,
      one withdrawal raising exactly one uncited-resolution; plus the
      complement, that a CITED disposition silences it.

## Phase 3 — the module (packet 2.2–2.5)

- [x] **T019** `CHANGELOG` constant; the four new action constants; the
      reserved-opener, separator, subject, entry-heading and ruling patterns;
      `_SPENT_ELEMENTS`. (2.4)
- [x] **T020** `SpentDeclaration` and `_parse_spent_line`. (2.2)
- [x] **T021** `read_spent_declarations(bytes) -> {bundle: declaration}` — one
      pure function, rejecting rather than skipping, counting duplicates. (2.2)
- [x] **T022** `spent_refusal(declaration, subject, cut)` — the seven pure
      refusals in order; and `inventory_path(bundle)`. (2.3)
- [x] **T023** `_finding` gains `path=MANIFEST` as a DEFAULT so every
      pre-existing finding keeps its identity. (2.4)
- [x] **T024** the ladder in `check_repo`: the changelog joins the manifest in
      ONE `blobs_at` call at ONE commit with the SAME guard (2.5); the ladder
      in the ABSENT arm AFTER ok/lightweight/misplaced (2.3); the three emits
      and the declared-bundle refusal (2.3, 2.4); the post-loop orphan sweep
      (2.4). Module docstring gains the state, its record, its three outcomes
      and its path rule.

## Phase 4 — docs (packet 2.8)

- [x] **T025** `docs/doc-health.md`: the family's note gains the third state,
      the reserved form, the three outcomes, the path rule, the action lines and
      the no-retrofit rule.
- [x] **T026** Confirm the family-count sentences are UNTOUCHED — this change
      adds no family — and that `family-enumeration` reports nothing.

## Phase 5 — evidence and gates (packet 2.9)

- [x] **T027** `pytest tests/doc-health/test_release_tag_publication.py` →
      **50 passed, 1 failed**, the failure being the self-gate reading remote
      `main` (see R1).
- [x] **T028** `pytest tests/doc-health` → **1415 passed, 1 failed**, same
      single failure. (packet 2.9)
- [x] **T029** THE POST-MERGE PROOF: a bare origin whose `main` is this branch,
      a clone of it, and the self-gate run there → **1 passed**. Then the
      declaration removed from that origin's `main` → the `error` returns and
      the self-gate fails. [`evidence/post-merge-proof.md`](./evidence/post-merge-proof.md)
- [x] **T030** `openspec validate --all --strict` → 85 passed, 0 failed.
- [x] **T031** `proposal-support.py . verify declare-spent-bundle-state` → ok.
- [x] **T032** `validate-sequenced-after.py .` → passed (32 active, 1
      declaring); `pytest tests/sequenced_after` → 118 passed. NO pin moved:
      this feature adds no OpenSpec change and moves no change directory.
- [x] **T033** `verify-commit --commit HEAD` → exactly TWO members mismatch,
      both disclosed; `verify-tag --remote origin --tag contract-v3.0` → pass.
      [`evidence/gates.md`](./evidence/gates.md)
- [x] **T034** `--single-repo` doc-health before/after, same clock → exactly
      ONE new ranked-plan row.
      [`evidence/doc-health-delta.md`](./evidence/doc-health-delta.md)
- [x] **T035** the full suite, and the PR body.
      [`evidence/test-counts.md`](./evidence/test-counts.md),
      [`pr-body.md`](./pr-body.md)

## NOT this feature

- **OpenSpec § 3.1** — `docs/contract-versioning-policy.md`'s obligation-side
  paragraph. ROUTED TO THE NEXT CUT by the owner's ruling of 2026-09-02; see
  plan.md § Routing. Left UNTICKED in the packet with a dated note.
- **OpenSpec § 5** — the archive, which follows the merge.
