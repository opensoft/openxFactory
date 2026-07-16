# Tasks: Possibles Derivation Lane

Governance tasks (sections 1-2, openxFactory contract) come first; realization
tasks (sections 3-4, codexFactory + aggregation + omnigent-install Speckit work)
are marked as such and are NOT done by authoring this change.

## 1. Origin And Contract Baseline (openxFactory governance)

- [ ] 1.1 Verify the `.openspec.yaml` ad-hoc origin (`kind: ad_hoc`, id `openxFactory:adhoc:possibles-derivation-lane`, reason + `approved_by` + `approved_on`) is complete and that no organized staging fragment for the derive-possibles surface exists that ad-hoc status would improperly substitute for.
- [ ] 1.2 Confirm the register-kernel delta (section 2) is ADDITIVE ONLY — optional `origin` + a `derivation` $def, no loosened `required`, no retyped field — so no `contract_schema_version` bump is warranted; record the additive determination.
- [ ] 1.3 Run `OPENSPEC_TELEMETRY=0 openspec validate add-possibles-derivation-lane --strict` and `--all --strict`; both pass before commit.

## 2. Register Contract Delta (openxFactory)

- [ ] 2.1 Add the additive delta to `contracts/schemas/ideation-possibles-register.schema.yaml`: optional `register_entry.origin` (enum `[human-authored, ai-derived]`; absent = human-authored), optional `register_entry.derivation` ($ref a new `$defs/derivation`), and an `allOf` conditional requiring `derivation` when `origin: ai-derived` — modelled one-for-one on `topic_entry.origin` + the `human_seen` conditional. Update the kernel description to document the AI-derivation sibling of human-seen intake and confirm the no-bump additive posture.
- [ ] 2.2 Define `$defs/derivation`: required `worker_run` (`correlation_id`, `worker_profile`, `prompt_contract_version`, all non-empty strings) + required `disposition` (`const: pending_review`) + optional `human_disposition` (documented structural mirror of the index schema's `human_disposition`: `outcome` accepted|rejected|deferred, `authority`, optional `at` date + `note`) — a local mirror, NOT a `$ref` back into the index schema (avoids a circular reference).
- [ ] 2.3 Add a packaged derived-possible example under `examples/ideation-cross-reference/` (or the register example set it reuses): a valid `origin: ai-derived` entry with a `derivation.worker_run`, `pending_review` disposition, `claiming_clusters`, and `supporting_evidence`; plus a negative that fails for a missing worker run / missing source citation. Prove valid/negative against the four-schema co-load registry.
- [ ] 2.4 Extend `scripts/validate-ideation-dashboard-contracts.py` (the delegated register validator per the kernel's C3 ownership line) to enforce: `origin: ai-derived` requires a `derivation` block; a derived entry cites at least one `claiming_clusters` edge AND one `supporting_evidence` pin; machine output is `disposition: pending_review` only; the one-way disposition lifecycle (accept -> `latent` retaining `origin`, reject -> `rejected` with reason+citation, no edit back to `pending_review`, no resurrection); `id` uniqueness across the register including derived entries. Add validator tests.
- [ ] 2.5 Note the delegation in `scripts/validate-ideation-cross-reference.py` (register-entry shape/transitions remain delegated to the dashboard-contracts validator) without duplicating the checks, and add an additive "AI-derived possibles" pointer to `ideation/README.md`'s Cross-Reference Readiness Index section, referencing this change's requirements without restating SHALL/MUST wording.
- [ ] 2.6 Register the delta at realization in `contracts/manifest.yaml` / `contracts/CHANGELOG.md` / `contracts/README.md` (avatar-client / document-cataloging precedent: registration at the realization commit after merge order is known), not before.

## 3. Derivation Worker (codexFactory Speckit realization)

Realization follows the ideation-readiness two-repo split; this section is
codexFactory Spec Kit work, not done by authoring this change.

- [ ] 3.1 Add the derive-possibles worker module with a versioned prompt contract that reads the index (topic clusters, staged topics, member documents) and proposes candidate possibles (title, claim, rationale prose only).
- [ ] 3.2 Stamp orchestration-computed identity and evidence on every proposal (register `id`, correlation id, passage/content hashes, counts); discard and never trust worker-supplied precision values; void proposals whose worker precision values disagree.
- [ ] 3.3 Require and validate the register evidence contract before persistence: `origin: ai-derived`, `derivation.worker_run` + `pending_review`, at least one `claiming_clusters` edge and one `supporting_evidence` pin, and a `provenance` citing the primary source member + cluster context; reject unsourced or malformed proposals.
- [ ] 3.4 Implement the next-run merge into `possibles_register` under concurrency protection against stale overwrite, preserving `id` uniqueness and never editing a disposed entry; wire human gate-console dispositions (accept -> latent, reject -> rejected with reason+citation, defer) into the merge.
- [ ] 3.5 Enforce the non-mutating bound: the pass writes only the `possibles_register` section and evidence artifacts; add tests proving any other write path is rejected and that source documents are never modified.

## 4. Nightly Lane (xFactory aggregation, omnigent-install — realization)

- [ ] 4.1 Wire the possibles-derivation lane into the nightly run after the deterministic pass, consuming the same inventory/index snapshot; a skipped or failed lane is reported as skipped and never affects deterministic results; derived possibles appear in their own report section, excluded from the Ranked Plan.
- [ ] 4.2 Add the watchdog: report and cancel a derivation child queued beyond ten minutes or running beyond thirty minutes; prove offline/unauthorized/partial/invalid/failed worker output cannot delay or suppress deterministic reporting.
- [ ] 4.3 Add the bounded read-only `derive-possibles` profile in omnigent-install reusing the existing document-analysis host pattern, with workload-specific readiness assertions and no repository credentials in the worker environment.
- [ ] 4.4 Commit immutable derivation evidence under the factory identity, add the openxFactory submodule commit-back + aggregation pin bump that persist the merged register, and link the index + evidence from the dated report.

## 5. Tests And Records

- [ ] 5.1 Add tests: a derived entry carries origin/derivation/pending_review + source citations; an unsourced or worker-run-less proposal is rejected; a mis-copied worker precision value voids the affected proposals; accept -> latent retaining origin; reject -> rejected with reason+citation; no edit back to pending_review; a skipped lane leaves deterministic results and prior derived possibles untouched; undisposed derived possibles are excluded from ranked plans and carry a non-`indexed` edge class.
- [ ] 5.2 Keep the openxFactory README "OpenSpec Records" entry current through ratification, realization, and archive.
