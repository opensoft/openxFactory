# document-lifecycle Specification Delta

## ADDED Requirements

### Requirement: Proposal packets carry the lifecycle header
An OpenSpec change packet's `proposal.md`, and any `review/` record whose subject is the ratification of that change, SHALL be governance documents for the purposes of the controlled status taxonomy and the ratification-citation rule.

Both carry a claim about the document's standing — a proposal says whether it
is drafted or ratified, a review record says a ratification happened — and a
claim of standing is what the taxonomy exists to make checkable. The rest of
the packet is deliberately NOT ruled here: `tasks.md`, `design.md`, spec
delta files, `supporting-docs/` and `evidence/` are working files of the
change rather than documents making a standing claim, and whether they are
governance documents is a separate question this capability leaves open.

A `review/` ratification record that names its ratifier and decision date in
its own vocabulary SHALL additionally carry a citation in one of the two
sanctioned spellings. Recording the same fact twice is the cost of having one
rule; inventing a third spelling for documents whose whole subject is
ratification would undo the single-rule result the two-spelling sanction
reached.

The pre-existing population is a matter of enforcement severity, not of the
rule: a packet authored before this requirement's contract date and never
migrated is reported at a reduced severity naming it as pre-contract legacy,
in the same shape the proposal-origin contract already uses for packets
predating its own date. Backfilling a header onto an archived packet is an
archived-record edit and takes the route archived-record edits take.

#### Scenario: A proposal declares its standing
- **WHEN** a change packet's `proposal.md` is authored or amended
- **THEN** it MUST carry a `Status:` header drawn from the controlled taxonomy, within the lifecycle header window
- **AND** where that status is `ratified` it MUST carry exactly one ratification citation, in the spelling the citation's own condition of use selects

#### Scenario: A review record records a ratification
- **WHEN** a `review/` document under a change packet records that the change was ratified
- **THEN** it MUST carry `Status: ratified` and one ratification citation in a sanctioned spelling
- **AND** a `Ratifier:` or `Decision date:` header MAY accompany the citation but MUST NOT stand in place of it

#### Scenario: A packet predates the contract date
- **WHEN** a proposal packet authored before this requirement's contract date carries no `Status:` header
- **THEN** it MUST be reported as pre-contract legacy at a reduced severity rather than as a current violation
- **AND** the reduced severity MUST NOT be extended to a packet authored after that date

#### Scenario: A packet working file carries no lifecycle header
- **WHEN** a change packet's `tasks.md`, `design.md`, spec delta, supporting document, or evidence file carries no `Status:` header
- **THEN** no finding is emitted under this requirement, because this requirement does not reach those files
