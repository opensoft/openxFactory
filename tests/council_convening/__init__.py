"""Tests for the `council-convening` contract family (feature 035), as a PACKAGE.

A package for the reason `tests/sequenced_after/__init__.py` gives. This
directory holds `test_gate_wiring.py`, and so does `tests/signed_execution_chain/`.
Under pytest's prepend import mode, two same-named modules under a rootdir with
no package chain collide in `sys.modules` and abort collection for the whole
run. As a package, these modules are `council_convening.test_*` instead.

ONE CONSEQUENCE, observed by every module here. pytest imports this package
under the bare name `council_convening`, which is also the basename of the
implementation under test, `scripts/council_convening/`. So the implementation
is ALWAYS imported as `scripts.council_convening`, and never under the bare name,
which here means this package.

The conftest beside this file is a package conftest (`council_convening.conftest`),
not an ambient top-level `conftest`, so it does not contend for the
`sys.modules["conftest"]` slot and needs no `claim_conftest_slot`. That follows
`tests/hermes_runtime_contracts/`.
"""
