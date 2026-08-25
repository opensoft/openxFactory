# Project and Subject Hermes Overview — Brainstorm

Status: brainstorm
Kind: reference
Summary: Project Hermes is proposed as one governed subject instance created
from a type template and carrying its own identity, scope, consent,
acceptance, roles, memory, and lifecycle.
Topics: project, project-hermes, subject-hermes, project-type-template
Repository context: openxFactory neutral Project/Customer Hermes layer
Captured: 2026-07-28

## Possible feats

- **Project/Subject Hermes contract** — define provisioning inputs, stable
  subject identity, authority, consent, acceptance, and lifecycle records.

## Motivation

Domain and company policy cannot substitute for the identity, goals,
acceptance, consent, and history of one customer, project, or person-subject.
Creating each instance ad hoc makes authority and memory boundaries unstable.

## Goals

- Provision a stable subject identity from a governed archetype.
- Bind one request to one project or subject scope.
- Keep project acceptance and subject consent explicit.
- Coordinate project roles with domain and client authorities.
- Separate authoritative tenant discovery from workstation preferences.

## Non-goals

- A project template does not grant tenant membership.
- A workstation cache does not authorize live operations.
- Project Hermes does not own reusable domain policy.
- This packet does not choose one database or UI.

## What the system delivers

Each project or subject gains a versioned layer containing identity, scope,
acceptance, consent, role assignments, private memory bindings, journey
state, and repository composition references.

## System model

```text
approved project type + tenant-authorized project record
  → provision subject identity and layer
  → bind roles, scope, consent, repositories, acceptance
  → seed Hermes and execute single-subject requests
  → record outcomes and lifecycle changes
```

## Cluster map

- [Project Provisioning and Subject Authority](project-synthesis-provisioning-and-authority.md)
  — joins archetype defaults, subject authority, and catalog boundaries.

## How it fits

The project layer narrows Domain and Client Hermes content. The tenant catalog
supports discovery and assignment, while the memory gateway controls private
recall. Speckit or another implementation workflow may realize an accepted
project change but does not define subject authority.

## Key decisions and open questions

Open choices include the first supported subject kinds, template exception
rules, lifecycle ownership, repository-composition approval, and how person
consent differs from ordinary project authorization.

## Document map

### Synthesis

- [Project Provisioning and Subject Authority](project-synthesis-provisioning-and-authority.md)

### Atomic explorations

- [Project/Subject Layer Scaffold](project-layer-scaffold.md)
- [Project-Type Template Library](project-type-template-library-draft.md)

### Related source

- [Tenant Project Catalog and Workstation Projection](tenant-project-catalog-and-workstation-cache.md)
