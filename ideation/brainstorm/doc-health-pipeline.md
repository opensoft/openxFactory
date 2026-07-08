# Doc Health Pipeline — Brainstorm

Status: brainstorm
Captured: 2026-07-08 — non-normative; to be organized into staging and then
an OpenSpec proposal. Nothing in this document is policy. The lifecycle
vocabulary and ideation convention sections were organized into the
[add-document-lifecycle-vocabulary](../../openspec/changes/add-document-lifecycle-vocabulary/proposal.md)
change; the tagging, nightly report, and implementation sections remain
un-staged.
Repository context: openxFactory (contract-level, cross-factory topic)
Participants: Brett Heap, Claude (design session)

## Problem

The xFactory family has a working discipline — prose gets converted to specs,
and prose that contradicts promoted specs must be expressed as an explicit
change-from-current (an OpenSpec delta) rather than an accidental restatement —
but nothing enforces it. As of 2026-07-08 there is **no CI at all** on
xFactory, openxFactory, or any DomainxFactory: the per-repo validators only run
when someone remembers to run them locally, and no tool checks prose-vs-spec
health. (Verified: no `.github/workflows` in any family repo; only auto-enabled
Copilot workflows on three remotes; agenttower's two workflows are unrelated.)

## Existing assets to build on (not reinvent)

- `docs/knowledge-lifecycle-model.md` — named states with governed gates,
  "every transition is explicit." This pipeline is the same lifecycle applied
  to governance knowledge (ideas about the system itself).
- codexFactory `workflows/approved-intent-intake` — the downstream endpoint;
  it begins from an already-approved intent. This pipeline is everything
  upstream of it.
- The `Status:` doc-header convention — an informal, human-only version of the
  tagging rule this design makes machine-checkable.
- Per-repo validators (Medx `validate.py`, codex `validate-docs.sh`, Ops
  `validate-domain-factory.py`, omnigent-install contract validator) — the
  deterministic layer the nightly run should execute first.

## Design

### Ownership split

```text
openxFactory      owns the CONTRACT: tag syntax, ideation lifecycle states,
                  staging schema, health-report schema (domain-neutral)
codexFactory      owns the IMPLEMENTATION: action scripts, report generator,
                  agent workflows that perform doc conversion (software
                  engineering execution)
xFactory (root)   HOSTS the nightly action: the only repo pinning all
                  submodules, so whole-family health is aggregation-repo work
each domain repo  owns APPROVAL of its own content: codex workers may stage
                  and transform another factory's prose, but promotion is
                  gated by that factory's Domain Hermes — execution moves,
                  authority stays
```

codexFactory workers operate on other factories' docs because a doc change in
a git repo is engineering work product regardless of subject matter; the
owning factory's Hermes signs off on meaning, codexFactory owns branch/PR/
merge mechanics.

### Prose tagging (opt-in conversion)

Only tagged prose is converted — tagging is the human act of selection.

- Doc-level: `Status: spec-candidate` in the standard header block queues a
  whole document.
- Block-level: comment fences select passages:
  `<!-- xspec:candidate target=<spec-name> -->` ... `<!-- /xspec:candidate -->`
- Anti-restatement rule: prose that changes anything already promoted must
  carry `<!-- xspec:supersedes spec=<capability>/<requirement> -->`, making
  "this is a delta from current" machine-visible.
- The deterministic checker enforces tag hygiene (well-formed tags,
  `supersedes` targets resolve to real spec requirements, candidate aging).
  It cannot detect semantic contradiction; the agentic pass covers that.

### Ideation pipeline (per repo)

```text
ideation/brainstorm/<topic>.md   free-form; explicitly non-normative;
                                 contradictions legal here and only here
   | organize gate: identity, dedup, target-spec links
ideation/staging/<topic>/        fragments: claim, target capability,
                                 delta type (ADDED/MODIFIED/REMOVED), evidence
   | proposal gate: staged set coherent and complete
openspec/changes/<name>/         standard OpenSpec flow from here
```

Ideation stays in the repo it concerns (locality + Hermes authority).
Cross-factory topics live in openxFactory's ideation area. The brainstorm
directory being the one sanctioned home for contradicting prose is what makes
the health rule enforceable everywhere else.

### Nightly health run (xFactory root repo)

Scheduled GitHub Action, `--recurse-submodules` checkout.

1. Deterministic pass: run every repo's validators; tag hygiene; staging
   inventory and aging (a spec-candidate untouched N days is a health smell);
   submodule pin drift vs remote mains; contract-copy drift.
2. Agentic pass: LLM sweep for untagged normative prose ("must", "owns",
   "never" outside specs) and prose-vs-promoted-spec contradictions.
3. Output: dated report in `health/reports/` in the root repo PLUS a ranked
   plan — each plan item a ready-to-stage conversion task, so the report's
   output feeds the pipeline's input. Open an issue on regression.

### Bootstrapping sequence

1. Capture this design (this document). ✔
2. Iterate here until stable.
3. Organize into `ideation/staging/doc-health-pipeline/`.
4. Two OpenSpec proposals: openxFactory (contract: tags, lifecycle, report
   schema) and codexFactory (implementation workflow).
5. Build the action only after both are approved.

## Open questions (deliberately unresolved)

- Runner location: root repo hosts the workflow directly, or codexFactory owns
  a reusable workflow the root repo invokes (cleaner code ownership)?
- Ideation placement: per-repo (current lean) vs a central work area in
  codexFactory if cross-factory brainstorms dominate?
- Tag syntax: `xspec:` comment fences vs YAML frontmatter vs a sidecar index
  file per docs directory?
- Report destination: committed file, GitHub issue, both, or Hermes dashboard
  once one exists?
- Agentic pass model/runtime: which agent runs the semantic sweep, and under
  which Omnigent worker profile and credential grants?
- Aging thresholds: how long may a spec-candidate sit untouched before it
  counts against health?
