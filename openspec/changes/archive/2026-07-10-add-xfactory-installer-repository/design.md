## Context

The top-level xFactory repository is an aggregation workspace that pins
independently released install, subsystem, and DomainxFactory repositories.
openxFactory already defines one shared intake contract with website, TUI, and
downloadable visual surfaces, but no implementation repository owns that
product family. CloudPC-Install explicitly owns workstation requirements rather
than device administration or application code, and OpsxFactory owns Intune
administration rather than a neutral public product.

The first implementation surface is a branded Windows application intended for
Microsoft Store and website distribution. Its eventual enrollment operations
cross tenant, device-owner, Microsoft Entra, Intune, Store-signing, and Graph
security boundaries, so it requires an independently versioned repository
before application development starts.

## Goals / Non-Goals

**Goals:**

- Establish one private neutral implementation repository for the xFactory
  installer product family.
- Pin an exact bootstrap release in the top-level aggregation workspace.
- Make ownership, compatibility, release, update, and rollback behavior
  machine-readable and testable.
- Preserve openxFactory, OpsxFactory, and CloudPC-Install authority boundaries.
- Provide a truthful scaffold that does not claim the WinUI or Store product is
  complete.

**Non-Goals:**

- Implementing the WinUI application, intake backend, Graph adapter, or Store
  submission in this repository-bootstrap change.
- Enrolling a live workstation or granting Intune, Entra, Graph, or Partner
  Center permissions.
- Moving the existing draft Flutter, website, or TUI plan out of openxFactory.
- Storing signing certificates, enrollment packages, bulk tokens, tenant
  credentials, or provider credentials in Git.

## Decisions

### 1. Use one private product repository

Create `opensoft/xFactory-Installer` with GitHub visibility `PRIVATE`. The
repository is the implementation home for installer surfaces, while the first
named product is `xFactory Workstation Intake`.

Alternative: create `xFactory-Workstation-Intake`. Rejected for bootstrap
because it would preclude the shared intake engine and encourage overlapping
repositories when website, CLI/TUI, or cross-platform clients are added.

### 2. Pin under the existing installs namespace

The aggregation path is `installs/xfactory-installer`. This preserves the
current top-level topology and makes the repository available in known-good
workspace assemblies without putting implementation code in xFactory itself.

Alternative: add a new top-level `apps/` namespace. Deferred until more than
one independent application repository demonstrates that a new category
removes real ambiguity.

### 3. Bootstrap boundaries before application code

The first release contains repository metadata, architecture, security,
compatibility, release documentation, and a deterministic validator. It does
not include a placeholder WinUI project that cannot be built or tested in the
current environment.

Application scaffolding is a successor feature with Windows build evidence.

### 4. Keep authority split across owning repositories

- openxFactory owns canonical intake, consent, routing, and evidence contracts.
- xFactory-Installer owns client implementation, packaging, Store metadata,
  tests, and release evidence.
- OpsxFactory owns Intune/Graph permissions, policy, deployment, compliance,
  and remediation adapters.
- CloudPC-Install owns host eligibility and required end state.
- xFactory owns only the exact submodule pin and workspace documentation.

### 5. Use explicit compatibility and release evidence

The installer repository records the compatible openxFactory repository,
change identifier, and tested commit in `compatibility/openxfactory.yaml`.
Version `0.1.0-bootstrap` is tagged after local validation. The xFactory parent
pins that tag's exact commit; it does not follow a moving branch.

### 6. Separate Store and direct-download trust

Store and direct-download metadata may live in the repository, but signing
material and Partner Center credentials MUST remain in approved external
secret stores. Direct-download and Store artifacts require separate release
evidence even if they are produced from one source revision.

## Risks / Trade-offs

- [A new repo adds release and dependency overhead] -> keep one installer
  product-family repo and use an explicit openxFactory compatibility file.
- [Private visibility conflicts with a future public download] -> repository
  visibility and binary distribution are independent; publish signed artifacts
  without exposing source until a separate approval changes visibility.
- [The bootstrap looks like a finished app] -> validator and README explicitly
  report `implementation_status: repository-bootstrap`.
- [A public package could contain tenant enrollment authority] -> prohibit
  embedded bulk tokens, Graph application secrets, and signing credentials.
- [Dirty aggregation work could be committed accidentally] -> stage only the
  new proposal, submodule entry, README lines, and exact gitlink.

## Migration Plan

1. Validate and commit this OpenSpec change independently in openxFactory.
2. Create the private GitHub repository and verify visibility through GitHub.
3. Add and validate the boundary scaffold, commit it, tag the bootstrap, and
   push branch and tag.
4. Add the repository as `installs/xfactory-installer` in xFactory.
5. Verify fresh submodule initialization, remote URL, private visibility, exact
   commit, compatibility declaration, and repository validator.
6. Commit and push only the parent integration paths.

Rollback removes the parent gitlink and `.gitmodules` entry in a dedicated
commit. The private repository and immutable bootstrap tag remain as evidence;
deleting the remote requires separate explicit authorization.

## Open Questions

- WinUI versus Flutter for the first production client remains a successor
  implementation decision; the repository boundary supports either while
  preventing two independent intake contracts.
- The Partner Center publisher identity and Store signing workflow remain
  external setup tasks and are not inferred from GitHub ownership.
