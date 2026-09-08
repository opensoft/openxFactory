# Proposal Ratification: add-consent-custody-rederivation-record

Status: ratified
Kind: report
Decision date: 2026-09-08
Ratifier: Brett Heap (reviewer of record; openxFactory operator authority) — in session
Ratified: 2026-09-08 by Brett Heap (reviewer of record) — in session, first-hand
to lane `opsXfactory-1` (harness session `ee808615-4d8a-475f-bcb3-6f92a89909f0`,
`session_01SdF4BiCNseq3B2HFzkN3SJ`), verbatim *"ratify 774, merge it and land
it"*, on openxFactory pull request
[#774](https://github.com/opensoft/openxFactory/pull/774); this record.

Ratified baseline: this change as committed at **`6cfe9ba6628b21649953c83c5b4fe1ade1eda76c`**,
the tip of `change/add-consent-custody-rederivation-record` and the head #774
carries — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/consent-instrument/spec.md`. The delta is **ONE `## MODIFIED` and ONE
`## ADDED` requirement, 22 scenarios**, no `## REMOVED` and no `## RENAMED`.
`design.md` carries **ELEVEN decisions** — C-1 through C-10 plus C-6a.
`tasks.md` carries **46 boxes, NONE ticked**. The change's row in
`tests/sequenced_after/corpus-ledger.yaml` reads
`{state: active, class: co-modifier, declares: [add-consent-instrument],
depth: 1, prose: false, moved_by: "#774"}`. Validated strict through the pinned
entrypoint (`scripts/validate-openspec-cli-pin.py`,
`@fission-ai/openspec@1.12.0` verified against its content address) at this
baseline.

## Decision

The word has **TWO CLAUSES and they are not the same act**, and this record
splits them rather than reading them as one:

- ***"ratify 774"*** — **THIS IS THE RATIFICATION.** It approves the packet's
  text as committed at `6cfe9ba6`: the requirements, the eleven decisions, and
  the task list as written.
- ***"merge it and land it"*** — **THIS IS AN ORDER TO PROCEED, NOT PART OF THE
  APPROVAL.** It authorizes landing the pull request. It does not tick a task,
  does not move a schema byte, does not cut a bundle and does not reach any
  consumer repository. What landing puts on `main` is a ratified PROPOSAL.

**RATIFICATION HYGIENE — HEARD AND RECORDED BY THE SAME LANE, NOTHING
RELAYED.** The word was given first-hand to lane `opsXfactory-1` in the harness
session named in the header, and this record is written by that same lane from
that same session. No intermediary carried it, and no part of the verbatim is
reconstructed from a summary.

## What was ratified

The **eleven decisions**, each with the substance approved:

- **C-1** — the record is a SIBLING of `custody`, never a member of it; `custody`
  keeps exactly `{locator, sha256}` and `additionalProperties: false` under
  ruling D9.
- **C-2** — the name `custody_rederivations`.
- **C-3** — **TEN required fields per entry**, entry closed: `at`, `commit`,
  `previous_locator`, `observed_locator`, `previous_sha256`, `observed_sha256`,
  `diff_class`, `reason`, `ruling_ref`, `recorded_by`.
- **C-4** — `diff_class` closed at **THREE members** with a currency consequence
  each: `path_only` (zero bytes changed; only the locator did) and `header_only`
  MAY reach CURRENT; `content` WITHHOLDS.
- **C-5** — `reason` closed at `lifecycle_header_edit`, `archive_move`,
  `other_ruled_edit`, every member carrying the authorizing-reference obligation.
- **C-6** — the chain rule: anchored to the pin AND its locator, no gap in
  either half, each link re-derived at `commit^` and `commit`, and **the
  ANCESTRY LEG** — every entry's commit an ancestor of the next and the last an
  ancestor of HEAD, so agreement reached off the history leading to HEAD is
  coincidence and not derivation. A chain that cannot be re-derived is a
  REFUSAL, never an admission.
- **C-6a** — **THE DECLARED CUSTODY STORE MAPPING.** `custody.locator` is
  OPAQUE and is NOT a path; the consuming repository DECLARES a mapping that
  resolves it, an unresolvable locator is a refusal, and a checker that INFERS
  an undefined path is nonconformant. Each entry carries the locator pair, the
  starting locator evaluated at `commit^` and the observed locator at `commit`.
- **C-7** — the validator split, and the OBLIGATION: the neutral validator takes
  only what is derivable from the record's own bytes; the git re-derivation runs
  where the target lives; and a repository whose instruments declare
  `custody_rederivations` SHALL OPERATE such a check.
- **C-8** — additive `contract_schema_version: 2 → 3`; the record envelope's
  `schema_version` stays `const: 1`; every existing instrument validates
  unchanged.
- **C-9** — **THE WITHHELD OUTCOME.** A `content`-class entry SHALL NOT reach
  CURRENT even when every digest leg re-derives; the verdict is WITHHELD — a
  THIRD outcome beside current and refused — pending re-execution, represented
  by the neutral validator as a named outcome of its own and propagated, never
  upgraded, by the consumer gate.
- **C-10** — **THE CARVE-OUT.** A custody re-derivation is NOT an amendment and
  does not transition the instrument's status.

### Task 1.3's operator veto was NOT exercised

`tasks.md` § 1.3 put **C-10's supersession of one clause of the F.1 ruling**
to the operator as its own veto point — the F.1 ruling (OpsxFactory PR #248,
comment
[5571629298](https://github.com/opensoft/OpsxFactory/pull/248#issuecomment-5571629298))
had said the three instruments take *"their `amendments` entries plus the
structured block"*, and C-10 writes the structured block and no amendment. The
veto was **NOT exercised**, so **the default stands**:

- **NO `amendments` entry is written** for a custody re-derivation, and
- **the three OpsxFactory instruments stay `status: executed`.**

Every other decision likewise stands as recommended; no veto was exercised on
any of the eleven.

## What this ratification authorizes

- **The 46 realization tasks, as a LATER and SEPARATELY CLAIMED act.** They are
  not performed by this word and not performed by landing #774. Every box stays
  unticked on `main`.
- **The `contract-v3.5` cut**, when it is taken — with the **row-4 version claim
  on openxFactory issue [#630](https://github.com/opensoft/openxFactory/issues/630)
  made BY THE CUTTING SESSION at cut time and not reserved here**
  (`docs/contract-versioning-policy.md` § *Bundle Realization Order* allocates
  the number late; `contract-v3.4` is the declared bundle at this baseline).
- **The consumer handoff, as OpsxFactory's OWED ACT** and outside this change's
  archive gate: the DECLARED custody store mapping, the `stack.yaml`
  `contract_ref` re-pin **in lockstep with the worker-enrollment-broker's
  runtime-shape validation**, and the **three non-uniform chains** — two-entry
  for `opensoft-exchange-monitor` and `opsx-farheap-service-discovery` (whose
  targets archived at `a98fca5b` and `0ebb1191`, both ancestors of `57fd9fd2`),
  one entry for the never-archived `opsx-opensoft-node-inventory`.

## What this ratification does NOT authorize

- **No schema byte lands by this record.**
  `contracts/schemas/consent-instrument.schema.yaml` is untouched at this
  baseline and stays at `contract_schema_version: 2`.
- **No contract bundle is cut**, no `contracts/manifest.yaml` row moves, no
  digest inventory is written and no annotated tag is owed.
- **No consumer file is edited.** No OpsxFactory instrument takes an entry, no
  pin advances, and no custody-digest gate is built.
- **No instrument is re-executed**, and no `content`-class divergence is
  dispositioned by this word.
- **No task is ticked.** 46 of 46 remain open.

## Ratified requirements text, by heading

`specs/consent-instrument/spec.md`:

- `## MODIFIED Requirements` → **The Signed Original Never Enters A Product
  Repo** — restated in full against promoted canon (0 uncarried units), grown
  with the sibling array, the ten-field closed entry, the three-member class
  enumeration, the never-rewritten pin and the C-10 carve-out.
- `## ADDED Requirements` → **Custody Currency Is Re-Derived From Git History
  Or Refused** — the declared-mapping obligation, the direct and chained
  conditions with the locator pair and the ancestry leg, the per-class currency
  table, the WITHHELD outcome with its representation and propagation duty, and
  the split of obligations between the neutral validator and the consumer's
  check.

## The review this record rests on

Three adversarial rounds preceded the word, each landing on this branch before
the next was run. **No round was clean**, and every finding was a real defect:

| Round | Head | Found |
| --- | --- | --- |
| 1 | `abade506` | The first packet. |
| 2 | `d55bf886` | **1 BLOCKER + 4 MAJOR** — locator resolution undefined, so `reason: archive_move` was unadmittable BY CONSTRUCTION and the worked example contradicted the finding; `diff_class: content` bought currency by omission; the instructed `amendments` entry would have transitioned three EXECUTED instruments; no ancestry leg; C-1's second leg argued backwards. |
| 3 | `c6028b8a` | **3 MAJOR, each a CONSEQUENCE of the round-2 fixes** — the repaired consumer prescription was still uniform when two of three cases need a two-entry chain; a pure path move had no truthful `diff_class` and fell to `content`, which C-9 would have withheld forever; WITHHELD was mandated while represented by nothing — no outcome, no task, no fixture. |
| 4 | `ab27744b` | `code_surface` understated the realization; README union at `bd263dca`; fixture ordering. |

`6cfe9ba6` re-stamped the sweep-ledger row from a provisional `#757` — a guess
at this packet's pull-request number, which #757 then took — to the real `#774`.

**Gates at the ratified baseline:** pinned CLI `--change … --strict` 1 passed /
0 failed and `--all --strict` 98 passed with 0 undispositioned failures (two
pre-existing accepted exceptions); MODIFIED-block currency 0 uncarried;
`validate-sequenced-after` 40 active changes and `--ledger-diff` consistent at
182 rows; `validate-scope-globs` pass; `validate-consent-instruments` 0 errors;
`validate-manifest-digests` 188 digests verify; doc-health finding set
diff-identical to `main` at every severity; `pytest tests/sequenced_after
tests/proposal-support tests/scope_globs` 330 passed.
