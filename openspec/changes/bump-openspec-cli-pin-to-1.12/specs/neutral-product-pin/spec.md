# neutral-product-pin Specification

## ADDED Requirements

### Requirement: A dispositioned finding is cited, upgrade-coupled, and refused when stale
A pinned tool's finding that a consuming repository DECLINES TO FIX SHALL be recorded as an explicit DISPOSITION in the pin file itself, and that disposition SHALL carry a non-empty CITATION to the canon that makes the acceptance lawful and SHALL name the authority that granted it; a disposition carrying neither is an UNCITED EXCEPTION and the pin is REFUSED rather than the entry being skipped.
A pinned tool is a FOREIGN JUDGMENT about a LOCAL corpus, and the two can
genuinely disagree without either being defective. Where the disagreement is
that the tool cannot read a convention this corpus has RATIFIED, the only edit
that satisfies the tool would REVERT a ratified decision — so the finding is not
a defect to remedy but an exception to accept, and an exception this estate
cannot see is worse than the finding it hides.

THE DISPOSITION IS ENUMERATED, NEVER PATTERNED. A disposition SHALL identify ONE
finding — the repository, the item, the delta path, and the finding's own text
compared whole after whitespace normalization — and SHALL NOT be expressed as a
pattern, a wildcard, a severity or a family. One written exception that could
absorb a second, unread finding is the failure mode of every suppression list,
and enumeration is what makes each acceptance a separate human reading.

THE DISPOSITIONS ARE UPGRADE-COUPLED. They are declared against ONE version's
findings and SHALL be RE-DERIVED whenever the pin's version moves, because a
different version is a different judgment: a tool that rewords, drops or adds a
check produces findings the old exceptions do not describe. A pin that carried
its predecessor's exceptions forward unexamined would be granting exemptions in
the name of a judgment nobody made.

A DISPOSITION MATCHED BY NO FINDING IN A WHOLE-CORPUS SCAN SHALL REFUSE THE
RUN, and a NARROWED scan SHALL NOT decide staleness at all — "this finding no
longer occurs" is a claim about the whole corpus, and a run over named targets
legitimately never opens the items it was not asked about. A narrowed run SHALL
still APPLY the dispositions it matches, and SHALL state that it checked none
for staleness, so a green narrowed run is never mistaken for an audit of the
list. An exception that
outlives the condition it was granted for is a standing exemption nobody
re-reads, and the moment that makes it stale — the change archiving out of the
scanned corpus, or the tool ceasing to report it — is precisely the moment a
human should re-examine it. The refusal SHALL be a defect of the PIN and not of
the deltas: an unmatched FINDING is a statement about what somebody wrote, an
unmatched DISPOSITION is a statement about the pin file, and the two send a
reader to different remedies.

A DISPOSITION IS SCOPED TO ONE REPOSITORY. Where one pin governs several
consuming repositories, a disposition SHALL name the repository whose corpus it
is about, and a run over any other repository SHALL neither apply it nor treat
it as stale — otherwise a change absent because it was never in that tree is
indistinguishable from a change absent because it archived, and only the second
may refuse.

A RUN THAT APPLIED A DISPOSITION SHALL SAY SO, BY NAME. The run's output SHALL
name every applied exception, its reason, its citations and its granting
authority, and SHALL NOT report the result in terms that read as a clean tree; a
green check that silently suppressed a finding has told its reader something
false by omission.

#### Scenario: A pinned tool reports a finding the corpus has ratified against
- **WHEN** a pinned tool's check contradicts a convention this corpus has ratified, and the only edit satisfying the tool would revert a ratified decision
- **THEN** the finding is DISPOSITIONED in the pin with a citation to that canon rather than fixed
- **AND** the pin is not moved back, nor the check disabled, nor the decision reverted

#### Scenario: A disposition carries no citation
- **WHEN** a disposition records no `cited_to:`, an empty one, or no granting authority
- **THEN** the pin is REFUSED as malformed, before any artifact is fetched
- **AND** the entry is not silently skipped, because skipping would re-fail a finding somebody believed was settled

#### Scenario: A dispositioned finding stops occurring
- **WHEN** a declared disposition is matched by no finding in the run — its change archived, or the tool no longer reports it
- **THEN** the run REFUSES with a named exit until the disposition is removed
- **AND** the refusal is a defect of the pin rather than of the deltas, so its remedy is an edit to the pin file

#### Scenario: A run opens only named targets
- **WHEN** the pinned validator is invoked over named items rather than the whole corpus
- **THEN** the dispositions matching those items are applied, and NO disposition is reported stale
- **AND** the run states that staleness was not checked, a narrowed scan being unable to establish that a finding no longer occurs

#### Scenario: A finding is reported that no disposition covers
- **WHEN** the pinned tool reports a blocking finding that no in-scope disposition matches
- **THEN** the run FAILS with the ordinary invalid-deltas verdict, naming each uncovered finding
- **AND** the remedy offered is to fix it OR to disposition it with a citation, never to loosen the match

#### Scenario: The pin's version moves
- **WHEN** a change moves the pinned version
- **THEN** the dispositions are RE-DERIVED against the target version's own findings and evidenced in that same change
- **AND** an exception inherited without re-derivation is refused, a different version being a different judgment

#### Scenario: A consuming repository runs the same pin over its own tree
- **WHEN** a repository other than the one a disposition names is validated through the same pinned entrypoint
- **THEN** that disposition is neither applied to nor treated as stale by that run
- **AND** the repository's own findings are judged only against dispositions scoped to it

#### Scenario: A run passes with dispositions applied
- **WHEN** every blocking finding is covered and the run succeeds
- **THEN** the output names each applied exception with its reason, citations and granting authority
- **AND** the result is NOT reported as a clean tree, the tree not being clean
