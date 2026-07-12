# F0-D Revocation Re-Run Notes — 2026-07-12 Supervised Lab Session

Status: record
Kind: report
Repository context: openxFactory
Change: qualify-avatar-brokered-call-feasibility
Run: F0-D revocation slice (`run --live --groups F0-D`, ~10 trials + 3 instrumented
diagnostic calls) against `gpt-realtime-2.1` on the dedicated capped lab project.
Terminal classification: `FAIL: termination confirmed but exceeded the 5s bound` (10/10),
redaction scan PASS.
Harness commit at run time: `48493b3` (F0-D active terminal probe + out-of-band REST
confirmation). Supersedes the F0-D observation in the first-run note
[f0-live-run-notes-2026-07-12.md](f0-live-run-notes-2026-07-12.md), which recorded the
un-instrumented `INCONCLUSIVE`.
Companion: this note is the durable record for the kernel owner's ACR-005 disposition; a
formal FAIL `f0-results.json` is deliberately NOT committed to the branch (a partial-slice
artifact) pending that disposition. The committed
[f0-results.json](f0-results.json) remains the first full run's `INCONCLUSIVE`.

This note records only bounded observations (timings, close codes, HTTP status). No SDP,
credential, raw call id, transcript, or media was captured at any point.

## Why the re-run

The first full run recorded F0-D `INCONCLUSIVE` ("no observable terminal signal within
bound"): passive WebRTC media teardown is not observable within the 5 s revocation bound
(aiortc's ICE-consent teardown is ~30 s). The branch replaced that with an **active
control-channel probe after hangup**; this session confirmed the provider's post-hangup
behavior and wired an out-of-band confirmation.

## Measured post-hangup teardown (consistent across 3 instrumented calls + 20 slice trials)

- After an **accepted** hangup, the provider sends **no clean close and no error frame** on
  the `?call_id=` control socket. It drops the socket with an **abnormal close 1006** at
  **~2.2 s** (2199 / 2201 / 2227 ms observed).
- A bare 1006 is indistinguishable from a local network blip, so it is **not** treated as
  termination on its own (conservative `_close_verdict`: only a clean 1000/1001 close
  classifies as terminated in-band).
- Out-of-band confirmation = a REST re-hangup `POST /v1/realtime/calls/{id}/hangup`:
  **404 → gone**, **200 → still alive** (and re-kills — acceptable, F0-D's purpose here is to
  kill the call). Fired at the moment of the 1006 close it **blocks ~5.9 s** while teardown
  settles, returning **404 at ~8.1 s post-hangup**. (A WSS re-attach alternative was measured
  and rejected: its 404 also arrives ~6 s post-close.)
- Net: the call **dies at ~2.2 s**, but **no channel positively confirms termination inside
  the 5 s bound**; the earliest authoritative "gone" is ~8.1 s.

## Classification and its basis

The bound is measured from `t_revocation_request` (the kill request) to `t_peer_terminal`
(positive confirmation). The confirmation lands at ~8.1 s > 5 000 ms, so `within = False` →
`FAIL: termination confirmed but exceeded the 5s bound`, 10/10. This is the honest reading of
*this observation channel*; it is not a probe defect.

**Probe design** (harness commit `48493b3`): `probe_terminated` classifies definitive in-band
signals **alone** — a clean 1000/1001 close, a `session.updated` ack, or an exact call-gone
error code — and consults the out-of-band `confirm_gone` **only** for ambiguous signals
(abnormal close, silence, unrecognized error): `gone=True → terminated`, `False → alive`,
`None/raise → inconclusive`.

## Review sign-off

The classification change was adversarially reviewed (false-PASS, probe-correctness,
regression) — **no false-PASS path**: definitive signals provably never consult the confirmer
(offline test asserts the confirmer is not invoked on a clean close or `session.updated`); a
"terminated" via confirmation requires an authoritative REST 404; a live call (200) → FAIL; a
transport failure (None) → INCONCLUSIVE. 94 offline tests pass, including the full
confirmation-matrix polarity tests.

## ACR-005 disposition — RULED 2026-07-12: client-enforced revocation

The finding is not "the harness can't observe termination" — it is **"this provider does not
give a positive, in-bound (≤5 s) termination confirmation"** (abnormal 1006 close ~2.2 s;
authoritative REST 404 ~8.1 s).

**Ruling (kernel owner, 2026-07-12): client-enforced revocation.** The AVC revocation
guarantee is enforced at the client/broker: on revoke, the client stops its **own** media leg
immediately (lease revoke → stop consuming/producing media locally) **and** requests provider
hangup — so no media reaches the user within the bound regardless of the provider's ~8.1 s
server-side settle. ACR-005 is clarified to require *client-side media stop + accepted
provider revocation request within 5 s*, **not** *provider-confirmed termination within 5 s*.
The provider's authoritative server-side settle is best-effort / eventually-consistent and is
recorded as an informational observation, not a gate.

Basis for the ruling: the guarantee already lives where it is enforceable — the reference
runtime (`implement-avatar-reference-runtime`) deterministically revokes the lease and
terminates the attempt within an injected 5 s bound (`ARR-005-S05`; `control.py` `revoke()`,
`consent.py` `REVOCATION_BOUND_TICKS`). F0-D's FAIL under the provider-confirmation reading
therefore does **not** contradict the runtime; it confirms the contract must not delegate the
kill guarantee to provider-side confirmation timing.

Rejected alternatives: (b) death-time bound (~2.2 s) rests on the ambiguous 1006 — a
control-socket blip would false-satisfy the kill guarantee; (c) requiring a provider change
depends on OpenAI.

### Downstream of this ruling (sequenced; governance-first)

1. **Kernel — clarify ACR-005** (OpenSpec change, contract-first): revocation = client-side
   media stop + accepted hangup request within 5 s; provider-side settle is informational.
2. **F0 — redefine F0-D** *(follows ratification)*: PASS iff the provider revocation request
   is accepted in-bound (`hangup` → 200); the provider-side settle verdict/time is recorded
   informationally; the `hangup_to_terminal_ms` gate is retired in favor of a
   request-accepted bound. Do **not** re-stamp `t_peer_terminal` to force a green before the
   kernel clarification lands.
3. **Runtime — no change**: `ARR-005-S05` already models client-enforced revocation.

## Provenance and redaction

All artifacts and this note carry only hashes, bounded reason codes, and monotonic offsets.
Redaction scan PASS on every run; no key, SDP, raw call id, transcript, or media was captured
or written. Total spend for the session: bounded lab calls on the capped project (F0-D slice +
diagnostics), all on the dedicated `openxfactory-realtime-f0-lab` project.
