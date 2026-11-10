# Conditional Lane Check Design

Status: draft
Kind: architecture

## Context

See [proposal](proposal.md) for the existing authority and scope. GitHub supplies a PR body but no trustworthy lane-launch binding. This is declaration validation, not membership attestation.

## Goals / Non-Goals

Permit absent attribution and strictly validate attribution supplied as a declaration. Preserve the workflow's current bot behavior and protection configuration. Do not infer membership from branch names or environment absence, introduce an opt-out label, or invent a register row.

## Decisions

Keep validation inline in `.github/workflows/lane-line.yml`, which requires no checkout of untrusted PR code. Pass the body only through `BODY`. Normalize CRLF for line analysis. Recognize declaration-shaped lines case-insensitively with optional leading whitespace so misspellings cannot masquerade as absence. When any such line exists, require exactly one, in the first nonempty line, with the established case-sensitive format. A prose mention in the middle of a sentence is not a declaration.

Preserve the optional parenthesized descriptive suffix from the old regex. Do not echo an invalid body into logs; emit a fixed error to avoid workflow-command interpretation. No-declaration bodies emit a fixed notice.

Regression tests extract and execute the exact inline shell from the workflow in an isolated directory using synthetic environment inputs. They test ordinary prose, empty/whitespace bodies, valid names/suffixes/CRLF, bad names, spacing/case, misplaced/duplicate tags and shell-syntax data. Structural assertions retain untrusted-input plumbing, bot exemption, event types and read-only permissions.

## Risks / Trade-offs

A lane-bound author could omit its declaration. The global protocol already forbids that; this check cannot prove launch provenance. Requiring every PR to invent an attribution would violate the in-force rule and would not fix that limitation.

## Migration Plan

Merge the normal reviewed workflow correction, then refresh blocked PRs onto main so the updated check executes. Keep the same required check name. Roll back by a reviewed revert if behavior differs from the delta; no protection toggle is part of rollout.

## Implementation Handoff

Only [Speckit tasks](../../../specs/041-conditional-lane-check/tasks.md) enumerate implementation work. This packet is not an approval to change any other gate.
