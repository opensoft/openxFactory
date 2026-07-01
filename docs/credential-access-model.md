# xFactory Credential Access Model

Status: shared xFactory standard
Repository context: openxFactory
Purpose: define how xFactory systems declare, bind, approve, issue, use, audit,
and revoke credentials without storing raw secrets in repos, Hermes memory, or
worker workspaces.

## 1. Core Rule

```text
No xFactory repo, domain stack repo, tenant repo, agent identity repo, customer
Hermes layer, client Hermes layer, domain Hermes layer, or Omnigent worker
stores raw credentials.
```

Repos store credential requirements, reference names, binding templates,
approval policy, grant templates, and audit rules. Real secrets live in approved
secret providers.

## 2. Layer Model

```text
Domain stack credential contract
  what this factory type may need

Client or tenant credential binding
  where this customer or Opensoft client stores or delegates the credential

Hermes credential policy
  who may request access, for which workflow, under which approval

Runtime capability grant
  short-lived scoped access issued to one approved job

Audit and revocation
  durable record of request, approval, issue, use, outcome, and cancellation
```

The domain stack says what kind of access may be needed. The client or tenant
binds that need to a real provider. Hermes approves use. Omnigent executes only
with the grant it receives. Workers never persist the credential.

## 3. Credential Ownership

### Domain Stack Repos

Domain stack repos such as `MedxFactory`, `OpsxFactory`, `LedgerxFactory`,
`AdxFactory`, and `codexFactory` may define:

- credential requirement IDs
- credential purposes
- allowed workflows
- required approval gates
- access modes
- minimum scopes
- maximum grant duration
- audit requirements
- binding templates

They must not define:

- passwords
- API keys
- OAuth refresh tokens
- private keys
- service principal secrets
- live connection strings
- patient, customer, or tenant secrets

### Client or Tenant Deployments

Client or tenant deployments bind domain requirements to real secret providers.
For self-hosted deployments, this binding is collected through the local
runtime binding wizard described in
[Self-Hosted Runtime Binding Plan](self-hosted-runtime-binding-plan.md).

Bindings may reference:

- Azure Key Vault
- AWS Secrets Manager
- GCP Secret Manager
- 1Password or Bitwarden enterprise vaults
- customer-owned vaults
- Opensoft-hosted vaults
- OAuth delegated consent stores
- workload identity providers

Bindings must use references, not raw secret values.

### Hermes

Hermes owns credential approval policy.

Hermes decides:

- whether a workflow may request a credential
- whether customer or patient consent is required and present
- whether client policy allows access
- whether human approval is required
- whether requested scopes are too broad
- how long the grant may live
- which audit record must be written

### Omnigent

Omnigent does not own credentials.

Omnigent receives a runtime capability grant after Hermes approval. The grant
should be specific to:

- one job
- one workflow
- one client or tenant
- one customer subject when applicable
- one worker or session
- one time window
- one allowed action set

Omnigent must not persist raw credential material into workspaces, logs, diffs,
repo files, memory files, screenshots, artifacts, or review packets.

## 4. Runtime Flow

```text
Customer Hermes
  -> requests a domain workflow

Client Hermes
  -> checks client policy, local integrations, tenant bindings, and consent

Domain Hermes
  -> validates domain policy, risk, review gates, and workflow authority

openxFactory / xFactory
  -> creates credential-aware job envelope

Domain Omnigent
  -> accepts job with credential requirement references

Credential broker
  -> resolves binding and issues short-lived grant

Worker session
  -> uses grant only for approved commands and tools

Audit store
  -> records request, approval, issue, use, outcome, and revocation
```

## 5. Credential Requirement Contract

Domain stacks declare requirements in abstract form.

```yaml
credential_requirements:
  - id: microsoft_365_admin
    purpose: tenant administration
    allowed_workflows:
      - mailbox_migration
      - user_lifecycle
      - security_review
    access_mode: delegated_oauth
    minimum_scopes:
      - user.readwrite.all
      - exchange.manage
    requires_domain_approval: true
    requires_human_approval: true
    max_grant_minutes: 60
    audit_required: true
```

The requirement says what kind of credential may be needed. It does not say
where a customer's credential lives and does not include the credential itself.

## 6. Credential Binding Contract

Client or tenant deployments bind requirements to real providers.

```yaml
credential_bindings:
  microsoft_365_admin:
    provider: azure_key_vault
    vault: opsxfactory-client-a
    secret_ref: m365-admin-app-registration
    owner: client_a
    rotation_policy: tenant_managed
```

The binding says where the credential can be resolved after approval. It must
not include the raw secret value.

## 7. Runtime Capability Grant

A runtime capability grant is the only credential shape a worker should see.

```yaml
runtime_capability_grant:
  id: RCG-2026-06-30-0001
  job_id: JOB-2026-06-30-0001
  client_id: client_a
  domain: opsx
  requirement_id: microsoft_365_admin
  issued_by: hermes_credential_broker
  approved_by: opsx_domain_hermes
  customer_ref: tenant://client-a
  allowed_workflows:
    - mailbox_migration
  allowed_actions:
    - read_mailbox_inventory
    - create_migration_batch
    - check_migration_status
  expires_at: "2026-06-30T15:00:00Z"
  audit_ref: audit://credential-access/RCG-2026-06-30-0001
```

The grant should be short-lived, narrowly scoped, auditable, and revocable.

## 8. OpsxFactory

`OpsxFactory` is the IT administration and operations domain stack.

OpsxFactory is credential-heavy because workflows may touch Microsoft 365,
Exchange Online, Azure, Entra ID, Intune, DNS, GitHub, backup platforms,
endpoint management, network devices, hosting providers, and customer tenant
admin portals.

OpsxFactory should prefer:

- delegated OAuth over stored passwords
- workload identity over long-lived client secrets
- just-in-time elevation over standing administrator access
- customer-owned vaults when the customer wants credential custody
- Opensoft-hosted vaults only when Opensoft is the managed service operator
- short grant windows for admin workflows
- mandatory audit for all privileged operations

OpsxFactory workers must never receive standing global admin credentials. They
should receive grants for exact workflows, tenants, command classes, and time
windows.

## 9. MedxFactory

`MedxFactory` is the medical domain stack.

MedxFactory credentials are sensitive because workflows may touch EHR systems,
practice management systems, scheduling systems, patient messaging systems,
diagnostic systems, lab portals, pharmacy systems, insurance portals, fax
services, document repositories, and medical device or IDTF systems.

MedxFactory must separate:

```text
Patient Hermes
  lifetime patient context, consent, preferences, and patient memory

Clinic or client Hermes
  local clinic, hospital, pharmacy, imaging center, or IDTF integrations

Medical Domain Hermes
  medical policy, workflow approval, review, and escalation

Medx Omnigent
  approved execution with scoped runtime grants
```

Patient Hermes must not own clinic-wide credentials. Patient Hermes may request
patient-specific actions, but client Hermes, Medical Domain Hermes, and tenant
policy decide what credential access is allowed.

MedxFactory should prefer:

- tenant-isolated vaults
- per-patient context scoping
- consent checks before patient-data access
- domain approval before regulated or care-affecting workflows
- de-identification before promoting patient-derived lessons to domain memory
- stricter audit than non-regulated stacks
- no broad credential grants to general-purpose workers

## 10. Other Domain Stacks

LedgerxFactory should use client and ledger scoping, explicit approval for money
movement or filing actions, and read-only grants by default.

AdxFactory should separate planning access, read-only analytics access,
campaign-management access, and spend-authorizing access.

codexFactory should separate read, branch, PR, package publish, deployment,
and production access. Deployment and production grants should require explicit
Hermes approval.

## 11. Audit Requirements

Every credential grant must write an audit record.

```yaml
credential_access_audit:
  grant_id:
  job_id:
  domain:
  client_id:
  customer_ref:
  requirement_id:
  binding_ref:
  requested_by:
  approved_by:
  issued_by:
  worker_id:
  allowed_actions:
  issued_at:
  expires_at:
  revoked_at:
  outcome:
  evidence_refs:
```

Audit records should be available to Hermes dashboards, client reporting, and
compliance review.

## 12. Revocation Rules

Hermes or the credential broker must revoke a grant when:

- the job completes
- the grant expires
- the tenant revokes authorization
- customer or patient consent is withdrawn
- the worker session is terminated
- the workflow leaves its approved scope
- suspicious behavior is detected
- a human approver cancels the job

Workers must tolerate revocation and stop the affected workflow immediately.

## 13. Design Rules

1. Raw credentials live only in approved secret providers.
2. Repos store requirements, references, and policy, never secret values.
3. Domain stacks declare credential requirements.
4. Clients or tenants bind requirements to real providers.
5. Hermes approves credential use.
6. Omnigent receives only short-lived scoped grants.
7. Patient Hermes does not own tenant-wide credentials.
8. Admin credentials require just-in-time approval.
9. Regulated data access requires audit and policy review.
10. Grants are revoked at completion, expiration, cancellation, or scope break.
