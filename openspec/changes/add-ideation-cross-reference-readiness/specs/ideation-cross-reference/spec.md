# ideation-cross-reference Delta: Readiness Index

## ADDED Requirements

### Requirement: Cross-reference index contract
openxFactory SHALL maintain one unified cross-stage cross-reference index at
the ideation level (`ideation/cross-reference.md`), organized by topic
cluster rather than by file. Each topic entry SHALL list every related
document across `ideation/brainstorm/`, `ideation/staging/`, and archived
change material, each member carrying a stage column value. Cluster
membership SHALL bootstrap from the `Topics:` and `Target capabilities:`
header fields already required by the document lifecycle; controlled
`document-cataloging` tags SHALL be folded in as an additional membership
source once that capability realizes, and the index MUST NOT block on the
catalog. The index is a generated projection over governed documents;
`ideation/staging/INDEX.md` remains the staged-file inventory, and the two
files MUST NOT duplicate each other's purpose.

#### Scenario: A topic spans stages
- **WHEN** related material exists in brainstorm, staging, and an archived change
- **THEN** the index MUST carry one topic entry listing every member with its stage value, not one entry per stage

#### Scenario: The catalog realizes later
- **WHEN** `document-cataloging` tags become available
- **THEN** they join header fields as an additive membership source without a schema break
- **AND** entries built from headers alone remain valid

#### Scenario: The inventory and the index are confused
- **WHEN** a staged file is added, removed, or promoted
- **THEN** `staging/INDEX.md` is updated under its own maintenance rule and the cross-reference index is regenerated
- **AND** neither file restates the other's content beyond member references

### Requirement: Extension-fit citation
Every topic entry SHALL carry an extension-fit note stating whether a
promoted capability already exists that the cluster would extend. A fit
note MUST name the specific promoted spec or capability; a pointer to an
archived change folder alone does not satisfy the citation. Where no
promoted fit exists, the note SHALL say so explicitly rather than being
omitted.

#### Scenario: A promoted fit exists
- **WHEN** a topic cluster would extend a promoted capability
- **THEN** its fit note MUST name that spec or capability and how the cluster extends it

#### Scenario: A fit note cites only an archive folder
- **WHEN** a fit note points at an archived change folder without naming the promoted spec or capability
- **THEN** the readiness lane MUST emit an `ideation-readiness` finding against the entry

#### Scenario: No promoted fit exists
- **WHEN** nothing promoted relates to the cluster
- **THEN** the entry MUST state that explicitly, distinguishing "no fit" from "fit check not performed"

### Requirement: Hermes-tier readiness panel
Three independent reviewers SHALL score every topic cluster from 1 to 10
for proposal readiness, one per tier: the domain tier is the owning
DomainxFactory's Domain Hermes authority; the company tier is the
openxFactory ratify authority; the project tier is the engineering
buildability lens — whether codexFactory's feature decomposition could turn
the cluster into a buildable Spec Kit feature DAG today. Each tier score
SHALL carry the same evidence-backed recommendation contract the
document-cataloger and ideation-organizer already use — committed source
revision, passage hash and section reference, rationale, confidence,
alternatives, and `pending_review` disposition; the panel MUST NOT
introduce a divergent rationale format. A tier that cannot score a cluster
SHALL be recorded as unscored with its reason.

#### Scenario: A cluster is scored
- **WHEN** the readiness pass evaluates a topic cluster
- **THEN** the entry MUST carry three tier scores, each with its own evidence-contract rationale
- **AND** each score cites the committed source revisions it judged

#### Scenario: A tier cannot score
- **WHEN** a tier's authority cannot be resolved for a cluster (for example no owning domain)
- **THEN** the entry records that tier as unscored with the reason
- **AND** the recommendation gate MUST NOT fire for that cluster

#### Scenario: Worker output violates the evidence contract
- **WHEN** a tier score arrives without a complete evidence-contract rationale
- **THEN** the score MUST be rejected before persistence and the entry left at its prior state

### Requirement: Readiness recommendation gate
A topic SHALL be flagged "propose for authorization" only when the minimum
of the three tier scores is at least 8. The flag SHALL always be a
recommendation carrying `pending_review` disposition — never an autonomous
action: the pass MUST NOT create proposals, move documents, or change any
lifecycle state. A wide spread between tier scores SHALL be surfaced as a
flagged conflict even when the minimum stays below the threshold.

#### Scenario: All tiers agree the cluster is ready
- **WHEN** every tier scores a cluster 8 or higher
- **THEN** the entry MUST be flagged "propose for authorization" as a `pending_review` recommendation for the disposing authority

#### Scenario: One tier disagrees
- **WHEN** two tiers score 10 and one scores below 8
- **THEN** the gate MUST NOT fire — no tier can be outvoted into silence

#### Scenario: Tiers diverge below threshold
- **WHEN** tier scores spread widely while the minimum stays below 8
- **THEN** the entry MUST carry a flagged conflict recording the divergence as signal

#### Scenario: A recommendation is disposed
- **WHEN** a human authority accepts or rejects a flagged recommendation
- **THEN** the disposition is recorded against the entry and proposing remains a deliberate, authorized step outside this capability

### Requirement: Non-mutating execution bound
The readiness pass SHALL be non-mutating over source content: it writes and
updates only the cross-reference index and its evidence artifacts. It MUST
NOT edit, move, promote, or delete any brainstorm, staging, or archived
document; archived material is read-only reference for the extension-fit
check.

#### Scenario: The pass runs
- **WHEN** a readiness pass completes
- **THEN** the only repository writes are the index file and its evidence artifacts

#### Scenario: A source document needs correction
- **WHEN** the pass observes a defect in a member document
- **THEN** it records the observation in the entry's evidence and MUST NOT modify the document

### Requirement: Nightly scheduling and snapshot consistency
The readiness pass SHALL run as a nightly doc-health lane after the
deterministic pass, consuming that run's document inventory so every score
cites the same corpus snapshot the report describes. A skipped or failed
readiness pass MUST be reported as skipped, MUST NOT affect deterministic
results, and MUST NOT cause prior recommendations to be treated as
resolved.

#### Scenario: The nightly run executes
- **WHEN** the nightly doc-health run completes its deterministic pass
- **THEN** the readiness lane runs against exactly that pass's inventory
- **AND** the dated report links the updated index and evidence

#### Scenario: The lane is unavailable
- **WHEN** the readiness worker is skipped, offline, or fails
- **THEN** the run reports the lane as skipped and deterministic results land unaffected
- **AND** recommendations absent only because the lane did not run are not treated as disposed
