# Archive verification: `add-model-provider-broker`

Status: record
Date: 2026-08-27
Verifier: Claude Opus 5 (agent), read-only against a fresh clone at
`origin/main` `7b7447da`.

## Method, and what this record deliberately does NOT redo

This is the ARCHIVE GATE pass, not a second tick audit. Every one of the
fifteen ticked boxes in `tasks.md` was already re-verified by PR #392's
finisher against the code and the test that discharges each, and that
verification is written down in the pull request body rather than asserted
here: the eleven build tasks `1.1`–`3.3` carry a per-task verdict table
("The tick audit"), `0.1`/`0.2`/`0.3` are discharged in "Ratification and
the 0.3 ruling, recorded", and `2.6` in "Reconciliation + review responses".
That sweep found and finished exactly one gap (1.2's four CLI verbs were
covered only through the store, not through the real parser) and unticked
nothing. Re-deriving it would add no evidence, so this record CITES it:
<https://github.com/opensoft/openxFactory/pull/392>.

What this pass owes instead, and does: the realization archive gate on its
own terms, and the requirement-map diff against promoted canon as it stands
TODAY rather than as it stood when the delta was written.

Read-only against one fresh clone under a scratchpad
(`opensoft/openxFactory` at `7b7447da`), plus a second pristine clone of the
same commit used only as the doc-health baseline. No file in any working
checkout was read or written.

## Archive gate

The proposal declares:

```
code_surface: openxFactory (dashboard settings surface for model-provider
              bindings; a token-minting broker seam that shells out to
              openProfiler; ONE server-side provider client behind it; the
              honest unavailable posture; the narrowed structural provider
              boundary; tests). openProfiler itself is OUT of scope and unbuilt.
target_release: none
```

(The quoted front-matter is reproduced verbatim as a record; its "unbuilt"
is the proposal's authoring-time fact of 2026-08-08. openProfiler's broker
surface merged 2026-08-26 as that repository's PR #18, which is the very
evidence this record verifies below.)

**The gate keys on the CODE SURFACE, not on the target.** `release-realization`'s
*Realization archive gate* opens "A change with a **non-empty code surface**
SHALL NOT archive until realization evidence exists" — the antecedent is the
surface. `target_release` is a separate field, declared by *Realization axis
declaration*, and the archive-on-landing path there is keyed to
`code_surface: none`, which this is not. So `target_release: none` cannot
downgrade a real surface to a doc-only archive, and the prior verifier's
ruling to that effect is confirmed rather than re-litigated.

**Authoring nit, recorded and NOT fixed.** `none` is not in the declared
vocabulary for that field: *Realization axis declaration* admits
`target_release:` of `implemented` (the affected repositories' main lines)
"or a named release defined in the aggregation repository", and offers no
third value. The intended reading is legible from the proposal's own Impact
section — "Depends on **openProfiler**, unbuilt … everything here is inert
until a binding names a working broker" — i.e. no aggregation release is
allocated to it.

It is a corpus-wide authoring habit rather than this packet's slip, counted
rather than asserted: of the 26 other active changes, **five** carry `none`
in the same field (`add-shared-identity-seeds`,
`add-composed-view-authoring`, `add-lens-document-selection`,
`add-substantive-review-lane`, `add-notebook-hosting-credential-custody` —
the last two glossing it as "no contract-bundle involvement"), and a further
set spells the field `implementation_pending`, `repository-bootstrap`, or
"next additive contract bundle", none of which is in the vocabulary either.
The field is in practice being read as "which contract bundle does this
cut?", for which `none` is the honest answer. Whether the vocabulary should
be widened to match that reading is a separate act; it is named here so a
reader does not mistake this packet's spelling for a ruling, and history is
left as written.

### (a) MERGED ON THE IMPLEMENTED TARGET — yes

PR #392, "The broker mints and doxBench calls, so the provider boundary
narrows to one module", merged to `main` 2026-08-26T23:21:12Z as
`bb7d7ae8`. Every commit on that branch is an ancestor of `origin/main`,
tested rather than assumed (`git merge-base --is-ancestor`):

| Commit | Subject (head) | Ancestor of main |
|---|---|---|
| `c172d865` | The broker mints and doxBench calls, so the provider boundary narrows… | yes |
| `449a0649` | openProfiler declared its surface, so the seam speaks its subcommands… | yes |
| `02815866` | Take the review's two prose notes… | yes |
| `91e3a0e9` | Merge `origin/main` into `change/model-provider-broker-build` | yes |
| `0c131981` | Take the review's three code notes… | yes |
| `bb7d7ae8` | merge commit of PR #392 | yes |

The follow-ups landed INSIDE #392's branch rather than as separate pull
requests, which is why the branch carries five commits and the change has
one merge.

Each declared surface element resolves to a file present at main `7b7447da`,
opened rather than grepped:

| Surface element | Path at main | Lines |
|---|---|---|
| binding record + store (settings surface) | `scripts/ideation_dashboard/doxbench_binding.py` | 557 |
| minting seam / broker invocation | `scripts/ideation_dashboard/doxbench_install.py` | 339 |
| the ONE provider client | `scripts/ideation_dashboard/doxbench_provider.py` | 906 |
| `model-binding` CLI verb group | `scripts/ideation_dashboard/cli.py` | 2328 |
| `model_port_factory` wiring | `scripts/ideation_dashboard/serve.py` | 6734 |
| behavioural tests | `tests/ideation-dashboard/test_model_provider_broker.py` | 1325 |
| real-binary e2e | `tests/ideation-dashboard/test_openprofiler_broker_e2e.py` | 408 |
| the NARROWED structural boundary test | `tests/ideation-dashboard/test_provider_boundary.py` | 274 |

Eight of eight. `doxbench_install.py` is larger at main (339) than PR #392
left it (150) because the `add-doxchat-model-intake` lane extended the same
module afterwards; the broker's own contribution is intact beneath it.

### (b) GREEN RUN OF THE RUNNABLE SURFACE — yes

**On the pull requests.** Both required checks reported SUCCESS at each head
sha, read from the status-check rollup rather than from a merge button:

| PR | Head sha | `pytest-suite` | `wallet-validation` |
|---|---|---|---|
| #392 (this change) | `0c131981` | SUCCESS — run `33022209136`, 2026-08-26T23:20:44Z | SUCCESS — run `33022209188`, 23:09:28Z |
| #401 (the consumer, contract-v1.45) | `7eee092d` | SUCCESS — run `33029559727`, 2026-08-27T01:29:51Z | SUCCESS — run `33029559670`, 01:16:37Z |

PR #401 matters as corroboration rather than duplication: it exercises the
same three broker modules AND the intake built on top of them, so a
regression in the broker seam would have surfaced there a second time.

**On main itself, which is the claim the gate actually wants.** The merge
commit of PR #392 has its own uncancelled, green push-triggered run:
`pytest-suite` run **`33023028983`, `bb7d7ae8`, conclusion `success`**,
2026-08-26T23:21:15Z, single job `pytest-suite` green. That is the broker
code green ON THE IMPLEMENTED TARGET, not merely on a branch.

**The last uncancelled green main run**, assessed the way the
`add-omnigent-domain-terminology` archiver assessed it — by naming the run
and testing whether it carries the code — is `pytest-suite` run
**`33031366342`, `d3e140ea`, `success`**, 2026-08-27T01:50:11Z (the merge of
PR #398, a runbook-pointer fix). It DOES include the broker code: `bb7d7ae8`
is an ancestor of `d3e140ea`, and all three broker modules and all three
broker test files resolve at that tree. `d3e140ea` is itself an ancestor of
this branch's base `7b7447da`.

**The cancellation artifact, named rather than papered over.**
`.github/workflows/pytest-suite.yml` declares
`concurrency: group: pytest-suite-${{ github.ref }}` with
`cancel-in-progress: true`, so a main that advances faster than a ~12–17
minute suite cancels its own predecessors. Between `d3e140ea` and current
main HEAD, `78ffb7f1` and `f9457d6f` are both `cancelled` for exactly that
reason, and the run on `7b7447da` (`33035345420`) was `in_progress` at the
moment of this verification. A `cancelled` run is not a red run, and none of
the runs in this window reported a test failure.

**Coverage is not incidental.** That workflow carries NO paths filter — its
header states why — and its final step is
`python3 -m pytest tests/ -q -m "not postgres"`. So `tests/ideation-dashboard/`,
including all three broker test files, is inside every one of the green runs
named above rather than potentially filtered out of them.

**Direct run in this fresh clone at main**, so the gate does not rest on CI
alone:

```
python3 -m pytest tests/ideation-dashboard/test_model_provider_broker.py \
                 tests/ideation-dashboard/test_provider_boundary.py \
                 tests/ideation-dashboard/test_openprofiler_broker_e2e.py -q
99 passed, 3 skipped in 4.26s   (exit 0)
```

`openspec validate --all --strict` is green in the same clone at 77/77.

**The three skips are stated, not hidden.** All three are in
`test_openprofiler_broker_e2e.py` and are self-skipping guards: the real
`openprofiler-broker` binary is not on PATH and `OPENPROFILER_BROKER_BIN`
names no executable. They skip the same way on the GitHub runner. So the
green evidence above covers the seam's BEHAVIOUR against a fake broker that
speaks the declared contract, and does NOT re-cover the one thing those three
tests exist for — whether openProfiler's declaration and its program agree.
That agreement was measured once, in task 2.6's build session, against the
real binary built from openProfiler `d0538c31`; it is a point-in-time
measurement, not a standing check, and this record says so rather than
letting a green CI badge imply otherwise. It does not block the gate: the
declared surface here is this repository's, and this repository's surface ran
green.

### Standing archive-gate clauses

- **Managed subject.** No realization deploys onto a registered managed
  subject of another factory, so the correlation-identifier clause of
  *Realization archive gate* does not apply.
- **Origin retention.** `.openspec.yaml` carries its `ad_hoc` origin exactly
  as created — id `openxFactory:adhoc:2026-08-08-add-model-provider-broker`,
  the reason recording why the packet's own `Ruling:` header was READ AND
  REJECTED as admission provenance, `approved_by` (Brett, 2026-08-25,
  verbatim "admit the three remaining packets") and `approved_on:
  2026-08-25`. Unmutated at blob `e5fe1dd6`, and **still at `e5fe1dd6` after
  the archive** — see "The dotfile, checked because it has been lost before".
- **Proposal support gate.** This change has no `supporting-docs/` folder and
  no `research/` folder, so the support-bundle clause has nothing to bundle.
- **Task state.** 15 of 15 boxes ticked, 0 unticked — checked mechanically,
  because `openspec archive` refuses an unticked list.

**GATE MET.** The change archives.

## Requirement-map diff (thin-delta check)

The delta at `specs/ideation-dashboard/spec.md` carries **`## ADDED
Requirements` only** — no `MODIFIED`, no `REMOVED`, no `RENAMED`. The
thin-delta hazard this check exists for (archive replaces a MODIFIED
requirement's block WHOLESALE, so a delta that restates the title but not the
full promoted scenario set silently deletes scenarios) therefore has **no
surface in this change**. Verified by structure first, then by content, and
then by the only test that actually matters — comparing SCENARIO SETS rather
than titles.

**No canon repair was needed, and that conclusion was measured rather than
assumed.** Promoted `ideation-dashboard` HAS moved since this delta was
written — `add-doxbench-distilled-abstract` and the earlier doxBench editing
phases all landed requirements into it — but a delta that MODIFIES nothing
cannot go stale against a moving canon. Each of the four ADDED titles was
tested for collision against all 95 promoted requirement titles: **0
collisions**, so all four promote as genuinely new blocks and no promoted
body is replaced.

| Capability | Requirements before | Requirements after | Scenarios before | Scenarios after |
|---|---|---|---|---|
| `ideation-dashboard` | 95 | 99 | 444 | 453 |

The four added requirements and their scenario counts:

- Model capability is reached with a broker-minted token — 2 scenarios
- The provider boundary narrows to one module rather than disappearing — 2
- The dashboard holds bindings, and a minted token outlives nothing — 3
- A broker or provider that cannot answer refuses honestly — 2

The table above is the MEASURED after-state, not a prediction: all 95
pre-existing requirement bodies were sha256-hashed before the archive and
re-hashed after. **95/95 unchanged, byte for byte**, 0 titles missing, 4
titles new, and their 444 scenarios carry forward intact. `openspec archive`
reported `+ 4 added, ~ 0, - 0, → 0` on `ideation-dashboard`, which agrees.

## The dotfile, checked because it has been lost before

There is a known defect in which `openspec archive` DELETES a change's
`.openspec.yaml` rather than moving it into the archived folder — which, under
*Origin retention at archive*, would destroy exactly the provenance that
requirement exists to preserve. So it was checked rather than trusted, and on
this run **it did not bite**:
`openspec/changes/archive/2026-08-27-add-model-provider-broker/.openspec.yaml`
exists and `git hash-object` returns `e5fe1dd697e18e51af040494f7b4cc58a6c31b75`
— byte-identical to the blob at the pre-archive `HEAD`, confirmed by a `diff`
against `git show HEAD:…/.openspec.yaml` returning empty. The file was MOVED,
not recreated, and no restoration by blob id was needed. CLI: `openspec`
1.2.0 (the version `pytest-suite.yml` pins for CI). A future archiver should
still check; this record says only that this run was clean.

### The adjacent promoted block, checked because it is the one at risk

The requirement a careless reading would expect this change to MODIFY is
canon's `doxBench model catalog and provider boundary`, since the proposal's
most consequential line moves a provider boundary. It is NOT modified, and
that is correct rather than an omission: canon's block governs the CATALOG
and the browser ("the browser MUST NOT call any model provider directly",
"an adapter that reaches a hosted provider SHALL obtain its credential
through the ratified broker lane and MUST NOT hold or read a raw secret of
its own"). That broker-lane clause was promoted by
`add-doxbench-editing-phase-b` (`02a71d6e`) — canon ANTICIPATED this lane —
and the four added requirements narrow a SOURCE-STRUCTURAL invariant that
lives in the test suite, not in that promoted block. The two are compatible,
not competing, so nothing is restated and nothing contradicts.

### Archive-order fact, recorded per the amendment precedent

`add-doxchat-model-intake`'s `tasks.md` records the rule that when two active
changes touch the same requirement block, whichever archives LAST must
already carry the other's text. That rule was tested here rather than
presumed inapplicable. Seven active changes carry an `ideation-dashboard`
delta; three of them contain `## MODIFIED Requirements`:

| Active change | MODIFIED block | Overlaps this change's ADDED set |
|---|---|---|
| `add-doxchat-model-intake` | `doxBench model catalog and provider boundary` | no |
| `add-nightly-dashboard-refresh` | `Runtime snapshot fetch with baked fallback and displayed freshness` | no |
| `add-composed-view-authoring` | `Composed views are read-only with a repository jump` | no |

**The two archives commute.** `add-doxchat-model-intake` is the near
neighbour — its own four ADDED titles are disjoint from these four, and its
MODIFIED restatement of `doxBench model catalog and provider boundary`
currently reproduces canon's **11 scenarios with none dropped and one added**
(12), which is a correct thick delta against canon as it stands. Because this
change modifies nothing, archiving it first leaves that restatement valid
byte-for-byte, and no amendment is owed in either direction. The ordering
constraint the precedent guards against simply does not arise between these
two packets.

## MINOR findings — recorded, none blocking

1. **`target_release: none` is outside the declared vocabulary**, as set out
   in the gate section above. Corpus-wide habit; not repaired in history.
2. **One path citation to this change survives the move.**
   `specs/017-openxwallet-carve/evidence/operator-log.md` names
   `openspec/changes/add-model-provider-broker/` in a dated operator log
   describing what six commits touched at the time. It is a `record`-class
   evidence file about a past moment, so the path is correct as history and
   is deliberately left alone; the only live citation, README's active-changes
   row, moves with this archive.
3. **The real-binary e2e coverage is point-in-time, not standing** — see the
   three skips above. Naming it here means a future reader asking "did CI ever
   drive the real broker?" gets the honest answer without re-deriving it.
