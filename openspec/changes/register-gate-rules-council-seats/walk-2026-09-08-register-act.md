# Walk record — the 2026-09-08 REGISTER ACT for `gate_rules_council`, against `docs/council-seat-key-mint-runbook.md`

<!-- FILENAME RESOLVED. This file was drafted as `walk-PENDING-register-act.md`
     and renamed to `walk-2026-09-08-register-act.md` on 2026-09-08, when the
     operator's public values landed and the walk had actually been walked. The
     precedent walk is named by the day it was walked, and naming this one
     before it was walked would have been the sort of anticipated fact this
     record exists to refuse. -->

Status: record
Kind: report
Repository context: openxFactory
Walked: 2026-09-08
Runbook walked: [`docs/council-seat-key-mint-runbook.md`](../../../docs/council-seat-key-mint-runbook.md)
  — `Status: ratified` (`Ratified by: register-gate-rules-council-seats`,
  flipped by task 1.6 in this same act), steps **§0**, **§1**, **§2**, **§3**,
  **§4**, **§5** and **§6**
The act: **the human-ratified REGISTER ACT commissioning a SECOND body** —
  sequencing step 4 of
  [`proposal.md`](proposal.md)'s 2026-09-07 AMENDMENT, tasks **§3.2–§3.9** with
  **§2.8**'s deferred consumer-gate literal flip performed in the same act
Ratifying human: **Brett Heap** (`Brett.Heap@opensoft.one`)
Effective instant: **`2026-09-08T12:31:36Z`** — ONE instant, taken once and
  written identically into `grant-grc-0001`'s `issued_at`, into every
  `declared_at` and `created_at` in `wal-agent-grc-0001.yaml`, and here. It is
  the instant the mint run COMPLETED (§3B.3), following the predecessor walk's
  definition of this field exactly: there it was `2026-09-02T13:33:48Z`, written
  identically into `grant-mrc-0002`'s `issued_at`, `grant-mrc-0001`'s
  `revocation.revoked_at` and that walk's own header. **It is NOT the merge
  instant**, and nothing in this record is deferred to one.
Predecessor walk: [`../add-wallet-carried-review-authority/walk-2026-09-02-register-act.md`](../add-wallet-carried-review-authority/walk-2026-09-02-register-act.md)
  — the 2026-09-02 re-issuance for `merge_readiness_council`, whose form this
  record follows. **It is a PREDECESSOR IN FORM, not in substance:** that act
  was a governed RE-ISSUANCE under `docs/governed-reissuance-runbook.md`; this
  one is a COLD START under the mint runbook, and no grant is superseded here.
Lane: `hermes-wallet-exercise`
  (CLAIMED on PR #717,
  <https://github.com/opensoft/openxFactory/pull/717#issuecomment-5576437395>)

---

## 0. THE HEADLINE, BEFORE THE DETAIL

**The register act was performed, and it commissioned a SECOND BODY into a
register that had carried exactly one row since it was created.**
`agent:gate-rules-council` — codexFactory's cross-layer rule-SETTING council —
now holds `wal-agent-grc-0001` (five declared keys), an attested
`holder_readable` custody row, the root grant `grant-grc-0001`, the authority
row `row-grc-0001`, and four per-seat signing keys in the register's
`seat_keys` surface. `row-mrc-0001` is untouched and
`revocation_staleness_bound: P7D` is untouched.

**THE KEYS WERE MINTED ON 2026-09-08 AND THE CUSTODY IS WRITTEN DOWN, NOT
SUMMARISED** (§3B). Five Ed25519 keypairs; the four seat halves stored into
codexFactory's `worker-credentials` environment and each confirmed present
between `04:18:53Z` and `04:19:00Z`; the root half printed once to the
operator's terminal and held there until he vaulted it and cleared the screen at
`12:29:23Z`. That eight-hour window is on the record because it happened, not
because any gate measured it.

**IT IS A COLD START, NOT A RE-ISSUANCE.** This body has never held a wallet, a
grant or a row. Nothing is revoked, nothing is superseded, and
`docs/governed-reissuance-runbook.md` does not govern here — `§0.2` of the mint
runbook draws that line explicitly.

**THE SEATS ARE REGISTERED AND UNEXERCISED, and that is the most important
sentence in this record.** **No `gate_rules_council` convening has ever run.**
Measured, not assumed: codexFactory workflow `gate-rules-convening.yml`
(id **352457764**) reports **`total_count: 0`**. This act records authority
that has never been presented, and the whole of what it proves is that the
FILES are consistent.

**What is NOT done, and none of it is a formality:**

* **THE PROJECTION IS NOT REFRESHED BY THIS ACT** (§7). **Until the Hermes
  register projection is re-derived, the runtime keeps refusing with
  `review_authority.root_key_mismatch` and NO AUTHORITY FLOWS.** Stopping at the
  register act is the commonest way to think this ceremony is finished when it
  is not.
* **NO CONVENING WAS ADMITTED, and none could be** (§8). The park is lifted when
  a real convening is admitted against the new grant; none has ever run.
* **NO ADEQUACY CLAIM IS MADE ABOUT THIS BENCH.** LQ-C1 forbids it and LQ-C4
  leaves the underlying question open (§8).

---

## 1. What each step produced

Each row says what the step PRODUCED. A tick would say only that somebody
looked.

| Runbook step (the runbook's own labels) | Exercised? | What it produced |
|---|---|---|
| **§0.1 the five preconditions** | yes | §2 — five checked, one (the consuming gate's literals) discharged BY this act rather than before it |
| **§0.3 who holds which act** | yes | §6 — the capacities, disclosed and not collapsed |
| **§1 read the roster, write the seat list down** | yes, **before minting** | §3 — six roster entries, FOUR registered and TWO deliberately not, each with its reason |
| **§2 mint, offline** | **YES — [OPERATOR]**, 2026-09-08 | five keypairs; the program, its command log and the custody timeline in **§3B**; codexFactory `hermes/domain/review-councils/records/2026-09-08-gate-rules-seat-signing-keys-minted.md` |
| **§2.1 where the private halves go** | **YES** | **§3B.3** — root in the operator's vault (printed once to the TTY, vaulted by hand, screen and scrollback cleared on the operator's confirmation); four seat halves as `COUNCIL_SEAT_SIGNING_KEY_GRC_<SEAT>` on codexFactory environment `worker-credentials`, custody complete at **`2026-09-08T04:19:00Z`** |
| **§3.1 the wallet** | **YES** | `governance/review-authority/wallets/wal-agent-grc-0001.yaml` — FIVE declared keys |
| **§3.2 the custody attestation** | **YES** | `governance/review-authority/attestations/custody-attest-wal-agent-grc-0001.yaml` — kindless, `verified_at: 2026-09-08T04:19:00Z` |
| **§3.3 the grant** | **YES** | `governance/review-authority/grants/grant-grc-0001.yaml` — ROOT grant, `issued_at: 2026-09-08T12:31:36Z` |
| **§3.4 the register row + seat keys** | **YES** | `governance/review-authority/register.yaml` — `row-grc-0001` plus four `seat_keys` entries, **append-only** |
| **§4 the consuming gate's literals, in the same change** | **YES** | `.github/workflows/openxwallet-consumer-gate.yml` — `4 of 4` → `8 of 8`, plus a SEPARATE `wal-agent-grc-0001` assertion (task 2.8's deferred flip) |
| **§5 run the gate locally, before you push** | **YES** | §5 — the before/after log lines, and **§5.1**, the consuming gate's own 13 assertions replayed against this tree |
| **§5b the projection** | **NO** | §7 — what it takes, who owns it, and what it costs until then |
| **"verify one convening admits"** | **NO — impossible today** | §8 |
| **the citations the act is fixed at** | yes | **§3A** — four, each OPENED AND READ rather than cited from memory |
| **§6 the walk record** | yes | This document |

**Bookkeeping performed in the same act, and named so it is not mistaken for
part of the ceremony:** task **1.6** (the runbook's own `Status: draft` →
`Status: ratified`) and task **3.1**'s tick (a codexFactory realization, ticked
here because openxFactory's task list is where the row lives).

---

## 2. Step 0 — the five preconditions, each checked rather than assumed

The mint runbook's `§0.1` names five preconditions, "each of which has refused
an act before".

| # | Precondition | State at this act | Evidence |
|---|---|---|---|
| 1 | **The reader can represent what you are about to write** | **MET** | `contracts/openxwallet-pin.yaml` at `wallet-v1.5` / `f3eb929b`, gitlink identical. `REGISTER_MVP_SINGLE_ROW` is **RETIRED BY NAME** in the widened reader, and the seat-duplicate table is keyed on the PAIR (`council_id`, `seat_id`) |
| 2 | **The body has a DECLARED COMPOSITION** | **MET** | codexFactory PR #277 → `511d95c5`: `agent-mixes.yaml#review_council_profiles.gate_rules_council` and `gate-rules.yaml#council.composition_source_map`, six components, exact identifiers |
| 3 | **The seats are read from the roster BY IDENTIFIER** | **MET** | `gate-rules.yaml#council.id: gate_rules_council`; four seat ids; two non-seats named and excluded (§3) |
| 4 | **Every count the consuming gate asserts is LITERAL** | **DISCHARGED BY THIS ACT** | task 2.8's deferred flip, performed here (§4.5) |
| 5 | **Nothing is green halfway** | **HONOURED** | wallet, attestation, grant, row, seat keys and the gate literals are ONE change |

**Precondition 1 was the hard one and it is the reason this act is late.** The
pinned reader **refused this exact shape** at `wallet-v1.4`, twice over, and
both refusals were MEASURED rather than predicted (design D5):
`register-minimal-shape-exceeded` on a second authority row, and
`register-seat-duplicate` on `lead-security` — a seat BOTH bodies seat. The
exits that would have made the gate green by narrowing the act were enumerated
and each was refused. **The fix was taken where the defect lived**: openXwallet
#16/#17/#18, merged `f3eb929b`, tag `wallet-v1.5`, under Q-GRC-5's ruling to
replace the scalar cap with the invariants it stood in for. Then the pin advance
was proved **NEUTRAL at one row before the register moved** (task 2.9) — which
is why this record can attribute any change in the gate's output to the register
act rather than to the reader.

---

## 3. Step 1 — the roster, written down BEFORE anything was minted

Read from `origin/main`, never from a local checkout
(`git -C <codexFactory> show origin/main:hermes/domain/review-councils/gate-rules.yaml`).
The council `id`, **VERBATIM**, is `gate_rules_council`.

| Roster entry | Layer | Declared as | Pinned model | Registered? |
|---|---|---|---|---|
| `lead-architect` | domain | `members.domain` | `claude-opus-5` (**R1**) | **REGISTERED** |
| `lead-security` | domain | `members.domain` | `claude-opus-5` | **REGISTERED** |
| `lead-quality` | domain | `members.domain` | `claude-sonnet-5` | **REGISTERED** |
| `company-policy-lead` | tenant | `members.client.seat` | `claude-sonnet-5` | **REGISTERED** |
| `client-security-compliance-officer` | tenant | `members.client.conjunction_pull_in.persona` | — | **NOT registered** |
| `intent_owner_role_slot` | project | `members.project.seat`, `binding: symbolic_until_project_roster` | — | **NOT registered** |

**THE TWO OMISSIONS ARE DECISIONS ON RECORD, NOT OVERSIGHTS.** Q-GRC-4, RULED
2026-09-06T14:13:46Z: *"register neither deferred seat now; delete neither."*
`client-security-compliance-officer` is named as a conjunction **persona** and
carries no seat identifier — its predicate is implemented and evaluated, and
when it HOLDS with no identifier declared the convening REFUSES with
`conjunction_seat_unbound` rather than dropping the seat or inventing a name.
`intent_owner_role_slot` is the neutral skeleton's symbolic slot. **A key
recorded for either would record authority nothing will ever present.** The
obligation lands on a FUTURE act: whichever codexFactory roster act binds them
registers the key **in the same governed act**, so the first convening that
seats one is not the convening that discovers a missing key (task 4.6).

**THE TWO SPELLINGS OF ONE BODY, both recorded on purpose.** `council_ref:
agent:gate-rules-council` is the AUTHORITY ATTACHMENT and must equal the
authorizing row's `holder_ref`; `council_id: gate_rules_council` is the RUNTIME
NAME, carried VERBATIM into the Hermes projection, which keys its seat lookup on
the exact pair. Neither is derivable from the other by any declared rule, so
both are recorded and neither is invented at projection time. The reader checks
that they denote one body (`council_ref == "agent:" +
council_id.replace("_","-")`).

**CONDITIONAL SEATS ARE MINTED WITH THE UNCONDITIONAL ONES.** The tenant seat
`company-policy-lead` is seated unconditionally by THIS body's roster; the
conditional company-policy pull-in this council may declare is a rule it writes
for OTHER councils' convenings, not a condition on its own bench. It is
registered with the domain trio either way, on the runbook's rule that a
candidate whose class seats a conditional seat must not be the convening that
discovers a missing key.

---

## 3A. THE CITATIONS THIS REGISTER ACT IS FIXED AT

**Numbered `3A` rather than `4`, on purpose.** The precedent walk carries this
section in this position, as its §3. Renumbering the sections already written
below would silently move every `§`-reference in this record, in `tasks.md` and
in the pull request that carries it — and a silent renumber inside a governed
act is exactly the class of edit this form exists to refuse. The POSITION
follows the precedent; the LABEL does not pretend the record was written in a
different order than it was.

**EACH OF THE FOUR WAS OPENED AND READ FOR THIS RECORD.** None is cited from
memory, and each row says what was read rather than that something was checked.

| # | The citation | Where | What was read, verbatim enough to fix the act |
|---|---|---|---|
| **(i)** | **THE RATIFICATION** | `review/ratification-2026-09-06.md` | `Status: ratified`; *"Ratified: 2026-09-06 by Brett Heap (repository owner) — in-session at 2026-09-06T14:13:46Z, verbatim: **\"lets take them in your recommended order all approved\"**"*, given against the lane's board whose item 3 read *"Ratify openxFactory #717 with rulings on Q-GRC-1 to Q-GRC-5."* Ratified baseline head `169f84ef`. PR **#717** → `a59f2ae5`. **Each of Q-GRC-1..Q-GRC-5 carried one recommendation and each is ruled as recommended** — which is why Q-GRC-1's premise moving needed its own ruling (B2, §4.2) rather than a reinterpretation. |
| **(ii)** | **THE R1/R2 AMENDMENT** | `proposal.md` § *"AMENDMENT — 2026-09-07 (R1/R2: lead-architect pin; 5.9a before 3.1)"* | Brett Heap, in-session, **2026-09-07T12:40:19Z**, verbatim: **"R1 lead-architect claude-opus-5, R2 (a) — re-sequence 5.9a first"** (<https://github.com/opensoft/openxFactory/pull/717#issuecomment-5570774593>), landed as PR **#751**. **R1** pins `lead-architect` to the exact identifier `claude-opus-5` through a RECORDED roster-change act. **R2(a)** mirrors merge-readiness's six declared components verbatim and RE-ORDERS § Sequencing so codexFactory task **5.9a** precedes row **3.1**. The restated order is **(1) openXwallet reader widening → (2) openxFactory pin advance + gate-literal move (#740 → `30eccf0c`) → (3′) codexFactory 5.9a + R1's roster act → (3) codexFactory row 3.1 → (4) THIS ACT → (5) the projection refresh → (6) the first signed convening.** **This act is step (4), and (1), (2), (3′) and (3) are all complete before it.** |
| **(iii)** | **THE ROSTER-CHANGE RECORD** | codexFactory `origin/main`: `hermes/domain/review-councils/records/2026-09-07-gate-rules-roster-lead-architect-pin.md` | `Status: record`. Its own header, verbatim: *"**NO SEAT WAS RUN, AND NO COUNCIL SELECTED THIS PIN.** The selection is Brett Heap's, as repository owner, operator and convener, given in session on 2026-09-07 as ruling **R1**."* And: *"This record amends no rule, no threshold, no floor, no clearable set, no kill switch and no council membership."* It declares itself a **DIRECT OPERATOR SELECTION in the pre-015 assembled-packet form, not a convening outcome**, and states that **no openxFactory task is ticked there**. |
| **(iv)** | **THE OPERATOR IDENTITY RECORD** | `../add-wallet-carried-review-authority/operator-identity-record-2026-09-01.md` | **SIGNED by the Operator (Brett Heap) 2026-09-01, in-session**, drafted 2026-08-31 by the Opus soak executor at the coordinator's direction. Every field the drafter could not evidence was marked `OPERATOR-VERIFICATION-PENDING` with the place it is read back, and each now carries the Operator's read-back (EXE-3, EXE-5, SEM-1) or live-run evidence (EXE-4/EXE-6 from xFactory run 33513966619; EXE-1/EXE-2 from run 33577170272). It is the record the predecessor register act carried to its governed home; **this act neither amends nor re-signs it, and adds no identity of its own.** |

**WHAT THE FOUR FIX, TAKEN TOGETHER.** (i) fixes the AUTHORITY to perform this
act and the five rulings its shape obeys. (ii) fixes the ORDER — this act is
step (4), and it may not run before (3′) and (3), which is why the seat keys
can be minted against a caller and a composition that both exist. (iii) fixes
the ROSTER the seat list is read from, and fixes what that roster's provenance
is and is not. (iv) fixes the OPERATOR whose `issued_by` appears on
`grant-grc-0001`.

**AND WHAT NO CITATION FIXES.** There is no citation here for the BENCH's
adequacy, because no such record exists: LQ-C1 forbids the claim and LQ-C4
leaves the underlying question open (§8). A reader looking for a fifth row that
says this council can do its job will not find one, and its absence is the
record.

---

## 3B. THE MINT ITSELF — the program that ran, its command log, and the custody timeline

**§2 and §2.1 of the runbook are the OPERATOR's steps, and they happened before
any file below was written.** They are recorded here in the same detail as the
writes, because a mint whose custody is not written down is a mint whose custody
cannot later be audited.

### 3B.1 The program

**A LANE-AUTHORED, HOST-SIDE PROGRAM. IT IS IN NO REPOSITORY**, and that is
stated first so no later reader searches for it in one:

```
~/session-prompts/mint-grc-council-seats/tools/mint-grc-council-seats.py
~/session-prompts/mint-grc-council-seats/tools/test_mint_grc_council_seats.py
```

**IT MIRRORS THE ORIGIN-KEY PRECEDENT AND INVENTS NO NEW DERIVATION PATH.** Its
sibling in form is openxFactory's own `scripts/mint-factory-origin-key.py`, the
program that minted `key-origin-0001` on 2026-09-03. What it does, measured
against its own source rather than its docstring:

* **The seed is generated IN-PROCESS** (`secrets.token_bytes(32)`) and is never
  written to any file.
* **It reaches `gh secret set` ON STDIN, with NO `--body` flag** — omitting the
  flag is what makes `gh` read the value from stdin, so the seed is never an
  argv element and never enters shell history or a process listing. (`--body -`
  is NOT the same thing and would store the literal string `-`; the program says
  so in its own comment.)
* **The four public values are derived IN-PROCESS through the PINNED reader** —
  `scripts/validate-factory-identity.py`'s own `derive` entry point, imported as
  a module rather than reimplemented. The program contains no derivation of its
  own, refuses if `derive` refuses, and re-checks that the derived `did` is
  `did:key:` + its own multibase, that the base64url spelling round-trips, that
  `public_key` is 43 characters and that `key_fingerprint` carries the `sha256:`
  prefix.
* **The ROOT seed is printed ONCE, to the TTY**, never to a file and never to a
  pipe.
* **Its own directory is a SCRATCHPAD.** The durable outputs — `values.json`
  (public values only) and the command log — were written to
  `~/session-prompts/mint-grc-council-seats/`. **No shred is claimed, and none
  was needed for key material: no seed was ever on disk to shred.** That is a
  narrower claim than the 2026-08-28 precedent's *"the minting directory was
  shredded"*, and it is narrower on purpose.

**ITS TEST SUITE: 23 TESTS, PASSING WHEN THE MINT RAN (2026-09-08).** They no
longer pass, and the reason is stated rather than left as a discrepancy: the
suite's `env_root` fixture copies
`openspec/changes/register-gate-rules-council-seats/walk-PENDING-register-act.md`
into a temporary tree, and the fill step renamed that file to this one. All 23
now ERROR AT SETUP with `FileNotFoundError` on that path, and none of them fails
on an assertion.

### 3B.2 The command log

`~/session-prompts/mint-grc-council-seats/mint-grc-command-log.txt` — **argv and
STDIN LENGTHS only; the program never logs stdin content** (its own line is
`[CONTENT NEVER LOGGED]`). Its material lines:

```
2026-09-08T04:08:02Z  # run start: … --preflight-only
2026-09-08T04:10:35Z  # run start: … --preflight-only
2026-09-08T04:18:43Z  # run start: … --preflight-only
2026-09-08T04:18:43Z  # run start: mint-grc-council-seats.py   (the real run)
2026-09-08T04:18:51Z  gh secret set COUNCIL_SEAT_SIGNING_KEY_GRC_LEAD_ARCHITECT      … stdin 64 byte(s) [CONTENT NEVER LOGGED]
2026-09-08T04:18:53Z  gh secret set COUNCIL_SEAT_SIGNING_KEY_GRC_LEAD_SECURITY       … stdin 64 byte(s) [CONTENT NEVER LOGGED]
2026-09-08T04:18:55Z  gh secret set COUNCIL_SEAT_SIGNING_KEY_GRC_LEAD_QUALITY        … stdin 64 byte(s) [CONTENT NEVER LOGGED]
2026-09-08T04:18:57Z  gh secret set COUNCIL_SEAT_SIGNING_KEY_GRC_COMPANY_POLICY_LEAD … stdin 64 byte(s) [CONTENT NEVER LOGGED]
2026-09-08T12:31:36Z  # mint complete: 4 seat secret(s) stored and confirmed, root key handed to the operator's vault, values.json written
```

Each `gh secret set` is followed in the log by a `gh secret list` against the
same environment — the CONFIRMATION, not a second write. **Three preflight-only
runs preceded the real one and each logged `# preflight-only: nothing generated,
stored or written`.**

### 3B.3 THE CUSTODY TIMELINE, stated plainly

**The four SEAT halves** — 64 lowercase hex of the 32-byte seed, one per seat —
were stored into **`opensoft/codexFactory` environment `worker-credentials`**
and each was confirmed present:

| Secret | Stored | Confirmed present |
|---|---|---|
| `COUNCIL_SEAT_SIGNING_KEY_GRC_LEAD_ARCHITECT` | `2026-09-08T04:18:51Z` | **`2026-09-08T04:18:53Z`** |
| `COUNCIL_SEAT_SIGNING_KEY_GRC_LEAD_SECURITY` | `2026-09-08T04:18:53Z` | **`2026-09-08T04:18:55Z`** |
| `COUNCIL_SEAT_SIGNING_KEY_GRC_LEAD_QUALITY` | `2026-09-08T04:18:55Z` | **`2026-09-08T04:18:57Z`** |
| `COUNCIL_SEAT_SIGNING_KEY_GRC_COMPANY_POLICY_LEAD` | `2026-09-08T04:18:57Z` | **`2026-09-08T04:19:00Z`** |

**`verified_at: 2026-09-08T04:19:00Z` on the attestation is the FOURTH
confirmation** — the instant custody of the seat halves became complete, and
therefore never earlier than any single one of them.

**The ROOT half, `key-grc-0001`, and the eight hours it was on a screen.** There
is no vault tool named in either the mint runbook's §2.1 or the 2026-08-28 mrc
precedent; both say only that the body's root key goes to the operator's own
vault and never to git, CI or an agent session. So the seed was **printed once
to the operator's terminal, shortly after `2026-09-08T04:19:00Z`**, and it
**remained on that screen until the operator had stored it in his vault
(1Password) and pressed Enter at `2026-09-08T12:29:23Z`** — a window of
**8 hours and 10 minutes**. The program then emitted the clear-screen and
scrollback-clear sequence and asked for confirmation; **the operator typed `y`,
confirming the seed was gone from the display**
(`clear_sequence_emitted: true`, `operator_confirmed_clear: true`). The run
completed at **`2026-09-08T12:31:36Z`**, which is `grant-grc-0001`'s `issued_at`
and this record's Effective instant.

**That window is recorded because it is a fact about this mint, not because it
is claimed to be safe or unsafe.** No gate measured it, no rule bounds it, and
nothing in this estate would have refused the act had it been longer or shorter.

### 3B.4 What `values.json` is, and what it is not

`~/session-prompts/mint-grc-council-seats/values.json` carries the **five
`{pub, fp, did, mb}` quadruples, the three instants, the walk date and the
per-key custody block — PUBLIC VALUES ONLY.** Both the mint program and the fill
program **REFUSE outright** — exit non-zero, write nothing — on any string of 64
bare hex characters without a `sha256:` prefix, on the ground that such a string
is the encoding of a private Ed25519 seed. The refusal is upstream of the pinned
reader's own shape refusal on purpose: the reader's would happen after the value
was already in a commit.

**AND IT WAS RE-CHECKED ON THIS TREE.** Every file this act touches was scanned
for 64-hex strings not preceded by `sha256:`: **zero hits, across all nine
files.**

---

## 4. Step 5 — the acts, verbatim

**FIVE WRITES AND ONE GATE MOVE, IN ONE CHANGE**, in the runbook's §3 order:
wallet → attestation → grant → row → seat keys → gate literals. Each resolves
against the one before it, and there is no ordering that is green halfway.

### 4.1 THE WALLET — `wal-agent-grc-0001`

| Field | Value |
|---|---|
| `wallet_id` | **`wal-agent-grc-0001`** |
| `holder.holder_id` / `holder_class` | `agent:gate-rules-council` / `agent` |
| `custody.model` | **`holder_readable`** |
| `key_reference` | **`key-grc-0001`** — did `did:key:z6MkqohimztNL3Moz7JzsoRx13Fbad2VDHBwG7rKMGU2xsaA`, multibase `z6MkqohimztNL3Moz7JzsoRx13Fbad2VDHBwG7rKMGU2xsaA`, `ed25519`. **NO `key_fingerprint`** — the mrc precedent's asymmetry, not an omission |
| `keys[]` | **FOUR** seat keys, each with `did`, `key_id`, `key_fingerprint`, `public_key_multibase`, `signature_algorithm`, `display_label` and its own `custody` block |
| **Declared keys** | **FIVE** — `declared_keys()` = `key_reference` + `keys[]` |

**WHY THE SEAT KEYS ARE DECLARED HERE AND NOT ONLY IN THE REGISTER.** The pinned
reader's rule (r) refuses an exercise record presenting a key no wallet
declares, and hermes-install writes the REGISTER-RECORDED `key_id` into
`presenting_key_ref`. A register-only recording would make this body's first
signed seat return **unrepresentable on arrival**.

**The file sits outside any `examples/` path**, or the scanner would silently
stop treating it as live.

### 4.2 THE CUSTODY ATTESTATION — `attest-custody-wal-agent-grc-0001`

**KINDLESS ON PURPOSE.** No `kind:` key: no contract schema for custody
attestation exists in the openxwallet family, this change authorizes none, and
inventing one would be an unratified contract release. Carrying no `kind:` means
`repo_scan` SKIPS the file and the register reader consumes it. **Without it the
unattested cap applies and `grant-grc-0001` reaches only `request`.**

| Field | Value |
|---|---|
| `custody_model_attested` | `holder_readable` |
| `verified_by` | Brett Heap, responsible operator, Human Escalation Contract |
| `verified_at` | **`2026-09-08T04:19:00Z`** — the secret-provisioning instant |
| `isolation_claimed` | **`none`** — the honest posture, not an assurance |

**THE HOLDER EXECUTION CONTEXT: Q-GRC-1'S PREMISE MOVED, AND THIS RECORD
CORRECTS IT RATHER THAN REPEATING IT.** Q-GRC-1 was ruled on 2026-09-06 against
a world in which the owed job did not exist, and its wording anticipated an
attestation that *"states plainly that it does not exist yet."* **It now
exists.** codexFactory `.github/workflows/gate-rules-convening.yml` landed with
task 5.9a in PR #277 → `511d95c5` on 2026-09-07, declares `environment:
worker-credentials`, and is exactly the context these four secrets are
provisioned into. Writing "the job does not exist yet" would now be false, and
the runbook's own rule governs the correction: *"Do not describe a context you
have not seen."*

**So the attestation records three measured facts and one honest limit** —
which is a STRONGER claim than the ruling assumed, not a weaker one:

1. **THE JOB EXISTS**, at codexFactory `origin/main`, with `environment:
   worker-credentials`.
2. **IT HAS NEVER RUN.** Workflow id **352457764**, `total_count: **0**`.
3. **IT REFUSES TODAY**, deliberately, with `seat_signing_unavailable` — a
   fail-closed presence check that parks the convening precisely because these
   four secrets are absent.
4. **THE WIRING IS PRESENCE-ONLY.** The four secret names appear in that
   workflow at its `env:` mapping and in the emptiness test of that refusal, and
   **nowhere else**. **No signing step consumes them yet.** Provisioning the
   four halves LIFTS THE REFUSAL; it does not by itself produce a signed seat
   return.

**THE RULINGS AS SPOKEN, B2 entry.** In the same form as Q-GRC-1..Q-GRC-5 above
(`review/ratification-2026-09-06.md`, "The five rulings"):

- **B2 RULED — Brett Heap, in-session, 2026-09-08T03:20:24Z, verbatim
  *"B2 as recommended"***
  (<https://github.com/opensoft/openxFactory/pull/717#issuecomment-5578601346>):
  Q-GRC-1 was ruled 2026-09-06 against a world where codexFactory task 5.9a
  (the `gate_rules_council` convening caller) did not exist and anticipated an
  attestation that "states plainly that it does not exist yet." 5.9a has since
  LANDED (codexFactory PR #277 → `511d95c5`;
  `.github/workflows/gate-rules-convening.yml`, `environment:
  worker-credentials`, workflow id 352457764, zero runs, refusing today with
  `seat_signing_unavailable`; the four GRC seat secrets are read presence-only,
  no signing step consumes them). B2 adopts the recommendation that the
  attestation name that job as the holder execution context and state that it
  EXISTS and has NEVER RUN, that no signing step consumes the secrets yet, and
  that the context is therefore named and owed rather than observed — a
  STRONGER, not weaker, claim than Q-GRC-1 assumed; `isolation_claimed: none`
  stands. This corrects the four-item list above from "owed job" to
  "existing-and-never-run job" without reopening Q-GRC-1 itself.

**THE SECRET NAMES ARE GRC-NAMESPACED, and the reason is a collision rather
than a style.** The 2026-08-28 merge-readiness mint took its names from
`root_key_env_var()`'s output, which is **not council-aware**. So
`COUNCIL_SEAT_SIGNING_KEY_LEAD_SECURITY` already holds the *merge-readiness*
seat's seed, and `lead-security` is a seat both bodies seat. An unnamespaced
name here would not be a second secret; it would be a collision on the first.
The landed caller declares `COUNCIL_SEAT_SIGNING_KEY_GRC_<SEAT>` and a test
holds it there. **This is recorded here because no governed openxFactory
document names those secrets** — the mint runbook names no secret and does not
say how a second council's names avoid the first's. That gap is real and is
named in §8.

### 4.3 THE GRANT — `grant-grc-0001`

| Field | Value |
|---|---|
| `grant_id` | **`grant-grc-0001`** |
| `parent_grant_ref` | **ABSENT — ROOT grant.** `parent_grant_ref` means DERIVED FROM; nothing here is derived from either mrc grant |
| `audience` | `wal-agent-grc-0001` / `agent:gate-rules-council` |
| `scope.acts` | `[review]` |
| `scope.objects` | `[opensoft/openxFactory]` |
| `scope.authority_tier` | `act` |
| `scope.approval_posture` | **byte-identical to `grant-mrc-0002`'s three lines** (diffed, not eyeballed) |
| `expires_at` | **`2027-06-30T00:00:00Z`** (Q-GRC-3) |
| `issued_at` | **`2026-09-08T12:31:36Z`** |
| `issued_by` | **`Brett.Heap@opensoft.one`** |
| `state` | `active` |

**THE SCOPE WAS EXAMINED, NOT PASTED**, and each element's reason is on the
file's own face. This is a cold start, so nothing is inherited and every element
is a FIRST choice — which makes the record more owed here, not less.

**`objects: [opensoft/openxFactory]` NEEDS ITS OWN SENTENCE BECAUSE IT LOOKS
WRONG AT FIRST READING.** This body governs **codexFactory's** gate rules, so a
reader expects `opensoft/codexFactory`. It is `opensoft/openxFactory` for a
structural reason and not because `grant-mrc-0002` says so: the reader enforces
SET EQUALITY between this list and the backing row's `target_repo`; the register
is an openxFactory artifact adjudicated inside THIS repository's REQUIRED
`wallet-validation` check; and `repo_scan` builds its context from the scanned
repository's own records, so a cross-repository audience has no resolution path
today (clarifications N7). A row naming `opensoft/codexFactory` would be a row
this estate cannot resolve — **not a wider authority, an unresolvable one.**
**The object is the repository whose REVIEW this register commissions; the
body's DOMAIN of rule-setting is a different thing that no field here carries.**

**Tier `act` stands on the attestation and on nothing else.** Without
`custody-attest-wal-agent-grc-0001.yaml` the unattested cap holds this grant at
`request`. `act_unsupervised` is refused outright for review authority and was
never a candidate.

### 4.4 THE ROW AND THE SEAT KEYS — `register.yaml`

| | |
|---|---|
| **Row** | `row-grc-0001` — **exactly nine fields**, exact set equality enforced by the reader |
| `expires_at` | **character-for-character equal** to `grant-grc-0001`'s, because the reader compares the two |
| **Seat entries** | **FOUR appended**, **exactly seven fields each** |
| `council_ref` / `council_id` | `agent:gate-rules-council` / `gate_rules_council` |
| `authorizing_row` | `row-grc-0001` (all four) |

**`row-mrc-0001` IS NOT TOUCHED AND `revocation_staleness_bound: P7D` IS NOT
TOUCHED — and that is MEASURED, not asserted.** `git diff --numstat --
governance/review-authority/register.yaml` reports **`129  0`**: one hundred and
twenty-nine lines added, **zero deleted**. One bound governs the whole register
(design D7), and tightening it is its own governed edit, never a tidy-up inside
a mint.

**THREE SEAT IDS NOW APPEAR TWICE IN ONE FILE.** `lead-security`,
`lead-quality` and `company-policy-lead` are seated by both bodies. That is
legal **only** at `wallet-v1.5`, whose duplicate table is keyed on the PAIR.
**`key_id` and `key_fingerprint` uniqueness stays GLOBAL** — a key is one key,
and two bodies presenting it would be two claims on one identity — which is why
every key id below carries the `grc` namespace.

| Seat | `key_id` |
|---|---|
| `lead-architect` | `key-grc-seat-lead-architect-0001` |
| `lead-security` | `key-grc-seat-lead-security-0001` |
| `lead-quality` | `key-grc-seat-lead-quality-0001` |
| `company-policy-lead` | `key-grc-seat-company-policy-lead-0001` |

**NO PRIVATE HALF, SEED OR PASSPHRASE APPEARS IN ANY FILE UNDER
`governance/`.** A `public_key` is 43 characters of canonical unpadded
base64url; a 64-hex private seed is refused **by shape**, in the required check
— but the refusal would happen after it was already in a commit, which is why
the discipline is upstream of the gate and not delegated to it.

### 4.5 THE GATE MOVE — task 2.8's deferred literal flip, performed HERE

`.github/workflows/openxwallet-consumer-gate.yml`:

* `intake register: **4 of 4** per-seat signing key(s) adjudicated and resolved`
  → **`8 of 8`**, and the failure message's "four" → "eight";
* a **NEW, SEPARATE** assertion
  `^note  wallet 'wal-agent-grc-0001': 5 declared key\(s\) adjudicated ` beside
  the mrc one, in the same form (trailing space; the parenthetical key list
  deliberately unasserted) — **the existing assertion is NOT widened**, per the
  runbook's §4: a single assertion covering either wallet would go green on a
  tree that lost one of them;
* the conjunction echo's grep alternation gains `wal-agent-grc-0001`, or the
  echo would hide the new line it exists to show.

**Every count stays LITERAL.** A wildcard would let a register that lost a body
pass the positive proof, which is the whole class of defect these assertions
exist to close.

**AND THE TEST THAT PINS THE LITERAL MOVED IN THE SAME ACT, because it is part
of the same precondition.** `tests/openxwallet_consumer_gate/test_gate_invocation.py`
asserts the workflow's own string, so a flip to `8 of 8` in the YAML alone turns
the REQUIRED `pytest-suite` check red — the identical failure mode §0.1.4 exists
to prevent, one file over. **Measured, not anticipated:** on the flipped tree
before the test moved,
`test_the_four_per_seat_keys_are_asserted_as_adjudicated` FAILED with *"the gate
does not assert that the four per-seat council signing keys were adjudicated"*.
Two edits close it, in the workflow's own discipline:

* the test is renamed to `test_the_eight_per_seat_keys_are_asserted_as_adjudicated`
  and its literal moved `4 of 4` → `8 of 8`, with the arithmetic (four plus
  four) and the reason for the move written into its docstring;
* a NEW sibling, `test_the_second_bodys_wallet_is_asserted_separately`, holds the
  grc wallet's grep in place — **a second test rather than a widened one**, for
  the same reason the workflow gained a second grep rather than a widened one.

`pytest-suite`'s `MIN_SELECTED` / `MIN_PASSED` are FLOORS and rise; its
`EXPECT_SKIPPED: 21` is exact and does not move, because the added test does not
skip.

**WHY IT LANDS HERE AND NOT WITH 2.7, AND THE TEXT THAT DISAGREES.** Three texts
speak to this. `tasks.md` §2.8's body says *"IN THE SAME PULL REQUEST as 2.7"*;
the 2026-09-07 coordinator disposition beneath it defers the flip to *"the
register act (§ 3.6/3.7)"*; `proposal.md`'s AMENDMENT says the flip is
*"performed in the SAME act"* as Brett's walk. **The amendment is newest and
governs.** The reason is arithmetic rather than preference: on a ONE-row
register the widened reader still emits `4 of 4`, so flipping the literal with
2.7 would have turned the REQUIRED check red on a human-only surface for as long
as the register stayed at one row. **§2.8's own body sentence was never edited
and is stale**; it is named here rather than silently overwritten.

---

## 5. Step 5 — the gate, run locally

Run from the worktree root with `set -o pipefail` — the `tee` pipeline masks a
validator's exit code without it, which is Copilot's open observation on PR #717
and is honoured here rather than left as a note.

```
python3 scripts/verify-openxwallet-pin.py
python3 openXwallet/scripts/wallet-yaml-syntax-gate.py .
python3 openXwallet/scripts/validate-openxwallet.py . | tee wallet-gate.log
```

**BEFORE — the baseline, taken at `origin/main` `6a09a2d4` BEFORE any file in
this act was edited**, so the after-state can be attributed to the act rather
than to the reader:

```
OK openxwallet-pin verified: openXwallet@f3eb929b… (tag label wallet-v1.5), 8 digest(s) recomputed
note  wallet 'wal-agent-mrc-0001': 5 declared key(s) adjudicated (…)
note  intake register read: governance/review-authority/register.yaml (1 row(s))
note  intake register: 4 of 4 per-seat signing key(s) adjudicated and resolved
note  repo scan: 7 openxWallet artifact(s) validated, 2119 document(s) skipped as another kind

validate-openxwallet: 0 error(s), 0 warning(s)
```

**THE SHAPE PROBE, run on the PLACEHOLDER tree before the values existed.**
This is the mint runbook's precondition 1 — *"Run the probe in §5 FIRST"* —
discharged by measurement rather than by argument, and it is recorded because
it isolates the one thing that could still have refused this act. The reader
emitted:

```
note  wallet 'wal-agent-grc-0001': 5 declared key(s) adjudicated (key-grc-0001, key-grc-seat-company-policy-lead-0001, key-grc-seat-lead-architect-0001, key-grc-seat-lead-quality-0001, key-grc-seat-lead-security-0001)
note  intake register read: governance/review-authority/register.yaml (2 row(s))
note  intake register: 4 of 8 per-seat signing key(s) adjudicated and resolved
```

**`2 row(s)` — no `register-minimal-shape-exceeded`.** **EIGHT seat entries
counted, and no `register-seat-duplicate`**, though `lead-security`,
`lead-quality` and `company-policy-lead` each appear twice in the file. **The
new wallet's five declared keys adjudicated**, in exactly the form §4.5's new
gate assertion greps for. **Both defects design D5 measured at `wallet-v1.4`
are gone**, on this act's own tree rather than on a fixture.

The run was RED, and every one of its 35 errors is a PLACEHOLDER SHAPE and
nothing else: 21 `[schema]`, 4 `[register-seat-key-malformed]`, 4
`[register-seat-fingerprint-malformed]`, 4
`[declared-key-fingerprint-mismatch]`, 1 `[attestation-malformed]`
(`verified_at is not an RFC3339 timestamp`) and the one
`[register-tier-act-unattested]` that follows from it — the attestation being
unparseable is exactly what drops the row to the unattested cap, which is the
control working. **No structural finding.** No stand-in value was substituted
to make the gate green; the runbook's rule holds — if the reader refuses a
shape you believe is correct, the refusal is evidence, not an obstacle.

**AFTER — the post-fill run, 2026-09-08, on this branch at base
`6a09a2d4`.** The branch was deliberately NOT merged forward from `origin/main`
before this run, so the only difference between the two logs is this act:

```
note  approval-scope vocabulary read from contracts/schemas/hermes-job-envelope.schema.yaml: ['authority_agents_may_approve', 'hermes_approval_required_before_apply', 'human_escalation_required_for']
note  wallet 'wal-agent-council-0011': 4 declared key(s) adjudicated (key-council-primary-0011, key-council-retired-0011, key-council-seat-a-0011, key-council-seat-b-0011)
note  corpus: 21 positive example(s), 45 negative confirmation(s) across 13/13 requirements
note  nested repositories pruned (not adjudicated): openXwallet
note  wallet 'wal-agent-grc-0001': 5 declared key(s) adjudicated (key-grc-0001, key-grc-seat-company-policy-lead-0001, key-grc-seat-lead-architect-0001, key-grc-seat-lead-quality-0001, key-grc-seat-lead-security-0001)
note  wallet 'wal-agent-mrc-0001': 5 declared key(s) adjudicated (key-mrc-0001, key-seat-company-policy-lead-0001, key-seat-lead-integration-0001, key-seat-lead-quality-0001, key-seat-lead-security-0001)
note  intake register read: governance/review-authority/register.yaml (2 row(s))
note  intake register: 8 of 8 per-seat signing key(s) adjudicated and resolved
note  repo scan: 9 openxWallet artifact(s) validated, 2120 document(s) skipped as another kind

validate-openxwallet: 0 error(s), 0 warning(s)
```

**THE FOUR THINGS THE RUNBOOK SAYS TO READ IN THE LOG, read:**

| What the runbook requires | Before (`6a09a2d4`) | After (this act) |
|---|---|---|
| `intake register read: … (n row(s))` | **`1 row(s)`** | **`2 row(s)`** |
| `intake register: n of n per-seat signing key(s) adjudicated and resolved` | **`4 of 4`** | **`8 of 8`** |
| `wallet 'wal-agent-grc-0001': 5 declared key(s) adjudicated` | **absent** — no such wallet | **present**, naming all five ids |
| any `[register-*]` finding | none | **none** (`grep -c '\[register-' wallet-gate.log` = **0**) |
| `repo scan: n … validated` | `7 artifact(s), 2119 document(s) skipped` | `9 artifact(s), 2120 document(s) skipped` — **+2 artifacts** (the wallet and the grant) and **+1 skipped document** (the kindless attestation, skipped by `repo_scan` exactly as §4.2 requires) |

**The other gates, all rc 0 on the same tree:**

```
verify-openxwallet-pin.py     OK openxwallet-pin verified: openXwallet@f3eb929b… (tag label wallet-v1.5),
                                 gitlink read from HEAD, 8 digest(s) recomputed          rc=0
wallet-yaml-syntax-gate.py .                                                             rc=0
validate-openxwallet.py . --strict     0 error(s), 0 warning(s)                          rc=0
validate-factory-identity.py .         factory-identity register read: … (1 row(s))
                                       1 active origin row(s) over 1 originating repository(ies)
                                       disjointness holds against governance/review-authority/
                                         (4 identifier(s) here, 46 identifier(s) there, 0 shared)
                                       0 error(s)                                        rc=0
```

**THE DISJOINTNESS NUMBER MOVED AND THAT IS THE POINT.** `46 identifier(s)
there` counts the review-authority side after this act's five new keys landed;
**`0 shared`** is the assertion — no key of this mint appears in
`governance/factory-identity/`, which is where a mint that reused the factory
origin key would show up.

**OpenSpec, through the CLI THIS REPOSITORY PINS** (`contracts/openspec-cli-pin.yaml`
→ `@fission-ai/openspec@1.12.0`, content address verified before invocation):

```
validate-openspec-cli-pin.py --change register-gate-rules-council-seats --strict --no-cache
    Totals: 1 passed, 0 failed (1 items)                                                 rc=0
validate-openspec-cli-pin.py --all --no-cache          (the invocation the REQUIRED
                                                        openspec-cli-pin job makes)
    97 passed, 2 failed (99 items); both failures are PRE-EXISTING DISPOSITIONED
    findings on `add-chain-attestation` and `add-composed-view-authoring`, accepted
    by Brett Heap 2026-09-05 ("take exit 2"), neither touched by this act          rc=0
```

**A `openspec` BINARY ON `PATH` IS NOT THIS GATE, and the difference is recorded
so nobody mistakes it for one.** The host `openspec` here is **1.2.0**, ten
minor versions behind the pin, and it reports one failure
(`disposition-codexfactory-declared-renames`) that the pinned 1.12.0 does not.
That change directory is **byte-identical between this branch and
`origin/main`** — measured with `git ls-tree` — so the finding is the stale
CLI's, not this act's. The pinned entrypoint is the one the required check runs
and the one this record stands on.

**`pytest-suite`, the other REQUIRED check this act moves:**
`tests/openxwallet_consumer_gate` **17 passed** after the literal and its new
sibling landed (§4.5); the full `pytest tests/ -m "not postgres"` run is recorded
in the pull request.

**READ THE LOG, NOT THE EXIT CODE.** That is the runbook's instruction and it is
not decoration: a green exit with a `1 row(s)` line would mean the act did not
land.

### 5.1 THE CONSUMING GATE'S OWN ASSERTIONS, REPLAYED LOCALLY

**Reading the log by eye is not the same act as the gate reading it.** So every
`grep` in `openxwallet-consumer-gate.yml`'s two assertion steps was extracted
verbatim and run against this tree's `wallet-gate.log` and
`factory-identity-gate.log`. **13 of 13 pass**, including the three this act
moved:

| Line | Assertion | Result |
|---|---|---|
| `:130` | `^note  repo scan: [0-9]+ openxWallet artifact` | **PASS** |
| `:132` | `^note  intake register read: …register\.yaml \([0-9]+ row\(s\)\)$` | **PASS** |
| `:134` | NOT `no intake register at this tree` | **PASS** |
| `:136` | NOT `\[register-[a-z-]+\]` | **PASS** |
| `:161` | `^note  intake register: 8 of 8 per-seat signing key\(s\) adjudicated and resolved$` | **PASS** — **the flipped literal** |
| `:163` | NOT `no per-seat signing key is recorded` | **PASS** |
| `:184` | `^note  wallet 'wal-agent-mrc-0001': 5 declared key\(s\) adjudicated ` | **PASS** |
| `:193` | `^note  wallet 'wal-agent-grc-0001': 5 declared key\(s\) adjudicated ` | **PASS** — **the new assertion** |
| `:196` | the conjunction echo's alternation | **PASS** — surfaces **5** lines, both wallets among them |
| `:236` | `^note  factory-identity register read: …\([0-9]+ row\(s\)\)$` | **PASS** |
| `:238` | `^note  factory-identity register: 1 active origin row\(s\) over 1 originating repository\(ies\)$` | **PASS** |
| `:240` | `^note  factory-identity: disjointness holds … 0 shared\)$` | **PASS** |
| `:242` | NOT `\[factory-identity-[a-z-]+\]` | **PASS** |

The `:196` echo, which exists so a human reading the CI log sees the conjunction
rather than inferring it, now prints both wallets:

```
note  wallet 'wal-agent-grc-0001': 5 declared key(s) adjudicated (key-grc-0001, key-grc-seat-company-policy-lead-0001, key-grc-seat-lead-architect-0001, key-grc-seat-lead-quality-0001, key-grc-seat-lead-security-0001)
note  wallet 'wal-agent-mrc-0001': 5 declared key(s) adjudicated (key-mrc-0001, key-seat-company-policy-lead-0001, key-seat-lead-integration-0001, key-seat-lead-quality-0001, key-seat-lead-security-0001)
note  intake register read: governance/review-authority/register.yaml (2 row(s))
note  intake register: 8 of 8 per-seat signing key(s) adjudicated and resolved
note  repo scan: 9 openxWallet artifact(s) validated, 2120 document(s) skipped as another kind
```

**NEITHER LOG IS COMMITTED.** The 2026-09-02 precedent committed no gate log
either — `git log --diff-filter=A -- '*wallet-gate.log'` is empty across every
branch — and the reason holds here: a log is a transcript of one run on one
tree, and committing it invites a later reader to trust the transcript instead
of re-running the gate. The excerpts above are cited; the artifact is
regenerated by anyone who wants it, with the three commands at the head of this
section.

---

## 6. CAPACITY DISCLOSURE (mint runbook §0.3)

**Brett Heap holds several capacities in this act, and they are disclosed
rather than collapsed** — the same discipline the 2026-09-02 walk applied, for
the same reason.

| Capacity | The act held in it | Where it was exercised |
|---|---|---|
| **the RATIFYING HUMAN** | ratifying `register-gate-rules-council-seats` and ruling Q-GRC-1..Q-GRC-5 | `review/ratification-2026-09-06.md`, 2026-09-06T14:13:46Z |
| **the OPERATOR** | **minting the five keypairs and provisioning the four private halves** — the only acts in this ceremony no agent may perform | offline; codexFactory environment `worker-credentials`, at `2026-09-08T04:19:00Z` |
| **the CONVENER / roster authority** | **selecting `lead-architect`'s pin directly (R1)**, with NO seat convened | codexFactory `records/2026-09-07-gate-rules-roster-lead-architect-pin.md` §2 |
| **the COORDINATOR** — the Fable session, **not** the ratifying human | sequencing the act and carrying the merge on the ratifier's word | this pull request |
| **the AUTHORING AGENT** — an Opus subagent, directed by the coordinator | **COMPOSING THE BYTES** of the wallet, attestation, grant, register comments, the gate edit and this walk | this change |

**THE LAST TWO ARE MACHINE-HELD AND ARE DISCLOSED FOR THE SAME REASON THE FIRST
THREE ARE. The ratifying human did not type the register.** An agent composed
the bytes on the ratifier's word; a coordinating session carries the merge.
Neither is an authority. But a capacity table listing only the human's three
would let a reader assume the writing was his too. **What is Brett Heap's here
is THE ACT** — the ratification, the five rulings, R1's selection, the keys
themselves, the private halves, and the decision to commission this body. **What
is not his is the typing and the button.**

**AND ONE CAPACITY WAS DELIBERATELY NOT EXERCISED, which matters more here than
in the predecessor act.** R1's pin was a **DIRECT OPERATOR SELECTION** — the
roster-change record says so in its own header: *"NO SEAT WAS RUN, AND NO
COUNCIL SELECTED THIS PIN."* One seat return exists (`lead-quality`, at its own
pin), and it is an **ACCEPT AS AMENDED**, not a selection.

**THE DISCLOSED, UNCURED CONFLICT TRAVELS WITH THE ACCEPTANCE.** LQ-C3, in the
accepting seat's own words:

> **LQ-C3 (my own conflict, disclosed and not cured).** My own seat's pin
> (`claude-sonnet-5`) sits in the block this return accepts. I have confined my
> findings to `lead-architect`'s row and to the mechanics of the roster as a
> whole; I offer no capability judgment about my own seat drawn from my own
> performance, and this return should not be read as such.

**No cure was attempted and none is attempted here.** A cure would manufacture a
procedure no sitting chartered. This record cites Lead Quality's acceptance with
the conflict attached rather than citing a clean acceptance.

**Why this is disclosed and not treated as an irregularity.** It is the estate's
standing condition — one operator, one code owner — and the honest form is to
say so beside the act rather than to let each capacity read as a separate check
on the others. **Several capacities held by one human are one check, not
several.**

---

## 7. THE PROJECTION — NOT PERFORMED BY THIS CEREMONY, and exactly what it takes

**THE REGISTER ACT DOES NOT REACH THE RUNTIME.** The Hermes runtime does not
read `governance/review-authority/register.yaml`; it reads an operator-
established **PROJECTION** of it. This act moves the register and moves nothing
else.

**UNTIL THE PROJECTION IS RE-DERIVED, THE RUNTIME KEEPS REFUSING WITH
`review_authority.root_key_mismatch`, AND NO AUTHORITY FLOWS.**

**WHAT IT TAKES, NAMED** (task 4.1; sequencing step 5): either the next
`hermes-register-projection-refresher` CronJob tick after this act merges, or a
manual `project-register` run against the merged revision. Nothing else — no
heredoc, no hand-built document.

**WHO OWNS IT:** the operator, against `opensoft/xFactory-Hermes-Install`. **It
is not this change's to perform and not this change's to tick** (task 5.2 puts
§4 explicitly OUT of the archive gate).

**THE VISIBLE SIGNAL THAT IT HAPPENED:** `seat_count` **4 → 8**, and `councils`
gaining `gate_rules_council`. **Nothing in hermes-install needs a code change**
— `derive_projection` already keys on `(council_id, seat_id)` and already
reports `councils` as a set.

**AND ONE THING NO OPENXFACTORY TASK NAMES, recorded here so it is a known gap
rather than a surprise:** hermes-install asserts the expected seat count in its
own test suite (`tests/unit/test_project_register.py`, `== 4`), and prior deploy
evidence records `seat_count 4`. **That assertion becomes `8` when the
projection is re-derived**, and it is a hermes-install edit that this change's
task list does not name. It will not go red on its own — it is a literal in
another repository — so nothing announces the divergence.

**`revocation_staleness_bound: P7D` TRAVELS VERBATIM** into
`projected_from.staleness_bound`, and it is **not touched by this act**.

**THE PROJECTION MUST NOT CARRY A FACT THIS REGISTER DOES NOT.** That is why the
two spellings of the council are both recorded (§3) rather than one being
invented at projection time.

**Stopping at §4 is the commonest way to think this ceremony is finished when it
is not.**

---

## 8. THE HONEST LIMITS

* **THE RUNBOOK DOES NOT ENFORCE ITSELF.** In its own words, and it belongs on
  every walk record it produces: *"It does not enforce itself. No gate in this
  estate refuses a register act that skips this document."* Flipping it to
  `Status: ratified` in this same act (task 1.6) changes **nothing** about that.
* **NO GATE-RULES CONVENING HAS EVER RUN, and the seats are therefore
  REGISTERED AND UNEXERCISED.** Measured: codexFactory workflow
  `gate-rules-convening.yml`, id **352457764**, **`total_count: 0`**. This is
  the strength at which the claim is made — not "rarely", not "not recently":
  **never, zero runs.** A vacuous non-exercise is recorded as a vacuous
  non-exercise and never as a pass. **Per Brett Heap's B2 ruling
  (2026-09-08T03:20:24Z, §4.2), the holder execution context is attested as
  EXISTING and NEVER RUN — named and owed rather than observed — not as an
  owed job that does not yet exist.**
* **PROVISIONING THE SECRETS LIFTS A REFUSAL AND PRODUCES NO SIGNATURE.** The
  caller's wiring is PRESENCE-ONLY (§4.2 limb 4). The FIRST SIGNED gate-rules
  convening is sequencing step 6, task 4.5, and it is **not this change's to
  perform**.
* **LQ-C1 — NO ADEQUACY CLAIM IS MADE OR MAY BE READ.** In the accepting seat's
  own words: *"Nothing beyond the pin itself is claimed for `lead-architect` …
  Before any first-signed convening's output is cited as evidence that
  `lead-architect`'s pin is adequate for its charge … a soak must be recorded at
  this exact identifier with the served-model read-back … Until then, the pin
  stands on the operator's judgment alone, and no later reader may cite this
  acceptance for more than that."* **No soak has run at `claude-opus-5` for
  `lead-architect`.** This walk registers keys; it certifies no bench.
* **LQ-C2 — REGISTERING KEYS DISCHARGES NO GATE.** *"This acceptance does not
  discharge `seat_diversity_disposed_on_soak_evidence`, `advisory_soak_recorded`,
  or any activation-gate entry of the enrolled surface … and it does not certify
  `lead-architect`'s role-fit by measurement."* Nor does this act.
* **LQ-C3 — THE CONFLICT IS CARRIED, NOT CURED** (§6, quoted in full there).
* **LQ-C4 — THE OPEN QUESTION IS NAMED AND LEFT OPEN.** *"Whether a
  packet-only lead-architect seat can meet its own charge — 'whether the vehicle
  chosen can express what the rule claims' — without running anything is
  untested by this acceptance and is not this act's to settle. It belongs with
  the first signed convening's own review, not with a roster pin."* **This act
  does not settle it either**, and no sentence in this record should be read as
  asserting that this body can discharge its charge from a packet alone.
* **LQ-A1 — AND THIS RECORD REPORTS NO SOAK ROW AT ALL.** LQ-A1 asks that
  wherever a gate-rules soak row is first reported, the scoping distinction (the
  cited `soak_gate` YAML entry lives on the ENROLLED surface's rule and is
  carried to this body by PRINCIPLE, not by direct execution) appear in that
  record's opening sentence. **This walk reports no soak row**, so the cleanest
  discharge is to say so plainly: **no gate-rules soak has been run, none is
  reported here, and this act neither performs nor stands in for one.**
* **THE GRC SECRET NAMES ARE IN NO GOVERNED OPENXFACTORY DOCUMENT.** They exist
  in codexFactory's caller and its test, and nowhere in this repository's
  governance. The mint runbook — the document this ceremony walked — **names no
  secret at all** and does not say how a second council's secret names avoid the
  first's. That is a real gap in a `Status: ratified` runbook, it is named here
  rather than quietly patched inside a mint, and its home is a dated runbook
  revision.
* **`root_key_env_var()` IS NOT COUNCIL-AWARE.** codexFactory's
  `council_seat_signing.py` derives a secret name from a seat id alone, so it
  cannot resolve a GRC seat's secret. The caller declares the namespaced names
  itself. Whether the signer needs a council-aware variant, or the caller
  re-exports, is **not stated anywhere this walk could find**, and it will be a
  live question at the first signed convening rather than at this act.
* **THE ACT IS HUMAN-LANDED BY CONSTRUCTION, and that is not a courtesy.**
  `register.yaml` declares on its own face that it is a *"PERMANENTLY HUMAN-ONLY
  SURFACE … no council verdict may ever produce an autonomous approval of a
  change to THIS file"*, and *"a council whose own commission is recorded here is
  never eligible to clear a candidate that edits it."* **This act commissions
  the body that SETS the gate rules and adds three files conferring its own
  authority.** There is no council verdict to obtain here, and obtaining one
  would be the violation.
* **THE FLOOR DOES NOT YET REACH THE THREE FILES THIS ACT ADDS.** codexFactory's
  `scripts/merge_master/openxfactory-review-authority-floor.yaml` names
  `register.yaml` but **not**
  `governance/review-authority/{grants,wallets,attestations}/`, and this act adds
  three files there — one of them the grant conferring the rule-setting body's
  own authority. **This change WIDENS a pre-existing gap and does not close it**
  (design D6, task 4.3); the owner is the arc owner of
  `add-wallet-carried-review-authority`. Recorded so it is owed to a named place
  rather than remembered.
* **THE PROGRAM THAT MINTED THESE KEYS IS IN NO REPOSITORY.** It is a
  lane-authored, host-side program at
  `~/session-prompts/mint-grc-council-seats/tools/mint-grc-council-seats.py`,
  mirroring openxFactory's own `scripts/mint-factory-origin-key.py` in form
  (§3B.1). **It is therefore not reviewable through this pull request**, and
  nothing here asks a reviewer to take its behaviour on trust: what it did is
  evidenced by the command log's argv lines, by `values.json` carrying only
  public values, and by the pinned reader independently re-deriving every one of
  those values on this tree. Whether such a program should live in a repository
  is a real question and it is not this act's to settle.
* **THE ROOT SEED WAS ON A SCREEN FOR EIGHT HOURS AND TEN MINUTES**
  (`04:19:00Z` → `12:29:23Z`, §3B.3). It is stated because it is what happened.
  **No rule in this estate bounds that window and no gate measured it**, so this
  record neither claims the window was safe nor asserts it was not — it declines
  to characterise a fact no control governs.
* **THE FILES ARE CONSISTENT; THE LANE IS UNPROVEN.** That is the honest state,
  and it is the same sentence the predecessor walk ended on.

---

## 9. Ledger movement this walk supports

**None by itself.** A walk ticks no task by itself.

* **§3.2–§3.9** tick on the operator's values landing and the gate reading
  `2 row(s)` / `8 of 8` — not on this document existing.
* **§2.8** is discharged by §4.5 of this act — **in the workflow AND in the test
  that pins the workflow's literal**, which is one precondition and not two —
  and the stale sentence in its own body is named rather than edited (§4.5).
* **§1.6** and **§3.1** are ticked in this act as bookkeeping, with §3.1's tick
  citing codexFactory PR #277 → `511d95c5` rather than restating the row as
  pending.
* **§4.1–§4.6 STAY OPEN**, and task 5.2 puts them explicitly out of the archive
  gate. Holding this change open on a convening nobody can yet run would park
  the register act indefinitely; ticking them from here would tick another
  repository's boxes.
* **§5.3** — before archive, the seat list is re-read against codexFactory
  `gate-rules.yaml` at the then-current `origin/main`. A roster that moved
  between this act and archive means the registered set is stale, and a stale
  seat set records authority no convening presents.
