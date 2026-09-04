"""Makes this directory a PACKAGE, so its test modules get unique names.

WHY IT IS HERE, and it is not a style choice. `tests/factory_identity/
test_gate_wiring.py` (added with the register realization) collides by BASENAME
with the pre-existing `tests/signed_execution_chain/test_gate_wiring.py`, and
under pytest's default `prepend` import mode a test file in a non-package
directory is imported under its bare basename — so two files named
`test_gate_wiring.py` contend for one `sys.modules` entry and collection
ABORTS. Measured on this branch's base commit: `python3 -m pytest tests/ -q -m
"not postgres"` (the REQUIRED `pytest-suite` invocation) collected 8761 of 9099
and then interrupted with one collection error, while
`pytest tests/factory_identity -q` — a single directory, no collision in scope
— was green. A per-directory run cannot see this class of defect at all.

With this file present, pytest walks up only until a directory has no
`__init__.py`, which is `tests/` — so the module name becomes
`factory_identity.test_gate_wiring` and the collision is gone.

THE ESTABLISHED PATTERN IN THIS SUITE, followed rather than invented:
`tests/sequenced_after/` is a package for exactly this reason (its
`test_integrity.py`, `test_schema.py` and `test_validate.py` all collide with
`tests/scope_globs/`), and so are `tests/avatar_client_validator/` and
`tests/hermes_runtime_contracts/`. Renaming the file would work too and was
rejected: the name says what it pins, both files pin the same KIND of thing in
different families, and a directory that is already a package cannot collide
again the next time a family adds a `test_gate_wiring.py`.

IT IS ALSO WHY THIS DIRECTORY NEEDS NO conftest.py, and must not grow one. A
package directory's conftest is imported as `<package>.conftest` and never
contends for the ambient flat `conftest` slot — but this directory has no
conftest at all, and the FR-043 hermeticity guard reaches it through
`tests/conftest.py`, which the repo-root `pytest.ini` rootdir anchor keeps in
the chain for every in-repo invocation. See `tests/hermeticity.py`.
"""
