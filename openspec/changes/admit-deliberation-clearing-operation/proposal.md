---
code_surface: openxFactory — `contracts/clearing/permitted-operations.registry.yaml` gains ENTRY NUMBER TWO; `scripts/validate-clearing-dispatch.py`'s `RATIFIED_OPERATIONS` frozen set, the INDEPENDENT copy in `tests/clearing/test_register_closure.py` (`RATIFIED`), the LITERAL member-count assertion in `.github/workflows/clearing-dispatch-gate.yml` ("1 registered operation"), and `tests/clearing/test_clearing_gate_wiring.py`'s assertion pinning that same literal from a second file all move in the SAME reviewed diff — FIVE frozen copies, not two, the fourth and fifth being real findings of this packet's authoring and its review round and recorded in design D9, together with three further pinned numerals the new schema moves (the five-schema filename list in `tests/clearing/test_schemas.py`, the six-row family count in `tests/clearing/test_clearing_manifest_rows.py`, and the per-file row digests); a NEW neutral `contracts/clearing/deliberation-return.schema.yaml` (Brett Heap's OQ1 ruling of 2026-09-04) of the ratified kind `xfactory_clearing_deliberation_return`, with a positive example and at least one negative fixture, registered in the validator's `SCHEMA_FILENAMES` and `KIND_TO_SCHEMA`, and the verdict scan extended to reach that kind; `contracts/clearing/dispatch-record.schema.yaml`'s CLOSED `refusal_ground` enumeration gains EXACTLY THREE members named in the ratified text — `lane_not_permitted`, `output_schema_failure`, `origin_scoped_credential` — the three of the record's nine awaited grounds that this entry's landing makes emittable, and no others; the two `deliberation`-named negative fixtures (`examples/negative/register-carrying-an-unratified-operation.yaml`, `examples/negative/manifest-naming-an-unregistered-operation.yaml`) RE-POINTED to another honest unratified operation name — `coding`, which `add-clearing-dispatch-boundary` design D11 names as the next real later operation — so the closure refusal keeps a live probe; `examples/dispatch-record-refused.example.yaml` and `tests/clearing/test_dispatch_record.py`'s refused-claim assertion follow the fixture re-point; `contracts/clearing/README.md`, `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and the repository README doc index. NO xFactory or codexFactory byte is this change's surface — those are dependent realizations named in the impact map.
target_release: the NEXT ADDITIVE MINOR of the contract bundle, ALLOCATED AT REALIZATION BY MERGE ORDER AND DELIBERATELY NOT NUMBERED HERE. `docs/contract-versioning-policy.md`, verbatim: *"A proposed change MUST NOT reserve a minor number before merge order is known, and a bundle is not published until its tag exists."* The class is ADDITIVE (minor) — *"new optional fields, new contracts, new validator warnings; domain repos on the same major version remain conformant without changes"* — because a register gaining a member and a new schema arriving add shapes and remove none. The archive gate is `release-realization`'s merged-plus-green realization evidence, and it is ORDERED AFTER `add-clearing-dispatch-boundary` archives, this packet's addition resting on that packet's unarchived one.
Status: draft
Proposed: 2026-09-04
Origin: codexFactory PR #165 (`adopt-bundle-shaped-deliberation`, head `b9714e2183d2e26a0f8023e47e3d00d8afc4245a`) tasks.md 1.6 / design D13 — the DEPENDENCY task that names this change and states that "leg 3 has no legal home until this lands"; standing on Brett Heap's clearing-boundary ruling of 2026-09-01 (operator workspace `cpc-clearing-boundary-ruling-2026-09-01.md`; `opensoft/codexFactory` issue #156) which #165 encodes, and on his ruling of 2026-09-04 settling this packet's OQ1 ("Ruling OQ1: new neutral deliberation-return schema").
---

# Proposal: admit-deliberation-clearing-operation

Status: draft

## Standing: this is the change the ratified basis asks for by name

`add-clearing-dispatch-boundary` is RATIFIED (2026-09-01, Brett Heap, on the
recorded word *"merge #192 and ratify #555"*; merged as PR #555, squash
`ab0bb2dd`), REALIZED in `contracts/clearing/` by PR #628 (`0d5e1ba9`), and NOT
YET ARCHIVED — so the capability `clearing-dispatch-boundary` lives in that
change's `## ADDED Requirements` block and in no promoted specification. Its
requirement *"The permitted-operations register is closed"* says what admission
costs:

> ADDING AN OPERATION SHALL BE A GOVERNED CONTRACT CHANGE with a spec delta and
> a reviewer, and SHALL NOT be a workflow edit: an operation set that any lane
> author may extend is a self-service widening of what the estate's hosts do,
> reviewed only as workflow configuration.

**This packet is that governed contract change, for the operation
`deliberation`, and it adds exactly one requirement.** It restates nothing the
basis already ratifies.

## Why

codexFactory PR #165 reshapes council deliberation into a four-leg,
bundle-shaped lane whose leg 3 runs the seats on the governed host. Its design
D13 states the blocker in its own words:

> Under #555 the permitted-operations register is CLOSED and its only member at
> landing is `readiness-diagnostic`. There is therefore **no legal home for a
> deliberation host job today**, and adding one by editing the clearing workflow
> is explicitly non-conformant.

The realized register instance agrees, deliberately and in writing. Its header
comment says `deliberation` "IS NOT HERE ON PURPOSE … It is a LATER GOVERNED
CHANGE", and the packaged corpus uses the name twice as the honest fixture that
proves the closure refusal fires:
`examples/negative/register-carrying-an-unratified-operation.yaml` and
`examples/negative/manifest-naming-an-unregistered-operation.yaml`. The
register's own words: *"The failure mode is never somebody adding an absurd
operation. It is somebody adding a REASONABLE one — wanted, well-formed, and in
the file rather than in a change."*

So the register is doing exactly what it exists to do, and the only way past it
is the front door. This is the front door.

## What changes

**ONE requirement, ADDED to `clearing-dispatch-boundary`:** *"deliberation is
register entry number two and returns evidence only"*. It mirrors the shape of
the basis's own entry-number-one requirement — one requirement per member,
declaring every fact the closure requirement demands — and it fixes:

| fact | value |
|---|---|
| operation id | `deliberation` |
| may | read the admitted, RE-SEALED bundle served from the CLEARING run; run the seat deliberations; emit the per-seat outputs as a STRUCTURED RETURN of evidence bound to the convening job id, the verified subject pin, and the inbound bundle digest |
| may not | check out any repository; write outside runner plumbing; reference a secret; **hold any seat key or signing key — sign-on-return means NO KEY ON THE HOST**; carry a verdict / eligibility / go-no-go field; report OBSERVED runner-group membership; affect any repository |
| `checks_out_code` | `false` |
| `writes` | `false` |
| `may_reference_secrets` | `false` |
| `token_scopes` | exactly `actions:read` — the CLEARING side's own scoped, short-lived read-only admission credential, enough to read the clearing repository's own run artifacts and no more |
| refusal grounds admitted | `lane_not_permitted`, `output_schema_failure`, `origin_scoped_credential` — THREE, named here because the record's ground enumeration is closed and this is the governed change (design D13). Each is a RENDERING of one of the nine names the dispatch record's own description already awaits in prose ("lane not permitted", "output-schema failure", "origin-scoped credential"), in the identifier form the two seeded members carry; no concept is coined, and the requirement writes the rule down so the remaining six render the same way |
| `timeout_minutes` | bounded |
| `worker_profile` | `council-deliberation-worker` |
| lanes | **ARTIFACT ONLY** — `lane_key` `artifact` / `xfactory-artifact-workers` / `host-rider-cpc-brett01` / `xfactory-artifact-cpc-brett01`; a coding-lane request is refused `clearing-lane-not-permitted` |
| `output_schema_ref` | `contracts/clearing/deliberation-return.schema.yaml` — a NEW NEUTRAL schema (OQ1, ruled), records of kind `xfactory_clearing_deliberation_return` |
| `data_handling` | `internal-governance` — STRICTER than entry one's `public_log_only`, as the register instance's comment promised a bundle-carrying operation would be. The FIELD's vocabulary is borrowed from `document-cataloging` as the register's schema says; the CLASS NAME is the `Handling:` header value the estate's governance corpus already travels under (design D7) |
| `repository_affecting_output` | `false` — the return is evidence; the verdict is computed by the runtime |

**Seven scenarios**, including the two the basis's closure requirement makes
refusable (an unpermitted lane; a widening of the class constraints), the
verdict-word refusal, the schema-validation refusal, the no-key-on-the-host
refusal, and the route-retirement refusal that stops this entry from becoming a
second door beside the grandfathered `council-deliberation-worker.yml`.

The requirement also states **which component emits which refusal**, so that no
part of it is left for a realizer to settle: the canonical validator reports a
shape failure as the family's non-member `schema` refusal and only once the new
`kind` is routed to its schema; the dispatch record's ground
`output_schema_failure` is written by the clearing workflow's hosted finalizer,
where the basis already places that refusal; `origin_scoped_credential` is a
property of a dispatch attempt and owes no fixture; and the validator's only duty
over the new members is the one it already performs, reading the enumeration out
of the schema at run time. **NO FINDING CODE IS MINTED** (design D13).

**TWO QUESTIONS ARE PUT FOR THE RATIFIER'S RULING**, each with both readings and
the cost of each, under a `THE QUESTION, PUT FOR RULING` heading in `design.md`:
**D10** — does the basis's dormant-second-door scenario reach THIS admission, or
only the act that declares the host job? — and **D13** — three refusal grounds
now, or two? Everything else in the packet beyond the two dated rulings is
flagged for veto in the ordinary way.

## What this proposal does NOT do

**NO CONTRACT BYTE MOVES IN THIS PULL REQUEST.** Ratification AUTHORIZES
realization; it does not PERFORM it — `add-cpc-clearing-boundary`'s own words for
the same posture: *"no register row, key, workflow, or authorization entry is
created by this change — those are dependent realizations named in the impact
map, authorized but not performed here."* The register instance still holds
exactly one member on this branch, the validator's frozen set still holds one
name, and `clearing-dispatch-gate` still asserts "1 registered operation". They
move together, once, in the realization slice of Phase 2.

It also does **not**:

- **Touch `opensoft/xFactory`'s `clearing-dispatch.yml` operation choice list.**
  `add-clearing-dispatch-boundary` tasks.md § 3.7 makes that the clearing lane's
  plumbing and states the consequence in its own words: once the registry
  instance exists, that workflow must validate the dispatched operation against
  the registry INSTANCE and stop relying on its own choice list as the
  authority. That is a task of the clearing repository, and a green gate here
  does not discharge it.
- **Add a `coding` operation.** `coding` appears in this packet only as the
  re-pointed fixture name — an honest, wanted, still-unratified operation, named
  as the next real one by the basis's design D11. Naming it in a fixture admits
  nothing.
- **Ship a finalizer.** `repository_affecting_output: false` means no finalizer
  applies.
- **Move a seat key, mint one, or change where signing happens.** Sign-on-return
  is codexFactory #165's design D6; this entry only forbids the key ever being
  on the host.

## Impact

- **Affected capability:** `clearing-dispatch-boundary` (ADDED, one requirement).
- **Affected code (at realization, not here):** the FIVE frozen member-set
  copies and the three pinned numerals beside them; the new neutral return
  schema, its kind routing and its fixtures; the three refusal grounds admitted
  to `contracts/clearing/dispatch-record.schema.yaml`; the two re-pointed
  negative fixtures and the refused dispatch-record example that follows them;
  `contracts/clearing/README.md`; `contracts/manifest.yaml`;
  `contracts/CHANGELOG.md`; the repository README doc index.
- **Dependent realizations, named and NOT performed here:** `opensoft/xFactory`
  — the `deliberation` host job declared physically in `clearing-dispatch.yml`,
  the registry-instance validation replacing the literal choice list (§ 3.7), and
  the RETIREMENT of the grandfathered `council-deliberation-worker.yml` in the
  same act; `opensoft/codexFactory` — PR #165's legs 1 and 4 and its own
  retirement half.
- **Ordering:** archives AFTER `add-clearing-dispatch-boundary`.
- **Lane:** `hermes-wallet-exercise`. Claim:
  https://github.com/opensoft/codexFactory/pull/165#issuecomment-5535747335.
  Shared-substrate claim (Rule 7):
  https://github.com/opensoft/openxFactory/issues/630#issuecomment-5535802164.
