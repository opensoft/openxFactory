# Tasks: Add private connectivity

Status: draft

The checklist covers governance and handoff. Each approved successor uses Speckit for its implementation checklist and records its own validation and release evidence.

## 1. Review and ratification

- [ ] 1.1 Review the local and hosted offering matrix, customer isolation, network ownership, and the independent subscription lifecycle against the proposal and spec.
- [ ] 1.2 Record ratification of the reviewed packet. At filing, generate the corpus ledger row using the actual pull request number and the repository's ledger seeder.

## 2. Prepare successor handoffs

- [ ] 2.1 Define the openxFactory runtime binding handoff, covering local install and connect-existing flows, managed network selection, scoped approval and enrollment, and compatibility for existing installs.
- [ ] 2.2 Define the install and operations handoff, covering repository ownership, local packaging, managed provisioning, customer isolation, policy enforcement, revocation, upgrades, and restore.
- [ ] 2.3 Define the openXsoft.com product handoff, covering standalone entitlement, factory attachment and detachment, hosted DomainxFactory onboarding, and per-domain release readiness.

## 3. Agree on pilot acceptance

- [ ] 3.1 Identify owners and a pilot environment for the local Headscale, standalone Hosted Headscale, local factory with Hosted Headscale, and hosted DomainxFactory paths.
- [ ] 3.2 Assign the verification evidence for cross-customer denial, approved access, replay and retry behavior, revocation, recovery, and migration rollback. Link that plan from the implementation handoffs.

## 4. Promote the approved policy

- [ ] 4.1 After landing and completion of the governance checklist, archive the packet through the repository's OpenSpec workflow and link the resulting requirements from the successor records.
