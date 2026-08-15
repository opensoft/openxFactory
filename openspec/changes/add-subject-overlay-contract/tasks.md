# Tasks — add-subject-overlay-contract

Legend: **(OPERATOR)** = a human act this change cannot perform;
**TRACKED** = owned by another repository's change, recorded here so the
dependency stays visible and never silently assumed.

## 1. Ratification

- [ ] 1.1 **(OPERATOR)** Ratify the proposal. Ratification confirms or
      corrects the three OQ-1 positions codexFactory
      `add-project-alfa-subject-overlay` design §8 assigned to openxFactory,
      because the schema branches on each:
      **(a) OQ-1.1 — kind name.** Position: `hermes_subject_overlay`
      (design D2). Canonical Subject/Tenant/Domain vocabulary, matching the
      `subject_hermes_template` kind already in this family; the descriptor's
      `customer` role key stays frozen and the mapping is recorded in the
      schema header rather than either side being renamed.
      **(b) OQ-1.2 — `id` vs `ref`.** Position: `subject.id` (design D3).
      `client.ref` references a tenant recorded elsewhere; a subject overlay
      declares an identity that exists nowhere else, and the domain templates
      already require `id` — spelling it `ref` would make conforming
      instances fail their own domain's template on the first field.
      **(c) OQ-1.3 — `stricter_only`.** Position: NO (design D4). Require
      `relation_to_baseline: additive_constraints_only` and enforce
      non-relaxation structurally. The tenant comparability engine's partial
      orders are keyed to tenant-policy keys; additive named constraints have
      no counterpart, so every one would return `review_required` and the
      declaration would enforce nothing.
      Ratification also accepts the consequence recorded in proposal Impact:
      codexFactory's authored document reshapes under its own task 2.3.
- [ ] 1.2 Strict-validate (`OPENSPEC_TELEMETRY=0 openspec validate
      add-subject-overlay-contract --strict` and `--all --strict`, run from
      the openxFactory root) and list the change in the README's OpenSpec
      Records block.

## 2. Implementation (openxFactory — this change's code surface)

- [ ] 2.1 Author `contracts/hermes-domain-overlay/hermes-subject-overlay.schema.yaml`
      (`schema_version: 1`, `name: hermes_subject_overlay`): required
      `schema_version` / `kind` / `subject`; `subject` requiring `id`,
      `subject_kind`, `display_name`, `policy_namespace`,
      `relation_to_baseline` (single-value enum
      `[additive_constraints_only]`), and a non-empty `policies` mapping
      keyed by policy id; `additionalProperties: true` on `subject` for
      domain-declared identity fields; each policy value requiring
      `policy_id` + `policy_namespace` with an OPEN body. Header records the
      canonical-`subject` / frozen-`customer` mapping and cites
      `contracts/policies/layer-vocabulary.yaml`.
- [ ] 2.2 Extend `scripts/validate-hermes-domain-overlay.py`:
      (a) `validate_document` dispatches `hermes_subject_overlay`;
      (b) `validate_repo` dispatches by kind at descriptor-declared paths
      instead of blanket-skipping every non-`hermes_domain_overlay` document,
      while RETAINING the skip-with-notice for kinds owned by another
      canonical validator (`hermes_client_overlay` →
      `scripts/validate-client-content.py`);
      (c) deterministic checks the shape cannot express — address uniqueness
      and self-consistency (`policies` key == `policy_id`; policy
      `policy_namespace` == `subject.policy_namespace`), the prohibited-block
      list (`authority_boundaries`, `approval_scope_kinds`,
      `required_approval_fields`, credential values), and the cross-document
      template rule of 2.3.
- [ ] 2.3 Cross-document conformance: read the domain's
      `hermes/subject/template.yaml` (`kind: subject_hermes_template`) at the
      documented convention path when a repo path is supplied; enforce
      `subject_kind ∈ subject_kinds` and
      `required_subject_fields[subject_kind] ⊆ non-empty keys of subject`;
      **skip with notice when no template exists** — no new refusal class for
      repos that ship none.
- [ ] 2.4 Fixtures in the family's self-testing idiom: one
      `examples/hermes-subject-overlay.example.yaml` positive, and negatives
      under `examples/negative/` each declaring `# expected_failure:` —
      at minimum: missing `policy_namespace`; empty `policies`; `policies`
      key ≠ `policy_id`; policy namespace ≠ subject namespace; prohibited
      `authority_boundaries` block; missing `relation_to_baseline`;
      `subject_kind` not declared by the template; template-required field
      missing. The last two need a repo-shaped negative (the family already
      has the `generated-domain-incomplete/` precedent for repo-scoped
      negatives).
- [ ] 2.5 Validator green: self-test passes over every packaged positive and
      negative, AND a real domain repo run reports the subject document as
      VALIDATED (not skipped) once codexFactory's instance exists — until
      then, the repo-shaped negative fixture is the standing proof.
- [ ] 2.6 Family README (`contracts/hermes-domain-overlay/README.md`): add the
      new file to the Files list, add the new canonical rules to the
      "Rules the canonical validator enforces beyond the schema shape"
      list, and add the consumer entry.
- [ ] 2.7 Contract release, per `docs/contract-versioning-policy.md`:
      `contracts/manifest.yaml` entry + `contracts/CHANGELOG.md` entry +
      minor number allocated LATE (verify the current bundle first; do NOT
      reserve one in the proposal) + digest inventory built with
      `scripts/validate-contract-release.py build` + `verify-commit` +
      `verify-promotion` + annotated tag published and verified. Additive
      only: no released file's bytes change, so existing pins resolve
      byte-identically.
- [ ] 2.8 Root `README.md` doc index unchanged — this change adds no
      standalone doc, only contract-family files that the family README
      indexes.

## 3. Consumption evidence — TRACKED, owned by hermes-install `add-subject-overlay-seeding`

Recorded here because the archive gate depends on it, and NOT claimed as this
change's work. The same discipline codexFactory's change applied to its own
prerequisites.

- [ ] 3.1 **TRACKED** hermes-install pins the released bundle: the new schema
      copied into `config/contracts/hermes-domain-overlay/` with its sha256
      in `manifest.yaml` and `contract_bundle_tag` advanced from
      `contract-v1.18` to the tag from 2.7.
- [ ] 3.2 **TRACKED** hermes-install extends
      `tests/unit/test_contract_parity.py` to COVER the new kind. Both of its
      loops currently `continue` past any fixture whose kind is not
      `hermes_domain_overlay`, so new subject fixtures are silently ignored
      and a green run would prove nothing. Parity green over the new
      positives and negatives is the evidence this task exists to produce.
- [ ] 3.3 **TRACKED** hermes-install dispatches the kind in
      `domain/overlay_content.py::validate_overlay` (today: two kinds, else
      `no validator for overlay kind …`) and
      `lifecycle/seed_layer_content.py::split_enforceable_slice` (today:
      client branch, else `doc["domain"]`), and enforces the two seed-time
      invariants openxFactory cannot check without a live stack:
      `subject.id` == the seeding `layer_id`, and `subject.policy_namespace`
      == that layer's `policy_namespace`.
- [ ] 3.4 **TRACKED** codexFactory `add-project-alfa-subject-overlay` task
      2.1 ticks with the released tag recorded, and its task 2.3 reshapes the
      authored document to the ratified contract
      (`relation_to_domain: stricter_only` → `relation_to_baseline:
      additive_constraints_only`; each named policy gains `policy_namespace`
      and `policy_id`).

## 4. Records and archive gate

- [ ] 4.1 Keep the change listed in the README's OpenSpec Records block with
      its status current, and record the released tag there once 2.7 lands.
- [ ] 4.2 Confirm `openspec validate add-subject-overlay-contract --strict`
      and `--all --strict` stay clean through ratification and any amendment.
- [ ] 4.3 Notify the trackers when 2.7 lands: codexFactory
      `add-project-alfa-subject-overlay` §2, hermes-install
      `add-subject-overlay-seeding`, and the staged topic
      `openxFactory:staging:subject-establishment` (DTN-017) — related, not
      blocking; this contract is the landing surface its realization artifact
      writes to, which is worth recording in the topic when it next iterates.
- [ ] 4.4 Archive per the `target_release` gate: ratified with the OQ-1
      positions confirmed; schema, fixtures and validator extension landed
      with the canonical validator green; the bundle released with a verified
      annotated tag, manifest, changelog and digest inventory; and CONSUMED —
      §3.1 and §3.2 done, with a parity suite that actually covers the new
      kind. A ratified contract that nothing validates and nobody pins is not
      realized, and does not archive.
