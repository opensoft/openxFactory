from __future__ import annotations

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import override
from unittest.mock import patch

from tests.notebooklm._test_validate_hosting_support import (
    BASE,
    is_example,
    validate_text,
    validator,
)


class TheResolvedDeclarationIsValidatedTests(unittest.TestCase):
    """The path resolves from configuration, and what it finds IS VALIDATED.

    adopt-configured-notebook-hosting-identity: "moving the record out of this
    repository moves WHERE it is checked and never WHETHER it is checked".
    These are the validator's half of that sentence — the sync's half is
    `tests/notebooklm/test_sync_notebooklm_books.py::
    TheDeclarationsPathResolvesFromConfigurationTests`.
    """

    @override
    def setUp(self) -> None:
        super().setUp()
        previous = dict(os.environ)
        self.addCleanup(os.environ.update, previous)
        self.addCleanup(os.environ.clear)
        _ = os.environ.pop(validator.HOSTING_ENV, None)

    @staticmethod
    def _tree(
        td: str, text: str = BASE, rel: str = "private/hosting.yaml"
    ) -> tuple[Path, Path]:
        root = Path(td)
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_text(text, encoding="utf-8")
        return (root, path)

    def test_a_resolved_declaration_is_validated(self) -> None:
        """One of the three things replacing the lost CI check (design § 3.4)."""
        with TemporaryDirectory() as td:
            root, path = self._tree(td)
            os.environ[validator.HOSTING_ENV] = str(path)
            self.assertEqual(validator.hosting_declaration_path(root), path)
            self.assertEqual(
                validator.validate(path),
                [],
                "a resolved declaration is checked by the SAME validator, against the same requirement",
            )

    def test_a_resolved_declaration_that_does_not_conform_still_fails(self) -> None:
        """The point of the previous test is only worth anything with this one."""
        with TemporaryDirectory() as td:
            root, path = self._tree(
                td, BASE.replace("case: operator_hosted", "case: partly_hosted")
            )
            os.environ[validator.HOSTING_ENV] = str(path)
            resolved = validator.hosting_declaration_path(root)
            assert resolved is not None
            errors = validator.validate(resolved)
        self.assertTrue(any("hosting.case" in e for e in errors), errors)

    def test_the_workspace_configuration_resolves_the_declaration(self) -> None:
        with TemporaryDirectory() as td:
            root, path = self._tree(td)
            cfg = root / validator.HOSTING_CONFIG_REL
            cfg.parent.mkdir(parents=True, exist_ok=True)
            _ = cfg.write_text(
                "declaration_path: private/hosting.yaml\n", encoding="utf-8"
            )
            self.assertEqual(validator.hosting_declaration_path(root), path)

    def test_the_env_var_wins_over_the_workspace_configuration(self) -> None:
        with TemporaryDirectory() as td:
            root, path = self._tree(td, rel="from-env/hosting.yaml")
            _ = self._tree(td, rel="from-config/hosting.yaml")
            cfg = root / validator.HOSTING_CONFIG_REL
            cfg.parent.mkdir(parents=True, exist_ok=True)
            _ = cfg.write_text(
                "declaration_path: from-config/hosting.yaml\n", encoding="utf-8"
            )
            os.environ[validator.HOSTING_ENV] = str(path)
            self.assertEqual(validator.hosting_declaration_path(root), path)

    def test_absent_configuration_resolves_to_nothing(self) -> None:
        with TemporaryDirectory() as td:
            self.assertIsNone(validator.hosting_declaration_path(Path(td)))

    def test_resolved_refuses_rather_than_falling_back_to_the_fixture(self) -> None:
        """--resolved is the LIVE record's evidence, so it may not answer about
        the fixture. A green line over a synthetic instance would be evidence
        about a synthetic instance, which is not what an operator asked."""
        with TemporaryDirectory() as td:
            root = Path(td)

            def fixture_root(_repo: Path) -> Path:
                return root

            with patch.object(validator, "workspace_root", fixture_root):
                code = validator.main(["prog", "--resolved"])
        self.assertEqual(code, 1)

    def test_resolved_refuses_a_record_marked_as_an_example(self) -> None:
        """The same fail-closed arm the sync carries, for the same reason."""
        with TemporaryDirectory() as td:
            marked = BASE.replace(
                "  case: operator_hosted",
                "  instance: example\n  case: operator_hosted",
            )
            _root, path = self._tree(td, marked)
            os.environ[validator.HOSTING_ENV] = str(path)
            self.assertTrue(is_example(path))
            code = validator.main(["prog", "--resolved"])
        self.assertEqual(
            code,
            1,
            "configuration pointing at a fixture must not produce a green conformance line",
        )

    def test_the_marker_does_not_make_an_otherwise_conforming_record_invalid(
        self,
    ) -> None:
        """`instance:` is metadata about the instance, not a conformance failure.

        The shipped example carries it and must still pass `validate()` — the
        refusal belongs to the RESOLUTION path, not to the record's shape.
        """
        marked = BASE.replace(
            "  case: operator_hosted", "  instance: example\n  case: operator_hosted"
        )
        self.assertEqual(validate_text(marked), [])

    def test_an_explicit_path_still_wins_over_everything(self) -> None:
        """`argv[1]` was already the override and stays the first arm."""
        with TemporaryDirectory() as td:
            root, path = self._tree(td)
            os.environ[validator.HOSTING_ENV] = str(root / "nowhere.yaml")
            code = validator.main(["prog", str(path)])
        self.assertEqual(code, 0)
