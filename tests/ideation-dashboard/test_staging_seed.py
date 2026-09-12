"""STAGING-QUEUE seeds drafted from a matrix selection (add-lens-document-selection).

Brett, 2026-08-08: "I should have a checkbox on each one to generate the seed
from checked." The register seed beside it answers the DTN question — does more
than one factory carry the same artifact — which is not the question a reader of
the keyword radar has. Theirs is "these documents keep meeting; what is the
topic?", and the artifact for that is a staging-queue fragment.

Everything here is DETERMINISTIC and WRITE-FREE, and the draft is a SCAFFOLD:
these tests pin all three, including the one that matters most — that the
drafter never argues the case it is seeding.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)
from test_gate_routes import _console_token, _post, _serving

from doc_health import staging_seed as ss
from opendox import serve as serve_mod


def _doc(path, topics, repository=None):
    row = {"id": path, "path": path, "topics": list(topics)}
    if repository:
        row["repository"] = repository
    return row


def test_the_convergence_separates_every_from_some():
    """The spine of the topic and the decisions about it are different facts,
    so the draft prints them apart: a term every selected document carries IS
    what the topic is about; a term only some carry is either in scope or
    evidence that this is really two topics."""
    docs = [_doc("a.md", ["governance", "lens"]),
            _doc("b.md", ["governance", "radar"]),
            _doc("c.md", ["governance", "lens", "radar"])]
    assert ss.convergence(docs) == (["governance"], ["lens", "radar"])
    # no overlap at all is an honest empty spine, never an invented one
    assert ss.convergence([_doc("a.md", ["x"]), _doc("b.md", ["y"])]) \
        == ([], ["x", "y"])
    assert ss.convergence([]) == ([], [])
    # a document with no declared term drags the spine to empty — correct: it
    # cannot be evidence for a term it does not carry
    assert ss.convergence([_doc("a.md", ["x"]), _doc("b.md", [])]) == ([], ["x"])


def test_the_topic_name_comes_from_the_shared_terms_and_never_collides():
    docs = [_doc("a.md", ["doc-workflow", "governance"])] * 2
    assert ss.topic_slug(["doc-workflow", "governance"], ["a.md"]) \
        == "doc-workflow-governance"
    # a folder that already exists is NOT targeted — a seed that silently
    # points at occupied ground invites a human to overwrite staged work
    assert ss.topic_slug(["lens"], ["a.md"], existing=["lens"]) == "lens-2"
    assert ss.topic_slug(["lens"], ["a.md"], existing=["lens", "lens-2"]) \
        == "lens-3"
    # no shared term: fall back to the document itself rather than to nothing
    assert ss.topic_slug([], ["docs/deep/some-note.md"]) == "some-note"
    assert ss.topic_slug([], []) == "untitled-convergence"


def test_the_draft_computes_the_evidence_and_refuses_to_argue_the_case():
    docs = [_doc("docs/a.md", ["governance", "lens"], "openxFactory"),
            _doc("docs/b.md", ["governance"], "MedxFactory")]
    seed = ss.draft_staging_seed(docs, project="domains", as_of="2026-08-08")

    assert seed.path == "ideation/staging/governance/governance.md"
    assert seed.shared == ["governance"] and seed.partial == ["lens"]
    # the queue's header block, in the queue's own grammar
    for header in ("Status: staged", "Kind: capability-proposal", "Topics: ",
                   "Staging ID: ", "Target capabilities: "):
        assert header in seed.text, header
    # the EVIDENCE is computed: every document, its repository, its terms
    assert "- `docs/a.md` (openxFactory) — `governance`, `lens`" in seed.text
    assert "- `docs/b.md` (MedxFactory) — `governance`" in seed.text
    assert "Carried by every one of them: `governance`." in seed.text
    assert "Carried by some: `lens`" in seed.text

    # …and the ARGUMENT is not. Every section a human owes is marked, once,
    # with one greppable marker — a drafter that wrote "why this is staged
    # now" would be the machine deciding what is worth staging.
    for section in ("Why this is staged now", "Claims", "Open questions",
                    "Exit path"):
        assert f"## {section} — {ss.TODO}" in seed.text, section
    assert seed.text.count(ss.TODO) >= 6
    assert "nothing was written" in seed.text

    # deterministic: same selection, same corpus state, byte-identical draft
    assert ss.draft_staging_seed(docs, project="domains",
                                 as_of="2026-08-08").text == seed.text
    # an empty selection is a programming error, not an empty fragment
    try:
        ss.draft_staging_seed([], project="d", as_of="2026-08-08")
        raise AssertionError("an empty selection must refuse")
    except ValueError:
        pass


def test_a_selection_with_no_shared_term_says_so_rather_than_inventing_one():
    """The lens can select any documents at all. When they share nothing, the
    draft must not manufacture a spine — it names the gap as the first thing
    the human has to answer."""
    docs = [_doc("a.md", ["alpha"]), _doc("b.md", ["beta"])]
    seed = ss.draft_staging_seed(docs, project="p", as_of="2026-08-08")
    assert seed.shared == []
    assert "No term is carried by all of them" in seed.text
    assert "human judgment" in seed.text


# ---- the wire ---------------------------------------------------------------

SNAPSHOT_DOCS = [
    {"id": "docs/a.md", "path": "docs/a.md", "topics": ["governance"]},
    {"id": "docs/b.md", "path": "docs/b.md", "topics": ["governance", "lens"]},
]


def _plane():
    return {"schema_version": 1, "kind": "ideation-snapshot",
            "repository": "openxFactory", "documents": SNAPSHOT_DOCS,
            "clusters": [], "possibles": [], "changes": [],
            "staged_topics": [], "keyword_index": [],
            "generation": {"generated_at": "2026-08-08T00:00:00Z"}}


def test_wire_the_route_drafts_from_the_serves_own_snapshot(tmp_path):
    """The client names DOCUMENTS; the terms are read here. A client that could
    supply the terms could claim a convergence the corpus does not have, and
    the fragment's whole value is that its evidence is checkable."""
    with _serving(tmp_path, snapshot=_plane()) as (host, port, root):
        before = sorted(p.name for p in Path(root).rglob("*") if p.is_file())

        status, payload = _post(host, port, "/actions/staging-seed", {})
        assert status == 400 and "documents" in payload["message"]
        status, payload = _post(host, port, "/actions/staging-seed",
                                {"documents": []})
        assert status == 400

        # a document the snapshot does not carry is refused BY NAME rather
        # than silently dropped: a seed missing a selected document would
        # misstate the convergence it claims
        status, payload = _post(host, port, "/actions/staging-seed",
                                {"documents": ["docs/a.md", "nope.md"]})
        assert status == 404 and payload["error"] == "unknown_document"
        assert "nope.md" in payload["message"]

        status, payload = _post(host, port, "/actions/staging-seed",
                                {"documents": ["docs/a.md", "docs/b.md"]})
        assert status == 200, payload
        assert payload["ok"] is True
        assert payload["shared"] == ["governance"]
        assert payload["path"].startswith("ideation/staging/governance/")
        assert payload["index"] == "ideation/staging/INDEX.md"
        # the terms came from the SNAPSHOT, not from the request
        assert "`lens`" in payload["text"]

        # …and the whole exchange wrote nothing anywhere in the checkout
        after = sorted(p.name for p in Path(root).rglob("*") if p.is_file())
        assert after == before


def test_wire_the_route_refuses_a_non_object_body(tmp_path):
    """Pre-existing defect (`#768`, found by Copilot reviewing #761): a body
    that parses as valid JSON but is not an object — a list, a string, a
    number, a bool — used to reach `body.get(...)` and raise `AttributeError`
    in the request thread, leaving the client with no HTTP response at all.
    The handler must refuse it with a clean 400 instead, the same idiom
    `_handle_refresh_action` already uses."""
    with _serving(tmp_path, snapshot=_plane()) as (host, port, root):
        for body in (["not", "a", "dict"], "scalar", 7, True):
            status, payload = _post(host, port, "/actions/staging-seed", body)
            assert status == 400, payload
            assert payload["error"] == "invalid_body"
            assert payload["message"] == serve_mod.JSON_OBJECT_BODY_REQUIRED


def test_wire_the_route_refuses_malformed_json(tmp_path):
    """Malformed JSON is refused by `_read_json_body` itself, before this
    handler ever sees a parsed body — a different refusal path from the
    object-shape guard above, pinned separately so the two are not confused."""
    import http.client
    import json

    with _serving(tmp_path, snapshot=_plane()) as (host, port, root):
        token = _console_token(host, port)
        headers = {"Content-Type": "application/json"}
        if token:
            headers["X-XF-Console-Token"] = token
        conn = http.client.HTTPConnection(host, port, timeout=10)
        conn.request("POST", "/actions/staging-seed", body=b"{not json",
                     headers=headers)
        response = conn.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        status = response.status
        conn.close()
    assert status == 400
    assert payload["error"] == "invalid_body"
    assert payload["message"] == serve_mod.JSON_OBJECT_BODY_REQUIRED


def test_wire_a_scoped_create_then_edit_lands_one_document_with_its_body(tmp_path):
    """Brett, 2026-08-09: "is the issue that we do not have a name to save it
    under?" — yes, and the name existed all along.

    My first attempt sent no scope and read the 400 as proof that a lens draft
    could never reach `edit-document`: a draft has no TILE, so I concluded no
    scope could name it. Wrong. `branch_session` adds an unknown tile to the
    inventory rather than refusing it —

        if tile not in inventory.tiles:
            inventory = TileInventory((*inventory.tiles, tile))

    — which is exactly right for the verb that CREATES a tile's first
    document. The staging seed already computes the name (`<repo>:staging:
    <topic>`), so both verbs can carry it: the create opens the branch session
    `draft/<topic>`, and the edit resolves that same live session and writes
    the body over the header.

    This proves the sequence end to end, which is what the earlier test could
    only guess at.
    """
    from test_gate_routes import _serving   # `_post` carries the console token
    from test_workbench import _commit, _init_git_repo

    scope = {"scope_kind": "staged-topic", "scope_id": "openxFactory:staging:probe"}
    with _serving(tmp_path, snapshot=_plane()) as (host, port, root):
        # a branch session is a GIT branch, so the served checkout has to be a
        # repository — the whole of what the first attempt at this was missing
        _init_git_repo(Path(root))
        _commit(Path(root), "docs/seed.md", "# seed\n")
        # the session branches FROM `main`; `git init` names it `master` here
        subprocess.run(["git", "-C", str(root), "branch", "-M", "main"],
                       check=True, capture_output=True)

        status, created = _post(host, port, "/actions/gate/create-document", {
            "area": "ideation/staging/probe/",
            "title": "A probe topic",
            "summary": "One sentence, written by a human, never generated.",
            "topics": ["governance"],
            "repository_context": "openxFactory",
            "status": "staged", "kind": "capability-proposal", **scope,
        })
        if status != 200:
            pytest.skip("this plane cannot create documents "
                        f"({status}: {created})")
        path = created.get("path")
        assert path, created
        # the create opened a SESSION for a tile that did not exist — the very
        # thing the earlier reading said was impossible
        assert created.get("ref"), created

        # IN A SESSION THE GATE IS ROOTED AT THE WORKTREE, so the document
        # lands on the branch and never in the served checkout — which is the
        # whole point of a session, and is why looking for it under `root`
        # found nothing.
        assert not (Path(root) / path).exists(), "main must not carry a draft"
        landed = next(Path(root).parent.rglob("sessions/*/" + path))
        header = landed.read_text(encoding="utf-8")
        assert "A probe topic" in header
        assert "## The convergence" not in header

        # …and the SAME scope reaches edit-document, which writes the body
        body = header.rstrip() + "\n\n## The convergence (computed)\n\nMine.\n"
        status, verdict = _post(host, port, "/actions/gate/edit-document", {
            "document": path, "content": body, **scope,
        })
        assert status == 200, verdict
        after = landed.read_text(encoding="utf-8")
        assert "A probe topic" in after                     # header survived
        assert "## The convergence (computed)" in after     # body landed
        assert "Mine." in after
