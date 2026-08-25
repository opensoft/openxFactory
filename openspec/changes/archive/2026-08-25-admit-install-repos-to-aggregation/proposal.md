---
code_surface: the xFactory aggregation act in `opensoft/xFactory` (two `.gitmodules` entries — `installs/keycloak-install` -> `git@github.com:opensoft/Keycloak-Install.git` and `installs/openxpki-install` -> `git@github.com:opensoft/OpenXPKI-Install.git` — the two gitlinks at the exact validated commits `1aa184e891d4ba6e641a31260d3f64d2b335f175` and `05f440444d9091206778e838454ed9b5bb7bff60`, and the README topology / current-submodule documentation update), plus this change's own admission records in openxFactory. No change to either admitted repository's tree.
target_release: repository-bootstrap (the archived `add-xfactory-installer-repository` precedent for a repository-boundary act against the aggregation; no contract bundle is cut — both admitted repositories PIN the already-released `contract-v1.37`, and realization lands on `opensoft/xFactory`'s `main`)
Status: ratified
Ratified: Brett Heap, 2026-08-21 — session instruction "do the aggregation admission change, the two repos are added to openXfactory github app"
---

# Proposal: admit-install-repos-to-aggregation

## Why

**Two ratified requirements demand this change by name and refuse to be it.**
`add-identity-brokering` and `add-trust-anchor` were both ratified on
2026-08-21 and both realized at `contract-v1.37`. Each added a
`repo-boundary-governance` requirement whose last discipline is the same
sentence: adding the repository to the aggregation SHALL be **a separate
reviewed change that records path, remote, visibility, exact validated commit,
checkout, compatibility, update, and rollback behavior**, and repository
creation SHALL NOT be treated as aggregation admission
([Keycloak](../implement-keycloak-install-repo/specs/repo-boundary-governance/spec.md),
[OpenXPKI](../implement-openxpki-install-repo/specs/repo-boundary-governance/spec.md)).
The Keycloak scenario goes further and says the repository's own creation
change **MUST NOT be accepted as that record**. This change is that record,
and it is the only artifact in the family that is allowed to be.

**The repositories exist and are validated; nothing in the workspace can see
them.** `implement-keycloak-install-repo` and
`implement-openxpki-install-repo` created and seeded `opensoft/Keycloak-Install`
and `opensoft/OpenXPKI-Install` on 2026-08-21, each with its boundary
validator green and red-proven at the recorded commit. Until the aggregation
pins them, they are two private repositories nobody's `git submodule update
--init --recursive` produces — every successor that needs them (the broker
deployment, the QA topology migration out of `opensoft/Opensoft-Tenant`, the
dashboard oauth2-proxy swap) starts by cloning something the workspace
contract does not mention.

**Admission is cheapest while the pin is the whole coupling.** Both
repositories are at their seed commit, hold nothing that runs, and carry no
submodules of their own — read back this session: neither has a
`.gitmodules` (HTTP 404 on the contents API at `main`), so recursive checkout
is plain checkout, and rollback is one revert of one gitlink. Recording the
update and rollback discipline now, against a pin with no history to unwind,
is what makes the second and hundredth pin advance boring.

The enumeration refresh
[`add-trust-anchor` tasks 8.1](../add-trust-anchor/tasks.md) has been waiting
for exactly this moment: it may only run when **both** install repositories
exist and **nothing else is replacing** the *"Install repository scope"*
requirement. Both conditions now hold (see design D-enumeration for the grep),
so this change discharges it rather than deferring it a third time.

## What Changes

- **Record the admission, per repository, field by field.** [design.md](design.md)
  carries one section per repository with the eight fields the ratified
  requirements enumerate, verbatim-labeled: **path, remote, visibility, exact
  validated commit, checkout, compatibility, update, rollback**. Every value
  is a read-back, not an assertion — repository ids, visibility, default
  branch, `main` tip, and the `contract-v1.37` pin commit were re-read from
  the GitHub API while this proposal was written.

- **Execute the aggregation act**: two `.gitmodules` entries, two gitlinks at
  the exact validated commits, and the README topology + `Current Submodules`
  documentation update — mirroring the archived installer precedent's tasks
  4.1, which updated "the xFactory topology and current-submodule
  documentation" in the same act. The aggregation is a pin-only workspace
  assembler; the pin is the entire coupling it takes on.

- **Refresh one enumeration.** ONE `MODIFIED` delta on *"Install repository
  scope"*, restating the requirement entirely — both its scenarios unchanged —
  and extending its enumeration with the two newly admitted repositories.
  Nothing else about that requirement changes, and no other requirement is
  touched: in particular the two boundary requirements are left exactly as
  their creating changes restated them.

- **Close the org-owner-gated bookkeeping.** Brett added both repositories to
  the `openxfactory` GitHub App installation, which was the 403 blocking
  `implement-*` tasks 1.3 and 3.3. Read back: installation `145372182` lists
  both repositories among 19. Those four boxes are ticked with the read-back
  facts, and each creation record gets a dated addendum.

- **No deployment. No pin advance. No repository change.** The pins land at
  the commits recorded here and nowhere further; neither admitted repository's
  tree is touched by this change.

## Capabilities

### Modified Capabilities

- `repo-boundary-governance`: exactly ONE delta — a `MODIFIED` restatement of
  *"Install repository scope"* that extends its enumeration with
  `installs/keycloak-install` (`opensoft/Keycloak-Install`) and
  `installs/openxpki-install` (`opensoft/OpenXPKI-Install`), admitted
  2026-08-21 by this change. Both of its scenarios are restated unchanged,
  because an archived `MODIFIED` delta wholesale-replaces the requirement it
  names and only that requirement.

No new capability. No contract family. No schema. No new requirement — the
admission discipline this change satisfies was ratified elsewhere; recording
compliance with a requirement does not need a requirement of its own.

## Impact

- **The aggregation repository `opensoft/xFactory`** — the only repository
  whose tree changes outside openxFactory: `.gitmodules`, two gitlinks, and
  the README topology / `Current Submodules` documentation. Its `main` needs a
  reviewed PR, opened through the `session-open-pr` route the aggregation
  already carries — its own copy of the same
  [workflow](../../../.github/workflows/session-open-pr.yml) openxFactory has
  — so the PR is authored by `openxfactory[bot]` and Brett remains free to
  approve it.

- **The two admitted repositories** — `opensoft/Keycloak-Install` (repo id
  `1342329131`) and `opensoft/OpenXPKI-Install` (repo id `1342329163`).
  Neither tree is modified. Each keeps the ownership boundary its own ratified
  requirement fixed; admission adds a pin, not a scope.

- **The changes whose open items this closes**:
  [`implement-keycloak-install-repo`](../implement-keycloak-install-repo/tasks.md)
  and
  [`implement-openxpki-install-repo`](../implement-openxpki-install-repo/tasks.md)
  — tasks **1.3** (the App-installation add) and **3.3** (its read-back) in
  both, plus each change's §4 aggregation-admission follow-up item, annotated
  as executed here rather than ticked: those items are booked as "NOT this
  change / a separate reviewed change", and ticking them inside the creation
  change would claim the creation change did the admission, which is the one
  thing its ratified requirement forbids.

- **[`add-trust-anchor`](../add-trust-anchor/tasks.md) tasks 8.1** — the
  deferred *"Install repository scope"* enumeration refresh, discharged by the
  delta here and ticked with a DONE note naming this change. Its design D8
  deferred it precisely so it could run once, after both repositories exist,
  without racing another replacement.

- **Relies on ratified work**: `repo-boundary-governance` (the promoted
  *"Deferred aggregation and web-console integration"* discipline these
  boundary clauses were modelled on, and the promoted *"Neutral installer
  repository integration"* precedent —
  [promoted spec](../../specs/repo-boundary-governance/spec.md)),
  `release-realization` (the `code_surface` / `target_release` declaration and
  the merged-realization archive gate), and `document-lifecycle` (the
  proposal-origin declaration, which is why the origin is `ad_hoc`).

- **NOT in scope, each its own change**: the broker deployment and its first
  generated `runtime-manifest.yaml`; the OpenXPKI QA topology migration out of
  `opensoft/Opensoft-Tenant` (gated on `add-openxpki-qa-image-pipeline`
  committing and ratifying); the CI wiring that turns each boundary validator
  into a required status check; the OpsxFactory `keycloak-administration` and
  `pki-administration` workflows; and the `contract-v1.37` release
  digest-inventory defect booked as `implement-*` tasks 4.7. Also out of
  scope: the pre-existing staleness of the aggregation README's submodule
  documentation, which omits several already-pinned submodules — this change
  adds its own two entries and does not silently adopt someone else's
  bookkeeping (design D-readme).

## Ratification

Ratified by Brett Heap, 2026-08-21 (session instruction: "do the aggregation
admission change, the two repos are added to openXfactory github app").

Ratification authorizes exactly four things:

1. **The two admission records** in this change — one per repository, carrying
   path, remote, visibility, exact validated commit, checkout, compatibility,
   update, and rollback behavior, which is the record both ratified boundary
   requirements demand before a pin is treated as supported.
2. **The enumeration refresh** — one `MODIFIED` delta extending
   *"Install repository scope"* with the two admitted repositories, restating
   that requirement entirely and touching no other.
3. **The aggregation act** in `opensoft/xFactory` — two `.gitmodules` entries,
   two gitlinks **at the exact validated commits
   `1aa184e891d4ba6e641a31260d3f64d2b335f175` (Keycloak-Install) and
   `05f440444d9091206778e838454ed9b5bb7bff60` (OpenXPKI-Install)**, and the
   README submodule-documentation update, landed by reviewed PR.
4. **The bookkeeping** this session's org-owner act unblocked — `implement-*`
   tasks 1.3 and 3.3 in both changes, their creation-record addenda, the §4
   annotations, and the `add-trust-anchor` tasks 8.1 tick.

It authorizes **no deployment of any kind** — no broker, no certificate
authority, no realm, no organization, no persona, no service client, no key,
no credential — **and no pin advance beyond the recorded commits.** A later
commit in either repository is a later reviewed aggregation PR, not an
extension of this ratification. Neither admitted repository's tree is
modified. The broker deployment, the QA topology migration, the boundary-
validator CI gates, and the OpsxFactory administration workflows remain the
separate successors named in the impact map and in tasks §5.
