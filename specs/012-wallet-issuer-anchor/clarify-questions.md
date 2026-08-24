# Clarification Record — 012-wallet-issuer-anchor

Session parameters: architect persona answers via `opencode run --agent architect`
(read-only); researcher persona for validator/corpus facts; doctrine-touching answers
escalate to convener. Implements the ratified requirement *"Every review-authority
grant names its issuer, and a root grant's issuer is anchored outside the register"*
(`openspec/changes/add-wallet-carried-review-authority/specs/review-authority-intake/spec.md:84-106`),
substrate item S2.

## Session 2026-08-23 → 2026-08-24

### Q0 — What the ratified text already fixes (pre-consult grounding)

**Facts (researcher + ratified-text read)**: today the validator reads `issued_by`
through zero rules — S2 is the field's first real enforcement. The ratified intake
spec already prescribes most mechanics: `issued_by` SHALL be named on every grant;
absence of `parent_grant_ref` defines a ROOT grant; a root grant's issuer is the
responsible operator; the anchor is the **Human Escalation Contract cited in the
register**, not a register row; machine-named root issuers are refused.
**Disposition**: no consult spent on settled ground; only the remaining forks
escalated.

### Q1 — Review-authority class marker (what makes a grant "review-class")

**Architect**: class marker = scope `acts` vocabulary membership, detected through a
named validator constant for the canonical review act token (`review`); confirmed by
architect mini-consult against the ratified vocabulary. Class detection reads scope
content and nothing else — presence of the token in any acts list triggers class
membership by design.
**Disposition**: encoded — FR-001/FR-002.

### Q2 — Anchor representation and matching semantics

**Architect**: anchor = validator constant citing HEC `docs/roles-and-authority.md:103-140`
as its authority — the code points at the standing record rather than duplicating it.
Legacy org-level string `opensoft`, carried by every existing example, does NOT
grandfather into the anchor: one negative specimen proves refusal specifically.
Three negative specimens total (`omits-issued-by`, `root-issuer-is-a-machine`,
`root-issuer-says-opensoft`), each declaring `expected_failure`, detail pins where
applicable, and REQ attribution.
**Disposition**: encoded — FR-004/FR-005.

### Q3 — Exact operator identity token (convener escalation)

**Gap**: the ratified HEC record carries no identity token, so the exact accepted
root-issuer string needed the convener's word.
**Convener**: **`Brett Heap`** — exact match, fail-closed, no whitespace/case
normalization (identity strings do not get fuzzy).
**Disposition**: encoded — FR-004, Key Entities, US2 acceptance scenario 3.

## Session totals

1 architect round (+1 mini-consult) · researcher facts consult · 1 escalation to
convener (resolved) · stopped on resolution rule. No [NEEDS CLARIFICATION] markers
remain; checklist all-pass (see checklists/requirements.md).
