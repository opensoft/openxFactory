#!/usr/bin/env python3
"""nlm auth via FULL CDP/Playwright extraction of a live NotebookLM session.

WHAT WORKS (proven 2026-08-19). A headed Google Chrome is driven under WSLg on a
localhost remote-debugging port (or launched by Playwright as a persistent
profile). Because the debug port is on 127.0.0.1 *inside* WSL, no Windows
firewall is involved — that firewall is exactly what blocked `nlm login --wsl`,
which drives WINDOWS Chrome over a TCP CDP port. A human signs into the books
account once and opens https://notebooklm.google.com/ (note: notebookLM, with
the L-M — a wrong host such as notebook.google.com makes extraction time out).
This harness then extracts the FULL native nlm profile:

    * the cookie LIST  (every google.com cookie, as full cookie dicts)
    * csrf_token       (scraped from the logged-in page HTML)
    * session_id       (scraped from the logged-in page HTML)

All three are required. `nlm notebook list` succeeds only when all three are
present in the native profile store.

WHAT DOES NOT WORK — and why this replaced it. The previous harness harvested
cookies only and handed them to `nlm login --manual`. That path is INSUFFICIENT:
`--manual` stored the cookies as a {name: value} DICT (the native store expects a
cookie LIST of full dicts) and left csrf_token / session_id NULL. The import
reported success, yet `nlm notebook list` returned "Authentication expired"
because csrf/session were missing and the cookie shape was wrong. Cookies alone
are not a working NotebookLM session — do not reintroduce the `--manual` path.

Modes:
  bootstrap  headed window; a human signs in once as the target account and
             opens NotebookLM, then this extracts the full profile.
  refresh    reuse the signed-in persistent profile (or an already-open browser
             over --cdp-url); extract the full profile with no human. This is
             xFactory's "log in whenever it wants" property.

Two ways to reach a logged-in browser (either produces the same full profile):
  --cdp-url http://127.0.0.1:9444   connect to an already-running headed Chrome
                                    that a human signed in (no re-login), OR
  (default)                         launch a persistent Chrome profile so the
                                    login form is seen once and reused after.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time
from datetime import datetime
from pathlib import Path

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", os.path.expanduser("~/.cache/ms-playwright"))
from playwright.sync_api import sync_playwright

REQUIRED = {"SID", "HSID", "SSID", "APISID", "SAPISID"}
NB_URL = "https://notebooklm.google.com/"
DEFAULT_PROFILE_DIR = os.path.expanduser("~/.notebooklm-mcp-cli/xf-auth-chrome-profile")
NLM_STORE = os.path.expanduser("~/.notebooklm-mcp-cli")

# Common install locations for the nlm CLI's site-packages (holds
# notebooklm_tools). Override with --cli-site-packages if yours differs.
_CLI_SITE_PACKAGES_HINTS = [
    "~/.local/share/uv/tools/notebooklm-mcp-cli/lib/python3.12/site-packages",
    "~/.local/share/uv/tools/notebooklm-mcp-cli/lib/python3.11/site-packages",
    "~/.local/share/uv/tools/notebooklm-mcp-cli/lib/python3.13/site-packages",
]


def _load_cli_extractors(extra_hint: str | None):
    """Import the CLI's csrf/session extractors. Degrade gracefully if absent.

    Returns (extract_csrf, extract_session) or (None, None). Without these,
    csrf_token/session_id cannot be scraped and the profile would be
    INCOMPLETE (the very defect this harness exists to avoid), so a hard warning
    is printed and extraction should be treated as unusable.
    """
    hints = ([extra_hint] if extra_hint else []) + _CLI_SITE_PACKAGES_HINTS
    for h in hints:
        p = os.path.expanduser(h)
        if os.path.isdir(os.path.join(p, "notebooklm_tools")):
            if p not in sys.path:
                sys.path.insert(0, p)
            break
    try:
        from notebooklm_tools.core.auth import (  # type: ignore
            extract_csrf_from_page_source,
            extract_session_id_from_page,
        )
        return extract_csrf_from_page_source, extract_session_id_from_page
    except Exception as e:  # pragma: no cover - environment-dependent
        print(f"[nlm-auth] WARNING: could not import notebooklm_tools extractors "
              f"({e}). csrf_token/session_id cannot be scraped, so the resulting "
              f"profile would be INCOMPLETE. Pass --cli-site-packages <dir>.",
              file=sys.stderr)
        return None, None


def google_cookies_list(ctx) -> list[dict]:
    """The cookie LIST (full cookie dicts), not a {name: value} dict.

    The native nlm store expects the list form; the {name: value} dict written
    by `nlm login --manual` is the wrong shape and does not authenticate.
    """
    return [c for c in ctx.cookies() if c.get("domain", "").endswith("google.com")]


def present_names(cookies: list[dict]) -> set[str]:
    return {c.get("name", "") for c in cookies}


def harvest_list(ctx, wait_s: int) -> list[dict]:
    """Poll until the five required session cookies are present, or time out."""
    deadline = time.time() + wait_s
    last = -1
    while time.time() < deadline:
        cookies = google_cookies_list(ctx)
        have = REQUIRED & present_names(cookies)
        if len(have) != last:
            print(f"[nlm-auth] session cookies present: {sorted(have)} ({len(have)}/5)", flush=True)
            last = len(have)
        if REQUIRED <= present_names(cookies):
            return cookies
        time.sleep(3)
    return google_cookies_list(ctx)


def write_native_profile(profile: str, cookies: list[dict],
                         csrf: str | None, session: str | None) -> Path:
    """Write the FULL native profile: cookies.json (LIST) + metadata.json.

    Mirrors AuthManager.save_profile: cookies.json is the cookie list, and
    metadata.json carries csrf_token/session_id/email/build_label/last_validated.
    email and build_label are left null (the books account's stored email is
    null; it is identified by the books it shows, not by name).
    """
    base = os.environ.get("NOTEBOOKLM_MCP_CLI_PATH", NLM_STORE)
    pdir = Path(os.path.expanduser(base)) / "profiles" / profile
    pdir.mkdir(parents=True, exist_ok=True)
    pdir.chmod(0o700)

    cookies_file = pdir / "cookies.json"
    cookies_file.write_text(json.dumps(cookies, indent=2, ensure_ascii=False), encoding="utf-8")
    cookies_file.chmod(0o600)

    metadata = {
        "csrf_token": csrf,
        "session_id": session,
        "email": None,
        "build_label": None,
        "last_validated": datetime.now().isoformat(),
    }
    meta_file = pdir / "metadata.json"
    meta_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    meta_file.chmod(0o600)
    return pdir


def extract_and_save(ctx, page, profile: str, wait_s: int,
                     extract_csrf, extract_session) -> int:
    """Harvest the full session and write the native profile. Returns exit code."""
    cookies = harvest_list(ctx, wait_s)
    have = REQUIRED & present_names(cookies)
    if not (REQUIRED <= present_names(cookies)):
        print(f"[nlm-auth] INCOMPLETE: only {sorted(have)} of 5 session cookies present; "
              "not writing. In bootstrap, finish signing in and open NotebookLM; in "
              "refresh, the persistent profile is no longer logged in — re-run bootstrap.",
              file=sys.stderr)
        return 3

    # Scrape csrf/session from the logged-in NotebookLM page HTML.
    csrf = session = None
    try:
        html = page.content()
    except Exception as e:
        print(f"[nlm-auth] WARNING: could not read page HTML for csrf/session ({e}).",
              file=sys.stderr)
        html = ""
    if extract_csrf and extract_session and html:
        csrf = extract_csrf(html)
        session = extract_session(html)

    if not csrf or not session:
        print("[nlm-auth] ERROR: csrf_token and/or session_id could not be extracted. "
              "A cookies-only profile does NOT authenticate (this is exactly the failure "
              "the old --manual path hit). Ensure the browser is ON "
              "https://notebooklm.google.com/ (L-M) and signed in, and that the CLI "
              "extractors are importable (--cli-site-packages).", file=sys.stderr)
        return 4

    pdir = write_native_profile(profile, cookies, csrf, session)
    print(f"[nlm-auth] wrote full profile '{profile}' ({len(cookies)} cookies, "
          f"csrf+session captured) -> {pdir}", flush=True)
    return verify(profile)


def verify(profile: str) -> int:
    """Verify the profile with a REAL call (`nlm notebook list`), not login --check."""
    print(f"[nlm-auth] verifying with `nlm notebook list --profile {profile}`...", flush=True)
    r = subprocess.run(["nlm", "notebook", "list", "--profile", profile],
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode == 0:
        print("[nlm-auth] OK: authentication is live.", flush=True)
    else:
        print("[nlm-auth] verification FAILED — profile not usable.", file=sys.stderr)
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["bootstrap", "refresh"])
    ap.add_argument("--profile", default="personal", help="target nlm profile name")
    ap.add_argument("--profile-dir", default=DEFAULT_PROFILE_DIR,
                    help="persistent Chrome profile dir (launch path)")
    ap.add_argument("--cdp-url", default=None,
                    help="connect to an already-running headed Chrome over CDP "
                         "(e.g. http://127.0.0.1:9444) instead of launching one; "
                         "the human is already signed in — no re-login")
    ap.add_argument("--wait", type=int, default=600,
                    help="bootstrap: seconds to wait for sign-in")
    ap.add_argument("--channel", default="chrome",
                    help="browser channel for the launch path: 'chrome' = system "
                         "Google Chrome (renders under WSLg); '' or 'bundled' = "
                         "Playwright's bundled Chromium (did NOT render under this WSLg)")
    ap.add_argument("--cli-site-packages", default=None,
                    help="dir containing notebooklm_tools (for the csrf/session extractors)")
    args = ap.parse_args()

    extract_csrf, extract_session = _load_cli_extractors(args.cli_site_packages)
    wait_s = args.wait if args.mode == "bootstrap" else 30

    with sync_playwright() as p:
        if args.cdp_url:
            # Connect to an already-signed-in browser. No navigation/re-login.
            browser = p.chromium.connect_over_cdp(args.cdp_url)
            ctx = browser.contexts[0] if browser.contexts else browser.new_context()
            page = next((pg for pg in ctx.pages if "notebooklm.google.com" in pg.url), None)
            if page is None:
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                page.goto(NB_URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(6)
            rc = extract_and_save(ctx, page, args.profile, wait_s, extract_csrf, extract_session)
            # Do not close a browser we did not launch.
            return rc

        # Launch path: persistent profile, headed for bootstrap.
        Path(args.profile_dir).mkdir(parents=True, exist_ok=True)
        headed = args.mode == "bootstrap"
        launch_kwargs = dict(
            headless=not headed,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
        )
        if args.channel and args.channel != "bundled":
            launch_kwargs["channel"] = args.channel
        ctx = p.chromium.launch_persistent_context(args.profile_dir, **launch_kwargs)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(NB_URL, wait_until="domcontentloaded", timeout=60000)
        if args.mode == "bootstrap":
            print("[nlm-auth] A browser window is open. Sign in as the TARGET (books) "
                  "account and open NotebookLM (notebooklm.google.com, L-M). Waiting for "
                  f"the session (up to {wait_s}s)...", flush=True)
        time.sleep(6)
        rc = extract_and_save(ctx, page, args.profile, wait_s, extract_csrf, extract_session)
        ctx.close()
        return rc


if __name__ == "__main__":
    raise SystemExit(main())
