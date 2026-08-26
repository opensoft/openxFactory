# Implementation Plan: split-openxwallet-repo §1 bookkeeping

**Branch**: `016-openxwallet-split-bookkeeping` | **Date**: 2026-08-26 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/016-openxwallet-split-bookkeeping/spec.md`

## Summary

Realize the three open tasks of `openspec/changes/split-openxwallet-repo/tasks.md`
§1 — the ratified change's own diff — plus one stale-text correction in its
ledger. Nothing here is designed: every text is quoted verbatim in the ratified
`proposal.md` (merged at `5ef6d8d2`, PR opensoft/openxFactory#391), so the work
is transcription against a fixed source plus recorded evidence.

Three edits across two repositories, and no code:

1. **openxFactory `docs/openxdox-naming.md`** — append `## Amendment 2 —
   openXwallet leaves the exception list (2026-08-26)` after Amendment 1, in
   Amendment 1's shape; rewrite the § Decision inline pointer at `:23-25` so its
   sentence stays grammatical with one exception named instead of two (task 1.11).
2. **xFactory (aggregation) `CLAUDE.md`** — replace § "Working rules" item 1 with
   the proposal's verbatim replacement text, delivered as an open PR against
   `opensoft/xFactory` (task 1.12).
3. **openxFactory `openspec/changes/split-openxwallet-repo/tasks.md` §1** — fix
   task 1.1's stale trailing `` `Status: draft`. ``, tick 1.10 with the
   measurement's real evidence, and tick 1.11/1.12 with file + commit/PR notes
   (tasks 1.1, 1.10, and the ticks for 1.11/1.12).

The one substantive judgment call is task 1.10's. Its measurement was already
performed and is **not** unconditionally green: the packet's landing produced
exactly one new doc-health finding, on a staged topic outside 1.10's stated scope
of "this change directory or the README entry". The plan ticks 1.10 with an
evidence note that names that finding rather than asserting a bare green, and
does not remedy it — the remedy is a lifecycle act on a staged topic that §1 does
not authorize.

## Technical Context

**Language/Version**: N/A — Markdown governance documents only. No source code
is added, changed, or deleted by this feature.

**Primary Dependencies**: `openspec` CLI (strict validation);
`scripts/doc-health.py` (openxFactory's in-repo checker); `git`; `gh` CLI for the
two pull requests.

**Storage**: N/A — files in two git repositories.

**Testing**: There is no code surface, so there are no unit tests. Verification
is (a) a byte-level diff of each written text against the corresponding block
quoted in the ratified `proposal.md`, (b)
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, and (c) a differential
`python3 scripts/doc-health.py --single-repo .` finding count against the feature
branch's base commit.

**Target Platform**: N/A (documentation).

**Project Type**: Governance documentation change spanning two repositories —
openxFactory (the neutral repo, this worktree) and `opensoft/xFactory` (the
aggregation superproject, a separate worktree).

**Performance Goals**: N/A.

**Constraints**:

- **The ratified text is the specification.** Where this feature's judgment
  differs from the text quoted in `proposal.md`, the quoted text wins. Improving
  the wording is a defect, not a contribution.
- **Amend, never rewrite.** No sentence of `docs/openxdox-naming.md` that
  predates Amendment 2 may be deleted or reworded, and the lifecycle header must
  stay byte-identical.
- **Exactly one ratification citation line.** `docs/document-lifecycle.md`
  § Status Claim Rules forbids a second citation line in a `ratified` header, so
  Amendment 2 adds no `Amended:`, `Ratified:` or second `Ratified by:` line.
  This matches Amendment 1's precedent, which changed no header line.
- **Shared-checkout discipline.** Neither
  `/home/brett/projects/xFactory/openxFactory` nor
  `/home/brett/projects/xFactory` may be edited in place; both edits are made in
  dedicated worktrees, staged by explicit pathspec, and committed with an
  explicit pathspec so no other session's staged work is swept in.
- **Case sensitivity.** `openXwallet` (brand), `openxwallet` (wire label) and
  `openxWallet` (retired spelling) all appear legitimately. Every substitution is
  case-sensitive and site-specific; no global replace.
- **Neither PR is merged.** Both are governance edits behind a human merge gate.
- **Successors are out of scope.** No box in `tasks.md` §2–§12 is ticked and no
  successor's text changes.

**Scale/Scope**: 3 files changed across 2 repositories; 2 pull requests; ~35
lines added to the naming record, 3 lines replaced in the aggregation `CLAUDE.md`,
~4 task lines edited in the ledger.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design — see
Post-Design Re-Check below.*

| Principle | Gate | Assessment |
|-----------|------|------------|
| **I. Contract-First, Domain-Neutral Core** | No domain-specific behavior, vocabulary or policy lands in openxFactory | **PASS.** Both edits are domain-neutral naming and placement doctrine. Notably, the working-rule amendment *strengthens* this principle's second half by making "domain repos never author neutral contracts" explicit where the old text left it implicit in an absolute that is about to become false. |
| **II. Governed Change Flow: OpenSpec Before Implementation** | Governance/boundary change runs through OpenSpec first | **PASS.** `split-openxwallet-repo` was ratified 2026-08-26 and merged at `5ef6d8d2`. This feature is the Speckit build vehicle for its §1, per the constitution's "larger changes decompose into one or more Speckit features" clause and the house rule that OpenSpec ratifies and Speckit builds. No new governance decision is taken here. |
| **III. Document Lifecycle and Status Discipline** | Controlled `Status:`; `ratified` names its change; no silent status edits | **PASS, and it is the point of the feature.** The target record keeps `Status: ratified` with its single existing `Ratified by:` citation. Amendment 2 is a dated, reviewable section, not a silent edit — the precise defect the principle exists to prevent, and precisely what the un-amended record currently commits by contradicting a ratified ruling. |
| **IV. Schema and Artifact Discipline** | `schema_version`/`kind` on YAML; new docs in the README index; no host-absolute paths in committed files | **PASS.** No YAML is touched. No *new* document is created in openxFactory's doc tree, so the README index rule does not fire (FR-014's expected outcome is no README edit). Committed prose uses repository-relative paths only. |
| **V. Validation Gates (NON-NEGOTIABLE)** | Repo validators pass; `openspec validate --all --strict` passes; contested findings resolved only by cited change or recorded disposition | **PASS with a named condition.** Both gates are run before commit. The one pre-existing `contested` finding the packet introduced is **not** silently edited away: it is recorded in task 1.10's evidence note with its family, path and class. That is the principle's own remedy for a contested finding — a citation, not a quiet fix. |
| **VI. Versioned, Content-Addressed Releases** | Contract release coordinates change atomically | **N/A.** No contract file, manifest row, digest, tag or changelog entry is touched. `contracts/` is untouched; the byte-identity floor at `wallet-v1.0` is a §3 concern. |
| **VII. Fail-Closed Authority Boundaries** | Closed registries; model output non-authoritative; evidence redacted | **PASS.** Authority for every text is the ratified proposal, not this agent's judgment — the strongest available form of "model output proposes, the human gate disposes", since the disposition already happened. No credentials, payloads or tenant data appear in the evidence. |
| **Repository Constraints** | Shared-tree discipline; feature worktrees under `../openxFactory-worktrees/`; submodule-first then aggregation pin | **PASS, with one deliberate deviation.** The feature runs from `../openxFactory-worktrees/016-openxwallet-split-bookkeeping`. The aggregation edit is `CLAUDE.md`-only — root-tracked, not a submodule pin — so the "commit in the submodule, then sync the pin" sequence does not apply; there is no pin to move. Both repos are edited in dedicated worktrees. |
| **Development Workflow and Quality Gates** | specify → clarify → plan → tasks → implement; material ambiguities resolved before planning; merges need Principle V green plus review | **PASS.** The flow was followed in order. Clarify found no material ambiguity, correctly: every text is ratified and quoted, so a clarification round could only invite deviation from a settled source. Both PRs are left open for the human review pass. |

**Gate result: PASS — no violations, so Complexity Tracking is not filled in.**

## Project Structure

### Documentation (this feature)

```text
specs/016-openxwallet-split-bookkeeping/
├── plan.md              # This file (/speckit-plan output)
├── spec.md              # /speckit-specify output
├── research.md          # Phase 0 output — the verbatim source texts, located
├── data-model.md        # Phase 1 output — the four edit sites as entities
├── quickstart.md        # Phase 1 output — how to verify the three edits
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

No `contracts/` directory: this feature exposes no API, CLI, schema or grammar.
Its "interface" is the prose of two governance documents, and the authoritative
statement of that prose already exists in the ratified proposal. A contracts
directory restating it would be a third copy to drift.

### Files changed (the two repositories)

```text
openxFactory  (worktree: ../openxFactory-worktrees/016-openxwallet-split-bookkeeping,
               branch 016-openxwallet-split-bookkeeping, base origin/main 5ef6d8d2)
├── docs/openxdox-naming.md                                  # task 1.11 (a) + (b)
├── openspec/changes/split-openxwallet-repo/tasks.md          # tasks 1.1, 1.10, ticks
└── specs/016-openxwallet-split-bookkeeping/*                 # this feature's artifacts

xFactory  (worktree: /home/brett/projects/xFactory-worktrees/openxwallet-working-rule,
           branch change/openxwallet-working-rule, base origin/main)
└── CLAUDE.md                                                # task 1.12 — item 1 only
```

**Structure Decision**: Two independent single-file governance edits plus one
ledger update, in two repositories, delivered as two pull requests. They are
sequenced ledger-last (the ledger records the other two), but the first two are
otherwise independent and neither blocks the other — matching the spec's two P1
user stories, either of which delivers value alone.

## Phase 0 — Research

See [research.md](./research.md). No `NEEDS CLARIFICATION` markers existed to
resolve; Phase 0's real work was **locating and pinning the source texts** so the
implementation is a transcription with a checkable origin, and establishing the
doc-health baseline that task 1.10's evidence note depends on. Findings:

- Amendment 2's body, the inline-pointer replacement, and the working-rule
  replacement are each quoted in full in `proposal.md` § "What this change
  RATIFIES" items 4 and 5. Line references recorded in research.md.
- Amendment 1's shape precedent, and the header rule that makes "add no citation
  line" the correct treatment.
- The doc-health differential: pre-packet `5ef6d8d2^1` vs post-packet
  `5ef6d8d2`, and the single new finding that distinguishes them.
- `docs/openxdox-naming.md` contains exactly **one** occurrence of the string
  `openxWallet` (line 24), which bounds edit (b) to a single site.

## Phase 1 — Design & Contracts

- [data-model.md](./data-model.md) — the four edit sites as entities, with their
  before-state, after-state, authority citation and invariants.
- [quickstart.md](./quickstart.md) — the verification runbook: how a reviewer
  proves each edit matches its ratified source and that the gates are green.
- `contracts/` — intentionally absent (see Project Structure above).

### Post-Design Re-Check (Constitution)

Re-evaluated after Phase 1. **Still PASS, unchanged.** The design added no new
document to openxFactory's doc tree (Principle IV's README-index rule stays
un-triggered), introduced no YAML, no contract-release coordinate, and no code
surface; it did not weaken any validation gate; and it converted the one place a
gate is not unconditionally green (task 1.10) into a recorded, cited evidence
note rather than a silent pass — which is what Principle V requires of a
contested finding. Design did not create any Complexity Tracking entry.

## Complexity Tracking

> Not applicable — Constitution Check returned PASS with no violations.
