---
code_surface: openxFactory (RENAME at realization, `opensoft/MedxFactory` -> `MedxSoft/MedxFactory`, twenty occurrences across fifteen files: `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` — the entry ALSO moves to the head of `entries`, because the list is bytewise sorted by repository and `M` sorts before `o`; `contracts/hermes-runtime/fixtures/regression/digest-mismatch.yaml`, `duplicate-repository.yaml`, `missing-exclusion-reason.yaml`; `contracts/hermes-runtime/README.md`; `contracts/omnigent/examples/fixtures/negative/manifest-dual-domain-overlay.yaml`; `examples/installation/domain-overlay-examples.yaml`; `tests/hermes_runtime_contracts/test_domain_regression.py` — `PINNED_TABLE` respelled AND reordered in the same commit as the fixture, its `sorted(..., key=lambda value: value.encode("utf-8"))` assertion being the thing that makes the reorder mandatory rather than cosmetic; and the live documents `docs/architecture.md`, `docs/workflow-contract.md`, `docs/terminology-and-repo-topology.md`, `docs/omnigent-constitution.md`, `docs/contract-versioning-policy.md`, `docs/xfactory-domain-factory-model.md` (five hits) and `README.md` (two hits). ADD `contracts/policies/repository-identity.yaml` plus its `contracts/manifest.yaml` entry and `contracts/CHANGELOG.md` release note. NO change to any schema, field name, `$id`, `contract_id`, `contract_schema_version`, digest-identity rule, validator behaviour, check family, or check-family numeral; no file is renamed or moved; no domain repository's `stack.yaml` is touched, openxFactory not pinning domain repos in either direction; and NOT ONE BYTE of the ten occurrences across eight files listed under § What this deliberately does not change.)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md; NO minor is reserved here, the policy forbidding a proposal to reserve one before merge order is known). A BUNDLE IS OWED AND THE REASON IS MEASURED, not assumed: six of the fifteen edited files are members of the declared `contract-v2.0` digest inventory — the regression inventory fixture, its three negative fixtures, `contracts/hermes-runtime/README.md` and `docs/contract-versioning-policy.md` — and none is in `scripts/doc_health/release_inventory.py`'s three-path `EDITORIAL` set, so each moved blob is an `ERROR`-severity `release-inventory-drift` finding and a red `verify-commit` on a non-editorial member until the cut re-baselines the inventory. The change class is ADDITIVE (minor): a repository's OWNER segment moves, no shape moves, and every pinned consumer of `contract-v2.0` keeps resolving byte-identically because a published bundle is never rewritten.
Status: draft
Proposed: 2026-08-27
Origin: The GitHub transfer of `opensoft/MedxFactory` and `opensoft/MedxEHR` to the `MedxSoft` organization on 2026-08-26, and the per-surface disposition set relayed with it. Operational rewiring (git remotes, aggregation `.gitmodules`, `medx-roottruth-install` deploy manifests and pins) landed the same day outside OpenSpec; this packet exists for the part that did not — repository identity inside governed contract content.
---

# Proposal: adopt-medxsoft-repository-identity

## Why

**A governed repository moved organizations and openxFactory's contract content
still names it at its old address.** On 2026-08-26 `opensoft/MedxFactory` and
`opensoft/MedxEHR` were transferred to `MedxSoft`. The operational half was
rewired the same day and is not in question here.

The half that remains is not operational. `opensoft/MedxFactory` is a
**normative value** in openxFactory:

| where | what it is |
| --- | --- |
| `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml:21` | the canonical repository key of one of the five entries in the supported-domain regression DENOMINATOR that gates every bundle publication |
| `fixtures/regression/{digest-mismatch,duplicate-repository,missing-exclusion-reason}.yaml` | the same key inside three negative fixtures that prove the denominator's failure modes |
| `contracts/hermes-runtime/README.md:126` | the prose enumeration of that denominator |
| `contracts/omnigent/examples/fixtures/negative/manifest-dual-domain-overlay.yaml:18` | the `repository:` of a domain overlay in a negative omnigent manifest fixture |
| `examples/installation/domain-overlay-examples.yaml:8` | `domain_factory_repo:` in the canonical installation example |
| `tests/hermes_runtime_contracts/test_domain_regression.py:67` | `PINNED_TABLE`, which pins the fixture row-for-row |
| seven live governance documents | the repository named as the medical domain's canonical home |

**The redirect is a grace period, not an identity.** GitHub redirects the old
owner today and stops the moment `opensoft` reuses either name — a real
possibility for a name that organization used for months. Governed content that
resolves only through a redirect is content whose correctness depends on nobody
creating a repository, which is not a property a contract may rest on.

**And ten of the thirty occurrences MUST NOT be touched.** Archived change
packets, a dated decision record, and three point-in-time verification tables
carrying commit SHAs and stack digests all name the repository as it was named
when they were written. Rewriting them would falsify recorded verification.
That is the same shape `adopt-subject-tenant-domain-vocabulary` faced on
2026-07-23 and answered the same way: rename the live surfaces, freeze the
recorded spellings, and publish a small machine-readable mapping so the frozen
strings stay interpretable rather than merely stale.

## The precedent this follows, cited

`adopt-subject-tenant-domain-vocabulary` (archived 2026-07-23) is the
controlling exemplar and this change mirrors it deliberately:

- It renamed the LIVE normative surfaces (canon prose, new contract families)
  and froze the RELEASED machine spellings byte-stable — `customer_subject_ref`,
  role kinds `customer|client|domain`, `$id`s — because pinned consumers resolve
  them.
- It published `contracts/policies/layer-vocabulary.yaml` (`schema_version: 1`,
  `kind: layer_vocabulary`) whose `legacy_mapping` makes every frozen spelling
  machine-interpretable, and stated the rule that a frozen identifier is read
  THROUGH the mapping and never renamed ad hoc.
- It added a NEW capability (`layer-vocabulary`) rather than bolting the naming
  rule onto an existing one, because no promoted capability owned naming.

This change is the repository-identity instance of that pattern:
`contracts/policies/repository-identity.yaml` is the sibling of
`layer-vocabulary.yaml`, and `repository-identity` is the sibling capability.

## What Changes

- **Add the `repository-identity` capability** (four ADDED requirements, no
  MODIFIED block anywhere): what canonical repository identity is and where the
  current spelling is owed; the obligation to publish a transfer mapping
  machine-readably; the freeze on immutable and dated records; and the change
  class a transfer takes when it moves a release-surface member.
- **Add `contracts/policies/repository-identity.yaml`** (`schema_version: 1`,
  `kind: repository_identity`, sibling of `layer-vocabulary.yaml`), recording
  BOTH 2026-08-26 transfers — `opensoft/MedxFactory -> MedxSoft/MedxFactory` and
  `opensoft/MedxEHR -> MedxSoft/MedxEHR` — with the transfer date and the
  redirect's status. Registered in `contracts/manifest.yaml` with a per-file
  `sha256` and a `consumption_rule`, exactly as `layer-vocabulary` is.
- **Rename the twenty live occurrences across fifteen files** listed in
  `code_surface`, at realization and not in this proposal.
- **Re-cut the contract bundle**, because six edited files are members of the
  declared `contract-v2.0` digest inventory. Allocated late per the versioning
  policy's realization order.
- **Leave `opensoft/MedxEHR` with no live openxFactory surface to rename**,
  measured rather than assumed: `MedxEHR` occurs in this repository only as a
  BARE member name (`--aggregate-members MedxFactory,openChart,MedxEHR,HealthLinc`
  in the doc-health workflow, the `medx-clinical` dashboard grouping, and their
  tests), never owner-qualified. **A transfer moves the OWNER segment only**, so
  bare-name enumerations are correct before and after and are not edited. The
  mapping still records the transfer, because the point of the mapping is that a
  frozen string encountered anywhere resolves.

## What this deliberately does not change

Ten occurrences across eight files keep their recorded spelling and are read
through the mapping:

- **`openspec/changes/archive/**` and any active change's `evidence/`.** Two
  occurrences today, both in
  `2026-08-27-add-hermes-customer-subject-runtime-contract/evidence/`. An
  archived packet is immutable; this is the rule `supersede-lost-pin-baseline`
  refused to break for a pin nobody could resolve, and it is not broken here for
  a name that still resolves.
- **`docs/decisions/0002-xfactory-aggregation-repo.md:86`.** A dated decision
  record stating the clone URL as it was decided.
- **The three `specs/005-customer-subject-runtime/` tables** —
  `research.md:217`, `contracts/release-and-consumer-pin.md:64`, and
  `us4-provider-handoff/shared-interface-contract.md:111`. Dated point-in-time
  VERIFICATION tables carrying commit SHAs and stack digests. Rewriting the
  repository column would state that a verification ran against an address that
  did not exist when it ran, which falsifies the record rather than updating it.
- **`scripts/ideation_dashboard/session_pr.py:209` and
  `tests/ideation-dashboard/test_session_confinement.py` (three occurrences).**
  The string there is an arbitrary example `GH_REPO` value inside prose and a
  fixture about recorded confinement behaviour — it is not repository identity,
  and changing it would edit a recorded incident narrative for no gain.

Also unchanged: no schema, no field name, no `$id` or `contract_id`, no
`contract_schema_version`, no digest-identity rule, no validator, no check
family and no family numeral. No file is renamed or moved. No domain
repository's `stack.yaml` is touched.

## Capabilities

### New Capabilities

- `repository-identity`: canonical `<owner>/<repo>` identity for governed
  repositories, the published transfer mapping, the freeze on immutable and
  dated records, and the change class a transfer takes.

## Why a new capability rather than an existing one

Measured against the fifty-two promoted capabilities. Only two name a repository
in `owner/repo` form at all — `repo-boundary-governance` (three occurrences) and
`shared-contract-ownership` (two) — and both use the spelling to say WHICH
repository owns WHAT, never how a repository is identified or what happens when
its address moves. `repo-boundary-governance`'s own requirements are
authority-and-scope requirements ("Canonical workflow authority", "Install
repository scope"); adding an identity rule there would put a naming obligation
inside an ownership boundary and make every later transfer look like a boundary
change. Nothing in `openspec/specs/` mentions repository transfer or an owner
redirect. The gap is real and it is the same gap `adopt-subject-tenant-domain-vocabulary`
found for layer names, so it takes the same answer: a small new capability that
owns naming, cited by the surfaces that use it.

## Impact

- **Affected specs:** `repository-identity` (NEW; ADDED requirements only). No
  MODIFIED block against any promoted capability, and
  `release-surface-integrity` is CITED rather than restated or widened.
- **Affected contracts:** `contracts/policies/repository-identity.yaml` (new,
  additive), `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and a new
  `contracts/releases/<bundle-tag>.digests.yaml` at the cut.
- **Affected fixtures and tests:** the regression inventory fixture, its three
  negative fixtures, the omnigent negative manifest fixture, the installation
  example, and `tests/hermes_runtime_contracts/test_domain_regression.py`.
- **Affected docs:** `docs/architecture.md`, `docs/workflow-contract.md`,
  `docs/terminology-and-repo-topology.md`, `docs/omnigent-constitution.md`,
  `docs/contract-versioning-policy.md`, `docs/xfactory-domain-factory-model.md`,
  `README.md` (prose plus the OpenSpec Records entry and doc index).
- **Predicted check movement:** `release-inventory-drift` gains six
  `ERROR`-severity findings the moment the renames land and returns to zero at
  the cut; that transient is the reason the cut is sequenced inside this change
  rather than deferred.
- **Operational rewiring: ALREADY DONE, OUTSIDE THIS CHANGE.** Git remotes, the
  aggregation `.gitmodules`, and `medx-roottruth-install`'s deploy manifests and
  pins (commit `d028336`) were rewired 2026-08-26. This proposal neither repeats
  nor governs that work; it records it as the reason the governed half is now
  the only half outstanding.

### Cross-repository follow-ons, named and out of scope

- **`installs/hermes-install` `config/negative/duplicate-domain-layer.manifest.yaml`**
  names the old owner in a negative fixture. That repository consumes
  openxFactory BY PIN and is unaffected until its pin bump, which is exactly the
  disposition `adopt-subject-tenant-domain-vocabulary` gave the same repository
  for the same reason. A separate act in that repository, at its next pin bump.
- **The four sibling DomainxFactory repositories** are untouched: they were not
  transferred, and their inventory rows keep their spelling.
- **No aggregation-level OpenSpec act is owed** for the submodule pointers; that
  is the operational pass already landed.
