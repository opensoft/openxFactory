# doc-health Specification Delta

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twenty-two check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, staged-topic template,
location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, client
identity roster composition, promotion fidelity, release-inventory drift,
duplicate packet, family enumeration, and modified-block currency.
Every check in this pass
MUST be
deterministic — identical inputs produce identical findings, with no model
calls; semantic analysis belongs to the agentic semantic sweep and the separate
document-cataloger and ideation-organizer lanes their owning capabilities
define. Check families SHALL implement promoted spec wording; staged ideation
fragments are inputs to contracts, never check definitions. The client
identity roster composition family SHALL cover only the CROSS-DOMAIN
concerns — assembling per-client fragments published by each domain and
reporting shared identity material or undeclared cross-domain reach —
because intra-repo roster conformance is a blocking domain gate rather than
an advisory report. Four of the twenty-two — status validity, standard backing,
ratified provenance, and succession integrity — SHALL additionally read the
lifecycle scan set this capability declares, so that a lifecycle header
carried by a document outside the governed corpus is still checked; the other
eighteen families and every corpus census, word count, canon-share figure,
shared-inventory entry, and catalog record SHALL be computed from the
governed corpus alone and MUST NOT move because the lifecycle scan set
exists. The promotion fidelity family reads archived spec DELTAS and promoted
SPECS — bodies rather than headers — and therefore takes neither the governed
corpus nor the lifecycle scan set as its document list; it moves no census,
word count, canon-share figure, inventory entry, or catalog record either. The
release-inventory drift family reads CONTRACT ARTIFACT BYTES — a release digest
inventory and the blobs it names — and likewise takes neither document list,
and it moves no census, word count, canon-share figure, inventory entry, or
catalog record. The duplicate packet family reads archived spec deltas ONLY
AGAINST EACH OTHER — never against canon, which by construction cannot show
that a ruling was discharged twice — and takes neither document list and moves
none of those figures either. The family enumeration family reads THIS
REQUIREMENT and the code registry that satisfies it — a promoted spec and a
Python dict, neither of them a governed-corpus document — so it likewise takes
neither document list and moves none of those figures. The modified-block
currency family reads ACTIVE CHANGE DELTAS, the promoted SPECS they have not yet
replaced, and each active change's own `proposal.md` — the last read only to
resolve whether one active writer declares its deltas relative to another, which
`release-realization` governs — so it likewise takes neither the governed corpus
nor the lifecycle scan set as its document list, and it moves no census, word
count, canon-share figure, inventory entry, or catalog record either.

**CORRECTED 2026-08-25 ON BRETT'S RULING — this block is now
SCENARIO-COMPLETE.** As first written it restated only ONE of this
requirement's scenarios. OpenSpec's `MODIFIED` REPLACES A REQUIREMENT
WHOLESALE rather than merging into it, so promoting that block would have
dropped the seven scenarios it did not restate — `Lifecycle conformance checks
fire`, `A register carries staged status`, `Drift checks fire`, `Catalog
conformance checks fire`, `Routing conformance checks fire`, `Origin
conformance checks fire`, and `Roster composition is checked across domains` —
silently, because the file-level scenario count would have stayed at 98: the
seven lost exactly offset the seven this change's ADDED requirement brings.
Caught by the byte-for-byte promotion verification at archive time, before
anything was committed. The seven are restored below VERBATIM from the promoted
spec; only the first scenario differs from canon, and it differs by TWO `AND`
bullets rather than one — only the second is this change's. The first names
`promotion fidelity`, and it is INHERITED: this delta was written on top of
`add-promotion-fidelity-check`'s text, on the assumption that the sibling would
land first. That assumption is why canon now says "nineteen check families"
while `promotion fidelity`'s own owning requirement is still inside that active
change, so the bullet's "as its owning requirement below defines" is a FORWARD
REFERENCE until the sibling archives, at which point it resolves on its own.
Recorded in issue #329 rather than papered over; it is an ordering dependency,
not a defect in either change.

**THE ORDERING DEPENDENCY RESOLVED, 2026-08-25 — appended, with the paragraph
above left exactly as ratified.** `add-promotion-fidelity-check` archived
(`560e0bd5`), so two sentences above are now historical rather than current, and
they are corrected here rather than edited in place. First: the `promotion
fidelity` bullet's "as its owning requirement below defines" is no longer a
forward reference — that requirement is promoted canon, and the bullet resolves
against it. Second: this block no longer differs from canon by TWO `AND`
bullets. Canon absorbed the inherited one when the sibling archived, so exactly
ONE bullet here is new, and it is this change's own — `duplicate packet`.
Verified at this archive gate scenario-by-scenario: 8 of canon's 8 scenarios
restated, 7 byte-identical, and the eighth differing by that single bullet and
nothing else. This change is the third and last of the three siblings that each
restated this requirement, so the chain closes here — the enumeration reaches
twenty and no further active change is left holding a version of it.

**FOURTH RESTATEMENT, AND THE FIRST ONE A CHECK VERIFIED — appended
2026-08-25, with every paragraph above left exactly as promoted.** The three
notes above record three separate repairs of this one requirement, all three
caught by a human. This block is the fourth restatement of it, and it is the
first written under `add-family-enumeration-check`: its own delta half read
this block, resolved every name here against `families.FAMILIES`, and checked
all three numerals before the change could be committed. The enumeration
reaches twenty-one and the counts are derived rather than re-typed. That the
check policing this requirement had to restate this requirement to add itself
to it is deliberate, and it is the acceptance test — a wrong restatement here
could not have landed, because the thing it would corrupt was standing at the
gate.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and the aggregation-hosted catalog snapshots as its owning requirement defines
- **AND** ideation routing MUST additionally inspect the aggregation root placement boundary and resolve explicitly referenced pinned repositories as its owning requirement defines
- **AND** proposal origin MUST validate active and archived proposal packets, support manifests, and staging-header linkage as its owning requirements define
- **AND** client identity roster composition MUST assemble the per-client roster fragments published by each pinned domain repository as its owning requirement in `client-identity-roster` defines
- **AND** promotion fidelity MUST compare each repository's archived spec deltas against its promoted specs as its owning requirement below defines
- **AND** release-inventory drift MUST compare each repository's declared bundle inventory against the blobs it names as its owning requirement below defines
- **AND** duplicate packet MUST compare each repository's archived spec deltas against each other as its owning requirement below defines
- **AND** family enumeration MUST verify this requirement's own family enumeration and counts against the code registry as its owning requirement below defines
- **AND** modified-block currency MUST compare each active change's `## MODIFIED Requirements` blocks against the promoted requirements they replace as its owning requirement below defines
- **AND** status validity, standard backing, ratified provenance, and succession integrity MUST additionally read the declared lifecycle scan set, reporting a finding against the document's own path exactly as they do for a governed-corpus document
- **AND** a family or reference check that cannot run (for example notebook drift without credentials or an unavailable external checkout) MUST be reported as skipped, never silently omitted

#### Scenario: Lifecycle conformance checks fire
- **WHEN** a governance document violates a `document-lifecycle` rule — a free-form or missing `Status:` value, an unbacked `standard` claim, a `ratified` document whose lifecycle header carries no ratification citation in either sanctioned spelling, a dangling `Ratified by:` reference, a record-citing `Ratified:` line naming none of an approver, a date, or a resolvable record path, a `ratified` document whose lifecycle header carries more than one ratification citation (one of each spelling, or the same spelling twice), a `superseded` doc without a successor, a `brainstorm` doc outside `ideation/brainstorm/`, a `staged` doc that is outside `ideation/staging/` and is not a candidate register (`Kind: register`), or a content edit to a `record` doc after capture
- **THEN** the run MUST emit a finding naming the check family, the repo, the path, and the violated rule

#### Scenario: A register carries staged status
- **WHEN** a candidate register (`Kind: register`) carries `Status: staged` outside `ideation/staging/`
- **THEN** location conformance MUST NOT emit a finding — registers are a promoted organized-state home per the `document-lifecycle` capability

#### Scenario: Drift checks fire
- **WHEN** a submodule pin lags its remote main, a contract copy diverges from its canonical source, or the lifecycle notebook projection dry-run reports nonzero add/update/delete operations
- **THEN** the run MUST emit a drift finding identifying what diverged and from which source of truth

#### Scenario: Catalog conformance checks fire
- **WHEN** governed-document coverage, catalog identity, freshness, taxonomy, provenance, override standing, or record immutability violates the promoted catalog contract
- **THEN** the run MUST emit a `document-catalog` finding with the violated requirement and evidence

#### Scenario: Routing conformance checks fire
- **WHEN** a routed idea, claim, destination, proposal manifest, repository ID or gitlink, or aggregation placement violates the promoted routing contract
- **THEN** the run MUST emit an `ideation-routing` finding with the violated requirement and evidence

#### Scenario: Origin conformance checks fire
- **WHEN** a proposal packet, support manifest, or staging-header linkage violates the promoted origin contract
- **THEN** the run MUST emit a `proposal-origin` finding with the violated requirement and evidence

#### Scenario: Roster composition is checked across domains
- **WHEN** two or more pinned domain repositories publish client identity roster fragments for the same client
- **THEN** the roster composition family assembles them and reports shared identity material or undeclared cross-domain reach
- **AND** intra-repo entry conformance is NOT reported here, because it fails the owning domain's gate instead

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
