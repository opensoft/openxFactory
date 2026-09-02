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

   The harness's own host handling is **repaired** (the #537 harness half): its
   `--cdp-url` page-selection predicate now matches a NotebookLM tab on EITHER
   host and reuses it, opening a NEW tab only when there is none — it no longer
   misses every post-rebrand tab and navigates an arbitrary one away — and its
   operator messages name both hosts. `NB_URL` deliberately stays on
   `notebooklm.google.com`: no recorded run has navigated DIRECTLY to the new
   host, and the "wrong host makes extraction time out" claim the harness used
   to carry is unevidenced (it entered with the 2026-08-19 docstring rewrite and
   describes `nlm login`'s allow-list timeout, not this harness). So the
   redirect dependency is recorded in a comment beside the constant rather than
   traded for an untested flip. The UPSTREAM half — `notebooklm_tools`'
   `_is_notebooklm_url()` allow-list — is unchanged and still rejects
   `notebook.google.com` (0.5.26), so `nlm login` stays broken.

The harness modes:

- `bootstrap` — headed window; a human signs in once as the books account.
- `refresh` — reuses the signed-in persistent profile (or an open browser over
  `--cdp-url`); no human. This is xFactory's "log in whenever it wants".

It writes the FULL native profile — `cookies.json` as the cookie **list** plus
`metadata.json` with `csrf_token`/`session_id`. It **merges** that metadata into
whatever the store already holds (openxFactory#543, fix (a)): the address the
sync's account check reads is carried forward rather than nulled, the signed-in
address is captured from the same page HTML when the CLI's extractor is
importable, and a capture that CONTRADICTS the stored address refuses the write
outright — nothing lands, cookies included — unless `--force` is passed, mirroring
`nlm login --force`. See step 5 of [How to resume](#how-to-resume).
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

Run under the `nlm` **`company`** profile — `xFactor001@opensoft.one`, the
account that has owned the xFactory books since the 2026-08-24 migration and
the one `examples/notebook-projection-hosting.yaml` declares
(`hosting.nlm_profile: company`, `migration.state: complete`). This is not a
preference: the sync reads that declaration and REFUSES a run whose active
profile is anything else (`enforce_hosting_profile()`,
`scripts/sync-notebooklm-books.py:2228`; refusal at :2271-2278).

Identify the account by the **books it shows** (a notebook list containing
"xFactory — Canon" etc.), and note that the sync also checks the ADDRESS, not
only the profile name: `profiles/company/metadata.json` records
`email: xFactor001@opensoft.one` — set from the vault-held username during the
migration, because the harness wrote that field null then — and a name pointed
at some other account is refused too (`profile_account()`, :2035-2051; refusal
at :2285-2292). Do NOT assume a named account (e.g. `farheap`); a profile
pointed at a different Google account will not see the books.

**That address check is armed only while the field is populated, and the auth
harness no longer empties it** (openxFactory#543 fix (a)). `nlm_auth.py` merges
`metadata.json` instead of replacing it, so a run of step 3 below leaves the
address standing; it also captures the signed-in address when it can and
REFUSES to write when that contradicts the stored one. Step 5 is therefore a
VERIFICATION step rather than a repair — read the field back and prove the
estate. Fix (b) — the sync refusing a null-address hosting profile outright —
is **not** implemented and remains a ruling to take, so a store that has never
recorded an address still runs on the profile NAME alone.

**The `personal` profile is now the LEGACY account** (`brettheap@gmail.com`).
It is kept to READ what stayed behind — the seven archive-renamed legacy
notebooks, and the two live session notebooks that step 5 of the migration HELD
on that account ([migration
evidence](notebook-projection-migration-evidence-2026-08-24.md); the
[step-8 retirement runbook](notebook-projection-retirement-runbook-step8.md)
switches to `personal` for exactly that reason). Reading the legacy account
under `personal` is legitimate; running the CURRENT projection under it is not,
and the sync refuses it. Statements further down that describe past
`personal`-profile runs are records of what happened then, not instructions for
now.

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
   migration. The harness's own page predicate is now host-correct (it accepts
   BOTH hosts and reuses an open NotebookLM tab rather than hijacking one), but
   that repairs only this repo's half: `NB_URL` still points at the old host by
   a recorded decision, so the redirect dependency stands, and the UPSTREAM
   allow-list is untouched — 0.5.26 still rejects `notebook.google.com`. #537
   therefore stays open for the upstream fix and for the unattended property.
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
3. Get a live session via full CDP extraction, using the harness, INTO THE
   `company` PROFILE — either
   `python .../nlm_auth.py bootstrap --profile company --channel chrome`
   (sign in as `xFactor001@opensoft.one` once; either NotebookLM URL is fine,
   the old one redirects), or connect to an already-signed-in Chrome with
   `... refresh --profile company --cdp-url http://127.0.0.1:9444`, which is
   how the 2026-08-24 migration authenticated. Pass `--profile` explicitly: it
   names the profile STORE the harness writes, and its default is still the
   legacy `personal` (`scripts/nlm_auth.py:207`). **Do NOT use `nlm login
   --cdp-url` — the rebrand broke it** (F1 / #537, see above); it only burns its
   300 s timeout against a browser that is genuinely signed in. The same defect
   is why `nlm login --profile company` — the first-time route the sync's own
   refusal text suggests at :2278 — is not the way in; the harness is.
4. Verify with a real `nlm notebook list` (not `login --check`), and confirm the
   list it returns is the xFactory books.
5. **Verify the account address in the profile store — without it the sync
   cannot tell which ACCOUNT it is writing to.** Step 3 no longer erases it:
   the harness MERGES `metadata.json` rather than replacing it, carries a
   populated `email` forward when the extraction yields none, captures the
   signed-in address from the same page HTML when the CLI's extractor is
   importable, and REFUSES the write (nothing lands, cookies included) when a
   captured address contradicts the stored one — `--force` overrides,
   mirroring `nlm login --force` (`merge_profile_metadata()` /
   `write_native_profile()` in `scripts/nlm_auth.py`; openxFactory#543 fix (a)).
   Step 3 prints one `[nlm-auth] account: …` line saying what it carried
   forward or captured; read it.

   Why the field still matters: the sync reads exactly it, and a null means
   UNKNOWN there, not "no such thing" (`profile_account()`,
   `scripts/sync-notebooklm-books.py:2035-2050`). A null still SKIPS the address
   refusal at :2285-2292 — it is guarded by `if signed_in and …` — leaving the
   run to print "records no account address … verified by profile NAME only"
   (:2293-2297) and bind anyway, so the only hard check left is the
   profile-NAME check at :2271-2278, which a re-auth into `company` passes no
   matter which Google account signed in. That sync-side hole is fix (b) of
   #543 and is **NOT** implemented: it hard-blocks every operator whose store
   legitimately has no recorded address, so it is a ruling, not a cleanup.
   **The failure this prevents:** authenticate the `company` store as the wrong
   account — most plausibly the legacy `brettheap@gmail.com`, which still holds
   the seven archive-renamed xFactory-titled notebooks — and step 7's `--apply`
   sends its additions AND its deletions into that estate.

   Read the field back:

   ```bash
   nlm login profile list     # expect: company: xFactor001@opensoft.one
   ```

   If it prints `Unknown`, the store never had an address and the harness
   captured none (the CLI's extractor was not importable — pass
   `--cli-site-packages`). Only then re-assert it by hand, merging the field
   rather than rewriting the file, or you drop the `csrf_token`/`session_id`
   step 3 just captured:

   ```bash
   python3 - <<'PY'
   import json, pathlib
   p = pathlib.Path.home() / ".notebooklm-mcp-cli/profiles/company/metadata.json"
   m = json.loads(p.read_text())
   m["email"] = "xFactor001@opensoft.one"
   p.write_text(json.dumps(m, indent=2) + "\n")
   p.chmod(0o600)
   PY
   ```

   `nlm login profile list` prints each profile's RECORDED address, and prints
   `Unknown` when it is null (`docs/notebook-projection-migration-runbook.md:63`),
   so it proves the check is armed — and only that. It cannot prove the cookies
   belong to that account, so the proof of estate stays step 4's read — run
   explicitly as `nlm notebook list --profile company`, the account-proof the
   migration used and the call the harness itself makes (`verify()` in
   `scripts/nlm_auth.py`), because the CLI's default profile is not bound to
   `company` until step 6 and a bare `nlm notebook list` before that reads
   whichever profile is default. Setting the field by hand is what the
   2026-08-24 migration had to do ([migration
   evidence](notebook-projection-migration-evidence-2026-08-24.md): "the harness
   writes that field null, so it was set from the vault-held username; the
   sync's binding check reads it") — that hand-repair is retired, but the
   read-back is not.

6. **Bind the CLI to `company` before syncing** — `nlm login switch company`,
   then read it back with `nlm config get auth.default_profile` (expect
   `company`). This is a SEPARATE act from step 3: the harness writes the
   profile store and never touches `auth.default_profile`, and the sync will not
   switch it either, because the CLI selects a profile PROCESS-GLOBALLY and that
   is shared user state — of the verbs the sync issues (`notebook`, `source`,
   `alias`, `tag`, `chat`) none takes a per-invocation `--profile`, so the
   binding is verified rather than passed (`active_nlm_profile()`,
   `scripts/sync-notebooklm-books.py:2125-2137`). Skip this and step 7 dies
   before writing anything, on `hosting: expected the 'company' profile but the
   CLI's active profile is 'personal'. Refusing: …` (:2271-2278). The check is
   re-asserted before EVERY invocation, so another terminal running
   `nlm login switch` mid-run aborts the rest of the job
   (`assert_still_bound()`, :2054-2079) — re-bind and re-run, the sync is
   idempotent over what finished.
7. Dry-run `sync-notebooklm-books.py .` → review the ADD plan and the
   `[workbench]` orphan-sweep plan (skip `xf-wb-*` orphans — see the bug
   below) → `--apply`.
8. Copy the updated manifest back to the aggregation root
   `.claude/nlm-sync-manifest.json`.

## Verification discipline

Confirm openxFactory facts against **origin/main or the pinned submodule
commit**, never a shared submodule working checkout — during this session the
shared `openxFactory` checkout sat 37 commits behind origin/main on another
lane's branch, which misreports recently-merged work as absent.
