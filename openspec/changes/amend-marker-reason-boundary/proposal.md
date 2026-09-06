---
code_surface: openxFactory — `parse_marker` in `scripts/doc_health/modified_block_currency.py` and the tests that pin it in `tests/doc-health/test_modified_block_currency.py`. ONE split is moved: the tail after a unit-naming marker's closing colon is divided at the FIRST ` — ` standing OUTSIDE every code span rather than after the LAST code span, and one new module-level helper (`_reason_boundary`) implements the test. The `Merged into` destination is matched in the PREFIX and is untouched; the third reserved form (`Modified over`) returns before this split and still takes its whole tail, its branch comment corrected where it described the retired rule. NOTHING ELSE MOVES: no severity, no threshold, no arm, no finding class, no path, no disposition rule, no workflow, no contract member and no other family. Seven tests are ADDED beside the existing ones (`tests/doc-health/test_modified_block_currency.py` 121 → 128) and no existing test is edited, because the amended rule agrees with the retired one on every marker whose reason quotes nothing. The delta ALSO ADDS TWO SCENARIOS to the MODIFIED block, at its end, pinning the amended sentence in canon rather than in code alone; no promoted scenario moves, is retitled or loses a bullet.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves and no release tag is owed. Under `release-realization` a non-empty code surface archives on merged-plus-green realization evidence rather than on landing; the tasks are individually executable, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green `pytest-suite` and doc-health runs.
Status: draft
Proposed: 2026-09-06
Origin: openxFactory issue **#692**, filed out of the adversarial review of PR **#685**. THE ORIGIN IS NOT A RATIFICATION: the issue records a defect and a proposed remedy, and no word of Brett Heap's ratifies this text or its design choice. `.openspec.yaml` carries drafting provenance only — no `approved_by`, no `approved_on` — and every document in the packet carries `Status: draft` to match. The decision most worth a veto is `design.md` **D1**: option A (the boundary) against option B (a fenced list of removed units).
---

# Proposal: amend-marker-reason-boundary

Status: draft
Proposed: 2026-09-06, in lane `openxfactory-1`.
Origin: openxFactory issue **#692**. The origin is a defect report, not an
approval: nothing here is ratified, and § Ratification records what is owed.

## Why

**A marker's reason is prose, prose in this corpus quotes, and the promoted
sentence turns every quotation into a declaration of removal.**

`doc-health`'s *Currency of an active change's MODIFIED requirement blocks*
defines the reserved deletion marker and, in one sentence, how it is parsed:

> The parser SHALL extract the code spans following the colon, in order, per
> CommonMark; **the reason is everything after the last code span's following
> ` — `**.

Measuring the reason from BEHIND means the names are "every code span in the
tail" — including every span the reason itself quotes. The live instance is the
marker PR **#685** promoted, at `openspec/specs/doc-health/spec.md:2716`:

```
**Removed from canon by amend-published-tip-unreadable-scenario (2026-09-05):**
``**WHEN** the blob read for the manifest … has not fetched that commit`` — the
clause after the dash asserts which cause is commonest … the unit is REPLACED
rather than deleted, by the `WHEN` that names both facts and the `AND` that
requires the family to establish which holds before it speaks.
```

Its author declared ONE unit. The promoted parser derives **three** — the
intended `WHEN` bullet, plus `WHEN` and `AND`, the two words the reason quotes —
and derives **no reason at all**, because nothing follows the last span with a
separator in front of it. Its sibling marker at `:2755`, promoted by **#688**, is
the same shape and reads the same way.

**IT IS INERT TODAY AND THAT IS AN ACCIDENT OF THE CORPUS.** Measured on this
tree on 2026-09-06, across every promoted specification and every active delta
OTHER THAN THIS ONE (this packet's own delta carries an eighth marker, handled
under *The self-reference hazard*): of **17,566** derived units, **none** is
literally `WHEN` or `AND` — nor is any of the units this packet's own text adds
— so
`suppression` finds no match for either name, suppresses nothing and reports
nothing (`--family modified-block-currency` reports identically before and
after). What is not inert is the next marker. The names a marker derives are
exactly what it suppresses, so an author whose reason quotes a real unit — a
scenario title, a clause this corpus actually carries — declares that unit
removed by mentioning it, and the carriage arms fall silent about a unit nobody
declared gone.

## Why this is NOT a plain fix

**Because the checker conforms to the sentence exactly, and the hazard is in the
sentence.** `parse_marker` does what canon tells it: take the spans, then take
the reason from after the last one. Changing the parser alone would put the
running code out of agreement with a promoted SHALL — the checker out-running
canon, which is the inverse of the defect **#678** and **#688** were written to
avoid and the shape this capability keeps refusing. So the remedy is a
`## MODIFIED` requirement that retires the sentence and states the boundary,
ratified by Brett, with the realization landing in the same pull request under
`release-realization`'s merged-plus-green rule.

**The sentence is promoted in ONE place, and that was checked.**
`document-lifecycle`'s own marker grammar (*"naming each deleted unit as a
CommonMark code span"*) says nothing about where the reason begins, so it needs
no amendment and none is made. `doc-health` is where the reading lives, and this
packet touches only it.

**WHAT THAT SENTENCE DOES NOT SAY, SAID HERE RATHER THAN LEFT TO BE FOUND.**
`document-lifecycle` requires the declaration to name *"each deleted unit as a
CommonMark code span"*, which under the retired rule was true of EVERY span in
the tail. Under the amended rule a span standing AFTER the boundary names
nothing, so a `document-lifecycle`-conforming author who separates two names
with ` — ` now declares only the first. **That is a NEW failure mode this
amendment creates, and it is deliberate**: it is the conservative direction —
the second unit suppresses nothing and is therefore REPORTED, never silently
dropped (measured: no marker in this corpus is written that way, and the
amended names are always a subset of the retired ones). It is nevertheless a
SILENT correction today, because `suppression`'s third resolution says nothing
about a name that matches no unit, so the author sees only this family's fixed
action string telling them to add a marker they already wrote. Reporting it is
scoped into the owed successor at `tasks.md` § 5.1, named there as this
amendment's own consequence rather than only as the pre-existing silence.

## What Changes

**ONE body sentence, inside ONE `## MODIFIED` requirement.**

The delta restates *Currency of an active change's MODIFIED requirement blocks*
in full — all 50 body units, all 14 scenario titles and all 40 scenario bullets,
byte-faithful, INCLUDING the fenced block that writes the two marker forms out —
and changes exactly this in the promoted text:

- **RETIRED:** *"The parser SHALL extract the code spans following the colon, in
  order, per CommonMark; the reason is everything after the last code span's
  following ` — `."*
- **REPLACING IT:** *"The parser SHALL extract the code spans following the
  colon, in order, per CommonMark, and THE REASON SHALL BEGIN AT THE FIRST
  ` — ` SEPARATOR STANDING OUTSIDE EVERY CODE SPAN: the units named are the
  spans that close before that separator, the reason is everything after it, and
  a code span that falls inside the reason is prose the reason quotes rather
  than a unit the marker names. Where no such separator stands, every span names
  a unit and the marker carries no reason, which is what the written-out
  `Merged into` example below is. The boundary is read the same way in both
  forms, the `Merged into` destination being matched in the prefix and the tail
  after the closing colon being parsed identically."*

The retired unit is declared by the reserved marker
`**Removed from canon by amend-marker-reason-boundary (2026-09-06):**`, naming it
verbatim as a code span fenced with a doubled backtick run — the unit cites
` — ` and so contains backticks, which is the corpus's own longer-fence rule
applied to a sentence about that rule.

**WHAT IS KEPT AND IS STILL TRUE.** The next promoted sentence —
*"Semicolons and dashes inside a unit or inside a reason are therefore
irrelevant, because extraction is by code span and never by splitting on
punctuation"* — is carried byte-identical and reads correctly under the new
boundary: a dash INSIDE a unit is inside a code span and is skipped, and a dash
INSIDE the reason falls after the boundary and decides nothing. Extraction of
units is still by code span; what the amendment adds is where the extraction
STOPS.

**The `Merged into` form is examined and amended CONSISTENTLY rather than
separately.** Both unit-naming forms share one tail parse — the destination is
matched in the prefix regex, never in the tail — so the sentence governed both
before and governs both after, and the new text says so in terms. The third
reserved form (`Modified over`) names no units, returns before this split, and
takes its whole tail as its reason; it is untouched, and the branch comment that
described the retired rule is corrected in the realization.

## The corpus measurement

Every unit-naming marker in `openspec/specs/*/spec.md` and every active
`openspec/changes/*/specs/*/spec.md` AS THE CORPUS STOOD BEFORE THIS PACKET,
parsed under both rules. The packet's own delta adds an EIGHTH marker, which is
the one *The self-reference hazard* below is about and which is excluded here so
that the figures re-derive against the tree the design was taken on:

| marker | document | names BEFORE | names AFTER | reason BEFORE → AFTER |
|---|---|---|---|---|
| `govern-sibling-added-modified-deltas` (2026-08-31) | `openspec/specs/doc-health/spec.md` | 2 | 2 | unchanged |
| `amend-published-tip-unreadable-scenario` (2026-09-05) | `openspec/specs/doc-health/spec.md` | **3** | **1** | `None` → the author's reason |
| `amend-unreadable-read-sibling-scenarios` (2026-09-05) | `openspec/specs/doc-health/spec.md` | **3** | **1** | `None` → the author's reason |
| `declare-generated-projection-status` (2026-08-28) | `openspec/specs/document-lifecycle/spec.md` | 1 | 1 | unchanged |
| `create-medxchart-overlay-boundary` (2026-09-03) | `openspec/specs/domain-descendant-boundary/spec.md` | 4 | 4 | unchanged |
| `add-chain-attestation` (2026-09-01) | `openspec/changes/add-chain-attestation/specs/signed-execution-chain/spec.md` | 1 | 1 | unchanged |
| `add-composed-view-authoring` (2026-08-27) | `openspec/changes/add-composed-view-authoring/specs/ideation-dashboard/spec.md` | 1 | 1 | unchanged |

**SEVEN markers; TWO change; FIVE are unaffected** — eight markers with this
packet's own, whose one name and one reason are identical under both rules by
construction. The four names the two lose
are `WHEN` and `AND` twice over, and **no marker in this corpus separates its
NAMES with ` — `** — so no marker loses a name its author meant to declare. That
is asserted as a test, not only measured:
`test_no_marker_in_this_corpus_loses_a_name_it_meant_to_declare` walks the same
population and requires every dropped name to match no derived unit of the
document that carries it.

## Impact

**Behaviour: none observable on this corpus today, by measurement.** The four
names that stop being derived match no canon unit, so `suppression` treated them
as *"names nothing; buys nothing"* before and does not see them after;
`python3 scripts/doc-health.py --single-repo . --family modified-block-currency`
reports identically at `origin/main` and on this branch. What moves is the
`reason` field of two markers, from `None` to the text their authors wrote —
read today only by `_pairing_state`, which handles the third form alone, so the
change is diagnostic on this corpus and normative for the next marker written.

**Tests:** `tests/doc-health/test_modified_block_currency.py` 121 → 128. No
existing test is edited: the amended rule agrees with the retired one on every
case the file already pinned, including the wrapped-marker case and the
two-name `REMOVED` example whose names are separated by `; `. One of the seven
runs at SUPPRESSION level rather than at parse level, because that is where the
defect's harm lands: canon carries a bullet the reason quotes, and the retired
names suppress it silently while the amended names leave it reported.

**Doc-health:** the `modified-block-currency` family reads this new active delta.
It drops one canon unit, that unit is named by the reserved marker, every other
unit and all 14 scenario titles are carried, and the two scenario titles the
block ADDS are titles the arms never report — so the block is expected to raise
**no** carriage finding, which is measured rather than expected in the pull
request. **AND THIS BLOCK IS ITS OWN SELF-REFERENCE TEST**: the
marker is parsed by the RETIRED grammar when the family runs from `main` and by
the AMENDED grammar when it runs from this branch, so its reason is written
free of code spans and both grammars derive exactly one name and the same
reason. That equality is verified in the pull request under both parsers.

**OpenSpec 1.12:** the block omits no scenario and retitles none — it replaces
one body sentence and appends two scenarios — so it adds no undispositioned
failure to `scripts/validate-openspec-cli-pin.py --all --no-cache`, which is
run in the pull request rather than assumed.

**No file is added under `openspec/specs/`**, so no codexFactory floor advance is
owed.

## Sequencing

`sequenced_after` is **ELECTIVE HERE AND IS NOT DECLARED.** The other writers of
this requirement — `add-modified-block-currency-check`,
`add-unclassified-finding-class` and `govern-sibling-added-modified-deltas` — are
all ARCHIVED and their text is already in the canon this block restates. **No
ACTIVE change carries a `## MODIFIED` block for it**, checked by grep over
`openspec/changes/` on the tree this packet is authored on: the two active
changes that name the requirement at all (`disposition-codexfactory-declared-renames`
in `design.md`, `prepare-openspec-1.12-readiness` in `tasks.md`) mention it in
prose and carry no delta over it. The ledger row is seeded with `--moved-by` this
pull request and classes on archived partners only, so no partner flips and no
MOVEMENT LOG entry is owed.

## Ratification

**NOT RATIFIED. NO WORD HAS BEEN GIVEN OVER THIS TEXT, and none is implied by
anything in this packet.** Brett Heap ruled *"do 3 and 4"* — which admits issue
**#692** to work and instructs a lane to author a remedy; it decides no wording
and takes no design decision. `tasks.md` § 1 is UNTICKED and names ratification
as owed, `.openspec.yaml` carries drafting provenance with no approval pair, and
every document here carries `Status: draft`.

**THE VETO POINT IS `design.md` D1 — option A against option B**, and it is put
rather than assumed: A moves the boundary and leaves every marker's written form
alone; B requires the removed units in a fenced list and rewrites every existing
marker plus the two prose templates that promote into canon. A is designed; B is
written out beside it with its cost. A veto of A is a veto of this delta's one
sentence, and the packet does not land on it.

## What this proposal does NOT claim

- It does not claim the defect has ever suppressed a real unit. It has not, and
  the measurement that says so is in this document and in a test.
- It does not change what the family reads, at which severity, or which
  repositories it speaks about.
- It does not touch the `Modified over` pairing form's parse, its reason rule,
  its states or its disclosure word.
- It does not amend `document-lifecycle`, whose marker grammar does not carry
  the retired sentence.
- **It does not edit the two promoted markers it names.** They are the record of
  two ratified removals and their bytes are canon; what is wrong is how they are
  READ, and the remedy is in the reading. Rewriting a marker to suit a parser
  would be the mutation this corpus refuses in `promotion-fidelity`'s own terms.
- It does not edit the archived deltas that carry the same markers under
  `openspec/changes/archive/`. An archived delta is a record of what was
  ratified.
