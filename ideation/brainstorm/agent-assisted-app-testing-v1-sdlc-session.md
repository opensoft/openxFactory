# V1 SDLC Session Protocol — Brainstorm

Status: brainstorm
Kind: process
Summary: Define the minimum durable intent-to-agent communication loop needed for a user or Hermes observation to become a proposed, iterated, tested, experience-admitted, and merged change.
Topics: agent-assisted-app-testing, sdlc-session, bidirectional-comms, intent-lifecycle, proposal-iteration, hermes-autonomy, merge-control
Repository context: openxFactory; v1 communication contract for the annotation client, Project Hermes, local bridge, coding and specialist agents, verification runners, and merge authority
Captured: 2026-08-02

## Possible feats

- **`v1-sdlc-session` protocol** — define the versioned event envelope, lifecycle states, authority decisions, and evidence references for the minimum autonomous or user-guided repair loop.
- **Local session bridge** — connect the browser annotation UI to the agent and repository tools without exposing model credentials or unrestricted source mutation to the page.

## Focus

The in-house annotation tool needs bidirectional communication with the coding agent, but v1 does not need general-purpose co-editing or arbitrary live browser control. Project Hermes also needs to originate work, manage decisions, and report outcomes without pretending every transition came from the browser user. The shared requirement is a small, durable control loop for the basic software-development lifecycle:

```text
observe/capture → propose → iterate → test → experience admission → request merge → merge
```

This document isolates the messages, states, and authority boundaries required for that loop.

## Proposed model

The participants are:

- **User browser:** may create an annotation, inspect status and previews, supply feedback, or exercise a policy-required decision; it is not the mandatory manager for every session.
- **Autonomous UI observatory:** creates evidence-backed findings and candidate intents under a Project Hermes audit mandate.
- **Project/Subject Hermes:** owns project intent context, Project Owner acceptance, Project Manager sequencing/disposition, the active autonomy policy, and agent-only decisions inside that envelope.
- **Annotation/session bridge:** owns the session stream, correlates events, presents agent status, and exposes narrowly scoped browser tools.
- **Coding agent:** interprets intent, proposes a plan, edits the repository, runs the selected checks, and requests merge.
- **Verification runner/CI:** executes tests and visual checks and emits evidence.
- **UI/UX specialists and Experience Council:** propose or review experience changes and emit independent findings and a decision-ready packet.
- **Merge Council and Merge Master:** evaluate complete readiness and authorize external enforcement inside the configured low-risk envelope.
- **External enforcement:** Git/CI applies the merge only when its checks, identities, and branch policy permit it.

The browser should communicate with a local bridge or agent client, not directly with a model provider. MCP can expose request/response capabilities such as reading an intent, requesting a capture, running verification, and publishing a preview. A small event stream can deliver progress and decisions back to the browser. The protocol does not require the browser to implement a full chat client.

### V1 lifecycle

```text
observed / captured
        │
        ▼
proposal_ready ── Subject Hermes rejects/revises ──┐
        │ admitted                                 │
        ▼                                          │
implementing ── blocked ───────────────────────────┤
        │                                          │
        ▼                                          │
verification_running                               │
        ├── failed → iteration_requested ──────────┘
        │
        ▼ passed
experience_review ── FIX/REJECT ───────────────────┐
        │ ADMIT                                    │
        ├── optional preview/user feedback ────────┤
        │                                          │
        ▼                                          │
merge_requested → merge_admitted                   │
        │                                          │
        ▼                                          │
      merged                                       │
        │                                          │
        └── post-merge observation → linked intent ┘
```

`abandoned`, `blocked`, and `parked` are terminal or waiting states available from any active state. Annotation cleanup should follow `merged`, a Project Hermes resolution, or an explicitly recorded user resolution—not merely a green test result. Protected decisions remain parked when the required human or professional authority is unavailable.

### V1 event vocabulary

| Event | Direction | Purpose |
| --- | --- | --- |
| `observation.created` | observatory/runner → bridge/Hermes | Record a proactive finding, regression, or approved telemetry signal without claiming user authorship. |
| `intent.created` | browser/Hermes → bridge/agent | Create the normalized request, origin, objective, autonomy class, and environment context. |
| `proposal.ready` | agent/specialist → Hermes/browser | Present the interpretation, variants, scope, risks, and test plan. |
| `proposal.decision` | Subject Hermes or policy-selected user → agent | Admit implementation, reject the proposal, or request a revision. |
| `work.status` | agent → Hermes/browser | Report queued, implementing, blocked, parked, or completed work with a concise explanation. |
| `verification.started` | runner/agent → Hermes/browser | Identify the checks and render manifests expected for evidence. |
| `verification.result` | runner/agent → Hermes/browser | Report pass, fail, unavailable, flaky, or needs-authority with evidence links. |
| `experience.review.result` | Experience Council → Subject Hermes | Report specialist findings, disagreements, required fixes, and recommendation. |
| `preview.ready` | agent → Hermes/browser | Provide the exact revision, synthetic missions, and optional user-review instructions. |
| `iteration.requested` | Hermes/browser/council → agent | Add findings, feedback, or a child observation to the same intent lineage. |
| `admission.decision` | Subject Hermes/owning gate → agent/merge council | Record `ADMIT`, `FIX`, `PARK`, or `REJECT` for the exact revision. |
| `merge.requested` | agent/Hermes → Merge Council | Request readiness evaluation after required experience and engineering evidence. |
| `merge.decision` | Merge Master → external enforcement/agent | Admit, block, or park the enforcement action under live policy. |
| `merge.result` | external enforcement → Hermes/browser | Report merged, failed, conflicted, or cancelled outcome. |
| `session.closed` | bridge/Hermes → browser/agent | Mark the intent lineage resolved, abandoned, blocked, or parked. |

### Event envelope

The v1 envelope can remain small while still supporting replay and idempotency:

```json
{
  "protocol": "xfactory.sdlc-session",
  "protocol_version": "1.0",
  "session_id": "session_01J...",
  "intent_id": "intent_01J...",
  "revision": 3,
  "event_id": "event_01J...",
  "event_type": "experience.review.result",
  "actor": "experience-council",
  "actor_role": "ui-experience-review",
  "authority_ref": "policy://project-alfa/ui-autonomy-v2",
  "state": "experience_review",
  "occurred_at": "2026-08-02T12:00:00Z",
  "required_action_owner": "project-owner",
  "correlation_id": "proposal_01J...",
  "payload": {
    "status": "admit-recommended",
    "summary": "Required functional, accessibility, visual, and journey checks passed with no blocking experience finding"
  },
  "evidence_refs": [
    "artifact://verification/intent_01J/report.json",
    "artifact://screenshots/manifest_01J/checkout-panel.png"
  ]
}
```

`event_id` must be idempotent, `revision` must advance within an intent lineage, and evidence should be referenced rather than embedded in every event. Actor identity, role, authority source, and original intent origin must remain explicit. The bridge should retain enough history to replay the current session to a reconnecting browser or Project Hermes controller.

## Interfaces and boundaries

The protocol owns session identity, lifecycle transitions, actor and authority decisions, progress, and links to evidence. It does not define the internal LLM prompt, repository editing mechanism, test implementation, screenshot algorithm, or Git provider API.

The browser may carry feedback or a policy-required decision, but it should not receive model credentials or arbitrary shell access. Project Hermes may admit in-envelope proposals and experience outcomes, but implementation, specialist review, Merge Master authority, and external enforcement remain separately auditable capabilities. Every agent or human decision should be attributable, authority-bound, and tied to the revision that was reviewed.

## Alternatives and tensions

- **Structured events versus free-form chat:** structured events make lifecycle and authority auditable; a small free-form note can still be carried inside proposal decisions and iteration requests.
- **MCP-only versus MCP plus event stream:** MCP can expose the tools, while a stream makes Project Hermes progress, browser status, and optional user feedback responsive. A polling fallback may be simpler for the first local prototype.
- **Agent-executed merge versus merge request only:** direct merge is faster but concentrates authority; v1 should route final admission through Merge Master and the external enforcement identity rather than treating Project Hermes acceptance as a Git capability.
- **One intent revision versus child intents:** editing the same revision is simpler; child annotations preserve a clearer lineage when the user's request changes materially.

## Open questions

- Is v1 transport local stdio MCP, local Streamable HTTP, or a bridge with a small browser event endpoint?
- Which event transitions are internal to Project Hermes, visible in the browser, or require a protected external authority?
- Is an integrated preview mandatory before `merge.requested` for every visual change, even when no human review is required?
- Which Git/CI surfaces accept Merge Master agent admission, and which remain structurally human-gated?
- What is the retention policy for session events, screenshots, test logs, and rejected proposals?

## Relationships

- [Annotation-Centered Test Intent](agent-assisted-app-testing-intent.md) supplies the initial intent and target provenance.
- [Preview Verification and Feedback Loop](agent-assisted-app-testing-preview-approval.md) supplies the integrated synthetic review, optional user feedback, and iteration boundary.
- [Cross-Environment Verification and Parity](agent-assisted-app-testing-verification-parity.md) supplies verification results and evidence references.
- [Chromium Render Manifest](agent-assisted-app-testing-chromium-render-manifest.md) identifies the canonical visual environment referenced by verification events.
- [Autonomous UI Observatory](agent-assisted-app-testing-autonomous-ui-observatory.md) emits proactive observations and Hermes-originated intents.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) emits structured review and fix events.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) supplies the live authority reference for agent-only decisions.
