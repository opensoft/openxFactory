# Data Model: Neutral resolved council protocol

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) · **Research**: [research.md](research.md) · **Analysis**: [analysis.md](analysis.md)

These are the shapes of the planned `contracts/council-convening/` family. A shape becomes normative only when two things happen:

1. its schema lands in the phase named for it;
2. a release publishes it (Phase 7 for the replacement, Phase 8 for the removal of legacy acceptance).

Until both happen, the shapes here are the plan, not a contract. Consumers read the landed schema, never this file ([contracts/provider-interface.md](contracts/provider-interface.md)).

Brett Heap's rulings of 2026-10-08 are encoded here: lifetime ceilings (E5, E6), the binding's home (E10), revision currency and its three follow-ups (E2, E7, E10), release membership (Phase 7), and the predicate identifiers (E3). The rulings are listed in [spec.md § Clarifications](spec.md#clarifications) and [research.md](research.md).

Four conventions apply throughout:

- Every record is a closed object, with `additionalProperties: false` at every depth, with one exception: E8's `payload`, whose members are the domain's and the consumer's. `parameters` is closed per predicate and `consumed_facts` per input contract (E3). Every record carries `schema_version: 1` and a `kind`.
- **R** means required and **O** optional.
- **One failing check names one code.** Where a named semantic refusal exists for a condition (an empty or duplicated roster, a reordered list, inequality with an oracle), the schema does not also check that condition. So the schema types `governed.revision` as a string (its grammar is `mutable_rule_reference`, E2 step 5), the binding's `issuer` as a string (`issuer_mismatch`), `changed_files_total` as a non-negative integer (above 3000 is `condition_unevaluable`), the snapshot's `assignments` as an array of objects (each is checked at E4 step 3), `conditions[].predicate` as a string (`predicate_unknown`, E2 step 8), the binding's `subject_template` and each `job_workflow_ref` as strings (E10 steps 5, 6 and 13), each `governed.sources[].path` as a string (its grammar is `rule_path_malformed`, E2 step 5), and E12's act-specific members, including `new_records_retained` and `new_records_protocol`, as optional (E12 steps 2 and 5). Each boundary has a normative evaluation order, and the first failing check names the outcome ([R21](research.md#r21--normative-evaluation-order)).
- **Every boundary over a protocol-carrying record begins with classification** (E1). The protocol-carrying kinds are E2 and E4–E8. A record of one of them is judged under replacement rules only after it has classified as a replacement record under a replacement selection. The registries (E1, E3), the binding (E10), the selection (E11) and activation evidence (E12) are judged by their `kind` and never classified.

## Shared definitions (`shared-definitions.schema.yaml`, Phase 1)

| Definition | Grammar | Notes |
|---|---|---|
| `opaque_id` | `^[A-Za-z0-9][A-Za-z0-9._:/@+=-]{0,255}$`, matched **whole** | Equals 049's `_OPAQUE_ID_RE` / `_ASSIGNMENT_ID_RE`. The validator matches the whole string (`\Z`), so a trailing newline is refused; a vector probes it. |
| `council_id`, `seat_id`, `matched_class` | `opaque_id` | No domain value appears in any schema. |
| `protocol_id` | 1 to 128 characters, no control character | Membership in the registry is the classification check (E1), not a grammar. |
| `repository` | `^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`, whole | Where an entity says so, the spelling is checked against `repository-identity.yaml`. |
| `full_sha` | `^[0-9a-f]{40}$`, whole | |
| `pull_number` | integer from 1 to 2147483647, never a boolean | Equals 049's `MAX_PULL_NUMBER`. |
| `relative_path` | A non-empty string of at most 4096 UTF-8 bytes. No leading `/`, no character below U+0020 and no U+007F, and no empty, `.` or `..` segment. | These are 049's `normalize_changed_path` rules exactly, so `\` and C1 characters are legal. The 4096-byte bound (Linux `PATH_MAX`) is the one tightening. 049's input sizing already takes 4096 bytes as its extreme path (the `MAX_INPUT_BYTES` comment in its `resolved_council_commission.py`), but 049 does not refuse a longer path today. That refusal is a recorded producer impact ([provider-interface](contracts/provider-interface.md#consumer-impacts-recorded-by-this-plan)), and a vector probes it. |
| `head_ref` | 1 to 255 characters, no character below U+0020 and no U+007F | The candidate's head branch name, read for class selection only. |
| `utc_instant` | `YYYY-MM-DDTHH:MM:SSZ`, calendar-valid | Expiry is refused at the instant and after it. |
| `raw_sha256` | `^sha256:[0-9a-f]{64}$` | SHA-256 over a file's raw bytes. |
| `digest` | `$ref` to `signed-execution-chain/digest-construction.schema.yaml#/$defs/digest` | `{construction: xfc-jcs-sha256-1, subject, value}`. Each use fixes its `subject` with a `const`. |
| `key_fingerprint` | `^sha256:[0-9a-f]{64}$` | `sha256:` + the lowercase hex SHA-256 of the raw 32-byte public key: the estate spelling T047 names, as openXwallet `fingerprint_of_public_key` (`scripts/validate-openxwallet.py:536-541` at openXwallet `f3eb929b`, the commit openxFactory pins) and codexFactory `key_fingerprint` (`.github/workflows/scripts/council_seat_signing.py:199-205`, through its `sha256_digest` at `:168-170`, at codexFactory `48d0560e`) compute it. *Corrected 2026-10-09 on Brett Heap's ruling of 2026-10-09T02:36:50Z, "Estate spelling (Recommended)": this row read "`sha256:` + hex of the raw 32-byte public key", the raw key's own hex, which is not the estate spelling and which Phase 1's fixture keys first computed. The pattern is unchanged; it accepts both spellings, so only a recomputation from `public_key` (E7 `fingerprint_mismatch`) tells them apart.* |
| `public_key`, `nonce` | Unpadded base64url of exactly 32 bytes | |
| `signature` | Unpadded base64url of exactly 64 bytes | |
| `decimal_string` | `^-?(0\|[1-9][0-9]*)(\.[0-9]*[1-9])?$`, whole, with `-0` refused | The one representation of a non-integer quantity inside a signed payload: no exponent, no `+`, and no trailing fractional zero ([R11](research.md#r11--return-payload-admissibility-and-decimal-quantities)). |
| `principal_kind` | `github_oidc_job` \| `governed_broker_job` | One closed enumeration, used by E5 and E10. |
| `candidate` | `{repository R, pull_number R, head_sha R(full_sha), subject_path O(relative_path)}` | D1's "candidate repository, positive pull number and lowercase full head". `subject_path` names a path-shaped subject at `head_sha`, such as the rule packet a gate-rules council judges ([R6](research.md#r6--roster-composition-the-neutral-rule-projection-and-path-shaped-subjects)). |
| `refusal_code` | Closed enumeration, see [Refusal vocabulary](#refusal-vocabulary) | snake_case contract values. It grows only by an edit in the task that authors the phase's schemas. |
| `finding_code` | Closed enumeration: `legacy_protocol_routed` (Phase 1), `legacy_protocol_deprecated` (Phase 6) | Kept apart from refusals, with its own coverage rule. A route carries an ordered list of findings. |

Every value must also be admissible under `xfc-jcs-sha256-1`:

- no non-integer number;
- no integer outside ±(2^53 − 1);
- no unpaired surrogate.

A value that is not admissible is refused as `value_not_canonicalizable` before any digest is taken. A value probed alone against a grammar here (boundary `definition`) is refused as `value_malformed`. The same failure inside a record is that record's malformed code.

*Added 2026-10-09 (Phase 1 review, reading 3): at boundary `definition` the grammar is checked first and admissibility second. A value that fails both is `value_malformed`, and a value is `value_not_canonicalizable` only where its grammar admits it, as a lone surrogate inside a `head_ref` or a `candidate` member is admitted.*

## E1. Protocol registry and classification (`protocol-registry.schema.yaml` + `protocol.registry.yaml`, Phase 1)

Kind: `xfactory_council_protocol_registry`. A closed instance with exactly two entries. Adding an entry is a governed contract change. The status enumeration in the schema already holds every status either entry will ever take, so the releases change instance data only ([R19](research.md#r19--release-sequencing-and-the-two-cuts)).

| Member | Replacement entry | Legacy entry |
|---|---|---|
| `protocol_id` | `xfc-resolved-council-1` | `xfactory-council-seat-return/v1` |
| `role` | `replacement` | `legacy` |
| `status` | `available` (Phases 1–7), then `admission_eligible` (from Phase 8) | `in_use` (Phases 1–6), `deprecated` (Phase 7), `historical_only` (Phase 8) |
| `signing_contexts` | `xfc-resolved-council-1/seat-key-registration`, `xfc-resolved-council-1/seat-return` | `xfactory-council-seat-return/v1`, `xfactory-council-seat-key-authorization/v1` |
| `recognition` | — | Used only for a record that carries no `protocol` member. Any one of: (a) a `council_convening` block with no `required_seats`; (b) a signing context in the legacy set; (c) a registration carrying `root_key_fingerprint`, `root_signature` or `authorization`. |
| `introduced_in` / `deprecated_in` / `removed_in` | `null` until a cut writes the allocated tag | `null` until a cut writes the allocated tag |

**Classification (Phase 1, boundary `classification`)** applies to a record whose `kind` is one of the protocol-carrying kinds (E2, E4–E8), or that carries no family `kind` at all, in this order:

1. A record whose `protocol` is `xfc-resolved-council-1` is a **replacement** record, whatever else it carries. A replacement record carrying root-authorization members is refused later as `root_authorization_refused` (spec delta, requirement 5). It is never legacy (I3 in [analysis.md](analysis.md)).
2. A record whose `protocol` is the legacy `protocol_id` is a **legacy** record. Any other `protocol` value is `protocol_unknown`.
3. A record with no `protocol` is legacy when a recognition rule matches, and `protocol_unknown` otherwise.

**Effects depend on the side's selected protocol, never on payload shape alone.** D5 says the binding "never guesses from payload shape", and that "Separate versioned endpoints ... do not confer dual-protocol acceptance on the active replacement binding". In production the selected protocol comes from the side's E11 record. In a vector it is `inputs.selected_protocol`: a registry `protocol_id`, or `null` for an offline `check`.

| Selected protocol | Legacy status | A legacy record | A replacement record |
|---|---|---|---|
| the replacement | any | **refuse** `legacy_protocol_refused` | judged under replacement rules |
| the legacy entry | `in_use` | **route** to the legacy verifier, with no verdict from this family | refuse `protocol_not_selected` |
| the legacy entry | `deprecated` (vectors from Phase 6) | **route**, plus the finding `legacy_protocol_deprecated` | refuse `protocol_not_selected` |
| the legacy entry | `historical_only` (vectors from Phase 6) | the selection itself is refused, in either mode: `legacy_protocol_refused` | the selection itself is refused, in either mode: `legacy_protocol_refused` |
| `null` (offline `check`) | any | **route** | judged under the offline replacement rules |
| `--historical` (Phase 6) | any | **route** (classified, never reinterpreted) | judged under replacement rules, at every later release |

"Route" means this family gives no verdict. The validator's `check` exits **3**, which is never a pass. The route carries the findings `[legacy_protocol_routed]`, or `[legacy_protocol_routed, legacy_protocol_deprecated]` while the legacy status is `deprecated`. The legacy verifier (Hermes 015 and its golden vectors) remains the only verifier of legacy bytes. This family never passes a legacy record unverified (C3 in [analysis.md](analysis.md); constitution Principle VII). A vector whose outcome reads a registry status carries a `registry_status` override ([contracts/conformance-corpus.md](contracts/conformance-corpus.md#environment-oracles)).

## E2. Commission record (`council-convening.schema.yaml`, Phase 2)

Kind: `xfactory_council_convening`. The producer submits it, and the consumer verifies it before any write (D1, D2).

| Member | R/O | Shape |
|---|---|---|
| `protocol` | R | `const: xfc-resolved-council-1` |
| `council_id` | R | `council_id` |
| `subject_pin` | R | `full_sha` |
| `packet_refs` | R | 1 to 64 strings, each 1 to 2048 characters with no control character. **This is not the legacy rule:** the replacement accepts no bare string and skips no malformed entry, and the pull number comes from `candidate`, never from `packet_refs`. |
| `mix_id` | O | `opaque_id`: the existing optional deliberation-mix selector, carried for the consumer's existing mix check. |
| `required_seats` | R | An array of at most 64 `seat_id`. Emptiness, duplicates and order are semantic checks. |
| `required_seats_provenance` | R | The object described below. |

`required_seats_provenance`:

| Member | R/O | Shape |
|---|---|---|
| `candidate` | R | `candidate` |
| `governed` | R | `{repository R, revision R(a string; its grammar is checked at step 5), sources R}`. `sources` holds 1 to 64 entries in bytewise path order, unique by path, all at the one `revision`. Each entry is either `{kind: file, path, sha256(raw_sha256)}` or `{kind: listing, path, suffixes, entries}`. A listing names a directory, the file suffixes read from it (for example `[".yaml", ".yml"]`), and the sorted paths of the files directly inside it with those suffixes; each of those files is also a `file` entry. Every governed file and listing the projection was built from is listed ([R7](research.md#r7--governed-sources-rule-authority-and-revision-currency)). For 049 these are the council profile (`hermes/domain/agent-mixes.yaml`), the council document, the rule directory's YAML files and their listing, and the envelope configuration. |
| `class_inputs` | O | `{repository R, head_ref R(head_ref)}`: the candidate facts the class is selected from (E3 `class_selector`). Present exactly when the council is classed in the projection, together with `matched_class`. |
| `matched_class` | O | `matched_class`. Present exactly when `class_inputs` is. An unclassed council, such as 049's gate-rules council, carries neither. |
| `standing_seats` | R | An array of at most 64 `seat_id`. |
| `conditions` | R | 0 to 64 entries of `{seat R(seat_id or null), predicate R, input_contract R, parameters R(object), held R(boolean)}`. |
| `fact_sources` | R | One entry per input contract in use, each `{input_contract, source}`. `source` is one of three: `candidate_pull` (`pr_facts` read from the candidate pull request at `head_sha`); `candidate_subject` (`rule_facts` read from `candidate.subject_path` at `candidate.head_sha`); or `{governed_path: <a path in governed.sources>}` (`rule_facts` read from a governed source at `governed.revision`). |
| `consumed_facts` | R | `{<input_contract>: {<fact>: value}}` |

**Derived value.** `convening_digest` is `xfc-jcs-sha256-1`, subject `council_convening`, over the whole record.

**Normative evaluation order at `commission` (producer) and `admission` (consumer).** The first failing check wins. Steps 1 to 13 are shared. At admission the consumer also runs five admission-only steps, A1 to A5, at the positions shown. A1 and A4 are the `binding` boundary (E10). A2, A3 and A5 place the guards 025 retains (025 FR-004, H1) in the same order Hermes runs them today: council and mix, then once-per-pin, then the pin verification, then the touched-object and base-branch guards (`council_orchestration.py`).

**A2 and A5 are outside the corpus.** They judge consumer-held state that this family does not model: the consumer's materialized council and mix content, its touched-object map, and the base branch's protection. Their refusals are 025's own codes, not this vocabulary, so they are exempt from the total-mapping rule ([provider-interface § What stays the successors'](contracts/provider-interface.md#what-stays-the-successors)). In a corpus run, a consumer's adapter runs them as seams that pass, configured to admit every vector's council and head. The provider reference implementation has no A2 or A5. No vector's `expected` depends on them, and no multi-defect vector pairs one of them with another defect, so every vector stays matchable by both the provider and the consumer. 025 proves them in its own tests (025 FR-004). A3 is inside the corpus: its refusal, `convening_conflict`, is this vocabulary's.

1. **Classification and selection** (E1). `protocol_unknown`, `legacy_protocol_refused`, `protocol_not_selected`, or a route.
2. **Shape.** `convening_malformed`, which also covers a record carrying only one of `class_inputs` and `matched_class`; a listing entry that is not also a `file` source; sources out of bytewise path order or repeated by path; a listing whose `entries` are unsorted; and a repeated `fact_sources` contract. Then `value_not_canonicalizable`.
   - **A1. Binding, admission only.** E10 steps 1 to 13 on the commission job's verified claims. Step 14 waits for step 5 (A4).
   - **A2. 025's retained council and mix guard, admission only.** The council is in the consumer's materialized council content, the subject pin is present, and a `mix_id`, when present, is in the consumer's mix content. Refused under 025's existing codes (`UnknownCouncilError`, `SubjectPinMissingError`, `UnknownMixError` and their kin), which are the consumer's and not this vocabulary.
   - **A3. Retry identity and once-per-pin, admission only** (E4). The convening key is `(protocol, council_id, subject_pin)`: 025's once-per-pin key, the council and the pin, with the protocol added. A consumer may scope it further by its own tenancy layer (Hermes's `layer_id`), which is not a record member. A record byte-identical to a live snapshot's `convening` returns that snapshot unchanged, and no later step runs. **Byte-identical** means equal canonical bytes: the record's `xfc-jcs-sha256-1` serialization, the bytes `convening_digest` is taken over, equals that of the snapshot's `convening`. So two parsed JSON records compare equal regardless of member order or whitespace in their transport. A different record for the same key, while a snapshot that has not failed exists (`environment.issued.live_snapshots`), is `convening_conflict`, including a record that differs only in `candidate.pull_number` or `candidate.subject_path`. This is 025's once-per-pin guard, and 025 maps its `ConveningExistsError` to `convening_conflict`. Retry identity runs before every drift check, so a lost response followed by source or head drift still returns the same snapshot (US1 scenario 4; 025 FR-006).
3. **Secrets, before any oracle is queried with a free-text value of the record.** `secret_bearing_fact`, over every string in `packet_refs`, `class_inputs`, `parameters` and `consumed_facts` ([R9](research.md#r9--fact-authenticity-unused-facts-and-secrets)). The admission steps before it consult oracles only by grammar-checked identifiers: A1 reads the verified claims, A2 the council and the consumer's own request members, and A3 the convening key. An identical retry equals a record that already passed this step. **Precedence, stated:** a secret-bearing record that conflicts with a live key is refused `convening_conflict` at A3, not `secret_bearing_fact`; either way nothing is written and no free-text value reaches an oracle.
4. **Candidate identity.** `candidate_mismatch` when any of these fails:
   - `subject_pin` equals `candidate.head_sha`;
   - `candidate` agrees with `inputs.expected_candidate` at commission on every member the trusted trigger names (for 049's merge-readiness trigger, `repository` and `pull_number`; for its gate-rules trigger, `repository`, `pull_number`, `subject_path` and `head_sha`), and equals `environment.resolved_candidate` at admission (the consumer's own resolution);
   - when the record carries `class_inputs`: `class_inputs.repository` equals `candidate.repository`, and `class_inputs.head_ref` equals the candidate's authoritative head ref (`environment.head_refs`, read by the trusted gather at commission and by the consumer at admission). Whether the council should carry them is judged at step 6.
5. **Governed sources**, under Brett Heap's OPEN-3 ruling and its follow-ups ([R7](research.md#r7--governed-sources-rule-authority-and-revision-currency)), in this order:
   - `mutable_rule_reference`: the revision is not a full lowercase commit id;
   - `rule_unauthorized`: `governed.repository` is not an allowlisted governed repository (`environment.governed_repositories`). This runs before any read of that repository's history, and an allowlist names the current spelling, so a former spelling refuses here;
   - `rule_revision_ungoverned`: the revision is not on the governed branch's first-parent history;
   - `governed_sources_mismatch`: the listed paths are not exactly the set the projection is built from. The `rules` oracle returns that set, and each side's adapter reports the set it read, so an omitted source cannot escape the currency test;
   - then each source in path order: `rule_path_malformed`; `rule_unavailable`; `rule_unauthorized` (not an admitted governed source); `rule_digest_mismatch` (a file's bytes, or a listing's entries, differ from the record's); and last `rule_superseded`.
   - **`rule_superseded` is normative at admission**, as the ruling says ("at admission"). It applies to **every governed source** the convening cites, not only the rule file (follow-up 1, "Every governed source (Recommended)"). A source superseded at the tip is a file whose bytes differ there, or a listing whose entry set differs there. At commission the producer may run the same comparison as a pre-check. That pre-check is producer-side and non-normative, and the shared commission vectors carry no `rule_superseded` case. A shared commission vector still carries tip values, equal to the values at the revision, so a consumer that runs it through its admission resolution applies this test and passes it ([conformance-corpus § How each side runs a shared vector](contracts/conformance-corpus.md#how-each-side-runs-a-shared-vector)).
   - **A4. Workflow revision, admission only.** E10 step 14, now that step 5 has checked the `governed` member it reads.
6. **Council and class.**
   - `council_unknown`: the projection does not declare the council.
   - `class_mismatch`: the record carries `class_inputs` and `matched_class` for an unclassed council, or omits them for a classed one.
   - `class_unresolved`: for a classed council, the class selector matches nothing for `class_inputs`.
   - `class_mismatch`: the selected class is not `matched_class`. A class the projection declares but did not select is refused here; it is never accepted because it exists.
7. **Projection.** `rule_projection_mismatch`: `standing_seats`, or `conditions` apart from `held`, differ from the projection for the selected class (or for the unclassed council), in content or in order.
8. **Predicates, per condition in order.** `predicate_unknown`, then `predicate_parameters_malformed` (bad parameters, or a predicate run against the wrong input contract).
9. **The record's own facts.**
   - `fact_source_mismatch`: a source kind not allowed for its contract, a `candidate_subject` source without `candidate.subject_path`, or a `governed_path` not in `governed.sources`.
   - `opaque_conclusion`: a fact a condition reads is absent from `consumed_facts`, so the record asserts `held` without the inputs.
   - `facts_unused`: a consumed fact that no condition reads.
10. **Authoritative facts.**
    - `condition_unevaluable`: the authoritative fact set lacks a fact a condition reads, or fails completeness (E3).
    - `consumed_facts_mismatch`: a consumed fact differs from the authoritative value.
11. **Held.**
    - `condition_result_mismatch`: `held` differs from the reference evaluation.
    - `condition_seat_unbound`: a condition with `held: true` and `seat: null`.
12. **Roster** ([R6](research.md#r6--roster-composition-the-neutral-rule-projection-and-path-shaped-subjects)). The expected roster is `standing_seats`, then each held condition's `seat` in order, each appended only if absent.
    - `roster_empty`;
    - then `roster_duplicate_seat`: a repeated seat in `required_seats`;
    - then `roster_mismatch`: any other difference, including order and a same-count substitution.
13. **Live head, the last read of the candidate's head.** `candidate_head_unavailable`, then `candidate_head_moved`. At admission this is 025's `verify_subject_pin`, whose refusals map to these two codes.
    - **A5. 025's retained touched-object and base-branch guards, admission only.** They run over the verified head, under 025's existing codes (`council.base_branch_unprotected`, `council.base_branch_unverifiable` and the self-review refusal). They read only immutable objects at that head, plus the base branch's rules.

Then the consumer writes the snapshot (E4).

**Two codes, one ruled test.** The ruling names one refusal, `rule_superseded`. The plan splits its test into two codes, and discloses the split: `rule_revision_ungoverned` for a revision off the governed first-parent history, and `rule_superseded` for a source changed at the tip. The test is unchanged; only its failures are named apart.

**Lifecycle.** The producer resolves, re-gathers, rechecks the head, then submits. The consumer runs the same order before any write and then freezes the snapshot (E4). A record is never mutated; a later head or rule needs a new convening (D2).

## E3. Predicate registry and rule projection (`predicate-registry.schema.yaml` + `predicate.registry.yaml`, Phase 2)

Kind: `xfactory_council_predicate_registry`. A closed instance. **The identifiers are decided** (OPEN-5, ruled by Brett Heap on 2026-10-08, "Keep the existing names (Recommended)"): the registry keeps the identifiers the governed rule files already declare, with no mapping layer ([R5](research.md#r5--the-closed-predicate-registry-and-input-contracts)).

| Member | Content |
|---|---|
| `input_contracts.pr_facts` | `changed_paths`: at most 6000 `relative_path`. `changed_files_total`: an integer from 0 to 3000. `changed_paths_entry_count`: an integer from 0 to 3000. A rename is one entry contributing two paths. A declared total above 3000 is `condition_unevaluable`, matching 049's refusal of a total its listing cannot complete (`GATHER_MAX_LISTING_ENTRIES`). |
| `input_contracts.rule_facts` | `rule_touched_paths`: at most 6000 `relative_path`. |
| `predicates[0]` | `changed_paths_intersect`, over `pr_facts`, with parameter `protected_paths`: 1 to 256 patterns. |
| `predicates[1]` | `rule_touches_security_posture`, over `rule_facts`, with parameter `security_surfaces`: 1 to 256 patterns. |
| `pattern_grammar` | An exact `relative_path`, or `<relative_path>/**`. The refusals and the bare-directory evidence rule are in [R5](research.md#r5--the-closed-predicate-registry-and-input-contracts). |

The decision semantics:

- A predicate holds when any read path matches any pattern.
- It is unevaluable when a fact it reads is absent, or, for `pr_facts`, when `changed_paths_entry_count ≠ changed_files_total`.
- Unevaluable is never false.

**The rule projection** is what the `rules` oracle answers, and what each side's adapter derives from the domain's files:

- `councils`: a map from `council_id` to exactly one of two forms:
  - **classed**: `{class_selector, classes}`;
  - **unclassed**: `{standing_seats, conditions}`, for a council no candidate class binds, such as 049's gate-rules council, whose governed rule is its own council document.
- `class_selector`: an ordered list of `{class, repositories: [repository], head_ref: {exact: <head_ref>} | {glob: <pattern>}}`. The first entry whose `repositories` contains `class_inputs.repository` and whose `head_ref` matches `class_inputs.head_ref` selects the class. This mirrors the existing surface lookup, where both the repository and the head ref must match an entry.
- `classes`: `{<class>: {standing_seats, conditions: [{seat (seat_id or null), predicate, input_contract, parameters}]}}`.
- `sources`: the sorted paths of every governed file and listing the projection was built from (E2 step 5, `governed_sources_mismatch`).

The `head_ref.glob` grammar is the governed envelope's matcher, restated here so that no implementation copies it. Vectors pin each rule.

- `*` matches a run of characters other than `/`.
- `?` matches one character other than `/`.
- `**/` matches zero or more leading segments.
- `**` not followed by `/` matches anything.
- Every other character is literal.
- The match is anchored at both ends.

## E4. Convening snapshot (`convening-snapshot.schema.yaml`, Phase 3)

Kind: `xfactory_council_convening_snapshot`. The consumer issues it atomically at admission. The consumer's response envelope, status codes and error body are 025's.

| Member | R/O | Shape |
|---|---|---|
| `protocol` | R | The replacement. |
| `convening_id` | R | `opaque_id`, issued by the consumer. |
| `convening_digest` | R | `digest`, subject `council_convening`. |
| `convening` | R | The admitted E2 record, verbatim. |
| `assignments` | R | An array of E5. |
| `admitted_at` | R | `utc_instant`. |

**Order at `admission`, snapshot half.**

1. Classification and selection (E1).
2. `snapshot_malformed`.
3. `assignment_malformed`: an assignment fails E5, including a lifetime above the ceiling.
4. `digest_construction_mismatch`: the digest does not recompute over `convening`.
5. `assignment_set_mismatch`: not exactly one assignment per `required_seats` entry in roster order, or an assignment whose `protocol`, `convening_id`, `convening_digest`, `council_id` or `candidate` differs from the snapshot's.
6. `assignment_duplicate`: a repeated `assignment_id`.
7. `assignment_shared_holder`: one `holder.principal_ref` on two seats.

**Retry identity** (E2 step A3). The convening key is `(protocol, council_id, subject_pin)`, which is 025's once-per-pin key.

- An incoming E2 byte-identical to a live snapshot's `convening` returns that snapshot unchanged: the same `convening_id` and the same assignments.
- A different E2 for the same key, while a snapshot that has not failed exists, is `convening_conflict`, and nothing is replaced.

The consumer enforces both transactionally (025 FR-005, FR-006). The corpus states the expected outcome for each pair.

## E5. Seat assignment (`seat-assignment.schema.yaml`, Phase 3)

Kind: `xfactory_council_seat_assignment`. This is the public assignment a seat job receives. It carries no other seat's identifiers and no secret.

| Member | R/O | Shape |
|---|---|---|
| `protocol`, `convening_id`, `convening_digest`, `council_id`, `candidate` | R | Equal to the snapshot's. |
| `assignment_id` | R | `opaque_id` |
| `seat_id` | R | `seat_id` |
| `holder` | R | `{principal_kind R(principal_kind), principal_ref R(opaque_id), binding_ref R(opaque_id)}`. `principal_ref` and `binding_ref` are issued by the trusted dispatcher or the owner-provisioned broker from verified execution evidence (D3: "The trusted dispatcher binds the assignment to verified execution evidence"). This family does not derive them; it binds them and checks them at use. `binding_ref` is the `binding_id` of the holder's E10 binding. |
| `permitted_operations` | R | A non-empty, duplicate-free subset of `[seat_key_registration, seat_return]`, in that order; otherwise `assignment_malformed`. The consumer issues both today. An assignment that lacks the operation being used is `operation_not_permitted` (E7 step 4, E8 step 3), so a vector probes it with a one-operation assignment. |
| `not_before`, `expires_at` | R | `utc_instant`. The lifetime `expires_at − not_before` must be greater than 0 and at most **21600 seconds (6 hours)**; otherwise `assignment_malformed`. This is the contract ceiling Brett Heap ruled for OPEN-1 on 2026-10-08, "600 s challenge, 6 h assignment (Recommended)"; the consumer may configure a tighter value. A tighter value applies when the consumer **issues** an assignment; verification and the corpus use the contract ceiling, so a stricter consumer still accepts a 21600-second vector ([R12](research.md#r12--lifetime-ceilings)). |

The validity refusals `assignment_not_yet_valid`, `assignment_expired` and `operation_not_permitted` are checked when an assignment is **used**, at `registration` and `return` (E7, E8; Phase 4).

## E6. Registration challenge (`registration-challenge.schema.yaml`, Phase 4)

Kind: `xfactory_council_registration_challenge`. The consumer issues it, for one assignment and one public key, to be used once. This is H3's "challenge bound to assignment and its public fingerprint".

| Member | R/O | Shape |
|---|---|---|
| `protocol` | R | The replacement. |
| `challenge_id` | R | `opaque_id` |
| `assignment_id` | R | |
| `key_fingerprint` | R | The fingerprint the seat job presented when it asked for the challenge. |
| `nonce` | R | `nonce` |
| `issued_at`, `expires_at` | R | `utc_instant`. The lifetime must be greater than 0 and at most **600 seconds**, the ruled OPEN-1 ceiling; otherwise `challenge_malformed`. A consumer's tighter value applies when it issues a challenge; verification and the corpus use the contract ceiling. |

## E7. Seat key registration (`seat-key-registration.schema.yaml`, Phase 4)

Kind: `xfactory_council_seat_key_registration`. The body carries **no principal**. The verified principal comes from identity evidence (the `identity` oracle).

| Member | R/O | Shape |
|---|---|---|
| `protocol` | R | The replacement. |
| `assignment_id`, `challenge_id` | R | |
| `public_key` | R | `public_key` |
| `key_fingerprint` | R | |
| `context` | R | The registration context the job signed (E9). |
| `proof` | R | A `signature` over the JCS bytes of `context`. |

**Order at `registration`.**

1. **Classification and selection** (E1).
2. **Root authorization.** `root_authorization_refused`: any `root_key_fingerprint`, `root_signature` or `authorization` member on a replacement record.
3. **Shape.** `registration_malformed`, including **key transport**: a member named `private_key`, `secret_key`, `seed`, `sk` or `d` at any depth, or a PEM private-key block in any string (the spec delta's "key transport MUST refuse").
4. **Assignment.** `assignment_unknown`, `assignment_not_yet_valid`, `assignment_expired`, `operation_not_permitted`.
5. **Principal**, against the holder's binding:
   - `binding_unresolved`: `holder.binding_ref` names no binding in `inputs.bindings`;
   - `broker_capability_insufficient`: the holder is a `governed_broker_job`, for which no binding shape exists yet;
   - E10 steps 1 to 6 on that binding;
   - E10 steps 7 to 14 on the seat job's verified claims, with operation `seat_execution`, where step 14 applies the seat rule against the snapshot's frozen `governed.revision`;
   - then `wrong_principal`: the verified principal is not the assignment's `holder`, even when the proof is valid.
6. **Challenge**, read from `environment.issued.challenges`: `challenge_unknown` (no issued challenge has the `challenge_id`); `challenge_malformed` (the issued challenge fails E6, including a lifetime above 600 seconds); `challenge_wrong_assignment`; `challenge_consumed`; `challenge_expired`.
7. **Key.**
   - `fingerprint_mismatch`: the fingerprint does not recompute from `public_key`, or differs from the challenge's `key_fingerprint`.
   - `assignment_already_registered`.
   - `shared_key`: the fingerprint is registered for another assignment in the convening.
8. **Context.** The verifier rebuilds the expected context from the frozen assignment, the challenge and the key, and compares it with the presented `context` member by member:
   - `cross_protocol_context`: `signing_context` or `protocol` differs, including any legacy context string;
   - `cross_convening_context`: `convening_id`, `convening_digest`, `council_id` or `candidate` differs;
   - `cross_seat_context`: `assignment_id` or `seat_id` differs;
   - a differing `key_fingerprint` is `fingerprint_mismatch`, and a differing `challenge_id` or `challenge_nonce` is `challenge_wrong_assignment`.
9. **Proof.** `proof_invalid`: the signature does not verify over the presented bytes, which by now equal the expected bytes.

## E8. Seat return (`seat-return.schema.yaml`, Phase 4)

Kind: `xfactory_council_seat_return`.

| Member | R/O | Shape |
|---|---|---|
| `protocol`, `assignment_id` | R | |
| `key_fingerprint` | R | |
| `payload` | R | The seat's **whole checked return entry**: the content 049 signs today, the posted block plus the floor fields. It is admissible under the construction, with non-integer quantities written as `decimal_string` ([R11](research.md#r11--return-payload-admissibility-and-decimal-quantities)). It is the family's one open object: its member set is the domain's and the consumer's. It is bounded at 1 MiB of canonical bytes, because H1 requires bounded inputs. |
| `return_digest` | R | `digest`, subject `council_seat_return_payload`, over `payload`. |
| `context` | R | The return context (E9). |
| `signature` | R | A `signature` over the JCS bytes of `context`. |

**Order at `return`.**

1. **Classification and selection** (E1).
2. **Shape.** `return_malformed`, including key transport (as at registration, at any depth of `payload` too); then `value_not_canonicalizable` for `payload`; then `return_malformed` for a `payload` above 1 MiB of canonical bytes.
3. **Assignment.** `assignment_unknown`, `assignment_not_yet_valid`, `assignment_expired`, `operation_not_permitted`.
4. **Key.** `return_unregistered` (no key is registered for the assignment), then `return_key_mismatch` (another key).
5. **Context, compared member by member** with the context rebuilt from frozen state: `cross_protocol_context`, then `cross_convening_context`, then `cross_seat_context`. A differing `key_fingerprint` is `return_key_mismatch`.
6. **Digest.** `return_digest_mismatch`: the digest does not recompute over `payload`, or differs from the context's `return_digest`.
7. **Signature.** `return_signature_invalid`.
8. **Replay.** `return_replayed`: an accepted return already exists for the assignment.

**Order at `completion`** (Phase 4, because it reads E8 returns), over the frozen snapshot and the accepted returns:

1. `return_unlisted`: an `assignment_id` not in the snapshot.
2. `return_duplicate`: two returns for one assignment.
3. `completion_set_mismatch`: a return's `seat_id` is not its assignment's. This is the same-count wrong-identity case.
4. `return_missing`: a frozen assignment with no return.

Only after these checks do the consumer's existing verdict computation and 025's retained verdict guards run. A count is never a completeness check.

## E9. Signing contexts (`signing-context.schema.yaml`, Phase 4)

These are closed objects, carried in E7 and E8. **The signed bytes** are the UTF-8 of `canonical.serialize(context)` ([R3](research.md#r3--digest-construction-subjects-and-signed-bytes)).

| Member | Registration context | Return context |
|---|---|---|
| `signing_context` | `xfc-resolved-council-1/seat-key-registration` | `xfc-resolved-council-1/seat-return` |
| `protocol`, `convening_id`, `council_id`, `candidate`, `assignment_id`, `seat_id`, `key_fingerprint` | R | R |
| `convening_digest` | R (the digest's `value` string) | R |
| `challenge_id`, `challenge_nonce` | R | — |
| `return_digest` | — | R (the digest's `value` string) |

A verifier always rebuilds the expected context from frozen state, then compares it with the presented one. It never trusts the presented context's labels.

## E10. Producer workflow binding (`producer-binding.schema.yaml` + `.template.yaml`, Phase 5)

Kind: `xfactory_council_producer_binding`. **The concrete instance lives in the consumer's governed runtime configuration** (OPEN-2, ruled by Brett Heap on 2026-10-08, "Consumer's runtime config (Recommended)"). The operator writes it at the provisioning act (049 T031; 025 H3), and it is validated with this family's validator at the consumer's pin. The provider ships only this schema, the `.template.yaml` stub, the derivation from `repository-identity.yaml`, and the corpus ([R13](research.md#r13--producer-workflow-binding-and-its-placement)).

| Member | R/O | Shape and rule |
|---|---|---|
| `protocol` | R | The replacement. |
| `binding_id` | R | `opaque_id`: the identifier an assignment's `holder.binding_ref` names. |
| `principal_kind` | R | `github_oidc_job` |
| `issuer` | R | A literal: exactly `https://token.actions.githubusercontent.com`, or that URL followed by `/<enterprise-slug>` (GitHub's documented enterprise issuer form). Any other value is `issuer_mismatch`. |
| `audience` | R | A literal string of 1 to 256 characters. A `*` is `binding_wildcard`. |
| `caller_repository` | R | `repository`: the repository the commission or seat job runs in, which is the verified token's `repository` claim (for a reusable workflow, the caller). The identity map `contracts/policies/repository-identity.yaml` is read through `load_transfers` in `scripts/estate_inventory.py`. That reader treats an absent or unreadable map as empty, so this family adds its own fail-closed check: an absent or unreadable map, or one for which `load_transfers` reports any malformed row, is `repository_identity_unavailable`. A spelling the map lists as `former` is `repository_identity_former`. So is a **non-canonical case variant**, defined mechanically: a spelling equal to a listed `current` or `former` spelling when ASCII case is ignored, but not byte-equal to it (the map's `owner_case` prose, made testable). Any other spelling is taken as current. The same checks apply to the repository in every `permitted_workflows[].job_workflow_ref`, because the one transferred repository, codexFactory, is the one that appears there. In the corpus every vector that reads the map carries it in the `repository_identity` oracle, as the frozen identity fixture's text or as an `absent` or `unreadable` state, so the outcome is covered by the vector's own digest and never by the live file ([conformance-corpus § The frozen identity fixture](contracts/conformance-corpus.md#the-frozen-identity-fixture)). |
| `repository_id` | R | An integer of at least 1: the immutable repository identity claim. |
| `subject_claim_keys` | R | The ordered claim keys of the caller repository's subject template: GitHub's default (`repo` then the context) or the keys of its documented subject customization. The closed set of keys is enumerated at T053 from GitHub's OIDC reference, which T053 cites. |
| `subject_template` | R | A literal OIDC `sub` that parses, under GitHub's documented `sub` grammar, into elements in `subject_claim_keys` order. Its `repo` or `repository_id` element must name `caller_repository` or `repository_id`. A template that does not parse, or that names another repository, is `subject_template_mismatch`. A `*` is `binding_wildcard`. |
| `permitted_workflows` | R | 1 to 8 entries of `{operation: commission \| seat_execution, job_workflow_ref: <owner>/<repo>/.github/workflows/<file>@<ref>, workflow_revision_rule}`. `workflow_revision_rule` is `equals_governed_revision` for `commission` and `on_governed_history_since_revision` for `seat_execution`; any other pairing is `binding_malformed`. A workflow not listed for the operation is `workflow_not_permitted`. |
| `broker` | R | `{broker_ref R(opaque_id), capability_verified R(boolean), evidence_ref R(opaque_id or null)}`. This records the broker's state and is its **one source of truth**; it refuses nothing at binding. `capability_verified: false`, or a `null` `evidence_ref`, parks activation: E12 reads this member through the activation record's `binding_refs` and refuses `broker_capability_insufficient` at `activation` and `resume` (D4). |
| `instantiation_stub` | O | `const: true`, in the `.template.yaml` only. A stub is never accepted as a live binding (`binding_malformed`). |

**The workflow-revision rule** encodes the second half of the OPEN-3 ruling ("where the rule repository is the producer repository, the producer's verified `job_workflow_sha` equals the cited rule revision"). The producer's code is the workflow named by the verified `job_workflow_ref` claim, and `job_workflow_sha` is a commit of that workflow's repository. So the comparison is with that repository, not with the caller. The closed enumeration has two values:

- `equals_governed_revision`, for a commission job: the repository named in the verified `job_workflow_ref` is `governed.repository`, and the verified `job_workflow_sha` is `governed.revision`.
- `on_governed_history_since_revision`, for a seat job: the repository named in the verified `job_workflow_ref` is the snapshot's frozen `governed.repository`, and the verified `job_workflow_sha` is on that repository's governed first-parent history, at or after the frozen `governed.revision`. A seat job runs after admission, often after `main` has moved, and 049's seat worker checks its tooling out from the default branch (049 `contracts/interfaces.md`, W1), so equality would refuse every seat whose `main` moved. This value applies the ruling's "history" half to seats. Brett Heap ruled it on 2026-10-08 as follow-up 3, "At or after the frozen rev (Recommended)".

**The seat's checkout must be that commit.** The verified `job_workflow_sha` vouches for the workflow file. A seat job that then checks out its tooling at another commit would run code nothing verified. So a seat job checks out its tooling at exactly its verified `job_workflow_sha`, as the commission job already must at the governed revision. 049's seat worker today checks out the default-branch HEAD (W1), which is a recorded producer impact ([provider-interface](contracts/provider-interface.md#consumer-impacts-recorded-by-this-plan); 049 T016b, T023).

This covers the estate's own calling pattern: xFactory's `council-convening-lane.yml` calls codexFactory's `council-lane-reusable.yml`, so the caller is `opensoft/xFactory` while the workflow, its commit and the rules are codexFactory's. A permitted producer workflow in a repository that is not the governed repository is refused (`workflow_revision_ungoverned`), which fails closed. Brett Heap ruled both halves on 2026-10-08 as follow-up 2, "job_workflow_ref's repo (Recommended)": the ruling's "producer repository" is the repository named in `job_workflow_ref`, and this entity's `caller_repository` is a different thing, the calling repository. Admitting a workflow outside the governed repository would be a governed contract change that adds a value.

**Order at `binding`.** At admission the consumer runs steps 1 to 13 as E2 step A1, once the record has classified and passed its shape check, and step 14 as E2 step A4, once E2 step 5 has checked the record's `governed` member. Its inputs are `inputs.binding` (the E10 instance), `inputs.operation` and the record's `governed` member; the verified claims come only from `environment.identity`, and broker capability only from the binding's `broker` member. Steps 1 to 6 judge the binding instance alone, so offline `check` runs them; steps 7 to 14 need the verified claims (D3: "the consumer verifies signed issuer/audience/expiry").

1. `binding_malformed`, including a `.template.yaml` stub presented as live.
2. `binding_wildcard`.
3. `issuer_mismatch`: the binding's `issuer` is not one of the two allowed forms.
4. `repository_identity_unavailable`: the identity map is absent, unreadable, or has a malformed row. Then `repository_identity_former`: `caller_repository`, or the repository in a permitted `job_workflow_ref`, is a former spelling or a non-canonical case variant.
5. `subject_workflow_conflation`: the `subject_template` is a bare workflow reference, meaning it has the shape `<owner>/<repo>/.github/workflows/<file>@<ref>` and no `key:` element.
6. `subject_template_mismatch`: the template does not parse, or names another repository.
7. `claims_unverified`: claims taken from a decoded assertion whose signature was not verified.
8. `claims_expired`: the token's `exp` is at or before `evaluation_time`, or its `nbf` is after it.
9. `issuer_mismatch`: the verified `iss` is not the binding's `issuer`.
10. `audience_mismatch`: the verified `aud` is not exactly the binding's `audience`.
11. `subject_template_mismatch`: the verified `sub` is not the binding's `subject_template`.
12. `repository_identity_mismatch`: the verified `repository` or `repository_id` claim differs from `caller_repository` or `repository_id`.
13. `workflow_not_permitted`: the verified `job_workflow_ref` is not listed for the operation.
14. `workflow_revision_ungoverned`: the verified `job_workflow_sha` breaks the operation's `workflow_revision_rule`.

**Conflation is judged by meaning, not by substring.** Step 5 refuses a template that is a bare workflow reference. A template that includes the `job_workflow_ref` claim key, through GitHub's documented subject customization, is legal.

Permitted workflows are matched against the verified `job_workflow_ref` claim, never against `sub`. Data can show this: a vector whose `sub` contains a permitted workflow reference, while its verified `job_workflow_ref` names an unlisted one, must refuse `workflow_not_permitted`.

## E11. Protocol selection (`protocol-selection.schema.yaml`, Phase 6)

Kind: `xfactory_council_protocol_selection`. This is the shape of each side's governed configuration (H4; 049 T027/T030).

| Member | R/O | Shape |
|---|---|---|
| `side` | R | `producer` or `consumer`. |
| `mode` | R | `rehearsal` or `active`. |
| `protocol` | R | A registry `protocol_id`. |
| `provider_commit` | R | `full_sha` |
| `provider_bundle` | R | `contract-v<major>.<minor>`, or `null`. `null` is allowed only with `mode: rehearsal`; otherwise `selection_malformed`. |
| `corpus_index_sha256` | R | `raw_sha256` |

**Order at `selection`.**

1. `selection_malformed`.
2. `protocol_unknown`.
3. For an `active` replacement selection, `replacement_not_admission_eligible` when the registry status is not `admission_eligible`. For any legacy selection, in either mode, while the legacy status is `historical_only`, `legacy_protocol_refused`.
4. Across two sides, `pair_mismatched` unless `mode`, `protocol`, `provider_commit`, `provider_bundle` and `corpus_index_sha256` are all equal.
5. `rejected_without_fallback`: the vector names the protocol a refusal was recorded under (`inputs.rejected_under`) and a later selection attempt (`inputs.selection_attempt`) that names any other protocol.

## E12. Activation evidence (`activation-evidence.schema.yaml`, Phase 6)

Kind: `xfactory_council_activation_evidence`. One record per act. It records owner acts; it does not perform them. `act` is one of `pause`, `drain`, `switch`, `rehearsal`, `activation`, `rollback` or `resume`.

| Member | Required for |
|---|---|
| `act`, `recorded_at` (`utc_instant`), `provider` (`{commit, bundle, corpus_index_sha256}`) | every act |
| `owner_word` (`{author, date, verbatim, cite}`) | `pause`, `switch`, `activation`, `rollback`, `resume` |
| `intake` (`{paused_at}`) | `drain`, `switch`, `activation`, `rollback`, and a `rehearsal` whose `rehearsal.mode` is `matched` |
| `in_flight` (`{disposition: drained \| cancelled, convening_ids}`) | `drain` |
| `producer`, `consumer` (`{repository, revision, selection}`, where `selection` is that side's E11 record) | `switch`, `rehearsal`, `activation`, `rollback`, `resume`. The two selections must agree on the five matched values (`pair_mismatched`). |
| `rehearsal` (`{mode: dormant \| matched, corpus_index_sha256, outcome: pass \| fail, evidence_ref}`) | `rehearsal` |
| `rehearsal_ref` (the raw SHA-256 of the bytes of a `rehearsal` record with `mode: matched` and `outcome: pass`; a vector supplies that record's exact UTF-8 text as the JSON string `inputs.rehearsal`, and the hash is taken over those bytes) | `activation`, `resume` |
| `binding_refs` (1 to 16 `opaque_id`, unique: the `binding_id` of every E10 binding the activated consumer will use, its commission binding and each seat holder's, resolved against `inputs.bindings`, the consumer's configured binding set) | `activation` and `resume`, but **not** `rollback`, which a broker failure may cause. The consumer refuses unless `binding_refs` equals its configured binding set, so the set is complete: a configured binding it omits is `activation_evidence_incomplete` (step 2), and an entry the consumer does not configure is `binding_unresolved` (step 3). The record carries no broker state of its own: broker capability is read only from each named binding's `broker` member (D4: "activation parks"). |
| `rollback` (`{restored_producer, restored_consumer, new_records_retained, new_records_protocol}`) | `rollback`. `new_records_retained` must be `true` (`activation_evidence_incomplete` otherwise). `new_records_protocol` names the protocol under which the retained new records stay verifiable, and must be the replacement's `protocol_id`. |

**Order at `activation`.**

1. `activation_evidence_malformed`: the record fails its schema.
2. `activation_evidence_incomplete`: a member its act requires is missing; `new_records_retained` is `false`; or an activation or resume has no passing matched rehearsal behind `rehearsal_ref`, or one whose `provider` or five matched selection values differ from the activation's; or an activation or resume whose `binding_refs` omits a binding in `inputs.bindings`.
3. **Broker capability**, for an activation or resume, for each entry of `binding_refs` in order: `binding_unresolved` when it names no binding in `inputs.bindings`; then `broker_capability_insufficient` when that binding's `broker.capability_verified` is `false`, or its `broker.evidence_ref` is `null`.
4. `pair_mismatched`: the two sides' selections differ on a matched value.
5. `historical_reinterpretation_refused`: a rollback whose `new_records_protocol` is not the replacement's `protocol_id`, so that new-protocol records would be read under another protocol.

## E13. Conformance corpus (Phases 1–6; digest registered at Phase 7)

The full format is in [contracts/conformance-corpus.md](contracts/conformance-corpus.md):

- the index `conformance/index.json`;
- vectors at `conformance/vectors/<area>/<case_id>.json`;
- outcomes `accept`, `refuse` and `route`;
- the oracles that `environment` injects.

## Refusal vocabulary

The vocabulary is closed. Each phase adds its codes to `refusal_code` in the task that authors its schemas. The validator requires every code in the enumeration **at that commit** to be probed (`council-convening-refusal-code-without-probe`). Finding codes are listed under [Shared definitions](#shared-definitions-shared-definitionsschemayaml-phase-1).

**The mapping to 049 is not one-to-one.** Where the last column lists one 049 name against several codes, 049 must split that refusal when T010 and T020 map its internal names onto these. This is a producer-side refinement, recorded as a consumer impact ([provider-interface](contracts/provider-interface.md#consumer-impacts-recorded-by-this-plan)). 049's `return_wrong_identity` maps to `completion_set_mismatch`.

| Codes | Boundary | Phase | 049 name today |
|---|---|---|---|
| `value_malformed`, `value_not_canonicalizable`, `protocol_unknown`, `protocol_not_selected`, `legacy_protocol_refused` | `definition`, `classification`, and step 1 of every later boundary | 1 | `facts_malformed` / `resolution_malformed` for a bad value (split); T026 `selector_unknown` |
| `convening_malformed`, `council_unknown`, `class_unresolved`, `class_mismatch`, `rule_projection_mismatch` | commission, admission | 2 | `resolution_malformed`, `council_unknown`, `class_unresolved`, `opaque_conclusion` (split) |
| `mutable_rule_reference`, `rule_revision_ungoverned`, `governed_sources_mismatch`, `rule_path_malformed`, `rule_unavailable`, `rule_unauthorized`, `rule_digest_mismatch`, `rule_superseded` | commission, admission | 2 | `mutable_rule_reference`, `rule_revision_ungoverned`, `rule_unavailable`, `rule_unauthorized` |
| `predicate_unknown`, `predicate_parameters_malformed`, `condition_unevaluable`, `condition_result_mismatch`, `condition_seat_unbound` | commission, admission | 2 | `condition_refused` (split), `condition_unevaluable`, `opaque_conclusion`, `conjunction_seat_unbound` |
| `opaque_conclusion`, `facts_unused`, `consumed_facts_mismatch`, `fact_source_mismatch`, `secret_bearing_fact` | commission, admission | 2 | `opaque_conclusion`, `unused_facts`, `consumed_facts_mismatch`, `secret_bearing_fact` |
| `candidate_mismatch`, `candidate_head_moved`, `candidate_head_unavailable` | commission, admission | 2 | `candidate_identity_mismatch`, `final_head_moved`, `final_head_unavailable` |
| `roster_empty`, `roster_duplicate_seat`, `roster_mismatch` | commission, admission | 2 | `invalid_membership` (split three ways) |
| `snapshot_malformed`, `digest_construction_mismatch`, `assignment_malformed`, `assignment_set_mismatch`, `assignment_duplicate`, `assignment_shared_holder`, `convening_conflict` | admission (E4 and E2 step A3) | 3 | `assignment_malformed`, `assignment_shared_holder` |
| `assignment_unknown`, `assignment_not_yet_valid`, `assignment_expired`, `operation_not_permitted` | registration, return | 4 | `assignment_unknown` |
| `challenge_malformed`, `challenge_unknown`, `challenge_wrong_assignment`, `challenge_consumed`, `challenge_expired` | registration | 4 | the same names |
| `registration_malformed`, `root_authorization_refused`, `wrong_principal`, `fingerprint_mismatch`, `assignment_already_registered`, `shared_key`, `cross_protocol_context`, `cross_convening_context`, `cross_seat_context`, `proof_invalid` | registration | 4 | the same names |
| `return_malformed`, `return_unregistered`, `return_key_mismatch`, `return_digest_mismatch`, `return_signature_invalid`, `return_replayed` | return | 4 | the same names |
| `return_unlisted`, `return_duplicate`, `return_missing`, `completion_set_mismatch` | completion | 4 | the same names; plus `return_wrong_identity` → `completion_set_mismatch` |
| `binding_unresolved`, `broker_capability_insufficient` | registration, activation | 4 | — |
| `binding_malformed`, `claims_unverified`, `claims_expired`, `issuer_mismatch`, `audience_mismatch`, `binding_wildcard`, `repository_identity_unavailable`, `repository_identity_former`, `repository_identity_mismatch`, `subject_template_mismatch`, `subject_workflow_conflation`, `workflow_not_permitted`, `workflow_revision_ungoverned` | binding, admission, registration | 5 | — |
| `selection_malformed`, `pair_mismatched`, `rejected_without_fallback`, `replacement_not_admission_eligible`, `activation_evidence_malformed`, `activation_evidence_incomplete`, `historical_reinterpretation_refused` | selection, activation, historical | 6 | `pair_mismatched`, `rejected_without_fallback`, `replacement_not_admitted` |

Phase 5 lands before Phase 4, because registration checks a seat job's claims against its holder's binding (E7 step 5). So every binding code is introduced in Phase 5, where `binding`-boundary vectors and admission vectors (operation `commission`) probe it, and reused in Phase 4. The two codes whose first triggers are in Phase 4, `binding_unresolved` and `broker_capability_insufficient` (both at E7 step 5, and both again at E12 from Phase 6), are introduced in Phase 4, so each phase's coverage rule can be met at its own commit.
