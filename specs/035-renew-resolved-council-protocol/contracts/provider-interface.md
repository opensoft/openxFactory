# Provider interface: what 049 and 025 consume

**Feature**: [spec.md](../spec.md) · **Plan**: [plan.md](../plan.md) · **Data model**: [data-model.md](../data-model.md)

This document lists the provider facts each successor needs and must not invent. For each fact it gives the planned value, the phase that first lands it on `main`, and the release that publishes it.

"Lands" is not "published". A successor may build dormant code against a reviewed `main` commit after the landing phase (D5). A successor activates only against the published releases, after Phase 8 and the owner's matched activation. Until a schema lands, the authoritative statement is that schema, never this table.

## The facts, and when each exists

| Provider fact | Planned value or location | Lands | Published | 049 tasks | 025 requirements |
|---|---|---|---|---|---|
| Replacement protocol identifier | `xfc-resolved-council-1` | Phase 1 (`protocol.registry.yaml`) | Phase 7 minor | T026→T030, T027 | FR-001, FR-011 |
| Legacy protocol identification | `xfactory-council-seat-return/v1` entry, recognition rules (data-model E1) | Phase 1 | Phase 7 (`deprecated`), Phase 8 (`historical_only`) | T028 | FR-011 |
| Digest construction | `xfc-jcs-sha256-1`, subjects `council_convening`, `council_seat_return_payload` | Phase 1 | Phase 7 | T010, T020 | FR-001, FR-010 |
| Commission record schema | `contracts/council-convening/council-convening.schema.yaml`, kind `xfactory_council_convening` | Phase 2 | Phase 7 | T010, T011b, T013 | FR-001–FR-004 |
| Predicate registry and input contracts | `predicate.registry.yaml`: `changed_paths_intersect` over `pr_facts`; `rule_touches_security_posture` over `rule_facts` | Phase 2 | Phase 7 | T003, T010 | FR-002, FR-003 |
| Conformance corpus and digest | `conformance/index.json`, plus the manifest row `sha256` of that file | Phases 1–6 (vectors); Phase 7 (digest row) | Phase 7 | T003, T013 | FR-001–FR-012 (agreement) |
| Canonical validator | `scripts/validate-council-convening.py`, modes in [validator-cli.md](validator-cli.md) | Phase 1 (skeleton) to Phase 6 | Phase 7 | T003, T010, T035 | FR-001 |
| Snapshot and assignment shapes | `convening-snapshot.schema.yaml`, `seat-assignment.schema.yaml` | Phase 3 | Phase 7 | T012, T015b, T016b, T021, T022 | FR-005–FR-007 |
| Challenge, registration and return shapes | `registration-challenge`, `seat-key-registration`, `seat-return` schemas | Phase 4 | Phase 7 | T020, T025 | FR-008–FR-010 |
| Signing-context strings | `xfc-resolved-council-1/seat-key-registration`, `xfc-resolved-council-1/seat-return` | Phase 4 (the registry names them from Phase 1) | Phase 7 | T020 (with T017/T019 mapping) | FR-010 |
| Signed bytes | UTF-8 of `canonical.serialize(context)`; contexts per data-model E9; known-answer vectors carry `expected.signed_bytes` | Phase 4 | Phase 7 | T020 | FR-010 |
| Repository-identity binding | `producer-binding.schema.yaml` and `.template.yaml`; derivation from `contracts/policies/repository-identity.yaml` | Phase 5 | Phase 7 | T023, T024, T031 | FR-008 |
| Protocol selection shape | `protocol-selection.schema.yaml` | Phase 6 | Phase 7 | T027, T030 | FR-011 |
| Activation evidence and runbook | `activation-evidence.schema.yaml`; `docs/council-convening-activation-runbook.md` | Phase 6 | Phase 7 | T029, T032–T034 | FR-012 |
| Deprecation-minor tag | the next available `contract-v<major>.<minor>`, allocated at the cut | — | Phase 7 (OWNER tag) | T030 | FR-011, FR-012 |
| Removal-major tag | the next major after the minor, allocated at the cut | — | Phase 8 (OWNER tag) | T030; T033/T034 prerequisite | FR-011, FR-012 |

## How a successor pins the provider

The rules:

- Pin the **exact openxFactory commit**, never a branch and never a tag alone (Principle VI).
- Record the bundle tag as a label beside the commit.
- Record the `sha256` of `contracts/council-convening/conformance/index.json` from `contracts/manifest.yaml` at that commit. This is the corpus digest; the index pins every vector's bytes.
- Record the manifest `sha256` of each schema the successor reads.

Before Phase 7 there is no manifest row. A dormant build pins the commit and computes the index's raw-byte SHA-256 itself, labelled as unpublished.

In 049 the pin is `stack.yaml` `xfactory.contract_ref` plus governed configuration (T003). In 025 it is the consumer's governed compatibility pin (H4). Both sides' E11 selection records name the same four values, and the matched-pair check compares them.

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
| Broker enforcement | owner-provisioned |

All of these must refuse with the vocabulary in data-model § Refusal vocabulary, or with a one-to-one mapping recorded in that side's evidence.
