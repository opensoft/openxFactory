# Ideation Cross-Reference Readiness Index

Status: record
Kind: report
Repository context: openxFactory

**GENERATED FILE — do not edit by hand.** This is a deterministic Markdown projection of the source-of-truth `ideation/cross-reference.yaml`, produced by `scripts/render-ideation-cross-reference.py`. Edit the YAML and re-render; per the `add-ideation-cross-reference-readiness` spec the index is a generated projection over governed documents. See `ideation/README.md` for how this surface relates to the promoted requirements and to `staging/INDEX.md`.

- Source revision: `3e6784f5ae2ac70c3cf151de1ca5ebf958c80e71`
- Generator: `ideation-xref-scorer-0.1.0`
- Topic clusters: 66

## Accessibility

- id: `cl-accessibility`
- topics: accessibility
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); company unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); project unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real))

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/hermes-legal-compliance-model.md` | brainstorm | accessibility |
| `ideation/staging/avatar-pilot-hardening/avatar-pilot-hardening.md` | staged | accessibility |

## Activation Gate

- id: `cl-activation-gate`
- topics: activation-gate
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'domain': rationale is not a non-empty string); company unscored (output rejected: tier 'domain': rationale is not a non-empty string); project unscored (output rejected: tier 'domain': rationale is not a non-empty string)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/nightly-sweep-council-clearance-rule.md` | brainstorm | activation-gate |
| `ideation/staging/qualify-avatar-live-voice/qualify-avatar-live-voice.md` | staged | activation-gate |

## Adoption Profile

- id: `cl-adoption-profile`
- topics: adoption-profile
- tag sources: topics-header
- origin: machine-derived
- extends promoted `memory-gateway` — The cluster's domain-memory-boundaries content is explicitly designed to feed into (not parallel) the already-ratified customer memory gateway's promotion vocabulary and authority_levels (self_reported | observed | source_backed | reviewed | domain_authoritative | below_threshold), and the practice catalog's entries cite already-promoted capabilities (doc-health, credential-contracts) as capability_ref targets rather than proposing new ones from scratch.
- readiness: domain 7; company 5; project 6
- recommendation: not flagged (pending_review) — gate not fired — minimum tier score is 5 (< 8): {'domain': 7, 'company': 5, 'project': 6}

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-memory-and-practices.md` | brainstorm | adoption-profile |
| `ideation/brainstorm/domain-practice-suggestion-generation.md` | brainstorm | adoption-profile |

## Agent Certification

- id: `cl-agent-certification`
- topics: agent-certification
- tag sources: topics-header
- origin: machine-derived
- extends promoted `credential-contracts` — The wallet document explicitly proposes extending the credential-contracts capability with a new credential type â€” an agent-certification verifiable credential (issuer = certification gate, subject = agent DID, claims = qualification level, certified config hash, battery scores, expiry) â€” alongside the existing patient/practitioner licensure credentials, and the persona document extends the same idea to persona-as-quantified-identity via its behavioral battery.
- readiness: domain unscored (No owning DomainxFactory resolves for this cluster); company 6; project 4
- recommendation: not flagged (pending_review) — gate not fired — tier(s) not scored: ['domain']

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/agent-certification-wallets.md` | brainstorm | agent-certification |
| `ideation/brainstorm/hermes-persona-character-model.md` | brainstorm | agent-certification |

## Agent Mixes

- id: `cl-agent-mixes`
- topics: agent-mixes, escalation-rules, review-councils
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'domain': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); company unscored (output rejected: tier 'domain': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); project unscored (output rejected: tier 'domain': grounding passage is not found verbatim in any cluster member document (a cited passage must be real))

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-deliberation.md` | brainstorm | agent-mixes, escalation-rules, review-councils |
| `ideation/staging/codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md` | staged | agent-mixes, escalation-rules, review-councils |

## Authority Personas

- id: `cl-authority-personas`
- topics: authority-personas
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'company': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); company unscored (output rejected: tier 'company': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); project unscored (output rejected: tier 'company': grounding passage is not found verbatim in any cluster member document (a cited passage must be real))

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-roster-draft.md` | brainstorm | authority-personas |
| `ideation/brainstorm/codexfactory-domain-hermes-content.md` | brainstorm | authority-personas |
| `ideation/brainstorm/codexfactory-domain-roster-draft.md` | brainstorm | authority-personas |
| `ideation/brainstorm/hermes-persona-character-model.md` | brainstorm | authority-personas |

## Auto Clear Envelope

- id: `cl-auto-clear-envelope`
- topics: auto-clear-envelope
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); company unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); project unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real))

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-content-draft.md` | brainstorm | auto-clear-envelope |
| `ideation/brainstorm/client-policy-wizard.md` | brainstorm | auto-clear-envelope |
| `ideation/brainstorm/nightly-sweep-council-clearance-rule.md` | brainstorm | auto-clear-envelope |
| `ideation/brainstorm/practice-clearance-and-project-realization.md` | brainstorm | auto-clear-envelope |
| `ideation/staging/client-layer-tuning/client-layer-tuning.md` | staged | auto-clear-envelope |

## Avatar Client

- id: `cl-avatar-client`
- topics: avatar-client
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); company unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); project unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real))

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/staging/avatar-pilot-hardening/avatar-pilot-hardening.md` | staged | avatar-client |
| `ideation/staging/qualify-avatar-live-voice/qualify-avatar-live-voice.md` | staged | avatar-client |

## Break Glass

- id: `cl-break-glass`
- topics: break-glass
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'company': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); company unscored (output rejected: tier 'company': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); project unscored (output rejected: tier 'company': grounding passage is not found verbatim in any cluster member document (a cited passage must be real))

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/subject-recall-and-consent-path.md` | brainstorm | break-glass |
| `ideation/staging/client-credential-escrow-registry/client-credential-escrow-registry.md` | staged | break-glass |

## Cerebras

- id: `cl-cerebras`
- topics: cerebras, evidence-rows
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); company unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); project unscored (output rejected: tier 'project': grounding passage is not found verbatim in any cluster member document (a cited passage must be real))

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-ingestion-adapter-contract.md` | brainstorm | cerebras, evidence-rows |
| `ideation/brainstorm/hermes-knowledge-base-architecture.md` | brainstorm | cerebras, evidence-rows |

## Character Model

- id: `cl-character-model`
- topics: character-model, trait-framework
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'domain': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); company unscored (output rejected: tier 'domain': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); project unscored (output rejected: tier 'domain': grounding passage is not found verbatim in any cluster member document (a cited passage must be real))

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-roster-draft.md` | brainstorm | character-model, trait-framework |
| `ideation/brainstorm/hermes-persona-character-model.md` | brainstorm | character-model, trait-framework |

## Client Hermes

- id: `cl-client-hermes`
- topics: client-hermes
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (output rejected: tier 'company': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); company unscored (output rejected: tier 'company': grounding passage is not found verbatim in any cluster member document (a cited passage must be real)); project unscored (output rejected: tier 'company': grounding passage is not found verbatim in any cluster member document (a cited passage must be real))

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-ingestion-adapter-contract.md` | brainstorm | client-hermes |
| `ideation/brainstorm/client-layer-content-draft.md` | brainstorm | client-hermes |
| `ideation/brainstorm/client-layer-roster-draft.md` | brainstorm | client-hermes |
| `ideation/brainstorm/client-layer-scaffold.md` | brainstorm | client-hermes |
| `ideation/brainstorm/client-policy-wizard.md` | brainstorm | client-hermes |
| `ideation/brainstorm/client-risk-and-assurance-model.md` | brainstorm | client-hermes |
| `ideation/brainstorm/cost-accountability-and-efficiency-model.md` | brainstorm | client-hermes |
| `ideation/brainstorm/hermes-knowledge-base-architecture.md` | brainstorm | client-hermes |
| `ideation/brainstorm/hermes-layer-content-seeding.md` | brainstorm | client-hermes |
| `ideation/brainstorm/hermes-legal-compliance-model.md` | brainstorm | client-hermes |
| `ideation/brainstorm/workflow-visualization-tooling.md` | staged | client-hermes |
| `ideation/staging/client-credential-escrow-registry/client-credential-escrow-registry.md` | staged | client-hermes |
| `ideation/staging/client-layer-tuning/client-layer-tuning.md` | staged | client-hermes |

## Client Layer

- id: `cl-client-layer`
- topics: client-layer
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-client-layer); company unscored (worker failed: no remote result collected for cl-client-layer); project unscored (worker failed: no remote result collected for cl-client-layer)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-content-draft.md` | brainstorm | client-layer |
| `ideation/brainstorm/client-layer-scaffold.md` | brainstorm | client-layer |
| `ideation/brainstorm/client-policy-wizard.md` | brainstorm | client-layer |

## Codexfactory

- id: `cl-codexfactory`
- topics: codexfactory
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-codexfactory); company unscored (worker failed: no remote result collected for cl-codexfactory); project unscored (worker failed: no remote result collected for cl-codexfactory)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-deliberation.md` | brainstorm | codexfactory |
| `ideation/brainstorm/codexfactory-domain-hermes-content.md` | brainstorm | codexfactory |
| `ideation/brainstorm/codexfactory-domain-memory-and-practices.md` | brainstorm | codexfactory |
| `ideation/brainstorm/codexfactory-domain-policy-model.md` | brainstorm | codexfactory |
| `ideation/brainstorm/codexfactory-domain-roster-draft.md` | brainstorm | codexfactory |
| `ideation/brainstorm/nightly-sweep-council-clearance-rule.md` | brainstorm | codexfactory |
| `ideation/staging/codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md` | staged | codexfactory |

## Company Policy

- id: `cl-company-policy`
- topics: company-policy
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-company-policy); company unscored (worker failed: no remote result collected for cl-company-policy); project unscored (worker failed: no remote result collected for cl-company-policy)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-content-draft.md` | brainstorm | company-policy |
| `ideation/brainstorm/client-layer-roster-draft.md` | brainstorm | company-policy |
| `ideation/brainstorm/client-layer-scaffold.md` | brainstorm | company-policy |
| `ideation/staging/client-layer-tuning/client-layer-tuning.md` | staged | company-policy |

## Consent

- id: `cl-consent`
- topics: consent
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-consent); company unscored (worker failed: no remote result collected for cl-consent); project unscored (worker failed: no remote result collected for cl-consent)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-ingestion-adapter-contract.md` | brainstorm | consent |
| `ideation/brainstorm/hermes-knowledge-base-architecture.md` | brainstorm | consent |
| `ideation/brainstorm/hermes-retrieval-primitives-contract.md` | brainstorm | consent |
| `ideation/brainstorm/project-layer-scaffold.md` | brainstorm | consent |
| `ideation/brainstorm/subject-recall-and-consent-path.md` | brainstorm | consent |

## Cost Accountability

- id: `cl-cost-accountability`
- topics: cost-accountability
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-cost-accountability); company unscored (worker failed: no remote result collected for cl-cost-accountability); project unscored (worker failed: no remote result collected for cl-cost-accountability)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/cost-accountability-and-efficiency-model.md` | brainstorm | cost-accountability |
| `ideation/brainstorm/nightly-sweep-council-clearance-rule.md` | brainstorm | cost-accountability |

## Credential Contracts

- id: `cl-credential-contracts`
- topics: credential-contracts
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-credential-contracts); company unscored (worker failed: no remote result collected for cl-credential-contracts); project unscored (worker failed: no remote result collected for cl-credential-contracts)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/contract-release-and-stack-surface.md` | brainstorm | credential-contracts |
| `ideation/brainstorm/keycloak-identity-brokering.md` | brainstorm | credential-contracts |

## Credentials

- id: `cl-credentials`
- topics: credentials
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-credentials); company unscored (worker failed: no remote result collected for cl-credentials); project unscored (worker failed: no remote result collected for cl-credentials)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/omnigent-lane-activation-path.md` | brainstorm | credentials |
| `ideation/staging/client-credential-escrow-registry/client-credential-escrow-registry.md` | staged | credentials |

## Determinism

- id: `cl-determinism`
- topics: determinism
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-determinism); company unscored (worker failed: no remote result collected for cl-determinism); project unscored (worker failed: no remote result collected for cl-determinism)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-policy-model.md` | brainstorm | determinism |
| `ideation/brainstorm/hermes-layer-seeding-mechanism.md` | brainstorm | determinism |

## Doc Health

- id: `cl-doc-health`
- topics: doc-health
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-doc-health); company unscored (worker failed: no remote result collected for cl-doc-health); project unscored (worker failed: no remote result collected for cl-doc-health)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/doc-health-pipeline.md` | staged | doc-health |
| `ideation/brainstorm/hermes-governed-nightly-sweep.md` | brainstorm | doc-health |
| `ideation/brainstorm/ideation-dashboard.md` | staged | doc-health |

## Doc Management

- id: `cl-doc-management`
- topics: doc-management, doc-workflow
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-doc-management); company unscored (worker failed: no remote result collected for cl-doc-management); project unscored (worker failed: no remote result collected for cl-doc-management)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/cluster-combining-gui.md` | staged | doc-management, doc-workflow |
| `ideation/brainstorm/doc-health-pipeline.md` | staged | doc-management, doc-workflow |
| `ideation/brainstorm/domain-to-neutral-promotion.md` | staged | doc-management, doc-workflow |
| `ideation/brainstorm/ideation-cross-reference-readiness.md` | staged | doc-management, doc-workflow |
| `ideation/brainstorm/ideation-dashboard.md` | staged | doc-management, doc-workflow |
| `ideation/brainstorm/lens-brainstorm-session-launch.md` | brainstorm | doc-management, doc-workflow |
| `ideation/brainstorm/lens-keyword-search-and-adhoc.md` | brainstorm | doc-management, doc-workflow |
| `ideation/brainstorm/lens-ring-combination-explorer.md` | brainstorm | doc-management, doc-workflow |
| `ideation/brainstorm/openspec-speckit-release-flow.md` | staged | doc-management, doc-workflow |
| `ideation/brainstorm/topic-compilation-tree.md` | brainstorm | doc-management, doc-workflow |

## Domain Hermes

- id: `cl-domain-hermes`
- topics: domain-hermes
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-domain-hermes); company unscored (worker failed: no remote result collected for cl-domain-hermes); project unscored (worker failed: no remote result collected for cl-domain-hermes)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-deliberation.md` | brainstorm | domain-hermes |
| `ideation/brainstorm/codexfactory-domain-hermes-content.md` | brainstorm | domain-hermes |
| `ideation/brainstorm/codexfactory-domain-memory-and-practices.md` | brainstorm | domain-hermes |
| `ideation/brainstorm/codexfactory-domain-policy-model.md` | brainstorm | domain-hermes |
| `ideation/brainstorm/codexfactory-domain-roster-draft.md` | brainstorm | domain-hermes |
| `ideation/brainstorm/cost-accountability-and-efficiency-model.md` | brainstorm | domain-hermes |
| `ideation/brainstorm/domain-practice-suggestion-generation.md` | brainstorm | domain-hermes |
| `ideation/brainstorm/hermes-layer-content-seeding.md` | brainstorm | domain-hermes |
| `ideation/brainstorm/hermes-persona-character-model.md` | brainstorm | domain-hermes |
| `ideation/staging/codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md` | staged | domain-hermes |

## Domain Memory

- id: `cl-domain-memory`
- topics: domain-memory
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-domain-memory); company unscored (worker failed: no remote result collected for cl-domain-memory); project unscored (worker failed: no remote result collected for cl-domain-memory)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-memory-and-practices.md` | brainstorm | domain-memory |
| `ideation/brainstorm/codexfactory-domain-policy-model.md` | brainstorm | domain-memory |

## Execution Lane

- id: `cl-execution-lane`
- topics: execution-lane
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-execution-lane); company unscored (worker failed: no remote result collected for cl-execution-lane); project unscored (worker failed: no remote result collected for cl-execution-lane)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/omnigent-lane-activation-path.md` | brainstorm | execution-lane |
| `ideation/brainstorm/tech-stack-benches.md` | brainstorm | execution-lane |

## Fail Closed

- id: `cl-fail-closed`
- topics: fail-closed
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-fail-closed); company unscored (worker failed: no remote result collected for cl-fail-closed); project unscored (worker failed: no remote result collected for cl-fail-closed)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-risk-and-assurance-model.md` | brainstorm | fail-closed |
| `ideation/brainstorm/hermes-layer-seeding-mechanism.md` | brainstorm | fail-closed |
| `ideation/brainstorm/hermes-legal-compliance-model.md` | brainstorm | fail-closed |

## Feat Request

- id: `cl-feat-request`
- topics: feat-request, keyword-lens
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-feat-request); company unscored (worker failed: no remote result collected for cl-feat-request); project unscored (worker failed: no remote result collected for cl-feat-request)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/lens-brainstorm-session-launch.md` | brainstorm | feat-request, keyword-lens |
| `ideation/brainstorm/lens-keyword-search-and-adhoc.md` | brainstorm | feat-request, keyword-lens |
| `ideation/brainstorm/lens-ring-combination-explorer.md` | brainstorm | feat-request, keyword-lens |

## Gate Rules Council

- id: `cl-gate-rules-council`
- topics: gate-rules-council
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-gate-rules-council); company unscored (worker failed: no remote result collected for cl-gate-rules-council); project unscored (worker failed: no remote result collected for cl-gate-rules-council)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-deliberation.md` | brainstorm | gate-rules-council |
| `ideation/brainstorm/codexfactory-domain-hermes-content.md` | brainstorm | gate-rules-council |
| `ideation/brainstorm/nightly-sweep-council-clearance-rule.md` | brainstorm | gate-rules-council |

## Hermes Install

- id: `cl-hermes-install`
- topics: hermes-install
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-hermes-install); company unscored (worker failed: no remote result collected for cl-hermes-install); project unscored (worker failed: no remote result collected for cl-hermes-install)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/hermes-layer-seeding-mechanism.md` | brainstorm | hermes-install |
| `ideation/staging/layer-content-materialization/layer-content-materialization.md` | staged | hermes-install |
| `ideation/staging/omnigent-core-domain-split/omnigent-core-domain-split.md` | staged | hermes-install |

## House Style

- id: `cl-house-style`
- topics: house-style
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-house-style); company unscored (worker failed: no remote result collected for cl-house-style); project unscored (worker failed: no remote result collected for cl-house-style)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-roster-draft.md` | brainstorm | house-style |
| `ideation/brainstorm/client-policy-wizard.md` | brainstorm | house-style |

## House Team

- id: `cl-house-team`
- topics: house-team
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-house-team); company unscored (worker failed: no remote result collected for cl-house-team); project unscored (worker failed: no remote result collected for cl-house-team)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-roster-draft.md` | brainstorm | house-team |
| `ideation/brainstorm/client-layer-scaffold.md` | brainstorm | house-team |
| `ideation/staging/client-layer-tuning/client-layer-tuning.md` | staged | house-team |

## Human Escalation

- id: `cl-human-escalation`
- topics: human-escalation, legal-compliance
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-human-escalation); company unscored (worker failed: no remote result collected for cl-human-escalation); project unscored (worker failed: no remote result collected for cl-human-escalation)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-risk-and-assurance-model.md` | brainstorm | human-escalation, legal-compliance |
| `ideation/brainstorm/hermes-legal-compliance-model.md` | brainstorm | human-escalation, legal-compliance |

## Hybrid Seam

- id: `cl-hybrid-seam`
- topics: hybrid-seam, materialization, seed-layer-content
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-hybrid-seam); company unscored (worker failed: no remote result collected for cl-hybrid-seam); project unscored (worker failed: no remote result collected for cl-hybrid-seam)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/hermes-layer-seeding-mechanism.md` | brainstorm | hybrid-seam, materialization, seed-layer-content |
| `ideation/staging/layer-content-materialization/layer-content-materialization.md` | staged | hybrid-seam, materialization, seed-layer-content |

## Hybrid Search

- id: `cl-hybrid-search`
- topics: hybrid-search, planner-executor-synthesizer, retrieval
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-hybrid-search); company unscored (worker failed: no remote result collected for cl-hybrid-search); project unscored (worker failed: no remote result collected for cl-hybrid-search)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/hermes-knowledge-base-architecture.md` | brainstorm | hybrid-search, planner-executor-synthesizer, retrieval |
| `ideation/brainstorm/hermes-retrieval-primitives-contract.md` | brainstorm | hybrid-search, planner-executor-synthesizer, retrieval |

## Ideation Cross Reference

- id: `cl-ideation-cross-reference`
- topics: ideation-cross-reference
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-ideation-cross-reference); company unscored (worker failed: no remote result collected for cl-ideation-cross-reference); project unscored (worker failed: no remote result collected for cl-ideation-cross-reference)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/ideation-cross-reference-readiness.md` | staged | ideation-cross-reference |
| `ideation/brainstorm/ideation-dashboard.md` | staged | ideation-cross-reference |

## Ideation Dashboard

- id: `cl-ideation-dashboard`
- topics: ideation-dashboard
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-ideation-dashboard); company unscored (worker failed: no remote result collected for cl-ideation-dashboard); project unscored (worker failed: no remote result collected for cl-ideation-dashboard)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/cluster-combining-gui.md` | staged | ideation-dashboard |
| `ideation/brainstorm/ideation-dashboard.md` | staged | ideation-dashboard |
| `ideation/brainstorm/keycloak-identity-brokering.md` | brainstorm | ideation-dashboard |
| `ideation/brainstorm/lens-brainstorm-session-launch.md` | brainstorm | ideation-dashboard |
| `ideation/brainstorm/lens-keyword-search-and-adhoc.md` | brainstorm | ideation-dashboard |
| `ideation/brainstorm/lens-ring-combination-explorer.md` | brainstorm | ideation-dashboard |
| `ideation/brainstorm/topic-compilation-tree.md` | brainstorm | ideation-dashboard |

## Ideation Lifecycle

- id: `cl-ideation-lifecycle`
- topics: ideation-lifecycle
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-ideation-lifecycle); company unscored (worker failed: no remote result collected for cl-ideation-lifecycle); project unscored (worker failed: no remote result collected for cl-ideation-lifecycle)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/doc-health-pipeline.md` | staged | ideation-lifecycle |
| `ideation/brainstorm/immovable-leaf-ideation-lifecycle.md` | brainstorm | ideation-lifecycle |

## Ideation Tooling

- id: `cl-ideation-tooling`
- topics: ideation-tooling, possibles-register
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-ideation-tooling); company unscored (worker failed: no remote result collected for cl-ideation-tooling); project unscored (worker failed: no remote result collected for cl-ideation-tooling)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/cluster-combining-gui.md` | staged | ideation-tooling, possibles-register |
| `ideation/brainstorm/topic-compilation-tree.md` | brainstorm | ideation-tooling, possibles-register |

## Layer Content Seeding

- id: `cl-layer-content-seeding`
- topics: layer-content-seeding
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-layer-content-seeding); company unscored (worker failed: no remote result collected for cl-layer-content-seeding); project unscored (worker failed: no remote result collected for cl-layer-content-seeding)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-scaffold.md` | brainstorm | layer-content-seeding |
| `ideation/brainstorm/client-policy-wizard.md` | brainstorm | layer-content-seeding |
| `ideation/brainstorm/codexfactory-domain-hermes-content.md` | brainstorm | layer-content-seeding |
| `ideation/brainstorm/codexfactory-domain-memory-and-practices.md` | brainstorm | layer-content-seeding |
| `ideation/brainstorm/codexfactory-domain-policy-model.md` | brainstorm | layer-content-seeding |
| `ideation/brainstorm/cost-accountability-and-efficiency-model.md` | brainstorm | layer-content-seeding |
| `ideation/brainstorm/hermes-layer-content-seeding.md` | brainstorm | layer-content-seeding |
| `ideation/staging/client-layer-tuning/client-layer-tuning.md` | staged | layer-content-seeding |
| `ideation/staging/codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md` | staged | layer-content-seeding |
| `ideation/staging/layer-content-materialization/layer-content-materialization.md` | staged | layer-content-seeding |

## Manual Writer

- id: `cl-manual-writer`
- topics: manual-writer, project-type-template, provisioning, subject
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-manual-writer); company unscored (worker failed: no remote result collected for cl-manual-writer); project unscored (worker failed: no remote result collected for cl-manual-writer)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/project-layer-scaffold.md` | brainstorm | manual-writer, project-type-template, provisioning, subject |
| `ideation/brainstorm/project-type-template-library-draft.md` | brainstorm | manual-writer, project-type-template, provisioning, subject |

## Medxfactory

- id: `cl-medxfactory`
- topics: medxfactory
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-medxfactory); company unscored (worker failed: no remote result collected for cl-medxfactory); project unscored (worker failed: no remote result collected for cl-medxfactory)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/medical-omnigent-harness-adaptation.md` | brainstorm | medxfactory |
| `ideation/staging/proposal-origin-contract/fda-samd-traceability-rationale.md` | staged | medxfactory |

## Memory Boundaries

- id: `cl-memory-boundaries`
- topics: memory-boundaries
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-memory-boundaries); company unscored (worker failed: no remote result collected for cl-memory-boundaries); project unscored (worker failed: no remote result collected for cl-memory-boundaries)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-content-draft.md` | brainstorm | memory-boundaries |
| `ideation/brainstorm/codexfactory-domain-memory-and-practices.md` | brainstorm | memory-boundaries |
| `ideation/staging/codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md` | staged | memory-boundaries |

## Memory Gateway

- id: `cl-memory-gateway`
- topics: memory-gateway
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-memory-gateway); company unscored (worker failed: no remote result collected for cl-memory-gateway); project unscored (worker failed: no remote result collected for cl-memory-gateway)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-ingestion-adapter-contract.md` | brainstorm | memory-gateway |
| `ideation/brainstorm/codexfactory-domain-memory-and-practices.md` | brainstorm | memory-gateway |
| `ideation/brainstorm/hermes-knowledge-base-architecture.md` | brainstorm | memory-gateway |
| `ideation/brainstorm/hermes-layer-content-seeding.md` | brainstorm | memory-gateway |
| `ideation/brainstorm/hermes-layer-seeding-mechanism.md` | brainstorm | memory-gateway |
| `ideation/brainstorm/hermes-persona-character-model.md` | brainstorm | memory-gateway |
| `ideation/brainstorm/hermes-retrieval-primitives-contract.md` | brainstorm | memory-gateway |
| `ideation/brainstorm/subject-recall-and-consent-path.md` | brainstorm | memory-gateway |

## Merge Master

- id: `cl-merge-master`
- topics: merge-master
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-merge-master); company unscored (worker failed: no remote result collected for cl-merge-master); project unscored (worker failed: no remote result collected for cl-merge-master)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-hermes-content.md` | brainstorm | merge-master |
| `ideation/brainstorm/nightly-sweep-council-clearance-rule.md` | brainstorm | merge-master |
| `ideation/brainstorm/omnigent-lane-activation-path.md` | brainstorm | merge-master |

## Merge Readiness Council

- id: `cl-merge-readiness-council`
- topics: merge-readiness-council
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-merge-readiness-council); company unscored (worker failed: no remote result collected for cl-merge-readiness-council); project unscored (worker failed: no remote result collected for cl-merge-readiness-council)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-deliberation.md` | brainstorm | merge-readiness-council |
| `ideation/brainstorm/nightly-sweep-council-clearance-rule.md` | brainstorm | merge-readiness-council |

## Nightly Sweep

- id: `cl-nightly-sweep`
- topics: nightly-sweep
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-nightly-sweep); company unscored (worker failed: no remote result collected for cl-nightly-sweep); project unscored (worker failed: no remote result collected for cl-nightly-sweep)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/hermes-governed-nightly-sweep.md` | brainstorm | nightly-sweep |
| `ideation/brainstorm/nightly-sweep-council-clearance-rule.md` | brainstorm | nightly-sweep |

## Omnigent Lane

- id: `cl-omnigent-lane`
- topics: omnigent-lane
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-omnigent-lane); company unscored (worker failed: no remote result collected for cl-omnigent-lane); project unscored (worker failed: no remote result collected for cl-omnigent-lane)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/nightly-sweep-council-clearance-rule.md` | brainstorm | omnigent-lane |
| `ideation/brainstorm/omnigent-lane-activation-path.md` | brainstorm | omnigent-lane |

## Overlay Ref

- id: `cl-overlay-ref`
- topics: overlay-ref
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-overlay-ref); company unscored (worker failed: no remote result collected for cl-overlay-ref); project unscored (worker failed: no remote result collected for cl-overlay-ref)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/hermes-layer-content-seeding.md` | brainstorm | overlay-ref |
| `ideation/brainstorm/hermes-layer-seeding-mechanism.md` | brainstorm | overlay-ref |

## Personality

- id: `cl-personality`
- topics: personality
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-personality); company unscored (worker failed: no remote result collected for cl-personality); project unscored (worker failed: no remote result collected for cl-personality)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/hermes-layer-content-seeding.md` | brainstorm | personality |
| `ideation/brainstorm/hermes-persona-character-model.md` | brainstorm | personality |

## Plane 1

- id: `cl-plane-1`
- topics: plane-1
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-plane-1); company unscored (worker failed: no remote result collected for cl-plane-1); project unscored (worker failed: no remote result collected for cl-plane-1)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-roster-draft.md` | brainstorm | plane-1 |
| `ideation/brainstorm/client-layer-scaffold.md` | brainstorm | plane-1 |
| `ideation/brainstorm/codexfactory-domain-roster-draft.md` | brainstorm | plane-1 |
| `ideation/brainstorm/project-layer-scaffold.md` | brainstorm | plane-1 |
| `ideation/staging/codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md` | staged | plane-1 |

## Plane 2

- id: `cl-plane-2`
- topics: plane-2
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-plane-2); company unscored (worker failed: no remote result collected for cl-plane-2); project unscored (worker failed: no remote result collected for cl-plane-2)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-ingestion-adapter-contract.md` | brainstorm | plane-2 |
| `ideation/brainstorm/client-layer-scaffold.md` | brainstorm | plane-2 |

## Plane 3

- id: `cl-plane-3`
- topics: plane-3
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-plane-3); company unscored (worker failed: no remote result collected for cl-plane-3); project unscored (worker failed: no remote result collected for cl-plane-3)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-deliberation.md` | brainstorm | plane-3 |
| `ideation/brainstorm/hermes-legal-compliance-model.md` | brainstorm | plane-3 |

## Policy Wizard

- id: `cl-policy-wizard`
- topics: policy-wizard
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-policy-wizard); company unscored (worker failed: no remote result collected for cl-policy-wizard); project unscored (worker failed: no remote result collected for cl-policy-wizard)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-scaffold.md` | brainstorm | policy-wizard |
| `ideation/brainstorm/client-policy-wizard.md` | brainstorm | policy-wizard |
| `ideation/staging/client-layer-tuning/client-layer-tuning.md` | staged | policy-wizard |

## Practice Adoption

- id: `cl-practice-adoption`
- topics: practice-adoption
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-practice-adoption); company unscored (worker failed: no remote result collected for cl-practice-adoption); project unscored (worker failed: no remote result collected for cl-practice-adoption)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/domain-practice-suggestion-generation.md` | brainstorm | practice-adoption |
| `ideation/brainstorm/hermes-governed-nightly-sweep.md` | brainstorm | practice-adoption |
| `ideation/brainstorm/practice-clearance-and-project-realization.md` | brainstorm | practice-adoption |

## Practice Catalog

- id: `cl-practice-catalog`
- topics: practice-catalog
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-practice-catalog); company unscored (worker failed: no remote result collected for cl-practice-catalog); project unscored (worker failed: no remote result collected for cl-practice-catalog)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-hermes-content.md` | brainstorm | practice-catalog |
| `ideation/brainstorm/codexfactory-domain-memory-and-practices.md` | brainstorm | practice-catalog |
| `ideation/brainstorm/cost-accountability-and-efficiency-model.md` | brainstorm | practice-catalog |
| `ideation/brainstorm/domain-practice-suggestion-generation.md` | brainstorm | practice-catalog |
| `ideation/brainstorm/hermes-layer-content-seeding.md` | brainstorm | practice-catalog |
| `ideation/staging/codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md` | staged | practice-catalog |

## Project Hermes

- id: `cl-project-hermes`
- topics: project-hermes
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-project-hermes); company unscored (worker failed: no remote result collected for cl-project-hermes); project unscored (worker failed: no remote result collected for cl-project-hermes)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/cost-accountability-and-efficiency-model.md` | brainstorm | project-hermes |
| `ideation/brainstorm/hermes-layer-content-seeding.md` | brainstorm | project-hermes |
| `ideation/brainstorm/project-layer-scaffold.md` | brainstorm | project-hermes |
| `ideation/brainstorm/project-type-template-library-draft.md` | brainstorm | project-hermes |

## Roles Authority Model

- id: `cl-roles-authority-model`
- topics: roles-authority-model
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-roles-authority-model); company unscored (worker failed: no remote result collected for cl-roles-authority-model); project unscored (worker failed: no remote result collected for cl-roles-authority-model)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/domain-to-neutral-promotion.md` | staged | roles-authority-model |
| `ideation/brainstorm/keycloak-identity-brokering.md` | brainstorm | roles-authority-model |
| `ideation/staging/github-administration-plane/multi-app-identity-and-github-administration.md` | superseded | roles-authority-model |

## Roster

- id: `cl-roster`
- topics: roster
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-roster); company unscored (worker failed: no remote result collected for cl-roster); project unscored (worker failed: no remote result collected for cl-roster)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-layer-roster-draft.md` | brainstorm | roster |
| `ideation/brainstorm/codexfactory-domain-roster-draft.md` | brainstorm | roster |
| `ideation/staging/codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md` | staged | roster |

## Scrum Coordinator

- id: `cl-scrum-coordinator`
- topics: scrum-coordinator
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-scrum-coordinator); company unscored (worker failed: no remote result collected for cl-scrum-coordinator); project unscored (worker failed: no remote result collected for cl-scrum-coordinator)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-hermes-content.md` | brainstorm | scrum-coordinator |
| `ideation/brainstorm/codexfactory-domain-roster-draft.md` | brainstorm | scrum-coordinator |

## Self Hosting

- id: `cl-self-hosting`
- topics: self-hosting
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-self-hosting); company unscored (worker failed: no remote result collected for cl-self-hosting); project unscored (worker failed: no remote result collected for cl-self-hosting)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/hermes-governed-nightly-sweep.md` | brainstorm | self-hosting |
| `ideation/brainstorm/omnigent-lane-activation-path.md` | brainstorm | self-hosting |

## Sops

- id: `cl-sops`
- topics: sops
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-sops); company unscored (worker failed: no remote result collected for cl-sops); project unscored (worker failed: no remote result collected for cl-sops)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/git-native-record-vault.md` | brainstorm | sops |
| `ideation/staging/client-credential-escrow-registry/client-credential-escrow-registry.md` | staged | sops |

## Source Authority

- id: `cl-source-authority`
- topics: source-authority, tenant-isolation
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-source-authority); company unscored (worker failed: no remote result collected for cl-source-authority); project unscored (worker failed: no remote result collected for cl-source-authority)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/client-ingestion-adapter-contract.md` | brainstorm | source-authority, tenant-isolation |
| `ideation/brainstorm/hermes-knowledge-base-architecture.md` | brainstorm | source-authority, tenant-isolation |
| `ideation/brainstorm/hermes-retrieval-primitives-contract.md` | brainstorm | source-authority, tenant-isolation |

## Three Layer Hermes Runtime

- id: `cl-three-layer-hermes-runtime`
- topics: three-layer-hermes-runtime
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-three-layer-hermes-runtime); company unscored (worker failed: no remote result collected for cl-three-layer-hermes-runtime); project unscored (worker failed: no remote result collected for cl-three-layer-hermes-runtime)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/codexfactory-domain-hermes-content.md` | brainstorm | three-layer-hermes-runtime |
| `ideation/brainstorm/hermes-layer-content-seeding.md` | brainstorm | three-layer-hermes-runtime |

## User Management

- id: `cl-user-management`
- topics: user-management
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-user-management); company unscored (worker failed: no remote result collected for cl-user-management); project unscored (worker failed: no remote result collected for cl-user-management)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/keycloak-identity-brokering.md` | brainstorm | user-management |
| `ideation/brainstorm/lens-keyword-search-and-adhoc.md` | brainstorm | user-management |

## Workbench

- id: `cl-workbench`
- topics: workbench
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-workbench); company unscored (worker failed: no remote result collected for cl-workbench); project unscored (worker failed: no remote result collected for cl-workbench)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/cluster-combining-gui.md` | staged | workbench |
| `ideation/brainstorm/lens-brainstorm-session-launch.md` | brainstorm | workbench |

## Workflow Visualization

- id: `cl-workflow-visualization`
- topics: workflow-visualization
- tag sources: topics-header
- origin: machine-derived
- no promoted fit — Readiness worker did not evaluate extension fit for this cluster (scoring skipped or the worker proposed none); recorded as no-promoted-fit-claim, not an asserted 'no fit exists' finding.
- readiness: domain unscored (worker failed: no remote result collected for cl-workflow-visualization); company unscored (worker failed: no remote result collected for cl-workflow-visualization); project unscored (worker failed: no remote result collected for cl-workflow-visualization)

| Member | Stage | Matched tags |
| --- | --- | --- |
| `ideation/brainstorm/ideation-dashboard.md` | staged | workflow-visualization |
| `ideation/brainstorm/workflow-visualization-tooling.md` | staged | workflow-visualization |
