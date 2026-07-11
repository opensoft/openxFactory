# AVC Reference Runtime — Test Suite

Deterministic conformance suite for `xfactory/avatar_runtime/` (feature
`specs/003-avc-reference-runtime`). The runtime package is **standard-library
only**; only this test tree and `scripts/validate-avatar-runtime.py` use pinned
dev dependencies.

## Toolchain

- **Python**: 3.11+ (no 3.12-only syntax in the runtime package).
- **Pinned dev dependencies** (test/validator only): `pytest`,
  `pytest-randomly`, `PyYAML`, `jsonschema`.

Create a worktree-local virtualenv (gitignored / locally excluded — never
committed) and install:

```bash
python3 -m venv --system-site-packages .venv && . .venv/bin/activate
pip install pytest pytest-randomly PyYAML jsonschema
```

## Running

```bash
# Deterministic suite (random order via pytest-randomly; the seed is printed):
python -m pytest tests/avatar_runtime -p randomly -q

# Reproduce a specific order/seed:
python -m pytest tests/avatar_runtime -p randomly --randomly-seed=<N> -q

# Boundary gate (execution-free static scan of the runtime package):
python scripts/validate-avatar-runtime.py

# Acceptance-ID conformance (scenario-test-map vs acceptance maps + collected tests):
python tests/avatar_runtime/conformance/check_conformance.py
```

## Seed convention (SC-003)

Order-independence is proven with `pytest-randomly`. Record **at least three**
seeds per gate run (the header line `avatar-runtime randomly-seed: <N>` reports
each). The recorded seeds are written to
`tests/avatar_runtime/conformance/realization-pin.yaml` (`conformance.seeds`) at
the Polish/realization step. Any failing seed is reproducible by re-running with
`--randomly-seed=<N>`.

## Layout

- `fakes/` — in-memory `FakeProvider` + fail-closed policy/consent/operation/usage fixtures.
- `provisional/` — test-only `avatar-client-parallel-v1` adapter (unreachable from the package).
- `boundary/` — pure-stdlib AST scanner + boundary tests + suite-hygiene lint.
- `conformance/` — `scenario-test-map.yaml`, `realization-pin.yaml`, `check_conformance.py`.
- `test_*.py` — the deterministic behavioral suite (one file per protocol concern).
