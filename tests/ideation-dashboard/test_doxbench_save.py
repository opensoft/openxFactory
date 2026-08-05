"""T067 (010-doxbench-editor-chat, US4): eligibility and stale-base refusals for
the governed ordered Save.

Save owns no authority of its own. It persists changed backed buffers through
the EXISTING create-document and edit-document actions, inside the tile's own
branch session, and every question it has to answer first is a refusal
question:

  * is this buffer's target the opened tile's OWN material, or is it inherited,
    cited, cluster-neighbourhood, inbound, or otherwise read-only context
    (FR-036)?
  * is the target a NEW path (the existing create action) or an EXISTING one
    (the existing edit action) (FR-031)?
  * is the base the human edited from still the base on disk, or has the
    source moved underneath them (FR-032's revalidation clause)?

Those three answers are prechecks of the first-edit TRANSACTION — T074's
`branch_session.commit_first_edit` and the two pure helpers it composes,
`first_edit_eligibility` and `first_edit_base_refusal`. They are asserted here,
at the transaction's own surface, and deliberately NOT at the route: route-level
enforcement of ownership, full identity, and action choice is T076's surface and
is out of this wave's scope.

Every test in this module is RED until T074 lands. The eligibility helper is
pure and hermetic (it reads a scratch directory tree and nothing else); the
transaction tests build a throwaway served checkout with a local bare origin and
never touch a network, a real corpus, or a real notebook.

Pins FR-031, FR-032 (revalidation), FR-036, and SC-005.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from session_fixtures import GATE_RECORDS_PREFIX
from ideation_dashboard import branch_session as bs
from ideation_dashboard import doxbench_hash as dh
from ideation_dashboard import gate_console as gc
from ideation_dashboard import session_git as sg
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.boundary import HumanGate
from ideation_dashboard.generator import generate_snapshot

TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
OWNED_PREFIX = f"ideation/staging/{TOPIC}/"
OUTLINE = f"{OWNED_PREFIX}README.md"           # seeded; exists in the served checkout
NEW_DOC = f"{OWNED_PREFIX}detail.md"           # a path nothing has created yet
INHERITED = "ideation/staging/other-topic/README.md"
BRAINSTORM = "ideation/brainstorm/a-loose-thought.md"
ALLOWLIST = (GATE_RECORDS_PREFIX, "ideation/staging/")
AT = "2026-07-30T09:00:00Z"
AT_LATER = "2026-07-30T09:00:05Z"

TILE = bs.Tile(bs.STAGED_TOPIC, TOPIC)


# --------------------------------------------------------------------------
# the world
# --------------------------------------------------------------------------

def _registry(repo, tmp_path):
    path = tmp_path / "main-snapshot.json"
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _gate_factory(actor="brett"):
    def build(worktree):
        return HumanGate(worktree, list(ALLOWLIST), human_actor=actor,
                         session_root=worktree)
    return build


def _first_save(repo, registry, *, document, content, base_hash=None, at=AT,
                owned_prefix=OWNED_PREFIX, git=None, **over):
    """One eligible first Save through T074's transaction entry point."""
    return bs.commit_first_edit(
        git or sg.SessionGit(repo.root), registry,
        repository=repo.repository, tile=TILE,
        document=document, content=content,
        gate_factory=_gate_factory(),
        checkout_root=repo.root, owned_prefix=owned_prefix,
        base_hash=base_hash, at=at, records_dir=GATE_RECORDS_PREFIX, **over)


def _with_another_topic(repo):
    """Another topic's committed material, in the SERVED checkout: the canonical
    inherited/context-only row the workbench shows read-only."""
    repo.write(INHERITED, "# Other Topic\n\nsomebody else's material.\n")
    repo.commit("Add another topic's material", INHERITED)
    return INHERITED


def _with_a_brainstorm_capture(repo):
    repo.write(BRAINSTORM, "# A Loose Thought\n\ncaptured elsewhere.\n")
    repo.commit("Capture a loose thought", BRAINSTORM)
    return BRAINSTORM


# ==========================================================================
# FR-036 / FR-031 — eligibility, as a PURE answer about a path
#
# `first_edit_eligibility` is the precheck the transaction runs before it opens
# anything, and it is pure so the refusal can be asserted without a session
# existing at all. It answers two things at once — MAY this be saved, and as
# WHICH existing action — because they are the same question about the same
# path and answering them in two places is how they drift apart.
# ==========================================================================

def test_the_tiles_own_existing_material_is_eligible_as_the_edit_action(
        scratch_repo):
    """FR-031's existing-path clause: a document inside the staged-topic tile's
    own folder that already exists is saved through the EXISTING edit action."""
    verdict = bs.first_edit_eligibility(
        document=OUTLINE, checkout_root=scratch_repo.root,
        owned_prefix=OWNED_PREFIX, tile=TILE)

    assert verdict.eligible is True
    assert verdict.action == gc.ACTION_EDIT_DOCUMENT
    assert verdict.document == OUTLINE
    assert verdict.reason is None


def test_a_new_path_inside_the_tiles_own_material_is_eligible_as_the_create_action(
        scratch_repo):
    """FR-031's new-path clause: the same folder, a path nothing has created
    yet, and the answer is the EXISTING create action — not a new verb."""
    verdict = bs.first_edit_eligibility(
        document=NEW_DOC, checkout_root=scratch_repo.root,
        owned_prefix=OWNED_PREFIX, tile=TILE)

    assert verdict.eligible is True
    assert verdict.action == gc.ACTION_CREATE_DOCUMENT
    assert verdict.document == NEW_DOC
    assert verdict.reason is None


def test_another_topics_existing_document_is_ineligible_and_says_why(
        scratch_repo):
    """FR-036's inherited clause. This is the one that matters most: worktree
    containment is not tile ownership, and the difference is committing another
    topic's document under a gate-action record that names THIS session."""
    inherited = _with_another_topic(scratch_repo)

    verdict = bs.first_edit_eligibility(
        document=inherited, checkout_root=scratch_repo.root,
        owned_prefix=OWNED_PREFIX, tile=TILE)

    assert verdict.eligible is False
    assert verdict.action is None
    assert verdict.reason and "other-topic" in verdict.reason
    assert "own material" in verdict.reason.lower()


def test_a_brainstorm_capture_outside_the_tile_is_ineligible(scratch_repo):
    """FR-036's other-context clause, spelled with a second real shape so the
    refusal is not accidentally specific to sibling staging folders."""
    capture = _with_a_brainstorm_capture(scratch_repo)

    verdict = bs.first_edit_eligibility(
        document=capture, checkout_root=scratch_repo.root,
        owned_prefix=OWNED_PREFIX, tile=TILE)

    assert verdict.eligible is False
    assert verdict.reason and "brainstorm" in verdict.reason


def test_a_tile_owning_no_folder_inherits_nothing(scratch_repo):
    """A cluster or possible tile owns no folder of its own, so it inherits
    NOTHING: every already-existing document is read-only context to it. The
    fail-closed reading is asserted through `owned_prefix=None`, which is what
    such a tile resolves to."""
    verdict = bs.first_edit_eligibility(
        document=OUTLINE, checkout_root=scratch_repo.root,
        owned_prefix=None, tile=bs.Tile(bs.CLUSTER, "some-cluster"))

    assert verdict.eligible is False
    assert verdict.reason and "no folder of its own" in verdict.reason


def test_a_tile_owning_no_folder_may_still_create_a_new_path(scratch_repo):
    """The other half of the same rule: inheriting nothing is not the same as
    being unable to author. A path that exists nowhere is still a create."""
    verdict = bs.first_edit_eligibility(
        document=NEW_DOC, checkout_root=scratch_repo.root,
        owned_prefix=None, tile=bs.Tile(bs.CLUSTER, "some-cluster"))

    assert verdict.eligible is True
    assert verdict.action == gc.ACTION_CREATE_DOCUMENT


def test_a_document_this_session_created_is_eligible_as_the_edit_action(
        scratch_repo, tmp_path):
    """FR-043's consequence for Save, at the eligibility layer: a path present
    in the session worktree and ABSENT from the served checkout was introduced
    on this branch, so it is the session's own material and its SECOND Save is
    an edit. (Chat eligibility for such a document is FR-043/T107 and is not
    re-tested here.)"""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    outside = "ideation/brainstorm/session-authored.md"
    opened = bs.open_session(git, registry, repository=scratch_repo.repository,
                             tile=TILE, checkout_root=scratch_repo.root)
    target = Path(opened.worktree) / outside
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# Session Authored\n", encoding="utf-8")

    verdict = bs.first_edit_eligibility(
        document=outside, checkout_root=scratch_repo.root,
        worktree=opened.worktree, owned_prefix=OWNED_PREFIX, tile=TILE)

    assert verdict.eligible is True
    assert verdict.action == gc.ACTION_EDIT_DOCUMENT
    assert verdict.session_created is True


def test_a_path_escaping_the_checkout_is_ineligible_rather_than_clamped(
        scratch_repo):
    """A path that escapes is a refusal, never a fallback (data-model validation
    rules). Asserted with a traversal spelling, because that is the one a
    client-supplied buffer path could actually carry."""
    verdict = bs.first_edit_eligibility(
        document="../outside-the-checkout.md", checkout_root=scratch_repo.root,
        owned_prefix=OWNED_PREFIX, tile=TILE)

    assert verdict.eligible is False
    assert verdict.reason and "outside" in verdict.reason.lower()


@pytest.mark.parametrize("document", ["", "   ", None])
def test_a_blank_target_is_ineligible(scratch_repo, document):
    """A buffer with no path has never been created, and the absence is a
    structural refusal rather than a guessed filename."""
    verdict = bs.first_edit_eligibility(
        document=document, checkout_root=scratch_repo.root,
        owned_prefix=OWNED_PREFIX, tile=TILE)

    assert verdict.eligible is False


# ==========================================================================
# FR-032's revalidation clause — the STALE BASE
#
# The buffer carries the identity of the base it was loaded from. If the file
# on disk no longer hashes to it, the human is about to overwrite somebody
# else's newer text with a diff computed against text that is gone. That is a
# refusal, and it is checked immediately before the mutation rather than at
# request-parse time, because the window that matters is the one inside the
# transaction's lock.
# ==========================================================================

def test_a_matching_base_hash_is_no_refusal(scratch_repo):
    served = (scratch_repo.root / OUTLINE).read_text(encoding="utf-8")

    refusal = bs.first_edit_base_refusal(
        document=OUTLINE, root=scratch_repo.root,
        action=gc.ACTION_EDIT_DOCUMENT, base_hash=dh.sha256_hex(served))

    assert refusal is None


def test_a_base_hash_that_no_longer_matches_the_file_is_refused(scratch_repo):
    """The stale-base refusal proper: the buffer's base identity is asserted
    against the bytes that would actually be replaced."""
    stale = dh.sha256_hex("# Demo Topic\n\nwhat the human loaded.\n")

    refusal = bs.first_edit_base_refusal(
        document=OUTLINE, root=scratch_repo.root,
        action=gc.ACTION_EDIT_DOCUMENT, base_hash=stale)

    assert refusal is not None
    assert stale in refusal, "the refusal names the base the human edited from"
    assert OUTLINE in refusal


def test_a_crlf_document_edited_from_its_served_bytes_is_no_refusal(scratch_repo):
    """T104 F10: the base revalidation reads through the SAME lens the client
    hashed. `/source` serves verbatim bytes and the browser's `Response.text()`
    keeps CR and CRLF, while `Path.read_text`'s universal-newline translation
    collapses them -- so a CRLF document's base was recomputed over text the
    client never saw and every honest Save of it was refused as stale,
    forever. The buffer's declared base below is exactly what the client
    computes: the hash of the served bytes, CRLF intact."""
    crlf = "# Demo Topic\r\n\r\nauthored on Windows.\r\n"
    (scratch_repo.root / OUTLINE).write_bytes(crlf.encode("utf-8"))

    refusal = bs.first_edit_base_refusal(
        document=OUTLINE, root=scratch_repo.root,
        action=gc.ACTION_EDIT_DOCUMENT, base_hash=dh.sha256_hex(crlf))

    assert refusal is None


def test_an_edit_of_a_vanished_file_is_refused_rather_than_recreated(
        scratch_repo):
    """A document that has been removed underneath the buffer is not silently
    recreated by an edit: the action choice was made against a file that no
    longer exists, and re-deriving it here would hide the deletion."""
    (scratch_repo.root / OUTLINE).unlink()

    refusal = bs.first_edit_base_refusal(
        document=OUTLINE, root=scratch_repo.root,
        action=gc.ACTION_EDIT_DOCUMENT, base_hash=dh.sha256_hex("# anything\n"))

    assert refusal is not None
    assert "no longer" in refusal or "does not exist" in refusal


def test_a_create_whose_path_appeared_underneath_it_is_refused(scratch_repo):
    """The create arm's stale base. A create action's base is the ABSENCE of the
    path; if something has since created it, saving would overwrite it while
    reporting a create."""
    scratch_repo.write(NEW_DOC, "# Detail\n\nsomebody got there first.\n")

    refusal = bs.first_edit_base_refusal(
        document=NEW_DOC, root=scratch_repo.root,
        action=gc.ACTION_CREATE_DOCUMENT, base_hash=None)

    assert refusal is not None
    assert NEW_DOC in refusal


def test_an_edit_declaring_no_base_identity_is_refused(scratch_repo):
    """An edit with no declared base cannot be revalidated at all, and an
    unrevalidatable overwrite is refused rather than trusted."""
    refusal = bs.first_edit_base_refusal(
        document=OUTLINE, root=scratch_repo.root,
        action=gc.ACTION_EDIT_DOCUMENT, base_hash=None)

    assert refusal is not None


# ==========================================================================
# The same two answers, through the TRANSACTION — because a precheck that the
# transaction does not actually consult is decoration.
# ==========================================================================

def test_the_transaction_refuses_inherited_material_without_opening_anything(
        scratch_repo, tmp_path):
    """FR-036 through FR-033: the ineligible target is refused in the PRECHECK
    state, so there is no branch, no worktree, and no live registry entry to
    clean up afterwards."""
    registry = _registry(scratch_repo, tmp_path)
    inherited = _with_another_topic(scratch_repo)
    git = sg.SessionGit(scratch_repo.root)
    served = (scratch_repo.root / inherited).read_text(encoding="utf-8")

    with pytest.raises(bs.SessionRefused) as exc:
        _first_save(scratch_repo, registry, document=inherited,
                    content="# Other Topic\n\nrewritten from doxBench.\n",
                    base_hash=dh.sha256_hex(served), git=git)

    assert "other-topic" in str(exc.value)
    assert git.branch_exists(DRAFT) is False
    assert not bs.worktree_path(scratch_repo.root, DRAFT).exists()
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is False


def test_the_transaction_revalidates_the_base_inside_its_own_lock(
        scratch_repo, tmp_path):
    """FR-032's "revalidate the source" clause. The base is asserted against the
    bytes in the SESSION WORKTREE — the tree the replacement would land in — and
    a session opened for a Save that then refuses leaves nothing behind."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)

    with pytest.raises(bs.SessionRefused) as exc:
        _first_save(scratch_repo, registry, document=OUTLINE,
                    content="# Demo Topic\n\nrewritten.\n",
                    base_hash=dh.sha256_hex("# not what is on disk\n"), git=git)

    assert OUTLINE in str(exc.value)
    assert git.branch_exists(DRAFT) is False, (
        "a first Save that refused on revalidation unwinds the session it opened")
    assert not bs.worktree_path(scratch_repo.root, DRAFT).exists()
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is False


def test_an_eligible_first_save_of_an_existing_path_uses_the_edit_action(
        scratch_repo, tmp_path):
    """FR-031 + FR-032 end to end for the existing-path arm."""
    registry = _registry(scratch_repo, tmp_path)
    served = (scratch_repo.root / OUTLINE).read_text(encoding="utf-8")

    outcome = _first_save(scratch_repo, registry, document=OUTLINE,
                          content="# Demo Topic\n\nsaved by doxBench.\n",
                          base_hash=dh.sha256_hex(served))

    assert outcome.action == gc.ACTION_EDIT_DOCUMENT
    assert outcome.document == OUTLINE
    assert outcome.ref == DRAFT
    assert outcome.joined is False, "the first Save OPENED this session"
    assert outcome.content_hash == dh.content_identity(
        "# Demo Topic\n\nsaved by doxBench.\n").as_dict()


def test_an_eligible_first_save_of_a_new_path_uses_the_create_action(
        scratch_repo, tmp_path):
    """FR-031's new-path arm end to end, including the identity the buffer
    rebases onto."""
    registry = _registry(scratch_repo, tmp_path)

    outcome = _first_save(scratch_repo, registry, document=NEW_DOC,
                          content="# Detail\n\nbrand new.\n")

    assert outcome.action == gc.ACTION_CREATE_DOCUMENT
    assert outcome.document == NEW_DOC
    assert outcome.joined is False
    assert outcome.content_hash == dh.content_identity(
        "# Detail\n\nbrand new.\n").as_dict()
    assert (Path(outcome.session.worktree) / NEW_DOC).read_text(
        encoding="utf-8") == "# Detail\n\nbrand new.\n"


def test_a_second_save_joins_the_session_the_first_one_opened(
        scratch_repo, tmp_path):
    """FR-032's "create OR JOIN" clause: the tile has exactly one session, and
    the second Save joins it rather than allocating a second ordinal."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)

    first = _first_save(scratch_repo, registry, document=NEW_DOC,
                        content="# Detail\n\nfirst.\n", at=AT, git=git)
    second = _first_save(scratch_repo, registry, document=NEW_DOC,
                         content="# Detail\n\nsecond.\n", at=AT_LATER, git=git,
                         base_hash=dh.sha256_hex("# Detail\n\nfirst.\n"))

    assert first.joined is False and second.joined is True
    assert second.ref == first.ref == DRAFT
    assert second.action == gc.ACTION_EDIT_DOCUMENT, (
        "the path exists on the branch now, so its next Save is an edit")
    assert git.commits_ahead("main", DRAFT) == 2


def test_a_stale_second_save_leaves_the_first_saves_commit_standing(
        scratch_repo, tmp_path):
    """FR-035's "MUST NOT rewrite successful history", at the transaction layer:
    a refused Save into a JOINED session unwinds ITS OWN work and nothing
    else — the earlier commit, its record, and the live session all survive."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    first = _first_save(scratch_repo, registry, document=NEW_DOC,
                        content="# Detail\n\nfirst.\n", at=AT, git=git)
    worktree = Path(first.session.worktree)
    committed = (worktree / NEW_DOC).read_bytes()

    with pytest.raises(bs.SessionRefused):
        _first_save(scratch_repo, registry, document=NEW_DOC,
                    content="# Detail\n\nsecond.\n", at=AT_LATER, git=git,
                    base_hash=dh.sha256_hex("# a base that is not on disk\n"))

    assert git.commits_ahead("main", DRAFT) == 1
    assert git.head(worktree) == first.commit.sha
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is True
    assert (worktree / NEW_DOC).read_bytes() == committed, (
        "a refused Save into a joined session restores the bytes it replaced")
    assert git.staged_paths(worktree) == ()


# ==========================================================================
# T071 (US4) — the ORDERED two-buffer Save: outline first, one existing
# governance action per changed document, honest partial success, and
# compatible revision ancestry.
#
# The ordering is not cosmetic. The Outline is the document that names the
# packet; a Document saved against an Outline that has not landed yet would
# carry an ancestry the Outline's own commit then contradicts. So the sequence
# invariant (data-model 11) is: skip clean buffers, save Outline, refresh and
# advance ONLY the Outline's base, then save Document against its exact file
# base and the resulting session ancestry — and if the Document refuses, keep it
# dirty and PRESERVE the Outline's commit (FR-035's "MUST NOT rewrite
# successful history").
#
# The orchestration itself is client-side and pure (`doxbench-save.js`, T077),
# so it is driven here through a Node harness with an INJECTED transport that
# records every call and can refuse a chosen buffer. The ancestry claim is a
# server fact and is measured on the branch.
#
# Pins FR-031, FR-034, FR-035 and SC-005. RED until T077 (client) / T074
# (server) land.
# ==========================================================================

import shutil  # noqa: E402
import subprocess  # noqa: E402

NODE = shutil.which("node")
SAVE_JS = (Path(__file__).resolve().parent.parent.parent / "scripts"
           / "ideation_dashboard" / "web" / "views" / "doxbench-save.js")
STATE_JS = SAVE_JS.parent / "doxbench-state.js"

# The harness builds a doxBench state with both buffers dirty, hands `runSave`
# an injected transport whose verdicts are scripted per buffer, and reports the
# call log plus the outcome and the resulting state. One process backs the whole
# T071 set: the scenarios are independent, so they are all run and returned
# together (the same economy `mutation_results` uses).
_SAVE_HARNESS = r"""
const { runSave, saveOrder, SAVE_BUFFER_ORDER } = await import('./doxbench-save.js');

const KEY = { repository: 'fixture-repo', ref: 'main',
              tile_kind: 'staged', tile_id: 'topic-x' };
const OUTLINE = 'ideation/staging/topic-x/topic-x.md';
const DOCUMENT = 'ideation/staging/topic-x/detail.md';

// LOWERCASE HEX, deterministically derived from the seed. The only identity a
// real gate can report is a lowercase SHA-256 one (`doxbench_hash`), and
// doxbench-state.js refuses any other when it writes one into working state, so
// a fixture emitting 64 arbitrary characters would model an impossible server.
const hex = (seed) => {
  let out = '';
  for (const ch of String(seed)) out += ch.charCodeAt(0).toString(16).padStart(2, '0');
  return out.padEnd(64, '0').slice(0, 64);
};
const identity = (seed) => ({ algorithm: 'sha256', hex: hex(seed) });

function buffer(kind, path, { dirty = true, owned = true } = {}) {
  const base = identity(kind + 'base');
  return {
    kind, path, owned, repository: KEY.repository,
    base_ref: 'main', base_revision: 'rev-' + kind,
    base_hash: base, base_content: '# ' + kind + '\n',
    current_hash: dirty ? identity(kind + 'curr') : base,
    content: dirty ? '# ' + kind + ' edited\n' : '# ' + kind + '\n',
    dirty, load_state: 'ready', hash_generation: dirty ? 1 : 0,
    hash_pending: false,
  };
}

function state(over = {}) {
  return {
    key: KEY, active_buffer: 'outline',
    buffers: {
      outline: buffer('outline', OUTLINE, over.outline || {}),
      document: buffer('document', DOCUMENT, over.document || {}),
    },
  };
}

// A transport that records every request and answers from a script keyed by
// buffer kind. `null` in the script means "accept"; a string means "refuse with
// this message".
function transportFor(script, calls) {
  let n = 0;
  return async (request) => {
    calls.push(request);
    const verdict = script[request.kind];
    n += 1;
    if (verdict) return { ok: false, message: verdict };
    return {
      ok: true, ref: 'draft/topic-x', commit: 'c'.repeat(40 - 1) + String(n),
      document: request.document, record: 'record-' + n,
      revision: 'newrev-' + n,
      content_hash: { algorithm: 'sha256', hex: hex(request.kind + 'saved') },
    };
  };
}

async function scenario(script, over = {}) {
  const calls = [];
  const outcome = await runSave(state(over), {
    transport: transportFor(script, calls),
  });
  return { calls, outcome };
}

const results = {
  order: SAVE_BUFFER_ORDER,
  plan: saveOrder(state()),
  planWithCleanOutline: saveOrder(state({ outline: { dirty: false } })),
  bothAccepted: await scenario({}),
  documentRefused: await scenario({ document: 'the document base moved' }),
  outlineRefused: await scenario({ outline: 'the outline base moved' }),
  cleanOutline: await scenario({}, { outline: { dirty: false } }),
  bothClean: await scenario({}, { outline: { dirty: false },
                                  document: { dirty: false } }),
  unbackedDocument: await scenario({}, { document: { owned: false } }),
};
console.log(JSON.stringify(results));
"""


@pytest.fixture(scope="module")
def save_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench Save orchestration probe")
    assert SAVE_JS.is_file(), (
        f"doxbench-save.js does not exist yet (expected at {SAVE_JS}); T077 "
        "creates it and every T071 orchestration test depends on it")
    root = tmp_path_factory.mktemp("doxbench-save-harness")
    (root / "views").mkdir()
    shutil.copy(SAVE_JS, root / "views" / "doxbench-save.js")
    shutil.copy(STATE_JS, root / "views" / "doxbench-state.js")
    (root / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    harness = root / "views" / "save-harness.mjs"
    harness.write_text(_SAVE_HARNESS, encoding="utf-8")
    done = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


# ---- outline first -------------------------------------------------------

def test_the_declared_save_order_is_outline_then_document(save_results):
    """The order is a declared constant, not an emergent property of whichever
    buffer happened to be iterated first."""
    assert save_results["order"] == ["outline", "document"]


def test_both_dirty_buffers_are_attempted_outline_first(save_results):
    """FR-034's ordering clause: Outline before Document, always."""
    calls = save_results["bothAccepted"]["calls"]
    assert [c["kind"] for c in calls] == ["outline", "document"]


def test_a_clean_outline_is_skipped_and_the_document_still_saves(save_results):
    """FR-031's "only changed buffers" clause. Skipping is not reordering: the
    Document is still attempted, and the Outline is reported `unchanged` rather
    than silently omitted."""
    scenario = save_results["cleanOutline"]
    assert [c["kind"] for c in scenario["calls"]] == ["document"]
    outline = _outcome_for(scenario, "outline")
    assert outline["status"] == "unchanged"
    assert outline["action"] is None


def test_two_clean_buffers_save_nothing_and_report_unchanged(save_results):
    """An explicit Save with nothing to persist performs no governance action at
    all — it does not open a session to discover it had nothing to do."""
    scenario = save_results["bothClean"]
    assert scenario["calls"] == []
    assert scenario["outcome"]["status"] == "unchanged"
    assert all(b["status"] == "unchanged" for b in scenario["outcome"]["buffers"])


def test_an_unowned_buffer_is_refused_rather_than_attempted(save_results):
    """FR-036 at the client: a buffer the tile does not own is not sent. The
    refusal is reported per buffer and the transport is never called for it."""
    scenario = save_results["unbackedDocument"]
    assert [c["kind"] for c in scenario["calls"]] == ["outline"]
    document = _outcome_for(scenario, "document")
    assert document["status"] == "refused"
    assert document["message"]


# ---- per-buffer action ---------------------------------------------------

def test_each_buffer_declares_the_existing_action_its_path_implies(save_results):
    """FR-031: an existing path is the existing edit action; a buffer with no
    path yet is the existing create action. Save introduces no third verb."""
    plan = save_results["plan"]
    by_kind = {row["kind"]: row for row in plan}
    assert by_kind["outline"]["action"] == "edit-document"
    assert by_kind["document"]["action"] == "edit-document"
    for call in save_results["bothAccepted"]["calls"]:
        assert call["action"] in ("edit-document", "create-document")


def test_the_plan_skips_a_clean_buffer(save_results):
    kinds = [row["kind"] for row in save_results["planWithCleanOutline"]]
    assert kinds == ["document"]


# ---- partial success ----------------------------------------------------

def test_a_refused_document_leaves_the_outlines_commit_standing(save_results):
    """FR-035's core claim, and the US4 independent test: the first base advances
    while the second stays dirty. Reported SEPARATELY — one committed, one
    refused — never as a single blended verdict."""
    scenario = save_results["documentRefused"]
    assert scenario["outcome"]["status"] == "partial"
    outline = _outcome_for(scenario, "outline")
    document = _outcome_for(scenario, "document")
    assert outline["status"] == "committed"
    assert outline["ref"] == "draft/topic-x"
    assert outline["revision"]
    assert document["status"] == "refused"
    assert document["message"] == "the document base moved"
    assert document["revision"] is None


def test_a_refused_document_stays_dirty_and_the_outline_goes_clean(save_results):
    """The state half of the same claim: only the successful buffer rebases."""
    resulting = save_results["documentRefused"]["outcome"]["state"]
    assert resulting["buffers"]["outline"]["dirty"] is False
    assert resulting["buffers"]["document"]["dirty"] is True
    assert resulting["buffers"]["document"]["content"] == "# document edited\n"


def test_the_outlines_base_advances_to_what_was_actually_committed(save_results):
    """"Advance only successful bases" means adopting the identity the SERVER
    reported, not the client's optimistic guess."""
    scenario = save_results["documentRefused"]
    outline_outcome = _outcome_for(scenario, "outline")
    saved = scenario["outcome"]["state"]["buffers"]["outline"]
    assert saved["base_hash"] == outline_outcome["content_hash"]
    assert saved["base_content"] == "# outline edited\n"
    assert saved["base_revision"] == outline_outcome["revision"]
    assert saved["base_ref"] == outline_outcome["ref"]


def test_a_refused_outline_does_not_attempt_the_document(save_results):
    """Outline-first is a DEPENDENCY, not merely an order. If the Outline refuses
    there is no landed ancestry for the Document to be saved against, so it is
    reported `not_attempted` rather than sent anyway."""
    scenario = save_results["outlineRefused"]
    assert [c["kind"] for c in scenario["calls"]] == ["outline"]
    assert _outcome_for(scenario, "outline")["status"] == "refused"
    assert _outcome_for(scenario, "document")["status"] == "not_attempted"
    assert scenario["outcome"]["status"] == "refused"


def test_a_fully_successful_save_reports_committed_for_both(save_results):
    scenario = save_results["bothAccepted"]
    assert scenario["outcome"]["status"] == "committed"
    assert [b["status"] for b in scenario["outcome"]["buffers"]] == [
        "committed", "committed"]
    resulting = scenario["outcome"]["state"]
    assert resulting["buffers"]["outline"]["dirty"] is False
    assert resulting["buffers"]["document"]["dirty"] is False


def test_every_buffer_outcome_carries_the_declared_outcome_fields(save_results):
    """data-model's `PerBufferSaveOutcome`, pinned field by field so a partial
    outcome cannot be reported with a field quietly missing."""
    for scenario_name in ("bothAccepted", "documentRefused", "outlineRefused"):
        for row in save_results[scenario_name]["outcome"]["buffers"]:
            assert set(row) == {"kind", "status", "action", "ref", "revision",
                                "content_hash", "message"}, row
            assert row["status"] in {"unchanged", "committed", "refused",
                                     "not_attempted"}


def _outcome_for(scenario, kind):
    for row in scenario["outcome"]["buffers"]:
        if row["kind"] == kind:
            return row
    raise AssertionError(f"no outcome reported for {kind}: {scenario['outcome']}")


# ---- revision ancestry (server-measured) --------------------------------

def test_the_second_saves_commit_descends_from_the_first_saves_commit(
        scratch_repo, tmp_path):
    """The ancestry claim, measured on the branch: the Document's commit has the
    Outline's commit as its parent, so "saved against a compatible session
    ancestry" is a fact about the graph rather than an ordering convention."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = (scratch_repo.root / OUTLINE).read_text(encoding="utf-8")

    first = _first_save(scratch_repo, registry, document=OUTLINE,
                        content="# Demo Topic\n\noutline saved.\n",
                        base_hash=dh.sha256_hex(served), at=AT, git=git)
    second = _first_save(scratch_repo, registry, document=NEW_DOC,
                         content="# Detail\n\ndocument saved.\n", at=AT_LATER,
                         git=git)

    worktree = Path(first.session.worktree)
    parent = git.git(worktree, "rev-parse", f"{second.commit.sha}^").strip()
    assert parent == first.commit.sha
    assert git.is_ancestor(first.commit.sha, second.commit.sha) is True


def test_a_refused_second_save_never_rewrites_the_first_saves_commit(
        scratch_repo, tmp_path):
    """FR-035's "MUST NOT rewrite successful history" at the graph level: the
    Outline's commit sha, and the branch tip it established, are untouched by the
    Document's refusal."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = (scratch_repo.root / OUTLINE).read_text(encoding="utf-8")
    first = _first_save(scratch_repo, registry, document=OUTLINE,
                        content="# Demo Topic\n\noutline saved.\n",
                        base_hash=dh.sha256_hex(served), at=AT, git=git)

    # A second Save of the SAME document still carrying the base it was first
    # loaded from -- the realistic stale race, now that the first Save advanced it.
    with pytest.raises(bs.SessionRefused):
        _first_save(scratch_repo, registry, document=OUTLINE,
                    content="# Demo Topic\n\nagainst a stale base.\n",
                    at=AT_LATER, git=git, base_hash=dh.sha256_hex(served))

    worktree = Path(first.session.worktree)
    assert git.head(worktree) == first.commit.sha
    assert git.commits_ahead("main", DRAFT) == 1
    assert (worktree / OUTLINE).read_text(encoding="utf-8") == \
        "# Demo Topic\n\noutline saved.\n"


# ---------------------------------------------------------------------------
# T100 P1-3 (operator finding, real corpus, 2026-08-01): a staged topic with
# NO outline document must still Save its document buffer. validatedState
# demanded an object for EVERY buffer kind, so the seam threw
# ("outline buffer must be an object") before any plan was built.
# An ABSENT buffer kind is now skipped; at least one buffer must remain.
# ---------------------------------------------------------------------------

_ABSENT_OUTLINE_HARNESS = """
import { saveOrder, savePlanState } from "./doxbench-save.mjs";

const out = {};
const documentBuffer = {
  kind: "document", path: "docs/registry.md", owned: true,
  base_ref: "main", base_revision: "r1",
  base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  base_content: "# Registry", content: "# Registry edited", dirty: true,
  hash_pending: false, hash_generation: 1,
};
const state = {
  key: { repository: "real-repo", ref: "main",
         tile_kind: "staged", tile_id: "client-credential-escrow-registry" },
  active_buffer: "document",
  buffers: { document: documentBuffer },   // NO outline key at all
};
try {
  out.order = saveOrder(state);
  const plan = savePlanState({ state });
  out.rows = plan.rows ? plan.rows.map((r) => r.kind)
    : (plan.order || out.order);
  out.threw = null;
} catch (error) {
  out.threw = String(error && error.message || error);
}
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def absent_outline_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench save probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-absent-outline")
    shutil.copy(SAVE_JS, tmp_path / "doxbench-save.mjs")
    harness = tmp_path / "absent-outline-harness.mjs"
    harness.write_text(_ABSENT_OUTLINE_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_an_absent_outline_buffer_no_longer_blocks_the_document_save(absent_outline_results):
    r = absent_outline_results
    assert r["threw"] is None, f"the seam still throws: {r['threw']!r}"
    kinds = [row["kind"] if isinstance(row, dict) else row
             for row in r["order"]]
    assert kinds == ["document"]


# ---------------------------------------------------------------------------
# T100 run-3 blocker (operator pinpoint, 2026-08-01): the CLIENT-emitted
# first-edit `scope_kind` must speak the SERVER's session vocabulary
# (branch_session.SCOPE_KINDS) — the tile vocabulary's `staged` was being
# forwarded verbatim while the server requires `staged-topic`. The route
# tests never caught it because they build bodies server-side; this test
# pins the two sides against each other across the language boundary.
# ---------------------------------------------------------------------------

MODEL_JS = (Path(__file__).resolve().parent.parent.parent / "scripts"
            / "ideation_dashboard" / "web" / "views"
            / "staging-workbench-model.js")

_SCOPE_KIND_HARNESS = """
import { firstEditBody } from "./staging-workbench-model.mjs";

const out = {};
for (const tileKind of ["staged", "cluster", "possible"]) {
  const body = firstEditBody("fixture-repo",
    { repository: "fixture-repo", ref: "main",
      tile_kind: tileKind, tile_id: "topic-x" },
    { document: "docs/topic.md", content: "# T",
      base_hash: "c".repeat(64) });
  out[tileKind] = body.scope_kind;
}
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def emitted_scope_kinds(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the scope-kind contract probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-scope-kind")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    harness = tmp_path / "scope-kind-harness.mjs"
    harness.write_text(_SCOPE_KIND_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_every_emitted_first_edit_scope_kind_is_a_server_scope_kind(emitted_scope_kinds):
    from ideation_dashboard import branch_session
    server_kinds = set(branch_session.SCOPE_KINDS)
    for tile_kind, emitted in emitted_scope_kinds.items():
        assert emitted in server_kinds, (
            f"tile kind {tile_kind!r} emits scope_kind {emitted!r}, which the "
            f"server's session vocabulary {sorted(server_kinds)} refuses — "
            "the T100 run-3 Save blocker")
