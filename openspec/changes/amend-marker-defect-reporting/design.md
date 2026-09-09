# Design: amend-marker-defect-reporting

Status: draft
Date: 2026-09-09
Kind: design

## 0. The brief

openxFactory issue **#729**, filed out of the adversarial review of PR **#685**'s
lineage, and the STOP measurement recorded on it (comment `5601771886`):

> a marker-defect finding (info) when a marker's reason carries a code span, or
> when a marker names something no unit matches, in the modified-block-currency
> family.

The issue offers two cases. This document takes the second as offered, takes the
first ONLY under a narrower predicate the measurement forced, writes the issue's
own predicate out beside it with its cost, and names the choice as the packet's
veto point.

## D0 — the measurement, taken before the design and re-derived on this branch

Every unit-naming marker in `openspec/specs/*/spec.md` and every active
`openspec/changes/*/specs/*/spec.md`, read through `derive_units` so fenced
example markers are never offered. Taken 2026-09-09 at `main` `245ee85a`:
**115 files, 18,394 derived units.**

| measure | value |
|---|---|
| unit-naming markers in the corpus | **16** |
| carrying a code span INSIDE the reason | **8** |
| reason-quoted spans that ARE a derived unit of their document | **0** |
| active MODIFIED blocks | **31** (23 resolved, 8 pending, 0 unresolved) |
| unit-naming markers the FAMILY reads (resolved blocks) | **2** |
| ground 2 findings today | **0** |
| ground 3 findings today | **0** |

**THE FIRST HALF IS WHY THE ISSUE'S WORDING COULD NOT SHIP.** Eight of sixteen
unit-naming markers quote a code span inside their reason. Every one of the eight
is PROMOTED — five of them by `refresh-install-repository-enumerations` alone —
and every quoted span is reason-prose: `or`, `and`, `WHEN`, `THEN`,
`openspec/specs`, a repository name. Canon blesses that shape in as many words
(*"a code span that falls inside the reason is prose the reason quotes rather
than a unit the marker names"*), so a rule reporting "a code span INSIDE the
reason" reports canon's own normal form. The share is GROWING, which is what
makes it a design fact rather than a coincidence: 2 of 7 on 2026-09-06, 8 of 16
on 2026-09-09.

**THE SECOND HALF IS WHY THE NARROW PREDICATE IS SAFE.** Zero reason-quoted
spans in the whole corpus are a derived unit of the document that carries them.
So the narrow predicate is silent on all eight, measured rather than argued.

**THE THIRD HALF IS THE SHIPPING PATH.** Two unit-naming markers reach the
family at all — `add-chain-attestation` and `add-composed-view-authoring`, both
`Merged into`, both naming one unit that matches their basis. Both grounds report
ZERO today. The defects are INERT AND NOT HARMLESS: what is lost while they are
silent is the diagnosis, and the diagnosis is the whole of what this family gives
an author.

## D1 — THE VETO POINT: option A (the narrow predicate) against option B (the issue's)

**A — RECOMMENDED, AND WHAT THE DELTA ENCODES.** Ground 2 fires only where a
code span standing AFTER the reason boundary matches, after the same whitespace
normalization every unit is read under, a unit of the BASIS that the block does
NOT carry. That is a would-be DECLARATION: the author wrote the unit's exact
bytes, on the wrong side of the separator, about a unit that is in fact missing.

- **It is silent on every promoted marker in the corpus** (D0: zero reason-quoted
  spans are a unit).
- **It distinguishes a declaration from a mention by CONTENT, which is the only
  axis left.** Position cannot distinguish them, because
  `amend-marker-reason-boundary` has already ruled what position means.
- **It is silent on a quoted span matching a unit the block DOES carry.** Canon
  carries it, the block carries it, nothing is being dropped, and the author is
  quoting text that is present. Reporting there would be a report about a
  quotation.
- **It is silent on a span the marker ALSO names before the separator** — that is
  a marker declaring a unit once and mentioning it once, which is ordinary prose.
- **It is the case a test already builds.**
  `test_a_reason_quoting_a_REAL_canon_unit_suppresses_it_under_the_retired_rule`
  constructs exactly this shape as the harm `amend-marker-reason-boundary`
  removed; this packet reports what that removal left behind.

**B — REJECTED FOR COST, AND IT IS THE ISSUE'S OWN WORDING rather than a straw
one.** Report any marker whose reason carries a code span. What it costs:

1. **It fires on canon's blessed form.** EIGHT of sixteen unit-naming markers
   today, every one promoted, the moment a MODIFIED block restates one of their
   requirements — and the population grows with the corpus.
2. **It reports authors who did exactly what canon asks.** A reason is prose and
   prose in this corpus quotes; the requirement's own reason for the boundary is
   that quoting is legitimate.
3. **It cannot be dispositioned cheaply.** The family is deliberately absent from
   `FAMILY_RESOLUTION`, so a finding that resolves without a citation does not
   become an `error` — but eight standing advisory rows on legitimate text is the
   standing-population shape this family's launch state was designed to avoid,
   and it would fall on whoever next restates one of those five requirements.
4. **It does not point at the defect.** "Your reason contains a code span" is
   true of most well-written markers; "your reason quotes a unit your block
   dropped" names the mistake.

**The veto is between A and B, and a veto of A is a veto of the delta's second
ground.** Ground 3 — a name matching nothing — is unaffected by the choice and
survives either way; if B is ruled, ground 2's sentence and its scenario are
withdrawn and re-authored, and the measurement is what a re-author starts from.

**A THIRD OPTION WAS CONSIDERED AND IS NOT PUT: report nothing about ground 2 and
take only ground 3.** It is coherent — ground 3 is the case
`suppression`'s docstring recorded — but it leaves the defect issue #729 was
actually filed about untouched, and leaves `Marker.quoted` unbuilt, so the next
author who quotes a unit they dropped is answered by a carriage row exactly as
today. Recorded so the ruling can take it if it wants it: ground 3 alone is a
strictly smaller packet, and everything in this one supports it unchanged.

## D2 — THE OWN-CHANGE SCOPE, and it is measured rather than cautious

**Grounds 2 and 3 are read ONLY against a marker whose change id is the block's
own change.** Ground 1 is untouched and stays unscoped.

**WHY IT IS NECESSARY, MEASURED ON THIS PACKET'S OWN BLOCK.** A marker promotes
into canon with the requirement that carries it. So a later block restating that
requirement carries a PREDECESSOR'S marker — whose named unit was removed from
canon by that predecessor and is therefore, necessarily, no longer a unit of
canon. That is ground 3's predicate exactly. **This block carries
`amend-marker-reason-boundary`'s promoted marker verbatim; with the scope removed
it reports ITSELF** — measured on this branch, one finding, naming the retired
sentence #719 removed. Unscoped, ground 3 would report every faithful
restatement of an amended requirement, forever, growing with each amendment, and
the corpus would learn to ignore the class.

**WHY IT IS PRINCIPLED AND NOT A PATCH.** The requirement already says a marker
*"is NOT a carriage unit, in either direction"* and that *"the durable record of
a deletion is the archived delta"*. A marker is a DECLARATION BY A CHANGE about
the block that change wrote; a marker a block merely carries forward is a
historical record it is obliged to restate. Only the change that wrote a marker
declares anything by it.

**WHY GROUND 1 IS NOT SCOPED.** It needs the named unit to be a canon unit the
block still carries. An inherited marker names units that LEFT canon, so it never
matches, and scoping it would move promoted behaviour for no defect. Checked
rather than assumed: no marker in this corpus names a unit canon re-acquired.

**MEASURED COST OF THE SCOPE TODAY: ZERO.** Both unit-naming markers the family
reads are declared by the change that carries them. The cost is prospective — a
block carrying a predecessor's marker whose reason quotes a unit the block
dropped is not reported — and it is the conservative direction: the unit is still
reported by the carriage arms, and the author is not blamed for a predecessor's
prose. It is stated in the delta's own text and in the fourth bullet of the new
`names something no unit matches` scenario, so it is canon rather than a code
comment.

## D3 — ONE new arm template, not two and not three

The two new grounds share ONE template, `TEMPLATE_MARKER_VOID`, with the
predicate in an interpolated `{why}`.

**WHY NOT TWO.** Brett Heap's shape ruling of 2026-08-28 — *"shape = arm
template, all interpolations masked"* — makes one shape one map entry and one map
entry one REMEDY. Both grounds land in `CLASS_MARKERS`, at `_LEDGER_SEVERITY`,
carrying `_MARKER_ACTION`; a `FindingClass` holds ONE action and
`test_every_finding_carries_its_class_s_band_and_action` compares each finding's
action to its class's constant, so the two grounds cannot carry different
remedies even in principle. Two templates would claim two remedies where there is
one. This is the same reading `govern-sibling-added-modified-deltas` applied to
the pairing class's FOUR reported states, which share one template for the same
stated reason.

**WHY NOT ONE — I.E. WHY NOT FOLD ALL THREE GROUNDS INTO `TEMPLATE_MARKERS`.**
Because `TEMPLATE_MARKERS` ends in an ASSERTION about its own predicate
(*"which the block still restates — a declaration that does not describe the
block"*) which is FALSE of both new grounds. Rewriting it would move a shipped
rule text that this suite pins by rendered bytes in 24 places and that a reader
may have dispositioned by text — a wider move than the packet needs, for a
cosmetic gain.

**AND THE OPENING IS DELIBERATELY `TEMPLATE_MARKERS`'.** `CLASS_MARKERS`' class
pattern is `_BLOCK_HEAD + r"carries a '\w+' marker by "`, so reusing that opening
means the class map already PLACES both new findings and the seventh class
(`unplaced-finding drift`) stays silent. A wording that did not reuse it would
raise one `warning` drift finding per unplaced shape — the STOP measurement said
so and it is verified in the pull request.

**THE `{why}` CLAUSES ARE WRITTEN AROUND THE INDEPENDENT PROBE TABLE.**
`tests/…_reporting.py` types one discriminating phrase per template, INDEPENDENTLY
of the module, and requires exactly one hit per finding. So neither clause may
contain another template's phrase — `" does not carry "` above all, which is why
the clause says "does not restate", `_MARKER_ACTION`'s own verb. And the
`markers` probe itself had to be re-pointed from `" marker by "` (now shared by
two templates) to `", which the block still restates"`, which is one of the three
edited assertions.

## D4 — THE SELF-REFERENCE HAZARD, twice, and how this block survives both

**FIRST, THE MARKER'S OWN READING.** This block's
`Removed from canon by amend-marker-defect-reporting (2026-09-09)` marker is read
by the family from `main` (which does not carry the realization) and from this
branch (which does). Under BOTH it must derive one name and no quoted span, so
its reason is written with **no code span anywhere in it** — inherited from
`amend-marker-reason-boundary`'s D4 and now made MANDATORY by this packet's own
ground 2 for every amendment marker whose reason would otherwise quote a unit.
Verified on the branch: `names=1`, `quoted=[]`, reason non-empty.

**SECOND, THE INHERITED MARKER.** The block also carries #719's promoted marker,
which is what D2 measures. Verified on the branch: the block raises **0**
findings from its own family, and with D2's scope removed it raises **1**.

**AND THE BLOCK IS ITS OWN CARRIAGE TEST.** 122 canon units, 121 carried, ONE
uncarried — the retired sentence — named by the marker and suppressed. 16 canon
scenario titles all carried, 2 added. Measured, not asserted.

## D5 — the retired unit is named with a SINGLE backtick fence, by canon's rule

The retired sentence contains no backtick, so a single-backtick span names it
exactly and CommonMark's longer-fence rule (which canon states for units that
DO carry backticks) does not apply. This is stated because the sibling amendment
needed a DOUBLED run and a reader comparing the two markers should not have to
work out why they differ.

## D6 — what is NOT taken here

- **No finding class is added.** Both grounds are `CLASS_MARKERS` findings. A
  class is something the delta DEFINES, and the delta defines grounds for
  reporting a marker, not a new kind of finding.
- **No severity moves and no `contested` classification is added.** The family is
  deliberately absent from `FAMILY_RESOLUTION` so that a corrected marker's
  finding DISAPPEARING does not become an `error` under the uncited-resolution
  rule — the same reason the existing marker-defect class carries no hedge and no
  contested class. The delta states the band and the class rather than leaving
  them to be inherited.
- **`suppression`'s behaviour is not touched.** Its third resolution still
  suppresses nothing and this function still reports nothing; the report is
  emitted beside it. Only its docstring's claim that the silence is deliberate
  moves, because that claim becomes false.
- **`parse_marker`'s names and reason are not touched.** `quoted` is additive.
- **The pairing form gets no `quoted`.** It names no units and its WHOLE tail is
  reason, so every span in it is a mention by construction and there is no
  would-be declaration to be about. Stated in the field's own comment.
- **`specs/019-modified-block-currency-family/spec.md` is not edited.** It is a
  BUILD RECORD of what `add-modified-block-currency-check` specified, pinned by
  no test and no gate, and precedent `amend-marker-reason-boundary` § 5.3 left it
  alone on the same argument. Recorded as residue in `tasks.md` § 5.
- **The estate-wide run is not taken here.** This lane is confined to its own
  clone; `tasks.md` § 5.4 carries what is owed and why the direction is safe.
