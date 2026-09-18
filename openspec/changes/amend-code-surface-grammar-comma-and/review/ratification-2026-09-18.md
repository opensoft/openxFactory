# Proposal Ratification: amend-code-surface-grammar-comma-and

Status: ratified
Kind: report
Decision date: 2026-09-18
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-18 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-5` (display `openXfactory-5`), verbatim: *"Amend the text to admit
', and '"*, given in session at approximately **09:55Z** as a TERMINAL
MULTIPLE-CHOICE answer and recorded by that lane as a `RULED` line at
**2026-09-18T10:15:10Z** in the LANE REGISTER, a SEPARATE REPOSITORY and not a
path in this one — [`opensoft/brett-wip@055bea8b:lanes/log/openXfactory-5.md`](https://github.com/opensoft/brett-wip/blob/055bea8b215ad8b46d83cbf1e366c93c23b08897/lanes/log/openXfactory-5.md#L107), line 107 —
with the same recording carried to openxFactory
[#1092](https://github.com/opensoft/openxFactory/issues/1092).

**THE WORD IS A MULTIPLE-CHOICE RULING AND THE CHOICES WERE THE ISSUE'S OWN.**
openxFactory #1092 put two shapes in its own § *Shape of the act*, and no
others: **(a)** amend the requirement text and its scenario to name `, and ` as
a fourth admitted separator, matching what the validator already accepts, or
**(b)** narrow `_SEPARATOR_RE` to drop the `, and ` alternative so the validator
matches the ratified three, at the cost of refusing declarations the corpus
already writes that way. The word takes **(a)**, and takes it in the issue's own
words.

## 1. The word, and exactly what it decided

Brett Heap, 2026-09-18, verbatim:

> Amend the text to admit ', and '

It decides **the direction of the reconciliation** and nothing else, which is
precisely what was asked. Two halves follow from it:

- **The text moves.** The promoted requirement *Code-surface declaration grammar
  is gated* names three list separators where `scripts/code_surface.py:152-157`
  admits four. Canon catches up.
- **The reader does not.** Option (b) is declined, so `_SEPARATOR_RE` keeps all
  four alternatives in their existing order, `, and ` stays tried FIRST, and
  `tests/code_surface/test_code_surface_gate.py:157-160` keeps its five
  parameters. **NO COMMIT OF THIS PACKET EDITS `scripts/code_surface.py`.**

**THE WORD AND ITS RECORDING ARE MINUTES APART, AND BOTH TIMES ARE STATED RATHER
THAN COLLAPSED.** The utterance was given in session at approximately
2026-09-18T09:55Z, in a terminal multiple-choice round put to this lane; it was
recorded as a `RULED` line at 2026-09-18T10:15:10Z, and the lane's `CLAIMED`
comment on #1092 followed twelve seconds later at 10:15:22Z. The approximate
instant is written to the precision the word was taken at and no finer, because
inventing a minute would be inventing evidence; the `RULED` line's timestamp is
exact and is what this record cites. Both instants fall inside the same UTC day,
so `Decision date:`, `approved_on:`, this file's name and every dated line in
the packet are all **2026-09-18**, and there is no boundary to reconcile.

## 2. Why this packet is ratified from its first commit

The ordinary shape in this corpus is a DRAFT packet that a later word ratifies,
and `.openspec.yaml` then gains `approved_by`/`approved_on` as an ADDITION
beside an untouched drafting origin (`add-drafted-proposal-origin`, issue #318).
**THAT SHAPE DOES NOT FIT HERE AND IS NOT FAKED.** The ruling reached the
packet's content before the packet existed: #1092 was filed as a finding with
two candidate remedies and no text, Brett Heap chose the remedy, and the
authoring that followed had nothing left to decide about the direction. There is
therefore no drafting phase to record and no approval to add later.

`proposal.md`, `design.md`, `tasks.md` and this record carry `Status: ratified`
from their first commit, each with exactly ONE citation line — `Ratified:` in
`proposal.md` and here, `Ratified by:` in `design.md` and `tasks.md` — which is
what `ratified-provenance` counts across both sanctioned spellings.
`.openspec.yaml` carries `proposed_by`/`proposed_on` and
`approved_by`/`approved_on` in one act beside a `kind` and an `id` that never
move.

## 3. What the word did NOT decide, and is carried beside it

The word names a direction, not a wording. Two sentences of the delta reach text
the word does not name in so many words, both are MEASURED against the module
rather than designed, and both are declared veto points so that a later word can
strike either without touching the rest:

- **`design.md` D2 — the exclusivity clause's antecedent.** "the two being
  EXCLUSIVE alternatives and never mixed" sits immediately after the separator
  list, which this delta grows from three items to four. Its antecedent is the
  two HEAD FORMS (`none`, or a list) and never the separators — the originating
  packet's own design record says so at
  `openspec/changes/archive/2026-09-16-gate-code-surface-declarations/design.md:631-637`,
  and `parse_head` enforces that pair and nothing else. The delta names the
  antecedent. **Veto cost: four words.**
- **`design.md` D3 — mixed separators.** The reader admits a head that separates
  its members by more than one of the four (`openxFactory, openXwallet and
  codexFactory` parses to three today), and the promoted text never said so
  either way. The delta states it. **Veto cost: one sentence of one added
  paragraph and one `AND` bullet of the added scenario.**

Neither moves a module, a test, a severity, a register or a verdict. Both are
the same species of act as the ruled one: text catching up with a reader that
has behaved this way since it was written.

## 4. What is NOT ratified by this word

**NOTHING IS PROMOTED AND NOTHING IS ARCHIVED.** The landing of this packet
edits no file under `openspec/specs/`, no script, no test, no contract and no
workflow. Promotion of the `## MODIFIED` block into
`openspec/specs/release-realization/spec.md` and the archive of the packet are
ONE later act on a SEPARATE word; `tasks.md` § 4 stays open, and openxFactory
#1092 closes there and not at this landing — which is why the pull request body
carries `Refs` and no closing keyword.

**THE `parse_head` DOCSTRING IS NOT CORRECTED** (`design.md` D4,
`tasks.md` § 5.1). It carries the same three-separator sentence at
`scripts/code_surface.py:447-448`; correcting it would give this packet a code
surface and move its archive behind merged-plus-green realization evidence. It
is named as residue and ticks at the archive act by naming a filed successor, or
on Brett Heap's word that a docstring needs no correction.

**AND THE MERGE IS A SEPARATE WORD AGAIN.** This record is the ratification of
the packet's CONTENT. The landing of the pull request that carries it is the
coordinator's act under the lane-collision protocol's Rule 6 window, never the
author's.
