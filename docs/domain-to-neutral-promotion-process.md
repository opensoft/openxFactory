# Domain-To-Neutral Promotion Process

Status: standard
Kind: process
Backed by: [openspec/specs/document-lifecycle/spec.md](../openspec/specs/document-lifecycle/spec.md) (promoted from the archived add-document-lifecycle-vocabulary change)
Repository context: openxFactory
Purpose: define a repeatable way to find domain repo patterns that should become
neutral openxFactory contracts, templates, validators, or specs.

Origin: organized from
[ideation/brainstorm/domain-to-neutral-promotion.md](../ideation/brainstorm/domain-to-neutral-promotion.md)
(captured 2026-07-08). The companion
[Doc Health Pipeline](../ideation/brainstorm/doc-health-pipeline.md) brainstorm
plans a nightly health report whose duplicate-contract detection feeds new
candidates into this process.

## Storage Decision

This process belongs in `openxFactory`, not the top-level `xFactory` aggregation
repo.

`openxFactory` owns domain-neutral contracts, gates, traceability, routing,
credential, memory, source-authority, workflow, and audit rules. Domain repos
own domain nouns, policy, examples, artifacts, agents, and implementation
details. The top-level `xFactory` repo should compose repos and pin submodules;
it should not become the place where neutral contract policy is authored.

## Inputs

Run the review from the top-level `xFactory` workspace so the neutral repo and
domain repos can be compared in one pass.

Expected layout:

```text
xFactory/
  openxFactory/
  xFactories/
    AdxFactory/
    LedgerxFactory/
    MedxFactory/
    OpsxFactory/
    codexFactory/
```

Review these file families first:

- `docs/**/*.md`
- `contracts/**/*`
- `schemas/**/*`
- `workflows/**/*`
- `credentials/**/*`
- `templates/**/*`
- `profiles/**/*`
- `examples/**/*`

Exclude generated files, package caches, vendor trees, runtime workspaces,
secret stores, and archived evidence unless a specific prior decision needs to
be checked.

## Search Pass

Run every command below from the top-level `xFactory` workspace root; all
paths are relative to it so the process works in any checkout location.

Start with inventory and cleanliness checks:

```bash
git status --short --branch
git submodule status
git -C openxFactory status --short --branch
find xFactories -maxdepth 2 -type f | sort
find openxFactory -maxdepth 3 -type f | sort
```

Search for control-surface words across domain repos and compare them to
existing neutral docs and contracts:

```bash
rg -n "workflow|gate|admission|state|transition|audit|traceability|contract|schema|validator" \
  openxFactory xFactories

rg -n "credential|grant|broker|binding|approval|allowed_actions|disallowed_actions|required_evidence" \
  openxFactory xFactories

rg -n "authority|Hermes|Omnigent|candidate|proposed trigger|review|handoff|escalation" \
  openxFactory xFactories

rg -n "provenance|citation|source authority|reliability|stale|reverification|risk-of-wrong|memory|promotion" \
  openxFactory xFactories
```

Use narrower follow-up reads on the most relevant files. Capture source paths
and line numbers for every candidate.

## Candidate Rule

Create a promotion candidate when one of these is true:

- Two or more domain repos use the same structure with different domain nouns.
- One domain repo has a control surface that is plainly domain-neutral, such as
  admission, gating, scoped credentials, provenance, trigger routing, audit, or
  candidate promotion.
- A domain repo has a stricter machine-readable schema than the neutral repo for
  a surface that openxFactory already claims to own.
- Repeated domain-local docs explain the same boundary that should be stated
  once as a shared rule.

Do not create a promotion candidate for:

- clinical, legal, accounting, marketing, operations, or engineering facts
- domain-specific standards or professional judgment
- domain-owned examples that only illustrate local policy
- live runtime data, customer data, credentials, tenant bindings, or production
  memory records
- agent populations or implementation details that belong to a DomainxFactory

## Classification

Classify each candidate before creating OpenSpec work.

| Decision | Meaning |
| --- | --- |
| `promote` | Move the neutral skeleton into openxFactory as a doc, contract, template, validator, or spec. |
| `split` | Promote the generic shape and keep domain-specific overlays in the domain repo. |
| `reference` | Add a neutral pointer to an existing domain example without moving content. |
| `keep-domain-local` | Leave the content in the domain repo because it encodes domain authority or implementation. |
| `defer` | Keep a backlog item because the pattern is plausible but evidence is thin. |

Most useful promotions are `split`: openxFactory gets the invariant contract,
and each domain keeps its nouns, gates, authority thresholds, reviewer roles,
examples, and adapters.

## Scoring

Score candidates from 0 to 3 on each axis.

| Axis | Question |
| --- | --- |
| Cross-domain reuse | Does the same shape apply across multiple DomainxFactories? |
| Neutral ownership | Is this a surface openxFactory claims to own? |
| Implementation readiness | Can it become a schema, template, validator, checklist, or OpenSpec requirement now? |
| Risk reduction | Would promotion reduce ambiguity, unsafe bypasses, or contract drift? |
| Domain leakage risk | Would promotion accidentally encode domain-specific authority? Lower is better. |

Suggested priority:

- `P0`: high reuse, clear neutral ownership, low leakage, needed before more domain work
- `P1`: strong reusable contract or validator candidate
- `P2`: useful template/checklist or backlog item
- `P3`: reference-only or wait for more domain evidence

## Evidence Packet

Every candidate should be recorded with this shape:

```yaml
candidate_id: DTN-000
title:
decision: promote | split | reference | keep-domain-local | defer
priority: P0 | P1 | P2 | P3
neutral_surface:
source_evidence:
  - repo:
    path:
    line_start:
    line_end:
neutral_gap:
proposed_openxfactory_artifact:
domain_local_exclusions:
openspec_needed: true | false
notes:
```

The current seed register is stored in
[Domain Neutralization Candidate Register](domain-neutralization-candidate-register.md).

## OpenSpec Handoff

Brainstorming and candidate discovery are not the hard spec. Use this split:

```text
domain repo scan
  -> candidate register entry
  -> optional ideation note for unresolved thinking
  -> OpenSpec change proposal
  -> approved spec delta and tasks
  -> implementation
  -> validation evidence
  -> archive
  -> domain adoption (re-pin, overlay, retire local copy)
```

Use `ideation/brainstorm/` only for exploratory prose that is not yet approved
as contract intent. Once a candidate is selected for implementation, create an
OpenSpec change in `openxFactory/openspec/changes/<change-id>/`.

Minimum OpenSpec artifacts:

- `proposal.md`: why this neutral contract change is needed and what stays out
- `design.md`: target doc, schema, validator, or template design
- `tasks.md`: implementation and validation tasks
- `specs/<capability>/spec.md`: requirements delta when behavior or conformance
  changes

The OpenSpec change should reference the candidate IDs from the register and
must identify domain-local exclusions so the neutral repo does not absorb domain
authority.

Validate before implementation and before archive:

```bash
cd openxFactory
OPENSPEC_TELEMETRY=0 openspec validate <change-id> --strict
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

## Implementation Outputs

A promoted candidate should produce one or more of:

- neutral documentation under `docs/`
- schema under `contracts/schemas/`
- policy or vocabulary under `contracts/policies/`
- template under `templates/`
- validation script under `scripts/`
- examples under `examples/`
- OpenSpec requirement under `openspec/specs/`
- changelog entry under `contracts/CHANGELOG.md` when a contract changes

If a change updates a machine-readable contract, also update the conformance
docs and validator references.

## Domain Adoption And Retirement

A promotion is not complete when the neutral artifact merges. It is complete
when the originating domain consumes it:

1. Re-pin gate: each consuming domain updates its pinned openxFactory version
   to one containing the promoted artifact.
2. Overlay replacement: the domain replaces its local copy with a reference to
   the neutral artifact plus a thin domain overlay carrying only domain nouns,
   thresholds, roles, and examples.
3. Retire gate: the domain-local duplicate is deleted or reduced to
   overlay-only. A surviving near-duplicate is a health finding, not a
   convenience.
4. Register update: the candidate's status moves to `adopted` with links to
   the neutral artifact and the domain overlays.

Neutrality test: the originating domain must be able to consume the promoted
version through a thin overlay — the origin becoming consumer #1 is the proof
the concept was genuinely neutral. If it cannot, the promotion was too broad:
demote it back and retry with a narrower skeleton.

Devolution runs the same lifecycle in reverse. When a neutral artifact proves
domain-specific in practice, stage a demotion: the owning domain adopts the
content, and openxFactory keeps only the abstract hook or deletes the
artifact. The reconcile-domain-neutral-and-engineering-spec-ownership change
(2026-07-08) is the precedent. Authority is symmetric: the owning Domain
Hermes approves surrendering or receiving a concept, boundary governance
approves the neutral side, and both gates are OpenSpec changes, never bare
commits.

## Review Checklist

Before merging a promotion:

- The neutral artifact uses generic xFactory vocabulary.
- Domain-specific terms are examples only or moved to overlays.
- Domain repos can still specialize through overlays without forking the base
  contract.
- The candidate register entry is updated with status and artifact links.
- The OpenSpec change validates.
- Contract versioning impact is documented.
- No secrets, runtime data, customer data, or generated workspaces are added.

