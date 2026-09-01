# Tasks: add-sequenced-after-substrate

Dependency-ordered, in groups that map ONE-TO-ONE to Speckit features for the
post-ratification build. **House rule: OpenSpec ratifies, Speckit builds — never
`opsx:apply`.** Group 1 is the authoring done BY this change. **Group 0 is the
ratification gate and is the only task here a human must perform.** Groups 2–5 are
the `code_surface: openxFactory` build, performed LATER via Speckit, one feature
per group. Group 6 is downstream consumption in codexFactory and is NOT this
change's code surface — it is the consumer's realization, tracked here only so the
dependency is explicit. **No push and no merge is performed by this change.**

## Group 0 — RATIFICATION GATE (human; blocks Groups 2–5 absolutely)

**CLOSED 2026-09-01 — RATIFIED AS AUTHORED by Brett Heap (convener).** OQ-1 ruled
FIX INSIDE THIS CHANGE; OQ-2 … OQ-5 confirmed as recommended; S1 … S9 confirmed,
none vetoed. Dispositions recorded in `proposal.md` § Ratification record. Groups
2–5 are authorized.

- [x] 0.1 **Convener read of `design.md` § 0** (the ten-line brief) — what is
  being ratified, the measured blast radius, and the one open question.
- [x] 0.2 **Rule OQ-1 — the strict-loader retrofit.** RULED: the retrofit lands
  INSIDE this change. The strict-loader requirement's reach into `scope_globs:`
  is realized here, repairing the `yaml.safe_load` duplicate-key hole in
  `scripts/scope_globs.py` — ONE loader over the whole realization-axis block for
  BOTH structured fields. Group 2 carries its full scope and Group 4 its full test
  set.
- [x] 0.3 **Confirm or veto OQ-2 … OQ-5.** All four CONFIRMED as recommended:
  multi-parent declarations ALLOWED; doc-health's whole-token reader LEFT IN
  PLACE with its migration a named follow-on; the cycle-refused /
  depth-unbounded split AS AUTHORED (no cap and no operator in the substrate);
  NO `gate_rules_council` co-sign required beyond convener ratification.
- [x] 0.4 **Confirm or veto authoring decisions S1 … S9** (`design.md`
  § Decisions) — all nine confirmed as written, none vetoed.
- [x] 0.5 On ratification: `Status: ratified` + the `Ratified by:` line and the
  `## Ratification record` section recording the five OQ dispositions are in
  `proposal.md`, and the README "OpenSpec Records" entry is moved from AUTHORED to
  RATIFIED.

## Group 1 — openxFactory doctrine authoring (THIS change; no code)

- [x] 1.1 Author `.openspec.yaml` — `kind: ad_hoc`, id
  `openxFactory:adhoc:2026-09-01-add-sequenced-after-substrate`, the derivation
  from ruling R1 and dependency 0.5, the checked reason `kind: staged` is NOT
  taken (`ideation/staging/` enumerated and `INDEX.md` read 2026-09-01; no topic
  carries this subject), the authorization-to-author disclaimer, and the four
  `related:` entries.
- [x] 1.2 Author `proposal.md` with honest `code_surface:` / `target_release:`
  front matter, and DECLARE THIS CHANGE'S OWN
  `sequenced_after: [add-structured-scope-substrate]` as the substrate's first
  instance.
- [x] 1.3 Author the `release-realization` spec delta — **ALL-ADDED**, nine
  requirements, thirty scenarios: machine-readable ordered-delta parent
  declaration; repository-qualified parent-reference syntax; strict loading of the
  realization-axis front-matter block; parent-declaration validation;
  ordered-delta identity survives archival; root status is proved and never
  inferred from absence; trust-root integrity of the parent declaration;
  parent-declaration retention at archive; chain-walk policy belongs to the
  consumer, and its bound SHALL be measured.
- [x] 1.4 Author `design.md` — § 0 convener brief, context, decisions S1 … S9,
  the corpus sweep, the first-instance proof, the sibling-rule measurement, risks,
  and open questions OQ-1 … OQ-5.
- [x] 1.5 **Measure the sibling rule rather than assume it.** Confirmed that
  `govern-sibling-added-modified-deltas` holds an ACTIVE `## MODIFIED Requirements`
  block over `release-realization`'s "Ordered deltas and branch vocabulary" and
  `add-structured-scope-substrate` one over "Realization axis declaration", and
  chose an ALL-ADDED delta so neither `govern-sibling`'s relative-declaration
  obligation nor its archive-order hold is incurred, and no currency marker is
  owed. Recorded in `proposal.md` § The sibling rule, measured.
- [x] 1.6 **Run the corpus sweep as an AUTHORING measurement**, requirement-
  granular and normalized, and record it in both `proposal.md` and `design.md`:
  152 change ids, 104 co-modified, 48 sole modifiers, 19/11 among the 30 active,
  3 prose `Sequenced-after:` headers (all archived), 0 occurrences of
  `sequenced_after:`.
- [x] 1.7 `OPENSPEC_TELEMETRY=0 openspec validate add-sequenced-after-substrate --strict`
  and `--all --strict` pass; the house validators touching the changed surfaces
  run clean.
- [x] 1.8 List the change in the openxFactory README "OpenSpec Records" ACTIVE
  block, marked AUTHORED-NOT-RATIFIED.

## Group 2 — Speckit feature: strict front-matter loader (code_surface: openxFactory)

Maps to a Speckit feature `frontmatter-strict-loader`. Realizes the "Strict
loading of the realization-axis front-matter block" requirement. **Ruled at 0.2:
FULL SCOPE — the retrofit lands here.** This group comes FIRST because every later
group reads the block through it.

> **CONSUMER NOTE — THIS GROUP BREAKS codexFactory'S VENDORED-COPY LOCKSTEP UNTIL
> A COORDINATED RE-VENDOR. READ BEFORE ADVANCING codexFactory's PIN.**
> codexFactory VENDORS this repository's `scripts/scope_globs.py` byte-for-byte as
> `scripts/merge_master/scope_globs.py`, pinned by
> `tests/merge-master/test_vendored_scope_globs.py` — a recorded `sha256` per
> vendored file (`VENDORED_SHA256`) plus a SOURCE-EQUALITY assertion that the
> vendored bytes equal `scripts/scope_globs.py` read at the openxFactory commit
> `stack.yaml`'s `contract_ref` names. Two of its tests are the ones that move:
> `test_the_vendored_file_matches_its_recorded_digest[scope_globs.py]` and
> `test_the_vendored_bytes_equal_the_source_at_the_pinned_contract_version[scope_globs.py]`.
> The second fails the moment codexFactory advances `contract_ref` past this
> change WITHOUT re-vendoring — its by-design "a divergence FAILS rather than
> being reconciled" behaviour, not a defect. **THE RETROFIT ALSO ADDS A SECOND
> VENDORED FILE:** `scripts/scope_globs.py` now imports the sibling
> `scripts/frontmatter_strict.py`, so a re-vendor that copies only
> `scope_globs.py` leaves the vendored copy UNIMPORTABLE. The coordinated
> re-vendor, in ONE codexFactory commit: (1) copy openxFactory
> `scripts/frontmatter_strict.py` to `scripts/merge_master/frontmatter_strict.py`
> and re-copy `scripts/scope_globs.py`; (2) add the new file to `VENDORED_SHA256`
> and `VENDORED_SOURCE_PATHS` and refresh the `scope_globs.py` digest; (3) advance
> `stack.yaml`'s `contract_ref` to the openxFactory commit carrying this change —
> all three in that one commit, the discipline that file already states. Consider
> also a differential fixture pinning the vendored loader's refused set against
> `merge_master/change_digest.py`'s own `StrictLoader`, on the same "exactly one
> authority while two engines ship" grounds as the existing glob-parity fixture.
> **NOTHING IN codexFactory IS TOUCHED BY THIS CHANGE** — the re-vendor is the
> consumer's act, tracked in Group 6, and its `change_digest.py` loader is
> UNCHANGED (this loader mirrors it, not the reverse).

- [x] 2.1 Implement ONE strict loader for the realization-axis front-matter block
  that REFUSES rather than resolves: duplicate keys at ANY level, YAML anchors
  (`&`), aliases (`*`), merge keys (`<<:`), non-UTF-8 bytes, and a document over a
  declared size ceiling. Name the ceiling as an operative number rather than
  gesturing at one.
- [x] 2.2 Refuse duplicate keys by CONSTRUCTION, not by post-hoc scan: a
  `yaml.SafeLoader` subclass overriding `construct_mapping` to raise on a repeated
  key, so nesting depth cannot smuggle one past a top-level check.
- [x] 2.3 **The `scope_globs` retrofit (RULED IN AT 0.2).** Route
  `scripts/scope_globs.py`'s `read_front_matter` through the strict loader,
  replacing the `yaml.safe_load` call whose last-duplicate-key-wins behaviour lets
  two `scope_globs:` blocks show a reviewer the FIRST and authorize the LAST.
  Assert the shipped `scope_globs` corpus still validates byte-identically after
  the swap — the retrofit changes how the field is LOADED, never what it MEANS.
- [x] 2.4 Negative fixtures, one per refused form: duplicate key at top level;
  duplicate key NESTED; anchor; alias; merge key (`<<:`); non-UTF-8 byte;
  over-ceiling document. Plus a POSITIVE fixture asserting an ordinary well-formed
  block loads unchanged.
- [x] 2.5 **Parity note as a build obligation.** Record in the module docstring
  that the refused set MIRRORS the consuming verifier's strict loader (the
  consumer's task 2.10), so validator and verifier cannot disagree about the same
  bytes, and that a change to either set must be made in lockstep.

## Group 3 — Speckit feature: sequenced_after schema + parser (code_surface: openxFactory)

Maps to a Speckit feature `sequenced-after-schema`. Realizes the "Machine-readable
ordered-delta parent declaration" and "Repository-qualified parent-reference
syntax" requirements. Depends on Group 2.

- [x] 3.1 Add the schema / data model: a sequence — possibly empty — of non-empty
  strings, no nulls, no nested collections, no duplicate entries. Keep the
  dependency-free posture of `scripts/scope_globs.py` (no `jsonschema`).
- [x] 3.2 A parser reading `sequenced_after:` from a change's `proposal.md`
  front matter THROUGH the Group 2 loader, alongside `code_surface:` /
  `target_release:` / `scope_globs:`. Absence returns a distinct sentinel from
  `[]` — the two mean different things and a parser that conflates them destroys
  the whole root-proof doctrine.
- [x] 3.3 Implement the reference grammar: bare `<change-id>` matching
  `[a-z0-9][a-z0-9-]*` with NO `/`; qualified `<repository>:<change-id>` with
  `<repository>` matching `[A-Za-z0-9_.-]+` (the same token grammar
  `scripts/doc_health/proposal_origin.py`'s origin-id regexes use); a
  self-qualified entry NORMALIZED to the bare form.
- [x] 3.4 Unit fixtures: absent field; `[]`; one bare entry; one self-qualified
  entry; one foreign-qualified entry (WELL-FORMED, disposition left to a
  consumer); two entries (VALIDATES — see 4.4); non-sequence value; null member;
  empty-string member; nested list member; duplicate member; entry with `/`;
  entry with an uppercase or underscore change-id character; entry with an empty
  repository half.

## Group 4 — Speckit feature: resolution, cycle and grammar validator (code_surface: openxFactory)

Maps to a Speckit feature `sequenced-after-validate`. Realizes the
"Parent-declaration validation" and "Ordered-delta identity survives archival"
requirements. Depends on Group 3.

- [x] 4.1 Implement two-location ANCHORED resolution: `openspec/changes/<change-id>/`
  and `openspec/changes/archive/<YYYY>-<MM>-<DD>-<change-id>/` with the date
  exactly `\d{4}-\d{2}-\d{2}` and the remainder EXACTLY the change id — never a
  prefix strip, never a split on the first hyphen. The union must hold EXACTLY
  ONE directory: zero ⇒ unresolvable, two or more ⇒ ambiguous, neither resolved
  by preference.
- [x] 4.2 A BARE entry that resolves to no change in the declaring repository's
  own corpus FAILS validation. A FOREIGN-qualified entry is checked for
  well-formedness ONLY — the neutral validator cannot read another repository's
  corpus and must not pretend to.
- [x] 4.3 Refuse a CYCLE reachable within the declaring repository's own corpus,
  naming the repeated id. A cycle is a WELL-FORMEDNESS defect (no policy can
  resolve it to a root), which is why it is refused here while depth is not.
- [x] 4.4 **Impose NO depth limit and NO fan-out limit.** Positive tests assert
  that a two-parent declaration VALIDATES and that a chain deeper than any gate's
  ceiling VALIDATES. A fork must be DECLARABLE for a consumer's fork refusal to be
  reachable and testable; a neutral depth number would drift from the gate that
  enforces it.
- [x] 4.5 Wire the checks into the house validate runner as
  `scripts/validate-sequenced-after.py` — the same enforcement route
  `scripts/validate-scope-globs.py` and the other `scripts/validate-*.py`
  validators take, because `openspec validate` is the EXTERNAL OpenSpec CLI and
  cannot be extended in-tree. Fail with a message naming the offending change,
  the offending entry, and the rule it breaks.
- [x] 4.6 A pytest gate running the validator over the LIVE corpus on every pull
  request, mirroring `test_corpus_scope_globs_all_validate`, so a malformed or
  dangling declaration anywhere reds the required suite check.
- [x] 4.7 Archive-resolution fixtures: a parent that has ARCHIVED still resolves;
  an id matching BOTH an active and an archived directory is ambiguous; two
  archive dates for one id are ambiguous; an archived directory whose post-date
  remainder merely STARTS WITH the id does NOT resolve; a nested
  `openspec/changes/<id>/openspec/changes/<id2>/` does NOT resolve.

## Group 5 — Speckit feature: integrity, archive retention, corpus sweep and docs (code_surface: openxFactory)

Maps to a Speckit feature `sequenced-after-integrity`. Realizes "Trust-root
integrity of the parent declaration", "Parent-declaration retention at archive",
and "Chain-walk policy belongs to the consumer, and its bound SHALL be measured".
Depends on Group 3.

- [x] 5.1 Add the retention (freeze) gate mirroring the shipped
  `scope_globs.scope_retention_at_archive` and the "Origin retention at archive"
  implementation: reject any mutation of `sequenced_after:` between ratification
  and archive by comparing the ratified git snapshot against the working tree. A
  mutated declaration is a CONTESTED-class failure requiring an explicit
  disposition.
- [x] 5.2 Assert the archive gate DOES NOT REWRITE declarations on archival — no
  date-prefixing, no re-pointing, no normalization of entries. A fixture archives
  a change carrying a declaration and asserts the entries are byte-unchanged.
- [x] 5.3 Author `docs/sequenced-after-trust-root-floor.md`, modelled on
  `docs/scope-globs-trust-root-floor.md`: the four trust-root properties, what
  openxFactory can assert about its own substrate (the 5.1 freeze gate and the
  policy-free validator) versus what only an enrolled repository's envelope and
  verifier can enforce, and the explicit statement that no autonomous merge writes
  the declaration surface. Link it into the README doc index.
- [x] 5.4 **CORPUS SWEEP as a shipped, re-runnable report**, not a one-off
  measurement. A mode of the validator (or a sibling script) that reports, over
  active + archive: the change-id population; the count that are co-modified at
  requirement granularity (candidates that would each owe a declaration); the
  count that are sole modifiers; how many DECLARE the field; and **the DEEPEST
  DECLARED CHAIN it resolves**. Re-running it is what makes the "measured, not
  assumed" obligation discharge over time instead of aging into a stale sentence.
- [x] 5.5 Record the sweep's FIRST post-adoption reading in the docs, replacing
  the authoring-time "0 declarations, deepest chain 0 hops BY CONSTRUCTION" with a
  real measurement, and state plainly that a zero reading is ZERO EVIDENCE about
  any gate's ceiling rather than evidence the ceiling is sufficient.
- [x] 5.6 Document that the depth ceiling, the fan-out disposition and the
  composition operator are the CONSUMING GATE's and are declared in the gate's own
  specification — with the consumer's current values (FOUR hops inclusive of the
  terminal change; INTERSECTION) cited as the first instance rather than adopted
  as neutral doctrine.

## Group 6 — codexFactory consumption (NOT this change's code surface)

Tracked for dependency clarity only; built under
`realize-provenance-gated-autonomous-merge`'s realization against a CURRENT
codexFactory checkout, archived on merged + green per `release-realization`.
Numbers are that packet's own task ids.

- [ ] 6.1 (their 2.7a) Read hops ONLY from `sequenced_after:`, base-read and
  covered by each hop's signed-ratification `change_digest`; refuse a qualified
  FOREIGN entry under `cross_repository_hop` rather than skipping it.
- [ ] 6.2 (their 2.11) The CO-MODIFIER CROSS-CHECK for root status —
  requirement-granular, NFC-normalized, promotion-anchored — keeping `[]` from
  buying authority that omission would not.
- [ ] 6.3 (their 2.12) Hop resolution across the ACTIVE and ARCHIVED corpora by
  the anchored patterns, exactly-one, with `hop_unresolvable` / `hop_ambiguous`.
- [ ] 6.4 (their 2.7c/2.7d) INTERSECTION composition and the FOUR-hop ceiling,
  with `chain_cycle` and `chain_depth_exceeded` as named refusals.
- [ ] 6.5 (their 2.10) The strict front-matter loader on the provenance path,
  whose refused set this substrate's Group 2 mirrors.
- [ ] 6.6 (their 2.19/design D19) Make the `openspec/changes/` declaration surface
  a never-clearable floor member of the enrolled repository's envelope.
- [ ] 6.7 Negative fixtures: a pull request that re-parents itself on HEAD does not
  move the base-read chain; an undeclared parent with a co-modifier refuses; a
  fork refuses; a cycle refuses; an archived-root chain still resolves.
- [ ] 6.8 **THE COORDINATED RE-VENDOR** the Group 2 consumer note specifies —
  vendor `scripts/frontmatter_strict.py` alongside a re-copied
  `scripts/scope_globs.py` into `scripts/merge_master/`, extend
  `VENDORED_SHA256` + `VENDORED_SOURCE_PATHS` in
  `tests/merge-master/test_vendored_scope_globs.py`, and advance `stack.yaml`'s
  `contract_ref`, ALL IN ONE COMMIT. Until it lands, advancing `contract_ref`
  past this change alone reds
  `test_the_vendored_bytes_equal_the_source_at_the_pinned_contract_version[scope_globs.py]`
  BY DESIGN — that assertion exists so a divergence fails rather than being
  reconciled at call sites. **This change touches nothing in codexFactory.**
