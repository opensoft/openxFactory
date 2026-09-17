---
code_surface: openxFactory (and NOT ONE BYTE OF IT MOVES IN THIS PULL REQUEST). The realization this packet proposes is a LATER pull request in this same repository, authored after ratification, and it is FOUR CLAUSES IN THREE MODULES plus FOUR TEST CASES IN THREE TEST PACKAGES plus FIVE DOCSTRINGS. The clauses, at the lines they carry on `c6997f12`: `scripts/code_surface.py:777` (`_unescaped`, `except OSError:` widened to `except (OSError, RuntimeError):`); `scripts/target_release.py:630` (`_unescaped`, the same widening) and `scripts/target_release.py:394` (`_registry_present`, the same widening); `scripts/proposal-support.py:347` (`_contained`, `except (OSError, ValueError):` widened to `except (OSError, ValueError, RuntimeError):`, the `ValueError` guarding a DIFFERENT operation's failure and STAYING). The test cases, ONE PER CLAUSE and therefore FOUR in three packages rather than one per module, each FAILING against the unfixed clause and each building its symlink loop at test time under `tmp_path`: ONE in `tests/code_surface/` (`_unescaped`), TWO in `tests/target_release/` (`_unescaped`, and `_registry_present` declared in its own docstring as a test of the CLAUSE, `design.md` D3 and D0.5), ONE in `tests/proposal-support/` (`_contained`, asserted through `contained_dir` and `contained_file`). The docstrings, FIVE and not four because `_contained` carries none of its own and the prose that states its contract lives on the two public wrappers it serves: `code_surface._unescaped`, `target_release._unescaped`, `target_release._registry_present`, `proposal-support.contained_dir` and `proposal-support.contained_file`, each amended to name `RuntimeError` beside `OSError`, which is also what keeps `code_surface._unescaped`'s written claim that `target_release._unescaped` "is the exact shape this mirrors" TRUE. NO OTHER FILE IS EDITED: no validator arm moves, no existing test is edited, renamed, flipped or deleted, no workflow changes (the required `pytest-suite` already runs `tests/`), no contract member, no schema, no report field and no promoted byte; and NO SYMLINK IS ADDED TO THIS REPOSITORY'S TRACKED TREE, which is a requirement of this packet and not merely its practice. THIS pull request carries the PACKET ONLY: `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, one `## ADDED` spec delta, one README *Active changes* bullet, and the machine-seeded per-change sweep-ledger row in `tests/sequenced_after/corpus-ledger.yaml` that any filing owes.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` is touched, no digest set moves, no `contract_bundle_version` is spent and no release tag is owed; the three modules are house tooling, pinned by nobody. Under `release-realization` a non-empty code surface archives on MERGED-PLUS-GREEN REALIZATION EVIDENCE rather than on landing, so this packet archives only after its realization pull request has merged and run green, and openxFactory issue 1074 closes THERE.
sequenced_after: []
---

# Proposal: harden-path-escape-helpers-against-symlink-loops

Status: draft

Proposed: 2026-09-17, in lane `openxfactory-5` (display `openXfactory-5`),
session `651195c7`, in answer to openxFactory
[#1074](https://github.com/opensoft/openxFactory/issues/1074), which this lane
FILED on 2026-09-16 at the landing of PR #1029 and CLAIMED before authoring
(comment `5714101833`). **NO RATIFYING WORD HAS BEEN GIVEN.** Nothing here is
ratified, promoted, realized or archived by this filing; `tasks.md` § 1 is Brett
Heap's act and is not ticked by this lane.

Origin: openxFactory

## Why

**FOUR GUARDS PROMISE AN ANSWER AND THREE OF THEM RAISE INSTEAD, ON ONE INPUT
NOBODY WROTE THEM AGAINST.**

`pathlib.Path.resolve(strict=True)` signals a symlink loop by raising
`RuntimeError`, not `OSError`. Measured on this machine at `Python 3.12.3`, the
version `.github/workflows/pytest-suite.yml` pins for the required check:

```
$ ln -s a b && ln -s b a
$ python3 -c "import pathlib; pathlib.Path('a').resolve(strict=True)"
RuntimeError: Symlink loop from 'a'
$ python3 -c "print(isinstance(RuntimeError(), OSError), isinstance(RuntimeError(), ValueError))"
False False
```

Three modules carry a guard that resolves a candidate path, compares it with the
resolved root, and hands the caller a NEGATIVE ANSWER when the comparison fails,
so the caller DROPS the candidate rather than judging bytes that live outside the
scanned tree. Each names only `OSError` (one names `OSError` and `ValueError`),
so all four clauses are open at the failure a symlink loop produces. **ONLY THREE
OF THE FOUR ARE DRIVEN TO THAT CLAUSE BY A COMMITTED TREE SHAPE**, which the
table's last column states per row rather than leaving to the prose. The line
numbers below are re-read on `c6997f12`, the head this packet is authored
against, rather than carried from the issue:

| module | guard | clause | contract | reached at the clause by |
| --- | --- | --- | --- | --- |
| `scripts/code_surface.py` | `_unescaped` (`:746`) | `except OSError:` (`:777`) | returns `None`, candidate dropped | a COMMITTED tree shape |
| `scripts/target_release.py` | `_unescaped` (`:600`) | `except OSError:` (`:630`) | returns `None`, candidate dropped | a COMMITTED tree shape |
| `scripts/target_release.py` | `_registry_present` (`:354`) | `except OSError:` (`:394`) | returns `False`, registry absent | NO tree shape; a RACE only |
| `scripts/proposal-support.py` | `_contained` (`:341`) | `except (OSError, ValueError):` (`:347`) | returns `False`, path uncontained | a COMMITTED tree shape |

**THREE OF THE FOUR ARE REACHABLE THROUGH A COMMITTED TREE SHAPE, AND THE
TRACEBACKS ARE TAKEN AND NOT INFERRED.** Built at `c6997f12` on a minimal tree
carrying one real change directory whose `proposal.md` is a two-link symlink
loop (`proposal.md -> loop-b -> proposal.md`), with a second tree whose
`.openspec.yaml` carries the loop instead:

```
$ python3 scripts/validate-code-surface.py <tree>
  File ".../scripts/code_surface.py", line 816, in _proposals
    proposal = _unescaped(repo_root, CHANGES_DIR / child.name / "proposal.md")
  File ".../scripts/code_surface.py", line 775, in _unescaped
    resolved = candidate.resolve(strict=True)
RuntimeError: Symlink loop from '<tree>/openspec/changes/a-real-change/proposal.md'

$ python3 scripts/validate-target-release.py <tree>
  File ".../scripts/target_release.py", line 628, in _unescaped
    resolved = candidate.resolve(strict=True)
RuntimeError: Symlink loop from '<tree>/openspec/changes/a-real-change/proposal.md'

$ python3 -c "... proposal_support.former_identity_claimants(<tree2>)"
RuntimeError: Symlink loop from '<tree2>/openspec/changes/a-real-change/.openspec.yaml'
$ python3 -c "... proposal_support.declared_former_ids_in_tree(<tree2>, 'a-real-change')"
RuntimeError: Symlink loop from '<tree2>/openspec/changes/a-real-change/.openspec.yaml'
```

Two whole house validators end in a traceback, and so do the two public readers
the ARCHIVE GATE's former-identity arm is built on. A traceback is neither a drop
nor a finding; it is the gate refusing to report on the tree at all, which is the
one outcome each guard's own docstring was written to prevent.

**THE FOURTH SITE IS NARROWER THAN #1074 STATES IT, AND THIS PACKET CORRECTS ITS
OWN ISSUE RATHER THAN INHERITING THE CLAIM.** #1074 says
`target_release._registry_present` is shielded by its own `is_dir()` pre-check
"except when the repository root itself sits behind a loop". Measured here, that
exception does not hold either: with `repo_root` pointed at a loop,
`registry.is_dir()` is `False` (the loop is absorbed by `stat`, which reports no
directory rather than raising), so the function returns `False` at `:390` and
never reaches `:392`.

RE-MEASURED AT THIS HEAD IN ALL THREE POSITIONS the first requirement names, and
not only the one #1074 raised: a loop at the registry LEAF `contracts/releases`,
a loop at the ANCESTOR `contracts/` above an ordinary leaf, and `repo_root`
itself a loop. `_registry_present` returned `False` in every one, the pre-check
absorbing the loop each time. And where the pre-check DOES pass, the registry is
a real directory every component of which `stat` has just resolved, so
`resolve(strict=True)` on the next line cannot meet a loop either: only a tree
that changes BETWEEN the two reads can put one inside the clause. **The fourth
site is a CLAUSE-LEVEL, RACE-ONLY case and not a tree state.** It is widened
anyway, and `design.md` D3 gives the three reasons (the first of which is exactly
that race); the point here is that the correction is recorded where the
overstatement was made.

**AND IT IS NOT A DEFECT ANY TREE IN THIS ESTATE STANDS ON.** The live corpus
tracks ZERO symlinks, so nothing tracebacks today. What exists is four guards
whose written contract is wider than their code, in tooling whose whole purpose
is to judge a tree it did not author.

## What changes

**TWO `## ADDED` REQUIREMENTS OVER `release-realization`, AND A REALIZATION THIS
PULL REQUEST DOES NOT PERFORM.**

1. **`### Requirement: A containment guard answers every resolution failure and
   raises none`** (SIX scenarios) defines a path-containment guard BY ROLE rather
   than by name, requires that its failure set be MEASURED against the
   interpreter the gates run on rather than assumed from the operation's name,
   reaches the loop at the leaf, at any parent component and at the scanned root
   alike, RETAINS any catch already wider than the obligation, and makes a
   guard's documented claim to mirror another guard part of the obligation, so
   the two move in ONE act.
2. **`### Requirement: A symlink-loop proof is built at test time and never
   committed`** (FOUR scenarios) forbids a committed loop as a fixture, sets the
   fails-then-passes standard for the proof, and states what a guard that no tree
   state can reach owes instead: the widening still, and a proof declared as a
   test of the CLAUSE rather than dressed as a tree the estate cannot build.

**TEN scenarios in all**, counted from the delta file rather than carried.

The realization is `tasks.md` § 3, and it is a LATER pull request on a LATER
word.

## Why a packet and not a fix PR

**THE SHAPE BELONGS TO A RATIFIED, REALIZED SURFACE THAT IS NOT THIS LANE'S TO
EDIT AS A RIDER.** `scripts/target_release.py` realizes
`gate-realization-axis-vocabulary`, ARCHIVED on 2026-09-12 with its requirements
promoted; `scripts/proposal-support.py` is the governed OpenSpec wrapper the
estate's archive acts run through; `scripts/code_surface.py` realizes
`gate-code-surface-declarations`, whose own archive is still held on
merged-plus-green evidence. `code_surface._unescaped`'s docstring says the shape
is not its packet's invention: "`target_release._unescaped` is the exact shape
this mirrors." Widening one module alone falsifies that claim. This is the
disposition PR #1029 recorded rather than taking the rider
([comment `5703004913`](https://github.com/opensoft/openxFactory/pull/1029#issuecomment-5703004913)),
and #1074 is the follow-up it promised.

## What this packet does NOT do

- **It does not move one byte of code.** The diff is this packet's own directory,
  one README bullet and one per-change sweep-ledger row.
- **It does not edit one promoted byte.** No file under `openspec/specs/` is
  touched, and the delta carries no `## MODIFIED` block, so no marker is owed and
  no modified-block-currency row is opened.
- **It does not commit a symlink.** The proof this packet's realization owes is
  built at test time; committing the loop is refused by the second requirement.
- **It does not widen any guard's JUDGMENT.** The same paths are dropped, the
  same registry is absent and the same paths are uncontained as before; what
  changes is that a failure which used to end the run now produces the answer the
  guard already promised.
- **It does not touch the other ELEVEN `except OSError`-family clauses in these
  modules.** `code_surface.py:568`, `:656`, `target_release.py:337`, `:528` and
  `proposal-support.py:162`, `:416`, `:2541`, `:3724`, `:4290`, `:4312`, `:4511`
  guard reads, writes and subprocess calls rather than containment resolutions,
  `:3724` being the support-archive read inside `verify_archive`. The eleven are
  counted by an AST scan of the three files rather than by eye. Nor does it
  narrow `proposal-support.py:3939`'s entrypoint `except Exception:`, which is
  already WIDER than this obligation and is RETAINED for that reason.
  `design.md` D4 records why the scope is the containment role and not the token
  `except OSError`.
- **It does not close the origin issue.** `code_surface` is non-empty, so the
  archive is a separate act on merged-plus-green realization evidence and a
  separate word, and openxFactory issue 1074 is closed THERE, by a closing
  keyword written in the archive pull request and in no commit message on this
  branch.

## The decision, put for a veto (OQ-1)

`design.md` carries five decisions. FOUR are put here as one multiple choice,
recommendation first:

- **(a) AS FILED, RECOMMENDED.** D1 ADDED over `release-realization` (against a
  MODIFIED block over either realization-axis title, against a new capability of
  its own). D2 all four sites in ONE act (against three riders, against fixing
  only the reachable three). D3 widen `_registry_present` too, though no tree
  state reaches it (against leaving it and naming a successor). D4 scope the
  obligation to the CONTAINMENT ROLE (against every `except OSError:` in the
  three modules, against naming the four clauses literally).
- **(b) Narrow D3:** leave `_registry_present` as it stands, name it a successor,
  and let the module carry one widened guard and one not.
- **(c) Narrow D2:** fix `code_surface.py` only, since that is where the finding
  was raised, and file the other two separately.
- **(d) Widen D4:** make the obligation reach every resolution this estate's
  tooling performs, not only the containment role.

Each cost is written out in `design.md`. **D5 (the test shape) is not put for a
veto**: it is the second requirement's own subject and the ratifying word reaches
it with the rest of the packet.
