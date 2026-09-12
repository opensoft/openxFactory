"""Cross-repository SHARED IDENTITY seeds (add-shared-identity-seeds).

The DTN promotion process names four ways a candidate is born and the FIRST
— "two or more domain repos use the same structure with different domain
nouns" — had no implementation: the neutrality lane's stage-1 signals ask
domain-vs-openxFactory and one-repo-at-a-time questions. This module answers
it from the dashboard's composed project view and drafts the register's own
intake artifact.

Everything here is DETERMINISTIC and WRITE-FREE: a seed is TEXT a human
merges, and these tests pin both halves of that promise.
"""

from __future__ import annotations

import json
from pathlib import Path

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)
from test_gate_routes import _console_token, _post, _serving

from doc_health import shared_identity as si
from doc_health.families import REGISTER_PATH
from opendox import serve as serve_mod


def _docs(*pairs):
    return [{"id": f"{repo}::{identity}", "path": identity, "repository": repo}
            for repo, identity in pairs]


def test_the_register_path_matches_the_family_constant():
    """The module restates the register's home so a request-path caller need
    not import the family module; the two must never drift."""
    assert si.REGISTER_PATH == REGISTER_PATH


def test_shared_identities_answer_the_registers_first_rule(tmp_path):
    docs = _docs(("adx", "docs/x.md"), ("ledgerx", "docs/x.md"),
                 ("medx", "docs/x.md"), ("adx", "docs/solo.md"),
                 ("ledgerx", "docs/pair.md"), ("medx", "docs/pair.md"))
    rows = si.shared_identities(docs)
    # widest convergence first; a single-carrier identity is not a candidate
    assert [(r.identity, r.repositories) for r in rows] == [
        ("docs/x.md", ("adx", "ledgerx", "medx")),
        ("docs/pair.md", ("ledgerx", "medx")),
    ]
    # the VISIBLE subset governs: asking about two repositories answers about
    # those two, so the seed matches what the human was looking at
    subset = si.shared_identities(docs, repositories=["adx", "ledgerx"])
    assert [(r.identity, r.repositories) for r in subset] == [
        ("docs/x.md", ("adx", "ledgerx"))]
    # nothing shared is an honest empty answer, never an invented candidate
    assert si.shared_identities(docs, repositories=["adx"]) == []
    assert si.shared_identities(None) == []
    # malformed rows are dropped rather than thrown on
    assert si.shared_identities([None, {}, {"repository": "a"}]) == []


def test_the_seed_is_register_format_numbered_from_the_register(tmp_path):
    rows = si.shared_identities(_docs(("adx", "docs/x.md"),
                                      ("ledgerx", "docs/x.md")))
    register = "| DTN-023 | a | | | | |\n### DTN-024: b\n"
    draft = si.draft_seed(register, rows, project="domains", as_of="2026-08-07")

    # numbered past every id the register mentions, rows AND sections
    assert draft.dtn == "DTN-025"
    # a six-cell row in the Candidate List's grammar, seed status/priority
    cells = [c.strip() for c in draft.row.strip().strip("|").split("|")]
    assert len(cells) == 6
    assert cells[0] == "DTN-025" and cells[2] == "`promote`"
    assert cells[3] == si.SEED_PRIORITY and cells[4] == f"`{si.SEED_STATUS}`"
    # the detail section opens with the register's own heading shape
    assert draft.section.startswith("### DTN-025: ")
    # the claim is checkable: the rule is quoted and the carriers listed
    assert si.CANDIDATE_RULE in draft.section
    assert "`docs/x.md` — carried by 2 of 2: adx, ledgerx" in draft.section
    assert "pending human approval" in draft.section
    # and the seed refuses to overclaim: a shared path is not a shared contract
    assert "Domain-local exclusions:" in draft.section

    # deterministic: same corpus state, byte-identical seed
    again = si.draft_seed(register, rows, project="domains", as_of="2026-08-07")
    assert again.as_dict() == draft.as_dict()
    # an empty finding is a programming error, not an empty seed
    try:
        si.draft_seed(register, [], project="domains", as_of="2026-08-07")
        raise AssertionError("an empty finding must refuse")
    except ValueError:
        pass


def test_numbering_starts_at_one_without_a_register():
    rows = si.shared_identities(_docs(("a", "x.md"), ("b", "x.md")))
    assert si.draft_seed("", rows, project="p", as_of="2026-08-07").dtn == "DTN-001"


# ---- the wire ---------------------------------------------------------------

REGISTER = """\
schema_version: 1
kind: project-register
projects:
  - id: core
    name: Core
    repositories: [alpha, beta]
"""


def test_wire_the_seed_route_drafts_and_writes_nothing(tmp_path):
    """The route recomputes the carriers from the SERVE's own composed view —
    the client names the project, never the evidence — and writes nothing."""
    (tmp_path / "project-register.yaml").write_text(REGISTER, encoding="utf-8")
    with _serving(tmp_path) as (host, port, root):
        before = sorted(p.name for p in Path(root).rglob("*") if p.is_file())
        status, payload = _post(host, port, "/actions/dtn-seed", {})
        assert status == 400 and "project_id" in payload["message"]
        status, payload = _post(host, port, "/actions/dtn-seed",
                                {"project_id": "core", "repositories": "no"})
        assert status == 400 and "list" in payload["message"]
        status, payload = _post(host, port, "/actions/dtn-seed",
                                {"project_id": "nope"})
        assert status == 404, payload
        # A single-repository plane composes nothing, so even a REAL register
        # project has no composed view to read carriers from — and the route
        # says so rather than drafting from one repository's documents. No
        # composition, no convergence, no candidate.
        status, payload = _post(host, port, "/actions/dtn-seed",
                                {"project_id": "core"})
        assert status == 404, payload
        assert payload["error"] == "unknown_project"
        # nothing was created anywhere in the checkout
        after = sorted(p.name for p in Path(root).rglob("*") if p.is_file())
        assert after == before


def test_wire_the_seed_route_refuses_a_non_object_body(tmp_path):
    """Pre-existing defect (`#768`, found by Copilot reviewing #761): a body
    that parses as valid JSON but is not an object — a list, a string, a
    number, a bool — used to reach `body.get(...)` and raise `AttributeError`
    in the request thread, leaving the client with no HTTP response at all.
    The handler must refuse it with a clean 400 instead, the same idiom
    `_handle_refresh_action` already uses."""
    with _serving(tmp_path) as (host, port, root):
        for body in (["not", "a", "dict"], "scalar", 7, True):
            status, payload = _post(host, port, "/actions/dtn-seed", body)
            assert status == 400, payload
            assert payload["error"] == "invalid_body"
            assert payload["message"] == serve_mod.JSON_OBJECT_BODY_REQUIRED


def test_wire_the_seed_route_refuses_malformed_json(tmp_path):
    """Malformed JSON is refused by `_read_json_body` itself, before this
    handler ever sees a parsed body — a different refusal path from the
    object-shape guard above, pinned separately so the two are not confused."""
    import http.client

    with _serving(tmp_path) as (host, port, root):
        token = _console_token(host, port)
        headers = {"Content-Type": "application/json"}
        if token:
            headers["X-XF-Console-Token"] = token
        conn = http.client.HTTPConnection(host, port, timeout=10)
        conn.request("POST", "/actions/dtn-seed", body=b"{not json",
                     headers=headers)
        response = conn.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        status = response.status
        conn.close()
    assert status == 400
    assert payload["error"] == "invalid_body"
    assert payload["message"] == serve_mod.JSON_OBJECT_BODY_REQUIRED


def test_wire_a_composed_plane_drafts_from_its_own_carriers(tmp_path):
    """On a plane that CAN compose, the route reads the carriers itself and
    answers with register-format text — and still writes nothing."""
    import http.client

    from test_project_aggregates import _source

    source = _source(tmp_path)                 # alpha + beta, project `pilots`
    composed = source.compose_view("pilots")
    assert composed is not None
    rows = si.shared_identities(composed.get("documents"))
    # the published fixture's two repositories carry the same document paths,
    # which is exactly the convergence this rule is about
    assert rows and all(r.carrier_count >= 2 for r in rows)
    draft = si.draft_seed("", rows, project="pilots", as_of="2026-08-07")
    assert draft.row.startswith("| DTN-001 |")
    assert all(f"`{r.identity}`" in draft.section for r in rows)


def test_a_region_seeds_exactly_its_own_combination():
    """The affordance must not lie about what it drafts: a lens row reading
    "carried by 3" drafts the identities those three share and NOT everything
    the wider visible set happens to share (caught in the live check —
    a 1-document row drafted a 4-artifact seed)."""
    docs = _docs(("a", "all.md"), ("b", "all.md"), ("c", "all.md"),
                 ("a", "ab.md"), ("b", "ab.md"),
                 ("b", "bc.md"), ("c", "bc.md"))
    visible = ["a", "b", "c"]
    # the whole visible set: every convergence, widest first
    assert [r.identity for r in si.shared_identities(docs, repositories=visible)] \
        == ["all.md", "ab.md", "bc.md"]
    # one sector: exactly the identities whose carriers ARE that combination
    assert [r.identity for r in si.shared_identities(
        docs, repositories=visible, exactly=["a", "b"])] == ["ab.md"]
    # the centre is the same rule with the whole set as the combination
    assert [r.identity for r in si.shared_identities(
        docs, repositories=visible, exactly=visible)] == ["all.md"]
    # a combination nothing matches yields nothing, never a near miss
    assert si.shared_identities(docs, repositories=visible,
                                exactly=["a", "c"]) == []
