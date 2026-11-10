# Specification Quality Checklist: Private connectivity for DomainxFactory

**Purpose**: Review the shared specification and the three delivery tracks before planning.

**Created**: 2026-11-10

**Feature**: [Private connectivity](../spec.md)

## Content Quality

- [x] Requirements describe observable behavior. Headscale and openXsoft.com are named product constraints. Framework, interface, and infrastructure choices belong to planning.
- [x] Scenarios describe outcomes for customers, factory operators, and service operators.
- [x] User scenarios, requirements, and measurable success criteria are present in the shared specification and each track.

## Requirement Completeness

- [x] The local track covers new and existing customer-operated Headscale and a local factory with managed connectivity.
- [x] The standalone track covers provisioning without a factory subscription, later attachment, isolation, revocation, and recovery.
- [x] The hosted factory track covers new and existing managed networks, per-domain readiness, and private endpoint and application authorization checks.
- [x] Edge cases include partial failure and retry, expired and replayed credentials, endpoint migration, and rollback.
- [x] The specs identify ownership and tie each track to the ratified requirements. Planning decisions and separate runtime authorizations are explicit.

## Feature Readiness

- [x] Each primary journey can be exercised independently using synthetic customers and installations.
- [x] Each track specifies observable pass and fail outcomes. The pilot covers all four offering paths and checks the boundary between two customers.
- [x] Relative links, the feature pointer, and requirement and success identifiers passed a local consistency check.

## Notes

The specs are ready for planning. Pilot domains, hosting platform and region, identity and relay arrangements, and operating windows are planning inputs. Operational tests are acceptance criteria for successor work.
