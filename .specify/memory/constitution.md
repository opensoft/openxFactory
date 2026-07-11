<!--
Sync Impact Report
- Version change: (template) → 1.0.0 (initial adoption)
- Modified principles: n/a (initial adoption)
- Added sections: Core Principles (I–VII), Repository Constraints,
  Development Workflow & Quality Gates, Governance
- Removed sections: none
- Templates requiring updates:
  ✅ .specify/templates/plan-template.md — generic Constitution Check gate
     resolves against this file; no edits required
  ✅ .specify/templates/spec-template.md — no constitution-mandated sections
     beyond the stock template; no edits required
  ✅ .specify/templates/tasks-template.md — validation-gate tasks are covered
     by Principle V; no edits required
- Follow-up TODOs: land the retroactive `adopt-project-constitution` OpenSpec
  change to back the ratified status claim (until then Status stays draft)
-->

# openxFactory Constitution

Status: draft
Kind: process
Adoption note: adopted for project bootstrap on 2026-07-11 with user approval;
the `ratified` status claim awaits a retroactive OpenSpec change
(planned: `adopt-project-constitution`) per the document-lifecycle standard.

## Core Principles

### I. Contract-First, Domain-Neutral Core

openxFactory owns only domain-neutral contracts, schemas, templates,
registries, and validators. Domain interpretation lives exclusively in
DomainxFactory repositories, which pin the openxFactory version they consume
in their `stack.yaml`. No domain-specific behavior, vocabulary, or policy may
land in this repository; domain-to-neutral promotion runs through the
candidate register and the promotion process, never through direct edits.
Rationale: the layer model (Hermes → xFactory → DomainxFactory → Omnigent)
only holds if the neutral layer stays neutral.

### II. Governed Change Flow: OpenSpec Before Implementation

Any change to product behavior, architecture, artifact contracts, boundaries,
or governance policy MUST go through an OpenSpec change before implementation.
A change realizes per the promoted release-realization spec: doc-only changes
(`code_surface: none`) archive when their artifacts land, with no Speckit
feature; changes whose OpenSpec tasks are directly executable MAY realize
through that task list; larger changes decompose into one or more Speckit
features (`specs/NNN-*`). Where Speckit features exist, OpenSpec records
governance decisions and handoff while Speckit owns the implementation tasks,
without duplicating task lists. Proposals declare
`code_surface:` and `target_release:`; a change with a code surface archives
only on merged, green realization evidence. Small implementation-only fixes
within an already-governed feature may skip OpenSpec.

### III. Document Lifecycle and Status Discipline

Every governance document carries a controlled `Status:` header from the
canonical taxonomy (`brainstorm | staged | draft | ratified | standard |
superseded | retired | record`) and moves along the lifecycle spine defined in
`docs/document-lifecycle.md`. No document may claim `standard` status unless a
promoted OpenSpec spec or canonical contract backs the claim; `ratified`
headers MUST name the approving change; `superseded` headers MUST name the
successor. Contradiction is legal only in `ideation/brainstorm/`. Every
transition is a deliberate, reviewable step — never a silent status edit.

### IV. Schema and Artifact Discipline

Every YAML artifact carries `schema_version` and `kind`. `.template.yaml` and
`.example.yaml` files are instantiation stubs, never live configuration. New
documents MUST be linked into the README document index of this repository.
Raw credentials MUST never be stored anywhere in the tree — grant and binding
templates only. Committed files MUST NOT contain host-absolute paths; use
repo-relative paths or runtime resolution.

### V. Validation Gates (NON-NEGOTIABLE)

Before any commit is pushed: the affected repo-local validators
(`scripts/validate-*.py`) MUST pass, and OpenSpec artifacts MUST pass
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict`. Doc-health findings
are classified auto-fixable or contested; a contested finding is resolved only
by a cited OpenSpec change or a recorded disposition, never by silent edits.
Implementation features MUST prove behavior with deterministic, reviewable
evidence (tests, fixtures, validator output) rather than assertion.

### VI. Versioned, Content-Addressed Releases

A contract release is identified by five coordinated values: per-file
`contract_schema_version`, `contract_bundle_version` in
`contracts/manifest.yaml`, an annotated `contract-v<major>.<minor>` tag, the
exact release commit with per-file SHA-256 digests, and a matching
`contracts/CHANGELOG.md` entry. Manifest, changelog, and contract files change
atomically; the tag points at that realized commit; version numbers are
allocated at realization, never reserved in proposals. Consumers pin the exact
commit and digests — a movable branch or tag is not a compatibility pin.
Additive changes are minor; breaking changes increment the schema major and
require migration notes.

### VII. Fail-Closed Authority Boundaries

Registries of capabilities, outcomes, purposes, and states are closed:
unrecognized values are rejected, and deferred features fail closed rather
than degrade open. Model or agent output is non-authoritative — it proposes;
disposition belongs to the owning human gate or governed authority. Committed
evidence MUST be redacted: no credentials, raw provider payloads, tenant data,
or high-cardinality identifiers. Authority claims not backed by a promoted
spec or ratified change are defects.

## Repository Constraints

- Shared-tree discipline: multiple sessions share the root checkout. Stage
  explicit paths only (never `git add -A`); verify the current branch with
  `git status -sb` before every commit; pushes race, so pull --rebase and
  retry.
- Speckit features use worktree checkout mode: each feature gets an isolated
  sibling worktree under `../openxFactory-worktrees/` created by the git
  extension; follow-on lifecycle commands run from that worktree, never the
  root checkout.
- This repository is a submodule of the `opensoft/xFactory` aggregation repo:
  commit here first, then update the aggregation pin in a separate sync
  commit.
- Runtime code is out of scope except governed reference implementations and
  validators explicitly ratified by an OpenSpec change; nothing here deploys,
  listens on a socket, or holds provider keys.

## Development Workflow and Quality Gates

- Lifecycle per feature: specify → clarify → plan (Constitution Check gate) →
  checklist → tasks → analyze → implement, run from the feature worktree.
- Clarifications are recorded in the feature's clarification file and encoded
  into `spec.md`; material ambiguities MUST be resolved before planning.
- `/speckit.analyze` MUST report no critical findings before implementation
  begins; analyze findings are dispositioned, not ignored.
- Merges to `main` require the Principle V gates green on the feature branch
  and a review pass; parallel features touching shared release metadata
  serialize their final integration commits.
- Commits are scoped and explicit; generated evidence lands with the change
  that produced it.

## Governance

This constitution supersedes other process descriptions in this repository
for development workflow; repo-local documents remain authoritative for
product facts and domain content. Amendments are made through an OpenSpec
change that edits this file, with a semantic version bump: MAJOR for removed
or redefined principles, MINOR for new or materially expanded principles or
sections, PATCH for clarifications. Compliance is checked at every plan-phase
Constitution Check and every `/speckit.analyze` run; violations require an
explicit Complexity Tracking justification or a constitution amendment. For
day-to-day guidance see `README.md`, `docs/document-lifecycle.md`, and
`docs/contract-versioning-policy.md`.

**Version**: 1.0.0 | **Adopted**: 2026-07-11 (ratification pending an OpenSpec change) | **Last Amended**: 2026-07-11
