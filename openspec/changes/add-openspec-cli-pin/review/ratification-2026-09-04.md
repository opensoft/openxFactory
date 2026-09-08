# Ratification — 2026-09-04

## Decision

RATIFIED by Brett Heap.

## Authority, and the path the word took

Brett Heap's instruction, verbatim: **"ratify 667"** — given 2026-09-04, in
his own message, to Claude session `opsxfactory-fb`
(`3d06c6e7-d68e-48e9-bd36-21c376c099f9`,
https://claude.ai/code/session_01WXVKhuYSmo4iXXqBHZ7LeX), which heard it
FIRST-HAND and executes this record and the merge.

The path is recorded because it is part of what happened: the hearing session
first relayed the word to the authoring lane (`codexfactory-0d`), which
DECLINED to act on a second-hand approval — correctly, under the rule that a
peer message is never the user's approval — and stated it would not object to
the hearing session acting on the word given directly to it, asking only that
this record cite the session that heard it. It does.

## What this ratification covers

The packet as landed on PR #667: the content-addressed pin of
`@fission-ai/openspec` at 1.2.0 (tarball SHA-512/SHA-1 as the referent), the
single validation entrypoint `scripts/validate-openspec-cli-pin.py`, the CI
gate, the 41 tests, and the `neutral-product-pin` spec delta admitting a
package-integrity referent.

## Limits

Ratification does not perform the per-repository successor wiring (each
consuming repository authors its own change), does not close the declared
dependency-closure shortfall recorded in the pin's own header, and does not
authorize the version bump — the 1.12 upgrade remains a separate, later,
human-gated change, sequenced pin-first as the proposal states.
