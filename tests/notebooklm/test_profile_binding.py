"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tests.notebooklm._sync_test_support import (
    HOSTING_DECLARED,
    _declare_hosting,
    _profile_runner,
    sync,
)


class ProfileBindingHoldsForTheWholeRunTests(unittest.TestCase):
    """The binding is re-asserted before EVERY invocation, not once.

    Found in review: profile selection is process-global, so another terminal
    running `nlm login switch` after the opening check would silently redirect
    every later add and delete into a different account — across a re-derivation
    that takes about forty minutes.
    """

    def tearDown(self):
        sync.reset_profile_state()

    @staticmethod
    def _config(root: Path, profile: str) -> Path:
        path = root / "config.toml"
        path.write_text(f'[output]\nformat = "table"\n\n[auth]\n'
                        f'browser = "auto"\ndefault_profile = "{profile}"\n',
                        encoding="utf-8")
        return path

    def test_the_configured_profile_is_read_from_the_file(self):
        with TemporaryDirectory() as td:
            path = self._config(Path(td), "company")
            self.assertEqual(sync.configured_nlm_profile(path), "company")

    def test_an_absent_config_is_unknown(self):
        with TemporaryDirectory() as td:
            self.assertIsNone(
                sync.configured_nlm_profile(Path(td) / "nope.toml"))

    def test_an_unbound_run_asserts_nothing(self):
        sync.bind_profile(None)
        sync.assert_still_bound()  # must not raise

    def test_a_profile_switched_mid_run_refuses_the_next_invocation(self):
        with TemporaryDirectory() as td:
            path = self._config(Path(td), "company")
            sync.reset_profile_state(path)
            sync.bind_profile("company")
            sync.assert_still_bound()          # still bound: no raise
            self._config(Path(td), "personal")  # another terminal switches
            sync.clear_profile_cache()
            with self.assertRaises(SystemExit) as caught:
                sync.assert_still_bound()
        message = str(caught.exception)
        self.assertIn("changed mid-run", message)
        self.assertIn("nlm login switch company", message)

    def test_the_cache_does_not_hide_a_switch(self):
        with TemporaryDirectory() as td:
            path = self._config(Path(td), "company")
            sync.reset_profile_state(path)
            sync.bind_profile("company")
            sync.assert_still_bound()
            # rewrite with a different size so the (mtime_ns, size) stamp
            # moves even inside one filesystem timestamp tick
            path.write_text('[auth]\ndefault_profile = "a-different-one"\n',
                            encoding="utf-8")
            with self.assertRaises(SystemExit):
                sync.assert_still_bound()

class DeclarationIsEnforcedOnTheOperationalPathTests(unittest.TestCase):
    """The refusals must fire during an ordinary run, not only in the validator.

    Found in review: nothing the sync runs invoked the validator, so a
    declaration naming a consumer or service account would have been accepted
    by `--apply`.
    """

    def tearDown(self):
        sync.bind_profile(None)

    def _enforce(self, root: Path, text: str, active: str = "company"):
        _declare_hosting(root, text)
        return sync.enforce_hosting_profile(root, runner=_profile_runner(active))

    def test_a_service_account_is_refused_by_the_sync_itself(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace(
                "account: xFactor001@opensoft.one",
                "account: books@xf.iam.gserviceaccount.com").replace(
                "domain: opensoft.one", "domain: xf.iam.gserviceaccount.com")
            with self.assertRaises(SystemExit) as caught:
                self._enforce(root, text)
        self.assertIn("service account", str(caught.exception))

    def test_a_consumer_account_is_refused_for_the_operator_hosted_case(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace(
                "account_type: google_workspace_user",
                "account_type: consumer_google_account")
            with self.assertRaises(SystemExit) as caught:
                self._enforce(root, text)
        self.assertIn("google_workspace_user", str(caught.exception))

    def test_an_account_outside_the_declared_domain_is_refused(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace("domain: opensoft.one",
                                            "domain: elsewhere.example")
            with self.assertRaises(SystemExit) as caught:
                self._enforce(root, text)
        self.assertIn("not in the declared domain", str(caught.exception))

    def test_a_third_case_is_refused(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace("case: operator_hosted",
                                            "case: partly_hosted")
            with self.assertRaises(SystemExit) as caught:
                self._enforce(root, text)
        self.assertIn("exactly one of", str(caught.exception))

    def test_a_conforming_declaration_binds_the_run(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                got = self._enforce(root, HOSTING_DECLARED)
        self.assertEqual(got["account"], "xFactor001@opensoft.one")
        self.assertEqual(sync.bound_profile(), "company",
                         "a bound run must pin the profile it verified")

    def test_an_undeclared_install_releases_the_pin(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            sync.bind_profile("stale")
            with contextlib.redirect_stdout(io.StringIO()):
                sync.enforce_hosting_profile(
                    root, runner=_profile_runner("personal"))
        self.assertIsNone(sync.bound_profile())

    def test_a_self_hosted_personal_declaration_is_accepted(self):
        text = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: self_hosted
  account: someone@gmail.com
  nlm_profile: personal
share_out: []
"""
        with TemporaryDirectory() as td:
            root = Path(td)
            with contextlib.redirect_stdout(io.StringIO()):
                got = self._enforce(root, text, active="personal")
        self.assertEqual(got["case"], "self_hosted",
                         "an individual's own account is a complete binding")

    def test_nlm_itself_reasserts_the_binding_before_running(self):
        """The wire, not just the check.

        `assert_still_bound()` is only worth anything if `nlm()` calls it: a
        drift detector nothing invokes is decoration. Asserted by driving the
        REAL `nlm()` with a drifted config and a stubbed subprocess, so the
        refusal must come from the binding rather than from the CLI.
        """
        with TemporaryDirectory() as td:
            path = Path(td) / "config.toml"
            path.write_text('[auth]\ndefault_profile = "someone-else"\n',
                            encoding="utf-8")
            ran = []
            sync.reset_profile_state(path)
            with patch.object(sync.subprocess, "run",
                              lambda *a, **k: ran.append(a)):
                sync.bind_profile("company")
                with self.assertRaises(SystemExit) as caught:
                    sync.nlm("notebook", "list", "--json")
        self.assertIn("changed mid-run", str(caught.exception))
        self.assertEqual(ran, [], "the invocation must be refused BEFORE the "
                                  "subprocess, not after it has written")
