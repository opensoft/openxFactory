# Avatar-First UI Examples

Status: draft

These examples show how the shared openxFactory avatar-first UI template and the
registered `avatar-first-ui-profile` schema are instantiated. They are static
contract examples and instantiation stubs (`.example.yaml`) — not runtime state,
and they contain no secrets, customer records, transcripts, or generated
workspaces.

Files:

- [domain-overlays.example.yaml](domain-overlays.example.yaml) — four
  **domain-neutral archetypes** (customer avatar-first, client hybrid, domain
  conventional-first, and confirmation-before-consequential-action) using the
  AVC-aligned blocks: persona reference-only, neutral consent-purpose mappings,
  selected timing within kernel-owned ceilings, retention references, and a
  structured accessibility baseline.
- [fixtures/](fixtures/README.md) — deterministic UI fixtures checked offline by
  `scripts/validate-avatar-first-ui.py`: one compatibility fixture (a legacy
  profile that stays valid), nine negative fixtures (one per enforced rule class,
  each failing exactly one stable `AFUV-*` error), and a deterministic
  offline-acceptance fixture, plus the requirement→evidence map.
