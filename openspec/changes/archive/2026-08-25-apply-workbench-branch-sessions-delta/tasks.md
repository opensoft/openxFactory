# Tasks: Apply the Workbench Branch-Sessions Delta

## 1. Restate the ratified delta

- [x] 1.1 Confirm the gap before writing anything, through the real code path
      rather than by reading: `scripts/doc_health/promotion_fidelity.py` via
      `runner.build_context` + `families.FAMILIES["promotion-fidelity"]` over
      this repository reports exactly TWO findings, both `warning`, both
      against
      `openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/specs/lifecycle-notebook-projection/spec.md`
      — "ratified ADDED requirement 'Branch-session notebooks' is absent from
      openspec/specs/lifecycle-notebook-projection/spec.md", and "requirement
      'Corpus scan scope' reached
      openspec/specs/lifecycle-notebook-projection/spec.md without 1 of its 4
      ratified scenarios: \"A canon book is offered a branch session's
      drafts\""
- [x] 1.2 Confirm canon has NOT drifted since the 2026-08-01 archive. Only two
      archived changes in the corpus contain "Requirement: Corpus scan scope"
      — `2026-07-12-exclude-worktrees-from-notebook-projection` (earlier) and
      `2026-08-01-add-workbench-branch-sessions` (this one), so 2026-08-01 is
      the latest ratified writer. No archived change names "Branch-session
      notebooks" at all except that one. The three later writers of
      `lifecycle-notebook-projection` touch neither requirement:
      `2026-08-05-adopt-neutral-tooling-home` modifies "Projection
      implementation ownership", `2026-08-10-split-ideation-book-per-repo`
      modifies "Derived notebook membership" and adds "Projection capacity
      guard", `2026-08-13-add-session-notebook-reconciliation` adds "The
      session namespace is reconciled against live sessions". Applying the
      ratified text clobbers no later ratified work
- [x] 1.3 Author this packet's delta as a byte-for-byte copy of the archived
      delta file — same SHA-256
      (`f6ffd39abeab7a1548a93ed78fda9a24d8da19606fbc5f30dc85fe013b0361cd`),
      empty `diff`, no re-wording, no re-derivation — with each requirement's
      SHALL on the first line of its body
- [x] 1.4 Record, do not fix, the one thing restating faithfully costs: the
      ratified body's "three lifecycle books" count, made stale on 2026-08-10
      by `split-ideation-book-per-repo`. Named in the proposal's § Recorded,
      not fixed; correcting it is a normative edit to ratified text and
      belongs to a successor change with its own ratification

## 2. Validation

- [x] 2.1 `OPENSPEC_TELEMETRY=0 openspec validate apply-workbench-branch-sessions-delta --strict`
- [x] 2.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` (75 before,
      76 with this change active, back to 75 after archive)
- [x] 2.3 `python3 -m pytest tests/doc-health` green at the pre-change baseline
- [x] 2.4 List this change in the README's OpenSpec Records block

## 3. Discharge the finding that commissioned this change

- [x] 3.1 Tick task 5.1 of `add-promotion-fidelity-check` under append
      discipline: the box text stands exactly as written, and one dated
      pointer line names this change as the exit taken. That change stays
      ACTIVE; its own archive gate is not this change's to close

## 4. Promotion and archive

- [x] 4.1 Promote the delta into
      `openspec/specs/lifecycle-notebook-projection/spec.md` and archive this
      change (promotion-only; `code_surface: none`, so it archives on landing)
- [x] 4.2 Diff-verify the promotion: both requirement blocks in canon are
      byte-identical to the ratified delta's, extracted and hashed rather than
      eyeballed. "Branch-session notebooks" carries five scenarios; "Corpus
      scan scope" carries four
- [x] 4.3 Re-measure the promotion-fidelity family through the same real code
      path: the two findings GONE, and this packet's own archived delta adds
      none of its own
- [x] 4.4 Re-validate after promotion (`--all --strict`; the single-change
      `--strict` no longer applies once archived) and re-run the doc-health
      suite. This packet's archived `proposal.md` is itself a lifecycle
      scan-set document and must read clean across the four lifecycle
      families, with exactly one in-window citation line clearing the
      approver and date axes
