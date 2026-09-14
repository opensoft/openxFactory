# Proposal Ratification: encode-wallet-authority-rulings-r6-r12

Status: ratified
Kind: report
Decision date: 2026-09-12
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-12T23:58Z by Brett Heap (openxFactory operator authority),
verbatim: *"accept all A on 1017"* — given as a MULTIPLE-CHOICE ruling over
all nine decisions `proposal.md` § Open questions and `design.md` D-1 through
D-9 put for the owner, given in session directly to the ENCODE seat of lane
`hermes-wallet-exercise` (window `hermes-wallet-exercise`, session
`codeXfactory-2`, workstation Eagle) and recorded in full here.
**THE WORD TAKES THE RECOMMENDATION ON EVERY ONE OF THE NINE: OQ-1 = (a),
OQ-2 = (a), OQ-3 = (a), OQ-4 = (a), OQ-5 = (a), OQ-6 = (a), OQ-7 = (a),
OQ-8 = (a), OQ-9 = (a).** Each is the option the packet already encoded, so
**THE DELTA'S WORDING STANDS UNCHANGED AND NOTHING WAS SUBSTITUTED, RESTORED
OR DELETED.**

## 1. The word, and what it reaches

**"accept all A on 1017" IS A SINGLE MULTIPLE-CHOICE RULING OVER NINE
DECISIONS, NOT NINE SEPARATE WORDS.** It was given at 2026-09-12T23:58Z and is
recorded verbatim, with that instant, on every document this ratification
touches — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`
(`approved_by`/`approved_on`, added beside the unmoved `proposed_by`/
`proposed_on` pair the `add-drafted-proposal-origin` (issue #318) shape
defined), the README OpenSpec Records entry, and this record.

**THE RATIFICATION IS APPLIED BY LEAVING THE TEXT ALONE, AND THAT IS VERIFIED
BY DIFF RATHER THAN ASSERTED.** `git diff --stat -- openspec/changes/encode-wallet-authority-rulings-r6-r12/specs/`
between the pre-ratification head (`2374d9ed`, the merge of `origin/main`
`dcf797a6` this branch carried into the encode) and the ratification commit is
**empty (0 files)** — the seven `## ADDED` requirements and their twenty-five
scenarios are ratified exactly as the packet was authored and as PR #1017's
review was drafted against.

## 2. The nine decisions, as put and as ruled

| OQ | `design.md` | Put | Ruled | Considered, not adopted |
| --- | --- | --- | --- | --- |
| **OQ-1** | D-1 | Home capability for R6–R12 | **(a) — `review-authority-intake`, `## ADDED`**, forced rather than preferred: no promoted spec exists and both authoring changes are ACTIVE | (b) a new `holder-composition` capability — splits the register's grammar across two specifications; (c) split R6/R7 into `signed-execution-chain` — would MODIFY shipped canon to carry a subject it does not compute |
| **OQ-2** | D-2 | How R7 is satisfied | **(a) — adopt `xfc-jcs-sha256-1` BY REFERENCE**, widening `digest_subject` by one member (`holder_composition`) | (b) a second JCS profile — two profiles free to drift; (c) leave the profile abstract, naming none — reproduces the defect the promoted requirement exists to close |
| **OQ-3** | D-3 | Digest agility / dual-digest transition | **(a) — NO agility mechanism minted now**; algorithm tagging plus a recorded profile name and version is what makes a later migration readable | (b) declare an agility register now; (c) declare a dual-digest transition window now |
| **OQ-4** | D-4 | R6's temporal reach — the one that can revoke live grants | **(a) — PROSPECTIVE**; composition digests live grants were issued against are not re-derived by this act | (b) retroactive re-derivation — under the shipped drift cascade REVOKES `grant-mrc-0002`, on a day `grant-grc-0002` is already VOID and `grant-grc-0003` cannot yet be minted; (c) prospective plus a named reconciliation task |
| **OQ-5** | D-5 | How much of R12 is encoded here | **(a) — the INTERIM half only**: unsigned digests admissible, activation fail-closed on match, self-attestation refused | (b) defer the whole ruling — leaves self-attestation UNREFUSED; (c) encode the signer here too — contradicts R12's own words |
| **OQ-6** | D-6 | Who discharges 7.6 Ground 1, and who ticks 7.6 | **(a) — ratification of THIS packet discharges Ground 1**; the tick in the parent's `tasks.md` is a separate act on a separate word | (b) this packet edits the parent's `tasks.md` itself — collides with the sibling S3/S5 bookkeeping lane; (c) discharge only on archive — contradicts Ground 1's own words, "ratified" |
| **OQ-7** | D-7 | Ratification ordering against the pending gate-rules act | **(a) — NOT sequenced against openxFactory PR #1006** — zero file overlap, measured | (b) hold until #1006 merges; (c) hold until the parent's S3/S5 bookkeeping lands |
| **OQ-8** | D-8 | Realization surface and archive gate | **(a) — declare the surface**; archive on merged-plus-green realization evidence | (b) `code_surface: none` — a FALSE declaration, since a `digest_subject` member is contract bytes; (c) split — doctrine now, contract later |
| **OQ-9** | D-9 | R10's governing-configuration members: closed or minimum | **(a) — four named members REQUIRED**, a corpus MAY declare further invalidating members | (b) exactly four, closed — a corpus could add a governing knob that silently never invalidates; (c) four required, further members non-invalidating |

**EVERY RULING IS THE RECOMMENDED OPTION.** No requirement text was rewritten,
no delta directory was renamed, and no `sequenced_after:` entry moved.

## 3. What this word admits, and what it does not

**ADMITTED.** The seven `## ADDED` requirements on `review-authority-intake`
exactly as authored on PR #1017: what a holder composition's model component
digests (R6, prospectively per OQ-4); the one digest construction that governs
a composition, adopted by reference (R7/OQ-2), with no agility mechanism
minted (OQ-3); the five-field re-issuance record as a floor, not a ceiling
(R8); a revoked holder parking the convening with a named refusal (R9); corpus
drift invalidating on identity or governing configuration, with the four
members required and not closed (R10/OQ-9); the lifecycle roles table with
REGISTER as the only human-ratified act (R11); and R12's interim half only —
unsigned digests admissible, self-attestation refused (OQ-5). The delta class
is `## ADDED` (OQ-1) and the archive ordering is held behind the three parents
named in `sequenced_after:`.

**NOT ADMITTED, AND NOT BY THIS WORD.**

- **Nothing reaches `openspec/specs/`.** This ratification edits no promoted
  file. `review-authority-intake` has no promoted specification today
  (`add-wallet-carried-review-authority` and `register-gate-rules-council-seats`
  are both still ACTIVE), and this packet's own `tasks.md` § 5 holds its
  archive behind those two plus `amend-register-act-5b-projection-proof`.
- **No contract byte moves.** `contracts/signed-execution-chain/digest-construction.schema.yaml`'s
  `digest_subject` enumeration is untouched, `contracts/manifest.yaml`'s
  `sha256:` row is untouched, and `contracts/CHANGELOG.md` gains no line —
  those are `tasks.md` § 3.1–3.2, realization, not ratification.
  R7's requirement stays UNREALIZABLE by its own text until they land.
- **No reader advances.** openXwallet's pinned reader is not touched and
  `contracts/openxwallet-pin.yaml` stays at `commit: f3eb929b` — `tasks.md`
  § 3.3–3.4.
- **The runbook is not amended.** `docs/governed-reissuance-runbook.md` keeps
  its own `Status` and gains no sentence — `tasks.md` § 3.5, which also
  requires taking `amend-register-act-5b-projection-proof`'s amendment first.
- **`add-wallet-carried-review-authority/tasks.md` is not touched.** Ground 1
  is discharged BY this ratification (§ 4 below), but the 7.6 tick itself is
  the parent's act on a separate word (OQ-6), performed by the lane holding
  that ledger.
- **Nothing in `governance/review-authority/` moves.** No register row, grant,
  wallet key or custody attestation is issued, revoked, re-issued or
  repointed.

## 4. What is owed after this word

- **§ 2 (encode) is a no-op**, recorded rather than performed: every OQ was
  ruled at its recommendation, so the encoded wording IS the ratified
  wording (`tasks.md` task 2.1's own escape clause).
- **§ 3 (realize)** — the contract enumeration member, the openXwallet reader
  advance and pin bump, and the runbook carry — is separate work, in two
  repositories, not part of this ratification.
- **§ 4 (cite back)** — Ground 1 is recorded discharged by this act (below);
  the 7.6 tick is handed off, not performed, to the lane holding
  `add-wallet-carried-review-authority/tasks.md`.
- **§ 5 (archive)** stays entirely open, held behind
  `add-wallet-carried-review-authority`, `register-gate-rules-council-seats`
  and `amend-register-act-5b-projection-proof`, per OQ-6/OQ-7 and this
  packet's own `sequenced_after:` declaration, plus § 3's merged-plus-green
  realization evidence.
- **Merge is a separate word.** This ratification takes PR #1017 out of DRAFT
  (marked READY) but does not merge it; Rule 6 (the landing-window protocol
  for a PR touching `openspec/changes/` + README) applies at landing.

## 5. Ground 1, discharged

`add-wallet-carried-review-authority/tasks.md` § 7.6's own sentence:
*"neither ruling is enforced until the change carrying R6–R12 is ratified, so
this task stays OPEN."* This packet IS the change carrying R6–R12,
ratification is this act, dated 2026-09-12T23:58Z. **Ground 1 is discharged as
of this record.** Ground 2 (whether the two dated walks discharge 7.6's "walk
it once" limb) is not this packet's to close — it is the parent-ledger lane's,
citing `walk-2026-08-31-composition-bump.md` and
`walk-2026-09-02-register-act.md`.

## 6. Provenance of this record

Written in the ratification commit itself, in the worktree
`~/projects/xFactory/openxFactory-worktrees/wcra-r6-r12`, by lane
`hermes-wallet-exercise`. It carries `Status: ratified` because
`document-lifecycle`'s *A review record records a ratification* governs a
`review/ratification-*` file. Every path in this file is repo-relative.
