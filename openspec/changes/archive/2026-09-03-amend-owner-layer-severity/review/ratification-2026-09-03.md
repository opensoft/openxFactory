# Proposal Ratification: amend-owner-layer-severity

Status: ratified
Decision date: 2026-09-03
Ratifier: Brett Heap (openxFactory repository owner) — in-session, recorded
VERBATIM as the latest comment on openxFactory issues #561 and #339
Ratified: 2026-09-03 by Brett Heap (repository owner) — in-session; record:
this file.
Ratified baseline: this change as committed in the commit carrying this
record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, this record,
and the TWO spec deltas
`specs/workflow-gate-contract/spec.md` (one `## MODIFIED Requirements` block,
one scenario) and `specs/release-surface-integrity/spec.md` (one block, four
scenarios). **THE DELTA TEXT IS BYTE-UNCHANGED FROM WHAT THE RULING AUTHORIZED**,
because the ruling was given on a WRITTEN RECOMMENDATION rather than on a tip:
no requirement text existed when it was given, and the recommendation named the
disposition and the vehicle, not a diff. What that means for this record is
stated in § *What the ruling authorized, and what it did not*.
Gates at the ratification commit:
`OPENSPEC_TELEMETRY=0 openspec validate amend-owner-layer-severity --strict`
VALID, and `--all --strict` **87 passed / 0 failed** (86 at the `origin/main`
baseline, this change being the one item added);
`python3 scripts/proposal-support.py . verify amend-owner-layer-severity` ok;
`python3 -m pytest tests/doc-health` and `python3 -m pytest tests/sequenced_after`
green with the two live corpus pins moved.

## Decision

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER**, over two
`## MODIFIED Requirements` blocks — `workflow-gate-contract`'s *"Owner layer
constraint"* (one scenario, canon's) and `release-surface-integrity`'s *"The
declared bundle describes the release surface"* (four scenarios, all canon's).

**Ratification here IS the whole change.** `code_surface: none`: there is no
realization slice to authorize, no code to merge, no bundle to cut and no
green run to wait for. What remains after this act is promotion and archive,
which is `tasks.md` § 6 and is the landing act rather than a separate release.

## The ruling, verbatim, and where it is recorded

Brett Heap, 2026-09-03, in session, over the lane's written recommendations for
issues #561/#339, #318, #511, #553 and the #543 fix (b) taken together:

> **"implement your recommendations on all these"**

It is recorded VERBATIM as the latest comment on **openxFactory issue #561**
and again on **openxFactory issue #339**, each comment resolving the general
word to that issue's own subject. On #561:

> **Canon moves to ERROR.** The validator's fall-through stays `rpt.error`;
> `workflow-gate-contract` "Owner layer constraint" is amended to say an
> unresolvable `owner_layer` is reported as a validator ERROR. Basis: the
> 2026-09-02 measurement above (0 unresolvable tokens across the five
> consumers), so no consumer is refused and no phasing is owed. Vehicle: one
> doc-only OpenSpec change (`code_surface: none`), which also carries #339's
> sentence.

On #339:

> **Fold into #561's packet.** The `release-surface-integrity` illustration
> naming `contract-v1.33`/`v1.35`/`v1.39` as untagged is past-tensed and dated
> (the treatment PR #333 gave the same claim in `release_inventory.py`), as a
> second delta in the same doc-only change that amends the owner-layer severity
> for #561.

**The recommendation he ruled on was not a bare preference.** It carried the
measurement issue #561's own item 2 demanded — zero unresolvable `owner_layer`
tokens across codexFactory, MedxFactory, LedgerxFactory, OpsxFactory and
AdxFactory at `96b2b968`, table reproduced in `design.md` — and it named the
alternative with its cost: relaxing the validator to `warning` would loosen a
conformance gate nobody asked to loosen. The alternative was put and declined.

## The chain of authority, as SEPARATE ACTS

Recorded as a chain because no act in it authorizes what the next one does.

1. **The divergence was RECORDED, not discovered here.**
   `retire-hermes-flat-keys-and-openworkflow-tokens` (ratified 2026-09-01, PR
   #551) met it while retiring the `openworkflow`-prefixed token branch, wrote
   it up as its **D4**, and deliberately did NOT resolve it — *"resolving it
   moves EVERY unresolvable `owner_layer` token in every domain repository at
   whatever severity is ruled, a strictly larger subject than a four-line
   retirement, and one that packet had no measurement to support."* Its
   `tasks.md` § 6.1 commissioned the issue so the record would outlive that
   packet's fate. **That act authorized a record, not a disposition.**
2. **The FILING of issue #339**, on the same principle one issue earlier: a
   promoted spec is amended only through an OpenSpec change, the defect is one
   sentence, and the issue is the discoverable queue for whoever next opens a
   delta against that capability. It named the treatment (PR #333's dating) and
   authorized nobody to apply it.
3. **The MEASUREMENT of 2026-09-02**, posted to #561 as item 2 of what the
   issue said a disposition owes. It settled that either direction is free. It
   ruled nothing, and its author said so in terms: *"Not claiming the packet
   until the ruling lands."*
4. **THE RULING of 2026-09-03**, quoted above, recorded on both issues.
5. **THIS RATIFICATION**, over the baseline named above.

**Act 1 does not authorize act 4, and act 4 does not perform act 5.** Each is
written down where it happened.

## What the ruling authorized, and what it did not

**AUTHORIZED**: the DISPOSITION (canon moves to `error`, #339's paragraph is
past-tensed and dated) and the VEHICLE (one doc-only change carrying both).

**NOT AUTHORIZED, and not claimed**:

1. **No edit to `scripts/validate-domain-factory.py`.** The ruling is that
   canon comes to the code; editing the code would perform the opposite. Not
   one line moves, and `design.md` § *THE VALIDATOR DOES NOT CHANGE* says so
   with the line quoted.
2. **No deprecation, no window, no refusal-list row and no bundle.** Nothing
   under `contracts/` moves. The measured population the severity rise would
   refuse is EMPTY, so no phasing is owed, and this change is deliberately not
   routed through `contract-deprecation-execution`.
3. **No reopening of #551's Executed row**, which states the fall-through's
   severity as *"whatever the general rule carries"* precisely so this change
   could move the general rule without touching it. It is not touched.
4. **No edit to the `contract-v1.33` / `v1.35` / `v1.39` release records.**
   `contracts/CHANGELOG.md`, `contracts/manifest.yaml` and the
   `contracts/releases/` inventories are the record of what was declared and
   are not rewritten to match a later world; the stale ILLUSTRATION is
   corrected where the illustration lives.
5. **No promotion and no archive by this act.** `tasks.md` § 6 is owed at
   landing, and its boxes are deliberately unticked on an unmerged branch.
6. **No disposition of OpsxFactory's three unrelated validator errors**,
   surfaced by the measurement and recorded in `design.md` only so the
   measurement is honest.

## Fidelity to canon, verified mechanically

Both blocks were **BUILT FROM CANON** by extraction and substitution rather
than retyped, which is what makes "two words and one paragraph" a measured
claim:

| requirement | canon block sha256 | delta block sha256 | word-diff |
| --- | --- | --- | --- |
| Owner layer constraint | `abe58572…77118237` | `035fb896…bc4ed439` | `validator warning.` -> `validator error.`; `MUST report a warning identifying` -> `MUST report an error identifying`. Nothing else |
| The declared bundle describes the release surface | `4c9e0b71…313f29567` | `6e102b2e…d02a1d19a` | one paragraph past-tensed and dated; four lines out, six in. Nothing else |

**Scenario completeness — the arm `modified-block-currency` gates at `error` —
reads ZERO**: canon's 1 scenario title under *Owner layer constraint* and its 4
under *The declared bundle describes the release surface* are all present, by
title, in canon's order.

## What this packet MOVES, measured

**Two new `info` findings and nothing else at any severity, WHILE THE PACKET
STOOD ACTIVE — and none at all on the landed tree.** Both are this packet's own
carriage-ledger rows, and both name exactly the units the word-diffs above
name:

* `workflow-gate-contract` — 2 of 3 units: the body clause and the scenario's
  `**THEN**` bullet. The `**WHEN**` bullet is byte-identical.
* `release-surface-integrity` — 1 of 23 units: the tag-is-not-the-reference
  paragraph. The other 22, including all four scenarios, are byte-identical.

The arm cannot distinguish a ruled amendment from stale text and does not claim
to; the rows ARE the audit trail. Both were named in
`tests/doc-health/test_modified_block_currency_self_gate.py` with dated notes,
and both RETIRED IN THIS SAME COMMIT on the condition they were written with —
the packet archived and its blocks promoted — with both halves verified before
the rows were deleted. **On the landed tree the two finding sets are
IDENTICAL**: 55 lines each, `6 critical / 6 error / 29 warning / 14 info` on
the branch and on the `origin/main` baseline alike, zero new at any severity
and zero lost.

**No `sibling-pairing` finding is possible**: both requirement titles are
promoted canon rather than an active sibling's `## ADDED` block, so this packet
owes no `Modified over` marker and carries none.

**Two live corpus pins move as BOOKKEEPING, not as a code surface**, each in
this change's own commit with a dated note, which is those pins' own protocol —
and the proposal's `code_surface: none` names them rather than leaving them to
a diff. `tests/sequenced_after/test_sweep.py`: `co_modified` 109 -> 111,
`active_co_modified` 21 -> 22, `change_ids - 1` 157 -> 158,
`sole_modifiers - 1` 48 -> 47, `active_sole - 1` HELD at 11 with the hold
asserted. Measured on both trees and BY EXCLUSION.
`tests/doc-health/test_modified_block_currency_self_gate.py`: the two rows
above, added and retired in the one commit — the population 8 -> 10 -> 8, both
halves recorded rather than netted, because a reader who sees only the net
cannot tell an archived packet from one that was never authored. The
`sequenced_after` pin moved twice for the same reason: `active_co_modified`
21 -> 22 on the authoring and 22 -> 21 on the archive, while `co_modified`
HELD at 111 (an archive never un-shares a requirement key), `change_ids - 1`
held at 158 and `sole_modifiers - 1` at 47.

## Next — nothing, and that is the point of `code_surface: none`

Promotion and archive (`tasks.md` § 6) were PERFORMED in the landing commit
that carries this record, through
`python3 scripts/proposal-support.py . archive amend-owner-layer-severity --yes`
and never a bare `openspec archive`, the shape
`2026-08-25-reconcile-lifecycle-books-count` set for a doc-only packet. Both
blocks promoted byte-identical to the delta bodies under the hashes in
§ *Fidelity to canon*, `promotion-fidelity` reads zero over the landed tree,
and no realization evidence stands owed. Adversarial review ran on the pull
request and is recorded there.
