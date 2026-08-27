# Phase 0 research — P2 carve and scaffold

**Feature**: `017-openxwallet-carve` · **Date**: 2026-08-26

Every "NEEDS CLARIFICATION" the plan template invites was already answered by the
ratified change. What follows is the FACT-FINDING that answering them against the
live tree required — measured, not assumed, because three of the ratified
shorthands turned out to lose something.

## R0. The carve commit

**Decision.** `CARVE_COMMIT = 30565e48ffe3d8a9773e10af33425701845e10f6`.

**Rationale.** `origin/main` of `opensoft/openxFactory` resolved from a FRESH
clone on 2026-08-26, then frozen as a literal 40-hex sha for the whole feature.
It is the merge of PR #396 (Amendment 2 — `openXwallet` takes the `openX<type>`
form), so the carve happens on a tree where the naming ruling has already landed.

**Alternatives rejected.** "HEAD" — no referent across a multi-PR wave, and
explicitly forbidden by task 3.3. The shared checkout's `main` — it is a shared
tree that other sessions move; a carve must read a tree nobody else is editing.

## R1. `git filter-repo` availability

**Decision.** Present on the host, version string `ed61b4050b71`. No install
needed; nothing was installed.

**Rationale.** Task 3.5 mandates `git filter-repo` specifically — not
`git subtree split`, which cannot take twelve disjoint path sets in one pass, and
not a fresh-history import, which would destroy the path history the openAvatar
precedent requires.

## R2. The carve surface, measured

**Decision.** 100 tracked files across the twelve sets at the carve commit.

| Path set | Files |
| --- | --- |
| `contracts/openxwallet/` | 55 |
| `contracts/openxwallet-agent-profile/` | 8 |
| `scripts/validate-openxwallet.py` | 1 |
| `scripts/wallet-yaml-syntax-gate.py` | 1 |
| `tests/wallet_yaml_syntax_gate/` | 1 |
| `.github/workflows/wallet-validation.yml` | 1 |
| `openspec/specs/openxwallet/` | 1 |
| `openspec/specs/openxwallet-agent-profile/` | 1 |
| `openspec/changes/archive/2026-08-08-add-openxwallet/` | 6 |
| `specs/006-openxwallet-contracts/` | **7** |
| `specs/010-wallet-validator-ci/` | 9 |
| `specs/012-wallet-issuer-anchor/` | 9 |
| **Total** | **100** |

**Rationale.** Task 3.6's completeness check needs a target number, and task 3.7
asserts two of these explicitly because a shorthand loses them. The `specs/006`
count of 7 is confirmed and includes its `evidence/` subtree.

## R3. The "36 negatives" count — the shorthand DID lose something

**Finding.** Task 3.7 asserts "**36** under
`contracts/openxwallet/examples/negative/`". Measured at the carve commit, that
directory holds **32** files. The missing 4 are in the SECOND family:
`contracts/openxwallet-agent-profile/examples/negative/` holds **4**.
**32 + 4 = 36.**

**Decision.** The ratified 36 is the cross-family total, and the assertion is
carried in the precise form the shorthand collapsed:

- `contracts/openxwallet/examples/negative/` → **32**
- `contracts/openxwallet-agent-profile/examples/negative/` → **4**
- both `contracts/openxwallet*/examples/negative/` → **36** (the ratified figure)

**Rationale.** This is the exact failure mode task 3.7 exists to prevent, applied
to task 3.7's own text. Asserting "36 in the core family" would FAIL against a
correct carve and would send an operator hunting for four files that were never
there. Asserting 32/4/36 proves the same property — no negative was lost — and is
true. Both `examples/` trees are also asserted to exist at identical relative
paths (task 3.8), which is the property the 36 was standing in for.

**Alternatives rejected.** Silently recording 32 and moving on (loses the
cross-check the ratified number provides); treating the mismatch as a carve
failure (the carve had not run yet when the count was taken).

## R4. The eight owned digests already agree at the carve commit

**Decision.** All 8 rows in `contracts/manifest.yaml` recompute to their recorded
`sha256` at the carve commit — verified BEFORE the carve.

| # | id | sha256 (first 16) |
| --- | --- | --- |
| 1 | `openxwallet-record` | `2012ef432616e73d` |
| 2 | `openxwallet-custody-registry-schema` | `df72638497a7f90c` |
| 3 | `openxwallet-custody-registry` | `94d631d6ee76dab0` |
| 4 | `openxwallet-grant` | `fde433c5821e2e6f` |
| 5 | `openxwallet-grant-exercise` | `f16ad31246186cec` |
| 6 | `openxwallet-distinct-holder-constraint` | `c2a6d2fd23fb3743` |
| 7 | `openxwallet-subject-attestation` | `d29eca519462aff7` |
| 8 | `openxwallet-agent-composition` | `aed3978e8ae952f3` |

**Rationale.** This is the CONTROL for the proof. If the recorded digests did not
already describe the carve commit's bytes, a post-carve match would prove nothing
about the carve — it would prove the manifest was stale. Establishing the control
first makes the post-carve comparison a statement about the carve alone.

**Rows carried verbatim.** Each row keeps the publisher's nine fields — `id`,
`path`, `source_path`, `type`, `schema_version`, `sha256`, `compatibility`,
`adapter_owner`, `consumption_rule`. Only `source_path` is rewritten
(`openxFactory/...` → `openXwallet/...`), because it names the repository a
consumer vendors FROM and that repository changes. `adapter_owner` stays the
publisher of the contract — see R6.

## R5. The vendored envelope schema

**Decision.** `contracts/schemas/hermes-job-envelope.schema.yaml`, byte-copied
from openxFactory at the carve commit, `sha256 =
8ce2c89903a2f5a68ce3d73a7b8eb4f47cdef913da038b9a68e22735ee96cb7c`. Pinned
openxFactory bundle: `contract-v1.44`.

**Rationale.** Identical repository-relative path, so `ENVELOPE_SCHEMA_PATH`
(`ROOT / "contracts" / "schemas" / "hermes-job-envelope.schema.yaml"`) and the
`.relative_to(ROOT)` print in the validator's note need NO edit — which is why
the validator's diff is empty rather than "empty except one line". Added by the
SCAFFOLD commit, not the carve: it is not one of the twelve path sets, and a
carved copy would make the empty-diff claim about a file whose role changed.

**The upstream row records no digest.** openxFactory's own manifest row for this
artifact carries `id`, `path`, `source_path`, `type`, `schema_version`,
`intended_consumers`, `compatibility: copied_from_source_commit` and
`adapter_owner: Omnigent-Install` — and **no `sha256`**; it is content-addressed
by commit from `opensoft/Omnigent-Install`. So the ratified "digest equal to the
pinned openxFactory row's" is satisfied by COMPUTING the digest over the pinned
bytes, which is the value the ratified text means. Recorded on the row and in
`clarify-questions.md` Q1.

## R6. `adapter_owner` on the consumed row

**Decision.** `adapter_owner: openxFactory`, as ratified — not
`Omnigent-Install`, which is what openxFactory's own row says.

**Rationale.** From openXwallet's position, openxFactory is who it pins and whose
copy it consumes; the pin file names openxFactory and the resync runbook resyncs
against openxFactory. The two-hop chain (Omnigent-Install → openxFactory →
openXwallet) is carried in a comment and in `source_path`, so nothing is hidden.

**Alternatives rejected.** Naming `Omnigent-Install` — it would make the row
describe a repository openXwallet has no pin to, no runbook for, and no way to
resync against.

## R7. Where the verify step goes — the one real design tension

**Decision.** The verify step is the FIRST step inside
`.github/workflows/wallet-validation.yml`'s `wallet-validation` job. No separate
`verify-contract-pin.yml` workflow is created.

**Rationale.** Task 3.19 and design D8 require the verify to run "BEFORE the
validator". Ordering across two workflows is not expressible in GitHub Actions —
independent workflows race. And task 3.24 enumerates the byte-identity floor
without the workflow file in it, so editing that file breaks nothing ratified.
The edit is declared: it is the ONLY post-carve edit to a carved file, and it is
recorded as such in the proof.

**Alternatives rejected.** A second workflow (cannot order before another
workflow's step; the launching brief proposed it, the ratified tasks make it
unnecessary). A second job in the same file (also unordered, and it would still
edit the file). Leaving the validator to check identity itself (it checks
`.is_file()` — presence, not identity — and rule (g) reads the approval-scope
vocabulary out of that very file, so an unverified swap silently redefines the
vocabulary the gate enforces).

## R8. The ruleset shape

**Decision.** Mirror ruleset **21538893**: `target: branch`,
`conditions.ref_name.include: ["~DEFAULT_BRANCH"]`, one
`required_status_checks` rule with
`strict_required_status_checks_policy: false`, `do_not_enforce_on_create: false`,
and contexts `wallet-validation` + `pytest-suite`. Created at `enforcement:
evaluate`, PATCHed to `active`.

**Rationale.** D8 says mirror openxFactory's shape, and read at the carve commit
that shape requires BOTH tokens (updated 2026-08-26 17:39). Task 3.27's evidence
names `wallet-validation`; requiring both satisfies it and matches the precedent.
21538893 is an ORGANIZATION-source ruleset; openXwallet's is created at the
REPOSITORY level (`POST repos/opensoft/openXwallet/rulesets`), which is the
surface task 3.27's evidence call reads back.

**Why EVALUATE first, and why it is not a shortcut.** GitHub cannot require a
status check that has never reported in the repository — the context is not
selectable. So day-one REQUIRED is *impossible*, not merely inconvenient, and the
ratified sequence (EVALUATE → one trivial PR → ACTIVE) is the only path. Recorded
in the runbook as unachievable rather than promised.

## R9. Reference shapes read, so the scaffold is house-style

| Artifact | Read from | What was taken |
| --- | --- | --- |
| `contract_pin.yaml` | `openAvatar/contract_pin.yaml` | `kind`, source repo + exact 40-hex commit, per-file `sha256`, and the FAIL-CLOSED pre-sync doctrine ("a recomputed digest can never equal an empty recorded digest → drift → fail before any test") |
| `docs/pin-resync-runbook.md` | `openAvatar/docs/pin-resync-runbook.md` | Preconditions → Checklist → re-verify the pin offline → re-run the offline gate suite; the offline law (no gate reads an upstream tree or the network) |
| "Domain descendants" README section | `openAvatar/README.md:30-45` | "pin and profile, never fork"; descendants are DISTRIBUTIONS; a need a profile cannot express is an upstream change, not a fork; upgrades are a pin bump |
| `AGENTS.md` / `CLAUDE.md` | `openxFactory/AGENTS.md` | Point at `$HOME/.agents/AGENTS.md` and the two protocol files; repo docs stay authoritative for product facts |
| `openspec/config.yaml` | `openxFactory/openspec/config.yaml` | `schema: spec-driven` |
| `wallet-validation.yml` | the carved file | job id `wallet-validation`, no display name (a display name silently de-advises the gate), `pull_request` on `main`, `permissions: contents: read`, 10-minute timeout, Python 3.12, `pip install pyyaml jsonschema rfc3339-validator` |

## R10. What the promoted specs actually say at `:4` and `:8`

**Measured.** Both files carry, verbatim:

- line 4: `TBD - created by archiving change add-openxwallet. Update Purpose after archive.`
- line 8: begins `openxFactory SHALL …`

**Decision.** Line 4 is replaced with a real Purpose for each family; every
`openxFactory SHALL` in the requirement bodies becomes `openXwallet SHALL`. The
part-two diff is then asserted line by line rather than described.

**Rationale.** D12 names both edits and calls them the ONLY prose the floor
permits. A moved requirement naming the wrong repository is not a pure move; a
moved spec whose Purpose names another repository's archiving change is not
either.

## Open risks carried into implementation

1. **A `--path` typo carves silently less.** Mitigated by the completeness check
   being a diff of two sorted listings against the measured total of 100, not a
   spot check.
2. **The trivial PR's checks could fail for an environment reason** (a missing
   pip dependency on the runner). Then the ruleset stays in EVALUATE and the tag
   is not cut — the ratified order makes this a stop, not a workaround.
3. **`pytest-suite` collects one test file.** `tests/wallet_yaml_syntax_gate/`
   holds exactly `test_gate.py` and no `__init__.py`. Collection is asserted
   non-zero so a silently-empty suite is distinguishable from a passing one.
