# Tasks: add-omnigent-domain-overlay

## 1. Contract schemas (openxFactory)

- [ ] 1.1 Author the Omnigent domain-overlay payload schema alongside
      `contracts/hermes-runtime/` (v2 family; consumes
      `overlay-manifest.schema.yaml` for the file-inventory + sha256 +
      `git_overlay_pin` shape): worker-class declarations with archetype
      mapping, the six-boolean generalized permission matrix (constitutional
      `execute_final_action`/`access_secrets` false enforced in-schema),
      credential tiers incl. `never_assignable`, prompt-pack / toolchain /
      validator / preseed / lane-delta sections, and the
      `domain_installation_overlay` operation envelope with
      `stricter_rule_wins`.
- [ ] 1.2 Author the Omnigent install-manifest schema: digest pin of the
      Hermes runtime manifest as stack identity, tenant/domain cardinality,
      subject-workload registry entries (identity ref, activation state,
      validator mode), and compose/verify evidence-record references.
      Canonical `subject`/`tenant`/`domain` spellings throughout.
- [ ] 1.3 Positive and negative fixtures: a conforming overlay + manifest
      pair; rejections for archetype-less worker class, constitutional
      boolean true, loosening overlay, dual domain overlay, identity drift,
      unrendered-profile launch, `never_assignable` grant.
- [ ] 1.4 Validator: extend or add a `scripts/validate-*.py` covering 1.3;
      register new files per the contract versioning policy (holding area
      until the allocated additive release).

## 2. Documentation

- [ ] 2.1 MODIFY `docs/xfactory-domain-factory-model.md`: prescribe the
      DomainxFactory `omnigent/` tree shape (sibling of `hermes/domain/`),
      its payload inventory, and the pin-consumption mechanism; cite this
      change as the ratification record.
- [ ] 2.2 Record the worker archetype vocabulary and permission-matrix
      semantics in the domain-factory model's Omnigent overlay section
      (with the codex and Medx alias examples).
- [ ] 2.3 Link this change in the README OpenSpec Records block; keep the
      staging INDEX row current (done at proposal authoring).

## 3. Gated follow-up changes (filed, not executed in this change)

- [ ] 3.1 `installs/omnigent-install`: manifest quartet +
      `domain_overlays[]` digest pins + cardinality validation + read-only
      compose/verify increment emitting seeding-vocabulary evidence
      (first realization increment; worker-host mutation verbs deferred).
- [ ] 3.2 `installs/hermes-install`: worker-readiness API port and pilot
      `hermes_service/` retirement (cutover shape per the design record's
      open question).
- [ ] 3.3 `xFactories/codexFactory`: author the first `omnigent/` overlay;
      the live coding-patch-worker binding becomes a rendered consequence
      of overlay + params, byte-equivalence proven.
- [ ] 3.4 `xFactories/MedxFactory`: second-domain params fixture rendered
      from the staged overlay draft
      (`ideation/staging/medical-omnigent-overlay/domain-overlay.draft.yaml`)
      without touching core — the pattern-is-real gate for archiving the
      staging topic.
