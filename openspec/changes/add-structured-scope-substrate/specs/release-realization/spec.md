# release-realization Specification

This delta MODIFIES the `release-realization` capability to add a machine-readable
path-scope substrate — the optional front-matter field `scope_globs:` — alongside
the existing `code_surface:` / `target_release:` realization-axis declarations.

The MODIFIED requirement below is declared RELATIVE TO the promoted
`release-realization` spec (`openspec/specs/release-realization/spec.md`,
"Realization axis declaration"); no active ratified change currently modifies it,
so the deltas are relative to the promoted outcome. The ADDED requirements are new
to the capability. `code_surface:` and `target_release:` are UNCHANGED: their
ratified contract, prose forms, dashboard reader, and archive-gate consumption
are untouched, and this change adds the machine-readable layer as an OPTIONAL
sibling without discarding the prose.

## MODIFIED Requirements

### Requirement: Realization axis declaration
Every OpenSpec change proposal SHALL declare `code_surface:` — `none` or the
repositories whose runtime artifacts it changes — and `target_release:` —
`implemented` (the affected repositories' main lines) or a named release defined
in the aggregation repository. A proposal without the declarations is a doc-only
change (`code_surface: none`, `target_release: implemented`) by default. A
proposal MAY ALSO declare an OPTIONAL sibling field `scope_globs:` carrying a
machine-readable path scope (defined in the "Structured path-scope declaration"
requirement); its ABSENCE is the pre-existing default and leaves the change
exactly as it is today — a proposal is never required to declare `scope_globs`,
and its absence never means "all paths."

#### Scenario: A doc-only change is proposed
- **WHEN** a change alters only governance documents, schemas-as-documents, or contract prose
- **THEN** its code_surface is `none` and it archives when its artifacts land, as before
- **AND** it declares no `scope_globs` and is unaffected by the structured-scope substrate

#### Scenario: A code-surface change is proposed
- **WHEN** a change alters scripts, workflows, services, or other runtime artifacts
- **THEN** its proposal MUST declare the affected repositories as code_surface and its target release

#### Scenario: A change declares no structured scope
- **WHEN** a change omits `scope_globs` entirely
- **THEN** it validates and archives exactly as before, and it is simply not provenance-eligible until an author adds `scope_globs` — its absence is never interpreted as an unbounded or repository-wide scope

## ADDED Requirements

### Requirement: Structured path-scope declaration
The `scope_globs:` field SHALL be an OPTIONAL front-matter sibling to
`code_surface:` / `target_release:` whose value is a MAPPING from repository name
to a non-empty list of repository-relative globs in the merge-gate envelope
dialect, declaring the paths within each named repository that the change's
realization pull request may touch. The field exists so a provenance-tie verifier
can mechanically confirm that a pull request's changed paths fall WITHIN the
scope its ratified change declared; a repository name alone (which `code_surface`
supplies) cannot bound a set of changed paths. Structured scope SHALL be REQUIRED
only for provenance-eligibility and never for all changes: a change whose
declared scope for a repository is absent, prose, or repository-level SHALL be
INELIGIBLE for the provenance axis in that repository, treated as ineligible
rather than as "all paths in scope" (fail-closed). Existing changes that declare
no `scope_globs` SHALL be grandfathered as not-provenance-eligible with no
migration pass, and `code_surface` SHALL remain unchanged as the
repository-granularity realization declaration that drives the archive gate.

The value SHALL be a per-repository MAPPING rather than a flat list because a
change's `code_surface` may name multiple repositories and containment is
evaluated PER repository against a pull request that lives in exactly one repo;
every repository key present in `scope_globs` SHALL also be named in
`code_surface`, while the reverse is NOT required (a `code_surface` repository may
have no scope, and its realization is then simply not provenance-eligible).

#### Scenario: A change declares a structured scope
- **WHEN** a change's realization pull request seeks the provenance-gated autonomous-merge path in an enrolled repository
- **THEN** the change MUST declare `scope_globs` with a non-empty list of envelope-dialect globs under that repository's key
- **AND** every path the realization pull request changes must fall within one of those globs for the pull request to be provenance-eligible

#### Scenario: A repository is in code_surface but has no scope entry
- **WHEN** `code_surface` names a repository that `scope_globs` does not
- **THEN** the change is valid, and that repository's realization is simply not provenance-eligible until an author adds its scope entry

#### Scenario: Scope declares a repository absent from code_surface
- **WHEN** a `scope_globs` key names a repository that `code_surface` does not declare
- **THEN** validation fails, because a scope may not authorize a repository the change declares no realization surface for

### Requirement: Structured path-scope validation
When `scope_globs` is present, `openspec validate --strict` SHALL enforce its
well-formedness and dialect conformance and SHALL remain FLOOR-AGNOSTIC. The
validator SHALL require that `scope_globs` is a mapping of string repository-key
to a non-empty list of non-empty, unique strings; SHALL require that every
repository key is also named in `code_surface` (cross-consistency); and SHALL
require that every glob conforms to the merge-gate envelope dialect — the single
glob engine (`_glob_to_regex` / `path_matches` / `_validate_path_allowlist`) that
the never-clearable floor uses — so the verifier's containment check and the
floor check cannot disagree. Dialect conformance SHALL reject: any entry starting
with `/` (leading-slash — changed paths are repository-relative and never match
it; the CODEOWNERS dialect is not this one); any entry starting with `!`
(negation — the dialect has none, and a surface expressed by subtraction is a
complement that fails open); the universal patterns `**`, `*`, `**/*`, `/**`, and
`./**` (each admits every path — the complement of the empty set — which would
leave the floor the only control); and any complement/denylist-shaped key
(`path_denylist` and its siblings). The validator SHALL NOT reject a glob merely
because it names a path that happens to lie inside some repository's
never-clearable floor: the floor is tree-specific and per-repository, published
in that repository's own envelope, and is applied at CHECK time by the verifier,
not at `openspec validate` time — so making the neutral validator floor-aware
would require it to vendor every enrolled repository's floor and would couple it
to each domain's tree, which the portability requirement forbids.

#### Scenario: A malformed or non-dialect scope is validated
- **WHEN** a `scope_globs` entry starts with `/` or `!`, is a universal pattern, uses a complement/denylist key, or the value is not a mapping of repo-key to a non-empty unique string list
- **THEN** `openspec validate --strict` fails with a message naming the offending entry and the dialect rule it breaks

#### Scenario: A well-formed scope names a floor path
- **WHEN** a `scope_globs` glob happens to match a path inside some repository's never-clearable floor
- **THEN** `openspec validate --strict` still passes — the neutral validator stays floor-agnostic and the floor override is enforced at check time by the verifier, never at validate time

#### Scenario: A scope glob is well-formed and dialect-conformant
- **WHEN** every `scope_globs` entry is a repository-relative glob using only `**`, `*`, `?`, and literal segments, is non-universal, has no leading `/` or `!`, and its repository key is named in `code_surface`
- **THEN** `openspec validate --strict` accepts the declaration

### Requirement: Trust-root integrity of the structured scope declaration
The `scope_globs` declaration SHALL be a trust-root source whose integrity is
bound to the change's ratification, satisfying the four properties the
provenance-gated autonomous-merge doctrine requires of trust-root source (iv):
it SHALL be BASE-READ (a provenance-tie verifier reads `scope_globs` only from
the base branch, never from a pull-request head, so a pull request can never
present its own widened scope to the check that authorizes it);
RATIFICATION-COVERED (the `scope_globs` bytes are part of the ratified change
artifact, covered by the change's ratification, so a governed pull request can
never widen its own scope post-ratification); NON-AUTHOR-MUTABLE (the
`openspec/changes/` surface that carries `scope_globs` SHALL be a never-clearable
floor member of EVERY repository enrolled for provenance-gated autonomous merge,
and no autonomous provenance merge SHALL write to it — closing the
self-authorization recursion in which an earlier governed merge could author the
scope a later tie corroborates against); and FROZEN AFTER RATIFICATION (mutation
of `scope_globs` after ratification is rejected at the archive gate, per the
"Scope retention at archive" requirement). These properties SHALL hold as a
condition of any repository's provenance-gated enablement; a repository that
floors any trust-root source outside its own tree-validated floor SHALL NOT
enable a non-docs provenance-eligible class.

#### Scenario: A pull request widens its own scope on its head
- **WHEN** a realization pull request edits `scope_globs` on its head to admit paths its base-branch scope excludes
- **THEN** the verifier is unaffected, because it reads `scope_globs` only from the base branch, and the pull request's out-of-scope paths still park

#### Scenario: The scope-carrying surface is not floored in an enrolling repository
- **WHEN** a repository would enable a non-docs provenance-eligible class without making the `openspec/changes/` scope surface a never-clearable floor member
- **THEN** the class MUST NOT be enabled, because a trust-root source the autonomous path could write would break the non-author-mutable property

#### Scenario: An autonomous merge would write a scope declaration
- **WHEN** a candidate pull request eligible for autonomous clearance would itself write or modify a `scope_globs` declaration
- **THEN** it parks for human review — no autonomous provenance merge writes a trust-root source

### Requirement: Scope retention at archive
The archive gate SHALL verify that a change's `scope_globs` declaration is
unchanged from the declaration present at ratification, and mutation of
`scope_globs` after ratification SHALL be rejected at the archive gate. This
mirrors the "Origin retention at archive" requirement and realizes the
FROZEN-AFTER-RATIFICATION property of the trust-root integrity requirement: a
ratified scope is auditable and immutable, so a change cannot silently widen the
paths its realization was authorized to touch between ratification and archive.
Whether the archive gate additionally ASSERTS that the realized pull request's
changed paths fell within `scope_globs` (a provenance closure making the declared
scope auditable against what actually shipped) is deferred to a named follow-up
and is NOT required by this requirement.

#### Scenario: Scope is unchanged at archive
- **WHEN** a change with a `scope_globs` declaration reaches its archive gate and the declaration matches the one present at ratification
- **THEN** the scope-retention check passes and archiving proceeds

#### Scenario: Scope was mutated after ratification
- **WHEN** the archive gate finds `scope_globs` differs from the declaration present at ratification
- **THEN** the archive MUST fail
- **AND** restoring or accepting the mutation is a contested-class act requiring an explicit disposition

### Requirement: Floor primacy over declared scope at check time
The never-clearable floor SHALL override the declared scope at CHECK time, and a
`scope_globs` declaration SHALL NEVER authorize a floor path. Because
`openspec validate` runs in the neutral repository and cannot know each enrolled
repository's tree-specific floor, scope validation stays floor-agnostic; a
provenance-tie verifier SHALL instead load the enrolled repository's own
base-branch never-clearable floor and subtract it from the authorized set,
reusing the shipped "the floor subtracts from the allowlist" semantics so that
exactly ONE floor authority per repository governs and scope checks and floor
checks cannot disagree. A change MAY over-declare scope (even naming a floor
path); the verifier SHALL still park any pull request whose diff touches the
floor, regardless of whether `scope_globs` named it. Floor always wins.

#### Scenario: A diff touches a floor path the scope named
- **WHEN** a pull request's changed path lies inside both the tied change's `scope_globs` and the enrolled repository's never-clearable floor
- **THEN** the verifier parks the pull request never-clearable — the floor overrides the declared scope

#### Scenario: A diff stays within scope and outside the floor
- **WHEN** every changed path matches the tied change's `scope_globs` for the repository and none matches the repository's base-branch floor
- **THEN** the scope-containment and floor sub-checks both pass, and provenance-eligibility depends only on the other criteria
