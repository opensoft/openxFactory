# F0 Live Run Notes — 2026-07-12 Supervised Lab Session

Status: record
Kind: report
Repository context: openxFactory
Change: qualify-avatar-brokered-call-feasibility
Run: full 70-trial live matrix + interruption drill against `gpt-realtime-2.1`
(dedicated capped lab project), terminal `INCONCLUSIVE`, redaction scan PASS.
Harness commit at run time: `4680718` (includes the sideband verify fix below).
Companion artifacts: [f0-results.json](f0-results.json),
[f0-results.md](f0-results.md), [f0-interface-impact.yaml](f0-interface-impact.yaml).

This note records the supervised session's empirical observations and their
provenance so the contract-kernel owner can dispose them. It contains only
bounded observations (hashes, reason codes, timings); no SDP, credential, raw
call id, transcript, or media was captured at any point.

## Summary of outcomes

- All 40 handshake-semantics assertions passed across F0-A/B/C/E/F (70/70
  trials completed): create/held-answer ordering, single-provider-call,
  readiness ceiling, no-media-on-failed-verification, readiness timeout, and
  both idempotency invariants.
- The run is terminal `INCONCLUSIVE` solely because all four F0-D assertions
  (`TERMINAL_5S`, `NO_LATE_IO`, `INTERRUPTED`, `BOUNDED_CLEANUP`) recorded no
  passing observations — see Finding 2.
- `f0-interface-impact.yaml` carries `variances: []`: every exercised API
  shape (`POST /v1/realtime/calls` multipart create, answer SDP body,
  `Location` call id, WSS `?call_id=` attach, `POST …/hangup`) conformed to
  the implemented GA surface.

## Finding 1 — no unsolicited sideband greeting (fixed in harness)

The GA `?call_id=` WSS attach never sends an unsolicited server event — no
`session.created` greeting — in either the held-answer or connected state
(observed windows: 10 s held, 2 s held + 8 s connected, zero events, socket
open throughout). The channel is nonetheless live and duplex: a client
`session.update` receives `session.updated` in ~80 ms **while the answer SDP
is still held**.

Impact: T058's original passive `verify()` (await first unsolicited event)
could never verify, so every baseline trial failed sideband verification.
Resolution applied: commit `4680718` changes `WssSideband.verify()` to an
active probe (send benign `session.update`, await reply; an `error` reply or
non-JSON frame fails closed). After the fix the live smoke and all 40
handshake assertions pass. The key empirical claim F0 exists to prove —
sideband verification is possible while the answer is held — is therefore
POSITIVELY confirmed, via active probe rather than passive wait.

Diagnostic provenance: three single-call probes (bounded output only) —
(a) passive watch, held, 10 s → zero events;
(b) passive watch, held 2 s then answer applied, 8 s connected → zero events,
    while first playable media output DID arrive on the WebRTC leg;
(c) duplex probe, held → `session.updated` reply at ~80 ms.

## Finding 2 — no passively observable media-terminal signal within bound

After an authorized answer apply, `POST …/hangup` is accepted (HTTP 200) but
the WebRTC media leg surfaces no terminal transition within the 5000 ms
revocation bound: all 10 F0-D trials recorded
`no observable terminal signal within bound`. The interruption drill then
recorded `INCONCLUSIVE` by its fail-closed design (it cannot confirm terminal
state it cannot observe). This mirrors Finding 1: the provider does not push
the passive teardown signal the harness watches for (aiortc's own
ICE-consent-expiry detection is ~30 s, far beyond the bound).

Not yet tested, likely disposition path: active terminal observability — a
post-hangup sideband probe whose `error` reply or socket close confirms
termination — i.e. the same passive-to-active correction already validated
for Finding 1. Requires a reviewed harness change plus a full matrix re-run
(a partial run cannot PASS).

## Items for the kernel owner

1. Dispose Findings 1–2 against the affected `ACR-*` acceptance criteria
   (acceptance map pinned at `495a816`): decide whether either requires a
   formal variance entry in `f0-interface-impact.yaml` or an acceptance-map
   correction (e.g. any ACR wording that presumes unsolicited provider events
   or passive terminal observability).
2. Approve the F0-D active-terminal-probe harness change; then a full 70-trial
   re-run targets `PASS`.
3. Gate friction to resolve before the validator run: `f0-results.json` does
   not record a harness source commit, while `f0_gate_decision` fails closed
   on `commit_match`. The evidence writer needs to embed the commit (or the
   pin needs an agreed source), else even a PASS bounces off the gate.
4. Runbook/test hygiene observed during the session: RUN.md omits the
   `pip install -e .` the CLI entrypoint requires (pytest works without it via
   `pythonpath`); the live smoke test does not hang up its call on the
   failure path (pre-fix failures relied on provider idle timeout).

## Cost and safety record

~76 short billed calls total (1 failed smoke, 3 diagnostics, 1 passing smoke,
70 matrix trials, 1 drill call) on the dedicated capped lab project. Key
loaded from `~/.ai-keys/openai.key` (mode 600) per the
[credential SOP](../../../../docs/sops/openai-realtime-f0-lab-credential.md);
never printed, logged, or committed. Non-qualification boundary respected: a
future PASS unblocks contract-kernel publication only, never live/production
media (owned by `qualify-avatar-live-voice`).
