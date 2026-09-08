# lifecycle-notebook-projection Delta: the hosting identity becomes a configured value

ONE `## MODIFIED Requirements` BLOCK, ONE REQUIREMENT, AND EVERY PROMOTED UNIT
CARRIED. The four promoted body paragraphs are byte-identical to canon at
`543d47a9`, all five promoted scenario titles are present, and every promoted
scenario bullet is carried verbatim EXCEPT ONE — the third bullet of *An
operating party declares the company account*, which is the single line of the
promoted corpus that states a real account address as a normative example. It is
REPLACED, not dropped: the same claim survives in role terms.

WHY THE RESERVED `Removed from canon by` MARKER IS NOT USED, AND THIS PARAGRAPH
IS ITS SUBSTITUTE. `document-lifecycle`'s marker names the retired unit as a
code span carrying that unit's exact text — which here would reprint the address
this change exists to remove, inside the delta that removes it, in the same
public tree. So the marker is deliberately absent and the divergence is declared
in prose instead. The measured consequence is stated rather than hidden: the
`modified-block-currency` carriage ledger will report ONE `info` finding against
this block for the one bullet it does not carry, which is exactly what that arm
is for — it says in its own rule text that it cannot distinguish a deliberate
rewording from stale text and does not claim to. The gate-bearing
scenario-title arm reads zero, no title being dropped.

NOTHING ELSE IN THIS CAPABILITY IS TOUCHED. The custody requirement, the
share-out requirement, the migration requirement and every other promoted
requirement keep their text; the two ADDED body paragraphs and two ADDED
scenarios below are additions to this one requirement, not a second delta
wearing a MODIFIED heading.

## MODIFIED Requirements

### Requirement: The projection's hosting identity is declared at install
An xFactory install SHALL declare which Google identity hosts its NotebookLM projection, as an intake fact of standing that install up rather than an incidental consequence of whoever authenticated the `nlm` CLI first. The declaration SHALL name exactly one of two cases: OPERATOR-HOSTED, a company-owned account belonging to the operating party, or SELF-HOSTED, an individual installer's own personal account. Both cases are legitimate; the second is not a degraded form of the first.

The declared identity SHALL be a Google USER account. This is a platform constraint, not a preference: NotebookLM exposes no API and a provider service account cannot drive its consumer web UI, so no service-principal identity can host a projection at all.

An operator-hosted declaration SHALL name a Google Workspace user account in a domain the operating party controls, and SHALL NOT name a consumer account merely designated as the company's. A consumer account carries a personal recovery path back to one individual, no administrative console, and no enforceable organizational policy — it would be the operator-hosted case wearing the self-hosted case's risk.

An install that declares NOTHING is NONCONFORMING with this requirement — a transition state, not a third case. Every install predating this requirement is in it, so the sync SHALL NOT break on it: it falls back to the CLI's default profile, which is today's behavior. What it SHALL NOT do is present that install as governed. The projection SHALL be reported as carrying no declared hosting identity, and the undeclared state SHALL be reported as unmet rather than as a legitimate configuration, so an implementation and a validator agree about what is expected of it.

The declaration's LOCATION SHALL be resolved from configuration, and any instance of this record committed to this repository SHALL be a SYNTHETIC example that names no live identity — not the operating party's account, not the account a completed migration came from, and not one roster user or granting actor. A hosting record is not prose about an account: its `account`, its `migration.from_account` and its roster rows are the values an implementation compares against the identity a CLI profile is signed in as, which is why redacting them in place is not available and why the live record and the shipped example must be two different files rather than one file read two ways.

A live declaration resolved from configuration SHALL remain subject to every rule of this requirement, and SHALL be validated by the same validator invoked against the resolved path, so that moving the record out of this repository moves WHERE it is checked and never WHETHER it is checked. Where configuration resolves to the committed synthetic example, an implementation SHALL refuse the run rather than bind to it: a fixture is no install's declaration, and binding to one would write a governed projection into an account nobody declared — the exact failure this requirement exists to retire.

#### Scenario: An operating party declares the company account
- **WHEN** an install's intake declares operator-hosted and names a Google Workspace user account in the operating party's own domain
- **THEN** the declaration is valid, and every book, alias and session notebook of that install is created under the named account
- **AND** the operating party's own install is such a declaration, naming the CONFIGURED HOSTING IDENTITY it resolves at run time rather than an address written into this repository

#### Scenario: An individual installer keeps their own books
- **WHEN** a person installs the system for themselves and declares self-hosted against their own personal Google account
- **THEN** the declaration is valid and complete, no company account is implied, and no share-approval governance obligation attaches

#### Scenario: A consumer account is offered as the company account
- **WHEN** an operator-hosted declaration names a consumer Google account rather than a Workspace user in a controlled domain
- **THEN** the declaration is refused, naming the missing administrative control rather than the account's label

#### Scenario: A service account is offered as the hosting identity
- **WHEN** a declaration names a provider service account or any non-user principal
- **THEN** the declaration is refused on the platform constraint: NotebookLM has no API and the identity could never drive the projection

#### Scenario: An install has not declared yet
- **WHEN** no hosting identity is declared for an install
- **THEN** the sync runs under the CLI's default profile as it does today, rather than breaking
- **AND** the install is reported as NOT MEETING this requirement — a transition state, never a third legitimate case

#### Scenario: The committed example carries no real identity
- **WHEN** this repository ships an instance of the hosting record
- **THEN** every identity-bearing value in it is synthetic — the hosting account, the account a completed migration names, each roster user, and the actors that grant and designate
- **AND** a reader or a validator can check the record's SHAPE against that instance without learning any live address

#### Scenario: The live declaration resolves from configuration
- **WHEN** an implementation needs the install's own hosting declaration
- **THEN** it resolves the declaration's path from configuration rather than from a fixed path in this repository, and it validates what it finds against this requirement
- **AND** where configuration names nothing, the install is UNDECLARED — the transition state this requirement already defines — rather than bound to the shipped example
- **AND** where configuration resolves to the shipped example, the run is REFUSED rather than bound

