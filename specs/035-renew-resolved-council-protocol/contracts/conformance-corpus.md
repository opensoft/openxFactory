# Conformance corpus format and adapter contract

**Feature**: [spec.md](../spec.md) · **Plan**: [plan.md](../plan.md) · **Research**: R1, R2, R8, R9, R16, R18, R21

The corpus is `contracts/council-convening/conformance/`. It is shared by three independent implementations:

- the provider reference implementation, which adjudicates every vector in CI;
- the producer, 049;
- the consumer, 025.

## Files

- `conformance/index.json` holds the index.
- `conformance/vectors/<area>/<case_id>.json` holds one vector per case. The area is one of `foundation` (Phase 1), `resolution` (Phase 2), `assignment` (Phase 3), `signing` (Phase 4), `binding` (Phase 5) and `migration` (Phase 6). Each area directory is created together with its first vector, so the tree never holds an empty directory or a placeholder file.

Every file is JSON (RFC 8259): UTF-8 with no byte-order mark, LF line endings, a single trailing newline, a closed object at every depth, and `schema_version: 1` plus `kind`. The generator writes members in sorted order with two-space indentation, so regeneration is byte-identical (R18).

## Index (`kind: openxfactory-council-convening-conformance-index`)

| Member | Content |
|---|---|
| `corpus_id` | `council-convening-conformance` |
| `protocol` | `xfc-resolved-council-1` |
| `coverage_floor` | The requirement identifiers that must be cited at this commit. Each phase raises it; from Phase 6 it is the full FR-001–FR-012 and SC-001–SC-003. |
| `cases` | Rows in bytewise UTF-8 order of `path`: `{case_id, area, boundary, applies_to, requirement_ids, path, sha256, expected}` |
| `totals` | Counts by `area`, by `expected.outcome`, and of rows whose `applies_to` names both sides |

Closure holds in both directions:

- every file under `conformance/` except `index.json` is a row;
- every row's file exists;
- every `sha256` (`sha256:` + 64 hex over raw bytes) matches;
- every `case_id` is unique and equals its file's basename.

Coverage is checked against the vocabulary **as landed at the commit** (R16):

- every `refusal_code` member is some row's `expected.refusal`;
- every `finding_code` member appears in some row's `expected.findings`;
- every `coverage_floor` requirement appears in some row's `requirement_ids`. SC-004 is an operational rehearsal: the corpus carries its rehearsal-record shape vectors under `migration`, but the rehearsal itself is not a corpus act;
- every vector whose outcome reads a registry status carries `environment.registry_status`.

## Vector (`kind: openxfactory-council-convening-conformance-vector`)

| Member | Content |
|---|---|
| `case_id` | Equals the index row. |
| `area`, `boundary` | `boundary` is one of `definition`, `classification`, `commission`, `admission`, `registration`, `return`, `completion`, `binding`, `selection`, `activation`, `historical`. Challenge issuance has no boundary of its own: an issued challenge is checked against E6 when a registration uses it (data-model E7, step 6). |
| `applies_to` | A non-empty subset of `[producer, consumer]`. The provider reference implementation runs every vector. |
| `requirement_ids` | The FR and SC identifiers the case probes. |
| `evaluation_time` | A `utc_instant`. Every expiry and lifetime check uses it, never the wall clock. |
| `inputs` | The record or records under test, keyed by role: for example `record`, `snapshot`, `registration`, `return`, `returns`, `binding`, `bindings` (the E10 instances an assignment's `holder.binding_ref`, or an activation's `binding_refs`, resolves against), `operation`, `selection_producer`, `selection_consumer`, and `rehearsal` (the exact UTF-8 text, as a JSON string, of the record an activation's `rehearsal_ref` names; the hash is over those bytes). Also `selected_protocol` (a registry `protocol_id`, or `null` for offline) on every boundary that classifies; `expected_candidate` at commission, holding only the members the trusted trigger names; and, at `selection`, `rejected_under` (the `protocol_id` a refusal was recorded under) with `selection_attempt` (a later selection), which together give `rejected_without_fallback` its input. For `definition`: `{definition, value}`. Issued challenges are not inputs: they are `environment.issued.challenges`, because the consumer issued them. |
| `environment` | The oracle data (below). Members a boundary does not use are absent, not empty. The one exception is a shared commission vector's tip values, which it always carries (§ How each side runs a shared vector). |
| `expected` | `{outcome: accept \| refuse \| route, refusal: <refusal_code> \| null, findings: [<finding_code>, ...], derived: {...}, derived_origin: hand \| generated}`. `findings` is ordered, and empty except on a route. |

`derived` holds known answers, so implementations compare more than a verdict:

- for `classification`: the classification (`replacement` or `legacy`);
- for `accept` at commission or admission: `required_seats` and `convening_digest`;
- for signing vectors: `signed_bytes` (unpadded base64url) and `key_fingerprint`.

`derived_origin: hand` marks a known answer authored by hand rather than by the generator. The foundation known answers are hand-authored, and one of them is taken from RFC 8785 itself (R16), so a canonicalization bug shared by the generator and the adjudicator cannot pass unseen.

### How each side runs a shared vector

A shared vector carries `applies_to: [producer, consumer]`. Every shared resolution vector uses boundary `commission`, and a consumer runs it through the same resolution its admission uses, so it must be runnable by both sides without either side's private inputs:

- it carries both `inputs.expected_candidate`, which the producer compares, and an `environment.resolved_candidate` consistent with it, which the consumer compares;
- its `live_heads` entry is a single read, so the producer's recheck and the consumer's one read see the same head;
- its `governed` oracle carries `tip_sha256` or `tip_entries` for every source, equal to the value at the revision. The consumer's admission-time tip comparison (`rule_superseded`) therefore runs and passes, and the producer may ignore the tip values. An adapter that needs a tip value and finds none fails the vector as a harness error; it never skips the check;
- it carries no binding, so the consumer runs it without E2 steps A1 and A4, which need a verified commission token and so belong to `admission` vectors;
- it carries no `rule_superseded` case and none of the consumer's admission-only steps (A1 to A5).

A producer runs it at commission. A consumer runs E2 steps 1 to 13 over it, with the record as the submitted record.

**What no vector covers.** E2 steps A2 and A5 are 025's own guards over consumer-held state the corpus does not model (data-model E2). A consumer's adapter runs them as seams that pass during every corpus run, shared and consumer-only admission vectors alike, so no vector carries an input for them. The provider reference implementation has no such steps, and no vector's `expected` depends on them. Both must reach the vector's `expected`. Vectors that need more than one head read, a binding, a retry against live snapshots, or the governed tip are `applies_to: [producer]` or `applies_to: [consumer]`.

## Environment oracles

An adapter must inject these and must not consult a live system during a corpus run (R8):

| Oracle | Key | Value |
|---|---|---|
| `governed_history` | `<repository>@<revision>` | `{on_first_parent: bool, at_or_after: [<revision>, ...]}`: whether the revision is on the governed branch's first-parent history, and the governed revisions it is at or after (the seat rule, data-model E10). |
| `governed` | `<repository>@<revision>:<path>` | `{available, governed, sha256 \| entries, tip_sha256 \| tip_entries}`: a file's SHA-256, or a listing's sorted entries, at the revision and at the governed tip when the check runs. At admission a difference is `rule_superseded`, under the OPEN-3 ruling and its follow-up 1, "Every governed source (Recommended)". At commission the comparison is a non-normative producer pre-check, so no shared commission vector carries a `rule_superseded` case. `governed` means an admitted governed source. |
| `governed_repositories` | — | The allowlisted governed repositories, each in its current spelling. `governed.repository` outside it is `rule_unauthorized`, checked before any `governed_history` read (data-model E2 step 5). |
| `rules` | `<repository>@<revision>` | `{councils: {<council_id>: {class_selector: [...], classes: {<class>: {standing_seats, conditions}}} \| {standing_seats, conditions}}, sources: [<path>, ...]}`: the neutral projection an adapter would derive from the governed sources, with each council classed or unclassed (data-model E3). |
| `facts` | `pr_facts:<repository>#<pull_number>@<head_sha>`, `rule_facts:<repository>@<head_sha>:<subject_path>` (a `candidate_subject` source) or `rule_facts:<repository>@<revision>:<path>` (a governed source) | The authoritative fact object for that source. |
| `live_heads` | `<repository>#<pull_number>` | A `full_sha` or `"unavailable"`. For commission vectors, a list read in order, so drift before and after the recheck is expressible. A shared commission vector has a single entry; a vector with more than one read is producer-only. |
| `head_refs` | `<repository>#<pull_number>` | The candidate's head ref, as the trusted gather read it (commission) or the consumer read it (admission). `class_inputs.head_ref` must equal it. |
| `resolved_candidate` | — | The consumer's own resolution of the candidate, compared at admission. |
| `issued` | — | `{challenges: [...], consumed_challenges: [...], registered_keys: [{assignment_id, key_fingerprint}], accepted_returns: [...], live_snapshots: [...]}` as of `evaluation_time`. |
| `identity` | — | `{verified: bool, claims: {...}, principal: {principal_kind, principal_ref}}`: the one home of verified claims. Decoded-only claims carry `verified: false`. Broker capability is the binding's own `broker` member, not an oracle. |
| `repository_identity` | — | **Required** on every vector whose boundary reads the identity map: `binding`, `registration`, and `admission` from Phase 5. One of three forms. `{"state": "text", "text": "<the map's exact UTF-8 text>"}`: the adapter writes it at `contracts/policies/repository-identity.yaml` under a temporary root and reads it with the same reader, so a text with a malformed row, or one that does not parse, is refused through the reader's own result, and a well-formed text with no transfer rows is a valid, empty map. `{"state": "absent"}`: no file. `{"state": "unreadable"}`: a file that cannot be read or decoded. The generator copies the `text` form from `contracts/policies/repository-identity.yaml` at generation, so the map a vector depends on is covered by that vector's own digest, and `generate --check` reports any drift between the two. A vector that reads the map without this oracle is malformed (`council-convening-vector-identity-map-missing`). |
| `registry_status` | — | An override of E1 statuses. **Required** on every vector whose outcome reads a status, so minor-time and major-time behavior are both vectors at one commit, and the registry flips at Phases 7 and 8 move no vector. |

## The `$parts` sentinel

Any string leaf may be written `{"$parts": ["..", ".."]}`. Before any other processing, adapters replace it with the concatenation of its parts. It exists so secret-shaped negative values never appear contiguously in a committed file, which the provider's own `scan_secrets` would flag (R9). It is the only object-valued leaf allowed where a schema expects a string. An object leaf anywhere else is a malformed record.

## Outcome semantics

- `accept`: no refusal, and every `derived` value matches.
- `refuse`: exactly the named code, which is the first failing check in the boundary's normative order ([data-model.md](../data-model.md); R21). A different refusal is a disagreement, even when it is also a refusal (SC-001: "negative vectors must agree on refusal").
- `route`: no verdict from this family; the record goes to the legacy verifier, with exactly the named findings in order: `[legacy_protocol_routed]`, or `[legacy_protocol_routed, legacy_protocol_deprecated]` while the legacy status is `deprecated`. A route is never a pass.

No outcome accepts a record with a finding, so the corpus has no `warn` outcome.

At the boundary, a refusal means zero submissions (commission), zero writes (admission), no recorded key (registration), and no completion (return and completion). Implementations prove the zero-effect half in their own tests (049 T009/T012; 025 FR-005). The corpus states the outcome, not the storage effect.

## Regeneration

Run `python3 -m scripts.council_convening.generate --check`. It regenerates every signed vector from labelled test-key derivations, and the index from the vectors, into a temporary tree and compares bytes. Any difference is a failure (`council-convening-generator-drift`). Without `--check`, it rewrites `conformance/` and the index. That is a reviewed change, and the corpus digest moves with it.
