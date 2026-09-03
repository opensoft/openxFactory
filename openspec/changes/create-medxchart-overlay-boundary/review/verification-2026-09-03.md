# Verification record: create-medxchart-overlay-boundary, 2026-09-03

Status: record
Kind: report
Captured: 2026-09-03, in the ratification lane `openxfactory-max001`
(session `5e783e4d`), on branch `ratify/create-medxchart-overlay-boundary`.

**Why this file exists.** `tasks.md` 4.3 says "Run targeted YAML/Markdown/Git
consistency checks and report any pre-existing dirty work left untouched" and is
ticked, but **no such report was ever written**. The checkbox is NOT unticked —
the checks were run in session on 2026-08-23 and unticking would assert they
were not. What is done instead is this: everything reproducible has been RE-RUN
now, with its command and its output, so the reader gets a report rather than a
claim; and the one half that cannot be reproduced is named as unreproducible
rather than described from memory.

This is a CAPTURED record. It is written once and never edited.

---

## 1. `openspec validate create-medxchart-overlay-boundary --strict`

```console
$ OPENSPEC_TELEMETRY=0 openspec validate create-medxchart-overlay-boundary --strict
Change 'create-medxchart-overlay-boundary' is valid
```

Run against the ratified content — the two spec deltas
(`specs/medxchart-overlay-boundary/spec.md`, THREE ADDED requirements;
`specs/domain-descendant-boundary/spec.md`, ONE MODIFIED requirement),
`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`. `openspec` 1.2.0.

## 2. `openspec validate --all --strict`

```console
$ OPENSPEC_TELEMETRY=0 openspec validate --all --strict
…
✓ spec/workstation-intake
✓ spec/xfactory-semantic-kernel
Totals: 85 passed, 0 failed (85 items)
```

Eighty-five items, zero failures — every active change and every promoted
specification in the repository, this change included.

## 3. The pin agreement, read from an INDEPENDENT clone

Read from a fresh shallow clone of `opensoft/MedxChart` rather than from any
working tree, so the result does not depend on the state of a shared checkout:

```console
$ git clone -q --depth 1 https://github.com/opensoft/MedxChart.git mcverify
$ git -C mcverify rev-parse HEAD
68d2f1f5db932cb5099ceac75dab66316ef22579
$ git -C mcverify ls-tree HEAD openChart
160000 commit d2376a31dbafa413d8e5ba032f4a2620a75d578e	openChart
$ grep -n revision mcverify/contracts/openchart-pin.yaml
7:  revision: d2376a31dbafa413d8e5ba032f4a2620a75d578e
```

**The two pins agree.** The nested `openChart` gitlink and
`contracts/openchart-pin.yaml`'s `pin.revision` both name
`d2376a31dbafa413d8e5ba032f4a2620a75d578e`. The manifest also carries
`schema_version: 1`, `kind: medxchart_openchart_pin`,
`repository: opensoft/openChart`, `remote: git@github.com:opensoft/openChart.git`,
`submodule_path: openChart`, `source_path: .`,
`relationship: pinned_upstream_composition` — the shape
`domain-descendant-boundary`'s pin rule names, and one of the two live examples
that rule was written from.

**What this verification does NOT establish, and the reason § 5 of `tasks.md`
exists:** that the agreement is ENFORCED. It is a human reading of two files.
`opensoft/MedxChart` carries no `tests/validate_pin.py`, no `pin-validation`
workflow, and no required check — its entire tracked tree is listed at § 5
below. The ratified rule's own scenario ("the descendant's own validator REFUSES
the tree rather than preferring either") has no implementation here yet.

## 4. The aggregation entry and gitlink, read from GitHub `main`

Read through the API rather than from the local superproject checkout:

```console
$ gh api repos/opensoft/xFactory/contents/.gitmodules --jq .content | base64 -d
[submodule "xFactories/MedxChart"]
	path = xFactories/MedxChart
	url = git@github.com:opensoft/MedxChart.git
[submodule "xFactories/MedxPractice"]
	path = xFactories/MedxPractice
	url = git@github.com:opensoft/MedxPractice.git

$ gh api repos/opensoft/xFactory/contents/xFactories --jq '.[] | select(.name=="MedxChart" or .name=="MedxPractice") | "\(.name) \(.type) \(.sha)"'
MedxChart file 68d2f1f5db932cb5099ceac75dab66316ef22579
MedxPractice file d8d73195609df3b567643a7bf1252eac352d9996
```

The aggregation's gitlink `68d2f1f5db932cb5099ceac75dab66316ef22579` is EQUAL to
`opensoft/MedxChart`'s own `main` (§ 3). The URL is the ABSOLUTE
`git@github.com:opensoft/MedxChart.git` form, **not** the relative
`../MedxChart` this proposal originally decided on:

```console
$ gh api repos/opensoft/xFactory/commits/386e7ee2 --jq '.sha, .commit.message, .commit.author.date'
386e7ee29fffab36197fbe12fe0139706a715f90
A relative submodule URL resolves to whatever cloned the superproject

MedxChart and MedxPractice entered .gitmodules as ../Medx* — on the
nightly runner the superproject is HTTPS, so they resolved to plain
https:// URLs the workflow's git@-only token rewrite never touches, and
every nightly since 2026-08-24 died at their clone. Normalize both to the
git@github.com: form their eighteen siblings use; the openxfactory App
now carries both repos, so the rewritten token'd clone succeeds.

2026-08-25T19:13:51Z
```

The boundary itself landed at `bed2a69` ("Replace openChart aggregate with
MedxChart", 2026-08-23T20:14:55Z). `0c6ea39` (2026-08-26) moved
`opensoft/MedxFactory` and `opensoft/MedxEHR` to the `MedxSoft` organization and
**did not touch either Medx descendant** — MedxChart's `opensoft/` home stands.

## 5. Host-absolute paths, and the descendant's whole tracked tree

```console
$ git grep -n '/home/' -- openspec/changes/create-medxchart-overlay-boundary
(no matches)
$ git -C mcverify grep -n '/home/'
(no matches)
$ git -C mcverify ls-files
.gitmodules
AGENTS.md
README.md
contracts/openchart-pin.yaml
openChart
openspec/changes/archive/.gitkeep
openspec/specs/.gitkeep
```

No host-absolute path in the change packet or in the descendant. And the
file list is the evidence for `tasks.md` 6.1: **seven tracked entries, all
composition metadata, ZERO openChart profile artifacts.** `opensoft/MedxPractice`
at `d8d73195` reads the same way — `.gitmodules`, `AGENTS.md`, `README.md`,
`contracts/openpractice-pin.yaml` (`kind: medxpractice_openpractice_pin`,
revision `9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`), and the `openPractice`
gitlink.

## 6. The remote

```console
$ gh repo view opensoft/MedxChart --json visibility,pushedAt,url
{"pushedAt":"2026-08-23T20:23:45Z","url":"https://github.com/opensoft/MedxChart","visibility":"PRIVATE"}
```

The remote `design.md`'s Open Question said "does not currently exist" has
existed since 2026-08-23T20:23:45Z — hours after the question was written.

## 7. The MedxFactory documentation edit, measured

```console
$ git show --stat 933c5025
commit 933c502511e2f9fb714a72cbcde8b9d6362d1b34
    Point intake plan at MedxChart composition
 ...-patient-intake-vertical-slice-delivery-plan-and-acceptance-gates.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```

`tasks.md` 3.3's "affected MedxFactory documentation links" is **one line in one
brainstorm file**: row P4 of the delivery-plan table, repointed from `openChart`
/ `../../../openChart/openspec/…` to `MedxChart` /
`../../../MedxChart/openChart/openspec/…`. The plural overstates the act.

## 8. What could NOT be reproduced

`tasks.md` 1.1's second half ("the unrelated dirty/staged state of the shared
xFactory and MedxFactory checkouts") and 4.3's "report any pre-existing dirty
work left untouched" describe a point-in-time observation of shared working
trees on 2026-08-23. **That state is gone and is not reconstructable**, ten days
and many sessions later. It is reported as unreproducible rather than restated
from memory.

What CAN be checked about it is the file list of each landing commit, and it is
reported here as measured rather than as clean:

```console
$ git show --stat bed2a69            # the aggregation
 .gitmodules | 6 +++---   CLAUDE.md | 3 ++-   README.md | 8 +++++++-
 openxFactory | 2 +-      project-register.yaml | 4 +++-
 xFactories/MedxChart | 1 +   xFactories/MedxFactory | 2 +-   xFactories/openChart | 1 -
 8 files changed, 18 insertions(+), 9 deletions(-)

$ git -C xFactories/MedxChart log --stat --format='%h %s'
68d2f1f Keep MedxChart bootstrap paths portable
 AGENTS.md | 6 +++---   openspec/changes/archive/.gitkeep | 0
4b0b6da Create MedxChart pinned openChart composition
 .gitmodules | 3 +++   AGENTS.md | 30 +++   README.md | 37 +++
 contracts/openchart-pin.yaml | 10 +++   openChart | 1 +   openspec/specs/.gitkeep | 0
```

Six of `bed2a69`'s eight paths are this packet's own — the `.gitmodules` swap,
the two gitlinks it trades, and the three documents `tasks.md` 3.2 names.
**TWO ARE NOT, and are disclosed rather than glossed:** the `openxFactory` and
`xFactories/MedxFactory` gitlinks moved in the same commit. Those are ordinary
submodule pin-syncs and neither is unrelated user work, but they are outside the
paths `tasks.md` 3.1–3.2 describe, so a reader comparing the task text to the
commit will find two entries the text does not account for. That is what the
commit contains.

Worth recording separately, because the ratified pin rule turns on it:
MedxChart's initial commit `4b0b6da` carries `contracts/openchart-pin.yaml` AND
the nested `openChart` gitlink **in the same commit**, which is exactly the
"BOTH SHALL be changed in the SAME commit" discipline
`domain-descendant-boundary` states. The boundary was built to the rule before
the rule was written (2026-08-23 against a 2026-08-28 ratification); § 5's
follow-on is what will keep it there without a human re-reading two files.
