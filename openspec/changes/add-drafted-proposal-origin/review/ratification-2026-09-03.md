# Proposal Ratification: add-drafted-proposal-origin

Status: ratified
Decision date: 2026-09-03
Ratifier: Brett Heap (repository owner) — in session
Ratified: 2026-09-03 by Brett Heap (repository owner) — in session; record: this
file.
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, the two
spec deltas (`specs/document-lifecycle/spec.md`,
`specs/doc-health/spec.md`), the realization named in `tasks.md` § 2, and the
README's active-changes entry. **Both `## MODIFIED Requirements` blocks were
copied from canon VERBATIM and then edited**, and every promoted scenario TITLE
is carried: four of four for `document-lifecycle`'s "Proposal origin
declaration" (five added), five of five for `doc-health`'s "Proposal-origin
checks enforced by reference" (five added), so
`modified-block-currency`'s gate-bearing arm reads 0 on both. Gates at the
ratification commit, which are the COMMIT'S gates and not `tasks.md` § 5's
archive gate: `OPENSPEC_TELEMETRY=0 openspec validate add-drafted-proposal-origin
--strict` **valid** and `--all --strict` **87 passed / 0 failed**;
`python3 -m pytest tests/doc-health` **1528 passed / 0 failed** (the same
suite reads 1500 at the merge-base, so this change adds 28 items); doc-health
`--single-repo` against
the merge-base `2b0615da`, measured in a clean worktree so the base tree
genuinely lacks this packet — base **6 critical, 6 error, 29 warning, 14 info**,
head **6 critical, 6 error, 29 warning, 16 info**, a movement of **+2 `info` and
nothing else**, both of them this packet's own two MODIFIED blocks in the
carriage ledger.

## The ruling

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER.** Brett Heap, in session on
2026-09-03, verbatim: **"implement your recommendations on all these"**, given
over the lane's written recommendations for openxFactory issues #561/#339,
**#318**, #511, #553 and the #543 fix (b). The resolution for THIS issue is
recorded as the RULING comment on issue #318 and reads, verbatim:

> **Shape 1: a drafted origin kind.** The proposal-origin contract gains an
> origin state that declares provenance without asserting approval (a `drafted`
> kind, or `proposed_on` without `approved_on`), so an unapproved packet is
> expressible and lawful; `approved_on` appears when the approval does, and a
> `Status: ratified` proposal still requires it. Vehicle: an OpenSpec change on
> `doc-health` with a code surface (`scripts/doc_health/proposal_origin.py` +
> fixtures), proposal and realization authored together.

## What the ruling settles, and what it does not

**IT SETTLES THE SHAPE** — shape 1 of the two issue #318 offered, over shape 2
(the draft window keyed on `proposal.md`'s `Status:`) — **AND THE VEHICLE**: one
OpenSpec change with a code surface, proposal and realization authored together,
which is why `tasks.md` groups 1–3 are all discharged on the branch this packet
lands on rather than sequenced behind it.

**IT LEAVES THE ENCODING OPEN, AND SAYS SO IN ITS OWN WORDS**: "a `drafted`
kind, or `proposed_on` without `approved_on`". The authoring session chose the
second and argued it in `design.md` § D1 on a property that decides between
them rather than on taste: `kind` and `id` are fields the SUPPORT MANIFEST
REPEATS, and the `proposal-origin` family reports a manifest/packet
disagreement as post-ratification mutation at `error` with resolution class
`contested`. A `drafted` kind must become `ad_hoc` when the approval lands, so
that encoding writes a contested-class mutation into the happy path of every
packet that gets approved; minting a `:drafted:` id and re-spelling it only
moves the same mutation onto `id`. Under the chosen encoding the identity never
moves and approval is two ADDED lines.

**IT DOES NOT COVER THE SIX DESIGN DECISIONS** taken inside that shape. They are
flagged for veto in `proposal.md` § Orchestrator Decisions, argued in
`design.md`, and reversible on a word: D1 the encoding; D2 where the
ratified-status rule keys (the packet's own declared `Status:`, read through the
single lifecycle-header reader, fired only where the unapproved state is
POSITIVELY declared, and never on the fact of archival); D3 the resolution
classes (`contested` for `unapproved-origin-at-ratification`, mechanical for
`drafting-provenance-incomplete`); D4 one finding rather than two for an origin
declaring no provenance state; D5 the split of the rule between the family and
the `proposal-support.py` gate; D6 the sanctioned writer's new arm.

## What this ratification does NOT do

**REALIZATION IS PERFORMED HERE, BY THE RULING'S OWN NAMING OF THE VEHICLE**,
and this is the `add-release-tag-publication-check` sequencing rather than the
usual one. Canon, the code that enforces it and the tests that pin them cannot
disagree across a merge boundary without reddening the gate that exists to
notice exactly that.

**IT DOES NOT ARCHIVE THE PACKET.** This surface is code, so under
`docs/release-realization-flow.md` § The Archive Gate the packet archives on
MERGED-PLUS-GREEN on `main` and not on landing. `tasks.md` § 5.1 is open.

**IT REPAIRS NO EXISTING FINDING.** Both medx boundary packets were admitted by
ruling on 2026-08-25 and carry complete approval pairs; they are byte-untouched
here. The baseline this change removes is the one the NEXT drafted packet would
have added. Measured: **109** ad-hoc origins in this corpus, all with a complete
approval pair, **0** with neither and **0** with half of one, and
`proposed_by`/`proposed_on` in no packet — so both new finding classes launch
with an **empty population by construction**.

**IT WEAKENS NOTHING ALREADY LAWFUL.** `approved_on` is still required in full
wherever approval is claimed, structurally rather than by test: the approval arm
of the checker is untouched in rule text and action line, and two tests pin
each half of the pair.

## One assertion moved, and it is named here rather than left in a diff

`tests/doc-health/test_modified_block_currency_self_gate.py`'s
`_LEDGER_SUBJECTS` — the EXACT named set of carriage-ledger subjects that family
reports over the real tree, compared with `==` and never `<=` — gains this
packet's two rows, with the per-unit explanation that set's own convention
requires and a retirement condition ("when the packet archives and its blocks
are promoted"). The self-gate FAILED first, by name, naming both subjects: that
is the assertion working. Its `_moved()` history sentence gains this packet's
step (8 → 10). `_PAIRING_SUBJECTS` stays empty — both blocks resolve against
promoted canon, not against an active sibling's addition — and no other
assertion, count or fixture in the suite moved.
