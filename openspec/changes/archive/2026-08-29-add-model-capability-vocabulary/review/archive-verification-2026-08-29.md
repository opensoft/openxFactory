# Archive verification: `add-model-capability-vocabulary`

Status: record
Date: 2026-08-29
Verifier: Claude Opus 5 (agent), in an isolated scratchpad clone branched from
`origin/main` `9c501df6`.

## The gate, and that it holds

`docs/release-realization-flow.md` refuses to archive a code-surface change
until its code is merged on the implemented target through the owning domain's
engineering gates, plus a green run. The proposal declares:

```
code_surface: openxFactory (contracts/schemas/xfactory-workbench-model-catalog.schema.yaml …
              scripts/ideation_dashboard/doxbench_model.py … tests/ideation-dashboard/)
target_release: implementation_pending
```

Both conjuncts are discharged, and each is checkable rather than asserted:

| obligation | evidence |
| --- | --- |
| merged on the target | PR #498, squash `8ccfb67bc0fabfa728d709a2efa0cd87b14656fb` |
| green run | `pytest-suite`, `merge-master-approval`, `wallet-validation` all pass on that head; the four gate directories re-run green AT the squash |
| the release the surface owed | `contract-v2.2`, tag object `f86f2212645d6fe71d36b20db04e107060033f05`, peeling **from the remote** to `8ccfb67b` |
| release verified | `verify-commit --commit contract-v2.2` pass; `verify-tag --remote origin --tag contract-v2.2` pass |
| sentinel resolved | `0b9e31c8` replaced `unpublished:contract-v2.2` with the dereferenced squash sha |

Brett ruled the archive in session on 2026-08-29, after the gate held.

## Promotion verified BYTE-FOR-BYTE

The archive ran through `scripts/proposal-support.py … archive`, never bare
`openspec`, and reported `+ 2, ~ 0, - 0, → 0`. That report is the claim; below
is the check of it.

THE DELTA IS PURELY ADDITIVE, which is verified rather than assumed. The
ratified `specs/ideation-dashboard/spec.md` carries exactly one section heading,
`## ADDED Requirements` — no `## MODIFIED`, no `## REMOVED`. The lossy-restatement
class (#329/#330), where a MODIFIED delta restates some of a requirement's
scenarios and promotion silently drops the rest, is therefore structurally
absent here rather than merely unobserved.

**Counts, measured before and after on the same checkout:**

| measure | before | after | delta |
| --- | --- | --- | --- |
| `ideation-dashboard` requirements | 100 | 102 | +2 |
| `ideation-dashboard` scenarios | 457 | 466 | +9 |
| `ideation-dashboard` bytes | 279,235 | 285,744 | +6,509 |
| promoted requirements, all specs | 531 | 533 | +2 |
| promoted scenarios, all specs | 1,835 | 1,844 | +9 |
| capability directories | 52 | 52 | 0 |

+2 and +9 are exactly what the delta carries (2 requirements; 5 + 4 = 9
scenarios). No capability directory is added: both requirements join an existing
capability.

**No sibling loss, proved by the diff rather than by the net count.** A netting
count is precisely what hid #329's defect, so the check here is directional:

```
diff PRE POST  ->  deleted lines: 0    added lines: 61
```

ZERO deleted lines. Every line of the pre-archive canon survives verbatim; the
promotion is strictly an insertion.

**The promoted text is byte-identical to the ratified text.** Each requirement
block was extracted from the archived delta and from promoted canon and hashed:

| requirement | scenarios | sha256 (delta) | sha256 (canon) |
| --- | --- | --- | --- |
| A catalog entry declares the input modalities it accepts, from a closed vocabulary | 5 | `607235d3a4a7…` | `607235d3a4a7…` |
| The catalog type enforces every bound the released schema enforces | 4 | `0ab29e77ccc4…` | `0ab29e77ccc4…` |

Identical in both rows. Nothing was reworded, truncated or re-wrapped on the way
into canon.

## Supporting docs

NONE. The packet holds `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`realization-evidence.md` and `review/ratification-2026-08-24.md`, and no
`supporting-docs/` directory — confirmed before the run and reported by the verb
itself: `NO SUPPORTING DOCS … (origin retained, nothing to package)`. The
supporting-doc half of the archive gate is vacuous here rather than skipped.

## Contracts untouched

`git status --porcelain -- contracts/` is EMPTY. An archive moves no contract
bytes: the release surface was cut at `contract-v2.2` and this act only promotes
requirements and relocates a packet, so `contracts/releases/contract-v2.2.digests.yaml`
still describes the bytes the repository holds and the published tag keeps
verifying at its own commit.

## The one path this archive strands, and why it stays stranded

`contracts/CHANGELOG.md` line 15, inside the `contract-v2.2` entry, cites

```
openspec/changes/add-model-capability-vocabulary/review/ratification-2026-08-24.md
```

and that directory no longer exists: the packet is now under
`openspec/changes/archive/2026-08-29-add-model-capability-vocabulary/`. Swept at
this commit, it is the ONLY dangling change-packet citation in the whole
changelog — every other reference already uses the `openspec/changes/archive/`
form. So this is a real path broken by this act, found here rather than by a
later reader, and it is left alone deliberately on two independent grounds.

**It was true when the release shipped.** `contract-v2.2` was cut and tagged on
2026-08-29 while the packet stood at exactly that path. A CHANGELOG entry is the
immutable record of what a release SHIPPED, and this repository has already
ruled on precisely this shape: the `contract-v1.40` entry was deliberately NOT
edited when its "TWO DELEGATED RULES" claim went outdated, on the reasoning that
"editing it would make it describe a bundle that was never published"
(recorded in `contracts/manifest.yaml`'s own comment block). The same reasoning
governs a path.

**And an archive moves no contract bytes.** `contracts/CHANGELOG.md` is a
digested member of `contracts/releases/contract-v2.2.digests.yaml`. Editing it
here would put editorial drift into a surface this act has no business touching,
purely to tidy a reference whose target is one predictable directory away. The
archived packet is discoverable from the README's "Archived changes:" row, from
the archive directory's own date-prefixed name, and from this record.

Recorded rather than silently accepted, so that a reader who follows that link
and lands nowhere finds the reason here instead of assuming the archive was
botched.

## What archiving does NOT close

The staged topic `doxchat-auto-fit-routing` KEEPS ITS ROW (§6.2). This is exit
(a) of three; the topic exits only when (b) fit-aware routing and (c)
compress-to-fit disclosure have landed too. Nothing here reads `modalities` to
choose a destination.
