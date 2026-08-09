---
code_surface: openxFactory (contracts/omnigent/ schema + example + negative fixtures; scripts/validate-omnigent-contracts.py semantic checks)
target_release: implemented
Status: draft
---

# Proposal: add-omnigent-domain-terminology

## Why

Brett, 2026-08-09: "i like that we have a neutral spine cross domain. but we
also need to have all notices to users and logs be show in domain best
practice and well adopted terminology to make easy for the domain experts to
understand."

Both halves of that are right, and today only the first is served. The five
domain overlays (codex, Medx, opsx, adx, ledgerx) all map onto the same
neutral archetype spine (`frame | generate | verify | challenge |
assemble_for_admission`), which is what makes the family coherent. But the
worker class ids — `blast_radius_reviewer`, `posting_admission_agent`,
`persona_panel` — are the ONLY names a human-facing surface can render
today, and they are internal identifiers, not the vocabulary an IT
operations lead, a controller, or a media director actually uses. Every
notice, log line, approval packet, escalation, and refusal therefore speaks
machine, in a system whose entire safety story is "a human reads this and
approves."

The wrong fix is renaming the taxonomy to an industry standard. That would
point each domain at a DIFFERENT framework (ITIL for opsx, AICPA for
ledgerx, IAB for adx), weakening the cross-domain spine rather than
strengthening it; it would churn ids that are load-bearing in
`credential_requirements.by_class`, `routing`, overlay-manifest digests, and
every install and fixture; and it would make a trademarked framework term
the identity of a product role.

The right fix already has precedent in this contract family, twice. This
very schema declares `permission_aliases` — domain-facing permission names
aliased onto the neutral booleans. And the Hermes layer model states the
same separation for layers: "Roles are fixed vocabulary. Display names may
be specialized by an installation without changing role or authority
ownership." This change extends that established pattern from permissions
and layers to the rest of the overlay's declared vocabulary.

## What Changes

- **ADD an optional `terminology` block to the omnigent-domain-overlay
  contract** — display labels for the ids the overlay declares (`workers`,
  `job_types`, `stop_conditions`, `routing` classes). Presentation only: a
  label never changes a worker's archetype, permissions, credential tier, or
  authority. Additive and optional, so all five existing overlays stay valid
  (verified: codex, Medx, opsx, adx, ledgerx all still pass).
- **ADD an optional `standards_alignment` crosswalk per worker class** —
  `framework` + `mapping` (+ `note`), descriptive only. It asserts no
  conformance, certification, or endorsement, and never becomes the class
  identity. Where a class has no honest counterpart in the framework, the
  literal `no_clean_equivalent` WITH a note is required rather than a forced
  mapping — the failure mode being avoided is a crosswalk that quietly
  overstates a worker's authority by borrowing a weightier standard term.
- **Require human-facing rendering**: notices, logs, approval packets,
  escalations, and refusals render the declared label where one exists, so
  domain experts read their own terminology, while ids stay machine
  identifiers and the neutral archetype spine is never renamed.
- **Semantic validation** in `validate-omnigent-contracts.py`: every
  terminology key must resolve to an id the overlay declares (an orphan
  label names a class that does not exist), display labels must be unique
  within a vocabulary (two ids reading identically in a notice is the defect),
  and `no_clean_equivalent` requires its note. Two negative fixtures added,
  each with its `# expect:` marker.

## Impact

- One capability modified: `omnigent-domain-overlay` (3 ADDED requirements).
  No existing requirement is weakened; the archetype vocabulary, permission
  matrix, credential tiers, and authority-conservation rules are untouched.
- Additive and optional at the contract layer — no domain overlay is
  invalidated, and no worker id, digest, or credential binding changes.
- Domain follow-ups (each its own change, in its own repo): populate
  `terminology` for codex, Medx, opsx, adx, and ledgerx. Those are where the
  actual best-practice vocabulary gets chosen per domain, with the crosswalk
  framework named per domain rather than assumed here.
- Consumer follow-up beyond the overlay: domain surfaces that render their
  OWN human-facing vocabulary outside the overlay — for example
  OpsxFactory's fixed-order adjudication refusals, which today name internal
  check ids like `tenant_managed` — should adopt the same
  render-the-domain-label principle in their own contracts. Named here so
  the principle is not silently scoped to omnigent alone.
