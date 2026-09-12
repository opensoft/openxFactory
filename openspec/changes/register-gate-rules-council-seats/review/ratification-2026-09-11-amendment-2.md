# Proposal Ratification: register-gate-rules-council-seats — Amendment 2 (the Q-GRC-4 discharge)

Status: ratified
Kind: report
Decision date: 2026-09-11
Ratifier: Brett Heap (repository owner, operator) — in session, window
`codeXfactory-2`, no comment URL.
Ratified: 2026-09-11T17:08:42Z by Brett Heap (repository owner, operator),
verbatim *"accept all A on 971, merge slice 3 when green"* — its FIRST clause,
a MULTIPLE-CHOICE ruling over the five open questions
`review/amendment-2026-09-11-q-grc-4-discharge.md` § 9 put (`design.md` D8
through D12), taking option **(a)**, the RECOMMENDED one, on every one of them.
Subject: the packet's SECOND amendment, landed DRAFT by PR
[#971](https://github.com/opensoft/openxFactory/pull/971) → `3402d93a`.

**THIS RATIFIES AN AMENDMENT, NOT THE PACKET.** `register-gate-rules-council-seats`
has been `Status: ratified` since 2026-09-06 (`review/ratification-2026-09-06.md`,
head `169f84ef`) and is not re-ratified here; no ruling in it is reopened.
**OQ-1 = (a), OQ-2 = (a), OQ-3 = (a), OQ-4 = (a), OQ-5 = (a)** — each the option
the amendment already encoded, so **THE DELTA'S WORDING STANDS UNCHANGED AND
NOTHING WAS SUBSTITUTED, RESTORED OR DELETED.**

## 1. The word, and what it reaches

**`"accept all A on 971, merge slice 3 when green"` IS TWO CLAUSES ADDRESSED TO
TWO SEATS, AND ONLY THE FIRST IS THIS RECORD'S.** It was given at
**2026-09-11T17:08:42Z**, in session, window `codeXfactory-2`, with **no comment
URL** — the ruling was spoken, and the absence is recorded rather than papered
over, on the precedent the amendment record's own `Ruling URL:` line already
cites for the 14:59:26Z rulings
(`split-opendox-two-layer-product/review/amendment-2026-09-05-repository-shape.md`,
whose `Ruler:` line likewise names a session rather than a URL). The second
clause — *"merge slice 3 when green"* — is the hermes-install Phase 8 slice 3
sweep, a different repository and a different seat's work, and is carried here
only so the word is quoted whole rather than trimmed to the half that suits this
record.

**`"accept all A on 971"` NAMES THE PULL REQUEST, AND THE PULL REQUEST NAMED THE
FIVE.** PR #971 landed the amendment as a DRAFT amendment at 2026-09-11T16:49:55Z
(head `1d49368b`, merge commit `3402d93a`), with its § 9 open questions and their
lettered options stated in the tree before the word was given. Nothing was put to
the owner that was not already on `main` to read.

**WHAT THE WORD MOVES, DOCUMENT BY DOCUMENT.** `proposal.md` (the `Amended:
2026-09-11` header block and § AMENDMENT — 2026-09-11's Rulings table),
`design.md` (D8-D12, each header gaining its inline `RULED (a), <UTC>` marker and
the 1:1 mapping table gaining a ruled column), `tasks.md` (§ 6.1 and § 6.1a
ticked; 6.6, 6.8, 6.10, 6.18 and 6.24 made definite where they had named an OQ as
undecided), the amendment record (§ 9's five appended `RULED` lines and one added
`Ratification:` header line), `README.md`'s active row, and this record.

**`.openspec.yaml` IS DELIBERATELY NOT TOUCHED, AND THAT IS MEASURED RATHER THAN
ASSUMED.** #960's ratification added `approved_by`/`approved_on` beside its
`proposed_by`/`proposed_on` drafting pair, in the shape
`add-drafted-proposal-origin` (issue #318) defined — but this packet's
`.openspec.yaml` already carries an `approved_by`/`approved_on` pair, whose own
text says in terms *"THIS FIELD RECORDS AUTHORIZATION TO AUTHOR, NOT RATIFICATION
OF CONTENT, AND MUST NOT BE READ AS ONE."* The packet's own content ratification
of 2026-09-06 did not rewrite it either: `git log --follow --oneline --
openspec/changes/register-gate-rules-council-seats/.openspec.yaml` returns
**exactly one commit** (`a59f2ae5`, the authoring commit). An amendment
ratification that overwrote an authoring-approval field would destroy the
distinction that field exists to make, and the YAML has no second pair to add.

## 2. The five open questions, as put and as ruled

| OQ | `design.md` | Put | Ruled | Considered, not adopted |
| --- | --- | --- | --- | --- |
| **OQ-1** | D8 | Who mints and holds the fifth seat keypair | **(a)** — Brett Heap, host-side, the task 3.2 ceremony generalized to one seat: seed generated in-process and never written to disk, `gh secret set` on stdin with `--body` omitted, custody `holder_readable`, secret `COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER`, a FRESH TTY-gated ceremony and never a rerun of stored state | (b) mint through the committed `scripts/mint-factory-origin-key.py`; (c) a different custody model for this one key, which would give one seat of one bench a key its own holder job cannot read |
| **OQ-2** | D9 | `expires_at` on the re-issued `grant-grc-0003` | **(a)** — `2027-06-30T00:00:00Z`, UNCHANGED: Q-GRC-3's ruled date, the one `grant-mrc-0002` still carries, so the two bodies' grants cannot silently diverge | (b) recompute from the earliest published retirement floor among the five pins — returns the same date today; (c) a shorter expiry for the new seat alone, refused by shape (the grant is addressed to the WALLET and carries one expiry) |
| **OQ-3** | D10 | Whether the CSC briefing owes a soak or an `activation_gate` pass before the seat sits live | **(a)** — BIND NOW, SOAK LATER, the lead-architect precedent exactly: the seat is bound and its key registered in this act, and **no soak and no `activation_gate` pass is a precondition of binding**. C13 re-opens this body's soak from zero and costs nothing today; LQ-C4's `tool_manifest` bound carries onto the new seat unchanged | (b) require an LQ-C1-shaped fresh soak at the CSC pin first; (c) declare a `gate_rules_council` `activation_gate` of its own — measured: none exists today, so this is new machinery rather than a gate being honoured |
| **OQ-4** | D11 | One T1/T2 pull-request pair, or a further split | **(a)** — the T1/T2 PAIR: one codexFactory pull request (H1, §§ 6.2-6.8), then one openxFactory pull request (H2, §§ 6.9-6.15). Two remotes, ONE governed act, the hold spanning them; **H1 is not split further** | (b) split H1 into separate mint / roster / composition pull requests; (c) one single cross-repository act — not available, two remotes cannot share a commit |
| **OQ-5** | D12 | Whether C2 doubles as the seat's first live (proof) convening | **(a)** — a SEPARATE proof convening PRECEDES C2, on a re-verified clean candidate, exactly as the 2026-09-11 walk did (§ 15, run `34586762846`, admitted). C2 is the convening the conjunction FIRES on, and one dispatch cannot say which of two proofs failed | (b) C2 IS the proof convening — cheaper by one pin, and task 6.22's read-only `resolved-seats` run already proves the BINDING; (c) two proof convenings, one each side of the conjunction — the most evidence and the most pins, and nothing in the corpus asks for it |

**EVERY RULING IS THE RECOMMENDED OPTION, SO THE DELTA MOVES NO BYTE**, which is
the sentence the amendment's own § 9 preamble predicted (*"taking all five
recommendations moves no byte of this packet"*). **PROVEN BY DIFF RATHER THAN
ASSERTED:** `git diff --stat 3402d93a -- openspec/changes/register-gate-rules-council-seats/specs/`
at the ratification commit is **EMPTY (0 files)** — the seven `## ADDED`
requirements on `review-authority-intake` are exactly what PR #971's ten green
checks ran against.

## 3. What this word admits, and what it does not

**ADMITTED.** The Q-GRC-4 discharge as authored: the
`client-security-compliance-officer` conjunction seat bound by the
lead-architect route at `lead-security`'s exact model pin (the 14:59:26Z ruling,
already recorded), and the five further decisions above — the minter and custody
of the fifth keypair (OQ-1), the re-issued grant's expiry (OQ-2), the
bind-now-soak-later order (OQ-3), the act's two-remote shape (OQ-4) and the
separate proof convening (OQ-5).

**NOT ADMITTED, AND NOT BY THIS WORD.**

- **RATIFICATION REALIZES NOTHING.** No key is minted, no seat is bound, no
  grant, wallet, register, attestation or roster byte moves, and no pin advances.
  `tasks.md` ticks § 6.1 and § 6.1a and nothing else.
- **C2 STAYS PARKED.** Brett's standing `α, park C2 until Q-GRC-4 is discharged`
  (2026-09-11T14:23:26Z) is NOT lifted here: § 7 of the amendment record says in
  terms that C2 unparks when the ACT completes, not when the amendment is
  ratified, and task 6.22's `resolved-seats` run showing
  `unbound_conjunction_seats` EMPTY is what lifts it.
- **§ 6.1b stays open.** The seat identifier string
  `client-security-compliance-officer` is an AUTHORING decision flagged for veto
  (amendment record § 4), not one of the five questions this word ruled, so it
  still owes its own confirmation before 6.2.
- **Nothing reaches `openspec/specs/`.** No promoted file is edited;
  `review-authority-intake` has no promoted specification today, both of its
  authors being ACTIVE changes.
- **codexFactory is not touched.** H1 is SPECIFIED by the amendment and BUILT
  after this ratification, through Speckit, in its own repository.
- **The archive gate is not widened.** § 6 is not an archive condition (§ 5.2
  puts § 4 outside it; 6.9 restates it), and `tasks.md` § 5 stays open.
- **No corpus-ledger row moves.** This packet already holds one
  (`tests/sequenced_after/corpus-ledger.yaml`, `state: active`, `class: sole`,
  `moved_by: "#717"`); an amendment ratification moves no state, and
  `--ledger-diff` re-proves it on the final tree.

## 4. What is owed after this word

- **H1 — the codexFactory roster act** (§§ 6.2-6.8), built via Speckit, opened as
  a pull request and **HELD for Brett Heap's merge word**. OQ-4 fixes it as ONE
  pull request rather than three.
- **H2 — the openxFactory register act** (§§ 6.9-6.15), Brett Heap's operator
  walk on a permanently human-only surface, after his host-side mint of the fifth
  keypair (OQ-1).
- **The proof convening**, separate and BEFORE C2, on a re-verified clean
  candidate (OQ-5) — then **C2**, which discharges the two carried-forward words
  `convene C2` (13:26:14Z) and `merge the C2 record PR when green` (13:27:23Z).
- **The landing of THIS ratification** is itself covered by a separate, later
  word — Brett Heap, **2026-09-11T17:13:06Z**, verbatim *"merge the ratification
  PR when green"* — which authorizes the merge of the pull request carrying this
  record and authorizes nothing else. Rule 1's claim and Rule 6's landing window
  are owed at that landing, not at this ratification.

## 5. Provenance of this record

Written in the ratification commit itself, in the worktree
`~/projects/xFactory/openxFactory-worktrees/ratify-q-grc-4`, by lane
`hermes-wallet-exercise` (window `codeXfactory-2`). It carries `Status: ratified`
because `document-lifecycle`'s *A review record records a ratification* governs a
`review/ratification-*` file, and one citation in the record-citing spelling
(`Ratified:`) because there is no approving OpenSpec change to name — the
approval is an in-session ruling. Its sibling
`review/verification-2026-09-11-amendment-2.md` keeps `Status: record`: that
file's subject is the GATE RUN. The amendment record
`review/amendment-2026-09-11-q-grc-4-discharge.md` likewise keeps `Status:
record` and gains one ADDED `Ratification:` header line, on that record's own
§ 8 rule — *a record's header states the act that made it, and an amendment adds
a line rather than rewriting one* — and on the corpus convention this
ratification measured rather than assumed: every one of the seven other
`review/amendment-*.md` records in this repository, active and archived, carries
`Status: record`. Every path in this file is repo-relative.
