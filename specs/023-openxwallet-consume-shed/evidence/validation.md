# Validation evidence — feature 023 (P3)

**Status**: record · **Date**: 2026-08-27 · **Branch**: `023-openxwallet-consume-shed`
**Pull request**: https://github.com/opensoft/openxFactory/pull/431
**Head at authoring**: rebased onto `origin/main` `94933adfcf993dbef2e74952662a3eb1281693e2`

## Local, at the rebased head

| # | Command | Result |
| --- | --- | --- |
| 1 | `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | **75 passed, 0 failed** (75 items) |
| 2 | `python3 scripts/verify-openxwallet-pin.py` | **exit 0** — `openXwallet@63f5a1adac89f017e70bab9a4ffe7cf02d6e6705 (tag label wallet-v1.1), gitlink read from HEAD, 8 digest(s) recomputed` |
| 3 | `python3 scripts/verify-openxwallet-pin.py --aggregation-root /home/brett/projects/xFactory` | **exit 2, `pin-member-missing`** — CORRECT: the aggregation carries no `openXwallet` gitlink until P4 |
| 4 | `python3 scripts/validate-trust-anchor.py .` | **exit 0**, `0 error(s), 0 warning(s)`, composition note names the path under `openXwallet/` |
| 5 | `python3 openXwallet/scripts/wallet-yaml-syntax-gate.py .` | **exit 0** |
| 6 | `python3 openXwallet/scripts/validate-openxwallet.py .` (the gate's exact command half) | **exit 0**, `0 error(s), 0 warning(s)` |
| 7 | the register conjunction over the captured log | **all four assertions hold** |
| 8 | `python3 -m pytest tests/openxwallet_pin/ -q` | **35 passed, 0 skipped** |
| 9 | `python3 -m pytest tests/trust-anchor/ -q` | **93 passed, 0 skipped** (83 failed / 4 passed before the repoint, which is the atomicity requirement made visible) |
| 10 | `python3 -m pytest tests/openxwallet_consumer_gate/ -q` | **14 passed, 0 skipped** |
| 11 | `python3 scripts/validate-contract-release.py build --tag contract-v2.0` | **192 entries**; a second build is byte-identical |
| 12 | `python3 scripts/validate-contract-release.py verify-tag --remote origin --tag contract-v1.47` | **`release verify-tag: pass`** — ticks `split-openxwallet-repo` 5.8 |
| 13 | `python3 scripts/doc-health.py --single-repo .` vs the SAME run on a throwaway `origin/main` worktree | **finding sets IDENTICAL: 65 = 65, zero new, zero resolved.** Headline both sides: 5 critical, 7 error, 41 warning, 12 info |
| 14 | grep for surviving `contracts/openxwallet/` references | only inside `openXwallet/` (the pinned submodule), `contracts/openxwallet-pin.yaml`, and two deliberate pin-relative citations (`scripts/validate-trust-anchor.py`, `contracts/manifest.yaml`) |
| 15 | `git diff --stat origin/main -- governance/` | **EMPTY** — §7.27, all four files untouched |

### The register conjunction, verbatim (#7)

```
note  nested repositories pruned (not adjudicated): openXwallet
note  intake register read: governance/review-authority/register.yaml (1 row(s))
note  repo scan: 2 openxWallet artifact(s) validated, 1612 document(s) skipped as another kind

validate-openxwallet: 0 error(s), 0 warning(s)
```

`repo scan:` present · `intake register read:` present · `no intake register at
this tree` ABSENT · no `[register-*]` code. The scan count moved 3 → 2 across the
shed: openxFactory's own copy of `openxwallet-custody.registry.yaml` was being
adjudicated as a live record of the scanned repository and is gone. The remaining
two are the live grant and attestation under `governance/review-authority/`, which
is exactly the population R6 keeps here.

### The eight digests, derived twice (#2)

Copied from `contracts/manifest.yaml`'s rows AND recomputed with `sha256sum`
against `openXwallet` at `wallet-v1.1`. They agree. The tag was resolved through
its ANNOTATED tag object (`021cdeef…` → `object.sha` `63f5a1ad…`) rather than
assumed to be lightweight.

### doc-health, the honest form of the claim (#13)

"No NEW findings" is asserted against a run of the SAME checker over
`origin/main` at `94933adf`, taken in a throwaway worktree and removed
afterwards — not against a stored report from an earlier session, whose baseline
had drifted (the `modified-block-currency` family landed on main in between, and
staged-topic ages advance daily). Normalised finding lines, sorted:
`comm -13` and `comm -23` both empty. `docs/archive-record-discrepancies.md`
already carried its `record-immutability` critical finding on `origin/main`, so
this feature's annotation of row 7 adds none.

## CI, on the pull request's own head

| Check | Run | Result |
| --- | --- | --- |
| `wallet-validation` (the required token, from the RENAMED file) | run **33109575651**, job **98648509131** | **PASS, 35s** — the ALIAS PROOF |
| `pytest-suite` | run **33109575624**, job **98648509080** | **FAIL — 2 failed, 7040 passed, 20 skipped, 338 deselected in 847s**, and both failures were the gate doing its job (below) |

### The alias proof, verbatim from run 33109575651

```
OK openxwallet-pin verified: openXwallet@63f5a1adac89f017e70bab9a4ffe7cf02d6e6705 (tag label wallet-v1.1), gitlink read from HEAD, 8 digest(s) recomputed
note  nested repositories pruned (not adjudicated): openXwallet
note  intake register read: governance/review-authority/register.yaml (1 row(s))
note  repo scan: 2 openxWallet artifact(s) validated, 1614 document(s) skipped as another kind
validate-openxwallet: 0 error(s), 0 warning(s)
register-read conjunction holds:
```

The required token `wallet-validation` reported GREEN on this pull request's own
head, produced by `.github/workflows/openxwallet-consumer-gate.yml`, with ruleset
21538893 edited by nothing. That is the entire alias resolution, proven rather
than argued.

### Ruleset 21538893, read 2026-08-27 — and one correction to the ratified wording

`GET repos/opensoft/openxFactory/rules/branches/main` returns, at ruleset_id
`21538893`: `required_status_checks: ["wallet-validation", "pytest-suite"]`,
`strict_required_status_checks_policy: false`.

`tasks.md` 7.31 asks for "the same SINGLE token as before the wave". **The set is
TWO**, and has been since an operator act OUTSIDE this wave marked `pytest-suite`
required. P3 changed NEITHER. Recorded rather than quietly satisfied: a row that
expects one token and is handed two should say so.

### Task 2.6's red-proof, RETARGETED — DISCHARGED (§7.32)

Draft pull request **#432**, branched from #431 so the gate under test is the one
P3 installs, carried ONE unknown field on the single register row.
`wallet-validation` went **RED** — run **33109857156**, job **98649492960**, 21s:

```
ERROR [register-row-malformed] /home/runner/work/openxFactory/openxFactory/governance/review-authority/register.yaml:rows[0]: field set mismatch (missing=[], unknown=['deliberately_malformed_probe']); the register has no schema so THIS reader is the shape, and it is strict
validate-openxwallet: 1 error(s), 0 warning(s)
```

The finding names the FULL PATH and came from the PINNED reader through the
renamed workflow — which the 2026-08-26 proof (PR #387, a malformed GRANT through
the OLD workflow) could not establish. Draft closed unmerged, its `pytest-suite`
run cancelled, scratch branch deleted local and remote — only that branch.
`git diff origin/main -- governance/` on this feature branch is EMPTY.

### The two CI failures, and why they were the RIGHT failures (run 33109575624)

`tests/doc-health/test_pin_reachability.py` — the derived-pin-reachability class
that landed on `main` in `govern-derived-pin-reachability` — refused
`contracts/openxwallet-pin.yaml` in BOTH directions, which is exactly the
coverage half of that obligation working on a new artifact:

1. `test_every_declared_repo_local_pin_in_this_repository_resolves` reported
   `contracts/openxwallet-pin.yaml:44 (commit) -> 63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`
   as an UNCOVERED site: a commit-shaped value in a swept artifact that no
   declared class member covers.
2. `test_every_committed_commit_shaped_value_that_resolves_is_covered` reported
   `contracts/openxwallet-pin.yaml carries commit 30565e48ffe3d8a9773e10af33425701845e10f6`
   — the CARVE COMMIT, which DOES resolve here and was likewise undeclared.

**Fix: two `PinMember` rows in `scripts/doc_health/pin_class.py`, not one.** This
is the first artifact in the repository that pins ANOTHER repository's bytes and,
in the same file, names the openxFactory commit those bytes were taken at, so the
two values have OPPOSITE localities and a single member could only have declared
one of them:

- `openxwallet-pin-carve-commit` — key `carve_commit`, **REPO_LOCAL**. It must
  stay reachable here: it is the byte-identity referent, and the claim that the
  move was byte-identical is checkable only while that commit can be
  reconstructed. `carve_commit` was a key the sweep vocabulary did not know;
  declaring the member teaches it, since `PIN_KEY_VOCABULARY` is the union of the
  declared field keys.
- `openxwallet-pin-product-commit` — key `commit`, **CROSS_REPOSITORY**. It is
  openXwallet's commit and must never be expected to resolve here; it is answered
  by that repository's authority and, locally, by
  `scripts/verify-openxwallet-pin.py`, which is a stronger guarantee than a local
  ref could give.

`python3 -m pytest tests/doc-health/test_pin_reachability.py -q` → **53 passed**
after the declaration. `contracts/releases/contract-v2.0.digests.yaml` is
unaffected (`scripts/doc_health/` is not an inventory member) and re-builds
byte-identical. `openspec validate --all --strict` → 76 passed.

### The triple, MEASURED IN CI and pinned (run 33111235491)

The workflow shipped with a sentinel and a step that FAILS LOUDLY printing the
actuals, because the self-skip guards ("no sibling openxFactory checkout", "no
aggregation checkout reachable from this tree") resolve differently in a developer
worktree that sits inside the aggregation than on a runner — the workflow header
has documented that two-skip difference since it was written. A wrong pin that
fails is correctable; a pin guessed from the wrong environment and passing is not
detectable at all.

Run **33111235491** printed, from the JUnit XML:

```
selected=7090 passed=7070 skipped=20 failures=0 errors=0
```

over a suite summary of `7042 passed, 20 skipped, 338 deselected, 7 warnings, 28
subtests passed in 866.19s`. Those three are now the pin: `EXPECT_SELECTED: 7090`,
`EXPECT_PASSED: 7070`, `EXPECT_SKIPPED: 20`.

**The arithmetic, recorded because it is not obvious**: pytest-subtests emits a
`<testcase>` per SUBTEST as well as per test, so `tests` = 7042 + 20 + 28 = 7090
and PASSED = 7090 − 20 = 7070, not 7042. The `-q` summary and the XML attributes
count different things. The XML is what is pinned, because the summary is a human
line whose format has changed before — and a pin taken from the wrong reading is
a pin that passes while measuring something else, which is the whole failure class
`tasks.md` 7.17 exists to close.

### AND WHY THE PIN'S SHAPE CHANGED — measured, on the next run

Run **33112622523**, on a head whose only diff from 33111235491's was the pin
values and two documents, reported `selected=7116 passed=7096 skipped=20`. **The
pull request added no test between the two runs.** A `pull_request` run builds a
MERGE of the head with `main`, so its totals carry every test `main` took in the
interval — 26 of them, in seventeen minutes.

An equality pin on SELECTED or PASSED is therefore a **deadlock on a REQUIRED
check**: it reds for merges the candidate cannot influence, which is the same
hazard `pytest-suite.yml`'s own "no paths filter" note refuses in the other
direction. So the three are checked in two shapes:

| number | shape | why |
| --- | --- | --- |
| SKIPPED | **exactly 20** | the load-bearing one. A directory that silently turns into skips MOVES it, and it does not drift with `main` — a merge adds passes, not skips |
| SELECTED | **floor 7090** | may only rise; the margin is printed every run |
| PASSED | **floor 7070** | as above. Both floors are the LOWER of the two measured runs, so each is a number this suite has actually met |
| FAILURES / ERRORS | **zero** | unchanged |

**The trade is stated rather than hidden**: a silent loss smaller than the day's
margin escapes the floor alone. It would still red on the exact SKIPPED pin if it
became skips, and on failures/errors if it became failures; the only shape that
escapes all three is a test that stops being COLLECTED while `main` adds at least
as many in the same window. Closing that needs per-directory counts — a successor,
not this change's scope. `tasks.md` 7.17 asked for a pinned triple; it gets three
checked numbers, with the one that actually detects the vacuous pass pinned
exactly.

**The nested submodule was genuinely initialized in that run** — "Mint
openxFactory app token", "Rewrite ssh submodule URLs for token auth" and "Init the
openXwallet gitlink only" each reported `success` as their own step, which is the
CI-side answer to the reachability question R1 asked.

## BOTH REQUIRED CHECKS GREEN — the final head

| Check | Run | Job | Result |
| --- | --- | --- | --- |
| `wallet-validation` | **33114027225** | 98663924186 | **PASS, 21s** |
| `pytest-suite` | **33114027245** | 98663924140 | **PASS, 13m39s** — `selected=7116 passed=7096 skipped=20 failures=0 errors=0`, both floors met with margin 26 |

`wallet-validation` reported GREEN on **four consecutive heads** of this pull
request (runs 33109575651, 33111235422, 33112622519, 33114027225), every one of
them produced by `.github/workflows/openxwallet-consumer-gate.yml` with ruleset
21538893 edited by nothing. **That is the alias proof, four times over.**

## Still owed — see `tasks.md` Phase 9 and `evidence/operator-acts.md`

§7.26 pre-merge rebase and digest RE-verification · §7.28/7.29/7.30 the green-run
evidence rows · §7.31 ruleset 21538893's unchanged state · §7.32 the retargeted
task-2.6 red-proof · §5.8-equivalent for `contract-v2.0`: the operator's tag ·
and the merge itself, **after P5a.2 lands**.
