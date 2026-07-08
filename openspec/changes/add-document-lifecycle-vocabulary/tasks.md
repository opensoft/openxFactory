# Tasks: Add Document Lifecycle Vocabulary

## 1. Vocabulary Artifact

- [x] 1.1 Write `docs/document-lifecycle.md` stating the lifecycle spine, the
      `Status:`/`Kind:` taxonomy, and the transition gates, referencing this
      change's design mapping table.
- [x] 1.2 Link the new doc from the README documentation index.

## 2. Ratify Existing Process Docs

- [x] 2.1 Move `docs/domain-to-neutral-promotion-process.md` from draft to
      `ratified` status, citing this change.
- [x] 2.2 Move `docs/domain-neutralization-candidate-register.md` to
      `staged` + `Kind: register` and define its alias statuses in terms of
      the lifecycle spine.
- [x] 2.3 Remove the draft caveat from `ideation/README.md` and update both
      ideation brainstorm docs' statuses to taxonomy values.

## 3. Status Header Sweep (openxFactory)

- [x] 3.1 Migrate every `Status:` header in `openxFactory/docs/` to the
      controlled taxonomy per the design mapping table, adding `Kind:` where
      useful.
- [x] 3.2 Demote each "shared xFactory standard" claim to `draft` unless a
      promoted spec backs it; list the demotions in the commit message.
- [x] 3.3 Mark generated reports and simulations as `record`.

## 4. Status Header Sweep (DomainxFactories)

- [ ] 4.1 Sweep `xFactories/codexFactory` docs to the taxonomy.
- [ ] 4.2 Sweep `xFactories/MedxFactory` docs to the taxonomy.
- [ ] 4.3 Sweep `xFactories/OpsxFactory`, `xFactories/LedgerxFactory`, and
      `xFactories/AdxFactory` docs to the taxonomy.
- [ ] 4.4 Seed an `ideation/` area (README only) in each DomainxFactory.

## 5. Validation

- [ ] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes.
- [ ] 5.2 Grep-verify no doc outside promoted-spec backing claims `standard`
      status and no free-form status values remain in swept repos.
- [ ] 5.3 Record the status-checking rules as requirements input for the
      doc-health pipeline implementation proposal (codexFactory).
