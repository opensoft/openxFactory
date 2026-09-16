# Design: adopt-entry-grain-dispositions-form

Status: draft

**WHAT THIS DOCUMENT IS FOR.** D-1 is the MEASUREMENT this packet rests on —
the verifier's PURE, SOURCE-FREE entry-grain guard, refusal by refusal, with
the script and line each was taken from. D-2 and D-3 are the two decisions that
could reasonably have gone the other way, each put as a question with the
recommendation FIRST and the cost of the alternatives beside it, so a veto costs
one section rather than a re-author.

Every figure here was taken in this packet's authoring session on a FRESH clone
of `main` at `8944758c739e6658d2ef7a9be03549e33b415db2`, by importing
`scripts/validate-openspec-cli-pin.py` at its fixed authored path and CALLING
`pinned_dispositions` on in-memory records — no file opened, no `git` run, no
network reached — and by calling `scripts/doc_health/pin_shapes.py`'s own forms
on the same values. Line numbers are that commit's.

---

## D-1 — THE MEASURED PURE ENTRY-GRAIN GUARD, AND THE GAP IT MEASURES

**FIRST, THAT THE GUARD IS PURE AT ALL, WHICH IS WHAT MAKES IT TRANSCRIBABLE.**
`pinned_dispositions(pin)` (`scripts/validate-openspec-cli-pin.py:787`) takes
ONE argument, the parsed record, and reads nothing else. It is called at
`:1966` as part of CHECK 1, with the pin's other shape rules; the repository
identity — the first step of that check sequence that touches a tree — is asked
afterwards at `:1973`, and only `if dispositions`. The function's own docstring
states the reason (`:790-793`): *"Evaluated as part of check 1 — with the pin's
other shape rules and BEFORE anything is fetched — because a malformed
exception is a defect of the PIN"*. Every refusal below is therefore a refusal
"whose ONLY INPUT IS THE RECORD", which is canon's own definition of the guards
this adapter may track.

**THE SEVEN READINGS, MEASURED.** Each row was produced by calling the guard;
the "raised at" column is the line the `PinRefusal` was raised from, read off
the traceback, and the "condition" column is the line the test that reaches it
is written on. `dispositions[N]` in the messages is ONE-BASED.

| # | reading | condition | raised at | measured input | guard | adapter today | named by canon, or guard-only |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | member ABSENT or `null` is EMPTY — not a refusal | `:801-803` | — | absent; `null` | `[]` | ACCEPTS — agrees | n/a — member grain, not one of the five |
| 1 | member PRESENT, non-null and NOT A LIST | `:804-809` | `:805` | `"not a list"`; `{a: 1}` | `pin-disposition-malformed` | REFUSES — agrees | n/a — member grain, not one of the five |
| 2 | an ENTRY is not a mapping | `:813-817` | `:814` | `[null]`; `["a"]` | `pin-disposition-malformed` | **ACCEPTS — GAP** | CANON-NAMED — a bare value cannot carry the identity keys `:586-588` names |
| 3 | an entry MISSING any of `DISPOSITION_REQUIRED` — `repo`, `item`, `path`, `finding`, `why`, `cited_to` (`:353-354`), where "missing" is FALSEY and not merely absent (`not entry.get(key)`, `:818`) | `:818-827` | `:820` | `[{}]`; an entry without `cited_to`; `cited_to: []`; `why: ""` | `pin-disposition-malformed` | **ACCEPTS — GAP** | MIXED — CANON-NAMED for `repo`/`item`/`path`/`finding` (`:586-588`) and `cited_to` (`:578`); GUARD-ONLY for `why` (no ratified sentence names a `why:` member) |
| 4 | an entry whose `cited_to` is truthy but NOT A NON-EMPTY LIST | `:828-836` | `:830` | `cited_to: "x"` | `pin-disposition-malformed` | **ACCEPTS — GAP** | CANON-NAMED (`:578`, `:633-636`) |
| 5 | an entry declaring a `level` that is not `None` and, upper-cased, is not in `BLOCKING_LEVELS` (`:366`, exactly `{"ERROR"}`) | `:837-848` | `:843` | `level: "WARNING"`; `level: ""` | `pin-disposition-malformed` | **ACCEPTS — GAP** | GUARD-ONLY — no ratified sentence names `level:` or `BLOCKING_LEVELS` |
| 6 | an entry naming NO AUTHORITY — neither `ratified_by` nor `recorded_by` truthy (`DISPOSITION_AUTHORITY`, `:361`) | `:849-855` | `:850` | entry without either | `pin-disposition-malformed` | **ACCEPTS — GAP** | CANON-NAMED (`:578`) |

**TWO READINGS THE MEASUREMENT CORRECTED, AND THEY MATTER TO A TRANSCRIPTION.**
(i) Row 3 SUBSUMES the falsey half of row 4: `cited_to: []` is refused at `:820`
as *missing* `cited_to`, not at `:830`, because `:818` tests truthiness. A
transcription that ordered these two the other way would name the wrong member
in the finding. (ii) Row 5 is CASE-FOLDED and `None`-guarded, not truthy-guarded:
`level: "error"` is ADMITTED (`str(level).upper()`), while `level: ""` is
REFUSED — an empty string is not `None`. A transcription reading `if level:`
would be NARROWER than the guard on `""`.

**THE GAP, COUNTED.** EIGHT measured records the guard REFUSES and the adapter
`judge(record, "openspec-cli")` ACCEPTS: `[{}]`, `[null]`, `["a"]`, an entry
without `cited_to`, `cited_to: []`, `cited_to: "x"`, `level: "WARNING"`, and an
entry naming no authority. ZERO in the other direction — nothing the adapter
refuses is admitted by the guard. So the adapter is NARROWER than the guard on
the entries and nowhere WIDER, which is exactly the one-directional defect canon
names: *"a resolver that ACCEPTED what the shape's own GUARD REFUSES would … admit a
record the repository's own gate rejects at its first shape check"*.

**AND THE ADAPTER ALREADY REACHES THIS GRAIN FOR THE OTHER OPTIONAL MEMBER.**
The table carries exactly two optional members. Measured side by side:

| optional member | shape | verifier's entry-grain pure refusal | adapter's form | `[{}]` |
| --- | --- | --- | --- | --- |
| `pinned_by_commit_only:` | (a) | non-string or blank entry refused `pin-unreadable` (`scripts/verify-openxwallet-pin.py:449-454`, `scripts/validate-openreposhape-pin.py:493-498`) | `_is_path_only_list` (`pin_shapes.py:151-171`) — `all(_is_text(entry) …)` | **REFUSED** |
| `dispositions:` | (c) | rows 2-6 above (`scripts/validate-openspec-cli-pin.py:813-855`) | `_is_disposition_list` (`pin_shapes.py:217-223`) — `value is None or isinstance(value, list)` | **ACCEPTED** |

So the entry grain is not a new idea this packet introduces into the adapter; it
is the adapter's existing practice for one optional member and its omission for
the other. **Canon already says so for the first one**, in the scenario *A
source pin enumerates its members in two different forms*: *"a
`pinned_by_commit_only:` entry that is a mapping rather than a path string, MUST
… be reported as a malformed member naming the list it came from"*. This
packet's scenario is that sentence's counterpart for shape (c), and is placed
immediately after it for that reason.

**AND THREE OF THE FIVE ENTRY-GRAIN REFUSALS ARE NOT THE VERIFIER'S
INVENTION — THEY ARE RATIFIED CANON, IN A SECOND CAPABILITY; THE OTHER TWO
ARE THE VERIFIER'S OWN PURE GUARD.** `neutral-product-pin`'s requirement *A
dispositioned finding is cited, upgrade-coupled, and refused when stale*
(`openspec/specs/neutral-product-pin/spec.md:577`) obliges the identity keys,
the citation and the authority — rows 2, 4 and 6, and four of row 3's six
keys — in its own words and before this packet:

- `:578`, the requirement's first line — a disposition *"SHALL carry a non-empty
  CITATION to the canon that makes the acceptance lawful and SHALL name the
  authority that granted it; a disposition carrying neither is an UNCITED
  EXCEPTION and the pin is REFUSED rather than the entry being skipped"* (rows 3,
  4 and 6, for `cited_to` and the authority pair).
- `:586-588` — *"A disposition SHALL identify ONE finding — the repository, the
  item, the delta path, and the finding's own text compared whole after
  whitespace normalization"* (row 3's six keys, four of them — `repo`, `item`,
  `path`, `finding` — named outright; a bare value cannot carry them, which is
  why row 2 is canon-named too).
- `:633-636`, the scenario **A disposition carries no citation** — *"WHEN a
  disposition records no `cited_to:`, an empty one, or no granting authority …
  THEN the pin is REFUSED as malformed, before any artifact is fetched … AND the
  entry is not silently skipped"*. It names the member, it names the empty case
  the measurement turned up at row 3, and it states the PURITY — *before any
  artifact is fetched* — that makes the guard transcribable at all.

**THE REMAINING TWO OF ROW 3'S SIX KEYS, AND ALL OF ROW 5, ARE NAMED BY NO
RATIFIED REQUIREMENT — THEY ARE THE VERIFIER'S OWN PURE GUARD.** `:622-624`
requires the RUN'S OUTPUT to *"name every applied exception, its reason, its
citations and its granting authority"* — an obligation on what a run REPORTS
after APPLYING a disposition, not a requirement that the entry itself carry a
`why:` member; no ratified sentence names a `why:` member. And no ratified
sentence names `level:` or `BLOCKING_LEVELS` at all — row 5 is the verifier's
own human-facing convenience, reconciling `ERROR` findings and nothing else.
So `why` (part of row 3) and `level` (row 5) are GUARD-ONLY: reaching them
imposes no obligation BEYOND what `pinned_dispositions` already enforces on
every landed pin — `contracts/openspec-cli-pin.yaml`'s six entries clear both
today, because the CLI itself refuses a record that does not.

So the gap is sharper than the issue states it, for three of the five. The
adapter does not merely admit what one verifier's local choice refuses on
those three: **it resolves a pinned target on a record that a ratified
requirement of this estate says is REFUSED as malformed.** On the other two —
`why` and `level` — the adapter admits what the record's OWN verifier
refuses, and reaching them costs a pin's author nothing beyond what that
verifier already asks of every landed record; it does not follow that
reaching them imposes NO obligation, only that the obligation is not a NEW
one this packet invents. Either way the direction of the remedy is fixed: the
entry grain reaches no member the guard does not already refuse, and the
offline resolver mirroring it is NEVER wider than the guard.

**WHICH IS ALSO WHY THIS PACKET CARRIES NO `neutral-product-pin` DELTA.** Issue
#1045 offers the act as one against `document-lifecycle` "and/or
`neutral-product-pin`". Measured, the second is not owed: that capability's text
is already correct and already complete on this member. What is missing is the
RESOLVER's reading, and the resolver is `document-lifecycle`'s grammar.

---

## D-2 — THIS IS THE OPTIONAL MEMBER'S *FORM*, NOT A NEW REQUIRED MEMBER

**RECOMMENDED (a): change the FORM FUNCTION ONLY; the member stays OPTIONAL.**
`_is_disposition_list` gains rows 2-6; `SHAPE_C.optional` keeps the member and
`SHAPE_C.required` does not gain it.

Four reasons, in order of force.

1. **REQUIRED MEANS REFUSED-WHEN-ABSENT, AND THIS MEMBER IS REFUSED-WHEN-ABSENT
   NOWHERE.** Canon fixes the required set as *"EXACTLY THE TOP-LEVEL MEMBERS
   THAT SHAPE'S IN-TREE PIN VERIFIER REFUSES-WHEN-ABSENT IN ITS PURE,
   SOURCE-FREE SHAPE GUARDS"*. Row 0 of D-1 measures the opposite: absent is
   `[]`. Adding it to the required table would make the adapter WIDER than the
   guard — refusing a shape-(c) record that declares no exception, which the
   verifier admits — and canon fails BOTH directions by name.
2. **IT WOULD FALSIFY A SENTENCE THIS DELTA CARRIES VERBATIM.** Canon says
   *"`dispositions:` is NOT in the set: it is read with an absent-is-empty
   default (`:801-803`)"*, and the nine-member shape-(c) enumeration beside it.
   Option (a) leaves both TRUE — absent-is-empty is a fact about the MEMBER, and
   this delta is about an entry inside a PRESENT one — so the `## MODIFIED`
   block carries every promoted unit unchanged and adds one scenario. A required
   `dispositions:` would rewrite two prose passages and the count, and the
   carriage-ledger self-gate would need a row recording the generalization.
3. **THE TABLE'S MEASURED SPLIT DOES NOT MOVE.** `_tracked_table`
   (`tests/doc-health/test_pin_shape_adapter.py:99`) ranges over
   `shape.required`, and `test_the_table_ranges_over_twenty_nine_member_entries_split_twenty_seven_two`
   pins the result at `(29, 27, 2)`. Option (a) touches neither number; option
   (b) moves both and re-opens the per-shape table in canon.
4. **IT IS THE SHAPE THE ADAPTER ALREADY USES NEXT DOOR** — D-1's second table.

**THE ONE THING THAT DOES CHANGE IN THE TEST: THE OPTIONAL ARM GAINS AN ENTRY
CASE, AND IT IS A *CALL*, NOT A CITATION.** The guard leg ranges over the
required table today for a stated reason — `pin_shapes.py:359-362`: *"each
verifier reads this member with an absent-is-empty default, so there is nothing
for the equivalence test's guard leg to call"*. That reason is exact and it is
about the REFUSED-WHEN-ABSENT question. The PRESENT-AND-MALFORMED question has
something to call, and it is source-free: `pinned_dispositions(record)` takes
the record and nothing else (D-1). So the optional arm can be held to the guard
in the STRONGEST available form — the verifier IMPORTED at its fixed, authored
path and the guard CALLED on a record carrying each malformed entry, asserted to
raise `PinRefusal`, with `ps.judge` asserted to refuse the same record — rather
than by the weaker citation re-read the two `files:` entries use. The adapter
still imports no verifier: the import lives in the TEST, as it already does for
the guard leg.

**ALTERNATIVE (b), PRICED: make `dispositions:` a REQUIRED member of shape (c).**
Cost: WIDER than the guard (reason 1), two canon passages rewritten and a
carriage-ledger row owed (reason 2), `(29, 27, 2)` re-measured (reason 3), and a
guard leg that must assert a refusal the verifier does not make — there is no
`pinned_dispositions` refusal for an absent member to call. **NOT RECOMMENDED.**

---

## D-3 — THE ALTERNATIVES TO ACTING AT ALL

**(a) LEAVE IT AS IT STANDS — the round-8 ruling's own position, and it is not
absurd.** The adapter is necessary-and-not-sufficient by design; a record
carrying `dispositions: [{}]` resolves nothing without a well-formed
`capabilities:` enumeration; every landed record has passed its full verifier.
**Cost:** the adapter stays NARROWER than the guard on precisely the trees it
was built for — a fixture tree, an aggregate run, an arbitrary `--single-repo`
checkout, an added `contracts/evil-pin.yaml` — where no verifier has run; the
asymmetry with `pinned_by_commit_only:` (D-1) stays unexplained in code whose
whole claim is that it is measured; and finding #1045 stays open with no
successor. The ruling itself called this delta *"a legitimate later delta …
noted, not filed"*, so leaving it is a choice to leave that sentence
unanswered rather than a judgement that it was wrong.

**(b) MAKE `dispositions:` REQUIRED** — priced in D-2 as alternative (b).
**NOT RECOMMENDED.**

**(c) RESTATE THE VERIFIER'S ENTRY RULES AS PROSE IN CANON** — spell `repo`,
`item`, `path`, `finding`, `why`, `cited_to`, the authority pair and the level
set into the requirement. **REFUSED, and by canon's own words, for both halves
D-1 splits them into — though the count of existing copies differs.** The
identity keys, `cited_to` and the authority pair are CANON-NAMED already:
`neutral-product-pin:577-636` is one independently-authored list and the
verifier is a second (D-1), so a restatement here would be a THIRD copy nobody
reconciles with the other two — exactly what *"is not restated as PROSE in
this requirement, where a restatement could drift unreviewed"* refuses. `why`
and the level set are GUARD-ONLY — named by no ratified sentence, so the
verifier is their ONLY existing list — and a restatement here would still be
refused, but as the SECOND independently-authored copy of those two, which is
the same hazard *"Of two INDEPENDENTLY-AUTHORED lists the WEAKER is always the
one that admits"* names: the count starts at two, not three. Either way the
scenario names the SOURCE of the form — the shape's own pure guard — and the
equivalence test pins the transcription to it. Of the six
`DISPOSITION_REQUIRED` keys, five — `repo`, `item`, `path`, `finding` and
`cited_to` — appear in `neutral-product-pin`'s normative text as well as in
this design's MEASUREMENT; `why` and the level set appear in the MEASUREMENT
alone, no ratified sentence naming either.

**(d) HAVE THE ADAPTER CALL THE VERIFIER INSTEAD OF TRANSCRIBING IT.**
**REFUSED, constitutionally.** `pin_shapes.py:13-16`: the adapter *"READS THE
RECORD AND NOTHING ELSE. It opens no file, imports no verifier, starts no
subprocess and reaches no network"*, and canon requires the completeness
judgement be reached through a code-fixed route that executes nothing the record
selects. The verifier is imported in ONE place — the equivalence test's guard
leg, at a fixed authored path — and that is where this packet's new case lives.

---

## What this packet does NOT decide

- **It does not decide the finding text or the finding CODE the pass emits.**
  The scenario requires the member AND the entry to be named; the exact
  rendering (`dispositions[2]`, the defect word, the rule string) is the
  realization's, inside the `MISSING`/`MALFORMED` vocabulary the adapter already
  has.
- **It does not touch `neutral-product-pin`, and it does not need to.** That
  capability's ratified text (`:577`, `:578`, `:586-588`, `:633-636`) already
  names the identity keys, the citation and the authority (D-1) and is not
  wrong about any of them; the entry's `why` member and its `level` value
  outside `BLOCKING_LEVELS` are named by no such ratified text and are the
  verifier's own guard, so reaching them imposes no obligation BEYOND what
  that guard already enforces on every landed pin. The defect is in the
  OFFLINE RESOLVER's reading, and the resolver is `document-lifecycle`'s
  grammar — so the delta is there and only there.
- **It does not oblige any pin record to carry or drop `dispositions:`.**
  `contracts/openspec-cli-pin.yaml` is the only record in this tree that carries
  the member (measured over all six `contracts/*-pin.yaml`), its six entries pass
  the guard today, and they pass the proposed form unchanged.
- **It does not reconcile a disposition against a finding.** That needs the
  corpus, is the full verifier's review concern, and stays outside the
  resolver's contract.
