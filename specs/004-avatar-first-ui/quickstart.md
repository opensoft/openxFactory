# Quickstart — Validate the Avatar-First UI Standard Alignment (offline)

**Feature**: 004-avatar-first-ui | **Date**: 2026-07-11

This is a **validation/run guide**, not implementation code. It shows how to
prove the feature end-to-end with offline, deterministic evidence — no provider,
runtime service, or live model. Run everything from the feature worktree root
(`openxFactory-worktrees/004-avatar-first-ui`).

## Prerequisites

- Python 3.11+ with PyYAML (`python3 -c "import yaml"` succeeds).
- OpenSpec CLI available (`openspec` on PATH).
- The five owned artifacts and the new `examples/avatar-first-ui/fixtures/`
  directory implemented per the plan (this guide is what the implement phase
  makes pass).

## 1. Offline UI validator (primary evidence — FR-020, SC-002/003/004)

```bash
# Default baseline mode (parallel work): resolves IDs/ceilings from the frozen baseline
python3 scripts/validate-avatar-first-ui.py
# Expect: "OK xFactory avatar-first UI template" and exit 0 over the schema,
# template, four representative examples, and the compatibility fixture.
```

Negative fixtures must each fail on exactly their rule (one primary rule per
fixture, stable error ID). If the validator grows a per-fixture mode, run:

```bash
# Illustrative — final flag/path settled in implement phase (see contracts/validator-rules.md)
python3 scripts/validate-avatar-first-ui.py --fixture examples/avatar-first-ui/fixtures/negative/mode-reserved.yaml
# Expect: "ERROR AFUV-MODE-RESERVED ..." and non-zero exit.
```

Expected outcomes:
- All four archetypes + compatibility fixture: PASS (`AFUV-PARITY-EXAMPLE` silent).
- Each negative fixture: fails with its mapped `AFUV-*` ID (see
  `contracts/validator-rules.md`).
- Omitting any new optional field keeps a profile valid (closed default), and no
  field defaults open (SC-004).

## 2. Final-realization cross-check (Phase 3 only — FR-021)

```bash
# Run ONLY after the kernel release; loads exact released registries read-only.
python3 scripts/validate-avatar-first-ui.py --mode realization
# Expect: PASS when the profile's content-addressed coordinates match the released
# bundle tag + commit + digests; fail closed on any registry drift.
```

## 3. OpenSpec strict validation (Principle V, SC-008)

```bash
OPENSPEC_TELEMETRY=0 openspec validate align-avatar-first-ui-standard --strict
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
# Expect: no errors.
```

## 4. Acceptance-map parity (SC-001, SC-008)

Confirm the acceptance map still declares 8 requirements / 25 scenarios and that
every one maps to owned evidence or a named successor:

```bash
python3 - <<'PY'
import yaml, pathlib
m = yaml.safe_load(pathlib.Path(
  "openspec/changes/align-avatar-first-ui-standard/supporting-docs/avatar-first-ui-acceptance-map.yaml"
).read_text())
reqs = m["requirements"]
scen = sum(len(r["scenarios"]) for r in reqs)
assert len(reqs) == m["expected_requirement_count"] == 8, (len(reqs),)
assert scen == m["expected_scenario_count"] == 25, scen
print(f"OK acceptance-map parity: {len(reqs)} requirements / {scen} scenarios")
PY
```

The extended validator also enforces this parity as `AFUV-PARITY-ACCEPTANCE`.

## 5. Ownership-boundary cross-check (SC-007)

```bash
git diff --check   # no whitespace/conflict errors
git status --porcelain
# Expect during parallel work: changes ONLY under docs/avatar-first-ui-standard.md,
# contracts/schemas/avatar-first-ui-profile.schema.yaml, templates/ui/avatar-first.yaml,
# examples/avatar-first-ui/**, scripts/validate-avatar-first-ui.py.
# NO changes to kernel (contracts/avatar-client/**), contracts/manifest.yaml,
# contracts/CHANGELOG.md, contracts/README.md, reference-runtime, F0,
# DomainxFactory, Flutter, or deployment files (those are Phase 3 / out of scope).
```

## 6. Determinism spot-check (SC-006)

```bash
python3 scripts/validate-avatar-first-ui.py > /tmp/run1.txt 2>&1
python3 scripts/validate-avatar-first-ui.py > /tmp/run2.txt 2>&1
diff /tmp/run1.txt /tmp/run2.txt && echo "OK deterministic verdict"
# Fixture expected-shape equivalence is asserted the same way (identical inputs -> identical shapes).
```

## Done when

- Sections 1, 3, 4, 5, 6 pass in `baseline` mode with the artifacts implemented.
- Section 2 is exercised only in the serialized Phase 3 after the kernel release.
- Every `AFU-*` requirement/scenario resolves to owned evidence or a named
  successor; no `AFUV-*` structural or rule error remains.
