"""`/source` serves GOVERNANCE DOCUMENTS — never a dot-directory (T092
acceptance sweep, defect 10).

The sweep pointed the read-only pass-through at a real checkout and asked it for
`/source/.git/config`. It answered 200 text/plain with the full remote
configuration — in a real checkout an https remote with an embedded PAT, handed
to any page on the CSP-free local origin for as long as the dashboard runs — and
`/source/.git/logs/HEAD` answered with the committer's name and email. Bounded
today by the loopback-only bind, which is not a boundary the resolver may rely
on, and which must not still be the only one when a non-loopback bind exists.

WHY THE EXISTING SUITE MISSED IT, restated as the design rule for this file.
`test_renderer.py` parametrizes seven ESCAPE shapes (`../../../etc/passwd`,
`%2e%2e/`, `..%2f`, `//etc/passwd`) and they all pass, before this fix and
after: the confinement is CORRECT and is not what was missing. Every one of
those cases asks "can the tail leave the root". None asks "is this in-root
target one `/source` should serve". So this file is deliberately the
LEGITIMATE-PATH, FORBIDDEN-TARGET half — every path here resolves cleanly inside
the served root and must still be refused.

And it needs a REAL `.git`, which is why it builds a `scratch_repo`
(`build_scratch_repo`, multi-topic) rather than pointing at the fixture tree:
`tests/ideation-dashboard/fixtures/base-repo/` has no `.git` of its own, so the
`.git` cases 404 there for the wrong reason and would have passed unfixed.
"""

from __future__ import annotations

import http.client
import threading
from contextlib import contextmanager

import pytest

from conftest import REPO_ROOT

from ideation_dashboard import serve as serve_mod
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.generator import generate_snapshot

from session_fixtures import build_scratch_repo  # noqa: F401  (harness)

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"

# Two staged topics beyond the default, so the served corpus is the multi-topic
# shape the rest of this wave's regressions use — a single-topic world hides
# whole classes of defect and this suite has been bitten by it once already.
EXTRA_TOPICS = ("second-topic", "third-topic")

# Legitimate, in-root, resolvable — and none of them a governance document.
FORBIDDEN_TAILS = [
    ".git/config",
    ".git/HEAD",
    ".git/logs/HEAD",
    "%2egit/config",                       # percent-encoded dot, decoded first
    ".git/refs/heads/main",
    ".hidden/secret.md",                   # a dot-DIRECTORY holding a .md
    "ideation/.hidden/secret.md",          # a dot-directory nested mid-path
    "ideation/staging/.env",               # an extensionless dot FILE
    ".env.production",                     # ...and one with an unserved suffix
    ".gitignore",
]

# The corpus's ONE legitimate dotfile family. Every OpenSpec change folder holds
# `.openspec.yaml`; the generator's `rglob` puts all of them into
# `changes[].files` and the explorer renders that list as clickable rows, so a
# blanket no-dotfile rule would 404 a path the surface itself offers.
SERVED_DOTFILE = "openspec/changes/demo-change/.openspec.yaml"


@pytest.fixture(scope="module")
def served(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("source-dot-dirs")
    repo = build_scratch_repo(tmp_path, extra_topics=EXTRA_TOPICS)
    # the two dot targets git does not create for us
    (repo.root / ".hidden").mkdir()
    (repo.root / ".hidden" / "secret.md").write_text("# not a document\n", encoding="utf-8")
    (repo.root / "ideation" / ".hidden").mkdir(parents=True, exist_ok=True)
    (repo.root / "ideation" / ".hidden" / "secret.md").write_text("# nor this\n",
                                                                  encoding="utf-8")
    (repo.root / "ideation" / "staging" / ".env").write_text("TOKEN=hunter2\n",
                                                             encoding="utf-8")
    (repo.root / ".env.production").write_text("TOKEN=hunter3\n", encoding="utf-8")
    (repo.root / ".gitignore").write_text("*.pyc\n", encoding="utf-8")
    served = repo.root / SERVED_DOTFILE
    served.parent.mkdir(parents=True, exist_ok=True)
    served.write_text("schema_version: 1\nkind: change\n", encoding="utf-8")
    assert (repo.root / ".git" / "config").is_file(), "the harness built no real .git"
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(
        __import__("json").dumps(generate_snapshot(repo.root, repo.repository)),
        encoding="utf-8")
    return repo, snap_path


@contextmanager
def _serving(repo, snapshot_path):
    httpd = serve_mod.build_server(WEB, snapshot_path, repo.root,
                                   repository=repo.repository, actor="tester")
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield host, port
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _raw_get(host, port, raw_path):
    """A RAW request-line path, so the server's own resolver is what answers."""
    conn = http.client.HTTPConnection(host, port, timeout=5)
    conn.putrequest("GET", raw_path, skip_host=False, skip_accept_encoding=True)
    conn.putheader("Host", f"{host}:{port}")
    conn.endheaders()
    resp = conn.getresponse()
    body = resp.read()
    conn.close()
    return resp.status, body


# ---------------------------------------------------------------------------
# the pure resolver
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tail", FORBIDDEN_TAILS)
def test_resolve_within_refuses_a_dot_directory_target(served, tail):
    repo, _ = served
    assert reg.resolve_within(repo.root, tail) is None, \
        f"/source resolved {tail!r} — a legitimate in-root path it must not serve"


def test_resolve_source_path_refuses_the_same_targets(served):
    """The serve-side entry point is the same check, so the two cannot diverge."""
    repo, _ = served
    for tail in FORBIDDEN_TAILS:
        assert serve_mod.resolve_source_path(repo.root, tail) is None, tail


def test_the_exclusion_does_not_narrow_what_source_is_for(served):
    """A governance document still resolves. The refusal is targeted at
    dot-prefixed components, not at 'anything unusual'."""
    repo, _ = served
    for topic in (repo.topic_id, *EXTRA_TOPICS):
        rel = f"ideation/staging/{topic}/README.md"
        assert reg.resolve_within(repo.root, rel) is not None, rel
    # a filename that merely CONTAINS a dot is untouched
    assert reg.resolve_within(repo.root, f"ideation/staging/{repo.topic_id}/README.md")


def test_the_one_dotfile_the_surface_itself_offers_still_serves(served):
    """The narrowing that keeps this honest. `changes[].files` is built by the
    generator's `rglob`, so every change folder's `.openspec.yaml` is in the
    snapshot and the explorer renders it as a clickable row. A blanket
    no-dot-prefixed-name rule would 404 a path the dashboard itself offers, so
    a dot-FILE with a projected extension is served while its dot-DIRECTORY
    siblings are not."""
    repo, snap_path = served
    assert reg.resolve_within(repo.root, SERVED_DOTFILE) is not None
    with _serving(repo, snap_path) as (host, port):
        status, body = _raw_get(host, port, "/source/" + SERVED_DOTFILE)
    assert status == 200
    assert body == (repo.root / SERVED_DOTFILE).read_bytes()


def test_a_dot_directory_is_refused_even_when_it_holds_a_served_extension(served):
    """The extension allowlist reaches the FILE name only: `.hidden/secret.md`
    has the most document-shaped extension there is and is still refused,
    because the directory is what the rule is about."""
    repo, _ = served
    assert reg.resolve_within(repo.root, ".hidden/secret.md") is None
    assert reg.resolve_within(repo.root, "ideation/.hidden/secret.md") is None


def test_the_containment_check_is_unchanged(served):
    """Stated so nobody 'simplifies' the resolver while reading this file: the
    escape shapes were correct before and are correct now."""
    repo, _ = served
    for tail in ("../../../etc/passwd", "%2e%2e/%2e%2e/etc/passwd",
                 "/etc/passwd", "does/not/exist.md"):
        assert reg.resolve_within(repo.root, tail) is None, tail


# ---------------------------------------------------------------------------
# over real HTTP, against a real .git
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tail", FORBIDDEN_TAILS)
def test_the_source_route_refuses_a_dot_directory(served, tail):
    repo, snap_path = served
    with _serving(repo, snap_path) as (host, port):
        status, body = _raw_get(host, port, "/source/" + tail)
    assert status == 404, f"/source/{tail} answered {status}"
    # and nothing leaked in the refusal body
    assert b"[remote " not in body and b"url =" not in body
    assert b"TOKEN=" not in body


def test_the_keyed_source_route_refuses_it_too(served):
    """Per-entry confinement runs through the same `resolve_within`, so the
    keyed form must not be a second door onto the same bytes."""
    repo, snap_path = served
    key = f"{repo.repository}@{reg.DEFAULT_REF}"
    with _serving(repo, snap_path) as (host, port):
        status, body = _raw_get(host, port, f"/source/{key}/.git/config")
        ok_status, ok_body = _raw_get(
            host, port, f"/source/{key}/ideation/staging/{repo.topic_id}/README.md")
    assert status == 404
    assert b"url =" not in body
    assert ok_status == 200 and ok_body, "the keyed route stopped serving documents"


def test_a_governance_document_still_serves_over_http(served):
    repo, snap_path = served
    rel = f"ideation/staging/{EXTRA_TOPICS[0]}/README.md"
    with _serving(repo, snap_path) as (host, port):
        status, body = _raw_get(host, port, "/source/" + rel)
    assert status == 200
    assert body == (repo.root / rel).read_bytes()
