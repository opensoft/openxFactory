"""#80, RULED by Brett Heap 2026-08-24: NO PENDING PROPOSAL SET IS EVER CLEARED
WITHOUT A FIXED-VOCABULARY NOTICE.

The filed defect was one path — a Send that replaces an unreviewed proposal set
with the new turn's, silently. The 2026-08-24 re-triage found the same silence on
two ADJACENT paths (a rekey, a document switch), and the ruling covers all three.

What is NOT in scope, and is deliberately re-pinned rather than touched: the
replacement-on-success itself is a RULING (doxbench-chat-model.js's proposal
banner, pinned by test_doxbench_proposals.py's
`test_a_new_turn_replaces_the_proposal_set_entirely`). A new turn IS the only
stale-proposal recovery. The defect is the SILENCE, never the replacement.

THREE PATHS, TWO FORMS. The form each path gets follows the path's own nature:

  * SEND is a human press, and it is refusable before anything has moved — so it
    gets the house TWO-PRESS ARM (`repo-selector.js`'s filter-trash idiom, and
    the arm this very rail carried on its retired Unload control). The first
    press refuses with a fixed sentence naming the pending TARGETS, dispatches
    nothing, and arms; the second press sends. The arm is keyed by the sentence's
    own subject, so any change to the pending set re-arms from scratch.

  * REKEY and the DOCUMENT SWITCH are consequences, not presses: by the time
    either reaches the clear, the thing that caused it has already happened (the
    tile has moved onto a new scope key; the canvas has already moved its active
    buffer and the thread has already been read). Neither can be refused without
    leaving the rail disagreeing with the surface beside it, so each gets the
    honest form for a clear that cannot be refused: the fixed-vocabulary notice
    announced ON the clear, naming the targets that went.

FIXED VOCABULARY THROUGHOUT: every sentence is composed from the state's own
buffer KEYS (the card badge's `title` idiom) and never from a proposal's summary
or content. The probes below carry deliberately distinctive summary/content text
and assert it never reaches a sentence.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")
WEB_VIEWS = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
CHAT_VIEW_JS = WEB_VIEWS / "doxbench-chat.js"
CHAT_MODEL_JS = WEB_VIEWS / "doxbench-chat-model.js"

# The two strings a sentence must NEVER carry: a proposal's own summary and its
# own content. Both ride every fixture record below.
SECRET_SUMMARY = "SUMMARY-THAT-MUST-NEVER-BE-ECHOED"
SECRET_CONTENT = "CONTENT-THAT-MUST-NEVER-BE-ECHOED"


def _stage(tmp_path):
    """Copy both modules as .mjs and re-point the view's own import."""
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")


def _run(tmp_path, name, body):
    harness = tmp_path / name
    harness.write_text(body, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# (a) SEND — the two-press arm, driven through the exported DOM-free seam
# ---------------------------------------------------------------------------

_ARM_HARNESS = """
import { createTurnDispatcher } from "./doxbench-chat.mjs";
import { createChatState, adoptCatalog, selectModel, editComposer, beginTurn,
         settleTurnSuccess, proposalsOf, rejectProposal, markProposalApplied,
         refreshProposalCurrency, pendingProposalTargets }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const LIVE = "d".repeat(64);
const MOVED = "e".repeat(64);
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" };
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] };
const bufferOf = (kind, path) => ({ kind, path, base_ref: "main",
  base_revision: "r1", base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: LIVE },
  hash_pending: false, content: "# " + kind, dirty: false });
const editorState = () => ({ active_buffer: "document", buffers: {
  outline: bufferOf("outline", "docs/outline.md"),
  document: bufferOf("document", "docs/detail.md"),
  "docs/other.md": bufferOf("document", "docs/other.md") } });
const OBSERVED = { outline: LIVE, document: LIVE, "docs/other.md": LIVE };
const proposal = (target) => ({ target, base_hash: LIVE,
  summary: "__SECRET_SUMMARY__", content: "__SECRET_CONTENT__" });
const successWith = (targets) => ({ schema_version: 1,
  kind: "workbench-chat-turn-v2-success", client_turn_id: "t-1",
  assistant_turn_id: "a-1", model_id: "model-a", observed_hashes: OBSERVED,
  assistant_prose: "here you go", proposals: targets.map(proposal) });

const idle = () => editComposer(selectModel(
  adoptCatalog(createChatState(KEY), ENVELOPE), "model-a"), "first question");
// A settled turn that LEFT a pending set behind, then a fresh composer for the
// next press (settleTurnSuccess clears the composer it submitted).
const withPending = (targets) => editComposer(
  settleTurnSuccess(beginTurn(idle()), successWith(targets)), "next question");

function rig() {
  let calls = 0;
  const dispatcher = createTurnDispatcher({
    turnIdFactory: (n) => "turn-" + n,
    transports: { chatTurn: async () => { calls += 1; return { ok: true,
      status: 200, payload: successWith(["outline"]) }; } } });
  return { dispatcher, consulted: () => calls };
}
const context = { scopeKey: KEY, editorState };
const failureOf = (s) => (s.lastFailure
  ? { error: s.lastFailure.error, message: s.lastFailure.message } : null);

// ---- the pure selector the sentences take their subject from ----
{
  let s = withPending(["outline", "docs/other.md"]);
  out.pendingTargets = pendingProposalTargets(s);
  s = rejectProposal(s, "docs/other.md");
  out.pendingAfterReject = pendingProposalTargets(s);
  s = markProposalApplied(s, "outline");
  out.pendingAfterApplied = pendingProposalTargets(s);
  // a STALE record is still pending -- it is unreviewed, and it is still what a
  // Send would discard
  const stale = refreshProposalCurrency(
    withPending(["outline"]), { outline: MOVED });
  out.staleStatus = proposalsOf(stale).outline.status;
  out.pendingWhenStale = pendingProposalTargets(stale);
}

// ---- press 1 refuses and arms; press 2 dispatches ----
{
  const { dispatcher, consulted } = rig();
  const before = withPending(["outline", "docs/other.md"]);
  const first = await dispatcher.submit(before, context);
  out.firstPress = {
    refused: first.refused === true,
    ok: first.ok === true,
    transportWasConsulted: consulted() > 0,
    phase: first.state.phase,
    composer: first.state.composer,
    transcriptTurns: first.state.transcript.length,
    proposalsIntact: Object.keys(proposalsOf(first.state)).sort(),
    failure: failureOf(first.state),
    armedForFirst: dispatcher.discardArmedFor(first.state),
  };
  const second = await dispatcher.submit(first.state, context);
  out.secondPress = {
    ok: second.ok === true,
    transportConsulted: consulted(),
    phase: second.state.phase,
    // the ruled replacement still holds: the new turn's set replaces the old
    proposalKeys: Object.keys(proposalsOf(second.state)).sort(),
    failure: failureOf(second.state),
    armedAfter: dispatcher.discardArmedFor(second.state),
  };
}

// ---- a TERMINAL-ONLY set never arms: no nagging on reviewed proposals ----
{
  const { dispatcher, consulted } = rig();
  let s = withPending(["outline", "docs/other.md"]);
  s = markProposalApplied(s, "outline");
  s = rejectProposal(s, "docs/other.md");
  const result = await dispatcher.submit(s, context);
  out.terminalOnly = {
    reviewedStatuses: Object.keys(proposalsOf(s)).sort().map(
      (k) => proposalsOf(s)[k].status),
    ok: result.ok === true,
    refused: result.refused === true,
    transportConsulted: consulted(),
  };
}

// ---- an EMPTY set never arms ----
{
  const { dispatcher, consulted } = rig();
  const result = await dispatcher.submit(idle(), context);
  out.noProposals = { ok: result.ok === true,
                      transportConsulted: consulted() };
}

// ---- a STALE-only set DOES arm: unreviewed is unreviewed ----
{
  const { dispatcher, consulted } = rig();
  const s = refreshProposalCurrency(withPending(["outline"]),
                                    { outline: MOVED });
  const first = await dispatcher.submit(s, context);
  out.stalePress = {
    refused: first.refused === true,
    transportConsulted: consulted(),
    failure: failureOf(first.state),
  };
}

// ---- the arm is keyed by the SENTENCE'S OWN SUBJECT: reviewing a proposal
// between the two presses re-arms from scratch, with the narrowed sentence ----
{
  const { dispatcher, consulted } = rig();
  const before = withPending(["outline", "docs/other.md"]);
  const first = await dispatcher.submit(before, context);
  const reviewed = rejectProposal(first.state, "docs/other.md");
  out.rearmed = {
    armedBeforeTheReview: dispatcher.discardArmedFor(first.state),
    armedAfterTheReview: dispatcher.discardArmedFor(reviewed),
  };
  const second = await dispatcher.submit(reviewed, context);
  out.rearmedSecond = {
    refused: second.refused === true,
    transportConsulted: consulted(),
    failure: failureOf(second.state),
  };
  const third = await dispatcher.submit(second.state, context);
  out.rearmedThird = { ok: third.ok === true,
                       transportConsulted: consulted() };
}

// ---- a set that goes EMPTY disarms ----
{
  const { dispatcher } = rig();
  const before = withPending(["outline"]);
  const first = await dispatcher.submit(before, context);
  const cleared = rejectProposal(first.state, "outline");
  out.emptiedSet = { armed: dispatcher.discardArmedFor(cleared) };
}

// ---- …and the arm cannot OUTLIVE that set: a LATER set naming the same
// buffers must earn its own press ----
{
  const { dispatcher, consulted } = rig();
  const first = await dispatcher.submit(withPending(["outline"]), context);
  // reviewed away, so the next press has nothing pending and simply sends
  const reviewed = editComposer(
    rejectProposal(first.state, "outline"), "another question");
  const sent = await dispatcher.submit(reviewed, context);
  // …and that turn's answer brings a BRAND NEW pending set on the same key
  const again = editComposer(sent.state, "one more question");
  const nextPress = await dispatcher.submit(again, context);
  out.armDoesNotOutliveTheSet = {
    dispatchedWithNothingPending: sent.ok === true,
    newSetKeys: Object.keys(proposalsOf(again)).sort(),
    refusedForTheNewSet: nextPress.refused === true,
    transportConsulted: consulted(),
    error: nextPress.state.lastFailure && nextPress.state.lastFailure.error,
  };
}

process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def arm_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the send-arm probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-send-arm")
    _stage(tmp_path)
    return _run(tmp_path, "send-arm-harness.mjs",
                _ARM_HARNESS.replace("__SECRET_SUMMARY__", SECRET_SUMMARY)
                            .replace("__SECRET_CONTENT__", SECRET_CONTENT))


def test_the_pending_set_is_the_non_terminal_records(arm_results):
    """The subject every discard sentence names: the UNREVIEWED records, in the
    declared order. `applied` and `rejected` are terminal — they have been
    reviewed, so discarding them costs the operator nothing and warning about
    them would be the nagging the ruling explicitly refuses."""
    assert arm_results["pendingTargets"] == ["outline", "docs/other.md"]
    assert arm_results["pendingAfterReject"] == ["outline"]
    assert arm_results["pendingAfterApplied"] == []


def test_a_stale_record_is_still_pending(arm_results):
    """`stale` is NON-terminal: it is unreviewed work whose only recovery is a
    new turn, and a Send discards it exactly as it discards a `current` one."""
    assert arm_results["staleStatus"] == "stale"
    assert arm_results["pendingWhenStale"] == ["outline"]


def test_the_first_send_with_a_pending_set_refuses_and_never_dispatches(
        arm_results):
    """#80's whole finding: the Send went straight through and the unreviewed
    set was gone with nothing said. The first press now REFUSES — the transport
    is never consulted, the rail stays idle, the composer is preserved verbatim
    (FR-016), the transcript does not grow, and the proposals are still there to
    review."""
    f = arm_results["firstPress"]
    assert f["refused"] is True
    assert f["ok"] is False
    assert f["transportWasConsulted"] is False
    assert f["phase"] == "idle"
    assert f["composer"] == "next question"
    assert f["transcriptTurns"] == 2, "the settled turn's own pair, unchanged"
    assert f["proposalsIntact"] == ["docs/other.md", "outline"]


def test_the_refusal_names_the_pending_targets_and_echoes_nothing(arm_results):
    """FIXED VOCABULARY: the sentence is chosen from the CODE and its only
    variable part is composed from the state's own buffer KEYS — the card
    badge's `title` idiom. A proposal's summary and content are never read."""
    failure = arm_results["firstPress"]["failure"]
    assert failure is not None, "the refusal must reach the visible channel"
    assert failure["error"] == "proposals_discard_armed"
    assert "outline" in failure["message"]
    assert "docs/other.md" in failure["message"]
    assert SECRET_SUMMARY not in failure["message"]
    assert SECRET_CONTENT not in failure["message"]
    assert "Send again" in failure["message"], (
        "the arm must say what the second press does")


def test_the_second_press_dispatches_and_the_ruled_replacement_holds(
        arm_results):
    """The arm is a PAUSE, never a block: the second press sends. And the
    replacement it warned about is the ruled one — the new turn's set replaces
    the whole previous set (test_doxbench_proposals.py's own pin), which this
    fix does not touch."""
    s = arm_results["secondPress"]
    assert s["ok"] is True
    assert s["transportConsulted"] == 1
    assert s["phase"] == "idle"
    assert s["proposalKeys"] == ["outline"], (
        "the ruled replacement-on-success, unchanged")
    assert s["failure"] is None, "a settled turn clears the arm's note"
    assert s["armedAfter"] is False


def test_the_arm_is_visible_to_the_control_between_the_presses(arm_results):
    """The house two-press idiom changes the CONTROL, so the second press says
    what it will do before it is pressed (`repo-selector.js`'s trash becomes
    "remove?"; this rail's retired Unload became "Discard and unload"). The arm
    is one authority — the dispatcher's — that the view reads."""
    assert arm_results["firstPress"]["armedForFirst"] is True


def test_a_fully_reviewed_set_sends_on_the_first_press(arm_results):
    """No nagging on reviewed sets: applied and rejected records are terminal,
    so there is nothing pending to discard and the arm never engages."""
    t = arm_results["terminalOnly"]
    assert sorted(t["reviewedStatuses"]) == ["applied", "rejected"]
    assert t["refused"] is False
    assert t["ok"] is True
    assert t["transportConsulted"] == 1


def test_a_conversation_with_no_proposals_sends_on_the_first_press(arm_results):
    n = arm_results["noProposals"]
    assert n["ok"] is True
    assert n["transportConsulted"] == 1


def test_a_stale_only_set_arms_too(arm_results):
    s = arm_results["stalePress"]
    assert s["refused"] is True
    assert s["transportConsulted"] == 0
    assert s["failure"]["error"] == "proposals_discard_armed"
    assert "outline" in s["failure"]["message"]


def test_reviewing_a_proposal_between_the_presses_re_arms_from_scratch(
        arm_results):
    """WHAT DISARMS THE ARM. The house arm (`repo-selector.js`) lives in the
    RENDER and is keyed by the row's own identity, so it cannot survive a change
    to what it is about. Send's control is never rebuilt, so the same rule is
    expressed as a match against the SENTENCE'S SUBJECT: the arm holds only
    while the pending target list is the one the refusal named. Rejecting one
    proposal between the presses changes that list, so the second press refuses
    again — with the narrowed sentence — and a third press sends."""
    r = arm_results["rearmed"]
    assert r["armedBeforeTheReview"] is True
    assert r["armedAfterTheReview"] is False
    second = arm_results["rearmedSecond"]
    assert second["refused"] is True
    assert second["transportConsulted"] == 0
    assert "outline" in second["failure"]["message"]
    assert "docs/other.md" not in second["failure"]["message"], (
        "the re-armed sentence names only what is still pending")
    third = arm_results["rearmedThird"]
    assert third["ok"] is True
    assert third["transportConsulted"] == 1


def test_an_emptied_pending_set_disarms(arm_results):
    """Nothing left to discard is nothing left to warn about."""
    assert arm_results["emptiedSet"]["armed"] is False


def test_the_arm_cannot_outlive_the_set_it_was_about(arm_results):
    """The token is a MATCH, not a latch — so the emptying has to clear it, or a
    later set that happens to name the same buffers would inherit a press nobody
    made about it and be discarded in silence: the filed defect again, one
    conversation later. Both observers clear it (the render-time predicate and
    the next press), so a dispatcher driven with no view at all is covered too."""
    a = arm_results["armDoesNotOutliveTheSet"]
    assert a["dispatchedWithNothingPending"] is True
    assert a["newSetKeys"] == ["outline"], "precondition: the same key came back"
    assert a["refusedForTheNewSet"] is True
    assert a["error"] == "proposals_discard_armed"
    assert a["transportConsulted"] == 1, (
        "only the nothing-pending press reached the transport")


def test_no_timer_and_no_blur_expiry_was_introduced():
    """The arm expires on STATE, never on a clock. This rail owns no clock (the
    model's purity rule forbids one and this view has never used one), and a
    wall-clock window would be a second authority on "is the arm still good"
    that nothing on the surface displays."""
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    for forbidden in ("setTimeout", "setInterval", "Date.now() -"):
        assert forbidden not in source, forbidden


# ---------------------------------------------------------------------------
# (a) again, on the MOUNTED rail: the two visible channels, and the control
# (b) rekey and (c) the document switch: the notice form
# ---------------------------------------------------------------------------

_RAIL_HARNESS = """
class Node {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = []; this.attributes = {}; this.listeners = {};
    this.className = ''; this._text = ''; this.hidden = false;
    this.disabled = false; this.value = '';
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  set textContent(value) { this.children = []; this._text = String(value); }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) {
    return Object.prototype.hasOwnProperty.call(this.attributes, name)
      ? this.attributes[name] : null;
  }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() { doc.activeElement = this; }
  walk() { return this.children.reduce((a, c) => a.concat(c.walk()), [this]); }
}
const doc = { createElement: (tag) => new Node(tag), activeElement: null };
const byClass = (root, cls) => root.walk().filter(
  (n) => String(n.className).split(' ').includes(cls));
const fire = async (node, type) => {
  for (const fn of node.listeners[type] || []) await fn({});
};

import { mountDoxBenchChatRail } from "./doxbench-chat.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const SESSION_KEY = { repository: "fixture-repo", ref: "session/abc",
                      tile_kind: "staged", tile_id: "ideation-governance" };
const LIVE = "d".repeat(64);
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" };
const bufferOf = (kind, path) => ({ kind, path, base_ref: "main",
  base_revision: "r1", base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: LIVE },
  hash_pending: false, content: "# " + kind, dirty: false });
const OBSERVED = { outline: LIVE, document: LIVE, "docs/other.md": LIVE };
const SUCCESS = { schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t-1", assistant_turn_id: "a-1", model_id: "model-a",
  observed_hashes: OBSERVED, assistant_prose: "here you go",
  proposals: [{ target: "outline", base_hash: LIVE,
                summary: "__SECRET_SUMMARY__", content: "__SECRET_CONTENT__" },
              { target: "docs/other.md", base_hash: LIVE,
                summary: "__SECRET_SUMMARY__", content: "__SECRET_CONTENT__" }] };

function mountRail(overrides) {
  const host = new Node("div"); host.ownerDocument = doc;
  let activeBuffer = "document";
  const editorState = () => ({ active_buffer: activeBuffer, buffers: {
    outline: bufferOf("outline", "docs/outline.md"),
    document: bufferOf("document", "docs/detail.md"),
    "docs/other.md": bufferOf("document", "docs/other.md") } });
  const rail = mountDoxBenchChatRail(host, Object.assign({
    scopeKey: KEY,
    transports: {
      catalog: async () => ({ schema_version: 1,
        kind: "workbench-model-catalog", models: [ENTRY] }),
      chatTurn: async () => ({ ok: true, status: 200, payload: SUCCESS }) },
    editorState,
    selectBuffer: async (key) => { activeBuffer = key; },
  }, overrides));
  return { host, rail, editorState };
}

// Drive one settled turn so a PENDING set exists, then type the next message.
async function propose(host) {
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "please propose"; await fire(composer, "input");
  await fire(byClass(host, "doxchat-send")[0], "click");
  composer.value = "next question"; await fire(composer, "input");
}

const read = (host, rail) => {
  const note = byClass(host, "doxchat-failure")[0];
  const announce = byClass(host, "doxchat-announce")[0];
  const send = byClass(host, "doxchat-send")[0];
  return {
    noteHidden: note.hidden,
    noteText: note.textContent,
    announced: announce.textContent,
    sendLabel: send.textContent,
    sendTitle: send.title,
    sendDisabled: send.disabled === true,
    transcriptTurns: rail.state().transcript.length,
    proposalKeys: Object.keys(rail.state().proposals).sort(),
    composer: rail.state().composer,
    error: rail.state().lastFailure && rail.state().lastFailure.error,
  };
};

// ---- (a) the mounted two-press arm: both visible channels, and the control --
{
  const { host, rail } = mountRail({});
  await rail.ready;
  await propose(host);
  out.beforeAnyPress = read(host, rail);
  await fire(byClass(host, "doxchat-send")[0], "click");
  out.armedPress = read(host, rail);
  await fire(byClass(host, "doxchat-send")[0], "click");
  out.sentPress = read(host, rail);
}

// ---- (b) REKEY: a Save moving the tile onto its session ref ----
{
  const { host, rail } = mountRail({});
  await rail.ready;
  await propose(host);
  const pendingBefore = Object.keys(rail.state().proposals).sort();
  rail.rekey(SESSION_KEY);
  out.rekey = Object.assign({ pendingBefore }, read(host, rail));
}

// ---- (b) negative: a rekey with a FULLY REVIEWED set says nothing ----
{
  const { host, rail } = mountRail({});
  await rail.ready;
  await propose(host);
  for (const card of byClass(host, "doxchat-card-reject")) {
    await fire(card, "click");
  }
  out.rekeyReviewedStatuses = Object.keys(rail.state().proposals).sort().map(
    (k) => rail.state().proposals[k].status);
  rail.rekey(SESSION_KEY);
  out.rekeyReviewed = read(host, rail);
}

// ---- (b) negative: a rekey to the SAME key clears nothing and says nothing --
{
  const { host, rail } = mountRail({});
  await rail.ready;
  await propose(host);
  rail.rekey(KEY);
  out.rekeySameKey = read(host, rail);
}

// ---- (c) the DOCUMENT SWITCH: the thread replaces the transcript ----
{
  const { host, rail } = mountRail({
    loadThread: async () => ({ turns: [
      { human: "an older question", assistant: "an older answer" }] }) });
  await rail.ready;
  await propose(host);
  const pendingBefore = Object.keys(rail.state().proposals).sort();
  const loaded = byClass(host, "doxchat-loaded")[0];
  loaded.value = "docs/other.md";
  await fire(loaded, "change");
  out.switch = Object.assign({ pendingBefore }, read(host, rail));
}

// ---- (c) negative: a switch with nothing pending says nothing ----
{
  const { host, rail } = mountRail({
    loadThread: async () => ({ turns: [] }) });
  await rail.ready;
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const loaded = byClass(host, "doxchat-loaded")[0];
  loaded.value = "docs/other.md";
  await fire(loaded, "change");
  out.switchNothingPending = read(host, rail);
}

process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def rail_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the mounted discard-notice probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-discard-rail")
    _stage(tmp_path)
    return _run(tmp_path, "discard-rail-harness.mjs",
                _RAIL_HARNESS.replace("__SECRET_SUMMARY__", SECRET_SUMMARY)
                             .replace("__SECRET_CONTENT__", SECRET_CONTENT))


def test_the_rail_says_nothing_until_send_is_actually_pressed(rail_results):
    """A pending set is not itself a problem — the operator is reviewing it. The
    arm is a property of the PRESS, so nothing is said, and the control reads
    Send, until a press asks to discard."""
    b = rail_results["beforeAnyPress"]
    assert b["noteHidden"] is True
    assert b["announced"] == ""
    assert b["sendLabel"] == "Send"
    assert b["proposalKeys"] == ["docs/other.md", "outline"]


def test_the_armed_press_renders_and_announces_the_fixed_sentence(rail_results):
    """The refusal lands on the two channels every other refusal on this rail
    uses — the VISIBLE failure note and the sr-only live region (the same pair
    T104 F5-5 gave the refused Apply) — and no new channel is invented."""
    a = rail_results["armedPress"]
    assert a["error"] == "proposals_discard_armed"
    assert a["noteHidden"] is False
    assert "outline" in a["noteText"]
    assert "docs/other.md" in a["noteText"]
    assert SECRET_SUMMARY not in a["noteText"]
    assert SECRET_CONTENT not in a["noteText"]
    assert a["announced"] == a["noteText"], (
        "a decision the operator has to make must be heard, not only shown")
    assert a["transcriptTurns"] == 2, "nothing was sent"
    assert a["proposalKeys"] == ["docs/other.md", "outline"]
    assert a["composer"] == "next question"
    assert a["sendDisabled"] is False, "the second press must be reachable"


def test_the_armed_send_control_says_what_the_second_press_does(rail_results):
    """The house idiom: the control itself changes so the second press is never
    a surprise (`repo-selector.js`'s trash reads "remove?"; this rail's retired
    Unload read "Discard and unload")."""
    a = rail_results["armedPress"]
    assert a["sendLabel"] == "Send and discard"
    assert a["sendTitle"] == a["noteText"], (
        "one sentence, one source — the hover text cannot drift from the note")


def test_the_second_press_sends_and_the_control_goes_back(rail_results):
    s = rail_results["sentPress"]
    assert s["transcriptTurns"] == 4, "the second press really dispatched"
    assert s["error"] is None
    assert s["noteHidden"] is True
    assert s["sendLabel"] == "Send"


def test_a_rekey_that_discards_a_pending_set_states_it(rail_results):
    """(b) REKEY — the NOTICE form. A Save landing on a session ref moves the
    tile's scope key, and FR-011 starts a fresh conversation on the new key:
    the proposals go with it. The rail cannot refuse that (the buffers have
    already moved, and a rail still naming the pre-session ref is the
    disagreement T104 F1 fixed), so the honest form is to SAY it on the clear."""
    r = rail_results["rekey"]
    assert r["pendingBefore"] == ["docs/other.md", "outline"]
    assert r["proposalKeys"] == [], "the fresh conversation, as ruled"
    assert r["error"] == "proposals_discarded_on_rekey"
    assert r["noteHidden"] is False
    assert "outline" in r["noteText"]
    assert "docs/other.md" in r["noteText"]
    assert SECRET_SUMMARY not in r["noteText"]
    assert r["announced"] == r["noteText"]


def test_a_rekey_with_a_fully_reviewed_set_says_nothing(rail_results):
    """Same no-nagging rule as the arm: reviewed records cost nothing to lose."""
    assert sorted(rail_results["rekeyReviewedStatuses"]) == \
        ["rejected", "rejected"]
    r = rail_results["rekeyReviewed"]
    assert r["error"] is None
    assert r["noteHidden"] is True
    assert r["announced"] == ""


def test_a_rekey_to_the_same_key_clears_nothing_and_says_nothing(rail_results):
    """`rekeyChatState` returns the identical state for an unchanged key, so
    there is no clear — and a notice about a clear that did not happen would be
    the mirror of the defect."""
    r = rail_results["rekeySameKey"]
    assert r["proposalKeys"] == ["docs/other.md", "outline"]
    assert r["error"] is None
    assert r["noteHidden"] is True
    assert r["announced"] == ""


def test_a_document_switch_that_discards_a_pending_set_states_it(rail_results):
    """(c) THE DOCUMENT SWITCH — the NOTICE form, for the same reason. By the
    time `adoptThreadTranscript` runs, the canvas has ALREADY moved its active
    buffer (the order contract: the selection moves first, the transcript
    follows) and the thread has already been read; refusing the clear here would
    leave document B on the canvas with document A's conversation, which is the
    defect the switch exists to close."""
    s = rail_results["switch"]
    assert s["pendingBefore"] == ["docs/other.md", "outline"]
    assert s["proposalKeys"] == [], "the thread switch's ruled clear"
    assert s["error"] == "proposals_discarded_on_switch"
    assert s["noteHidden"] is False
    assert "outline" in s["noteText"]
    assert SECRET_SUMMARY not in s["noteText"]
    assert s["announced"] == s["noteText"]
    assert s["transcriptTurns"] == 2, "the adopted thread, as ruled"


def test_a_document_switch_with_nothing_pending_says_nothing(rail_results):
    s = rail_results["switchNothingPending"]
    assert s["error"] is None
    assert s["noteHidden"] is True
    assert s["announced"] == ""
