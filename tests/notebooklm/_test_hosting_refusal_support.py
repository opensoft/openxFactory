"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import functools
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import ClassVar
from unittest.mock import patch

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


def _profile_account(profile: str, *, home: Path | None = None) -> str | None:
    from notebooklm_sync.hosting import profile_account

    return profile_account(profile, home=home)


def _unknown_account(_profile: str, _home: Path | None = None) -> None:
    pass


class _ProfileCleanup:
    def tearDown(self) -> None:
        sync.bind_profile(None)


class UnreadableDeclarationFailsClosedTests(_ProfileCleanup, HostingIsolation):
    """A declaration the sync cannot read is NOT an absent one.

    Found in review: the narrow reader wants the `hosting:` block's own
    two-space scalars. Flow style, four-space indentation and tabs are all
    valid YAML — the validator passes them — and all yielded nothing here, so
    the run took the UNDECLARED branch, bound nothing, and left
    `assert_still_bound()` a no-op for the whole job.
    """

    FLOW: ClassVar[str] = (
        "schema_version: 1\nkind: notebook_projection_hosting\n"
        "hosting: {case: operator_hosted, account: x@opensoft.one, "
        "nlm_profile: company}\nshare_out: []\n"
    )
    FOUR: ClassVar[str] = (
        "schema_version: 1\nkind: notebook_projection_hosting\nhosting:\n"
        "    case: operator_hosted\n    account: x@opensoft.one\n"
        "    nlm_profile: company\nshare_out: []\n"
    )
    TABS: ClassVar[str] = (
        "schema_version: 1\nkind: notebook_projection_hosting\nhosting:\n"
        "\tcase: operator_hosted\n\taccount: x@opensoft.one\n"
        "\tnlm_profile: company\nshare_out: []\n"
    )

    def scenario_an_existing_file_always_yields_a_dict_never_none(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, self.FLOW)
            got = sync.read_hosting_declaration(root)
        self.assertEqual(
            got,
            {},
            "present-but-unparsed must be distinguishable " + "from absent",
        )

    def scenario_an_absent_file_is_the_only_undeclared_case(self) -> None:
        with TemporaryDirectory() as td:
            self.assertIsNone(sync.read_hosting_declaration(Path(td)))

    def scenario_each_unreadable_shape_refuses_instead_of_running_unbound(self) -> None:
        for label, text in (
            ("flow", self.FLOW),
            ("four-space", self.FOUR),
            ("tabs", self.TABS),
        ):
            with self.subTest(shape=label), TemporaryDirectory() as td:
                root = Path(td)
                declare_hosting(root, text)
                with self.assertRaises(SystemExit) as caught:
                    _ = sync.enforce_hosting_profile(
                        root, runner=profile_runner("personal")
                    )
                self.assertIn("no declaration could be read", str(caught.exception))


class MigrationStateVocabularyTests(_ProfileCleanup, HostingIsolation):
    """The sync owns the state vocabulary too — one rule, not two gates.

    Found in review: `state: in_progress` FAILED the validator and PASSED the
    sync, which then bound the DECLARED profile while the books were still in
    the previous account — a premature migration under `--apply`.
    """

    BASE: ClassVar[str] = """schema_version: 1
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

    def _enforce(self, text: str, active: str) -> dict[str, str] | None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, text)
            with contextlib.redirect_stdout(io.StringIO()):
                return sync.enforce_hosting_profile(root, runner=profile_runner(active))

    def scenario_an_unrecognized_state_is_refused(self) -> None:
        with self.assertRaises(SystemExit) as caught:
            _ = self._enforce(self.BASE.format(state="in_progress"), "company")
        self.assertIn("migration.state", str(caught.exception))

    def scenario_pending_and_complete_are_both_accepted(self) -> None:
        self.assertIsNotNone(
            self._enforce(self.BASE.format(state="pending"), "personal")
        )
        self.assertIsNotNone(
            self._enforce(self.BASE.format(state="complete"), "company")
        )

    def scenario_a_pending_migration_without_a_from_profile_is_refused(self) -> None:
        text = self.BASE.format(state="pending").replace(
            "    from_nlm_profile: personal\n", ""
        )
        with self.assertRaises(SystemExit) as caught:
            _ = self._enforce(text, "personal")
        self.assertIn("from_nlm_profile", str(caught.exception))

    def scenario_the_top_level_profile_is_required_even_while_pending(self) -> None:
        text = self.BASE.format(state="pending").replace("  nlm_profile: company\n", "")
        with self.assertRaises(SystemExit) as caught:
            _ = self._enforce(text, "personal")
        self.assertIn("no top-level nlm_profile", str(caught.exception))


class ProfileAccountIsCheckedWhenTheCliRecordedOneTests(
    _ProfileCleanup, unittest.TestCase
):
    """The CLI DOES store a profile's email — this change first claimed it did not.

    `profiles/<name>/metadata.json` carries `email`: populated by a recent
    login, left null by an older one. Null means UNKNOWN and is reported; a
    populated address that disagrees with the declaration is a refusal.
    """

    @staticmethod
    def _home(root: Path, profile: str, email: str | None) -> Path:
        home = root / "cli-home"
        d = home / "profiles" / profile
        d.mkdir(parents=True)
        body = "null" if email is None else f'"{email}"'
        _ = (d / "metadata.json").write_text(f'{{"email": {body}}}', encoding="utf-8")
        return home

    def scenario_a_recorded_address_is_read(self) -> None:
        with TemporaryDirectory() as td:
            home = self._home(Path(td), "company", "xFactor001@opensoft.one")
            self.assertEqual(
                _profile_account("company", home=home), "xFactor001@opensoft.one"
            )

    def scenario_a_null_address_is_unknown_not_empty_string(self) -> None:
        with TemporaryDirectory() as td:
            home = self._home(Path(td), "company", None)
            self.assertIsNone(_profile_account("company", home=home))

    def scenario_a_missing_profile_directory_is_unknown(self) -> None:
        with TemporaryDirectory() as td:
            self.assertIsNone(_profile_account("nope", home=Path(td) / "cli-home"))

    def scenario_the_right_profile_name_signed_in_as_the_wrong_account_refuses(
        self,
    ) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, HOSTING_DECLARED)
            home = self._home(root, "company", "someone-else@elsewhere.test")
            # the REAL reader, pointed at a synthetic CLI home
            real = functools.partial(_profile_account, home=home)
            with (
                patch.object(sync, "profile_account", real),
                self.assertRaises(SystemExit) as caught,
            ):
                _ = sync.enforce_hosting_profile(root, runner=profile_runner("company"))
        message = str(caught.exception)
        self.assertIn("signed in as someone-else@elsewhere.test", message)
        self.assertIn("nlm login --profile company", message)

    def scenario_an_unknown_address_is_reported_not_treated_as_a_mismatch(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, HOSTING_DECLARED)
            out = io.StringIO()
            with (
                patch.object(sync, "profile_account", _unknown_account),
                contextlib.redirect_stdout(out),
            ):
                got = sync.enforce_hosting_profile(
                    root, runner=profile_runner("company")
                )
        self.assertIsNotNone(
            got,
            "an older login that recorded no address must " + "not block the run",
        )
        self.assertIn("records no account address", out.getvalue())
