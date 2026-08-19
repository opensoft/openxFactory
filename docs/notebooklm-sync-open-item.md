# NotebookLM Projection Sync — Open Operational Item

Status: open (operational)
Owner: openxFactory (the projection capability and its tooling live here —
`scripts/sync-notebooklm-books.py`, `docs/lifecycle-notebook-projection.md`).
Opened: 2026-08-19 (handoff from the 08-14→08-19 cross-repo session).

This is an operational open item, not a capability change. It records a
pending projection run, the auth blocker that stalls it, the workaround built
for that blocker, and the strategic direction that retires the blocker for
good — so any session can resume without rediscovery.

## What is pending

The derived NotebookLM books (`sync-notebooklm-books.py`, run from the
aggregation root as `python3 openxFactory/scripts/sync-notebooklm-books.py .
--apply`) need one `--apply` run to reflect recent doc-lifecycle changes —
e.g. the `client-identity-roster` archive on openxFactory main and the new
OpsxFactory staging topics (`managed-service-inventory`,
`tenant-reader-grant-pipeline`). Projection is **derived, never curated**, so
a single reconciling run brings every book current; there is no manual
per-source work.

## The blocker

Authentication to NotebookLM. Auth is five Google session cookies
(`SID, HSID, SSID, APISID, SAPISID`, valid ~1 week); there is no API and no
device-code flow. The `nlm` CLI's browser logins fail on this WSL2 host:

- `nlm login --wsl` launches **Windows** Chrome and reads cookies over a
  **TCP CDP port** that the WSL firewall blocks (the firewall-rule prompt did
  not clear it across multiple attempts).
- Cookie hand-import is not a workable path here.

## The workaround (built this session — `scripts/nlm_auth.py`)

A Playwright persistent-profile harness that sidesteps the exact wall above:
it launches Chromium **inside WSL under WSLg** and drives it over a **stdio
pipe** — no TCP, no Windows firewall, no Windows Chrome. Cookies are harvested
from the live browser context and imported via `nlm login --manual` (the CLI's
own store-writer). A **persistent profile** means the Google login form is
seen once; later `refresh` runs are unattended.

- `bootstrap` — headed window; a human signs in once as the target account.
- `refresh` — reuses the signed-in persistent profile; no human.
- Defaults to system Google Chrome via `--channel chrome` (Playwright's
  bundled Chromium did not render under this WSLg).

**Unresolved:** whether WSLg surfaces a GUI window to the Windows desktop at
all on this host. The harness launches and reads cookies, but no visible
window appeared, including after a reboot. That is a Windows-side WSLg
question (try `wsl --update` from PowerShell), not a harness defect — the
firewall/CDP wall the harness was built to bypass is genuinely gone.

Durable host staging for a resume: `~/xf-nlm-sync/` (`AFTER-REBOOT.md`
runbook, a full aggregation clone with submodules at pins, venv rebuildable).
The harness there and the copy committed here as `scripts/nlm_auth.py` are the
same tool.

## Account

Run under the `nlm` **`personal`** profile — the account that owns the
xFactory books (its notebook list contains "xFactory — Canon" etc.). Confirmed
this session. Do NOT use the `farheap` profile (a different account; the books
are not there).

## Strategic direction (retires the blocker)

Migrate projection to a dedicated **machine Google user account** so xFactory
can re-authenticate unattended from a persistent profile — the "log in
whenever it wants" property. A GCP service account cannot be used (NotebookLM
has no API and service accounts cannot drive the consumer web UI); it must be
a Google **user** account (e.g. a Workspace user), owning all books and
sharing them to human accounts. Because projection is derived, migrating is
one `--apply` run in the new account. Staged: `ideation/staging/
notebook-projection-identity/notebook-projection-identity.md`.

## Related known bug (own change, not this item)

A routine `sync-notebooklm-books.py --apply` in one checkout can delete another
engineer's `xf-wb-*` scratch notebooks — gitignored workbench manifests mean
liveness cannot be proven cross-checkout. Wants its own change; noted in the
`add-workbench-branch-sessions` research.

## How to resume

1. See `~/xf-nlm-sync/AFTER-REBOOT.md`; rebuild the venv if `/tmp` was wiped.
2. Confirm WSLg renders a GUI window before spending time on the harness.
3. `python .../nlm_auth.py bootstrap --profile personal --channel chrome` →
   sign into the books account once.
4. Verify with a real `nlm notebook list` (not `login --check`).
5. Dry-run `sync-notebooklm-books.py .` → review the ADD plan and the
   `[workbench]` orphan-sweep plan → `--apply`.
6. Copy the updated manifest back to the aggregation root
   `.claude/nlm-sync-manifest.json`.

## Verification discipline

Confirm openxFactory facts against **origin/main or the pinned submodule
commit**, never a shared submodule working checkout — during this session the
shared `openxFactory` checkout sat 37 commits behind origin/main on another
lane's branch, which misreports recently-merged work as absent.
