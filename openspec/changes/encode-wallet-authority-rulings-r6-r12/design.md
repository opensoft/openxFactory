# Design: encode-wallet-authority-rulings-r6-r12

Status: ratified
Ratified by: Brett Heap, 2026-09-12T23:58Z — verbatim "accept all A on 1017" (record `review/ratification-2026-09-12.md`)
Kind: design
Lane: hermes-wallet-exercise

**WHAT THIS DOCUMENT IS FOR.** `proposal.md` carries the seven rulings verbatim
and the nine decisions. This document carries three things a reader needs and
that prose cannot hold: the RULING → REQUIREMENT map (so no ruling is silently
dropped and no requirement is silently invented), the decisions D-1 through D-9
that mirror OQ-1 through OQ-9 with their rejected alternatives, and the two
questions the lane was asked to answer explicitly — whether this packet changes
`governance/review-authority/` semantics, and whether any ruling reaches the
gate-rules chain currently under hold.

---

## 1. Ruling → requirement map

Seven rulings, seven ADDED requirements, one to one. **No ruling is split
across requirements and no requirement carries two rulings**, so a later reader
holding a requirement against `rulings-2026-08-29.md` compares one text with
one text.

| ruling | requirement title (`specs/review-authority-intake/spec.md`) | scenarios | what is DEFERRED out of it |
|---|---|---|---|
| **R6** | A holder composition's model component digests the provider plane together with the exact published identifier | 4 | nothing; OQ-4 fixes its temporal reach as prospective |
| **R7** | One digest construction governs a holder composition, and it is the estate's existing one | 4 | nothing; OQ-3 answers the agility/dual-digest question R7 assigned to "the carrying change" |
| **R8** | A re-issuance act records five fields as a MINIMUM, and the floor is not a ceiling | 3 | nothing; the "may extend" permission is recorded and NOT exercised |
| **R9** | A revoked holder parks the convening, and only a new human-ratified issuance resumes it | 3 | nothing |
| **R10** | Retrieval-corpus drift invalidates on identity or governing configuration, never on rows | 4 | nothing; OQ-9 fixes the four members as REQUIRED and not CLOSED |
| **R11** | Register is the only human-ratified act in the lifecycle, revoke waits on no human, and re-issue always requires one | 3 | nothing |
| **R12** | An unsigned composition digest is admissible in the interim, and a holder MUST NOT attest its own composition | 4 | **the signer half, by name**: envelope standard, key distribution, signature algorithm, evidence-retention location — all travel with `signed-execution-chain`, as R12 rules |

**THE ONE DELIBERATE OMISSION IS R12's SIGNER HALF, and the rulings record
predicts it in its own words** — *"carrying R6–R12 as ratified contract text
(with R12's signer half landing in signed-execution-chain instead)"*. Nothing
else in Packet 4 is omitted, narrowed or extended.

**R1–R5 ARE NOT IN THIS PACKET AND ARE NOT SILENTLY DROPPED.** They belong to
Packets 1 and 2, they have their own enforcement paths (the Gate-Rules
Council's selection act plus the roster-change Lead's acceptance for R1–R4; the
Operator identity record for R5), and the rulings record assigns them there.
R5's operator record exists —
`add-wallet-carried-review-authority/operator-identity-record-2026-09-01.md` —
and this packet neither amends nor re-performs it.

---

## 2. Decisions

### D-1 (OQ-1) — Home capability: `review-authority-intake`, `## ADDED` — RULED (a), 2026-09-12T23:58Z

**The class is FORCED, not preferred.** `openspec/specs/` carries no
`review-authority-intake/spec.md`: both authoring changes
(`add-wallet-carried-review-authority`, `register-gate-rules-council-seats`)
are ACTIVE and neither has archived, so there is no requirement to
`## MODIFIED`. The consequence is stated rather than inferred: **these seven
requirements promote when THIS change archives**, and tasks § 5 holds that
archive behind its parents so the capability's promoted file is created by its
author and not by a successor.

Rejected: a new `holder-composition` capability (splits the register's grammar
across two specifications with no rule obliging agreement); a split placing
R6/R7 in `signed-execution-chain` (that capability IS promoted, so R6/R7 would
become a `## MODIFIED` of shipped canon to carry a subject it does not compute
— and `signed-execution-chain`'s own promoted text says a capability computing
digests SHALL NOT carry a second construction rule, which is an argument for
adopting its construction, not for moving composition doctrine into it).

### D-2 (OQ-2) — R7 by ADOPTION, and the route is precedented twice — RULED (a), 2026-09-12T23:58Z

`xfc-jcs-sha256-1` is R7's ruled profile already shipped: RFC 8785 JCS,
SHA-256, `sha256:` + 64 lowercase hex, profile named and versioned, every
digest algorithm-tagged. It is declared in
`contracts/signed-execution-chain/digest-construction.schema.yaml` and its
header invites extension by SUBJECT: *"A LATER TRANCHE ADDS NO SECOND RULE …
with its subject added to the enumeration below."*

**Taken twice already, and once from OUTSIDE the family** — `add-chain-anchoring`
(eleven subjects, inside `signed-execution-chain`) and `add-cpc-clearing-boundary`
(`sealed_bundle_manifest`, realized by the neutral `contracts/clearing/` family).
The second is this packet's precedent exactly: a different capability's
requirement naming `xfc-jcs-sha256-1` and a one-member widening, with the
honest self-limiting sentence *"Until that subject exists, this requirement is
UNREALIZABLE as written and SHALL NOT be reported as satisfied."* **This
packet's R7 requirement carries that same sentence**, so it cannot be reported
green before the enumeration member lands.

**THE CLAIM IS BOUNDED HONESTLY.** Declaring a second JCS profile would not
LITERALLY violate the promoted requirement, which scopes itself to
`signed-execution-chain`. What it would do is reproduce the identical defect at
estate scale. This packet says that, and does not dress a design preference as
a contract violation.

### D-3 (OQ-3) — No agility mechanism, and it is DECIDED — RULED (a), 2026-09-12T23:58Z

R7 left "digest agility and any dual-digest transition" open and assigned both
to "the carrying change". This is the carrying change, so leaving them open a
second time would be the one outcome the ruling forbids. **Decision: none is
minted.** Algorithm tagging plus a recorded profile name and version is what
makes a later migration a readable change; a transition mechanism with no
second algorithm to transition to is a widening nothing exercises, and an
admitted mechanism with no consumer is the shape
`digest-construction.schema.yaml` itself declines elsewhere (*"an admitted
subject with no consumer is a widening nothing exercises"*).

### D-4 (OQ-4) — PROSPECTIVE, and this is the decision that can revoke live grants — RULED (a), 2026-09-12T23:58Z

**Retroactive re-derivation would revoke both councils' authority as a side
effect of a doctrine packet.** The shipped drift cascade revokes on a changed
composition; re-deriving every live composition digest under R6's
plane-inside-the-digest reading changes those digests; a changed digest IS a
composition change to the cascade. Measured against `bcde1575`, that lands on:

| chain | row | grant | state today |
|---|---|---|---|
| merge-readiness | `row-mrc-0001` | `grant-mrc-0002` | ACTIVE, issued 2026-09-02T13:33:48Z, expires 2027-06-30 |
| gate-rules | `row-grc-0001` | `grant-grc-0002` | **VOID** since codexFactory PR #439 → `eff9ae19`, merged 2026-09-12T15:59:10Z; successor `grant-grc-0003` PRE-STAGED and unmergeable in openxFactory PR #1006 pending Brett Heap's host-side key mint |

So option (b) would revoke the one live grant in the estate on a day when the
other chain's successor cannot yet be minted. **Prospective binding is chosen
for that reason and the reason is recorded, not assumed.** The next genuine
composition event re-derives under the ruled reading in the ordinary way, which
is the path both walks already exercised.

### D-5 (OQ-5) — R12's interim half encoded, signer half deferred by name — RULED (a), 2026-09-12T23:58Z

Three interim sentences in R12 are enforceable statements and are encoded:
unsigned digests admissible; activation fail-closed on digest match regardless;
the 2026-08-28 per-seat Ed25519 keys refused for self-attestation. Deferring
the whole ruling would leave self-attestation UNREFUSED, which is a live
permission and not a silence. The four envelope questions are named as deferred
so the requirement's silence cannot be read as an answer — the delta carries a
scenario refusing exactly that inference.

### D-6 (OQ-6) — Ratification discharges Ground 1; the parent ticks 7.6 — RULED (a), 2026-09-12T23:58Z

Ground 1's own words are *"until the change carrying R6–R12 is **ratified**"* —
ratified, not archived, not realized. **So ratification of this packet
discharges it**, and the tick is then an act in the PARENT's ledger on a
separate word. This packet does not edit
`add-wallet-carried-review-authority/tasks.md`: a sibling lane is actively
ticking its S3/S5 rows, and two lanes editing one ledger is precisely the
collision the lane-collision protocol exists to prevent.

**AND GROUND 2 IS NOT THIS PACKET'S TO CLOSE EITHER.** The parent's note frames
the remaining question as *"whether the pair discharges 7.6's 'walk it once'
limb, and the answer is very likely yes on the evidence"* — the lane holding
that ledger answers it, citing the two walk records.

### D-7 (OQ-7) — Not sequenced against PR #1006 — RULED (a), 2026-09-12T23:58Z

**FILE-LEVEL MEASUREMENT, not a judgment call.** PR #1006 edits
`governance/review-authority/register.yaml`,
`governance/review-authority/wallets/wal-agent-grc-0001.yaml` and a grant file.
This packet edits none of them — its whole diff is
`openspec/changes/encode-wallet-authority-rulings-r6-r12/**`, one README block,
and one generated ledger row, with the contract enumeration member owed at
realization. **Zero file overlap, so either may land first.**

`sequenced_after:` declares `add-wallet-carried-review-authority`,
`register-gate-rules-council-seats` and `amend-register-act-5b-projection-proof`.
That is a REALIZATION-AXIS declaration — which changes must archive before this
one can — and it is not a merge queue.

### D-8 (OQ-8) — Declared code surface, archive on merged-plus-green — RULED (a), 2026-09-12T23:58Z

A `digest_subject` member is a contract artifact's bytes, so
`code_surface: none` would be a FALSE declaration. Under `release-realization`
a declared surface archives on merged-plus-green realization evidence, which is
the gate tasks § 5 holds this packet behind. The ENFORCING half — the reader
that refuses a non-conforming composition, an unnamed refusal or a
self-attestation — is openXwallet's, consumed here through
`contracts/openxwallet-pin.yaml` (`commit: f3eb929b`), so it is a pinned-reader
advance in another repository plus a pin bump here. **Named in tasks § 3 and
NOT performed by this packet.**

### D-9 (OQ-9) — R10's four members REQUIRED, not CLOSED — RULED (a), 2026-09-12T23:58Z

Scope, selection configuration, admission policy and ontology package digest
are each required members of the governing configuration digest; a governed
corpus MAY declare further members that likewise invalidate. **Reading the four
as closed would let a corpus add a new governing knob that silently never
invalidates** — the exact failure R10 exists to refuse, reintroduced through the
enumeration. This mirrors R8's own floor-not-ceiling shape, so the packet reads
consistently across the two rulings that both bound a field set.

---

## 3. Does this change `governance/review-authority/` SEMANTICS?

**YES, prospectively — and NO to any file under it today.** Both halves matter
and neither is the other.

**The semantics it changes**, once ratified and realized: what a `model_version`
component must digest (R6); under which construction a composition digest is
computed and how it is tagged (R7); what a re-issuance act must record (R8);
what an exercise must do on a composition mismatch and what may resume it (R9);
which corpus movements invalidate a composition (R10); which lifecycle acts
require a human (R11); and whether an unsigned or self-signed composition digest
is admitted (R12). These are the rules by which the register's grants are
issued, revoked, re-issued and read.

**The files it touches today: NONE of them.** Not `register.yaml`, not
`grants/grant-mrc-0002.yaml`, not `grants/grant-grc-0002.yaml`, not
`wallets/wal-agent-mrc-0001.yaml`, not `wallets/wal-agent-grc-0001.yaml`, not
either custody attestation. **No row is added, repointed, expired or
deactivated; no grant is issued, revoked or superseded; no wallet key is
registered; the `revocation_staleness_bound` is not touched.** The register is
single-file and serial, and this packet takes no place in that queue.

**AND NO EXISTING RECORD BECOMES RETROACTIVELY NON-CONFORMANT**, because D-4
binds R6 prospectively. That is the whole reason D-4 was put as a decision
rather than assumed: the alternative reading is the one that would reach into
`governance/review-authority/` without editing a byte of it.

---

## 4. Does any ruling reach the gate-rules chain now under hold?

**NO ruling singles it out, and every ruling will eventually govern BOTH
chains.** The distinction is worth stating exactly, because the two are easy to
conflate.

**The chain under hold is `agent:gate-rules-council`'s** — `row-grc-0001`,
whose grant lineage on `main` at `bcde1575` reads `grant-grc-0001` (revoked for
DRIFT 2026-09-11T02:12:30Z) → `grant-grc-0002` (the row's current `grant_ref`,
**VOID** since codexFactory PR #439 → `eff9ae19` merged 2026-09-12T15:59:10Z, by
the declared composition change itself and not by anything in openxFactory) →
`grant-grc-0003`, which is PRE-STAGED and unmergeable in openxFactory PR #1006
pending one 32-byte host-side mint. The row's own `state` is still `active`,
because a row is the authority's continuing existence and a void grant does not
deactivate the row that points at it.

**The chain that is live is `agent:merge-readiness-council`'s** —
`row-mrc-0001` → `grant-mrc-0002`, ACTIVE, and the chain both existing walk
records were performed against.

**R6–R12 are holder-neutral.** Not one of the seven names a council, a holder,
a row or a grant. They govern what a composition IS (R6, R7, R10), what a
re-issuance RECORDS (R8), what an exercise DOES on mismatch (R9), who must be
human (R11), and what an attestation may claim (R12) — for any holder in the
register. **So the answer to "does it touch only merge-readiness' chain" is
no: it touches neither today and will govern both tomorrow.**

**TWO CONSEQUENCES THAT FOLLOW, and both are already decided above.** First,
D-4's prospective binding is what keeps this neutrality harmless: a retroactive
reading would fire on BOTH chains at once, and the gate-rules chain cannot
currently mint a successor. Second, D-7's zero-file-overlap measurement is what
keeps this packet out of the register's serial queue while that mint is
pending.

---

## 5. Where the requirements are enforced, and by what

**Nothing in this repository enforces a composition rule today.** Measured at
`bcde1575`: `grep -rn "model_version" scripts/ tests/ .github/` returns
NOTHING. The checking reader is openXwallet's, consumed through
`contracts/openxwallet-pin.yaml` at `commit: f3eb929b` (`wallet-v1.5`), and the
register's own comments name it as the thing that refuses — its
`register-seat-row-unresolved` rule, its exact-set-equality over the nine row
fields, its `(council_id, seat_id)` uniqueness.

So the realization splits in three, and tasks § 3 names each:

1. **The contract member** — `holder_composition` added to
   `digest-construction.schema.yaml`'s `digest_subject` enumeration, its
   `contracts/manifest.yaml` `sha256:` row moved, one `contracts/CHANGELOG.md`
   line. In THIS repository. Without it, the R7 requirement is UNREALIZABLE by
   its own text.
2. **The reader** — openXwallet advancing to refuse a composition that digests
   an identifier without its plane, a re-issuance record missing one of the
   five, a self-attested composition, and an unnamed park refusal; then
   `contracts/openxwallet-pin.yaml` advancing here to consume it.
3. **The runbook** — `docs/governed-reissuance-runbook.md` carrying R8's record
   grammar and R9's parking language, so the document the two walks followed
   says what the requirements now require. **This is the same file
   `amend-register-act-5b-projection-proof` amends at ITS realization**, which
   is why that change is declared in `sequenced_after:` and why tasks § 3 tells
   the realizing lane to take that amendment first rather than race it.

**AND THE DEFECT THE 2026-09-02 WALK FOUND SITS IN LEG 2.** That walk's § 9
measured the pinned reader REFUSING a correctly-performed re-issuance:
`check_register`'s closing loop filters REVIEW-class grants by act and never
checks `state`, so a correctly revoked grant demands a backing active row the
one-row cap forbids, with a two-line remedy measured green. **It is not this
packet's deliverable and this packet does not claim it** — but leg 2 is where a
realizing lane will meet it, and naming it here is cheaper than rediscovering
it.
