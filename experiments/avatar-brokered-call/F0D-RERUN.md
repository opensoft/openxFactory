# F0-D Revocation Re-Run — Confirm Client-Enforced Revocation

This runbook covers the supervised live re-run of the **F0-D revocation slice**. Its purpose
is now to **confirm F0-D PASSes under the ratified client-enforced revocation model** — not to
diagnose or tune the provider's teardown (that was the first re-run; see the record below).
Read `RUN.md` first for the general live-run setup; this doc covers only what is specific to
F0-D.

> **F0-D is safety-critical** — it proves revocation actually works within a 5 s bound. Do
> **not** game it to green. If it FAILs, capture and report; do not weaken the assertion.

## What F0-D now verifies (ACR-005, clarified + ratified 2026-07-12)

Revocation is **client-enforced**. On revoke, within 5 s, F0-D requires BOTH halves, verified
against the real aiortc media leg:

- **(a) client-side stop:** the client closes its own media leg and **no media I/O flows after
  the stop** (`F0-D-TERMINAL_5S` + `F0-D-NO_LATE_IO`);
- **(b) provider request accepted:** the provider revocation request (`hangup`) is accepted
  (200) within 5 s.

The provider-side authoritative termination confirmation MAY lag (measured ~8.1 s on the OpenAI
profile) and is **recorded informationally, not gated**. So F0-D PASSes even though the
provider's server-side settle is slow, as long as (a) and (b) hold in-bound.

## Steps

### 0. Get the code + confirm green offline

```bash
git fetch && git checkout fix/f0d-active-terminal-probe && git pull
cd experiments/avatar-brokered-call
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install -e .
.venv/bin/pytest tests/offline -q          # expect 94 passed; if not, STOP
```

### 1. Load the lab credential

Per `docs/sops/openai-realtime-f0-lab-credential.md` (raw-key file at `~/.ai-keys/openai.key`):

```bash
export OPENAI_API_KEY="$(tr -d '\r\n' < ~/.ai-keys/openai.key)"
[ -n "$OPENAI_API_KEY" ] && echo "key present (len ${#OPENAI_API_KEY})"   # never printenv the value
```

Confirm it is the dedicated lab project with a spend cap set. If unsure, STOP and ask Brett.

### 2. Run the F0-D slice (~10 real calls + the interruption drill)

```bash
.venv/bin/python -m avatar_f0.cli run --live --groups F0-D
```

Read `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/f0-results.json` —
the F0-D group counts and the per-trial notes (each PASS note records the informational
`provider settle=…`).

### 3. Interpret and act

- **F0-D PASS (all 10)** → client-enforced revocation confirmed live. Go to step 4.
- **F0-D FAIL** — read the note:
  - `media I/O continued after the client-side stop` → the client leg did not actually stop
    (a real defect in the client media teardown — report; do not tune around it).
  - `client did not stop its media leg within the 5s bound` → the local `close()` exceeded the
    bound (investigate the aiortc teardown timing on this host).
  - `revocation request not accepted …` → the provider `hangup` did not return 200 in-bound
    (a provider/API finding — capture the status).
- **Note the informational provider settle** in the PASS notes (`provider settle=terminated/
  alive/inconclusive`) for the evidence packet — it does not change the outcome.

One caveat to confirm on this run: the client-stop mechanism (`arm_no_late_io` → `close` →
observation window) is offline-mock-tested; its real timing against a live aiortc peer at
24 kHz / 20 ms frames is validated here. If a **healthy** stop spuriously trips
`media I/O continued after the client-side stop`, widen the arm→close ordering or the
observation window — that is a mechanism-timing fix (commit with the empirical basis; it is
ACR-005-adjacent, so flag for review), NOT a weakening of the assertion.

### 4. Full matrix + handoff (once F0-D passes)

```bash
.venv/bin/python -m avatar_f0.cli run --live      # full 70-trial matrix for the complete green
```

Confirm `overall == PASS`, `redaction_scan` PASS, and that `f0-results.json` carries
`source_commit`. Hand the three evidence files to the AVC contract-kernel owner; they run
`scripts/validate-avatar-client.py` with the F0 gate active — it validates the evidence against
the pinned F0 schemas, matches `source_commit` against the pinned `f0_source_commit`, reads
`PASS`, and disposes any variances — to permit the `contract-v1.7` tag.

## Record — first re-run, 2026-07-12 (disposition RULED)

The first F0-D re-run measured the provider's post-hangup teardown (durable record in
`openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/f0d-revocation-rerun-notes-2026-07-12.md`):

- After an accepted hangup the provider sends NO clean close and NO error frame — it drops the
  `?call_id=` socket with an **abnormal close 1006 at ~2.2 s**; the earliest authoritative
  "call gone" (REST 404) settles at **~8.1 s**. No channel positively confirms termination
  inside 5 s.
- **Ruling (kernel owner, 2026-07-12): client-enforced revocation.** The ≤5 s guarantee is the
  client-side stop + accepted revocation request; provider-side settle is informational. ACR-005
  was clarified (`change/clarify-avatar-revocation-client-enforced`), F0-D redefined to the model
  above, and the F0 change spec/design aligned. The reference runtime already conforms
  (`ARR-005-S05`). This re-run confirms the redefined F0-D PASSes live.

## Safety (hard stops)

- Dedicated lab project only; never print/log/commit the key; never widen to production.
- Do **not** weaken F0-D to force a PASS. A FAIL is a real finding — capture and report.
- A PASS does **not** qualify the provider for live/production media — that is
  `qualify-avatar-live-voice`.
- Report back: F0-D outcome + notes, the informational provider settle, any mechanism-timing
  change made, and total call spend. Never include the key or SDP.
