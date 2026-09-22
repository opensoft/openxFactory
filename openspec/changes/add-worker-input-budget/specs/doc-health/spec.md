## MODIFIED Requirements

### Requirement: Sweep sequencing and snapshot consistency
The semantic sweep SHALL run after the deterministic pass and consume the
doc inventory that pass emits (paths, statuses, content hashes), so both
passes report against the same corpus snapshot; the changed-docs set for
incremental sweeps is derived from inventory hash diffs against the
previous report. The set actually SENT to the analysis worker MAY be a
subset of that changed-docs set where the assembled input would exceed the
worker input budget, and where it is a subset the run MUST report which
documents were held back — the sweep's corpus statement alone no longer
describes what was analyzed.

#### Scenario: A nightly run executes both passes
- **WHEN** the nightly run completes
- **THEN** the sweep's corpus is exactly the deterministic pass's inventory for that run
- **AND** the final report MUST verify that the prepared inventory matches the immutable checkout before merging worker findings

#### Scenario: The deterministic pass fails
- **WHEN** the deterministic pass fails before emitting an inventory
- **THEN** the sweep MUST NOT run against a stale inventory and MUST be reported as skipped

#### Scenario: The input budget holds documents back
- **WHEN** the input budget excludes documents the scope selected
- **THEN** the report MUST state the budget, the bytes actually sent, the number of documents sent, and the number deferred
- **AND** it MUST name every deferred document, an unnamed exclusion being indistinguishable from a document with nothing wrong with it

## ADDED Requirements

### Requirement: Bounded worker input budget
Every bounded worker lane SHALL bound the size of the input it sends to the
model, and SHALL NOT send an input that exceeds that bound. The budget is a
byte cap on the WHOLE assembled prompt — instruction contract, framing and
document payload together, because that whole text is what the model
receives — derived from the pinned model's context window with headroom
reserved for the worker's own output and the invoking tool's fixed
overhead. The budget SHALL travel with the dispatched bundle so the worker
enforces the same number the orchestrator packed against, rather than a
duplicated constant that can drift.

Packing SHALL be deterministic: the same corpus and the same budget always
produce the same prompt and the same held-back set. Documents SHALL be
included whole or not at all. Where the lane sends more than one population
of documents, each population SHALL have a reserved share of the budget, so
that no population can be starved to nothing by another.

#### Scenario: The assembled input would exceed the budget
- **WHEN** the documents a run selected assemble to more than the input budget
- **THEN** orchestration MUST pack documents up to the budget in a deterministic order and defer the remainder
- **AND** the dispatched bundle MUST record the budget, the bytes sent, the count sent, the count deferred, and the identity of every deferred document

#### Scenario: A single document exceeds the budget on its own
- **WHEN** one document's own size exceeds the input budget
- **THEN** that document MUST be deferred entire and recorded, and MUST NOT be sent in truncated or partial form
- **AND** the documents ordered after it MUST still be sent where they fit, one oversized document never starving the rest of the run

#### Scenario: A worker receives an input over the budget
- **WHEN** a bounded worker's assembled input exceeds the budget recorded in its bundle
- **THEN** the worker MUST refuse before invoking the model, emit an error naming the measured size and the budget, and exit non-zero
- **AND** it MUST NOT emit an empty result that orchestration would read as a completed analysis with no findings

#### Scenario: A prior finding's document was deferred
- **WHEN** a prior semantic finding is absent only because its document was deferred by the input budget
- **THEN** the prior finding MUST NOT be treated as resolved and MUST NOT generate an uncited-resolution error, exactly as an unavailable sweep does not

#### Scenario: Everything selected fits the budget
- **WHEN** the assembled input is at or under the budget
- **THEN** every selected document MUST be sent and the run MUST record no deferral
