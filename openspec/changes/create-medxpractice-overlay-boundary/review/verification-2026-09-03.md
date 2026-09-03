# Verification record: create-medxpractice-overlay-boundary, 2026-09-03

Status: record
Kind: report
Captured: 2026-09-03, in the ratification lane `openxfactory-max001`
(session `5e783e4d`), on branch
`change/ratify-create-medxpractice-overlay-boundary`, which is stacked on
`change/ratify-create-medxchart-overlay-boundary` (openxFactory PR #608).

**Re-measured 2026-09-03 in this packet's pre-capture fix round, on a tree that
had moved.** The sibling's own fix round landed while this one was in flight, so
its branch advanced `c39d29bc` → `4cb31b17` and was merged into this one (no
conflict) before these corrections were written. Everything below is stated
against THAT tree. What the merge changed for this record is named where it
falls: § 2's parenthetical about the sibling's item count, and § 4, § 5 and § 6's
console blocks, which showed filtered or composite output as though it were raw
and now show the filter that was actually run.

**Re-measured A SECOND TIME, 2026-09-03, after `create-medxchart-overlay-boundary`
(#608) merged to `main` at `0f1edc0e` and this branch was retargeted and
actually merged with `main` rather than with the sibling's own branch.** § 6's
console block is restated on that merged tree; § 10 carries the full
re-derivation and what did and did not move.

**Why this file exists.** `tasks.md` 4.1 and 4.2 are ticked and no report was
ever written for either. The checkboxes are NOT unticked — the checks were run
in session on 2026-08-23 and unticking would assert they were not. What is done
instead is this: everything reproducible has been RE-RUN now, with its command
and its output, so the reader gets a report rather than a claim; and the one
half that cannot be reproduced is named as unreproducible rather than described
from memory. It also carries the live readings the ratification's findings turn
on — the absent validator, the upstream drift, the aggregation entry — each
taken from an INDEPENDENT source rather than from a shared working tree.

This is a CAPTURED record. It is written once and never edited.

---

## 1. `openspec validate create-medxpractice-overlay-boundary --strict`

```console
$ OPENSPEC_TELEMETRY=0 openspec validate create-medxpractice-overlay-boundary --strict
Change 'create-medxpractice-overlay-boundary' is valid
```

Run against the ratified content — ONE spec delta
(`specs/medxpractice-overlay-boundary/spec.md`, THREE ADDED requirements and NO
`## MODIFIED Requirements` block), `proposal.md`, `design.md`, `tasks.md`,
`.openspec.yaml`. `openspec` 1.2.0.

## 2. `openspec validate --all --strict`

```console
$ OPENSPEC_TELEMETRY=0 openspec validate --all --strict
…
✓ spec/workstation-intake
✓ spec/xfactory-semantic-kernel
Totals: 86 passed, 0 failed (86 items)
```

Eighty-six items, zero failures — every active change and every promoted
specification in the repository, this change included. **The same command on the
sibling branch this one is stacked on returns 86 as well**, checked in a
detached worktree at `origin/change/ratify-create-medxchart-overlay-boundary`,
so this ratification adds no item and removes none; it narrows one that was
already counted. (As first written this paragraph added that "the sibling's own
record states 85, a reading taken earlier in that branch's life". **That is no
longer so, and the sentence is corrected pre-capture rather than left standing**:
the sibling's own fix round re-derived its record on its rebased tree and now
states 86/86 as well. Both branches read 86, both records say 86, and there is
nothing left to reconcile.)

## 3. The pin agreement, read from an INDEPENDENT clone

Read from a fresh shallow clone of `opensoft/MedxPractice` rather than from any
working tree, so the result does not depend on the state of a shared checkout:

```console
$ git clone -q --depth 1 https://github.com/opensoft/MedxPractice.git mpverify
$ git -C mpverify rev-parse HEAD
d8d73195609df3b567643a7bf1252eac352d9996
$ git -C mpverify ls-tree HEAD openPractice
160000 commit 9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d	openPractice
$ cat mpverify/contracts/openpractice-pin.yaml
schema_version: 1
kind: medxpractice_openpractice_pin

pin:
  repository: opensoft/openPractice
  remote: git@github.com:opensoft/openPractice.git
  revision: 9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d
  submodule_path: openPractice
  source_path: .
  relationship: pinned_upstream_composition
```

**The two pins agree.** The nested `openPractice` gitlink and
`contracts/openpractice-pin.yaml`'s `pin.revision` both name
`9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`, and the manifest carries the exact
shape `domain-descendant-boundary`'s pin rule names — including the
`kind: medxpractice_openpractice_pin` that rule cites as one of the live
examples its `<descendant_repo_snake>_<product_snake>_pin` grammar was written
from.

The repository has **one commit**, and that commit is the same-commit rule:

```console
$ gh api repos/opensoft/MedxPractice/commits --jq '.[] | "\(.sha[0:8]) \(.commit.author.date) \(.commit.message)"'
d8d73195 2026-08-23T20:44:43Z Create MedxPractice pinned openPractice composition
$ gh api repos/opensoft/MedxPractice/commits/d8d73195… --jq '[.files[].filename]|join(", ")'
.gitmodules, AGENTS.md, README.md, contracts/openpractice-pin.yaml, openPractice
```

`contracts/openpractice-pin.yaml` and the nested `openPractice` gitlink land in
the SAME commit, which is exactly the "BOTH SHALL be changed in the SAME commit"
discipline `domain-descendant-boundary` states — built to the rule on 2026-08-23,
five days before the rule was ratified with `split-openxwallet-repo` on
2026-08-28.

**What this verification does NOT establish, and the reason `tasks.md` § 5
exists:** that the agreement is ENFORCED. It is a human reading of two files.

## 4. The upstream: reachable, PUBLIC, and two commits ahead

```console
$ gh repo view opensoft/openPractice --json visibility,pushedAt,url,defaultBranchRef
{"defaultBranchRef":{"name":"main"},"pushedAt":"2026-08-30T15:03:12Z","url":"https://github.com/opensoft/openPractice","visibility":"PUBLIC"}

$ gh api repos/opensoft/openPractice/commits/9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d --jq '.sha, .commit.message, .commit.author.date'
9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d
Initialize spec-driven openPractice repository
2026-08-02T20:34:55Z

$ git ls-remote https://github.com/opensoft/openPractice.git HEAD refs/heads/main
0ec9fca72ecf493e2520e676387f0c3f327cc6e6	HEAD
0ec9fca72ecf493e2520e676387f0c3f327cc6e6	refs/heads/main

$ gh api repos/opensoft/openPractice/compare/9526bd9e…...main --jq '{status,ahead_by,behind_by}'
{"ahead_by":2,"behind_by":0,"status":"ahead"}

$ gh api repos/opensoft/openPractice/compare/9526bd9e…...main \
    --jq '.commits[] | "\(.sha[0:8]) \(.commit.message | split("\n")[0])"'
0205901b Document reimbursement retention control
0ec9fca7 Merge pull request #1 from opensoft/docs/add-reimbursement-retention-control
```

**The pinned revision is reachable on the public remote** — `design.md`'s first
risk, discharged by measurement rather than assertion. **And the pin is two
commits behind that remote's `main`**, which is the pin working: the composition
does not follow a moving branch. `design.md` Decision 2 records that re-pinning
is a deliberate act under the same-commit rule and that no re-pin runbook exists
in this repository today.

## 5. The aggregation entry and gitlink, read from GitHub `main`

Read through the API rather than from the local superproject checkout:

```console
$ gh api repos/opensoft/xFactory/contents/.gitmodules --jq .content | base64 -d
…    # excerpt: 20 submodule stanzas in the file; the two Medx ones are adjacent
[submodule "xFactories/MedxChart"]
	path = xFactories/MedxChart
	url = git@github.com:opensoft/MedxChart.git
[submodule "xFactories/MedxPractice"]
	path = xFactories/MedxPractice
	url = git@github.com:opensoft/MedxPractice.git
…

# and the same file asked directly whether openPractice is entered at all:
$ gh api repos/opensoft/xFactory/contents/.gitmodules --jq .content | base64 -d \
    | grep -c 'openPractice'
0

$ gh api repos/opensoft/xFactory/contents/xFactories --jq '.[] | select(.name=="MedxPractice") | "\(.name) \(.type) \(.sha)"'
MedxPractice file d8d73195609df3b567643a7bf1252eac352d9996
```

The aggregation's gitlink `d8d73195609df3b567643a7bf1252eac352d9996` is EQUAL to
`opensoft/MedxPractice`'s own `main` (§ 3). The URL is the ABSOLUTE
`git@github.com:opensoft/MedxPractice.git` form, **not** the relative
`../MedxPractice` this packet's landing commit chose:

```console
$ gh api repos/opensoft/xFactory/commits/3a365206 --jq '.sha, .commit.message, .commit.author.date, ([.files[].filename]|join(", "))'
3a365206f7e91d0563fd831feeee274f33d04642
Add MedxPractice composition boundary
2026-08-23T20:46:44Z
.gitmodules, CLAUDE.md, README.md, openxFactory, project-register.yaml, xFactories/MedxFactory, xFactories/MedxPractice

# the .gitmodules hunk as it landed
+[submodule "xFactories/MedxPractice"]
+	path = xFactories/MedxPractice
+	url = ../MedxPractice
```

`386e7ee29fffab36197fbe12fe0139706a715f90` (2026-08-25T19:13:51Z) normalized both
Medx entries to the `git@github.com:` form, verbatim: *"A relative submodule URL
resolves to whatever cloned the superproject … on the nightly runner the
superproject is HTTPS, so they resolved to plain https:// URLs the workflow's
git@-only token rewrite never touches, and every nightly since 2026-08-24 died at
their clone."*

**Two of `3a365206`'s seven paths deserve naming.** `xFactories/MedxFactory`
(`37a194f3` → `ccd40789`) is task 3.2's own pin-sync and is accounted for.
**`openxFactory` (`f879070f` → `a3248684`) is NOT accounted for by any task in
this packet** — an ordinary submodule pin-sync, not unrelated user work, but
outside the paths tasks 2.3–3.2 describe. Disclosed at `tasks.md` 2.3 rather
than glossed.

## 6. No validator, no workflow, no required check — and no sweep movement

```console
$ gh api repos/opensoft/MedxPractice/actions/workflows
{"total_count":0,"workflows":[]}

$ gh api repos/opensoft/MedxPractice/rulesets --jq '.[] | "\(.id) \(.name) source_type=\(.source_type) enforcement=\(.enforcement)"'
8981805 Copilot Auto-Review All PRs source_type=Organization enforcement=active
18834180 Require Code Owner Review source_type=Organization enforcement=active
```

**Zero workflows.** The only two rulesets are ORGANIZATION-sourced and neither
requires a status check, so there is no `pin-validation` check and nothing
re-reads the two pins § 3 agrees on. This is the measurement `tasks.md` § 5 is
commissioned from, and it is what keeps the ARCHIVE gate shut.

The corpus pin does **not** move for this ratification, and that is measured
rather than assumed:

```console
$ python3 scripts/validate-sequenced-after.py . --sweep
sequenced_after corpus sweep
----------------------------
change ids (33 active + 125 archived): 158
co-modified at requirement granularity (each would owe a declaration): 109
sole modifiers (each would declare `sequenced_after: []`): 49
ACTIVE changes: co-modified / sole: 21 / 12
declaring `sequenced_after:`: 1 (add-sequenced-after-substrate)
declaring an explicit `[]` root claim: 0
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 1 hop(s), from add-sequenced-after-substrate
```

**This is the merged-tree reading, after `main` at `0f1edc0e` (§ 10); the
reading on this branch's own pre-merge head was `157 / 109 / 48 / 22 / 11`
(33 active + 124 archived).** Identical, reading for reading, to the same
command on the branch base before this commit's edits, at whichever of the two
trees it is read. The reason is structural rather than lucky: this packet's
delta is ADDED-only both before and after the narrowing, and its capability
`medxpractice-overlay-boundary` has exactly one writer in the whole corpus — so
the change was a SOLE modifier before today and is a SOLE modifier after, and
renaming its requirement titles cannot make it share a key with anything.
**`tests/sequenced_after/test_sweep.py` is therefore NOT touched by this
commit**, and the contrast with the sibling is the point: adding a
`## MODIFIED Requirements` block moved four readings there
(`co_modified` 108 → 109, `active_co_modified` 21 → 22, `sole_modifiers` 49 → 48,
`active_sole` 12 → 11); narrowing an ADDED-only delta moves none here — on
either tree.

## 7. Host-absolute paths, and the descendant's whole tracked tree

```console
$ git grep -n '/home/' -- openspec/changes/create-medxpractice-overlay-boundary
(no matches)
$ git -C mpverify grep -n '/home/'
(no matches)
$ git -C mpverify ls-files
.gitmodules
AGENTS.md
README.md
contracts/openpractice-pin.yaml
openPractice
```

No host-absolute path in the change packet or in the descendant. And the file
list is the evidence for `tasks.md` 6.1: **FIVE tracked entries, all composition
metadata, ZERO openPractice profile artifacts.** `opensoft/MedxChart` at
`68d2f1f5` reads the same way with two `openspec/` `.gitkeep` placeholders
besides — an asymmetry deliberately not equalized (ratification record § 3,
P3-10).

## 8. The remote, and the MedxFactory edit, measured

```console
$ gh repo view opensoft/MedxPractice --json visibility,pushedAt,url,createdAt
{"createdAt":"2026-08-23T20:44:44Z","pushedAt":"2026-08-23T20:44:48Z","url":"https://github.com/opensoft/MedxPractice","visibility":"PRIVATE"}
```

PRIVATE, over a PUBLIC upstream (§ 4) — the asymmetry the narrowed spec delta's
first requirement names as the boundary's reason for existing. Unlike its
sibling, this packet never claimed the remote did not exist: `tasks.md` 2.2
tasked the publication and `design.md` § Goals assumed it, so there is nothing to
correct here.

```console
$ gh api repos/opensoft/MedxFactory/commits/ccd40789… --jq '.sha, .commit.message, .commit.author.date, ([.files[] | .filename + " (+" + (.additions|tostring) + "/-" + (.deletions|tostring) + ")"]|join(", "))'
ccd407895f869a072eb920c2541ea9bc5b4b7723
Use MedxPractice branded practice overlay
2026-08-23T20:45:44Z
README.md (+5/-0)
```

`tasks.md` 3.1's "MedxFactory orientation/composition documentation" is **one
file, five insertions, zero deletions**: two lines added to the "MedxFactory
uses" list and a three-line stanza to the layer ladder, both naming MedxPractice
as branded practice operations "over its pinned public `openPractice` upstream".
That is the whole of this change's MedxFactory surface, and `code_surface`
declares it in those terms.

## 9. What could NOT be reproduced

`tasks.md` 2.3's "without staging unrelated workspace changes" and 4.2's "clean
status for the newly changed repositories" describe point-in-time observations
of shared working trees on 2026-08-23. **That state is gone and is not
reconstructable**, eleven days and many sessions later. It is reported as
unreproducible rather than restated from memory.

What CAN be checked about it is the file list of each landing commit, and every
one of them is reported above as measured rather than as clean: `3a365206`'s
seven paths (§ 5, including the one no task accounts for), `d8d73195`'s five
(§ 3), and `ccd40789`'s one (§ 8). Nothing in any of the three is unrelated user
work; one path in one of them is simply outside what the task text describes,
and it is named.

Also not reproducible, and named rather than inferred: **why** the standalone
`openPractice` checkout's relocation (task 2.1) left no artifact anywhere a
remote can be read from. It is a local filesystem move of a repository whose
history, origin and tracked content are unchanged BY DESIGN — the act's own
success criterion is that it leaves no trace in Git.

**And that is why the spec delta's second requirement now obliges only half of
it** — corrected pre-capture, on this pull request's own review. As first
narrowed, that requirement stated BOTH halves: that the checkout lives at the
projects workspace root AND that the aggregation reaches openPractice only
through MedxPractice's gitlink. The first half is exactly what this section
reports as unverifiable, so swearing it as a SHALL contradicted this record. It
is now recorded as a LOCAL CONVENTION at `design.md` Decision 4, and the
requirement — retitled **"The aggregation reaches openPractice only through
MedxPractice"** — keeps only the remotely checkable half, which § 5 confirms:
the entry is `xFactories/MedxPractice` at its `git@github.com:opensoft/` remote,
and `grep -c 'openPractice'` over the aggregation's `.gitmodules` returns `0`.

## 10. Re-derived after merging `main` at `0f1edc0e`

**RE-DERIVED AFTER MERGING `main` AT `0f1edc0e` (the sibling #608 landed at
15:11:52Z, after #611/#614/#602/#604): strict total 86/86 → 86/86 (unchanged —
#608's own merge added no item this total was not already counting, and this
packet adds none); sweep `157 / 109 / 48 / 22 / 11` → `158 / 109 / 49 / 21 / 12`
(change ids / co-modified / sole modifiers / active co-modified / active
sole), identical to `main`'s own pin because this packet carries no `##
MODIFIED Requirements` block. Nothing else in either record changed; no
capture happened before the merge — capture is the merge of #609.**

This branch was RETARGETED from
`change/ratify-create-medxchart-overlay-boundary` to `main` after #608 merged,
and `git merge origin/main` (merge commit `de975f81`, parents `4fee15ce` and
`0f1edc0e`) landed with no conflict in this file, `ratification-2026-09-03.md`,
or `tests/sequenced_after/test_sweep.py` — the only conflict the operation
anticipated was `README.md`'s "OpenSpec Records" block, and git resolved it
without markers because the two branches' additions sat in non-overlapping
hunks: `main` already carried the sibling's RATIFIED row from #608 and this
branch added only its own MedxPractice row beside it. `git diff origin/main --
README.md` after the merge is confined to that one row. `python3 -m pytest
tests/sequenced_after -q` reads 118 passed against the merged-tree pin.
