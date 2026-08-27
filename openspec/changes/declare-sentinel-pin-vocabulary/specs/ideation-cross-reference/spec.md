# ideation-cross-reference Specification Delta

## ADDED Requirements

### Requirement: A generator that cannot truthfully pin a commit writes a declared sentinel, never a commit name
A generator recording a repo-local derivation pin SHALL write a commit name ONLY
where that commit describes the content being recorded, and where it cannot, it
MUST write a value drawn from a DECLARED shared sentinel vocabulary — never a
commit name that never described the content, and never an undeclared free-form
string of the generator's own invention.

AN UNTRUE PIN IS WORSE THAN AN UNREACHABLE ONE, and the two defects are not the
same defect wearing different clothes. The promoted obligation next to this one
governs a pin that STOPPED being resolvable: the artifact's claim was true when
it was written, something later made the state unrecoverable, and the repair is
to make the state reachable again. That is not this. A pin stamped from `HEAD`
while the generator reads a dirty working tree names a commit that is perfectly
reachable and perfectly wrong — it says "I was derived from the corpus as it
stood at X" about content no commit ever held. A reader who resolves it gets an
answer, checks nothing, and is misled precisely because the pin looks healthy.
Neither the reachability rule nor its retention repair reaches this, because
nothing about the object is missing. Neither promoted requirement is restated or
modified here; this states the obligation that runs before either of them can
apply.

A SENTINEL IS A PROVENANCE CLAIM, NOT AN ABSENCE OF ONE. "This was taken from a
working tree that was not committed" is a statement a reader can act on: it says
the content is unreconstructible from the repository, names why, and stops the
reader from believing the artifact was derived from a state anybody can
reproduce. That is strictly more than a commit name that resolves to the wrong
tree, and strictly more than a key nobody wrote. The vocabulary therefore
carries one declared value PER CONDITION rather than a single "no pin" value:
content read from an uncommitted working tree, a derivation performed outside
any repository context, a repository whose state could not be read at all, and a
projection composed from several sources with no single source revision are four
different facts about how the artifact came to be, and collapsing them loses the
part a reader needs.

THE VOCABULARY IS SHARED ACROSS EVERY GENERATOR, and that is the whole of what
makes it a vocabulary rather than a habit. One condition SHALL have one declared
spelling, used by every generator that stamps a repo-local derivation pin, so
that a reader meeting the value in an artifact they have never seen knows what
it means without reading that artifact's generator, and so that a consumer
guarding on the value guards on the same string everywhere. A spelling invented
per lane is invisible to every consumer written against a different lane's
spelling, and a consumer that misses a sentinel treats it as a pin.

A SENTINEL IS NEVER A LICENCE TO SKIP A PIN THAT WAS AVAILABLE. Where the
generator can name a commit that truthfully describes the recorded content, it
SHALL write that commit; writing a sentinel to avoid resolving the question is a
provenance claim that is itself false, and the verification cannot tell it from
an honest one.

#### Scenario: The generator reads a working tree that is not committed
- **WHEN** a generator records a derivation pin for content it read from a working tree carrying uncommitted changes to that content
- **THEN** it MUST write the declared sentinel for that condition rather than the current `HEAD`, because `HEAD` would name a commit that never held the content being recorded
- **AND** the resulting artifact MUST NOT be treated as carrying a commit pin at all

#### Scenario: The working tree is clean
- **WHEN** a generator records a derivation pin for content that is committed at the revision it is reading
- **THEN** it MUST write that commit name exactly as before, and nothing in this requirement changes the pin, the key, or the artifact
- **AND** the reachability obligation applies to that pin unchanged

#### Scenario: The generator cannot read repository state at all
- **WHEN** the generator runs outside a repository, against an unborn `HEAD`, or where the revision cannot be resolved
- **THEN** it MUST write the declared sentinel for that condition rather than omitting the key, an empty string, or a placeholder of its own choosing
- **AND** the condition it names MUST be the one that actually held, so a reader can tell an ad-hoc derivation from an unreadable repository

#### Scenario: A generator invents its own spelling
- **WHEN** a generator writes a non-commit value into a derivation-pin key that the shared vocabulary does not declare
- **THEN** the value MUST be refused as an undeclared sentinel rather than accepted as a locally reasonable choice
- **AND** the remedy MUST be to declare the value in the shared vocabulary or to use the declared spelling for the condition, never to leave the spelling local to one generator

### Requirement: The sentinels already committed are declared as they stand, and are never rewritten to normalize them
Committed values that already act as sentinels SHALL be brought into the
declared vocabulary as the spellings the repository actually carries, and MUST
NOT be rewritten in place to make the vocabulary tidier.

THIS RULE EXISTS BECAUSE THE PRACTICE CAME FIRST. The sentinel idea was not
designed and then adopted; it was written by hand, one packet at a time, into
proposal-support manifests whose generator has never emitted such a value — and
it was right every time. Those hand-written values are the evidence that a
generator confronted with content it cannot pin reaches for an honest non-pin
rather than a false commit, and they are the reason this vocabulary is worth
declaring at all. A declaration that erased them to start from a clean sheet
would delete its own justification.

REWRITING THEM IS ALSO REFUSED ON THE RULE THIS CAPABILITY ALREADY CARRIES.
Every such value sits inside an archived packet, and a content edit to captured
material after capture is a finding in its own right; a value edited to a
spelling the run did not write makes the artifact state something that did not
happen. The same ordering the retention rule settles for an orphaned pin settles
this: when the record cannot move, the declaration is what accommodates it.

MULTIPLE SPELLINGS FOR ONE CONDITION ARE THEREFORE LEGAL, AND EACH SHALL SAY
WHICH IT IS. Where the committed corpus carries more than one spelling of the
same condition, the declaration SHALL name one as canonical — the spelling new
generator output uses — and declare the others as legacy members that remain
legal in committed state and MUST NOT be written afresh. A legacy member without
that marking is indistinguishable from a second canonical spelling, which is the
drift this requirement exists to stop rather than to bless.

AND THE DECLARATION IS WHERE THE CONSUMERS ARE RECONCILED. A guard that compares
a pin value against one spelling of a condition SHALL be reconciled against the
declared vocabulary rather than against whichever spelling its own lane happened
to write, because a consumer that recognizes only one member of a condition
treats every other member as a commit name and fails on it.

#### Scenario: A committed sentinel predates the vocabulary
- **WHEN** the declaration is written and the repository already carries values acting as sentinels in committed artifacts
- **THEN** those spellings MUST be declared as members of the vocabulary, each naming the condition it stands for
- **AND** the artifacts carrying them MUST NOT be edited to a different spelling

#### Scenario: Two spellings name one condition
- **WHEN** the committed corpus carries more than one spelling for the same condition
- **THEN** the declaration MUST name one canonical spelling for new output and mark the others as legacy members that stay legal where they are already committed
- **AND** a generator MUST NOT write a legacy spelling into new output

#### Scenario: A consumer recognizes only one spelling
- **WHEN** code that reads a derivation pin compares its value against a single sentinel spelling rather than against the declared vocabulary
- **THEN** that comparison MUST be reported as a coverage gap, because every unrecognized member of the vocabulary reaches that code as though it were a commit name
- **AND** the repair MUST be to consult the declaration rather than to add one more literal to the comparison

#### Scenario: Tidying is proposed as the repair
- **WHEN** a change proposes to normalize committed sentinel spellings by editing the artifacts that carry them
- **THEN** the edit MUST be refused for a captured artifact, on the same rule that refuses editing a captured pin
- **AND** the vocabulary MUST absorb the spelling instead, because the declaration is the thing that can change without falsifying a record
