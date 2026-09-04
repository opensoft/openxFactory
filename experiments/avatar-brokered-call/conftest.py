"""Collection guard for this experiment's isolated test suite (issue #625).

`tests/` here imports the `avatar_f0` package, which lives only inside this
experiment's own venv — see README.md's "Setup" (`pip install -e .
--no-deps` after `pip install -r requirements.lock`) and RUN.md, both of
which document running this suite with `cd experiments/avatar-brokered-call`
first. The root repository's environment never installs that package, so a
bare `pytest` invocation at the repo root that walks into this directory
always failed collection with `ModuleNotFoundError: No module named
'avatar_f0'` — one error per test file, 19 in total.

Adding `testpaths = tests` to the root `pytest.ini` was tried first and
reverted: `scripts/hermes_runtime_validation/pytest_config.py` statically
parses `pytest.ini`'s `[pytest]` section and requires every key there to be
in `ALLOWED_COLLECTION_OPTIONS` (currently only `markers`) before it trusts
its own static PostgreSQL-marker test-node inventory; adding `testpaths`
failed that check closed and broke six tests under
`tests/hermes_runtime_contracts/` with "unsupported pytest collection
configuration". That option is repo-wide, so this experiment's problem
cannot be fixed there without touching an unrelated invariant.

Ignore this directory's tests instead — but only when `avatar_f0` is not
actually importable, so the suite still collects normally for anyone running
pytest from inside this experiment's own venv (its `pyproject.toml` already
scopes `testpaths` to `tests/offline` for that case). This leaves the root
`pytest.ini` untouched and changes nothing about CI's `tests/` invocation,
which never walks here.
"""

from __future__ import annotations

import importlib.util

collect_ignore: list[str] = []

if importlib.util.find_spec("avatar_f0") is None:
    collect_ignore = ["tests"]
