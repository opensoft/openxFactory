# Archive verification: `add-shared-identity-seeds`

Status: record
Date: 2026-08-27
Verifier: Claude Opus 5 (agent), against a fresh clone at `origin/main`
`42662b70`.

## Method, and what this record does and does not redo

This is the ARCHIVE GATE pass. Unlike `add-model-provider-broker`, which
archived a day earlier and could CITE a finisher's per-task verdict table in
PR #392's body, this packet has no separate finishing pull request to cite:
tasks 1.1–4.4 were discharged inside the single build pull request that landed
the whole surface (#105, 2026-08-07), and 4.5 by a later, one-purpose pull
request (#380, 2026-08-26). There is therefore no prior tick audit to lean on,
so this pass re-derives the ticks rather than asserting them — cheaply, because
there are only eleven and each names a symbol or a file that either exists or
does not.

Read-only against one fresh clone under a scratchpad
(`opensoft/openxFactory` at `42662b70`), plus a second pristine clone of the
same commit used only as the doc-health baseline. No file in any working
checkout was read or written.

## Archive gate

The proposal declares:

```
code_surface: openxFactory (doc_health.shared_identity detector + deterministic
              seed drafter; dashboard serve drafting route; the repository
              lens's seed affordance and panel; tests)
target_release: none
```

**The gate keys on the CODE SURFACE, not on the target.** `release-realization`'s
*Realization archive gate* opens "A change with a **non-empty code surface**
SHALL NOT archive until realization evidence exists" — the antecedent is the
surface. `target_release` is a separate field, declared by *Realization axis
declaration*, and the archive-on-landing path there is keyed to
`code_surface: none`, which this is not. So `target_release: none` cannot
downgrade a real surface to a doc-only archive. This is the ruling
`add-model-provider-broker`'s archive recorded on 2026-08-27 and this record
applies rather than re-litigates; that record also counted this packet among
the five active changes spelling `target_release: none` outside the field's
declared vocabulary, and the same authoring nit is carried here without repair,
for the same reason: it is a corpus-wide habit, and history is left as written.

### (a) MERGED ON THE IMPLEMENTED TARGET — yes

PR #105, "Shared-identity seeds: the DTN register's first candidate rule,
computed", merged to `main` 2026-08-07T16:51:28Z as `82e3ec4e`, from branch
head `8a028c21`. The whole surface landed in ONE commit — this change has no
follow-up build commits at all — and both are ancestors of `origin/main`
`42662b70`, tested rather than assumed (`git merge-base --is-ancestor`):

| Commit | Subject | Ancestor of main |
|---|---|---|
| `8a028c21` | Shared-identity seeds: the DTN register's first candidate rule, computed | yes |
| `82e3ec4e` | merge commit of PR #105 | yes |
| `73a535d9` | merge commit of PR #380 (task 4.5, DTN-025 admitted) | yes |

Each declared surface element resolves to a file present at main `42662b70`,
opened rather than grepped, and each ticked task re-derived against it:

| Surface element | Path at main | Lines | Discharges |
|---|---|---|---|
| the detector + drafter | `scripts/doc_health/shared_identity.py` | 207 | 1.1, 1.2, 1.3 |
| the loopback drafting route | `scripts/ideation_dashboard/serve.py` (`_handle_dtn_seed`, `ACTIONS_DTN_SEED_ROUTE`) | 6740 | 2.1 |
| the lens affordance + panel | `scripts/ideation_dashboard/web/views/lens.js` (`DTN_SEED_ROUTE`, the "draft seed" button, the read-only seed panel) | 1524 | 3.1, 3.2 |
| the panel's styles | `scripts/ideation_dashboard/web/styles.css` (`.seedtext`) | — | 3.2 |
| behavioural tests | `tests/ideation-dashboard/test_shared_identity.py` | 175 | 4.1, 4.2, 4.3 |

Five of five. The ticks were re-derived, not taken on trust:

- **1.1** `shared_identities(documents, *, repositories=None, minimum=…,
  exactly=…)` exists at line 84 with exactly the declared keywords.
- **1.2** `draft_seed(register_text, rows, *, project, as_of)` at line 158,
  with `next_dtn_id` at 133 supplying the register-derived numbering and
  `CANDIDATE_RULE` at 42 the quoted rule.
- **1.3** `si.REGISTER_PATH` (line 50) and `families.REGISTER_PATH` (line 680)
  are the same string, and `test_the_register_path_matches_the_family_constant`
  pins them equal — the mirror is enforced, not merely intended.
- **2.1** `_handle_dtn_seed` refuses non-loopback with `403 loopback_only`,
  refuses an absent project with `400`, refuses a non-composable project with
  `404 unknown_project`, and opens the register with `read_text` only. There is
  no write path in the handler.
- **3.1/3.2** `lens.js` attaches "draft seed" to convergent drill-in rows and
  states its refusal on single-carrier ones; the drafted seed renders in a
  read-only `<pre class="seedtext">` under the heading "drafted register seed
  … — nothing is written", with the merge destination named.
- **4.1–4.3** seven tests, covering subset scoping, exact-combination
  narrowing, register-format numbering with and without a register, and two
  wire tests including the byte-for-byte unchanged-checkout assertion.
- **4.4** the live browser check of 2026-08-07 is recorded in the task's own
  body with its counts (three convergent regions enabled, five single-carrier
  rows disabled with their reason, the 3-carrier sector drafting DTN-025,
  zero console errors / page errors / >=400 responses). It is a point-in-time
  human observation, not a standing check, and is left as the task states it.
- **4.5** discharged by PR #380 (`73a535d9`, merged 2026-08-26T15:44:24Z), and
  verified in the artifact rather than in the commit message: the register at
  main carries `| DTN-025 | Shared across 3 factories: docs/credentialing.md |`
  in the Candidate List and `### DTN-025:` in Candidate Details.

Nothing on the surface has decayed since it landed:
`scripts/doc_health/shared_identity.py` is at blob `428e7a7e` and
`tests/ideation-dashboard/test_shared_identity.py` at blob `2d70f9e2` at every
green main tree named below, identical to the tree PR #105 produced.
`lens.js` and `serve.py` are both much larger at main than #105 left them,
because later dashboard lanes extended the same two modules; this change's
contributions are intact beneath them, checked by symbol rather than by size.

### (b) GREEN RUN OF THE RUNNABLE SURFACE — yes, and the honest shape of it

**PR #105 carries no check runs, and that is a fact about the repository, not
about this change.** The GitHub check-runs API returns an empty list for
`8a028c21`. The reason is dated: `.github/workflows/pytest-suite.yml` — this
repository's only trigger that runs pytest at all — first landed 2026-08-24 as
`74af6cc4` (issue #292, PR #304), SEVENTEEN DAYS after this surface merged. Its
own header says so: "Until this workflow, NO trigger in this repository ran
pytest at all". So the green evidence for this packet cannot come from its own
pull request and this record does not pretend otherwise; it comes from MAIN,
where the gate has run over this code from the moment the gate existed.

**On main.** Every uncancelled green `pytest-suite` run on `main`, first to
last, carries this surface:

| Run | Head sha | Conclusion | When | Detector | Route/affordance | Test file |
|---|---|---|---|---|---|---|
| `32802536347` | `cbf2368d` | success | 2026-08-25T02:44:19Z | present | present | present |
| `33023028983` | `bb7d7ae8` | success | 2026-08-26T23:21:15Z | present | present | present |
| `33031366342` | `d3e140ea` | success | 2026-08-27T01:50:11Z | present | present | present |
| `33055215377` | `891d1981` | success | 2026-08-27T08:42:24Z | present | present | present |
| **`33062355435`** | **`42662b70`** | **success** | **2026-08-27T10:17:02Z** | present | present | present |

`cbf2368d` is the FIRST green main run the workflow ever produced (the run on
its own landing commit `74af6cc4` was cancelled), and `8a028c21` is an ancestor
of it — so there has been no window in which the gate existed and this code sat
outside it.

**The last uncancelled green main run is `33062355435`, head `42662b70`,
conclusion `success`, single job `pytest-suite` green, completed
2026-08-27T10:31:25Z.** That head sha IS this branch's base commit, so the run
covers exactly the tree this archive is cut from — the strongest form the
"last green main run" claim can take, rather than a descendant argument.

**The cancellation artifact, named rather than papered over.**
`pytest-suite.yml` declares `concurrency: group: pytest-suite-${{ github.ref }}`
with `cancel-in-progress: true`, so a main that advances faster than a ~12–17
minute suite cancels its own predecessors. `4be330a3` (run `33062331587`),
`8e9c0756`, `7b7447da`, `78ffb7f1` and `f9457d6f` are all `cancelled` for
exactly that reason. A `cancelled` run is not a red run, and no run in this
window reported a test failure.

**Coverage is not incidental.** The workflow carries NO paths filter — its
header explains why ("a paths filter on a check that is later marked REQUIRED
deadlocks") — and its final step is `python3 -m pytest tests/ -q -m "not
postgres"`. So `tests/ideation-dashboard/test_shared_identity.py` is inside
every green run named above rather than potentially filtered out of one.

**PR #380's own checks are thin, and it does not matter.** Its head
`defd9b6c` carries one check run, `wallet-validation`, `cancelled`; no
`pytest-suite` ran on it. #380 changed three files —
`docs/domain-neutralization-candidate-register.md`, `README.md`, and this
change's `tasks.md` — and touched no code, so the code-surface gate does not
rest on it. It is cited above as the ACT that discharged 4.5, and the artifact
it produced was verified directly in the register at main.

**Direct run in this fresh clone at main**, so the gate does not rest on CI
alone:

```
python3 -m pytest tests/ideation-dashboard/test_shared_identity.py -q
7 passed in 2.33s   (exit 0)

python3 -m pytest tests/ideation-dashboard/test_shared_identity.py \
                 tests/ideation-dashboard/test_lens.py -q
32 passed, 1 skipped in 5.71s   (exit 0)
```

`test_lens.py` is run alongside because tasks 3.1/3.2 put this change's
affordance into the lens's drill-in pane; the one skip is
`test_lens.py:481`, "pinned openxFactory validator(s) not reachable" — a
pre-existing environment guard in the lens suite, not in this change's tests. `openspec validate --all
--strict` was green in the same clone at 76/76 before the archive and 75/75
after (one fewer item because the change moved out of the active set).

### Standing archive-gate clauses

- **Managed subject.** No realization deploys onto a registered managed subject
  of another factory, so the correlation-identifier clause of *Realization
  archive gate* does not apply.
- **Origin retention.** `.openspec.yaml` carries its `ad_hoc` origin exactly as
  the 2026-08-25 sweep created it — id
  `openxFactory:adhoc:2026-08-07-add-shared-identity-seeds`, `approved_by`
  quoting this packet's own `Ratified by:` header verbatim, `approved_on:
  2026-08-07`. Unmutated at blob `afd0e600`, and **still at `afd0e600` after
  the archive** — see "The dotfile, checked because it has been lost before".
- **Proposal support gate.** This change has no `supporting-docs/` folder and
  no `research/` folder, so the support-bundle clause has nothing to bundle,
  and the archive used the bare CLI rather than the `proposal-support.py`
  wrapper — the same shape `add-roster-device-admission-surface` and
  `refine-demote-round-trip-mechanics` used, whose predicate is the PRESENCE
  OF SUPPORTING DOCUMENTS rather than the origin kind.
- **Task state.** 11 of 12 boxes ticked. The twelfth is §5's successor box and
  is unticked deliberately — see the next section — so the archive was taken
  with `--yes`, and the CLI reported `Task status: 11/12 tasks` on the way
  through. This is a recorded boundary, not an incomplete change.

**GATE MET.** The change archives.

## The unticked box: 5.1, and why it stays unticked

`tasks.md` §5 is headed "Successor (not this change)" and holds one box:
promoting the detector to a fifth neutrality-drift stage-1 signal so the
nightly lane files these seeds unattended.

The precedent followed is `add-roster-device-admission-surface` (archived
2026-08-22), whose §6 box for the OpsxFactory side archived UNTICKED with a
closing note, itself following `refine-demote-round-trip-mechanics`'s §8 by
ruling: "an unticked box here means 'owned elsewhere', and ticking it would
claim work this repository never did." That is the disposition applied here.
The box gained a closing note on this archive; the tick was NOT applied.

**The successor is named rather than gestured at, and its unbuilt state was
measured.** The successor is a fifth entry in
`scripts/doc_health/neutrality.py`'s `SIGNAL_NAMES`, which at `42662b70` reads
exactly `("near_duplicate", "lexicon_absence", "cross_repo_consumer",
"uninventoried_tooling")` — four names — so `shared_identity` is not among the
lane's signals and `neutrality_dispatch.py`'s nightly prepare/merge path does
not file these seeds. No active change proposes it and no staging topic
declares it as an exit. The proposal's Impact section already says why the
order is deliberate: "This change deliberately ships the human-driven path
first, because the lens is where the question is already being asked."

## Requirement-map diff (thin-delta check)

The delta at `specs/ideation-dashboard/spec.md` carries **`## ADDED
Requirements` only** — no `MODIFIED`, no `REMOVED`, no `RENAMED`, and exactly
one requirement. The thin-delta hazard this check exists for (archive replaces
a MODIFIED requirement's block WHOLESALE, so a delta that restates the title
but not the full promoted scenario set silently deletes scenarios) therefore
has **no surface in this change**. Verified by structure first, then by
comparing SCENARIO SETS rather than titles.

**No canon repair was needed, and that conclusion was measured rather than
assumed.** Promoted `ideation-dashboard` HAS moved a long way since this delta
was written on 2026-08-07 — it stood at 95 requirements when
`add-model-provider-broker` archived on 2026-08-27 and at 99 when this pass
began — but a delta that MODIFIES nothing cannot go stale against a moving
canon. The one ADDED title was tested for collision against all 99 promoted
requirement titles: **0 collisions**, so it promotes as a genuinely new block
and no promoted body is replaced. The nearest-neighbour titles were read, not
just diffed — `Drill-in scopes the dashboard to a region's documents`,
`The lens serves a repository vocabulary`, `Workbench creation affordances and
seeding` — and none of them governs the drafting act this requirement
introduces.

| Capability | Requirements before | Requirements after | Scenarios before | Scenarios after |
|---|---|---|---|---|
| `ideation-dashboard` | 99 | 100 | 453 | 457 |

The added requirement and its scenarios:

- Convergent lens regions draft candidate-register seeds — 4 scenarios
  (a convergent region drafts a seed; a seed covers exactly its region; a
  single-carrier region cannot be drafted; a plane that cannot compose has no
  candidates)

The table above is the MEASURED after-state, not a prediction: all 99
pre-existing requirement bodies were sha256-hashed before the archive and
re-hashed after. **99/99 unchanged, byte for byte**, 0 titles missing, 1 title
new, and their 453 scenarios carry forward intact. `openspec archive` reported
`+ 1 added, ~ 0, - 0, → 0` on `ideation-dashboard`, which agrees.

### The adjacent promoted block, checked because it is the one at risk

The requirement a careless reading would expect this change to MODIFY is
canon's `Composed views are read-only with a repository jump` (D10) — because
this change puts a NEW AFFORDANCE onto a composed, read-only view, which is
precisely what that block exists to forbid. It is NOT modified, and that is
correct rather than an omission. Canon's rule is scoped to gate-bearing
affordances: "On a composed snapshot every gate-bearing affordance SHALL hide
— a gate verb binds to one served checkout, and a composed view has none". The
drafting affordance is not gate-bearing: it writes nothing, opens the register
read-only, and claims no gate capability, and the added requirement states that
predicate explicitly ("because nothing is written, the affordance SHALL remain
available on a composed read-only view and SHALL NOT claim a gate capability").
The two blocks are compatible on their own terms, so nothing is restated and
nothing contradicts. The route's code agrees with the spec: `_handle_dtn_seed`
gates on `self.loopback`, never on the gate capability.

### Archive-order fact, recorded per the amendment precedent

`add-doxchat-model-intake`'s `tasks.md` records the rule that when two active
changes touch the same requirement block, whichever archives LAST must already
carry the other's text. That rule was tested here rather than presumed
inapplicable. Five OTHER active changes carry an `ideation-dashboard` delta
after this archive; three of them contain `## MODIFIED Requirements`:

| Active change | MODIFIED block | Overlaps this change's ADDED requirement |
|---|---|---|
| `add-doxchat-model-intake` | `doxBench model catalog and provider boundary` | no |
| `add-nightly-dashboard-refresh` | `Runtime snapshot fetch with baked fallback and displayed freshness` | no |
| `add-composed-view-authoring` | `Composed views are read-only with a repository jump` | no |

**All three archives commute with this one.** Because this change modifies
nothing, archiving it first cannot invalidate any of the three restatements:
each still faces the same promoted bytes it faced before, all 99 of which are
provably unchanged. The near neighbour is `add-composed-view-authoring`, which
restates the very D10 block discussed above and grows it from canon's 2
scenarios to 6 (renaming `Gate verbs hide on a composed view` to `Tile-bound
gate verbs hide on a composed view` and adding four). Whether that restatement
is a correct thick delta is that packet's business, not this one's; what
matters for ORDER is that it is unaffected by this archive, and no amendment is
owed in either direction.

## The dotfile, checked because it has been lost before

There is a known defect in which `openspec archive` DELETES a change's
`.openspec.yaml` rather than moving it into the archived folder — which, under
*Origin retention at archive*, would destroy exactly the provenance that
requirement exists to preserve. So it was checked rather than trusted, and on
this run **it did not bite**:
`openspec/changes/archive/2026-08-27-add-shared-identity-seeds/.openspec.yaml`
exists and `git hash-object` returns
`afd0e6003a0f200f3452bb8beaf34aa8c5523b23` — byte-identical to the blob at the
pre-archive `HEAD`. The file was MOVED, not recreated, and no restoration by
blob id was needed. CLI: `openspec` 1.2.0 (the version `pytest-suite.yml` pins
for CI), the same version that moved `add-model-provider-broker`'s dotfile
correctly a day earlier. A future archiver should still check; this record says
only that this run was clean.

## MINOR findings — recorded, none blocking

1. **`target_release: none` is outside the field's declared vocabulary**, as
   set out in the gate section. Corpus-wide habit — this packet is one of the
   five `add-model-provider-broker`'s archive record counted — and not repaired
   in history.
2. **The declared surface says `doc_health`, the tests live under
   `tests/ideation-dashboard/`.** The detector module is
   `scripts/doc_health/shared_identity.py`, but its only test file is
   `tests/ideation-dashboard/test_shared_identity.py`, not
   `tests/doc-health/`. The placement follows the CONSUMER (the dashboard route
   and lens the tests actually drive through the wire) rather than the module's
   package, and both directories are inside `pytest tests/`, so nothing is
   unrun. It is named here because a reader looking for this change's tests
   under `tests/doc-health/` will not find them.
3. **The green evidence for this packet is main-only, by dates rather than by
   choice.** PR #105 has zero check runs because it predates
   `pytest-suite.yml` by seventeen days. Stated plainly above so a future
   reader asking "was this change's own PR green?" gets the honest answer —
   "there was nothing to be green" — rather than re-deriving it from an empty
   API response.
4. **Task 4.4's live browser check is point-in-time.** It was performed once,
   2026-08-07, against the real five-factory `domains` project, and no standing
   check re-drives the browser. The wire tests DO stand, including the
   unchanged-checkout assertion; what does not stand is the rendered-affordance
   observation.
