# credential-contracts

## ADDED Requirements

### Requirement: A declared requirement reference is resolved on its own binding, whatever that binding shares
A `requirement_ref` declared on a credential binding SHALL be RESOLVED, and a resolution returning ZERO requirements or MORE THAN ONE SHALL be REPORTED on the binding that declares it — on EVERY such binding, and NOT ONLY on a binding whose `secret_ref` is shared with another.

THE SHARED SECRET REFERENCE IS A PROXY HERE TOO, AND THIS FAMILY HAS ALREADY
RULED ON THAT PROXY ONCE. Of the authority collapse the same capability says, in
terms, that *"a shared secret reference is a proxy for the rule and not the
rule"*, and raises that finding on the holder/fetch-identity pair independently
of `secret_ref`. A reference that resolves to nothing is a defect OF THE
REFERENCE, not of a pair: the record names a requirement the repository under
validation does not carry, and it names it whether or not some other binding
happens to point at the same vault entry. Reporting it only where an EXEMPTION
was being asked for reports the defect exactly where a reader was already being
refused, and stays silent everywhere it merely sits.

THREE CLAUSES OF THE INTRODUCING PACKET ARE RECONCILED HERE RATHER THAN LEFT TO
A READER TO SETTLE. Its block requirement states the duty GENERALLY — a
reference *"that resolves to zero or to more than one requirement SHALL be
reported and SHALL NOT be treated as resolved"* — with no predicate about
sharing. Its lift requirement carries a scenario whose WHEN opens *"two bindings
share a `secret_ref`"*. Its task list § 2.5 states the duty as a CONJUNCTION:
*"ZERO matches AND MORE THAN ONE match both report and withhold the lift"*. The
three agree the moment the conjunction is SPLIT: REPORTING is owed by every
binding that declares a reference, and WITHHOLDING is owed by the pair that asks
for the exemption. The lift's scenario is a scenario ABOUT THE LIFT and is not a
bound on the reporting duty; § 2.5 describes what a sharing pair gets, which is
both halves at once. Nothing in the sibling is contradicted by this requirement
and nothing in it is restated — this is the reporting half, given the home it
never had.

TWO FINDINGS ON ONE SHARING PAIR ARE NOT A DUPLICATE, and the family's "a
refusal shall name the fault it found, and name it once" rule is not breached by
them. They answer DIFFERENT QUESTIONS: whether this reference is sound, and
whether this pair may be exempted from the default refusal. A reader repairing
the reference discharges the first, while the second may still stand on a
different condition — a shared holder reference, a one-sided acknowledgment, a
dispatch-only access mode — and telling that reader only about the pair leaves
them repairing a record whose reference is still wrong. The rule this family
wrote against duplicates is a rule against TWO NAMES FOR ONE FAULT, not against
two faults in one record.

ZERO AND MORE-THAN-ONE ARE NAMED APART, because their remedies are different.
A reference resolving to NOTHING is repaired at the reference — the id is
misspelled, the document moved, or the requirement was never written. A
reference resolving to SEVERAL is repaired in the REQUIREMENTS DOCUMENT, by
making the ids it declares unique, and it is the more dangerous of the two:
requirement ids carry no repository-wide uniqueness, the matches may differ in
`access_mode`, and a reader told only that "the reference did not resolve" has
no way to know that two records answered.

THE RESOLVER'S EXISTING SAFETY RULES ARE PRESERVED AND ARE NOT RE-EARNED HERE.
Resolution SHALL continue to run ONLY against `xfactory_credential_requirements`
records the validator itself discovered and schema-checked in the tree under
validation, and the validator SHALL NEVER OPEN A PATH TAKEN FROM A RECORD. This
requirement adds no new read, no new path and no new input: it reports a
resolution the validator already performs and today discards on every code path
but one.

AN UNDECLARED REFERENCE IS NOT AN UNRESOLVED ONE. The member is OPTIONAL at the
release that declares it, and a binding that declares no `requirement_ref` SHALL
draw nothing from this requirement. The subject is a reference that IS declared
and does not resolve — the fail-open shape this family has already had to repair
once, in a drift check that treated what it could not read as satisfied.

#### Scenario: A reference that resolves to nothing on a binding that shares nothing
- **WHEN** a binding declares a qualified, grammatical `requirement_ref` matching no requirement record in the repository under validation, and no other binding in the document shares its `secret_ref`
- **THEN** the unresolvable reference MUST be reported on that binding
- **AND** the report MUST NOT depend on any other binding in the document, on the vault, the owner, the provider or the consumer any other binding declares

#### Scenario: A reference that resolves to several on a binding that shares nothing
- **WHEN** a binding declares a qualified, grammatical `requirement_ref` matching more than one requirement record, and no other binding shares its `secret_ref`
- **THEN** the ambiguity MUST be reported on that binding
- **AND** an implementation MUST NOT resolve the ambiguity by picking one, the matches being free to differ in `access_mode`

#### Scenario: The shipped check is silent on both of them today
- **WHEN** the conformance validator as shipped at the release that introduces the consumer block is run over a binding template whose only defects are one reference resolving to nothing and one resolving to two records with different access modes, and whose bindings declare `secret_ref`s that differ from each other by a SINGLE BYTE
- **THEN** it reports NEITHER, which is the gap this requirement closes
- **AND** making the two `secret_ref`s equal — that one byte, and no other edit to any file — MUST be enough to make the same tree report, which is what identifies the scope as the defect rather than the depth of the check

#### Scenario: A reference that resolves draws nothing
- **WHEN** a declared reference matches exactly one requirement record in the repository under validation
- **THEN** nothing about resolution is reported for that binding, whatever it shares with any other

#### Scenario: A binding that declares no reference draws nothing
- **WHEN** a binding declares a consumer block carrying no `requirement_ref`
- **THEN** nothing about resolution is reported, the member being optional at this release and an omission being a different question from a wrong answer

#### Scenario: The sharing pair keeps both duties
- **WHEN** two bindings share a `secret_ref` and one of them names a reference that resolves to nothing
- **THEN** the lift MUST stay UNAVAILABLE and the default refusal MUST stand exactly as it does today
- **AND** the unresolvable reference MUST ALSO be reported on the binding that declares it, the two findings answering different questions rather than naming one fault twice

### Requirement: Resolution integrity carries its own code and phases like every other narrowing
The resolution-integrity finding SHALL carry a code of ITS OWN FAMILY — never a widening of a code that already names a different fault — and, because a record carrying an unresolvable reference VALIDATES on the current major, it SHALL be emitted as a WARNING for a full minor and enforced as an ERROR only at the major that refuses it.

IT IS NOT A NINTH CODE ON THE CONSUMER BLOCK, and the reason is the block
packet's own enumeration rule. Those codes are ENUMERATED AGAINST THE REFUSALS
that land at the major, and each names a SHAPE fault: a block that is missing,
incomplete, closed-and-violated, ungrammatical, or carrying a token declared
false. A reference that resolves to nothing is none of those. It is
well-formed, inside the declared member set, grammatical in both members, and
WRONG ABOUT THE WORLD. Filing it under a grammar code would make that code
untrue in the other direction — a code whose meaning is "this value does not
match the pattern" would come to carry a record whose values match every pattern
this family declares.

AND THE ENUMERATION RULE IS SATISFIED BY MAKING THE MAJOR REFUSE THE SHAPE, NOT
BY EXEMPTING IT FROM THE RULE. The sibling's rule is that a warning set is
derived from the list of things the major refuses — a warning no refusal ever
follows is a warning with no deprecation to serve. So this requirement does not
smuggle a warning into a set that answers to nothing: it declares AN ACT AT THE
MAJOR — a declared reference that resolves to zero or to more than one
requirement is REFUSED there — and the warning is that act's deprecation window.
The sibling's enumeration stays exhaustive of the acts IT names; this act
carries its own code, its own packaged probe and its own row.

THE PHASING IS MEASURED RATHER THAN ASSERTED, because the versioning policy's
test is whether the CURRENT major accepts the value the next one would refuse. A
binding template declaring two bindings with DISTINCT secret references, one
naming a requirement id no record carries and one naming an id two records carry
with DIFFERENT access modes, validates with zero errors and zero warnings under
the shipped validator. It is therefore a shape the current major accepts, and
refusing it is the BREAKING class however obviously wrong the record looks —
which the policy answers with at least one full minor of deprecation warnings, a
migration note, and a validator that refuses the old shape only at the new major.

THE DEPRECATION SHALL BE DECLARED WHERE A CONSUMER UPGRADING ACROSS IT WILL READ
IT, and the entry that already claims to name EVERY act landing at that major
SHALL be reconciled with it rather than left to contradict it. An entry asserting
completeness that is not complete is worse than one asserting nothing, because a
reader at the major uses it to demonstrate that the deprecation precondition was
met, and cannot tell an act that served its window from one that never had an
entry.

THE CORPUS SHALL PROBE BOTH DIRECTIONS, and the silent direction is the one that
distinguishes a working check from one that fires on everything. Each code SHALL
carry a registered packaged probe, and a positive record whose reference resolves
to exactly one requirement and whose bindings share no secret SHALL stay silent —
a corpus holding only the failing direction cannot tell the two apart.

#### Scenario: The finding is not a widening of an existing code
- **WHEN** an unresolvable or ambiguous declared reference is reported
- **THEN** its code MUST NOT be one of the codes that name the consumer block's shape or grammar faults
- **AND** a reader MUST be able to tell a resolution failure from a grammar failure by the code alone, without reading the message

#### Scenario: Zero and more-than-one are named apart
- **WHEN** one record carries a reference resolving to nothing and another carries a reference resolving to several
- **THEN** the two MUST be reported under DISTINCT codes, their remedies being at the reference and in the requirements document respectively
- **AND** neither MUST be reported as the other

#### Scenario: The introducing minor warns and refuses nothing
- **WHEN** the check lands at an additive minor
- **THEN** a record whose only defect is a declared reference that does not resolve MUST stay VALID and MUST draw a WARNING
- **AND** the verdict MUST NOT redden on it, a warning never being a refusal

#### Scenario: The major refuses what the minor warned about
- **WHEN** the major this deprecation names is cut
- **THEN** the same record MUST be REFUSED
- **AND** the removal target and the migration MUST be stated where a consumer upgrading across the major reads them

#### Scenario: The completeness claim beside it stays true
- **WHEN** an act lands at a major whose deprecation entry claims to name every act landing there
- **THEN** that entry MUST either carry the new act or name the entry that does
- **AND** an entry that claims completeness while omitting an act MUST be treated as a defect of the entry rather than of the act

#### Scenario: Both directions are packaged
- **WHEN** the packaged corpus is self-tested
- **THEN** every declared code MUST carry a registered probe
- **AND** a positive record whose reference resolves and whose bindings share no secret MUST stay silent, so a check that fired on every record would fail the corpus rather than pass it
