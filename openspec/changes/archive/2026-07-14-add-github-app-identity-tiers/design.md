## Context

A single GitHub App (`openxfactory`) currently does both content work
(reports, review-record PRs, pin syncs) and holds org-wide `Contents: write`
+ `Pull requests: write`, which also lets it bypass branch protection on any
family repo. This was exposed by the review lane's first live run on
2026-07-10. The already-ratified "Structural parking in external
enforcement" requirement (`roles-authority-model`) assumes branch
protection/rulesets reliably encode a fail-closed human gate, but the neutral
model never constrained which identity may reconfigure that enforcement —
that is the gap this change closes.

A parallel research and ratification pass (2026-07-14) already resolved the
open design questions this proposal draws from; full detail is recorded in
`ideation/staging/github-administration-plane/multi-app-identity-and-github-administration.md`
("Open questions — resolved 2026-07-14" and "Scope note" sections). An
interim stop-gap is already applied (2026-07-10): a manual codexFactory
`main` ruleset (PR + 1 approval, OrganizationAdmin bypass), still relying on
the same over-privileged content App underneath.

## Goals / Non-Goals

**Goals:**
- Establish, at the neutral authority-model layer, that any identity capable
  of modifying a structural human-review gate must be authority-separated
  from any identity performing ordinary content/workflow actions on the same
  surface.
- Define the resulting content-vs-administration GitHub App identity tiers
  and the administration tier's credential-custody obligations.

**Non-Goals:**
- Does not instantiate an actual second GitHub App, workflow, or command
  class — that is the sibling OpsxFactory-local change (`github-administration`).
- Does not define client-tenant GitHub administration (own GitHub org vs. a
  customer repo hosted inside Opensoft's org, and who administers it) — that
  routes through the staged `client-infrastructure-liaison` topic.
- Does not modify the `credential-contracts` schema itself; its five record
  kinds are reused unchanged.
- Does not prescribe repo scope, the rules-as-code workflow mechanism, or a
  plan-tier enforcement fallback ladder — those are OpsxFactory
  implementation decisions for the sibling change.

## Decisions

1. **One administration identity per operating org, not several scoped by
   function.** GitHub's App permission model has no permission finer than
   `Administration` / `Organization administration` to split rulesets from
   repo-settings from installation-policy along — both hypothetical splits
   would request the identical underlying permission (confirmed against
   GitHub's current permission documentation, 2026-07-14). Splitting into
   multiple App identities would only multiply custody surfaces (more
   vaulted keys, more rotation schedules) with no enforceable narrowing at
   the GitHub-permission layer. Authority is narrowed instead at the
   runtime-capability-grant layer (short-lived, workflow-scoped,
   human-approved), which `credential-contracts` already supports.
   *Alternative considered:* multiple Apps split by function — rejected
   because GitHub cannot express that split technically, and
   installation-policy in particular is not an App-holdable permission at
   all (App installation is an org-owner action).

2. **Extend the existing "Structural parking in external enforcement"
   requirement rather than write a wholly separate one.** That requirement
   already establishes GitHub branch protection/rulesets as the
   machine-readable declaration of a human gate; identity separation is a
   direct precondition of that guarantee holding — a content identity that
   can also touch branch protection makes "fail-closed against agent
   misbehavior" untrue in practice. Keeping both in one requirement keeps the
   fail-closed guarantee whole instead of splitting it across two
   independently-evolvable requirements.
   *Alternative considered:* a standalone requirement with no textual link
   to structural parking — rejected as weaker traceability between the
   incident and the guarantee it undermines.

3. **Credential custody reuses the existing `credential-contracts` shape
   unchanged, at the family's strictest existing tier.** DTN-004
   (`credential-contracts`) was already promoted shape-only, and the
   family's existing privileged-writer convention (`microsoft_endpoint_app_writer`,
   `microsoft_endpoint_policy_writer`: short-lived grants, human approval,
   exact effective scopes) already gives real, enforced narrowing. The
   already-ratified "Privileged deployment gate is structural" scenario in
   this same spec already names GitHub Environment required-reviewers as a
   structural human-gate mechanism, reusable here for the administration
   key's access gate instead of inventing a new dual-control primitive.
   *Alternative considered:* a new formal "tier" enum or dual-control record
   kind in the neutral credential schema — rejected as unnecessary
   governance surface when reuse already achieves the same effect.

## Risks / Trade-offs

- [Risk] Extending a ratified, in-force requirement could destabilize other
  domains already instantiating it (e.g. codexFactory's engineering merge
  gate). → [Mitigation] The added scenario is additive — a new precondition
  on the same requirement, not a removal or narrowing of any existing
  scenario — and no domain currently has more than one App identity to
  separate, so nothing existing is disrupted until the sibling change
  actually stands up a second identity.
- [Risk] This spec change alone does not close the actual security gap — the
  `openxfactory` App still holds org-wide `Contents: write` until the sibling
  change lands and narrows it. → [Mitigation] The sibling OpsxFactory
  `github-administration` change is scoped and ready to draft next; the
  interim manual ruleset (2026-07-10) remains the stop-gap meanwhile.
- [Risk] A future domain might read "identity" too narrowly (e.g. a single
  shared CI token treated as a single identity spanning both roles). →
  [Mitigation] The requirement text is enforcement-system-neutral ("any
  identity capable of modifying that enforcement configuration"), not
  GitHub-specific, so it generalizes without further amendment.

## Migration Plan

- No running-system migration is required by this change alone — it only
  extends a specification.
- Sequencing: land this neutral change first; the sibling OpsxFactory
  `github-administration` change instantiates the second App identity and
  narrows `openxfactory`'s permissions, at which point the interim manual
  ruleset stop-gap is superseded.
- Rollback: reverting this spec change has no runtime effect since nothing
  yet depends on it structurally; the sibling change's own migration plan
  covers reverting the actual App/permission changes if needed.
