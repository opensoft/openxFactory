# Feature Specification: The hosting declaration becomes a configured value

**Feature Branch**: `031-configured-notebook-hosting-identity`
**Created**: 2026-09-08
**Status**: Draft
**Realizes**: openxFactory OpenSpec change `adopt-configured-notebook-hosting-identity`
(ratified 2026-09-08 by Brett Heap, verbatim "Ratify 783 and merge"; merged as
PR #783 → main `e7c53012`; record
`openspec/changes/adopt-configured-notebook-hosting-identity/review/ratification-2026-09-08.md`)
**Lane**: provenance-autonomous-merge

**THE RATIFIED PACKET IS THE AUTHORITY, NOT THIS FILE.** Every requirement below
traces to a task group in that packet's `tasks.md` or to one of the five rulings
OQ-A..OQ-E. Where this specification and the packet disagree, the packet wins and
this file is wrong. This spec exists to carry the packet's disposition into
Speckit's build flow, which is Brett's standing rule: OpenSpec ratifies, Speckit
builds.

## User Scenarios & Testing *(mandatory)*

The actors are an OPERATOR running the projection sync against a live NotebookLM
account, a PUBLIC CLONER who fetches the repository after it becomes public, and
a REVIEWER reading the record to check a governed act happened.

### User Story 1 - The operator keeps a governed binding while the record moves out of the public tree (Priority: P1)

An operator's install today reads its hosting declaration from one fixed path in
this repository, and the addresses in that file are the values the run compares
against the account a CLI profile is actually signed in as. The operator needs
that comparison to keep firing after the record moves to a private home.

**Why this priority**: It is the one behaviour the change must not break. An
install that stops comparing writes a governed projection into whatever account
happens to be active, which is the failure the capability was raised to retire.

**Independent Test**: Point configuration at a declaration in a temporary tree
and run the enforcement path; it binds, refuses a wrong profile, and refuses a
right profile signed in as the wrong account, exactly as it does today.

**Acceptance Scenarios**:

1. **Given** configuration naming a declaration by absolute path, **When** the
   enforcement path runs with the declared profile active, **Then** the run binds
   to that profile and reports the declared case and account.
2. **Given** configuration naming a declaration by workspace-relative path,
   **When** the enforcement path runs, **Then** the same binding is reached — the
   two spellings resolve to one file.
3. **Given** a resolved declaration whose profile is signed in as a different
   account, **When** the enforcement path runs, **Then** the run refuses and the
   refusal names both the signed-in account and the expected one.
4. **Given** a resolved live declaration, **When** the operator runs the
   validator's resolved-path mode, **Then** it validates that record and exits 0
   only if the record conforms.

### User Story 2 - A public cloner carries a shape, never an identity (Priority: P1)

Someone clones the repository after the flip. They must be able to read the
record's shape, run the validator over the shipped instance, and run the sync,
without the tree carrying a live identity for this projection and without the
clone being treated as a declared install.

**Why this priority**: It is the change's purpose. Every other requirement
serves it.

**Independent Test**: `git grep` the four convener addresses over the tree
returns nothing; the validator over the shipped instance exits 0; the sync in a
tree with no configuration reports UNDECLARED and does not break.

**Acceptance Scenarios**:

1. **Given** a clone with no configuration, **When** the sync's enforcement path
   runs, **Then** it reports NO DECLARED HOSTING IDENTITY as a transition state
   and runs under the CLI's default profile rather than failing.
2. **Given** the shipped instance, **When** the validator runs over it, **Then**
   it conforms — the shape stays gated in CI.
3. **Given** the shipped instance, **When** a reader looks for an identity in it,
   **Then** every identity-bearing value is synthetic and every actor is a role
   placeholder.
4. **Given** configuration that resolves to the shipped instance, **When** the
   sync's enforcement path runs, **Then** the run is REFUSED and the message
   names the file and the remedy — a fixture is no install's declaration.

### User Story 3 - A reviewer can still see the eight governed acts (Priority: P2)

Seven share grants and one recorded denial of 2026-08-27 discharge a ratified
obligation. A reviewer must be able to reach them, and the public tree must say
they exist without restating their values.

**Why this priority**: `document-lifecycle` forbids redacting a record of
governed acts. Losing the roster would be a worse defect than the one being
fixed, but it is not what breaks an operator's run today, so it sits below P1.

**Independent Test**: The roster moves intact into the private home, byte-for-byte
as to its eight rows; the public tree's instance carries a synthetic roster of
the same arity plus a pointer saying where the live record lives.

**Acceptance Scenarios**:

1. **Given** the live record in its private home, **When** a reviewer reads it,
   **Then** all seven grants, the denial, the approval block and the custody
   reference are present unaltered.
2. **Given** the public instance, **When** a reviewer reads it, **Then** it says a
   live roster exists and where the class of home is, and names no live value.

### Edge Cases

- **Configuration names a path that does not exist** (an uninitialized submodule,
  a machine that has not cloned the private home). Resolves to UNDECLARED, which
  the ratified requirement already defines as a non-breaking transition state.
  The packet's OQ-A table states this case and calls it correct.
- **Configuration names a directory, or an unreadable file.** Same as absent: the
  reader cannot produce a declaration, so the install is undeclared rather than
  broken. A file that IS readable but that the narrow reader cannot parse stays a
  REFUSAL, unchanged from today — an unreadable declaration is not an absent one.
- **Both the environment variable and the workspace configuration are set.** The
  environment variable wins; a one-off operator run and a CI job both need to
  override without editing a file.
- **The environment variable is set to an empty string.** Treated as unset.
- **The record marked as an example is reached through some path other than the
  shipped one** (a copy, a symlink, a worktree). The refusal is decided by the
  marker INSIDE the record, not by comparing paths, so it fires anyway.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The declaration's location MUST resolve from configuration in one
  order, shared by both readers: an environment variable, then a workspace-local
  configuration file's declared path, then UNDECLARED.
- **FR-002**: A configured path MAY be absolute or workspace-relative, and both
  spellings MUST resolve to the same file.
- **FR-003**: Absent configuration MUST be UNDECLARED — reported as not meeting
  the requirement, never as a third legitimate case, and never breaking a run.
- **FR-004**: The shipped instance MUST NOT be a declaration source. The resolver
  MUST NOT fall back to it.
- **FR-005**: A configured path that resolves to a record marked as an example
  MUST be REFUSED rather than bound, and the refusal MUST name what was found,
  why it is refused, and the remedy.
- **FR-006**: The refusal of FR-005 MUST be decidable by the sync's existing
  dependency-free reader — no YAML dependency may be introduced, and no path
  comparison may be relied on.
- **FR-007**: The enforcement path's comparisons, refusals and messages MUST be
  unchanged; only the place the record is read from changes.
- **FR-008**: The validator MUST accept an explicit path first, then the resolver,
  then the shipped instance AS A FIXTURE, and MUST offer one scriptable mode that
  validates the RESOLVED path so an operator has a single command.
- **FR-009**: The shipped instance MUST carry no live identity: the hosting
  account, the account a completed migration names, every roster user and hosting
  account, the denial's row, and every actor name MUST be synthetic.
- **FR-010**: The shipped instance MUST keep the live record's SHAPE — same keys,
  same order, same comment structure, same roster arity — so a fixture that
  drifted in shape cannot stop proving the shape.
- **FR-011**: The shipped instance MUST carry its example marker as a FIELD the
  narrow reader parses, not as a comment.
- **FR-012**: Every test fixture literal that mirrors a live identity MUST become
  synthetic, and every negative mutation MUST keep firing for its stated reason.
- **FR-013**: The conformance check the split costs MUST be replaced, not lost:
  the shipped instance's conformance stays gated in CI, a resolved declaration's
  validation is proved over a synthetic record, and the live record's conformance
  becomes a named operator command.
- **FR-014**: The workspace configuration file MUST be gitignored and MUST state
  in its own header that it is per-machine and carries no secret.
- **FR-015**: `git grep` over this repository for the four convener addresses MUST
  return nothing once the whole realization has landed, including the archive act
  that promotes the delta.
- **FR-016**: No commit, message, test name, comment or pull-request body produced
  by this feature may reprint one of those four addresses.

### Key Entities

- **Hosting declaration** — the record naming which Google identity hosts an
  install's projection, its CLI profile, its migration history, its custody
  reference by binding, its approval designation, its share-out roster and its
  recorded denials. After this feature there are TWO instances of it: one
  synthetic and public, one live and private.
- **Workspace configuration** — a small per-machine, uncommitted file whose one
  job is to name where the live declaration is. It carries a path and no secret.
- **The example marker** — one field inside a record that says "this instance is a
  fixture". It is what the refusal reads.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A search of the public tree for the four convener addresses returns
  zero lines.
- **SC-002**: An operator with configuration in place reaches the same binding
  decision as before the change in every case the existing suite covers — proved
  by the existing tests passing with their assertions unaltered.
- **SC-003**: A clone with no configuration completes a sync run and reports
  itself undeclared; it does not fail and it does not bind to a fixture.
- **SC-004**: Pointing configuration at the shipped fixture fails the run with a
  message that names the file and the remedy.
- **SC-005**: The repository's conformance coverage does not fall: the number of
  automatic conformance assertions over a hosting record rises by at least the
  four the resolver owes, and none is added skipped.
- **SC-006**: A reviewer can enumerate all eight governed acts of 2026-08-27 from
  the live record's new home, unaltered.

## Assumptions

- **A-1**: The live record's private home is hermes-install
  `config/clients/opensoft/notebook-projection-hosting.yaml`. This is not an
  assumption of this feature's making — it is OQ-A, ruled 2026-09-08.
- **A-2**: The move itself is an OPERATOR act in a private repository, performed
  on Brett Heap's word (packet `tasks.md` Group 5). This feature PREPARES it and
  does not perform it.
- **A-3**: The Q1/Q3 docs pull request has landed (PR #786, merged
  2026-09-08T12:28Z, main `e8021fed`), so this feature's structural rewrite of
  `docs/lifecycle-notebook-projection.md` does not race its redactions. Verified
  rather than assumed — packet task 0.3.
- **A-4**: The promoted spec text moves into
  `openspec/specs/lifecycle-notebook-projection/spec.md` BY THE ARCHIVE ACT and
  never by hand (packet task 1.1). This feature therefore leaves the promoted
  spec alone, and SC-001 is reached only when the archive lands — which is why
  FR-015 says "including the archive act".
- **A-5**: The role-placeholder spellings for actors follow the ones already in
  the corpus after PR #786.
