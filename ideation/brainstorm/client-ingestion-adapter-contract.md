# Client Ingestion-Adapter Contract: governed connectors from source systems to evidence rows — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Details the ingestion-adapter contract for the client-layer knowledge
base — the governed equivalent of Cerebras' "plugin script per source." An
adapter connects one client source system (chat, VCS, tickets, CRM, calendar,
docs) and emits **evidence rows** into the tenant-scoped store. It composes the
ratified memory-gateway provider contracts (provider-profile + provider-binding
+ consent-profile) rather than duplicating them, and adds the ingestion layer:
differential sync, structure-before-embed, PII redaction, source-authority
tagging, and permission mapping. It runs as a bounded read-only Plane-2 worker
under the client's Integrations & Credentials Steward and the consent gate —
never holding a secret, never crossing a tenant boundary. Neutral (openxFactory)
contract; per-source adapters are client instances. Parent:
`hermes-knowledge-base-architecture.md`.
Topics: ingestion-adapter, evidence-rows, memory-gateway, provider-binding,
consent, tenant-isolation, source-authority, structure-before-embed,
differential-sync, client-hermes, plane-2, cerebras
Repository context: openxFactory (neutral adapter contract; instances per client under config/clients/<client>/)
Captured: 2026-07-21

## Possible feats

- **Neutral `client_source_adapter` schema** (composes the gateway provider contracts).
- **Neutral `evidence_row` schema** (extends `context-packet`).
- **Reference adapters** (chat, VCS, tickets) as the first instances.
- **Structuring-worker contract** (structure-before-embed as a Plane-2 worker).

## What an adapter is

A bounded, read-only connector from one client source system to the knowledge
base. Cerebras' plugin script "reads from the system and emits rows matching a
shared schema"; the xFactory adapter does the same *inside* the governance rails
— it composes the ratified gateway contracts and adds the ingestion pipeline. It
runs as a **Plane-2 omnigent worker** (read-only to the source, no standing
credentials), governed by the client's Hermes (the Integrations & Credentials
Steward approves the binding; the consent gate authorizes the data).

## The adapter manifest

Composes, does not duplicate, the ratified gateway contracts
(`provider-profile`, `provider-binding`, `consent-profile`):

```yaml
schema_version: 1
kind: client_source_adapter
adapter:
  id: <slug>                       # e.g. opensoft-slack, opensoft-jira
  source_class: chat | version_control | ci | ticketing | calendar | crm | documents | custom
  tenant_ref: <client>             # tenant-isolation key on every emitted row
  provider_profile_ref: <ref>      # ratified: the source TYPE + capabilities
  provider_binding_ref: <ref>      # ratified: the client instance; credential by REFERENCE (vaultref://…), never a secret
  scope:
    projects: [<subject/project refs>]   # which Customer-layer subjects this source maps to
    include: [<channels|repos|folders>]
    exclude: [...]
  consent:
    consent_profile_ref: <ref>     # ratified; ingest AND retrieval blocked without it
    pii_handling: redact | tokenize | exclude
  source_authority: source_backed | observed | self_reported   # ratified authority_levels (memory-gateway vocabularies) — tag stamped on every row
  sync:
    mode: full | differential      # differential re-processes only changed items (Cerebras)
    cadence: <schedule>
    since_cursor: <opaque>
  structuring:
    mode: structure_before_embed   # noisy sources are summarized, never raw-embedded
    structurer_worker: <plane-2 worker ref>
  emits: evidence_row
  status: configured_but_inactive | active | revoked
```

## The evidence-row output

The ingested, governed unit; the governed form of Cerebras' embeddings row, and
what retrieval later composes into the gateway's `context-packet`:

```yaml
kind: evidence_row
row:
  id
  tenant_ref                       # isolation — retrieval never crosses it
  source_ref: {adapter_id, native_id, url}       # provenance + back-link
  project_scope: [<subject/project refs>]
  content: <structured text>       # the summarized/structured form that gets embedded
  structured: {question, summary, resolution, entities, refs}   # source-shaped (Cerebras' Slack shape)
  key_excerpts: [<raw>]            # "burst": high-signal raw items kept alongside the summary
  embedding: <vector | deferred>
  metadata: {authored_at, author_ref, source_class}
  visibility: {acl_from_source, tenant_scoped: true}   # source ACL → who may retrieve
  source_authority: <tag>          # low-authority cannot silently drive a decision
  consent_state: granted | ... ; revocable: true
  freshness: {ingested_at, source_cursor}
```

## The ingestion pipeline (governed)

1. **Discover** — the client `source_inventory_agent` lists candidate sources
   (the `installation_discovery` workflow).
2. **Bind** — a `provider-binding` with the credential *reference*; the
   Integrations & Credentials Steward approves scope + binding.
3. **Consent gate** — no ingest without a satisfied `consent-profile`; the Legal
   & Compliance Counsel's constraints apply (data-protection).
4. **Fetch** — differential since the cursor (only changed items re-processed).
5. **Structure-before-embed** — a Plane-2 structuring worker summarizes each item
   into the structured record and captures key raw excerpts (burst).
6. **Redact** — PII per `pii_handling`.
7. **Emit** — evidence rows, tenant-tagged, source-authority-tagged, ACL-mapped.
8. **Embed + store** — into the tenant-partitioned store.
9. **Audit** — a gateway `usage-event` per ingest; supports `revocation` /
   `erasure` (revoke a source → purge its rows).

The `client_memory_steward` then decides which emitted rows promote from
`current_state_evidence` into `client_private_memory`,
`customer_relationship_memory`, or a `domain_learning_candidate`.

## Governance obligations (non-negotiable)

- **Credential-reference only** — never a secret in the manifest or a row.
- **Tenant isolation** — rows tagged + partitioned by `tenant_ref`; retrieval
  never crosses it.
- **Consent-gated** — both ingest and retrieval pass the consent profile;
  revocable and erasable.
- **Source-authority tagged** — every row; synthesis cites, low-authority cannot
  drive a decision silently.
- **Permission mapping** — source ACL → row `visibility`; retrieval honors it.
- **No raw-embed** — noisy sources are structured first.

## Lifecycle & authority

`configured_but_inactive` by default → **Integrations & Credentials Steward**
approves the binding/scope + the **consent gate** authorizes the data → one
successful dry-run → `active`. Health shows on the scaffold's
`integration_credential_status` surface. A consent `revocation` or a steward
decision → `revoked` + `erasure` of its rows.

## Open questions

- **evidence_row vs. context-packet** — is `evidence_row` a new kernel or an
  ingest-time profile of the ratified `context-packet`? (Leaning: distinct at
  ingest, composed into context-packets at retrieval.)
- **Adapter runtime** — a first-party worker per `source_class`, or a generic
  worker + declarative source config (the Cerebras "small Python module")?
- **Structurer trust** — the summarizing worker shapes what becomes memory; does
  its output need a spot-check gate before embedding, or is provenance enough?
- **ACL freshness** — source permissions change; how often is `visibility`
  re-synced vs. checked live at retrieval?
- **Custom `source_class`** — the plugin escape hatch: how bounded is a
  client-authored custom adapter, and who reviews it?
