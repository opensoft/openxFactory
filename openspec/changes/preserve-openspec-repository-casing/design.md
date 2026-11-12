# Repository casing compatibility

Status: draft
Kind: architecture

## Context

The reader and selected consumer baseline are identical at the implementation
level, but current factory main has retired two dispositions the consumer still
needs. The maintenance must correct repository spelling without absorbing that
separate pin-advance work. GitHub repository IDs for the authorized names remain
unchanged; no network or repository-ID discovery is introduced into an offline gate.

## Goals / Non-Goals

Match the two approved spelling pairs at disposition-scope comparison. Preserve
all exception content, exact finding matching, duplicate/stale refusal and
actual remote identity reporting. General case-folding, other aliases, grant
changes, remote rewrites, exception retirement, contract cuts and live pilot
operation are outside this change.

## Decisions

Use a private comparison key mapping only `codeXfactory` to `codexFactory` and
`openXfactory` to `openxFactory`. Apply it to both the declared scope and observed
identity, leaving strings and printed records untouched. A broad lowercase or
Unicode case-fold would admit spellings that this maintenance did not select.

Reconciliation still groups by exact item, path and normalized finding. Two
entries using the approved spellings for the same finding remain duplicates and
refuse. An alias never hides a stale exception or turns another repository's
exception into an applicable one.

The source branch starts at the domain's selected immutable commit
`93d13d6c8e14008c0b66adea65756d106fef6227`. Its head is a narrow compatibility
backport; the PR into main also carries the correction into current tooling.
The consumer selects that exact backport head only through its governed pin hop
and must retain the existing contract and browser identity boundaries. It does
not jump to unrelated later exception retirements. Every frozen pin and released
contract file must remain byte-identical to the selected baseline.

## Risks / Trade-offs

An unlisted spelling continues to refuse; extending aliases requires its own
verified naming authority. The current main merge tree and backport head differ
because main has other accepted work; test and record both identities rather
than claiming their trees are equal. Do not archive this change or claim pilot
runtime acceptance from these tooling tests.

## Migration Plan

Verify the backport source, PR integration and scoped consumer corpus. After
accepted upstream landing, the consumer's preparation PR carries the immutable
backport pin, unchanged vendored acquisition bytes and a generated fold-preserving
browser pin hop. Rollback uses the prior exact source selection through the same
governed mechanism; it does not rewrite recorded hop history.

## Open Questions

None for the bounded maintenance. Human broker acceptance and protected runtime
qualification remain in pilot feature 058, outside this tool correction.
