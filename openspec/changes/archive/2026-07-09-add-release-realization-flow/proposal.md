# Add Release Realization Flow

code_surface: none
target_release: implemented
Status: ratified
Ratified: 2026-07-09 by Brett — record: the archive commit `3d51c3e`, "Archive add-release-realization-flow (ratified; doc-only, archives on landing)", whose body opens "Ratify gate approved by Brett 2026-07-09"; the same act promoted this change's delta into `openspec/specs/release-realization/spec.md`. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

Doc-only changes archive when prose lands, but the family now ships code:
the doc-health checker change piloted realization-gated archival ad hoc —
it declared at its proposal gate that it would archive only when its code
ran green, stayed active through three failed CI runs, and archived after
the green nightly. That discipline preserved the brownfield invariant
(promoted specs describe what the code does; active changes are approved
intent not yet realized), but it exists nowhere as a rule: the next
code-surface change could archive on paperwork and silently break the
spec-vs-code link.

## What Changes

- Every proposal declares `code_surface:` (`none` default) and
  `target_release:`; doc-only changes keep archiving on landing.
- Code-surface changes archive only on realization evidence: merged code on
  the implemented target, with a green run where a runnable surface exists.
- Decomposition scale rule: small changes execute their own tasks; multi-
  feat changes go through codexFactory feature decomposition; batched
  releases decompose late from the release delta.
- Release definitions live in the aggregation repo; implemented target
  defaults to affected repos' main lines; branch while open, tag at
  promotion.
- Ordered deltas: later changes touching an actively-modified requirement
  reference and sequence after the earlier change.
- The three branch kinds are named contract vocabulary.

## Capabilities

### New Capabilities

- `release-realization`: the realization axis on OpenSpec changes, archive
  gating, decomposition scale rules, and release target definitions.

### Modified Capabilities

- None. (document-lifecycle's gates are consumed, not altered: "archive" as
  a gate is unchanged — what qualifies a code-surface change to pass it is
  this capability's subject.)

## Impact

- openxFactory: new docs/release-realization-flow.md (with the lifecycle
  visualization and the pilot as case study); brainstorm marked organized.
- codexFactory: approved-intent-intake doc notes ratified code-surface
  changes as admitted intent records.
- Doc-only (code_surface: none); archives on landing.
