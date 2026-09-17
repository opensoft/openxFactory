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

AND THE HEAD ALONE DOES NOT NAME A READING: THE REPORT SHALL STATE, BESIDE THE
HEAD, WHETHER THE TRACKED CONTENT IT READ STANDS UNMODIFIED AT THAT HEAD, and a
reading taken over content that differs from its printed head SHALL NOT be
presented as a later point in that series. The population below is the
repository's tracked entries read AS THEY STAND — which is what the containment
test on a link demands and what no stored blob could answer — so an uncommitted
edit to one tracked file moves the counts while the printed head does not move,
and two readings that disagree for that reason are indistinguishable to a reader
who has only the head between them. This is the rule the population's
refinements already owe, stated for the same reason and at the same cost: a
reading taken over something other than the default is still produced, still
useful, and still not a later point in the same series. IT IS A DECLARATION AND
NOT A REFUSAL. A tree carrying uncommitted work is a tree the report can read,
the scheduled reading is taken on a clean checkout in any case, and the only
non-zero exit this capability has is the one for a report that could not run at
all.

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

AND A REMAINDER ENTRY IS A TOKEN — never an identity, and never the TRACKED
ENTRY the population below is counted in: THE REPORT SHALL CARRY ONE REMAINDER
ENTRY PER REMAINDER TOKEN, one record each in whatever form a reading is emitted
in; an entry's class and its flags SHALL be properties of THAT TOKEN; the report
SHALL NOT merge two tokens' classes because they address one identity; grouping
by identity SHALL NEST the entries beneath the identity they address, changing
the ORDER a reading lists things in and never what is listed; and every CLASS
TOTAL SHALL therefore be a count of TOKENS, any count taken over identities
being labelled as the identity count it is. `entry` is the word the requirements
below name, count and classify with, and the two units it could mean answer
differently wherever one identity is spelled several ways — the identity above
carrying six tokens is this corpus's extreme: a report reading the unit as an
identity would have to choose ONE class for a packet cited once as a severed
token and once whole, and its class totals would not sum with the totals of a
report that kept them apart.

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

#### Scenario: The tree read is not clean at the head printed
- **WHEN** the report runs over a working tree whose tracked content differs from the head it prints
- **THEN** it MUST state, beside that head, that the content it read stands modified at it
- **AND** the reading MUST NOT be presented as a later point in the series taken at that head
- **AND** the report MUST still produce the reading rather than refuse to run

#### Scenario: One identity is cited by several tokens
- **WHEN** two or more remainder tokens address the same packet identity
- **THEN** the identity MUST be counted ONCE in the identity total
- **AND** each token MUST still appear in the itemized remainder
- **AND** the report MUST NOT present the token total as a count of packets

#### Scenario: One identity's tokens carry different classes
- **WHEN** two remainder tokens address one identity and each token's own evidence supports a different class
- **THEN** the report MUST carry one entry per token, each keeping the class its own evidence supports
- **AND** it MUST NOT merge the two into one entry or one class because they share an identity
- **AND** the class totals MUST count both tokens

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

AND A FILE THE REPORT CANNOT DECODE AS TEXT SHALL BE SKIPPED, COUNTED AND
REPORTED, NEVER REPLACEMENT-DECODED AND NEVER FATAL. A repository may track a
binary file or a file that is not valid UTF-8, and three realizations could
replacement-decode it, skip it silently, or abort on it — producing three
readings of one tree that are not comparable, which is the one thing this
capability cannot afford. The report SHALL decode each file in the population
strictly; a file that does not decode SHALL contribute no token, SHALL NOT be
read with character replacement (bytes that are not text can yield matches that
no record wrote), SHALL NOT end the run, and SHALL be counted in a stated
SKIPPED total. The population arithmetic SHALL therefore close: the tracked
ENTRIES in scope equal the FILES read, plus the entries skipped as non-files,
plus the files skipped as undecodable.

AND THAT CLOSURE NAMES TWO SKIP TERMS WHERE THIS POPULATION RULE HAS THREE: AN
ENTRY SKIPPED BECAUSE ITS PATH LEAVES THE REPOSITORY ROOT ONCE RESOLVED SHALL BE
COUNTED AND REPORTED IN A SKIP TERM OF ITS OWN. The containment rule below skips
such an entry, and a SYMBOLIC LINK IS A TRACKED FILE — it is not the submodule
link the non-file term is about, which *is* a directory and has no text, and it
never reaches a decoder, so it belongs to neither of the two terms named above
and an arithmetic offering only those two has nowhere to put it. THE COMPLETE
IDENTITY SHALL THEREFORE BE: the tracked ENTRIES in scope equal the FILES read,
plus the entries skipped as non-files, PLUS THE ENTRIES SKIPPED AS LINKS LEAVING
THE REPOSITORY ROOT, plus the files skipped as undecodable. **AND THAT TERM
SHALL BE PRINTED EVEN WHERE IT IS ZERO**, for the reason the AMBIGUOUS row is
printed at zero: a term omitted whenever nothing lands in it teaches its readers
not to look for it, and this is the term whose non-zero value means the report
DECLINED to read text a naive implementation would have reported as this
corpus's. Folding it into the non-file term instead would close the arithmetic
and hide the one thing a reader needs from it, because a tree carrying no links
and a tree whose links were all refused would then print the same number. A
READING WHOSE ARITHMETIC DOES NOT CLOSE SHALL NOT BE PRESENTED AS A LATER POINT
IN THE SERIES: a population a reader cannot re-add is a population a reader
cannot reproduce.

#### Scenario: A tracked file in the population is not valid text
- **WHEN** a file in the population cannot be decoded as UTF-8
- **THEN** the report MUST skip it and take no token from it
- **AND** it MUST count it in the skipped total it states, rather than in the files it read
- **AND** it MUST NOT read the file with character replacement and MUST NOT end the run

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

AND WHERE A REPORT ADMITS REFINEMENTS, THEIR SEMANTICS SHALL BE THESE THREE AND
SHALL NOT BE A REALIZATION'S: A REFINEMENT'S PREFIX SHALL MATCH ON PATH-SEGMENT
BOUNDARIES; A REFINEMENT THAT ADMITS SHALL RE-ADMIT INTO THE STATED POPULATION
RATHER THAN REPLACE IT; AND A REFINEMENT THAT REMOVES SHALL BE APPLIED LAST AND
SHALL WIN over any admission naming the same path. A refinement surface named
without its semantics is a surface two realizations implement differently, and
each of these three decides which number the report prints — which is the one
thing a capability that exists to produce a SERIES cannot leave open.
**A PREFIX MATCHES ON SEGMENT BOUNDARIES** — a path matches where it EQUALS the
prefix with any trailing `/` removed, or begins with that plus `/` — because a
bare string prefix swallows a sibling directory whose name merely begins the
same way, and the population would then differ between two readings by a
directory neither reader named. **ADMISSION RE-ADMITS AND DOES NOT REPLACE**: a
caller asking after one excluded fixture corpus asks for it BESIDE the stated
population, and a refinement that replaced the population would let a reading
over three files be published in the shape of a reading over the corpus, which
is the opposite of what narrowing a question means. **REMOVAL IS APPLIED LAST
AND WINS**, so the pair is order-independent: a reader predicts the population
without knowing which refinement was given first, and a wrapper that appends a
removal cannot have it undone by an admission written earlier. A FOURTH RULE
GOVERNS THE ONE PATH NO REFINEMENT MAY REACH — the report's own output — and it
stands in the two paragraphs below rather than among these three.

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

AND A TRAILING HYPHEN IS A SUSPICION, NOT A VERDICT: RESOLUTION SHALL BE TRIED
FIRST AND A TOKEN THAT RESOLVES SHALL NEVER BE CLASSED `truncated`. The
repository's own change-id grammar admits an identifier that ends in `-`, so a
report that classed every such token as severed would suppress a VALID citation
as an artifact of its own regular expression, and the suppression would be
invisible — the entry would neither resolve nor appear as a defect of the
record. The order is therefore fixed: resolve, and class `truncated` only where
the token does not resolve.

AND THE HYPHEN IS NOT THE ONLY CHARACTER THAT RULE OWES: RESOLUTION SHALL BE
TRIED FIRST BEFORE ANY TRAILING CHARACTER THE CHANGE-ID GRAMMAR ADMITS IS
STRIPPED, AND A TOKEN THAT RESOLVES AS EXTRACTED SHALL BE REPORTED AS IT
RESOLVED, SHALL CARRY NO NORMALIZATION RECORD AND SHALL TAKE NO NORMALIZATION
CLASS. The safeguard above names ONE character while the normalization above
strips more than one, so a rule written for `-` alone leaves another strip free
to do exactly what the safeguard exists to prevent. THE PREDICATE SHALL
THEREFORE BE THE GRAMMAR'S AND NOT A LIST OF PUNCTUATION MARKS: this estate's
canonical change-id grammar is `[A-Za-z0-9][A-Za-z0-9._-]*`, which admits an
identifier ending in a letter, a digit, `.`, `_` or `-`, so a trailing FULL STOP
can be an identifier's own last character exactly as a trailing hyphen can, and
a report that stripped it unconditionally would rewrite a VALID packet id and
report the citing record as dangling — invisibly, and for a fact about a regular
expression rather than about the record. A TRAILING PATH SEPARATOR IS THE ONE
EXCEPTION, AND IT IS AN EXCEPTION BECAUSE THE GRAMMAR MAKES IT ONE: no
identifier may carry `/`, so stripping it can suppress no valid citation, and
its strip SHALL stay unconditional because the deduplication choice below
depends on it — a directory citation and its unslashed sibling are ONE token and
not two. A trailing character the grammar admits and this specification names no
normalization for SHALL simply be left where it stands. The rule is written
against the GRAMMAR so that it cannot fall behind one: a grammar that later
admits another character admits it to this safeguard in the same act.

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

#### Scenario: A link that leaves the root is counted where the arithmetic can find it
- **WHEN** the report skips a tracked entry because the entry's path, once resolved, leaves the repository root
- **THEN** it MUST count that entry in the skip term for entries skipped as links leaving the root, and in neither the non-file term nor the undecodable term
- **AND** the tracked ENTRIES in scope MUST still equal the FILES read plus all three skip terms
- **AND** the report MUST print that term even where its value is zero

#### Scenario: A tracked link stands inside the root
- **WHEN** a tracked entry is a symbolic link whose target, once resolved, still stands inside the repository root
- **THEN** the report MUST admit its text and take tokens from it as from any other file it reads
- **AND** it MUST count it among the FILES read and in no skip term

#### Scenario: A refinement's prefix has a sibling whose name begins the same way
- **WHEN** a refinement names a directory prefix and the tree also carries a sibling directory whose name begins with that prefix followed by more characters
- **THEN** the report MUST match the prefix on path-segment boundaries and leave the sibling unmatched
- **AND** it MUST NOT read the prefix as a bare string prefix

#### Scenario: A caller admits one excluded corpus
- **WHEN** a caller's refinement admits a prefix that one of the stated exclusions had removed
- **THEN** the report MUST read that prefix BESIDE the stated population rather than in place of it
- **AND** it MUST state the population it actually used and the refinement it was given

#### Scenario: Two refinements name one path
- **WHEN** one refinement admits a path and another removes it, in either order
- **THEN** the removal MUST be applied last and MUST win
- **AND** the population MUST NOT depend on the order the refinements were given in

#### Scenario: A citation is followed by sentence punctuation
- **WHEN** a citation token is extracted with a trailing full stop that ended the sentence carrying it
- **THEN** the report MUST resolve the token without the full stop
- **AND** it MUST record that the normalization was applied
- **AND** it MUST NOT report the record as carrying a dangling citation

#### Scenario: A citation is severed across two source lines
- **WHEN** a citation token ends in `-` because the path continued on the next line or in the next concatenated string literal
- **THEN** the report MUST class the token `truncated`
- **AND** it MUST NOT resolve the severed token as if it were a complete citation

#### Scenario: A citation ends in a hyphen the packet id actually carries
- **WHEN** a citation token ends in `-` and the token RESOLVES to a packet under the resolution rule
- **THEN** the report MUST report the resolved outcome
- **AND** it MUST NOT class the token `truncated`

#### Scenario: A citation ends in a full stop the packet id actually carries
- **WHEN** a citation token ends in `.` and the token RESOLVES to a packet under the resolution rule exactly as it was extracted
- **THEN** the report MUST report the resolved outcome
- **AND** it MUST NOT strip the full stop, MUST NOT record a normalization, and MUST NOT class the entry `punctuation-stripped`
- **AND** it MUST NOT report the citing record as carrying a dangling citation

#### Scenario: A citation ends in a character the grammar admits and no normalization names
- **WHEN** a citation token ends in a character the change-id grammar admits — a letter, a digit or `_` — that this specification names no normalization for
- **THEN** the report MUST resolve the token exactly as extracted
- **AND** it MUST NOT strip that character and MUST NOT class the entry under any normalization class

#### Scenario: A directory citation ends in a path separator
- **WHEN** a citation token ends in `/`, a character the change-id grammar admits in no identifier
- **THEN** the report MUST strip the separator whether or not the token resolves as extracted
- **AND** it MUST count the stripped token and its unslashed sibling as ONE token
- **AND** the resolve-first safeguard MUST NOT suppress that strip

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

THE SUSPICION IS A HEURISTIC AND SHALL BE REPORTED AS ONE, AND THE WINDOW AND
THE SIGNAL SET IN WHICH IT IS LOOKED FOR SHALL BE STATED HERE RATHER THAN LEFT
TO A REALIZATION. **THE WINDOW SHALL BE THE CITING LINE PLUS THE THREE LINES
ABOVE IT.** A check that reads only the citing line misses the citations that
name the other repository one to three lines above the bare path, which is the
largest known class in this population; three lines is a reach derived from that
observation and from nothing else, which is exactly why what it produces is a
FLAG and never a deletion. **THE SIGNALS SHALL BE THESE FIVE AND NO OTHERS**,
looked for inside that window:
**(1) A PATH-JOINED PREFIX** (`xFactories/LedgerxFactory/…`);
**(2) A GITHUB BLOB OR TREE URL**;
**(3) A BARE QUALIFIER WORD IMMEDIATELY BEFORE THE TOKEN** (`codexFactory
openspec/changes/…`);
**(4) THE `opsx:opensoft/…` CUSTODY-LOCATOR SCHEME THIS CORPUS WRITES
OpsxFactory CITATIONS IN** — a signal no adjacency word supplies, because a
repository that writes its cross-repository citations in a locator scheme of its
own carries the qualifier INSIDE the token rather than beside it, and a report
that omits that scheme misses the class it was written to catch;
**(5) A TRAILING `(RepoName)` PARENTHETICAL**.
**THE WINDOW AND THE SIGNAL SET ARE PROPERTIES OF THE
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

AND EACH SIGNAL'S MATCHING RULE SHALL BE FIXED HERE TOO, BECAUSE A SIGNAL NAMED
WITH AN EXAMPLE IS NOT A SIGNAL TWO REALIZATIONS MATCH THE SAME WAY. A window
that is fixed and a set that is closed still leave open every question that
decides whether a signal FIRES — which words are repository names, in which
case, where a forge URL ends, where a path-joined prefix begins, what may
decorate a bare word, and how close a parenthetical must stand — and a flag that
moves between realizations is a field two readings cannot be compared by, which
is the one thing this capability cannot afford.

**THE REPOSITORY-NAME VOCABULARY SHALL BE THE CLOSED SET NAMED HERE**, and it is
named here because this repository carries no machine-readable enumeration of
its siblings to read one from: this estate's repository IDENTIFIERS are defined
as the aggregation's `.gitmodules` submodule paths, and that file is not in this
tree; the only DECLARED repository vocabulary that is holds two names. The set
SHALL therefore be `codexFactory`, `OpsxFactory`, `LedgerxFactory`,
`openXwallet`, `hermes-install` and `xFactory-Hermes-Install` — the five estates
the measured cross-repository population belongs to, the last two being one
estate under the two spellings this corpus writes it in — and it SHALL be
CLOSED: an implementation SHALL NOT widen it, and a corpus needing a wider set
takes a RULING, exactly as the fixture-path location set does. **AND A
QUALIFIER NAMING THIS REPOSITORY SHALL FIRE NO SIGNAL**: `openxFactory` and
`opensoft/openxFactory` are this repository's own spellings, a citation
qualified by one of them is an IN-TREE citation, and the exclusion is not a
nicety — every trailing parenthetical of this shape measured in this corpus
names THIS repository.

**A NAME SHALL MATCH WITHOUT REGARD TO CASE.** Exact case is the rule this
corpus does not keep: measured over the population, one estate's name is written
in SIX different cases and another's is written in lower case MORE OFTEN than in
its canonical one, so an exact-case rule would drop about a sixth of the first
estate's occurrences and the majority spelling of the second. Case-insensitive
matching is also what this estate's own qualifier reader already does, and the
report SHALL NOT read a difference of case as a different repository.

**(1) THE PATH-JOINED PREFIX SHALL FIRE** where the citing line carries, ending
immediately before the token, a vocabulary name followed by `/`, the character
before that name being absent or NOT one of `A-Z`, `a-z`, `0-9`, `.`, `_` or
`-`. The name matched is the SEGMENT immediately before the token, so
`xFactories/LedgerxFactory/` fires on `LedgerxFactory` and a longer word that
merely ends in a vocabulary name fires nothing.

**(2) THE FORGE URL SHALL FIRE** where the token is immediately preceded on the
citing line by `http://` or `https://`, the host `github.com`, ONE owner
segment, ONE repository segment naming a vocabulary member, `/blob/` or
`/tree/`, ONE ref segment, and `/`. It is the REPOSITORY segment that is matched
and never the OWNER segment, because a transfer moves the owner segment alone
and a repository's own name is unchanged by one.

**(3) THE BARE QUALIFIER WORD SHALL FIRE** where a word inside the window — a
whitespace-delimited run, stripped at both ends of the decoration characters
`` ` ``, `'`, `"`, `“`, `”`, `(`, `)`, `[`, `]`, `{`, `}`, `<`, `>`, `,`, `;`,
`§`, `*` and `_`, and read without regard to case — is a vocabulary member: ON
THE CITING LINE the word IMMEDIATELY BEFORE the token, and ON EACH OF THE THREE
LINES ABOVE ANY word on the line, because "immediately before" names nothing on
a line the token does not stand on. This is the ONLY one of the five that can
fire off the citing line; the other four are relations to the token itself.

**(4) THE CUSTODY-LOCATOR SCHEME SHALL FIRE** where the token is immediately
preceded on the citing line by the literal scheme prefix `opsx:` followed by one
owner segment and `/`. The scheme names its repository ITSELF rather than by any
word, which is why it is in the set at all; and the same prefix followed by
anything other than an owner segment and a path — a command name, a subject, a
workflow locator — SHALL NOT fire it.

**(5) THE TRAILING PARENTHETICAL SHALL FIRE** where the characters immediately
following the token on the citing line are at most ONE space, then `(`, then a
vocabulary member under the decoration and case rules above, then `)`. More than
one space, any further content inside the parentheses, or a parenthetical that
is not the next thing after the token SHALL NOT fire it.

THE HEADLINE REMAINDER SHALL BE THE INCLUSIVE ONE, with the cross-repository
reading printed BESIDE it rather than substituted for it. The inclusive number is
the one every earlier reading of this population reported, so substituting a
filtered number would break the only series the capability exists to produce.

AND THE FILTERED COUNT PRINTED BESIDE THE HEADLINE SHALL BE DEFINED HERE RATHER
THAN LEFT TO A READING: IT SHALL BE THE REMAINDER WITH EVERY ENTRY CARRYING THE
CROSS-REPOSITORY FLAG REMOVED, COUNTED IN TOKENS, WITH ITS CORRESPONDING
IDENTITY COUNT PRINTED BESIDE IT AND LABELLED AS ONE. A filtered count named
without its unit and without its predicate is two numbers, and they differ by
exactly the quantity the flag exists to measure. The unit is the TOKEN, because
a remainder entry is a token and every class total above is a count of tokens;
AND AN IDENTITY LEAVES THE IDENTITY COUNT ONLY WHERE EVERY ONE OF ITS REMAINDER
TOKENS IS FLAGGED, because one unflagged token is a citation this tree still
answers for and the identity it addresses is still work a reader would do.
**AND THE ARITHMETIC SHALL BE PRINTED, IN TOKENS, SO THAT IT RECONCILES**: the
INCLUSIVE remainder EQUALS the FILTERED count PLUS THE NUMBER OF REMAINDER
ENTRIES CARRYING THE FLAG, and it is that last term the arithmetic row SHALL
print. **IT IS NOT THE NUMBER OF FLAGGED TOKENS IN THE CORPUS**, which is a
larger and a different quantity: a flagged citation whose raw path stands in
this tree never entered the remainder at all, so a row built on the corpus
figure subtracts a token the remainder never held and prints a filtered count
lower than the one the entries themselves give. The difference is measured
rather than feared — in the tree this capability was measured against, 22 tokens
carried the flag and 21 of them stood in the remainder — and a reader cannot
tell the two apart from a row that does not say which it printed. **AND THE
IDENTITY PAIR SHALL NOT BE PRESENTED AS SUMMING**: an identity carrying one
flagged token and one unflagged token is counted in the inclusive identity total
AND in the filtered identity total, so the identity figures are two labelled
readings of one population and never an arithmetic row.

#### Scenario: A citation carries a repository qualifier nearby
- **WHEN** a remainder citation has a cross-repository signal within the stated window
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** the entry MUST still be counted in the inclusive remainder
- **AND** the report MUST print the filtered count beside the inclusive one, never instead of it

#### Scenario: One identity's remainder tokens are part flagged and part not
- **WHEN** an identity is addressed by two remainder tokens and exactly one of them carries the cross-repository flag
- **THEN** the identity MUST stay in the filtered identity count
- **AND** the unflagged token MUST stay in the filtered token count and the flagged one MUST NOT
- **AND** the report MUST NOT present the inclusive and filtered identity counts as summing to a total

#### Scenario: Every one of an identity's remainder tokens is flagged
- **WHEN** every remainder token addressing one identity carries the cross-repository flag
- **THEN** the identity MUST leave the filtered identity count
- **AND** every one of those tokens MUST leave the filtered token count
- **AND** all of them MUST still be counted in the inclusive remainder

#### Scenario: The filtered reading is printed beside the inclusive one
- **WHEN** the report prints the filtered reading beside the inclusive headline
- **THEN** it MUST print the filtered count in TOKENS and its identity count beside it, each labelled with the unit it counts
- **AND** it MUST print the arithmetic in tokens, the inclusive remainder standing as the filtered count plus the number of REMAINDER ENTRIES carrying the flag
- **AND** it MUST NOT print the number of flagged tokens in the corpus as that term

#### Scenario: The qualifier sits outside the window
- **WHEN** a citation names another repository further from the token than the stated window reaches
- **THEN** the report MUST leave the entry unflagged
- **AND** the report MUST state the window it used, so a reader can see why

#### Scenario: The repository is named two lines above the citation
- **WHEN** a remainder citation's own line carries no signal and one of the five signals stands two lines above it
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** the entry MUST still be counted in the inclusive remainder

#### Scenario: The repository is named four lines above the citation
- **WHEN** the nearest signal stands four lines above the citing line
- **THEN** the report MUST leave the entry unflagged
- **AND** the report MUST NOT widen the window for that entry or for any other

#### Scenario: A path-joined prefix names another repository
- **WHEN** a citation inside the window is written with a path-joined prefix naming another repository
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** the entry MUST still be counted in the inclusive remainder

#### Scenario: A forge blob or tree URL carries the citation
- **WHEN** a citation inside the window appears in a GitHub blob or tree URL
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** the entry MUST still be counted in the inclusive remainder

#### Scenario: A bare qualifier word stands immediately before the token
- **WHEN** a citation inside the window is preceded immediately by a bare word naming another repository
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** the entry MUST still be counted in the inclusive remainder

#### Scenario: The citation is written in a custody-locator scheme
- **WHEN** a citation inside the window is written in a locator scheme whose own prefix names another repository
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** the report MUST NOT require an adjacent qualifier word before flagging it

#### Scenario: A trailing parenthetical names the repository
- **WHEN** a citation inside the window is followed by a parenthetical naming another repository
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** the entry MUST still be counted in the inclusive remainder

#### Scenario: A path-joined prefix stands on a name boundary
- **WHEN** the citing line carries a vocabulary repository name followed by `/` ending immediately before the token, and the character before that name is absent or is not a letter, a digit, `.`, `_` or `-`
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** it MUST match the segment immediately before the token, so an enclosing directory prefix does not prevent the match

#### Scenario: A longer word merely ends in a repository name
- **WHEN** the characters immediately before the token are a vocabulary name preceded directly by a letter, a digit, `.`, `_` or `-`
- **THEN** the report MUST NOT flag the entry on the path-joined signal
- **AND** it MUST NOT read a name character before the name as a boundary

#### Scenario: A forge URL names the repository in its own segment
- **WHEN** the token is immediately preceded on the citing line by a `github.com` URL whose repository segment names a vocabulary member and whose path continues through `/blob/` or `/tree/` and one ref segment
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** it MUST match the repository segment and MUST NOT require the owner segment to be a vocabulary member

#### Scenario: A forge URL names this repository
- **WHEN** the URL immediately before the token names THIS repository in its repository segment
- **THEN** the report MUST NOT flag the entry
- **AND** it MUST NOT read a forge URL alone, without a repository segment it recognizes, as a signal

#### Scenario: A decorated qualifier word stands immediately before the token
- **WHEN** the word immediately before the token on the citing line is a vocabulary name carrying emphasis, quotation or bracket decoration and spelled in a case other than the canonical one
- **THEN** the report MUST strip that decoration and match the name without regard to case
- **AND** it MUST flag the entry as suspected cross-repository

#### Scenario: The word before the token names a repository this specification does not
- **WHEN** the word immediately before the token is a repository name that is not a member of the vocabulary named here
- **THEN** the report MUST NOT flag the entry
- **AND** it MUST NOT widen the vocabulary to admit it

#### Scenario: The custody-locator prefix carries an owner segment
- **WHEN** the token is immediately preceded on the citing line by `opsx:` followed by one owner segment and `/`
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** it MUST NOT require an adjacent qualifier word

#### Scenario: The same scheme prefix introduces something that is not a locator
- **WHEN** `opsx:` is followed by a command name, a subject or a workflow locator rather than an owner segment and a path
- **THEN** the report MUST NOT flag the entry on that scheme

#### Scenario: A parenthetical follows the token with at most one space
- **WHEN** the characters immediately after the token on the citing line are at most one space, then parentheses containing only a vocabulary member
- **THEN** the report MUST flag the entry as suspected cross-repository
- **AND** the entry MUST still be counted in the inclusive remainder

#### Scenario: A parenthetical names this repository or stands further off
- **WHEN** the parenthetical after the token names this repository, or carries anything besides a vocabulary member, or is not the next thing after the token
- **THEN** the report MUST NOT flag the entry on the parenthetical

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

AND `truncated` SHALL CARRY A PREDICATE RATHER THAN A DESCRIPTION, CLOSED HERE
AS `fixture-path`'s IS: THE REPORT SHALL CLASS A REMAINDER ENTRY `truncated`
WHERE EVERY ONE OF ITS OCCURRENCES SATISFIES AT LEAST ONE OF THE THREE PROBES
NAMED BELOW, OR WHERE THE TOKEN ENDS IN `-` AND DOES NOT RESOLVE UNDER THE ORDER
THIS SPECIFICATION ALREADY FIXES — AND SHALL NOT CLASS IT `truncated` OTHERWISE.
"The extraction severed mid-path" describes what happened to a token; it is not
a test a realization can run, and two realizations reading it would assert this
class over different entries and publish class totals that do not compare. The
three probes are:
**(i) A LONGER PATH ON THE SAME LINE ENDS WITH THE TOKEN AND STANDS IN THIS
TREE** — the citation is that longer path and the token is only its tail,
because the extraction pattern is anchored on `openspec/changes/` and cannot
reach a head written before it. This is the probe the trailing-character rules
cannot reach at all: such a token is severed at its FRONT and carries no
punctuation to notice.
**(ii) THE CHARACTER IMMEDIATELY FOLLOWING THE TOKEN IS `<`** — the path
continues into a placeholder whose opening character the grammar admits nowhere,
so the extraction stopped short of the path's end rather than at it.
**(iii) THE TOKEN ENDS ITS SOURCE LINE INSIDE A STRING LITERAL, THE NEXT LINE
OPENS ONE, AND THE PATH REJOINED ACROSS THE TWO RESOLVES** — an implicit string
concatenation split one path across two source lines, and the rejoin is what
proves it rather than a reader's guess.
THE OCCURRENCE RULE IS **ALL**, NEVER **ANY**, for the reason `fixture-path`'s
is: an occurrence at which the token stands as the whole citation is a citation
this corpus really carries, and an entry carrying one is not an artifact of the
tool. THE THREE ARE THE MEASURED SET RATHER THAN AN AUTHOR'S LIST — together
they caught 4 of 4 hand-classified tokenization artifacts with ZERO false
positives — AND THEY ARE CLOSED: an implementation SHALL NOT add a probe, widen
one, or assert `truncated` on evidence none of them names, because a mechanical
class that grows a probe is a mechanical class quietly absorbing a judgment.

AND `punctuation-stripped` SHALL CARRY ITS FIRING CONDITION, WHICH IS NOT THE
SAME STATEMENT AS ITS DESCRIPTION: THE REPORT SHALL CLASS A REMAINDER ENTRY
`punctuation-stripped` WHERE IT STRIPPED A TRAILING CHARACTER FROM THE TOKEN
UNDER THE GRAMMAR'S NORMALIZATION, THE STRIPPED TOKEN STILL RESOLVED TO NOTHING,
AND THE `truncated` PREDICATE DID NOT FIRE — AND SHALL NOT CLASS IT
`punctuation-stripped` OTHERWISE. Each of the three conditions carries its
weight. **A TOKEN THAT RESOLVES IS NOT A REMAINDER ENTRY AND TAKES NO CLASS AT
ALL**: under the resolve-first rule above a token that resolves AS EXTRACTED
carries no normalization record either, and a token that resolves only once a
trailing character is stripped is reported as RESOLVED with that normalization
printed in its own row — so this class is asserted only where the strip was
tried, was not enough, and the entry stayed in the remainder, which is the case
in which the label tells a reader something: the punctuation was not the reason
the citation fails. **AND `truncated` WINNING IS THE PRECEDENCE THIS
SPECIFICATION ALREADY STATES**, spelled into the condition so that no
realization has to derive it. **AND THE CLASS HAS NO MEMBER IN THE TREE THIS
CAPABILITY WAS MEASURED AGAINST**, which is a fact about that corpus and not a
defect of the vocabulary: the one sentence-terminal full stop measured there
sits on a token that RESOLVES once the stop is gone, so it never entered the
remainder. A closed vocabulary may hold a member with no member today; what it
may not hold is a member with no firing condition, which is an invitation for
two realizations to fill it differently and call the results one series.

AND `fixture-path` SHALL CARRY A PREDICATE RATHER THAN A DESCRIPTION, CLOSED
HERE: THE REPORT SHALL CLASS AN ENTRY `fixture-path` WHERE EVERY ONE OF ITS
OCCURRENCES STANDS UNDER THE TOP-LEVEL `examples/` TREE, UNDER
`ideation/dashboard/gate-records/`, UNDER AN `examples/` DIRECTORY BELOW
`contracts/`, OR UNDER A `tests/` DIRECTORY NESTED BENEATH THE POPULATION'S OWN
TOP-LEVEL `tests/` EXCLUSION — AND SHALL NOT CLASS IT `fixture-path` WHERE ANY
ONE OCCURRENCE STANDS ANYWHERE ELSE. "Where this corpus keeps fixtures and
worked examples" is a description, and two realizations reading it would assert
this class over different entries; a class total read differently is a series
read differently, and this is a class a later gate would be measured against.
The set is the MEASURED one rather than an author's list — it is the probe that
caught 17 of 18 hand-classified fixture entries with ZERO false positives, with
the nested-`tests/` location carrying the entries whose citing test ASSERTS the
cited file's absence — and it is CLOSED: an implementation SHALL NOT widen it,
because a widened location set is how a mechanical class quietly absorbs a
judgment. AND THE OCCURRENCE RULE IS **ALL**, NEVER **ANY**: one occurrence
outside every named location is a citation carried by ordinary prose, and an
entry carrying one takes whatever other mechanical class its evidence supports,
or `unclassified`.

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

AND WHERE TWO NORMALIZATION CLASSES BOTH FIT ONE ENTRY, `truncated` SHALL WIN
OVER `punctuation-stripped`. The order is not a new one: the grammar above
already strips a token's trailing prose punctuation BEFORE resolution is tried,
and already classes a token `truncated` ONLY WHERE IT DOES NOT RESOLVE — so a
token spelled `…-.` is stripped, tried, and, where the stripped token still
resolves to nothing, SEVERED, which is the later verdict and the stronger
statement. Filing it under the strip instead would report the repair the tool
made and hide that the path is incomplete, sending a reader to look for a
missing packet where the citation is missing its own tail. Nothing is lost by
the precedence: every normalization the report applied is reported in the
entry's own normalization record whatever class the entry lands in.

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

#### Scenario: Every occurrence of an entry stands in a fixture location
- **WHEN** every occurrence of a remainder entry stands under one of the fixture locations this specification names
- **THEN** the report MUST class the entry `fixture-path`
- **AND** it MUST name those occurrence locations as the evidence

#### Scenario: One occurrence of an entry stands outside the fixture locations
- **WHEN** a remainder entry has occurrences in a named fixture location and one occurrence outside every one of them
- **THEN** the report MUST NOT class the entry `fixture-path`
- **AND** it MUST class the entry under whatever other mechanical class its evidence supports, or `unclassified`

#### Scenario: An entry carries a suspicion and a class at once
- **WHEN** a remainder entry is flagged as suspected cross-repository and its own evidence supports a class
- **THEN** the flag MUST be carried in its own field and the class field MUST keep the class the evidence supports
- **AND** the flag MUST NOT be counted in any class total

#### Scenario: Two classes fit one entry
- **WHEN** an entry's evidence supports both a class about the report's own normalization and a class about a location
- **THEN** the report MUST assign the normalization class
- **AND** it MUST NOT report the entry under the location class instead

#### Scenario: A token is both stripped and severed
- **WHEN** a token ends in `-.`, the report strips the trailing full stop, and the stripped token still resolves to nothing
- **THEN** the report MUST class the entry `truncated`
- **AND** it MUST NOT class it `punctuation-stripped` instead
- **AND** it MUST still report the punctuation normalization it applied

#### Scenario: A longer path on the line ends with the token and stands in the tree
- **WHEN** every occurrence of a remainder entry sits at the end of a longer path written on the same line, and that longer path stands in this tree
- **THEN** the report MUST class the entry `truncated`
- **AND** it MUST name that longer path as the evidence

#### Scenario: A longer path on the line ends with the token and stands nowhere
- **WHEN** an occurrence sits at the end of a longer path on the same line and that longer path does NOT stand in this tree
- **THEN** the report MUST NOT class the entry `truncated` on that probe
- **AND** it MUST class the entry under whatever other mechanical class its evidence supports, or `unclassified`

#### Scenario: The character after the token opens a placeholder
- **WHEN** the character immediately following every occurrence of a remainder entry is `<`
- **THEN** the report MUST class the entry `truncated`
- **AND** it MUST NOT resolve the token as though the path ended where the extraction did

#### Scenario: The character after the token is ordinary prose
- **WHEN** the character immediately following an occurrence is anything other than `<`, and no other probe fires for that occurrence
- **THEN** the report MUST NOT class the entry `truncated` on that probe

#### Scenario: A path split across two source lines rejoins and resolves
- **WHEN** an occurrence ends its source line inside a string literal, the next line opens one, and the path rejoined across the two RESOLVES
- **THEN** the report MUST class the entry `truncated`
- **AND** it MUST NOT report the rejoined path as a second citation

#### Scenario: A path split across two source lines rejoins and still resolves to nothing
- **WHEN** an occurrence ends its line inside a string literal and the path rejoined across the two lines still resolves to nothing
- **THEN** the report MUST NOT class the entry `truncated` on that probe
- **AND** the entry MUST still be reported with the resolver outcome it has

#### Scenario: A stripped token still resolves to nothing
- **WHEN** the report strips a trailing character from a token under the grammar's normalization, the stripped token still resolves to nothing, and no `truncated` probe fires for the entry
- **THEN** the report MUST class the entry `punctuation-stripped`
- **AND** it MUST record the normalization it applied

#### Scenario: A token resolves once its trailing character is stripped
- **WHEN** a token resolves only after the report strips a trailing character from it
- **THEN** the report MUST report the resolved outcome and MUST print the normalization in its own row
- **AND** it MUST NOT class the entry `punctuation-stripped`, a token that resolves being no remainder entry at all

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
