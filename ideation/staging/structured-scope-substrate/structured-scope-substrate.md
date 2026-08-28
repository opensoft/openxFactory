# Staged: Structured path-scope substrate for provenance-gated merge

Status: staged
Kind: architecture
Summary: A machine-readable path-scope declaration on ratified OpenSpec changes —
a new `scope_globs:` sibling to `code_surface:` carrying a per-repository glob
allowlist in the merge-gate envelope dialect — so the provenance-tie verifier in
`add-provenance-gated-autonomous-merge` can mechanically check that a PR's
changed files stay WITHIN the scope its ratified change declared. Resolves that
change's Open Question 2 (amend `code_surface` vs a new sibling field) in favour
of a new, additive, non-breaking sibling.
Topics: release-realization, code_surface, provenance-gated-merge, path-scope, glob-dialect, merge-master, never-clearable-floor, backward-compat
Repository context: openxFactory owns the neutral `release-realization`
capability that defines `code_surface:` / `target_release:` change front-matter
(`openspec/specs/release-realization/spec.md`). The consuming verifier and the
glob engine the substrate must align with live in codexFactory
(`scripts/merge_master/envelope.py`, `scripts/merge_master/council_clearance.py`);
the substrate is declared and validated in openxFactory, consumed at merge time
per enrolled repo.
Staging ID: openxFactory:staging:structured-scope-substrate
Source: `add-provenance-gated-autonomous-merge` (openxFactory, branch
`change/add-provenance-gated-autonomous-merge`) design D6 + Open Question 2, and
its proposal's "Structured-path-scope precondition" impact line: the ratified
`code_surface:` field is repository-granularity prose (`release-realization`
`:7-8`), so it cannot bound a changed-path set; the provenance-tie verifier
"is not buildable-as-described against prose `code_surface`." Named there as an
explicit, human-gated `openspec/`-touching PRECONDITION that must land before any
provenance-eligible code class can be published.
Target capabilities: release-realization (MODIFIED)

## 1. Problem statement + current-state survey

### The problem

`add-provenance-gated-autonomous-merge` (the "B" change) proposes an interim
eligibility axis under which a fully-governed code PR can become autonomously
clearable. Its buildable core is a provenance-tie verifier that, at clearance
time from the base branch, must confirm (verifier step iii) that

> the PR's changed paths fall WITHIN the ratified change's MACHINE-READABLE path
> scope — a glob allowlist, NOT prose `code_surface` — so the tie proves the diff
> was authorized, not merely that a same-named ratified change exists; a change
> whose scope is prose or repository-level is INELIGIBLE, never "all paths in
> scope."

Today that substrate does not exist. A change declares its realization surface
as `code_surface:` front-matter whose ratified contract is **repository
granularity** ("`none` or the repositories whose runtime artifacts it changes",
`release-realization/spec.md:4-6`). A repository name cannot bound a set of
changed file paths, so the containment check has nothing to evaluate against.
B's design records this as D6 ("A machine-readable path-scope substrate is a hard
precondition") and Open Question 2: amend `code_surface` into a structured field,
OR add a new structured sibling field. This topic resolves Q2 and designs the
substrate.

### Current-state survey (measured)

Measured on openxFactory `origin/main` (`6612d323`), the openxFactory
`openspec/changes/` tree:

- **`code_surface` appears 164 times** across change proposals, tasks, designs,
  and ruling records (`grep -rn 'code_surface' openspec/changes/` → 164 lines).
- **Front-matter declarations** (`^code_surface:` at proposal top), by distinct
  form:

  | Form | Count | Example |
  | --- | --- | --- |
  | Bare repository name(s) | 11 | `code_surface: openxFactory` |
  | `none` (doc-only) | 5 | `code_surface: none` |
  | Bare repo name(s), other repos | 3 | `code_surface: codexFactory` |
  | Comma-list of repositories | ~4 | `openxFactory, codexFactory, xFactory, …` |
  | Repo name + parenthetical prose | ~20 | `openxFactory (scripts/doc_health/ …)` |
  | Multi-sentence prose paragraph | ~6 | the openxwallet split (a ~600-word paragraph naming dozens of files across six repos) |

  Every declaration is **prose**: even the forms that name specific paths do so
  inside free text (`openxFactory (scripts/doc_health/ neutrality lane + …)`),
  never as an enumerable, dialect-conformant glob list.

- **No validator parses `code_surface` as structured data.** The only readers
  are `scripts/ideation_dashboard/generator.py` (`_release_frontmatter` →
  `_header_value(text, "code_surface")`, a free-text header value shown on the
  dashboard) and two doc-health comments. `openspec validate` does NOT check the
  field's form; the `release-realization` archive gate consumes it as prose. So
  the field is today free-form and unvalidated.

This is the load-bearing survey fact for the backward-compat story below: there
are **~45+ active changes with a prose/repo-name/`none` `code_surface`, none in a
machine-checkable form, and no validator enforcing any form.** Any resolution
that redefines `code_surface` breaks every one of them.

## 2. Q2 RESOLVED — a NEW sibling field (`scope_globs:`), not amending `code_surface`

**Recommendation: add a new, OPTIONAL, additive sibling front-matter field
`scope_globs:`. Do NOT amend `code_surface` into a structured field.**

### Rationale

1. **Backward-compat is decisive.** Amending `code_surface` is a breaking,
   flag-day migration: all ~45+ active changes (and every archived change the
   archive gate and dashboard read) declare it in prose/repo-name/`none` forms
   that a structured schema would reject. A sibling field is **additive and
   non-breaking**: every existing prose-`code_surface` change keeps working
   unchanged; it is simply **not provenance-eligible** until it also declares
   `scope_globs`. This is exactly the posture B already assumes — "prose or
   repository-level scope ⇒ ineligible, never 'all paths in scope'" — so a
   sibling field realizes B's own default without touching anything else.

2. **The two fields answer different questions at different granularities.**
   `code_surface` answers *which repositories' runtime artifacts change* — a
   release-realization / archive-gate concern that drives the per-repo
   merged-plus-green gate. `scope_globs` answers *which paths within an enrolled
   repo the diff may touch* — a provenance-verifier / merge-gate concern. They
   have different consumers and different natural cardinality. Overloading one
   field to carry both a repo list and a path allowlist would entangle two axes —
   the same entanglement B's D1 rejected for eligibility ("keep the floor a
   single, axis-independent invariant").

3. **Optionality preserves the doc-only default.** `code_surface: none`
   doc-only changes (5 today) and every change that never seeks the provenance
   axis carry no `scope_globs` and are untouched. Making structured scope
   *required for all changes* would force a path allowlist onto pure governance
   documents that have no code paths at all — nonsensical and needlessly
   breaking.

4. **`code_surface` prose stays useful.** The prose forms carry real
   information (rationale, cross-repo sequencing, "this change's own diff vs
   downstream realization"). A sibling adds the machine-readable layer WITHOUT
   discarding that prose, so nothing is lost.

**Trade-off acknowledged:** two fields can drift (a `scope_globs` that names a
repo `code_surface` omits, or vice versa). Handled by a cross-consistency check
in validation (§4) rather than by collapsing the fields.

## 3. The substrate shape

### The field

A new OPTIONAL front-matter key `scope_globs:` in a change's `proposal.md` YAML
front-matter, sibling to `code_surface:` / `target_release:` (the same block the
ratified realization-axis declarations already live in — one source of truth,
one place the archive gate and origin-retention already read).

### Value form

A **mapping from repository name → list of repository-relative globs** in the
**merge-gate envelope dialect** (§ glob-dialect alignment, and §4). A mapping
(not a flat list) because a change's `code_surface` may name multiple
repositories, and containment is evaluated **per repository** against a PR that
lives in exactly one repo; the verifier selects the entry for the PR's repo. The
repo keys are a subset of `code_surface`'s repositories.

### Where declared

**In the change front-matter**, not a separate scope file. Rationale: the scope
belongs beside its `code_surface` prose sibling so the two are read, validated,
and origin-retained together; front-matter is already the ratified home for the
realization-axis declarations. (A `scope_globs.yaml` sidecar for very large
scopes is a named future affordance — see Open Questions — but front-matter is
the v1 home.)

### Worked example

A realizing codexFactory change that touches only the doc-health neutrality lane
and its tests would declare:

```yaml
---
code_surface: codexFactory (the doc-health neutrality lane + its suite)
target_release: implemented
scope_globs:
  codexFactory:
    - "scripts/doc_health/neutrality/**"
    - "scripts/doc_health/dispatch.py"
    - "tests/doc-health/test_neutrality_lane.py"
---
```

The verifier, evaluating a codexFactory PR tied to this ratified change, reads
`scope_globs["codexFactory"]` and confirms every changed path matches at least
one of those three globs using the SAME glob engine the envelope floor uses. A
PR that also touched `scripts/merge_master/envelope.py` would be parked: that
path matches none of the globs (out of scope) AND lies inside codexFactory's
`scripts/**` never-clearable floor (floor override) — either alone is
disqualifying.

Illustration of what the dialect FORBIDS (each would fail validation, §4):

```yaml
scope_globs:
  codexFactory:
    - "/scripts/doc_health/**"   # REJECTED: leading slash matches no repo-relative path
    - "**"                        # REJECTED: universal — complement of the empty set
    - "!scripts/merge_master/**"  # REJECTED: negation — the dialect has none
```

## 4. Validation (`openspec validate`)

The eventual change adds a validation requirement to `release-realization` and a
validator hook so `openspec validate --strict` enforces, when `scope_globs` is
present:

1. **Structure.** `scope_globs` is a mapping of string repo-key → non-empty list
   of non-empty strings; entries within a list are unique.
2. **Dialect conformance** (mirrors codexFactory
   `envelope.py:_validate_path_allowlist`, the authoritative implementation):
   - reject any entry starting with `/` (leading-slash — unreachable against
     repo-relative changed paths; "the CODEOWNERS dialect is not this one");
   - reject any entry starting with `!` (negation — the dialect has none; a
     surface expressed by subtraction is a complement that fails open);
   - reject the universal patterns `**`, `*`, `**/*`, `/**`, `./**` (each admits
     every path — the complement of the empty set — which would leave the floor
     the only control);
   - reject complement/denylist shapes (no `path_denylist`-style keys).
3. **Well-formedness.** Each glob compiles under the envelope dialect
   (`**` = zero+ segments, `*` = non-separator run, `?` = one non-separator,
   anchored full-match).
4. **Cross-consistency with `code_surface`.** Every repo key in `scope_globs`
   MUST be named in `code_surface` (a scope may not authorize a repo the change
   does not declare a surface for). The reverse is NOT required — a change may
   name a repo in `code_surface` without giving it a scope (that repo's
   realization simply isn't provenance-eligible).

### The floor relationship — RECOMMENDATION: floor overrides at CHECK time; `openspec validate` does NOT reject floor paths

`openspec validate` runs in **openxFactory** and CANNOT know each enrolled repo's
never-clearable floor: the floor is **tree-specific and per-repo**, published in
that repo's `.github/merge-approval-envelope.yml` `gate_integrity.never_clearable_paths`
(`scripts/**` = "the decision core" holds in codexFactory, not necessarily
elsewhere — B's D4). So validation stays floor-agnostic: it does NOT reject a
`scope_globs` entry that happens to name a floor path.

Instead the **floor overrides at verify time** — and this is not a new
invention, it is the semantics codexFactory already ships. `council_clearance.py`
already evaluates the floor as a SUBTRACTION from the allowlist:

> the floor subtracts from the allowlist (design D1), so a gate-integrity path
> that happens to sit inside the tier-1 allowlist is floored too
> (`_gate_integrity_problem`, quantified over EVERY changed path, not merely the
> overflow).

Reusing that rule for `scope_globs` gives exactly ONE floor authority (the
repo's envelope), so scope checks and floor checks cannot disagree. A change may
over-declare scope (even naming a floor path); the verifier still parks any PR
whose diff touches the floor. **Floor always wins; scope can never authorize a
floor path.** An optional repo-side ADVISORY lint MAY warn when a change's
`scope_globs` names a known floor path, but that is advisory, never an
`openspec validate` gate (openxFactory would have to vendor every enrolled repo's
floor to gate on it, coupling the neutral validator to each domain's tree — the
coupling B's portability requirement forbids).

## 5. Verifier consumption

Given a PR in enrolled repo `R`, head `H`, base `B`, tied (per B's D3, by
base-read corroboration) to currently-ratified change `C`:

1. **Select scope.** Read `C.scope_globs[R]`. If `scope_globs` is absent, has no
   entry for `R`, or `R`'s entry is empty ⇒ **INELIGIBLE**, park with the named
   condition ("no machine-readable scope declared for repo R"). Prose or
   repo-level `code_surface` alone never satisfies this — exactly B's step iii.
2. **Compute changed files.** `F` = the PR's changed paths, repo-relative, from a
   name-status diff of `H` against `B`.
3. **Containment (SAME engine as the floor).** Every `f ∈ F` MUST satisfy
   `envelope.path_matches(f, C.scope_globs[R])` — the identical function
   (`envelope.py:path_matches` → `_glob_to_regex`) the floor uses. Any `f`
   matching none ⇒ park ("changed path outside declared scope: <f>").
4. **Floor override.** Load `R`'s `.github/merge-approval-envelope.yml`
   `gate_integrity.never_clearable_paths` from BASE `B` (the tree-validated
   floor, never head). Any `f` with `path_matches(f, floor)` ⇒ park
   never-clearable ("floor path in diff: <f>"), REGARDLESS of whether
   `scope_globs` named it. Floor wins.
5. **Eligible** only if `F ⊆ scope_globs[R]` AND `F ∩ floor = ∅`, in addition to
   B's other criteria (enrolled; currently-ratified + signed record; all
   required checks green; SHA-pinned to the verdict).

**Fail-closed + legible-park.** Any unreadable/absent scope, unparseable glob,
unreadable floor, empty-`F` edge case, or ambiguous tie ⇒ park for human review,
and the park record names WHICH condition/sub-check failed (containment vs floor
vs missing-scope vs malformed) — matching B's "fail-closed + legible" contract.

## 6. Backward-compat / migration

- **No flag-day, no migration pass.** `scope_globs` is optional; its absence
  means "not provenance-eligible," which is the pre-existing state of every
  change. The ~45+ active changes with prose/repo-name/`none` `code_surface` keep
  validating and archiving unchanged.
- **Grandfather as not-provenance-eligible.** Existing changes are neither
  broken nor auto-migrated; they simply cannot use the provenance axis until an
  author adds `scope_globs`. Migration is **opt-in, per change, at authoring
  time**, only when a change wants the provenance-gated path.
- **Not required for all changes.** Structured scope is REQUIRED only for a
  change whose realization PR seeks provenance-gated autonomous merge. Doc-only
  and prose-realized changes never need it. This keeps the doc-only default
  (`code_surface: none`, `target_release: implemented`) intact.
- **`code_surface` unchanged.** Its ratified contract, prose forms, dashboard
  reader, and archive-gate consumption are all untouched.

## 7. Interactions

- **Never-clearable floor (`gate_integrity.never_clearable_paths`)** — always
  overrides at verify time (§4-recommendation, §5 step 4). Single floor
  authority per repo; `scope_globs` can never authorize a floor path. The floor
  is checked with the SAME `path_matches` engine as scope, so the two agree by
  construction.
- **Enrollment envelope (`.github/merge-approval-envelope.yml`)** — the
  per-enrolled-surface `path_allowlist` (a CLASS allowlist) is distinct from a
  change's `scope_globs` (a per-CHANGE allowlist), but both use the same dialect
  and the verifier reads both from base. Enrollment presence is B's criterion 1;
  scope containment is verifier step iii. The two allowlists compose: a PR must
  fall within its class allowlist AND within its tied change's `scope_globs` AND
  outside the floor.
- **`add-repo-enrollment` PR route** — unaffected. `scope_globs` lives in
  openxFactory change front-matter, not in the envelope, so the owner-verified,
  machine-prepared enrollment PR against the protected envelope path does not
  carry it and is not bypassed.
- **`release-realization` archive gate** — `scope_globs` is a sibling to
  `code_surface`; v1 keeps it validate-only. Two candidate closures are deferred
  to Open Questions: (a) origin-retention-style immutability (reject mutation of
  `scope_globs` after ratification, mirroring the origin-retention requirement);
  (b) archive-time assertion that the realized PR's paths fell within
  `scope_globs` — a provenance closure that would make the declared scope
  auditable against what actually shipped.
- **B's provenance-tie verifier** — this substrate IS B's D6 precondition; B's
  step iii consumes `scope_globs[R]`. B stays doctrine; the codexFactory
  realization consumes both.

## Claims

1. Amending `code_surface` into a structured field is breaking (~45+ active
   changes + all archived changes carry prose/repo-name/`none` forms; no
   validator enforces any form today); a new optional sibling `scope_globs:` is
   additive and non-breaking. (Measured, §1.)
2. `scope_globs` must carry repository-relative globs in the codexFactory
   envelope dialect (`envelope.py:_glob_to_regex` / `_validate_path_allowlist`:
   no leading slash, no negation, no universal pattern, anchored full-match), so
   the verifier's containment check and the never-clearable floor check use the
   SAME engine and cannot disagree. (Verified against codexFactory `origin/main`
   `2b16ec5`; the glob region is byte-identical to the pinned checkout.)
3. The floor overrides at CHECK time, not at declaration time: `openspec
   validate` (in openxFactory) stays floor-agnostic because the floor is
   tree-specific and per-repo; the verifier subtracts the repo's own base-branch
   floor from the authorized set, reusing the shipped
   `_gate_integrity_problem` "floor subtracts from the allowlist" semantics — one
   floor authority, no disagreement.
4. Structured scope is required only for provenance-eligibility, never for all
   changes; grandfathering existing changes as not-eligible needs no migration
   pass.

## Open questions

1. **Front-matter map vs `scope_globs.yaml` sidecar.** Recommend front-matter
   for v1; but the openxwallet split's ~600-word `code_surface` shows scopes can
   get large. Allow a sidecar as an alternative representation, or keep it
   front-matter-only and accept verbose YAML?
2. **Map vs flat list.** Recommend a per-repo map (a change may span repos;
   containment is per-repo). If provenance PRs are always single-repo in
   practice, a flat list keyed implicitly by the PR's repo is simpler — confirm
   the map is warranted.
3. **Archive-gate closure.** Should the `release-realization` archive gate (a)
   freeze `scope_globs` against post-ratification mutation (origin-retention
   style), and/or (b) assert the realized PR's paths fell within `scope_globs`?
4. **Ordered-delta scope composition.** When a change is an ordered delta on
   another (B itself is one), does `scope_globs` inherit/compose across the
   chain, or does each change declare its own standalone scope? B calls
   multi-delta chain resolution "a realization detail left to the follow-on."
5. **Advisory floor lint in openxFactory.** Keep `openspec validate`
   floor-agnostic (recommended) and rely solely on the verifier's check-time
   override, or add a best-effort advisory lint that warns when `scope_globs`
   names a path matching a vendored copy of a known repo floor?
6. **Ratification authority.** Does the substrate change — which feeds the merge
   gate — need Gate-Rules Council sign-off in addition to Brett's ratification,
   given it defines an input the autonomous-merge path consumes?

## Exit path

An openxFactory OpenSpec change (human-gated, `openspec/`-touching per B's D6)
that MODIFIES `release-realization`:

- ADDS the optional `scope_globs:` sibling declaration to the realization-axis
  requirement (value form: per-repo map of envelope-dialect globs; optional;
  required only for provenance-eligibility);
- ADDS a validation requirement + validator hook so `openspec validate --strict`
  enforces structure, dialect conformance, well-formedness, and
  `code_surface` cross-consistency (§4);
- states the floor-overrides-at-check-time relationship (§4-recommendation) as
  neutral doctrine, leaving the check-time enforcement to the codexFactory
  verifier.

This change has a real `code_surface: openxFactory` (the spec delta + the
validator extension), so it archives on merged-plus-green per
`release-realization`. It is the named precondition in B's Migration Plan step 2;
the codexFactory provenance-tie verifier (B's downstream realization) is the
first consumer. Ordered-delta note: if B's `roles-authority-model` delta is still
active when this is authored, this change is independent of B (it touches
`release-realization`, not `roles-authority-model`) and may proceed in parallel;
only the codexFactory realization depends on BOTH landing.
