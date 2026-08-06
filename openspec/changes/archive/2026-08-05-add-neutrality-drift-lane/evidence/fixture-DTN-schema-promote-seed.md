# Drafted DTN Register Seed — DTN-025

Status: record
Kind: register-seed-draft
Drafted by: doc-health neutrality-drift lane (run 4e7b81a490ba, 2026-08-05)
Subject: xFactories/zephyrFactory/schemas/session-envelope.schema.yaml
Content-SHA256: 9831a3baf033605d4a1a9351b613960d8208be9b6c351b3bd80c6ab80cc39646

Approval: merge the row and section below into
`docs/domain-neutralization-candidate-register.md`. Rejection: record a
disposition in health/dispositions.yaml (family neutrality-drift,
keyed repo + path + content_sha256).

## Register row

| DTN-025 | A JSON Schema (YAML) for a 'gate intent' — a signed, attributed request that a g | `promote` | P2 | `seed` | contracts/schemas/gate-intent.schema.yaml |

## Register detail section

### DTN-025: A JSON Schema (YAML) for a 'gate intent' — a signed, attributed request that a g

Machine-drafted seed from the doc-health neutrality-drift lane (2026-08-05, run 4e7b81a490ba, prompt contract v1, model claude-sonnet-5; confidence 0.88) — pending human approval; this candidate enters the register lifecycle only when the seed is merged. Stage-1 signals: lexicon_absence, near_duplicate.

A JSON Schema (YAML) for a 'gate intent' — a signed, attributed request that a gate-console verb (demote, edit-apply, ratify, kickoff, dispose-possible, propose, promote-to-staging, derive-possibles, research-brief) be applied, with actor/verb/target/snapshot/status lifecycle fields.

Evidence:

- `xFactories/zephyrFactory/schemas/session-envelope.schema.yaml` (content sha256 `9831a3baf033`)
- The document's own $id and title declare it 'gate-intent.schema.yaml' / 'Gate intent: a signed, attributed REQUEST for a gate-console action', which contradicts its local filename 'session-envelope.schema.yaml' — the content itself, not the path, identifies what it is.
- Every property (actor, verb, target.change_id/possible_id/cluster_id/topic_id, snapshot_rev_seen, status, idempotency_key) models a generic gate-console request/apply lifecycle with no domain-specific noun anywhere in the schema body.
- The description explicitly frames the contract as serving 'a zero-write-authority client (the hosted dashboard, the Flutter verdict terminal)' talking to 'the gate-console engine' — infrastructure-agnostic actors, not domain participants.
- Token-set similarity of 1.00 against openxFactory/contracts/schemas/gate-intent.schema.yaml indicates this is a verbatim copy of an already-established neutral contract, not an independently-evolved domain artifact.

Counter-evidence:

- The verb enum names ('demote', 'kickoff', 'dispose-possible', 'promote-to-staging', 'derive-possibles', 'research-brief') are specific to the ideation-dashboard workflow vocabulary and would need that same wheel/possible/cluster/topic model to be meaningful to a consuming domain.

Domain-local exclusions: none identified by the scout.
