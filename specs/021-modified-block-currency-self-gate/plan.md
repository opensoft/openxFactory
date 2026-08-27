# Implementation Plan: The modified-block-currency self-gate

**Branch**: `021-modified-block-currency-self-gate` | **Date**: 2026-08-27 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/021-modified-block-currency-self-gate/spec.md`

## Summary

Add one test module, `tests/doc-health/test_modified_block_currency_self_gate.py`,
that runs the `modified-block-currency` family over **this checkout** through the
family's own entry point and asserts what it finds **by named subject**. Add one
evidence file recording the three gates with their numbers and the exact commands.
No module changes; no `openspec/` or `.github/` changes.

The feature's whole difficulty is not writing assertions. It is writing
assertions about a **live corpus** that (a) cannot pass vacuously, (b) cannot
lie about which tree they measured, and (c) tell the next engineer what to do
when the corpus legitimately moves under them.

## Technical Context

**Language/Version**: Python 3.12 (stdlib only, as the doc-health package is)

**Primary Dependencies**: `scripts/doc_health/modified_block_currency.py` (F1,
unmodified); `scripts/doc-health.py` CLI for the report gate; `pytest`

**Storage**: N/A — the corpus is the filesystem under test

**Testing**: `pytest tests/doc-health` (the suite of record; the whole-tree
`pytest tests` drives live Postgres and is never run from a worktree)

**Target Platform**: Linux; the doc-health suite runs in
`.github/workflows/pytest-suite.yml` and in `doc-health-reusable.yml`

**Project Type**: governance tooling — a validator package plus its test suite

**Performance Goals**: the added tests must not materially slow the gate. Budget:
under 20s added to a 51s suite. The corpus family run is ~0.3s; the two report
runs are ~7s each.

**Constraints**: hermetic (no network, no `nlm`/`gh`/`omp` — the structural guard
in `tests/hermeticity.py`); deterministic; must not read any tree other than the
checkout under test.

**Scale/Scope**: 22 active MODIFIED blocks over 12 active changes and 13
capabilities in this checkout; 10 findings; one new test module of ~10 tests.

## Constitution Check

| Principle | Verdict | Basis |
| --- | --- | --- |
| **I. Contract-First, Domain-Neutral Core** | PASS | Tests only. No domain vocabulary enters; the named subjects are openxFactory's own change ids and requirement titles. |
| **II. Governed Change Flow: OpenSpec Before Implementation** | PASS | `add-modified-block-currency-check` was ratified 2026-08-27 before any code and declares `code_surface:` / `target_release:`. This is the third of the four Speckit features its § 2–§ 5 decompose into. `tasks.md` here references § 4's boxes rather than restating them. |
| **III. Document Lifecycle and Status Discipline** | PASS | No governance document is authored or re-statused. The evidence file is a feature artefact under `specs/`, not a governance doc. |
| **IV. Schema and Artifact Discipline** | PASS | No YAML, no schema, no template. |
| **V. Validation Gates (NON-NEGOTIABLE)** | PASS — and this feature IS a gate | `pytest tests/doc-health` and `openspec validate --all --strict` both run and are recorded with counts; the doc-health report is run twice and diffed. |
| **VI. Versioned, Content-Addressed Releases** | N/A | No release surface. |
| **VII. Fail-Closed Authority Boundaries** | PASS | The family stays advisory (`_LAUNCH_SEVERITY` WARNING, absent from `FAMILY_RESOLUTION`); this feature asserts that state and does not move it. No authority claim is added. |

**Repository constraints**: this feature runs from its own worktree
(`../openxFactory-worktrees/021-modified-block-currency-self-gate`), commits with
explicit pathspecs, and never runs `git add -A`.

**Post-design re-evaluation**: unchanged. The design adds one test module and one
evidence file. The single judgement call the design makes — running the report
CLI as a subprocess from inside pytest — is examined in `research.md` R6 against
Principle V's hermeticity expectation and passes because a single-repo run has no
aggregation root and therefore never reaches `nlm` (`runner._real_notebook_dryrun`
returns immediately when `agg_root is None`).

## THE FIGURES — RE-MEASURED AT `76a2ad27`, AND THE PACKET'S ARE STALE

**Measured by this session, at this branch point, with the family registered and
§ 2.1's block present.** The commands are in `evidence/self-gate.md`; this table
is the single home for the figures in this feature and nothing else restates
them.

| | measured at `76a2ad27` |
| --- | --- |
| active MODIFIED blocks examined | **22** (over 12 changes, 13 capabilities) |
| scenario-title arm | **1** `warning` |
| carriage ledger | **9** `info` |
| resolution arm (unresolved) | **0** |
| ordering arm (two-writers undecided) | **0** |
| marker-defect class | **0** |
| `error` / `critical` | **0** / **0** |

**Report movement, from two single-repo runs of this checkout differing only by
`--skip-family modified-block-currency`:**

```text
without: 5 critical, 7 error, 42 warning,  4 info
with:    5 critical, 7 error, 43 warning, 13 info
         ------------------------------------------
movement:      0          0        +1        +9
```

This is byte-for-byte what F1's `plan.md` § Predicted movement recorded at its
own branch point, re-measured here rather than inherited. F1 is the origin of the
figure; this feature is where it becomes an assertion.

### The named subjects

**The one `warning`** —
`openspec/changes/add-composed-view-authoring/specs/ideation-dashboard/spec.md`,
requirement `Composed views are read-only with a repository jump`, omitting
canon's scenario `Gate verbs hide on a composed view`. A deliberate rename (the
packet's § 6.3), the case the `Removed from canon by` marker exists for, and
**not** claimed as a defect.

**The nine `info`**, as `(change, capability, requirement title)`:

| change | capability | requirement |
| --- | --- | --- |
| `add-composed-view-authoring` | `ideation-dashboard` | Composed views are read-only with a repository jump |
| `add-doxchat-model-intake` | `ideation-dashboard` | doxBench model catalog and provider boundary |
| **`add-modified-block-currency-check`** | **`doc-health`** | **Deterministic check families** |
| `add-notebook-projection-identity` | `lifecycle-notebook-projection` | The session namespace is reconciled against live sessions |
| `declare-client-standing-policy-contract` | `client-layer-tuning` | Client content shapes are contract-validated |
| `qualify-avatar-live-voice` | `avatar-client-lab` | Repository and ownership boundary |
| `qualify-avatar-live-voice` | `avatar-client-runtime` | Redacted telemetry and latency evidence |
| `qualify-avatar-live-voice` | `avatar-client-runtime` | Versioned neutral avatar-client contract kernel |
| `qualify-avatar-live-voice` | `repo-boundary-governance` | Neutral avatar-client repository boundary |

The bold row is the self-finding: § 2.1's block does not carry canon's two stale
numeral sentences (`twenty-one check families`, `Four of the twenty-one`). It is
expected, advisory, and **must never be dispositioned** — it is the evidence that
the family reads its own packet.

## Decisions taken by the orchestrator — FLAGGED FOR VETO

**Five decisions were taken for this feature by the orchestrating session before
authoring began. None is backed by a ruling from Brett.** Reverting any one of
them is an edit to this plan rather than a new feature. D1 and D2 reconcile the
packet against a tree it no longer describes; D3–D5 are method.

---

**D1 — THE PACKET'S § 4.1 FIGURE IS STALE, AND THE GATE ASSERTS THE CURRENT
MEASURED TRUTH.**

§ 4.1 says "1 scenario-arm finding, 11 carriage-ledger findings, 0
title-resolution findings", from § 6.6's prediction of "16 units across 11
requirements, +1 warning and +11 info". That figure was taken at `9be81a40` over
**23** MODIFIED blocks. This tree carries **22**, and two changes
(`add-hermes-customer-subject-runtime-contract`, `add-shared-identity-seeds`)
archived in between. Re-measured here: **+1 `warning`, +9 `info`**.

The gate asserts what the tree produces now, re-measured at `76a2ad27` through
the family itself, and names the packet's numbers in the test module's docstring
as **history**. It never asserts a count the tree no longer produces.

*Cost of a veto*: asserting 11 `info` reds the gate on its first run, so a veto
means either re-opening the packet to correct § 4.1 (the honest option) or
building the tree the figure describes (impossible — two changes archived). The
figure's provenance is preserved either way: F1's `plan.md` records it, this
plan records it, and the test docstring records it.

---

**D2 — § 2.1's BLOCK IS MEASURED AGAINST CANON, NOT AGAINST
`add-family-enumeration-check`'s OUTCOME.**

§ 4.2 asks the gate to assert that the block "is measured against
`add-family-enumeration-check`'s outcome". That sibling **archived** at
`f027d3b3` (PR #419) before F1 registered the family, so it is not among this
tree's active changes and there is no sibling outcome to measure against. F1's
T052 wrote the block against canon for exactly this reason. Measured here:
`resolve()` returns status `canon` with basis `openspec/specs/doc-health/spec.md`.

The gate therefore asserts § 4.2's *purpose* — that discovery reaches the
packet's own delta and that the delta is compared against a named basis — with
the basis being canon, and asserts the sibling's **absence** so the packet's
wording is visibly history rather than silently unmet.

*Cost of a veto*: the gate would have to assert a basis no reader can name,
which is the exact defect `release-realization`'s "Ordered deltas" rule exists to
prevent. A veto here is really a veto on F1's T052, which has already landed.

---

**D3 — § 4.3, § 4.4 AND § 4.5 ARE GATES; § 4.5 IS ALSO ONE TEST.**

§ 4.3 (the suite), § 4.4 (`openspec validate`) and § 4.5 (the report diff) are
worded as measurements to record, not as behaviour to assert. They are recorded
in `evidence/self-gate.md` with their commands and numbers.

§ 4.5 additionally becomes a test, because it is the one place a **count**
assertion is worth its cost and the only place the "moves in no other line"
claim can be mechanically held. It is written as a **diff between two runs of
this checkout** — with the family, and with `--skip-family
modified-block-currency` — never against a hard-coded total and never against
another worktree's `main`.

*Cost of a veto*: the report claim reverts to a recorded observation that rots
the first time a shared reader changes. The suite pays ~14s.

---

**D4 — NO REVISION-ADDRESSING. THE RESOLVER DISCIPLINE IS MIRRORED; THE
`git archive` MECHANISM IS NOT.**

`test_ideation_readiness.py` reads both sides revision-addressed
(`harden-ideation-readiness-check`) because its subject is an index that **pins a
revision** — the proof is meaningless against any other corpus state. This family
has no such pin: it measures the **checkout** by contract, and F1's
`test_the_promoted_reader_cannot_reach_a_measurement_basis` asserts structurally
that `promoted(root, capability)` has no ref, no git shim and no context to
receive one. Revision-addressing here would contradict a landed pin.

What IS mirrored is the resolution **discipline** that packet fixed: resolve the
**repository under test** first, confirm it by markers, and **fail with a named
reason rather than walking up**. The bare ancestor walk that defect describes
always terminated on the one shared checkout beneath the aggregation root, so an
agent worktree's verdict was a verdict about another session's working tree. This
gate additionally asserts that the resolved root is the same tree the test file
lives in.

*Cost of a veto*: revision-addressing this gate means reading `openspec/` out of
`git archive` at HEAD, which measures committed state rather than the working
tree — a different (and defensible) subject, but one that would no longer match
what the report the steward reads measures, and one F1's structural pin forbids
the family itself from doing.

---

**D5 — F1's OWN-PACKET HOOK (T057) DOES NOT EXIST, AND F3 WRITES IT RATHER THAN
WAITING FOR F1 TO.**

F1's `tasks.md` records T057 — `test_the_family_reads_its_own_packet_s_delta` —
as `[x]`, and its § Hand-off tells F3 "the own-packet assertion F3 § 4.2 wants is
live". **It is not.** No function of that name, and no assertion of that content,
exists anywhere under `tests/`:

```text
$ grep -rn "reads_its_own_packet\|its_own_packet" tests/
$ echo $?
1
```

F2's own residue section already records five F1 artefact discrepancies; this is
a sixth and it is the only one with a behavioural consequence, because F3's § 4.2
was scoped on the assumption the hook was there. F3 writes the assertion. It is
**not** a duplicate — there is nothing to duplicate — and this plan records the
discrepancy so F1's owner reads it.

*Cost of a veto*: F3 stalls on an F1 amendment that would land the same test in a
different file. The assertion is small and belongs beside the rest of the
self-gate.

## Project Structure

### Documentation (this feature)

```text
specs/021-modified-block-currency-self-gate/
├── spec.md                         # the feature specification
├── plan.md                         # this file
├── research.md                     # R1–R10, the design questions and their answers
├── data-model.md                   # the four entities the gate manipulates
├── contracts/
│   └── self-gate-contract.md       # what each test asserts, and its RED form
├── quickstart.md                   # how to run and re-measure the gate
├── evidence/
│   └── self-gate.md                # the three gates, their commands, their numbers
├── checklists/
│   └── requirements.md             # spec quality checklist
└── tasks.md                        # generated by /speckit-tasks
```

### Source Code (repository root)

```text
tests/doc-health/
├── conftest.py                                   # REPO_ROOT, make_ctx, FakeGit — READ, not edited
├── test_modified_block_currency.py               # F1's behavioural suite — NOT edited
├── test_modified_block_currency_fixtures.py      # F2's regression catalogue — NOT edited
├── test_family_enumeration.py                    # the real-corpus precedent — READ, not edited
├── test_ideation_readiness.py                    # the resolver precedent — READ, not edited
└── test_modified_block_currency_self_gate.py     # ← THE ONLY FILE THIS FEATURE ADDS

scripts/doc_health/modified_block_currency.py     # F1's module — NOT edited (FR-019)
```

**Structure Decision**: one new test module in `tests/doc-health/`, beside F1's
and F2's. A separate file rather than an appendix to F1's, for three reasons: the
subject is different (a live corpus, not a fixture), the maintenance obligation
is different (it moves when the corpus moves, and its docstring must say so), and
a reviewer bisecting a corpus failure should not have to read 1409 lines of
fixture behaviour to find it. `conftest.py` supplies `REPO_ROOT`; nothing in
`conftest.py` changes.

## Design: how each assertion avoids being vacuous

The gate has **three independent guards**, and the design turns on their
independence. A single guard that both proves discovery ran and names what it
found can be satisfied by a mutant that breaks one half.

1. **The resolver guard** — the resolved root is this checkout, confirmed by
   markers, cross-checked against the test file's own location, and asserted to
   be a git toplevel equal to itself. A resolver pointed anywhere else fails
   here, before any finding is read.
2. **The discovery floor** — `active_blocks(root)` is non-empty, asserted in its
   own test with no reference to any finding. A broken read fails here with
   "examined 0 MODIFIED blocks over <root>", not with a moved count.
3. **The named subjects** — the `warning`'s subject, the nine `info` triples as
   an exact set, and the empty classes by rule text. These fail by name.

Guard 3 alone would pass on a tree where discovery worked but the corpus was
clean (an empty finding set is not an empty read). Guard 2 alone would pass on a
tree where every finding was wrong. Guard 1 alone would pass on the right tree
read by a broken family. All three are needed, which is why the mutation round
targets one each.

### The lightweight context, and why it is faithful

`fam_modified_block_currency(ctx)` reads exactly two things from its context:
`ctx.repo_paths`, and — through `promotion_fidelity.load_dispositions(ctx,
FAMILY)` — `getattr(ctx, "agg_root", None)`. So a two-attribute stand-in is
faithful, which is what `test_family_enumeration.py`'s real-corpus precedent
already relies on (`class Ctx: repo_paths = {...}`).

"Faithful because I read the source once" is not a guarantee. FR-018 makes it
structural: a test greps the module for `ctx.` attribute access and asserts the
set is exactly `{repo_paths}` plus the `load_dispositions(ctx, …)` handoff. A
future field added to the family's context read reds that test, which is the
signal to widen the stand-in rather than to discover the gap from a wrong
verdict.

### The failure messages are a deliverable

Every corpus assertion's message names: the resolved root, the subject that
moved, that **corpus movement is the expected cause**, and the two legitimate
responses —

> re-measure with `python3 scripts/doc-health.py --single-repo . --family
> modified-block-currency` and update the named set in this module; or, if the
> family now reads ZERO over this tree, that is the desired end state — assert
> zero by the same named-subject mechanism and keep the discovery floor.

This is FR-016 and SC-001. `add-composed-view-authoring` declaring its rename
with a marker, or archiving, is not a hypothetical: it is the disposition the
packet's § 6.3 already identified as correct, so this gate's `warning` assertion
is expected to fall due.

## Complexity Tracking

| Complexity | Justification | Alternative rejected |
| --- | --- | --- |
| Two report subprocess runs (~14s) inside the suite | The "moves in no other line" claim is the blast-radius bound for registering a twenty-second family, and it cannot be held by inspection. Stated as a diff, it also self-documents the before-state. | Recording the diff in evidence only — rots on the first shared-reader change. Comparing against another worktree's `main` — forbidden: it measures a tree nobody asked about. |
| A named-subject set of nine triples that will move | The packet's own § 4.1 forbids bare counts, and a set that moves with the corpus is the price of a non-vacuous claim. FR-016's failure message pays it down. | A count assertion — vacuous on a broken read, which is the defect § 4.1 names. A regex over the section — passes on a section rendering the wrong subjects. |
| A structural grep for `ctx.` access (FR-018) | It is the only way "the lightweight context is faithful" stays true after someone widens the family's context read. | Building the real `runner.Context` — needs `corpus.load_docs` over the whole repo (~4s) plus fields the family never reads, and would still not detect a newly-read field. |

## Sequencing and dependencies

F1 (`19e3f6b5`) and F2 (`76a2ad27`) are both on `main` and this branch's base is
`76a2ad27`, so nothing blocks. F4 is blocked on this feature and inherits three
things from it: the measured figures table above, the evidence file's commands,
and the fact that this gate's `warning` assertion falls due when
`add-composed-view-authoring` moves.

**One live risk, named rather than mitigated**: any change landing on `main`
between this branch's head and its merge that edits an active MODIFIED block, or
archives one of the twelve changes in the table, moves the named-subject set. The
gate then fails on merge with FR-016's message, which is the designed behaviour —
re-measure and update. This is why the feature is small and why the figure lives
in one place.
