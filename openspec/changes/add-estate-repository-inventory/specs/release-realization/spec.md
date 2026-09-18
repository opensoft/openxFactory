## MODIFIED Requirements

### Requirement: Code-surface declaration grammar is gated
An ACTIVE change proposal's `code_surface:` declaration SHALL open with a
DECLARED HEAD the ratified grammar admits — EITHER the single token `none`, OR a
list of one or more REPOSITORY IDENTIFIERS separated by a comma, by ` and `, or
by ` + `, the two being EXCLUSIVE alternatives and never mixed — and a
house validator SHALL REFUSE any active declaration whose head it cannot read,
naming the proposal's path and the text the declaration carries. A declaration
whose repositories cannot be told from its explanation is a declaration no
reader can act on, which is what the corpus shows.

THE DECLARATION IS A HEAD FOLLOWED BY AN OPTIONAL PROSE GLOSS, and the gate
SHALL judge the HEAD and never the gloss. That is the corpus's own form rather
than a rule invented at the gate: the house writes `code_surface: openxFactory —
`scripts/…` (NEW) …`, and a reader that judged the whole string would refuse
every declaration that explains itself. The gloss SHALL be introduced by a GLOSS
OPENER, and the opener set SHALL be the set the corpus already uses rather than
one the gate prefers: an em dash, an en dash, an opening parenthesis, a full
stop, a colon, or a semicolon. A head that runs into ordinary prose with no
opener — a possessive, an apposition, or a sentence continued by `, and …` — is
REFUSED, because there is then no point in the string at which the declaration
stops and the explanation starts, and every reader must guess a different one.

A REPOSITORY IDENTIFIER IS EITHER A BARE REPOSITORY NAME OR AN `<owner>/<name>`
ADDRESS, and BOTH SHALL BE ADMITTED because the corpus carries both. THE GRAMMAR
ARM SHALL JUDGE THE IDENTIFIER'S SHAPE AND SHALL NOT JUDGE ITS MEMBERSHIP, the
two being separate questions with separate remedies: a head the grammar refuses
is re-punctuated by its author, and a head naming a repository the estate does
not carry is either corrected or the repository is admitted. MEMBERSHIP SHALL BE
JUDGED, by the arm *A declared repository is judged for membership against the
estate inventory* defines, against the enumeration *The estate's repositories are
enumerated in a governed inventory* defines. THE BOUND THIS PARAGRAPH PREVIOUSLY
STATED IS LIFTED BY THE ACT THAT REMOVED ITS REASON AND BY NOTHING ELSE: it read
that membership was not judged "for the measured reason that this repository
defines no inventory of the estate's repositories to resolve against", and that a
gate resolving membership "against a place that does not exist would refuse every
declaration on the day it landed". The first clause stops being true at the
landing of the inventory. The second is measured FALSE against the corpus the
inventory is built from: 34 readable heads name SIX distinct identifiers, and the
candidate inventory carries every one of them, so the membership arm refuses
NOTHING on the day it lands. A bound stated with its reason is lifted by removing
the reason, never by outvoting the sentence that stated it.

**Removed from canon by add-estate-repository-inventory (2026-09-18):** `The
gate SHALL judge the identifier's SHAPE and SHALL NOT judge its MEMBERSHIP of
any inventory, for the measured reason that this repository defines no inventory
of the estate's repositories to resolve against — the nearest files are a
former-to-current TRANSFER map and a five-row domain-factory regression fixture,
neither of which enumerates the estate.`; `A gate that resolved membership
against a place that does not exist would refuse every declaration on the day it
landed.`; `Whether canon should define such an inventory is a separate act and
is named as a successor, not smuggled in here.` — all three state, or rest on,
the same fact: that this repository defines no inventory of the estate's
repositories. This packet's realization defines one, so the first unit's premise
is spent, the second's prediction is measured FALSE (34 readable heads name six
distinct identifiers and the candidate inventory carries all six, so the
membership arm refuses nothing on the day it lands), and the third's successor
is this change. NONE IS DROPPED WITHOUT REPLACEMENT: the paragraph above
replaces all three, keeps the shape rule the first unit states, names the arm
and the enumeration that now judge membership, and records the lifting as the
removal of a stated reason rather than as an overruling.

`none` IS THE EMPTY-SURFACE SENTINEL AND SHALL NEVER BE READ AS A REPOSITORY
IDENTIFIER. A head is EITHER the single token `none` and nothing else, OR a list
in which the token `none` appears nowhere — so a MIXED head such as
`none, openxFactory` SHALL be REFUSED rather than parsed as a two-member list.
The exclusivity is stated here rather than left to a reader's good sense because
the two readings differ in the one way that matters: parsed as a list, a mixed
head yields a NON-EMPTY derived repository set for a change that declared the
empty surface, contradicting the promoted meaning of `none` and the rule the next
requirement states for it. `none` is not a repository, so a declaration naming it
beside one is not a wide surface but a self-contradictory one, and the author
owes a correction rather than a reader a guess. The refusal SHALL hold wherever
in the list the token appears, position being no part of the contradiction.

A BLOCK THAT DECLARES `code_surface:` TWICE SHALL BE REFUSED RATHER THAN READ
FROM ITS FIRST HEAD. The declaration is a prose header, and a prose header's
repeat is joined into one value rather than refused as the duplicate key a
structured field's repeat would be — so a block declaring one repository and then
another would show a reviewer two declarations and authorize the first. One
declaration per block, and a repeat is a finding against that proposal.

A DECLARATION WRITTEN AS A YAML BLOCK SCALAR SHALL BE REFUSED BY NAME. `>-` and
`|` are YAML folding indicators, and `code_surface:` is a PROSE HEADER that no
YAML loader reads, so the indicator survives into the value and becomes the first
thing a reader sees where a repository name belongs. The corpus carries one such
declaration today. The refusal SHALL say what it is rather than merely reporting
an unreadable head, because the author who wrote those two characters was
reaching for a structure this field does not have.

ABSENCE IS THE PROMOTED DEFAULT AND SHALL NEVER BE A FINDING. *Realization axis
declaration* makes a proposal without the declarations a doc-only change
(`code_surface: none`, `target_release: implemented`) by default, so a proposal
that declares nothing declares the default. Only a PRESENT declaration is judged
— and a declaration present with no value SHALL be refused, because the author
wrote the key and the default is available by omitting it.

AN ARCHIVED PROPOSAL SHALL BE READ AND NEVER JUDGED. An archived packet's front
matter is frozen record — `record-immutability` and `govern-archived-record-edits`
put it beyond a plain fix — so the gate SHALL count what the archive carries and
report it, and SHALL refuse nothing there. A gate that demanded an edit nobody
may make would be a standing finding with no remedy, which is the defect this
estate disposes of rather than creates.

#### Scenario: An active proposal's head runs into prose
- **WHEN** an active change's `proposal.md` declares a `code_surface:` whose head is followed by ordinary prose with no gloss opener — a possessive, an apposition, or a sentence continued by `, and …` — and the register does not name it
- **THEN** the validator MUST fail, naming the proposal's path and the declaration text it carries
- **AND** the remedy belongs to the declaring packet, which re-punctuates its own declaration so the head ends where the explanation begins

#### Scenario: An active proposal declares the empty code surface
- **WHEN** an active change declares `code_surface: none`, with or without a prose gloss after a gloss opener
- **THEN** the validator passes, the gloss being explanation and not declaration

#### Scenario: An active proposal declares one repository and explains itself
- **WHEN** an active change declares a single repository identifier followed by a gloss opened by an em dash, an opening parenthesis or a full stop
- **THEN** the validator passes, and the declared repository set is that one identifier

#### Scenario: An active proposal declares several repositories
- **WHEN** an active change declares two or more repository identifiers separated by a comma, by ` and `, or by ` + `
- **THEN** the validator passes and the declared repository set is every identifier in the head
- **AND** an identifier spelled as an `<owner>/<name>` address is admitted on the same terms as a bare repository name, both spellings being ones the corpus carries

#### Scenario: A head mixes none with a repository identifier
- **WHEN** an active change's head carries both the token `none` and a repository identifier, in either order — `none, openxFactory` or `openxFactory and none`
- **THEN** the validator MUST refuse that proposal, naming the mixed head, rather than reading `none` as one member of a multi-repository list
- **AND** the derived repository set MUST NOT be computed for it, a head that declares the empty surface beside a named one being self-contradictory rather than wide
- **AND** the refusal holds wherever in the list the token appears, position being no part of the contradiction

#### Scenario: A declaration is written as a YAML block scalar
- **WHEN** an active change's declaration opens with a YAML folding indicator such as `>-` or `|`, the prose header carrying it into the value unread
- **THEN** the validator MUST refuse that proposal and MUST name the indicator as the defect, rather than reporting only that the head is unreadable

#### Scenario: A proposal declares the code surface twice
- **WHEN** an active change's `proposal.md` front matter carries two `code_surface:` header lines, the shared prose-header loader joining them into one value
- **THEN** the validator MUST refuse that proposal, naming it, rather than judging the first head and ignoring the second declaration

#### Scenario: A proposal declares no code surface
- **WHEN** an active change's `proposal.md` declares no `code_surface:` at all
- **THEN** the validator passes, the proposal having taken the promoted doc-only default

#### Scenario: A proposal declares the key with no value
- **WHEN** an active change's `proposal.md` carries a `code_surface:` header line whose value is empty
- **THEN** the validator MUST refuse that proposal, the promoted default being available by omitting the key

#### Scenario: An archived proposal carries an unreadable head
- **WHEN** the scan reaches a proposal under `openspec/changes/archive/` whose declaration the grammar does not admit
- **THEN** it MUST NOT be a finding, and the run reports how many such records the archive carries

## ADDED Requirements

### Requirement: The estate's repositories are enumerated in a governed inventory
openxFactory SHALL carry a machine-readable inventory of the estate's
repositories, ONE ROW PER REPOSITORY, and every row SHALL carry the repository's
`<owner>/<name>` address, its BARE NAME, its ROLE in the layer model, its
GOVERNANCE CLASS, and the ADMISSION EVIDENCE that puts it in the estate. The
file SHALL carry `schema_version` and `kind` like every other governed YAML in
this repository, and a house validator SHALL read it.

THE INVENTORY RECORDS AN ADMISSION TAKEN ELSEWHERE AND PERFORMS NONE, and that
is the answer to the authority question the successor was filed on: who admits a
repository to the estate. Nobody admits one BY WRITING A ROW. A repository joins
the estate when a governed tree NAMES it, and the row is the record of that
naming. So every row SHALL carry `admitted_by:` naming at least one NAMING SITE
and the kind of act it is, and the admissible kinds SHALL be exactly these five,
because they are exactly the ways this estate has ever named a repository:

- `gitlink`: a GOVERNED ESTATE REPOSITORY's `.gitmodules` carries the submodule,
  and the evidence SHALL NAME THE REPOSITORY THAT CARRIES IT. This is the
  estate's own act of admission and the widest class. THE AGGREGATION
  REPOSITORY IS THE WIDE CASE AND NOT THE ONLY ONE: the estate also places a
  repository as a NESTED DESCENDANT of a governed DomainxFactory rather than as
  an aggregation sibling, and a `gitlink` read as the aggregation's alone would
  leave every nested member admitted by nothing at all. Naming the carrier is
  what keeps the evidence checkable, a reader being unable to look in a tree the
  row does not name.
- `pin`: an openxFactory file under `contracts/` names the repository as the
  source of a commit-and-digest pin. This is openxFactory's act, for a product
  PINNED rather than governed.
- `workflow`: an openxFactory workflow dispatches into the repository, or
  checks it out, at a named ref.
- `root`: the aggregation repository ITSELF, which no `.gitmodules` can name
  because a superproject is not its own submodule, and which would otherwise be
  the one member of the estate no evidence admits.
- `change`: a RATIFIED change in this repository whose realization CREATES the
  repository. This kind exists because a code surface is FORWARD-LOOKING: it
  names where a change WILL write, so a repository the estate is creating is
  declared before any gitlink, pin or workflow can name it. A `change`-admitted
  row is PROVISIONAL, and SHALL say so.

A `change`-ADMITTED ROW SHALL NOT REMAIN PROVISIONAL FOREVER. When its change
ARCHIVES, one of the other four kinds is owed, because the repository the
realization created now exists and a governed tree can name it. THE GOVERNED
TREE THAT NAMES IT IS COMMONLY THE DOMAINxFACTORY THE REALIZATION NESTED IT
UNDER, which is the measured reason `gitlink` is not read as the aggregation's
alone: a realization that creates a repository and nests it would otherwise
discharge into no kind, and the provisional row it opened could never be closed.
A row still admitted only by an ARCHIVED change SHALL be a finding, on the same
terms as a row whose evidence has gone: the provisional admission outlived the
act that justified it.

THE RE-CHECK OF ADMISSION EVIDENCE IS BOUNDED BY WHERE THE EVIDENCE LIVES, and
the bound is STATED rather than left for a reader to discover when the validator
cannot do what the requirement says. FOUR of the five kinds name evidence inside
THIS repository's working tree — `pin` a file under `contracts/`, `workflow` a
file under `.github/workflows/`, `change` a directory under `openspec/changes/`,
and `root` a constant naming no file at all — so a row carrying one of them
SHALL be re-checked on EVERY run, DETERMINISTICALLY and with NO NETWORK CALL.
`gitlink` is the ONE kind whose evidence lives in ANOTHER repository's tree,
which an openxFactory checkout does not contain. Its re-check SHALL therefore be
an EXPLICITLY INVOKED mode taking the carrying repository's working tree as a
PATH INPUT, and a run given no such path SHALL REPORT its `gitlink` rows as NOT
RE-CHECKED, with their count, rather than passing them silently or failing them.
A validator that fetched the tree itself would make a required check depend on a
token and on read access to a private repository, which is the cost the derived
shape was refused for and which may not be readmitted at the reverse arm.

THE GOVERNANCE CLASS SAYS WHAT A ROW MEANS FOR A REPOSITORY THAT IS PINNED
RATHER THAN GOVERNED, which is the second half of the same authority question,
and it SHALL be one of three: `governed`, the estate authors its contents;
`pinned`, openxFactory consumes it at a commit and digest and authors none of
it; `external`, it is pinned and is NOT of this estate at all. The three are
kept distinct because a consumer that collapsed them would authorize a change
to a repository nobody here may change. An `external` row is carried so that
KNOWN-BUT-NOT-OURS is distinguishable from UNKNOWN, which is a distinction no
validator can draw from absence.

A BARE NAME SHALL RESOLVE THROUGH THE ROW WHOSE BARE NAME IT MATCHES, and the
bare names SHALL BE UNIQUE ACROSS THE INVENTORY. The corpus writes both
spellings, so a reader must resolve both; two rows sharing a bare name would make
one spelling ambiguous, and the validator SHALL REFUSE THE INVENTORY rather than
pick a row, because picking is how an authorization lands in the wrong
repository.

A FORMER ADDRESS SHALL BE RESOLVED THROUGH
`contracts/policies/repository-identity.yaml` AND NEVER THROUGH A PROVIDER
REDIRECT. That file already states the reason in its own header: a redirect is a
grace period that stops the moment the former owner reuses the name, and
governed content whose correctness depends on nobody creating a repository is
not content a contract may rest on. The inventory SHALL carry CURRENT addresses
only, and the transfer map SHALL remain the one place a former address is read.

THE INVENTORY IS NOT A FILE UNDER `contracts/`, AND THE REASON IS MEASURED
RATHER THAN PREFERRED. A file under `contracts/` is a bundle surface whose change
owes a manifest entry, a recomputed digest and a bundle cut, and the fact this
inventory tracks moves often: the aggregation repository's `.gitmodules` took
NINETEEN commits between 2026-07-01 and 2026-09-12, almost all of them an
admission, a retirement or an owner transfer, which is one inventory-moving act
every four days. An enumeration that could not be corrected without cutting a
contract release would be corrected late or not at all, which is the reason
`scripts/code-surface-register.yaml` states for its own placement and the reason
this file takes the same one.

#### Scenario: A repository is admitted to the estate by a gitlink
- **WHEN** a governed estate repository's `.gitmodules` carries a submodule for a repository — the aggregation repository's in the wide case, a governed DomainxFactory's where the estate nested the repository rather than sibling-linking it
- **THEN** the inventory SHALL carry a row for it whose `admitted_by:` names that gitlink AND the repository that carries it
- **AND** the row's governance class states whether the estate authors its contents or consumes it at a pin

#### Scenario: A neutral product is pinned but is no submodule
- **WHEN** an openxFactory file under `contracts/` names a repository as the source of a commit-and-digest pin, and no `.gitmodules` entry names it
- **THEN** the inventory SHALL carry a row for it admitted by that pin, with governance class `pinned`
- **AND** the absence of a gitlink is not an absence of membership, the pin being an admission in its own right

#### Scenario: A repository a ratified change is creating
- **WHEN** a RATIFIED active change declares a code surface in a repository its own realization creates, and no gitlink in any governed estate repository, no pin and no workflow names it yet
- **THEN** the inventory MAY carry a PROVISIONAL row admitted by that change, marked as provisional and naming the change id
- **AND** once that change ARCHIVES, a row still admitted only by it MUST be reported as a finding, the repository being nameable by a governed tree from that point — commonly by the gitlink of the DomainxFactory the realization nested it under

#### Scenario: The aggregation repository itself
- **WHEN** the inventory enumerates the estate
- **THEN** it SHALL carry a row for the aggregation repository, admitted by `root`
- **AND** the row exists precisely because a superproject is not its own submodule, so no gitlink can admit it

#### Scenario: Two rows share a bare name
- **WHEN** the inventory carries two rows whose bare repository names are the same
- **THEN** the validator MUST REFUSE the inventory, naming both rows and the shared name
- **AND** it MUST NOT resolve the bare spelling to either row, an ambiguous resolution being how an authorization lands in the wrong repository

#### Scenario: A row's in-tree admission evidence names nothing
- **WHEN** a row's `admitted_by:` names a pin, a workflow or a change that THIS repository's own working tree does not carry
- **THEN** the validator MUST report a finding against that row, on every run, deterministically and with no network call, the evidence being a file in the tree it is already reading
- **AND** the remedy is to correct the evidence or to remove the row, never to widen what counts as evidence

#### Scenario: A gitlink row is re-checked only against a supplied tree
- **WHEN** the run reaches a row admitted by a `gitlink` and no working tree was supplied for the repository the row names as the carrier
- **THEN** the validator MUST report that row as NOT RE-CHECKED and MUST count it, and MUST NOT pass it silently, MUST NOT fail it, and MUST NOT fetch the carrying repository
- **AND** when that working tree IS supplied as a path input, the row's `.gitmodules` evidence MUST be re-checked in it and its absence MUST be a finding against the row

#### Scenario: The inventory carries a former address
- **WHEN** a row's `repository:` is an address `contracts/policies/repository-identity.yaml` records as FORMER
- **THEN** the validator MUST report a finding against that row, naming the current address the transfer map resolves
- **AND** the remedy is the respelling, the inventory carrying current addresses only

### Requirement: A declared repository is judged for membership against the estate inventory
A house validator SHALL REFUSE an ACTIVE change proposal whose `code_surface:`
DECLARED HEAD names a repository identifier the estate inventory does not carry,
naming the proposal's path, the identifier, and the inventory the identifier was
resolved against. THE ARM FAILS CLOSED: an identifier the inventory does not
carry is REFUSED and is never admitted on the strength of its shape, because the
whole content of this arm is the difference between a name that resolves and a
name that merely looks like one.

THE DEFECT THIS CLOSES IS NAMED AND IS STANDING. The grammar arm judges shape
alone, so `openxFactorie` passes it and so does a repository that is no part of
this estate. The class is not hypothetical: measured at the authoring,
`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` names
`opensoft/LegalxFactory`, which is a 404 on the provider and appears in no
`.gitmodules` and in no pin, and it names two more repositories at addresses
that live only through a provider redirect. A plausible misspelling of a real
repository is already written in this tree.

RESOLUTION IS BY THE ROW AND NEVER BY THE PROVIDER. An `<owner>/<name>` head
resolves against a row's address; a BARE head resolves against a row's unique
bare name; and NEITHER SHALL be resolved by asking GitHub, because a gate whose
verdict depends on a network call gives a different answer on a bad afternoon
than it gave at the ratification, and because the redirect that would answer it
is the grace period the transfer map exists to refuse.

A HEAD NAMING A FORMER ADDRESS SHALL BE REPORTED AND NOT REFUSED. The transfer
map resolves it to a current row, so the identifier is INTERPRETABLE and the
estate's membership is not in doubt; what is owed is a respelling, and the
finding SHALL name the current address so the author need not look it up. This
is the one place the arm reports rather than refuses, and the reason is that
refusing an interpretable name teaches an author nothing the finding does not.

A HEAD NAMING AN `external` ROW SHALL BE REFUSED, naming the governance class.
A code surface is the set of repositories whose runtime artifacts a change
CHANGES, and a change cannot change a repository this estate does not author.
The row exists so the refusal can say WHICH of the two defects it is.

A DECLARATION THE CLOSED REGISTER NAMES HAS NO READABLE HEAD, so membership
SHALL NOT be judged for it and the arm SHALL NOT FALL BACK to the whole
declaration, to the gloss, or to an empty set. The register suspends the
grammar's refusal for one declaration and supplies no repository set, and an arm
that invented one would authorize on text no reader can parse.

AN INVENTORY ROW THAT NO NAMING SITE NAMES SHALL BE A FINDING, and the asymmetry
is deliberate and is the register's own. An identifier the inventory does not
carry FAILS, because somebody declared a surface in a repository the estate does
not know. A row that nothing names REPORTS, because the row outlived the
admission it records and the remedy is to retire it in the pull request that
made it stale. Silently tolerating the second is how an enumeration rots into a
list of names. THE ARM IS BOUND BY WHERE THE EVIDENCE LIVES, on the terms the
enumeration requirement states: it re-checks the in-tree kinds on every run, and
it reports a `gitlink` row whose carrying tree was not supplied as NOT RE-CHECKED
rather than as named or as stale, because a run that has not looked may not
report either verdict.

AN ARCHIVED PROPOSAL SHALL BE READ AND NEVER JUDGED, on the same terms and for
the same reason the grammar arm is bound by: an archived packet's front matter is
frozen record, and a gate demanding an edit nobody may make is a standing finding
with no remedy.

#### Scenario: A head names a repository the inventory carries
- **WHEN** an active change's declared head names an identifier that resolves to an inventory row whose governance class is `governed` or `pinned`
- **THEN** the validator passes for that identifier

#### Scenario: A head names a plausible misspelling
- **WHEN** an active change's declared head names an identifier the inventory does not carry, such as a one-letter variant of a real repository
- **THEN** the validator MUST fail, naming the proposal's path, the identifier, and the inventory it was resolved against
- **AND** it MUST NOT admit the identifier on the strength of its shape, and MUST NOT resolve it by asking the provider

#### Scenario: A head is written as a bare repository name
- **WHEN** an active change's declared head names a bare repository name that matches exactly one row's bare name
- **THEN** the validator resolves it to that row and passes, both spellings being ones the corpus carries

#### Scenario: A head names an external repository
- **WHEN** an active change's declared head names an identifier that resolves to a row whose governance class is `external`
- **THEN** the validator MUST fail, naming the governance class rather than reporting the identifier as unknown
- **AND** the distinction is the point of carrying the row at all

#### Scenario: A head names a former address
- **WHEN** an active change's declared head names an address the transfer map records as FORMER, which resolves to a current inventory row
- **THEN** the validator MUST report a finding and MUST NOT refuse the proposal, the identifier being interpretable
- **AND** the finding names the current address, so the remedy is a respelling the author can take without a lookup

#### Scenario: An inventory row nothing names
- **WHEN** the run reaches an inventory row whose in-tree `admitted_by:` evidence no longer appears in this repository's own working tree
- **THEN** it MUST be reported as a finding against the row, and MUST NOT fail the declaration arm
- **AND** a row admitted by a `gitlink` whose carrying tree was not supplied MUST be reported as NOT RE-CHECKED instead, the evidence living in a tree this checkout does not contain
- **AND** the remedy is to retire the row in the pull request that made it stale

#### Scenario: A registered declaration reaches the membership arm
- **WHEN** the run reaches an active proposal the closed code-surface register names, whose head no reader can parse
- **THEN** membership MUST NOT be judged for that proposal
- **AND** the arm MUST NOT fall back to the whole declaration, to the gloss, or to an empty set

#### Scenario: A proposal declares the empty surface or declares nothing
- **WHEN** an active change declares `code_surface: none`, or declares no `code_surface:` at all and so takes the promoted doc-only default
- **THEN** there is no identifier to resolve and the membership arm passes

#### Scenario: An archived proposal names a repository the inventory does not carry
- **WHEN** the scan reaches a proposal under `openspec/changes/archive/` whose head names an identifier no inventory row carries
- **THEN** it MUST NOT be a finding, the archived record being frozen
- **AND** the run reports how many such records the archive carries
