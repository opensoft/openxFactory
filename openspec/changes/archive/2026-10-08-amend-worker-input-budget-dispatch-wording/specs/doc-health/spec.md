## MODIFIED Requirements

### Requirement: Bounded worker input budget
Every bounded worker lane SHALL bound the size of the input it sends to the
model, and SHALL NOT send an input that exceeds that bound. The budget is a
byte cap on the WHOLE assembled prompt — instruction contract, framing and
document payload together, because that whole text is what the model
receives — derived from the pinned model's context window with headroom
reserved for the worker's own output and the invoking tool's fixed
overhead. The budget SHALL travel with the dispatched bundle so the worker
enforces the same number the orchestrator recorded, rather than a
duplicated constant that can drift.

Two assembly shapes exist and the obligation differs between them. Where
the ORCHESTRATOR assembles the prompt, it SHALL pack within the budget and
defer what does not fit. Where the WORKER assembles the prompt from a
dispatchable unit the orchestrator prepared, the orchestrator SHALL measure
each unit's assembled size, record it, and SHALL NOT dispatch a unit it has
measured over the budget. The worker's refusal of an over-budget input
(scenario "A worker receives an input over the budget") is a backstop that
keeps such an input from reaching the model. It does not make an
over-budget dispatch conformant, and relying on it wastes the run, because
the same unit is selected again next run.

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

#### Scenario: A dispatchable unit measures over the budget
- **WHEN** the orchestrator measures a unit the worker would assemble and finds it over the input budget
- **THEN** that unit MUST NOT be dispatched, and the run MUST record it as measured over the budget
- **AND** the lane MUST proceed with the units that fit rather than spend the run on a call the model would refuse

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
