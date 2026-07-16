# Client-Infrastructure Examples

Status: draft

Reference examples for the two `client-infrastructure` contract schemas under
`contracts/schemas/` (`add-client-infrastructure-liaison` change, task 2.3):

- `xfactory-client-infrastructure-request.schema.yaml`
  (`client_infrastructure_request`)
- `xfactory-infrastructure-readiness-result.schema.yaml`
  (`infrastructure_readiness_result`)

These are static reference material, not runtime state — instance records live
in client installs (credential-contracts residency model; see `../README.md`).
All content uses synthetic Southside Clinic orgs from the change's
`supporting-docs/southside-operating-model-scenarios.md`. No real
organizations, and no secret values (a secret's *shape*, where one must be
shown, uses the bounded `SENTINEL_` forms from
`contracts/avatar-client/redaction/sentinels.yaml`).

`scripts/validate-client-infrastructure.py` self-tests every file here on each
run: every `*.example.yaml` must validate and pass all deterministic checks;
every file under `negative/` must fail, and specifically for its intended
reason.

## Layout

```text
client-infrastructure/
├── README.md                                     # this index
├── request-client-managed.example.yaml           # client_managed binding, NO OpsxFactory reference
├── request-opsxfactory-executed.example.yaml      # opsxfactory_executed, WITH handoff, completed (readiness-gated)
├── request-managed-host.example.yaml             # managed_host binding, host-scoped grant ref
├── readiness-result-ready.example.yaml           # infrastructure_readiness_result gating the opsx request
└── negative/                                      # one violation per file
    ├── embedded-secret-value.yaml                 # secret value in a field
    ├── subject-id-in-authority-field.yaml         # subject id in approval.authority_ref
    ├── actor-equals-authority.yaml                # execution actor == approval authority
    ├── liaison-marks-completed.yaml               # illegal transition (liaison certifies completion)
    ├── completed-without-fresh-readiness.yaml     # completion with no fresh readiness result
    ├── escalation-as-state.yaml                   # escalation modeled as a status value
    ├── terminal-mutation.yaml                     # transition out of a terminal state
    ├── digestless-package-ref.yaml                # package_refs entry without a digest
    └── cancellation-with-unacknowledged-children.yaml  # cancelled + handoff, no child_acks
```

## Schema → example map

| Schema | Valid example(s) | Negative example(s) |
| --- | --- | --- |
| `xfactory-client-infrastructure-request.schema.yaml` | `request-client-managed`, `request-opsxfactory-executed`, `request-managed-host` | `embedded-secret-value`, `subject-id-in-authority-field`, `actor-equals-authority`, `liaison-marks-completed`, `completed-without-fresh-readiness`, `escalation-as-state`, `terminal-mutation`, `digestless-package-ref`, `cancellation-with-unacknowledged-children` |
| `xfactory-infrastructure-readiness-result.schema.yaml` | `readiness-result-ready` | (readiness shape is exercised as the completion gate for the opsx request) |
