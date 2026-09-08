# Proposal Ratification: add-chain-anchoring (tranche three)

Status: ratified
Decision date: 2026-08-30
Ratifier: Brett Heap (repository owner) — in session
Ratified: 2026-08-30 by Brett Heap (repository owner) — in session
Ratified baseline: this change as committed in the ratification commit carrying
this record (`proposal.md`, `design.md`, `tasks.md`,
`specs/chain-anchoring/spec.md` — NINE ADDED requirements over 89 scenarios, no
`## MODIFIED Requirements` block anywhere), validated `--strict` and
`--all --strict`, doc-health zero-new, `pytest-suite` green.

## The ruling

**Six items, ruled in one act on 2026-08-30, verbatim:**

> **"1 yes, 2 yes with note, 3 merge, 4a, 5 bless, 6a."**

| # | Item | Ruled |
|---|---|---|
| 1 | — | **yes** |
| **2** | **Ratification of `add-chain-anchoring`** | **YES, WITH NOTE** — this record, and the note is §"The note" below |
| 3 | Merge | **merge** — performed by the orchestrator, NOT by this record |
| **4** | The frozen sitting-bundle headers | **4a** — normalization; performed as his act, §"Ruling 4a" |
| **5** | LS-A9's out-of-disposition execution | **bless** — §"Ruling 5" |
| **6** | The timing model | **6a** — consolidation; performed BEFORE ratification, §"Ruling 6a" |

**RATIFY tranche three of the staged topic `signed-execution-chain`** — the
neutral public anchoring layer and the permissioned consent plane, as the new
`chain-anchoring` capability. **Ratification authorizes REALIZATION and performs
none of it.** No contract byte moves here; `target_release` remains deliberately
unnumbered and is allocated at realization by merge order.

## THE NOTE — what "yes with note" attaches to, stated where nobody can miss it

**A TAIL OF THIS PACKET HAS BEEN REVIEWED BY NO BOT.** The §7.4 council judged
`cf5a24b8`. Nine bot rounds then followed the fix round, and the last review that
actually ran read **`0b550d2d`**. Everything from **`fd7c1ca7`** onward is
**unreviewed by any automated reviewer**:

* round nine's three discharges — the skew band that replaced a false
  upper-bound inference, the lower-bound delay proof with its
  *never-proves-compliance* clause, and the closure rule that ended the
  unbound-field family;
* the tripwire bookkeeping;
* **and this entire closing set — the ruling-6a consolidation included.**

**The cause is QUOTA EXHAUSTION, NOT SILENCE.** The reviewing bot returned *"You
have reached your Codex usage limits for code reviews"* rather than a verdict. A
refusal to review is not a clean review, and this record does not let the two
read alike. The state was disclosed head-by-head on the pull request before the
ruling, so **Brett ratified with this tail in view rather than in ignorance of
it** — on the recorded prescribed-fix principle: a defect found later in that
tail is a prescribed fix against ratified text, not a reopening of the
ratification.

**What partially offsets it, stated without overclaiming.** The consolidation
that landed in that tail is **restructure-with-proof** and changed semantics
nowhere, and its proof is the scenario set — nine rounds of accumulated
adversarial knowledge, every clock-relevant scenario satisfied and none
overturned. That is evidence about the consolidation and about nothing else in
the tail.

## Ruling 6a — the consolidation, performed BEFORE this ratification

The timing model had accreted across **eighteen normative paragraphs in two
requirements over four rounds**, and **three consecutive rounds found DIRECTION
ERRORS** in it. It is now ONE delimited section of the receipt requirement — the
three clocks, every bound as an explicit inequality with its direction, every
width with its citation, the three decisions and their shared one-directional
margin, a closed table of what each verifier mode may and may not conclude, and
the closure rule — with every other timing paragraph reduced to a reference.

**Performed on Brett's word, NOT on the tripwire this session had armed.** That
tripwire was defined to fire on a further clock-area defect from a tenth bot
round; the tenth round never ran, so it never fired. **A ruling and an automatic
trigger are different authorities and the record keeps them apart.** Design
rationale: `design.md` **D11** (unify-don't-patch at design scale); realization
mirror: `tasks.md` §5.2. Nine requirements and 89 scenarios, both unchanged.

## Ruling 4a — the frozen headers, normalized as the record owner's act

The four carried sitting records wrote `Status: record — <elaboration>` on one
line, which the `status-validity` family reads as a free-form status. This
session **declined to fix them** while they were the convener's bytes: the
disposition rules the packet and ballot unedited and requires itself carried
byte-identically in #510's bundle, so a unilateral edit would have manufactured
the drift that rule exists to prevent.

**Ruling 4a is that act, made by the record's owner.** The transformation is
deterministic and content-preserving — the header line becomes two lines,
`Status: record` followed by `Record scope: <elaboration verbatim>` — and
**nothing else in any file changes**. The identical transformation lands on
#510's branch under the same ruling, so the disposition stays byte-identical
across both bundles. Post-normalization
`sha256(disposition-2026-08-30.md)` = `71fae769bd6f8e41c87b2e3618367f741b552c7d16fc5f1b2172067f540699f0`.

**Effect:** doc-health is now **zero-new outright**, not merely zero-new over
authored bytes.

## Ruling 5 — LS-A9 blessed

A fix round executed **LS-A9**, a seat amendment the convener had left
**undisposed** (disposition §6 leaves the should-fix schedule open item by item).
This session escalated it rather than executing it, then executed it on the
coordinating session's direction, and recorded both facts with a revert one
commit away.

**Brett's blessing converts that execution into HIS ACT.** The amendment stands
as ruled rather than as tolerated, and the revert path closes. **The sequence is
not rewritten** — escalated, then executed on direction, then blessed — because a
blessing settles authority and does not edit history.

## What this ratification does NOT do

* **It performs no realization.** The contract family, its refusing validator and
  the operator infrastructure in `tasks.md` §4 are a later commission.
* **It does not dispose the remaining SHOULD-FIX set.** LA-A7, LS-A7, LS-A8,
  LQ-A10, LQ-A11, LQ-A12, LQ-A14 and CPL-A5 remain open and undisposed;
  disposition §6 governs them and this record does not reach them.
* **It does not merge.** Ruling 3 authorizes the merge and the orchestrator
  performs it.
* **It settles nothing about #510 or #509**, whose own rounds and records are
  theirs.

## Evidence at ratification

| Gate | Result |
|---|---|
| `openspec validate add-chain-anchoring --strict` | green |
| `openspec validate --all --strict` | 79 passed, 0 failed |
| Structure | 9 ADDED requirements, 89 scenarios, no `## MODIFIED` block |
| doc-health vs `origin/main`, matched baseline basename | **zero-new** |
| `pytest-suite` | **pass** |
| Sitting bundle vs the sitting's own bytes | identical apart from ruling 4a's header normalization |
| Council record | `council-review-2026-08-30.md` |
| Disposition of record | `disposition-2026-08-30.md` |
