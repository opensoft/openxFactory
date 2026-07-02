# Deploy Artifacts Plan

Status: implementation plan
Repository context: openxFactory
Purpose: define the deployment artifacts needed to run the complete xFactory
stack locally and then promote it to production.

## Goal

Produce repeatable deployment artifacts for local development, self-hosted
single-node installs, and production environments. Deployment must preserve the
separation between non-secret repo contracts and customer-specific runtime
bindings.

## Artifact Set

### Local Development

- `Dockerfile` for each service:
  - Hermes API
  - openxFactory control API
  - worker gateway
  - adapter runner
  - readiness service
- `docker-compose.yml` for:
  - services
  - Postgres
  - queue or lightweight broker
  - local object/artifact store
  - local development vault emulator or reference provider
- `.env.example` with non-secret defaults and required variable names.
- `scripts/dev-up.sh`, `scripts/dev-down.sh`, and `scripts/dev-smoke.sh`.

Exit criteria:

- A fresh checkout can run `docker compose up` and pass a read-only dry-run smoke test.

### Runtime Configuration

- `runtime-binding.schema.yaml` for non-secret runtime manifests.
- `runtime-binding.example.yaml` for local development.
- Secret-provider binding examples for:
  - local development
  - Azure Key Vault
  - AWS Secrets Manager
  - GCP Secret Manager
  - 1Password or Bitwarden enterprise vault
- Adapter endpoint templates per domain.

Exit criteria:

- `xfactory validate-runtime` can reject raw secrets and unresolved required references.

### Database And State

- Postgres migration scripts.
- Seed data for local dry-run only.
- Backup and restore scripts.
- DR runbook.
- Retention and redaction policy for artifacts and audit logs.

Exit criteria:

- A local database can be created from scratch, migrated, smoke-tested, backed up, and restored.

### CI/CD

- GitHub Actions workflows for:
  - lint and schema validation
  - unit tests
  - container image build
  - vulnerability scan
  - integration smoke test
  - image publish
  - deploy to staging
- Required status checks for PR admission.
- Manual approval gate for production deploy.

Exit criteria:

- A PR cannot merge unless validation, tests, image build, and smoke tests pass.

### Production Infrastructure

Choose one initial target and keep the others as future adapters.

Recommended first target:

- Kubernetes with Helm chart:
  - deployments
  - services
  - ingress
  - config maps
  - secret references
  - persistent volumes
  - network policies
  - liveness and readiness probes
  - horizontal scaling defaults

Alternative first target:

- Terraform or Bicep for a managed Azure Container Apps deployment:
  - Container Apps environment
  - Postgres flexible server
  - Key Vault
  - Log Analytics
  - managed identity
  - private networking where needed

Exit criteria:

- A staging environment can be provisioned, deployed, validated, rolled back, and destroyed from documented commands.

### Observability

- Structured logs.
- Metrics for jobs, queue depth, adapter health, grants, revocations, approvals, dry-run success, and worker failures.
- Trace IDs from approved intent through artifacts.
- Alert rules for stuck jobs, failed grants, adapter outage, emergency stop, and audit write failure.
- Dashboard starter.

Exit criteria:

- An operator can identify why a dry-run or workflow is blocked without reading service internals.

### Release And Operations

- Release manifest mapping:
  - openxFactory commit or tag
  - Hermes install commit or package
  - Omnigent install commit or package
  - domain repo commit
  - adapter package versions
- Upgrade procedure.
- Rollback procedure.
- Support bundle generator with redaction.
- Production readiness checklist.

Exit criteria:

- A release can be pinned, deployed, verified, rolled back, and audited.

## First Delivery Order

1. Local Compose stack with Postgres and no live adapters.
2. Postgres migrations and runtime binding validation.
3. Dry-run job path for Ledgerx `bank_feed_review`.
4. Local credential broker with revocation audit.
5. Adapter health-check runner.
6. Worker gateway with isolated workspace.
7. CI build and smoke test.
8. Helm or Azure Container Apps production target.
