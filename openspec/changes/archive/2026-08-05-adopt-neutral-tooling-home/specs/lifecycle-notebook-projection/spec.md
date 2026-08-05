# lifecycle-notebook-projection Delta: Sync Implementation Comes Home

## MODIFIED Requirements

### Requirement: Projection implementation ownership
`openxFactory` SHALL own this projection contract, the workflow
documentation, and the conforming sync implementation
(`scripts/sync-notebooklm-books.py`). Book identity, charter text, title
prefixes, and chat framing SHALL be treated as contract conformance, not
implementation preference.

#### Scenario: The sync implementation is modified

- **WHEN** the sync implementation changes book definitions, prefixes, charter, exclusions, or chat framing
- **THEN** the change MUST be preceded by an OpenSpec delta to this capability

#### Scenario: A workspace names the sync manager

- **WHEN** a lifecycle notebook declares its `managed_by` implementation
- **THEN** the declared path resolves inside openxFactory, and the invocation is run from the workspace root against every pinned repo
