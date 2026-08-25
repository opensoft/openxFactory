# document-lifecycle

## MODIFIED Requirements

### Requirement: Controlled document status taxonomy
Every governance document SHALL carry a `Status:` header drawn from the
controlled taxonomy: `brainstorm`, `staged`, `draft`, `ratified`, `standard`,
`superseded`, `retired`, `record`. Document genre SHALL NOT be encoded in the
status value; an optional `Kind:` header carries genre.

**Ratification citation.** A `ratified` header SHALL name its ratification. A bare, uncited `Status: ratified` is a violation whatever else the document says, because the header asserts an approval the document does not point at. TWO citation spellings are sanctioned, and they are not interchangeable — each has a condition of use, and the condition is what decides which one is correct:

- `Ratified by: <change>` is the PRIMARY spelling and SHALL be used wherever an approving OpenSpec change exists to name. The named change IS the citation.
- `Ratified:` is the RECORD-CITING alternative and SHALL be used only where no approving OpenSpec change exists to name — an in-session ruling, a disposition, an `.openspec.yaml` approval pair, an archive or ratification commit, or another durable record. Reaching for the primary spelling in that situation would mean naming a change that does not exist.

A document SHALL carry exactly one ratification citation, in one of the two spellings. The count is ONE TOTAL across both spellings: a document MUST NOT carry one of each, and MUST NOT carry the same spelling twice. Two lines each claiming to name the ratification say nothing about which is current, whether or not they are spelled alike.

**The three-way floor on the record-citing form.** A `Ratified:` citation SHALL name at least one of three things: an approver, a date, or a resolvable record path. Naming none of the three is a finding, because such a line asserts a ratification nothing can be checked against — the bare uncited header's defect, differently spelled. The floor is deliberately a floor and not a fixed field set: the corpus's honest citations name different subsets (approver plus date plus a verbatim instruction; date plus a record pointer with no approver named; date alone where the record names no ratifier), and a rule demanding all three would force the invention of provenance the record does not carry, which is the failure mode this rule exists to prevent.

The floor SHALL apply to the `Ratified:` form only and SHALL NOT be applied to `Ratified by:`, whose named change is itself the resolvable record. A governed document whose `Ratified by:` line names its approving change and nothing else is correct as written and MUST NOT be reported.

A ratification citation is read in the document's lifecycle header, alongside the `Status:` header it justifies. Prose elsewhere in a document that begins with the same word — a section-level decision label, a sentence starting "Ratified together with…" — is body text and is NOT a ratification citation.

#### Scenario: A document claims standard authority
- **WHEN** a document's header declares `standard` status or its prose claims to be a shared xFactory standard
- **THEN** a promoted OpenSpec spec or canonical contract MUST back the claim
- **AND** absent such backing the document MUST carry `draft` or lower status

#### Scenario: A generated artifact is stored
- **WHEN** a simulation report, generated runbook, audit output, or other evidence artifact is committed
- **THEN** it MUST carry `record` status
- **AND** it MUST be excluded from prose-to-spec conversion and contradiction checks

#### Scenario: A document is superseded
- **WHEN** a later artifact replaces a document's content
- **THEN** the replaced document MUST move to `superseded` status naming its successor, or be deleted with the successor recording provenance

#### Scenario: An approving OpenSpec change exists
- **WHEN** a document carries `Status: ratified` and an approving OpenSpec change exists to name
- **THEN** it MUST cite that change with `Ratified by: <change>`
- **AND** the record-citing `Ratified:` spelling MUST NOT be used in its place

#### Scenario: A ratification has no approving OpenSpec change
- **WHEN** a document carries `Status: ratified` and no approving OpenSpec change exists — the ratification is an in-session ruling, a disposition, an `.openspec.yaml` approval pair, or another durable record
- **THEN** it MUST cite that record with `Ratified:` naming at least one of an approver, a date, or a resolvable record path
- **AND** the citation MUST NOT name a change that does not exist, and MUST NOT invent an approver, a date, or a record the evidence does not carry

#### Scenario: A record-citing ratification names nothing checkable
- **WHEN** a `Ratified:` citation names none of an approver, a date, or a resolvable record path
- **THEN** it MUST be reported as a finding
- **AND** a `Ratified by:` citation naming its approving change and nothing else MUST NOT be reported, because the named change is its record

#### Scenario: A ratified header carries no citation at all
- **WHEN** a document carries `Status: ratified` with neither a `Ratified by:` nor a `Ratified:` line in its lifecycle header
- **THEN** it MUST be reported as a finding
- **AND** body prose beginning with the word "Ratified" outside the lifecycle header MUST NOT be counted as the missing citation

#### Scenario: A ratified header carries more than one citation
- **WHEN** a document carries `Status: ratified` and its lifecycle header carries more than one ratification citation line — one in each spelling, or the same spelling twice
- **THEN** it MUST be reported as a finding, because two lines each claiming to name the ratification say nothing about which is current
- **AND** the violation MUST be reported on the count, not on the pair, so a second citation in the same spelling is the same finding as one of each — including where the first line alone would be correct
