# NotebookLM Projection Sync — Open Operational Item

Status: draft
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
2. A human signs into the **books account** and opens NotebookLM. Since the
   provider's rebrand the live host is **`notebook.google.com`** ("Gemini
   Notebook") and `https://notebooklm.google.com/` redirects there, so either
   URL lands on the signed-in app. The old L-M spelling now matters only to the
   TOOLING, which still matches on it — see the broken CLI bullet in step 3.
3. Extract fully with the harness `scripts/nlm_auth.py` — connect to the
   already-signed-in browser over `--cdp-url` (no re-login) or launch a
   persistent profile; it writes the native profile directly. This is the route
   that actually authenticated the 2026-08-24 hosting migration.

   The CLI's own extraction — `nlm login --cdp-url http://127.0.0.1:9444
   --profile <profile>` — was the documented alternative and is **BROKEN since
   the provider's rebrand; do not run it.** It polls for a tab on
   `notebooklm.google.com` while the signed-in tab is now on
   `notebook.google.com`, so `is_logged_in()` reports false for a browser that
   IS signed in and the command dies on "Login timeout" after its 300 s wait;
   `NOTEBOOKLM_BASE_URL` cannot be repointed, because it is validated against
   the same allow-list. Recorded as F1 in
   [the migration evidence](notebook-projection-migration-evidence-2026-08-24.md);
   the fix is carried by opensoft/openxFactory#537.

   The harness is **not** host-clean either: `NB_URL` and its `--cdp-url`
   page-selection predicate both hard-code `notebooklm.google.com`, and its
   operator messages still name that host. It works today only because the
   predicate's miss falls through to navigating a tab to `NB_URL`, which
   redirects to the live host. That correction belongs to #537 as well; until it
   lands, the harness is the working route, not a repaired one.

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

RATIFIED and REALIZED 2026-08-23 as `add-notebook-projection-identity`, except
for the migration itself. The declared account is `xFactor001@opensoft.one`;
the declaration lives in `examples/notebook-projection-hosting.yaml`, and the
sync now refuses to run against an account nobody declared. THIS ITEM STAYS
OPEN by its own terms: it closes on the migration, which is gated on an
interactive `nlm login --profile company` that only Brett can perform, on a
host with a browser. The sequencing — re-derive, migrate live sessions, replace
the workspace records, prove parity against the corpus scan, retire the legacy
books by recorded act — is
[the hosting migration runbook](notebook-projection-migration-runbook.md).

**2026-08-31 — THE CHANGE IS ARCHIVED AND THIS ITEM IS STILL OPEN.**
`add-notebook-projection-identity` archived that day at
`openspec/changes/archive/2026-08-31-add-notebook-projection-identity`, with the
migration, the parity proof and the legacy-book retirement all done. Its § 5.1 —
the box whose whole job was to close THIS item — was **deliberately not ticked**
and archives standing as a disposition, ruled by Brett Heap that day. The reason
is the "Strategic direction" above, read literally: the account moved, but the
**unattended** property it names did not arrive with it.

Three grounds, all still true:

1. Google's sign-in for `xFactor001@opensoft.one` is an **interactive browser
   flow**. There is no unattended path today.
2. **`nlm login` is broken upstream** by the notebook.google.com rebrand — the
   CLI's `_is_notebooklm_url()` allow-list accepts only `notebooklm.google.com`
   / `notebooklm.cloud.google.com`, so `is_logged_in()` reports false for a
   browser that IS signed in, `nlm login --cdp-url` dies on "Login timeout", and
   `NOTEBOOKLM_BASE_URL` cannot be repointed because it is validated against the
   same allow-list. Only the login path is affected; the API calls still work.
   The "method that works" section above has been corrected accordingly: its
   `nlm login --cdp-url` bullet is marked BROKEN, and the way in is the harness
   `scripts/nlm_auth.py` — the route that actually authenticated the 2026-08-24
   migration. The harness hard-codes the same old host in `NB_URL` and its page
   predicate and works only because the redirect covers for it, so #537 carries
   that correction too.
3. `add-notebook-hosting-credential-custody` states in **ratified text** that
   custody governs who may obtain the credential and **does not deliver
   automation**. No custody work discharges this item.

**The named successor is opensoft/openxFactory#537** — the deferred
automated-Google-login item, carrying the upstream CLI allow-list defect and the
machine-account "log in whenever it wants" property as two distinct halves (only
the second one closes this). **This item closes when unattended
re-authentication actually works**, and not before.

## Related known bug (own change, not this item)

A routine `sync-notebooklm-books.py --apply` in one checkout can delete another
engineer's `xf-wb-*` scratch notebooks — gitignored workbench manifests mean
liveness cannot be proven cross-checkout. Wants its own change; noted in the
`add-workbench-branch-sessions` research.

## How to resume

1. See `~/xf-nlm-sync/AFTER-REBOOT.md`; rebuild the venv if `/tmp` was wiped.
2. WSLg GUI rendering is resolved (see above); if a headed window fails to
   appear, `wsl --update` from PowerShell and reboot.
3. Get a live session via full CDP extraction, using the harness — either
   `python .../nlm_auth.py bootstrap --profile personal --channel chrome`
   (sign into the books account once; either NotebookLM URL is fine, the old
   one redirects), or connect to an already-signed-in Chrome with
   `... refresh --profile personal --cdp-url http://127.0.0.1:9444`, which is
   how the 2026-08-24 migration authenticated. **Do NOT use `nlm login
   --cdp-url` — the rebrand broke it** (F1 / #537, see above); it only burns its
   300 s timeout against a browser that is genuinely signed in.
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
