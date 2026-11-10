# Implementation Plan: Conditional Lane Check

Status: draft
Branch: `041-conditional-lane-check`
Date: 2026-11-10
Spec: [feature](spec.md)
Governance: [realization packet](../../openspec/changes/honor-conditional-lane-attribution/proposal.md)

## Summary

Implement the in-force conditional declaration rule in the existing inline workflow shell and prove its behavior with regression tests of those exact bytes.

## Technical Context

GitHub Actions shell; existing Python pytest/PyYAML test tooling. No new dependency, network call, checkout or persistent store. The PR body remains an environment input. Preserve each repository's bot exemption and existing check identity.

## Constitution Check

| Principle | Assessment |
| --- | --- |
| Governance before implementation | Amendment 21 supplies the existing rule; the owner's 2026-11-10 instruction commissions its realization. OpenSpec and this feature precede code. No new ratification is fabricated. |
| Neutral boundaries and contracts | Repository CI only; no product/domain contract changes. |
| Fail-closed evidence and validation | Supplied malformed declarations refuse; actual shell and structural invariants are tested. Local, hosted and review results stay distinct. |
| Single-operator honesty | No two-human control, invented identity or self-approval is introduced. |
| Lane discipline | This session is outside a lane. Amendment 21 scopes older unconditional attribution summaries; overlap search found no competing lane-check PR. |
| Append-only records and owner acts | No ratified packet, owner checkbox or constitution text is rewritten. |
| Artifact, secret and release discipline | No credentials, host-specific committed paths, release allocation or pin changes. Measured file-count changes are disclosed. |

## Project Structure

- `.github/workflows/lane-line.yml`: existing inline body validation.
- `tests/lane_line/test_conditional_lane_line.py`: execution and structural cases.
- `openspec/changes/honor-conditional-lane-attribution/`: governance record and delta.
- `specs/041-conditional-lane-check/`: specification, plan, tasks and evidence.

## Phase 0: Research

[Research](research.md) resolves declaration detection, bot behavior and untrusted-input handling using the existing source and Amendment 21.

## Phase 1: Design

[Data model](data-model.md) covers the transient body/result only. There is no external interface or runtime schema to publish. [Quickstart](quickstart.md) gives verification commands. Post-design constitution check: no new exception.

## Verification and Landing

Run focused behavior tests, required OpenSpec validation and affected measured probes. Push, request exact-head Codex review, wait for required hosted checks and use a normal reviewed merge. Refresh the design PRs after the correction lands. Respect existing merge holds; no required check is bypassed.
