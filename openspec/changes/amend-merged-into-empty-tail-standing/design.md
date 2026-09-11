# Design: amend-merged-into-empty-tail-standing

Status: draft
Date: 2026-09-11
Kind: design

## 0. The brief

openxFactory **[#914](https://github.com/opensoft/openxFactory/issues/914)**,
filed UNCLAIMED by this lane at the archive of `amend-marker-declaring-nothing`
(PR [#926](https://github.com/opensoft/openxFactory/pull/926) → `114d6e3d`),
which owed it at its own `tasks.md` § 7.1 and `design.md` D6. The issue put TWO
options and asked for a ruling first — *"Rule the silence correct"* and
*"Report it as a sixth ground"*.

**BRETT HEAP RULED ON 2026-09-11, verbatim "Rule the silence correct in
canon"**, by multiple choice in session (~01:3xZ), recorded on #914 at
2026-09-11T02:06:38Z (comment
[`5628349929`](https://github.com/opensoft/openxFactory/issues/914#issuecomment-5628349929)).
A `Merged into` marker declares its DESTINATION in its PREFIX and owes no tail;
the silence is correct and canon IS TO SAY SO — which this packet proposes and
does not perform, promoted canon still carrying the undecided clause until the
archive act.

**THAT RULING REACHES D1's DIRECTION AND NOTHING ELSE ON THIS PAGE.** It was
given before a sentence existed, so it cannot have approved one. **D1 IS
THEREFORE STILL A VETO POINT** — the WORDING, put with the rejected alternative
written out beside it — and **D2 IS A SECOND ONE**, decided here by measurement
rather than by the ruling: whether the amendment owes a `Removed from canon`
marker. Every document in this packet is `Status: draft` and `.openspec.yaml`
carries no approval pair.

## D0 — the measurement, taken before the design, and the correction it forces

Every marker in `openspec/specs/*/spec.md` and every active
`openspec/changes/*/specs/*/spec.md`, read through `derive_units` (so this
requirement's own written-out examples, which are complete markers, are never
offered — exactly as they are never offered to a run). Taken 2026-09-11 on the
clone of `main` @ `96b4835b`, the corpus BEFORE this packet:

| measure | 2026-09-10 (the predecessor, @ `e0638f11`) | 2026-09-11 (@ `96b4835b`) |
| --- | --- | --- |
| markers of any form | 26 | **27** |
| of `Removed from canon` form | — | **15** |
| of `Merged into` form | — | **3** |
| of the pairing form (`Modified over …`) | 9 | **9** |
| **`Merged into` markers whose tail carries NO code span** | — | **0** |
| `Removed from canon` markers with an empty tail | 0 | **0** |
| pairing-form markers carrying no reason at all | — | **0** |
| active MODIFIED blocks the family reads | 30 | **29** |
| of those, blocks carrying a unit-naming marker | 2 | **2** |
| marker-defect findings a run raises | 0 | **0** |

**THE ISSUE'S OWN FIGURE IS CORRECTED RATHER THAN COPIED, AND THE CORRECTION IS
NOT COSMETIC.** #914 records *"9 pairing-form markers, none with an empty
tail"*. Nine is the count of the PAIRING form —
``**Modified over `<basis>`'s addition by …**`` — which is a THIRD form, and
not the form this packet rules on. The ruled shape belongs to the `Merged into`
form, of which the corpus carries THREE, and its population is **ZERO**
independently. Both zeros are real and both are now stated apart, because a
sentence written over a conflated count would be a sentence nobody could
re-derive: the pairing form names no units BY CONSTRUCTION (its whole tail is a
reason and `Marker.quoted` is empty for it), while a `Merged into` marker names
none only when its author writes none. The promoted sentence already keeps them
apart, and so does the replacement.

**THE SHIPPING PATH IS WHERE THE ZERO LIVES.** The family reads markers only
inside active `## MODIFIED Requirements` blocks. Of the twenty-nine active
blocks exactly TWO carry a unit-naming marker — `add-chain-attestation` and
`add-composed-view-authoring`, both `Merged into`, each naming exactly one
superseded title that matches its resolved basis. So the ruled shape has a
population of ZERO today, measured rather than assumed, and the silence has
never cost anybody a row.

**AND THE ZERO IS ALREADY ASSERTED AS A TEST, WHICH IS WHY NO TEST IS ADDED**
(`tasks.md` § 2.3): `test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT`
builds exactly this marker, asserts `names == []` and `quoted == []`, and
asserts the defect list is empty. The predecessor wrote it so the silence would
be *"a decision a later act can overturn rather than a gap it has to
rediscover"*. This is the later act, and it CONFIRMS the assertion rather than
flipping it — which is the whole difference between this packet and its
predecessor.

## D1 — THE VETO POINT: the sentence, and the sixth ground it is not

**RULED IN DIRECTION on 2026-09-11 by Brett Heap, verbatim "Rule the silence
correct in canon"**, as a multiple-choice ruling over #914's two options. **THE
DIRECTION IS SETTLED AND THE WORDING IS NOT** — this section is what a veto
would reach.

**A — WHAT THE DELTA ENCODES.** One sentence, added to the grounds paragraph
immediately after the fifth ground's scoping sentence:

> AND A `Merged into` MARKER WHOSE TAIL NAMES NO SUPERSEDED TITLE IS SILENT BY
> RULE RATHER THAN BY OMISSION: that form declares its DESTINATION IN ITS
> PREFIX, complete before the closing colon and where this form's declaration
> has always been read, so the tail names what the destination ABSORBED and a
> marker whose tail names nothing has still declared everything the form
> obliges it to declare; it SHALL NOT be reported on the fifth ground, which is
> read on the `Removed from canon` form alone, and where its tail carries NO
> CODE SPAN AT ALL it reaches none of the other four either, each of those
> being read through a name or a quoted span such a tail does not carry — so NO
> ground fires on it and NO ground is added here; a code span its reason DOES
> quote remains subject to the second ground exactly as in every other marker.

Four properties, each deliberate:

- **IT CANNOT BE READ AS A SIXTH GROUND.** It is a PROHIBITION — *SHALL NOT be
  reported* — in a paragraph whose grounds are all obligations to report; the
  count stays FIVE in the sentence directly above it, unedited; and the added
  scenario's THEN bullet says MUST NOT report. A ground is a thing a run emits,
  and this sentence emits nothing.
- **IT GIVES THE SHAPE A READING, WHICH IS WHAT THE PREDECESSOR SAID NOBODY
  HAD.** `design.md` D6 there left open *"whether it declares nothing, or
  declares a destination that absorbed nothing named here"*. The answer taken is
  the second: the DESTINATION is the declaration, the tail is what the
  destination absorbed, and a marker naming none has declared everything its
  form obliges it to — which is exactly the asymmetry with the removal form,
  whose prefix declares nothing at all and whose whole content is its tail.
  That asymmetry is why ground five exists for one form and this prohibition
  for the other.
- **IT IS DERIVABLE FROM CANON RATHER THAN FROM THE CODE.** The claim that no
  ground fires is checked against the FIVE grounds as canon states them, not
  against `suppression`: grounds one, three and four are read through the
  marker's NAMES and ground two through the spans its REASON QUOTES, so a tail
  with no code span reaches none of them, and ground five is scoped to the
  removal form in canon's own words. A reader can verify the sentence without
  opening a Python file.
- **IT IS SCOPED AT THE SHAPE, NEVER AT THE FORM.** A `Merged into` marker
  whose reason quotes a code span still has `Marker.quoted` populated and is
  still subject to the second ground. Without the final clause, *"IS SILENT BY
  RULE"* could be read as a blanket exemption for the form — which would create
  a real silence where the second ground currently reports, and would be the
  first thing this packet's own family should have caught.

**B — REJECTED, AND IT IS THE ISSUE'S OWN SECOND OPTION RATHER THAN A STRAW
ONE.** Report it as a SIXTH GROUND at `info`, on the `Merged into` form alone: one predicate
(`marker.form == "merged" and not marker.names and not marker.quoted`), one
`_WHY_*` template clause, the flipped test, and a `## MODIFIED` block with its
own scenario. **BRETT HEAP'S RULING IS WHY IT IS NOT ENCODED**, and its cost is
written out so the ruling is a choice on the record rather than an author's
preference:

1. **It would report a marker that declared everything its form requires.** The
   removal form's tail IS its declaration; the merge form's prefix is. A sixth
   ground would tell an author to name a superseded title where there may be
   none to name — a merge that absorbed unnamed material is a legitimate act,
   and the remedy the class's own ACTION offers (*"name a unit the block does
   not restate, or drop the declaration"*) would be advice to drop a
   declaration that is true.
2. **It costs a code surface this packet does not have.** B is a change to
   `scripts/doc_health/modified_block_currency.py`, a flipped assertion in
   `tests/doc-health/test_modified_block_currency.py`, and therefore
   `code_surface: openxFactory` — which under `release-realization` means the
   packet archives on merged-plus-green realization evidence rather than on
   landing. A is a canon-only edit. That is a real difference in the size of
   the act, and it is the reason the two options were put before the authoring
   rather than after it.
3. **It would need a new WHY clause that carries no interpolation**, like
   ground five's, and a sixth entry in a grounds sentence that already runs to
   five — while `_ARM_TEMPLATES` stays a count of REMEDIES and the remedy here
   is not the class's remedy.
4. **It is the harder rule to retire.** A ratified reporting ground is
   withdrawn only by another `## MODIFIED` block over the same sentence; the
   silence, if it ever proves wrong, is overturned by exactly the act this
   packet is — and the test that pins it is already written.

**THE COST OF VETOING A.** A veto of the WORDING costs the added sentence, the
added scenario and the `Removed from canon` marker's one name; the retired
clause would be restored verbatim and canon would keep its recorded
non-decision; and the packet would be re-authored against whatever wording the
veto names. **A VETO OF THE DIRECTION IS A DIFFERENT ACT** — it would reverse
the ruling of 2026-09-11 and send this back as option B with a code surface,
and this packet does not treat that as available to it.

## D2 — the marker: OWED, and decided by measurement rather than by preference

**THE QUESTION.** A pure ADDITION to canon owes no `Removed from canon` marker:
nothing is retired, every canon unit is carried, and the carriage ledger has
nothing to report. That is the cheaper shape and it was the first one tried.

**THE MEASUREMENT REFUSED IT, AND THE REFUSAL IS MECHANICAL.** The clause this
ruling contradicts — *"is a question this requirement does not decide"* — does
not stand alone. `derive_units` splits a body paragraph into SENTENCES, and the
whole of

> THE FIFTH GROUND SHALL BE READ ON THE `Removed from canon` FORM ALONE: … and
> a `Merged into` marker whose tail names no superseded title is a question this
> requirement does not decide, its destination standing in the prefix where that
> form's declaration has always been read.

is ONE unit, 478 characters, one sentence, one period. There is no instrument in
this corpus for retiring a CLAUSE. So the choice was: leave the sentence
standing and add a second sentence that contradicts it, or REPLACE the sentence
and declare the replacement.

**LEAVING IT WAS REFUSED BECAUSE IT WOULD MAKE CANON CONTRADICT ITSELF INSIDE
ONE PARAGRAPH** — and not subtly: the paragraph would say the requirement does
not decide the question, and then decide it, two sentences apart. This
requirement's own family exists to catch a block that misdescribes canon; a
canon that misdescribes itself is worse, and the predecessor packet made
exactly this call for exactly this reason when #857 named one paragraph and the
measurement found four sites (*"correcting one and leaving three would make
canon contradict itself inside one requirement"*).

**SO ONE UNIT IS RETIRED AND REPLACED IN PLACE, AND THE MARKER IS OWED.** The
figure, derived by the family's own `carried()` over the generated block: **165
canon units, 1 uncarried, that one named by the marker and suppressed, 0
marker defects, 21 of 21 promoted scenario titles carried, 0 missing**
(`tasks.md` § 3.1). The replacement carries the retired sentence's removal-form
scoping and its ENTIRE pairing-form exclusion word for word; only the merge
clause is dropped, and the ruling replaces it in the sentence added beside it.

**AND THIS PACKET'S OWN MARKER IS WRITTEN TO SURVIVE THE FIVE GROUNDS, WHICH IS
MEASURED RATHER THAN ASSERTED** (`tasks.md` § 3.3). ONE name, assembled from
`derive_units`' own output rather than retyped, so it cannot name a fragment;
the name contains backticks, so it is fenced with a LONGER run exactly as canon
requires; it matches a canon unit the block does not carry, so ground one
cannot fire and grounds three and four cannot be reached; the reason carries NO
code span at all, so ground two has nothing to resolve; and a name is present,
so ground five is vacuous. The family's own derivation over the branch reports
**0 marker defects** on it.

**THE PREDECESSOR'S MARKER IS DELIBERATELY NOT RESTATED**, on this
requirement's own rule that *"a marker is NOT a carriage unit, in either
direction"*: `amend-marker-declaring-nothing`'s promoted `Removed from canon`
marker names two sentences canon no longer carries, so restating it here would
make this block report ITSELF under ground three. The `AMENDED BY` note says so
in terms, so a reader does not read the omission as an oversight.

## D3 — why an OpenSpec change and not a patch

The sentence is PROMOTED, RATIFIED canon. Working rule 3 and this corpus's
document lifecycle admit exactly one instrument for changing a promoted
requirement — a ratified change carrying a `## MODIFIED` block — and the family
whose rule is being amended is the one that reads MODIFIED blocks for a living.
Editing `openspec/specs/doc-health/spec.md` directly would be the defect this
capability exists to report, and the `modified-block-currency` family would
report the next block that restated the requirement against the edited canon.

**AND THE CHECKER IS NOT WRONG ABOUT CANON.** `suppression` conforms to the
promoted sentence exactly — its fifth ground reads `marker.form == "removed"`,
and its own comment records the merge form's tail as *"a question nobody has
ruled"*. There is no bug to patch: the packet is a RULING over a question the
implementation correctly declined to answer, which is a change to the
requirement and not to the code.

## D4 — `code_surface: none` archives ON LANDING, and the archive is still a separate act

`release-realization` gives an empty code surface the LANDING-plus-task-list
rule rather than the merged-plus-green realization rule, which is the shape
`amend-modified-block-currency-standing` took two days ago. **THAT IS NOT A
LICENCE TO ARCHIVE IN THIS PULL REQUEST.** Nothing under `openspec/specs/` is
edited here; the promotion and the archive are ONE later act on a later word,
`tasks.md` § 5 stays OPEN, and openxFactory #914 closes THERE and not at this
landing — which is why this pull request's body carries `refs` and no closing
keyword, and why `closingIssuesReferences` is verified empty before it is
opened.

**THE EMPTINESS OF THE CODE SURFACE IS MEASURED, NOT ASSUMED.** The two
artifacts that already implement the ruled behaviour —
`scripts/doc_health/modified_block_currency.py`'s fifth-ground predicate and
`tests/doc-health/test_modified_block_currency.py::test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT`
— are CITED by this packet and edited by NOTHING in it. The diff is the packet
directory, one README row and one per-change sweep ledger row.

## D5 — the sibling search, pasted rather than summarised

Taken 2026-09-11 before the claim, on `main` @ `96b4835b` and against the live
pull-request list, in the order the lane-collision protocol requires (search by
FILE PATH, read it, then claim).

**ACTIVE CHANGES CARRYING A `doc-health` DELTA — THREE, OF WHICH TWO ARE
SIBLINGS:**

| change | operation | requirements it touches |
| --- | --- | --- |
| `add-nightly-dashboard-refresh` | `## ADDED` | *Ideation-dashboard image refresh lane*; *The refresh lane skips when its worker is unavailable and never falls back to a hosted runner*; *A refresh that changes nothing proposes nothing*; *The refresh lane proposes its pin as an envelope-shaped pull request*; *The refresh chain is landed by four separate authorities, and no actor holds more than its own rung*; *The refresh lane's outcome is visible in the nightly reporting surface*; *The refresh lane conserves the worker and identity authority the nightly already holds* |
| `settle-aging-staging-topics` | `## MODIFIED` | *Aging threshold defaults* |
| `amend-merged-into-empty-tail-standing` | `## MODIFIED` | *Currency of an active change's MODIFIED requirement blocks* (this packet) |

**NO OTHER ACTIVE CHANGE CARRIES A `## MODIFIED` BLOCK FOR THIS REQUIREMENT**,
so the two-writers ordering this very requirement reports is not in play and
`sequenced_after: []` is declared as an explicit root claim. The three OTHER
active changes that name the requirement at all mention it in PROSE —
`prepare-openspec-1-12-readiness/tasks.md`,
`disposition-codexfactory-floor-relocation-retitle/design.md`,
`disposition-codexfactory-declared-renames/design.md` — and carry no delta over
it.

**OPEN PULL REQUESTS — SEVEN, NONE OF THEM THIS SURFACE:** #940
(`split-opendox` § 5.2, the openDox shed), #937
(`amend-repo-boundary-governance-scope-first-line`, capability
`repo-boundary-governance`), #934 (retire the `corpus_adapter` replica), #921
(`state-header-window-budget`, capability `release-realization`), #888 (the
nightly derive-possibles register merge), #594 (a rescue snapshot), #518 (a
docs page). File lists were read for the three nearest — #921, #937 and #888 —
and not one touches `openspec/specs/doc-health/spec.md`,
`scripts/doc_health/modified_block_currency.py` or
`tests/doc-health/test_modified_block_currency.py`.

**OPEN ISSUES NAMING A MARKER — ONE, AND IT IS #914 ITSELF.** The TWO OTHER
issues this family's recent packets left open are #893 (the uncited-resolution
rule's per-class grain, filed by `amend-modified-block-currency-standing`) and
#915 (`specs/019` FR-018's three-grounds restatement, filed by
`amend-marker-declaring-nothing`), neither of which this packet touches or
forecloses — see D6. Two, and #914 itself, is the three this family is carrying.

**THE CLAIM.** It stands on #914 at 2026-09-11T02:06:38Z — the ruling comment
itself carries it — naming lane `openxfactory-1` and session `a9c24afc` and its
own sibling-search line (*"no open PR or active change names the pairing form's
empty tail"*). **THAT LINE'S "pairing form" IS #914'S COLLOQUIAL WORDING AND NOT
THIS PACKET'S TERM**, quoted as the record has it rather than silently repaired:
the shape searched for, and the shape ruled on, is the `Merged into` form, while
"pairing form" elsewhere in this packet and in `parse_marker` means the distinct
``**Modified over `<basis>`'s addition by …**`` form whose whole tail is a
reason. D0 corrects the same conflation where it reaches a FIGURE. The table
above is THIS AUTHORING'S re-derivation of that search,
taken against the tree and the live pull-request list before a byte of the delta
was written, so the claim rests on a search that was performed twice rather than
on one that was recited.

## D6 — what is measured and deliberately NOT taken here

- **`scripts/doc_health/modified_block_currency.py` IS NOT EDITED, AND THREE
  PIECES OF PROSE GO STALE AT THE PROMOTION — TWO IN THE MODULE, ONE IN ITS
  TEST.** `suppression`'s docstring (`:1432`) and the comment beside the
  fifth-ground predicate (`:1535`), both in the module itself, and the
  docstring of `test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT`
  (`tests/doc-health/test_modified_block_currency.py:2698-2710`) all say the
  merge form's empty tail is *"a question nobody has ruled"*. After the
  archive, none of the three is true. The PREDICATE and the ASSERTION are both
  correct either way and no behaviour moves, so this is a comment-currency
  debt across two files and not a defect; taking it here would give the
  packet a code surface and change its archive rule (D4). Recorded as residue
  in `tasks.md` § 6.1, with a successor to be NAMED at the archive act on the
  tick-on-the-recording rule of 2026-09-06, naming all three sites.
- **`specs/019-modified-block-currency-family/` IS NOT EDITED.** Its FR-018
  states the ONE reporting ground a marker had before
  `amend-marker-defect-reporting`, and the restatement is already owed by
  openxFactory #915, filed at the predecessor's archive and OPEN. This packet
  adds no ground, so it neither widens #915's scope nor discharges it, and the
  build record says nothing at all about the merge form's empty tail — checked,
  not assumed.
- **NO TEST IS ADDED OR CHANGED.** `test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT`
  already asserts exactly what this packet promotes, so a second test would
  assert the same fact twice and the suite's own count would move for nothing.
  The predecessor FLIPPED the assertion it inherited; this packet CONFIRMS it,
  and that difference is the packet.
- **`document-lifecycle` IS NOT AMENDED.** It owns the marker GRAMMAR — how a
  unit is NAMED — and carries no reporting rule, the boundary
  `amend-marker-defect-reporting` § 2.4 checked in both directions. Amending it
  would be the shape D1 of the predecessor packet rejected.
- **THE ESTATE-WIDE RUN IS NOT OWED.** The predecessor owed one because it
  ADDED two reporting grounds and a sibling repository's marker could have
  surfaced new advisory rows. Both directions of THIS amendment are silence: no
  finding starts being emitted, none stops, no severity moves and no
  suppression changes, so no governed repository can gain or lose a row and the
  uncited-resolution rule has nothing to fire on. Measured on this repository
  as well — the branch's `doc-health` finding set is identical to
  `origin/main`'s line for line (`tasks.md` § 4.6).
- **THE PAIRING FORM'S SILENCE IS NOT RE-OPENED.** It was ruled correct by
  `amend-marker-defect-reporting`'s `design.md` D3 on 2026-09-09 and the
  promoted sentence states it; the replacement carries that clause word for
  word and this packet neither widens nor narrows it.
- **NO PROMOTED MARKER AND NO ARCHIVED DELTA IS EDITED.** They are records of
  ratified removals, and every one of them is correct under the amended
  sentence.
- **THE UNCITED-RESOLUTION RULE IS NOT WIDENED TO FINDING-CLASS GRAIN.** That
  is openxFactory #893, filed by this family's earlier packet, and it is that
  issue's work rather than this packet's.
