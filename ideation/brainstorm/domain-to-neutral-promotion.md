# Domain-To-Neutral Concept Promotion — Brainstorm

Status: staged
Kind: architecture
Summary: Sketches the trigger signals and lifecycle for promoting a
domain-born concept into a neutral openxFactory contract (and devolving it
back), so promotions can't half-neutralize a contract or orphan domain
copies.
Topics: domain-to-neutral-promotion, contract-ownership, roles-authority-model
Repository context: openxFactory (contract-level, cross-factory topic)
Captured: 2026-07-08
Organized: 2026-07-08 into
[docs/domain-to-neutral-promotion-process.md](../../docs/domain-to-neutral-promotion-process.md)
and the seed
[docs/domain-neutralization-candidate-register.md](../../docs/domain-neutralization-candidate-register.md).
The process doc is now the working definition; this file is kept as design
history plus the open questions below that remain unresolved. Companion to
[Doc Health Pipeline](doc-health-pipeline.md): that pipeline moves ideas
through states *within* a repo; this one moves proven concepts *between* repo
tiers. Nothing in this document is policy.

## Problem

`shared-contract-ownership` obliges any concept governing two or more
factories to live canonically in `openxFactory/contracts/` — but no process
defines how a concept that was born inside one DomainxFactory gets there.
History shows both directions happening ad hoc:

- Promotion: "Make worker model domain neutral" (openxFactory, 2026-06) lifted
  an engineering-born concept into the neutral layer by plain commit.
- Devolution: the reconcile-domain-neutral-and-engineering-spec-ownership
  change (landed 2026-07-08) pushed software-specific Spec Kit / PR admission
  mechanics back down to codexFactory.

Without a defined lifecycle, promotions risk half-neutralized contracts
(domain vocabulary leaking into the neutral layer) and orphaned domain copies
that drift from the promoted version.

## Design sketch

### Trigger signals (when promotion should be considered)

- The same concept appears independently in two or more domain repos
  (convergent evolution — e.g. credential grant templates, Hermes layer
  models).
- A second domain starts referencing a concept documented in another domain's
  repo.
- The nightly doc-health report detects near-duplicate contracts or overlay
  keys across domains.

### Lifecycle (mirrors the knowledge-lifecycle gate pattern)

```text
domain-local concept
  | tag: <!-- xspec:promote-candidate scope=neutral -->
promotion candidate            visible in nightly health report
  | organize gate: neutralization draft in openxFactory ideation/staging/
staged neutral concept         domain vocabulary stripped; overlay points
                               identified for each consuming domain
  | proposal gate
openxFactory OpenSpec change   ADDED capability in the neutral layer
  | approval + implementation
promoted neutral contract      openxFactory/contracts/ owns it
  | re-pin gate (per domain)
originating domain consumes    local version replaced by a reference plus a
                               thin domain overlay — the origin domain
                               becoming consumer #1 is the proof of
                               genuine neutrality
  | retire gate
domain-local copy retired      or reduced to overlay-only; health report
                               flags any surviving duplicate
```

### Rules of thumb

- Neutrality test: if the originating domain cannot consume the promoted
  version through a thin overlay, the concept was not actually neutral —
  demote it back and try again narrower.
- Devolution uses the same lifecycle in reverse (neutral concept proves
  domain-specific → staged demotion → domain repo adopts → neutral layer
  keeps only the abstract hook). The reconcile change is the precedent.
- Authority: the owning Domain Hermes approves surrendering its concept;
  openxFactory boundary governance approves receiving it; both gates are
  OpenSpec changes, never bare commits.

## Open questions

Resolved by the process doc: the two-domain trigger question (the Candidate
Rule admits single-domain candidates with plainly neutral surfaces, and the
Scoring axes weigh reuse explicitly).

Still open:

- Who drafts the neutralization — the originating domain's workers or
  codexFactory doc-engineering workers under the doc-health pipeline?
- Should `stack.yaml` grow a `promoted_from` / `specializes` field so
  provenance of promoted contracts is machine-readable?
- How do version pins interact mid-promotion, while a concept exists in both
  the domain repo and openxFactory staging?
