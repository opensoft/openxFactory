# domain-conformance-checks — add-client-identity-roster deltas

## MODIFIED Requirements

### Requirement: The conformance-check pack is openxFactory-owned and runs from the pinned checkout
The neutral domain-repo conformance-check pack — `scripts/check-inventory-consistency.py` (inventory consistency), `scripts/check-workflow-state-parity.py` (workflow state parity), `scripts/check-openxfactory-pin.py` (openxFactory pin ancestry), and `scripts/validate-client-identity-roster.py` (client identity roster conformance) — SHALL be owned by openxFactory and run from the pinned openxFactory checkout against a target domain repository, never copied into domain repos.
Each check takes its target (the domain repo root, or its `workflows/`
directory) as an explicit argument, the same consumption shape as the
existing canonical validators. Pack membership is what confers BLOCKING
status: the roster check joins the pack because a nonzero exit from any
member fails the domain gate, and no other promoted mechanism makes a
canonical validator blocking.

#### Scenario: A domain repo invokes the pack from its pinned checkout

- **WHEN** a DomainxFactory validate chain resolves its pinned openxFactory checkout (via `OPENXFACTORY_ROOT` or the aggregation sibling path)
- **THEN** the four checks are invocable from that checkout against the domain repository, each handed the target repo (or its workflows directory) as an argument
- **AND** a nonzero exit from any check fails the domain gate

#### Scenario: A copied check is a conformance defect

- **WHEN** a copy of one of these check scripts is found inside a domain repository
- **THEN** it is a conformance defect of this capability, and the domain gate MUST be repointed at the pinned-checkout copy

#### Scenario: The pin-check overlap is a declared non-goal

- **WHEN** `check-openxfactory-pin.py` and `validate-domain-openxfactory-pins.py` coexist on the openxFactory scripts surface
- **THEN** both remain valid entry points — the pin checker classifies aggregation-pointer ancestry, the canonical validator checks the declared pin block — and merging them is deliberately deferred to its own change (design D3), not a defect of this capability

#### Scenario: A roster nonconformance fails the gate rather than reporting

- **WHEN** `validate-client-identity-roster.py` finds an intra-repo entry nonconformance in the target repo's roster fragments
- **THEN** it exits nonzero and the domain gate fails
- **AND** the cross-domain composition concerns are NOT reported here — they are the doc-health family's, which leaves the gate exit unchanged

### Requirement: The verified properties hold for a conformant domain repo
For a conformant DomainxFactory repository, each check's verified property SHALL hold: `stack.yaml` required-artifact lists, the artifacts shipped on disk, and the `schemas/README.md` table agree (with `stack.yaml` the declared source of truth); every workflow `.md`'s transition-target states equal its paired `.yaml` gates' `produces[]` states; the `stack.yaml` `xfactory.contract_ref` sits on the ancestry of the aggregation repo's recorded openxFactory submodule pointer; and every roster fragment the repo publishes satisfies the intra-repo entry rules of `client-identity-roster` while carrying the roster kind only at the contract's declared placement.

#### Scenario: Inventory agreement

- **WHEN** `check-inventory-consistency.py` runs against a conformant domain repo
- **THEN** every `stack.yaml` `schemas.required`/`workflows.required` entry exists on disk, every shipped schema and workflow (with its `.yaml` gate-contract pair) is declared, and the `schemas/README.md` table matches the shipped set
- **AND** any disagreement is reported as an error naming the drifted artifact, exiting nonzero

#### Scenario: Workflow state parity

- **WHEN** `check-workflow-state-parity.py` runs against the domain repo's `workflows/` directory
- **THEN** for every `.md`/`.yaml` workflow pair, the `.yaml` gates' `produces[]` state set equals the `.md` transition-target state set — excluding `blocked`, which the `.yaml` expresses via `blocks_when[]` — with the `.md` the authoritative state machine
- **AND** divergence is reported naming the workflow and the mismatched states, exiting nonzero

#### Scenario: Pin ancestry

- **WHEN** `check-openxfactory-pin.py` runs against a domain repo inside an aggregation checkout
- **THEN** it passes on stack-pin/submodule-pointer equality, warns with the refresh instruction when the pin is a proper ancestor (stale-behind is legal but must be visible), and errors when the pin is not an ancestor of the pointer (the declared contract is off the submodule's history)
- **AND** outside an aggregation checkout it skips with an explicit notice rather than failing or passing silently

#### Scenario: Roster entry conformance

- **WHEN** `validate-client-identity-roster.py` runs against a domain repo publishing roster fragments at the declared placement
- **THEN** every entry satisfies the intra-repo rules — uniqueness tuple, closed vocabularies, verified admission, achieved-versus-intended authority, resolvable gate obligation, residency model, lifecycle and attestation, and both roots — and a violation is reported naming its own rule, exiting nonzero
- **AND** an instance carrying the roster kind outside the declared placement is reported as a misplacement finding rather than skipped as out of scope

#### Scenario: A target repo publishes no roster fragment

- **WHEN** the roster check runs against a domain repo that publishes no roster fragment at all
- **THEN** it passes with an explicit notice naming the absence, exiting 0
- **AND** neither a missing fragment nor a missing entry is a finding, because this release enforces no roster completeness rule and scoped completeness is a named successor change
