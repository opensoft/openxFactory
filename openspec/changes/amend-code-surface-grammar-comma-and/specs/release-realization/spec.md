# release-realization

**ONE `## MODIFIED` REQUIREMENT, AND IT IS A RECONCILIATION WITH RUNNING CODE
RATHER THAN A DECISION.** The block below is written OVER CANON —
`openspec/specs/release-realization/spec.md` as `main` states it at `3e32d987`,
lines 1014–1132 — and every word of it is canon's own except what
`scripts/code_surface.py` has made untrue since the gate this requirement
governs first ran. `_SEPARATOR_RE` (`scripts/code_surface.py:152-157`) admits
FOUR list separators and the promoted text names THREE; the fourth, `, and `, is
tried FIRST so that a list spelled out with an Oxford comma is consumed as one
separator rather than as a bare comma followed by a member opening with the word
`and`. This block is that catch-up. **NOT ONE CHARACTER OF THE READER CHANGES**:
no declaration that passes today is refused after it, none that is refused today
passes, and no derived repository set moves.

**THIS CHANGE IS THE SOLE ACTIVE MODIFIER OF THE REQUIREMENT IT CARRIES.**
Measured 2026-09-18 over every active change directory: three other active
changes carry a `release-realization` delta — `add-sequenced-after-substrate`
(`## ADDED` only, nine ordered-delta requirements), `add-structured-scope-substrate`
(a `## MODIFIED` block over *Realization axis declaration*, plus five `## ADDED`)
and `add-target-release-deferred-allocation` (a `## MODIFIED` block over
*Realization axis declaration* and one over *Realization axis vocabulary is
gated*) — and NONE writes this requirement key. So no ordering declaration is
owed in either direction and `sequenced_after: []` is the positive root claim
that follows from the measurement.

**WHAT MOVES: ONE BODY SENTENCE, ONE BODY SENTENCE OF A SECOND PARAGRAPH, AND
ONE SCENARIO BULLET — THREE UNITS, EACH REPLACED IN PLACE AND EACH NAMED IN ONE
`Removed from canon` MARKER. TWO BODY PARAGRAPHS AND ONE SCENARIO ARE ADDED.**
Every other unit of the requirement is carried byte-faithfully, by CONSTRUCTION
rather than by transcription: the block was produced by slicing promoted canon
and applying each replacement as an exact single-occurrence substitution.

## MODIFIED Requirements

### Requirement: Code-surface declaration grammar is gated
An ACTIVE change proposal's `code_surface:` declaration SHALL open with a
DECLARED HEAD the ratified grammar admits — EITHER the single token `none`, OR a
list of one or more REPOSITORY IDENTIFIERS separated by a comma, by `, and `, by
` and `, or by ` + `, THOSE TWO HEAD FORMS being EXCLUSIVE alternatives and
never mixed — and a house validator SHALL REFUSE any active declaration whose
head it cannot read, naming the proposal's path and the text the declaration
carries. A declaration whose repositories cannot be told from its explanation is
a declaration no reader can act on, which is what the corpus shows.

`, and ` IS ONE SEPARATOR AND SHALL BE READ AHEAD OF THE BARE COMMA, which is
the whole of what distinguishes it from the other three. A list spelled out the
way English spells one out — `openxFactory, openXwallet, and codexFactory` —
offers a reader two readings: THREE identifiers, the last separated by a comma
and the conjunction together; or TWO identifiers and a head that resumes at the
word `and`. The grammar takes the first, and takes it BY ORDER rather than by a
special case: the longer separator is tried at each position before the bare
comma, so the conjunction is consumed WITH the comma that precedes it instead of
being left to open the next member. THE FOUR SEPARATORS ARE ALTERNATIVES WITHIN
ONE LIST AND ARE NOT EXCLUSIVE OF EACH OTHER — one head MAY separate its members
by more than one of them, which is what a three-item list in ordinary prose does,
and nothing in a mixed-separator head makes a reader guess.

THE DECLARATION IS A HEAD FOLLOWED BY AN OPTIONAL PROSE GLOSS, and the gate
SHALL judge the HEAD and never the gloss. That is the corpus's own form rather
than a rule invented at the gate: the house writes ``code_surface: openxFactory —
`scripts/…` (NEW) …``, and a reader that judged the whole string would refuse
every declaration that explains itself. The gloss SHALL be introduced by a GLOSS
OPENER, and the opener set SHALL be the set the corpus already uses rather than
one the gate prefers: an em dash, an en dash, an opening parenthesis, a full
stop, a colon, or a semicolon. A head that runs into ordinary prose with no
opener — a possessive, an apposition, or a sentence continued by `, and …` whose
continuation the identifier grammar cannot read — is REFUSED, because there is
then no point in the string at which the declaration stops and the explanation
starts, and every reader must guess a different one.

THE `, and …` CASE IS THE ONE THE SEPARATOR ABOVE NARROWS, AND THE NARROWING IS
STATED HERE RATHER THAN LEFT TO BE FOUND. Where the words after `, and ` are
themselves a REPOSITORY IDENTIFIER followed by a gloss opener or by the end of
the declaration, they are ADMITTED as a further member of the list, that being
exactly the spelled-out form the separator exists to read. Where they are not —
an ordinary sentence, which is what an explanation is — the REFUSAL STANDS and
names the point at which reading stopped. The two cases are told apart by the
identifier grammar and by nothing else, no reader weighing whether a word looks
like a repository; and the remedy is unchanged and is the author's, a gloss
opener written before the explanation begins.

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

**AMENDED BY `amend-code-surface-grammar-comma-and` (2026-09-18).** Every
paragraph and every scenario of this block is promoted canon's own bytes except
what `scripts/code_surface.py` made untrue on the day the gate landed: the
opening sentence's list of separators, the sentence that refused a head
continued by `, and …` flatly, and the WHEN bullet of *An active proposal
declares several repositories*. `_SEPARATOR_RE` has admitted a FOURTH
alternative since the module was written — `, and `, tried FIRST, ahead of the
bare comma — and the promoted text named three, so a declaration spelled out
with an Oxford comma passed a gate canon said would refuse it. THIS BLOCK MOVES
NO BEHAVIOUR: not one character of `scripts/code_surface.py` changes with it, no
declaration that passes today is refused after it and none that is refused today
passes, and the repository set derived from any head in the corpus is
identical before and after. TWO CLARIFICATIONS RIDE THE CORRECTION AND BOTH
DESCRIBE THE SAME READER: the exclusivity clause of the opening sentence is said
of THE TWO HEAD FORMS rather than of the separators it now follows four of —
which is the antecedent the originating packet's own design record names,
"EITHER the single token none, OR a list … the two being EXCLUSIVE alternatives
and never mixed" — and the separators are stated to be alternatives WITHIN one
list, which is what the reader has always done and what the promoted text left a
reader of a four-item list to guess at. NOTHING ELSE MOVES: the sentinel rule,
the identifier shape, the gloss-opener set, the repeated-header refusal, the
block-scalar refusal, the absence default and the archived-record rule are
carried unchanged, and no scenario is removed or retitled. ONE SCENARIO IS
ADDED, beside *An active proposal declares several repositories* rather than at
the end of the block, because it is that scenario's own case at the grain the
correction moves and a reader looking for the list grammar finds them together.

**Removed from canon by amend-code-surface-grammar-comma-and (2026-09-18):** ``An ACTIVE change proposal's `code_surface:` declaration SHALL open with a DECLARED HEAD the ratified grammar admits — EITHER the single token `none`, OR a list of one or more REPOSITORY IDENTIFIERS separated by a comma, by ` and `, or by ` + `, the two being EXCLUSIVE alternatives and never mixed — and a house validator SHALL REFUSE any active declaration whose head it cannot read, naming the proposal's path and the text the declaration carries.``; ``A head that runs into ordinary prose with no opener — a possessive, an apposition, or a sentence continued by `, and …` — is REFUSED, because there is then no point in the string at which the declaration stops and the explanation starts, and every reader must guess a different one.``; `` **WHEN** an active change declares two or more repository identifiers separated by a comma, by ` and `, or by ` + ` `` — the module has read a fourth separator since the gate landed, so the first of these three units names three where the reader admits four, and the second states as a flat refusal a case the reader decides by whether the words after the conjunction are themselves a readable identifier. The third is the same three-separator list in the scenario that exercises it. Each is REPLACED in place rather than dropped: the sentences above state the four separators, the order that makes the longest one win, and the narrow case the fourth one admits. This reason carries no code span, so the marker names exactly the three units listed before the separator.

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
- **WHEN** an active change declares two or more repository identifiers separated by a comma, by `, and `, by ` and `, or by ` + `
- **THEN** the validator passes and the declared repository set is every identifier in the head
- **AND** an identifier spelled as an `<owner>/<name>` address is admitted on the same terms as a bare repository name, both spellings being ones the corpus carries

#### Scenario: A declaration spells its list out with an Oxford comma
- **WHEN** an active change's head separates the last two of three repository identifiers by `, and ` — `openxFactory, openXwallet, and codexFactory`
- **THEN** the validator passes and the declared repository set is the THREE identifiers, the comma and the conjunction having been consumed as ONE separator
- **AND** the head MUST NOT be read as two identifiers followed by a member opening with the word `and`, the longer separator being tried before the bare comma at each position
- **AND** a head that separates its members by more than one of the admitted separators is admitted on the same terms, the separators being alternatives within one list rather than exclusive of each other

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
