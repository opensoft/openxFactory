# Design: Council-Clearance Gate-Rule Template

## Context

Everything load-bearing here was decided in the 2026-07-23 first exercise
and Brett's accept-time ruling; this change organizes those decisions into a
neutral contract rather than making new ones.

## Decisions (inherited, not reopened)

### D1 — The clearable set is a static, owner-attributed allowlist
Q1 of the first exercise: deterministic, auditable, amendable only through
owner-accepted recorded events. The template requires every instantiation to
name the owning seat (codexFactory's was Lead Quality).

### D2 — A v1 clearable set admits one lowest-risk condition class
Q4 of the first exercise: codexFactory started with docs-only overflow
alone; widening is a normal rule amendment through the same council, never
an inline edit.

### D3 — The never-clearable floor is part of the pattern, not the instance
Security-touching failures, check failures, and identity mismatches park for
the human in every instantiation. An instance may widen its floor, never
narrow it.

### D4 — Instantiation IS a Gate-Rules Council exercise
Widening what auto-clears is a per-repo gate rule, so the template's
instantiation checklist is the recorded council convening: seat
verifications, allowlist ruling, transport blessing, authority
acknowledgement — the moves of the recorded 2026-07-23 rehearsal
(`hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`).

### D5 — Instances ship dormant behind an activation gate
`configured_but_inactive` until council orchestration exists in the
executing lane; a clearance path with no orchestrated council would be a
bypass.

## Ratification precondition

Brett's accept note fixed the extraction discipline: rule-of-three — the
template is ratified when a SECOND sweep or repo names itself as wanting a
tier-2 rule. This proposal packet may exist ahead of that trigger (it is the
organized template a second consumer starts from), but it returns to staging
rather than ratifying while the trigger is unfired.
