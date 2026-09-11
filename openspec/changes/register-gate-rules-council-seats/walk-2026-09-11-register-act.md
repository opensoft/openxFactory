# Walk record — the 2026-09-11 REGISTER ACT (RE-ISSUANCE) for `gate_rules_council`, against `docs/governed-reissuance-runbook.md`

Status: record
Kind: report
Repository context: openxFactory
Walked: 2026-09-11
Runbook walked: [`docs/governed-reissuance-runbook.md`](../../../docs/governed-reissuance-runbook.md)
  — `Status: draft`, steps **5**, **§5.1**, **step 5b (§5.2)** and **§7**
The act: **the human-ratified REGISTER ACT (RE-ISSUANCE)** — the group-3
  governed re-issuance that codexFactory's
  `clarify-gate-rules-decline-position` names as the only thing that lifts its
  operational hold
Ratifying human: **Brett Heap** (`Brett.Heap@opensoft.one`)
Effective instant: **`2026-09-11T02:12:30Z`** — ONE instant, taken once from
  `date -u`, written identically into `grant-grc-0001`'s
  `revocation.revoked_at`, into `grant-grc-0002`'s `issued_at`, and here
Predecessor walk: [`walk-2026-09-08-register-act.md`](walk-2026-09-08-register-act.md)
  — `grant-grc-0001`'s own COLD START. **This act supersedes it; it does not
  re-derive it.**
Precedent walk: [`../add-wallet-carried-review-authority/walk-2026-09-02-register-act.md`](../add-wallet-carried-review-authority/walk-2026-09-02-register-act.md)
  — the one completed re-issuance in this estate, and the convention every
  timestamp below follows

---

## 0. THE HEADLINE, BEFORE THE DETAIL

**The register act is composed and it is NOT YET LANDED.** `grant-grc-0001` is
revoked for **DRIFT** on the 2026-09-10 composition change; `grant-grc-0002` is
issued against the changed composition at the same instant; `row-grc-0001` is
repointed onto it; no row was added.

**It DID land green locally, and that is the difference from the precedent.**
The 2026-09-02 act could not pass `wallet-validation` at all — the pinned
reader's `check_register` loop demanded a backing ACTIVE row for a *correctly*
revoked grant (`register-no-active-row`). That defect was fixed in openXwallet
#14 (`b7b0fbb3`, `wallet-v1.4`) and this repository now consumes `wallet-v1.5`
(`f3eb929b9ab6d78bf30e26bf1d7a99af86a7016e`). **§6 records the measurement,
taken fresh over this act's own amended tree rather than assumed from the pin
label.**

**What is NOT done, and none of it is a formality:**

* **THIS ACT IS NOT MERGED.** It is composed by the coordinating lane and
  awaits **Brett Heap's merge word**. The merge is the second of two words
  (§7.3), and until it is given nothing here is on `main`.
* **STEP 5b IS NOT DONE BY THIS ACT** (§8). The register act does not reach the
  runtime by itself. **Until the projection is re-derived, the runtime keeps
  refusing with `review_authority.root_key_mismatch` and NO AUTHORITY FLOWS.**
* **THE HOLD IS NOT LIFTED BY THIS FILE'S EXISTENCE** (§9). It lifts when a
  real convening is observed to be ADMITTED, not when a validator goes green.

---

## 1. THIS FILE'S PATH IS THE RECORD ID THE HOLD CITES

The operational hold posted on codexFactory issue **#279**
([comment 5626749744](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5626749744),
Brett Heap, 2026-09-10T23:20:43Z) and on PR **#374**
([comment 5626750445](https://github.com/codeXfactory/codexFactory/pull/374#issuecomment-5626750445),
2026-09-10T23:20:48Z) names exactly one lift condition:

> **What lifts it — one condition and no other.** The group-3 governed
> re-issuance record exists on `opensoft/openxFactory:governance/review-authority/`
> and is cited by id at task 3.7. Not elapsed time, not a green suite, not a
> re-run.

**The record id is this file's path:**

```
openspec/changes/register-gate-rules-council-seats/walk-2026-09-11-register-act.md
```

Filed here on Brett Heap's ruling of **2026-09-11T02:03:35Z**, choosing this
directory over the codexFactory change directory: this is the gate-rules
holder's walk-record home, established by task 3.9 of this same change
(*"`openspec/changes/register-gate-rules-council-seats/walk-<YYYY-MM-DD>-register-act.md`,
in the form of `walk-2026-09-02-register-act.md`"*), and the predecessor walk
for this holder is its sibling in the same directory.

**A WORDING DIFFERENCE, NAMED RATHER THAN PAPERED OVER.** The hold says the
record *"exists on `opensoft/openxFactory:governance/review-authority/`"*. The
**act** is there — three writes under `governance/review-authority/`, listed in
§5. The **record of the act** is this file, under `openspec/changes/`, which is
where both prior walk records in this estate live and where the ruling places
this one. Nothing is hidden by the distinction: the hold's substance is that the
governed re-issuance was performed on the human-only surface and can be cited by
id, and both halves are satisfied. Cite **this path** at codexFactory task 3.7,
and cite the merge commit of this pull request beside it.

**This file is NOT ITSELF THE LIFT.** §9 states the real exit condition, which
is an admitted convening.

---

## 2. What each step produced

Each row says what the step PRODUCED. A tick would say only that somebody looked.

| Runbook step | Exercised? | What it produced |
|---|---|---|
| **§0.3 who holds which act** | yes | §7 — the capacity table, **three capacities in one human plus two machine-held ones**, disclosed and not collapsed |
| **§1 the superseded state** | yes, **fetched live and hash-compared** | §4 — `grant-grc-0001` and `row-grc-0001` as they stood, proved identical to `origin/main` before anything was edited |
| **§2 the bump** | **inherited, not re-performed** | §3 — codexFactory `02e14c08`, and the five digests that moved, computed by rendering |
| **§3 in-flight (R9)** | **NO — and NOT vacuously this time** | §9.1 — R9 is keyed on composition *mismatch*, and this change moved text and pin together, so no mechanical park fires. The **hold** is what stands in for it, and closing the window is Part C's §3.8 check |
| **§4 R8 five fields** | yes — **four filled, one substituted and labelled** | §6.4 |
| **§5 the register act** | **YES — COMPOSED, not yet merged** | §5 |
| **§5.1 revoke / mint / repoint / do-not-add** | **YES — three writes and one non-write, ONE commit** | §5 |
| **§5.2 (step 5b) the projection** | **NO** | §8 — Part C's, stubbed here |
| **§5.2 "verify one convening admits"** | **NO** | §9 — Part C's, stubbed here |
| **§7 record the act** | yes | This document |

---

## 3. T1 — THE COMPOSITION EVENT, FILLED

**T1 = `2026-09-10T23:34:23Z`**, the merge of codexFactory PR **#374** at commit
**`02e14c086d5ead77d0c390c33ba5df622f07a4df`**.

`gh pr view 374 -R codeXfactory/codexFactory --json state,mergedAt,mergeCommit`
returns `"state":"MERGED"`, `"mergedAt":"2026-09-10T23:34:23Z"`,
`"mergeCommit":{"oid":"02e14c086d5ead77d0c390c33ba5df622f07a4df"}` — checked at
this act, not carried from the draft that prepared it (which recorded #374 still
`OPEN`).

### 3.1 What moved

`hermes/domain/agent-mixes.yaml` **component 2** — the `gate_rules_council`
**PROMPT-CORPUS pin** — under the ratified change
`clarify-gate-rules-decline-position`, **row C+** (variant V2S): the
decline/refuse standing distinction plus the tool-less `executed` guard, in
**PROHIBITION** form carrying adversarial review R1's **S2** checked/unchecked
sentence. The ratified packet is codexFactory PR **#361** → **`65ee2f10`**, and
the governing clause sits at `hermes/domain/agent-mixes.yaml:396-401`.

**EXACTLY ONE of the six declared components moved**, and one is sufficient:
*"WHEN any single component of the declared set changes, THEN the change alone
is sufficient to revoke, AND no threshold, score, or tolerance band is
consulted."*

### 3.2 The five digests, before and after

Computed by **rendering** the four seat briefings through
`.github/workflows/scripts/deliberation_packet.py#seat_system_prompt` — the same
method `test_the_rendered_set_matches_the_declared_content_pin` uses — and
**never copied from `design.md`'s table**. Every value was additionally
re-derived by a second route (renders written to files and hashed with
`sha256sum`; the set by concatenating `<seat> NUL <render> NUL`), and both
routes agreed.

| | **BEFORE** (row A, as shipped) | **AFTER** (row C+ / V2S) |
|---|---|---|
| `rendered_set_digest` | `sha256:2d4660230104fb9e5fddeef37eec494cd38b57627feef7a2e396ac98eaf9a99e` | `sha256:aac9b60e877d5ab61324ebb5102fe24b685b1bcc1d97aecf9f6c8ef254358f21` |
| `lead-architect` | `sha256:5d3e6b12ad01b5c20de5242d2fef51e4bac990d09adaa5a9cca063499871b554` | `sha256:619153c4f31cb1c2f57d00a692d785eed656e354424443507cb01726298a12d0` |
| `lead-security` | `sha256:bc29937e550768cf319fc8ad39c73abddf58da0087c6431f78ff4fe30be583d6` | `sha256:4d90a110c52095c998744e04cb8e2d24387c01d8d5ddc399ba81f28b2ad69cab` |
| `lead-quality` | `sha256:a106892a47254408b3ec571115e235fc117f529aef2bd12952d89e4d0aa9a506` | `sha256:3a7bb5718adcaa4ad01cb8f2e983125601cd06b5bd5aed4bee855d66f2571e29` |
| `company-policy-lead` | `sha256:22cb4fb6d7af36f3341ba73febac1794e7c1821249838204741fe562d372b595` | `sha256:7c170ecb2b46e53e041d122c2d92cdbee32ce0da110c38e559e432b088d0e2d0` |

**There is no half of that edit that is green**, exercised rather than quoted:
the clause edit applied WITHOUT the matching re-pin gives
`test_gate_rules_holder_composition.py` **1 failed, 34 passed**, failing at
`test_the_rendered_set_matches_the_declared_content_pin`. **And that is
precisely why no mechanical park fires** — see §9.1.

### 3.3 The revocation is BY DECLARATION, not by anything that ran

`agent-mixes.yaml`'s own comment governing this holder's component 2 said so
before the fact:

> "THE DIGEST MAKES AN EDIT A DECLARED COMPOSITION CHANGE, exactly as it does
> for merge-readiness: under `openxwallet-agent-profile` a composition change
> revokes this holder's grants immediately and requires a governed
> re-issuance. For THIS holder no grant exists yet — the grant is Brett's walk
> (`register-gate-rules-council-seats` task 3.5) — so this first pin revokes
> nothing. **Every LATER edit will.**"

PR #374 is that later edit. **`grant-grc-0001` was void from T1** — by the
ratified rule itself, not by any daemon, reconciler or hook. Nothing in this
estate writes `state: revoked` into a grant file; §7.2 says so in terms.

### 3.4 The two-body coupling did NOT fire — checked, not assumed

Q-GRC-2 (RULED 2026-09-06T14:13:46Z) couples the two bodies on an
**ENROLLED-ROSTER pin flip**: *"a roster pin flip revokes both bodies' grants
and parks both."* **This event is not one.** No `model_version` moved; only this
holder's rendered prompt text did.

Checked: `test_a_gate_rules_prompt_edit_does_NOT_move_the_merge_readiness_pin`
passed on every variant; `merge_readiness_council`'s `rendered_set_digest`
renders unchanged at `sha256:751e03a2…`; and neither anchor string appears in
any of its four seats. **`grant-mrc-0002` is NOT revoked by this act and
`row-mrc-0001` is not touched.** A one-body re-issuance is the correct shape;
the two-body ceremony remains owed on the day a roster pin does move.

---

## 4. Step 1 — the superseded state, quoted and PROVED CURRENT

Both files were fetched from `origin/main` and **hash-compared against the
working tree before anything was edited** — `grant-grc-0001.yaml` at
`sha256:0b05215c3f879f108ee62374eb828aad813146f3f8f6ef002a60524641b330b0`,
identical local and remote. Step 1 is a record of what was ENDED, and a
reconstruction after the fact would not be one.

```yaml
grant_id: grant-grc-0001
audience: {wallet_ref: wal-agent-grc-0001, holder_ref: agent:gate-rules-council}
scope:
  acts: [review]
  objects: [opensoft/openxFactory]
  authority_tier: act
  approval_posture:
    hermes_approval_required_before_apply: true
    authority_agents_may_approve: false
    human_escalation_required_for: []
expires_at: "2027-06-30T00:00:00Z"
issued_at:  "2026-09-08T12:31:36Z"
issued_by:  Brett.Heap@opensoft.one
state: active
```

and the backing row, **as a set of all nine fields**, because the reader
enforces exact set equality over them: `row_id: row-grc-0001`,
`holder_ref: agent:gate-rules-council`, `wallet_ref: wal-agent-grc-0001`,
`target_repo: opensoft/openxFactory`, `act: review`, `authority_tier: act`,
`grant_ref: grant-grc-0001`, `expires_at: "2027-06-30T00:00:00Z"`,
`state: active`.

---

## 5. Step 5 — the acts, verbatim

**Three writes and one non-write, in ONE commit** (`a30b8234`), per the
runbook's §5.1. There is no ordering of the three that is green halfway — the
reader checks that a row's `grant_ref` names a grant whose `state` is `active`
and whose `expires_at` equals the row's — which is why they are one commit.

### 5.1 REVOKE — `grant-grc-0001`, in place

| | |
|---|---|
| **File** | `governance/review-authority/grants/grant-grc-0001.yaml` |
| **`state`** | `active` → **`revoked`** |
| **`revocation.revoked_at`** | **`2026-09-11T02:12:30Z`** |
| **Reason class** | **DRIFT** |

**`revocation.reason`, verbatim:**

> DRIFT: declared composition change — `agent-mixes.yaml` component 2, the
> gate_rules_council prompt-corpus pin, moved under the ratified change
> clarify-gate-rules-decline-position (row C+: decline-vs-refuse by standing;
> tool-less `executed` guard); codexFactory
> 02e14c086d5ead77d0c390c33ba5df622f07a4df, PR #374, 2026-09-10. A declared
> composition change ends this holder's certified identity at once, with no
> tolerance band and no grace period. Re-issued as grant-grc-0002 by the
> register act of 2026-09-11 (walk-2026-09-11-register-act.md). Terminal: this
> grant never returns to active.

**587 characters against the pinned schema's `maxLength: 600`.** Recorded
because it is a real constraint that shaped the wording: a first draft carrying
the full clause description measured **661** and was refused by the schema
before it could be written. The detail that did not fit lives in the file's own
appended header and in §3 above — not dropped, relocated, and said so here.

**The reason NAMES THE COMPOSITION EVENT**, because *"a revocation whose reason
does not name what caused it is indistinguishable from an outage."*

**DRIFT propagates exactly as CAUSE** — *"no derived authority survives on the
strength of its parent's reason."* `grant-grc-0001` is a ROOT grant and no grant
in this tree declares it as `parent_grant_ref` (checked). **The propagation is
VACUOUS here, and is recorded as vacuous rather than as satisfied.**

**TERMINAL, NOT SUSPENDED.** *"A revoked grant SHALL NEVER return to the active
state."* **Nothing above the file's existing header was rewritten**; a dated
`# ====` section is appended beneath it, and the present-tense sentences above
it — the scope, the expiry, the resolution paths — are explicitly re-pointed by
that block rather than edited.

### 5.2 MINT — `grant-grc-0002`

New file: `governance/review-authority/grants/grant-grc-0002.yaml`.

| Field | Value |
|---|---|
| `schema_version` / `kind` | `1` / `xfactory_wallet_grant` |
| `grant_id` | **`grant-grc-0002`** |
| `audience.wallet_ref` / `audience.holder_ref` | `wal-agent-grc-0001` / `agent:gate-rules-council` — **unchanged** |
| `scope.acts` | `[review]` — carried forward, re-examined |
| `scope.objects` | `[opensoft/openxFactory]` — carried forward, re-examined |
| `scope.authority_tier` | `act` — carried forward, re-examined |
| `scope.approval_posture` | identical to `grant-grc-0001`'s, **byte for byte** (`diff` of the four lines is empty) |
| `expires_at` | **`"2027-06-30T00:00:00Z"`** |
| `issued_at` | **`"2026-09-11T02:12:30Z"`** |
| `issued_by` | **`Brett.Heap@opensoft.one`** |
| `state` | `active` |
| `parent_grant_ref` | **ABSENT — this is a ROOT grant.** `parent_grant_ref` means DERIVED FROM, and a superseding grant is not derived from the one it replaces |

**Every schema-required field is present** — `schema_version`, `kind`,
`grant_id`, `audience`, `scope`, `expires_at`, `state` — and the file validates
against the **pinned** schema (`openXwallet/contracts/openxwallet/openxwallet-grant.schema.yaml`,
`sha256:fde433c5821e2e6f62926a72c58a67a784961d2e9e27e9f2b3520fcc8e738e88`,
matching `contracts/openxwallet-pin.yaml`'s digest row) under a
Draft 2020-12 validator. So does the amended `grant-grc-0001`.

**THE SCOPE WAS RE-EXAMINED, NOT COPIED**, and the reasons are on the file's own
face. The one worth repeating here: `acts: [review]` stands, and the clause that
moved is a constraint *on* the review act — how a seat may decline or refuse,
and when `executed` may be claimed on a tool-less lane. **That tightens how the
act is discharged; it is not a new act**, and widening the act set on a
re-issuance would smuggle authority through a recovery.

**NO GAP BETWEEN REVOCATION AND ISSUANCE.** `revoked_at` and `issued_at` are the
same instant, taken once from `date -u` and written into three places —
asserted programmatically, not eyeballed.

### 5.3 REPOINT — `row-grc-0001`

File: `governance/review-authority/register.yaml`.

| Field | Before | After |
|---|---|---|
| `grant_ref` | `grant-grc-0001` | **`grant-grc-0002`** |
| `expires_at` | `"2027-06-30T00:00:00Z"` | **`"2027-06-30T00:00:00Z"` — DOES NOT MOVE** |
| `state` | `active` | **`active` — UNCHANGED** |
| `row_id`, `holder_ref`, `wallet_ref`, `target_repo`, `act`, `authority_tier` | unchanged | unchanged |

**`grant_ref` IS THE ONLY FIELD THAT MOVES.** This is where this act differs
visibly from the 2026-09-02 precedent, which moved `expires_at` as well
(`2026-11-23T12:00:00Z` → `2027-06-30T00:00:00Z`). Here the ruled expiry is the
same string, so the field is character-for-character equal to
`grant-grc-0002`'s — asserted, because the reader compares the two and any drift
is a `register-grant-mismatch`. **The string being unchanged is a RESULT, not a
short-cut**: §6.2 records that the expiry was ruled afresh.

**The row's own `state` stays `active`** — the row is the authority's continuing
existence, not the grant's. A revoked grant does not deactivate the row that was
repointed off it.

**All four gate-rules `seat_keys` entries still resolve — checked, not
assumed.** All four name `authorizing_row: row-grc-0001`; that row is still
`state: active` and still unexpired; none of the four names a grant, so none
moved; and the pinned reader confirmed it on the amended tree, emitting
`intake register: 8 of 8 per-seat signing key(s) adjudicated and resolved`.

**`revocation_staleness_bound: P7D` is untouched.** One bound governs the whole
register, and tightening it is its own governed edit, never a tidy-up inside a
re-issuance.

### 5.4 THE NON-WRITE — no row was added

**No second row for this holder.** The row still carries **exactly nine
fields**, which the reader enforces as exact set equality (verified: the parsed
row has nine keys). **The composition was not smuggled onto the row:** there is
no model field on a row, adding one would be refused, and this act added none.

### 5.5 THE OTHER NON-WRITES, enumerated so their absence is a decision

Three files name `grant-grc-0001` and were deliberately **not** edited, matching
the precedent, which likewise touched only the three:

* `governance/review-authority/wallets/wal-agent-grc-0001.yaml` — names
  `grant-grc-0001` only in prose recording what it was minted alongside; carries
  no `grant_ref` field. The wallet is unchanged by a composition event: the
  wallet that must prove possession at exercise is the same wallet.
* `governance/review-authority/attestations/custody-attest-wal-agent-grc-0001.yaml`
  — likewise prose only; the custody attestation is untouched by this event and
  is the unchanged basis on which tier `act` still stands.
* `openspec/changes/register-gate-rules-council-seats/tasks.md` — **no task row
  is ticked by this act.** Checked: this change's §4 "Downstream owed acts"
  contains no re-issuance task, and its §5.1 archive-evidence set does not
  include this act. This act files its record in this directory because that is
  this holder's walk-record home (task 3.9's naming convention), **not** because
  it discharges a task here.

`contracts/CHANGELOG.md` also names the old grant in a dated historical entry
and is correctly left standing.

---

## 6. Step 4 — the R8 five-field record

> **R8 — the five fields are the MINIMUM.** *"A re-issuance act records the
> superseding grant reference, the superseded grant reference, the composition
> hash issued against, the ratifying human, and the effective time … a floor a
> carrying change may extend, and NOT a ceiling."*

| R8 field | Value |
|---|---|
| **superseded grant reference** | **`grant-grc-0001`** — root grant, issued `2026-09-08T12:31:36Z` by `Brett.Heap@opensoft.one`, backing `row-grc-0001`; now `state: revoked`, reason class **DRIFT** |
| **superseding grant reference** | **`grant-grc-0002`** — minted by this act. Root grant, no `parent_grant_ref` |
| **composition hash issued against** | **STILL PENDING R6/R7 — filled with a SUBSTITUTE, EXPLICITLY LABELLED ONE.** See §6.1 |
| **ratifying human** | **Brett Heap** (`Brett.Heap@opensoft.one`), the anchored responsible operator under the Human Escalation Contract |
| **effective time** | **`2026-09-11T02:12:30Z`** — one instant, taken once, written into all three places |

### 6.1 The composition hash — still PENDING, and what stands in for it

**NO CANONICAL DIGEST IS IMPLEMENTABLE YET, AND NONE WAS INVENTED.** R6 (the
plane sits INSIDE the digest) and R7 (JCS / RFC 8785, `sha256:<lowercase-hex>`,
recorded with the canonicalization profile name and version) remain
**ratification targets**, and the change that carries them is still not
authored. Recorded instead, **as substitutes, so labelled**:

1. **The declaring commit** — codexFactory
   **`02e14c086d5ead77d0c390c33ba5df622f07a4df`** (PR #374, T1).
2. **The holder's own declared digests** — the five row-C+ values in §3.2, read
   back from the live file at this act.

**NEITHER IS THE R6/R7 DIGEST**, and neither covers the provider plane — which
is exactly what R6 says the real digest must. A locally-invented digest recorded
in the hash's place is worse than an empty field, because a later reader cannot
tell the two apart. This is the precedent's own method (§4.1 of
`walk-2026-09-02-register-act.md`), followed deliberately.

### 6.2 The expiry — RULED AFRESH, at the same value

**`expires_at: 2027-06-30T00:00:00Z`**, ruled by **Brett Heap at
`2026-09-11T02:03:35Z`**, choosing **option A of two offered**:

* **Option A (taken)** — keep `2027-06-30T00:00:00Z`. The date is bound to the
  earliest published retirement floor among this council's pinned model
  identifiers (`claude-opus-5` for `lead-architect`/`lead-security`,
  `claude-sonnet-5` for `lead-quality`/`company-policy-lead`). **PR #374 moved
  no model identifier** — only rendered prompt text — so the floor the date is
  bound to has not moved either. Q-GRC-3's operational reason also still holds:
  `grant-mrc-0002` carries the same date, so one re-issuance ceremony covers
  both bodies.
* **Option B (rejected)** — a fresh date bound to some other named artifact.

**A re-issuance chooses its expiry AFRESH** (runbook §5.1 act 2). The number is
the same; **the choosing is new**, and what carried it forward is the BINDING —
re-checked against this event — rather than the convenience of the string
already being there. Recorded explicitly because a reader who saw only the diff
would see `expires_at` not move and could reasonably mistake a ruling for an
omission.

**THE HONEST CAVEAT, the runbook's §6.1 own:** *nothing in this estate reads a
retirement date.* What IS enforced is this date itself, computed by the reader
at read time (`register-row-expired`, `grant-state-stale`). On 2027-06-30 every
gate-rules convening parks — **if and when one runs; none ever has** (§9.3). The
sentence describes the control's shape, not an observed behaviour.

### 6.3 `issued_by` — CARRIED FROM THE PRECEDENT, AND FLAGGED FOR CONFIRMATION

`issued_by: Brett.Heap@opensoft.one`. This is **the same identity the precedent
grant carries** — verified by reading `grant-mrc-0002.yaml`, which was minted by
the 2026-09-02 register act with exactly this value, and by `grant-grc-0001`,
whose cold start used it too. It is not a guess and not a house style: it is the
anchored operator identity under the Human Escalation Contract, and the schema
widened `issued_by`'s grammar specifically so it could carry an operator's email
address.

**It is nonetheless FLAGGED on the pull request as "confirm on merge"**, because
`issued_by` is the field that names who issued this authority, and a coordinator
composing bytes on a ratifier's word should not be the last party to have
checked it.

### 6.4 Beyond the minimum — what this act carries on top

R8 is a floor, and adding is the ruling working as intended:

* the citations of §3 and §10, each verified live at this act;
* **the supersession, IN PROSE** — no field carries it (§5.2); it lives in this
  record, in `grant-grc-0002`'s header, and in `grant-grc-0001`'s appended
  revocation block, and nowhere else;
* **the measured gate result** (§6.5) — including the explicit re-proof that the
  precedent's blocking defect does not recur;
* the vacuous propagation (§5.1) and the non-firing two-body coupling (§3.4),
  each recorded as checked rather than as satisfied;
* the non-writes of §5.4 and §5.5.

### 6.5 THE MEASUREMENT — the gate this act had to pass, and did

Run over the amended tree at commit `a30b8234`, from the worktree root, using
**the literal invocation the required check pins**:

| Command | Result |
|---|---|
| `python3 scripts/verify-openxwallet-pin.py` | `OK openxwallet-pin verified: openXwallet@f3eb929b… (tag label wallet-v1.5), gitlink read from HEAD, 8 digest(s) recomputed` |
| `python3 openXwallet/scripts/wallet-yaml-syntax-gate.py .` | exit 0 |
| `python3 openXwallet/scripts/validate-openxwallet.py .` | **`0 error(s), 0 warning(s)`** |
| the consumer gate's six positive log assertions, re-run verbatim | **all hold** |
| `python3 scripts/validate-factory-identity.py .` | `0 error(s)`; disjointness holds, **0 shared** |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | `change/register-gate-rules-council-seats` **✓**; totals unchanged from the pre-edit baseline (3 pre-existing failures, none introduced by this act — §6.6) |

The notes the pinned reader emitted, which are the positive proof the register
was OPENED rather than skipped:

```
note  intake register read: governance/review-authority/register.yaml (2 row(s))
note  intake register: 8 of 8 per-seat signing key(s) adjudicated and resolved
note  wallet 'wal-agent-grc-0001': 5 declared key(s) adjudicated (…)
note  wallet 'wal-agent-mrc-0001': 5 declared key(s) adjudicated (…)
note  repo scan: 10 openxWallet artifact(s) validated, 2169 document(s) skipped as another kind
```

**`register-no-active-row` DID NOT RECUR — and that was proved, not assumed.**
The 2026-09-02 act could not pass this gate at all: at `wallet-v1.3` the pinned
reader's `check_register` closing loop iterated every review-class grant and
never filtered on grant STATE, so it demanded a backing ACTIVE row for the
correctly revoked `grant-mrc-0001`. That was a reader defect, not an act defect,
and it was fixed in openXwallet #14 (`b7b0fbb3`, `wallet-v1.4`). This repository
now consumes `wallet-v1.5`. **The draft that prepared this act said to prove the
fix fresh rather than trust the pin label; it was proved fresh, over this act's
own amended tree, and the finding is absent.**

### 6.6 The openspec baseline, taken BEFORE the edits

`openspec validate --all --strict` was run on the unedited branch first, so a
pre-existing failure could not be mistaken for one this act introduced:
**97 passed, 3 failed** — `change/disposition-codexfactory-declared-renames`,
`change/disposition-codexfactory-floor-relocation-retitle`, and
`spec/repo-boundary-governance` (the last is the subject of open PR #937). The
same three, and only those three, fail after this act.

---

## 7. CAPACITY DISCLOSURE (runbook §0.3)

**Brett Heap holds three capacities in this act and they are disclosed rather
than collapsed** — the runbook's own instruction. **Two further capacities are
machine-held and are disclosed for the same reason.**

| Capacity | The act held in it | Where exercised |
|---|---|---|
| **the OPERATOR** | evidencing exact provider identity and the plane (R5) | **N/A here** — no `model_version` moves in this packet, so no operator identity evidence is owed. The standing record (`operator-identity-record-2026-09-01.md`) is unmoved and unre-derived |
| **the CONVENER** | accepting the Council's output on record | the LANE-DEFECT-FIRST ruling, codexFactory issue #279 comment 5622264144, 2026-09-10T16:48:53Z, and the packet ratification 2026-09-10T21:46:19Z |
| **the RATIFYING HUMAN** | **the register act itself** (R11: REGISTER is the only human-ratified act, and RE-ISSUE always requires one) | this change — the expiry ruled at §6.2, the filing location ruled at §1, the effective instant, the reason class |
| **the COORDINATOR** — the lane session `hermes-wallet-exercise`, **not** the ratifying human | **COMPOSING the candidate bytes** on the ratifier's word, and **performing the merge** on his separate, later word | this pull request |
| **the AUTHORING AGENT** — an Opus agent directed by the lane | writing this record, both grant headers and the register row's comment | this change directory |

### 7.1 What is Brett Heap's, and what is not

**What is his is the ACT**: the decision to re-issue, the reason class DRIFT,
the effective instant, the expiry ruled as option A, the filing location, and
the merge word. **What is not his is the typing and the button.** He ruled
exactly that at **2026-09-11T02:03:35Z**: the lane composes this pull request,
he reviews it and gives the merge word — with himself as **author of record**
holding Operator + Convener + Ratifier, and the lane as **Coordinator**, the
same role split the 2026-09-02 precedent's §7 recorded.

A capacity table that listed only the human's three would let a reader assume
the writing and the merging were his too, and §0.3's whole point is that roles
are named rather than collapsed — which does not stop applying at the boundary
where the holder stops being a person.

### 7.2 "Operator act" names whose act, not whose hands

R11 rules that revocation needs no ratifier because a fail-closed cascade must
not wait on a human. **That is not a claim that anything here performed it.**
NOTHING IN THIS ESTATE WRITES `state: revoked` INTO A GRANT FILE — there is no
daemon, no reconciler and no hook that walks a composition change into
`governance/review-authority/`. This write is an **operator act with a
machine-enforced refusal behind it**, and it must never be read as a cascade
that ran while nobody was looking.

### 7.3 THE MERGE IS A SEPARATE, LATER WORD

The word that authorized composing these bytes
(2026-09-11T02:03:35Z) is **not** the word that merges them. This pull request
is **NOT FOR MERGE** until Brett Heap says so. On that word the coordinating
lane merges — by **admin bypass**, exactly as the precedent did — and posts the
Rule 6 `LANDING` / `LANDED` lines and a provenance comment naming the act and
the word.

**Why an admin merge is the CORRECT route here and not a bypass of review.**
`register.yaml` declares on its own face that it is a *"PERMANENTLY HUMAN-ONLY
SURFACE … no council verdict may ever produce an autonomous approval of a change
to THIS file"*, and *"a council whose own commission is recorded here is never
eligible to clear a candidate that edits it."* The approval for this change is
the **ratifier's**, recorded here and on both grants' faces. There is no council
verdict to obtain, and obtaining one would be the violation. **For this file the
ordinary clearing lane is not a stricter option — it is an ineligible one.**

**A CORRECTION, carried forward from the draft that prepared this act.** The
human-only-ness of this surface is **not** a CODEOWNERS or branch-protection
gate: `.github/CODEOWNERS` on this repository routes five other surfaces to
`@brettheap` but **never** `governance/review-authority/` (checked in full).
It is a **ratified prose requirement**, honored by this discipline. Nothing in
GitHub will refuse a differently-routed merge of this path; only the ratified
rule and the ratifier's word do.

---

## 8. STEP 5b — THE PROJECTION. NOT DONE BY THIS ACT

**STUBBED — appended by Part C after T2.**

The register act does not reach the runtime. The Hermes register projection is
an operator-established, lagging copy, and **until it is re-derived from the
amended register the runtime keeps refusing with
`review_authority.root_key_mismatch` and NO AUTHORITY FLOWS.**
`revocation_staleness_bound: P7D` travels into it verbatim as
`projected_from.staleness_bound` and is unchanged by this act.

Part C fills, below this line:

* **the re-derivation itself** — the refresher tick or manual `project-register`
  run against the merged revision, with the `source-revision` it resolved;
* **the visible signal** — what changed in the `hermes-register-projection`
  ConfigMap annotations, read back rather than inferred;
* **the proof the projection carries `grant-grc-0002`'s constraints** and
  nothing this register does not say.

> *(appended by Part C after T2)*
> **2026-09-11 — Part C STOPPED here. Step 5b is NOT performed, and the "verify one convening admits" route named above does NOT reach the register projection at all. See §13.2.**
> **2026-09-11, LATER — SUPERSEDED BY §14.1: step 5b IS PERFORMED.** The route above still does not reach the register projection; an authorized read-only cluster read stands in its place, and the projection’s `source-revision` is `61cee60d` — ahead of this act. See §14.1.

---

## 9. THE HOLD, AND WHAT ACTUALLY LIFTS IT

### 9.1 Why a hold was needed at all — R9 does not cover this

**R9 is keyed on composition MISMATCH.** PR #374 moved the briefing text and the
five-value content pin **together**, so a convening run in the window between T1
and T2 passes every mechanical check while `grant-grc-0001`'s grants stand
revoked. **No mechanical park fires for this change** — that is not a defect in
this act, it is the reason the hold exists, and it is why §3.2's "no half of
that edit is green" property cuts both ways.

### 9.2 The window check (task 3.8) — STUBBED

**Appended by Part C after T2.** Part C confirms that **every**
`agent:gate-rules-council` convening between **T1 = `2026-09-10T23:34:23Z`** and
**T2 = the merge of this pull request** either did not occur, or parked with a
refusal naming the composition event — **never a silent pass**. The expected
finding is that none occurred (§9.3), and a checked absence is recorded as one
rather than assumed.

> *(appended by Part C after T2)*
> **2026-09-11 — FILLED. The window is EMPTY: no `agent:gate-rules-council` convening ran between T1 and the merge. See §13.1.**

### 9.3 "VERIFY ONE CONVENING ADMITS" — STUBBED, and it is the real exit

**A green validator does not lift the hold. An ADMITTED convening does.**

No `gate_rules_council` convening has ever run: codexFactory's
`.github/workflows/gate-rules-convening.yml` (workflow id 352457764) reported
`total_count: 0` at the cold start. Part C records **which convening was
watched, by run id**, and whether it was admitted against `grant-grc-0002`.

> *(appended by Part C after T2 — the proof convening's run id)*
> **2026-09-11 — No convening was dispatched, and §13.2 records why one would have proved nothing about review authority. See §13.4.**
> **2026-09-11, LATER — one convening WAS then dispatched: run `34561266626`, REFUSED HTTP 422 `council.self_review_refused`.** Not a register-side refusal, exactly as §13.2 predicted. See §14.3.

### 9.4 The hold lift — STUBBED

**Appended by Part C after T2.** The hold posted at §1 lifts on the coordinating
lane's own comment on codexFactory PR #374 and issue #279, citing this record by
the path in §1 and the merge commit of this pull request beside it.

> *(appended by Part C after T2)*
> **2026-09-11 — NOT LIFTED. The hold posted at §1 remains IN FORCE. See §13.3.**
> **2026-09-11, LATER — LIFTED**, 04:10:09Z–04:10:20Z, in all three places the hold was posted, citing both the act (`f0eea7ed`) and this record’s path and naming the wording mismatch. See §14.2.

### 9.5 TWO INSTANTS, AND THEY ARE NOT THE SAME — read this before citing either

This record carries two timestamps that a careless reader will conflate:

| | Value | What it is |
|---|---|---|
| **the EFFECTIVE INSTANT** | **`2026-09-11T02:12:30Z`** | the instant written into `revoked_at` and `issued_at`. Taken once from `date -u` at the moment the write began — **COMPOSE time**, which is exactly what the 2026-09-02 precedent did (`revoked_at` = `issued_at` = `2026-09-02T13:33:48Z`, against a merge at `2026-09-02T23:10:14Z`, ~9.6 h later) |
| **T2, the window boundary** | **the merge of this pull request** | what Part C's §9.2 window check measures to, because it is when the amended register reaches `main` and becomes the register anyone reads |

**They differ, and the gap is real.** Between the effective instant and the
merge, the files declare an authority that has not yet landed. **The hold, not
the timestamp, is what covers that gap** — which is precisely why the hold's
lift condition is an admitted convening rather than a filed record. Following
the precedent's convention here was deliberate: doing anything else would have
made this act's timestamps incomparable with the only completed re-issuance in
the estate.

---

## 10. THE WORDS AS SPOKEN

Brett Heap, in session, with UTC stamps, because a paraphrase is not a ruling
anyone can audit later.

| When (UTC) | Word | What it authorized |
|---|---|---|
| **2026-09-10T21:46:19Z** | *"ratify all as recommended"* | the packet `clarify-gate-rules-decline-position`: OQ-1 INCLUDE, OQ-2 (i) PROHIBITION + S2 — **row C+ / variant V2S** |
| **2026-09-10T22:50:06Z** | *"open the governed path"* | opening the landing of PR #374, the composition edit that is T1 |
| **2026-09-10T16:48:53Z** | *"merge 344 and 410, lane-defect-first"* | the LANE-DEFECT-FIRST ruling, #279 comment 5622264144; soak PRs #344 → `3fae7858`, #348 → `368ba140` |
| **2026-09-11T02:03:35Z** | the multi-choice rulings | **(1)** the lane composes this pull request and he reviews it and gives the merge word, as author of record holding Operator + Convener + Ratifier with the lane as Coordinator; **(2)** `grant-grc-0002`'s `expires_at` = `2027-06-30T00:00:00Z`; **(3)** the walk record files at `openspec/changes/register-gate-rules-council-seats/walk-<T2 date>-register-act.md` |
| **PENDING** | the merge word | §7.3 — the second, separate word. **Not yet given.** |

---

## 11. THE HONEST LIMITS, RESTATED IN TERMS (runbook §7)

* **R8/R9 ARE NOT ENFORCED.** The change carrying R6–R12 is not ratified. This
  act demonstrates the runbook against a real event; it does not exercise an
  enforced control.
* **The composition hash is a labelled SUBSTITUTE**, not the real R6/R7 digest,
  and it does not cover the provider plane (§6.1).
* **No field records the supersession.** It lives in this record, in
  `grant-grc-0002`'s header and in `grant-grc-0001`'s appended revocation
  block — and nowhere else (§5.2).
* **This act does not reach the runtime.** Step 5b is Part C's (§8).
* **This act does not lift the hold.** An admitted convening does (§9.3).
* **No convening has ever run for this holder**, so "verify one convening
  admits" has never once been exercised in this estate for `gate_rules_council`.
* **The human-only surface is prose, not a technical gate** (§7.3).
* **This record is written BEFORE the merge.** Its §8 and §9 stubs are owed, and
  a reader who finds them still unfilled should read this act as composed and
  landed but **not yet operative**.

---

## 12. REVERSIBILITY

**Before this act lands:** fully reversible — revert the branch, and nothing has
been written to `governance/review-authority/` on `main`.

**After it lands: there is no rollback, only a further governed re-issuance.**
The ratified core rule is terminal: *"A revoked grant SHALL NEVER return to the
active state. Authority resumes only as a NEW grant, which records the grant it
supersedes."* Undoing this in spirit means reverting PR #374's commit — restoring
the old composition — **and then walking this entire register act again** to
issue a THIRD grant (`grant-grc-0003`) against the reverted composition. A full
second ceremony, not a `git revert`.

That asymmetry is exactly why the build and the register act are opened as one
deliberate pair rather than treating the register act as a formality that can be
deferred.

---

## 13. DATED APPEND — 2026-09-11, PART C, AND IT IS **INCOMPLETE**

**Appended 2026-09-11 by the coordinating lane `hermes-wallet-exercise`, after
this record reached `main` (PR #941 → `f0eea7ed1af5a3b7cc247adc8316e04e4b610dc0`,
merged `2026-09-11T02:29:10Z`). Nothing above this line is rewritten.** The only
other change this append makes to the file is a one-line dated POINTER under each
of §8, §9.2, §9.3 and §9.4's stub markers, directing a reader here; no existing
sentence is altered or removed, and the diff proves it. This follows
`openxFactory/docs/document-lifecycle.md`'s rule for a document already at
`Status: record`: *"if it has to be revisited later … it stays open or gets a
dated append, never silently rewritten."*

**READ THIS FIRST.** Part C ran, and it **stopped**. Of the four stubs this
record left for it, **ONE is filled (§9.2, the window check) and THREE are still
owed (§8, §9.3, §9.4).** The hold posted at §1 **IS STILL IN FORCE.** No
convening was dispatched, no lift was posted anywhere, and `tasks.md` 3.6 and 3.8
remain unticked. The reason is not caution: it is a defect in the exit condition
this record and its runbook both name, set out at §13.2 below.

> **POINTER ADDED 2026-09-11, LATER — §13 IS NO LONGER THE LAST WORD. §14 closes Part C: step 5b is performed (§14.1), the hold IS LIFTED (§14.2), and one convening was dispatched and refused (§14.3). §13 is left exactly as written because it was true when written.**

### 13.1 §9.2 — THE WINDOW CHECK (task 3.8): **CLOSED, AND THE FINDING IS EMPTY**

**No `agent:gate-rules-council` convening ran in the window. Nothing was consumed
under revocation.** A checked absence, recorded as one.

The command, verbatim, run `2026-09-11T02:36Z` by the landing lane, read-only:

```sh
gh run list -R codeXfactory/codexFactory --workflow gate-rules-convening-trigger.yml \
  --json databaseId,createdAt,event,conclusion,headSha --limit 100
```

It returns **five runs in the workflow's entire history**, and **every one of
them predates T1** — the latest by more than ten hours:

| run | createdAt | event | conclusion |
|---|---|---|---|
| `34481205558` | 2026-09-10T13:12:32Z | workflow_dispatch | success |
| `34480882955` | 2026-09-10T13:09:22Z | workflow_dispatch | failure |
| `34318204178` | 2026-09-09T06:14:39Z | workflow_dispatch | failure |
| `34317084150` | 2026-09-09T05:59:09Z | workflow_dispatch | failure |
| `34307939608` | 2026-09-09T03:39:04Z | workflow_dispatch | failure |

Filtered to the window, the result is **`[]`**.

**THE TWO CANDIDATE UPPER BOUNDS DISAGREE, AND THE FINDING SURVIVES BOTH.**
`tasks.md` 3.8 says the window runs to *"the step-4 effective time"* —
`2026-09-11T02:12:30Z`, this record's effective instant. §9.2 above says it runs
to *"T2 = the merge of this pull request"* — `2026-09-11T02:29:10Z`. The wider
bound strictly contains the narrower, the window is empty under the wider, and so
it is empty under both. The disagreement is recorded rather than quietly resolved,
because a later reader comparing the two documents will find it.

**The ~17-minute gap between the two instants is real, and it is covered by the
HOLD, not by either timestamp** — §9.5 says so already, and Part C confirms the
gap was uneventful in fact as well as in principle.

**Two independent cross-checks, because one empty list is not a finding:**

* **The records side.**
  `gh api "repos/codeXfactory/codexFactory/commits?path=hermes/domain/review-councils/records&since=2026-09-10T23:34:23Z&until=2026-09-11T02:29:10Z"`
  → **`[]`**. No convening record was committed inside the window.
* **The trap named in 3.8, avoided and recorded as avoided.**
  `gh run list … --workflow gate-rules-convening.yml` → `[]`, which is a **FALSE
  NEGATIVE** and carries no evidential weight: that file is `workflow_call`-only
  and reports zero runs of its own whether or not one occurred. It was not relied
  on.

**A THIRD CHECK THE TASK DID NOT ASK FOR, AND IT MATTERED.** Enumerating *every*
workflow run in codexFactory inside the window returns **243 runs, of which 104
are council-shaped** — 52 `council-deliberation-worker.yml`, 26
`council-convening-lane.yml`, 26 `council-authorization-trigger.yml`. **None is a
gate-rules convening**, and that is established from the files' own headers rather
than from their names: `council-convening-lane.yml` *"Commissions a
**merge-readiness** council convening"*; `council-authorization-trigger.yml`
*"recognizes stamped **merge-readiness** convenings"*;
`council-deliberation-worker.yml` *"A commissioned **merge-readiness**
convening"*; and `gate-rules-convening-trigger.yml`'s own design note records that
the reusable those three callers use *"hard-codes `merge_readiness_council`"*.
That trigger is the only file in the repository naming
`council_id: gate_rules_council`. A sampled in-window run (`34554768628`,
`council-convening-lane`, 2026-09-11T02:28:42Z, `event: schedule`) resolved and
then **skipped** its `convene` job — a clean no-op.

These 104 runs belong to `merge_readiness_council`, whose grant `grant-mrc-0002`
this act did **not** revoke (§3.4). They are therefore not "CONSUMED UNDER
REVOCATION" candidates, and it would be wrong to record them as such.

### 13.2 §8 — STEP 5b: **NOT PERFORMED, AND THE ROUTE THIS RECORD NAMES FOR PROVING IT DOES NOT REACH IT**

This is the finding that stopped Part C, and it is a defect in the exit
condition, not in the register act.

**The claim under test.** `design.md` §D4 Step 5b, the runbook, and the Part C
brief all hold that *"verify one convening admits"* is the actual exit condition,
and that dispatching one real gate-rules convening is therefore itself the
no-cluster proof that the register projection has been re-derived and carries
`grant-grc-0002`. §9.3 above restates it: *"A green validator does not lift the
hold. An ADMITTED convening does."*

**It does not hold. THERE ARE TWO DIFFERENT PROJECTIONS AND THE CLAIM CONFLATES
THEM.**

1. **The DOMAIN-CONTENT projection** — the layer's materialized `review_council`
   content. The convening trigger *does* read it, at its step **"Verify the
   domain-content projection carries this council"**
   (`gate-rules-convening-trigger.yml:273`). Its refusals are
   `domain_content_council_absent`, `domain_content_unseeded` and
   `domain_content_read_unauthorized` — all of which are about council *content*,
   none about review *authority*.
2. **The REGISTER projection** — ConfigMap `hermes-register-projection`, refreshed
   by the `0 */2 * * *` CronJob. **This** is the document that carries grant state
   and raises `review_authority.register_stale` and
   `review_authority.grant_revoked`.

**The convening admission path never reads (2).** Established three independent
ways against shipped code and this estate's own landed records:

* **`admit_convening` and `admit_layer_convening`**
  (`hermes-install/src/hermes_install/domain/council_orchestration.py`) take
  `review_council`, `deliberation_mix`, `content_provenance`,
  `existing_convening`, `machinery_map`, `resolver` and `head_resolver`. **No
  projection path. No `SeatExerciseGate`.** There is no parameter through which a
  register projection could reach admission.
* **The register projection is read by `DatabaseSeatExerciseGate`, and that gate
  is constructed inside `verdict_for_completion`** — same module, which passes it
  `projection_path` and `max_staleness_seconds`, and whose docstring says it
  *"builds the `SeatExerciseGate` that reads the register projection … and hands
  it to `check_verdict`."* So `register_stale` and `grant_revoked` are
  **verdict-completion** refusals. They cannot fire at admission.
* **This lane never reaches verdict completion, by ratified design.**
  `gate-rules-convening.yml`'s own header: *"IT CONVENES NO SEAT, INVOKES NO MODEL
  AND SIGNS NO SEAT RETURN. Those are legs 3 and 4"*, and wiring them is ratified
  **phase 6**, whose *"gate is not met (leg 4 does not exist, so the lane would
  have no signer)."* codexFactory's own landed record of the one successful
  precedent —
  `hermes/domain/review-councils/records/2026-09-10-gate-rules-first-signed-convening.md`
  — says it in terms: ***"NO SEAT WAS CONVENED, NO MODEL WAS INVOKED, AND NO SEAT
  RETURN WAS SIGNED"***, *"No verdict, no disposition"*, and *"openxFactory task
  4.5 stays OPEN. It names the first signed convening in the **seat-return**
  sense. This run signed the ORIGIN attestation over a request; it signed no seat
  return."*

**What an ADMITTED gate-rules convening therefore proves:** that the
domain-content projection carries the council; that the posted `subject_pin`
equals the candidate pull request's live head; that no prior non-failed convening
exists for that pin; and that a sealed, origin-signed request was published. **It
proves nothing whatever about the register projection, `grant-grc-0002`, or
whether any authority flows.**

**AND DISPATCHING ONE NOW WOULD HAVE BEEN WORSE THAN USELESS — IT WOULD HAVE
MANUFACTURED A CLEARANCE.** The register projection's last scheduled tick before
this append was **02:00Z**, which is *before* the merge at 02:29:10Z, so the live
projection was derived from an openxFactory revision at which `grant-grc-0001`
was still `active`. Even a consumer that *did* read it would not refuse: the
currency gate compares the projection's age against
`min(declared P7D, DEFAULT_MAX_STALENESS_SECONDS = 7 × 24 × 60 × 60)` = **P7D**,
and a forty-five-minute-old projection is nowhere near that bound. So the
predicted `register_stale` / `grant_revoked` refusal would **not** have appeared.
A green ADMISSION would have — and this record's §9.3, the runbook and the brief
would all then have read that green as the proof that lifts the hold. That is
precisely the *"treat a mechanically-green run as clearance"* forgery the
governed-re-issuance discipline refuses. **The proof convening was therefore not
dispatched.** Declining to run it also avoided irreversibly consuming a candidate
pin: a non-failed convening refuses any second commissioning for the same
(council, subject pin) forever.

**WHAT THIS MEANS FOR 5b.** There is **no GitHub-visible artifact of the register
projection's live content** — the ConfigMap exists only on-cluster and nothing
commits it. With the convening route eliminated, **the only remaining proof is an
on-cluster read**, which this lane does not perform: no `az` or `kubectl`
invocation was made. **It requires Brett Heap's operator word and a named
executing lane**, doing one of:

1. read the `hermes-register-projection` ConfigMap and confirm its `row-grc-0001`
   entry reads `grant_ref: grant-grc-0002` with the matching `expires_at`, that
   `projected_from.staleness_bound` still carries `revocation_staleness_bound`
   **`P7D`** verbatim, and that the projection's own
   `hermes.opensoft.one/source-revision` annotation resolves to
   `f0eea7ed1af5a3b7cc247adc8316e04e4b610dc0` **or later** — that annotation is
   what distinguishes a post-merge projection from the pre-merge one, and it is
   the field to check; or
2. run `hermes-lifecycle project-register` by hand against the merged revision to
   force a tick rather than waiting for the scheduled window.

**`tasks.md` 3.6 stays unticked.**

### 13.3 §9.4 — THE HOLD: **NOT LIFTED. STILL IN FORCE.**

Nothing was posted to codexFactory issue #279, to PR #374, or to `LANES.md`. The
hold's own condition is unmet, and its text is exact about what does not satisfy
it: *"Not elapsed time, not a green suite, not a re-run."*

**A WORDING MISMATCH THE EVENTUAL LIFT MUST NAME RATHER THAN PAPER OVER.** The
hold posted at 2026-09-10T23:20:38Z describes the lifting record as existing *on*
`opensoft/openxFactory:governance/review-authority/`. Brett Heap's ruling of
2026-09-11T02:03:35Z filed this record at
`openspec/changes/register-gate-rules-council-seats/walk-2026-09-11-register-act.md`
instead — beside both prior walks, and §1 above already explains the split: the
**ACT** is under `governance/review-authority/` (the three writes, landed as
#941 → `f0eea7ed`), while the **RECORD** of it lives where the walks live. The
two are not in conflict, but a lift that cites only one of them would not visibly
satisfy the hold's literal text. **When the lift is eventually posted it must
cite BOTH** — the act's merge commit `f0eea7ed` on
`governance/review-authority/`, and this record's path as the record id — and
name the mismatch, so the lift reads as satisfying the hold by its substance. The
original hold postings are not to be reworded.

### 13.4 §9.3 — THE PROOF CONVENING: **NOT DISPATCHED**

No run id, because no run. See §13.2 for why, and for why this is a refusal to
manufacture evidence rather than an omission. When the estate is ready to
exercise this properly, the honest exercise is a convening that reaches **seat
return and verdict completion** — ratified phase 6 — because that is the only
path on which the register projection is consulted at all.

### 13.5 The five digests, cross-checked rather than retyped

The ten values in §3.2 were re-read from this record on `main` at this append and
compared character-for-character against the Part C brief's independently carried
"Known constants" list. **All ten agree**, before and after, for
`rendered_set_digest`, `lead-architect`, `lead-security`, `lead-quality` and
`company-policy-lead`. They are not restated here; §3.2 is the single copy, which
is the point.

### 13.6 What is owed, and by whom

| Owed | Whose | Blocked on |
|---|---|---|
| §8 / `tasks.md` 3.6 — the 5b projection proof | a named operator lane | **Brett Heap's operator word** for an on-cluster read or a manual `project-register` tick (§13.2) |
| §9.3 — a convening that actually exercises review authority | the estate | ratified **phase 6** (legs 3 and 4); not a Part C act |
| §9.4 — the hold lift | lane `hermes-wallet-exercise` | 5b above; and it must cite both the act and this record (§13.3) |
| `tasks.md` 3.8 tick | lane `hermes-wallet-exercise` | **this append reaching `main`** — the finding at §13.1 is what 3.8 ticks against |

**This record stays `Status: record`** — it records, accurately, an act that was
performed and a follow-on that was stopped with its reason. It is not `Status:
draft`, because nothing here is provisional; §13.2's finding is as much a result
as a green would have been.

---

## 14. DATED APPEND — 2026-09-11, PART C **CLOSE-OUT**

**Appended 2026-09-11 by the coordinating lane `hermes-wallet-exercise`, after
§13 itself reached `main` (PR #948 →
`fa94dfb5bae699f83b0c51205ab6a7ba4e0acc80`, merged 2026-09-11T03:19:58Z).
Nothing above this line is rewritten.** As with §13, the only other change this
append makes is a one-line dated pointer under each of §8, §9.3 and §9.4's
markers, directing a reader here; the diff carries **zero deletions**, which is
the proof. Same lifecycle rule as before
(`docs/document-lifecycle.md`): a document at `Status: record` *"stays open or
gets a dated append, never silently rewritten."*

**READ THIS FIRST.** Of the three stubs §13 left owed, **two are now filled and
one is answered by a finding rather than by the result it asked for.**

| Stub | §13 left it | §14 leaves it |
|---|---|---|
| **§8** — step 5b, the projection | NOT PERFORMED | **PERFORMED** — by an authorized read-only cluster read, §14.1. `tasks.md` 3.6 ticks. |
| **§9.4** — the hold | NOT LIFTED, still in force | **LIFTED**, in all three places the hold was posted, §14.2 |
| **§9.3** — the proof convening | NOT DISPATCHED | **DISPATCHED ONCE AND REFUSED** — `council.self_review_refused`, §14.3. It is not a register-side refusal, and §13.2 already said it could not have been one. |

### 14.1 §8 — STEP 5b: **PERFORMED, BY THE SUBSTITUTE §13.2 CALLED FOR**

**The authority.** Brett Heap, multi-choice ruling **2026-09-11T03:01:28Z**,
verbatim: *"Operator word: hermes-wallet-exercise reads it."* §13.2 had left 5b
owed to *"a named operator lane"* on *"Brett Heap's operator word"*; this is that
word, and the named lane is `hermes-wallet-exercise` — the same lane that
coordinated the act. **ONE read-only cluster read, no change.**

**The wait condition, met rather than assumed.** The register-projection
refresher's schedule is `0 */2 * * *`; the first tick after T2 (02:29:10Z) is
**04:00Z**. The read ran **2026-09-11T04:03:38Z–04:03:40Z** (the `az aks command
invoke`'s own `startedAt`/`finishedAt`), after that tick had already recorded a
success.

**How it was executed.** One `az aks command invoke` against
`aks-opensoft-platform-qa-01` / `rg-opensoft-platform-aks-qa` (`westus`;
subscription `sub-opensoft-platform-aks-qa`, the only cluster in it), namespace
`hermes` throughout, `exitCode` 0. **Every command was a `kubectl get` with
`-o jsonpath` or `-o custom-columns`** — no `apply`, `patch`, `create`,
`delete`, `edit`, `rollout`, or side-effecting `exec`. The cluster coordinates
were taken from hermes-install
`docs/evidence/refresher-installation-split-2026-09-10.md` read via `git show
origin/main:<path>` (no checkout, no pull, no working-tree mutation).

**What was read, verbatim:**

| | Value |
|---|---|
| CronJob `hermes-register-projection-refresher` `lastScheduleTime` | `2026-09-11T04:00:00Z` |
| …`lastSuccessfulTime` | `2026-09-11T04:00:08Z` |
| First Job created after T2 | **`hermes-register-projection-refresher-29818320`**, created `2026-09-11T04:00:00Z`, **`succeeded=1`** |
| ConfigMap `hermes-register-projection` → `hermes.opensoft.one/source-revision` | **`61cee60d85ec53a1107033fe0aea55ffe8987fa0`** |
| …`hermes.opensoft.one/projected-at` | `2026-09-11T04:00:02Z` |
| …`hermes.opensoft.one/projection-digest` | `sha256:10b1fb625bc704819140315c880fd8cf7c25111294c166fa0447b1a3cca92d3f` |
| …object `resourceVersion` / `creationTimestamp` | `36303438` / `2026-08-30T15:23:46Z` |

**THE TEST, AND IT PASSES.** §13.2 named the field to check:
*"the projection's own `hermes.opensoft.one/source-revision` annotation resolves
to `f0eea7ed1af5a3b7cc247adc8316e04e4b610dc0` **or later**."* Run locally,
read-only:

```sh
gh api repos/opensoft/openxFactory/compare/f0eea7ed1af5a3b7cc247adc8316e04e4b610dc0...61cee60d85ec53a1107033fe0aea55ffe8987fa0 --jq .status
```

→ **`ahead`**. `61cee60d` is `opensoft/openxFactory` `main` at
**2026-09-11T03:43:29Z** (the merge of PR #937,
`amend-repo-boundary-governance-scope-first-line`) — strictly after T2, and
after §13's own PR #948 (`fa94dfb5`, 03:19:58Z) as well. **The published
projection was derived from a revision of `main` that already carries this
act.** The council refresher is healthy on the same tick
(`lastSuccessfulTime` `2026-09-11T04:00:06Z`) — context, not part of the proof.

**STATED LIMIT, because a record that overclaims is worse than one that stops.**
This read establishes 5b **by source revision**: the projection's provenance
annotation names a revision that contains `grant-grc-0002` and the repointed
row. It does **not** read the ConfigMap's own data back. §13.2's option (i) also
listed the row-level confirmations — `row-grc-0001` reading
`grant_ref: grant-grc-0002` with the matching `expires_at`, and
`projected_from.staleness_bound` still carrying `revocation_staleness_bound`
**`P7D`** verbatim — and **those three fields were NOT separately read.** They
follow from the source revision only if the refresher is faithful to its input,
which is its whole job but is not a thing this read observed. Whoever next has
operator cause to touch that ConfigMap should read the three fields and note the
result; nothing here depends on it, and it is recorded as owed rather than
quietly treated as covered.

**Posted in full at** codexFactory
[#279 comment 5629286164](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5629286164)
(2026-09-11T04:05:40Z).

### 14.2 §9.4 — THE HOLD: **LIFTED**

Posted 2026-09-11T04:10:09Z–04:10:20Z, in the **same three places** the hold of
2026-09-10T23:20:38Z was posted, and nowhere else:

| Where | URL / id | UTC |
|---|---|---|
| codexFactory issue **#279** | [`issuecomment-5629329609`](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5629329609) | 2026-09-11T04:10:09Z |
| codexFactory PR **#374** | [`issuecomment-5629329846`](https://github.com/codeXfactory/codexFactory/pull/374#issuecomment-5629329846) | 2026-09-11T04:10:10Z |
| `LANES.md` (`opensoft/brett-wip` `lanes/LANES.md`, line 558) | commit `45a138c98e2b66dd3bc4f51ae6396b4016bddee4`, pushed to `origin/main` | 2026-09-11T04:10:20Z |

The lift sentence, as posted:

> LIFTED — the HOLD posted at 2026-09-10T23:20:38Z on `agent:gate-rules-council`
> convenings (lane hermes-wallet-exercise). Cause: the openxFactory governed
> re-issuance record
> `opensoft/openxFactory:openspec/changes/register-gate-rules-council-seats/walk-2026-09-11-register-act.md`,
> `grant-grc-0002` effective `2026-09-11T02:12:30Z`, register projection
> re-derived and observed at `2026-09-11T04:03:38Z–04:03:40Z`.

**IT CITES BOTH HALVES, AND IT NAMES THE MISMATCH — as §13.3 required.** The
hold says it lifts on a record that *"exists on
`opensoft/openxFactory:governance/review-authority/`"*; Brett Heap's ruling of
2026-09-11T02:03:35Z filed the record under `openspec/changes/` instead. The
lift therefore cites **the ACT** — openxFactory PR #941 →
`f0eea7ed1af5a3b7cc247adc8316e04e4b610dc0` on
`governance/review-authority/`, merged 02:29:10Z, with all three writes and the
non-write enumerated — **and THE RECORD ID**, this file's path, `Status: record`,
landed by #941 and extended by #948 → `fa94dfb5`. It states the mismatch in
terms and states that **the original hold postings are not reworded**. It also
carries §13.1's EMPTY window finding under both candidate upper bounds, §14.1's
cluster read with its values, and an explicit *"what this lift does not claim"*
paragraph disowning the admitted-convening route.

The lift releases **this hold and nothing else**. Merge-readiness-council
convenings were never held (§3.4: `grant-mrc-0002` was not revoked, and that
holder's pin `751e03a2…` did not move).

### 14.3 §9.3 — THE PROOF CONVENING: **DISPATCHED ONCE, AND REFUSED**

**RUN [`34561266626`](https://github.com/codeXfactory/codexFactory/actions/runs/34561266626)**
— `workflow_dispatch` on `codeXfactory/codexFactory` `main` (`77537d7d`),
created **2026-09-11T04:11:31Z**, completed 04:11:44Z, **conclusion `failure`**.
Job `claim` failed at its sixth step; job `convene` skipped.

Inputs — the shape of the one admitted precedent (run `34481205558`), never its
values:

```sh
gh workflow run gate-rules-convening-trigger.yml -R codeXfactory/codexFactory --ref main \
  -f rule_packet_ref=hermes/domain/review-councils/convening-packets/2026-09-09-openxfactory-substantive-candidate-class-re-put.md \
  -f subject_pin=585214d97ab85d8efbd3853cb7c39685b487703b \
  -f candidate_pull_number=349
```

The candidate is codexFactory PR **#349** (`OPEN`, not a draft; the preferred
candidate #377 had merged at 02:37:40Z). Its head was re-read twice, the second
time in the same command as the dispatch — both `585214d9…`, and the brief's
pre-found snapshot `a4a32e4d…` was already stale.

**THE REFUSAL, verbatim from the run log:**

```
##[error]claim_refused: the runtime answered HTTP 422 (council.self_review_refused).
the subject of this convening touches council 'gate_rules_council''s own declared machinery
('hermes/domain/agent-mixes.yaml'); a council never clears its own commission (FR-021)
```

**IT IS NOT A REGISTER-SIDE REFUSAL.** Not `review_authority.register_stale`,
not `review_authority.grant_revoked`, not `council.convening_exists`. §13.2
predicted exactly this class of outcome: the admission path never reads the
register projection, so no register-side code can fire on it either way. **This
run therefore neither confirms nor contradicts §14.1**, and it is recorded as
the observation it is rather than as a verdict on the re-issuance.

**THE REFUSAL IS CORRECT IN ITS OWN TERMS, and the cause is exact.** The subject
pin `585214d9…` is a **merge commit** — *"Merge branch 'main' into
refactor/111-decision-core-complexity"*, 2026-09-11T03:54:08Z, parents
`a4a32e4d…` (#349's own tip) and `77537d7d…` (codexFactory `main`). GitHub's
commits API reports **215 files** for that sha — the first-parent diff, i.e.
everything `main` gained since the branch point — and that set **contains
`hermes/domain/agent-mixes.yaml`**, which is precisely the file T1 changed:

```sh
gh api repos/codeXfactory/codexFactory/commits/585214d9… \
  --jq '[.files[].filename | select(test("agent-mixes"))]'   # → ["hermes/domain/agent-mixes.yaml"]
```

#349's **own** three files (`scripts/merge_master/council_clearance.py` and two
test modules) touch no council machinery.
`hermes/domain/review-councils/gate-rules.yaml` declares
`hermes/domain/agent-mixes.yaml#…` as this council's machinery, so
`guard_convening`'s `machinery_intersection` is non-empty and
`SelfReviewRefusedError` fires (hermes-install
`src/hermes_install/domain/touched_objects.py:323`).

**A FINDING THIS SURFACED. RECORDED, NOT ACTED ON.** The touched-object set is
derived over the subject pin's own commit, so for a merge commit it is the
first-parent diff. Because T1 put `hermes/domain/agent-mixes.yaml` onto
codexFactory `main`, **every open codexFactory pull request that merges `main`
from T1 onward derives a touched set containing that file, and
`gate_rules_council` will refuse it `council.self_review_refused`** until that
file falls out of the first-parent diff. FR-021 is reaching further than a
reader of #349's own diff would expect. That is a codexFactory / hermes-install
question, not a register question; nothing was changed for it here, and it is
named so the next reader does not rediscover it as a mystery.

**NOTHING WAS CONSUMED, AND ONE THING WAS PROVED.** The runtime answered **422**,
not 201: no `ConveningStamp` was produced and no convening was persisted, so
#349's pin remains free for a future commissioning. And `admit_convening`'s own
docstring fixes the ordering — the D7 guard *"runs LAST, after … the
once-per-pin discipline has passed and the pin has been verified"* — so the
runtime **had already verified that `585214d9…` is #349's current head** before
refusing. Feature 021's pin verification is observed working, which is the one
positive thing this run establishes.

**NOT RE-DISPATCHED.** One dispatch, one refusal, stop. Choosing a
non-merge-commit pin until a green appeared would be choosing the answer, which
is the forgery this whole ceremony exists to refuse.

### 14.4 The five digests — re-verified against the LANDED composition

§13.5 compared §3.2's ten values against the Part C brief's independently
carried list. **This append makes the check that actually matters and that
neither had made: §3.2's AFTER column against the composition as it now stands
on codexFactory `main`.** Read from
`hermes/domain/agent-mixes.yaml`
(`review_council_profiles.gate_rules_council`, `pinned_on: "2026-09-10"`,
`previously_pinned_on: "2026-09-07"`) and compared programmatically, not by eye:

| | §3.2 AFTER (row C+ / V2S) | landed on codexFactory `main` | match |
|---|---|---|---|
| `rendered_set_digest` | `sha256:aac9b60e…358f21` | `sha256:aac9b60e…358f21` | ✓ |
| `lead-architect` | `sha256:619153c4…8a12d0` | `sha256:619153c4…8a12d0` | ✓ |
| `lead-security` | `sha256:4d90a110…d69cab` | `sha256:4d90a110…d69cab` | ✓ |
| `lead-quality` | `sha256:3a7bb571…f2571e29` | `sha256:3a7bb571…f2571e29` | ✓ |
| `company-policy-lead` | `sha256:7c170ecb…d0e2d0` | `sha256:7c170ecb…d0e2d0` | ✓ |

**All five agree character-for-character** (the table abbreviates for width; the
comparison was over the full 64-hex values, and §3.2 remains the single
unabbreviated copy in this record). **`grant-grc-0002` was therefore issued
against the composition that is actually shipped**, which is the property the
whole re-issuance exists to establish. The merge-readiness holder's own
`rendered_set_digest` still reads `sha256:751e03a2…` — unmoved, confirming §3.4's
two-body check on the landed file rather than on the intention.

### 14.5 What is owed after this append

| Owed | Whose | State |
|---|---|---|
| §8 / `tasks.md` 3.6 | lane `hermes-wallet-exercise` | **DONE** (§14.1); the tick rides the codexFactory close-out pull request |
| §9.4 / the hold | lane `hermes-wallet-exercise` | **DONE** (§14.2) |
| §9.2 / `tasks.md` 3.8 | lane `hermes-wallet-exercise` | finding landed in §13.1 by #948; the tick rides the same close-out pull request |
| §9.3 / a convening that actually exercises review authority | the estate | **STILL OWED** — ratified phase 6 (legs 3 and 4). Run `34561266626` is not it, and §14.3 says why |
| The three ConfigMap row-level fields | whoever next has operator cause | **owed**, §14.1's stated limit |
| The FR-021 merge-commit reach | codexFactory / hermes-install | **recorded, unowned** (§14.3) |
| `design.md` §D4 step 5b's unreachable exit condition | a narrow OpenSpec change | **DISPOSITIONED BELOW**, change queued |

**This record stays `Status: record`.**

---

## Disposition — design § D4 step 5b

**Class: a contested finding against a ratified design, dispositioned rather
than routed around.** Recorded 2026-09-11 by lane `hermes-wallet-exercise`.

**THE FINDING.** codexFactory
`openspec/changes/clarify-gate-rules-decline-position/design.md` § D4 step 5b —
carried forward into `docs/governed-reissuance-runbook.md` and into §9.3 of this
record — makes ***"verify one convening admits"*** the exit condition for the
projection step, on the reading that an admitted `gate_rules_council` convening
is itself proof that the register projection has been re-derived and carries the
new grant. **That exit condition is UNREACHABLE AS BUILT.** §13.2 establishes it
against shipped code and this estate's own landed records: the convening
admission path reads the **domain-content** projection, while the **register**
projection is read only by `DatabaseSeatExerciseGate` inside
`verdict_for_completion`, which this lane never reaches because legs 3 and 4 do
not exist (ratified phase 6, ungated). An admitted convening proves the council
content, the pin and the once-per-pin discipline; it proves nothing about grant
state. Worse, dispatched at the wrong moment it returns a **green admission
against a stale projection**, which the design's own wording would then read as
clearance — the manufactured-clearance failure the governed-re-issuance
discipline exists to refuse.

**THE RULING.** Brett Heap, multi-choice, **2026-09-11T03:01:28Z**:
**disposition entry now, cited change later.** In terms: this finding is
recorded as a disposition here and in the codexFactory packet at the time it was
found, and **a narrow OpenSpec change amending `design.md` § D4 step 5b is
QUEUED for after this ceremony closes.** The design is not edited under cover of
a walk record, and the finding is not left as loose prose either.

**THE SUBSTITUTE, AND ITS STANDING.** For this ceremony, step 5b was satisfied by
the **read-only on-cluster read of §14.1**, performed on the same ruling's
operator word (*"hermes-wallet-exercise reads it"*) by a named lane. It is a
substitute for the design's stated exit condition, **not an instance of it**, and
this record says so rather than reading the two as the same thing. Its own limit
is stated at §14.1 (proof by source revision; three row-level fields not read).

**WHAT THE QUEUED CHANGE SHOULD SETTLE** — recorded as the finder's input, not as
a ruling:

1. **What the real exit condition is**, given that the only path on which the
   register projection is consulted is verdict completion — which is phase 6
   work. A projection read is the honest bar until then.
2. **Whether the runbook's *"a green validator does not lift the hold"* framing
   survives.** It is right about validators; it is wrong that an admitted
   convening is the alternative.
3. **Whether the step names the `hermes.opensoft.one/source-revision` test**
   (§14.1) as the check, and whether it requires the three row-level fields.
4. **Who may perform it** — today it needs a human operator's word for a cluster
   read, which is a governance fact, not a convenience.

**NOTHING IS AMENDED BY THIS SECTION.** `design.md` § D4 reads today exactly as
it was ratified. This is a disposition entry and a queue marker.

---

## 15. Proof convening — result (2026-09-11T09:58:00Z)

**Appended by lane `hermes-wallet-exercise`, on Brett Heap's ruling (multi-choice,
2026-09-11T09:51:53Z): "Re-dispatch once on a clean candidate."** §14.3 recorded run
`34561266626`'s refusal (`council.self_review_refused`, against #349) and the ruling that
followed named the remedy: re-dispatch once, on a candidate the FR-021 assessment
(`brief-part-C-executor.md`, appended section `## FR-021 self-review reach — assessment
(2026-09-11T09:52:51Z)`) actually names as clean. This section records that one re-dispatch.
Nothing above this line is rewritten, per this document's own lifecycle rule
(`docs/document-lifecycle.md`).

### 15.1 Candidate selection and cleanliness

The FR-021 assessment's §(5) named codexFactory **#389** as the recommended candidate
(merge-base `77537d7d` ≥ T1 `02e14c08`; zero `agent-mixes.yaml`/`gate-rules.yaml`
occurrences in its then-current head's commit-API enumeration), with **#363** as fallback.
Both were re-verified fresh at dispatch time, not reused from the assessment's snapshot:

| | Value |
|---|---|
| Chosen candidate | codexFactory PR **#389** (open, non-draft, `mergeable: MERGEABLE`) |
| Head sha (`subject_pin`) at dispatch | `ba83adc8983b34a2a92e872f00da8a44156b3613` — a 2-parent merge commit (parents `6bfeb0439…`, #389's own prior tip per the assessment table, and `9433796e4…`), re-read immediately before dispatch and unchanged |
| Commit-API enumeration | 18 files (`gh api repos/codeXfactory/codexFactory/commits/ba83adc8… --jq '[.files[].filename]'`) — **no** `hermes/domain/agent-mixes.yaml`, **no** `hermes/domain/review-councils/gate-rules.yaml` |
| Fallback considered | codexFactory PR #363 — merged in the same window, at `2026-09-11T09:52:07Z` (head `bdf1b886…`); independently re-verified clean (3 files, no council-machinery names) — **not needed**, #389 passed |

### 15.2 Dispatch and outcome

```sh
gh workflow run gate-rules-convening-trigger.yml -R codeXfactory/codexFactory --ref main \
  -f rule_packet_ref=hermes/domain/review-councils/convening-packets/2026-09-09-openxfactory-substantive-candidate-class-re-put.md \
  -f subject_pin=ba83adc8983b34a2a92e872f00da8a44156b3613 \
  -f candidate_pull_number=389
```

**RUN [`34586762846`](https://github.com/codeXfactory/codexFactory/actions/runs/34586762846)**
— `workflow_dispatch`, created **2026-09-11T09:56:58Z**, **conclusion `success`**.

**VERDICT: ADMITTED.** The `claim` job succeeded through all six steps, including "Verify the
domain-content projection carries this council" and "Claim the convening from the runtime."
The `convene / convene` job succeeded (17s), sealing and publishing the bounded request.

- `subject_pin_source`: `codeXfactory/codexFactory#389`
- `subject_pin_verified_at`: `2026-09-11T09:57:05.742914+00:00`
- Runtime notice, verbatim: *"convening GRC-CONVENE-ba83adc8983b-34586762846 admitted for
  ba83adc8983b34a2a92e872f00da8a44156b3613; the producer is called next."*
- **GRC id: `GRC-CONVENE-ba83adc8983b-34586762846`**
- Materialized `review_council` content carries `gate_rules_council` at overlay revision
  `8931ee2e18948d7e61418a3f84c94180f283eccf`.
- Resolved bench (4 seats): `lead-architect`, `lead-security`, `lead-quality`,
  `company-policy-lead` (`intent_owner_role_slot` excluded as `symbolic_until_project_roster`,
  the same roster rule the earlier run also observed).
- Sealed artifact `sealed-gate-rules-convening-request` published, 9928 bytes, one-day
  retention.

**No refusal of any code** — not `council.self_review_refused` (§14.3's cause on the prior
candidate), not `review_authority.register_stale`, not `review_authority.grant_revoked`, not
`council.convening_exists`. **One dispatch, one admission, stop** — not re-dispatched again,
per the ruling.

Posted in full at codexFactory
[#279 comment 5632761595](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5632761595).

### 15.3 FR-021 self-review reach — assessment summary

Full assessment: `~/session-prompts/stage-361-clarify-gate-rules-decline-position/brief-part-C-executor.md`,
appended section `## FR-021 self-review reach — assessment (2026-09-11T09:52:51Z)`.

**Verdict: a real, narrow defect, filed against `hermes-install`** (owner of the derivation),
not against codexFactory's wrapper —
[`opensoft/xFactory-Hermes-Install#89`](https://github.com/opensoft/xFactory-Hermes-Install/issues/89).
`guard_convening` (hermes-install `src/hermes_install/domain/touched_objects.py:264-326`)
derives the touched-object set via `HttpCommitTouchedObjectResolver.resolve`
(`review_authority/resolvers.py:381-391`), which reads GitHub's **single-commit**
`commits/{sha}` endpoint. For an ordinary commit this is that commit's own changed files; for
a **merge commit**, GitHub reports the diff against the **first parent only** — so when a
candidate's head is itself a "merge `main` in" commit, the derived touched set becomes
"everything `main` gained since the branch point," not "what the candidate itself changed."
Since T1 put `hermes/domain/agent-mixes.yaml` onto codexFactory `main`, any such merge-forward
commit's first-parent diff sweeps that file in, and `gate_rules_council` refuses it
`council.self_review_refused` regardless of the candidate's own substantive diff — #349
(refused at run `34561266626`, §14.3) is the proof: its own three files touch no council
machinery at all. Measured blast radius (2026-09-11T09:52:51Z): **zero** of the 5 then-open
codexFactory PRs actually carried `agent-mixes.yaml` in their commit-API enumeration, and
30/30 `merge-master-approval` runs plus 23/23 `council-convening-lane` runs since T1 were
unaffected — the guard only bites the rare, manual, operator-dispatched gate-rules-council
proof-convening path, never ordinary tier-1/tier-2 PR merging. **Not urgent**; avoidable by
candidate choice, which is exactly what §15.1 did. Proposed fix direction (filed in the
issue): derive the touched set against the merge-base with the base branch instead of a
single-commit read, or exclude a merge commit's second-parent reach from the enumeration.

**This record stays `Status: record`.**
