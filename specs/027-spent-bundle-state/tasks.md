# Tasks: the third state — a SPENT bundle

**Feature**: `027-spent-bundle-state` | **Branch point**: `f4fddf7c`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

**Realizes**: `openspec/changes/declare-spent-bundle-state` § 2, boxes
**2.1–2.9**. Every task below cites the packet box it realizes. These are the
EXECUTABLE steps; they are not a re-typing of the packet's list, whose boxes
are ticked with evidence in the same PR.

**Tests ARE requested, RED-FIRST.** The packet requires *"the RED-FIRST proof
for 2.1's verification: the declaration removed, the `error` returns"* and the
constitution's deterministic-evidence principle requires the rest.

## THE RED GATE (a hard ordering constraint)

`T004`–`T018` are the RED tests. Every one MUST be written and seen to fail for
its stated reason — recorded in [`evidence/red-log.md`](./evidence/red-log.md) —
**before `T019`**, the first module task, is started.

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

### The reader, with no repository (11 tests)

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

### The ladder, over real git fixtures (13 scenarios + 2 report proofs)

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
- [x] **T018a** OQ-3: a contested `info` vanishing raises an
      `uncited-resolution` ERROR on that bundle's path — PROVED, not inherited.
- [x] **T018b** the Codex repair with TWO bundles: two `info`s, two match keys,
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
      **47 passed, 1 failed**, the failure being the self-gate reading remote
      `main` (see R1).
- [x] **T028** `pytest tests/doc-health` → **1412 passed, 1 failed**, same
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
