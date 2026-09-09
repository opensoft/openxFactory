---
code_surface: openxFactory — `scripts/doc_health/modified_block_currency.py` and the tests that pin it in `tests/doc-health/test_modified_block_currency.py`. TWO REPORTING GROUNDS ARE ADDED to the marker-defect class and nothing else moves: `Marker` gains one field for the code spans a reason quotes (which `parse_marker` derived and then DISCARDED, so the defect was not mechanically detectable at all), `suppression` resolves those spans and the names that match nothing, and `_arm_marker_defects` renders one finding per ground through the class's EXISTING template — whose opening is unchanged, so the existing `CLASS_MARKERS` probe places every new finding and the seventh class (`unplaced-finding drift`) stays silent. Ground one's rendered text is BYTE-IDENTICAL to the one this class shipped with. NOTHING ELSE MOVES: no parse, no severity, no threshold, no arm, no finding class, no template entry, no path, no disposition rule, no workflow, no contract member and no other family. Eleven tests are ADDED beside the existing ones (`tests/doc-health/test_modified_block_currency.py` 128 → 139) and THREE assertions in three existing tests are FLIPPED rather than loosened — the three tests that BUILD these grounds' shapes and asserted the silence this packet retires, one of them the REAL fixture instance of it. The delta ALSO ADDS TWO SCENARIOS to the MODIFIED block, at its end, one for each ground; no promoted scenario moves, is retitled or loses a bullet.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves and no release tag is owed. Under `release-realization` a non-empty code surface archives on merged-plus-green realization evidence rather than on landing, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green `pytest-suite` and doc-health runs.
Status: draft
Proposed: 2026-09-09
Origin: openxFactory issue **#729** (found by the adversarial review of PR **#685**, which filed **#692**, whose packet `amend-marker-reason-boundary` — PR **#719** — owed this successor at its own `tasks.md` § 5.1); THE ORIGIN IS NOT A RATIFICATION. The issue records two silences and a proposed remedy, and no word of Brett Heap's ratifies this text or its design choice. `.openspec.yaml` carries drafting provenance only — no `approved_by`, no `approved_on` — and every document in the packet carries `Status: draft`. The decision most worth a veto is `design.md` **D1**: option A (the NARROW unit-match predicate) against option B (the BROAD position predicate the issue's own remedy shape proposed).
---

# Proposal: amend-marker-defect-reporting

Status: draft
Proposed: 2026-09-09, in lane `openxfactory-1`.
Origin: openxFactory issue **#729**. The origin is a defect report, not an
approval: nothing here is ratified, and § Ratification records what is owed.

## Why

**A marker is a declaration, and until now a declaration that described nothing
was silent about ITSELF in two ways — so its author was pointed at a unit
instead of at their own paragraph.**

`doc-health`'s *Currency of an active change's MODIFIED requirement blocks*
gives a marker exactly ONE reporting ground, in one sentence:

> A marker naming a unit the block still carries declares nothing and SHALL
> itself be reported, because a declaration that does not describe the block is
> a declaration no reader can rely on.

Two other ways of declaring nothing fall outside it.

**THE FIRST IS AS OLD AS THE FAMILY.** A name matching no unit of the
requirement suppresses nothing and is reported as nothing.
`suppression`'s own docstring states the consequence and the reason:

> That third case is fail-closed and is deliberately NOT a finding: the delta
> mandates exactly one reporting case for a marker, and adding a second is an
> obligation this feature has no standing to invent. Recorded as a plausible
> later ruling.

**THE SECOND IS YOUNGER THAN THE REASON BOUNDARY.**
`amend-marker-reason-boundary` (PR **#719**) stopped reading a code span inside
a marker's reason as a name — correctly, that being what a reason is — and named
the new failure mode it created in the same breath: an author who separates two
NAMES with ` — `, which `document-lifecycle`'s *"naming each deleted unit as a
CommonMark code span"* reads as legitimate, now declares only the first. The
second span suppresses nothing, so the unit it meant to declare is REPORTED,
which is the conservative direction and is why that packet shipped. But the
MARKER is not reported, so its author reads this family's fixed action string —
*"name a unit the block does not restate, or drop the declaration"* — telling
them to write a declaration they have already written.

**AND THE SPAN WAS NOT EVEN KEPT.** `parse_marker`'s unit-naming branch derives
`names = [normalize(c) for _s, e, c in spans if e <= cut]` and drops the rest:
the spans after the boundary are not carried on the `Marker` at all, not even as
a discarded field. So the second silence was not merely unreported — it was not
mechanically detectable. One field is the enabling half of this packet.

## Why this is NOT a plain fix

**Because the requirement mandates exactly ONE reporting ground, and both new
findings are additions to it rather than implementations of it.** The clause a
reader reaches for — *"a declaration that does not describe the block"* — is the
THEN's RATIONALE in canon's scenario, not a second WHEN:

> #### Scenario: A marker names a unit the block still carries
> - **WHEN** a marker names a scenario title or body unit that the block does in fact restate

Neither new case satisfies that WHEN. Case one's own author recorded a report
here as *"a plausible later ruling"* the feature had no standing to take; case
two is prescribed the OPPOSITE treatment by canon, which does not merely omit a
report but says what happens instead:

> - **AND** the units the span would have named MUST therefore remain subject to
>   the carriage arms, an author who only mentioned a unit having declared
>   nothing about it

That remedy is KEPT here, word for word. What this packet adds is a report about
the MARKER beside it. Adding a second obligation over the same facts is an
amendment of the requirement, ratified by Brett, with the realization landing in
the same pull request under `release-realization`'s merged-plus-green rule —
the shape `amend-published-tip-unreadable-scenario` (#685),
`amend-unreadable-read-sibling-scenarios` (#688) and
`amend-marker-reason-boundary` (#719) all took over this same capability.

**AND THE PACKET THAT OWED THIS SUCCESSOR ALREADY RULED ITS SHAPE.**
`openspec/changes/archive/2026-09-06-amend-marker-reason-boundary/tasks.md`
§ 5.1, ratified 2026-09-06, carried verbatim: *"it is an OWED SUCCESSOR with its
own scenarios to write, and it is not this packet."* Issue #729's own body agrees,
naming the code surface as `scripts/doc_health/modified_block_currency.py`
**"and its scenarios in `specs/doc-health/spec.md`"**.

**The sentence is promoted in ONE place, and that was checked in both
directions.** `document-lifecycle`'s marker grammar says how a deleted unit is
NAMED and says nothing about when a marker is reported, so it needs no amendment
and none is made. `doc-health` is where the reporting rule lives, and this
packet touches only it.

## What Changes

**ONE body sentence, inside ONE `## MODIFIED` requirement, plus two scenarios at
the end of the block.**

- **RETIRED:** *"A marker naming a unit the block still carries declares nothing
  and SHALL itself be reported, because a declaration that does not describe the
  block is a declaration no reader can rely on."*
- **REPLACING IT:** a marker that declares nothing SHALL itself be reported on
  any of THREE grounds, each one finding at the `info` band the marker-defect
  class already carries — it names a unit the block still carries; or a code
  span standing INSIDE its reason matches EXACTLY a unit of the promoted
  requirement that the block does not carry and that no marker declares removed;
  or it names something matching no unit of the promoted requirement and no unit
  of the block — with the second ground read NARROWLY, on the exact match and
  never on the span's position alone, and never withdrawing the carriage arms
  from the unit the span would have named.

The retired unit is declared by the reserved marker
`**Removed from canon by amend-marker-defect-reporting (2026-09-09):**`, naming
it verbatim as a code span; the unit contains no backtick, so a single-backtick
fence names it whole and canon's longer-fence rule has nothing to do here.

**TWO SCENARIOS ARE ADDED AT THE END OF THE BLOCK**, *A marker's reason quotes a
unit the block does not carry* and *A marker names something no unit matches*.
Without them the two new grounds would promote with nothing exercising them and
would be pinned only by this packet's tests — running code standing in for canon,
which is the shape § *Why this is NOT a plain fix* refuses.

**WHAT IS KEPT AND IS STILL TRUE.** The reason-quotes scenario is carried
BYTE-IDENTICAL, its third `AND` included: the unit a reason only quoted stays
subject to the carriage arms. The two obligations do not compete — the arm
reports the UNIT, the new ground reports the MARKER, and an author needs both
rows to see what happened. The `Merged into` form, the pairing form, the
derivation, the suppression rules, the scenario-title cascade and its
`adds_new_title` gate, the disposition rule and every severity are untouched.

## The corpus measurement

Every unit-naming marker in `openspec/specs/*/spec.md` and every active
`openspec/changes/*/specs/*/spec.md`, read through `derive_units` so that fenced
example markers are never offered — the walk `_corpus_markers()` runs — taken on
2026-09-09 on `main` @ `6df21737`, the corpus AS IT STOOD BEFORE THIS PACKET:

| measure | 2026-09-06 (`amend-marker-reason-boundary`) | 2026-09-09 (this packet) |
| --- | --- | --- |
| unit-naming markers in the corpus | 7 | **16** |
| carrying a code span INSIDE the reason | 2 | **8** |
| reason-quoted spans that ARE a derived unit of their document | 0 | **0** |
| unit-naming markers the FAMILY actually reads (active MODIFIED blocks) | — | **2** |
| findings the NARROW ground two would raise today | — | **0** |
| findings ground three would raise today | — | **0** |

All eight reason-quoting markers are PROMOTED specifications' own markers, and
every span they quote is reason-prose: `WHEN`, `AND`, `or`, `openspec/specs`,
`openxFactory`, `OpenXPKI-Install`, `opensoft/xFactory-Hermes-Install`. **The
shipping path** — the active MODIFIED blocks this family reads — carries exactly
TWO unit-naming markers, `add-chain-attestation` and
`add-composed-view-authoring`, both of the `Merged into` form, each naming one
unit that matches its resolved basis, neither quoting a code span in a reason.

**THAT MEASUREMENT IS WHAT MAKES GROUND TWO NARROW** (`design.md` D1). Half of
this corpus's unit-naming markers quote a code span inside their reason, and
canon blesses precisely that shape — so a ground written on the span's POSITION
would report eight legitimate promoted markers the moment a MODIFIED block
restated one of their requirements, and would grow with the corpus (2 of 7 in
September's first week, 8 of 16 by the second). Written on an EXACT MATCH against
an uncarried unit, it is silent on all eight, because ZERO of the spans they
quote is a derived unit at all.

## Impact

**Behaviour: none observable on this corpus today, by measurement.**
`python3 scripts/doc-health.py --single-repo . --family modified-block-currency`
returns output IDENTICAL to `origin/main`'s, line for line, apart from the
repository identity label — this packet's own block included. Both new grounds
have a population of zero at landing, which is what makes them normative for the
next marker written rather than a sweep of the present one.

**Tests:** `tests/doc-health/test_modified_block_currency.py` **128 → 139**, and
**THREE existing assertions are FLIPPED**, named here rather than left to be
found in the diff. Two are in that file —
`test_names_separated_by_the_separator_fail_in_the_CONSERVATIVE_direction` and
`test_a_reason_quoting_a_REAL_canon_unit_suppresses_it_under_the_retired_rule`,
which each BUILD ground two's shape and each asserted `defective == []`. The
third is `test_the_inner_backtick_does_not_truncate_the_named_unit` in
`test_modified_block_currency_fixtures.py`, and it is **THE REAL INSTANCE**: a
fixture marker whose single-backtick fence truncates its name to a fragment
matching no unit, whose author saw only a ledger row for a clause they thought
they had declared and nothing pointing at the fence that caused it. Its
docstring said in as many words that such a marker "is NOT reported as a marker
defect", which was true of the one-ground sentence and is what ground three
retires. All three now assert the marker IS reported, with the reason written
where the assertion stands. Nothing else in any of the three moves, and no other
existing test is edited. The full `tests/doc-health` suite goes 1635 → 1646.

**Doc-health:** the `modified-block-currency` family reads this new active delta.
It drops one canon unit, that unit is named by the reserved marker, every other
body unit, all sixteen promoted scenario titles and all their bullets are
carried, and the two scenario titles the block ADDS are titles the arms never
report — so the block raises ZERO findings from its own family, which is
MEASURED in the pull request rather than expected.

**AND THIS BLOCK IS ITS OWN SELF-REFERENCE TEST, IN A NEW WAY** (`design.md`
D4). Ground three reports a name matching no unit of the requirement or of the
block — and `amend-marker-reason-boundary`'s promoted `Removed from canon` marker
names a sentence canon no longer carries. Restating that marker in this block
would therefore make this block report ITSELF under its own new ground. It is
deliberately NOT restated, on this requirement's own rule that *"a marker is NOT
a carriage unit, in either direction"*, and the block's `AMENDED BY` note says so
in terms. That is a general consequence of ground three, disclosed rather than
discovered later: copying a predecessor's declaration forward into a later block
is now reportable, and canon already told authors not to.

**Severity and resolution: NOTHING MOVES, AND WHAT IS ALREADY TRUE IS SAID
PLAINLY.** The new findings carry the marker-defect class's existing `info` band
(`_LEDGER_SEVERITY`) and its existing action, so no `--fail-on` configuration
reds on them. They also inherit — as every class of this family does since the
flip of 2026-08-31 (issue #357) — the family's `contested` row in
`families.FAMILY_RESOLUTION`, which has no per-class grain. **This packet claims
no exemption from that and creates no new mechanism**: a marker-defect finding
that stops being reported without a citation already owes one under
`report.uncited_resolutions`, and with a population of zero at landing there is
nothing that can disappear. Canon's own *advisory at launch* paragraph still
describes the PRE-flip state and is carried here byte-faithfully because this
packet replaces exactly one sentence; correcting it is its own amendment with its
own ruling (`tasks.md` § 5.3).

**OpenSpec 1.12:** the block omits no scenario and retitles none — it replaces
one body sentence and appends two scenarios — so it adds no undispositioned
failure to `scripts/validate-openspec-cli-pin.py --all --no-cache`, which is run
in the pull request rather than assumed.

**No file is added under `openspec/specs/`**, so no codexFactory floor advance is
owed.

## Sequencing

`sequenced_after` is **ELECTIVE HERE AND IS NOT DECLARED.** The writers of this
requirement — `add-modified-block-currency-check`,
`add-unclassified-finding-class`, `govern-sibling-added-modified-deltas` and
`amend-marker-reason-boundary` — are all ARCHIVED, and their text is already in
the canon this block restates. **No ACTIVE change carries a `## MODIFIED` block
for it**, grepped over `openspec/changes/` on the tree this packet is authored
on: the two active changes that name the requirement at all
(`prepare-openspec-1-12-readiness/tasks.md`,
`disposition-codexfactory-declared-renames/design.md`) mention it in prose and
carry no delta over it. The ledger row is seeded with `--moved-by` this pull
request and classes on archived partners only, so no partner flips and no
MOVEMENT LOG entry is owed.

## Ratification

**NOT RATIFIED. NO WORD HAS BEEN GIVEN OVER THIS TEXT, and none is implied by
anything in this packet.** Brett Heap's *"author the 729 packet"*
(2026-09-09T12:32:46Z) instructs a lane to author it; his *"merge 842 and 846
when green, then ratify the 729 packet"* (2026-09-09T13:13:41Z) states the
INTENDED sequence and is recorded on the issue — it names no wording and takes no
design decision, and the ratification it foresees happens on a later word, when
this pull request is frozen green. `tasks.md` § 1 is UNTICKED and names
ratification as owed, `.openspec.yaml` carries drafting provenance with no
approval pair, and every document here carries `Status: draft`.

**THE VETO POINT IS `design.md` D1 — option A against option B**, and it is put
rather than assumed: A reports only where a reason-quoted span matches an
uncarried promoted unit EXACTLY; B reports any code span inside a reason, which
is the remedy shape issue #729's own body proposes and which fires on canon's
blessed form. A is designed and encoded; B is written out beside it with its cost
measured. A veto of A is a veto of ground two, and ground three stands
independently of it.

## What this proposal does NOT claim

- It does not claim either silence has ever hidden a real deletion. Neither has,
  and the measurement that says so is in this document and in a test.
- It does not change what a marker SUPPRESSES. Both new grounds report and
  suppress nothing; the three-way resolution is untouched.
- It does not change any parse. `names` and `reason` are exactly what the
  amended boundary already derived; one field carries what was thrown away.
- It does not touch the pairing form, whose whole tail is a reason by
  construction and which names no units, so no span in it is a would-be
  declaration.
- It does not amend `document-lifecycle`, whose marker grammar carries no
  reporting rule.
- **It does not report a name matching a unit the BLOCK adds and canon does
  not.** That is a fourth ground nobody has ruled, and it is left silent
  deliberately (`design.md` D3), pinned by a test so the silence is a decision
  rather than a gap.
- **It does not edit the promoted markers it counts**, nor the archived deltas
  that carry them. They are records of ratified removals.
