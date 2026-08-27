# Phase 0 Research: openxwallet deprecation minor (P2.5)

All findings are from the repository at base commit `42662b70` (`origin/main`,
2026-08-27). Nothing here was inferred from memory.

---

## R1 — Is there a manifest schema or validator that would reject `relocating:`?

**Decision**: No schema extension is needed. `relocating:` can be added as-is.

**Evidence**:
- No JSON Schema for `contracts/manifest.yaml` exists. A sweep of every `.yaml`
  in the tree for `contract_bundle_version` returns only `contracts/manifest.yaml`
  itself and two unrelated avatar-client files. Nothing under
  `contracts/schemas/` matches `manifest`.
- `scripts/validate-manifest-digests.py` (68 lines) has no `additionalProperties`,
  no allowed-key list, and no unknown-key handling. It walks nested mappings via
  `iter_entries()` and yields a node only when **both** `sha256` and `path` are
  present. A `relocating:` mapping with sub-keys `to` / `tag` / `since` has
  neither, so it is invisible to that walker — this is the one real collision risk
  and it is absent by construction.
- `scripts/hermes_runtime_validation/release.py` loads the manifest with
  `yaml.safe_load` and reads only `contract_bundle_version` plus the artifact
  entries; unknown row keys are ignored.
- `scripts/doc_health/release_inventory.py` parses the manifest with a regex over
  `^contract_bundle_version:\s*(\S+)$` only.

**Alternatives considered**: extending a manifest schema (there is none to
extend); adding a validator for the marker's shape (rejected — D5 chose the
manifest as the carrier precisely to avoid new machinery, and the checker in
change 2 is the thing that reads it, so a malformed marker surfaces there).

**Consequence for the plan**: the "extend schema + validator" contingency named in
the feature brief is **not triggered**. Recorded rather than silently skipped.

---

## R2 — The eight rows, exactly

**Decision**: eight rows at `contracts/manifest.yaml`, at these `- id:` lines.

| # | line | id | path root |
|---|------|----|-----------|
| 1 | 1999 | `openxwallet-record` | `contracts/openxwallet/` |
| 2 | 2017 | `openxwallet-custody-registry-schema` | `contracts/openxwallet/` |
| 3 | 2030 | `openxwallet-custody-registry` | `contracts/openxwallet/` |
| 4 | 2043 | `openxwallet-grant` | `contracts/openxwallet/` |
| 5 | 2056 | `openxwallet-grant-exercise` | `contracts/openxwallet/` |
| 6 | 2069 | `openxwallet-distinct-holder-constraint` | `contracts/openxwallet/` |
| 7 | 2082 | `openxwallet-subject-attestation` | `contracts/openxwallet/` |
| 8 | 2095 | `openxwallet-agent-composition` | `contracts/openxwallet-agent-profile/` |

The block is introduced by the comment at line 1992 ("openxWallet core + agent
profile — contract-v1.31 registration") and ends at line 2107, immediately before
the `client-identity-roster` comment block at 2108. The design's cited span
`:1967-2082` names where the block sat when D5 was written; the tree today puts it
at 1992–2107. The **eight ids** are the stable identifier and are what this
feature keys on — line numbers are recorded for review convenience only.

---

## R3 — How a bundle cut is actually done in this repository

**Decision**: mirror commit `2cd5fce5` (`contract-v1.45`), found with
`git log --oneline -S "contract-v1.45" -- contracts/`.

Its `--stat`:

```
contracts/CHANGELOG.md                              136 +++
contracts/manifest.yaml                              35 +-
contracts/releases/contract-v1.45.digests.yaml     1056 ++++
contracts/schemas/gate-action-record.schema.yaml     150 ++-
contracts/schemas/xfactory-workbench-chat-turn...     55 +
```

**What the precedent does NOT touch**: `README.md`, `contracts/README.md`, any
workflow, and it creates no tag. The feature brief's "README rows if the precedent
touched them" is therefore answered: **it did not**, so this feature does not
either.

**The generator**:
`python3 scripts/validate-contract-release.py build --tag <tag> --output contracts/releases/<tag>.digests.yaml`
→ `release.build_release_inventory(repo_root, bundle_tag=tag)`, serialized by
`release.dump_inventory` (`yaml.safe_dump(..., sort_keys=False, allow_unicode=False)`).
Verified working at base: emitted 192 entries, `release build: pass`. The
inventory excludes itself and sorts entries bytewise by path.

**Alternatives considered**: hand-authoring the inventory — explicitly forbidden;
`release_inventory.py`'s own family text says a hand-edited inventory is
"already forbidden", and the drift family's action string says "never hand-edit an
inventory or `contract_bundle_version` to make this comparison pass".

---

## R4 — Who cuts the tag

**Decision**: not this feature. The operator cuts it at merge.

**Evidence**: `git for-each-ref refs/tags/contract-v1.44 refs/tags/contract-v1.45`
shows both are **annotated tag objects** tagged by `brettheap` on 2026-08-26. A
grep of `.github/workflows/` for `git tag` / `refs/tags` returns **no workflow**
that creates a tag. `tasks.md` 5.8 marks the allocation-and-tag step `[OPERATOR]`
for exactly this reason.

**Consequence**: task 5.8 is left unticked with a note, and the pull-request body
states the tag is cut by the merger on the realized commit.

---

## R5 — Bundle numbering

**Decision**: author as `contract-v1.46`; state in the PR body that it is
re-verified at merge.

**Evidence**: `contracts/manifest.yaml:3` declares `contract-v1.45` at base; tags
run contiguously to `contract-v1.45`. `docs/contract-versioning-policy.md:30-31`:
"A proposed change MUST NOT reserve a minor number before merge order is known,
and a bundle is not published until its tag exists."

**How the number is honoured rather than reserved**: four places carry it — the
manifest's `contract_bundle_version`, the eight rows' `since:`, the changelog
heading, and the inventory filename — and the PR body names all four as the
renumber surface. If another bundle lands first, those four move together.

---

## R6 — The deprecating-minor obligations, and the precedent that discharges them

**Decision**: the changelog section states the removal version and migration path;
`docs/contract-versioning-policy.md`'s "Deprecations Currently In Force" list
gains an entry.

**Evidence**:
- `docs/contract-versioning-policy.md:246-248` (the deprecating-minor class):
  "a field or shape is marked deprecated; the conformance validator emits warnings
  but still accepts it. Deprecations must state the removal version and a
  migration path in the CHANGELOG."
- `:250-252` (breaking): a removed shape requires "at least one full minor release
  where the old shape produced deprecation warnings" — the precondition this
  feature exists to satisfy.
- **The `contract-v1.34` precedent** (`contracts/CHANGELOG.md:1470`+): a cut
  classed "ADDITIVE (minor) plus a DEPRECATION (minor)" that (a) declared the
  class explicitly, (b) named the removal target as `contract-v2.0`, (c) gave a
  concrete migration path, and (d) **also updated
  `docs/contract-versioning-policy.md`'s "Deprecations Currently In Force" list**,
  noting "one normative document moves with it … Both are release-surface members
  and both are digested in this cut's inventory."
- All three existing entries in that list (`:274`+) end with "removal target
  contract-v2.0".

**Consequence**: the policy-doc list entry is in scope. It was not named in
`tasks.md` §5, but the `contract-v1.34` precedent makes it the house shape for a
deprecation, and omitting it would leave the list wrong about what is in force.
Recorded here as a deliberate addition rather than scope creep.

---

## R7 — The emitter: what `check-openxfactory-pin.py` looks like today

**Decision**: add three pure/impure helpers and two lines to `main()`. Do not
modify `classify()`.

**Evidence** (124 lines total):
- `:35` — `PASS, WARN, ERROR, SKIP = "PASS", "WARN", "ERROR", "SKIP"`. The only
  candidate with a warning tier, exactly as D5 says.
- `:38-52` — `classify(pin, pointer, is_ancestor) -> tuple[str, str]`, documented
  "Pure decision".
- `:123` — `return 1 if verdict == ERROR else 0`. WARN already exits 0, so
  FR-008 needs no change to preserve.
- The script does **not read the manifest at all** today. It compares a
  `stack.yaml` `xfactory.contract_ref` commit against
  `git ls-tree HEAD openxFactory` in the aggregation root, using
  `merge-base --is-ancestor` inside `aggregation_root / "openxFactory"`.
- Existing tests: `tests/conformance-gate/test_conformance_checks.py`, section
  `# --- pin ---`, five tests at `:196-225` — equal→PASS, stale→WARN with the
  refresh instruction, divergent→ERROR, skip outside aggregation, and one
  monkeypatched test that pins the absolute-path argv git receives. The module is
  loaded by `load("check-openxfactory-pin")` at `:51` via `importlib` from
  `scripts/`.

**Alternative rejected (and required to be recorded, FR-011)**:
`scripts/validate-domain-openxfactory-pins.py` — no `warn` token in its 138
lines, so emitting there would make a relocation notice an ERROR and red every
domain that pins this minor. That is the precise failure the manifest-carried
marker was chosen to avoid. This is `tasks.md` 5.5 and is recorded in the script's
own docstring by this feature so the reason survives without the tasks file.

---

## R8 — Doc-health baseline at the base commit (so "no NEW findings" is measurable)

**Decision**: record the baseline before editing. `--family release-inventory-drift`
at base commit `42662b70` returns:

| severity | path | note |
|---|---|---|
| **error** | `scripts/validate-hermes-runtime-contracts.py` | bytes differ from what `contract-v1.45`'s inventory records |
| info | `contracts/CHANGELOG.md` | editorial member — expected between cuts |
| info | `contracts/manifest.yaml` | editorial member — expected between cuts |

Process exit was 0 (the family's findings do not fail the default gate), but the
first row is **error-class and pre-existing** — it is not introduced by this
feature.

`scripts/doc_health/release_inventory.py`'s `EDITORIAL` frozenset is
`{contracts/CHANGELOG.md, contracts/manifest.yaml, contracts/README.md}`;
`scripts/validate-hermes-runtime-contracts.py` is not a member, which is why it is
an error rather than an info.

**Consequence, and it is a happy one**: the finding's own prescribed action is
"cut a release through the bundle realization order". Generating
`contract-v1.46.digests.yaml` over the current tree records that file's real bytes
and **discharges the pre-existing error**, along with the two infos. So the
expected post-change state of this family is *no findings at all*. The PR body
states this so a reviewer does not read the disappearance as something hidden.

---

## R9 — Which files the inventory covers (why generation must come last)

**Decision**: generate the inventory as the final edit.

**Evidence**: the `contract-v1.45` inventory includes `contracts/CHANGELOG.md`
(entry 1), `contracts/manifest.yaml` (line 827) and
`docs/contract-versioning-policy.md` (line 917) — all three are files this feature
edits, and all three are release-surface members whose digests are recorded. The
generator reads working-tree bytes (`_WorkingTreeSource`) and excludes only the
inventory file itself.

---

## R10 — The successor tag, and why the design's literal is stale

**Decision**: `wallet-v1.1`. Fully argued in
[`clarify-questions.md`](./clarify-questions.md) § D-1 and recorded in
`spec.md`'s Clarifications section; summarized here for completeness:
`tasks.md`'s preamble says openxFactory's P3 pin records `wallet-v1.1`;
`proposal.md`'s `code_surface` calls it "the tag openxFactory actually pins"; the
tag exists on `opensoft/openXwallet` (`63f5a1ad`) as of 2026-08-26; and D5's
`wallet-v1.0` literal predates P2b. A relocation notice must name the migration
target. Every other element of D5's shape is taken verbatim.

---

## R11 — The release inventory's surface is CATALOG-driven, not manifest-driven (discovered during implementation)

**Finding**: `contracts/releases/*.digests.yaml` does **not** enumerate the
artifacts registered in `contracts/manifest.yaml`. Its membership comes from
`contracts/hermes-runtime/contract-index.yaml` (`release.CATALOG_PATH`), filtered
to entries with `release_member: true` and path-normalized against
`FAMILY_PREFIX = "contracts/hermes-runtime/"`, plus the cross-family members that
catalog names with `..` segments.

**Consequence**: the eight openxwallet artifacts are **not inventory members and
never have been**. `grep -ci openxwallet contracts/releases/contract-v1.45.digests.yaml`
returns `0`. The 192 members break down as:

| prefix | count |
|---|---|
| `contracts/hermes-runtime/` | 148 |
| `contracts/worker-enrollment/` | 7 |
| `contracts/schemas/` | 5 |
| `contracts/CHANGELOG.md`, `contracts/README.md`, `contracts/manifest.yaml`, `contracts/releases/…` | 4 |
| `scripts/` | 22 |
| `docs/` | 3 (including `contract-versioning-policy.md`) |
| `requirements*` | 2 |
| `tests/hermes_runtime_contracts/postgres/images.lock.yaml` | 1 |

**Why this matters, and how it is resolved rather than ignored**: design **D6**
says P2.5's inventory must be "over a release surface that STILL CONTAINS the
eight artifacts", and `tasks.md` 5.7 says "a minor that skips it is a
non-conformant release under `release-surface-integrity`". Read as *file
membership*, the first clause is unsatisfiable by this tooling and always has
been. Read as what the tooling actually models, both clauses are satisfied:

1. **5.7's real obligation is discharged exactly.** The minor HAS its own
   inventory, `contracts/releases/contract-v1.46.digests.yaml`, 192 members,
   tool-generated and byte-reproducible. That is what
   `release-surface-integrity` and the drift family check.
2. **D6's containment holds TRANSITIVELY, and checkably.**
   `contracts/manifest.yaml` IS a digested inventory member. It still carries all
   eight openxwallet rows. The inventory records digest
   `sha256:0750cbdce8a0e0f3625ca8f0484389567107e38a7b697d7e3deae241a4416e6f` — the
   digest of an eight-row manifest. At P3, when the rows are deleted, the same
   member's digest will record a manifest that has none. So the inventory does
   distinguish the two surfaces, through the manifest rather than through eight
   separate entries.

**FR-017 was corrected in `spec.md`** to state the checkable form, rather than
leaving a requirement that reads as satisfiable-by-inspection but is not. This is
recorded as a finding rather than quietly reworded because it is a real gap
between D6's prose and the tooling's model, and P3's author will hit the same
sentence.

**Not changed by this feature**: making the eight artifacts real inventory members
would mean adding them to the hermes-runtime contract index, which is a different
family's catalog and squarely out of P2.5's scope — and it would be pointless
work three weeks before P3 deletes the rows anyway.
