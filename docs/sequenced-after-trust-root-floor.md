# The `sequenced_after` Parent-Declaration Surface Is a Never-Clearable Trust-Root Floor

Status: ratified
Ratified by: add-sequenced-after-substrate
Kind: reference
Owner: openxFactory (the `release-realization` capability and the
`sequenced_after` substrate — `openspec/specs/release-realization/spec.md`,
`scripts/sequenced_after.py`, `scripts/validate-sequenced-after.py`,
`scripts/frontmatter_strict.py`).
Realizes: the "Trust-root integrity of the parent declaration",
"Parent-declaration retention at archive" and "Chain-walk policy belongs to the
consumer, and its bound SHALL be measured" requirements ADDED by
`add-sequenced-after-substrate` (ratified 2026-09-01 by convener ruling, as
authored). Sibling record:
[The `scope_globs` Scope Surface Is a Never-Clearable Trust-Root Floor](scope-globs-trust-root-floor.md).

This is **doctrine text realized as a record and an openxFactory-side check**
(add-sequenced-after-substrate task 5.3). It states the trust-root property the
`sequenced_after` substrate must hold in every repository that enables a gate
consuming the ordered-delta chain. The mechanical ENFORCEMENT of the floor lives
in each enrolled repository's own merge-approval envelope and provenance-tie
verifier; this document records the requirement and the assertion openxFactory
can make about its own substrate.

## The requirement

The `openspec/changes/` surface carries the machine-readable ordered-delta parent
declaration (`sequenced_after:`) that a chain-consuming gate walks to decide
whether a fully governed pull request may clear. That makes it a **trust-root
source** — and a chain walk is only as trustworthy as the links it follows. For
the chain it feeds to be trustworthy, the surface must hold four properties:

1. **Base-read.** A consumer reads `sequenced_after` only from the BASE BRANCH of
   an enrolled repository, never from a pull-request head. A pull request can
   therefore never present the check that authorizes it with a chain of its own
   choosing — it cannot shorten its chain, re-point it at a friendlier parent, or
   promote itself to a root on its own head.

2. **Ratification-covered.** The declaration's bytes live in `proposal.md` front
   matter, are part of the ratified change artifact, and are covered by that
   change's ratification. A chain cannot be re-shaped post-ratification, and
   `sequenced_after: []` is a POSITIVE ROOT CLAIM a human ratified rather than a
   formatting artifact.

3. **Non-author-mutable.** The `openspec/changes/` surface that carries the
   declaration **SHALL be a never-clearable floor member of EVERY repository
   enrolled for an autonomous-merge axis that consumes it**, and **no autonomous
   merge SHALL write to it**. This closes the self-authorization recursion in
   which an earlier autonomous merge could author the chain a later decision
   corroborates against.

4. **Frozen after ratification.** Mutation of `sequenced_after` after
   ratification is rejected at the archive gate (the "Parent-declaration
   retention at archive" requirement, realized by
   `sequenced_after.retention_at_archive` and
   `scripts/validate-sequenced-after.py --archive-gate`). Absence, an explicit
   `[]` and a null value are kept THREE DISTINGUISHABLE FACTS in the freeze's
   canonical form, so a change cannot promote itself to a declared root between
   ratification and archive — which under any narrowing composition would be a
   widening.

A repository that cannot floor the declaration-carrying surface **within its own
tree-validated floor** SHALL NOT enable a chain-consuming gate for any non-docs
class: a trust-root source the autonomous path could write breaks property 3.

## Absence is fail-closed, and root status is proved

A consumer **SHALL NOT infer root status from the ABSENCE of the field**, and
SHALL NOT treat an explicit `sequenced_after: []` as sufficient on its own where
a mechanical cross-check can contradict it. The alternative reading is a
fail-OPEN default that every future consumer would otherwise rediscover: before
the field is adopted no change carries it, so "absence is the root" makes every
chain read as a depth-one root and silently authorizes on the terminal change's
own declarations, with the refusal it was supposed to raise UNREACHABLE. After
adoption the same reading makes declaration author-opt-in and, under any
narrowing composition, PENALIZES honest declaration and REWARDS omission. A
control that rewards omission is not a control.

Root status is established by EITHER an explicit `[]` covered by ratification OR
a mechanical CO-MODIFIER CROSS-CHECK finding no other change declaring a delta on
the same requirements — and where neither holds, a consumer REFUSES under a named
identifier. **The cross-check is the consumer's to implement**, because its key
is a per-repository corpus fact (the promoted
`openspec/specs/<capability-id>/spec.md` a delta's requirement titles resolve
against), and a consumer SHALL keep it IN FORCE after adopting the field, so `[]`
plus a detected co-modifier still refuses.

## What openxFactory asserts, and what it does not

openxFactory owns and can assert:

- The **freeze** — `scripts/validate-sequenced-after.py --archive-gate` rejects a
  post-ratification mutation of the declaration, root promotion included
  (property 4).
- The **policy-free validator** —
  `scripts/validate-sequenced-after.py` conforms a present declaration to the
  shape, the repository-qualified reference grammar, the resolvability of every
  bare entry over both anchored corpus locations, and ACYCLICITY, with **no depth
  ceiling, no fan-out cap and no composition operator** of its own.
- The **one strict loader** — `scripts/frontmatter_strict.py` reads both
  structured fields of the realization-axis block and REFUSES duplicate keys at
  any level, anchors, aliases, merge keys, non-UTF-8 bytes, YAML directives, more
  than one document, and a block over the 65,536-byte ceiling, so the neutral
  validator and the consuming verifier cannot disagree about what the same bytes
  mean.
- That **archival does not rewrite declarations** — no date-prefixing, no
  re-pointing, no normalization of entries on archival, so a chain's declared
  shape at ratification is the shape it still has years later.

openxFactory does **not** enforce, and each enrolled repository MUST, in its own
`.github/merge-approval-envelope.yml` and provenance-tie verifier:

- Make `openspec/changes/` a never-clearable floor member of the enrolled surface
  (property 3, enforcement half).
- Base-read the declaration and PARK any autonomous candidate that would itself
  write a `sequenced_after` declaration (properties 1 and 3).
- Implement and keep in force the CO-MODIFIER CROSS-CHECK that proves root
  status, and refuse under a named identifier where neither proof holds.
- Refuse a QUALIFIED FOREIGN entry under a named identifier rather than SKIP it —
  skipping would fabricate a root out of a declaration that says the opposite.

These enrolled-repository obligations are the consumer's realization, built
against a current checkout of the consuming repository and tracked under
`realize-provenance-gated-autonomous-merge` — NOT under
`add-sequenced-after-substrate`, whose surface is the neutral substrate alone.

## The walk policy is the gate's, and its bound must be measured

The substrate declares **no depth ceiling, no fan-out cap and no scope- or
authority-composition operator**. Those are AUTHORIZATION POLICY of the gate that
acts on a chain: they differ between gates, and a number fixed in the neutral
field would bind repositories that never adopt any such gate while drifting from
the one gate that enforces it. A consuming gate SHALL declare its own **as
operative numbers in its own specification**.

The first consumer's values are cited here **as the first instance, not adopted
as neutral doctrine**: codexFactory's provenance-tie verifier walks at most
**FOUR hops inclusive of the terminal change** and composes the authorized scope
by **INTERSECTION**, refusing a fork, a cycle and an over-deep chain under its
own named identifiers. Those numbers live in that gate's specification, where
they are enforced and can be measured. **Raising any gate's ceiling is a
specification change with a recorded disposition — never an operational
adjustment made at the point a candidate refuses.**

### The measured bound: first post-adoption reading, 2026-09-01

Re-run this reading with
`python3 scripts/validate-sequenced-after.py . --sweep`. It is a DATED
measurement, not a currency obligation: the numbers move as the corpus grows, and
the sweep — not this paragraph — is the authority.

**Where the PER-CHANGE reading lives.** The table below is the whole-corpus
reading at one date. What the sweep reads about EACH change — its corpus, its
co-modified/sole class, its declaration, its resolved chain depth and its legacy
prose header — is carried one row per change id in
`tests/sequenced_after/corpus-ledger.yaml`, and every total the sweep reports is
DERIVED from those rows rather than pinned as a literal
(`add-per-change-sweep-ledger`, proposed 2026-09-03 on openxFactory issue #618,
`Status: draft`). `--ledger-diff` checks the rows against the live corpus and
names any that are stale; `--seed-ledger --moved-by '#<PR>'` rewrites them,
stamping only the rows that actually moved. **A verification or record file
cites its own change's row and the ledger's consistency with the corpus at a
named commit — never a corpus-wide total**, a total being a number that moves
whenever anybody else lands.

| measure | reading |
| --- | --- |
| change ids (31 active + 122 archived) | **153 change ids** |
| co-modified at requirement granularity (each would owe a declaration) | 104 |
| sole modifiers (each would declare `sequenced_after: []`) | 49 |
| ACTIVE changes: co-modified / sole | 19 / 12 |
| declaring `sequenced_after:` | 1 (`add-sequenced-after-substrate`) |
| declaring an explicit `[]` root claim | 0 |
| prose `Sequenced-after:` headers (all archived) | 3 |
| **deepest declared chain resolved** | **1 hop** |

**Later reading, not an edit to the dated table above.** As at
`add-per-change-sweep-ledger` (proposed 2026-09-03, `Status: draft`) the deepest
resolvable declared chain is **2 hops**, from `add-per-change-sweep-ledger` to
`add-sequenced-after-substrate` to `add-structured-scope-substrate`. The table
stays as the 2026-09-01 first-post-adoption measurement it is; re-run the sweep
for the current reading, which is derived from the per-change ledger.

The **deepest declared chain it resolves is 1 hop**, from
`add-sequenced-after-substrate` to `add-structured-scope-substrate` — the
substrate's own first instance. At authoring time, one day earlier, the field
existed in no corpus and the deepest chain anywhere was **zero hops BY
CONSTRUCTION**.

**A ONE-HOP READING IS STILL ZERO EVIDENCE ABOUT ANY GATE'S CEILING.** No honest
chain has yet approached the first consumer's four-hop bound, so that bound
remains an UNMEASURED one: it has never refused a real chain and has never been
shown sufficient for one. This is recorded as such rather than allowed to read as
a validated number. The corpus reality the sweep also measures is what makes the
question live rather than academic: **104 of 153 changes are co-modified at
requirement granularity** — real ordered deltas that would each owe a
declaration — so the chain shape is the NORMAL shape in this corpus, not an edge
case, and the depth a real adoption produces is a fact to be MEASURED as
adoption proceeds, by re-running the sweep.
