# Operator acts — feature 023 (P3)

**Status**: record

## App-installation reachability: NO ACT TAKEN, and why that is the right answer

**Authorization held.** Brett's "lets do all 3 of these now" authorized adding
`opensoft/openXwallet` to the App installation the consumer gate mints from, if
one was needed.

**Measured first, as `brettheap` (organization owner), 2026-08-27:**

```
GET /orgs/opensoft/installations
  → id=145372182  app_slug=openxfactory  app_id=4253636
    repository_selection=all
    permissions={contents: write, metadata: read, pull_requests: write, …}

GET /repos/opensoft/openXwallet
  → id=1347887821  private=true  default_branch=main

GET /repos/opensoft/openxFactory/actions/secrets
  → OPENXFACTORY_APP_ID, OPENXFACTORY_APP_PRIVATE_KEY

GET /orgs/opensoft/actions/secrets/XFACTORY_APP_ID
  → visibility=selected
GET /orgs/opensoft/actions/secrets/XFACTORY_APP_ID/repositories
  → opensoft/Omnigent-Install, opensoft/xFactory        # NOT openxFactory
```

**Conclusion: `PUT /user/installations/145372182/repositories/1347887821` was NOT
issued.** Installation `145372182` carries `repository_selection: all`, which is
GitHub's own term for every repository in the organization, private repositories
included. The `PUT` endpoint is for `selected`-scope installations; against an
`all`-scope installation it either errors or is a no-op. Issuing it anyway would
have produced an operator-act record describing a change that did not happen,
which is worse for the audit trail than the absence of a record.

**What DID change as a result of the measurement**: the consumer gate and
`pytest-suite` mint from `OPENXFACTORY_APP_ID` / `OPENXFACTORY_APP_PRIVATE_KEY`
rather than from the `XFACTORY_APP_*` names `doc-health-reusable.yml` uses. Had
the design's literal secret names been copied, `secrets.XFACTORY_APP_ID` would
have resolved to EMPTY in an openxFactory workflow, `create-github-app-token`
would have failed or the token expression would have fallen back to
`github.token`, and the nested clone would have failed with a 403 that reads like
a missing submodule. The PATTERN is the ratified one; only the secret names are
this repository's own.

`doc-health-reusable.yml` keeps `XFACTORY_APP_*` unchanged: it is a
`workflow_call` reusable invoked from `opensoft/xFactory`, which IS one of the two
repositories that org secret is visible to. Whether the App behind
`XFACTORY_APP_*` reaches openXwallet is P4's question, not this feature's — and
the second scoped init this feature adds there is guarded so it cannot fail the
nightly before P4 lands.

## Acts still owed by the operator

| # | Act | Why it is not automatable |
| --- | --- | --- |
| §7.31 | Record ruleset 21538893's UNCHANGED state from `GET repos/opensoft/openxFactory/rules/branches/main` | a repository setting is not a tree fact and no merge commit records it |
| §7.32 | The task-2.6 red-proof against the consumer gate | it requires opening a deliberately-red pull request and closing it |
| §7.26 | Rebase and RE-VERIFY the eight digests immediately before merge | the shared-tree freeze is unenforceable, so the re-verification must be the last thing before the merge |
| §5.8 / §7 | Cut the `contract-v2.0` annotated tag on the merged commit | `contract-v1.44`/`v1.45`/`v1.47` are all operator-cut annotated tags; no workflow makes them |
| — | THE MERGE, after P5a.2 lands | `tasks.md` §6 — the deprecation window must be OBSERVED by the one live consumer first |

## §5.8 discharged in part

`contract-v1.47` was cut by the operator on `af7ac0fa4d31ffeec45524a0fe74524ba5b5b22c`
(2026-08-27) and `python3 scripts/validate-contract-release.py verify-tag --remote
origin --tag contract-v1.47` returns `release verify-tag: pass`. The P2.5 bundle
is therefore PUBLISHED, which is the precondition
`docs/contract-versioning-policy.md:31-32` states for this major existing at all.
`split-openxwallet-repo` `tasks.md` 5.8 is ticked on that evidence.
