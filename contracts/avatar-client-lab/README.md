# Avatar Client Lab — Neutral Acceptance (openxFactory-owned)

Status: draft
Kind: register
Repository context: openxFactory
Proposed by: implement-avatar-client-lab

Neutral, openxFactory-owned acceptance surface for the **offline deterministic
avatar client lab**. The Flutter application and its Dart bindings live in
codexFactory under `apps/avatar-client-lab/`; openxFactory owns the neutral
contracts, conformance fixtures, and the acceptance map the client is measured
against (spec `avatar-client-lab`, requirement *Repository and ownership
boundary*).

## Contents

- [`client-acceptance-map.yaml`](client-acceptance-map.yaml) — the client-lab
  acceptance map. It **declares** what the lab proves; it holds no Flutter
  evidence (evidence nodes are produced in codexFactory, and a scenario's status
  effectively flips only when that work lands). It transcribes, **verbatim**, the
  inherited ACR/SCO/RBG/AFU scenario slice that the two released acceptance maps
  already name `implement-avatar-client-lab` as an `owner_change` for
  (`supporting-docs/acceptance-and-tests.md` claim 2), maps each scenario to its
  planned client evidence class — `fixture` (reducer replay), `golden` (widget /
  avatar frame), or `successor` (deferred / discharged via the successor evidence
  register) — per FR-040 (reducer + widget behaviour, **not** schema re-proof),
  and carries the gating frame: the **nine** offline CI gates and the **eleven**
  accessibility-baseline capabilities, plus the F1-F4 acceptance foci.

## Ownership boundary (why this lives here, not in a bundle dir)

This map is **not** a member of either released bundle. It lives OUTSIDE
`contracts/avatar-client/` (so none of the AVC kernel's digest / metadata /
redaction scans touch it) and OUTSIDE `examples/avatar-first-ui/`. The two
released acceptance maps, the released evidence register, and
`contracts/manifest.yaml` stay **byte-identical**. The one deferred scenario the
lab owns (`SCO-001-S05`) is discharged only through the successor register
`contracts/avatar-client/evidence-register.implement-avatar-client-lab.yaml`
(locked decision 7), never by an entry here.

## Validation

Machine-checked fail-closed by
`scripts/validate-avatar-client.py::check_client_lab_acceptance_map`: verbatim
id + title parity against the released source maps, owner linkage (no
overclaiming), requirement-level completeness (no silently dropped inherited
requirement), the exact nine gates / eleven a11y capabilities, evidence-class and
gate-reference legality, referenced-fixture existence, and successor-register
consistency for any `discharge_via`. Negative coverage lives in
`tests/avatar_client_validator/test_client_lab_acceptance_map.py`.

The replayable seeds the map references are the deterministic UI fixtures under
`examples/avatar-first-ui/fixtures/deterministic/` (the released
`offline-acceptance` / `six-state-transition-arc` seeds plus the task-4.2
governed-denial, control-lost-failure, and consent-withdraw worked-scenario
seeds).
