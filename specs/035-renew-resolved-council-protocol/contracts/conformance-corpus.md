# Conformance corpus format and adapter contract

**Feature**: [spec.md](../spec.md) · **Plan**: [plan.md](../plan.md) · **Research**: R1, R2, R8, R9, R16, R18

The corpus is `contracts/council-convening/conformance/`. It is shared by three independent implementations:

- the provider reference implementation, which adjudicates every vector in CI;
- the producer, 049;
- the consumer, 025.

## Files

- `conformance/index.json` holds the index.
- `conformance/vectors/<area>/<case_id>.json` holds one vector per case. The area is one of `foundation`, `resolution`, `assignment`, `signing`, `binding`, `migration`.

Every file is JSON (RFC 8259): UTF-8 with no byte-order mark, LF line endings, a single trailing newline, a closed object at every depth, and `schema_version: 1` plus `kind`. The generator writes members in sorted order with two-space indentation, so regeneration is byte-identical (R18).

## Index (`kind: openxfactory-council-convening-conformance-index`)

| Member | Content |
|---|---|
| `corpus_id` | `council-convening-conformance` |
| `protocol` | `xfc-resolved-council-1` |
| `cases` | Rows in bytewise UTF-8 order of `path`: `{case_id, area, boundary, applies_to, requirement_ids, path, sha256, expected}` |
| `totals` | Counts by `area`, by `expected.outcome`, and of rows whose `applies_to` names both sides |

Closure holds in both directions:

- every file under `conformance/` except `index.json` is a row;
- every row's file exists;
- every `sha256` (`sha256:` + 64 hex over raw bytes) matches;
- every `case_id` is unique and equals its file's basename.

Two coverage rules also hold:

- every refusal code in the closed vocabulary is some row's `expected.refusal`;
- every `FR-001`–`FR-012` and `SC-001`–`SC-003` appears in some row's `requirement_ids`. SC-004 is an operational rehearsal; the corpus carries its rehearsal-record shape vectors under `migration`, but the rehearsal itself is not a corpus act.

## Vector (`kind: openxfactory-council-convening-conformance-vector`)

| Member | Content |
|---|---|
| `case_id` | Equals the index row. |
| `area`, `boundary` | `boundary` is one of `commission`, `admission`, `registration`, `return`, `completion`, `binding`, `selection`, `activation`, `historical`. |
| `applies_to` | A non-empty subset of `[producer, consumer]`. The provider reference implementation runs every vector. |
| `requirement_ids` | The FR and SC identifiers the case probes. |
| `evaluation_time` | A `utc_instant`. Every expiry and lifetime check uses it, never the wall clock. |
| `inputs` | The record or records under test, keyed by role, for example `record`, `snapshot`, `registration`, `returns`, `selection_producer`, `selection_consumer`. |
| `environment` | The oracle data (below). Members not used by the boundary are absent, not empty. |
| `expected` | `{outcome: accept \| refuse \| warn, refusal: <code> \| null, derived: {...}}`. |

`derived` holds known answers, so implementations compare more than a verdict:

- for `accept` at commission or admission: `required_seats` and `convening_digest`;
- for signing vectors: `signed_bytes` (unpadded base64url) and `key_fingerprint`;
- for `warn`: the finding code.

## Environment oracles

An adapter must inject these and must not consult a live system during a corpus run (R8):

| Oracle | Key | Value |
|---|---|---|
| `governed` | `<repository>@<revision>:<path>` | `{available, governed, blob_sha256, tip_blob_sha256}`. `tip_blob_sha256` drives `rule_superseded` under the OPEN-3 ruling. |
| `rules` | `<repository>@<revision>:<path>` | `{classes: {<matched_class>: {councils: [...], standing_seats: [...], conditions: [{seat, predicate, input_contract, parameters}]}}}`: the neutral projection an adapter would derive from the domain file. |
| `facts` | `pr_facts:<repository>#<pull_number>@<head_sha>` or `rule_facts:<repository>@<revision>:<path>` | The authoritative fact object for that source. |
| `live_heads` | `<repository>#<pull_number>` | A `full_sha` or `"unavailable"`. For commission vectors, a list read in order, so drift before and after the recheck is expressible. |
| `issued` | — | `{challenges: [...], consumed_challenges: [...], registered_keys: [{assignment_id, key_fingerprint}], accepted_returns: [...], live_snapshots: [...]}` as of `evaluation_time`. |
| `identity` | — | `{verified: bool, claims: {...}, principal: {principal_kind, principal_ref}, broker_capability_verified: bool}`. Decoded-only claims carry `verified: false`. |
| `repository_identity` | — | Absent: the adapter reads `contracts/policies/repository-identity.yaml` at the pinned commit. |
| `registry_status` | — | Optional override of E1 statuses, so minor-time and major-time behavior can both be vectors at one commit. |

## The `$parts` sentinel

Any string leaf may be written `{"$parts": ["..", ".."]}`. Before any other processing, adapters replace it with the concatenation of its parts. It exists so secret-shaped negative values never appear contiguously in a committed file, which the provider's own `scan_secrets` would flag (R9). It is the only object-valued leaf allowed where a schema expects a string. An object leaf anywhere else is a malformed record.

## Outcome semantics

- `accept`: no refusal, and every `derived` value matches.
- `refuse`: exactly the named code. A different refusal is a disagreement, even when it is also a refusal (SC-001: "negative vectors must agree on refusal").
- `warn`: accepted, with exactly the named finding (`legacy_protocol_deprecated`, under `registry_status` `deprecated`).

At the boundary, a refusal means zero submissions (commission), zero writes (admission), no recorded key (registration), and no completion (return and completion). Implementations prove the zero-effect half in their own tests (049 T009/T012; 025 FR-005). The corpus states the outcome, not the storage effect.

## Regeneration

Run `python3 -m scripts.council_convening.generate --check`. It regenerates every signed vector from labelled test-key derivations into a temporary tree and compares bytes. Any difference is a failure (`council-convening-generator-drift`). Without `--check`, it rewrites `conformance/` and the index. That is a reviewed change, and the corpus digest moves with it.
