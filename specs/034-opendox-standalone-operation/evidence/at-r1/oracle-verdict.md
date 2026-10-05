# AT-R1 at `RELEASE1_TIP`: the browser half's oracle verdict, with the HTTP half beside it (T096)

Status: record

**Feature**: [`034-opendox-standalone-operation`](../../spec.md) · **Task**: T096
([`tasks.md`](../../tasks.md)) · **Run**: 2026-10-05, 15:30:02–15:34:07Z, at
openDox-code `main` `389e5a4a`, `RELEASE1_TIP` · **Lane**: `openXfactory-3`,
delegated by `openxfactory-4` (#656 `5987202449`)

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`; T091). It is T096's run of AT-R1's browser half (spec.md §
"AT-R1", steps 4–8; quickstart.md § 4). The browser half is driven with
Playwright and judged by openDox-code's own `tests/smoke_signals.py` at the
commit under test. Beside it are AT-R1's HTTP half at the same commit, run on
the host with T095's harness, and T095's `acceptance` job at that commit.
Together they are SC-004's evidence for both halves. The run follows the
plan's text on `main`: quickstart.md §§ 1–5, as openxFactory#1222 amends them
(batch N: the page opens through the private copy, `5963851934`) and #1225
amends them (what "both editors stay usable" means, RULED `5971834845`).

## The commits

| | commit | how it is fixed |
|---|---|---|
| X, `RELEASE1_TIP` | `389e5a4a22e1778653dac9f17172de2c18f9f808` | T095's landing commit on openDox-code `main`: openDox-code#75 is `MERGED` into `main` with merge commit `389e5a4a` (`gh pr view 75 -R opensoft/openDox-code`) |
| P, T087's pin | `dede32b4b6f3d0f147d599776f83628c5af8ff3d` | the openDox root's `contracts/code-pin.yaml` `commit:` and its `code` gitlink, both `dede32b4`, at openDox `main` `504324de`. T087 set them (openDox#18 → `e1e3a3c3`) |
| P-against-X | `git diff --quiet dede32b4 389e5a4a -- src/ pyproject.toml migrations/ README.md LICENSE` exits **0** | T099. Neither commit's `pyproject.toml` maps a build input from outside that list: both map `package-dir` `src`, `data-files` `migrations/*.sql` and `readme` `README.md`. With exit 0, X's runs stand for P, so nothing ran at P and no temporary branch was made |
| T095's `acceptance` job at X | a `workflow_dispatch` of `validate.yml` on `main` while `main` was X: run [`37333323932`](https://github.com/opensoft/openDox-code/actions/runs/37333323932), `head_sha` `389e5a4a22e1778653dac9f17172de2c18f9f808` (equal to X), `acceptance` job [`111841708700`](https://github.com/opensoft/openDox-code/actions/runs/37333323932/job/111841708700): **success**, *"AT-R1 HTTP half: PASS (314 assertions held)"* | the holder's ruling `5987619278`, Q1; § "T095's acceptance job" |

## Verdict

**PASS** at X: every item of T096's list passes in both repositories, with
zero `pageerror`, nothing undeclared (the three declarations below, each
satisfied exactly) and no 5xx.

```text
AT-R1 HTTP half    at 389e5a4a22e1778653dac9f17172de2c18f9f808: PASS (314 assertions held)
AT-R1 browser half at 389e5a4a22e1778653dac9f17172de2c18f9f808: PASS ((a) PASS; (b) PASS)
```

| AT-R1 item (T096's list) | (a) plain-documents | (b) plain-notes, no front matter |
|---|---|---|
| the page opens through the `file://` URL the start printed, and the token leaves the address bar (step 4; T104, #1222) | PASS | PASS |
| the wheel renders the fixture's tiles: a tile for every station the snapshot fills (step 5) | PASS: 8 / 2 / 1 / 1 / 1 / 1 tiles for source, grouping, candidate, selection, submission, completion | PASS: 3 / 2 for source and grouping, and 2 derived "Candidate:" tiles, an extra and not a miss |
| the lens renders the radar with the documents as dots, and no "nothing on the radar" (step 6) | PASS: 8 dots for 8 documents | PASS: 3 for 3 |
| the lens offers neither seed action (R1Q19 (a)) | PASS: no seed control, no selection column | PASS |
| a grouping tile's `workbench` verb opens the staging workbench (step 7) | PASS | PASS: (b) yields 2 grouping tiles from shared topics (R1Q13 (a) with (c)) |
| before any turn, the chat rail shows "no model configured", with how to configure one | PASS: *"No model configured. To configure one, declare a model binding with "opendox model-binding add" ("--help" lists its fields), or put the local harness "omp" on PATH, then restart this console."* | PASS |
| a turn is refused `model_capability_unavailable` | PASS: HTTP 403 `model_capability_unavailable`; the rail withholds Send, naming why (*"chat is unavailable — no approved model is configured; both editors remain fully usable."*) | PASS |
| both editors open and accept edits (`5971834845`) | PASS: the Outline and Document buffers | PASS: Outline, Document and two more document buffers |
| create is refused by name: no create control is offered, and the plane note names creating a document and Save as needing the create gate (T102's by-scope posture) | PASS | PASS |
| Save is refused by name (`GATELESS_SAVE_REFUSAL`), and nothing is written | PASS: no request, and no browser signal | PASS |
| zero `pageerror` (step 8) | PASS: 0 | PASS: 0 |
| nothing undeclared, every declaration satisfied (step 8) | PASS | PASS |
| no 5xx from any route the panes request (step 8) | PASS | PASS |

**The declarations** (the driver's fixed list, `DECLARATIONS` in
`at_r1_browser.py`; each is satisfied exactly in both repositories, *"4
observed / 4 declared across 3 declaration(s)"*):

| URL | answer | console / requestfailed | why |
|---|---|---|---|
| `/views/intent-feed.js` | 404 | 1 / 1 | RULED OQ-F / Q5: not owed (10.2a, T075); `intent-binding.js` imports it optionally |
| `/snapshot-index.json` | 404 | 1 / 0 | openXdox's projection route; no standalone binding answers it, and the index degrades to the single snapshot |
| `/project-register.json` | 404 | 1 / 0 | a plain repository has no project register (`no project register`) |

> **Non-normative note** (the holder's ruling `5987619278`, Q2, as corrected
> by lane openxfactory-4; T097 lists it with research R16's non-normative
> corrections). spec.md's AT-R1 step 7 and T096 say that the create and Save
> refusal "is declared to `tests/smoke_signals.py`'s oracle". As observed,
> both are refused by name, with no browser signal: no `pageerror`, no
> console error and no failed request. Save's click shows
> `GATELESS_SAVE_REFUSAL` in place and sends no request at all (0 requests in
> the Save step, in both repositories). Create offers no control, and the
> plane note names it beside Save. So there is nothing to declare, and the
> oracle's "nothing undeclared" holds with the three load-time declarations
> alone; a declared signal that is never observed would itself fail the
> oracle. The text of spec.md and of the plan is not reworded.

## The HTTP half at X

T095's harness, `python3 acceptance/at_r1_http.py --keep-going`, as it is at
X (sha256 `fb2a2ff0545c3d1d2a31c0f5f53a93871b29bd0260068ef7fd43397a11d1bb25`),
run on the host from a fresh clone: **PASS**, *"AT-R1 HTTP half: PASS (314
assertions held)"*, exit 0. It covers both repositories, the private copy
read as a browser reads it, the catalog with no available entry, every route
the bundle can request (none answers 5xx), the stop, the opener's removal,
and no bundled PostgreSQL left behind.

## T095's acceptance job

openDox-code's `validate.yml` runs on `pull_request` and `workflow_dispatch`
only, so no job runs at a commit on `main` by itself. On the holder's ruling
`5987619278` (Q1), the evidence is a `workflow_dispatch` of `validate.yml` on
`main`, made while `main` was X. #75's last PR run does not stand in, because
a PR run tests a merge ref, not X. [`x/acceptance-job.txt`](x/acceptance-job.txt)
holds the exact calls.

- **The dispatch.** At 15:30:06Z,
  `gh api repos/opensoft/openDox-code/commits/main` answered X. At 15:30:07Z,
  `gh workflow run validate.yml -R opensoft/openDox-code --ref main` was run.
- **The run.** Run
  [`37333323932`](https://github.com/opensoft/openDox-code/actions/runs/37333323932),
  `workflow_dispatch` on `main`, created 15:30:05Z. Its `head_sha` is
  `389e5a4a22e1778653dac9f17172de2c18f9f808`, which equals X. Its `acceptance`
  job fetched `+389e5a4a22e1778653dac9f17172de2c18f9f808:refs/remotes/origin/main`
  and checked out `main`, so it ran at X.
- **The `acceptance` job.** Job
  [`111841708700`](https://github.com/opensoft/openDox-code/actions/runs/37333323932/job/111841708700),
  15:30:09–15:30:33Z: **success**, *"AT-R1 HTTP half: PASS (314 assertions
  held)"*.
- **At P.** Nothing was dispatched at P, and no temporary branch was made.
  The P-against-X step exited 0 (§ "The commits").

## At P

The P-against-X step exited 0, so X's runs stand for P, and nothing ran at P
(T099; the holder's ruling on Copilot's `r4174344151`, openxFactory#1225,
option (b), applies only when the step exits non-zero). Lane openxfactory-4's
own run of T099's step, at 15:29:25Z, exited 0 as well.

## How it ran

- **The runbook.** [`run-at-r1.sh`](run-at-r1.sh), beside this file, runs in
  the foreground. The run used the bytes with sha256
  `702e2a4be2ce59ced647fafe23771fd22102cd9c29b0da3b8bafef19c2574148`, which
  this PR's first commit, `f632d70c`, holds. Review then changed three
  things, and none changes a step the run took:
  - the commit argument is resolved with `rev-parse --verify
    "<arg>^{commit}"` before the checkout, so a ref such as `main` is accepted
    (Copilot `r4185918186`). The run passed X's full sha, which both forms
    accept;
  - GNU grep is found at run time, as the first `grep` on the PATH that
    reports itself as GNU grep, and no path is named for it (Principle IV;
    Copilot's second review). On the run's host that is the same program.
    The browser half run again at X with the file as it then stood gives the
    same check results in both repositories;
  - a commit's own harness must leave its checkout clean, or the run stops
    before the browser half installs it (Copilot `r4186065384`). The run's
    `x/tree-after-harness.txt` is empty, so this run passes it, and the HTTP
    half run again at X with the file as it now stands passes too (`314
    assertions held`).

  The file beside this record has sha256
  `8ba962fd7586ad476a6a464b0be4c102b415d078469ce4ed53ded2c03426bbb9`. The runbook runs:
  - a fresh clone of openDox-code at the commit, with an empty
    `git status --porcelain --ignored`;
  - the HTTP half;
  - then quickstart.md §§ 1–5, once per repository.
- **The install** is quickstart.md § 1's, `pip install "<checkout>[local]"`.
  It is constrained by the commit's `constraints-cpython312-linux.txt` on
  CPython 3.12 on Linux, the same lock on the same condition as T095's harness
  (the holder's ruling on t096-dry finding F3). It installs `opendox==0.1.0`
  and `pixeltable-pgserver==0.6.0`; [`x/venv-freeze.txt`](x/venv-freeze.txt)
  lists the whole set.
- **The start** is the one documented command, `opendox generate-and-open
  --local --repo-root <repo> --repository fixture --no-open --port 18636`,
  run from outside the checkout.
  - Its output names the private copy in ONE `console file://…` line and
    adds B3's hint line. It never prints the token.
  - The runbook reads that printed URL and checks that it names
    `$OPENDOX_STATE_DIR/console/<port>.html`.
  - It reads the token from the copy as quickstart.md § 3 on `main` does,
    which includes checking that the raw `/capabilities` payload holds the
    token neither by name nor by value.
  - It sends the token to the catalog over stdin, never on a command line.
- **The drive.** [`at_r1_browser.py`](at_r1_browser.py) (sha256
  `763b59194df0a451935974808d1a1183d79593cb6e0133233542bb2f9fdddff8`) opens
  exactly the printed `file://` URL.
  - It runs Playwright 1.61.0 with its Chromium 149.0.7827.55, from the
    environment's own browser cache, at a 1500 × 1000 viewport.
  - It collects `console`, `pageerror` and `requestfailed` from the first
    byte, through the oracle's own `Errors.wire`.
- **After each pass:**
  - the copy is gone once the server stops;
  - no process references the state directory;
  - the start printed no token;
  - no file of the pass's record holds the token's value
    (`token-scan.txt`).
- **The record, sanitized.**
  - Every host path in the files under `x/` is replaced by a placeholder
    (`$TMPDIR`, `<state>`), and byte-identical screenshots are stored once.
  - `screenshots.txt` names every screenshot the driver took, with its
    sha256 and the stored file, so each `screenshot` field in a
    `<label>-result.json` still resolves.
  - `SHA256SUMS` covers every file of the run.

## Before this run

- **Lane openxfactory-4's dry run, t096-dry (2026-10-03),** ran on local
  integrations of the phase-3 drafts and found four things. Each is resolved
  in X:
  - F1: the rail's loaded-document switch read `/workbench/thread`, which a
    standalone plane answers `403`, giving one undeclared console error per
    switch. On the holder's ruling (i) the product was fixed: openDox-code#85
    → `c4b55cc4`, `doxbenchThreadSeam(workbenchGate.session, …)` in `app.js`.
    At X the drive makes 1 / 4 switches and 0 thread reads.
  - F2: `tests/test_chat_model_configuration.py` read the token from
    `/capabilities`. The fix was applied in T104's own branch (`ddb26c3`,
    "F2 applied") and landed with #84 → `32943cbf`.
  - F3: the two halves installed different dependency sets. The holder ruled
    that the browser half installs with the harness's lock.
  - F4: the harness's thread query was not the rail's. #75 now asks the bare
    route only, following #85 (`4d0e6d1`).
- **Lane openXfactory-3's rehearsals (2026-10-05)** all ran through this
  runbook and driver, on local merges that were never pushed. Every one
  passed both halves, with `314 assertions held`:
  - `main` `38d3350e` with #84's `c5fcdfa4` and #75's `b7b9b843`;
  - `main` `32943cbf` (T104 landed) with #75's `d50e8cef`, `ff04e015`,
    `234229d7` and `d698c6ea` in turn;
  - #75's head `d29e68ca`, which merges P.
- **What the runbook changed since t096-dry:**
  - it opens the page through the printed `file://` URL, not the copy's
    path rebuilt;
  - it reads the token as quickstart.md § 3 on `main` does (the raw-payload
    check, and the header over stdin);
  - it checks create as T102's by-scope posture states it (no create
    control, and the plane note names create and Save);
  - it scans the record for the token's value;
  - for T099's re-run at P it takes `HARNESS_FROM=X`;
  - its driver venv pins Playwright, and falls back to a private browser
    cache where the shared one is read-only.

## Observations (none moves a verdict)

- (b) The wheel adds 2 derived "Candidate:" tiles while the candidate station
  is unfilled: an extra, not a miss (t096-dry's observation, unchanged).
- Save's refusal note reads *"Outline: Save refused -- …"* even when another
  buffer is the active one, as in t096-dry.
- No turn leaves the page: the rail withholds Send, naming why. So the
  refusal is measured on the route itself (HTTP 403
  `model_capability_unavailable`), from outside the page.

## The run's files

- [`run-at-r1.sh`](run-at-r1.sh) and [`at_r1_browser.py`](at_r1_browser.py):
  the runbook and the driver. The driver is as run, and the runbook is as run
  but for three review fixes (§ "How it ran").
- `x/`, the run at X. It holds:
  - `verdict.txt`;
  - `commit.txt` (the commit, the P-against-X line, the harness, the
    install, the driver);
  - `acceptance-job.txt`;
  - `http-half.log`;
  - `venv-freeze.txt`;
  - `a/` and `b/`, one per repository. Each holds the driver's log (the
    oracle's printed verdict), `<label>-result.json` (every check with its
    evidence, and every console error, `pageerror`, failed request and
    4xx/5xx tagged with its step), the start's output, and the screenshots
    of steps 1–4 (`<label>-1-load.png` to `<label>-4g-save-refused.png`).
- `SHA256SUMS`: every file of the run above.
