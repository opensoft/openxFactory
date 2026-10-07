# Analyze, round 1: the Opus review of `6d6911e1`

Status: record

**Feature**: [`038-opendox-document-tool-self-maintenance`](../spec.md) ·
**Reviewed**: plan 038 at `6d6911e1`, draft PR #1245 · **Run**: 2026-10-05,
read-only, by an independent Opus reviewer the holder dispatched (the plan
writer did not run it) · **Folded in**: the revision that commits this file ·
**Lane**: `openxfactory-4`

This note is bookkeeping, so it carries no `Arc:` trailer (R1Q20 (a),
`5817152735`). T003's round 2 is a separate, later pass ([`tasks.md`](../tasks.md)).

## Verdict

The reviewer's verdict, verbatim: **"READY after the listed fixes. It is not
ready for Brett's ruling at `6d6911e1`."**

The adversarial pass found 3 CRITICAL, 10 HIGH, 15 MEDIUM and 13 LOW findings
(ADV-01 to ADV-41). The `speckit-analyze` table found 1 CRITICAL, 9 HIGH, 9
MEDIUM and 6 LOW (D1, F1–F10, C1–C6, E1–E4, A1–A2, B1–B2), most of them the
same defects seen through the skill's rubric. Every row is dispositioned below.

The holder (lane `openxfactory-4`) ruled how each item is resolved: conform to
ratified text wherever a conforming route exists, so that what reaches Brett is
short. On those rulings this revision:

- **applies** 60 of the 66 rows; four of them (ADV-09, ADV-10, ADV-11 and
  ADV-16, with their analyze twins F3 and F9) by conforming to ratified text
  where the reviewer offered Brett a choice or a confirmation;
- **leaves 2 unchanged** that the reviewer itself called acceptable (A2, B2);
- **puts 4 to Brett**: ADV-20 (tier 1's ARC-5), ADV-25 (tier 1's N-6), ADV-15
  (tier 2's CF-5) and B1 (tier 2's CF-1);
- **disagrees with none of the 66 findings**. It disagrees with one measured
  cite in the review's § 4.6 (item 3), and corrects a second (item 22); both are
  in § "The review's measured claims" below.

## How the review was run, and how this revision checked it

The reviewer worked read-only in the assigned worktree at `6d6911e1` and in
clones of every product repository, each still at research R0's `main`
(openDox-code `a9ac96f9`, openXdox-code `56e1c238`, openDox `d77f8cbf`,
openDox-spec `f7ee3c76`, codexFactory `972bb6f6`). Its own account is the first
block of the verbatim text below.

The plan writer re-measured each claim before applying it, in its own clones
(openDox-code `a9ac96f9`, openXdox-code `56e1c238`, both still `main`) and in
this branch's worktree. The decisive commands and their output:

    $ git -C openDox-code rev-parse --short=8 HEAD
    a9ac96f9
    $ grep -n 'THE DEFAULT IS HOSTED\|return raw or INSTALL_MODE_HOSTED' src/opendox/runtime/config.py
    1958:    THE DEFAULT IS HOSTED, and it is the default because it is the safe one
    1996:    return raw or INSTALL_MODE_HOSTED
    $ grep -n '^ *commit:' src/opendox/contracts/copies.yaml
    32:commit: "f7ee3c763b3af4581daf1cd54406e5111e9358e6"
    $ grep -n 'SPEC_COMMIT\b\|PINNED_BY_THE_ROOT' tests/test_validator_input_set.py   (excerpt)
    66:SPEC_COMMIT = "f7ee3c763b3af4581daf1cd54406e5111e9358e6"
    74:PINNED_BY_THE_ROOT = {
    103:    assert record.commit == SPEC_COMMIT, (
    116:        assert copy.sha256 == PINNED_BY_THE_ROOT[copy.id], (
    $ grep -n 'def answers_a_gate_verb\|def compute_capabilities' src/opendox/serve.py
    509:def answers_a_gate_verb(binding) -> bool:
    536:def compute_capabilities(*, nlm_present: bool, checkout_real: bool, loopback: bool,
    $ grep -n '^DEFAULT_SCOPED_FAMILIES\|def register_health_check\|def run_scoped_doc_health\|already registered' src/opendox/workbench.py
    1557:DEFAULT_SCOPED_FAMILIES = ("status-validity", "tag-hygiene")
    1622:def register_health_check(check: Callable[..., HealthCheckRun]
    1646:            "a health check is already registered at openDox's health-check "
    1666:def run_scoped_doc_health(
    $ grep -n '^_EXECUTED_LOCAL_KEYS\|def _refuse_repository_local_command_config\|def _bound_local_destination\|def _receive_pack_for\|def _push_to_remote_with\|def refuse_credential_bearing_remote' src/opendox/runtime/repository_act.py
    203:def refuse_credential_bearing_remote(remote_url: str) -> None:
    1335:_EXECUTED_LOCAL_KEYS = ("credential.helper", "core.gitProxy", "core.sshCommand",
    1372:def _refuse_repository_local_command_config(git: GitRunner, location: Any) -> None:
    1613:def _bound_local_destination(destination: str | None, location: Any, *,
    1720:def _receive_pack_for(destination: str | None, location: Any) -> str:
    1742:def _push_to_remote_with(git: GitRunner, row: Any) -> str:
    $ sed -n 560,564p tests/test_session_git.py
            assert allowed in sg.SERVED_ALLOWED_SUBCOMMANDS, allowed
        for refused in sg.FORBIDDEN_SERVED_SUBCOMMANDS:
            assert refused not in sg.SERVED_ALLOWED_SUBCOMMANDS
        for refused in ("add", "commit", "merge", "clean", "update-ref", "rm", "mv"):
            assert refused not in sg.SERVED_ALLOWED_SUBCOMMANDS

    $ git -C openXdox-code rev-parse --short=8 HEAD
    56e1c238
    $ grep -n 'spec_leg\|^commit' src/openxdox/contracts/copies.yaml   (excerpt)
    32:spec_leg: opensoft/openXdox-spec
    33:commit: "f088b09732e236279898b53ab9fb0f5ebc89509a"
    $ sed -n 81,83p tests/test_packaged_validator.py
    def test_the_copies_are_the_validators_own_three_kinds():
        """The record's three are the validator's `OWN_KIND_SCHEMAS`, and each copy
        declares the kind its id names, so no fourth kind rides in as a copy."""
    $ sed -n 642,643p src/openxdox/gate_console.py; sed -n 665p …; sed -n 711p …
        schema_path = (Path(__file__).resolve().parents[2] / "contracts" / "schemas"
                       / schema_filename)
            record, schema_filename="gate-action-record.schema.yaml",
            receipt, schema_filename="demotion-execution-receipt.schema.yaml",

    $ T=openspec/changes/add-neutral-product-standalone-operability/tasks.md   (this worktree)
    $ sed -n 2834p $T; sed -n 2848p $T; sed -n 3253p $T
          opendox submit --repo-root "$W/plain" --branch sess-1 > "$W/submit.out"
          assert r is not None and r.ref.endswith("sess-1") and str(W / "remote") in r.url, r
      | `health fix` | `health fix --repo-root <corpus> --finding ID [--batch]` |
    $ sed -n 3503,3525p $T | grep -o 'fixture-[a-z]*-pack' | sort -u
    fixture-anonymous-pack fixture-crashing-pack fixture-escaping-pack fixture-forking-pack
    fixture-garbage-pack fixture-patching-pack fixture-slow-pack fixture-writing-pack
    $ grep -n '65,536' $T
    3473:  than the engine's bound, 65,536 bytes by default (the order of the server's own
    $ ls scripts/ideation_dashboard/__init__.py
    ls: cannot access 'scripts/ideation_dashboard/__init__.py': No such file or directory

No openxFactory test pins the `/capabilities` `actions` key set (ADV-14's
check). `grep -rn` for `"actions"` over this worktree's `tests/` finds only
per-key reads (`tests/ideation-dashboard/test_intent_feed.py:533-589`,
`test_gate_routes.py:192-212`, `test_intent_plane_boundary.py:532-536`,
`test_doxbench_routes.py:673`, `:692`), and a search for a set or equality
assertion over the map (`set(caps`, `actions"].keys`, `capabilities ==`) finds
none.

## Findings, and what this revision does with each

"Applied" means this revision makes the fix; "conformed" means the reviewer
offered Brett a choice and the holder took the route that conforms to ratified
text, so no question is put. Tier numbers refer to plan.md § "Design decisions
for Brett to rule with this plan". Paths are this feature directory's.

### The `speckit-analyze` table

| ID | sev | finding | disposition | where |
|---|---|---|---|---|
| D1 | CRITICAL (skill) | The planning documents are not linked in the README index (Principle IV). | Applied. The feature's entry links plan, research, data model, contracts, quickstart, tasks and both round-1 evidence files; every evidence task now carries README upkeep. Conflict C-17 is marked FIXED. | openxFactory `README.md:87`; tasks.md § Format ("README"); plan.md C-17 |
| F1 | HIGH | `submit <branch>` and `land <branch>` are positional; 12.4a, 12.6a and F12.2 use `--repo-root … --branch …`. | Applied, as ADV-01. | contracts/cli-http-submit-land.md; T015, T016 |
| F2 | HIGH | `Submission` lacks `ref` and `url`. | Applied, as ADV-02. | data-model.md § Submission; T011 |
| F3 | HIGH | `health fix` drops 14.5's `[--batch]`. | Applied, as ADV-11 (conformed). | contracts/cli-http-health.md; tier 3 N-19; T046 |
| F4 | HIGH | A patch may be whole replacement text. | Applied, as ADV-12. | data-model.md § Patch; T049 |
| F5 | HIGH | T055's packs are not 15.6a's eight. | Applied, as ADV-03. | T055 |
| F6 | HIGH | ARC-6 (a) makes T061 wait on the arc's ratify word. | Applied, as ADV-06. | tier 3 ARC-6; T061, T072 |
| F7 | HIGH | `left` moves `main` under a dirty served checkout. | Applied, as ADV-08. | data-model.md § The landing's states; T012 |
| F8 | MEDIUM | The spec's "gate-action record schema" and T021's openxFactory receipt are different schemas. | Applied. The spec names both schemas the gate console reads (`gate_console.py:642-643`, `:665`, `:711`): openXdox-spec's gate-action record, already packaged, and openxFactory's demotion-execution receipt, from a schema source the host registers. | spec.md FR-005's repair means and § Assumptions; T021; tier 3 P4F-4 |
| F9 | MEDIUM | N-10 removes R2Q12 (a)'s working-state runs. | Applied, as ADV-16 (conformed). | data-model.md § Health run; tier 3 N-10, N-14 |
| F10 | MEDIUM | The falsifier map claims batch Q gives F12.2 `--local`. | Applied. The claim is dropped: F12.2 runs as ratified, and batch Q item 1 says so. | tasks.md § Falsifier mapping (F12.2 row); T005 item 1 |
| C1 | HIGH | The CLI `submit`'s behaviour with no install mode is unstated; the default is hosted. | Applied, as ADV-04. | tier 3 N-17; contracts/cli-http-submit-land.md § `opendox submit`; T015; conflict C-21 |
| C2 | HIGH | The finding id's locator serialization is unstated. | Applied, as ADV-07. | contracts/health-finding.md § The id rule; tier 3 N-13 |
| C3 | MEDIUM | Empty stubs must be `assisted`; no proposal defined. | Applied, as ADV-17. | data-model.md § Families; tier 3 OQ-H-8, OQ-H-11; T043, T044, T053 |
| C4 | MEDIUM | The uncommitted-exception reading is deferred and never stated. | Applied. New default N-14: an uncommitted exception suppresses only in a working-state run. | tier 3 N-14; contracts/health-exceptions.md |
| C5 | LOW | 15.6's default timeout has no number; "stale stub" has no criterion. | Applied, as ADV-40. | tier 3 OQ-H15-5 (60 s, cap 600); data-model.md § Families; conflict C-20 |
| C6 | LOW | The `ls-remote` check's ref and its empty-remote behaviour are unstated. | Applied. New default N-16: it reads `refs/heads/main`; an absent branch, or no remote, passes. | tier 3 N-16; T012; contracts/cli-http-submit-land.md |
| E1 | HIGH | No task runs F15.1's shell block with a live sandbox. | Applied, as ADV-13. | T067; plan.md single-writer row for `validate.yml`; tier 3 N-4 |
| E2 | MEDIUM | R2Q9 items 4 and 6 sit in the runner task, not the fixture task. | Applied, as ADV-22. | T055, T056 |
| E3 | LOW | T018 omits R2Q6 (a)'s two push routes. | Applied, as ADV-30. | T018 |
| E4 | LOW | Evidence files are never linked in the README. | Applied, as ADV-34. | tasks.md § Format; each evidence task's README line |
| A1 | LOW | Rows 34/49 and 37/55/62 split one question each. | Applied, as ADV-35. | tier 1 ARC-5; tier 2 CF-2 |
| A2 | LOW | FR-006 and FR-007 overlap on the guardrails. | No change: the reviewer called it acceptable. | none |
| B1 | LOW | R2Q1 (a)'s "every mode" is read through I-1. | To Brett, as a reading to confirm. | tier 2 CF-1 |
| B2 | LOW | The near-duplicate threshold is left to measurement. | No change: the reviewer called it acceptable as planned; T044 measures and records it. | tier 3 OQ-H-21 |

### The adversarial findings

| ID | sev | finding | disposition | where |
|---|---|---|---|---|
| ADV-01 | CRITICAL | Positional branch arguments contradict 12.4a, 12.6a and F12.2. | Applied: `opendox submit --repo-root PATH --branch BRANCH [--local] [--json]`, and `land` the same. Verified at #1144 `tasks.md:2536-2537`, `:2814-2815`, `:2834`. | contracts/cli-http-submit-land.md; T015, T016; quickstart.md § 3 |
| ADV-02 | CRITICAL | `Submission` has no `ref` or `url`; F12.2 asserts both. | Applied: fields `branch`, `remote`, `ref`, `url` (redacted), `commit`. A refused or failed push RAISES (`NoSubmissionTarget`, FR-002; `SubmissionRefused` otherwise); nothing returns a failure value. Verified at `:2848`. | data-model.md § Submission; contracts/cli-http-submit-land.md; T011 |
| ADV-03 | CRITICAL | T055's packs are not 15.6a's eight. | Applied: the eight by exact name; the escaping pack also hunts the CANARY variable and the CANARY descriptor through `/proc/self/fd` and follows a planted symlink; R2Q9 items 4 and 6 moved here. The canary's definition is corrected to match. Verified at `:3503-3525`. | T055; data-model.md § Sandbox probe and canary; contracts/health-packs-manifest.md |
| ADV-04 | HIGH | A CLI `submit` that refuses on the hosted default fails F12.2. | Applied: the CLI `submit` does not read the install mode; only `--local` disagreeing with `OPENDOX_INSTALL_MODE=hosted` refuses; the hosted refusal applies to the route. The false falsifier-map claim is dropped (F10). Verified: `install_mode` returns hosted by default (`config.py:1954-1996`). | tier 3 N-17; conflict C-21; contracts/cli-http-submit-land.md; T015 |
| ADV-05 | HIGH | Copying before the root's spec pin breaks openDox-code's copy-record invariants; T047 and T054 race; no cut word. | Applied: T060 (the root's spec pin, the manifest and the `dox-v1.2` cut, on Brett's cut word, asked for in T060 itself) moves to straight after T040; T041 → T047 → T054 then copy at the commit the root pins, in that fixed order; the copy record, `schemas/`, `contracts/__init__.py` and `tests/test_validator_input_set.py` join the single-writer table and each task's Files. Verified: one `commit:` (`copies.yaml:32`), and the test's `SPEC_COMMIT` and `PINNED_BY_THE_ROOT` asserts (`:66`, `:74`, `:103`, `:116`). | T060, T041, T047, T054; plan.md single-writer table and critical path |
| ADV-06 | HIGH | ARC-6 (a) puts the arc on release 2's cut, against ARC-Q3 (a). | Applied: T072 is opportunistic; T061 never waits for T071 or T072; a late T072 rides the arc's own pin. | tier 3 ARC-6; T061, T072, T074 |
| ADV-07 | HIGH | The id hashes line numbers, so it is not stable. | Applied: the id hashes a position-independent identity key the family supplies, in canonical sorted-key JSON, with `pack_id`, `kind` and `path`; line ranges are display-only. Stated as a conforming refinement of R2Q10 (a)'s "a locator the family supplies". | contracts/health-finding.md § The id rule; data-model.md § Finding; tier 3 N-13; T041 |
| ADV-08 | HIGH | `left` moves `main` under a dirty served checkout. | Applied: a served checkout that holds `main` and is not clean is refused before merging, naming the remedy; `left` only for a served checkout on another branch; a test node in T012. | data-model.md § The landing's states; T012 (`test_a_dirty_served_checkout_on_main_is_refused_before_merging`); contracts/cli-http-submit-land.md § `opendox land` |
| ADV-09 | HIGH | Refusing a credential-bearing remote narrows 12.1a. | Conformed: such a remote is pushed, and the report and every message are redacted, as 12.1a designs. No question for Brett. | tier 3 OQ-12-11; data-model.md § Submission; T011 |
| ADV-10 | HIGH | Vendoring openxFactory's receipt schema into openXdox-code conflicts with `neutral-product-pin`, 7.1 and R1Q27 (a). | Conformed: nothing is vendored into openXdox-code's single-source copy record. `gate-action-record` is read from openXdox-code's own package; the receipt from a schema source the host registers (the composed conftest, then host wiring at T030); the runbook is placed from the composed tree. No question for Brett. Verified: `copies.yaml:32-33`, `test_packaged_validator.py:81-92`, `gate_console.py:642-643`. | tier 3 P4F-3, P4F-4; T021, T022, T030; conflict C-19; § Complexity Tracking |
| ADV-11 | HIGH | `health fix` drops `[--batch]`. | Conformed: `health fix --repo-root <corpus> --finding ID [--batch]` exactly as 14.5 declares; `--class` added to `list` only. Verified at `:3253`. | contracts/cli-http-health.md § CLI; tier 3 N-19; T046 |
| ADV-12 | HIGH | Whole-text patches contradict 15.2 and 15.2a. | Applied: unified diffs only; T049 carries 15.2a's full refusal list and the 65,536-byte bound (`:3473`). | data-model.md § Patch; T049; spec.md FR-018 unchanged |
| ADV-13 | HIGH | Nothing runs F15.1's shell block where a sandbox is live. | Applied: new CI-owner task T067, after T058 and before T065, adds F15.1's shell block as a step of the required job on `ubuntu-24.04` with bubblewrap; it joins `validate.yml`'s single-writer chain. | T067; plan.md single-writer table; tier 3 N-4; critical path |
| ADV-14 | MEDIUM | Core routes and `/capabilities` keys would change every host's payload. | Applied, with one addition: the routes and their flags are default-profile contributions, derived from route bindings as `gate` is (`serve.py:509`), so a host profile's payload is unchanged. The addition: `actions.submit` is a new route-derived key, because `session` alone would offer a submit control where no submit route answers. Checked: no openxFactory test pins the `actions` key set. | tier 3 OQ-12-14, N-2; contracts/cli-http-submit-land.md § `/capabilities`; contracts/cli-http-health.md; T015, T016, T057, T019, T064 |
| ADV-15 | MEDIUM | Batch Q item 3's "until the direction arc's realization lands" would expire F12.1's composed line. | To Brett, as a reading to confirm: "F12.1 runs composed; ARC-Q2 (a) makes the composition its permanent home". | tier 2 CF-5; T005 item 3 |
| ADV-16 | MEDIUM | N-10 narrows R2Q12 (a); the uncommitted-exception reading is unstated. | Conformed: runs at the tip, on a branch and over the working state are all supported; only default-tip runs form the baseline or measure disappearance. N-14 states the uncommitted-exception reading. | data-model.md § Health run; tier 3 N-10, N-14; T046 |
| ADV-17 | MEDIUM | Empty stubs are ratified `assisted`, with no proposal or fixture. | Applied: an empty stub is `assisted`, with a deterministic proposal; one is planted in 14.9's fixture and tested in T044 and T053; the stub criteria are declared. | data-model.md § Families; tier 3 OQ-H-8, OQ-H-11; T043, T044, T053 |
| ADV-18 | MEDIUM | An unconditional registration collides with openxFactory's `register_health_check`. | Applied: openDox's own check registers only when the scoped seam is empty; a host's check wins (R2Q16 (a)); both registration orders tested. Verified: `workbench.py:1622-1651`. | tier 3 OQ-H-3; T052; contracts/cli-http-health.md § The scoped seam |
| ADV-19 | MEDIUM | T074 retargets to seams the host registers only at T075. | Applied: until T075, T074's composed conftest registers the governed implementations from the composed `scripts/`. | T074; plan.md single-writer row for openXdox-code `tests/conftest.py` |
| ADV-20 | MEDIUM | Ticking F9.2 inside an archived #1144 is covered by no rule. | To Brett, merged into tier 1's ARC-5 with lane 3's MISLABEL row 49. The writer's wording: F9.2's later closure is recorded in the arc change's own evidence (T076); the archived `tasks.md` is never edited. | tier 1 ARC-5; T076; conflict C-6 |
| ADV-21 | MEDIUM | A git-URL pack source names no transport hardening. | Applied: `https://` or `ssh://` only; `file://`, `ext::`, local paths and credential URLs refused; the runtime's hardened transport rules reused (`repository_act.py:1335`, `:1372`). | tier 3 OQ-H15-14; contracts/health-packs-manifest.md § Rules; T047 |
| ADV-22 | MEDIUM | T048 measures bounds before the pack corpus exists; items 4 and 6 are fixture behaviour. | Applied: the bound measurement moves to T056; items 4 and 6 move to T055. | T048, T055, T056; tier 3 OQ-H15-5 |
| ADV-23 | MEDIUM | Single-writer table gaps and missing orders. | Applied: rows added for openDox-code's copy record (and `test_validator_input_set.py`), `session_pr.py`, `runtime/repository_act.py`, `pyproject.toml`, openXdox-code `tests/composed_host_pin.yaml` and the README entry; `serve.py` ordered T052 → T057; openXdox-code's copy record has NO writer (ADV-10). After lines: T017 After T010; T057 After T052; T050 After T045; T055 After T048; T012 After T011 (`session_pr.py`, `repository_act.py`); the `health_contract.py` hand-off T041 → T045 named. A chain check (each listed order against the After lines) reports no unordered pair. | plan.md § Parallel slices and cross-lane hand-offs; the named tasks' After and Files lines |
| ADV-24 | MEDIUM | Batch Q item 4 misses literal ids beyond selection lines. | Applied: item 4 enumerates every literal-id use in F14.1 and F15.1 by line, `x['id'] == 'broken-link'`, the `refused_patch` values, `--finding patch-*` and `refs/heads/health-fix-patch-ok` among them. | T005 item 4; tier 2 CF-2 item 4; conflict C-8 |
| ADV-25 | MEDIUM | N-6 changes the ruled release map's build order. | To Brett, as a tier 1 ruling with options. | tier 1 N-6 |
| ADV-26 | MEDIUM | "origin only" refuses a sole remote of another name. | Applied in the holder's conforming form rather than the review's relabel: `origin`, else the sole remote; several remotes and no `origin` refuse by name. "A remote attached" holds for a sole remote of any name. | tier 3 OQ-12-12; data-model.md § Submission; T011 |
| ADV-27 | MEDIUM | `message` is unbounded and may quote the document. | Applied: `message` is bounded like `evidence` (200 characters) and never quotes document text. | contracts/health-finding.md § Shape and § Rules; quickstart.md § 3 |
| ADV-28 | MEDIUM | README index omits the plan documents. | Applied, as D1. | openxFactory `README.md:87` |
| ADV-29 | LOW | `workbench.py:1542-1557` is `DEFAULT_SCOPED_FAMILIES`, not the seam. | Applied: `run_scoped_doc_health` `:1666`, registration `:1622`; `:1542-1557` named as the constant's block. | T052; research.md; conflict C-9 |
| ADV-30 | LOW | T018 omits R2Q6 (a)'s README push routes. | Applied. | T018 |
| ADV-31 | LOW | `SERVER` is never assigned; "packs live (CI)" is false for `acceptance`. | Applied: `SERVER=$!` with a `trap`; `caps.health.packs` is recorded, not asserted, because the acceptance job is not a provisioned sandbox host. | quickstart.md § 3, § 5 |
| ADV-32 | LOW | C-1 says the spec is not this plan's to edit. | Applied: `spec.md` now reads 11 files and 5 green suites (210 cases); C-1 is marked FIXED. | spec.md § Assumptions; plan.md C-1 |
| ADV-33 | LOW | Phase 5's stated critical path is wrong and omits the pack track. | Applied: two poles, health and packs, joining at T061; T060 (Brett's cut word) on both. Marked inferred. | plan.md § The critical path |
| ADV-34 | LOW | No task links evidence in the README. | Applied, as E4. | tasks.md § Format; each evidence task |
| ADV-35 | LOW | Rows to merge, split or drop. | Applied: rows 34 and 49 → tier 1 ARC-5; rows 37, 55 and 62 → tier 2 CF-2; row 59 (N-9) is a record; row 57 split into N-7a (the file layout) and N-7b (the required-check act: the holder adds `composed` after T029's first green run on `main`, recorded in T029's evidence). | plan.md § Design decisions (preamble, tiers 1–3) |
| ADV-36 | LOW | Session worktrees are siblings; only `merge --ff-only` at the served root needs the new check. | Applied. Verified: `session_git.py:250-263`. | T013 |
| ADV-37 | LOW | The arc's own trailer removes T075's edits from F11.1's guard. | Applied: an equivalent surfaces check over the arc's own landings, quoted in T075 and T077. | tier 3 ARC-4; T075, T077 |
| ADV-38 | LOW | `--local` must count as the same selection as the setting. | Applied. | spec.md FR-007 (`standalone`); data-model.md § Governance; T012 |
| ADV-39 | LOW | The shim's directory must not add an `__init__.py`. | Applied. Verified: openxFactory's `scripts/ideation_dashboard/__init__.py` does not exist. | tier 2 CF-3; T024; plan.md single-writer table |
| ADV-40 | LOW | Declare 15.6's default timeout and the stale-stub criterion. | Applied: 60 seconds per pack, capped at 600, engine-owned; stub criteria in the data model. | tier 3 OQ-H15-5; data-model.md § Families; conflict C-20 |
| ADV-41 | LOW | T008 names neither codexFactory's required checks nor its review lane (inferred). | Applied, and measured: `gh api repos/codeXfactory/codexFactory/rules/branches/main` gives required checks `validate` and `lane-line`, one approving review, Copilot code review, merge commits only. | tier 3 N-8; T008; research.md R13 |

### The review's other sections

| where | item | disposition |
|---|---|---|
| § 4.1 | Every file two tasks write, with its order | Applied through ADV-23. T025's Files now name `tests/test_web_boundary.py`. |
| § 4.2 | N-4's "before any slice adds a test" is encoded nowhere | Applied: the claim is gone; N-4 now states the CI-owner chain, and T048 (the first sandbox test) is After T010. |
| § 4.3 | Row 26 applies `sorted-ls-tree-r-v1` to a tree-ish; "say so in the contract" | Applied: tier 3 OQ-H15-12 and contracts/health-packs-manifest.md state the reading. |
| § 4.4 | C-1 to C-17 | Confirmed by the reviewer; C-1 and C-17 are FIXED in this revision; C-18 to C-21 added. |
| § 4.5 | C-6 and C-14 coherent readings | C-6: adopted as tier 1's ARC-5 (a), with ADV-20's record. C-14: the reviewer reads I-2 as needing no ruling, since F14.1 passes either way; the holder put I-2 to Brett as a tier 1 ruling on lane 3's MISLABEL row 36, recommending (a), "the baseline branch is `main`, else the branch HEAD names". Both readings are recorded at C-14. AT-R2's `-b main` stands. |
| § 4.6 item 3 | "`:564` holds the `merge` absence loop; its assertion is at `:565`" | **Disagreed.** `sed -n 560,564p tests/test_session_git.py` at `a9ac96f9` (above) shows the loop at `:563` and its assertion at `:564`. The plan's `:563-564` stands (T013). |
| § 4.6 item 22 | "`config.py:1954` reads 'THE DEFAULT IS HOSTED'" | Corrected, not disputed: `:1954` opens `install_mode`; the words are at `:1958` and the default return at `:1996`. The plan now cites `:1954-1996`. |
| header | the spec writer's tree at `dede32b4` | No action: the plan cites none of it. |

## The checks after the dispositions

Run over this revision before it was pushed, and quoted in the PR:
the feature's self-check (every FR, SC, R2Q, ARC-Q and release-2 box mapped to
a task; no dependency cycle), the single-writer chain check (every order in
plan.md's table encoded in an After line), the pinned OpenSpec gate
(`python3 scripts/validate-openspec-cli-pin.py --all`), and the closing-keyword
and host-path scans.

**A note on the verbatim text.** Two of its lines name local paths, and are
kept as written: the reviewer's clone location, relative to its own home
directory, and the four path prefixes its host-path scan searched for. Neither
is a path this repository depends on.

## Next

T003's round 2 runs over this revision. Brett rules the three tiers at T004.

## The review, verbatim

Saved by the reviewer at the lane's work directory as
`review-038-6d6911e1-opus.md` (449 lines); quoted here unchanged, as a block.

> **Review of feature 038 (release 2 plan) at `6d6911e1`, draft PR opensoft/openxFactory#1245**
>
> The plan is not ready for Brett's ruling as it stands. It is ready after the listed fixes, almost all of which are the plan writer's. I made no edits, commits, pushes or posts. One side effect: I ran a `git fetch origin main` in the assigned worktree's clone, which moved its FETCH_HEAD and remote-tracking ref only.
>
> - **Worktree check:** `git rev-parse --short=8 HEAD` gives `6d6911e1`. `git status --porcelain` is empty. The PR is OPEN, draft, head `6d6911e1`.
> - **Clones:** the brief's remote form `ssh://git@ssh.github.com:443/...` failed with "Host key verification failed". I cloned over `git@github.com:` into `~/.local/state/R2-review/{openDox-code,openXdox-code,openDox,openDox-spec,codexFactory}`. Every `main` still equals research R0: `a9ac96f9`, `56e1c238`, `d77f8cbf`, `f7ee3c76`, `972bb6f6`.
> - **openxFactory `main`:** now `ba89e046`. It is one commit past `0f2a87f6` (#1209), and that commit touches none of #1144, `README.md` or feature 038.
> - **Spec writer's tree:** its `openDox/code` is at `dede32b4`, not `a9ac96f9`, so I did not cite from it.
> - **Not done:** I ran no tests, and did not re-measure the 174 composed reds (so C-1's 10-versus-11 files is unverified by me).
> - **Read in full:** the feature directory (spec, plan, research, data-model, quickstart, tasks, all contracts, clarify-questions, checklist), R2-ARC-ASK.md and the constitution.
> - **Read in part:** for #1144 I read its release map, Groups 6, 9, 11, 12, 14 and 15, requirements 6, 11, 14, 15 and 16 of its spec delta, and `design.md` §§ D9–D13. I did not read the bodies of release 1's ticked groups. For plan 034 I read `plan.md` § Ruled answers and R1Q4–R1Q7 of `clarify-questions.md`.
>
> ## 1. Summary
>
> | | CRITICAL | HIGH | MEDIUM | LOW | total |
> |---|---|---|---|---|---|
> | Adversarial findings (the brief's rubric) | 3 | 10 | 15 | 13 | 41 |
> | `speckit-analyze` table (the skill's rubric) | 1 | 9 | 9 | 6 | 25 |
>
> The three CRITICAL findings are all quick wording fixes. Each is a design artifact that, followed as written, produces something #1144's ratified falsifiers reject:
> - the `submit` and `land` command shapes in `contracts/cli-http-submit-land.md`;
> - the `Submission` fields in `data-model.md`;
> - T055's list of fixture packs.
>
> Of the ten HIGH findings, three need Brett, or a relabel into a question for him: OQ-12-11, P4F-4, and the `--batch` change to `health fix`. The other seven are the plan writer's fixes.
>
> ## 2. `speckit-analyze` findings
>
> Paths are under `specs/038-opendox-document-tool-self-maintenance/` unless they say otherwise. `C1144` means `openspec/changes/add-neutral-product-standalone-operability/`.
>
> | ID | Category | Severity | Location(s) | Summary | Recommendation |
> |---|---|---|---|---|---|
> | D1 | Constitution IV | CRITICAL (skill rubric) | `README.md:87`; `plan.md:138` | The new plan documents (plan, research, data-model, quickstart, tasks) are not linked in the README index, which Principle IV requires ("MUST be linked"). T004 tracks it. | Add the links before the PR leaves draft (T004), as the plan says. |
> | F1 | Inconsistency | HIGH | `contracts/cli-http-submit-land.md:17,38` against `spec.md:596-598,694`; `C1144/tasks.md:2536-2537,2814-2815,2834` | The contract's `opendox submit <branch>` and `opendox land <branch>` take a positional branch. Ratified 12.4a and 12.6a, F12.2 and FR-004/FR-007 all use `--branch`. | Use the `--repo-root ... --branch ...` form. |
> | F2 | Inconsistency | HIGH | `data-model.md:20-27` against `spec.md:565-568`; `C1144/tasks.md:2848` | `Submission` has no `ref` or `url` (it has `destination` instead). F12.2 asserts `r.ref` and `r.url`. | Restore `remote`, `ref` and `url` (redacted). |
> | F3 | Inconsistency | HIGH | `contracts/cli-http-health.md:19` against `spec.md:831`; `C1144/tasks.md:3253` | `health fix` drops the ratified `[--batch]` flag and makes `--finding` repeatable. | Conform to 14.5, or put it to Brett. |
> | F4 | Inconsistency | HIGH | `data-model.md:187` against `spec.md:965-966`; `C1144/tasks.md:3459-3464` | A patch's `content` may be "the replacement document text". 15.2 and 15.2a allow unified-diff patches only. | Allow unified diffs only. |
> | F5 | Inconsistency | HIGH | `tasks.md:762-765` against `spec.md:998-1003`; `C1144/tasks.md:3503-3525` | T055's list of fixture packs is not 15.6a's eight. | Copy 15.6a's eight names exactly. |
> | F6 | Inconsistency | HIGH | `plan.md:581`; `tasks.md:840-841` against `plan.md:497` | ARC-6 (a) makes T061 wait for T072, which waits for T071. The plan's own ARC-Q3 row says the arc gates nothing. | Make T072 opportunistic. |
> | F7 | Inconsistency | HIGH | `data-model.md:79,93-94` against `spec.md:706-713` | The landing state `left` moves `main` under a dirty served checkout that holds `main`. | Refuse in that case. |
> | F8 | Terminology | MEDIUM | `spec.md:642,1196` against `tasks.md:391-394`; `plan.md:569` | The spec says "gate-action record schema" (openXdox-spec's, already copied). T021 says the openxFactory-owned `demotion-execution-receipt`. | Name the one schema. |
> | F9 | Inconsistency | MEDIUM | `plan.md:596` against `clarify-questions.md:591-593` | N-10 removes the "working state" runs that R2Q12 (a) names. | State it, and have Brett confirm. |
> | F10 | Inconsistency | MEDIUM | `tasks.md:1108` against `tasks.md:108-137` | The falsifier map says batch Q amends F12.2 with `--local`. Neither T005's item list nor R2Q9 (a) does. | See ADV-04. |
> | C1 | Underspecification | HIGH | `tasks.md:295-296`; `spec.md:608-610` | What the CLI `submit` does with no install mode is unstated. The shipped default is hosted. | See ADV-04. |
> | C2 | Underspecification | HIGH | `contracts/health-finding.md:23,28`; `plan.md:599` | The finding id hashes a line-bearing locator. Its canonical serialization is unstated. | See ADV-07. |
> | C3 | Underspecification | MEDIUM | `plan.md:526,528` against `C1144/tasks.md:3274-3278` | Empty stubs must be `assisted`; no class or proposal is defined for them. | See ADV-17. |
> | C4 | Underspecification | MEDIUM | `spec.md:534-536` | The spec defers the uncommitted-exception reading to the plan. The plan never states it. | State it. |
> | C5 | Underspecification | LOW | `contracts/health-packs-manifest.md:27`; `C1144/tasks.md:3496` | 15.6's per-pack default timeout is not declared as a number. "Stale stub" has no criterion. | Declare both. |
> | C6 | Underspecification | LOW | `data-model.md:90`; `quickstart.md:102` | The `ls-remote` check's behaviour on an empty remote, and which ref it reads, are unstated. | Read `refs/heads/main`; absent passes. |
> | E1 | Coverage (SC-002) | HIGH | `tasks.md:813-822,869-874` | No task runs F15.1's shell block where a sandbox is live. | See ADV-13. |
> | E2 | Coverage (R2Q9 items 4, 6) | MEDIUM | `tasks.md:674-676` against `tasks.md:762-765` | Two fixture properties are assigned to the runner task (T048), not the fixture task (T055). | Move them to T055. |
> | E3 | Coverage (FR-007, last bullet) | LOW | `tasks.md:346-353` | T018 omits the README's two push routes that R2Q6 (a) requires. | Add them to T018. |
> | E4 | Coverage (Principle IV, evidence) | LOW | `tasks.md:87-91,518-538,869-879` | Evidence files are never linked in the README index. Plan 034 did link its evidence. | Add README upkeep to the evidence tasks. |
> | A1 | Duplication | LOW | `plan.md:550` and `:580`; `:558`, `:591` and `:598` | Rows 34 and 49 split one archive question. Rows 37, 55 and 62 split batch Q's contents. | Merge them. |
> | A2 | Duplication | LOW | `spec.md:648-654` and `:655-738` | FR-006 and FR-007 overlap on the guardrails. | Acceptable. |
> | B1 | Ambiguity | LOW | `plan.md:556`; `spec.md:600-601` | R2Q1 (a)'s "every mode" is read through I-1. | Brett rules I-1. |
> | B2 | Ambiguity | LOW | `plan.md:535` | The near-duplicate threshold is left to measurement. | Acceptable as planned. |
>
> **Coverage summary** (from `tasks.md:1114-1170`, checked against the task bodies):
>
> | Requirement | Has task? | Task IDs | Notes |
> |---|---|---|---|
> | FR-001 | yes | T011 | The data-model drops `ref` and `url` (F2). |
> | FR-002 | yes | T011 | |
> | FR-003 | yes | T014, T019, T005 | |
> | FR-004 | yes | T015, T016, T019 | The command shape conflicts with the contract (F1). Behaviour with no install mode is unstated (C1). |
> | FR-005 | yes | T020–T029, T032, T063, T005 | Batch Q's time limit conflicts with ARC-Q2 (ADV-15). |
> | FR-006 | yes | T012, T016 | |
> | FR-007 | yes | T008, T012, T013, T016, T018, T031 | The `left` state (F7). The README routes (E3). |
> | FR-008 | yes | T044, T052, T065 | T052 must not break the one-check seam (ADV-18). |
> | FR-009 | yes | T042 | |
> | FR-010 | yes | T044, T046 | N-10 (F9). Empty stubs (C3). |
> | FR-011 | yes | T046, T057 | `--batch` (F3). |
> | FR-012 | yes | T041, T053 | Empty stubs (C3). |
> | FR-013 | yes | T053 | |
> | FR-014 | yes | T054, T040 | Uncommitted exception (C4). |
> | FR-015 | yes | T043, T065, T005 | |
> | FR-016 | yes | T040, T045, T047 | Copy ordering (ADV-05). |
> | FR-017 | yes | T010, T048 | |
> | FR-018 | yes | T041, T045, T049 | Patch content (F4). |
> | FR-019 | yes | T050, T056 | |
> | FR-020 | yes | T010, T048, T055, T056, T058 | T055 (F5). No live-sandbox run of F15.1's shell block (E1). |
> | FR-021 | yes | T042, T047, T056 | |
> | FR-022 | yes | T091–T093, T082 | |
> | FR-023 | yes | T060, T061, T084, T090, T083 | Ordering (ADV-05). |
> | FR-024 | yes | T080, T081 | |
> | FR-025 | yes | T004, T005 | |
> | SC-001 | yes | T031–T033 | |
> | SC-002 | yes | T065, T066 | Not reachable as scheduled (E1). |
> | SC-003 | yes | T032, T065, T093 | |
> | SC-004 | yes | T082 | |
> | SC-005 | yes | T010, T017, T051, T030, T064, T075 | |
> | SC-006 | yes | T011, T016, T057, T042, T054, T048 | |
> | SC-007 | yes | T012, T013, T016 | |
> | SC-008 | yes | T080, T081 | |
>
> **Constitution alignment:** D1, above. Every file carries `Status: draft`. No committed file contains a host path (a grep for `/home/`, `/workspace/`, `/Users/` and `/tmp/` across the feature directory found nothing).
>
> **Unmapped tasks:** none that matter. T001–T004, T006, T007 and T009 are holder or process tasks under FR-025.
>
> **Metrics:**
> - Requirements: 33 (25 FRs and 8 SCs).
> - Tasks: 77 (2 done).
> - Coverage: 100% (33 of 33 have at least one task).
> - Ambiguities: 2.
> - Duplications: 2.
> - CRITICAL findings: 1 under the skill's rubric, 3 under the brief's.
>
> **Next actions:** fix the CRITICAL and HIGH findings before T004 puts the plan to Brett; there is no `/speckit-implement` until then. Remediation edits for the top issues are in § 3.
>
> **Extension hooks:** `before_analyze` and `after_analyze` each hold one optional hook, `speckit.git.commit` ("Commit outstanding changes before analysis?" and "Commit analysis results?"). I did not run either, because this review is read-only.
>
> ## 3. Adversarial findings
>
> "Writer" means the fix belongs to the plan writer. "Brett" means it needs his ruling.
>
> ### CRITICAL
>
> - **ADV-01**
>   - **Where:** `contracts/cli-http-submit-land.md:17` (`opendox submit <branch>`) and `:38` (`opendox land <branch>`). `tasks.md:298` makes this contract "the surface" for T015.
>   - **What and why:** a positional branch argument contradicts ratified 12.4a and 12.6a (`C1144/tasks.md:2536-2537`, `:2814-2815`: `--branch <session-branch>`), FR-004/FR-007, and F12.2's own command (`C1144/tasks.md:2834`: `opendox submit --repo-root "$W/plain" --branch sess-1`). Built as written, F12.2 fails on argument parsing. If Brett rules the contract as written, the plan contradicts ratified text.
>   - **Fix:** `opendox submit --repo-root PATH --branch BRANCH [--local] [--json]`, and the same shape for `land`. **Writer.**
>
> - **ADV-02**
>   - **Where:** `data-model.md:20-27`.
>   - **What and why:** `Submission` has `branch`, `remote`, `destination`, `commit`, `outcome` and `message`, with no `ref` and no `url`. FR-001 (`spec.md:565-568`) and 12.1a (`C1144/tasks.md:2476-2484`) require `remote`, `ref` and `url`. F12.2 asserts `r.ref.endswith("sess-1") and str(W / "remote") in r.url` (`C1144/tasks.md:2848`). T011 builds "the report (data-model.md § Submission)", so it would fail F12.2 with an AttributeError.
>   - **Fix:** fields `remote`, `ref`, `url` (redacted), plus whatever else is wanted. Also settle whether a refused or failed push returns or raises: FR-002 says `NoSubmissionTarget` raises. **Writer.**
>
> - **ADV-03**
>   - **Where:** `tasks.md:762-765` (T055).
>   - **What and why:** T055's packs are "a well-behaved pack, and one each that writes, connects, reads outside the export, forks, hangs, babbles, crashes and tries a restore". 15.6a's eight are `fixture-crashing-pack`, `-slow-`, `-writing-`, `-escaping-`, `-forking-`, `-garbage-`, `-anonymous-` and `-patching-pack` (`C1144/tasks.md:3503-3525`). T055 has no anonymous pack and no patching pack (the one with six findings), and it splits the escaping pack in three. F15.1 asserts these by name (`:3582-3586`, `:3595-3611`), so T055 cannot realize 15.6a as written.
>   - **Fix:** list 15.6a's eight by their exact names. Carry R2Q9 (a) items 4 and 6 here (see ADV-22). **Writer.**
>
> ### HIGH
>
> - **ADV-04**
>   - **Where:** `tasks.md:295-296` (T015: "The hosted plane refuses by name"); `tasks.md:1108`; `spec.md:608-610`.
>   - **What and why:** openDox-code `runtime/config.py:1954` reads "THE DEFAULT IS HOSTED … an install that sets nothing is hosted" and ends `return raw or INSTALL_MODE_HOSTED`. F12.2 runs `opendox submit` with neither `--local` nor `OPENDOX_INSTALL_MODE`. If the CLI verb consults the install mode and refuses on hosted, F12.2 fails. `tasks.md:1108` claims batch Q item 1 amends F12.2 with `--local`. But R2Q9 (a) item 7 amends verb shapes only, and names F14.1 and F15.1, not F12.2. T005's items (`tasks.md:111-137`) do not include it either.
>   - **Fix:** state that the CLI `submit` is independent of install mode, and only a disagreement between flag and setting refuses. The hosted refusal applies to the route. Drop the falsifier-map claim. **Writer.** It needs Brett only if F12.2 is to be amended instead.
>
> - **ADV-05**
>   - **Where:** `tasks.md:566-578` (T041), `:657-668` (T047), `:748-761` (T054) and `:826-835` (T060). The single-writer table at `plan.md:292-325` omits the files involved.
>   - **What and why, ordering:** openDox-code's copy record `src/opendox/contracts/copies.yaml` holds one `commit:` (`f7ee3c76…`). `tests/test_validator_input_set.py:97-121` asserts `record.commit == SPEC_COMMIT` and that each digest equals `PINNED_BY_THE_ROOT`. `:148-160` asserts `set(THE_FOUR) == entries == on_disk == set(contracts.record().ids)`. Batch G's ratified 7.1 rule is "a test holds each copy to the spec-leg commit the openDox root pins". Release 1 therefore moved the root's spec pin and cut the bundle first (034 T053), and copied after (T057 After T053). This plan copies first (T041, T047, T054) and moves the root's spec pin later (T060 After the copies). T041 cannot add a copy to the existing record without breaking these invariants or editing unlisted files.
>   - **What and why, cross-lane writers:** `copies.yaml` and `tests/test_validator_input_set.py` are written by T041 (lane 4), T047 (lane 3) and T054 (lane 4), and nothing orders T047 against T054. That refutes the claim of no concurrent cross-lane writers.
>   - **What and why, cut word:** release 1's bundle was cut by Brett (RULED `5894235642`). T060 names no cut word.
>   - **Fix:** split T060. Move the spec pin, the manifest and the `dox-v1.y` cut (on Brett's cut word) to straight after T040. Then make T041, then T047, then T054 copy at the commit the root pins, and add both files to the single-writer table in that order. The alternative is a separate copy record for the health schemas, stated as such. **Writer, plus Brett's cut word.**
>
> - **ADV-06**
>   - **Where:** `plan.md:581` (row 50, ARC-6); `tasks.md:840-841`; `tasks.md:906-914`.
>   - **What and why:** under ARC-6 (a), T061 (the 0.2.0 bump) is After T072, which is After T071, Brett's ratify word on the arc's own change. That puts the arc on release 2's cut, against ARC-Q3 (a) (`6003918488`: "gates neither release 2's close nor #1144's archive"). A recommended default contradicts a ruling.
>   - **Fix:** "T072 rides T061 only if it has already landed; T061 never waits for it." **Writer.**
>
> - **ADV-07**
>   - **Where:** `plan.md:599` (N-13); `contracts/health-finding.md:23,28,54`; `data-model.md:122`.
>   - **What and why:** the id is SHA-256 over `pack_id`, `kind`, `path` and a `locator` that carries `line_start` and `line_end`, and the locator's serialization (an object) is unspecified. Any edit above a finding moves its lines, which changes the id. The baseline then sees a new finding plus an uncited disappearance, re-raised as `human-only` (R2Q12 (a)). An exception keyed by the old id silently stops suppressing. This defeats R2Q10 (a)'s "STABLE" and requirement 15's "cite what it is accepting". F14.1 does not catch it, because nothing moves between its accept and its re-run.
>   - **Fix:** separate an identity key the family supplies and that does not depend on position (a link target, a pair of paths, a heading key) from display locators. Hash only the identity key, in a canonical form such as sorted-key JSON. **Writer.** Brett confirms the reading of R2Q10's "locator".
>
> - **ADV-08**
>   - **Where:** `data-model.md:79` (`left` (it did not; the user's `main` ref still moved)) and `:93-94`.
>   - **What and why:** when the served checkout holds `main` and is dirty, moving `main` moves that checkout's `HEAD` under its index and working tree. Feature 007's SC-002 forbids that, and R2Q6 (a) admits only "`merge --ff-only` … only when that checkout is clean". FR-007 is silent on this case, and the data-model settles it unsafely.
>   - **Fix:** if the served checkout holds `main` and is not clean, refuse before merging, naming the remedy. Keep `left` only for a served checkout on another branch. Add the refusal to the state diagram and a test to T012. **Writer.**
>
> - **ADV-09**
>   - **Where:** `plan.md:518` (row 2, OQ-12-11, "ADOPT").
>   - **What and why:** refusing any credential-bearing remote narrows ratified 12.1a (`C1144/tasks.md:2476-2484`). 12.1a designs exactly that case, `https://user:<token>@host/…`, as a successful submission whose report is redacted. It also narrows requirement 11's third scenario (spec delta `:363-365`: a session is submitted to "a remote attached" and the report says where it went). The row is labelled as an ordinary default.
>   - **Fix:** take the alternative (push, then redact the report and every message, as 12.1a describes), or relabel the row as a reading of 12.1a for Brett. **Brett.**
>
> - **ADV-10**
>   - **Where:** `plan.md:569` (row 43, P4F-4); `tasks.md:391-401` (T021).
>   - **What and why:** vendoring openxFactory's `demotion-execution-receipt.schema.yaml` (read at openXdox-code `gate_console.py:711`; listed by its validator at `validate-ideation-dashboard-contracts.py:357`) into openXdox-code "under copies.yaml" conflicts with three things:
>     - The promoted `neutral-product-pin` requirement (`openspec/specs/neutral-product-pin/spec.md:258-271`). It allows ONE vendored openxFactory contract, which its own validator reads, registered as a CONSUMED member in the product's `contracts/manifest.yaml`, verified against `contract_pin.yaml`, and naming the contract version.
>     - #1144's 7.1 ("needing more than one is itself a finding").
>     - R1Q27 (a): the other kinds are validated "only where the tree it runs from supplies their schemas". The composed run already supplies openxFactory's tree.
>
>     In addition, openXdox-code's record carries `spec_leg: opensoft/openXdox-spec` and a single `commit`, so it cannot hold an openxFactory-sourced copy.
>   - **Fix:** read the schema from the composed openxFactory tree (U-9 already composes it), or take the alternative (openXdox-spec gains the schema). Otherwise put the vendoring to Brett. Also reconcile with the spec's "gate-action record schema" (F8). **Brett** if vendoring is kept, otherwise **writer**.
>
> - **ADV-11**
>   - **Where:** `contracts/cli-http-health.md:19`; `tasks.md:643-646`.
>   - **What and why:** ratified 14.5 declares `health fix --repo-root <corpus> --finding ID [--batch]` (`C1144/tasks.md:3253`), so that "groups 14 and 15 close on an exact surface"; FR-011 says the same. The contract drops `--batch` for a repeatable `--finding`, and T046 freezes that parser. Adding `--class` is additive and harmless.
>   - **Fix:** keep `--batch` as 14.5 declares it, or carry the change as a ruled amendment in batch Q. **Writer**, or **Brett** if the change is wanted.
>
> - **ADV-12**
>   - **Where:** `data-model.md:187`.
>   - **What and why:** a patch's `content` may be "the replacement document text". That contradicts 15.2 ("MAY return proposed fixes AS PATCHES ONLY"), 15.2a ("checks each patch itself, as a unified diff"; it recognizes refusals by diff headers) and FR-018 ("unified-diff patches only"). Whole-text replacement also evades the checks on headers.
>   - **Fix:** unified diffs only. **Writer.**
>
> - **ADV-13**
>   - **Where:** `tasks.md:813-822` (T058), `:869-874` (T065); `spec.md:1117-1119` (SC-002), `:1294-1295`.
>   - **What and why:** T058 puts F15.1's 24 pytest nodes into the suite. F15.1's shell block is a different matter: the `pack-corpus` run under `timeout 120`, the `ps` check, the tamper re-run and the patch loop. It needs a live sandbox. No task adds it to `validate.yml` (T051 sets floors, T080 is the acceptance job), and the lane's containers refuse `bwrap`. So T065's "F15.1 in the required job with the sandbox live" has nowhere to run.
>   - **Fix:** a CI-owner task (after T058, before T065) adds F15.1's command as a step of the required `validate` job, or of a declared required job on `ubuntu-24.04` with bubblewrap. Put it in the single-writer chain for `validate.yml`. **Writer.**
>
> ### MEDIUM
>
> - **ADV-14**
>   - **Where:** `tasks.md:292-293`, `:320-321`, `:797-798` against `:357` and `:860-864`.
>   - **What and why:** the submit, land and health routes and the new `/capabilities` keys (`actions.land` and the `health` block) are dispatched by core `serve.py`. `compute_capabilities` is core: openDox-code `serve.py:528-650` holds a fixed `actions` map. Every host's `/capabilities` would therefore change, while T019 and T064 assert it is "unchanged". R1Q4 (a) has the default profile contribute openDox's own "verbs and routes".
>   - **Fix:** contribute the routes and their capability flags through the default profile's route extensions, derived from route bindings as `gate` is. Or drop "unchanged" from T019 and T064 and check openxFactory's tests that pin the payload. Partly inferred. **Writer.**
>
> - **ADV-15**
>   - **Where:** `tasks.md:119-120` (batch Q item 3); `spec.md:632-634`.
>   - **What and why:** batch Q item 3 writes R2Q8 (a)'s "composed … until the direction arc's realization lands". ARC-Q2 (a) makes the composed workflow permanent, and ARC-Q1 (a) leaves the governed-behaviour tests composed. Once T074 lands, F12.1's limit would expire into a standalone form that cannot pass.
>   - **Fix:** word item 3 as "composed; ARC-Q2 (a) makes the composition its permanent home", recorded as a reading of the two rulings. **Brett** (cheap).
>
> - **ADV-16**
>   - **Where:** `plan.md:596` (N-10); `spec.md:534-536`.
>   - **What and why:** R2Q12 (a) names runs "at the tip, on a branch or over the working state" (`clarify-questions.md:591-593`). N-10 removes runs over the working state, and its "why" ("runs and baselines are per commit (R2Q12 (a))") misreads the answer. The plan also never states the uncommitted-exception reading that the spec's edge case defers to it.
>   - **Fix:** say N-10 narrows R2Q12's set of runs, and state whether an exception is read from `HEAD` or from the working tree. **Writer**, with Brett confirming.
>
> - **ADV-17**
>   - **Where:** `plan.md:526,528` (rows 10, 12); `tasks.md:610-623`, `:734-747`.
>   - **What and why:** ratified 14.6 and requirement 14's third scenario put empty stubs in `assisted` (`C1144/tasks.md:3276-3277`; spec delta `:480-482`). Row 10 classes stale stubs `human-only` and is silent on empty stubs. OQ-H-11 defines an `assisted` proposal only for near-duplicates. The 14.9 fixture plants no empty stub.
>   - **Fix:** state empty stub = `assisted`, define its deterministic proposal, and test it in T044 and T053. **Writer.**
>
> - **ADV-18**
>   - **Where:** `tasks.md:715-733` (T052).
>   - **What and why:** openDox-code `workbench.py:1622-1651` holds one check at the scoped seam. It refuses a different second one: "a health check is already registered … a different one would replace it". If the entry point registers openDox's own check unconditionally, it collides with openxFactory's `register_health_check` (`scripts/opendox_host.py:524`). Depending on the order, either the host breaks at T064's pin or openDox's check never registers.
>   - **Fix:** the entry point registers openDox's own check only when the seam is empty. A host's check wins, in process and unstored, per R2Q16 (a). Test both orders. **Writer.**
>
> - **ADV-19**
>   - **Where:** `tasks.md:929-958` (T074, T075); `plan.md:593` (N-7).
>   - **What and why:** T074 retargets `gate_console`, `cli_gate` and `gate_routes` to seams the host registers, but openxFactory's host registers them only in T075, which comes after T074. T074's required composed run uses `composed_host_pin.yaml` at T064's commit, so the 12.5 suites would meet unregistered seams.
>   - **Fix:** state that T074's composed conftest registers the governed implementations from the composed `scripts/` until T075 moves that registration into host wiring. Inferred. **Writer.**
>
> - **ADV-20**
>   - **Where:** `plan.md:580` (row 49, ARC-5); `tasks.md:959-965` (T076).
>   - **What and why:** if #1144 archives first, T076 "ticks F9.2" inside an archived change directory. The archive-date checker is sensitive to history, and editing an archived record afterwards is not covered by any rule in the plan. Details in § 4.5.
>   - **Fix:** record F9.2's closure in the arc change's own evidence, and report it open in the archive record (R1Q6 (d)'s form). Do not edit the archived `tasks.md`. **Brett** (ARC-5 is already his), wording by the **writer**.
>
> - **ADV-21**
>   - **Where:** `plan.md:543` (row 27, OQ-H15-14).
>   - **What and why:** the engine fetches a git URL from a corpus's committed `health/packs.yaml` at `health run`. The row names no transport hardening. A cloned corpus could name an `ext::` or `file://` source, or a local path. The runtime's push already pins `protocol.ext.allow=never` and refuses repo-local command config (`repository_act.py:1335-1372`).
>   - **Fix:** fetch only over https or ssh, refuse credential URLs, and reuse the hardened transport rules. **Writer.**
>
> - **ADV-22**
>   - **Where:** `tasks.md:673-676` (T048).
>   - **What and why:** "the bounds' defaults fixed after running the pack corpus under them" needs T055's `pack-corpus`, but T055 is not a dependency of T048, and the `pyproject.toml` order runs T048 before T055. Separately, R2Q9 (a) items 4 (the forking child's pack id in argv) and 6 (the restore counts as a write) are fixture behaviours, not runner behaviours.
>   - **Fix:** move the bound measurement to T056 or T058, and items 4 and 6 to T055. **Writer.**
>
> - **ADV-23**
>   - **Where:** `plan.md:292-325`.
>   - **What and why:** the single-writer table has gaps, listed in § 4.1. The ones not ordered by any dependency are: openXdox-code `src/openxdox/contracts/copies.yaml` (T021 and T022, both [P] on day one); openDox-code `serve.py` (T052 against T057); `pyproject.toml` (T048 against T055); `runtime/repository_act.py` (T011 against the creation-site audit in T012). In addition, T017's After omits T010, T012's Files omit `session_pr.py` (whose re-exports 12.6a requires), and the cross-lane hand-off of `health_contract.py` (T041 to T045) is missing.
>   - **Fix:** add these files to the table and encode the orders in each task's After line. **Writer.**
>
> - **ADV-24**
>   - **Where:** `tasks.md:121-122` (batch Q item 4).
>   - **What and why:** under R2Q10 (a), F15.1 uses literal ids in more places than "selection lines": `x['id'] == 'broken-link'` (`C1144/tasks.md:3590`, which would yield `set()`), the `refused_patch` values (`:3608-3612`), and `--finding patch-*` with `refs/heads/health-fix-patch-ok` (`:3595-3602`).
>   - **Fix:** enumerate every one of them in item 4. **Writer.**
>
> - **ADV-25**
>   - **Where:** `plan.md:592` (N-6).
>   - **What and why:** letting phase 5's openDox-code land before phase 4's checkpoint changes the build order of the RULED release map (`5799646419`: "The ORDER they are built in is the release map"). The row presents it as an ordinary proposal.
>   - **Fix:** relabel it as a reading of the map for Brett. **Brett.**
>
> - **ADV-26**
>   - **Where:** `plan.md:519` (row 3, OQ-12-12).
>   - **What and why:** "origin only" means a repository whose one remote is named, say, `fork` gets `NoSubmissionTarget` while a remote is attached. That blurs requirement 11's third and fourth scenarios.
>   - **Fix:** name the refusal "no remote named origin" (as `data-model.md:30` does) and record that the reading narrows "a remote attached". **Writer.**
>
> - **ADV-27**
>   - **Where:** `contracts/health-finding.md:31`.
>   - **What and why:** `message` is required, and "never quotes the document" is unenforced. Only `evidence` is bounded. So pack messages could carry document text into the store, against R2Q25 (a) and RULING Q1's "no document".
>   - **Fix:** apply the same length and key rule to `message`. **Writer.**
>
> - **ADV-28**
>   - **Where:** `README.md:87`; `plan.md:138`.
>   - **What and why:** the README index omits the new plan documents (Principle IV MUST; this is D1). T004 tracks it.
>   - **Fix:** add the links before the PR leaves draft. **Writer.**
>
> ### LOW
>
> - **ADV-29** (`tasks.md:717`; `research.md:204-206`): `workbench.py:1542-1557` is the `DEFAULT_SCOPED_FAMILIES` block. The seam itself is `def run_scoped_doc_health` at `:1666`, and registration is at `:1622`. T052's tick would write a wrong correction into #1144. Fix the cite. **Writer.**
> - **ADV-30** (`tasks.md:346-353`): T018 omits R2Q6 (a)'s README content: a plain repository pushes to its remote with `git push`, and a clone of a project repository pushes to it, after which `project push` carries the work on. **Writer.**
> - **ADV-31** (`quickstart.md:78`, `:144`, `:81`): `SERVER` is never assigned, yet § 5 runs `kill "$SERVER"` under `set -u`. "Packs live (CI)" is false for the `acceptance` job, which T010 neither pins nor provisions. **Writer.**
> - **ADV-32** (`plan.md:612`): C-1 says "spec.md is not this plan's to edit", but the spec is this feature's own, and T004 can correct it. **Writer.**
> - **ADV-33** (`plan.md:354-366`): the stated critical path for phase 5 contains a step that is not a dependency (T057 then T060: T060 does not depend on T057). It also omits the pack track (T045, T048, T056, T058, then T061), which runs through what the plan itself calls the riskiest slice. **Writer.**
> - **ADV-34** (`tasks.md` evidence tasks): no task links the evidence files in the README index, which plan 034 did. **Writer.**
> - **ADV-35** (`plan.md:550`, `:580`, `:558`, `:591`, `:598`, `:595`, `:593`): rows to merge, split or drop:
>   - merge rows 34 and 49;
>   - merge rows 37, 55 and 62;
>   - row 59 (N-9) is a record, not a decision;
>   - split row 57 (N-7) into the file layout and the required-check settings act, and name who sets the required check and when.
>
>   **Writer.**
> - **ADV-36** (`tasks.md:256-261`): session worktrees live in `<repo>-worktrees/` beside the checkout (`session_git.py:250-263`), where `merge` is already allowed. Only `merge --ff-only <commit>` at the served root needs the new argument check. **Writer.**
> - **ADV-37** (`plan.md:579`, ARC-4): giving the arc its own trailer removes T075's openxFactory edits from F11.1's guard. Give the arc's change an equivalent surfaces check. **Writer.**
> - **ADV-38** (`spec.md:664-666`): "standalone requires `OPENDOX_INSTALL_MODE=local`". Since R2Q9 item 7, the `--local` flag must count as the same selection. **Writer.**
> - **ADV-39** (`plan.md:566`, H-1): openxFactory's `scripts/ideation_dashboard/` has no `__init__.py`. The shim's directory must not add one, or it shadows openxFactory's package in the composed run. Inferred. **Writer.**
> - **ADV-40** (`C1144/tasks.md:3496`; `plan.md:526`): declare 15.6's default timeout as a number, and the criterion for a stale stub. **Writer.**
> - **ADV-41** (`plan.md:594`, N-8; `tasks.md:157-167`): T008 lands in codexFactory but names neither that repository's required checks nor its review lane. Inferred. **Writer.**
>
> ## 4. The brief's specific checks
>
> ### 4.1 Lanes and single writers
>
> The claim that no two concurrent slices write one file is refuted. Every file written by two tasks:
>
> | file | writers | ordered by dependencies? |
> |---|---|---|
> | oDc `validate.yml` | T010, T017, T051, T080 | Partly. T017's After omits T010. |
> | oDc `serve.py` | T014, T015, T016, T052, T057 | T057 does not list T052. |
> | oDc `cli.py` | T014, T016, T046, T052 | Yes. |
> | oDc `default_profile.py` | T015, T016, T046 | Yes. |
> | oDc `health/cli.py` | T046, T053, T054 | Yes. |
> | oDc `web/app.js`, `index.html` | T015, T016, T057 | Yes. |
> | oDc `web_boundary_census.yaml`, `test_web_boundary.py` | T025 (lane 3), T015, T016, T057 | Yes. T025's Files omit `test_web_boundary.py`. |
> | oDc `health_contract.py` | T041 (lane 4), T045 (lane 3) | Yes. Not in the hand-off list. |
> | **oDc `contracts/copies.yaml`, `tests/test_validator_input_set.py`** | T041 (4), T047 (3), T054 (4) | **No: T047 and T054 can run together. Not in the table.** |
> | oDc `pyproject.toml` | T048, T055, T061 | T055 does not list T048. |
> | oDc `session_pr.py` | T011, T012 | Yes, but T012's Files omit it. |
> | oDc `runtime/repository_act.py` | T011, T012 (audit) | No. Not in the table. |
> | oDc migrations and `tests_runtime` schema suites | T042 | One writer. |
> | oXc `tests/conftest.py` | T020 (3), T073 (3), T074 (4) | Yes. |
> | oXc `gate_console.py` | T021 (3), T074 (4) | Yes. |
> | oXc `cli_gate.py`, `gate_routes.py`, `generator.py` | T074 only | Yes as files, but see ADV-19 on sequencing. |
> | **oXc `src/openxdox/contracts/copies.yaml`** | T021, T022 | **No. Both [P] on day one. Not in the table.** |
> | oXc `.github/workflows/` | T029, T073, T074 | Yes. |
> | oXc `tests/composed_host_pin.yaml` | T029, T030, T064 | Yes. Not in the table. |
> | oXc `declared_exclusion.yaml` | T073, T074 | Yes. |
> | oXc `pyproject.toml` | T028, T063, T074 | Yes. |
> | oxF `README.md` | T004, T070, T077, evidence links | Serial by the holder. Not in the table. |
> | oxF #1144 directory | T005, T076, T082 | Yes, each under its own Rule 6 window. |
>
> ### 4.2 Dependencies
>
> - **Batch Q before phase 4's checkpoint:** holds. T033, T031, T026 and T015 are each After T005.
> - **R2Q17's CI change before the first sandbox test:** holds. T048 is After T010, and T056 and T058 follow T048. But N-4's "before any slice adds a test" is encoded nowhere.
> - **Cycles:** none in the graph. The ordering problem is ADV-05, an inversion against an invariant, not a cycle.
> - **Missing dependencies:** ADV-06 (an external ruling on the cut path), ADV-13, ADV-19, ADV-22 and ADV-23.
> - **Critical path:** phase 4's join at T029 is real. T029 is After T020–T026 and T028, and T028 is After T027, which is After T010–T017. Whether P4-F is the longer pole is unmeasured; the plan says as much. Phase 5's stated path is not real (ADV-33). Under ARC-6 (a), Brett's word T071 also sits on the path (ADV-06).
>
> ### 4.3 The 63 design decisions
>
> **Count:** 63 is correct (34 + 3 + 7 + 6 + 13).
>
> **Labelled as ordinary defaults, but they change or narrow ratified text or rulings:**
>
> | decision | what it touches |
> |---|---|
> | Row 2 (OQ-12-11) | narrows 12.1a and requirement 11 (ADV-09) |
> | Row 43 (P4F-4) | conflicts with the promoted `neutral-product-pin`, 7.1 and R1Q27 (a) (ADV-10) |
> | Row 50 (ARC-6) | contradicts ARC-Q3 (a) (ADV-06) |
> | Row 56 (N-6) | changes the ruled release map's build order (ADV-25) |
> | Row 60 (N-10) | narrows R2Q12 (a) (ADV-16) |
> | Row 63 (N-13) | undermines R2Q10's "stable" (ADV-07) |
> | Row 3 (OQ-12-12) | narrows "a remote attached" (ADV-26) |
>
> **Gaps:**
> - Row 10 omits the ratified empty-stub class (ADV-17).
> - Row 8 needs the registration precedence of ADV-18.
> - Row 27 needs transport hardening (ADV-21).
> - Row 22 has a misplaced measurement (ADV-22).
> - Row 26 applies `sorted-ls-tree-r-v1`, defined over `<commit>` (`contracts/opendox-pin.yaml:122-134`), to the tree-ish `<commit>:<source>`. That reading is acceptable; say so in the contract.
>
> **Labelled correctly:** R-1 and W-1 as rulings; H-1 and H-2 for confirmation (batch C's ratified wording does not limit respellings to seams the arc moved, `C1144/tasks.md:922-936`, so H-2 needs no amendment); ARC-1 for Brett to name.
>
> **Split, merge or drop:** see ADV-35.
>
> ### 4.4 Conflicts C-1 to C-17
>
> | # | Real? | Resolution path | Comment |
> |---|---|---|---|
> | C-1 | Yes (not re-measured by me) | Weak | T004 can fix `spec.md` (ADV-32). |
> | C-2 | Yes | Answer | Fine. |
> | C-3 | Yes | I-3 note | Fine. |
> | C-4 | Yes | N-12 | Fine. |
> | C-5 | Yes | T008 then T013 | Fine. |
> | C-6 | Partly | ARC-5, row 34 | See § 4.5. |
> | C-7 | Yes (verified) | Row 13 | Fine. |
> | C-8 | Yes | Batch Q item 4 | Incomplete (ADV-24). |
> | C-9 | Yes | T052's tick | The line cite is wrong (ADV-29). |
> | C-10 | Yes | Row 39, ruling | Fine. |
> | C-11 | Yes | Row 38, ruling | Fine. |
> | C-12 | Weaker than stated | Row 41 | Batch C's text admits it. |
> | C-13 | Yes (GitHub runners ship `gh`) | Row 6 | Fine. |
> | C-14 | Yes | I-2 | See § 4.5. |
> | C-15 | Yes | N-2 | Routes need the same treatment (ADV-14). |
> | C-16 | Yes | N-3 | Fine. |
> | C-17 | Yes (verified) | T004 | Fine. |
>
> **Conflicts the plan did not list:** ADV-01–ADV-11, ADV-14, ADV-15 and ADV-18.
>
> ### 4.5 C-6 and C-14
>
> **C-6, the coherent reading.**
> - F9.2's ruled note (`5859927858`, as plan 034's T008 records it: "F9.2's box stays open until then") governs when the box ticks. It is not a gate on the archive.
> - ARC-Q3 (a), the later ruling, governs the archive gate: the arc gates neither release 2's close nor #1144's archive.
> - R1Q6 (d) and plan 034's watch item ("the archive act must report it as open") supply the form: #1144 may archive with F9.2 unticked, reported as part of requirement 9's open extraction for openXdox-code.
> - The only real tension is with OQ-038-2's default, which was never ruled and predates the arc ruling. Row 34 rightly withdraws its clause.
> - ARC-5's recommendation is therefore the coherent reading, with one fix: F9.2's later closure must be recorded outside the archived #1144 directory (ADV-20).
>
> **C-14, the coherent reading.**
> - F14.1's `git init -q` (and F15.1's) produces whatever git's `init.defaultBranch` gives, which is `master` on an unconfigured CI runner.
> - R2Q7 (a)'s `main` governs landing only, and F14.1 never lands.
> - Under R2Q12 (a) with I-2, F14.1's findings are unclassed, plus one install-level `no-default-branch` finding with an empty path. Selection by fixture document skips that finding, and F14.1 asserts no baseline class. So F14.1 passes unamended, and no ruling is needed.
> - Do not add `-b main` to F14.1, because that is falsifier text.
> - The consequence: #1144's own falsifiers will never exercise the baseline in CI. T046's tests must cover a repository on `main` themselves. AT-R2's `-b main` (`quickstart.md:62`) is correct.
>
> ### 4.6 Measured claims I checked (30)
>
> Unless noted, the openDox-code lines are at `a9ac96f9`, the openXdox-code lines at `56e1c238`, and the openxFactory lines at `0f2a87f6`.
>
> **Confirmed:**
> 1. `session_pr.py:55` and `branch_session.py:149` read `DEFAULT_BASE = "main"`.
> 2. `session_git.py:93` reads "Nothing that touches the served working tree, its index, or its HEAD is here". `:99` opens `SERVED_ALLOWED_SUBCOMMANDS = frozenset({`. `:125` reads `FORBIDDEN_ANYWHERE_SUBCOMMANDS = ("fetch", "pull")`.
> 3. `tests/test_session_git.py:523` holds `("merge", "other-branch"),`. Line `:564` holds the `merge` absence loop; its assertion is at `:565` (a minor drift in the cite).
> 4. `cli.py:1292` is `def _pull_request_port`, returning `GhPullRequests(repo_root)` at `:1306`. `serve.py:1062` is `pull_request_factory = None`. `:1229-1230` construct `GhPullRequests(Path(self.checkout_root))`. `:2107` returns `WorkingTreeCorpus()`.
> 5. `validate.yml:47` is `runs-on: ubuntu-latest`. `:272` sets `MIN_SELECTED: "3977"`, `:273` `MIN_PASSED: "3966"`, `:306` `EXPECT_SKIPPED: "11"`, enforced at `:344`. The `acceptance` job at `:374` is also `ubuntu-latest`. Nothing matches `bwrap` or `bubblewrap`.
> 6. `migrations/` holds `0001_identity_and_coordination.sql` and `0002_migration_state.sql` only. `pyproject.toml:23` reads `version = "0.1.0"`.
> 7. `default_profile.py:41` reads "Release 2's `submit`, `land` and `health` join the tuple when they exist."
> 8. `workbench.py:1594` is `HEALTH_CHECK_NOT_REGISTERED`.
> 9. `tests_runtime/conftest.py:130` is `def _skip_or_fail`.
> 10. `repository_act.py:203` is `refuse_credential_bearing_remote`. `:982` runs `init --bare`. `:1298` is `push_to_remote`. `local_git_adapter.py:146` reads `DEFAULT_BRANCH = "main"`. `runtime/cli.py:114` declares `PROJECT_VERBS … "push")`. `["0001","0002"]` is hard-coded 10 times (2, 7 and 1 across three files).
> 11. The openXdox-code governed set is 16 files. 15 are exclusion entries; the one that is not is `tests/test_gate_loop_views.py`.
> 12. `test_session_snapshot.py:910` reads `assert isinstance(port, session_pr.GhPullRequests)`.
> 13. `test_dependency_direction.py:353-363` lists 8 modules, with 7 import-time and 6 deferred imports.
> 14. `declared_exclusion.yaml` counts 66 files: `doc_health` 60, `openxfactory-contracts` 5, `status-exemption-rail` 3.
> 15. `tests/conftest.py:533` opens `HOST_PLANE_SUITES`, and `:413-421` hold the composed-only registration. `test_session_transaction.py:296` reads `from ideation_dashboard import session_git as sg`.
> 16. `test_staging_workbench.py:492` is `_CREATE_HARNESS`, `:1008` is `_SESSION_HARNESS`; `:802` and `:1286` are the import-free assertions; `:1291` and `:1333` hold the route claims. `staging-workbench-model.js:38` says its "ONE SIBLING IMPORT … is `./display.js`", and `1e46971` is "§ 3.4 S7".
> 17. In openxFactory, `scripts/opendox_host.py:524` is `(workbench, "register_health_check", scoped_doc_health)`. `families.py:371-372` hold the "removing its health/dispositions.yaml entry re-opens" words. `scripts/doc_health/` holds 38 modules. `test_extension_point_parity.py:284` reads "Regenerate the golden ONLY with a ruling".
> 18. In codexFactory, feature 007's FR-004 is at `:517-519` and SC-002 at `:811-816`. `git diff --stat 1a32f399 origin/main` on that spec is empty.
> 19. C-7: `opensoft/xFactory` returns `health/dispositions.yaml 1ef89c06…`, and `opensoft/openxFactory` returns HTTP 404.
> 20. #1144 line cites all match: F6.1 `:1143`, F11.1 `:2007`, F12.1 `:2670`, F12.2 `:2816`, F14.1 `:3302`, F15.1 `:3548`, 9.5 `:1553`, F9.2 `:1718`, 15.1b `:3426`, the release map `:108`, 12.4's repoint `:2513-2519`, and `design.md:476-478`, `:799-801`, `:1059-1061`.
>
> **Wrong:**
> 21. `workbench.py:1542-1557` is the `DEFAULT_SCOPED_FAMILIES` block; `run_scoped_doc_health` is at `:1666` (ADV-29).
>
> **New facts behind findings:**
> 22. `config.py:1954` reads "THE DEFAULT IS HOSTED" (ADV-04).
> 23. openDox-code's `copies.yaml` holds a single commit, and the test asserts exactly four copies (ADV-05).
> 24. openXdox-code's `copies.yaml` reads `spec_leg: opensoft/openXdox-spec` with a single commit (ADV-10).
> 25. `gate_console.py:711` reads `demotion-execution-receipt.schema.yaml` (ADV-10).
> 26. `serve.py:528-650` builds a core `actions` map (ADV-14).
> 27. `workbench.py:1622-1651` refuses a second, different check (ADV-18).
> 28. `session_git.py:250-263` places session worktrees in a sibling container (ADV-36).
> 29. openxFactory's `scripts/ideation_dashboard/` has no `__init__.py` (ADV-39).
> 30. All repository `main`s still match R0. openxFactory moved one commit, which touches nothing here.
>
> ## 5. Verdict
>
> **READY after the listed fixes.** It is not ready for Brett's ruling at `6d6911e1`.
>
> **Must fix before T004:**
> - ADV-01, ADV-02 and ADV-03 (quick wording fixes).
> - HIGH findings that are the plan writer's: ADV-04, ADV-05, ADV-06, ADV-07, ADV-08, ADV-12 and ADV-13.
> - Relabel as explicit questions for Brett, with options: ADV-09, ADV-10 and ADV-11.
> - Add to the ruling block: ADV-15, ADV-25 and ARC-5's archive-record fix (ADV-20).
> - Add T060's bundle cut word to T060 (ADV-05).
>
> The MEDIUM and LOW findings can be folded into the same revision.
