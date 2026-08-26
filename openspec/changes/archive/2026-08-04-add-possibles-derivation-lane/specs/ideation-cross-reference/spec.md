# ideation-cross-reference Delta: Possibles Derivation Lane

## ADDED Requirements

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
