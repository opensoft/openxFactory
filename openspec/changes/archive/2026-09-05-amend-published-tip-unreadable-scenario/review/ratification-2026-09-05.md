# Proposal Ratification: amend-published-tip-unreadable-scenario

Status: record
Kind: report
Decision date: 2026-09-05
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-05 by Brett Heap (openxFactory operator authority) —
in-session, verbatim: *"ratify 678, use openxfactory-1, land it when green"*,
given after a presentation that carried `design.md` **D1** as the packet's veto
point and § Lane spelling as an open question. **D1 was not vetoed.**
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/doc-health/spec.md` (**ONE MODIFIED requirement**, *"Release-tag
publication"*, restated in full with all 30 promoted scenarios, **ONE canon unit
replaced** and that unit declared by a reserved `Removed from canon by` marker)
— together with `README.md` and `tests/sequenced_after/corpus-ledger.yaml`, with
`openspec validate amend-published-tip-unreadable-scenario --strict` and
`--all --strict` green and the verification run captured beside this file at
`verification-2026-09-05.md`.

**This record is CAPTURED AT MERGE, not at first push, and it was RE-DERIVED
PRE-CAPTURE.** `record-immutability` forbids editing a `Status: record` document
AFTER capture; capture is the merge of the pull request that establishes it, and
nothing is merged yet. Every number in `verification-2026-09-05.md` was
re-derived on the tree this record sits in. A commit cannot write its own hash
into its own tree, so the ratification commit is named by its subject and its
position on the branch rather than by a hash.

## 1. What was ratified, and what it says

**ONE requirement is MODIFIED and none is added.** `doc-health`'s promoted
*Release-tag publication* is restated in full — every body unit and all 30
promoted scenario titles — and exactly one scenario changes, *The manifest
cannot be read at the published tip*:

- its `WHEN` bullet is **REPLACED**, from naming one cause as commonest to
  naming **both facts** the single empty answer stands for;
- an `AND` is **ADDED** requiring that the family have **established which of
  the two holds** before choosing its words — asking presence, and attempting
  one bounded fetch where the commit is absent — *rather than naming a cause it
  did not check*;
- a second `AND` is **ADDED** saying that where the commit IS present and
  carries no manifest, the skip must say THAT and state the presence, because a
  tip the checkout holds is an ANSWER rather than a read that failed.

The promoted `THEN` and the closing `verify_tag` / #338 clause are carried
**byte-identical**. No file is added under `openspec/specs/`, so **no
codexFactory floor advance** is owed.

## 2. Why the packet exists, in one measurement

The promoted `WHEN` told its reader that the commonest cause of an empty
manifest read is *"a checkout that has not fetched that commit"*. **The
measurement ran the other way.** openxFactory **#612**: on the aggregation
nightly the commit **WAS** fetched — the workflow's own *"Fetch each governed
submodule's live origin/main"* step had put all ten published tips in the store
— and **nine of the ten governed repositories simply carry no
`contracts/manifest.yaml` at all**. Every night those nine were reported in the
words of an unfetched checkout, sending anyone reading the report to hunt a
fetch defect the workflow had already ruled out.

**PR #646 (`2177b2a2`, 2026-09-04) fixed the family**: `obtain_commit` asks
whether the commit is present and attempts one bounded fetch of exactly that
commit where it is not, and the two outcomes carry two different skips. **This
packet is canon catching up with the checker**, and it changes no behaviour.

## 3. The decision ratified knowingly

### D1 — the establishing obligation is written on the `WHEN` side

*"The family MUST establish which one holds before choosing its words"* is an
obligation, and a scenario has two sides for one. **Written as a `THEN` it is
circular**: the scenario's trigger is *the read answered nothing*, both of its
outcomes depend on which fact holds, and a `THEN` saying "establish which holds"
would place the establishing AFTER the branch it decides. So it is a `WHEN`-side
`AND`: the scenario applies to a family that HAS already asked presence and
attempted its one bounded fetch, which is exactly the code's order —
`obtain_commit` runs before the two `manifest is None` arms, and the arms are
gated on `tip_present` rather than asserting it.

**The cost was put to the ratifier with the decision**, and is restated here so
ratification cannot be read as unaware of it: a `WHEN`-side obligation is weaker
as a compliance hook, because a family that never established anything does not
*violate* the scenario, it simply never enters it. The mechanical alternative —
move the bullet below the `THEN` and reword it as a `MUST` — was named in
`tasks.md` 1.2 and is kept in `design.md` D1 so the cost of reversing the
decision sits beside it.

**Ratified as designed.** The remedy was NOT taken.

## 4. The second thing the word settled: the lane id

The same word says **_"use openxfactory-1"_**, and it settles a real collision
this packet surfaced rather than papered over.

The lane was renamed on 2026-09-05 and circulated in session as
**`openXfactory-1`**, with a capital X. **The ratified `lane-line` check cannot
express that**: `.github/workflows/lane-line.yml` requires a pull request body to
open with `Lane: <name>` matching `^Lane: [a-z0-9-]+( \(.*\))?$`, lowercase only,
and every other lane id in this corpus is lowercase. The capitalised spelling
**failed that required check** on this packet's first push (run `33970709751`),
and Copilot independently flagged the casing from the corpus side as splitting
one lane's history across two spellings.

**The canonical id is therefore the lowercase `openxfactory-1`** — the spelling
the grammar can express and the one this packet already wrote — and
`openXfactory-1` is a display form, not a second lane. **`lane-line.yml` is NOT
amended.** Weakening a required gate so a name fits is a governed change, not a
side effect of an unrelated prose amendment, and this packet neither proposed
nor made it.

## 5. Independent review, recorded including its absence

- **Codex: REFUSED.** Requested once on this pull request; the connector replied
  with its usage-limit message. **No Codex round ran** — the fifth such refusal
  across this arc (#668, #672, #678).
- **Sourcery:** the private-repo upsell stub.
- **Copilot: two rounds, and the first was right.** Round 1 (on head
  `060e1f37`) reported that `tasks.md` 3.6 was ticked while
  `tests/sequenced_after/corpus-ledger.yaml` carried no row for this change —
  the tick had preceded the fact. Fixed by `3fdcd95b`. It also flagged the lane
  casing against corpus precedent, independently of the `lane-line` failure;
  that is `cd71ff12`. **Round 2 on the fixed head: 🟢 Approval recommended,
  0 new comments.**

## 6. The marker, and the probe that proves it is doing the work

Replacing a bullet DROPS a canon unit, so unlike `add-release-tag-gate` — whose
`## MODIFIED` block only ADDED and therefore owed no marker — this block carries
the reserved form:

```
**Removed from canon by amend-published-tip-unreadable-scenario (2026-09-05):**
``<the old WHEN bullet, verbatim>`` — <reason>
```

`modified-block-currency` names this change **zero** times as authored, which
alone cannot be distinguished from a block the family never read. So it was
probed **both ways**, and both fired:

- **marker removed** → *"does not carry **1** of the 214 body units and scenario
  bullets"* — so exactly ONE unit is dropped, and the marker is what declares
  it;
- **a promoted scenario title mutated** → *"omits 1 of the **30** scenarios …
  'The published tag is lightweight rather than annotated'"*;
- **restored** → silent again.

## 7. A false claim in the ratified text, corrected before landing

**The ratified `proposal.md` carried one factually wrong sentence and it is
corrected rather than left standing.** Its § *What this proposal does NOT claim*
said the sibling scenario *The changelog cannot be read at the published tip*
"carries no equivalent misnamed cause". It does:
`openspec/specs/doc-health/spec.md:2788` carries the SAME clause word for word,
over `contracts/CHANGELOG.md` instead of the manifest.

**How it was found, and why that matters here.** A REHEARSAL of the archive act
— run on a throwaway worktree before the real one, asserting among other things
that the retired clause no longer appears in canon after promotion — reported
that it still did, and the surviving site was the sibling. The error was the
authoring session's: it searched for the manifest phrasing rather than for the
clause, and found one of its two sites.

**The DELTA is untouched and the SCOPE is unchanged.** Issue #662 asks about the
manifest scenario; the ratified delta amends that scenario and no other.
Widening a ratified packet after the word that ratified it is not a correction,
it is a different change. What is corrected is the packet's own PROSE about the
corpus, which was wrong; the sibling is recorded as an **owed successor** in
§ 8, with the one reading it owes before the wording is copied across.

## 8. What lands, and what is still owed

**Lands with this ratification:** the delta, the README row and the ledger row.

**Still owed, and not by this word:**

1. **The sibling scenario** *The changelog cannot be read at the published tip*
   (§ 7) carries the identical misnamed cause and needs the same one-line
   amendment plus its marker. It owes one reading first: the changelog read has
   no presence probe of its own — it inherits the manifest read's — so whether
   the "established which holds" wording transfers unchanged is a question that
   packet must answer rather than assume.
2. **The archive act.** `code_surface: none`
means this change archives **ON LANDING** under `release-realization` — there is
no realization to wait for, because the realization is what this amendment is
catching up to — so the archive is a separate pull request opened after #678
merges, promoting the MODIFIED requirement into `openspec/specs/doc-health/spec.md`
with its marker and closing issue #662.
