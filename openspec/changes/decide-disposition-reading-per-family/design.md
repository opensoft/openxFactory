# Design: decide-disposition-reading-per-family

Status: draft
Kind: design

**EVERY DECISION THIS AUTHORING SESSION TOOK IS HERE, WITH ITS ALTERNATIVES AND
EACH ALTERNATIVE'S COST.** Brett Heap's word of 2026-09-11 — verbatim **"usage
reset, resume all. read handoff and resume and fan out wide and do as much as
possible in parallel"** — commissioned the authoring and took none of them.

**D1 IS FOUR MULTIPLE-CHOICE QUESTIONS, ONE PER CLASS, AND EVERY ONE IS OPEN.**
The eight families are grouped into four classes by the SHAPE of their finding
and of their entry, so the CLASS decision is taken four times rather than eight.
The recommendation is stated first in each. **A FIFTH RULING IS OPEN BESIDE
THEM AND IS NOT ONE OF THE FOUR**: the packet's own shape — decision-only with
`code_surface: none`, or a code surface declared now — is D3 here and
`tasks.md` § 1.5, and it is separate because it is a question about this packet
rather than about any family's entries. **FIVE OPEN RULINGS IN ALL: FOUR CLASS
QUESTIONS AND ONE PACKET-SHAPE QUESTION.** **NO ARM IS BUILT AHEAD OF THE
WORD**: `tasks.md` § 4 scopes what each veto would commission and leaves every
box open.

## 0. The brief

openxFactory [#966](https://github.com/opensoft/openxFactory/issues/966),
carrying § 7.2 of the ratified `tasks.md` of
`honour-grandfather-dispositions-in-ratified-provenance` (#939, archived
2026-09-11). That packet taught ONE family — `ratified-provenance` — to read a
dated, cited entry in the aggregation's `health/dispositions.yaml` and report a
matching ARCHIVED finding at `info` with its citation quoted. Every other
family's entries in that same file were untouched by it, deliberately (its
`design.md` D6), and what they mean is undecided.

## D0 — the measurement, taken before the design

**NOTHING BELOW RESTS ON A NUMBER ANYBODY TYPED, AND NO FIGURE IS CARRIED FROM
THE ISSUE.** The issue's 49/18/31 table was taken at `opensoft/xFactory`
`ecb0cade`; every figure here is re-measured at the shas named below.

**THE FILE.** `opensoft/xFactory` `main`
`0ecb370e8fec2c1ac78498adf8f6a4ea3ca1c9bb`, `health/dispositions.yaml`, blob
`9458d6c2794f0c0a937a82f7f58b802ab4b4027b`, sha256
`4d9034e34f4189ddf1d08c9a9cffbe467747357ac28cfdc3906701d9577a1c60`, 1701 lines,
**49 entries**, root a list. **18** carry `family: ratified-provenance` — the
population the parent packet settled — and the other **31** belong to eight
families.

**THE RIG.** An aggregation-shaped checkout: `openxFactory`
`8015d45fdf68b7bf60abb79dd152585d1a4330fd` (this branch's base),
`codexFactory` `dc67ad82cf4dd522e6fe033b1e56424bb1086630` under
`xFactories/`, `OpsxFactory` `7368cb49830cb332f9afce33c404671c6b92f8bb`,
`MedxFactory` `9f125a6ae2f12669e10822dd1123f824aedcae36`, and the real
dispositions file above at `health/`. Each family run as
`python3 scripts/doc-health.py --repo-root <rig> --family <f>`, exit 0 in every
case. Those four repositories are the only ones the thirty-one entries name.

### D0.1 — the population, per family

| entries | family | rows the rig reports for that family | canon declares a reading? |
| ---: | --- | ---: | --- |
| 10 | `location-conformance` | 7 | no |
| 8 | `proposal-origin` | 130 | no |
| 5 | `record-immutability` | 16 | no |
| 4 | `modified-block-currency` | 48 | **YES** — *A finding is dispositioned*, `openspec/specs/doc-health/spec.md` line 2177 |
| 1 | `document-catalog` | 1 | no |
| 1 | `semantic-contradiction` | — (LLM sweep; no deterministic run emits it) | no |
| 1 | `semantic-normative-prose` | — (LLM sweep; no deterministic run emits it) | no |
| 1 | `uncited-resolution` | — (emitted by `report.uncited_resolutions`, not by a family module) | no |
| **31** | **eight families** | | |

Canon declares a disposition reading for **FIVE** families and names each in its
own requirement: `promotion-fidelity` (spec line 1174), `duplicate-packet`
(1289), `modified-block-currency` (2177) — three scenarios all titled *A finding
is dispositioned*, all three SUPPRESSING — `ratified-provenance` (938), *A
finding is grandfathered by a recorded disposition*, the parent's DOWNGRADE, and
**`neutrality-drift`** at *A rejected candidate stays rejected* (681-685), whose
reading is a SUPPRESSION ON A DIFFERENT KEY: the disposition is recorded "keyed
by repo, path, and content digest", and `neutrality.disposition_suppressions`
builds `{(repo, path): {sha256, …}}` from entries carrying that lane's family,
suppressing only while the content digest is unchanged
(`scripts/doc_health/neutrality.py`, `disposition_suppressions` / `is_suppressed`;
reached from `runner._neutrality_scope` → `neutrality_dispatch`). A sixth
scenario — *The act that extends the class map records a disposition for the
finding it reclassifies* (2602), under the requirement *A modified-block-currency
finding its own class map cannot place is itself a finding* (2480) — reads a
disposition as suppressing for that same family. **OF THE EIGHT FAMILIES HOLDING ENTRIES, EXACTLY ONE IS AMONG THE FIVE**
— `modified-block-currency`. No entry in the measured population carries
`family: neutrality-drift`, which is why that lane changes no figure here; it is
named because the claim "the file has one reader" is false about the ESTATE even
where it is true about this population, and a later reader must not inherit the
narrower claim.

### D0.2 — does each entry's `(repo, path)` draw a finding of its family today?

Thirty-one entries, one row each, collapsed by outcome:

| outcome | entries | which |
| ---: | --- | --- |
| **matched** — the path draws a live finding of that family | **10** | `proposal-origin` 7 (5 `warning`, 2 `error`), `record-immutability` 3 (all `critical`) |
| **unmatched**, target present — the path exists and draws no finding of that family | **7** | `location-conformance` 3, `modified-block-currency` 2, `record-immutability` 2 |
| **target vanished** — the path does not exist in the repository named | **11** | `location-conformance` 7, `modified-block-currency` 2, `proposal-origin` 1, `document-catalog` 1 |
| **not deterministically measurable** — no deterministic run emits this family | **3** | `semantic-contradiction` 1, `semantic-normative-prose` 1, `uncited-resolution` 1 (all three targets present) |

**NOT ONE OF THE THIRTY-ONE NAMES A PATH UNDER `openspec/changes/archive/`.**
A set test over the thirty-one, not a count: zero. So the parent's ground in its
strongest form — `govern-archived-record-edits` putting an archived packet's
bytes beyond ANY fix, so the owner rules because nobody can edit — **does not
reach this population**.

**THAT TEST IS NOT THE IMMUTABILITY TEST, AND THE FIRST FILING OF THIS PACKET
READ IT AS ONE.** `fam_record_immutability` does not scan a path prefix: it
scans every governed document whose `Status:` is `record`, wherever it sits
(`scripts/doc_health/families.py`, `fam_record_immutability`:
`for doc in ctx.docs: if doc.status != "record": continue`). The status was
therefore read off each `record-immutability` target directly, at the D0 rig:

| entry target | `Status:` header | immutable in the parent's sense? |
| --- | --- | --- |
| `openxFactory docs/domain-ontology-pilot-report.md` | `record` | no — a revert is available to its owner |
| `openxFactory docs/archive-record-discrepancies.md` | `record` | no — same |
| `MedxFactory examples/patient-assembly/runs/08-connector-input/p1-divergence-report.md` | `record` | no — same |
| `codexFactory docs/browser-ui-repair-lineage-reissue-2026-09-10.md` | `record` | no — same |
| `openxFactory ideation/cross-reference.md` | `projection` | not a record at all |

**FOUR OF THE FIVE ARE `Status: record` DOCUMENTS.** What separates them from
the parent's population is not the status but the REMEDY: this family's own
action text names one — *"revert the content edit or re-issue as a new record"*
— and none of the four sits under `openspec/changes/archive/`, where
`govern-archived-record-edits` forbids the revert. The anticipated class is
therefore NOT EMPTY; it is WEAKER than the parent's, and the split that implies
is put to Brett Heap as Class C option **(C4)** rather than taken here.

### D0.3 — the control: what would change if the file were empty?

The real file was replaced by `[]` and every deterministic family that holds
entries re-run at the same rig:

| family | plan rows, real file | plan rows, `[]` | `diff` of the row sets |
| --- | ---: | ---: | --- |
| `location-conformance` | 7 | 7 | empty |
| `proposal-origin` | 130 | 130 | empty |
| `record-immutability` | 16 | 16 | empty |
| `modified-block-currency` | 48 | 48 | empty |
| `document-catalog` | 1 | 1 | empty |

**THIRTY-ONE ENTRIES, ZERO STANDING DETERMINISTIC-FAMILY ROWS MOVED — AND THE
HEADLINE IS SCOPED TO WHAT THE CONTROL MEASURED AND NOT ONE STEP WIDER.** This
table compares the STANDING plan rows of the five deterministic families that
hold entries and nothing else. The separate, derived effect — 30
`uncited resolution` findings without the file and 0 with it — is D0.4's
measurement, not this one, and the two must never be read as one figure.
`modified-block-currency` — the one of
the eight whose module DOES read the file under its own name, through
`promotion_fidelity.load_dispositions(ctx, FAMILY)` — suppresses nothing today
either, because its four entries match no finding it currently raises. The file
was restored to its measured sha256 after the control.

### D0.4 — the estate-wide arm, what it can reach, and the one entry it cannot

`report.uncited_resolutions` keys on `(family, repo, path)` for EVERY family,
so an entry of ANY family silences the `uncited resolution` error that would
otherwise be raised when its CONTESTED finding stops being reported. **THE
CONDITION IS LOAD-BEARING AND IS STATED BEFORE THE FIGURE**: that arm iterates
`previous_contested` and nothing else, and `report.parse_previous` admits a key
to that set only from a previous-report row written `class="contested"`
(`if m.group(7) == "contested" and m.group(2) != UNCITED_RESOLUTION_FAMILY`).
An entry whose family never emits a contested finding is therefore never reached
by it either.

Measured by building a synthetic previous report carrying one
`class="contested"` ranked-plan row per entry and running
`report.parse_previous` and `report.uncited_resolutions` over it — which
measures the LOOKUP, with the class forced, and is reported as that and not as a
production count:

- 31 rows written; **30 admitted** to the contested set.
- `uncited_resolutions` with an EMPTY disposition set: **30** findings.
- `uncited_resolutions` with the real file: **0** findings.
- The ONE row refused admission is the `uncited-resolution` entry itself:
  `parse_previous` never admits an `uncited-resolution` row to `contested`
  (`report.UNCITED_RESOLUTION_FAMILY`, the anti-echo of issue #515), so that
  key can never reach the lookup. **It disposes nothing, now or ever.**

**AND THE CLASS THE SYNTHETIC ROWS FORCED IS MEASURED RATHER THAN ASSUMED.** The
same rig runs, read for `class="…"` rather than for row counts:

| family | entries | resolution class of that family's rows at the rig | reachable by this arm on today's classes? |
| --- | ---: | --- | --- |
| `location-conformance` | 10 | `contested` 7/7 | yes |
| `record-immutability` | 5 | `contested` 16/16 | yes |
| `modified-block-currency` | 4 | `contested` 48/48 | yes |
| `proposal-origin` | 8 | **`auto-fixable` 130/130** | **no** |
| `document-catalog` | 1 | **`auto-fixable` 1/1** | **no** |
| `semantic-contradiction` / `semantic-normative-prose` | 2 | not deterministically emitted | not measurable here |
| `uncited-resolution` | 1 | — | no, by construction (above) |

**NINETEEN OF THE THIRTY-ONE BELONG TO A FAMILY WHOSE ROWS ARE CONTESTED AT THIS
RIG; NINE BELONG TO FAMILIES WHOSE 131 ROWS ARE ALL `auto-fixable`.** So the
honest statement of the arm's reach is a CONDITIONAL one: thirty of the
thirty-one are admissible to the lookup BY KEY, and the lookup fires only for a
prior finding recorded `contested` — which, on today's classes, nine of them
could never have been. That does not weaken the recommendation; it strengthens
the class boundary, because the eight `proposal-origin` entries and the one
`document-catalog` entry turn out to be inert on every arm that exists today,
and their disposers wrote them as audit trail rather than as suppression.

### D0.5 — what the entries say about themselves

**TEN** of the thirty-one state their own effect in their `rationale`,
correctly, in prose, in another repository, because canon does not state it —
and they do it in **three** distinct patterns, one quoted per pattern below
(`proposal-origin` ×8 share one wording; the other two are one entry each):

> nothing is suppressed by this entry. Its purpose is the permanent audit trail
> of the 2026-09-11T11:02Z ruling, and to pre-empt a future uncited-resolution
> ERROR if the finding ever stops being reported — `proposal-origin` ×8

> the CRITICAL is NOT suppressible and is reported live either way (measured — a
> run with this entry present is byte-identical to a run without it)
> — `record-immutability`, `openxFactory docs/archive-record-discrepancies.md`

> The finding remains visible as a warning; only the spurious uncited-resolution
> ERROR is disposed here. — `semantic-contradiction`

**THE WRITERS' RECORDED INTENT IS THAT THE STANDING ROW STAYS.** That is
evidence about what the mechanism is FOR, and it is why the recommendation below
is not the parent's.

## D1 — THE DECISION: four classes, four questions, recommendation first

(The fifth open ruling, the packet's own shape, is D3 — it is not a class and is
not counted among these four.)

### Class A — ALREADY RULED BY CANON: `modified-block-currency` (4 entries)

Canon's *A finding is dispositioned* (spec line 2177) already tells this family
what an entry means: *findings on that path MUST be suppressed, or only the
named requirement's findings where the entry carries a `requirement` key*.
Measured: all four entries suppress nothing today (D0.3), two targets have
vanished and two are present but draw no finding of this family.

**RECOMMENDED — (A1) NO CHANGE.** The question was answered when the family's
requirement was promoted; re-deciding it here would be a second rule about the
same entries, and two readers of one file that can disagree is the drift this
estate has written about repeatedly.

- **(A2) Narrow it** — restate the reading as `info`-with-citation to match the
  parent. Cost: a `## MODIFIED` over a promoted scenario, a code change in
  `modified_block_currency.py`, and a family whose contract now disagrees with
  its two suppressing neighbours for no measured reason — the population it
  would change is ZERO.
- **(A3) Widen it** — admit archived delta paths as well as active ones. Cost:
  the same distinction D2 of the parent refused, in the family where an active
  delta is one commit from correct.

### Class B — DISAPPEARANCE CITATIONS: `location-conformance` (10), `document-catalog` (1) — 11 entries

Every one of these was written because a contested finding DISAPPEARED for a
cited reason: a change workspace archived, a promotion that moved the document,
a detector repair (PR #505), a lifecycle reclassification. Measured: 8 of the 11
targets no longer exist in the repository at all; the other 3 exist and draw no
finding of their family. The entry is doing the file's ORIGINAL job — it is the
citation the contested-resolution rule asks for — and it is doing it today.

**RECOMMENDED — (B1) DELIBERATELY IGNORE: no family-side reading; the entry
stays a resolution citation and nothing else.** The finding is already gone; a
downgrade arm would have a population of ZERO and a suppression arm would have
nothing to suppress. The entry is not a governance record ABOUT a standing
defect, it is the record of why a defect stopped being reported.

- **(B2) Read and downgrade** (the parent's reading). Cost: an arm in two family
  modules, its tests, and a `## MODIFIED` over two promoted requirements, for a
  set of findings that do not exist. The first entry that ever matched would be
  one where the finding came BACK — and downgrading it to `info` would hide a
  regression behind a citation written for its disappearance.
- **(B3) Read and suppress** (the three siblings' reading). Cost: the same arm,
  plus the standing risk that a re-appearing finding is silenced by an entry
  written about a different event. `location-conformance` is CONTESTED and its
  findings are repairable: suppression here buys nothing and can hide a defect.

### Class C — AUDIT TRAIL BESIDE A STANDING, REPAIRABLE FINDING: `proposal-origin` (8), `record-immutability` (5), `semantic-contradiction` (1), `semantic-normative-prose` (1) — 15 entries

Measured: **10 of the 15 draw a live finding today** — 7 `proposal-origin` (5
`warning`, 2 `error`) and 3 `record-immutability` (all `critical`). Two more
name a present target that draws nothing, one names a vanished target, and the
two semantic entries name findings only the LLM sweep emits.

**THE REPAIRABILITY IS MEASURED PER TARGET, NOT INFERRED FROM A PATH PREFIX**
(D0.2). None of the fifteen names an archived path, so none is beyond repair in
`govern-archived-record-edits`' absolute sense — but FOUR of the five
`record-immutability` targets ARE `Status: record` documents, and calling them
"repairable" is true only because this family's own action text names the repair
("revert the content edit or re-issue as a new record") and no archive rule
forbids it. That is a WEAKER distinction from the parent's than the first filing
of this packet claimed, and it is the reason (C4) below exists. Ten of the
fifteen entries say in their own `rationale` that nothing is suppressed and the
row stays visible.

**RECOMMENDED — (C1) DELIBERATELY IGNORE: no family-side reading; the entry is a
governance record and the finding keeps its band.** This is the decision the
entries were written under, it is what the nightly does today, and it keeps the
one distinction the parent's D2 bought at the cost of an `and` in a predicate:
a ruling is recorded on something nobody can repair, and a deferral is recorded
on something nobody has repaired yet. An arm here would turn every one of these
fifteen into the second.

- **(C2) Read and downgrade to `info` with the citation** (the parent's
  reading). Cost: an arm reaching four family modules and the semantic lane,
  tests, and a `## MODIFIED` over each family's requirement. It would move **10
  measured rows** — including three `critical` record-immutability rows — and it
  would extend a remedy built for immutable records to records somebody can
  edit this afternoon. A reader who then repairs the document gets no signal
  that the entry is now stale (`#965`'s subject, at ten times the population).
- **(C3) Read and suppress** (the three siblings' reading). Cost: the same arm,
  and the ten rows vanish from the report entirely. Two of the entries state in
  terms that their authors did NOT intend this; adopting it would silence
  findings their own disposers expected to stay visible, and would make the
  count of dispositioned-but-live defects unreadable from the artifact.
- **(C4) SPLIT THE CLASS ON THE MEASURED STATUS** — `record-immutability`'s four
  `Status: record` targets ruled separately from the rest, on the ground that a
  record's repair is a REVERT-OR-REISSUE rather than an edit. Cost and honest
  statement of it: this is the only option here that could carry the parent's
  downgrade reading into any of this population, and it is put as an option
  BECAUSE THE MEASUREMENT SUPPORTS PUTTING IT — but it splits one ruling into
  two, and the three `critical` rows it would move are rows whose own disposer
  wrote that the CRITICAL "is NOT suppressible and is reported live either way".
  **This packet does not take it**; a class is Brett Heap's to rule, and the
  recommendation above remains (C1).

### Class D — THE DEAD LETTER: `uncited-resolution` (1 entry)

`openxFactory :: openspec/specs/shared-contract-ownership/spec.md`, recorded
2026-08-14. Measured (D0.4): `report.parse_previous` never admits an
`uncited-resolution` row to the contested set, so this key can never be looked
up by THE ONLY ARM THAT COULD LOOK UP A KEY OF THIS FAMILY — which is not the
only arm that reads the file at all (§ 2.6 enumerates the others) — and no
family module reads it either.
**It disposes nothing and can never dispose anything.**

**RECOMMENDED — (D1a) RECORD THAT IT IS INERT AND LEAVE IT.** It costs a reader
nothing, it is the governance record of the 2026-08-13/14 triage, and retiring
an entry is an act in `opensoft/xFactory`, not here.

- **(D1b) Teach the arm to read its own family's entries.** Cost: it re-opens
  exactly the infinite echo issue #515 closed. Refused on that ground unless
  Brett rules otherwise.
- **(D1c) Retire the entry in the aggregation.** Cost: a pull request in another
  repository and a judgement about a 2026-08-14 triage nobody here witnessed. It
  is NOT [#965](https://github.com/opensoft/openxFactory/issues/965)'s either:
  that successor's packet (PR #981) limits itself to `ratified-provenance` by
  name and by construction, so this entry is outside its subject. If Brett takes
  (D1c) it needs a successor of its own, named at the ruling; until then it is
  unassigned residue and (D1a) leaves it where it is.

### The class the brief anticipated, and what the measurement actually did to it

The commissioning brief and the issue both anticipated a class of families whose
findings are about ARCHIVED records frozen by `record-immutability` /
`govern-archived-record-edits`, for which the parent's downgrade-with-citation
reading would apply unchanged. **IT HAS NO MEMBERS IN THAT EXACT SHAPE, AND IT
IS NOT EMPTY IN THE SHAPE A PATH TEST MISSES.** Zero of the thirty-one entries
names a path under `openspec/changes/archive/`, so the absolute bar reaches
none of them; but four of the five `record-immutability` targets ARE
`Status: record` documents (D0.2), which is the status that family actually
scans. The residue is a WEAKER version of the anticipated class, and it is
carried as Class C option **(C4)** rather than dropped — recorded here in terms
because the next lane to read the issue will look for this class, and because
the first filing of this packet said "empty" on the path test alone and was
right to be corrected.

## D2 — the arm the recommended rows imply: NONE, and the seam is named anyway

**UNDER THE FOUR RECOMMENDATIONS NO ARM IS OWED**, which is why `code_surface`
is `none`. Should a class be VETOED toward (B2)/(B3)/(C2)/(C3), the seam is
already cut and `tasks.md` § 4 scopes it without building it: the parent wired
`ratified-provenance` as a LAST PASS over the family's returned findings
(`families.fam_ratified_provenance` returns
`_honour_grandfather_dispositions(ctx, findings)`), delegating the admission
rule to `promotion_fidelity.load_dispositions(ctx, <family>)` — **the SHARED
FAMILY-SIDE ADMISSION HELPER, which is not the estate's only reader of the
file**: `runner.main` loads the same file independently to build the disposition
set `report.uncited_resolutions` reads, and the neutrality lane has its own
digest-keyed reader (§ 2.6 enumerates all of them) — and supplying only the
citation text that helper does not return. A
vetoed class would take the same shape ONE LEVEL UP: one shared helper, called
by each opting-in family with its own family name, so a second admission rule is
never written. Per-family opt-in is the whole point — an entry naming one family
has never disposed another's findings, and ONE FAMILY-SIDE ADMISSION HELPER is
how that stays true.

## D3 — RECOMMENDED: this packet ratifies the DECISION ONLY, `code_surface: none`

**RECOMMENDED: the decision is the deliverable; any arm a veto commissions is a
per-family successor with its own packet.**

Under the four recommendations NO ADDITIONAL ARM IS COMMISSIONED — not "no arm
exists": `modified-block-currency` already carries a family-side reader of its
own (D0.1, D0.3), and (A1) deliberately keeps it. The choice is therefore only
about what a VETO would do. Carrying a non-empty `code_surface` speculatively
would mean declaring a realization surface for work nobody has commissioned, and
under `release-realization` it would hold the archive on merged-plus-green
evidence for a diff of pure governance text.

- **The alternative** — declare `scripts/doc_health/` + `tests/doc-health/` now
  and add at least a regression test pinning "an entry of an unreading family
  moves no STANDING FINDING OF THE FAMILY IT NAMES" — scoped that way and not to
  "moves nothing", because D0.4 measures a deliberate 30-to-0 change in the
  DERIVED `uncited resolution` findings and a test written the wider way would
  encode the opposite of the first added scenario. Cost: it builds the first inch of an arm ahead of the word,
  and the control run in D0.3 already proves the property at the rig, on demand,
  with no test to maintain. **The trade-off, stated plainly:** the recommended
  route leaves the boundary unpinned by any test, so a future refactor could
  break it silently; the alternative pins it but commissions code the ruling has
  not asked for. The recommendation takes the first and names the test as owed
  residue in `tasks.md` § 7, where a successor can pick it up under its own word.
- **If Brett vetoes a class toward an arm**, `code_surface` changes AT THAT
  RULING to name the modules and tests § 4 scopes, and the archive moves to
  merged-plus-green for that reason. That is an addition beside a fixed `kind`
  and `id`, exactly as `add-drafted-proposal-origin` (#318) defined.

## D4 — the `--single-repo` asymmetry is NOT taken here

`health/dispositions.yaml` lives at the AGGREGATION root and a `--single-repo`
run has `Context.agg_root is None`, so no disposition of any family applies in
that scope — this repository's own gate reports every one of these findings at
its own severity, and will continue to whatever Brett rules above. Whether a run
whose job is to report THIS repository's defects should consult another
repository's disposition file at all is
[#968](https://github.com/opensoft/openxFactory/issues/968), filed by the
parent's § 7.4, and it is left there rather than answered by a packet about a
different question. The added scenario is written so that it says nothing about
scope: it constrains what an entry MEANS, not where the file is found.

## D5 — the LIMIT of this packet, stated so no reader has to infer it

- **`ratified-provenance`'s eighteen entries are settled by the parent and are
  not re-opened.** THE PARENT IS THE CAPABILITY'S DECLARATION FOR THAT FAMILY —
  `doc-health`'s promoted *A finding is grandfathered by a recorded disposition*,
  which the parent added. The added scenario here is conditioned on the ABSENCE
  of such a declaration, so it never reaches `ratified-provenance` and cannot be
  read over the parent's downgrade rule; the second added scenario states that
  boundary in terms, for `promotion-fidelity`, `duplicate-packet`,
  `modified-block-currency` and `ratified-provenance` alike.
- **STALE ENTRIES ARE NOT THIS PACKET'S SUBJECT, AND — RE-MEASURED AGAINST
  #965'S OWN PACKET — THE RESIDUE OUTSIDE `ratified-provenance` HAS NO OWNER
  TODAY.** [#965](https://github.com/opensoft/openxFactory/issues/965) is the
  stale-disposition successor filed by the parent's § 7.1, and its packet is PR
  #981. **#981 DECLINES THE REST BY NAME**: its own D5 says the 31 entries of
  the other eight families are "a question about a different subject … and it is
  #966's", and its `proposal.md` repeats it — and its arm is narrow BY
  CONSTRUCTION, `_grandfather_cites` asking
  `promotion_fidelity.load_dispositions(ctx, "ratified-provenance")` for its key
  set, so an entry naming another family can never be reported by it however the
  file grows. An earlier draft of this bullet said the residue was HANDED to
  #965; that was wrong and is corrected here rather than left for a reader to
  discover. The measurement stands — **eleven of the thirty-one name a path that
  no longer exists**, and seven more name a present path that draws no finding —
  and it is recorded as **UNASSIGNED RESIDUE**: this packet decides what an entry
  MEANS and does not grade staleness, #981 rules staleness for one family only,
  and **no successor is named for the other eight**. Naming one is an act for
  Brett Heap's word, not for this filing, and `tasks.md` § 7.2 records it in the
  same terms rather than ticking on a hand-off that would not be honoured. No
  finding class is graded and no severity is chosen by this packet.
- **NO ACTIVE SIBLING DELTA COLLIDES WITH THE HEADING THIS PACKET MODIFIES, AND
  THE COORDINATION WAS TAKEN LATE ON PURPOSE — LATE ENOUGH THAT THE ANSWER
  CHANGED UNDER IT.** #965's packet is the one that could collide, and it now
  EXISTS: **PR [#981](https://github.com/opensoft/openxFactory/pull/981),
  `report-stale-grandfather-dispositions`, DRAFT, opened 2026-09-11T20:40Z** on
  `change/report-stale-grandfather-dispositions` — after the two earlier runs of
  `gh pr list --repo opensoft/openxFactory --search 965 --state open` (taken
  after this branch merged `origin/main` `c521504c` and again after `d4d96cca`)
  had both returned only this pull request. **MEASURED RATHER THAN ASSUMED**:
  `git show origin/change/report-stale-grandfather-dispositions:openspec/changes/report-stale-grandfather-dispositions/specs/doc-health/spec.md
  | grep '^### Requirement'` returns exactly one heading, *Governed corpus
  membership and the lifecycle scan set*, under a single `## MODIFIED
  Requirements` block. **THAT IS NOT THIS PACKET'S HEADING**, so the two deltas
  touch disjoint requirements of the same capability and **NEITHER OWES
  `sequenced_after:` TO THE OTHER**. #981's own `.openspec.yaml` `related:`
  records this pull request and reaches the same conclusion in the same terms,
  which is the two lanes agreeing rather than one lane deciding for both. Two
  differences are recorded here so a later reader does not have to re-derive
  them: #981 carries a CODE SURFACE (`scripts/doc_health/families.py` and
  `tests/doc-health/test_grandfather_dispositions.py`) where this packet carries
  none, and both branches seed a row in `tests/sequenced_after/corpus-ledger.yaml`
  — a textual merge matter for whichever lands second, never a sequencing one.
  The whole open set was listed as the control
  (#979, #977, #976, #963, #962, #888, #594, #518 and this one), and the
  repository-wide search
  `grep -rn "Finding severity and regression handling" openspec/changes/ |
  grep -v /archive/ | grep -v decide-disposition-reading-per-family` returns
  NOTHING (exit 1). The third filter is part of the test and not a way of hiding
  a hit: WITHOUT it the command returns exactly FOUR lines and all four are this
  packet's own — `proposal.md`, `specs/doc-health/spec.md`, `tasks.md` and this
  `design.md`, the last two because each QUOTES the command it is reporting on —
  which is the self-match `tasks.md` § 3.4 records in the same terms. `sequenced_after:` therefore stays
  `[]`. **IF EITHER PACKET LATER MOVES A DELTA ONTO THE OTHER'S HEADING, THE
  LATER-LANDING PACKET DECLARES `sequenced_after:` AT ITS ENCODE** — that is the
  sequencing plan, and neither packet declares a branch-only parent, #981 being
  a DRAFT branch and not an archived act.
- **ONE ACTIVE SIBLING TOUCHES THIS PACKET'S FRONT MATTER RATHER THAN ITS
  HEADING**, and is named so the next reader does not rediscover it:
  `gate-realization-axis-vocabulary` (PR #963, issue #956) adds a gate over
  `target_release:` with a CLOSED register. That register does not name this
  packet, and its own act corrects the token `none` in four sibling proposals, so
  this packet declares `target_release: implemented` — the ratified vocabulary's
  own value — rather than relying on an exception it could not be granted. Its
  delta is `## ADDED` over `release-realization` and touches no heading of
  `doc-health`, so it raises no sequencing question for this one.
