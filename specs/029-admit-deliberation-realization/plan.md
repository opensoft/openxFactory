# Implementation Plan: `deliberation` — register entry two and its neutral return schema

**Branch**: `029-admit-deliberation-realization` | **Date**: 2026-09-04 | **Spec**: [spec.md](./spec.md)

**Lane**: `hermes-wallet-exercise`

## Summary

Realize, as neutral openxFactory bytes, the ONE requirement the ratified change
`admit-deliberation-clearing-operation` added to `clearing-dispatch-boundary`:
`deliberation` becomes register entry number two; a NEW neutral
`contracts/clearing/deliberation-return.schema.yaml` of the ratified kind
`xfactory_clearing_deliberation_return` becomes its declared output schema and is
ROUTED so the shape check and the verdict scan reach it; the dispatch record's
CLOSED refusal enumeration gains exactly the three grounds this entry makes
emittable; the two `deliberation`-named negative fixtures re-point to `coding` so
the closure refusal keeps a live probe; and the contract-tree bookkeeping —
manifest rows and digests, READMEs, changelog, the additive minor — moves with
the bytes.

**The approach is derivative by construction.** Every value is fixed in the
ratified text or grounded in codexFactory PR #165; the few points the ratified
text leaves silent are listed in [research.md](./research.md) under OPEN POINTS
with the most conservative reading taken and flagged for the ratifier.

## Technical Context

**Language/Version**: Python 3.12 (validator and tests); YAML 1.2 (contracts).

**Primary Dependencies**: `PyYAML`, `jsonschema` (draft 2020-12),
`rfc3339-validator`. **No new dependency.**

**Testing**: pytest — `python3 -m pytest tests/ -q -m "not postgres"`, plus
`python3 scripts/validate-clearing-dispatch.py .` and
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.

**Project Type**: an extension to an existing contract family. Not an
application.

**Constraints**:
- **NO SPEC DELTA.** This is realization; it authors no requirement.
- **NO NEW FINDING CODE.** `REFUSAL_CODES` stays closed at 26.
- **NO FOURTH REFUSAL GROUND.** Exactly the three the ratified text names.
- **NO SECOND VOCABULARY.** No digest construction, no handling vocabulary, no
  job envelope, no scope spelling is minted; each is referenced.
- **FIVE FROZEN COPIES MOVE TOGETHER OR THE CHANGE IS RED**, and each is proven
  to fail alone.

## Constitution / house-rule check

| rule | how this feature meets it |
|---|---|
| Domain-neutral contracts live in openxFactory | the return schema is authored HERE, which is design D4's whole ruling |
| Every YAML carries `schema_version` + `kind` | the new schema does, in the family's form |
| Run the local validator before pushing | `validate-clearing-dispatch.py` plus the full pytest suite plus openspec strict |
| A version number is allocated at realization by merge order | `contract-v3.4`, measured against `git tag -l` and the base manifest; **the tag itself is the owner's act at the landed sha** |
| Lane on every artifact | `Lane: hermes-wallet-exercise` on the PR body, every PR comment, and every commit trailer |
| Never `git add -A` | explicit pathspecs on every commit in the shared checkout |

## Ordering, and why it is this order

1. **The Speckit packet** — so the pull request can open as a draft with its
   authority stated before any contract byte moves.
2. **The five frozen copies, in one commit** — the register instance, the
   validator's `RATIFIED_OPERATIONS`, the test's independent `RATIFIED`, the CI
   gate's literal, and the test that pins that literal from a second file.
   Together with the two fixture re-points, because admitting the member and
   leaving the fixtures would turn them green for the wrong reason in the same
   instant.
3. **The new schema, its routing, and the verdict scan** — the schema is what the
   entry's `output_schema_ref` already points at, so it lands immediately after.
   The shared verdict check is EXTRACTED rather than copied.
4. **The three refusal grounds** — independent of 3, ordered after it only so the
   diff reads in the order the requirement does.
5. **Bookkeeping** — manifest rows, digests, counts, READMEs, changelog, the
   additive minor, the release inventory, and the two shipped assertions that
   pin the old bundle number.
6. **The proof that each frozen copy fails alone**, run one at a time and
   recorded.
7. **Ticks** on the ratified change's `tasks.md` Phase 2, each with its sha.

## Risks, and what is done about them

| risk | mitigation |
|---|---|
| Four of five frozen copies move, one is missed | ratified task 2.6: revert exactly one, five times, and observe red |
| An unrouted `kind` silently validates nothing | `KIND_TO_SCHEMA` row is a named task; the positive example proves the route by validating, the shape fixture proves it by failing |
| The verdict scan is copied rather than shared, and drifts | the scan is extracted to one function called from both check paths |
| A realizer mints a finding code for the schema failure | ratified design D13 names the emitter; the fixture declares `schema`, which the closed-set test excepts by name |
| The gate's `N/N` line moves | the new negative fixture declares `schema`, which is not in the probed set, so N stays 26 |
| The bundle version advances with no inventory | the inventory is built by `validate-contract-release.py build` in the same commit set |
| A shared-index commit sweeps another session's work | explicit pathspecs; `git diff --cached --stat` inspected before each commit |

## Out of scope

See [spec.md](./spec.md) § Out of Scope. In one line: **no xFactory byte, no
codexFactory byte, no host job, no retirement, no tag, no archive.**
