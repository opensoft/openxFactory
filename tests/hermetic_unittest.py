"""`unittest discover`, with the FR-043 hermeticity guard installed FIRST.

`scripts/validate-docs.sh` runs its test directories through pytest, and falls
back to `python3 -m unittest discover` when pytest is unavailable. That fallback
was structurally outside the guard — a conftest fixture cannot apply to a runner
that never loads conftests — and PR #49 review finding 17 measured a probe in
`tests/notebooklm/` reaching a real-binary `nlm` stand-in TWICE from it, with the
refusal ledger empty. A gate whose degraded path is unguarded is a gate that stops
being one on any host that happens to lack pytest.

So the gate invokes THIS instead of `unittest` directly. It installs the same two
layers `tests/hermeticity.py` gives pytest, from the same declarations
(`install_binary_shim`, `runner_seams`) so the two routes cannot drift, and then
runs the ordinary discovery. Nothing about the discovery changes: one
`start_dir=<directory>` per argument with `pattern="test_*.py"`, which is exactly
what `-s <dir> -p "test_*.py"` did, and the exit status is non-zero if ANY
directory fails.

Deliberately importable without pytest: this is the no-pytest world by definition,
which is why `import pytest` is optional in `tests/hermeticity.py`.

    python3 tests/hermetic_unittest.py tests/notebooklm/ tests/review-lane/
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))

import hermeticity  # noqa: E402  (after the path insert, by construction)


def install_guard(where: Path | None = None) -> Path:
    """Both layers, in this process. Returns the shim directory.

    Layer 2 is a plain `setattr` rather than a monkeypatch: there is no fixture
    lifetime here, the process exists to run one discovery, and the seams must be
    poisoned before the first test module imports anything."""
    root = Path(where) if where is not None \
        else Path(tempfile.mkdtemp(prefix="hermetic-unittest-"))
    shim, _restore = hermeticity.install_binary_shim(root / "bin")
    for target, attribute, replacement in hermeticity.runner_seams():
        setattr(target, attribute, replacement)
    return shim


def run(directories, *, verbosity: int = 1) -> int:
    loader = unittest.TestLoader()
    ok = True
    for directory in directories:
        start = str(directory)
        suite = loader.discover(start_dir=start, pattern="test_*.py",
                                top_level_dir=start)
        result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
        ok = ok and result.wasSuccessful()
    return 0 if ok else 1


def main(argv=None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if not args:
        sys.stderr.write("usage: python3 tests/hermetic_unittest.py <dir> [<dir>…]\n")
        return 2
    install_guard()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
