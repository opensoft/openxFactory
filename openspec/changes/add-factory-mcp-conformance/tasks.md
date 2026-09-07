# Governance and realization handoff

Lane: mcp-family-contract

These are governance checkpoints. The single Speckit feature created at 2.1
will own executable implementation tasks; this file does not duplicate them.

## 1. Proposal and ratification

- [x] 1.1 Capture design and write proposal, design and scenario-complete delta; verify all artifacts exist and every requirement has scenarios.
- [x] 1.2 Validate the exact proposal and origin and record a consistency review; per-change checks pass and unrelated baseline findings are recorded in review/validation-2026-09-07.md.
- [x] 1.3 Brett Heap ratified this exact packet and ad-hoc origin on 2026-09-07; review/ratification-2026-09-07.md names the reviewed revision.

## 2. Speckit realization

- [ ] 2.1 Create exactly one canonical numbered Speckit feature from a clean root/base checkout after ratification; record its path here and verify spec/plan traceability to this delta.
- [ ] 2.2 Complete clarify, plan, checklist, tasks and analyze in that feature worktree; verify no critical findings and executable task coverage for the neutral schema, offline validator, synthetic fixtures and compatibility guidance.
- [ ] 2.3 Complete implementation and verification from the feature task list; record deterministic positive/negative evidence and required repository checks. No live deployment or release acceptance is implied.

## 3. Review and closure

- [ ] 3.1 Review and land realization through the authorized repository process; verify exact merged revision and green checks, respecting sibling and shared-substrate claims.
- [ ] 3.2 Archive only after merged green realization; verify promoted requirements and preserved provenance under the archive gate. Release cuts, hosted acceptance and consumer adoption remain separately governed.
