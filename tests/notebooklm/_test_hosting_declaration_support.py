"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import io
from collections.abc import Callable
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from notebooklm_sync.nlm_client import ProviderResult

from tests.notebooklm._projection_test_support import HostingIsolation
from tests.notebooklm._sync_test_support import (
    HOSTING_DECLARED,
    HOSTING_PENDING,
    FakeNlm,
)
from tests.notebooklm.typed_sync_contracts import (
    constant_runner,
    declare_hosting,
    load_typed_sync,
    profile_runner,
)

sync = load_typed_sync()


class HostingDeclarationTests(HostingIsolation):
    """The declaration is READ, and the run is BOUND to it or refused."""

    def scenario_undeclared_install_is_reported_as_a_transition_state_not_a_case(
        self,
    ) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                got = sync.enforce_hosting_profile(
                    root, runner=profile_runner("personal")
                )
        self.assertIsNone(got, "an undeclared install has no declaration to return")
        self.assertIn("NO DECLARED HOSTING IDENTITY", out.getvalue())
        self.assertIn(
            "transition state",
            out.getvalue(),
            "undeclared must be reported as nonconforming, never as "
            + "a third legitimate case",
        )

    def scenario_declared_profile_active_binds_the_run(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, HOSTING_DECLARED)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                got = sync.enforce_hosting_profile(
                    root, runner=profile_runner("company")
                )
        if got is None:
            raise AssertionError("declared profile did not bind")
        self.assertEqual(got["account"], "xFactor001@opensoft.one")
        self.assertIn("verified active", out.getvalue())

    def scenario_a_run_pointed_at_another_account_refuses(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, HOSTING_DECLARED)
            with self.assertRaises(SystemExit) as caught:
                _ = sync.enforce_hosting_profile(
                    root, runner=profile_runner("personal")
                )
        message = str(caught.exception)
        self.assertIn(
            "Refusing",
            message,
            "writing a governed projection into an undeclared "
            + "account is the failure this capability retires",
        )
        self.assertIn(
            "nlm login switch company",
            message,
            "the refusal must carry the exact remediation command",
        )

    def scenario_an_unreadable_profile_refuses_rather_than_guessing(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, HOSTING_DECLARED)
            with self.assertRaises(SystemExit) as caught:
                _ = sync.enforce_hosting_profile(root, runner=profile_runner(None))
        self.assertIn("cannot prove", str(caught.exception))

    def scenario_a_pending_migration_binds_to_the_account_that_holds_the_books(
        self,
    ) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, HOSTING_PENDING)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                got = sync.enforce_hosting_profile(
                    root, runner=profile_runner("personal")
                )
        self.assertIsNotNone(got)
        self.assertIn("MIGRATION PENDING", out.getvalue())
        self.assertIn(
            "brettheap@gmail.com",
            out.getvalue(),
            "a declaration is not a migration: until the books move, "
            + "the run binds where they actually live",
        )

    def scenario_a_pending_migration_still_refuses_a_third_account(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, HOSTING_PENDING)
            with self.assertRaises(SystemExit):
                _ = sync.enforce_hosting_profile(
                    root, runner=profile_runner("someone-else")
                )

    def scenario_the_reader_ignores_comments_and_nested_blocks(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            declare_hosting(root, "# leading comment\n" + HOSTING_PENDING)
            got = sync.read_hosting_declaration(root)
        if got is None:
            raise AssertionError("declared hosting file was not read")
        self.assertEqual(got["nlm_profile"], "company")
        self.assertEqual(got["migration_from_nlm_profile"], "personal")
        self.assertEqual(got["case"], "operator_hosted")


class ParityReportTests(HostingIsolation):
    """Parity is proven against THE CORPUS SCAN, never against other books."""

    @staticmethod
    def _world(root: Path) -> None:
        (root / "openxFactory/examples").mkdir(parents=True, exist_ok=True)
        _ = (
            root / "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
        ).write_text("workspaces:\n", encoding="utf-8")
        for g in sync.GROUNDING:
            p = root / g
            p.parent.mkdir(parents=True, exist_ok=True)
            _ = p.write_text("# Grounding\n", encoding="utf-8")
        base = root / "openxFactory/ideation/brainstorm"
        base.mkdir(parents=True, exist_ok=True)
        _ = (base / "idea-00.md").write_text(
            "# Idea\n\nStatus: brainstorm\n", encoding="utf-8"
        )

    def _run_parity(
        self, root: Path, fake: Callable[..., ProviderResult]
    ) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), patch.object(sync, "nlm", fake):
            code = sync.parity_report(root)
        return code, out.getvalue()

    def scenario_a_book_missing_a_derived_title_fails_parity(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            fake = FakeNlm(
                [
                    {"id": f"nb{i}", "title": specs[k].title}
                    for i, k in enumerate(sorted(desired))
                ]
            )
            code, text = self._run_parity(root, fake)
        self.assertEqual(
            code,
            1,
            "an empty live book cannot be at parity with "
            + "a scan that derives members",
        )
        self.assertIn("PARITY FAIL", text)
        self.assertIn("MISSING", text)

    def scenario_matching_books_prove_parity_with_nothing_pending(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            fake = FakeNlm(
                [
                    {"id": f"nb{i}", "title": specs[k].title}
                    for i, k in enumerate(sorted(desired))
                ]
            )
            for i, key in enumerate(sorted(desired)):
                fake.sources[f"nb{i}"] = [
                    {"id": f"s{i}-{j}", "title": title}
                    for j, title in enumerate(sorted(desired[key].values()))
                ]
            code, text = self._run_parity(root, fake)
        self.assertEqual(code, 0, text)
        self.assertIn("parity: PROVEN", text)
        self.assertIn("0 pending ADD/DEL/UPD", text)

    def scenario_parity_never_mutates(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            fake = FakeNlm(
                [
                    {"id": f"nb{i}", "title": specs[k].title}
                    for i, k in enumerate(sorted(desired))
                ]
            )
            _ = self._run_parity(root, fake)
            verbs = {call[:2] for call in fake.calls}
        # `alias set` belongs in this blocklist: the alias store is a single
        # flat file shared across profiles, so registering one during a parity
        # proof repoints xf-canon for every account on the host.
        for mutating in (
            ("source", "add"),
            ("source", "delete"),
            ("notebook", "create"),
            ("notebook", "delete"),
            ("alias", "set"),
            ("alias", "delete"),
        ):
            self.assertNotIn(
                mutating,
                verbs,
                "a parity proof that changes the thing it measures " + "is not a proof",
            )

    def scenario_a_non_string_profile_answer_is_unknown_not_a_crash(self) -> None:
        """A runner that answers with anything but text means 'unknown'.

        The refusal path depends on this returning None rather than raising:
        an exception here would escape the guard instead of becoming the
        governed refusal.
        """
        answers: tuple[ProviderResult, ...] = ({}, [], None, 42)
        for answer in answers:
            with self.subTest(answer=answer):
                self.assertIsNone(sync.active_nlm_profile(constant_runner(answer)))
