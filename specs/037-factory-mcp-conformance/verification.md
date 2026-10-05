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
