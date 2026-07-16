# Tasks: add-client-infrastructure-liaison

Source: the six staged fragments in `supporting-docs/` (moved at the proposal
gate; origin recorded in `supporting-docs/README.md`). Design decisions
locked per the impact map; D1 rules the one fragment divergence. Shared
checkout: explicit paths, `git status -sb` before every commit.

## 1. Provenance and index hygiene

- [x] 1.1 Move the staging fragments into `supporting-docs/` with the origin block recorded (done at the proposal gate; `git mv`, history preserved).
- [x] 1.2 Update `ideation/staging/INDEX.md`: the client-infrastructure-liaison row flips to EXITED 2026-07-16 with the change pointer; section Exit rewritten as record (github-administration-plane pattern).
- [x] 1.3 Cross-reference hygiene resolved by delegation, not regeneration: `validate-ideation-cross-reference.py` runs 0/0 clean post-move; the index's stale member paths are NOT rewritten here because `ideation/cross-reference.yaml` is actively owned by the in-flight `add-ideation-cross-reference-readiness` change (avoiding a cross-session clobber) — the path refresh is recorded in the INDEX exit note as that change's follow-up.

## 2. Contract family (schemas, examples, validator)

- [x] 2.1 Author `contracts/schemas/xfactory-client-infrastructure-request.schema.yaml` (draft 2020-12, per-kind, `contract_schema_version: 1`, `additionalProperties: false`): the six identity-reference classes as `$defs`, `execution_binding.mode` enum per design D1, approval/communication blocks, digest-bearing `package_refs`, closed `status` enum, orthogonal `conditions[]`, embedded `handoff` block, `supersedes_request_ref`, `evidence_refs`.
- [x] 2.2 Author `contracts/schemas/xfactory-infrastructure-readiness-result.schema.yaml`: status enum `ready|degraded|not_ready|unknown|maintenance`, `valid_until`, trust/validator refs, per-check results, signature/traceability refs — never a bare boolean.
- [x] 2.3 Author `examples/client-infrastructure/`: at least one valid request per execution binding (client-managed WITHOUT OpsxFactory, opsxfactory_executed WITH handoff, managed_host), one valid readiness result, plus one-violation-each negatives covering: embedded secret value, subject id in an authority field, actor==authority, illegal transition (liaison marks completed), completed-without-fresh-readiness, escalation-as-state, terminal mutation, digest-less package ref, cancellation-with-unacknowledged-children.
- [x] 2.4 Implement `scripts/validate-client-infrastructure.py` (kind-keyed, skip-with-notice for foreign kinds, packaged-examples self-test per design D6: secret rejection, transition legality + terminal immutability + readiness-gated completion, identity-class separation, idempotency/supersedes integrity) + tests; run clean over `examples/client-infrastructure/`.
- [x] 2.5 Add the family to `contracts/README.md` "Contracts Pending Realization" (schemas + validator rows, realization deferred to the next bundle cut).

## 3. Governing doc and role wiring

- [x] 3.1 Author `docs/client-infrastructure-liaison.md` (Status: draft → ratified by this change): role definition, authority boundary, the three operating models, request lifecycle + transition matrix (the normative prose home), handoff + readiness contracts, activation gate, out-of-band recovery rule, Southside worked scenarios as appendix pointers into `supporting-docs/`.
- [x] 3.2 Link the doc into the README doc index; add the one-line client-tenant routing pointer to `docs/roles-and-authority.md` §External enforcement identity separation (additive, mirrors the promoted-spec delta).
- [x] 3.3 Extend `templates/client-layer/product-service-scaffold.yaml` with the liaison profile block per design D7 (configured-but-inactive default, responsible operator + escalation path required, activation-gate fields, `activation_blocking` trigger) + update `templates/client-layer/README.md`.
- [x] 3.4 Register the liaison in `docs/client-hermes-product-service-scaffold.md` §4 (the canonical Client Hermes role roster it composes from) — the "scaffold AND templates" half of the primary fragment's Required Delta 4 (panel finding, fragment-faithfulness #1).

## 4. Ratification gate

- [x] 4.1 [GATE] Product-owner sign-off on D1 (execution-binding enum tokens) and D5 (roles-authority-model scenario wording) recorded here before the specs are treated as settled. — SIGNED OFF by Brett, 2026-07-16, item-by-item: D1 tokens `client_managed|managed_host|opsxfactory_executed` approved as landed; D5 amended sentence + appended scenario approved as landed; D3 optional `transition` block KEPT OPTIONAL; D4 structural separation (`execution_binding.actor_ref` ≠ `created_by` ≠ `approval.authority_ref` + subject-separation + transition-legality) approved over an identity-keyed check; the three minor implementation choices (per-check `outcome` + required `mandatory`; distinct `vaultref://` grant-ref scheme; quoted example timestamps) approved as a batch. Governing doc flipped to `Status: ratified` + `Ratified by: add-client-infrastructure-liaison` at this gate.
- [x] 4.2 Fresh 2-lens adversarial panel over the whole change (fragment-faithfulness vs supporting-docs + protocol/vocabulary compliance incl. the OpsxFactory consume-don't-rename rule); findings fixed to clean; evidence recorded. — cycle 1 (`wf_3f85acaf-5c3`): 4 findings — BLOCKING `code_surface: none` vs the release-realization code-surface rule (fixed: openxFactory named), plus 3 minor fragment-coverage gaps (canonical scaffold-doc roster → new task 3.4; overdue→escalation scenario added; cancellation-propagation + scope-change-supersede clauses/scenarios added). All fixes are the refuters' own proposed remedies; strict validation green post-fix. A fresh confirmation cycle can run at the 4.1 ratification if requested.
- [x] 4.3 `OPENSPEC_TELEMETRY=0 openspec validate add-client-infrastructure-liaison --strict` and `--all --strict` green (29/29 repo-wide, post-implementation sweep 2026-07-16); change listed in the README "OpenSpec Records" block; `validate-client-infrastructure.py` self-test 4 valid / 9 negatives each failing for its intended reason.

## 5. Realization (per contract-versioning-policy: at the next bundle cut)

- [ ] 5.1 Register the two schemas (`type: schema`, per-file sha256) and the validator (`type: tool`) in `contracts/manifest.yaml`; CHANGELOG entry; move the contracts/README row out of "Pending Realization"; `contracts/releases/contract-vX.Y.digests.yaml` + annotated tag at the allocated bundle version.
- [ ] 5.2 Archive this change with the verified supporting-doc bundle; the per-domain adoption changes (OpsxFactory binding/readiness producer first, then Medx/Ledger/Ad/codex aliases) are proposed as successors per the impact map's sequence.
