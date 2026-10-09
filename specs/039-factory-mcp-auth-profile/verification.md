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
