"""The `sequenced_after` substrate's tests, as a PACKAGE.

Not a style choice: `tests/scope_globs/` already holds `test_schema.py`,
`test_validate.py` and `test_integrity.py`, and this directory mirrors its
structure deliberately (the two fields are siblings in one front-matter block).
Two same-named test modules under a rootdir with no package chain collide on the
`sys.modules` name in pytest's prepend import mode and abort collection for the
whole run — so this file makes these modules `sequenced_after.test_*` instead.

ONE CONSEQUENCE, and every module here observes it: the implementation under test
is loaded from `scripts/sequenced_after.py` under the name
`sequenced_after_substrate`, NOT `sequenced_after`. Registering the script module
under this package's own name would replace the package in `sys.modules` and
abort collection of every sibling test module.

It is the SAME remedy the house already applies to the identical collision
between `tests/hermes_runtime_contracts/test_release_inventory.py` and
`tests/doc-health/test_release_inventory.py`, where
`tests/hermes_runtime_contracts/__init__.py` is what keeps
`pytest tests/ -q -m "not postgres"` collectable. Deliberately NOT a conftest.py:
`conftest` is an ambient top-level module name with one `sys.modules` entry (see
`pytest.ini`), and a new per-directory conftest is the one thing that must not be
added here.
"""
