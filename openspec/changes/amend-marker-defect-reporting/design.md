# Design: amend-marker-defect-reporting

Status: draft
Date: 2026-09-09
Kind: design

## 0. The brief

openxFactory issue **#729**, filed for the queue on 2026-09-06 out of
`amend-marker-reason-boundary`'s own owed-successor list (§ 5.1), which the
adversarial review of PR **#685** set in motion:

> Remedy shape: a `marker-defect` finding (the ledger's `info` band, alongside
> the existing "names a unit the block still carries" defect in
> `_arm_marker_defects`) for two new cases — "this marker names something no
> unit of the requirement matches" … and "this marker carries a code span
> INSIDE its reason" … which requires `_reason_boundary`/`parse_marker` to
> additionally report the spans found after the boundary.

The issue offers the second case as a POSITION predicate. This document takes a
narrower one, writes the issue's own shape out beside it with its measured cost,
and names the choice as the packet's veto point.

## D0 — the measurement, taken before the design

Every unit-naming marker in `openspec/specs/*/spec.md` and every active
`openspec/changes/*/specs/*/spec.md`, read through `derive_units` (so this
requirement's own written-out examples, which are complete markers, are never
offered — exactly as they are never offered to a run). Taken 2026-09-09 on
`main` @ `6df21737`, the corpus BEFORE this packet:

| measure | 2026-09-06 | 2026-09-09 |
| --- | --- | --- |
| unit-naming markers | 7 | **16** |
| carrying a code span INSIDE the reason | 2 | **8** |
| reason-quoted spans that ARE a derived unit of their document | 0 | **0** |
| unit-naming markers the family READS (active blocks) | — | **2** |
| findings the narrow ground two raises today | — | **0** |
| findings ground three raises today | — | **0** |

The eight, every one of them a PROMOTED specification's own marker:

| promoted spec | marker | names | spans its reason quotes |
| --- | --- | --- | --- |
| `canonical-contract-migration` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | 4 |
| `doc-health` | `amend-published-tip-unreadable-scenario` (2026-09-05) | 1 | 2 (`WHEN`, `AND`) |
| `doc-health` | `amend-unreadable-read-sibling-scenarios` (2026-09-05) | 1 | 2 (`WHEN`, `AND`) |
| `repo-boundary-governance` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | 7 |
| `repo-boundary-governance` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | 2 |
| `repo-boundary-governance` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | 6 |
| `shared-contract-ownership` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | 7 |
| `shared-contract-ownership` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | 4 |

**AND THE THIRD ROW IS THE ONE THE DESIGN TURNS ON: of the 34 spans those eight
reasons quote, ZERO is a derived unit of the document that carries the marker.**
They are `WHEN`, `AND`, `or`, `and`, `THEN`, `openspec/specs`, `openxFactory`,
`OpenXPKI-Install`, `opensoft/xFactory-Hermes-Install`, `FarHeap/Hermes-Install`
— prose a reason quotes while explaining itself. That is what separates the
defect from the normal form, and it is a property of the SPAN's identity rather
than of its position.

**THE SHIPPING PATH IS NARROWER STILL.** The family reads MARKERS only inside
active `## MODIFIED Requirements` blocks. Of the active blocks on this tree
exactly TWO carry a unit-naming marker — `add-chain-attestation` and
`add-composed-view-authoring`, both `Merged into`, one name each, matching their
resolved basis, neither quoting a code span in a reason. So both new grounds have
a population of ZERO today, measured rather than assumed, and the silence they
retire has never yet cost anybody a row.

## D1 — THE VETO POINT: option A (the exact match) against option B (the position)

**A — RECOMMENDED, AND WHAT THE DELTA ENCODES.** A code span standing after the
reason boundary is reported ONLY where it, normalized, matches EXACTLY a unit of
the promoted requirement that the block does not carry and that no marker in the
block declares removed. Such a span is a WOULD-BE DECLARATION: its author had a
unit in mind, the boundary read it as prose, and nothing in the block declares
it.

- **It is silent on all eight promoted markers**, today and on the same shape
  tomorrow, because none of the spans they quote is a unit (D0). Silence there is
  not a tolerance; it is the correct answer, because those reasons are correct.
- **It fires on exactly the shape `amend-marker-reason-boundary` created** — an
  author separating two NAMES with the separator — which is the case that
  packet's § 5.1 owed a successor for, and which two of this file's existing
  tests already BUILD.
- **It costs one field and no parse.** `Marker.quoted` carries what
  `parse_marker` already computed and discarded; `names` and `reason` are
  unchanged, so no marker in the estate parses differently.
- **Its failure direction is silence, not noise.** Where a span is a unit under a
  different spelling, or a unit of a sibling's pending addition rather than of
  canon, ground two says nothing and the carriage arm still reports the unit —
  the same conservative direction #719 shipped in.

**B — REJECTED FOR MEASURED COST, and it is the issue's own remedy shape rather
than a straw one.** Report any code span standing inside a marker's reason:

1. **It fires on canon's blessed form.** Canon says in as many words that such a
   span *"is prose the reason quotes rather than a unit the marker names"*. B
   reports the author for writing what the requirement told them to write.
2. **EIGHT of the sixteen markers in this corpus are reportable under it**, every
   one of them promoted and correct, the moment any MODIFIED block restates one
   of their requirements — and the share is GROWING: 2 of 7 on 2026-09-06, 8 of
   16 on 2026-09-09.
3. **It cannot be narrowed by wording later without a second amendment.** A
   ratified ground on the span's position is a ratified obligation; retiring it
   costs another `## MODIFIED` block over the same sentence, which is this
   family's third amendment in four days.
4. **It does not even distinguish the defect it is aimed at.** The two-names
   author and the quoting author write the SAME BYTES in the same positions; only
   the span's identity tells them apart. B reports both and calls it a defect
   report.

**The veto is between A and B. A veto of A is a veto of ground TWO ONLY** —
ground three (a name matching no unit of the requirement or of the block) rests
on no predicate choice, is the silence `add-modified-block-currency-check`
recorded as a plausible later ruling, and stands whichever way D1 goes. If B is
ruled, the delta's second ground is re-authored on the position predicate and
the eight-marker cost is ratified with it; nothing else in the packet moves.

## D2 — ONE TEMPLATE FOR THREE GROUNDS, not three templates

The three grounds share a band (`info`), a class (`marker-defects`) and an ACTION
(*"name a unit the block does not restate, or drop the declaration"*). This
module already ruled what that means, in `TEMPLATE_PAIRING`'s own comment, on
Brett's amendment of 2026-08-28 (*"Amend: shape = arm template, all
interpolations masked"*): one SHAPE is one TEMPLATE is one map entry, and the
count of `_ARM_TEMPLATES` is a count of REMEDIES. Four pairing states share one
template for exactly this reason.

So `TEMPLATE_MARKERS` gains one interpolated `{why}` field and keeps its fixed
opening and its fixed trailing prose. Three consequences, all of them checked
rather than argued:

- **The existing `CLASS_MARKERS` probe places every new finding.** It reads
  `_BLOCK_HEAD + r"carries a '\w+' marker by "`, which is the opening the
  template keeps — so the seventh class (`unplaced-finding drift`) stays silent
  and no map entry is owed.
- **`_ARM_TEMPLATES` stays at EIGHT**, so the two standing count assertions and
  the drift grain hold untouched.
- **Ground one's rendered text is BYTE-IDENTICAL** to the one the class shipped
  with, pinned by a test that types the expected string out rather than reading
  it off the template.

The trailing prose stays FIXED rather than being folded into `{why}` because
`_ArmTemplate`'s `\Z` bites only on a template that ends in fixed prose, and this
is one of the two that do. And neither new WHY clause may carry another
template's fixed prose in order, or one rule text could match two templates and
red the partition the shape mask rests on:
`test_each_new_marker_defect_ground_matches_exactly_one_arm_template` holds that
property instead of trusting the wording.

## D3 — WHAT GROUND THREE DOES NOT REPORT, and why the residue is a decision

A name matching no CANON unit but matching a unit the BLOCK states is text the
block ADDS. Ground three reports a name matching NEITHER side, so this case is
silent.

It is a real case with a real reading available — a marker declaring a unit of
the block's own addition removed declares something odd — but which reading is
right depends on a rule nobody has written: whether a block may declare its own
additions, and against what. Inventing a fourth ground here would repeat exactly
the fault this packet exists to correct, on the same afternoon. It is pinned by
`test_a_name_matching_a_unit_the_BLOCK_adds_stays_SILENT` so the silence is a
decision a later reader can overturn, not a gap they have to rediscover.

**AND A MARKER THAT NAMES NOTHING AT ALL IS SILENT TOO, WHICH IS WHY THE
SENTENCE CLAIMS THE THREE GROUNDS RATHER THAN THE CONVERSE.** A
`Removed from canon` marker whose tail carries no code span parses to `names =
[]` and `quoted = []`, so `suppression`'s per-name loop never runs, `restated`
stays false, `unmatched` stays empty and the second pass has nothing to resolve
— it reaches NONE of the three grounds. It is the FOURTH case of a marker that
declares nothing about the block, and it is unruled: what such a paragraph even
is (a marker form with no declaration, or prose that merely looks like one) is a
grammar question this packet does not open. So the delta's sentence is written to
say what the three grounds report rather than to say that every marker declaring
nothing is reported, and the case is recorded as residue at `tasks.md` § 5.7.

The same discipline applies to the PAIRING form. Its whole tail is a reason by
construction and it names no units, so no span in it is a would-be declaration;
`Marker.quoted` is empty for it and ground two cannot reach it.

## D4 — THE SELF-REFERENCE HAZARD, WHICH GROUND THREE CREATES

`amend-marker-reason-boundary`'s promoted `Removed from canon` marker names, as a
code span, the sentence THAT change retired. Canon no longer carries that
sentence — the removal is what the marker declares — so the name matches no unit
of the requirement.

**Restating that marker in this block would therefore make this block report
ITSELF under its own new ground three.** It is deliberately not restated, and the
authority for not restating it is this requirement's own promoted sentence: *"A
marker is NOT a carriage unit, in either direction … if it were a unit every
later block would have to restate every marker any predecessor ever wrote,
forever."* The block's `AMENDED BY` note says so in terms, so a reader does not
read the omission as an oversight.

That generalizes, and the generalization is disclosed rather than left to be
found: **after this packet, copying a predecessor's promoted `Removed from canon`
marker forward into a later MODIFIED block is a reportable defect.** Canon
already told authors not to do it; the report is new. Measured on this tree: no
active block does it, so the population of that consequence is also zero today.

This packet's OWN marker is written to survive its own rules — one name matching
a canon unit the block does not carry, and a reason CARRYING NO CODE SPAN AT ALL,
so ground two has nothing to resolve and the marker parses to exactly one name.
Verified in the pull request rather than asserted here.

## D5 — GROUND TWO RUNS IN A SECOND PASS, and it has to

Its predicate asks whether the quoted unit is one NO marker accounts for. A
sibling marker that properly declares the unit removed makes the quotation
harmless — reporting it would send an author to fix a marker that is already
right — so the question cannot be answered until every name in the block has been
resolved. Hence: pass one resolves names (grounds one and three, in that order,
per marker); pass two resolves the quoted spans against `suppressed` and the
block. The order is fixed so that a marker defective twice reports the same two
rows every run, and `test_a_marker_defective_on_two_grounds_reports_TWO_findings`
holds it.

**A SPAN THE MARKER ALSO NAMES IS SKIPPED.** Its author declared it; quoting it
again in the reason declares nothing new and hides nothing. That single line is
also what keeps the retired-rule half of
`test_a_reason_quoting_a_REAL_canon_unit_suppresses_it_under_the_retired_rule`
true, which is the comparison that made the #719 defect legible in the first
place.

## D6 — ONE FINDING PER GROUND, per marker

A ranked plan is a list of REMEDIES, and the grounds are different edits: move a
span in front of the separator; stop naming a unit the block restates; correct a
name that matches nothing. A marker defective two ways gets two rows, which is
proportional in the same way `suppression`'s per-name voiding (ruled 2026-08-27)
is proportional. WITHIN a ground the record is per MARKER: ground one names all
of the marker's names, exactly as it always has, and ground three names only the
names that matched nothing, because those are the names an author edits.

## D7 — the band, and the one thing that is TRUE rather than convenient

The new findings carry `_LEDGER_SEVERITY` (`info`) and the marker-defect class's
existing action, so no `--fail-on` configuration reds on them and the class needs
no new registration.

**AND THEY INHERIT THE FAMILY'S `contested` ROW, WHICH IS SAID PLAINLY BECAUSE IT
IS ALREADY TRUE.** `families.FAMILY_RESOLUTION` has carried
`"modified-block-currency": CONTESTED` since the flip of 2026-08-31 (issue
#357), that table has no per-class grain, and `runner.main` applies it by
`Finding.family` alone. So a marker-defect finding that stops being reported
without a citation already owes one under `report.uncited_resolutions` — for the
ground that shipped as much as for the two added here. This packet claims no
exemption and creates no new mechanism, and with a population of zero at landing
there is nothing that can vanish between two reports. Canon's *advisory at
launch* paragraph still describes the pre-flip state (`warning` severities,
absence from the resolution table); it is a promoted unit, it is carried here
byte-faithfully because this packet replaces exactly ONE sentence, and correcting
it is its own amendment with its own ruling (`tasks.md` § 5.3).

## D8 — what is NOT taken here

- **The promoted markers are not edited**, nor the archived deltas that carry
  them. They are records of ratified removals, and every one of them is correct
  under the narrow ground.
- **`document-lifecycle` is not amended.** Its marker grammar says how a unit is
  named and carries no reporting rule, checked on this tree.
- **No severity moves and no class is added.** Three grounds, one class, one
  action, one template.
- **The action string is not re-worded.** It already names the remedy for all
  three grounds — *"name a unit the block does not restate, or drop the
  declaration"* — and a per-ground action would break the class's own pin
  (`test_every_finding_carries_its_class_s_band_and_action`) for no reader's
  benefit.
