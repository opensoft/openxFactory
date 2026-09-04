# Data Model: contracts/clearing

**Feature**: 028-clearing-contracts | **Date**: 2026-09-03

Every shape below is derived from the ratified text of
`add-clearing-dispatch-boundary` as MODIFIED by `add-cpc-clearing-boundary`.
Where the live realization (`opensoft/xFactory` `.github/workflows/clearing-dispatch.yml`,
PR #191, squash `95f1a9c6`) already emits a name, THAT NAME IS ADOPTED VERBATIM —
`tasks.md` §3.5 makes the emitted names the interface the neutral schema is
authored against, not the other way round.

## Family conventions

- Directory: `contracts/clearing/`.
- Every file carries `schema_version: 1` and (schemas) `kind: openxfactory-clearing-contract-schema`,
  `name:`, `$schema:`, `$id: https://xforge.us/schemas/openxfactory/clearing/v1/<file>`,
  `contract_id:`, `contract_schema_version: 1`, `title:`, `description:` —
  the `signed-execution-chain` / `trust-anchor` family header shape.
- Every record schema is `type: object`, `additionalProperties: false`, with an
  explicit `required` list. A shape that permits unknown members cannot refuse a
  smuggled field.
- Digest values are NEVER redefined: a digest is
  `{construction, subject, value}` matching the shipped
  `signed-execution-chain/digest-construction.schema.yaml` `$defs/digest`, cited
  by prose reference (the two families are separately registered contract files;
  a cross-file `$ref` by relative path is not how this repository's schemas
  compose, so the constraint is restated STRUCTURALLY — same three members, same
  patterns — and the validator asserts the values agree with the chain's own
  `$defs`).

## 1. Sealed bundle manifest — `sealed-bundle-manifest.schema.yaml`

`kind: xfactory_sealed_bundle_manifest`. The TEN ratified fields, numbered in
the schema description so a reviewer can count them:

| # | member | shape | notes |
|---|---|---|---|
| 1 | `origin` | `{repository, workflow_path}` | field (1), both required |
| 2 | `source_commit` | 40-hex | field (2) |
| 3 | `job` | `{job_id, expires_at}` | field (3); `expires_at` RFC 3339 UTC, REQUIRED |
| 4 | `selected_files` | array, minItems 1, each `{path, content_hash}` | field (4); `content_hash` is `^sha256:[0-9a-f]{64}$` over the file BYTES — NOT a canonical-JSON digest |
| 5 | `operation` | operation id | field (5); resolved against the register |
| 6 | `worker_profile` | string | field (6); a CLAIM compared to the register entry |
| 7 | `lane` | `{runner_group, dispatch_label}` | field (7); both literal |
| 8 | `output_schema_ref` | string | field (8); a CLAIM compared to the register entry |
| 9 | `data_handling` | string | field (9); a CLAIM compared to the register entry |
| 10 | `origin_attestation` | one of two variants | field (10), below |

**Field 10** is a tagged union with `attestation_type`:

- `origin_signature` — `{attestation_type: origin_signature, register_row_id,
  key_id, manifest_digest: <digest>, signature, covered_fields}`.
  `manifest_digest.construction` is `xfc-jcs-sha256-1` and
  `manifest_digest.subject` is `sealed_bundle_manifest` (the tranche-3 subject
  this realization adds). `covered_fields` is a CLOSED enum-valued array whose
  member set must be ALL TEN field tokens — a partial signature is refused, per
  the ratified scenario *"A signature covers less than the declared fields"*.
- `hosted_workflow_provenance` — `{attestation_type: hosted_workflow_provenance,
  provider, run_id, run_url}`. Legal ONLY when the originating repository holds
  no active origin row; the CROSS-SHAPE rule is the validator's, because a
  schema cannot read the register.

`policy_claims_are_claims`: the schema's description states, and the validator
enforces, that members 6, 8 and 9 (and 7) are CLAIMS. The register governs.

## 2. Permitted-operations register — schema + instance

Two files, on the `openxwallet-custody` / `trust-anchor-chain-custody`
schema-plus-instance convention:

- `permitted-operations.schema.yaml` — `kind: xfactory_clearing_permitted_operations_registry`,
  carrying `registry_id` (const `clearing-permitted-operations`),
  `registry_version`, and `operations: [...]`.
- `permitted-operations.registry.yaml` — the CLOSED INSTANCE.

Each operation entry:

| member | shape | ratified source |
|---|---|---|
| `operation_id` | identifier | "Each entry SHALL declare its operation id" |
| `title` | string | readability |
| `permitted_semantics.may` | array of strings, minItems 1 | "what the operation may do" |
| `permitted_semantics.may_not` | array of strings, minItems 1 | "and what it may not" |
| `class_constraints.checks_out_code` | boolean | "at minimum: whether it checks out code" |
| `class_constraints.writes` | boolean | "whether it writes" |
| `class_constraints.may_reference_secrets` | boolean | "whether it may reference secrets" |
| `class_constraints.token_scopes` | array (may be empty) | "the token scopes its job carries" |
| `class_constraints.timeout_minutes` | integer ≥ 1 | `readiness-diagnostic`'s "bounded timeout" |
| `worker_profile` | string | "its required worker profile" |
| `lanes` | array, minItems 1, of `{runner_group, dispatch_label, expected_runner}` | "the lanes — runner group and dispatch label — it may be dispatched to" |
| `output_schema_ref` | string | "its declared output schema" |
| `data_handling` | string | field (9)'s register-side authority |
| `repository_affecting_output` | boolean | "whether it returns repository-affecting output" |

**The instance holds EXACTLY ONE member**, `readiness-diagnostic`, populated
from the ratified text and the live realization:

- `permitted_semantics.may`: runner identity vs expected identity, declared
  group, declared dispatch label, service account, host identity, heartbeat and
  clock, name-allowlisted environment echo, fixed-digest compute round trip,
  read-only tool print-back.
- `permitted_semantics.may_not`: check out, write outside the runner's own temp
  plumbing, reference a secret, carry a token scope, dump the environment
  wholesale, report OBSERVED group membership, carry an eligibility verdict.
- `class_constraints`: `checks_out_code: false`, `writes: false`,
  `may_reference_secrets: false`, `token_scopes: []`, `timeout_minutes: 5`.
- `worker_profile`: `cpc-readonly-probe`.
- `lanes`: coding — group `xfactory-execution-lane-workers`, label
  `host-coding-cpc-brett01`, runner `xfactory-coding-cpc-brett01`; artifact —
  group `xfactory-artifact-workers`, label `host-rider-cpc-brett01`, runner
  `xfactory-artifact-cpc-brett01` (`tasks.md` §3 constants table).
- `output_schema_ref`: `contracts/clearing/operation-report.schema.yaml`.
- `data_handling`: `public_log_only` (the value the live gate emits as
  `clearing.dispatch.handling=`).
- `repository_affecting_output`: `false`.

**Closure** is not expressible in JSON Schema against a future instance, so it
is a VALIDATOR rule: the validator carries the ratified member set as a frozen
constant and refuses any instance member outside it. This mirrors the L4 guard's
frozen-origin-set mechanism, and it is a TRIPWIRE backed by review, not an
unforgeable refusal — the same honesty the ratified text demands of the guard.

## 3. Operation report — `operation-report.schema.yaml`

`kind: xfactory_clearing_operation_report`. THE COMPOSED report of record: ONE
per dispatch, however many lanes were probed. Per-lane facts are a KEYED
COLLECTION (`lanes: {<lane_key>: {...}}`), never a top-level array of fragments.

Top level: `dispatch_id`, `operation` (the CLEARED operation; nullable),
`operation_claimed`, `lane_selector`, `cleared_at`, `clearing_result`,
`outcome` (`success|failure` — the `clearing.dispatch.outcome=` the report
appends), `run_url`, `lanes`.

Each lane value:

- `declared: {runner_group, dispatch_label, expected_runner}` — typed as
  DECLARED. The member names carry the word, and the schema description states
  that OBSERVED group membership is established only by the single-door
  attestation. There is deliberately NO `observed_runner_group` member: a shape
  that cannot express the claim cannot make it.
- `runner: {name, os, arch, environment, identity}` where `identity` is
  `CONFIRMED|MISMATCH` (the live `clearing.report.<lane>.runner.identity=`).
- `host: {hostname, computername, whoami, username, userprofile, workspace}`.
- `heartbeat: {job_executing, utc, epoch}`.
- `environment: {<ALLOWLISTED_NAME>: <value>}` with `propertyNames` restricted
  to the NAME ALLOWLIST the ratified entry requires (`RUNNER_NAME`, `RUNNER_OS`,
  `RUNNER_ARCH`, `RUNNER_TEMP`, `COMPUTERNAME`, `USERNAME`,
  `PROCESSOR_ARCHITECTURE`, `NUMBER_OF_PROCESSORS`, `GITHUB_WORKSPACE`) — a
  wholesale dump cannot validate.
- `tools: {<tool>: {path, version}}`.
- `compute: {python, platform, node, sha256, expected_sha256,
  sha256_check, arithmetic_check, round_trip}` — the fixed-input,
  fixed-expected-digest round trip, with BOTH values recorded so the ratified
  disagreement scenario is expressible.
- `result` — the lane job's result.

**No verdict.** The schema is `additionalProperties: false` and its description
names the refusal: a member expressing eligibility, readiness, or a go/no-go
decision turns the report into the awaited infrastructure-readiness result
(design D9) and MUST be refused at review. The validator additionally refuses a
report carrying any member whose name matches the verdict wordlist.

## 4. Dispatch record — `dispatch-record.schema.yaml`

`kind: xfactory_clearing_dispatch_record`.

**Why a new file and not the existing `contracts/schemas/dispatch-record.schema.yaml`.**
That file is `kind: dispatch_record` for `add-capability-steward`'s
DISPATCH-JUNCTION decision: which of the crystallized or AI path served a
capability request. It shares an English word and nothing else — different
subject, different owning capability, different required members, different
`$id`. Merging them would put two capabilities' vocabularies in one shape, which
is the exact defect `add-clearing-dispatch-boundary`'s "NO SECOND VOCABULARY"
section exists to prevent, in reverse. Neither file is moved or renamed; the new
one's description names the other so a reader who greps the filename lands on the
distinction.

Members:

- `dispatch_id` (the live `cd-<run_id>-<attempt>` form is permitted, not
  mandated), `dispatched_at`, `actor`, `clearing_repository`,
  `clearing_workflow_ref`, `run_id`, `run_attempt`, `run_url`.
- `cleared` — boolean. ONE shape for admissions and refusals, per the ratified
  requirement that a refusal is a ledger entry too.
- `operation` — object with `claimed` REQUIRED and `resolved` nullable. On a
  refusal `resolved` is null and `claimed` is what was asked for.
- `verification` — three DISJOINT groups, because the ratified text refuses to
  fold them together:
  - `provider_verified: [{field, claimed, resolved, agrees}]` — the five fields
    with an authoritative provider answer.
  - `policy_checked: [{field, claimed, resolved_from_register, agrees}]` — the
    fields the register governs. `resolved_from_register` is the value the
    dispatch RUNS ON (`add-cpc-clearing-boundary`'s second addition).
  - `origin_signature: {performed, outcome, register_row_id, key_id}` — its own
    outcome, never inside `provider_verified`
    (`add-cpc-clearing-boundary`'s first addition).
- `lane_declarations` — array of `{lane, declared_runner_group,
  declared_dispatch_label}`. The member names carry DECLARED; there is no
  observed counterpart in this shape.
- `declared_data_handling` — the REGISTER ENTRY's class for a bundle-less
  dispatch.
- `refusal` — `null` when `cleared: true`; otherwise `{ground, detail}` where
  `ground` is an ENUM. **Seeded with exactly the two grounds the realization
  emits**: `unregistered_operation`, `unknown_lane_selector`. The description
  lists the nine further grounds the requirement text names and states that each
  becomes a member by governed change as the operation that can produce it lands.
- `workspace_disposal` — `{disposed, disposed_at, method, evidence_ref}`,
  REQUIRED and non-empty (`add-cpc-clearing-boundary`'s ADDED requirement, which
  makes disposal a field of THIS record).
- `chain_ref` — nullable `sha256:`-tagged reference to a signed execution chain
  where one governs the work (OQ2's recommendation: a REFERENCE, not a second
  log format and not a chain link).
- `outcome` — `success|failure|refused`.

Cross-shape rules the schema cannot state, left to the validator: `cleared:
true` requires `refusal: null` and a non-null `operation.resolved`; `cleared:
false` requires a `refusal.ground`; a `policy_checked` row with `agrees: false`
requires `cleared: false`.

## 5. Single-door attestation — `single-door-attestation.schema.yaml`

`kind: xfactory_clearing_single_door_attestation`.

- `attested_at`, `provider`, `clearing_repository`, `clearing_workflow_path`.
- `groups` — array, minItems 1, each:
  `{runner_group, expected_allowlist: [...], observed_allowlist: [...],
  expected_repositories: [...], observed_repositories: [...],
  clearing_path_admitted: boolean, findings: [...]}`.
  The EXPECTED SET IS A PER-GROUP MEMBER. There is no top-level
  `expected_allowlist`: a shape with one estate-wide expected set cannot express
  the per-group computation the ratified text requires, and the validator
  additionally refuses a record whose group expected sets are all identical to
  a single declared estate set.
- Each finding: `{finding_class, group, subject, expected_set, detail}` with
  `finding_class` a CLOSED enum of exactly three:
  - `widening` — an observed entry the group's expected set does not derive, or
    an admitted repository other than the clearing repository. A BREACH.
  - `dark_lane` — an enumerated member with no observed allowlist entry. NOT a
    breach; a disposition item.
  - `convergence_not_yet_reached` — the clearing path absent before the operator
    act. NOT a widening.
- `completeness_claim` — `{strength, cites_green_attestation}` where `strength`
  is `narrower_pre_admission` or `full_post_admission`. The validator refuses
  `full_post_admission` on a record carrying any `convergence_not_yet_reached`
  finding, which is the ratified conditioning made mechanical.

## Cross-family change

`contracts/signed-execution-chain/digest-construction.schema.yaml` gains ONE
member in `$defs/digest_subject`: `sealed_bundle_manifest`. That file's own
header declares this the one way it is meant to move (*"A later tranche adds
SUBJECTS to this enumeration and never a second CONSTRUCTION"*), and
`add-cpc-clearing-boundary` `tasks.md` §2.9 names the widening as the
precondition for the origin signature. `construction_name` is untouched.

The `sealed_return` subject that §2.9 also names is NOT added: nothing in this
realization computes a digest over a sealed return, and an enum member with no
shipped consumer is a widening no shape exercises. It belongs to the finalizer
successor that first produces one.
