---
code_surface: contracts/signed-execution-chain/digest-construction.schema.yaml (ONE new `digest_subject` member), contracts/manifest.yaml (that file's `sha256:` row, which moves because the bytes move), contracts/CHANGELOG.md (one line), and docs/governed-reissuance-runbook.md (the re-issuance record grammar R8 fixes and the parking language R9 fixes). MEASURED, NOT ASSUMED, against openxFactory `main` `bcde1575`. (1) R7 rules RFC 8785 JCS with a `sha256:<lowercase-hex>` digest "recorded together with the canonicalization profile name and its version" — and that construction ALREADY SHIPS here as `xfc-jcs-sha256-1`, so the realization is ADOPTION BY REFERENCE plus one enumeration member, the exact movement `contracts/signed-execution-chain/digest-construction.schema.yaml`'s own header sanctions ("A LATER TRANCHE ADDS NO SECOND RULE ... with its subject added to the enumeration below") and that `add-cpc-clearing-boundary` already took from a different capability. A contract artifact's bytes move, so this is NOT a `code_surface: none` packet and MUST NOT be filed as one. (2) `grep -rn "model_version" scripts/ tests/ .github/` returns NOTHING — no in-tree script, test or workflow computes or checks a holder composition today; the checking reader is openXwallet's, consumed through `contracts/openxwallet-pin.yaml` (`commit: f3eb929b`), so R8/R9/R10/R11/R12's mechanical enforcement is a PINNED-READER advance in another repository and a pin bump here, named in tasks § 3 and NOT performed by this packet. (3) NOTHING under `governance/review-authority/` is touched: not `register.yaml`, not a grant, not a wallet, not a custody attestation — this packet writes requirement text and one contract enumeration member, and it issues, revokes, re-issues and repoints nothing. (4) The one file under `tests/` that moves is `tests/sequenced_after/corpus-ledger.yaml`, a GENERATED registry gaining this change's own sweep row through the sanctioned `scripts/validate-sequenced-after.py . --seed-ledger`. Under `release-realization` a DECLARED code surface archives on merged-plus-green realization evidence and not on landing, which is the gate tasks § 5 holds this packet behind.
target_release: contract bundle — a `digest_subject` enumeration member is a contract artifact change, so the realization is owed a bundle cut and a `contracts/CHANGELOG.md` line, and every consumer that pins the bundle receives it by advancing that pin. NO BUNDLE NUMBER IS TAKEN OR RESERVED HERE: the cut, the `contract_bundle_version` bump and the CHANGELOG line stay the cutting session's act, exactly as `contracts/manifest.yaml`'s own realization notes require. The requirement text itself promotes at archive; the bundle is what carries the enumeration member to readers.
sequenced_after: [add-wallet-carried-review-authority, register-gate-rules-council-seats, amend-register-act-5b-projection-proof]
---

# Proposal: encode-wallet-authority-rulings-r6-r12

Status: ratified
Ratified: 2026-09-12T23:58Z by Brett Heap (openxFactory operator authority) — verbatim "accept all A on 1017"; record at review/ratification-2026-09-12.md
Lane: hermes-wallet-exercise
Proposed: 2026-09-12, in lane `hermes-wallet-exercise` (window
`hermes-wallet-exercise`, session `codeXfactory-2`, workstation Eagle), on
Brett Heap's multiple-choice word of 2026-09-12, verbatim:
***"Author the R6–R12 successor change"***.
Origin: the closing paragraph of
[`add-wallet-carried-review-authority/rulings-2026-08-29.md`](../add-wallet-carried-review-authority/rulings-2026-08-29.md)
§ "Packet 4 — canonical composition and re-issuance (R6–R12)", which names this
change by shape and makes seven rulings unenforceable until it is ratified.

**THIS PACKET IS NOW RATIFIED.** It was filed `Status: draft` and HELD; the
word that commissioned its authoring commissioned the AUTHORING only. Nine
decisions were put below as multiple choice (§ Open questions), each with a
RECOMMENDED option and the one-line reason it was recommended. **Brett Heap
ruled 2026-09-12T23:58Z, verbatim ***"accept all A on 1017"*** — all nine at
their RECOMMENDED option (§ Rulings below), so the delta moved not one byte.**
Ruling otherwise on OQ-1, OQ-2, OQ-3, OQ-5 or OQ-9 would have rewritten the
requirement it names before ratification; ruling otherwise on OQ-4 would have
revoked live grants; ruling otherwise on OQ-6, OQ-7 or OQ-8 would have moved
the packet rather than its wording — none of that was taken.

---

## Why

**Seven ruled directions are recorded and none of them is enforced, and the
record says so in its own words.** From
[`rulings-2026-08-29.md`](../add-wallet-carried-review-authority/rulings-2026-08-29.md),
§ Packet 4, verbatim:

> **What makes R6–R12 enforceable:** a FRESH OpenSpec change, authored after
> issuance, carrying R6–R12 as ratified contract text (with R12's signer half
> landing in signed-execution-chain instead). Until that change is authored,
> ratified and realized, the canonical serialization, the digest, the
> re-issuance grammar and the corpus-drift rule are recorded direction and NOT
> enforced behavior: report §7's "Canonical serialization profile and value-
> domain rules" and "Attestation envelope and signer trust model" rows stay
> blocking. No implementation of R6–R12 precedes that change.

The same section opens by saying the same thing from the other end, verbatim:

> These rulings answer report §5 "Proposed Canonicalization And Attestation
> Design", "Lifecycle Roles", and "In-Flight Behavior And Re-Issuance". They are
> ratification TARGETS: none of them is implementable until the change that
> carries them is authored and ratified.

**And that absence is the ONE ground on which the parent's load-bearing S5 task
stays shut.** From
[`add-wallet-carried-review-authority/tasks.md`](../add-wallet-carried-review-authority/tasks.md)
§ 7.6, verbatim:

> - **GROUND 1 — THE TASK'S OWN SENTENCE, and it has nothing to do with the
>   walk:** *"neither ruling is enforced until the change carrying R6–R12 is
>   ratified, so this task stays OPEN."* **R6–R12 is not authored, let alone
>   ratified.** No walk can discharge a condition about a different change's
>   ratification, and a tick here would assert an enforced control that does
>   not exist — nothing in this estate would refuse a bump that ignored the
>   runbook entirely.

And, after the second walk, restated so no reader can mistake which ground
survives, verbatim:

> - **GROUND 1 IS UNTOUCHED AND IT IS THE ONE THAT SHUTS THE TASK.** *"Neither
>   ruling is enforced until the change carrying R6–R12 is ratified, so this
>   task stays OPEN."* **R6–R12 is still not authored.** No act of any class
>   can discharge a condition about a different change's ratification, and the
>   bullet above already says nothing turns on Ground 2 today.

**GROUND 2 IS ALREADY DISCHARGED ON THE EVIDENCE, so Ground 1 is alone.** The
runbook exists — `docs/governed-reissuance-runbook.md`, openxFactory `65c3a803`
(PR #527) — and it has been walked TWICE, in the two classes the task's own
notes name:

| walk | class | record | what it exercised |
|---|---|---|---|
| 2026-08-31 | precision | [`walk-2026-08-31-composition-bump.md`](../add-wallet-carried-review-authority/walk-2026-08-31-composition-bump.md) | the alias-to-exact enrolled-roster pin flip, codexFactory `6edecaf1` (PR #146), performed BY following the runbook. Steps 5, 5.1 and 5.2 NOT exercised, and the record says so in terms |
| 2026-09-02 | revocation | [`walk-2026-09-02-register-act.md`](../add-wallet-carried-review-authority/walk-2026-09-02-register-act.md) | `grant-mrc-0001` REVOKED for DRIFT, `grant-mrc-0002` MINTED at the same instant (`2026-09-02T13:33:48Z`), `row-mrc-0001` REPOINTED, no row added — runbook § 5.1's three writes and one non-write, performed for real |

The parent's own note draws the conclusion this packet acts on, verbatim:
*"When R6–R12 ratifies, the question is whether the pair discharges 7.6's
'walk it once' limb, and the answer is very likely yes on the evidence;
**Ground 1 is what will still need to move.**"* This packet is what moves it.

## The measurement that shaped the delta before it was written

**R7 rules a canonicalization profile that this repository already ships.**
R7's text names "JSON Canonicalization Scheme (RFC 8785)", a
`sha256:<lowercase-hex>` digest, and recording "the canonicalization profile
name and its version". Measured at `bcde1575`, that is
**`xfc-jcs-sha256-1`** — declared ONCE, in
`contracts/signed-execution-chain/digest-construction.schema.yaml`, under the
PROMOTED `signed-execution-chain` requirement *"One digest construction governs
every digest this capability computes"*, as three non-optional parts: RFC 8785
JCS over the digest subject; a closed admitted value-class set (object, array,
string, integer, boolean, null — non-integer and out-of-range numbers refused,
unpaired surrogates refused); SHA-256 rendered as `sha256:` plus 64 lowercase
hex, every digest algorithm-tagged.

**That file invites exactly this movement, in writing**, verbatim:

> A LATER TRANCHE ADDS NO SECOND RULE. Any digest a later tranche introduces is
> computed under this construction, with its subject added to the enumeration
> below; a second construction declared beside this one is a defect whatever it
> is called.

**And the invitation has already been taken from OUTSIDE the family**, which is
what makes this packet's route precedented rather than novel. From the same
file's `digest_subject` enumeration, verbatim:

> ADDED AT TRANCHE THREE (`add-cpc-clearing-boundary`, realized by the neutral
> `contracts/clearing/` family) — ONE SUBJECT, NO SECOND CONSTRUCTION, which is
> exactly the movement this file's own header sanctions. That packet's MODIFIED
> requirement says it in its own words: the manifest's digest and the origin
> signature over it "SHALL use the estate's canonical JSON construction
> `xfc-jcs-sha256-1`, which requires the manifest to be admitted as a SUBJECT of
> that construction's closed `digest_subject` enumeration — a tranche widening
> of SUBJECTS, never a second construction ... Until that subject exists, this
> requirement is UNREALIZABLE as written and SHALL NOT be reported as
> satisfied." This member is what makes it realizable.

**So R7 is encoded as ADOPTION BY REFERENCE plus ONE enumeration member
(`holder_composition`), not as a second JCS profile.** Declaring a second
profile would not literally violate the promoted requirement — that requirement
scopes itself to `signed-execution-chain` — and this packet does not overclaim
otherwise. What it would do is reproduce the SAME defect one layer up: two JCS
profiles in one estate, free to drift in their value-class rules, with no
requirement anywhere obliging them to agree. The promoted text names the cost
in its own voice: *"two readers serializing the same record differently derive
different digests, and neither can verify the other."*

**This is also why this packet declares a real `code_surface` and not `none`.**
A `digest_subject` member is a contract artifact's bytes.

## What this changes, ruling by ruling

Each ruling below is quoted VERBATIM from `rulings-2026-08-29.md` § Packet 4.
**Nothing here is paraphrased, extended, narrowed or invented**, and where a
ruling leaves something open it is put as an open question rather than
answered in the delta.

### R6 — what `model_version` digests

> **R6 — `model_version` digests the PROVIDER PLANE plus the exact published
> identifier.** This closes the residual §5 narrowed from D5: the plane sits
> INSIDE the digest, because the same immutable model does not carry the same
> string across planes and a pin is a pair. Execution and deployment identity
> (account, region, deployment, endpoint, authentication) stays OUTSIDE
> composition and is carried by REFERENCE to the Packet 2 evidence record,
> keeping the DRIFT blast radius where the report's default puts it. Effort,
> reasoning and thinking settings are generation parameters and belong under
> the Parameters component, not under `model_version`.

→ ADDED requirement *"A holder composition's model component digests the
provider plane together with the exact published identifier"*. **OQ-4** decides
whether this reading applies prospectively or retroactively.

### R7 — canonical serialization

> **R7 — Canonical serialization: JSON Canonicalization Scheme (RFC 8785).**
> The digest is `sha256:<lowercase-hex>`, recorded together with the
> canonicalization profile name and its version. This selects the named
> profile report §5 left open between JCS, canonical CBOR and another named
> profile; digest agility and any dual-digest transition remain open and
> belong to the carrying change.

→ ADDED requirement *"One digest construction governs a holder composition, and
it is the estate's existing one"*. **This packet IS "the carrying change"** the
ruling's last clause names, so **OQ-3** answers the digest-agility and
dual-digest question rather than leaving it open a second time.

### R8 — re-issuance record grammar

> **R8 — Re-issuance record grammar: the five fields are the MINIMUM.** A
> re-issuance act records the superseding grant reference, the superseded
> grant reference, the composition hash issued against, the ratifying human,
> and the effective time. The S5 implementer proposed these fields; this
> ruling adopts them as a floor a carrying change may extend, and NOT as a
> ceiling. It does not make them an already-required record format before
> that change is ratified.

→ ADDED requirement *"A re-issuance act records five fields as a MINIMUM, and
the floor is not a ceiling"*. **This packet exercises no extension** — the five
stand exactly as ruled and no sixth field is minted — so the "may extend"
permission is recorded rather than used, and no open question is put on it.

### R9 — in-flight behavior

> **R9 — In-flight: a revoked holder PARKS the convening with a named
> refusal.** No grandfathering. An earlier admission stamp is not honored by
> an exercise that detects a composition mismatch. A parked convening resumes
> only under a new human-ratified issuance act — never by the runtime, never by
> elapsed time. This is the direction task 7.7's gate text already describes,
> ruled so the runbook is written against a settled target.

→ ADDED requirement *"A revoked holder parks the convening, and only a new
human-ratified issuance resumes it"*.

### R10 — retrieval-corpus drift

> **R10 — Retrieval-corpus drift invalidates on IDENTITY or GOVERNING
> CONFIG, not on rows.** A change to corpus identity, or to the governing
> configuration digest (scope, selection configuration, admission policy,
> ontology package digest), invalidates the composition. A row-level content
> change inside the same governed corpus does not, by itself, invalidate.
> The binding remains to the pinned seat prompt and the pinned ontology
> package, and never to the candidate repository at HEAD.

→ ADDED requirement *"Retrieval-corpus drift invalidates on identity or
governing configuration, never on rows"*. **OQ-9** decides whether the four
named members are a CLOSED set or a MINIMUM.

### R11 — lifecycle roles

> **R11 — Lifecycle roles table adopted as proposed** (report §5 "Lifecycle
> Roles"): `propose → approve → attest → register → activate → revoke`, with
> REGISTER as the ONLY human-ratified act; REVOKE requires no human, because
> the cascade is fail-closed and a fail-closed cascade must not wait on a
> human; and RE-ISSUE always requires one. This is consistent with the
> 2026-08-26 Q8(a) ruling that re-issuance is always an explicit register
> act.

→ ADDED requirement *"Register is the only human-ratified act in the lifecycle,
revoke waits on no human, and re-issue always requires one"*.

### R12 — attestation-envelope signer

> **R12 — Attestation-envelope SIGNER: DEFERRED to the
> signed-execution-chain change** (staged; PR #452). Composition digests MAY
> be recorded UNSIGNED in the register in the meantime, and activation stays
> fail-closed on digest match, so the deferral narrows what is claimed
> rather than opening a window. The per-seat Ed25519 keys minted 2026-08-28
> are NOT to be used for self-attestation: a holder signing its own
> composition attests nothing an independent party can rely on. Report §5's
> remaining envelope questions — standard, key distribution, signature
> algorithm, evidence-retention location — travel with that change.

→ ADDED requirement *"An unsigned composition digest is admissible in the
interim, and a holder MUST NOT attest its own composition"* — **the interim
half only**. The signer, envelope standard, key distribution, signature
algorithm and evidence-retention location are NOT encoded here; they travel
with `signed-execution-chain`, exactly as ruled. **OQ-5** is where the
interim-versus-defer-the-whole-ruling split is put for ruling.
**STATUS NOTE, measured:**
R12 names the target as "staged; PR #452". That change has since **ratified and
ARCHIVED** — `openspec/changes/archive/2026-08-31-add-signed-execution-chain/`
— and `openspec/specs/signed-execution-chain/spec.md` is promoted. The deferral
target therefore EXISTS as canon, which is what makes deferring to it a
reference rather than a promise.

## What this packet does NOT do

- **It ticks nothing in `add-wallet-carried-review-authority`.** 7.6 lives in
  that change's ledger, a sibling lane is ticking its S3/S5 rows, and a change
  does not reach into another change's task list. What discharges Ground 1 is
  THIS packet's ratification (OQ-6).
- **It touches no file under `governance/review-authority/`.** No register row,
  no grant, no wallet, no custody attestation. It issues, revokes, re-issues,
  repoints and voids nothing.
- **It performs no register act and no runbook walk.** Both walks already
  exist and are cited as evidence, not repeated.
- **It does not resolve the gate-rules chain's live state.** `grant-grc-0002`
  has been VOID since codexFactory PR #439 → `eff9ae19` merged
  2026-09-12T15:59:10Z; `grant-grc-0003` is PRE-STAGED and unmergeable in
  openxFactory PR [#1006](https://github.com/opensoft/openxFactory/pull/1006)
  pending Brett Heap's host-side key mint. **This packet writes requirement
  text and one contract enumeration member; it edits none of those files and
  is not sequenced against that act's merge** (OQ-7).
- **It declares no second digest construction** (§ The measurement, above).
- **It cuts no contract bundle and reserves no bundle number.**

## Open questions

Nine, each with a RECOMMENDED option marked **(a)** and the reason.
**Taking every recommendation moves not one byte of the delta.**

**OQ-1 — Home capability for R6–R12.**
- **(a) RECOMMENDED — `review-authority-intake`, delta class `## ADDED`.**
  Forced rather than preferred: that capability has NO promoted specification
  (both changes that author it — `add-wallet-carried-review-authority` and
  `register-gate-rules-council-seats` — are ACTIVE and neither has archived),
  so there is no requirement to `## MODIFIED`, and it is the capability whose
  register, grants and re-issuance acts these rulings govern.
- (b) A new capability, e.g. `holder-composition`. Rejected as recommended: it
  would split the register's grammar across two specifications with no rule
  obliging them to agree.
- (c) Split — R6/R7 to `signed-execution-chain`, R8–R12 to
  `review-authority-intake`. Rejected as recommended: `signed-execution-chain`
  is promoted, so R6/R7 would become a `## MODIFIED` of shipped canon to carry
  a subject that capability does not compute.

**OQ-2 — How R7 is satisfied.**
- **(a) RECOMMENDED — adopt `xfc-jcs-sha256-1` BY REFERENCE and widen
  `digest_subject` by one member (`holder_composition`).** It is literally R7's
  ruled profile (RFC 8785 JCS, `sha256:` + lowercase hex, named and versioned),
  the file's own header invites it, and `add-cpc-clearing-boundary` already took
  that route from a different capability.
- (b) Declare a second JCS profile for composition digests. Rejected: two JCS
  profiles free to drift on value-class rules, with nothing obliging agreement.
- (c) Leave the profile abstract ("an RFC 8785 profile") and name none.
  Rejected: it reproduces the defect the promoted requirement exists to close —
  agreement mandated, serialization unnamed.

**OQ-3 — Digest agility and dual-digest transition** (R7 leaves these "open"
and assigns them to "the carrying change", which is this packet).
- **(a) RECOMMENDED — NO agility mechanism is minted now.** Every digest is
  ALGORITHM-TAGGED and the profile name and version are RECORDED, which is
  precisely what makes a later migration a readable change; a transition
  mechanism with no second algorithm to transition to is a widening nothing
  exercises. State that in terms so a reader knows it was decided.
- (b) Declare an agility register (permitted algorithms + selection rule) now.
- (c) Declare a dual-digest transition window now.

**OQ-4 — Does R6 apply PROSPECTIVELY or force re-derivation?** *(the one that
can revoke live grants)*
- **(a) RECOMMENDED — PROSPECTIVELY.** The requirement binds compositions
  declared or re-declared AFTER this packet's realization; composition digests
  that live grants were issued against are not re-derived by this act, and the
  next genuine composition event re-derives them under the ruled reading in the
  ordinary way. Reason: a retroactive re-derivation would change the digest
  every active grant is bound to, and under the shipped drift cascade a changed
  composition REVOKES — so option (b) would revoke both councils' authority as
  a side effect of a doctrine packet, on a day when `grant-grc-0002` is already
  void and `grant-grc-0003` cannot yet be minted.
- (b) Retroactive re-derivation, performed as its own register act.
- (c) Prospective now, plus a NAMED reconciliation task in this packet's § 3.

**OQ-5 — How much of R12 is encoded here.**
- **(a) RECOMMENDED — encode the INTERIM half only.** Unsigned composition
  digests admissible; activation fail-closed on digest match; the per-seat
  Ed25519 keys refused for self-attestation. Envelope standard, key
  distribution, signature algorithm and evidence-retention location travel with
  `signed-execution-chain`, exactly as R12 says.
- (b) Encode nothing of R12 here; defer the whole ruling.  Rejected: R12's
  interim sentences are enforceable statements, and leaving them unencoded
  leaves self-attestation unrefused.
- (c) Encode the signer here too. Rejected: it contradicts the ruling's own
  words.

**OQ-6 — Who discharges 7.6 Ground 1, and who ticks 7.6.**
- **(a) RECOMMENDED — ratification of THIS packet discharges Ground 1; the tick
  in `add-wallet-carried-review-authority/tasks.md` is the PARENT's act, on a
  separate word, performed by the lane holding that ledger.** This packet
  records the discharge and ticks nothing there.
- (b) This packet edits the parent's `tasks.md` and ticks 7.6 itself. Rejected:
  a sibling lane is actively ticking those rows, and two lanes editing one
  ledger is the collision the lane protocol exists to prevent.
- (c) Ground 1 is discharged only on this packet's ARCHIVE, not its
  ratification. Rejected as recommended: the ground's own words are *"until the
  change carrying R6–R12 is **ratified**"*.

**OQ-7 — Ratification ordering against the pending gate-rules act.**
- **(a) RECOMMENDED — not sequenced against it.** This packet edits no
  `governance/review-authority/` file and no file PR #1006 touches, so the two
  can land in either order. `sequenced_after:` declares the two CAPABILITY
  AUTHORS plus the sibling runbook amendment, which is a realization-axis
  declaration and not a merge queue.
- (b) Hold ratification until #1006 merges and `grant-grc-0003` is ACTIVE.
- (c) Hold ratification until the parent's S3/S5 bookkeeping lands.

**OQ-8 — Realization surface and archive gate.**
- **(a) RECOMMENDED — declare the surface named in the front matter and archive
  on merged-plus-green realization evidence**, per `release-realization`, with
  the openXwallet reader advance and pin bump named as the enforcing half and
  NOT performed here.
- (b) File as `code_surface: none` and archive on landing. Rejected: a
  `digest_subject` member is a contract artifact's bytes, and filing that as
  `none` is a false declaration.
- (c) Split — a doctrine packet now (`none`) and a separate contract packet
  later.

**OQ-9 — R10's governing-configuration members: closed set or minimum?**
- **(a) RECOMMENDED — the four named members (scope, selection configuration,
  admission policy, ontology package digest) are REQUIRED, and a corpus MAY
  declare further members that also invalidate.** Reason: this mirrors R8's own
  floor-not-ceiling shape, and reading the four as CLOSED would mean a governed
  corpus could add a new governing knob that silently never invalidates.
- (b) Exactly four, closed.
- (c) Four required, further members permitted but non-invalidating.

## Rulings

**Brett Heap, 2026-09-12T23:58Z, verbatim "accept all A on 1017"** — given in
session directly to the ENCODE seat of lane `hermes-wallet-exercise` (window
`hermes-wallet-exercise`, session `codeXfactory-2`, workstation Eagle), and
captured in full at `review/ratification-2026-09-12.md`. The word reaches all
nine decisions this packet put, each at its RECOMMENDED option, so **the
delta's wording stands unchanged**: not one byte of
`specs/review-authority-intake/spec.md` moves.

| OQ | Decision | Ruled | Considered, not adopted |
| --- | --- | --- | --- |
| **OQ-1** — home capability for R6–R12 | `design.md` D-1 | **RESOLVED (a)** — `review-authority-intake`, delta class `## ADDED` (forced: no promoted spec exists, both authoring changes are ACTIVE) | (b) a new `holder-composition` capability — splits the register's grammar across two specifications with no rule obliging agreement; (c) split R6/R7 into `signed-execution-chain` — would make R6/R7 a `## MODIFIED` of shipped canon to carry a subject it does not compute |
| **OQ-2** — how R7 is satisfied | `design.md` D-2 | **RESOLVED (a)** — adopt `xfc-jcs-sha256-1` BY REFERENCE plus one `digest_subject` member (`holder_composition`) | (b) declare a second JCS profile — two profiles free to drift, nothing obliging agreement; (c) leave the profile abstract and name none — reproduces the defect the promoted requirement exists to close |
| **OQ-3** — digest agility / dual-digest transition | `design.md` D-3 | **RESOLVED (a)** — no agility mechanism is minted now; algorithm tagging plus a recorded profile name and version is what makes a later migration a readable change | (b) declare an agility register now; (c) declare a dual-digest transition window now |
| **OQ-4** — R6's temporal reach *(the one that can revoke live grants)* | `design.md` D-4 | **RESOLVED (a)** — PROSPECTIVE; composition digests live grants were issued against are not re-derived by this act | (b) retroactive re-derivation — under the shipped drift cascade this REVOKES `grant-mrc-0002`, on a day `grant-grc-0002` is already VOID and `grant-grc-0003` cannot yet be minted; (c) prospective plus a named reconciliation task — no reconciliation is owed |
| **OQ-5** — how much of R12 is encoded here | `design.md` D-5 | **RESOLVED (a)** — the INTERIM half only: unsigned composition digests admissible, activation fail-closed on digest match, self-attestation refused | (b) defer the whole ruling — leaves self-attestation UNREFUSED; (c) encode the signer here too — contradicts R12's own words |
| **OQ-6** — who discharges 7.6 Ground 1, and who ticks 7.6 | `design.md` D-6 | **RESOLVED (a)** — ratification of THIS packet discharges Ground 1; the tick in `add-wallet-carried-review-authority/tasks.md` is the PARENT's act, on a separate word | (b) this packet edits the parent's `tasks.md` and ticks 7.6 itself — collides with the sibling lane actively ticking those S3/S5 rows; (c) discharge only on archive — contradicts Ground 1's own words, "ratified" |
| **OQ-7** — ratification ordering against the pending gate-rules act | `design.md` D-7 | **RESOLVED (a)** — NOT sequenced against openxFactory PR #1006 — zero file overlap, measured | (b) hold ratification until #1006 merges; (c) hold ratification until the parent's S3/S5 bookkeeping lands |
| **OQ-8** — realization surface and archive gate | `design.md` D-8 | **RESOLVED (a)** — declare the surface named in the front matter; archive on merged-plus-green realization evidence | (b) file as `code_surface: none` — a FALSE declaration, since a `digest_subject` member is contract artifact bytes; (c) split — a doctrine packet now (`none`) and a separate contract packet later |
| **OQ-9** — R10's governing-configuration members: closed or minimum | `design.md` D-9 | **RESOLVED (a)** — the four named members (scope, selection configuration, admission policy, ontology package digest) are REQUIRED, and a corpus MAY declare further invalidating members | (b) exactly four, closed — a corpus could add a new governing knob that silently never invalidates; (c) four required, further members permitted but non-invalidating |

**EVERY RULING IS THE RECOMMENDED OPTION.** No requirement text was rewritten,
no delta directory was renamed, and no `sequenced_after:` entry moved. This
packet is `Status: ratified`; realization (§ 3) and archive (§ 5) are separate
acts on separate words, and neither has been given — `tasks.md` § 5 stays
entirely open, held behind the three parents named in `sequenced_after:`.

