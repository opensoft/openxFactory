## Context

`ideation/staging/` is intended to be the queue of organized topics that have
not yet crossed the proposal gate. In practice, staged source documents remain
there after their OpenSpec changes are proposed, ratified, implemented, and
archived. The OpenSpec change records summarize that material but do not own an
exact supporting source set, so deleting the stale staging folders would break
links and lose accessible provenance.

The active proposal directory is already the canonical proposed-state home.
The design therefore extends each change directory rather than creating a
parallel `ideation/proposals/` hierarchy. It must also preserve the hybrid
NotebookLM source-return workflow and avoid placing opaque history in the
canonical `openspec/specs/` tree.

## Goals / Non-Goals

**Goals:**

- Make `ideation/staging/` accurately list only organized, unproposed work.
- Preserve proposal source provenance and Git history.
- Keep supporting documents readable while a change is active.
- Retain a deterministic, verifiable cold-storage bundle after archival.
- Preserve NotebookLM source returns through the proposed state.
- Support one-to-one and partial/one-to-many staging promotions.

**Non-Goals:**

- Moving brainstorm history automatically; brainstorm remains design history.
- Treating supporting documents as normative specification.
- Adding historical bundles to canonical `openspec/specs/`.
- Modifying the upstream OpenSpec CLI package.
- Automatically deciding which staged claims belong in a proposal.

## Decisions

1. **The active change owns proposal support.** Selected staged files move with
   `git mv` to `openspec/changes/<change-id>/supporting-docs/`. A separate
   `ideation/proposals/` tree was rejected because it would duplicate OpenSpec's
   active-change state and create another synchronization boundary.

2. **Move selected files, not necessarily the whole topic.** A transition
   command accepts a staging topic and selected paths. If all material is
   selected, the empty staging folder disappears. If unresolved material
   remains, it stays staged and the manifest records that partial promotion.

3. **Active supporting documents remain plain text.** Proposed prose changes
   to `Status: draft` and names `Proposed by: <change-id>`; immutable evidence
   remains `Status: record`. `manifest.yaml` records the source path, source
   revision, transition date, file paths and SHA-256 hashes, optional NotebookLM
   workspace id, and remaining staged paths.

4. **Archive packaging wraps, rather than replaces, OpenSpec archive.** A
   codexFactory command performs preflight checks, makes one final NotebookLM
   import an explicit operator prerequisite, writes a deterministic
   `supporting-docs.tar.gz`, leaves `supporting-docs.manifest.yaml` readable,
   removes the uncompressed folder, and then invokes the normal `openspec
   archive`. Packaging before that invocation lets OpenSpec move the complete
   record without patching upstream code.

5. **Bundles live beside archived changes.** The final path is
   `openspec/changes/archive/<date>-<change-id>/supporting-docs.tar.gz`. Binary
   bundles under `openspec/specs/` were rejected because that tree is current,
   searchable contract surface.

6. **The bundle is deterministic and verifiable.** Entries sort by path and
   use normalized timestamps, uid/gid, ownership names, and modes. The readable
   archive manifest records the bundle SHA-256 and the original per-file hashes.
   The command rejects symlinks and path traversal.

7. **Proposal-stage NotebookLM origins are first-class.** The hybrid importer
   accepts `openspec/changes/<change-id>/supporting-docs/`, writes imported
   synthesis there with `Status: draft`, and preserves idempotence/provenance.
   Evidence explicitly imported as immutable stays `record`. A final import is
   required before packaging; the hybrid retires after archive.

8. **Doc-health reports stale state rather than silently moving content.** New
   deterministic checks report staged files that cite an active/archived change,
   missing or invalid proposal manifests, staged status under active supporting
   docs, missing/mismatched archive bundles, and bundles under canonical specs.
   Transition and packaging remain explicit operator commands.

## Risks / Trade-offs

- [Compression makes supporting prose unsearchable after archive] -> keep the
  manifest readable and require accepted claims/rationale to be represented in
  proposal, design, and canonical specs before packaging.
- [Relative links break during a move] -> transition tooling scans Markdown
  links and fails if moved files leave unresolved relative targets.
- [One staging topic feeds several changes] -> support selected-file moves and
  record remaining paths instead of assuming one folder equals one proposal.
- [NotebookLM receives sources after packaging] -> require a final import in
  the archive checklist and retire the hybrid only after successful archive.
- [Changing upstream OpenSpec behavior is brittle] -> wrap the CLI and verify
  arbitrary bundle preservation with an integration fixture.
- [Historical migration rewrites many links] -> migrate one topic/change pair
  per reviewable commit and verify checksums and links before deletion.

## Migration Plan

1. Ratify the four spec deltas and document the new paths.
2. Land codexFactory transition, packaging, verification, doc-health, and
   NotebookLM support with unit/integration tests.
3. Pilot an active change without changing that change's capability scope.
4. Inventory existing staging files and map each selected file to its active or
   archived change; package completed topics and preserve unresolved fragments.
5. Update ideation indexes and all links away from removed staging paths.
6. Run repository validation and strict OpenSpec validation.

Rollback: restore moved files from Git history to their original staging paths,
remove proposal support manifests/bundles, and revert the spec delta. Canonical
spec outcomes are unaffected by supporting-document storage.

## Open Questions

- Whether a later retention policy should expire compressed support bundles
  after a fixed period; this change retains them indefinitely.
- Whether NotebookLM workspace retirement can become automated once its API
  exposes a reliable delete/retire operation.
