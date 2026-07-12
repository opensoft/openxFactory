# F0 Brokered-Call Feasibility — Supervised Live Run (T058)

This is the runbook for executing the **live** F0 matrix against the real OpenAI Realtime
API. F0 empirically proves whether a brokered WebRTC call can be created, **held under
sideband + control authorization until media is authorized**, and terminated within bound —
the behaviors no schema or mock can prove.

> **Non-qualification boundary.** A live `PASS` unblocks the AVC **contract-kernel
> publication gate** (after the kernel owner disposes any interface variances). It does
> **not** qualify a provider profile for internal-live or production media — that is owned
> by `qualify-avatar-live-voice`. A run is never a production readiness signal.

---

## 0. What you need

- A **dedicated lab OpenAI project** (not shared/production).
- A **project-scoped API key** for that project, with a **low spend cap** set in the
  OpenAI dashboard. The full matrix is 70 short calls + a handful of smoke/drill calls;
  cost is small, but a cap is the safety net.
- Model access: `gpt-realtime-2.1` (voice `marin`, `server_vad`) available to the project.
- A host with **unrestricted outbound HTTPS *and* UDP/STUN** (WebRTC media). Restricted
  sandboxes / many CI runners block UDP and cannot complete the media leg — run on a real
  workstation or a network that permits WebRTC.

## 1. Credential handling (never in args or tracked files)

The harness reads the key **only** from the `OPENAI_API_KEY` process environment variable
(`credential.py`). It is never accepted via CLI arguments, a tracked `.env`, a config file,
or an evidence file, and is never logged, copied, or committed. Preflight **fails closed**
on a key supplied through any prohibited channel.

The canonical local binding is a **raw-key file** at `~/.ai-keys/openai.key` (one line, just
the key), installed per **`docs/sops/openai-realtime-f0-lab-credential.md`** (§"Install or
Rotate the Local Binding" — hidden input, mode 600). Load it into the environment for one
session:

```bash
test "$(stat -c '%a' ~/.ai-keys/openai.key)" = 600
export OPENAI_API_KEY="$(tr -d '\r\n' < ~/.ai-keys/openai.key)"
[ -n "$OPENAI_API_KEY" ] && echo "key present (length ${#OPENAI_API_KEY})"    # never printenv the value
```

Never `printenv OPENAI_API_KEY`, `cat` the key file, or enable shell tracing while it is
loaded. Verify auth non-disclosingly with the check in the SOP (§"Verify Authentication
Without Disclosure") — it prints only the HTTP result and whether `gpt-realtime-2.1` is
listed. `unset OPENAI_API_KEY` when finished.

## 2. Environment

```bash
cd experiments/avatar-brokered-call
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install -e .        # REQUIRED: installs the avatar_f0 package so
                                            # `python -m avatar_f0.cli` resolves (the pytest
                                            # pythonpath=src does NOT cover the CLI).
```

`aiortc` / `av` / `pylibsrtp` install from binary wheels on common Linux/macOS. If a wheel
is unavailable for your platform, install the native libs first (FFmpeg, Opus, libvpx,
libsrtp2) so the source build can proceed. (Alternatively to `pip install -e .`, prefix the
CLI with `PYTHONPATH=src`.)

## 3. Run it

Three modes, in increasing cost:

```bash
# (a) Offline — no key, no provider call. Terminal INCONCLUSIVE record (SC-013).
.venv/bin/python -m avatar_f0.cli run

# (b) Live smoke — ONE real handshake. Proves the components interoperate + held-answer gate.
.venv/bin/pytest tests/live -m live -v

# (c) Full live matrix — the 70-trial run + interruption/cleanup drill. Writes terminal evidence.
.venv/bin/python -m avatar_f0.cli run --live
```

Notes:
- `--live` is an explicit opt-in. Without it, a run stays offline/INCONCLUSIVE **even when a
  key is present** — the safe default, so no accidental billed run happens.
- `--groups F0-A,F0-D` restricts the matrix; `--readiness-ms N` sets the readiness deadline
  (≤ 5000). Preflight rejects a value above the 5000 ms ceiling.

## 4. Outputs and how to read them

Written directly and atomically under
`openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/`:

| File | What it is |
| --- | --- |
| `f0-results.json` | schema-valid machine record (groups, per-trial rows, metrics, assertions, overall) |
| `f0-results.md` | human summary (status + counts only; no payloads) |
| `f0-interface-impact.yaml` | provider/baseline variances, each citing affected `ACR-*` IDs |

**Overall status**
- `PASS` — every mandatory trial ran and every assertion passed, all timing bounds held,
  redaction clean. Unblocks the kernel gate after variance disposition.
- `FAIL` — a reproduced contrary observation (ordering/timing/retry/cleanup/redaction).
- `INCONCLUSIVE` — a mandatory trial could not run or lacked evidence (e.g. provider API
  shape differs, no key, no observable terminal signal). **Never** silently a PASS.

Evidence carries only **hashes, bounded reason codes, and monotonic offsets** — never SDP,
a credential, a raw call id, transcript, media, or a high-cardinality identifier. A
redaction finding fails the run closed and blocks the write.

## 5. Expect variances on the first real run

The live path is implemented against the GA `POST /v1/realtime/calls` surface (multipart
`sdp` + `session`, answer SDP body, `Location` call id; WSS attach via `?call_id=`; hangup
via `POST …/{call_id}/hangup`). If the provider differs in shape or timing, F0 is designed
to record that as an **interface variance** (→ INCONCLUSIVE, not a fabricated PASS) for the
contract-kernel owner to dispose. That is a normal, expected F0 outcome — not a defect.

## 6. After a PASS

1. Copy the three evidence files into the kernel's F0 pin inputs.
2. The kernel owner runs `scripts/validate-avatar-client.py` with the F0 gate active: it
   validates the evidence against the pinned F0 schemas, checks the source commit + digests,
   reads `PASS` + variance dispositions, and only then permits the `contract-v1.7` tag.
