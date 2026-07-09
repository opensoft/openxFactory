## ADDED Requirements

### Requirement: Proposal supporting-document integrity checks
The deterministic doc-health pass SHALL validate proposal supporting-document
lifecycle integrity. It SHALL report staged material that already cites an
active or archived proposal, active supporting-document folders with missing or
invalid manifests, `Status: staged` documents under active proposal support,
archive manifests whose bundle or file hashes do not verify, and supporting
bundles stored under canonical `openspec/specs/`.

#### Scenario: Proposed material remains in staging
- **WHEN** a staged document names an active or archived OpenSpec change as its exit or proposal
- **THEN** doc-health MUST report that document as stale staged state

#### Scenario: An active proposal lacks its manifest
- **WHEN** an active change contains `supporting-docs/` without a valid `manifest.yaml`
- **THEN** doc-health MUST report the incomplete proposal support record

#### Scenario: An archived bundle fails verification
- **WHEN** an archived change's readable supporting-document manifest does not match its bundle hash or bundled file hashes
- **THEN** doc-health MUST report an archive-integrity error

#### Scenario: A historical bundle is stored as canonical specification
- **WHEN** a compressed supporting-document bundle exists below `openspec/specs/`
- **THEN** doc-health MUST report a location-conformance error
