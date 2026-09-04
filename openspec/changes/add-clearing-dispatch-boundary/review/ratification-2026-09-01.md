# Proposal Ratification: add-clearing-dispatch-boundary

Status: ratified
Decision date: 2026-09-01
Ratifier: Brett Heap (repository owner) — in-session, on the recorded word
Ratified: 2026-09-01 by Brett Heap (repository owner) — in-session, verbatim:
*"merge #192 and ratify #555"*.
Ratified baseline: head `15b14bb3` — "Name the origin record's PR: written and
pushed as xFactory#192, merge pending" — `proposal.md`, `design.md`,
`tasks.md`, `.openspec.yaml`, and `specs/clearing-dispatch-boundary/spec.md`
(TEN ADDED requirements) as they stood at that commit.

## Decision

**RATIFY.** The requirement set stands as it is at the ratified head. Brett's
word carried two acts, executed together and recorded here as one: the
origin record's pull request, `opensoft/xFactory#192`, was **MERGED the same
moment** at `faee7a96ae6e06c15b6c2122947c62356e96f71d`
(2026-09-01T11:47:21Z), and this packet, `opensoft/openxFactory#555`, was
**RATIFIED** at head `15b14bb3`.

**This ratification authorizes realization; it does not perform it.** The
change carries a code surface and `target_release: the next additive minor`,
so it archives only on merged code with green realization evidence. **No
contract byte moves with this ratification**, no number is spent, and
`contracts/` is untouched by the ratified diff.

## The precondition discharged

`tasks.md` §2.3 held ratification gated on the origin record — `Origin:
cpc-clearing-boundary-ruling-2026-09-01.md` — being merged to `main` in
`opensoft/xFactory`, because requirements 8–10 trace to that record's
append-only addendum and a reader could not open their provenance while the
record sat unmerged on a branch. **That gate is discharged by the same act
this record ratifies**: `opensoft/xFactory#192` merged at
`faee7a96ae6e06c15b6c2122947c62356e96f71d`, 2026-09-01T11:47:21Z, putting
`cpc-clearing-boundary-ruling-2026-09-01.md` on `opensoft/xFactory`'s `main`
before the ratifying word was given, not after it.

## Open questions — carried, not re-litigated

Brett's word ratified the packet as drafted, with no further elaboration on
`tasks.md` 2.1's four open questions recorded beyond that. This record states
what "ratified as drafted" means for each rather than inventing a ruling that
was not given:

- **OQ1** (signature requirement for field 10) — carried on `design.md`'s
  stated recommendation: required at the first cross-organization producer,
  expressed against `trust-anchor`'s certificate record. Not yet triggered;
  no cross-organization producer exists today.
- **OQ2** (ledger record vs. transparency-log entry) — carried on the stated
  recommendation: own record kind, referencing a chain.
- **OQ3** (where the grandfather enumeration lives) — already **SETTLED AT
  REALIZATION** per `design.md`, carried here for confirmation only; ratifying
  the text confirms it: the governed data file
  `.github/clearing/grandfather-enumeration.yaml` in `opensoft/xFactory`, read
  by both the L4 guard and the L5 attestation, closed, per-member group
  attribution and allowlist status, and shrink-only.
- **OQ4** (attestation cadence and finding surface) — carried on the stated
  recommendation: ride the existing nightly lane, emit a doc-health-shaped
  finding. Remains open with that recommendation; nothing in the ratified
  text forecloses a different cadence at realization.

None of the four is a blocking condition on this ratification; each is
either already settled or carried on its recorded recommendation, per
`tasks.md` 2.1's own "ruling or carrying" framing.

## What this ratification authorizes

1. **The xFactory realization**, `opensoft/xFactory#191` ("Open the CPC
   clearing door: clearing-dispatch.yml, with readiness-diagnostic as its
   first operation") — `tasks.md` §3. Authorized to merge on its own
   verification bar; this record does not merge it.
2. **The neutral contract bytes**, `contracts/clearing/` at their own
   additive cut, POST-REALIZATION per `tasks.md` §6 — the sealed-bundle
   manifest record, the closed permitted-operations register, the
   `readiness-diagnostic` operation report schema, the dispatch ledger, the
   single-door attestation record, packaged examples, and
   `scripts/validate-clearing-dispatch.py`, registered in
   `contracts/manifest.yaml` and `contracts/CHANGELOG.md`.
3. **The operator's console acts**, `tasks.md` §4 — the one permanent
   allowlist entry per runner group (added after §3 merges, so the path
   being admitted exists), the codexFactory admission's removal from group
   `xfactory-artifact-workers`, and the required-status-check ruleset for
   the L4 guard. These are operator acts recorded as tasks, not committed
   artifacts, and none of them is performed by this record.

## What this ratification does not do

- **It does not move a contract byte.** `contracts/` is untouched by the
  ratified diff; the neutral family realizes post-ratification at its own
  cut.
- **It does not merge `opensoft/openxFactory#555`.** This packet's own pull
  request stays gated on the inherited pytest-suite failure recorded at
  `tasks.md` §9.2 —
  `test_every_carriage_ledger_finding_over_the_real_tree_is_named` failing on
  a subject belonging to the in-flight `add-chain-attestation` lane, which
  reproduces on `origin/main` and is owned by that lane's realization, not
  this packet. Ratification and merge are separate acts; this record performs
  only the former.
- **It does not merge or realize `opensoft/xFactory#191`.** That pull
  request's own verification bar governs its own merge.
- **It does not perform the operator's console acts.** `tasks.md` §4 stays
  open until performed, in the stated order (after §3 lands on `main`).
- **It does not settle OQ1, OQ2, or OQ4 beyond their carried
  recommendations** — see above.

## Next

Realization per `tasks.md` §3 (xFactory workflow, PR #191), §4 (operator
console acts, in order after §3), and §6 (neutral contract cut,
post-ratification). `tasks.md` §9.2's inherited pytest-suite failure governs
when `#555` itself can merge; re-check before merge rather than assuming it
has cleared.
