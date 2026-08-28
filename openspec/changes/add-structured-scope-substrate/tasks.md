# Tasks: add-structured-scope-substrate

Dependency-ordered, in groups that map to Speckit features for the
post-ratification build (house rule: OpenSpec ratifies, Speckit builds — never
`opsx:apply`). Group 1 is the authoring done by THIS change. Groups 2–4 are the
`code_surface: openxFactory` build (the `openspec validate` extension) performed
LATER via Speckit, one feature per group. Group 5 is downstream consumption in
codexFactory and is NOT this change's code surface — it is B's realization,
tracked here only so the dependency is explicit. No push/merge is performed by
this change.

## Group 1 — openxFactory doctrine authoring (THIS change; no code)

- [x] 1.1 Author `.openspec.yaml` (staged origin, topic
  `openxFactory:staging:structured-scope-substrate`).
- [x] 1.2 Author `proposal.md` (the sibling-field resolution, absence=fail-closed,
  validation summary, trust-root integrity, floor-override-at-check-time,
  backward-compat) with honest `code_surface` / `target_release` front-matter.
- [x] 1.3 Author the `release-realization` spec delta: MODIFY "Realization axis
  declaration" to add the optional `scope_globs:` sibling; ADD "Structured
  path-scope declaration", "Structured path-scope validation", "Trust-root
  integrity of the structured scope declaration", "Scope retention at archive",
  and "Floor primacy over declared scope at check time".
- [x] 1.4 Author `design.md` (decisions D1–D6, risks, open questions carried for
  ratification).
- [x] 1.5 `OPENSPEC_TELEMETRY=0 openspec validate add-structured-scope-substrate --strict` and `--all --strict` pass.
- [ ] 1.6 Convener ratification read (resolve Open Questions 1–6; confirm whether
  `gate_rules_council` co-sign is required). Human-gated.
- [ ] 1.7 On ratification: set `Status: ratified` + `Ratified by:`; list in the
  openxFactory README "OpenSpec Records" block.

## Group 2 — Speckit feature: scope_globs schema + parser (code_surface: openxFactory)

Maps to a Speckit feature `scope-globs-schema`. Realizes the "Structured
path-scope declaration" requirement's value form.

- [x] 2.1 Add a lightweight schema / data model for the `scope_globs` front-matter
  field: mapping of string repo-key → non-empty, unique list of non-empty
  strings. No jsonschema dependency required to stay in step with the
  dependency-free posture of the envelope core. (`scripts/scope_globs.py`:
  `validate_shape` / `ScopeGlobs`.)
- [x] 2.2 A front-matter parser that reads `scope_globs` from a change's
  `proposal.md` YAML block alongside `code_surface` / `target_release`
  (`scripts/scope_globs.py`: `read_front_matter` / `read_scope_globs` — the one
  place the realization-axis block is parsed for a structured, non-flat field;
  the ideation-dashboard `_release_frontmatter` reader handles only the flat
  `code_surface` / `target_release` headers).
- [x] 2.3 Unit fixtures: absent field (valid, not-eligible), empty map, empty
  list, non-string keys/values, duplicate entries.
  (`tests/scope_globs/test_schema.py`.)

## Group 3 — Speckit feature: dialect-conformant validator hook (code_surface: openxFactory)

Maps to a Speckit feature `scope-globs-validate`. Realizes the "Structured
path-scope validation" requirement. Depends on Group 2.

- [ ] 3.1 Implement the dialect-conformance checks mirroring codexFactory
  `envelope.py:_validate_path_allowlist` EXACTLY: reject leading `/`, leading `!`,
  the universal patterns (`**`, `*`, `**/*`, `/**`, `./**`), and complement/denylist
  keys; require each glob compiles under the envelope dialect (`**`/`*`/`?`,
  anchored full-match).
- [ ] 3.2 Implement the `code_surface` cross-consistency check (every `scope_globs`
  key must be named in `code_surface`; reverse not required).
- [ ] 3.3 Keep the validator FLOOR-AGNOSTIC: no floor knowledge, no rejection of
  floor-named paths (a positive test asserts a floor-named glob passes validate).
- [ ] 3.4 Wire the checks into `openspec validate --strict` so a malformed or
  non-dialect `scope_globs` fails strict validation with a message naming the
  offending entry and the rule it breaks.
- [ ] 3.5 Lockstep test pinning the validator's accept/reject set to the same
  fixtures as `envelope.py:_validate_path_allowlist`, so the two dialects cannot
  drift.

## Group 4 — Speckit feature: trust-root + archive integrity (code_surface: openxFactory)

Maps to a Speckit feature `scope-globs-integrity`. Realizes "Trust-root integrity
of the structured scope declaration" and "Scope retention at archive". Depends on
Group 2.

- [ ] 4.1 Add the scope-retention archive-gate check mirroring the existing
  "Origin retention at archive" implementation: reject any mutation of
  `scope_globs` between ratification and archive; a mutated scope is a
  contested-class failure requiring an explicit disposition.
- [ ] 4.2 Document (as neutral doctrine + a check where openxFactory can assert it)
  that the `openspec/changes/` scope-carrying surface must be a never-clearable
  floor member in every enrolled repository, and that no autonomous provenance
  merge writes it — the enforcement lives in each repo's envelope + verifier
  (Group 5), so this task records the requirement and any openxFactory-side
  assertion available.

## Group 5 — codexFactory consumption (NOT this change; B's realization)

Tracked for dependency clarity only; built under `add-provenance-gated-autonomous-merge`'s
realization against a CURRENT codexFactory checkout, archived on merged+green per
`release-realization`.

- [ ] 5.1 The provenance-tie verifier's step (iii): read `C.scope_globs[R]` from
  base; absent/empty ⇒ park not-eligible; every changed path must
  `path_matches` a scope glob; else park out-of-scope. Uses the SAME
  `envelope.path_matches` engine as the floor.
- [ ] 5.2 The floor override (verifier step 4): load `R`'s base-branch
  `gate_integrity.never_clearable_paths`; any changed path matching the floor
  parks never-clearable regardless of scope. Floor wins.
- [ ] 5.3 Make the `openspec/changes/` scope surface (and the other B trust-root
  sources) never-clearable floor members of the enrolled repository's envelope.
- [ ] 5.4 Negative fixtures: a PR that widens `scope_globs` on head does not move
  the base-read scope; an out-of-scope path parks; a floor-named in-scope path
  parks never-clearable.
