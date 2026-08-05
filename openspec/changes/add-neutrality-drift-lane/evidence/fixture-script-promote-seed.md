# Drafted DTN Register Seed — DTN-026

Status: record
Kind: register-seed-draft
Drafted by: doc-health neutrality-drift lane (run 4e7b81a490ba, 2026-08-05)
Subject: xFactories/zephyrFactory/scripts/validate-envelopes.py
Content-SHA256: 8b8c0a64710c4ae6e9b23fb30fddaf0e4ac032d137db5c14a27218e5fdf8d3c3

Approval: merge the row and section below into
`docs/domain-neutralization-candidate-register.md`. Rejection: record a
disposition in health/dispositions.yaml (family neutrality-drift,
keyed repo + path + content_sha256).

## Register row

| DTN-026 | A Python validator for the three-kind consent-instrument contract family (xfacto | `promote` | P2 | `seed` | scripts/validate-consent-instruments.py |

## Register detail section

### DTN-026: A Python validator for the three-kind consent-instrument contract family (xfacto

Machine-drafted seed from the doc-health neutrality-drift lane (2026-08-05, run 4e7b81a490ba, prompt contract v1, model claude-sonnet-5; confidence 0.90) — pending human approval; this candidate enters the register lifecycle only when the seed is merged. Stage-1 signals: lexicon_absence, near_duplicate, uninventoried_tooling.

A Python validator for the three-kind consent-instrument contract family (xfactory_consent_instrument, its class registry, and its purpose model), enforcing cross-shape rules like class membership, custody-as-pointer, purpose resolution, and termination cascade evidence.

Evidence:

- `xFactories/zephyrFactory/scripts/validate-envelopes.py` (content sha256 `8b8c0a64710c`)
- The module docstring self-identifies as 'The openxFactory-owned canonical validator for the three kinds ... STANDALONE by ruling D8' and instructs operators to 'Run from the pinned openxFactory checkout, never copied into a domain repo' — the content itself asserts it is shared, cross-domain tooling, not that its path merely resembles one.
- SCHEMA_DIR/EXAMPLES_DIR are computed relative to the script's own file location (ROOT = parents[1]) and point at 'contracts/schemas' and 'examples/consent-instrument', the openxFactory layout, not anything zephyr-specific.
- Every check (check_class, check_custody, check_purposes, check_termination_cascade, check_data_consent) explicitly treats the class registry and purpose model as domain-owned documents to be located 'in the domain repo' and matched by a generic `domain` key — the validator's own logic separates generic shape from domain content.
- Token-set similarity of 1.00 against openxFactory/scripts/validate-consent-instruments.py, combined with the script naming that exact file as its own canonical counterpart, shows this is a duplicate of tooling the content itself says should not be copied into a domain repo.

Counter-evidence:

- The docstring's illustrative examples name other domains ('the Medx constraint', 'the Ledgerx tenant tree', 'Ledgerx `active` -> `executed`' alias) as usage scenarios, which could be read as domain-flavored commentary embedded in the tooling.

Domain-local exclusions: The instrument_class registry and purpose model documents the validator adjudicates against are explicitly domain-owned per the script's own rule (a): 'the registry is domain-owned and may live in the domain repo' — only the generic validation shape, not any domain's registry/purpose content, is the candidate..
