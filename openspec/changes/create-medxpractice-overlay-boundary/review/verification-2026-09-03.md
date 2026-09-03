# Verification record: create-medxpractice-overlay-boundary, 2026-09-03

Status: record
Kind: report
Captured: 2026-09-03, in the ratification lane `openxfactory-max001`
(session `5e783e4d`), on branch
`change/ratify-create-medxpractice-overlay-boundary`, which is stacked on
`change/ratify-create-medxchart-overlay-boundary` (openxFactory PR #608).

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
already counted. (The sibling's own record states 85, a reading taken earlier in
that branch's life; the current reading on BOTH branches is 86, and it is stated
here as measured rather than reconciled to the earlier number.)

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
[submodule "xFactories/MedxChart"]
	path = xFactories/MedxChart
	url = git@github.com:opensoft/MedxChart.git
[submodule "xFactories/MedxPractice"]
	path = xFactories/MedxPractice
	url = git@github.com:opensoft/MedxPractice.git

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
change ids (33 active + 124 archived): 157
co-modified at requirement granularity (each would owe a declaration): 109
sole modifiers (each would declare `sequenced_after: []`): 48
ACTIVE changes: co-modified / sole: 22 / 11
declaring `sequenced_after:`: 1 (add-sequenced-after-substrate)
declaring an explicit `[]` root claim: 0
prose `Sequenced-after:` headers: 3 (3 archived)
DEEPEST DECLARED CHAIN RESOLVED: 1 hop(s), from add-sequenced-after-substrate
```

Identical, reading for reading, to the same command on the branch base before
this commit's edits. The reason is structural rather than lucky: this packet's
delta is ADDED-only both before and after the narrowing, and its capability
`medxpractice-overlay-boundary` has exactly one writer in the whole corpus — so
the change was a SOLE modifier before today and is a SOLE modifier after, and
renaming its requirement titles cannot make it share a key with anything.
**`tests/sequenced_after/test_sweep.py` is therefore NOT touched by this
commit**, and the contrast with the sibling is the point: adding a
`## MODIFIED Requirements` block moved four readings there
(`co_modified` 108 → 109, `active_co_modified` 21 → 22, `sole_modifiers` 49 → 48,
`active_sole` 12 → 11); narrowing an ADDED-only delta moves none here.

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
success criterion is that it leaves no trace in Git. The narrowed spec delta's
second requirement states the resulting obligation (the checkout lives at the
workspace root and the aggregation reaches openPractice only through
MedxPractice's gitlink), and the half of that which IS remotely checkable — no
direct `xFactories/openPractice` aggregate entry — is confirmed in § 5.
