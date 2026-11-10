# Design: openXsoft.com hosted connectivity ownership

Status: draft

## Context

The authenticated GitHub lookup returned 404 for the proposed hosted product slug. `codeXfactory/codexFactory` exists and is recorded in the [estate inventory](../../../scripts/estate-repository-inventory.yaml) and [domain regression inventory](../../../contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml). Its engineering domain is a candidate for a synthetic, non-clinical pilot. The proposed maintainer role does not imply acceptance.

## Decisions

| T001 key | Owner and proposed scope | Release and verification |
| --- | --- | --- |
| hosted_product | Proposed private `opensoft/openXsoft-Hosted-Services`, default branch `main`. Seed scope `README.md`, `SECURITY.md`, `docs/ownership.md`, and `Makefile`. Proposed runtime scope `services/entitlement/`, `services/network-provisioning/`, `services/factory-onboarding/`, `services/catalog/`, `tests/qualification/`, and `release/`. | Independent non-production product candidate with approved contract and install pins. Proposed `make validate` and `make test` interfaces. Bootstrap must establish working entry points and review controls before T001 accepts them. |
| hosted_domain | Proposed `codeXfactory/codexFactory` maintainers. Scope `profiles/hosted/private-connectivity.yaml` and `tests/private_connectivity/` for a synthetic domain profile and evidence. | Exact hosted profile revision and approval, pinned to the tested candidate. Proposed `python3 -m pytest tests/private_connectivity -q` plus the domain's repository gates. |

A standalone subscription can exist without a factory. Managed operations are authorized per customer and boundary. Provisioning and attachment retries reconcile the original operation. Factory cancellation revokes the affected attachment and leaves independent entitlement intact. Network termination requires separate authority.

Hosted onboarding supports new and existing managed networks and installations that require no binding. Verify private reachability and application authorization independently. Keep private services outside public ingress. Catalog admission requires current evidence for the exact domain profile revision.

## Risks and trade-offs

Use synthetic data and non-production infrastructure for the first pilot. A generic profile verifies shared onboarding. A domain-specific release requires that domain's own evidence and approval. The hosted product owner must confirm whether to bootstrap the proposed repository or use an existing approved repository.

## Migration and verification

Approve the product owner and repository choice, bootstrap and inventory route if needed, and the accountable pilot domain maintainer. Record exact owner scopes, release targets and verification commands for T001. Require the qualified install interface and approved lab. Run G1 for standalone entitlement and isolation, G3 for hosted onboarding, and G4 for the expansion decision.
