# release-realization Specification Delta

This delta is ALL-ADDED, and that is a MEASURED CHOICE rather than a style. The
divergence it governs sits in the promoted requirement *Realization axis
declaration*, and an active ratified change — `add-structured-scope-substrate` —
already holds a `## MODIFIED Requirements` block over that exact title,
restating its two-value sentence verbatim and adding `scope_globs:` beside it. A
second MODIFIED block over the same title would have to be declared relative to
that change's outcome under *Ordered deltas and branch vocabulary*, and would
inherit that requirement's archive-order hold. An ADDED requirement over a NOVEL
title owes neither, restates no promoted text, drops none, and therefore owes no
`Modified over`, `Removed from canon by` or `Merged into` marker.

**NOTHING PROMOTED IS CHANGED.** *Realization axis declaration* keeps its
two-value vocabulary exactly as ratified — `implemented` or a named release —
and this delta neither widens it nor reads a third value into it. What it adds
is the thing the vocabulary has never had: a reader that refuses a value outside
it. *Realization archive gate* is untouched; the archive path is still decided
by `code_surface:`.

**IT ALSO DOES NOT CONTRADICT THE OTHER ACTIVE DELTA ON THIS CAPABILITY.**
`add-sequenced-after-substrate` ADDS *Strict loading of the realization-axis
front-matter block*, which reaches "every STRUCTURED field" of the block —
`scope_globs:` and `sequenced_after:`. `target_release:` is a PROSE HEADER of
the same block and not a structured field, so this requirement is neither that
one's realization nor an amendment to it. It CONSUMES the loader that rule
produced: the gate reads the declaration through
`scripts/frontmatter_strict.read_front_matter`, so a document the strict loader
refuses is refused here too, reported as a finding against that document rather
than crashing the run.

## ADDED Requirements

### Requirement: Realization axis vocabulary is gated
An ACTIVE change proposal's `target_release:` declaration SHALL carry a value
the ratified vocabulary admits — `implemented`, or a release identifier that
resolves to a release this estate defines — and a house validator SHALL REFUSE
any other value on an active proposal, naming the proposal's path and the value
it carries. A vocabulary stated in prose and read by nobody is a vocabulary the
next proposal diverges from, which is what the corpus shows.

THE DECLARATION IS A VALUE TOKEN FOLLOWED BY AN OPTIONAL PROSE GLOSS, and the
gate SHALL judge the TOKEN and never the gloss. That is the corpus's own form
rather than a rule invented at the gate: the house writes `target_release:
implemented (the openxFactory main line). No contract bundle is cut …`, and a
reader that judged the whole string would refuse every declaration that explains
itself. The token is the first whitespace-delimited word of the declaration.

ABSENCE IS THE PROMOTED DEFAULT AND SHALL NEVER BE A FINDING. *Realization axis
declaration* makes a proposal without the declarations a doc-only change
(`code_surface: none`, `target_release: implemented`) by default, so a proposal
that declares nothing declares the default. Only a PRESENT declaration is
judged — and a declaration present with no value SHALL be refused, because the
author wrote the key and the default is available by omitting it.

AN ARCHIVED PROPOSAL SHALL BE READ AND NEVER JUDGED. An archived packet's front
matter is frozen record — `record-immutability` and `govern-archived-record-edits`
put it beyond a plain fix — so the gate SHALL count what the archive carries and
report it, and SHALL refuse nothing there. A gate that demanded an edit nobody
may make would be a standing finding with no remedy, which is the defect this
estate disposes of rather than creates.

THE STANDING DIVERGENCE SHALL BE NAMED IN A CLOSED REGISTER RATHER THAN
FORGIVEN IN CODE. Where the corpus at the gate's landing carries declarations
outside the vocabulary that are not corrected by the same act, each SHALL be
named in a register carried beside the validator, with the value token as it
stands, the class of divergence, the reason, a citation, and the event that
retires the entry. The register SHALL be CLOSED: an entry may be REMOVED when
its declaration is corrected or its packet archives, and admitting a NEW value
to the vocabulary SHALL be a change to this specification rather than an
addition to the register. A registered declaration is REPORTED and not refused;
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
- **WHEN** an active change declares a release identifier and the estate's release registry carries that release
- **THEN** the validator passes
- **AND** a release-shaped name the registry does not carry MUST be refused, because a name that resolves to nothing is not a named release

#### Scenario: An archived proposal carries an off-vocabulary value
- **WHEN** the scan reaches a proposal under `openspec/changes/archive/` whose declaration is outside the vocabulary
- **THEN** it MUST NOT be a finding, and the run reports how many such records the archive carries

#### Scenario: A standing declaration is named by the register
- **WHEN** an active declaration outside the vocabulary is named by a register entry carrying its current value token, its class, its reason, its citation and its retirement event
- **THEN** the validator reports it as registered and does not refuse it

#### Scenario: A register entry matches nothing
- **WHEN** a whole-corpus scan finds a register entry whose change has archived, or whose declaration has been corrected so the value token no longer matches
- **THEN** the run MUST refuse with a status distinct from an off-vocabulary failure, naming the entry
- **AND** the remedy is to delete the entry in the same pull request that made it stale

#### Scenario: A proposal declares no target release
- **WHEN** an active change's `proposal.md` declares no `target_release:` at all
- **THEN** the validator passes, the proposal having taken the promoted doc-only default
