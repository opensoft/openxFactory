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

from pathlib import Path

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)
from test_gate_routes import _post, _serving

from doc_health import staging_seed as ss


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
