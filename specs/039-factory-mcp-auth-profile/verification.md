# Verification record: Factory MCP authorization profile

Status: record
Kind: report
Lane: openxfactory-5 (openXfactory-5)

This record keeps the evidence the feature's success criteria demand, in the
order it was made. Every run names the tree it ran on. Runs used a Python 3.12
virtual environment built from `requirements/hermes-runtime-contracts.lock`
with `--require-hashes`, the command CI's `pytest-suite` runs
(`research.md` R-11). `jsonschema` is 4.25.1.

## 1. Baseline on `main` `93d13d6c`

- `tests/factory-mcp/`: **88 passed, 203 subtests passed**. This matches feature
  037's final record (88 tests, 203 subtests).
- The same module under a system interpreter that carries a URI format-checker
  package CI's lock does not: 4 failed (`invalid_json_schema` where the tests
  expect `invalid_pointer` or `remote_or_unsafe_schema_reference`). These are
  environment failures, on `main`. That is why every run here uses the
  CI-matched environment.
- Probes of `main`'s validator are recorded in `research.md` § *Starting point,
  measured*.

## 2. Specify, clarify, plan, checklists, tasks, analyze

- **Specify**: `spec.md`, with the requirements-quality checklist
  `checklists/requirements.md`, which passed in one pass.
- **Clarify**: no question. The ratified packet decides every material question
  (spec § Clarifications). The lane's coordinator accepted the verdict, and the
  skipped `before_specify` hook, when it resumed the seat (2026-10-09T17:2xZ).
- **Plan**: `plan.md`, `research.md` (R-1 to R-17), `data-model.md`,
  `contracts/interface.md`, `quickstart.md`. Constitution Check: PASS before and
  after design.
- **Checklists**, run with no focus argument, so at maximum coverage: seven
  domain checklists (`contract`, `security`, `diagnostics`, `outcomes`,
  `compatibility`, `governance`, `acceptance`), 97 items. The pass found seven
  gaps in `spec.md`, each fixed and noted at its item: FR-013's exact
  comparison; the offline limit of a shared audience; runtime token checks
  placed out of scope; FR-019's moving of the unreleased wording; SC-008, the
  engineering domain's expected signals; the operations domain's position; and
  the statement that this feature edits no packet file and lands on its own
  word.
- **Tasks**: `tasks.md`, T001 to T028, red-first by construction.
- **Analyze, round 1** (read-only pass, then fixed under the brief's "Fix what
  analyze finds"):

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| D1 | CRITICAL | Constitution IV requires new documents to be linked into README's document index. The plan relied on the runbook link, while features 034, 035 and 038 each have a README Documentation bullet. | Fixed: one README Documentation bullet (T024a); plan row IV updated. |
| B1 | MEDIUM | FR-012's "within the field's bounds" deferred to research. | Fixed: FR-012 states 1 to 2048 characters. |
| B2 | MEDIUM | FR-005's "path" could be read decoded. | Fixed: "as written in the URI, not decoded". |
| F1 | MEDIUM | T025 pushes the branch at the stop; the plan's step 6 did not say so. | Fixed: plan step 6 aligned. |
| D2 | LOW | The constitution names a bare `openspec validate`, while the repository validates through its pinned CLI. | Kept: the pinned entrypoint is the repository's documented practice, and stricter. |
| E1 | LOW | FR-018 (runbook) has a review-only witness. | Kept: documentation has no executable witness. |

Coverage after the fixes: 19 of 19 functional requirements and 8 of 8 success
criteria map to tasks, with no unmapped task, no placeholder and no
duplication. No CRITICAL finding remains.

## 3. Red first (change task 2.2; SC-002, SC-003, SC-005)

The tests were committed alone, at `bd76faf4`, on top of the feature documents
(`a8e91bf8`) and `main` `93d13d6c`. No schema, example or validator byte had
moved. Run at that commit, so against `main`'s validator and schema:

```text
python -m pytest tests/factory-mcp -q
93 failed, 97 passed, 176 subtests passed
```

(Counts are pytest's, with each failing subtest counted once.)

Per test (pytest's JUnit report, one row per test method):

| Test | On `main`'s validator | Why |
| --- | --- | --- |
| `test_hosted_declaration_without_block` | fails | `main` has no `hosted_auth_missing`, and refuses the `auth` concern (`schema_enum`) |
| `test_a_valid_hosted_block_is_accepted` | fails | `main` refuses every block (`schema_oneOf` at `/service`) |
| `test_block_shape_is_closed` | fails | its valid block comes first, and `main` refuses it |
| `test_issuer_must_be_an_https_identifier` | fails | no `invalid_issuer` on `main` |
| `test_metadata_path_is_the_rfc9728_location` | fails | no `auth_metadata_path_mismatch` on `main` |
| `test_hosted_resource_uri_carries_no_query` | fails | no `auth_resource_query` on `main` |
| `test_auth_claims_cite_support` | fails | no `unsupported_auth`, and no `/service/auth/...` locations for the two existing codes |
| `test_auth_concern_is_admitted_everywhere` | fails | `main`'s concern vocabulary refuses `auth` (`schema_enum`) |
| `test_rs256_is_required` | fails | no `auth_rs256_missing` on `main` |
| `test_none_and_hmac_are_refused_by_name` | fails | no `auth_algorithm_forbidden` on `main` |
| `test_other_algorithms_are_not_admitted` | fails | no `auth_algorithm_unadmitted` on `main` |
| `test_audience_is_bound_to_the_server` | fails | no `auth_audience_unbound` on `main` |
| `test_auth_diagnostics_are_deterministic` | fails | none of the seven expected codes exists on `main` |
| `test_packaged_deployed_example` | fails | the deployed example does not exist yet (`input_unreadable`, exit 2) |
| `test_resource_identity_without_optional_format_checker` (amended) | fails | its deployed service now carries a block, which `main` refuses |
| `test_resource_uri_is_https_without_fragment_or_userinfo` (amended) | fails | the same |
| `test_auth_on_an_undeployed_service_is_refused` | **passes** (characterization) | the closed not-deployed branch refuses `auth` on `main` too |
| `test_stdio_declaration_needs_no_block` | **passes** (characterization) | `main` accepts a block-free stdio declaration |
| `test_dependency_failure_reported_as_an_error_is_an_execution_failure` | **passes** (characterization) | `main` enforces the classification; see § 4 |
| `test_result_statuses_are_completed_evaluations` | **passes** (characterization) | the same |
| `test_two_domains_share_a_code_name` | **passes** (characterization) | `main` never compares declarations |
| `test_a_code_no_other_domain_uses` | **passes** (characterization) | `main` has no neutral code list |

The 86 test methods `main` already had and this feature did not amend all
passed.

**Amended tests (SC-005).** Two existing tests build a deployed service with no
block and expect the resource URI to be judged alone. The ratified design's
*Compatibility* section reverses that premise: "A deployed declaration without
the block, which is valid today, becomes invalid (`hosted_auth_missing`)". Both
now give the service a valid block with an `issuer_assigned` audience (the
`assigned()` helper). Where a URI in their list carries a query, they also
expect `auth_resource_query` (`research.md` R-15).

**One correction before the commit.** The first draft of
`test_auth_on_an_undeployed_service_is_refused` built its block through the
`hosted()` helper, which also adds an `auth` gap. On `main` that gap is refused
too (`schema_enum`), so a test meant as characterization failed. Its block is
now built directly and cites nothing, so the declaration differs from `main`'s
example only by the `auth` field. It passes on `main`, as a characterization
test must.

## 4. M5's mutant (change task 2.2, design D8; SC-004)

Two scratch trees were made from `git archive 93d13d6c` (the validator, the
contract directory and the test module's directory), each with the test module
from `bd76faf4` copied in. In one, the classification comparison was removed
from `check_mapping`:

```diff
@@ -980,8 +980,6 @@
             continue
         error = inventories[index]["kind"] == "error"
         expected = "execution_failure" if error else "completed_evaluation"
-        if row["is_error"] != error or row["class"] != expected:
-            bad("outcome_classification_mismatch", f"/outcomes/mapping/{k}")
```

Both trees ran the two classification tests:

```text
python -m unittest discover -s tests/factory-mcp -p 'test_*.py' \
  -k test_dependency_failure_reported_as_an_error_is_an_execution_failure \
  -k test_result_statuses_are_completed_evaluations
```

- **Mutant: FAILED (failures=4).** All three subtests of the first test failed
  (an error-inventory `UNAVAILABLE` mapped as a completed evaluation, or with the
  wrong `is_error`), each `[] != [('outcome_classification_mismatch',
  '/tools/0/outcomes/mapping/2')]`. The second test failed too: a result status
  mapped as an execution failure gave `[] != [('outcome_classification_mismatch',
  '/tools/0/outcomes/mapping/4')]`.
- **`main`'s own validator: Ran 2 tests, OK.**

The repository's pytest scaffolding (`tests/conftest.py` and `pytest.ini`) was
left out of both scratch trees, because it imports modules the two-directory
archive does not carry. The test module is a plain `unittest` module, so the
standard runner ran it unchanged.

## 5. Implementation (change tasks 2.3 to 2.5)

| Commit | Task | `tests/factory-mcp/` after it |
| --- | --- | --- |
| `bcdf2235` | 2.3: the schema's `auth` block and `auth` concern; the deployed example | 71 failed, 105 passed, 232 subtests passed: the 11 methods still failing all wait for the validator, and every characterization test passes |
| `3245c0c3` | 2.4: the validator's authorization checks | **108 passed, 300 subtests passed** |
| `3335da43` | 2.5: the runbook | 108 passed, 300 subtests passed |

The starting-point probes of § 1, re-run against the validator at `3245c0c3`,
now give: a deployed service with no block is `invalid`, `hosted_auth_missing`
at `/service`. A not-deployed service with a block is `invalid`, `schema_oneOf`
at `/service`, as on `main`. A deployed service with a query and no block is
`invalid`, `hosted_auth_missing` at `/service` and `auth_resource_query` at
`/service/canonical_resource_uri`. The shipped not-deployed example is
`valid-with-gaps` with no diagnostic, as on `main`. Both classification probes
are unchanged.

None of the files this branch touches is a member of
`contracts/releases/contract-v4.0.digests.yaml` (283 members), so the branch
adds no non-editorial mismatch to `verify-commit` before the cut.

The contract cut (change task 2.6), the gates on the branch and on `main`, the
full suite and the out-of-tree engineering check (change task 2.7) follow the
version claim on #630 row 4. They are recorded in the next sections.

## 6. The contract cut and its re-cut (change task 2.6)

**The number.** Registering the declaration adds a contract and removes,
narrows or reinterprets nothing, so the cut is ADDITIVE, a minor
(`docs/contract-versioning-policy.md` § Change Classes). At the stop (T025),
`main`'s manifest declared `contract-v4.0`, whose annotated tag is published.
No later inventory existed under `contracts/releases/`, and no comment on #630
named a later number. The one open pull request touching the release surface,
#1284, refreshed one row's digest and moved no version. The next minor was
`contract-v4.1`. The lane's coordinator claimed it as row 4 on #630 (comment
`6086467830`, 2026-10-09T18:02:11Z) before the cut was made. The packet's
`target_release: deferred-allocation` reserved nothing earlier.

**The first candidate, `38c78817`**, cut from `main` `93d13d6c`, is one commit of
seven files:

- `contracts/manifest.yaml`: `contract_bundle_version: contract-v4.1`, and the
  row `factory-mcp-declaration` with the schema's per-file `sha256`
  (`5e3cf502cea37f18e5281ce6b344a621196e1fa77bfe40b57e17b4ddd2fa28ac`). It is a
  registered row, not a release-inventory member;
- `contracts/factory-mcp/declaration.schema.json`: the title no longer says
  "Unreleased", and the row's digest is of these bytes;
- `contracts/CHANGELOG.md`: the `contract-v4.1` entry;
- `contracts/README.md`: two native-index rows, for the declaration and for its
  validator;
- `tests/intent-compliance/test_release_boundary.py`: the release-boundary
  advance for this cut. No intent-compliance member moved since
  `contract-v4.0`, measured by `git diff --name-status`;
- `docs/factory-mcp-conformance.md`: the unreleased wording moves to
  `contract-v4.1` (FR-019);
- `contracts/releases/contract-v4.1.digests.yaml`, built last, from the
  candidate's bytes, by `scripts/validate-contract-release.py build --tag
  contract-v4.1`.

Checks on `38c78817`:

- `scripts/validate-contract-release.py verify-commit --commit 38c78817`: PASS,
  against `contracts/releases/contract-v4.1.digests.yaml`.
- `scripts/validate-manifest-digests.py .`: 185 per-file digests verify.
- The modules coupled to a cut (release boundary, the clearing manifest rows,
  manifest digests, the release inventory, the doc-health release families,
  `tests/factory-mcp/` and the others the inventory touches): 585 passed, 300
  subtests passed.
- `scripts/validate-release-tag-gate.py .` on an emulated pull-request merge
  tree (`93d13d6c` plus a `--no-ff` merge of `38c78817`): no error and no
  warning, plus the expected notice that the `contract-v4.1` tag is owed.

**The re-cut, forward-only.** Before the realization landed, #1284 merged into
`main` as `9a272c6d` (2026-10-09T18:07Z). It moved two inventory members,
`contracts/manifest.yaml` (the digest-construction schema's row) and
`contracts/README.md` (the council-convening index rows). The first candidate
was pushed unchanged. `main` was then merged in (`24699ca5`, never a rebase).
The merge had one add/add conflict, in `contracts/README.md`, and both sides
were kept, `main`'s rows first. The re-cut, `6300772b`, rebuilt the inventory
with the same tool, from the merged bytes. Three members' digests changed
against `38c78817`: `contracts/CHANGELOG.md`, `contracts/README.md` and
`contracts/manifest.yaml`. The changelog entry is re-attributed by inventory
diff and keeps the number, which stays claimed on #630.

The inventory against `contract-v4.0`, as the changelog records it:

- 283 entries become 342: 59 added, none removed, 8 digests moved.
- The 59 added are the clearing family, joining at its release floor, and none
  of them moved a byte since `contract-v4.0`.
- Each of the 8 moved digests is attributed in the changelog to the commits and
  pull requests that moved it.
- Rows of `contracts/manifest.yaml`: 202 become 204.
  - `factory-mcp-declaration` was added by this cut.
  - `openxwallet-pin` was added by #1026.
  - `signed-execution-chain-digest-construction` changed digest in #1284.
  - #1284's `contracts/council-convening/` is dormant and unregistered, so this
    bundle registers none of it.

Checks on `6300772b`:

- `verify-commit --commit 6300772b`: PASS.
- `validate-manifest-digests`: 185 per-file digests verify.
- `release-tag-gate` on an emulated merge tree, `7ee4e874` (`9a272c6d` plus a
  `--no-ff` merge of `6300772b`, without submodules, as the workflow checks it
  out): it reports both release-surface paths, `contracts/manifest.yaml` and
  `contracts/releases/contract-v4.1.digests.yaml`, and the bundle moving from
  `contract-v4.0` at the base to `contract-v4.1` at the head. It finds "no
  error, no warning", plus the notice `TAG OWED: contract-v4.1 has no published
  annotated tag`, which names publication as an act after the merge.

**No tag is published.** Under § *Bundle Realization Order* step 5, the
annotated tag follows the landing, and this realization lands only on its own
word.

## 7. Gates, on the branch and on `main` (change task 2.7)

Both sides ran in the same clone kind. Each is a full clone, with `openXwallet`
initialized and `openXdox` and `openDox` initialized recursively, as
`pytest-suite` does; neither is shallow. They ran the same commands under the
same CI-matched environment, at the branch head `6300772b` and at `main`
`9a272c6d`. The OpenSpec gates ran through the repository's pinned CLI
(`@fission-ai/openspec@1.12.0`, verified against its content address).

| Gate | Command | Branch `6300772b` | `main` `9a272c6d` |
| --- | --- | --- | --- |
| OpenSpec strict | `scripts/validate-openspec-cli-pin.py --all --strict` | 0 | 0 |
| OpenSpec, no cache | `scripts/validate-openspec-cli-pin.py --all --no-cache` | 0 | 0 |
| openXwallet pin | `scripts/verify-openxwallet-pin.py` | 0 | 0 |
| clearing dispatch | `scripts/validate-clearing-dispatch.py .` | 0 | 0 |
| former-id arrival | `scripts/validate-former-id-arrival.py .` | 0 | 0 |
| openRepoShape pin | `scripts/validate-openreposhape-pin.py --checkout <pinned checkout>` | 0 | 0 |
| openXdox pin | `scripts/verify-openxdox-pin.py` | 0 | 0 |
| openDox pin | `scripts/verify-opendox-pin.py` | 0 | 0 |
| wallet YAML syntax | `openXwallet/scripts/wallet-yaml-syntax-gate.py .` | 0 | 0 |
| openXwallet | `openXwallet/scripts/validate-openxwallet.py .` | 0 | 0 |
| factory identity | `scripts/validate-factory-identity.py .` | 0 | 0 |
| signed execution chain | `scripts/validate-signed-execution-chain.py . --require-pinned-wallet-vocabulary` | 0 | 0 |
| release tag gate | `scripts/validate-release-tag-gate.py .` | 2 at the bare tip; **0 on the merge tree** (note a) | 0 |
| proposal support | `scripts/proposal-support.py . verify` | 0 | 0 |
| sequenced-after | `scripts/validate-sequenced-after.py .` | 0 | 0 |
| sequenced-after ledger | `scripts/validate-sequenced-after.py . --ledger-diff` | 0 | 0 |
| code surface | `scripts/validate-code-surface.py .` | 0 | 0 |
| target release | `scripts/validate-target-release.py .` | 0 | 0 |
| manifest digests | `scripts/validate-manifest-digests.py .` | 0 (185 verify) | 0 (184 verify) |
| release verify-commit | `scripts/validate-contract-release.py verify-commit --commit HEAD` | **0** | 1 (note b) |
| doc-health | `scripts/doc-health.py --single-repo .` | 0 | 0 (note c) |

Every other gate's output is identical on the two sides once the checkout's
own path is set aside, apart from counts that the branch's new files explain:

- the manifest gate verifies the one new row;
- the openXwallet and signed-execution-chain repository scans each skip one
  more document as another kind, the added YAML file (the release inventory).

**Note a, the release tag gate.** Run on the bare branch tip, the gate compares
the tip with its first parent, the merge `24699ca5`. It reports "contract-v4.1
is declared and has no published annotated tag, 2 first-parent landing(s)
after the commit that declared it", because it counts the branch's own commits
after the cut as landings. That is not the tree CI judges.
`release-tag-gate.yml` runs on the pull request, whose checkout is the merge of
the branch into `main`. On that tree, emulated as `7ee4e874` in § 6, the gate
finds no error and no warning, only the owed-tag notice. On `main` itself, it
judges #1284's merge and finds no error and no warning.

**Note b, `verify-commit` on `main`.** `main` fails with
`HGR-RELEASE-DIGEST-MISMATCH` on seven `contract-v4.0` members:
`contracts/CHANGELOG.md`, `contracts/README.md`, `contracts/manifest.yaml`,
`scripts/hermes_runtime_validation/catalog.py`,
`scripts/hermes_runtime_validation/release.py`,
`scripts/validate-hermes-runtime-contracts.py` and
`scripts/validate-ideation-dashboard-contracts.py`. `main` has moved them
since `contract-v4.0` without a cut, and they are exactly the moves the
`contract-v4.1` changelog attributes to earlier pull requests. The branch
passes against its own inventory. The cut resolves this condition; the branch
does not cause it.

**Note c, doc-health.** The two reports differ only where the cut acts:

- **Release-inventory drift.** The branch has 4 fewer errors and 3 fewer
  infos (`main`: 31 critical, 26 error, 69 warning, 20 info; branch: 31
  critical, 22 error, 69 warning, 17 info). `main` reports seven
  release-inventory-drift findings, "bytes differ from the digest
  'contract-v4.0' records": four errors for the scripts above, and three infos
  for the editorial members. At the branch head, that family reports "No
  findings".
- **Word counts.** The draft row of the lifecycle table gains 2,783 words,
  this feature's documents. Canon words are equal, so the canon share reads
  39.2% against 39.3%.
- **No new finding.** The branch has no finding that `main` lacks, and neither
  side reports a new regression.

## 8. Tests (change task 2.7)

**`tests/factory-mcp/` at the head:** 108 passed, 300 subtests passed. `main`
has 88 tests and 203 subtests, so the feature adds 20 test methods and 97
subtests. All of them pass.

**The full suite, under `setsid` with its log polled.** The command was CI's
`pytest-suite` command (`python -m pytest tests/ -q -m "not postgres"`), with
JUnit output, `-rs` and a `--basetemp` outside the checkout. Both sides ran
concurrently on the same host:

| | Branch `6300772b` | `main` `9a272c6d` |
| --- | --- | --- |
| Result | 1 failed, **9546 passed**, 7 skipped, 338 deselected, 701 subtests passed | 1 failed, 9526 passed, 7 skipped, 338 deselected, 604 subtests passed |
| Wall time | 52:38 | 52:37 |

The two JUnit reports were compared test by test:

- **The same single failure on both sides.** It is
  `tests/doc-health/test_tag_hygiene_pinned_targets.py::test_a_lexically_malformed_value_builds_no_path_and_reads_nothing`.
  The cause is the environment: the test asserts that no argument on the read
  surface contains the substring `one`. The local checkout's absolute path
  contains that substring in a parent directory's name, so a legitimate
  fixture path (`…/fixtures/tag-hygiene-pinned/alpha`) matches. CI's checkout
  path does not contain it. Nothing on the branch touches the test or the
  module it exercises.
- **The same 7 skips on both sides**:
  - two wait on a later tranche (`ideation_dashboard`);
  - two run only in domain repositories (`conformance-gate`);
  - one needs a sibling domain checkout;
  - two need the pinned decision core (`PINNED_CORE_CHECKOUT`), which CI's job
    provides and a local run does not.
- **20 more test cases on the branch,** all in
  `tests.factory-mcp.test_factory_mcp_conformance.ConformanceTests`. None is
  only on `main`, and no shared test changed state.

**`doc-health-py314`'s command** (`python -m pytest tests/doc-health -q -rs`)
ran under Python 3.14.7, in an environment built from the same lock with
`--require-hashes --only-binary :all:`. Both sides gave 1 failed and 2156
passed, and the failure is the same environmental one as above.

## 9. Out-of-tree engineering check (change task 2.7; SC-008)

The engineering domain's repository is private, so this repository carries
none of its bytes. The check ran outside this tree, using only the validator's
`--snapshot` option. The snapshot was a read-only checkout of
`codeXfactory/codexFactory` at `33b916c12a1dcccf882557d6edcf396c98824f31`. Its
three published schemas (tool request, tool result, domain error) have the
digests the 2026-09-07 baseline records at `4b12ba83`. The schemas did not
move, as the runbook says this profile leaves them unchanged.

Four declarations were composed in scratch over those schemas:

- The result inventory points at the schema's classification vocabulary.
- The error inventory points at its error union, with `discriminator: code`,
  which yields eleven codes.
- Every value is mapped (two completed evaluations, eleven execution failures).
- Domain `engineering`, synthetic service fields only.

| Declaration | Validator at the branch head | `main`'s validator |
| --- | --- | --- |
| not deployed | `valid-with-gaps`, no diagnostic (gap `audit-gap`) | `valid-with-gaps`, no diagnostic |
| deployed, no `auth` block | **`invalid`: `hosted_auth_missing` at `/service`** | `valid-with-gaps`, no diagnostic |
| deployed, EdDSA-only block cited to an `auth` gap | **`invalid`: `auth_rs256_missing` at `/service/auth/algorithms`** | `invalid`: `schema_enum` at `/gaps/1/concerns/0`, `schema_oneOf` at `/service` |
| deployed, RS256 and EdDSA block cited to an `auth` gap | `valid-with-gaps`, no diagnostic (gaps `audit-gap`, `auth-gap`) | `invalid`: the same two schema codes |

Every run reported `verified_conformance: false`. These are the engineering
domain's expected signals:

- its schemas and outputs are unchanged;
- a not-deployed declaration validates as before;
- a hosted declaration without the block names the missing block;
- an EdDSA-only block names the missing RS256 algorithm.

No codex schema byte, private path or internal name entered this repository.

## 10. Hygiene (change task 2.7)

- `git diff --check origin/main...HEAD`: clean.
- **Closing-keyword scan.** The scan covered every commit message on the branch
  (`git log origin/main..HEAD`: nine commits and the merge) for a closing
  keyword followed by an issue or pull-request reference. It found none.
- **Public-repository scan.** The added lines were scanned for host-absolute
  paths, private repository paths and internal names. It found none.
- `specs/039-*` is absent from `main` (`git ls-tree origin/main specs/`).

T028, the draft pull request, its reviews and its threads, follows this
record. The realization lands only on Brett Heap's realization word (change
task 3.2).
