# Implementation verification

Status: record
Kind: report
Date: 2026-09-07
Lane: mcp-family-contract

## Authority and planning

Brett ratified both exact proposals and their ad-hoc origins with “yes”; [the approval record](../../openspec/changes/add-factory-mcp-conformance/review/ratification-2026-09-07.md) retains the reviewed revision and full approval question. This feature started from the clean locally committed ratified design branch. The canonical git extension allocated 030-factory-mcp-conformance; implementation ran in that generated worktree. (Renumbered to 037-factory-mcp-conformance on 2026-10-05 for opensoft/openxFactory#1242, because main had taken 030 on 2026-09-08; see the dated addendum in the change's tasks.md.) Relative Git plumbing allows host and container to use the same worktree. No agent-prefixed implementation branch or consumer pin was created.

Clarify found no material unanswered decision within the ratified first slice. Spec, plan, research, data model, interface, six domain requirements checklists and tasks were analyzed before behavior implementation. All eight requirements have tasks; no orphan task, authority conflict or critical cross-artifact finding was identified. Operational reader/cancellation, hosting, adoption, release and audit infrastructure remain explicitly deferred by the ratified design. Optional auto-commit hooks were not enabled; scoped local commits preserve the result.

## Behavioral evidence

Runtime: py-bench, Python 3.12.3, jsonschema 4.25.1. Tests use synthetic data, temporary local files and injected clocks; they require no credentials, network observations or sleeps.

- Before implementation, all 11 initial tests failed because the validator module did not exist.
- Final focused suite: **16 tests passed** with additional adversarial subcases. Command: `python3 -m unittest discover -s tests/factory-mcp -q`.
- Packaged example CLI: exit 0, valid-with-gaps, all three checks true, explicit audit-gap, verified_conformance false.
- Explicit socket-denial test proves remote references refuse without attempting network access.

| Requirement | Witness (test method names omit test_ prefix) |
| --- | --- |
| FR-001 | closed_shapes; support_and_unique_identity |
| FR-002 | reference_integrity; symlink_escape; contained_local_reference_is_pinned; nested_remote_and_bad_local_reference; reference_checks_never_open_network; recursive_local_schema_without_fetch |
| FR-003 | closed_shapes; support_and_unique_identity |
| FR-004 | closed_shapes; support_and_unique_identity; repetition_cross_checks |
| FR-005 | outcomes_exhaustive_and_typed; unresolvable_vocabulary_requires_gap; unsupported_constraints_do_not_claim_exhaustiveness |
| FR-006 | support_and_unique_identity; valid_with_gaps_is_not_certification |
| FR-007 | repetition_cross_checks |
| FR-008 | cli_exit_codes; valid_with_gaps_is_not_certification; source-pinned codex baseline and runbook review |

## Repository checks and limits

- Strict OpenSpec: **97/99 pass**. The new change passes. Two existing unrelated failures remain: add-chain-attestation omits “a tranche-two link does not exist yet”; add-composed-view-authoring omits “Gate verbs hide on a composed view”. Neither source delta was modified by this feature.
- Targeted doc-health: status-validity retains 3 existing errors; proposal-origin has zero findings. These match the proposal-stage baseline; no finding concerns this MCP change.
- The 14-document brainstorm packet was validated at the proposal checkpoint; implementation leaves those documents unchanged.

The earlier [proposal validation record](../../openspec/changes/add-factory-mcp-conformance/review/validation-2026-09-07.md) names the baseline findings. Whole-repository cleanliness is not inferred from a passing new capability test. No unrelated baseline document was edited to make checks green.

## Review and corrections

An explicit standard-library resource-URI check preserves absolute service identity validation even when optional JSON Schema format checkers are absent; a test removes them to prove the boundary.

Local diff review checked the request/reference trust boundary, closed schemas, refusal classification/order, provenance, bounded output, deterministic identities and release scope. Corrections incorporated before this checkpoint: strict end-of-string schema patterns; conservative finite-vocabulary handling instead of unsupported exhaustiveness; explicit not-run report dimensions; separate prior/proposed TTL bounds; and canonical YAML realization metadata.

The repository realization-axis validator requires code_surface and target_release in leading YAML front matter. The original packet placed them in body text. This implementation corrects the format: code_surface names the owning repository and paths; target_release uses the existing “implemented” target token, annotated as future reviewed main-line realization. It does not claim that merge, release or deployment occurred. Proposal lifecycle prose now reflects the recorded ratification; original reviewed bytes remain in Git history. No design requirement or approved origin was changed.

## Closure state

The local implementation and deterministic verification are complete. Formal repository review, merged-green realization and OpenSpec archive remain open governance tasks. No PR was opened, branch pushed, release allocated, artifact accepted, credential obtained, endpoint deployed or consumer pin advanced by this implementation.

## Addendum 2026-10-05: on main (opensoft/openxFactory#1242, pull request #1243)

Lane openxfactory-5 (openXfactory-5) brought this feature onto main by merging
`d2baf6fd`, renumbered it from 030 to 037, and realigned the validator with
requirements already ratified. The change's tasks.md addendum lists every
repair; none changed requirement or scenario text. The closure state above is
the Codex lane's record of 2026-09-07; this addendum supersedes it for the
pull request.

### Red first

Every row's tests were committed and run against the unfixed validator before
the fix was written.

| Round | Tests committed | Result against the unfixed validator | Fix | Result after |
| --- | --- | --- | --- | --- |
| Review findings H2, H3, M1, M7, L1-L5 | `d8b2e0cb` | 96 failed, 23 passed (tests and subtests) at `71013ba4` | `59fbab7b` | 51 passed, 85 subtests passed |
| Copilot review 5419026094 (10 threads) | `94ca87e1` | 12 failed | `c9dbaa9b` | 59 passed, 91 subtests passed |
| Copilot review 5419154777 (5 threads) | `91507eec` | 9 failed | `c96d1894` | 64 passed, 98 subtests passed |
| Copilot review 5419262363 (4 threads) | `7fb10867` | 4 failed | `6a1f6d1c` | 68 passed, 100 subtests passed |
| Copilot reviews 5419355635 and 5419477722 (5 threads) | `b080a3a8` | 13 failed (tests and subtests) | `754d94bc` | 72 passed, 117 subtests passed |
| Copilot review 5419809508 (3 threads) | `66b610b6` | 11 failed; union coverage peaked at 64 MB on a 29 KB schema | `a12c7027` | 74 passed, 141 subtests passed; peak 1.2 MiB (4.7 MiB at four times the layers) |
| Copilot review 5421098780 (2 threads and one finding in the review body) | `67558dbe` | 7 failed; 267,776 resolver calls for 512 shared aliases | `bc2e387e` | 77 passed, 149 subtests passed; 3,072 resolver calls (6,144 at twice the aliases) |
| Copilot review 5421267903 (1 thread and one finding in the review body) | `d4177714` | 5 failed | `d3a9e05b` | 79 passed, 156 subtests passed |

`5d0ea5de` split the validator into phase functions with no behaviour change.
Copilot review 5420018661 at `a12c7027` reported no findings. Every review
thread was answered and resolved.

### Out of tree, against the real schemas

These ran read-only, from existing snapshots, and copied nothing into this
repository. A faithful codex declaration at `4b12ba83` and the Ops DNS proposed
fit at `6b7cdaa6` both return `valid-with-gaps`, with only their scope and
audit gaps, once the error inventory names `discriminator: code`. Without the
discriminator, both return `unresolved_inventory_without_gap`. With one codex
code unmapped, the result is `incomplete_outcome_mapping`.

Correction: the messages of `5d0ea5de`, `c9dbaa9b`, `c96d1894` and `6a1f6d1c`
say these probes gave unchanged output. When they were written, the probe was
loading the validator from a clone still at `b8c0d5e2`. It was then re-run
against each of those commits' own validator and declaration schema, extracted
with `git archive`, and against `754d94bc`, `a12c7027`, `bc2e387e` and
`d3a9e05b`. Every report is byte-identical, so the statements hold. The review's adversarial probe, which
always loaded the right tree, refuses P3, P3b, P4, P6, P7, P8, P9 and P17 with
located codes.

### Full CI command

`python3 -m pytest tests/ -q -m "not postgres"`, run in two full clones of the
same kind, with the CI lock's packages installed with hashes:

- At `a12c7027` against main `0f2a87f6`: no test newly fails, none newly
  passes, and the skips are the same (7 on both). There are 74 new testcases,
  all in `tests/factory-mcp`. The same diff at `b8c0d5e2` against `12753f27`
  was also clean.
- Three tests fail on BOTH sides, and in isolation on both. None is caused by
  this branch:
  - `test_the_bare_unittest_route_is_detected_as_unguarded` needs pytest's
    basetemp under `TMPDIR`; with it, the test passes on both sides.
  - `test_a_lexically_malformed_value_builds_no_path_and_reads_nothing` reads
    the clone root through a symlinked workspace path.
  - `test_release_mode_field_is_preserved_on_the_real_repository` hit a
    subprocess timeout on a loaded host.
  The required `pytest-suite` check runs in CI, without any of these local
  conditions.
- After `a12c7027`, the commits change only `scripts/validate-factory-mcp.py`,
  its test module, the runbook and this feature's Markdown. At `1f9e3d7e`, the
  test files that read the corpus, plus the factory-mcp module, ran again:
  2974 passed, and the only failures were the two environment tests above.
  At `d3a9e05b`, the factory-mcp module passes (79 tests, 156 subtests). CI's
  required `pytest-suite` runs the full command at the pull request's final
  head.

### Gates

At `a12c7027` against main `0f2a87f6`, in clones of the same kind:

- Pinned OpenSpec `--all --strict`: exit 0 on both. The branch passes 111 of
  112 items and main 110 of 111. The single remaining item is the same
  accepted exception on both (`add-chain-attestation`, Brett Heap 2026-09-05).
  `--change add-factory-mcp-conformance --strict` passes clean.
- doc-health `--single-repo`: 31 critical, 26 error, 69 warning and 20 info
  findings on both, with no new regression. The only differing line is the
  informational draft count (71 drafts against 70).
- `validate-sequenced-after.py` and `--ledger-diff`: exit 0 on both.
- These validators exit 0 on both: code-surface, target-release, scope-globs,
  manifest-digests, pin-registrations, ideation-routing and document-catalog.
  code-surface and target-release differ only in counting this change's
  proposal.
- ideation-cross-reference (exit 1) and contract-release (exit 2) give
  byte-identical output on both sides; neither result comes from this branch.
