# Research: Neutral resolved council protocol

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) · **Analysis**: [analysis.md](analysis.md) · **Date**: 2026-10-08

Each decision records what was chosen, the reason, and the alternatives considered. Each reason is traced to a feature requirement (FR or SC), a ratified design decision (D1–D5), and the consumer need it serves. The consumers are:

- codexFactory feature 049, read at `origin/main` `3d5c2c38` on 2026-10-08, with its class binding and gate-rules candidate re-read at `2ce8544e` the same day;
- Hermes packet `admit-resolved-council-protocol` (design H1–H4) and its feature 025 spec.

**Five questions were Brett Heap's to decide, and all five are ruled; so are the three follow-ups that apply OPEN-3.** He chose the recommended option of each, first-hand, on 2026-10-08. The record is brett-wip `lanes/log/codeXfactory-2.md`: RULED lines at 19:24:21Z (OPEN-1 to OPEN-4), 19:24:59Z (OPEN-5) and 23:03:35Z (the three follow-ups, and N10). Each label below is quoted verbatim.

| Question | Ruling | Encoded in |
|---|---|---|
| OPEN-1, lifetime ceilings | "600 s challenge, 6 h assignment (Recommended)" | [R12](#r12--lifetime-ceilings) |
| OPEN-2, producer-binding home | "Consumer's runtime config (Recommended)" | [R13](#r13--producer-workflow-binding-and-its-placement) |
| OPEN-3, revision currency | "History + unchanged rule file (Recommended)" | [R7](#r7--governed-sources-rule-authority-and-revision-currency) |
| OPEN-3 follow-up 1, which sources | "Every governed source (Recommended)" | [R7](#r7--governed-sources-rule-authority-and-revision-currency) |
| OPEN-3 follow-up 2, the producer repository | "job_workflow_ref's repo (Recommended)" | [R7](#r7--governed-sources-rule-authority-and-revision-currency), [R13](#r13--producer-workflow-binding-and-its-placement) |
| OPEN-3 follow-up 3, the seat's workflow commit | "At or after the frozen rev (Recommended)" | [R7](#r7--governed-sources-rule-authority-and-revision-currency), [R13](#r13--producer-workflow-binding-and-its-placement) |
| OPEN-4, release inventory | "Join behind a version floor (Recommended)" | [R15](#r15--release-surface-membership) |
| OPEN-5, predicate identifiers | "Keep the existing names (Recommended)" | [R5](#r5--the-closed-predicate-registry-and-input-contracts) |

The questions, their options and the answers are kept in [clarify-questions.md](clarify-questions.md) and encoded in [spec.md § Clarifications](spec.md#clarifications).

## Inputs read, and the facts this research rests on

- **Provider base.** The governing packet, #1267, landed in `main` as `80f47483` on 2026-10-08, and this branch merges `origin/main` from there. The manifest declares `contract_bundle_version: contract-v4.0`, and `contract-v4.0` is tagged on the remote. No `contracts/council-convening/` exists on `main`. The old #517 candidate (branch `026-add-resolved-council-seats`) is preserved for reference only, and nothing here depends on it.
- **The legacy protocol is not provider-owned.** The roster-less `council_convening` envelope block is Hermes-local: `council_id`, `subject_pin`, `packet_refs` and an optional `mix_id`, with `members` derived from materialized council content (`src/hermes_install/domain/council_orchestration.py`). Hermes accepts a bare-string `packet_refs`, skips malformed entries, and derives the pull number from them. Its two signing contexts are `xfactory-council-seat-return/v1` and the root-authorized `xfactory-council-seat-key-authorization/v1`. Both are defined by codexFactory's `council_seat_signing.py` and Hermes spec 015's golden vectors. The neutral job envelope (`contracts/hermes-runtime/`) declares no convening block.
- **Existing provider constructions.**
  - `xfc-jcs-sha256-1` is the JSON value digest (`contracts/signed-execution-chain/digest-construction.schema.yaml`, implemented in `scripts/signed_execution_chain/canonical.py`). It refuses non-integer numbers, integers outside ±(2^53 − 1) and unpaired surrogates.
  - Raw-byte SHA-256 is used for files: the release inventory and manifest rows.
  - The key fingerprint is `sha256:` + the lowercase hex SHA-256 of the raw 32-byte Ed25519 public key (openXwallet `fingerprint_of_public_key`; codexFactory `key_fingerprint`). *Corrected 2026-10-09 on Brett Heap's ruling of 2026-10-09T02:36:50Z, "Estate spelling (Recommended)": this line read "`sha256:` + hex of the raw 32-byte Ed25519 public key", which is not what the cited function computes; see data-model E1 `key_fingerprint`.*
  - `scripts/signed_execution_chain/ed25519.py` verifies signatures with the standard library alone.
- **049's state.** The producer has realized only producer-internal, dormant structures, and invented no provider shape. T001 stops all provider-facing wiring until this family is published and pinned: T010, T012, T015b, T020, T023's policy source, T027 and T030.
  - The producer's current internal refusal names are listed against the shared vocabulary in [data-model.md](data-model.md#refusal-vocabulary). The mapping is many-to-one in places.
  - Its identifier bound is `^[A-Za-z0-9][A-Za-z0-9._:/@+=-]{0,255}\Z`.
  - Its predicate registry holds two entries: `changed_paths_intersect` over `pr_facts`, and `rule_touches_security_posture` over `rule_facts`.
  - Its roster order is the standing seats first, then each held condition's seat, appended if absent.
  - It has two councils. The merge-readiness council's candidate is `{repository, pull_number, head_sha}`, and its class is bound by the envelope surface the candidate's repository and head ref match (`envelope._find_surface`, then `select_rule`). The gate-rules council's candidate is `{repository, rule_packet_path, subject_pin}`. Its `rule_facts` are read from the rule packet at `subject_pin`, and its live head comes from the dispatch's `candidate_pull_number` (049 T011b).
  - Its gather refuses a declared total above 3000 changed files (`GATHER_MAX_LISTING_ENTRIES`).
  - Its seat entry carries floating-point `costUSD` values in `model_usage`, so its internal entry digest does not use a float-refusing canonical form.

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

Every signature in this family covers the UTF-8 bytes of `canonical.serialize(context)`, where `context` is a closed object carrying a `signing_context` member, a versioned string ([R10](#r10--protocol-and-signing-context-identifiers-and-classification)). No prefix framing is used. No other digest or framing is introduced.

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
- The reference implementation and the generator could share one canonicalization bug and agree with each other. So known answers that come from outside this code are pinned too ([R16](#r16--the-corpus-digest-and-coverage)).
- Trace: FR-010, SC-001.

**Alternatives.** An index of expected outcomes with no provider-side execution: an unexecuted expectation is an assertion (Principle V). Rejected.

## R5 — The closed predicate registry and input contracts

**Decision (ruled).** `predicate.registry.yaml` is a closed instance of `predicate-registry.schema.yaml`. It keeps the identifiers the governed rule files already declare, with no mapping layer. Brett Heap ruled this for OPEN-5 on 2026-10-08: "Keep the existing names (Recommended)".

| Predicate | Input contract | Parameters | Facts read | Decision |
|---|---|---|---|---|
| `changed_paths_intersect` | `pr_facts` | `protected_paths`: 1 to 256 patterns | `changed_paths`, `changed_files_total`, `changed_paths_entry_count` | Holds when any changed path matches any pattern. **Unevaluable** when a fact it reads is absent, or when the entry count differs from the declared total. |
| `rule_touches_security_posture` | `rule_facts` | `security_surfaces`: 1 to 256 patterns | `rule_touched_paths` | Holds when any touched path matches any surface. **Unevaluable** when `rule_touched_paths` is absent. |

The pattern grammar is exact and total. A pattern is either an exact repository-relative path or a `dir/**` tree. The refusals, all `predicate_parameters_malformed`:

- a rooted, dot-relative or trailing-slash pattern;
- any `*`, `?` or `[` outside the trailing `/**`;
- an exact pattern for which an observed path lies inside `pattern/`: it was a directory declared as a file (the bare-directory evidence rule).

Each implementation must reproduce every one of these by vector.

Both input contracts are closed. `pr_facts` is the three facts above, with `changed_paths` bounded at 6000 paths and both counts at 3000, which is 049's listing bound; a rename is one entry contributing two paths. `rule_facts` is `rule_touched_paths`, bounded at 6000. Fact values are strings, integers within the construction's bound, booleans, or lists of strings, never non-integer numbers. Adding or renaming a predicate kind or a fact is a governed contract change.

**Rationale.**

- D1 says "The closed predicate registry and input type contracts are shared specifications and vectors".
- The ruling settles how this reads beside the Goals' "Domain predicates remain domain-owned". The domain owns which seats a rule conditions on, and with which parameters. The evaluation mechanism is neutral.
- Both kinds are mechanical intersections over declared paths (Principle I).
- Keeping the declared identifiers leaves no renaming layer between a governed rule and the record citing it, so there is no mapping where the two adapters could drift apart.
- The completeness, unevaluable and bare-directory rules keep "unevaluable" from silently reading as "false" (spec delta, requirement 1: "an unevaluable condition MUST refuse commissioning rather than become false").
- Trace: FR-002, FR-003; 049 T003 and T010; 025 FR-002 and FR-003.

**Alternatives.**

- Neutral identifiers, with each side's adapter mapping its domain's declared names: put to Brett Heap as OPEN-5 option (b), and not chosen.
- Open-ended predicate strings: the "unenforced-key hazard" the producer's closed registry exists to prevent. Rejected.
- Copying the producer's glob code: forbidden by R4. The semantics are specified here, and the producer's code is not the source.

## R6 — Roster composition, the neutral rule projection and path-shaped subjects

**Decision.** The provenance carries the governed rule's **neutral projection** for the matched class, plus the inputs that selected the class:

- `class_inputs`: the candidate's `repository` and `head_ref`, for a classed council;
- `matched_class`, for a classed council;
- `standing_seats`, ordered;
- `conditions`, ordered: `seat`, `predicate`, `parameters`, `input_contract`, `held`.

The projection's `class_selector` is an ordered list of `{class, repositories, head_ref}` entries, where `head_ref` is exact or a glob. The first entry matching both `class_inputs` members selects the class, so the consumer reproduces class selection instead of trusting the cited class ([data-model E3](data-model.md#e3-predicate-registry-and-rule-projection-predicate-registryschemayaml--predicateregistryyaml-phase-2)). A class that the projection declares but did not select is `class_mismatch`.

**The class inputs are authenticated, not only cited.** `class_inputs.head_ref` must equal the candidate's head ref as the trusted gather read it at commission, and as the consumer reads it at admission (`environment.head_refs`); otherwise `candidate_mismatch`. Without that check a producer could cite a head ref that selects a lighter class.

**Some councils have no class.** The projection declares each council as either classed (a class selector and classes) or unclassed (one set of standing seats and conditions). 049's gate-rules council is unclassed: no candidate class binds it, and its governed rule is its own council document. Its record carries neither `class_inputs` nor `matched_class`, and carrying them, or omitting them for a classed council, is `class_mismatch`.

The roster rule is: `required_seats` equals `standing_seats` in order, followed by the seat of each condition with `held: true` in `conditions` order, each appended only if not already present. The result must be non-empty and unique. A condition whose `held` is true and that names no seat refuses (`condition_seat_unbound`).

**The candidate is D1's**: repository, positive pull number and full head. It may also name a `subject_path`, a path-shaped subject at the head. That is how the gate-rules council fits:

- its `rule_packet_path` becomes `candidate.subject_path`;
- its `subject_pin` becomes `candidate.head_sha`;
- the dispatch's `candidate_pull_number`, which 049 T011b already reads for the live head, becomes `candidate.pull_number`;
- its `rule_facts` are declared with the fact source `candidate_subject`;
- it carries no class inputs, so no head ref is read for it.

Each side derives the projection from the domain's rule files through its own adapter. 049 uses its existing loader. 025 uses H1's "allowlisted governed-repository adapter". The corpus supplies projections through a rule oracle ([R8](#r8--environment-oracles-make-authority-facts-and-heads-testable)).

**Rationale.**

- D1 requires "ordered, nonempty, unique" membership with the "predicate identifier and typed parameters" in provenance, and refuses "reordered results". It also requires that the consumer "reproduces its roster", which it cannot do if the class is only cited.
- The order rule is exactly 049's `resolve_required_seats`, so the producer's roster composition needs no change. Its refusal names do need refining ([data-model § Refusal vocabulary](data-model.md#refusal-vocabulary)).
- Carrying `held: false` conditions keeps every evaluated condition reproducible. It also lets the producer derive its unseated-conjunction metadata (T015a) from the frozen record alone.
- Domain rule shapes, such as flat versus layered rosters and the envelope's surface entries, stay domain-owned (Principle I). The projection carries only what membership needs.
- Trace: FR-001–FR-003, SC-001; 049 T010, T011, T015b; 025 FR-002.

**Consumer impact, recorded.** 049's gate-rules candidate gains `pull_number` and is respelled as above at T010/T011. Reading that pull request's live head needs `pull-requests: read` in the gate-rules trigger, which is already an owner decision under 049 T011b. Its merge-readiness record gains `class_inputs`, taken from the trusted gather. See [provider-interface § Consumer impacts](contracts/provider-interface.md#consumer-impacts-recorded-by-this-plan).

**Residual risk, recorded.** The two adapters could map the same domain file differently, and the neutral corpus cannot test a domain file. Such a disagreement fails closed: the consumer's projection differs from the record's, and admission refuses `rule_projection_mismatch`. Phase 1 states this in the family README. 049's own tests over real council documents and the matched rehearsal (049 T032; SC-004) are where it is caught before activation.

**Alternatives.**

- Provider-specified domain rule shapes: domain vocabulary in the neutral layer. Rejected.
- Carry only `required_seats` plus a rule digest: an "opaque Boolean conclusion" and a "digest-only rule reference", both refused by D1. Rejected.
- A tagged candidate union with no pull number for path-shaped subjects: contradicts D1's "positive pull number", and 049 already has the pull number. Rejected.

## R7 — Governed sources, rule authority and revision currency

**Decision (ruled).** Authority is not availability. The record lists **every governed source** the projection was built from, at one immutable revision of one governed repository. A source is a file, with its raw SHA-256, or a listing. A listing names a directory, the suffixes read from it, and the sorted files directly inside it with those suffixes, each of which is also a file source. 049's merge-readiness projection, for example, reads the council document, every YAML document directly in the rule directory, and the envelope configuration; its `read_directory` reads exactly the `.yaml` and `.yml` files there. A listing is not a git tree id, because the rule directory also holds code, and a tree id would change on every unrelated code edit.

Revision currency is Brett Heap's OPEN-3 ruling of 2026-10-08, "History + unchanged rule file (Recommended)". The label is his. The RULED line records the option it selects as: "a revision on the governed first-parent history whose rule-file blob equals the governed tip's at admission, otherwise rule_superseded; where the rule repository is the producer repository, the producer's verified job_workflow_sha equals the cited rule revision"

The checks run in this order ([data-model E2](data-model.md#e2-commission-record-council-conveningschemayaml-phase-2), step 5):

| Condition | Refusal |
|---|---|
| The revision is not a full lowercase 40-hex commit id | `mutable_rule_reference` |
| `governed.repository` is not an allowlisted governed repository, checked before any read of its history (a former spelling refuses here, because the allowlist names the current spelling) | `rule_unauthorized` |
| The revision is not on the governed branch's first-parent history | `rule_revision_ungoverned` |
| The listed paths are not exactly the set the projection is built from | `governed_sources_mismatch` |
| A source path is not normalized and relative | `rule_path_malformed` |
| A source is absent at the revision | `rule_unavailable` |
| A source exists but is not an admitted governed source | `rule_unauthorized` |
| A file's bytes, or a listing's entries, do not match the record | `rule_digest_mismatch` |
| At admission, a source at the revision differs from the same source at the governed tip; for a listing, the set of entries differs | `rule_superseded` |

**Every governed source is held to the ruled test, not only the rule file.** Each source contributes to the projection: the class selector, the standing seats or the conditions. A changed council document at the tip would otherwise seat an outdated roster, which is what the ruling refuses. The ruling's words name "the rule file", so the plan put the wider reading to Brett Heap, who ruled it on 2026-10-08 as follow-up 1, "Every governed source (Recommended)". No narrower fallback remains.

**`rule_superseded` is normative at admission only**, as the ruling says ("equals the governed tip's at admission"). The producer may run the same comparison at commission as a pre-check, so that it does not submit a record it knows the consumer will refuse. That pre-check is producer-side and non-normative: the shared commission vectors carry no `rule_superseded` case, and its effect on 049 is recorded in [provider-interface](contracts/provider-interface.md#consumer-impacts-recorded-by-this-plan).

**Two codes for one ruled test, disclosed.** The ruling names one refusal, `rule_superseded`. The plan names a revision that is off the governed first-parent history `rule_revision_ungoverned`, and keeps `rule_superseded` for a source changed at the tip. The test is the ruled one; only its two failures are named apart, so a vector can say which half failed.

**The workflow half** is encoded in the producer binding's closed `workflow_revision_rule`, which has two values, one per operation ([data-model E10](data-model.md#e10-producer-workflow-binding-producer-bindingschemayaml--templateyaml-phase-5)):

- `equals_governed_revision`, for the commission job: the repository in the verified `job_workflow_ref` is `governed.repository`, and the verified `job_workflow_sha` equals `governed.revision`;
- `on_governed_history_since_revision`, for a seat job: the repository in the verified `job_workflow_ref` is the snapshot's frozen `governed.repository`, and the verified `job_workflow_sha` is on its governed first-parent history at or after the frozen `governed.revision`. A seat runs after admission, when `main` may have moved, so equality would refuse every seat whose `main` moved. Brett Heap ruled this on 2026-10-08 as follow-up 3, "At or after the frozen rev (Recommended)".

The producer's code is the workflow the verified `job_workflow_ref` names, and `job_workflow_sha` is a commit of that workflow's repository. So "the rule repository is the producer repository" is read as: the repository in `job_workflow_ref` is `governed.repository`. Brett Heap ruled that reading on 2026-10-08 as follow-up 2, "job_workflow_ref's repo (Recommended)".

That reading fits the estate's calling pattern. xFactory's `council-convening-lane.yml` calls codexFactory's `council-lane-reusable.yml`, so the token's `repository` (the binding's `caller_repository`) is the caller, while the workflow, its commit and the rules are codexFactory's. A permitted producer workflow whose repository is not the governed repository is refused (`workflow_revision_ungoverned`), which fails closed; follow-up 2 rules this too.

**Each job checks out what was verified.** The verified `job_workflow_sha` vouches for the workflow file only. So the commission job checks out its trusted tooling at that commit, which equals the governed revision, and a seat job checks out its tooling at exactly its own verified `job_workflow_sha`. 049's seat worker today checks out the default-branch HEAD (W1), which this requirement changes; it is a recorded producer requirement on 049 (T016b, T023).

**Why the ruled option.**

- It refuses a roster under a governed source that has changed by the time admission reads the tip. A source can still change in the interval between that read and the snapshot write. The check narrows that race to the admission transaction; it does not close it, and the frozen snapshot records the revision it was admitted under.
- It never refuses on movement of main outside the governed sources. Under the every-source ruling it does refuse when any governed source changed between commission and admission. Only first-parent movement of the governed branch can supersede a source. 29 first-parent codexFactory commits touched the governed sources, council documents included, with committer dates from 2026-09-01T00:00:00Z up to 2026-10-08T00:00:00Z: about 0.78 a day across those 37 days. In UTC all of them fall between 2026-09-01T12:52:38Z and 2026-09-12T15:59:10Z, with at most 6 on one day (2026-09-03). That is against a commission-to-admission window of minutes. The count comes from this command, run in codexFactory at `2ce8544e`, with both bounds pinned in UTC:

  ```text
  git log --oneline --first-parent --since=2026-09-01T00:00:00Z --until=2026-10-08T00:00:00Z 2ce8544e -- \
    ':(glob)hermes/domain/agent-mixes.yaml' ':(glob)hermes/domain/review-councils/*.yaml' \
    ':(glob)scripts/merge_master/*.yaml' ':(glob)scripts/merge_master/*.yml' \
    ':(glob).github/merge-approval-envelope.yml' | wc -l
  ```

  It prints 29; without `--first-parent` it prints 50. The `:(glob)` magic matters: in a plain git pathspec `*` also matches `/`, so the same paths without it also count the YAML records, templates and vendored pins in subdirectories, which are not governed sources. That form prints 43 first-parent and 102 in all, an upper bound. The dates come from `TZ=UTC git log --date=format-local:...`. An earlier count, 28 and 48, left the bounds without a time or zone, so the shell's local zone shifted the window. A refused convening is convened again.
- It closes the self-selection class the producer's adversarial review found (049 T008, F1: a candidate choosing the rule that decides its own membership).

**Consumer impact.** 049 T010/T023 checks out its trusted tooling at exactly the verified workflow revision, for the commission job and, under follow-up 3, for each seat job. 049 already requires the governed revision to be the run's own checkout HEAD (W0, `governed_revision_not_head`). The consumer reads the governed tip at admission. Both oracles model the ruled option ([R8](#r8--environment-oracles-make-authority-facts-and-heads-testable)), and the `rule_revision_ungoverned`, `rule_superseded` and `workflow_revision_ungoverned` vectors are authored in Phases 2 and 5.

**Trace.** FR-003; D1, D2, D4; 049 T010, T023; 025 FR-002.

## R8 — Environment oracles make authority, facts and heads testable

**Decision.** A vector carries an `environment` block. Each implementation's corpus adapter must inject it into its own lookups, never reading live systems during a corpus run:

| Oracle | Answers |
|---|---|
| `governed_history` | For each `(repository, revision)`: whether the revision is on the governed branch's first-parent history, and which governed revisions it is at or after |
| `governed` | For each `(repository, revision, path)`: whether it is available, whether it is an admitted governed source, its SHA-256 (a file) or its entries (a listing), and the same value at the governed tip |
| `governed_repositories` | The allowlisted governed repositories, in current spelling, checked before any `governed_history` read |
| `rules` | The neutral projection derived from the governed sources at a revision |
| `facts` | The authoritative facts for each fact source |
| `live_heads` | The head of each `(repository, pull_number)`, or `unavailable` |
| `head_refs` | The head ref of each `(repository, pull_number)`, as the trusted gather or the consumer read it |
| `resolved_candidate` | The consumer's own resolution of the candidate, for admission |
| `issued` | The issued challenges, registered keys, consumed challenges, accepted returns and live snapshots, as of `evaluation_time` |
| `identity` | The verified claims, whether they were verified, and the principal. Broker capability is the binding's own `broker` member, not an oracle |
| `repository_identity` | Required on every vector that reads the identity map: the text of the corpus's frozen identity fixture, or an `absent` or `unreadable` state that makes `repository_identity_unavailable` probeable |
| `registry_status` | An override of E1 statuses, required on every vector whose outcome reads a status |

No oracle models 025's council and mix guard or its touched-object and base-branch guards (E2 steps A2 and A5): they judge consumer-held state, keep 025's own codes, and run as passing seams during a corpus run ([data-model E2](data-model.md#e2-commission-record-council-conveningschemayaml-phase-2)).

The trusted trigger's expected candidate is an input, `inputs.expected_candidate`, not an oracle, because the producer receives it from its trigger.

**The identity map in vectors is a frozen corpus fixture, not the live file** (round 7, R7-M1). `conformance/fixtures/repository-identity.json` holds a fixed map text with the rows the vectors need. It is indexed with its digest, and carried verbatim in every map-reading vector. The generator, and so `generate --check`, never reads `contracts/policies/repository-identity.yaml`. The reasons:

- The live map is a shared estate file that other changes edit; the open `adopt-medxsoft-repository-identity` change is one.
- A corpus that tracked it would fail its own `generate --check`, in the required pytest suite, on another lane's PR. It would also move this family's corpus digest, and after Phase 7 its manifest row, from a PR that is not this family's.
- The corpus tests the binding mechanism over a fixed map. The live map's form is checked by its own validator, and a real binding is checked against the live map at the consumer's pin by `check`.

The cost is that the corpus does not show that the live map's rows match the fixture's. Nothing in the corpus depends on that, because a vector's outcome is fixed by the map it carries ([conformance-corpus § The frozen identity fixture](contracts/conformance-corpus.md#the-frozen-identity-fixture)).

**Rationale.**

- Race, authority and staleness refusals can only be shared vectors if their inputs are data.
- The hermes-runtime fixtures already fix an `evaluation_time` per case.
- 049's tests already inject `fetch`, `live_head` and `governed_root`, and its W0 work added the expected candidate.
- A required `registry_status` keeps every status-reading vector's outcome fixed when Phases 7 and 8 flip the registry, so the corpus digest does not move at either cut.
- Trace: FR-004, FR-010, SC-001; spec edge cases (head drift before and after the POST, changing totals, an immutable rule that is accessible but unauthorized).

**Alternatives.** Live fixtures against real repositories: not reproducible, and network-dependent. Rejected.

## R9 — Fact authenticity, unused facts and secrets

**Decision.** Facts are checked as follows ([data-model E2](data-model.md#e2-commission-record-council-conveningschemayaml-phase-2), steps 3, 9 and 10):

| Check | Refusal |
|---|---|
| A fact source kind not allowed for its contract, or a governed path not listed among the sources | `fact_source_mismatch` |
| A fact a condition reads is absent from `consumed_facts` | `opaque_conclusion` |
| A consumed fact no condition reads | `facts_unused` |
| The authoritative fact set lacks a read fact, or fails completeness | `condition_unevaluable` |
| A consumed fact differs from the authoritative value | `consumed_facts_mismatch` |

The **secret detector floor** is the provider's existing `SECRET_PATTERNS` (`scripts/validate-domain-factory.py`), loaded by `importlib`, never copied. It is applied, before any oracle read, to every string in `packet_refs`, `class_inputs`, `parameters` and `consumed_facts`; a match refuses as `secret_bearing_fact`. An implementation may detect more, but it must refuse every corpus secret vector and accept every positive one.

**The floor and 049 differ, and both gaps are recorded.**

- The floor lacks four patterns 049 detects: the PKCS#8 `BEGIN PRIVATE KEY` header (the form an Ed25519 key takes), `github_pat_`, `xox?-` tokens and `Bearer` credentials.
- 049 lacks the floor's `(password|passwd|secret|token)` assignment detector. 049 T009/T010 must add it, because the corpus refuses it ([provider-interface § Consumer impacts](contracts/provider-interface.md#consumer-impacts-recorded-by-this-plan)).
- Widening the floor changes what every domain-factory scan refuses, so this feature does not do it in passing. Phase 2's T033 measures whether the four patterns would flag any tracked file and files the widening as its own governed follow-up. Until that lands, the family's secret vectors cover the floor exactly.

Secret-shaped corpus values are stored as a `{"$parts": [...]}` join sentinel. Every adapter concatenates it before any other step, so no corpus file matches a detector when the provider's own `scan_secrets` sweeps `.json` files.

**Rationale.**

- D1 refuses "unused inputs and secrets" and requires "normalized facts actually consumed".
- A second detector list would be a second vocabulary.
- 049's CI was failed once by its own literal secret-shaped vectors and fixed by building them from parts (049 evidence, the `f0064e95` CI round).
- Trace: FR-002, FR-003; 049 T009/T010; 025 FR-003.

## R10 — Protocol and signing-context identifiers, and classification

**Decision.** The values below become normative when the Phase 1 registry lands.

| Identifier | Value | Status |
|---|---|---|
| Replacement protocol | `xfc-resolved-council-1` | `available` (dormant) until the major; `admission_eligible` at the major |
| Registration context | `xfc-resolved-council-1/seat-key-registration` | the replacement's |
| Return context | `xfc-resolved-council-1/seat-return` | the replacement's |
| Legacy protocol entry | `xfactory-council-seat-return/v1` | `in_use` until the minor; `deprecated` at the minor; `historical_only` at the major |
| Legacy key-authorization context | `xfactory-council-seat-key-authorization/v1` | recognized for classification only |

The legacy entry is **identification only**. Classification applies to the protocol-carrying record kinds (E2 and E4–E8) and to records with no family `kind`. It runs in Phase 1, before any other check at every boundary over such a record ([data-model E1](data-model.md#e1-protocol-registry-and-classification-protocol-registryschemayaml--protocolregistryyaml-phase-1)):

1. A record carrying `protocol: xfc-resolved-council-1` is a replacement record, whatever else it carries. Root-authorization members on it are refused as `root_authorization_refused`; they never make it legacy.
2. A record carrying the legacy protocol identifier is legacy; any other `protocol` value is `protocol_unknown`.
3. A record with no `protocol` is legacy when a recognition rule matches: a convening block without `required_seats`, a context string in the legacy set, or a registration carrying root-authorization members. Otherwise it is `protocol_unknown`.

**What follows from classification depends on the side's selected protocol**, never on shape alone. A legacy record presented under a replacement selection is refused (`legacy_protocol_refused`). Under a legacy selection, or offline, a legacy record is **routed**. Routing means this family gives no verdict: the validator exits 3, which is never a pass, and the legacy verifier (Hermes 015 and its golden vectors) remains the only verifier of legacy bytes.

**Rationale.**

- D1 requires an "explicit protocol identifier".
- D3 requires "a distinct versioned signing context to prevent cross-protocol replay".
- D5 requires that the binding "never guesses from payload shape", and that "Separate versioned endpoints during a deprecation release do not confer dual-protocol acceptance on the active replacement binding".
- Principle VII requires that deferred features "fail closed rather than degrade open". A family that does not own the legacy shape cannot pass it, so it routes it.
- The spec delta, requirement 5, says root-authorization payloads "MUST refuse under the replacement protocol".
- The `xfc-…-1` form follows `xfc-jcs-sha256-1`.
- Trace: FR-001, FR-008, FR-011; 049 T020, T026→T030, T027; 025 FR-010, FR-011.

**Alternatives.**

- `…/v2` under the legacy strings: reads as a revision of the root-authorized protocol, which it is not. Rejected.
- Codify the legacy shapes as a provider schema: the provider would take ownership of a protocol it never published, only to remove it. Rejected.
- Accept legacy records as "in use" with no finding: passes bytes nothing verified. Rejected (analysis C3).

## R11 — Return payload admissibility and decimal quantities

**Decision.** `return_digest` is the `xfc-jcs-sha256-1` digest, subject `council_seat_return_payload`, of the seat's return payload. The payload is the seat's **whole checked return entry**: the content 049's `entry_digest` covers today, the posted block plus the floor fields. A partial payload would leave signed-looking content outside the signature.

The payload must be admissible under the construction: no non-integer number, no integer outside ±(2^53 − 1), no unpaired surrogate. A payload that is not admissible is refused as `value_not_canonicalizable`. **A non-integer quantity is written as a `decimal_string`**: a plain decimal with no exponent, no `+`, no leading zero and no trailing fractional zero ([data-model § Shared definitions](data-model.md#shared-definitions-shared-definitionsschemayaml-phase-1)). The payload's member set stays domain- and consumer-agreed, and verdict semantics are Hermes's existing ones.

**Consumer impact.** 049's seat entry carries `model_usage.costUSD` as a float, and its cost floor reads it. To sign under this contract, 049 T020 writes each such value as a `decimal_string`, converting the float's shortest round-trip form without an exponent, and the floor reads the string. 025 compares the strings it receives and never parses them as floats. This is forced by D1 ("do not mint another canonicalization"); it is recorded here and in [provider-interface](contracts/provider-interface.md#consumer-impacts-recorded-by-this-plan) so T020 is not surprised.

**Alternatives.**

- Integer minor units: they fix a scale that a cost reported to more decimal places would overflow or round. Rejected.
- A raw-bytes digest over the serialized payload: it makes the digest depend on one serializer's bytes, which is a second construction in effect. Rejected.
- Exempting floats: reintroduces the cross-implementation number disagreement the construction refuses on purpose. Rejected.

## R12 — Lifetime ceilings

**Decision (ruled).** Brett Heap ruled OPEN-1 on 2026-10-08: "600 s challenge, 6 h assignment (Recommended)". These are contract maximums. The consumer may configure a tighter value, and that value applies when it **issues** an assignment or a challenge. Verification and the corpus use the contract ceiling, so a consumer with a tighter value still accepts a vector at the ceiling and still refuses one second above it.

- An assignment carries `not_before` and `expires_at`. Its lifetime must be greater than 0 and at most **21600 seconds**; otherwise `assignment_malformed`.
- A challenge carries `issued_at` and `expires_at`. Its lifetime must be greater than 0 and at most **600 seconds**; otherwise `challenge_malformed`.
- Both are ISO 8601 UTC instants with seconds precision and a `Z` suffix.
- Expiry is refused at the instant and after it (`assignment_expired`, `challenge_expired`), measured against the vector's `evaluation_time`.

**Why these values.**

- A challenge is consumed within seconds of issue, at the seat job's first step.
- An assignment must outlive runner queueing plus the seat job's 30-minute timeout (049 W1).
- A convening whose assignments expire fails and may be convened again, because once-per-pin counts only convenings that did not fail.
- 049's internal pre-check currently bounds challenges at 3600 seconds. That is a producer-side pre-check, not issuance, so it needs no change. A challenge issued under this contract never exceeds 600 seconds. The challenge-ceiling vectors therefore carry `applies_to: [consumer]`, because the consumer issues challenges; 049 may tighten its pre-check to 600 seconds, but conformance does not require it.

**Vectors at the ceilings.** Each boundary gets an accept at exactly the ceiling, a refusal one second above it, and refusals at zero and at a negative lifetime: 21600 and 21601 seconds for assignments (Phase 3), and 600 and 601 seconds for challenges (Phase 4).

**Trace.** FR-007; D3; 049 T019/T020; 025 FR-009.

## R13 — Producer workflow binding and its placement

**Decision (ruled for placement).** Brett Heap ruled OPEN-2 on 2026-10-08: "Consumer's runtime config (Recommended)". The concrete instance is written into the consumer's governed runtime configuration at the provisioning act (049 T031; 025 H3 "runtime-held configuration"; D4 "Identity provisioning is an operator act"). It is validated with `validate-council-convening.py check` at the consumer's pin. The provider ships only the schema, a `.template.yaml` stub, the derivation from `repository-identity.yaml` and the corpus. The provider stays the only source of repository spelling.

**The schema** (`producer-binding.schema.yaml`, closed) holds:

- **The issuer**, for principal kind `github_oidc_job`: exactly `https://token.actions.githubusercontent.com`, or that URL followed by `/<enterprise-slug>`. That is GitHub's documented issuer form for an enterprise with a unique issuer URL.
- **The repository identity.** `caller_repository` is the repository the commission or seat job runs in: the verified token's `repository` claim, which for a reusable workflow is the caller. It is named for the caller so it is not confused with the ruling's "producer repository", which is the repository in `job_workflow_ref` ([R7](#r7--governed-sources-rule-authority-and-revision-currency)). `contracts/policies/repository-identity.yaml` is read through the existing `load_transfers` reader (`scripts/estate_inventory.py`). That reader returns an empty map when the file is absent or unreadable, and lists malformed rows separately, so this family fails closed on all three: `repository_identity_unavailable`. A spelling the map lists as `former` is refused as `repository_identity_former`, and so is a non-canonical case variant, defined mechanically as a spelling equal to a listed spelling when ASCII case is ignored but not byte-equal to it (the map's `owner_case` is prose). Any other spelling is taken as current; the map has one transfer row today. `repository_id` is the immutable numeric identity. A verified `repository` or `repository_id` claim that differs from the binding is `repository_identity_mismatch`.
- **The claims.** `audience` is a literal, never a pattern. `subject_claim_keys` and `subject_template` name the actual verified OIDC `sub` template, including a template customized through GitHub's documented subject claim keys. The closed key set is enumerated at T053 from GitHub's OIDC reference, which T053 cites. `permitted_workflows` lists `{operation, job_workflow_ref, workflow_revision_rule}`. The rule is `equals_governed_revision` for the commission job, under the OPEN-3 ruling ([R7](#r7--governed-sources-rule-authority-and-revision-currency)), and `on_governed_history_since_revision` for a seat job, under follow-up 3, "At or after the frozen rev (Recommended)". A seat runs after admission, when `main` may have moved, so the seat value applies the ruling's "history" half. The binding carries a `binding_id`, which an assignment's `holder.binding_ref` names, so registration checks a seat job's claims against its own binding (data-model E7 step 5).
- **The broker**: its reference, whether its capability is verified, and the evidence.

The rules:

| Rule | Refusal |
|---|---|
| `job_workflow_ref` and `sub` are different fields, judged by meaning: a template that is a bare workflow reference, checked before the parse | `subject_workflow_conflation` |
| Permitted workflows are matched against the verified `job_workflow_ref`, never against `sub`; a vector whose `sub` contains a permitted reference while `job_workflow_ref` names an unlisted workflow shows it | `workflow_not_permitted` |
| The template does not parse, or its `repo` or `repository_id` element names another repository, or the verified `sub` is not the template | `subject_template_mismatch` |
| A wildcard in any member | `binding_wildcard` |
| A claim taken from a decoded assertion whose signature was not verified | `claims_unverified` |
| The verified token is outside its validity window at `evaluation_time` (`exp` at or before it, or `nbf` after it) | `claims_expired` |
| The verified `iss` is not the binding's issuer | `issuer_mismatch` |
| The verified `aud` is not exactly the binding's audience | `audience_mismatch` |
| The identity map is absent, unreadable, or has a malformed row | `repository_identity_unavailable` |
| A former spelling, or a non-canonical case variant, of the caller repository or of the repository in a permitted `job_workflow_ref` | `repository_identity_former` |
| A broker whose capability is not verified | recorded at binding; refused at `activation` and `resume` (data-model E12): `broker_capability_insufficient` |

`principal_kind` is one closed enumeration in the shared definitions, `github_oidc_job` or `governed_broker_job`, used by both the binding and the assignment holder. The holder's `principal_ref` and `binding_ref` are issued by the trusted dispatcher or the owner-provisioned broker from verified execution evidence (D3). This family binds them and checks them at use; it does not derive them.

The template `producer-binding.template.yaml` carries an `instantiation_stub` marker and no live values.

**Rationale.**

- D4: "Bindings must name the actual verified subject template and workflow/job claims". A substring rule against `.github/workflows/` would refuse GitHub's documented customization, which is the strongest reusable-workflow binding.
- D4: "No unverified JWT decoding, alternate former-owner spelling, configuration wildcard or silent environment-only substitute is accepted."
- D4: "if the chosen provider cannot enforce it, activation parks until the broker enforces the full binding".
- Trace: FR-009; D3, D4; 049 T023, T024, T031; 025 FR-008.

**Alternatives.** Provider-published instances under `contracts/council-convening/`: put to Brett Heap as OPEN-2 option (b), and not chosen. It would make the neutral repository a holder of one domain's authority configuration, and every audience or subject-template change a provider contract cut.

## R14 — Protocol registry, selection, deprecation and historical classification

**Decision.** The protocol registry is closed. A `protocol_selection` record is each side's governed configuration shape: `{side, mode, protocol, provider_commit, provider_bundle, corpus_index_sha256}`. `mode` is `rehearsal` or `active`. A `null` bundle is legal only in rehearsal, and an active replacement selection needs the replacement's `admission_eligible` status. Two sides match only when `mode`, `protocol`, `provider_commit`, `provider_bundle` and `corpus_index_sha256` are all equal; otherwise the refusal is `pair_mismatched`.

The rules for selection and history:

- A refusal under the selected protocol never selects another protocol (`rejected_without_fallback`). A vector shows it with two inputs: `inputs.rejected_under`, the `protocol_id` a refusal was recorded under, and `inputs.selection_attempt`, a later selection that names another protocol.
- A legacy record under a replacement selection is always refused (`legacy_protocol_refused`), at every status. The active replacement binding never accepts both shapes.
- Under a legacy selection, a legacy record is routed to the legacy verifier. While the legacy status is `deprecated`, the route also carries the finding `legacy_protocol_deprecated`; `--strict` promotes it to an error. Once the status is `historical_only`, any legacy selection is itself refused, in either mode.
- In `--historical` mode a record is classified by its recorded protocol and never reinterpreted. Legacy records are routed (exit 3). Replacement records stay verifiable under the replacement rules at every later release.

`activation_evidence` records each owner act of the runbook (pause, drain, switch, rehearsal, activation, rollback and resume), with per-act required members ([data-model E12](data-model.md#e12-activation-evidence-activation-evidenceschemayaml-phase-6)). An activation or resume needs a passing matched rehearsal and verified broker capability. Broker capability has one source of truth, each binding's `broker` member: the record names the bindings it activates (`binding_refs`), and E12 reads their `broker` members, so an activation record cannot claim a capability its bindings lack. A rollback needs neither, because a broker failure may be what caused it. The validator refuses a record missing any member its act requires (`activation_evidence_incomplete`).

*Clarified 2026-10-09, on Brett Heap's ruling of 2026-10-09T13:22:16Z, "Back to Release A pins (Recommended)" (opensoft/brett-wip `lanes/log/codeXfactory-2.md`, RULED line 259).* A paired rollback after activation returns both sides to their Release A (Phase 7) pins and reselects legacy there, where the legacy protocol is still `deprecated` and selectable. The new records are kept as audit evidence. That is D5's "restores both prior versions/configurations together". It matches the consumer's own rollback, which returns its image to the Phase 7 pin. A legacy selection at the removal major's pin stays refused, so a rollback never restores legacy there ([data-model E11, E12](data-model.md#e12-activation-evidence-activation-evidenceschemayaml-phase-6)).

**Rationale.**

- D5 requires that "The active binding selects exactly one protocol ... never guesses from payload shape or falls back".
- D5 also requires that "Historical records retain their original protocol".
- H4 reads "one declared protocol and exact provider compatibility pin from governed configuration".
- § Change Classes, *Deprecating (minor)*: "the conformance validator emits warnings but still accepts it". Here the deprecated shape is never accepted by this family: it is routed to the verifier that still accepts it, with the warning.
- Trace: FR-011, FR-012, SC-004; 049 T026–T030, T032; 025 FR-011, FR-012.

**Alternatives.** Selector symbols only, as 049 T026 does internally: those cannot show that a pair matches on the provider pin and corpus. Rejected for the shared shape; the producer maps its symbols at T030.

## R15 — Release-surface membership

**Decision (ruled).** Brett Heap ruled OPEN-4 on 2026-10-08: "Join behind a version floor (Recommended)". `contracts/council-convening/`, its validator, package and tests join the release digest inventory behind a floor-gated block in `scripts/hermes_runtime_validation/release.py`, `COUNCIL_CONVENING_RELEASE_FLOOR`, set to the version allocated at the Phase 7 cut.

**Rationale.**

- This follows the clearing precedent: openxFactory #722 treated a family's absence from the inventory as a defect, and Brett Heap ruled the floor form for clearing in #745.
- Inventories already published keep verifying, because below the floor no family path is a member.
- The corpus's per-file digests then travel in the inventory that consumers already verify.
- The corpus digest consumers pin is still the manifest row's SHA-256 of `conformance/index.json`, whose rows pin every vector's bytes ([R16](#r16--the-corpus-digest-and-coverage)).
- Trace: FR-010, FR-012; D5 ("regenerates manifest/changelog/inventory from the actual candidate"); 049 T003, T030.

**Alternatives.** Identity by manifest-row SHA-256 only, as 028 research R6 did for a new family and `signed-execution-chain` still does: put to Brett Heap as OPEN-4 option (b), and not chosen.

## R16 — The corpus digest and coverage

**Decision.** `conformance/index.json` lists every vector with its path and `sha256:` over its raw bytes, plus the counts per area and outcome. The validator enforces closure in both directions:

- every file under `conformance/` is indexed, except the index itself;
- every row's file exists;
- every digest matches;
- rows are in bytewise UTF-8 path order.

**Coverage is scoped to the commit**, so every phase's PR is self-consistent:

- every code in the `refusal_code` enumeration at that commit is some vector's expected refusal;
- every code in the `finding_code` enumeration at that commit appears in some vector's expected `findings` list;
- every requirement in the index's `coverage_floor` is cited by some vector. Each phase raises the floor to the requirements it serves, and from Phase 6 the floor is the full FR-001–FR-012 and SC-001–SC-003, which a test asserts;
- every vector whose outcome reads a registry status carries `registry_status`.

**Known answers from outside the code.** The `derived` values are generated, so a canonicalization bug shared by the generator and the adjudicator would go unseen. Two guards apply:

- A vector marks hand-authored known answers with `derived_origin: hand`. The foundation known answers are hand-authored.
- One known answer comes from RFC 8785 itself. It is the RFC's own example object with its `numbers` member removed, because the construction refuses non-integer numbers. Its canonical bytes are taken from the RFC text.

The **corpus digest** is the manifest row `sha256` of `conformance/index.json`, registered at the Phase 7 cut. A consumer pins `{openxFactory commit, index sha256}`, and the index transitively pins every vector.

**Rationale.**

- Per-file hashes are "plain algorithm-tagged SHA-256 over the file's BYTES" (the clearing family's ratified rule).
- One digest gives consumers a single value to pin and compare during the matched rehearsal.
- Coverage of the whole vocabulary at a commit where half of it has no boundary yet would make every early PR red, so coverage follows the vocabulary as landed.
- Trace: FR-010; Risks ("exact corpus digest/pin"); 049 T003, T013; 025 FR-001.

**Alternatives.** An `xfc-jcs-sha256-1` subject over the index's parsed value: a file is bytes, and the existing rule for files is raw SHA-256. Rejected.

## R17 — CI gate and the pytest-suite pin

**Decision.** Add `.github/workflows/council-convening-gate.yml`.

- Its job id is `council-convening-gate`, with no `name:` key.
- It runs on `pull_request` and on `push` to `main`, as `clearing-dispatch-gate.yml` does.
- It ends with a positive assertion step that greps for the validator's proof-of-work notes. The asserted set grows by phase: the predicate-registry note joins in Phase 2, when the registry lands ([contracts/validator-cli.md](contracts/validator-cli.md#proof-of-work-notes-asserted-by-the-ci-gate)).
- It reports and does not gate until the owner makes it required.

The check that no feature commit touches `governance/review-authority/` or `openXwallet/` is a per-PR check against the PR's own merge base (`git diff --name-only origin/main...HEAD`), run in the quickstart, not a repository test, because a repository test has no stable base once phases merge.

**Rationale.**

- This is the house gate form (`clearing-dispatch-gate.yml`): a display name silently de-advises a required check, and "a green check that walked nothing is a vacuous pass".
- The tests need no submodule and no network, and `cryptography` comes from the lock `pytest-suite` already installs. So `EXPECT_SKIPPED` does not move, and the `MIN_*` floors only rise.
- Trace: Principle V; FR-010.

## R18 — Fixture keys and reproducible signatures

**Decision.** `scripts/council_convening/generate.py` derives each fixture's Ed25519 seed from a **labelled** SHA-256 of a fixed, public phrase naming it a council-convening corpus test key. It signs with `cryptography`, and writes only public keys, signatures and signed-bytes known answers into vectors.

- No seed or private key is written to any file. A test refuses any corpus member named `seed`, `private_key`, `secret_key`, `sk` or `d`, at any depth. It keys on member names, because every SHA-256 digest is also 32 bytes.
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
- the family joins the release inventory behind `COUNCIL_CONVENING_RELEASE_FLOOR`, under the OPEN-4 ruling;
- the cut adds a `contracts/CHANGELOG.md` entry, a `docs/contract-versioning-policy.md` § *Deprecations Currently In Force* entry written from the refusal list, the manifest rows, the release inventory, and the registration of the `contracts/README.md` and `README.md` rows that Phase 1 added as pending;
- the cut runs the supported-domain regression denominator.

**Phase 8 — the major.** Cut only after all four of:

- (a) the minor's tag is published and verified;
- (b) at least one full minor has served;
- (c) both successors' dormant implementations are verified against the published minor (D5 Migration Plan);
- (d) the owner's release act.

The major flips the registry statuses, writes the CHANGELOG migration note and § *Deprecations Executed*, refreshes the manifest rows of every file it changes, and re-baselines the denominator against the actual union. It must also process every other § *Deprecations Currently In Force* entry that targets the version it becomes. **Three** entries now target `contract-v5.0`, as the policy itself says ("Those three name `contract-v5.0` now"):

- the flat `hermes` keys;
- the undeclared credential `consumer:` block;
- a `requirement_ref` that resolves to nothing or to more than one requirement.

Each is restated again under its own pre-authorized text unless its acts are ready. Phase 8 does not decide those acts.

**Per-file schema versions do not move at the major.** Phase 8 changes instance data (the registry statuses and tags) and validator behavior, not the shape of any schema: every status was in the schema's enumeration from Phase 1. So every family file's `contract_schema_version` stays `1`, and the break is carried by the bundle major, the per-file `sha256` and the CHANGELOG migration note. The policy's own precedent is the ideation-dashboard removal at `contract-v3.0`, whose file "deliberately STAYS `1`" for the same reason (`docs/contract-versioning-policy.md`, § *Deprecations Executed*).

Both cuts claim the contract-cut shared substrate on openxFactory's pinned "Shared substrates — claims" issue (lane protocol Amendment 1, rule 7). Each allocates the next available version from the manifest at that moment, merging `origin/main` first (Bundle Realization Order step 1). Each tag is the owner's act (change task 3.2; precedent: `contract-v4.0` ASK-9a, "the annotated tag is Brett's act").

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

## R21 — Normative evaluation order

**Decision.** Every boundary has one normative evaluation order, and the first failing check names the outcome. The orders are in [data-model.md](data-model.md): commission and admission (E2), the snapshot half of admission (E4), registration (E7), return and completion (E8), binding (E10), selection (E11) and activation (E12). Every order over a protocol-carrying record begins with classification (E1). The binding, selection and activation orders are over records judged by kind, and completion is over frozen state. At admission the order is: classification and shape (E2 steps 1 and 2); binding (A1); 025's council and mix guard (A2); retry identity and once-per-pin (A3); the shared checks, with the workflow-revision step of binding (A4) only after E2 step 5 has checked the `governed` member it reads; the live head (step 13, 025's `verify_subject_pin`); and last 025's touched-object and base-branch guards (A5). That keeps 025's retained guards (025 FR-004) in the order Hermes runs them today (`council_orchestration.py`). Every vector names exactly one expected code, with no "or", and multi-defect vectors pin the order: one record with two defects must yield the earlier code.

Four ordering rules matter most:

- **Classification first.** A legacy record is classified before any replacement shape check runs, so it is never called malformed.
- **Secrets before any oracle is queried with a free-text value.** A secret-bearing record is refused before any oracle is queried with a string the secret scan covers. The admission steps before it (A1 to A3) consult oracles only by grammar-checked identifiers: the verified claims, the council, and the convening key. An identical retry equals a record that already passed the scan. The precedence is stated, not hidden: a secret-bearing record that conflicts with a live key is refused `convening_conflict` at A3, not `secret_bearing_fact`, and either way nothing is written and no free-text value reaches an oracle.
- **Retry identity before drift.** At admission, retry identity (E2 step A3) runs after classification, shape and binding, and before every check that reads something that can drift: governed sources, facts and the live head. A producer whose response was lost may resend after the tip or the head moved, and still gets the same snapshot back (US1 scenario 4; 025 FR-006). Once-per-pin runs in the same step and only after the identical-retry test, so it never pre-empts an identical retry.
- **The live head last among reads of the candidate.** The producer's closing head read is the last read before submission (049 W0). The consumer's head check (E2 step 13) is its last read of the candidate's head. Only 025's touched-object and base-branch guards follow it (A5), and they read immutable objects at the verified head plus the base branch's rules.

Schemas check types only where a named semantic refusal exists for the same condition, so a schema failure never shadows a semantic code.

**Rationale.**

- SC-001 says negative vectors "must agree on refusal". Two implementations can agree on a code only if they agree on which check runs first.
- D2 says admission "validates the ordered roster and candidate head before creating the convening".
- 049's own order (shape, candidate identity, governed revision, resolution, then the live head) is preserved in substance. Where 049's current order differs in detail, T010 reorders it.
- Trace: FR-002–FR-004, SC-001; 049 T009, T010; 025 FR-002–FR-005.

**Alternatives.** Accept any refusal for a negative vector: that measures only that both sides refused, which SC-001 rejects. Rejected.
