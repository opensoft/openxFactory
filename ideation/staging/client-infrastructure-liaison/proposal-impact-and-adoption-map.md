# Client Infrastructure Liaison Proposal Impact And Adoption Map

Status: staged
Kind: plan
Repository context: openxFactory
Staging ID: openxFactory:staging:client-infrastructure-liaison
Target capabilities: `client-infrastructure-liaison` (ADDED),
`client-infrastructure-request` (ADDED), and
`roles-authority-model` (MODIFIED)

## Locked Decisions

- The liaison is a Client Hermes coordination capability with one accountable
  owner, composed from existing roles.
- The infrastructure request is a durable artifact separate from the neutral
  job envelope.
- Subjects, actors, authorities, organizations, capabilities, and grants use
  distinct reference fields.
- Deadline and escalation are conditions/events, not terminal request states.
- Completion requires a fresh readiness result.
- The liaison never receives tenant-admin authority merely because it owns the
  coordination record.
- An out-of-band recovery path is required when the managed dependency hosts
  any part of its own control plane.

## Neutral Artifact Impact

| Surface | Proposed delta |
|---|---|
| `openspec/specs/client-infrastructure-liaison/` | new capability requirements |
| `openspec/specs/client-infrastructure-request/` | new request, transition, evidence, and readiness requirements |
| `openspec/specs/roles-authority-model/` | coordination versus privileged execution boundary |
| `docs/client-hermes-product-service-scaffold.md` | liaison capability and composition across existing roles |
| Client Hermes templates | accountable owner, operator binding, contacts, channels, validation, and out-of-band path |
| Contracts/schemas | request, condition/event, handoff acknowledgment, and readiness result schemas |
| Validators | state transitions, secret rejection, immutable package digests, completion/readiness checks |
| Examples | customer-managed, managed-host, OpsxFactory, failure, cancellation, and recovery |

The neutral job-envelope schema is referenced but not modified merely to store
the infrastructure request. A later job may carry the request correlation ID.

## Domain Adoption

| Domain | Required adoption |
|---|---|
| OpsxFactory | execution binding, service-request correlation, readiness producer, privileged gate mapping |
| MedxFactory | Care Infrastructure Liaison alias, protected-data fallback rules, Omni dependency profiles |
| LedgerxFactory | Firm Infrastructure Liaison alias and financial-system dependency profiles |
| AdxFactory | Marketing Infrastructure Liaison alias and campaign/platform dependency profiles |
| codexFactory | Engineering Infrastructure Liaison alias and build/runner dependency profiles |

The capability defaults to configured-but-inactive when a client installation
has no external infrastructure dependencies. It becomes activation-blocking
when a declared component requires an external operator.

## Proposal Sequence

1. OpsxFactory `refine-opsx-service-subject-model` settles domain-owned names,
   subject taxonomy, graph, persistence, and migration.
2. openxFactory `add-client-infrastructure-liaison` ratifies the neutral
   coordination capability and request/readiness contracts.
3. Domain adoption changes bind OpsxFactory execution and add domain-specific
   liaison aliases, requirement profiles, and fallback policy.

This sequence avoids a circular dependency and a cross-repository mega-change.

## Proposal Gate Checklist

- staging files move into proposal `supporting-docs/` with manifest and origin;
- requirements distinguish request artifacts from job envelopes;
- every transition has actor, guard, and evidence requirements;
- role overlap with the existing Client Hermes scaffold is explicit;
- schemas reject embedded secrets and mutable package references;
- out-of-band recovery is tested;
- adoption responsibilities name each repository; and
- code surfaces and target release are declared by the proposal.
