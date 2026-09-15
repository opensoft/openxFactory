# Walk record — the 2026-09-12 REGISTER ACT (RE-ISSUANCE, SEAT ADDITION) for `gate_rules_council`, against `docs/governed-reissuance-runbook.md`

Status: record
Kind: report
Repository context: openxFactory
Walked: 2026-09-12
Runbook walked: [`docs/governed-reissuance-runbook.md`](../../../docs/governed-reissuance-runbook.md)
  — `Status: draft`, steps **5**, **§5.1**, **step 5b (§5.2)** and **§7**
The act: **the human-ratified REGISTER ACT (RE-ISSUANCE)** — **H2 / T2** of the
  Q-GRC-4 discharge, the openxFactory half of the ONE governed act whose
  codexFactory half (**H1 / T1**) landed at
  `eff9ae191d78c396800a72cdec9fffe0caf866d7`
Governing packet: `register-gate-rules-council-seats` **AMENDMENT 2** —
  [`review/amendment-2026-09-11-q-grc-4-discharge.md`](review/amendment-2026-09-11-q-grc-4-discharge.md),
  oxF PR #971 → `3402d93a`; RATIFIED and encoded at oxF PR #993 → `323c7adf`.
  This act is its tasks **6.9-6.15** (with **6.14** carried in the same commit)
Ratifying human: **Brett Heap** (`Brett.Heap@opensoft.one`)
Effective instant: **`2026-09-13T02:20:48Z`** — ONE instant, taken once from
  `date -u`, written identically into `grant-grc-0002`'s
  `revocation.revoked_at`, into `grant-grc-0003`'s `issued_at`, into the fifth
  wallet key's `custody.declared_at`, and here. **RE-STAMPED AT THE FILL** from
  the composed-day value `2026-09-12T16:33:01Z`, under § 6.3 step 2's rule,
  because the mint landed the day after the act was composed (§ 6.2, § 6.8)
Mint (task 6.8): **DONE** — minted host-side by Brett Heap, secret provisioned
  **`2026-09-13T02:12:15Z`**; this act is FILLED and carries no placeholder (§ 6.8)
Predecessor walk: [`walk-2026-09-11-register-act.md`](walk-2026-09-11-register-act.md)
  — `grant-grc-0002`'s own issuance. **This act supersedes it; it does not
  re-derive it.**
Lane: hermes-wallet-exercise

---

## 0. THE HEADLINE, BEFORE THE DETAIL

**THIS ACT WAS PRE-STAGED, AND IT IS NOW FILLED.** It carried **ONE
PLACEHOLDER** — the public half of a keypair Brett Heap had not yet minted — and
it **COULD NOT MERGE** until that placeholder was filled. **The mint happened**,
host-side, the secret provisioned `2026-09-13T02:12:15Z` (task 6.8), and the
fill was performed against § 6.3's own recipe. **The tree now carries the real
public half in all five slots and the REQUIRED `wallet-validation` gate reads
`0 error(s), 0 warning(s)`, `9 of 9 per-seat signing key(s)` and
`6 declared key(s)`.** § 6.3 is the recipe as it was written; **§ 6.8 is the
fill as it was performed**. What remains is Brett Heap's merge, and the merge
is T2 (§ 7.3).

Everything the mint does NOT determine is written, measured and proved here:
the revocation and its reason class, the successor grant and its scope, the
row repoint, the fifth seat entry's identity fields, the wallet declaration,
the two literal gate counts, and the test that pins them. The mint determines
exactly one fact — **32 bytes** — and that one fact appeared in this tree as
**one placeholder token**. Since the fill it appears as the minted public half,
in the same five slots, derived through the pinned decoder (§ 6.8).

**What is DONE, and is not a formality:**

* **T1 HAS HAPPENED.** codexFactory PR #439 →
  `eff9ae191d78c396800a72cdec9fffe0caf866d7`, merged **2026-09-12T15:59:10Z**.
  `client-security-compliance-officer` is BOUND. **`grant-grc-0002` has been
  VOID since that instant** — by the declared composition change itself, not by
  this file.
* **THE HOLD IS POSTED AND IN FORCE**, one minute fifty-one seconds before that
  merge (§ 3.4).
* **THE ROUTE'S SECOND HALF IS RECORDED** — Lead Quality's acceptance, **ACCEPT
  AS AMENDED**, five conditions (§ 3.5).

**What is NOT done, and none of it is a formality:**

* ~~**THE MINT (amendment task 6.8) HAS NOT HAPPENED** (§ 6.3). It is Brett
  Heap's, host-side, and it is the PRECONDITION of this act.~~ **IT HAS NOW
  HAPPENED** — Brett Heap minted it host-side and the secret was provisioned
  `2026-09-13T02:12:15Z` (§ 6.8). The line is struck rather than deleted, so the
  pre-staged state this record was written in stays legible.
* **THIS ACT IS NOT MERGED.** The merge **is T2** (§ 7.3).
* **STEP 5b IS NOT DONE BY THIS ACT** (§ 8). Until the projection is re-derived
  the runtime keeps refusing with `review_authority.root_key_mismatch` and **NO
  AUTHORITY FLOWS**.
* **THE HOLD IS NOT LIFTED BY THIS FILE'S EXISTENCE** (§ 9).
* **PART C IS ENTIRELY UNWRITTEN** (§ 13). Its five sections are stubbed below
  and each says so on its own face.

---

## 1. WHAT MAKES THIS ACT DIFFERENT FROM ITS TWO PREDECESSORS

This register has now seen three re-issuances and they are three different
events. Saying so matters, because the mechanics look identical on the diff and
are not identical in what they cover.

| | 2026-09-02 (`grant-mrc-0002`) | 2026-09-11 (`grant-grc-0002`) | **2026-09-12 (this act)** |
|---|---|---|---|
| the event | enrolled-roster **model pin flip** (alias → exact) | **prompt-corpus edit** over a fixed four-seat roster | **SEAT ADDITION — the roster grew** |
| components moved | 1 (`model_version`) | 2 (`prompt_contract`) | **1 AND 2, both** |
| seats before → after | 4 → 4 | 4 → 4 | **4 → 5** |
| a new key minted? | no | no | **YES — minted host-side `2026-09-13T02:12:15Z`, § 6.8** |
| `seat_keys` entries touched | none | none | **one ADDED (the ninth)** |
| wallet file edited? | no | no | **YES — a fifth declared key** |
| consuming gate counts moved? | no | no | **YES — two literals, task 6.14** |

**THE CONSEQUENCE THAT MATTERS: this is the first re-issuance that cannot be
composed complete in one sitting.** The other two needed no key that did not
already exist. This one does, and the key's private half is Brett Heap's to
generate host-side under a TTY (**OQ-1 ruled (a)**, 2026-09-11T17:08:42Z). So
this record is filed **ahead of** the fact it depends on, and says so in every
place the fact is missing, rather than waiting and composing under time
pressure after the mint. **THE FACT HAS SINCE ARRIVED** (§ 6.8): the mint landed
`2026-09-13T02:12:15Z` and the five slots carry it. The places that named the
fact as missing are corrected in place and the correction says what it was.

---

## 2. WHAT EACH STEP PRODUCED

| Runbook step | Produced |
|---|---|
| **§5.1 act 1 — REVOKE** | `grants/grant-grc-0002.yaml`: `state: revoked`, `revocation.revoked_at`, reason class **DRIFT** naming **SEAT ADDITION** (§ 5.1) |
| **§5.1 act 2 — MINT** | `grants/grant-grc-0003.yaml`, new root grant, no `parent_grant_ref` (§ 5.2) |
| **§5.1 act 3 — REPOINT** | `register.yaml` `row-grc-0001.grant_ref` → `grant-grc-0003` (§ 5.3) |
| **task 6.12 — REGISTER the key** | `register.yaml` `seat_keys` gains its NINTH entry (§ 5.4) — **FILLED** (§ 6.8) |
| **task 6.13 — DECLARE the key** | `wallets/wal-agent-grc-0001.yaml` `keys` gains its FIFTH entry (§ 5.5) — **FILLED** (§ 6.8) |
| **task 6.14 — move the literals** | `.github/workflows/openxwallet-consumer-gate.yml` `8 of 8` → `9 of 9` and grc `5 declared key` → `6 declared key`, plus the test that pins them (§ 5.6) |
| **§5.1 — the NON-WRITES** | no second row; no custody-attestation edit; no `revocation_staleness_bound` edit; `row-mrc-0001` untouched (§ 5.7) |
| **step 4 — the R8 record** | this file (§ 6) |
| **§0.3 — capacity disclosure** | § 7 |
| **step 5b — the projection** | **NOT PERFORMED** (§ 8) |

---

## 3. T1 — THE COMPOSITION EVENT, FILLED

### 3.1 The act, by its commit

**T1 = `2026-09-12T15:59:10Z`.** codexFactory PR
[#439](https://github.com/codeXfactory/codexFactory/pull/439) → merge commit
**`eff9ae191d78c396800a72cdec9fffe0caf866d7`**, titled *"Q-GRC-4 H1 (T1): bind
the client-security-compliance-officer conjunction seat — the word is given"*.
Twenty-one files; the four that constitute the composition change are
`hermes/domain/review-councils/gate-rules.yaml`,
`hermes/domain/agent-mixes.yaml`,
`.github/workflows/scripts/deliberation_packet.py` and
`.github/workflows/gate-rules-convening.yml`.

**THE ONE KEY THAT IS THE MECHANICAL DISCHARGE** is `seat:` beside `persona:`
under `members.client.conjunction_pull_in` — read by
`scripts/merge_master/seat_resolution.py` as `pull_in.get("seat")`, which is
the only thing that moves `seat_identity` from `UNBOUND` to `declared`. Measured
at the build head against the real C2 subject, the resolver answered
`unbound_conjunction_seats: []`, `seat_identity: "declared"`, `unbound_why:
null`. **That is the concrete state change the whole Q-GRC-4 discharge exists to
produce**, and it has already happened on codexFactory `main`.

### 3.2 What moved in the DECLARED COMPOSITION

**BOTH content components**, which neither predecessor did:

* **component 1, `model_assignments`** — a new entry for the seat: `selector:
  claude-opus-5`, `selector_kind: exact_provider_version`, `pin_status: pinned`
  (`lead-security`'s three values verbatim, under Brett Heap's ruling of
  2026-09-11T14:59:26Z, *"same model pin as lead-security"*),
  `authority_layer: domain`, and an `authority_ref` deliberately **NOT** copied
  from `lead-security` — it names this act's own record, in `lead-architect`'s
  shape, because `authority_ref` records WHO DECIDED, not WHAT WAS DECIDED.
* **component 2, `prompt_contract`** — the seat added to `seats`, a new
  `GATE_RULES_SEAT_FOCUS` briefing written from the TENANT's own specialization
  (`hermes/client/role-overrides.yaml`) because this seat has never sat and no
  convening has ever charged it, and `all_possible_seats` 4 → 5.

Components 3-6 — tool manifest, parameters, policy version, retrieval corpus —
are **untouched**.

### 3.3 The six digests, READ from the landed tree

Read with `git show eff9ae191d78c396800a72cdec9fffe0caf866d7:hermes/domain/agent-mixes.yaml`
at `review_council_profiles.gate_rules_council.prompt_contract`. **Not guessed,
not copied from the H1 pull request's own summary table.**

| | before (`grant-grc-0002`'s composition) | after (this grant's) |
|---|---|---|
| `rendered_set_digest` | `sha256:aac9b60e877d5ab61324ebb5102fe24b685b1bcc1d97aecf9f6c8ef254358f21` | **`sha256:0ea5f7afd8a55f286129206470ab4ad377ac73535644f95fc3811515a44321ad`** |
| `client-security-compliance-officer` | *(absent)* | **`sha256:09d59e06a9fb6d2bca9caa5c27e407f9a28e5a0962682b12d99dbd00409487f2`** |
| `lead-architect` | `sha256:619153c4f31cb1c2f57d00a692d785eed656e354424443507cb01726298a12d0` | **UNMOVED** |
| `lead-security` | `sha256:4d90a110c52095c998744e04cb8e2d24387c01d8d5ddc399ba81f28b2ad69cab` | **UNMOVED** |
| `lead-quality` | `sha256:3a7bb5718adcaa4ad01cb8f2e983125601cd06b5bd5aed4bee855d66f2571e29` | **UNMOVED** |
| `company-policy-lead` | `sha256:7c170ecb2b46e53e041d122c2d92cdbee32ce0da110c38e559e432b088d0e2d0` | **UNMOVED** |
| `pinned_on` / `previously_pinned_on` | `2026-09-10` / `2026-09-07` | `2026-09-12` / `2026-09-10` |

**THE FOUR UNMOVED SEAT DIGESTS ARE THE PROOF THAT NOTHING BUT THE NEW ENTRY
ENTERED THE SET.** The set digest moved anyway and **could not have been
patched**: the basis takes seats in LEXICOGRAPHIC order and
`client-security-compliance-officer` sorts FIRST of the five
(`cli` < `com` < `lea`), so the new prompt entered at the HEAD of the
concatenation and every byte after it shifted.

**The merge-readiness holder's own pin did not move** — `sha256:751e03a2…` at
`eff9ae19`, read rather than assumed (§ 3.6).

### 3.4 The hold — posted BEFORE the merge, as the word required

Brett Heap, **2026-09-12T03:14:35Z**, verbatim: **`merge H1 when green, post the
hold first`**. The hold was posted on codexFactory issue #279 at
**2026-09-12T15:57:19Z** —
[comment `5646989264`](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5646989264)
— **one minute fifty-one seconds ahead of the merge** (precedent: cxF #374's
hold, ~14 minutes ahead of its own).

**WHAT IT HOLDS.** From T1, **no `agent:gate-rules-council` convening may be
dispatched** — not `gate-rules-convening-trigger.yml`, not a hand-assembled
one — until the lift. It does **not** hold merge-readiness convenings.

**WHY A HOLD AND NOT A MECHANICAL PARK**, in the hold's own words: *"No
mechanical park fires for this change: the briefing text and the content pin
move together, so a convening run in the window between this merge and the
openxFactory register act would pass every mechanical check while the holder's
grant stands revoked. **This hold is the only thing between the two.**"*

**WHAT THE HOLD SAYS LIFTS IT** — and it names this act by its parts: the fifth
key registered in the wallet row; REVOKE/MINT/REPOINT; the walk record; then the
3.8 window check, then the 5b read, then the lift. It also names, in terms, the
**precondition still owed by Brett Heap**: the host-side mint. **This record
does not enlarge that list and does not shorten it.**

### 3.5 The route's second half — Lead Quality's acceptance, and LQ2-C1 CARRIED

The route is `guardrails.roster_change: lead_accepted_recorded` and it has two
halves. The **selection** was Brett Heap's (2026-09-11T14:59:26Z). The
**acceptance** is a real seat return, produced by the `lead-quality` seat at its
own pin `claude-sonnet-5`, commissioned by Brett Heap's word of
**2026-09-12T03:05:02Z** (*"commission the lead-quality acceptance return"*) and
recorded at codexFactory
`hermes/domain/review-councils/records/2026-09-12-seat-returns/lead-quality.md`,
commit `7d7ee39a`, with its packet, envelope, prompt and schema committed beside
it.

**POSITION: ACCEPT AS AMENDED.** Six items (D-1..D-4 and D-6
`accept_as_amended`, D-5 `accept`); none declined, none refused. **Five
conditions, all `should_fix`, none blocking, NONE discharged by their own
recording** — they are the convener's. **No condition required a pre-T1 change
to H1**, a verdict reached independently by two readers on the same reasons.

**LQ2-C1 IS CARRIED FORWARD ONTO THIS RECORD, WHICH IS WHAT THE CONDITION
ASKS FOR** — verbatim: *"Any future record citing this pin must carry this bound
forward rather than let the pin imply what it does not."* This record cites the
pin (§ 3.2, § 5.2). **THE BOUND, in the seat's own words:**

> "This pin may be cited only as (a) a lawful, ruled operator selection entered
> through the named route with correctly-uncopied `authority_ref`, and (b)
> internally consistent composition/digest/resolver mechanics. It may NOT be
> cited as (c) a comparative or quality claim about claude-opus-5's fitness for
> this seat's distinct charge, (d) evidence that this seat's behavior has been
> soaked or calibrated at this bench, or (e) evidence that this seat's charge is
> practically, as opposed to textually, distinguishable from lead-security's or
> company-policy-lead's."

**NOTHING IN THIS ACT DEPENDS ON (c), (d) OR (e).** A grant records WHICH
composition authority is issued against; it never claims the composition is
good. The digests in § 3.3 are identity, not quality. Where this record says the
pin is lawful it means (a); where it says the mechanics hold it means (b); it
makes no claim of the other three kinds anywhere.

**THE OTHER FOUR CONDITIONS, and where they sit relative to this act:**

| | what it requires | relative to H2 |
|---|---|---|
| **LQ2-C2** | the 3:2 acceptance recorded **together with the disclosed structural conflict** (lead-quality's own pin is inside the bench it counted), with an independent recorded confirmation that it is the ≥2-distinct-models constraint being certified, not the 2:2/3:2 shape as such | **RULED TO FOLLOW T1** — Brett Heap, 2026-09-12T15:51:38Z, verbatim *"corroborate C2 after T1, proceed"*. It does **not** gate this act. The 3:2 fact itself is recorded at § 5.2 and in `grant-grc-0003`'s expiry section |
| **LQ2-C3** | no practical-distinctness claim until a soak exists | **honoured by silence**: no claim of that kind is made in this act, and § 3.2's "written from the tenant's specialization" is a statement about PROVENANCE, not distinctness |
| **LQ2-C4** | LQ-C4's `tool_manifest` question re-routed naming this seat specifically, **no later than the first convening at which the conjunction fires with this seat bound** | **AFTER this act** — that convening is C2, seven steps downstream (§ 13.5). Named here so the deadline is not discovered late |
| **LQ2-C5** | the reserved-form test admits ACCEPT / ACCEPT AS AMENDED / REFUSE / REQUEST EVIDENCE but not DECLINE | **closed for the CSC test in `7d7ee39a`**; R1's sibling tuple deliberately left alone. Nothing owed here |

### 3.6 The two-body coupling did NOT fire — checked, not assumed

Q-GRC-2 couples the two bodies on an **ENROLLED-ROSTER pin flip**. This event is
not one:

* the pin that moved is `gate_rules_council`'s **own** `model_assignments`;
* the new seat sits on **no other bench** — `merge_readiness_council`'s roster
  is `lead-quality`, `lead-security`, `lead-integration`, `company-policy-lead`,
  and `client-security-compliance-officer` is none of them;
* `merge_readiness_council`'s `rendered_set_digest` is **unchanged** at
  `sha256:751e03a203fd5cef59f0e4873fc910ef6c2c501e60472ea54791ad77fda7c92a`,
  read at `eff9ae19`;
* the new seat's pin `claude-opus-5` adds **no new model identifier** to the
  estate — it is one both bodies already carry.

**`grant-mrc-0002` is NOT revoked by this act and `row-mrc-0001` is not
touched.**

---

## 4. STEP 1 — THE SUPERSEDED STATE, QUOTED AND PROVED CURRENT

Before the writes, on `origin/main` at `5972c8f3055d325e7fb6bd5a701a4b3c6d6ca105`:

* `grant-grc-0002.yaml` — `state: active`, `issued_at: "2026-09-11T02:12:30Z"`,
  `expires_at: "2027-06-30T00:00:00Z"`, `issued_by: Brett.Heap@opensoft.one`,
  no `revocation` block, no `parent_grant_ref`.
* `register.yaml` `row-grc-0001` — nine fields, `grant_ref: grant-grc-0002`,
  `state: active`, `expires_at` character-for-character equal to the grant's.
* `register.yaml` `seat_keys` — **eight** entries, four `merge_readiness_council`
  and four `gate_rules_council`.
* `wal-agent-grc-0001.yaml` — `keys:` carries **four** seat keys plus the
  operator-vaulted root `key-grc-0001` declared at `key_reference`.
* The whole tree passed the pinned validator: **`0 error(s), 0 warning(s)`**,
  `2 row(s)`, `8 of 8 per-seat signing key(s) adjudicated and resolved`, both
  wallets `5 declared key(s)`. **That baseline was measured, not assumed** —
  § 6.5.

---

## 5. STEP 5 — THE ACTS, VERBATIM

### 5.1 REVOKE — `grant-grc-0002`, in place

`state: active` → **`revoked`**; `revocation.revoked_at:
"2026-09-13T02:20:48Z"` (re-stamped at the fill from `2026-09-12T16:33:01Z`, § 6.2);
`revocation.reason` of class **DRIFT**, **575
characters** against the pinned schema's `maxLength: 600` (measured, not
estimated). The free text names **SEAT ADDITION**, as task 6.9 requires — the
2026-09-11 precedent's named the prompt-corpus pin move, and a reason that read
the same for both events would tell a later reader nothing about which happened.

A header block is **APPENDED** above the schema keys and **nothing already in
the file is rewritten**. The sentences that read in the present tense were true
of an ACTIVE grant issued against a FOUR-seat composition and are now read
through the new block — the same append-only discipline `grant-grc-0001` got.

### 5.2 MINT — `grant-grc-0003`

A **ROOT** grant: no `parent_grant_ref`. `issued_at` is byte-identical to the
revocation instant, so **there is no window between the revocation and the
issuance**. `issued_by: Brett.Heap@opensoft.one`. `expires_at:
"2027-06-30T00:00:00Z"` — **ruled afresh at the same value** by **OQ-2 option
(a)** (2026-09-11T17:08:42Z): *"Q-GRC-3's date UNCHANGED, the date
`grant-mrc-0002` still carries, so the two bodies' grants cannot silently
diverge."*

**THE EXPIRY'S BINDING WAS RE-CHECKED AGAINST THIS EVENT AND IT HOLDS.** The
date is bound to the earliest published retirement floor among this council's
pinned model identifiers. **The fifth seat adds no new identifier** — its pin
`claude-opus-5` is already carried by `lead-architect` and `lead-security` — so
the bench's identifier SET is unchanged, `{claude-opus-5, claude-sonnet-5}`
before and after, and the floor has not moved. Checked against the landed
`model_assignments` block, not inferred from the ruling.

**WHAT DID CHANGE IS THE RATIO, AND IT IS NAMED RATHER THAN DISCOVERED.** The
2:2 opus/sonnet split that the 2026-08-22 Q3 disposition sought and the
2026-09-07 R1 act preserved becomes **3:2**. A ratio is not a floor and this
expiry does not move for it. **LQ2-C2 attaches to the acceptance of that 3:2
shape, not to this date**, and is ruled to follow T1 (§ 3.5).

**SCOPE RE-EXAMINED, NOT COPIED.** All four elements stand, each with its reason
recorded on the grant's own face: `acts: [review]` (a new seat is a new VOICE
inside the same act, not a new act); `objects: [opensoft/openxFactory]` (set
equality against the row's `target_repo`; a cross-repository audience has no
resolution path today); `authority_tier: act` (standing on the **untouched**
custody attestation — Q-GRC-1 was never scoped to four seats, so the fifth key's
`holder_readable` custody needs no fresh determination and gets none);
`approval_posture` byte-identical (a wider bench is a reason to keep the
compensating control, not to loosen it).

### 5.3 REPOINT — `row-grc-0001`

`grant_ref` `grant-grc-0002` → **`grant-grc-0003`**, **and nothing else on the
row**. `expires_at` does not move. `state` stays `active` — the row is the
authority's CONTINUING EXISTENCE, not the grant's. **NO ROW WAS ADDED**: D2's
one-body-one-row shape is unchanged and **a seat is not a holder**. The row
still carries exactly **nine** fields, which the reader enforces as exact set
equality (verified: 9).

### 5.4 REGISTER THE KEY — the ninth `seat_keys` entry (task 6.12)

Added after the gate-rules `company-policy-lead` entry, in the seven-field shape
(verified: 7 fields):

| field | value |
|---|---|
| `seat_id` | `client-security-compliance-officer` |
| `council_ref` | `agent:gate-rules-council` |
| `council_id` | `gate_rules_council` |
| `key_id` | `key-grc-seat-client-security-compliance-officer-0001` |
| `public_key` | `cxm-qmZVKXb_B5aucwuNzeOrXbgLPMKqa6D6DX1DUiQ` — the mint's public half, VERBATIM (§ 6.8) |
| `key_fingerprint` | `sha256:85a4f47606f68a65be7c40f4abb392321d8bc6604ed7c27bef7418ac18df3310` — recomputed by the reader from the line above |
| `authorizing_row` | `row-grc-0001` |

The `key_id` follows the established naming scheme exactly — `key-grc-seat-` +
the seat id + `-0001`, the `grc` namespace being what keeps `key_id` and
`key_fingerprint` globally unique across two bodies that share three seat names.
It happens not to collide here (CSC sits on one bench) and the namespace is used
anyway, because the scheme is the scheme.

### 5.5 DECLARE THE KEY — the fifth wallet key (task 6.13)

**BOTH PLACES ARE REQUIRED, and this is the second.** The register recording a
key is not the wallet declaring it: the pinned validator's **rule (r)** refuses a
presenting key no wallet declares, and hermes-install writes the
register-recorded `key_id` into every exercise record's `presenting_key_ref`.
Without this entry the first gate-rules seat return naming this key would be
refused on arrival.

Seven fields, the shape of the four above it: `did`, `key_id`,
`key_fingerprint`, `public_key_multibase`, `signature_algorithm: ed25519`,
`display_label`, `custody` (`model: holder_readable`, `registry_version: 1`,
`declared_at`, `declared_by: Brett.Heap`). **Three of the seven carried the
placeholder** — `did`, `key_fingerprint`, `public_key_multibase` — because all
three are encodings of the SAME 32 bytes. **All three are now filled** from the
one minted public half, each derived through the pinned decoder (§ 6.8):
`did:key:z6MknCZhXWq3KkPXubK4TTcKCSxXLfC3r2GBQ24Qcrwf9fp7`, `sha256:85a4f47606f68a65be7c40f4abb392321d8bc6604ed7c27bef7418ac18df3310`,
`z6MknCZhXWq3KkPXubK4TTcKCSxXLfC3r2GBQ24Qcrwf9fp7`.

**`custody.declared_at` is the REGISTER ACT's effective instant**
(`2026-09-13T02:20:48Z`), not a mint instant this file cannot know. The fill
landed on 2026-09-13, the day after the act was composed, so the instant WAS
re-stamped together with the other two instants of this act — § 6.3 step 2 —
rather than left to drift silently: `2026-09-12T16:33:01Z` → `2026-09-13T02:20:48Z`.
**The mint's own instant, `2026-09-13T02:12:15Z`, is recorded at § 6.8 and in the
codexFactory mint record; it is deliberately not written into this field.**

**NOTE WHAT IS NOT ADDED.** The entry carries no `minted_by` and no `minted_at`.
Those field names appear nowhere in this family; the pinned reader enforces an
EXACT field set on a declared key, so inventing them would fail the required
check for a reason that has nothing to do with the missing key. The mint's
authorship is recorded where the corpus already records it: this walk record
(§ 6.3), the grant header, and the codexFactory mint record Brett publishes.

### 5.6 MOVE THE CONSUMING GATE'S LITERALS (task 6.14) — **in the same commit**

Task 6.14 requires this by name, and gives the reason: *"a wildcard there would
let a register that lost a body pass the positive proof."* Two literals move,
and the test that pins them moves with them:

| where | before | after |
|---|---|---|
| `.github/workflows/openxwallet-consumer-gate.yml` | `8 of 8 per-seat signing key(s) adjudicated and resolved` | **`9 of 9 …`** |
| same file | `wallet 'wal-agent-grc-0001': 5 declared key(s) adjudicated` | **`… 6 declared key(s) …`** |
| `tests/openxwallet_consumer_gate/test_gate_invocation.py` | the two literals above, plus the function name `test_the_eight_per_seat_keys_…` | **`9 of 9`, `6 declared key`, `test_the_nine_per_seat_keys_…`** |

**`wal-agent-mrc-0001` STAYS AT FIVE.** The two bodies' counts now DIFFER — mrc
5, grc 6 — which is exactly why the mint runbook's §4 says *"add one for the new
wallet, do not widen the existing one"*: a single assertion covering either
wallet would go green on a tree that lost one.

**THE TEST IS PART OF "THE SAME ACT" TOO**, by its own docstring's reasoning
when it moved 4 → 8: leaving it behind would redden `pytest-suite` for the whole
window instead of `wallet-validation`. Measured: `18 passed`.

### 5.7 THE NON-WRITES, enumerated so their absence is a decision

* **no second register row** — a seat is not a holder (§ 5.3).
* **`custody-attest-wal-agent-grc-0001.yaml` NOT edited.** It attests custody
  for the WALLET. Q-GRC-1's `holder_readable` determination was made about this
  body's seat keys and was never scoped to four of them, so the fifth needs no
  fresh attestation and gets none. Checked: the file carries no per-key list and
  no `grant_ref`.
* **`revocation_staleness_bound: P7D` NOT edited.** One bound governs the whole
  register (design D7); tightening it is its own governed edit, never a tidy-up
  inside a re-issuance.
* **`row-mrc-0001`, `grant-mrc-0002`, `wal-agent-mrc-0001` NOT touched** (§ 3.6).
* **`key_reference` (the root key `key-grc-0001`) NOT touched.** The root key is
  operator-vaulted and has no register row; a seat key is not a root key.
* **`contracts/openxwallet-pin.yaml` NOT advanced.** This act needs no reader
  capability that `wallet-v1.5` lacks: a fifth seat on a second body is exactly
  the case Q-GRC-5's `(council_id, seat_id)` pair key already admits. Verified —
  `verify-openxwallet-pin.py` re-run green over the amended tree.
* **`task 4.6` NOT ticked** — amendment task 6.27 in terms: it names TWO seats
  and this act discharges one. `intent_owner_role_slot` stays deferred on its own
  unchanged trigger.

---

## 6. STEP 4 — THE R8 FIVE-FIELD RECORD

> **R8 — the five fields are the MINIMUM.** *"A re-issuance act records the
> superseding grant reference, the superseded grant reference, the composition
> hash issued against, the ratifying human, and the effective time … a floor a
> carrying change may extend, and NOT a ceiling."*

| R8 field | Value |
|---|---|
| **superseded grant reference** | **`grant-grc-0002`** — root grant, issued `2026-09-11T02:12:30Z` by `Brett.Heap@opensoft.one`, backing `row-grc-0001`; now `state: revoked`, reason class **DRIFT** |
| **superseding grant reference** | **`grant-grc-0003`** — minted by this act. Root grant, no `parent_grant_ref` |
| **composition hash issued against** | **STILL PENDING R6/R7 — filled with a SUBSTITUTE, EXPLICITLY LABELLED ONE.** See § 6.1 |
| **ratifying human** | **Brett Heap** (`Brett.Heap@opensoft.one`), the anchored responsible operator under the Human Escalation Contract |
| **effective time** | **`2026-09-13T02:20:48Z`** — one instant, taken once, written into four places (§ 6.2); RE-STAMPED at the fill from `2026-09-12T16:33:01Z` under § 6.3 step 2 |

### 6.1 The composition hash — still PENDING, and what stands in for it

**NO CANONICAL DIGEST IS IMPLEMENTABLE YET, AND NONE WAS INVENTED.** R6 (the
provider plane sits INSIDE the digest) and R7 (JCS / RFC 8785,
`sha256:<lowercase-hex>`, recorded with the canonicalization profile name and
version) remain ratification targets. **The substitute this act records, exactly
as the 2026-09-11 walk did**, is the DECLARING COMMIT plus the holder's OWN six
declared digests (§ 3.3), read back from the live file at `eff9ae19`.

**IT IS LABELLED, and the labelling is the point.** These digests do not cover
the provider plane, which is exactly what R6 says the real hash must. A
locally-invented digest recorded in the hash's place would be **worse than an
empty field**: a later reader could not tell the two apart.

### 6.2 The effective instant — one instant, four places

`2026-09-13T02:20:48Z`, taken once from `date -u`, written byte-identically
into:

1. `grant-grc-0002.yaml` `revocation.revoked_at`
2. `grant-grc-0003.yaml` `issued_at`
3. `wal-agent-grc-0001.yaml` `keys[4].custody.declared_at`
4. this record's header

**THE EFFECTIVE INSTANT AND T2 ARE NOT THE SAME INSTANT, and they are not
conflated.** T2 is the **merge** of this pull request — the window boundary
§ 13.1 measures to. The precedent's gap was ~27 minutes (compose
2026-09-11T02:12:30Z, merge 02:29:10Z) and before that ~9.6 hours
(2026-09-02). **THIS ACT'S GAP WAS LARGER**, because it waited on a mint that
had not happened when the act was composed. That is disclosed, not minimized:
**the hold, not the timestamp, is what covers the window**, and § 6.3 step 2
makes re-stamping an explicit, named step of the fill rather than something a
reader has to notice.

**AND THE RE-STAMP HAPPENED, WHICH IS WHY THIS SECTION READS 2026-09-13T02:20:48Z.**
The act was composed pre-staged on 2026-09-12 and took `2026-09-12T16:33:01Z`
then. The mint landed `2026-09-13T02:12:15Z` — **not the same day** — so § 6.3
step 2's rule fired and ONE fresh `date -u` value, `2026-09-13T02:20:48Z`, was
written into all four places above in the fill commit. **The superseded value is
recorded, here and beside each field, and not silently dropped**; a reader
comparing this record with the pre-fill commit `764006df` sees both instants and
the rule that moved them. **The mint instant is a FIFTH fact and is deliberately
NOT one of the four** — it lives at § 6.8 and in the codexFactory mint record,
because a custody declaration records when the act declared the key, not when
the operator generated it.

### 6.3 ⚠ THE ONE PLACEHOLDER, AND THE RECIPE THAT FILLS IT

**THE MINT HAS HAPPENED — `2026-09-13T02:12:15Z` — AND § 6.8 RECORDS IT.** This
section is left standing as it was written, in the tense it was written in,
because it is the recipe the fill was actually held to; read it as the
instruction and § 6.8 as the discharge. Amendment task 6.8, **OQ-1 ruled (a)** at
2026-09-11T17:08:42Z: **Brett Heap mints and holds it**, host-side, as a FRESH
TTY-gated ceremony and never a rerun of stored state — the task 3.2 ceremony
generalized to one seat. Seed generated in-process (`secrets.token_bytes(32)`),
never written to disk, passed to `gh secret set` **on stdin with `--body`
omitted**, private half stored ONLY as
`COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER` in
codexFactory's `worker-credentials` environment. The consuming caller already
binds that exact secret NAME
(`.github/workflows/gate-rules-convening.yml:276` at `eff9ae19`), with its
fail-closed refusal count moved 4 → 5 in the same H1 act. **NO SEED, EVER, IN
ANY FILE.**

**THE PLACEHOLDER TOKEN, exactly as it stood in the tree at `764006df`** — it
is quoted here and no longer appears in any file. **Its parenthetical `(task
3.2)` is a MIS-NUMBERING and is corrected here rather than in the quote: the
amendment task that performed this mint is 6.8**, and `task 3.2` names only the
PRECEDENT ceremony this one generalizes (that is the sense every other `task
3.2` in this packet carries, and those are correct as written):

```
<<PUBLIC KEY — Brett's host-side mint (task 3.2), secret COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER>>
```

**ONE UNKNOWN — 32 BYTES — IN FIVE SLOTS.** The token is byte-identical in all
five, so `grep -c` finds them all and none can be missed. It is a valid YAML
plain scalar and round-trips unchanged through the parser (verified), so every
file in this act still parses while unfilled:

| # | file | slot | what the fill writes |
|---|---|---|---|
| 1 | `governance/review-authority/register.yaml` | `seat_keys[8].public_key` | the RAW value, 43 chars of canonical unpadded base64url |
| 2 | `governance/review-authority/register.yaml` | `seat_keys[8].key_fingerprint` | `sha256:` + sha256(32 raw bytes).hexdigest() |
| 3 | `governance/review-authority/wallets/wal-agent-grc-0001.yaml` | `keys[4].did` | `"did:key:" + <multibase>`, **quoted**, matching the four entries above it |
| 4 | `…/wal-agent-grc-0001.yaml` | `keys[4].key_fingerprint` | **byte-identical to slot 2** |
| 5 | `…/wal-agent-grc-0001.yaml` | `keys[4].public_key_multibase` | `z` + base58btc(`0xed 0x01` ‖ the 32 raw bytes) |

**DERIVE SLOTS 3-5 THROUGH THE PINNED DECODERS AND NEVER A SECOND TOOL** —
`scripts/validate-factory-identity.py --derive`, the route the four existing
entries took. The pinned reader RECOMPUTES the fingerprint from the multibase,
and the register reader recomputes the same value from the base64url half, so a
transcription slip in either place fails the REQUIRED `wallet-validation`
check. That is the safety net; it is not a substitute for deriving correctly.

**THE FILL-AND-MERGE RECIPE:**

1. **Mint** (task 6.8), host-side. Publish the public half, the `did:key:` and
   the fingerprint in a codexFactory mint record mirroring
   `records/2026-09-08-gate-rules-seat-signing-keys-minted.md`.
2. **Re-stamp the effective instant IF the fill is not same-day** — one fresh
   `date -u` value into the three file slots listed at § 6.2 (1-3) and this
   record's header. Same-day, leave them.
3. **Fill the five slots** from the mint record, deriving 3-5 through the pinned
   decoder.
4. **Re-run the gates** (§ 6.5's table): `verify-openxwallet-pin.py`,
   `wallet-yaml-syntax-gate.py .`, `validate-openxwallet.py .` — **this last
   must reach `0 error(s), 0 warning(s)`, `9 of 9 per-seat signing key(s)`, and
   `wal-agent-grc-0001: 6 declared key(s)`** — plus
   `pytest tests/openxwallet_consumer_gate/`, `openspec validate --all
   --strict`, `doc-health.py --single-repo . --fail-on error`.
5. **Mark the pull request ready**, and **Brett Heap merges**. **THE MERGE IS
   T2.**
6. Then, in order: § 13.1 the window check, § 13.2 the 5b read (on his separate
   operator word), § 13.3 the lift, § 13.4 the proof convening, § 13.5 C2.

**WHAT THE PLACEHOLDER REFUSED WHILE IT STOOD, MEASURED** (§ 6.5): six errors,
all of them the placeholder's, none of them anything else. **A pre-staged act
that could merge unfilled would be worse than one that cannot.** All six are
gone on the filled tree and nothing replaced them (§ 6.8).

### 6.4 `issued_by` — carried from the precedent, and flagged

`issued_by: Brett.Heap@opensoft.one`. **Verified, not guessed:** the same
identity `grant-grc-0002`, `grant-grc-0001` and `grant-mrc-0002` carry — the
anchored operator identity under the Human Escalation Contract, for which the
schema widened `issued_by`'s grammar to accept an email address. **Flagged
anyway**, as the precedent flagged it: `issued_by` names who issued this
authority, and a lane composing bytes on a ratifier's word should not be the
last party to have checked it. **Please confirm at merge.**

### 6.5 THE MEASUREMENT — every gate, run locally over the amended tree

| Command | Baseline (`origin/main`, before edits) | This tree (placeholder unfilled) |
|---|---|---|
| `scripts/verify-openxwallet-pin.py` | `OK … openXwallet@f3eb929b (wallet-v1.5), 8 digest(s) recomputed` | **identical** |
| `openXwallet/scripts/wallet-yaml-syntax-gate.py .` | exit 0 | **exit 0** |
| `openXwallet/scripts/validate-openxwallet.py .` | **`0 error(s), 0 warning(s)`**; `2 row(s)`; `8 of 8 per-seat signing key(s)`; both wallets `5 declared key(s)` | **`6 error(s), 0 warning(s)`** — **ALL SIX ARE THE PLACEHOLDER'S** (§ 6.6); `2 row(s)`; `8 of 9 per-seat signing key(s)`; `wal-agent-grc-0001: 6 declared key(s)` |
| `pytest tests/openxwallet_consumer_gate/` | 18 passed | **18 passed** |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | 100 passed / 3 failed | **identical set** (§ 6.7) |
| `scripts/doc-health.py --single-repo . --fail-on error` | 31 critical / 9 error / 23 warning / 16 info | **identical** (§ 6.7) |

**THE `8 of 9` LINE IS THE PROOF THAT THE PLACEHOLDER IS BEING REFUSED AND NOT
PASSED OVER.** The pinned reader EXCLUDES every entry it refused from that
count, so `8 of 9` says precisely: nine entries present, eight adjudicated, one
refused. On the filled tree it reads `9 of 9`, which is what the consuming gate
now asserts literally.

**AND THE `6 declared key(s)` LINE ALREADY READS SIX**, unfilled — the wallet's
declared-set note counts entries, not valid ones. That is why the wallet half's
refusal shows up as three `[schema]` errors and one
`[declared-key-fingerprint-mismatch]` instead: **the count assertion alone would
not have caught an unfilled key, and the schema and fingerprint rules do.**

### 6.6 The six errors, named individually

Every one is the placeholder, and nothing else in this act produces a finding:

| # | code | where |
|---|---|---|
| 1 | `[schema]` | `wal-agent-grc-0001.yaml: keys/4/did` — does not match `^did:[a-z0-9]+:[A-Za-z0-9._:%-]+$` |
| 2 | `[schema]` | `keys/4/key_fingerprint` — does not match `^sha256:[0-9a-f]{64}$` |
| 3 | `[schema]` | `keys/4/public_key_multibase` — does not match `^z[1-9A-HJ-NP-Za-km-z]+$` |
| 4 | `[declared-key-fingerprint-mismatch]` | `keys[4]` — the multibase "does not decode as base58btc carrying the ed25519 multicodec prefix and 32 raw bytes; the fingerprint beside it cannot be checked, and an unverifiable public half is refused rather than passed over" |
| 5 | `[register-seat-key-malformed]` | `register.yaml:seat_keys[8]` — `public_key` is not 43 characters of canonical unpadded base64url |
| 6 | `[register-seat-fingerprint-malformed]` | `register.yaml:seat_keys[8]` — `key_fingerprint` is not `sha256:<64 lowercase hex>` |

**`register-no-active-row` did NOT recur, and that is proved fresh rather than
assumed from the pin label.** The 2026-09-02 act could not pass this gate at all
(the reader demanded a backing active row for a *correctly* revoked grant);
fixed in openXwallet #14 (`b7b0fbb3`, `wallet-v1.4`), and this repository
consumes `wallet-v1.5`. The finding is absent from the measured output above.

### 6.7 The two whole-repo baselines, taken BEFORE the edits

* `openspec validate --all --strict`: **100 passed, 3 failed** —
  `change/disposition-codexfactory-declared-renames`,
  `change/disposition-codexfactory-floor-relocation-retitle`,
  `change/disposition-codexfactory-regular-pr-council-clearance-archive`. All
  three pre-existing on `origin/main`; **`change/register-gate-rules-council-seats`
  passes** both before and after.
* `doc-health.py --single-repo . --fail-on error`: **31 critical, 9 error, 23
  warning, 16 info; 0 new regressions**, and it exits non-zero on `origin/main`
  already. The identical set after the edits is what this act claims — **not**
  that the repository is clean.

### 6.8 THE FILL — the mint, its values, and the gates on the filled tree

**THE MINT HAPPENED, AND IT IS BRETT HEAP'S ACT.** Task 6.8, host-side and
TTY-gated: the seed generated in-process, never written to disk, the private
half passed to `gh secret set` on stdin with `--body` omitted. **No lane, no
agent and no file in this repository ever held the private half. Every value in
this section is a PUBLIC one.**

| Fact | Value |
|---|---|
| secret | `COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER`, `codeXfactory/codexFactory` environment `worker-credentials` |
| `provisioned_at` | **`2026-09-13T02:12:15Z`** — the CONFIRMING `gh secret list` read, not the store attempt |
| `public_key` (base64url) | `cxm-qmZVKXb_B5aucwuNzeOrXbgLPMKqa6D6DX1DUiQ` |
| `key_fingerprint` | `sha256:85a4f47606f68a65be7c40f4abb392321d8bc6604ed7c27bef7418ac18df3310` |
| `did:key` | `did:key:z6MknCZhXWq3KkPXubK4TTcKCSxXLfC3r2GBQ24Qcrwf9fp7` |
| `public_key_multibase` | `z6MknCZhXWq3KkPXubK4TTcKCSxXLfC3r2GBQ24Qcrwf9fp7` |
| derivation | `scripts/validate-factory-identity.py --derive`, at openXwallet `f3eb929b` (`wallet-v1.5`) — the pinned decoder named at § 6.3, and never a second tool |
| mint record | codexFactory PR #452 — `hermes/domain/review-councils/records/2026-09-12-gate-rules-seat-signing-key-minted-csc.md` |

**THE DERIVED FIELDS WERE NOT HAND-TYPED.** The fill took the public half ALONE
and re-derived `did`, `key_fingerprint` and `public_key_multibase` through the
pinned decoder, so a transcription slip in the operator's hand-back sentence
could not enter the tree. The five substituted values were then byte-compared
against the hand-back's own derived triple and matched exactly, and the pinned
reader independently recomputes the fingerprint from BOTH encodings — which is
the safety net § 6.3 promised, exercised.

**FOOTNOTE — A FIRST SEED WAS PROVISIONED AND DELETED, UNUSED.** An earlier run
of the same ceremony provisioned the same secret name at `2026-09-13T00:33:05Z`.
Its PUBLIC half was lost to a swallowed non-TTY stdout, so nothing could be
registered from it. **No file, no register entry, no wallet declaration and no
convening ever carried or consumed it**; the secret was DELETED before use and
the ceremony re-run. The `2026-09-13T02:12:15Z` seed above is the only one this
act registers. The first is recorded because a later reader of the repository's
secret history will see two provisioning events on one name and is owed the
reason for the first.

**THE FOUR BANNERS THAT NAMED THE FACT AS MISSING, CORRECTED IN PLACE.** The
pre-staged act said so "in every place the fact is missing" (§ 1). Four of those
places are standing banners rather than the five slots, and the fill CORRECTS
EACH IN PLACE RATHER THAN REWRITING IT, so the state each was written in stays
legible and a reader of the merged tree is never told the file cannot merge:

| # | where | what it said | the correction |
|---|---|---|---|
| 1 | `register.yaml`, above `seat_keys[8]` | "THE PUBLIC HALF BELOW IS A PLACEHOLDER AND THIS FILE IS NOT MERGEABLE UNTIL IT IS FILLED … HAS NOT HAPPENED YET" | a dated block naming the mint, the decoder, and `0 error(s)` / `9 of 9` |
| 2 | `wal-agent-grc-0001.yaml`, above the four existing keys | "THE FIFTH ENTRY'S KEY MATERIAL IS A PLACEHOLDER … NOT MERGEABLE in this state" | a dated block naming the mint and `6 declared key(s)` |
| 3 | `wal-agent-grc-0001.yaml`, above `keys[4]` | "PLACEHOLDER — NOT MERGEABLE UNTIL FILLED. Amendment task 6.8's mint has not happened" | a dated block naming the mint and the fingerprint agreement across both encodings |
| 4 | `tasks.md`, the 2026-09-12 pre-stage block | "6.8 — THE MINT HAS NOT HAPPENED … cannot merge until it is filled" | the bullet STRUCK, plus a dated 2026-09-13 addendum recording the tick, the re-stamp, and that nothing else moved |

**None of the four is deleted.** Each superseded sentence is still readable
beside its correction, which is the same treatment § 0 and § 7 item 7 give their
own struck lines and the treatment `register.yaml` already gave the sentence its
row comment corrected. **A governance file that merges while asserting it cannot
merge is a defect, not a formality** — that is why these are part of the fill and
not left to Part C.

**THE GATES, ON THE FILLED TREE** (compare § 6.5's unfilled column):

| Command | Filled tree |
|---|---|
| `scripts/verify-openxwallet-pin.py` | OK — `openXwallet@f3eb929b` (`wallet-v1.5`), 8 digest(s) recomputed |
| `openXwallet/scripts/wallet-yaml-syntax-gate.py .` | exit 0 |
| `openXwallet/scripts/validate-openxwallet.py .` | **`0 error(s), 0 warning(s)`**; `2 row(s)`; **`9 of 9 per-seat signing key(s)`**; `wal-agent-grc-0001: 6 declared key(s)` |
| `pytest tests/openxwallet_consumer_gate` | 18 passed |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | the same three pre-existing `disposition-codexfactory-*` failures as `origin/main`, **0 new**; this change passes |

**THE SIX ERRORS OF § 6.6 ARE GONE AND NOTHING REPLACED THEM.** The `9 of 9`
line is the positive proof § 6.5 named in advance: nine entries present, nine
adjudicated, none refused.

**WHAT THE FILL DID NOT DO.** It did not merge — **T2 is Brett Heap's** (§ 7.3).
It did not lift the hold (§ 9), did not perform step 5b (§ 8), and wrote no
Part C section (§ 13 is still entirely unwritten). **Task 6.8 is ticked by the
fill commit and nothing else is**; every other task of this act ticks at T2 or
after it.

**ONE NAMING TENSION, DISCLOSED AND NOT RESOLVED.** Task 6.15 names this record
`walk-<T2-date>-register-act.md`. This file is named for the day it was walked
and pre-staged, 2026-09-12; T2 will fall on 2026-09-13 or later, so the filename
and the T2 date will differ. **The fill does NOT rename it**: four governance
files and `tasks.md` already cite this path inside append-only blocks, and
rewriting those for a cosmetic gain would cost more than the divergence does.
It is recorded here so a later reader does not read the filename as a claim
about T2. The ratifying human may have Part C re-date it.

---

## 7. CAPACITY DISCLOSURE (runbook §0.3)

**Brett Heap holds three capacities in this act and they are disclosed rather
than collapsed** — the runbook's own instruction. **Two further capacities are
machine-held and are disclosed for the same reason.** **THIS ACT'S SPLIT IS NOT
THE PRECEDENT'S**, and the difference is the row that matters most.

| Capacity | The act held in it | Where exercised |
|---|---|---|
| **the OPERATOR** | evidencing exact provider identity and the plane (R5); **and, uniquely here, MINTING THE FIFTH KEYPAIR** | **THE MINT IS OWED AND NOT YET PERFORMED** (§ 6.3). No `model_version` moves in the openxFactory half, so no operator identity evidence is owed; the standing record (`operator-identity-record-2026-09-01.md`) is unmoved |
| **the CONVENER** | accepting the Council's output on record | Lead Quality's ACCEPT AS AMENDED and its five conditions (§ 3.5) — **and their disposition is his, not the seat's, and not this record's** |
| **the RATIFYING HUMAN** | **the register act itself** (R11: REGISTER is the only human-ratified act, and RE-ISSUE always requires one) | this change — the expiry (OQ-2), the reason class, the effective instant, the seat identifier confirmation (6.1b), and **the merge** |
| **the COORDINATOR** — the lane session `hermes-wallet-exercise`, **not** the ratifying human | **COMPOSING the candidate bytes**, pre-staged ahead of the mint. **THE LANE DOES NOT MERGE THIS ONE** | this pull request |
| **the AUTHORING AGENT** — an Opus agent directed by the lane | writing this record, both grant headers, the register and wallet comments, the gate literals | this change directory |

### 7.1 What is Brett Heap's, and what is not

**What is his is the ACT**: the decision to re-issue, the reason class DRIFT,
the effective instant, the expiry ruled at OQ-2, the seat identifier confirmed
at 6.1b, **the mint**, and **the merge**. **What is not his is the typing.**

**THE MERGE IS HIS HERE, AND THAT IS A DEPARTURE FROM THE PRECEDENT WORTH
NAMING.** On 2026-09-11 he ruled that the lane composes AND merges on his word
(#941's § 7.3). This act is pre-staged **before** its own precondition exists,
so there is no merge word to act on and none is assumed: **the lane composes,
Brett Heap merges.** A coordinator that merged this would be merging a file
whose most important field it could not have checked.

### 7.2 "Operator act" names whose act, not whose hands

R11 rules that revocation needs no ratifier because a fail-closed cascade must
not wait on a human. **That is not a claim that anything here performed it.**
NOTHING IN THIS ESTATE WRITES `state: revoked` INTO A GRANT FILE — no daemon,
no reconciler, no hook walks a composition change into
`governance/review-authority/`. This write is an **operator act with a
machine-enforced refusal behind it**, and it must never be read as a cascade
that ran while nobody was looking.

### 7.3 THE MERGE IS T2

There is no word in hand that authorizes merging this. The words that authorize
**composing** it are the amendment's ratification (2026-09-11T17:08:42Z) and the
6.1b confirmation (2026-09-12T03:23:17Z). **The merge is a separate, later word,
and the merge is T2**: at that instant `grant-grc-0003` becomes the active grant
and the T1→T2 window closes.

---

## 8. STEP 5b — THE PROJECTION. NOT DONE BY THIS ACT.

**The register act does not reach the runtime.** Until the
`hermes-register-projection` is re-derived, the runtime keeps refusing with
`review_authority.root_key_mismatch` and **NO AUTHORITY FLOWS** — including for
the four seats that were already registered.

**THE ROUTE IS NOW RATIFIED, NOT MERELY DISPOSITIONED.**
`amend-register-act-5b-projection-proof`, openxFactory PR #960 → `ac688c40`,
ratified on Brett Heap's word *"accept all A on 960"* (2026-09-11T13:09:12Z). It
fixes the design's own wrong exit condition, which the 2026-09-11 act had to
dispose of as a contested finding: **an ADMITTED convening proves nothing about
the register projection**, because the convening-admission path reads the
domain-content projection only, while the register projection is read inside
`verdict_for_completion`, which this council's lane never reaches.

**THE PROOF IS A READ-ONLY CLUSTER READ**, confirming the ConfigMap's
`hermes.opensoft.one/source-revision` annotation is **at or after T2's merge
sha**. **IT REQUIRES BRETT HEAP'S EXPLICIT OPERATOR WORD EACH TIME — IT IS NOT
SELF-SERVE** (precedent: *"Operator word: hermes-wallet-exercise reads it"*,
2026-09-11T03:01:28Z). **Do NOT attempt it via a convening dispatch.**

> **2026-09-14 — STEP 5b IS PERFORMED, see § 13.2: source-revision
> 96895259 is `ahead` of T2. The hold (§ 9) is NOT lifted by this section;
> § 13.3 records the lift.**

---

## 9. THE HOLD, AND WHAT ACTUALLY LIFTS IT

The hold is § 3.4's, posted 2026-09-12T15:57:19Z, **IN FORCE**. Its lift
condition is its own text: this act landed, then the window check, then the 5b
read, then the lift posted citing the record id. **THE RECORD ID IS THIS FILE'S
PATH**:
`openspec/changes/register-gate-rules-council-seats/walk-2026-09-12-register-act.md`.

**A GREEN VALIDATOR DOES NOT LIFT IT. NEITHER DOES THIS FILE'S EXISTENCE.**
Neither, per § 8, does an admitted convening.

> **POINTER ADDED 2026-09-14 — § 13.1 IS NOW CLOSED, AND EMPTY: no
> `gate_rules_council` convening ran between T1 and T2 (full record at § 13.1
> below). §§ 13.2 and 13.3 REMAIN OPEN. THE HOLD IS STILL IN FORCE — a closed
> window check does not lift it.**

---

> **POINTER ADDED 2026-09-14 — THE HOLD IS LIFTED (task 6.21), § 13.3.** Posted 2026-09-14T09:10:05Z on #279 (`5661634651`), mirrored on PR #439 (`5661635340`) and in `LANES.md` (`837c9e9`), after § 13.1 (EMPTY) and § 13.2 (`ahead`). The lift releases the `gate_rules_council` hold only.

## 10. THE WORDS AS SPOKEN

| UTC | Brett Heap, verbatim | What it authorized |
|---|---|---|
| **2026-09-11T14:59:26Z** | `amend register-gate-rules-council-seats, lead-architect route, same model pin as lead-security` | the amendment, the route, and the pin |
| **2026-09-11T17:08:42Z** | `accept all A on 971, merge slice 3 when green` | Amendment 2 RATIFIED; **OQ-1..OQ-5 all at option (a)** — Brett mints the fifth keypair; `expires_at` unchanged; bind now / soak later; ONE T1/T2 pair; a SEPARATE proof convening precedes C2 |
| **2026-09-12T03:05:02Z** | `commission the lead-quality acceptance return` | the route's second half (§ 3.5) |
| **2026-09-12T03:14:35Z** | `merge H1 when green, post the hold first` | T1, and the hold's ordering |
| **2026-09-12T03:23:17Z** | `confirm client-security-compliance-officer, proceed with T1` | **task 6.1b DISPOSED** — the seat identifier confirmed, no veto |
| **2026-09-12T15:51:38Z** | `corroborate C2 after T1, proceed` | LQ2-C2's corroboration sequenced AFTER T1, so it does not gate this act |
| **2026-09-11T14:23:26Z** | `α, park C2 until Q-GRC-4 is discharged` | the standing ruling this whole discharge serves |

**NO WORD IN THIS TABLE AUTHORIZES MERGING THIS PULL REQUEST.** That word does
not exist yet, and this record does not treat any of the above as standing in
for it.

---

## 11. THE HONEST LIMITS, RESTATED IN TERMS (runbook §7)

1. **The composition hash is a substitute** (§ 6.1), labelled.
2. **No supersession FIELD exists** — the relation lives in prose here, in both
   grant headers, and nowhere else (schema is `additionalProperties: false`).
3. **Nothing in this estate reads a retirement date.** The expiry is enforced
   only by the register reader computing against it at read time.
4. **The seat has never sat, and neither has the bench.** No
   `gate_rules_council` convening has ever been admitted. Every entry in this
   act records authority that has never been presented.
5. **The briefing is DERIVED, not soaked.** LQ2-C3 governs: textual
   non-identity is proved, behavioural distinctness is not claimed.
6. **`tool_manifest` is empty for every seat on this bench**, and LQ-C4's open
   question — whether a packet-only seat can meet its charge without running
   anything — is carried onto the new seat unchanged, with LQ2-C4 requiring it
   be re-routed naming this seat specifically by the first convening the
   conjunction fires on.
7. ~~**THE ACT IS INCOMPLETE AS FILED.** One placeholder, five slots, one mint
   outstanding (§ 6.3).~~ **COMPLETED AT THE FILL** — the mint landed
   `2026-09-13T02:12:15Z`, the five slots carry it, and the limit that remains is
   the one above it in this list, not this one (§ 6.8). **What is still
   outstanding is the MERGE, which is Brett Heap's and is T2.**

---

## 12. REVERSIBILITY

**Before merge: fully reversible.** Nothing is written to
`governance/review-authority/` on `main`; closing this pull request undoes all
of it. **The composition change is NOT reversed by that** — T1 has landed, and
`grant-grc-0002` is void whether or not this merges. Closing this pull request
leaves the body parked with no active grant, which is the fail-closed state, not
a clean one.

**After merge: there is no rollback, only a further governed re-issuance.** *"A
revoked grant SHALL NEVER return to the active state. Authority resumes only as
a NEW grant."* Undoing this in spirit means reverting codexFactory #439 **and
then walking this entire act again** to issue `grant-grc-0004` — a full second
ceremony, not a `git revert`.

---

## 13. PART C — **UNWRITTEN. EVERY SECTION BELOW IS A STUB.**

**NOTHING IN THIS SECTION HAS BEEN PERFORMED.** Each is filled by a dated
append, in order, after T2 — the shape the 2026-09-11 walk's §§ 13-15 took.
**Reading a stub as done is the specific error this section is written to
prevent.**

### 13.1 The 3.8-equivalent window check (task 6.19) — **APPENDED BY PART C**

Prove **NO `gate_rules_council` convening ran between T1 and T2**. Method, from
the 2026-09-11 walk § 13.1: `gh run list --workflow
gate-rules-convening-trigger.yml` cross-checked against `records/` commits in
the window, under both candidate upper bounds (the effective instant and the
merge instant) so the answer does not depend on which is called T2.
**Window lower bound is fixed: `2026-09-12T15:59:10Z`.** Upper bound is the
merge of this pull request. **The hold (§ 3.4) is what makes the expected
finding empty; the check is what proves it.**

#### 13.1 — APPENDED 2026-09-14, PART C: THE WINDOW CHECK IS CLOSED, AND THE FINDING IS EMPTY

**No `agent:gate-rules-council` convening ran in the window. Nothing was
consumed under revocation.** A checked absence, recorded as one.

**Window: T1 = codexFactory PR #439 → `eff9ae191d78c396800a72cdec9fffe0caf866d7`,
merged `2026-09-12T15:59:10Z`. T2 = openxFactory PR #1006 →
`765d8c6fcd3fbfdb71540903858e8fca74f04929`, merged `2026-09-13T22:30:20Z`.**

The command, verbatim, run `2026-09-13T22:4xZ` by lane `hermes-wallet-exercise`
(session `661394c0-589c-4d88-b1b6-1e692bfbc2e8`, container `0e7d1a79a07e`),
read-only `gh` calls only:

```sh
gh run list -R codeXfactory/codexFactory --workflow gate-rules-convening-trigger.yml \
  --json databaseId,createdAt,event,conclusion,headSha --limit 100
```

It returns **seven runs in the workflow's entire history**, and **every one of
them predates T1**:

| run | createdAt | conclusion | headSha |
|---|---|---|---|
| `34586762846` | 2026-09-11T09:56:58Z | success | `9433796e` |
| `34561266626` | 2026-09-11T04:11:31Z | failure | `77537d7d` |
| `34481205558` | 2026-09-10T13:12:32Z | success | `f881cea1` |
| `34480882955` | 2026-09-10T13:09:22Z | failure | `f881cea1` |
| `34318204178` | 2026-09-09T06:14:39Z | failure | `6f50112b` |
| `34317084150` | 2026-09-09T05:59:09Z | failure | `6f50112b` |
| `34307939608` | 2026-09-09T03:39:04Z | failure | `c02abc84` |

Filtered to the window, the result is **`[]`**.

**THE TWO CANDIDATE UPPER BOUNDS DISAGREE, AND THE FINDING SURVIVES BOTH.** The
effective instant — `grant-grc-0003.issued_at`, equal to
`grant-grc-0002.revocation.revoked_at` on oxF `main` — is `2026-09-13T02:20:48Z`.
The merge instant is T2's own `2026-09-13T22:30:20Z`. **The two are 20h 09m 32s
apart** (the 2026-09-11 precedent's own two bounds were 17 minutes apart).
Both give the same empty result, so the finding is empty under both, and the
disagreement is recorded rather than resolved, exactly as the precedent
recorded its own gap. **The gap between them is covered by the HOLD, not by
either timestamp.**

**Two independent cross-checks, because one empty list is not a finding:**

* **The records side is NOT `[]`.**
  `gh api "repos/codeXfactory/codexFactory/commits?path=hermes/domain/review-councils/records&since=2026-09-12T15:59:10Z&until=2026-09-13T22:30:20Z&per_page=100"`
  → **9 commits** — walked from `main` as of `22:4xZ`, so it includes PR
  #452's commits, which merged AFTER T2, at `22:32:20Z`. Via PR #441 (merged
  `17:24:27Z`), PR #450 (`18:52:32Z`), PR #446 (`23:43:32Z`), PR #452
  (`22:32:20Z`, post-T2). **9 distinct files**, each header-verified on
  `main`: `2026-09-11-gate-rules-provenance-axis-declaration.md` (RULING
  PACKET, Status: record); `2026-09-12-gate-rules-roster-csc-pin.md` (Status:
  record; *"NO SEAT WAS RUN, AND NO COUNCIL SELECTED THIS PIN"*);
  `2026-09-12-gate-rules-seat-signing-key-minted-csc.md` (mint record);
  `2026-09-12-lq2-c2-corroboration.md` plus 4 evidence files; and
  `2026-09-12-lq2-c4-reroute.md`. **Zero convening records; none produced by a
  `gate_rules_council` convening.** Stated plainly because it is easy to miss:
  the precedent's `[]` reflected a quiet 3-hour window; this window is 30.5 h
  of lane-authored governance records, and the header-verified answer is
  still zero convening records.
* **The trap named in the runbook, avoided and recorded as avoided (NO
  weight).** `gh run list … --workflow gate-rules-convening.yml` → `0`. That
  file is `workflow_call`-only and reports zero runs whether or not one
  occurred; it was not relied on.

**A THIRD CHECK, NOT ASKED FOR BY THE TASK TEXT, AND IT MATTERED.** Every
workflow run in the window, enumerated in 3-hour chunks (the single-range
query returned exactly 1000 — the API's own page cap — so it was chunked, and
no chunk came back capped): **2546 distinct runs** — council-deliberation-worker
726, council-authorization-trigger 364, council-convening-lane 350,
merge-master-approval 335, lane-line 211, sonar 192, validate 192, Copilot
review 143, floor-regeneration 31, publish-project-bench 1,
provenance-reconciliation 1. **`gate-rules-convening-trigger` /
`gate-rules-convening`: NONE.** Files naming `gate_rules_council` on `main` are
now FIVE (the precedent knew one): the trigger (the only dispatcher),
`gate-rules-convening.yml` (`workflow_call`, REFUSES any other `council_id`),
`merge-master-approval.yml` (a comment, line 2957),
`provenance-reconciliation.yml` (comments plus a LAPSE error string, lines
60/282/291 — it convenes nothing), and `scripts/deliberation_packet.py` (a
profile reader). The `council-*` runs above are all `merge_readiness_council` —
`grant-mrc-0002` was never revoked — and are not "consumed under revocation"
candidates.

**Finding: EMPTY.**

```
WINDOW CHECK (task 6.19): [T1 eff9ae19/2026-09-12T15:59:10Z .. T2
765d8c6f/2026-09-13T22:30:20Z] — EMPTY. No `agent:gate-rules-council`
convening ran. Evidence: 7 trigger runs all pre-T1; records-API 9 commits / 0
convening records (header-verified); 2546 in-window runs, 0 gate-rules; both
upper bounds agree.
```

### 13.2 Step 5b — the register-projection read (task 6.20) — **APPENDED BY PART C**

**OPERATOR WORD REQUIRED — NOT SELF-SERVE.** Read-only cluster read of the
`hermes-register-projection` ConfigMap; confirm
`hermes.opensoft.one/source-revision` is **at or after T2's merge sha**. Route
ratified by oxF #960 → `ac688c40` (§ 8). **Not via a convening dispatch.**

#### 13.2 — APPENDED 2026-09-14, PART C: STEP 5b IS PERFORMED — THE PROJECTION CARRIES THIS ACT

This section performs task 6.20 / step 5b per runbook §§ 2.1-2.6, satisfying
the four ratified requirements of `amend-register-act-5b-projection-proof`
(openxFactory PR #960 → `ac688c40`, capability `review-authority-intake`) by
number: requirement 1 (exit on an OBSERVED projection, never an admitted
convening) is what THE TEST below is; requirements 2 and 3 (read-only, on a
named operator's word, recorded with commands and values; taken only after a
refresh that COMPLETED after T2) are what The authority / The wait condition /
How it was executed / What was read establish; requirement 4 (state the limit)
is STATED LIMIT below.

**The authority.** Brett Heap, in session with this lane, verbatim: *"do the
5b read"* (2026-09-13T22:4xZ) — the fresh operator word naming the executing
lane that § 8 and runbook § 0.3 both require (the 2026-09-11 word —
*"Operator word: hermes-wallet-exercise reads it"* — was spent on that act
only and does not carry forward). **For the credential path**, Brett Heap,
verbatim: *"mount it"* (2026-09-14T08:5xZ) — authorizing his host Azure CLI
profile to be mounted **read-write** into an
`mcr.microsoft.com/azure-cli:latest` container run from the lane's bench
container `0e7d1a79a07e` (the bench container has no `az`/`kubectl` of its
own; a read-only mount fails because `az` writes `az.sess` on start). The
subscription was passed per command (`--subscription
sub-opensoft-platform-aks-qa`), so Brett's default subscription was not
changed. `az account show` confirmed subscription
`sub-opensoft-platform-aks-qa`, user `brett.heap@opensoft.one`.

**The wait condition, met rather than assumed.** The register-projection
refresher's schedule is `0 */2 * * *` (hermes-install
`deploy/kubernetes/overlays/aks-qa/register-projection-cronjob.yaml`,
`successfulJobsHistoryLimit: 1`); the first tick after T2 (`765d8c6f`,
2026-09-13T22:30:20Z) is **2026-09-14T00:00:00Z**. The read ran after the
**08:00Z** tick: because the history limit is 1, only the newest Job is ever
observable — `hermes-register-projection-refresher-29822880`, created
**2026-09-14T08:00:00Z**, **`succeeded=1`**. CronJob `lastScheduleTime`
**2026-09-14T08:00:00Z**, `lastSuccessfulTime` **2026-09-14T08:00:08Z**. The
read ran roughly **8.9 hours** after the first eligible tick — not a cluster
or refresher delay, but the wait for the credential decision above; recorded
so the gap reads as accounted for, not overlooked.

**How it was executed.** One `az aks command invoke` against
`aks-opensoft-platform-qa-01` / `rg-opensoft-platform-aks-qa`, namespace
`hermes` throughout: `provisioningState` `Succeeded`, `exitCode` `0`,
`startedAt` `2026-09-14T08:56:45+00:00`, `finishedAt`
`2026-09-14T08:56:47+00:00`. The lane's own shell clock: **START
2026-09-14T08:56:37Z, END 08:56:52Z**. The command was a shell script passed
inline (base64) — **every line a `kubectl get` with `-o jsonpath`** — no
`apply`, `patch`, `create`, `delete`, `edit`, `rollout`, or side-effecting
`exec`:

```sh
NS=hermes
kubectl -n "$NS" get cronjob hermes-register-projection-refresher -o jsonpath='{.status.lastScheduleTime} {.status.lastSuccessfulTime}'
kubectl -n "$NS" get jobs -l app.kubernetes.io/name=hermes-register-projection-refresher --sort-by=.metadata.creationTimestamp -o jsonpath='{range .items[*]}{.metadata.name}{" created="}{.metadata.creationTimestamp}{" succeeded="}{.status.succeeded}{"\n"}{end}'
kubectl -n "$NS" get configmap hermes-register-projection -o jsonpath='{.metadata.annotations}'
kubectl -n "$NS" get configmap hermes-register-projection -o jsonpath='{.metadata.resourceVersion} {.metadata.creationTimestamp}'
kubectl -n "$NS" get cronjob -o jsonpath='{range .items[*]}{.metadata.name}{" lastSuccessful="}{.status.lastSuccessfulTime}{"\n"}{end}'
```

**What was read, verbatim:**

| | Value |
|---|---|
| CronJob `hermes-register-projection-refresher` `lastScheduleTime` | `2026-09-14T08:00:00Z` |
| …`lastSuccessfulTime` | `2026-09-14T08:00:08Z` |
| Newest Job | **`hermes-register-projection-refresher-29822880`**, created `2026-09-14T08:00:00Z`, **`succeeded=1`** |
| ConfigMap `hermes-register-projection` → `hermes.opensoft.one/source-revision` | **`968952596dfa9f3a6ba4e0cc47a71a37c7c65eea`** |
| …`hermes.opensoft.one/projected-at` | `2026-09-14T08:00:02Z` |
| …`hermes.opensoft.one/projection-digest` | `sha256:58dd5e737a6a11a580b31354d05914a87521f67be84694aa46c2116057d87bff` |
| …object `resourceVersion` / `creationTimestamp` | `38705388` / `2026-08-30T15:23:46Z` |

Context only, not part of the proof: `hermes-council-refresher`
`lastSuccessful` `2026-09-14T08:45:04Z`.

**THE TEST, AND IT PASSES.** Runbook § 2.4 names the check:

```sh
gh api repos/opensoft/openxFactory/compare/765d8c6fcd3fbfdb71540903858e8fca74f04929...968952596dfa9f3a6ba4e0cc47a71a37c7c65eea --jq .status
```

→ **`ahead`** (`ahead_by` 31, `behind_by` 0). `96895259` is
`opensoft/openxFactory` `main` at **2026-09-14T05:05:22Z** — the merge of PR
#888 (`Derive-possibles register merge 2026-09-10`) — identical to `main` at
read time, and strictly after T2 (`765d8c6f`, 2026-09-13T22:30:20Z). **The
published projection was derived from a revision of `main` that already
carries this act** (`grant-grc-0003`, the repointed `row-grc-0001`, the
registered fifth seat key). **PASSES** per runbook § 2.4 (accept = `ahead` or
`identical`).

**STATED LIMIT (ratified requirement 4).** This read establishes 5b **BY
SOURCE REVISION ONLY.** Fields actually read: CronJob
`.status.lastScheduleTime`, `.status.lastSuccessfulTime`; Jobs
`.metadata.name`, `.metadata.creationTimestamp`, `.status.succeeded`;
ConfigMap `.metadata.annotations`, `.metadata.resourceVersion`,
`.metadata.creationTimestamp`. It did not read the ConfigMap's `data` at all
— only `metadata`; no `.data` jsonpath was ever run. NOT separately read,
and recorded here as **OWED** to whoever next has operator cause to touch this
ConfigMap:

(i) `row-grc-0001`'s projected `grant_ref` reading `grant-grc-0003` inside the
published projection's own data; (ii) that row's `expires_at` matching
`grant-grc-0003`'s; (iii) `projected_from.staleness_bound` still carrying
`revocation_staleness_bound` **`P7D`** verbatim.

These follow from the source revision only if the refresher is faithful to its
input, which is its whole job but is not a thing this read observed.

**Posted in full at** codexFactory [#279 comment 5661631470](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5661631470) (2026-09-14T09:09:49Z), before the lift; the raw `az aks command invoke` output is attached to openxFactory #1033 (comment 5661515412).

### 13.3 The hold lift (task 6.21) — **APPENDED BY PART C. THE HOLD IS IN FORCE.**

Posted only after § 13.1 and § 13.2 both pass, citing **T2's merge commit** and
**this file's path**, and naming any wording mismatch as the precedent's lift
text did.

#### 13.3 — APPENDED 2026-09-14, PART C: THE HOLD IS **LIFTED**

Posted 2026-09-14T09:10:05Z–2026-09-14T09:10:20Z, in the **same three places** the hold of
2026-09-12T15:57:19Z was posted — § 3.4 of this record names one (issue #279);
the register's own line of 2026-09-12T15:57:40Z names all three (*"HOLD posted
(#279 5646989264, #439 5646989441)"* plus the row itself) — and nowhere else:

| Where | URL / id | UTC |
|---|---|---|
| codexFactory issue **#279** | [`issuecomment-5661634651`](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5661634651) | 2026-09-14T09:10:05Z |
| codexFactory PR **#439** (merged; the hold's second posting, `5646989441`) | [`issuecomment-5661635340`](https://github.com/codeXfactory/codexFactory/pull/439#issuecomment-5661635340) | 2026-09-14T09:10:09Z |
| `LANES.md` (`opensoft/brett-wip` `lanes/LANES.md`, row `codeXfactory-2`) | commit `837c9e9`, pushed to `origin/main` | 2026-09-14T09:10:20Z |

The lift sentence, as posted:

> LIFTED — the HOLD posted at 2026-09-12T15:57:19Z on `agent:gate-rules-council`
> convenings (this issue, comment `5646989264`; mirrored on PR #439 comment
> `5646989441` and in `LANES.md`), by lane `hermes-wallet-exercise` — register
> key `codeXfactory-2` since 2026-09-14T00:30Z (same lane, same window).

**IT CITES BOTH HALVES, AND IT NAMES THE MISMATCHES — as § 9 and task 6.21
require.** T1 (`eff9ae19`, 2026-09-12T15:59:10Z) and T2 (`765d8c6f`,
2026-09-13T22:30:20Z, Brett Heap's word *"merge 1006"*); § 13.1's EMPTY window
under both candidate upper bounds; § 13.2's read with its values and the
`ahead` result; the record id — **this file's path** — with §§ 13.1/13.2 on
openxFactory #1033. Three wording mismatches are named rather than reworded:
**(1)** the hold says *"the 3.8 window check"* — task 3.8 of this change is a
pre-push validator run; the check performed is task 6.19, the 3.8-equivalent,
by the 2026-09-11 walk's § 13.1 method (runbook § 4.2). **(2)** The hold calls
H2 *"Brett Heap's register act … human-only surface"* — the act is his, by his
word *"merge 1006"*, and the hands that merged were this lane's, as § 7.2
defines "operator act". **(3)** The hold says the lift is posted *"on Brett
Heap's word, after that read"* — the word relied on is the read-word itself
(*"do the 5b read"*, 2026-09-13T22:4xZ); `tasks.md` 6.21 is a `[lane]` task
with no separate operator word, and the lift states that reading so a reader
can disagree with it. **The original hold postings are not reworded.**

The lift releases **this hold and nothing else**: merge-readiness-council
convenings were never held (§ 3.4 — `grant-mrc-0002` did not move). It carries
forward, undischarged, Brett Heap's two still-open words of 2026-09-11 —
**13:26:14Z** *"convene C2"* (the live half of *"merge the packet PR when green
then convene C2"*) and **13:27:23Z** *"merge the C2 record PR when green"* —
both owed at `tasks.md` 6.25–6.26, downstream of 6.22 (`deliberation_packet.py
resolved-seats` → `unbound_conjunction_seats` EMPTY), the proof convening
(6.24, Brett Heap dispatches) and C2 (6.25). **What the lift does not claim:**
no convening was dispatched or admitted as proof — § 8's route does not reach
the register projection, and none was tried.

### 13.4 The proof convening (task 6.24) — **APPENDED BY PART C**

**OQ-5 ruled (a)**: it is **SEPARATE and it PRECEDES C2**, on a re-verified
clean candidate. C2 does not double as it — C2 is the convening the conjunction
FIRES on, and one dispatch cannot say which of two proofs failed. **Brett
dispatches**: the workflow's federated credential is `ref:refs/heads/main`-scoped
and reads the factory origin key.

Before it, task 6.22: re-run `deliberation_packet.py resolved-seats` against a
security-surface-touching subject and confirm `unbound_conjunction_seats` is
**EMPTY**. That is the concrete verification the whole act exists for, and it
spends no pin.

#### 13.4 — PRE-NOTE APPENDED 2026-09-14: TASK 6.22 IS PERFORMED (α LIFTED); THE PROOF CONVENING AWAITS BRETT HEAP'S DISPATCH

**Task 6.22 — `resolved-seats` re-run against a security-surface-touching
subject: `unbound_conjunction_seats` is EMPTY.** Run 2026-09-14T09:1xZ (before
09:13:34Z, the candidate-selection run that followed it) by lane
`codeXfactory-2`, in a read-only codexFactory `main` worktree at `3cbb4bd9`,
spending no pin — the concrete verification the whole act exists for, and
step 8 of `records/2026-09-12-gate-rules-roster-csc-pin.md` § 9 (*"THIS is
what lifts α"*, Brett Heap's `α, park C2 until Q-GRC-4 is discharged`,
2026-09-11T14:23:26Z):

```sh
python3 .github/workflows/scripts/deliberation_packet.py rule-facts \
  --packet hermes/domain/review-councils/convening-packets/2026-09-11-routine-code-clearance-repository-respelling.md \
  --out facts.json
# rule_touched_paths: ["scripts/merge_master/codexfactory-routine-code-clearance.yaml"]
python3 .github/workflows/scripts/deliberation_packet.py resolved-seats \
  --council hermes/domain/review-councils/gate-rules.yaml \
  --council-id gate_rules_council --facts facts.json
```

| field | value read |
|---|---|
| `required_seats` | `lead-architect`, `lead-security`, `lead-quality`, `company-policy-lead`, **`client-security-compliance-officer`** |
| `conjunction_evidence[0]` | seat `client-security-compliance-officer`, `predicate: rule_touches_security_posture`, `required: true`, **`seat_identity: "declared"`**, `unbound_why: null` |
| `unbound_conjunction_seats` | **`[]`** |

Where the 2026-09-11 measurement read `seat_identity: "UNBOUND"` and
`unbound_conjunction_seats: ['client-security-compliance-officer']`
(c2-prep § ★), the bound seat now resolves: T1 declared it, T2 registered its
key and grant, and § 13.2 proved the projection carries T2.

**The proof packet, chosen as the 2026-09-11 walk § 15 chose.** Against the
non-security 2026-09-09 packet
(`2026-09-09-openxfactory-substantive-candidate-class-re-put.md`, surfaces
`openspec/changes/**` and `openspec/specs/**`) the same resolver gives the four
registered seats, the conjunction `required: false` with the seat `declared`,
and `unbound_conjunction_seats: []` — so a proof convening on it proves ONE
thing, admission and signing under `grant-grc-0003` with the register act in
the projection, and does not double as C2 (OQ-5 (a)).

**Candidate, re-verified 2026-09-14T09:2xZ and handed to Brett Heap** (cxF #279
comments 5661759632 and 5661766095): codexFactory PR **#471**, head
`4a92ee67c97e896bc906c1dde89ffe0d2ce471d1` — MERGED 2026-09-14T08:56:21Z, so
the head cannot move; a single-parent commit touching exactly one file
(`tests/merge-master/test_clearing_integration_proof_paths.py`, no machinery
path), so the FR-021 guard cannot fire; descends from T1 `eff9ae19`; carries
the 2026-09-09 packet; its pin post-dates every convening run this council has
had (latest 2026-09-11T09:56:58Z), so it is unspent by construction. **Nothing
is dispatched by the lane**: step 9 is Brett Heap's act, and this section is
appended before it so the candidate's basis is on record when he does.

### 13.5 C2 unparks (tasks 6.23, 6.25, 6.26) — **APPENDED BY PART C**

Re-select a clean candidate at that moment (heads and pins will have moved),
dispatch C2 expecting **FIVE** resolved seats and an admitted, sealed convening,
then hand-write the convening record, commit the sealed bundle **before its
1-day artifact retention expires**, and post `C2 DISCHARGED` on cxF #279 —
closing α and all three carried-forward C2 words in one motion.

**LQ2-C4'S DEADLINE IS THIS CONVENING** (§ 3.5): LQ-C4 must be re-routed naming
`client-security-compliance-officer` specifically **no later than** the first
convening at which the conjunction fires with this seat bound. Named here so it
is not discovered afterwards.

#### 13.5 — PRE-NOTE APPENDED 2026-09-15: C2-PREP § 3'S CANDIDATE RULE IS STALE UNDER T1 `eff9ae19`; A POST-T1 C2 CANDIDATE IS PRE-SELECTED; THE PROOF CONVENING STILL AWAITS BRETT HEAP'S DISPATCH

Read 2026-09-15T22:3xZ by lane `codeXfactory-2` (session resumed
2026-09-15T22:34:28Z after Brett Heap's usage reset), in a read-only
codexFactory `main` worktree at `6294a5d7339abd9e27a5acf5e72c4dd888f29694`
(2026-09-14T11:37:45Z, PR #474). Spends no pin. **Nothing is dispatched.**

**Task 6.24 is still Brett Heap's undischarged act.** `gh run list --workflow
gate-rules-convening-trigger.yml` shows 7 runs in the workflow's whole history,
the latest 2026-09-11T09:56:58Z (run `34586762846`); none since. No convening
record has landed under `hermes/domain/review-councils/records/` since the §
13.4 pre-note.

**The proof candidate and machinery re-verified against `6294a5d7`.** `git diff
--stat 3cbb4bd9 6294a5d7` over
`.github/workflows/gate-rules-convening-trigger.yml`,
`.github/workflows/gate-rules-convening.yml`,
`.github/workflows/scripts/deliberation_packet.py`,
`hermes/domain/review-councils/gate-rules.yaml`,
`hermes/domain/agent-mixes.yaml` and the 2026-09-09 packet is **empty** — the
only `records/` change in that range is an addendum § 8.7 to
`2026-09-11-gate-rules-provenance-axis-declaration.md` (another lane's,
unrelated). codexFactory PR **#471** head
`4a92ee67c97e896bc906c1dde89ffe0d2ce471d1` is still MERGED, still descends from
T1 `eff9ae19`, and is still an ancestor of main; a `select-c2-candidate.sh` run
at 2026-09-15T22:38:37Z rates the #471 landing CLEAN*. `resolved-seats` re-read
(the same two commands as § 13.4):

| packet | `required_seats` | conjunction `required` | `seat_identity` | `unbound_conjunction_seats` |
|---|---|---|---|---|
| 2026-09-09 (`2026-09-09-openxfactory-substantive-candidate-class-re-put.md`) | `lead-architect`, `lead-security`, `lead-quality`, `company-policy-lead` | `false` | `"declared"` | `[]` |
| 2026-09-11 C2 packet (`2026-09-11-routine-code-clearance-repository-respelling.md`) | the same four **+ `client-security-compliance-officer`** (five) | `true` | `"declared"` | `[]` |

**Identical to the 2026-09-14 reads in § 13.4.** The dispatch command handed to
Brett Heap at cxF #279 comment `5661759632` stands unchanged.

**THE FINDING (task 6.23's basis moved).** `c2-prep.md` § 3
(`handoffs/xFactory/recovered-host-session-prompts/codexfactory-org-transfer/c2-prep.md`
in brett-wip) recommends *"the C2 packet PR itself"* — cxF #407, head
`772ec85dedac1246193e90eeeccdd3c0eef99b74` (MERGED 2026-09-11T14:01:10Z →
`76f2e771`). That rule was written against the T1 of 2026-09-11 (`02e14c08`).
Under the T1 now in force, `eff9ae19` (cxF #439, 2026-09-12T15:59:10Z), `git
merge-base --is-ancestor eff9ae19 772ec85d` is **FALSE**: #407's head was
branched from `982ff36a`, before #439 landed. **The packet PR's own head is no
longer an admissible C2 candidate; C2 needs a post-T1 landing that carries the
packet in its tree.** tasks.md 6.23 already says heads and pins will have
moved; this names the specific way they moved.

**Pre-selected C2 candidate, to be RE-VERIFIED at 6.23** (after the proof
convening spends `4a92ee67`; recorded on cxF #279 comment `5689096294`): cxF
**#470** head `cd5ee34082a63b59b4037a6732138602996a4f1f` — MERGED
2026-09-14T08:55:47Z (`record/close-dependency-0-3`, merge commit `046e9c51`),
a single-parent commit touching exactly one file (a `tasks.md` under
`openspec/changes/`; neither `hermes/domain/review-councils/gate-rules.yaml`
nor `hermes/domain/agent-mixes.yaml`), descends from T1 `eff9ae19`, carries the
C2 packet in its tree (`git cat-file -e cd5ee340:<packet path>` OK), and its
pin post-dates every convening run this council has had, so it is unspent by
construction — the same shape as the proof candidate. Fallback: #474 head
`049455c054cc…` (single-parent, two test files, same properties). The
2026-09-15 head-shape screen of #474/#473/#470/#469/#468/#466/#467/#448 found
every one T1-descended, packet-carrying and machinery-free; #470 and #474 are
the two single-parent heads.

**LQ2-C4's deadline** (§ 13.5 above) is unaffected: the reroute record
`records/2026-09-12-lq2-c4-reroute.md` names
`client-security-compliance-officer`; nothing further is owed before C2.

**Nothing is ticked by this note.** Task 6.23 ticks at the moment of selection,
after the proof convening — this section is appended so the finding and the
pre-selection are on record before Brett Heap's dispatch, as § 13.4's pre-note
was.

### 13.6 What is owed, and by whom

| Owed | By | Gates what |
|---|---|---|
| ~~**the mint of the fifth keypair**~~ **DONE `2026-09-13T02:12:15Z`** | Brett Heap | **THIS ACT** — it no longer blocks anything (§ 6.8) |
| ~~the fill~~ **DONE** + ~~the merge (T2)~~ **DONE `2026-09-13T22:30:20Z` (oxF #1006 → `765d8c6f`)** | the lane filled; Brett Heap merged | everything below |
| ~~§ 13.1 window check~~ **DONE `2026-09-13T22:4xZ`** | the lane | § 13.3 |
| ~~§ 13.2 5b read~~ **DONE `2026-09-14T08:56:47Z`** | Brett Heap's word, then the lane | § 13.3 |
| ~~§ 13.3 lift~~ **DONE `2026-09-14T09:10:05Z`** | the lane, on his word | § 13.4 |
| § 13.4 proof convening — re-verified 2026-09-15 (§ 13.5 pre-note) | Brett Heap dispatches | § 13.5 |
| § 13.5 C2 candidate re-selection (6.23) — **pre-selected 2026-09-15: cxF #470 head `cd5ee340`, fallback #474 head `049455c0`; c2-prep § 3's #407 head fails T1 `eff9ae19`** | the lane, after § 13.4 | § 13.5's C2 dispatch (6.25) |
| LQ2-C2 corroboration | the lane, ruled to follow T1 | nothing here |
| LQ2-C4 re-route | the lane | § 13.5's convening |
