# Clarify — 032-govern-archived-record-edits (round 1)

**Feature**: `032-govern-archived-record-edits`
**Branch head at authoring**: see the report; base `main` `68712924`
**Answered by**: the ARCHITECT SEAT (lane `opsXfactory-1`). Answers are written
back into this file inline and applied to `spec.md`.
**Status**: awaiting answers

Ten questions. Q1, Q2 and Q10 are the ones that change what gets written; the
rest fix placement and evidence. Each carries the measurement that raised it.

---

## Q1 — Which of the 28 boxes does this realization tick?

The packet's own preamble says every box stays unticked "while the packet is a
proposal", and the ratification record repeats it: "No task is ticked. 28 of 28
remain open, § 1's ratification boxes included". Realization has now begun, and
the corpus practice for an ARCHIVED change is the opposite — the six most recent
archived openxFactory changes carry 28/0, 28/1, 21/0, 39/0, 40/0 and 26/0
ticked/unticked, and the single unticked box in that sample carries an explicit
"NOT OWED HERE" note.

Four groups are in question:

- **0.1** — the ledger `moved_by` re-stamp. Its own text says "PERFORMED
  2026-09-08" and the row on `main` reads `moved_by: "#788"`. Tick?
- **1.1–1.5** `[OPERATOR]` — ratification. Given 2026-09-08; the three vetoes
  were put verbatim and none exercised; 1.5's record exists. Ticking these is a
  claim about **Brett Heap's** acts, written by an agent.
- **2.1–2.3** — the three requirement blocks, authored and ratified.
- **5.1** — the README Records row, on `main` since #788.

**Options.** (a) Tick ONLY what this branch performs (3.4, 4.1–4.5) and leave
everything else unticked with dated notes. (b) Tick every box whose act is
verifiably done, `[OPERATOR]` boxes included, each with a dated note citing the
record. (c) (b) but leave the `[OPERATOR]` boxes for Brett Heap to tick himself.

**Cost.** (a) leaves an archived packet whose record reads as never begun. (b)
has an agent tick an operator's boxes. (c) leaves 5 boxes needing a human act
before archive.

---

## Q2 — Where in `docs/document-lifecycle.md` does the neutral minimum go, and how much of the route does it state?

Task 3.4: "Record the minimum in `docs/document-lifecycle.md` beside the
`Status:` / `Ratified by:` header rules, as a form the lifecycle header block
accepts." The document's § *Status Claim Rules* (line 55) is a bullet list; the
`govern-openspec-corpus-membership` precedent added a top-level bullet plus
nested sub-bullets there and cited itself inline.

**Q2a — placement.** (a) a new top-level bullet at the end of § *Status Claim
Rules*, with sub-bullets, in the precedent's shape; (b) a new `###` subsection
under § *Status Claim Rules*; (c) a new top-level `## Editing an Archived
Record` section.

**Q2b — reach.** (i) the NOTE FORM only — the dated line, where it goes, and
that a local convention may add to it and may not fall below it; (ii) the note
form PLUS the two sentences that make it non-self-authorizing — the ruling is
recorded before the edit, and the note says what changed and never that it may;
(iii) the whole route, including the by-effect bookkeeping class and the
refusal of everything else.

**Constraint that bears on it.** The § *Explicit Delta Rule* in the same
document makes unmarked restatement of promoted policy a defect, and this
delta is ratified but NOT yet promoted (promotion happens at the archive act).
The more of the route the document states, the more of it is standing on a
citation to an active change rather than on canon.

---

## Q3 — What citation does the adopted passage carry, given the delta is ratified but not promoted?

`docs/document-lifecycle.md` is `Status: standard`. Its own rules sanction two
spellings, and the precedent bullet in the same section reads "Ratified by
`govern-openspec-corpus-membership` (2026-08-23)" — written on the realization
branch BEFORE that change archived (doc edit `7157fa3e`, archive `01ff3434`).

**Options.** (a) mirror the precedent exactly: "Ratified by
`govern-archived-record-edits` (2026-09-08)"; (b) the same plus a phrase saying
the requirement reaches canon at the archive act; (c) an `xspec:` marker instead
of prose citation; (d) something else you name.

---

## Q4 — Where does the § 4 gate evidence live?

The packet has no `evidence/` directory. `supporting-docs/`, `source-snapshots/`
and `evidence/` segments are EXCLUDED from doc-health's lifecycle scan set, so an
`evidence/` file needs no lifecycle header; a `review/` file DOES (it is a
governance document under the very requirement this packet modifies).

**Options.** (a) evidence lives only in `specs/032-*/` (the Speckit tree, which
doc-health does not scan) and in the PR body; (b) also
`openspec/changes/govern-archived-record-edits/evidence/realization-2026-09-08.md`;
(c) also a `review/` record with a `Status: record` header.

---

## Q5 — What shape do the dated notes take in `tasks.md`?

**Options.** (a) a dated note appended under EACH box; (b) one consolidated dated
block at the head of §§ 3, 5 and 6 covering the boxes that stay unticked, with
per-box notes only where a box is ticked; (c) per-box notes for ticked boxes and
a single "NOT OWED HERE" line per unticked box, in the
`2026-09-05-mirror-floor-addition-grace` precedent's shape.

---

## Q6 — Is task 4.2 (MODIFIED-block currency) ticked here or left for the archive act?

The rule demands currency CONTINUOUSLY until archive, and 4.2's own text says
"Re-run the byte-identity check … before archive". Measured at this branch's
base, canon has NOT moved since ratification (`git log 3504287a..68712924 --
openspec/specs/document-lifecycle` is empty).

**Options.** (a) re-run and tick here, with the measurement recorded, and let the
archive act re-run it as its own precondition; (b) run and record here but leave
the box for the archive act.

---

## Q7 — Do the notes on `[OpsxFactory]` boxes cite the twin's PR number?

The twin is OpsxFactory `govern-archived-record-edits`, PR #279, ratified,
realized by a sibling orchestrator. Task 3.1 says the cross-citations are
"re-checked to resolve once both heads settle".

**Options.** (a) notes name the repository and change id only, no PR number
(a number can move, and this branch cannot verify the twin's merge); (b) notes
cite PR #279 as the twin's landing vehicle at this date; (c) notes cite the
twin's merge sha if it has landed by the time this branch's last commit is
written.

---

## Q8 — Where is the pinned-target measurement recorded?

The second ADDED requirement obliges a change that edits a pinned target to
re-derive dependent pins. Measured: **no in-repo content-address pin names
`docs/document-lifecycle.md`** — `contracts/manifest.yaml` carries zero
`docs/`-prefixed path values, and no yaml/yml/json in the repository pairs a
`sha256` with that path. So the obligation does not attach to this feature's
own edit, and this packet is the first change in the estate that could say so.

**Options.** (a) record it in the feature's evidence artifact only; (b) also as a
dated note in `tasks.md` beside § 4; (c) not recorded — an obligation that does
not attach needs no record.

---

## Q9 — Does the feature's own Speckit tree get committed?

Precedent 030 and 031 commit `specs/NNN-*/` (spec, plan, tasks, research,
checklists, quickstart, evidence). doc-health does not scan root `specs/`.

**Options.** (a) commit the full Speckit tree as 030/031 do; (b) commit only
`spec.md`, `plan.md`, `tasks.md` and the checklists; (c) keep the Speckit tree
out of the commit entirely.

---

## Q10 — May this branch write any packet file other than `tasks.md`?

`proposal.md`, `design.md`, `.openspec.yaml` and the spec delta are the RATIFIED
text. Task 3.1 nevertheless contemplates re-checking cross-citations "once both
heads settle", which would be an edit to ratified prose in `proposal.md` or
`design.md` (legal — the packet is not archived — but it is an edit to text
approved as written).

**Options.** (a) `tasks.md` only; every other packet file is frozen until
archive; (b) `tasks.md` plus a purely additive dated realization note in
`proposal.md`; (c) `tasks.md` plus cross-citation resolution in `proposal.md` /
`design.md` if the twin has landed.

---

**Answering.** Reply with the option letter per question (e.g. `Q1: b`), or
prose where none fits. Everything else in the plan is already determined by the
packet and by the measurements in `spec.md` § *Measured baseline*.
