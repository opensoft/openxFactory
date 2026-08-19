#!/usr/bin/env python3
"""nlm auth via a Playwright-driven persistent Chromium profile under WSLg.

Why this exists: `nlm login --wsl` drives WINDOWS Chrome and reads cookies over
a TCP CDP port that WSL's firewall blocks — the wall that cost hours. Playwright
launches Chromium INSIDE WSL under WSLg and controls it over a stdio pipe: no
TCP, no firewall, no Windows Chrome. A PERSISTENT profile means the Google login
form is seen ONCE; every later run reuses the logged-in session (bootstrap =
attended once, refresh = unattended forever after).

Modes:
  bootstrap  headed window; a human signs in once as the target account, then
             this harvests cookies into the nlm profile store.
  refresh    reuse the persistent profile (already signed in); harvest cookies
             with no human. This is xFactory's "log in whenever it wants".

It never writes the nlm store directly — it hands cookies to `nlm login --manual`
so the CLI's own save_profile does the writing (format, 0600, metadata, mismatch
guard).
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, tempfile, time
from pathlib import Path

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", os.path.expanduser("~/.cache/ms-playwright"))
from playwright.sync_api import sync_playwright

REQUIRED = {"SID", "HSID", "SSID", "APISID", "SAPISID"}
NB_URL = "https://notebooklm.google.com/"
DEFAULT_PROFILE_DIR = os.path.expanduser("~/.notebooklm-mcp-cli/xf-auth-chrome-profile")


def google_cookies(ctx) -> dict[str, str]:
    out = {}
    for c in ctx.cookies():
        if c.get("domain", "").endswith("google.com"):
            out[c["name"]] = c["value"]
    return out


def harvest(ctx, wait_s: int) -> dict[str, str]:
    """Poll until the five required cookies are present, or time out."""
    deadline = time.time() + wait_s
    last = 0
    while time.time() < deadline:
        ck = google_cookies(ctx)
        have = REQUIRED & set(ck)
        if len(have) != last:
            print(f"[nlm-auth] cookies present: {sorted(have)} ({len(have)}/5)", flush=True)
            last = len(have)
        if REQUIRED <= set(ck):
            return ck
        time.sleep(3)
    return google_cookies(ctx)


def import_into_nlm(cookies: dict[str, str], profile: str) -> int:
    fd, path = tempfile.mkstemp(suffix=".json", prefix="nlm-ck-")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(cookies, f)
        os.chmod(path, 0o600)
        r = subprocess.run(["nlm", "login", "--manual", "-f", path, "--profile", profile],
                           capture_output=True, text=True)
        sys.stdout.write(r.stdout); sys.stderr.write(r.stderr)
        return r.returncode
    finally:
        try: os.remove(path)
        except OSError: pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["bootstrap", "refresh"])
    ap.add_argument("--profile", default="opensoft-bot", help="target nlm profile name")
    ap.add_argument("--profile-dir", default=DEFAULT_PROFILE_DIR, help="persistent Chrome profile dir")
    ap.add_argument("--wait", type=int, default=600, help="bootstrap: seconds to wait for sign-in")
    ap.add_argument("--channel", default="chrome",
                    help="browser channel: 'chrome' = system Google Chrome (renders under WSLg); "
                         "'' or 'bundled' = Playwright's bundled Chromium (did NOT render under this WSLg)")
    args = ap.parse_args()

    Path(args.profile_dir).mkdir(parents=True, exist_ok=True)
    headed = args.mode == "bootstrap"
    launch_kwargs = dict(
        headless=not headed,
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
    )
    if args.channel and args.channel != "bundled":
        launch_kwargs["channel"] = args.channel
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(args.profile_dir, **launch_kwargs)
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.goto(NB_URL, wait_until="domcontentloaded", timeout=60000)
        if args.mode == "bootstrap":
            print("[nlm-auth] A browser window is open. Sign in as the TARGET account "
                  "and open NotebookLM. Waiting for the session (up to "
                  f"{args.wait}s)...", flush=True)
            cookies = harvest(ctx, args.wait)
        else:
            cookies = harvest(ctx, 30)
        ctx.close()

    have = REQUIRED & set(cookies)
    if REQUIRED > set(cookies):
        print(f"[nlm-auth] INCOMPLETE: only {sorted(have)} present; not importing. "
              "In bootstrap, finish signing in; in refresh, the persistent profile "
              "is no longer logged in — re-run bootstrap.", file=sys.stderr)
        return 3
    print(f"[nlm-auth] all 5 required cookies captured ({len(cookies)} total); "
          f"importing into nlm profile '{args.profile}'", flush=True)
    return import_into_nlm(cookies, args.profile)


if __name__ == "__main__":
    raise SystemExit(main())
