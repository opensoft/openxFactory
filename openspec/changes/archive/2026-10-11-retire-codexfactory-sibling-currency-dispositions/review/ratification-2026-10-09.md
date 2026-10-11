# Ratification: retire-codexfactory-sibling-currency-dispositions

Status: ratified
Kind: report
Decision date: 2026-10-09
Ratifier: Brett Heap (openxFactory convener)
Ratified: 2026-10-09 by Brett Heap (openxFactory convener) — "Ratify + land when green (Recommended)", 2026-10-09T21:00:16.594Z, first-hand, a multiple-choice selection in lane codeXfactory-1's own session, given over head ed0c67adde1c35bd1b1c1b6472246957f9263a7f; recorded at https://github.com/opensoft/openxFactory/pull/1288#issuecomment-6089181718 and on the estate's lane register, opensoft/brett-wip commit 78488f6c0c944ba92ae3818f8ececd40236b6333, lanes/log/codeXfactory-1.md, RULED 2026-10-09T21:01:42Z on openxFactory #1286

## Decision

**RATIFIED by Brett Heap, AS DRAFTED.** This packet (`proposal.md`,
`design.md`, `tasks.md`, the `.openspec.yaml` declaration and this record) is
ratified as it stands over head `ed0c67ad`. Each of its four open questions
lands at the default it states and stays **FLAGGED rather than resolved**.

**The same answer carries the LANDING WORD, as its own component**: *"land when
green"*. **THE MERGE IS NOT DONE BY THIS RECORD.** The pull request stays DRAFT
at this encoding. It leaves DRAFT and lands under lane-collision Rule 6, read
green on the head it lands, on the coordinator's act and not the authoring
seat's.

---

## The word

Brett Heap answered first-hand, in lane `codeXfactory-1`'s own session
(session `2b17a476-c057-4a49-abbf-dadbc5529729`), as a **selection in a
multiple-choice round**. The answer carries the session transcript's own
timestamp, **2026-10-09T21:00:16.594Z**. The minute is taken from the
transcript, not from a later clock read.

The question put to him, verbatim (asked at 2026-10-09T20:56:43.188Z):

> openxFactory #1288 (G-1) deletes the two codexFactory sibling dispositions,
> with its tests. It's safe to land first, and is the prerequisite for #549's
> second advance carrying 7.3. What should happen with it?

The three options offered, verbatim, with the one chosen marked:

| option | offered as | |
| --- | --- | --- |
| **"Ratify + land when green (Recommended)"** | "Ratify and land it in openxFactory under Rule 6 when green. That unblocks 7.3's second advance, which must then re-derive both siblings in one codexFactory PR." | **CHOSEN** |
| "Ratify only" | "Record the ratification, and land it later on its own word." | not taken |
| "Hold" | "Leave it as a DRAFT." | not taken |

**WHERE IT IS RECORDED.**

* On the pull request itself:
  [PR #1288, comment 6089181718](https://github.com/opensoft/openxFactory/pull/1288#issuecomment-6089181718),
  posted 2026-10-09T21:00:58Z, *"WORD, recorded before any act"*. It quotes the
  option label and its offered meaning.
* On the estate's lane register (lane-collision protocol Rule 4): `opensoft/brett-wip`
  commit `78488f6c0c944ba92ae3818f8ececd40236b6333` (committed
  2026-10-09T21:01:43Z), file `lanes/log/codeXfactory-1.md`, whose RULED line
  reads: *"RULED — lane codeXfactory-1, session
  2b17a476-c057-4a49-abbf-dadbc5529729@Eagle, 2026-10-09T21:01:42Z,
  lane:codeXfactory-1 → opensoft/openxFactory#1286 — Ratify + land when green
  (Recommended), first-hand 2026-10-09T21:00:16Z: openxFactory PR #1288, the G-1
  disposition deletion"*.

**THE HEAD IS NAMED, NOT INFERRED.** The word was given over
`ed0c67adde1c35bd1b1c1b6472246957f9263a7f`, the only head PR #1288 had carried.
That head was committed at 20:55:13Z. The pull request was opened DRAFT over it
at 20:55:30Z, and the question was put at 20:56:43Z. That is why this
ratification is a **SECOND commit on the same branch** and not a rewrite of the
first: the packet was genuinely `draft` when written and pushed, and is
genuinely `ratified` from the commit that records the word.

**IT IS BARE AS TO THIS TEXT.** The option names no amendment, and it rules
none of `design.md` § 7's open questions. A bare word ratifies what is in front
of it and resolves nothing it does not name.

**IT IS NOT THE DRAFTING WORD, WHICH STILL STANDS FOR WHAT IT COVERED.**
*"This lane drafts it (Recommended)"*, 2026-10-09T17:35:29Z, recorded on
codeXfactory/codexFactory#549 (comment 6086047985), authorized the draft only.
It is held in `.openspec.yaml` `origin.proposed_by` / `proposed_on`, kept as
authored. This word is ADDED as `origin.approved_by` / `approved_on` and does
not replace the drafting pair.

**IT IS THE DELETION'S AUTHORITY.** The template's record says *"A human word is
what ADDS an exception; the tool is what removes one."* Here no tool has
refused either entry on any tree codexFactory reads, so the two deletions in
`contracts/openspec-cli-pin.yaml` rest on this word (`design.md` § 1).

---

## RATIFIED AS DRAFTED

Every position this packet states is ratified as it stands. Each stated open
question lands at the default the packet recommends and stays **FLAGGED rather
than resolved**:

| disclosed item | where | lands at | status |
| --- | --- | --- | --- |
| OQ-1: `CANON_MOVED` with no member | `design.md` § 7, `tasks.md` 2.3 | **kept**, with its `DISPOSITION_CLASS_CITATION` row and the pin header's class declaration | default, flagged |
| OQ-2: the template's `tasks.md` 6.3 | `design.md` § 7, `tasks.md` 5.2 | **left unedited** here; ticking or annotating it is that packet's own act | default, flagged |
| OQ-3: land on ratification, or hold for G-2 | `design.md` § 7, `tasks.md` 0.3 | **land on its own landing word, after ratification**; the same answer gives that word as *"land when green"* | default; landing word GIVEN, landing act NOT taken |
| OQ-4: `CITED_ACTIVE_PACKETS` | `design.md` §§ 6–7 | **left as it is** | default, flagged |
| the deletion goes ahead of the re-derivations | `design.md` § 1 | stands as written | ratified as stated |
| no spec delta, declared | `.openspec.yaml` `skip_specs: true`, `design.md` § 3 | stands as written | ratified as stated |
| three test files move: 5 → 3, 5 → 3, floor 4 → 3 | `design.md` § 4 | stands as written | ratified as stated |
| THE HARD CONSTRAINT: after **D** lands, codexFactory does not advance its declared openxFactory pin to D or later without both re-derivations in the same pull request | `proposal.md` § Impact | stands as written | ratified as stated |
| codexFactory #549's second advance, with both re-derivations under their own owner words | `tasks.md` 5.1 | lane `codeXfactory-1`'s act in codexFactory | **open** |
| the watch on `Fission-AI/OpenSpec#1793` | `tasks.md` 5.3 | unchanged by this packet | **open** |
| this packet's archive | `tasks.md` 5.4 | merged plus green realization evidence, on its own word | **open** |

**Nothing in `tasks.md` is ticked by this word.** Its `[OWNER]` boxes 0.2 and
0.3 stay `[ ]`, each with a dated note beneath it: an agent does not tick an
owner's-act box.

---

## The landing word, and what it does not do

*"land when green"* is the separate landing word that OQ-3's default and
`tasks.md` 0.3 wait for. *"Ratify only"*, the option that would have withheld
it, was not taken. Its condition is **GREEN, read on the head that lands**.
That head is not `ed0c67ad`, because this ratification commit and a merge of
openxFactory `main` follow it. Leaving DRAFT, posting `LANDING` / `LANDED` on
the pull request and in the register, and the merge are the coordinator's acts
under Rule 6. The merge commit is **D** in `proposal.md` § Impact.

---

## Read at this encoding

* PR #1288 was OPEN and DRAFT, head `ed0c67ad`. Its fourteen checks on that head
  read `pass` at this encoding (`gh pr checks 1288`): SonarCloud Code Analysis,
  clearing-dispatch-gate, council-convening-gate, doc-health-py314,
  former-id-arrival-gate, lane-line, merge-master-approval, openreposhape-pin,
  openspec-cli-pin, openxdox-consumer-gate, pytest-suite, release-tag-gate,
  signed-execution-chain-gate and wallet-validation. That is a reading of the
  word's head. It is not the landing's green, which is read on the head that
  lands.
