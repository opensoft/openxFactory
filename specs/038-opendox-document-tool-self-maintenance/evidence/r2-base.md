# Release 2's base, and the re-measure at the ruling (T002)

Status: record

**Feature**: [`038-opendox-document-tool-self-maintenance`](../spec.md) · **Task**:
T002 ([`tasks.md`](../tasks.md)) · **Taken**: 2026-10-06, 16:09–16:27Z ·
**Lane**: `openxfactory-4` (the holder), with lane `openXfactory-3` for the
composed re-run (§ 4)

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a), `5817152735`;
T091). It follows plan 034's [`arc-base.md`](../../034-opendox-standalone-operation/evidence/arc-base.md)
in form. Every figure below is a command quoted with its output, or a measurement
credited to the lane that made it. Anything inferred says so.

## What it records

T002 asks for four things, in `evidence/r2-base.md`: every repository's `main`
(research.md's R0 command), the box census, `PACKET_MERGE=94b6f7f1` for F11.1, and
lane 3's composed re-run of 12.5's 16 governed suites against R2-INV-P4F's 174
reds. Plan 038 is ruled (`#656` `6013547504`) and release 2's first landings are
on `main`, so this note is the base the rest of release 2 is measured from.

## 1. Every repository's `main`

The R0 command of [`research.md`](../research.md) (§ R0), with its nine
repositories written out, run from this branch's clone. Run A, with its own
clock:

```text
$ date -u +%Y-%m-%dT%H:%M:%SZ; for r in <the nine repositories>; do git ls-remote https://github.com/$r refs/heads/main | cut -c1-8; done; date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-06T16:09:44Z
opensoft/openDox-code      34c20641
opensoft/openXdox-code     56e1c238
opensoft/openDox           d77f8cbf
opensoft/openXdox          9564d5d9
opensoft/openDox-spec      7db9438b
opensoft/openXdox-spec     f088b097
opensoft/openxFactory      51456835
opensoft/xFactory          1047586d
codeXfactory/codexFactory  563212a1
2026-10-06T16:10:31Z
```

The same command again as run B, at 16:26:12Z to 16:26:49Z, read the same nine
values except one: `opensoft/openXdox-code` `c6d15b27`. Its commit (T020,
openXdox-code#39) carries the committer time 16:10:44Z, 13 seconds after run A's
last line, so run A read the `main` that was in place when it asked. Each
repository's `main` SHA with its commit date, from `gh api repos/<repository>/commits/<sha>`
at run B:

| repository | R0 at plan time (2026-10-05T22:19:52Z) | `main` at run B (full SHA) | its commit date (UTC) | its subject |
|---|---|---|---|---|
| `opensoft/openDox-code` | `a9ac96f9` | `34c20641bb6b90ec344e3b173c2df6624eade59f` | 2026-10-06T14:34:28Z | T010: R2Q17 (a)'s required-check change, the sandbox live in validate (plan 038) (#89) |
| `opensoft/openXdox-code` | `56e1c238` | `c6d15b27ed2f941701897513090c7a7898df7be7` | 2026-10-06T16:10:44Z | T020, U-1: the governed host for the governed suites that drive the gate verbs (plan 038, P4F-5) (#39) |
| `opensoft/openDox` | `d77f8cbf` | `d77f8cbfb45f13c4393c958615e0ff4861ac6cb9` | 2026-10-05T16:39:19Z | T099, the root README names the PyPI install line (plan 034) (#19) |
| `opensoft/openXdox` | `9564d5d9` | `9564d5d9462ffd1a3155d9177206368e5061efa8` | 2026-10-05T12:34:19Z | openXdox root: code -> 56e1c238 (T086) and openDox -> e1e3a3c3 (T087) (plan 034 T094, T090 step 5) (#22) |
| `opensoft/openDox-spec` | `f7ee3c76` | `7db9438b4cc4446ab4e6ab5b552c220312deccc9` | 2026-10-06T14:37:28Z | T040, openDox-spec's three health schemas (plan 038) (#17) |
| `opensoft/openXdox-spec` | `f088b097` | `f088b09732e236279898b53ab9fb0f5ebc89509a` | 2026-09-17T12:24:45Z | Receive add-nightly-dashboard-refresh: the refresh lane, re-homed under RULING Q6 (§ 6.1) (#15) |
| `opensoft/openxFactory` | `0f2a87f6` | `5145683522d817f1b4e735e7837bdcbf4728777a` | 2026-10-06T14:38:35Z | T070: file realize-doc-health-direction-arc, the doc_health direction arc's own change (plan 038) (#1247) |
| `opensoft/xFactory` | `ce47bbc0` | `1047586df1885146437c4dd461bc3f0b016a0dd1` | 2026-10-06T14:23:23Z | Merge pull request #565 from opensoft/chore/sync-codexfactory-pin-a4036e00 |
| `codeXfactory/codexFactory` | `972bb6f6` | `563212a1166311d27abb2f95606aa9fa95dac254` | 2026-10-06T16:04:55Z | Merge pull request #510 from codeXfactory/049-us3-t026-selection |

The R0 column is [`research.md`](../research.md) § R0, as quoted there. Three
repositories did not move since it: openDox, openXdox and openXdox-spec. Six did,
and this is how far, each by the repository's own compare (`gh api
repos/<repository>/compare/<R0>...<run B>`):

- **openDox-code**, `a9ac96f9` → `34c20641`: one commit, T010 (#89). It changes one
  file, `.github/workflows/validate.yml` (+119 −1).
- **openXdox-code**, `56e1c238` → `c6d15b27`: one commit, T020 (#39), the first of
  12.5's repairs. It changes two files, `tests/conftest.py` (+206 −7) and
  `tests/test_host_plane.py` (+203 −3).
- **openDox-spec**, `f7ee3c76` → `7db9438b`: one commit, T040 (#17), 67 files, the
  three health schemas.
- **openxFactory**, `0f2a87f6` → `51456835`, from `git log --oneline 0f2a87f6..origin/main`:
  `ba89e046` (#1209), `92010d3e` (#1243, feature 037), `260234b5` (#1245, plan
  038), `91e961a0` (#1248, T005's batch Q), `51456835` (#1247, T070's arc change).
- **xFactory**, `ce47bbc0` → `1047586d`: two commits, the routine pin-sync of
  codexFactory to `a4036e00` (#565).
- **codexFactory**, `972bb6f6` → `563212a1`: the compare reports `ahead_by=146`. T008
  (#515) is among them, its merge commit `f1b019fe`.

The 2026-10-06 commit times are the pull requests' merge times, which is when
each landed.

## 2. The box census

#1144's `tasks.md` holds 125 boxes. plan 038's `tasks.md` § "Box accounting"
gives "42 open at `ce64afc9`" (research.md R0's census, taken at that branch
head). Re-counted at the current openxFactory `main`, `51456835`, with plan 034's
`box_census.py`, verbatim from [plan 034's `research.md`
appendix](../../034-opendox-standalone-operation/research.md) (lines 607–632; the
extracted file's sha256 is `516f11c3b4c958f1b05db4a0919a1e48368dc9d49ef0bd6ed8d637411ca0f2b7`):

```text
$ git rev-parse --short=8 HEAD   # a clone of origin/main, no edit to #1144
51456835
$ python3 -I box_census.py openspec/changes/add-neutral-product-standalone-operability/tasks.md
1 9 1.1[x] 1.2[x] 1.3[x] 1.4[x] 1.5[x] 1.6[x] 1.7[x] 1.8[x] 1.9[x]
2 8 2.1[x] 2.1a[x] 2.2[x] 2.3[x] 2.4[x] 2.5[x] 2.6[x] F2.1[x]
3 5 3.0[x] 3.1[x] 3.2[x] 3.3[x] F3.1[x]
4 5 4.1[x] 4.1a[x] 4.2[x] 4.3[x] F4.1[x]
5 12 5.0[x] 5.1[x] 5.2[x] 5.3[x] 5.3a[x] F5.1[x] 5.4[x] 5.4a[x] F5.2[x] 5.5[x] 5.6[x] F5.3[x]
6 4 6.1[ ] 6.1a[ ] 6.2[ ] F6.1[ ]
7 8 7.0[x] 7.1[x] 7.1b[x] 7.1a[x] 7.2[x] 7.3[x] F7.1[x] F7.2[x]
8 5 8.1[~] 8.1a[~] 8.1b[~] 8.2[~] F8.1[~]
9 8 9.1[x] 9.2[x] 9.2a[x] 9.3[x] 9.4[x] 9.5[ ] F9.1[x] F9.2[ ]
10 5 10.1[x] 10.2[x] 10.2a[x] 10.3[x] F10.1[x]
11 3 11.0[ ] 11.1[ ] F11.1[ ]
12 11 12.1[ ] 12.1a[ ] 12.2[ ] 12.3[ ] 12.4[ ] 12.4a[ ] 12.5[ ] F12.1[ ] 12.6[ ] 12.6a[ ] F12.2[ ]
13 8 13.1[x] 13.2[x] 13.3[x] 13.4[x] 13.4a[x] 13.5[x] 13.6[x] F13.1[x]
14 10 14.1[ ] 14.2[ ] 14.3[ ] 14.4[ ] 14.5[ ] 14.6[ ] 14.7[ ] 14.8[ ] 14.9[ ] F14.1[ ]
15 12 15.1[ ] 15.1a[ ] 15.1b[ ] 15.2[ ] 15.2a[ ] 15.3[ ] 15.4[ ] 15.5[ ] 15.6[ ] 15.6a[ ] 15.7[ ] F15.1[ ]
16 8 16.1[x] 16.2[x] 16.3[x] 16.3a[x] 16.4[x] 16.5[x] 16.6[x] F16.1[x]
F 4 F1[~] F2[~] F3[~] F4[~]
total 125 Counter({'x': 74, ' ': 42, '~': 9})
```

A second count, by line, over the same file:

```text
$ for s in ' ' x '~'; do /usr/bin/grep -c -F -- "- [$s] " tasks.md; done
42
74
9
$ /usr/bin/grep -c -E '^- \[( |x|~)\] ' tasks.md
125
```

The delta against `ce64afc9` is ZERO. The same script over #1144's `tasks.md` as
`ce64afc9` holds it (`git show ce64afc9:openspec/changes/add-neutral-product-standalone-operability/tasks.md`)
reads `total 125 Counter({'x': 74, ' ': 42, '~': 9})`, and `diff` of the two full
outputs is empty:

```text
$ diff census-ce64.txt census-main.txt && echo "census outputs identical"   # the two full outputs, saved to files
census outputs identical
```

Batch Q (T005, #1248, `91e961a0`) landed between the two, and it adds paragraphs
only: `git diff --shortstat ce64afc9 origin/main -- <#1144's tasks.md>` reads `1
file changed, 526 insertions(+)`, no deletion. So no box changed state.

The 42 open boxes are the same ones research.md R0 lists: Group 6's four (6.1,
6.1a, 6.2, F6.1), Group 12's eleven, Group 14's ten and Group 15's twelve (the 37
of release 2); 9.5, 11.0, 11.1 and F11.1 (the every-phase boxes); and F9.2 (the
direction arc's). 4 + 11 + 10 + 12 = 37; with 9.5, 11.0, 11.1, F11.1 and F9.2,
42.

## 3. `PACKET_MERGE`, for F11.1

`PACKET_MERGE=94b6f7f1`, as T002 and T093 say, is
`94b6f7f13b45c351b9142345738965c974b7dd37`, "File
add-neutral-product-standalone-operability: open the BUILD arc, recording ten
rulings (#1144)", committed 2026-09-23T20:16:24-04:00 (2026-09-24T00:16:24Z).
It is #1144's own landing, so F11.1 reads the arc's openxFactory landings as
`$PACKET_MERGE..$ARC_TIP` (#1144 `tasks.md`, 11.1's falsifier). It is on
openxFactory `main`'s first-parent line, as plan 034 recorded it:

```text
$ git rev-list --first-parent origin/main | /usr/bin/grep -c '^94b6f7f13b45c351b9142345738965c974b7dd37$'
1
$ git log -1 --format='%P' 94b6f7f1
f1c690b8f1041c892da8f7e1c7f847f11c35d7aa
$ git rev-list --count --first-parent 94b6f7f1..origin/main
83
$ git log --first-parent --format=%h --grep='^Arc: neutral-product-standalone-operability$' 94b6f7f1..origin/main | wc -l
3
```

The three openxFactory landings that carry the trailer are release 1's consumer
pins: `f56c87c6` (phase 1), `fcb45380` (phase 2) and `36908480` (phase 3).
Release 2 has landed none yet. F11.1 for release 2 is T093's, run as T032, T065
and T082.

## 4. Lane openXfactory-3's composed re-run

Lane openXfactory-3 measured it and this note quotes it; nothing here was
re-run. The claim is `#656` `6013610393` (2026-10-06T09:43:59Z), "release 2,
T002's composed run (lane 3's part), a READ-ONLY re-measure". The result is two
lines of `lane-coord-034/lane3-to-lane4.log` in the lane workspace, verbatim:

```text
2026-10-06T09:52:07Z T002 COMPOSED a9ac96f9 56e1c238 92010d3e: 174 red vs 174 (170 failed + 4 errors, 668 passed; R1Q23 (a) form, openxFactory submodules initialized recursively; openDox-code and openXdox-code tips unchanged since R2-INV-P4F, openxFactory 0f2a87f6 -> 92010d3e moved no submodule and nothing the suites import); moved: none (the same 174 nodes, short-summary causes byte-identical 174/174, traceback E-lines identical in all 147 parsed sections modulo the tmp path); passing composed: 5 suites / 210 cases (doxbench_mutation_boundary 80, gate_loop_views 74, hosted_actor 5, session_commits 22, session_records 29)
2026-10-06T09:52:31Z T002 NOTE for evidence/r2-base.md: the composed re-run (09:52:07Z line, 174 red, moved none, 5 suites / 210 cases passing) installs openDox from openDox-code main a9ac96f9, as R2-INV-P4F did, while openXdox-code pyproject.toml:126 and openxFactory nested openDox/code both pin dede32b4 (v0.1.0); openxFactory main moved 0f2a87f6 -> 92010d3e (only scripts/ideation_dashboard/nightly_lane.py and scripts/validate-factory-mcp.py, imported by none of the 16 suites). T002 writer finished
```

Read as lane 3's figures, each quoted:

- **174 red**: 170 failed and 4 errors, with 668 passed, against R2-INV-P4F's
  174 (research.md R2: "668 passed, 170 failed plus 4 errors, so 174 red, over
  **11** files").
- **No node moved**: "moved: none (the same 174 nodes ...)".
- **5 suites pass composed, 210 cases**: `doxbench_mutation_boundary` 80,
  `gate_loop_views` 74, `hosted_actor` 5, `session_commits` 22,
  `session_records` 29.
- **What the run installed**: openDox from openDox-code `main` `a9ac96f9`, the
  same as R2-INV-P4F did, while openXdox-code's `pyproject.toml:126` and
  openxFactory's nested `openDox/code` pin `dede32b4` (v0.1.0).
- **What moved under it**: openxFactory `main` `0f2a87f6` → `92010d3e`, "only
  `scripts/ideation_dashboard/nightly_lane.py` and
  `scripts/validate-factory-mcp.py`, imported by none of the 16 suites".

One check of the last bullet was made here, by command. Of the 48 files that
differ between `0f2a87f6` and `92010d3e`, two are under `scripts/`, and they are
those two:

```text
$ git diff --name-only 0f2a87f6 92010d3e | wc -l
48
$ git diff --name-only 0f2a87f6 92010d3e | /usr/bin/grep -E '^scripts/'
scripts/ideation_dashboard/nightly_lane.py
scripts/validate-factory-mcp.py
```

The other 46 are contracts, docs, ideation notes and `specs/` of feature 037.
That none of the 16 suites imports the two scripts is lane 3's statement and was
not re-checked here.

**What is newer than the re-run.** The re-run read openDox-code `a9ac96f9` and
openXdox-code `56e1c238`. Since then `main` moved in each (§ 1): openDox-code by
T010's one workflow file, openXdox-code by T020, a repair of the 174 itself
(`tests/conftest.py` and `tests/test_host_plane.py`). So the 174 is the base the
repairs T020 to T026 start from, and T020's effect on it is NOT measured here.
That T010's change to `.github/workflows/validate.yml` moves none of the 174 is an
inference from the file list above: no `src/` file of openDox-code changed, and
nothing was run to confirm it.

## What this note does not claim

- It does not re-run the composed suites. Section 4 is lane 3's, quoted.
- The nine `main`s are a reading at a moment (16:09–16:27Z). The repositories keep
  moving through release 2, and each task re-reads its own base.
- It adds no decision. The figures are inputs to T004's ruling and to the
  checkpoints (T033, T066), which record any node that moved since T002.
