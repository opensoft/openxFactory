# shared-contract-ownership Specification (delta)

## MODIFIED Requirements

### Requirement: Contract version pinning
Install repositories SHALL pin compatible contract bundles from `openxFactory`
before runtime adapters are treated as compatible. A governed bundle pin SHALL
include the canonical repository, published bundle tag, exact repository commit,
canonical manifest path/digest, release-inventory path/digest, and unique required
contract entries containing contract ID, repository-relative path, schema version,
and SHA-256 digest. Its own compatibility-manifest digest SHALL be bound from an
external runtime manifest or realization record rather than self-recorded. Online
Gate verification SHALL prove the annotated tag on the canonical remote; offline
runtime verification SHALL resolve exact commit/tree/blob objects already present
locally. Both modes SHALL fail closed for branch refs, tag-only refs, duplicate IDs
or paths, missing bundle members, path traversal, symlink escape, version mismatch,
or digest drift. For this Gate G0 handoff, the consumer receipt SHALL require
`opensoft/xFactory-Hermes-Install` and SHALL reject `FarHeap/Hermes-Install`
before resolving downstream objects.

#### Scenario: Install repo consumes a contract
- **WHEN** `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, or `OmniWorker-Install` consumes a shared contract
- **THEN** it MUST document and verify the exact published `openxFactory` bundle tag and commit
- **AND** it MUST pin the required contract paths, schema versions, and per-file digests

#### Scenario: Published tag is verified
- **WHEN** an install repository verifies a bundle pin
- **THEN** the tag MUST be annotated, published remotely, and dereference to the exact pinned commit
- **AND** the canonical manifest and changelog MUST declare the same bundle version

#### Scenario: Pinned file drifts
- **WHEN** bytes read from a pinned contract path at the exact commit do not match the recorded digest
- **THEN** compatibility validation MUST fail before runtime realization

#### Scenario: Runtime verifies without a network connection
- **WHEN** the exact pinned commit, trees, blobs, manifest, and release inventory are already present locally
- **THEN** offline verification MUST reproduce every required digest without consulting a mutable working tree

#### Scenario: Compatibility manifest is modified
- **WHEN** the compatibility manifest bytes do not match the digest bound by runtime or realization evidence
- **THEN** compatibility validation MUST fail

#### Scenario: Contract changes incompatibly
- **WHEN** a shared contract change would break an install repo adapter or smoke test
- **THEN** the change MUST be split from adapter migration or explicitly approved as a breaking change

#### Scenario: Existing consumer retains an older pin
- **WHEN** a consumer remains on an older valid bundle pin during an additive release
- **THEN** that consumer remains conformant to its pinned contract until it deliberately upgrades

**Removed from canon by refresh-install-repository-enumerations (2026-09-08):** ``**WHEN** `Hermes-Install` or `Omnigent-Install` consumes a shared contract`` — the bullet is REPLACED rather than deleted, by the widened trigger above it. **THE EDIT IS A LIST EXTENSION PLUS THE PUNCTUATION A LONGER LIST TAKES, AND NOTHING ELSE:** the two names become five, in canon's own order, keeping canon's own `or` and its surrounding grammar word for word, and a serial comma is added before that `or` because a five-item list takes one where canon's two-item list correctly did not. The style is MEASURED rather than preferred — `openspec/specs` carries 561 lines with a serial comma before a final `or` against 232 without, and this requirement's own body uses one before its final `and`. Every other clause of this requirement is word for word what canon states, the Gate G0 handoff sentence included: that sentence requires `opensoft/xFactory-Hermes-Install` and rejects `FarHeap/Hermes-Install` for ONE consumer receipt and is not an index of install repositories, so it is carried unchanged and deliberately not widened.

### Requirement: Submodule sequencing
`openxFactory` SHALL document submodule intent and update procedures before
adding install repositories as submodules.

#### Scenario: Submodule is proposed
- **WHEN** a change proposes adding `Hermes-Install`, `Omnigent-Install`, `Keycloak-Install`, `OpenXPKI-Install`, `OmniWorker-Install`, or a later install repository as a submodule
- **THEN** a decision record MUST document the remote, path, pinned commit, update process, and rollback process

#### Scenario: Hermes-Install remote is unresolved
- **WHEN** `Hermes-Install` still points to a non-Opensoft remote and the target umbrella repo is `opensoft/openxFactory`
- **THEN** the Hermes submodule MUST NOT be added until the move, fork, mirror, or external remote decision is approved

**Removed from canon by refresh-install-repository-enumerations (2026-09-08):** ``**WHEN** a change proposes adding `Hermes-Install` or `Omnigent-Install` as a submodule`` — the bullet is REPLACED rather than deleted, by the widened trigger above it, which keeps canon's grammar exactly (`a change proposes adding … as a submodule`) and extends only its list, with the serial comma a five-plus-item list takes before its final `or` (measured style: `openspec/specs` carries 561 such lines against 232 without). **AND IT IS THE ONE WIDENING IN THIS PACKET THAT DOES NOT CLOSE THE LIST**, which is a deliberate difference from the other five and not an inconsistency: the two names become five plus `or a later install repository`, because this scenario governs the act of ADMITTING a repository that by definition is not yet indexed, and a closed list here would exempt the sixth admission from the decision record the scenario exists to require. The requirement's body and its *"Hermes-Install remote is unresolved"* scenario are word for word what canon states; that scenario names one repository's unresolved remote as a condition, not an index, and is not widened.
