"""Tests for the NotebookLM auth harness (`scripts/nlm_auth.py`).

Two defects are pinned here.

**opensoft/openxFactory#543 — the harness erased the account address the sync
enforces.** `write_native_profile()` built its metadata dict literally with
`"email": None, "build_label": None` and overwrote `metadata.json`, on the
`refresh` path as well as `bootstrap`. That nulled the address
`enforce_hosting_profile()` reads, and a null there means UNKNOWN — so the
address refusal was skipped and the run proceeded on the profile NAME alone,
which cannot tell one Google account from another. The tests below hold the
merge: an address is carried forward, never nulled, and a captured address that
CONTRADICTS the stored one refuses before anything is written.

**opensoft/openxFactory#537 (harness half) — the page predicate knew only the
old host.** After the provider's rebrand a signed-in tab is on
`notebook.google.com`, so the predicate matched nothing, fell through to
`ctx.pages[0]` and navigated an arbitrary tab. Both hosts are accepted now.

NO BROWSER AND NO NETWORK. Playwright is not a dependency of this suite, so the
module is loaded with a REFUSING `playwright.sync_api` stub in `sys.modules`
when the real package is absent; every context/page here is a plain fake. No
test touches the real profile store either — the store root is injected
(`store=`), never `~/.notebooklm-mcp-cli`.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import types
import unittest
import unittest.mock
from pathlib import Path
from tempfile import TemporaryDirectory


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "nlm_auth.py"


def _load_nlm_auth():
    """Import the harness by path, stubbing playwright only if it is absent.

    The stub's `sync_playwright` RAISES: nothing in this file may drive a
    browser, and a silently-working stub would hide a test that tried.
    """
    stubbed: list[str] = []
    try:
        have_playwright = importlib.util.find_spec("playwright.sync_api") is not None
    except (ImportError, ValueError):
        have_playwright = False
    if not have_playwright:
        def _refuse(*_a, **_kw):  # pragma: no cover - defensive
            raise AssertionError("no test in this suite may start a browser")

        pkg = types.ModuleType("playwright")
        sync_api = types.ModuleType("playwright.sync_api")
        sync_api.sync_playwright = _refuse
        pkg.sync_api = sync_api
        sys.modules["playwright"] = pkg
        sys.modules["playwright.sync_api"] = sync_api
        stubbed = ["playwright.sync_api", "playwright"]
    try:
        spec = importlib.util.spec_from_file_location("nlm_auth", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        # Leave sys.modules as we found it; the module holds its own reference.
        for name in stubbed:
            sys.modules.pop(name, None)


nlm_auth = _load_nlm_auth()

STORED = "xFactor001@opensoft.one"
LEGACY = "brettheap@gmail.com"


class FakePage:
    """The only page surface the harness touches on the selection path."""

    def __init__(self, url: str):
        self.url = url
        self.goto_calls: list[str] = []

    def goto(self, url: str, **_kw) -> None:
        self.goto_calls.append(url)
        self.url = url


class FakeContext:
    def __init__(self, urls: list[str]):
        self.pages = [FakePage(u) for u in urls]
        self.new_pages = 0

    def new_page(self) -> FakePage:
        self.new_pages += 1
        page = FakePage("about:blank")
        self.pages.append(page)
        return page


class MergeCarriesIdentityForward(unittest.TestCase):
    """#543: a refresh must not erase what the store already proves."""

    def merge(self, existing, **kw):
        kw.setdefault("profile", "company")
        kw.setdefault("csrf", "new-csrf")
        kw.setdefault("session", "new-session")
        return nlm_auth.merge_profile_metadata(existing, **kw)

    def test_email_and_build_label_carry_forward_when_the_extraction_has_none(self):
        existing = {
            "csrf_token": "old", "session_id": "old",
            "email": STORED, "build_label": "20260824",
            "last_validated": "2026-08-24T00:00:00",
        }
        metadata, note = self.merge(existing)

        self.assertEqual(metadata["email"], STORED)
        self.assertEqual(metadata["build_label"], "20260824")
        # This extraction owns csrf/session and replaces them.
        self.assertEqual(metadata["csrf_token"], "new-csrf")
        self.assertEqual(metadata["session_id"], "new-session")
        self.assertNotEqual(metadata["last_validated"], "2026-08-24T00:00:00")
        self.assertIn(STORED, note)
        self.assertIn("build_label carried forward", note)

    def test_a_populated_email_is_never_nulled(self):
        for new_value in (None, "", "   "):
            with self.subTest(extracted=repr(new_value)):
                metadata, _ = self.merge({"email": STORED}, email=new_value)
                self.assertEqual(metadata["email"], STORED)

    def test_a_fresh_profile_writes_the_expected_keys(self):
        metadata, note = self.merge({})

        self.assertEqual(
            set(metadata),
            {"csrf_token", "session_id", "email", "build_label", "last_validated"})
        self.assertIsNone(metadata["email"])
        self.assertIsNone(metadata["build_label"])
        self.assertIn("no account address recorded", note)

    def test_other_existing_keys_survive(self):
        existing = {"email": STORED, "provider": "builtin", "quirk": {"a": 1}}
        metadata, _ = self.merge(existing)

        self.assertEqual(metadata["provider"], "builtin")
        self.assertEqual(metadata["quirk"], {"a": 1})

    def test_a_captured_address_populates_an_empty_store(self):
        metadata, note = self.merge({}, email=STORED)

        self.assertEqual(metadata["email"], STORED)
        self.assertIn("captured", note)

    def test_a_case_only_difference_keeps_the_stored_spelling(self):
        metadata, note = self.merge({"email": STORED}, email=STORED.lower())

        self.assertEqual(metadata["email"], STORED)
        self.assertIn("matches the stored address", note)

    def test_a_different_account_refuses(self):
        with self.assertRaises(nlm_auth.AccountMismatch) as caught:
            self.merge({"email": STORED}, email=LEGACY)

        self.assertEqual(caught.exception.stored, STORED)
        self.assertEqual(caught.exception.captured, LEGACY)
        self.assertEqual(caught.exception.profile, "company")

    def test_force_overwrites_the_recorded_account(self):
        metadata, note = self.merge({"email": STORED}, email=LEGACY, force=True)

        self.assertEqual(metadata["email"], LEGACY)
        self.assertIn("--force", note)


class WriteNativeProfile(unittest.TestCase):
    """The on-disk half: merge, permissions, and refuse-before-write."""

    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name)
        self.pdir = self.store / "profiles" / "company"

    def seed(self, metadata: dict, cookies: str = "[]") -> None:
        self.pdir.mkdir(parents=True)
        (self.pdir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
        (self.pdir / "cookies.json").write_text(cookies, encoding="utf-8")

    def written(self) -> dict:
        return json.loads((self.pdir / "metadata.json").read_text(encoding="utf-8"))

    def test_a_refresh_preserves_the_hand_set_address(self):
        self.seed({"csrf_token": "old", "session_id": "old", "email": STORED,
                   "build_label": None, "last_validated": "2026-08-24T00:00:00"})

        pdir, note = nlm_auth.write_native_profile(
            "company", [{"name": "SID", "value": "x"}], "csrf", "session",
            store=self.store)

        self.assertEqual(pdir, self.pdir)
        self.assertEqual(self.written()["email"], STORED)
        self.assertEqual(self.written()["csrf_token"], "csrf")
        self.assertIn(STORED, note)

    def test_a_fresh_profile_is_created_with_restrictive_permissions(self):
        nlm_auth.write_native_profile("company", [], "csrf", "session",
                                      store=self.store)

        self.assertEqual(self.written()["email"], None)
        self.assertEqual((self.pdir / "metadata.json").stat().st_mode & 0o777, 0o600)
        self.assertEqual((self.pdir / "cookies.json").stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.pdir.stat().st_mode & 0o777, 0o700)

    def test_unreadable_metadata_does_not_abort_the_write(self):
        self.pdir.mkdir(parents=True)
        (self.pdir / "metadata.json").write_text("{not json", encoding="utf-8")

        nlm_auth.write_native_profile("company", [], "csrf", "session",
                                      store=self.store)

        self.assertEqual(self.written()["csrf_token"], "csrf")

    def test_a_wrong_account_capture_writes_NOTHING(self):
        self.seed({"email": STORED, "csrf_token": "old", "session_id": "old"},
                  cookies='["original"]')

        with self.assertRaises(nlm_auth.AccountMismatch):
            nlm_auth.write_native_profile(
                "company", [{"name": "SID", "value": "wrong-account"}],
                "csrf", "session", email=LEGACY, store=self.store)

        # Cookies are written BEFORE metadata in the happy path, so the guard
        # has to run first or a wrong-account capture lands half of itself.
        self.assertEqual(self.written()["email"], STORED)
        self.assertEqual(self.written()["csrf_token"], "old")
        self.assertEqual((self.pdir / "cookies.json").read_text(encoding="utf-8"),
                         '["original"]')

    def test_the_store_root_falls_back_to_the_env_var(self):
        with unittest.mock.patch.dict(
                "os.environ", {"NOTEBOOKLM_MCP_CLI_PATH": str(self.store)}):
            self.assertEqual(nlm_auth.profile_dir("company"), self.pdir)


class PageSelection(unittest.TestCase):
    """#537 harness half: both hosts count as NotebookLM."""

    def test_a_new_host_tab_is_selected(self):
        ctx = FakeContext(["https://mail.google.com/",
                           "https://notebook.google.com/notebook/abc"])

        page, how = nlm_auth.select_notebooklm_page(ctx)

        self.assertEqual(how, "existing")
        self.assertEqual(page, ctx.pages[1])
        self.assertEqual(ctx.new_pages, 0)
        self.assertEqual(page.goto_calls, [])

    def test_an_old_host_tab_is_still_selected(self):
        ctx = FakeContext(["https://notebooklm.google.com/"])

        page, how = nlm_auth.select_notebooklm_page(ctx)

        self.assertEqual(how, "existing")
        self.assertEqual(page, ctx.pages[0])

    def test_no_notebooklm_tab_opens_a_new_one_and_hijacks_nothing(self):
        ctx = FakeContext(["https://docs.google.com/document/d/keep-me"])
        first = ctx.pages[0]

        page, how = nlm_auth.select_notebooklm_page(ctx)

        self.assertEqual(how, "new")
        self.assertEqual(ctx.new_pages, 1)
        self.assertIsNot(page, first)
        self.assertEqual(first.url, "https://docs.google.com/document/d/keep-me")
        self.assertEqual(first.goto_calls, [])

    def test_an_empty_browser_opens_a_tab(self):
        ctx = FakeContext([])

        _page, how = nlm_auth.select_notebooklm_page(ctx)

        self.assertEqual(how, "new")
        self.assertEqual(ctx.new_pages, 1)

    def test_the_predicate_matches_on_host_not_substring(self):
        self.assertTrue(nlm_auth.is_notebooklm_url("https://notebook.google.com/x"))
        self.assertTrue(nlm_auth.is_notebooklm_url("https://notebooklm.google.com/"))
        self.assertFalse(
            nlm_auth.is_notebooklm_url("https://evil.example/?q=notebook.google.com"))
        self.assertFalse(nlm_auth.is_notebooklm_url("https://mail.google.com/"))
        self.assertFalse(nlm_auth.is_notebooklm_url(""))
        self.assertFalse(nlm_auth.is_notebooklm_url(None))

    def test_NB_URL_stays_on_the_host_the_evidence_covers(self):
        # Deliberate, and documented beside the constant: no recorded run has
        # navigated DIRECTLY to the new host, and this cannot be tested without
        # a live signed-in browser. Flip it only with such a run behind it.
        self.assertEqual(nlm_auth.NB_URL, "https://notebooklm.google.com/")
        self.assertEqual(set(nlm_auth.NB_HOSTS),
                         {"notebook.google.com", "notebooklm.google.com"})


class ExtractAndSave(unittest.TestCase):
    """The wiring: capture -> merge -> refuse, with `verify()` never run."""

    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Path(self.tmp.name)
        self.pdir = self.store / "profiles" / "company"
        self.pdir.mkdir(parents=True)
        (self.pdir / "metadata.json").write_text(
            json.dumps({"email": STORED, "csrf_token": "old", "session_id": "old"}),
            encoding="utf-8")

    def run_extract(self, captured_email, force=False):
        cookies = [{"name": n, "value": "v", "domain": ".google.com"}
                   for n in nlm_auth.REQUIRED]
        ctx = types.SimpleNamespace(cookies=lambda: cookies)
        page = types.SimpleNamespace(content=lambda: "<html>page</html>")
        # `verify()` shells out to the real `nlm`, which the suite's hermeticity
        # guard refuses; it is out of scope here and is stubbed to a fixed code.
        with unittest.mock.patch.object(nlm_auth, "verify", return_value=0):
            return nlm_auth.extract_and_save(
                ctx, page, "company", 1,
                lambda _html: "csrf", lambda _html: "session",
                lambda _html: captured_email, force=force, store=self.store)

    def metadata(self) -> dict:
        return json.loads((self.pdir / "metadata.json").read_text(encoding="utf-8"))

    def test_the_right_account_is_confirmed_and_the_address_kept(self):
        self.assertEqual(self.run_extract(STORED), 0)
        self.assertEqual(self.metadata()["email"], STORED)
        self.assertEqual(self.metadata()["csrf_token"], "csrf")

    def test_no_capture_still_carries_the_address_forward(self):
        self.assertEqual(self.run_extract(""), 0)
        self.assertEqual(self.metadata()["email"], STORED)

    def test_a_wrong_account_exits_non_zero_and_writes_nothing(self):
        self.assertNotEqual(self.run_extract(LEGACY), 0)
        self.assertEqual(self.metadata()["email"], STORED)
        self.assertEqual(self.metadata()["csrf_token"], "old")
        self.assertFalse((self.pdir / "cookies.json").exists())

    def test_force_records_the_captured_account(self):
        self.assertEqual(self.run_extract(LEGACY, force=True), 0)
        self.assertEqual(self.metadata()["email"], LEGACY)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
