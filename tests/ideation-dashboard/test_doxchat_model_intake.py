"""add-doxchat-model-intake: the selector's intake affordance, the flow behind
it, the recorded approval that follows it, and the mid-turn re-mint the turn
record now carries.

FOUR LAYERS, because the change has four and each needs a different instrument:

  1. THE PURE MODEL — `doxbench-chat-model.js`, in node, with no DOM: the
     affordance's value, the default-selection rule, the refusal that keeps the
     affordance from ever being submitted as a model, and the browser's adoption
     of the re-mint fact.
  2. THE MOUNTED RAIL — the same minimal DOM stub `test_doxbench_chat_view.py`
     drives, because "first option" and "selected by default" are facts about
     rendered nodes and nothing else can prove them.
  3. THE ROUTES — a real ephemeral `ThreadingHTTPServer` over a real scratch
     corpus, with a REAL broker: a small program the test writes, invoked
     exactly as an operator's declaration would invoke it. THE GREP TEST
     (tasks.md 2.4) is the reason it is real rather than faked — a hand-off that
     never runs proves nothing about where a value went.
  4. THE CONTRACT — the additive `approve-model` enum member, its conditional,
     and the v2 record's `provider_retry`, asserted against the released bytes
     this repository ships.

WHAT IS DELIBERATELY NOT HERE: task 4.1's live-console proof. It needs a real
serve and a real browser and is recorded, unticked, in tasks.md with exactly
what was proven headlessly and what still owes a human at a screen.
"""

from __future__ import annotations

import hashlib
import http.client
import json
import os
import shutil
import stat
import subprocess
import sys
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest
import yaml

from conftest import (  # noqa: F401
    PINNED_REVISION, REPO_ROOT, FakeGit, serve_surface_source,
)
from session_fixtures import scratch_repo  # noqa: F401

from ideation_dashboard import doxbench_binding
from ideation_dashboard import doxbench_install
from ideation_dashboard import doxbench_intake
from ideation_dashboard import doxbench_provider
from ideation_dashboard import gate_console
from ideation_dashboard import serve as serve_mod
from ideation_dashboard.generator import generate_snapshot

NODE = shutil.which("node")
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
VIEWS = WEB / "views"
CHAT_MODEL_JS = VIEWS / "doxbench-chat-model.js"
CHAT_VIEW_JS = VIEWS / "doxbench-chat.js"
INTAKE_JS = VIEWS / "swb-model-intake.js"
SWB_JS = VIEWS / "staging-workbench.js"
SWB_MODEL_JS = VIEWS / "staging-workbench-model.js"
APP_JS = WEB / "app.js"

# The routes under test. Referenced at module scope deliberately: they must
# exist, so a checkout without them fails closed at collection rather than
# silently skipping every test below.
SURFACE_ROUTE = serve_mod.WORKBENCH_MODEL_INTAKE_ROUTE
INTAKE_ROUTE = serve_mod.ACTIONS_WORKBENCH_MODEL_INTAKE_ROUTE
APPROVAL_ROUTE = serve_mod.ACTIONS_WORKBENCH_MODEL_APPROVAL_ROUTE

#: The value a human types. A shape the credential validator's own denylist
#: would recognise (`sk-…`), so the grep test is searching for something that
#: looks exactly like the thing the rule exists to keep out of a corpus.
SUPPLIED_VALUE = "sk-INTAKEPROOF0123456789abcdefGHIJKLMNOP"


# ===========================================================================
# layer 1 — the pure model, in node
# ===========================================================================

_MODEL_HARNESS = """
import {
  createChatState, adoptCatalog, adoptIntakeOffer, selectModel,
  recordCatalogFailure, defaultSelectorValue, firstAvailableModelId,
  beginTurn, editComposer, settleTurnSuccess, canSend,
  INTAKE_OPTION_VALUE, INTAKE_OPTION_LABEL, PROVIDER_RETRY_NOTE,
} from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const entry = (id, available) => ({
  model_id: id, label: "Model " + id, provider_class: "on-tenant", available,
  input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" });
const envelope = (models) => ({ schema_version: 1,
  kind: "workbench-model-catalog", models });

out.affordance = { value: INTAKE_OPTION_VALUE, label: INTAKE_OPTION_LABEL };

// 1) EMPTY catalog + intake offered -> the affordance IS the default
const empty = adoptIntakeOffer(
  adoptCatalog(createChatState(KEY), envelope([])), true);
out.emptyOffered = { selector: defaultSelectorValue(empty),
                     canSend: canSend(empty),
                     selected: empty.selectedModelId };

// 2) EMPTY catalog + intake NOT offered -> exactly today's default
const emptyClosed = adoptCatalog(createChatState(KEY), envelope([]));
out.emptyClosed = { selector: defaultSelectorValue(emptyClosed) };

// 3) an AVAILABLE entry -> the default is a MODEL, never the affordance
const populated = adoptIntakeOffer(
  adoptCatalog(createChatState(KEY), envelope([entry("model-a", true)])), true);
out.populated = { selector: defaultSelectorValue(populated),
                  first: firstAvailableModelId(populated) };

// 4) a catalog that could not be READ -> no affordance default, whatever the
//    intake surface said
const failed = adoptIntakeOffer(
  recordCatalogFailure(createChatState(KEY), "unreadable"), true);
const stale = adoptIntakeOffer(
  recordCatalogFailure(createChatState(KEY), "console_required"), true);
out.failures = { unreadable: defaultSelectorValue(failed),
                 consoleRequired: defaultSelectorValue(stale) };

// 5) the affordance can NEVER become a selection
const chosen = selectModel(empty, INTAKE_OPTION_VALUE);
out.neverSelected = { same: chosen === empty,
                      selected: chosen.selectedModelId,
                      canSend: canSend(chosen) };

// 6) THE RE-MINT FACT, adopted from the released record and nowhere else
const armed = () => beginTurn(editComposer(
  selectModel(adoptCatalog(createChatState(KEY),
    envelope([entry("model-a", true)])), "model-a"), "ask"));
const success = (extra) => ({
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
  bound_buffer: "outline", observed_hashes: {},
  assistant_prose: "answered", proposals: [], ...extra });
out.retry = {
  absent: settleTurnSuccess(armed(), success({})).providerRetry,
  present: settleTurnSuccess(armed(), success({
    provider_retry: { retried: true, at_most_once: true,
                      audit_ref: "audit-1" } })).providerRetry,
  noRef: settleTurnSuccess(armed(), success({
    provider_retry: { retried: true, at_most_once: true } })).providerRetry,
  malformed: settleTurnSuccess(armed(), success({
    provider_retry: { retried: false } })).providerRetry,
  note: PROVIDER_RETRY_NOTE,
};
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def model_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the intake model probe")
    tmp_path = tmp_path_factory.mktemp("doxchat-intake-model")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "intake-model-harness.mjs"
    harness.write_text(_MODEL_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_affordance_carries_a_value_no_catalog_entry_could_collide_with(
        model_results):
    """Task 1.1. The affordance is NOT a catalog entry: it carries no model id,
    and its value belongs to no provider's namespace. That is what makes the
    second guard structural rather than careful — the server refuses a turn
    naming it through the SAME fixed absent-model refusal, with no
    intake-specific failure code, because the affordance is not a model and the
    existing refusal already states the truth."""
    value = model_results["affordance"]["value"]
    assert value.startswith("__") and value.endswith("__")
    assert model_results["affordance"]["label"]


def test_an_empty_catalog_defaults_to_the_affordance_and_send_stays_refused(
        model_results):
    """Tasks 1.2 and 1.3, together, because they are one decision and its
    accepted consequence (OQ-4, ruled 2026-08-21). Brett asked for the default
    explicitly — "if no current models loaded, that is the default" — and the
    consequence is that the selector shows a selected option that is not a
    model while the rail says no approved model is configured. Selecting intake
    is NOT selecting a model: no id is held, and the send control stays refused
    for exactly the reason it is refused today."""
    empty = model_results["emptyOffered"]
    assert empty["selector"] == model_results["affordance"]["value"]
    assert empty["selected"] is None
    assert empty["canSend"] is False


def test_with_no_flow_behind_it_the_selector_is_indistinguishable_from_today(
        model_results):
    """Task 1.6, the pure-model half. The ratified sequencing requirement says
    the affordance SHALL NOT be released ahead of the flow it opens: where the
    flow's dependencies are unmet the selector keeps its present behaviour
    UNCHANGED, rather than showing a disabled or explanatory option that would
    only restate the rail's sentence more weakly."""
    assert model_results["emptyClosed"]["selector"] == ""


def test_an_available_model_is_the_default_rather_than_the_affordance(
        model_results):
    """Task 1.2's other half. A human who already has an approved model is
    trying to chat, not to enrol — so the affordance stays FIRST but the
    default selection is a model, and choosing one never requires passing
    through the affordance."""
    populated = model_results["populated"]
    assert populated["first"] == "model-a"
    # The PURE model never selects for anybody — that act is the rail's, and it
    # is asserted on the mounted control below. What the pure rule guarantees is
    # the half that must hold everywhere: with something selectable the default
    # is NOT the affordance, so a human with an approved model never has to pass
    # through the enrolment option to reach it.
    assert populated["selector"] != model_results["affordance"]["value"]
    assert populated["selector"] == ""


def test_an_unreadable_catalog_never_defaults_to_the_affordance(model_results):
    """Task 1.4, the model half. An unreadable catalog and an empty one are
    different facts with different remedies — the dashboard already
    distinguishes them — and offering enrolment as the cure for a stale console
    token or an unreadable answer would send a human to buy a subscription to
    fix a reload."""
    assert model_results["failures"] == {"unreadable": "",
                                         "consoleRequired": ""}


def test_the_affordance_can_never_become_a_selection(model_results):
    """Task 1.5, the browser half: `selectModel` refuses any value the catalog
    does not vouch for, so the affordance leaves the state IDENTICAL. The route
    half is asserted over HTTP below."""
    never = model_results["neverSelected"]
    assert never["same"] is True
    assert never["selected"] is None
    assert never["canSend"] is False


def test_the_browser_adopts_the_remint_fact_only_from_the_released_block(
        model_results):
    """Task 3.6, the browser half. The record's block is OPTIONAL and present
    only when it happened; an absent, malformed or `retried !== true` block
    adopts as null, which is SILENCE rather than a claim in either direction —
    the same fail-closed reading the context posture already gets."""
    retry = model_results["retry"]
    assert retry["absent"] is None
    assert retry["malformed"] is None
    assert retry["present"] == {"retried": True, "audit_ref": "audit-1"}
    assert retry["noRef"] == {"retried": True}
    assert "extra provider call" in retry["note"]


# ===========================================================================
# layer 2 — the mounted rail, against the minimal DOM stub
# ===========================================================================

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
  focus() {}
  walk() { return this.children.reduce((a, c) => a.concat(c.walk()), [this]); }
}
const doc = { createElement: (tag) => new Node(tag), activeElement: null };
const byClass = (root, cls) => root.walk().filter(
  (n) => String(n.className).split(' ').includes(cls));
const fire = async (node, type) => {
  for (const fn of node.listeners[type] || []) await fn({});
};

import { mountDoxBenchChatRail } from "./doxbench-chat.mjs";
import { INTAKE_OPTION_VALUE } from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const ENTRY = { model_id: "model-a", label: "Approved", provider_class: "on-tenant",
  available: true, input_limit_bytes: 800000, output_limit_bytes: 900000,
  data_handling: "on-tenant" };
const bufferOf = (kind, path) => ({ kind, path, base_ref: "main",
  base_revision: "r1", base_hash: { algorithm: "sha256", hex: "c".repeat(64) },
  current_hash: { algorithm: "sha256", hex: "d".repeat(64) },
  hash_pending: false, content: "# " + kind, dirty: false });
const editorState = () => ({ active_buffer: "document", buffers: {
  outline: bufferOf("outline", "docs/outline.md"),
  document: bufferOf("document", "docs/detail.md") } });

async function mount(models, { offered, openIntake } = {}) {
  const host = new Node("div"); host.ownerDocument = doc;
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: async () => ({ schema_version: 1,
        kind: "workbench-model-catalog", models }),
      chatTurn: async () => null },
    openIntake,
    editorState });
  await rail.ready;
  if (offered !== undefined) rail.intakeOffer(offered);
  return { host, rail };
}

const optionsOf = (host) => byClass(host, "doxchat-model")[0]
  .children.map((o) => ({ value: o.value, text: o.textContent,
                          intake: String(o.className).includes("doxchat-model-intake") }));

// 1) offered + empty catalog: FIRST option, selected, selector usable
{
  const { host } = await mount([], { offered: true });
  const selector = byClass(host, "doxchat-model")[0];
  const send = byClass(host, "doxchat-send")[0];
  const note = byClass(host, "doxchat-unavailable")[0];
  out.emptyOffered = {
    options: optionsOf(host),
    selected: selector.value,
    selectorDisabled: selector.disabled === true,
    sendDisabled: send.disabled,
    noteText: note.textContent,
  };
}

// 2) NOT offered + empty catalog: byte-for-byte the pre-change rail
{
  const { host } = await mount([], { offered: false });
  const selector = byClass(host, "doxchat-model")[0];
  const send = byClass(host, "doxchat-send")[0];
  const note = byClass(host, "doxchat-unavailable")[0];
  out.emptyClosed = {
    options: optionsOf(host),
    selected: selector.value,
    selectorDisabled: selector.disabled === true,
    sendDisabled: send.disabled,
    noteText: note.textContent,
  };
}

// 3) offered + a model available: affordance still first, model selected
{
  const { host } = await mount([ENTRY], { offered: true });
  const selector = byClass(host, "doxchat-model")[0];
  out.populated = { options: optionsOf(host), selected: selector.value };
}

// 4) choosing the affordance OPENS THE FLOW and changes no selection
{
  let opened = 0;
  const { host, rail } = await mount([ENTRY], { offered: true,
                                                openIntake: () => { opened += 1; } });
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = INTAKE_OPTION_VALUE;
  await fire(selector, "change");
  out.chosen = { opened, selected: rail.state().selectedModelId,
                 snappedBack: selector.value };
}

// 5) the re-mint note is rendered from the record and from nothing else
{
  const host = new Node("div"); host.ownerDocument = doc;
  const SUCCESS = { schema_version: 1, kind: "workbench-chat-turn-v2-success",
    client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
    bound_buffer: "document",
    observed_hashes: { outline: "d".repeat(64), document: "d".repeat(64) },
    assistant_prose: "answered",
    provider_retry: { retried: true, at_most_once: true, audit_ref: "audit-1" },
    proposals: [] };
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: {
      catalog: async () => ({ schema_version: 1,
        kind: "workbench-model-catalog", models: [ENTRY] }),
      chatTurn: async () => ({ ok: true, status: 200, payload: SUCCESS }) },
    editorState });
  await rail.ready;
  const before = byClass(host, "doxchat-provider-retry")[0];
  const beforeState = { hidden: before.hidden, text: before.textContent };
  const selector = byClass(host, "doxchat-model")[0];
  selector.value = "model-a"; await fire(selector, "change");
  const composer = byClass(host, "doxchat-composer")[0];
  composer.value = "ask"; await fire(composer, "input");
  await fire(byClass(host, "doxchat-send")[0], "click");
  const after = byClass(host, "doxchat-provider-retry")[0];
  out.retryNote = { before: beforeState,
                    after: { hidden: after.hidden, text: after.textContent },
                    live: after.getAttribute("aria-live") };
}
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def rail_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the intake rail probe")
    tmp_path = tmp_path_factory.mktemp("doxchat-intake-rail")
    source = CHAT_VIEW_JS.read_text(encoding="utf-8").replace(
        './doxbench-chat-model.js', './doxbench-chat-model.mjs')
    (tmp_path / "doxbench-chat.mjs").write_text(source, encoding="utf-8")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "intake-rail-harness.mjs"
    harness.write_text(_RAIL_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_affordance_renders_first_and_selected_on_an_empty_catalog(
        rail_results):
    """Tasks 1.1 and 1.2 on the RENDERED control, which is the only place
    "first" and "default" mean anything. Brett's annotation, verbatim: "we need
    to have add model as the first option in the dropdown and if no current
    models loaded, that is the default"."""
    empty = rail_results["emptyOffered"]
    assert empty["options"][0]["intake"] is True
    assert empty["selected"] == empty["options"][0]["value"]
    # …and the control is USABLE, because it now carries the one thing there is
    # to do. A disabled selector holding the remedy would be the dead end the
    # sequencing requirement exists to prevent.
    assert empty["selectorDisabled"] is False


def test_the_rails_sentence_and_send_refusal_are_unchanged_by_the_affordance(
        rail_results):
    """Task 1.3, pinned as an ASSERTION rather than a reading. The sentence is
    compared against the module's own constant, so a future edit to either side
    fails here — and the send control stays refused for the reason it is
    refused today, because selecting intake is not selecting a model."""
    view = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert ('"chat is unavailable — no approved model is configured; both '
            'editors "\n  + "remain fully usable."') in view
    for case in ("emptyOffered", "emptyClosed"):
        rung = rail_results[case]
        assert rung["sendDisabled"] is True
        assert rung["noteText"] == (
            "chat is unavailable — no approved model is configured; both "
            "editors remain fully usable.")


def test_with_no_flow_the_rendered_selector_is_indistinguishable_from_today(
        rail_results):
    """Task 1.6's own words: "a test proves the indistinguishability". The
    rendered option list carries no intake option at all, the selected value is
    the placeholder's empty string, and the control is disabled exactly as it
    was before this change."""
    closed = rail_results["emptyClosed"]
    assert not any(option["intake"] for option in closed["options"])
    assert closed["selected"] == ""
    assert closed["selectorDisabled"] is True


def test_a_populated_catalog_keeps_the_affordance_first_and_a_model_selected(
        rail_results):
    populated = rail_results["populated"]
    assert populated["options"][0]["intake"] is True
    assert populated["selected"] == "model-a"


def test_choosing_the_affordance_opens_the_flow_and_selects_no_model(
        rail_results):
    """Task 1.1's behavioural half and §1's own sentence: "Selecting intake does
    not select a model". The control snaps back to the state's own default, so
    the human is never left looking at a selection the send gate does not
    agree with."""
    chosen = rail_results["chosen"]
    assert chosen["opened"] == 1
    # the rail's own default selection stands, untouched by the detour
    assert chosen["selected"] == "model-a"
    assert chosen["snappedBack"] == "model-a"


def test_the_remint_note_appears_only_after_a_record_that_carries_the_fact(
        rail_results):
    """Task 3.6's whole point: the fact reaches the human. Before the turn the
    live region is empty and hidden; after a record carrying the block it
    carries the fixed sentence on a polite live region, so a screen-reader user
    hears it too — a note only sighted readers get is half a disclosure."""
    note = rail_results["retryNote"]
    assert note["before"] == {"hidden": True, "text": ""}
    assert note["after"]["hidden"] is False
    assert "extra provider call" in note["after"]["text"]
    assert note["live"] == "polite"


# ===========================================================================
# layer 2b — the module boundaries the change must not cross
# ===========================================================================

def test_the_intake_transport_stays_out_of_the_fetch_bearing_set():
    """The front-matter's own budget clause: `app.js` gains no catalog call
    site, and "any intake route it does gain is budgeted by the transport-pin
    suite". It gains NONE, because the three intake routes are addressed by a
    sibling module in the `doFetch` shape `swb-create.js` and `swb-session.js`
    established — so the pinned cap on `app.js` and every pinned per-file count
    stay exactly where they were."""
    body = INTAKE_JS.read_text(encoding="utf-8")
    assert "const doFetch = fetcher || fetch;" in body
    assert "const doFetch = init.fetcher || fetch;" in body
    assert "doFetch(" in body
    assert "fetch(" not in body           # the case-sensitive bundle pin
    assert "XMLHttpRequest" not in body
    assert "import(" not in body
    # ONE write literal for TWO routes: the pin allows exactly one per
    # transport file, so both acts share one request helper.
    assert body.count('method: "POST"') == 1
    # routes come from the pure model, never from a literal here
    assert 'from "./staging-workbench-model.js"' in body
    for symbol in ("MODEL_INTAKE_SURFACE_ROUTE", "MODEL_INTAKE_ROUTE",
                   "MODEL_APPROVAL_ROUTE", "intakeQuery"):
        assert symbol in body, symbol
    model = SWB_MODEL_JS.read_text(encoding="utf-8")
    for route in ("/workbench/model-intake", "/actions/workbench/model-intake",
                  "/actions/workbench/model-approval"):
        assert route in model, f"{route} is not a model constant"
    view = SWB_JS.read_text(encoding="utf-8")
    assert "/workbench/model-intake" not in view
    assert "/actions/workbench/model-approval" not in view


def test_no_browser_module_names_the_authentication_kinds():
    """The absolute views clause, applied where it bites hardest. The intake
    flow offers two authentication kinds and NO browser module spells either
    one: the vocabulary is served, rendered by its label, and submitted
    verbatim. A page that hard-coded the kinds would be carrying exactly the
    spellings the boundary test sweeps for."""
    for path in sorted(WEB.rglob("*.js")):
        if "vendor" in path.relative_to(WEB).parts:
            continue
        source = path.read_text(encoding="utf-8")
        assert doxbench_binding.AUTH_KIND_API_KEY not in source, path.name
    # …and the server IS where they live, read from the record that owns them.
    kinds = [entry["kind"] for entry in doxbench_intake.auth_kind_disclosure()]
    assert kinds == list(doxbench_binding.AUTH_KINDS)
    assert [entry["accepts_secret"]
            for entry in doxbench_intake.auth_kind_disclosure()] == [True, False]


def test_the_editor_only_rung_gains_the_fact_and_the_failure_rungs_do_not():
    """Task 1.4, the ladder half. The `approvedModels === 0` rung KEEPS its
    sentence — character for character, asserted above through the rail — and
    gains the intake-offered FACT beside it. Neither `catalogFailure` rung
    offers it, because a bug's remedy is not a subscription."""
    model = SWB_MODEL_JS.read_text(encoding="utf-8")
    editor_only = model.index('kind: "editor-only"')
    assert "intakeOffered: facts.intakeOffered === true" in model[
        editor_only - 400:editor_only + 400]
    for rung in ('kind: "console-token-stale"', 'kind: "catalog-unreadable"',
                 'kind: "hosted-hidden"', 'kind: "gate-off"'):
        start = model.index(rung)
        assert "intakeOffered" not in model[start:start + 400], rung


# ===========================================================================
# layer 3 — the routes, over real HTTP, against a real broker
# ===========================================================================

#: The broker program the test writes and an operator's declaration names. It
#: speaks the DECLARED CLI surface (`docs/broker-cli.md`), reads standard input
#: to EOF as the whole of the secret, and refuses an `oauth` intake BEFORE
#: reading anything — which is exactly what the real `openprofiler-broker`
#: declares it does, and what makes the honest oauth posture testable.
_BROKER_PROGRAM = '''#!/usr/bin/env python3
import json
import sys

RECORD = {record!r}
CALLS = {calls!r}

def main():
    args = sys.argv[1:]
    # WAS THIS PROCESS STARTED AT ALL. Written before anything is parsed and
    # before standard input is touched, because "the broker never took custody"
    # is a claim about the SPAWN, not about what the spawn went on to store — an
    # oauth intake reaches this program and stores nothing, and a test that read
    # only RECORD could not tell that apart from never running.
    with open(CALLS, "a", encoding="utf-8") as handle:
        handle.write((args[0] if args else "<no-operation>") + "\\n")
    if not args:
        return 2
    operation = args[0]
    flags = {{}}
    rest = args[1:]
    for index in range(0, len(rest) - 1, 2):
        flags[rest[index]] = rest[index + 1]
    if operation == "intake":
        if flags.get("--auth-kind") == "oauth":
            # Refused BEFORE standard input is read, on purpose: a grant never
            # enters a process that cannot store it correctly.
            return 3
        supplied = sys.stdin.read()
        with open(RECORD, "w", encoding="utf-8") as handle:
            handle.write(supplied)
        sys.stdout.write(json.dumps({{
            "schema_version": 1,
            "kind": "openprofiler_broker_intake",
            "reference": "ref-" + str(len(supplied)),
            "binding": flags.get("--binding"),
            "provider": flags.get("--provider"),
            "auth_kind": flags.get("--auth-kind"),
            "label": flags.get("--label"),
            "created_at": "2026-08-26T18:00:00Z",
            "max_lifetime_seconds": 900,
            "issued_by": "broker",
            "approved_by": flags.get("--approved-by"),
            "audit_ref": "audit-openprofiler-1",
        }}))
        return 0
    return 4

sys.exit(main())
'''


def _broker_calls(tmp_path: Path) -> Path:
    """Where the fake broker logs THAT it was started, one line per spawn.

    Separate from the received-value record on purpose: the value record stays
    the evidence of custody, and this is the evidence of INVOCATION. A refusal
    that must never reach the broker at all is a claim only this file can
    settle — its absence means no child was spawned."""
    return tmp_path / "broker-calls.txt"


def _write_broker(tmp_path: Path) -> tuple[Path, Path]:
    """The broker program plus the file it records what it received into.

    The record path is baked INTO the program rather than passed in the
    environment, because `doxbench_provider` scrubs the child's environment down
    to a five-name allowlist — which is the point of that allowlist, and a test
    that widened it would be testing something else. `_broker_calls(tmp_path)`
    is baked in for the same reason and answers a different question."""
    record = tmp_path / "broker-received.txt"
    program = tmp_path / "fake-openprofiler-broker"
    program.write_text(
        _BROKER_PROGRAM.format(record=str(record),
                               calls=str(_broker_calls(tmp_path))),
        encoding="utf-8")
    program.chmod(program.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP)
    return program, record


def _declare_broker(checkout: Path, program: Path) -> None:
    store = doxbench_intake.DeclarationStore(
        doxbench_intake.declarations_path(checkout))
    store.declare_broker(doxbench_intake.BrokerDeclaration(
        argv=(sys.executable, str(program))))


@contextmanager
def _serving(checkout: Path, tmp_path: Path, *, actor="brett"):
    snap_path = tmp_path / "snapshot.json"
    snapshot = generate_snapshot(checkout, "fixture-repo",
                                 source_revision=PINNED_REVISION, git=FakeGit())
    snap_path.write_text(json.dumps(snapshot), encoding="utf-8")
    httpd = serve_mod.build_server(WEB, snap_path, checkout,
                                   head=PINNED_REVISION, actor=actor)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield host, port
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _request(host, port, method, path, *, body=None, headers=None):
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request(method, path, body=body, headers=headers or {})
    resp = conn.getresponse()
    raw = resp.read()
    try:
        payload = json.loads(raw.decode("utf-8") or "{}")
    except ValueError:
        payload = None
    conn.close()
    return resp.status, payload, raw


def _request_without_content_length(host, port, method, path, *, headers=None):
    """A request that declares NO `Content-Length` and sends no body.

    `http.client.request(body=None)` would helpfully declare `Content-Length: 0`
    for a POST, which is a different case from the header being absent. Driving
    `putrequest`/`putheader`/`endheaders` by hand is the only way to send the
    absent one, and the route's reading of an absent declaration as zero is
    exactly what this exercises."""
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.putrequest(method, path, skip_accept_encoding=True)
    for name, value in (headers or {}).items():
        conn.putheader(name, value)
    conn.endheaders()
    resp = conn.getresponse()
    raw = resp.read()
    try:
        payload = json.loads(raw.decode("utf-8") or "{}")
    except ValueError:
        payload = None
    conn.close()
    return resp.status, payload, raw


def _console(host, port):
    status, payload, _raw = _request(host, port, "GET", "/capabilities")
    assert status == 200, payload
    return payload["console_token"]


def _intake_query(**facts) -> str:
    from urllib.parse import urlencode
    return INTAKE_ROUTE + "?" + urlencode(facts)


_FACTS = dict(binding="authoring-model", label="Authoring model",
              provider="demo-provider", endpoint="https://provider.invalid/v1",
              dialect=doxbench_binding.DIALECT_XFACTORY_PROMPT_V1)


def _enrol(host, port, token, *, kind, value=SUPPLIED_VALUE, **overrides):
    facts = dict(_FACTS, kind=kind)
    facts.update(overrides)
    return _request(host, port, "POST", _intake_query(**facts),
                    body=value.encode("utf-8"),
                    headers={"Content-Type": "text/plain; charset=utf-8",
                             "X-XF-Console-Token": token,
                             "Content-Length": str(len(value.encode("utf-8")))})


def test_the_surface_refuses_when_no_broker_is_declared(scratch_repo, tmp_path):
    """Task 2.1's refusal half, and the requirement's own words: an intake flow
    SHALL refuse rather than degrade when no broker is declared, and SHALL
    present no field that would accept a secret. The surface answers
    `offered: false` with the stated reason and discloses NO authentication
    kinds at all — so the page has nothing to build a field from."""
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        status, payload, _raw = _request(
            host, port, "GET", SURFACE_ROUTE,
            headers={"X-XF-Console-Token": token})
    assert status == 200, payload
    assert payload["offered"] is False
    assert payload["auth_kinds"] == []
    assert payload["dialects"] == []
    assert payload["reason"] == doxbench_intake.NO_BROKER_NOTICE


def test_a_declared_broker_offers_both_kinds_and_the_dialect_vocabulary(
        scratch_repo, tmp_path):
    """Task 2.1. Both authentication kinds a human may hold are offered, and
    only one of them declares that it accepts a supplied value — which is the
    fact a renderer actually needs, stated on the server beside the vocabulary
    rather than inferred in a browser from a kind's name."""
    program, _record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        status, payload, _raw = _request(
            host, port, "GET", SURFACE_ROUTE,
            headers={"X-XF-Console-Token": token})
    assert status == 200, payload
    assert payload["offered"] is True
    assert [k["kind"] for k in payload["auth_kinds"]] == list(
        doxbench_binding.AUTH_KINDS)
    assert payload["dialects"] == list(doxbench_binding.DIALECTS)
    assert "reason" not in payload


def test_an_agent_invocation_is_refused_and_reported_on_every_intake_route(
        scratch_repo, tmp_path, capfd):
    """Tasks 2.1 and 3.2's shared boundary: agent invocation refuses, exactly as
    every other gate action refuses one, and it is REPORTED — FR-019 says reject
    AND report, and an agent that reached for the credential surface is exactly
    the event an operator should be able to find afterwards."""
    program, _record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        # no console token presented at all — the pre-identity refusal
        surface = _request(host, port, "GET", SURFACE_ROUTE,
                           headers={"Content-Type": "application/json"})
        intake = _request(host, port, "POST",
                          _intake_query(**dict(_FACTS, kind="api_key")),
                          body=b"x",
                          headers={"Content-Type": "application/json",
                                   "Content-Length": "1"})
        approval = _request(host, port, "POST", APPROVAL_ROUTE,
                            body=json.dumps({"binding": "authoring-model"}),
                            headers={"Content-Type": "application/json"})
    expected = serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    for status, payload, _raw in (surface, intake, approval):
        assert status == expected, payload
        assert payload["error"] == serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED
    assert "agent_invocation refused" in capfd.readouterr().err


def test_a_completed_intake_keeps_only_the_reference_and_declares_it_pending(
        scratch_repo, tmp_path):
    """Tasks 2.2 and 3.1. The value goes to the broker and only the returned
    reference is retained, in the binding shape `credential-contracts` already
    owns — and completing the flow yields a PENDING declaration that contributes
    NO available catalog entry, because supplying a payment credential is not
    the act of approving a provider for governed work."""
    program, record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        status, payload, _raw = _enrol(host, port, token, kind="api_key")
    assert status == 200, payload
    # THE BROKER REALLY RECEIVED IT, and received it whole and alone: the
    # declared stdin contract is that `intake` reads to EOF and treats all of it
    # as the secret, so a framing byte of this dashboard's invention would show
    # up here.
    assert record.read_text(encoding="utf-8") == SUPPLIED_VALUE
    binding = payload["binding"]
    assert set(binding) == {"kind", *doxbench_binding.BINDING_FIELDS,
                            "credential_custody"}
    assert binding["credential_ref"] == "ref-" + str(len(SUPPLIED_VALUE))
    assert binding["credential_custody"] == doxbench_binding.CUSTODY_NOTICE
    declaration = payload["declaration"]
    assert declaration["status"] == doxbench_intake.STATUS_PENDING
    assert declaration["availability"] == doxbench_intake.PENDING_NOTICE
    # …and the PENDING declaration contributes no available entry: the one seam
    # where availability is decided passes over it exactly as if it were not
    # declared at all.
    factory = doxbench_install.declared_model_port_factory(
        tmp_path / "sessions", checkout_root=scratch_repo.root,
        spawn=lambda *a, **k: None)
    port_obj = factory()
    assert not isinstance(port_obj, object.__class__)  # a real port, not a class
    assert all(entry.model_id != "authoring-model"
               for entry in port_obj.catalog().entries)


def test_the_supplied_value_is_found_nowhere_afterwards(scratch_repo, tmp_path,
                                                        capfd):
    """TASK 2.4 — THE GREP TEST, and the test that makes the requirement real.

    After a completed intake the whole checkout, every response body, and every
    line this process wrote to its own output are searched for the supplied
    value. It is found NOWHERE. That is structural rather than careful: the
    facts ride the query string and the body is the credential and nothing else,
    streamed from the connection into the broker's standard input through a
    function whose signature takes an open handle and refuses to take a value.

    The BROKER's own record is excluded from the sweep, and excluding it is the
    point rather than a loophole: the whole design is that the value ends up in
    exactly one custody, and a sweep that found it nowhere at all would be
    proving the hand-off never happened."""
    program, record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        status, payload, raw = _enrol(host, port, token, kind="api_key")
        assert status == 200, payload
        approved = _request(host, port, "POST", APPROVAL_ROUTE,
                            body=json.dumps({"binding": "authoring-model"}),
                            headers={"Content-Type": "application/json",
                                     "X-XF-Console-Token": token})
    assert approved[0] == 200, approved[1]
    assert record.read_text(encoding="utf-8") == SUPPLIED_VALUE

    offenders = []
    for path in sorted(scratch_repo.root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if SUPPLIED_VALUE in text:
            offenders.append(str(path))
    assert not offenders, offenders
    assert SUPPLIED_VALUE.encode("utf-8") not in raw
    assert SUPPLIED_VALUE.encode("utf-8") not in approved[2]
    captured = capfd.readouterr()
    assert SUPPLIED_VALUE not in captured.out
    assert SUPPLIED_VALUE not in captured.err


def test_the_oauth_kind_surfaces_the_brokers_refusal_and_fakes_no_dance(
        scratch_repo, tmp_path):
    """Task 2.3, HONESTLY. For the OAuth kind the dashboard must not be the
    party that receives the provider's tokens: it hands the human to the
    broker's OWN authorization flow (OQ-2, ruled 2026-08-21) and receives back
    a reference. A broker that has not declared that flow refuses — before
    reading standard input at all — and this console says so in its own fixed
    sentence rather than inventing a redirect, presenting a field for token
    material, or simulating an authorization it never performed.

    Nothing is stored: no binding, no declaration."""
    program, record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        status, payload, _raw = _enrol(host, port, token, kind="oauth",
                                       value="")
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_INTAKE_REFUSED), payload
    assert payload["reason"] == doxbench_intake.OAUTH_UNAVAILABLE_NOTICE
    assert not record.exists(), "an oauth intake sent the broker no value"
    # …but it DID reach the broker, with the empty source that kind is supposed
    # to send. The api_key emptiness refusal added for PR #401's review must
    # never widen onto this path: the oauth flow's whole point is that the
    # broker, not this dashboard, decides whether an authorization can be
    # opened, and it cannot decide about a request this route never forwards.
    assert _broker_calls(tmp_path).read_text(encoding="utf-8").split() == \
        ["intake"], "the oauth kind reaches the broker with an empty source"
    store = doxbench_intake.DeclarationStore(
        doxbench_intake.declarations_path(scratch_repo.root))
    assert store.list() == ()
    bindings = doxbench_binding.BindingStore(
        doxbench_binding.bindings_path(scratch_repo.root))
    assert bindings.list() == ()


def test_the_approval_writes_a_gate_record_before_the_model_becomes_available(
        scratch_repo, tmp_path):
    """Task 3.2. Approval is an explicit act by the resolved local human actor,
    recorded the way this dashboard records every other governed act: a gate
    action naming the model declaration it approved, carrying who issued, who
    approved, when it expires, and the audit reference — the accountability
    `credential-contracts` already demands of an issued grant."""
    program, _record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        assert _enrol(host, port, token, kind="api_key")[0] == 200
        status, payload, _raw = _request(
            host, port, "POST", APPROVAL_ROUTE,
            body=json.dumps({"binding": "authoring-model"}),
            headers={"Content-Type": "application/json",
                     "X-XF-Console-Token": token})
    assert status == 200, payload
    records = sorted((scratch_repo.root / gate_console.DEFAULT_RECORDS_DIR
                      / "authoring-model").glob("approve-model-*.gate-action.yaml"))
    assert len(records) == 1, records
    record = yaml.safe_load(records[0].read_text(encoding="utf-8"))
    assert record["action"] == doxbench_intake.GATE_ACTION_APPROVE_MODEL
    assert record["target"]["model_declaration"] == "authoring-model"
    approval = record["model_approval"]
    assert set(approval) == set(doxbench_intake.APPROVAL_FIELDS)
    assert approval["install_posture"] == doxbench_intake.POSTURE_SINGLE_OPERATOR
    assert approval["approved_by"] == "brett"
    assert approval["audit_ref"]
    # the RELEASED schema accepts it — the same validator the console ran
    gate_console.validate_gate_action_record(record)
    # …and only NOW does the model become available.
    factory = doxbench_install.declared_model_port_factory(
        tmp_path / "sessions", checkout_root=scratch_repo.root)
    entries = factory().catalog().entries
    assert [entry.model_id for entry in entries] == ["authoring-model"]
    assert entries[0].available is True


def test_a_second_approval_and_an_unknown_declaration_both_refuse(
        scratch_repo, tmp_path):
    """Task 3.2's edges. A repeated approval would record an act with no effect,
    and an approval of something nobody declared would record an authority over
    nothing. Both refuse with a STATED reason and write nothing."""
    program, _record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        assert _enrol(host, port, token, kind="api_key")[0] == 200
        headers = {"Content-Type": "application/json",
                   "X-XF-Console-Token": token}
        first = _request(host, port, "POST", APPROVAL_ROUTE,
                         body=json.dumps({"binding": "authoring-model"}),
                         headers=headers)
        second = _request(host, port, "POST", APPROVAL_ROUTE,
                          body=json.dumps({"binding": "authoring-model"}),
                          headers=headers)
        unknown = _request(host, port, "POST", APPROVAL_ROUTE,
                           body=json.dumps({"binding": "nobody-declared-this"}),
                           headers=headers)
    assert first[0] == 200
    refused = serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_APPROVAL_REFUSED)
    for status, payload, _raw in (second, unknown):
        assert status == refused, payload
        assert payload["error"] == serve_mod.DOXBENCH_ERR_APPROVAL_REFUSED
        assert payload["reason"]
    records = sorted((scratch_repo.root / gate_console.DEFAULT_RECORDS_DIR
                      / "authoring-model").glob("*.gate-action.yaml"))
    assert len(records) == 1


def test_an_intake_request_declaring_an_unknown_fact_refuses_the_whole_request(
        scratch_repo, tmp_path):
    """The closed query vocabulary. A parameter this route does not name refuses
    rather than being ignored — a caller that believed it had declared something
    must never have it silently dropped, and a credential must never be accepted
    as a query parameter under any spelling."""
    program, record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        status, payload, _raw = _enrol(host, port, token, kind="api_key",
                                       **{"secret": "smuggled"})
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_INVALID_INTAKE_REQUEST), payload
    assert not record.exists()


def test_an_empty_api_key_body_refuses_before_the_broker_takes_custody(
        scratch_repo, tmp_path):
    """PR #401's review, note 2. The api_key kind's whole BODY is the secret, so
    a request declaring `Content-Length: 0` has declared that it is enrolling
    nothing — and a broker asked to take custody of nothing answers with a
    reference naming nothing, after which the binding and the PENDING
    declaration this route writes would both assert a credential that does not
    exist. The records are all anyone can read afterwards, so a refusal is the
    only honest outcome.

    It is the EXISTING invalid-request refusal, not a new code: an empty body is
    a malformed request, exactly as an unknown query fact and an over-bound
    length are, and §1's own rule is that this flow invents no failure code it
    does not need. The broker child is never spawned, which is the half the
    calls log — not the value record — is able to prove: an oauth intake reaches
    the broker and stores nothing either, and only the spawn tells them apart.
    """
    program, record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        empty = _enrol(host, port, token, kind="api_key", value="")
        # …and with NO `Content-Length` at all, which this route reads as zero.
        # The secret is streamed, so the length is never counted by buffering
        # the body — the declaration is the whole of what is checked.
        undeclared = _request_without_content_length(
            host, port, "POST",
            _intake_query(**dict(_FACTS, kind="api_key")),
            headers={"Content-Type": "text/plain; charset=utf-8",
                     "X-XF-Console-Token": token})
    expected = serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_INVALID_INTAKE_REQUEST)
    for status, payload, _raw in (empty, undeclared):
        assert status == expected, payload
        assert payload["error"] == serve_mod.DOXBENCH_ERR_INVALID_INTAKE_REQUEST
    assert not _broker_calls(tmp_path).exists(), \
        "the broker child must never be spawned for an empty credential"
    assert not record.exists()
    # NOTHING WAS WRITTEN EITHER: no binding claiming a reference, no PENDING
    # declaration claiming a model is awaiting approval.
    assert doxbench_intake.DeclarationStore(
        doxbench_intake.declarations_path(scratch_repo.root)).list() == ()
    assert doxbench_binding.BindingStore(
        doxbench_binding.bindings_path(scratch_repo.root)).list() == ()


def test_a_turn_naming_the_affordance_refuses_through_the_existing_refusal(
        scratch_repo, tmp_path):
    """Task 1.5, the ROUTE half, and §1's own scenario: a chat request naming
    the intake affordance's selector value refuses with the SAME fixed refusal
    an absent model id produces, before any provider call — and NO
    intake-specific failure code exists, because the affordance is not a model
    and the existing refusal already states the truth.

    Asserted structurally rather than over the wire: the affordance's value is
    not a catalog entry on ANY install, so `selectable_entry_for` cannot vouch
    for it and the route's existing unknown-model arm is the only one it can
    reach. The proof that matters is the ABSENCE — no new code names it."""
    value = "__doxchat_intake__"
    model_js = CHAT_MODEL_JS.read_text(encoding="utf-8")
    assert f'INTAKE_OPTION_VALUE = "{value}"' in model_js
    # THE WHOLE SERVE SURFACE (§ 2.4 PR 2 of 4): this is an ABSENCE, and an
    # absence asserted over one of four files is an absence with three holes
    # in it — the turn route the claim is about now lives in another of them.
    serve_source = serve_surface_source()
    assert value not in serve_source, (
        "the server must not know the affordance's value: a turn naming it "
        "refuses through the EXISTING absent-model refusal, and a route that "
        "recognised it would be a new failure code by another name")
    for code in serve_mod.DOXBENCH_ERROR_CATALOG:
        assert "intake" not in code or code in (
            serve_mod.DOXBENCH_ERR_INTAKE_REFUSED,
            serve_mod.DOXBENCH_ERR_INVALID_INTAKE_REQUEST), code


# ===========================================================================
# layer 3b — the records themselves
# ===========================================================================

def test_the_closed_catalog_entry_does_not_widen(scratch_repo, tmp_path):
    """Task 3.5, asserted rather than asserted-about. Proposed-versus-approved
    is a SERVER-SIDE distinction and a pending declaration is simply not in the
    catalog, so the public entry's shape is untouched — widening it is a
    separate, governed additive release and this change does not spend one.

    THE REFERENT MOVES, THE CLAIM DOES NOT. This docstring said "seven-field"
    and named Phase B task 11.7 as the owed widening. That widening landed
    (contract-v1.38's routing declaration), and a second followed
    (contract-v2.2's `modalities`), so the count is no longer the shape and the
    named successor is no longer pending. What this test asserts is unchanged
    and still passes byte-for-byte: an APPROVED plain entry projects exactly
    `PUBLIC_ENTRY_FIELDS`, because each optional group is emitted only by an
    entry that declares it."""
    from ideation_dashboard.doxbench_model import (
        PUBLIC_ENTRY_FIELDS, catalog_wire_envelope)
    program, _record = _write_broker(tmp_path)
    _declare_broker(scratch_repo.root, program)
    with _serving(scratch_repo.root, tmp_path) as (host, port):
        token = _console(host, port)
        assert _enrol(host, port, token, kind="api_key")[0] == 200
        status, payload, _raw = _request(
            host, port, "POST", APPROVAL_ROUTE,
            body=json.dumps({"binding": "authoring-model"}),
            headers={"Content-Type": "application/json",
                     "X-XF-Console-Token": token})
    assert status == 200, payload
    # Read through the SAME wire projection the catalog route serves, rather
    # than over HTTP: the route additionally resolves the RELEASED validators
    # from a pinned openxFactory checkout, which is a different fact and has its
    # own suite. What task 3.5 is about is the SHAPE, and this is the shape.
    factory = doxbench_install.declared_model_port_factory(
        tmp_path / "sessions", checkout_root=scratch_repo.root)
    envelope = catalog_wire_envelope(factory().catalog())
    assert envelope["models"], "the approved model is in the catalog"
    for entry in envelope["models"]:
        assert set(entry) == set(PUBLIC_ENTRY_FIELDS)
    assert len(PUBLIC_ENTRY_FIELDS) == 7


def test_a_declaration_carries_no_field_a_credential_could_occupy():
    """The structural half of §2's retention rule. The declaration is a frozen,
    slotted dataclass over a CLOSED field list, so an extra keyword is a
    `TypeError` at construction and an extra attribute is an `AttributeError` at
    assignment — the same enforcement the binding record keeps, and for the same
    reason: a convention can be forgotten and a validator can be softened."""
    declaration = doxbench_intake.ModelDeclaration(
        binding_id="m", status=doxbench_intake.STATUS_PENDING,
        install_posture=doxbench_intake.POSTURE_SINGLE_OPERATOR,
        proposed_by="brett", proposed_at="2026-08-26T18:00:00Z")
    with pytest.raises(TypeError):
        doxbench_intake.ModelDeclaration(
            binding_id="m", status=doxbench_intake.STATUS_PENDING,
            install_posture=doxbench_intake.POSTURE_SINGLE_OPERATOR,
            proposed_by="brett", proposed_at="2026-08-26T18:00:00Z",
            credential="sk-nope")
    # A frozen, SLOTTED dataclass refuses the assignment; which exception the
    # interpreter reaches for is a CPython detail, and the guarantee under test
    # is that the assignment cannot succeed.
    with pytest.raises((AttributeError, TypeError)):
        declaration.credential = "sk-nope"
    assert "credential" not in doxbench_intake.DECLARATION_FIELDS
    assert not any("secret" in field or "token" in field
                   for field in doxbench_intake.DECLARATION_FIELDS)


def test_the_consent_rule_is_enforced_in_both_directions():
    """Brett's OQ-3 ruling of 2026-08-21, encoded structurally. A recorded gate
    action suffices on a single-operator loopback console; a consent instrument
    is REQUIRED on a shared or tenant install, and ONLY that case carries
    `consent_ref` — so a single-operator record that carried one would claim a
    second party that does not exist."""
    common = dict(binding_id="m", status=doxbench_intake.STATUS_APPROVED,
                  proposed_by="brett", proposed_at="2026-08-26T18:00:00Z",
                  issued_by="brett", approved_by="brett",
                  expires_at="2026-11-24T18:00:00Z", audit_ref="audit-1")
    with pytest.raises(doxbench_intake.IntakeRefused):
        doxbench_intake.ModelDeclaration(
            install_posture=doxbench_intake.POSTURE_SHARED, **common)
    with pytest.raises(doxbench_intake.IntakeRefused):
        doxbench_intake.ModelDeclaration(
            install_posture=doxbench_intake.POSTURE_SINGLE_OPERATOR,
            consent_ref="consent-1", **common)
    shared = doxbench_intake.ModelDeclaration(
        install_posture=doxbench_intake.POSTURE_SHARED,
        consent_ref="consent-1", **common)
    assert shared.approval_block()["consent_ref"] == "consent-1"
    solo = doxbench_intake.ModelDeclaration(
        install_posture=doxbench_intake.POSTURE_SINGLE_OPERATOR, **common)
    assert "consent_ref" not in solo.approval_block()


def test_a_pending_declaration_carries_no_approval_fact():
    """The other half of the same discipline: a half-filled approval is exactly
    the shape that lets a reader believe a model was answerable when it was
    not."""
    with pytest.raises(doxbench_intake.IntakeRefused):
        doxbench_intake.ModelDeclaration(
            binding_id="m", status=doxbench_intake.STATUS_PENDING,
            install_posture=doxbench_intake.POSTURE_SINGLE_OPERATOR,
            proposed_by="brett", proposed_at="2026-08-26T18:00:00Z",
            approved_by="brett")
    with pytest.raises(doxbench_intake.IntakeRefused):
        doxbench_intake.ModelDeclaration(
            binding_id="m", status=doxbench_intake.STATUS_APPROVED,
            install_posture=doxbench_intake.POSTURE_SINGLE_OPERATOR,
            proposed_by="brett", proposed_at="2026-08-26T18:00:00Z",
            approved_by="brett")


def test_a_hand_declared_binding_is_unaffected_by_the_pending_rule(tmp_path):
    """The rule this change deliberately did NOT invert. A binding the
    declarations document says nothing about resolves exactly as it resolved
    before this change, byte for byte: it was declared by hand in the settings
    file by the operator, and the operator is who approval is a record of.
    Making every binding pending until approved would have retroactively
    unapproved every install that already works."""
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    store = doxbench_binding.BindingStore(
        doxbench_binding.bindings_path(checkout))
    store.add(doxbench_binding.ModelProviderBinding(
        id="hand-declared", label="Hand declared", provider="p",
        credential_ref="ref-1",
        auth_kind=doxbench_binding.AUTH_KIND_API_KEY, approved_by="brett",
        endpoint="https://provider.invalid/v1",
        dialect=doxbench_binding.DIALECT_XFACTORY_PROMPT_V1,
        broker_argv=("/usr/bin/true",)))
    assert doxbench_intake.pending_binding_ids(checkout) == frozenset()
    factory = doxbench_install.declared_model_port_factory(
        tmp_path / "sessions", checkout_root=checkout)
    assert [e.model_id for e in factory().catalog().entries] == ["hand-declared"]


def test_an_unreadable_declarations_document_suppresses_nothing(tmp_path):
    """Fail-OPEN here, and the direction is deliberate and stated. This set
    SUPPRESSES bindings, so an unreadable document that suppressed everything
    would take an operator's working console down over a settings-file typo —
    the same failure `declared_model_port_factory` already refuses to take for
    the bindings document itself."""
    checkout = tmp_path / "checkout"
    path = doxbench_intake.declarations_path(checkout)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("kind: something-else\n", encoding="utf-8")
    assert doxbench_intake.pending_binding_ids(checkout) == frozenset()


# ===========================================================================
# layer 4 — the contract
# ===========================================================================

CONTRACTS = REPO_ROOT / "contracts"


def test_the_gate_action_enum_gained_exactly_one_additive_member():
    """Task 3.3. ONE new `action` enum member plus its `allOf` conditional,
    allocated at realization. Reusing an existing member would misname a
    governance record — the failure mode `add-doxbench-editing-phase-b` already
    hit with `share-session` and declined to take."""
    schema = yaml.safe_load(
        (CONTRACTS / "schemas" / "gate-action-record.schema.yaml").read_text(
            encoding="utf-8"))
    members = schema["properties"]["action"]["enum"]
    assert members[-1] == doxbench_intake.GATE_ACTION_APPROVE_MODEL
    assert len(members) == len(set(members))
    # ADDITIVE: the schema's own version does not move, and no object in this
    # file closes itself, which is the schema's stated forward-compatible rule.
    assert schema["contract_schema_version"] == 1
    # the conditional constrains ONLY the new member
    conditionals = [c for c in schema["allOf"]
                    if c["if"].get("properties", {}).get("action", {}).get(
                        "const") == doxbench_intake.GATE_ACTION_APPROVE_MODEL]
    assert len(conditionals) == 1
    then = conditionals[0]["then"]
    assert then["required"] == ["model_approval"]
    assert then["properties"]["target"]["required"] == ["model_declaration"]
    block = schema["$defs"]["model_approval"]
    assert set(block["required"]) == set(doxbench_intake.APPROVAL_FIELDS)


def test_the_turn_record_gained_the_remint_fact_additively():
    """Task 3.6's contract half. An OPTIONAL fact on the SUCCESS envelope only,
    carrying the REDACTED fact and nothing more.

    The blast-radius clause used to read "and the DEPRECATED v1 envelope is
    untouched", which was contract-v1.45's way of saying the same thing: at that
    release the v1 success was the other success in the file, and its promise was
    byte-identical stability. That envelope is gone at contract-v3.0
    (retire-doxbench-chat-turn-v1), so the clause is re-expressed against the
    envelopes that remain — a record-only fact must not appear on a REQUEST or on
    a FAILURE, which is the claim the v1 clause was one instance of."""
    schema = yaml.safe_load(
        (CONTRACTS / "schemas"
         / "xfactory-workbench-chat-turn.schema.yaml").read_text(
             encoding="utf-8"))
    success_v2 = schema["$defs"]["success_v2"]
    assert "provider_retry" in success_v2["properties"]
    assert "provider_retry" not in success_v2["required"], (
        "an OPTIONAL key is what makes this release additive")
    # no OTHER envelope in the family carries it, and each is closed, so a
    # producer cannot smuggle the fact onto a shape that does not declare it
    for other in ("request_v2", "failure_v2"):
        assert "provider_retry" not in schema["$defs"][other]["properties"], other
        assert schema["$defs"][other]["additionalProperties"] is False, other
    block = schema["$defs"]["provider_retry"]
    assert block["additionalProperties"] is False
    assert block["properties"]["retried"] == {"const": True}
    assert block["properties"]["at_most_once"] == {"const": True}
    assert set(block["properties"]) == {"retried", "at_most_once", "audit_ref"}
    assert schema["contract_schema_version"] == 1


def test_the_bundle_release_names_both_schemas_and_recomputes_both_digests():
    """The additive-release recipe, followed exactly: the manifest's bundle
    version moves, both changed rows' `sha256` are recomputed from the bytes on
    disk, both `consumption_rule`s name what arrived, and the CHANGELOG carries
    one entry per release."""
    manifest = yaml.safe_load(
        (CONTRACTS / "manifest.yaml").read_text(encoding="utf-8"))
    # `contract_bundle_version` is a MOVING POINTER at whatever bundle was cut
    # last, not a fact about THIS release: pinning it to contract-v1.45 asserted
    # that no later bundle exists, which contract-v1.46 falsified and every
    # future cut would falsify again. This release's own facts are immutable and
    # are the ones asserted — its CHANGELOG entry and its digest inventory,
    # both of which name the two schemas — plus the LIVE half that actually
    # matters here: both schemas are still manifest members whose recorded
    # digests match their bytes on disk.
    rows = {row["id"]: row for row in manifest["contracts"]}
    for contract_id in ("gate-action-record", "xfactory-workbench-chat-turn"):
        row = rows[contract_id]
        digest = hashlib.sha256(
            (REPO_ROOT / row["path"]).read_bytes()).hexdigest()
        assert row["sha256"] == digest, contract_id
        assert row["schema_version"] == 1
    assert "contract-v1.45" in rows["gate-action-record"]["consumption_rule"]
    assert "contract-v1.45" in rows[
        "xfactory-workbench-chat-turn"]["consumption_rule"]
    changelog = (CONTRACTS / "CHANGELOG.md").read_text(encoding="utf-8")
    assert changelog.count("## contract-v1.45 —") == 1
    # Scoped to THIS entry's own section. Reading everything above the v1.44
    # heading was the same moving-pointer mistake in a second dress: once a
    # newer entry sat on top, a later release's "ADDITIVE" line could satisfy
    # this assertion while v1.45's said anything at all.
    entry = changelog.split("## contract-v1.45")[1].split("## contract-v1.44")[0]
    assert "**Change class: ADDITIVE (minor)**" in entry
    assert "gate-action-record" in entry
    assert "xfactory-workbench-chat-turn" in entry
    inventory = yaml.safe_load(
        (CONTRACTS / "releases" / "contract-v1.45.digests.yaml").read_text(
            encoding="utf-8"))
    assert inventory["bundle_tag"] == "contract-v1.45"
    named = {e["path"] for e in inventory["entries"]}
    for schema in ("contracts/schemas/gate-action-record.schema.yaml",
                   "contracts/schemas/xfactory-workbench-chat-turn.schema.yaml"):
        assert schema in named, schema


# ===========================================================================
# layer 4b — the re-mint derivation, and the envelope it lands on
# ===========================================================================

class _LedgerPort:
    """A duck-typed port with a ledger, which is all the derivation reads."""

    def __init__(self, events):
        self.ledger = list(events)


def _event(reason, audit_ref=None, at=1.0):
    return doxbench_provider.MintEvent(binding_id="b", reason=reason, at=at,
                                       audit_ref=audit_ref)


def test_the_remint_derivation_reports_only_a_real_paid_retry():
    """Task 3.6's derivation. A first mint is not a retry; a re-mint WITH the
    paid call that followed it is, and the audit reference comes off the
    re-mint event — the identifier the broker's own trail is keyed by."""
    first = _event(doxbench_provider.REASON_FIRST_MINT, "audit-first")
    remint = _event(doxbench_provider.REASON_EXPIRY_REMINT, "audit-second",
                    at=2.0)
    retry = _event(doxbench_provider.REASON_PAID_RETRY, None, at=3.0)
    assert serve_mod.provider_retry_fact((), (first,)) is None
    assert serve_mod.provider_retry_fact((first,), (first,)) is None
    assert serve_mod.provider_retry_fact(
        (first,), (first, remint, retry)) == {
            "retried": True, "at_most_once": True, "audit_ref": "audit-second"}


def test_a_second_identical_retry_is_still_reported_under_a_frozen_clock():
    """PR #401's review, note 1. `MintEvent` is a FROZEN dataclass, so two
    DISTINCT events whose fields coincide compare EQUAL — and a `paid_retry`
    event carries no `audit_ref`, so under a clock that returns the same value
    twice its four fields are the same four fields every time. A delta derived
    with `event not in before` therefore filters the second turn's real paid
    retry out as already-seen and reports nothing, which is precisely the
    invisibility Brett's 2026-08-26 ruling exists to forbid.

    Driven the way the route drives it: a snapshot before, the port's own
    appends, a snapshot after. Turn one retries; turn two retries again on the
    same frozen tick; BOTH must be reported."""
    at = 1000.0
    port = _LedgerPort([])
    # turn one: a first mint, an expiry re-mint, and the paid call it bought.
    port.ledger.append(_event(doxbench_provider.REASON_FIRST_MINT,
                              "audit-1", at=at))
    port.ledger.append(_event(doxbench_provider.REASON_EXPIRY_REMINT,
                              "audit-2", at=at))
    port.ledger.append(_event(doxbench_provider.REASON_PAID_RETRY, None, at=at))
    first = serve_mod.provider_retry_fact(
        (), serve_mod.mint_ledger_snapshot(port))
    assert first == {"retried": True, "at_most_once": True,
                     "audit_ref": "audit-2"}

    # turn two: the same shape again, on the same tick. Its `paid_retry` event
    # is field-for-field turn one's — a different event, an equal value.
    before = serve_mod.mint_ledger_snapshot(port)
    port.ledger.append(_event(doxbench_provider.REASON_EXPIRY_REMINT,
                              "audit-3", at=at))
    port.ledger.append(_event(doxbench_provider.REASON_PAID_RETRY, None, at=at))
    assert port.ledger[-1] == port.ledger[2], (
        "the regression needs the collision it guards against: two distinct "
        "paid-retry events that compare equal")
    assert port.ledger[-1] is not port.ledger[2]
    second = serve_mod.provider_retry_fact(
        before, serve_mod.mint_ledger_snapshot(port))
    assert second == {"retried": True, "at_most_once": True,
                      "audit_ref": "audit-3"}, (
        "a second paid provider call the human cannot see is exactly what the "
        "ruling forbids")

    # …and a turn that bought nothing still reports nothing, frozen clock or no.
    quiet = serve_mod.mint_ledger_snapshot(port)
    assert serve_mod.provider_retry_fact(
        quiet, serve_mod.mint_ledger_snapshot(port)) is None


def test_the_ledger_delta_survives_the_bounded_ledgers_front_trim():
    """The ledger is NOT strictly append-only, which is why the delta is not
    positional: `_record` trims from the FRONT at `MAX_LEDGER_EVENTS`, so a
    `ledger[before_len:]` slice reads nothing at all once a long-lived console
    has filled it. The invariant that does hold — appended at the right, dropped
    only from the left — is enough, and identity honours it."""
    cap = doxbench_provider.MAX_LEDGER_EVENTS
    port = _LedgerPort([_event(doxbench_provider.REASON_FIRST_MINT,
                               f"audit-{index}", at=1.0)
                        for index in range(cap)])
    before = serve_mod.mint_ledger_snapshot(port)
    assert len(before) == cap
    port.ledger.append(_event(doxbench_provider.REASON_EXPIRY_REMINT,
                              "audit-fresh", at=1.0))
    port.ledger.append(_event(doxbench_provider.REASON_PAID_RETRY, None, at=1.0))
    del port.ledger[:-cap]           # exactly what `_record` does at the bound
    after = serve_mod.mint_ledger_snapshot(port)
    assert len(after) == cap, "the ledger is bounded, not unbounded"
    assert len(after[len(before):]) == 0, (
        "the positional delta reads nothing here — this is why it is not used")
    assert serve_mod.provider_retry_fact(before, after) == {
        "retried": True, "at_most_once": True, "audit_ref": "audit-fresh"}


def test_the_ledger_snapshot_is_a_copy_and_absence_is_a_posture():
    """`ledger` is NOT a port member and is not becoming one: the declared
    surface stays exactly three. An adapter without one contributes nothing and
    nothing about its turns changes."""
    port = _LedgerPort([_event(doxbench_provider.REASON_FIRST_MINT)])
    snapshot = serve_mod.mint_ledger_snapshot(port)
    port.ledger.append(_event(doxbench_provider.REASON_PAID_RETRY))
    assert len(snapshot) == 1, "a snapshot is a fact about the moment it was taken"
    assert serve_mod.mint_ledger_snapshot(object()) == ()


def test_the_success_envelope_carries_the_fact_only_when_it_happened():
    """The builder REBUILDS the closed block from two named scalars, so a caller
    handing in a ready-made dict cannot splice a key past it — the same
    discipline `selected_model` and `context_packet` already keep."""
    common = dict(client_turn_id="t", assistant_turn_id="a",
                  model_id="m", requested_model_id="m", routing_rule=False,
                  data_handling="on-tenant", bound_buffer="outline",
                  observed_hashes={"outline": "d" * 64,
                                   "docs/detail.md": "e" * 64},
                  assistant_prose="answered", context_posture="full")
    quiet = serve_mod.doxbench_turn_v2_success_body(**common)
    assert "provider_retry" not in quiet
    loud = serve_mod.doxbench_turn_v2_success_body(
        provider_retried=True, provider_retry_audit_ref="audit-1", **common)
    assert loud["provider_retry"] == {
        "retried": True, "at_most_once": True, "audit_ref": "audit-1"}
    bare = serve_mod.doxbench_turn_v2_success_body(
        provider_retried=True, **common)
    assert bare["provider_retry"] == {"retried": True, "at_most_once": True}
    # and all three shapes validate against the RELEASED bytes, reached through
    # the schema's own `$ref` rather than by splicing the definition into the
    # root — a spliced copy is a different document, and this assertion is only
    # worth anything if it runs against the one that ships.
    from jsonschema import Draft202012Validator
    schema = yaml.safe_load(
        (CONTRACTS / "schemas"
         / "xfactory-workbench-chat-turn.schema.yaml").read_text(
             encoding="utf-8"))
    validator = Draft202012Validator(
        {"$defs": schema["$defs"], "$ref": "#/$defs/success_v2"})
    for body in (quiet, loud, bare):
        assert not list(validator.iter_errors(body)), body
    # …and the closed block really is closed against the one key it must never
    # carry.
    leaky = json.loads(json.dumps(loud))
    leaky["provider_retry"]["minted"] = "the token"
    assert list(validator.iter_errors(leaky))
