# Drafted DTN Register Seed — DTN-025

Status: record
Kind: register-seed-draft
Drafted by: doc-health neutrality-drift lane (run 1114f93f46d0, 2026-08-05)
Subject: xFactories/codexFactory/hermes/domain/ontology/README.md
Content-SHA256: af23ee7c07a51c3dbd7225b2516c6fbccdfd1e0f8b984c9705cb9b5402754467

Approval: merge the row and section below into
`docs/domain-neutralization-candidate-register.md`. Rejection: record a
disposition in health/dispositions.yaml (family neutrality-drift,
keyed repo + path + content_sha256).

## Register row

| DTN-025 | A starter-scaffolded README explaining the operating rules for the domain-ontolo | `split` | P2 | `seed` | domain-ontology starter-pack template README (contracts/domain-ontology/) |

## Register detail section

### DTN-025: A starter-scaffolded README explaining the operating rules for the domain-ontolo

Machine-drafted seed from the doc-health neutrality-drift lane (2026-08-05, run 1114f93f46d0, prompt contract v1, model claude-sonnet-5; confidence 0.55) — pending human approval; this candidate enters the register lifecycle only when the seed is merged. Stage-1 signals: near_duplicate.

A starter-scaffolded README explaining the operating rules for the domain-ontology package tree (package.yaml/concepts.yaml/sources.yaml immutability, append-only candidate records, governed publication, and the validation command).

Evidence:

- `xFactories/codexFactory/hermes/domain/ontology/README.md` (content sha256 `af23ee7c07a5`)
- Front matter declares it is starter-generated ('starter_source: openxFactory/domain-factory-starter-pack', 'managed_mode: scaffold'), not authored domain content.
- Every operating rule in the body (digest-closed package content, append-only candidate ingestion via 'apply-domain-starter.py --ingest-candidates', governed Domain Hermes release, validation via 'validate-domain-ontology.py') is generic starter-pack mechanics with no engineering-specific vocabulary anywhere in the text.
- The only domain-specific tokens are the 'domain_id: codex' front-matter field and the title string; the remaining four numbered rules would read identically for any other domain's ontology package.

Counter-evidence:

- The file lives under a domain-owned Hermes tree ('hermes/domain/ontology/') where Domain Hermes is declared to own everything.
- The title names the domain ('codex Factory Domain Ontology (DRAFT)').

Domain-local exclusions: The 'domain_id: codex' identity and package_id binding ('xf/codex') stay domain-local.; The document title naming the specific domain factory stays domain-local..
