# Research: Neutral resolved council protocol

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) · **Date**: 2026-10-08

Each decision records what was chosen, the reason, and the alternatives considered. Each reason is traced to a feature requirement (FR or SC), a ratified design decision (D1–D5), and the consumer need it serves. The consumers are:

- codexFactory feature 049, read at `origin/main` `3d5c2c38` on 2026-10-08;
- Hermes packet `admit-resolved-council-protocol` (design H1–H4) and its feature 025 spec.

Four questions are left **OPEN** for Brett Heap, each with a recommendation: R7, R12, R13 and R15. The plan proceeds without deciding them, and the tasks that depend on each one say so.

## Inputs read, and the facts this research rests on

- **Provider base.** This worktree sits at `5e2e6b5e` (the 035 branch over #1267's `237e63a0`). The manifest declares `contract_bundle_version: contract-v4.0`, and `contract-v4.0` is tagged on the remote. No `contracts/council-convening/` exists on `main`. The old #517 candidate (branch `026-add-resolved-council-seats`) is preserved for reference only, and nothing here depends on it.
- **The legacy protocol is not provider-owned.** The roster-less `council_convening` envelope block is Hermes-local: `council_id`, `subject_pin`, `packet_refs`, optional `mix_id`, with `members` derived from materialized council content (`src/hermes_install/domain/council_orchestration.py`). Its two signing contexts are `xfactory-council-seat-return/v1` and the root-authorized `xfactory-council-seat-key-authorization/v1`. Both are defined by codexFactory's `council_seat_signing.py` and Hermes spec 015's golden vectors. The neutral job envelope (`contracts/hermes-runtime/`) declares no convening block.
- **Existing provider constructions.**
  - `xfc-jcs-sha256-1` is the JSON value digest (`contracts/signed-execution-chain/digest-construction.schema.yaml`, implemented in `scripts/signed_execution_chain/canonical.py`). It refuses non-integer numbers, integers outside ±(2^53 − 1) and unpaired surrogates.
  - Raw-byte SHA-256 is used for files: the release inventory and manifest rows.
  - The key fingerprint is `sha256:` + hex of the raw 32-byte Ed25519 public key (openXwallet `fingerprint_of_public_key`).
  - `scripts/signed_execution_chain/ed25519.py` verifies signatures with the standard library alone.
- **049's state.** The producer has realized only producer-internal, dormant structures, and invented no provider shape. T001 stops all provider-facing wiring until this family is published and pinned: T010, T012, T015b, T020, T023's policy source, T027 and T030.
  - The producer's current internal names are listed against the shared vocabulary in [data-model.md](data-model.md#refusal-vocabulary).
  - Its identifier bound is `^[A-Za-z0-9][A-Za-z0-9._:/@+=-]{0,255}\Z`.
  - Its predicate registry holds two entries: `changed_paths_intersect` over `pr_facts`, and `rule_touches_security_posture` over `rule_facts`.
  - Its roster order is the standing seats first, then each held condition's seat, appended if absent.
  - Its seat entry carries floating-point `costUSD` values, so its internal entry digest does not use a float-refusing canonical form.

---

## R1 — Family layout and corpus placement

**Decision.** The schemas, two closed registries and a template live at `contracts/council-convening/`. The conformance corpus lives at `contracts/council-convening/conformance/`: one `index.json` and vectors under `conformance/vectors/<area>/`. The provider reference implementation lives at `scripts/council_convening/`, behind a thin `scripts/validate-council-convening.py`. Tests live at `tests/council_convening/`.

**Rationale.**

- The governing change's `code_surface` names `contracts/council-convening`.
- The corpus is a cross-implementation artifact whose expectations live in an index. That follows the indexed-fixture precedent `contracts/hermes-runtime/fixtures/index.yaml`: case id, class, requirement ids, inputs, `evaluation_time` and expected outcome.
- JSON vectors cannot carry the `# expected_failure:` header convention that `examples/negative/*.yaml` families use, so the index is where expectations go.
- The package-plus-thin-CLI layout follows `scripts/validate-contract-release.py` over `scripts/hermes_runtime_validation/`.
- Trace: FR-010; D1 ("shared specifications and vectors"); 049 T003 (pin corpus references); 025 FR-001–FR-003.

**Alternatives.**

- `contracts/council-convening/examples/` plus `examples/negative/` with header comments: a teaching corpus, not a two-implementation one. Rejected.
- A separate corpus repository pinned by commit, like openXwallet: an extra publication act and pin for no gain, because the provider owns both shape and corpus (proposal). Rejected.

## R2 — Corpus encoding: JSON vectors and a JSON index

**Decision.** Every corpus file is JSON (RFC 8259), UTF-8, LF-terminated, a closed object, and carries `schema_version` and `kind`. The schemas stay house YAML.

**Rationale.**

- The corpus is read by two independent implementations in other repositories. Its values must have exactly one parse.
- JSON's data model is the `xfc-jcs-sha256-1` input domain.
- YAML resolver differences change values silently. PyYAML turns an unquoted ISO timestamp into a `datetime` and reads `on`/`yes` as booleans, and YAML 1.1 and 1.2 disagree on octal.
- `contracts/factory-mcp/` already ships JSON examples.
- Trace: FR-010, SC-001 (identical outcomes in separate implementations).

**Alternatives.** YAML vectors with strict quoting rules: the parse would depend on an author's discipline. Rejected.

## R3 — Digest construction, subjects and signed bytes

**Decision.** The family reuses `xfc-jcs-sha256-1` by `$ref` and adds exactly two subjects to its closed `digest_subject` enumeration and to the `canonical.SUBJECTS` mirror:

- `council_convening`: the commission record, the value the snapshot and every assignment bind as `convening_digest`;
- `council_seat_return_payload`: the seat's return payload, bound by the return context as `return_digest`.

Every signature in this family covers the UTF-8 bytes of `canonical.serialize(context)`, where `context` is a closed object carrying a `signing_context` member, a versioned string ([R10](#r10--protocol-and-signing-context-identifiers)). No prefix framing is used. No other digest or framing is introduced.

**Rationale.**

- D1 says "Reuse the provider's existing digest construction by reference; do not mint another canonicalization".
- D3 says the return uses "the existing digest construction and a distinct versioned signing context".
- The construction file's own rule is that "a later tranche adds SUBJECTS ... never a second CONSTRUCTION".
- Signing the JCS bytes of the signed block is the house form: `validate-clearing-dispatch.py` and `validate-signed-execution-chain.py` both verify over `canonical.serialize(...)`.
- A replacement message always begins with `{`. A legacy v1 message begins with its protocol string followed by a newline. The two byte strings can never coincide, so neither protocol's signature verifies as the other's (FR-008; D3 "cross-protocol replay").
- Hermes H2 needs "full verified provenance and its provider-defined digest". 049 T020 needs the signing contexts.

**Alternatives.**

- Keep the legacy `protocol + "\n" + json.dumps(...)` framing under new strings: that is a second canonicalization, because `json.dumps` with `sort_keys` is not JCS (key order and number form differ). Rejected.
- Sign a digest of the context instead of its bytes: it adds a subject nothing else consumes (precedent: 028 research R4, "an admitted subject with no consumer is a widening nothing exercises"). Rejected.
- Add a subject for the snapshot: the snapshot is bound through `convening_digest` plus its consumer-issued identifiers, and no shape needs a digest over the snapshot itself. Rejected until a consumer needs one.

## R4 — The provider reference implementation is a third, independent implementation

**Decision.** `scripts/council_convening/` is written from this family's own specification ([data-model.md](data-model.md) and [contracts/conformance-corpus.md](contracts/conformance-corpus.md)). It imports nothing from codexFactory or Hermes. The canonical validator uses it to adjudicate every vector on every run. The producer and the consumer each run the same corpus through their own implementations and adapters.

**Rationale.**

- The handoff says "never copy the producer evaluator into the provider and call that independent validation".
- D1 says "independent implementations are required".
- With a provider adjudicator, every vector's expected outcome is reproduced by code before any consumer relies on it. A vector cannot carry an expectation that no implementation produces.
- Trace: FR-010, SC-001.

**Alternatives.** An index of expected outcomes with no provider-side execution: an unexecuted expectation is an assertion (Principle V). Rejected.

## R5 — The closed predicate registry and input contracts

**Decision.** `predicate.registry.yaml` is a closed instance of `predicate-registry.schema.yaml`. Its first two entries keep the identifiers the governed rule files already declare.

| Predicate | Input contract | Parameters | Facts read | Decision |
|---|---|---|---|---|
| `changed_paths_intersect` | `pr_facts` | `protected_paths`: a non-empty list of patterns | `changed_paths`, `changed_files_total`, `changed_paths_entry_count` | Holds when any changed path matches any pattern. **Unevaluable** when `changed_paths` is absent, or when the entry count differs from the declared total. |
| `rule_touches_security_posture` | `rule_facts` | `security_surfaces`: a non-empty list of patterns | `rule_touched_paths` | Holds when any touched path matches any surface. **Unevaluable** when `rule_touched_paths` is absent. |

The pattern grammar is exact and total. A pattern is either an exact repository-relative path or a `dir/**` tree. Rooted, dot-relative or trailing-slash patterns are refused as `predicate_parameters_malformed`, and so is any `*`, `?` or `[` outside the trailing `/**`. An exact pattern for which an observed path lies inside `pattern/` is refused as `predicate_parameters_malformed`: it was a directory declared as a file. Each implementation must reproduce every one of these by vector.

Both input contracts are closed. `pr_facts` is the three facts above. `rule_facts` is `rule_touched_paths`. Fact values are strings, integers within the construction's bound, booleans, or lists of strings, never non-integer numbers. Adding a predicate kind or a fact is a governed contract change.

**Rationale.**

- D1 says "The closed predicate registry and input type contracts are shared specifications and vectors". The Goals say "Domain predicates remain domain-owned": the domain owns which seats a rule conditions on which parameters, while the mechanism is neutral.
- Both kinds are mechanical intersections with no domain vocabulary (Principle I).
- Keeping the identifiers the rule files already declare avoids a renaming layer between a governed rule and the record citing it, where drift could hide.
- The completeness, unevaluable and bare-directory rules are what keep "unevaluable" from silently reading as "false" (spec delta, requirement 1: "an unevaluable condition MUST refuse commissioning rather than become false").
- Trace: FR-002, FR-003; 049 T003 and T010; 025 FR-002 and FR-003.

**Alternatives.**

- Neutral renames such as `rule_paths_intersect`: adds a mapping between a rule file's declared predicate and the record. Rejected.
- Open-ended predicate strings: the "unenforced-key hazard" the producer's closed registry exists to prevent. Rejected.
- Copying the producer's glob code: forbidden by R4. The semantics are specified here, and the producer's code is not the source.

## R6 — Roster composition and the neutral rule projection

**Decision.** The provenance carries the governed rule's **neutral projection** for the matched class:

- `standing_seats`, ordered;
- `conditions`, ordered: `seat`, `predicate`, `parameters`, `input_contract`, `held`.

The roster rule is: `required_seats` equals `standing_seats` in order, followed by the seat of each condition with `held: true` in `conditions` order, each appended only if not already present. The result must be non-empty and unique. A condition whose `held` is true and that names no seat refuses (`condition_seat_unbound`).

Each side derives the projection from the domain's rule file through its own adapter. 049 uses its existing loader. 025 uses H1's "allowlisted governed-repository adapter". The corpus supplies projections through a rule oracle ([R8](#r8--environment-oracles-make-authority-facts-and-heads-testable)).

**Rationale.**

- D1 requires "ordered, nonempty, unique" membership with the "predicate identifier and typed parameters" in provenance, and refuses "reordered results".
- The order rule is exactly 049's `resolve_required_seats`, so the producer conforms without changing its evaluator.
- Carrying `held: false` conditions keeps every evaluated condition reproducible. It also lets the producer derive its unseated-conjunction metadata (T015a) from the frozen record alone.
- Domain rule shapes, such as flat versus layered rosters, stay domain-owned (Principle I).
- Trace: FR-001–FR-003, SC-001; 049 T010, T015b; 025 FR-002.

**Residual risk, recorded.** The two adapters could map the same domain file differently, and the neutral corpus cannot test a domain file. Phase 2 states this in the family README. 049's own tests over real council documents and the matched rehearsal (049 T032; SC-004) are where it is caught.

**Alternatives.**

- Provider-specified domain rule shapes: domain vocabulary in the neutral layer. Rejected.
- Carry only `required_seats` plus a rule digest: an "opaque Boolean conclusion" and a "digest-only rule reference", both refused by D1. Rejected.

## R7 — Rule authority and revision currency (OPEN-3)

**Decision (part decided).** Authority is not availability. The consumer must establish that the cited `governed_rule` is an admitted governed rule of an allowlisted governed repository for that council. The record's governed-rule reference is checked as follows:

| Condition | Refusal |
|---|---|
| The revision is not a full lowercase 40-hex commit id | `mutable_rule_reference` |
| The path is not normalized and relative | `rule_path_malformed` |
| The object is absent | `rule_unavailable` |
| The object exists but is not governed | `rule_unauthorized` |
| `blob_sha256` does not match the bytes | `rule_digest_mismatch` |

**OPEN-3, Brett Heap's to decide.** D1 and D4 say "admitted governed rule" and "at the governed ref and immutable code revision", but not how current a revision must be at admission. Main can move between the producer's commission and the consumer's admission. The options:

- **(a) Any revision on the governed branch's first-parent history.** A superseded rule could seat an outdated roster.
- **(b) Exactly the governed tip at admission.** Spurious refusals whenever the branch advances, even for unrelated files.
- **(c) First-parent history plus an unchanged rule file (recommended).** Require the revision to be on the governed first-parent history, and the rule file's blob at that revision to equal its blob at the governed tip when admission runs. Refuse `rule_superseded` otherwise. Where the rule repository is the producer repository, also require the producer's verified `job_workflow_sha` claim to equal the cited rule revision (R13), so "the code that produced the record" and "the rule that governed it" are one commit.

**Why (c).**

- It never admits a roster under a rule that has since changed.
- It never refuses on unrelated movement of main.
- It closes the self-selection class the producer's adversarial review found (049 T008, F1: a candidate choosing the rule that decides its own membership).

**Consumer impact of (c).** 049 T010/T023 would check out its trusted tooling at exactly the verified workflow revision. 049 already requires the governed revision to be the run's own checkout HEAD (W0, `governed_revision_not_head`). Both oracles model whichever option is chosen, and the corpus vectors for `rule_superseded` and `workflow_revision_ungoverned` are authored in Phases 2 and 5 under the ruling.

**Trace.** FR-003; D1, D2, D4; 049 T010, T023; 025 FR-002.

## R8 — Environment oracles make authority, facts and heads testable

**Decision.** A vector carries an `environment` block. Each implementation's corpus adapter must inject it into its own lookups, never reading live systems during a corpus run:

| Oracle | Answers |
|---|---|
| `governed` | For each `(repository, path, revision)`: whether it is available, whether it is governed, its blob digest, and the tip blob digest under the OPEN-3 option |
| `rules` | The neutral projection of the rule at `(repository, path, revision)` for each declared class |
| `facts` | The authoritative facts for each fact source |
| `live_heads` | The head of each `(repository, pull_number)`, or `unavailable` |
| `issued` | The issued challenges, registered keys, consumed challenges and accepted returns, as of `evaluation_time` |
| `identity` | The verified claims a broker reported, and its capability |

**Rationale.**

- Race, authority and staleness refusals can only be shared vectors if their inputs are data.
- The hermes-runtime fixtures already fix an `evaluation_time` per case.
- 049's tests already inject `fetch`, `live_head` and `governed_root`.
- Trace: FR-004, FR-010, SC-001; spec edge cases (head drift before and after the POST, changing totals, an immutable rule that is accessible but unauthorized).

**Alternatives.** Live fixtures against real repositories: not reproducible, and network-dependent. Rejected.

## R9 — Fact authenticity, unused facts and secrets

**Decision.** Facts are checked as follows:

| Check | Refusal |
|---|---|
| `consumed_facts` differs from the authoritative facts projected onto exactly the keys the conditions read | `consumed_facts_mismatch` |
| A fact key that no condition reads | `facts_unused` |
| A fact source that is not the candidate (for `pr_facts`) or not a governed path at an immutable revision (for `rule_facts`) | `fact_source_mismatch` |

The **secret detector set** is the provider's existing `SECRET_PATTERNS` (`scripts/validate-domain-factory.py`), loaded by `importlib`, never copied. It is applied to every string in `consumed_facts`, `parameters` and `packet_refs`; a match refuses as `secret_bearing_fact`. An implementation may detect more, but it must refuse every corpus secret vector and accept every positive one.

Secret-shaped corpus values are stored as a `{"$parts": [...]}` join sentinel. Every adapter concatenates it before any other step, so no corpus file matches a detector when the provider's own `scan_secrets` sweeps `.json` files.

**Rationale.**

- D1 refuses "unused inputs and secrets" and requires "normalized facts actually consumed".
- A second detector list would be a second vocabulary.
- 049's CI was failed once by its own literal secret-shaped vectors and fixed by building them from parts (049 evidence, the `f0064e95` CI round).
- Trace: FR-002, FR-003; 049 T009/T010; 025 FR-003.

## R10 — Protocol and signing-context identifiers

**Decision.** The planned values below become normative when the Phase 1 registry lands.

| Identifier | Value | Status |
|---|---|---|
| Replacement protocol | `xfc-resolved-council-1` | `available` (dormant) at the minor; `admission_eligible` at the major |
| Registration context | `xfc-resolved-council-1/seat-key-registration` | the replacement's |
| Return context | `xfc-resolved-council-1/seat-return` | the replacement's |
| Legacy protocol entry | `xfactory-council-seat-return/v1` | `deprecated` at the minor; `historical_only` at the major |
| Legacy key-authorization context | `xfactory-council-seat-key-authorization/v1` | recognized for classification and refusal only |

The legacy entry is **identification only**. Its recognition criteria are:

- a convening block without `protocol` and `required_seats`;
- a context string in the legacy set;
- a registration carrying `root_key_fingerprint` or a root authorization.

The provider specifies no legacy schema. Legacy verification stays the legacy verifier's (Hermes 015 and its golden vectors).

**Rationale.**

- D1 requires an "explicit protocol identifier".
- D3 requires "a distinct versioned signing context to prevent cross-protocol replay".
- D5 requires a deprecation that warns before removal, and historical records kept under their recorded protocol. The validator must recognize the old shape to warn on it and later refuse it; it need not own that shape.
- The `xfc-…-1` form follows `xfc-jcs-sha256-1`.
- Trace: FR-001, FR-008, FR-011; 049 T020, T026→T030, T027; 025 FR-010, FR-011.

**Alternatives.**

- `…/v2` under the legacy strings: reads as a revision of the root-authorized protocol, which it is not. Rejected.
- Codify the legacy shapes as a provider schema: the provider would take ownership of a protocol it never published, only to remove it. Rejected.

## R11 — Return payload admissibility (a consumer-impact consequence of D1)

**Decision.** `return_digest` is the `xfc-jcs-sha256-1` digest, subject `council_seat_return_payload`, of the seat's return payload. The neutral contract constrains the payload only to be admissible under the construction: no non-integer number, no integer outside ±(2^53 − 1), no unpaired surrogate. A payload that is not admissible is refused as `value_not_canonicalizable`. The payload's content stays domain- and consumer-agreed; verdict semantics are Hermes's existing ones.

**Consumer impact.** 049's seat entry carries `model_usage` with floating-point `costUSD` values (049 evidence: the reason it avoids a float-refusing form). To sign under this contract, 049 T020 must carry such values as decimal strings or integer minor units inside the payload. This is forced by D1 ("do not mint another canonicalization"); it is not a new policy choice. It is recorded here so T020 is not surprised.

**Alternatives.**

- A raw-bytes digest over the serialized payload: it makes the digest depend on one serializer's bytes, which is a second construction in effect. Rejected.
- Exempting floats: reintroduces the cross-implementation number disagreement the construction refuses on purpose. Rejected.

## R12 — Lifetime ceilings (OPEN-1)

**Decision (part decided).** Assignments and challenges carry their limits:

- An assignment carries `not_before` and `expires_at`.
- A challenge carries `issued_at` and `expires_at`.
- Both are ISO 8601 UTC instants with seconds precision and a `Z` suffix.
- Expiry is refused at and after the instant (`assignment_expired`, `challenge_expired`).
- A lifetime of zero or less, or above the contract ceiling, is refused as malformed.
- The consumer configures any tighter actual value.

**OPEN-1, Brett Heap's to decide: the two ceilings.** D3 says "short lifetime" and FR-007 says "bounded one-use challenges", with no numbers.

- **Recommendation: a challenge ceiling of 600 seconds and an assignment ceiling of 6 hours.**
- A challenge is consumed within seconds of issue, at the seat job's first step.
- An assignment must outlive runner queueing plus the seat job's 30-minute timeout (049 W1).
- A convening whose assignments expire fails and may be convened again, because once-per-pin counts only convenings that did not fail.
- 049's internal pre-check currently bounds challenges at 3600 seconds. That is a producer-side pre-check, not issuance, so it needs no change under either ceiling.
- The vectors at each ceiling are authored at the ruled value.

**Trace.** FR-007; D3; 049 T019/T020; 025 FR-009.

## R13 — Producer workflow binding and its placement (OPEN-2)

**Decision (part decided).** `producer-binding.schema.yaml` is closed and holds the following. The issuer:

- `issuer`, the constant `https://token.actions.githubusercontent.com`, for the `github_oidc` principal kind.

The repository identity:

- `producer_repository`, which must be the `current` spelling of a completed transfer in `contracts/policies/repository-identity.yaml`, or a repository that file does not list as `former`. It is read through the existing reader. Case variants, which the file's `owner_case` names as non-canonical, are refused as `repository_identity_former`.
- `repository_id`, the immutable numeric repository identity.

The claims:

- `audience`, a literal and never a pattern.
- `subject_template`, the actual verified OIDC `sub` template.
- `permitted_workflows`, a list of `{operation, job_workflow_ref, workflow_revision_rule}`.

They are subject to these rules:

| Rule | Refusal |
|---|---|
| `job_workflow_ref` and `sub` are different fields | A `sub` that is a workflow ref is `subject_workflow_conflation` |
| No wildcard in any member | `binding_wildcard` |
| No claim taken from a decoded, unverified assertion | `claims_unverified` |
| A broker whose capability is not verified | Parks activation: `broker_capability_insufficient` |

The template `producer-binding.template.yaml` carries an `instantiation_stub` marker and no live values.

**OPEN-2, Brett Heap's to decide: where the concrete instance lives.**

- **(a) Recommended:** in the consumer's governed runtime configuration, written by the operator at the provisioning act (049 T031; 025 H3 "runtime-held configuration"; D4 "Identity provisioning is an operator act"). It is validated with `validate-council-convening.py check` at the consumer's pin. The provider stays the only source of repository spelling (`repository-identity.yaml`).
- **(b)** Provider-published under `contracts/council-convening/`. That makes the neutral repository a holder of one domain's authority configuration, and every audience or subject-template change a provider contract cut.

**Trace.** FR-009; D3, D4; 049 T023, T024, T031; 025 FR-008.

## R14 — Protocol registry, selection, deprecation and historical classification

**Decision.** The protocol registry is closed. A `protocol_selection` record is each side's governed configuration shape: `{protocol, provider_commit, provider_bundle, corpus_index_sha256}`. Two sides match only when all four are equal; otherwise the refusal is `pair_mismatched`.

The rules for selection and history:

- A refusal under the selected protocol never selects another protocol (`rejected_without_fallback`).
- At the minor, a record classified as legacy and presented to active validation is accepted with the warning `legacy_protocol_deprecated`, which `--strict` promotes to an error.
- At the major, the same record is refused as `legacy_protocol_refused`.
- In `--historical` mode a record is classified by its recorded protocol and never reinterpreted. Legacy records are routed to the legacy verifier, which is outside this family. Replacement records stay verifiable under the replacement rules at every later release.

`activation_evidence` records the matched configurations, provider and successor revisions, broker capability evidence, in-flight disposition, rehearsal result, rollback disposition, and the dated owner word. The validator refuses an activation record missing any of these (`activation_evidence_incomplete`).

**Rationale.**

- D5 requires that "The active binding selects exactly one protocol ... never guesses from payload shape or falls back".
- D5 also requires that "Historical records retain their original protocol".
- H4 reads "one declared protocol and exact provider compatibility pin from governed configuration".
- § Change Classes, *Deprecating (minor)*: "the conformance validator emits warnings but still accepts it".
- Trace: FR-011, FR-012, SC-004; 049 T026–T030, T032; 025 FR-011, FR-012.

**Alternatives.** Selector symbols only, as 049 T026 does internally: those cannot show that a pair matches on the provider pin and corpus. Rejected for the shared shape; the producer maps its symbols at T030.

## R15 — Release-surface membership (OPEN-4)

**Decision: OPEN-4, Brett Heap's to decide.** The question is whether `contracts/council-convening/`, its validator, package and tests join the release digest inventory.

- **(a) Recommended: join.** Add a floor-gated block in `scripts/hermes_runtime_validation/release.py`, `COUNCIL_CONVENING_RELEASE_FLOOR`, set to the version allocated at the Phase 7 cut. This follows the clearing precedent: openxFactory #722 treated a family's absence from the inventory as a defect, and Brett Heap ruled the floor form in #745. Published inventories keep verifying, and the corpus's per-file digests travel in the inventory that consumers already verify.
- **(b) Do not join.** Identity travels by manifest-row SHA-256 only, as 028 research R6 did for a new family and `signed-execution-chain` still does.

Either way, the corpus digest consumers pin is the manifest row's SHA-256 of `conformance/index.json`, whose rows pin every vector's bytes ([R16](#r16--the-corpus-digest)).

**Trace.** FR-010, FR-012; D5 ("regenerates manifest/changelog/inventory from the actual candidate"); 049 T003, T030.

## R16 — The corpus digest

**Decision.** `conformance/index.json` lists every vector with its path and `sha256:` over its raw bytes, plus the counts per area and outcome. The validator enforces closure in both directions:

- every file under `conformance/` is indexed, except the index itself;
- every row exists;
- every digest matches;
- rows are in bytewise UTF-8 path order;
- every closed refusal code is probed;
- every FR-001–FR-012 and SC-001–SC-003 is cited.

The **corpus digest** is the manifest row `sha256` of `conformance/index.json`, registered at the Phase 7 cut. A consumer pins `{openxFactory commit, index sha256}`, and the index transitively pins every vector.

**Rationale.**

- Per-file hashes are "plain algorithm-tagged SHA-256 over the file's BYTES" (the clearing family's ratified rule).
- One digest gives consumers a single value to pin and compare during the matched rehearsal.
- Trace: FR-010; Risks ("exact corpus digest/pin"); 049 T003, T013; 025 FR-001.

**Alternatives.** An `xfc-jcs-sha256-1` subject over the index's parsed value: a file is bytes, and the existing rule for files is raw SHA-256. Rejected.

## R17 — CI gate and the pytest-suite pin

**Decision.** Add `.github/workflows/council-convening-gate.yml`.

- Its job id is `council-convening-gate`, with no `name:` key.
- It ends with a positive assertion step that greps for the validator's proof-of-work notes.
- It reports and does not gate until the owner makes it required.

**Rationale.**

- This is the house gate form (`clearing-dispatch-gate.yml`): a display name silently de-advises a required check, and "a green check that walked nothing is a vacuous pass".
- The tests need no submodule and no network, and `cryptography` comes from the lock `pytest-suite` already installs. So `EXPECT_SKIPPED` does not move, and the `MIN_*` floors only rise.
- Trace: Principle V; FR-010.

## R18 — Fixture keys and reproducible signatures

**Decision.** `scripts/council_convening/generate.py` derives each fixture's Ed25519 seed from a **labelled** SHA-256 of a fixed, public phrase naming it a council-convening corpus test key. It signs with `cryptography`, and writes only public keys, signatures and signed-bytes known answers into vectors.

- No seed or private key is written to any file.
- Ed25519 (RFC 8032) is deterministic, so regeneration is byte-identical, and a test asserts that the generator reproduces the committed corpus exactly.
- Verification at validation time uses the stdlib `ed25519.verify`.

**Rationale.**

- Signatures in signing vectors must really verify.
- This applies the 028 research R7 practice: public halves and signatures only, keys visibly test-only, with nothing private committed.
- Unlike an ephemeral key, a labelled derivation keeps the corpus digest stable across regenerations.
- Trace: FR-008, FR-010, SC-003.

**Alternatives.** Fixed literal seeds in a vector file, the v1 golden-vector form: key-shaped secrets in governed bytes. Rejected.

## R19 — Release sequencing and the two cuts

**Decision.** The two releases are sequenced as follows.

**Phase 7 — the minor.** One minor that is both additive and deprecating:

- the family appears with the replacement `available`;
- the legacy protocol is `deprecated`, with its removal stated as "the next major" and named concretely at the cut;
- the cut adds a `contracts/CHANGELOG.md` entry, a `docs/contract-versioning-policy.md` § *Deprecations Currently In Force* entry written from the refusal list, the manifest rows, the release inventory, and the `contracts/README.md` and README index rows;
- the cut runs the supported-domain regression denominator.

**Phase 8 — the major.** Cut only after all four of:

- (a) the minor's tag is published and verified;
- (b) at least one full minor has served;
- (c) both successors' dormant implementations are verified against the published minor (D5 Migration Plan);
- (d) the owner's release act.

The major flips legacy selection to refusal, writes the CHANGELOG migration note and § *Deprecations Executed*, and re-baselines the denominator against the actual union. It must also process every other § *Deprecations Currently In Force* entry that targets the version it becomes. Two entries now target `contract-v5.0`: the flat `hermes` keys and the credential `consumer:` block. Each is restated again under its own pre-authorized text unless its acts are ready. Phase 8 does not decide those acts.

Both cuts claim the contract-cut shared substrate on openxFactory's pinned "Shared substrates — claims" issue (lane protocol Amendment 1, rule 7). Each allocates the next available version from the manifest at that moment, rebasing first (Bundle Realization Order step 1). Each tag is the owner's act (change task 3.2; precedent: `contract-v4.0` ASK-9a, "the annotated tag is Brett's act").

**Rationale.** § Change Classes, *Breaking (major)*: "at least one full minor release where the old shape produced deprecation warnings". The proposal: "allocate neither version here". Trace: FR-011, FR-012; 049 T030; 025 FR-011.

**Alternatives.** A separate additive minor followed by a deprecating minor: one more owner tag act, and no difference in the warning window. Rejected.

## R20 — What this feature does not do

The following are out of scope, and the family README states it:

- producer or consumer implementation;
- HTTP routes, envelopes, status codes and error bodies (025);
- persistence and transactions (025);
- the domain rule-file adapters (each side);
- broker provisioning and credentials;
- deployment;
- successor pin advances;
- activation;
- any spec delta;
- the archive.

Local tests are never reported as publication, deployment or activation (spec User Story 3, scenario 4).
