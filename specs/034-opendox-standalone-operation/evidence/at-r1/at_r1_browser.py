"""AT-R1, the browser half (plan 034 T096): quickstart.md § 4, driven with
Playwright against the server § 3 started, with the verdict computed by
openDox-code's own `tests/smoke_signals.py` oracle.

For openxFactory `specs/034-opendox-standalone-operation/evidence/at-r1/`.
Lane openxfactory-4 wrote it for its t096-dry run; lane openXfactory-3
(slice D6) adapted it for T096's own run. It is bookkeeping, so it carries
no `Arc:` trailer (R1Q20 (a)).

It follows the plan's text on `main`: quickstart.md § 4 and T096, as
openxFactory#1222 amended them (batch N: the page is opened through the
private copy, `5963851934`) and #1225 (what "both editors stay usable"
means, RULED `5971834845`: each editor opens and accepts edits, while create
and Save are refused by name on standalone). On a standalone plane, T102's
by-scope posture offers no create control at all, and its plane note names
both: "creating one and Save need the create gate ... so Save is refused by
name". So this driver checks the create half as that absence plus that note,
and the Save half as the click's refusal by name.

Run it with the Playwright venv's python, with the server from § 3 running:

    python at_r1_browser.py --port P --label a|b --out DIR \
        --odc <openDox-code checkout at the commit under test> \
        --copy "$OPENDOX_STATE_DIR/console/$PORT.html" \
        [--copy-url <the file:// URL the start printed>]

With `--copy-url`, the page is opened through exactly the URL the start
printed (quickstart.md § 4 step 1), which must name the same file as
`--copy`. Without it, the URL is `--copy`'s own `file://` form.

It exits 0 only when every check below passes; 1 otherwise; 2 when it
could not reach a verdict. Every console error, pageerror, failed request
and 4xx/5xx is also recorded with the step it happened in
(<label>-result.json), so a failure names where it happened.

The oracle verdict is computed twice over the SAME collected signals:
  * RAW: no declarations at all (what an undeclared run sees);
  * DECLARED: with DECLARATIONS below, each a server answer a standalone
    install gives by a cited product decision.
The falsifier is DECLARED plus zero pageerror, which cannot be declared at all.
"""
from __future__ import annotations

import argparse
import html as htmlmod
import json
import os
import re
import stat
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--port", required=True, type=int)
ap.add_argument("--label", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--odc", required=True, help="the openDox-code checkout under test")
ap.add_argument("--copy", required=True, help="the private copy the start wrote")
ap.add_argument("--copy-url", default=None,
                help="the file:// URL the start printed for the private copy")
a = ap.parse_args()
OUT = Path(a.out)
OUT.mkdir(parents=True, exist_ok=True)
BASE = f"http://127.0.0.1:{a.port}"
sys.path.insert(0, str(Path(a.odc) / "tests"))
import smoke_signals  # noqa: E402  (stdlib-only oracle module, from the commit under test)
import yaml  # noqa: E402

GATELESS_SAVE_WORDS = "Save needs the first-edit transport"   # staging-workbench-model.js GATELESS_SAVE_REFUSAL
NO_MODEL_WORDS = "no model configured"
HOW_TO_CONFIGURE = "model-binding add"
# staging-workbench-model.js `scopeEditingNote()`, the by-scope plane note
# (T102): it names creating a document AND Save as needing the create gate.
CREATE_NAMED_WORDS = "creating one and Save need the create gate"
SAVE_NAMED_WORDS = "Save is refused by name"
SCOPE_PILL_WORDS = "editing by scope"
EDIT_MARK = " T096 edit"

STEP = ["load"]
RAIL_SWITCHES = [0]
events: list[dict] = []
checks: dict[str, dict] = {}


def ev(kind, **kw):
    kw.update(kind=kind, step=STEP[0], t=round(time.time(), 3))
    events.append(kw)


def check(name, ok, **evidence):
    checks[name] = {"result": "PASS" if ok else "FAIL", **evidence}
    print(f"[{checks[name]['result']}] {name}: {json.dumps(evidence, default=str)[:700]}", flush=True)


def shot(page, name):
    p = OUT / f"{a.label}-{name}.png"
    try:
        page.screenshot(path=str(p), full_page=True)
    except Exception as exc:  # a screenshot is evidence, never the verdict
        return f"(screenshot failed: {exc!r})"
    return p.name


def http(method, path, body=None, headers=None):
    req = urllib.request.Request(BASE + path, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def read_private_copy(copy: str, port: int) -> str:
    """quickstart.md § 3 as openxFactory#1222 amends it: the token is read
    from the private copy, never from /capabilities."""
    for path, mode in ((os.path.dirname(copy), 0o700), (copy, 0o600)):
        info = os.lstat(path)
        assert info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == mode, \
            f"{path} is not this user's own, mode {mode:o}"
    assert stat.S_ISREG(os.lstat(copy).st_mode), "the private copy is not a regular file"
    text = open(copy, encoding="utf-8").read()
    # quickstart.md § 3 on main: every "console_token=" in the copy opens a
    # fragment, none follows "?", "&" or "&amp;", and none starts the file
    assert all(m.start() > 0 and text[m.start() - 1] == "#" for m in re.finditer("console_token=", text)), \
        "the private copy puts the token outside a fragment"
    target = re.search(r"""(?i)http-equiv=["']?refresh["']?\s+content=["']\s*\d+\s*;\s*url=([^"']+)""", text)
    assert target, "the private copy forwards to no page"
    url = urllib.parse.urlsplit(htmlmod.unescape(target.group(1)))
    assert (url.scheme, url.netloc, url.path, url.query) == ("http", f"127.0.0.1:{port}", "/index.html", ""), \
        "the private copy does not forward to this server's /index.html with an empty query"
    token = urllib.parse.parse_qs(url.fragment).get("console_token", [""])[0]
    assert token, "the opened URL carries no token in its fragment"
    return token


def opened_through(copy: str, copy_url: str | None) -> str:
    """The `file://` URL the drive opens: the one the start printed, which
    must name this same private copy, or else the copy's own `file://`."""
    if not copy_url:
        return Path(copy).as_uri()
    parts = urllib.parse.urlsplit(copy_url)
    assert parts.scheme == "file" and parts.netloc in ("", "localhost") \
        and not parts.query and not parts.fragment, \
        "the printed console URL is not a plain file:// URL"
    named = urllib.parse.unquote(parts.path)
    assert os.path.samefile(named, copy), \
        "the printed console URL does not name the private copy"
    assert "console_token" not in copy_url, "the printed console URL carries the token"
    return copy_url


try:
    TOKEN = read_private_copy(a.copy, a.port)
    OPEN_URL = opened_through(a.copy, a.copy_url)
    st, body = http("GET", "/snapshot.json")
    snap = json.loads(body)
    st, body = http("GET", "/capabilities")
    caps = json.loads(body)
    assert "console_token" not in caps, "/capabilities still carries the console token (T104)"
except Exception as exc:  # no verdict can be reached: say so, never a PASS
    print(f"AT-R1 browser half ({a.label}): ERROR before the drive: {exc!r}")
    sys.exit(2)

# ---- what the snapshot fills, station by station (the display facet's map) --
fields = caps["display"]["fields"]
filled = {}
for role in caps["display"]["stage_order"]:
    f = fields[role]
    items = snap.get(f["field"]) or []
    if f.get("status"):
        items = [i for i in items if i.get("status") == f["status"]]
    filled[role] = len(items)
print("snapshot fills:", filled, flush=True)

raw = smoke_signals.Errors()
save_step_signals: dict = {}

BROWSER_VERSION = [None]
with sync_playwright() as p:
    browser = p.chromium.launch()
    BROWSER_VERSION[0] = browser.version
    print(f"browser: chromium {browser.version}", flush=True)
    ctx = browser.new_context(viewport={"width": 1500, "height": 1000})
    page = ctx.new_page()
    raw.wire(page)
    page.on("pageerror", lambda e: ev("pageerror", message=str(e), stack=getattr(e, "stack", None)))
    page.on("console", lambda m: ev("console_" + m.type, text=m.text, location=m.location)
            if m.type in ("error", "warning") else None)
    page.on("requestfailed", lambda r: ev("requestfailed", method=r.method, url=r.url, failure=r.failure))
    page.on("response", lambda r: ev("http_" + str(r.status), method=r.request.method, url=r.url)
            if r.status >= 400 else None)
    page.on("request", lambda r: ev("request", method=r.method, url=r.url))

    def section(name, fn):
        STEP[0] = name
        try:
            fn()
        except Exception as exc:  # a driver failure is a FAIL of that step, recorded
            check(f"{name}: the driver completed the step", False, error=repr(exc),
                  trace=traceback.format_exc()[-1500:])
            shot(page, f"{name}-driver-failure")

    # ---- 1. load, through the private copy (§ 4 step 1, #1222) --------------
    def s_load():
        page.goto(OPEN_URL)
        page.wait_for_url(re.compile(r"^" + re.escape(BASE) + r"/index\.html"), timeout=20000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        url_now = page.url
        check("load: the private copy opens the console page on loopback",
              url_now.startswith(BASE + "/index.html"), url=url_now.split("#")[0],
              opened_through=OPEN_URL, printed_url_used=bool(a.copy_url),
              title=page.title(), screenshot=shot(page, "1-load"))
        check("load: the token is stripped from the address bar",
              "console_token" not in url_now, url_has_fragment="#" in url_now)
    section("load", s_load)

    # ---- 2. wheel -----------------------------------------------------------
    def s_wheel():
        page.click("#tab-wheel")
        page.wait_for_timeout(1500)
        per = page.eval_on_selector_all(
            "#view-wheel .wheeltile:not(.wheelblank)",
            "els => { const o = {}; for (const e of els) { const k = e.dataset.wheel;"
            " (o[k] = o[k] || new Set()).add(e.dataset.index); }"
            " return Object.fromEntries(Object.entries(o).map(([k, v]) => [k, v.size])); }")
        labels = page.eval_on_selector_all(
            "#view-wheel .wheeltile:not(.wheelblank)",
            "els => els.map(e => [e.dataset.wheel, e.dataset.index, (e.querySelector('.wheellabel')||{}).textContent])")
        missing = [r for r, n in filled.items() if n and not per.get(r)]
        short = {r: [per.get(r, 0), n] for r, n in filled.items() if n and per.get(r, 0) < n}
        check("wheel: a tile for every station the snapshot fills", not missing and not short,
              filled=filled, tiles_per_station=per, missing=missing,
              fewer_tiles_than_items=short, screenshot=shot(page, "2-wheel"))
        (OUT / f"{a.label}-wheel-tiles.json").write_text(json.dumps(labels, indent=1))
    section("wheel", s_wheel)

    # ---- 3. lens ------------------------------------------------------------
    def s_lens():
        page.click("#tab-lens")
        page.wait_for_timeout(1500)
        svg = page.locator("#view-lens svg.bullseye")
        dots0 = page.locator("#view-lens svg.bullseye g.lensdot").count()
        text0 = page.inner_text("#view-lens")
        first = shot(page, "3a-lens-on-open")
        seeds0 = page.eval_on_selector_all("#view-lens [data-seed-action]", "els => els.map(e => e.dataset.seedAction)")
        # the dots need checked keywords: check every keyword ("all")
        more = page.locator("#view-lens button.railmore")
        solos = more.first.inner_text() if more.count() else None
        if more.count() and more.first.inner_text().startswith("show"):
            more.first.click()
            page.wait_for_timeout(800)
        allbtn = page.locator("#view-lens button", has_text="all")
        if allbtn.count():
            allbtn.first.click()
            page.wait_for_timeout(1500)
        dots = page.eval_on_selector_all("#view-lens svg.bullseye g.lensdot", "els => els.map(e => e.dataset.doc)")
        text1 = page.inner_text("#view-lens")
        seeds1 = page.eval_on_selector_all("#view-lens [data-seed-action]", "els => els.map(e => [e.dataset.seedAction, e.textContent])")
        seedwords = [w for w in ("draft seed", "draft staging seed", "re-draft") if w in text1.lower()]
        pickcol = page.locator("#view-lens th.pickcol").count()
        docs = sorted(d.get("path") or d.get("id") or "" for d in snap.get("documents") or [])
        second = shot(page, "3b-lens-all-checked")
        check("lens: the bullseye renders", svg.count() == 1,
              dots_on_open=dots0, on_open_says_check_a_keyword="check a keyword" in text0.lower(),
              screenshot=first)
        check("lens: the documents render as dots",
              len(dots) > 0 and len(set(dots)) == len(dots) and set(dots) == set(docs),
              dots=len(dots), distinct=len(set(dots)), documents=len(docs),
              missing_docs=sorted(set(docs) - set(dots)), extra_dots=sorted(set(dots) - set(docs)),
              solo_toggle=solos, screenshot=second)
        check("lens: the text 'nothing on the radar' is absent",
              "nothing on the radar" not in text0.lower() and "nothing on the radar" not in text1.lower())
        check("lens: neither seed action is offered (R1Q19 (a))",
              not seeds0 and not seeds1 and not seedwords and pickcol == 0,
              seed_controls_on_open=seeds0, seed_controls_all_checked=seeds1,
              seed_words=seedwords, selection_column=pickcol)
        offered = page.eval_on_selector_all(
            "#view-lens button", "els => els.filter(e => e.offsetParent).map(e => [e.textContent.trim().slice(0,50), e.disabled])")
        (OUT / f"{a.label}-lens-controls.json").write_text(json.dumps(offered, indent=1))
    section("lens", s_lens)

    # ---- 4. chat, from a grouping tile's workbench verb ---------------------
    R = "#staging-workbench-root"

    def controls():
        return page.eval_on_selector_all(
            f"{R} button, {R} textarea, {R} input, {R} select, {R} [contenteditable]",
            "els => els.map(e => ({tag: e.tagName, cls: e.className, text: (e.textContent||'').trim().slice(0,60),"
            " title: (e.title||'').slice(0,160), disabled: !!e.disabled, visible: !!e.offsetParent,"
            " ro: !!e.readOnly, aria: e.getAttribute('aria-label')}))")

    def s_chat():
        page.click("#tab-wheel")
        page.wait_for_timeout(1200)
        tiles = page.locator("#view-wheel .wheeltile[data-wheel='grouping']:not(.wheelblank)")
        n = tiles.count()
        check("chat: the repository yields a grouping tile (fails, never skips)", n > 0, grouping_tiles=n)
        if not n:
            return
        tile = tiles.first
        label = tile.locator(".wheellabel").inner_text()
        tile.click()
        page.wait_for_timeout(1500)
        focused = page.locator("#view-wheel .wheeltile.wheelfocused[data-wheel='grouping']")
        if focused.count():
            focused.first.click()
            page.wait_for_timeout(1200)
        verbs = page.eval_on_selector_all(
            "#view-wheel .wheelactions button",
            "els => els.map(e => [e.textContent.trim(), e.title, e.disabled])")
        shot(page, "4a-wheel-grouping-verbs")
        wb = page.locator("#view-wheel .wheelactions button[title^='open the staging workbench']")
        check("chat: the grouping tile offers an enabled workbench verb",
              wb.count() > 0 and not wb.first.is_disabled(), tile=label, verbs=verbs)
        if not wb.count() or wb.first.is_disabled():
            return
        wb.first.click()
        page.wait_for_timeout(3000)
        root = page.locator(R)
        opened = root.count() > 0 and root.inner_text().strip() != ""
        (OUT / f"{a.label}-workbench-text.txt").write_text(root.inner_text() if root.count() else "")
        (OUT / f"{a.label}-workbench-controls.json").write_text(json.dumps(controls(), indent=1))
        check("chat: the staging workbench opens", opened, screenshot=shot(page, "4b-workbench-open"))
        if not opened:
            return
        # BEFORE any turn: the rail's "no model configured" state, with how to configure one
        page.wait_for_timeout(1500)
        notes = page.eval_on_selector_all(
            ".doxchat-no-model", "els => els.map(e => ({hidden: e.hidden, visible: !!e.offsetParent, text: e.textContent}))")
        vis = [x for x in notes if x["visible"] and not x["hidden"]]
        turns_before = [e for e in events if e["kind"] == "request" and "chat-turn" in e["url"]]
        check("chat: before any turn, the rail shows 'no model configured', naming how to configure one",
              bool(vis) and NO_MODEL_WORDS in vis[0]["text"].lower() and HOW_TO_CONFIGURE in vis[0]["text"]
              and not turns_before,
              no_model_notes=notes, turns_before=len(turns_before), screenshot=shot(page, "4c-chat-no-model"))
        # a turn: through the rail, as a human would
        STEP[0] = "chat-turn"
        composer = page.locator(f"{R} textarea.doxchat-composer").first
        send = page.locator(f"{R} button.doxchat-send").first
        rail = {"composer": composer.count(), "send": send.count()}
        if composer.count():
            rail["composer_enabled"] = composer.is_enabled()
            rail["composer_visible"] = composer.is_visible()
            if composer.is_enabled() and composer.is_visible():
                composer.fill("Summarise this grouping, please.")
        turn_responses: list = []

        def on_resp(r):
            if "chat-turn" in r.url:
                try:
                    turn_responses.append({"status": r.status, "body": r.json()})
                except Exception:
                    turn_responses.append({"status": r.status, "body": None})
        page.on("response", on_resp)
        if send.count():
            rail["send_disabled"] = send.is_disabled()
            desc = send.get_attribute("aria-describedby")
            rail["send_title"] = send.get_attribute("title")
            if desc:
                d = page.locator("#" + desc)
                rail["send_description"] = d.first.text_content() if d.count() else None
            if not send.is_disabled():
                send.click()
                page.wait_for_timeout(2500)
        rail["ui_turn_responses"] = turn_responses
        rail["after_text_tail"] = page.locator(R).inner_text()[-1200:]
        # and as any client can: the schema-valid example turn, from OUTSIDE the
        # page (so the oracle's browser channels are not touched by it)
        ex = yaml.safe_load((Path(a.odc) / "tests/fixtures/spec-examples/workbench-chat-turn-v2-loaded-set.example.yaml").read_text())
        st, body = http("POST", "/actions/workbench/chat-turn", json.dumps(ex).encode(),
                        {"Content-Type": "application/json", "X-XF-Console-Token": TOKEN})
        try:
            body = json.loads(body)
        except Exception:
            body = body[:400].decode("utf-8", "replace")
        http_refused = isinstance(body, dict) and body.get("error") == "model_capability_unavailable" and 400 <= st < 500
        ui_refused = any(isinstance(r.get("body"), dict) and r["body"].get("error") == "model_capability_unavailable"
                         for r in turn_responses)
        ui_withheld = rail.get("send_disabled") is True
        check("chat: a turn is refused model_capability_unavailable",
              http_refused and (ui_refused or ui_withheld),
              http_status=st, http_error=(body.get("error") if isinstance(body, dict) else body),
              ui_refused=ui_refused, ui_send_withheld=ui_withheld, ui=rail,
              screenshot=shot(page, "4d-chat-after-turn"))
        STEP[0] = "chat"

        # ---- both editors stay usable: each opens and accepts edits (5971834845)
        STEP[0] = "editors"
        ed: dict = {"buffers": {}}

        def editor_tab():
            t = page.locator(R + " button.doxbench-viewtab", has_text="Editor")
            if t.count():
                t.first.click()
                page.wait_for_timeout(400)
            return t.count()

        def buffer_textareas():
            return page.eval_on_selector_all(
                f"{R} textarea[aria-label$=' buffer text']",
                "els => els.map(e => ({aria: e.getAttribute('aria-label'), visible: !!e.offsetParent,"
                " disabled: !!e.disabled, ro: !!e.readOnly, len: e.value.length}))")

        def type_into(aria):
            res: dict = {}
            ta = page.locator(f"{R} textarea[aria-label='{aria}']")
            res["present"] = ta.count()
            if not ta.count():
                return res
            ta = ta.first
            res["visible"] = ta.is_visible()
            res["enabled"] = ta.is_enabled()
            res["readonly"] = ta.evaluate("e => e.readOnly")
            if res["visible"] and res["enabled"] and not res["readonly"]:
                before = ta.input_value()
                ta.click()
                page.keyboard.press("Control+End")
                page.keyboard.type(EDIT_MARK)
                page.wait_for_timeout(400)
                after = ta.input_value()
                res["typed"] = after != before and after.endswith(EDIT_MARK)
            return res

        ed["editor_tabs"] = editor_tab()
        ed["textareas_on_open"] = buffer_textareas()
        # load the tile's own documents through the docs tile's `edit` verb
        doctiles = page.locator(R + " .wheeltile:not(.wheelblank)")
        ed["doc_tiles"] = doctiles.count()
        loaded = 0
        for i in range(min(doctiles.count(), 8)):
            if loaded >= 2:
                break
            t = doctiles.nth(i)
            for _ in range(2):
                if t.locator("button.swb-docload").count():
                    break
                t.click()
                page.wait_for_timeout(900)
            btn = t.locator("button.swb-docload")
            if btn.count() and not btn.first.is_disabled() and btn.first.inner_text().strip() == "edit":
                btn.first.click()
                page.wait_for_timeout(2000)
                loaded += 1
        ed["documents_loaded_via_edit_verb"] = loaded
        editor_tab()
        tas = buffer_textareas()
        ed["textareas_after_load"] = tas
        # The buffers. The ACTIVE one is typed into first; every other held
        # buffer is reached through the rail's loaded-document selector
        # (`select.doxchat-loaded`), exactly once each, and each switch is
        # counted: a switch is the rail's one thread read
        # (doxbench-chat.js, `switchThread`), so the count is what a
        # `/workbench/thread` declaration must expect.
        sel = page.locator(f"{R} select.doxchat-loaded")
        opts = sel.first.evaluate("e => [...e.options].map(o => [o.value, o.textContent])") if sel.count() else []
        ed["buffer_options"] = opts
        for t in tas:
            if t["visible"]:
                ed["buffers"][t["aria"] + " [active on open]"] = type_into(t["aria"])
        current = sel.first.input_value() if sel.count() else None
        for val, text in opts:
            if not val or val == current:
                continue
            sel.first.select_option(val)
            RAIL_SWITCHES[0] += 1
            page.wait_for_timeout(1200)
            editor_tab()
            for t in buffer_textareas():
                if t["visible"]:
                    ed["buffers"][t["aria"] + f" [{text}]"] = type_into(t["aria"])
            current = val
        ed["rail_switches"] = RAIL_SWITCHES[0]
        shot(page, "4e-editors-typed")
        typed = [k for k, v in ed["buffers"].items() if v.get("typed")]
        ed["typed"] = typed
        outline = any(k.startswith("Outline") for k in typed)
        documents = [k for k in typed if not k.startswith("Outline")]
        # "both editors": each editor the by-scope workbench offers opens and accepts edits
        offered = sorted({t["aria"] for t in ed["textareas_on_open"] + tas})
        not_typed = [o for o in offered if not any(k.startswith(o) for k in typed)]
        check("editors: each editor offered opens and accepts edits (5971834845)",
              bool(typed) and not not_typed and len(documents) >= 1,
              offered=offered, typed=typed, outline_typed=outline, not_typed=not_typed,
              detail=ed, screenshot=shot(page, "4f-editors"))
        # Create: on a standalone plane, T102's by-scope posture offers NO
        # create control (`editingPosture` answers `create: false`), and its
        # plane note, `scopeEditingNote()`, names creating a document and Save
        # as needing the create gate this install does not have. That absence
        # plus that note is how create is "refused by name" (RULED
        # `5971834845`); the t096-dry driver recorded the absence only.
        STEP[0] = "create"

        def create_controls_now():
            return [c for c in controls() if c["visible"] and re.search(
                r"\bcreate\b|new document", (c["text"] + " " + c["title"]).lower())]
        cr: dict = {"create_controls_visible": create_controls_now()}
        cr["posture_note"] = page.eval_on_selector_all(
            f"{R} .swb-posture-note",
            "els => els.map(e => ({hidden: e.hidden, visible: !!e.offsetParent, text: e.textContent.trim().slice(0,600)}))")
        cr["pills"] = page.eval_on_selector_all(
            f"{R} .pill", "els => els.map(e => ({text: e.textContent.trim(), title: (e.title||'').slice(0,300)}))")
        shown = [x for x in cr["posture_note"] if x["visible"] and not x["hidden"]]
        cr["create_named"] = any(CREATE_NAMED_WORDS in x["text"] for x in shown)
        cr["save_named_in_note"] = any(SAVE_NAMED_WORDS in x["text"] for x in shown)
        cr["scope_pill"] = any(x["text"] == SCOPE_PILL_WORDS for x in cr["pills"])
        check("editors: creating a document is not offered, and the plane note names create and Save as refused (T102, by scope)",
              not cr["create_controls_visible"] and cr["create_named"] and cr["save_named_in_note"],
              **cr, screenshot=shot(page, "4f2-create-absent"))
        # Save: refused by name, and nothing is written
        STEP[0] = "save"
        n_events_before = len(events)
        raw_before = {"console": len(raw.console_errors), "requestfailed": len(raw.failed_requests),
                      "pageerror": len(raw.page_errors)}
        save = page.locator(f"{R} button.doxbench-save")
        sv: dict = {"present": save.count()}
        if save.count():
            sv["visible"] = save.first.is_visible()
            sv["disabled"] = save.first.is_disabled()
            sv["title"] = save.first.get_attribute("title")
            if sv["visible"] and not sv["disabled"]:
                save.first.click()
                page.wait_for_timeout(2500)
        txt = page.locator(R).inner_text()
        sv["refusal_named"] = GATELESS_SAVE_WORDS in txt
        notes_now = page.eval_on_selector_all(
            f"{R} .doxbench-eventnote, {R} .doxbench-save-note",
            "els => els.map(e => ({cls: e.className, hidden: e.hidden, text: e.textContent.trim().slice(0,400)}))")
        sv["notes"] = notes_now
        new = events[n_events_before:]
        sv["requests_during_save"] = [e for e in new if e["kind"] == "request"]
        sv["writes_during_save"] = [e for e in new if e["kind"] == "request" and e["method"] != "GET"]
        sv["signals_during_save"] = {
            "console": len(raw.console_errors) - raw_before["console"],
            "requestfailed": len(raw.failed_requests) - raw_before["requestfailed"],
            "pageerror": len(raw.page_errors) - raw_before["pageerror"]}
        save_step_signals.update(sv["signals_during_save"])
        sv["edits_kept"] = [t for t in buffer_textareas()]
        sv["create_controls_visible"] = create_controls_now()
        check("editors: Save is refused by name, nothing is written",
              sv["present"] > 0 and sv["refusal_named"] and not sv["writes_during_save"],
              **sv, screenshot=shot(page, "4g-save-refused"))
        STEP[0] = "chat"
    section("chat", s_chat)

    STEP[0] = "settle"
    page.wait_for_timeout(1500)
    page.close()
    browser.close()

# ---- 5. the oracle ----------------------------------------------------------
# Each declaration: a server answer a STANDALONE install gives by a product
# decision, with the exact count per channel the oracle then holds it to. The
# list is fixed here, in review, and nothing outside this file extends it.
# The rail's `/workbench/thread` 403 on a plane with no branch session
# (t096-dry finding F1) is NOT declared: the holder ruled it a product fix,
# the rail reading the thread only when a session column is registered.
DECLARATIONS = [
    ["/views/intent-feed.js",
     "RULED OQ-F / Q5: intent-feed.js is not owed (10.2a, T075, openDox-code#73); "
     "views/intent-binding.js imports it optionally, so a standalone load answers 404 once",
     {"status": 404, "console": 1, "requestfailed": 1}],
    ["/snapshot-index.json",
     "openXdox's projection route (views/projection-index.js); no standalone binding answers it, "
     "and fetchSnapshotIndex degrades to the single snapshot",
     {"status": 404, "console": 1, "requestfailed": 0}],
    ["/project-register.json",
     "openDox's register projection (views/repo-selector.js); a plain repository has no project "
     "register and is answered 404 'no project register'",
     {"status": 404, "console": 1, "requestfailed": 0}],
]


def judged(declarations):
    er = smoke_signals.Errors()
    er.page_errors = list(raw.page_errors)
    er.console_errors = list(raw.console_errors)
    er.failed_requests = list(raw.failed_requests)
    for u, why, kw in declarations:
        er.account(u, why, **kw)
    return er


oracles = {"raw": judged([]), "declared": judged(DECLARATIONS)}
verdicts = {}
for name, er in oracles.items():
    verdicts[name] = {"clean": er.clean(), "summary": er.summary_line(),
                      "report": json.loads(er.report())}
    print(f"ORACLE {name}: clean={er.clean()} {er.summary_line()}")
    print(json.dumps({"unexpected": verdicts[name]["report"]["unexpected"],
                      "unsatisfied": verdicts[name]["report"]["unsatisfied_declarations"]}, indent=1)[:4000])

fivexx = [e for e in events if e["kind"].startswith("http_5")]
fourxx = [e for e in events if e["kind"].startswith("http_4")]
# F1's own measurement: every thread read the page made, with its answer.
thread_reads = [e["url"].split("?", 1)[-1] for e in events
                if e["kind"] == "request" and "/workbench/thread" in e["url"]]
thread_403 = [e for e in events if e["kind"] == "http_403" and "/workbench/thread" in e["url"]]
print(f"F1 measurement: rail switches {RAIL_SWITCHES[0]}, thread reads {len(thread_reads)}, "
      f"thread 403s {len(thread_403)}")
check("oracle: zero pageerror", not raw.page_errors, pageerrors=raw.page_errors)
check("oracle: nothing undeclared, every declaration satisfied", oracles["declared"].clean(),
      unexpected=verdicts["declared"]["report"]["unexpected"],
      unsatisfied=verdicts["declared"]["report"]["unsatisfied_declarations"])
check("oracle: no 5xx from any route the panes request", not fivexx, five_xx=fivexx)

result = {"label": a.label, "base": BASE, "browser_version": BROWSER_VERSION[0],
          "opened_through": OPEN_URL, "filled": filled, "checks": checks,
          "rail_switches": RAIL_SWITCHES[0], "thread_reads": thread_reads,
          "thread_403s": len(thread_403),
          "verdicts": verdicts, "declarations": DECLARATIONS,
          "save_step_signals": save_step_signals,
          "events": [e for e in events if e["kind"] != "request"],
          "requests": [e for e in events if e["kind"] == "request"],
          "four_xx": fourxx, "five_xx": fivexx}
(OUT / f"{a.label}-result.json").write_text(json.dumps(result, indent=1, default=str))
print("NON-REQUEST EVENTS:")
for e in result["events"]:
    print(" ", json.dumps(e, default=str)[:700])
fails = [k for k, v in checks.items() if v["result"] != "PASS"]
print("FAILED CHECKS:", fails)
print(f"AT-R1 browser half ({a.label}): {'PASS' if not fails else 'FAIL'}")
sys.exit(1 if fails else 0)
