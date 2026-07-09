# Staged: Contested Findings — Instance Fix And Process Rule

Status: staged
Kind: architecture
Repository context: openxFactory
Source: incident evidence, 2026-07-09 — doc-health report #1's location
finding against the candidate register was a false positive (the checker
implemented the staged fragment's narrow wording, "staging fragments only
under ideation/staging/", over the promoted spec's broader
"ideation/staging/ **or a candidate register**", document-lifecycle spec
line 64), and the resolving session auto-fixed a compliant document
(register `staged -> draft`, commit ff5b06b) because no rule distinguishes
a defect from a contested finding.
Target capabilities: `doc-health` (delta: MODIFIED/ADDED — process rule),
`document-lifecycle` (delta: MODIFIED — clarification), plus a codexFactory
checker bug fix (implementation, no contract delta needed).

## Part 1 — THIS INSTANCE (bug fix + state restore)

1. codexFactory checker: the location-conformance family must implement the
   promoted spec — `staged` is legal in `ideation/staging/` OR a candidate
   register (`Kind: register`). Fixture added: a register outside staging
   that must NOT be flagged.
2. Restore the register to `Status: staged`, citing this topic and the
   corrected rule. Sequencing: checker fix FIRST, restore SECOND, or the
   next report re-flags it and invites the same auto-fix.

## Part 2 — THE PROCESS (contested-finding rule; future-proofing)

Delta to `doc-health`: findings SHALL be classified auto-fixable (mechanical
defects: malformed markers, broken links, missing headers) or **contested**
(resolution would change a deliberately-set state, arbitrate between rules,
or reverse a prior gate decision). Contested findings are report-and-escalate
only: resolution requires a cited OpenSpec change or an explicit human
disposition recorded against the finding id — never a silent normalizing
edit.

Self-enforcement: the regression diff already compares reports; a finding
that disappears via a status/state change with no citing change id or
disposition becomes a NEW finding ("uncited resolution"). The process rule
is checkable by the machinery it governs.

## Part 3 — CLARIFICATION (prevent this ambiguity class)

Delta to `document-lifecycle`: the ideation/location language names candidate
registers explicitly wherever `staged` placement is stated, so no future
implementer can re-derive the narrow reading from a fragment instead of the
spec.

## Why the incident happened (for the change's design.md)

- The finding was manufactured by implementing fragment wording over
  promoted spec wording (fragments are staged inputs, not contracts).
- No promoted rule obligated escalation: the explicit-delta rule governs
  prose, and a Status flip is a state transition whose only requirement was
  review-history visibility — satisfied by any commit.
- Clear-the-findings mode treats "suggested action" as authoritative; the
  contract had no contested class to stop it.

## Exit

Satisfied by
[add-contested-finding-rule](../../../openspec/changes/archive/2026-07-09-add-contested-finding-rule/proposal.md)
(2026-07-09). Correction found at proposal: document-lifecycle needed NO
delta — its promoted text already allows registers; both deltas landed in
doc-health (register-aware location rule + resolution classes with the
uncited-resolution regression rule). Checker fixed first, register restored
to `staged` second; exemption verified against the live corpus.
