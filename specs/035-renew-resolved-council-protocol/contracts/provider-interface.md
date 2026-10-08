# Provider interface: what 049 and 025 consume

**Feature**: [spec.md](../spec.md) · **Plan**: [plan.md](../plan.md) · **Data model**: [data-model.md](../data-model.md)

This document lists the provider facts each successor needs and must not invent. For each fact it gives the planned value, the phase that first lands it on `main`, and the release that publishes it. It also records every change this plan asks of a successor.

"Lands" is not "published". A successor may build dormant code against a reviewed `main` commit after the landing phase (D5). A successor activates only against the published releases, after Phase 8 and the owner's matched activation. Until a schema lands, the authoritative statement is that schema, never this table.

## The facts, and when each exists

| Provider fact | Planned value or location | Lands | Published | 049 tasks | 025 requirements |
|---|---|---|---|---|---|
| Replacement protocol identifier | `xfc-resolved-council-1` | Phase 1 (`protocol.registry.yaml`) | Phase 7 minor | T026→T030, T027 | FR-001, FR-011 |
| Legacy protocol identification and classification | `xfactory-council-seat-return/v1` entry; classification order and selection effects (data-model E1) | Phase 1 | Phase 7 (`deprecated`), Phase 8 (`historical_only`) | T028 | FR-011 |
| Digest construction | `xfc-jcs-sha256-1`, subjects `council_convening`, `council_seat_return_payload` | Phase 1 | Phase 7 | T010, T020 | FR-001, FR-010 |
| Commission record schema and evaluation order | `contracts/council-convening/council-convening.schema.yaml`, kind `xfactory_council_convening`; data-model E2 order | Phase 2 | Phase 7 | T010, T011, T011b, T013 | FR-001–FR-004 |
| Predicate registry and input contracts | `predicate.registry.yaml`: `changed_paths_intersect` over `pr_facts`; `rule_touches_security_posture` over `rule_facts` (ruled, OPEN-5) | Phase 2 | Phase 7 | T003, T010 | FR-002, FR-003 |
| Conformance corpus and digest | `conformance/index.json`, plus the manifest row `sha256` of that file | Phases 1–6 (vectors); Phase 7 (digest row) | Phase 7 | T003, T013 | FR-001–FR-012 (agreement) |
| Canonical validator | `scripts/validate-council-convening.py`, modes in [validator-cli.md](validator-cli.md) | Phase 1 (skeleton) to Phase 6 | Phase 7 | T003, T010, T035 | FR-001 |
| Snapshot and assignment shapes | `convening-snapshot.schema.yaml`, `seat-assignment.schema.yaml`; assignment ceiling 21600 s (ruled, OPEN-1) | Phase 3 | Phase 7 | T012, T015b, T016b | FR-005–FR-007 |
| Challenge, registration and return shapes, and the completion order | `registration-challenge`, `seat-key-registration`, `seat-return` schemas; challenge ceiling 600 s (ruled, OPEN-1); the E8 completion order over the frozen identities | Phase 4 | Phase 7 | T020, T021, T022, T025 | FR-005 (completion), FR-008–FR-010 |
| Signing-context strings | `xfc-resolved-council-1/seat-key-registration`, `xfc-resolved-council-1/seat-return` | Phase 4 (the registry names them from Phase 1) | Phase 7 | T020 (with T017/T019 mapping) | FR-010 |
| Signed bytes | UTF-8 of `canonical.serialize(context)`; contexts per data-model E9; known-answer vectors carry `expected.derived.signed_bytes` | Phase 4 | Phase 7 | T020 | FR-010 |
| Repository-identity binding | `producer-binding.schema.yaml` and `.template.yaml`; derivation from `contracts/policies/repository-identity.yaml`; the instance lives in the consumer's runtime configuration (ruled, OPEN-2) | Phase 5 | Phase 7 | T023, T024, T031 | FR-008 |
| Protocol selection shape | `protocol-selection.schema.yaml` | Phase 6 | Phase 7 | T027, T030 | FR-011 |
| Activation evidence and runbook | `activation-evidence.schema.yaml`; `docs/council-convening-activation-runbook.md` | Phase 6 | Phase 7 | T029, T032–T034 | FR-012 |
| Release-inventory membership | `COUNCIL_CONVENING_RELEASE_FLOOR` in `scripts/hermes_runtime_validation/release.py` (ruled, OPEN-4) | — | Phase 7 | T003, T030 | FR-001 |
| Deprecation-minor tag | the next available `contract-v<major>.<minor>`, allocated at the cut | — | Phase 7 (OWNER tag) | T030 | FR-011, FR-012 |
| Removal-major tag | the next major after the minor, allocated at the cut | — | Phase 8 (OWNER tag) | T030; a prerequisite of T033 and T034 | FR-011, FR-012 |

The task ids in the 049 column are 049's own.

## Consumer impacts recorded by this plan

Each item is a change a successor makes to conform. None is hidden behind a claim that the successor needs no change.

| Impact | Who | Where it comes from |
|---|---|---|
| Refusal names are refined, and several internal names split into more than one code. `return_wrong_identity` maps to `completion_set_mismatch`. | 049 T010, T020 | data-model § Refusal vocabulary |
| Refusals follow the normative evaluation order of each boundary; where 049's order differs in detail, it is reordered. | 049 T010; 025 | R21 |
| The gate-rules candidate is respelled: `rule_packet_path` becomes `candidate.subject_path`, `subject_pin` becomes `candidate.head_sha`, and the dispatch's `candidate_pull_number` becomes `candidate.pull_number`. Its `rule_facts` source is `candidate_subject`. | 049 T010, T011 | R6 |
| The merge-readiness record carries `class_inputs` (repository and head ref) from the trusted gather, and both sides check the head ref against the one they read; the consumer reproduces class selection from them. The gate-rules record carries no class inputs, because that council is unclassed. | 049 T010; 025 FR-002 | R6; data-model E2, E3 |
| The record lists every governed source (the council profile `hermes/domain/agent-mixes.yaml`, the council document, each YAML rule file and the listing of the rule directory, the envelope configuration) at one revision. Each is held to the currency test, under Brett Heap's follow-up 1 ruling, "Every governed source (Recommended)". | 049 T010, T023; 025 FR-002 | R7 |
| `rule_superseded` is normative at admission only. 049 may compare its sources with the governed tip at commission as a pre-check, so it does not submit a record the consumer will refuse; that pre-check is producer-side and non-normative, the shared commission vectors carry no `rule_superseded` case, and 049's conformance does not depend on it. | 049 T010; 025 FR-002 | R7; data-model E2 step 5 |
| A changed path longer than 4096 bytes is refused. | 049 T010 | data-model § Shared definitions |
| The floor's `(password\|passwd\|secret\|token)` assignment detector is added to 049's secret scan. | 049 T009, T010 | R9 |
| The seat's whole checked entry is the signed payload, and `model_usage.costUSD` and every other non-integer quantity is written as a `decimal_string`; the cost floor reads the string. | 049 T020; 025 | R11 |
| The commission job's verified `job_workflow_ref` names a workflow in the governed repository, and its verified `job_workflow_sha` equals the record's `governed.revision` (`equals_governed_revision`). The caller, the binding's `caller_repository`, may be another repository, as xFactory's lane calling codexFactory's reusable workflow is. A permitted producer workflow outside the governed repository is refused, under follow-up 2, "job_workflow_ref's repo (Recommended)". | 049 T023 | R7, R13 |
| The consumer runs `binding` inside admission in two parts: E10 steps 1 to 13 as E2 step A1, right after the shape check, verifying the token's issuer, audience, validity window and subject against the binding; and E10 step 14, the workflow revision, as E2 step A4, after E2 step 5 has checked the `governed` member it reads. It routes or refuses legacy records by its selection. | 025 FR-008, FR-011 | data-model E1, E2, E10 |
| The consumer's identity-map read fails closed: an absent or unreadable `repository-identity.yaml`, or one with a malformed row, is `repository_identity_unavailable`, where `load_transfers` alone would return an empty map. A non-canonical case variant is defined mechanically (equal ignoring ASCII case, not byte-equal). | 025 FR-008 | data-model E10; R13 |
| 025's retained guards (025 FR-004) keep their place in the admission order, under their own consumer codes: the council and mix guard at E2 step A2; once-per-pin at E2 step A3, after the identical-retry test, so it never pre-empts an identical retry; `verify_subject_pin` as E2 step 13; and the touched-object and base-branch guards last, at E2 step A5. Its verdict guards run after the E8 completion order. | 025 FR-004 | data-model E2, E8 |
| Retry identity runs at E2 step A3, after classification, shape and binding and before every drift check, so an identical retry returns the same snapshot even after the governed tip or the live head moved. | 025 FR-006; 049 T012 | data-model E2, E4; R21 |
| A consumer's tighter lifetime values apply when it issues an assignment or a challenge. Its verification, and the corpus, use the contract ceilings, so the ceiling vectors pass unchanged. | 025 FR-009 | R12; data-model E5, E6 |
| Registration checks the seat job's claims against its holder's binding (resolved through `holder.binding_ref` to the binding's `binding_id`) the same way. The seat job's workflow commit must be on the governed history at or after the frozen revision (`on_governed_history_since_revision`), under follow-up 3, "At or after the frozen rev (Recommended)". | 025 FR-008; 049 T020 | data-model E7 step 5, E10 |
| **A seat job checks out its trusted tooling at exactly its verified `job_workflow_sha`**, as the commission job already must at the governed revision. The verified commit vouches for the workflow file only, so a seat that runs tooling from another commit runs code nothing verified. 049's seat worker today checks out the default-branch HEAD (049 `contracts/interfaces.md`, W1); conforming changes that. This is a consumer requirement on 049. | 049 T016b, T023 | data-model E10; R7 |
| `broker_capability_insufficient` refuses only at `activation` and `resume` (E12), and at registration for a `governed_broker_job` holder (E7 step 5). A binding whose `broker.capability_verified` is `false` is accepted at binding and admission, which record it. | 025 H3; 049 T024 | data-model E7, E10, E12 |
| The listed governed sources must be exactly the set the projection reads (`governed_sources_mismatch`), so each adapter reports the set it read. | 049 T010; 025 FR-002 | data-model E2 step 5 |

## How a successor pins the provider

The rules:

- Pin the **exact openxFactory commit**, never a branch and never a tag alone (Principle VI).
- Record the bundle tag as a label beside the commit.
- Record the `sha256` of `contracts/council-convening/conformance/index.json` from `contracts/manifest.yaml` at that commit. This is the corpus digest; the index pins every vector's bytes.
- Record the manifest `sha256` of each schema the successor reads.

Before Phase 7 there is no manifest row. A dormant build pins the commit and computes the index's raw-byte SHA-256 itself, labelled as unpublished.

In 049 the pin is `stack.yaml` `xfactory.contract_ref` plus governed configuration (T003). In 025 it is the consumer's governed compatibility pin (H4). Both sides' E11 selection records name the same five matched values, and the matched-pair check compares them.

## How a successor runs the corpus

Each side writes a corpus adapter in its own repository against [conformance-corpus.md](conformance-corpus.md):

1. Read the index.
2. Verify each vector's bytes.
3. Join `$parts` sentinels.
4. Inject the vector's `environment` oracles into its own lookups.
5. Evaluate at the vector's `evaluation_time`.
6. Compare the result with `expected`.

Vectors whose `applies_to` names the side are mandatory for it. Every vector whose `applies_to` lists both `producer` and `consumer` is part of the agreement set SC-001 measures. No side imports another side's code or the provider's reference implementation as its evaluator (D1; R4).

## What stays the successors'

| Item | Owner |
|---|---|
| Domain rule-file adapters | 049, and 025 through H1's allowlisted governed-repository adapter |
| HTTP routes, request and response envelopes, status codes and error bodies | 025 |
| Persistence, transactions and uniqueness | 025 |
| Trusted collection and pre-submit rechecks | 049 |
| Per-seat job isolation and key minting | 049 |
| The binding instance in the consumer's runtime configuration | the operator, at the provisioning act |
| Broker enforcement | owner-provisioned |

Each side refuses with the vocabulary in data-model § Refusal vocabulary, through a total mapping from its internal names that it records in its own evidence. Several internal names may map to one code, and one internal name may need splitting into several.
