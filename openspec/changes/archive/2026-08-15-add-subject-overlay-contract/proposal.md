---
code_surface: openxFactory — `contracts/hermes-domain-overlay/hermes-subject-overlay.schema.yaml` (NEW), one positive example plus indexed negative fixtures under `contracts/hermes-domain-overlay/examples/`, an extension of the canonical validator `scripts/validate-hermes-domain-overlay.py` (dispatch the new kind at descriptor-declared subject paths, replacing today's blanket skip), the family `README.md`, and the release surface `contracts/manifest.yaml` + `contracts/CHANGELOG.md` + `contracts/releases/<tag>.digests.yaml`. NO instance document is authored here — instances live only in domain repos (codexFactory `hermes/subject/`, ruling D1). NO hermes-install code changes: the seeder dispatch is the parallel consumer change `add-subject-overlay-seeding`.
target_release: contract-v<next minor> — allocated LATE at realization per `docs/contract-versioning-policy.md` (v1.31 is the current bundle; a proposal MUST NOT reserve a minor number before merge order is known). Archives only on ALL of: ratified with the OQ-1 positions confirmed; schema, fixtures and validator extension landed on openxFactory main with `validate-hermes-domain-overlay.py` green (self-test + a real domain repo); the bundle released — manifest, changelog, digest inventory, and a verified annotated tag; and CONSUMED — hermes-install pinning that release and its CI parity suite green over the new kind. A contract nothing validates and nobody pins is not realized.
Status: ratified
Ratified: Brett Heap, reviewer of record, 2026-08-15 — the three OQ-1
positions confirmed as written: kind `hermes_subject_overlay` (D2), identity
`subject.id` (D3), `stricter_only` refused in favor of
`relation_to_baseline: additive_constraints_only` with structural
non-relaxation (D4).
---

# Proposal: add-subject-overlay-contract

## Why

**A live Hermes layer is pointed at a document that no contract in this
repository can describe, and the canonical validator says so out loud by
skipping it.**

codexFactory's `add-project-alfa-subject-overlay` (ratified 2026-08-15)
authors a Subject Hermes overlay at `hermes/subject/project-alfa/overlay.yaml`
and declares it to the seeder through `hermes/overlay-descriptor.yaml` under
the `customer` role. The `project-alfa` seat's manager-profile binding in
hermes-install already addresses its standing policy as
`opensoft.codexfactory.project-alfa/admission-conditions` — a
`<namespace>/<policy-id>` address. **Neither existing overlay kind can carry
that address**, and each fails for its own structural reason:

- **`hermes_domain_overlay`** fixes `kind` to the single-value enum
  `[hermes_domain_overlay]` and requires a top-level `domain` block with
  `id` (pattern `^[a-z][a-z0-9_]*$`), `display_name`, non-empty
  `approval_scope_kinds`, non-empty `required_approval_fields`, and
  `authority_boundaries` closing over exactly one `<domain.id>_owns` list.
  A project is not a domain; using this kind fabricates a domain and its
  authority-boundary closure, and its enforceable slice
  (`approval_scope` + `authority_boundary`) carries no policy at all.
- **`hermes_client_overlay`** requires `client.policy_overrides`, whose
  contract `client-content/client-policy-overrides.schema.yaml` enumerates a
  **closed set** — `repo_boundaries`, `realization`, `credential_posture`,
  `budget_envelopes`, `tracking_granularity`, `security_posture`,
  `auto_clear_envelope` — and carries **no policy namespace and no
  named-policy identity anywhere**. `admission-conditions` has no home in it,
  and `client` is the frozen v1 machine spelling of the **Tenant** layer
  (`contracts/policies/layer-vocabulary.yaml`), so writing one into a Subject
  layer would file the document under the wrong layer to clear a checkbox.

- **The canonical validator confirms the gap by silence.**
  `scripts/validate-hermes-domain-overlay.py::validate_repo` walks the
  descriptor-declared role paths and, for any document whose kind is not
  `hermes_domain_overlay`, prints `skip role customer: … (not a domain
  overlay)` and moves on. The declared path's EXISTENCE is checked; its
  CONTENT is governed by nothing.

The family was built expecting this. `overlay-descriptor.schema.yaml` already
accepts the `customer` role key and its own comment anticipates the exact
location — *"the customer role's overlay may live under `hermes/subject/`,
per the 2026-07-22 naming decision"* — and the family already owns
`hermes-layer-template.schema.json`, whose `subject_hermes_template` kind
declares a domain's subject KINDS and their required fields. What is missing
is the INSTANCE contract: the document that instantiates one subject of one
declared kind and carries its addressable named policies.

## What Changes

- **ADD `contracts/hermes-domain-overlay/hermes-subject-overlay.schema.yaml`**
  — the neutral shape for `kind: hermes_subject_overlay`: subject identity
  (`id`, `subject_kind`, `display_name`, plus the domain's own required
  fields), the layer's `policy_namespace`, a declared
  `relation_to_baseline`, and `policies` — a mapping keyed by policy id, each
  value a named policy document whose BODY is domain-owned and open.
- **ADDRESSABILITY IS THE POINT.** For a subject whose namespace is `N`, every
  policy id `P` under it resolves the address `N/P` to exactly one enforceable
  payload; ids are unique within the document; each payload restates its own
  `policy_namespace` and `policy_id` so a materialized row is address-resolvable
  without joining to a sibling row. The neutral contract **MUST NOT enumerate
  policy names** — enumerating them is precisely the flaw that makes the tenant
  policy contract unable to carry this one.
- **ENFORCE IDENTITY AGAINST THE DOMAIN'S OWN TEMPLATE, NOT AGAINST A NEUTRAL
  FIELD LIST.** The canonical validator reads the domain's
  `hermes/subject/template.yaml` (`kind: subject_hermes_template`, already in
  this family) and enforces that `subject.subject_kind` is one of its declared
  `subject_kinds` and that every entry of
  `required_subject_fields[subject_kind]` is present. codexFactory's `project`
  kind therefore requires `id`, `owner`, `repositories` **because codexFactory
  says so**, not because openxFactory hard-coded engineering field names into
  a neutral contract.
- **ADD A NON-RELAXATION INVARIANT, AND DO NOT IMPORT THE CLIENT MECHANISM.**
  A subject overlay declares `relation_to_baseline: additive_constraints_only`
  and the validator refuses domain-authority blocks
  (`authority_boundaries`, `approval_scope_kinds`,
  `required_approval_fields`), authority-granting or permission-widening
  blocks, and credential values. The client layer's
  `relation_to_domain: stricter_only` comparability engine is deliberately NOT
  reused — see design D3 and OQ-1.3.
- **EXTEND THE CANONICAL VALIDATOR** so a descriptor-declared subject path is
  VALIDATED instead of skipped, while any other kind at a declared path keeps
  today's skip-with-notice (the client family has its own canonical
  validator). Ship one positive example and indexed negatives, each declaring
  its `# expected_failure:` reason, in the family's existing self-test idiom.
- **SPECIFY THE ENFORCEABLE SLICE, AND STOP AT THE BOUNDARY.** The contract
  states WHAT a subject overlay contributes as enforceable content — a
  `subject_identity` payload and a `policy_position` payload keyed by policy
  id — so a consumer has a stated contract to split against. HOW it is
  materialized (extraction, transaction shape, provenance columns) stays
  hermes-install's, in `add-subject-overlay-seeding`.
- **PUBLISH AS A VERSIONED ADDITIVE BUNDLE** so hermes-install can digest-pin
  the new copy alongside the three files it already pins at `contract-v1.18`.

## Capabilities

### Modified Capabilities

- `hermes-domain-overlay`: six ADDED requirements — the neutral
  `hermes_subject_overlay` shape; namespace/policy-id addressability with no
  closed policy-name enum; subject identity conformance to the domain's own
  subject template; the additive-constraints-only non-relaxation invariant;
  canonical validation of descriptor-declared subject paths (replacing the
  blanket skip); and the specified enforceable slice with the ownership
  boundary between document shape and materialization mechanics.

## Impact

- **openxFactory**: one new schema, fixtures, a validator extension, a family
  README entry, and one bundle release. No existing schema, fixture, or
  released digest changes — the release is additive, so every current pin
  resolves byte-identically.
- **hermes-install** (CONSUMER, not this change's surface):
  `add-subject-overlay-seeding` pins the release, adds the third branch to
  `domain/overlay_content.py::validate_overlay` (today: two kinds, else
  `no validator for overlay kind …`) and to
  `lifecycle/seed_layer_content.py::split_enforceable_slice`, and — the part
  that is easy to miss — **extends `tests/unit/test_contract_parity.py`**,
  which today `continue`s past any fixture whose kind is not
  `hermes_domain_overlay`. Left unextended, the parity suite would ignore
  every new fixture and report green while proving nothing about the new
  kind.
- **codexFactory** (INSTANCE HOLDER): `add-project-alfa-subject-overlay`
  task 2.1 closes when this ratifies and its tag is recorded; its task 2.3
  already anticipates a mechanical reshape of the authored document if the
  ratified contract differs from that change's design §7 sketch — and under
  the OQ-1 positions below, it does (`relation_to_domain: stricter_only` →
  `relation_to_baseline: additive_constraints_only`; each named policy gains
  its own `policy_namespace`/`policy_id`).
- **Related, NOT blocking**: staged topic
  `openxFactory:staging:subject-establishment` (DTN-017), whose second
  consumer is DECIDED as codexFactory new-project. That topic designs the
  neutral PIPELINE by which a subject comes into being; this change gives its
  output a landing surface — the document a subject-establishment realization
  writes, and the address a lens later reads. It stays gated on LedgerxFactory
  reaching proposal and is cited here as context, not as a dependency.
- **Out of scope**: any instance document; a subject CONTENT MANIFEST (the
  symmetric follow-up to `hermes_domain_content_manifest` — a subject content
  SET does not exist, which is why v1 policies live inline); widening
  `resolve_pin`'s compatibility-manifest sections to add `customer_overlays`
  (hermes-install's, recorded as OQ-3 of the consumer change); and any
  runtime join from `policy_refs` to a materialized row (worker-side; see
  design §5).
