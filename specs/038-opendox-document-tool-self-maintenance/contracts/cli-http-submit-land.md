# Contract: `submit` and `land`, CLI and HTTP

Status: draft

**Feature**: 038 · **Authority**: boxes 12.1–12.4a, 12.6, 12.6a; answers R2Q1–R2Q7,
R2Q9 (a) item 7 (`--local`). **A PROPOSAL until Brett rules the plan**
(OQ-12-9, -11, -12, -13, -14, -17; OQ-038-1; decisions N-1, N-2, N-11, I-1).

Both verbs are contributions of openDox's DEFAULT profile (decision N-2): a
host profile that replaces it carries neither in release 2 (R2Q3 (a)), and
under openDox's own profile they behave the same in every governance mode
(interplay I-1).

## `opendox submit`

```text
opendox submit <branch> [--repo-root PATH] [--local] [--json]
```

- Pushes `<branch>` to the attached remote `origin` through `SubmissionPort`
  (the bound `submission_factory` / `_submission_port`; `LocalGitSubmissions`
  by default, R2Q2 (a)). Prints the `Submission` report (data-model.md), `--json`
  as an object.
- Runs as the invoking user, in that user's checkout, with no console-presence
  or `--actor` gate (OQ-12-9). `--local` selects local mode explicitly, as
  `generate-and-open --local` does (R2Q9 (a) item 7).
- **Refuses by name** (exit non-zero, nothing pushed): `<branch>` is `main`; no
  `origin` (`NoSubmissionTarget`, 12.3); `origin` has several push URLs; the push
  URL carries a credential, redacted in the message (OQ-12-11).
- Never calls `gh` (12.4; F12.2 runs with `gh` absent).
- Under `governed`, `submit` goes through the host's contributed
  `SubmissionPort` (the instrument) when one is bound; the report names where
  the work went (R2Q4 (a)).

## `opendox land`

```text
opendox land <branch> [--repo-root PATH] [--local] [--json]
```

- Asks for confirmation over `/dev/tty`, naming the branch and its head; the
  answer mints the confirmation capability (12.6a). With no `/dev/tty`, it
  refuses, naming the missing terminal; there is no bypass flag (decision N-11).
- `standalone`: merges `--no-ff` in its own landing worktree, then
  fast-forwards a clean served checkout on `main` (R2Q6 (a)). Prints `Landed`,
  with the `git revert -m 1 <merge_commit>` that undoes it. Pushes nothing; a
  landed `main` leaves the checkout only by the user's own `git push`.
- `governed` with an instrument: submits through it and reports where the work
  went; the merge stays the governance's act (R2Q4 (a)).
- **Refuses by name**: `unknown` (no `main`; no declaration, naming the exact
  file `.opendox/governance.yaml` and the content to commit, R2Q7 (a));
  `governed-without-an-instrument`; `<branch>` is `main`; local `main` lacks the
  remote's tip (`ls-remote`); a stale or used confirmation; a conflict
  (`MergeConflict`, naming the paths and the remedy: bring `main` into the
  branch and resolve there, OQ-038-1).
- Serves the fix loop's drafts unchanged: a batch is one branch (OQ-12-17).

## HTTP routes (loopback server; 12.4a's three-clause gate and the console token on all three)

| method and path | body | answer |
|---|---|---|
| `POST /actions/session/submit` | `{"branch": "…"}` | the `Submission` object, or a named refusal |
| `POST /actions/session/land-nonce` | `{"branch": "…"}` | `{"nonce": "…", "branch": "…", "head": "<40-hex>"}`: single-use, bound to that branch and head (OQ-12-13) |
| `POST /actions/session/land` | `{"branch": "…", "nonce": "…"}` | the `Landed` object, or a named refusal (the same refusals as the CLI) |

The hosted plane refuses all three by name and records nothing, as `submit`
already does there.

## `/capabilities`

| key | meaning |
|---|---|
| `session` (existing) | the submit control is offered (OQ-12-14: no new `actions.submit` key) |
| `actions.land` (new) | `true` only where a lander is bound for this repository (plan 034's T084 honesty rule); `false` under `unknown`, under `governed` with no instrument, and on the hosted plane |

## The view

The submit control and the land confirm control live in a new
`web/views/branch-actions.js`, never in the `doxbench-*.js` files FR-037's
sentinels guard (OQ-12-14). The confirm control fetches a nonce, shows the
branch and head it is bound to, and posts it once.

## F12.2's named nodes (unchanged; 12.6a)

`tests/test_submission_default.py` (2), `tests/test_submit_route.py` (5),
`tests/test_landing_guardrails.py` (13), all in openDox-code, run with `gh`
hidden from PATH (OQ-12-16).
