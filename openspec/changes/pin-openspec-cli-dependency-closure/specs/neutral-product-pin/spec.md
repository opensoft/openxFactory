# neutral-product-pin Specification

## ADDED Requirements

### Requirement: A pinned artifact that resolves dependencies at install time carries a vendored lockfile, and the install runs through it
Where a pinned external neutral product is distributed as a published artifact
whose installation RESOLVES dependency ranges, the pin SHALL carry a VENDORED
RESOLUTION — a lockfile in the format that product's own package manager
consumes, committed beside the pin, addressed by a digest over its exact bytes
recorded in the pin, together with the size of the tree it locks. The consumer's
verifier SHALL recompute that digest BEFORE any registry round trip is spent and
SHALL REFUSE with a named exit on disagreement; SHALL REFUSE unless the vendored
resolution's own entry for the pinned product carries the pin's OWN referent, so
that one pin cannot name two artifacts; and SHALL INSTALL THROUGH the vendored
resolution with the package manager's CLEAN-INSTALL verb — the one that resolves
nothing and refuses when the manifest and the lockfile disagree — never the verb
that may re-resolve a range. A pin that declares NO vendored resolution for such
a product SHALL be refused on the same ground a range is refused: the ranges it
leaves unresolved are a moving reference, and the moment a pin trusts a range the
fail-closed property is gone.

VERIFYING AN ARTIFACT'S OWN BYTES SAYS NOTHING ABOUT THE CODE IT RUNS ON. A
content address over a published artifact addresses every file inside it and no
file outside it, so a tool whose declared dependencies are ranges is a tool whose
BEHAVIOUR is not pinned by its own digest: two runs of identical, verified bytes
may execute different dependency trees, on two machines or on one machine a week
apart. Where that tool is a REQUIRED check, the unpinned half is the half that
can turn a green gate red with no version moved, no pin changed and no commit
authored. The vendored resolution closes that, and any reuse cache the consumer
keeps SHALL be keyed on the vendored resolution's digest as well as the
artifact's, because a different tree is a different install and must not be
served out of a directory built for another one.

THE STAGING MANIFEST THE CLEAN INSTALL REQUIRES SHALL BE DERIVED from the
vendored resolution rather than committed beside it. A clean install refuses when
its manifest and its lockfile disagree, so a second committed file would be a
second copy of one declaration, and copies of a declaration move separately —
which is the defect this capability's pin rule exists to end.

#### Scenario: A pinned artifact declares dependency ranges
- **WHEN** a pin names a published artifact whose manifest declares dependencies as ranges rather than as exact versions
- **THEN** the pin carries a vendored resolution beside it, addressed by a digest over its bytes, and the verifier installs through it
- **AND** a pin carrying none is refused, unresolved ranges being the moving reference this capability already refuses

#### Scenario: The committed resolution and the pin disagree
- **WHEN** the vendored resolution's recomputed digest differs from the digest the pin records, or its entry for the pinned product carries a referent other than the pin's
- **THEN** the run refuses with a named exit, before any artifact is installed
- **AND** the refusal is reported as a defect of the CONSUMING REPOSITORY rather than of the registry, the two halves of one pin having disagreed with each other

#### Scenario: The install re-resolves a range
- **WHEN** a consumer installs the pinned product with a verb that treats the lockfile as a starting point rather than as the answer
- **THEN** the install does not satisfy this requirement, whatever tree it happens to produce, because a run that MAY re-resolve has not pinned the resolution
- **AND** the clean-install verb is used instead, so that "the installed tree is the pinned tree" is a fact about the run rather than a hope

#### Scenario: A reuse cache serves a tree it was not built for
- **WHEN** the vendored resolution changes and a consumer's cache is keyed only on the artifact's address
- **THEN** one directory would serve two different dependency trees and whichever ran first would decide what the second received
- **AND** the cache key incorporates the resolution's digest, so the second tree is a new entry rather than a silent reuse

### Requirement: A vendored resolution is regenerated with the referent, and an entry without one is declared uncovered
A change that moves a pinned artifact's REFERENT SHALL regenerate the vendored
resolution and re-record its digest and its tree size IN THE SAME CHANGE, so that
the referent and its closure move together and never apart; and the regeneration
COMMAND SHALL be recorded in the pin, so a bump does not depend on remembering
how the file was produced. Where a pin records an entry that is NOT covered by a
vendored resolution — a recorded rollback referent, or any other alternative the
pin names — the pin SHALL DECLARE that entry uncovered in the pin itself, stating
what a consumer must author before that entry can be installed at all; an
uncovered entry SHALL NOT be silently installable by resolving its ranges.

THIS OBLIGATION IS ENFORCED AND NOT MERELY STATED. A bump that moved the referent
and left the vendored resolution behind leaves that resolution's entry for the
product carrying the OLD referent, so the verifier's first run after the bump
refuses on the disagreement rule above. The declaration in the pin is therefore a
statement of a condition the running code already checks, which is the form this
capability requires of every pin obligation: running code rather than a stated
duty.

A SPECULATIVELY GENERATED RESOLUTION IS WORSE THAN A DECLARED GAP. Generating a
lockfile for an old referent at today's date records the versions today's ranges
resolve to, which is a fiction of reproducibility rather than a record of one;
and because nothing installs through it, its correctness is checked by no run and
rots unobserved. So the gap is written down, with its consequence, rather than
papered over.

#### Scenario: A version bump forgets the resolution
- **WHEN** a change moves the pin's referent and does not regenerate the vendored resolution
- **THEN** the verifier refuses on its first run, the resolution's entry for the product naming the previous referent
- **AND** the pull request cannot merge where the verifier is a required check, so the obligation is met by the gate rather than by memory

#### Scenario: A rollback referent carries no resolution
- **WHEN** a pin records a previous referent as a rollback and no vendored resolution is committed for it
- **THEN** the pin declares that entry uncovered, and names what must be authored before it can be installed
- **AND** restoring that referent is a change to author rather than a revert to apply, because a rollback that installs an unpinned tree is not the state it claims to restore

#### Scenario: The regeneration recipe is unrecorded
- **WHEN** a pin carries a vendored resolution but does not say how it was produced
- **THEN** the next bump must guess at the staging project that generated it, and a guess produces a diff that is the wrapper rather than the tree
- **AND** the pin records the command and the staging shape, so a regeneration is reproducible by a reader who was not there
