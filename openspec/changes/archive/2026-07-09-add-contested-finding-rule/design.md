# Design: Add Contested Finding Rule

## Decision 1: Enforce the process with the regression diff, not review vigilance

A rule that says "don't auto-fix contested findings" binds only if
violations are visible. The regression diff already compares consecutive
reports; emitting "uncited resolution" as a new error turns operator
process violations into ordinary findings — the machinery polices its own
operators.

## Decision 2: Classification is per-family default, overridable per-finding

Families are born auto-fixable (tag hygiene, link resolution, missing
headers) or contested (status/state changes, register status,
gate-decision reversals); a family may emit the other class for specific
findings when it can prove mechanicalness (e.g. a status value with a typo
matching one valid value). Keeps the report deterministic.

## Decision 3: No document-lifecycle delta

Investigation showed the promoted document-lifecycle text already names
candidate registers as an organized-state home; the narrow reading came
from implementing a fragment. The corrective lands in doc-health (where the
check is defined) plus the new fragments-are-inputs sentence; touching
document-lifecycle would be restatement.

## Decision 4: Sequenced instance repair

Checker fix and fixture first, register restore second — restoring first
would re-flag on the next run and invite the same auto-fix this change
exists to prevent.
