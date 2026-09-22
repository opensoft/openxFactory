# Proposal Ratification: amend-neutral-product-pin-source-tree-digest

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
Ratified baseline: head **`ca47e2cb`**, the head the word names.
Current head: **`9f82caeb`**, which is NOT the ratified baseline — see § 3.

## Decision

**RATIFY.** The requirement set stands as it is at `ca47e2cb`.

**This ratification authorizes realization; it does not perform it.** Nothing is
promoted by it: `openspec/specs/neutral-product-pin/spec.md` is untouched until
the archive, which is a separate act on a separate word. `code_surface: none`, so
under `release-realization` that archive follows LANDING plus the task list
rather than merged-plus-green realization evidence. **No contract byte moves with
this ratification** — `contracts/opendox-pin.yaml` and
`contracts/openxdox-pin.yaml` are not edited by the ratified diff, because what
they carry was settled and executed by RULED `5768144952`.

## 1. The word, and exactly what it decided

> ratify #1140 and #1141

It ratifies TWO packets in one utterance and decides nothing about their
CONTENT, which two earlier rulings had already decided:

- **`5777949892`** (2026-09-22T14:04:00Z, by multi-choice, *"(b) — AMEND THE
  CLAUSE"*) commissioned this packet and named its form: *"it becomes its own
  small OpenSpec change against `neutral-product-pin`, citing 5768144952, this
  ruling, and Copilot `r4067623184`."*
- **`5768144952`** (2026-09-21, *"(b) for the pin shape, keep going"*) settled
  what the pin FILES carry; this packet settles only the normative text.

**The word is therefore a ratification of TEXT, not a fresh decision**, and this
record claims nothing more for it.

## 2. No council sitting was held, and none was owed

**Stated plainly so the record is not read as more than it is.** There was no
convening packet, no ballot, no seat returns and no council review. The packet is
a single-requirement wording amendment with `code_surface: none`, commissioned by
a ruling that already named its form, and it was ratified by the repository
owner's direct word in session. The review it did receive was mechanical and is
recorded at § 4.

## 3. THE HEAD MOVED ONE SECOND BEFORE THE WORD, AND THE MOVE WAS NORMATIVE

**This is the one thing about this ratification a later reader must not
discover for themselves.**

| | |
| --- | --- |
| `ca47e2cb` | the head the word names, and the ratified baseline |
| `9f82caeb` | committed **2026-09-22T15:45:53Z** — ONE SECOND before the word — and pushed around it |
| the word | **2026-09-22T15:45:54Z** |

**Brett Heap cannot have read `9f82caeb`**, and it is not a cosmetic commit. It
reverses a NORMATIVE clause that `ca47e2cb` carried: the round-1 repair had
EXCLUDED runtime-clause-governed pins from the equivalence, and `9f82caeb`
removes that exclusion, on a measurement that the exclusion would have made
`contracts/opendox-pin.yaml` — which carries a real `migration:` block at :190
AND a whole-tree digest with no per-file list — **non-conformant**. That is the
opposite of what RULED `5768144952` settled, so the correction runs in the
ratified direction rather than against it.

**It is still requirement text moved after a ratify word, and that is not the
authoring lane's to absorb.** The estate's rule is that only NON-NORMATIVE
corrections may be folded after the word; a requirement or scenario change goes
back for a word. **RE-RATIFICATION AT `9f82caeb` IS REGISTERED AS OWED** —
`tasks.md` § 1.3 — and until it is given, the two heads and their difference are
what this record carries. The house has the instrument for exactly this: a
`Re-ratified:` line beside the `Ratified:` one, as `add-chain-attestation`
carries.

**Nothing was back-dated and no line claims the word covered text it could not
have.** The `Ratified:` lines in `proposal.md`, `design.md` and `tasks.md` all
name `ca47e2cb` explicitly.

## 4. What stood between proposal and ratification

Two Copilot review rounds, ten findings, all answered and every thread resolved.
**Six were taken as fixes, one was registered with its reason, and four were true
when written and already false at the head they were raised against.** The two
that changed the requirement's meaning:

- **`r4073364832`** — the amendment said the two lists *"MAY then be absent"*,
  which left a pin carrying BOTH a whole-tree digest and a `files:` list
  apparently conformant, while `scripts/doc_health/pin_shapes.py`:763-775 already
  refuses that record as MIXED. The text now says such a pin carries NEITHER
  list, and a scenario refuses the mixture.
- **`r4073177274`, then `r4073495698`** — the runtime-scope question, taken twice
  and resolved the second time against the first. `design.md` D3 carries both
  rounds, because the discarded reading is the instructive one.

**One finding is registered rather than fixed** (`r4073110728`, `tasks.md` § 5.3):
the required-check requirement's scenario conditions on the per-file digests,
which a whole-tree pin does not carry. The gap PREDATES this packet — both pins
have carried the whole-tree form since they were filed — and amending a SECOND
requirement is beyond a commission that names one clause.

## 5. What was measured, and by which reader

**Validation ran through the PINNED CONSUMER ENTRYPOINT**,
`python3 scripts/validate-openspec-cli-pin.py`, at `@fission-ai/openspec@1.12.0`
verified against its recorded content address — never the `openspec` on `PATH`,
which at this workstation is `1.13.1`. This packet's sibling `#1141` is the
change that makes that distinction a requirement; this one simply observes it.

- pinned entrypoint, this change alone: **`1 passed, 0 failed`**
- `validate-code-surface.py`, `validate-target-release.py`,
  `validate-sequenced-after.py`: **exit 0** each
- `scripts/doc-health.py --single-repo .`: names this packet in **ZERO**
  findings, and its `## MODIFIED` block raises **no** `modified-block-currency`
  finding while nine other active changes do
- `pytest tests/opendox_pin tests/openxdox_pin`: **105 passed**, over fixtures
  already in the shape this amendment admits

**The corpus-wide `--all` run reads `108 passed, 1 failed (109 items)` and exits
0**, the one failure being the long-lived `add-chain-attestation` disposition
carrying `ratified_by: 'Brett Heap, 2026-09-05, "take exit 2"'`. **It is
inherited and is not this packet's.**
