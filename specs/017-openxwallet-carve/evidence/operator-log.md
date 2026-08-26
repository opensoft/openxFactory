# P2 operator log — feature 017-openxwallet-carve

**CARVE_COMMIT**: `30565e48ffe3d8a9773e10af33425701845e10f6`

## T001 — case-variant repository-name check (at create time)

```
gh repo view opensoft/openXwallet    -> GraphQL: Could not resolve to a Repository with the name 'opensoft/openXwallet'. (repository)
gh repo view opensoft/openxwallet    -> GraphQL: Could not resolve to a Repository with the name 'opensoft/openxwallet'. (repository)
gh repo view opensoft/OpenXWallet    -> GraphQL: Could not resolve to a Repository with the name 'opensoft/OpenXWallet'. (repository)
gh repo view opensoft/openXWallet    -> GraphQL: Could not resolve to a Repository with the name 'opensoft/openXWallet'. (repository)
gh repo view opensoft/OPENXWALLET    -> GraphQL: Could not resolve to a Repository with the name 'opensoft/OPENXWALLET'. (repository)
gh repo view opensoft/Openxwallet    -> GraphQL: Could not resolve to a Repository with the name 'opensoft/Openxwallet'. (repository)
gh repo view opensoft/openxWallet    -> GraphQL: Could not resolve to a Repository with the name 'opensoft/openxWallet'. (repository)
gh search repos openxwallet --owner opensoft ->
  (no rows = absent)
gh search repos openxwallet (unscoped, incl. forks) ->
  (no rows = absent)
```

**Result: ALL ABSENT.** No case variant of `openxwallet` exists in `opensoft`, and no repository of that name exists anywhere reachable by search. The carve may proceed.

## T002 — `git filter-repo` availability

```
$ git filter-repo --version
ed61b4050b71
```

Present on the host; **nothing was installed**. No `pip install --user git-filter-repo` or `pipx` path was taken.

## T003 — the frozen carve commit, and a main that moved under it

```
CARVE_COMMIT = 30565e48ffe3d8a9773e10af33425701845e10f6
  = "Merge pull request #396 from opensoft/016-openxwallet-split-bookkeeping"

origin/main at first resolve (2026-08-26):  30565e48ffe3d8a9773e10af33425701845e10f6
origin/main at carve time (re-fetched):     bb7d7ae813d3a8e1bfe62b859cf3c4a25f829def
```

**openxFactory's `main` MOVED between freezing the carve commit and taking the
carve** — six commits landed (PR #392, `change/model-provider-broker-build`).
This is precisely the hazard ratified task 3.3 exists to defeat: "Never 'HEAD',
which is no referent across a multi-PR wave." The carve commit stays
`30565e48`; it is not re-resolved, because re-resolving it is a ratified act
and not an implementation convenience.

**And the carve surface is untouched by the move**, which is checked rather than
assumed:

```
$ git diff --name-only 30565e48..origin/main -- <the twelve path sets>
(no output)
```

The six new commits touch `README.md`, `openspec/changes/add-model-provider-broker/`,
`openspec/changes/add-doxchat-model-intake/tasks.md`, `scripts/ideation_dashboard/`
and `tests/ideation-dashboard/` — none of the twelve sets. So the wallet content at
the frozen carve commit is byte-identical to the wallet content at the moved
`main`, and the carve loses nothing by being anchored where it is.

## T006–T008 — the cutover runbook, authored BEFORE the carve

`docs/openxwallet-cutover-runbook.md` was authored in staging and committed into
the carved repository by the scaffold, with:

- the six ordered phases from the proposal's cutover section;
- a **ROLLBACK written first in every phase**, before that phase's own steps;
- the NAMED CARVE COMMIT as a 40-hex literal, never "HEAD" — and a record of
  `main` moving under the wave, which is the reason the rule exists;
- the two-part byte-identity proof table shape (T008), filled by the proof run;
- **day-one REQUIRED recorded as impossible** (T007), not promised: GitHub cannot
  require a status check that has never reported, so no configuration makes the
  gate REQUIRED on creation day. The EVALUATE → report → ACTIVE sequence is the
  only path GitHub offers.

## T009 — the P2 rollback, recorded BEFORE Phase 3 began

**Nothing pins openXwallet yet.** The reversal is `gh repo delete
opensoft/openXwallet`, or simply leaving the repository unpinned. openxFactory is
untouched by P2 in either case: the carve COPIES, and P2 makes zero deletions in
openxFactory. Per-phase rollbacks are tabulated in the runbook's Phase 6.

---

## T035 — the six offline gates, at the pushed head

| Gate | Exit |
| --- | --- |
| `python3 scripts/verify-contract-pin.py` | **0** |
| `python3 scripts/wallet-yaml-syntax-gate.py .` | **0** |
| `python3 scripts/validate-openxwallet.py .` | **0** (0 errors, 0 warnings) |
| `python3 scripts/validate-openxwallet.py . --strict` | **0** |
| `python3 -m pytest tests/ -q` | **0** — **4 passed** (collection non-zero, so an empty suite is distinguishable from a passing one) |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | **0** — 2 passed, 0 failed |

The validator's notes at this tree:

```
note  approval-scope vocabulary read from contracts/schemas/hermes-job-envelope.schema.yaml:
      ['authority_agents_may_approve', 'hermes_approval_required_before_apply',
       'human_escalation_required_for']
note  corpus: 17 positive example(s), 36 negative confirmation(s) across 13/13 requirements
note  no intake register at this tree; nothing to read
```

The third note is CORRECT, not a gap: R6 keeps `governance/review-authority/` in
openxFactory and moves only its READER. openxFactory's consumer gate runs this
pinned reader over openxFactory's own tree by passing `.`, where the register does
resolve. And the second note is the validator independently confirming the
cross-family count of 36 negatives.

## T036 — the V8 RED proof, and the gap it demonstrates

```
$ printf '\n# deliberately mutated\n' >> contracts/schemas/hermes-job-envelope.schema.yaml
$ python3 scripts/verify-contract-pin.py
REFUSED contracts/schemas/hermes-job-envelope.schema.yaml: DIGEST DRIFT
          recorded   8ce2c89903a2f5a68ce3d73a7b8eb4f47cdef913da038b9a68e22735ee96cb7c
          recomputed d1a0a462c333ecfe6ba06632a1f400c638b2ccfe5372c62648df76aef0ba6a29
        the vendored copy is not the openxFactory artifact pinned at 30565e48…
  remediation: git submodule update --init openXwallet
  remediation: see docs/pin-resync-runbook.md
exit=1
```

Both remediation strings present (N1). Restored, verifier back to exit 0.

**And the gap the step closes, demonstrated rather than argued.** On the SAME
mutated tree:

```
$ python3 scripts/validate-openxwallet.py .
exit=0
```

The validator returns **zero** on a tampered vendored schema, because `main()`
checks only `ENVELOPE_SCHEMA_PATH.is_file()` — presence, not identity — while rule
(g) reads the approval-scope vocabulary out of that very file. Without the verify
step running FIRST, an unverified swap silently redefines the vocabulary the
REQUIRED gate enforces. This is the strongest available argument for the step's
position, and it is a measurement rather than a claim.

## T043–T045 — the operator acts

| Act | Result |
| --- | --- |
| repository created | **https://github.com/opensoft/openXwallet** — PRIVATE |
| description | `openXwallet — the neutral wallet standard: contracts, validator, corpus (split from openxFactory at 30565e48ffe3d8a9773e10af33425701845e10f6)` |
| `main` pushed | head `5c8d9aa428f7f0c7953336c4b03cd65dc29ef7af` |
| default branch | `main` |
| ruleset created | **21607344** — "openXwallet wallet-gate (require wallet-validation + pytest-suite)" |
| enforcement at creation | **`evaluate`** |
| required contexts | `wallet-validation`, `pytest-suite` |
| shape | `target: branch`, `ref_name.include: ["~DEFAULT_BRANCH"]`, `strict_required_status_checks_policy: false`, `do_not_enforce_on_create: false`, `bypass_actors: [OrganizationAdmin/always]` — mirroring openxFactory ruleset 21538893 |

**Why EVALUATE and not ACTIVE**: GitHub cannot require a status check that has
never reported in the repository — the context is not selectable. Day-one REQUIRED
is therefore **impossible**, recorded as unachievable rather than promised (task
3.25), and the EVALUATE → report → ACTIVE sequence is the only path GitHub offers.

**On requiring TWO tokens.** Task 3.27's evidence names
`required_status_checks → [wallet-validation]`. Ruleset 21538893 — the shape design
D8 says to mirror — requires **both** `wallet-validation` and `pytest-suite` as of
2026-08-26 17:39. Both are required here: that satisfies the named minimum and
mirrors the live precedent. Recorded as a choice, not absorbed as an assumption.

## T046 — the trivial bootstrap pull request

**https://github.com/opensoft/openXwallet/pull/1** — "Bootstrap the gate so both
checks become selectable". Touches `README.md` only, adding the record that
day-one REQUIRED is unachievable so a reader does not mistake the EVALUATE window
for an oversight.

## T047 — the V8 GREEN evidence: the verify ran BEFORE the validator

Run **33024308629** (`wallet-validation`, PR #1, conclusion `success`). Step order
proven by the runner's own timestamps, not by reading the YAML:

```
23:42:19.9757443  [Verify the vendored openxFactory artifact against contract_pin.yaml]
                  OK contracts/schemas/hermes-job-envelope.schema.yaml
                  sha256=8ce2c89903a2f5a68ce3d73a7b8eb4f47cdef913da038b9a68e22735ee96cb7c
23:42:19.9759224  OK contract pin verified: 1 vendored file(s) match contract_pin.yaml
                  at openxFactory@30565e48ffe3
23:42:19.9826055  [Run python3 scripts/wallet-yaml-syntax-gate.py .]
23:42:20.2282242  [Run python3 scripts/validate-openxwallet.py .]
23:42:20.7233661  note  approval-scope vocabulary read from
                        contracts/schemas/hermes-job-envelope.schema.yaml: [...]
23:42:20.7235465  note  corpus: 17 positive example(s), 36 negative confirmation(s)
                        across 13/13 requirements
23:42:20.7238223  validate-openxwallet: 0 error(s), 0 warning(s)
```

**The digest was verified 253 milliseconds before the validator started**, and the
validator's own next note is it reading the approval-scope vocabulary out of the
file that was just verified. That is the conjunction V8 asks for: the vendored
schema digest-verified against `contract_pin.yaml` BEFORE the validator ran.

Paired with T036's red run, the verifier is known both to pass and to REFUSE.

| Run | Check | Conclusion | Run id |
| --- | --- | --- | --- |
| PR #1 | `wallet-validation` | **success** | `33024308629` |
| PR #1 | `pytest-suite` | **success** | `33024308567` |

## T048–T049 — merge, then promote to ACTIVE

| Act | Result |
| --- | --- |
| PR #1 merged | merge commit `936ceb2066705d82fa60b333bea3babe6297a1b7`, 2026-08-26T23:43:24Z |
| ruleset 21607344 enforcement | `evaluate` → **`active`** |
| required contexts after promotion | `wallet-validation`, `pytest-suite` |

**A correction worth recording**: the ruleset update endpoint is **`PUT`**,
not `PATCH`. `gh api -X PATCH repos/.../rulesets/<id>` returns a **404** while
`GET` on the same path succeeds — a 404 that reads as "the ruleset does not
exist" when it actually means "that method does not exist here". `PUT` also
requires the COMPLETE ruleset body, not a partial patch.

### EVIDENCE — `GET repos/opensoft/openXwallet/rules/branches/main`

```json
[
    {
        "type": "non_fast_forward",
        "ruleset_source_type": "Organization",
        "ruleset_source": "opensoft",
        "ruleset_id": 8981805
    },
    {
        "type": "copilot_code_review",
        "parameters": {
            "review_on_push": true,
            "review_draft_pull_requests": true
        },
        "ruleset_source_type": "Organization",
        "ruleset_source": "opensoft",
        "ruleset_id": 8981805
    },
    {
        "type": "deletion",
        "ruleset_source_type": "Organization",
        "ruleset_source": "opensoft",
        "ruleset_id": 18834180
    },
    {
        "type": "non_fast_forward",
        "ruleset_source_type": "Organization",
        "ruleset_source": "opensoft",
        "ruleset_id": 18834180
    },
    {
        "type": "pull_request",
        "parameters": {
            "required_approving_review_count": 0,
            "dismiss_stale_reviews_on_push": true,
            "required_reviewers": [],
            "require_code_owner_review": true,
            "require_last_push_approval": false,
            "required_review_thread_resolution": false,
            "require_extra_approval_for_unattributed_changes": true,
            "allowed_merge_methods": [
                "merge",
                "squash",
                "rebase"
            ]
        },
        "ruleset_source_type": "Organization",
        "ruleset_source": "opensoft",
        "ruleset_id": 18834180
    },
    {
        "type": "required_status_checks",
        "parameters": {
            "strict_required_status_checks_policy": false,
            "do_not_enforce_on_create": false,
            "required_status_checks": [
                {
                    "context": "wallet-validation"
                },
                {
                    "context": "pytest-suite"
                }
            ]
        },
        "ruleset_source_type": "Repository",
        "ruleset_source": "opensoft/openXwallet",
        "ruleset_id": 21607344
    }
]
```

## T050 — `wallet-v1.0`, tagged only after the proof

The proof was **re-verified at the tag head** (`936ceb20`, the merge commit),
not just at the pre-push head, because the tag names that commit and a proof taken
elsewhere is a proof about elsewhere:

| Assertion at the tag head | Result |
| --- | --- |
| pin verify | exit **0** |
| part one — the eight digests, three-way | **8/8** |
| part two — git blob + mode identity over the 100 carved paths | **97/100** |
| the 3 that differ | the 2 promoted specs + `.github/workflows/wallet-validation.yml` — all enumerated |

```
tag object : de74c8ccf10dee4f36bd69cd7162f04cea569167  (annotated)
targets    : 936ceb2066705d82fa60b333bea3babe6297a1b7  (main)
message    : wallet-v1.0 — byte-identical carve of
             openxFactory@30565e48ffe3d8a9773e10af33425701845e10f6
```

## T051 — the check state on `main`, stated accurately

`gh run list --branch main` returns **`[]`**, and main's head carries no
check-runs. **This is correct, not a gap.** Both workflows trigger on
`pull_request` → `main` — the shape carried from openxFactory by the carve — so
the checks run on a pull request's head, which is exactly what a
`required_status_checks` ruleset gates. There is no `push` trigger to produce a
run on `main` itself, and adding one would be a change to a carved file outside
what P2 authorizes.

The P2 realization evidence is therefore the pull request's runs, which is what
the ratified table asks for ("first green `wallet-validation`", "first green
`pytest-suite`"):

| Realization row | Green check | Run id | Paired evidence |
| --- | --- | --- | --- |
| P2 — carve + scaffold | `wallet-validation` | **33024308629** | the carve-completeness check: 100/100, empty listing diff, `specs/006-openxwallet-contracts/evidence/` and both `examples/negative/` trees named explicitly |
| P2 — runnable half | `pytest-suite` | **33024308567** | the byte-identity proof of the eight rows against the NAMED CARVE COMMIT: 8/8 |
| P2 — vendored-schema verify (V8) | `wallet-validation` | **33024308629** | the log line at `23:42:19.9757` showing the digest verified 253 ms BEFORE the validator started, PLUS the red run refusing a mutated copy with both remediation lines |
