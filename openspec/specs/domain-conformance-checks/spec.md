# domain-conformance-checks Specification

## Purpose
TBD - created by archiving change adopt-neutral-utility-pack. Update Purpose after archive.
## Requirements
### Requirement: The conformance-check pack is openxFactory-owned and runs from the pinned checkout
The neutral domain-repo conformance-check pack — `scripts/check-inventory-consistency.py` (inventory consistency), `scripts/check-workflow-state-parity.py` (workflow state parity), and `scripts/check-openxfactory-pin.py` (openxFactory pin ancestry) — SHALL be owned by openxFactory and run from the pinned openxFactory checkout against a target domain repository, never copied into domain repos.
Each check takes its target (the domain repo root, or its `workflows/`
directory) as an explicit argument, the same consumption shape as the
existing canonical validators.

#### Scenario: A domain repo invokes the pack from its pinned checkout

- **WHEN** a DomainxFactory validate chain resolves its pinned openxFactory checkout (via `OPENXFACTORY_ROOT` or the aggregation sibling path)
- **THEN** the three checks are invocable from that checkout against the domain repository, each handed the target repo (or its workflows directory) as an argument
- **AND** a nonzero exit from any check fails the domain gate

#### Scenario: A copied check is a conformance defect

- **WHEN** a copy of one of these check scripts is found inside a domain repository
- **THEN** it is a conformance defect of this capability, and the domain gate MUST be repointed at the pinned-checkout copy

#### Scenario: The pin-check overlap is a declared non-goal

- **WHEN** `check-openxfactory-pin.py` and `validate-domain-openxfactory-pins.py` coexist on the openxFactory scripts surface
- **THEN** both remain valid entry points — the pin checker classifies aggregation-pointer ancestry, the canonical validator checks the declared pin block — and merging them is deliberately deferred to its own change (design D3), not a defect of this capability

### Requirement: The verified properties hold for a conformant domain repo
For a conformant DomainxFactory repository, each check's verified property SHALL hold: `stack.yaml` required-artifact lists, the artifacts shipped on disk, and the `schemas/README.md` table agree (with `stack.yaml` the declared source of truth); every workflow `.md`'s transition-target states equal its paired `.yaml` gates' `produces[]` states; and the `stack.yaml` `xfactory.contract_ref` sits on the ancestry of the aggregation repo's recorded openxFactory submodule pointer.

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

