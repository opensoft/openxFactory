# hermes-domain-overlay — Spec Delta (content manifest)

## ADDED Requirements

### Requirement: The domain content set is declarable, with the documented convention as fallback
A domain repository SHALL be able to declare its seedable content set in a `hermes/domain/content-manifest.yaml` document of `kind: hermes_domain_content_manifest` — mapping each declared `content_kind` from the ratified content-kind vocabulary to a document `path` or per-file `directory` within the archive — and a consumer SHALL honor the declaration when present, fall back to the documented convention when absent, fail closed when a declared path is missing from the archive, and never load an undeclared kind silently.

#### Scenario: A declared manifest is honored
- **WHEN** a domain archive ships `hermes/domain/content-manifest.yaml` declaring `practice_adoption: {path: hermes/domain/practice-catalog.yaml}`
- **THEN** the consumer loads the practice catalog from the declared path and the manifest validates against the neutral schema

#### Scenario: A missing manifest falls back to convention
- **WHEN** a domain archive carries no content manifest
- **THEN** the consumer loads the documented conventional set exactly as before, with no new refusal class

#### Scenario: A declared path missing from the archive fails closed
- **WHEN** the manifest declares a kind whose path does not exist in the archive
- **THEN** validation fails closed naming the kind and path, and no content loads for that archive

#### Scenario: An unknown content kind fails validation
- **WHEN** the manifest declares a `content_kind` outside the ratified vocabulary
- **THEN** the canonical validator rejects the manifest naming the unknown kind
