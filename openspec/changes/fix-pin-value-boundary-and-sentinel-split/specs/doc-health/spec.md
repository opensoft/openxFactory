# doc-health

## ADDED Requirements

### Requirement: A pin site is built only from a value that is a whole object name
The pin verification SHALL create a derivation-pin site only where the matched
value is a WHOLE object name, and MUST NOT manufacture a pin from a prefix of a
longer hexadecimal run.

A PIN THE ARTIFACT DOES NOT CARRY IS THE ONE VALUE THIS VERIFICATION MUST NEVER
PRODUCE. Everything else the class reports is a reading of committed bytes: a
pin is reachable, orphaned, lost, uncovered, a legal non-pin or an undeclared
one, and in every case the value under judgment is the value the artifact
holds. A truncated prefix is not. It is a string the verification composed out
of the first forty characters of something longer, and every downstream verdict
about it is a verdict about a value nobody wrote — which is a worse failure than
any of the outcomes the class already names, because the reader cannot find the
subject of the finding by opening the file.

BOTH WAYS IT GOES WRONG ARE WORTH FAILING ON, and they fail in opposite
directions. The fabricated prefix is overwhelmingly likely to name no object at
all, so the run reports an ORPHANED PIN on an artifact whose recorded value is
intact — sending a reader to retention, to a superseding record, or to a
re-derivation, for a defect that does not exist. And it may instead COLLIDE: a
forty-character prefix that happens to name a real commit in this repository
reports as REACHABLE, and the verification then certifies a provenance claim it
never read. A check that can certify a claim it did not read is worse than a
check that abstains.

THE GUARD ALREADY EXISTS IN THE SAME MODULE AND WAS NOT CARRIED TO THE REGEXES
THAT BUILD SITES. The standalone-object-name scanner carries an explicit
hexadecimal boundary on both sides and a comment stating that a longer digest
would otherwise yield spurious pins. The obligation here is that EVERY
expression that builds a pin site carries the same boundary — the field forms,
the vocabulary sweep, and the prose members' own patterns alike. A guard stated
in one place and absent from the four that matter is not coverage; it is a
comment.

THE OBLIGATION IS ON THE VALUE, NOT ON A LIST OF LENGTHS. The rule is not "reject
sixty-four characters": it is that a value is a pin only if the WHOLE value is
an object name, so a forty-one-character run, a sixty-four-character digest and
a forty-hex token abutting further hexadecimal text are all refused by the same
rule rather than by an enumeration of the widths somebody thought of. And a
repository whose object names are a different width is accommodated by widening
what counts as an object name, never by loosening the boundary — the boundary is
what makes "whole" mean anything.

THE VALUE IS NOT DISCARDED, IT IS HANDED ON WHOLE. A value refused as a pin is
still a value standing under a declared pin key, and it therefore reaches the
non-commit classification exactly as any other non-commit value does, where the
promoted classification requirement already decides it — a legal non-pin where
the vocabulary declares it, a defect naming the artifact, the key and THE WHOLE
VALUE where it does not. Refusing to build the site is what makes that
classification the only reading of the value, rather than a second reading
racing a fabricated first one.

NOTHING ABOUT A CONFORMING PIN MOVES. A value that IS a whole object name builds
the same site it builds today, against the same declared class, the same key
set, the same serializations, the same ref set and the same verdicts. This
requirement changes what is REFUSED, and refuses nothing that was ever a pin.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, for the reasons the verification that
carries it already states in its own promoted requirements, and the family
enumeration and its numerals are untouched and unrestated.

#### Scenario: A digest longer than an object name stands under a declared pin key
- **WHEN** a swept artifact carries, under a declared pin key, a hexadecimal value longer than a whole object name — a sixty-four-character digest, or any run of hexadecimal characters that does not end where an object name would
- **THEN** the verification MUST NOT build a pin site from any prefix of it, and MUST NOT report that prefix as reachable, orphaned, lost or retained
- **AND** the whole value MUST reach the non-commit classification unshortened, where an undeclared value is reported as a defect naming the artifact, the key and the value as written

#### Scenario: The fabricated prefix would have resolved
- **WHEN** the first forty characters of such a value happen to name an object this repository holds and a ref reaches
- **THEN** the verification MUST still refuse to build a site, because a coincidental resolution is not a reading of the artifact's claim
- **AND** it MUST NOT report the artifact's provenance claim as verified on the strength of an object the artifact does not name

#### Scenario: A whole object name is unaffected
- **WHEN** the value under a declared pin key is a whole object name — quoted or bare, in a mapping field, in compact serialization, or inside the sentence a prose class member declares its own pattern for
- **THEN** the site is built exactly as before, and the ref set consulted, the verdicts reached and the reported outcomes are unchanged
- **AND** no finding is introduced by this requirement for any value that was a pin before it

#### Scenario: The boundary is stated once and applied everywhere a site is built
- **WHEN** the module carries an expression that builds a pin site — a field form, a vocabulary sweep, or a class member's declared prose pattern
- **THEN** every such expression MUST carry the whole-object-name boundary, and a new one added later MUST carry it too
- **AND** a boundary present on the module's standalone scanner MUST NOT be read as covering the expressions that build sites, because the site builders are where a fabricated pin is produced
