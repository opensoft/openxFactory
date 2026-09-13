# release-realization Specification Delta

**ONE MODIFIED BLOCK AND THREE ADDED REQUIREMENTS, AND THE SPLIT IS A MEASURED
CHOICE.** The promoted requirement *Origin retention at archive* decides the
comparison this packet changes — it names "the declaration present at
ratification" as the baseline, and the whole defect is that after a rename the
walk compares against a commit that is not the ratification. That sentence has
to move, so it is MODIFIED. What the packet ADDS — a declaration, a refusal at a
landing, and a resolution rule for references — states three obligations canon
does not have at all, over three titles neither canon nor any active delta
carries.

**THE MODIFIED BLOCK CARRIES EVERY PROMOTED UNIT VERBATIM AND ONLY ADDS.** Every
sentence of the promoted requirement and all three of its scenarios are restated
byte-for-byte; nothing promoted is narrowed, dropped or re-worded. What follows
them is new. Measured rather than asserted: no active change holds a
`## MODIFIED Requirements` block over this title — the only other mention of it
anywhere under `openspec/changes/*/specs/` is one line of prose in
`add-structured-scope-substrate`'s delta, which mirrors the requirement for its
own scope declaration and does not restate it — so this block declares its
deltas against CANON and owes no `sequenced_after:` under *Ordered deltas and
branch vocabulary*.

**NOTHING HERE WALKS HISTORY.** The mechanism is a DECLARATION the author
writes, read from the tree the gate already reads. Where canon below says the
gate resolves a former identity, it resolves it the way this estate already
resolves a packet at a ref — by id, to the one path that id occupies there —
and never by rename detection, similarity scoring, or a walk over a lineage.

## MODIFIED Requirements

### Requirement: Origin retention at archive
The archive gate SHALL verify that a change's `.openspec.yaml` still carries
its original origin declaration unchanged. For staged origins, the
compressed supporting-document manifest SHALL retain the same origin id and
path; for ad-hoc origins, the archived change SHALL retain the reason and
approval provenance even when no support bundle exists. Mutation of an
origin declaration after ratification SHALL be rejected at the archive gate.

THE DECLARATION PRESENT AT RATIFICATION IS FOUND UNDER THE IDENTITY THE PACKET
WAS RATIFIED UNDER, WHICH IS NOT ALWAYS THE IDENTITY IT CARRIES NOW. Where the
packet declares a former identity, the gate SHALL resolve the ratifying commit
across the current identity and every declared former identity together, and
SHALL take the EARLIEST commit at which any of them declares `Status:
ratified`. Earliest is the whole of it: the failure this requirement exists to
catch is a baseline LATER than the real ratification, which waves through every
mutation made in between, so a resolution that could return a later commit than
some identity of the same packet offers would reintroduce the defect by another
route.

THE RESOLUTION IS BY IDENTITY AND NEVER BY HISTORY. Each identity is resolved
to the path it occupies at the commit being read, the way this estate already
locates a packet at a ref — the active location, or the dated archive
directory that carries the same id — and the gate SHALL NOT infer an identity
from rename detection, from similarity between two packets, or from any walk
over a lineage. An identity the packet has not declared is not an identity of
that packet, whatever history suggests.

AND THE COMPARISON ITSELF DOES NOT MOVE. A declared former identity changes
WHERE the baseline declaration is read and changes nothing about what is then
required of it: the origin block of the packet being archived must equal the
declaration at that baseline exactly, the support manifest's repeated origin
fields are measured against the same declaration, and an accepted mutation
still takes the explicit disposition this requirement's own scenario names. A
rename SHALL NOT be a way to acquire a later baseline, and therefore SHALL NOT
be a way to launder a mutation.

EVERY READ BEHIND THE BASELINE SHALL FAIL CLOSED, AND ABSENT SHALL BE
DISTINGUISHED FROM UNREADABLE. A checkout that cannot read the history holding
the baseline answers "there is nothing there" and "I cannot tell you" with the
same silence, and a gate that reads the second as the first is a gate that
switches itself off exactly where it can prove nothing. So the gate SHALL
establish whether a path is PRESENT at a commit from the tree, SHALL treat a
read it could not perform as a refusal — CANNOT RUN, naming the read that
failed and the identity it was for — and SHALL NOT report an unreadable
history as an unratified one. An EXISTING probe that collapses the two SHALL
NOT be reused for this read merely because it already resolves a packet by id.

AND AN IDENTITY THAT RESOLVES TO MORE THAN ONE PATH AT A COMMIT SHALL REFUSE
RATHER THAN CHOOSE. Where the current id or a declared former id matches more
than one candidate location in the tree being read, the gate SHALL refuse as
CANNOT RUN naming the candidates, on the same ground the estate's own
archived-directory lookup already states: two archive dates for one id is an
ambiguity to report, not a collision to resolve by taking one.

#### Scenario: A staged-origin change archives
- **WHEN** a change with a staged origin reaches its archive gate
- **THEN** the archived `.openspec.yaml` and the readable support manifest MUST carry the identical origin id and path declared at creation

#### Scenario: An ad-hoc change without a support bundle archives
- **WHEN** a change with an ad-hoc origin and no supporting documents reaches its archive gate
- **THEN** the archived packet MUST retain the origin's reason, approving authority, and approval date

#### Scenario: An origin was mutated after ratification
- **WHEN** the archive gate finds the origin declaration differs from the declaration present at ratification
- **THEN** the archive MUST fail
- **AND** restoring or accepting the mutation is a contested-class act requiring an explicit disposition

#### Scenario: A packet that declares a former identity reaches its archive gate
- **WHEN** a change declares a former identity and a commit under that identity declares `Status: ratified` earlier than any commit under the identity the packet carries now
- **THEN** the declaration present at that earlier commit MUST be the baseline
- **AND** the packet's current origin block and its support manifest MUST be measured against that declaration on the same terms as any other packet

#### Scenario: A mutation rides in the commit that renamed the packet
- **WHEN** a declared move also edits the origin declaration, so the packet's origin differs from the declaration at the baseline the declared former identity resolves
- **THEN** the archive MUST fail as an origin mutated after ratification
- **AND** the move having been lawfully declared MUST NOT be read as accepting the mutation

#### Scenario: The history holding the baseline cannot be read
- **WHEN** the gate cannot perform a read it needs to resolve the baseline — the tree says a path is present at a commit and the checkout cannot produce what stands there
- **THEN** the gate MUST refuse as CANNOT RUN, naming the read that failed
- **AND** it MUST NOT report the packet as unratified, and MUST NOT establish a baseline from the reads that did succeed

#### Scenario: A declared identity resolves to two locations at one commit
- **WHEN** the current id or a declared former id matches more than one candidate location in the tree being read
- **THEN** the gate MUST refuse as CANNOT RUN, naming the candidates
- **AND** it MUST NOT resolve the ambiguity by preferring one of them

## ADDED Requirements

### Requirement: A moved packet declares the identity it was ratified under
A change packet whose directory MOVES to a new change id SHALL declare the id it
moved from, in its own `.openspec.yaml`, as a member of a top-level
`former_ids:` list — a list, because a packet may move more than once, ordered
oldest first, and appended to rather than rewritten. The declaration is the
author's statement THIS DIRECTORY IS THAT PACKET, MOVED, and it is the only
thing in the corpus that carries that statement: history records that two paths
are similar and cannot record what the author meant by the similarity.

THE DECLARATION IS A SIBLING OF `origin:` AND NEVER A MEMBER OF IT, and the
reason is the freeze this specification already imposes. The origin declaration
is fixed at ratification and any post-ratification edit to it is a mutation
requiring an explicit disposition; a former-id entry is written by the very act
that MOVES the packet, which happens after ratification by construction, because
a draft that moves needs no declaration at all. A field inside the origin block
would therefore make every lawful move a mutation of a frozen declaration and
would need a disposition for each one. A top-level sibling is outside the block
the gate freezes, and it is the archive gate's own reader of that block — the
one that collects the `origin:` mapping's own lines and stops at the first
line that is not part of it — that makes this true rather than a convention.

AN ENTRY NAMES AN ID AND NEVER A PATH. This estate addresses a packet by its
change id and derives the path, at a ref as well as in the working tree — the
active location, or the dated archive directory carrying the same id — so an id
is declared ONCE per identity change and both of the paths it can occupy follow
from it. A declared PATH would have to restate the archive-directory convention
in every packet that ever moved, and would have to be re-declared when the
packet archives, which is not an identity change at all.

THE ARCHIVE RELOCATION IS NOT A MOVE UNDER THIS REQUIREMENT and SHALL NEVER BE
DECLARED. Archiving relocates `openspec/changes/<id>/` to
`openspec/changes/archive/<YYYY-MM-DD>-<id>/` and PRESERVES the id; it is
performed by the archive wrapper, it is recognizable from the id alone, and a
packet that declared it as a former identity would be declaring that it used to
be itself.

A DECLARED FORMER ID SHALL RESOLVE TO A PACKET THAT ACTUALLY MOVED. A former id
that stands as a live packet directory at the commit that declared it is a claim
to be the move of something that did not move, and SHALL be refused naming both
ids — that shape is a COPY, and a copy is a new packet with its own origin.

AN ENTRY IS ADDED ONLY BY THE COMMIT THAT PERFORMS THE MOVE IT RECORDS, and a
commit that adds a former id while moving nothing into this packet SHALL be
refused. Absence of a live directory is not proof of predecessorship: an id that
has archived, or that never existed, has no live directory either, so a rule
that only checks for one would let a standing packet append an unrelated
identity in an ordinary edit, acquire that identity's ratification as its
baseline, and capture every reference written under it. The entry a commit adds
SHALL therefore be exactly the source of the move that commit performs.

THE LIST IS APPEND-ONLY ACROSS COMMITS AND NOT ONLY WITHIN ONE. A commit that
REMOVES, REORDERS or REWRITES an entry an earlier commit established SHALL be
refused, whether or not that commit moves anything. Without that, a lawful move
could be declared at its landing and the declaration deleted the day after,
which would hand the archive gate the later ratification under the current id —
the very baseline this mechanism exists to keep it away from — and would do it
in a commit no arrival check ever looks at.

A FORMER IDENTITY HAS EXACTLY ONE OWNER. Where two packets declare the same
former id, or where an id is at once a live packet id and some packet's declared
former id, the declaration SHALL be refused naming every claimant: an identity
claimed twice resolves to a set, and a baseline chosen from a set is a baseline
chosen by the resolver rather than by an author.

#### Scenario: A ratified packet is renamed and declares where it came from
- **WHEN** the commit that renames a ratified packet also adds the former id to the destination packet's `former_ids:`
- **THEN** the move is lawful, the packet keeps the ratification it had under the former id, and its archive gate reads the baseline there

#### Scenario: A packet moves more than once
- **WHEN** a packet that already declares a former id moves again
- **THEN** the new former id MUST be appended to the existing list, oldest first, and no existing entry may be rewritten or removed

#### Scenario: A fork by copy declares nothing
- **WHEN** a new packet is authored as a copy of a ratified one, the source packet still standing in the tree
- **THEN** it MUST declare no former id, MUST carry its own origin declaration, and is baselined at its own first ratification
- **AND** the gate MUST NOT refuse it, the source having not moved

#### Scenario: A declared former id still stands in the tree
- **WHEN** a packet declares a former id and a live packet directory carries that id at the same commit
- **THEN** the declaration MUST be refused, naming both ids, because a packet that still stands was copied and not moved

#### Scenario: A draft is renamed
- **WHEN** a packet that has never declared `Status: ratified` is renamed
- **THEN** no declaration is owed, the packet having no ratification for a former identity to carry

#### Scenario: A former id is appended by a commit that moves nothing
- **WHEN** a standing packet adds a former id in a commit that performs no move of that id into it
- **THEN** the declaration MUST be refused, naming the id and the commit
- **AND** the id having no live directory MUST NOT be read as evidence that it moved here

#### Scenario: A later commit removes or reorders a declared former id
- **WHEN** a commit rewrites `former_ids:` so that an entry an earlier commit established is removed, reordered or respelled
- **THEN** that commit MUST be refused, the list being append-only across commits and not only within one

#### Scenario: Two packets claim the same former identity
- **WHEN** two packets declare the same id in `former_ids:`, or an id is both a live packet id and a declared former id
- **THEN** the declaration MUST be refused, naming every claimant
- **AND** the resolver MUST NOT settle the claim by preferring one of them

### Requirement: An undeclared rename arrival is refused at its landing
A landing SHALL be REFUSED where its commit brings a change packet directory in
by a MOVE from another change packet directory WHOSE IDENTITY HAS EVER DECLARED
`Status: ratified`, and the arriving packet does not declare the source id in
`former_ids:` in that same commit. The refusal is taken AT THE LANDING of
the commit that performs the move, which is the only place the question is
cheap: a move lands as one commit, so the gate reads one commit and never a
chain, and the author who made the move is the author who is asked.

THE SOURCE IDENTITY IS THE SOURCE PACKET'S WHOLE DECLARED LINEAGE — its own id
TOGETHER WITH every id it declares in `former_ids:` at that commit's parent —
and the "ever ratified" test SHALL be taken over all of them. Reading the source
id alone would lose a packet that has already moved once lawfully: X ratified,
X moved to Y with the move declared and the header returned to draft, then Y
moved to Z undeclared. Y's own id never declared `Status: ratified`, so a test
over Y alone would pass the second landing and Z would stand with no lineage at
all. THIS IS NOT A HISTORY WALK: the source packet's own declaration is one
blob at one commit, and every id it names is asked directly, exactly as the
baseline resolution asks them.

AND THE ARRIVING PACKET'S LIST SHALL BE THE SOURCE'S LIST WITH THE SOURCE ID
APPENDED — every entry the source carried, in the order it carried them, then
the id the move came from. A move that drops an entry the source declared is a
move that sheds a lineage, which is the same defect as never declaring one.

A MOVE OF A PACKET THAT HAS NEVER BEEN RATIFIED IS OUT OF SCOPE AND STAYS
LAWFUL. Renaming a draft is an ordinary authoring act this estate performs, the
promoted realization record says so in as many words — *"renaming a DRAFT
change, and a single commit that renames a draft and ratifies it, are
unaffected"* — and a refusal reaching it would make the mechanism cost more than
the defect. The qualification is EVER, read over the source identity's whole
history up to that commit, and never its blob at the parent: a packet renamed
and un-ratified in one commit is back in DRAFT for every later hop, so a test
taken at the parent would exempt exactly the shape this refusal exists to catch.

THE REFUSAL IS WHAT MAKES THE DECLARATION MORE THAN AN HONOUR SYSTEM. A
mechanism that only reads declarations protects the author who writes one; the
failure this gate exists to catch is a rename that sheds a ratification, which
is by construction a rename whose author would not declare it. So the
UNDECLARED case is the refused case, and the declared case is the ordinary one.

THE ARCHIVE RELOCATION IS EXCEPTED BY ID, and it is the only exception. A
destination under `openspec/changes/archive/<YYYY-MM-DD>-<id>/` whose id equals
the source's id is the archive wrapper's own relocation and SHALL pass without a
declaration.

THE ARRIVAL READ SHALL FAIL CLOSED. Where the gate cannot perform the read that
would pair an arrival with a departure — a checkout that cannot produce the
content the pairing is computed from — and the tree at that commit shows both a
packet directory arriving and a packet directory leaving, the gate SHALL refuse
as CANNOT RUN, naming the read it could not perform, rather than reporting that
no arrival was found. A silence that cannot be distinguished from an answer is
not an answer.

THE REFUSAL SHALL NAME THE REMEDY AND SHALL CARRY NO BYPASS FLAG. It names the
commit, the source path, the destination path, and the one repair: declare the
source id in the destination packet's `former_ids:` in the same commit. A flag
would be the declaration nobody writes.

#### Scenario: A ratified packet is renamed with no declaration
- **WHEN** a commit moves a change packet directory to a new id and the arriving packet declares no former id
- **THEN** the gate MUST refuse that landing, naming the commit, both paths, and the declaration that would repair it

#### Scenario: A rename chain is attempted one hop at a time
- **WHEN** a packet is renamed, un-ratified, renamed again while draft, and ratified under its third id, each hop landing as its own commit
- **THEN** the FIRST undeclared hop MUST be refused at its own landing, so no later hop is ever reached
- **AND** the gate MUST NOT need to walk the chain to reach that answer
- **AND** the first hop qualifies because its source had declared `Status: ratified`, whatever the destination declares at that commit

#### Scenario: A never-ratified draft is renamed
- **WHEN** a commit moves a packet directory whose identity has never declared `Status: ratified` anywhere in its history
- **THEN** the landing passes with no declaration, the move being an ordinary authoring act

#### Scenario: A once-ratified packet is moved while back in draft
- **WHEN** a commit moves a packet whose identity declared `Status: ratified` earlier in its history but does not at that commit
- **THEN** the landing MUST be refused unless the arriving packet declares the source id
- **AND** the test MUST be the source identity's whole history and never its blob at the commit's parent

#### Scenario: A packet that already moved lawfully moves again
- **WHEN** a packet ratified under one id, moved to a second with the move declared and the header returned to draft, is moved to a third
- **THEN** the "ever ratified" test MUST reach the id the packet declares as its former identity, so the second move is refused unless it too is declared
- **AND** the arriving packet's list MUST be the source's list with the source id appended, so no entry the source declared is dropped

#### Scenario: A move drops an entry the source declared
- **WHEN** a declared move's destination omits an id the source packet carried in its own `former_ids:`
- **THEN** the landing MUST be refused, a move that sheds a lineage being the same defect as never declaring one

#### Scenario: The declared move lands
- **WHEN** the moving commit carries the source id in the destination packet's `former_ids:`
- **THEN** the landing passes and the identity continuity is on the record where the archive gate will read it

#### Scenario: A packet archives
- **WHEN** a commit relocates `openspec/changes/<id>/` to `openspec/changes/archive/<YYYY-MM-DD>-<id>/` with the id unchanged
- **THEN** the landing passes with no declaration, the archive relocation preserving the identity rather than changing it

#### Scenario: The pairing read cannot be performed
- **WHEN** the checkout cannot produce what the arrival pairing is computed from, and the tree at that commit shows a packet directory arriving and a packet directory leaving
- **THEN** the gate MUST refuse as CANNOT RUN, naming the read it could not perform
- **AND** it MUST NOT report that no arrival was found

### Requirement: A packet reference resolves by identity, not by path
A reference that addresses a change packet SHALL be resolved BY ITS CHANGE ID —
against the location that id occupies now, whether active or archived, and
against any packet that declares that id in `former_ids:` — and a reference is
dangling only when it resolves to nothing under that rule. A path written into a
record is a spelling of an identity at one moment; the identity is what the
record meant, and it is the identity that has to resolve.

A PACKET-RELATIVE PATH CARRIES THE ID IT ADDRESSES, so this rule reaches
citations written as paths and not only citations written as ids: the second
segment of `openspec/changes/<id>/…` names the packet, and the remainder names a
file within it, which is what makes the reference re-resolvable at all.

BOTH HALVES SHALL RESOLVE, AND A FAILURE SHALL SAY WHICH HALF FAILED. Where a
citation names a file inside the packet, the location the identity resolves to
MUST also carry that remainder; an identity that resolves to a packet which does
not carry the cited file is a DANGLING reference, reported against the file and
not against the packet. Resolving the identity alone would accept a citation to
a file that was deleted, renamed or never written — a defect this rule exists to
find, spelled at a finer grain than the one the archive relocation breaks.

THE DEFECT IS THAT NOTHING RESOLVES THEM. A citation contract that requires a
citation and never checks that it leads anywhere accepts a citation to a path
that has not existed for weeks, and the corpus's own citations break by an act
nobody thinks of as breaking anything — the archive relocation, which every
packet performs exactly once.

RESOLUTION IS TO EXACTLY ONE PACKET, OR TO NOTHING, AND NEVER TO A SET. Where an
id would resolve to more than one candidate — two dated archive directories
carrying the same id, a live directory and some packet's declared former id, or
two packets declaring the same former id — the reference SHALL be reported as
AMBIGUOUS and SHALL NOT be resolved by preferring one. This estate already draws
that line where it resolves a packet by id: its archived-directory lookup
returns every match as a LIST rather than a path, on the stated ground that two
archive dates for one id is "an AMBIGUITY the resolver must be able to report,
not a collision to resolve by taking the newest". A resolver that silently picks
one candidate makes the record's meaning depend on sort order.

CORRECTING A RECORD IS NOT THE REMEDY THIS REQUIREMENT IMPOSES. Where a
reference resolves by identity, it is not a defect and nothing is owed; the
reader resolves it. Only a reference that resolves to no identity at all is a
defect, and it belongs to the record that wrote it. An AMBIGUOUS reference is
neither: it is a defect of the corpus that made one identity resolve twice, and
it belongs to the declaration that created the collision.

#### Scenario: A cited path names a packet that has since archived
- **WHEN** a record cites `openspec/changes/<id>/<file>` and that packet now stands at `openspec/changes/archive/<YYYY-MM-DD>-<id>/<file>`
- **THEN** the reference MUST resolve by id to the archived location and MUST NOT be reported as dangling
- **AND** no edit to the citing record is owed

#### Scenario: A cited path names an id a packet declares as a former id
- **WHEN** a record cites a packet by an id that no directory carries, and some packet declares that id in `former_ids:`
- **THEN** the reference MUST resolve to that packet
- **AND** the declaration is what authorizes the resolution, a path similarity never being one

#### Scenario: A cited path resolves to no identity at all
- **WHEN** a cited packet id names no active directory, no archived directory, and no declared former id
- **THEN** the reference is dangling and is a defect of the citing record

#### Scenario: The identity resolves and the cited file does not
- **WHEN** a citation's packet id resolves but the location it resolves to does not carry the remainder the citation names
- **THEN** the reference is dangling and the report MUST name the FILE as the half that failed, the identity having resolved

#### Scenario: A reference names another repository's packet
- **WHEN** a citation names a packet in a repository other than the one being read
- **THEN** it MUST NOT be reported as dangling on that tree, a reference out of scope being no evidence about the reference

#### Scenario: An id resolves to more than one packet
- **WHEN** a cited id matches two dated archive directories, or a live directory and a declared former id, or two packets' declared former ids
- **THEN** the reference MUST be reported as AMBIGUOUS and MUST NOT be resolved by preferring one candidate
- **AND** the defect belongs to the declaration that made one identity resolve twice, not to the citing record
