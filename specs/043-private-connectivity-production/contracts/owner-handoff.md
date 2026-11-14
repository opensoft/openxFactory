# Planned owner and execution handoff

Status: draft
Created: 2026-11-13
Feature: [043-private-connectivity-production](../spec.md)

This feature-local document proposes acceptance obligations. It is not a supported public contract, a new record kind, a file allowlist or a deployment grant.

## Commissioning input and output

Input is the ratified policy plus the owner scope proposal, intended consumed platform/domain choices, support/release needs and governing authority. C-01 records the accepted human owner, canonical repository/revision, exact code/CI/schema/test surfaces, verification commands, allowed effects, exclusions and validity. A candidate directory in owner-scopes.md is not accepted scope.

Output is only a current bounded commissioning decision. Missing approval or a required owning OpenSpec decision blocks dependent implementation. C-02 platform selection precedes provider-specific implementation; actual domain selection precedes domain-specific work.

## Owner release handoff

A producer emits supported artifact/provenance and exact candidate content/revision references, compatibility/support matrix and verification output for its accepted scope. It does not acquire a standing deployed write credential or grant consumer eligibility.

Neutral publication follows the existing release cut and tag verification process. Consumer pin changes follow owner approval and verified published content. Release publication, integration acceptance, target execution and customer activation remain separate.

## Managed-subject execution handoff

Reuse client_infrastructure_request and existing managing-factory intake, execution binding, approvals, custody, correlation and readiness mechanisms. Environment changes approval depth, not executor. All approvals required by the target's current production workflow remain required.

A channel needing a deployment grant uses a valid request-scoped grant and closes/revokes it on completion. A reviewed merge into the managing factory's governed configuration tree, applied by pull reconciliation, requires no additional push credential. Existing AKS-specific minting is not a universal provider API or a platform decision.

Preserve current correlation carriers supported by the selected channel, including existing Xfactory-Correlation-Id / Xfactory-Request-Ref Git trailers and applicable target/registry metadata. The correlation audit joins collected observations with accepted requests/dispositions; it does not collect live state or pass Q acceptance.

Executor completion projects to validation_pending in the inspected Ops flow. Trusted readiness and observed qualification remain necessary.

## Unmanaged customer operation

Current authorized customer operation and required consent govern an unmanaged local target. Do not manufacture a managing-factory request/grant for it. Its staging/canary, monitoring, support and commercial decisions remain required for their own approved scope.

## Acceptance and failure obligations

Every handoff verifies customer/environment/target/candidate scope and current validity before effects and activation. Unknown scope, changed retry inputs, expired authority and unapproved drift fail closed. Preserve immutable original subjects and cleanup references across retries/restarts.

Owner source tests/CI prove their declared class only. Required suite wiring is explicit; no generic green job is evidence of an uncollected private suite. Failed, partial or uncertain effects remain unready and are reconciled under current bounded authority.

Changes to these semantics or new executable readers require the owning governance process. This document supplies planning input, not its approval.
