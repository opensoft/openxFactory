# Speckit F3: the modified-block-currency self-gate — what the family says about THIS repository, by name

Realizes § 4 (4.1–4.5) of `add-modified-block-currency-check`, ratified
2026-08-27 by Brett ("Ratify as-is") on the packet as written at `06c7475a`.
Third of four Speckit features. F1 (`019-…`, `19e3f6b5`) built and registered
the family; F2 (`020-…`, `76a2ad27`) built the regression catalogue; F4 owns
reporting and the workflow boundary and is not started.

**Tests and specs only. No module change.**
`git diff --stat $(git merge-base HEAD origin/main) -- scripts/ openspec/ .github/`
is empty.

## What this adds, and why fixtures were not enough

`tests/doc-health/test_modified_block_currency_self_gate.py` — 15 tests.

Fixtures prove the RULES. Nothing proved the VERDICT. F1's 97 tests and F2's
regression catalogue both assert over synthetic trees; neither says a word about
what the family reports over the corpus the nightly report is computed on. This
feature is that measurement, asserted **by named subject** — which change, which
capability, which requirement, and for the gate-bearing `warning` the omitted
scenario title itself — because the packet's own § 4.1 forbids a bare count.

Three independent guards, and the independence is the design:

1. **The resolver** — the tree measured is the tree the test file lives in,
   confirmed by markers and cross-checked against `git rev-parse --show-toplevel`.
2. **The discovery floor** — the MODIFIED-block population is non-empty,
   asserted in its own test naming no severity, no change and no requirement.
3. **The named subjects** — one `warning` by all four of its fields, nine `info`
   as an exact set, three empty classes by the module's own rule text with a
   positive control on each probe.

Guard 3 alone passes on a clean corpus read by a broken family. Guard 2 alone
passes when every finding is wrong. Guard 1 alone passes on the right tree read
by a broken family.

## The gates

| gate | result |
| --- | --- |
| `pytest tests/doc-health` | **1115 → 1130** (+15) |
| `openspec validate --all --strict` | **76 passed** (24 changes + 52 specs) |
| report movement vs `--skip-family modified-block-currency` | **0 critical, 0 error, +1 warning, +9 info** |
| report lines moved | 24, in 5 hunks, in 3 sections — headline, this family's section, ranked plan |
| everything else in the report | byte-identical |
| F1's, F2's and the enumeration suites | 176 passed, unchanged |
| **CI shape** — bare checkout, no aggregation ancestor | **15 passed** (pre-fix: 1 failed / 14 passed) |

Full commands and numbers: `specs/021-modified-block-currency-self-gate/evidence/self-gate.md`.

## THE PACKET'S § 4 FIGURES WERE STALE — four defects, four decisions

Recorded as orchestrator decisions D1–D5 in `plan.md`, **flagged for veto**. None
is backed by a ruling; reverting any is an edit to this feature.

1. **§ 4.1's count.** It predicted "1 scenario-arm finding, **11**
   carriage-ledger findings" from a spike at `9be81a40` over **23** MODIFIED
   blocks. That tree no longer exists —
   `add-hermes-customer-subject-runtime-contract` and `add-shared-identity-seeds`
   archived since. Re-measured at `76a2ad27` over **22** blocks: **+1 `warning`,
   +9 `info`**. The gate asserts what the tree produces and names the packet's
   numbers in its docstring as history. **(D1)**
2. **§ 4.2's basis.** It asks that § 2.1's block be asserted "measured against
   `add-family-enumeration-check`'s outcome". That sibling ARCHIVED at
   `f027d3b3` (PR #419) before F1 registered the family, so there is no sibling
   outcome in this tree and F1's T052 wrote the block against CANON. The gate
   asserts the basis that exists (`status == "canon"`) **and** the sibling's
   absence, so § 4.2's wording is visibly history rather than silently unmet.
   **(D2)**
3. **§ 4.5 contradicts itself** — "+1 warning, +11 info … headline unchanged",
   where the headline is the line those counts are printed on. Implemented as:
   the `error` and `critical` BANDS do not move (so `--fail-on error` is
   unaffected by construction) and census/inventory/catalog are untouched.
   **(D3)** § 4.5 also says "diffed against the same run on `main`"; the
   before-state used is **this tree with the family skipped**, because no other
   family's behaviour changed and diffing another worktree would compare two
   corpora and blame the difference on this change.
4. **F1's own-packet hook does not exist.** F1's `tasks.md`:235 records T057
   (`test_the_family_reads_its_own_packet_s_delta`) as `[x]` and its § Hand-off
   tells F3 the assertion "is live". It is not — `grep -rn
   "reads_its_own_packet" tests/` returns nothing. F3 wrote the assertion.
   **F1 residue finding 6**, after F2's five, and the only one with a
   behavioural consequence. **(D5)**

**D4** is method: the gate is **not** revision-addressed.
`harden-ideation-readiness-check` reads both sides out of `git archive` because
its subject PINS a revision; this family measures the checkout by contract, and
F1's `test_the_promoted_reader_cannot_reach_a_measurement_basis` asserts
structurally that it has no way to reach a ref. What is mirrored is the resolver
DISCIPLINE — under-test first, named failure, no ancestor walk.

## The combined review found a blocker, and it was a required check going red

**B1.** The first cut of the resolver's negative test searched `ROOT.parents` for
a real checkout carrying `.gitmodules` and `xFactories/` and asserted one was
**found** — an assertion about the developer's filesystem, not about the
resolver. It passes in a worktree under the aggregation checkout and **fails in
`pytest-suite`**, which runs against a bare `$GITHUB_WORKSPACE/openxFactory` with
no such ancestor. A green branch would have reddened a required check on `main`.

Reproduced and closed, both halves measured in the same tree:

```bash
CI=<scratch>/ci-shape/openxFactory
mkdir -p $CI && git archive HEAD | tar -x -C $CI
cd $CI && git init -q . && git add -A && git commit -q -m "CI shape"
python3 -m pytest tests/doc-health/test_modified_block_currency_self_gate.py -q
```

```text
pre-fix file (0a15bee7):  1 failed, 14 passed   ← exactly what the review measured
fixed file:              15 passed
```

The fix is a `tmp_path` **decoy** carrying the aggregation markers and neither of
the family's, so the real content — "aggregation markers without the family
markers are refused" — holds in every environment. The repository's standing
answer to an environment-dependent proof is a skip
(`test_session_harness.py`:251, `test_aggregation_register_instance.py`:25-27),
and both are right for a proof that NEEDS a real aggregation tree; this one does
not, and a skip would have meant the assertion never ran in CI at all. **Removing
the dependence beats guarding it.**

The harness reproduces one CI property (no aggregation ancestor) and breaks
another (full history, `fetch-depth: 0`), so the whole-suite run inside it reads
4 failed — all four are git-history readers and all four are artifacts of
`git archive | git init`, named and explained in `evidence/self-gate.md` § 7a.
**"15 of 15 in the harness" is the claim; "the suite is green in CI shape" is
not, and is not made.**

**Six further findings, all fixed.** Two structural pins had SURVIVED mutants and
now die: the context probe missed `getattr(ctx, "git", None)` (the spelling the
disposition reader itself uses), and `count("load_dispositions(ctx") == 1` proved
one known collaborator is called once rather than that there is one collaborator.
A third pinned PROSE — the allowlist scan ran over raw source while its docstring
said "matched on use" — and **the first fix for it reproduced the same defect in a
comment**. That makes three separate times a probe in this family's suite has been
caught matching a mention; `evidence/self-gate.md` § 6a records all of them,
because the pattern is clearly not learnable by intention alone.

Also closed: a once-a-day flake (the report's dated H1 fell outside `_SECTION`
and was compared verbatim, so two runs straddling midnight would fail the
movement pin), the fact that the documented zero end-state was **unreachable by
the documented mechanism** (the movement pin's two vacuity guards are true at
zero and must be re-aimed in the same commit), and **this change's own archival**
— nearer than the composed-view rename, reds four assertions, previously
unmentioned, now carrying an expected disposition in `quickstart.md` and the F4
hand-off.

## OPEN QUESTION FOR BRETT — the blast radius of a named-subject set in a required check

**Not decided here.** `_LEDGER_SUBJECTS` is an exact set of **nine live corpus
triples** and `pytest-suite` is a REQUIRED check, so any PR that adds a lossy
MODIFIED block, archives one of the twelve changes in the table, or edits canon in
a way an active block quotes **will red this gate** — on a branch whose author may
have nothing to do with doc-health. That is § 4's PR-gate intent working as
written, and it is a cost nobody has priced.

The option, if the cost is judged too high: a marker routing the six
corpus-facing tests to the nightly doc-health lane, keeping the resolver guard,
the discovery floor and the four structural pins in `pytest-suite`. The trade is
explicit — it gives up catching a lossy block *before* it merges. Arguments both
ways are recorded in `tasks.md` § OPEN QUESTION FOR BRETT. **Pending his call the
tests stay in `pytest-suite`**, with `_moved()`'s message as the mitigation.

## The mutation round found the thing worth knowing

**This machine carries fifteen other measurable openxFactory checkouts.** So
"point the resolver at another checkout" is not a hypothetical mutant. Pointed at
`/home/brett/projects/xFactory/openxFactory` — the shared submodule tree, exactly
the tree `harden-ideation-readiness-check`'s ancestor walk always landed on — the
module imports cleanly and **four tests kill it independently**. That tree is a
genuinely different corpus: two warnings instead of one, five ledger subjects
this branch does not have, and `add-family-enumeration-check` still ACTIVE in it.
A gate without the resolver guard would have reported its verdict as this
branch's.

Six mutants, all killed. Two tests also went RED on their own first run, both on
the same mistake in opposite directions — matching a probe on a MENTION rather
than a USE. One was the positive control on the zero-class probes doing exactly
its job. Both are recorded as evidence rather than quietly fixed.

## This gate is EXPECTED to fall due

Its subjects are live corpus content. When `add-composed-view-authoring` declares
its rename with a `Removed from canon by` marker — which the packet's § 6.3
already calls the correct disposition — the `warning` vanishes and
`test_the_scenario_arm_names_the_composed_view_rename_and_nothing_else` fails.
That is designed behaviour. Every corpus assertion's failure message names the
tree, the subject, that corpus movement is the expected cause, the re-measure
command, and the end state:

> if the family now reads ZERO over this tree, that is the DESIRED end state —
> assert zero by this same named-subject mechanism and keep the discovery floor,
> which is then the only assertion distinguishing a clean corpus from a broken
> reader.

`quickstart.md` § WHEN THE GATE FAILS is the runbook. **Do not "fix" a fallen-due
assertion by loosening it.**

## The self-finding is evidence and MUST NOT be dispositioned

The family draws exactly one `info` against this change's own § 2.1 block, naming
canon's two stale numeral sentences (`twenty-one check families`,
`Four of the twenty-one`). The packet predicted it (§ 6.6), F1's O2 recorded that
the self-gate must treat it as evidence, and a disposition would hide the proof
that the family reads its own packet. The gate also asserts that no disposition
CAN apply in the single-repo scope it runs in, so that silence is understood
rather than discovered.

## THIS CHANGE DOES NOT CLOSE #330

Packet § 7.1 requires the PR to say so, and it stays open. Its shape 1 — the
post-archive safety net, diffing a promoted spec against its own prior state
across the archive commit — is not built here (D1 of the packet): it needs a
third measurement basis inside a family whose promoted requirement obliges it to
declare which of TWO it measured. OWNER: the doc-health steward, at the next
family change touching `promotion_fidelity.py`.

Packet § 7.4 also stands: **the domain factories are unmeasured.** This
feature's evidence is openxFactory's own active changes. What the eighteen pinned
domains' active changes will say is unknown, which is why the launch is advisory
and why F4's first instruction is to run the aggregation pass before tuning
anything.

## Analyze pass

Eleven findings, **no CRITICAL**. Five fixed before implementation, six
dispositioned; all eleven in `tasks.md` § Analyze pass. The one worth naming: the
spec's own motivating paragraph claimed a broken `active_blocks` would leave every
fixture test green. It would not — the fixture trees carry `openspec/changes/`,
an `archive/` directory and a `proposal.md` each. An overstatement in a document
about lossy restatement is recorded rather than quietly corrected.

## Still open after this

- **§ 5 (F4)**: the report section rendering, the action line, and the workflow
  boundary pin. `.github/` has no diff on this branch and must not gain one.
- **§ 7.2**: the advisory-to-enforcing flip of the scenario-title arm — `error`
  severity AND the `contested` classification, moved together, never apart. The
  standing population to discharge first is the one `warning` this gate names.
- **§ 8**: the archive act, after this realization merges and is green.
- **The five packet-level orchestrator decisions (its § 1.2)** remain
  not-vetoed rather than affirmatively ruled.

## Issues: `Refs`, not `Closes` — and the citation for that

`Refs #357` · `Refs #329` · `Refs #330`

**The packet does not claim any of the three closes at this feature's landing,**
and I checked rather than assumed:

- **#330 is explicitly held open.** `proposal.md`:311-313 — "It does not claim to
  close #330 in both of that issue's shapes. The pre-archive gate is built and
  the post-archive safety net is not; #330 stays open with an owner." And
  `tasks.md` § 7.1 — "This change MUST NOT be read as closing #330, and its PR
  says so." Said, above and here.
- **#357 and #329 carry no closure claim anywhere in the packet.**
  `proposal.md`:7 names all three under `Origin:` and nothing else in
  `proposal.md` or `tasks.md` says the self-gate's landing discharges either.
  The only `clos*` matches in the packet are #318's origin-gap ruling (:20) and
  the two #330 disclaimers above.
- **And substantively they are not discharged.** #357 asked for a validator; the
  validator exists (F1) and is now measured (F3), but the packet's own § 8.1 makes
  the **archive** a separate later act "once the realization is merged to `main`
  and green" — and F4 (§ 5, reporting) is not built. #329's two lossy blocks are
  **reported, advisory, and standing**: § 7.2 keeps the scenario-title arm at
  `warning` and records that "seven of #351's nine items are reported rather than
  gated until one is taken". An issue about text that is still lost is not closed
  by a check that now mentions it.

So all three are `Refs`. The right place for `Closes #357` / `Closes #329`, if
they are to close at all, is the archive commit that packet § 8.1 describes —
after F4, after the merge, and after § 8.2's byte-for-byte promotion check.
