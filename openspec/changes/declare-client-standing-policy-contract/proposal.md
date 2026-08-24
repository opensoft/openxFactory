---
code_surface: openxFactory — `contracts/client-content/client-overlay.schema.yaml` (two OPTIONAL properties added INLINE under `client`; NO new sibling file and NO new manifest row), an extension of the canonical validator `scripts/validate-client-content.py` (the `hermes_client_overlay` structural branch gains the standing-policy rules, and `self_test` sweeps every packaged positive instead of one hardcoded filename), one new positive example plus eight `# expected_failure:`-declaring negatives under `contracts/client-content/examples/`, the family `README.md`, and the release surface `contracts/manifest.yaml` (the `client-overlay` row's sha256 RECOMPUTED — no row added) + `contracts/CHANGELOG.md` + `contracts/releases/<tag>.digests.yaml`. NO client overlay INSTANCE is authored here — the seedable instance is `config/clients/<client_ref>/overlay.yaml` in the install repo. NO hermes-install code changes: the runtime already implements this, ratified and landed 2026-08-22; the re-pin and its parity admission are its own follow-ups.
target_release: contract-v<next minor> — allocated LATE at realization per `docs/contract-versioning-policy.md` (v1.40 is the current bundle; a proposal MUST NOT reserve a minor number before merge order is known), and the cut is SHARED with whatever other next-additive-bundle changes fold into the same `Unreleased` section. Archives only on ALL of: ratified with the three D-positions confirmed; schema, fixtures and validator extension landed on openxFactory main with `validate-client-content.py` green; the bundle released — manifest, changelog, digest inventory, and a verified annotated tag; and CONSUMED — hermes-install re-pinning the client-content family at that release and admitting `hermes_client_overlay` to its `PARITY_KINDS` sweep. A declaration nothing validates against and nobody pins is not realized.
Status: ratified
Ratified: 2026-08-23 by Brett Heap (openxFactory operator authority) —
in-session ruling: D1 (inline, no sibling schema), D4 (subtree-scoped scan,
the asymmetry deliberate), D5 (message/constant adoptions) all ratified as
built. The contract shape itself was not re-litigated — it mirrors the shape
ratified in hermes-install add-client-overlay-standing-policy.
---

# Proposal: declare-client-standing-policy-contract

## Why

**A live runtime validates and seeds two blocks of a contract this repository
owns, and this repository declares neither.** `hermes_client_overlay` is
openxFactory's (`contracts/client-content/client-overlay.schema.yaml`, realized
at `contract-v1.17`, live-proven by the opensoft tenant flip 2026-07-24).
hermes-install's `add-client-overlay-standing-policy` — ratified 2026-08-22 by
Brett Heap, merged — extends it with an optional `client.policies` map and a
`client.policy_namespace` the map is address-validated against, so a **Tenant**
layer can carry FREESTANDING company-wide standing policy rather than only
deviations from the domain baseline. That is the semantically correct seat for
it: Tenant is the tenant-operator layer
(`contracts/policies/layer-vocabulary.yaml`), which is exactly where
company-wide policy belongs, and it closes the design/code half of
`xFactory-Hermes-Install#34` — the standing-policy veto seat's policy finally
has a route to seed.

**The sequencing was ruled deliberately, and the ruling names this change as
its other half.** From issue `opensoft/openxFactory#254`, Brett Heap,
2026-08-22:

> **Sequencing decision (Brett Heap, 2026-08-22):** land the hermes-install
> extension now rather than gating it behind this contract change first —
> nothing in the current runtime enforces against the unknown field
> (`validate-client-content.py`'s structural check inspects
> `ref`/`display_name`/`policy_overrides` and rejects no unknown block; the
> schema itself sets no `additionalProperties: false`), so nothing breaks and
> no consumer needs to re-pin. But `client.policies`/`client.policy_namespace`
> are currently an UNDECLARED extension of a contract this repo owns, and that
> should be formalized here rather than left permanently implicit.

The same ruling appears in the commissioning change's own record
(`add-client-overlay-standing-policy` task 1.2, design §7 OQ-1): options (ii)
gate-behind-upstream and (iii) retire-the-pinned-copy-as-hermes-install-owned
were both **declined**, and the accepted divergence is bounded and
one-directional — *"hermes-install is stricter than canon, never the reverse"*.

**Every premise of that safety argument was re-verified in this repository at
authoring time, and every one holds — which is the same reading that makes the
gap real.**

| Claim | Evidence read |
|---|---|
| Canon does not declare the block | `client-overlay.schema.yaml` `client.properties` lists exactly `ref`, `display_name`, `policy_overrides`, `memory_boundaries`, `integration_boundaries`; `client.required` is `[ref, display_name, policy_overrides]` |
| Canon rejects no unknown block | `scripts/validate-client-content.py::validate_structure`, `hermes_client_overlay` branch: checks `client.ref`, `client.display_name`, recurses into `policy_overrides`, returns. No unknown-key sweep anywhere in the family |
| The schema is open | No `additionalProperties: false` in any of the four `client-content/*.schema.yaml` files |
| No parity suite covers the kind | hermes-install `tests/unit/test_contract_parity.py` `PARITY_KINDS = {hermes_domain_overlay, hermes_subject_overlay}`, with a comment stating that `hermes_client_overlay`'s canonical meaning belongs to `validate-client-content.py` over a different fixture corpus |
| The shape to mirror already exists here | `contracts/hermes-domain-overlay/hermes-subject-overlay.schema.yaml` `subject.policy_namespace` + `subject.policies` (`minProperties: 1`; per-entry `required: [policy_id, policy_namespace]`; open body), and its six canonical rules in `scripts/validate-hermes-domain-overlay.py::validate_subject_overlay` |

So the window is safe **and** the window is a hole: canon is silent, therefore
the install repository is the de facto source of truth for a neutral tenant
contract it does not own. This change closes it by DECLARING what is already
true, not by inventing anything.

## What Changes

- **DECLARE `client.policy_namespace` and `client.policies` in
  `contracts/client-content/client-overlay.schema.yaml`**, both OPTIONAL, both
  INLINE under `client`. `policies` is a `minProperties: 1` mapping keyed by
  policy id whose entries `required: [policy_id, policy_namespace]` and keep an
  OPEN body; `policy_namespace` is a non-empty string. A faithful mirror of
  `subject.policy_namespace` + `subject.policies` one layer up.
- **`client.required` IS BYTE-FROZEN.** `[ref, display_name, policy_overrides]`
  is unchanged. An overlay that declares neither key takes exactly the verdict
  it took before the block existed. The change is additive in the strict sense
  and no consumer is forced to re-pin.
- **NO `relation_to_*` FIELD** — the one place the mirror is deliberately
  imperfect. Ratified 2026-08-22, ruling (d): a tenant's standing policy is a
  POSITION, not a deviation, so there is no baseline for it to declare a
  relation to. `policy_overrides` (a DEVIATION, `relation_to_domain:
  stricter_only`, read by `approvals.tenant_auto_clear_envelope` for a
  different question) and `policies` (a POSITION) are orthogonal in every
  direction: a document may carry either, both, or neither.
- **ADDRESSABILITY IS THE POINT, AND THE CONTENT KIND IS `policy_position`.**
  Ratified 2026-08-22, ruling (b). For a tenant whose namespace is `N`, every
  policy id `P` under it resolves `N/P` to exactly one enforceable payload;
  each payload restates its own `policy_namespace` and `policy_id` so a
  materialized row is address-resolvable without joining to a sibling row. The
  neutral contract MUST NOT enumerate policy names — enumerating them is
  precisely what stops `client-policy-overrides.schema.yaml` (a CLOSED set of
  seven) from carrying a named standing policy.
- **A DECLARED-BUT-EMPTY BLOCK IS REFUSED, NOT TREATED AS ABSENT.** Ratified
  2026-08-22, ruling (c). An empty map materializes an empty `policy_position`
  row, and `manager_review.commissioning_readiness` clears
  `materialized_policy:<layer>` on ROW PRESENCE rather than row content, so an
  empty block would report a standing-policy veto seat READY with nothing
  behind it — reopening on the write side exactly what hermes-install issue #32
  closed on the read side.
- **TEACH THE CANONICAL VALIDATOR THE SIX RULES THE SHAPE CANNOT EXPRESS** —
  non-empty map (with the empty refusal, and a DISTINCT finding for a
  wrong-typed block); per-entry mapping; `policy_id` non-empty and equal to its
  key; entry `policy_namespace` non-empty and equal to
  `client.policy_namespace`; `client.policy_namespace` required non-empty WHEN
  AND ONLY WHEN `policies` is present; `<namespace>/<id>` address uniqueness —
  plus a prohibited-domain-block and credential-value scan **scoped to the
  `client.policies` subtree only**. JSON Schema in this family carries no
  `if`/`then`, so the conditional requirement lives in the validator, exactly
  as the subject family leaves its own cross-field rules to
  `scripts/validate-hermes-domain-overlay.py`.
- **SHIP FIXTURES, AND FIX THE TRAP THAT WOULD HAVE HIDDEN THEM.** One positive
  example and eight negatives, each declaring its `# expected_failure:` reason.
  `self_test` hardcoded exactly ONE positive filename, so a second positive
  would have been packaged and never run; it now sweeps every packaged
  `*.example.yaml` other than the baseline comparand, which keeps its role
  unchanged.
- **PUBLISH AS A VERSIONED ADDITIVE BUNDLE** so hermes-install can re-pin the
  client-content family and finally admit `hermes_client_overlay` to
  `PARITY_KINDS`.

## Capabilities

### Modified Capabilities

- `client-layer-tuning`: one MODIFIED requirement — *Client content shapes are
  contract-validated* — restated in full with its overlay scenario widened to
  name the OPTIONAL standing-policy block and the frozen `client.required`;
  and one ADDED requirement — *Tenant standing policy is address-resolvable and
  validated* — carrying the addressability rules, the conditional namespace
  requirement, the declared-but-empty refusal, and the subtree-scoped
  prohibited-content scan.

## Impact

- **openxFactory**: two optional properties on one existing schema, a validator
  extension, nine fixtures, a family README entry, and one shared bundle
  release. No existing schema property, fixture, or validator verdict changes:
  every rule added is reached only from `if "policies" in client`.
- **Release surface, SHARED.** `contracts/manifest.yaml`'s `client-overlay` row
  digest is RECOMPUTED (the schema file's bytes changed) and its
  `consumption_rule` restated; `contracts/CHANGELOG.md` opens an `Unreleased —
  pending bundle registration` section. **No minor number is allocated and no
  tag is cut here** — `docs/contract-versioning-policy.md` allocates the
  version LATE, at realization, and forbids reserving one in a proposal. The
  cut, the digest inventory and the annotated tag are ONE act shared with
  whatever other next-additive-bundle changes fold into the same section.
- **hermes-install** (the IMPLEMENTED REALITY, not this change's surface): no
  code change is owed. `_validate_client_policies` in
  `src/hermes_install/domain/overlay_content.py` already enforces these rules
  in-process and `split_enforceable_slice` already emits the
  `policy_position` row. What becomes AVAILABLE when this lands, and what its
  own ruling says is *"not scheduled here"*: re-pinning the client-content
  family at the new tag, and adding `hermes_client_overlay` to
  `tests/unit/test_contract_parity.py`'s `PARITY_KINDS`. That admission is not
  free — `_fixture_dir()` resolves ONE directory
  (`contracts/hermes-domain-overlay/examples`) and the client fixtures live in
  `contracts/client-content/examples`, so the sweep needs a per-kind fixture
  root before a client floor can mean anything. Named here so it is not
  discovered as a surprise; owned there.
- **Divergences CLOSED by this change**: canon now declares the two properties;
  canon now enforces all six address rules the runtime enforces; canon now
  refuses a declared-but-empty block; canon now scans the standing-policy
  subtree for domain-authority blocks and key material. After this lands the
  runtime and the canonical validator agree on every verdict over the packaged
  corpus.
- **Divergences deliberately PRESERVED**: (1) **the subtree-scoped scan
  asymmetry** — the subject path walks the WHOLE document, this path walks only
  `client.policies`. Widening it would change the verdict of released overlays
  that use none of the new block, which is a breaking change wearing an
  additive change's clothes, and it would invert the one-directional divergence
  the sequencing ruling was granted on (canon would refuse what the runtime
  accepts). (2) **No remediation vocabulary** — hermes-install raises a
  credential finding under a distinct `SECRET_MATERIAL_PRESENT` remediation
  category; this validator has one flat findings list and no remediation
  concept, so the same verdict arrives through one channel. (3) **No
  `relation_to_*`**, as ruled.
- **Out of scope**: hermes-install's re-pin and its `PARITY_KINDS` admission
  (both available on landing, both its own, both *"not scheduled here"* by its
  ruling); authoring the company's actual standing-policy DOCUMENT (act (b) of
  hermes-install issue #34, a human's, and its OQ-3 — whether tenant policy
  content lives in the install repo's overlay or a neutral home the overlay
  composes — is undecided and unaffected by this shape); a tenant content SET
  or `hermes_client_content_manifest` (its OQ-4: tenant policies ride INLINE
  because `load_domain_content_set` sweeps `hermes/domain/<dir>` only); any
  runtime join from `policy_refs` to a materialized row (its OQ-5, worker-side
  — this contract makes the address RESOLVABLE, it does not assign the
  resolver); and renaming the subject validator's `PROHIBITED_SUBJECT_BLOCKS`
  constant, which belongs to a released contract's own change.
