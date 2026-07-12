# F0-D Revocation Re-Run — Confirm the Active Terminal Probe

This runbook covers the supervised live re-run of the **F0-D revocation slice** to confirm
(and, if needed, tune) the active control-channel terminal probe against the real provider.
It is the last gap to a green F0. Read `RUN.md` first for the general live-run setup; this
doc only covers what is specific to F0-D.

> **F0-D is safety-critical.** It proves the harness can actually KILL a live call within a
> 5 s bound. Do **not** game it to green. Only tune the probe to match *observed* provider
> behavior, and keep the conservative posture (exact-code match, clean-close-only,
> `alive → FAIL`, ambiguous → `INCONCLUSIVE`). A false PASS on F0-D is the worst possible
> outcome.

## Why a re-run

The first live run was an honest `INCONCLUSIVE`: feasibility was proven (40/40 handshake
assertions across F0-A/B/C/E/F), but F0-D could not observe termination — passive WebRTC
teardown is not visible within 5 s (the provider emits no prompt terminal signal; aiortc's
ICE-consent teardown is ~30 s). This branch (`fix/f0d-active-terminal-probe`) replaces the
passive wait with an **active control-channel probe after hangup**
(`WssSideband.probe_terminated`).

Two things only the live provider can resolve — both conservative (they can only cause a
false `INCONCLUSIVE`, never a false `PASS`):

1. Does the provider **cleanly close** the `?call_id=` control socket (code `1000/1001`) on
   hangup? → clean PASS.
2. If it **errors** instead, what is the exact call-gone error code? → add it to
   `TERMINATION_ERROR_CODES`.

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
the F0-D group counts and the per-trial notes.

### 3. Interpret and act

- **F0-D PASS (all 10)** → the probe works. Go to step 4.
- **F0-D FAIL** (`revocation failed: call still live after hangup`) → the provider did NOT
  terminate the call within 5 s. That is a real feasibility finding, **not** a probe bug —
  do not tune around it. Capture and report to Brett + the kernel owner.
- **F0-D INCONCLUSIVE** (`no conclusive termination signal within bound`) → the probe could
  not attribute the provider's post-hangup behavior. **Diagnose:**
  1. Add a **temporary, redaction-safe** diagnostic in `WssSideband.probe_terminated`
     (`src/avatar_f0/sideband.py`) that records ONLY: each drained frame's `type`, any error
     frame's `error.code`/`error.type`, and any close code (`exc.code` / `exc.rcvd.code`).
     **Never** log frame content, SDP, tokens, or the key.
  2. Run one trial and observe what the control socket actually does after hangup — a clean
     close (which code?), an error (which code?), or silence.
  3. Make the **minimal correct** change:
     - Cleanly closes with `1000/1001` → already handled (re-check why it read otherwise;
       if the real teardown is an abnormal close code, confirm that is genuinely the
       termination signal before treating it as terminated).
     - Returns an error → add the **exact** observed code to `TERMINATION_ERROR_CODES`
       (exact match only — never a broad substring).
  4. Keep every safety invariant (exact-code match, clean-close-only, drain loop,
     `alive → FAIL`, ambiguous → `INCONCLUSIVE`). Update the offline unit test
     `tests/offline/test_live_runner_mock.py::test_probe_terminated_drain_loop_polarity` to
     cover the newly-confirmed code. **Remove the temporary diagnostic before committing.**
  5. A change to the probe's classification logic is **ACR-005-affecting** — commit it with
     the empirical basis in the message, note it needs kernel-owner review, and re-run step 2.

### 4. Full matrix + handoff (once F0-D passes)

```bash
.venv/bin/python -m avatar_f0.cli run --live      # full 70-trial matrix for the complete green
```

Confirm `overall == PASS`, `redaction_scan` PASS, and that `f0-results.json` now carries
`source_commit`. Hand the three evidence files to the AVC contract-kernel owner; they run
`scripts/validate-avatar-client.py` with the F0 gate active — it validates the evidence
against the pinned F0 schemas, matches `source_commit` against the pinned `f0_source_commit`,
reads `PASS`, and disposes any variances — to permit the `contract-v1.7` tag.

## Safety (hard stops)

- Dedicated lab project only; never print/log/commit the key; never widen to production.
- Do **not** weaken the probe's safety guard to force a PASS — only tune to what you observe.
- A PASS does **not** qualify the provider for live/production media — that is
  `qualify-avatar-live-voice`.
- Report back: F0-D outcome, the observed post-hangup control-channel behavior (close/error
  code), any probe change made, and total call spend. Never include the key or SDP.
