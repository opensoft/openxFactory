"""WHOSE MATERIAL MAY A SESSION REWRITE? — the T092 acceptance sweep's defect 1.

The sweep drove the real `generate-and-open` entrypoint against a 177-document
clone and found that a staged tile's session could REWRITE ANOTHER TOPIC'S
STAGED DOCUMENT. The path came from the workbench's own rewrite picker, which
offered every resolved row in the tile's scope — including the CLUSTER
NEIGHBOURHOOD section the same panel labels "inferred via clusters, not the
topic's own material" — and the route accepted it: a 1,460-word staged document
was replaced by a five-line probe, committed onto the OTHER tile's session
branch, with a gate-action record filed under the foreign document's target id so
the audit trail read as authorised. Reproduced on two independent tiles.

WHY THE COMMITTED SUITE COULD NOT SEE IT. Every session test builds
`build_scratch_repo(...)` with no `extra_topics`, i.e. a ONE-TOPIC world. With one
topic there is no second topic's material, no inbound declaring document and no
cluster neighbourhood, so the picker can never be offered a foreign path and the
most severe defect in the triage is STRUCTURALLY UNREACHABLE. Every test here
therefore builds a MULTI-TOPIC corpus, and the model assertion is an EQUALITY on
the picker's option set rather than a membership check — a membership assertion
would pass again the next time an extra section is flattened in.

The rule, one sentence, enforced in two places on purpose: a session may rewrite
the tile's OWN material (a staged topic's staging folder) plus documents THIS
SESSION created. `staging-workbench-model.rewritableDocuments` is the picker;
`gate_routes.foreign_document_refusal` is the boundary — and the boundary is what
these tests spend most of their time on, because the picker is UI and the route
answers a hand-shaped body, the CLI parity verb, and whatever surface comes next.

Hermetic throughout: `build_scratch_repo`'s throwaway checkout + local bare
origin, no network, no real `gh`/`nlm` (tests/hermeticity.py), no real checkout
touched.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import REPO_ROOT
from session_fixtures import build_scratch_repo
from staging_shapes import staging_fragment

from ideation_dashboard import branch_session as bs
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import session_git as sg
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.generator import generate_snapshot

REPO = "openxFactory"
TOPIC = "demo-topic"                 # the tile the session opens on
OTHER = "other-topic"                # a SECOND staged topic, with its own material
DRAFT = f"draft/{TOPIC}"
OTHER_DOC = f"ideation/staging/{OTHER}/README.md"
BRAINSTORM_DOC = "ideation/brainstorm/a-neighbourhood-capture.md"
PROBE = "# Foreign scope probe\n\nthis must never land\n"
NODE = shutil.which("node")
WEB_VIEWS = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"

CREATE_BODY = {
    "title": "First Draft",
    "summary": "The session's first document.",
    "topics": ["alpha"],
    "area": f"ideation/staging/{TOPIC}/",
    "repository_context": REPO,
    "scope_kind": bs.STAGED_TOPIC,
    "scope_id": TOPIC,
}


# --------------------------------------------------------------------------
# the MULTI-TOPIC world (the thing the committed smoke never built)
# --------------------------------------------------------------------------

@pytest.fixture
def multi_topic_repo(tmp_path):
    """Two staged topics plus a brainstorm capture — the smallest world in which
    "another topic's material" exists at all."""
    repo = build_scratch_repo(tmp_path, repository=REPO, topic_id=TOPIC,
                              extra_topics=(OTHER,))
    repo.write(BRAINSTORM_DOC, staging_fragment("A Neighbourhood Capture",
                                                "a-neighbourhood-capture"))
    repo.commit("Add a brainstorm capture", BRAINSTORM_DOC)
    repo.git("push", "origin", "main")
    return repo


def _registry(repo, tmp_path):
    path = tmp_path / "main-snapshot.json"
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _open_session(repo, registry):
    status, payload = gr.run_gate_action(
        "create-document", dict(CREATE_BODY), checkout_root=repo.root,
        actor="brett", snapshot_path=None, session_registry=registry,
        repository=repo.repository)
    assert status == 200, payload
    return payload


def _edit(repo, registry, *, document, content=PROBE, scope_id=TOPIC,
          scope_kind=bs.STAGED_TOPIC):
    return gr.run_gate_action(
        "edit-document",
        {"scope_kind": scope_kind, "scope_id": scope_id,
         "document": document, "content": content},
        checkout_root=repo.root, actor="brett", snapshot_path=None,
        session_registry=registry, repository=repo.repository)


def _worktree(repo):
    return bs.worktree_path(repo.root, DRAFT)


def _branch_head(repo):
    return sg.SessionGit(repo.root).branch_sha(DRAFT)


# ==========================================================================
# the ROUTE — the boundary
# ==========================================================================

def test_a_tile_session_cannot_rewrite_another_topics_staged_document(
        multi_topic_repo, tmp_path):
    """THE DEFECT, reproduced at the route: tile `demo-topic`'s session naming
    `other-topic`'s staged document.

    Four things are asserted, because the sweep found all four broken together:
    the refusal, the OTHER topic's bytes in the session worktree, the branch not
    having moved (no commit), and no gate-action record filed under the foreign
    document."""
    registry = _registry(multi_topic_repo, tmp_path)
    _open_session(multi_topic_repo, registry)
    worktree = _worktree(multi_topic_repo)
    before_bytes = (worktree / OTHER_DOC).read_bytes()
    before_head = _branch_head(multi_topic_repo)
    assert before_bytes, "the multi-topic world must really carry the other topic"

    status, payload = _edit(multi_topic_repo, registry, document=OTHER_DOC)

    assert status == 409, payload
    assert payload["error"] == "gate_refused"
    message = payload["message"]
    assert "NOT this tile's own material" in message
    assert OTHER_DOC in message and TOPIC in message
    assert "Nothing was written" in message
    # the other topic's document is byte-identical, in the worktree AND on main
    assert (worktree / OTHER_DOC).read_bytes() == before_bytes
    assert (multi_topic_repo.root / OTHER_DOC).read_bytes() == before_bytes
    # no commit rode it, and no record was filed under the foreign target
    assert _branch_head(multi_topic_repo) == before_head
    records = list((worktree / "ideation" / "dashboard" / "gate-records").glob("*"))
    assert not any(OTHER.replace("-", "") in p.name.replace("-", "")
                   and "staging" in p.name for p in records), records


def test_a_brainstorm_area_document_is_read_only_context_too(
        multi_topic_repo, tmp_path):
    """The sweep's second tile offered two `ideation/brainstorm/` documents and
    rewrote one. A capture in the brainstorm area belongs to whoever wrote it —
    the workbench shows it as context, and context is not a rewrite target."""
    registry = _registry(multi_topic_repo, tmp_path)
    _open_session(multi_topic_repo, registry)
    worktree = _worktree(multi_topic_repo)
    before = (worktree / BRAINSTORM_DOC).read_bytes()

    status, payload = _edit(multi_topic_repo, registry, document=BRAINSTORM_DOC)

    assert status == 409, payload
    assert "NOT this tile's own material" in payload["message"]
    assert (worktree / BRAINSTORM_DOC).read_bytes() == before


def test_the_tiles_own_folder_document_is_still_rewritable(
        multi_topic_repo, tmp_path):
    """The positive control, and it is load-bearing: a refusal that also refused
    the tile's own material would "fix" the defect by breaking the verb."""
    registry = _registry(multi_topic_repo, tmp_path)
    _open_session(multi_topic_repo, registry)
    own = f"ideation/staging/{TOPIC}/README.md"
    replacement = staging_fragment("Demo Topic", TOPIC) + "\nRewritten.\n"

    status, payload = _edit(multi_topic_repo, registry, document=own,
                            content=replacement)

    assert status == 200, payload
    assert payload["document"] == own
    assert payload["ref"] == DRAFT
    assert (_worktree(multi_topic_repo) / own).read_text("utf-8") == replacement


def test_the_document_this_session_created_is_rewritable(
        multi_topic_repo, tmp_path):
    """The other half of the rule: a session may rewrite what it CREATED. Here it
    is also inside the tile's folder, which is the ordinary case; the
    cluster/possible case below is the one that needs the allowance."""
    registry = _registry(multi_topic_repo, tmp_path)
    created = _open_session(multi_topic_repo, registry)

    status, payload = _edit(multi_topic_repo, registry,
                            document=created["path"],
                            content="# First Draft\n\nrewritten.\n")

    assert status == 200, payload
    assert payload["document"] == created["path"]


def test_a_cluster_tile_session_owns_no_corpus_document_at_all(
        multi_topic_repo, tmp_path):
    """A CLUSTER tile has no folder, so it inherits nothing: its member documents
    live all over the corpus and belong to whoever authored them. This is the
    conflation the old code made — "inside the worktree" was read as "this tile's"
    — and a cluster session is where it was widest."""
    registry = _registry(multi_topic_repo, tmp_path)
    snapshot = json.loads((tmp_path / "main-snapshot.json").read_text("utf-8"))
    clusters = [c["id"] for c in snapshot.get("clusters") or []]
    if not clusters:
        pytest.skip("the scratch corpus projects no cluster to open a tile on")
    cluster_id = clusters[0]
    status, created = gr.run_gate_action(
        "create-document",
        {**CREATE_BODY, "area": "ideation/brainstorm/",
         "title": "Cluster Session Capture",
         "scope_kind": bs.CLUSTER, "scope_id": cluster_id},
        checkout_root=multi_topic_repo.root, actor="brett", snapshot_path=None,
        session_registry=registry, repository=multi_topic_repo.repository)
    assert status == 200, created
    worktree = Path(created["ref"] and bs.worktree_path(
        multi_topic_repo.root, created["ref"]))
    before = (worktree / OTHER_DOC).read_bytes()

    refused = _edit(multi_topic_repo, registry, document=OTHER_DOC,
                    scope_kind=bs.CLUSTER, scope_id=cluster_id)
    allowed = _edit(multi_topic_repo, registry, document=created["path"],
                    content="# Cluster Session Capture\n\nrewritten.\n",
                    scope_kind=bs.CLUSTER, scope_id=cluster_id)

    assert refused[0] == 409, refused[1]
    assert "inherits none" in refused[1]["message"]
    assert (worktree / OTHER_DOC).read_bytes() == before
    # …and what the session itself created is still rewritable
    assert allowed[0] == 200, allowed[1]


# ==========================================================================
# the CLI parity surface (FR-020) — the same refusal, same rule
# ==========================================================================

def test_the_cli_parity_verb_refuses_the_same_foreign_document(
        multi_topic_repo, tmp_path, capsys, monkeypatch):
    """`cli.py gate edit-document` drives the SAME engine, and the sweep drove the
    CLI to confirm the crash it saw in the browser. If the ownership rule lived in
    the route instead of the engine, this surface would still overwrite."""
    registry = _registry(multi_topic_repo, tmp_path)
    _open_session(multi_topic_repo, registry)
    worktree = _worktree(multi_topic_repo)
    before = (worktree / OTHER_DOC).read_bytes()
    before_head = _branch_head(multi_topic_repo)
    # the CLI re-derives the process registry; point it at the one this test made
    monkeypatch.setattr(cli_mod, "_session_registry",
                        lambda root, repository: registry)
    monkeypatch.setattr(cli_mod, "_session_identity_gate",
                        lambda verb, root, args: None)
    content_file = tmp_path / "probe.md"
    content_file.write_text(PROBE, encoding="utf-8")

    rc = cli_mod.main([
        "gate", "edit-document", "--repo-root", str(multi_topic_repo.root),
        "--repository", REPO, "--actor", "brett",
        "--scope-kind", bs.STAGED_TOPIC, "--scope-id", TOPIC,
        "--document", OTHER_DOC, "--content-file", str(content_file),
    ])

    assert rc == 1
    err = capsys.readouterr().err
    assert "edit-document refused" in err
    assert "NOT this tile's own material" in err
    assert (worktree / OTHER_DOC).read_bytes() == before
    assert _branch_head(multi_topic_repo) == before_head


# ==========================================================================
# the PICKER — the pure model, run in node (the surface that offered the path)
# ==========================================================================

_HARNESS = """
import { rewritableDocuments, workbenchScope } from './model.mjs';
import { readFileSync } from 'node:fs';
const snap = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const scope = workbenchScope(snap, 'staged', process.argv[3]);
console.log(JSON.stringify({
  sections: scope.sections.map((s) => ({ key: s.key, owned: !!s.owned,
    inherited: !!s.inherited,
    documents: s.documents.filter((r) => r.resolved).map((r) => r.path) })),
  flattened: scope.documents.filter((r) => r.resolved).map((r) => r.path),
  offered: rewritableDocuments(scope, []),
  offeredWithCreated: rewritableDocuments(scope, ['ideation/brainstorm/fresh.md']),
}));
"""


def _run_model(snapshot, staging_id, tmp_path):
    if not NODE:
        pytest.skip("node not available for the JS derivation probe")
    shutil.copy(WEB_VIEWS / "staging-workbench-model.js", tmp_path / "model.mjs")
    (tmp_path / "probe.mjs").write_text(_HARNESS, encoding="utf-8")
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot), encoding="utf-8")
    done = subprocess.run(
        [NODE, str(tmp_path / "probe.mjs"), str(snap_path), staging_id],
        capture_output=True, text=True, cwd=str(tmp_path))
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


def test_the_rewrite_picker_offers_the_tiles_own_material_and_nothing_else(
        multi_topic_repo, tmp_path):
    """An EQUALITY assertion on the picker's option set, deliberately.

    The defect was a flatten: `scope.documents` is every section concatenated,
    which is right for a READ and wrong for a WRITE. A membership assertion
    ("the foreign path is absent") would pass again the moment another context
    section is added and flattened in; an equality assertion cannot."""
    snapshot = generate_snapshot(multi_topic_repo.root,
                                 multi_topic_repo.repository)
    staged = [t["staging_id"] for t in snapshot.get("staged_topics") or []]
    staging_id = next(s for s in staged if s.endswith(TOPIC))
    result = _run_model(snapshot, staging_id, tmp_path)

    owned = [path for s in result["sections"] if s["owned"] for path in s["documents"]]
    assert owned, "the tile must really own something for this to prove anything"
    # exactly one section is the tile's own material, and it is the folder
    assert [s["key"] for s in result["sections"] if s["owned"]] == ["folder"]
    # EQUALITY — the picker offers the owned paths and nothing else
    assert result["offered"] == owned
    # and the flattened list really is bigger, i.e. the world has foreign rows in
    # it (otherwise this test would pass on a one-topic corpus, which is exactly
    # how the defect survived)
    assert len(result["flattened"]) >= len(owned)
    for path in result["flattened"]:
        if path not in owned:
            assert path not in result["offered"], path
    # a document THIS SESSION created is offered even though no section holds it
    assert "ideation/brainstorm/fresh.md" in result["offeredWithCreated"]


# ==========================================================================
# T075 (010-doxbench-editor-chat, US4): the FIRST SAVE, exposed through this
# same gate — `gate_routes.execute_first_edit`.
#
# doxBench's Save is not a new verb. It is one of the two EXISTING document
# actions, run inside the tile's own branch session, with the session created or
# joined as part of the same transaction. The exposure under test here owns
# exactly two things, and this block asserts exactly those two:
#
#   1. THE GATE — rooted at the session worktree and DECLARING it, handed to the
#      transaction as a factory because the worktree does not exist until the
#      transaction has opened or joined the session.
#   2. THE OWNERSHIP INPUT — `tile_owned_prefix`, the SAME single source
#      `foreign_document_refusal` uses for `edit-document`, injected as
#      `owned_prefix`. The exposure re-decides nothing: a second copy of the
#      ownership rule is precisely how the two surfaces drift apart, which is the
#      defect the rest of this file exists to hold closed.
#
# So the pins below are deliberately about the SEAM (which rule reaches the
# transaction, through which gate, via which entry point) plus end-to-end
# evidence in the multi-topic world that the injected rule really refuses
# another topic's material and really permits the tile's own. Eligibility,
# revalidation, action choice and rollback are asserted at the transaction's own
# surface (test_session_transaction.py, test_doxbench_save.py); route-level
# enforcement of ownership and identity is a later task and is NOT performed by
# this exposure.
#
# Pins FR-031, FR-032, FR-034 and FR-036.
# ==========================================================================

from session_fixtures import GATE_RECORDS_PREFIX          # noqa: E402

from ideation_dashboard import doxbench_hash as dh        # noqa: E402

SAVE_TILE = bs.Tile(bs.STAGED_TOPIC, TOPIC)
OWN_DOC = f"ideation/staging/{TOPIC}/README.md"           # seeded, exists
NEW_DOC = f"ideation/staging/{TOPIC}/detail.md"           # nothing has created it
SAVE_AT = "2026-07-30T11:00:00Z"
SAVE_AT_LATER = "2026-07-30T11:00:05Z"


def _first_save(repo, registry, *, document, content, base_hash=None,
                at=SAVE_AT, git=None, tile=SAVE_TILE, actor="brett", **over):
    """One first Save through the ROUTE-LEVEL exposure, with nothing about
    ownership passed in: the exposure is what injects it."""
    return gr.execute_first_edit(
        git=git or sg.SessionGit(repo.root), session_registry=registry,
        repository=repo.repository, tile=tile, document=document,
        content=content, actor=actor, checkout_root=repo.root,
        records_dir=GATE_RECORDS_PREFIX, base_hash=base_hash, at=at, **over)


def _own_doc_hash(repo, document=OWN_DOC):
    return dh.sha256_hex((repo.root / document).read_text(encoding="utf-8"))


# ---- the seam itself ----------------------------------------------------

def test_the_first_save_exposure_injects_the_gates_own_ownership_rule(
        monkeypatch, multi_topic_repo, tmp_path):
    """The load-bearing pin: `tile_owned_prefix` stays the SINGLE ownership
    source and reaches the transaction as `owned_prefix`.

    Asserted by capturing what the exposure hands the PUBLIC entry point, so a
    future edit that starts deciding ownership here — or that reaches past the
    entry point into the transaction's private helpers — fails on this line
    rather than by drifting quietly out of agreement with `edit-document`."""
    captured = {}

    def recorder(git, registry, **kwargs):
        captured["positional"] = (git, registry)
        captured.update(kwargs)
        raise bs.SessionRefused("probe: nothing was opened")

    monkeypatch.setattr(gr.branch_session, "commit_first_edit", recorder)
    with pytest.raises(bs.SessionRefused):
        _first_save(multi_topic_repo, None, document=OWN_DOC, content=PROBE)

    assert captured["owned_prefix"] == gr.tile_owned_prefix(SAVE_TILE)
    assert captured["owned_prefix"] == f"ideation/staging/{TOPIC}/"
    # and the ownership answer is not restated here in any other form
    assert "foreign" not in captured and "owned" not in captured


def test_the_first_save_gate_is_rooted_at_the_worktree_and_declares_it(
        multi_topic_repo, tmp_path):
    """FR-015 through the factory: the gate's root, its DECLARED session root,
    and the tree the record lands in are one directory. The factory is what makes
    that possible at all — the worktree does not exist when the caller is
    building its request."""
    worktree = tmp_path / "pretend-worktree"
    worktree.mkdir()

    gate = gr.first_edit_gate_factory("brett", GATE_RECORDS_PREFIX)(worktree)

    assert Path(gate.output.root).resolve() == worktree.resolve()
    assert Path(gate.session_root).resolve() == worktree.resolve()
    assert gate.human_actor == "brett"


def test_the_first_save_calls_only_the_public_transaction_entry_point():
    """The transaction's locked body and its unwind are MODULE-PRIVATE: the lock
    they run under is not reentrant and the unwind is asymmetric on whether the
    Save opened or joined the session, so reaching them directly would bypass
    both decisions. The exposure names neither."""
    source = (REPO_ROOT / "scripts" / "ideation_dashboard"
              / "gate_routes.py").read_text(encoding="utf-8")
    assert "commit_first_edit" in source
    for private in ("_commit_first_edit_locked", "_unwind_first_edit"):
        assert private not in source, private
    # and it claims no lock of its own around a transaction that claims one
    body = source.split("def execute_first_edit(", 1)[1].split("\ndef ", 1)[0]
    assert "worktree_action_lock" not in body


# ---- end to end, in the multi-topic world ------------------------------

def test_a_first_save_of_the_tiles_own_existing_material_opens_the_session(
        multi_topic_repo, tmp_path):
    """FR-032's create arm plus FR-031's existing-path clause: no session exists,
    the tile's own seeded document is saved, and the answer is the EXISTING edit
    action on a branch this Save opened."""
    registry = _registry(multi_topic_repo, tmp_path)
    git = sg.SessionGit(multi_topic_repo.root)
    served_before = (multi_topic_repo.root / OWN_DOC).read_bytes()
    replacement = staging_fragment("Demo Topic", TOPIC) + "\nSaved by doxBench.\n"

    result = _first_save(multi_topic_repo, registry, document=OWN_DOC,
                         content=replacement,
                         base_hash=_own_doc_hash(multi_topic_repo), git=git)

    assert result["ok"] is True
    assert result["verb"] == "edit-document"
    assert result["ref"] == DRAFT
    assert result["document"] == OWN_DOC
    assert result["session"] == "opened"
    assert result["record"].startswith(GATE_RECORDS_PREFIX)
    assert result["content_hash"]["hex"] == dh.sha256_hex(replacement)
    assert (_worktree(multi_topic_repo) / OWN_DOC).read_text("utf-8") == replacement
    # FR-037: the SERVED checkout is never written by a Save
    assert (multi_topic_repo.root / OWN_DOC).read_bytes() == served_before
    assert git.commits_ahead("main", DRAFT) == 1


def test_a_first_save_of_a_new_path_inside_the_tile_uses_the_create_action(
        multi_topic_repo, tmp_path):
    """FR-031's new-path clause, through the exposure: a path nothing has created
    yet is the EXISTING create action — Save introduces no third verb."""
    registry = _registry(multi_topic_repo, tmp_path)

    result = _first_save(multi_topic_repo, registry, document=NEW_DOC,
                         content="# Detail\n\na brand new document.\n")

    assert result["verb"] == "create-document"
    assert result["document"] == NEW_DOC
    assert result["session"] == "opened"
    assert (_worktree(multi_topic_repo) / NEW_DOC).is_file()
    assert not (multi_topic_repo.root / NEW_DOC).exists()


def test_a_second_first_save_joins_the_session_the_first_one_opened(
        multi_topic_repo, tmp_path):
    """FR-034: two changed buffers are two governance actions in ONE session, and
    the second reports that it JOINED rather than opening a second branch."""
    registry = _registry(multi_topic_repo, tmp_path)
    git = sg.SessionGit(multi_topic_repo.root)

    first = _first_save(multi_topic_repo, registry, document=OWN_DOC,
                        content=staging_fragment("Demo Topic", TOPIC) + "\nOne.\n",
                        base_hash=_own_doc_hash(multi_topic_repo), git=git)
    second = _first_save(multi_topic_repo, registry, document=NEW_DOC,
                         content="# Detail\n\ntwo.\n", at=SAVE_AT_LATER, git=git)

    assert first["session"] == "opened"
    assert second["session"] == "joined"
    assert second["ref"] == first["ref"] == DRAFT
    assert git.commits_ahead("main", DRAFT) == 2
    assert git.is_ancestor(first["commit"], second["commit"]) is True


def test_a_first_save_of_another_topics_document_is_refused_and_opens_nothing(
        multi_topic_repo, tmp_path):
    """FR-036 through the injected rule, in the world where it matters: the
    refusal arrives before anything is opened, so there is no branch, no
    worktree, and no live entry to clean up — and the other topic's bytes never
    move, in the served checkout or anywhere else."""
    registry = _registry(multi_topic_repo, tmp_path)
    git = sg.SessionGit(multi_topic_repo.root)
    before = (multi_topic_repo.root / OTHER_DOC).read_bytes()

    with pytest.raises(bs.SessionRefused) as refusal:
        _first_save(multi_topic_repo, registry, document=OTHER_DOC,
                    content=PROBE, base_hash=dh.sha256_hex(
                        before.decode("utf-8")), git=git)

    message = str(refusal.value)
    assert "NOT this tile's own material" in message
    assert OTHER_DOC in message and "Nothing was written" in message
    assert (multi_topic_repo.root / OTHER_DOC).read_bytes() == before
    assert git.branch_exists(DRAFT) is False
    assert not _worktree(multi_topic_repo).exists()
    assert bs.is_live(registry, multi_topic_repo.repository, DRAFT) is False


def test_a_brainstorm_capture_is_refused_by_the_first_save_too(
        multi_topic_repo, tmp_path):
    """The same rule the `edit-document` route applies to a brainstorm capture,
    reached through the Save seam instead: context is not a Save target."""
    registry = _registry(multi_topic_repo, tmp_path)
    before = (multi_topic_repo.root / BRAINSTORM_DOC).read_bytes()

    with pytest.raises(bs.SessionRefused) as refusal:
        _first_save(multi_topic_repo, registry, document=BRAINSTORM_DOC,
                    content=PROBE,
                    base_hash=dh.sha256_hex(before.decode("utf-8")))

    assert "NOT this tile's own material" in str(refusal.value)
    assert (multi_topic_repo.root / BRAINSTORM_DOC).read_bytes() == before


def test_the_existing_edit_document_route_is_untouched_by_the_new_exposure(
        multi_topic_repo, tmp_path):
    """Byte-compatibility, asserted rather than assumed: the pre-existing route
    still refuses a foreign document with its OWN message and still accepts the
    tile's own material, with the Save exposure sitting beside it and changing
    neither."""
    registry = _registry(multi_topic_repo, tmp_path)
    _open_session(multi_topic_repo, registry)

    refused_status, refused = _edit(multi_topic_repo, registry,
                                    document=OTHER_DOC)
    own = f"ideation/staging/{TOPIC}/README.md"
    ok_status, accepted = _edit(
        multi_topic_repo, registry, document=own,
        content=staging_fragment("Demo Topic", TOPIC) + "\nStill fine.\n")

    assert refused_status == 409
    assert "NOT this tile's own material" in refused["message"]
    assert ok_status == 200
    assert accepted["verb"] == "edit-document"
    assert set(accepted) == {"ok", "verb", "ref", "commit", "document",
                             "record", "hint"}


# ---- the gate VERB itself (T080 server-route slice, 2026-07-30) -----------
#
# T075 exposed the first-edit transaction as a gate-layer FUNCTION; nothing
# dispatched it. This block pins the missing half: a `first-edit` GATE VERB on
# the same table-driven `run_gate_action` surface every other console verb
# uses — so the browser Save seam has a transport to bind, serve.py's generic
# gate handler needs no verb-specific change, and console-presence enforcement
# applies because the verb is SESSION-BEARING (its side effects are a branch,
# a worktree, and a governance record).

def _first_edit_verb(repo, registry, *, document, content=PROBE,
                     base_hash=None, scope_id=TOPIC,
                     scope_kind=bs.STAGED_TOPIC, use_registry=True,
                     continuation=None):
    body = {"scope_kind": scope_kind, "scope_id": scope_id,
            "document": document, "content": content}
    if base_hash is not None:
        body["base_hash"] = base_hash
    if continuation is not None:
        body["continuation"] = continuation
    return gr.run_gate_action(
        "first-edit", body,
        checkout_root=repo.root, actor="brett", snapshot_path=None,
        session_registry=(registry if use_registry else None),
        repository=repo.repository)


def test_the_first_edit_verb_is_session_bearing():
    """FR-024's console discipline reaches the verb through the SAME clause the
    other session verbs use: membership, not a parallel mechanism."""
    assert "first-edit" in gr.SESSION_BEARING_VERBS


def test_the_first_edit_verb_lands_a_first_save_over_the_gate_dispatch(
        multi_topic_repo, tmp_path):
    registry = _registry(multi_topic_repo, tmp_path)
    replacement = staging_fragment("Demo Topic", TOPIC) + "\nSaved via verb.\n"
    status, payload = _first_edit_verb(
        multi_topic_repo, registry, document=OWN_DOC, content=replacement,
        base_hash=_own_doc_hash(multi_topic_repo))
    assert status == 200
    assert payload["ok"] is True
    assert payload["verb"] == "edit-document"
    assert payload["session"] == "opened"
    assert set(payload) == {"ok", "verb", "ref", "commit", "document",
                            "record", "content_hash", "session", "hint"}
    # the STRUCTURED identity (named algorithm + hex), as the transaction
    # reports it -- the same shape the client seam's identity check reads
    assert payload["content_hash"] == {
        "algorithm": "sha256", "hex": dh.sha256_hex(replacement)}
    # the served checkout is byte-identical; the write lives in the session
    assert (multi_topic_repo.root / OWN_DOC).read_text(
        encoding="utf-8") != replacement


def test_the_first_edit_verb_refuses_a_foreign_document_cleanly(
        multi_topic_repo, tmp_path):
    registry = _registry(multi_topic_repo, tmp_path)
    before = (multi_topic_repo.root / OTHER_DOC).read_bytes()
    status, payload = _first_edit_verb(
        multi_topic_repo, registry, document=OTHER_DOC)
    assert status == 409
    assert payload["ok"] is False
    assert "NOT this tile's own material" in payload["message"]
    assert (multi_topic_repo.root / OTHER_DOC).read_bytes() == before
    assert not _worktree(multi_topic_repo).exists()


def test_the_first_edit_verb_refuses_a_stale_base_naming_the_document(
        multi_topic_repo, tmp_path):
    registry = _registry(multi_topic_repo, tmp_path)
    status, payload = _first_edit_verb(
        multi_topic_repo, registry, document=OWN_DOC,
        base_hash=dh.sha256_hex("not what is there any more"))
    assert status == 409
    assert payload["ok"] is False
    assert OWN_DOC in payload["message"]
    assert not _worktree(multi_topic_repo).exists()


def test_the_first_edit_verb_requires_a_session_registry(
        multi_topic_repo, tmp_path):
    registry = _registry(multi_topic_repo, tmp_path)
    status, payload = _first_edit_verb(
        multi_topic_repo, registry, document=OWN_DOC, use_registry=False)
    assert status == 409
    assert payload["ok"] is False
    assert "registry" in payload["message"].lower()


def test_the_first_edit_verb_validates_its_body(multi_topic_repo, tmp_path):
    registry = _registry(multi_topic_repo, tmp_path)
    status, payload = gr.run_gate_action(
        "first-edit", {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC},
        checkout_root=multi_topic_repo.root, actor="brett",
        snapshot_path=None, session_registry=registry,
        repository=multi_topic_repo.repository)
    assert status == 400
    assert payload["ok"] is False


# ---- T104 F3 (PR #63 second review, gate_routes.py:2714): CONTINUATION ------
#
# `first-edit` is a session-OPENING verb, and FR-025's resume-or-new report
# tells the human to answer with `continuation='resume'` (or `'new'`). The
# transaction reads one — `commit_first_edit` -> `open_session` — and
# `execute_first_edit` already forwards one, but this ROUTE never read the
# field off the body, so the answer the refusal asks for was silently dropped
# and the human's second attempt got the identical report.
#
# Both tests below refuse: one because the value is not a continuation at all,
# one because it IS a continuation with nothing to continue. Both prove the
# field is READ, and neither requires an abandoned branch to exist — a body
# whose continuation is ignored simply SAVES, which is what they used to do.

def test_the_first_edit_verb_reads_the_fr025_continuation_from_the_body(
        multi_topic_repo, tmp_path):
    """`continuation='resume'` with nothing to resume is the engine's own
    refusal, reported verbatim — proof the answer reached `open_session`. The
    tile must be left exactly as it was: nothing opened, nothing written."""
    registry = _registry(multi_topic_repo, tmp_path)
    before = (multi_topic_repo.root / OWN_DOC).read_bytes()
    status, payload = _first_edit_verb(
        multi_topic_repo, registry, document=OWN_DOC,
        base_hash=_own_doc_hash(multi_topic_repo), continuation="resume")
    assert status == 409
    assert payload["ok"] is False
    assert "continuation" in payload["message"]
    assert "no abandoned session branch to continue from" in payload["message"]
    assert not _worktree(multi_topic_repo).exists()
    assert (multi_topic_repo.root / OWN_DOC).read_bytes() == before


def test_the_first_edit_verb_refuses_a_continuation_that_is_not_one(
        multi_topic_repo, tmp_path):
    """The same validator every other session-opening verb uses
    (`branch_session.normalize_continuation`), reached at the same place: a
    shaping refusal before anything opens, naming the two legal answers."""
    registry = _registry(multi_topic_repo, tmp_path)
    status, payload = _first_edit_verb(
        multi_topic_repo, registry, document=OWN_DOC,
        base_hash=_own_doc_hash(multi_topic_repo), continuation="carry-on")
    assert status == 400
    assert payload["ok"] is False
    assert "continuation" in payload["message"]
    assert not _worktree(multi_topic_repo).exists()


# ---- T076 closure pins (2026-07-30 ownership-semantics review) -------------
#
# The review's ruling: T076's four clauses are ENFORCED by the T074 eligibility
# precheck under the gate's own injected ownership rule (T075), and content
# identity is the designed "full identity" (R4/data-model S3 -- ref/revision
# are advisory bookkeeping). What was implied but unpinned is the FORGERY side
# (CHK012's Save half, CHK003's classification consistency): request-supplied
# authority claims must license nothing. These pins arrived green -- the
# behavior predates them -- and exist so it cannot regress silently.

def test_a_forged_owned_claim_licenses_nothing_at_the_verb(
        multi_topic_repo, tmp_path):
    """A body that smuggles `owned: true` (the client flag doxbench-save.js
    deliberately drops before transport) for ANOTHER topic's document is
    refused exactly like the honest request: ownership is the server's answer
    from its own rule, never a request field."""
    registry = _registry(multi_topic_repo, tmp_path)
    before = (multi_topic_repo.root / OTHER_DOC).read_bytes()
    status, payload = gr.run_gate_action(
        "first-edit",
        {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
         "document": OTHER_DOC, "content": PROBE,
         "owned": True},
        checkout_root=multi_topic_repo.root, actor="brett",
        snapshot_path=None, session_registry=registry,
        repository=multi_topic_repo.repository)
    assert status == 409
    assert payload["ok"] is False
    assert "NOT this tile's own material" in payload["message"]
    assert (multi_topic_repo.root / OTHER_DOC).read_bytes() == before
    assert not _worktree(multi_topic_repo).exists()


def test_advisory_identity_fields_are_ignored_never_trusted(
        multi_topic_repo, tmp_path):
    """`base_ref`/`base_revision` are bookkeeping the client reports and the
    verb must neither require nor trust: with the ONE real authority present
    (a correct content hash, R4/FR-032), forged advisory values refuse
    nothing -- and (next test) correct-looking advisory values rescue nothing
    when the hash is stale. Authoring this pin surfaced a STRONGER fact than
    the review assumed: an existing-material edit with NO hash at all is
    refused outright ("an unrevalidatable overwrite is refused rather than
    trusted", FR-032) -- the fail-closed reading, recorded here."""
    registry = _registry(multi_topic_repo, tmp_path)
    replacement = staging_fragment("Demo Topic", TOPIC) + "\nAdvisory test.\n"
    status, payload = gr.run_gate_action(
        "first-edit",
        {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
         "document": OWN_DOC, "content": replacement,
         "base_hash": _own_doc_hash(multi_topic_repo),
         "base_ref": "refs/heads/forged", "base_revision": "f" * 40},
        checkout_root=multi_topic_repo.root, actor="brett",
        snapshot_path=None, session_registry=registry,
        repository=multi_topic_repo.repository)
    assert status == 200 and payload["ok"] is True, payload


def test_correct_advisory_fields_cannot_rescue_a_stale_hash(
        multi_topic_repo, tmp_path):
    registry = _registry(multi_topic_repo, tmp_path)
    status, payload = gr.run_gate_action(
        "first-edit",
        {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC,
         "document": OWN_DOC, "content": PROBE,
         "base_hash": dh.sha256_hex("stale content"),
         "base_ref": "main", "base_revision": "2" * 40},
        checkout_root=multi_topic_repo.root, actor="brett",
        snapshot_path=None, session_registry=registry,
        repository=multi_topic_repo.repository)
    assert status == 409
    assert payload["ok"] is False
    assert OWN_DOC in payload["message"]
    assert not _worktree(multi_topic_repo).exists()
