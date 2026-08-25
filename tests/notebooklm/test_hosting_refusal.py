"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import functools
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


class UnreadableDeclarationFailsClosedTests(unittest.TestCase):
    """A declaration the sync cannot read is NOT an absent one.

    Found in review: the narrow reader wants the `hosting:` block's own
    two-space scalars. Flow style, four-space indentation and tabs are all
    valid YAML — the validator passes them — and all yielded nothing here, so
    the run took the UNDECLARED branch, bound nothing, and left
    `assert_still_bound()` a no-op for the whole job.
    """

    def tearDown(self):
        sync.bind_profile(None)

    FLOW = ("schema_version: 1\nkind: notebook_projection_hosting\n"
            "hosting: {case: operator_hosted, account: x@opensoft.one, "
            "nlm_profile: company}\nshare_out: []\n")
    FOUR = ("schema_version: 1\nkind: notebook_projection_hosting\nhosting:\n"
            "    case: operator_hosted\n    account: x@opensoft.one\n"
            "    nlm_profile: company\nshare_out: []\n")
    TABS = ("schema_version: 1\nkind: notebook_projection_hosting\nhosting:\n"
            "\tcase: operator_hosted\n\taccount: x@opensoft.one\n"
            "\tnlm_profile: company\nshare_out: []\n")

    def test_an_existing_file_always_yields_a_dict_never_none(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, self.FLOW)
            got = sync.read_hosting_declaration(root)
        self.assertEqual(got, {}, "present-but-unparsed must be distinguishable "
                                  "from absent")

    def test_an_absent_file_is_the_only_undeclared_case(self):
        with TemporaryDirectory() as td:
            self.assertIsNone(sync.read_hosting_declaration(Path(td)))

    def test_each_unreadable_shape_refuses_instead_of_running_unbound(self):
        for label, text in (("flow", self.FLOW), ("four-space", self.FOUR),
                            ("tabs", self.TABS)):
            with self.subTest(shape=label), TemporaryDirectory() as td:
                root = Path(td)
                _declare_hosting(root, text)
                with self.assertRaises(SystemExit) as caught:
                    sync.enforce_hosting_profile(
                        root, runner=_profile_runner("personal"))
                self.assertIn("no declaration could be read",
                              str(caught.exception))

class MigrationStateVocabularyTests(unittest.TestCase):
    """The sync owns the state vocabulary too — one rule, not two gates.

    Found in review: `state: in_progress` FAILED the validator and PASSED the
    sync, which then bound the DECLARED profile while the books were still in
    the previous account — a premature migration under `--apply`.
    """

    def tearDown(self):
        sync.bind_profile(None)

    BASE = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: operator_hosted
  account: xFactor001@opensoft.one
  account_type: google_workspace_user
  domain: opensoft.one
  nlm_profile: company
  migration:
    state: {state}
    from_account: brettheap@gmail.com
    from_nlm_profile: personal
share_out: []
"""

    def _enforce(self, text: str, active: str):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, text)
            with contextlib.redirect_stdout(io.StringIO()):
                return sync.enforce_hosting_profile(
                    root, runner=_profile_runner(active))

    def test_an_unrecognized_state_is_refused(self):
        with self.assertRaises(SystemExit) as caught:
            self._enforce(self.BASE.format(state="in_progress"), "company")
        self.assertIn("migration.state", str(caught.exception))

    def test_pending_and_complete_are_both_accepted(self):
        self.assertIsNotNone(
            self._enforce(self.BASE.format(state="pending"), "personal"))
        self.assertIsNotNone(
            self._enforce(self.BASE.format(state="complete"), "company"))

    def test_a_pending_migration_without_a_from_profile_is_refused(self):
        text = self.BASE.format(state="pending").replace(
            "    from_nlm_profile: personal\n", "")
        with self.assertRaises(SystemExit) as caught:
            self._enforce(text, "personal")
        self.assertIn("from_nlm_profile", str(caught.exception))

    def test_the_top_level_profile_is_required_even_while_pending(self):
        text = self.BASE.format(state="pending").replace(
            "  nlm_profile: company\n", "")
        with self.assertRaises(SystemExit) as caught:
            self._enforce(text, "personal")
        self.assertIn("no top-level nlm_profile", str(caught.exception))

class ProfileAccountIsCheckedWhenTheCliRecordedOneTests(unittest.TestCase):
    """The CLI DOES store a profile's email — this change first claimed it did not.

    `profiles/<name>/metadata.json` carries `email`: populated by a recent
    login, left null by an older one. Null means UNKNOWN and is reported; a
    populated address that disagrees with the declaration is a refusal.
    """

    def tearDown(self):
        sync.bind_profile(None)

    @staticmethod
    def _home(root: Path, profile: str, email) -> Path:
        home = root / "cli-home"
        d = home / "profiles" / profile
        d.mkdir(parents=True)
        body = "null" if email is None else f'"{email}"'
        (d / "metadata.json").write_text(f'{{"email": {body}}}',
                                         encoding="utf-8")
        return home

    def test_a_recorded_address_is_read(self):
        with TemporaryDirectory() as td:
            home = self._home(Path(td), "company", "xFactor001@opensoft.one")
            self.assertEqual(sync.profile_account("company", home=home),
                             "xFactor001@opensoft.one")

    def test_a_null_address_is_unknown_not_empty_string(self):
        with TemporaryDirectory() as td:
            home = self._home(Path(td), "company", None)
            self.assertIsNone(sync.profile_account("company", home=home))

    def test_a_missing_profile_directory_is_unknown(self):
        with TemporaryDirectory() as td:
            self.assertIsNone(
                sync.profile_account("nope", home=Path(td) / "cli-home"))

    def test_the_right_profile_name_signed_in_as_the_wrong_account_refuses(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, HOSTING_DECLARED)
            home = self._home(root, "company", "someone-else@elsewhere.test")
            # the REAL reader, pointed at a synthetic CLI home
            real = functools.partial(sync.profile_account, home=home)
            with (
                patch.object(sync, "profile_account", real),
                self.assertRaises(SystemExit) as caught,
            ):
                sync.enforce_hosting_profile(
                    root, runner=_profile_runner("company")
                )
        message = str(caught.exception)
        self.assertIn("signed in as someone-else@elsewhere.test", message)
        self.assertIn("nlm login --profile company", message)

    def test_an_unknown_address_is_reported_not_treated_as_a_mismatch(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, HOSTING_DECLARED)
            out = io.StringIO()
            with (
                patch.object(sync, "profile_account", lambda *a, **k: None),
                contextlib.redirect_stdout(out),
            ):
                got = sync.enforce_hosting_profile(
                    root, runner=_profile_runner("company")
                )
        self.assertIsNotNone(got, "an older login that recorded no address must "
                                  "not block the run")
        self.assertIn("records no account address", out.getvalue())

