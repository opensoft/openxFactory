# document-lifecycle Specification Delta

## ADDED Requirements

### Requirement: Proposal packets carry the lifecycle header
An OpenSpec change packet's `proposal.md`, and EVERY `review/` record under that packet, SHALL be governance documents for the purposes of the controlled status taxonomy and the ratification-citation rule.

Both carry a claim about the document's standing — a proposal says whether it
is `draft` or `ratified`; a review record says what standing its own finding
has, whether that is a ratification, a captured `record` of a review that
happened, or a superseded earlier round. A claim of standing is what the
taxonomy exists to make checkable, and a review record makes one whatever its
subject. The rest of the packet is deliberately NOT ruled here: `tasks.md`,
`design.md`, spec delta files, `supporting-docs/` and `evidence/` are working
files of the change rather than documents making a standing claim, and whether
they are governance documents is a separate question this capability leaves
open.

The two obligations this requirement creates are DIFFERENT in reach, and
conflating them would over-state the rule:

- The **taxonomy** obligation reaches every document named above. A
  `review/` record SHALL carry a `Status:` header drawn from the controlled
  taxonomy, within the lifecycle header window, whatever its subject. A
  review record that is not about a ratification most often carries
  `Status: record`, which is a conforming value and needs nothing further.
- The **ratification-citation** obligation reaches only those documents whose
  status IS `ratified`. A `review/` record carrying any other taxonomy value
  owes no citation, and demanding one of a `record` would be demanding
  provenance for a claim the document does not make.

A `review/` record whose status IS `ratified` and which names its ratifier and
decision date in its own vocabulary SHALL additionally carry a citation in one
of the two sanctioned spellings. Recording the same fact twice is the cost of
having one rule; inventing a third spelling for documents whose whole subject
is ratification would undo the single-rule result the two-spelling sanction
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

#### Scenario: A review record is not about a ratification
- **WHEN** a `review/` document under a change packet records a finding, a disposition, a captured review round, or any other subject that is not the ratification of that change
- **THEN** it MUST still carry a `Status:` header drawn from the controlled taxonomy, within the lifecycle header window, because it is a governance document under this requirement whatever its subject
- **AND** it MUST NOT be required to carry a ratification citation, because the citation rule binds a `ratified` status and this document does not claim one

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
