# Research: P3 — consume and shed

**Feature**: `023-openxwallet-consume-shed` · **Date**: 2026-08-27

Three questions had to be answered before a line was written, because a wrong
answer to any of them makes the pull request unmergeable rather than wrong.

## R1 — Can openxFactory Actions clone the private `opensoft/openXwallet`?

**Answered YES, with a correction to the design's literal secret names.**

`doc-health-reusable.yml:140-158` is the house pattern: mint an App token with
`actions/create-github-app-token@v2`, then
`git config --global url."https://x-access-token:$TOKEN@github.com/".insteadOf
"git@github.com:"` BEFORE checkout. That file names the org secrets
`XFACTORY_APP_ID` / `XFACTORY_APP_PRIVATE_KEY`.

Measured, as `brettheap` (org owner):

| Check | Result |
| --- | --- |
| `GET /orgs/opensoft/actions/secrets/XFACTORY_APP_ID` | `visibility: selected` |
| `GET /orgs/opensoft/actions/secrets/XFACTORY_APP_ID/repositories` | `opensoft/Omnigent-Install`, `opensoft/xFactory` — **openxFactory is NOT among them** |
| `GET /repos/opensoft/openxFactory/actions/secrets` | `OPENXFACTORY_APP_ID`, `OPENXFACTORY_APP_PRIVATE_KEY` |
| `GET /orgs/opensoft/installations` → installation `145372182` | App `4253636`, `repository_selection: all`, `contents: write` |
| `GET /repos/opensoft/openXwallet` | `private: true`, id `1347887821`, default `main` |

So: `secrets.XFACTORY_APP_ID` would resolve to EMPTY in an openxFactory workflow,
the token would silently fall back to `github.token`, and the nested clone would
fail with a 403 that reads like a missing submodule. The pattern is adopted; the
secret names used are this repository's own content-App pair, whose installation
already covers every repository in the organization — `repository_selection: all`
is the whole organization by GitHub's own semantics, private repositories
included.

**No installation edit was required, and none was made.** The authorized
`PUT /user/installations/145372182/repositories/1347887821` was NOT executed
because the installation is already org-wide; issuing it would have been a
no-op recorded as an operator act, which is worse than not issuing it. Recorded
in `evidence/operator-acts.md`.

`doc-health-reusable.yml` keeps `XFACTORY_APP_*` unchanged: that file is a
`workflow_call` reusable invoked from `opensoft/xFactory`, which IS one of the two
repositories the org secret is visible to.

## R2 — Is `wallet-v1.1` the commit the design names, and do the eight digests match?

**Answered YES, both directions, before the pin was written.**

`refs/tags/wallet-v1.1` is an ANNOTATED tag: object `021cdeef…`, whose
`object.sha` is `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705` — the commit design
D4 names. `git -C openXwallet describe --tags` returns `wallet-v1.1` at that
commit.

`sha256sum` over the eight members at `wallet-v1.1` equals, byte for byte, the
eight `sha256:` values `contracts/manifest.yaml` carried at `contract-v1.47`
(themselves unchanged since `contract-v1.31`):

| member | sha256 |
| --- | --- |
| `openxwallet-record.schema.yaml` | `2012ef43…b1d4eb08` |
| `openxwallet-custody-registry.schema.yaml` | `df726384…8ae3b51a` |
| `openxwallet-custody.registry.yaml` | `94d631d6…b5278539` |
| `openxwallet-grant.schema.yaml` | `fde433c5…8e738e88` |
| `openxwallet-grant-exercise.schema.yaml` | `f16ad312…113c8858` |
| `openxwallet-distinct-holder-constraint.schema.yaml` | `c2a6d2fd…82374b25` |
| `openxwallet-subject-attestation.schema.yaml` | `d29eca51…2bc0c0b2` |
| `openxwallet-agent-composition.schema.yaml` | `aed3978e…4de4be91` |

They were COPIED from the manifest rows, then independently recomputed against
the submodule by `scripts/verify-openxwallet-pin.py`, which is the check the gate
runs. Two derivations, one answer.

## R3 — Does the pinned `wallet-v1.1` reader actually open openxFactory's register?

**Answered YES, measured before the workflow was written**, because the whole
gate design rests on it:

```
note  nested repositories pruned (not adjudicated): openXwallet
note  intake register read: governance/review-authority/register.yaml (1 row(s))
note  repo scan: 2 openxWallet artifact(s) validated, 1612 document(s) skipped as another kind

validate-openxwallet: 0 error(s), 0 warning(s)
```

Both P2b additions are present and both matter here: the nested-repository prune
(without it the vendored family inside the gitlink would be re-adjudicated as
LIVE records of the scanned repository, inside a REQUIRED check) and the
`intake register read:` NOTE (which is what makes the gate's assertion POSITIVE
rather than an absence). The note is a NOTE and not a warning, which is why
LedgerxFactory's `--strict` run stays green.

The count moved 3 → 2 across the shed: openxFactory's own copy of
`openxwallet-custody.registry.yaml` was being adjudicated as a live record of the
scanned repository and is gone. The remaining two are the live grant and
attestation under `governance/review-authority/`, which is exactly the population
R6 keeps here.

## R4 — Which line of `tasks.md` 7.13/7.14 governs the invocation string?

7.13 fixes the step as `python3 openXwallet/scripts/validate-openxwallet.py . |
tee wallet-gate.log`; 7.14 requires one step's `run` to be EXACTLY `python3
openXwallet/scripts/validate-openxwallet.py .`, for the stated reason that the
argument be "present AND equal to `.`". Both are satisfied by pinning the whole
line exactly AND the command half exactly — a strictly stronger assertion than
either sentence alone, recorded in the test's own docstring so a later reader
does not re-open it. The `tee` is load-bearing: the POSITIVE register assertion
reads that log.

`shell: bash` is declared on that step because GitHub's default `run` shell does
not set `-o pipefail`, and without it `tee` returns 0 over a failing validator —
a gate that pipes its verdict into `tee` without pipefail is green whatever the
validator decided. A test asserts the declaration.
