# Research — 011-council-feature-clearance

## R1 — Tranche and classification rulings

Clarify Q1 (architect): first tranche = BOTH `opensoft/xFactory` and
`opensoft/openxFactory`; verdicts ADVISORY-only for every first-tranche class.
Clarify Q2 (architect): mechanism = **intake-per-effort** — one reviewed exact-ref
envelope entry per opened feature effort; ref-pattern schema amendment refused as
blanket pre-authorization; relaxing ref binding refused as spoofing surface.

## R2 — Envelope schema facts (researcher)

Schema v1 (codexFactory-owned, consumed at pinned version, UNCHANGED here): candidates
require `id`, `target_repos`, `expected_author`, `expected_head_ref` (EXACT string),
`path_allowlist`; `additionalProperties: false` — no classification-intent field, no
ref patterns, no repo-count limit, human authors not forbidden. Tier-1 resolves head
refs FROM the config (`--list-head-refs`). Consequence: an entry's mere presence makes
the PR a classification subject; advisory-vs-clearable posture lives in tier-2 state,
not the envelope.

## R3 — Tier-2 posture discovery (resolves decision #3's contradiction)

The xFactory aggregation README carries a section titled **"Merge Master tier-2
council clearance — ACTIVE"**, and tonight's dispatched approval run executed a job
named "…council clearance (**tier 2, active**)". The registration runbook §7 ("rule
ships `active: false`, report-only") predates activation. **Operational consequence:
the tier-2 autonomy chain is LIVE** — a classified candidate whose verdict is
unanimous-ready, within its path allowlist, and inside the consecutive-clearance
chain can be approved autonomously by the merge-master App.

## R4 — ESCALATION: classification mechanics for human-authored feature candidates

Because tier-2 is ACTIVE, adding a live envelope entry for a human-authored feature
PR is not merely "advisory recording": if the entry's facts ever prove clearable
(green checks, exact head, path allowlist satisfied, verdict unanimous-ready,
consecutive-clearance threshold met), **the merge-master App could autonomously
approve human feature code**. The convener's advisory-first intent cannot be encoded
in the envelope (schema fact, R2) and must be resolved by him. Options escalated:

- (a) Land live entries under ACTIVE tier-2, accepting eventual autonomous approval
  for narrowly-scoped classes;
- (b) Confirm/restore report-only posture for the new classes specifically (may
  require a codexFactory-side rule or schema `classification_intent` successor);
- (c) Defer ALL live entries until the classification mechanics ruling lands; land
  only the safe scaffolding now (template block, lane parameterization, docs).

Per the session escalation guardrail, (this orchestrator) implements (c)'s safe
subset by default and presents (a)/(b) for the convener's explicit ruling. No live
entry for any human-authored PR lands without that ruling.

## R5 — Pilot/refusal subject selection (conditional on R4 resolution)

Existing open xFactory PRs surveyed: **#141** (adds `.github/workflows/
dashboard-image-worker.yml` — assembly-class; ideal named-refusal demonstration),
#22 (pointer restoration — lowest-risk pilot candidate), #21, #5. Selection executes
only after R4 lands; the rehearsal procedure is fully specified in quickstart.md.

## R6 — Lane repository parameterization

`council-convening-lane.yml` sets `REPO: ${{ github.repository }}` at three sites
(140/308/370). Generalization: add optional `pr_repo` dispatch input defaulting to
`github.repository` (byte-identical behavior for existing callers), propagated to
all three sites; emission token already derives scope from the resolved target repo
(runbook §2), so second-repo emission fails closed — naming the missing App
installation — until the operator extends installation (FR-008 prerequisite honored).
