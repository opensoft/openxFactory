# Tasks — add-omnigent-semantic-wiring

Realized 2026-07-30. Contracts (1.1–1.2): overlay `worker_class` gains the
closed `semantic_context: {profile_id, package_id}` block (identity only,
authority-free); install manifest gains the closed `semantic_contexts`
section (kernel + ontology_package exact pins, per-worker
`{worker_class, context_id, content_digest, path}` entries). Validation
(2.1–2.3): family suite extended (wired positive examples; three new
`# expect:` negatives — missing profile_id, smuggled `grant`, duplicate
worker_class; 14 negatives total); repo mode
(`validate-omnigent-contracts.py <domain-repo>`) resolves declarations
against the repo's inventoried profiles with worker_scope
archetype-or-class agreement and fails declarations without an ontology
tree; canonical `install_wiring_errors` enforces both-direction
completeness and per-artifact content-digest / kernel-pin / package-pin /
worker-scope agreement, exercised by
`scripts/test-omnigent-semantic-wiring.py` (14 checks over constructed
trees incl. a REAL artifact compiled from a stamped fixture package).
Hardening (3.1–3.2): compile tool verifies kernel + package bytes against
recorded digests before compiling (drift refuses, restamp compiles);
truncation itemizes transitively in the tool AND the ontology validator
fails a truncated context whose itemization stops short
(`truncation-not-transitive` negative; ratchet 49 → 50). First consumer
(4.1): MedxFactory 80a81af — prof-medx-verify (archetype-scoped) +
prof-medx-case-framing (class-scoped) inventoried and restamped,
declarations on `data_reverification_agent` and `case_framing_agent`,
overlay-manifest re-pinned, repo mode + `make validate` green;
codexFactory (no in-repo ontology package) and install repositories
recorded as deferrals through their own governed changes. Battery (4.2):
omnigent suite, wiring suite, ontology self-test 10 positives / 50
negatives + repo scan + determinism, starter/stewardship/semantic suites,
memory gateway, MedxFactory validate, OpenSpec strict — all green.

- [x] 1.1 `omnigent-domain-overlay.schema.yaml`: optional per-worker `semantic_context: {profile_id, package_id}` (closed shape, identity only — no digest, no permission field).
- [x] 1.2 `omnigent-install-manifest.schema.yaml`: optional `semantic_contexts` section — exact kernel + domain package pins and `{worker_class, context_id, content_digest, path}` entries (closed shapes).
- [x] 2.1 `validate-omnigent-contracts.py` semantic checks: install `semantic_contexts` entries unique per worker class; overlay declarations well-formed; wired positive examples + `# expect:`-marked negatives.
- [x] 2.2 Repo mode (`validate-omnigent-contracts.py <domain-repo>`): validate the repo's `omnigent/domain-overlay.yaml` (schema + semantics) and, when `hermes/domain/ontology/` exists, resolve every declared profile — inventoried `xfactory_semantic_context_profile`, matching `package_id`, `worker_scope` archetype-or-class agreement — failing unresolved or mismatched declarations.
- [x] 2.3 Install cross-checks (exercised in `scripts/test-omnigent-semantic-wiring.py` over constructed trees): both-direction completeness against the pinned overlay's declaring workers; per-artifact pin, digest, and worker-scope agreement; overlay-without-section and section-without-overlay failures.
- [x] 3.1 `ontology-compile-context.py` verifies kernel and package bytes against recorded digests before compiling; drift refuses naming the file (F20).
- [x] 3.2 Truncation itemization is transitive in the compile tool, and `validate-domain-ontology.py` fails a truncated context whose itemization omits a transitive closure member; new negative `truncation-not-transitive`; ratchet 49 → 50 (F19).
- [x] 4.1 MedxFactory: two worker-scoped profiles inventoried into the draft ontology package (verify archetype-scoped; `case_framing_agent` class-scoped), `semantic_context` declared on `data_reverification_agent` and `case_framing_agent`, overlay-manifest re-pinned, repo-mode + `make validate` green; codexFactory and install repos recorded as deferrals through their own governed changes.
- [x] 4.2 Battery: omnigent validator (schemas, wired examples, negatives), new wiring test suite, ontology self-test + determinism (50 negatives), compile-tool suites, memory gateway, MedxFactory validate, OpenSpec strict all green.
Release + review (4.3–4.4): contract-v1.23 cut bfa57d1, inventory + tag
3a99bfa, `verify-tag`/`verify-commit` pass against origin; the reviewer
independently recomputed all 179 inventory entries (0 mismatches) and
both refreshed omnigent schema digests. Round-1 verification at 3a99bfa:
areas 1–8 PASS (six overlay attacks incl. class-equality-wins; install
checks both directions; F19 verified on a 4-ring chain both tool- and
validator-side; F20 verified against the real kernel drifted in place;
MedxFactory consumer; disclosed gateway-example repair independently
confirmed) — BLOCKED on **N5**: the artifact `content_digest` was
compared but never recomputed, so a body widened after sealing passed
every gate; plus non-blocking N6 (standalone duplicate collapse) and N7
(pre-existing stale `contracts/manifest.yaml` digest with no checker).
The N5 wave: `install_wiring_errors` AND the canonical ontology
validator recompute the digest from artifact bytes with the compile
tool's own derivation ("a seal, not a label"); the ratified requirement
amended from "declared content_digest" to recomputed, with the
body-widened scenario; every fixture context now carries a REAL seal
(generator derivation shared); new negative `context-body-widened`
(corpus 51, ratchet 51); wiring suite gains the widened-body and
standalone-duplicate probes (16 checks). N6: duplicate `worker_class`
counted before the dict collapses. N7: entry refreshed
(content-manifest.schema.yaml, stale since 403c2b5) and
`scripts/validate-manifest-digests.py` added — recomputes every per-file
sha256 in `contracts/manifest.yaml` (104 verify; it reproduced the 1/104
mismatch before the refresh), closing the class.

- [x] 4.3 Cut contract-v1.23 (omnigent schema bytes changed): manifest digests refreshed, CHANGELOG entry, digest inventory, annotated tag pushed, remote bytes independently verified.
- [ ] 4.4 Reviewer verification against the release candidate; docs (omnigent README, ontology guide seam section, adoption handoff) updated; archive on green evidence with README moved Active → Archived.
