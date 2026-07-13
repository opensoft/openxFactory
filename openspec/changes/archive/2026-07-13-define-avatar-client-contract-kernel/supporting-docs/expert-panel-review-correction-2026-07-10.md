# Expert Panel Review Correction Record

Status: record
Kind: correction record
Captured: 2026-07-10
Repository context: openxFactory
Proposed by: define-avatar-client-runtime
Corrects:
[Expert Panel Review Record](expert-panel-review-2026-07-10.md)

This immutable addendum corrects arithmetic and provider statements in the
captured expert-panel record without rewriting that historical record. The
current proposal, design, and delta specifications remain authoritative.

## Corrected Verdict Accounting

The seven expert reports produced 71 classified findings: 57 CONFIRMED, 13
ADJUSTED, and 1 REFUTED. CONFIRMED plus ADJUSTED means 70 expert findings
survived verification. The completeness critic added 8 findings. The corrected
summary is therefore:

- 79 total findings considered;
- 78 surviving or added actionable findings; and
- 1 refuted finding.

The original machine-readable finding register was not retained. These totals
are narrative provenance, not independently reproducible review evidence, and
no implementation or release decision may depend on the counts alone.

## Corrected OpenAI Provider Facts

Facts rechecked against OpenAI documentation on 2026-07-10:

- `gpt-realtime-2.1` is an API Realtime model with a 128,000-token context
  window and 32,000 maximum output tokens. The earlier ~28.7k input-token claim
  is not applicable to this model.
- A Realtime session has a maximum duration of 60 minutes, and voice cannot be
  changed after the model has emitted audio.
- With VAD enabled, WebRTC and SIP automatically cancel an interrupted response
  and truncate unplayed audio.
- WebRTC push-to-talk is a separate flow. In addition to `response.cancel` and
  `output_audio_buffer.clear`, it requires `input_audio_buffer.clear`,
  `input_audio_buffer.commit`, and `response.create` with VAD disabled.
- `POST /v1/realtime/calls/{call_id}/hangup` can terminate both SIP and WebRTC
  Realtime sessions.
- The public OpenAI developer documentation does not establish that
  `gpt-live-1` is "ChatGPT-only." The only verified API statement is that no
  supported `gpt-live-1` API contract was found; the stronger historical claim
  is withdrawn.

Official sources:

- [GPT-Realtime-2.1 model](https://developers.openai.com/api/docs/models/gpt-realtime-2.1)
- [Realtime conversations](https://developers.openai.com/api/docs/guides/realtime-conversations)
- [Realtime SIP and hangup](https://developers.openai.com/api/docs/guides/realtime-sip#hang-up-the-call)

## Corrected Qualification Status

API availability is not xFactory qualification. `gpt-realtime-2.1` is the
candidate used by the F0 lab spike, but this kernel defines no qualified
internal-live or production provider profile. Live voice remains disabled until
`qualify-avatar-live-voice` records approved promotion evidence. `gpt-live-1`
remains disabled until a supported API contract exists and a later change
qualifies it.

The neutral kernel interaction mode is `provider_vad`; the F0 OpenAI candidate
pins the documented `server_vad` example values. Push-to-talk fails preflight
into text or human handoff until a successor change defines and secures the
expanded provider-event surface.

## Subsequent Architecture Hardening

The final pre-review pass supersedes several dispositions described in the
original review record:

- the broker holds the SDP answer until call-ID-bound sideband verification,
  and the trusted client media adapter does not apply it until
  `media_authorized`;
- AVC-02 is a discriminated grant, denial, or terminal session result rather
  than a prose-only collection of canonical failures;
- avatar media consent uses a neutral purpose registry and server-side
  consent-authority port rather than extending the memory-gateway schema; and
- contract releases use matching manifest/changelog versions, annotated tags,
  exact commits, and per-file digests, with `contract-v1.6` recorded as the
  recovered legacy baseline.

## Artifact Disposition

- `proposal.md`, `design.md`, the runtime delta, and `tasks.md` carry the
  corrected provider and qualification rules.
- The four pre-review design documents in this folder are marked superseded and
  retained only as historical inputs.
- The original panel record remains unchanged and must be read together with
  this correction record.
