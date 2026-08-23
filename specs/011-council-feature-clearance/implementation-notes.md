# Implementation Notes — 011-council-feature-clearance

## Round 1 — Safe-subset implementation (T001–T004, T007–T008)

Cross-repo realization landed on `opensoft/xFactory` branch
`011-council-feature-clearance`: envelope comment-template (parsed doc verified
semantically unchanged), lane `pr_repo` parameterization, README coverage/intake
section. openxFactory side: this spec artifact set.

Reviewer (code-reviewer, gpt-5.6-terra) round 1: REVISE with one MAJOR — token-mint
site (`target_repo`) remained hardwired while resolve/classify followed `pr_repo`.
**Fixed**: same resolved-repo expression applied; post-fix sweep confirms expression
at exactly 4 sites, remaining bare `github.repository` occurrences intentional
(RUN_URL self-references + org-scoped owner).

## Gate status (endpoint degradation disclosure)

Model endpoints degraded repeatedly during this session (ox-alpha and GPT routes:
multiple 300–600s hangs). Status honesty:

- Structural verification battery: PASSED (objective, local): YAML parses; envelope
  schema-valid vs codexFactory schema v1; parsed doc unchanged by comment append;
  pr_repo input present; resolved-repo expression at 4 sites; injection surface
  assessed (all REPO consumptions quoted).
- Reviewer round-1 REVISE finding: ADDRESSED VERBATIM; re-verdict PENDING endpoint
  recovery.
- QA adversarial round: PENDING (two timeout attempts).

Per house discipline these are declared-pending, not silently waived; re-run both
consults when endpoints recover, before merge or as PR review commentary.

## Escalation (convener ruling required before Phase 3 tasks)

Classification mechanics for human-authored feature candidates under ACTIVE tier-2:
options (a) accept eventual autonomous approval for narrowly-scoped classes;
(b) restore report-only posture for new classes specifically (codexFactory-side
successor); (c) defer all live entries until ruled. Safe subset landed under (c)
provisionally; live entries (T005/T006/T010) blocked pending ruling.
