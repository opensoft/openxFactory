---
code_surface: openxFactory (this change's ONLY diff is the `release-realization` spec delta plus the follow-on `openspec validate` extension it specifies — a validator hook + a lightweight schema for the `scope_globs:` front-matter field, landing under openxFactory `scripts/` and `openspec/`. It amends the neutral realization-axis front-matter contract and its validator; it touches no domain repository's tree. The codexFactory provenance-tie verifier that CONSUMES `scope_globs` is downstream and explicitly NOT built here — it is the realization of `add-provenance-gated-autonomous-merge`, tracked in that change's tasks, not this one.)
target_release: implemented (the affected repository's main line — openxFactory. Realization = the `scope_globs:` field is validated by `openspec validate --strict` and available for the provenance-tie verifier to consume; the change archives on merged-plus-green per `release-realization` once the validator extension lands and its suite runs green. There is no aggregation-repo release bundle.)
---

# Proposal: add-structured-scope-substrate

Status: draft
Authored: 2026-08-28, as the first exit of the staged topic
`openxFactory:staging:structured-scope-substrate`.
Directed by: the staged topic fragment (Brett Heap, openxFactory operator
authority, 2026-08-28), which cleared the topic to exit as a change.
Authoring method: hand-authored per openxFactory OpenSpec conventions. The
`opsx:propose` alignment-review + council-debate flow was NOT run headless in
this authoring session; the design decisions it would surface are already
RESOLVED in the staged topic (Q2, the glob dialect, floor-override-at-check-time,
the per-repo map, and the grandfather backward-compat story), and the residual
alignment/council concerns are carried forward verbatim as this proposal's Open
Questions (see `design.md` § Open questions) for the convener read at task 1.5.

## Why

`add-provenance-gated-autonomous-merge` (the "B" change, ratified AS AMENDED by
the `gate_rules_council` on 2026-08-28) makes a fully-governed code pull request
autonomously clearable on a new PROVENANCE axis. Its buildable core is the
"Provenance-tie verifier contract" (openxFactory `roles-authority-model`), whose
step (iii) must confirm at clearance time, from the base branch, that

> the pull request's changed paths fall WITHIN the tied change's MACHINE-READABLE
> path scope (a glob allowlist), treating a change whose declared scope is prose
> or repository-level as INELIGIBLE rather than as "all paths in scope."

**Today that substrate does not exist.** A change declares its realization
surface as `code_surface:` front-matter whose ratified contract is REPOSITORY
GRANULARITY — "`none` or the repositories whose runtime artifacts it changes"
(`release-realization`, "Realization axis declaration"). A repository name cannot
bound a set of changed file paths, so the containment check has nothing to
evaluate against. Measured on openxFactory `origin/main` (`6612d323`),
`code_surface` appears 164 times across `openspec/changes/`, every declaration is
PROSE — even the forms that name paths do so inside free text
(`openxFactory (scripts/doc_health/ …)`), never as an enumerable,
dialect-conformant glob list — and NO validator parses the field as structured
data (`openspec validate` does not check its form; the only readers are the
ideation dashboard's free-text header value and two doc-health comments). B
records this as its design D6 ("A machine-readable path-scope substrate is a hard
precondition") and Open Question 2, and names it in B's Migration Plan step 2 as
an explicit, human-gated `openspec/`-touching PRECONDITION that must land before
any provenance-eligible code class can be published.

**This is the first HARD, human-gated precondition of the provenance-gated
autonomous-merge program.** It is also load-bearing for the floor: B's folded
CRITICAL #1 (now in the "Floor primacy and per-repository floor instantiation"
requirement) makes the machine-readable path-scope substrate a TRUST-ROOT source
(iv) that "SHALL be a never-clearable floor member of EVERY enrolled repository"
and to which "No autonomous provenance merge SHALL write." This change must make
`scope_globs` satisfy exactly those trust-root/floor/non-author-mutable
properties, or the verifier it feeds cannot be trusted.

## What Changes

This change MODIFIES the neutral `release-realization` capability. It adds NO
runtime behavior to any domain repository; it defines the field, its validation,
and its trust-root integrity as neutral doctrine, and leaves the check-time
consumption to the codexFactory provenance-tie verifier (B's downstream
realization).

- **A new, OPTIONAL, additive front-matter sibling field `scope_globs:`** on a
  change's `proposal.md`, sibling to `code_surface:` / `target_release:` (the
  same realization-axis block the archive gate and origin-retention already
  read). Its value is a MAPPING from repository name → non-empty list of
  repository-relative globs in the merge-gate ENVELOPE DIALECT. It is NOT an
  amendment to `code_surface`: Open Question 2 is resolved in favour of a
  sibling, because amending `code_surface` would be a flag-day break of every one
  of the 45+ active prose/repo-name/`none` declarations, whereas a sibling is
  additive and leaves them all validating and archiving unchanged.

- **Absence is fail-closed, never "all paths."** A change with no `scope_globs`,
  or with no entry for a given repository, is NOT provenance-eligible for that
  repository. This realizes B's default ("prose or repository-level scope ⇒
  ineligible, never 'all paths in scope'") without touching anything else.
  Structured scope is REQUIRED only for provenance-eligibility; doc-only and
  prose-realized changes never need it, and `code_surface: none` stays intact.

- **`openspec validate --strict` enforces the field when present**: structure (a
  mapping of string repo-key → non-empty, unique list of non-empty strings);
  dialect conformance (rejecting the envelope dialect's forbidden forms —
  leading-slash, negation, universal patterns, complement/denylist keys);
  well-formedness (each glob compiles under the envelope dialect); and
  cross-consistency (every repo key in `scope_globs` MUST be named in
  `code_surface`). The validator stays FLOOR-AGNOSTIC — it does NOT reject a
  glob that happens to name a floor path, because the never-clearable floor is
  tree-specific and per-repo and is applied at CHECK time by the verifier, not at
  `openspec validate` time.

- **The dialect is the codexFactory merge-gate envelope's single glob engine**
  (`scripts/merge_master/envelope.py`, `_glob_to_regex` / `path_matches` /
  `_validate_path_allowlist`), so the verifier's containment check and the
  never-clearable floor check use the SAME engine and cannot disagree. The
  validator's rejection rules mirror `_validate_path_allowlist` exactly:
  `**`/`*`/`**/*`/`/**`/`./**` (universal), leading `/`, leading `!` (negation),
  and any `path_denylist`-style complement key are refused.

- **Trust-root integrity bound to ratification.** The `scope_globs` declaration
  is BASE-READ (the verifier reads it from the base branch, never from a PR
  head), RATIFICATION-COVERED (it is part of the ratified change artifact; its
  bytes are covered by the change's ratification, so a governed PR can never
  widen its own scope post-ratification), NON-AUTHOR-MUTABLE (the
  `openspec/changes/` surface that carries it is a never-clearable floor member
  in every enrolled repository, and no autonomous provenance merge may write it),
  and FROZEN AT ARCHIVE (the archive gate rejects mutation of `scope_globs` after
  ratification, mirroring the existing "Origin retention at archive"
  requirement). These four properties are exactly B's CRITICAL #1 trust-root
  source (iv) requirements, restated as a `release-realization` obligation on the
  field.

- **The floor overrides at CHECK time, as neutral doctrine.** `openspec validate`
  (in openxFactory) stays floor-agnostic; the verifier subtracts the enrolled
  repository's own base-branch never-clearable floor from the authorized set,
  reusing the shipped `_gate_integrity_problem` "floor subtracts from the
  allowlist" semantics. One floor authority per repository; `scope_globs` can
  never authorize a floor path; floor always wins.

Ratifying this doctrine unlocks no autonomous merge by itself. It makes the
`scope_globs` field validated and available; B's provenance-tie verifier (built
downstream in codexFactory, against a current codexFactory checkout) is the first
consumer.

## Impact

- **Affected spec:** `release-realization` (MODIFIED). One requirement is
  MODIFIED ("Realization axis declaration", to add the optional `scope_globs:`
  sibling); four requirements are ADDED (structured-scope validation;
  trust-root integrity of the scope declaration; scope retention at archive; the
  floor-overrides-at-check-time neutral doctrine).

- **Affected code (this change's `code_surface`, built later via Speckit):** the
  `openspec validate` extension — a validator hook + a lightweight schema for the
  `scope_globs` field — under openxFactory `scripts/` and `openspec/`. This
  change AUTHORS only the proposal artifacts; per the house rule (OpenSpec
  ratifies, Speckit builds) the validator/schema code is built post-ratification
  via the Speckit features mapped in `tasks.md`.

- **This change is NOT itself provenance-eligible.** It is an
  `openspec/`-touching, human-gated change (B's D6 class); it therefore declares
  no `scope_globs` of its own and seeks no autonomous merge. That is the correct
  posture: the substrate is authored by the human-gated route it protects.

- **Backward-compat:** no flag-day, no migration pass. Every existing change with
  a prose/repo-name/`none` `code_surface` keeps validating and archiving
  unchanged; `code_surface`'s ratified contract, prose forms, dashboard reader,
  and archive-gate consumption are all untouched. Existing changes are
  grandfathered as not-provenance-eligible; migration is opt-in, per change, at
  authoring time.

- **Interactions:** the never-clearable floor (`gate_integrity.never_clearable_paths`)
  overrides at verify time; the enrollment envelope's per-class `path_allowlist`
  composes with a change's per-change `scope_globs` (both in the same dialect,
  both base-read); the `add-repo-enrollment` PR route is unaffected
  (`scope_globs` lives in openxFactory change front-matter, not the envelope);
  B's provenance-tie verifier consumes `scope_globs[R]` at step (iii).

- **Dependency ordering:** independent of B's `roles-authority-model` delta (this
  touches `release-realization`) and may proceed in parallel; only the
  codexFactory verifier realization depends on BOTH landing.
