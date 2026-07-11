# F0 Brokered Realtime Call Spike Protocol

Status: draft
Kind: plan
Captured: 2026-07-10
Originally proposed by: define-avatar-client-runtime
Current owner: qualify-avatar-brokered-call-feasibility
Target capability: avatar-brokered-call-feasibility

F0 is an empirical architecture gate, not provider qualification. It uses a
lab OpenAI project, generated test audio, no tenant data, no external tools,
and no durable transcript or media. A failed or incomplete mandatory assertion
blocks contract publication.

## Fixed Candidate Profile

| Setting | F0 value |
| --- | --- |
| Model | `gpt-realtime-2.1` |
| Voice | `marin`; rejection is an API-shape failure requiring protocol disposition |
| Interaction mode | `provider_vad` |
| OpenAI turn detection | `server_vad` |
| VAD parameters | threshold `0.5`; prefix padding `300 ms`; silence `500 ms`; create response and interrupt response enabled |
| Tools | Empty |
| Transcript retention | Disabled; event type/timing only |
| Readiness timeout | default `3,000 ms`; hard ceiling `5,000 ms` |
| Media | Generated phrase and silence fixture; never a real user recording |

The configuration is based on the official
[WebRTC](https://developers.openai.com/api/docs/guides/realtime-webrtc),
[server-control](https://developers.openai.com/api/docs/guides/realtime-server-controls),
[Server VAD](https://developers.openai.com/api/docs/guides/realtime-vad#server-vad),
and [hangup](https://developers.openai.com/api/docs/guides/realtime-sip#hang-up-the-call)
documentation retrieved on 2026-07-10. The result record must capture the
resolved model snapshot, voice, hashed provider request ID, region if exposed, dependency
versions, network type, and retrieval date.

## Instrumentation

Use a monotonic clock and record, per trial:

- `t_offer_ready`
- `t_provider_create_sent`
- `t_provider_create_accepted`
- `t_sideband_open`
- `t_sideband_verified`
- `t_answer_released`
- `t_lease_ack`
- `t_media_authorized`
- `t_answer_applied`
- `t_first_input_sent`
- `t_first_output_playable`
- `t_hangup_sent`
- `t_peer_terminal`

Persist durations and event types only. Never persist SDP, keys, scoped
credentials, raw audio, transcript text, or arbitrary subject identifiers.

## Trial Matrix

| Group | Count | Procedure | Mandatory assertion |
| --- | ---: | --- | --- |
| F0-A baseline | 20 | Normal create, sideband attach, held answer, lease ack, authorization, generated turn, hangup | `sideband_verified <= answer_released <= lease_ack <= media_authorized <= answer_applied <= first_input_sent`; one provider call per request |
| F0-B delayed sideband | 10 | Inject 1,500-2,500 ms delay before sideband attach | Answer remains server-held; no authorization or media; all calls still ready within 5,000 ms |
| F0-C sideband failure | 10 | Prevent or invalidate sideband attach until timeout | No answer is released; AVC-02 reason is `media_readiness_timeout`; hangup begins within the timeout path |
| F0-D revocation | 10 | Authorize generated media, invalidate fixture consent, invoke hangup | Peer reaches terminal state within 5,000 ms of broker knowledge; no later input/output |
| F0-E exact retry | 10 | Drop first broker response and repeat identical AVC-01 | Same pending provider call and answer; no duplicate billable call |
| F0-F changed retry | 10 | Reuse request ID with one SDP byte changed | AVC-02 `idempotency_conflict`; no old answer and no second provider call |

## Pass And Escalation Rules

F0 is `PASS` only when all conditions hold:

1. Every ordering, no-answer-on-failure, single-call, and redaction assertion
   passes in 100% of its trials.
2. Baseline sideband verification has p95 no greater than 3,000 ms and no trial
   exceeds 5,000 ms from provider create acceptance.
3. First playable output after `media_authorized` has p95 no greater than
   2,000 ms. This is an architecture threshold, not a production SLA.
4. All revocation trials reach peer-terminal state and cease observable
   provider-bound input/output within 5,000 ms.
5. The observed provider request/response shapes can be represented by AVC-01
   and the AVC-02 result union without a provider DTO in neutral fields.
6. Logs, traces, crash output, and the evidence files contain none of the
   prohibited content classes.

Any mandatory assertion failure yields `FAIL`. Environmental inability to run
the complete matrix yields `INCONCLUSIVE`, which also blocks contract
publication but does not block parallel implementation against the provisional
interface baseline.
A latency miss requires an explicit design disposition; averages cannot hide a
p95 or hard-ceiling failure.

## Required Evidence

The spike writes:

- `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/f0-results.json`
- `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/f0-results.md`
- `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/f0-interface-impact.yaml`

The JSON MUST validate against
[`f0-results.schema.yaml`](f0-results.schema.yaml) and contains protocol
version, environment metadata, aggregate counts, p50/p95/max durations, one
redacted row per trial, assertion results, overall
`PASS|FAIL|INCONCLUSIVE`, and SHA-256 of the human-readable report. The Markdown
report records deviations, API-shape corrections, threat-model disposition,
and reviewer decision. Task 3.1 remains incomplete until both result files
exist and validate. Only `PASS` satisfies the sibling kernel publication gate;
`FAIL` and `INCONCLUSIVE` remain valid terminal experiment records.

Current execution state: `INCONCLUSIVE`. The 2026-07-10 review worktree has no
`OPENAI_API_KEY` and no repository `.env`; no live call was attempted and no
result artifacts were fabricated.
