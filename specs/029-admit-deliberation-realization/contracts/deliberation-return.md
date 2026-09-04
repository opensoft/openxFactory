# Contract note: `xfactory_clearing_deliberation_return`

**Feature**: [../spec.md](../spec.md) | **Shape**: `contracts/clearing/deliberation-return.schema.yaml`

The interface this feature adds. Written as a contract note rather than as a
second schema: the schema itself is the artifact, and this file records what a
CONSUMER may rely on and what it may not.

## Identity

| | |
|---|---|
| `kind` | `xfactory_clearing_deliberation_return` — **ratified text**, not chosen at realization |
| `contract_id` | `clearing-deliberation-return` |
| `$id` | `https://xforge.us/schemas/openxfactory/clearing/v1/deliberation-return.schema.yaml` |
| dialect | JSON Schema draft 2020-12 |
| routing | `KIND_TO_SCHEMA` in `scripts/validate-clearing-dispatch.py` |
| registered | `contracts/manifest.yaml`, row `clearing-deliberation-return` — AT REALIZATION, reserving no bundle number (research.md § O7) |

**Why the kind is ratified rather than realized.** The verdict scan is DISPATCHED
ON KIND. A realization free to choose the kind would be free to choose whether
the scan reaches this operation at all — a policy choice wearing the clothes of
an identifier (ratified design D13).

## What a consumer may rely on

1. **The root is CLOSED.** An unknown top-level member cannot validate.
2. **Every nested object is closed.** A smuggled member fails the shape check
   wherever it is put.
3. **The verdict scan reaches this kind.** A member at ANY depth whose name reads
   as a verdict, eligibility, decision, go/no-go, approval or recommendation is
   refused `clearing-report-carries-a-verdict` — the EXISTING code; no code is
   minted for this kind.
4. **A return names the three binding identifiers or it does not validate**:
   `convening_job_id`, `verified_subject_pin`, `inbound_bundle_digest`.
5. **At least one seat.** `seats` is `minProperties: 1`.
6. **Seat identity is the KEY.** Duplicate seat identity is unrepresentable.

## What a consumer may NOT rely on, stated rather than left to be discovered

1. **There is no signature member, and there will not be one at this boundary.**
   The return is UNSIGNED on the host — no key of any kind is ever present there
   — and is signed ON RETURN by the originating repository's own hosted signer,
   downstream of and outside this shape.
2. **There is no outcome, verdict, or eligibility member**, at any depth, by
   construction. The outcome is computed by the runtime from the signed returns.
3. **The seat's OUTPUT is opaque to this contract.** It is a string payload or a
   reference plus a byte hash. The producing estate's per-seat accounting
   (`num_turns`, `declared_turn_cap`, `model_usage`, `declared_model`, …) lives
   INSIDE that payload and is not a neutral member — a neutral schema that
   enumerated it would be authoring the producer's shape, which is precisely what
   design D4 refuses when it forbids a producer-owned `output_schema_ref`.
4. **`lane` is not pinned to `artifact` by this schema.** WHICH lanes the
   operation may use is the CLOSED REGISTER's answer, and a `const` here would be
   a second copy of a decision the register owns.
5. **No digest construction is declared here.** `inbound_bundle_digest` is the
   VALUE of the inbound sealed-bundle manifest's `manifest_digest`, computed
   under `signed-execution-chain`'s `xfc-jcs-sha256-1` over the
   `sealed_bundle_manifest` subject. This family declares no construction, no
   handling vocabulary, and no job envelope.

## Failure modes, and who emits each

| condition | reported as | by |
|---|---|---|
| the return does not match this shape | finding code `schema` | the canonical validator — and ONLY because the kind is routed |
| a member reads as a verdict | `clearing-report-carries-a-verdict` | the canonical validator |
| a LIVE return fails its declared schema at dispatch | record ground `output_schema_failure` | the clearing workflow's hosted finalizer — **not** the canonical validator, which never writes a dispatch record |
| a coding-lane request for this operation | `clearing-lane-not-permitted`, recorded with ground `lane_not_permitted` | the clearing workflow |
| a producer-scoped credential or a key in the host job | record ground `origin_scoped_credential` | the clearing workflow, at dispatch — a property of an ATTEMPT, so no fixture can make it fire and none is owed |

## Example

`contracts/clearing/examples/deliberation-return.example.yaml` (positive).
Negative fixtures:
`examples/negative/deliberation-return-that-does-not-match-its-shape.yaml`
(declares `schema`) and
`examples/negative/deliberation-return-carrying-a-verdict.yaml`
(declares `clearing-report-carries-a-verdict`).
