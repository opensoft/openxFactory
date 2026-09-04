# Data Model: register entry two, and the deliberation return

**Feature**: [spec.md](./spec.md) | **Date**: 2026-09-04

Two shapes move and one grows. Every value below is traced to the ratified text
or to codexFactory PR #165; the grounding table is [research.md](./research.md)
§ R2.

---

## 1. `permitted-operations.registry.yaml` — ENTRY NUMBER TWO

Shape unchanged: the entry conforms to the already-shipped
`permitted-operations.schema.yaml` `$defs/operation_entry`. `registry_version`
advances `1 → 2`.

| member | value | source |
|---|---|---|
| `operation_id` | `deliberation` | requirement, "Operation id" |
| `title` | prose naming it register entry number two | schema requires a title |
| `permitted_semantics.may` | read the RE-SEALED bundle served from the CLEARING run; run the seat deliberations; emit the per-seat outputs as a STRUCTURED RETURN bound to the three identifiers, sealed as an object of the clearing run | requirement, "What it MAY do" |
| `permitted_semantics.may_not` | check out any repository; write outside the runner's temporary plumbing (and prove the staging area is gone); reference a secret; HOLD ANY SEAT OR SIGNING KEY; carry a verdict/eligibility/decision/go-no-go/approval/recommendation field; report OBSERVED runner-group membership; affect any repository | requirement, "What it MAY NOT do" |
| `class_constraints.checks_out_code` | `false` | requirement, "Class constraints" |
| `class_constraints.writes` | `false` | idem |
| `class_constraints.may_reference_secrets` | `false` | idem |
| `class_constraints.token_scopes` | `[actions:read]` — EXACTLY one member | idem + design D6 |
| `class_constraints.timeout_minutes` | bounded (see below) | idem |
| `worker_profile` | `council-deliberation-worker` | requirement + design D5 |
| `lanes` | ONE: `artifact` / `xfactory-artifact-workers` / `host-rider-cpc-brett01` / `xfactory-artifact-cpc-brett01` | requirement, "Lanes" + design D3 |
| `output_schema_ref` | `contracts/clearing/deliberation-return.schema.yaml` | requirement + design D4 (OQ1 ruled) |
| `data_handling` | `internal-governance` | requirement + design D7 |
| `repository_affecting_output` | `false` | requirement |

**`timeout_minutes`.** The requirement says BOUNDED and fixes no number; the
schema admits `1 … 1440`. Entry one declares `5` for a probe. A seat deliberation
is a multi-turn model run, so `5` would make the entry describe an operation that
cannot complete. **`120` is declared**, as the smallest round number that leaves
the bound real rather than nominal, and the entry's `notes` say in as many words
that the number is a BOUND and not a budget. This is the only numeric value in the
entry the ratified text leaves to realization, and it is recorded here for that
reason.

---

## 2. `deliberation-return.schema.yaml` — THE NEW NEUTRAL SHAPE

`kind: xfactory_clearing_deliberation_return` (ratified text, not chosen here).
`additionalProperties: false` at the root and at every nested object.

### Root

| member | required | type | grounding |
|---|---|---|---|
| `schema_version` | yes | `const: 1` | family convention |
| `kind` | yes | `const: xfactory_clearing_deliberation_return` | ratified requirement |
| `operation` | yes | `const: deliberation` | the entry this return answers; the ONE fact the return may state about itself without consulting the register |
| `lane` | yes | `identifier` | requirement ("the lane"); NOT pinned to `artifact` — research O4 |
| `binding` | yes | object (3 required members) | requirement, "the run identifiers that bind the return" |
| `seats` | yes | keyed collection, `minProperties: 1` | requirement, "the per-seat outputs"; research O1 |

There is **no `signature` member, no `outcome` member, no `verdict`-shaped member
of any name, and no observed-membership member.** Each absence is a ratified
prohibition rather than an oversight, and the schema's description says so.

### `binding`

| member | required | type | grounding |
|---|---|---|---|
| `convening_job_id` | yes | `identifier` | #165 tasks 2.3 `convening_job_id` |
| `verified_subject_pin` | yes | `identifier` | requirement "the verified subject pin"; #165 `subject_pin` (research O3) |
| `inbound_bundle_digest` | yes | `^sha256:[0-9a-f]{64}$` | #165 `return-manifest.bundle_digest`; the VALUE of the inbound sealed-bundle manifest's `manifest_digest`. **No construction is declared here** — `xfc-jcs-sha256-1` over the `sealed_bundle_manifest` subject is `signed-execution-chain`'s, referenced and not restated (task 2.2) |

### `seats.<seat identity>` — one per seat

| member | required | type | grounding |
|---|---|---|---|
| `output` | yes | tagged union, `form: inline` or `form: reference` | requirement "that seat's output"; task 2.2 "(inline payload or reference)" |

`output.form: inline` carries `payload` — a STRING, deliberately, because the
seat's output is the producing estate's shape and a neutral contract that typed
it as an object would be authoring that shape (the error design D4 refuses from
the other side). An optional `content_hash` may accompany it.
`output.form: reference` carries `path` and a required `content_hash`, with an
optional `size_bytes`. The tagged-union form follows this family's own field-(10)
precedent (`attestation_type`), so no new discriminator convention is minted.

**The seat's own accounting members** (`num_turns`, `declared_turn_cap`,
`model_usage`, `declared_model`, …) live INSIDE the payload and are not neutral
members — research R2.

---

## 3. `dispatch-record.schema.yaml` — `$defs.refusal_ground.enum` 2 → 5

| member | status | admitted by |
|---|---|---|
| `unregistered_operation` | seeded | `add-clearing-dispatch-boundary` |
| `unknown_lane_selector` | seeded | `add-clearing-dispatch-boundary` |
| `lane_not_permitted` | **NEW** | `admit-deliberation-clearing-operation` |
| `output_schema_failure` | **NEW** | `admit-deliberation-clearing-operation` |
| `origin_scoped_credential` | **NEW** | `admit-deliberation-clearing-operation` |

Six of the record's nine awaited grounds stay absent — expiry, hash mismatch,
workflow-path contradiction, commit mismatch, unreadable API, committed-data
offer — until the operation that can emit them lands.

**THE RENDERING RULE, written into the `$defs` description** (ratified design
D13): an identifier is produced from one of the awaited PROSE names by
lower-casing it, joining its words with underscores, dropping any `clearing-`
prefix, and turning a compound's hyphen into an underscore. The two seeded
members already follow it (`unregistered_operation` ← "unregistered operation";
`unknown_lane_selector` ← "unknown lane selector"), and the three admitted here
are produced by it. Applying the rule to the six that remain is NOT authorization
to seed them.

## 4. What does NOT move

`REFUSAL_CODES` — the validator's hyphenated, `clearing-`-prefixed finding set —
is unchanged at 26 members. It is a DIFFERENT SET from the record's grounds, with
a different spelling and a different emitter (ratified design D13's table).
`schema` is not a member of it and stays not a member.
