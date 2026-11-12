# Source compatibility evidence

Status: draft
Scope: source tooling only

The backport starts at `93d13d6c8e14008c0b66adea65756d106fef6227`.
The complete reader suite passed 168 tests in 27.33 seconds. The actual consumer
corpus, with its current codeXfactory remote identity, exited 0 with four named
accepted exceptions and zero undispositioned errors. This is not a clean corpus.
Pinned strict validation of this change passed 1/1. OpenSpec artifacts are complete.

All contracts, exception bytes, workflows and dependency mounts remain identical
to the selected baseline. The private scope key admits only the two approved
spelling pairs; duplicate aliases still refuse, missing findings remain stale
on whole-corpus scans and unrelated/unapproved names remain out of scope.

Hosted integration checks and exact-head Codex review are pending. The main
integration tree and selected backport source must be recorded separately.
No release, archive, domain execution pin or runtime acceptance is claimed.
Feedback remains deferred; neither historically blocked write is replayed.

## Local expert-panel correction

The panel reproduced an unhashable repository scope at the in-memory
`pinned_dispositions` / `reconcile` boundary. Inline collection-like scope text
is parsed as a string; further review proved a nested block-valued `repo` is
parsed as a list and reaches the same failure through the CLI. Equality
comparisons retain the prior out-of-scope behavior without adding pin-shape
rules. Two in-memory list/dict regressions failed before correction; two CLI text
controls and a block-valued CLI regression prove uncovered findings still refuse
without applying an alias or crashing. The complete reader suite passes 173
tests after correction. This review is local and does not stand in for a GitHub
Codex receipt.
