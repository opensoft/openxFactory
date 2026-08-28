# doc-health

## MODIFIED Requirements

### Requirement: Proposal supporting-document integrity checks
The deterministic doc-health pass SHALL validate proposal supporting-document
lifecycle integrity. It SHALL report staged material that already cites an
ACTIVE proposal, active supporting-document folders with missing or
invalid manifests, `Status: staged` documents under active proposal support,
archive manifests whose bundle or file hashes do not verify, and supporting
bundles stored under canonical `openspec/specs/`.

A citation of an ARCHIVED change SHALL NOT raise the staged-material finding.
That finding's remedy is to move the material into the cited proposal's
supporting-docs folder, and an archived packet is closed: the move names an act
nobody can perform, so the finding would report a defect with no conforming
resolution. Archived-ness SHALL be read from the change tree rather than
presumed, and the union of active and archived ids that other families require
— a ratification citation may name an archived change, and must — SHALL remain
available to them unchanged.

#### Scenario: Proposed material remains in staging
- **WHEN** a staged document names an ACTIVE OpenSpec change as its exit or proposal
- **THEN** doc-health MUST report that document as stale staged state

#### Scenario: Staged material cites a change that has archived
- **WHEN** a staged document's only cited exit or proposal names a change that has archived
- **THEN** doc-health MUST NOT report that document as stale staged state
- **AND** the id MUST remain resolvable to the families that read the union of active and archived changes

#### Scenario: Staged material cites both an archived and an active change
- **WHEN** a staged document names both an archived change and an active one as its exits
- **THEN** doc-health MUST report the document against the ACTIVE change
- **AND** the finding MUST NOT name the archived change, whose supporting-docs folder cannot receive the material

#### Scenario: An active proposal lacks its manifest
- **WHEN** an active change contains `supporting-docs/` without a valid `manifest.yaml`
- **THEN** doc-health MUST report the incomplete proposal support record

#### Scenario: An archived bundle fails verification
- **WHEN** an archived change's readable supporting-document manifest does not match its bundle hash or bundled file hashes
- **THEN** doc-health MUST report an archive-integrity error

#### Scenario: A historical bundle is stored as canonical specification
- **WHEN** a compressed supporting-document bundle exists below `openspec/specs/`
- **THEN** doc-health MUST report a location-conformance error
