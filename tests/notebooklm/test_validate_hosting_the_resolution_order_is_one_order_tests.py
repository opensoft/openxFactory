from __future__ import annotations

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tests.notebooklm._test_validate_hosting_support import BASE, sync_module, validator


class TheResolutionOrderIsOneOrderTests(unittest.TestCase):
    """TWO IMPLEMENTATIONS, ONE ORDER — and this refuses them to diverge.

    The sync carries no YAML dependency and must not gain one, and it is HANDED
    its workspace root rather than discovering one, so the resolver could not
    simply be shared as code. What CAN be shared is the order, the variable name
    and the configuration path — and a duplicated order that drifts is worse
    than no sharing at all, because each reader would bind a different file
    while both reported success.
    """

    def test_both_readers_name_the_same_environment_variable(self) -> None:
        self.assertEqual(validator.HOSTING_ENV, "XFACTORY_NOTEBOOK_HOSTING_DECLARATION")
        self.assertEqual(sync_module().HOSTING_ENV, validator.HOSTING_ENV)

    def test_both_readers_name_the_same_configuration_file(self) -> None:
        self.assertEqual(
            validator.HOSTING_CONFIG_REL, ".xfactory/notebook-hosting.yaml"
        )
        self.assertEqual(sync_module().HOSTING_CONFIG_REL, validator.HOSTING_CONFIG_REL)

    def test_both_readers_agree_on_the_example_marker(self) -> None:
        self.assertEqual(
            sync_module().HOSTING_EXAMPLE_MARKER, validator.HOSTING_EXAMPLE_MARKER
        )

    def test_both_readers_resolve_the_same_three_cases_the_same_way(self) -> None:
        """The order itself, driven through both implementations."""
        sync = sync_module()
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "a").mkdir()
            (root / "b").mkdir()
            from_env = root / "a" / "hosting.yaml"
            from_cfg = root / "b" / "hosting.yaml"
            _ = from_env.write_text(BASE, encoding="utf-8")
            _ = from_cfg.write_text(BASE, encoding="utf-8")
            cfg = root / validator.HOSTING_CONFIG_REL
            cfg.parent.mkdir(parents=True, exist_ok=True)
            _ = cfg.write_text("declaration_path: b/hosting.yaml\n", encoding="utf-8")
            with patch.dict(os.environ, {}, clear=False):
                _ = os.environ.pop(validator.HOSTING_ENV, None)
                self.assertEqual(sync.hosting_declaration_path(root), from_cfg)
                self.assertEqual(validator.hosting_declaration_path(root), from_cfg)
                os.environ[validator.HOSTING_ENV] = "a/hosting.yaml"
                self.assertEqual(sync.hosting_declaration_path(root), from_env)
                self.assertEqual(validator.hosting_declaration_path(root), from_env)
                os.environ[validator.HOSTING_ENV] = str(from_env)
                self.assertEqual(sync.hosting_declaration_path(root), from_env)
                self.assertEqual(validator.hosting_declaration_path(root), from_env)
            cfg.unlink()
            with patch.dict(os.environ, {}, clear=False):
                _ = os.environ.pop(validator.HOSTING_ENV, None)
                self.assertIsNone(sync.hosting_declaration_path(root))
                self.assertIsNone(validator.hosting_declaration_path(root))
