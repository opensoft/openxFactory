# Design: add-structured-scope-substrate

Primary source: the staged topic `openxFactory:staging:structured-scope-substrate`
(`ideation/staging/structured-scope-substrate/structured-scope-substrate.md`),
which resolved the key decisions below. This design records those decisions as the
buildable contract and carries the residual open questions forward for the
convener ratification read (task 1.5). It is a buildable spec, not a re-design.

## Context

- **Ratified consumer doctrine (B):** `add-provenance-gated-autonomous-merge`,
  ratified AS AMENDED by the `gate_rules_council` 2026-08-28 (openxFactory
  `change/add-provenance-gated-autonomous-merge` @ `a9180588`). Its
  "Provenance-tie verifier contract" step (iii) needs a machine-readable path
  scope; its folded CRITICAL #1 ("Floor primacy and per-repository floor
  instantiation") makes the substrate trust-root source (iv).
- **Amended capability:** `release-realization`
  (`openspec/specs/release-realization/spec.md`) — the neutral home of the
  `code_surface:` / `target_release:` front-matter contract.
- **Glob engine to conform to:** codexFactory
  `scripts/merge_master/envelope.py` (`_glob_to_regex`, `path_matches`,
  `_validate_path_allowlist`, `_UNIVERSAL_PATTERNS`, `_COMPLEMENT_KEYS`) —
  verified against a current codexFactory checkout (worktree head
  `3143f34d`; the glob region last changed at `9ebe805`). The openxFactory
  submodule pin of codexFactory is stale, so the dialect was read from the live
  checkout, not the pin.

## Decisions

### D1 — A new sibling field `scope_globs:`, NOT an amendment to `code_surface`
Resolves B's Open Question 2. Amending `code_surface` into a structured field is a
flag-day break: 45+ active changes and every archived change carry
prose/repo-name/`none` forms a structured schema would reject, and no validator
enforces any form today (measured: 164 refs, all prose). A sibling is additive and
non-breaking — every existing change keeps working and is simply not
provenance-eligible until it adds `scope_globs`. The two fields answer different
questions at different granularities (`code_surface` = which repositories'
artifacts change, an archive-gate concern; `scope_globs` = which paths within a
repository the diff may touch, a verifier concern), and overloading one field
would entangle two axes. `code_surface` prose stays useful and is untouched.
Trade-off (the two fields can drift) is handled by the cross-consistency check
(every `scope_globs` key must be in `code_surface`), not by collapsing them.

### D2 — Per-repository MAP, not a flat list
A change's `code_surface` may name several repositories; containment is evaluated
per repository against a pull request that lives in exactly one repo, so the
verifier selects `scope_globs[R]` for the pull request's repository `R`. A flat
list keyed implicitly by the pull request's repo would be simpler IF provenance
pull requests are always single-repo, but the map is the safe superset and costs
nothing when a change spans one repo. (Carried as Open Question 2 for the
convener to confirm the map is warranted.)

### D3 — Front-matter home, not a sidecar file (for v1)
`scope_globs` lives in `proposal.md` YAML front-matter beside its `code_surface`
sibling, so the two are read, validated, and origin-retained together, and the
archive gate + dashboard already read that block. A `scope_globs.yaml` sidecar for
very large scopes (the openxwallet split's ~600-word `code_surface` shows scopes
can get large) is a named future affordance, not the v1 home. (Carried as Open
Question 1.)

### D4 — Conform to the ONE envelope glob engine; forbid the crown-jewel dialect's forbidden forms
`scope_globs` globs are repository-relative and use exactly the envelope dialect:
`**` = zero+ path segments, `*` = a non-separator run within a segment, `?` = one
non-separator, anchored full-match. The validator's rejection set mirrors
`_validate_path_allowlist` byte-for-behaviour: reject leading `/` (unreachable
against repo-relative paths — CODEOWNERS dialect is not this one), leading `!`
(negation — none in the dialect; subtraction is a complement that fails open), the
universal patterns `**`/`*`/`**/*`/`/**`/`./**` (complement of the empty set —
would leave the floor the only control), and any complement/denylist key
(`path_denylist` and siblings). Using the SAME engine as the floor is what makes
scope-containment and floor checks incapable of disagreeing.

### D5 — Floor overrides at CHECK time; `openspec validate` stays floor-agnostic
The never-clearable floor is tree-specific and per-repository, published in each
repository's `.github/merge-approval-envelope.yml`
(`gate_integrity.never_clearable_paths`). The neutral `openspec validate` in
openxFactory cannot and must not know it — making it floor-aware would force it to
vendor every enrolled repository's floor and couple it to each domain's tree
(portability requirement forbids this). So validation does NOT reject a glob that
names a floor path; the verifier subtracts the repository's own base-branch floor
from the authorized set at check time, reusing the shipped
`_gate_integrity_problem` "floor subtracts from the allowlist" semantics. One
floor authority per repository; `scope_globs` can never authorize a floor path;
floor always wins. An optional repo-side ADVISORY lint MAY warn when a change's
scope names a known floor path, but that is advisory, never an `openspec validate`
gate. (Carried as Open Question 5.)

### D6 — Trust-root integrity bound to ratification (CRITICAL #1 satisfaction)
B's folded CRITICAL #1 makes the substrate trust-root source (iv), requiring four
properties this change realizes as `release-realization` obligations:

1. **Base-read.** The verifier reads `scope_globs` only from the base branch,
   never a pull-request head — so a pull request cannot present its own widened
   scope to the check that authorizes it. (Neutral doctrine here; enforced in the
   codexFactory verifier.)
2. **Ratification-covered.** The `scope_globs` bytes are part of the ratified
   change artifact and covered by the change's ratification, so a governed pull
   request can never widen its own scope post-ratification.
3. **Non-author-mutable.** The `openspec/changes/` surface that carries
   `scope_globs` is a never-clearable floor member of EVERY enrolled repository,
   and no autonomous provenance merge may write it — closing the
   self-authorization recursion (an earlier governed merge cannot author the
   scope a later tie corroborates against). This is symmetric with how B floors
   its other trust-root sources.
4. **Frozen after ratification.** The archive gate rejects mutation of
   `scope_globs` after ratification (the "Scope retention at archive"
   requirement), mirroring "Origin retention at archive."

The staged topic listed the freeze/immutability as an OPEN question (Q3a); B's
CRITICAL #1 forces it, so this design ELEVATES the freeze from optional to a
REQUIRED property (Scope retention at archive) and carries only the SECOND half of
that open question — whether the archive gate additionally asserts realized paths
⊆ scope (Q3b) — forward for ratification.

## Risks / trade-offs

- **Field drift** (`scope_globs` names a repo `code_surface` omits, or a scope is
  stale vs the realized diff) — mitigated by the cross-consistency check and the
  base-read + freeze properties; fully closing the "realized ⊆ scope" gap is
  deferred (Q3b).
- **Dialect drift from the engine** — mitigated by conforming the validator's
  rejection set to `_validate_path_allowlist` and pinning it by test to the same
  fixtures; if the envelope engine ever changes its dialect, the validator's
  mirror must be updated in lockstep (a Speckit-feature task note).
- **Over-declaration naming a floor path** — accepted by design: validation allows
  it, the verifier's floor override parks it. Floor always wins.
- **Verbose front-matter for large scopes** — accepted for v1; the sidecar
  affordance (Q1) is the escape hatch if it bites.

## Open questions (carried forward for the convener ratification read, task 1.5)

These are the residual alignment/council concerns from the staged topic. The
`opsx:propose` alignment-review + council-debate flow was not run headless in this
authoring session; these stand in for its surfaced concerns.

1. **Front-matter map vs `scope_globs.yaml` sidecar (D3).** Keep front-matter-only
   for v1 and accept verbose YAML for large scopes, or allow a sidecar as an
   alternative representation now?
2. **Map vs flat list (D2).** Keep the per-repository map, or — if provenance
   pull requests are always single-repo in practice — a flat list keyed
   implicitly by the pull request's repo?
3. **Archive-gate closure.** The freeze half (reject post-ratification mutation)
   is now REQUIRED by CRITICAL #1 and specified as "Scope retention at archive."
   OPEN: should the archive gate ALSO assert that the realized pull request's
   changed paths fell within `scope_globs` (a provenance closure making the
   declared scope auditable against what shipped)?
4. **Ordered-delta scope composition.** When a change is an ordered delta on
   another (B itself is one), does `scope_globs` inherit/compose across the chain,
   or does each change declare its own standalone scope? B calls multi-delta chain
   resolution "a realization detail left to the follow-on"; confirm the
   substrate's stance.
5. **Advisory floor lint in openxFactory (D5).** Keep `openspec validate`
   strictly floor-agnostic and rely solely on the verifier's check-time override,
   or add a best-effort advisory lint that warns when `scope_globs` names a path
   matching a vendored copy of a known repository floor?
6. **Ratification authority.** Does this substrate change — which defines an input
   the autonomous-merge path consumes — need `gate_rules_council` sign-off in
   addition to Brett's convener ratification, given B's realization depends on it?
