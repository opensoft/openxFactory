# Staged fragment: Drive Membrane — projection mirror out, intake lane in

Status: staged
Kind: architecture
Summary: Google Drive as a MEMBRANE around the git truth, never a competing
record. Outbound: a projection lane exports lifecycle-filtered,
revision-stamped markdown (canon/drafts/ideation sets) to a Drive tree owned
by the org service identity; Google's Drive↔NotebookLM sync ingests those
folders, replacing per-source push churn (nlm CLI stays as fallback).
Inbound: per-engineer Drive INBOX folders + notebook notes are swept by an
intake lane that converts to markdown, scaffolds house headers (authoring
create-only scaffold), stamps human-authored provenance (author = inbox
owner), and delivers via a rolling intake PR; on merge the doc joins the
corpus/index/mirror and the inbox copy retires to imported/. Git repos are
NEVER cloned into Drive (sync corruption + wrong branch semantics).
Topics: notebooklm-projection, lifecycle-projection, google-drive, ideation-dashboard, identity-brokering, doc-management, doc-workflow
Repository context: openxFactory owns the membrane contract and lifecycle
deltas; codexFactory realizes the export/intake lanes; provisioning
(service identity, Drive tree, per-engineer inboxes) lands in the install
repos per the OpsxFactory runbook pattern.
Staging ID: openxFactory:staging:ideation-action-plane (fragment 2)
Source: ideation/brainstorm/cloud-workstation-topology.md (Brett-locked 2026-07-23)
Target capabilities: lifecycle-notebook-projection (MODIFIED — mirror + intake)

## Claims

1. Git is the only truth; Drive holds a generated outbound mirror and
   per-engineer inbound capture buffers — both regenerable, neither a record.
2. The mirror exports main only, filtered by lifecycle set, revision-stamped.
3. Intake captures are create-only, header-scaffolded, author-attributed
   (`origin: human-authored`) and land via rolling PR; inbox copies retire
   after merge.
4. Per-engineer Workspace identities are required by the NLM share-grant
   model regardless; the membrane adds no identity cost beyond it.

## Open questions

1. SPIKE (blocks exit): does Drive↔NLM sync ingest markdown well, and what
   are its cadence/quota behaviors on a few-hundred-file tree?
2. Folder↔notebook mapping (per lifecycle set vs hybrid per-topic subfolders).
3. Export transform (raw markdown vs light rendering of load-bearing headers).
4. Drive API credential custody (a lane credential, never in serving pods)
   and the provisioning runbook home.
5. Whether workbench ad-hoc sets get ephemeral Drive exports.

## Deferral with a named gate (recorded 2026-08-28)

**DEFERRED. The gate is a spike nobody owns.** Fragment 1 (the intent
plane) exited at its gate and is live as the ACTIVE change
`add-ideation-intent-plane`; this fragment did not go with it, and open
question 1 above is the reason.

**GATE: the Drive↔NLM markdown-ingestion spike** — does Drive↔NLM sync
ingest markdown well, and what are its cadence and quota behaviours over a
few-hundred-file tree? The spike is unassigned and unscheduled. Every other
question here (folder↔notebook mapping, export transform, credential
custody, ephemeral workbench exports) is answerable only after it, so the
fragment cannot be advanced by design work alone — which is exactly what
distinguishes this from a topic that is merely waiting for attention.

**This deferral is a schedule, not a standing.** It changes no `Status:`,
and it does NOT stop the topic ageing in doc-health: there is no `deferred`
state for a staged topic and this change deliberately adds none. The
`ideation-action-plane` topic folder holds both fragments, so it keeps
ageing on fragment 1's account too until that change lands.

## Exit path

Own change (working name `add-drive-membrane`) AFTER the ingestion spike
answers open question 1; rides the intent plane's identity ladder
(htpasswd→Keycloak) for share-list automation.
