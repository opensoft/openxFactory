## MODIFIED Requirements

### Requirement: Contract version pinning
Install repositories SHALL pin compatible contract bundles from `openxFactory` before runtime adapters are treated as compatible. A governed bundle pin SHALL include the canonical repository, published bundle tag, exact repository commit, canonical manifest path/digest, release-inventory path/digest, and unique required contract entries containing contract ID, repository-relative path, schema version, and SHA-256 digest. Its own compatibility-manifest digest SHALL be bound from an external runtime manifest or realization record rather than self-recorded. Online Gate verification SHALL prove the annotated tag on the canonical remote; offline runtime verification SHALL resolve exact commit/tree/blob objects already present locally. Both modes SHALL fail closed for branch refs, tag-only refs, duplicate IDs or paths, missing bundle members, traversal, symlink escape, version mismatch, or digest drift.

#### Scenario: Install repo consumes a contract
- **WHEN** `Hermes-Install` or `Omnigent-Install` consumes a shared contract
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
