# Clarify Questions: AVC Reference Runtime (003-avc-reference-runtime)

**Spec**: [spec.md](./spec.md)
**Generated**: 2026-07-11
**Question count**: 8
**Status**: Answered inline; ready for the track agent to encode into `spec.md`.


## Accepted Answers

**Answered**: 2026-07-10 (America/Los_Angeles)

**Decision summary**: `Q1=A; Q2=A; Q3=A; Q4=A; Q5=Custom; Q6=A; Q7=A; Q8=A`.

### Q1: A

Use `pytest` with pinned test-only dependencies. Use parametrization for the
ARR/ACR matrix and `pytest-randomly` with recorded multiple seeds to prove the
suite is order-independent. A failing seed must be reproducible from reported
output.

### Q2: A

Target Python 3.11 or newer, matching the existing `xfactory/` floor. Do not use
3.12-only syntax in the reference package.

### Q3: A

Keep `xfactory/avatar_runtime/` stdlib-only. Tests and repo validators may use
pinned repo-approved test dependencies, including PyYAML, jsonschema, pytest,
and pytest-randomly. The boundary validator enforces that test/provider/network
dependencies are not imported by the runtime package.

### Q4: A

Add deterministic AST/import/export/file-surface boundary tests and a standalone
`scripts/validate-avatar-runtime.py` repo gate. It must detect provisional-test
imports, network/provider SDKs, listeners, application factories, persistence,
credential loading, deployment files, and forbidden entrypoints without relying
on code execution.

### Q5: Custom - consume the shared baseline map; do not duplicate it

During parallel work, the conformance checker reads the versioned
`openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml`
from `avatar-client-parallel-v1`, verifies its source commit and digest, and
derives the applicable `ACR-*` set from it. At realization it switches to the
digest-pinned released `contracts/avatar-client/acceptance-map.yaml`. The Q6
mapping artifact records explicit non-applicability dispositions. Do not keep a
second hand-maintained ACR enumeration under the runtime tests.

### Q6: A

Create a checked-in mapping such as
`tests/avatar_runtime/conformance/scenario-test-map.yaml` from each required
ARR/ACR scenario ID to one or more collected pytest node IDs, or to an allowed
non-applicability disposition with rationale. The conformance checker compares
that artifact with the acceptance maps and the collected test set and fails on
missing, duplicate, dangling, skipped-required, or unknown mappings.

### Q7: A

Record the five release coordinates and final conformance results in
`tests/avatar_runtime/conformance/realization-pin.yaml`, with explicit
`schema_version` and `kind`. Keep it inside the runtime-owned test surface and
validate it as part of final conformance.

### Q8: A

Add `scripts/validate-avatar-runtime.py` to the README validator index and run it
plus the deterministic pytest suite for every feature commit and before push.
This is the narrow governance exception to the runtime/test implementation
paths; it must not edit any sibling-owned contract, F0, UI, domain, deployment,
or release-metadata path.

The spec derives from the ratified OpenSpec change `implement-avatar-reference-runtime`,
whose `proposal.md`/`design.md` already pin most behavior (injected ports, non-deployable
boundary, provisional-adapter location, snapshot barrier, five-second revocation bound,
credential-free terminal replay, etc.). The questions below therefore raise **only material
ambiguities** that would change planning or implementation, prioritized
scope > authority/security > acceptance evidence > sequencing. Repo reality grounding the
recommendations: `xfactory/` already exists (uses `datetime.UTC` → Python 3.11+, `from
__future__ import annotations`, dataclasses); there is **no** `tests/` tree, no test
framework, and no packaging config; repo checks are standalone `scripts/validate-*.py`
(stdlib + PyYAML/jsonschema), indexed in the README and gated by constitution Principle V.

---

## Q1: Test framework and conformance runner

**Category**: Constraints & Tradeoffs (build tooling)

**Context** — spec Assumptions: "The reference implementation and its deterministic tests
use the openxFactory-standard reference-code tooling named by the source change." But the
repo currently has no `tests/` tree, no `pytest`/`unittest` config, and no test runner; the
entire deliverable is a deterministic suite under `tests/avatar_runtime/`.

**Question**: What framework/runner hosts the deterministic suite, given SC-003 requires
identical results across repeated **and randomized-order** runs?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | `pytest` (Recommended) | Ubiquitous; parametrization + fixtures fit the 34 ARR-/ACR-* matrix; randomized order via `pytest-randomly` directly serves SC-003; adds a dev dependency (test-only, not in the runtime core). |
| B | stdlib `unittest` | Zero third-party dependency, matches the dependency-averse core; more boilerplate for the large parametrized matrix; randomized-order rerun must be hand-built. |
| C | Extend the repo's `scripts/validate-*.py` pattern into a bespoke conformance harness (no framework) | Consistent with existing gate scripts and Principle V wiring; but reinvents discovery/assertion/reporting and is costlier to maintain. |
| Custom | Provide your own answer | Explain the runner and how randomized-order determinism (SC-003) is proven. |

---

## Q2: Python version baseline

**Category**: Constraints & Tradeoffs

**Context** — the spec sets no version floor; existing `xfactory/memory_gateway.py` uses
`datetime.UTC` (added in 3.11), `from __future__ import annotations`, and `@dataclass`, with
no `match` statements.

**Question**: What minimum Python version does the reference runtime target?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | 3.11+ (Recommended) | Matches the de facto floor already in `xfactory/` (`datetime.UTC`); enables dataclasses, `Self`, exception groups; broadly available. |
| B | 3.12+ | Newer typing/`type`-alias ergonomics; narrows target environments and exceeds current repo usage. |
| C | 3.10+ | Enables `match` for declarative state tables and widest compatibility; but below the existing `datetime.UTC` usage, forcing a refactor of shared helpers. |
| Custom | Provide your own answer | Name the exact floor and any language features it unlocks/forbids for the state machines. |

---

## Q3: Dependency policy — runtime core vs tests

**Category**: Integration & External Dependencies / Boundary

**Context** — FR-001: the package "MUST expose no network listener, application factory,
deployment manifest, persistent repository, provider-credential loading, or live provider
SDK." Existing `scripts/validate-*.py` already import third-party `PyYAML`/`jsonschema`.

**Question**: What third-party dependency policy applies to the runtime package versus its
tests?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Runtime package = stdlib-only; tests may use repo-approved libs (PyYAML/jsonschema + the chosen test framework) (Recommended) | Keeps the non-deployable core trivially dependency-free and easy to prove at the boundary; lets tests validate canonical fixtures with libs the repo already uses. |
| B | Both runtime and tests stdlib-only | Maximal purity and simplest boundary proof; canonical-fixture (YAML / JSON-Schema) validation must be hand-rolled in tests. |
| C | Both may use repo-approved third-party libs | Most convenient; weakens the "no SDK / trivially non-deployable core" guarantee behind FR-001/SC-005. |
| Custom | Provide your own answer | State the allowed dependency set for core vs tests and how the boundary check enforces it. |

---

## Q4: Boundary and provisional-import kill-proof mechanism

**Category**: Security & Non-Functional / Verification

**Context** — FR-004: "import-boundary validation MUST fail if any reference module imports
the provisional path"; FR-001 requires scanning imports, exports, entrypoints, and files for
deployment surfaces; SC-010: a reviewer can confirm every boundary "from automated boundary
output alone."

**Question**: How is the boundary + provisional-import prohibition evidenced and enforced?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | A dedicated automated boundary test doing a static AST/import scan, plus a repo-gate script `scripts/validate-avatar-runtime.py` (Recommended) | Static scan is deterministic and needs no execution; the `validate-*.py` script matches the Principle V gate + README-index convention and surfaces SC-010 output standalone. |
| B | Automated boundary test only (inside the suite), no separate gate script | Simpler, single location; not surfaced as a standalone repo validator for the shared gate. |
| C | Runtime import-guard that raises on a forbidden import at load time | Catches violations at execution; not a static guarantee and misses modules that are never imported at runtime. |
| Custom | Provide your own answer | Describe the detection method (static vs runtime) and where it plugs into the gate. |

---

## Q5: Applicable-ACR set — source of truth before kernel release

**Category**: Integration & Versioning / Acceptance evidence

**Context** — spec Assumptions: "The authoritative set of applicable ACR-* scenarios is
defined by the released kernel's acceptance map. Until release, the
`avatar-client-parallel-v1` provisional baseline and its stable acceptance IDs stand in."
The kernel and its `ACR-*` list are **not** present in this worktree.

**Question**: Where does the implementer read the concrete list of applicable `ACR-*` IDs
during parallel work, so US2/SC-002 ("every applicable ACR-* mapped") is provable before the
kernel lands?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | A checked-in ACR ID enumeration inside `tests/avatar_runtime/provisional/` mirroring `avatar-client-parallel-v1`, swapped at realization for the released kernel acceptance-map (Recommended) | Gives a concrete, versioned target now; final swap is a digest-pinned file change, keeping the provisional/canonical seam clean. |
| B | A standalone provisional ACR-list fixture (e.g. YAML) under `tests/avatar_runtime/`, referenced by both the adapter and the mapping checker | Decouples the list from adapter code and is easy to diff; one more artifact to keep in sync with the adapter. |
| C | Defer: map only `ARR-*` during parallel work; enumerate `ACR-*` from the released kernel at realization | Simplest now; but SC-002 "every applicable ACR mapped" stays unprovable until the kernel lands, deferring risk to realization. |
| Custom | Provide your own answer | Name the artifact/path that enumerates applicable ACR IDs pre-kernel and how non-applicable ones are dispositioned. |

---

## Q6: Acceptance ID → test mapping enforcement

**Category**: Completion Signals / Acceptance

**Context** — FR-034: "conformance MUST fail on any missing mapping, skipped required case,
nondeterministic result, or prohibited path modification." The acceptance map declares
`evidence_id_template: TEST-{scenario_id}`.

**Question**: How is the ARR/ACR-to-test mapping made machine-checkable so a missing mapping
fails conformance (rather than passing silently)?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | A checked-in mapping artifact (`scenario_id → test node id`) validated by the conformance checker against both the acceptance map and the collected test set (Recommended) | Explicit, diffable, fails closed on any unmapped required scenario or dangling test; aligns with `evidence_id_template`. |
| B | Naming/marker convention where each test embeds its `ARR-xxx-Sxx` / `ACR-*` id, scanned by the checker | Less bookkeeping and no separate file; relies on naming discipline and a reliable scanner. |
| C | Manual traceability table in a Markdown doc | Lowest tooling cost; not fail-closed and prone to drift from the actual tests. |
| Custom | Provide your own answer | Describe the mapping representation and the check that makes an omission fail. |

---

## Q7: Location of realization pin and conformance evidence

**Category**: Functional Scope / Boundary

**Context** — FR-005/SC-006: realization must record five coordinates (released tag, exact
commit, per-file digests, interface-lock digest, acceptance-map digest) plus conformance
evidence; SC-008/FR-036: the diff must modify **0** canonical-contract / F0 / UI /
DomainxFactory / deployment / release-metadata files.

**Question**: Where are the five release-pin coordinates and conformance evidence recorded
(without touching a sibling-owned path)?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | A runtime-owned evidence file under `tests/avatar_runtime/` (e.g. `conformance/realization-pin.yaml`) carrying `schema_version` + `kind` (Recommended) | Stays inside this feature's path ownership (satisfies SC-008/FR-036) and follows repo YAML discipline (Principle IV). |
| B | Under the feature spec dir `specs/003-avc-reference-runtime/` | Keeps evidence with the Speckit feature; separates the pin from the code and tests it governs. |
| C | A new top-level `conformance/` (or `evidence/`) directory | Neutral and visible; introduces a new tracked root path with its own README-index obligation. |
| Custom | Provide your own answer | Name the exact evidence path and format, confirming it is not sibling-owned. |

---

## Q8: Repo validation-gate integration and documentation index

**Category**: Completion Signals / Governance (sequencing)

**Context** — constitution Principle V requires repo-local validators pass before any push,
Principle IV requires new docs be linked in the README document index; SC-010 expects
boundary conformance confirmable "from automated boundary output alone." The feature runs on
a parallel branch before kernel realization.

**Question**: How does this feature's deterministic suite / boundary check join the shared
repo validation gate and documentation index during parallel work?

| Option | Answer | Implications |
|--------|--------|--------------|
| A | Add `scripts/validate-avatar-runtime.py` to the README validator index and run it plus the deterministic suite as the feature's Principle V gate (Recommended) | Matches the existing `validate-*.py` gate + README-index convention; gives reviewers/CI one command; guards every intermediate commit. |
| B | Run only the test suite (e.g. `pytest tests/avatar_runtime`) as the gate and document the command in the README, adding no new validate script | Lighter footprint; diverges from the repo's `validate-*.py` gate pattern and README validator index. |
| C | Keep the suite out of the shared gate during parallel work (feature-branch-only), integrate it at realization | Least disruption while the kernel is unreleased; risks unguarded intermediate commits until realization. |
| Custom | Provide your own answer | State how/when the suite and boundary check enter the shared gate and get indexed. |

---

_End of clarify block — 8 questions. Accepted answers are recorded above for the track agent to encode into `spec.md`._
