# clearing Contract Family

Status: ratified
Ratified by: add-clearing-dispatch-boundary (ratified 2026-09-01 by Brett Heap,
record `openspec/changes/add-clearing-dispatch-boundary/review/ratification-2026-09-01.md`;
merged as PR #555, squash `ab0bb2dd`, 2026-09-02), as MODIFIED by
add-cpc-clearing-boundary (ratified 2026-09-02, merged `c0270d28`). Registered in
[`contracts/manifest.yaml`](../manifest.yaml) + [`contracts/CHANGELOG.md`](../CHANGELOG.md)
at `contract-v3.3`, per [Contract Versioning Policy](../../docs/contract-versioning-policy.md).

The neutral contract for **the clearing and dispatch boundary in front of a
governed execution estate** — the shapes a clearing implementation validates,
records and attests with.

## What this family is, in one paragraph

An estate can hold a governed execution host that more than one repository wants
to reach. The ratified boundary says exactly one repository — the CLEARING
REPOSITORY — may originate execution on it; that work crosses only as a SEALED
BOUNDED REQUEST carrying ten declared fields; that every field with an
authoritative provider-side answer is RESOLVED FROM THE PROVIDER and never
believed because the bundle asserts it; that the set of operations a host may be
asked to perform is a CLOSED REGISTER; and that every dispatch and every refusal
is RECORDED, with the single-door claim ATTESTED rather than assumed. This family
is the machine-readable half of that: five record shapes, one closed register
instance, and a canonical validator that refuses.

## The five shapes

| file | kind | what it is |
|---|---|---|
| [`sealed-bundle-manifest.schema.yaml`](sealed-bundle-manifest.schema.yaml) | `xfactory_sealed_bundle_manifest` | The sealed bounded request's manifest — the TEN declared fields, its expiry, its per-file byte hashes, and field (10)'s origin attestation. |
| [`permitted-operations.schema.yaml`](permitted-operations.schema.yaml) + [`permitted-operations.registry.yaml`](permitted-operations.registry.yaml) | `xfactory_clearing_permitted_operations_registry` | The CLOSED register, schema plus its one instance. |
| [`operation-report.schema.yaml`](operation-report.schema.yaml) | `xfactory_clearing_operation_report` | `readiness-diagnostic`'s COMPOSED report of record — probed facts as data, and no verdict. |
| [`dispatch-record.schema.yaml`](dispatch-record.schema.yaml) | `xfactory_clearing_dispatch_record` | The ledger entry, written for a cleared dispatch AND for a refusal. |
| [`single-door-attestation.schema.yaml`](single-door-attestation.schema.yaml) | `xfactory_clearing_single_door_attestation` | The periodic per-group comparison that keeps the ledger's completeness claim honest. |

Canonical validator:
[`scripts/validate-clearing-dispatch.py`](../../scripts/validate-clearing-dispatch.py).
Packaged corpus: [`examples/`](examples/) — positives at the top level, one
intended-invalid fixture per closed refusal code under
[`examples/negative/`](examples/negative/). Tests: `tests/clearing/`.

## THE REGISTER IS CLOSED, and what that costs

`permitted-operations.registry.yaml` holds **exactly one member**,
`readiness-diagnostic` — the ratified entry #1, a strictly read-only probe that
asserts only what the host can state about itself.

**Adding an operation is a GOVERNED CONTRACT CHANGE with a spec delta and a
reviewer. It is not a workflow edit, and it is not an edit to this file alone.**
The ratified requirement is explicit about why: *"an operation set that any lane
author may extend is a self-service widening of what the estate's hosts do,
reviewed only as workflow configuration."* Widening an existing entry's class
constraints — letting it check out code, write, or reference a secret where its
entry forbids it — is a governed change on the same terms.

The validator refuses an instance member outside the ratified set with
`clearing-register-member-unratified`.

**THE HONEST LIMIT OF THAT REFUSAL.** The register, the validator that reads it,
and the test that pins it all live in this repository, so one diff can edit every
side of the mechanism. What the refusal guarantees is that an addition cannot be
made SILENTLY: it is a red check plus a diff touching the register or the
validator, and REVIEW OF THAT DIFF is the declared backstop. This is stated
rather than overclaimed for the same reason the ratified authoring-time guard
requires it — a tripwire described as an unforgeable refusal is a control nobody
checks.

`deliberation` (codexFactory #165) is a LATER governed change and is deliberately
absent; `examples/negative/register-carrying-an-unratified-operation.yaml` uses it
as the fixture that proves the refusal fires.

## NO SECOND VOCABULARY

This family adds the boundary and nothing another capability owns:

| borrowed | owner |
|---|---|
| the ONE digest construction `xfc-jcs-sha256-1` and its subjects | `signed-execution-chain` — [`digest-construction.schema.yaml`](../signed-execution-chain/digest-construction.schema.yaml). `sealed_bundle_manifest` was added to ITS enumeration at tranche three; no construction is declared here. |
| runner group, dispatch label, trust tier, the enrollment audit record | `worker-enrollment-broker` |
| scoped short-lived credentials and their custody | `credential-contracts` |
| job scope references | `neutral-job-envelope` |
| handling class and host attestation | `document-cataloging` / `ideation-routing` |
| the origin identity a field-(10) signature resolves to | [`governance/factory-identity/`](../../governance/factory-identity/README.md) (`factory-origin-identity`) |

**PER-FILE HASHES ARE NOT JSON VALUES.** A manifest's per-file `content_hash` is
plain algorithm-tagged SHA-256 over the file's BYTES. A canonical-JSON
construction has nothing to canonicalize in a byte stream, so applying one there
is a category error and the validator refuses it as such. One construction for
JSON values, one byte hash for file content — both already in use, neither
invented here.

## A NAME COLLISION THAT IS NOT A DUPLICATE

[`contracts/schemas/dispatch-record.schema.yaml`](../schemas/dispatch-record.schema.yaml)
already exists and is a DIFFERENT record: `add-capability-steward`'s
dispatch-JUNCTION decision, answering which of the crystallized or AI path served
a capability request. This family's
[`dispatch-record.schema.yaml`](dispatch-record.schema.yaml) answers what was
CLEARED to a governed execution host, and what was refused. Different subject,
different owning capability, different required members, different `$id`. Neither
file is moved or renamed; each names the other so a reader who greps the filename
lands on the distinction rather than on a coincidence.

## WHAT REGISTRATION DOES NOT CONFER

Registering these shapes does not make the boundary enforced. Enforcement is the
CLEARING IMPLEMENTATION's — today `opensoft/xFactory`'s
`.github/workflows/clearing-dispatch.yml` (PR #191, squash `95f1a9c6`), which
emits its ledger as `clearing.*=` key-value lines and validates its operation id
against its own literal choice list. `add-clearing-dispatch-boundary` `tasks.md`
§3.7 states the consequence in its own words: **once this register instance
exists, that workflow must validate the dispatched operation against the registry
INSTANCE and stop relying on its own choice list as the authority.** That is a
task of the clearing repository, not a byte of this family, and a green gate here
does not discharge it.

Likewise, the validator does not contact a provider API, does not evaluate
revocation at the moment of clearing (the factory-identity register declares that
unrealizable until a projection path exists, and this family does not claim
otherwise), and does not verify a sealed RETURN — no return shape ships here.

## NOT THIS FAMILY'S SURFACE

Each named in the ratified `code_surface` paragraph as a successor or as
somebody else's artifact: `realize-factory-bundle-packaging` (the codexFactory
hosted packaging workflow and the CODING operation's register entry); the HOSTED
FINALIZER for patch-returning operations; the grandfather retirements; any
runner, group, label, host or credential; the L4 authoring-time guard and the L5
attestation IMPLEMENTATIONS; and the neutral INFRASTRUCTURE-READINESS RESULT that
`ideation-routing` and `document-cataloging` await — to which the operation report
is a candidate INPUT and which it is deliberately NOT.
