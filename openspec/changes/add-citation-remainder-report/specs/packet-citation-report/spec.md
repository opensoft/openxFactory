# packet-citation-report Specification Delta

This delta is ALL-`ADDED` over a NEW capability, and that is a MEASURED CHOICE
rather than a style. The two capabilities a citation report could plausibly have
been folded into are each closed by a promoted sentence of their own.
`doc-health`'s *Deterministic check families* enumerates *"twenty-three check
families"* and names them, and *The family enumeration is derived, not restated
on trust* makes the suite refuse a restatement that *"omits a registered family,
names an unregistered one, or carries a numeral inconsistent with the registry
in its own tree"* — so a twenty-fourth family is a `## MODIFIED Requirements`
block over that whole enumeration, and OpenSpec `MODIFIED` replaces wholesale.
`proposal-origin`'s own text fixes *"The family's finding classes are therefore
SEVEN, named: …"*, so an eighth class is equally a MODIFIED block, over a
requirement about proposal ORIGINS carrying a class about CITATIONS.

A NEW capability directory owes neither. Every requirement below is `## ADDED`
over a title that appears nowhere else in this corpus, so no promoted byte
moves, no `Modified over`, `Removed from canon by` or `Merged into` marker is
owed, and `sequenced_after:` is the POSITIVE root claim `[]` rather than a
dependency on any active change's MODIFIED block.

**WHAT THIS CAPABILITY IS NOT.** It is not a gate, it is not a doc-health
family, and it is not an editor. `release-realization`'s promoted *A packet
reference resolves by identity, not by path* is the RULE; `scripts/packet_reference.py`
is that rule's shipped resolver; `scripts/validate-pin-registrations.py`'s
`check_citations` is the one GATE that consumes it, over one field of registered
pins. This capability adds the REPORT that has never existed: a corpus-wide
reading of what the rule still cannot resolve. It consumes the resolver and
changes nothing about it.

## ADDED Requirements

### Requirement: The citation remainder is reported
A repository adopting this capability SHALL produce a CORPUS-WIDE REPORT of
every `openspec/changes/…` citation its resolution rule cannot resolve, and the
report SHALL state, for every reading it takes, the repository head it was taken
at. A resolution rule whose remainder nobody reads is a rule whose coverage
nobody can know; the rule's own consumer resolves a few dozen referents of one
registered field, and the corpus carries hundreds.

THE REPORT SHALL COUNT BOTH TOKENS AND IDENTITIES, and SHALL NOT report one in
place of the other. A remainder TOKEN is one distinct citation string; a
remainder IDENTITY is one packet id that at least one remainder token addresses.
These are different quantities and the difference is large: in the tree this
capability was measured against, 74 identity-half tokens collapsed onto 48
identities, one identity carrying six tokens, because a trailing slash, a
directory citation and a file citation under it are three tokens naming one
packet. A reader repairs identities, so a report that prints only tokens
overstates the work by the ratio of one to the other, and a report that prints
only identities hides how many records mention each.

THE REPORT SHALL NAME THE CITING FILES of every remainder entry. A dangling
citation is a fact about a RECORD, not about a packet, and a reader who cannot
see which record carries it cannot act on it at all.

THE REPORT SHALL REPORT EVERY OUTCOME THE RESOLUTION RULE RETURNS, AND SHALL
NAME THEM AS THE RULE NAMES THEM. A rule that distinguishes a reference which
RESOLVED, one which is DANGLING, one which is AMBIGUOUS and one which was NOT A
PACKET REFERENCE at all has made four different statements, and a report that
collapses them has thrown away the distinction its own remainder is defined by.
The report SHALL ITEMIZE the DANGLING outcome — separately for each half the
rule reports, because the rule's own contract is that a failure says WHICH HALF
failed and the two halves want different repairs — and SHALL ITEMIZE the
AMBIGUOUS outcome. It SHALL COUNT, without itemizing, the outcomes that owe
nobody anything: RESOLVED, with the count of those that resolved somewhere other
than the path they were spelled as reported within it, because that count is the
rule working and is the one figure a reader weighing whether the rule earns its
keep needs; and NOT A PACKET REFERENCE, which is a statement about the caller's
own path resolution and not about any packet.

AND THE AMBIGUOUS COUNT SHALL BE PRINTED EVEN WHEN IT IS ZERO. It is the only
outcome that indicts a DECLARATION rather than a citation — two packets claiming
one identity is a defect in the claims, not in the record that cites them — and
a report that omits the row when the count is zero teaches its readers not to
look for it, so its absence and its zero become indistinguishable.

#### Scenario: The report is taken over a corpus
- **WHEN** the report runs against a repository root
- **THEN** it MUST print the head the reading was taken at
- **AND** it MUST print the number of tracked ENTRIES in scope and the number of FILES it read, the number of distinct citation tokens, the remainder in TOKENS and the remainder in IDENTITIES
- **AND** every remainder entry MUST name the files that cite it

#### Scenario: One identity is cited by several tokens
- **WHEN** two or more remainder tokens address the same packet identity
- **THEN** the identity MUST be counted ONCE in the identity total
- **AND** each token MUST still appear in the itemized remainder
- **AND** the report MUST NOT present the token total as a count of packets

#### Scenario: No identity in the corpus is claimed by two packets
- **WHEN** the report runs and the resolution rule returns no AMBIGUOUS outcome
- **THEN** it MUST print the AMBIGUOUS count as zero rather than omit the row
- **AND** it MUST print the DANGLING count for each half, and the RESOLVED and NOT-A-PACKET-REFERENCE counts, in the same reading
- **AND** a reader MUST NOT be able to mistake an omitted outcome for a measured zero

### Requirement: The reported population is derived from a stated recipe
The report's FILE POPULATION and TOKEN GRAMMAR SHALL be stated in this
specification and not left to the implementation, because a figure whose recipe
lives only in code cannot be reproduced by hand and therefore cannot be checked.
Two readings taken by different recipes are not comparable, and this capability
exists to produce a SERIES.

AND THE POPULATION SHALL BE REPORTED AS TWO NUMBERS, NEVER ONE. A report that
skips entries it counted has two different populations — the tracked ENTRIES the
exclusions leave, and the FILES it actually read and tokenized — and a single
"files in scope" figure is ambiguous between them by exactly the number of
entries skipped. The report SHALL state BOTH, labelled, and SHALL NOT present
either as the other; a reader reproducing a published figure can then tell which
one they are reproducing, and an implementation that skips a different set of
entries is visible in the gap between them rather than hidden inside one
number.

A TRACKED ENTRY THAT IS NOT A FILE SHALL BE SKIPPED AND SHALL CONTRIBUTE NO
TOKEN. A repository's tracked-entry listing names submodule links as well as
files; a link is a directory, it has no text, and counting one as an unreadable
file both misstates the population's size and invites an implementation to
recover text from it. Skipping it is also the population's half of the rule that
nothing cross-repository is resolved.

A TRACKED ENTRY WHOSE PATH LEAVES THE REPOSITORY ROOT ONCE RESOLVED SHALL BE
SKIPPED TOO, AND THE POPULATION RULE SHALL SAY SO RATHER THAN LEAVE IT TO THE
IMPLEMENTATION. A tracked entry may be a SYMBOLIC LINK, and the ordinary
"is this a file?" test follows the link and answers about its TARGET — so an
implementation that asks only that question reads whatever the link points at,
including a file outside this repository, and reports text that is not this
corpus's as this corpus's citations. The report SHALL therefore admit a link's
text ONLY after resolving the entry and finding it still inside the repository
root, and SHALL skip it otherwise. This is not a new boundary: it is the
containment test the RESOLUTION RULE ITSELF already applies to every path it
touches — resolve the path, then require it to stay under the root — and the
population owes the same test for the same reason, since a reader cannot
distinguish a citation this repository wrote from one it merely links to.

THE FILE POPULATION SHALL BE the repository's tracked files, less three
exclusions, each excluded for a stated reason: the ARCHIVED corpus
(`openspec/changes/archive/`), because an archived packet is frozen record whose
citations may not be repaired; the TEST corpus (`tests/`), because fixtures
deliberately carry synthetic ids and deliberately-absent files; and SPEC KIT
FEATS (`specs/`), because they are another tool's artifacts citing packets
illustratively. An implementation MAY let a caller refine the population, and
the report SHALL then state both the population it actually used AND the
refinements it was given, because a reading taken over a different population is
not a later point in the same series and a reader who cannot see the difference
will treat it as one.

THE REPORT'S OWN OUTPUT SHALL BE EXCLUDED FROM THE POPULATION wherever that
output is committed into the repository. A report that lists remainder citations
writes one citation token per remainder line, so a committed report is read by
the next run as a record citing every packet it reported on — the report
counting its own output, and the series it produces drifting upward by its own
act. The exclusion SHALL be declared BEFORE any such output is committed and not
after the first inflated reading.

AND NO REFINEMENT A CALLER SUPPLIES SHALL RE-ADMIT IT. The output exclusion is
not one of the defaults a caller refines: a report that admits refinements SHALL
either preserve that exclusion under every one of them or REFUSE a refinement
naming the output path, and SHALL NOT produce a reading in which the report
counted its own output. The refinement surface exists so a reader can ask a
narrower question, and the one thing it may not do is switch the self-counting
back on — a loop this requirement prevents is not prevented if any caller can
lift it with a flag.

THE TOKEN GRAMMAR SHALL BE STATED, AND EVERY NORMALIZATION IT APPLIES SHALL BE
PRINTED rather than applied silently. A citation extracted from free text
carries the punctuation of the prose around it: a trailing `/` on a directory
citation, a trailing full stop that ended a sentence, a trailing `-` where a
source line or an implicit string concatenation split the path across two lines.
A report that silently repaired these would be reporting its own grammar as a
property of the corpus; a report that silently kept them would report a record
as defective for a fact about a regular expression. The report therefore
normalizes, states which normalization it applied to which token, and treats a
token it cannot complete — one severed mid-path — as `truncated` rather than
resolving it as though it were whole.

THE EXTRACTION PATTERN ITSELF SHALL BE WRITTEN IN THIS SPECIFICATION AND NOT
ONLY DESCRIBED BY ITS EFFECTS. A requirement that promises a stated grammar and
then states only what the grammar is afterwards corrected for has not stated it:
two implementations can honour every normalization above and still extract
different tokens, and their remainders are then incomparable for a reason
neither report can show. The pattern is
`openspec/changes/[A-Za-z0-9][A-Za-z0-9._\-/]*`, applied to the TEXT of every
file in the population; the normalizations above are applied to each match, and
the matches are deduplicated afterwards.

AND THE THREE CHOICES THAT DECIDE WHICH NUMBER THE REPORT PRINTS SHALL BE FIXED
IN THIS SPECIFICATION AND DECLARED IN EVERY READING'S HEADER. They are choices
and not details: on the corpus this capability was measured against they
separate three honest readings of one tree by eight points of remainder, and the
recipe that produced the earliest of those readings stated none of them.
**(1) NORMALIZATION HAPPENS BEFORE DEDUPLICATION**, so one citation spelled both
with and without a trailing separator is ONE token and not two.
**(2) THE NOT-A-PACKET-REFERENCE OUTCOME SITS OUTSIDE THE REMAINDER** and is
counted beside it: it is the rule handing a path back to its caller, never a
citation the rule failed on, and counting it inside reports a caller's own path
resolution as this corpus's unresolved citation.
**(3) A TOKEN CITED IN SEVERAL PLACES CARRIES THE CROSS-REPOSITORY FLAG WHERE
ANY ONE OCCURRENCE CARRIES THE SIGNAL**, not only where every occurrence does. A
suspicion is a reason for a reader to look and one qualified occurrence is that
reason; requiring all of them switches the flag off precisely where a citation
is spelled several ways, which is the case the flag exists for.
A READING THAT APPLIED A DIFFERENT CHOICE SHALL NOT BE PRESENTED AS A LATER
POINT IN THE SAME SERIES.

#### Scenario: Some tracked entries in scope are not files
- **WHEN** the population's exclusions leave tracked entries that the report skips because they are not files it can read
- **THEN** the report MUST state the number of tracked ENTRIES in scope and the number of FILES it read, separately and labelled
- **AND** it MUST NOT report either number as the other

#### Scenario: A tracked entry is a link whose target leaves the tree
- **WHEN** a tracked entry is a symbolic link whose target, once resolved, stands outside the repository root
- **THEN** the report MUST skip the entry and take no token from it
- **AND** it MUST NOT report text read from outside the root as a citation carried by this corpus

#### Scenario: A citation is followed by sentence punctuation
- **WHEN** a citation token is extracted with a trailing full stop that ended the sentence carrying it
- **THEN** the report MUST resolve the token without the full stop
- **AND** it MUST record that the normalization was applied
- **AND** it MUST NOT report the record as carrying a dangling citation

#### Scenario: A citation is severed across two source lines
- **WHEN** a citation token ends in `-` because the path continued on the next line or in the next concatenated string literal
- **THEN** the report MUST class the token `truncated`
- **AND** it MUST NOT resolve the severed token as if it were a complete citation

#### Scenario: A reading is compared against an earlier reading
- **WHEN** a reading of the remainder is presented beside an earlier reading of the same corpus
- **THEN** each reading MUST state the extraction pattern and the three fixed choices it applied
- **AND** a reading that applied a different pattern or a different choice MUST NOT be presented as a later point in the same series

#### Scenario: The report's own output is committed into the corpus
- **WHEN** a repository commits the remainder report into its own tree
- **THEN** the committed report's path MUST be excluded from the file population
- **AND** the exclusion MUST be in force in the same change that first commits it

#### Scenario: A caller's refinement names the report's own output
- **WHEN** a caller passes a population refinement that would re-admit the committed report
- **THEN** the report MUST either keep its own output excluded or refuse the refinement
- **AND** it MUST NOT publish a reading that counted its own output

### Requirement: A suspected cross-repository citation is flagged and never dropped
A citation this repository judges to address ANOTHER repository's packet SHALL
be FLAGGED as suspected and SHALL remain in the reported population, and SHALL
NOT be removed from it. This tree cannot resolve another tree: the resolver
holds no repository vocabulary and no module-level root, so *"the same reference
answers differently against two roots"*, and a reading that removed a token on
that basis would be asserting a fact it cannot check.

THE SUSPICION IS A HEURISTIC AND SHALL BE REPORTED AS ONE. The signals are
adjacency signals — a path-joined prefix naming another repository, a forge URL
naming another repository, a qualifier word near the token, a locator scheme
whose own prefix names another repository, a trailing parenthetical naming a
repository — and the window in which they are looked for SHALL be stated. The
signal set SHALL be stated with it, because a repository that writes its
cross-repository citations in a locator scheme of its own has a signal no
adjacency word supplies, and a report that omits that scheme misses the class it
was written to catch. **THE WINDOW AND THE SIGNAL SET ARE PROPERTIES OF THE
CAPABILITY AND NOT OF A RUN**: both SHALL be FIXED, both SHALL be CLOSED, and
the report SHALL NOT offer a caller an option that varies either, because a
suspicion whose reach moves between runs makes two readings of one corpus
disagree for a reason neither reading records. What neither can move is the
HEADLINE: the requirement below fixes that as the INCLUSIVE remainder, so a
disagreement about the window changes which entries carry a flag and what the
filtered count beside the headline reads, and never the series itself. A citation whose qualifier sits outside that window is a MISS
and a paragraph that merely mentions another repository above an in-tree
citation is a FALSE POSITIVE; both are inevitable, which is precisely why the
verdict is a flag and not a deletion.

THE HEADLINE REMAINDER SHALL BE THE INCLUSIVE ONE, with the cross-repository
reading printed BESIDE it rather than substituted for it. The inclusive number is
the one every earlier reading of this population reported, so substituting a
filtered number would break the only series the capability exists to produce.

#### Scenario: A citation carries a repository qualifier nearby
- **WHEN** a remainder citation has a cross-repository signal within the stated window
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** the entry MUST still be counted in the inclusive remainder
- **AND** the report MUST print the filtered count beside the inclusive one, never instead of it

#### Scenario: The qualifier sits outside the window
- **WHEN** a citation names another repository further from the token than the stated window reaches
- **THEN** the report MUST leave the entry unflagged
- **AND** the report MUST state the window it used, so a reader can see why

### Requirement: The report classifies only what it can decide mechanically
The report SHALL assign a class to a remainder entry ONLY where the evidence is
a fact about a PATH or about the report's own normalization, and SHALL class
every other entry `unclassified`. A class that requires reading what a record
INTENDED — whether a citation is an illustrative example in a docstring, whether
an id ever existed, whether a name was renamed before renames were tracked,
whether a draft-named file was since finalized — is a human's, and a report that
guessed would put its guesses into the series a later gate is measured against.

THE CLASS VOCABULARY SHALL BE CLOSED AND NAMED IN THIS SPECIFICATION, and an
implementation SHALL NOT add a member to it or rename one. It is `truncated` —
a token the extraction severed mid-path; `punctuation-stripped` — a token whose
trailing prose punctuation the report removed; `fixture-path` — an entry every
occurrence of which stands where this corpus keeps fixtures and worked examples;
and `unclassified`. Labels are what two readings are compared by, so a report
whose labels differ from another's cannot be a later point in its series, and
the series is the whole reason a class is asserted at all.

AND A FLAG IS NOT A CLASS, AND SHALL BE CARRIED IN A FIELD OF ITS OWN. A
suspicion the report reports without asserting — a suspected cross-repository
citation above all — SHALL NOT be written into the class field, SHALL NOT
displace the class an entry's own evidence supports, and SHALL NOT be counted in
any class total. An entry carries exactly one class and any number of flags, and
a reader summing the classes SHALL find every remainder entry counted once.

AND WHERE AN ENTRY'S EVIDENCE SUPPORTS MORE THAN ONE CLASS, THE ONE ABOUT THE
REPORT'S OWN NORMALIZATION SHALL WIN over the one about a LOCATION. A token the
report itself severed or stripped is a fact about the TOOL, and filing it under
where it happened to be written would attribute the tool's own grammar to a
record. The precedence SHALL be stated with the vocabulary so that two readings
classify one entry the same way.

`unclassified` SHALL NOT be treated as a defect of the report. It is the report
declining to assert what it cannot see, and an implementation SHALL NOT reduce
the `unclassified` count by widening a mechanical class to cover a judgment.

AND NOTHING IS REPAIRED. A reference that resolves owes the citing record no
edit — that rule is already promoted, and this requirement states its other
half: **a reference that does NOT resolve owes the citing record no edit FROM
THIS REPORT EITHER.** The report SHALL NOT propose a corrected spelling, SHALL
NOT emit a patch, and SHALL NOT edit any file it reads. A reader that offers a
correction has become an editor, and several entries in a real remainder are
dangling by their own file's design — scope-isolation fixtures whose cited file
is deliberately absent, and docstring examples that must stay unresolvable to
illustrate what unresolvable means.

#### Scenario: The evidence is a path fact
- **WHEN** a remainder entry's class follows from the citing file's location or from a normalization the report applied
- **THEN** the report MUST assign that class
- **AND** it MUST name the evidence, so a reader can check it

#### Scenario: An entry carries a suspicion and a class at once
- **WHEN** a remainder entry is flagged as suspected cross-repository and its own evidence supports a class
- **THEN** the flag MUST be carried in its own field and the class field MUST keep the class the evidence supports
- **AND** the flag MUST NOT be counted in any class total

#### Scenario: Two classes fit one entry
- **WHEN** an entry's evidence supports both a class about the report's own normalization and a class about a location
- **THEN** the report MUST assign the normalization class
- **AND** it MUST NOT report the entry under the location class instead

#### Scenario: The evidence is a fact about intent
- **WHEN** deciding a remainder entry's class would require judging what the citing record meant
- **THEN** the report MUST class the entry `unclassified`
- **AND** it MUST NOT infer the class from the citation's spelling

#### Scenario: A dangling citation is found
- **WHEN** the report finds a citation that resolves to nothing
- **THEN** it MUST report the citation, its half, its identity and its citing files
- **AND** it MUST NOT propose a corrected spelling, emit a patch, or modify any file

### Requirement: The citation remainder report is advisory and gates nothing
The report SHALL exit successfully whatever it finds, and SHALL NOT provide an
option that makes a finding fail a run. Nothing in the reported population has
been ruled a defect: it is prose, docstrings, fixtures, other repositories'
packets and a handful of genuinely stale references, mixed, and a tool able to
exit non-zero acquires the meaning of a gate the first time anybody wires it
into a required check.

A NON-ZERO EXIT SHALL MEAN THE REPORT COULD NOT RUN, never that it found
something. The two are different facts wanting different repairs — an unreadable
tree is fixed by fixing the tree, a dangling citation by a judgment nobody has
made — and reporting them under one code sends a reader to the wrong one.

PROMOTING THE REPORT TO A GATE SHALL BE A SEPARATE ACT ON A SEPARATE WORD, and
the severity decision SHALL follow a measurement of the population the gate
would refuse rather than precede it. That ordering is not invented here: it is
the rule this estate's own check-family capability already states for its own
launches, and two of its families have walked it.

#### Scenario: The report finds a remainder
- **WHEN** the report runs and finds any number of unresolvable citations
- **THEN** it MUST exit successfully
- **AND** it MUST NOT offer an option that converts the finding into a failure

#### Scenario: The report cannot run
- **WHEN** the tree cannot be read, or the root is not a repository the report can walk
- **THEN** it MUST exit non-zero
- **AND** it MUST say that it did not run, rather than reporting an empty remainder

#### Scenario: Somebody proposes to gate on the remainder
- **WHEN** a change proposes to refuse a run on the citation remainder
- **THEN** that change MUST carry its own ruling
- **AND** it MUST cite a measurement of the population the gate would refuse, taken before the decision
