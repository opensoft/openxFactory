# ideation-cross-reference Specification

## Purpose
TBD - created by archiving change add-ideation-dashboard. Update Purpose after archive.
## Requirements
### Requirement: Possibles register consolidation
The cross-reference index SHALL consolidate every `Possible feats:`
declaration into the canonical possibles register, one register entry per
possible with explicit many-to-many edges to its claiming topic clusters —
the same bootstrap posture as the index's tag sources, with no third
standalone register file. Each possible SHALL carry exactly one state:
`latent` (enumerated, unpicked — backlog, not failure), `picked` (citing
the staged topic's staging ID and inheriting the change ID at the proposal
gate), `rejected`, or `superseded`; `rejected` and `superseded` SHALL
require a recorded reason plus a citation, mirroring the contested-finding
disposition rule.

#### Scenario: Declarations are consolidated
- **WHEN** the index pass runs over documents carrying `Possible feats:` sections
- **THEN** the register carries one canonical entry per possible with edges to every claiming cluster

#### Scenario: A possible is rejected without citation
- **WHEN** a register entry transitions to `rejected` or `superseded` without a recorded reason and citation
- **THEN** strict register validation MUST fail the transition

#### Scenario: A picked possible's topic crosses the proposal gate
- **WHEN** the staged topic cited by a `picked` possible becomes an OpenSpec change
- **THEN** the pick citation inherits the change ID while retaining the original staging ID

### Requirement: Human-seen cluster intake
An ad-hoc workbench reference set matching no machine cluster SHALL be
accepted as a human-seen cluster proposal into the same recommendation
queue as machine clustering, carrying the full evidence contract already
used by the panel's scores — committed source revision, passage hash and
section reference, rationale, confidence, alternatives, and
`pending_review` disposition. Human-seen submissions MUST NOT bypass
review: they are recommendations disposed by the same authorities as
machine suggestions.

#### Scenario: A human submits an ad-hoc set
- **WHEN** a workbench user submits a reference set as a human-seen cluster
- **THEN** the submission enters the recommendation queue with the full evidence contract and `pending_review` disposition

#### Scenario: A submission lacks evidence
- **WHEN** a human-seen submission arrives without the complete evidence contract
- **THEN** it MUST be rejected before persistence

#### Scenario: A human-seen cluster is accepted
- **WHEN** the disposing authority accepts a human-seen cluster
- **THEN** it becomes a topic cluster in the index like any machine-derived cluster, recording its human-seen provenance

### Requirement: Derived possible register entry and provenance
Every possibles-register entry the derivation lane proposes SHALL carry
`origin: ai-derived`, a `derivation` block naming the worker run (correlation
id, worker profile, and prompt-contract version), and machine
`disposition: pending_review`, and SHALL cite the source material it was derived
from through the register's existing evidence fields — at least one
`claiming_clusters` topic-cluster edge and at least one `supporting_evidence`
passage pin — so a derived possible is never an unsourced assertion.

The `origin` and `derivation` fields are an ADDITIVE, forward-compatible delta to
the `ideation-possibles-register` kernel, modelled one-for-one on the topic
entry's `origin` + `human_seen` intake pair: a human-authored possible carries no
`origin` (defaulting to human-authored) and is unaffected, so the delta requires
no `contract_schema_version` bump. The worker-run identity lives in the
`derivation` block, not in `ingestion_provenance`, which keeps its `Possible
feats:` meaning; a derived entry's required `provenance` cites the primary source
member document and the cluster context it was derived from.

#### Scenario: A possible is derived
- **WHEN** the lane proposes a candidate possible from a topic cluster
- **THEN** the register entry MUST carry `origin: ai-derived`, a `derivation` block naming the worker run, `disposition: pending_review`, at least one `claiming_clusters` edge, and at least one `supporting_evidence` pin

#### Scenario: A derived entry omits its worker run
- **WHEN** a proposed derived entry lacks the `derivation` worker-run identity or its `pending_review` disposition
- **THEN** it MUST be rejected before persistence and no register entry is created

#### Scenario: A derived entry cites no source
- **WHEN** a proposed derived entry carries neither a `claiming_clusters` edge nor a `supporting_evidence` pin
- **THEN** it MUST be rejected as an unsourced possible

#### Scenario: A human-authored possible is unaffected
- **WHEN** the register holds a human-authored possible with no `origin` field
- **THEN** it remains valid and defaults to human-authored without a `derivation` block

### Requirement: Orchestration-authoritative identifiers and hashes
The tool-less model worker MUST NOT compute, invent, or transcribe any
machine-precision value — register ids, correlation ids, content or passage
hashes, revisions, or counts — in its proposed possibles; orchestration SHALL
compute every such value and treat its own values as authoritative, and any
worker-supplied precision value that disagrees with the orchestration-computed
value SHALL void the affected proposals rather than persist a corrupted entry.

This carries the document-cataloger lane's contract forward: a worker that
mis-copied a single hex character of a content hash voided twenty-five
classifications. The worker proposes titles, claims, and rationale prose only;
identity and evidence pins are stamped by orchestration.

#### Scenario: Worker output contains a precision value
- **WHEN** worker output includes a register id, hash, revision, or count
- **THEN** orchestration MUST discard the worker value and substitute its own computed value

#### Scenario: A worker value disagrees with orchestration
- **WHEN** a worker-supplied precision value does not match the orchestration-computed value for the same entry
- **THEN** the affected proposals MUST be voided and reported, never persisted

### Requirement: One-way derived-possible disposition on the gate console
A derived possible SHALL remain `pending_review` until a human authority disposes
it on the gate console, and its disposition SHALL be one-way — accepted,
rejected, or deferred — never edited back to `pending_review` and never
auto-promoted by the lane.

An accepted derived possible becomes a first-class register possible in `latent`
state, retaining its `origin: ai-derived` provenance exactly as an accepted
human-seen cluster retains `origin: human-seen`, and thereafter follows the
normal pick lifecycle. A rejected derived possible is recorded in `rejected`
state with the required reason and citation drawn from the disposition,
preserving its audit trail so the same candidate is never silently re-derived; a
previously rejected possible that becomes viable again is a NEW entry with a new
`id`, never a resurrection. The lane itself creates no proposal, moves no
document, and changes no lifecycle state.

#### Scenario: A derived possible is accepted
- **WHEN** a human authority accepts a `pending_review` derived possible on the gate console
- **THEN** it becomes a `latent` register possible retaining `origin: ai-derived`
- **AND** proposing remains a deliberate authorized step outside this lane

#### Scenario: A derived possible is rejected
- **WHEN** a human authority rejects a `pending_review` derived possible
- **THEN** it is recorded `rejected` with the disposition's reason and citation
- **AND** it MUST NOT re-enter `pending_review` and MUST NOT be silently re-derived

#### Scenario: The lane never promotes
- **WHEN** the derivation lane runs
- **THEN** it MUST NOT accept, pick, or promote any possible autonomously — every disposition is a human act on the gate console

### Requirement: Bounded derivation worker, immutable evidence, and concurrency-protected merge
The derivation worker SHALL run as a distinct, bounded, read-only
artifact-in/artifact-out Omnigent lane with its own worker profile, prompt, and
output schema, receiving no repository credentials and no write authority, and
its output MUST NOT block deterministic work: an offline, unauthorized, partial,
invalid, timed-out, or failed worker run MUST leave the deterministic pass and
its report unaffected and the possibles register unchanged.

A watchdog SHALL report and cancel a derivation child queued longer than ten
minutes or running longer than thirty minutes. Validated derivation output SHALL
be persisted as immutable evidence under the factory identity and SHALL merge
into `ideation/cross-reference.yaml`'s `possibles_register` only through a later
main run, under concurrency protection that refuses a stale overwrite of a
register a concurrent run has already advanced. The merge preserves register
`id` uniqueness and never edits a disposed entry.

#### Scenario: The worker is offline
- **WHEN** the derivation worker is unavailable or fails
- **THEN** the deterministic pass and its report MUST land unaffected and no derived possible is persisted

#### Scenario: A child exceeds its bounds
- **WHEN** a derivation child is queued beyond ten minutes or runs beyond thirty minutes
- **THEN** the watchdog MUST report and cancel it

#### Scenario: Output merges on a later run
- **WHEN** a derivation child returns after its dispatching run has closed
- **THEN** its immutable evidence MUST be merged by a later main run and the closed run's records MUST NOT be edited

#### Scenario: A concurrent run advanced the register
- **WHEN** a merge would overwrite a `possibles_register` a concurrent run has already advanced
- **THEN** the merge MUST refuse the stale overwrite rather than clobber the newer state

### Requirement: Derived possibles are a distinct class until disposed
Undisposed derived possibles SHALL be contractually and visually distinct from
human-picked possibles wherever the index is consumed: their cross-class edges
SHALL carry a non-`indexed` edge class (`inferred` or `synthesized`) in the
dashboard/WHEEL realization data contract, and no consumer SHALL render or count
an undisposed derived possible as human-picked, indexed data.

Real derived possibles populating the register replace the WHEEL's
synthesized-and-demo-marked placeholders (the "possibles honesty rule"); once a
derived possible is disposed accepted it MAY be treated as real register data,
but until then it is never confusable with indexed edges.

#### Scenario: The WHEEL renders derived possibles
- **WHEN** the WHEEL renders a possibles column containing undisposed derived possibles
- **THEN** their possible-to-cluster edges MUST carry a non-`indexed` class and be visually distinct from indexed human-picked edges

#### Scenario: A consumer counts possibles
- **WHEN** a consumer reports possible counts or a ranked plan
- **THEN** undisposed derived possibles MUST be excluded from human-picked totals and from any ranked plan

### Requirement: Non-mutating derivation bound
The derivation lane SHALL be non-mutating over source content: it writes and
updates only the cross-reference index (the `possibles_register` section) and its
evidence artifacts. It MUST NOT edit, move, promote, or delete any brainstorm,
staging, or archived document; archived material is read-only reference for
deriving candidates, and no third standalone possibles file is created.

#### Scenario: The lane runs
- **WHEN** a derivation pass completes and merges
- **THEN** the only repository writes are the `possibles_register` section of the index and the lane's evidence artifacts

#### Scenario: The lane observes a source defect
- **WHEN** the lane observes a defect in a member document while deriving
- **THEN** it records the observation in evidence and MUST NOT modify the document

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

