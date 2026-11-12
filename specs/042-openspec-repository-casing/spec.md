# Feature 042: OpenSpec repository casing compatibility

Status: draft
Governance: [proposal](../../openspec/changes/preserve-openspec-repository-casing/proposal.md)

A factory operator validates an unchanged corpus after the authorized spelling
migration. The same existing dispositions apply and remain visible. An author
cannot add an unapproved alias, hide a stale entry or duplicate an exception.

FR-001: Match exactly the two approved old/current spelling pairs at scope comparison.
FR-002: Preserve raw identity, all record bytes and item/path/finding matching.
FR-003: Refuse duplicate aliases and preserve whole-corpus stale detection.
FR-004: Leave other repository names under existing exact-match behavior.
FR-005: Preserve the selected baseline's contract/pin bytes and qualify the consumer's actual corpus.

Acceptance: positive checks in both directions, scope-negative cases, duplicate
and stale controls, complete reader suite, pinned strict validation and exact
source/PR integration evidence. CI success is source-tooling evidence only.
