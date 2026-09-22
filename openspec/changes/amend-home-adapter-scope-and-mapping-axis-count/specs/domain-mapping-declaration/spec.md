# domain-mapping-declaration Specification

**ONE `## MODIFIED` REQUIREMENT, AND THE BLOCK CARRIES EVERY SCENARIO THE
PROMOTED REQUIREMENT HAS.** A `## MODIFIED` block REPLACES the requirement it
names, so all THREE promoted scenarios are carried below BYTE-IDENTICALLY —
extracted by script rather than retyped, and re-compared at `tasks.md` § 4.2
against the IMMUTABLE BASIS, the promoting delta archived at
`openspec/changes/archive/2026-09-22-split-opendox-two-layer-product/specs/domain-mapping-declaration/spec.md`,
and not against `openspec/specs/domain-mapping-declaration/spec.md`, which this
block rewrites when it archives and which the proof reads only to confirm it
still states that basis or this block — and ONE is added. No active change carries a delta on this capability (checked by
enumerating `openspec/changes/*/specs/` on `main` `4f92d651`), so there is no
collision, no basis marker is owed, and this block is written over canon as
promoted.

**WHAT THE AMENDMENT REACHES.** The AXIS COUNT and the identity of the sixth
axis, and nothing else. The parameterization obligation, the hardcoding refusal,
the DIRECTION Q5 citation and all three promoted scenarios are carried unedited,
and the two requirements below this one — including the one that MANDATES the
axis being added — are untouched: this packet adds no obligation, it names one
the corpus already carries.

## MODIFIED Requirements

### Requirement: A domain descendant declares its mapping, and the neutral layer ships no domain's vocabulary
A `<Domainx>Dox` descendant SHALL carry a DOMAIN MAPPING DECLARATION and the
neutral layer SHALL be parameterized by it rather than shipping any one domain's
words. The declaration SHALL cover exactly six axes: the domain's ARTIFACT
KINDS; the LIFECYCLE VOCABULARY each kind travels — its statuses, the legal
transitions between them, and the point at which a record becomes
immutable-with-addenda; the ACTS and the GATE each act passes; the EVIDENCE
CLASSES a derived statement must cite; the PROMOTING AUTHORITIES, named as
roles rather than as people; and the DERIVED-MODEL BOUNDARY — for every
derived-model family the domain declares under `governed-derived-model`, the
TRUTH STORE that family may never write and the EXTERNAL ENFORCEMENT point that
store sits behind — which the requirement *A mapping declaration names the truth
store its derived models may never write* below states in full. THE SIXTH AXIS
IS AN AXIS OF THIS DECLARATION AND NOT A FIELD OF `governed-derived-model`'s OWN
DIAL, and saying which it is, is the whole of what this clause adds: that
capability decides what a derived model may be, this declaration records what
each of THIS domain's families is non-authoritative ABOUT, and a closed axis
list that omitted the field could not tell an implementer whether declaring it
was forbidden or owed. A neutral layer that hardcodes one domain's status words,
artifact nouns or act verbs SHALL be reported, because every other descendant
then forks it — which is the failure DIRECTION Q5 was given to prevent.

**Removed from canon by amend-home-adapter-scope-and-mapping-axis-count (2026-09-22):** `The declaration SHALL cover exactly five axes: the domain's ARTIFACT KINDS; the LIFECYCLE VOCABULARY each kind travels — its statuses, the legal transitions between them, and the point at which a record becomes immutable-with-addenda; the ACTS and the GATE each act passes; the EVIDENCE CLASSES a derived statement must cite; and the PROMOTING AUTHORITIES, named as roles rather than as people.` — the ONE unit this block does not carry, declared rather than left to be noticed. It is REPLACED and not dropped: the paragraph above restates it verbatim through `PROMOTING AUTHORITIES` and changes exactly two things — the count, five to six, and the sixth axis appended with its content deferred to the requirement that already states it in full. Its removal is the whole object of this amendment, on Copilot finding `r4067955892` of review `5273796676`: a CLOSED list of five, in a specification whose third requirement mandates a sixth field for every derived-model family, cannot tell an implementer whether declaring that field is forbidden or owed — and the estate's one realized declaration already carries it as a sixth, at `contracts/domain-profiles/openxfactory-engineering.yaml`:415, top level and under no axis banner. Nothing the removed unit obliged is lost; the five axes it names are all five carried forward, in its own words and its own order.

#### Scenario: A descendant carries no mapping declaration
- **WHEN** a `<Domainx>Dox` descendant is created with no domain mapping declaration
- **THEN** it is an empty boundary under `domain-descendant-boundary`, because the declaration is the profile artifact that makes it a descendant rather than a directory

#### Scenario: The neutral layer hardcodes a domain's status words
- **WHEN** the domain-mapping core reads or writes a status vocabulary it did not receive from a declaration
- **THEN** the hardcoding is reported, and the vocabulary moves into the declaration of the domain it belongs to

#### Scenario: openxFactory's own vocabulary is treated as neutral
- **WHEN** `openxFactory`'s nine-word `Status:` taxonomy, its change/spec/delta nouns or its doc-health families are placed in the neutral layer rather than in the engineering descendant's declaration
- **THEN** the placement is refused under RULING C2, because a clinician using a descendant would then see the word "requirement"

#### Scenario: A declaration carries five axes and no derived-model boundary
- **WHEN** a descendant declares its artifact kinds, its lifecycle vocabulary, its acts and gates, its evidence classes and its promoting authorities, and declares a derived-model family with no truth store and no external enforcement point
- **THEN** the declaration is INCOMPLETE against this requirement's own axis list, and not merely against the requirement that states the sixth axis in full
- **AND** the omission is reported as a missing axis rather than read as a forbidden sixth, which is the reading a closed list of five left open
