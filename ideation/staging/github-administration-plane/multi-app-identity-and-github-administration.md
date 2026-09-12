# Staged: Multi-App Identity Tiering and GitHub Administration Plane

Status: superseded
Superseded by: openspec/changes/archive/2026-07-14-add-github-app-identity-tiers (openxFactory) and 2026-07-15-add-github-administration-workflow (OpsxFactory)
Kind: architecture
Summary: Separates the content-only GitHub App identity from a new
administration-tier App identity and locates GitHub administration in
OpsxFactory as a managed platform; both exit changes are realized and
archived — retained as provenance.
Topics: github-administration, app-identity-tiers, roles-authority-model, opsxfactory, branch-protection
Repository context: openxFactory (neutral) with an OpsxFactory-owned realization
Staging ID: openxFactory:staging:github-administration-plane
Source: xFactory family decision 2026-07-10 (review-lane first live run exposed
the factory App holding org-wide Contents:write and bypassing branch protection)

The family currently has one GitHub App identity (`openxfactory`) that both does
content work (reports, review-record PRs, pin syncs) and, because it was granted
org-wide `Contents: write`, can push to and bypass protection on any family repo.
That conflates two authority tiers and gives the content identity control-plane
power it should not have. This topic separates them and puts GitHub
administration where it belongs: OpsxFactory, the IT-operations factory that
already administers managed platforms (Entra, Intune, endpoints).

## Claims

1. **GitHub is a managed platform, and OpsxFactory administers platforms.** The
   GitHub org is a `platform_tenant` subject under the promoted OpsxFactory
   service-subject model — the same subject kind as an Intune or M365 tenant.
   Branch-protection rules and org rulesets are `endpoint_management`-style
   desired-state artifacts. GitHub administration is therefore the SAME pattern
   as the Cloud PC / Intune work, not a new one.
2. **Separate content identity from administration identity (separation of
   duties).** A content App (existing `openxfactory`: Contents + Pull requests
   write) does factory work under the rules. A distinct administration App
   (new, operated by OpsxFactory: Administration write + org rulesets) sets the
   rules. Neither can escalate the other: the App that does work cannot change
   the rules; the App that sets rules does no content work.
3. **Correction — a GitHub App cannot install another App.** App installation is
   an org-owner action; there is no App permission for it. The intent is
   reframed: OpsxFactory owns the *installation and app-permission policy* as
   governed records, and its administration App enforces the control plane it
   *can* manage via API — org/repo rulesets and branch protection.
4. **Rules-as-code, gated by the review lane.** Branch-protection rulesets live
   as versioned config in a repo; changes to them go through the governed review
   lane and the ratify gate; the administration App applies only reviewed
   config. This closes the loop non-circularly: the review lane gates changes to
   the very protections that enforce the review lane.
5. **Least authority per App, custody per credential.** Each App's private key
   is vaulted (openxFactory credential-contracts / Key Vault), its actions
   audited, and its permission set is exactly its tier — the administration App
   (which can un-protect main) gets the strongest custody.
6. **Extends, does not replace, the promoted roles-authority model.** The
   content/administration App tiering is a neutral authority-boundary addition;
   the GitHub-as-managed-platform realization is OpsxFactory-owned.

## Scope note (added 2026-07-14)

This topic governs GitHub administration for Opensoft's own vendor build org
(`opensoft` — the family repo: openxFactory + the five `xFactories/*` domain
templates + `installs/*`). It does NOT cover GitHub hosting/administration for
a client's deployed tenant repo. Client-tenant GitHub topology is a per-client
decision (client's own GitHub org vs. a customer repo hosted inside Opensoft's
org) that routes through the `client-infrastructure-liaison` staging topic's
three execution bindings (customer-managed / managed-host / full OpsxFactory)
as a `client_infrastructure_request` dependency, not through this topic's
administration App. The distinction matters because OpsxFactory is itself an
optional purchase — it cannot be assumed present in every client's install the
way it is in Opensoft's own vendor org.

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

No conflicts recorded.

## Open questions — resolved 2026-07-14

A research pass (six parallel investigations, one per question, plus a
synthesis/consistency pass) produced recommendations for all six; Brett
reviewed and ratified all six below. Q1 and Q2 required a correction after the
research pass surfaced the vendor-org-vs-client-tenant scope gap — see the
callouts below and the Scope note above.

1. **One OpsxFactory administration App, or several scoped ones (e.g. rulesets
   vs installation-policy vs repo-settings)?**
   → One administration App (distinct from the content App `openxfactory`),
   bundling GitHub's `Administration` (repo-level) + `Organization
   administration` (org-level) permissions. GitHub has no finer-grained
   permission to split those functions along — both hypothetical splits would
   request the identical underlying permission, so separate Apps would only
   multiply custody surfaces with no technical narrowing. Narrow authority at
   the runtime_capability_grant layer instead (short-lived, workflow-scoped,
   human-approved grants) plus GitHub's native "selected repositories"
   installation targeting.
   **Correction (2026-07-14):** this answer is scoped to Opensoft's own
   vendor org only. It assumes an OpsxFactory-owned App is always present to
   be the administering identity — true for Opensoft's own build org, not
   true for a client tenant that hasn't purchased OpsxFactory. Client-tenant
   GitHub administration is NOT this topic's concern; it routes through
   `client-infrastructure-liaison`'s three execution bindings, each with its
   own App identity (client's own App in the customer-managed case,
   Opensoft's admin App in the managed-host case, the client's own purchased
   OpsxFactory instance's App in the full-OpsxFactory case).

2. **Org-level rulesets (central, one enforcement across all family repos)
   vs. per-repo branch protection?**
   → Org-level rulesets, targeted via explicit "manually selected
   repositories" (never name-pattern-only — 3 of 12 candidate repos don't
   contain "Factory" in their name). Confirmed non-blocking for Opensoft's own
   org via a live `gh api orgs/opensoft` check: plan.name = enterprise.
   **Correction (2026-07-14):** org-level rulesets require a GitHub Team or
   Enterprise org plan — not available on Free. This holds for Opensoft's own
   org (confirmed Enterprise) but cannot be assumed for a client tenant in the
   customer-managed model, where plan tier varies. Repository-level rulesets
   have their own gate (Free: public repos only; Team/Enterprise: all repos),
   and even classic branch protection loses bypass-actor restriction
   granularity below Team/Enterprise. The capability's "plan" phase must
   therefore probe the target org's actual plan (`GET /orgs/{org}`) and select
   from a three-tier ladder — org ruleset → repo ruleset → classic branch
   protection — rather than assuming org rulesets are always available, and
   must record which tier was used plus any protection that tier couldn't
   achieve (e.g. no bypass-actor restriction on a Free-plan private repo) as
   an explicit degraded-capability note. This requirement applies to the
   client-tenant execution path only; Opensoft's own org stays on org-level
   rulesets as originally answered.

3. **Is the rules-as-code change gated/applied through the
   `endpoint_management` workflow generalized to GitHub, or a dedicated
   github-administration workflow?**
   → Dedicated `github_administration` write workflow, extending the
   already-existing (currently read-only) `github-admin` OpsxFactory command
   class, reusing `endpoint_management`'s plan/apply/verify/recover pattern
   without touching its file/spec. Ratified as researched — no change.

4. **Credential custody and rotation for the administration App key?**
   → Apply DTN-004's five credential-contract record kinds unchanged, at the
   family's strictest existing tier: new `github_administration_app`
   requirement (15-min grants, human + domain approval), an Opensoft-owned Key
   Vault binding, a new fixed 90-day max key age on top of existing
   trigger-based rotation (Brett to confirm the exact figure), a GitHub
   Actions Environment with required reviewers as the human gate, and fast
   App-installation-suspension as first containment on suspected exposure.
   Ratified as researched — no change.

5. **Scope: which repos and org settings the administration App may touch;
   explicit prohibited actions?**
   → Two-tier repo scope for Opensoft's own org: Tier 1 in scope now (7 repos
   — `xFactory`, `openxFactory`, and the five domain repos), Tier 2 deferred
   (the 5 `installs/*` repos, matching a boundary the review lane already
   enforces in code today). Settings: rulesets/branch-protection read+write
   only; explicit prohibited-actions list (no repo lifecycle, no
   org/team/billing, no Actions secrets, no Contents/PR write, no
   self-permission changes). Enforced at the OpsxFactory workflow/credential
   layer, since GitHub's permission model itself is too coarse to enforce
   these exclusions. Ratified as researched — no change.

6. **Is GitHub administration a second profile of the `endpoint_management`
   envelope, or its own capability?**
   → Own capability, sibling to `endpoint_management`/`entra-admin`/
   `dns-admin`, realized by extending the existing `github-admin` command
   class. Independently confirmed by Q3 — no contradiction. Ratified as
   researched — no change.

## Interim state (already applied, to be superseded by the governed path)

- 2026-07-10: a manual codexFactory `main` ruleset now requires a PR + one
  approval with OrganizationAdmin bypass, blocking bot direct pushes and
  force-push/deletion. This is a stop-gap; the durable version is
  OpsxFactory-administered org rulesets applied from reviewed config.
- The `openxfactory` App was granted org-wide `Contents: write` +
  `Pull requests: write` to unblock review-record PR delivery. Under this
  topic, that content App's authority stays content-only and the
  administration authority moves to the new OpsxFactory App.

## Exit

All six open questions are resolved (see above) — ready to propose.

1. `add-github-app-identity-tiers` (openxFactory) — ratified and **archived
   2026-07-14** as `openspec/changes/archive/2026-07-14-add-github-app-identity-tiers/`;
   its two new requirements and the structural-parking amendment are folded
   into `openspec/specs/roles-authority-model/spec.md`, and
   `docs/roles-and-authority.md` carries the identity-tiering description.
2. `add-github-administration-workflow` (OpsxFactory) — ratified 2026-07-14,
   realized and **archived 2026-07-15** as
   `openspec/changes/archive/2026-07-15-add-github-administration-workflow/`
   (six requirements folded into the `github-administration-workflow` spec).
   Full lifecycle complete: deterministic realization merged (PR #9,
   `7860bc1`, 260 tests, 3-lens adversarial review); admin App
   `opsxfactory` (4300489) registered + installed on the 7 Tier-1 repos;
   environment-gated live apply created org ruleset 18962101 (PR+1,
   OrgAdmin-only bypass); nightly doc-health adapted to PR-flow; content
   App's always-bypass removed from ruleset 18834180 and its installation
   narrowed from all-367 to 12 repos. **The 2026-07-10 incident is closed.**
   Follow-ups live outside this topic: 5 minor PR #9 findings; the
   Hermes/Merge Master autonomous approver (retires Brett's daily
   nightly-PR approval chore).

Two OpenSpec changes:

1. Neutral (openxFactory): extend `roles-authority-model` with GitHub App
   identity tiers (content vs administration) and per-App credential custody.
2. OpsxFactory: a `github-administration` capability — the GitHub org as a
   managed `platform_tenant` subject, a dedicated `github_administration`
   workflow extending the existing `github-admin` command class (sibling to,
   not a profile of, `endpoint_management`), the administration App identity,
   branch-protection/ruleset desired-state with a plan-tier-aware
   org/repo/classic ladder, installation/permission policy, and the
   rules-as-code governance loop. Scope this change explicitly to Opensoft's
   own vendor org (see Scope note); client-tenant GitHub administration is out
   of scope here and belongs to `client-infrastructure-liaison`.
