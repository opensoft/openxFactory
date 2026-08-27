# doc-health Specification Delta

## ADDED Requirements

### Requirement: Derivation-pin reachability is verified across a declared artifact class
The doc-health suite SHALL verify derivation-pin reachability across every
committed artifact class that records a repo-local commit pin, rather than
across the cross-reference index alone, and the class SHALL be DECLARED and
checked rather than discovered afresh on each run.

The promoted obligation this extends already exists and covers exactly one
artifact: an unreachable pinned `source_revision` fails the readiness
derivation proof. That requirement is not restated here and nothing about it
moves. What it does not reach is every OTHER committed artifact in this
repository that records the same kind of pin — the derivation and readiness
evidence records under `health/`, gate records under `ideation/dashboard/`, and
any future artifact whose generator stamps a revision. The two live orphans in
this repository at authoring are both in that uncovered remainder, which is the
evidence that a per-artifact obligation does not generalize on its own.

THE DECLARED CLASS IS THE MECHANISM, and it is declared for the same reason the
family enumeration is derived rather than trusted: a scan that finds pin-carrying
artifacts by pattern will silently stop covering an artifact whose generator
renames its key, and a silent loss of coverage looks exactly like a clean run.
The verification SHALL therefore compare the declared class against what the
repository actually carries, and report a pin-carrying artifact that no declared
class member covers — naming the artifact and the key — rather than passing over
it. The declaration MUST distinguish repo-local commit pins from cross-repository
pins, because only the former are answerable against this repository's own refs.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, and the enumeration and its numerals in
the "Deterministic check families" requirement are deliberately untouched and
unrestated. Two reasons, and the first is about the check rather than about
convenience. Reachability is not deterministic in the sense that requirement
means: identical governance-corpus inputs produce different answers in a shallow
clone and a complete one, because the answer is a function of fetched history
rather than of the corpus. A check whose verdict moves with clone depth does not
belong in a pass whose defining property is that identical inputs produce
identical findings. Second, that requirement is the one requirement in this
capability that EVERY new family must restate in full, and a `MODIFIED` block
replaces its counterpart wholesale — so each family added puts canon's family
list at the mercy of archive order, and a requirement every new family must
restate is a requirement every new family can truncate. That hazard is not
hypothetical: three changes in three days truncated it, all three caught by a
human rather than by a check, and this capability now carries a promoted family
whose whole purpose is to catch the next one. A verification that needs no family
declines the hazard entirely rather than managing it.

The verification SHALL live where the existing pin obligation already lives —
the readiness proof surface and the per-repo validator preflight — and SHALL
report a pin unreachable in a complete clone as a failure while reporting a
truncated clone as a skip that names the truncation observed, by reference to the
promoted requirement that already states that split rather than by restating it.

THE REF SET CONSULTED IS `main` PLUS THE RETENTION NAMESPACE
`refs/retention/pins/<full-sha>`, and no more. A pin that neither reaches is
unreachable; a pin either reaches is conforming. The namespace is derivable from
the pin itself, so the verification computes the ref name rather than enumerating
a namespace, which is what keeps the check cheap and keeps a stray ref elsewhere
in the repository from silently greening a pin nobody can find.

#### Scenario: A pin-carrying artifact outside the index is orphaned
- **WHEN** a declared class member other than the cross-reference index carries a pin reachable from no ref, in a complete clone
- **THEN** the run MUST report it, naming the artifact, the pin key, and the pinned commit
- **AND** the report MUST NOT be limited to the cross-reference index because that is where the obligation was first stated

#### Scenario: An artifact carries a pin no declared class covers
- **WHEN** the repository carries a committed artifact recording a repo-local commit pin that no declared class member covers
- **THEN** the run MUST report the uncovered artifact and the key it carries, so the coverage gap is visible rather than invisible
- **AND** the run MUST NOT report the class as fully verified

#### Scenario: A declared member's pin is reachable but stale
- **WHEN** a declared class member pins an ancestor of `main` that is not its tip
- **THEN** no finding is emitted, because staleness between regenerations is legal under the owning capability's rule
- **AND** the verification MUST NOT convert an age comparison into a reachability finding

#### Scenario: The clone cannot answer the question
- **WHEN** the repository under test is shallow or its history is otherwise truncated
- **THEN** the run MUST report the verification as skipped, naming the truncation actually observed
- **AND** no deterministic check family is added, removed, or renumbered by this verification in any run configuration
