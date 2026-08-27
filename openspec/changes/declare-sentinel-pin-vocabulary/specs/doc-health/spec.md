# doc-health Specification Delta

## ADDED Requirements

### Requirement: A declared sentinel is verified as a legal non-pin, and an undeclared non-commit value is a defect
The pin verification SHALL classify a derivation-pin value that is not a commit
name into one of exactly two outcomes — a LEGAL NON-PIN where the value is
declared in the shared sentinel vocabulary, or a DEFECT where it is not — and
MUST NOT leave such a value unclassified.

SILENCE IS THE CURRENT ANSWER, AND SILENCE IS THE DEFECT. The verification finds
pins by matching a commit-shaped value against a declared key, so a key holding
anything else produces no site at all: it is not reachable, not orphaned, not
lost, and — this is the part that matters — not UNCOVERED either. The artifact
is swept, the key is declared, the file is a member of the class in good
standing, and the value is skipped. A run therefore reports a fully verified
class over an artifact whose central provenance claim nothing has read. That is
exactly the silent-coverage shape the declared class was built to end, arriving
through the value rather than through the key, and the declared class does not
close it because the class declares WHICH KEYS carry pins and never what a
non-commit value in one of them means.

THE LEGAL NON-PIN IS A FIFTH OUTCOME, NOT A PASS IN DISGUISE. It sits beside
reachable, orphaned, lost and uncovered rather than inside any of them, and the
distinctions are load-bearing in both directions. It is NOT reachable: there is
no commit, so no ref reaches it and reporting it as reachable would claim a
resolution nobody performed. It is NOT orphaned or lost: those verdicts say a
named commit cannot be found, and here no commit was ever named, so a repair
route — retention, re-derivation, a superseding record — would be offered for a
defect that does not exist. It is NOT uncovered: the key is declared and the
sweep did read the site, so reporting a coverage gap would send the next reader
to widen a declaration that is already correct. And a legal non-pin MUST NOT
hold full verification open, because the artifact is conforming: it made an
honest claim about content nobody can reconstruct, which is the outcome the
generator obligation asks for.

AN UNDECLARED NON-COMMIT VALUE IS REPORTED AS A DEFECT, naming the artifact, the
key and the value. Two things reach that branch and both are worth failing on: a
generator that invented a spelling nobody declared, and a value that is neither
a commit nor a sentinel — a truncated object name, a placeholder, an empty
string, a spelling drifted by one character from a declared member. The
verification cannot tell those apart and SHALL NOT try, because the remedy is
the same for all of them: declare the value or fix the generator. What it MUST
NOT do is guess that a value resembling a declared member was meant as that
member, since a near-miss spelling is precisely the condition under which every
consumer guarding on the exact string already fails.

THE COMMIT-SHAPED PATH IS UNTOUCHED. A value that is a commit name is verified
for reachability exactly as the promoted requirement states, and this
requirement neither restates nor modifies it. Nothing here converts a
reachability answer into a vocabulary answer, or the reverse.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, and the enumeration and its numerals in
the "Deterministic check families" requirement are deliberately untouched and
unrestated. This is a classification inside a verification that already declines
a family for reasons its own requirement states, and a `MODIFIED` block over a
requirement every new family must restate in full is a hazard this capability
now carries a family to police.

#### Scenario: A declared sentinel stands in a pin key
- **WHEN** a swept artifact carries, under a declared pin key, a value that the shared sentinel vocabulary declares
- **THEN** the verification MUST report it as a legal non-pin, naming the artifact, the key and the condition the sentinel states
- **AND** it MUST NOT be reported as reachable, orphaned, lost or uncovered, and MUST NOT hold full verification open

#### Scenario: An undeclared non-commit value stands in a pin key
- **WHEN** a swept artifact carries, under a declared pin key, a value that is neither a commit name nor a declared sentinel
- **THEN** the verification MUST report it as a defect, naming the artifact, the key and the value
- **AND** it MUST NOT be skipped, guessed at, or matched to the nearest declared member

#### Scenario: The value is a commit name
- **WHEN** a swept artifact carries a commit name under a declared pin key
- **THEN** the reachability verification proceeds exactly as before, and this classification changes neither its ref set nor its verdicts
- **AND** no sentinel outcome is emitted for it

#### Scenario: A sentinel appears under a key no declared member covers
- **WHEN** a sentinel-valued key is carried by an artifact that no declared class member covers
- **THEN** the uncovered-artifact report MUST still fire on the key, because a coverage gap in the declaration is a separate finding from the value's classification
- **AND** the two findings MUST be reported separately rather than one being allowed to mask the other

### Requirement: The sentinel vocabulary is declared beside the pin class, and the declaration is itself checked over the same inventory
The shared sentinel vocabulary SHALL be DECLARED rather than discovered, in the
same place and the same form as the declared pin class it qualifies, and the
declaration SHALL be checked against what the repository actually carries rather
than trusted.

A DECLARATION THAT NOTHING CHECKS IS A SECOND PLACE FOR DRIFT TO HIDE. This
capability already learned that lesson twice — the check-family enumeration is
derived from the registry rather than restated on trust, and the pin class is
compared against the committed corpus so a renamed key surfaces as an uncovered
site rather than as silence. A vocabulary of honest non-pins earns the same
treatment for the same reason: its whole purpose is that one condition has one
spelling everywhere, and a list nobody measures against the corpus stops being
true the first time a generator writes a value the list does not carry.

THE CHECK RUNS IN BOTH DIRECTIONS, and each direction catches a different
failure. Corpus against declaration: a non-commit value standing in a declared
pin key that the vocabulary does not declare is reported, which is the branch
that catches a new generator inventing a spelling. Declaration against corpus: a
declared member that no committed artifact carries and no generator emits is
reported too, because a vocabulary that accumulates entries nobody writes
becomes a place where a reader looks up a value and finds a plausible-sounding
condition that never applied. Reporting a stale member is not deleting it — a
condition can be declared before its generator lands, in the same way the pin
class declares members whose first committed instance has not arrived yet — but
the state MUST be visible rather than assumed.

THE INVENTORY THE CHECK RUNS OVER IS THE PIN CLASS'S OWN, STATED EXPLICITLY.
The scope is every artifact the declared pin class already sweeps, under every
key that class declares, in the serializations it already reads. It is NOT
widened to files the class excludes, and the declared exclusions keep their
stated reasons and their stated trades: prose quotes sentinels exactly as it
quotes commit names, so a governance document narrating a dirty-tree derivation
is not itself making one. Naming the scope as the class's own inventory is what
keeps the two declarations answering for the same corpus — a vocabulary checked
over a wider or narrower set than the pins it qualifies would report gaps that
the pin class does not have, and miss gaps that it does.

THE DECLARATION STATES A CONDITION PER MEMBER, and a member without one is
itself a defect. A sentinel whose meaning is not written down is a magic string,
and a reader who meets it in an artifact learns only that somebody chose not to
write a commit. Every member SHALL name the condition it stands for and whether
it is canonical for new output or a legacy spelling retained for committed
state.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, for the reasons the verification that
carries it already states, and the family enumeration and its numerals are
untouched and unrestated.

#### Scenario: A generator writes a spelling the vocabulary does not declare
- **WHEN** committed state carries a non-commit value under a declared pin key and the vocabulary declares no such member
- **THEN** the check MUST report it, naming the artifact, the key and the value, so the spelling is declared or the generator corrected
- **AND** the report MUST NOT be satisfied by the value being plainly readable to a human

#### Scenario: A declared member nothing carries
- **WHEN** the vocabulary declares a member that no committed artifact carries and no generator emits
- **THEN** the check MUST report the member as unused, so the declaration cannot silently accumulate conditions that never applied
- **AND** the report MUST NOT be treated as an instruction to delete a member whose generator has not landed yet

#### Scenario: A member is declared without its condition
- **WHEN** a vocabulary member is declared without stating the condition it stands for, or without stating whether it is canonical or legacy
- **THEN** the declaration MUST be reported as incomplete
- **AND** the member MUST NOT be accepted on the strength of its spelling being self-explanatory

#### Scenario: The scope is questioned at the edge of the class
- **WHEN** a non-commit value stands under a pin-shaped key in a file the declared pin class excludes as a non-member
- **THEN** no sentinel finding is emitted for it, because the vocabulary check runs over the pin class's own inventory and inherits its declared exclusions with their stated reasons
- **AND** the exclusion MUST remain a declaration with a reason rather than becoming an unstated boundary of this check
