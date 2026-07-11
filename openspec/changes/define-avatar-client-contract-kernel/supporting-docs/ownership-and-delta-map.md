# Avatar Client Ownership And Delta Map

Status: superseded
Kind: proposal support
Captured: 2026-07-10
Updated: 2026-07-10 after lead architecture review
Superseded: 2026-07-10
Superseded by: avatar-client split proposal set
Relocation note: historical body frozen; supersession links updated for the split
Proposed by: define-avatar-client-runtime
Staging ID: openxFactory:staging:avatar-client

> Historical pre-review map. Its 12-contract ownership table and F1-F6 scope
> are superseded and must not drive implementation. Use the
> [kernel proposal](../proposal.md), [kernel design](../design.md),
> [runtime delta](../specs/avatar-client-runtime/spec.md), and
> [repository-boundary delta](../specs/repo-boundary-governance/spec.md). The
> [parallel plan](avatar-client-parallel-workstream-plan.md) owns decomposition.

## Ownership

| Concern | Canonical owner | Implementation home | Rule |
| --- | --- | --- | --- |
| AVC-01 through AVC-12, shared definitions, registries, fixtures, compatibility, validation | openxFactory | `contracts/avatar-client/`, validator scripts | Neutral meaning never originates in generated bindings or provider DTOs. |
| Provider-neutral session broker, WSS control, leases, commands/events/snapshots, audit, kill switches | openxFactory control API | `xfactory/avatar_runtime/` | This is the authoritative server trust boundary. |
| OpenAI call creation, standard API key, model/prompt/tool configuration, sideband controller | openxFactory server adapter | `xfactory/avatar_runtime/openai/` | Privileged provider logic never ships in Flutter. |
| Generated Dart bindings, pure reducer, adaptive UI, direct WebRTC peer, constrained data channel, platform adapters | `xfactory-avatar-client` | Private Flutter repository | The client emits commands and observations; it cannot author authority or execute tools. |
| Hermes policy, consent, confirmations, approvals, normalized tool arguments, execution, records, handoff | Hermes and governed workflow services | Control/workflow plane | Provider output is evidence, not authority. |
| Domain persona, language, disclosure, speech gate, safety, consent purposes, retention, tools, handoff | Owning DomainxFactory | Immutable domain overlay | Domain policy specializes without forking neutral protocol. |
| Interactive workflow editing and dense operations | Future conventional web console | Separately approved private web repository | Existing React Flow/XState standard remains authoritative. |
| Generated TypeScript bindings | Future web console | Web repository | Deferred until the web-console boundary is proposed. |

## Neutral Standard

- logical session, session epoch, media leg, control lease, and state revision;
- AVC-01 through AVC-12 fields and compatibility;
- command/event/snapshot authority and idempotency;
- lifecycle, control health, media state, workflow projection, and presentation
  modes;
- confirmation digest, consent, retention, recovery, handoff, and audit rules;
- capability and model-promotion behavior;
- accessibility, safe rendering, fallback, acceptance, and release gates.

## OpenAI Server Adapter

- `gpt-realtime-2.1` and future qualified model bindings;
- brokered `/v1/realtime/calls` SDP creation and provider call identity;
- standard API key and approved safety identifier;
- sideband WebSocket, prompt/policy/voice/turn/tool configuration;
- provider function-call evidence and governed result return;
- provider event/error mapping, cleanup, redaction, model resolution, and
  provider-specific latency markers.

## Flutter Client Implementation

- reproducible Dart bindings pinned to openxFactory;
- immutable view state, pure reducer, widgets, responsive layout, and
  accessibility;
- authenticated AVC WSS client and typed command API;
- direct WebRTC peer, microphone/device/audio lifecycle, and strict
  data-channel allowlist;
- Windows/web storage capability adapters and offline-policy enforcement;
- deterministic fixture adapter, platform packaging, telemetry, and release
  automation.

## OpenSpec Delta Map

| Capability | Delta | Material promoted |
| --- | --- | --- |
| `avatar-first-ui` | New | Adaptive shell, orthogonal state, Hermes defaults, controls, recording awareness, accessibility, persona/media-leg continuity, disclosure, safe rendering, handoff, Flutter/web split. |
| `avatar-client-runtime` | New | AVC-01 through AVC-12, authenticated grants, brokered direct media, sideband, commands/events/snapshots, leases, recovery, confirmation digest, safety, retention, telemetry, F1-F6 release gates. |
| `shared-contract-ownership` | Added requirements | Canonical contract/validator and reference server ownership plus reproducible generated binding pins. |
| `repo-boundary-governance` | Added requirements | Private independently released Flutter repository, server/client trust split, supply-chain evidence, deferred aggregation/web integration. |
| `workflow-visualization` | No delta | React Flow/XState/Mermaid remains authoritative; Flutter uses read-only summaries and authenticated web handoff. |

## Realization Boundary

This proposal realizes neutral contracts, reference server control modules,
private Flutter F1-F6, and the first qualified OpenAI profile. It does not pick
an aggregation gitlink path, build the web console, replace workflow
visualization, release native iOS/Android, add a second provider, or activate
GPT-Live before its separately satisfied qualification gate.
