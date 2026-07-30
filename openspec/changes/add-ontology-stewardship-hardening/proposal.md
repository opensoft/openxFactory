---
code_surface: openxFactory (`scripts/apply-domain-starter.py` --ontology-only + structural placeholder recording + inventoried STARTER marker, `scripts/ontology-release.py` faithful manifest rewrite + evidence-path containment + superseded retained snapshots, `scripts/validate-domain-ontology.py` marker/retention/cadence rules + structural readiness, `scripts/validate-memory-gateway.py` executable conformance probes, `contracts/domain-ontology/ontology-stewardship-policy.schema.yaml` + `ontology-starter-provenance.schema.yaml`, `examples/memory-gateway/conformance-fixtures.yaml`, the fixture corpus and pilots, test suites); MedxFactory + codexFactory inventory the STARTER marker through small follow-on commits
target_release: next additive contract bundle (contract-v1.24; two domain-ontology schema files change bytes — the cut also carries the recorded contract-v1.23 erratum correction to consumers)
Status: ratified
Ratified by: Brett's direction on 2026-07-30 ("yes, fold it into that hardening pass" — the --ontology-only adoption mode joining the F21/F24–F27 stewardship pass carried forward from the domain-ontology release review); strict validation green
---

# Proposal: add-ontology-stewardship-hardening

## Why

The domain-ontology release review carried five non-blocking findings to
"the stewardship pass", and two real adoption runs (MedxFactory,
codexFactory) exposed one operational hazard the tooling should own:

- **F21** — the release tool rewrites `package.yaml` from a hardcoded
  line list, silently dropping ratified fields (`adoption`, `notes` — a
  kernel release would shed its adoption evidence); its evidence-path
  arguments (`--migration-map ../x`) can escape the package directory
  into the inventory; and a retained snapshot still claims the lifecycle
  it had when active, so a consumer reading `retained/<v>/package.yaml`
  cannot tell it is history.
- **F24** — readiness detects placeholder content by STRING MATCHING
  (`/placeholder_subject`, `"UNASSIGNED"` in a name): rename the
  placeholder and the scaffold reads ready.
- **F25** — the STARTER provenance marker is a deletable beside-package
  file, and the generated-domain completeness check keys on its
  presence: delete one file and a generated domain silently sheds its
  generated status and every completeness obligation.
- **F26** — the stewardship-policy schema REQUIRES `min_value` on every
  quality signal, so a max-bounded signal (`unknown_term_rate` must stay
  UNDER a ceiling) is inexpressible correctly; and a policy can declare
  a source-review cadence while external sources carry no review
  deadline for it to apply to.
- **F27** — the memory-gateway conformance fixtures are DECLARATIVE
  (prose `asserts` strings); the validator only checks their ids exist,
  so a fixture can promise behavior nothing executes.
- **Adoption runs** — the starter emits the whole-repo scaffold on
  mature repositories; both real adoptions required a manual
  delete-the-strays step that rests on operator discipline in a
  shared-checkout workspace. Three domains still owe adoptions and the
  candidate-ingestion loop reruns the starter routinely.

## What Changes

- **`--ontology-only` adoption mode** (starter): writes ONLY
  `hermes/domain/ontology/**` and the content-manifest declaration
  (candidate ingestion included); the whole-repo template stage and
  README link stage do not run; the rerun report prints to stdout
  instead of landing in `docs/`. Instantiation behavior on empty targets
  is unchanged.
- **Structural placeholders (F24)**: the STARTER marker records the
  placeholder term ids and steward ids the run seeded
  (`placeholders: {terms, stewards}` — starter-provenance schema gains
  the optional block); readiness blocks on any recorded placeholder
  still present, with the old string heuristics retained only as
  defense-in-depth.
- **Marker integrity (F25)**: the STARTER marker becomes INVENTORIED
  package content — generated packages digest-cover it, so deleting it
  breaks the package digest (fail closed) and a marker left beside the
  inventory is flagged; the overlay validator's completeness check stays
  keyed on the recorded marker. MedxFactory and codexFactory inventory
  their markers in follow-on commits.
- **Release-tool housekeeping (F21)**: the manifest rewrite carries
  every declared field (`adoption`, `notes` — verified against the
  schema's property list); `--migration-map`, `--quality-report`, and
  `--consumer-impact` refuse paths that resolve outside the package
  directory; and retained snapshots are BORN `lifecycle_state:
  superseded` (both the self-retained copy and the fallback copy) — a
  retained manifest claiming an active lifecycle is a validator finding.
  Append-only retention is untouched: nothing rewrites an existing
  snapshot.
- **Quality-gate expressiveness (F26)**: a required signal declares
  `min_value` OR `max_value` (at least one — schema `anyOf`); when the
  policy declares `source_review`, every external-kind source SHALL
  carry a `review_by` deadline (validator rule).
- **Executable conformance fixtures (F27)**: each semantic-context
  fixture either carries a `probe` (a mutation of the canonical example
  packet the gateway validator EXECUTES through its own preflight,
  asserting rejection) or names `executed_by` (an existing artifact or
  suite that executes the behavior, resolution verified). A fixture that
  neither executes nor resolves its delegate fails validation.

## Impact

- Affected specs: `domain-ontology-lifecycle` (MODIFIED scaffold
  pipeline, quality accountability, generated-domain acceptance;
  evolution/retention scenarios), `memory-gateway` (MODIFIED
  `Gateway Conformance Is Testable`).
- Contract bytes: the two schema files → contract-v1.24 (which also
  delivers the corrected `content-manifest.schema.yaml` digest recorded
  as the v1.23 erratum).
- Affected code: the four scripts and fixture surfaces in
  `code_surface`; new negatives ratchet the corpus minimum upward.
- Domain follow-ons: MedxFactory and codexFactory restamp their draft
  packages with the marker inventoried (kernel pins unchanged).
- NOT affected: the semantic plane's authority firewall, the omnigent
  wiring surfaces (contract-v1.23), packet schemas, and all published
  retained bytes.
