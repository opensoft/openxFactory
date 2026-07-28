# Requirements Mining: From Episode Corpus to Buildable Spec — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Hermes turns a family's episodes into a buildable spec by mining
invariants, parameters, branches, and counterexamples; the curated episode
set becomes the acceptance corpus (with declared equivalence predicates and
record-replay cassettes, never byte-equality goldens); the scope fence — the
input region the capability claims, everything else falling back to AI — is
itself a requirement artifact; and the whole spec is regenerable from corpus
digest + miner version, with human ratification gates scaled to rung and
risk.
Topics: crystallization, requirements-mining, acceptance-corpus, scope-fence,
equivalence-predicates, record-replay, episode-ledger, governed-derived-model,
domain-hermes
Repository context: openxFactory (neutral micro-spec and fence schemas;
mining runs as a bounded domain worker)
Captured: 2026-07-28

## Possible feats

- **Crystallization micro-spec template** — feat-spec-shaped, machine-drafted,
  citing episodes as evidence; scaled ratification by risk class.
- **Acceptance-corpus contract** — curated episode refs + equivalence
  predicates + cassettes, digest-pinned; the corpus IS the contract.
- **Scope-fence artifact** — a deterministic predicate over envelope/inputs
  declaring jurisdiction, consumed verbatim by dispatch.
- **Counterexample harvesting** — failed/corrected episodes become negative
  requirements and regression entries automatically.

## Position in the packet

Third document of the invest/build arc: activated by an approved
[economics decision](crystallization-economics.md), consumes the family's
[episodes](crystallization-episode-ledger.md), and hands spec + corpus +
fence to the [build pipeline](crystallization-build-pipeline.md). The fence
it authors is enforced by
[dispatch](crystallization-dispatch-and-fences.md); the corpus it curates is
replayed by [parity](crystallization-parity-and-cutover.md).

## Mining moves

From N episodes of one family:

- **Invariants** — behavior constant across episodes ("the report always
  balances to zero", "the PR always carries the gate-evidence block").
  Invariants become requirements and post-conditions.
- **Parameters** — what varied, with observed types and ranges (months,
  accounts, repos). Parameters become the capability's typed inputs — and
  their observed ranges seed the fence.
- **Branches** — episodes whose plans diverged reveal conditionals ("when
  the export has a continuation page, fetch it first"). Divergent episodes
  are requirements gold, not noise.
- **Counterexamples** — episodes with bad label folds (corrected, reverted,
  reopened) become negative requirements ("MUST NOT close the period when
  any entry is unreconciled") and mandatory regression entries. A spec with
  only happy paths fails the gate.

## The acceptance corpus is the contract

The curated episode set is the ground truth the build must satisfy and the
replay set parity uses forever after. Two disciplines keep it honest:

- **Equivalence predicates, not byte goldens** — outputs are compared by
  declared predicates per output type (structured fields exact; prose by
  semantic predicate, AI-judged where needed — judging is far cheaper than
  solving). Byte-equality goldens rot on the first cosmetic change.
- **Cassettes for side effects** — `record-replay` episodes (EL-C3) replay
  against recorded tool I/O, VCR-style, so the corpus runs without touching
  the world. `live-only` families get thinner corpora and lean harder on
  shadow proof — which lowers their practical rung ceiling.

The corpus is versioned by digest; the spec pins the corpus digest; the
capability's provenance pins both. Refreshing the corpus (new episodes in,
stale ones out) is a recorded transition that triggers re-proof.

## The scope fence is a requirement

The spec declares not just behavior but **jurisdiction**: a deterministic
predicate over envelope and inputs defining what the capability claims.
Derived conservatively from observed support (parameter ranges seen,
branch conditions covered), widened only by evidence (fallback episodes
that were handled fine become fence-expansion candidates). Everything
outside the fence routes to AI — the fence is why a crystallized capability
can be trusted young: it only ever speaks inside the region its evidence
covers.

## Who writes it, who signs it

The Domain Hermes drafts (it holds the efficiency mandate and the domain
expertise); the draft is a templated **micro-spec** — deliberately
feat-spec-shaped like a staging fragment, so humans review a familiar form.
Ratification scales: low rung + low authority → auto-ratify with audit;
high rung or subject-affecting → human gate. Coverage honesty is mandatory:
the spec declares its evidence bounds (episode count, parameter ranges,
time span) so a reviewer sees exactly how much world the corpus has seen.

## Claims

- **RQ-C1** — Specs cite episodes as their evidence base; every requirement
  traces to episodes (invariant, branch, or counterexample), and the
  declared evidence bounds are part of the spec.
- **RQ-C2** — The acceptance corpus is the operative contract: curated
  episode refs, equivalence predicates per output type, cassettes for side
  effects, all digest-pinned.
- **RQ-C3** — The scope fence is a requirement artifact authored here and
  consumed verbatim by dispatch — never runtime configuration invented at
  deploy time.
- **RQ-C4** — Specs are regenerable: corpus digest + miner version →
  the same spec (governed-derived-model discipline applied to
  requirements).
- **RQ-C5** — Counterexample content is mandatory; a corpus without failure
  cases is rejected at the intake gate.

## Open questions

- **RQ-Q1** — Minimum corpus size by rung (an L3 playbook from 3 episodes
  may be fine; L6 code from 3 episodes is reckless) — schedule or
  evidence-quality score?
- **RQ-Q2** — PII scrubbing standard for corpora: reuse the knowledge
  lifecycle's de-identify gate as-is, or a corpus-specific profile?
- **RQ-Q3** — Fence-only releases: can a fence widen without a rebuild when
  fallback evidence supports it, or does any fence change re-run proof?
- **RQ-Q4** — Who signs equivalence predicates — they quietly define
  "correct," which makes them the most authority-laden artifact in the
  chain?
- **RQ-Q5** — Can the miner propose fragment extraction mid-mining ("these
  4 steps are a shared sub-family — crystallize them instead"), feeding
  back to [family](crystallization-task-families.md) fragment lanes?

## Related

- [Episode Ledger](crystallization-episode-ledger.md) — evidence source and
  replayability classes.
- [Build Pipeline](crystallization-build-pipeline.md) — the consumer of
  spec + corpus + fence.
- [Parity and Cutover](crystallization-parity-and-cutover.md) — the corpus's
  second life as a replay suite.
