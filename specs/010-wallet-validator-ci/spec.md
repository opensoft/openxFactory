# Feature Specification: Wallet Validator CI Gate (S1)

**Feature Branch**: `010-wallet-validator-ci`

**Created**: 2026-08-23

**Status**: Draft

**Input**: User description: "S1 of the ratified OpenSpec change add-wallet-carried-review-authority (openxFactory @ 89b11ec): Wire the `validate-openxwallet` validator into CI as a required check."

**Governance source**: This feature realizes named successor **S1** of the ratified change
`openspec/changes/add-wallet-carried-review-authority` (@ 89b11ec). It adopts that change's
requirement text verbatim: *an intake entry with no reader confers nothing* — until the
validator is a required check on this repository, **no grant is operative** and no grant
property may be described in the present tense. Per the ratified substrate discipline,
S1 changes NOTHING about the grant schemas, the validator's rules, or any future register;
it only makes the existing, already-written validator impossible to bypass.

## Clarifications

### Session 2026-08-23

- Q: What tree scope must every PR's wallet-validation check evaluate, and how are intentionally-invalid example specimens treated so main stays green while malformed grants are still caught? → A: Whole-tree scan on every PR with exactly ONE named, path-scoped exclusion — `contracts/openxwallet/examples/negative/**` — implemented in the check's scoping layer (never as validator changes or a generic allowlist); the negative specimens there become the self-test corpus, with at least one validated per run outside the scan scope expecting explicit failure plus rule name.
- Q: Plan-phase discovery showed the validator natively implements both mechanisms the clarify rounds specified — layer 1 asserts every packaged negative fails for its declared reason on EVERY invocation; layer 2's whole-repo sweep already excludes packaged examples so negatives are never re-adjudicated as live records. Does the check still need its own scoping/self-test code? → A: NO — zero check-layer scoping code. FR-004 is satisfied by validator-native layer-1 corpus assertion each run; FR-009's single named exclusion is satisfied by the validator's pre-existing packaged-corpus exclusion (validator unchanged, no generic allowlist). Duplicating it would be dead code. Factual correction recorded: the negative corpus numbers 29 specimens, not 18 (earlier figure came from a truncated name-only listing).
- Q (CONVENER AUTHORIZATION, amends the zero-code ruling above for this hole only): QA proved layer 2 skips syntactically unparseable YAML as "another kind", so a live grant with broken syntax escapes the sweep. Convener ruling 2026-08-23: "authorized hardening." → A: Add FR-011 — a kind-aware syntax gate as a committed helper script (`scripts/wallet-yaml-syntax-gate.py`) that fails the check when any `*.y*ml` file referencing a family kind string fails to parse; vocabulary is imported from the validator module (no parallel copy); unrelated broken YAML keeps current skip semantics; validator still untouched. Companion convener ruling: enforcement-plane mitigation via `.github/CODEOWNERS` routing gate paths to @brettheap (routing-only).
- Q: What is the canonical CI check name, and where does FR-007's operator instruction live? → A: Check name `wallet-validation` (the spec's own token from SC-001 — distinct from the validator *tool* name, because branch protection pins the literal string forever and a mismatch silently de-advises the gate); instruction lives as a top-level README section, reachable in under a minute post-merge without knowing which workflow file exists.
- Q: Validator exits zero with non-fatal warnings — pass or fail? And what wall-clock budget before fail-closed on hang? → A: Warnings PASS with log-only treatment (converting them to failures would re-tighten rules the unmodified validator does not enforce, against FR-002); explicit 10-minute budget, then fail-closed (runner defaults are ~hours, making hangs untimely and indistinguishable from slowness).
- Q: Is the trigger matrix correct and complete for S1 — PRs to main incl. drafts; no push-to-main runs; no scheduled runs? → A: CONFIRMED, no changes. The ratified gate is defined solely at the PR plane; push-plane gaps are operator settings acts (PART III pattern), and adding triggers now would exceed the verbatim adopted successor text — scope creep toward S2–S5 enforcement surface.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A malformed grant can no longer enter the tree unnoticed (Priority: P1)

A contributor (human or agent) opens a pull request whose diff introduces a wallet grant
artifact that violates the openxwallet contract family — wrong fields, missing required
scope, bad enum values, anything the existing `validate-openxwallet` validator rejects.
The CI check runs automatically on the PR, reports the offending file and the violated
rule by name, and fails. The defect is visible before review, not after.

**Why this priority**: This is the entire point of S1. The ratified doctrine leans on
rules that today run "only when a human types the command"; until they run on every PR,
the doctrine describes controls that do not control. This story converts description into enforcement.

**Independent Test**: Commit a deliberately malformed grant fixture, open a PR, observe
the check fail naming the file and rule. Fully testable without any other story landing.

**Acceptance Scenarios**:

1. **Given** a PR containing one malformed grant artifact, **When** CI completes, **Then**
   the wallet validation check FAILS and its log names the offending path and the violated rule.
2. **Given** the failing check, **When** the contributor fixes the artifact, **When** CI
   re-runs, **Then** the same check turns green without any manual intervention.
3. **Given** any PR to main, **When** CI completes, **Then** the wallet validation check
   has RUN (presence of a result is itself required — a skipped or absent check is a defect).

---

### User Story 2 - Conforming content passes with zero false positives (Priority: P2)

All currently-conforming wallet artifacts in the tree — the contract family's example
specimens included — pass the check on every PR. Routine documentation, workflow, and
contract work that touches nothing wallet-related also passes. The gate never becomes
noise that contributors learn to ignore.

**Why this priority**: A required check that false-fails trains the sole developer to
bypass it (`--admin` ritual), recreating the exact deadlock the parent change exists to end.

**Independent Test**: Open a PR containing only unrelated changes plus the existing
example artifacts; observe the check pass.

**Acceptance Scenarios**:

1. **Given** the current tree's wallet example artifacts, **When** the check runs, **Then**
   it PASSes, exactly matching the verdict a knowledgeable human gets invoking the
   validator manually today.
2. **Given** a PR that touches no wallet-related path at all, **When** CI completes,
   **Then** the check PASSes in comparable time to the repo's other checks.

---

### User Story 3 - The check becomes un-bypassable at merge time (Priority: P3)

After the feature lands and the human operator flips the repository setting that marks
the check as required, no pull request to main can be merged while that check is red,
missing, or pending — including merges performed through the web interface. Until the
operator performs that act, the check runs on every PR but remains advisory, and the
feature documents the exact remaining step.

**Why this priority**: Enforcement-at-merge is what makes the check "required" in the
ratified sense, but the enabling configuration is a repository-settings act owned by the
operator (assembly-class surfaces stay permanently human-only per PART III); the code
deliverable is complete when the check is correct and the instruction is exact.

**Independent Test**: With required status configured, attempt to merge a PR with a red
check through the UI; observe refusal. Without it, observe the documented advisory state.

**Acceptance Scenarios**:

1. **Given** the operator has marked the check required, **When** a PR's check is red,
   **When** merge is attempted via UI or CLI, **Then** the merge is refused.
2. **Given** the feature is merged but the operator has not yet marked the check required,
   **Then** the feature's documentation states precisely which setting, on which branch,
   names which check — such that the act takes under a minute.

---

### Edge Cases

- What happens when the validator itself crashes, hangs, or is missing from the checkout?
  The check FAILS — fail-closed, never degrade-open (Constitution Principle VII).
- What happens when a future change adds a new wallet artifact kind the validator does not
  recognize? Out of scope here; the check simply applies whatever the (unchanged)
  validator decides. This feature adds no rules and changes none.
- What happens when someone adds a file under `contracts/openxwallet/examples/negative/`?
  It lands inside the single named exclusion, so it is invisible to routine scans by
  design — which is exactly why any diff touching that directory must be treated as a
  review-visible event (FR-009), and why the FR-004 self-test keeps the corpus load-bearing.
- What happens on draft PRs? The check runs like any other status check; draft status
  confers no exemption.
- What about direct pushes to main? Out of scope for this feature; the repo's existing
  push protections (if any) govern, and tightening them is an operator settings act.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The CI system MUST run the wallet validation check automatically on every
  pull request targeting main.
- **FR-002**: The check MUST evaluate the tree using the EXISTING `validate-openxwallet`
  validator, unmodified; this feature MUST NOT alter the validator's rules, schemas, or
  any contract bytes (that would belong to a different change).
- **FR-003**: When validation fails, the check output MUST name each offending file path
  and the specific violated rule, sufficient for a contributor to fix without consulting
  the validator's source.
- **FR-004**: The check MUST run an automated self-test on every invocation: the validator
  is invoked over at least one specimen from `contracts/openxwallet/examples/negative/`
  (outside the scan scope) and the check PASSES only if that invocation FAILS with an
  explicit rule attribution. The existing negative-specimen corpus serves as this fixture
  set; no new fixture artifact is invented.
- **FR-005**: The check MUST pass on the current tree as-is: every wallet artifact outside
  the single named exclusion conforms per the validator's own semantics.
- **FR-006**: Any validator non-zero exit, timeout, or execution error MUST surface as
  check FAILURE (fail-closed). The check MUST impose an explicit 10-minute wall-clock
  budget on the validation step; exceeding it fails the check rather than hanging until
  a runner default kills it.
- **FR-010**: Validator output emitted as non-fatal warnings at exit zero MUST pass the
  check and be logged only — the check MUST NOT convert warnings into failures (that
  would re-tighten rules the unmodified validator does not enforce, against FR-002).
- **FR-011** (convener-authorized hardening, amending the Q5 zero-code ruling for this
  hole only): The check MUST run a kind-aware YAML syntax gate — a committed helper
  script that fails the check, naming file and parse error, for any `*.y*ml` whose raw
  text references an openxwallet family kind string yet fails `yaml.safe_load_all`.
  Family vocabulary MUST be imported from the validator module (no parallel copy);
  files that fail to parse WITHOUT referencing family kinds keep the validator's
  existing skip semantics; the validator itself remains untouched (FR-002).
- **FR-007**: The check MUST be named exactly `wallet-validation`, and the feature MUST
  leave a top-level README section stating the single operator act (the active ruleset
  governing main OR a classic branch-protection rule — whichever enforces this repo;
  repository setting, branch, the literal check name `wallet-validation`) that upgrades
  the check from advisory to required, for execution after merge.
- **FR-008**: The check MUST NOT read, create, or require the authority register (that is
  S4's deliverable and must not be pre-created here).
- **FR-009**: The scan scope MUST implement exactly one named path-scoped exclusion
  (`contracts/openxwallet/examples/negative/**`) in the check layer. Generic exemption
  mechanisms, per-file allowlists, and validator-side changes are forbidden; any addition
  under the excluded directory remains a fully visible diff in review.

### Key Entities *(include if feature involves data)*

- **Grant artifact**: a document expressing an openxwallet grant (audience, scope acts/
  objects, authority tier, expiry, issuer, derivation). In this feature it appears only
  as (a) existing example specimens and (b) the negative fixture.
- **Validator**: the repo's existing `validate-openxwallet` checker. Reused verbatim.
- **Check result**: the CI status produced per PR — green, red with named findings, or
  red-by-malfunction (all three observable).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of pull requests to main carry a wallet-validation check result —
  verified over the next N≥5 merged-or-opened PRs after landing.
- **SC-002**: A PR containing the negative fixture fails the check on its first CI run,
  with file-and-rule attribution in the log (rehearsed during implementation, evidence committed).
- **SC-003**: Zero false failures across the existing example artifact set, demonstrated
  by a green check on the landing PR itself.
- **SC-004**: After the operator's one-time settings act, a UI merge attempt against a red
  check is refused — rehearsed once and recorded as realization evidence per the parent
  change's archive-on-green-evidence discipline.

## Assumptions

- The existing `validate-openxwallet` validator is functional when invoked manually today
  (per the ratified proposal's honest-current-state finding); this feature wires it, does
  not repair it. If wiring exposes latent defects, they are dispositioned as findings, not
  silently patched.
- ~~The contract family's example artifacts are meant to pass validation as-is; if any
  specimen is intentionally invalid as a teaching device, the check's path scoping will
  account for it — surfaced and decided at clarify, not assumed silent.~~ RESOLVED by
  Clarification Session 2026-08-23: the corpus contains 29 intentional negative specimens
  under `examples/negative/`; handled by FR-004/FR-009, not an open assumption.
- Marking the check "required" in repository settings is a post-merge human operator act
  (PART III floor: assembly-class surfaces human-only); the code deliverable is the check
  plus the exact instruction, not the settings mutation.
- Direct pushes to main, scheduled runs, and other triggers beyond PRs are out of scope;
  the parent change requires the gate at the PR plane where candidates are reviewed.
