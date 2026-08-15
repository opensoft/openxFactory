# Tasks — add-subject-overlay-contract

Legend: **(OPERATOR)** = a human act this change cannot perform;
**TRACKED** = owned by another repository's change, recorded here so the
dependency stays visible and never silently assumed.

## 1. Ratification

- [x] 1.1 **(OPERATOR)** **RATIFIED 2026-08-15 by Brett Heap** — all three
      OQ-1 positions confirmed as written (a/b/c below).
      Original text: Ratify the proposal. Ratification confirms or
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
- [x] 1.2 Strict-validate (`OPENSPEC_TELEMETRY=0 openspec validate
      add-subject-overlay-contract --strict` and `--all --strict`, run from
      the openxFactory root) and list the change in the README's OpenSpec
      Records block.
      (DONE — `Change 'add-subject-overlay-contract' is valid`; `--all
      --strict` → `Totals: 59 passed, 0 failed (59 items)`. Listed in the
      README OpenSpec Records block as the first active change.)

## 2. Implementation (openxFactory — this change's code surface)

- [x] 2.1 Author `contracts/hermes-domain-overlay/hermes-subject-overlay.schema.yaml`
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
      (DONE — `schema_version: 1` / `name: hermes_subject_overlay`, sha256
      `5cd792fb…`. Required `schema_version`/`kind`/`subject`; `subject`
      requires all six declared members with `relation_to_baseline` as the
      single-value enum and `policies` `minProperties: 1`; each policy value
      requires `policy_id` + `policy_namespace` with `additionalProperties:
      true`; `subject.additionalProperties: true`. `id` deliberately carries
      NO neutral pattern — identity spelling is the domain's and is enforced
      against its own template by 2.3, and the domain kind's
      `^[a-z][a-z0-9_]*$` would have refused `project-alfa` on the first
      field. Header records the frozen-`customer` / canonical-`subject`
      mapping citing `layer-vocabulary.yaml` `legacy_mapping` and
      `frozen_identifiers`.)
- [x] 2.2 Extend `scripts/validate-hermes-domain-overlay.py`:
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
      (DONE — (a) `validate_document` gains the `hermes_subject_overlay`
      branch; (b) the role loop moved into `validate_declared_paths`, which
      dispatches on `FAMILY_VALIDATED_KINDS` and keeps the skip-with-notice —
      `hermes_client_overlay` now names its canonical owner
      `scripts/validate-client-content.py`, any other kind prints "no
      canonical validator in this family" — plus a wrong-kind finding when a
      family-owned kind sits at the wrong role's path (design §7's first
      negative); (c) address self-consistency, address uniqueness, the
      prohibited-block list walked RECURSIVELY so a block cannot hide one
      level deeper, and credential values by credential-shaped key or explicit
      issuer marker — no entropy/base64 heuristic, which would have invented a
      refusal class on long opaque identifiers. Proof: `skip role client: …
      (canonical owner: scripts/validate-client-content.py)` and `overlay ok
      (customer): hermes/subject/project-alfa/overlay.yaml` in one run.)
- [x] 2.3 Cross-document conformance: read the domain's
      `hermes/subject/template.yaml` (`kind: subject_hermes_template`) at the
      documented convention path when a repo path is supplied; enforce
      `subject_kind ∈ subject_kinds` and
      `required_subject_fields[subject_kind] ⊆ non-empty keys of subject`;
      **skip with notice when no template exists** — no new refusal class for
      repos that ship none.
      (DONE — `_validate_subject_template` reads
      `hermes/subject/template.yaml`, requires `kind:
      subject_hermes_template`, enforces `subject_kind ∈ subject_kinds` and
      `required_subject_fields[subject_kind] ⊆ non-empty keys of subject`, and
      prints `note: no subject template at hermes/subject/template.yaml;
      skipping cross-document subject identity conformance` when the repo
      ships none. Runs only when a repo path is supplied, so a flat fixture is
      unaffected. No-regression proof: the real codexFactory checkout still
      exits 0 — `overlay ok (domain)`, `repo validation ok: 1 overlay(s)
      validated`.)
- [x] 2.4 Fixtures in the family's self-testing idiom: one
      `examples/hermes-subject-overlay.example.yaml` positive, and negatives
      under `examples/negative/` each declaring `# expected_failure:` —
      at minimum: missing `policy_namespace`; empty `policies`; `policies`
      key ≠ `policy_id`; policy namespace ≠ subject namespace; prohibited
      `authority_boundaries` block; missing `relation_to_baseline`;
      `subject_kind` not declared by the template; template-required field
      missing. The last two need a repo-shaped negative (the family already
      has the `generated-domain-incomplete/` precedent for repo-scoped
      negatives).
      (DONE — one positive `examples/hermes-subject-overlay.example.yaml`
      (two named policies, the domain-declared `owner`/`repositories` identity
      fields) and ELEVEN negatives. Eight document-shaped under
      `examples/negative/`: `subject-missing-policy-namespace`,
      `subject-empty-policies`, `subject-policy-key-mismatch`,
      `subject-policy-namespace-mismatch`,
      `subject-prohibited-authority-boundaries`,
      `subject-missing-relation-to-baseline`, plus two beyond the declared
      minimum — `subject-relaxing-relation` (`stricter_only`, the relation
      this change refuses, caught by the enum rather than passing silently)
      and `subject-credential-value`. Three repo-shaped, following the
      `generated-domain-incomplete/` precedent, each shipping a descriptor, a
      valid domain overlay and a subject template so it fails for exactly one
      reason: `subject-undeclared-kind/`,
      `subject-missing-template-field/`, and
      `subject-wrong-kind-at-subject-path/`. The self-test learned the
      repo-shaped form: a `negative/` directory carrying an overlay descriptor
      is walked through the real declared-path code, with the
      `# expected_failure:` header read from the document at its declared
      subject path.)
- [x] 2.5 Validator green: self-test passes over every packaged positive and
      negative, AND a real domain repo run reports the subject document as
      VALIDATED (not skipped) once codexFactory's instance exists — until
      then, the repo-shaped negative fixture is the standing proof.
      (DONE at the standing-proof level the task defines — `self-test ok: 23
      fixture(s)`, every subject negative failing for its own declared reason
      and no other. The real-instance half stays open by the task's own terms
      until codexFactory `add-project-alfa-subject-overlay` task 2.3 lands
      (tracked at §3.4). Interim proof that a declared subject path is
      VALIDATED rather than skipped: an assembled repo (the packaged positive
      at a descriptor-declared `customer` path + codexFactory's REAL
      `hermes/subject/template.yaml`) reports `overlay ok (customer):
      hermes/subject/project-alfa/overlay.yaml` and `repo validation ok: 2
      overlay(s) validated`, with the tenant document at the `client` path
      still skipped with notice.)
- [x] 2.6 Family README (`contracts/hermes-domain-overlay/README.md`): add the
      new file to the Files list, add the new canonical rules to the
      "Rules the canonical validator enforces beyond the schema shape"
      list, and add the consumer entry.
      (DONE — Files list gains the new schema; the canonical-rules list gains
      rules 5-8 (subject policy addressing, the prohibited-block list, the
      cross-document identity check, kind dispatch at declared paths);
      consumers gain hermes-install `add-subject-overlay-seeding` (including
      the parity-suite trap of design §8) and codexFactory as the first
      instance. A new section records the enforceable slice
      (`subject_identity` + `policy_position`), the `blocking`-defaults-true
      convention as a CONVENTION rather than a validated field, and the two
      seed-time invariants openxFactory cannot check.)
- [ ] 2.7 Contract release, per `docs/contract-versioning-policy.md`:
      `contracts/manifest.yaml` entry + `contracts/CHANGELOG.md` entry +
      minor number allocated LATE (verify the current bundle first; do NOT
      reserve one in the proposal) + digest inventory built with
      `scripts/validate-contract-release.py build` + `verify-commit` +
      `verify-promotion` + annotated tag published and verified. Additive
      only: no released file's bytes change, so existing pins resolve
      byte-identically.
      **PARTIAL, deliberately left unticked — the remainder is merge-gated.**
      Landed on the branch: the `contracts/manifest.yaml` entry
      (`id: hermes-subject-overlay`, sha256
      `5cd792fba0b39a83bae2937ead705397eef324704bca872dc197a80aa786ca72`,
      verified by `scripts/validate-manifest-digests.py`) and the
      `contracts/CHANGELOG.md` entry under **Unreleased — pending bundle
      registration**. NOT done, and must not be done on a branch: the minor
      number is allocated LATE after merge order is known (the policy forbids
      reserving one), `contract_bundle_version` stays at `contract-v1.31`, and
      the digest inventory (`build` / `verify-commit` / `verify-promotion`)
      plus the annotated tag are published against the exact commit that lands
      on `origin/main`.
- [x] 2.8 Root `README.md` doc index unchanged — this change adds no
      standalone doc, only contract-family files that the family README
      indexes.
      (DONE — verified: the only root README edit this change carries is its
      existing OpenSpec Records entry (task 1.2). No standalone doc was added,
      so the doc index needs no entry.)

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
