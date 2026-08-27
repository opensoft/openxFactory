# Evidence: the modified-block-currency self-gate

Every number below names the tree it was taken at. Commands are given verbatim so
a reader can re-run them; nothing here is asserted from memory.

**Tree**: `/home/brett/projects/xFactory/openxFactory-worktrees/021-modified-block-currency-self-gate`,
branch `021-modified-block-currency-self-gate`, merge base `76a2ad27`
(F2's merge, PR #426).

**Never run `python3 -m pytest tests`** (the whole tree) from a worktree: it
drives live Postgres containers. `tests/doc-health` is the suite of record
(F1 ruling N12).

---

## 1. Packet § 4.3 — the suite, before and after

```bash
python3 -m pytest tests/doc-health -q
```

| when | result |
| --- | --- |
| **BASELINE**, at `76a2ad27` before a line of test code existed | **1115 passed**, 4 warnings, 51.12s |
| **AFTER**, with `test_modified_block_currency_self_gate.py` | **1130 passed**, 4 warnings, 61.33s |
| **BASELINE re-derived** at `175682e2` merged in, this file moved aside | **1163 passed**, 7 warnings, 137.74s |
| **AFTER**, same tree | **1178 passed**, 7 warnings, 180.58s |

**Delta +15 in both measurements**, which is the fifteen tests this feature adds —
visible as a delta rather than asserted (SC-006). The absolute numbers moved by
48 because merging `origin/main` brought in PR #424's own
`tests/doc-health/test_pin_reachability.py`; the DELTA is the figure this feature
owns, and the baseline was re-derived by moving this file aside rather than by
subtracting.

**The sibling suites are unchanged** — F1's, F2's, the enumeration collateral and
the scan-set classification:

```bash
python3 -m pytest tests/doc-health/test_modified_block_currency.py \
    tests/doc-health/test_modified_block_currency_fixtures.py \
    tests/doc-health/test_family_enumeration.py \
    tests/doc-health/test_lifecycle_scan_set.py -q
# 176 passed in 1.14s
```

## 2. Packet § 4.4 — `openspec validate`

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
# Totals: 76 passed, 0 failed (76 items)
```

**76** = 24 active changes + 52 promoted specs, run from the repository root per
the aggregation `CLAUDE.md`'s authoring note. Unchanged before and after — this
feature adds no OpenSpec artefact.

**THE FIGURE MOVED SINCE F1, AND THE ITEM IS NAMED.** F1's `plan.md` recorded
**75** at its own branch point ("having been 77 when this feature started and 76
before the archive"), and the orchestrator's brief for this feature also said 75.

The item the tree gained is **`openspec/changes/govern-derived-pin-reachability`**
— PR #416, merge commit `d2ed6d34`, "The pin two packets deferred: an orphaned
`source_revision` is a defect". Verified rather than inferred:

```bash
git cat-file -e 19e3f6b5:openspec/changes/govern-derived-pin-reachability/proposal.md
# fatal: … exists on disk, but not in '19e3f6b5'      ← absent at F1's branch point
git log --oneline -1 d2ed6d34
# d2ed6d34 Merge pull request #416 from opensoft/change/govern-derived-pin-reachability
```

So 75 → 76 is one new ACTIVE change, not a spec, and nothing this feature did.
"The tree gained an item" was the first wording here and the review was right to
reject it: an unexplained count discrepancy in an evidence file is the thing
evidence exists to prevent.

## 3. Packet § 4.5 — the report, moved by exactly this family and nothing else

```bash
python3 scripts/doc-health.py --single-repo . --report-out /tmp/with.md
python3 scripts/doc-health.py --single-repo . \
        --skip-family modified-block-currency --report-out /tmp/without.md
diff /tmp/without.md /tmp/with.md
```

```text
at 76a2ad27 (branch point)          at 175682e2 merged in — CURRENT
without: 5c 7e 42w  4i              without: 5c 7e 40w  4i
with:    5c 7e 43w 13i              with:    5c 7e 41w 12i
         -----------------                   -----------------
movement:  0  0 +1 +9               movement:  0  0 +1 +8
```

24 changed lines in 5 hunks at the branch point; **22 in 5 hunks at the merged
head**, the two fewer being the ledger row that went away in both the section and
the ranked plan. The `error` and `critical` bands do not move in either.

**The branch-point diff, line by line — 24 changed lines in 5 hunks, 3 sections:**

| hunk | line(s) | class |
| --- | --- | --- |
| `9c9` | `Findings: … 42 → 43 warning, 4 → 13 info.` | the headline |
| `17d16` | ``- `modified-block-currency` — skipped by run configuration`` | the skipped-family notice |
| `183c182,191` | `Skipped: …` → the family's 10 finding rows | `### modified-block-currency` |
| `210a219` | 1 `severity=warning family=modified-block-currency …` row | `## Ranked Plan` |
| `255a265,273` | 9 `severity=info family=modified-block-currency …` rows | `## Ranked Plan` |

**Byte-identical**: `## Per-Stage Counts`, `## Preflight`, `## Findings By
Family`'s other twenty-one `### <family>` sections, `### semantic-normative-prose`,
`### semantic-contradiction`, `### preflight`, and the report preamble. Census,
inventory and catalog untouched.

**§ 4.5 IS SELF-CONTRADICTORY AS WRITTEN, and this is the reading implemented.**
It asks for "+1 `warning`, +11 `info`, 0 `error`, 0 `critical`, **headline
unchanged**". The headline is the line the warning and info counts are printed
on, so a run that gains a warning cannot leave it unchanged. Read as: the `error`
and `critical` BANDS do not move — so a run configured `--fail-on error` or
`--fail-on critical` is unaffected by construction — and census / inventory /
catalog are untouched.

The pin lives in
`test_the_report_moves_only_in_this_family_s_lines`, and it asserts the movement
against **the family's own per-severity finding counts taken from the same tree
in the same test**. The literals `1` and `9` appear nowhere in it.

## 4. The re-measured corpus verdict

```bash
python3 scripts/doc-health.py --single-repo . --family modified-block-currency
```

| | at `76a2ad27` |
| --- | --- |
| active MODIFIED blocks examined | **22** (12 changes, 13 capabilities) |
| scenario-title arm | **1** `warning` |
| carriage ledger | **9** `info` |
| resolution arm (unresolved) | **0** |
| ordering arm (two-writers undecided) | **0** |
| marker-defect class | **0** |
| `error` / `critical` | **0** / **0** |

The named subjects are tabulated in `../plan.md` § The named subjects, which is
the single home for them; the test module holds them as `_SCENARIO_SUBJECT` and
`_LEDGER_SUBJECTS`.

**The own-packet resolution, measured:**

```python
basis, status = mbc.resolve(own_block, mbc.promoted(ROOT, "doc-health"),
                            mbc.sibling_titles(ROOT))
# status                          == "canon"
# basis.spec_rel                  == "openspec/specs/doc-health/spec.md"
# len(group of active writers)    == 1
# _arm_ordering(...)              == ({}, [])
```

## 5. RED evidence — every test shown failing first (FR-020)

Two REDs happened **by themselves**, on the module's first run, and both are the
same class of defect this family exists to catch:

| # | test | RED, as observed |
| --- | --- | --- |
| N1 | `…_resolution_ordering_and_marker_classes_read_zero_…` | `AssertionError: probe 'resolves to no promoted requirement' is not the module's own wording, so the absence below would be vacuous` — **the positive control working.** The family writes its rules as adjacent f-string literals, so a phrase contiguous in the OUTPUT is split in the SOURCE. Fixed by `_joined_source`, which closes the seams. |
| N2 | `…_family_reads_exactly_two_things_from_its_run_context` | `AssertionError: the disposition reader now reads a context attribute directly` — matched on a MENTION: `load_dispositions`'s own docstring writes "`runner.main` guards the same read with `if ctx.agg_root`". Fixed by `_without_docstrings`. **The third time this family's tests have learned "match on use, not on mention"** — F1's `test_the_promoted_reader_cannot_reach_a_measurement_basis` learned it the same way. |

The remaining thirteen were shown failing by deliberate mutation, one at a time,
the file restored between each. Driver:
`scratchpad/red.py` (not committed — it edits the tracked file in place).

| test | RED applied | observed failure |
| --- | --- | --- |
| `…repository_under_test_is_the_tree_this_test_file_lives_in` | `ROOT == here.parent` | `assert PosixPath('…/021-…') == PosixPath('…/openxFactory-worktrees')` |
| `…resolver_fails_on_a_checkout_it_cannot_confirm…` | `pytest.raises` around the GOOD root | `Failed: DID NOT RAISE UnresolvedRepository` |
| `…examined_at_least_one_modified_block…` | floor raised to `>= 10_000` | the empty-read message, with `assert 22 >= 10000` |
| `…returns_findings_and_not_a_skip…` | `assert isinstance(out, Skip)` | `the family SKIPPED a tree that carries openspec/changes/` (it did not) |
| `…scenario_arm_names_the_composed_view_rename…` | omitted title set to the rename DESTINATION | `assert "'Tile-bound gate verbs hide on a composed view'" in "… 'Gate verbs hide on a composed view'"` |
| `…every_carriage_ledger_finding…is_named` | one triple DROPPED | `0 named subject(s) NO LONGER reported []; 1 unnamed subject(s) NEWLY reported [('add-doxchat-model-intake', …)]` |
| `…every_carriage_ledger_finding…is_named` | a fabricated triple ADDED | `1 named subject(s) NO LONGER reported [('add-not-a-change', …)]; 0 unnamed` — **both directions fail by name** |
| `…resolution_ordering_and_marker_classes_read_zero…` | `len(unresolved) == 1` | `assert 0 == 1 where 0 = len([])` |
| `…own_delta_is_among_the_blocks_the_family_examined` | own path → a neighbouring packet | `0 block(s): []`, naming the wrong path it looked for |
| `…own_delta_is_measured_against_canon…` | expect status `pending` | `assert 'canon' == 'pending'` |
| `…self_finding_quotes…two_stale_numeral_sentences` | expect `twenty-two` | `assert 'twenty-two check families' in "… 'twenty-one check families' …"` — the arm names what CANON states, not what the block says |
| `…no_disposition_can_apply_in_the_single_repo_scope…` | expect a non-empty set | `assert set() != set()` |
| `…every_corpus_assertion_explains_what_to_do…` | require a command not in the message | `AssertionError: make validate` |
| `…family_reads_exactly_two_things…` | expected set widened to `{"repo_paths", "git"}` | `assert {'repo_paths'} == {'git', 'repo_paths'}` |
| `…gate_reaches_the_corpus_only_through_the_family` | a fourth regex `_SNEAKY = re.compile(r"^#### Scenario: (.+)$")` | `this module's regex set moved: ['_SNEAKY']. A new pattern here is a parser this gate should not own` |
| `…report_moves_only_in_this_family_s_lines` | both passes run with the family SKIPPED | `movement (0, 0, 0, 0)` against a family reporting 1 warning and 9 info |

## 6. Mutation round — six mutants, all killed

**M1 — remove the named-subject assertions; is the floor independent?**
Discovery mutated to return nothing (`mbc.active_blocks = lambda root: []`),
which is invisible to every fixture test in F1 and F2, then the FLOOR TEST RUN
ALONE:

```text
KILLED by the floor:
  DISCOVERY EXAMINED 0 MODIFIED BLOCKS over …/021-… using glob
  'openspec/changes/*/specs/*/spec.md'.
  THIS IS NOT CORPUS MOVEMENT. No repository carrying active changes reads zero
  here, so the family's DISCOVERY broke: check `active_blocks`, `DELTA_GLOB`, the
  `archive/` exclusion and the resolved root — not the named subjects below.

…and the family itself over the mutated discovery: findings: []
  (indistinguishable from a clean corpus)
```

SC-003 discharged: the floor catches the vacuous read **on its own**, and its
message says discovery broke rather than that a count moved.

**M2 — point the resolver at another checkout.** Two forms, and the second is the
one that matters.

*M2a, the resolver pointed at a NON-measurable tree* (`parents[3]`, the worktrees
container): the module **fails at collection** with
`UnresolvedRepository: NOT A MEASURABLE openxFactory CHECKOUT: …/openxFactory-worktrees
does not carry both openspec/changes/ … This resolver does NOT walk up`. Killed
fail-closed, before any test runs.

*M2b, the resolver pointed at a DIFFERENT VALID openxFactory CHECKOUT* —
`/home/brett/projects/xFactory/openxFactory`, the shared submodule tree, which is
**exactly** the tree `harden-ideation-readiness-check`'s ancestor walk always
landed on. **This machine carries fifteen other measurable openxFactory
checkouts**, so this is not a hypothetical. The module imports cleanly and FOUR
tests kill it independently:

```text
the gate resolved /home/brett/projects/xFactory/openxFactory but this test file
  lives in …/openxFactory-worktrees/021-modified-block-currency-self-gate

subject : the scenario-title arm's population (expected exactly 1: …)
observed: 2 warning(s): [… 'Composed views are read-only with a repository jump',
          … 'Staged-topic proposal commissioning' …]

subject : the carriage-ledger population (9 named subjects at 76a2ad27)
observed: 5 named subject(s) NO LONGER reported […]; 5 unnamed subject(s)
          NEWLY reported [('add-doxbench-distilled-abstract', …),
          ('add-family-enumeration-check', 'doc-health', 'Deterministic check
          families'), …]

subject : this change's own MODIFIED block (…/add-modified-block-currency-check/…)
observed: 0 block(s): []
```

That shared checkout is a genuinely different corpus — two warnings, five ledger
subjects this branch does not have, and `add-family-enumeration-check` still
ACTIVE in it. A gate without the resolver guard would have reported its verdict
as this branch's.

**M3 — make discovery skip the own packet.** `_own_block`'s filter neutered:
killed by `…own_delta_is_among_the_blocks_the_family_examined` and
`…own_delta_is_measured_against_canon…`, both naming the path that went missing.

**M4 — widen the context probe's allowed set.** Killed by
`…family_reads_exactly_two_things_from_its_run_context`.

**M5 — run both movement passes with the family skipped.** Killed by
`…report_moves_only_in_this_family_s_lines`: `movement (0, 0, 0, 0)` while the
family reports one warning and nine info.

**M6 — add a fourth regex to the gate.** Killed by
`…gate_reaches_the_corpus_only_through_the_family`.

**Survivals, reported honestly.** M2a is killed at COLLECTION rather than by a
test, so the tests written for it never run in that mutant — which is why M2b
exists and is the one that exercises them. No mutant survived, and no mutant was
killed by only one test except M4, M5 and M6, which are structural pins with one
subject each by design.

## 6a. Second mutation round — the review round (2026-08-27)

The combined review found two structural pins that **survived mutants**, and one
that pinned prose instead of code. Each fix was proven by the mutant it was
written for, applied to `scripts/doc_health/modified_block_currency.py` or to
the gate and then reverted (`git status --porcelain scripts/` clean afterwards).

**N1a — the family gains `getattr(ctx, "git", None)`.** The attribute probe
matched only `ctx.<attr>`, so the *safe* spelling of an attribute access — the
one `promotion_fidelity.load_dispositions` itself uses — went unseen. Mutant
applied beside the disposition call:

```text
E  AssertionError: ['git', 'repo_paths']
E  assert {'git', 'repo_paths'} == {'repo_paths'}
```

Now killed. The probe is a union of `\bctx\.(\w+)` and
`getattr\(\s*ctx\s*,\s*["']( \w+)`.

**N1b — the family gains a SECOND collaborator taking the context.**
`source.count("load_dispositions(ctx") == 1` proved that one KNOWN collaborator
is called once, which is not the claim. A `_second_reader(ctx, FAMILY)` beside it
survived. Now a SET of callees:

```text
E  AssertionError: the family hands its context to ['_second_reader',
   'load_dispositions']; `_ctx`'s two-attribute stand-in is only faithful while
   `load_dispositions` is the one collaborator …
```

Tightening the callee pattern was needed too, and its first cut was wrong in the
other direction: `\(ctx\b` collected `sorted`, because
`sorted(ctx.repo_paths.items())` puts a word boundary right after `ctx`. Reading
an ATTRIBUTE is the first probe's business; handing the whole OBJECT away is this
one's, so the pattern is `\(ctx\s*[,)]` with an optional leading argument group.

**N2 — the allowlist pinned PROSE.** `test_the_gate_reaches_the_corpus_only_
through_the_family` ran its `mbc.` scan over the raw source while its own
docstring said "matched on use, not on mention". Both directions now proven:

```text
mutant: `mbc.carried` named in a DOCSTRING of the gate
   → 1 passed          (a mention is no longer a use — correct)

mutant: `_x = mbc.carried([], [])` in real CODE
   → E AssertionError: reached but not declared: ['carried']
                       (a use is still caught — correct)
```

**AND THE FIX FOR N2 REPRODUCED N2.** The first `_code_only` stripped docstrings
only, and the COMMENT written to explain the fix named a family attribute — which
reddened the equality it was documenting. `_code_only` now strips docstrings AND
whole-line comments (only comments owning their line, so a `#` inside a string
literal — the family compiles `r"^####\s+Scenario:"` — survives). **Three
separate times in this family's test suite, a probe has been caught matching a
mention**: F1's `test_the_promoted_reader_cannot_reach_a_measurement_basis`, this
file's context probe on its first run (§ 5, N2), and now this file's own fix for
it. Recorded because the pattern is clearly not learnable by intention alone.

**N6 — the dated H1 could flake the movement pin.** Not run as a mutant (it
needs a midnight boundary), and closed structurally instead: `_sections` drops
the `# Doc-Health Report — <date>` line by name, and the movement test asserts
BOTH reports carried one, so the drop cannot hide a change it was not written
for. Widening `_SECTION` to match the title was rejected: it would also match
`### Requirement: …`, which `test_the_gate_reaches_the_corpus_only_through_the_family`
forbids on purpose.

## 7. Packet § 4's defects, as found

Four things in the packet's § 4 were wrong or unimplementable as written. Each is
recorded as an orchestrator decision in `../plan.md`, flagged for veto.

1. **§ 4.1's figure is stale.** "1 scenario-arm finding, **11** carriage-ledger
   findings" came from a spike at `9be81a40` over **23** MODIFIED blocks. This
   tree carries **22** and reads **9** `info`. Two changes archived in between.
   (D1)
2. **§ 4.2's basis is stale.** It asks that § 2.1's block be asserted "measured
   against `add-family-enumeration-check`'s outcome". That sibling ARCHIVED at
   `f027d3b3` before F1 registered the family; there is no sibling outcome in
   this tree and F1's T052 wrote the block against CANON. The gate asserts the
   basis that exists AND the sibling's absence. (D2)
3. **§ 4.5 contradicts itself.** "+1 warning, +11 info … headline unchanged" —
   the headline is the line those counts are printed on. Implemented as: the
   `error`/`critical` bands do not move, census/inventory/catalog untouched.
4. **F1's own-packet hook does not exist.** F1's `tasks.md`:235 records T057
   (`test_the_family_reads_its_own_packet_s_delta`) as `[x]` and its § Hand-off
   states "the own-packet assertion F3 § 4.2 wants is live". It is not:

   ```text
   $ grep -rn "reads_its_own_packet\|its_own_packet" tests/
   $ echo $?
   1
   ```

   F3 wrote the assertion. **F1 residue finding 6**, after F2's five. (D5)

Also recorded: **§ 4.5's "diffed against the same run on `main`"** was not done
that way, deliberately. The before-state is **this tree with the family
skipped** — no other family's behaviour changed, so skipping this one IS the
pre-registration report, and it is a rendering of the same corpus. Diffing
against another worktree's `main` would compare two different corpora and
attribute the difference to this change.

## 7a. CI shape — the blocker the combined review found, reproduced and closed

**The defect.** The first cut of
`test_the_resolver_fails_on_a_checkout_it_cannot_confirm_and_never_walks_up`
searched `ROOT.parents` for a real checkout carrying `.gitmodules` **and**
`xFactories/`, and asserted one was **found**:

```python
aggregation = next((d for d in ROOT.parents if ...), None)
assert aggregation is not None, "this checkout has no reachable aggregation …"
```

That is an assertion about the **developer's filesystem**. It passes in this
worktree, which sits under the aggregation checkout, and it fails in the
REQUIRED `pytest-suite` check, which runs against a bare
`$GITHUB_WORKSPACE/openxFactory` with no such ancestor. A green branch would have
reddened a required check on `main`.

**The reproduction.** A bare checkout with no aggregation ancestor, built by
`git archive` so no working-tree state leaks in:

```bash
CI=<scratch>/ci-shape/openxFactory
mkdir -p $CI && git archive HEAD | tar -x -C $CI
cd $CI && git init -q . && git add -A && git commit -q -m "CI shape"
python3 -m pytest tests/doc-health/test_modified_block_currency_self_gate.py -q
```

The shape is confirmed rather than assumed — the extracted tree carries
openxFactory's own `.gitmodules` but no `xFactories/`, and **no ancestor of it
carries either**:

```text
$ ls -a $CI | grep -E '^\.gitmodules$|^xFactories$'
.gitmodules
$ d=$(dirname $CI); while [ "$d" != "/" ]; do
      [ -f "$d/.gitmodules" ] || [ -d "$d/xFactories" ] && echo "markers at $d"
      d=$(dirname "$d"); done
        (no output — no aggregation ancestor, which is the pytest-suite shape)
$ git rev-parse --show-toplevel
<scratch>/ci-shape/openxFactory
```

**Before and after, in the same tree**, the pre-fix file taken straight from the
implementation commit:

```text
$ git show 0a15bee7:tests/doc-health/test_modified_block_currency_self_gate.py \
      > $CI/tests/doc-health/test_modified_block_currency_self_gate.py
$ python3 -m pytest …self_gate.py -q
E  AssertionError: this checkout has no reachable aggregation ancestor, so the
   assertion below would be vacuous — if that is now true of the environment,
   say so here rather than deleting the case
E  assert None is not None
FAILED …::test_the_resolver_fails_on_a_checkout_it_cannot_confirm_and_never_walks_up
1 failed, 14 passed in 12.88s          ← exactly what the review measured
```

```text
$ cp <the fixed file> $CI/tests/doc-health/
$ python3 -m pytest …self_gate.py -q
15 passed in 11.86s                     ← the fix, same tree
```

**The fix, and why not a skip.** The repository's standing answer to an
environment-dependent proof is to skip it —
`tests/ideation-dashboard/test_session_harness.py`:251
(`pytest.skip("no aggregation checkout reachable from this tree")`) and
`test_aggregation_register_instance.py`:25-27 (`pytest.mark.skipif(…
GITMODULES.is_file() …)`). Both are right for a proof that NEEDS a real
aggregation tree. This one does not. Its content is *"aggregation markers without
the family markers are refused"*, and a `tmp_path` decoy — `.gitmodules`,
`xFactories/`, `installs/`, and neither of the family's two markers — states
exactly that in every environment, with no skip and no filesystem assumption.
**Removing the dependence beats guarding it**, and it also strengthens the case:
a skip would have meant the assertion never ran in CI at all.

### WHAT THIS HARNESS DOES *NOT* REPRODUCE — stated, because it is not green

Running the WHOLE doc-health suite in this harness reads **4 failed, 1126
passed**. Those four are **artifacts of the harness, not of CI**, and it would be
dishonest to file them either as a pass or as a defect:

```text
FAILED test_ideation_readiness.py::test_derivation_reproduces_the_real_bootstrap_clusters
FAILED test_modified_block_currency_fixtures.py::test_the_reconstructed_fixtures_are_the_history_they_claim[351]
FAILED test_modified_block_currency_fixtures.py::test_the_reconstructed_fixtures_are_the_history_they_claim[329]
FAILED test_readiness_proof_resolution.py::test_the_landed_index_pins_a_revision_this_repository_can_resolve
```

All four read **real git history** — F2's two reconstruct the #351 and #329
instances from the commits that made them, and the two readiness proofs resolve a
pinned `source_revision`. `git archive | git init` deliberately discards history:

```text
$ git rev-list --count HEAD
1
```

Real CI does not. `pytest-suite` checks out at `fetch-depth: 0` (which is why
`test_ideation_readiness.py`'s own truncation branch says "`pytest-suite.yml`
checks out at `fetch-depth: 0`" and treats a shallow clone as a fact about the
CLONE). So the harness reproduces **one** CI property — no aggregation ancestor —
and breaks **another** — full history. That is the right trade for proving B1,
because the self-gate is history-independent by construction: it reads the
working tree and asks `git` only for `rev-parse --show-toplevel`, which one
commit answers. **15 of 15 in the harness is the claim; "the suite is green in CI
shape" is not, and is not made.**

## 7b. THE GATE FELL DUE ON ITS OWN PULL REQUEST — the open question, answered live

The `tasks.md` § OPEN QUESTION FOR BRETT was written as a hypothetical: an exact
set of live corpus triples in a REQUIRED check means "any PR that adds or
archives a lossy MODIFIED block, or edits canon in a way an active block quotes,
reds this gate". **It stopped being hypothetical within hours, on this feature's
own pull request.**

`pytest-suite` on PR #427, run against the merge of `021-…` into a `main` that
had moved:

```text
1 failed, 6985 passed, 20 skipped, 338 deselected, 28 subtests passed in 697.31s
FAILED tests/doc-health/test_modified_block_currency_self_gate.py::test_every_carriage_ledger_finding_over_the_real_tree_is_named
E  assert (not {('qualify-avatar-live-voice', 'repo-boundary-governance',
                 'Neutral avatar-client repository boundary')})
```

**The failure named its own subject and its own remedy**, which is the whole
point of `_moved()`:

```text
subject : the carriage-ledger population (9 named subjects at 76a2ad27)
observed: 1 named subject(s) NO LONGER reported [('qualify-avatar-live-voice',
          'repo-boundary-governance', 'Neutral avatar-client repository boundary')]
WHAT TO DO: re-measure with `python3 scripts/doc-health.py --single-repo .
          --family modified-block-currency` and update the named subjects …
```

**The cause, found by following that instruction rather than by guessing.**
PR #424 (`realize-pin-reachability`) merged to `main` while #427 was open:

```text
$ git log --oneline 76a2ad27..origin/main
175682e2 Merge pull request #424 from opensoft/change/realize-pin-reachability
…
7e4e2f99 The client was extracted three weeks early under another name, so canon
         learns to say openAvatar
```

`7e4e2f99` renamed `xfactory-avatar-client` to `openAvatar` in **both**
`openspec/specs/repo-boundary-governance/spec.md` (canon) and
`openspec/changes/qualify-avatar-live-voice/specs/repo-boundary-governance/spec.md`
(the active delta that quotes it), **in one commit**. That is the correct
authoring move — it is precisely what the carriage arm is advisory about — so the
block now carries all twelve of canon's units and the family correctly reports
nothing for that requirement.

**Verified before deleting the triple, and the verification caught my own error.**
A first ad-hoc probe reported "UNCARRIED: 12", which would have meant the
opposite. `mbc.carried(canon_units, block_units)` returns the **UNCARRIED**
units — the name reads the other way, and F1's own tests
(`test_case_and_trailing_punctuation_are_significant`) settle it: `assert not
mbc.carried(canon, [<a whitespace-variant>])` is the CARRIED case. Read correctly,
the probe says all twelve are carried, and canon's sentence and the block's are
byte-identical. **Nothing was deleted on the strength of a misread probe.**

**What was done.** `git merge origin/main` (no rebase), corpus re-measured, the
named set reduced by one row with the cause and the commit recorded beside it in
the source. Every figure in this file and in `plan.md` § THE FIGURES now carries
both measurements with the tree each was taken at.

**What was NOT done.** The assertion was not loosened, the set was not made a
subset comparison, and the test was not moved to the nightly lane. The open
question for Brett stands exactly as written — this event is evidence for BOTH
sides of it, and it would be dishonest to present it as settling the matter:

- **For keeping it in `pytest-suite`**: the gate worked. It caught a real corpus
  change, named the subject, named the remedy, and the remedy took one merge and
  one line. No human had to reason about doc-health internals.
- **For moving it to the nightly lane**: the failing PR was *this* one, authored
  by someone who knew exactly what the gate was for. The next one will not be.
  An unrelated author seeing "the carriage-ledger population moved" on a branch
  about something else has every incentive to do the one thing this file must not
  survive — loosen it.

Recorded, with the numbers, so Brett rules on evidence rather than on a
hypothetical.

## 8. Scope guard

```bash
git diff --stat $(git merge-base HEAD origin/main) -- scripts/ openspec/ .github/
# (no output)
```

The full change surface:

```text
tests/doc-health/test_modified_block_currency_self_gate.py   (new)
specs/021-modified-block-currency-self-gate/                 (new)
```

`scripts/doc_health/modified_block_currency.py` is **unmodified** (FR-019); no
defect in it was found that would have needed its own task. `report.py`,
`promotion_fidelity.py`, `families.py`, `__init__.py`, every threshold and
`.github/workflows/**` show no diff.
