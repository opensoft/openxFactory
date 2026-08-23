# NotebookLM Projection Sync — Open Operational Item

Status: open (operational)
Owner: openxFactory (the projection capability and its tooling live here —
`scripts/sync-notebooklm-books.py`, `docs/lifecycle-notebook-projection.md`).
Opened: 2026-08-19 (handoff from the 08-14→08-19 cross-repo session).

This is an operational open item, not a capability change. It records the
projection auth blocker, the method that actually authenticates `nlm`, the
2026-08-19 run that used it, and the strategic direction that retires the
blocker for good — so any session can resume without rediscovery.

## What is pending

The derived NotebookLM books (`sync-notebooklm-books.py`, run from the
aggregation root as `python3 openxFactory/scripts/sync-notebooklm-books.py .
--apply`) reconcile on each run to reflect recent doc-lifecycle changes.
Projection is **derived, never curated**, so a single reconciling run brings
every book current; there is no manual per-source work. A run landed
2026-08-19 (see Run history below); resume from wherever the docs have moved
since.

## The blocker

Authentication to NotebookLM. A working `nlm` session needs THREE things, not
just cookies: the google.com cookie **list** (session cookies
`SID, HSID, SSID, APISID, SAPISID` among them, valid ~1 week), plus a
**csrf_token** and a **session_id** scraped from the logged-in page. There is
no API and no device-code flow. `nlm login --wsl` fails on this WSL2 host: it
launches **Windows** Chrome and reads tokens over a **TCP CDP port** that the
Windows firewall blocks (the firewall-rule prompt did not clear it across
multiple attempts).

## The method that works — full CDP extraction (`scripts/nlm_auth.py`)

The path that actually authenticates is a **full CDP/Playwright extraction of a
live NotebookLM session** under WSLg — captured all three of cookie-list +
csrf_token + session_id. It sidesteps the firewall wall by keeping the debug
port on **127.0.0.1 inside WSL**, so no Windows firewall is involved:

1. WSLg renders a headed **Google Chrome** (system Chrome; Playwright's bundled
   Chromium did not render under this WSLg — use `--channel chrome`). Either
   launch it on a localhost remote-debugging port, e.g.
   `google-chrome --user-data-dir=<profile> --remote-debugging-port=9444
   https://accounts.google.com/`, or let the harness launch a persistent
   profile.
2. A human signs into the **books account** and opens
   `https://notebooklm.google.com/` — note **notebooklm** (with the L-M); a
   wrong host such as `notebook.google.com` makes extraction time out.
3. Extract fully, one of two ways (both produce the same native profile):
   - `nlm login --cdp-url http://127.0.0.1:9444 --profile <profile>` — the
     CLI's native extraction. The port **must differ from the default 18800**
     to trigger the external-CDP path, and the browser must be **on
     notebooklm.google.com** when the CLI polls.
   - the harness `scripts/nlm_auth.py` — connect to the already-signed-in
     browser over `--cdp-url` (no re-login) or launch a persistent profile,
     then it writes the native profile directly.

The harness modes:

- `bootstrap` — headed window; a human signs in once as the books account.
- `refresh` — reuses the signed-in persistent profile (or an open browser over
  `--cdp-url`); no human. This is xFactory's "log in whenever it wants".

It writes the FULL native profile — `cookies.json` as the cookie **list** plus
`metadata.json` with `csrf_token`/`session_id` (email/build_label left null).
Verify with a REAL call (`nlm notebook list`), never `login --check`.

### Why the old cookies-only path is INSUFFICIENT (the lesson)

The earlier approach harvested cookies only and imported them via
`nlm login --manual`. **That does not produce working auth** and must not be
reintroduced:

- `--manual` stored cookies as a `{name: value}` **dict**; the native store
  expects a cookie **list** of full dicts (wrong shape).
- it left `csrf_token` and `session_id` **null**.

The import reported success, yet `nlm notebook list` returned "Authentication
expired". Cookies alone are not a NotebookLM session — csrf_token and
session_id are mandatory, and the cookie shape matters.

### WSLg GUI rendering — RESOLVED

Whether WSLg surfaces a GUI window was previously unresolved. It is now
**resolved**: a Windows/WSL reboot fixed WSLg GUI rendering, a headed Chrome
window appears on the Windows desktop, and the sync was run successfully on
2026-08-19. If a headed window ever fails to appear again, run
`wsl --update` from PowerShell and reboot.

Durable host staging for a resume: `~/xf-nlm-sync/` (`AFTER-REBOOT.md`
runbook, a full aggregation clone with submodules at pins, venv rebuildable).
The harness there and the copy committed here as `scripts/nlm_auth.py` are the
same tool.

## Run history

- **2026-08-19** — sync RUN successfully (full CDP extraction path). Projected
  changes: canon (3 add / 8 upd), drafts (18 add / 8 upd),
  ideation-openxFactory (7 add / 2 upd), ideation-OpsxFactory (1 add); no
  deletions. The orphan sweep of `xf-wb-staged-staged-topic-outline-template`
  was deliberately **SKIPPED** — the known cross-checkout sweep bug (below)
  cannot prove another engineer's `xf-wb-*` notebook is not live. The updated
  manifest was copied back to the aggregation root
  `.claude/nlm-sync-manifest.json`.

## Account

Run under the `nlm` **`personal`** profile — the account that owns the
xFactory books. Identify that account by the **books it shows** (its notebook
list contains "xFactory — Canon" etc.), not by name: its stored `email` is
null. Do NOT assume a named account (e.g. `farheap`); a profile pointed at a
different Google account will not see the books.

## Strategic direction (retires the blocker)

Migrate projection to a dedicated **machine Google user account** so xFactory
can re-authenticate unattended from a persistent profile — the "log in
whenever it wants" property. A GCP service account cannot be used (NotebookLM
has no API and service accounts cannot drive the consumer web UI); it must be
a Google **user** account (e.g. a Workspace user), owning all books and
sharing them to human accounts. Because projection is derived, migrating is
one `--apply` run in the new account. Staged: `ideation/staging/
notebook-projection-identity/notebook-projection-identity.md`.

Dispositioned 2026-08-23: that staged topic's five hosting-identity
questions all carry dispositions now — Brett ruled a Google Workspace USER
account in `opensoft.one` — but THIS operational item stays open, because
it closes on the eventual change's realization, not on the rulings.

## Related known bug (own change, not this item)

A routine `sync-notebooklm-books.py --apply` in one checkout can delete another
engineer's `xf-wb-*` scratch notebooks — gitignored workbench manifests mean
liveness cannot be proven cross-checkout. Wants its own change; noted in the
`add-workbench-branch-sessions` research.

## How to resume

1. See `~/xf-nlm-sync/AFTER-REBOOT.md`; rebuild the venv if `/tmp` was wiped.
2. WSLg GUI rendering is resolved (see above); if a headed window fails to
   appear, `wsl --update` from PowerShell and reboot.
3. Get a live session via full CDP extraction — either
   `python .../nlm_auth.py bootstrap --profile personal --channel chrome`
   (sign into the books account once, on notebooklm.google.com), or connect to
   an already-signed-in Chrome with `... refresh --profile personal
   --cdp-url http://127.0.0.1:9444`, or `nlm login --cdp-url
   http://127.0.0.1:9444 --profile personal` (non-default port, browser on
   notebooklm.google.com).
4. Verify with a real `nlm notebook list` (not `login --check`).
5. Dry-run `sync-notebooklm-books.py .` → review the ADD plan and the
   `[workbench]` orphan-sweep plan (skip `xf-wb-*` orphans — see the bug
   below) → `--apply`.
6. Copy the updated manifest back to the aggregation root
   `.claude/nlm-sync-manifest.json`.

## Verification discipline

Confirm openxFactory facts against **origin/main or the pinned submodule
commit**, never a shared submodule working checkout — during this session the
shared `openxFactory` checkout sat 37 commits behind origin/main on another
lane's branch, which misreports recently-merged work as absent.
