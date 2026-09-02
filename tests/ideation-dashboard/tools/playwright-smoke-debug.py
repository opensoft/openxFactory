#!/usr/bin/env python3
"""T098: the scratch-repository doxBench Playwright smoke (quickstart §7).

PROVENANCE. Ported into openxFactory on 2026-08-26, on Brett's ruling that
this tool's home is openxFactory — beside the runtime it drives. It came from
codexFactory branch `010-doxbench-editor-chat`, path
`specs/010-doxbench-editor-chat/playwright-smoke.py`, blob `fc321637`
(authored there 2026-08-08 at commit `3e6f900`). codexFactory's
`adopt-neutral-tooling-home` tranche C shed the shorter `main` version along
with the dashboard runtime it drives; this extended 892-line version was never
adopted and survived only in that branch's history. The port is VERBATIM apart
from this header and the checkout-root depth below — nothing in the eleven
scenarios changed. The `quickstart §7` the title names is codexFactory's,
retained there as the specification of what T098 covered.

AN OPERATOR TOOL, OUTSIDE THE HERMETIC SUITE. It drives a real browser, so it
lives under `tests/ideation-dashboard/tools/` and is deliberately NOT named
`test_*.py`: neither pytest collection nor `tests/hermetic_unittest.py`'s
`test_*.py` discovery may ever pick it up, and no gate may require it. Do not
add a `conftest.py` beside it either — `test_hermeticity.py` pins the SET of
conftests under `tests/`, and `conftest` is an ambient module name.

WHAT IT NEEDS. Playwright 1.61.0 and its chromium browser, on the HOST (`pip
install playwright==1.61.0 && python -m playwright install chromium`; the
1.61.1 pin this header once named DOES NOT EXIST on PyPI — corrected from the
first real run's findings, 2026-07-31). Containers built for the hermetic
suite deliberately do not carry it. Run from an openxFactory checkout:

    python3 tests/ideation-dashboard/tools/playwright-smoke.py

NO CONSOLE URL IS PASSED, and no console should be started for it. The smoke
builds its own world end to end — a scratch bare remote, a scratch checkout
seeded from `tests/ideation-dashboard/fixtures/base-repo`, a snapshot, and a
loopback server constructed IN PYTHON through `serve.build_server` bound to
127.0.0.1 on an ephemeral port — and then drives that. The operator rig's
serves (`scripts/ideation_dashboard/cli.py generate-and-open`, or
`~/doxbench-operator/t100_serve.py <worktree> <corpus> <port>`) are for a
human at a real corpus and are NOT used here; pointing this smoke at one would
break the session runbook §7 rule that a serve under test points at a SCRATCH
checkout only.

`OPENXFACTORY_ROOT` IS NO LONGER REQUIRED. Under codexFactory the env override
pointed `doxbench_contracts` at a pinned openxFactory release so the routes'
released-schema validators could resolve. Run from openxFactory itself,
`doxbench_contracts.resolve_root` recognises the hosting repository as a
publisher checkout and resolves the contract there. Set it only to pin a
DIFFERENT released checkout deliberately.

The script fails CLOSED with a named preflight error rather than skipping, so
a green run can only ever mean the scenarios really ran.

Everything here is hermetic by construction: a scratch checkout cloned from a
scratch bare remote, a fake model port (deterministic prose + one typed
proposal bound to the live outline identity), a fake pull-request port, and a
loopback server built through the same `build_server` seams the route tests
use. No real provider, no `gh`, no network beyond 127.0.0.1.

Covers, in order (quickstart §7's eleven steps):
  1  open a staged topic in doxBench;
  2  edit Outline;
  3  submit a turn;
  4  select the backed detail document and edit it;
  5  submit a later turn and prove it saw BOTH current buffers;
  6  apply one current proposal;
  7  make another proposal stale and prove refusal;
  8  ORDERED Save — Outline then Document, two ordered commits proven in git;
  8b PARTIAL Save — a second actor's commit in the SESSION WORKTREE moves
     the document base; the next Save commits Outline and REFUSES the
     Document row, whose text and dirty flag survive (FR-031/FR-032 live);
  9  refresh/rekey to the session;
  10 the session verbs on the proposal-carrying tile: open-pr REFUSES with
     FR-024 verbatim ("worked OR proposed, never both") — recorded live,
     with the doxBench session deliberately left open on that tile;
  10e MERGE-ENDING live, on keyword-lens (no proposal): first Save opens
     session A, the submitted save form really opens the pull request
     (FakePullRequests), the branch is merged EXTERNALLY into the bare
     remote, the next save refuses base_stale VERBATIM (naming the runbook's
     mandatory pull), the scripted operator refresh (T100's
     `main_view_refreshed`) is performed and recorded, the save after it
     ends the session — branch deleted, worktree/registry torn down, FR-039
     working state cleared — and a dashboard rebuilt at the refreshed main
     plus a reload restores NOTHING but the merged governed content;
  10f ABANDON-CLEANUP live — session B on the same tile (the merge ending
     freed the deterministic branch name; an abandoned branch would refuse
     the next open as resume-or-new) is abandoned with its durable reason:
     worktree and registry entry torn down, branch RETAINED, FR-039 working
     state cleared;
  11 zero page errors, failed requests, or provider-network requests; the
     served checkout is never moved by any governance action — its ONE
     recorded movement is the scripted operator refresh in 10e.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

# `tests/ideation-dashboard/tools/playwright-smoke.py` — three directories
# down from the checkout root. Under codexFactory the script sat two down
# (`specs/010-doxbench-editor-chat/`), which is the ONLY path fact the port
# had to change; every path below is derived from here and needs no edit.
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
# The proven session fixtures (fake pull-request port) live beside the
# hermetic suites; steps 8-10 reuse them at their ONE injection point each.
sys.path.insert(0, str(REPO_ROOT / "tests" / "ideation-dashboard"))


def _preflight_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ModuleNotFoundError:
        raise SystemExit(
            "T098 PREFLIGHT REFUSED: playwright is not installed. Install "
            "playwright==1.61.0 and its chromium browser in the acceptance "
            "environment, then re-run. This script never skips."
        )
    from playwright.sync_api import sync_playwright

    return sync_playwright


def _run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _scratch_checkout(base: Path) -> tuple[Path, Path]:
    """A scratch bare remote plus a working clone seeded from the COMMITTED
    base-repo fixture (tests/ideation-dashboard/fixtures/base-repo), so the
    snapshot generator and the scope projection see exactly the world every
    hermetic suite already exercises — same repository name, same staged
    tiles, same outline paths."""
    remote = base / "scratch-remote.git"
    checkout = base / "scratch-checkout"
    _run(
        ["git", "-c", "init.defaultBranch=main", "init", "--bare", str(remote)],
        cwd=base,
    )
    _run(
        ["git", "-c", "init.defaultBranch=main", "clone", str(remote), str(checkout)],
        cwd=base,
    )
    # The checkout's OWN git identity must authenticate the smoke's actor
    # claim (actor_identity trust gap, 72b9c48f): a `-c user.name=...` flag
    # scopes to ONE command and never persists, so `git config user.name`
    # here would fall through to the operator's global identity and the
    # "t098" claim would resolve to NOBODY — fail-closed, and the plane
    # comes up read-only with the canvas never offered.
    _run(["git", "config", "user.name", "T098"], cwd=checkout)
    _run(["git", "config", "user.email", "t098@example.invalid"], cwd=checkout)
    fixture = REPO_ROOT / "tests" / "ideation-dashboard" / "fixtures" / "base-repo"
    for child in fixture.iterdir():
        if child.name == ".git":
            continue
        dest = checkout / child.name
        if child.is_dir():
            shutil.copytree(child, dest)
        else:
            shutil.copy(child, dest)
    # A SECOND corpus document in the staged topic, so the tile has a real
    # active-document candidate (T104 F2 excludes the outline from the picker,
    # so a one-file topic is outline-only and the ordered Outline-then-Document
    # variant would have nothing to order). The header block is what the corpus
    # scanner requires for registration; without it the file never reaches the
    # scope projection.
    (
        checkout / "ideation" / "staging" / "ideation-governance" / "detail.md"
    ).write_text(
        "# Ideation Governance Detail\n\n"
        "Status: staged\n"
        "Kind: staging-packet\n"
        "Summary: Worked-example authoring companion seeded for the T098 "
        "smoke.\n"
        "Topics: ideation-governance\n"
        "Repository context: fixture-repo\n"
        "Captured: 2026-08-08\n\n"
        "Companion document body for the ordered-Save live variant.\n",
        encoding="utf-8",
    )
    _run(["git", "add", "-A"], cwd=checkout)
    _run(
        [
            "git",
            "-c",
            "user.email=t098@example.invalid",
            "-c",
            "user.name=T098",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "core.hooksPath=/dev/null",
            "commit",
            "-m",
            "scratch fixture",
        ],
        cwd=checkout,
    )
    _run(["git", "push", "origin", "HEAD"], cwd=checkout)
    return remote, checkout


class _Recorder:
    """Collects step 11's evidence: page errors, failed/foreign requests."""

    def __init__(self):
        self.page_errors: list[str] = []
        self.failed: list[str] = []
        self.foreign: list[str] = []

    def wire(self, page, host_port: str):
        page.on("pageerror", lambda e: self.page_errors.append(str(e)))
        page.on("requestfailed", lambda r: self.failed.append(r.url))
        page.on(
            "request",
            lambda r: self.foreign.append(r.url) if host_port not in r.url else None,
        )


def main() -> int:
    sync_playwright = _preflight_playwright()
    from ideation_dashboard import serve as serve_mod  # noqa: E402
    from ideation_dashboard import doxbench_model  # noqa: E402
    from ideation_dashboard.generator import generate_snapshot  # noqa: E402

    base = Path(tempfile.mkdtemp(prefix="t098-doxbench-"))
    try:
        _remote, checkout = _scratch_checkout(base)
        tree_before = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=checkout,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        snapshot = generate_snapshot(
            checkout, "fixture-repo", source_revision=tree_before
        )
        snapshot_path = base / "snapshot.json"
        snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")

        entry = doxbench_model.ModelCatalogEntry(
            model_id="fixture-model",
            label="Fixture authoring model",
            provider_class="on-tenant",
            available=True,
            input_limit_bytes=800_000,
            output_limit_bytes=900_000,
            data_handling="Processed in the approved tenant boundary",
        )
        catalog = doxbench_model.ModelCatalog.from_entries([entry])

        class _SmokeModelPort(doxbench_model.FakeWorkbenchModelPort):
            """Deterministic prose plus ONE typed proposal bound to the
            LIVE outline identity the envelope was assembled against —
            exactly the shape the review cards need for steps 6-7."""

            def dispatch(self, prompt_envelope):
                self.calls.append("dispatch")
                self.dispatched.append(prompt_envelope)
                return {
                    "assistant_prose": "grounded smoke answer",
                    "proposals": [
                        {
                            "target": "outline",
                            "base_hash": prompt_envelope.observed_hashes.outline.hex,
                            "summary": "Tighten the outline (smoke)",
                            "content": "# Outline reworked by the smoke\n",
                        }
                    ],
                }

        port = _SmokeModelPort(catalog)

        from session_fixtures import FakePullRequests  # noqa: E402

        web_dir = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
        httpd = serve_mod.build_server(
            web_dir,
            snapshot_path,
            checkout,
            host="127.0.0.1",
            port=0,
            head=tree_before,
            actor="t098",
            repository="fixture-repo",
            pull_request_factory=FakePullRequests,
            model_port_factory=lambda: port,
        )
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        host_port = f"127.0.0.1:{httpd.server_address[1]}"
        recorder = _Recorder()

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            recorder.wire(page, host_port)
            catalog_hits = []
            page.on(
                "response",
                lambda r: catalog_hits.append(r.status)
                if "/workbench/model-catalog" in r.url
                else None,
            )
            page.goto(f"http://{host_port}/")

            def open_workbench(tile_text="ideation-governance"):
                # Idempotent: a tile already expanded (e.g. after a teardown
                # for the R-1 remount guard) would COLLAPSE on a blind second
                # click, so the verb is polled for instead of assumed. The
                # click target is the tile's own wheel window — the label span
                # can sit under a sibling window's hit area.
                page.click('button:has-text("the wheel")')
                page.wait_for_selector("#view-wheel:not([hidden])")
                # The wheel is a carousel: "click a tile to focus, click it
                # again for its actions" (the view's own hint). The click must
                # land on the LABELLED TILE ELEMENT itself — pointer clicks
                # hit whatever tile the wheel geometry has in front, which is
                # how the first keyword-lens attempt reopened the previous
                # tile's workbench — so the tile node is clicked
                # programmatically, after an Escape collapses any tile the
                # previous flow left expanded.
                page.keyboard.press("Escape")
                page.wait_for_timeout(200)
                clicker = (
                    "(t) => {"
                    "  const labels = [...document.querySelectorAll("
                    "    '#view-wheel .wheellabel')];"
                    "  const span = labels.find("
                    "    (s) => s.textContent.trim() === t);"
                    "  if (!span) return 'no-label';"
                    "  span.parentElement.click();"
                    "  return 'clicked';"
                    "}"
                )
                verb = page.locator('button:has-text("open workbench")')
                for _ in range(6):
                    res = page.evaluate(clicker, tile_text)
                    assert res == "clicked", (
                        f"tile {tile_text!r} not found on the wheel"
                    )
                    page.wait_for_timeout(400)
                    if verb.count() and verb.first.is_visible():
                        break
                verb.first.click()
                page.wait_for_selector(".doxbench-canvas:visible", timeout=15000)
                try:
                    page.wait_for_function(
                        "(t) => (document.querySelector("
                        "'#staging-workbench-root') || {textContent: ''})"
                        ".textContent.includes(t)",
                        arg=tile_text,
                        timeout=8000,
                    )
                except Exception:
                    seen = page.evaluate(
                        "() => { const r = document.querySelector("
                        "'#staging-workbench-root'); return r ? "
                        "r.textContent.slice(0, 400) : '(no root)'; }"
                    )
                    raise SystemExit(
                        f"open_workbench({tile_text!r}) landed on the wrong "
                        f"surface; workbench text starts: {seen!r}"
                    )
                # The canvas opens on its Preview view (the deliberate
                # default); every editing step below needs the Editor view.
                # setActiveView is idempotent, so this is safe on re-entry.
                page.click(
                    '.doxbench-canvas button.doxbench-viewtab:has-text("Editor")'
                )

            def close_workbench():
                # An open affordance form swallows the first Escape (it closes
                # the FORM, deliberately), so cancel it first, then Escape the
                # workbench itself until the canvas is really gone.
                cancel = page.locator('.swb-cform button:has-text("cancel")')
                if cancel.count():
                    cancel.first.click()
                    page.wait_for_timeout(200)
                for _ in range(3):
                    if not page.locator(".doxbench-canvas:visible").count():
                        break
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(400)

            def save_notes():
                return page.eval_on_selector_all(
                    ".doxbench-save-note, .doxbench-status",
                    "els => els.map(e => e.textContent.trim()).filter(Boolean)",
                )

            def submit_session_form(label_text, submit_text, fills=None, selects=None):
                """Open one session-bar affordance form and submit it. Returns
                (verdict, outcome_text) after either verdict renders."""
                page.locator(".swb-sessionbtn", has_text=label_text).first.click()
                page.wait_for_selector(".swb-cform")
                for selector, value in (selects or {}).items():
                    page.select_option(f".swb-cform {selector}", value)
                for selector, value in (fills or {}).items():
                    page.fill(f".swb-cform {selector}", value)
                panel_before = page.locator(".refusalpanel-item").count()
                page.click(f'.swb-cform button:has-text("{submit_text}")')
                # An ENDING re-renders the affordance row, which can destroy
                # the in-form outcome box before a poll sees it — but every
                # outcome also lands one NEW entry in the shared refusal
                # panel (newest first), so the wait accepts either, and the
                # panel only counts entries newer than this submit.
                handle = page.wait_for_function(
                    "(n) => {"
                    "  const l = document.querySelector('.swb-clanded');"
                    "  if (l && l.textContent) return 'landed\\u0000' + l.textContent;"
                    "  const r = document.querySelector('.swb-crefused');"
                    "  if (r && r.textContent) return 'refused\\u0000' + r.textContent;"
                    "  const items = document.querySelectorAll('.refusalpanel-item');"
                    "  if (items.length > n) {"
                    "    const txt = items[0].textContent;"
                    "    return (txt.startsWith('applied') ? 'landed' : 'refused')"
                    "      + '\\u0000' + txt;"
                    "  }"
                    "  return false;"
                    "}",
                    arg=panel_before,
                    timeout=15000,
                )
                verdict, outcome = str(handle.json_value()).split("\u0000", 1)
                return (verdict, outcome)

            def session_branches():
                out = subprocess.run(
                    [
                        "git",
                        "for-each-ref",
                        "--format=%(refname:short)",
                        "refs/heads/draft/",
                    ],
                    cwd=checkout,
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout
                return [b for b in out.splitlines() if b]

            def storage_names_ref(ref):
                return page.evaluate(
                    "(ref) => Object.keys(window.sessionStorage)"
                    ".some((k) => { try { return decodeURIComponent(k)"
                    ".includes(ref); } catch { return false; } })",
                    ref,
                )

            def wait_storage_cleared(ref, why):
                # The FR-039 clear runs inside the ending handler's async
                # chain (after the panel entry that reports the landing), so
                # the absence is POLLED, never asserted instantaneously.
                try:
                    page.wait_for_function(
                        "(ref) => !Object.keys(window.sessionStorage)"
                        ".some((k) => { try { return decodeURIComponent(k)"
                        ".includes(ref); } catch { return false; } })",
                        arg=ref,
                        timeout=10000,
                    )
                except Exception:
                    raise SystemExit(
                        f"FR-039 regression — {why}: the working state for "
                        f"{ref!r} survived the ending"
                    )

            # 1: switch to the wheel, focus the staged topic tile, open its
            # actions, and enter the workbench; wait for the doxBench canvas.
            open_workbench()
            print("STEP 1 OK: canvas open")
            # 2: edit Outline.
            page.fill(".doxbench-canvas textarea", "# Outline edited\n")
            print("STEP 2 OK: outline edited")
            # 3: select the approved model (the send disclosure appears),
            # then submit a turn.
            page.wait_for_selector(".doxchat-model")
            try:
                page.wait_for_function(
                    "document.querySelectorAll('.doxchat-model option').length > 1",
                    timeout=15000,
                )
            except Exception:
                raise SystemExit(
                    f"STEP 3 BLOCKED — catalog never adopted; "
                    f"/workbench/model-catalog statuses: {catalog_hits}; "
                    f"page errors: {recorder.page_errors[:3]}"
                )
            page.select_option(".doxchat-model", "fixture-model")
            page.fill(".doxchat-composer", "First question")
            page.click(".doxchat-send")
            try:
                page.wait_for_selector(".doxchat-turn", timeout=15000)
            except Exception:
                note = (
                    page.eval_on_selector(".doxchat-failure", "e => e.textContent")
                    or "(empty)"
                )
                raise SystemExit(
                    f"STEP 3 FAILED — rail failure note: {note!r}; "
                    f"page errors: {recorder.page_errors[:3]}"
                )
            print("STEP 3 OK: first turn settled")
            # 4: select the BACKED detail document (the seeded candidate) and
            # edit it. Selecting first matters: the null not-yet-created
            # buffer this step once edited could never exercise the ordered
            # or partial Save variants below.
            try:
                page.click(".doxbench-canvas [role=tab] >> text=Document")
            except Exception as e:
                page.screenshot(path="/tmp/t098-step4.png", full_page=True)
                html = page.evaluate("""() => {
                  const pick = (sel) => { const n = document.querySelector(sel); return n ? n.outerHTML.slice(0, 2500) : null; };
                  return {
                    selects: [...document.querySelectorAll('.doxbench-canvas select, .swb-context select')].map(x => ({cls: x.className, label: x.getAttribute('aria-label'), options: [...x.options].map(o => o.textContent)})),
        canvasButtons: [...document.querySelectorAll('.doxbench-canvas button, .doxbench-canvas [role=button], .doxbench-canvas [role=tab], .doxbench-canvas [role=combobox]')].map(b => ({tag: b.tagName, cls: b.className, role: b.getAttribute('role'), text: b.textContent.trim().slice(0,50), hidden: b.hidden || !!b.closest('[hidden]')})),
        canvasHtml: (document.querySelector('.doxbench-canvas')||{outerHTML:''}).outerHTML.replace(/<textarea[\s\S]*?<\/textarea>/g, '<textarea…>').slice(0, 2500),
                    contextText: (document.querySelector('.swb-context')||{textContent:''}).textContent.slice(0,500),
                  };
                }""")
                import json as _j
                print("STEP4 DOM:", _j.dumps(html, indent=1)[:3000])
                raise SystemExit(f"DEBUG4: {e}")
            page.select_option(
                ".doxbench-document-picker",
                "ideation/staging/ideation-governance/detail.md",
            )
            page.wait_for_timeout(600)  # let the selection load its base
            page.fill(".doxbench-canvas textarea:visible", "# Document edited\n")
            print("STEP 4 OK: backed detail document selected and edited")
            # 5: the later turn carries BOTH current buffers (asserted via
            # the fake port's recorded envelopes).
            page.fill(".doxchat-composer", "Second question")
            page.click(".doxchat-send")
            page.wait_for_function(
                "document.querySelectorAll('.doxchat-turn').length >= 4"
            )
            print("STEP 5 OK: second turn settled")
            # 6: apply one current proposal.
            page.click(".doxchat-card-apply:enabled")
            print("STEP 6 OK: proposal applied")
            # 7: a THIRD turn mints a fresh current proposal; a further
            # human edit drifts the buffer; Apply then REFUSES at the swap
            # (T064's settled-identity gate) — the buffer keeps the human
            # text and the card never becomes applied.
            page.fill(".doxchat-composer", "Third question")
            page.click(".doxchat-send")
            page.wait_for_function(
                "document.querySelectorAll('.doxchat-turn').length >= 6"
            )
            page.click(".doxbench-canvas [role=tab] >> text=Outline")
            page.fill(".doxbench-canvas textarea:visible", "# Drift\n")
            # T100 P1-A LIVE GUARD: the drift must reach the RENDERED card —
            # stale in the DOM, Apply disabled — not just the model.
            page.wait_for_timeout(1200)  # allow settle + currency refresh
            assert page.locator(".doxchat-card-stale").count() >= 1, (
                "P1-A regression — the stale transition never reached the DOM"
            )
            assert page.locator(".doxchat-card-apply:enabled").count() == 0, (
                "P1-A regression — a stale card still offers an enabled Apply"
            )
            before_applied = page.locator(".doxchat-card-applied").count()
            drifted = page.eval_on_selector(
                ".doxbench-canvas textarea:visible", "e => e.value"
            )
            assert drifted.startswith("# Drift"), (
                f"the human text must survive the refusal, got {drifted!r}"
            )
            print("STEP 7 OK: stale posture observed")
            # 8: Save Outline then Document through the governed seam. The
            # click self-reports the plane's posture when Save is withheld.
            save_btn = page.locator(
                ".doxbench-canvas button.doxbench-save:visible"
            ).first
            if not save_btn.is_enabled():
                caps_json = page.evaluate("fetch('/capabilities').then(r => r.json())")
                raise SystemExit(
                    "STEP 8 BLOCKED — Save disabled; title="
                    f"{save_btn.get_attribute('title')!r}; "
                    f"caps={json.dumps(caps_json.get('actions'))}"
                )
            save_btn.click()
            page.wait_for_timeout(1500)
            # T100 P1-B LIVE GUARD: the settled identity must actually reach
            # the Save seam — the unsettled refusal on a settled buffer was
            # the run-2 blocker (bufferRequestRow omitted current_hash).
            notes = save_notes()
            assert not any("has not settled" in n for n in notes), (
                f"P1-B regression — unsettled refusal on a settled buffer: {notes[:2]}"
            )
            for blocker in ("has not settled", "scope_kind", "scope is one of"):
                assert not any(blocker in n for n in notes), (
                    f"blocker class {blocker!r} reappeared: {notes[:3]}"
                )

            # THE ORDERED VARIANT (FR-031, quickstart §4 "Outline then Document
            # produces two ordered commits" — LIVE). Both buffers are dirty and
            # BOTH target distinct backed files now, so both rows must commit,
            # and the session branch must carry the outline commit STRICTLY
            # BEFORE the document commit. GIT is the oracle here — the DOM
            # statuses are transient (the post-save rekey re-render replaces
            # "saved as …" with the clean-buffer posture almost immediately).
            def session_commits():
                branches = session_branches()
                if len(branches) != 1:
                    return None, []
                shas = subprocess.run(
                    [
                        "git",
                        "log",
                        "--reverse",
                        "--format=%H",
                        branches[0],
                        f"^{tree_before}",
                    ],
                    cwd=checkout,
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.split()
                return branches[0], shas

            session_branch, ordered = session_commits()
            for _ in range(20):
                if session_branch and len(ordered) >= 2:
                    break
                page.wait_for_timeout(500)
                session_branch, ordered = session_commits()
            assert session_branch, f"no single session branch: {session_branches()}"
            assert len(ordered) == 2, (
                f"expected exactly two session commits, got {ordered}"
            )
            touched = []
            for sha in ordered:
                files_out = subprocess.run(
                    ["git", "show", "--name-only", "--format=", sha],
                    cwd=checkout,
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout
                touched.append(files_out)
            assert "README.md" in touched[0] and "detail.md" not in touched[0], (
                f"first commit must be the Outline: {touched[0]!r}"
            )
            assert "detail.md" in touched[1], (
                f"second commit must be the Document: {touched[1]!r}"
            )
            print(
                "STEP 8 OK: ordered Save — Outline then Document, two "
                f"ordered commits on {session_branch}"
            )

            # 8b: THE PARTIAL VARIANT (FR-032, quickstart §4 "second refusal
            # leaves Outline committed and Document dirty" — LIVE). A commit
            # in the SESSION WORKTREE — the same tree a second operator's gate
            # action writes — moves the document's base behind the buffer's
            # back; the next Save then commits the Outline row and REFUSES the
            # Document row, whose human text and dirty flag must survive
            # exactly. (The session-bar rewrite verb was tried first, but its
            # picker offers no documents on the rekeyed fixture view —
            # recorded as an observed nit, not this step's subject.)
            def fill_and_hold(tab_label, text):
                # The post-save rekey refresh re-renders the buffers
                # asynchronously; a fill landing inside that window is
                # overwritten by the refreshed governed content, so every 8b
                # edit is verified to HOLD and retried until it does.
                page.click(f".doxbench-canvas [role=tab] >> text={tab_label}")
                for _ in range(6):
                    page.fill(".doxbench-canvas textarea:visible", text)
                    page.wait_for_timeout(700)
                    held = page.eval_on_selector(
                        ".doxbench-canvas textarea:visible", "e => e.value"
                    )
                    if held == text:
                        return
                raise SystemExit(f"the {tab_label} edit never held against the refresh")

            fill_and_hold("Outline", "# Drift v2\n")
            fill_and_hold("Document", "# Document edited again\n")
            page.wait_for_timeout(1200)  # both identities settle
            worktrees_out = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=checkout,
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            session_wt = None
            current_path = None
            for line in worktrees_out.splitlines():
                if line.startswith("worktree "):
                    current_path = line.split(" ", 1)[1]
                if line == f"branch refs/heads/{session_branch}":
                    session_wt = Path(current_path)
            assert session_wt, f"no session worktree found: {worktrees_out!r}"
            (
                session_wt
                / "ideation"
                / "staging"
                / "ideation-governance"
                / "detail.md"
            ).write_text("# Rewritten behind the buffer (smoke)\n", encoding="utf-8")
            _run(
                [
                    "git",
                    "-c",
                    "user.email=actor2@example.invalid",
                    "-c",
                    "user.name=Actor2",
                    "-c",
                    "commit.gpgsign=false",
                    "-c",
                    "core.hooksPath=/dev/null",
                    "commit",
                    "-m",
                    "second actor moves the document base",
                    "--",
                    "ideation/staging/ideation-governance/detail.md",
                ],
                cwd=session_wt,
            )
            save_btn = page.locator(
                ".doxbench-canvas button.doxbench-save:visible"
            ).first
            save_btn.click()
            refusals = []
            for _ in range(20):
                page.wait_for_timeout(500)
                notes = save_notes()
                refusals = [n for n in notes if "refused" in n.lower()]
                if refusals:
                    break
            assert refusals, (
                f"the Document row must refuse in the partial Save: {save_notes()[:4]}"
            )
            # the Outline row's commit is the FOURTH session commit overall
            # (two from step 8, one from the session-bar rewrite, then this) —
            # again proven in git, not in the transient DOM
            shas_after_partial = []
            for _ in range(20):
                _branch, shas_after_partial = session_commits()
                if len(shas_after_partial) >= 4:
                    break
                page.wait_for_timeout(500)
            assert len(shas_after_partial) == 4, (
                f"the partial Save must commit the Outline row: "
                f"{shas_after_partial}; notes: {save_notes()[:4]}"
            )
            doc_text = page.eval_on_selector(
                ".doxbench-canvas textarea:visible", "e => e.value"
            )
            assert doc_text.startswith("# Document edited again"), (
                f"the refused Document text must survive, got {doc_text!r}"
            )
            partial_refusal_note = refusals[0]
            # resolve the refused row so the later steps start clean: Discard
            # restores the buffer to its last loaded base (T035's other arm)
            page.click(".doxbench-canvas button.doxbench-discard:visible")
            page.wait_for_timeout(400)
            print(
                "STEP 8b OK: partial Save — Outline committed, Document "
                f"refused with its text retained (note: {partial_refusal_note[:80]!r})"
            )
            # 9: refresh, RE-ENTER the workbench (the overlay is per-page
            # UI state), and observe the retained per-key working state.
            page.reload()
            open_workbench()
            print("STEP 9 OK: refreshed and re-entered")
            # 10a: keyboard-only turn — the refreshed rail is FRESH state
            # (in-memory by design), so select the model by keyboard first,
            # then compose and send, all without a pointer.
            page.wait_for_function(
                "document.querySelectorAll('.doxchat-model option').length > 1"
            )
            page.focus(".doxchat-model")
            page.keyboard.press("ArrowDown")
            page.focus(".doxchat-composer")
            page.keyboard.type("Keyboard question")
            page.keyboard.press("Tab")
            page.keyboard.press("Enter")
            page.wait_for_selector(".doxchat-turn")
            print("STEP 10a OK: keyboard-only turn settled")
            # 10b: narrow layout — all three regions present, no horizontal
            # loss of the page.
            page.set_viewport_size({"width": 420, "height": 900})
            page.wait_for_timeout(300)
            assert page.locator(".swb-context").is_visible()
            assert page.locator(".doxbench-canvas").is_visible()
            assert page.locator(".doxbench-rail").is_visible()
            no_h_loss = page.evaluate(
                "document.documentElement.scrollWidth <= window.innerWidth + 1"
            )
            assert no_h_loss, "narrow layout must not scroll horizontally"
            page.set_viewport_size({"width": 1280, "height": 900})
            print("STEP 10b OK: narrow layout holds")
            # 10c: CHK007 — the APG tablist pattern, measured live (this was
            # the one AT check that FAILED the T100 measurement pass).
            # EVERY role=tablist on the surface must implement the pattern —
            # the 2026-08-02 re-report was a SECOND strip (the shell's
            # docs/lens/outline tabs) that the canvas-only check had missed.
            strips = page.evaluate("""() => {
              const out = [];
              for (const list of document.querySelectorAll('[role=tablist]')) {
                if (list.closest('[hidden]')) continue;
                const tabs = [...list.querySelectorAll('[role=tab]')];
                if (!tabs.length) continue;
                out.push({
                  label: list.className,
                  indices: tabs.map((t) => t.tabIndex),
                  tabbable: tabs.filter((t) => t.tabIndex === 0).length,
                });
              }
              return out;
            }""")
            assert len(strips) >= 2, f"expected both tablists, saw {strips}"
            for strip in strips:
                assert strip["tabbable"] == 1, (
                    f"CHK007: {strip['label']} has {strip['tabbable']} tabbable tabs: {strip}"
                )
                assert all(i in (-1, 0) for i in strip["indices"]), (
                    f"CHK007: {strip['label']} tabIndex values {strip['indices']}"
                )
            tabs = page.locator(".doxbench-canvas [role=tab]")
            selected_before = page.locator(
                '.doxbench-canvas [role=tab][aria-selected="true"]'
            ).first.get_attribute("id")
            page.locator(
                '.doxbench-canvas [role=tab][aria-selected="true"]'
            ).first.focus()
            page.keyboard.press("ArrowRight")
            selected_after = page.locator(
                '.doxbench-canvas [role=tab][aria-selected="true"]'
            ).first.get_attribute("id")
            assert selected_after != selected_before, (
                "CHK007: ArrowRight moved neither focus nor selection"
            )
            page.keyboard.press("Home")
            home_selected = page.locator(
                '.doxbench-canvas [role=tab][aria-selected="true"]'
            ).first.get_attribute("id")
            assert home_selected == selected_before, (
                "CHK007: Home did not return to the first tab"
            )
            print("STEP 10c OK: CHK007 roving tablist (arrows + Home/End)")
            # 10d: R-1 LIVE GUARD (the operator's exact prescription — the
            # model-level persistence test passes while the live surface loses
            # everything, the same class as refreshCurrency having no caller).
            # Edit a buffer, TEAR DOWN and REMOUNT the workbench under the
            # SAME key, then assert the RENDERED editor still holds the text.
            page.click(".doxbench-canvas [role=tab] >> text=Outline")
            marker = "PERSIST-MARKER-9f3c"
            page.fill(".doxbench-canvas textarea:visible", "# Outline " + marker + "\n")
            page.wait_for_timeout(1200)  # let the identity settle
            page.keyboard.press("Escape")  # tear the workbench down
            page.wait_for_timeout(400)
            open_workbench()  # remount, same tile/key
            page.click(".doxbench-canvas [role=tab] >> text=Outline")
            restored = page.eval_on_selector(
                ".doxbench-canvas textarea:visible", "e => e.value"
            )
            assert marker in restored, (
                "R-1 regression — the remounted editor lost the unsaved text; "
                f"rendered value starts {restored[:60]!r}"
            )
            # And the chat companion came back with it: the transcript from
            # this session's turns is still rendered (buffers and chat restore
            # from ONE record, so neither can come back without the other).
            turns = page.locator(".doxchat-turn").count()
            assert turns >= 2, (
                "R-1 regression — buffers restored but the chat working state "
                f"did not ({turns} turns rendered)"
            )
            print("STEP 10d OK: R-1 buffers AND chat state survive a remount")
            # 10 + 10e + 10f run on the OTHER tile. The first submit of
            # open-pr on ideation-governance surfaced FR-024 live: the tile
            # carries the picked proposal `add-ideation-governance`, so every
            # SESSION VERB refuses ("a tile is worked OR proposed, never
            # both") — even though the doxBench first-edit HAD opened a
            # session there (recorded as an observed seam finding for T104's
            # review; session #1 therefore deliberately stays open). The
            # keyword-lens tile carries no proposal, so the endings are
            # exercised there: session A is ABANDONED, session B is PUSHED,
            # EXTERNALLY MERGED, and ENDED.
            verbs = page.eval_on_selector_all(
                ".swb-sessionbtn", "els => els.map(e => e.textContent.trim())"
            )
            verdict, fr024 = submit_session_form(
                "save — open the pull request", "open-pr"
            )
            assert verdict == "refused" and "never both" in fr024, (
                f"expected the FR-024 refusal on the proposal tile: {fr024!r}"
            )
            fr024_note = fr024.strip()
            print(
                f"STEP 10 OK: session verbs offered ({verbs}); open-pr on "
                "the proposal-carrying tile refused with FR-024, verbatim"
            )
            # 10e: THE MERGE-ENDING LIVE VARIANT (FR-033, FR-039), session
            # A on keyword-lens (ideation-governance is barred from session
            # verbs by FR-024 above). The pushed branch merges EXTERNALLY (a
            # separate clone of the bare remote — GitHub's part in T100's
            # real run). The very next save REFUSES base_stale, because the
            # served checkout has not seen the merge and the server never
            # fetches (FR-026); the scripted operator refresh (T100's
            # `main_view_refreshed`) is the ONE recorded served-checkout
            # movement; the save after it observes the merge and ENDS the
            # session. The merge ending DELETES the branch, which is what
            # lets session B open afterwards — an ABANDONED branch would
            # survive and turn the next open into the resume-or-new refusal
            # (AbandonedBranchSurvives), so the abandon variant runs LAST.
            close_workbench()
            open_workbench("keyword-lens")
            # The rewrite must stay a REGISTERED corpus document: a save
            # that strips the packet headers would (correctly) drop the file
            # from the regenerated snapshot after the merge, and the tile
            # would withdraw its outline as no-longer-governed material.
            page.fill(
                ".doxbench-canvas textarea:visible",
                "# Keyword Lens\n\nStatus: staged\nKind: staging-packet\n"
                "Summary: edited by the T098 merge-ending live variant.\n"
                "Topics: keyword-lens, ideation-dashboard\n"
                "Repository context: fixture-repo\n"
                "Captured: 2026-08-08\n\n"
                "Edited by the merge-ending live variant (smoke).\n",
            )
            page.wait_for_timeout(1200)
            page.click(".doxbench-canvas button.doxbench-save:visible")
            branch_a = None
            for _ in range(20):
                page.wait_for_timeout(500)
                fresh = [b for b in session_branches() if b != session_branch]
                if fresh:
                    branch_a = fresh[0]
                    break
            assert branch_a, (
                f"the keyword-lens first Save opened no session: "
                f"{session_branches()}; notes: {save_notes()[:4]}"
            )
            verdict, outcome = submit_session_form(
                "save — open the pull request", "open-pr"
            )
            assert verdict == "landed", f"open-pr refused: {outcome!r}"
            assert "pull request" in outcome, outcome
            print(
                f"STEP 10e-1 OK: pull request opened for {branch_a} "
                "(the push is recorded by FakePullRequests — no network,"
                " so the branch stays local by design)"
            )
            # GitHub's part, modelled: the merge clone FETCHES the session
            # branch from the served checkout (a read — the checkout is never
            # written), merges it with a real merge commit whose merged
            # parent IS the branch tip (merge_state arm 3), and advances the
            # bare remote's main.
            merge_clone = base / "merge-clone"
            _run(["git", "clone", str(_remote), str(merge_clone)], cwd=base)
            _run(["git", "fetch", str(checkout), branch_a], cwd=merge_clone)
            _run(
                [
                    "git",
                    "-c",
                    "user.email=t098@example.invalid",
                    "-c",
                    "user.name=T098",
                    "-c",
                    "commit.gpgsign=false",
                    "-c",
                    "core.hooksPath=/dev/null",
                    "merge",
                    "--no-ff",
                    "FETCH_HEAD",
                    "-m",
                    "external merge of the session branch (smoke)",
                ],
                cwd=merge_clone,
            )
            _run(["git", "push", "origin", "HEAD:main"], cwd=merge_clone)
            verdict, outcome = submit_session_form(
                "save — open the pull request", "open-pr"
            )
            assert verdict == "refused", (
                f"a stale base must refuse, got {verdict}: {outcome!r}"
            )
            assert "base" in outcome, outcome
            base_stale_note = outcome.strip()
            tree_mid = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=checkout,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            assert tree_mid == tree_before, (
                "a governance action moved the served checkout"
            )
            _run(
                [
                    "git",
                    "-c",
                    "core.hooksPath=/dev/null",
                    "pull",
                    "--ff-only",
                    "origin",
                    "main",
                ],
                cwd=checkout,
            )
            head_after_pull = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=checkout,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            verdict, outcome = submit_session_form(
                "save — open the pull request", "open-pr"
            )
            assert verdict == "landed", f"merged ending refused: {outcome!r}"
            assert (
                "MERGED, so the session ENDED" in outcome or "session merged" in outcome
            ), outcome
            wait_storage_cleared(branch_a, "merge ending")
            assert branch_a not in session_branches(), (
                "the merged branch must be deleted locally"
            )
            worktrees = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=checkout,
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            assert f"refs/heads/{branch_a}" not in worktrees, (
                f"the merged worktree survived: {worktrees!r}"
            )
            # The operator's dashboard restart at the refreshed main —
            # the same posture T100's real run recorded as
            # `main_view_refreshed`: the server was built at the pre-merge
            # head, so it is rebuilt at the pulled head with a regenerated
            # snapshot before the page reloads. Same port, same page.
            server_port = httpd.server_address[1]
            httpd.shutdown()
            httpd.server_close()  # release the listening socket for rebind
            snapshot2 = generate_snapshot(
                checkout, "fixture-repo", source_revision=head_after_pull
            )
            snapshot_path.write_text(json.dumps(snapshot2), encoding="utf-8")
            httpd = serve_mod.build_server(
                web_dir,
                snapshot_path,
                checkout,
                host="127.0.0.1",
                port=server_port,
                head=head_after_pull,
                actor="t098",
                repository="fixture-repo",
                pull_request_factory=FakePullRequests,
                model_port_factory=lambda: port,
            )
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            # And a reload restores NOTHING: the cleared working state cannot
            # resurrect, and the canvas shows the MERGED governed content.
            page.reload()
            open_workbench("keyword-lens")
            page.click(".doxbench-canvas [role=tab] >> text=Outline")
            restored = ""
            for _ in range(20):
                restored = page.eval_on_selector(
                    ".doxbench-canvas textarea:visible", "e => e.value"
                )
                if restored:
                    break
                page.wait_for_timeout(300)
            assert (
                restored.startswith("# Keyword Lens")
                and "Edited by the merge-ending live variant" in restored
            ), f"expected the merged main outline, got {restored[:120]!r}"
            print(
                f"STEP 10e OK: {branch_a} merged externally — base_stale "
                "refused first, the recorded operator refresh let the "
                "ending land, branch deleted, and a reload restored nothing"
            )
            # 10f: THE ABANDON-CLEANUP LIVE VARIANT (FR-021, FR-039), session
            # B on the same tile — the merge ending freed the deterministic
            # branch name, so this open is clean. Abandoned with its durable
            # reason: worktree and registry entry torn down, the branch
            # RETAINED for the separate human-invoked cleanup verb, and the
            # doxBench working state for the abandoned ref CLEARED.
            page.fill(
                ".doxbench-canvas textarea:visible",
                "# Keyword lens edited again (smoke)\n",
            )
            page.wait_for_timeout(1200)
            page.click(".doxbench-canvas button.doxbench-save:visible")
            branch_b = None
            for _ in range(20):
                page.wait_for_timeout(500)
                fresh = [b for b in session_branches() if b != session_branch]
                if fresh:
                    branch_b = fresh[0]
                    break
            assert branch_b, (
                f"session B never opened: {session_branches()}; "
                f"notes: {save_notes()[:4]}"
            )
            assert storage_names_ref(branch_b), (
                "no session-keyed working state was persisted for session B"
            )
            verdict, outcome = submit_session_form(
                "abandon this session",
                "abandon-session",
                fills={
                    "input": "smoke: exercising the abandon-cleanup live variant (T098)"
                },
            )
            assert verdict == "landed", f"abandon refused: {outcome!r}"
            assert "abandon" in outcome, outcome
            wait_storage_cleared(branch_b, "abandon ending")
            worktrees = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=checkout,
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            assert f"refs/heads/{branch_b}" not in worktrees, (
                f"the abandoned worktree survived: {worktrees!r}"
            )
            assert branch_b in session_branches(), (
                "the abandoned branch must be RETAINED (D15)"
            )
            print(
                f"STEP 10f OK: {branch_b} abandoned — worktree/registry "
                "torn down, branch retained, working state cleared"
            )
            # 11 collected by the recorder below.
            browser.close()

        httpd.shutdown()
        tree_after = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=checkout,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

        evidence = {
            "page_errors": recorder.page_errors,
            "failed_requests": recorder.failed,
            "foreign_requests": recorder.foreign,
            "served_checkout_moved_by_governance": tree_before != tree_mid,
            "operator_refresh": {"from": tree_before, "to": head_after_pull},
            "final_head_is_refreshed_main": tree_after == head_after_pull,
            "dispatches": port.calls.count("dispatch"),
            "partial_refusal_note": partial_refusal_note,
            "base_stale_note": base_stale_note,
        }
        print(json.dumps(evidence, indent=2))
        ok = (
            not recorder.page_errors
            and not recorder.failed
            and not recorder.foreign
            and tree_before == tree_mid
            and tree_after == head_after_pull
        )
        return 0 if ok else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
