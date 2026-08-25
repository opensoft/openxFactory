# Tasks: The Register and Its Reader (S4)

**Feature**: 014-register-and-reader | **Branch**: `014-register-and-reader` | **Date**: 2026-08-25
**Input**: [spec.md](./spec.md) · [plan.md](./plan.md) · [research.md](./research.md) · [data-model.md](./data-model.md) · [quickstart.md](./quickstart.md)

Scope guard (ratified tasks §5 + design D11): register and reader in ONE
change; kindless register (no contract schema authored); first root grant
included per operator ruling. Floor entry BY NAME stays task 5.4
(codexFactory). Revocation surface stays S5.

## Phase 1 — Grounding & rulings

- [x] T001 Governing texts verified: intake spec delta requirements 1–5,
      D4/D11, N7/N8, Q1c wording; reader home = the named validator inside
      S1's required check.
- [x] T002 Operator rulings recorded: grant+register together; target
      opensoft/openxFactory; expires ~90 days.

## Phase 2 — Reader

- [x] T003 Rule (u) docstring + `check_register`/`_load_attestations` +
      repo_scan wiring: strict row shape; wallet/grant resolution and
      reconciliation; computed expiry (N8) incl. stale-state finding on the
      grant; act-tier attestation coupling; minimal-shape bound; absent-
      register posture split by review-grant presence.
- [x] T004 Eight self-test probes green (clean / computed-expiry triple /
      no-active-row via empty rows / tier-act-unattested / minimal-shape /
      row-malformed / absent-register postures).

## Phase 3 — Live artifacts

- [x] T005 `governance/review-authority/register.yaml` — header carries Q1c
      constraint, permanently-human-only declaration, by-name floor pointer,
      D11 no-schema note; one MVP row.
- [x] T006 `governance/review-authority/grants/grant-mrc-0001.yaml` — FIRST
      root review-authority grant; anchored issuer; tier act over
      opensoft/openxFactory; ~90-day term.

## Phase 4 — Gates

- [x] T007x Gates: whole-checkout sweep exit 0 with BOTH live artifacts
      validated; corpus unchanged 17/36 across 13/13; live mutation probe
      fired `register-no-active-row` through production wiring (restored);
      pytest wallet_yaml_syntax_gate 4 passed; openspec validate --all
      --strict 75 passed / 0 failed; boundary proofs clean vs branch base
      dda06ba3; zero private material in diff. Evidence in
      implementation-notes.md.

## Dependencies

T001–T002 → T003 → T004 → T005/T006 → T007x. Reader before artifacts, so the
live tree lands already enforced.

## Implementation strategy

Prove every refusal code on synthesized trees first; only then let real
authority depend on it. The mutation probe then proves the production wiring
(not just the unit path), once, with immediate restore — nothing red is ever
committed.
