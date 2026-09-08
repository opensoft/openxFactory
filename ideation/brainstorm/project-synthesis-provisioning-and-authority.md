# Synthesis: Project Provisioning and Subject Authority — Brainstorm

Status: brainstorm
Kind: architecture
Summary: A project-layer scaffold and project-type template library can
provision a bounded subject layer while leaving tenant discovery and live
authorization to the company runtime.
Topics: project, project-hermes, project-type-template, subject, synthesis
Repository context: openxFactory Project/Customer Hermes exploration
Captured: 2026-07-28

## Possible feats

- **Project Hermes provisioner** — instantiate identity, scope, acceptance,
  consent, roles, defaults, and repository bindings from an approved
  project type.

## Members and their joints

Atomic members:
[Project/Subject Layer Scaffold](project-layer-scaffold.md)
and [Project-Type Template Library](project-type-template-library-draft.md).

Related source:
[Tenant Project Catalog and Workstation Projection](tenant-project-catalog-and-workstation-cache.md).

### Templates seed defaults, not authority

The template library supplies expected practices, workflows, and role
defaults. Provisioning binds those defaults to one subject identity and
records explicit project decisions and exceptions.

### The project layer owns acceptance

Project roles govern scope, subject consent, acceptance, and journey state.
Domain and client layers provide reusable policy and constraints but do not
silently decide project outcomes.

### Catalog discovery remains separate

The tenant catalog may reveal which projects a principal can discover or is
assigned to. Each governed request still selects exactly one subject scope,
and live authorization is not inferred from a local cache or template.

## Emergent behavior

The factory can create consistent project subjects quickly while preserving
distinct identity, consent, acceptance, and authority for every instance.

## Tensions to hold

- Templates improve consistency but can hide assumptions inappropriate for a
  specific project.
- Relaxed spike defaults need quarantine rather than silent inheritance
  violations.
- Multi-project discovery must not become cross-project execution scope.

## Recombination opportunities

Project instances consume the
[Client Hermes packet](client-overview.md), the
[Hermes runtime packet](hermes-overview.md), and the
[memory and retrieval packet](memory-retrieval-overview.md).

## Open questions

- Which template fields are defaults versus mandatory constraints?
- Who approves repository composition changes after provisioning?
- How are subject consent and project lifecycle transitions synchronized?
