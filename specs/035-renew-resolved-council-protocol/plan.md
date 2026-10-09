# Implementation Plan: Neutral resolved council protocol

**Branch**: `035-renew-resolved-council-protocol-publish` (feature `035-renew-resolved-council-protocol`) | **Date**: 2026-10-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification [spec.md](spec.md); governing change [renew-resolved-council-protocol](../../openspec/changes/renew-resolved-council-protocol/proposal.md), design D1–D5 ([design.md](../../openspec/changes/renew-resolved-council-protocol/design.md)), seven ADDED `roles-authority-model` requirements ([spec delta](../../openspec/changes/renew-resolved-council-protocol/specs/roles-authority-model/spec.md)), [implementation handoff](../../openspec/changes/renew-resolved-council-protocol/implementation-handoff.md) and [ratification record](../../openspec/changes/renew-resolved-council-protocol/review/ratification-2026-10-03.md).

**Authority**:

- The change is ratified (Brett Heap, 2026-10-03, "ratify all three as disclosed"). Its packet, #1267, landed in `main` as `80f47483` on 2026-10-08.
- Lane codeXfactory-2 builds this feature on Brett Heap's 2026-10-08 word "This lane, 035 then 025 (Recommended)".
- Brett Heap ruled the plan's five open questions, and the three follow-ups that apply OPEN-3, on 2026-10-08 ([Decisions ruled by Brett Heap](#decisions-ruled-by-brett-heap)).
- Every pull request this plan produces lands only on his word. This plan authorizes no release, tag, pin, credential, deployment or activation act.

## Summary

Realize the provider half of the replacement council protocol as neutral contract bytes in `opensoft/openxFactory`: a new `contracts/council-convening/` family, a closed predicate registry with its input contracts, a provider reference implementation and canonical validator, and a shared positive/negative conformance corpus with a pinnable digest. Two independent successors consume it: the producer, codexFactory feature 049 (`realize-resolved-council-protocol`), and the consumer, Hermes feature 025 (`admit-resolved-council-protocol`).

The family defines what both sides need and neither may invent:

- the commission record `council_convening` with its resolved, ordered roster and reproducible provenance, including the governed sources and the class-selection inputs (D1);
- the frozen snapshot and per-seat assignment identities (D2);
- the challenge, key registration, signed return and two versioned signing contexts (D3);
- the producer workflow binding derived from `contracts/policies/repository-identity.yaml` (D4);
- the protocol registry and classification, per-side protocol selection, activation evidence and historical classification (D5);
- one normative evaluation order per boundary, so that two implementations agree on the refusal, not only on refusing ([R21](research.md#r21--normative-evaluation-order)).

Every digest reuses the existing `xfc-jcs-sha256-1` construction by adding subjects to its closed enumeration. It never adds a second construction ([research R3](research.md#r3--digest-construction-subjects-and-signed-bytes)).

Delivery is nine phases. Each lands as its own reviewed pull request:

- Phases 1–6 build the family on `main` in a dormant, unregistered state. The successors can then implement against a reviewed provider commit, as D5 allows.
- Phase 7 cuts the additive-and-deprecating minor.
- Phase 8 cuts the removal major.
- Phase 9 closes out the evidence.

Version numbers are allocated only inside Phases 7 and 8, under the release lock. Each annotated tag is an owner act.

## Technical Context

**Language/Version**: Python 3.12 (validator, reference implementation, generator and tests; the py-bench interpreter is 3.12.3). YAML 1.2 for schemas and registries, as house JSON Schema draft 2020-12. JSON (RFC 8259) for the conformance corpus ([R2](research.md#r2--corpus-encoding-json-vectors-and-a-json-index)).

**Primary Dependencies**: all are already in the tree, and no new third-party dependency is introduced.

- `jsonschema` and `PyYAML`.
- `scripts/signed_execution_chain/canonical.py`, the one `xfc-jcs-sha256-1` implementation.
- `scripts/signed_execution_chain/ed25519.py`, the stdlib Ed25519 verifier.
- The existing repository-identity reader, `load_transfers` in `scripts/estate_inventory.py`.
- The provider's existing secret detector floor, `SECRET_PATTERNS` in `scripts/validate-domain-factory.py`, loaded by `importlib`.
- `cryptography==50.0.0`, already hash-locked in `requirements/hermes-runtime-contracts.lock`, used only by the corpus generator to sign fixtures.

**Storage**: files in the repository. The contracts are data; there is no runtime store. Persistence, transactions and uniqueness belong to the consumer (025).

**Testing**: pytest under `tests/council_convening/`, run as `python3 -m pytest tests/council_convening -q -m "not postgres"`. Each phase also runs the repository gates: the pinned OpenSpec CLI, doc-health in single-repo mode and `pytest-suite`. Phase 1 also runs the two validators that consume the widened digest-subject enumeration. The canonical validator adjudicates every corpus vector on every run.

**Target Platform**: CI (GitHub Actions, `ubuntu-latest`) and the declared py-bench development container.

**Project Type**: a contract family, a canonical validator with a reference implementation, and a conformance corpus, in an existing repository. It is not an application, and nothing here listens on a socket or holds a key.

**Performance Goals**: none imposed. The validator walks a bounded corpus in CI.

**Constraints**:

- **No second vocabulary or construction.** Digests are `xfc-jcs-sha256-1` subjects. Key fingerprints use the estate's one spelling, `sha256:` + the lowercase hex SHA-256 of the raw 32-byte public key (openXwallet `fingerprint_of_public_key`; codexFactory `key_fingerprint`). *Corrected 2026-10-09 on Brett Heap's ruling of 2026-10-09T02:36:50Z, "Estate spelling (Recommended)": this sentence read "`sha256:` + hex of the raw 32-byte public key"; see data-model E1 `key_fingerprint`.* Per-file hashes are plain SHA-256 over bytes. Repository identity is read from `repository-identity.yaml`.
- **No producer code is copied into the provider.** The reference implementation is written from this family's own specification. It is a third implementation, and agreement between the producer and the consumer is proven by the shared corpus (FR-010, SC-001).
- **No version is reserved.** Numbers are allocated at Phase 7 and Phase 8 from the manifest as it then stands (Principle VI; D5).
- **No live values.** Nothing committed carries a live credential, live key material, a live audience or a live subject template. Fixture keys follow [R18](research.md#r18--fixture-keys-and-reproducible-signatures).
- **Neutrality.** Family schemas name no domain, council, seat or workflow. Domain facts appear only as instance data in the corpus or a `.template.yaml` stub (Principle I).
- **Fail closed on legacy bytes.** This family never passes a legacy record. It refuses one under a replacement selection and routes one to the legacy verifier otherwise, with exit 3, which is never a pass ([R10](research.md#r10--protocol-and-signing-context-identifiers-and-classification)).
- **Dormancy.** The replacement protocol is `available` and selectable for rehearsal only. No record of this family can make it active before the removal major and the owner's activation (FR-011, FR-012).
- **No new skip.** `pytest-suite` pins `EXPECT_SKIPPED` exactly. The new tests need no submodule and no network, and `cryptography` is installed from the lock in CI.

**Scale/Scope**: 13 schemas and 2 closed registries, 1 template, 1 conformance index with roughly 160 vectors, 1 reference package, 1 validator and 1 generator, 1 test package, 1 CI gate, 1 runbook, and the registration surfaces of two release cuts. The vector count is re-baselined at each release against the actual union of cases, not against the old #517 counts (handoff).

## Constitution Check

*GATE: evaluated before Phase 0 research and re-evaluated after Phase 1 design, then again after the analysis fixes and Brett Heap's rulings of 2026-10-08. All evaluations pass.*

| Principle | Pre-design | Post-design evidence |
|---|---|---|
| I. Contract-First, Domain-Neutral Core | PASS | The family names no domain, council, seat or workflow in schema vocabulary. The two predicate kinds are mechanical path-set intersections over declared input contracts ([R5](research.md#r5--the-closed-predicate-registry-and-input-contracts)), adopted under the ratified D1 ("the closed predicate registry and input type contracts are shared specifications and vectors"). Their identifiers are the ones the governed rule files declare, on Brett Heap's ruling "Keep the existing names (Recommended)" (OPEN-5, 2026-10-08). That ruling reads the Goals' "Domain predicates remain domain-owned" as: the domain owns which seats a rule conditions on and with which parameters, while the mechanism is neutral. Domain rule files stay domain-owned: each side maps them through its own adapter (D1, H1). |
| II. Governed Change Flow | PASS | The governing change is ratified, its packet is in `main` at `80f47483`, and this is its sole Speckit feature (proposal Impact; tasks 2.2). The feature adds no spec delta. Any rule found missing becomes a finding for a successor change, never an edit here. Because `code_surface` is not `none`, the change archives only on merged, green realization evidence plus the linked successor evidence (proposal front matter). |
| III. Document Lifecycle and Status Discipline | PASS | The family README and the activation runbook carry `Status: ratified` and `Ratified by: renew-resolved-council-protocol`, because they realize ratified text. These feature planning files carry no `Status:` header, following the 028 and 037 precedent. |
| IV. Schema and Artifact Discipline | PASS | Every YAML and every corpus JSON file carries `schema_version` and `kind`. The binding ships only as `producer-binding.template.yaml`; the instance lives in the consumer's runtime configuration (OPEN-2). Every new document is linked in the `README.md` document index **in the PR that creates it**: this plan's documents now (C1), `evidence.md` at T001, the family README at T004 (also in the `contracts/README.md` native index, as pending), and the runbook at T062. The cut (T072) only changes the family's rows from pending to registered. There are no credentials and no host-absolute paths. |
| V. Validation Gates (NON-NEGOTIABLE) | PASS | Each phase runs: its tests first, failing; then the canonical validator self-test; the pinned OpenSpec CLI; a doc-health comparison of base against head; and `pytest-suite` floors with no new skip. Phase 1 also runs `validate-signed-execution-chain.py` and `validate-clearing-dispatch.py`, because it widens the digest-subject enumeration they consume. Every refusal and finding code in the vocabulary at a commit needs a probing vector, or the validator fails (`council-convening-refusal-code-without-probe`). |
| VI. Versioned, Content-Addressed Releases | PASS | Two cuts, each with the five coordinated values. Registration happens only at a cut. Phase 1's manifest-row refresh changes no version and no CHANGELOG entry, following the row's own recorded precedent that a row moves with its bytes and the version is the cutting session's act. The family joins the release inventory behind `COUNCIL_CONVENING_RELEASE_FLOOR` at the Phase 7 cut (OPEN-4). Each tag is Bundle Realization Order step 5, an owner act at the landed commit. A deprecation minor precedes the removal major, as § Change Classes requires (D5). At the major, per-file `contract_schema_version` stays `1`, because no schema's shape changes; the break is carried by the bundle major, the digests and the migration note, following the policy's ideation-dashboard precedent ([R19](research.md#r19--release-sequencing-and-the-two-cuts)). |
| VII. Fail-Closed Authority Boundaries | PASS | Every enumeration is closed: protocols, predicates, input contracts, refusal codes, finding codes, principal kinds and the workflow-revision rule. Classification runs first at every boundary over a protocol-carrying record, a legacy record is refused or routed but never passed, and the record has no fallback protocol. An unevaluable condition refuses rather than reading as false. Possession of a key is not authority (D3). A broker that is not verified parks activation (D4). Model output is never authoritative here: the validator decides only shapes and reproductions. |

Repository constraints honored:

- shared-tree discipline: this worktree has one writer, and pathspec commits only;
- worktree mode;
- the aggregation pin is a separate later sync;
- no runtime code beyond the ratified canonical validator and reference implementation (constitution, Repository Constraints).

The one workflow deviation, planning before the questions were ruled, is recorded and closed under [Complexity Tracking](#complexity-tracking).

## Project Structure

### Documentation (this feature)

```text
specs/035-renew-resolved-council-protocol/
├── spec.md                         # existing (ratified scope), with § Clarifications
├── checklists/requirements.md      # existing
├── clarify-questions.md            # the five questions, the three follow-ups, N10, and Brett Heap's rulings
├── plan.md                         # this file
├── research.md                     # Phase 0: decisions R1–R21
├── data-model.md                   # Phase 1: entities E1–E13, evaluation orders, refusal vocabulary
├── quickstart.md                   # Phase 1: validation and pinning guide
├── contracts/
│   ├── provider-interface.md       # what 049 and 025 consume, when it exists, and consumer impacts
│   ├── conformance-corpus.md       # index/vector format, adapter contract, digest
│   └── validator-cli.md            # canonical validator CLI, modes, exits, findings
├── tasks.md                        # Phase 2 (speckit-tasks)
├── analysis.md                     # speckit-analyze record and dispositions
└── evidence.md                     # created by T001; one section per phase
```

### Source Code (repository root)

```text
contracts/council-convening/                       # NEW family (dormant until Phase 7)
├── README.md                                      # Status: ratified / Ratified by:
├── shared-definitions.schema.yaml                 # identifiers, candidate, digest refs, refusal and finding codes
├── protocol-registry.schema.yaml
├── protocol.registry.yaml                         # CLOSED: replacement + legacy (identification)
├── predicate-registry.schema.yaml
├── predicate.registry.yaml                        # CLOSED: two predicates, two input contracts
├── council-convening.schema.yaml                  # D1 commission record
├── convening-snapshot.schema.yaml                 # D2 frozen snapshot
├── seat-assignment.schema.yaml                    # D2/D3 public assignment
├── registration-challenge.schema.yaml             # D3
├── seat-key-registration.schema.yaml              # D3
├── seat-return.schema.yaml                        # D3
├── signing-context.schema.yaml                    # D3 registration + return contexts
├── producer-binding.schema.yaml                   # D4
├── producer-binding.template.yaml                 # D4 instantiation stub only
├── protocol-selection.schema.yaml                 # D5 / H4
├── activation-evidence.schema.yaml                # D5
└── conformance/
    ├── index.json                                 # the corpus digest's subject (raw bytes)
    └── vectors/<area>/<case_id>.json

contracts/signed-execution-chain/digest-construction.schema.yaml   # MODIFIED: +2 digest subjects
scripts/signed_execution_chain/canonical.py                        # MODIFIED: SUBJECTS mirror +2

scripts/council_convening/                          # NEW provider reference implementation
├── __init__.py
├── records.py         # schema registry, closed shapes, full-match identifiers
├── classification.py  # protocol classification and selection effects (E1)
├── predicates.py      # predicate registry semantics
├── resolution.py      # roster composition and provenance reproduction (oracles injected)
├── assignments.py     # snapshot, assignment, retry identity; completion (Phase 4)
├── signing.py         # contexts, signed bytes, verification, fingerprints
├── binding.py         # producer binding against repository-identity.yaml
├── migration.py       # selection, activation evidence, deprecation, historical mode
├── corpus.py          # index closure, digests, coverage, vector adjudication
└── generate.py        # deterministic corpus generator (fixture signing only)
scripts/validate-council-convening.py               # NEW canonical validator CLI

tests/council_convening/                            # NEW
.github/workflows/council-convening-gate.yml        # NEW gate (reports; requiring it is an owner act)
docs/council-convening-activation-runbook.md        # NEW (Phase 6)

# Registration surfaces, Phase 7 (minor) and Phase 8 (major) only:
contracts/manifest.yaml, contracts/CHANGELOG.md, contracts/README.md, README.md,
contracts/releases/contract-v<allocated>.digests.yaml, docs/contract-versioning-policy.md,
scripts/hermes_runtime_validation/release.py (Phase 7, COUNCIL_CONVENING_RELEASE_FLOOR),
tests/hermes_runtime_contracts/test_council_convening_release_floor.py (Phase 7),
contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml (Phase 8)
```

**Structure Decision**: The family lives at `contracts/council-convening/`, the path the governing change's `code_surface` names. The corpus lives under `conformance/`, not `examples/`, because it is a cross-implementation corpus whose index carries the expectations. It follows the indexed-fixture precedent of `contracts/hermes-runtime/fixtures/index.yaml`. It does not use the per-file `# expected_failure:` header convention, which JSON cannot carry ([R1](research.md#r1--family-layout-and-corpus-placement)).

The reference implementation is a package, so each phase adds one module beside its tests. The validator stays a thin CLI over it, following `scripts/validate-contract-release.py` over `scripts/hermes_runtime_validation/`.

## Phase 0 — Research

See [research.md](research.md). Twenty-one decisions are recorded, each traced to the spec, a design decision (D1–D5) and a consumer need. The five questions only Brett Heap could decide, and the three follow-ups that apply OPEN-3, were put to him and ruled on 2026-10-08 (below). No `NEEDS CLARIFICATION` remains in the Technical Context.

## Phase 1 — Design

- [data-model.md](data-model.md) describes thirteen entities member by member, each boundary's normative evaluation order, and the closed refusal vocabulary. A column maps each refusal to 049's current producer-internal name; the mapping is many-to-one in places, and 049 refines its refusals to match.
- [contracts/provider-interface.md](contracts/provider-interface.md) lists everything 049 and 025 consume, including the identifiers, kinds, signing contexts, signed-bytes construction, digest subjects and pinning recipe. It says in which phase each item first exists on `main` and when it is published, and it records every consumer impact this plan creates.
- [contracts/conformance-corpus.md](contracts/conformance-corpus.md) covers the corpus index and vector format, the oracle model each implementation's corpus adapter feeds, outcome semantics, coverage and the corpus digest.
- [contracts/validator-cli.md](contracts/validator-cli.md) covers the canonical validator's modes, exit codes and finding codes.
- [quickstart.md](quickstart.md) gives the commands that prove each phase and the consumer pinning recipe.

The agent-context update step of the plan template has no script in this repository: `.specify/scripts/bash/` carries none. `AGENTS.md` has no managed active-feature block. The only pointer the setup step wrote is `.specify/feature.json`, which `.gitignore` excludes as worktree-local state. No repository-wide pointer moved.

## Phase map (implementation; one reviewed pull request per phase)

| Phase | Lands | 049 tasks it unblocks (provider half) | 025 requirements it serves |
|---|---|---|---|
| 1 Setup & foundational | Family skeleton and README, `shared-definitions`, protocol registry and classification, two digest subjects, corpus index and vector format, generator skeleton, validator skeleton, CI gate | T027 and T026→T030 (protocol identifier values to bind), T001's follow-up dated section | FR-001 (exact contract identity), FR-011 (protocol identifiers, classification) |
| 2 US1: membership before work (MVP) | `council_convening`, predicate registry and input contracts, resolution reproduction in the normative order, US1 corpus | T003, T010, T011 (the gate-rules `subject_path`), T011b (POST body shape, with 025), T012 (head-race half), T013 | FR-001–FR-004 |
| 3 US2a: frozen assignments | Snapshot, assignment and retry identity, with their vectors | T012 (retry identity), T015b, T016b (assignment shape) | FR-005–FR-007 |
| 4 US2b: seat signing and completion (lands after Phase 5) | Challenge, registration, return, the two signing contexts, return digest, completion over the frozen identities, key and completion vectors | T020, T017/T019 (context mapping), T021/T022 (completion mapping), T025 (what consumer evidence must show) | FR-007 (completion), FR-008–FR-010 |
| 5 US2c: producer identity | Producer binding schema and template, repository-identity derivation, identity vectors | T023, T024, T031 (the shape the owner provisions) | FR-008 (principal inputs); H3 activation park |
| 6 US3: matched migration | Protocol selection, activation evidence, historical mode, deprecation routing, migration vectors, activation runbook | T027 (selection shape), T028, T029, T032 | FR-011, FR-012 |
| 7 Release A: additive and deprecating minor | Registration, release floor, CHANGELOG, policy deprecation entry, inventory, index rows. OWNER: tag | T030 (minor half), T003 (published pin) | FR-011, FR-012 (published compatible pin) |
| 8 Release B: removal major | Legacy refusal for active selection, migration note, executed deprecation, row refresh, inventory. OWNER: tag | T030 (major half); a prerequisite of T033 and T034 | FR-011 (old shapes refused), FR-012 |
| 9 Closeout | Evidence acceptance and handoff; archive stays gated | T036 (provider evidence) | 3.1 / 3.3 evidence |

The task ids in the 049 column are 049's own. All 025 entries are requirement identifiers: feature 025 has a specification and checklist only, and no task list exists on `025-admit-resolved-council-protocol-spec`.

**Order and parallelism.**

- #1267 is in `main` (`80f47483`), so that precondition is satisfied. This planning PR, #1268, lands on Brett Heap's word before PR-1 opens (I5).
- Phase 1 precedes everything.
- Phases 2→3 are sequential, because the snapshot binds the commission record.
- Phase 5 may be authored in parallel from Phase 1. It lands after Phases 2 and 3, because binding runs inside admission and PR-5 re-authors every admission vector at that commit, and because its workflow-revision rule reads the E2 `governed` member.
- Phase 4 needs Phases 3 and 5: registration checks a seat job's claims against its holder's binding (data-model E7 step 5). So the landing order is 1, 2, 3, 5, 4, 6.
- Phase 6 needs Phases 2–5.
- Phase 7 needs Phases 1–6 merged plus a claim on the contract-cut shared substrate.

Phase 8 needs four things:

- Phase 7's tag published and verified;
- at least one full minor served;
- the successors' dormant implementations verified against the published minor (D5, Migration Plan);
- the owner's release act.

Phase 9 follows Phase 8 and the successor evidence.

**Dormancy.** No consumer may activate the replacement before Phase 8 and the owner's matched activation (T034 in 049; FR-012 in 025). The successors may pin a reviewed `main` commit after any of Phases 1–6 to build dormant code (D5: "Successors can implement the new protocol dormant against a reviewed provider commit").

## Decisions ruled by Brett Heap

Five questions were left for Brett Heap, each with a recommendation. He ruled all five on 2026-10-08, first-hand, choosing the recommended option of each. The record is brett-wip `lanes/log/codeXfactory-2.md`, RULED at 19:24:21Z (OPEN-1 to OPEN-4) and 19:24:59Z (OPEN-5). Applying OPEN-3 raised three follow-up questions and one packet question (N10); he ruled those on 2026-10-08 too, again choosing the recommended option of each, RULED at 23:03:35Z (lines 209–212 of the same log). The labels are quoted verbatim. The questions and options are in [clarify-questions.md](clarify-questions.md), and the answers are encoded in [spec.md § Clarifications](spec.md#clarifications).

- **OPEN-1: lifetime ceilings.** Ruled "600 s challenge, 6 h assignment (Recommended)".
  - A challenge lives at most 600 seconds, and an assignment at most 21600 seconds. These are contract maximums; the consumer configures any tighter value.
  - Encoded in [R12](research.md#r12--lifetime-ceilings), data-model E5 and E6, and the ceiling tests, vectors and schemas in Phases 3 and 4 (T035, T036, T038; T042, T044, T046).
- **OPEN-2: where the concrete producer-binding instance lives.** Ruled "Consumer's runtime config (Recommended)".
  - The instance is written into the consumer's governed runtime configuration at the provisioning act (049 T031; 025 H3), and validated by this family's validator at the consumer's pin.
  - The provider ships only the schema, a `.template.yaml` stub, the derivation from `repository-identity.yaml` and the corpus.
  - Encoded in [R13](research.md#r13--producer-workflow-binding-and-its-placement), data-model E10, and T052, T053 and T055.
- **OPEN-3: revision currency.** Ruled "History + unchanged rule file (Recommended)".
  - A cited revision must be on the governed branch's first-parent history, and the rule file at that revision must equal its counterpart at the governed tip when admission runs; otherwise `rule_superseded`. `rule_superseded` is normative at admission; a producer's commission-time comparison is a non-normative pre-check. The plan names the off-history failure `rule_revision_ungoverned`, a disclosed two-code refinement of the one ruled refusal.
  - Where the rule repository is the producer repository, the producer's verified `job_workflow_sha` must equal the cited rule revision. The binding's closed `workflow_revision_rule` has two values: `equals_governed_revision` for the commission job, and `on_governed_history_since_revision` for a seat job (follow-up 3).
  - Encoded in [R7](research.md#r7--governed-sources-rule-authority-and-revision-currency), data-model E2 step 5 and E10, and T025, T026, T031, T050, T051 and T053.
  - Its three follow-ups, ruled 2026-10-08 ([analysis.md § Ruled](analysis.md#ruled)):
    1. "Every governed source (Recommended)": the currency test covers every governed source the convening cites, not only the rule file (Phase 2);
    2. "job_workflow_ref's repo (Recommended)": the ruling's "producer repository" is the repository named in `job_workflow_ref`, and a permitted producer workflow outside the governed repository is refused, failing closed (Phase 5);
    3. "At or after the frozen rev (Recommended)": a seat job's workflow commit must be on the governed history at or after the frozen revision, not equal to it (Phases 4 and 5). The plan adds, as its own requirement and not as part of the ruling, that a seat job checks out its tooling at its verified `job_workflow_sha` (R7).
- **OPEN-4: release-inventory membership.** Ruled "Join behind a version floor (Recommended)".
  - `COUNCIL_CONVENING_RELEASE_FLOOR` is set at the Phase 7 cut, following the clearing precedent (#722, ruled in #745).
  - Encoded in [R15](research.md#r15--release-surface-membership), T066 and T068.
- **N10: the packet's stale allocation notes.** Ruled "Dated correction + tick 2.2 (Recommended)". #1268 replaces the 2026-10-03 allocation notes under `openspec/changes/renew-resolved-council-protocol/` with a dated allocation record, ticks packet task 2.2, and lands in a Rule 6 window.
- **OPEN-5: predicate identifiers.** Ruled "Keep the existing names (Recommended)".
  - The neutral registry keeps `changed_paths_intersect` over `pr_facts` and `rule_touches_security_posture` over `rule_facts`, exactly as the governed rule files declare them, with no mapping layer.
  - "Domain predicates remain domain-owned" means the domain owns which seats a rule conditions on and with which parameters, while the evaluation mechanism is neutral. Adding or renaming a predicate is a governed contract change.
  - Encoded in [R5](research.md#r5--the-closed-predicate-registry-and-input-contracts), data-model E3, and T024, T026 and T028.

## Owner gates this plan reaches and does not perform

Each act below is the owner's, and no task here performs it. Each is recorded with dated evidence, and its box stays unticked:

- landing each phase PR, and this planning PR (Brett Heap's word);
- making `council-convening-gate` a required check (a ruleset act);
- allocating and publishing each release, and the annotated tags (change task 3.2);
- the successors' pin advances;
- broker and credential provisioning, including writing the binding instance into the consumer's runtime configuration;
- managing-factory deployment;
- the commissioning pause, matched activation and paired rollback (change tasks 3.3 and 3.4);
- the archive (change task 3.5).

## Complexity Tracking

**One workflow deviation, recorded and now closed.** The constitution says "material ambiguities MUST be resolved before planning". This plan was written with five questions open (OPEN-1 to OPEN-5) and recommendations beside each, because they surfaced only while planning against the two consumers, and the ratified spec had stated "The scope contains no new unresolved policy decision". The independent analysis (C2 in [analysis.md](analysis.md)) flagged it as critical. The resolution:

- the lane coordinator put the questions to Brett Heap on 2026-10-08, and he ruled all five that day;
- applying OPEN-3 raised three follow-ups (which sources, which repository, the seat's commit). Analysis rounds 2 to 4 planned each at its fail-closed default and flagged it for confirmation, rather than claiming it as ruled; he ruled all three that day too, choosing those defaults;
- they are recorded in [clarify-questions.md](clarify-questions.md) and encoded in [spec.md § Clarifications](spec.md#clarifications), with a dated note on the Assumptions sentence;
- this plan and its research now state each as decided, and no task is gated on an open question or a confirmation.

No implementation began before the rulings. No other deviation is requested.

Several simpler options were considered and rejected in research:

- One combined schema file was rejected: closed kinds per record are the house closure unit.
- A YAML corpus was rejected because of resolver ambiguity across independent readers ([R2](research.md#r2--corpus-encoding-json-vectors-and-a-json-index)).
- Reusing the producer's evaluator as the provider's check was rejected (handoff: "never copy the producer evaluator into the provider and call that independent validation").
- A second signed-bytes framing beside `xfc-jcs-sha256-1` was rejected (D1).
- Accepting legacy records with no finding was rejected as failing open ([R10](research.md#r10--protocol-and-signing-context-identifiers-and-classification)).

## Extension hooks

`.specify/extensions.yml` registers optional `before_plan`, `after_plan`, `before_analyze` and `after_analyze` hooks, all `speckit.git.commit`. `.specify/extensions/git/git-config.yml` disables auto-commit, so none of them ran. The lane commits with explicit pathspecs instead.
