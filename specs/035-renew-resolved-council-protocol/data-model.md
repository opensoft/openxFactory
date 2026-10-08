# Data Model: Neutral resolved council protocol

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) · **Research**: [research.md](research.md)

These are the shapes of the planned `contracts/council-convening/` family. A shape becomes normative only when two things happen:

1. its schema lands in the phase named for it;
2. a release publishes it (Phase 7 for the replacement, Phase 8 for the removal of legacy acceptance).

Until both happen, the shapes here are the plan, not a contract. Consumers must read the landed schema, never this file ([contracts/provider-interface.md](contracts/provider-interface.md)).

The common conventions:

- Every record is a closed object, with `additionalProperties: false` at every depth.
- Every record carries `schema_version: 1` and a `kind`.
- Members are listed in the order a reader meets them.
- **R** means required, **O** optional.

## Shared definitions (`shared-definitions.schema.yaml`, Phase 1)

| Definition | Grammar | Notes |
|---|---|---|
| `opaque_id` | `^[A-Za-z0-9][A-Za-z0-9._:/@+=-]{0,255}$`, matched **whole** | Equals 049's `_OPAQUE_ID_RE` / `_ASSIGNMENT_ID_RE` bound. The validator enforces whole-string matching (`\Z`), so a trailing newline is refused. Python's `re.search` with `$` would accept one, and a corpus vector probes it. |
| `council_id`, `seat_id`, `matched_class` | `opaque_id` | No domain value appears in the schema. |
| `repository` | `^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`, whole | Spelling is checked against `repository-identity.yaml` only where an entity says so. |
| `full_sha` | `^[0-9a-f]{40}$`, whole | A branch, a tag, an abbreviated id and uppercase are all refused (`mutable_rule_reference` where a rule is cited). |
| `pull_number` | integer 1 to 2147483647, never boolean | Equals 049's `MAX_PULL_NUMBER`. |
| `relative_path` | UTF-8, 1 to 4096 bytes. No leading `/`, no `./`, no `..` segment, no `\`, no empty segment, no trailing `/`, no C0 or C1 control character, no NUL | `rule_path_malformed` for a cited rule; otherwise the record's malformed code. |
| `utc_instant` | `YYYY-MM-DDTHH:MM:SSZ`, calendar-valid | Seconds precision. Expiry is refused at and after the instant. |
| `raw_sha256` | `^sha256:[0-9a-f]{64}$` | SHA-256 over a file's raw bytes. |
| `digest` | `$ref` to `signed-execution-chain/digest-construction.schema.yaml#/$defs/digest` | `{construction: xfc-jcs-sha256-1, subject, value}`. Each use fixes its `subject` by `const`. |
| `key_fingerprint` | `^sha256:[0-9a-f]{64}$` | `sha256:` + hex of the raw 32-byte public key: the estate's one spelling. |
| `public_key` | unpadded base64url of exactly 32 bytes | |
| `signature` | unpadded base64url of exactly 64 bytes | |
| `nonce` | unpadded base64url of exactly 32 bytes | |
| `candidate` | `{repository R, pull_number R, head_sha R(full_sha)}` | D1: "candidate repository, positive pull number and lowercase full head". |
| `refusal_code` | closed enumeration, see [Refusal vocabulary](#refusal-vocabulary) | snake_case, because these are contract values. Validator findings are kebab-case. |

A value admitted by a schema must also be admissible under `xfc-jcs-sha256-1`:

- no non-integer number;
- no integer outside ±(2^53 − 1);
- no unpaired surrogate.

A value that is not admissible is refused as `value_not_canonicalizable` before any digest is taken.

## E1. Protocol registry (`protocol-registry.schema.yaml` + `protocol.registry.yaml`, Phase 1)

Kind: `xfactory_council_protocol_registry`. A closed instance with exactly two entries. Adding an entry is a governed contract change.

| Member | Replacement entry | Legacy entry |
|---|---|---|
| `protocol_id` | `xfc-resolved-council-1` | `xfactory-council-seat-return/v1` |
| `role` | `replacement` | `legacy` |
| `status` | `available` (at Phases 1–7); `admission_eligible` (from Phase 8) | `in_use` (Phases 1–6); `deprecated` (Phase 7); `historical_only` (Phase 8) |
| `signing_contexts` | `xfc-resolved-council-1/seat-key-registration`, `xfc-resolved-council-1/seat-return` | `xfactory-council-seat-return/v1`, `xfactory-council-seat-key-authorization/v1` |
| `recognition` | — | Any one of: (a) a convening block with no `protocol` and no `required_seats`; (b) a context naming a legacy signing context; (c) a registration carrying `root_key_fingerprint`, `root_signature` or `authorization` |
| `introduced_in` / `deprecated_in` / `removed_in` | `null` until a cut writes the allocated tag | `null` until a cut writes the allocated tag |

`status` is what the validator acts on. Its effect on a record classified as legacy and presented to active validation:

| `status` | Effect |
|---|---|
| `in_use` | Accepted as legacy, with no finding. |
| `deprecated` | Accepted, with WARN `legacy_protocol_deprecated` (an error under `--strict`). |
| `historical_only` | Refused as `legacy_protocol_refused`. |

Historical mode always classifies and never reinterprets.

## E2. Commission record (`council-convening.schema.yaml`, Phase 2)

Kind: `xfactory_council_convening`. The producer submits it and the consumer verifies it before any write (D1, D2).

| Member | R/O | Shape and rule |
|---|---|---|
| `protocol` | R | `const: xfc-resolved-council-1`. Any other protocol identifier is `protocol_unknown`. A legacy-shaped block goes through E1 recognition. |
| `council_id` | R | `council_id`. It must be a council the rule projection declares; otherwise `council_unknown`. |
| `subject_pin` | R | `full_sha`, equal to `required_seats_provenance.candidate.head_sha` (`candidate_mismatch`). |
| `packet_refs` | R | 1 to 64 strings, each 1 to 2048 characters with no control character. Reader material, as today. Secret-scanned. |
| `mix_id` | O | `opaque_id`. Existing optional deliberation-mix selector, carried for the consumer's existing mix check. |
| `required_seats` | R | 1 to 64 `seat_id`, unique, ordered. |
| `required_seats_provenance` | R | Object, below. |

`required_seats_provenance`:

| Member | R/O | Shape and rule |
|---|---|---|
| `candidate` | R | `candidate`. Must equal the consumer's independently resolved candidate and the trusted trigger's expected candidate (`candidate_mismatch`), and the live head (`candidate_head_moved`, or `candidate_head_unavailable`). |
| `governed_rule` | R | `{repository, path(relative_path), revision(full_sha), blob_sha256(raw_sha256)}`. The authority and currency rules are in [research R7](research.md#r7--rule-authority-and-revision-currency-open-3). |
| `matched_class` | R | `matched_class`. It must be a class the projection declares (`class_unresolved`). |
| `standing_seats` | R | 1 to 64 `seat_id`, unique, ordered. It must equal the projection's standing seats exactly (`rule_projection_mismatch`). |
| `conditions` | R | 0 to 64 entries: `{seat R(seat_id), predicate R, input_contract R, parameters R, held R(boolean)}`. They must equal the projection's conditions in order, apart from `held`. `held` must equal the reference evaluation (`condition_result_mismatch`). An unknown predicate is `predicate_unknown`. Bad parameters are `predicate_parameters_malformed`. An unevaluable condition is `condition_unevaluable`. A predicate run against the wrong input contract is `predicate_parameters_malformed`. |
| `fact_sources` | R | One per input contract the conditions use, unique by `input_contract`: `{input_contract: pr_facts, repository, pull_number, head_sha}` equal to the candidate, or `{input_contract: rule_facts, repository, path, revision}` at an immutable revision. Otherwise `fact_source_mismatch`. |
| `consumed_facts` | R | `{<input_contract>: {<fact>: value}}`. The keys are exactly the input contracts in use, and the facts are exactly those the conditions read. An unread fact is `facts_unused`. A missing fact is `condition_unevaluable`. A fact differing from the authoritative facts is `consumed_facts_mismatch`. A secret is `secret_bearing_fact`. |

The derived values and their rules:

- **Roster rule** ([R6](research.md#r6--roster-composition-and-the-neutral-rule-projection)). `required_seats` = `standing_seats`, then each `held: true` condition's `seat` in order, each appended if absent.
  - An empty roster is `roster_empty`.
  - A repeated seat is `roster_duplicate_seat`.
  - Any other difference, including order and same-count substitution, is `roster_mismatch`.
  - A held condition whose seat is unbound is `condition_seat_unbound`.
- **Opaque conclusions.** Provenance that carries a result without the inputs that reproduce it is `opaque_conclusion`. Examples are a digest-only rule, no `consumed_facts`, or `held` with no `parameters`.
- **`convening_digest`.** `xfc-jcs-sha256-1`, subject `council_convening`, over the whole record.

**Lifecycle.** The producer resolves, re-gathers and rechecks the head, then submits. The consumer verifies all the above before any write. Then the snapshot (E4) is frozen. A record is never mutated; a later head or rule needs a new convening (D2).

## E3. Predicate registry (`predicate-registry.schema.yaml` + `predicate.registry.yaml`, Phase 2)

Kind: `xfactory_council_predicate_registry`. A closed instance.

| Member | Content |
|---|---|
| `input_contracts.pr_facts` | `changed_paths`: list of `relative_path`. `changed_files_total`: integer ≥ 0. `changed_paths_entry_count`: integer ≥ 0. Facts are read from the candidate at `head_sha`. Both rename paths are included, and a rename is one entry contributing two paths. |
| `input_contracts.rule_facts` | `rule_touched_paths`: list of `relative_path`. Facts are read from a governed path at an immutable revision. |
| `predicates[0]` | `changed_paths_intersect`, over `pr_facts`. Parameters: `protected_paths`, a non-empty list of patterns. |
| `predicates[1]` | `rule_touches_security_posture`, over `rule_facts`. Parameters: `security_surfaces`, a non-empty list of patterns. |
| `pattern_grammar` | An exact `relative_path`, or `<relative_path>/**`. The refusals and the bare-directory evidence rule are in [R5](research.md#r5--the-closed-predicate-registry-and-input-contracts). |

The decision semantics:

- A predicate holds when any read path matches any pattern.
- It is unevaluable when a read fact is absent, or, for `pr_facts`, when `changed_paths_entry_count ≠ changed_files_total`.
- "Unevaluable" is never "false".

## E4. Convening snapshot (`convening-snapshot.schema.yaml`, Phase 3)

Kind: `xfactory_council_convening_snapshot`. The consumer issues it atomically at admission. The consumer's own response envelope, status codes and error body wrap it; those are 025's.

| Member | R/O | Rule |
|---|---|---|
| `protocol` | R | Equal to `convening.protocol`. |
| `convening_id` | R | `opaque_id`, issued by the consumer. |
| `convening_digest` | R | `digest`, subject `council_convening`. It must recompute over `convening` (`digest_construction_mismatch`). |
| `convening` | R | The admitted E2 record, verbatim. |
| `assignments` | R | Exactly one E5 per `required_seats` entry, in roster order. A missing, extra or reordered assignment is `assignment_set_mismatch`. A repeated `assignment_id` is `assignment_duplicate`. One holder on two seats is `assignment_shared_holder`. |
| `admitted_at` | R | `utc_instant`. |

**Retry identity.** The convening key is `(protocol, council_id, candidate, convening_digest)`.

- An incoming record identical to a live snapshot's `convening` returns that snapshot unchanged: the same `convening_id`, the same assignments.
- A different record for the same `(protocol, council_id, candidate)` while a non-failed snapshot exists is `convening_conflict`, and nothing is replaced.

The consumer enforces both transactionally (025 FR-005, FR-006). The corpus states the expected outcome for each pair.

## E5. Seat assignment (`seat-assignment.schema.yaml`, Phase 3)

Kind: `xfactory_council_seat_assignment`. This is the public assignment a seat job receives. It carries no other seat's identifiers and no secret.

| Member | R/O | Rule |
|---|---|---|
| `protocol`, `convening_id`, `convening_digest`, `council_id`, `candidate` | R | Equal to the snapshot's. Otherwise `cross_convening_context`. |
| `assignment_id` | R | `opaque_id`. |
| `seat_id` | R | `seat_id`, a member of the frozen roster. |
| `holder` | R | `{principal_kind R: github_oidc_job \| governed_broker_job, principal_ref R(opaque_id), binding_ref R(opaque_id)}`, bound by the trusted dispatcher or broker from verified execution evidence (D3). |
| `permitted_operations` | R | Exactly `[seat_key_registration, seat_return]`. Any other operation is `operation_not_permitted`. |
| `not_before`, `expires_at` | R | `utc_instant`. The lifetime must be greater than 0 and no more than the ceiling ([OPEN-1](research.md#r12--lifetime-ceilings-open-1)); otherwise `assignment_malformed`. Use before `not_before` is `assignment_not_yet_valid`. Use at or after `expires_at` is `assignment_expired`. |

## E6. Registration challenge (`registration-challenge.schema.yaml`, Phase 4)

Kind: `xfactory_council_registration_challenge`. The consumer issues it, for one assignment, to be used once.

| Member | R/O | Rule |
|---|---|---|
| `protocol` | R | The replacement. |
| `challenge_id` | R | `opaque_id`. |
| `assignment_id` | R | The assignment it was issued for. |
| `nonce` | R | `nonce`, 32 random bytes. |
| `issued_at`, `expires_at` | R | `utc_instant`. The lifetime must be greater than 0 and no more than the ceiling (OPEN-1); otherwise `challenge_malformed`. |

The refusals are:

| Condition | Refusal |
|---|---|
| Not issued | `challenge_unknown` |
| Issued for another assignment | `challenge_wrong_assignment` |
| Already consumed | `challenge_consumed` |
| Used at or after expiry | `challenge_expired` |

## E7. Seat key registration (`seat-key-registration.schema.yaml`, Phase 4)

Kind: `xfactory_council_seat_key_registration`. The body carries **no seat label and no principal**. The seat comes from the frozen assignment, and the principal from verified identity evidence (D3, H3).

| Member | R/O | Rule |
|---|---|---|
| `protocol` | R | The replacement. |
| `assignment_id`, `challenge_id` | R | |
| `public_key` | R | `public_key`. |
| `key_fingerprint` | R | It must recompute from `public_key` (`fingerprint_mismatch`). |
| `proof` | R | `signature` over the registration context (E9). An invalid proof is `proof_invalid`. A context bound to another seat is `cross_seat_context`, to another convening `cross_convening_context`, and to another protocol `cross_protocol_context`. |

The registration-level refusals:

- A verified principal that is not the assignment's `holder` is `wrong_principal`, even when the proof is valid.
- A second key for an assignment is `assignment_already_registered`.
- A fingerprint already registered for another assignment in the convening is `shared_key`.
- Any `root_key_fingerprint`, `root_signature` or `authorization` member is `root_authorization_refused`. This check runs before the generic closed-shape refusal `registration_malformed`, so a root-authorized legacy request is named for what it is.

## E8. Seat return (`seat-return.schema.yaml`, Phase 4)

Kind: `xfactory_council_seat_return`.

| Member | R/O | Rule |
|---|---|---|
| `protocol`, `assignment_id` | R | |
| `key_fingerprint` | R | It must be the key registered for the assignment. With no key registered the refusal is `return_unregistered`; with a different key it is `return_key_mismatch`. |
| `payload` | R | An object whose content the domain and the consumer agree. It must be admissible under the construction ([R11](research.md#r11--return-payload-admissibility-a-consumer-impact-consequence-of-d1)). |
| `return_digest` | R | `digest`, subject `council_seat_return_payload`, over `payload` (`return_digest_mismatch`). |
| `signature` | R | `signature` over the return context (E9) (`return_signature_invalid`). |

The completion rules, applied against the frozen snapshot:

- The returns must be exactly the frozen `(assignment_id, seat_id)` set.
- An unlisted return is `return_unlisted`; a repeated one is `return_duplicate`; a missing one is `return_missing`.
- The same count with different identities is `completion_set_mismatch`.
- A return replayed into another assignment, convening or protocol is `return_replayed` (or the matching `cross_*_context`).
- Only after these checks pass does the consumer's existing verdict computation run (spec User Story 2).

## E9. Signing contexts (`signing-context.schema.yaml`, Phase 4)

Both contexts are closed objects that are signed and never stored on their own. **Signed bytes** = UTF-8 of `xfc-jcs-sha256-1`'s serialization (`canonical.serialize`) of the context ([R3](research.md#r3--digest-construction-subjects-and-signed-bytes)).

| Member | Registration context | Return context |
|---|---|---|
| `signing_context` | `xfc-resolved-council-1/seat-key-registration` | `xfc-resolved-council-1/seat-return` |
| `protocol`, `convening_id`, `council_id`, `candidate`, `assignment_id`, `seat_id`, `key_fingerprint` | R | R |
| `convening_digest` | R (the digest's `value` string) | R |
| `challenge_id`, `challenge_nonce` | R | — |
| `return_digest` | — | R (the digest's `value` string) |

A verifier builds the context from the frozen assignment, the issued challenge or the registered key, and the presented record. It never builds the context from caller-supplied labels.

## E10. Producer workflow binding (`producer-binding.schema.yaml` + `.template.yaml`, Phase 5)

Kind: `xfactory_council_producer_binding`. The concrete instance's home is [OPEN-2](research.md#r13--producer-workflow-binding-and-its-placement-open-2).

| Member | R/O | Rule |
|---|---|---|
| `protocol` | R | The replacement. |
| `principal_kind` | R | `github_oidc`. |
| `issuer` | R | `const: https://token.actions.githubusercontent.com`. Otherwise `issuer_mismatch`. |
| `audience` | R | A literal string of 1 to 256 characters, with no `*` (`binding_wildcard`). |
| `producer_repository` | R | `repository`. It must not be a `former` spelling or a non-canonical case variant in `repository-identity.yaml` (`repository_identity_former`), and must be resolvable (`repository_identity_unknown`). |
| `repository_id` | R | Integer ≥ 1: the immutable repository identity claim. |
| `subject_template` | R | A literal OIDC `sub` beginning `repo:<producer_repository>:`. A value containing `.github/workflows/`, `@refs/` or `*` is refused: the first two as `subject_workflow_conflation`, `*` as `binding_wildcard`. |
| `permitted_workflows` | R | 1 to 8 entries of `{operation R: commission \| seat_execution, job_workflow_ref R: <owner>/<repo>/.github/workflows/<file>@<ref>, workflow_revision_rule R: <one closed value, per OPEN-3>}`. An unlisted workflow is `workflow_not_permitted`. A revision that breaks the rule is `workflow_revision_ungoverned`. |
| `broker` | R | `{broker_ref R(opaque_id), capability_verified R(boolean), evidence_ref R(opaque_id or null)}`. `false` or `null` parks activation: `broker_capability_insufficient`. |
| `instantiation_stub` | O | `const: true`, in the `.template.yaml` only. A stub is never accepted as a live binding (`binding_malformed`). |

Claims presented without verified signature evidence are `claims_unverified`. The corpus models verified versus decoded-only claims in the `identity` oracle.

## E11. Protocol selection (`protocol-selection.schema.yaml`, Phase 6)

Kind: `xfactory_council_protocol_selection`. This is the shape of each side's governed configuration (H4; 049 T027/T030).

| Member | R/O | Rule |
|---|---|---|
| `side` | R | `producer` or `consumer`. |
| `protocol` | R | A registry `protocol_id` (`protocol_unknown`). |
| `provider_commit` | R | `full_sha`. |
| `provider_bundle` | R | `contract-v<major>.<minor>`, or `null` before Phase 7. A `null` selection may be used only in rehearsal. |
| `corpus_index_sha256` | R | `raw_sha256`. |

The pair rules:

- Two selections match only when `protocol`, `provider_commit`, `provider_bundle` and `corpus_index_sha256` are all equal (`pair_mismatched`).
- A replacement selection outside rehearsal requires the registry status `admission_eligible` (`replacement_not_admission_eligible`).
- A rejection under one protocol selects no other (`rejected_without_fallback`).

## E12. Activation evidence (`activation-evidence.schema.yaml`, Phase 6)

Kind: `xfactory_council_activation_evidence`. One record per act. It records owner acts; it does not perform them.

| Member | R/O | Rule |
|---|---|---|
| `act` | R | `rehearsal`, `activation` or `rollback`. |
| `recorded_at` | R | `utc_instant`. |
| `owner_word` | R for `activation` and `rollback` | `{author, date, verbatim, cite}`. |
| `provider` | R | `{commit, bundle, corpus_index_sha256}`. |
| `producer`, `consumer` | R | `{repository, revision, selection_digest}`, where `selection_digest` is the raw SHA-256 of that side's E11 file. Both must name the same E11 values (`pair_mismatched`). |
| `broker_capability` | R | `{verified: true, evidence_ref}` (`broker_capability_insufficient`). |
| `intake` | R | `{paused_at R, resumed_at O}`. `resumed_at` is allowed only after a passing rehearsal with both sides verified. |
| `in_flight` | R | `{disposition: drained \| cancelled, convening_ids: [...]}`. |
| `rehearsal` | R for `rehearsal` and `activation` | `{corpus_index_sha256, outcome: pass \| fail, evidence_ref}`. |
| `rollback` | R for `rollback` | `{restored_producer, restored_consumer, new_records_retained: true}`. |

A record with any member missing for its act is `activation_evidence_incomplete`. A rollback that lists new-protocol records to be read as legacy is `historical_reinterpretation_refused`.

## E13. Conformance corpus (Phases 1–6; digest registered at Phase 7)

The full format is in [contracts/conformance-corpus.md](contracts/conformance-corpus.md). In summary:

- **The index.** `conformance/index.json`, of kind `openxfactory-council-convening-conformance-index`. It carries every case's `case_id`, `area`, `boundary`, `applies_to`, `requirement_ids`, `path`, `sha256`, and `expected` (outcome and refusal), plus totals.
- **A vector.** `conformance/vectors/<area>/<case_id>.json`, of kind `openxfactory-council-convening-conformance-vector`. It carries its `inputs`, the `environment` oracles, `evaluation_time` and `expected`.

## Refusal vocabulary

The vocabulary is closed and grows by phase. Every code must be probed by at least one vector (`council-convening-refusal-code-without-probe`). The last column is 049's current producer-internal name; T010 and T020 map these one-to-one.

| Code | Boundary | Phase | 049 name today |
|---|---|---|---|
| `convening_malformed`, `value_not_canonicalizable`, `digest_construction_mismatch` | all | 1–2 | `resolution_malformed`, `facts_malformed` |
| `protocol_unknown`, `legacy_protocol_deprecated` (warn), `legacy_protocol_refused` | all | 1, 6, 8 | (`selector_unknown`, T026) |
| `council_unknown` | commission, admission | 2 | `council_unknown` |
| `roster_empty`, `roster_duplicate_seat`, `roster_mismatch` | commission, admission | 2 | `invalid_membership` |
| `mutable_rule_reference`, `rule_path_malformed`, `rule_unavailable`, `rule_unauthorized`, `rule_digest_mismatch`, `rule_superseded` (OPEN-3) | commission, admission | 2 | `mutable_rule_reference`, `rule_unavailable`, `rule_unauthorized`, `rule_revision_ungoverned` |
| `class_unresolved`, `rule_projection_mismatch` | commission, admission | 2 | `class_unresolved`, `opaque_conclusion` |
| `predicate_unknown`, `predicate_parameters_malformed`, `condition_unevaluable`, `condition_result_mismatch`, `condition_seat_unbound` | commission, admission | 2 | `condition_refused`, `condition_unevaluable`, `opaque_conclusion`, `conjunction_seat_unbound` |
| `opaque_conclusion`, `facts_unused`, `consumed_facts_mismatch`, `fact_source_mismatch`, `secret_bearing_fact` | commission, admission | 2 | `opaque_conclusion`, `unused_facts`, `consumed_facts_mismatch`, `secret_bearing_fact` |
| `candidate_mismatch`, `candidate_head_moved`, `candidate_head_unavailable` | commission, admission | 2 | `candidate_identity_mismatch`, `final_head_moved`, `final_head_unavailable` |
| `snapshot_malformed`, `assignment_malformed`, `assignment_set_mismatch`, `assignment_duplicate`, `assignment_shared_holder`, `convening_conflict` | admission | 3 | `assignment_malformed`, `assignment_shared_holder` |
| `assignment_not_yet_valid`, `assignment_expired`, `operation_not_permitted` | registration, return | 3 | — |
| `return_unlisted`, `return_duplicate`, `return_missing`, `completion_set_mismatch` | completion | 3 | `return_unlisted`, `return_duplicate`, `return_missing`, `completion_set_mismatch` |
| `challenge_malformed`, `challenge_unknown`, `challenge_wrong_assignment`, `challenge_consumed`, `challenge_expired` | registration | 4 | the same names |
| `registration_malformed`, `wrong_principal`, `cross_seat_context`, `cross_protocol_context`, `cross_convening_context`, `fingerprint_mismatch`, `assignment_already_registered`, `shared_key`, `proof_invalid`, `root_authorization_refused` | registration | 4 | the same names |
| `return_malformed`, `return_unregistered`, `return_replayed`, `return_key_mismatch`, `return_digest_mismatch`, `return_signature_invalid` | return | 4 | the same names |
| `binding_malformed`, `issuer_mismatch`, `binding_wildcard`, `repository_identity_former`, `repository_identity_unknown`, `subject_workflow_conflation`, `workflow_not_permitted`, `workflow_revision_ungoverned`, `claims_unverified`, `broker_capability_insufficient` | binding | 5 | — |
| `selection_malformed`, `pair_mismatched`, `rejected_without_fallback`, `replacement_not_admission_eligible`, `activation_evidence_incomplete`, `historical_reinterpretation_refused` | selection, activation, historical | 6 | `pair_mismatched`, `rejected_without_fallback`, `replacement_not_admitted` |
