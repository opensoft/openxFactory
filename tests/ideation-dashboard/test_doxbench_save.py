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


def test_an_undecodable_files_refusal_names_the_class_and_echoes_no_bytes(
        scratch_repo):
    """Wave re-review P3-5. A non-UTF-8 file cannot be revalidated: the strict
    server-side decode raises, and the honest answer is a refusal (the
    strict-decode asymmetry is DELIBERATE — see the why-comment at the read).
    But the refusal SENTENCE must state only the exception CLASS: a
    `UnicodeDecodeError`'s str embeds the offending byte value and its offset
    from the file being edited, and refusals never echo document content."""
    target = scratch_repo.root / OUTLINE
    target.write_bytes(b"# Demo Topic\n\n\xff\xfe not UTF-8 \x81\n")

    refusal = bs.first_edit_base_refusal(
        document=OUTLINE, root=scratch_repo.root,
        action=gc.ACTION_EDIT_DOCUMENT,
        base_hash=dh.sha256_hex("# whatever the client held\n"))

    assert refusal is not None
    assert "UnicodeDecodeError" in refusal, (
        "the refusal names the exception CLASS, so the operator still learns "
        "WHY the read failed")
    # ... and nothing more than the class: no quoted byte, no offset. The
    # document path is the only permitted content-adjacent detail.
    scrubbed = refusal.replace(OUTLINE, "").replace("UnicodeDecodeError", "")
    assert "0x" not in scrubbed
    assert "position" not in scrubbed
    assert not any(ch.isdigit() for ch in scrubbed), (
        f"byte-offset or byte-value digits leaked into the refusal: {refusal!r}")


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
const { runSave, saveOrder, saveBufferOrder, SAVE_DOCUMENT_ORDER_RULE } =
  await import('./doxbench-save.js');

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
  order: saveBufferOrder(Object.keys(state().buffers)),
  orderRule: SAVE_DOCUMENT_ORDER_RULE,
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

def test_the_declared_save_order_is_outline_then_documents(save_results):
    """RE-PINNED by `add-doxbench-editing-phase-b` (task 6.1).

    Phase A pinned a declared CONSTANT (`SAVE_BUFFER_ORDER`, a fixed ordered
    pair). Phase B holds N documents, so a constant list cannot express the
    order and the ratified contract states a RULE instead: the outline first
    because its commit is the session ancestry, then every document in a
    deterministic order the realization declares. The assertion is not
    weakened -- the order is still not an emergent property of whichever buffer
    happened to be iterated first; it is now a declared FUNCTION of the buffer
    keys, and the declaration itself is asserted beside it.
    """
    assert save_results["order"] == ["outline", "document"]
    assert save_results["orderRule"] == (
        "ascending lexicographic by buffer key (UTF-16 code unit)")


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
    by_kind = {row["key"]: row for row in plan}
    assert by_kind["outline"]["action"] == "edit-document"
    assert by_kind["document"]["action"] == "edit-document"
    for call in save_results["bothAccepted"]["calls"]:
        assert call["action"] in ("edit-document", "create-document")


def test_the_plan_skips_a_clean_buffer(save_results):
    kinds = [row["key"] for row in save_results["planWithCleanOutline"]]
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
            assert set(row) == {"key", "status", "action", "ref", "revision",
                                "content_hash", "message"}, row
            assert row["status"] in {"unchanged", "committed", "refused",
                                     "not_attempted"}


def _outcome_for(scenario, kind):
    for row in scenario["outcome"]["buffers"]:
        if row["key"] == kind:
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
#
# T104 F6-4 (harness fix, 2026-08-04): the original harness called
# `savePlanState({ state })` -- the wrong argument shape (the real seam
# contract is the editor's request, `{ key, buffers: [<request rows>] }`; see
# savePlanState itself and app.js's `save:` composition) -- and DISCARDED the
# result, so despite naming the seam it exercised only saveOrder over a
# hand-built state (`savePlanState({state})` yields `{key: undefined,
# buffers: {}}`, an empty plan). It now drives savePlanState with the real
# request shape and runs the plan end to end: a lone document ROW plans, is
# sent, and commits, while the absent outline is reported `unchanged` rather
# than blocking anything.
# ---------------------------------------------------------------------------

_ABSENT_OUTLINE_HARNESS = """
import { runSave, saveOrder, savePlanState } from "./doxbench-save.mjs";

const out = {};
// The row exactly as doxbench-editor.js's bufferRequestRow hands it over.
const documentRow = {
  kind: "document", path: "docs/registry.md", owned: true,
  base_ref: "main", base_revision: "r1",
  base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  content: "# Registry edited", dirty: true, hash_pending: false,
};
const request = {
  key: { repository: "real-repo", ref: "main",
         tile_kind: "staged", tile_id: "client-credential-escrow-registry" },
  buffers: [documentRow],   // NO outline row at all
};
try {
  const state = savePlanState(request);
  out.planKey = state.key;
  out.planKinds = Object.keys(state.buffers);
  out.rows = saveOrder(state).map((row) => ({
    key: row.key, action: row.action, document: row.document,
    base_hash: row.base_hash, refusal: row.refusal,
  }));
  const sent = [];
  const outcome = await runSave(state, { transport: async (req) => {
    sent.push(req.kind);
    return { ok: true, ref: "draft/client-credential-escrow-registry",
             revision: "newrev-1",
             content_hash: { algorithm: "sha256", hex: "e".repeat(64) } };
  } });
  out.sent = sent;
  out.outcome = outcome.buffers.map((row) => ({
    key: row.key, status: row.status }));
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
    # the reshaped state carries the request's own key and ONLY the rows sent
    assert r["planKey"]["tile_id"] == "client-credential-escrow-registry"
    assert r["planKinds"] == ["document"]
    # the plan: one document row, the edit action (the path exists in the
    # buffer), its declared base hex, and no refusal from the missing outline
    assert r["rows"] == [{
        "key": "document", "action": "edit-document",
        "document": "docs/registry.md", "base_hash": "c" * 64,
        "refusal": None,
    }]
    # and the run itself: the document is sent and commits; the absent outline
    # is reported `unchanged` rather than blocking the document behind it
    assert r["sent"] == ["document"]
    outcome = {row["key"]: row["status"] for row in r["outcome"]}
    assert outcome == {"outline": "unchanged", "document": "committed"}


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


# ---------------------------------------------------------------------------
# T104 F5-1 (doxBench review, 2026-08-04): the WHOLE client chain, composed
# the way production composes it — the transport's answer is
# `firstEditVerdict(<route payload>)` (swb-session.firstEditTransport), and
# `runSave`'s readVerdict adopts `answer.action` into a committed row. The
# verdict mapping used to carry `action` only on its ok:false return (where
# readVerdict ignores it) and omit it from ok:true (where readVerdict reads
# it), so the server's own create-vs-edit resolution — the SUCCESS payload's
# `verb` — could never override the client's prediction. This harness drives
# the two real modules together across that seam.
# ---------------------------------------------------------------------------

_SERVER_VERB_HARNESS = """
import { runSave } from "./doxbench-save.mjs";
import { firstEditVerdict } from "./staging-workbench-model.mjs";

const out = {};
const documentBuffer = {
  kind: "document", path: "ideation/staging/topic-x/detail.md", owned: true,
  base_ref: "main", base_revision: "r1",
  base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  base_content: "# Detail", content: "# Detail edited", dirty: true,
  hash_pending: false, hash_generation: 1,
};
const state = {
  key: { repository: "fixture-repo", ref: "main",
         tile_kind: "staged", tile_id: "topic-x" },
  active_buffer: "document",
  buffers: { document: documentBuffer },
};

// The realistic divergence: the buffer HAS a path, so the client plans the
// edit action — but the branch session's own tree does not carry the file
// yet, so the server resolved and reports the CREATE verb.
const SERVER_PAYLOAD = {
  ok: true, verb: "create-document", ref: "draft/topic-x",
  commit: "e".repeat(40), document: documentBuffer.path,
  record: "ideation/dashboard/gate-records/draft-topic-x/create.yaml",
  content_hash: { algorithm: "sha256", hex: "f".repeat(64) },
  session: "opened",
};
{
  const requests = [];
  const outcome = await runSave(state, {
    transport: async (req) => { requests.push(req);
      return firstEditVerdict(SERVER_PAYLOAD); } });
  out.serverVerb = {
    plannedAction: requests[0] && requests[0].action,
    committedAction: outcome.buffers.find((b) => b.key === "document").action,
    status: outcome.buffers.find((b) => b.key === "document").status,
  };
}
{
  // The null-payload arm of the same finding: a transport that produced no
  // verdict at all maps to the FIXED refusal — never a TypeError mid-Save.
  const outcome = await runSave(state, {
    transport: async () => firstEditVerdict(null) });
  const row = outcome.buffers.find((b) => b.key === "document");
  out.nullVerdict = { status: row.status, message: row.message };
}
console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def server_verb_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the server-verb save probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-server-verb")
    shutil.copy(SAVE_JS, tmp_path / "doxbench-save.mjs")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    harness = tmp_path / "server-verb-harness.mjs"
    harness.write_text(_SERVER_VERB_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_committed_row_reports_the_servers_verb_not_the_clients_guess(
        server_verb_results):
    """SC: the client predicted edit (the path exists in ITS buffer), the
    server answered create (the path was new to the tree it wrote) — and the
    committed row reports the SERVER's answer."""
    s = server_verb_results["serverVerb"]
    assert s["plannedAction"] == "edit-document", "precondition: client planned edit"
    assert s["status"] == "committed"
    assert s["committedAction"] == "create-document", (
        "the committed row must adopt the server's own resolved verb")


def test_a_transport_with_no_payload_yields_the_mapped_refusal_mid_save(
        server_verb_results):
    n = server_verb_results["nullVerdict"]
    assert n["status"] == "refused"
    assert n["message"] == (
        "the Save transport returned no verdict for this buffer")


# ==========================================================================
# add-doxbench-editing-phase-b §6: N DOCUMENTS, ancestry-then-independence.
#
# The ordering rule Phase A could not express and Phase B ratifies (design D3):
# the outline first as ANCESTRY, then every dirty document INDEPENDENTLY, one
# document's refusal stopping no other. This harness is the shape no Phase A
# scenario could take -- an outline plus three documents -- and it drives the
# three cases the delta's own scenarios name:
#
#   * all four land;
#   * the outline REFUSES, so every document is `not_attempted` with the
#     missing-ancestry reason and nothing is sent;
#   * one document refuses, and the ones behind it are STILL ATTEMPTED, because
#     they descend from the same ancestry and the refusal was not about them.
#
# Plus the tile Save's scope (D4): the same pipeline, restricted to one document
# plus the ancestry step, persisting no other loaded document.
# ==========================================================================

_N_DOCUMENT_HARNESS = r"""
const { runSave, saveOrder, saveBufferOrder } =
  await import('./doxbench-save.js');

const KEY = { repository: 'fixture-repo', ref: 'main',
              tile_kind: 'staged', tile_id: 'topic-x' };
const OUTLINE = 'ideation/staging/topic-x/topic-x.md';
const ALPHA = 'ideation/staging/topic-x/alpha.md';
const MIDDLE = 'ideation/staging/topic-x/nested/alpha.md';
const ZULU = 'ideation/staging/topic-x/zulu.md';

const hex = (seed) => {
  let out = '';
  for (const ch of String(seed)) out += ch.charCodeAt(0).toString(16).padStart(2, '0');
  return out.padEnd(64, '0').slice(0, 64);
};
const identity = (seed) => ({ algorithm: 'sha256', hex: hex(seed) });

function buffer(kind, path, { dirty = true, owned = true } = {}) {
  const base = identity(path + 'base');
  return {
    kind, path, owned, repository: KEY.repository,
    base_ref: 'main', base_revision: 'rev',
    base_hash: base, base_content: '# ' + path + '\n',
    current_hash: dirty ? identity(path + 'curr') : base,
    content: dirty ? '# ' + path + ' edited\n' : '# ' + path + '\n',
    dirty, load_state: 'ready', hash_generation: dirty ? 1 : 0,
    hash_pending: false,
  };
}

function state(over = {}) {
  return {
    key: KEY, active_buffer: ALPHA,
    buffers: {
      outline: buffer('outline', OUTLINE, over.outline || {}),
      [ZULU]: buffer('document', ZULU, over[ZULU] || {}),
      [ALPHA]: buffer('document', ALPHA, over[ALPHA] || {}),
      [MIDDLE]: buffer('document', MIDDLE, over[MIDDLE] || {}),
    },
  };
}

// The transport answers from a script keyed by DOCUMENT PATH (the outline by
// its own path), so a refusal can be aimed at exactly one buffer.
function transportFor(script, calls) {
  let n = 0;
  return async (request) => {
    calls.push({ kind: request.kind, document: request.document });
    const verdict = script[request.document];
    n += 1;
    if (verdict) return { ok: false, message: verdict };
    return {
      ok: true, ref: 'draft/topic-x', revision: 'newrev-' + n,
      document: request.document,
      content_hash: { algorithm: 'sha256', hex: hex(request.document + 'saved') },
    };
  };
}

async function scenario(script, over = {}, options = {}) {
  const calls = [];
  const outcome = await runSave(state(over), {
    transport: transportFor(script, calls), ...options });
  return {
    calls,
    status: outcome.status,
    rows: outcome.buffers.map((r) => ({ key: r.key, status: r.status,
                                        message: r.message })),
    dirty: Object.fromEntries(Object.entries(outcome.state.buffers)
      .map(([k, b]) => [k, b.dirty])),
    bases: Object.fromEntries(Object.entries(outcome.state.buffers)
      .map(([k, b]) => [k, b.base_content])),
  };
}

console.log(JSON.stringify({
  order: saveBufferOrder(Object.keys(state().buffers)),
  plan: saveOrder(state()).map((r) => r.key),
  allLand: await scenario({}),
  outlineRefused: await scenario({ [OUTLINE]: 'the outline base moved' }),
  oneDocumentRefused: await scenario({ [MIDDLE]: 'that document base moved' }),
  tileScoped: await scenario({}, {}, { only: ALPHA }),
  tileScopedCleanOutline: await scenario(
    {}, { outline: { dirty: false } }, { only: ALPHA }),
  tileScopedOutlineRefused: await scenario(
    { [OUTLINE]: 'the outline base moved' }, {}, { only: ALPHA }),
}));
"""


@pytest.fixture(scope="module")
def n_document_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the N-document Save probe")
    root = tmp_path_factory.mktemp("doxbench-save-n-documents")
    (root / "views").mkdir()
    shutil.copy(SAVE_JS, root / "views" / "doxbench-save.js")
    shutil.copy(STATE_JS, root / "views" / "doxbench-state.js")
    (root / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    harness = root / "views" / "n-document-harness.mjs"
    harness.write_text(_N_DOCUMENT_HARNESS, encoding="utf-8")
    done = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


def test_the_outline_leads_and_documents_follow_in_the_declared_order(
        n_document_results):
    """Task 6.1: the outline FIRST because its commit is the session ancestry,
    then every document in the declared deterministic order."""
    assert n_document_results["order"] == [
        "outline",
        "ideation/staging/topic-x/alpha.md",
        "ideation/staging/topic-x/nested/alpha.md",
        "ideation/staging/topic-x/zulu.md",
    ]
    assert n_document_results["plan"] == n_document_results["order"]


def test_four_dirty_buffers_each_produce_their_own_gate_action(
        n_document_results):
    """The delta's `Several dirty documents are saved` scenario: the outline runs
    first and each changed document produces its OWN existing gate-action commit,
    with no combined or hidden write verb."""
    scenario = n_document_results["allLand"]
    assert scenario["status"] == "committed"
    assert [c["document"] for c in scenario["calls"]] == [
        "ideation/staging/topic-x/topic-x.md",
        "ideation/staging/topic-x/alpha.md",
        "ideation/staging/topic-x/nested/alpha.md",
        "ideation/staging/topic-x/zulu.md",
    ]
    assert all(row["status"] == "committed" for row in scenario["rows"])
    assert all(dirty is False for dirty in scenario["dirty"].values())


def test_a_refused_outline_stops_every_document_with_the_ancestry_reason(
        n_document_results):
    """The delta's `The outline's save refuses` scenario: every dirty document is
    reported `not_attempted` with the missing-ancestry reason and MUST NOT be
    sent, and every buffer's text, base and dirty state is preserved exactly."""
    scenario = n_document_results["outlineRefused"]
    assert scenario["status"] == "refused"
    assert [c["document"] for c in scenario["calls"]] == [
        "ideation/staging/topic-x/topic-x.md"], (
        "a document was sent with no ancestry to descend from")
    by_key = {row["key"]: row for row in scenario["rows"]}
    assert by_key["outline"]["status"] == "refused"
    for key in ("ideation/staging/topic-x/alpha.md",
                "ideation/staging/topic-x/nested/alpha.md",
                "ideation/staging/topic-x/zulu.md"):
        assert by_key[key]["status"] == "not_attempted"
        assert "no session ancestry" in by_key[key]["message"]
    assert all(dirty is True for dirty in scenario["dirty"].values())


def test_one_documents_refusal_stops_no_other_document(n_document_results):
    """The delta's `One document's save refuses` scenario, and the whole reason
    design D3 restated the rule instead of lengthening the list: the third
    document MUST still be attempted, because it descends from the same ancestry
    and the refusal was not about it. Keeping Phase A's chain here would report
    untried work as blocked by a refusal that had nothing to do with it -- a
    false statement about both buffers."""
    scenario = n_document_results["oneDocumentRefused"]
    assert scenario["status"] == "partial"
    # ALL FOUR were attempted: the refusal in the middle stopped nothing.
    assert [c["document"] for c in scenario["calls"]] == [
        "ideation/staging/topic-x/topic-x.md",
        "ideation/staging/topic-x/alpha.md",
        "ideation/staging/topic-x/nested/alpha.md",
        "ideation/staging/topic-x/zulu.md",
    ]
    by_key = {row["key"]: row for row in scenario["rows"]}
    # The report NAMES the committed, refused and remaining buffers separately.
    assert by_key["outline"]["status"] == "committed"
    assert by_key["ideation/staging/topic-x/alpha.md"]["status"] == "committed"
    assert by_key["ideation/staging/topic-x/nested/alpha.md"]["status"] == "refused"
    assert by_key["ideation/staging/topic-x/zulu.md"]["status"] == "committed"
    assert "that document base moved" in \
        by_key["ideation/staging/topic-x/nested/alpha.md"]["message"]
    # …and NO row claims to have been blocked by it.
    assert not any(row["status"] == "not_attempted" for row in scenario["rows"])
    # The refused buffer keeps its text; the committed ones advanced.
    assert scenario["dirty"]["ideation/staging/topic-x/nested/alpha.md"] is True
    assert scenario["dirty"]["ideation/staging/topic-x/zulu.md"] is False


def test_the_tile_save_persists_that_document_plus_the_ancestry_step_only(
        n_document_results):
    """Design D4 and the delta's `The tile save runs with a dirty outline`
    scenario: the outline is persisted first as the ancestry step, that document
    is then persisted, each reporting its own verdict -- and NO other loaded
    document is persisted by that act, because a control that lives on one
    document's tile and is enabled by that document's state must not persist
    three others the human is not looking at."""
    scoped = n_document_results["tileScoped"]
    assert [c["document"] for c in scoped["calls"]] == [
        "ideation/staging/topic-x/topic-x.md",
        "ideation/staging/topic-x/alpha.md",
    ]
    keys = {row["key"] for row in scoped["rows"]}
    assert keys == {"outline", "ideation/staging/topic-x/alpha.md"}
    # The two documents the act did not touch keep their unsaved work, and are
    # not reported as refused -- nobody asked about them.
    assert scoped["dirty"]["ideation/staging/topic-x/zulu.md"] is True
    assert scoped["dirty"]["ideation/staging/topic-x/nested/alpha.md"] is True


def test_the_tile_save_skips_a_clean_outline_and_still_lands(n_document_results):
    scoped = n_document_results["tileScopedCleanOutline"]
    assert [c["document"] for c in scoped["calls"]] == [
        "ideation/staging/topic-x/alpha.md"]
    by_key = {row["key"]: row for row in scoped["rows"]}
    assert by_key["outline"]["status"] == "unchanged"
    assert by_key["ideation/staging/topic-x/alpha.md"]["status"] == "committed"


def test_the_tile_save_cannot_commit_a_document_without_the_ancestry(
        n_document_results):
    """The ancestry step is not skippable by a scoped entry point, or a tile Save
    would be a way to commit a document without the ancestry the ordering rule
    requires."""
    scoped = n_document_results["tileScopedOutlineRefused"]
    assert [c["document"] for c in scoped["calls"]] == [
        "ideation/staging/topic-x/topic-x.md"]
    by_key = {row["key"]: row for row in scoped["rows"]}
    assert by_key["outline"]["status"] == "refused"
    assert by_key["ideation/staging/topic-x/alpha.md"]["status"] == "not_attempted"
