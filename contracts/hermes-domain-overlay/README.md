# hermes-domain-overlay Contract

Status: draft
Ratified by: add-hermes-domain-overlay-contract (on ratification)

The neutral contract for a domain's **seedable Hermes overlay** — the
document the hermes-install `seed-layer-content` verb loads digest-verified
from a domain repo pin (capability `layer-content-seeding`, realized
2026-07-22).

## Files

- `hermes-domain-overlay.schema.yaml` — the overlay shape: domain identity,
  non-empty `approval_scope_kinds` and `required_approval_fields`, and
  `authority_boundaries` (domain-owned list + `xfactory_owns` +
  `repository_owns`).
- `hermes-subject-overlay.schema.yaml` — the SUBJECT layer's overlay shape
  (`kind: hermes_subject_overlay`, add-subject-overlay-contract): subject
  identity (`id`, `subject_kind`, `display_name`), a `policy_namespace`, a
  declared `relation_to_baseline` (single-value enum
  `additive_constraints_only`), and a non-empty `policies` mapping keyed by
  policy id, each entry restating its own `policy_id` and `policy_namespace`
  with an OPEN body. The `subject` block stays open to the domain's own
  identity fields. The kind name is canonical (`subject`) while the runtime
  layer ROLE key stays the frozen `customer`; the mapping is
  `contracts/policies/layer-vocabulary.yaml` `legacy_mapping`, and neither
  side is renamed. INSTANCES LIVE IN DOMAIN REPOSITORIES ONLY — openxFactory
  describes this kind and never hosts one.
- `overlay-descriptor.schema.yaml` — the optional role→path declaration a
  domain repo MAY ship at `hermes/overlay-descriptor.yaml`. Keys are runtime
  layer **roles** (`domain`/`client`/`customer`), deliberately not directory
  names — the customer role's overlay may live under `hermes/subject/`.
- `content-manifest.schema.yaml` — the optional content-set declaration a
  domain repo MAY ship at `hermes/domain/content-manifest.yaml`
  (`kind: hermes_domain_content_manifest`, add-hermes-domain-content-manifest):
  per ratified `content_kind`, exactly one of `path` or `directory`; absent
  manifest, consumers fall back to the documented conventional set the
  hermes-install seeder ships (increment 4a); an undeclared kind never loads
  silently.
- `hermes-layer-template.schema.json` — the subject/tenant Hermes layer
  template shape (kinds `subject_hermes_template` / `client_hermes_template`,
  which carry no top-level domain object; the domain layer stays under
  `hermes-domain-overlay.schema.yaml`). JSON Schema draft 2020-12, retained
  in JSON format as adopted from codexFactory's
  `schemas/hermes-template.schema.json` with a neutralized `$id`
  (DTN-021, adopt-neutral-utility-pack).
- `examples/` — positive reference examples plus self-testing negatives
  (each declares its `# expected_failure:` reason).

## Rules the canonical validator enforces beyond the schema shape

`scripts/validate-hermes-domain-overlay.py` (run from the pinned openxFactory
checkout, never copied):

1. **Domain-owned list naming** — `authority_boundaries` carries exactly one
   domain-owned list named `<domain.id>_owns` (e.g. `codex_owns`), non-empty.
2. **No-overlap** — no authority item appears in more than one boundary list.
3. **Descriptor paths** — declared roles are limited to
   domain/client/customer, and every declared path exists when a domain repo
   path is supplied. A missing descriptor falls back to the documented
   convention: `domain → hermes/domain/overlay.yaml`.
4. **Content-manifest kinds and locations** — declared content kinds are
   limited to the ratified vocabulary, each declares exactly one of
   `path`/`directory`, and every declared location exists when a domain repo
   path is supplied.
5. **Subject policy addressing** — every `policies` key equals its entry's
   `policy_id`, every policy's `policy_namespace` equals the subject's, and no
   two policies declare the same `<policy_namespace>/<policy_id>` address. The
   address is what a consumer resolves, so it must resolve to exactly one
   payload.
6. **The subject prohibited-block list** — a subject overlay ADDS constraints
   and never grants, widens, or waives, so `authority_boundaries`,
   `approval_scope_kinds` and `required_approval_fields` (the Domain layer's
   enforceable slice) are refused anywhere in the document, as is any
   credential VALUE. The invariant is enforced structurally rather than by
   importing the tenant layer's `relation_to_domain: stricter_only`
   comparability engine, whose partial orders are keyed to tenant-policy keys
   and would return `review_required` for every additive named constraint.
7. **Cross-document subject identity** — when a repo path is supplied and the
   repo ships `hermes/subject/template.yaml`
   (`kind: subject_hermes_template`), `subject.subject_kind` must be a
   declared member of `subject_hermes.subject_kinds` and every entry of
   `subject_hermes.required_subject_fields[subject_kind]` must be present and
   non-empty on `subject`. A repo shipping no subject template is skipped with
   notice — no new refusal class.
8. **Kind dispatch at declared paths** — every descriptor-declared path is
   dispatched by the KIND of the document found there, replacing the former
   blanket skip of everything that was not a domain overlay. A kind owned by
   another canonical validator (`hermes_client_overlay` →
   `scripts/validate-client-content.py`) still skips with notice, because two
   implementations of one rule fork canonical meaning; a family-owned kind
   sitting at the wrong role's path is a finding, not a silent pass.

## The enforceable slice a conforming subject overlay contributes

Stated here because the contract owns the DOCUMENT and the slice, while the
consuming install repository owns materialization. A conforming subject
overlay contributes exactly two content payloads:

- `subject_identity` — the declared identity without the policies (`id`,
  `subject_kind`, `display_name`, `policy_namespace`,
  `relation_to_baseline`, plus the domain template's own required identity
  fields).
- `policy_position` — keyed by policy id, reusing the already-ratified
  `policy_position` content kind so a consumer resolving a namespaced address
  reads the same KIND of content whichever layer holds it. Each payload
  restates its own `policy_namespace` and `policy_id`, deliberately: one row
  holds all named policies for the layer, so without the restatement an
  address could only be resolved by joining to the identity record.

Extraction, transaction shape, provenance, digest verification, and the
refusal vocabulary are the consumer's and stay there. A policy entry's
`blocking` flag is a documented convention rather than a validated field —
the policy body is open, and where `blocking` is absent it defaults TRUE; it
must not be used to mark a condition advisory-by-default.

Two seed-time invariants this repository cannot check without a live stack,
stated so the consumer implements a rule rather than inventing one:
`subject.id` equals the `layer_id` of the layer being seeded, and
`subject.policy_namespace` equals that layer's `policy_namespace` exactly.

## Consumers

- **hermes-install seeding (materialization increment)** — replaces its
  minimal structural check with validation against this contract, pinned at
  the `contract-v1.15` release.
- **DomainxFactory validate chains** — invoke the canonical validator against
  their own repo the same way as the other canonical validators.
- **hermes-install subject seeding** (`add-subject-overlay-seeding`) — pins the
  bundle carrying `hermes-subject-overlay.schema.yaml`, dispatches the new kind
  in `domain/overlay_content.py::validate_overlay` and
  `lifecycle/seed_layer_content.py::split_enforceable_slice`, extends its
  `tests/unit/test_contract_parity.py` to COVER the new kind (both of its loops
  filter on `hermes_domain_overlay` today, so subject fixtures would otherwise
  be silently skipped and a green parity run would prove nothing), and enforces
  the two seed-time invariants above.
- **codexFactory** (`add-project-alfa-subject-overlay`) — the first instance,
  at `hermes/subject/project-alfa/overlay.yaml`, declared to the seeder through
  the descriptor's `customer` role.

Provenance: staged topic `openxFactory:staging:layer-content-materialization`;
design basis `ideation/brainstorm/hermes-layer-seeding-mechanism.md`
(Decided 2026-07-22). Realization proof: codexFactory's live 37-authority
overlay passes unmodified.
