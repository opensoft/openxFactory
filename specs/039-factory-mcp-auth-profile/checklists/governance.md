# Governance Requirements Quality Checklist: Factory MCP authorization profile

Status: record
Kind: report

**Purpose**: test whether the feature's requirements trace to the ratified
change, leave its text untouched, and meet this repository's lifecycle and
public-repository rules, at release-gate rigor.
**Created**: 2026-10-09
**Feature**: [`spec.md`](../spec.md)

## Traceability

- [x] CHK001 Does every functional requirement name the delta scenario and the design decision it serves? [Traceability, Spec §Requirements]
- [x] CHK002 Is every one of the 19 delta scenarios either covered by an acceptance scenario or recorded as outside the feature? [Coverage, Spec §User Scenarios; §SC-001]
- [x] CHK003 Is each realization decision recorded with the packet line, or the standard, that decides or delegates it? [Traceability, research R-1 to R-17]

## Authority

- [x] CHK004 Is it stated that the ratified requirement and scenario text is the authority, and that the feature never restates it differently? [Clarity, Spec §Authority and traceability]
- [x] CHK005 Is the clarify outcome recorded, with who accepted it? [Completeness, Spec §Clarifications]
- [x] CHK006 Is the departure from the git extension's worktree mode recorded, with its reason and acceptance? [Completeness, Spec §Clarifications; plan §Constitution Check]
- [x] CHK007 Is it stated that the feature edits no file of the change packet, and that it lands only on its own word? [Completeness, Spec §Assumptions] (Gap found and fixed in this pass.)

## Lifecycle and Repository Rules

- [x] CHK008 Does every new document carry a controlled `Status:` that claims no ratification of its own? [Consistency, plan §Constitution Check III]
- [x] CHK009 Is it specified how the new documents are reached from README's index (through the runbook)? [Completeness, plan §Constitution Check IV; Spec §FR-018]
- [x] CHK010 Are the public-repository constraints stated: synthetic identifiers, no host-absolute or private paths, no vendored domain bytes? [Completeness, Spec §Assumptions; research R-16]
- [x] CHK011 Are the gates the feature must pass, and the comparison against `main` in the same clone kind, specified? [Completeness, plan §Constitution Check V; Spec §SC-006]

## Notes

- 11 items; all pass after the one fix recorded at CHK007.
