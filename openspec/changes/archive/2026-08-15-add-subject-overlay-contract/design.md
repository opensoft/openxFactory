# Design — add-subject-overlay-contract

Every claim below was read at authoring time against the checked-out sources;
file and symbol names are given so a reviewer can re-verify without trusting
this document. The three D-sections are the OQ-1 sub-questions codexFactory
`add-project-alfa-subject-overlay` design §8 left open and explicitly assigned
to openxFactory. Each states a POSITION; ratification confirms or corrects it.

## 1. The gap, re-verified in this repository

Sources: `contracts/hermes-domain-overlay/*.schema.yaml`,
`contracts/client-content/*.schema.yaml`,
`scripts/validate-hermes-domain-overlay.py`,
`contracts/policies/layer-vocabulary.yaml`.

| Claim | Evidence read |
|---|---|
| The domain kind cannot host a subject | `hermes-domain-overlay.schema.yaml` — `kind` is `enum: [hermes_domain_overlay]`; `required: [schema_version, kind, domain]`; `domain` requires `id` (`^[a-z][a-z0-9_]*$`), `display_name`, non-empty `approval_scope_kinds`, non-empty `required_approval_fields`, `authority_boundaries` with `xfactory_owns` + `repository_owns` |
| The tenant kind cannot carry a named policy address | `client-overlay.schema.yaml` requires `client: {ref, display_name, policy_overrides}`; `client-policy-overrides.schema.yaml` requires `relation_to_domain` + `policy`, and `policy` enumerates exactly seven properties. No `policy_namespace`, no policy id, anywhere in the family |
| The declared subject path is ungoverned | `validate-hermes-domain-overlay.py::validate_repo` lines ~295-307: it resolves `role_paths`, checks the file EXISTS, then `if kind != "hermes_domain_overlay": print(f"skip role {role}: … (not a domain overlay)"); continue` |
| The family expected this | `overlay-descriptor.schema.yaml` `overlay_paths` properties are `domain|client|customer` with a comment naming `hermes/subject/`; `validate-hermes-domain-overlay.py` `DESCRIPTOR_ROLES = {"domain","client","customer"}` |
| The family already owns subject vocabulary | `hermes-layer-template.schema.json` governs `subject_hermes_template` and `client_hermes_template`; codexFactory `hermes/subject/template.yaml` declares `subject_kinds: [project, repository, product, feature_initiative]` and `required_subject_fields.project: [id, owner, repositories]` |

The missing piece is precisely one document kind: the **instance** of a
declared subject kind, carrying addressable named policies.

## 2. D1 — The kind is `hermes_subject_overlay` (OQ-1.1)

**Position: `hermes_subject_overlay`.**

1. **The canonical layer vocabulary is Subject/Tenant/Domain**
   (`contracts/policies/layer-vocabulary.yaml`, ratified
   `adopt-subject-tenant-domain-vocabulary` 2026-07-23), and the promoted
   `layer-vocabulary` requirement *Machine identifier freeze and mapping*
   says plainly: *"New contract families authored after adoption use the
   canonical vocabulary from their first version."*
2. **This family already carries both spellings, by rule, and the precedent
   points the same way.** The descriptor's role KEY stays `customer` — a
   released, frozen runtime identifier. The family's newest schema,
   `hermes-layer-template.schema.json`, names its kind `subject_hermes_template`
   with canonical spelling. A subject overlay is the instance of that template,
   so it takes the same spelling; `hermes_<layer>_overlay` is the family's
   overlay-kind idiom (`hermes_domain_overlay`, `hermes_client_overlay`).
3. **The mapping is stated in the contract rather than left to the reader.**
   The schema header records explicitly: this kind is seeded at the layer
   whose runtime `role` is the frozen key `customer`, which
   `layer-vocabulary.yaml` `legacy_mapping` resolves to the canonical
   `subject` layer. Neither side is renamed — the descriptor keeps `customer`,
   the new kind uses `subject`, and the bridge is written down where a
   consumer will trip over it.

**Rejected: `hermes_customer_overlay`.** It matches the descriptor role key,
which is its only virtue. It would introduce a NEW frozen-legacy identifier
after adoption, which the reserved-terms requirement forbids for new
surfaces, and it would sit in the same directory as `subject_hermes_template`
describing the same layer under a different name.

## 3. D2 — Subject identity uses `id`, not `ref` (OQ-1.2)

**Position: `subject.id`.** The two precedents genuinely disagree, so the
tie-break is which one this document IS.

- **`client.ref` is a REFERENCE.** In `hermes_client_overlay`, `ref` names a
  tenant whose record lives elsewhere — it is the key of the install-repo path
  `config/clients/<client_ref>/overlay.yaml`. The document points at an
  identity it does not define.
- **A subject overlay DECLARES.** It is the subject's authored record in the
  domain repo; there is no prior registry entry it defers to. `id` is the
  honest spelling for a declaration, and it is what
  `subject_hermes_template.required_subject_fields.project` — `[id, owner,
  repositories]` — already names.
- **The decisive reason is mechanical, not aesthetic.** D4's cross-document
  rule enforces `required_subject_fields[subject_kind] ⊆ keys(subject)`. If
  the neutral instance spelled identity `ref`, then every domain whose
  template requires `id` (codexFactory's does, for all four of its subject
  kinds) would fail its own template on the first field — and openxFactory
  would be publishing a template whose conforming instances cannot satisfy it.
  Choosing `ref` would mean choosing to weaken or drop the cross-document
  rule, which is the single highest-value check in this contract.
- **Nothing is renamed.** `client.ref` stays exactly as released; this is a
  new kind choosing its own field, not a migration.

**Additional invariant, stated but NOT validated here:** `subject.id` equals
the `layer_id` of the layer being seeded, and `subject.policy_namespace`
equals that layer's `policy_namespace` exactly. openxFactory cannot see a live
stack, so these are consumer-side seed-time checks (`add-subject-overlay-seeding`);
the contract states them as requirements so the consumer implements a rule
rather than inventing one.

## 4. D3 — `stricter_only` does NOT apply; the subject invariant is `additive_constraints_only` (OQ-1.3)

**Position: do not import the client comparability mechanism. Require a
declared `relation_to_baseline: additive_constraints_only` and enforce
non-relaxation STRUCTURALLY.**

**Why `stricter_only` would be decorative here.** `stricter_only` is a
COMPARABILITY invariant, and comparability needs a baseline of the same shape.
`scripts/validate-client-content.py` implements it as a key-by-key walk with
defined partial orders — allowlists `⊆`, denylists `⊇`, numeric ceilings `≤`,
add-only conjunctive envelopes, ordered enums at-or-above the baseline rung —
and *"anything else with no defined partial order: verdict `review_required`,
never a silent pass."* A subject's admission conditions are **additive named
constraints with no domain counterpart key**: `packet-digest-binding` does not
narrow a domain allowlist, it adds a refusal. Run through the client engine,
every condition lands in `review_required`. The document would carry the
strongest-sounding word in the family and enforce nothing — the exact failure
mode this contract exists to avoid (a green check that is true and
misleading).

**Why the comparand is wrong as well.** `relation_to_domain` names the domain
alone. A subject sits under a COMPOSED baseline: the runtime's seeding-order
invariant is domain → client → subject (`_ROLE_PREREQUISITES` in
`seed_layer_content.py`), and the neutral composition rule in the sibling
Omnigent family is `stricter_rule_wins`. Declaring a relation to the domain
would assert a comparison against the wrong document even where a comparison
existed.

**What IS enforceable, and is therefore what the contract requires.** The real
invariant is *a subject may add constraints; it may never grant, widen, or
waive*. That is checkable structurally, on the document alone, with a hard
failure rather than a deferral:

1. `relation_to_baseline` is a required single-value enum
   `[additive_constraints_only]` — the same shape discipline as
   `relation_to_domain: [stricter_only]`, so the position is declared in the
   document and a later relation can be added without a breaking change.
2. The validator refuses a prohibited-block list: `authority_boundaries`,
   `approval_scope_kinds`, `required_approval_fields` (the Domain layer's
   slice — a subject that carried them would be legislating for the domain),
   and any authority-granting / permission-widening / credential-value block.
3. A named policy's entries are constraint-shaped: each carries an `id` and
   states a condition; `blocking` defaults true where absent and MUST NOT be
   used to mark a condition advisory-by-default.

**Consequence for the pending instance, recorded honestly:** codexFactory's
design §7 draft carries `relation_to_domain: stricter_only`. Under this
position it becomes `relation_to_baseline: additive_constraints_only`. That
change's task 2.3 already sanctions exactly this reshape ("expected, not a
failure — the contract is openxFactory's to decide").

## 5. D4 — Identity conforms to the DOMAIN's template, not to a neutral field list

The neutral schema requires only what is neutral: `id`, `subject_kind`,
`display_name`, `policy_namespace`, `relation_to_baseline`, `policies`. It sets
`additionalProperties: true` on `subject` (the same choice
`hermes-layer-template.schema.json` already makes) because per-domain identity
fields differ — codexFactory's `repository` kind needs `check_profile` and
`reviewer_group`; MedxFactory's patient kind will need neither.

The domain's own requirements are enforced by CROSS-DOCUMENT validation, when
a repo path is supplied:

- convention path `hermes/subject/template.yaml` (`kind:
  subject_hermes_template`), mirroring the family's existing
  convention-then-contract idiom;
- `subject.subject_kind` MUST be a member of `subject_hermes.subject_kinds`;
- every entry of `subject_hermes.required_subject_fields[subject_kind]` MUST
  be a present, non-empty key of `subject`;
- **no template, no new refusal class** — the validator prints a
  skip-with-notice, exactly as it does for an absent descriptor or content
  manifest. Repos without a subject template are not retroactively broken.

This is how `project` gets `id`/`owner`/`repositories` enforced without a
single engineering field name entering a domain-neutral contract.

## 6. The enforceable slice, and where openxFactory stops

`hermes_layer_content` has primary key `(layer_id, content_kind)` with a
JSONB `enforceable_payload` (hermes-install `migrations/0009_layer_content.sql`),
so a slice is a mapping of content kind → payload, one row each.

A conforming subject overlay contributes exactly two:

```yaml
subject_identity:                 # the declared identity, minus the policies
  id: …
  subject_kind: …
  display_name: …
  policy_namespace: …
  relation_to_baseline: additive_constraints_only
  # plus the domain's own template-required identity fields
policy_position:                  # keyed by policy id
  <policy-id>:
    policy_namespace: …           # restated in the payload, deliberately
    policy_id: <policy-id>
    …the domain-owned policy body…
```

Three deliberate choices:

1. **`policy_position` is reused, not invented.** It is already a ratified
   content kind on the domain path (`domain_content_set.py::CONTENT_DIRECTORIES`
   maps `policies → policy_position`; the same token is in the canonical
   validator's `CONTENT_KINDS`). A lens resolving `<namespace>/<policy-id>`
   then reads the same KIND of row whichever layer it is reading, which is the
   whole point of a namespaced address.
2. **Each payload restates its own namespace and id.** One row holds all named
   policies for the layer, so without the restatement an address could only be
   resolved by joining to the `subject_identity` row. Self-addressing rows make
   `N/P` resolvable from the row alone.
3. **Nothing about mechanics is specified here.** Extraction from the archive,
   the delete-then-insert transaction, provenance columns, digest verification,
   and the refusal vocabulary are hermes-install's and stay there. openxFactory
   owns document shape and canonical validation; the consumer owns
   materialization. The line is drawn at: *what a conforming document
   contributes* (ours) vs *how the rows get written* (theirs).

**Not specified, deliberately:** who performs the `policy_refs` →
`hermes_layer_content` join at read time. Nothing in hermes-install resolves
`policy_refs` today (it is parsed onto the manager-profile binding and never
joined); the join is worker-side. This contract makes the address RESOLVABLE;
it does not assign the resolver.

## 7. Validator extension

`scripts/validate-hermes-domain-overlay.py`:

- `validate_document` gains a `hermes_subject_overlay` branch alongside the
  three existing kinds.
- `validate_repo` stops blanket-skipping. Today: any declared path whose kind
  is not `hermes_domain_overlay` is skipped. After: dispatch by kind — domain
  kind → domain rules, subject kind → subject rules, **anything else keeps
  today's skip-with-notice** (a `hermes_client_overlay` at a declared `client`
  path is governed by `scripts/validate-client-content.py`, and quietly
  double-validating it here would fork canonical meaning).
- New deterministic checks the schema shape cannot express: address uniqueness
  and self-consistency (`policies` key == `policy_id`; every policy's
  `policy_namespace` == `subject.policy_namespace`), the prohibited-block list
  (D3), and the cross-document template conformance (D4).
- Fixtures follow the family's self-testing idiom: one
  `hermes-subject-overlay.example.yaml` positive, and negatives each declaring
  `# expected_failure:` — at minimum: wrong kind at a declared subject path,
  missing `policy_namespace`, empty `policies`, policy key ≠ `policy_id`,
  policy namespace ≠ subject namespace, a prohibited `authority_boundaries`
  block, a `subject_kind` not declared by the template, and a
  template-required field missing.

## 8. Consumer parity — the trap worth naming

hermes-install holds its in-process rules to VERDICT PARITY with this
validator via `tests/unit/test_contract_parity.py`. That suite currently
filters both loops with `if … doc.get("kind") != "hermes_domain_overlay":
continue`. **New subject fixtures are therefore silently skipped by it.** A
consumer that pins the release, adds its dispatch branch, and reports a green
parity run has proven nothing about the new kind unless the suite is extended
to cover it. Tracked as task 3.2, owned by `add-subject-overlay-seeding`.

## 9. Release shape

Additive: one new file, plus an extended validator, README, manifest,
changelog and digest inventory. No released file's bytes change, so every
existing pin (including hermes-install's `contract-v1.18` pinned copy of the
three schemas) resolves byte-identically until it chooses to re-pin. The minor
number is allocated LATE, at realization, per `docs/contract-versioning-policy.md`
— this proposal reserves none.

## 10. Risks and rollback

- **Risk: the position on `stricter_only` is wrong and subjects DO need
  comparability.** Mitigated by shape: `relation_to_baseline` is a
  single-value enum, so a future `stricter_only_vs_composed_baseline` relation
  is an additive enum widening plus a comparability engine, not a breaking
  change to authored documents.
- **Risk: the cross-document template check breaks a domain repo that has a
  subject template but no subject overlay.** It cannot: the check runs only
  when a subject overlay exists at a declared path, and an absent template is
  a skip-with-notice.
- **Risk: the contract ratifies and no consumer pins it.** Visible by
  construction — the `target_release` gate requires a pinned consumer with a
  parity suite that actually covers the kind, so an unconsumed contract cannot
  be archived as delivered.
- **Rollback:** the release is additive and the validator extension is
  dispatch-only; reverting the schema file and the dispatch branch returns
  `validate_repo` to its current skip behaviour, with no other kind affected.

## 11. Open questions

- **OQ-A — should `subject_identity` be added to the ratified content-kind
  vocabulary?** `CONTENT_KINDS` in the canonical validator governs the DOMAIN
  content manifest's declarable kinds; `hermes_layer_content.content_kind` is
  free TEXT with no such closure. They are different vocabularies today. This
  change treats them as different and adds nothing to `CONTENT_KINDS`. If the
  two are later unified, `subject_identity` is the first entry that would need
  registering.
- **OQ-B — a subject CONTENT MANIFEST.** v1 carries policies INLINE because a
  subject content SET does not exist (`load_domain_content_set` sweeps
  `hermes/domain/<dir>` only, so a `hermes/subject/<id>/policies/` directory
  would be unloaded content that drifts). The symmetric successor to
  `hermes_domain_content_manifest` is named as future work, not smuggled in.
- **OQ-C — multiple subjects per domain repo.** The descriptor declares ONE
  path per role, so one repo currently declares one seedable subject document.
  codexFactory's `project-bravo` will surface this. Options (a repeated role,
  a per-subject descriptor, or a directory form) are not decided here; nothing
  in this contract's shape forecloses any of them.
