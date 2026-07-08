# Ideation Work Area

Status: draft convention — this structure is itself a brainstorm output and is
to be ratified through an OpenSpec change proposal before it becomes a shared
xFactory standard.
Repository context: openxFactory
Purpose: provide the governed pre-proposal pipeline that turns free-form
thinking into OpenSpec proposals, so prose never silently becomes (or
contradicts) policy.

## Lifecycle

```text
brainstorm/<topic>.md      free-form discussion and design exploration;
                           explicitly NON-NORMATIVE — nothing here is policy,
                           and doc-health checks ignore contradictions here
      |
      |  organize gate: pieces get identity, duplicates merge,
      |  each fragment names the spec or capability it targets
      v
staging/<topic>/           structured fragments ready for proposal drafting:
                           claim, target capability, delta type
                           (ADDED / MODIFIED / REMOVED), evidence links
      |
      |  proposal gate: the staged set is coherent and complete
      v
openspec/changes/<name>/   a normal OpenSpec change proposal; from here the
                           standard flow applies (approve -> implement ->
                           archive -> promoted specs)
```

Rules while this convention is in draft:

- Content in `brainstorm/` may contradict promoted specs freely; that is what
  the area is for. Everywhere else, prose that changes promoted policy must be
  an explicit delta (see the doc-health pipeline brainstorm).
- Moving material from `brainstorm/` to `staging/` and from `staging/` to an
  OpenSpec change are deliberate, reviewed steps — never bulk copies.
- Each DomainxFactory keeps its own `ideation/` area for domain-scoped topics;
  cross-factory and contract-level topics belong here in openxFactory.

## Contents

- [Doc Health Pipeline](brainstorm/doc-health-pipeline.md) — first captured
  design: prose-to-spec conversion rules, tagging, staging, and the nightly
  repo-health report.
- [Domain-To-Neutral Concept Promotion](brainstorm/domain-to-neutral-promotion.md)
  — lifecycle for lifting concepts born in a DomainxFactory into the neutral
  layer (and devolving them back down); companion to the doc health pipeline.
