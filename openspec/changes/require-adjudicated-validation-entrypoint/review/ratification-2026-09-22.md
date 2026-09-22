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

**THE TALLY IS STATED AS OF THIS RECORD'S OWN COMMIT AND THE PULL REQUEST CARRIES
THE RUNNING ONE**, because review continued after the ratifying word and a count
frozen into a record is a count that goes stale. As of `691a7dfc`, four rounds
and **EIGHTEEN findings**, all answered and every thread resolved: **16 FIXED**,
and **2 true when written and already false at the head they were raised
against** (`r4073183972`, the `.openspec.yaml` origin, which had landed at
`50ac2fc5`; and `r4073991484`, the scenario count, corrected at `691a7dfc`
before the review naming it was posted).

*(An earlier draft of this paragraph said "one round, five findings". It was true
when written and three rounds have happened since — the same failure mode this
packet's own findings kept catching elsewhere, which is why the count is now
bound to a named head rather than restated.)*

The three that changed the requirement's meaning:

- **`r4073184083`** — the delta said only a whole-corpus run could be reconciled
  against the dispositions *"at all"*, which **contradicts ratified canon**:
  `openspec/specs/neutral-product-pin/spec.md`:663-668 — *"A narrowed run SHALL
  still APPLY the dispositions it matches, and SHALL state that it checked none
  for staleness"* — says a narrowed run still applies them and only may not
  decide staleness. *(The record cited `:602-604` when it was written; the
  merge-from-main that `#1140`'s landing required moved the canon file, and
  `:602-604` now lands on an unrelated scenario. **The POINTER is corrected so it
  still reaches the sentence it always named — the quoted text, not the number,
  is what this record relies on** — and the quotation is carried here so the next
  drift is visible rather than silent. Copilot, PR #1141.)* The
  restriction is now scoped to staleness. **A packet whose whole subject is
  deferring to the disposition mechanism could not afford to misstate it**, which
  is why it was taken as a fix rather than argued.

- **`r4073721220`** — the subject required only the script path plus `--all`, so
  `--path-mode` or an alternate `--pin` **satisfied the letter of the rule while
  resolving the tool from `PATH` or reading a foreign pin** — precisely the
  invocation the capability already forbids a required check to use. It now
  requires the DEFAULT, PINNED-ARTIFACT form. **The flags are part of the name.**
- **`r4073721379`, then `r4073925702`** — the unsatisfiability claim was
  unconditional twice over: first it ignored that a STALE disposition inverts the
  two verdicts, then that an unrelated blocking finding prevents the inversion.
  Both conditions are now in the text, and the second correction forced it to say
  what the requirement is actually about — **WHICH READER a record names, never
  which exit code happens to result.**

Others sharpened the text: `r4073391844` widened the requirement's SUBJECT to
carry every record kind the packet claims; `r4073391907` and `r4073721340`
corrected *"never more permissive"* in the delta and then in the proposal, false
against this packet's own central measurement; `r4073925921` completed a scenario
bullet that stopped mid-clause; `r4073925779`/`r4073925865`/`r4073925957`
corrected a scenario count that lagged the delta; and
`r4073798745`/`r4073798821` corrected two lifecycle claims that ratification
itself made false.

## 5. What was measured, and by which reader

**The measurement IS the packet**, so it is recorded here in full. Both commands
over one tree, **as they read AT THE RATIFIED HEAD `c36ff08c`** — the figures
this record freezes, and it does not update them:

| command | version that answered | verdict | exit |
| --- | --- | --- | ---: |
| `scripts/validate-openspec-cli-pin.py --all --no-cache` | `@fission-ai/openspec@1.12.0`, verified against its recorded content address | `108 passed, 1 failed (109 items)`, the 1 finding DISPOSITIONED and named with its citation and granting authority | **0** |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | **1.13.1** on `PATH` — not the pinned version | same totals, same finding | **1** |

**Same tree. Same finding. Opposite exit.** The finding is
`add-chain-attestation`, carrying `ratified_by: 'Brett Heap, 2026-09-05, "take
exit 2"'`. **It is inherited and is not this packet's.**

**A LATER RE-TAKE DOES NOT AMEND THIS TABLE, and this is the reason it names a
head.** After `#1140` landed as `e90997bc`, this branch took the merge-from-main
that the shared README Records block required, and the same two commands at the
merged head `925d146b` read `110 passed, 1 failed (111 items)` — **the same
single finding and the same opposite exits**, with the item count higher only
because `origin/main`'s corpus grew in between. The figures above are what the
ratifying word was given and they stay as given; the RUNNING measurement lives
in the pull request and in `tasks.md` § 3.1, which is the same division `#1140`
adopted after a frozen tally went stale there (Copilot, PR #1141).

Also green at the ratified head: the pinned entrypoint over this change alone
(`1 passed, 0 failed`); `validate-code-surface.py`, `validate-target-release.py`
and `validate-sequenced-after.py` (exit 0 each); and
`scripts/doc-health.py --single-repo .`, which names this packet in **ZERO**
findings.
