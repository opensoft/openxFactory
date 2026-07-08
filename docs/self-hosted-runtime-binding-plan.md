# Self-Hosted Runtime Binding Plan

Status: draft
Kind: plan
Repository context: openxFactory
Purpose: define how a self-hosted user supplies runtime bindings,
credentials, adapters, validation, and approvals so xFactory can move from an
installable candidate to a runnable local deployment.

## 1. Position In The Lifecycle

Pre-run intake answers what should be built. Runtime binding answers what this
specific installation can actually reach, approve, and run.

```text
pre-run intake
  -> installable candidate
  -> self-hosted runtime binding
  -> local validation
  -> dry-run workflow
  -> runtime_ready or gap report
```

Pre-run should not collect raw credentials. Runtime binding may start local
login, consent, vault, adapter, and approval flows, but raw secret values still
must not be written to repos, generated docs, Hermes memory, Omnigent
workspaces, logs, screenshots, or support bundles.

## 2. Hosting Modes

### 2.1 Opensoft-Hosted

When Opensoft hosts the stack, Opensoft can handle more of the runtime
infrastructure:

- hosting environment
- base Hermes install
- base Omnigent install
- managed databases
- logging and audit stores
- secret provider setup when Opensoft has custody
- adapter deployment
- runtime validation
- managed update path

The customer still must provide authorization, consent, tenant-specific
bindings, and any approvals required by policy, law, contract, or professional
authority.

### 2.2 Self-Hosted

When the customer self-hosts, the installer must collect or verify everything
needed to run inside the customer's environment:

- local deployment target
- runtime paths and service accounts
- Hermes install or package
- Omnigent install or package
- secret provider and vault references
- adapter selection and endpoints
- OAuth or workload identity setup
- approval roles and approver references
- audit store
- validation command
- first dry-run workflow

The simple self-hosted experience should be one guided wizard with resumable
stages.

## 3. Intake Versus Runtime Binding

The intake form may collect:

- industry
- organization type
- workflows
- credential requirement families
- preferred secret provider type
- likely systems to integrate
- approval role names
- hosting preference

The runtime binding wizard collects or verifies:

- actual secret provider references
- actual adapter endpoints
- actual OAuth consent or workload identity references
- actual approver group references
- actual local service ports, paths, URLs, and storage locations
- actual validation results

Runtime binding outputs are still reference-based. They should not contain raw
secret values.

## 4. Self-Hosted Simple Process

Recommended command flow:

```bash
xfactory intake --industry <industry>
xfactory install --answers examples/instantiation-answers.generated.yaml
xfactory bind-runtime
xfactory validate-runtime
xfactory dry-run --workflow <workflow-id>
xfactory readiness
```

The TUI and Flutter installer should expose the same stages:

```text
1. Load or create intake answers.
2. Confirm self-hosted mode.
3. Check local prerequisites.
4. Install or locate Hermes.
5. Install or locate Omnigent.
6. Choose secret provider.
7. Bind credential requirements to secret references.
8. Select adapters and enter non-secret endpoints.
9. Run provider login or workload identity flows locally.
10. Configure approvers and approval gates.
11. Run validation.
12. Run first dry-run workflow.
13. Produce readiness report.
```

The wizard should be resumable. Each stage should write a non-secret state file
that says what is complete, blocked, or waiting for approval.

## 5. What The Wizard Collects

### 5.1 Deployment Target

Collect:

- operating system
- install directory
- data directory
- service user or service account reference
- container, system service, or Kubernetes preference
- local hostname or base URL
- TLS certificate reference or local dev mode
- database choice and connection reference
- object or artifact store reference
- log and audit store reference
- backup location reference

Do not collect:

- database passwords as plain text
- private keys as files inside the repo
- production connection strings in generated docs

### 5.2 Hermes Runtime

Collect:

- Hermes install source or local path
- profile directory
- memory provider reference
- domain, client, and customer Hermes layer names
- Hermes group registry source
- AI provider reference names
- tool bridge endpoint references
- backup and restore policy

Validate:

- Hermes starts
- configured profiles load
- memory provider is reachable
- three Hermes layers are mapped
- MoA/council profiles validate
- Hermes can write audit or decision records

### 5.3 Omnigent Runtime

Collect:

- Omnigent install source or local path
- worker runtime mode
- sandbox mode
- tool bundle selection
- domain overlay path
- worker capability map
- execution workspace location
- artifact output location

Validate:

- Omnigent starts
- domain overlay loads
- worker capabilities match workflow requirements
- workers cannot access raw secrets directly
- workers receive only runtime grants
- sandbox and output paths are isolated

### 5.4 Secret Provider And Credential Bindings

Collect:

- secret provider type
- vault or secret store reference
- credential requirement to secret reference mapping
- access mode for each requirement
- OAuth app or delegated consent reference
- workload identity reference
- rotation owner
- revocation owner
- max grant duration

Allowed providers:

- Azure Key Vault
- AWS Secrets Manager
- GCP Secret Manager
- 1Password or Bitwarden enterprise vault
- customer-owned vault
- local development vault for non-production
- OAuth delegated consent store
- workload identity provider

Collection methods:

- provider login flow
- OAuth device code or browser consent flow
- workload identity verification
- paste secret reference name, not secret value
- import existing vault reference
- create local development secret only when explicitly marked non-production

Validate:

- secret reference exists
- installer can verify access without printing the secret
- scope is no broader than the requirement allows
- grant duration does not exceed policy
- revocation can be tested or simulated
- audit record can be written

### 5.5 Adapters

Collect:

- adapter package or built-in adapter ID
- target external system
- non-secret endpoint URL or tenant identifier
- auth mode
- credential requirement IDs used by the adapter
- supported read, write, admin, send, publish, deploy, or destructive actions
- rate limits
- dry-run or sandbox support
- health check path
- schema or field mapping references

Validate:

- adapter loads
- adapter declares supported workflows
- adapter can run a read-only health check
- adapter refuses actions outside approved scope
- adapter can consume a runtime capability grant
- adapter writes audit events
- adapter supports dry-run when required

### 5.6 Approvals

Collect:

- bootstrap administrator reference
- domain approver role or group
- client approver role or group
- customer-subject consent or authorization path
- human approver references for high-risk work
- emergency stop owner
- revocation owner
- escalation path
- approval notification channel

Approval records should include:

- approver reference
- approval scope
- workflow or credential requirement
- expiration or review date
- evidence reference
- decision status
- timestamp

Validate:

- privileged workflows have an approval path
- high-risk workflows have a Hermes council mode
- credential requirements have approver mappings
- emergency stop and revocation owners are set
- no inferred approval is treated as approved

## 6. Runtime Binding Manifest

The self-hosted wizard should generate a non-secret manifest.

```yaml
schema_version: 1
kind: xfactory_runtime_binding_manifest

deployment:
  hosting_mode: self_hosted
  environment: <dev|test|prod>
  install_dir: <path>
  data_dir: <path>
  base_url: <url-or-localhost>

hermes:
  install_ref: <path-or-package-ref>
  profile_dir: <path>
  memory_provider_ref: <provider-ref>
  domain_layer: <domain-hermes-name>
  client_layer: <client-hermes-name>
  customer_layer: <customer-hermes-name>

omnigent:
  install_ref: <path-or-package-ref>
  domain_overlay: <path>
  workspace_root: <path>
  sandbox_mode: <mode>

secret_provider:
  type: <provider>
  vault_ref: <vault-ref>
  custody: customer

credential_bindings:
  <requirement-id>:
    provider: <provider>
    secret_ref: <secret-reference-name>
    access_mode: <delegated_oauth|workload_identity|api_key_reference>
    owner: customer
    max_grant_minutes: <minutes>

adapters:
  - id: <adapter-id>
    system: <external-system>
    endpoint_ref: <endpoint-or-tenant-ref>
    credential_requirements:
      - <requirement-id>
    dry_run_supported: true

approvals:
  bootstrap_admin_ref: <user-or-group-ref>
  high_risk_approver_refs:
    - <user-or-group-ref>
  emergency_stop_owner_ref: <user-or-group-ref>
  revocation_owner_ref: <user-or-group-ref>

validation:
  status: pending
  report_ref: <path>
```

This manifest can live in a customer-controlled runtime config area. If it is
checked into a repo, it must contain references only and pass secret scanning.

## 7. Validation Ladder

Validation should progress in levels.

```text
L0 schema_valid
  manifests parse, required fields exist

L1 local_prereqs_valid
  OS, runtime, paths, ports, package availability, permissions

L2 services_start
  Hermes and Omnigent start locally

L3 bindings_resolve
  secret references, approver references, adapter endpoints are resolvable

L4 grant_issuance_valid
  credential broker can issue and revoke a test runtime capability grant

L5 adapter_health_valid
  adapters load and pass read-only or sandbox health checks

L6 workflow_dry_run_valid
  first workflow completes without touching live state

L7 runtime_ready
  required dry-run, approvals, audit, revocation, and rollback checks pass

L8 live_ready
  live execution explicitly approved
```

Self-hosted installation should stop at the first failed level and produce a
gap report with exact next actions.

## 8. Approval Ladder

Approvals should also have levels.

```text
approval_declared
  role or group named

approval_resolvable
  role or group exists in the local identity system

approval_notified
  approver can receive requests

approval_recorded
  approver decision can be stored in Hermes audit

approval_enforced
  workflow gates block without approval

approval_revocable
  approval or grant can be cancelled
```

No live workflow should run unless the required approvals are enforced and
revocable.

## 9. Installer UX

The simple installer should feel like:

```text
Choose domain
  -> choose hosting mode
  -> connect local runtime
  -> connect vault
  -> connect systems
  -> choose approvers
  -> validate
  -> dry-run
  -> ready or gap report
```

The wizard should show each requirement as a checklist:

```text
[x] Hermes starts
[x] Omnigent starts
[x] Vault reference resolves
[ ] Microsoft 365 adapter health check
[ ] High-risk approver group
[ ] Dry-run workflow
```

Every blocked item should have:

- reason
- owner
- safe next command or UI action
- whether Opensoft can assist
- whether it blocks install, runtime, workflow, or live readiness

## 10. Self-Hosted Safety Defaults

Self-hosted defaults:

- customer owns secret custody
- reference-based manifests only
- local validation before live execution
- read-only first workflow
- dry-run before write/admin/send/publish/deploy/destructive action
- high-risk workflows use `deliberative_council`
- bootstrap admin cannot bypass domain policy
- runtime grants expire quickly
- revocation path is tested before live readiness
- support bundles redact local paths, identifiers, and logs where needed

## 11. Opensoft Assist Mode

Self-hosted does not mean Opensoft cannot help. The installer should be able to
produce a support bundle that contains:

- intake answer packet
- runtime binding manifest with references only
- validation report
- adapter health summaries
- gap report
- logs with secret redaction

The bundle must not include raw credentials, tokens, private keys, private
records, or unrestricted tenant data.

## 12. Implementation Phases

### Phase 1: Manifest And Validation

- Define runtime binding manifest schema.
- Add local secret-pattern scan.
- Add readiness-level classifier.
- Add gap report format.

### Phase 2: TUI Runtime Binding

- Add `xfactory bind-runtime`.
- Add provider selection.
- Add adapter selection.
- Add approval collection.
- Add local validation ladder.

### Phase 3: Flutter Runtime Binding

- Add the same stages to the visual installer.
- Support local-only mode.
- Support exportable support bundles.
- Support resume and retry.

### Phase 4: Provider Connectors

- Add provider-specific checks for vaults, OAuth, workload identity, and common
  adapters.
- Keep provider connectors pluggable by domain.

### Phase 5: Dry-Run Execution

- Add dry-run job envelope.
- Test runtime grant issue and revoke.
- Test audit write.
- Test adapter health.
- Test first workflow without live external changes.

## 13. Open Decisions

- Which local vault should be the default for non-production self-hosted setup?
- Should production self-hosted require a managed secret provider?
- Which identity systems should approver resolution support first?
- Which adapters should be included in the first self-hosted release?
- Should Flutter installer bundle the TUI binary or call the same core library?
- How should offline installs receive signed domain templates and adapter
  packages?
