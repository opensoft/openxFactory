# F0 Terminal PASS Report — Supervised Live Sessions, 2026-07-12

Status: record
Kind: report
Repository context: openxFactory
Change: qualify-avatar-brokered-call-feasibility
Candidate: `gpt-realtime-2.1` (voice `marin`, `server_vad`), GA
`POST /v1/realtime/calls` surface
Terminal evidence: [f0-results.json](f0-results.json) ·
[f0-results.md](f0-results.md) ·
[f0-interface-impact.yaml](f0-interface-impact.yaml)
Harness source commit: `5142065b2833a2b6d2ccbcb460bf164fd4e1e417`
(embedded in the results record; the F0 gate matches it against the pinned
`f0_source_commit`).

This report is the human-readable arc of the three supervised live rounds
that produced the terminal `PASS`. It contains only bounded observations
(hashes, reason codes, millisecond offsets, close/HTTP codes); no SDP,
credential, raw call id, transcript, or media was captured at any point.
Companion round records: [f0-live-run-notes-2026-07-12.md](f0-live-run-notes-2026-07-12.md)
(round 1) and
[f0d-revocation-rerun-notes-2026-07-12.md](f0d-revocation-rerun-notes-2026-07-12.md)
(round 2, ACR-005 disposition packet).

## Terminal result

| Dimension | Result |
| --- | --- |
| Overall | **PASS** |
| Trials | 70/70 — every group `completed == planned == passed`, zero failed |
| Mandatory assertions | All PASS, including the four F0-D revocation assertions and both cross-cutting drill assertions |
| Redaction scan | PASS, 0 prohibited findings |
| Interface variances | None (`variances: []`) — every exercised API shape conformed |
| First playable output after authorization | p50 604 ms · p95 643 ms (n=40) |
| Sideband ready | p50 772 ms · p95 1642 ms (n=30) |
| Client media-leg stop after revocation request | 2–3 ms (positive drain-end confirmation) |
| Provider hangup acceptance | ~250 ms |

## The three rounds

**Round 1 — first full matrix: honest INCONCLUSIVE.** 40/40 handshake
assertions passed across F0-A/B/C/E/F, proving the core feasibility claim
(create → hold under sideband + control authorization → release media only on
authorization). Two passive-observability findings blocked PASS:

1. *No unsolicited sideband greeting.* The GA `?call_id=` WSS attach never
   sends a first server event; it answers a client `session.update` in ~80 ms
   even while the answer SDP is held. Fixed by making `verify()` an active
   probe (commit `4680718`).
2. *No passive media-terminal signal after hangup* — all F0-D trials
   `no observable terminal signal within bound`.

**Round 2 — F0-D diagnosis: the teardown, measured.** With an active terminal
probe plus out-of-band REST confirmation (commit `48493b3`), the provider's
post-hangup behavior was measured (3 instrumented calls + 20 slice trials,
fully consistent): hangup accepted (200) → socket drops with abnormal close
`1006` at ~2.2 s (no clean close, no error frame) → earliest authoritative
"call gone" (REST 404) settles ~8.1 s post-hangup (a REST re-hangup fired at
the close blocks ~5.9 s; a WSS re-attach 404s at ~6 s; on a live call the
re-hangup returns 200). F0-D honestly classified
`FAIL: termination confirmed but exceeded the 5s bound` — deliberately not
tuned to green. **Ruling (kernel owner, ACR-005, ratified 2026-07-12):
revocation is client-enforced** — the ≤5 s guarantee is the client-side media
stop plus the accepted revocation request; provider-side settle is recorded
informationally, not gated
(`change/clarify-avatar-revocation-client-enforced`).

**Round 3 — confirming slice + full matrix: PASS.** Under the redefined F0-D
(commits `e2ae1cd`…`5142065`), the one question only live execution could
settle was settled: real `pc.close()` ends the inbound receive drain within
2–3 ms of the revocation request — positive confirmation, no teardown-flush
false negatives, on all 10 slice trials and all 10 matrix trials, each also
recording the informational `provider settle=terminated`. The full 70-trial
matrix then passed everything. **No mechanism change was needed on the live
run.**

## Empirical provider profile (for the variance/disposition record)

- The `?call_id=` control channel is duplex but silent: it emits no
  unsolicited events in any state; active probes are answered in ~80 ms.
- Post-hangup teardown: abnormal close `1006` at ~2.2 s; REST "call gone"
  (404) settles at ~8.1 s; no positive termination confirmation exists inside
  5 s. This is why ACR-005's client-enforced reading is load-bearing for this
  provider profile.
- `POST /v1/realtime/calls` create (multipart `sdp` + `session`, answer SDP
  body, `Location` call id), WSS attach via `?call_id=`, and
  `POST …/hangup` (200 live / 404 gone) all conformed to the implemented GA
  surface — hence the empty variance record.

## Cost and safety

~183 short billed calls across the three rounds (76 + 25 + 82) on the
dedicated, spend-capped lab project (`openxfactory-realtime-f0-lab`),
generated audio only, tools disabled, no tenant data, per
[the credential SOP](../../../../docs/sops/openai-realtime-f0-lab-credential.md).
The key was loaded from the mode-600 local binding and never printed, logged,
or committed.

## Gate handoff

The three evidence files above are the F0 publication-gate inputs. Remaining
steps belong to the AVC contract-kernel owner: merge
`fix/f0d-active-terminal-probe`, set the `f0_evidence_pin` (status `ready`,
pinned `f0_source_commit` + schema digests) in `interface-lock.yaml`, and run
`scripts/validate-avatar-client.py` with the F0 gate active to permit the
`contract-v1.7` tag.

A PASS unblocks contract-kernel publication only. It is not provider
qualification and never enables production or live media — that boundary is
owned by `qualify-avatar-live-voice`.
