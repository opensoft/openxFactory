# Proposal Ratification: add-neutral-product-standalone-operability

Status: ratified
Kind: report
Decision date: 2026-09-24
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-24 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-4` (display `openXfactory-4-openDox_extraction`), interactive in
the lane session, verbatim: *"ratify #1144, land the follow-ons, (a) on C1–C5"*,
given at **2026-09-24T13:51:09Z** and recorded at `opensoft/openxFactory`
[#656](https://github.com/opensoft/openxFactory/issues/656) comment
[`5815412869`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5815412869).
Ratified baseline: PR #1144's final head **`19237b91`**, which landed on `main` as
squash commit **`94b6f7f1`** (2026-09-24T00:16:25Z) with an identical tree.

## Decision

**RATIFY.** The packet stands as it is at `19237b91`: ONE `## ADDED` block
creating the capability `neutral-product-standalone-operability`, with
**seventeen requirements and seventy-five scenarios**, and `design.md` and
`tasks.md` as they landed.

**This ratification authorizes realization; it does not perform it.** The ruling
record says what it authorizes: the realization of **release 1**, phases 1-3 of
the release map at the head of `tasks.md`. Nothing is promoted by it.
`openspec/specs/` gains no capability until the archive, which is a later,
separate act. `code_surface:` is not `none`, so under `release-realization` that
archive waits for merged, green realization evidence, for BOTH releases (RULED
`5800995035`). Landing release 1 alone archives nothing.

**No code byte, pin, gitlink, contract bundle or release tag moves with this
record.**

## 1. The word, and exactly what it decided

> ratify #1144, land the follow-ons, (a) on C1–C5

The ruling record in comment `5815412869` states four items. **Only item 1 is this
record's subject.**

1. **#1144 is RATIFIED.** The packet moves from `Status: draft` to `ratified`, and
   the ratification record lands as its own pull request under a Rule 6 window.
   The word authorizes realization of release 1, phases 1-3. The realization does
   not happen by the word itself.
2. **The archive follow-ons land when green.** These are the catalog entries for
   `corpus-adapter-seam` and `domain-mapping-declaration`, and the removal of the
   spent `add-composed-view-authoring` disposition row. They are other acts, in
   other pull requests, and none of them edits this packet.
3. **(a) on the banked helper items C1–C5.** These are other acts too.
4. **C6 is not ruled** and stays open.

## 2. The ratification read: nothing is struck

The packet reserved ONE question for the ratification read and said so where a
reader meets it: `proposal.md`, `design.md` § D5 and its "What is still open after
the ruling" paragraph, and `tasks.md` 3.0. The question was whether RULED ASK-2
option (2) (`#656` comment `5628886636`) forecloses requirement 3's default profile
for openDox's OWN domain. If it did, requirement 3 was the one to strike, and the
other sixteen would stand without it.

**The word ratifies #1144 whole and strikes nothing.** Requirement 3 stands with
the other sixteen. An EMPTY default stays refused, as requirement 3 itself says,
so ASK-2's reasoning is untouched. Task 3.0 is ticked on this record.

## 3. What the word authorizes, and what it does not

- **It authorizes** the realization of release 1: phase 1 (the G1/G4 cut, a
  neutral default host profile, and openDox's own default corpus adapter), phase 2
  (the neutral generator) and phase 3 (the install: bundled Postgres, the local
  identity mode, and chat's model configuration).
- **It does not name release 2** (phase 4: merge, publish and the submission
  interface; phase 5: the health engine, the fix loop, exceptions in git and the
  check packs). The ruling record names release 1 alone. Release 2's rulings stay
  recorded and SEQUENCED after release 1, as the release map says.
- **It performs nothing.** No realization, no archive, no promotion and no pin
  move happens by the word or by this record.
- **It moves no declaration.** `code_surface:`, `target_release:` and
  `sequenced_after:` stand as landed, and so does every requirement and scenario.

## 4. The packet did not move between its landing and the word

`94b6f7f1` was `main`'s head when the word was given at 13:51:09Z. The next commit,
#1149 → `dd2466ad` (13:55:40Z, the archive of `add-estate-repository-inventory`),
touched no byte of this packet and not its README entry. This record's branch is
cut from `dd2466ad`.

The changes this record makes are the first after the landing, and **none of them
is requirement or scenario text**:

- **`proposal.md`:**
  - `Status: ratified` with a `Ratified:` citation.
  - A qualifier above the filing's "FILING IS NOT RATIFYING" paragraph, which
    is kept verbatim as the filing's record.
  - A `## Ratification record` section.
  - A read-at-ratification note on the ASK-2 paragraph.
- **`design.md` and `tasks.md`:** `Status: ratified` with a `Ratified by:`
  citation. `design.md` § D5 and its "What is still open" paragraph gain the
  same read-at-ratification note, and `tasks.md` 1.8 and 3.0 are ticked.
- **`.openspec.yaml`:** the approval pair `approved_by` / `approved_on` is ADDED
  after `proposed_on`, never substituted. `kind`, `id`, `reason`, `proposed_by`
  and `proposed_on` do not move.
- **This record.**
- **`README.md`:** the *Active changes* entry's status.

The citation split is the one the lane's own #1140 and #1141 carried: `Ratified:`
on `proposal.md`, and `Ratified by:` on `design.md` and `tasks.md`.

## 5. No council sitting was convened

No convening packet, ballot or seat return exists for this packet. `proposal.md`'s
authoring method records that no alignment review or council debate was run. The
design decisions rest on the archived carve packet's rulings and on the rulings on
`#656` that this packet records. The word is the repository owner's own, given in
session.

## 6. What stood between the proposal and the word

PR #1144 was reviewed round by round before it landed. At its final head
`19237b91`:

- all 122 review threads were resolved;
- Copilot's review at that exact head listed no finding;
- every check run completed green, with Sourcery skipped because the pull
  request exceeded its diff limit;
- `pytest-suite` reported 8440 passed, 6 skipped and 0 failed.

The pull request carries the history. This record freezes only the state that the
word was given over.

## 7. What was measured at this record's commit

The measurement was taken on the tree this record lands in: `main` at `dd2466ad`
plus this record's changes.

| gate | result |
| --- | --- |
| `OPENSPEC_TELEMETRY=0 openspec validate add-neutral-product-standalone-operability --strict` | valid |
| `openspec validate --all --strict` | 110 passed, 1 failed (111 items), the same totals as `main` alone; the one failure is `add-chain-attestation`'s ratified disposition |
| `scripts/validate-openspec-cli-pin.py --all --no-cache` | exit 0, 0 UNDISPOSITIONED failures |
| `scripts/validate-code-surface.py .` and `scripts/validate-target-release.py .` | passed |
| `scripts/validate-sequenced-after.py --ledger-diff` | consistent; this packet's row does not move |
| `scripts/proposal-support.py . verify add-neutral-product-standalone-operability` | ok |
| `scripts/doc-health.py --single-repo .` | names this packet in ZERO findings, and the totals are unchanged from `main` alone |

The running measurement lives in the pull request that carries this record.
