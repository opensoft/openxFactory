# ideation-dashboard Delta: Staged-Topic Proposal Commissioning

## ADDED Requirements

### Requirement: Staged-topic proposal commissioning
The gate console SHALL offer a human-only `propose` action on a staging topic that commissions proposal authoring as a recorded dispatch — a `workflow-job` descriptor naming the proposal-authoring workflow and targeting the topic's staging id, plus a gate-action record — without authoring anything itself; the commissioned authoring runs externally and lands as an ordinary OpenSpec change subject to the existing review and ratify gates. The console SHALL refuse a topic absent from the pinned checkout's staging area and SHALL refuse a duplicate commission while a dispatched `propose` job for the same topic remains undelivered.

#### Scenario: A staged tile is taken toward proposal
- **WHEN** a human runs the propose action on a staging topic
- **THEN** a `workflow-job` descriptor (workflow `proposal-authoring`, target `topic_id`) and a `propose` gate-action record are written through the human gate
- **AND** no proposal artifact is authored by the console itself

#### Scenario: A missing topic is refused
- **WHEN** propose is invoked for a topic id with no directory under the checkout's `ideation/staging/`
- **THEN** the console MUST refuse with the reason and persist nothing

#### Scenario: A duplicate commission is refused
- **WHEN** propose is invoked for a topic that already carries a dispatched, undelivered `propose` workflow-job
- **THEN** the console MUST refuse, citing the existing dispatch

#### Scenario: An agent invokes propose
- **WHEN** any agent or automated path calls the propose action
- **THEN** the call MUST be rejected and reported, like every gate action
