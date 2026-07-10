# Staged: Multi-App Identity Tiering and GitHub Administration Plane

Status: staged
Kind: architecture
Repository context: openxFactory (neutral) with an OpsxFactory-owned realization
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

## Open questions

- One OpsxFactory administration App, or several scoped ones (e.g. rulesets vs
  installation-policy vs repo-settings)?
- Org-level rulesets (central, one enforcement across all family repos) vs
  per-repo branch protection — likely org rulesets, to confirm.
- How is a change to the rules-as-code gated and applied — through the
  `endpoint_management` workflow generalized to GitHub, or a dedicated
  github-administration workflow?
- Credential custody and rotation for the administration App key (per-App Key
  Vault bundle; the admin key is the highest-value secret in the family).
- Scope: which repos and which org settings the administration App may touch;
  explicit prohibited actions (must not disable protection without a reviewed
  change).
- Relationship to the OpsxFactory `endpoint_management` capability (the fleet
  change): is GitHub administration a second profile of the same
  desired-state/plan/apply/verify/recover envelope, or its own capability?

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

Two OpenSpec changes once details are settled (do NOT propose yet):

1. Neutral (openxFactory): extend `roles-authority-model` with GitHub App
   identity tiers (content vs administration) and per-App credential custody.
2. OpsxFactory: a `github-administration` capability — the GitHub org as a
   managed `platform_tenant` subject, the administration App identity,
   branch-protection/ruleset desired-state, installation/permission policy, and
   the rules-as-code governance loop; likely a profile of, or sibling to,
   `endpoint_management`.
