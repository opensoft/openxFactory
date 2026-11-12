# Plan: OpenSpec repository casing compatibility

Status: draft
Feature: 042-openspec-repository-casing
Branch: 042-openspec-repository-casing
Date: 2026-11-11

## Summary

Add a private exact comparison-key mapping in the existing Python reader and
focused regressions. Keep the backport based on the domain's selected
`93d13d6c8e14008c0b66adea65756d106fef6227`. No new dependency, storage or network
client is required. Complexity remains linear in disposition count.

## Constitution Check

PASS before implementation: the existing neutral reader owns its scope match;
the explicit aliases implement authorized naming maintenance, preserving all
authority and frozen bytes. OpenSpec precedes code. The source is an existing
linked worktree in its declared bench. No product runtime, release, policy,
owner-act box or acceptance floor changes. Post-design PASS under the same bounds.

## Implementation and validation

[Tasks](tasks.md) is the sole implementation list. Run the complete
`tests/openspec_cli_pin` suite, reader pin-integrity checks and the actual consumer
corpus using the unchanged selected pin data. Verify a main integration candidate
with fresh hosted CI and explicit Codex review. The consumer separately proves
its fold-preserving immutable pin hop before its preparation PR is considered.
