# Document Catalog Adoption Guide

Status: draft
Kind: process
Repository context: openxFactory
Proposed by: add-document-cataloging
Purpose: give an adopting DomainxFactory one place to see what it owns when
the active `add-document-cataloging` change's external document catalog
reaches its repository, entirely by reference to that change's spec.

## Scope

This guide is additive orientation for a DomainxFactory maintainer, not a new
contract of its own. Every rule it points to is owned by the
`add-document-cataloging` change's
[document-cataloging spec](../openspec/changes/add-document-cataloging/specs/document-cataloging/spec.md);
this guide only names which requirement to read and which files in your own
repository that requirement applies to. Until that change promotes, treat
every reference below as proposed, not ratified — the same caveat the two
neutral contracts it touches already carry (see
[Document Lifecycle](document-lifecycle.md#catalog-tags-are-not-lifecycle-state)
and [Doc-Health Contract](doc-health.md#check-families)).

## What an adopting DomainxFactory owns

### 1. Your namespaced tag registry

Your repository owns one namespaced registry file at
`catalog/document-tag-registry.yaml`, validated against
[`xfactory-document-tag-registry.schema.yaml`](../contracts/schemas/xfactory-document-tag-registry.schema.yaml).
The spec's *Controlled classification facets and provenance* requirement is
what actually defines the namespace-ownership rule (a registry may declare
tags only inside namespaces it owns), the effective-registry merge across
every pinned repository, and what makes a namespace or tag claim invalid —
read that requirement before adding your first tag. `scripts/apply-domain-
starter.py` seeds new domains with an empty stub of this file (one owned
namespace declared, zero tags); filling it in with real tags is domain
implementation work, not starter work.

### 2. Owner-override authority and review duties

Your Domain Hermes is the reviewing authority for classifications on your
domain-owned documents. The spec's *External catalog application and
disposition authority* requirement is what assigns that authority and
describes how a `reviewed` or `overridden` disposition is recorded, cited,
and later invalidated by a content change. Overrides you record live only in
your own repository at `catalog/document-tag-overrides.yaml` (schema:
[`xfactory-document-tag-overrides.schema.yaml`](../contracts/schemas/xfactory-document-tag-overrides.schema.yaml))
and are never authored on the aggregation side. The starter does not seed
this file — create it the first time your Domain Hermes dispositions a
classification.

### 3. Protected-evidence handling

If any of your documents carry handling policy that restricts what may leave
your repository, the spec's *Bounded cataloger execution and protected
evidence* requirement is what governs dispatch gating, opaque locators, and
output-policy filtering for that content — read it before assuming a
sensitive document can be classified centrally at all. Nothing in your
repository needs to change for this protection to apply; it is derived from
your existing source-declared handling policy.

### 4. Classification-aging expectations

The spec's *Full baseline and incremental refresh* requirement is what sets
the pending-classification aging thresholds that your unreviewed or
newly-invalidated classifications are measured against once cataloging runs
against your repository. Reviewing a pending classification before it ages is
a Domain Hermes review duty; aging out on its own does not dispose it.

## What this guide does not grant

Nothing in this guide, and no value your registry or override files ever
record, assigns document ownership, lifecycle status, promotion, access,
handling policy, approval, or routing state. That boundary belongs to the
spec's *External catalog application and disposition authority* and
*Lifecycle and xspec marker exclusion* requirements, not to this guide.

## Related Documents

- [document-cataloging spec](../openspec/changes/add-document-cataloging/specs/document-cataloging/spec.md)
  — the owned vocabulary, provenance, and disposition-authority rules this
  guide only points into.
- [Document Lifecycle](document-lifecycle.md) — the lifecycle spine catalog
  values never move a document through.
- [Doc-Health Contract](doc-health.md) — the deterministic `document-catalog`
  check family your registry and override files feed.
- [`xfactory-document-tag-registry.schema.yaml`](../contracts/schemas/xfactory-document-tag-registry.schema.yaml)
  and
  [`xfactory-document-tag-overrides.schema.yaml`](../contracts/schemas/xfactory-document-tag-overrides.schema.yaml)
  — the schemas your two owned files validate against.
- [`examples/document-cataloging/`](../examples/document-cataloging/) — worked
  valid and invalid examples for both file shapes.
