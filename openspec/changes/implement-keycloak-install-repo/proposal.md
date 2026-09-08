---
code_surface: opensoft/Keycloak-Install (a NEW private repository — its SEED tree only: a README stating the ownership boundary verbatim from the ratified requirement, `config/contracts/identity-brokering/manifest.yaml` pinning `contract-v1.37` by tag plus per-file sha256, the `config/clients/opensoft/` placeholder, the `deploy/` and `docs/` skeleton, `scripts/validate-boundary.py` with its self-test corpus, and the `.github/workflows/session-open-pr.yml` mirror). No openxFactory code surface beyond this change's own records.
target_release: repository-bootstrap (the archived `add-xfactory-installer-repository` precedent for a repo-creation act; no contract bundle is cut — the new repository PINS the released `contract-v1.37` and realization lands on `opensoft/Keycloak-Install`'s own `main`)
Status: ratified
Ratified: Brett Heap, 2026-08-21 — session instruction "do both install repos", following his same-day rulings that the install repositories are Opensoft-level and unprefixed (the parent proposal's Amendment) and on the identity/PKI workstream as a whole
---

# Proposal: implement-keycloak-install-repo

## Why

**The requirement already exists, and it names this change.**
`add-identity-brokering` was ratified on 2026-08-21 and realized at
`contract-v1.37`. Its
[`repo-boundary-governance` delta](../add-identity-brokering/specs/repo-boundary-governance/spec.md)
adds the requirement *"Keycloak install repository boundary"*, whose first
sentence says the identity-broker runtime SHALL live in a private,
independently released repository named `Keycloak-Install`, **created by the
`implement-keycloak-install-repo` successor change**. The parent's
[tasks 4.2](../add-identity-brokering/tasks.md) books the same handoff.
Nothing here is a new decision; this change executes a ratified one.

**The realized contracts have no deployable home.** `contract-v1.37`
published the six-schema neutral `identity-brokering` family and its
canonical validator (see
[`contracts/CHANGELOG.md`](../../../contracts/CHANGELOG.md)). A contract
family with no install repository is a vocabulary nothing can be deployed
against: the dashboard oauth2-proxy swap, the gate-console `actor_subject`
binding, and the editor-product login are all named successors that need a
broker, and a broker needs a governed deployment home before any of them can
begin. The boundary requirement is what makes that home safe to create —
without it the first person to need a running broker puts a realm export
with a client secret in a repository.

**Creating it now is the cheap moment.** The repository is empty, so the
boundary validation, the contract pin discipline, and the session-PR
authorship route can all be installed *before* there is any content to
migrate. Every one of those is harder to retrofit than to seed, and the
per-client `runtime-manifest.yaml` rule — generated, never hand-edited — only
holds if it is true of the first manifest as well as the hundredth.

The sibling change [`implement-openxpki-install-repo`](../implement-openxpki-install-repo/proposal.md)
does the same act for the PKI half of the same session's rulings. The two are
deliberately parallel and deliberately independent.

## What Changes

- **Create `opensoft/Keycloak-Install`** — private, default branch `main`,
  under the boundary the ratified requirement already fixed. Nothing about
  the boundary is authored here; it is quoted.

- **Seed the skeleton, and only the skeleton.** A README carrying the
  ownership boundary verbatim; `config/contracts/identity-brokering/manifest.yaml`
  pinning `contract-v1.37` by tag, exact commit, and per-file sha256 on the
  `pinned_contract_manifest` shape `xFactory-Hermes-Install` already uses;
  a `config/clients/opensoft/` placeholder that documents how the first
  `runtime-manifest.yaml` will be GENERATED rather than pre-writing one;
  `deploy/` and `docs/` directory homes; `scripts/validate-boundary.py`.

- **Install the governance plumbing at creation time**, not later: the `main`
  ruleset requiring one approving review, the repository added to the
  `openxfactory` GitHub App installation so the content App can author PRs,
  the two App secrets, and the
  [`session-open-pr.yml`](../../../.github/workflows/session-open-pr.yml)
  mirror. The authorship route works on day one or the first PR is authored
  by the only human who can approve it.

- **Add the boundary validator.** `scripts/validate-boundary.py` refuses a
  committed secret, key material, or a credential-bearing realm or broker
  configuration export — the exact artifact the ratified requirement's third
  scenario says boundary validation MUST reject. It reuses the detection
  classes the contract-family validators already established rather than
  inventing a second vocabulary for "this is a secret".

- **No broker. No realm. No organization. No persona. No credential. No
  aggregation pin.** The requirement is explicit that repository creation
  SHALL NOT be treated as aggregation admission; that is its own reviewed
  change, named in the impact map below.

## Capabilities

### Modified Capabilities

- `repo-boundary-governance`: exactly ONE delta — a `MODIFIED` restatement of
  this change's OWN parent requirement, *"Keycloak install repository
  boundary"*, flipping its creation clause from future to past tense now that
  the creating act has run. All four MUST-NOT paragraphs and all five
  scenarios are restated unchanged, because an archived `MODIFIED` delta
  wholesale-replaces the requirement it names. No other requirement is
  touched — in particular the *"Install repository scope"* enumeration is
  left alone, because its refresh is already booked as
  [`add-trust-anchor` tasks 8.1](../add-trust-anchor/tasks.md).

No new capability. No contract family. No schema.

## Impact

- **Parent, and the authority for every word of the boundary**:
  [`add-identity-brokering`](../add-identity-brokering/proposal.md) —
  ratified 2026-08-21, realized at `contract-v1.37`, amended the same day to
  Opensoft-level naming. This change is its tasks 4.2. The MODIFIED delta
  here is declared relative to that change's outcome, per
  `release-realization`'s ordered-deltas requirement, which means the parent
  must archive first (see design D-delta).

- **Sibling, same session, same rulings**:
  [`implement-openxpki-install-repo`](../implement-openxpki-install-repo/proposal.md).
  The two changes MODIFY DIFFERENT requirements, so they cannot collide at
  archive time — the same collision-avoidance the two parents used when they
  each added their own requirement instead of sharing one enumeration.

- **Aggregation admission — NOT this change.** A separate reviewed change
  pins `installs/keycloak-install` and records path, remote, visibility,
  exact validated commit, checkout, compatibility, update, and rollback. The
  ratified requirement's fourth scenario says this change MUST NOT be
  accepted as that record.

- **The administration-workflow successor — NOT this change.** The OpsxFactory
  `keycloak-administration` capability owns the governed administration
  procedure, developed in `OpsxFactory:staging:identity-pki-administration`
  together with the PKI half because both need the same service-subject
  registration in lockstep (`customer-kinds` + the Hermes template +
  `stack.yaml`, grant ceilings in `credentials/requirements.yaml`). The
  ratified requirement's last paragraph forbids that workflow from living in
  this repository.

- **The first two consumers, each its own change**: the dashboard
  oauth2-proxy swap (which retires the shared htpasswd secret in the same
  change) and the gate-console `actor_subject` binding (which settles the
  parent's OQ-3 against a real record). Both need a running broker, which
  needs the deployment topology this repository will hold — but neither is
  authorized here.

- **Relies on ratified work**: `repo-boundary-governance` (the avatar-client
  per-repo template these boundary requirements followed —
  [promoted spec](../../specs/repo-boundary-governance/spec.md)),
  `release-realization` (the `code_surface` / `target_release` declaration and
  the realization archive gate), `credential-contracts` (where every secret
  this repository refuses actually goes), and `document-lifecycle` (the
  proposal-origin declaration, which is why the origin here is `ad_hoc`).

- **Reference material that is NOT imported**: the untracked local Keycloak
  compose workspace at `/home/brett/projects/keycloak/`, and the stale public
  fork `opensoft/keycloak`. See design D-keycloak-reference; neither is
  touched by this change.

## Ratification

Ratified by Brett Heap, 2026-08-21 (session instruction: "do both install
repos"), following his same-day rulings that the install repositories are
Opensoft-level and unprefixed — recorded as the Amendment on
`add-identity-brokering` — and on the identity/PKI workstream as a whole.

Ratification authorizes exactly one thing: **creating and seeding the ONE
repository `opensoft/Keycloak-Install` under the already-ratified
`repo-boundary-governance` requirement "Keycloak install repository
boundary".** It creates the repository, its governance plumbing, its seed
skeleton, its `contract-v1.37` pin, and its boundary validator.

It authorizes **no broker deployment, no certificate authority, no realm, no
organization, no persona, no service client, no key, no credential, and no
aggregation admission.** Aggregation admission is a named separate reviewed
change, as the ratified requirement itself demands — repository creation
SHALL NOT be treated as aggregation admission, and this change MUST NOT be
accepted as that record. The broker deployment, the dashboard oauth2-proxy
swap, the gate-console `actor_subject` binding, and the OpsxFactory
`keycloak-administration` workflow are separate successors named in the
impact map and in tasks §4.
