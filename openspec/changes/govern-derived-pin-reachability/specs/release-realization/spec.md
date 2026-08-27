# release-realization Specification Delta

## ADDED Requirements

### Requirement: A history-rewriting landing re-derives the pins its rewrite orphans
A history-rewriting landing SHALL re-derive or re-pin every committed artifact
whose derivation pin names a commit that landing orphans, as part of the landing
itself, and MUST NOT move a pin by hand without regenerating the artifact the
pin describes. A history-rewriting landing is one that lands a branch by rebase,
squash, amend, or force-update.

The obligation belongs to the LANDING and not to a later sweep, and the reason
is mechanical rather than stylistic. Before the rewrite, the pinned commit is
reachable and the artifact can be regenerated from it, so the equivalence
between old pin and new pin is measurable. After the rewrite, the old commit may
be reachable from nothing, and the very state a regeneration would read is gone.
A rule that says "fix it afterwards" therefore describes a repair that may no
longer be performable, which is why this reads as a landing obligation and why
the check that discharges it belongs on the branch rather than on `main`.

RE-PINNING IS DEFINED BY REPRODUCTION, not by the pin's value. Where the
artifact's own tooling defines how the artifact is derived — the cross-reference
derivation and its strict index validator are this repository's worked example —
the re-pin SHALL reproduce the committed body BYTE-FOR-BYTE at the new pin, and
the landing SHALL record that it ran the reproduction rather than asserting the
equivalence. Where no tool defines reproduction, the re-pin SHALL name the
measurement that established equivalence at the new pin, or the artifact SHALL
be regenerated so that the question does not arise. A pin edited to a value that
happens to be reachable, with no reproduction and no measurement, satisfies
nothing: it converts an unverifiable claim into a plausible one, which is worse,
because the next reader has no signal that the claim was never checked.

The rewrite's own commits are not the only pins in question. A landing SHALL
consider every artifact its branch touched AND every artifact already on `main`
whose pin names a commit the rewrite orphans, because a branch can orphan a
commit that a previously landed artifact pins without touching that artifact's
file at all.

Where a landing completes and leaves an orphaned pin behind, accepting it SHALL
be a contested-class act requiring an explicit disposition, and the repair route
SHALL be the one the pinned artifact's own class allows rather than whichever is
convenient.

#### Scenario: A branch whose commits are pinned lands rebased
- **WHEN** a branch is landed by rebase or squash, and a committed artifact pins one of the commits that landing rewrites
- **THEN** the landing MUST re-derive or re-pin that artifact as part of itself, before the rewritten commits become unreachable
- **AND** the landing MUST NOT be treated as complete while the artifact still names an orphaned commit

#### Scenario: A pin is moved by hand without regeneration
- **WHEN** a pin is edited to a new commit and the artifact's body is not regenerated at that commit
- **THEN** the reproduction obligation MUST reject the re-pin, because reproduction was neither run nor recorded
- **AND** the pin's reachability MUST NOT be accepted as evidence that the body matches the state it now claims

#### Scenario: The rewrite orphans no pinned commit
- **WHEN** a landing rewrites history and no committed artifact pins any commit the rewrite orphans
- **THEN** no re-derivation is owed and the landing proceeds unchanged
- **AND** the absence MUST be established by looking, not assumed from the branch's file list

#### Scenario: A landing completes with an orphaned pin on main
- **WHEN** a landing has completed and an artifact on `main` names a commit no ref reaches
- **THEN** accepting that state MUST be a contested-class act carrying an explicit disposition
- **AND** the repair MUST follow the route the artifact's own class allows, which for captured evidence is retention of the commit rather than an edit to the pin
