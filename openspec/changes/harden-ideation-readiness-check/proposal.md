---
code_surface: openxFactory (`tests/doc-health/test_ideation_readiness.py` — the `_openxfactory_root()` ancestor walk at `:28`, the index read at `:389-390`, the `git archive` read point and its skip branch at `:393-398`, and three further call sites of the same helper at `:556`, `:568`, `:934`; `tests/doc-health/test_derive_possibles.py:29` and `tests/doc-health/test_readiness_dispatch.py:318` — the same helper spelled twice more, which must move with it or the hazard survives in two places; `scripts/doc_health/ideation_readiness.py` — `find_index_validator()` at `:682-692`, whose identical walk resolves the pinned validator out of a foreign checkout, and the resolution helper the module already carries at `:1067-1077` for the renderer, which is the shape the other two should take. NO change to `derive_clusters`, the prompt contract, the evidence contract, the gate constants, the boundary allowlist, the readiness lane's severity or disposition, the index schema, or the generator.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` moves, no digest set changes, and no release tag is owed. The archive gate is therefore merge-plus-green on main, plus one piece of evidence the code alone cannot give — the index repair in `tasks.md` § 3, because requirement 3 turns today's silent skip into a red and the change would otherwise land red on its own gate. Concretely: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a scratch-clone run of the readiness proof that PASSES rather than skips — which is the first time any fresh clone will have executed this test's assertion at all. The change ships ACTIVE and archives only after that.
Status: draft
Proposed: 2026-08-26
Origin: The 2026-08-26 triage of a red `tests/doc-health` suite in an agent worktree. The red was not caused by the branch under test; chasing it found two independent defects in one test, and the second of them had been hiding an assertion that has never run in continuous integration.
---

# Proposal: harden-ideation-readiness-check

## Why

`tests/doc-health/test_ideation_readiness.py::test_derivation_reproduces_the_real_bootstrap_clusters`
is the proof that the readiness lane's cluster derivation still reproduces the
landed `ideation-cross-reference` index. It carries two independent defects.
One makes it red on a healthy repository. The other makes it green — by never
running — on every repository that matters.

### Defect A — the proof reads a checkout nobody asked it to read

```python
def _openxfactory_root():
    marker = Path("openxFactory") / "ideation" / "cross-reference.yaml"
    base = Path(REPO_ROOT).resolve()
    for d in [base, *base.parents]:
        if (d / marker).is_file():
            return d / "openxFactory"
    return None
```

The walk starts at the repository under test and climbs until it finds a
directory holding `openxFactory/ideation/cross-reference.yaml`. Inside the
aggregation workspace that condition is satisfied by exactly one directory —
the aggregation root — and the answer it returns is always the same one shared
checkout, `/home/brett/projects/xFactory/openxFactory`, no matter which
repository the run was launched against.

For the shared checkout itself the answer is correct by coincidence: the
resolved path and the repository under test are the same directory. For every
agent worktree it is wrong, and wrong silently. The proof reads another
session's index, another session's corpus, and — through the checker's
identically-shaped `find_index_validator()` — another session's validator,
then reports a verdict about the repository the developer thinks they are
testing.

The failure mode is not theoretical. It fired on 2026-08-26: the shared
checkout carried an uncommitted edit to `ideation/cross-reference.yaml` that
bumped `generation.source_revision` without regenerating the body, leaving 67
listed clusters against a corpus that derives 253 at the revision it now
claims. Every worktree on the
machine went red. Every isolated clone passed, at every revision. A test whose
verdict is a function of what an unrelated session has open in an editor is
not a test of anything.

This is the same hazard family the workspace has met before —
`exclude-worktrees-from-notebook-projection` (2026-07-12) fixed the mirror
image of it, a scan that treated `<repo>-worktrees/` containers as governed
repositories and would have published unmerged branch content into the shared
books. The lesson there was the same: in this workspace, a filesystem walk is
not a repository identity.

### Defect B — the assertion has never run in continuous integration

The proof reconstructs its comparison corpus from git at the index's own
pinned revision, which is right. What it does with a pin it cannot resolve is
not:

```python
    proc = subprocess.run(["git", "-C", str(openx), "archive", rev, "ideation"],
                          capture_output=True)
    if proc.returncode != 0:
        pytest.skip(f"pinned revision {rev[:12]} unreachable (shallow clone?)")
```

`main` pins `f13a3b6007736292e1e157febef1ac733e534de9`. That commit is
reachable from no local branch, is not an ancestor of `origin/main`, and
appears in zero refs on the remote. So `git archive` fails, the branch above
turns the failure into a skip, and the assertion below it is never evaluated.

The parenthetical guess is also false where it fires. `pytest-suite.yml`
checks out at `fetch-depth: 0` — a complete clone. A complete clone still does
not carry an object no ref reaches, so continuous integration hits this branch
with a NON-shallow repository and reports a shallow-clone suspicion. Anyone
following that reason would go looking for a fetch-depth setting that is
already correct.

Locally the object survives only as a leftover from a fetch of the source
branch. `git gc --prune` flips this test from pass to skip on a developer's
machine with no change to any tracked file.

## What was measured

Everything below was measured on 2026-08-26 against `origin/main` at
`31c931fa`, in a scratch worktree created off it. Nothing was written to the
shared checkout.

**The suite, before any edit.** `python3 -m pytest tests/doc-health -q` →
**1 failed, 895 passed**. The single failure is
`test_derivation_reproduces_the_real_bootstrap_clusters`, and it is defect A
in flight: the branch changes no code at all.

**Defect A, resolution.** From the scratch worktree,
`ir.find_index_validator()` returns
`/home/brett/projects/xFactory/openxFactory/scripts/validate-ideation-cross-reference.py`
— the shared checkout's copy, not the worktree's own. At the same moment,
`git -C /home/brett/projects/xFactory/openxFactory status -sb --
ideation/cross-reference.yaml` reported ` M` with the file pinning
`8fe986f0` and listing 67 clusters, against 253 that derive from the corpus at
that revision — while the committed file on `main` pins `f13a3b60` and lists
290.

**Defect B, reachability.** `git branch -a --contains f13a3b60` returns
nothing; `git merge-base --is-ancestor f13a3b60 origin/main` is false;
`git ls-remote origin | grep -c f13a3b60` is `0`. A fresh
`git clone --bare --no-local` of the repository reports
`rev-parse --is-shallow-repository` → `false`, cannot `cat-file` the object,
and returns 128 from `git archive f13a3b60 ideation`. Complete clone, absent
object, skip fires, reason is wrong.

**How the pin got there, exactly.** The index was regenerated on branch
`codex/brainstorm-packet-migration` at commit `1f852a5f` ("docs: regenerate
cross-reference after packet migration"), which correctly pinned that
branch's then-HEAD, `da9bf3b7`. The branch landed on `main` as a single
squashed commit, `4e57009c` ("Migrate brainstorms into three-tier packets
(#322)"), whose only parent is `700c1a19`. Diffing the branch tip's index
against the landed index yields exactly one changed line:

```text
10c10
<   source_revision: da9bf3b7d0ee1d86d2d437d42a715c238dddce4b
---
>   source_revision: f13a3b6007736292e1e157febef1ac733e534de9
```

So the pin was moved by hand to the branch tip while the body stayed as
generated, and the squash then made both the old pin and the new one
unreachable. Two revisions of the same shape as the working-tree edit found in
the shared checkout the same morning — a pin bumped without a regeneration.

**The repair is one line, and it is measured.** Rebuilding the derivation from
the corpus at each candidate revision and comparing skeletons against the
committed body:

| revision | reachable | derived clusters | reproduces the committed body |
| --- | --- | --- | --- |
| `da9bf3b7` (what the body was generated at) | no | 290 | yes |
| `4e57009c` (the commit that landed the index) | **yes** | 290 | yes |
| `origin/main` at `31c931fa` | yes | 290 | yes |

The derivation is stable across that whole range, so no regeneration of the
body is owed. Re-pinning to `4e57009c` makes the index's provenance claim
true and verifiable, and it is the honest choice among the three: it is the
commit that introduced this index into `main`, it is immutable, and the
derivation at it reproduces the body exactly.

## What this changes

The proof gains the two properties it was assumed to have.

1. **It resolves the repository under test first.** The ancestor walk becomes
   an explicit, announced fallback rather than the only mechanism. The module
   already carries the better shape at
   `scripts/doc_health/ideation_readiness.py:1067` — an `OPENXFACTORY_ROOT`
   override consulted before the walk, with `tests/ideation-dashboard/test_doxbench_contracts.py`
   pinning both the override and the explicit-root-wins ordering — so this is
   an existing pattern extended over two more resolvers, not a new one
   invented.
2. **It reads the index from committed state.** The corpus side is already
   revision-addressed; the index side becomes so too, at a named commit of the
   repository under test. After this, no concurrent edit anywhere on the
   machine can move the verdict.
3. **An unresolvable pin is a red, not a silence.** The two conditions are
   separated by asking the repository whether its history is truncated rather
   than by guessing, and the reported reason names the one observed.
4. **The current defect instance is repaired in the same change**, because
   requirement 3 turns today's skip into a failure and this change would
   otherwise land red on its own gate. The repair is the one-line re-pin
   measured above.

The effect on continuous integration is worth stating plainly: after this
change, a fresh clone runs an assertion that no fresh clone has ever run.
Whatever that assertion finds, it will be the first time it has been asked.

## What this deliberately does not change

- **The readiness lane's own findings stay report-only.** The lane is
  `pending_review`, `contested`, at most `warning`, and MUST NOT block merges
  or open regression issues in v1. None of that moves. The obligations here
  land on the VERIFICATION — the suite that proves the derivation rule — not
  on what the nightly lane reports.
- **No new deterministic check family.** The family enumeration and its three
  numerals in `doc-health`'s "Deterministic check families" are untouched, and
  this delta deliberately does not restate that requirement.
- **No change to the derivation rule, the evidence contract, or the index
  schema.** `derive_clusters`, `enforce_contract`, the gate constants, the
  boundary allowlist and the index schema are all out of scope. This change
  makes an existing proof honest; it does not change what is being proved.
- **The index generator is not touched.** `git_generation()` in
  `scripts/bootstrap-ideation-cross-reference.py` pins `rev-parse HEAD`, and
  it did nothing wrong here — the pin it wrote was correct for the tree it
  ran on. What went wrong happened afterwards, by hand.

### Named follow-ups, out of scope here

- **The governance rule that an index pin must be rewritten when a branch
  lands rebased or squashed is a SEPARATE FUTURE PACKET and is deliberately
  not proposed here.** This change makes the consequence loud — an unreachable
  pin turns red instead of silent — and repairs the one live instance. It does
  not state the process obligation that would have prevented the instance,
  because that obligation reaches beyond this surface: it is about how packets
  land, it would bind every generator that records a `source_revision`, and it
  interacts with the house rule against squash merges (`4e57009c` is itself a
  squash). That packet should be raised on its own evidence.
- **Two sibling test modules spell the same `_openxfactory_root()` helper**
  (`test_derive_possibles.py:29`, `test_readiness_dispatch.py:318`). This
  change moves them with the original, because leaving two copies of a
  resolver that was just declared wrong is how the hazard comes back. Whether
  the three should collapse into one shared fixture is a tidying question left
  open in `tasks.md` § 5.
- **The generator's behaviour on a dirty tree.** `git_generation()` pins
  `HEAD` whether or not the working tree is clean, so an index can be
  generated from content that no commit contains. That is a real gap, it was
  observed on the same morning, and it is not this change.

## Orchestrator decisions, flagged for veto

This packet was authored by a delegated session against a triage record. NO
approval act exists for it — see § Open Questions Q0 — so every decision below
was taken by the authoring session and is flagged for reversal. Reverting any
one of them is an edit to this change, not a new one.

1. **All three requirements land in `doc-health`, all ADDED, and no
   requirement is MODIFIED.** The obligations are about how the verification
   behaves, and `doc-health` owns the readiness lane. The alternative — an
   index-side requirement in `ideation-cross-reference` saying a pin must be
   reachable — was considered and declined: OpenSpec's `MODIFIED` replaces a
   requirement wholesale, ADDED requirements carry no such hazard, and an
   index-side obligation is close enough to the deferred governance packet
   above to risk pre-empting it.
2. **The read point is the repository under test at a committed revision, not
   the working tree and not the pinned revision itself.** Recorded with its
   two rejected alternatives in `design.md` § 2.
3. **The re-pin target is `4e57009c`, not current `main`.** Measured above;
   the alternative is stated in Q2 below.
4. **The repair rides this change rather than landing separately.** Splitting
   it would land requirement 3 red on its own gate.

## Open Questions

**Q0 — admission.** This packet has no approval act, and its `.openspec.yaml`
therefore carries `kind: ad_hoc` with an `id` and a `reason` but NO
`approved_by` / `approved_on` pair. That is deliberate rather than an
oversight: the promoted origin requirement demands explicit approval
provenance for an ad-hoc origin, the authoring session has none to record, and
fabricating one is the failure mode this repository has already refused once —
openxFactory PR #344 stopped rather than declare an origin it could not
support, and `create-medxchart-overlay-boundary` carries the shape of the
admission that closed it. **Until Brett admits this packet, `proposal-origin`
will report two `ad-hoc origin lacks required` ERRORS against it in the
nightly run.** Admission is a two-field edit to `.openspec.yaml` plus a
`Status:` move; nothing else in the packet depends on it.

**Q1 — should the skip survive at all?** Requirement 3 keeps a skip for a
genuinely truncated clone. The stricter alternative is to delete the skip
entirely and let a truncated clone fail too, on the argument that a proof
which silently declines to run in some environments is exactly what produced
defect B. The recommendation is to KEEP the narrowed skip: no current runner
is shallow (`fetch-depth: 0` everywhere that matters), so the branch is
already unreachable in practice, and keeping it costs one named, observable
condition while deleting it would red every future shallow runner for a reason
unrelated to the index.

**Q2 — re-pin to `4e57009c` or regenerate at current `main`?** Both produce a
body identical to today's, so the choice is about which claim the index should
make. `4e57009c` says "this index describes the corpus as it stood when this
index landed", which is true and stays true. Current `main` says "this index
describes the corpus as it stands today", which is also true today and decays
on the next ideation commit. **Recommendation: `4e57009c`** — a provenance pin
should name the state it was derived from, not the state it happens to still
match.

**Q3 — should the three duplicated resolver helpers collapse?** Left open in
`tasks.md` § 5 rather than decided here. The three test modules each carry
their own `_openxfactory_root()`; this change fixes all three in place. A
shared fixture would be tidier and would make the next such fix one edit
instead of three, but it moves test infrastructure that three unrelated
modules depend on, and that is a bigger change than the defect warrants.

## Impact

- Affected capability: `doc-health` — three ADDED requirements, nine
  scenarios, no requirement MODIFIED.
- Affected code: `tests/doc-health/test_ideation_readiness.py`,
  `tests/doc-health/test_derive_possibles.py`,
  `tests/doc-health/test_readiness_dispatch.py`,
  `scripts/doc_health/ideation_readiness.py`.
- Affected artifacts: `ideation/cross-reference.yaml` — one line, the
  `generation.source_revision` pin — and `ideation/cross-reference.md`, which
  restates that pin at its line 9 and is re-rendered with it.
- Risk: LOW on the code, and the residual risk is entirely in what the
  un-silenced assertion will find. The proof has never run in a fresh clone,
  so its first honest execution is also its first real result. If it fails
  there for a reason unrelated to these three requirements, that finding
  belongs to this change's realization and is reported rather than suppressed.
