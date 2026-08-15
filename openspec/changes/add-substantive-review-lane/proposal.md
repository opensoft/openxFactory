---
code_surface: xFactory aggregation repo (.github/workflows/merge-master-approval.yml + .github/merge-approval-envelope.yml — additional substantive candidate classes and generalized council-verdict consumption; per-repo instances of these files for repos beyond opensoft/xFactory), codexFactory (hermes/domain/review-councils/gate-rules.yaml candidate-class + risk-tier additions, merge_readiness_council scope generalized to substantive human- and agent-authored PRs), openxFactory (this spec delta on roles-authority-model; opensoft/openxFactory as the pilot repo's ruleset + workflow wiring). This change's own diff is the spec delta; the workflow/council/ruleset realization across the three surfaces is downstream, tracked in tasks.md and archived only on merged, green realization evidence per release-realization.
target_release: none (no contract-bundle involvement — this generalizes the roles-authority-model authority doc and cross-repo rules-as-code, not a `contracts/schemas/` artifact; realization lands as workflow, council, and ruleset changes in the affected repos)
---

# Proposal: add-substantive-review-lane

Status: draft — not yet ratified. Authored 2026-08-15 from verified current
state (`.openspec.yaml` origin block); the open questions below are declared
for review, not decided by this proposal.

## Why

Governed xFactory repos carry review-required rulesets. Today there are
exactly two ways past one: a human review, or an `--admin` bypass.

A governed, accountable AI reviewer already exists, and it is already live —
but only for one narrow lane. codexFactory's `gate_rules_council`
(lead-architect + lead-security + lead-quality + the tenant
company-policy-lead seat) sets per-repo merge/gate rules
(`per_repo_gate_rules`, `enforcement: merge_master_operator`); its
`merge_readiness_council` (lead-quality + lead-security + lead-integration)
judges individual pull requests `ready | blocked | needs_human_review`; and
the aggregation repo's `merge-master-approval.yml` +
`merge-approval-envelope.yml` is a mechanical GitHub-App operator that
consumes a signed, identity-bound council-verdict check-run
(`council-verdict/merge-readiness`, App 4397053) and, when the low-risk
envelope clears, mints a dedicated merge-master App token — never
`GITHUB_TOKEN` — and posts a real `APPROVE` review as `codexfactory[bot]`.
This is not a design sketch: fully autonomous council deliberation ran
2026-08-14 — three seats, written rationales, unanimous READY, a signed
check-run, a real GitHub approval (records in
`xFactories/codexFactory/hermes/domain/review-councils/records/`, proven on
xFactory PRs #85 and #100).

**The gap is that the candidate class is rules-as-code-limited to almost
nothing.** The one entry in `.github/merge-approval-envelope.yml`
(`doc-health-nightly`) matches only `expected_author: openxfactory[bot]`,
`expected_head_ref: doc-health/nightly`, `path_allowlist: [health/**]`, and
`target_repos: [opensoft/xFactory]`. The one council-clearable condition is
`docs_only_path_overflow`. No human-authored PR, no other agent-authored PR,
and no repo other than the aggregation repo itself can ever receive a
council-cleared approval — and openxFactory, the repo carrying the neutral
contracts this whole family depends on, has no merge-master workflow and no
persona/council instantiation of its own at all.

This proposal generalizes the proven machinery: extend the council + Merge
Master pattern so substantive PRs — human- and agent-authored, across
governed xFactory repos — can receive a team-member-equivalent, accountable,
policy-and-best-practices review from Hermes-stack personas, replacing
`--admin` bypasses without ever letting the mechanical enforcer originate a
judgment it does not already hold as a verdict.

## Decided principles (encoded as requirements; not reopened by this change)

1. **Councils judge; Merge Master stays the mechanical enforcer.** The
   generalization adds candidate classes and council scope — it never moves
   judgment into the enforcer.
2. **Accountability is the product.** Every seat produces a written
   rationale; the verdict transports as a signed, identity-bound check-run;
   an audit artifact records inputs, rules version, and verdicts; the
   approving review is cast by a dedicated reviewer/merge-master App
   identity, never `GITHUB_TOKEN`, never the author's identity.
3. **Identity separation.** The reviewing council and enforcing identity
   must be distinct from the PR author's identity (human or agent); review
   rules always evaluate from the base branch.
4. **Fail-closed.** Anything outside a defined candidate class, any
   non-unanimous or conditioned verdict, any stale/missing rule set → no
   approval, park with explanation; `needs_human_review` escalation is
   always available and some classes may be declared human-only by the
   gate-rules council.
5. **Substantive candidate classes.** The `gate_rules_council` (which
   includes the tenant company-policy-lead seat) defines per-repo candidate
   classes covering substantive human- and agent-authored PRs, each with a
   risk tier and a clearance rule — the council reviews for company-policy
   compliance AND domain best practices.
6. **Pilot.** `opensoft/openxFactory` is reviewed by codexFactory's councils
   (the software-engineering domain reviewing the engineering-contracts
   repo), then extended per adoption.

## What Changes

- **`roles-authority-model` (ADDED requirements)** — six new requirements
  generalizing the existing "Low-risk enforcement envelope" and "GitHub App
  identity tiers" requirements into a named substantive review lane:
  authority generalization, gate-rules-council-defined candidate classes,
  accountability (rationale + signed check-run + audit artifact + dedicated
  identity), reviewer/enforcer identity separation from the author,
  fail-closed envelope generalization, and the pilot repository/reviewing
  domain declaration. See `design.md` for why `roles-authority-model` is the
  target rather than `workflow-gate-contract` or a new capability.
- **Downstream realization (named, not performed by this change; tracked in
  `tasks.md`)**:
  - codexFactory's `gate-rules.yaml` gains a `risk_tier` and `clearance_rule`
    field per candidate class, and its `gate_rules_council` record for
    `opensoft/openxFactory` names the pilot's substantive candidate classes.
  - The aggregation repo's `merge-master-approval.yml` and
    `merge-approval-envelope.yml` generalize their single-candidate,
    single-repo matching to a candidate-class list keyed by
    `(repo, author-shape, path/diff-shape, risk_tier)`, with the
    council-verdict transport and anti-spoofing binding unchanged.
  - `opensoft/openxFactory` gets its own ruleset wiring (App approval
    satisfying its required-review or required-check-run configuration) and
    its own workflow instance, since `pull_request_target` events fire in
    the repo the PR is opened against.
  - A `gate_rules_council` record and, on first live candidate, a
    `merge_readiness_council` record for an `opensoft/openxFactory` PR,
    mirroring the 2026-08-14 xFactory precedent.

## Open questions (declared here, not decided by this proposal)

- **Rollout order beyond the pilot.** Which repos come next, and in what
  order, is not decided here.
- **Persona home for non-engineering domain repos.** Do Medx/Ledgerx/Ops/Adx
  instantiate their own review personas, or does codexFactory review all
  *software* changes regardless of which repo they land in? Both are
  consistent with the requirements above; this proposal picks neither.
- **Company-policy-lead seat scope.** Whether the company-policy-lead seat
  joins per-PR `merge_readiness_council` deliberation, or remains rules-only
  (as it is today, seated only in `gate_rules_council`), is undecided.
- **Ruleset interaction shape per repo.** Whether App approval satisfies a
  required-review check or a required check-run, and whether human review
  remains an always-available alternate path per repo, is a per-repo
  ruleset-wiring decision this proposal does not make.
- **Risk-tiering taxonomy.** The candidate-class risk tiers (for example
  docs-only / config / contract / runtime-code) and which tiers are ever
  eligible for autonomous clearance are not enumerated here; the
  requirements above only require that every class DECLARE a risk tier and
  a clearance rule, not what the tier vocabulary is.

## Capabilities

### Modified Capabilities

- `roles-authority-model`: six ADDED requirements generalizing the
  substantive-review authority, accountability, identity-separation, and
  fail-closed envelope machinery already partially present (Merge Master's
  low-risk envelope, GitHub App identity tiers) into a named, extensible
  lane, plus a declared pilot.

## Impact

- No change to any `contracts/schemas/` artifact, `contracts/manifest.yaml`,
  or `contracts/CHANGELOG.md` — this is a roles-authority-model spec delta
  plus cross-repo rules-as-code realization, not a neutral contract bundle
  release.
- No existing candidate class, workflow, or council record is removed or
  altered by this change; `doc-health-nightly` / `docs_only_path_overflow`
  continues operating exactly as proven 2026-08-14.
- Downstream realization touches three repos (xFactory aggregation,
  codexFactory, openxFactory) and is tracked, not performed, by this change
  — see `tasks.md` §3–§5, each task marked as its own successor realization
  step with archive-on-evidence discipline per `release-realization`.
- No `--admin` bypass is removed by this proposal; it is a precondition
  (the substantive review lane existing and being wired for a given repo)
  for later retiring bypass usage on that repo, which is out of scope here.

## Out of scope, deliberately

- Deciding the risk-tiering taxonomy, rollout order, non-engineering persona
  homes, company-policy-lead per-PR seating, or the per-repo ruleset
  interaction shape — all five are declared as open questions above, for a
  human or a follow-on change to settle.
- Retiring any existing `--admin` bypass usage on any repo — this proposal
  only makes a governed alternative available; removing bypass access is a
  separate, per-repo policy decision.
- Any change to the council-verdict transport mechanism itself (the signed
  `council-verdict/merge-readiness` check-run, its anti-spoofing App-identity
  binding, or the merge-master token-minting flow) — the proven transport is
  reused as-is; see `design.md` Decision C.
- Non-GitHub enforcement surfaces (client-tenant infrastructure) — this
  lane governs Opensoft's own vendor build org only, consistent with the
  existing "GitHub App identity tiers" requirement's scope.
