# Proposal Ratification: decide-disposition-reading-per-family

Status: ratified
Kind: report
Decision date: 2026-09-12
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-12 by Brett Heap (openxFactory operator authority) — given in
lane `openxfactory-1` (display `openXfactory-1`)'s window, verbatim: *"do all
as recomended"*, in answer to the orchestrator's list of FIVE open rulings —
one per class (Q-A through Q-D) plus the packet's own shape (Q-E), each put
with its recommendation first — and recorded on openxFactory PR
[#978](https://github.com/opensoft/openxFactory/pull/978#issuecomment-5646923059)
at **2026-09-12T15:45:25Z** (comment `5646923059`), by the orchestrator
(session `5e1d3c`). **EVERY RECOMMENDATION WAS TAKEN, SO NOT ONE BYTE OF THE
DELTA MOVES.**

This is the ONE citation line `ratified-provenance` counts (the `Ratified:`
line above); everything below is exposition of what it decided, not a second
citation.

## 1. The two words, and what each decided

**THE ORIGIN WORD — given ~2026-09-11T18:20Z, recorded in `.openspec.yaml`
`proposed_by` and in `proposal.md`'s `Proposed:` line.** Brett Heap, verbatim:

> usage reset, resume all. read handoff and resume and fan out wide and do as
> much as possible in parallel

This word COMMISSIONED THE AUTHORING of this packet and decided NONE of the
five rulings below; it admitted no text to canon and is not read as an
approval. It stays recorded as the ORIGIN of the authoring.

**THE RATIFYING WORD — given 2026-09-12, recorded 2026-09-12T15:45:25Z.**
Brett Heap, verbatim:

> do all as recomended

Given in the lane's window in answer to the orchestrator's own list of the
five open rulings this packet's `design.md` D1/D3 and `tasks.md` § 1 carry,
each put as a multiple-choice question with the recommendation stated first,
and recorded on openxFactory PR #978 at 2026-09-12T15:45:25Z (comment
`5646923059`) by the orchestrator (session `5e1d3c`) acting on Brett Heap's
word. **THIS RATIFIES THE PACKET AND TAKES EVERY RECOMMENDED OPTION.**

## 2. What was ratified, class by class

### Q-A — Class A: `modified-block-currency` (4 entries)

**RULED: (A1) NO CHANGE — TAKEN.** Canon's own *A finding is dispositioned*
(`openspec/specs/doc-health/spec.md` line 2177 at `origin/main` `d4d96cca`)
already tells this family what an entry means; re-deciding it here would be a
second rule about the same entries. (A2) narrow it to `info`-with-citation and
(A3) widen it to archived delta paths are NOT taken.

### Q-B — Class B: `location-conformance` (10) + `document-catalog` (1), 11 entries

**RULED: (B1) DELIBERATELY IGNORE — TAKEN.** No family-side reading; the entry
stays a resolution citation and nothing else — the finding these entries cite
is already gone (8 of 11 targets vanished, the other 3 present but drawing no
finding of their family), and a reading arm would have a population of ZERO.
(B2) read and downgrade and (B3) read and suppress are NOT taken.

### Q-C — Class C: `proposal-origin` (8), `record-immutability` (5), `semantic-contradiction` (1), `semantic-normative-prose` (1), 15 entries

**RULED: (C1) DELIBERATELY IGNORE — TAKEN.** No family-side reading; the entry
is a governance record and the finding keeps its band — ten of the fifteen
draw a live finding today (7 `proposal-origin`, 3 `record-immutability`, all
`critical`), and this is the decision the entries were written under. (C2)
read and downgrade to `info` with the citation and (C3) read and suppress are
NOT taken.

**(C4) — THE SPLIT OF `record-immutability`'s FOUR `Status: record` TARGETS
OUT FOR A SEPARATE RULING — IS NOT TAKEN.** The class rules as ONE population
under (C1); the four `record-immutability` targets that are `Status: record`
documents (measured directly, `design.md` D0.2, not inferred from an
archive-path prefix) are ruled with the rest of the class rather than carved
out, and (C4a)/(C4b) (`tasks.md` § 1.3) are never reached or asked.

### Q-D — Class D: `uncited-resolution` (1 entry)

**RULED: (D1a) RECORD THAT IT IS INERT AND LEAVE IT — TAKEN**, in the ruling's
own words:

> the `uncited-resolution` entry; its retirement is an act in
> `opensoft/xFactory`, coupled to #965

(D1b) teach the arm to read its own family's entries and (D1c) retire the
entry in `opensoft/xFactory` are NOT taken. **NO ENTRY IS RETIRED BY THIS
RATIFICATION.** This packet's own D5/Class D measurement (`design.md`) stands
beside the ruling's words rather than being read over by them: openxFactory PR
#981 — issue [#965](https://github.com/opensoft/openxFactory/issues/965)'s own
packet — declines this entry by name and by construction
(`_grandfather_cites` keys on `family="ratified-provenance"` alone, so it
cannot report an `uncited-resolution` entry however the file grows). The
coupling the ruling states is therefore to the SUBJECT — retiring a stale
entry from the aggregation's own disposition file, the kind of act #965 opened
— and not a claim that PR #981's particular arm performs it. If (D1c) is ever
taken on a later word, it still needs a successor named at that ruling; until
then this is unassigned residue and (D1a) leaves it exactly where it is.

### Q-E — the packet's own shape (`design.md` D3, `tasks.md` § 1.5)

**RULED: DECISION ONLY, `code_surface: none` — TAKEN.** Declaring a code
surface now, for a regression test pinning the boundary the two added
scenarios state, is NOT taken. No box in Q-A through Q-D was vetoed toward a
reading arm, so `code_surface` does not change at this ratification:
`code_surface: none` and `target_release: implemented` stand CONFIRMED.

## 3. What this ratification changes in the packet

- `proposal.md`, `design.md`, `tasks.md`: `Status: draft` → `Status: ratified`,
  one citation line each, in the grammar this file's own `Ratified:` line
  states.
- `.openspec.yaml`: `approved_by` / `approved_on` ADDED beside the untouched
  origin block — `kind`, `id`, `reason` and `proposed_by` unmoved, the
  addition-not-rewrite shape `add-drafted-proposal-origin` (issue #318)
  defined.
- `tasks.md` § 1: all six boxes ticked, each naming the option taken and the
  options declined, citing this ruling.
- `tasks.md` § 4: all five boxes ticked **NOT COMMISSIONED** — no class was
  vetoed and (C4) was not taken, so every condition in § 4 failed to occur and
  no arm is built.
- `README.md` "OpenSpec Records": the ACTIVE row moved to the ratified
  grammar, citing this record.
- **NOTHING UNDER `openspec/specs/` MOVES.** The spec delta's own text (two
  added scenarios over *Finding severity and regression handling*) is
  UNCHANGED by this ratification: the mechanism it states was already correct
  for the ruled reading of every class, so ratifying the decision confirms the
  delta's wording rather than rewriting it. Promotion happens at the ARCHIVE,
  a separate act on a separate word; openxFactory #966 closes there.
- `tasks.md` § 5 (verification) and § 6 (archive) are NOT touched by this
  ratification: § 5 is re-run and re-pointed at this ratifying commit's own
  head as its own step (this pull request, after this commit); § 6 stays
  entirely open, to be closed only at the archive.

## 4. What this ratification does NOT do

- It does not promote the delta into `openspec/specs/doc-health/spec.md`.
- It does not archive the packet or close openxFactory #966.
- It does not retire, edit or add any entry in `opensoft/xFactory`'s
  `health/dispositions.yaml`.
- It does not build any arm in `scripts/doc_health/`: `tasks.md` § 4 stays at
  NOT COMMISSIONED throughout, and no line of runtime code is touched by this
  commit.
- It does not re-open or re-litigate any of the eighteen `ratified-provenance`
  entries the parent packet (`honour-grandfather-dispositions-in-ratified-provenance`,
  archived 2026-09-11) already settled.

## 5. Addendum — the separate archive word (recorded at the archive, 2026-09-12)

This ratification (§4 above) explicitly did NOT archive the packet or close
openxFactory #966; § 6 of `tasks.md` states the archive is "a separate act on
a separate word." That word came later, on the archive pull request itself,
after Codex's review (thread `PRRT_kwDOTAvnrs6hyMbj` on PR #1007,
2026-09-12T17:47:21Z) found no such word yet on record: **Brett Heap,
2026-09-12T18:01:30Z, verbatim *"archive it"***, recorded on PR
[#1007](https://github.com/opensoft/openxFactory/pull/1007#issuecomment-5647690592)
and mirrored on issue
[#966](https://github.com/opensoft/openxFactory/issues/966#issuecomment-5647690759).
This line is an ADDITION appended after the archive, not an edit to the
ratification prose above, which stands as it was ratified.
