# doc-health Specification Delta

## MODIFIED Requirements

### Requirement: Proposal-origin checks enforced by reference
The `proposal-origin` deterministic check family SHALL enforce the promoted
origin requirements of `document-lifecycle` and `release-realization` by
reference. It SHALL report an active or archived proposal with no origin
declaration; an unknown or malformed origin kind or id; a staged origin
whose id, path, or staging-header linkage does not resolve against its
recorded provenance; a mismatch among staging header, proposal packet, and
support manifest; an ad-hoc origin lacking `reason`; an ad-hoc origin that
claims approval without the whole of the approval pair; an ad-hoc origin
that declares neither approval nor drafting provenance, and so declares no
provenance state at all; an ad-hoc origin whose declared drafting provenance
is incomplete; a proposal whose own declared status claims ratification or
beyond while its origin asserts no approval;
and mutation of an origin declaration after ratification. Backfilled
origins SHALL be validated against recorded migration provenance; the
family MUST NOT fabricate or infer staging history for changes that predate
the contract.

The family's finding classes are therefore SEVEN, named: `missing-origin`,
`malformed-origin`, `origin-mismatch`, `staged-origin-unresolvable`,
`adhoc-provenance-incomplete`, `drafting-provenance-incomplete`, and
`unapproved-origin-at-ratification`. The last two are added by
`add-drafted-proposal-origin` and are the two halves of one rule: an
unapproved draft is EXPRESSIBLE, and an approval APPEARS when a status claims
it.

**THE UNAPPROVED STATE PRODUCES NO FINDING, AND THAT IS THE POINT OF ADDING
IT.** Before it existed this family reported every drafted-but-unapproved
packet — an `ad_hoc` origin without `approved_on` was
`adhoc-provenance-incomplete`, a packet with no origin block at all was
`missing-origin`, and no third shape existed, so the only ways to clear the
finding were to approve the change, delete the draft, or invent an approval
date. The last is the defect this family exists to catch, and a rule whose
only mechanical remedy is the defect it forbids does not survive contact with
the repository's own workflow: a "scout and draft, do not implement"
assignment is SUPPOSED to yield a packet that exists, validates, and is not
yet approved.

`unapproved-origin-at-ratification` is `error` with resolution class
`contested`, and the class is argued rather than inherited: resolving the
finding either TRANSCRIBES an approval act that happened or WITHDRAWS a status
claim that should not have been made, and the third move — writing a date
nobody gave — is the defect. `drafting-provenance-incomplete` is mechanical:
a half-written pair is completed from the record of who drafted it.

The status the last class reads SHALL be the packet's own declared `Status:`,
read through the single lifecycle-header reader this contract already
requires, and the class SHALL fire only where the packet POSITIVELY declares
the unapproved state. Silence is not that state: an origin that merely omits
its approval has declared no provenance state and is reported as such, so a
packet cannot buy the lenient treatment by leaving fields out. Archival is
not a status claim either — an archived packet may lawfully declare a
pre-ratification standing, and this family MUST NOT read the fact of
archiving as the approval its origin does not carry.

#### Scenario: A proposal lacks an origin declaration
- **WHEN** an active or archived proposal carries no origin declaration and no recorded migration exemption
- **THEN** the run MUST emit a `proposal-origin` finding naming the change and the violated requirement

#### Scenario: Origin declarations disagree
- **WHEN** the staging header, the `.openspec.yaml` declaration, and the support manifest do not agree on origin kind, id, or path
- **THEN** the run MUST emit a `proposal-origin` finding identifying each disagreeing record

#### Scenario: An origin was mutated after ratification
- **WHEN** an origin declaration differs from the declaration recorded at ratification
- **THEN** the run MUST emit an `error` finding with resolution class `contested` — resolving it reverses a gate decision

#### Scenario: A pre-contract change carries a backfilled origin
- **WHEN** an archived change's origin was backfilled by the recorded migration
- **THEN** the family MUST validate it against the migration provenance record and MUST NOT report it merely for having been declared late

#### Scenario: An unapproved draft declares its origin
- **WHEN** a proposal declaring a pre-ratification standing carries an ad-hoc origin with `reason`, `proposed_by`, and `proposed_on`, and no approval fields
- **THEN** the family MUST report nothing against that origin
- **AND** the absence of `approved_by` and `approved_on` MUST NOT be reported as incomplete provenance

#### Scenario: A declared status claims a ratification the origin does not carry
- **WHEN** a proposal's own `Status:` declares `ratified` or any standing beyond it while its origin carries drafting provenance and asserts no approval
- **THEN** the family MUST emit an `error` finding with resolution class `contested`, naming the declared status
- **AND** the finding MUST NOT be resolvable by writing an approval date the record does not carry

#### Scenario: Declared drafting provenance is incomplete
- **WHEN** an ad-hoc origin declares one of `proposed_by` or `proposed_on` and not the other, and asserts no approval
- **THEN** the family MUST emit an `error` finding naming the missing field as a drafting-provenance defect rather than as a missing approval

#### Scenario: An ad-hoc origin declares no provenance state
- **WHEN** an ad-hoc origin carries neither a complete approval pair nor any drafting field
- **THEN** the family MUST emit one `error` finding naming both lawful shapes rather than one finding per absent approval field

#### Scenario: A claimed approval is incomplete
- **WHEN** an ad-hoc origin carries one of `approved_by` or `approved_on` without the other
- **THEN** the family MUST report the missing field exactly as it did before the unapproved state existed

#### Scenario: The origin contract evolves
- **WHEN** a later OpenSpec change modifies the promoted origin requirements
- **THEN** the family MUST follow the owning requirements by reference rather than a stale implementation copy
