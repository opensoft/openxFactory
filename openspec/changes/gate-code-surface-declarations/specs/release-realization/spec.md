# release-realization Specification Delta

This delta is ALL-ADDED, and that is a MEASURED CHOICE rather than a style. The
divergence it governs sits in the promoted requirement *Realization axis
declaration*, and an active ratified change — `add-structured-scope-substrate` —
already holds a `## MODIFIED Requirements` block over that exact title, restating
its two-halved sentence verbatim and adding `scope_globs:` beside it. A second
MODIFIED block over the same title would have to be declared relative to that
change's outcome under *Ordered deltas and branch vocabulary*, would have to
restate that change's text as its pre-text, and would inherit that requirement's
archive-order hold. An ADDED requirement over a NOVEL title owes none of it,
restates no promoted text, drops none, and therefore owes no `Modified over`,
`Removed from canon by` or `Merged into` marker. The sibling packet
`gate-realization-axis-vocabulary` took the same shape for the OTHER half of the
same sentence and for the same reason, and this delta writes titles neither it
nor any other active change carries.

**NOTHING PROMOTED IS CHANGED.** *Realization axis declaration* keeps its
`code_surface:` half exactly as ratified — `none` or the repositories whose
runtime artifacts the change changes — and this delta neither widens it, narrows
it, nor reads a third value into it. What it adds is the thing that half has
never had: a reader that can tell which repositories a declaration actually
declares, and that refuses a declaration from which no reader could tell.
*Realization archive gate* is untouched; the archive path is still decided by
whether the code surface is empty.

**IT DOES NOT CONTRADICT THE OTHER ACTIVE DELTAS ON THIS CAPABILITY, AND THE
RELATION TO EACH IS STATED RATHER THAN ASSUMED.**
`add-sequenced-after-substrate` ADDS *Strict loading of the realization-axis
front-matter block*, which reaches "every STRUCTURED field" of the block —
`scope_globs:` and `sequenced_after:`. `code_surface:` is a PROSE HEADER of the
same block and not a structured field, so these requirements are neither that
one's realization nor an amendment to it; they CONSUME the loader that rule
produced, so a document the strict loader refuses is refused here too, reported
as a finding against that document rather than crashing the run.
`add-structured-scope-substrate` ADDS *Structured path-scope declaration*, whose
own sentence requires that "every repository key present in `scope_globs` SHALL
also be named in `code_surface`". That requirement states the obligation and
leaves OPEN what "named in `code_surface`" means; the second requirement below
answers exactly that question and constrains no other part of it. A shipped
reader that answers it by splitting the whole declaration — gloss included —
into words is the defect measured in this packet's `design.md` D4, and the
answer below is a tightening of a rule that requirement already states, never a
substitution for it.

**THE GRAMMAR BELOW IS THE CORPUS'S OWN FORM, DERIVED AND NOT INVENTED.**
Measured over the 45 active declarations this repository carries: 38 of them
already open with a repository identifier — or with `none` — and then hand off to
a prose gloss through one of exactly three openers (an opening parenthesis, an em
dash, or a full stop). The grammar states what those 38 already do. The other
seven are the population the register names.

## ADDED Requirements

### Requirement: Code-surface declaration grammar is gated
An ACTIVE change proposal's `code_surface:` declaration SHALL open with a
DECLARED HEAD the ratified grammar admits — the single word `none`, or one or
more REPOSITORY IDENTIFIERS separated by a comma, by ` and `, or by ` + ` — and a
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
ADDRESS, and BOTH SHALL BE ADMITTED because the corpus carries both. The gate
SHALL judge the identifier's SHAPE and SHALL NOT judge its MEMBERSHIP of any
inventory, for the measured reason that this repository defines no inventory of
the estate's repositories to resolve against — the nearest files are a
former-to-current TRANSFER map and a five-row domain-factory regression fixture,
neither of which enumerates the estate. A gate that resolved membership against a
place that does not exist would refuse every declaration on the day it landed.
Whether canon should define such an inventory is a separate act and is named as a
successor, not smuggled in here.

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

### Requirement: The declared repository set is derived from the head and never from the gloss
A consumer deriving a repository SET from a `code_surface:` declaration SHALL
derive it from the DECLARED HEAD alone, and SHALL NOT derive it from the prose
gloss. A declaration's gloss is where an author explains the
surface — naming the repositories the change does NOT touch, the repository a
companion change will touch, and the repository a pin points at — so a derivation
that reads the gloss returns repositories the author expressly did not declare a
surface for, and any authorization resting on that set is wider than the
declaration a ratification read.

THE SET IS AN AUTHORIZATION SURFACE AND NOT A DISPLAY STRING, WHICH IS WHY THIS
IS A REQUIREMENT AND NOT AN IMPLEMENTATION NOTE. `add-structured-scope-substrate`
makes every `scope_globs:` repository key a key that "SHALL also be named in
`code_surface`", and `scope_globs:` is what bounds the paths a provenance-gated
autonomous merge may write. A derived set drawn from the gloss therefore admits a
path grant in a repository the declaration never named, on the strength of a word
that appears in an explanation.

THE DERIVATION SHALL BE ONE SHARED READER RATHER THAN ONE PER CONSUMER. Two
readers of one field are two vocabularies, and the divergence between them is
invisible until something authorizes on the wider one. A consumer that needs the
set SHALL obtain it from the reader this capability's gate uses.

WHERE THE HEAD IS `none` THE DERIVED SET SHALL BE EMPTY, and a gloss SHALL NOT
add to it. A declaration of `none` is a declaration that the change has no code
surface at all; a reader that returned the gloss's words for it would return a
non-empty surface for a change that declared none, which inverts the very
distinction the archive gate turns on.

#### Scenario: A consumer derives the repository set from a declaration with a gloss
- **WHEN** a consumer needs the repositories an active change declared, and the declaration is a head followed by a gloss that mentions other repositories by name
- **THEN** the derived set MUST contain exactly the head's identifiers and none of the gloss's

#### Scenario: A structured scope names a repository only the gloss mentions
- **WHEN** a change declares `scope_globs:` for a repository that appears in its `code_surface:` gloss but not in its declared head
- **THEN** the cross-consistency check MUST refuse, the scope naming a repository the change declares no realization surface for

#### Scenario: A declaration of none is read for its repository set
- **WHEN** a consumer derives the repository set from a declaration whose head is `none`, its gloss naming repositories the change does not touch
- **THEN** the derived set MUST be empty

### Requirement: Standing code-surface divergence is named in a closed register
A CLOSED register carried beside the validator SHALL name every active
declaration the grammar does not admit that the act landing this gate does not
correct, each entry carrying its declaration text as it
stands, the class of divergence, the reason, a citation, and the event that
retires the entry. A registered declaration is REPORTED and never refused; every
declaration the register does not name is judged from the day the gate lands, so
the gate is a ratchet and the divergence cannot grow.

THE REGISTER SHALL BE CLOSED, AND CLOSURE SHALL BE ENFORCED RATHER THAN MERELY
DECLARED. An entry may be REMOVED when its declaration is corrected or its packet
archives; admitting a NEW exception SHALL be a change to this specification
rather than an addition to a data file. The validator SHALL carry the baseline of
entries the register holds when the gate lands and SHALL REFUSE any entry that
baseline does not carry, so an exception cannot be granted by appending a line —
granting one takes an edit where the refusal itself is written, and the diff
shows the act for what it is.

THE TWO REFUSALS ARE ASYMMETRIC AND SHALL STAY SO. An unreadable declaration the
register does not name is a statement about the PROPOSAL and the run SHALL fail;
a register entry that matches nothing on a whole-corpus scan is a statement about
the REGISTER — the exception outlived the condition it was granted for — and the
run SHALL refuse with a distinct status until the entry is deleted. Silently
tolerating the second is how an exception list rots into a blanket, and refusing
makes the correction, or the archive, the event that forces the re-examination.

THE REGISTER'S POPULATION IS A FACT ABOUT A TREE AND SHALL BE MEASURED AT THE
TREE THE GATE LANDS ON, never carried from the tree the packet was drafted
against. A proposal landing between the drafting measurement and the gate's own
landing can add a carrier the register was never written for, and the gate is
what makes that visible at all.

#### Scenario: A standing declaration is named by the register
- **WHEN** an active declaration the grammar does not admit is named by a register entry carrying its current declaration text, its class, its reason, its citation and its retirement event
- **THEN** the validator reports it as registered and does not refuse it

#### Scenario: An entry is appended to the closed register
- **WHEN** a register entry names a change and declaration the validator's recorded closed baseline does not carry
- **THEN** the run MUST refuse, because the register is removable and never addable
- **AND** granting the exception takes an edit to the baseline in the same pull request, where the diff shows it

#### Scenario: A register entry matches nothing
- **WHEN** a whole-corpus scan finds a register entry whose change has archived, or whose declaration has been corrected so the recorded text no longer matches
- **THEN** the run MUST refuse with a status distinct from an unreadable-declaration failure, naming the entry
- **AND** the remedy is to delete the entry in the same pull request that made it stale

#### Scenario: The corpus moves between drafting and landing
- **WHEN** a proposal declaring an unreadable head lands on the main line after this packet's register was written and before the gate itself lands
- **THEN** the register MUST be re-measured at the head the gate lands on, and the new carrier disposed of there
- **AND** a register carried unchanged from the drafting tree MUST NOT be treated as evidence about the landing tree
