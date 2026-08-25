---
code_surface: openxFactory (`scripts/validate-domain-ontology.py` term-lifecycle/version rules and prior-revision comparison, `scripts/ontology-release.py` draft-term publication refusal, `scripts/ontology-compile-context.py` retired-term compilation refusal, the negative-fixture corpus and pilots under `contracts/domain-ontology/examples/`, `scripts/test-ontology-stewardship.py`); no schema byte changes — lifecycle enums and effective_version already exist in the ratified shapes
target_release: none (no contract-bundle bytes change; the canonical validator, tools, and fixture corpus are content-addressed by commit under the contract-v1.22 registration)
Status: ratified
Ratified by: Brett's direction on 2026-07-30 ("lets do F18 term-lifecycle enforcement"), landing the first carried-forward finding from the add-domain-ontology-layer release review (APPROVED at 5d39bb4); strict validation green
---

# Proposal: add-ontology-term-lifecycle-enforcement

## Why

The domain-ontology release review (four rounds, APPROVED at 5d39bb4)
carried forward finding **F18** as the first follow-up to land: term-level
`lifecycle_state` and `effective_version` are declared in every ratified
shape but enforced nowhere — "the last place where a stated contract has
no enforcement behind it." Concretely: both reference pilots shipped
`published` packages composed entirely of `draft` terms, a retired term
still compiles into new live semantic contexts, a retired identifier can
be silently resurrected in the next revision, and a term's meaning can
change without any version movement. The promoted
`domain-ontology-lifecycle` spec already states that "new classification,
mapping, or binding against a retired identifier fails closed" — this
change puts machinery behind the sentence before term retirement becomes
load-bearing in a live domain (MedxFactory is the first adopter).

## What Changes

- **Term-level lifecycle discipline** (new requirement in
  `domain-ontology-lifecycle`): a `published`/`deprecated` package carries
  no `draft` term — publication is a per-term steward decision made
  before release, and `ontology-release.py` refuses a publication while
  any term remains draft; across consecutive versions a term's lifecycle
  only moves forward (`draft → published → deprecated → retired`, skips
  allowed, resurrection fails validation); a meaning-bearing change
  (label, aliases, definition, parents; for relations domain, range,
  characteristics) requires an `effective_version` bump, and
  `effective_version` never moves backward.
- **Retired terms refuse new compilation** (modified `Bounded semantic
  context` in `xfactory-semantic-kernel`): `ontology-compile-context.py`
  refuses a retired term in the requested set or computed closure; a
  worker profile naming a retired required term is invalid; the canonical
  validator rejects a context pinned at the CURRENT package digest whose
  subset carries a retired term. Historical contexts pinned at prior
  digests keep their original interpretation unchanged.
- **Validator**: new finding codes `ONT-TERM-LIFECYCLE` (draft term in a
  published package; backward lifecycle movement; retired term in a
  profile or current-digest context) and `ONT-TERM-VERSION`
  (meaning-bearing change without a bump; version moving backward),
  evaluated in the prior-revision comparison — which now loads retained
  prior terms for EVERY compatibility class, not only non-breaking ones.
- **Fixtures and pilots**: five new indexed negatives (minimum ratchets
  44 → 49); the pilots publish their terms as an explicit steward act
  before first release and bump `effective_version` on the reparented
  term, demonstrating the real workflow.

## Impact

- Affected specs: `domain-ontology-lifecycle` (ADDED requirement),
  `xfactory-semantic-kernel` (MODIFIED `Bounded semantic context`).
- Affected code: the three scripts named in `code_surface`, the fixture
  generator outputs, and the stewardship test suite (which gains
  draft-term refusal probes).
- NOT affected: schemas (enums/fields already ratified at
  contract-v1.22), the memory-gateway packet contracts (term-level state
  never rides in packets), MedxFactory's draft package (draft packages
  may hold draft terms by design), and the DRAFT `xf/core` kernel — its
  terms flip to published as part of the future governed kernel
  publication, which this change makes mechanically checkable.
