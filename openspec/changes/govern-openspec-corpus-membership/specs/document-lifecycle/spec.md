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

The pre-existing population SHALL be discharged rather than grandfathered:
this requirement defines NO contract date and NO reduced-severity legacy
class, so a packet carrying no `Status:` header is a current violation
whenever it was authored. Backfilling a header onto an archived packet is an
archived-record edit and takes the route archived-record edits take.

Deriving a header is nevertheless authoring, not correcting, and the rule is
bounded accordingly: a `Status:` value and, where that value is `ratified`,
its citation SHALL be derived from the packet's own record — its origin
declaration, its ratification or archive commit, its own task record, or the
index row that announced it. Where the record supports neither, the document
SHALL be reported by name, stating what its record does and does not carry,
and SHALL NOT be given a header the record does not support. A packet whose
own archive record states a decision against carrying a status value keeps
that decision; overturning it takes a ruling naming it, not a backfill pass.

#### Scenario: A proposal declares its standing
- **WHEN** a change packet's `proposal.md` is authored or amended
- **THEN** it MUST carry a `Status:` header drawn from the controlled taxonomy, within the lifecycle header window
- **AND** where that status is `ratified` it MUST carry exactly one ratification citation, in the spelling the citation's own condition of use selects

#### Scenario: A review record records a ratification
- **WHEN** a `review/` document under a change packet records that the change was ratified
- **THEN** it MUST carry `Status: ratified` and one ratification citation in a sanctioned spelling
- **AND** a `Ratifier:` or `Decision date:` header MAY accompany the citation but MUST NOT stand in place of it

#### Scenario: A pre-existing packet carries no header
- **WHEN** a proposal packet authored at any date carries no `Status:` header
- **THEN** it MUST be reported as a current violation at full severity, because this requirement defines no contract date and no pre-contract legacy class
- **AND** the remedy MUST be a header derived from that packet's own record, not a reduced severity that leaves the claim unmade

#### Scenario: A record cannot support a derived header
- **WHEN** a packet's own record supports neither a `Status:` value nor, for a `ratified` value, a citation clearing the ratification floor
- **THEN** the document MUST be reported by name together with what its record does and does not carry
- **AND** a header the record does not support MUST NOT be written, because an invented provenance is a worse defect than the missing one it hides
- **AND** where the packet's archive record states a decision against carrying a status value, that decision stands until a ruling names it

#### Scenario: A packet working file carries no lifecycle header
- **WHEN** a change packet's `tasks.md`, `design.md`, spec delta, supporting document, or evidence file carries no `Status:` header
- **THEN** no finding is emitted under this requirement, because this requirement does not reach those files
