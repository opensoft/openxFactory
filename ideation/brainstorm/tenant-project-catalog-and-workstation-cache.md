# Tenant Project Catalog and Engineer Workstation Projection — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Defines the boundary between a company-scoped codexFactory project
catalog and its engineer-workstation projection. The deployed company runtime
is authoritative for projects, repository composition, and principal access;
the workstation keeps only a tenant- and principal-scoped cache plus local
preferences in native operating-system config, state, and cache locations.
Topics: project, tenant-project-catalog, project-register, project-hermes,
principal-project-projection, engineer-project-assignment, project-manifest,
workstation-cache, ideation-dashboard, codexfactory, runtime-plane,
feat-request
Repository context: openxFactory (neutral contract; codexFactory and Hermes
Install realize the runtime; workBenches and workbenches-setup are the first
multi-repository consumer)
Captured: 2026-07-27

## Possible feats

- **ADDED `tenant-project-catalog`** — a company runtime's authoritative
  catalog of projects and each project's repository composition.
- **ADDED `principal-project-projection`** — the projects a signed-in
  principal may discover and the assigned subset shown as "My Projects".
- **ADDED `project-manifest` contract** — a portable, repository-owned
  description that can propose a project's identity and repository topology
  without granting access.
- **ADDED `workstation-project-cache` contract** — an authenticated,
  tenant-scoped, replaceable local projection with freshness and integrity
  metadata.
- **MODIFIED runtime dashboard adapter** — a future runtime-plane successor
  that consumes the catalog while preserving the current dashboard's
  repository/ref snapshot seam.

## Why this is a separate capability

A deployed codexFactory installation serves a company, such as Company Y.
That company has a set of projects, and one engineer can be entitled to many
of them while actively working on only a subset. The runtime therefore needs
to answer two related but different questions:

1. Which company projects may this principal discover?
2. Which of those are this principal's assigned or selected projects?

The existing `project-register.yaml` contract answers neither question. It is
an aggregation/developer-workspace navigation aid: it describes repositories
available in a checkout and intentionally carries no runtime authorization.
The current `add-dashboard-repo-selector` change is similarly a development
plane selector over generated repository snapshots. Its proposal explicitly
excludes the runtime plane.

codexFactory already has the right runtime subject boundary: a tenant/client
Hermes layer serves the engineering organization, while each Customer/Project
Hermes layer serves one project. What is missing is the catalog and assignment
relationship that lets a principal discover and select one of those project
subjects.

This should become a separate successor proposal. Expanding
`add-dashboard-repo-selector` would conflate a read-only development snapshot
roster with tenant authorization and runtime state.

## Conceptual model

```text
Company Y codexFactory runtime
├── tenant project catalog                         authoritative
│   ├── Project A
│   │   ├── primary repository
│   │   └── supporting repositories
│   ├── Project B
│   └── Project C
├── principal access and assignments               authoritative
│   └── Engineer 1 → discover A, B, C; assigned A, C
└── catalog projection API
    └── authenticated sync
        └── engineer workstation                   derived
            ├── Company Projects → A, B, C
            ├── My Projects → A, C
            └── recent/favorite choices            local preference
```

An engineer may be entitled to several projects, but every governed request
still selects exactly one Project Hermes scope. Multi-project entitlement must
not become an implicit cross-project read.

## Vocabulary and relationships

| Term | Meaning |
|---|---|
| Tenant/company | The engineering organization served by one Client Hermes layer. |
| Project | A governed subject served by one Customer/Project Hermes layer. |
| Repository | A source or document repository participating in a project. A project may contain more than one. |
| Principal | The authenticated engineer or service identity. |
| Project grant | Server-side authorization to discover or operate in a project. |
| Project assignment | A server-side working relationship used to derive "My Projects"; it never broadens a grant. |
| Preference | A recent, favorite, or locally pinned project choice; it never grants access. |

The exact meaning of "all company projects" must be tenant policy:

- if the company makes its full catalog discoverable, **Company Projects**
  contains every active project;
- otherwise it contains every project the principal is authorized to
  discover.

**My Projects** is a filtered projection of that visible set, not a second
catalog. The first contract should define whether it means formal assignment,
membership, explicit pinning, or a combination. Favorites and recents should
remain visually distinct from assignments.

## Authority and storage

| Information | Authority | Notes |
|---|---|---|
| Company project identity and lifecycle | Deployed codexFactory data store | Tenant-scoped runtime state. |
| Project-to-repository composition | Deployed codexFactory data store | May be imported from an approved project manifest. |
| Principal grants and assignments | Deployed identity/authorization plane | Never inferred from a checkout or local cache. |
| Portable project definition | Primary repository `.xfactory/project.yaml` | Descriptive input only; no user grants or credentials. |
| Developer checkout navigation | Aggregation-owned `project-register.yaml` | Development convenience, not runtime authority. |
| Workstation project list | Tenant/principal-scoped cache | Replaceable projection with revision, digest, and freshness. |
| Recents, favorites, checkout locations | Workstation state/preferences | Local UX state that cannot broaden server authority. |
| Authentication material | OS secure credential store | Never written to the project manifest or catalog cache. |

### Portable project manifest sketch

The primary repository may publish a portable description such as:

```yaml
schema_version: 1
kind: xfactory-project
id: workbenches
display_name: workBenches
primary_repository: github.com/opensoft/workBenches
repositories:
  - repository: github.com/opensoft/workBenches
    role: control-plane
    document_roots: [docs]
  - repository: github.com/opensoft/workbenches-images
    role: foundational-images
  - repository: github.com/opensoft/workbenches-setup
    role: workstation-installer
```

The manifest is a proposal/import source. Registering it into Company Y must
be an authenticated, auditable company action. Committing the file cannot
create a project, add a member, or grant repository access.

### Runtime record sketch

The neutral contract likely needs records equivalent to:

```text
projects
project_repositories
principal_project_grants
principal_project_assignments
principal_project_preferences          optional server sync
tenant_catalog_revisions
```

The physical database design belongs to the codexFactory realization. The
neutral contract should specify identities, tenancy, lifecycle, revisions,
and authorization behavior rather than prescribing a database engine.

## Workstation xFactory home

The logical local home should be named `xfactory` consistently, but Windows
and WSL/Linux should use their native directory conventions instead of one
literal `~/.xFactory` directory.

| Purpose | Windows | WSL/Linux |
|---|---|---|
| Configuration | `%APPDATA%\Opensoft\xFactory\config.yaml` | `~/.config/opensoft/xfactory/config.yaml` |
| Durable local state | `%LOCALAPPDATA%\Opensoft\xFactory\state\` | `~/.local/state/opensoft/xfactory/` |
| Replaceable project cache | `%LOCALAPPDATA%\Opensoft\xFactory\cache\projects\` | `~/.cache/opensoft/xfactory/projects/` |
| Credentials | Windows Credential Manager or another OS secure store | A supported keyring/credential broker |

Configuration identifies company endpoints and the active tenant. Durable
state may hold checkout mappings, last selection, and sync status. The cache
holds the fetched project projection. Raw access tokens, refresh tokens,
company grants, and repository credentials do not belong in these files.

Each cached tenant projection should carry at least:

```yaml
tenant_id: company-y
principal_id: engineer-1
catalog_revision: 184
content_digest: sha256:...
generated_at: 2026-07-27T15:00:00Z
synced_at: 2026-07-27T15:00:03Z
```

The concrete format may be signed JSON or SQLite. The contract matters more
than the serialization: the cache is scoped, integrity-checkable, atomically
replaceable, and visibly stale when it cannot be refreshed.

## Sync and offline behavior

```text
authenticate principal
  → fetch visible project catalog and My Projects projection
  → validate tenant, principal, schema, revision, and digest
  → atomically replace the last-known-good cache
  → preserve local recents/favorites that still reference visible projects
  → render freshness and any stale/offline state
```

On refresh failure, the client may show the last-known-good cache for
navigation, but it must display that it is stale. A cached grant must never
authorize a live operation after the server denies or revokes it; every live
project action is authorized by the runtime.

## Windows and WSL ownership

A Windows xFactory application and its WSL tooling must not silently maintain
two competing project catalogs. The installation needs one cache owner and a
defined bridge:

- the Windows application may own authentication and catalog sync, then expose
  a local broker/API or a deliberate derived projection to WSL; or
- the WSL client may own sync, with Windows consuming its broker/API.

Sharing one writable database directly across Windows and WSL filesystems is
not the preferred default because locking, permissions, and lifecycle can
diverge. The cache owner and broker protocol remain an explicit design
decision for the Windows setup application.

## Dashboard projection

The runtime dashboard can present:

- **Company Projects** — the principal's tenant-policy-visible catalog;
- **My Projects** — assigned projects within that visible catalog;
- **Favorites** and **Recent** — preference views, clearly labeled as such;
- one selected project whose repository snapshots retain repository, ref,
  source revision, and generated-at provenance.

This composes with the repository/ref seam from
`add-dashboard-repo-selector`; it does not replace provenance or flatten a
multi-repository project into an untraceable document pile.

## Security and tenancy invariants

- Every catalog, cache, lookup, and assignment is explicitly tenant-scoped.
- Project listing and project-content authorization are separate decisions.
- A principal's access to several projects never creates a cross-project
  request scope.
- A repository manifest and local checkout never grant membership.
- Cached state is a usability projection, not an authorization token.
- Credentials stay in a secure credential provider and out of source,
  manifests, caches, logs, and container images.
- Project removal or access revocation must disappear on the next successful
  sync and be enforced immediately by every live operation.

## Relationship to workBenches

workBenches is a useful first multi-repository consumer:

- `workBenches` can publish the project manifest after this contract is
  accepted;
- its manifest can name the control plane, foundational images,
  `workbenches-setup`, and independently owned bench repositories;
- `workbenches-setup` can configure the company endpoint, initiate
  authentication, create native config/state/cache locations, perform the
  first sync, and report sync health;
- neither repository owns the Company Y catalog, principal assignments, or
  credentials.

The workBenches pre-proposal pack records only this consumer dependency. The
neutral project-catalog behavior belongs here and later in its own xFactory
proposal.

## Boundaries and non-goals

- This brainstorm does not implement a catalog, database, login flow, or
  Windows/WSL broker.
- It does not authorize importing a project manifest into a live tenant.
- It does not move runtime membership into Git.
- It does not extend the current development-plane repository selector.
- It does not define organization-wide project visibility policy.
- It does not decide whether personal projects outside a company tenant join
  the same catalog in a later version.

## Dependencies and sequencing

1. Land the current development-plane `add-dashboard-repo-selector` seam
   independently.
2. Ratify the Customer/Project Hermes subject identity and provisioning
   contract.
3. Decide the visibility, assignment, preference, and Windows/WSL ownership
   questions below.
4. Raise a separate OpenSpec proposal for the tenant catalog, principal
   projection, manifest, and workstation-cache contracts.
5. Realize the server catalog and workstation client in codexFactory/Hermes
   Install.
6. Adopt the accepted manifest and setup integration in workBenches.

## Open questions

1. Are all active company projects discoverable, or only projects for which a
   principal has an explicit grant?
2. Does "My Projects" mean assignment, team membership, an explicit pin, or a
   defined union with separate labels?
3. Will a later version combine company projects and personal projects, or
   keep them as separate tenants/accounts?
4. Is the offline projection signed JSON, SQLite, or another format?
5. Does the Windows application or the WSL client own catalog sync, and what
   broker contract joins them?
6. Are favorites and recents local-only, or optionally synchronized by the
   company runtime?
7. Who may import or approve a repository's `.xfactory/project.yaml`, and how
   are later manifest changes reconciled?
8. What retention and deletion behavior is required when a tenant is removed
   from a workstation?

## Exit path

Keep this artifact as a brainstorm until the open questions have explicit
answers. Then stage the chosen vocabulary, authority model, cache contract,
and dashboard projection as one topic before generating a separate OpenSpec
proposal. No runtime or installer implementation should treat this document
as accepted authority.
