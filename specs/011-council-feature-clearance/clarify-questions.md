# Clarification Record — 011-council-feature-clearance

Session parameters: architect persona answers via `opencode run --agent architect`
(model opencode/x-preview-f-free, read-only); researcher persona for corpus facts;
cap effectively unlimited per owner override 2026-08-23 with stop-on-resolution rule;
doctrine-touching answers escalate to convener.

## Session 2026-08-23

### Q1 — Tranche scope and classification intent
**Asked**: First-tranche repos (xfactory-only / xfactory+openxFactory / all-governed)?
Feature-PR verdicts advisory or clearable?
**Architect**: `xfactory+openxFactory ; advisory` — openxFactory is the ratified pilot
home where real feature PRs occur; zero evidence base exists for any clearable class,
and flipping classification intent is the tier-2 activation gate-flip reserved to the
convener. Floor untouched.
**Disposition**: encoded — FR-006 rewritten; Assumptions resolved inline.

### Q2 — Expressing open-ended feature classes under exact-string refs
**Facts (researcher)**: schema v1 requires exact `expected_head_ref`;
`additionalProperties: false`; no classification-intent field; no repo-count limit;
human authors not forbidden. Tier-1 resolves refs FROM config.
**Asked**: A) codexFactory schema amendment adding head_ref_pattern · B) intake-per-
effort exact-ref entries · C) relax ref binding for author+base+path matching.
**Architect**: `B ; SCHEMA-CHANGE: none` — C refused outright (widens spoofing surface
against Principle VII); A refused as blanket pre-authorization plus premature cross-repo
chain; B is the intake-act doctrine read literally. Successor note: if pilot friction
proves real, promote `head_ref_pattern` as its own evidence-backed change.
**Disposition**: encoded — FR-006 rewritten to per-effort entries; author-expectation
assumption made per-entry; successor note recorded.

## Session totals
2 consults · researcher facts consult · 0 escalations to convener · stopped on resolution rule.
