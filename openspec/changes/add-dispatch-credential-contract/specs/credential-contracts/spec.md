## ADDED Requirements

### Requirement: Dispatch-only credential least privilege and serving-tier separation
A dispatch-only credential — one that exists to TRIGGER execution (a workflow dispatch or job kickoff) — SHALL be scoped to exactly the minimal permission required to trigger its one named target and nothing more (for a GitHub-hosted factory, `actions: write` on the single repository that owns the workflow), carrying no repository-contents authority. It SHALL be a DISTINCT binding from any content-write credential the same capability uses, and a zero-write-authority serving surface holding a dispatch-only credential MUST NOT hold — nor hold key material capable of minting — a content-write credential.

#### Scenario: A dispatch credential requests contents authority
- **WHEN** a dispatch-only credential requirement or binding grants repository-contents write, or any scope beyond triggering its one named target
- **THEN** the validator MUST report an error

#### Scenario: A dispatch credential reuses the content credential's identity
- **WHEN** a dispatch binding names the same App or key identity as a content-write binding
- **THEN** it MUST be rejected, because the serving tier would then hold key material capable of minting a content-write token

#### Scenario: A correctly separated dispatch credential
- **WHEN** a dispatch-only credential is scoped to trigger exactly one named workflow on one repository, held as a binding distinct from the content-write credential
- **THEN** it is valid

### Requirement: Reference-delivered credential with operator-as-binding
A runtime credential an install materializes SHALL be delivered BY REFERENCE — a
vault URI plus the runtime's own fetch identity — and materialized EPHEMERALLY,
named at call time and never baked into an image, committed config, or log. The
vault OPERATOR SHALL be a per-install execution binding rather than a fixed
party: the licensed operator when the tenant licenses one (for example
OpsxFactory), or the client's own IT channel when self-hosted, where no
operator-domain identity performs the privileged change. The neutral contract —
reference shape, fetch-identity requirement, ephemeral materialization, and
audit-by-vault-log — SHALL live in openxFactory and MUST NOT be an
operator-domain capability, so a domain licensed WITHOUT the operator can still
realize it; the serving and lane code SHALL be identical across bindings, with
the vault URI and fetch identity riding as bindings.

#### Scenario: A credential value is baked into an image or config
- **WHEN** a credential contract materializes a secret value into a container image, committed config, or log instead of by vault reference at call time
- **THEN** repository policy MUST reject it

#### Scenario: The operator is fixed to one domain
- **WHEN** a credential contract requires a specific operator domain as the only permissible vault operator
- **THEN** it MUST be rejected, because the operator is a per-install binding and a self-hosted client's IT channel is an equally valid operator

#### Scenario: The neutral contract is authored in an operator domain
- **WHEN** the reference-delivery credential contract is authored in an operator DomainxFactory rather than openxFactory
- **THEN** it MUST be relocated to openxFactory, so a domain licensed without the operator still reaches the contract
