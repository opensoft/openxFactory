# Support-Bundle Scope in the Archive Gate — Open Contract Item

Status: record
Kind: reference
Disposition: OPEN — both items below are unresolved and neither is authorized
by this document; each needs an OpenSpec change to close it.
Owner: openxFactory (the `release-realization` capability and the tooling that
executes it — `openspec/specs/release-realization/spec.md`,
`scripts/proposal-support.py`).
Opened: 2026-08-21, from the PR #228 review round (findings F2 and F3).

This is a **spec-text precision item, not a mechanism change**. The rule is
already right and the tool already implements it correctly; one SCENARIO under
it reads more absolutely than the requirement it illustrates, and that gap is
what generated a P2 review finding on PR #228 that was ultimately overturned.
Recorded so the next change that touches `release-realization` closes it,
rather than the next reviewer rediscovering it.

## F2 — the staged-origin scenario over-reads its own requirement

`openspec/specs/release-realization/spec.md`, the **Origin retention at
archive** requirement, is antecedent-scoped in its normative sentence but not
in its scenario.

The requirement's own governing clause (spec.md:81, under *Proposal support
archive gate*) is conditional:

> An OpenSpec change **with proposal supporting documents** SHALL NOT archive
> until … the supporting folder has been converted into a deterministic bundle
> with a readable, verifiable manifest.

But the staged-origin scenario reads unconditionally:

> **WHEN** a change with a staged origin reaches its archive gate
> **THEN** the archived `.openspec.yaml` **and the readable support manifest**
> MUST carry the identical origin id and path declared at creation

A staged-origin change that legitimately carries no supporting documents has no
support manifest for the origin id to be carried in, so read literally the
scenario cannot be satisfied by a shape the corpus contains **sixteen** prior
examples of (`add-ideation-dashboard`, `add-workbench-branch-sessions`,
`add-openxwallet`, `add-repository-lens`,
`add-session-notebook-reconciliation`, …). The executable reading has always
been the conditional one: `proposal-support.py`'s `verify()` checks an active
change's support only when `supporting-docs` exists, and an archived change's
bundle only when a manifest or bundle is present, falling through to the origin
check alone otherwise.

**The fix, when a change carries it:** amend the scenario's THEN to
*"and, where a support bundle exists, the readable support manifest"*, so the
scenario matches the requirement it illustrates. Spec text changes through an
OpenSpec change; this item is not one and does not authorize the edit.

## F3 — the deleted-supporting-docs surface

`archive_change` now decides whether to package on the presence of
`supporting-docs`, which means a change whose support folder was DELETED rather
than never created archives quietly with no bundle and no complaint. The origin
declaration still has to survive the gate (`origin_errors(strict=True)` runs
either way), so this is not a hole in origin retention — but it is a way to
lose supporting material silently.

The predicate half is already closed: `archive_change` reads
`(directory / "supporting-docs").exists()`, the same spelling `verify()` uses,
so the two readers of "does this change have supporting documents" cannot
disagree. What is NOT closed is detection: nothing notices that a folder which
once existed is gone. The candidate answer is the manifest's own history — a
support manifest recorded at transition time is evidence the folder existed —
but that is a mechanism change with its own design questions, not a one-liner,
and it belongs with whoever next touches the packaging path.

## Why neither blocks anything today

Both are refinements to a gate that is currently correct in behaviour. Phase A
archived through the sanctioned path with its origin intact and verified; no
supporting material was lost, because there was none to lose (its task 9.2
deliberately kept the staged topic for Phase B). The PR #228 refutation of the
associated review finding is on that PR, and cites the same spec.md:81 clause.
