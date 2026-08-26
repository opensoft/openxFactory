# Research — 010-wallet-validator-ci

Phase 0 output. Every NEEDS CLARIFICATION from Technical Context was resolved during
discovery (no open unknowns entered planning). Decisions recorded with rationale.

## R1 — Dedicated workflow file vs extending existing workflows

**Decision**: New dedicated `.github/workflows/wallet-validation.yml`.

**Rationale**: The repo's two existing workflows are specialized —
`doc-health-reusable.yml` is a `workflow_call` reusable driven by the aggregation repo's
scheduler; `session-open-pr.yml` is a `workflow_dispatch` authorship route. Neither is a
pull_request gate, and FR-007 requires a stable standalone check name for branch
protection. A dedicated file isolates blast radius and makes the required-status string
unambiguous.

**Alternatives considered**: Extending `doc-health-reusable.yml` — rejected: it is
called by an external scheduler with its own inputs/permissions model; coupling a merge
gate into it would entangle two unrelated governance surfaces.

## R2 — Validator invocation and the `--strict` question

**Decision**: Run `python3 scripts/validate-openxwallet.py .` — positional repo path,
NO `--strict`.

**Rationale**: Verified at `scripts/validate-openxwallet.py:1389-1412`:
`report()` returns exit 1 on errors, or on warnings ONLY when `--strict` is passed.
Clarification Q3 ruled warnings pass log-only (FR-010), so `--strict` must be omitted.
A malformed LIVE artifact is always an *error* (exit 1) regardless of strict mode, so
the S1 gate ("a deliberately malformed grant fails the PR") holds without it.

**Alternatives considered**: Passing `--strict` for extra toughness — rejected: it
would re-tighten rules the unmodified validator does not enforce, violating FR-002's
spirit and Q3 verbatim.

## R3 — Self-test mechanism (FR-004)

**Decision**: No new test fixture or harness. The validator's layer 1 already asserts,
on every invocation, that every packaged negative specimen under
`contracts/openxwallet/examples/negative/` FAILS for its own declared
`expected_failure:` reason (with optional detail pin and requirement attribution),
with closed coverage in both directions (every requirement probed; every claimed
requirement id exists).

**Rationale**: Discovered in the validator header (`--docstring`, lines 1–40). Building
a parallel fixture would duplicate an existing control and touch nothing this feature
may touch anyway (FR-002).

**Consequence**: Spec trued-up via Clarifications Q5 — FR-004 is satisfied by
validator-native semantics; the check layer contributes zero scoping/self-test code.
Also corrected a factual slip: the negative corpus numbers **29** specimens, not 18
(the earlier figure came from a truncated name-only listing).

## R4 — Scoping / exclusion mechanism (FR-009)

**Decision**: Rely on the validator's built-in packaged-corpus exclusion in its layer 2
sweep; add ZERO exclusion logic in the workflow.

**Rationale**: Layer 2 sweeps REPO_PATH for family-kind YAML documents while excluding
the packaged examples "so a whole-repo sweep does not re-adjudicate the negatives as
though they were live records" (validator docstring). This IS the single named
path-scoped exclusion FR-009 mandates — pre-existing, validator-owned, unchanged.
Duplicating it in the check would be dead code against the least-complexity principle.

**Alternatives considered**: Check-layer pruning/copying of the tree to hide
`examples/negative/` from the sweep — rejected as redundant machinery with its own
failure modes; architect blessed zero-scoping-code explicitly (R5 consult).

## R5 — CI runtime conventions

> **SUPERSEDED-IN-PART (2026-08-23, post-review):** the dependency install is now
> `pip install pyyaml jsonschema rfc3339-validator` (validator hard-requires all
> three; reviewer finding, clean-venv parity proven) and permissions grant
> `contents: read` (checkout token requirement). Trigger matrix, runner, checkout
> pin, unnamed-job naming, and the 10-minute budget stand as originally ruled.

**Decision**: Mirror `doc-health-reusable.yml`: `runs-on: ubuntu-latest`,
`actions/checkout@v4`, `actions/setup-python@v5` with Python `"3.12"`, plus
`pip install pyyaml` (verified hard dependency: the validator exits 2 without PyYAML).
Job-level `timeout-minutes: 10` (FR-006). Job left unnamed so the displayed check name
defaults to the workflow name — the literal `wallet-validation` token branch protection
will pin (architect execution note: a distinct job display name is the classic silent
de-advisation bug). Least-privilege permissions — originally `{}`, corrected to
`contents: read` post-review (see R5 supersession note); matches the
`session-open-pr.yml` precedent of an explicit minimal grant.

**Rationale**: Consistency with the only existing pull-repo CI surface; minimal
novelty; every pin copied from an in-repo precedent rather than invented.

## R6 — Trigger matrix

**Decision**: `on: pull_request` with `branches: [main]` and default types
(`opened`, `synchronize`, `reopened`) — drafts included; no push, no schedule, no other
triggers.

**Rationale**: Clarification Q4 confirmed verbatim; the ratified gate lives at the PR
plane, and adding triggers now was ruled scope creep toward S2–S5 enforcement surface.

## R7 — Invalid-YAML fail-open hardening (convener-authorized)

**Decision**: Committed helper `scripts/wallet-yaml-syntax-gate.py` (architect option C),
invoked by the workflow BEFORE the validator sweep; plus `.github/CODEOWNERS` routing
`.github/workflows/**`, `/scripts/validate-openxwallet.py`, and the helper itself to
@brettheap.

**Rationale**: QA proved layer 2 skips unparseable YAML as "another kind"
(`validate_openxwallet.py:1353-1355,1384`) — a live grant with broken syntax escapes.
Convener authorized hardening 2026-08-23 (amends Clarification Q5's zero-code ruling for
this hole only). Inline-heredoc variant rejected: untestable outside CI, quoting-fragile
in the exact mechanism whose job is parsing; Constitution V wants deterministic,
reviewable evidence. Whole-tree strict parse (option A) rejected: wider than the ruled
hole and a false-fail generator across ~1500 documents against US2's zero-false-positive
floor. The helper imports `KIND_TO_SCHEMA` from the validator module via importlib
path-load (hyphenated filename blocks plain import) so no parallel vocabulary exists and
future kinds auto-track. CODEOWNERS routes the helper itself too — the fix cannot change
without owner review.

**Alternatives considered**: upstream validator fix — deferred to its own change (FR-002
wall stands); blocking S1 on it — rejected by convener in favor of authorized hardening.
