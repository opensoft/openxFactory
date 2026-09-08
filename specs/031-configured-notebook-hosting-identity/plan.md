# Implementation Plan: The hosting declaration becomes a configured value

**Branch**: `031-configured-notebook-hosting-identity` | **Date**: 2026-09-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/031-configured-notebook-hosting-identity/spec.md`
**Realizes**: `openspec/changes/adopt-configured-notebook-hosting-identity/` (ratified 2026-09-08)
**Lane**: provenance-autonomous-merge

## Summary

Split one file into two: a synthetic instance stays public as the shape's example
and the validator's fixture; the live record moves intact to a private home and is
resolved from configuration. Both readers learn ONE resolution order; the
enforcement path's comparisons and messages do not move; the conformance check the
split costs is replaced by three things rather than lost.

## Technical Context

**Language/Version**: Python 3.12 (the repository's own scripts and tests)
**Primary Dependencies**: none added. `scripts/sync-notebooklm-books.py` carries
NO YAML dependency and this plan must not introduce one — the refusal that reads
the example marker is therefore decided by the existing narrow scalar reader.
`scripts/validate-notebook-projection-hosting.py` already imports `yaml` and keeps
it.
**Storage**: two YAML records (one public and synthetic, one private and live) plus
one uncommitted per-machine configuration file.
**Testing**: `python3 -m pytest tests/notebooklm tests/doc-health tests/sequenced_after -q`,
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict`,
`python3 scripts/doc-health.py --single-repo .`, and a `git grep` sweep for the
four convener addresses.
**Target Platform**: developer and operator workstations; GitHub Actions
(`pytest-suite`, doc-health).
**Project Type**: single repository, script + validator + tests + governed records.
**Performance Goals**: none. The resolver runs once per process and costs a stat
and at most one small file read.
**Constraints**:
- The enforcement path's five steps, its comparisons and every refusal message stay
  byte-identical in meaning (FR-007).
- Standard library only in the sync (FR-006).
- No commit, test name, comment or message may reprint one of the four addresses
  (FR-016) — which is also why the packet's own delta cannot use the reserved
  `Removed from canon by` marker.
**Scale/Scope**: five files carrying forty lines at the packet's measurement; two
scripts gaining a resolver; one shipped record rewritten; three test modules'
fixture literals; two documents' structural sections.

## Constitution Check

This repository's governing rules for a change of this shape, and how the plan
meets each:

| Rule | How this plan satisfies it |
| --- | --- |
| OpenSpec ratifies, Speckit builds (Brett's standing rule) | The packet is ratified and merged; this feature performs no governance act and asks for no ratification. |
| Promoted canon moves only through a delta, applied by the archive act | The promoted spec is NOT edited here. Packet task 1.1. |
| The reserved `Removed from canon by` marker is unavailable | It would reprint the address inside the delta that removes it; the delta's header paragraph is the declared substitute (packet task 1.3, `design.md` § 4). Nothing in this plan adds the marker. |
| Every validator stays meaningful | The eight questions the validator asks are all shape properties or equalities between two of the record's own fields, so synthetic literals satisfy and violate each exactly as real ones did (`design.md` § 2.3). Every negative mutation is kept. |
| A record of governed acts is never redacted | The roster MOVES intact (OQ-E). The public instance gets a synthetic roster of the same arity plus a pointer. |
| Shared-tree discipline | Explicit pathspecs on every stage and commit; no `git add -A`; no bare `git commit`; no stash; no force-push. |
| Rule 6 (landing window) | This feature's pull request touches `openspec/changes/` (the tasks.md ticks), so the lane posts LANDING/LANDED at merge. |

**No constitution violation is claimed or requested.**

## Project Structure

### Documentation (this feature)

```text
specs/031-configured-notebook-hosting-identity/
├── plan.md              # this file
├── spec.md              # the feature specification
├── tasks.md             # the ordered build
├── quickstart.md        # how an operator configures and proves a binding
├── research.md          # what the code actually does today, read rather than described
└── checklists/
    └── requirements.md  # spec quality gate
```

### Source Code (repository root)

```text
scripts/
├── sync-notebooklm-books.py                     # resolver + example refusal
└── validate-notebook-projection-hosting.py      # precedence + --resolved

examples/
└── notebook-projection-hosting.yaml             # becomes the SYNTHETIC instance

tests/notebooklm/
├── test_nlm_auth.py                             # 2 literals
├── test_sync_notebooklm_books.py                # 11 literals + resolver tests
└── test_validate_hosting.py                     # 8 literals + resolved-path test

docs/
├── lifecycle-notebook-projection.md             # § The declaration, § The approval lane
├── notebook-projection-migration-runbook.md     # path references that now resolve differently
└── notebooklm-sync-open-item.md                 # same

.gitignore                                       # the workspace configuration file
openspec/changes/adopt-configured-notebook-hosting-identity/tasks.md   # ticks
```

**Structure Decision**: single project. Nothing is added to `contracts/`: the
record is deliberately not a `contracts/` member (nothing pins it, no other
repository consumes it), so no digest set moves, no `contract_bundle_version` is
spent and no release tag is owed. Measured by the packet against
`contract-v3.4.digests.yaml`'s 283 entries by exact path.

## The resolution order, once

```text
hosting_declaration_path(workspace_root) ->
  1. $XFACTORY_NOTEBOOK_HOSTING_DECLARATION   absolute, or workspace-relative
  2. <workspace>/.xfactory/notebook-hosting.yaml  ->  declaration_path:
  3. nothing                                  ->  UNDECLARED
```

Three properties, each chosen against a named alternative (`design.md` § 2.1,
D-1/D-2):

- **The shipped example is not step 3.** Defaulting to it would make every fresh
  clone declare an install it is not.
- **Absent configuration is UNDECLARED**, the transition state the requirement
  already defines, reported as unmet and non-breaking.
- **A configured path resolving to the example REFUSES**, decided by the marker
  inside the record rather than by comparing paths that symlinks and worktrees
  make unreliable.

**A configured path that does not exist resolves to UNDECLARED.** This is not a
new judgement: the packet's OQ-A table states the case ("a checkout without the
submodule initialized reads as UNDECLARED — which is correct, and is why that
state must stay non-breaking") and this plan implements what it says.

## Ordering, and where this plan deviates from the packet's literal wording

The packet's `tasks.md` states one load-bearing order: Group 2 lands green BEFORE
Group 5 (the operator move), and Group 5 before Group 3 (the public instance goes
synthetic). Its purpose is stated: no window in which an install cannot bind.

**This feature ships Groups 2, 3 and 4 in ONE pull request, and the ordering
property is preserved by the MERGE SEQUENCE rather than by two merges.** The
sequence, which belongs in the pull-request body and not only here:

1. The hermes-install pull request merges — the live record is in its private home.
2. Brett writes `.xfactory/notebook-hosting.yaml` naming that path. The old code
   ignores that file, so writing it early is inert.
3. This pull request merges. Before it, the sync reads the committed live record
   through the old constant and binds; after it, the resolver reads the private
   record and binds. **There is no unbound window at all** — which the two-merge
   order would actually open, because a landed resolver with no configuration yet
   written is undeclared until the operator acts.
4. Brett runs packet 5.2's proof and 5.4's gate.
5. A separate archive pull request promotes the delta and empties the address
   sweep.

The deviation is declared rather than taken quietly. If Brett prefers the literal
two-merge order, the split point is clean: Groups 2 and 4 in one pull request,
Group 3 and the documents in a second.

## Complexity Tracking

| Item | Why it is not simpler | Rejected alternative |
| --- | --- | --- |
| Two records instead of one edit | The addresses are the values an equality test compares against a live Google account, and eight lines are the record of eight governed acts. Redacting in place disarms a guard and falsifies a record. | Placeholders in the one committed file — rejected in the packet's § Why. |
| An example marker as a FIELD | The refusal must be decidable by a reader that carries no YAML dependency. A comment is invisible to it; a filename is not read at all. | Renaming to `.example.yaml` — measured at twenty-one references across eight files for a signal the resolver cannot read (OQ-C). |
| Three replacements for one lost check | The live record cannot be checked by this repository's CI without publishing it. | Accepting the loss with a note — rejected as D-5: an unchecked live declaration is how the original defect arrived. |
