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
import sys
import types
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

from notebooklm_sync.nlm_client import JsonValue

from tests.notebooklm._sync_test_support import TestSupportError, load_script_module

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "nlm_auth.py"


class SyncAPIStub(types.ModuleType):
    def __init__(self, name: str, refuse: Callable[[], None]) -> None:
        super().__init__(name)
        self.sync_playwright: Callable[[], None] = refuse


class PlaywrightStub(types.ModuleType):
    def __init__(self, name: str, api: SyncAPIStub) -> None:
        super().__init__(name)
        self.sync_api: SyncAPIStub = api


class CookieContext(Protocol):
    def cookies(self) -> Sequence[Mapping[str, str]]: ...


class HtmlPage(Protocol):
    def content(self) -> str: ...


@dataclass(frozen=True, slots=True)
class ExtractionContext:
    cookies: Callable[[], list[dict[str, str]]]


@dataclass(frozen=True, slots=True)
class ExtractionPage:
    content: Callable[[], str]


@runtime_checkable
class AccountMismatchDetails(Protocol):
    stored: str
    captured: str
    profile: str


@runtime_checkable
class AuthModule(Protocol):
    NB_URL: str
    NB_HOSTS: tuple[str, ...]
    REQUIRED: frozenset[str]
    AccountMismatch: type[Exception]
    verify: Callable[[str], int]

    def merge_profile_metadata(
        self,
        existing: Mapping[str, JsonValue],
        *,
        profile: str,
        csrf: str | None,
        session: str | None,
        email: str | None = None,
        build_label: str | None = None,
        force: bool = False,
    ) -> tuple[dict[str, JsonValue], str]: ...
    def write_native_profile(
        self,
        profile: str,
        cookies: Sequence[Mapping[str, JsonValue]],
        csrf: str | None,
        session: str | None,
        *,
        email: str | None = None,
        build_label: str | None = None,
        force: bool = False,
        store: Path | None = None,
    ) -> tuple[Path, str]: ...
    def profile_dir(self, profile: str, store: Path | None = None) -> Path: ...
    def is_notebooklm_url(self, url: str | None) -> bool: ...
    def select_notebooklm_page(self, ctx: FakeContext) -> tuple[FakePage, str]: ...
    def extract_and_save(
        self,
        ctx: CookieContext,
        page: HtmlPage,
        profile: str,
        wait_s: int,
        extract_csrf: Callable[[str], str | None],
        extract_session: Callable[[str], str | None],
        extract_email: Callable[[str], str | None],
        *,
        force: bool = False,
        store: Path | None = None,
    ) -> int: ...


def _load_nlm_auth() -> AuthModule:
    """Import the harness by path, stubbing playwright only if it is absent.

    The stub's `sync_playwright` RAISES: nothing in this file may drive a
    browser, and a silently-working stub would hide a test that tried.

    sys.modules is left EXACTLY as it was found — whatever was under those two
    names (a real package, or another module's own stub) is saved and restored,
    not popped — because this runs at import time inside a shared interpreter.
    """
    names = ("playwright", "playwright.sync_api")
    try:
        have_playwright = importlib.util.find_spec("playwright.sync_api") is not None
    except (ImportError, ValueError):
        have_playwright = False
    saved = {n: sys.modules[n] for n in names if n in sys.modules}
    injected: tuple[str, ...] = ()
    if not have_playwright:

        def _refuse() -> None:
            raise AssertionError("no test in this suite may start a browser")

        sync_api = SyncAPIStub("playwright.sync_api", _refuse)
        pkg = PlaywrightStub("playwright", sync_api)
        sys.modules["playwright"], sys.modules["playwright.sync_api"] = (pkg, sync_api)
        injected = names
    try:
        module = load_script_module("nlm_auth", SCRIPT)
        if not isinstance(module, AuthModule):
            raise TestSupportError("auth harness lacks its declared test contract")
        return module
    finally:
        for name in injected:
            if name in saved:
                sys.modules[name] = saved[name]
            else:
                _ = sys.modules.pop(name, None)


nlm_auth = _load_nlm_auth()
STORED = "projection-host@example.invalid"
LEGACY = "previous-host@example.invalid"


class FakePage:
    """The only page surface the harness touches on the selection path."""

    def __init__(self, url: str):
        self.url: str = url
        self.goto_calls: list[str] = []

    def goto(self, url: str, **_kw: str | int) -> None:
        self.goto_calls.append(url)
        self.url = url


class FakeContext:
    def __init__(self, urls: list[str]):
        self.pages: list[FakePage] = [FakePage(u) for u in urls]
        self.new_pages: int = 0

    def new_page(self) -> FakePage:
        self.new_pages += 1
        page = FakePage("about:blank")
        self.pages.append(page)
        return page
