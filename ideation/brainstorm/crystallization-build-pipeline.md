# The Crystallization Build Pipeline: The Factory Builds Its Own Shortcuts — Brainstorm

Status: staged
Kind: architecture
Summary: A crystallization build is an ordinary governed engineering job
(`job_type: crystallization_build`) executed by codexFactory for every
domain — the factory recursively applying itself — flowing intake → design →
implement → corpus-green → security and data-leak review → permission
binding → dry-run proof → shadow → promote → register, with a mandatory
provenance manifest chaining capability → spec → corpus → episodes →
original runs, regeneration-first maintenance (hand-patching breaks lineage
and is gated as an exception), and a budget cap with declared abort
behavior.
Topics: crystallization, build-pipeline, codexfactory, provenance,
governed-derived-model, release-realization, workflow-gate-contract,
tech-stack-benches, data-leak, dry-run
Repository context: openxFactory (neutral build-job and provenance schemas;
execution lives in codexFactory)
Captured: 2026-07-28
Organized: 2026-07-29 into the
[recurrence-crystallization staged topic](../staging/recurrence-crystallization/recurrence-crystallization.md)
(staged); kept as design history.

## Possible feats

- **`crystallization_build` job kind** — a neutral envelope profile with
  spec + corpus + fence as input artifacts and a registered capability as
  output.
- **Capability provenance manifest** — digest chain over episodes, corpus,
  spec, builder identity, test and review evidence.
- **Generated-code data-leak scan gate** — detect memorized tenant constants
  in generated artifacts; hardened further for pooled builds.
- **Dry-run mode as a build acceptance criterion** — every capability must
  ship simulation support because shadow parity depends on it.

## Position in the packet

Fourth document of the invest/build arc: receives spec + corpus + fence from
[requirements mining](crystallization-requirements-mining.md) under a funded
[decision](crystallization-economics.md); its output registers in the
[capability registry](crystallization-capability-registry.md) and enters
proof under [parity](crystallization-parity-and-cutover.md). Permission
review applies [authority conservation](crystallization-authority-and-consent.md).

## Recursion is the point

The factory family's whole premise is governed expert work executed by
agents. Building a crystallized capability **is** governed expert work — so
it is submitted as a normal job, planned, gated, and audited like any other.
No parallel build machinery. Two consequences:

- **codexFactory serves all domains.** A recurring Medx pattern is still an
  engineering artifact; codexFactory builds it, MedxFactory reviews domain
  fitness and owns the domain gates. This cross-domain service contract is a
  new seam (a domain consuming another domain's factory) worth its own
  design attention.
- **Builds are themselves episodes.** The build job lands in the episode
  ledger like anything else — so the crystallizer's own recurring work is
  subject to crystallization. The miner, the fence-checker, the corpus
  runner all start as AI work and harden along the same ladder.

## Stage sketch

```text
intake      spec + corpus + fence validated; evidence bounds reviewed
design      artifact shape chosen (playbook | micro-agent set | program)
implement   built by Omnigent engineering workers under normal lanes
corpus      acceptance corpus green (equivalence predicates, cassettes)
security    sandbox conformance; dependency policy; DATA-LEAK SCAN —
            generated artifacts must not embed memorized tenant values
            (a literal that is actually one tenant's account number)
authority   permission binding derived and reviewed (never wider than the
            AI configuration it replaces)
dry-run     simulation mode demonstrated — a hard acceptance criterion
shadow →    handed to parity proof (separate doc); promotion and
register    registration follow its gates
```

Each arrow is a workflow-gate-contract instance; evidence lands in the run
record as usual.

## Provenance: regenerate, never hand-edit

The capability is a **derived artifact of episodes**, and the
governed-derived-model discipline applies verbatim: a provenance manifest
pins episode digests, corpus digest, spec version, builder identity/version,
toolchain (bench) pins, and test/review evidence. Consequences:

- The durable asset is the **pipeline**, not any single artifact — drift
  repair is "regenerate from a refreshed corpus," not "patch the code."
- Hand-patching breaks lineage and is gated as an exception that must fold
  back (the patch becomes a spec/corpus delta and the artifact is
  regenerated to include it).
- Release rides the existing release-realization capability: the build
  declares a `code_surface`, and promotion requires merged + green
  realization evidence — machinery that already exists.

## Budget discipline

Builds run under the decision's cap with declared abort behavior: stop at
the threshold, persist partial work, return actuals, renominate with honest
numbers. Estimate-vs-actual lands in
[accounting](crystallization-accounting.md) and calibrates future
estimates — the variance-vs-estimate audit the cost-accountability
brainstorm already wants.

## Claims

- **BP-C1** — A crystallization build is an ordinary governed job through
  the existing factory lanes; no parallel build machinery exists.
- **BP-C2** — codexFactory builds for every domain; the consuming domain
  owns fitness review and domain gates — a named cross-domain service seam.
- **BP-C3** — The provenance manifest is mandatory and chains capability →
  spec → corpus → episodes → original runs without gaps.
- **BP-C4** — Maintenance is regeneration-first; hand-patches are gated
  exceptions that must fold back into spec/corpus and re-derive.
- **BP-C5** — Dry-run/simulation support is a build acceptance criterion,
  because shadow proof and safe drift re-verification depend on it.

## Open questions

- **BP-Q1** — Artifact packaging: playbooks as workflow instances, programs
  as containers/plugins? Repo-per-capability vs. a capabilities monorepo per
  domain?
- **BP-Q2** — Toolchain allowlist: are tech-stack benches
  ([benches brainstorm](tech-stack-benches.md)) the required execution
  substrate from day one?
- **BP-Q3** — Maintainer of record after the build: the domain, codexFactory,
  or a steward role — who answers the pager when post-conditions fail?
- **BP-Q4** — Does the data-leak scan need its own capability (it looks like
  doc-health's sibling: mechanical checks + contested findings)?
- **BP-Q5** — Licensing/IP posture for generated code, especially once
  pooled evidence is involved (defer to
  [cross-tenant](crystallization-cross-tenant.md) but the gate needs a
  placeholder now).

## Related

- [Requirements Mining](crystallization-requirements-mining.md) — the input
  contract.
- [Parity and Cutover](crystallization-parity-and-cutover.md) — the proof
  stages this pipeline hands into.
- `openspec/specs/governed-derived-model/` and
  `openspec/specs/release-realization/` — the two existing disciplines this
  pipeline composes.
