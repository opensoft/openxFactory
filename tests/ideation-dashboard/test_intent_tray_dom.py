"""DOM behaviour of the HOSTED dispose tray and the intent-feed overlay
(add-ideation-intent-plane task 4.4; Brett Heap's rulings D-1 / Path A on
openxFactory #656).

Drives the REAL `dispose.js` and `intent-feed.js` under node against the same
minimal DOM shim the sibling probe uses. Nothing here reads a module's SOURCE:
every claim is made by mounting, clicking and inspecting the resulting tree and
the recorded requests, so a passing test means the behaviour exists rather than
that the code looks right.

The shim's `innerHTML` setter throws on any non-empty assignment, which is what
turns "a refusal renders as text" from a promise into a mechanical guarantee —
and a refusal reason on this plane is written by a DIFFERENT SERVICE (the intent
inbox) or by the apply lane, so it is the least trusted string on the page.

Pins I1-I9.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"

_DOM_SHIM = r"""
class Node {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = []; this.attributes = {}; this.listeners = {};
    this.className = ''; this._text = ''; this.disabled = false;
    this.value = ''; this.hidden = false; this.type = ''; this.title = '';
    this.dataset = {};
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  set textContent(value) { this.children = []; this._text = String(value); }
  set innerHTML(value) {
    if (String(value) !== '') throw new Error('only literal "" clears are allowed');
    this.children = []; this._text = '';
  }
  appendChild(child) { child.parent = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  insertBefore(child, ref) {
    const at = this.children.indexOf(ref);
    this.children.splice(at < 0 ? 0 : at, 0, child);
    return child;
  }
  remove() {
    if (!this.parent) return;
    const at = this.parent.children.indexOf(this);
    if (at >= 0) this.parent.children.splice(at, 1);
  }
  contains(node) {
    return this === node || this.children.some((c) => c.contains(node));
  }
  classList = {
    add: () => {}, remove: () => {}, toggle: () => {},
  };
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return this.attributes[name]; }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() {}
  querySelector(selector) {
    const cls = selector.replace(/^\./, '');
    return this.walk().find((n) => String(n.className).split(' ').includes(cls))
      || null;
  }
  walk() {
    return this.children.reduce((all, c) => all.concat(c.walk()), [this]);
  }
}
globalThis.document = {
  createElement: (tag) => new Node(tag),
  createTextNode: (text) => { const n = new Node('#text'); n._text = String(text);
    return n; },
  body: new Node('body'),
};
globalThis.window = { prompt: () => { throw new Error('unused on this plane'); } };
function byClass(root, cls) {
  return root.walk().filter((n) => String(n.className).split(' ').includes(cls));
}
async function click(node) {
  for (const fn of node.listeners.click || []) await fn({ stopPropagation() {} });
}
function panelText() {
  return globalThis.document.body.walk()
    .filter((n) => String(n.className).includes('refusalpanel-msg'))
    .map((n) => n.textContent);
}
function panelKinds() {
  return globalThis.document.body.walk()
    .filter((n) => String(n.className).includes('refusalpanel-kind'))
    .map((n) => n.textContent);
}
// A recording fetch. `routes` maps a path prefix to a response factory.
function recorder(routes) {
  const calls = [];
  const doFetch = async (url, init) => {
    calls.push({ url, method: (init && init.method) || 'GET',
                 body: init && init.body ? JSON.parse(init.body) : null });
    const path = String(url).split('?')[0];
    const make = routes[path];
    if (!make) throw new Error('unrouted fetch: ' + url);
    return make(url, init);
  };
  doFetch.calls = calls;
  return doFetch;
}
const json = (status, payload) => async () => ({
  status, ok: status < 400, json: async () => payload });
"""

_HARNESS = _DOM_SHIM + """
import { mountDisposeTray, GATE_DISPOSE_ROUTE } from './dispose.js';
import { mergeFeeds, readEmission, renderIntentChips, refusalLine,
         startIntentFeed, intentCapable, statesByTarget } from './intent-feed.js';

const results = {};
const REV = '0123456789abcdef0123456789abcdef01234567';
const POSSIBLE = { id: 'pos-derived-x' };

// ---- I1: the hosted click EMITS, and emits the kernel's shape --------------
{
  const fetcher = recorder({
    '/intents': json(202, { intent: { schema_version: 1, kind: 'gate-intent',
      actor: 'brett', verb: 'dispose-possible',
      target: { possible_id: POSSIBLE.id }, args: { outcome: 'accepted' },
      requested_at: '2026-09-06T00:00:00Z', snapshot_rev_seen: REV,
      status: 'pending', idempotency_key: 'k-1' } }),
  });
  const row = new Node('div');
  mountDisposeTray(row, POSSIBLE, {
    fetcher,
    intent: { snapshotRev: REV, rows: [], error: null },
  });
  await click(byClass(row, 'dispose-accepted')[0]);
  results.i1_routes = fetcher.calls.map((c) => c.url);
  results.i1_never_local = !fetcher.calls.some(
    (c) => String(c.url) === GATE_DISPOSE_ROUTE);
  results.i1_body = fetcher.calls[0].body;
  results.i1_method = fetcher.calls[0].method;
  results.i1_panel_kinds = panelKinds();
  results.i1_panel = panelText();
}

// ---- I2: a rejection carries reason + citation in ARGS, never in target ----
{
  const fetcher = recorder({
    '/intents': json(202, { intent: { status: 'pending', verb: 'dispose-possible',
      target: { possible_id: POSSIBLE.id }, idempotency_key: 'k-2' } }),
  });
  const row = new Node('div');
  mountDisposeTray(row, POSSIBLE, {
    fetcher,
    collect: () => ({ reason: 'not evidenced', citation: 'docs/x.md#3' }),
    intent: { snapshotRev: REV, rows: [], error: null },
  });
  await click(byClass(row, 'dispose-rejected')[0]);
  results.i2_body = fetcher.calls[0].body;
  results.i2_target_keys = Object.keys(fetcher.calls[0].body.target);
  results.i2_args_keys = Object.keys(fetcher.calls[0].body.args).sort();
}

// ---- I3: the LOCAL transport is untouched when no intent option is given ---
{
  const fetcher = recorder({
    '/actions/gate/dispose-possible': json(200, { ok: true, outcome: 'accepted' }),
  });
  const row = new Node('div');
  mountDisposeTray(row, { id: 'pos-local' }, { fetcher });
  await click(byClass(row, 'dispose-accepted')[0]);
  results.i3_routes = fetcher.calls.map((c) => c.url);
  results.i3_body = fetcher.calls[0].body;
  results.i3_panel_kinds = panelKinds();
  results.i3_no_chips = byClass(row, 'intentchips').length === 0;
}

// ---- I4: the inbox's own refusal reaches the panel, as TEXT ----------------
{
  const markup = '<img src=x onerror="boom()"> verb dispose-possible is ' +
    "outside auditor's allowlist";
  const fetcher = recorder({
    '/intents': json(403, { intent: { status: 'refused',
      refusal_reason: markup, verb: 'dispose-possible',
      target: { possible_id: POSSIBLE.id } } }),
  });
  const row = new Node('div');
  mountDisposeTray(row, POSSIBLE, {
    fetcher, intent: { snapshotRev: REV, rows: [], error: null } });
  await click(byClass(row, 'dispose-deferred')[0]);
  const texts = panelText();
  results.i4_kind = panelKinds()[0];
  results.i4_literal = texts[0].includes(markup);
  results.i4_no_element_from_message =
    globalThis.document.body.walk().every((n) => n.tagName !== 'IMG');
}

// ---- I5: chips render from the JOINED feeds; the corpus wins --------------
{
  const inbox = { intents: [
    // the ordinary path: the inbox NEVER learns the outcome, so this row
    // still reads "pending" after the lane already applied it
    { verb: 'dispose-possible', target: { possible_id: POSSIBLE.id },
      actor: 'brett', status: 'pending', idempotency_key: 'k-decided',
      requested_at: '2026-09-06T00:00:00Z', snapshot_rev_seen: REV },
    { verb: 'dispose-possible', target: { possible_id: 'pos-other' },
      actor: 'brett', status: 'pending', idempotency_key: 'k-inflight',
      requested_at: '2026-09-06T00:05:00Z', snapshot_rev_seen: REV },
  ] };
  const corpus = { intents: [
    { verb: 'dispose-possible', target: { possible_id: POSSIBLE.id },
      target_id: POSSIBLE.id, actor: 'brett', status: 'applied',
      idempotency_key: 'k-decided', requested_at: '2026-09-06T00:00:00Z',
      applied_at: '2026-09-06T00:02:00Z', snapshot_rev_seen: REV,
      applied_record: 'r.yaml', args: { outcome: 'accepted' } },
  ] };
  const merged = mergeFeeds(inbox.intents, corpus.intents);
  results.i5_states = merged.map((r) => r.state + ':' + r.targetId);
  results.i5_no_duplicate_for_decided =
    merged.filter((r) => r.targetId === POSSIBLE.id).length === 1;

  const row = new Node('div');
  mountDisposeTray(row, POSSIBLE, {
    fetcher: recorder({}),
    intent: { snapshotRev: REV, rows: merged, error: null } });
  const chips = byClass(row, 'intentchip');
  results.i5_chip_labels = chips.map((c) => c.textContent);
  results.i5_chip_states = chips.map((c) => c.dataset.intentState);
  results.i5_other_target_not_shown =
    chips.every((c) => c.dataset.intentTarget === POSSIBLE.id);
}

// ---- I6: a LANE refusal arrives through the feed and files ONE panel entry -
{
  const before = panelText().length;
  const laneRefusal = { verb: 'dispose-possible',
    target: { possible_id: POSSIBLE.id }, target_id: POSSIBLE.id,
    actor: 'brett', status: 'refused', idempotency_key: 'k-lane',
    requested_at: '2026-09-06T01:00:00Z', snapshot_rev_seen: REV,
    refusal_reason: '<b>stale</b> view: the target has advanced' };
  const fetcher = recorder({
    '/intents': json(200, { intents: [] }),
    '/committed-intents.json': json(200, { intents: [laneRefusal] }),
  });
  let ticks = 0;
  const feed = startIntentFeed({
    fetcher, actor: 'brett',
    timer: (fn) => { ticks += 1; if (ticks === 1) fn(); return ticks; },
    clearTimer: () => {},
    onRefusal: (rec) => { globalThis.__panelEntry('refused', refusalLine(rec)); },
  });
  await new Promise((r) => setTimeout(r, 20));
  await feed.refresh();                       // a SECOND poll, same refusal
  results.i6_rows = feed.rows().map((r) => r.state);
  results.i6_panel_added = panelText().length - before;
  results.i6_literal = panelText()[0].includes('<b>stale</b>');
  results.i6_no_element_from_reason =
    globalThis.document.body.walk().every((n) => n.tagName !== 'B');
  feed.stop();
}

// ---- I7: an unreachable feed is STATE, not a throw and not silence ---------
{
  const fetcher = recorder({
    '/intents': async () => { throw new Error('offline'); },
    '/committed-intents.json': json(200, { intents: [] }),
  });
  let waits = [];
  const feed = startIntentFeed({
    fetcher, actor: 'brett', intervalMs: 1000,
    timer: (fn, ms) => { waits.push(ms); if (waits.length === 1) fn(); return 1; },
    clearTimer: () => {},
  });
  await new Promise((r) => setTimeout(r, 20));
  results.i7_error = feed.error();
  await feed.refresh();
  results.i7_backoff_grows = waits.length >= 3 && waits[2] > waits[1];
  const box = new Node('span');
  renderIntentChips(box, POSSIBLE.id, [], feed.error());
  results.i7_chip = byClass(box, 'intentchip-error').map((c) => c.textContent);
  feed.stop();
}

// ---- I8: the inbox's response vocabulary, every branch --------------------
{
  results.i8 = {
    accepted: readEmission(202, { intent: { status: 'pending' } }).state,
    deduped: readEmission(200, { intent: { status: 'pending' },
                                 deduplicated: true }).state,
    refused: readEmission(403, { intent: { status: 'refused',
                                           refusal_reason: 'r' } }).state,
    dispatch_error: readEmission(502, { intent: { status: 'pending',
      dispatch_error: 'boom' }, error: 'boom' }).state,
    unauthenticated: readEmission(401, { error: 'missing ingress identity' }).state,
    rate_limited: readEmission(429, { error: 'rate limit exceeded' }).state,
    malformed: readEmission(400, { error: 'body must be a JSON object' }).state,
  };
  results.i8_messages_carry_the_servers_words =
    readEmission(401, { error: 'missing ingress identity' }).message ===
      'missing ingress identity';
  results.i8_capability = [intentCapable(null),
    intentCapable({ actions: { gate: true } }),
    intentCapable({ actions: { intent: true } })];
}

// ---- I9: the per-tile state index the wheel decorates from ----------------
{
  const rows = mergeFeeds(
    [{ verb: 'dispose-possible', target: { possible_id: 'pos-b' },
       actor: 'brett', status: 'pending', idempotency_key: 'k-b',
       requested_at: '2026-09-06T00:09:00Z', snapshot_rev_seen: REV }],
    [{ verb: 'dispose-possible', target: { possible_id: 'pos-a' },
       target_id: 'pos-a', actor: 'brett', status: 'refused',
       idempotency_key: 'k-a-old', requested_at: '2026-09-06T00:01:00Z',
       snapshot_rev_seen: REV, refusal_reason: 'stale' },
     { verb: 'dispose-possible', target: { possible_id: 'pos-a' },
       target_id: 'pos-a', actor: 'brett', status: 'applied',
       idempotency_key: 'k-a-new', requested_at: '2026-09-06T00:07:00Z',
       applied_at: '2026-09-06T00:08:00Z', snapshot_rev_seen: REV,
       applied_record: 'r.yaml' }]);
  const states = statesByTarget(rows);
  results.i9_index = { 'pos-a': states.get('pos-a'), 'pos-b': states.get('pos-b'),
                       'pos-none': states.get('pos-none') || null };
  results.i9_size = states.size;
}

console.log(JSON.stringify(results));
"""


def _run(tmp_path):
    """Drive the REAL dispose.js + intent-feed.js under node."""
    if NODE is None:
        pytest.skip("node not available for the DOM-driven intent-tray probe")
    views = tmp_path / "views"
    views.mkdir()
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    for name in ("dispose.js", "helpers.js", "intent-feed.js"):
        shutil.copy(WEB / "views" / name, views / name)
    harness = views / "intent-tray.js"
    # `panelEntry` is dispose.js's, reached through the module the tray itself
    # uses — so the probe files feed refusals into the SAME panel a click does.
    harness.write_text(
        "import { panelEntry } from './dispose.js';\n"
        "globalThis.__panelEntry = panelEntry;\n" + _HARNESS,
        encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


# ---- I1 -------------------------------------------------------------------

def test_i1_the_hosted_tray_emits_an_intent_and_never_executes(tmp_path):
    """Task 4.4's first half: on the hosted plane the verdict button submits a
    `gate-intent` to the inbox SAME-ORIGIN and never touches the executing gate
    route (which refuses off-loopback anyway, before it reads a body)."""
    r = _run(tmp_path)
    assert r["i1_routes"] == ["/intents"]
    assert r["i1_never_local"] is True
    assert r["i1_method"] == "POST"


def test_i1_the_emitted_body_is_the_kernel_request_shape(tmp_path):
    """The kernel's request half and nothing more: verb, the verb's ONE target
    key, `snapshot_rev_seen` (design D4), and args. NO actor — the inbox stamps
    it from the ingress and discards a body-claimed one — and no
    idempotency_key, which both servers recompute from validated fields."""
    body = _run(tmp_path)["i1_body"]
    assert body["verb"] == "dispose-possible"
    assert body["target"] == {"possible_id": "pos-derived-x"}
    assert body["snapshot_rev_seen"] == \
        "0123456789abcdef0123456789abcdef01234567"
    assert body["args"] == {"outcome": "accepted"}
    assert "actor" not in body
    assert "idempotency_key" not in body
    assert "possible_id" not in body


def test_i1_a_queued_intent_is_neither_applied_nor_refused_in_the_panel(tmp_path):
    """Design D1: the click IS the decision, but the ACT has not happened yet.
    Calling it "applied" would be a lie the human acts on."""
    r = _run(tmp_path)
    assert r["i1_panel_kinds"] == ["queued"]
    assert "dispose-possible accepted" in r["i1_panel"][0]


# ---- I2 -------------------------------------------------------------------

def test_i2_a_rejection_puts_reason_and_citation_in_args_not_in_target(tmp_path):
    """`intent_apply_lane.shape_error` refuses an intent whose `args` carry a
    target key ("the validated target is the only target"), so the tray must
    strip `possible_id` out of the verb arguments it collected locally."""
    r = _run(tmp_path)
    assert r["i2_target_keys"] == ["possible_id"]
    assert r["i2_args_keys"] == ["citation", "outcome", "reason"]
    assert r["i2_body"]["args"]["reason"] == "not evidenced"
    assert r["i2_body"]["args"]["citation"] == "docs/x.md#3"


# ---- I3 -------------------------------------------------------------------

def test_i3_the_local_transport_is_byte_for_byte_unchanged(tmp_path):
    """D5's other half: absent the intent option NOTHING about the loopback
    path moves — same route, same body, same "applied" panel entry, and no
    chips (the local plane has its own session overlay)."""
    r = _run(tmp_path)
    assert r["i3_routes"] == ["/actions/gate/dispose-possible"]
    assert r["i3_body"] == {"possible_id": "pos-local", "outcome": "accepted"}
    assert r["i3_panel_kinds"][0] == "applied"
    assert r["i3_no_chips"] is True


# ---- I4 -------------------------------------------------------------------

def test_i4_an_inbox_refusal_renders_in_the_panel_as_literal_text(tmp_path):
    """The inbox refuses an out-of-allowlist verb BEFORE dispatch and never
    commits it, so this response is the only place that refusal is ever seen —
    and its text is written by another service, which makes it the least
    trusted string on the page. The shim throws on any non-empty innerHTML, so
    this is mechanical."""
    r = _run(tmp_path)
    assert r["i4_kind"] == "refused"
    assert r["i4_literal"] is True
    assert r["i4_no_element_from_message"] is True


# ---- I5 -------------------------------------------------------------------

def test_i5_a_committed_outcome_wins_over_the_inboxs_stale_pending(tmp_path):
    """The inbox never updates its own store after a successful dispatch, so
    EVERY applied intent is still "pending" there. Concatenating the two feeds
    would show a permanent pending chip beside its own applied chip."""
    r = _run(tmp_path)
    assert r["i5_no_duplicate_for_decided"] is True
    assert "applied:pos-derived-x" in r["i5_states"]
    assert "pending:pos-other" in r["i5_states"]


def test_i5_the_chips_show_this_targets_lifecycle_only(tmp_path):
    r = _run(tmp_path)
    assert r["i5_chip_labels"] == ["applied"]
    assert r["i5_chip_states"] == ["applied"]
    assert r["i5_other_target_not_shown"] is True


# ---- I6 -------------------------------------------------------------------

def test_i6_a_lane_refusal_arrives_through_the_corpus_feed(tmp_path):
    """Ruling D-1: a lane refusal never reaches the inbox at all — it is
    COMMITTED, and the dashboard reads it from the corpus. It must still land
    in the same refusal panel a local refusal does."""
    r = _run(tmp_path)
    assert r["i6_rows"] == ["refused"]
    assert r["i6_literal"] is True
    assert r["i6_no_element_from_reason"] is True


def test_i6_a_refusal_is_filed_once_however_often_it_is_polled(tmp_path):
    """The panel is a log, not a live view. A committed refusal is returned by
    every subsequent poll, so a feed that files it each time would bury the
    page in one refusal."""
    assert _run(tmp_path)["i6_panel_added"] == 1


# ---- I7 -------------------------------------------------------------------

def test_i7_an_unreachable_feed_is_rendered_state_and_backs_off(tmp_path):
    """Errors are state, never a silent console line: the failure is readable
    from the controller, renders as its own chip (so an unknown state cannot
    be mistaken for "nothing happened"), and the poll interval grows instead
    of hammering a pod that is already unhappy."""
    r = _run(tmp_path)
    assert r["i7_error"]
    assert r["i7_backoff_grows"] is True
    assert r["i7_chip"] == ["feed unavailable"]


# ---- I8 -------------------------------------------------------------------

def test_i8_every_inbox_response_maps_to_one_state(tmp_path):
    """The inbox answers with seven distinct shapes. A 502 keeps `status:
    pending` and adds `dispatch_error`, which a status filter cannot tell from
    a healthy queue — so it gets its own state rather than reading as
    in-flight forever."""
    r = _run(tmp_path)
    assert r["i8"] == {
        "accepted": "pending",
        "deduped": "pending",
        "refused": "refused",
        "dispatch_error": "stalled",
        "unauthenticated": "error",
        "rate_limited": "error",
        "malformed": "error",
    }
    assert r["i8_messages_carry_the_servers_words"] is True


# ---- I9 -------------------------------------------------------------------

def test_i9_the_tile_index_takes_the_newest_decision_per_target(tmp_path):
    """The wheel decorates every tile on every animation frame, so the feed is
    reduced to a Map ONCE per update rather than scanned per tile. A target
    decided twice shows its NEWEST decision — the re-decision, not the refusal
    it followed."""
    r = _run(tmp_path)
    assert r["i9_index"] == {"pos-a": "applied", "pos-b": "pending",
                             "pos-none": None}
    assert r["i9_size"] == 2


def test_i8_the_capability_probe_reads_the_new_key_only(tmp_path):
    """`intentCapable` must not fall back to `gate`: the two transports are
    mutually exclusive and a tray that confused them would execute locally what
    it was asked to request."""
    assert _run(tmp_path)["i8_capability"] == [False, False, True]
