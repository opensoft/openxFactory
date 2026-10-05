# Contract: `submit` and `land`, CLI and HTTP

Status: draft

**Feature**: 038 · **Authority**: boxes 12.1–12.4a, 12.6, 12.6a; answers R2Q1–R2Q7,
R2Q9 (a) item 7 (`--local`). **A PROPOSAL until Brett rules the plan**
(OQ-12-9, -11, -12, -13, -14, -17; OQ-038-1; decisions N-1, N-2, N-11, N-16,
N-17; tier 2's CF-1). Review round 1 corrected the command shapes to the ratified ones (ADV-01).

Both verbs, their routes and their capability flags are contributions of
openDox's DEFAULT profile (decision N-2; ADV-14): the verbs through
`SUBCOMMAND_EXTENSIONS`, the routes through `ROUTE_EXTENSIONS` and
`HANDLER_CONTRIBUTIONS`. A host profile that replaces the default carries none
of them in release 2 (R2Q3 (a)), so its parser, its routes and its
`/capabilities` payload are unchanged. Under openDox's own profile they behave
the same in every governance mode (tier 2's CF-1).

## `opendox submit`

```text
opendox submit --repo-root PATH --branch BRANCH [--local] [--json]
```

This is 12.4a's ratified shape (`submit --repo-root <repo> --branch
<session-branch>`, #1144 `tasks.md:2536-2537`), which F12.2 runs as `opendox submit
--repo-root "$W/plain" --branch sess-1` (`:2834`). Options follow the verb (10.1).

- Pushes `BRANCH` through `SubmissionPort` (the bound `submission_factory` /
  `_submission_port`; `LocalGitSubmissions` by default, R2Q2 (a)) to the remote
  named `origin`, else the sole remote (ADV-26). Prints the `Submission` report
  (data-model.md), `--json` as an object.
- **Install mode.** The CLI verb does not depend on the install mode: it pushes
  the invoking user's own checkout with the user's own git, which a hosted
  plane never holds (ADV-04; `runtime/config.py:1954-1996`'s default is hosted).
  `--local` is accepted, and refused only where it DISAGREES with
  `OPENDOX_INSTALL_MODE=hosted`, naming both (R2Q9 (a) item 7; FR-004). F12.2
  runs it with neither, and passes.
- Runs as the invoking user, in that user's checkout, with no console-presence
  or `--actor` gate (OQ-12-9).
- **Refuses by name** (exit non-zero, nothing pushed, message redacted):
  `BRANCH` is `main`; no remote, or several remotes and none named `origin`
  (`NoSubmissionTarget`, 12.3, raised); the chosen remote has several push URLs
  (`SubmissionRefused`). A remote whose URL carries a credential is PUSHED, and
  the report and every message are redacted (12.1a; ADV-09).
- Never calls `gh` (12.4; F12.2 runs with `gh` absent).
- Under `governed`, `submit` goes through the host's contributed
  `SubmissionPort` (the instrument) when one is bound; the report names where
  the work went (R2Q4 (a)).

## `opendox land`

```text
opendox land --repo-root PATH --branch BRANCH [--local] [--json]
```

12.6a's ratified shape (`land --repo-root <repo> --branch <session-branch>`,
`tasks.md:2814-2815`), interactive by construction.

- Asks for confirmation over `/dev/tty`, naming the branch and its head; the
  answer mints the confirmation capability (12.6a). With no `/dev/tty`, it
  refuses, naming the missing terminal; there is no bypass flag (decision N-11;
  12.6a: "refuses when there is none").
- `standalone` (which needs the explicit local install, `OPENDOX_INSTALL_MODE=local`
  or `--local`; FR-007): merges `--no-ff` in its own landing worktree, then
  fast-forwards the served checkout when it holds `main` and is clean (R2Q6 (a)).
  Prints `Landed`, with the `git revert -m 1 <merge_commit>` that undoes it.
  Pushes nothing; a landed `main` leaves the checkout only by the user's own
  `git push`.
- `governed` with an instrument: submits through it and reports where the work
  went; the merge stays the governance's act (R2Q4 (a)).
- **Refuses by name**: `unknown` (no `main`, naming it; no declaration, naming
  the exact file `.opendox/governance.yaml` and the content to commit, R2Q7
  (a)); `governed-without-an-instrument`; `BRANCH` is `main`; the served
  checkout holds `main` and is not clean (ADV-08), naming the remedy; local
  `main` lacks the remote's `main` tip (`ls-remote refs/heads/main`; a remote with
  no `main` passes); a stale or used confirmation; a conflict (`MergeConflict`,
  naming the paths and the remedy: bring `main` into the branch and resolve
  there, OQ-038-1).
- Serves the fix loop's drafts unchanged, the batch draft included: a batch is
  one branch (OQ-12-17).

## HTTP routes (loopback server; 12.4a's three-clause gate and the console token on all three)

| method and path | body | answer |
|---|---|---|
| `POST /actions/session/submit` | `{"branch": "…"}` | the `Submission` object, or a named refusal |
| `POST /actions/session/land-nonce` | `{"branch": "…"}` | `{"nonce": "…", "branch": "…", "head": "<40-hex>"}`: single-use, bound to that branch and head (OQ-12-13) |
| `POST /actions/session/land` | `{"branch": "…", "nonce": "…"}` | the `Landed` object, or a named refusal (the same refusals as the CLI) |

The routes take no repository from the request (12.4a; F12.2's
`test_submit_route_takes_no_repository_from_the_request`). The hosted plane
refuses all three by name and records nothing: the hosted refusal is the
ROUTE's (ADV-04).

## `/capabilities`

The two keys exist ONLY where openDox's default profile contributes their routes,
derived from the route bindings as `gate` is (`serve.py:509-526`,
`answers_a_gate_verb`; plan 034 T084's rule that a flag whose affordance is a
route this server serves is true only where such a route answers). A host that
replaces the default sees neither key, so its payload is byte-for-byte what it
was (T019, T064). No openxFactory test pins the `actions` key set (measured by
grep over `tests/`; research R13), so the derivation is what keeps "unchanged"
true, not a test's tolerance.

| key | meaning |
|---|---|
| `actions.submit` | present under openDox's profile; `true` where the submit route answers and the plane is a local human's (loopback, a real checkout, a resolved actor) |
| `actions.land` | present under openDox's profile; `true` only where a lander is bound for this repository; `false` under `unknown`, under `governed` with no instrument, and on the hosted plane |

`session` keeps its meaning (the core session routes); the submit control keys
on `actions.submit`, never on `session`, so it cannot be offered where no submit
route answers (OQ-12-14, refined by ADV-14).

## The view

The submit control and the land confirm control live in a new
`web/views/branch-actions.js`, never in the `doxbench-*.js` files FR-037's
sentinels guard (OQ-12-14). The confirm control fetches a nonce, shows the
branch and head it is bound to, and posts it once.

## F12.2's named nodes (unchanged; 12.6a)

`tests/test_submission_default.py` (2), `tests/test_submit_route.py` (5),
`tests/test_landing_guardrails.py` (13), all in openDox-code, run with `gh`
hidden from PATH (OQ-12-16). T012 adds, beside the thirteen, nodes for R2Q7
(a)'s two refusals (no `main`; no declaration) and ADV-08's dirty-checkout
refusal.
