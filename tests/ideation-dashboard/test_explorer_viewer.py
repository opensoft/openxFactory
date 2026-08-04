"""US4 drill-down explorer + read-only viewer tests (T019):

  * explorer listing derivation — the ACTUAL explorer.js run in node against
    the real fixture snapshot (mirroring test_renderer.py's model.js pattern),
    plus a Python-side check that the generator's `staged_topics[].files` /
    `changes[].files` fields the explorer reads actually match the fixture
    repo's real directory tree (folder listings match the fixture repo tree);
  * viewer fetch path — serve.py integration over real HTTP: a rendered
    response for a real fixture doc reachable through the explorer's own
    derived file list, and 404s (including a stale/regenerated-snapshot
    path, not just path-traversal attacks already covered in
    test_renderer.py);
  * vendored-renderer integrity — the file exists, is a real markdown-it
    build, contains zero LIVE network primitives (test_renderer.py's
    bundle-wide scan excludes vendor/ from the generic URL-substring check,
    since the vendored library's own link-normalization logic legitimately
    contains "http://" string literals; THIS test asserts the stronger,
    narrower invariant that actually matters — no fetch/XHR/WebSocket/etc.),
    and that html/code-escaping actually behaves as configured (raw HTML
    escaped, fenced code content escaped);
  * divergence banner logic — unit-level, on the header value alone, via the
    real viewer.js run in node (no DOM/fetch needed for these pure helpers).

All against the REAL fixture snapshot, generated in-test via the same
FakeGit + PINNED_REVISION substrate as test_generator.py/test_renderer.py.
"""

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
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
EXPLORER_JS = WEB / "views" / "explorer.js"
VIEWER_JS = WEB / "views" / "viewer.js"
VENDOR_JS = WEB / "vendor" / "markdown-it.min.js"
NODE = shutil.which("node")


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


# ----------------------------------------------------------------------------
# explorer listing derivation — the ACTUAL explorer.js, run in node
# ----------------------------------------------------------------------------

_EXPLORER_HARNESS = """
import { resolveExplorerTarget, classifyChangeFile } from './explorer.mjs';
import { readFileSync } from 'node:fs';
const snap = JSON.parse(readFileSync(process.argv[2], 'utf8'));

const out = {
  staged: resolveExplorerTarget('staged', 'ideation-governance', snap),
  proposal: resolveExplorerTarget('proposal', 'add-ideation-governance', snap),
  realized: resolveExplorerTarget('realized', 'add-document-cataloging', snap),
  unknownKind: resolveExplorerTarget('bogus', 'x', snap),
  unknownId: resolveExplorerTarget('staged', 'does-not-exist', snap),
  classify: {
    proposal: classifyChangeFile('openspec/changes/foo/proposal.md'),
    design: classifyChangeFile('openspec/changes/foo/design.md'),
    tasks: classifyChangeFile('openspec/changes/foo/tasks.md'),
    specDeltas: classifyChangeFile('openspec/changes/foo/specs/bar/spec.md'),
    supportingDocs: classifyChangeFile('openspec/changes/foo/supporting-docs/x.md'),
    other: classifyChangeFile('openspec/changes/foo/notes.txt'),
  },
};
console.log(JSON.stringify(out));
"""


def _run_node_explorer(snapshot, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(EXPLORER_JS, tmp_path / "explorer.mjs")
    (tmp_path / "harness.mjs").write_text(_EXPLORER_HARNESS, encoding="utf-8")
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot), encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(tmp_path / "harness.mjs"), str(snap_path)],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_explorer_js_exists_and_is_importable_standalone():
    assert EXPLORER_JS.is_file()
    # No `import` statement referencing viewer.js — the two modules are
    # decoupled (mountExplorer takes an onOpenFile callback instead), so
    # explorer.js is independently landable/testable. (Doc comments may still
    # mention "viewer.js" by name, hence checking import statements only.)
    imports = re.findall(r'^\s*import\s.*$', EXPLORER_JS.read_text(encoding="utf-8"), re.MULTILINE)
    assert not imports, imports


def test_staged_tile_lists_the_topic_folder_with_headers(tmp_path):
    r = _run_node_explorer(_snapshot(), tmp_path)
    staged = r["staged"]
    assert staged["kind"] == "staged"
    assert staged["id"] == "ideation-governance"
    files = staged["groups"][0]["files"]
    assert [f["path"] for f in files] == ["ideation/staging/ideation-governance/README.md"]
    # headers (status/kind/summary) come from the matched documents[] entry
    doc = files[0]["doc"]
    assert doc is not None
    assert doc["stage"] == "staged"
    assert doc["kind"]
    assert doc["summary"]


def test_aggregate_folder_entry_keeps_its_member_source_key(tmp_path):
    if not NODE:
        pytest.skip("node not available for the explorer derivation probe")
    path = "ideation/staging/shared/README.md"
    snapshot = {
        "repository": "all",
        "documents": [
            {"id": "alpha::doc", "path": path, "repository": "alpha",
             "ref": "draft/alpha", "summary": "alpha"},
            {"id": "beta::doc", "path": path, "repository": "beta",
             "ref": "main", "summary": "beta"},
        ],
        "staged_topics": [
            {"staging_id": "beta::shared", "files": [path],
             "repository": "beta", "ref": "main"},
        ],
    }
    # Drive the real resolver with the aggregate's namespaced tile id.
    shutil.copy(EXPLORER_JS, tmp_path / "aggregate-explorer.mjs")
    script = """
import { resolveExplorerTarget } from './aggregate-explorer.mjs';
const snapshot = JSON.parse(process.argv[2]);
console.log(JSON.stringify(resolveExplorerTarget('staged', 'beta::shared', snapshot)));
"""
    harness = tmp_path / "aggregate-harness.mjs"
    harness.write_text(script, encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(harness), json.dumps(snapshot)],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stderr
    [entry] = json.loads(proc.stdout)["groups"][0]["files"]
    assert entry["repository"] == "beta"
    assert entry["ref"] == "main"
    assert entry["doc"]["summary"] == "beta"


def test_aggregate_folder_entry_disambiguates_same_repository_refs(tmp_path):
    if not NODE:
        pytest.skip("node not available for the explorer derivation probe")
    path = "ideation/staging/shared/README.md"
    snapshot = {
        "repository": "all",
        "documents": [
            {"id": "alpha::main-doc", "path": path, "repository": "alpha",
             "ref": "main", "summary": "main"},
            {"id": "alpha::draft-doc", "path": path, "repository": "alpha",
             "ref": "draft/shared", "summary": "draft"},
        ],
        "staged_topics": [
            {"staging_id": "alpha::shared", "files": [path],
             "repository": "alpha", "ref": "draft/shared"},
        ],
    }
    shutil.copy(EXPLORER_JS, tmp_path / "aggregate-explorer.mjs")
    script = """
import { resolveExplorerTarget } from './aggregate-explorer.mjs';
const snapshot = JSON.parse(process.argv[2]);
console.log(JSON.stringify(resolveExplorerTarget('staged', 'alpha::shared', snapshot)));
"""
    harness = tmp_path / "aggregate-ref-harness.mjs"
    harness.write_text(script, encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(harness), json.dumps(snapshot)],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stderr
    [entry] = json.loads(proc.stdout)["groups"][0]["files"]
    assert entry["repository"] == "alpha"
    assert entry["ref"] == "draft/shared"
    assert entry["doc"]["summary"] == "draft"


def test_aggregate_wheel_navigation_threads_the_owning_member_key():
    """Wheel reads cannot resolve aggregate ownership from a path alone."""
    app = (WEB / "app.js").read_text(encoding="utf-8")
    wheel = (WEB / "views" / "wheel.js").read_text(encoding="utf-8")
    assert "openDoc: (path, doc, owner) =>" in app
    assert "sourceKeyFor(owner || doc)" in app
    assert ("path, opts.wheelKey === \"documents\" ? item.ref : null, item.ref"
            in wheel)
    assert "nav.openDoc(entry.path, null, item.ref);" in wheel
    explorer = EXPLORER_JS.read_text(encoding="utf-8")
    assert ("docByPath(snapshot, path, sourceKey?.repository, sourceKey?.ref)"
            in explorer)
    assert "resolved?.repository || sourceKey?.repository || null" in explorer
    assert "resolved?.ref || sourceKey?.ref || null" in explorer


def test_proposal_tile_groups_proposal_and_tasks(tmp_path):
    r = _run_node_explorer(_snapshot(), tmp_path)
    proposal = r["proposal"]
    assert proposal["kind"] == "proposal"
    labels = [g["label"] for g in proposal["groups"]]
    assert labels == ["proposal", "tasks"]  # fixture has no design/spec-deltas/supporting-docs
    paths = {f["path"] for g in proposal["groups"] for f in g["files"]}
    assert paths == {
        "openspec/changes/add-ideation-governance/proposal.md",
        "openspec/changes/add-ideation-governance/tasks.md",
    }


def test_realized_tile_lists_the_archived_change_folder(tmp_path):
    r = _run_node_explorer(_snapshot(), tmp_path)
    realized = r["realized"]
    assert realized["kind"] == "realized"
    assert realized["subtitle"] == "openspec/changes/archive/2026-07-12-add-document-cataloging"
    paths = {f["path"] for g in realized["groups"] for f in g["files"]}
    assert paths == {"openspec/changes/archive/2026-07-12-add-document-cataloging/proposal.md"}


def test_unresolvable_tile_and_kind_degrade_to_null(tmp_path):
    r = _run_node_explorer(_snapshot(), tmp_path)
    assert r["unknownKind"] is None
    assert r["unknownId"] is None


def test_change_file_classification(tmp_path):
    r = _run_node_explorer(_snapshot(), tmp_path)
    assert r["classify"] == {
        "proposal": "proposal", "design": "design", "tasks": "tasks",
        "specDeltas": "spec deltas", "supportingDocs": "supporting docs", "other": "other",
    }


# ----------------------------------------------------------------------------
# folder listings match the fixture repo's REAL directory tree (not just the
# JS derivation over a given snapshot — the snapshot's own files fields must
# be accurate against disk, since the explorer never scans the repo itself)
# ----------------------------------------------------------------------------

def test_staged_topic_files_match_the_real_directory_tree():
    snap = _snapshot()
    staged = {t["staging_id"]: t for t in snap["staged_topics"]}
    for staging_id, topic in staged.items():
        real = sorted(
            p.relative_to(BASE_REPO).as_posix()
            for p in (BASE_REPO / "ideation" / "staging" / staging_id).rglob("*") if p.is_file()
        )
        assert topic.get("files", []) == real, staging_id


def test_change_files_match_the_real_directory_tree():
    snap = _snapshot()
    by_id = {c["id"]: c for c in snap["changes"]}
    active = by_id["add-ideation-governance"]
    assert active["folder"] == "openspec/changes/add-ideation-governance"
    assert active["files"] == [
        "openspec/changes/add-ideation-governance/proposal.md",
        "openspec/changes/add-ideation-governance/tasks.md",
    ]
    archived = by_id["add-document-cataloging"]
    assert archived["folder"] == "openspec/changes/archive/2026-07-12-add-document-cataloging"
    assert archived["files"] == [
        "openspec/changes/archive/2026-07-12-add-document-cataloging/proposal.md",
    ]
    for change in snap["changes"]:
        real = sorted(
            p.relative_to(BASE_REPO).as_posix()
            for p in (BASE_REPO / change["folder"]).rglob("*") if p.is_file()
        )
        assert change.get("files", []) == real, change["id"]


# ----------------------------------------------------------------------------
# viewer fetch path — serve.py integration over real HTTP
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


def _get(host, port, path):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.request("GET", path)
    resp = conn.getresponse()
    body = resp.read()
    headers = {k.lower(): v for k, v in resp.getheaders()}
    conn.close()
    return resp.status, headers, body


def test_viewer_source_fetch_renders_a_real_doc_reachable_from_the_explorer(tmp_path):
    # The exact path the explorer's staged-tile listing hands the viewer.
    snap = _snapshot()
    staged = {t["staging_id"]: t for t in snap["staged_topics"]}
    rel = staged["ideation-governance"]["files"][0]
    with _serving(tmp_path, head=PINNED_REVISION) as (host, port):
        status, headers, body = _get(host, port, "/source/" + rel)
    assert status == 200
    assert "text/markdown" in headers.get("content-type", "")
    assert body == (BASE_REPO / rel).read_bytes()
    assert headers.get("x-snapshot-divergence") == "aligned"


def test_viewer_source_fetch_renders_a_change_folder_doc(tmp_path):
    snap = _snapshot()
    by_id = {c["id"]: c for c in snap["changes"]}
    rel = by_id["add-ideation-governance"]["files"][0]
    with _serving(tmp_path, head=PINNED_REVISION) as (host, port):
        status, headers, body = _get(host, port, "/source/" + rel)
    assert status == 200
    assert body == (BASE_REPO / rel).read_bytes()


def test_viewer_source_fetch_404_for_a_stale_snapshot_reference(tmp_path):
    # A file the snapshot never listed (simulating drift after regeneration,
    # not an attack) — the pass-through must still 404, never fabricate.
    with _serving(tmp_path, head=PINNED_REVISION) as (host, port):
        status, _, _ = _get(host, port,
                             "/source/ideation/staging/ideation-governance/no-longer-there.md")
    assert status == 404


def test_viewer_source_fetch_404_for_path_traversal():
    assert serve_mod.resolve_source_path(BASE_REPO, "../../../../etc/passwd") is None


def test_viewer_surfaces_diverged_header_on_the_same_doc(tmp_path):
    snap = _snapshot()
    rel = snap["staged_topics"][0]["files"][0]
    with _serving(tmp_path, head="f" * 40) as (host, port):
        status, headers, _ = _get(host, port, "/source/" + rel)
    assert status == 200
    assert headers.get("x-snapshot-divergence") == "diverged"


# ----------------------------------------------------------------------------
# vendored-renderer integrity
# ----------------------------------------------------------------------------

def test_vendor_file_exists_and_is_the_expected_library():
    assert VENDOR_JS.is_file()
    text = VENDOR_JS.read_text(encoding="utf-8")
    assert text.startswith("/*! markdown-it")
    assert "@license MIT" in text.splitlines()[0]
    assert VENDOR_JS.stat().st_size > 50_000  # a real build, not a stub


_LIVE_NETWORK_PRIMITIVE_RE = re.compile(
    r"fetch\(|XMLHttpRequest|WebSocket|EventSource|navigator\.sendBeacon|\.postMessage\(",
    re.IGNORECASE,
)


def test_vendor_file_contains_no_live_network_primitives():
    # The vendored library's own internal string literals mention "http://"
    # as part of its (disabled, in our config) link-normalization logic —
    # test_renderer.py's bundle-wide URL scan excludes vendor/ for exactly
    # that reason. What actually matters for supply-chain trust is that the
    # vendored code never itself CALLS OUT — asserted directly here.
    text = VENDOR_JS.read_text(encoding="utf-8")
    offenders = _LIVE_NETWORK_PRIMITIVE_RE.findall(text)
    assert not offenders, offenders


def test_viewer_js_only_import_is_the_vendor_file():
    text = VIEWER_JS.read_text(encoding="utf-8")
    imports = re.findall(r'^\s*import\s.*$', text, re.MULTILINE)
    assert len(imports) == 1
    assert "vendor/markdown-it.min.js" in imports[0]


@pytest.mark.skipif(not NODE, reason="node not available")
def test_vendor_html_disabled_escapes_raw_html_and_code_content(tmp_path):
    # Exercises the ACTUAL vendored build via node's CJS `require` (the UMD
    # wrapper's first branch — the same code path a browser's `html:false`
    # config takes once loaded as a global). Proves the orchestrator's
    # "html option DISABLED" decision is real, not just configured-and-hoped:
    # a raw HTML block is escaped to inert text, and fenced code content is
    # escaped too (markdown-it always escapes code, independent of `html`).
    script = f"""
const markdownit = require({json.dumps(str(VENDOR_JS))});
const md = markdownit({{ html: false, linkify: false, typographer: false }});
const out = md.render("# Hi\\n\\n<script>alert(1)</script>\\n\\n```js\\nconst x = '<b>bold</b>';\\n```\\n");
console.log(JSON.stringify(out));
"""
    proc = subprocess.run([NODE, "-e", script], capture_output=True, text=True, cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    rendered = json.loads(proc.stdout)
    assert "<h1>Hi</h1>" in rendered
    # the raw <script> tag is escaped to text, never emitted as a live tag
    assert "<script>alert(1)</script>" not in rendered
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in rendered
    # fenced code content is escaped too, independent of the html option
    assert "&lt;b&gt;bold&lt;/b&gt;" in rendered
    assert "<b>bold</b>" not in rendered


# ----------------------------------------------------------------------------
# divergence banner logic — unit-level, on the header value alone
# ----------------------------------------------------------------------------

_VIEWER_HARNESS = """
import {
  divergenceBannerText, isFileProtocol, NO_SHIM_MESSAGE, runEditAction,
} from './viewer.mjs';
const editCalls = [];
const successButton = { textContent: '✎ edit', disabled: false };
const successStatus = { textContent: '', hidden: true };
await runEditAction(successButton, successStatus, 'ideation/example.md', {
  enabled: true,
  async open(path) { editCalls.push(path); return { ok: true, path }; },
});
const failureButton = { textContent: '✎ edit', disabled: false };
const failureStatus = { textContent: '', hidden: true };
await runEditAction(failureButton, failureStatus, 'ideation/missing.md', {
  enabled: true,
  async open() { throw new Error('document unavailable'); },
});
console.log(JSON.stringify({
  diverged: divergenceBannerText('diverged'),
  aligned: divergenceBannerText('aligned'),
  unknown: divergenceBannerText('unknown'),
  missing: divergenceBannerText(null),
  fileProtocol: isFileProtocol({ protocol: 'file:' }),
  httpProtocol: isFileProtocol({ protocol: 'http:' }),
  noLoc: isFileProtocol(null),
  noShimMessage: NO_SHIM_MESSAGE,
  edit: {
    calls: editCalls,
    successButton,
    successStatus,
    failureButton,
    failureStatus,
  },
}));
"""


def _run_node_viewer_pure(tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    # Preserve the real web/ layout (views/viewer.js importing ../vendor/...)
    # so the copied module's relative import resolves exactly as it does in
    # the actual bundle.
    (tmp_path / "views").mkdir(exist_ok=True)
    (tmp_path / "vendor").mkdir(exist_ok=True)
    shutil.copy(VIEWER_JS, tmp_path / "views" / "viewer.mjs")
    # The vendor side-effect import runs harmlessly under node (it resolves
    # via node's CJS loader for a plain .js file with no package.json "type",
    # so it never sets globalThis.markdownit there — irrelevant to these pure
    # functions, which never call the renderer).
    shutil.copy(VENDOR_JS, tmp_path / "vendor" / "markdown-it.min.js")
    harness = tmp_path / "views" / "harness.mjs"
    harness.write_text(_VIEWER_HARNESS, encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(harness)], capture_output=True, text=True, cwd=tmp_path,
    )
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_divergence_banner_text_only_fires_on_diverged(tmp_path):
    r = _run_node_viewer_pure(tmp_path)
    assert r["diverged"] == "snapshot behind checkout — regenerate"
    assert r["aligned"] is None
    assert r["unknown"] is None
    assert r["missing"] is None


def test_is_file_protocol(tmp_path):
    r = _run_node_viewer_pure(tmp_path)
    assert r["fileProtocol"] is True
    assert r["httpProtocol"] is False
    assert r["noLoc"] is False


def test_no_shim_message_text(tmp_path):
    r = _run_node_viewer_pure(tmp_path)
    assert r["noShimMessage"] == "viewer requires the serve shim — run generate-and-open"


def test_select_to_edit_reports_success_and_failure_in_place(tmp_path):
    edit = _run_node_viewer_pure(tmp_path)["edit"]
    assert edit["calls"] == ["ideation/example.md"]
    assert edit["successButton"] == {"textContent": "✎ edit", "disabled": False}
    assert edit["successStatus"] == {
        "textContent": "opened in your editor — ideation/example.md",
        "hidden": False,
    }
    assert edit["failureButton"] == {"textContent": "✎ edit", "disabled": False}
    assert edit["failureStatus"] == {
        "textContent": "could not open editor: document unavailable",
        "hidden": False,
    }
