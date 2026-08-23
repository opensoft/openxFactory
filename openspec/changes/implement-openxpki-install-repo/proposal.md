---
code_surface: opensoft/OpenXPKI-Install (a NEW private repository — its SEED tree only: a README stating the ownership boundary verbatim from the ratified requirement including the image-custody split, `config/contracts/trust-anchor/manifest.yaml` pinning `contract-v1.37` by tag plus per-file sha256, the `config/clients/opensoft/` placeholder, the `deploy/` topology home with its digest-only consumption rule, the `docs/` procedure homes, `scripts/validate-boundary.py` with its self-test corpus, and the `.github/workflows/session-open-pr.yml` mirror). No openxFactory code surface beyond this change's own records.
target_release: repository-bootstrap (the archived `add-xfactory-installer-repository` precedent for a repo-creation act; no contract bundle is cut — the new repository PINS the released `contract-v1.37` and realization lands on `opensoft/OpenXPKI-Install`'s own `main`)
Status: ratified
Ratified: Brett Heap, 2026-08-21 — session instruction "do both install repos", following his same-day rulings that the install repositories are Opensoft-level and unprefixed (the parent proposal's Amendment) and on the identity/PKI workstream as a whole
---

# Proposal: implement-openxpki-install-repo

## Why

**The requirement already exists, and it names this change.**
`add-trust-anchor` was ratified on 2026-08-21 and realized at
`contract-v1.37`. Its
[`repo-boundary-governance` delta](../add-trust-anchor/specs/repo-boundary-governance/spec.md)
adds the requirement *"OpenXPKI install repository boundary"*, whose first
sentence says the deployable certificate-authority runtime SHALL live in a
private, independently released repository named `OpenXPKI-Install`,
**created by the `implement-openxpki-install-repo` successor change**. The
parent's [tasks 7.2](../add-trust-anchor/tasks.md) books the same handoff.
Nothing here is a new decision; this change executes a ratified one.

**The realized contracts have no deployable home.** `contract-v1.37`
published the eight-schema neutral `trust-anchor` family, its chain-custody
registry, and its canonical validator (see
[`contracts/CHANGELOG.md`](../../../contracts/CHANGELOG.md)). One of the two
realizations that forced that contract — Intune Cloud PKI — is a
cloud-managed authority we do not host. The other, OpenXPKI for the Opensoft
production core, is exactly the one that needs a governed deployment home,
and it does not have one.

**And this half is time-bound in a way the identity half is not.** The
OpsxFactory change `add-openxpki-qa-image-pipeline` was amended on 2026-08-21,
before its own ratification, to split the QA scope per the ratified custody
ruling: image custody (build, release / package / configuration / base-image
pins, the offline and integration harness, the immutable ACR digest) stays in
`opensoft/Opensoft-Tenant`, and the QA server / client / web deployment
topology belongs to `OpenXPKI-Install`. That amendment added a
**tasks 3.4 migration obligation** whose text says the manifests migrate
"when `implement-openxpki-install-repo` creates it", and records their
current location as *transitional, not their governed home*. A migration task
that names a repository which does not exist cannot close. The governed home
must exist before that change ratifies with the obligation aboard — which is
this change.

**Creating it now is the cheap moment**, for the same reason as the sibling:
the repository is empty, so the boundary validation, the contract pin
discipline, the digest-only image-consumption rule, and the session-PR
authorship route are all seeded rather than retrofitted. In this repository
one of those is unusually load-bearing — the boundary refuses image build
sources and *mutable tag references*, and a mutable tag is the single easiest
thing to introduce accidentally during a bring-up under time pressure. The
upstream OpenXPKI Docker image is explicitly a demonstration artifact
published with mutable tags; that is the hazard the whole custody split
exists to contain.

The sibling change [`implement-keycloak-install-repo`](../implement-keycloak-install-repo/proposal.md)
does the same act for the identity half of the same session's rulings. The
two are deliberately parallel and deliberately independent.

## What Changes

- **Create `opensoft/OpenXPKI-Install`** — private, default branch `main`,
  under the boundary the ratified requirement already fixed. Nothing about
  the boundary is authored here; it is quoted.

- **Seed the skeleton, and only the skeleton.** A README carrying the
  ownership boundary verbatim, including the three-way split — `openxFactory`
  owns the neutral `trust-anchor` contract, OpsxFactory `pki-administration`
  owns the governed administration procedure, `opensoft/Opensoft-Tenant` owns
  image custody, and this repository realizes all three and owns none of
  them; `config/contracts/trust-anchor/manifest.yaml` pinning
  `contract-v1.37` by tag, exact commit, and per-file sha256 on the
  `pinned_contract_manifest` shape `xFactory-Hermes-Install` already uses; a
  `config/clients/opensoft/` placeholder documenting how the first
  `runtime-manifest.yaml` will be GENERATED rather than pre-writing one;
  `deploy/` as the topology HOME carrying the digest-only consumption rule
  and no manifests; `docs/` procedure homes; `scripts/validate-boundary.py`.

- **Do not invent the topology.** The QA server / client / web manifests
  already exist — another session built them during the QA bring-up, in
  `opensoft/Opensoft-Tenant`, and they are the artifacts tasks 3.4 migrates.
  This change seeds the HOME and the rules that will govern them; it does not
  author a second set. See design D-openxpki-migration.

- **Install the governance plumbing at creation time**, not later: the `main`
  ruleset requiring one approving review, the repository added to the
  `openxfactory` GitHub App installation so the content App can author PRs,
  the two App secrets, and the
  [`session-open-pr.yml`](../../../.github/workflows/session-open-pr.yml)
  mirror.

- **Add the boundary validator.** `scripts/validate-boundary.py` refuses
  committed secrets, credentials, and certificate-authority key material —
  and, specific to this repository, image build sources, a pipeline producing
  the image, and any **mutable image tag reference**, which the requirement's
  second scenario says boundary validation MUST reject and route to
  `opensoft/Opensoft-Tenant`.

- **No certificate authority. No anchor. No certificate. No realm. No key.
  No credential. No image build. No aggregation pin.** The requirement is
  explicit that repository creation MUST NOT be treated as aggregation
  admission; that is its own reviewed change, named in the impact map below.

## Capabilities

### Modified Capabilities

- `repo-boundary-governance`: exactly ONE delta — a `MODIFIED` restatement of
  this change's OWN parent requirement, *"OpenXPKI install repository
  boundary"*, flipping its creation clause from future to past tense now that
  the creating act has run. The image-custody sentence, the MUST-NOT list,
  the three-way ownership paragraph, and all three scenarios are restated
  unchanged, because an archived `MODIFIED` delta wholesale-replaces the
  requirement it names. No other requirement is touched — in particular the
  *"Install repository scope"* enumeration is left alone, because its refresh
  is already booked as [`add-trust-anchor` tasks 8.1](../add-trust-anchor/tasks.md).

No new capability. No contract family. No schema.

## Impact

- **Parent, and the authority for every word of the boundary**:
  [`add-trust-anchor`](../add-trust-anchor/proposal.md) — ratified
  2026-08-21, realized at `contract-v1.37`, amended the same day to
  Opensoft-level naming. This change is its tasks 7.2. The MODIFIED delta
  here is declared relative to that change's outcome, per
  `release-realization`'s ordered-deltas requirement, which means the parent
  must archive first (see design D-delta).

- **Sibling, same session, same rulings**:
  [`implement-keycloak-install-repo`](../implement-keycloak-install-repo/proposal.md).
  The two changes MODIFY DIFFERENT requirements, so they cannot collide at
  archive time — the same collision-avoidance the two parents used when they
  each added their own requirement instead of sharing one enumeration.

- **The `add-openxpki-qa-image-pipeline` migration seam (OpsxFactory), and an
  honest dependency note.** That change's amended **tasks 3.4** migrates the
  QA deployment manifests of its 3.1-3.3 into this repository once it exists,
  keeping image source, build, pins, harness, and runbook/evidence templates
  in `opensoft/Opensoft-Tenant`; its Impact already names
  `opensoft/OpenXPKI-Install` as the governed home and cross-references the
  parent. **But that change is still an uncommitted working-tree draft in its
  owning session** — it was found already implemented through its QA gate
  (tasks 3.x / 4.x checked) and is not yet ratified, and the parent's own
  tasks 2.3 is still open for exactly this reason. Consequences, stated
  plainly: the **immutable ACR digest** its QA gate produced is **not yet
  durably recorded** anywhere this change can cite, so **seeding proceeds and
  the topology migration waits**. The seed carries the digest-only
  consumption RULE with no digest value in it; the migration and the first
  recorded digest land in a later change, after that draft commits and
  ratifies.

- **Aggregation admission — NOT this change.** A separate reviewed change
  pins `installs/openxpki-install` and records path, remote, visibility,
  exact validated commit, recursive checkout, compatibility, update, and
  rollback. The ratified requirement's third scenario says repository
  creation MUST NOT be treated as aggregation admission.

- **The administration-workflow successor — NOT this change.** The OpsxFactory
  `pki-administration` capability owns the governed administration procedure
  as a SIBLING of `exchange-administration`, `aks-administration-workflow`,
  `github-administration-workflow`, and `business-central-administration` —
  not a profile of one of them — with the certificate-authority
  service-subject kind registered in lockstep (`customer-kinds` + the Hermes
  template + `stack.yaml`, grant ceilings in
  `credentials/requirements.yaml`). Developed in
  `OpsxFactory:staging:identity-pki-administration`, shared with the identity
  half because both need the same registration work. The ratified requirement
  keeps that procedure out of this repository.

- **Relies on ratified work**: `repo-boundary-governance` (the avatar-client
  per-repo template these boundary requirements followed —
  [promoted spec](../../specs/repo-boundary-governance/spec.md)),
  `release-realization` (the `code_surface` / `target_release` declaration and
  the realization archive gate), `credential-contracts` (where authority key
  material and issuance credentials actually live — with no QA exemption,
  because a QA authority's key is still an authority key), `openxwallet` (the
  declared-custody model the contract composes with), and
  `document-lifecycle` (the proposal-origin declaration, which is why the
  origin here is `ad_hoc`).

## Ratification

Ratified by Brett Heap, 2026-08-21 (session instruction: "do both install
repos"), following his same-day rulings that the install repositories are
Opensoft-level and unprefixed — recorded as the Amendment on
`add-trust-anchor` — and on the identity/PKI workstream as a whole.

Ratification authorizes exactly one thing: **creating and seeding the ONE
repository `opensoft/OpenXPKI-Install` under the already-ratified
`repo-boundary-governance` requirement "OpenXPKI install repository
boundary".** It creates the repository, its governance plumbing, its seed
skeleton, its `contract-v1.37` pin, and its boundary validator.

It authorizes **no certificate authority, no trust anchor, no certificate, no
issuance, no realm, no key, no credential, no image build or image pin, and
no aggregation admission.** Aggregation admission is a named separate
reviewed change, as the ratified requirement itself demands — repository
creation MUST NOT be treated as aggregation admission. The QA topology
migration (the amended `add-openxpki-qa-image-pipeline` tasks 3.4, which
waits on that draft committing and ratifying), the deployment itself, and the
OpsxFactory `pki-administration` workflow are separate successors named in
the impact map and in tasks §4.
