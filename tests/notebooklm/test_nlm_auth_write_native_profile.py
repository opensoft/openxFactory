from __future__ import annotations

import json
import unittest
import unittest.mock
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import override

from notebooklm_sync.nlm_client import JsonValue, decode_json

from tests.notebooklm._sync_test_support import TestSupportError as SupportError
from tests.notebooklm._test_nlm_auth_support import (
    LEGACY,
    STORED,
    nlm_auth,
)


class WriteNativeProfile(unittest.TestCase):
    """The on-disk half: merge, permissions, and refuse-before-write."""

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.tmp: TemporaryDirectory[str] | None = None
        self.store: Path = Path()
        self.pdir: Path = Path()

    @override
    def setUp(self) -> None:
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name)
        self.pdir = self.store / "profiles" / "company"

    def seed(self, metadata: dict[str, JsonValue], cookies: str = "[]") -> None:
        self.pdir.mkdir(parents=True)
        _ = (self.pdir / "metadata.json").write_text(
            json.dumps(metadata), encoding="utf-8"
        )
        _ = (self.pdir / "cookies.json").write_text(cookies, encoding="utf-8")

    def written(self) -> dict[str, JsonValue]:
        value = decode_json((self.pdir / "metadata.json").read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise SupportError("metadata fixture must be an object")
        return value

    def test_a_refresh_preserves_the_hand_set_address(self) -> None:
        self.seed(
            {
                "csrf_token": "old",
                "session_id": "old",
                "email": STORED,
                "build_label": None,
                "last_validated": "2026-08-24T00:00:00",
            }
        )
        pdir, note = nlm_auth.write_native_profile(
            "company",
            [{"name": "SID", "value": "x"}],
            "csrf",
            "session",
            store=self.store,
        )
        self.assertEqual(pdir, self.pdir)
        self.assertEqual(self.written()["email"], STORED)
        self.assertEqual(self.written()["csrf_token"], "csrf")
        self.assertIn(STORED, note)

    def test_a_fresh_profile_is_created_with_restrictive_permissions(self) -> None:
        _ = nlm_auth.write_native_profile(
            "company", [], "csrf", "session", store=self.store
        )
        self.assertEqual(self.written()["email"], None)
        self.assertEqual((self.pdir / "metadata.json").stat().st_mode & 511, 384)
        self.assertEqual((self.pdir / "cookies.json").stat().st_mode & 511, 384)
        self.assertEqual(self.pdir.stat().st_mode & 511, 448)

    def test_unreadable_metadata_does_not_abort_the_write(self) -> None:
        self.pdir.mkdir(parents=True)
        for content in (b"{not json", b"\xff\xfe not utf-8", b"[1, 2, 3]"):
            with self.subTest(content=content[:12]):
                _ = (self.pdir / "metadata.json").write_bytes(content)
                _ = nlm_auth.write_native_profile(
                    "company", [], "csrf", "session", store=self.store
                )
                self.assertEqual(self.written()["csrf_token"], "csrf")
                self.assertIsNone(self.written()["email"])

    def test_a_wrong_account_capture_writes_NOTHING(self) -> None:
        self.seed(
            {"email": STORED, "csrf_token": "old", "session_id": "old"},
            cookies='["original"]',
        )
        with self.assertRaises(nlm_auth.AccountMismatch):
            _ = nlm_auth.write_native_profile(
                "company",
                [{"name": "SID", "value": "wrong-account"}],
                "csrf",
                "session",
                email=LEGACY,
                store=self.store,
            )
        self.assertEqual(self.written()["email"], STORED)
        self.assertEqual(self.written()["csrf_token"], "old")
        self.assertEqual(
            (self.pdir / "cookies.json").read_text(encoding="utf-8"), '["original"]'
        )

    def test_the_store_root_falls_back_to_the_env_var(self) -> None:
        with unittest.mock.patch.dict(
            "os.environ", {"NOTEBOOKLM_MCP_CLI_PATH": str(self.store)}
        ):
            self.assertEqual(nlm_auth.profile_dir("company"), self.pdir)
