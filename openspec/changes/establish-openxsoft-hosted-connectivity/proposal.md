---
code_surface: none
target_release: implemented
sequenced_after: [add-private-connectivity]
---

# Proposal: Establish openXsoft.com hosted connectivity ownership

Status: ratified
Ratified: 2026-11-10 by Brett Heap. [Ratification record](review/ratification-2026-11-10.md)
Kind: proposal
Proposed: 2026-11-10

## Why

Standalone Hosted Headscale and hosted DomainxFactories need a product owner, a deployment repository, and a pilot domain owner. The [ratified policy](../add-private-connectivity/proposal.md) assigns product responsibility to openXsoft.com and leaves those implementation assignments to a successor.

## What Changes

- Propose private `opensoft/openXsoft-Hosted-Services` as the product repository for independent entitlement, managed network provisioning, factory attachments, hosted onboarding, and catalog qualification.
- Propose the maintainers of `codeXfactory/codexFactory` as the first pilot domain owner. They would sponsor a synthetic hosted profile and declare its minimum access. The live pilot requires an accountable maintainer to accept the role.
- Use two synthetic customers and the generic hosted profile to prove common onboarding. Use the codexFactory-owned profile to qualify the first named domain once its own evidence is available.
- Keep product, install, and domain responsibilities distinct and require exact approved scopes and verification for T001.

## Capabilities

### New Capabilities

- `openxsoft-hosted-connectivity-ownership` governs standalone Hosted Headscale and hosted DomainxFactory product and pilot ownership.

### Modified Capabilities

None.

## Impact

This packet proposes ownership and scope. Repository creation and executable product and domain work require approved realization records. A pilot pass qualifies the tested lab paths. Each customer-facing launch requires approval and evidence for its own profile.
