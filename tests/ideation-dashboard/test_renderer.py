"""US2 renderer surface (T013): the snapshot-only web bundle, the pure funnel
view-model derivation, the serve.py route/security behavior, and the
generate-and-open CLI wiring. Python-side only — no browser automation:

  * asset integrity is asserted by inspecting web/ (the JS fetches ONLY the
    snapshot; there is no external URL anywhere in the bundle — grep-proven);
  * the snapshot→view-model derivation and the five-column collapse run the
    ACTUAL model.js in node against the real fixture snapshot (skipped when node
    is absent), and the tally=edge-count parity is also proven on the snapshot
    data the renderer displays verbatim;
  * serve.py is driven over real HTTP: 200 snapshot, 200 source pass-through,
    the source_revision-vs-HEAD divergence header, and 404 on every
    path-traversal attempt (the security guarantee);
  * the CLI is exercised with an injected browser opener and the non-blocking
    --no-serve path.

All against the REAL fixture snapshot, generated in-test via the wave-2 API with
FakeGit + the pinned revision (the same substrate as test_generator.py)."""

from __future__ import annotations

import http.client
import json
import re
import shutil
import subprocess
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit  # noqa: F401

from ideation_dashboard import serve as serve_mod
from ideation_dashboard.cli import build_parser, cmd_generate_and_open
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
MODEL_JS = WEB / "views" / "model.js"
VIEWER_JS = WEB / "views" / "viewer.js"
VENDOR_MARKDOWN_JS = WEB / "vendor" / "markdown-it.min.js"
NODE = shutil.which("node")

EXPECTED_VIEW_FILES = [
    WEB / "index.html",
    WEB / "app.js",
    WEB / "styles.css",
    WEB / "views" / "model.js",
    WEB / "views" / "funnel.js",
    WEB / "views" / "board.js",
    WEB / "views" / "docs.js",
    WEB / "views" / "lineage.js",
    WEB / "views" / "grouping.js",
    WEB / "views" / "notebook.js",
    # add-dashboard-repo-selector: the selector/refresh transport and its pure
    # view model (the roster, the freshness header, the passive newer-data hint).
    WEB / "views" / "repo-selector.js",
    WEB / "views" / "repo-selector-model.js",
    # 010-doxbench-editor-chat (T088): the doxBench authoring canvas — pure
    # buffer state, the editor view, and Save orchestration. Client modules
    # whose only transports are injected seams; pinned below in their own
    # boundary block.
    WEB / "views" / "doxbench-state.js",
    WEB / "views" / "doxbench-editor.js",
    WEB / "views" / "doxbench-save.js",
]

# Any of these appearing in OUR OWN hand-written bundle code would mean an
# off-snapshot data path or a non-vendored asset. The SVG XML namespace
# (w3.org) and JSON-Schema $id are the only permitted literal URLs.
EXTERNAL_URL_RE = re.compile(
    r"https?://|//(?:cdn|unpkg|cdnjs)|unpkg|jsdelivr|googleapis|cdnjs|"
    r"integrity=|crossorigin|XMLHttpRequest|WebSocket|EventSource|navigator\.sendBeacon",
    re.IGNORECASE,
)
_ALLOWED_URL_RE = re.compile(r"w3\.org|json-schema\.org", re.IGNORECASE)


def _bundle_files():
    return sorted(p for p in WEB.rglob("*") if p.is_file() and p.suffix in {".js", ".html", ".css"})


# The hand-written surface only — excludes `web/vendor/` (T018's vendored
# markdown-it is a reviewed, offline third-party asset whose own minified
# source legitimately contains generic "http://" string literals as part of
# its link-normalization logic, never a live fetch; the vendored-renderer
# integrity test in test_explorer_viewer.py asserts it has zero LIVE network
# primitives instead of zero URL-shaped substrings).
def _own_bundle_files():
    return [p for p in _bundle_files() if "vendor" not in p.relative_to(WEB).parts]


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


# ----------------------------------------------------------------------------
# asset integrity — the snapshot-only, no-external-asset boundary (grep-proven)
# ----------------------------------------------------------------------------

def test_web_bundle_files_present():
    missing = [str(p.relative_to(WEB)) for p in EXPECTED_VIEW_FILES if not p.is_file()]
    assert not missing, f"missing bundle files: {missing}"


def test_no_external_urls_anywhere_in_bundle():
    offenders = []
    for path in _own_bundle_files():
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if _ALLOWED_URL_RE.search(line):
                continue
            if EXTERNAL_URL_RE.search(line):
                offenders.append(f"{path.relative_to(WEB)}:{lineno}: {line.strip()}")
    assert not offenders, "external URL/network primitive in the bundle:\n" + "\n".join(offenders)


def test_data_fetches_target_only_snapshot_and_source_passthrough():
    # Every fetch() in the bundle targets one of exactly five backend routes:
    # the snapshot (app.js — the STATE fetch, addressed by the active
    # (repository, ref) pair), the read-only /source/ pass-through (viewer.js —
    # D15 document CONTENT, T018 — wheel.js's archived `landed` verb, and now a
    # second app.js call site: the doxBench authoring canvas's source-loading
    # seam, 010-doxbench-editor-chat T023, threaded through the workbench's own
    # current source base rather than a second route), the v2 tile action seam
    # (notebook.js — GET /capabilities + POST /actions/notebook), and the
    # repository-selector seam (repo-selector.js — GET /snapshot-index.json +
    # POST /actions/refresh).
    # The fetch-count invariant widens ONLY by the arithmetic of new SAME-ORIGIN
    # backend routes, or of a new call site against an EXISTING route (T023's
    # renderer-boundary item): the external data source is read by the SERVING
    # side (design D5), so no bundle file addresses anything but its own origin
    # — the ban assertions above are untouched.
    fetches = []
    for path in _bundle_files():
        for line in path.read_text(encoding="utf-8").splitlines():
            for m in re.finditer(r"fetch\(([^)]*)", line):
                fetches.append((path.name, m.group(1)))
    by_file = {}
    for fname, arg in fetches:
        by_file.setdefault(fname, []).append(arg)
    assert set(by_file) == {"app.js", "viewer.js", "notebook.js", "wheel.js",
                            "repo-selector.js"}, fetches
    # T023 wire clause (2026-07-31): app.js gains the two doxBench transports
    # -- the released model-catalog GET and the chat-turn POST -- exactly the
    # same-origin route arithmetic this docstring declares widening by.
    assert len(by_file["app.js"]) == 4
    assert any("snapshotUrl" in a or "snapshot" in a.lower() for a in by_file["app.js"])
    assert any("sourceBase" in a for a in by_file["app.js"])
    assert sum("CATALOG_ROUTE" in a for a in by_file["app.js"]) == 1
    assert sum("CHAT_TURN_ROUTE" in a for a in by_file["app.js"]) == 1
    assert len(by_file["viewer.js"]) == 1
    assert any("sourceBase" in a for a in by_file["viewer.js"])
    # wheel.js: exactly the archived `landed` read, on the read-only /source route
    # (its keyed base — `sourceBase` defaults to SOURCE_ROUTE).
    assert len(by_file["wheel.js"]) == 1
    assert any("sourceBase" in a for a in by_file["wheel.js"])
    # notebook.js: exactly the capability probe + the action POST, no other host.
    assert len(by_file["notebook.js"]) == 2
    assert any("CAPABILITIES_ROUTE" in a for a in by_file["notebook.js"])
    assert any("ACTIONS_NOTEBOOK_ROUTE" in a for a in by_file["notebook.js"])
    # repo-selector.js: exactly the index read + the refresh POST, both
    # same-origin serve.py routes.
    assert len(by_file["repo-selector.js"]) == 2
    assert any("SNAPSHOT_INDEX_ROUTE" in a for a in by_file["repo-selector.js"])
    assert any("ACTIONS_REFRESH_ROUTE" in a for a in by_file["repo-selector.js"])


def test_shared_markdown_seam_is_exported_and_owns_the_nonempty_html_sink():
    viewer = VIEWER_JS.read_text(encoding="utf-8")
    assert "export function renderSafeMarkdownHtml(" in viewer
    assert "export function mountSafeMarkdown(" in viewer
    assert "body.innerHTML = mdRenderer().render(text);" not in viewer
    assert "mountSafeMarkdown(body, text);" in viewer
    assert viewer.count("innerHTML = renderSafeMarkdownHtml(") == 1


@pytest.mark.skipif(NODE is None, reason="node not available for shared Markdown probe")
def test_shared_markdown_seam_escapes_html_and_defers_external_images(tmp_path):
    (tmp_path / "views").mkdir()
    (tmp_path / "vendor").mkdir()
    shutil.copy(VIEWER_JS, tmp_path / "views" / "viewer.mjs")
    shutil.copy(VENDOR_MARKDOWN_JS, tmp_path / "vendor" / "markdown-it.min.js")
    harness = tmp_path / "views" / "markdown-harness.mjs"
    harness.write_text(
        """
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
globalThis.markdownit = require('../vendor/markdown-it.min.js');
const {
  mountSafeMarkdown,
  renderSafeMarkdownHtml,
} = await import('./viewer.mjs');

const source = [
  '# doxBench',
  '',
  '<script>alert("raw")</script>',
  '',
  '<img src=x onerror="alert(1)">',
  '',
  '![tracker](https://example.invalid/pixel.png)',
  '',
  '![legacy](ftp://example.invalid/pixel.png)',
  '',
  '![file](file:///tmp/private.png)',
  '',
  '![local](images/local.png)',
  '',
  '[unsafe](javascript:alert(2))',
].join('\\n');
const html = renderSafeMarkdownHtml(source);
const container = {
  innerHTML: '',
  queryCount: 0,
  querySelectorAll(selector) {
    this.queryCount += 1;
    if (selector !== '.ext-img-load') throw new Error('unexpected selector');
    return [];
  },
};
const mounted = mountSafeMarkdown(container, source);
let nonTextError = null;
try {
  renderSafeMarkdownHtml({ text: source });
} catch (error) {
  nonTextError = { name: error.constructor.name, message: error.message };
}
console.log(JSON.stringify({
  html,
  mountedIsContainer: mounted === container,
  mountedHtml: container.innerHTML,
  queryCount: container.queryCount,
  nonTextError,
}));
""".strip()
        + "\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [NODE, str(harness)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    output = json.loads(proc.stdout)
    html = output["html"]

    assert "<h1>doxBench</h1>" in html
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "<img src=x" not in html
    assert "&lt;img src=x onerror=" in html
    assert '<a href="javascript:' not in html
    assert '<img src="https://example.invalid' not in html
    assert '<img src="ftp://example.invalid' not in html
    assert '<img src="file:///tmp/private.png"' not in html
    assert html.count('class="ext-img"') == 2
    assert '<img src="images/local.png" alt="local">' in html
    assert output["mountedIsContainer"] is True
    assert output["mountedHtml"] == html
    assert output["queryCount"] == 1
    assert output["nonTextError"] == {
        "name": "TypeError",
        "message": "Markdown source must be a string",
    }


# ----------------------------------------------------------------------------
# T104 F7-6 + F6-5: the external-image click path, REALLY exercised. The stub
# harness above deliberately answers querySelectorAll with [] (its subject is
# the HTML string), so the click-to-load behaviour was untested — and it was
# broken twice over: the replacement <img> shipped alt="" (the derived label
# was rendered into the placeholder and then thrown away) with no error
# handler (a failed load left an unlabeled broken-image box, no retry), and
# every debounced preview re-render rebuilt via innerHTML, reverting an image
# the human explicitly loaded to a placeholder. Consent now persists per
# container per src; a NEW src still requires its own click; a FAILED load
# revokes the consent and restores a labeled retry placeholder.
#
# The DOM here parses exactly the placeholder markup the renderer emits
# (span.ext-img with data-src/data-label wrapping button.ext-img-load) into
# live nodes — enough for querySelectorAll/closest/replaceWith, the whole
# surface this path touches.
# ----------------------------------------------------------------------------

_EXT_IMG_HARNESS = r"""
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
globalThis.markdownit = require('../vendor/markdown-it.min.js');

function unescapeHtml(s) {
  return String(s).replace(/&(amp|lt|gt|quot|#39);/g, (m, name) => (
    { amp: '&', lt: '<', gt: '>', quot: '"', '#39': "'" }[name]));
}

class FakeNode {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.className = ''; this.children = []; this.parentNode = null;
    this.listeners = {}; this.dataset = {}; this._text = '';
    this.alt = undefined; this.src = undefined; this.type = '';
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  set textContent(value) { this.children = []; this._text = String(value); }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  walk() { return this.children.reduce((a, c) => a.concat(c.walk()), [this]); }
  querySelectorAll(selector) {
    const cls = selector.replace(/^\./, '');
    return this.walk().filter(
      (n) => n !== this && String(n.className).split(' ').includes(cls));
  }
  closest(selector) {
    const cls = selector.replace(/^\./, '');
    let node = this;
    while (node) {
      if (String(node.className).split(' ').includes(cls)) return node;
      node = node.parentNode;
    }
    return null;
  }
  replaceWith(replacement) {
    const parent = this.parentNode;
    if (!parent) return;
    const at = parent.children.indexOf(this);
    replacement.parentNode = parent;
    parent.children.splice(at, 1, replacement);
    this.parentNode = null;
  }
}

// The container: parses the renderer's own placeholder markup into live
// holder/button nodes on every innerHTML assignment (the preview re-render).
class Container extends FakeNode {
  set innerHTML(html) {
    this.children = []; this._text = '';
    const holderRe = /<span class="ext-img" data-src="([^"]*)" data-label="([^"]*)">/g;
    let m;
    while ((m = holderRe.exec(String(html))) !== null) {
      const holder = new FakeNode('span');
      holder.className = 'ext-img';
      holder.dataset.src = unescapeHtml(m[1]);
      holder.dataset.label = unescapeHtml(m[2]);
      holder._text = '\u{1F5BC} external image not loaded — '
        + holder.dataset.label + ' ';
      const btn = new FakeNode('button');
      btn.className = 'ext-img-load';
      btn._text = 'load image';
      holder.appendChild(btn);
      this.appendChild(holder);
    }
  }
  get innerHTML() { return ''; }
}

globalThis.document = { createElement: (tag) => new FakeNode(tag) };

const { mountSafeMarkdown } = await import('./viewer.mjs');

const fire = (node, type) => {
  for (const fn of (node && node.listeners[type]) || []) fn({});
};
const byClass = (root, cls) => root.walk().filter(
  (n) => n !== root && String(n.className).split(' ').includes(cls));

const SOURCE = [
  '![tracker one](https://example.invalid/one.png)',
  '',
  '![tracker two](https://example.invalid/two.png)',
].join('\n');

const out = {};
const container = new Container('div');
mountSafeMarkdown(container, SOURCE);
out.initialPlaceholders = byClass(container, 'ext-img').length;
out.placeholderLabels = byClass(container, 'ext-img').map(
  (h) => h.dataset.label);

// 1: the human clicks LOAD on the first image — the replacement carries the
// derived label as alt, and the off-origin src only now lands in the tree
fire(byClass(container, 'ext-img-load')[0], 'click');
const loaded = byClass(container, 'ext-img-loaded');
out.afterClick = {
  images: loaded.length,
  alt: loaded.length ? loaded[0].alt : null,
  src: loaded.length ? loaded[0].src : null,
  remainingPlaceholders: byClass(container, 'ext-img').length,
};

// 2: the debounced preview re-render rebuilds the SAME container — consent
// persists per container per src, so the loaded image comes back loaded and
// the never-clicked src stays a placeholder
mountSafeMarkdown(container, SOURCE);
const reloaded = byClass(container, 'ext-img-loaded');
out.afterRemount = {
  images: reloaded.length,
  alt: reloaded.length ? reloaded[0].alt : null,
  src: reloaded.length ? reloaded[0].src : null,
  placeholders: byClass(container, 'ext-img').length,
};

// 3: the load FAILS — a labeled retry placeholder comes back, never an
// empty broken-image box
if (reloaded.length) fire(reloaded[0], 'error');
const afterError = byClass(container, 'ext-img');
const retryButtons = byClass(container, 'ext-img-load');
out.afterError = {
  loadedLeft: byClass(container, 'ext-img-loaded').length,
  placeholders: afterError.length,
  labelPresent: container.textContent.includes('tracker one'),
  retryButtons: retryButtons.length,
};

// 4: a failed load REVOKES the consent: the next re-render placeholders
// again instead of auto-retrying an endless failing fetch
mountSafeMarkdown(container, SOURCE);
out.afterErrorRemount = {
  images: byClass(container, 'ext-img-loaded').length,
  placeholders: byClass(container, 'ext-img').length,
};

// 5: the RETRY button is live — a fresh click loads again, alt intact
fire(byClass(container, 'ext-img-load')[0], 'click');
const retried = byClass(container, 'ext-img-loaded');
out.afterRetry = {
  images: retried.length,
  alt: retried.length ? retried[0].alt : null,
};

// 6: consent is PER CONTAINER — a different container starts placeholdered
const other = new Container('div');
mountSafeMarkdown(other, SOURCE);
out.otherContainer = {
  images: byClass(other, 'ext-img-loaded').length,
  placeholders: byClass(other, 'ext-img').length,
};

console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def ext_img_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the external-image click probe")
    tmp_path = tmp_path_factory.mktemp("viewer-ext-img")
    (tmp_path / "views").mkdir()
    (tmp_path / "vendor").mkdir()
    shutil.copy(VIEWER_JS, tmp_path / "views" / "viewer.mjs")
    shutil.copy(VENDOR_MARKDOWN_JS, tmp_path / "vendor" / "markdown-it.min.js")
    harness = tmp_path / "views" / "ext-img-harness.mjs"
    harness.write_text(_EXT_IMG_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_placeholder_markup_carries_the_label_for_the_swap(ext_img_results):
    """F7-6 preliminary: the derived label (`token.content || src`) is stored
    on the placeholder (data-label), not merely rendered into its text —
    otherwise the click-time swap has nothing to put in alt."""
    assert ext_img_results["initialPlaceholders"] == 2
    assert ext_img_results["placeholderLabels"] == ["tracker one", "tracker two"]


def test_a_click_loaded_image_carries_the_label_as_alt(ext_img_results):
    a = ext_img_results["afterClick"]
    assert a["images"] == 1
    assert a["alt"] == "tracker one", "the derived label must survive onto alt"
    assert a["src"] == "https://example.invalid/one.png"
    assert a["remainingPlaceholders"] == 1, "the unclicked image stays inert"


def test_a_loaded_image_survives_a_preview_remount_of_the_same_container(
        ext_img_results):
    """F6-5: mountSafeMarkdown rebuilds via innerHTML on every debounced
    preview keystroke; the human's explicit load consent persists per
    container per src, while the never-clicked src still requires its own
    click."""
    r = ext_img_results["afterRemount"]
    assert r["images"] == 1
    assert r["alt"] == "tracker one"
    assert r["src"] == "https://example.invalid/one.png"
    assert r["placeholders"] == 1, "a new/unclicked src still placeholders"


def test_a_failed_load_restores_a_labeled_retry_placeholder(ext_img_results):
    e = ext_img_results["afterError"]
    assert e["loadedLeft"] == 0, "the broken img must not linger unlabeled"
    assert e["placeholders"] == 2
    assert e["labelPresent"] is True, "the placeholder must carry the label"
    assert e["retryButtons"] == 2, "the failed image offers a retry control"


def test_a_failed_load_revokes_the_remount_consent(ext_img_results):
    r = ext_img_results["afterErrorRemount"]
    assert r["images"] == 0, "a failed src must not auto-retry on re-render"
    assert r["placeholders"] == 2


def test_the_retry_control_is_live_and_keeps_the_label(ext_img_results):
    r = ext_img_results["afterRetry"]
    assert r["images"] == 1
    assert r["alt"] == "tracker one"


def test_load_consent_is_per_container(ext_img_results):
    o = ext_img_results["otherContainer"]
    assert o["images"] == 0
    assert o["placeholders"] == 2


def test_the_session_transport_stays_out_of_the_fetch_bearing_set():
    """T080 / FR-047 (007-workbench-branch-sessions): the session surface added a
    FOURTH renderer module — `views/swb-session.js`, the only session transport —
    and the pin above did NOT move.

    The arithmetic is the whole point. `swb-session.js` addresses three
    same-origin gate routes, but it takes an INJECTED fetcher and calls it through
    the `doFetch` spelling (`const doFetch = fetcher || fetch;`), exactly as
    `swb-create.js` and `dispose.js` do, so it contributes no `fetch(` call site
    to the bundle and the pinned set and per-file counts are UNCHANGED. This test
    states that as an assertion rather than leaving it as a fact somebody could
    quietly undo: it re-derives the same measurement, asserts the new file is
    absent from the set, and quotes the pinned assertions above — the set AND all
    five per-file counts, each needle assembled at runtime so it cannot match its
    own source (finding 24) — so a future pass that "widens" the pin to admit a
    transport module fails here even if it edits the pin itself."""
    session_js = WEB / "views" / "swb-session.js"
    assert session_js.is_file(), "the session transport module is missing"
    body = session_js.read_text(encoding="utf-8")
    assert "const doFetch = fetcher || fetch;" in body
    assert "doFetch(" in body and "fetch(" not in body
    by_file = {}
    for path in _bundle_files():
        for line in path.read_text(encoding="utf-8").splitlines():
            for m in re.finditer(r"fetch\(([^)]*)", line):
                by_file.setdefault(path.name, []).append(m.group(1))
    assert "swb-session.js" not in by_file
    assert "swb-create.js" not in by_file
    assert set(by_file) == {"app.js", "viewer.js", "notebook.js", "wheel.js",
                            "repo-selector.js"}
    # T023 wire clause (2026-07-31): app.js's budget rose 2 -> 4 with the two
    # doxBench transports — the LOUD, individually-named widening the sibling
    # pin's docstring declares; every other count is unchanged.
    assert {name: len(args) for name, args in by_file.items()} == {
        "app.js": 4, "viewer.js": 1, "wheel.js": 1, "notebook.js": 2,
        "repo-selector.js": 2}
    # the pin above, quoted: a clobber that relaxes it cannot pass by satisfying
    # the looser form (SC-007's reasoning applied to the renderer boundary)
    own = Path(__file__).read_text(encoding="utf-8")
    assert ('assert set(by_file) == {"app.js", "viewer.js", "notebook.js", '
            '"wheel.js",\n                            "repo-selector.js"}, '
            'fetches') in own
    # EVERY per-file count, and every needle BUILT rather than written (PR #49
    # second-review finding 24). The count half of this guard used to quote ONE of
    # the five counts as a single source literal, and a literal quoting a line of
    # code occurs verbatim inside its own quotes — so `needle in own` was satisfied
    # by the quote itself. Mutation-proven: deleting the real pin left this test
    # PASSING, and relaxing that pin from an equality to an inequality did too. The
    # other four counts were not quoted at all. A needle ASSEMBLED at runtime
    # cannot match its own source line, so an exact occurrence count is meaningful
    # now: ONE, the pin itself. (Nothing in this block may spell a pinned line
    # literally, in a comment or anywhere else — that is what re-creates the hole.)
    q = '"'
    for name, n in (("app.js", 4), ("viewer.js", 1), ("wheel.js", 1),
                    ("notebook.js", 2), ("repo-selector.js", 2)):
        count_line = f"assert len(by_file[{q}{name}{q}]) == {n}"
        assert own.count(count_line) == 1, (
            f"the per-file count pin for {name} is not spelled exactly once: a "
            f"widened or deleted pin reads as zero occurrences")
        # and the second, independent re-derivation above — the exact dict — which
        # the old guard left unquoted too
        assert own.count(f"{q}{name}{q}: {n}") == 1, (
            f"the exact-dict pin for {name} is not spelled exactly once")


def test_index_references_local_assets_only():
    html = (WEB / "index.html").read_text(encoding="utf-8")
    # module entrypoint + stylesheet are relative-local (exact literals — no
    # backtracking-prone attribute-order regex; S8786)
    assert '<script type="module" src="./app.js"></script>' in html
    assert '<link rel="stylesheet" href="./styles.css">' in html
    # no absolute or protocol-relative asset references
    assert not re.search(r'(src|href)="(?:https?:)?//', html)


def test_dynamic_import_is_absent():
    # ES module static imports only (no dynamic import() that could pull a URL).
    for path in _bundle_files():
        assert "import(" not in path.read_text(encoding="utf-8"), f"dynamic import in {path.name}"


# ----------------------------------------------------------------------------
# six-column default + five-column collapse (structural, CSS-level)
# ----------------------------------------------------------------------------

def _grid_tracks(css: str, selector: str) -> list[str]:
    """The grid-template-columns tracks of the rule opened by `selector` —
    string-sliced rather than regexed so the scan stays strictly linear
    (S8786: the old [^}]*-then-literal pattern backtracked super-linearly)."""
    assert selector in css, f"selector not found: {selector}"
    block = css.split(selector, 1)[1].split("}", 1)[0]
    assert "grid-template-columns:" in block, f"no grid-template-columns under {selector}"
    return block.split("grid-template-columns:", 1)[1].split(";", 1)[0].split()


def test_six_column_default_and_five_column_collapse_marker():
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    # the docs column collapses via an opt-in modifier, never by default
    assert ".funnel-inner.collapsed-docs .only-docs { display: none; }" in css
    # default funnel grid is six columns; the collapse switches to five
    six = _grid_tracks(css, ".colheads, .funnel-cols {")
    assert len(six) == 6, "default funnel is not six columns"
    five = _grid_tracks(css, ".funnel-inner.collapsed-docs .colheads, .funnel-inner.collapsed-docs .funnel-cols {")
    assert len(five) == 5, "collapse is not five columns"


def test_funnel_default_is_not_collapsed():
    # The renderer must not ship the collapsed class on the funnel by default
    # (six columns is the structural default; five is opt-in).
    funnel = (WEB / "views" / "funnel.js").read_text(encoding="utf-8")
    assert 'v6.setAttribute("aria-pressed", "true")' in funnel
    assert "let collapsed = false;" in funnel


# ----------------------------------------------------------------------------
# tally == edge-count parity on the snapshot the renderer renders VERBATIM
# ----------------------------------------------------------------------------

def test_cluster_document_link_tally_equals_edge_count():
    snap = _snapshot()
    for c in snap["clusters"]:
        assert c["tallies"]["document_links"] == len(c["document_edges"]), c["id"]


def test_cluster_possible_link_tally_equals_claiming_count():
    snap = _snapshot()
    claims = {c["id"]: 0 for c in snap["clusters"]}
    for p in snap["possibles"]:
        for cid in p.get("claiming_clusters", []):
            claims[cid] = claims.get(cid, 0) + 1
    for c in snap["clusters"]:
        assert c["tallies"]["possible_links"] == claims[c["id"]], c["id"]


# ----------------------------------------------------------------------------
# the ACTUAL model.js derivation, run in node against the real fixture snapshot
# ----------------------------------------------------------------------------

_NODE_HARNESS = """
import { buildFunnelModel, visibleEdges } from './model.mjs';
import { readFileSync } from 'node:fs';
const snap = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const m = buildFunnelModel(snap);
const cols = Object.fromEntries(m.columns.map(c => [c.key, c.nodes.length]));
const kinds = {};
for (const e of m.edges) kinds[e.kind] = (kinds[e.kind] || 0) + 1;
const docEdgesInto = {};
for (const e of m.edges) if (e.kind === 'topic' && e.fromColumn === 'docs') docEdgesInto[e.to] = (docEdgesInto[e.to] || 0) + 1;
const clusters = m.columns.find(c => c.key === 'clusters').nodes;
const tallyParity = clusters.every(n => (n.cluster.tallies.document_links || 0) === (docEdgesInto[n.domId] || 0));
const collapsed = visibleEdges(m, { collapsed: true });
const collapsedTouchesDocs = collapsed.some(e => e.fromColumn === 'docs' || e.toColumn === 'docs');
console.log(JSON.stringify({
  cols, kinds, edges: m.edges.length, tallyParity,
  collapsedEdges: collapsed.length, collapsedTouchesDocs,
  domIdsUnique: new Set(m.edges.flatMap(e => [e.from, e.to])).size >= 0,
}));
"""


def _run_node_model(snapshot, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(MODEL_JS, tmp_path / "model.mjs")
    (tmp_path / "harness.mjs").write_text(_NODE_HARNESS, encoding="utf-8")
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "harness.mjs"), str(snap_path)],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_model_derives_the_six_columns(tmp_path):
    r = _run_node_model(_snapshot(), tmp_path)
    assert r["cols"] == {"docs": 6, "clusters": 6, "possibles": 5, "staged": 2, "proposals": 1, "realized": 1}


def test_model_edge_derivation(tmp_path):
    r = _run_node_model(_snapshot(), tmp_path)
    # 10 doc->cluster + 6 cluster->possible = 16 topic; 1 pick; 1 flow
    assert r["kinds"] == {"topic": 16, "pick": 1, "flow": 1}
    assert r["edges"] == 18


def test_model_tally_equals_edge_count_through_the_real_js(tmp_path):
    r = _run_node_model(_snapshot(), tmp_path)
    assert r["tallyParity"] is True


def test_five_column_collapse_drops_doc_edges(tmp_path):
    r = _run_node_model(_snapshot(), tmp_path)
    # collapsing docs removes exactly the 10 doc->cluster edges; nothing left
    # touches the docs column
    assert r["collapsedEdges"] == 8
    assert r["collapsedTouchesDocs"] is False


def test_model_degrades_on_empty_snapshot(tmp_path):
    empty = {"documents": [], "clusters": [], "possibles": [], "staged_topics": [], "changes": []}
    r = _run_node_model(empty, tmp_path)
    assert r["cols"] == {"docs": 0, "clusters": 0, "possibles": 0, "staged": 0, "proposals": 0, "realized": 0}
    assert r["edges"] == 0


# ----------------------------------------------------------------------------
# serve.py — routes, divergence, and the path-traversal security guarantee
# ----------------------------------------------------------------------------

@contextmanager
def _serving(tmp_path, *, head):
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(_snapshot()), encoding="utf-8")
    httpd = serve_mod.build_server(WEB, snap_path, BASE_REPO, head=head)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield host, port
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _raw_get(host, port, raw_path, method="GET"):
    """Send a RAW request-line path (no client-side normalization) so the
    server's own traversal defense is what gets tested."""
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.putrequest(method, raw_path, skip_host=False, skip_accept_encoding=True)
    conn.putheader("Host", f"{host}:{port}")
    conn.endheaders()
    resp = conn.getresponse()
    body = resp.read()
    headers = {k.lower(): v for k, v in resp.getheaders()}  # HTTP headers are case-insensitive
    conn.close()
    return resp.status, headers, body


def test_serve_snapshot_route_and_alignment(tmp_path):
    with _serving(tmp_path, head=PINNED_REVISION) as (host, port):
        status, headers, body = _raw_get(host, port, "/snapshot.json")
    assert status == 200
    assert "application/json" in headers.get("content-type", "")
    assert json.loads(body)["repository"] == "fixture-repo"
    assert headers.get("x-snapshot-divergence") == "aligned"


def test_serve_static_bundle(tmp_path):
    with _serving(tmp_path, head=PINNED_REVISION) as (host, port):
        s_index, _, b_index = _raw_get(host, port, "/index.html")
        s_app, h_app, _ = _raw_get(host, port, "/app.js")
    assert s_index == 200 and b"ideation dashboard" in b_index
    assert s_app == 200 and "javascript" in h_app.get("content-type", "")


def test_serve_source_passthrough(tmp_path):
    rel = "ideation/brainstorm/legacy-note.md"
    with _serving(tmp_path, head=PINNED_REVISION) as (host, port):
        status, headers, body = _raw_get(host, port, "/source/" + rel)
    assert status == 200
    assert "text/markdown" in headers.get("content-type", "")
    assert body == (BASE_REPO / rel).read_bytes()
    assert headers.get("x-snapshot-divergence") == "aligned"


def test_serve_divergence_diverged(tmp_path):
    with _serving(tmp_path, head="f" * 40) as (host, port):
        status, headers, _ = _raw_get(host, port, "/snapshot.json")
    assert status == 200
    assert headers.get("x-snapshot-divergence") == "diverged"
    assert headers.get("x-source-head") == "f" * 40


def test_serve_divergence_unknown_without_head(tmp_path):
    with _serving(tmp_path, head="") as (host, port):
        status, headers, _ = _raw_get(host, port, "/snapshot.json")
    assert status == 200
    assert headers.get("x-snapshot-divergence") == "unknown"


@pytest.mark.parametrize("raw_path", [
    "/source/../../../../etc/passwd",
    "/source/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
    "/source/ideation/../../../../etc/passwd",
    "/source//etc/passwd",
    "/source/..%2f..%2f..%2fetc%2fpasswd",
    "/source/nonexistent-file.md",
    "/source/",
])
def test_serve_rejects_path_traversal(tmp_path, raw_path):
    with _serving(tmp_path, head=PINNED_REVISION) as (host, port):
        status, _, body = _raw_get(host, port, raw_path)
    assert status == 404, f"{raw_path} should be refused, got {status}"
    assert b"root:" not in body  # never leak /etc/passwd


def test_serve_source_is_read_only(tmp_path):
    # No write route exists: a POST to the source route is not served.
    with _serving(tmp_path, head=PINNED_REVISION) as (host, port):
        status, _, _ = _raw_get(host, port, "/source/ideation/brainstorm/legacy-note.md", method="POST")
    assert status != 200


def test_resolve_source_path_unit():
    root = BASE_REPO
    assert serve_mod.resolve_source_path(root, "ideation/brainstorm/legacy-note.md") is not None
    assert serve_mod.resolve_source_path(root, "../../../etc/passwd") is None
    assert serve_mod.resolve_source_path(root, "/etc/passwd") is None
    assert serve_mod.resolve_source_path(root, "does/not/exist.md") is None


def test_divergence_states_unit():
    assert serve_mod.divergence("abc", "abc")["state"] == "aligned"
    assert serve_mod.divergence("abc", "xyz")["state"] == "diverged"
    assert serve_mod.divergence("abc", None)["state"] == "unknown"


# ----------------------------------------------------------------------------
# CLI wiring — generate-and-open
# ----------------------------------------------------------------------------

def test_cli_exposes_generate_and_open():
    parser = build_parser()
    args = parser.parse_args([
        "generate-and-open", "--repo-root", str(BASE_REPO), "--repository", "fixture-repo",
        "--source-revision", PINNED_REVISION, "--no-open", "--no-serve",
    ])
    assert args.command == "generate-and-open"
    assert args.func is cmd_generate_and_open
    assert args.no_open and args.no_serve


def _gao_args(tmp_path, **over):
    argv = [
        "generate-and-open", "--repo-root", str(BASE_REPO), "--repository", "fixture-repo",
        "--source-revision", PINNED_REVISION, "--run-dir", str(tmp_path / "run"),
        "--no-validate",
    ]
    for k, v in over.items():
        argv.append("--" + k.replace("_", "-"))
        if v is not True:
            argv.append(str(v))
    return build_parser().parse_args(argv)


def test_generate_and_open_generates_and_always_prints_url(tmp_path, capsys):
    calls = []
    args = _gao_args(tmp_path, no_serve=True)  # opener still fires (no --no-open)
    rc = cmd_generate_and_open(args, opener=lambda url: calls.append(url))
    out = capsys.readouterr().out
    assert rc == 0
    # the snapshot was generated into the run dir
    assert (tmp_path / "run" / "snapshot.json").is_file()
    # the URL is printed on its own line, and the opener was invoked with it
    url_lines = [ln for ln in out.splitlines() if ln.startswith("http://127.0.0.1:")]
    assert url_lines, out
    assert calls and calls[0].startswith("http://127.0.0.1:")


def test_generate_and_open_respects_no_open(tmp_path, capsys):
    calls = []
    args = _gao_args(tmp_path, no_serve=True, no_open=True)
    rc = cmd_generate_and_open(args, opener=lambda url: calls.append(url))
    assert rc == 0
    assert calls == []  # --no-open suppresses the browser
    out = capsys.readouterr().out
    # a loopback URL was printed (the 127.0.0.1 prefix keeps this in S5332's
    # explicit loopback exemption, matching the sibling test above)
    assert any(ln.startswith("http://127.0.0.1:") for ln in out.splitlines())


def test_generated_snapshot_is_schema_shaped(tmp_path):
    # what generate-and-open serves is exactly the deterministic snapshot the
    # renderer reads — the same object test_generator asserts on.
    args = _gao_args(tmp_path, no_serve=True, no_open=True)
    cmd_generate_and_open(args, opener=lambda url: None)
    data = json.loads((tmp_path / "run" / "snapshot.json").read_text(encoding="utf-8"))
    assert data["kind"] == "ideation-dashboard-snapshot"
    assert {c["id"] for c in data["clusters"]}  # non-empty projection


# ----------------------------------------------------------------------------
# T088 (010-doxbench-editor-chat, US5): the doxBench client modules hold the
# static renderer/network boundary. The bundle-wide sweeps above already cover
# them by construction (rglob); this block pins each NEW module BY NAME so a
# future rename or an added transport fails here, in the suite that owns the
# renderer boundary, with a sentence naming the module.
# ----------------------------------------------------------------------------

DOXBENCH_CLIENT_MODULES = (
    WEB / "views" / "doxbench-state.js",
    WEB / "views" / "doxbench-editor.js",
    WEB / "views" / "doxbench-save.js",
)

# The live network primitives a client module could smuggle past the URL sweep
# (EXTERNAL_URL_RE covers XHR/WebSocket/EventSource/sendBeacon but not fetch).
_DOXBENCH_NETWORK_RE = re.compile(
    r"fetch\(|XMLHttpRequest|WebSocket|EventSource|sendBeacon|import\(",
)


def test_doxbench_modules_are_present_and_inside_the_hand_written_sweep():
    own = set(_own_bundle_files())
    for module in DOXBENCH_CLIENT_MODULES:
        assert module.is_file(), f"{module.name} missing from the bundle"
        assert module in own, (
            f"{module.name} escaped the hand-written no-external-asset sweep"
        )


def test_doxbench_state_and_save_are_import_free():
    # The pure halves: no import statement of any kind — their only way out is
    # an injected seam (R2; pinned again here from the renderer's side).
    for module in (DOXBENCH_CLIENT_MODULES[0], DOXBENCH_CLIENT_MODULES[2]):
        source = module.read_text(encoding="utf-8")
        offenders = [
            ln for ln in source.splitlines()
            if ln.lstrip().startswith("import ") or ln.lstrip().startswith("import{")
        ]
        assert not offenders, (module.name, offenders)


def test_doxbench_editor_imports_only_its_own_view_family():
    # The editor is the one doxBench module allowed static imports, and only
    # from the sanitized viewer seam and its own pure state module.
    source = DOXBENCH_CLIENT_MODULES[1].read_text(encoding="utf-8")
    targets = re.findall(r'from\s+"(.+?)"', source)
    assert targets, "editor should import its seams statically"
    assert set(targets) <= {"./viewer.js", "./doxbench-state.js"}, targets


def test_doxbench_modules_construct_no_live_transport():
    for module in DOXBENCH_CLIENT_MODULES:
        source = module.read_text(encoding="utf-8")
        hits = [
            (i + 1, ln.strip())
            for i, ln in enumerate(source.splitlines())
            if _DOXBENCH_NETWORK_RE.search(ln)
        ]
        assert not hits, (module.name, hits)


def test_doxbench_markdown_flows_only_through_the_sanitized_viewer_seam():
    # Renderer boundary (R3): the editor renders preview/prose exclusively via
    # viewer.js's mountSafeMarkdown; no doxBench module names the vendored
    # renderer or assigns raw markup itself.
    editor = DOXBENCH_CLIENT_MODULES[1].read_text(encoding="utf-8")
    assert "mountSafeMarkdown" in editor
    for module in DOXBENCH_CLIENT_MODULES:
        source = module.read_text(encoding="utf-8")
        assert "markdown-it" not in source, module.name
        assert "vendor/" not in source, module.name
        offenders = [
            (i + 1, ln.strip())
            for i, ln in enumerate(source.splitlines())
            if ".innerHTML" in ln and "= \"\"" not in ln and "= ''" not in ln
        ]
        assert not offenders, (module.name, offenders)


# ---------------------------------------------------------------------------
# T100 P1-1 tripwire (operator finding, 2026-08-01): every doxchat-*/doxbench-*
# class a view constructs MUST have at least one styles.css rule. The chat
# rail shipped with ZERO rules and collapsed on real corpus — silently, since
# every suite pins structure, not rendered layout. This guard would have
# caught it at birth.
# ---------------------------------------------------------------------------

def test_every_constructed_doxbench_class_has_a_styles_rule():
    views = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
    styles = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" /
              "styles.css").read_text(encoding="utf-8")
    import re
    constructed = set()
    for name in ("doxbench-chat.js", "doxbench-editor.js",
                 "staging-workbench.js"):
        source = (views / name).read_text(encoding="utf-8")
        for match in re.findall(
                r'(?:el\(\s*"[a-z]+",\s*|\.className\s*=\s*)"([^"]+)"',
                source):
            for cls in match.split():
                if (cls.startswith(("doxchat-", "doxbench-"))
                        and not cls.endswith("-")):
                    constructed.add(cls.split(" ")[0])
        # dynamic status classes built by concatenation
        if 'doxchat-card doxchat-card-" + card.status' in source:
            constructed.update(
                "doxchat-card-" + s for s in
                ("current", "stale", "rejected", "applied"))
        if '"doxchat-turn doxchat-" + turn.role' in source:
            constructed.update(("doxchat-human", "doxchat-assistant"))
    assert constructed, "extraction found nothing — the regex drifted"
    unstyled = sorted(
        cls for cls in constructed if ("." + cls) not in styles)
    assert not unstyled, (
        "constructed classes with ZERO styles.css rules (the T100 P1-1 "
        f"failure class): {unstyled}")
