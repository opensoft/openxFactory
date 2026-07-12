# Quickstart: AVC Reference Runtime

**Feature**: 003-avc-reference-runtime | **Date**: 2026-07-11

A validation/run guide proving the reference runtime works end-to-end and stays inside its
boundary. This is **not** implementation code — see [data-model.md](./data-model.md) and
[contracts/](./contracts/) for shapes, and `tasks.md` (from `/speckit-tasks`) for the build steps.

## Prerequisites

- Python **3.11+** (matches the existing `xfactory/` floor; no 3.12-only syntax).
- Pinned test-only dependencies (the runtime core needs **none**):
  `pytest`, `pytest-randomly`, `PyYAML`, `jsonschema`.

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install pytest pytest-randomly PyYAML jsonschema   # pinned versions per the repo dev-deps
```

All commands are run from the repository root (the feature worktree).

## 1. Run the deterministic suite (proves protocol behavior — US1)

```bash
python -m pytest tests/avatar_runtime -q
```

Expected: all tests pass with **no** network, filesystem-persistence, sleep, or Hermes access.
Every time-dependent transition is driven by the injected clock (`ManualClock.advance(...)`),
never real elapsed time.

## 2. Prove order-independence over recorded seeds (SC-003)

```bash
# pytest-randomly prints the seed; re-run with a pinned seed to reproduce.
python -m pytest tests/avatar_runtime -p randomly -q            # random seed (printed)
python -m pytest tests/avatar_runtime -p randomly -q -p no:cacheprovider --randomly-seed=12345
python -m pytest tests/avatar_runtime -p randomly -q --randomly-seed=67890
```

Expected: identical authoritative results across seeds and orders. A failing seed is reproducible
by re-running with the printed `--randomly-seed=<n>` (record the seeds used in `realization-pin.yaml`).

## 3. Run the boundary gate (proves non-deployability — US3, SC-005/SC-010)

```bash
python scripts/validate-avatar-runtime.py
```

Expected (execution-free static scan): **no** listener, application factory, deployment manifest,
persistence adapter, live provider SDK, credential loading, or forbidden entrypoint in
`xfactory/avatar_runtime/`; the runtime package imports **only** the standard library; **no**
module imports the provisional test path. The same rules run in-suite via
`tests/avatar_runtime/boundary/test_package_boundary.py`.

## 4. Check acceptance-ID conformance (SC-001/SC-002)

```bash
python tests/avatar_runtime/conformance/check_conformance.py
```

Expected: every runtime-owned `ARR-*` scenario and every applicable `ACR-*` scenario (derived from
the **digest-verified** shared baseline map during parallel work) is either `mapped` to a
collected test node or `non_applicable` with rationale. The checker fails on any missing,
duplicate, dangling, skipped-required, or unknown mapping.

## 5. Feature gate (what runs before every commit / push — Principle V)

```bash
python scripts/validate-avatar-runtime.py \
  && python -m pytest tests/avatar_runtime -p randomly -q \
  && python tests/avatar_runtime/conformance/check_conformance.py
```

`scripts/validate-avatar-runtime.py` is listed in the README validator index (the declared narrow
governance exception; no sibling-owned path is touched — SC-008).

## 6. Realization (only when the released kernel exists — US2)

At realization the provisional adapter is disabled, the checker's acceptance source switches to the
digest-pinned released `contracts/avatar-client/acceptance-map.yaml`, and
`tests/avatar_runtime/conformance/realization-pin.yaml` is populated with the five release
coordinates (tag + exact commit + per-file digests + interface-lock digest + acceptance-map digest)
plus the final conformance results. Realization **fails** if any coordinate is missing, if the
provisional path is reachable, or if canonical execution diverges from the provisional suite
(FR-005, FR-035). See [contracts/conformance-artifacts.md](./contracts/conformance-artifacts.md).

## Success signals (map to Success Criteria)

| Step | Proves |
|------|--------|
| 1–2 | SC-001, SC-003, SC-004 — mapped deterministic tests, order-independent, no ambient deps |
| 3 | SC-005, SC-010 — stdlib-only core, no deployment surface, no provisional reach |
| 4 | SC-002 — every applicable ACR mapped or dispositioned |
| 5 | Principle V gate green (guards intermediate commits) |
| 6 | SC-006, SC-008, SC-009 — five-coordinate pin, no sibling edits, credential-free terminal replay |
