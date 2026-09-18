# Design: harden-path-escape-helpers-against-symlink-loops

Status: ratified
Ratified by: Brett Heap, 2026-09-18, approximately 09:55Z — verbatim "Ratify;
land when green" (record `review/ratification-2026-09-18.md`)
Kind: design

**EVERY DECISION THIS AUTHORING SESSION TOOK IS HERE, WITH ITS ALTERNATIVE AND
THE ALTERNATIVE'S COST.** Filing openxFactory
[#1074](https://github.com/opensoft/openxFactory/issues/1074) at the landing of
PR #1029 and claiming it commissioned this AUTHORING and took none of them.
`proposal.md` § *The decision, put for a veto* (OQ-1) puts D1 through D4 as one
multiple choice with the recommendation first; this file carries the
measurements and the costs.

## D0. The measurement, taken before the design

**NOTHING BELOW RESTS ON A NUMBER ANYBODY TYPED, AND NOTHING IS CARRIED FROM THE
ISSUE.** Every line number was re-read on `c6997f12` in a fresh clone of
`origin/main`; every transcript was re-taken on that clone.

### D0.1 The interpreter

`.github/workflows/pytest-suite.yml:556` pins `python-version: "3.12"` for the
required check. The measuring shell is `Python 3.12.3 (main, Aug 31 2026)`.

```
$ ln -s a b && ln -s b a
$ python3 -c "import pathlib; pathlib.Path('a').resolve(strict=True)"
RuntimeError: Symlink loop from 'a'
$ python3 -c "import pathlib; pathlib.Path('a','proposal.md').resolve(strict=True)"
RuntimeError: Symlink loop from 'a'
$ python3 -c "print(isinstance(RuntimeError(), OSError), isinstance(RuntimeError(), ValueError))"
False False
```

CPython reaches it at `pathlib.py:1244` `check_eloop(e)`, which catches the
kernel's `OSError: [Errno 40] Too many levels of symbolic links` and re-raises it
as `RuntimeError`. The LEAF and a PARENT COMPONENT behave identically, which is
what makes the exposure wider than "a symlinked proposal".

### D0.2 The four sites, called directly

The three modules loaded from the clone at `c6997f12` and each guard called with
a root holding an `a -> b -> a` loop:

```
code_surface._unescaped(LOOP, Path('a'))                    -> RAISED RuntimeError
code_surface._unescaped(LOOP, Path('a')/'proposal.md')      -> RAISED RuntimeError
target_release._unescaped(LOOP, Path('a'))                  -> RAISED RuntimeError
target_release._unescaped(LOOP, Path('a')/'proposal.md')    -> RAISED RuntimeError
target_release._registry_present(LOOP)     [registry='a']   -> returned False
target_release._registry_present(LOOP/'a') [root in a loop] -> returned False
proposal_support.contained_dir(LOOP, LOOP/'a')              -> RAISED RuntimeError
proposal_support.contained_file(LOOP, LOOP/'a'/'x.yaml')    -> RAISED RuntimeError
```

### D0.3 The three reachable sites, end to end: TWO TREES, FOUR TRACEBACKS

THE COUNT IS THREE SITES, TWO TREES AND FOUR TRACEBACKING ENTRY POINTS, and they
are three different numbers of three different things. A FIFTH entry point was
driven and did NOT traceback, and that result is recorded here because the
realization must PRESERVE it rather than change it.

TREE ONE, a minimal `openspec/changes/a-real-change/` with `proposal.md -> loop-b`
and `loop-b -> proposal.md`:

```
$ python3 scripts/validate-code-surface.py <tree>     -> RuntimeError at code_surface.py:775 (via _proposals:816)
$ python3 scripts/validate-target-release.py <tree>   -> RuntimeError at target_release.py:628
```

TREE TWO, the same tree with the loop on `.openspec.yaml` instead, driving the
two public readers the archive gate's former-identity arm uses, and a third
reader beside them:

```
former_identity_claimants(<tree2>)                    -> RAISED RuntimeError
declared_former_ids_in_tree(<tree2>, 'a-real-change') -> RAISED RuntimeError
contained_change_dir_names(<tree2>)                   -> {'a-real-change'}   (does not reach the loop)
```

`contained_change_dir_names` is the fifth entry point and the one that already
ANSWERS: it filters change directories by their own `is_dir()` before any
containment resolution, so the loop on the header never reaches a guard. Its
result is CORRECT today and must be UNCHANGED after the widening, which is why
`tasks.md` § 4.3 re-runs it beside the four and asserts the same set rather than
a drop. A widening that turned this into a drop would be a change of judgment,
which `proposal.md` forbids.

### D0.4 Where the guards are NOT reachable, and why that matters

`code_surface._proposals` skips a child whose `is_dir()` is `False`, so a loop at
a CHANGE DIRECTORY name is absorbed before `_unescaped` is called. The reachable
committed shapes are the ones above (`<change>/proposal.md`,
`<change>/.openspec.yaml`) and a loop at `openspec`, `openspec/changes` or
`openspec/changes/archive`, which `_proposals` resolves with no pre-check at
`code_surface.py:795` and `:799`. This is why the requirement is written about the
GUARD'S ANSWER rather than about one file name: which paths reach a guard is a
property of today's callers, and the callers move.

### D0.5 The correction to #1074's own text

#1074 says `_registry_present` is shielded "except when the repository root
itself sits behind a loop". Measured, that exception does not hold: `is_dir()` on
`<loop>/contracts/releases` answers `False` rather than raising, so the function
returns at `target_release.py:390` and never reaches `:392`.

RE-MEASURED ACROSS ALL THREE POSITIONS the first requirement names, so the claim
is exhaustive over the requirement's own vocabulary rather than over the one
position #1074 raised. `Python 3.12.3`, a two-link `a -> b -> a` loop built under
`tmp_path` in each position:

```
loop AT the registry leaf `contracts/releases`   -> registry.is_dir() False -> returned False
loop at the ANCESTOR `contracts/` above the leaf -> registry.is_dir() False -> returned False
repo_root ITSELF a loop                          -> registry.is_dir() False -> returned False
(control) registry a REAL dir, loop below it     -> registry.is_dir() True  -> returned True
(control) (loop).resolve(strict=True)            -> RAISED RuntimeError
(control) os.stat(loop)                          -> OSError errno 40, Too many levels of symbolic links
```

The two controls are what make the result a mechanism and not a coincidence:
`Path.is_dir()` calls `os.stat`, which reports the loop as `OSError(ELOOP)`, and
`is_dir()` ABSORBS `OSError` and answers `False`. `Path.resolve(strict=True)` on
the identical path re-raises the same `OSError` as `RuntimeError`
(`pathlib.py:1244` `check_eloop`). The narrower of the two contracts is the one
in front.

AND THE PRE-CHECK PASSING IS ITSELF THE PROOF THAT THE CLAUSE IS RACE-ONLY. If
`registry.is_dir()` is `True`, `os.stat` has just resolved every component of
`<root>/contracts/releases`, so `resolve(strict=True)` on the next line cannot
meet a loop on that path either. NO TREE STATE WAS FOUND, AND NONE CAN BE BUILT,
that drives this guard to its own clause by standing still: only a tree that
CHANGES between `:390` and `:392` does. That is D3's first reason stated as a
measurement rather than as a worry, and it is why the fourth site is called a
CLAUSE-LEVEL, RACE-ONLY case in `proposal.md`, in `.openspec.yaml`'s origin
reason and in `tasks.md` alike. The correction is recorded in all four
documents; D3 decides what follows from it.

## D1. Which capability, and ADDED rather than MODIFIED — RULED (a), 2026-09-18, approximately 09:55Z

**RECOMMENDED: two `## ADDED` requirements over `release-realization`.**

All three modules are `release-realization` tooling. `target_release.py` realizes
its promoted *Realization axis vocabulary is gated*; `code_surface.py` realizes
`gate-code-surface-declarations`, whose three requirements promote into the same
capability; `proposal-support.py` is the wrapper its *Proposal support archive
gate*, *Origin retention at archive*, *A moved packet declares the identity it was
ratified under* and *An undeclared rename arrival is refused at its landing* are
enforced by. One capability covers all four sites with no cross-capability delta.

**Alternative (i): a `## MODIFIED` block over *Realization axis vocabulary is
gated* or over *Realization axis declaration*.** Cost, measured: both titles are
ALREADY written by the active ratified `add-target-release-deferred-allocation`.
A second writer would owe `sequenced_after: [add-target-release-deferred-allocation]`,
would take its pre-text from that change's outcome rather than from canon under
*Ordered deltas and branch vocabulary*, and would inherit that requirement's
archive-order hold. It would also make a THIRD active writer of a requirement
whose existing two are part of the modified-block-currency population this
repository's self-gate is red on today. Declined.

**Alternative (ii): a new capability, `tooling-path-containment` or similar.**
Cost: a capability with two requirements and no other member, whose whole subject
is a property of `release-realization`'s own readers, and a second place a later
author must think to look. Declined.

**Neither title exists anywhere in the corpus** (`openspec/specs/`, every active
change's delta, the archive), so the ADDED block collides with nobody and
`sequenced_after: []` is a CORROBORATED root claim and not an assumed one.

## D2. One act across all four sites, or three riders — RULED (a), 2026-09-18, approximately 09:55Z

**RECOMMENDED: one act, all four sites, all three modules.**

`code_surface._unescaped`'s docstring ends: "`target_release._unescaped` is the
exact shape this mirrors." `target_release._unescaped`'s docstring opens: "THIS
IS `_registry_present`'S TEST, GENERALIZED TO ANY PATH THIS MODULE OPENS." Those
two sentences bind the four sites into one claim of identity. Correcting one
module leaves that claim FALSE, and a false claim of identity is worse for the
next reader than no claim: it is precisely what tells them they need only
understand one of the two. This is the reasoning PR #1029 recorded when it
DECLINED the rider, and it is why the remedy was deferred to a packet rather than
taken there.

**Alternative (i): three riders, one per owning packet.** Cost: each rider is a
one-line change to a module whose ratified packet is someone else's, arriving
under a landing about something else, with no test of its own and no record; and
between the first and the last, the mirror claim is false in the tree.

**Alternative (ii): fix the three REACHABLE sites and leave `_registry_present`.**
That is D3, and it is put separately because it stands whichever way D2 goes.

## D3. `_registry_present`, which no tree state reaches — RULED (a), 2026-09-18, approximately 09:55Z

**RECOMMENDED: widen it too, in the same act, and say plainly that its proof is a
test of the clause.**

Three reasons, each a fact rather than a preference:

1. **The shield is a race, not a proof.** `is_dir()` at `:390` and
   `resolve(strict=True)` at `:392` are two separate reads of a filesystem that
   can change between them. The pre-check makes the clause unreachable in a
   STATIC tree; it does not make it unreachable.
2. **The reader sees the clause.** A module whose two guards carry different
   failure sets teaches the narrower one, and `_unescaped`'s own docstring points
   AT this function as the test it generalizes. Leaving one of the two narrower
   re-opens the mirror defect INSIDE one module.
3. **The cost of widening is one token.** The cost of not widening is a named
   successor, a second review, and a module that disagrees with itself in the
   meantime.

**Alternative: leave it, name a successor.** Cost as above, plus the packet would
have to explain why the module it is fixing is left half-fixed. Declined.

**What this decision COSTS, stated rather than hidden:** the test for this site
cannot be a tree state. It is a test of the EXCEPT CLAUSE, driven by a seam (the
pre-check made to pass while the resolution fails), and the second requirement
requires that it be DECLARED as such rather than dressed as a reachable tree.
The other three sites carry ordinary fails-then-passes tree tests.

## D4. The scope of the obligation: the containment ROLE — RULED (a), 2026-09-18, approximately 09:55Z

**RECOMMENDED: the obligation reaches a guard by its ROLE (deciding whether a
candidate path is really inside the scanned tree, by resolving and comparing) and
not by the token `except OSError:`.**

The three modules carry ELEVEN other `except OSError`-family clauses, counted by
an AST scan of the three files rather than read off by eye
(`code_surface.py:568`, `:656`; `target_release.py:337`, `:528`;
`proposal-support.py:162`, `:416`, `:2541`, `:3724`, `:4290`, `:4312`, `:4511`).
Every one of them guards a READ, a WRITE or a SUBPROCESS, where an `OSError` is
the failure and a `RuntimeError` is not a thing the operation produces.
`proposal-support.py:3724` (`except (SupportError, tarfile.TarError, OSError)`,
the support-archive read inside `verify_archive`) is a READ like the rest and
stands with them; it was missed by the first hand count and the number above is
the scan's. ONE FURTHER CATCH in these modules is deliberately NOT in that count
because it is already WIDER than this obligation rather than narrower:
`proposal-support.py:3939`'s entrypoint `except Exception:`, which the first
requirement's fourth paragraph RETAINS and never narrows to match. Widening the
eleven would absorb real defects: a `RuntimeError` out of a YAML load or a subprocess helper is
a bug in this repository's own code, and swallowing it is how a gate starts
passing for the wrong reason.

**Alternative (i): every `except OSError:` in the three modules.** Cost above.
Declined.

**Alternative (ii): name the four clauses literally in the requirement.** Cost:
the requirement rots the first time a line moves or a fifth guard is written,
and a requirement that names line numbers is a requirement nobody can keep true.
The ROLE definition reaches a guard written next year. Declined.

## D5. The test shape (not put for a veto; it is the second requirement's subject)

**The loop is built at test time under `tmp_path` and nothing is committed.**

A committed loop is tracked as two ordinary git objects (mode `120000`) and
arrives through a pull request like any other file, which is exactly why it is
the shape the guards defend against; but as a FIXTURE it would be met by every
recursive reader this estate runs (`scripts/doc-health.py`, the corpus scans, the
archive gate, the notebook projection, the packaging tools), and by every
developer's editor and backup tool. A fixture that reds tools unrelated to the
defect it proves is a second defect introduced to demonstrate the first. The live
corpus tracks ZERO symlinks and this packet keeps it that way.

**The proof is a PAIR of runs.** A test authored beside a fix, which passes on
both sides of it, proves the fixed code works and says nothing about whether the
defect was real. `tasks.md` § 3 records, per module, the failing run against the
unfixed clause and the passing run against the widened one.

**Where the loop is built matters as much as when, FOR THE THREE REACHABLE GUARDS.**
Each test OF A REACHABLE GUARD, which is the case in `tests/code_surface/`, the
`_unescaped` case in `tests/target_release/` and the case in
`tests/proposal-support/`, builds its loop in ALL THREE exposed positions the
first requirement names: at the candidate's leaf, in a parent component above an
ordinary leaf, and at the SCANNED ROOT itself. THE FOURTH CASE IS NOT ONE OF
THEM AND THIS PARAGRAPH DOES NOT REACH IT: `_registry_present`'s proof is D3's
CLAUSE test, driven by a seam that makes the pre-check pass while the resolution
fails, and building it as a filesystem tree in any of these three positions
would produce a test that passes against the UNFIXED clause, which D5's own
fails-then-passes standard refuses. D0.5 measures all three positions for that
guard and gets `False` from every one; that measurement is the reason the case
is a clause test, and it is not a fourth tree fixture. (Copilot, PR #1083
`PRRT_kwDOTAvnrs6jcrL_`.) The second position is the one a reviewer's intuition
misses, because the leaf is a perfectly ordinary file. The third is NOT ONE SHAPE BUT TWO, and WHICH RESOLUTION FAILS
DIFFERS BY GUARD, which is why the transcript records the raising line and not
only the outcome. Measured at `c6997f12` on `Python 3.12.3`, root set to the loop:

```
code_surface._unescaped(LOOP, 'x.md')          -> RuntimeError at code_surface.py:775     `candidate.resolve(strict=True)`
target_release._unescaped(LOOP, 'x.md')        -> RuntimeError at target_release.py:628   `candidate.resolve(strict=True)`
target_release._registry_present(LOOP)         -> returned False, at the `is_dir()` pre-check
proposal_support.contained_file(LOOP, LOOP/'x.md') -> RuntimeError at proposal-support.py:343 `path.resolve(strict=True)`
proposal_support.contained_file(LOOP, real/'x.md') -> RuntimeError at proposal-support.py:346 `resolved.relative_to(root.resolve(strict=True))`
proposal_support.contained_dir(LOOP, real)         -> RuntimeError at proposal-support.py:346 `resolved.relative_to(root.resolve(strict=True))`
```

BOTH `_unescaped`s reach the loop THROUGH THE CANDIDATE and never through a
separate root read: `candidate = repo_root / relative` traverses the loop, so the
first resolution raises and the root resolution on the NEXT line never executes.
A test for that position proves a candidate path whose failing component is the
root, which is the scenario's subject, and it must NOT be written as a claim
about a root-side read. (Copilot, PR #1083 `PRRT_kwDOTAvnrs6jYFzB`.)

`_contained` IS the one guard whose root read is reachable on its own, because it
resolves the candidate first and the root separately inside `relative_to`: with a
real path as the candidate, `:343` succeeds and `:346` raises. That
clean-candidate sub-case is proved once, in `tests/proposal-support/`, and
claimed nowhere else.

`_registry_present` answers `False` at its pre-check in this position exactly as
in the other two (D0.5's table), so the scanned root is not an exception for that
guard: its single test is D3's CLAUSE test and not a fourth POSITION. That clause
test is the second of `tests/target_release/`'s two cases, which is what makes
the realization FOUR TEST CASES IN THREE PACKAGES (`tasks.md` § 3.4, § 4.1).
