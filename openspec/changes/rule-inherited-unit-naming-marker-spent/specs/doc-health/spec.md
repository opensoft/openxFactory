# doc-health

## MODIFIED Requirements

### Requirement: Currency of an active change's MODIFIED requirement blocks
The modified-block currency family SHALL compare every active change's
`## MODIFIED Requirements` block against the requirement as the promoted
specification currently states it, and report what the block does not carry —
reporting against the active delta's own path, while the change can still be
edited.

The obligation being checked belongs to `document-lifecycle` ("A MODIFIED
requirement block restates the requirement as canon currently states it"); this
requirement defines only how doc-health checks it, in the same by-reference
relationship promotion fidelity and duplicate packet already have with that
capability's obligations.

**This family answers a question the promotion fidelity family cannot, and it
asks it at the only time the answer is cheap.** That family compares an
archived delta to canon, and after an archive act canon IS the delta — a block
that dropped seven scenarios and a canon that now lacks them agree perfectly,
so that family reports nothing. The comparison that can see the class is
between an active delta and the canon it has not yet replaced, which is a
different document pair read at a different moment, and is why this is a
separate family rather than a wider reading of that one. It is also why the
loss is invisible to counting: the file-level scenario count can stay flat
while a requirement goes from eight scenarios to one, because a change's own
ADDED requirement offsets what its MODIFIED block drops.

**The family SHALL read every active change regardless of its lifecycle
standing.** A `draft` packet's block is as capable of restating stale canon as
a `ratified` one, and a finding against a draft costs its author one line —
which is the cheapest moment to pay it, the scenario-title arm below now
carrying an `error` that reds any run configured to fail on it. This is a
reading rule for the check and is deliberately WIDER than the two-writers
obligation below, which `release-realization` scopes to an active RATIFIED
change and which this requirement does not widen.

The family SHALL implement three comparison arms over one document pair, and
SHALL report them as distinct finding classes so that a precise signal is never
buried in an editorial one:

- **Scenario-title completeness.** Every `#### Scenario:` title the promoted
  requirement carries SHALL appear as a scenario title in the block. This arm
  reports deletion at the granularity the defect occurs at, its inputs are
  short titled strings rather than prose, and it is the arm that carries this
  family's gate.
- **The carriage ledger.** Every body unit of the promoted requirement, and
  every scenario bullet it carries, SHALL be reported where the block does not
  carry it. Scenario bullets SHALL be compared against ALL bullets of ALL
  scenarios in the block, never scenario by scenario: a bullet carries the
  requirement's actual obligations, and pairing each bullet to the scenario
  that restates it would let a block retitle a scenario, declare the retitle,
  and drop the bullets underneath it unreported. This arm CANNOT distinguish a
  deliberate rewording from stale text and SHALL NOT be read as claiming it
  does; it is the list a reviewer reads to confirm that each divergence is one
  the change intended. It SHALL emit at most one finding per requirement,
  listing the units, rather than one finding per unit.
- **Title resolution and the two-writers rule.** A MODIFIED block whose
  capability and requirement title resolve to no promoted requirement SHALL be
  resolved in order: FIRST against the change's own `## RENAMED Requirements`
  block, and where that block renames a promoted requirement to this title the
  three arms above SHALL run against canon under the OLD name, a rename being a
  change of title rather than of the content a block must carry; THEN against a
  requirement an active sibling change ADDS or RENAMES. Where a title resolves
  to none of those, the block SHALL be reported. Where two active changes carry
  a MODIFIED block for ONE promoted requirement, ORDER IS BY DECLARATION AND
  NEVER BY DATE. `release-realization`'s "Ordered deltas and branch vocabulary"
  already requires the later proposal to reference the earlier change and
  declare its deltas relative to that change's outcome, so the change that
  makes that declaration IS the later writer and nothing else needs to decide
  it. The declaration SHALL be read as the sibling's change id occurring as a
  whole token in the declaring change's own `proposal.md` — the whole-token
  match the duplicate packet family already uses, so one change id occurring
  inside a longer one satisfies nothing. The declaring block SHALL be measured
  against the declared sibling's outcome rather than against canon, and the
  sibling's additions SHALL be present in it. EXACTLY ONE of two active
  RATIFIED writers SHALL declare: where neither does the run SHALL report the
  undeclared ordering against both blocks, and where both declare relative to
  each other the run SHALL report that too, mutual declaration deciding
  nothing. Where no declaration stands, each block SHALL be measured against
  canon, which is the only basis a reader can name. No folder name, commit
  timestamp, or `created:` date SHALL be consulted.

**A canon unit is CARRIED only by a block unit of the SAME KIND, matched in
full after whitespace normalization.** Normalization collapses runs of
whitespace to a single space and strips leading and trailing whitespace, so a
re-wrapped paragraph compares equal to the same paragraph wrapped differently;
no normalization beyond it applies. A canon body unit is carried only by a body
unit of the block, a canon scenario title only by a scenario title of the
block, and a canon scenario bullet only by a scenario bullet of the block.
**Matching MUST NOT be substring containment.** A block bullet that CONTAINS
canon's bullet has replaced it — which is precisely how issue #351's widened
line entered — and a containment rule would report nothing there. A similarity
or near-match rule MUST NOT be used either: it would accept a clause whose
meaning had been reversed, which is also on this class's record, and the
corpus has already ruled against resemblance as an identity test in the
duplicate packet family.

**The units of a requirement SHALL be derived mechanically, and the derivation
is normative.** Backticked spans SHALL be masked before any sentence split, so
that a period inside `.openspec.yaml` or `promotion_fidelity.py` never ends a
sentence. In the requirement BODY — everything above the first
`#### Scenario:` — each bullet line SHALL be one unit with its list marker
stripped; each dated bold note SHALL be one unit, undivided, a note being a
single editorial statement whose sentences mean nothing apart; and every other
paragraph SHALL be split into sentences at a period, question mark or
exclamation mark followed by whitespace or the end of the paragraph. In the
SCENARIOS, each `#### Scenario:` heading SHALL be one title unit and each
bullet line SHALL be one bullet unit. A paragraph of RESERVED MARKER form —
defined below — SHALL NOT be a unit of either kind, in canon or in a block.

**A deliberate deletion SHALL be declared by a RESERVED MARKER, recognized by
form and never by prose.** A marker is ONE PARAGRAPH inside the MODIFIED block,
read after the same whitespace normalization every other unit gets so that a
marker wrapped across several lines is still one marker, in one of exactly two
forms:

- `**Removed from canon by <change-id> (<YYYY-MM-DD>):**` followed by the
  deleted units, then ` — <reason>`.
- ``**Merged into `<destination scenario title>` by <change-id> (<YYYY-MM-DD>):**``
  followed by the superseded scenario titles — the form for two scenarios
  legitimately becoming one. The destination is written as a code span like
  every other title this marker carries, and in this one spelling everywhere.

**A paragraph is of MARKER FORM only where, after normalization, it BEGINS with
one of those two prefixes COMPLETE** — the bold run, a resolvable change-id, an
ISO date in parentheses, and the closing colon. A paragraph that merely quotes,
templates or describes a marker does not begin with one, and is an ordinary body
unit like any other prose. This anchor is load-bearing rather than pedantic:
this requirement's own text and `document-lifecycle`'s both set out the two
templates in prose, both promote into canon, and a looser test would read them
as markers and exempt them from carriage — the check quietly declining to check
the paragraphs that define it.

**Every unit a marker names, and the `Merged into` destination, SHALL be written
as a CommonMark code span, and a unit that itself contains backticks SHALL be
fenced with a longer run of them.** Roughly a third of this corpus's requirement
body units and a sixth of its scenario bullets contain a backtick, because they
cite things like `openxFactory` or `promotion_fidelity.py`; a single-backtick
span around such a unit ends at its first inner backtick and names a fragment,
so the marker would name something that is not a unit at all. CommonMark already
provides the longer fence and this rule adds nothing to it. The parser SHALL
extract the code spans following the colon, in order, per CommonMark, and THE
REASON SHALL BEGIN AT THE FIRST ` — ` SEPARATOR STANDING OUTSIDE EVERY CODE
SPAN: the units named are the spans that close before that separator, the reason
is everything after it, and a code span that falls inside the reason is prose
the reason quotes rather than a unit the marker names. Where no such separator
stands, every span names a unit and the marker carries no reason, which is what
the written-out `Merged into` example below is. The boundary is read the same
way in both forms, the `Merged into` destination being matched in the prefix and
the tail after the closing colon being parsed identically. Semicolons and dashes
inside a unit or inside a reason are therefore irrelevant, because extraction is
by code span and never by splitting on punctuation.

**The `Merged into` destination is NOT a named unit.** It states where the
superseded scenarios went, and it is present in the block by construction —
reading it as a named unit would make every valid merge marker report itself
under the rule below. Only the code spans after the colon name units.

A marker SHALL suppress only the units it names AND that are in fact absent
from the block. A MARKER SHALL ITSELF BE REPORTED ON ANY OF FIVE GROUNDS, each
of them one finding at the `info` band this family's marker-defect class
already carries: it names a unit the block still carries; or a code span
standing INSIDE its reason matches EXACTLY a unit of the requirement's basis
that the block does not carry and that no marker declares removed, the boundary
above reading that span as prose rather than as a name, so that its author
declared nothing about a unit they plainly had in mind; or it names something
matching no unit of the requirement's basis and no unit of the block; or it
names something matching no unit of the requirement's basis and a unit THE
BLOCK ITSELF STATES, declaring removed from canon a unit canon never carried;
or it is of `Removed from canon` form and its tail carries NO code span at all,
so that it names nothing, quotes nothing and declares nothing while occupying
the one paragraph shape this requirement exempts from carriage. Each of the
five is a declaration that does not describe the block, which is a declaration
no reader can rely on, and a report on the MARKER is what points an author at
the paragraph they wrote rather than at the unit it failed to declare. THE
FOURTH GROUND RESTS ON THE BLOCK'S OWN ADDITION AND ON NOTHING ELSE, and it
changes no suppression: a name matching no unit of the requirement's basis has
never suppressed anything and still suppresses nothing, and the addition the
name matches SHALL NOT be reported for being named, an addition being text no
arm of this family reads. THE FIFTH GROUND SHALL BE READ ON THE `Removed from
canon` FORM ALONE: the pairing form names no units by construction, its whole
tail being a reason, so a pairing marker carrying no code span declares exactly
what that form declares and SHALL NOT be reported on this ground. AND A `Merged
into` MARKER WHOSE TAIL NAMES NO SUPERSEDED TITLE IS SILENT BY RULE RATHER THAN
BY OMISSION: that form declares its DESTINATION IN ITS PREFIX, complete before
the closing colon and where this form's declaration has always been read, so
the tail names what the destination ABSORBED and a marker whose tail names
nothing has still declared everything the form obliges it to declare; it SHALL
NOT be reported on the fifth ground, which is read on the `Removed from canon`
form alone, and where its tail carries NO CODE SPAN AT ALL it reaches none of
the other four either, each of those being read through a name or a quoted span
such a tail does not carry — so NO ground fires on it and NO ground is added
here; a code span its reason DOES quote remains subject to the second ground
exactly as in every other marker. THE SECOND GROUND SHALL BE READ NARROWLY, on
the exact match and never on the span's position alone: a reason is prose and
prose in this corpus quotes, so a code span inside a reason matching no unit of
the requirement is the NORMAL FORM of a reason and SHALL NOT be reported. The
second ground SHALL NOT withdraw the carriage arms from the unit the span would
have named — the scenario below that keeps that unit subject to them stands
unchanged — the report being added BESIDE the carriage and never in place of
it.

**A named scenario TITLE carries its bullets with it ONLY IN A GENUINE
REMOVAL.** Where a `Removed from canon` marker names a scenario title AND the
block adds no scenario title canon does not already carry, the bullets that
scenario carried in canon SHALL also be treated as declared removed — unless
they appear as bullets elsewhere in the block, in which case they are carried
and nothing is reported about them either way. Declaring a scenario genuinely
gone and then reporting its bullets forever would make the declaration useless
for the act it exists to declare.

**Where the block DOES add a scenario title canon does not carry, a
`Removed from canon` marker SHALL NOT suppress the removed title's bullets.**
That shape is a retitle, whatever the marker calls it, and treating it as a
removal reopens the defect the bullet arm exists to close: name the old title
removed, add a replacement carrying two of its four bullets, and two obligations
leave canon with nothing reported. The author's instrument for a retitle is
`Merged into`, whose bullets must be carried somewhere in the block or named
individually in a `Removed from canon` marker of their own. **A `Merged into`
marker names titles only**, so a bullet a merge makes redundant is a declared
removal, not a permanent editorial row — but it has to be declared as a bullet,
one at a time, which is exactly the deliberation the class deserves.

**A marker is NOT a carriage unit, in either direction.** A marker promotes
into canon with the requirement that carries it, and if it were a unit every
later block would have to restate every marker any predecessor ever wrote,
forever. The durable record of a deletion is the archived delta, which is where
every other archived governance act is read from. **A UNIT-NAMING MARKER IS
SPENT ONCE THE UNIT IT NAMES HAS LEFT CANON BY A DECLARED ACT, AND DROPPING IT
IS THEREFORE THE LAWFUL CARRIAGE.** The act the marker declares is complete and
the unit it names is gone from the promoted text, so the marker describes
nothing a later block could be carrying: a later block SHALL NOT be required to
restate it, SHALL NOT be reported for omitting it, and loses no record by
dropping it, the archived delta named above being where that record is read.
WHERE A LATER BLOCK CARRIES A SPENT MARKER FORWARD INSTEAD, THE THIRD GROUND
ABOVE REPORTS THAT MARKER, AND THAT REPORT IS THIS CLASS WORKING AS WRITTEN
RATHER THAN A DEFECT OF THE LATER AUTHOR'S CARE: the name matches no unit of
the requirement's basis, the declared act having removed it, and no unit of the
block, a block not restating a retired unit, which is the third ground exactly
as it already stands. NO GROUND IS ADDED HERE, NONE IS WITHDRAWN AND NO
SUPPRESSION MOVES: the count stays at FIVE, a spent name suppresses nothing and
never has, and both carriage arms are untouched — what is written here is which
of the two standing options is the lawful one and what the other one costs, not
a sixth ground and not a suppression this class does not carry. AND IT IS READ
ON A MARKER THAT NAMES A UNIT AND ON NO OTHER: a marker that names nothing
reaches the third ground through no name at all, so nothing here decides
anything about it, and the standing of a tail that names nothing is decided in
the grounds paragraph above rather than in this one.

Written out, the two forms are exactly:

```
**Removed from canon by add-example-change (2026-08-27):** `Gate verbs hide on a composed view`; ``an adapter that reaches a hosted provider SHALL obtain its credential through the `openxFactory` broker lane`` — the affordance is now tile-bound and the credential clause moved to its own requirement
**Merged into `Tile-bound gate verbs hide on a composed view` by add-example-change (2026-08-27):** `Gate verbs hide on a composed view`
```

**The marker is NEW, and the existing dated-note convention MUST NOT be reused
for it.** Every dated bold note in this corpus today records a caught near-miss
and a RESTORATION, never a deletion — and `doc-health`'s own "Deterministic
check families" carries one naming SEVEN of its eight scenario titles in
backticks as restored. A rule that read deletion out of prose would therefore
read a faithful restatement of that very requirement as declaring seven
scenarios deleted, on the requirement whose truncation is issue #329. Form,
not prose, is what makes the declaration falsifiable.

A recorded disposition in the aggregation checkout's `health/dispositions.yaml`
naming THIS family, with a `cite`, optionally narrowed to one requirement,
SHALL suppress the findings it names; an entry naming another family MUST NOT
suppress this family's findings. Nothing else suppresses.

**This family SHALL measure the checked-out tree.** The live-`main` basis this
capability defines applies to the promotion fidelity family alone, and it would
be actively wrong here: an active change lives on a branch, so a family reading
`main` would measure a delta `main` does not carry against canon the branch may
have moved.

**This family SHALL be ENFORCING IN ONE ARM AND CLASSIFIED `contested` WHOLE,
which is what the flip of 2026-08-31 left behind.** Every finding of the
scenario-title completeness arm — the arm that carries this family's gate —
SHALL carry `error` severity, so a run configured to fail on `error` fails on a
MODIFIED block that drops a scenario canon still carries; every other class the
family emits SHALL keep the band its own rule states, the title-resolution and
ordering arm at `warning` and the carriage ledger and the marker defects at
`info`, so no `--fail-on` configuration reds on those; and the family SHALL be
classified `contested`, so a finding of ANY of its classes is a contested
finding, and a session working a report's ranked plan SHALL NOT apply a
state-changing edit for one, escalating it to a change proposal or a recorded
disposition instead. THE DISAPPEARANCE THAT OWES A CITATION IS READ AT THE
GRAIN THE UNCITED-RESOLUTION RULE KEYS ON, WHICH IS `(family, repository,
path)` AND NOT THE CLASS: where this family stops reporting at a repository and
path the previous report carried, the resolution is uncited without a recorded
citation and SHALL be the `error` that rule defines; where a finding of ONE
class stops being reported while ANY other finding of this family is still
emitted at that same repository and path, the key never leaves the current
report and the rule does not fire — which the promoted *A
modified-block-currency finding its own class map cannot place is itself a
finding* already states of this family's key, and this requirement neither
widens nor narrows it. THE RESOLUTION TABLE HAS NO PER-CLASS GRAIN — it is
applied by finding FAMILY alone, one string every arm and every class of this
module shares — so the classification reaches every class the family emits, and
neither this requirement nor any other can hold one class out of it.

THE FAMILY SHIPPED ADVISORY IN BOTH HALVES AND WAS FLIPPED IN BOTH BY ONE
RULING, WHICH RAISED EXACTLY ONE SEVERITY ARM AND LEFT EVERY OTHER BAND WHERE
IT STOOD, which is the sequence this requirement records rather than a history
it has replaced. At launch every finding carried `warning` or `info` and the
family was deliberately absent from `FAMILY_RESOLUTION`, because no run had yet
measured what the governed repositories' active changes would say and a
`contested` advisory family would have gated through the back door on the first
block anyone corrected. The flip SHALL be taken as ONE decision by ruling,
never as a judgement call inside an implementation, and SHALL follow the
discharge of the standing population rather than precede it — a gate that goes
red on the commit introducing it teaches everyone to route around the gate. IT
WAS TAKEN THAT WAY: the ruling of 2026-08-27 was "MEASURE FIRST, THEN FLIP",
the nightly aggregation runs of 2026-08-30 and 2026-08-31 read the
scenario-title arm's population at ZERO across every governed repository, and
the flip was ordered on 2026-08-31 and landed as ONE COMMIT that raised the
scenario-title arm's severity constant to `error` and added the family's
`contested` row together (openxFactory issue #357, pull request #529). THE TWO
HALVES MOVE TOGETHER AND MUST NOT BE TAKEN APART: severity alone gates the
family without the disposition discipline that makes a disappearing finding
accountable, and the contested class alone gates it through
`uncited-resolution` under a family name that does not say what happened. **No
flip is proposed for the carriage ledger in this change**, whose population is
standing by construction — every legitimate MODIFIED block edits something — so
an editorial band is the honest launch state; a later flip remains available
and is a ruling like any other.

**AMENDED BY `amend-marker-reason-boundary` (2026-09-06).** Every paragraph and
every scenario above this note stands exactly as promoted, and the only change
this block makes to promoted text is to ONE body sentence: the one that told the
parser to measure a marker's reason from BEHIND, from its LAST code span. TWO
SCENARIOS ARE ADDED, at the END of the block, and they pin that sentence rather
than restate it — a normative rule no scenario exercises is a rule the next
author re-deriving this parser has nothing to test against. No promoted scenario
moves, is retitled or loses a bullet; no arm is removed, no severity changes, no
threshold moves, no disposition rule changes, and the set of trees over which
this family speaks is not altered by one line.

MEASURING THE REASON FROM BEHIND MAKES EVERY CODE SPAN AN AUTHOR WRITES INSIDE
IT A NAME. A reason is prose, and prose in this corpus quotes: the two markers
`doc-health`'s own *Release-tag publication* carries each name the `WHEN` bullet
they retire and then, in the reason that explains the retirement, quote the
words `WHEN` and `AND` as code spans — so the promoted parser reads THREE
declared-removed names where each author declared one, and reads the explanation
as no reason at all. Measured on this corpus on 2026-09-06, ACROSS THE PROMOTED
SPECIFICATIONS AND EVERY ACTIVE DELTA OTHER THAN THIS ONE — this block carries
an eighth marker, the one below, and a figure a reader is invited to re-derive
must name the tree it was taken on: SEVEN unit-naming markers, of which TWO are
misread this way and FIVE are unaffected; and of 17,566 derived units NONE
is literally `WHEN` or `AND`, and neither is any unit this block's own text
adds, so today every wrongly-derived name matches no
canon unit, suppresses nothing and is reported as nothing. **THE DEFECT IS
INERT AND IS NOT HARMLESS.** The names a marker derives are what it suppresses,
and the next author whose reason quotes a real unit — a scenario title, a clause
this corpus actually carries — declares that unit removed by mentioning it. The
boundary above puts the reason where its author put it, and its direction of
failure is the conservative one: a marker that separated its names with ` — `
would have the later ones read as reason, would suppress nothing with them, and
the units it meant to name would be REPORTED rather than silently dropped. No
marker in this corpus is written that way, which is what the seven were measured
to establish.

**AMENDED BY `amend-marker-defect-reporting` (2026-09-09).** Every paragraph
and every scenario above this note stands exactly as promoted —
`amend-marker-reason-boundary`'s own note and its narrative included — and the
only change this block makes to promoted text is to ONE body sentence: the one
that gave a marker exactly ONE reporting ground. TWO SCENARIOS ARE ADDED, at the
END of the block, one for each ground added, because a normative ground no
scenario exercises is a ground the next author re-deriving this class has nothing
to test against. No promoted scenario moves, is retitled or loses a bullet: the
reason-quotes scenario's third `AND`, which keeps the quoted unit subject to the
carriage arms, is carried word for word, this amendment adding a report about the
MARKER beside that carriage rather than replacing it. No arm is removed, no
severity moves, no threshold moves, no disposition rule changes, this family's
registration in the resolution table is untouched, and the set of trees over
which this family speaks is not altered by one line. AND
`amend-marker-reason-boundary`'S OWN `Removed from canon` MARKER IS DELIBERATELY
NOT RESTATED HERE, on this requirement's own rule that a marker is not a
carriage unit in either direction: restating it would declare a removal this
change did not perform, and its named unit — a sentence canon no longer carries
because that change removed it — matches no unit of the requirement or of this
block, which is the third ground above reporting this block for copying a
predecessor's declaration forward.

A MARKER IS A DECLARATION, AND UNTIL THIS AMENDMENT A DECLARATION THAT DESCRIBED
NOTHING WAS SILENT IN TWO WAYS. The first is as old as the family: a name
matching no unit of the requirement suppressed nothing and was reported as
nothing, which `add-modified-block-currency-check` recorded as a plausible later
ruling it had no standing to take, because this sentence gave a marker exactly
one reporting ground. The second is younger than the boundary:
`amend-marker-reason-boundary` correctly stopped reading a code span inside a
reason as a name, and an author who separates two NAMES with the separator
therefore declares only the first — the second is read as prose, suppresses
nothing, and the unit it meant to declare is REPORTED, which is the conservative
direction, but the marker that caused it is not, so its author is pointed at a
unit rather than at their own paragraph. THE SECOND GROUND IS NARROW BY DESIGN
AND THE MEASUREMENT IS WHY. Measured on this corpus on 2026-09-09, across every
promoted specification and every active delta OTHER THAN THIS ONE — this block
carries a marker of its own and a figure a reader is invited to re-derive must
name the tree it was taken on: SIXTEEN unit-naming markers, of which EIGHT quote
a code span inside their reason, every one of them a marker promoted into canon
and every quoted span reason-prose; and of those quoted spans, ZERO is a derived
unit of the document carrying it. So a ground written on the span's POSITION
would report eight legitimate markers the moment a MODIFIED block restated one
of them, and would grow with the corpus, while a ground written on an EXACT
MATCH against an uncarried unit is silent on all eight. THE POPULATION OF BOTH
NEW GROUNDS IS ZERO TODAY, and that is measured rather than hoped: of the active
MODIFIED blocks this family reads, TWO carry a unit-naming marker at all, both
of the `Merged into` form, each naming one unit that matches its resolved basis,
neither quoting a code span in a reason. A ground whose population is zero at
landing is a ground that reports the NEXT marker written, which is the only
moment at which either silence has ever cost anybody anything.

**AMENDED BY `amend-modified-block-currency-standing` (2026-09-10).** Every
paragraph and every scenario above this note stands exactly as promoted —
`amend-marker-reason-boundary`'s and `amend-marker-defect-reporting`'s own
notes and their narratives included — and the only promoted text this block
changes is what the flip of 2026-08-31 made untrue: ONE sentence of the
lifecycle-standing paragraph, TWO sentences of the *advisory at launch*
paragraph, and TWO bullets of the first scenario. ONE SCENARIO IS ADDED, at the
END of the block, because the resolution row reaches every class this family
emits and no scenario exercised that — stated at the `(family, repository,
path)` grain the uncited-resolution rule keys on, never at finding-class grain,
which is the grain that rule has always read and is not moved here. No arm is
added or removed, no threshold moves, no disposition rule changes, no parse and
no marker grammar moves, and the set of trees over which this family speaks is
not altered by one line. THIS BLOCK MOVES NO SEVERITY AND ADDS NO ROW: the
scenario-title arm's severity constant has read `error` and
`families.FAMILY_RESOLUTION` has carried `"modified-block-currency": CONTESTED`
since 2026-08-31, so this is promoted canon catching up with running code
rather than a new decision — the same catch-up the promoted *A
modified-block-currency finding its own class map cannot place is itself a
finding* performed for its own sentence on the day that flip landed. THE
SENTENCE ABOVE STATING THAT NO FLIP IS PROPOSED FOR THE CARRIAGE LEDGER IS
CARRIED UNCHANGED AND IS STILL TRUE: its "this change" names
`add-modified-block-currency-check`, which promoted this requirement, no flip
has been ruled for that arm since, and its band is `info` today. AND
`amend-marker-defect-reporting`'S OWN `Removed from canon` MARKER IS
DELIBERATELY NOT RESTATED HERE, on this requirement's own rule that a marker is
not a carriage unit in either direction: restating it would declare a removal
this change did not perform, and its named unit — a sentence canon no longer
carries because that change removed it — matches no unit of the requirement or
of this block, which is the third ground above reporting this block for copying
a predecessor's declaration forward.

**AMENDED BY `amend-marker-declaring-nothing` (2026-09-10).** Every paragraph
and every scenario above this note stands exactly as promoted —
`amend-marker-reason-boundary`'s, `amend-marker-defect-reporting`'s and
`amend-modified-block-currency-standing`'s own notes and their narratives
included — and the only promoted text this block changes is TWO SENTENCES OF ONE
PARAGRAPH: the sentence that states the marker-defect grounds, and the sentence
that counts them. Two grounds are added, and two sentences are added beside the
replacements in that same paragraph, one scoping each new ground. TWO SCENARIOS
ARE ADDED, at the END of the block, one per ground, because a normative ground no
scenario exercises is a ground the next author re-deriving this class has nothing
to test against. No promoted scenario moves, is retitled or loses a bullet, and
the narrow reading of the second ground and the carriage it preserves are carried
word for word — this amendment adds two reports about a MARKER and withdraws
none. No arm is added or removed, no severity moves, no threshold moves, no
disposition rule changes, no parse and no marker grammar moves, this family's
registration in the resolution table is untouched, and the set of trees over
which this family speaks is not altered by one line. BOTH NEW GROUNDS HAVE A
POPULATION OF ZERO, MEASURED RATHER THAN ASSUMED on 2026-09-10 over the corpus as
it stood before this packet: of the 26 markers it carries — 17 of the two
unit-naming forms and 9 of the pairing form — NOT ONE is of `Removed from canon`
form with an empty tail, and of the thirty active MODIFIED blocks this family
reads exactly TWO carry a unit-naming marker at all, `add-chain-attestation` and
`add-composed-view-authoring`, both `Merged into`, each naming one unit that
matches its resolved basis, so a run reports no marker defect today and reports
none after this amendment. A ground whose population is zero at landing is a
ground that reports the NEXT marker written, which is the only moment at which
either silence has ever cost anybody anything. AND
`amend-modified-block-currency-standing`'S OWN `Removed from canon` MARKER IS
DELIBERATELY NOT RESTATED HERE, on this requirement's own rule that a marker is
not a carriage unit in either direction: restating it would declare a removal
this change did not perform, and its five named units — sentences canon no longer
carries because that change removed them — match no unit of the requirement or of
this block, which is the third ground above reporting this block for copying a
predecessor's declaration forward.

**AMENDED BY `amend-merged-into-empty-tail-standing` (2026-09-11).** Every
paragraph and every scenario above this note stands exactly as promoted —
`amend-marker-reason-boundary`'s, `amend-marker-defect-reporting`'s,
`amend-modified-block-currency-standing`'s and
`amend-marker-declaring-nothing`'s own notes and their narratives included —
and the only promoted text this block changes is ONE SENTENCE OF ONE PARAGRAPH:
the sentence that scopes the fifth ground to the `Removed from canon` form and
then records the `Merged into` form's empty tail as a question this requirement
does not decide. That sentence is REPLACED IN PLACE, carrying its removal-form
scoping and its whole pairing-form exclusion word for word and dropping only
the clause that says the question is undecided, because a clause saying so
cannot stand beside the sentence that decides it; ONE SENTENCE IS ADDED beside
it, stating the decision. ONE SCENARIO IS ADDED, at the END of the block,
because a rule no scenario exercises is a rule the next author re-deriving this
class has nothing to test against. NO GROUND IS ADDED AND NONE IS WITHDRAWN:
the class still states FIVE grounds, and the added sentence is a PROHIBITION on
reporting rather than a sixth ground written in the negative. No promoted
scenario moves, is retitled or loses a bullet; no arm is added or removed, no
severity moves, no threshold moves, no disposition rule changes, no parse and
no marker grammar moves, this family's registration in the resolution table is
untouched, and the set of trees over which this family speaks is not altered by
one line. NO CODE MOVES EITHER, AND THAT IS MEASURED RATHER THAN PROMISED:
`scripts/doc_health/modified_block_currency.py` already reports nothing on this
shape — its fifth-ground predicate reads `marker.form == "removed"` and each of
the other four is reached through `marker.names` or `marker.quoted`, both empty
here — and
`tests/doc-health/test_modified_block_currency.py::test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT`
has pinned exactly that since 2026-09-10, so this block states in canon the
behaviour the module already ships rather than asking for a new one. THE
POPULATION IS ZERO, MEASURED RATHER THAN ASSUMED on 2026-09-11 over the corpus
as it stood before this packet: of the 27 markers it carries — 15 of `Removed
from canon` form, 3 of `Merged into` form and 9 of the pairing form — NOT ONE
`Merged into` marker has a tail carrying no code span, and of the 29 active
MODIFIED blocks this family reads exactly TWO carry a unit-naming marker at
all, `add-chain-attestation` and `add-composed-view-authoring`, both `Merged
into` and each naming one superseded title that matches its resolved basis. AND
`amend-marker-declaring-nothing`'S OWN `Removed from canon` MARKER IS
DELIBERATELY NOT RESTATED HERE, on this requirement's own rule that a marker is
not a carriage unit in either direction: restating it would declare a removal
this change did not perform, and its two named units — sentences canon no
longer carries because that change removed them — match no unit of the
requirement or of this block, which is the third ground above reporting this
block for copying a predecessor's declaration forward.

**AMENDED BY `rule-inherited-unit-naming-marker-spent` (2026-09-11).** Every
paragraph and every scenario above this note stands exactly as
`amend-merged-into-empty-tail-standing`'s block states it —
`amend-marker-reason-boundary`'s, `amend-marker-defect-reporting`'s,
`amend-modified-block-currency-standing`'s, `amend-marker-declaring-nothing`'s
and `amend-merged-into-empty-tail-standing`'s own notes and their narratives
included — BECAUSE THIS BLOCK IS WRITTEN OVER THAT CHANGE'S OUTCOME AND NOT
OVER THE PROMOTED TEXT THAT CHANGE REPLACES:
`amend-merged-into-empty-tail-standing` is an active ratified writer of this
requirement, this change declares it as its ordered-delta parent, and
`release-realization` makes that declaration the order. THIS AMENDMENT RETIRES
NOTHING AND IS A PURE ADDITION: four sentences are added at the END of ONE
paragraph — the one ruling that a marker is not a carriage unit — and TWO
SCENARIOS are added at the END of the block, one for each half of the rule,
because a rule no scenario exercises is a rule the next author re-deriving this
class has nothing to test against and because pinning one half of a two-option
rule invites a reader to take that half for the whole. NO UNIT IS RETIRED,
REWORDED, MOVED OR DROPPED, so NO `Removed from canon` MARKER IS OWED AND NONE
IS WRITTEN — derived through `derive_units` rather than asserted. NO GROUND IS
ADDED AND NONE IS WITHDRAWN: the class still states FIVE, the added sentences
being a carriage rule and a reading of the third ground rather than a sixth
ground written in the negative; no severity moves, no threshold moves, no arm
is added or removed, no parse and no marker grammar moves, no disposition rule
changes, this family's registration in the resolution table is untouched, and
the set of trees over which this family speaks is not altered by one line. NO
CODE MOVES EITHER, AND THAT IS MEASURED RATHER THAN PROMISED: the third ground
already reports a name matching no unit of the basis and no unit of the block,
which is what `suppression` does today, and DROPPING a marker is the absence of
an edit rather than an edit — so this block states in canon which of two
standing options is lawful and asks the module for nothing it does not already
do. THE POPULATION IS MEASURED RATHER THAN ASSUMED, on 2026-09-11 over the
corpus as it stood before this packet: of the 18 markers the promoted
specifications carry — 15 of `Removed from canon` form, 1 of `Merged into` form
and 2 of the pairing form — SIXTEEN name at least one unit and ALL SIXTEEN ARE
SPENT, every unit every one of them names being absent from the requirement
that carries it, across THIRTEEN requirements in SEVEN promoted
specifications; and of the 29 active MODIFIED blocks this family reads, TWO
carry a unit-naming marker, both of the `Merged into` form and each naming one
unit that matches its resolved basis, so a run reports NO marker defect before
this amendment and none after it. AND
`amend-merged-into-empty-tail-standing`'S OWN `Removed from canon` MARKER IS
DELIBERATELY NOT RESTATED HERE — the fifth consecutive amendment of this
requirement to drop its predecessor's, and the first to drop one under the rule
it is itself writing: the marker's one named unit is a sentence this
requirement's basis no longer carries, so restating it would declare a removal
this change did not perform and would report this block under the third ground
above, which is the state these added sentences exist to write down.

#### Scenario: An active block drops a scenario the requirement keeps
- **WHEN** an active change's MODIFIED block restates a promoted requirement and omits a scenario title that requirement currently carries, with no marker naming it
- **THEN** the run MUST emit an `error` finding against the active delta's own path, naming each omitted scenario title and the promoted spec it was read from
- **AND** the finding MUST cause a run configured `--fail-on error` to fail, and MUST NOT cause a run configured `--fail-on critical` to fail
- **AND** the finding MUST carry the `contested` resolution class

#### Scenario: A deletion is declared by marker
- **WHEN** the MODIFIED block carries a `Removed from canon by` or `Merged into` marker naming a unit as a code span, and that unit is absent from the block
- **THEN** that unit MUST NOT be reported
- **AND** the suppression MUST extend to exactly the units named and to no others

#### Scenario: A genuinely removed scenario title carries its bullets with it
- **WHEN** a `Removed from canon` marker names a scenario title that is absent from the block, and the block adds NO scenario title the promoted requirement does not already carry
- **THEN** the bullets that scenario carried in canon MUST NOT be reported either, the title's removal declaring them
- **AND** a bullet of that scenario that DOES appear elsewhere in the block MUST be treated as carried

#### Scenario: A removal marker is used where the block adds a replacement scenario
- **WHEN** a `Removed from canon` marker names a scenario title AND the block adds a scenario title the promoted requirement does not carry
- **THEN** the removed title's bullets MUST NOT be suppressed by that marker, the shape being a retitle rather than a removal however it is labelled
- **AND** every such bullet the block does not carry somewhere MUST be reported, unless it is itself named in a `Removed from canon` marker as a bullet

#### Scenario: A marker names a unit the block still carries
- **WHEN** a marker names a scenario title or body unit that the block does in fact restate
- **THEN** the run MUST report the marker itself, a declaration that does not describe the block being unusable as evidence about it

#### Scenario: A block does not carry canon's body text or a scenario bullet
- **WHEN** an active MODIFIED block does not carry a body unit of the promoted requirement, or one of its scenario bullets, as a unit of the same kind after whitespace normalization
- **THEN** the run MUST emit one `info` finding for that requirement listing every uncarried unit
- **AND** the finding MUST NOT assert that the divergence is unintended, the arm having no means to distinguish a rewording from stale text

#### Scenario: A block retitles a scenario and drops its bullets
- **WHEN** a block replaces a scenario title with a new one, declares the replacement by marker, and does not carry every bullet the superseded scenario carried
- **THEN** the uncarried bullets MUST still be reported, the bullet comparison running across all bullets of the block rather than within the scenario that restates them

#### Scenario: Two active changes modify one requirement and one declares
- **WHEN** two or more active changes carry a MODIFIED block for the same capability and requirement title, and exactly one declares its deltas relative to another by naming that change as a whole token in its own `proposal.md`
- **THEN** the declaring change MUST be treated as the later writer, and its block MUST be measured against the declared sibling's outcome rather than against canon
- **AND** an addition the sibling's block makes that the declaring block does not carry MUST be reported against the declaring delta's path
- **AND** no folder name, commit timestamp, or `created:` date MUST be consulted to decide which writer is later

#### Scenario: Two active ratified changes modify one requirement and the ordering is undeclared
- **WHEN** two active ratified changes carry a MODIFIED block for one promoted requirement and neither names the other as `release-realization` requires
- **THEN** the run MUST report the undeclared ordering against both blocks, no reader being able to tell which text canon will keep
- **AND** where both declare relative to each other, the run MUST report that as well, mutual declaration deciding nothing
- **AND** each block MUST meanwhile be measured against canon, the only basis a reader can name while no declaration stands

#### Scenario: A change renames a requirement and modifies it in one delta
- **WHEN** a MODIFIED block names a title canon does not carry, and the change's own `## RENAMED Requirements` block renames a promoted requirement to that title
- **THEN** the block MUST NOT be reported as unresolved
- **AND** the three arms MUST compare it against the promoted requirement under its OLD name, a rename changing a title rather than the content the block must carry

#### Scenario: A MODIFIED title resolves to an active sibling's addition
- **WHEN** a MODIFIED block names a requirement canon does not carry, and an active sibling change ADDS or RENAMES that title
- **THEN** the block MUST NOT be reported as unresolved, the promoted requirement being pending rather than absent

#### Scenario: A MODIFIED title resolves to nothing at all
- **WHEN** a MODIFIED block names a capability and requirement title carried neither by the promoted spec, nor by the change's own `## RENAMED Requirements` block, nor by any active change's ADDED or RENAMED block
- **THEN** the run MUST emit a finding naming the unresolved title, a block modifying nothing being a block whose promotion adds text nobody reviewed as an addition

#### Scenario: A finding is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an active delta path, and a `cite`
- **THEN** findings on that path MUST be suppressed, or only the named requirement's findings where the entry carries a `requirement` key
- **AND** an entry without a `cite`, or an entry naming another family, MUST suppress nothing

#### Scenario: No repository in scope carries active changes
- **WHEN** no repository in the run's scope has an `openspec/changes/` directory the family can read
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted
- **AND** a scope that carries active changes but no `## MODIFIED Requirements` block among them MUST NOT be reported as skipped, the family having run and found nothing

#### Scenario: A marker's reason quotes a code span
- **WHEN** a unit-naming marker's tail carries a ` — ` separator standing outside every code span, and a code span falls after that separator
- **THEN** that span MUST NOT be read as a unit the marker names, a reason being prose that quotes rather than a declaration
- **AND** the units named MUST be exactly the spans that close before that separator, and the reason MUST be everything after it
- **AND** the units the span would have named MUST therefore remain subject to the carriage arms, an author who only mentioned a unit having declared nothing about it

#### Scenario: A marker's tail carries no separator outside a code span
- **WHEN** a unit-naming marker's tail carries no ` — ` separator standing outside every code span, a separator INSIDE a span being that unit's own bytes rather than a boundary
- **THEN** every code span after the closing colon MUST name a unit
- **AND** the marker MUST carry no reason, which is the form the written-out `Merged into` example above is in

#### Scenario: A marker's reason quotes a unit the block does not carry
- **WHEN** a code span standing after a unit-naming marker's reason separator, and not also named before it, matches a unit of the requirement's basis exactly, and neither the block nor any marker in it accounts for that unit
- **THEN** the run MUST report the marker itself in the `info` band, the span having been read as prose while the unit it had in mind went undeclared
- **AND** the unit MUST remain subject to the carriage arms, the report being added beside that carriage rather than in place of it
- **AND** a code span inside a reason that matches NO unit of the requirement's basis MUST NOT be reported, a reason being prose that quotes and this corpus's markers quoting one routinely

#### Scenario: A marker names something no unit matches
- **WHEN** a marker names a code span matching no unit of the requirement's basis and no unit of the block
- **THEN** the run MUST report the marker itself in the `info` band, a declaration about nothing being unusable as evidence about the block
- **AND** the name MUST suppress nothing, which is the reading this family has always taken and is unchanged by the report

#### Scenario: This family stops reporting a path without a citation
- **WHEN** this family emitted one or more findings — of ANY class, the `info` carriage ledger included — at a repository and delta path the previous report carried, the next report carries NO finding of this family at that repository and path, and no OpenSpec change or recorded disposition cites the resolution
- **THEN** the run MUST emit the uncited-resolution `error` this capability's contested-finding rule defines, the family's resolution row having no per-class grain to hold one class out of it
- **AND** a finding of ONE class that stops being reported while ANY other finding of this family is still emitted at that same repository and path MUST NOT raise that error, the rule keying on `(family, repository, path)` alone, so the key never leaves the current report
- **AND** the disappeared finding's own severity MUST NOT be read as moved by that classification, the resolution class and the severity being separate fields

#### Scenario: A marker names a unit the block itself adds
- **WHEN** a marker names a code span matching no unit of the requirement's basis and matching a unit the block itself states
- **THEN** the run MUST report the marker itself in the `info` band, a block declaring removed from canon a unit canon never carried having declared nothing about canon and nothing about the block
- **AND** the name MUST suppress nothing, and the addition it matches MUST NOT be reported for being named, an addition being text no arm of this family reads

#### Scenario: A marker of removal form declares nothing at all
- **WHEN** a paragraph of `Removed from canon` marker form carries no code span after its closing colon, so that it names no unit and quotes none
- **THEN** the run MUST report the marker itself in the `info` band, a declaration naming nothing being unusable as evidence about the block while the paragraph is exempt from carriage for being of marker form
- **AND** a marker of the pairing form whose tail carries no code span MUST NOT be reported on this ground, that form naming no units by construction and its silence being correct

#### Scenario: A merge marker's tail names no superseded title
- **WHEN** a paragraph of `Merged into` marker form carries no code span after its closing colon, so that it names no superseded title and quotes none, its destination standing complete in its prefix
- **THEN** the run MUST NOT report the marker on the fifth ground, that ground being read on the `Removed from canon` form alone, and MUST NOT report it on any of the other four either, each of those being reached through a name or a quoted span such a marker does not carry
- **AND** the silence MUST be read as this requirement's ruling that such a marker declares what its form declares, rather than as a ground this requirement has left unwritten
- **AND** a code span a `Merged into` marker's reason DOES quote MUST remain subject to the second ground, the silence covering a tail with no code span in it and not the form as such

#### Scenario: A later block drops an inherited unit-naming marker
- **WHEN** an active MODIFIED block restates a requirement whose basis carries a unit-naming marker, and every unit that marker names has left canon by the act the marker declares
- **THEN** the block MUST NOT be reported for omitting that marker, a marker being no carriage unit in either direction and a marker whose act is complete being spent
- **AND** the omission MUST NOT be read as undeclaring the removal, the archived delta remaining the durable record of the act

#### Scenario: A later block carries an inherited unit-naming marker forward
- **WHEN** an active MODIFIED block carries such a marker forward instead, its named unit matching no unit of the requirement's basis and no unit of the block
- **THEN** the run MUST report the marker itself in the `info` band on the third ground, exactly as it reports any other name matching neither side
- **AND** the report MUST NOT be read as a new ground, as a new severity or as a defect of the carriage arms, the name suppressing nothing and the block's own carriage being measured unchanged
