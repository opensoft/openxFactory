# Feature Specification: F1 — the modified-block-currency family module and its registrations

**Feature Branch**: `019-modified-block-currency-family`

**Created**: 2026-08-27

**Status**: Draft

**Input**: User description: "Speckit F1 of add-modified-block-currency-check: the modified-block-currency doc-health family module — active-change delta reader, promoted-requirement reader, MODIFIED-section parser, normative unit derivation (backtick masking, sentence split, bullet and dated-note units), same-kind exact matching, the three arms (scenario-title completeness WARNING, carriage ledger INFO, title resolution / by-declaration two-writers WARNING), the reserved-marker parser (Removed from canon / Merged into), own-RENAMED-first title resolution, disposition read reused from promotion_fidelity — plus its registrations in FAMILIES and FAMILY_IDS, landed in the same commit as the owed MODIFIED block on Deterministic check families (8 → 8 scenarios, relative to add-family-enumeration-check)."

**Realizes**: `openspec/changes/add-modified-block-currency-check` § 2 (tasks
2.1–2.10) — the first of four Speckit features that build that change. The
packet was ratified 2026-08-27 by Brett, verbatim "Ratify as-is", on the text
at `06c7475a`; its two spec deltas (`doc-health` ADDED, `document-lifecycle`
ADDED) are this feature's binding inputs and nothing here reopens them. The
five decisions in the proposal's § Orchestrator Decisions were flagged for veto
and were NOT vetoed at that ratification, which is not the same as
affirmatively ruled; this feature builds them as written and inherits their
flags. Two questions WERE ruled in that round and are built as rulings: § 7.3
(two-writer ordering, verbatim "By declaration") and § 7.5 (the packet's own
origin admission).

**Scope boundary**: F1 only. The exhaustive regression-fixture catalogue (F2,
packet § 3), the self-gate against this repository's own tree with its
predicted movement it asserts (F3, § 4 — the figures live in one place,
`plan.md` § Predicted movement), and the report section,
action line and workflow-boundary pin (F4, § 5) are named successors and are
explicitly OUT of scope. F1 leaves the hooks each of them needs and builds
nothing they own.

## Clarifications

### Session 2026-08-27

**No `[NEEDS CLARIFICATION]` markers were raised.** The ratified delta settles
every question this feature has to answer, including the ones a normal
specification would leave to an implementation: unit derivation, the matching
rule, the marker grammar, the ordering rule, the severities, and the launch
posture are all normative in the delta's own text. Four points were resolved by
READING the delta closely rather than by asking, and each is recorded in
Assumptions below with the line that settles it, because an implementer who did
not notice them would build something the delta forbids:

- The reason clause of a `Removed from canon` marker is OPTIONAL: marker FORM is
  anchored on the complete prefix alone (`specs/doc-health/spec.md`:125–129),
  and the delta's own written-out `Merged into` example carries no reason
  (:189).
- Unit matching is CASE-SENSITIVE. "No normalization beyond it applies" (:84–90)
  forbids the casefolding `promotion_fidelity.norm` performs, so that helper
  cannot be reused for units even though it is reused for the disposition key.
- The scenario-title arm's severity must be a SEPARATE named constant from the
  title-resolution arm's, both `warning` today, because the flip § 7.2 reserves
  moves the scenario-title arm ALONE.
- A group of more than two active MODIFIED writers of one requirement is
  evaluated over the group, not pairwise; the population is zero today
  (packet § 6.7) and the delta's scenario says "two or more" (:262).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The packet author is shown the scenario they were about to delete (Priority: P1)

A session authoring or amending an OpenSpec change writes a
`## MODIFIED Requirements` block for a promoted requirement. Canon has moved
since the block was written — or the author restated only the scenario their
change touches — so the block silently holds the deletion of scenarios the
requirement still carries. Today `openspec validate --strict` is green
throughout and a human catches it at an archive gate, or does not. This story
delivers the finding, at authoring time, against the delta's own path, naming
each omitted scenario title.

**Why this priority**: It is the arm that carries the family's gate and the arm
that reports the class at the granularity the defect occurs at. Two of the nine
items of the #351 instance are this arm; the other seven are US2's. Without it
the feature reports nothing precise.

**Independent Test**: Give the family a fixture with one promoted requirement
carrying several scenarios and one active delta whose MODIFIED block restates a
subset, with no marker. The run names every omitted title and nothing else. The
value — the deletion is visible before it can happen — is delivered with no
other arm built.

**Acceptance Scenarios**:

1. **Given** a promoted requirement carrying eight scenario titles and an
   active change whose MODIFIED block for it restates one, **When** the family
   runs, **Then** it emits a `warning` finding against the active delta's own
   path naming all seven omitted titles and the promoted spec they were read
   from.
2. **Given** the same fixture, **When** the run is configured `--fail-on error`
   or `--fail-on critical`, **Then** the run does not fail on this family.
3. **Given** a block that restates every scenario title canon carries, but
   re-wraps every paragraph it carries, **When** the family runs, **Then** it
   reports nothing from this arm — whitespace normalization being the only
   normalization applied.
4. **Given** an active change whose lifecycle standing is `draft`, **When** the
   family runs, **Then** its block is read exactly as a `ratified` one is, the
   reading scope being deliberately wider than the two-writers obligation.

---

### User Story 2 - The reviewer reads a ledger of what the block does not carry (Priority: P2)

A reviewer, or the author at the moment of amendment, needs the list of body
clauses and scenario bullets the block does not carry — the clause-granular
half of the class, which is where six of #351's nine items lived. The list is
editorial: it cannot tell a deliberate rewording from stale text, and it says
so rather than claiming a defect.

**Why this priority**: It is the half the counting gates cannot see and the
half a human verification had to do by hand at PR #358. It is second because
its population is standing by construction — every legitimate MODIFIED block
edits something — so it informs rather than gates.

**Independent Test**: One fixture whose block widens one canon bullet at both
ends and drops two body sentences. One `info` finding for that requirement
lists exactly three units, and the widened bullet proves that containment is
not carriage.

**Acceptance Scenarios**:

1. **Given** a block that does not carry a body unit of the promoted
   requirement, or one of its scenario bullets, as a unit of the same kind
   after whitespace normalization, **When** the family runs, **Then** it emits
   exactly ONE `info` finding for that requirement listing every uncarried
   unit.
2. **Given** a block bullet that CONTAINS canon's bullet verbatim as a
   substring, widened at either end, **When** the family runs, **Then** canon's
   bullet is reported as uncarried.
3. **Given** a block that retitles a scenario, declares the retitle by marker,
   and drops bullets the superseded scenario carried, **When** the family runs,
   **Then** the dropped bullets are still reported — bullets being compared
   against ALL bullets of ALL scenarios in the block, never scenario by
   scenario.
4. **Given** a requirement body carrying backticked tokens with internal
   periods, a bullet list, and a dated bold note spanning several sentences,
   **When** units are derived, **Then** no unit boundary falls inside a
   backticked span, each bullet is one unit, and the note is ONE unit — so an
   edit to the note's third sentence reports the note once.
5. **Given** any ledger finding, **When** its rule text is read, **Then** it
   does not assert that the divergence is unintended.

---

### User Story 3 - A deliberate deletion is declared once and stops being reported (Priority: P2)

Removing a scenario or a clause is a normal governance act. The author declares
it by a reserved marker inside the block — `Removed from canon by <change-id>
(<date>):` naming each unit as a code span, or ``Merged into `<destination>` by
<change-id> (<date>):`` where two scenarios legitimately become one — and the
family goes quiet about exactly those units and no others.

**Why this priority**: Without it US1 and US2 are unusable: the corpus's one
standing scenario-arm finding is a deliberate rename, and an advisory nobody
can discharge is an advisory nobody reads. It is not P1 only because the
reports it silences must exist first.

**Independent Test**: One fixture with a valid marker naming two of three
absent units. The two named are silent, the third is reported, and a second
fixture whose marker names a unit the block still restates reports the marker
itself.

**Acceptance Scenarios**:

1. **Given** a marker naming a unit as a code span, and that unit absent from
   the block, **When** the family runs, **Then** that unit is not reported, and
   the suppression extends to exactly the units named.
2. **Given** a marker naming a scenario title absent from the block, and a
   block that adds NO scenario title the promoted requirement does not already
   carry, **When** the family runs, **Then** the bullets that scenario carried
   in canon are not reported either, and one of those bullets appearing
   elsewhere in the block is treated as carried.
3. **Given** a `Removed from canon` marker naming a scenario title AND a block
   that adds a scenario title the promoted requirement does not carry, **When**
   the family runs, **Then** the removed title's bullets are NOT suppressed —
   that shape is a retitle whatever the marker calls it — and every such bullet
   the block does not carry somewhere is reported unless itself named as a
   bullet in a `Removed from canon` marker.
4. **Given** a marker naming a scenario title or body unit the block does in
   fact restate, **When** the family runs, **Then** the marker itself is
   reported.
5. **Given** a paragraph that merely quotes, templates or describes a marker —
   as both of this packet's own deltas do, in prose that promotes into canon —
   **When** units are derived, **Then** it is NOT of marker form and remains an
   ordinary carriage unit.
6. **Given** a named unit that itself contains backticks, fenced with a longer
   run as CommonMark provides, **When** the marker is parsed, **Then** the unit
   is extracted whole rather than truncated at its first inner backtick.
7. **Given** a `Merged into` marker, **When** it is parsed, **Then** its
   destination title is not read as a named unit.
8. **Given** a promoted requirement that already carries a marker paragraph,
   **When** the ledger runs, **Then** the marker is not a carriage unit and no
   later block is required to restate it.
9. **Given** a dated bold note that is not one of the two reserved forms,
   **When** the family runs, **Then** it declares nothing and suppresses
   nothing.

---

### User Story 4 - A block that modifies nothing, or that races a sibling, is resolved rather than guessed (Priority: P3)

A MODIFIED block whose capability and requirement title match no promoted
requirement is either lawful (the change renames it itself, or an active
sibling adds it) or a block whose promotion adds text nobody reviewed as an
addition. And where two active changes both MODIFY one promoted requirement,
the ordering is decided by the declaration `release-realization` already
requires — never by a date.

**Why this priority**: Its population on this repository is zero today
(packet § 6.7), so it protects rather than reports. It is still F1 work because
without it the arms above compare nothing where they should compare everything
— every rename-and-amend change would be reported as unresolved.

**Independent Test**: Four fixtures: own-RENAMED resolution, sibling-ADDED
resolution, resolves-to-nothing, and a two-writers pair with exactly one
declaring. Each asserts the resolution taken, not merely that something fired.

**Acceptance Scenarios**:

1. **Given** a MODIFIED block naming a title canon does not carry, and the
   change's own `## RENAMED Requirements` block renaming a promoted requirement
   to that title, **When** the family runs, **Then** the block is not reported
   as unresolved and the three arms compare it against canon under the OLD
   name.
2. **Given** a MODIFIED block naming a requirement canon does not carry, and an
   active sibling change that ADDS or RENAMES that title, **When** the family
   runs, **Then** the block is not reported as unresolved — the promoted
   requirement being pending rather than absent.
3. **Given** a MODIFIED block naming a capability and title carried neither by
   the promoted spec, nor by the change's own RENAMED block, nor by any active
   change's ADDED or RENAMED block, **When** the family runs, **Then** it emits
   a finding naming the unresolved title.
4. **Given** two or more active changes carrying a MODIFIED block for one
   capability and requirement title, exactly one of which names another as a
   whole token in its own `proposal.md`, **When** the family runs, **Then** the
   declaring change is treated as the later writer and its block is measured
   against the declared sibling's outcome rather than against canon — a BASIS
   SUBSTITUTION and nothing more — so an addition the sibling's block makes
   that the declaring block does not carry is reported by the carriage arms
   against the declaring delta's path, with no second finding for the same
   units.
5. **Given** a MODIFIED block whose title canon does not carry and that an
   active sibling ADDS, **When** the family runs, **Then** the block is
   compared against NOTHING — the promoted requirement being pending rather
   than absent — and no basis is synthesized from the sibling's ADDED text.
6. **Given** two active RATIFIED changes carrying a MODIFIED block for one
   promoted requirement and neither naming the other, **When** the family runs,
   **Then** the undeclared ordering is reported against both blocks, each block
   is meanwhile measured against canon, and the same is reported where both
   declare relative to each other.
7. **Given** a declaration naming a change id that occurs only INSIDE a longer
   change id, **When** the declaration is read, **Then** it satisfies nothing —
   the match being on whole tokens.
8. **Given** an UNRATIFIED sibling, **When** the two-writers arm runs, **Then**
   no reference obligation is created, `release-realization`'s `ratified`
   scoping not being widened here.
9. **Given** any two-writers evaluation, **When** the ordering is decided,
   **Then** no folder name, commit timestamp or `created:` date is consulted.

---

### User Story 5 - The family arrives as a registered family, in one commit with the enumeration it moves (Priority: P1)

The module is only reachable through the report a session actually reads if it
is registered. Registering a twenty-second family also moves the numerals of
`doc-health`'s own "Deterministic check families" requirement, which is still
enumerated in prose. The owed MODIFIED block and the registration are ONE
commit, and that commit is GATED: it cannot land while
`add-family-enumeration-check` is active, because the live-registry check reads
THAT packet's restatement too and this change cannot edit it. So the order is
ruled — that change archives, this branch merges `main`, and only then does the
registration land, with its block written against canon.

**Why this priority**: It is the acceptance condition of the whole feature. An
unregistered module reports nothing, and a registration whose enumeration block
is missing or wrong cannot land.

**Independent Test**: On the feature tree, `fam_family_enumeration` reads zero
and the doc-health suite is green — the same call that read three findings when
the block was written into a registry-less tree.

**Acceptance Scenarios**:

1. **Given** a tree in which `add-family-enumeration-check` is STILL ACTIVE,
   **When** a twenty-second family is registered, **Then**
   `fam_family_enumeration` reports three findings against THAT packet's delta
   path — so the registration is withheld, and this is asserted rather than
   assumed.
2. **Given** that change ARCHIVED and merged into this branch, **When** the
   module is registered in `FAMILIES` and `FAMILY_IDS` in the same commit as
   the owed block written against canon, **Then** `fam_family_enumeration`
   reports zero findings on both halves, all eight scenario titles are
   restated, the three dated bold notes are carried verbatim, and the
   per-requirement count is recorded as 8 → 8.
3. **Given** the same commit, **When** the family runs against this
   repository's own tree, **Then** the ONE carriage-ledger finding this block
   draws against itself is present and expected — advisory, predicted in the
   packet's own table, and not a regression.
4. **Given** the registration, **When** the lifecycle-scan-set classification
   is read, **Then** the family is a declared NON-reader, and the assertion
   that the non-reader count equals the registry size minus four still holds.
5. **Given** the registration, **When** `FAMILY_RESOLUTION` is read, **Then**
   the family is deliberately absent, with the reason recorded beside the
   registration.

---

### Edge Cases

- **No active changes at all in scope.** The family is reported SKIPPED with
  its reason, never silently omitted. A scope that DOES carry active changes
  but no `## MODIFIED Requirements` block among them is NOT skipped: the family
  ran and found nothing, and canon's skip rule is "cannot run", not "found
  nothing".
- **A capability with no promoted spec at all.** Every MODIFIED title in it
  resolves to nothing unless an active sibling adds it; the resolution arm is
  what reports it, and the carriage arms have nothing to compare.
- **A marker wrapped across several lines.** Whitespace normalization applies
  to a marker as to every other unit, so it is still one marker.
- **A marker whose change-id or date is malformed.** The paragraph is not of
  marker form, so it declares nothing and is an ordinary carriage unit — a
  broken declaration must never buy silence.
- **A block that carries a bullet verbatim under a DIFFERENT scenario.** The
  bullet is carried and the ledger says nothing about it. Deliberate: the arm
  reads carriage, not meaning, and cannot tell a sensible relocation from a
  careless one.
- **Two runs over one tree.** Findings are byte-identical, ordering included.
- **A single-repo run.** `health/dispositions.yaml` lives at the aggregation
  root, so no disposition applies in that scope — the pre-existing shape of the
  mechanism, not a choice this family makes.
- **More than two active MODIFIED writers of one requirement.** Evaluated over
  the group; anything other than exactly one declaration is reported. Zero
  such groups exist today.

## Requirements *(mandatory)*

### Functional Requirements

**Reading and basis**

- **FR-001**: The family MUST read every active change's
  `## MODIFIED Requirements` blocks from `openspec/changes/*/specs/*/spec.md`
  with `openspec/changes/archive/` excluded, and MUST read them regardless of
  the change's lifecycle standing.
- **FR-002**: The family MUST read the promoted requirement from the
  CHECKED-OUT tree's `openspec/specs/<capability>/spec.md`. It MUST NOT offer
  or consume a live-`main` basis; that basis belongs to promotion fidelity
  alone and would measure a delta the read tree does not carry. This is
  ASSERTED, not merely intended: the family reads no basis field from the
  context, publishes no `FAMILY_NOTES` entry, and reaches no git ref.
- **FR-003**: Every finding MUST land on the active delta's own path, and MUST
  name the promoted spec it was read from in its rule text.

**Unit derivation (normative)**

- **FR-004**: Backticked spans MUST be masked before any sentence split, so no
  unit boundary falls inside `` `.openspec.yaml` ``, `` `promotion_fidelity.py` ``
  or any other backticked token carrying an internal period. The unit's
  reported text MUST be the original text, not the masked text.
- **FR-005**: In the requirement BODY — everything above the first
  `#### Scenario:` — each bullet line MUST be one unit with its list marker
  stripped; each dated bold note MUST be one undivided unit; and every other
  paragraph MUST be split into sentences at a period, question mark or
  exclamation mark followed by whitespace or the end of the paragraph.
- **FR-006**: In the SCENARIOS, each `#### Scenario:` heading MUST be one title
  unit and each bullet line MUST be one bullet unit.
- **FR-007**: A paragraph of reserved-marker form MUST NOT be a unit of either
  kind, in canon or in a block, in either direction.

**Matching**

- **FR-008**: A canon unit MUST be treated as CARRIED only by a block unit of
  the SAME KIND — body by body, scenario title by scenario title, scenario
  bullet by scenario bullet — matched in full after whitespace normalization,
  where normalization collapses runs of whitespace to a single space and strips
  leading and trailing whitespace and does nothing else.
- **FR-009**: Substring containment MUST NOT count as carriage. A block unit
  that contains a canon unit has replaced it and the canon unit MUST be
  reported.
- **FR-010**: No similarity, near-match, stemming, casefolding or
  punctuation-insensitive rule MUST be used anywhere in unit comparison.

**The three arms**

- **FR-011**: The scenario-title completeness arm MUST report, at `warning`,
  every `#### Scenario:` title the promoted requirement carries that does not
  appear as a scenario title in the block and is not declared by marker.
- **FR-012**: The carriage-ledger arm MUST report, at `info` and as AT MOST ONE
  finding per requirement listing every uncarried unit, each body unit and each
  scenario bullet of the promoted requirement the block does not carry.
  Scenario bullets MUST be compared against ALL bullets of ALL scenarios in the
  block. The finding's text MUST NOT assert that a divergence is unintended.
- **FR-013**: The title-resolution arm MUST resolve a MODIFIED block's
  capability and requirement title in this order: the promoted spec; then the
  change's OWN `## RENAMED Requirements` block, where a rename to this title
  makes the three arms run against canon under the OLD name; then a
  requirement an active sibling change ADDS or RENAMES. A title resolving to
  none of those MUST be reported at `warning`.
- **FR-014**: Where two or more active changes carry a MODIFIED block for one
  capability and requirement title, ordering MUST be BY DECLARATION: the change
  whose own `proposal.md` names a sibling's change id as a WHOLE TOKEN is the
  later writer, and its block MUST be measured against that sibling's outcome
  rather than against canon. **That substitution is the ONLY effect of a
  declaration.** The three arms then run unchanged against the substituted
  basis, so an addition the sibling makes that the declaring block does not
  carry is reported by the CARRIAGE ARMS against the declaring delta's path —
  the delta's own scenario requires that it be reported, not that a fourth
  finding say so, and a separate resolution finding would report at `warning`
  the same units the ledger already reports at `info`. The resolution arm
  itself MUST report exactly two things and nothing else: (i) a title that
  resolves to no requirement, and (ii) an undeclared or mutual ordering between
  two active RATIFIED writers. Exactly one of two active RATIFIED writers MUST
  declare: neither declaring MUST be reported against both blocks, both
  declaring MUST be reported, and where no declaration stands each block MUST
  be measured against canon. No folder name, commit timestamp or `created:`
  date MUST be consulted. An unratified sibling MUST create no declaration
  obligation.

**The reserved marker**

- **FR-015**: A marker MUST be recognized by FORM and never by prose: ONE
  paragraph, read after the same whitespace normalization every unit gets, that
  BEGINS with one of exactly two prefixes COMPLETE — the bold run, a resolvable
  change-id, an ISO date in parentheses, and the closing colon —
  `**Removed from canon by <change-id> (<YYYY-MM-DD>):**` or
  ``**Merged into `<destination scenario title>` by <change-id> (<YYYY-MM-DD>):**``.
  A paragraph that quotes, templates or describes a marker MUST NOT be of
  marker form.
- **FR-016**: Named units MUST be extracted as CommonMark code spans following
  the colon, in order, honouring a longer backtick fence where the unit itself
  contains backticks. The reason MUST begin at the first ` — ` separator
  standing outside every code span, and MUST NOT be found by splitting on
  punctuation — canon's own wording: "THE REASON SHALL BEGIN AT THE FIRST
  ` — ` SEPARATOR STANDING OUTSIDE EVERY CODE SPAN: the units named are the
  spans that close before that separator, the reason is everything after it,
  and a code span that falls inside the reason is prose the reason quotes
  rather than a unit the marker names."
  (`openspec/specs/doc-health/spec.md`:1725–1730).
  *(Amended 2026-09-09 to match canon after `amend-marker-reason-boundary`
  (#739); this bullet previously stated the retired last-code-span rule.)*
  A marker MUST remain of marker form when no reason is present.
- **FR-017**: The `Merged into` destination MUST NOT be read as a named unit.
- **FR-018**: A marker MUST suppress only units it names AND that are in fact
  absent from the block. A marker MUST itself be reported, as a FOURTH finding
  class — "marker defects" — carrying the ledger's `info` severity and never
  `error`, on ANY OF THREE GROUNDS — canon's own wording:
  "A MARKER SHALL ITSELF BE REPORTED ON ANY OF THREE GROUNDS, each of them
  one finding at the `info` band this family's marker-defect class already
  carries: it names a unit the block still carries; or a code span standing
  INSIDE its reason matches EXACTLY a unit of the requirement's basis that
  the block does not carry and that no marker declares removed, the boundary
  above reading that span as prose rather than as a name, so that its author
  declared nothing about a unit they plainly had in mind; or it names
  something matching no unit of the requirement's basis and no unit of the
  block."
  (`openspec/specs/doc-health/spec.md`:1744–1751). The second ground MUST be
  read narrowly, on the exact match and never on the span's position alone, and
  MUST NOT withdraw the carriage arms from the unit the span would have named
  (:1754–1760).
  *(Amended 2026-09-10 to match canon after `amend-marker-defect-reporting`
  (#850); this bullet previously stated the ONE-ground rule — a marker naming a
  unit the block still carries — which is now the first of the three.)*
  Producing the defect without emitting it would leave the delta's "SHALL
  itself be reported" unrealized in a function nothing calls.
- **FR-019**: Where a `Removed from canon` marker names a scenario title AND
  the block adds no scenario title canon does not already carry, the bullets
  that scenario carried in canon MUST also be treated as declared removed —
  unless they appear as bullets elsewhere in the block, in which case they are
  carried and nothing is reported about them either way.
- **FR-020**: Where the block DOES add a scenario title canon does not carry, a
  `Removed from canon` marker MUST NOT suppress the removed title's bullets;
  each such uncarried bullet MUST be reported unless itself named as a bullet
  in a `Removed from canon` marker.
- **FR-021**: A dated bold note that is not one of the two reserved forms MUST
  declare and suppress nothing.

**Dispositions, skip, determinism, launch posture**

- **FR-022**: A recorded disposition in the aggregation checkout's
  `health/dispositions.yaml` naming THIS family, carrying a `cite`, optionally
  narrowed by a `requirement:` key, MUST suppress the findings it names, and
  nothing else MUST suppress. The reader MUST be the one
  `promotion_fidelity.load_dispositions` / `disposed` already implements, read
  under this family's own name; no second reader MUST be written.
- **FR-023**: The family MUST be reported SKIPPED, with its reason, where no
  repository in scope has an `openspec/changes/` directory it can read. A scope
  carrying active changes but no `## MODIFIED Requirements` block among them
  MUST NOT be reported as skipped.
- **FR-024**: Every finding MUST carry `warning` severity for the
  scenario-completeness and title-resolution arms and `info` for the carriage
  ledger; the family MUST be ABSENT from `FAMILY_RESOLUTION`. The
  scenario-completeness arm's severity MUST be a named module constant DISTINCT
  from the other arms' constants, so that the later flip — which moves that arm
  alone, together with a `FAMILY_RESOLUTION` row — is one line beside one row
  and cannot drag another arm with it.
- **FR-025**: Two runs over one unchanged tree MUST produce byte-identical
  findings, ordering included.

**Registration and the owed enumeration block**

- **FR-026**: The family MUST be registered in `families.FAMILIES` and in
  `doc_health.FAMILY_IDS`, with a comment recording why it is deliberately
  absent from `FAMILY_RESOLUTION`, and `families.py`'s module docstring owner
  list MUST name the new module.
- **FR-027**: The family MUST be classified a NON-reader of the lifecycle scan
  set in the test that exists to fail loudly when a new family is not
  classified, and the non-reader count assertion MUST move with the registry
  size.
- **FR-028**: The registration MUST NOT land while
  `add-family-enumeration-check` is still ACTIVE. **RULED 2026-08-27 by the
  reviewing coordinator, option (a): that change archives FIRST.** The reason is
  measured, not argued: `fam_family_enumeration` checks EVERY active delta's
  restatement of "Deterministic check families" against the LIVE registry
  (`family_enumeration.py`:424-435), so the moment a twenty-second family is
  registered, that OTHER packet's still-active restatement is stale and emits
  three findings against ITS delta path — an omitted family name and two stale
  numerals. A block in THIS change's delta cannot clear them, because each
  active delta is checked independently and this change has no standing to edit
  another ratified packet's text. Measured on this branch: 0 findings with 21
  registered, 3 with 22.
- **FR-028a**: Once that archive has landed on `main` and been merged into this
  branch, the `doc-health` delta's owed `## MODIFIED Requirements` block on
  "Deterministic check families" MUST land in the SAME COMMIT as the
  registration, written relative to CANON — which by then IS
  `add-family-enumeration-check`'s promoted outcome, so there is no second
  authority to reconcile: `twenty-one` → `twenty-two`, the enumeration gaining
  `modified-block currency`, `Four of the twenty-two`, `the other eighteen
  families`, one new sentence declaring that this family reads active change
  deltas and promoted specs and therefore takes neither the governed corpus nor
  the lifecycle scan set, and one new `AND` bullet in
  `A run executes the check families`. ALL EIGHT scenario titles MUST be named
  and restated, the three dated bold notes canon carries MUST be carried
  VERBATIM, the per-requirement count 8 → 8 MUST be recorded in the commit
  message, and `fam_family_enumeration` MUST read zero against the resulting
  tree.
- **FR-028b**: The registration commit MUST also bring the enumeration
  COLLATERAL that `add-family-enumeration-check` declares as its own surface
  (`openspec/changes/add-family-enumeration-check/proposal.md`:2): the numeral
  and family-name assertions in `tests/doc-health/test_family_enumeration.py`
  and the enumeration text in its `tests/doc-health/fixtures/family-enumeration-*`
  fixture specs. A registration that moves the registry without moving those
  reds that family's own suite.
- **FR-029**: The ONE carriage-ledger finding that block draws against this
  change's own delta MUST be treated as expected and advisory — it is the
  packet's own prediction (§ 6.6) — and MUST NOT be treated as a regression or
  suppressed by a disposition.
- **FR-030**: F1 MUST NOT touch `.github/workflows/`, `report.py`'s grammars,
  any threshold, or any other family's behaviour, and `promotion-fidelity`'s
  existing tests MUST stay green unchanged.

**Evidence discipline**

- **FR-031**: Every behaviour above MUST be pinned by a behavioural test
  written to FAIL FIRST against the tree that lacks the behaviour. No F1
  behaviour ships on a text-grep assertion or on a test authored after the code
  it covers.

### Key Entities

- **Active MODIFIED block**: one `### Requirement:` block inside an active
  change's `## MODIFIED Requirements` section, identified by
  (change, capability, requirement title) and located by the delta file's own
  repository-relative path — which is where every finding lands and what a
  disposition keys on.
- **Promoted requirement**: the same title's `### Requirement:` block in the
  checked-out `openspec/specs/<capability>/spec.md`, and the only thing a block
  is measured against absent a standing declaration.
- **Normative unit**: one comparable fragment of a requirement, carrying its
  KIND (body / scenario-title / scenario-bullet), its normalized comparison
  spelling, and its original text for reporting.
- **Reserved marker**: a declaration paragraph of one of two forms, carrying
  its form, the change id and date it names, the ordered list of unit names it
  declares, an optional `Merged into` destination, and an optional reason.
- **Writer set**: the active changes carrying a MODIFIED block for one
  (capability, requirement title), together with the declarations their
  proposals make about each other — the input to the ordering rule.
- **Finding class**: one of the three arms, each with its own severity, its own
  rule grammar and its own granularity (per omitted title; one per requirement;
  per unresolved or undeclared block).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The SHAPE of the #351 instance — body clauses on the ledger, two
  scenario titles on the scenario arm, a reverted scenario line on the ledger —
  is reported by the family, naming the units rather than a count. The
  BYTE-FAITHFUL reconstruction of that instance is F2's fixture (packet § 3.1);
  what F1 owes is the behaviour it will exercise.
- **SC-002**: The SHAPE of the #329 instance — a block restating 1 of 8
  scenarios while the change's own ADDED requirement brings 7, so the
  file-level scenario count does not move — is reported with every omitted
  title named, and a second assertion pins that the flat file-level count is
  not what the family reads. F2's § 3.2 owns the full reconstruction.
- **SC-003**: Canon's own bullet, widened at either end by the block, is
  reported as uncarried — the property a containment rule loses and the
  property that reproduced PR #358's manual verification.
- **SC-004**: A scenario-complete block that re-wraps every paragraph it
  carries reports nothing.
- **SC-005**: A single marker line silences exactly the units it names and
  leaves every other divergence reported.
- **SC-006**: `fam_family_enumeration` reports zero findings against the
  feature tree, and `python3 -m pytest tests/doc-health` is green, in the same
  commit that registers the family — which is reachable ONLY after
  `add-family-enumeration-check` has archived (FR-028). Measured before that
  archive: 3 findings, on that packet's delta path, which this change cannot
  clear.
- **SC-007**: The doc-health suite's test count rises by the number of tests
  this feature adds, and every added test is shown to have failed before the
  behaviour it covers existed.
- **SC-008**: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` is green.
- **SC-009**: No run configured `--fail-on error` or `--fail-on critical` fails
  because of this family, on any tree.
- **SC-010**: A mutation round over the new module leaves no surviving mutant
  in the matching rule, the marker anchor, the same-kind constraint or the
  block-wide bullet comparison.

## Assumptions

Each of these is a reading of the ratified delta, with the line that settles
it. None is a choice this feature makes freely.

- **A1 — A `Removed from canon` marker's reason is optional.** Marker FORM is
  anchored on the complete prefix (`specs/doc-health/spec.md`:125–129); the
  reason begins at the first ` — ` separator standing outside every code span
  — canon's own wording: "THE REASON SHALL BEGIN AT THE FIRST ` — ` SEPARATOR
  STANDING OUTSIDE EVERY CODE SPAN: the units named are the spans that close
  before that separator, the reason is everything after it, and a code span
  that falls inside the reason is prose the reason quotes rather than a unit
  the marker names." (`openspec/specs/doc-health/spec.md`:1725–1730), and the
  delta's own written-out `Merged into` example carries none (:189).
  *(Amended 2026-09-09 to match canon after `amend-marker-reason-boundary`
  (#739); this reading previously cited the retired last-code-span rule at
  :142–146.)* A marker with no reason is therefore of marker form and
  declares its named units.
- **A2 — Unit comparison is case-sensitive and cannot reuse
  `promotion_fidelity.norm`.** ":84–90 — matched in full after whitespace
  normalization ... no normalization beyond it applies" forbids the casefolding
  that helper performs. The helper IS reused for the DISPOSITION key, where its
  spelling is the mechanism's own and consistency with the other families
  matters more.
- **A3 — A "dated bold note" is a paragraph that opens a bold run containing an
  ISO `YYYY-MM-DD` date.** The delta makes the note ONE undivided unit
  (:103–107) without spelling out the recognition predicate. This reading is
  the corpus's own convention, it is the predicate the marker-form test excludes
  FIRST (a marker is also a dated bold paragraph), and it is pinned against the
  real notes the corpus carries rather than asserted.
- **A4 — Groups of more than two active MODIFIED writers are evaluated over the
  group.** The delta's scenario says "two or more" (:262) and the corpus carries
  zero such groups (packet § 6.7); anything other than exactly one declaration
  in the group is reported as an undeclared ordering.
- **A5 — Severity constants are three, not one.** § 2.4 of the packet's tasks
  asks for `_LAUNCH_SEVERITY` as a module constant so the flip is one line;
  § 7.2 reserves the flip for the scenario-title arm ALONE. Both are satisfied
  by naming the arms' severities separately, with the flip-bearing one keeping
  the `_LAUNCH_SEVERITY` name the three sibling families use.
- **A6 — The disposition read needs no refactor.**
  `promotion_fidelity.load_dispositions(ctx, family)` already takes a family
  parameter and `disposed()` is already generic; `duplicate_packet.py` consumes
  both in exactly this shape. Task 2.8's "reuse that reader; do not write a
  second one" is satisfied by importing, and promotion fidelity's behaviour is
  untouched.

## Dependencies

- The ratified packet `openspec/changes/add-modified-block-currency-check`
  (proposal, design, both spec deltas, tasks) — binding input.
- `openspec/changes/add-family-enumeration-check` — **a SEQUENCING DEPENDENCY,
  not merely a reference (FR-028)**. It is active with code landed and delta
  unpromoted; its family checks every active delta's restatement against the
  live registry, so it must ARCHIVE before this feature may register. Once it
  has, canon carries its outcome and § 2.1's block is written against canon. It
  also owns the standing gate
  `test_family_enumeration.py::test_the_real_corpus_reads_zero_on_both_halves`
  that the block must keep green, and the enumeration collateral FR-028b moves.
- `scripts/doc_health/promotion_fidelity.py` — the disposition reader and the
  module shape this family follows; consumed, never modified.
- `scripts/doc_health/families.py`, `scripts/doc_health/__init__.py` — the two
  registration points.
- `tests/doc-health/conftest.py` — `make_ctx`, `FakeGit`, `FIXTURES`,
  `REPO_ROOT`; the harness every new test uses.

## Out of Scope

- The exhaustive regression-fixture catalogue of packet § 3 (F2), including the
  two historical reconstructions as FIXTURES, the tokenization fixture, the
  full marker matrix, the determinism pin and the structural launch pins. F1
  writes the behavioural tests its own code needs; F2 owns the catalogue.
- The self-gate of packet § 4 (F3): the asserted run against this
  repository's own tree against `plan.md` § Predicted movement — the single
  home for the figure, re-measured at this branch point — plus the suite and
  validate counts and the report diff against `main`.
- The report section, the action line and the workflow-boundary test of packet
  § 5 (F4). F1 emits three distinct finding classes so F4 can render them
  distinguishably; it renders nothing itself.
- Any flip of severity or `FAMILY_RESOLUTION` membership (packet § 7.2 — a
  later ruling).
- #330's shape 1, the post-archive safety net (packet § 7.1 — recorded, not
  built; this feature does not close #330).
- Any change to `promotion-fidelity`, `family-enumeration`, or any other
  family's behaviour, and any change to `.github/workflows/`, thresholds, the
  report schema or the regression-diff rule.
