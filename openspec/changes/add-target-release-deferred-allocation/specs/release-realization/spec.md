# release-realization Specification

## MODIFIED Requirements

### Requirement: Realization axis declaration
Every OpenSpec change proposal SHALL declare `code_surface:` — `none` or the
repositories whose runtime artifacts it changes — and `target_release:` —
`implemented` (the affected repositories' main lines), a named release defined in
the aggregation repository, or `deferred-allocation` — a contract bundle this
change realizes into whose NUMBER this estate's own versioning policy allocates AT
THE CUT, so that no number exists to be named at proposal time. A proposal without
the declarations is a doc-only
change (`code_surface: none`, `target_release: implemented`) by default. A
proposal MAY ALSO declare an OPTIONAL sibling field `scope_globs:` carrying a
machine-readable path scope (defined in the "Structured path-scope declaration"
requirement); its ABSENCE is the pre-existing default and leaves the change
exactly as it is today — a proposal is never required to declare `scope_globs`,
and its absence never means "all paths."

**`deferred-allocation` IS A THIRD VALUE AND NEVER A THIRD DEFAULT.** It SHALL be
declared only by a change whose `code_surface:` is non-empty AND whose realization
lands in a contract bundle; a change that cuts no bundle has `implemented`
available and the default sentence above already says so. It is a TEMPORARY
declaration by construction — the number it stands in for comes into existence at
the cut — so it SHALL be resolved to the literal release identifier the cut
allocated, or to `implemented` where the realization ended up cutting no bundle,
and the requirement *Realization axis vocabulary is gated* governs when.

#### Scenario: A doc-only change is proposed
- **WHEN** a change alters only governance documents, schemas-as-documents, or contract prose
- **THEN** its code_surface is `none` and it archives when its artifacts land, as before
- **AND** it declares no `scope_globs` and is unaffected by the structured-scope substrate

#### Scenario: A code-surface change is proposed
- **WHEN** a change alters scripts, workflows, services, or other runtime artifacts
- **THEN** its proposal MUST declare the affected repositories as code_surface and its target release

#### Scenario: A change declares no structured scope
- **WHEN** a change omits `scope_globs` entirely
- **THEN** it validates and archives exactly as before, and it is simply not provenance-eligible until an author adds `scope_globs` — its absence is never interpreted as an unbounded or repository-wide scope

#### Scenario: A change realizes into a bundle whose number is not yet allocatable
- **WHEN** a change's realization lands in a contract bundle and `docs/contract-versioning-policy.md` § Bundle Realization Order allocates that bundle's version at the cut, so no number exists to name
- **THEN** its proposal declares `target_release: deferred-allocation`, and naming a number instead would reserve one the policy allocates late

#### Scenario: A doc-only change reaches for the deferred value
- **WHEN** a change that cuts no contract bundle declares `target_release: deferred-allocation`
- **THEN** the declaration MUST NOT stand, `implemented` being the value for a realization that lands on the affected repositories' main lines

### Requirement: Realization axis vocabulary is gated
An ACTIVE change proposal's `target_release:` declaration SHALL carry a value
the ratified vocabulary admits — `implemented`, a release identifier that
resolves to a release this estate defines, or `deferred-allocation` — and a
house validator SHALL REFUSE
any other value on an active proposal, naming the proposal's path and the value
it carries. A vocabulary stated in prose and read by nobody is a vocabulary the
next proposal diverges from, which is what the corpus shows.

THE DECLARATION IS A VALUE TOKEN FOLLOWED BY AN OPTIONAL PROSE GLOSS, and the
gate SHALL judge the TOKEN and never the gloss. That is the corpus's own form
rather than a rule invented at the gate: the house writes `target_release:
implemented (the openxFactory main line). No contract bundle is cut …`, and a
reader that judged the whole string would refuse every declaration that explains
itself. The token is the first whitespace-delimited word of the declaration.

A BLOCK THAT DECLARES `target_release:` TWICE SHALL BE REFUSED RATHER THAN READ
FROM ITS FIRST TOKEN. The declaration is a prose header, and a prose header's
repeat is joined into one value rather than refused as the duplicate key a
structured field's repeat would be — so a block declaring `implemented` and then
`none` would show a reviewer two declarations and authorize the first. One
declaration per block, and a repeat is a finding against that proposal.

ABSENCE IS THE PROMOTED DEFAULT AND SHALL NEVER BE A FINDING. *Realization axis
declaration* makes a proposal without the declarations a doc-only change
(`code_surface: none`, `target_release: implemented`) by default, so a proposal
that declares nothing declares the default. Only a PRESENT declaration is
judged — and a declaration present with no value SHALL be refused, because the
author wrote the key and the default is available by omitting it.

A RELEASE IDENTIFIER SHALL RESOLVE AGAINST THE REGISTRY THE SCANNED TREE
DEFINES, AND WHERE THE TREE DEFINES NONE THE SHAPE SHALL BE THE WHOLE TEST AND
THE RUN SHALL SAY SO. Where the tree carries a release registry, a name that
resolves to nothing in it is NOT a named release and SHALL be refused. Where
the tree carries no registry at all — every consuming repository that defines
no releases of its own — refusing every release name would make the gate
unusable outside the repository that defines them, so the identifier's SHAPE is
accepted on its own; that is a WEAKER judgment and SHALL NOT be silent, so the
run SHALL report that it judged on shape alone. The identifier's shape SHALL be
the shape this estate DEFINES for a release tag rather than one the gate
invents, so the gate cannot refuse a release the estate's own inventory admits.

AN ARCHIVED PROPOSAL SHALL BE READ AND NEVER JUDGED. An archived packet's front
matter is frozen record — `record-immutability` and `govern-archived-record-edits`
put it beyond a plain fix — so the gate SHALL count what the archive carries and
report it, and SHALL refuse nothing there. A gate that demanded an edit nobody
may make would be a standing finding with no remedy, which is the defect this
estate disposes of rather than creates.

`deferred-allocation` NAMES A TARGET THAT EXISTS AND A NUMBER THAT DOES NOT, AND
THE GATE SHALL ADMIT IT ON AN ACTIVE PROPOSAL. `docs/contract-versioning-policy.md`
§ Bundle Realization Order opens *"Contract-bundle realization is serialized and
allocates versions late"* and allocates the next available version at step 1 of the
cut, so an author who named a number at proposal time would reserve one that policy
allocates at the cut. Without a third value such an author must depart from one
ratified rule in order to obey another, which is what the corpus measured at the
gate's landing showed twelve times. The value SHALL be available only to a change
whose `code_surface:` is non-empty and whose realization lands in a contract
bundle: a change that cuts no bundle has `implemented`, and a value available to
everybody would become the second `none`.

THE DECLARATION IS TEMPORARY BY CONSTRUCTION AND SHALL BE RESOLVED BEFORE THE
PACKET ARCHIVES. The number `deferred-allocation` stands in for comes into
existence at the cut, so a change SHALL NOT archive while it still declares it:
the archiving act SHALL first resolve the declaration to the literal release
identifier the cut allocated, or — where the realization ended up cutting no
bundle — to `implemented`. An archived packet is frozen record, and a record that
declares a number nobody ever allocated is the `none` defect wearing a better
name: permanent, unresolvable, and beyond the reach of any later fix.

THE RESOLVING EDIT SHALL NAME THE CUT IT OBSERVED, never merely swap a token. The
pull request that replaces `deferred-allocation` with a literal SHALL name the
bundle version and the release surface that carries it, so the number is OBSERVED
rather than predicted — the same direction § Bundle Realization Order takes at
steps 4 and 5, where the tag follows the landing and never precedes it. A bare
token swap cites nothing and is indistinguishable from the reservation the policy
forbids.

THE ARCHIVE SHALL BE REPORTED AND STILL NEVER JUDGED. The paragraph above binds
the ARCHIVING ACT and not the archived record: a record already carrying
`deferred-allocation` SHALL NOT be refused by the gate, the never-judged rule
above admitting no exception for this value, and demanding an edit to a frozen
record would be a standing finding with no remedy. The run SHALL instead COUNT
and REPORT how many archived records carry an unresolved `deferred-allocation`,
so the number is visible to a reader without being a refusal to anyone.

A REGISTER ENTRY OF CLASS `deferred-allocation` RETIRES ON ITS PACKET'S OWN
CORRECTION AND NOT ON THIS ADMISSION. Admitting the value does not by itself make
a standing entry's declaration lawful — the entries name the tokens their authors
actually wrote — so each retires when its owning packet corrects its declaration
to the admitted token, and the entry SHALL be deleted in that same pull request,
which is what the stale-entry refusal below already forces.

THE STANDING DIVERGENCE SHALL BE NAMED IN A CLOSED REGISTER RATHER THAN
FORGIVEN IN CODE. Where the corpus at the gate's landing carries declarations
outside the vocabulary that are not corrected by the same act, each SHALL be
named in a register carried beside the validator, with the value token as it
stands, the class of divergence, the reason, a citation, and the event that
retires the entry. The register SHALL be CLOSED: an entry may be REMOVED when
its declaration is corrected or its packet archives, and admitting a NEW value
to the vocabulary SHALL be a change to this specification rather than an
addition to the register. CLOSURE SHALL BE ENFORCED AND NOT MERELY DECLARED:
the validator SHALL carry the baseline of entries the register holds when the
gate lands and SHALL REFUSE any entry that baseline does not carry, so an
exception cannot be granted by appending a line to a data file — granting one
takes an edit where the refusal itself is written, and the diff shows the act
for what it is. A registered declaration is REPORTED and not refused;
every declaration the register does not name is judged from the day the gate
lands, so the gate is a ratchet and the divergence cannot grow.

THE TWO REFUSALS ARE ASYMMETRIC AND SHALL STAY SO. An off-vocabulary
declaration the register does not name is a statement about the PROPOSAL and
the run SHALL fail; a register entry that matches nothing on a whole-corpus scan
is a statement about the REGISTER — the exception outlived the condition it was
granted for — and the run SHALL refuse with a distinct status until the entry is
deleted. Silently tolerating the second is how an exception list rots into a
blanket, and refusing makes the correction, or the archive, the event that
forces the re-examination.

#### Scenario: An active proposal declares a value outside the vocabulary
- **WHEN** an active change's `proposal.md` declares a `target_release:` whose value token is neither `implemented` nor a release identifier that resolves, and the register does not name it
- **THEN** the validator MUST fail, naming the proposal's path and the value token it carries
- **AND** the remedy belongs to the declaring packet, which corrects its own declaration

#### Scenario: An active proposal declares the implemented target
- **WHEN** an active change declares `target_release: implemented`, with or without a prose gloss after the token
- **THEN** the validator passes, the gloss being explanation and not declaration

#### Scenario: An active proposal names a release the estate defines
- **WHEN** an active change declares a release identifier and the scanned tree's release registry carries that release
- **THEN** the validator passes
- **AND** where that tree HAS a registry, a release-shaped name the registry does not carry MUST be refused, because a name that resolves to nothing is not a named release

#### Scenario: The scanned tree defines no release registry at all
- **WHEN** the tree carries no release registry, so no name in it could resolve, and an active change declares a release-shaped identifier
- **THEN** the identifier's shape MUST be the whole test and the declaration passes, because refusing every release name in a tree that cannot define one would make the gate unusable outside the repository that defines them
- **AND** the run MUST report that it judged on shape alone, the weaker judgment never being silent

#### Scenario: An archived proposal carries an off-vocabulary value
- **WHEN** the scan reaches a proposal under `openspec/changes/archive/` whose declaration is outside the vocabulary
- **THEN** it MUST NOT be a finding, and the run reports how many such records the archive carries

#### Scenario: A standing declaration is named by the register
- **WHEN** an active declaration outside the vocabulary is named by a register entry carrying its current value token, its class, its reason, its citation and its retirement event
- **THEN** the validator reports it as registered and does not refuse it

#### Scenario: A proposal declares the target release twice
- **WHEN** an active change's `proposal.md` front matter carries two `target_release:` header lines, the shared prose-header loader joining them into one value
- **THEN** the validator MUST refuse that proposal, naming it, rather than judging the first token and ignoring the second declaration

#### Scenario: An entry is appended to the closed register
- **WHEN** a register entry names a change and value token the validator's recorded closed baseline does not carry
- **THEN** the run MUST refuse, because the register is removable and never addable
- **AND** granting the exception takes an edit to the baseline in the same pull request, where the diff shows it

#### Scenario: A register entry matches nothing
- **WHEN** a whole-corpus scan finds a register entry whose change has archived, or whose declaration has been corrected so the value token no longer matches
- **THEN** the run MUST refuse with a status distinct from an off-vocabulary failure, naming the entry
- **AND** the remedy is to delete the entry in the same pull request that made it stale

#### Scenario: A proposal declares no target release
- **WHEN** an active change's `proposal.md` declares no `target_release:` at all
- **THEN** the validator passes, the proposal having taken the promoted doc-only default

#### Scenario: An active proposal declares a deferred bundle allocation
- **WHEN** an active change whose code surface is non-empty realizes into a contract bundle whose version the versioning policy allocates at the cut, and its proposal declares `target_release: deferred-allocation`
- **THEN** the validator passes, the value being the third the ratified vocabulary admits
- **AND** naming a literal release identifier instead MUST NOT be required of it, that being the reservation `docs/contract-versioning-policy.md` § Bundle Realization Order forbids

#### Scenario: A change tries to archive while its target release is deferred
- **WHEN** a change declaring `target_release: deferred-allocation` reaches its archive gate with the declaration unresolved
- **THEN** it MUST NOT archive, the archiving act first resolving the declaration to the literal release the cut allocated, or to `implemented` where no bundle was cut
- **AND** a record carrying an unresolved deferred allocation MUST NOT be created, the archive being frozen and the number never becoming knowable afterwards

#### Scenario: The resolving pull request swaps the token and cites nothing
- **WHEN** a pull request replaces `deferred-allocation` with a literal release identifier and names neither the bundle version it observed nor the release surface carrying it
- **THEN** the resolution MUST NOT be treated as complete, an uncited number being indistinguishable from the reservation the versioning policy forbids

#### Scenario: An archived record still carries the deferred value
- **WHEN** the scan reaches a proposal under `openspec/changes/archive/` whose declaration is `deferred-allocation`
- **THEN** it MUST NOT be a finding, the never-judged rule admitting no exception for this value
- **AND** the run MUST report how many such records the archive carries, the breach being visible without being refused to anyone

#### Scenario: A doc-only change declares the deferred value
- **WHEN** an active change whose realization cuts no contract bundle declares `target_release: deferred-allocation`
- **THEN** the declaration MUST NOT stand, the value being available only where a bundle is cut and `implemented` being what such a change means

#### Scenario: The admission does not retire a standing register entry by itself
- **WHEN** canon admits `deferred-allocation` and a register entry of class `deferred-allocation` still names the token its packet actually declares
- **THEN** the entry MUST remain live until that packet corrects its own declaration, the admission having changed no byte of the packet's front matter
- **AND** the entry MUST be deleted in the same pull request that makes the correction, the stale-entry refusal being what forces it
