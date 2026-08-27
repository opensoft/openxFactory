# doc-health Specification Delta

## ADDED Requirements

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
a `ratified` one, the arms below are advisory, and a finding against a draft
costs its author one line. This is a reading rule for the check and is
deliberately WIDER than the two-writers obligation below, which
`release-realization` scopes to an active RATIFIED change and which this
requirement does not widen.

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
  a MODIFIED block for ONE promoted requirement, the later SHALL be measured
  against the earlier change's outcome rather than against canon, and the
  earlier change's additions SHALL be present in the later block; where the
  earlier change is an active RATIFIED change,
  `release-realization`'s "Ordered deltas and branch vocabulary" already
  requires the later proposal to reference it, and the reference SHALL be read
  as that change's id occurring as a whole token in the later change's own
  `proposal.md` — the whole-token match the duplicate packet family already
  uses, so that one change id occurring inside a longer one satisfies nothing.

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
extract the code spans following the colon, in order, per CommonMark; the reason
is everything after the last code span's following ` — `. Semicolons and dashes
inside a unit or inside a reason are therefore irrelevant, because extraction is
by code span and never by splitting on punctuation.

**The `Merged into` destination is NOT a named unit.** It states where the
superseded scenarios went, and it is present in the block by construction —
reading it as a named unit would make every valid merge marker report itself
under the rule below. Only the code spans after the colon name units.

A marker SHALL suppress only the units it names AND that are in fact absent from
the block. A marker naming a unit the block still carries declares nothing and
SHALL itself be reported, because a declaration that does not describe the block
is a declaration no reader can rely on.

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

**A marker is NOT a carriage unit, in either direction.** A marker promotes into
canon with the requirement that carries it, and if it were a unit every later
block would have to restate every marker any predecessor ever wrote, forever.
The durable record of a deletion is the archived delta, which is where every
other archived governance act is read from.

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

**This family SHALL be advisory at launch, in both halves of what that means.**
Every finding carries `warning` severity for the scenario-completeness and
title-resolution arms and `info` for the carriage ledger, so no `--fail-on`
configuration reds on it; and the family is deliberately absent from
`FAMILY_RESOLUTION`, so its findings are not classified `contested` — a
contested finding that resolves without a citation becomes an `error` under
this capability's uncited-resolution rule, which would gate the family through
the back door on the first block anyone corrected. Raising the
scenario-completeness arm to `error` and adding the contested classification
are ONE later decision taken together by ruling, and SHALL follow the discharge
of the standing population rather than precede it. **No flip is proposed for
the carriage ledger in this change**, whose population is standing by
construction — every legitimate MODIFIED block edits something — so an
editorial band is the honest launch state; a later flip remains available and
is a ruling like any other.

#### Scenario: An active block drops a scenario the requirement keeps
- **WHEN** an active change's MODIFIED block restates a promoted requirement and omits a scenario title that requirement currently carries, with no marker naming it
- **THEN** the run MUST emit a `warning` finding against the active delta's own path, naming each omitted scenario title and the promoted spec it was read from
- **AND** the finding MUST NOT cause a run configured `--fail-on error` or `--fail-on critical` to fail

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

#### Scenario: Two active changes modify one requirement
- **WHEN** two or more active changes carry a MODIFIED block for the same capability and requirement title
- **THEN** the later change's block MUST be measured against the earlier change's outcome rather than against canon
- **AND** an addition the earlier block makes that the later block does not carry MUST be reported against the later delta's path
- **AND** where the earlier change is an active ratified change, the later change's `proposal.md` MUST name it as a whole token, as `release-realization` requires

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
