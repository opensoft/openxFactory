from __future__ import annotations

import contextlib
import io
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import override

from tests.notebooklm._sync_test_support import HOSTING_DECLARED as TEMPLATE_HOSTING
from tests.notebooklm.typed_sync_contracts import load_typed_sync
from tests.notebooklm.typed_sync_contracts import profile_runner as _profile_runner

HOSTING_DECLARED = TEMPLATE_HOSTING.replace(
    "xFactor001@opensoft.one", "projection-host@example.invalid"
).replace("domain: opensoft.one", "domain: example.invalid")
sync = load_typed_sync()
from tests.notebooklm._projection_test_support import (
    HostingIsolation,
    configure_hosting,
)


class TheDeclarationsPathResolvesFromConfigurationTests(HostingIsolation):
    @override
    def tearDown(self) -> None:
        sync.bind_profile(None)

    def _bind(
        self, root: Path, active: str = "company"
    ) -> tuple[dict[str, str] | None, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            got = sync.enforce_hosting_profile(root, runner=_profile_runner(active))
        return (got, out.getvalue())

    @staticmethod
    def _write(root: Path, rel: str, text: str = HOSTING_DECLARED) -> Path:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_text(text, encoding="utf-8")
        return path

    def scenario_the_env_var_resolves_the_declaration(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            path = self._write(root, "elsewhere/private/hosting.yaml")
            os.environ[sync.HOSTING_ENV] = str(path)
            got, text = self._bind(root)
        assert got is not None
        self.assertEqual(got["account"], "projection-host@example.invalid")
        self.assertIn("verified active", text)

    def scenario_a_workspace_relative_env_var_resolves_from_the_root(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = self._write(root, "elsewhere/private/hosting.yaml")
            os.environ[sync.HOSTING_ENV] = "elsewhere/private/hosting.yaml"
            got, _ = self._bind(root)
        assert got is not None
        self.assertEqual(got["account"], "projection-host@example.invalid")

    def scenario_the_workspace_configuration_resolves_the_declaration(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = self._write(root, "installs/private/hosting.yaml")
            configure_hosting(root, "installs/private/hosting.yaml")
            got, text = self._bind(root)
        assert got is not None
        self.assertEqual(got["account"], "projection-host@example.invalid")
        self.assertIn("verified active", text)

    def scenario_the_env_var_wins_over_the_workspace_configuration(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = self._write(
                root,
                "from-config/hosting.yaml",
                HOSTING_DECLARED.replace(
                    "nlm_profile: company", "nlm_profile: from-the-config-file"
                ),
            )
            configure_hosting(root, "from-config/hosting.yaml")
            _ = self._write(root, "from-env/hosting.yaml")
            os.environ[sync.HOSTING_ENV] = "from-env/hosting.yaml"
            got, _ = self._bind(root)
        assert got is not None
        self.assertEqual(
            got["nlm_profile"],
            "company",
            "the environment variable is FIRST in the order; a config file that also answers must not win",
        )

    def scenario_absent_configuration_is_undeclared_and_does_not_break(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            got, text = self._bind(root, active="whatever-is-active")
        self.assertIsNone(got)
        self.assertIn("NO DECLARED HOSTING IDENTITY", text)
        self.assertIn("transition state", text)
        self.assertIn(
            "nothing is configured",
            text,
            "an undeclared install must be told WHY it is undeclared, or the operator cannot act on it",
        )
        self.assertIsNone(sync.bound_profile())

    def scenario_a_configured_path_that_does_not_exist_is_undeclared(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            configure_hosting(root, "installs/not-cloned-yet/hosting.yaml")
            got, text = self._bind(root, active="whatever-is-active")
        self.assertIsNone(got)
        self.assertIn("NO DECLARED HOSTING IDENTITY", text)
        self.assertIn(
            "is not a readable file",
            text,
            "silence here would let an operator believe the record was read",
        )

    def scenario_a_configured_path_resolving_to_the_shipped_example_is_refused(
        self,
    ) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = self._write(
                root,
                "anywhere/copied-example.yaml",
                HOSTING_DECLARED.replace(
                    "  case: operator_hosted",
                    "  instance: example\n  case: operator_hosted",
                ),
            )
            os.environ[sync.HOSTING_ENV] = "anywhere/copied-example.yaml"
            with self.assertRaises(SystemExit) as caught:
                _ = self._bind(root)
        message = str(caught.exception)
        self.assertIn("SHIPPED SYNTHETIC EXAMPLE", message)
        self.assertIn(
            "copied-example.yaml",
            message,
            "the refusal must name the file the operator configured",
        )
        self.assertIn(
            "declaration_path",
            message,
            "and the exact remedy, like its sibling refusals do",
        )
        self.assertIn("hosting.instance", message)

    def scenario_the_marker_is_read_from_the_record_not_from_the_path(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = self._write(root, "anywhere/copied-example.yaml")
            os.environ[sync.HOSTING_ENV] = "anywhere/copied-example.yaml"
            got, _ = self._bind(root)
        assert got is not None
        self.assertEqual(
            got["account"],
            "projection-host@example.invalid",
            "only the marker refuses; the path never did",
        )

    def scenario_the_shipped_example_is_not_the_last_resort(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = self._write(root, sync.EXAMPLE_REL)
            self.assertIsNone(sync.hosting_declaration_path(root))
            self.assertIsNone(sync.read_hosting_declaration(root))

    def scenario_a_record_marked_live_binds(self) -> None:
        for marker in ("live", "opensoft-production", None):
            with self.subTest(marker=marker), TemporaryDirectory() as td:
                root = Path(td)
                text = (
                    HOSTING_DECLARED
                    if marker is None
                    else HOSTING_DECLARED.replace(
                        "  case: operator_hosted",
                        f"  instance: {marker}\n  case: operator_hosted",
                    )
                )
                _ = self._write(root, "private/hosting.yaml", text)
                os.environ[sync.HOSTING_ENV] = "private/hosting.yaml"
                got, _ = self._bind(root)
                assert got is not None
                self.assertEqual(got["account"], "projection-host@example.invalid")

    def scenario_an_empty_environment_value_is_unset(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = self._write(root, "installs/private/hosting.yaml")
            configure_hosting(root, "installs/private/hosting.yaml")
            os.environ[sync.HOSTING_ENV] = "   "
            self.assertEqual(
                sync.hosting_declaration_path(root),
                root / "installs/private/hosting.yaml",
                "an empty override must fall through to the next step rather than resolving to the workspace root",
            )
