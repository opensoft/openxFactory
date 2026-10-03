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
    ExtractionContext,
    ExtractionPage,
    nlm_auth,
)


class ExtractAndSave(unittest.TestCase):
    """The wiring: capture -> merge -> refuse, with `verify()` never run."""

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
        self.pdir.mkdir(parents=True)
        _ = (self.pdir / "metadata.json").write_text(
            json.dumps({"email": STORED, "csrf_token": "old", "session_id": "old"}),
            encoding="utf-8",
        )

    def run_extract(self, captured_email: str, force: bool = False) -> int:
        cookies = [
            {"name": n, "value": "v", "domain": ".google.com"}
            for n in nlm_auth.REQUIRED
        ]
        ctx = ExtractionContext(cookies=lambda: cookies)
        page = ExtractionPage(content=lambda: "<html>page</html>")
        with unittest.mock.patch.object(nlm_auth, "verify", return_value=0):
            return nlm_auth.extract_and_save(
                ctx,
                page,
                "company",
                1,
                lambda _html: "csrf",
                lambda _html: "session",
                lambda _html: captured_email,
                force=force,
                store=self.store,
            )

    def metadata(self) -> dict[str, JsonValue]:
        value = decode_json((self.pdir / "metadata.json").read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise SupportError("metadata fixture must be an object")
        return value

    def test_the_right_account_is_confirmed_and_the_address_kept(self) -> None:
        self.assertEqual(self.run_extract(STORED), 0)
        self.assertEqual(self.metadata()["email"], STORED)
        self.assertEqual(self.metadata()["csrf_token"], "csrf")

    def test_no_capture_still_carries_the_address_forward(self) -> None:
        self.assertEqual(self.run_extract(""), 0)
        self.assertEqual(self.metadata()["email"], STORED)

    def test_a_wrong_account_exits_non_zero_and_writes_nothing(self) -> None:
        self.assertNotEqual(self.run_extract(LEGACY), 0)
        self.assertEqual(self.metadata()["email"], STORED)
        self.assertEqual(self.metadata()["csrf_token"], "old")
        self.assertFalse((self.pdir / "cookies.json").exists())

    def test_force_records_the_captured_account(self) -> None:
        self.assertEqual(self.run_extract(LEGACY, force=True), 0)
        self.assertEqual(self.metadata()["email"], LEGACY)
