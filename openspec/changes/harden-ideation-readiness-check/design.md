# Design: harden-ideation-readiness-check

Three decisions needed recording. The first two are about WHERE the proof
reads from; the third is about how one branch tells two conditions apart.
Everything else in this change is mechanical.

## 1. Resolution order — repository under test, then a declared fallback

**Chosen.** Try the repository under test. If it carries
`ideation/cross-reference.yaml`, it IS the subject and nothing else is
consulted. Only if it does not does the resolver reach further, and when it
does the run says which checkout it took and why.

The order for the reach-further step follows the shape this module already
carries at `scripts/doc_health/ideation_readiness.py:1067` for the Markdown
renderer: an explicit argument wins, then the `OPENXFACTORY_ROOT` environment
variable, then the ancestor walk. That ordering is not invented here — it is
already pinned by `tests/ideation-dashboard/test_doxbench_contracts.py`
(`test_openxfactory_root_env_selects_the_checkout`,
`test_explicit_root_wins_over_the_env_override`), and the same file pins the
fail-closed behaviour this change wants for an unreachable checkout
(`test_unreachable_checkout_fails_closed`). Extending an existing pinned
pattern over two more resolvers is cheaper and safer than a fourth spelling.

**Rejected — keep the walk, but stop it at the first git repository root.**
Superficially attractive and wrong in this workspace: a worktree's root IS a
git repository root, so the walk would stop correctly there, but the shared
checkout sits directly under an aggregation root that is also a git
repository, and the marker file (`openxFactory/ideation/cross-reference.yaml`)
is only ever satisfied ABOVE a repository root, never at one. The rule would
have to special-case the aggregation layout, which is exactly the coupling
that produced the defect.

**Rejected — resolve by remote URL rather than by path.** Correct in
principle, and it would identify a checkout rather than a location. It also
requires a subprocess per candidate, fails inside a bare or detached
environment, and cannot distinguish two worktrees of the same remote — which
is the case that actually matters here.

## 2. The read point for the index — committed state at the repository under test

**Chosen.** Read the index with `git show <ref>:ideation/cross-reference.yaml`
at a named committed revision of the repository under test, then read the
corpus at the `generation.source_revision` that index carries. The two sides
of the comparison are then both revision-addressed, and neither is a function
of anybody's editor.

The named revision is `HEAD` of the repository under test. That is the
smallest choice that fixes the defect: `HEAD` is what the checkout claims to
be, it is stable for the duration of a run, and it is what a reviewer would
name if asked which version of the index they were looking at.

**Rejected — read the working tree but require it clean.** This is the
tempting minimal fix, and it fails on its own terms in this workspace. An
agent worktree is routinely dirty for reasons unrelated to the index; refusing
to run there would trade a false red for a permanent skip, which is defect B's
mistake in a new place. Requiring only `ideation/cross-reference.yaml` to be
clean is better but still wrong: it makes the proof's availability depend on
whether an unrelated session happens to have saved a file, and it still cannot
run over a checkout that is legitimately mid-edit.

**Rejected — read the index at its own pinned revision.** Circular: the pin
lives inside the file, so the file must be read before the pin is known. It
would also prove the wrong thing — that the index at revision R agrees with
the corpus at revision R, which is a statement about history rather than about
what `main` carries today.

**The consequence, stated rather than hidden.** An index edit under review is
not proved while it sits in a working tree; it becomes subject to the proof
when it is committed. That is a real cost — a proposal that regenerates the
index will see the proof pass on the old index until the regeneration is
committed — and it is accepted, because the alternative is a verdict that
different sessions on one machine can disagree about.

## 3. Failure versus skip — ask the repository, do not guess

**Chosen.** When `git archive <rev> ideation` fails, ask two further
questions before deciding what the failure means:

- `git rev-parse --is-shallow-repository` — is this clone truncated?
- `git cat-file -e <rev>^{commit}` — is the object present at all?

A complete clone that cannot resolve the pin is a defect in the INDEX: the
index names a corpus state no reader can reconstruct, and the proof fails,
naming the pin and the file that carries it. A truncated clone that cannot
resolve the pin is a fact about the CLONE, and the proof reports a skip whose
reason names the truncation it observed.

The distinction is cheap — two `git` calls on a path that today runs zero —
and it is the whole point. The current reason, `"pinned revision ...
unreachable (shallow clone?)"`, is a conjecture presented as a diagnosis, and
it is false in the one environment where it actually fires: `pytest-suite.yml`
checks out at `fetch-depth: 0`, so continuous integration reaches this branch
with a complete clone and is told to suspect a shallow one.

**Rejected — always fail.** See proposal § Open Questions Q1. Recommended
against, not on principle but on cost: no runner that matters is shallow, so
the branch is already unreachable in practice, and deleting it would red a
future shallow runner for a reason that has nothing to do with the index.

**Rejected — fall back to the working-tree corpus when the pin is
unresolvable.** This is what the test did before its current form, and it was
removed for cause: the live tree moves daily, so the comparison broke as soon
as the ideation area grew past the index. Restoring it would reintroduce a
known defect in order to avoid reporting a new one.

## 4. Why the repair rides this change

Requirement 3 turns today's silence into a red. `main`'s index pins
`f13a3b60`, which is unreachable from every ref, so the first honest run of
the hardened proof fails on `main` itself. Landing the requirement without the
repair would mean landing a change that reds its own gate — so the one-line
re-pin is a task of this change rather than a follow-up.

The repair is a pin edit, not a regeneration: the derivation reproduces the
committed body byte-for-byte at `da9bf3b7`, at `4e57009c`, and at `origin/main`
alike (proposal § What was measured). `4e57009c` is chosen because it is
reachable, immutable, and the commit that actually introduced this index into
`main`.

What the repair does NOT do is state the rule that would have prevented the
defect — that a `source_revision` recorded on a branch must be re-derived when
the branch lands rewritten. That rule is named as a follow-up packet in the
proposal's § Named follow-ups and is deliberately not proposed here.
