# Re-issuance record — THE REGISTER ACT, 2026-09-02, on the S5 composition change

    Status: record
    Kind: report
    Repository context: openxFactory
    Act performed: the governed re-issuance runbook's STEP 5 and its §5.1 —
      revoke, mint, repoint, and do not add a row
    Runbook: docs/governed-reissuance-runbook.md (Status: draft)
    Ratifying human: Brett Heap (Brett.Heap@opensoft.one)
    Effective instant: 2026-09-02T09:00:00Z
    Drafted: 2026-09-02, in-session, at the Operator's direction (see §6)

---

## 0. WHERE THIS FILE LIVES, AND WHY HERE

**The location was chosen for want of a ratified one, and that is said here
rather than left to be inferred.** The runbook names a home for a **walk**
record — *"Beside the change that commissioned it, as a dated artifact —
`openspec/changes/<change>/walk-<YYYY-MM-DD>-<subject>.md`"* (§7) — and names
**no** records path under `governance/review-authority/` or `docs/` for the
**step-4 re-issuance record** itself. Its §5.1 tells you the supersession *"is
recorded in the re-issuance record of step 4 and nowhere else"* without saying
where that record sits.

So this file follows §7's in-change-dir convention with a `reissuance-` prefix
instead of `walk-`, beside
[`walk-2026-08-31-composition-bump.md`](walk-2026-08-31-composition-bump.md).
**It is not a walk record.** A walk exercises the runbook's steps 0–5; this
document records the performance of **step 5 alone**, which the walk of
2026-08-31 explicitly left owed (that record's §5.2: *"Nothing was revoked,
nothing was minted, no row was repointed"*).

Giving the re-issuance record a ratified home is a small named residual (§7.6).

---

## 1. THE ACT — three writes and one non-write, in ONE commit

Runbook §5.1, in its own order. **A grant is REPLACED, never revived.**

### 1.1 REVOKED — `grant-mrc-0001`, in place

`governance/review-authority/grants/grant-mrc-0001.yaml`

| Field | Before | After |
|---|---|---|
| `state` | `active` | **`revoked`** |
| `revocation` | *(absent)* | **added** — `revoked_at: "2026-09-02T09:00:00Z"`, `reason:` naming the composition event |

**Nothing else in that file was touched.** `grant_id`, `audience`, `scope`,
`expires_at`, `issued_at` and `issued_by` are byte-identical to the record that
stood before this act, because a revocation is a fact ABOUT a grant and not a
rewrite of it.

**Reason class is DRIFT**, and the class is carried in the reason PROSE. The
pinned schema's `revocation` block is `additionalProperties: false` over exactly
`{revoked_at, reason, propagated_from}` and has **no classed field**; whether
`reason` may carry DRIFT/CAUSE as-is or needs a distinct carrier is openXwallet
`add-composition-drift-cascade` **task 3.2, still OPEN**. DRIFT propagates
exactly as CAUSE — no derived authority survives on the strength of its parent's
reason — and there are no derived grants today, so nothing cascaded.

`propagated_from` is **absent and correctly so**: this grant is the ORIGIN of the
revocation, not a descendant that inherited one.

**There is no `revoked_by` field in the pinned schema**, so the ratifying human
is named in THIS record and not in the grant. The instruction that drafted this
act said "revoked_by the ratifying human **if the shape has such a field**"; it
does not, and inventing one would be refused by `additionalProperties: false`.

### 1.2 MINTED — `grant-mrc-0002`

`governance/review-authority/grants/grant-mrc-0002.yaml` (new file)

| Field | Value | Why |
|---|---|---|
| `grant_id` | `grant-mrc-0002` | a NEW id; the revoked id is never reused |
| `state` | `active` | |
| `issued_at` | `"2026-09-02T09:00:00Z"` | the effective instant, equal to `revoked_at` above — there is no window between them |
| `issued_by` | `Brett.Heap@opensoft.one` | exact; the reader's `ROOT_ISSUER_OPERATOR_TOKEN`, and the only accepted root-issuer value |
| `expires_at` | `"2027-06-30T00:00:00Z"` | **chosen afresh**, see §1.5 |
| `audience.wallet_ref` | `wal-agent-mrc-0001` | carried forward |
| `audience.holder_ref` | `agent:merge-readiness-council` | carried forward |
| `scope.acts` | `[review]` | carried forward |
| `scope.objects` | `[opensoft/openxFactory]` | carried forward — exactly `{target_repo}` |
| `scope.authority_tier` | `act` | carried forward; still standing on the custody attestation, untouched by this act |
| `scope.approval_posture` | approval-before-apply true, agent approval false, no escalation triggers | carried forward |
| `parent_grant_ref` | **ABSENT, deliberately** | see §1.4 |

**No provenance or citation block was added to the grant.** The pinned grant
schema is `additionalProperties: false` and has no such property; the citations
live in §2 of this record. The file carries YAML **comments** pointing here,
which confer nothing and are read by no validator.

### 1.3 REPOINTED — `row-mrc-0001`

`governance/review-authority/register.yaml`, and the diff is **exactly two
fields**:

```diff
-    grant_ref: grant-mrc-0001
-    expires_at: "2026-11-23T12:00:00Z"
+    grant_ref: grant-mrc-0002
+    expires_at: "2027-06-30T00:00:00Z"
```

The row's own **`state` stays `active`** — the row is the authority's continuing
existence, not the grant's. `expires_at` is character-for-character the new
grant's. The exact nine-field set is unchanged and no field was added: there is
no model field on a row and a re-issuance does not smuggle the composition onto
one.

### 1.4 THE NON-WRITE — no row was added, and no parent edge was drawn

**No row was added.** The single-row cap is retained and bounds AUTHORITY ROWS;
a second row for the same holder and target is refused by the reader
(`register-minimal-shape-exceeded`).

**`parent_grant_ref` was NOT set to `grant-mrc-0001`**, and the reason is
substantive rather than stylistic. That field means *derived from*, which is a
different relation from *supersedes*; borrowing it would (a) misdescribe a root
grant as an attenuation, (b) make the new grant descend from a **revoked**
ancestor, which is what `_revoked_ancestor` exists to catch, and (c) fail
`attenuation-widened` outright, because a derived grant's lifetime may only
shorten and this one deliberately lengthens.

### 1.5 THE EXPIRY, and the one judgment inside it

`2027-06-30` is the **review expiry the signed Operator identity record RULED**
(§1 of that record): bound to the earliest **pinned** component's published
retirement floor — `claude-sonnet-5`, *"Not sooner than June 30, 2027"*,
confirmed first-party by the Operator at SEM-1 on 2026-09-01.
`claude-haiku-4-5-20251001`'s earlier **2026-10-15** floor is NOT a pinned
component and does not bind this expiry (§7.4 carries it as a residual instead).

**The time-of-day is a drafting judgment and is disclosed as one.**
`grant-mrc-0001` used noon UTC. This grant uses **`T00:00:00Z`** — midnight at
the START of the floor date — so that authority cannot remain live into an
instant at which the pinned model may already be retired. Both forms satisfy the
ruling "expires_at = 2027-06-30"; if the Operator prefers the noon convention,
that is a two-character edit in two files (`grant-mrc-0002.yaml` and the row)
and the two values must move together, character-for-character.

---

## 2. THE THREE CITATIONS

The register act's citation was fixed at three things by the soak run-2 record
§12.3, and all three are named here.

### 2.1 The activation ruling

**codexFactory `hermes/domain/review-councils/records/2026-09-01-s5-seat-model-soak-run3.md`, §12 / §12.1 ("THE ACTIVATION RULING")** — landed in
codexFactory **PR #155**, merge commit **`fd4319aa`** (2026-08-31T16:33:18Z),
titled *"Record the S5 soak run 3: the LA-C3 completion round — 5 of 6, the C9
inverse clean, DA-3's question routed to #154"*.

### 2.2 The roster-change record

**codexFactory `hermes/domain/review-councils/records/2026-08-31-enrolled-roster-model-pin-flip.md`** —
the Lead's acceptance of the enrolled-roster model pin flip, applied to the
roster as `roster_change: lead_accepted_recorded`, with the Lead-Quality
conflict disclosed on the face of the act (that record's §10, spoken by Brett
Heap in session 2026-08-31).

**This is the COMPOSITION EVENT this act is issued against.** The bump itself is
codexFactory merge commit **`6edecaf13e88fc56f9a7182b93a0d48cc2e40541`** (PR
#146), which moved **exactly one of six** declared components — `model_version`
— measured rather than asserted
([`walk-2026-08-31-composition-bump.md`](walk-2026-08-31-composition-bump.md)
§2.2).

### 2.3 The signed Operator identity record (R5 / Packet 2)

**codexFactory `hermes/domain/review-councils/records/2026-09-01-s5-operator-identity-record.md`** —
record id `s5-operator-identity-2026-09-01`, **SIGNED by the Operator
2026-09-01** in session, all six execution acts (EXE-1…EXE-6) and the semantic
act (SEM-1) EVIDENCED, the plane read back as the **DIRECT ANTHROPIC** plane.

> **PLACEHOLDER — MUST BE FILLED BEFORE MERGE.**
> Landing PR **opensoft/codexFactory#`<N>`** — **merge SHA to be recorded at
> merge: `<SHA>`**.
>
> That record was still a scratchpad artifact when this act was drafted; a
> sibling session is opening its landing PR at the path above. **No number and
> no SHA is invented here.** Either the Operator fills the two tokens before
> merging this pull request, or a follow-up commit on this branch fills them
> before merge. A citation to a record that has not landed is the one thing this
> act may not carry silently.

**What that record does and does not do**, in its own words: it *"evidences the
plane for the register act. It does not itself perform issuance or activation —
the register act does, citing this record."* A later partner-plane read-back
REFUSES issuance and activation and requires a new Operator record.

---

## 3. THE R8 FIVE FIELDS — the minimum, filled

R8 adopts five fields as a **floor a carrying change may extend, and NOT as a
ceiling**. The walk of 2026-08-31 could fill three of five; this act fills all
five and the two that were PENDING are now real.

| R8 field | Value |
|---|---|
| **superseded grant reference** | **`grant-mrc-0001`** — root grant, issued `2026-08-25T12:45:00Z` by `Brett.Heap@opensoft.one`, `expires_at "2026-11-23T12:00:00Z"`, now `state: revoked` with a DRIFT-class `revocation` block |
| **superseding grant reference** | **`grant-mrc-0002`** — *was* `PENDING` in the walk record's §4; this act is what made it exist |
| **composition hash issued against** | **PENDING R6/R7** — no canonical digest is implementable until the change carrying R6 (the plane sits inside the digest) and R7 (JCS / RFC 8785, `sha256:<lowercase-hex>`) is authored and ratified. Recorded instead as the walk record's §2.2 per-component **substitute** at codexFactory `6edecaf1`, explicitly labelled a substitute: the component that moved is `model_version`, `sha256:3ff506b8af0c…` → `sha256:a5c245462beb…`. **A locally-invented digest recorded in the hash's place would be worse than an empty field.** |
| **ratifying human** | **Brett Heap** (`Brett.Heap@opensoft.one`), the anchored responsible operator under the Human Escalation Contract (`docs/roles-and-authority.md:103-140`) |
| **effective time** | **`2026-09-02T09:00:00Z`** — one instant, written into both `revocation.revoked_at` and the new grant's `issued_at`, so no window exists between the revocation and the re-issuance |

**Beyond the minimum** — the three citations of §2; the identity assertion
linking the alias the 2026-08-26 record ruled to the exact identifier now pinned
(`opus → claude-opus-5` 25/25, `sonnet → claude-sonnet-5` 8/8, and 80 of 80
across all three soak runs with no substitution observed); the supersession
recorded **in prose** at §1.1–§1.2 because no grant field carries it; and every
residual at §7.

---

## 4. AUTHORSHIP — how the human-only rule was read, honestly

`register.yaml` declares itself a **PERMANENTLY HUMAN-ONLY SURFACE (ratified
requirement, explicit here by name)**, and the sentence that follows is the whole
of what it forbids:

> *"no council verdict may ever produce an autonomous approval of a change to
> THIS file. When entered into gate rules, it is a never-clearable floor member
> BY NAME … A council whose own commission is recorded here is never eligible to
> clear a candidate that edits it."*

**What that rule forbids: CLEARANCE. What it is silent on: DIFF AUTHORSHIP.**

So this act is recorded for what it is, with no softer word for it:

* **The three writes and this record were DRAFTED IN-SESSION by an agent**, at
  the Operator's direction, on the Operator's rulings of 2026-09-02.
* **Every judgment the act encodes is the Operator's**, ruled in session before
  drafting began: that the act runs now; that step 5b is a tracked follow-on and
  not part of it; that the new expiry is 2027-06-30; and that this authorship
  interpretation be recorded here rather than glossed.
* **The RATIFICATION is the Operator's admin-merge of the pull request carrying
  this commit**, performed by Brett Heap on his own word. Nothing in this
  document is performed until that merge.
* **No council verdict cleared this path, and none could.** The required check
  is expected to show as non-clearable; that is the floor working, not a failure
  to route.
* **Two roles were kept separate and one was not collapsed into the other:** the
  drafter drafts and ratifies nothing; the Operator ratifies and did not draft.
  The runbook's §0.3 warns *"If you find yourself about to perform two of these
  roles in one motion, stop and disclose it on the record instead"* — the
  disclosure is this section.

**A reading that would have been dishonest, and is refused:** that agent
authorship of the diff makes this act non-human, or that human ratification of
an agent-drafted diff makes the surface less than human-only. Neither. The
surface's requirement is about who may CLEAR a change to it; the answer remains
"no council, ever, only the named human."

---

## 5. THE BLOCKER — this act does not currently pass the REQUIRED check

**READ THIS BEFORE MERGING.** The three writes are exactly what the runbook
§5.1 prescribes, and performed exactly as prescribed they leave openxFactory's
**REQUIRED `wallet-validation` check RED**. This was found by running the check,
not reasoned about.

### 5.1 The finding, with the evidence

`python3 openXwallet/scripts/validate-openxwallet.py .` at pin
`wallet-v1.3` (`6b248d4050e1f88b3ca75c1290ad2c81f465300c`), on the tree this
record is committed with:

```
ERROR [register-no-active-row] active REVIEW-class grant 'grant-mrc-0001' has no
backing active register row; admitting a convening for this holder would confer
authority the register never granted

validate-openxwallet: 1 error(s), 0 warning(s)
```

**The cause is a defect in the pinned reader, and the reader's own comment is the
proof.** `check_register`'s headline loop
(`openXwallet/scripts/validate-openxwallet.py:3006-3023`) is introduced by:

> `# The headline obligation, inverted for CI: an active REVIEW-class grant whose holder carries no ACTIVE register row means a convening could admit authority the register never granted.`

and then **omits the state test that comment declares**:

```python
for gid, g in sorted(ctx.grants.items()):
    scope = g.get("scope") if isinstance(g.get("scope"), dict) else {}
    if REVIEW_ACT_TOKEN not in _hashable_set(scope.get("acts")):
        continue
    backed = any(... r.get("grant_ref") == gid and r.get("state") == "active" ...)
    if not backed:
        f.error("register-no-active-row", ...)
```

`ctx.grants` indexes **every** grant in the scanned tree regardless of `state`
(`Context.index`, `:670-675`), so the loop treats a **revoked** grant as an
"active REVIEW-class grant". Combined with the retained **single-row cap**, the
consequence is exact and worth stating in one sentence:

> **The pinned reader can represent exactly ONE review-class grant in
> openxFactory's tree, and that grant must be active and backed. The first
> re-issuance — or the first natural expiry — makes the tree unrepresentable.**

### 5.2 Two counterfactuals, run rather than argued

| Experiment | Result |
|---|---|
| the tree as committed here (`grant-mrc-0001` revoked in place, per runbook §5.1) | **1 error** — `register-no-active-row` |
| the identical tree with `grant-mrc-0001.yaml` **moved out of the scanned tree** | **0 errors, 0 warnings** |
| the identical tree with `grant-mrc-0001` at **`state: expired`** instead of `revoked` | **1 error** — byte-identical `register-no-active-row` |

The third row is the important one: **the defect is not revocation-specific.** It
fires for any retained non-active review-class grant, which means it was going to
fire on **2026-11-23** — `row-mrc-0001`'s own expiry — with no re-issuance and no
act of anybody's at all. Task 7.7 already records that date as a scheduled
runtime event (*"every convening parks under `review_authority.grant_expired`"*);
what it does not record, and what this act discovered, is that the same date
turns a **REQUIRED repository check** red and therefore blocks **every pull
request in openxFactory**, not only convenings.

### 5.3 What was NOT done to make it green, and why

Four routes exist and all four were refused:

1. **Delete `grant-mrc-0001.yaml`.** Green (§5.2 row two) and **refused**: the
   runbook says revoke *"in place. In its own file"*; the ratified core rule
   makes revocation *"a terminal fact about that grant"* and a terminal fact
   needs a durable record; and deleting it removes the edge `_revoked_ancestor`
   walks, which is the mechanism by which revocation propagates to derived
   grants.
2. **Strip its `kind:`** so `repo_scan` skips it, as the custody attestation
   beside it is deliberately kindless. **Refused**: the grant schema's `state`
   enum contains `revoked`, so the family plainly intends revoked grants to stay
   schema'd, and de-classing a record to dodge its own reader is the vacuous-pass
   class this estate keeps closing.
3. **Move it under an `examples/` path**, which `repo_scan` excludes as packaged
   corpus. **Refused**: `wal-agent-mrc-0001.yaml`'s own header warns that a live
   record *"must stay OUTSIDE any examples/ path or the scanner will silently
   stop treating it as live"*. Hiding a live revoked grant in the corpus
   exclusion is a lie told to a gate.
4. **Add a second row backing the revoked grant.** **Refused twice over**: the
   Operator's ruling for this act says DO NOT add a row, and the reader refuses
   it anyway under `register-minimal-shape-exceeded`.

### 5.4 The named successor this act is blocked on

**openXwallet must give `check_register`'s headline loop the state test its own
comment already declares** — skip a grant whose `state` is not `active`, so a
retained revoked or expired predecessor is not read as live authority — and
openxFactory must then bump `contracts/openxwallet-pin.yaml` to the release
carrying it. Verified 2026-09-02: **openXwallet's own `main` (`cd5b1c8`) carries
the same omission**, so no existing release fixes this and the successor is real
work, not a pin bump to something that already exists.

**That is a contract release in another repository and it is NOT folded into this
act**, which is scoped to openxFactory's human-only surface and to one commit of
three writes. The pinned reader is also digest-pinned by
`scripts/verify-openxwallet-pin.py`, so editing it in place here would fail the
pin check before it failed anything else.

**THE RULING THIS NEEDS, and it is the Operator's:**

* **(a)** Hold this pull request until the openXwallet reader fix and the pin bump
  land, then merge all of it green. The composition has been unre-issued since
  2026-08-31 either way, and holding does not make that worse.
* **(b)** Merge this now, accepting that `wallet-validation` is red on `main` for
  every pull request until the fix lands. **This is not recommended** — it
  converts a governance gap into a repository-wide outage.
* **(c)** Rule that a revoked predecessor leaves the scanned tree, quoted
  verbatim into this record instead of retained as a file, and amend the runbook
  §5.1's "in place" accordingly. That is a doctrinal change and belongs in a
  change, not in a merge.

**Nothing here presumes the answer.**

---

## 6. WHAT THIS ACT IS AND IS NOT

* **It does not restore live authority by itself.** The runtime does not read
  `register.yaml`; it reads an operator-established **projection** of it, and
  *"Until the projection is re-derived, the runtime still refuses with
  `review_authority.root_key_mismatch`"*. Step 5b is owed (§7.1).
* **It does not evidence the provider plane.** That is the R5 record of §2.3, a
  different artifact by a different holder. Nothing in this document may be cited
  as plane evidence.
* **It does not exercise an enforced control.** R8 and R9 are ruled **DIRECTION**
  and are not enforced until the change carrying R6–R12 is ratified; the runbook
  is `Status: draft` and *"no gate in this estate today refuses a re-issuance that
  skips it."*
* **It does not claim a fully pinned composition.** `claude-haiku-4-5-20251001`
  executed in 80 of 80 measured judgments, is declared in no composition file,
  and carries the earliest floor in the register (**2026-10-15**). The **runtime**
  is likewise not one of the six declared components.
* **It ticks no task.** Task 7.6 stays OPEN by its own text until R6–R12 is
  ratified. Task 7.7's gate was ruled **MET 2026-09-02** in a separate pull
  request, on its own argument; this act neither performs nor depends on that
  ruling, and the revocation-class evidence 7.7 discusses arrives with step 5b.

---

## 7. RESIDUALS — what this act leaves owed

### 7.1 Step 5b — the projection, and one watched convening

**OWED, tracked, and deliberately not part of this pull request** (the
Operator's ruling of 2026-09-02). It is three things:

1. re-derive the Hermes register projection
   (`hermes_review_authority_register_projection`,
   schema_version 2) from the amended register — nothing invented;
2. carry `revocation_staleness_bound` **verbatim** into
   `projected_from.staleness_bound`; it is **`P7D`** today, loose on purpose
   because nothing refreshes the projection automatically, and **it must not be
   tightened here as a tidy-up**;
3. **verify ONE convening ADMITS**, and record which one. *"The park is not
   lifted by a green validator — it is lifted when a real convening is admitted
   against the new grant."*

**Until 5b is done, this act has made the FILES consistent and has produced no
evidence that the LANE recovered.**

### 7.2 R8/R9 are ruled DIRECTION, not enforced

Restated because paraphrase is where this gets lost: R8's five fields are a
**floor for a carrying change**, not an already-required record format; R9's
in-flight park is a **description of the target**, not a report of a control
exercised here. No convening was in flight at this act and none parked.

### 7.3 The floor names `register.yaml` and NOT its siblings — a pre-existing gap

codexFactory's never-clearable floor
(`scripts/merge_master/openxfactory-review-authority-floor.yaml`, realized by
`protect-review-authority-register`, PR #91 at `da6795b`) names the exact path
`governance/review-authority/register.yaml` for `opensoft/openxFactory`. **It
does not name `governance/review-authority/{grants,wallets,attestations}/`.**

**This act touches two files that the floor does not protect** —
`grants/grant-mrc-0001.yaml` and `grants/grant-mrc-0002.yaml` — and the whole
authority of the row it repoints rests on them. The gap is **pre-existing and
already named** as *"this change's to own"* (`tasks.md` §8, "What P3 did NOT
change here"), and it is **not created by this act**; it is restated here because
a re-issuance is the first act that makes it load-bearing.

### 7.4 The lifecycle watch, under its own caveat

*"Nothing in the estate reads a retirement date, so every one of these is today a
promise rather than a control."*

| Pinned identifier | Horizon | Named owner |
|---|---|---|
| `claude-opus-5` | not sooner than 2027-07-24 | Brett Heap |
| `claude-sonnet-5` | not sooner than 2027-06-30 — **this grant's expiry is bound to it** | Brett Heap |
| `claude-haiku-4-5-20251001` (CLI helper, **undeclared component**) | **2026-10-15** — earliest in the register | Brett Heap |
| runtime / reseed (**not a composition component**) | continuous | Brett Heap |

The helper's disposition — declared in the composition, or refused at read-back —
belongs to the R6–R12 change (2026-08-29 §6.1, P-1), not here.

### 7.5 Stale references left deliberately unedited

The Operator's ruling constrained the `register.yaml` diff to the two repointed
fields and this act touched no wallet. Three **comment** references to
`grant-mrc-0001` are therefore now stale and are named rather than silently left:

| File | Line | What it says |
|---|---|---|
| `governance/review-authority/register.yaml` | ~60 | *"Backed by grant-mrc-0001 (root, issued_by the anchored operator)"* |
| `governance/review-authority/register.yaml` | ~85 | the seat-keys rationale, *"share … `grant-mrc-0001`"* |
| `governance/review-authority/wallets/wal-agent-mrc-0001.yaml` | ~54 | *"grant-mrc-0001 is addressed to the WALLET"* |

All three are prose, none is read by a validator, and each remains true of the
history it describes. A comment-only follow-up should refresh them; doing it in
this commit would have widened a diff the Operator deliberately bounded.

### 7.6 The re-issuance record has no ratified home

§0. Small, and worth fixing in whichever change gives R8 its carrying surface.

### 7.7 A downstream test asserts the OLD expiry

`tasks.md` task 7.7 records that hermes-install **#51** asserts
`row-mrc-0001`'s `2026-11-23T12:00:00Z` boundary in both directions
(`test_the_live_register_rows_expiry_is_a_fact_a_test_asserts`). That branch is
**unmerged**, and this act moves the expiry to `2027-06-30T00:00:00Z`. **The test
literal must move with it before #51 lands**, or #51 lands red against a register
it no longer describes. Named here so it is found rather than discovered.

---

## 8. VALIDATION, verbatim

Run exactly as `.github/workflows/openxwallet-consumer-gate.yml` runs it, at
openXwallet pin `6b248d4050e1f88b3ca75c1290ad2c81f465300c` (`wallet-v1.3`).

```
$ python3 scripts/verify-openxwallet-pin.py
OK openxwallet-pin verified: openXwallet@6b248d4050e1f88b3ca75c1290ad2c81f465300c
(tag label wallet-v1.3), gitlink read from HEAD, 8 digest(s) recomputed

$ python3 openXwallet/scripts/wallet-yaml-syntax-gate.py .
(exit 0)

$ python3 openXwallet/scripts/validate-openxwallet.py .
note  intake register read: governance/review-authority/register.yaml (1 row(s))
note  intake register: 4 of 4 per-seat signing key(s) adjudicated and resolved
note  wallet 'wal-agent-mrc-0001': 5 declared key(s) adjudicated (key-mrc-0001,
      key-seat-company-policy-lead-0001, key-seat-lead-integration-0001,
      key-seat-lead-quality-0001, key-seat-lead-security-0001)
note  repo scan: 3 openxWallet artifact(s) validated, 1841 document(s) skipped
      as another kind
ERROR [register-no-active-row] active REVIEW-class grant 'grant-mrc-0001' has no
backing active register row; admitting a convening for this holder would confer
authority the register never granted

validate-openxwallet: 1 error(s), 0 warning(s)
```

**The one error is §5's blocker and nothing else.** Every cross-field rule the
three writes had to satisfy passed: the row resolves to an active grant whose
`audience`, `acts`, `objects == {target_repo}`, `authority_tier` and
`expires_at` all match it (`register-grant-mismatch` silent); the root issuer is
the anchored operator (`root-issuer-unanchored` silent); tier `act` still stands
on its attestation (`register-tier-act-unattested` silent); the revocation block
is recorded (`revocation-unrecorded` silent); the register's top level and the
row's nine-field set are unchanged (`register-top-level-unknown`,
`register-row-malformed` silent); and the four per-seat keys still resolve to an
active, unexpired `row-mrc-0001`.
