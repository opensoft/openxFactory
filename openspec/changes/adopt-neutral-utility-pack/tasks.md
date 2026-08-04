# Tasks: adopt-neutral-utility-pack

## 1. openxFactory adopts (this change)

- [x] 1.1 Copy from codexFactory
      main@1568c54b65e0de1dc63d9eef771f299ddbe60fcf with provenance (D1),
      via `git archive` from the object DB (no sibling working-tree reads):
      `scripts/check-inventory-consistency.py`,
      `scripts/check-workflow-state-parity.py`,
      `scripts/check-openxfactory-pin.py`, `scripts/proposal-support.py`,
      `tests/conformance-gate/`, `tests/proposal-support/`, and
      `schemas/hermes-template.schema.json` →
      `contracts/hermes-domain-overlay/hermes-layer-template.schema.json`
      (D4). Evidence 2026-08-03: `proposal-support.py` adopted
      byte-identical (source sha256 `7095279f032dc6da…`); the three checks
      and the conformance test module carry only the classified 1.2 edits;
      the schema differs from source (sha256 `9ac5aa880d4ffb55…`) only in
      `$id`/title/description (D4). openxFactory's existing pytest
      infrastructure (pytest.ini anchor, tests/conftest.py hermeticity
      guard) already hosts the suites — nothing re-copied from the pin's
      test scaffolding.
- [x] 1.2 Path hygiene + CLI-target verification. Full `codexFactory` grep
      over the adopted files, classified — FIXED: the three checks'
      docstrings now name the neutral capability and the run-from-pinned
      consumption shape (was "conformance-gate capability"); help text
      "codexFactory repo root (default: this script's repo)" → "domain repo
      root to check"; the wrong-target self-repo CLI defaults dropped — the
      target `repo_root`/`workflows_dir` positionals are now REQUIRED (the
      publisher checkout is not a domain repo, and codexFactory's
      validate-docs.sh already passes `"$REPO_ROOT"` explicitly, so the D2
      repoint stays path-only); the conformance test docstring cites the
      neutral spec, qualifying the codexFactory origin; the two real-repo
      self-gate tests (`test_inventory_real_repo_is_consistent`,
      `test_parity_all_real_pairs_pass`) guarded with
      `skipif(not DOMAIN_SHAPED)` — they target the HOSTING repo, which is
      now the publisher; schema `$id`/title/description neutralized (D4).
      KEPT as legitimate: the FLOW_YAML fixture's
      `kind: codex_workflow_contract` (fixture stub for a plausible domain
      instance; the parity check never reads `kind`) and the frozen machine
      kinds `subject_hermes_template`/`client_hermes_template` +
      `role: client` const (layer-vocabulary frozen v1 spellings).
      CLI-target verification: all four tools take the target as an
      explicit argument (domain repo root ×2, workflows dir, OpenSpec repo
      root) — verified functionally by running the three checks from this
      checkout against a pin-extracted codexFactory tree: inventory ok,
      parity ok, pin check SKIP with notice outside aggregation scope (as
      specified); `proposal-support.py` needs no fix (target `root` was
      already a required positional).
- [x] 1.3 `contracts/hermes-domain-overlay/README.md` gains the
      layer-template schema row in its Files list.
- [x] 1.4 README.md: Conformance section row for the utility pack
      (mirroring the canonical-validator rows) + OpenSpec Records entry for
      this change.

## 2. codexFactory sheds (named follow-up PR: change/shed-neutral-utility-pack)

- [x] 2.1 Remove the moved surface: `scripts/check-inventory-consistency.py`,
      `scripts/check-workflow-state-parity.py`,
      `scripts/check-openxfactory-pin.py`, `scripts/proposal-support.py`,
      `schemas/hermes-template.schema.json`, `tests/conformance-gate/`,
      `tests/proposal-support/`.
- [x] 2.2 `scripts/validate-docs.sh` repoints (path-only, D2): the three
      conformance-check invocations move from `python3 scripts/<name>` to
      the resolved `$OPENX/scripts/<name>` copies (the
      `resolve_openxfactory()` block already exists; the checks join the
      canonical-validator section and fail closed in CI when no checkout
      resolves); drop `tests/proposal-support/` and `tests/conformance-gate/`
      from the pytest and hermetic_unittest suite lists.
- [x] 2.3 Inventory edit — REQUIRED, verified at the pin: `stack.yaml`
      `schemas.required` lists `hermes-template.schema.json` (line 122) and
      `schemas/README.md` carries its table row (line 18: "Hermes layer
      templates (subject/client)"); both entries must drop with the file or
      the now-pinned-checkout inventory check fails the shed PR itself.
- [x] 2.4 Repoint the remaining in-repo references found at the pin
      (CONTRIBUTING.md, workflows/README.md mentions of the moved scripts)
      and retire/redirect codexFactory's promoted `conformance-gate` spec
      text that names local script paths — its own codexFactory OpenSpec
      change, same class as the doc-health-checker retirement flagged by
      adopt-neutral-tooling-home tranche C.

## 3. Register

- [x] 3.1 `docs/domain-neutralization-candidate-register.md`: DTN-018,
      DTN-019, DTN-021 table rows → `implemented`; one realized-by line
      appended to each detail section naming this change and the adoption
      pin. `adopted` waits for the 2.x shed + gate repoint (register
      adoption rule: local copy stays authoritative until the re-pin gate
      completes).

## 4. Gates

- [x] 4.1 `python3 -m pytest tests/conformance-gate tests/proposal-support
      -q` → 23 passed, 2 skipped (the two publisher-checkout self-gate
      skips of 1.2, each naming its reason).
- [x] 4.2 Each adopted script's `--help` runs from the new home;
      `hermes-layer-template.schema.json` parses and
      `jsonschema.Draft202012Validator.check_schema` passes.
- [x] 4.3 `OPENSPEC_TELEMETRY=0 openspec validate adopt-neutral-utility-pack
      --strict` and `--all --strict` green.
- [x] 4.4 Existing quick suite unaffected: `tests/ideation_dashboard` 45
      passed.

## Shed execution record (2026-08-03)

Realized as codexFactory PR #73 (merge 25e46fd1bf, branch
change/shed-utility-pack@4d90eec): 18 files / -1,963 lines; validate-docs.sh
repointed to the pinned checkout with explicit targets; stack.yaml re-pinned
ff64e81 -> 45129cf7 (required for the shed's own CI; v1.29 ancestry + doxBench
digests verified); hermes-template inventory entries dropped; the council-lane
runbook deletion rode along (aggregation adoption xFactory@19b06ba).
DTN-018/019/021 -> adopted (domain re-pin + local-copy retirement complete).
Deferred per task 2.4: retiring codexFactory's conformance-gate spec.
