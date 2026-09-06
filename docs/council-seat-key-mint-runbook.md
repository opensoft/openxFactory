# Council Seat Signing Keys — Mint and Register Act (operator runbook)

Status: draft
Kind: runbook
Repository context: openxFactory
Backed by: `openspec/changes/register-gate-rules-council-seats/tasks.md` §3,
  written against the 2026-08-28 merge-readiness seat-key mint (codexFactory
  `hermes/domain/review-councils/records/2026-08-28-seat-signing-keys-minted.md`,
  merged `78b8fa2`) and the register-act form of
  [`walk-2026-09-02-register-act.md`](../openspec/changes/add-wallet-carried-review-authority/walk-2026-09-02-register-act.md)

**Why this document is `draft` and not `ratified`.** It is authored by a
PROPOSAL. `register-gate-rules-council-seats` is unratified as this is written,
and a runbook that ratifies itself would be the same defect the estate has
already named twice: a described control treated as an existing one. It becomes
`Status: ratified` at task 1.6, on the change's ratification, and not before.

**What it is for.** The operator ceremony for commissioning a COUNCIL BODY into
openxFactory's intake register: mint its seat signing keys, declare them in a
wallet, attest their custody, issue one grant, and write one authority row. The
2026-08-28 merge-readiness mint performed exactly this and was recorded but
never written down as a repeatable procedure; the second body is what makes a
procedure worth having.

**Who may run it.** Only the responsible operator.
`governance/review-authority/register.yaml` is a PERMANENTLY HUMAN-ONLY SURFACE
by ratified requirement and a never-clearable floor member by exact path in
codexFactory's gate rules. No agent writes any file in this ceremony, and no
council verdict clears a candidate that carries one.

---

## 0. Before you start

### 0.1 The five preconditions, each of which has refused an act before

1. **The reader can represent what you are about to write.** Run the probe in
   §5 FIRST. `governance/review-authority/register.yaml` has no schema — the
   PINNED reader is its shape, and it has twice refused a correct act it could
   not represent (`wallet-v1.4`; and the two-council defects measured in
   `register-gate-rules-council-seats` design D5). **If the pinned reader
   refuses the shape, stop: the fix is an openXwallet change and a pin advance,
   never a workaround here.**
2. **The body has a DECLARED COMPOSITION** in the domain repository that governs
   its roster, pinned to exact model identifiers. A grant issued against a
   composition that does not exist can never be revoked for drift.
3. **The seats are read from the roster BY IDENTIFIER.** A symbolic slot or a
   persona with no seat identifier is NOT a seat; recording a key for it records
   authority nothing will present.
4. **Every count the consuming gate asserts is LITERAL.** Grep
   `.github/workflows/openxwallet-consumer-gate.yml` for the note counts you are
   about to move and move them in the same act, or the REQUIRED check goes red
   on a human-only surface.
5. **Nothing is green halfway.** The mint, wallet, attestation, grant and row
   are ONE change. There is no ordering in which a partial act passes the
   required check, which is why they are not split into separate pull requests.

### 0.2 What is minted, and what is not

**Minted:** one Ed25519 keypair per SEAT, plus one for the BODY's root identity
if the body has none. Nothing else.

**Not minted, and not this ceremony's to touch:** any existing body's keys, the
factory origin key, any deploy credential, any GitHub App key. If the body
already holds a wallet, you are performing a re-issuance and
[`governed-reissuance-runbook.md`](governed-reissuance-runbook.md) governs
instead of this document.

### 0.3 Who holds which act

| Act | Who |
|---|---|
| Generate the seeds | the operator, offline |
| Store the private halves | the operator — a vault for a root key, the holder's own execution-context secret store for a seat key |
| Write the wallet, attestation, grant, row | the operator, by hand, in one change |
| Ratify the composition pin | the domain repository's governing body |
| Approve the pull request | a human. No council. |

---

## 1. Step 1 — read the roster, and write the seat list down

From the domain repository at `origin/main`, never from a local checkout that
may be stale:

```
git -C <domain-repo> show origin/main:hermes/domain/review-councils/<council>.yaml
```

Write down, in the walk record before you mint anything:

* every seat the council seats BY IDENTIFIER, including conditional seats —
  mint conditional seats WITH the unconditional ones, because a candidate whose
  class seats a conditional seat must not be the convening that discovers a
  missing key;
* every seat you are NOT registering, and why (symbolic binding; a persona with
  no identifier), so the omission is a decision on record and not an oversight;
* the council's `id` exactly as spelled in the roster. The register's
  `council_id` is that spelling VERBATIM — it is carried into the Hermes
  projection, which keys its seat lookup on `(council_id, seat_id)`.

**The two spellings.** `council_ref` is the AUTHORITY ATTACHMENT and must equal
the authorizing row's `holder_ref`; `council_id` is the RUNTIME NAME. The reader
checks that they denote one body: `council_ref == "agent:" +
council_id.replace("_", "-")`. Neither is derivable from the other by any
declared rule, so both are recorded and neither is invented at projection time.

---

## 2. Step 2 — mint, offline

One 32-byte Ed25519 seed per key. Generate them where no CI log, no shell
history file and no agent session can see them.

Derive, for each key, the three public values the register family needs:

* the raw 32-byte public key, as **43 characters of canonical unpadded
  base64url** — this is the register's `public_key`. A 64-hex value is the
  encoding of a PRIVATE SEED and the reader refuses it by shape, in the required
  check, before it can merge;
* `key_fingerprint` = `"sha256:" + sha256(raw 32-byte public key).hexdigest()`.
  The reader RECOMPUTES it from `public_key`, so a transcription slip fails the
  gate rather than entering the register;
* the `did:key` / `public_key_multibase` form for the wallet — `z` plus
  base58btc of the two-byte ed25519 multicodec prefix and the 32 raw bytes.

**Derive these with the PINNED decoders, not with a script of your own.** The
one spelling the mint record, the register reader and the wallet all agree on is
the pinned openXwallet reader's; deriving them twice by two routes is how two
spellings of one key's identity get committed.

### 2.1 Where the private halves go

* **A body's ROOT key** — the operator's vault. It never enters git, CI or an
  agent session, and the wallet carries only its public half.
* **A SEAT key** — the holder's OWN execution context, and nowhere else. For a
  council whose seats run in a CI job, that is that repository's environment
  secret store, one secret per seat, named for the seat. **Every seat has its
  own key**: one seat's compromise must be one seat's problem.
* **If the holder's execution context does not exist yet** — say so in the
  custody attestation, in terms, naming the owed job. Do not describe a context
  you have not seen. An attestation attests that the DECLARED custody model
  matches reality, and "the job is owed" is part of reality.

**Never** paste a private half, a seed or a passphrase into any file under
`governance/`. The reader refuses a seed by shape, but the refusal happens after
it is in a commit.

---

## 3. Step 3 — write the four artifacts, in this order

Order matters: each one resolves against the one before it, and writing the row
first produces a row pointing at nothing.

### 3.1 The wallet — `governance/review-authority/wallets/wal-agent-<body>-0001.yaml`

`kind: xfactory_wallet_record`. The body's root key in `key_reference`; every
seat key in `keys:`, each with its own `custody` block, `key_fingerprint` and
`display_label`. Declare the seat keys HERE and not only in the register: the
reader's rule (r) refuses an exercise record presenting a key no wallet
declares, and the runtime writes the REGISTER-RECORDED `key_id` into
`presenting_key_ref` — so a register-only recording makes the body's first
signed seat return unrepresentable.

The file must sit OUTSIDE any `examples/` path or the scanner stops treating it
as live.

### 3.2 The custody attestation — `governance/review-authority/attestations/custody-attest-wal-agent-<body>-0001.yaml`

Deliberately kindless: it carries no `kind:`, so `repo_scan` skips it and the
register reader consumes it. **Without it the unattested cap applies and the
grant reaches only `request`.** Record WHO verified the custody, AGAINST WHAT,
and WHEN; state the isolation actually claimed (usually `none`) rather than an
assurance; and name the compensating control that lets the declared model reach
tier `act`.

### 3.3 The grant — `governance/review-authority/grants/grant-<body>-0001.yaml`

`kind: xfactory_wallet_grant`, a ROOT grant (no `parent_grant_ref`), `issued_by`
the anchored operator in its email form. Scope: `acts: [review]` (the canonical
token the reader enforces), `objects: [<the one target repository>]`,
`authority_tier: act`, and an `approval_posture` that keeps
approval-before-apply required and forbids authority agents approving — that
posture is the compensating control the tier stands on.

Re-examine every scope element and RECORD WHY IT STANDS. A later reader must be
able to tell a decision from a paste.

### 3.4 The register row — `governance/review-authority/register.yaml`

Exactly the nine fields the reader enforces as an exact set:
`row_id`, `holder_ref`, `wallet_ref`, `target_repo`, `act`, `authority_tier`,
`grant_ref`, `expires_at`, `state`. **`expires_at` must be
character-for-character equal to the grant's, because the reader compares the
two.** Add nothing to the row — there is no key field and no composition field
on a row, and adding one fails the exact set equality.

Then append one `seat_keys` entry per registered seat, each with exactly seven
fields: `seat_id`, `council_ref`, `council_id`, `key_id`, `public_key`,
`key_fingerprint`, `authorizing_row`. `key_id` and `key_fingerprint` are unique
ACROSS THE WHOLE FILE, so namespace the key ids by body.

**Do not touch another body's row, keys, or the file's
`revocation_staleness_bound`.** One bound governs the whole register; tightening
it is its own governed edit and never a tidy-up inside a mint.

---

## 4. Step 4 — move the consuming gate's literals in the same change

`.github/workflows/openxwallet-consumer-gate.yml` asserts the reader's notes
POSITIVELY and with LITERAL counts, on purpose: a green check that proves no
register was opened is a vacuous pass. Your act moves at least:

* `intake register: N of N per-seat signing key(s) adjudicated and resolved`;
* a per-wallet `M declared key(s) adjudicated` line for each multi-key wallet —
  add one for the new wallet, do not widen the existing one.

Keep them literal. A wildcard would let a register that lost a body pass the
positive proof, which is the whole class of defect those assertions exist to
close.

---

## 5. Step 5 — run the gate locally, before you push

```
git submodule update --init openXwallet
python3 scripts/verify-openxwallet-pin.py
python3 openXwallet/scripts/wallet-yaml-syntax-gate.py .
python3 openXwallet/scripts/validate-openxwallet.py . | tee wallet-gate.log
```

Read the LOG, not just the exit code. It must carry:

* `note  repo scan: <n> openxWallet artifact(s) validated` — the sweep ran;
* `note  intake register read: governance/review-authority/register.yaml
  (<rows> row(s))` — with the row count you intended;
* `note  intake register: <k> of <k> per-seat signing key(s) adjudicated and
  resolved` — ADJUDICATED, not parsed; `k of k` is the only acceptable form;
* `note  wallet '<wallet_id>': <m> declared key(s) adjudicated` for the new
  wallet;
* and NO line matching `[register-*]`.

**If the reader refuses a shape you believe is correct, stop and read design D5
of `register-gate-rules-council-seats`.** The refusal is evidence about the
reader; the exits that would make the gate green by narrowing the act are
enumerated there and each is refused.

---

## 6. Step 6 — the walk record

One file, in the change directory, in the form of
[`walk-2026-09-02-register-act.md`](../openspec/changes/add-wallet-carried-review-authority/walk-2026-09-02-register-act.md).
It carries, at minimum:

1. **The headline before the detail** — what was and was not performed.
2. **What each step produced**, with the artifact paths.
3. **The citations the act is fixed at** — the rulings, the roster record, the
   operator identity record — each VERIFIED, not cited from memory.
4. **The rulings as spoken**, verbatim, with their timestamps and URLs.
5. **The projection step, which this ceremony does NOT perform** — say what it
   takes, name the owner, and do not imply the register act un-parked anything.
   Stopping at the register act is the commonest way to think the work is
   finished when it is not.
6. **The honest limits.** If no convening of this body has ever run, say so at
   the strength it was measured. A vacuous non-exercise is recorded as a vacuous
   non-exercise and never as a pass.

---

## What this runbook deliberately does not do

* **It does not mint anything.** It is a checklist the operator executes.
* **It does not refresh the Hermes projection.** That is an operator act against
  the cluster, or a scheduled CronJob tick, and it reads the DEFAULT BRANCH — so
  it is invisible to the pull request carrying your act by construction.
* **It does not admit a convening.** The park is lifted when a real convening is
  admitted against the new grant. Until you have seen that, you have evidence
  that the FILES are consistent and no evidence that the LANE recovered.
* **It does not enforce itself.** No gate in this estate refuses a register act
  that skips this document. That sentence belongs on every walk record it
  produces.
