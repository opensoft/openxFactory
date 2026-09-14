# Staged: Ideation Action Plane — intents over write authority

Status: staged
Kind: architecture
Summary: Turn the ideation dashboard into the action center where humans
manage the whole ideation process — WITHOUT weakening D16. The dashboard
(hosted web, and the Flutter verdict-terminal app) never gains write
authority: a click emits a signed, attributed INTENT; a minimal-authority
inbox service dispatches the apply lane; the existing gate-console engine
applies the verb against a fresh cloud checkout with server-side
revalidation, and delivers intent + gate-action record + updated artifacts
together via the rolling-PR pattern. Two-plane rendering keeps the snapshot
deterministic while a live intent feed overlays pending/applied/refused; the
refusal ledger becomes UI. First verb: the dispose-possible tray. Identity:
per-user htpasswd (ingress-forwarded actor) now, Keycloak later without
contract change. Includes the temporal governance rule the plane depends on:
GATES HAPPEN ON MAIN (a lifecycle transition is not real until merged).
Topics: ideation-dashboard, gate-console, interactivity-boundary, intent-queue, possibles-register, roles-authority-model, identity-brokering, document-lifecycle, doc-management, doc-workflow
Repository context: openxFactory owns the `gate-intent` kernel, the
`ideation-intent-plane` capability, and the document-lifecycle delta;
codexFactory realizes the tray/overlay UI, the local executing gate routes,
and the apply-lane orchestration; the inbox service and per-user ingress
auth deploy through omnigent-install; the aggregation repo wires the lane.
Staging ID: openxFactory:staging:ideation-action-plane
Source: ideation/brainstorm/dashboard-action-center.md and
ideation/brainstorm/cloud-workstation-topology.md (both Brett-locked
2026-07-23, the day the first derive->dispose cycle ran end-to-end)
Target capabilities: ideation-intent-plane (ADDED), document-lifecycle (MODIFIED)

## Claims

1. **Intent, not write.** A hosted/mobile action is a request artifact
   (`gate-intent`: actor, verb, target, args, requested_at,
   snapshot_rev_seen, status) — the serving surfaces keep zero write
   authority and zero repo credentials; the gate-console engine remains the
   only executor, with full server-side revalidation.
2. **Minimal-authority inbox.** The only new credentialed component holds
   `actions:write` on ONE workflow (dispatch-only); it stamps the actor from
   the ingress-authenticated username and enforces a per-actor verb
   allowlist. It cannot touch repository contents.
3. **Custody, not decision (second-touch, DECIDED).** The authenticated
   click is the decision; the rolling intents PR is custody — batched,
   auto-merge on approval within the existing Merge-Master ritual; the
   intent-feed overlay covers the latency (apply lane may trigger
   snapshot rebake on success).
4. **Two-plane rendering.** The deterministic snapshot stays the only
   view-model source; a live intent feed overlays per-tile chips and a
   refusal panel (GateRefused/boundary refusals rendered, never silent).
5. **Client parity.** Hosted web and the Flutter app are the same client
   class: snapshot consumer + intent emitter over the same two endpoints;
   no on-device checkout ever (Codespaces + port-forwarded local dashboard
   is the heavy-authoring escape hatch).
6. **Gates happen on main.** Organize/propose/ratify/archive are main
   events; unmerged transitions are exploration, not status — the shared
   dashboard is definitionally the team's true pipeline picture.

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

No conflicts recorded.

## Open questions

1. Inbox hosting shape: sidecar in the dashboard pod vs own deployment.
2. Intent kernel home: gate-action-record family sibling vs own schema
   file (it is a REQUEST, not an applied-action record).
3. Per-actor verb authority map: static config first vs
   roles-authority-model binding from day one.
4. Apply cadence: on-dispatch per intent vs micro-batch (N minutes) vs
   piggyback on the nightly only.
5. Intent retention: are applied/refused intents committed forever beside
   gate-action records, or pruned after N days with the record as the
   durable trace?

## Exit path

Immediate exit: `add-ideation-intent-plane` (this gate) — the gate-intent
kernel + inbox + apply lane + dispose tray + local executing gate routes +
the document-lifecycle gates-on-main delta. The sibling fragment
[drive-membrane.md](drive-membrane.md) exits separately after its
Drive↔NotebookLM markdown-ingestion spike.
