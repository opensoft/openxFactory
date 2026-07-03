# xFactory Memory Gateway Examples

These examples show how DomainxFactories can bind memory and expert knowledge
providers without making any provider the authority boundary.

The examples are intentionally non-secret. Provider endpoints, account IDs, and
credential references are placeholders or broker references only.

Key files:

- `gbrain-provider-profile.yaml`, `honcho-provider-profile.yaml`,
  `agentmemory-provider-profile.yaml`, and
  `local-postgres-provider-profile.yaml` show customer-memory provider roles.
- `expert-provider-profiles.yaml` shows root-truth, vector, source workspace,
  case-pattern, playbook, and evaluation-memory provider roles.
- `provider-bindings.example.yaml` and `provider-mappings.example.yaml` show
  custody, grants, route scope, and canonical-to-provider traceability.
- `hermes-memory-gateway-config.example.yaml` and
  `xfactory-memory-tool-surface.example.yaml` show Hermes/Omnigent callers how
  governed memory calls route through `xfactory.memory.*`.
- `conformance-fixtures.yaml` is the gateway rail fixture catalog.
- Smoke files show Hermes and Omnigent calling `xfactory.memory.*` rather than
  providers directly.
