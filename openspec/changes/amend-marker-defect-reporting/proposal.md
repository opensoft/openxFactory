---
code_surface: openxFactory — `scripts/doc_health/modified_block_currency.py` + `tests/doc-health/test_modified_block_currency.py`. ONE READING IS ADDED and no reading moves: `Marker` gains a `quoted` field carrying the code spans that stand AFTER the reason boundary (`parse_marker` derived them and threw them away), one new module-level helper `_declares_nothing` reads them and the marker's names against the block's basis, and `_arm_marker_defects` gains a LAST parameter with a default so every existing call still reads. `names` is unchanged, `suppression` is unchanged in signature and in behaviour — nothing new is suppressed and nothing stops being suppressed — and the two new findings render through ONE new arm template that reuses `TEMPLATE_MARKERS`' opening, so `CLASS_MARKERS`' existing class pattern places them and the seventh class (`unplaced-finding drift`) stays silent. NOTHING ELSE MOVES: no severity, no threshold, no arm, no finding CLASS, no action string, no path, no disposition rule, no workflow, no contract member and no other family. Tests are ADDED beside the existing ones and one new fixture tree is added; THREE assertions in `tests/doc-health/test_modified_block_currency_reporting.py` are edited because a ninth arm template makes them literally false, and `tasks.md` § 3.6 names each one and why. The delta ALSO ADDS TWO SCENARIOS to the MODIFIED block, at its end, pinning the amended sentence in canon rather than in code alone; no promoted scenario moves, is retitled or loses a bullet.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves and no release tag is owed. Under `release-realization` a non-empty code surface archives on merged-plus-green realization evidence rather than on landing; the tasks are individually executable, so this packet realizes through its own task list in this pull request and its realization evidence is that pull request's green `pytest-suite` and doc-health runs.
Status: draft
Proposed: 2026-09-09
Origin: openxFactory issue **#729** (found by the adversarial review of PR **#685**); the origin is not a ratification. The issue records two defects and a proposed remedy, and no word of Brett Heap's ratifies this text or its design choice — his *"author the 729 packet"* (2026-09-09) instructs a lane to AUTHOR. `.openspec.yaml` carries drafting provenance only — no `approved_by`, no `approved_on` — and every document in the packet carries `Status: draft` to match. The decision most worth a veto is `design.md` **D1**: option A (the NARROW predicate) against option B (the BROAD one).
---

# Proposal: amend-marker-defect-reporting

Status: draft
Proposed: 2026-09-09, in lane `openxfactory-1`.
Origin: openxFactory issue **#729** (found by the adversarial review of PR
**#685**); the origin is not a ratification. Nothing here is ratified, and
§ Ratification records what is owed.

## Why

**A sentence stating ONE ground for reporting a marker was read — correctly, by
the running code — as stating the ONLY ground, and two defects in a declaration
therefore pass in silence.**

`doc-health`'s *Currency of an active change's MODIFIED requirement blocks*
defines the reserved deletion marker and states, in one sentence, when the
marker itself is reported:

> A marker naming a unit the block still carries declares nothing and SHALL
> itself be reported, because a declaration that does not describe the block is
> a declaration no reader can rely on.

Its scenario is gated the same way — *"WHEN a marker names a scenario title or
body unit that the block does in fact restate"*. Two shapes fall outside it:

**ONE — A NAME THAT MATCHES NOTHING AT ALL.** An author who mistypes a unit, or
names a unit that has already left canon, declares nothing: the name suppresses
nothing, and the run says nothing. `suppression`'s own docstring states the
consequence and the reason for it, verbatim:

> That third case is fail-closed and is deliberately NOT a finding: the delta
> mandates exactly one reporting case for a marker, and adding a second is an
> obligation this feature has no standing to invent. Recorded as a plausible
> later ruling.

**TWO — A CODE SPAN THE AUTHOR WROTE INSIDE THE REASON.**
`amend-marker-reason-boundary` (2026-09-06, PR **#719**) ruled that a span after
the reason separator *"is prose the reason quotes rather than a unit the marker
names"*. That ruling is right and this packet does not touch it. But
`parse_marker` accordingly DISCARDS those spans, so where a quoted span happens
to be exactly the unit the block dropped, the author's would-be declaration is
mechanically invisible: the unit is reported by the carriage arms — correctly —
with nothing to show that a declaration for it was attempted three words away.

**WHAT THAT COSTS, IN THE ONE PLACE IT IS PAID.** Both silences are silences of
DIAGNOSIS, not of enforcement: no unit is wrongly suppressed by either, which is
why the corpus has not been damaged by them (measured below: both grounds report
ZERO today). What is lost is the only thing this family exists to give an author
— a finding that names the defect they actually made. Today they are handed a
carriage row that names the unit and never the declaration, plus a fixed action
string telling them to declare a deletion with a marker they already wrote.

## Why this is NOT a plain fix

**Because the checker conforms to the sentence exactly, and the sentence states
one ground.** Reporting a second and a third would put running code ahead of a
promoted SHALL — the checker out-running canon, the inverse of the defect
**#678** and **#688** were written to avoid and the shape this capability keeps
refusing. The family's own author said so in the code rather than leaving it to
be found: adding a second reporting case is *"an obligation this feature has no
standing to invent"*.

**AND THE ORIGIN PACKET'S RATIFIED TEXT ALREADY RULED THE SHAPE.**
`openspec/changes/archive/2026-09-06-amend-marker-reason-boundary/tasks.md`
§ 5.1, ratified 2026-09-06 by Brett Heap, carries verbatim:

> The family's own author recorded that as a plausible later ruling; it is an
> OWED SUCCESSOR **with its own scenarios to write**, and it is not this packet.

Issue **#729**'s own body agrees, naming the code surface as
`scripts/doc_health/modified_block_currency.py` *"and its scenarios in
`specs/doc-health/spec.md`"*.

**AND CANON PRESCRIBES A COMPLETE TREATMENT FOR THE SECOND GROUND ALREADY, so
the report has to be added BESIDE it rather than instead of it.** The promoted
scenario *A marker's reason quotes a code span* ends:

> - **AND** the units the span would have named MUST therefore remain subject to
>   the carriage arms, an author who only mentioned a unit having declared
>   nothing about it

That bullet PRESCRIBES the carriage arms and does not forbid reporting the
marker, so it is carried WHOLE — third `AND` included — and no second marker is
owed. The amendment adds a report standing beside that carriage and takes
nothing from it, which the new scenario says in its own third bullet.

**The sentence is promoted in ONE place, and that was checked.**
`document-lifecycle`'s marker grammar (*"naming each deleted unit as a
CommonMark code span"*) says nothing about when a marker is reported, so it needs
no amendment and none is made. `doc-health` is where the reading lives, and this
packet touches only it.

## What Changes

**ONE body sentence, inside ONE `## MODIFIED` requirement.**

The delta restates *Currency of an active change's MODIFIED requirement blocks*
in full — all 122 canon units (59 body units, 16 scenario titles, 47 scenario
bullets), byte-faithful, INCLUDING the fenced block that writes the two marker
forms out, the `AMENDED BY` note **#719** promoted and the
`Removed from canon by amend-marker-reason-boundary (2026-09-06)` marker it
promoted with it — and changes exactly this in the promoted text:

- **RETIRED:** *"A marker naming a unit the block still carries declares nothing
  and SHALL itself be reported, because a declaration that does not describe the
  block is a declaration no reader can rely on."*
- **REPLACING IT:** *"A MARKER SHALL ITSELF BE REPORTED ON ANY OF THREE GROUNDS,
  because a declaration that does not describe the block is a declaration no
  reader can rely on: where it NAMES a unit the block still carries; where its
  REASON quotes a code span that … matches a unit of the promoted requirement the
  block does NOT carry … ; and where it NAMES something matching no unit of the
  promoted requirement and no unit of the block, which is a declaration about
  nothing."* — followed by four sentences that bound it: the second and third
  grounds report the marker and SUPPRESS NOTHING and replace no part of the
  three-way resolution; two shapes MUST NOT be reported (a reason quoting a unit
  the marker already named, and a reason-quoted span matching a unit the block
  DOES carry); the second and third grounds are read only against a marker THE
  BLOCK'S OWN CHANGE DECLARES; and all three carry the carriage ledger's `info`
  band and are NOT classified `contested`.

The retired unit is declared by the reserved marker
`**Removed from canon by amend-marker-defect-reporting (2026-09-09):**`, naming
it verbatim as a code span, with a reason that quotes **no code span anywhere** —
the constraint `design.md` D4 states and the one this packet's own new ground
makes mandatory for every amendment marker from here on.

**The first ground is carried, not restated.** Its clause and its rationale are
word for word what the retired sentence said; what the replacement adds is two
more grounds and the four bounding sentences.

**TWO SCENARIOS ARE ADDED at the end of the block** — *A marker's reason quotes a
unit the block does not carry* and *A marker names something no unit matches* —
because a normative rule no scenario exercises is a rule the next author
re-deriving this family has nothing to test against, and because the origin
packet's § 5.1 named "its own scenarios to write" as part of what is owed.

## The corpus measurement

Taken on this branch on **2026-09-09** at `main` `245ee85a`, over
`openspec/specs/*/spec.md` and every active `openspec/changes/*/specs/*/spec.md`,
read through `derive_units` so fenced example markers are never offered — the
same walk the family itself runs. **115 files, 18,394 derived units.**

| measure | 2026-09-06 (the origin amendment) | 2026-09-09 (this packet) |
|---|---|---|
| unit-naming markers in the corpus | 7 | **16** |
| carrying a code span INSIDE the reason | 2 | **8** |
| reason-quoted spans that ARE a derived unit of their document | 0 | **0** |
| active MODIFIED blocks | — | **31** (23 resolved, 8 pending, 0 unresolved) |
| unit-naming markers the FAMILY reads | — | **2** |
| **ground 2 findings today** | — | **0** |
| **ground 3 findings today** | — | **0** |

**The eight markers whose reason quotes a code span — every one PROMOTED, and
every quoted span reason-prose:**

| promoted spec | marker | names | spans quoted in the reason |
|---|---|---|---|
| `canonical-contract-migration` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | `would break <families> runtime adapters`, `or`, `openspec/specs`, `openxFactory` |
| `doc-health` | `amend-published-tip-unreadable-scenario` (2026-09-05) | 1 | `WHEN`, `AND` |
| `doc-health` | `amend-unreadable-read-sibling-scenarios` (2026-09-05) | 1 | `WHEN`, `AND` |
| `repo-boundary-governance` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | `or`, `or`, `openspec/specs`, `or`, `and`, `THEN`, `AND` |
| `repo-boundary-governance` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | `OpenXPKI-Install`, `and` |
| `repo-boundary-governance` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | `or`, `or`, `openspec/specs`, `or`, `and`, `implement-omniworker-install-repo` |
| `shared-contract-ownership` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | `or`, `or`, `openspec/specs`, `or`, `and`, `opensoft/xFactory-Hermes-Install`, `FarHeap/Hermes-Install` |
| `shared-contract-ownership` | `refresh-install-repository-enumerations` (2026-09-08) | 1 | `a change proposes adding … as a submodule`, `or`, `openspec/specs`, `or a later install repository` |

**THE MEASUREMENT IS WHAT CHOSE THE PREDICATE, AND IT MOVED THE ISSUE'S OWN
WORDING.** Issue #729 proposed reporting a marker that *"carries a code span
INSIDE its reason"*. **That is not a defect predicate; it is the predicate for
canon's blessed form** — eight of this corpus's sixteen unit-naming markers are
written that way today, every one of them promoted, and the share is growing
(2 of 7 on 2026-09-06, 8 of 16 three days later). The narrow predicate this
packet encodes fires only where a reason-quoted span EXACTLY MATCHES a unit of
the basis the block does not carry, and **zero** reason-quoted spans in this
corpus are a unit at all.

**THE SHIPPING PATH.** 31 active MODIFIED blocks carry exactly **two**
unit-naming markers — `add-chain-attestation` (`Merged into`, one name, reason
present) and `add-composed-view-authoring` (`Merged into`, one name, no reason).
Neither fires either ground: both names match a unit of their resolved basis and
neither reason quotes a code span. **BOTH NEW GROUNDS RAISE ZERO FINDINGS ON
THIS CORPUS TODAY** — inert exactly as `design.md` D0 measures, and not idle:
the next mistyped name and the next reason quoting a dropped unit are told so.

## Impact

**Behaviour: none observable on this corpus today, by measurement.**
`python3 scripts/doc-health.py --single-repo . --family modified-block-currency`
is byte-IDENTICAL between `origin/main` in a separate worktree and this branch
once the repository-identity line is normalized — 9 `info` findings before and
after, 0 new, and **the report never names this change**. The full
`--single-repo .` run differs by nothing at all.

**Tests:** tests are ADDED to `tests/doc-health/test_modified_block_currency.py`
and one new fixture tree `tests/doc-health/fixtures/modified-block-currency-void/`
is added, because
`test_every_finding_matches_exactly_one_arm_template` requires every REGISTERED
template to be exercised over the corpus and the real tree raises zero. **THREE
assertions are EDITED**, each because a ninth arm template makes it literally
false rather than merely dated, and each named in `tasks.md` § 3.6: the arm
template count (`8` → `9`), the independent probe table (`" marker by "` no
longer discriminates once two templates share that opening), and its label map.
No other existing test is edited.

**Doc-health:** the `modified-block-currency` family reads this new active delta.
It drops one canon unit, that unit is named by the reserved marker, every other
unit and all 16 scenario titles are carried, and the two titles the block ADDS
are titles the arms never report — so the block raises **no** carriage finding,
measured rather than expected. **AND THIS BLOCK IS ITS OWN SELF-REFERENCE TEST
TWICE OVER**: it carries a PREDECESSOR'S promoted marker whose named unit is no
longer canon's, which is precisely the false positive the third ground's
own-change scope exists to prevent — measured, in `design.md` D2: with the scope
removed, this packet's block reports ITSELF.

**OpenSpec 1.12:** the block omits no scenario and retitles none — it replaces
one body sentence and appends two scenarios — so it adds no undispositioned
failure to `scripts/validate-openspec-cli-pin.py --all --no-cache`, which is run
in the pull request rather than assumed.

**No file is added under `openspec/specs/`**, so no codexFactory floor advance is
owed.

## Sequencing

`sequenced_after` is **ELECTIVE HERE AND IS NOT DECLARED.** The writers of this
requirement — `add-modified-block-currency-check`, `add-unclassified-finding-class`,
`govern-sibling-added-modified-deltas` and `amend-marker-reason-boundary` — are
all ARCHIVED and their text is in the canon this block restates. **No ACTIVE
change carries a `## MODIFIED` block for it**, grepped over `openspec/changes/`
on the tree this packet is authored on. The ledger row is seeded with
`--moved-by` this pull request and classes on archived partners only, so no
partner flips and no MOVEMENT LOG entry is owed.

## Ratification

**NOT RATIFIED. NO WORD HAS BEEN GIVEN OVER THIS TEXT, and none is implied by
anything in this packet.** Brett Heap said *"author the 729 packet"* — which
instructs a lane to author and decides no wording and no design decision. It is
recorded as the ORIGIN in this document's front matter and in `.openspec.yaml`,
which carries drafting provenance ONLY. `tasks.md` § 1 is UNTICKED and names
ratification as owed.

**THE VETO POINT IS `design.md` D1 — option A against option B**, and it is put
rather than assumed: A reports only a reason-quoted span that exactly matches a
unit of the basis the block does not carry; B reports any span inside any reason
and would fire on eight legitimate promoted markers the moment a block restated
one of their requirements. A is designed and encoded; B is written out beside it
with its cost. A veto of A is a veto of this delta's second ground, and the
packet does not land on it.

## What this proposal does NOT claim

- It does not claim either defect has ever suppressed a real unit, or ever
  reported a wrong one. Neither has; the measurement that says so is in this
  document, in `design.md` D0 and in a test.
- It does not change what the family reads, at which severity, in which
  repositories, or under which dispositions.
- It does not add a finding CLASS. The two new grounds are `CLASS_MARKERS`
  findings at `CLASS_MARKERS`' band and action, and `design.md` D3 says why one
  new TEMPLATE is nevertheless right and three would be wrong.
- It does not touch `suppression`: nothing new is suppressed and nothing stops
  being suppressed. Only its docstring's account of the third resolution moves,
  because that account becomes false.
- It does not touch `amend-marker-reason-boundary`'s boundary rule. A span inside
  a reason still names nothing; what changes is that the corpus now says so out
  loud where the span is a unit the block dropped.
- It does not amend `document-lifecycle`, whose marker grammar carries no
  reporting rule.
- **It does not edit any promoted marker, and it does not edit the archived
  deltas that carry them.** They are records of ratified removals. Reporting is
  about a marker's FIT to the block that carries it; a promoted marker in canon
  is read by nothing this packet changes.
- It does not report a marker a block CARRIES but did not WRITE, on either new
  ground — `design.md` D2, and it is a designed limit rather than an omission.
