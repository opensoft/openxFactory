# Design: Private connectivity evidence pin registration

Status: ratified
Ratified: 2026-11-10 by Brett Heap. [Ratification record](review/ratification-2026-11-10.md)

## Context

The failed required check is `test_every_committed_commit_shaped_value_that_resolves_is_covered` in PR #1303. The feature checker already validates four required pilot boundaries independently of submitted baselines; that earlier review finding is fixed. The remaining coverage failure concerns undeclared reference sites, including original authority and candidate revisions.

## Goals / Non-Goals

Complete the inventory for feature 040 evidence and retain repository-local reachability checks. Do not exempt the evidence directory or classify local derivation claims as foreign or historical simply to pass CI. No review-lane floor, merge authority, runtime behavior or published contract changes belong here.

## Decisions

Use existing `PinMember` declarations and extraction mechanisms, narrowly matched to the feature evidence paths. Make repository ownership explicit in the evidence format where necessary; a raw commit name without an owner is insufficient for a mixed-repository record. Declare local current derivation references separately from foreign-owner source references and immutable observations. Preserve original measurements and actual source revisions.

Before editing the reader, measure all committed sites and the existing standing census. Add only the corresponding declarations and directly affected census expectations. Add regression cases for missed local references, foreign references, and a mixed record so that adding the inventory cannot hide a local orphan. Keep the existing uncovered-site sweep intact. If existing mechanisms cannot express ownership without expanding the reader, return for scope review before adding a generalized parser.

## Risks / Trade-offs

A broad regex could misclassify foreign hashes as local or silently exempt a local claim. Constrain declarations by path and reference form, require explicit repository ownership, and retain the uncovered-value test. An observed revision is not a fresh rerun; retain its measurement context when adding metadata.

## Migration Plan

After ratification, extend T001's evidence-tooling authority with this exact scope. Implement and validate through feature 040, including the current feature chain and full relevant doc-health suite. Regenerate the corpus ledger with the PR number. Keep G4 blocked until all checks and affected human sign-offs are complete. All implementation PRs remain drafts.

## Implementation placement note

The measured standing-census assertion is in `tests/doc-health/test_sentinel_vocabulary.py`, not the initially named sibling test module. The authorized measured-census update applies there; the shared reader continues to use existing declarations and the coverage sweep remains intact. This is a placement correction within the ratified narrow repair.
