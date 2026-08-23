## ADDED Requirements

### Requirement: MedxPractice owns the branded practice-operations boundary

`MedxPractice` SHALL be a separate private repository that contains only
Medx-specific composition and overlay material around the independently usable
public `openPractice` application.

#### Scenario: Private boundary is independently addressable

- **WHEN** the xFactory composition resolves the practice-operations satellite
- **THEN** it resolves `opensoft/MedxPractice` rather than a direct public
  `openPractice` aggregate checkout

#### Scenario: Public upstream remains independent

- **WHEN** a consumer initializes the nested upstream repository
- **THEN** `openPractice` resolves from its own public repository and its
  history is not copied or rewritten into MedxPractice

### Requirement: The upstream revision is immutable and reviewable

MedxPractice SHALL pin one exact `openPractice` commit through its nested
gitlink and SHALL record the same revision in a committed pin manifest.

#### Scenario: Gitlink and manifest agree

- **WHEN** the MedxPractice composition is validated
- **THEN** the nested `openPractice` gitlink revision equals the manifest
  revision and the declared repository and path are correct

#### Scenario: Pin is reachable

- **WHEN** a fresh recursive clone initializes the composition
- **THEN** the pinned upstream commit is fetchable from the declared public
  remote without requiring a local-only path

### Requirement: Aggregate and domain references use MedxPractice

The xFactory aggregation SHALL expose MedxPractice as the Medx practice-
operations satellite, and MedxFactory SHALL document MedxPractice as the
branded overlay consumed for practice operations.

#### Scenario: No direct aggregate public pin remains

- **WHEN** the aggregate submodule manifest is inspected
- **THEN** the practice-operations entry is `xFactories/MedxPractice` and no
  direct `openPractice` aggregate entry is present

#### Scenario: MedxFactory names the branded dependency

- **WHEN** MedxFactory's stack orientation is read
- **THEN** it names MedxPractice as the practice-operations composition and
  identifies openPractice as its pinned public upstream
