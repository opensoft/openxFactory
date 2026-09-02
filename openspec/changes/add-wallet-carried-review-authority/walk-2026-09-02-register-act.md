# Walk record — the 2026-09-02 REGISTER ACT, against `docs/governed-reissuance-runbook.md`

Status: record
Kind: report
Repository context: openxFactory
Walked: 2026-09-02
Runbook walked: [`docs/governed-reissuance-runbook.md`](../../../docs/governed-reissuance-runbook.md)
  — `Status: draft`, steps **5**, **§5.1**, **step 5b (§5.2)** and **§7**
The act: **the human-ratified REGISTER ACT** — sequencing step 5 of
  [`rulings-2026-08-29.md`](rulings-2026-08-29.md)
Ratifying human: **Brett Heap** (`Brett.Heap@opensoft.one`)
Effective instant: **`2026-09-02T13:33:48Z`**
Predecessor walk: [`walk-2026-08-31-composition-bump.md`](walk-2026-08-31-composition-bump.md)
  (steps 0–4 and §6.1; steps 5, §5.1 and 5b explicitly NOT performed there)

---

## 0. THE HEADLINE, BEFORE THE DETAIL

**The register act was performed.** `grant-mrc-0001` is revoked for **DRIFT** on
the 2026-08-31 composition change; `grant-mrc-0002` is issued against the changed
composition at the same instant; `row-mrc-0001` is repointed onto it; no row was
added; and the signed Operator identity record is carried to its first governed
home in the same change.

**And it did NOT land green, for a reason that is a real defect in the pinned
reader and not a defect in this act.** §9 records it in full, with the
measurement, the minimal remedy, and the reason no workaround was taken. **Read
§9 before merging anything.**

**What is NOT done, and neither is a formality:**

* **STEP 5b IS NOT DONE BY THIS ACT** (§8). The register act does not reach the
  runtime by itself. **Until the projection is re-derived, the runtime keeps
  refusing with `review_authority.root_key_mismatch` and NO AUTHORITY FLOWS.**
* **"VERIFY ONE CONVENING ADMITS" IS NOT PERFORMED** (§8.3), and cannot be:
  **no real convening has ever run in this estate.**

---

## 1. What each step produced

Each row says what the step PRODUCED. A tick would say only that somebody looked.

| Runbook step (the runbook's own labels) | Exercised? | What it produced |
|---|---|---|
| **§0.3 who holds which act** | yes | §7 — **three capacities in one human, disclosed and not collapsed**, plus the previously disclosed Lead-Quality conflict |
| **§1 superseded state** | yes, **quoted from the predecessor walk** | §2 — the grant and the row as they stood, quoted rather than remembered |
| **§2 the bump** | **inherited, not re-performed** | §2.2 — codexFactory `6edecaf1`, and the tests that proved it green-whole/red-partial |
| **§3 in-flight (R9)** | **NO — vacuously, again** | §8.3 — nothing was in flight because nothing convenes. A vacuous non-exercise is recorded as one |
| **§4 R8 five fields** | yes — **now COMPLETE** | §4 — the two fields the predecessor walk left PENDING are filled; the third stays PENDING R6/R7 with its substitute labelled |
| **§5 the register act** | **YES — PERFORMED** | §5 |
| **§5.1 revoke / mint / repoint / do-not-add** | **YES — three writes and one non-write, one change** | §5 |
| **§5.2 (step 5b) the projection** | **NO** | §8 — what it would take, named, and what it costs until then |
| **§5.2 "verify one convening admits"** | **NO — impossible today** | §8.3 |
| **§7 record the act** | yes | This document |

---

## 2. Step 1 — the superseded state

### 2.1 What was ended, quoted

Quoted from [`walk-2026-08-31-composition-bump.md`](walk-2026-08-31-composition-bump.md)
§2.3, which established it BEFORE anything was edited — which is the whole point
of step 1, and why this record quotes that one rather than reconstructing the
state after the fact:

```yaml
grant_id: grant-mrc-0001
audience: {wallet_ref: wal-agent-mrc-0001, holder_ref: agent:merge-readiness-council}
scope: {acts: [review], objects: [opensoft/openxFactory], authority_tier: act}
expires_at: "2026-11-23T12:00:00Z"
issued_at:  "2026-08-25T12:45:00Z"
issued_by:  Brett.Heap@opensoft.one
state: active
```

and the backing row, **as a set of all nine fields**, because the reader enforces
exact set equality over them: `row_id: row-mrc-0001`,
`holder_ref: agent:merge-readiness-council`, `wallet_ref: wal-agent-mrc-0001`,
`target_repo: opensoft/openxFactory`, `act: review`, `authority_tier: act`,
`grant_ref: grant-mrc-0001`, `expires_at: "2026-11-23T12:00:00Z"`,
`state: active`.

That walk recorded both files **byte-identical after it ran**. They were still
byte-identical at the head this act branched from, so the state ended here is the
state established there — not a later one nobody wrote down.

### 2.2 The step-2 bump's identity — INHERITED

**The bump: codexFactory `6edecaf13e88fc56f9a7182b93a0d48cc2e40541`, the MERGE
COMMIT of PR #146.** Stated precisely, because the two obvious ways to name it
disagree by one line and one second.
`gh api repos/opensoft/codexFactory/commits/6edecaf13e88fc56f9a7182b93a0d48cc2e40541`
returns that sha with a commit message whose **first line** is *"Merge pull
request #146 from opensoft/change/s5-roster-flip-2026-08-31"* and whose **body**
is the roster title *"The enrolled roster's aliases become exact provider
pins"* — so the title this record uses is the message BODY, not the subject the
commits API leads with. The instant is **`committer.date`
2026-08-31T07:36:33Z**; PR #146's own `mergedAt` is **2026-08-31T07:36:34Z**
(`gh pr view 146 --repo opensoft/codexFactory --json title,mergedAt,
mergeCommit`, which also confirms `mergeCommit` is that sha and the PR title is
the body line). **The one-second gap is the two APIs' stamps of one event, not
two events.**

The roster's `model_version` component moved from mutable provider aliases
(`opus`, `sonnet`) to exact identifiers (`claude-opus-5`, `claude-sonnet-5`).
**Exactly one of six declared components moved** — measured, per-component, in the
predecessor walk's §2.2 — and one is sufficient: *"WHEN any single component of
the declared set changes, THEN the change alone is sufficient to revoke."*

The tests the predecessor walk names as proof that the commit set is **green
whole and red partial**, reproduced here so this record does not send a reader to
find them:

* domain roster flipped, tenant not → `test_R23_the_domain_roster_is_bound_to_the_tenant_declaration` **red**;
* tenant flipped, domain not → the same test **red**;
* a one-seat partial flip → `test_the_enrolled_seat_roster_is_the_recorded_map` **red**;
* 21 mutations, each anchor-checked before mutating, **all red**; two vacuity
  probes; two must-stay-green tests green and unmodified.

Green whole: codexFactory CI `validate` on `main` after the merge — **1657
passed, 12 skipped** (run `33369133430`).

**This act does not re-perform the bump and claims no credit for it.**

---

## 3. THE THREE CITATIONS THIS REGISTER ACT IS FIXED AT

The chain is not this act's invention. It was fixed by the convener at
codexFactory `hermes/domain/review-councils/records/2026-09-01-s5-seat-model-soak-run3.md`
**in the ruling itself, §12.1**: the clause *"cites this activation ruling
+ the roster-change record + the still-owed R5 Operator identity record"* is
part of the convener's own transcribed sentence, inside §12.1's block quote
(lines 776–778 of the fetched bytes) — **not §12.4's**, which is where this
record previously attributed it. **§12.4 is the record's RESTATEMENT** of that
citation set as a three-row table, per run-2 §12.3, and §12.4 is what carries the
consequence: at that moment **one of the three did not exist**, and §12.4 said
so in terms: *"One of the three does not exist, so the register act cannot yet
be taken, and no authority continues until it is."* Both sections are cited
here because they say different things and only one of them is the ruling.

**All three now exist. Each was verified, and the verification method is recorded
rather than the conclusion alone.**

### (i) THE ACTIVATION RULING

**Where:** codexFactory
`hermes/domain/review-councils/records/2026-09-01-s5-seat-model-soak-run3.md`,
**§12.1 "THE ACTIVATION RULING"**. Landed in **PR #155**, merge commit
**`fd4319aa1ed857557f559611fe7652fb37272003`**, merged **2026-08-31T16:33:18Z**,
titled *"Record the S5 soak run 3: the LA-C3 completion round — 5 of 6, the C9
inverse clean, DA-3's question routed to #154"*.

**Verified how:** the record's bytes were fetched with
`gh api repos/opensoft/codexFactory/contents/hermes/domain/review-councils/records/2026-09-01-s5-seat-model-soak-run3.md`
and §12.1 read directly; PR #155 and commit `fd4319aa` were resolved with
`gh pr view 155` and `gh api …/commits/fd4319aa`, both returning the sha, title
and merge instant above.

**The ruling's operative sentences, quoted.** The attribution is the record's
own, at its §12 header, and is reproduced in its order rather than reflowed:
*"Brett Heap, convener, 2026-09-01, in session."*

> `lead-integration`'s activation hold (LA-C3) is DISCHARGED and the seat is
> ACTIVATED into the same posture as the other three conditional selections.
> … The one miss (DA-3) is adjudicated **DUTY PERFORMED UNDER A FLAWED
> INSTRUCTION** … and is carried as a **WATCH ITEM attached to issue #154** …
> it does not block activation. **THE ACTIVATION IS NOT ISSUANCE**: the REGISTER
> ACT — the convener's, separately, citing this activation ruling + the
> roster-change record + the still-owed R5 Operator identity record — **remains
> the gate before any authority continues.**

**What it does NOT license, in its own words:** the activation is **not**
issuance. This act is the issuance the ruling names as the remaining gate; it is
not licensed by the activation and does not inherit anything from it beyond the
citation.

### (ii) THE ROSTER-CHANGE RECORD

**Where:** codexFactory
`hermes/domain/review-councils/records/2026-08-31-enrolled-roster-model-pin-flip.md`.

**Verified how:** fetched by `gh api …/contents/…` and read; **§2** carries the
re-pinned four-seat roster (`lead-security` → `claude-opus-5`, `lead-integration`
→ `claude-opus-5`, `lead-quality` → `claude-sonnet-5`, `company-policy-lead` →
`claude-sonnet-5`, the last a TENANT declaration the domain roster consumes), and
**§10** carries the Lead's acceptance route
`roster_change: lead_accepted_recorded`, **PERFORMED** and quoted verbatim in
that section.

**The conflict that record discloses travels onto this act** and is repeated at
§7 below rather than left behind: the accepting Lead is **Lead Quality**, which
is also a **SUBJECT** of the selection. The record chose **disclosure over cure**
and so does this one.

### (iii) THE OPERATOR IDENTITY RECORD

**Where, now:**
[`operator-identity-record-2026-09-01.md`](operator-identity-record-2026-09-01.md),
in this change directory — **carried here BY THIS ACT**, which is its first
governed home. Before this commit it existed only as a scratchpad copy, and its
own header said so.

**Verified how:** the signed source was copied **byte-identical** (MD5
`b82fd26d73f3b2f5c061eaef6b77d588` on both source and copy, compared after the
copy), and the source file was **not modified** — re-hashed afterwards and
unchanged. The record is **SIGNED by the Operator (Brett Heap) 2026-09-01**,
in-session, with the signature block at its §8.

**What it evidences, and the one thing it must not be read as evidencing:** the
**plane** is **EVIDENCED BY READ-BACK** — EXE-1/EXE-2, xFactory run
**33577170272** — and never inferred from the transport. R5's error is reading a
Claude Code transport as evidence of a direct-Anthropic plane, and the record
does not commit it: its §3.1 states in terms that the drafter's own runs cannot
evidence the plane and why.

**The version of record:** **`2.1.206`**, ruled by the Operator in session on
2026-09-02 and appended to the record as its
*"Addendum 2026-09-02 — Operator ruling: the version of record"* — the
WORKER-resolved version (EXE-6, xFactory run **33513966619**, artifact lane,
service account **`svc-omniworker`**). The workstation soak's **2.1.251** and the
2026-08-22 corpus's **2.1.239** are the drafter's transport and remain on record
as the single named deviation (§3.1), **not** the version of record; the coding
lane's **2.1.207** skew is carried as §8 EXE-6 states it. **That ruling is not a
pin and enforces nothing** — the runtime is not one of the six declared
components.

**The addendum is APPENDED. Nothing above the signature was edited**, and §5's
`Proposed issuance / grant reference` row still reads **PENDING** on purpose: it
records the state at signature, which is the only state a signed record may
assert. The answer — `grant-mrc-0002` — is recorded beneath the signature and
here.

**AND ITS FROZEN `Status:` HEADER IS KNOWINGLY STALE, LEFT THAT WAY ON PURPOSE.**
The record's header block still reads *"this is the scratchpad copy — NOT YET
committed to a governed repository; the register act carries it there"* — which
this commit makes untrue the moment it lands. It is **not corrected**, because
it sits above the signature and the whole discipline of a signed record is that
signed text is not edited afterwards. It also raises no doc-health finding: the
block is INDENTED, and the checker's `STATUS_RE` is `^Status:\s*(.+?)\s*$`
(`scripts/doc_health/corpus.py:110`), anchored at column zero, so an indented
`Status:` is not a status line to it; the file additionally sits under
`openspec/changes/`, outside the governed prose roots. **The stale sentence is
resolved by the 2026-09-02 addendum beneath the signature**, which records where
the record now lives — the append is the correction, and the header is left as
the artifact of what was true when it was signed.

---

## 4. Step 4 — the R8 five-field record, COMPLETE

> **R8 — the five fields are the MINIMUM.** *"A re-issuance act records the
> superseding grant reference, the superseded grant reference, the composition
> hash issued against, the ratifying human, and the effective time … a floor a
> carrying change may extend, and NOT a ceiling."*
> — [`rulings-2026-08-29.md`](rulings-2026-08-29.md) R8

**The predecessor walk left two of the five PENDING. Both are now filled. This is
the return trip its §4 required.**

| R8 field | Value |
|---|---|
| **superseded grant reference** | **`grant-mrc-0001`** — root grant, issued 2026-08-25T12:45:00Z by `Brett.Heap@opensoft.one`, backing `row-mrc-0001`; now `state: revoked`, reason class **DRIFT** |
| **superseding grant reference** | **`grant-mrc-0002`** — *was* PENDING; minted by this act. Root grant (no `parent_grant_ref`) |
| **composition hash issued against** | **STILL PENDING R6/R7 — and it is filled with a SUBSTITUTE, EXPLICITLY LABELLED ONE.** See below |
| **ratifying human** | **Brett Heap** (`Brett.Heap@opensoft.one`), the anchored responsible operator under the Human Escalation Contract |
| **effective time** | **`2026-09-02T13:33:48Z`** — *was* PENDING. One instant, taken once, written into all three places |

### 4.1 The composition hash — why it is still PENDING, and what stands in for it

**NO CANONICAL DIGEST IS IMPLEMENTABLE YET, AND NONE WAS INVENTED.** R6 (the
plane sits INSIDE the digest) and R7 (JCS / RFC 8785, `sha256:<lowercase-hex>`,
recorded with the canonicalization profile name and version) are **ratification
targets**: *"none of them is implementable until the change that carries them is
authored and ratified."* That change is **not authored**.

**Recorded instead, as the runbook's §1 prescribes — A SUBSTITUTE, SO LABELLED:**

1. **The declaring commit.** codexFactory
   **`6edecaf13e88fc56f9a7182b93a0d48cc2e40541`**, plus the per-component
   substitute digests the predecessor walk's §2.2 computed at it (definition and
   the six before/after values are there, with `model_version` the one that
   moved: `sha256:3ff506b8af0c…` → `sha256:a5c245462beb…`).
2. **The roster's own declared digest.** codexFactory
   `hermes/domain/agent-mixes.yaml` `rendered_set_digest`
   **`sha256:751e03a203fd5cef59f0e4873fc910ef6c2c501e60472ea54791ad77fda7c92a`**
   — read back from the live file at the time of this act and matching the value
   the Operator identity record's §5 carries.

**BOTH ARE SUBSTITUTES AND NEITHER IS THE R6/R7 DIGEST.** A locally-invented
digest recorded in the hash's place is worse than an empty field, because a later
reader cannot tell the two apart. Neither value covers the provider plane, which
is exactly what R6 says the real digest must cover.

### 4.2 Beyond the minimum — what this act actually carries

R8 is a floor, and adding is the ruling working as intended:

* **the three citations** of §3, each verified to exist;
* **the supersession, IN PROSE** — `grant-mrc-0002` supersedes `grant-mrc-0001`.
  **No field carries this.** The pinned grant schema
  (openXwallet `contracts/openxwallet/openxwallet-grant.schema.yaml`) is
  `additionalProperties: false` and has **no `supersedes` key**;
  `parent_grant_ref` means **derived from**, a different relation, and was not
  borrowed. So the relation lives in this record, in `grant-mrc-0002`'s header
  and in `grant-mrc-0001`'s appended revocation comment — and nowhere else,
  exactly as the runbook's §5.1 "HONEST LIMIT" says it must;
* **the expiry ruling and the merge ruling**, as spoken — §6;
* **the conditions still outstanding**, unchanged: the selection remains
  **CONDITIONAL** (no seat returned an unqualified SELECT); six of run 2's
  residual judgments are untouched; DA-3 is a live watch item on codexFactory
  issue **#154**.

---

## 5. Step 5 — the acts, verbatim

**Three writes and one non-write, in ONE change**, per the runbook's §5.1. There
is no ordering of the three that is green halfway, which is why they are one
change.

### 5.1 REVOKE — `grant-mrc-0001`, in place

| | |
|---|---|
| **File** | `governance/review-authority/grants/grant-mrc-0001.yaml` |
| **`state`** | `active` → **`revoked`** |
| **`revocation.revoked_at`** | **`2026-09-02T13:33:48Z`** |
| **Reason class** | **DRIFT** |

**`revocation.reason`, verbatim:**

> DRIFT: declared composition change — the enrolled roster's model pins moved
> from mutable provider aliases (opus, sonnet) to exact identifiers
> (claude-opus-5, claude-sonnet-5); codexFactory
> 6edecaf13e88fc56f9a7182b93a0d48cc2e40541,
> records/2026-08-31-enrolled-roster-model-pin-flip.md, 2026-08-31. A declared
> composition change ends this holder's certified identity at once, with no
> tolerance band and no grace period. Re-issued as grant-mrc-0002 by the register
> act of 2026-09-02 (walk-2026-09-02-register-act.md). Terminal: this grant never
> returns to active.

**The reason NAMES THE COMPOSITION EVENT** because *"a revocation whose reason
does not name what caused it is indistinguishable from an outage"*, and because
the ratified scenario *"declaring the change is not performing it"* makes an
unnamed revocation a validation failure in its own right.

**DRIFT propagates exactly as CAUSE** — *"no derived authority survives on the
strength of its parent's reason."* **No derived grant exists**: `grant-mrc-0001`
is a root grant and no grant in this tree declares it as `parent_grant_ref`
(checked). So the propagation is vacuous here, and is recorded as vacuous rather
than as satisfied.

**TERMINAL, NOT SUSPENDED.** The header comment appended to the file says so and
says why: *"A revoked grant SHALL NEVER return to the active state"* — the
grant was **replaced**, never revived. **Nothing above the file's existing header
comment was rewritten**; the revocation note is appended beneath it and dated.

### 5.2 MINT — `grant-mrc-0002`

| Field | Value |
|---|---|
| `grant_id` | **`grant-mrc-0002`** |
| `audience.wallet_ref` / `audience.holder_ref` | `wal-agent-mrc-0001` / `agent:merge-readiness-council` — **unchanged** |
| `scope.acts` | `[review]` — carried forward, re-examined (below) |
| `scope.objects` | `[opensoft/openxFactory]` — carried forward, re-examined |
| `scope.authority_tier` | `act` — carried forward, re-examined |
| `scope.approval_posture` | identical to `grant-mrc-0001`'s, byte for byte |
| `issued_at` | **`2026-09-02T13:33:48Z`** |
| `issued_by` | **`Brett.Heap@opensoft.one`** |
| `expires_at` | **`2027-06-30T00:00:00Z`** |
| `state` | `active` |
| `parent_grant_ref` | **ABSENT — this is a ROOT grant.** `parent_grant_ref` means DERIVED FROM, and a superseding grant is not derived from the one it replaces |

**THE SCOPE WAS RE-EXAMINED, NOT COPIED.** The runbook requires the scope be
*"carried forward deliberately rather than copied without looking"*, so the
reasons are on the file's own face: the composition event changed **which model
sits in each seat** and changed nothing about **what the holder may do**, so
`acts` stands; `objects` stands as the one target the row commissions; tier `act`
stands on an **untouched** custody attestation
(`attestations/custody-attest-wal-agent-mrc-0001.yaml`), without which the
unattested cap would hold this grant at `request`; and `approval_posture` is
unchanged because approval-before-apply is the compensating control that lets
`holder_readable` custody reach tier `act` at all.

**NO GAP BETWEEN REVOCATION AND ISSUANCE.** `revoked_at` and `issued_at` are the
same instant, taken once from `date -u` and written into three files.

### 5.3 REPOINT — `row-mrc-0001`

| Field | Before | After |
|---|---|---|
| `grant_ref` | `grant-mrc-0001` | **`grant-mrc-0002`** |
| `expires_at` | `"2026-11-23T12:00:00Z"` | **`"2027-06-30T00:00:00Z"`** |
| `state` | `active` | **`active` — UNCHANGED** |
| the other six fields | unchanged | unchanged |

`expires_at` is **character-for-character equal** to `grant-mrc-0002`'s, because
the reader compares the two and any drift is a `register-grant-mismatch`.

**The row's own `state` stays `active`** — the row is the authority's continuing
existence, not the grant's. A revoked grant does not deactivate the row that was
repointed off it.

**All four `seat_keys` entries still resolve — checked, not assumed.** All four
name `authorizing_row: row-mrc-0001`; that row is `state: active` and unexpired
at `2027-06-30T00:00:00Z`; and the pinned reader confirmed it, emitting
`intake register: 4 of 4 per-seat signing key(s) adjudicated and resolved` on the
amended tree (§9's run).

### 5.4 THE NON-WRITE — no row was added

**The single-row cap is RETAINED.** It bounds AUTHORITY ROWS — one holder, one
target repository, one act, one tier, one expiry — and a second row for the same
holder and target is refused (`register-minimal-shape-exceeded`). The row still
carries **exactly nine fields**, which the reader enforces as exact set equality.
**The composition was not smuggled onto the row:** there is no model field on a
row, adding one would be refused, and this act added none.

---

## 6. THE RULINGS AS SPOKEN

Brett Heap, in session, 2026-09-02. The operative words were **"A3, B2"**, given
against two enumerated questions. Both are recorded with what the options were,
because a bare letter is not a ruling anyone can audit later.

### 6.1 "2.1.206 is the version of record"

Spoken first, and it is what let the act start: it resolved the open version note
in the Operator identity record (§3(iii)), the third citation. Recorded in full
in that record's own addendum.

### 6.2 "A3" — the expiry

**A3 = `expires_at: 2027-06-30T00:00:00Z`**, bound to the Operator identity
record's review expiry, which is itself bound to **`claude-sonnet-5`'s published
retirement floor** — the earlier of the two pinned seat identifiers' floors. The
grant may not outlive the evidence of the identity it was issued against.

**What A3 was chosen OVER:** a shorter term that would have re-run this whole act
inside the quarter, and a longer one that would have outlived the identity record
that grounds it. The rejected shapes matter because the reason A3 was picked is a
BINDING — the expiry is tied to a named artifact rather than to a convenient
number of days — and that binding is what a later reader needs.

**THE HONEST CAVEAT, and it is the runbook's §6.1 own:** *"nothing in the estate
reads a retirement date, so every one of these is today a promise rather than a
control."* What IS enforced is this date itself: the reader computes expiry at
read time (`register-row-expired`, `grant-state-stale`) and the runtime refuses
past it. **On 2027-06-30 every convening parks — IF AND WHEN A CONVENING RUNS;
none has to date** (§8.3) — with no code change and no deploy to blame.
Re-issuance is an operator act with a lead time; this is where that date is
stated as a **scheduled event**. The sentence describes the control's shape, not
an observed behaviour, and it is written that way so a later reader does not
take "every convening parks" as evidence that convenings happen.

### 6.3 "B2" — how this change merges

**B2 = the coordinator admin-merges on the ratifier's word, with a provenance
comment.**

**Why an admin merge is the CORRECT route here and not a bypass of review.**
`register.yaml` declares on its own face that it is a *"PERMANENTLY HUMAN-ONLY
SURFACE (ratified requirement, explicit here by name): no council verdict may
ever produce an autonomous approval of a change to THIS file"*, and *"a council
whose own commission is recorded here is never eligible to clear a candidate that
edits it."* **The approval for this change is the RATIFIER'S, and it is recorded
here** — in this walk, on the grant's face, and beside the row. There is no
council verdict to obtain, and obtaining one would be the violation.

**What B2 was chosen OVER:** the alternative was a route that would have routed
this candidate through the ordinary clearing lane — which for THIS file is not a
stricter option but an ineligible one.

**This walk's author does not merge.** The act is authored, the record is
written, and the merge is the ratifier's word carried out by the coordinator with
a provenance comment naming it.

---

## 7. CAPACITY DISCLOSURE (runbook §0.3)

**Brett Heap holds THREE capacities in this act, and they are disclosed rather
than collapsed** — the runbook's own instruction: *"If you find yourself about to
perform two of these roles in one motion, stop and disclose it on the record
instead — the 2026-08-22 precedent did exactly that when one human held two
capacities."*

| Capacity | The act held in it | Where it was exercised |
|---|---|---|
| **the OPERATOR** | evidencing exact provider identity and the plane (R5) | the Packet 2 identity record, signed 2026-09-01, and its 2026-09-02 version-of-record addendum |
| **the CONVENER** | accepting the Council's output on record, and the **activation ruling** | codexFactory `records/2026-09-01-s5-seat-model-soak-run3.md` §12.1 |
| **the RATIFYING HUMAN** | **the register act itself** (R11: REGISTER is the only human-ratified act, and RE-ISSUE always requires one) | this change |
| **the COORDINATOR** — the Fable session, **not** the ratifying human | **performing the ADMIN-MERGE** of this change, on the ratifier's word **"B2"**, with the provenance comment that word requires | this pull request, at merge |
| **the AUTHORING AGENT** — an Opus subagent, directed by the coordinator | **COMPOSING THE BYTES** of this act's files: both grant headers, the register row's comment, this walk, the tasks notes | this change directory |

**THE LAST TWO CAPACITIES ARE MACHINE-HELD, AND THEY ARE DISCLOSED FOR THE SAME
REASON THE FIRST THREE ARE.** **The ratifying human did not type the register.**
An agent composed the bytes on the ratifier's word; a coordinating session
carries the merge. Neither is an authority: the authorship is directed, and the
merge is the execution of a ruling already given ("B2", §6.3). But a capacity
table that listed only the human's three would let a reader assume the writing
and the merging were the ratifier's too — and runbook §0.3's whole point is that
roles are named rather than collapsed, which does not stop applying at the
boundary where the holder stops being a person. **What is Brett Heap's here is
the ACT** — the decision to revoke, the reason class, the effective instant, the
expiry ruled as A3, the route ruled as B2. **What is not his is the typing and
the button.**

**Plus the previously disclosed conflict, which does not go away by being old.**
The roster-change record's §10: the accepting Lead is **Lead Quality**, which is
also a **SUBJECT** of the selection — *"the conflict is DISCLOSED here and
travels with the act."* **No cure was attempted and none is attempted here**; a
cure would manufacture a procedure no sitting chartered.

**Why this is disclosed and not treated as an irregularity.** It is the estate's
standing condition — one operator, one code owner — and the honest form is to say
so beside the act rather than to let each capacity be read as a separate check on
the others. **Three capacities held by one human are one check, not three.**

---

## 8. STEP 5b — the projection. NOT DONE BY THIS ACT, and here is exactly what it takes

**Investigated rather than assumed.** The runbook's §5.2 and `register.yaml`'s own
P7D justification both say the projection is established BY HAND and that
*"nothing refreshes the projection automatically today."* **That is no longer
true, and this record corrects it rather than repeating it.**

### 8.1 What mechanism exists — a CronJob, not a heredoc

Searched: `installs/hermes-install` (READ-ONLY) for `register_projection`,
`root_key_mismatch` and `review_authority`, and this repository for the same.
**The local hermes-install checkout sits on a stale branch 157 commits behind
`origin/main` and contains none of it; the machinery is on `origin/main`**, which
is why a search of the working tree alone would have reported "nothing committed"
and been wrong.

What is committed, on hermes-install `origin/main`:

| Artifact | What it is |
|---|---|
| `src/hermes_install/lifecycle/project_register.py` | the **`project-register` verb** — resolve one revision, read, derive, validate with the runtime's own reader, **publish last**; no retry, the schedule is the retry |
| `src/hermes_install/review_authority/derivation.py` | **the ONE implementation of the narrowing** (`derive_projection`, `GOVERNANCE_ROOT = "governance/review-authority"`) |
| `config/schemas/hermes-review-authority-register-projection.schema.yaml` | the projection schema (`schema_version 2`) |
| `config/negative/*.review-authority-projection.yaml` | seven negative fixtures, including **`revoked-grant`**, **`stale-projection`** and **`expired-grant`** |
| `specs/019-register-projection-refresher/` | the feature: `spec.md`, `contracts/project-register-cli.md`, `contracts/register-source.md`, `contracts/register-narrowing.md`, `contracts/published-projection-configmap.md` |
| `docs/evidence/register-projection-refresher-deploy-2026-08-30.md` | **the deploy record — it is LIVE** |

**IT IS INSTALLED, AND ONE RUN OF IT HAS SUCCEEDED — WHICH IS NOT THE SAME
CLAIM AS "IT IS RUNNING".** Per that evidence record (2026-08-30, PR #63
`6b68c93` + stamp PR #64 `5741c9b`, image tag
`xfactory-hermes-install:wallet-exercise-019-20260830`): CronJob
**`hermes-register-projection-refresher`** is present, schedule
**`0 */2 * * *`**, publishing ConfigMap `hermes-register-projection`.

**THE RUN THAT IS ON RECORD IS A MANUAL MIGRATION JOB, NOT A SCHEDULED FIRING.**
It is that record's own step 2, labelled **"THE ONE ACT"**:
`job/register-projection-migration-202608301523`, which completed with
`outcome: succeeded`, `repository opensoft/openxFactory`, `revision 698073f7…`,
`register_version 1`, `declared_staleness_bound P7D`, `seat_count 4`, all four
`merge_readiness_council` seats validated, and
`earliest_expires_at 2026-11-23T12:00:00Z`.

**NO SCHEDULED FIRING HAS BEEN OBSERVED ON RECORD AS OF THIS ACT.** The evidence
record's verification section says only that the CronJob's schedule is
*"present; first scheduled run due at the next even hour"* — **DUE**, not
observed — and its follow-ups list *"Observe the first scheduled refresher run
and the first convening"* as work still owed. Measured here rather than assumed:
`gh api repos/opensoft/xFactory-Hermes-Install/contents/docs/evidence --jq
'.[].name'` returns **eleven** evidence records, the newest of which is that
2026-08-30 deploy record itself; and a shallow clone of that repository's
default branch resolves to **`7f59baa9`, dated 2026-08-30T11:34:43-04:00** —
i.e. **nothing has landed in that repository since the deploy**, so there is no
later observation to find and none is being overlooked.

**SO WHAT THE MANUAL DUTY'S RETIREMENT ACTUALLY WAITS ON.** The machinery that
replaces the standing seven-day re-projection duty is installed and has run
correctly once, by hand. **The duty is retired only once a SCHEDULED firing is
observed** — that observation is hermes-install's to make and hermes-install's
to record, it is on that repository's own follow-up list, and **this record does
not assert the retirement on the strength of the installation.**

### 8.2 What this means for THIS act — precisely

* **THE PROJECTION IS NOT RE-DERIVED BY THIS ACT.** It is not this act's to
  perform: it is the operator's, and it now runs as machinery on the cluster.
* **IT WILL NOT MOVE WHILE THIS PULL REQUEST IS OPEN — and the mechanism is not
  `origin/HEAD`.** The deployed CronJob passes **no `--source`**, and `--source`
  defaults to `github`
  (`src/hermes_install/lifecycle/cli.py:718` —
  `p.add_argument("--source", choices=("github", "checkout"), default="github")`),
  so the run resolves through **`GitHubContentsSource.resolve()`**: with no
  `--revision` it reads the repository's **`default_branch`** over the GitHub
  contents API and takes that branch's head
  (`src/hermes_install/lifecycle/project_register.py:252`). **`origin/HEAD` is
  the OTHER source** — `GitCheckoutSource.resolve()`, same file, line 180, whose
  `revision or "origin/HEAD"` is the OPERATOR's local-checkout path that the
  deploy runbook invokes, not the cluster's. Either way, a branch that is not the
  default branch is never read, so this candidate's revision is invisible to the
  refresher until it lands.
* **"WITHIN TWO HOURS OF MERGE" IS THE SCHEDULE'S PROMISE, NOT A MEASURED
  PROPERTY.** `0 */2 * * *` is what the manifest says will happen. **No scheduled
  firing of this CronJob has been observed on record** (§8.1), so the first
  post-merge tick is itself the thing to watch for rather than something to
  predict — and if it does not fire, the projection does not move and nothing in
  this repository will say so.
* **WHAT IT WOULD TAKE, NAMED:** either the next scheduled CronJob tick after
  merge, or a manual `project-register` run against the merged revision. Nothing
  else — no heredoc, no hand-built document.
* **`revocation_staleness_bound: P7D` TRAVELS VERBATIM** into
  `projected_from.staleness_bound`. It is **not touched by this act** — the row
  moved, the bound did not — and it must not be tightened here as a tidy-up. The
  2026-08-30 migration already carried `P7D` verbatim, which is the property
  observed working.
* **THE REVOKED GRANT DOES NOT BREAK THE DERIVATION** — checked, not hoped:
  `derivation.py` reads `grants/<the row's grant_ref>.yaml` and only that, so
  `grant-mrc-0001.yaml` is never opened by it. It also refuses a grant whose
  `state` is not `active` and a row whose `state` is not `active`; the repointed
  row satisfies both.
* **`earliest_expires_at` will move** from `2026-11-23T12:00:00Z` to
  `2027-06-30T00:00:00Z` on the first post-merge projection. That is the visible
  signal that 5b happened.

**UNTIL THE PROJECTION IS RE-DERIVED, THE RUNTIME KEEPS REFUSING WITH
`review_authority.root_key_mismatch`, AND NO AUTHORITY FLOWS.** Landing the
register act does not un-park anything by itself. **Stopping at §5 is the
commonest way to think this runbook is finished when it is not.**

### 8.3 "VERIFY ONE CONVENING ADMITS" — NOT PERFORMED, and not performable today

The runbook's §5.2 step 3 is unambiguous: *"The park is not lifted by a green
validator — it is lifted when a real convening is admitted against the new
grant. Until you have seen that, you have evidence that the FILES are consistent
and no evidence that the LANE recovered."*

**No convening was watched, because NO REAL CONVENING HAS EVER RUN IN THIS
ESTATE.** Not one commissioned soak has run; no deliberation row exists; and
**runner provisioning is ops.**

**MEASURED FOR THIS ACT, NOT INHERITED.** The workflow is
`.github/workflows/council-deliberation-worker.yml`, **id 339735899** (`gh api
"repos/opensoft/codexFactory/actions/workflows" --jq '.workflows[]|select(
.name|test("deliberation"))|{id,name,path}'`; its sibling
`council-deliberation-reusable`, id 330757762, reports **0** runs of its own —
it is called, not dispatched). Paginating that workflow's runs twelve pages deep
(`gh api "repos/opensoft/codexFactory/actions/workflows/339735899/runs?
per_page=100&page=N"`, N = 1…12) returns **1113 runs across 166 DISTINCT HEAD
SHAS**, spanning 2026-08-21T23:16:55Z to 2026-09-02T14:31:36Z. Taking the **30
most recent** and reading each run's jobs (`gh api
repos/opensoft/codexFactory/actions/runs/<id>/jobs --jq
'.jobs[]|{name,conclusion}'`): the `deliberate` job's conclusion is **`skipped`
in 30 of 30**, executed in none.

**SO THE FACT, STATED AT THE STRENGTH IT WAS MEASURED: the `deliberate` job has
never been observed to execute — it is skipped in every sampled run of 1113
total across 166 head shas, sampled through 2026-09-02.** That is the claim this
record makes, and it is deliberately narrower than "every run in the repository's
history is at one commit", which is **not** true of this workflow: 166 distinct
head shas have dispatched it.

**THE EARLIER READING, AND IT IS NOW A CLOSED RECORD.** codexFactory issue
**#156** — *"Channel A was never live: the deliberate job has never executed
(855 runs, claimed=false) — the soak records' Channel-A lines rest on skipped
runs"* — made the same measurement at **855 runs**, and it is **CLOSED, state
reason COMPLETED, 2026-09-02T00:51:24Z** (`gh issue view 156 --repo
opensoft/codexFactory --json state,closedAt,stateReason`). It is cited here as
**the durable record of that measurement**, not as a live tracking item, and its
own qualification travels with it rather than being dropped: *"Stated as
observed, not diagnosed — no runner-provisioning investigation was done here."*

**AND NOTHING OPEN OWNS IT.** Searched for the open item that carries this
obligation — `gh issue list --repo opensoft/codexFactory --state open --search
"convening OR deliberate OR runner"`, the same against `opensoft/xFactory` and
`opensoft/openxFactory`, plus codexFactory's full open list — and nothing
returned owns *"no real convening has ever run"*: codexFactory **#154** is the
convening-packet-refs carve-out protocol question and **#131** is the
gate-rules charter amendment; neither is this. **No open issue owns it as of
2026-09-02.** This act does **not** file one — filing is not a register act's to
do — and the absence is recorded here so it is a known gap rather than an
assumed owner.

**The predecessor walk recorded the absence from the other side, and its wording
is quoted rather than strengthened**: *"Every `council-deliberation-worker` run
in the repository's history **at the time of writing** is at `01a0c64a` — the
flip's first parent."* Its hedge is its own and stays on it; the measurement
above supersedes the READING, not the sentence.

**So step 3 of the runbook's §3 (R9's in-flight park) is VACUOUSLY not exercised
here too**: nothing was in flight when this act landed because nothing convenes.
A vacuous non-exercise is recorded as a vacuous non-exercise and never as a pass.

**This is the honest state: the files are consistent; the lane is unproven.**

---

## 9. WHAT THIS ACT DISCOVERED — THE PINNED READER REFUSES A CORRECTLY-PERFORMED RE-ISSUANCE

**This section is the most important thing in this record, and it is a defect in
the pinned reader, not in the act.**

### 9.1 The measurement

Running the required gate's own invocation over the amended tree —
`python3 openXwallet/scripts/validate-openxwallet.py .`, which is literally what
`.github/workflows/openxwallet-consumer-gate.yml` runs. **The block below is an
EXCERPT.** The run emits **eight** `note` lines and eleven lines in all (eight
notes, the one `ERROR`, a blank line, the summary); the **five** notes elided
here report the approval-scope vocabulary read, two wallet key adjudications,
the corpus positive/negative tally and the nested-repository prune. **None of
the five is a finding**, and none is omitted because it is inconvenient — they
are dropped only so the three that bear on the register act sit next to the
error:

```
note  intake register read: governance/review-authority/register.yaml (1 row(s))
note  intake register: 4 of 4 per-seat signing key(s) adjudicated and resolved
note  repo scan: 3 openxWallet artifact(s) validated, 1843 document(s) skipped as another kind
ERROR [register-no-active-row] active REVIEW-class grant 'grant-mrc-0001' has no
  backing active register row; admitting a convening for this holder would confer
  authority the register never granted

validate-openxwallet: 1 error(s), 0 warning(s)
```

**Everything the act itself had to get right is green** — the register read, the
row, the four seat keys, the new grant, the wallet's five declared keys. The one
error is fired **about the grant this act correctly revoked**.

### 9.2 Why it fires — the message asserts a filter the code does not perform

`check_register`'s closing loop (pinned validator, and **identical on openXwallet
`main`** — checked, so a pin bump alone does not fix it):

```python
for gid, g in sorted(ctx.grants.items()):
    scope = g.get("scope") if isinstance(g.get("scope"), dict) else {}
    if REVIEW_ACT_TOKEN not in _hashable_set(scope.get("acts")):
        continue
    backed = any(... r.get("grant_ref") == gid and r.get("state") == "active" ...)
    if not backed:
        f.error("register-no-active-row",
                f"active REVIEW-class grant {gid!r} has no backing active register row; ...")
```

**The message says "active REVIEW-class grant". The code never checks
`g["state"]`.** It filters on the ACT class only. A revoked grant that still
carries `acts: [review]` — which every correctly-revoked review grant does, since
falsifying its scope to escape a validator would be a forgery — is treated as
though it were live and demanded a backing row.

**And it cannot be given one.** The row cap is exactly ONE authority row
(`register-minimal-shape-exceeded`), and `backed` requires a row that is `state:
active` and unexpired. So there is no register this reader accepts that also
contains a revoked review-class grant. **The register, as read today, cannot
represent a re-issued authority at all.**

### 9.3 The combination has never been exercised anywhere

The packaged corpus contains exactly **ONE** revoked grant, not two: openXwallet
`contracts/openxwallet/examples/grant-revoked-parent.example.yaml`
(`state: revoked`, line 17). Its companion
`grant-revoked-derivation.example.yaml` is **`state: active`** (line 21) — it is
the **DERIVED CHILD** of that revoked parent, and what it exercises is the
`_revoked_ancestor` chain walk, not a revoked state of its own. **Both are
`post_transaction`-class** (`acts: [post_transaction]`), **never
`review`-class**, and both live under an `examples/` path the live sweep
excludes by construction. The self-test's `register-no-active-row` probe uses an **empty
register**, not a revoked grant. **"Revoked + review-class + a live register" is
a state the corpus, the self-test and every prior run have never produced** — the
first re-issuance in this estate is the first thing that produces it.

**The runbook asserts the opposite in terms**, and the assertion is now measured
false: *"There is no order of these writes that is green halfway."* True — and
insufficient, because there is no order that is green at the **END** either.

### 9.4 The minimal remedy, MEASURED — and NOT taken here

Two lines in the pinned reader's loop — `check_register`'s closing loop, the
`for gid, g in sorted(ctx.grants.items())` block at
`openXwallet/scripts/validate-openxwallet.py` **lines 3006–3023** in the pinned
copy (`6b248d4050e1f88b3ca75c1290ad2c81f465300c`), whose
`f.error("register-no-active-row", …)` sits at line **3019**. **There are TWO
candidate filters, and the difference between them is not cosmetic. Both are
presented; neither is taken here.**

**(a) THE BROADER FILTER — the one measured below:**

```python
    if g.get("state") != "active":
        continue
```

**(b) THE NARROWER FILTER — the terminal fact and nothing more:**

```python
    if g.get("state") == "revoked":
        continue
```

**WHAT SEPARATES THEM.** (a) additionally exempts a grant whose STORED state is
`expired`. That matters because the reader's expiry checking runs in one
direction only: `grant-state-stale` (line **2987**) fires for a grant stored
`active` whose COMPUTED expiry has passed, and **there is no inverse check** —
nothing refuses a grant stored `expired` while its own `expires_at` is still in
the future. Under (a) such a grant leaves the loop silently; under (b) it is
still required to have a backing row and is still caught. (b) is backstopped
from the other side by **`revocation-unrecorded`** (line **1161**), which
refuses `state: revoked` with no `revocation` block — so (b) cannot be satisfied
by writing the word "revoked" and nothing else.

**NEITHER WEAKENS PROTECTION, and that is the load-bearing claim here.** The
row→grant direction is untouched by both: **`register-grant-mismatch`** (line
**2994**) already appends `f"grant state {grant.get('state')!r}"` to its
mismatch list whenever a row's grant is not `active`, so **a revoked grant can
never back a live row** under either filter. And **`_revoked_ancestor`** (line
**1179**) still refuses any exercise whose grant chain reaches a revoked grant
or a revoked wallet. What either filter removes is only the REVERSE obligation —
*"this grant must have a row"* — applied to a grant that has stopped claiming
anything.

**THE RECOMMENDATION, FOR openXwallet TO RULE ON AND NOT FOR THIS RECORD TO
DECIDE: (b), the narrower one.** It encodes the terminal fact the cascade
contract already defines, changes behaviour in exactly the case that motivated
the change, and does not quietly widen an exemption to `expired` in the same
edit — a widening that the missing inverse check makes more than theoretical.

**Measured:** **variant (a)** applied to a throwaway copy of the validator, the
same tree validates **`0 error(s), 0 warning(s)`**. The copy was then restored
**byte-identical** (diff clean) and the submodule left clean; **no change to the
pinned reader is carried by this pull request.** **Variant (b) is offered
UN-MEASURED**, as a design recommendation — which is the honest label for it,
and the reason it is openXwallet's call and not this record's.

**WHY IT WAS NOT TAKEN HERE, and why no workaround was taken either.**

* The reader lives in **`opensoft/openXwallet`**, a different repository, consumed
  here at a **commit plus eight digests**. Editing it from this change is
  impossible and would be wrong: it is a contract change and goes through
  openXwallet's own OpenSpec, then a pin bump here.
* **Deleting `grant-mrc-0001.yaml`** would make the gate green and was
  **REFUSED**: revocation is a terminal FACT about a grant, and the runbook
  requires it revoked **in place, in its own file**.
* **Editing its `scope.acts` so it is no longer review-class** would make the gate
  green and was **REFUSED as a forgery**.
* **Moving it under an `examples/` path** would make the gate green by making the
  scanner stop treating it as live, and was **REFUSED**: it hides a live
  governance record to satisfy a checker.
* **Adding a second row** was **REFUSED** by the cap, by the runbook's own
  non-write, and because a row for a revoked grant would not satisfy `backed`
  anyway.

### 9.5 The consequence, stated plainly

**TWO REQUIRED CHECKS ARE RED AT THIS HEAD, AND THEY ARE RED FOR DIFFERENT
REASONS. ONE IS THIS ACT'S; ONE IS NOT.** Ruleset **21538893** requires **both**
`wallet-validation` **and** `pytest-suite` — verified by `gh api
repos/opensoft/openxFactory/rules/branches/main`, which returns ruleset 21538893
with contexts `wallet-validation` and `pytest-suite` (and a second ruleset,
**21957695**, requiring `signed-execution-chain-gate`). At head **`f1706a3a`**
the check runs read (`gh api
repos/opensoft/openxFactory/commits/f1706a3aa8e6bc0c6e0490c62a8f1227533a8e0e/check-runs`):
`wallet-validation` **failure**, `pytest-suite` **failure**,
`signed-execution-chain-gate` **success**, `merge-master-approval` success,
`copilot-pull-request-reviewer` success.

* **`wallet-validation` IS THIS ACT'S RED.** It is the reader defect of §9.1–§9.4
  — one `register-no-active-row` on the correctly revoked `grant-mrc-0001`. It
  clears when the pin moves to a fixed reader, and not by any edit to this
  record.
* **`pytest-suite` IS INHERITED FROM `main`, NOT CAUSED HERE.** It fails on
  **`tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire`**.
  `main`'s own latest `pytest-suite` run — **33621990229**, head `f4fddf7c`,
  2026-09-02T10:55:58Z (`gh run list --repo opensoft/openxFactory --branch main
  --workflow pytest-suite.yml --limit 1`) — fails **the same single test**:
  `--log-failed` returns `FAILED
  tests/doc-health/test_release_tag_publication.py::test_this_repository_reads_zero_and_the_probe_can_fire`
  in a run of `1 failed, 8620 passed, 21 skipped, 338 deselected`. **This change
  neither causes it nor fixes it**, and it is named here so that an admin merge
  under "B2" is not read as merging past a red this act introduced — one of the
  two reds it would be merging past is `main`'s.

`wallet-validation` is a **REQUIRED** check (opensoft org ruleset **21538893**)
and the consumer gate runs **on pull requests only**. So merging this change with
the reader unfixed puts `main` in a state where **every subsequent pull request's
`wallet-validation` is red** — the breakage never reports on `main` and surfaces
on somebody else's candidate. **That is a known trap in this estate and it is
named here so nobody rediscovers it.**

**THE CORRECT ORDER, IN FULL — AND THE THIRD STEP IS THE ONE THAT IS EASY TO
DROP:**

1. **Fix the reader in `opensoft/openXwallet`** — the narrower filter (b) of
   §9.4 — through that repository's own OpenSpec, and release it.
2. **Bump `contracts/openxwallet-pin.yaml` AND the `openXwallet` gitlink on
   `main`**, in its own human-only pull request.
3. **MERGE `main` INTO THIS BRANCH (or rebase this branch onto it).** **A pin
   bump on `main` does not move THIS branch's gitlink.** The gitlink is a tree
   entry recorded per commit, so until `main` is merged in, this branch keeps
   pointing at `6b248d40` — the reader with the defect — and
   `contracts/openxwallet-pin.yaml` here keeps naming it. Skip this step and
   `wallet-validation` is re-run against the OLD reader and stays red, and the
   admin merge becomes a merge past a red that the fix had already cured
   everywhere except on the one branch that needed it.
4. **Re-run `wallet-validation` ON THIS HEAD and see it GREEN**, against the
   fixed reader this branch now carries. That green — not `main`'s — is the
   evidence that the act passes.
5. **THEN admin-merge under "B2"** — the coordinator, on the ratifier's word,
   with the provenance comment. (`pytest-suite`'s inherited red, §9.5 above, is
   not cleared by any of this and is merged past knowingly.)

**WHY STEPS 1–2 ARE NOT FOLDED INTO THIS PULL REQUEST, and the ground is
ratified rather than preferential.** `openspec/specs/neutral-product-pin/spec.md`
carries the requirement **"Repointing the reader and editing what it reads is
one human-only act"**: a pull request that changes a neutral product's pin or
its gitlink **and** any file under the review-authority register's directory
*"SHALL be HUMAN-ONLY … because a candidate could otherwise repoint the very
reader that judges its own change."* **This candidate edits the register
directory.** Stated exactly: the requirement's remedy is *human-only*, not
*forbidden*, so folding the bump in would not by itself violate it — but it
would produce precisely the shape the requirement exists to name, a register act
that also chooses which reader judges it. **The pin bump is therefore a separate
act, taken first, and this branch consumes its result through step 3.**

This record does not decide that order; it states it.

---

## 10. The honest limits, restated in terms (runbook §7)

* **R8 AND R9 ARE NOT ENFORCED.** *"Neither ruling is enforced until the change
  carrying R6–R12 is ratified"* — and **R6–R12 is not authored, let alone
  ratified**. This walk performs a real act against a settled target; **it does
  not exercise an enforced control**, and no gate in this estate would have
  refused a re-issuance that ignored the runbook entirely.
* **THIS WALK DOES NOT EVIDENCE THE PLANE, AND MUST NOT APPEAR TO.** The plane is
  R5's, and it is evidenced by the Operator identity record's read-back
  (EXE-1/EXE-2), which this act CARRIES but did not perform. *"This Council does
  not evidence the plane and must not appear to."*
* **NO FULLY-PINNED-COMPOSITION CLAIM IS MADE.** `claude-haiku-4-5-20251001` — the
  CLI's internal helper — executed in **33 of 33** measured judgments of the
  2026-08-22 corpus and **4 of 4** inventory invocations, is declared in no
  composition file, is pinned by no flip, and carries the earliest published
  retirement floor in the register (**2026-10-15**). The **runtime** is likewise
  not one of the six declared components. Whether the helper becomes a seventh
  component or lives under `parameters` belongs to the R6–R12 change.
* **THE SELECTION REMAINS CONDITIONAL.** No seat returned an unqualified SELECT;
  the three domain slots stand on the union of the bench's conditions; six of run
  2's residual judgments are untouched; DA-3 is a live watch item on codexFactory
  issue **#154**.
* **THE ACTIVATION IS NOT ISSUANCE, AND ISSUANCE IS NOT ADMISSION.** This act
  issues. It does not project (§8), and it does not admit a convening (§8.3).
* **ONE STALE PROSE REFERENCE IS LEFT STANDING, DELIBERATELY.**
  `governance/review-authority/wallets/wal-agent-mrc-0001.yaml`'s `keys:` comment
  says *"grant-mrc-0001 is addressed to the WALLET"*. It is now
  `grant-mrc-0002`. **The wallet file is NOT edited by this act** — it is a live
  instance record, the sentence is an argument about key multiplicity rather than
  a resolution path, nothing reads it, and rewriting a live wallet to fix a
  comment is a wider act than a register act. **It is named here so the next
  editor of that file fixes it deliberately rather than discovering it.**
* **THE RUNBOOK AND THE REGISTER'S OWN PROSE ARE BOTH STALE ABOUT §5b.** Both say
  nothing refreshes the projection automatically; a CronJob has done so since
  2026-08-30 (§8.1). **Neither document is amended by this act** — the runbook is
  `Status: draft` and its correction belongs with the R6–R12 change or with a
  dated runbook revision, and `register.yaml`'s P7D paragraph is standing
  governance prose on a human-only surface, corrected only by an argued edit.
  **Recorded here so the correction is owed to a named place rather than
  remembered.**
* **THE CROSS-REPOSITORY DEBT IS NOT ONE EDIT. IT IS 90 OCCURRENCES ACROSS 44
  FILES, AND THIS IS WHERE THE REAL NUMBER LIVES.** The tasks-ledger note under
  7.7 originally named one hermes-install test; that was the sharpest instance,
  not the scope. Measured against a read-only shallow clone of
  `opensoft/xFactory-Hermes-Install` `main` (`7f59baa9`, 2026-08-30) with
  `grep -rn 'grant-mrc-0001\|2026-11-23T12:00:00Z' --include='*.py'
  --include='*.yaml' --include='*.md' .` → **90 hits**, and the same with
  `-rln` → **44 files**:

  | Class | Files | Hits | What is stale in it |
  |---|---|---|---|
  | **runtime code** | 1 | 1 | `src/hermes_install/review_authority/derivation.py` |
  | **A VENDORED COPY OF THIS REGISTER** | 10 | 25 | `tests/fixtures/review_authority_register/` — including literal copies of `governance/register.yaml` and `governance/grants/grant-mrc-0001.yaml`, an `expected-projection.yaml`, and six negative fixtures |
  | **test modules** | 11 | 20 | `tests/{unit,pg,api,support}/` — the assertions, incl. `test_the_live_register_rows_expiry_is_a_fact_a_test_asserts` |
  | **config example** | 1 | 6 | `config/examples/review-authority-register-projection.example.yaml` |
  | **config negative fixtures** | 7 | 14 | `config/negative/*.review-authority-projection.yaml` |
  | **docs** | 4 | 6 | two evidence records, the deploy-window runbook, `docs/traceability.md` |
  | **specs** | 10 | 18 | features 015, 016, 019 |

  **THE VENDORED REGISTER COPY IS THE ONE THAT MATTERS MOST**, and it is the one
  a reader of the 7.7 note would not have expected: hermes-install carries its
  own `governance/grants/grant-mrc-0001.yaml` and `governance/register.yaml`
  under `tests/fixtures/`, so **this repository's register now disagrees with a
  copy of itself in another repository**, and the copy is what that repository's
  derivation tests derive from. **None of the 90 will go red** — every one is a
  literal, a fixture, or prose — **so nothing announces the divergence.** The
  edit is a hermes-install change, is **NOT** made from this repository or by
  this act, and is recorded here at its measured size because "one
  cross-repository edit" understated it by a factor no reader could recover.
* **THIS PULL REQUEST APPENDS TO A DOCUMENT WHOSE `Status:` IS `record`, AND
  THAT TENSION IS NAMED RATHER THAN GLOSSED.**
  [`walk-2026-08-31-composition-bump.md`](walk-2026-08-31-composition-bump.md)
  carries `Status: record`, and a record is not ordinarily reopened. Its §8
  return trip is appended here **because the runbook's §5.1 mandates it** — the
  predecessor walk is where the re-issuance it anticipated must be answered.
  **The append is append-only, and that is checkable rather than asserted:**
  `git diff origin/main...HEAD --numstat --
  openspec/changes/add-wallet-carried-review-authority/walk-2026-08-31-composition-bump.md`
  → **`48  0`** — forty-eight lines added, **zero deleted**. Nothing the record
  said has been unsaid.

---

## 11. Ledger movement this walk supports

**None by itself.** *"A walk ticks no task by itself."*

* **7.5 — ALREADY TICKED**, 2026-08-31. This act **closes the gap that tick
  explicitly named as still open**: *"THE REGISTER ACT IS OWED — sequencing step
  5; the declared composition moved and no governed re-issuance has been
  performed, so `grant-mrc-0001` still stands against the prior composition."*
  **It no longer does.** No checkbox moves; the note is argued at that task.
* **7.6 — STAYS OPEN**, on its own sentence (*"neither ruling is enforced until
  the change carrying R6–R12 is ratified, so this task stays OPEN"*). Ground 1 is
  untouched by any walk. What this act DOES settle is 7.6's **Ground 2**: the
  revocation-class exercise the predecessor walk lacked has now happened — the
  three atomic writes of §5.1, performed for real.
* **7.7 — STAYS OPEN, and its own text is why.** Its gate is *"a revoked holder
  parks a convening with a named refusal in a rehearsed test; an unreadable
  register refuses; the runbook has been walked once."* Limb three moved on
  2026-08-31 and moves further here. **Limb one is NOT met**: a revoked holder
  now exists, but **no convening was parked, because nothing convenes** (§8.3).
  **A gate is met when all its limbs are.**
