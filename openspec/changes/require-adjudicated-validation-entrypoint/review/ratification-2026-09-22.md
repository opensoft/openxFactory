# Proposal Ratification: require-adjudicated-validation-entrypoint

Status: ratified
Kind: report
Decision date: 2026-09-22
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-22 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-4` (display `openXfactory-4-openDox_extraction`), interactive in
the lane session, verbatim: *"ratify #1140 and #1141"*, given at
**2026-09-22T15:45:54Z** and recorded at `opensoft/openxFactory`
[#656](https://github.com/opensoft/openxFactory/issues/656) comment
[`5779511063`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5779511063).
Ratified baseline: head **`c36ff08c`**, the head the word names, and the head
this packet still stood at when the word was given.

## Decision

**RATIFY.** The requirement stands as it is at `c36ff08c`.

**This ratification authorizes realization; it does not perform it.** Nothing is
promoted by it: `openspec/specs/neutral-product-pin/spec.md` is untouched until
the archive, a separate act on a separate word. `code_surface: none`, so the
archive follows LANDING plus the task list rather than merged-plus-green
realization evidence. **No contract byte moves** — `contracts/openspec-cli-pin.yaml`
is not edited, and neither is `scripts/validate-openspec-cli-pin.py` or its
`reconcile()`. The disposition mechanism works; this packet leans on it.

## 1. The word, and exactly what it decided

> ratify #1140 and #1141

It ratifies TWO packets in one utterance. For this one it ratifies **the GENERAL
rule stated from a PARTICULAR ruling**, which is the only thing this packet adds
and the reason it needed a word of its own:

- **`5778300335`** (2026-09-22T14:26:38Z) is the read-only MEASUREMENT, accepted:
  the enforced gate is the consumer entrypoint, the `add-chain-attestation`
  finding is already dispositioned and cited, and the gate is SUCCESS on every
  pull request.
- **`5778397686`** (2026-09-22T14:33:02Z, by multi-choice) RULED the PARTICULAR
  box: *"§ 8.9 clause (2) READS LITERALLY; the tick becomes `[~]`"*.

**That ruling disposed of ONE box. The defect is a CLASS**, and nothing in the
corpus forbade the next box being written the same way. This packet writes the
rule down; the word ratifies the writing.

## 2. No council sitting was held, and none was owed

**Stated plainly so the record is not read as more than it is.** No convening
packet, no ballot, no seat returns, no council review. A single ADDED requirement
with `code_surface: none`, stated from a ruling given hours earlier, ratified by
the repository owner's direct word in session. The review it received was
mechanical and is recorded at § 4.

## 3. The head did not move between the word and this record

`c36ff08c` is both the head the word names and the head this packet stood at when
the word was given. The ratification front-matter, this record and the README
status line are the first changes after it, and **none of them is requirement
text**.

**The sibling `#1140` is NOT in that position**, and this record names the
difference rather than leaving a reader to assume the two packets were handled
alike: its head moved one second before the word, and moved requirement text, so
re-ratification is registered as owed in ITS record and ITS `tasks.md` § 1.3.
**They are separate acts and this one inherits nothing from that.**

## 4. What stood between proposal and ratification

One Copilot review round, five findings, **all answered and every thread
resolved**. Three were taken as fixes, one was a mechanism finding applied to
both packets, and one was true when written and already false at the head it was
raised against. The one that changed the requirement's meaning:

- **`r4073184083`** — the delta said only a whole-corpus run could be reconciled
  against the dispositions *"at all"*, which **contradicts ratified canon**:
  `openspec/specs/neutral-product-pin/spec.md`:602-604 says a narrowed run SHALL
  still APPLY the dispositions it matches and only may not decide staleness. The
  restriction is now scoped to staleness. **A packet whose whole subject is
  deferring to the disposition mechanism could not afford to misstate it**, which
  is why it was taken as a fix rather than argued.

Two others sharpened the text: `r4073391844` widened the requirement's SUBJECT to
carry every record kind the packet claims, and `r4073391907` corrected *"never
more permissive"*, which was false against this packet's own central measurement.

## 5. What was measured, and by which reader

**The measurement IS the packet**, so it is recorded here in full. Both commands
over one tree, at this packet's own head:

| command | version that answered | verdict | exit |
| --- | --- | --- | ---: |
| `scripts/validate-openspec-cli-pin.py --all --no-cache` | `@fission-ai/openspec@1.12.0`, verified against its recorded content address | `108 passed, 1 failed (109 items)`, the 1 finding DISPOSITIONED and named with its citation and granting authority | **0** |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | **1.13.1** on `PATH` — not the pinned version | same totals, same finding | **1** |

**Same tree. Same finding. Opposite exit.** The finding is
`add-chain-attestation`, carrying `ratified_by: 'Brett Heap, 2026-09-05, "take
exit 2"'`. **It is inherited and is not this packet's.**

Also green at the ratified head: the pinned entrypoint over this change alone
(`1 passed, 0 failed`); `validate-code-surface.py`, `validate-target-release.py`
and `validate-sequenced-after.py` (exit 0 each); and
`scripts/doc-health.py --single-repo .`, which names this packet in **ZERO**
findings.
