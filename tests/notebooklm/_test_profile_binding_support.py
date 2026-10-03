"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from notebooklm_sync.nlm_client import (
    assert_still_bound,
    bind_profile,
    bound_profile,
    clear_profile_cache,
    configured_nlm_profile,
    reset_profile_state,
)

from tests.notebooklm._projection_test_support import HostingIsolation
from tests.notebooklm._sync_test_support import (
    HOSTING_DECLARED,
)
from tests.notebooklm.typed_sync_contracts import (
    declare_hosting,
    load_typed_sync,
    profile_runner,
)

sync = load_typed_sync()


class _ProfileCleanup:
    def tearDown(self) -> None:
        reset_profile_state()


class ProfileBindingHoldsForTheWholeRunTests(_ProfileCleanup, HostingIsolation):
    """The binding is re-asserted before EVERY invocation, not once.

    Found in review: profile selection is process-global, so another terminal
    running `nlm login switch` after the opening check would silently redirect
    every later add and delete into a different account — across a re-derivation
    that takes about forty minutes.
    """

    @staticmethod
    def _config(root: Path, profile: str) -> Path:
        path = root / "config.toml"
        _ = path.write_text(
            '[output]\nformat = "table"\n\n[auth]\n'
            + f'browser = "auto"\ndefault_profile = "{profile}"\n',
            encoding="utf-8",
        )
        return path

    def scenario_the_configured_profile_is_read_from_the_file(self) -> None:
        with TemporaryDirectory() as td:
            path = self._config(Path(td), "company")
            self.assertEqual(configured_nlm_profile(path), "company")

    def scenario_an_absent_config_is_unknown(self) -> None:
        with TemporaryDirectory() as td:
            self.assertIsNone(configured_nlm_profile(Path(td) / "nope.toml"))

    def scenario_an_unbound_run_asserts_nothing(self) -> None:
        bind_profile(None)
        assert_still_bound()  # must not raise

    def scenario_a_profile_switched_mid_run_refuses_the_next_invocation(self) -> None:
        with TemporaryDirectory() as td:
            path = self._config(Path(td), "company")
            reset_profile_state(path)
            bind_profile("company")
            assert_still_bound()  # still bound: no raise
            _ = self._config(Path(td), "personal")  # another terminal switches
            clear_profile_cache()
            with self.assertRaises(SystemExit) as caught:
                assert_still_bound()
        message = str(caught.exception)
        self.assertIn("changed mid-run", message)
        self.assertIn("nlm login switch company", message)

    def scenario_the_cache_does_not_hide_a_switch(self) -> None:
        with TemporaryDirectory() as td:
            path = self._config(Path(td), "company")
            reset_profile_state(path)
            bind_profile("company")
            assert_still_bound()
            # rewrite with a different size so the (mtime_ns, size) stamp
            # moves even inside one filesystem timestamp tick
            _ = path.write_text(
                '[auth]\ndefault_profile = "a-different-one"\n', encoding="utf-8"
            )
            with self.assertRaises(SystemExit):
                assert_still_bound()


class DeclarationIsEnforcedOnTheOperationalPathTests(
    _ProfileCleanup, unittest.TestCase
):
    """The refusals must fire during an ordinary run, not only in the validator.

    Found in review: nothing the sync runs invoked the validator, so a
    declaration naming a consumer or service account would have been accepted
    by `--apply`.
    """

    def _enforce(
        self, root: Path, text: str, active: str = "company"
    ) -> dict[str, str] | None:
        declare_hosting(root, text)
        return sync.enforce_hosting_profile(root, runner=profile_runner(active))

    def scenario_a_service_account_is_refused_by_the_sync_itself(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace(
                "account: xFactor001@opensoft.one",
                "account: books@xf.iam.gserviceaccount.com",
            ).replace("domain: opensoft.one", "domain: xf.iam.gserviceaccount.com")
            with self.assertRaises(SystemExit) as caught:
                _ = self._enforce(root, text)
        self.assertIn("service account", str(caught.exception))

    def scenario_a_consumer_account_is_refused_for_the_operator_hosted_case(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace(
                "account_type: google_workspace_user",
                "account_type: consumer_google_account",
            )
            with self.assertRaises(SystemExit) as caught:
                _ = self._enforce(root, text)
        self.assertIn("google_workspace_user", str(caught.exception))

    def scenario_an_account_outside_the_declared_domain_is_refused(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace(
                "domain: opensoft.one", "domain: elsewhere.example"
            )
            with self.assertRaises(SystemExit) as caught:
                _ = self._enforce(root, text)
        self.assertIn("not in the declared domain", str(caught.exception))

    def scenario_a_third_case_is_refused(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace(
                "case: operator_hosted", "case: partly_hosted"
            )
            with self.assertRaises(SystemExit) as caught:
                _ = self._enforce(root, text)
        self.assertIn("exactly one of", str(caught.exception))

    def scenario_a_conforming_declaration_binds_the_run(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                got = self._enforce(root, HOSTING_DECLARED)
        if got is None:
            raise AssertionError("conforming declaration did not bind")
        self.assertEqual(got["account"], "xFactor001@opensoft.one")
        self.assertEqual(
            bound_profile(), "company", "a bound run must pin the profile it verified"
        )

    def scenario_an_undeclared_install_releases_the_pin(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            bind_profile("stale")
            with contextlib.redirect_stdout(io.StringIO()):
                _ = sync.enforce_hosting_profile(
                    root, runner=profile_runner("personal")
                )
        self.assertIsNone(bound_profile())

    def scenario_a_self_hosted_personal_declaration_is_accepted(self) -> None:
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
        if got is None:
            raise AssertionError("self-hosted declaration did not bind")
        self.assertEqual(
            got["case"],
            "self_hosted",
            "an individual's own account is a complete binding",
        )

    def scenario_nlm_itself_reasserts_the_binding_before_running(self) -> None:
        """The wire, not just the check.

        `assert_still_bound()` is only worth anything if `nlm()` calls it: a
        drift detector nothing invokes is decoration. Asserted by driving the
        REAL `nlm()` with a drifted config and a stubbed subprocess, so the
        refusal must come from the binding rather than from the CLI.
        """
        with TemporaryDirectory() as td:
            path = Path(td) / "config.toml"
            _ = path.write_text(
                '[auth]\ndefault_profile = "someone-else"\n', encoding="utf-8"
            )
            ran: list[tuple[str, ...]] = []

            def record_run(*args: str, **kwargs: bool) -> None:
                del kwargs
                ran.append(args)

            reset_profile_state(path)
            with patch.object(sync.subprocess, "run", record_run):
                bind_profile("company")
                with self.assertRaises(SystemExit) as caught:
                    _ = sync.nlm("notebook", "list", "--json")
        self.assertIn("changed mid-run", str(caught.exception))
        self.assertEqual(
            ran,
            [],
            "the invocation must be refused BEFORE the "
            + "subprocess, not after it has written",
        )
