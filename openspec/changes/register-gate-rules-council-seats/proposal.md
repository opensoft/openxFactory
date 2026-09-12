---
code_surface: openxFactory — NOT `none`, and the distinction is load-bearing. This proposal's OWN diff is spec text, one runbook and bookkeeping; but its realization moves four openxFactory surfaces and the change MUST NOT archive until they are merged and green: (1) `governance/review-authority/register.yaml` — a SECOND authority row plus FOUR per-seat key entries, written by Brett's operator act on a permanently human-only surface; (2) `governance/review-authority/{wallets,grants,attestations}/` — `wal-agent-grc-0001.yaml`, `grant-grc-0001.yaml`, `custody-attest-wal-agent-grc-0001.yaml`, likewise operator-written; (3) `contracts/openxwallet-pin.yaml` — `commit:` and `contract_bundle_tag:` advance to the openXwallet release that can represent a second council (NO digest row moves: `scripts/validate-openxwallet.py` is pinned by commit only, `pinned_by_commit_only:`); (4) `.github/workflows/openxwallet-consumer-gate.yml` — the REQUIRED check's LITERAL positive assertions (`4 of 4 per-seat signing key(s)`, and a new one for the second wallet's declared keys) move in the same act, because a wildcard there would let a register that lost a body pass the positive proof. NO reader code is written here: the reader lives in `opensoft/openXwallet` and its widening is that repository's own OpenSpec change, named in tasks §2 as a hard prerequisite.
target_release: implemented — no contract bundle is cut by openxFactory. Nothing under `contracts/openxwallet/` or `contracts/schemas/` is authored or edited here; the pin advance CONSUMES an openXwallet bundle (`wallet-v1.5` or later) rather than publishing one, and no `contracts/manifest.yaml` row or `contracts/CHANGELOG.md` line is owed on this side.
sequenced_after: [add-wallet-carried-review-authority, openXwallet:widen-register-reader-for-a-second-council]
---

# Proposal: register-gate-rules-council-seats

Status: ratified
Proposed: 2026-09-06, on Brett Heap's queuing ruling of 2026-09-05 (below).
Ratified: 2026-09-06 by Brett Heap (repository owner) — in-session at
2026-09-06T14:13:46Z, verbatim *"lets take them in your recommended order all
approved"*, ratified head `169f84ef`; record at
`openspec/changes/register-gate-rules-council-seats/review/ratification-2026-09-06.md`.
Lane: hermes-wallet-exercise
Family: S5 of `add-wallet-carried-review-authority` — the register-act family,
  following `add-per-seat-register-entries` (openXwallet, wallet-v1.2) and the
  2026-09-02 register act (PR #583).
Amended: 2026-09-07 — R1/R2 (`lead-architect`'s pin; 5.9a before row 3.1), by
  Brett Heap in session, verbatim *"R1 lead-architect claude-opus-5, R2 (a) —
  re-sequence 5.9a first"*
  (<https://github.com/opensoft/openxFactory/pull/717#issuecomment-5570774593>);
  carried in § AMENDMENT — 2026-09-07 below and `design.md`
  § AMENDED 2026-09-07.
Amended: 2026-09-11 — **Q-GRC-4 DISCHARGED** for
  `client-security-compliance-officer`, by Brett Heap in session, window
  `codeXfactory-2`, 2026-09-11T14:59:26Z, verbatim *"amend
  register-gate-rules-council-seats, lead-architect route, same model pin as
  lead-security"*; record:
  `review/amendment-2026-09-11-q-grc-4-discharge.md`. Q-GRC-4 is NOT reopened —
  it ruled *"register neither deferred seat NOW"* and named the trigger; this is
  the trigger arriving for ONE of the two seats, and `intent_owner_role_slot`
  stays deferred unchanged. **That amendment's own five open questions OQ-1..
  OQ-5 were RULED 2026-09-11T17:08:42Z** by Brett Heap in session, window
  `codeXfactory-2`, no comment URL, verbatim *"accept all A on 971, merge slice
  3 when green"* — its FIRST clause is this ruling, and it takes each of the
  five at option **(a)**, its RECOMMENDED one, so the ruling moved no byte of
  the delta (§ Rulings in § AMENDMENT — 2026-09-11 below; `design.md` D8-D12;
  record § 9 and its `Ratification:` header line; `tasks.md` § 6.1 / § 6.1a;
  record `review/ratification-2026-09-11-amendment-2.md`).

## AMENDMENT — 2026-09-07 (R1/R2: lead-architect pin; 5.9a before 3.1)

Row 3.1 (design D3's PREREQUISITE) was found BLOCKED on execution — measured
on codexFactory main `8f4920ce`, reported on openxFactory PR #717 as a
BLOCKED status comment, 2026-09-07T02:09:57Z
(<https://github.com/opensoft/openxFactory/pull/717#issuecomment-5564009224>).
Two rulings resolve it — Brett Heap (repository owner, operator), in-session,
2026-09-07T12:40:19Z, verbatim: **"R1 lead-architect claude-opus-5, R2 (a) —
re-sequence 5.9a first"**
(<https://github.com/opensoft/openxFactory/pull/717#issuecomment-5570774593>).

**R1 RULED — `lead-architect` is pinned to the exact model identifier
`claude-opus-5`.** Per codexFactory `agent-mixes.yaml#guardrails.roster_change:
lead_accepted_recorded`, the pin enters the roster through a RECORDED
roster-change act: Brett Heap's selection (this ruling) plus Lead Quality's
acceptance, produced by the lead-quality seat AT ITS OWN PIN
(`claude-sonnet-5`) as a seat return, plus an evidence record. No family pin;
Q8(d) stands, unreopened.

**R2 RULED — (a): mirror merge-readiness's six declared components verbatim**
(`model_version`, `prompt_contract`, `tool_manifest`, `policy_version`,
`parameters`, `retrieval_corpus`), **and § Sequencing below is RE-ORDERED**
so that codexFactory task 5.9a — the caller that convenes
`gate_rules_council` with seat briefings and returns signed seat returns —
precedes row 3.1 (the composition map). Declared against a caller that
exists, `prompt_contract`, `tool_manifest`, `parameters` and
`retrieval_corpus.seat_prompts_ref` become execution-matched, as the
precedent (`016e9f43`) requires, rather than asserted against a caller that
does not exist yet.

**The defect this amendment fixes:** the original § Sequencing below put step
3 (composition, row 3.1) ahead of step 6 (the 5.9a caller) even though step
3's own components resolve only once a caller exists to match them against —
proven by execution: the only renderer (`deliberation_packet.py#seat_system_prompt`)
hard-codes `merge_readiness_council` and refuses `lead-architect` as an
unknown seat, and `lead-architect` itself had no enrolled pin anywhere (fixed
by R1, above). The original § Sequencing text is left standing below,
unedited; this section supersedes it for EXECUTION ORDER.

**§ Sequencing, restated in the corrected order:**

1. **openXwallet** — the reader widening. **DONE**: opensoft/openXwallet
   #16, #17, #18 (merged `f3eb929b`), tag `wallet-v1.5`.
2. **openxFactory** — pin advance + gate-literal move. **DONE**:
   opensoft/openxFactory #740 (merged `30eccf0c`).
3′. **codexFactory** — task 5.9a: the `gate_rules_council` caller with seat
   briefings, together with R1's roster act (`lead-architect` pinned to
   `claude-opus-5` via the recorded roster-change).
3. **codexFactory** — the composition source map and agent-mix profile (row
   3.1), now declared against a caller that exists rather than asserted.
4. **Brett's walk** — mint, attest, grant, row (tasks § 3.2–3.9), with task
   2.8's deferred consumer-gate literal flip performed in the SAME act (per
   tasks § 2.8's 2026-09-07 disposition).
5. **hermes-install / operator** — the projection refresh.
6. **codexFactory** — the first signed `gate_rules_council` convening: 3′'s
   caller's first run.

Steps 1 and 2 are complete. Step 3′ (codexFactory task 5.9a + the R1 roster
act) is now sequenced ahead of step 3 (row 3.1) — **row 3.1 realizes AFTER
5.9a.**

## AMENDMENT — 2026-09-11 (Q-GRC-4 discharged for the CSC conjunction seat)

**Q-GRC-4 (§ below) deferred two seats and named the act that would register
each. That act has arrived for one of them.** codexFactory's C2 convening —
the routine-code-clearance repository respelling, packet on cxF main at PR
[#407](https://github.com/codeXfactory/codexFactory/pull/407) → `76f2e771` —
touches `scripts/merge_master/**`, so `rule_touches_security_posture` HOLDS and
`members.client.conjunction_pull_in` seats `client-security-compliance-officer`
as a second client voice. The council document declares no `seat:` for it, so
`scripts/merge_master/seat_resolution.py` returns `seat_identity: UNBOUND` and
the convening REFUSES with `conjunction_seat_unbound`. Brett Heap parked C2
rather than spending its subject pin on a dispatch that could not seal:
**`α, park C2 until Q-GRC-4 is discharged`** — 2026-09-11T14:23:26Z, cxF #279
comment
[`5635898767`](https://github.com/codeXfactory/codexFactory/issues/279#issuecomment-5635898767).

**Three rulings — Brett Heap, in session, window `codeXfactory-2`,
2026-09-11T14:59:26Z, verbatim:**

> **`amend register-gate-rules-council-seats, lead-architect route, same model pin as lead-security`**

1. **VEHICLE — amend this packet.** It is still ACTIVE, its own task 4.6 names
   this exact act as owed to it, and its directory is the holder's established
   walk-record home (task 3.9). A sibling `amend-*` change was checked and is
   unavailable anyway: every archived `amend-*` precedent amends a PROMOTED
   capability, and `review-authority-intake` is not promoted.
2. **ROUTE — the lead-architect route**, i.e. codexFactory
   `agent-mixes.yaml#guardrails.roster_change: lead_accepted_recorded` — Brett's
   selection PLUS Lead Quality's acceptance at its own pin PLUS an evidence
   record — and NOT a tenant `seat_representation` declaration in
   `hermes/client/role-overrides.yaml`. **This does not move the persona out of
   the client layer**; it chooses which authority route writes the model pin.
3. **PIN — `claude-opus-5`, exactly `lead-security`'s.** Q8(d) stands: an exact
   provider version, never a family. **The `authority_ref` field is NOT copied**
   — `lead-security`'s points at the enrolled merge-readiness roster because
   that seat's pin was never re-selected for this body; CSC's was, so its
   reference names its own record, in `lead-architect`'s shape. And the 2:2
   opus/sonnet split the 2026-08-22 Q3 disposition sought and R1 preserved
   becomes **3:2** — any fifth seat ends it either way, and this records which
   way.

**THE ACT, IN TWO HALVES, SPECIFIED IN `tasks.md` § 6 AND
`review/amendment-2026-09-11-q-grc-4-discharge.md`:**

- **H1, codexFactory** (built via Speckit AFTER ratification; **not authored by
  the amendment pull request**): `gate-rules.yaml` gains
  `seat: client-security-compliance-officer` under the conjunction and the
  persona's `deferred_seats` entry becomes a discharged one; `agent-mixes.yaml`
  gains the seat in `all_possible_seats`, a `model_assignments` entry carrying
  `lead-security`'s pin fields with its OWN `authority_ref`, and a
  `prompt_contract.seats` entry whose briefing must be WRITTEN (no convening has
  ever charged this persona, so the existing four's method — *"written from the
  records"* — is unavailable and the tenant's specialization text is the only
  raw material); the `rendered_set_digest` and a fifth `seat_digests` entry are
  re-pinned against the LIVE RENDER; and a `roster_change:
  lead_accepted_recorded` record in R1's shape carries the ruling, the owed Lead
  Quality acceptance and C13's soak re-open.
- **H2, openxFactory** (Brett's OPERATOR act on a permanently human-only
  surface): mint the fifth Ed25519 keypair (`holder_readable`, Q-GRC-1, never
  scoped to four); **REVOKE `grant-grc-0002` (DRIFT — seat addition) → MINT
  `grant-grc-0003` → REPOINT `row-grc-0001` → ADD the fifth `seat_keys` entry to
  `register.yaml` AND the fifth key to `wal-agent-grc-0001.yaml`** → move the
  consumer gate's literal key count; one walk record at
  `walk-<T2-date>-register-act.md`.

**THE CEREMONY:** hold posted BEFORE the H1 merge → **T1** (H1 merges;
`grant-grc-0002` void from that instant) → **T2** (H2 merges) → the 3.8-equivalent
window check → **step 5b, the register-projection source-revision read** — an
operator-word-gated, read-only observation, **now RATIFIED by
`amend-register-act-5b-projection-proof` (PR #960 → `ac688c40`) and never an
admitted convening**, which reads the domain-content projection only → lift the
hold → `resolved-seats` shows `unbound_conjunction_seats` EMPTY → the proof
convening → **C2 with five seats**, discharging Brett's carried-forward
`convene C2` (13:26:14Z) and `merge the C2 record PR when green` (13:27:23Z).

**FIVE OPEN QUESTIONS went back to Brett** (record § 9, design D8-D12): the
minter of the fifth key; `grant-grc-0003`'s `expires_at`; whether the seat owes
a soak or an activation pass before it sits; one T1/T2 pair or a further split;
whether C2 doubles as the proof convening. Every recommendation is what this
packet already encodes, so taking all five moves no byte.

**ALL FIVE ARE RULED — Brett Heap, in session, window `codeXfactory-2`, no
comment URL, 2026-09-11T17:08:42Z, verbatim:**

> **`accept all A on 971, merge slice 3 when green`**

The first clause is this ruling; the second addresses a different seat's
hermes-install sweep and is not carried here. **Every one is option (a), the
RECOMMENDED one, so the prediction above held and the delta moved no byte** —
proven by diff in the ratifying pull request rather than asserted.

| OQ | decision | RULED (a) | considered, not adopted |
| --- | --- | --- | --- |
| **OQ-1** — who mints and holds the fifth keypair | `design.md` D8 | **(a)** Brett Heap, host-side, the task 3.2 ceremony generalized to one seat: seed in-process, never on disk, `gh secret set` on stdin with `--body` omitted, custody `holder_readable`, secret `COUNCIL_SEAT_SIGNING_KEY_GRC_CLIENT_SECURITY_COMPLIANCE_OFFICER`, a FRESH TTY-gated ceremony | (b) mint through the committed `scripts/mint-factory-origin-key.py`; (c) a different custody model for this key alone |
| **OQ-2** — `expires_at` on `grant-grc-0003` | `design.md` D9 | **(a)** `2027-06-30T00:00:00Z`, unchanged — Q-GRC-3's ruled date, which `grant-mrc-0002` still carries | (b) recompute from the earliest published retirement floor (returns the same date today); (c) a shorter expiry for the new seat |
| **OQ-3** — soak or `activation_gate` before the seat sits | `design.md` D10 | **(a)** bind now, soak later — the lead-architect precedent; **no soak and no activation pass is a precondition of binding**; C13 re-opens this body's soak from zero and costs nothing today | (b) require an LQ-C1-shaped fresh soak first; (c) declare a `gate_rules_council` `activation_gate` (measured: none exists) |
| **OQ-4** — one T1/T2 pair or a further split | `design.md` D11 | **(a)** the T1/T2 PAIR: one codexFactory pull request (H1), then one openxFactory pull request (H2) — two remotes, ONE governed act, the hold spanning them | (b) split H1 into mint / roster / composition pull requests; (c) one cross-repository act (unavailable) |
| **OQ-5** — does C2 double as the proof convening | `design.md` D12 | **(a)** a SEPARATE proof convening precedes C2, on a re-verified clean candidate, as the 2026-09-11 walk did (§ 15, run `34586762846`, admitted) | (b) C2 IS the proof convening; (c) two proof convenings, one each side of the conjunction |

**RATIFICATION REALIZES NOTHING.** No key is minted, no seat is bound, no grant,
row or wallet byte moves, and **C2 stays PARKED under α** — task 6.22's
`resolved-seats` run showing `unbound_conjunction_seats` EMPTY is what lifts it,
not this word. `tasks.md` § 6.1 and § 6.1a tick; **§ 6.1b and §§ 6.2-6.28 stay
open**, and 6.1b — the seat identifier string, an authoring decision flagged for
VETO rather than asked as an OQ — is untouched by a word that ruled the five
questions, so it stays open for its own confirmation before 6.2.

**THE SPEC DELTA IS `## ADDED`, NOT `## MODIFIED`, AND THAT IS MEASURED.** The
pinned CLI 1.12.0 reports *"Archive would refuse this delta:
review-authority-intake: target spec does not exist; only ADDED requirements are
allowed for new specs"* — the capability is authored by two ACTIVE changes and
is not yet canon. Three requirements are appended (7 → 10; 21 → 30 scenarios):
an unbound conjunction seat refuses rather than being dropped; a by-equality pin
carries the exact identifier and its OWN authority reference; a re-issued grant
waits until every identified seat carries a registered key.

## The ruling this realizes

codexFactory PR #165, the OQ-C ruling — Brett Heap, in session,
2026-09-05T17:15Z
(<https://github.com/opensoft/codexFactory/pull/165#issuecomment-5553459343>),
verbatim:

> RULING for this PR's OQ-C (`gate_rules_council` has no projected seat, so a
> signed convening cannot complete) — Brett Heap, in-session,
> 2026-09-05T17:15Z: **operator ratification now, seats later.** … Registering
> gate-rules seats (mint + rows in openxFactory
> `governance/review-authority/register.yaml`) is QUEUED as its own S5-family
> openxFactory change so later convenings are signed.

**This change is that queued change.** It is a PROPOSAL and it PERFORMS
NOTHING: no key is minted, no wallet, grant, attestation or register row is
written, no pin is advanced, no workflow assertion is moved. The intake
register is a PERMANENTLY HUMAN-ONLY SURFACE by ratified requirement and its
exact path is a never-clearable floor member in codexFactory's gate rules, so
every write to it is Brett's operator act. What this change does is SPECIFY,
SEQUENCE and GATE those acts — and it finds, by measurement rather than by
reading, that they cannot be performed at all until a reader defect in a second
repository is fixed.

## The headline, before the detail

**The gate-rules seats cannot be registered against the pinned reader. Two
distinct defects refuse them, and both were MEASURED, not inferred.**

The probe: a copy of the live `governance/review-authority/` tree with a second
authority row (`row-grc-0001`, holder `agent:gate-rules-council`), a matching
wallet, grant and custody attestation, and two gate-rules seat entries; run
through the reader openxFactory pins today
(`openXwallet/scripts/validate-openxwallet.py`, commit
`b7b0fbb3e6d614f60a24737c247e45dada9408aa`, `wallet-v1.4`). The reader's own
words:

```
ERROR [register-minimal-shape-exceeded] …/register.yaml: 2 AUTHORITY rows;
  the ratified first shape is exactly ONE holder/target/act row - wider
  registers are a named successor change.
ERROR [register-seat-duplicate] …/register.yaml:seat_keys[5] (lead-security):
  seat_id 'lead-security' is already recorded at seat_keys[1]; a repeated
  seat_id is refused rather than resolved by file order
```

1. **The single-row cap.** `REGISTER_MVP_SINGLE_ROW = 1`. A second body needs a
   second AUTHORITY row — it cannot descend from `row-mrc-0001`, because
   `_check_seat_keys` requires an entry's `council_ref` to equal the authorizing
   row's `holder_ref`, and that row's holder is
   `agent:merge-readiness-council`. So the cap is not a stylistic bound here; it
   is the thing that makes a second council unrepresentable.
2. **Seat-name uniqueness is GLOBAL, not per council.** The reader's `seen`
   table is keyed on `seat_id` alone across every entry in the file.
   `gate_rules_council` seats `lead-security` and `lead-quality` and
   `company-policy-lead` — three names `merge_readiness_council` already
   records. Three collisions, refused as duplicates of a different body's
   seats. This defect is invisible until a second council arrives, which is why
   nothing has found it before now.

The runtime side, by contrast, is ALREADY READY — checked, not assumed.
hermes-install's `derive_projection`
(`src/hermes_install/review_authority/derivation.py`) keys its duplicate table
on the PAIR `(council_id, seat_id)`, joins each seat to its own authorizing row
through `_rows_by_id`, and reports `councils` as a sorted set. **The projection
can already carry two bodies; only the reader cannot.**

So the order is fixed and is not negotiable:

**openXwallet reader widening → openxFactory pin advance + gate-literal move →
Brett's mint and register act → projection refresh → the first signed
gate-rules convening.**

## What is specified, and what is performed

| | Specified here | Performed here |
|---|---|---|
| The seats, by id | yes | no |
| The wallet / grant / attestation / row shapes | yes | no |
| The mint ceremony | yes (a runbook) | no key is minted |
| The reader widening | yes (as an owed openXwallet change with its red-first tests named) | no code is written |
| The pin advance and the gate literals | yes (as tasks with exact values) | no |
| The projection refresh and the first signed convening | yes (as named owed acts with owners) | no |

## The seats

From codexFactory `hermes/domain/review-councils/gate-rules.yaml` on
`origin/main`, read by identifier and with nothing invented:

| Seat id | Layer | Status in the roster | This change |
|---|---|---|---|
| `lead-architect` | domain | unconditional member | **REGISTER** |
| `lead-security` | domain | unconditional member | **REGISTER** (name collides with the mrc seat — see defect 2) |
| `lead-quality` | domain | unconditional member | **REGISTER** (name collides) |
| `company-policy-lead` | tenant (`members.client.seat`) | unconditional member; `missing_required_seat: refused` names it *"a gate-rules council without its client seat cannot set rules for that repo"* | **REGISTER** (name collides) |
| `client-security-compliance-officer` | tenant | named as `conjunction_pull_in.persona`, NOT as a seat id | **DEFERRED** — open question Q-GRC-4 |
| `intent_owner_role_slot` | project | `binding: symbolic_until_project_roster`, explicitly SYMBOLIC | **DEFERRED** — open question Q-GRC-4 |

**Four seats are registered. Two are deferred and named**, because the register's
own text refuses a seat the council does not seat: *"Adding a seat here that the
council does not seat records authority nothing will ever present."* A symbolic
slot and a persona with no seat identifier are exactly that.

## What each registered seat gets

ONE body, ONE row, FOUR keys — the same arithmetic the merge-readiness council
already stands on, and deliberately not a per-seat grant:

* **One wallet** — `wal-agent-grc-0001`, holder `agent:gate-rules-council`,
  custody `holder_readable`, carrying an operator-vaulted root key
  (`key-grc-0001`) plus the FOUR declared seat keys. Five declared keys, exactly
  the shape `wal-agent-mrc-0001` took at `wallet-v1.3`, and for the same
  ratified reason: the pinned reader's rule (r) refuses an exercise record
  presenting a key no wallet DECLARES.
* **One custody attestation** — `custody-attest-wal-agent-grc-0001.yaml`.
  Without it the unattested cap applies and the grant reaches only `request`.
* **One root grant** — `grant-grc-0001`: `acts: [review]`, `objects:
  [opensoft/openxFactory]`, `authority_tier: act`, `issued_by` the anchored
  operator, `approval_posture` byte-identical to `grant-mrc-0002`'s.
* **One register row** — `row-grc-0001`, exactly the nine fields the reader
  enforces as an exact set, with `expires_at` character-for-character equal to
  the grant's, because the reader compares the two.
* **Four `seat_keys` entries** — `council_ref: agent:gate-rules-council`,
  `council_id: gate_rules_council` (the reader checks the two denote one body),
  `authorizing_row: row-grc-0001`, one `key_id` and one recomputing
  `key_fingerprint` each.

## What this change refuses to pretend

* **It does not claim the seats will be exercised.** `gate_rules_council` has
  NO automated lane: its own roster says a gate-rules convening *"is an
  assembled packet process, not an automated lane"* and that *"what is still
  missing is a caller"* (codexFactory task 5.9a). Registering the seats makes a
  signed convening POSSIBLE; it does not make one happen, and the ratification
  record for PR #165 says plainly that no seat was run.
* **It does not claim a composition is pinned.** `gate-rules.yaml` carries no
  `composition_source_map` and codexFactory's `hermes/domain/agent-mixes.yaml`
  declares a `review_council_profiles` entry for `merge_readiness_council`
  ONLY. There is nothing to pin today, so authoring it is a prerequisite act in
  codexFactory, not an assumption here.
* **It does not close the floor-reachability gap it widens.** codexFactory's
  floor names `governance/review-authority/register.yaml`,
  `contracts/openxwallet-pin.yaml` and the `openXwallet` gitlink — and omits
  `grants/`, `wallets/` and `attestations/`, a PRE-EXISTING gap recorded at
  `split-openxwallet-repo` §8.3 with lead-security's 2026-08-26
  floor-reachability finding still standing. This change adds THREE MORE files
  into that unfloored space, one of which is the grant conferring the
  rule-setting body's own authority. The gap is named with an owner (tasks §4)
  and is NOT declared closed.

## Delta summary

`specs/review-authority-intake/spec.md` — **7 ADDED requirements**, no MODIFIED
and no REMOVED:

1. A second commissioned body enters the register as its own authority row.
2. Seat identity is the pair (`council_id`, `seat_id`), never the seat name alone.
3. A body with no declared composition is not issued review authority.
4. A symbolic seat and a conditionally pulled-in persona are not registered until the council seats them by identifier.
5. The rule-setting body never clears a candidate that edits the register or the artifacts that confer its own authority.
6. A register act a pinned reader cannot represent is sequenced behind the reader and never worked around.
7. One revocation staleness bound governs the whole register.

**No `## MODIFIED Requirements` block.** The MVP shape requirement in
`add-wallet-carried-review-authority` is not amended: its own scenario *"The
minimal shape is exceeded → the additional scope is a named successor rather
than part of the first shape"* is the door this change walks through, and
requirement 1 is that named successor. Editing an active sibling's ratified
text from outside would be the wrong instrument for a door it already left open.

## Open questions

Every one of these is a QUESTION for Brett, with a recommendation. None is
decided here.

### Q-GRC-1 — Where do the four private halves live, given that no gate-rules lane exists?

The merge-readiness seat keys are `holder_readable` because their private halves
sit in codexFactory's `worker-credentials` environment and the `deliberate` job
reads them out of its own process environment — that job IS the holder's
execution context, so the custody declaration describes reality. **For
gate_rules_council there is no such job.** Two exits:

* **(i) Mint into `worker-credentials` now**, `holder_readable`, with the
  custody attestation naming the OWED job (codexFactory task 5.9a) as the
  holder execution context and saying plainly that it does not exist yet.
* **(ii) Mint operator-vaulted now** and re-declare custody when the lane lands
  — a second ceremony, and a wallet whose custody line changes under a live row.

**Recommendation: (i).** The doctrine that minted the mrc conditional seat with
its unconditional trio — *"a candidate whose class seats `company-policy-lead`
must not be the convening that discovers a missing key"* — argues for minting
ahead of the caller, and (ii) buys nothing except a rotation. The attestation
must state the honest posture: the context is named and owed, not observed.

### Q-GRC-2 — The composition pin for a body that has none (Q8's reserved half)

**Q8(d) IS ALREADY RULED and this change does not reopen it**: *"Exact model
versions only. A hosted holder may NOT pin a model family … today's validation
failure is ratified as intended behavior"* (rulings-2026-08-26). What is
genuinely open is narrower and is the half the queuing ruling reserved:
gate_rules_council is a rule-SETTING body convened as an assembled packet, and
it has no declared composition at all. Does it get one, and what is the blast
radius when it does?

**Recommendation: pin it, exactly, from the same enrolled roster**, mirroring
merge-readiness's six declared components — and accept the coupling openly: one
roster model-pin flip (as on 2026-08-31) then revokes BOTH bodies' grants at
once and parks both, which is a scheduled two-body re-issuance with one walk
record per body, not one act for two. The alternative — leaving the rule-setting
body uncomposed so it never drifts — would give the body that sets the rules the
only authority in the estate that no drift cascade can revoke. That is the wrong
body to exempt.

### Q-GRC-3 — The expiry horizon for `grant-grc-0001`

`grant-mrc-0002` expires `2027-06-30T00:00:00Z`, ruled by Brett as option A3 and
bound to the Operator identity record's own review expiry, itself bound to the
earliest published retirement floor among the pinned seat identifiers.

**Recommendation: the same date, `2027-06-30T00:00:00Z`**, so one re-issuance
ceremony covers both bodies and the two grants cannot silently diverge. The
honest caveat travels with it unchanged: nothing in this estate reads a
retirement date, and the expiry is a scheduled event with a named human owner,
not a control.

### Q-GRC-4 — The two deferred seats

`intent_owner_role_slot` is symbolic until the subject-layer roster lands.
`client-security-compliance-officer` is named as a PERSONA on a conjunction
pull-in, not as a seat id, and its predicate `rule_touches_security_posture` has
an implementation and no caller.

**Recommendation: register neither now; do not delete either.** Record both as
owed registrations that trigger on a codexFactory roster act — the project
roster binding for the first, a seat identifier for the second — and require
that whichever act binds them registers the key in the same governed act, so the
first convening that seats them is not the one that discovers a missing key.

> **Amended 2026-09-11.** The ratified question and recommendation above are
> UNCHANGED and are not reopened. The trigger this question names has ARRIVED
> for ONE of the two seats: on 2026-09-11T14:59:26Z Brett Heap ruled *"amend
> register-gate-rules-council-seats, lead-architect route, same model pin as
> lead-security"*, binding `client-security-compliance-officer` to a seat
> identifier and registering its key in the same governed act — exactly as this
> recommendation requires. `intent_owner_role_slot` STAYS DEFERRED, on its own
> unchanged trigger (the subject-layer roster binding), and nothing here brings
> it closer. See § AMENDMENT — 2026-09-11 above, `tasks.md` § 6, `design.md`
> § AMENDED 2026-09-11 (D8-D12) and the record
> `review/amendment-2026-09-11-q-grc-4-discharge.md`.

### Q-GRC-5 — Does the second row retire the cap, or raise it?

The reader widening can either DELETE `REGISTER_MVP_SINGLE_ROW` or raise it to
a declared number.

**Recommendation: replace the scalar cap with the invariant it was standing in
for** — every row resolves end to end, every seat entry attaches to a row that
commissions its body, and (`council_id`, `seat_id`) is unique — rather than
substitute the number 2 for the number 1. A cap of 2 would have to be edited
again by the third body and would say nothing true about why two is right. This
is openXwallet's decision to make in its own change; it is recorded here because
this change is the one asking for it.

## Sequencing, restated as a single order

1. **openXwallet** — the reader widening, red-first (tasks §2). Its own OpenSpec
   change, its own bundle tag.
2. **openxFactory** — pin advance (`commit:`, `contract_bundle_tag:`) plus the
   consumer gate's literal assertions, ONE pull request. Both paths are
   never-clearable floor members, so it is human-landed by construction.
3. **codexFactory** — the `gate_rules_council` composition source map and agent
   mix profile (Q-GRC-2), before the grant is issued.
4. **Brett's walk** — mint, attest, grant, row, in that order, one walk record
   (tasks §3). Human-only surface; nothing agent-written.
5. **hermes-install / operator** — the projection refresh; the visible signal is
   `seat_count` moving 4 → 8 and `councils` gaining `gate_rules_council`.
6. **codexFactory** — the caller that convenes gate-rules and returns signed
   seat returns (task 5.9a). The FIRST SIGNED CONVENING is the gate that makes
   the queuing ruling's *"so later convenings are signed"* true, and it is not
   this change's to perform.

Steps 1–2 have no valid interleaving with step 4: there is no ordering in which
the register carries a second row and the required check is green at the pinned
reader. That is the finding, and it is why this proposal is a sequencing
document as much as a specification.
