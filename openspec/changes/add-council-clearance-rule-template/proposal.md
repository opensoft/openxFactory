---
code_surface: none
target_release: none
Status: draft
---

# Proposal: add-council-clearance-rule-template

## Why

The Gate-Rules Council's first exercise (2026-07-23) ratified a tier-2
council-clearance rule for codexFactory's nightly doc-health rolling PR:
when the Merge Master's conjunctive tier-1 envelope fails on a condition in
a declared *council-clearable* set, the merge-readiness council convenes and
its unanimous `ready` verdict — pinned to the exact head SHA — lets the
Merge Master approve, while security-touching failures, check failures, and
identity mismatches stay never-clearable and park for the human. That rule
shipped rules-as-code (`add-nightly-sweep-council-clearance`, rule YAML +
`council_clearance.py`, `configured_but_inactive`), and its authoring left
behind every generalizable element: the clearable-set boundary as an
owner-attributed static allowlist, the anti-normalization rule (a condition
cleared repeatedly stops being clearable and parks with a fix-the-generator
flag), and the required activation gate until council orchestration exists
in the executing lane.

The accepted possible
`pos-derived-reusable-tier-2-council-clearance-pattern-beyond` (Brett,
2026-07-23) names the abstraction: the shape is repo-agnostic, and the next
autonomous sweep that wants a tier-2 path should instantiate a template
through its own Gate-Rules Council exercise rather than re-derive a one-off
carve-out. The staged topic `tier2-council-clearance-pattern` (organized
2026-08-05 from Brett's promote-to-staging commission) holds the pattern
content this change promotes.

## What Changes

- ADD a neutral `council-clearance-gate-rule` capability: the tier-2
  council-clearance pattern contract — declared clearable set with a named
  owning seat, SHA-pinned unanimous council verdict, never-clearable floor,
  anti-normalization rule, and a required `configured_but_inactive`
  activation gate — plus the instantiation checklist (each instantiation is
  a recorded Gate-Rules Council exercise).
- CITE codexFactory's ratified rule as the conforming first instance; the
  rule itself and `workflow-gate-contract` are not modified.

## Impact

- New capability spec: `council-clearance-gate-rule` (this change's delta).
- No code surface, no contract-schema release, no domain-repo change; the
  first instantiation already conforms by construction.
- The staged topic's exit condition (rule-of-three: author when a second
  consumer names itself) is carried as this proposal's ratification
  precondition — the packet exists so the second consumer starts from a
  template, and it is not ratified before that trigger fires.
