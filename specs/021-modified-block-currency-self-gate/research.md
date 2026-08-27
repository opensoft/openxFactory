# Research: The modified-block-currency self-gate

Ten questions the design had to settle, each with what was measured or read to
settle it. Nothing here is a NEEDS CLARIFICATION carried forward — the spec has
none.

---

## R1 — How does the precedent build a context for a real-tree run?

**Read**: `tests/doc-health/test_family_enumeration.py:149-171`
(`test_the_real_corpus_reads_zero_on_both_halves`).

**Decision**: a two-attribute stand-in, exactly as that precedent does:

```python
class Ctx:
    repo_paths = {"openxFactory": <root>}
    agg_root = None
```

**Rationale, MEASURED not assumed.** `fam_modified_block_currency` reads exactly
one attribute off its context —

```text
$ grep -n "ctx\." scripts/doc_health/modified_block_currency.py
1181:    scoped = [(repo, Path(path)) for repo, path in sorted(ctx.repo_paths.items())
```

— and hands the context itself to `promotion_fidelity.load_dispositions(ctx,
FAMILY)`, which reads `getattr(ctx, "agg_root", None)` and nothing else
(`promotion_fidelity.py:739`). Two attributes is the whole surface.

**Alternatives considered.** `conftest.make_ctx(family)` builds a context over
`tests/doc-health/fixtures/<family>/` and is the wrong tree by construction.
`runner.build_context(args)` builds the real thing but needs argparse namespace
plumbing and `corpus.load_docs` over the whole repository (~4s) for fields this
family never reads.

**The residual risk, and how it is closed.** "Two attributes today" is not a
guarantee about tomorrow. FR-018 asserts the surface structurally: a test greps
the module and asserts the `ctx.` access set is exactly `{repo_paths}`. Widen the
family's context read and that test reds, which is the signal to widen the
stand-in — rather than discovering the gap from a wrong verdict.

---

## R2 — Should the gate be revision-addressed?

**Read**: `test_ideation_readiness.py:40-99` (`_openxfactory_root`),
`:460-506` (the `git archive` reader),
`test_modified_block_currency.py:1361-1389`
(`test_the_promoted_reader_cannot_reach_a_measurement_basis`).

**Decision: NO.** Mirror the resolver **discipline**; do not mirror the
`git archive` mechanism. Recorded as orchestrator decision D4, flagged for veto.

**Rationale.** `harden-ideation-readiness-check` revision-addresses because its
subject is an index that *pins* `generation.source_revision` — a proof against
any other corpus state proves nothing, and the live-tree comparison had already
broken once when the corpus grew past the index. This family has no pin. It
measures the checkout by contract, and F1 asserted that structurally:

```python
assert list(inspect.signature(mbc.promoted).parameters) == ["root", "capability"]
assert list(inspect.signature(mbc.active_blocks).parameters) == ["root"]
```

plus a source grep forbidding `WorkingTree(`, `GitRefTree(`, `.resolve_ref(`,
`.ls_tree_paths(`, `.show_blob(` and `ctx.git`. There is nothing for a revision
to arrive through, and building one in the *test* would measure a different
subject from the one the report the steward reads measures.

**What is mirrored**: the resolution order's first rung and its failure mode —
the repository under test first, confirmed by a marker, and a **named failure**
rather than an ancestor walk. The defect that packet fixed is precisely the one
this gate must not reintroduce: "the bare ancestor walk this replaces always
terminated on the one shared checkout beneath the aggregation root, whatever
repository the run was launched against — so an agent worktree's verdict was a
verdict about another session's working tree."

---

## R3 — Is `_openxfactory_root` shared, and can it be reused?

**Read**: `test_ideation_readiness.py:25-38`, the comment above the resolver.

**Decision**: no, and no. It is a module-private function in one test file, and
the file's own comment records that **three copies exist deliberately**, tracked
as that packet's open Q3: "If you edit one, edit all three; the shape is small on
purpose."

Its marker is `ideation/cross-reference.yaml`, which is the wrong marker for this
family — a checkout could carry it and carry no `openspec/changes/` at all. So
the gate resolves on the markers **this** family needs
(`openspec/changes/` as a directory, `openspec/specs/doc-health/spec.md` as a
file) and does not import or copy the ideation resolver. Mirroring the discipline
without cloning a fourth copy of a function whose duplication is already an open
question.

---

## R4 — What does the family actually report over this checkout?

**Measured at `76a2ad27`**, through `fam_modified_block_currency` with the
two-attribute context:

- 22 active MODIFIED blocks, over 12 changes and 13 capabilities
- 1 `warning` — `add-composed-view-authoring` / `ideation-dashboard` /
  `Composed views are read-only with a repository jump`, omitting canon's
  `Gate verbs hide on a composed view`
- 9 `info` — the triples are tabulated in `plan.md` § The named subjects
- 0 unresolved, 0 ordering, 0 marker defects, 0 `error`, 0 `critical`

**The packet's § 4.1 figure of 11 `info` is stale** — taken at `9be81a40` over 23
blocks, before `add-hermes-customer-subject-runtime-contract` and
`add-shared-identity-seeds` archived. Orchestrator decision D1.

---

## R5 — Which document is § 2.1's block measured against?

**Measured**:

```python
basis, status = mbc.resolve(own_block, mbc.promoted(root, "doc-health"),
                            mbc.sibling_titles(root))
# status == "canon"
# basis.spec_rel == "openspec/specs/doc-health/spec.md"
```

and `add-family-enumeration-check` is **not** an active change —

```text
$ ls openspec/changes/ | grep -c family-enumeration
0
$ ls openspec/changes/archive/ | grep family-enumeration
2026-08-27-add-family-enumeration-check
```

**Decision**: the gate asserts the basis is **canon** and asserts the sibling's
**absence**, so the packet's § 4.2 wording ("measured against
`add-family-enumeration-check`'s outcome") is visibly history rather than
silently unmet. Orchestrator decision D2.

**Consequence for the ordering arm, checked rather than assumed.** The
declarations reader finds six declaring pairs in this tree, two of them from this
change (`add-modified-block-currency-check` naming `add-doxchat-model-intake` and
`add-composed-view-authoring`). None of them is a *two-MODIFIED-writers* group on
one requirement, so `_arm_ordering` reports nothing — the packet's § 6.7
re-measurement ("0 two-MODIFIED pairs at the branch point, 1 with § 2.1 present,
0 findings either way") holds in its zero-findings conclusion, and its "1 pair
with § 2.1 present" clause no longer applies because the second writer archived.

---

## R6 — Can the report CLI be run as a subprocess from inside pytest?

**Read**: `tests/hermeticity.py:1-90` (the two layers, `GUARDED_BINARIES = ("nlm",
"gh", "omp")`), `scripts/doc_health/runner.py:77-92`
(`_real_notebook_dryrun`), `:156-172` (`build_context`).

**Decision**: yes, for a **single-repo** run, and the reason is structural rather
than empirical luck.

```python
def _real_notebook_dryrun(agg_root):
    def run():
        if agg_root is None or not (agg_root / SYNC_SCRIPT).is_file():
            return None          # ← the single-repo path; nlm is never reached
```

`build_context` sets `agg_root = None` whenever `--single-repo` is passed, so the
only `nlm` call site in the runner returns before spawning anything. `gh` and
`omp` have no call site in the doc-health runner at all. Layer 2's in-process
seams (`workbench._default_runner`, `session_pr.SubprocessCommandRunner.run`) are
in modules the runner never imports.

**Cost, measured**: 6.8s per report run, so ~14s for the pair against a 51s
suite. Accepted, and tracked in `plan.md` § Complexity Tracking.

**Alternatives considered.** Running `runner.run_suite` in-process twice — avoids
the subprocess but needs the full `Context` (R1's rejected path) and compares
`Finding` objects rather than rendered lines, which is not what "moves in no
other line" means. Recording the diff in evidence only — D3 considers and rejects
this: the claim rots on the first shared-reader change.

---

## R7 — What exactly moves between the two report runs?

**Measured**, `diff without.md with.md` over two single-repo runs of this
checkout:

| # | line | class |
| --- | --- | --- |
| 1 | `Findings: 5 critical, 7 error, 42 → 43 warning, 4 → 13 info.` | the headline |
| 2 | `- \`modified-block-currency\` — skipped by run configuration` (removed) | the skipped-family notice |
| 3 | `### modified-block-currency` section: `Skipped: skipped by run configuration` → 10 finding rows | the family's own section |
| 4 | 10 `severity=… family=modified-block-currency …` rows added | the ranked-plan rows for this family |

**24 changed lines in FIVE hunks** — the headline, the skip notice, the family's section,
and two in the ranked plan (its `warning` row and its nine `info` rows land in
separate hunks). The four LINE CLASSES sit in three SECTIONS; the hunk count is a
property of `diff`, not of the claim. `## Per-Stage Counts`, `## Preflight`, every other
`### <family>` section, and the semantic/catalog sections are **byte-identical**.

**§ 4.5 IS SELF-CONTRADICTORY AS WRITTEN, and the gate implements the reading
that makes sense.** It asks for "+1 `warning`, +11 `info`, 0 `error`, 0
`critical`, **headline unchanged**" — but the headline is the line the warning and
info counts are printed on, so a run that gains a warning *cannot* leave it
unchanged. Read as: the `error` and `critical` **bands** do not move (so a
`--fail-on error` run is unaffected by construction), and census / inventory /
catalog are untouched. That is what the gate asserts, and the four line classes
above are what it permits to move.

---

## R8 — Does F1's own-packet hook (T057) exist?

**Measured**:

```text
$ grep -rn "reads_its_own_packet\|its_own_packet" tests/
$ echo $?
1
```

**No.** F1's `tasks.md:235` records T057 as `[x]` and its § Hand-off states "the
own-packet assertion F3 § 4.2 wants is live". Neither the function name
`test_the_family_reads_its_own_packet_s_delta` nor an assertion of its content
appears anywhere under `tests/`.

The closest thing that does exist is F2's
`test_the_packets_own_marker_templates_are_not_marker_form`
(`test_modified_block_currency_fixtures.py:908`), which reads the same file for a
different purpose — it asserts the packet's two marker *templates* are not of
marker form. It says nothing about discovery or about the basis.

**Decision**: F3 writes the assertion. Nothing is duplicated because nothing
exists. Recorded as orchestrator decision D5 and reported as F1 residue finding 6
(F2 recorded 1–5).

---

## R9 — How should an assertion that WILL fall due be written?

**Read**: `test_modified_block_currency.py:381-419`
(`test_the_real_notes_this_corpus_carries_are_each_one_unit`) — the precedent for
this exact problem, and its own record of getting it wrong first: "it pinned
`== 2` and broke the moment `add-family-enumeration-check` archived and promoted
its third note. The population GROWS every time the corpus records a repair on
this requirement, so pinning it exactly makes an unrelated archive look like this
family's regression."

**Decision**, three rules taken from that lesson:

1. **A floor where the population only grows** — the discovery floor is `>= 1`,
   not `== 22`. The number of MODIFIED blocks in the corpus is nobody's
   invariant.
2. **An exact set where the population is the claim** — the nine `info` triples
   are asserted as set equality, because "which requirements are currently lossy"
   IS the claim, and a subset assertion would let a new lossy block land
   unreported.
3. **A failure message that names the remedy** — FR-016. `add-composed-view-authoring`
   declaring its rename is the disposition the packet's § 6.3 already calls
   correct, so the `warning` assertion is *expected* to fall due, and the message
   must say so rather than leave the next engineer to guess whether the family
   broke.

The end state is explicit in the message: **if the family reads zero over this
tree, that is the desired outcome** — assert zero by the same named-subject
mechanism and keep the discovery floor, which is exactly the shape
`test_the_real_corpus_reads_zero_on_both_halves` took after its own subject was
promoted.

---

## R10 — What is the RED form of each test?

RED-first is FR-020 and there is no code to break, so each test's RED is produced
by asserting something the tree does not say. Two shapes:

- **Wrong named subject** — assert a subject the corpus does not carry (a
  neighbouring change id, a renamed requirement title, the *destination* of the
  composed-view rename rather than canon's title). The test fails naming the
  subject, which also demonstrates FR-016's message.
- **A tree with the family skipped** — for the movement pin, run BOTH passes with
  `--skip-family modified-block-currency`. The movement then reads 0/0/0/0 and the
  pin fails, which is the same manoeuvre as the mutation-round mutant.

For the resolver guard the RED is a wrong root: pass the parent directory (the
worktrees container) as `under_test` and assert it fails. That RED is *kept* as a
permanent test rather than discarded, because it is the assertion that the
resolver does not walk up.

The full per-test RED table is in `contracts/self-gate-contract.md`; the observed
RED output is recorded in `evidence/self-gate.md`.
