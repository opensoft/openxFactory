#!/usr/bin/env python3
"""nlm auth via FULL CDP/Playwright extraction of a live NotebookLM session.

WHAT WORKS (proven 2026-08-19). A headed Google Chrome is driven under WSLg on a
localhost remote-debugging port (or launched by Playwright as a persistent
profile). Because the debug port is on 127.0.0.1 *inside* WSL, no Windows
firewall is involved — that firewall is exactly what blocked `nlm login --wsl`,
which drives WINDOWS Chrome over a TCP CDP port. A human signs into the books
account once and opens NotebookLM on EITHER of its two hosts — the live one
since the provider's rebrand is `notebook.google.com` ("Gemini Notebook"), and
the older `notebooklm.google.com` (L-M) redirects there. This harness then
extracts the FULL native nlm profile:

    * the cookie LIST  (every google.com cookie, as full cookie dicts)
    * csrf_token       (scraped from the logged-in page HTML)
    * session_id       (scraped from the logged-in page HTML)
    * email            (the signed-in address, scraped from the same HTML by
                        the CLI's own extractor when it is importable)

The first three are required. `nlm notebook list` succeeds only when all three
are present in the native profile store. The address is what proves WHICH
account was captured, and the sync's hosting enforcement reads it
(`profile_account()` / `enforce_hosting_profile()` in
`scripts/sync-notebooklm-books.py`) — so this harness MERGES metadata rather
than replacing it, and never nulls a populated address (opensoft/openxFactory#543).

HOSTS. Both spellings name the same app and both are accepted here: the
`--cdp-url` page predicate prefers an already-open NotebookLM tab on EITHER
host rather than hijacking an unrelated one (opensoft/openxFactory#537).
`NB_URL` deliberately stays on the OLD host — see the note beside it.

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
from urllib.parse import urlparse

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", os.path.expanduser("~/.cache/ms-playwright"))
from playwright.sync_api import sync_playwright

REQUIRED = {"SID", "HSID", "SSID", "APISID", "SAPISID"}

# BOTH hosts serve the same app. `notebook.google.com` is the live one since the
# provider's rebrand; `notebooklm.google.com` (L-M) redirects to it. A page on
# either is a NotebookLM page for this harness's purposes.
NB_HOSTS = ("notebook.google.com", "notebooklm.google.com")

# NB_URL STAYS ON THE OLD HOST, DELIBERATELY — and this harness therefore
# depends on the provider's redirect. The evidence, such as it is:
#   * The module docstring used to claim "a wrong host such as
#     notebook.google.com makes extraction time out". That claim entered in
#     `fa5ee9f3` (2026-08-19), the commit that rewrote this docstring wholesale;
#     it is the ONLY commit in this file's history that mentions the new host
#     (`git log -S"notebook.google.com" -- scripts/nlm_auth.py`), and it carries
#     no run, test or record behind it. The timeout it describes is `nlm
#     login`'s 300 s "Login timeout", which comes from the CLI's
#     `_is_notebooklm_url()` allow-list (F1 in
#     docs/notebook-projection-migration-evidence-2026-08-24.md) and says
#     nothing about THIS harness, which never inspects the host.
#   * The 2026-08-24 migration authenticated through this harness against a
#     browser signed in on the NEW host: the predicate missed, a tab was
#     navigated to NB_URL, the provider redirected it to
#     `notebook.google.com`, and extraction succeeded on that page. So
#     extraction demonstrably works on the new host once the redirect lands.
# What is NOT evidenced is navigating DIRECTLY to `https://notebook.google.com/`,
# which no recorded run has done. Flipping this constant cannot be tested
# without a live signed-in browser, so it is left alone rather than changed on
# speculation. Flip it only with a recorded bootstrap+refresh run behind it.
NB_URL = "https://notebooklm.google.com/"
DEFAULT_PROFILE_DIR = os.path.expanduser("~/.notebooklm-mcp-cli/xf-auth-chrome-profile")
NLM_STORE = os.path.expanduser("~/.notebooklm-mcp-cli")


class AccountMismatch(RuntimeError):
    """The live session is a DIFFERENT account than the profile store records.

    Mirrors `notebooklm_tools`' own `AccountMismatchError`, raised by
    `AuthManager.save_profile()` unless `force=True` — the guard this harness
    bypasses by writing the store directly (opensoft/openxFactory#543).
    """

    def __init__(self, stored: str, captured: str, profile: str):
        self.stored, self.captured, self.profile = stored, captured, profile
        super().__init__(
            f"profile {profile!r} records {stored!r} but the live session is "
            f"{captured!r}")

# Common install locations for the nlm CLI's site-packages (holds
# notebooklm_tools). Override with --cli-site-packages if yours differs.
_CLI_SITE_PACKAGES_HINTS = [
    "~/.local/share/uv/tools/notebooklm-mcp-cli/lib/python3.12/site-packages",
    "~/.local/share/uv/tools/notebooklm-mcp-cli/lib/python3.11/site-packages",
    "~/.local/share/uv/tools/notebooklm-mcp-cli/lib/python3.13/site-packages",
]


def _ensure_cli_on_path(extra_hint: str | None) -> None:
    """Put the nlm CLI's site-packages on sys.path so notebooklm_tools imports."""
    hints = ([extra_hint] if extra_hint else []) + _CLI_SITE_PACKAGES_HINTS
    for h in hints:
        p = os.path.expanduser(h)
        if os.path.isdir(os.path.join(p, "notebooklm_tools")):
            if p not in sys.path:
                sys.path.insert(0, p)
            break


def _load_cli_extractors(extra_hint: str | None):
    """Import the CLI's csrf/session extractors. Degrade gracefully if absent.

    Returns (extract_csrf, extract_session) or (None, None). Without these,
    csrf_token/session_id cannot be scraped and the profile would be
    INCOMPLETE (the very defect this harness exists to avoid), so a hard warning
    is printed and extraction should be treated as unusable.
    """
    _ensure_cli_on_path(extra_hint)
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


def _load_email_extractor(extra_hint: str | None):
    """Import the CLI's own signed-in-address extractor, or None if absent.

    `notebooklm_tools.utils.cdp.extract_email(html)` is the function `nlm login`
    itself uses to fill the `email` field of exactly this metadata file, and it
    reads the SAME page HTML this harness already fetches for csrf/session — so
    capturing the address costs one extra call on a page we have in hand, and no
    new mechanism is invented here.

    Absence is not fatal: without it the address is CARRIED FORWARD from the
    existing profile rather than captured (which is the #543 fix's floor).
    """
    _ensure_cli_on_path(extra_hint)
    try:
        from notebooklm_tools.utils.cdp import extract_email  # type: ignore
        return extract_email
    except Exception as e:  # pragma: no cover - environment-dependent
        print(f"[nlm-auth] note: the CLI's email extractor is unavailable ({e}); "
              f"the signed-in address cannot be captured, so any stored address "
              f"is carried forward unverified.", file=sys.stderr)
        return None


def is_notebooklm_url(url: str | None) -> bool:
    """True for a NotebookLM page on EITHER host (rebrand-tolerant).

    Matched on the parsed hostname rather than as a substring, so a URL that
    merely mentions the host somewhere in a query string does not qualify.
    """
    try:
        host = (urlparse(url or "").hostname or "").lower()
    except ValueError:
        return False
    return host in NB_HOSTS


def select_notebooklm_page(ctx):
    """Pick the tab holding the live NotebookLM session; returns (page, how).

    `how` is "existing" when an already-open NotebookLM tab was reused (on
    either host) and "new" when none existed and a NEW tab was opened for the
    caller to navigate.

    Before opensoft/openxFactory#537 this matched only `notebooklm.google.com`,
    so after the rebrand it matched NOTHING: the code fell through to
    `ctx.pages[0]` and navigated whatever tab the human happened to have first
    to `NB_URL`. That worked only because the provider redirects. A new tab is
    opened instead of hijacking an unrelated one — this browser belongs to the
    operator, not to the harness.
    """
    page = next((pg for pg in ctx.pages if is_notebooklm_url(pg.url)), None)
    if page is not None:
        return page, "existing"
    return ctx.new_page(), "new"


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


def profile_dir(profile: str, store: str | os.PathLike | None = None) -> Path:
    """The native store directory for `profile` (root injectable for tests)."""
    base = store or os.environ.get("NOTEBOOKLM_MCP_CLI_PATH", NLM_STORE)
    return Path(os.path.expanduser(str(base))) / "profiles" / profile


def read_profile_metadata(pdir: Path) -> dict:
    """The existing metadata.json as a dict; {} when absent or unreadable.

    ValueError covers BOTH json.JSONDecodeError (malformed JSON) and
    UnicodeDecodeError (non-UTF-8 bytes) — an unreadable store must degrade to
    "nothing to carry forward", never crash the extraction.
    """
    try:
        data = json.loads((pdir / "metadata.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _clean(value) -> str | None:
    """A non-blank string, or None. Anything else in the store reads as unknown."""
    return value.strip() or None if isinstance(value, str) else None


def merge_profile_metadata(existing: dict, *, profile: str, csrf: str | None,
                           session: str | None, email: str | None = None,
                           build_label: str | None = None,
                           force: bool = False) -> tuple[dict, str]:
    """MERGE this extraction into the stored metadata; never null what it holds.

    Returns (metadata, note) where `note` is a one-line human account of what
    was captured or carried forward. Raises AccountMismatch when a captured
    address contradicts a stored one and `force` is false.

    WHY MERGE (opensoft/openxFactory#543). This harness used to build the dict
    literally with `"email": None, "build_label": None` and overwrite the file,
    on the refresh path as well as bootstrap. That erased an identity the SYNC
    depends on: `enforce_hosting_profile()` treats a null address as UNKNOWN and
    falls back to checking the profile NAME alone, which cannot tell one Google
    account from another — so a refresh silently disarmed the check that exists
    to stop a governed projection being written into the wrong estate. The old
    rationale ("the books account's stored email is null; it is identified by
    the books it shows, not by name") described the LEGACY personal account and
    has been false since 2026-08-24: the `company` profile records
    `xFactor001@opensoft.one`, set from the vault-held username precisely so the
    sync could check it.

    So: this extraction owns csrf_token, session_id and last_validated and
    overwrites them; `email` and `build_label` are carried forward whenever the
    extraction has no value for them; and every OTHER key the store already
    holds survives untouched, because this function does not know what the CLI
    may add to that file next.

    Address comparison is CASE-INSENSITIVE and keeps the STORED spelling on a
    match — `xFactor001@opensoft.one` as recorded from the vault vs a
    lower-cased scrape must not read as two accounts (the sync compares
    case-insensitively too). Upstream's own guard compares exactly; this is a
    deliberate, documented relaxation in the safe direction.
    """
    metadata = dict(existing)
    stored_email = _clean(existing.get("email"))
    captured = _clean(email)
    notes: list[str] = []

    if captured and stored_email and captured.casefold() != stored_email.casefold():
        if not force:
            raise AccountMismatch(stored_email, captured, profile)
        metadata["email"] = captured
        notes.append(f"REPLACED the stored address {stored_email} with the "
                     f"captured {captured} (--force)")
    elif captured and stored_email:
        # Same account: keep the stored spelling rather than the scraped one.
        metadata["email"] = stored_email
        notes.append(f"captured {captured} from the live session; it matches "
                     "the stored address")
    elif captured:
        metadata["email"] = captured
        notes.append(f"captured {captured} from the live session (the store "
                     "recorded none)")
    elif stored_email:
        metadata["email"] = stored_email
        notes.append(f"carried the stored address {stored_email} forward (the "
                     "live session yielded none)")
    else:
        # Keep the KEY (the CLI's own shape has it) but normalise the value to
        # null: a blank or non-string leftover reads as UNKNOWN to the sync
        # anyway, and writing it back would preserve junk as if it meant
        # something.
        metadata["email"] = None
        notes.append("no account address recorded — none stored, none captured; "
                     "the sync will verify this profile by NAME only")

    # Same rule for build_label: carry a real value forward, normalise anything
    # blank or non-string to null rather than round-tripping it.
    metadata["build_label"] = _clean(build_label) or _clean(existing.get("build_label"))
    if not _clean(build_label) and metadata["build_label"]:
        notes.append("build_label carried forward")

    metadata["csrf_token"] = csrf
    metadata["session_id"] = session
    metadata["last_validated"] = datetime.now().isoformat()
    return metadata, "; ".join(notes)


def write_native_profile(profile: str, cookies: list[dict],
                         csrf: str | None, session: str | None, *,
                         email: str | None = None,
                         build_label: str | None = None,
                         force: bool = False,
                         store: str | os.PathLike | None = None) -> tuple[Path, str]:
    """Write the FULL native profile: cookies.json (LIST) + metadata.json.

    Mirrors AuthManager.save_profile: cookies.json is the cookie list, and
    metadata.json carries csrf_token/session_id/email/build_label/last_validated.
    Metadata is MERGED into whatever the store already holds — see
    `merge_profile_metadata()` for why nulling `email` is a defect and not a
    default.

    The merge (and therefore the account-mismatch refusal) runs BEFORE anything
    is written, so a wrong-account capture leaves the store exactly as it was —
    cookies included. Returns (profile_dir, note).
    """
    pdir = profile_dir(profile, store)
    metadata, note = merge_profile_metadata(
        read_profile_metadata(pdir), profile=profile, csrf=csrf, session=session,
        email=email, build_label=build_label, force=force)

    pdir.mkdir(parents=True, exist_ok=True)
    pdir.chmod(0o700)

    cookies_file = pdir / "cookies.json"
    cookies_file.write_text(json.dumps(cookies, indent=2, ensure_ascii=False), encoding="utf-8")
    cookies_file.chmod(0o600)

    meta_file = pdir / "metadata.json"
    meta_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    meta_file.chmod(0o600)
    return pdir, note


def extract_and_save(ctx, page, profile: str, wait_s: int,
                     extract_csrf, extract_session, extract_email=None, *,
                     force: bool = False,
                     store: str | os.PathLike | None = None) -> int:
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
              "the old --manual path hit). Ensure the browser is ON NotebookLM "
              "(notebook.google.com, or the older notebooklm.google.com which "
              "redirects there) and signed in, and that the CLI extractors are "
              "importable (--cli-site-packages).", file=sys.stderr)
        return 4

    # The signed-in address, from the SAME page HTML. Never fatal: absence means
    # the stored address is carried forward instead of confirmed.
    email = None
    if extract_email and html:
        try:
            email = (extract_email(html) or "").strip() or None
        except Exception as e:  # pragma: no cover - upstream regex/env failure
            print(f"[nlm-auth] WARNING: could not read the signed-in address ({e}).",
                  file=sys.stderr)

    try:
        pdir, note = write_native_profile(profile, cookies, csrf, session,
                                          email=email, force=force, store=store)
    except AccountMismatch as e:
        print(f"[nlm-auth] REFUSING TO WRITE: profile {e.profile!r} records the "
              f"account {e.stored!r}, but the browser this extraction read is "
              f"signed in as {e.captured!r}. Nothing was written — not cookies, "
              f"not metadata. Sign the browser into {e.stored!r} and re-run, or "
              f"pass --force to overwrite the recorded account deliberately "
              f"(same semantics as `nlm login --force`).", file=sys.stderr)
        return 5

    print(f"[nlm-auth] wrote full profile '{profile}' ({len(cookies)} cookies, "
          f"csrf+session captured) -> {pdir}", flush=True)
    print(f"[nlm-auth] account: {note}.", flush=True)
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
                    help="dir containing notebooklm_tools (for the csrf/session "
                         "and signed-in-address extractors)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite the profile's recorded account address even "
                         "when the live session is a DIFFERENT account (same "
                         "semantics as `nlm login --force`)")
    args = ap.parse_args()

    extract_csrf, extract_session = _load_cli_extractors(args.cli_site_packages)
    extract_email = _load_email_extractor(args.cli_site_packages)
    wait_s = args.wait if args.mode == "bootstrap" else 30

    with sync_playwright() as p:
        if args.cdp_url:
            # Connect to an already-signed-in browser. No navigation/re-login.
            browser = p.chromium.connect_over_cdp(args.cdp_url)
            ctx = browser.contexts[0] if browser.contexts else browser.new_context()
            page, how = select_notebooklm_page(ctx)
            if how == "existing":
                print(f"[nlm-auth] reusing the open NotebookLM tab ({page.url}).",
                      flush=True)
            else:
                print(f"[nlm-auth] no NotebookLM tab open on "
                      f"{' or '.join(NB_HOSTS)}; opening a NEW tab on {NB_URL} "
                      f"rather than navigating one you are using.", flush=True)
                page.goto(NB_URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(6)
            rc = extract_and_save(ctx, page, args.profile, wait_s, extract_csrf,
                                  extract_session, extract_email, force=args.force)
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
        # This browser is OURS (a dedicated profile dir we just launched), so
        # navigating its first tab hijacks nobody — the #537 hazard is the
        # --cdp-url path above, which connects to the operator's own browser.
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(NB_URL, wait_until="domcontentloaded", timeout=60000)
        if args.mode == "bootstrap":
            print("[nlm-auth] A browser window is open. Sign in as the TARGET (books) "
                  "account and open NotebookLM — either notebook.google.com (the "
                  "live host since the rebrand) or notebooklm.google.com (L-M), "
                  f"which redirects there. Waiting for the session (up to {wait_s}s)...",
                  flush=True)
        time.sleep(6)
        rc = extract_and_save(ctx, page, args.profile, wait_s, extract_csrf,
                              extract_session, extract_email, force=args.force)
        ctx.close()
        return rc


if __name__ == "__main__":
    raise SystemExit(main())
