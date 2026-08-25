"""The MODEL-DERIVED abstract's pane: its pure state formatter, its explicit
invocation, and the one region both abstracts share.

`add-doxbench-distilled-abstract` §7 (tasks 7.1-7.10) and 8.2. The derivation
half of the docs subpane — what `documentAbstract()` reads out of the snapshot —
is pinned next door in `test_doxbench_context_panes.py` and is NOT restated
here; this file is about the SECOND abstract, the one a model writes on explicit
human request, and about the region the two of them take turns inside.

WHY A SECOND FILE. `test_doxbench_context_panes.py` owns the docs/lens
RESTRUCTURE — the split, the subtabs, the height budget, the relocated
captioning pin — and it is already 600 lines carrying three Node harnesses. The
interaction pins below need two more (a pure-formatter probe and a mounted
workbench driven through a scripted abstract seam), and folding them in would
have made one file the place where every doxBench context question is answered.
The two files share their idioms deliberately: the same `_EDITOR_DOM_SHIM`,
the same mounted-workbench recipe, the same JSON-out-of-one-node-process shape.

THE THREE SEAMS THIS FILE PINS, and where each lives (design D8):

  * the PURE formatter — `abstractRegionState` in `staging-workbench-model.js`,
    which takes a description of what the pane knows and returns the caption,
    the body, the accessible name, and which controls exist. No DOM, no I/O,
    no imports;
  * the CONTROLS and the states — `staging-workbench.js`, which owns the one
    region, the explicit generate/re-generate/cancel controls and the state
    switch, and which carries NO transport of its own;
  * the ONE fetch call site — `app.js`, pinned by `test_renderer.py`.

CAPTION STRINGS ARE BRIDGED, NEVER RETYPED. Every caption assertion below reads
`doxbench_knowledge.RULED_CAPTIONS`, the Python constant the route already
answers with, so the JS strings and the server's vocabulary cannot drift into
five-and-a-sixth spellings.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402

from test_doxbench_view import _EDITOR_DOM_SHIM  # noqa: E402

NODE = shutil.which("node")
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
VIEWS = WEB / "views"
SHELL_JS = VIEWS / "staging-workbench.js"
MODEL_JS = VIEWS / "staging-workbench-model.js"
APP_JS = WEB / "app.js"

PATH_A = "ideation/staging/topic-x/topic-x.md"
PATH_B = "ideation/staging/topic-x/detail.md"

DIGEST_1 = "a" * 64
DIGEST_2 = "b" * 64

CAP_MODEL = kn.RULED_CAPTIONS[kn.CAPTION_MODEL_DERIVED]
CAP_DETERMINISTIC = kn.RULED_CAPTIONS[kn.CAPTION_DETERMINISTIC]
CAP_STALE = kn.RULED_CAPTIONS[kn.CAPTION_STALE]
CAP_UNGENERATED = kn.RULED_CAPTIONS[kn.CAPTION_NOT_YET_GENERATED]
CAP_HOSTED = kn.RULED_CAPTIONS[kn.CAPTION_HOSTED_PLANE]


# ---------------------------------------------------------------------------
# 1. the PURE formatter, in node, with no DOM at all
# ---------------------------------------------------------------------------

_FORMATTER_HARNESS = """
import {
  documentAbstract, abstractRegionState, abstractSubjectDigest,
  ABSTRACT_CAPTIONS,
} from "./staging-workbench-model.mjs";

const DOC = {
  path: "%(path_a)s",
  id: "topic-x", stage: "staged", kind: "capability-proposal",
  summary: "A neutral contract for the thing every domain re-invents.",
  topics: ["alpha"], destinations: { staged_topics: ["topic-x"] },
  completeness: { score: 0.5, structure: { value: 1, count: 6 } },
};
const SUBJECT = { path: DOC.path, title: "topic-x.md" };
const GENERATED = {
  prose: "The document argues for one neutral contract.",
  subjectDigest: "%(d1)s", modelId: "m1", generation: 1,
};

const base = {
  subject: SUBJECT, view: "deterministic", plane: "local", capable: true,
  generated: null, currentDigest: null,
  inFlight: false, waitBoundSeconds: null, refusal: null, dirty: false,
};
const at = (over) => abstractRegionState({ ...base, ...over });

const out = {
  captions: ABSTRACT_CAPTIONS,
  deterministicField: documentAbstract(DOC).caption,
  bareField: documentAbstract({ path: "docs/plain.md", id: "plain" }).caption,
  empty: at({ subject: null }),
  deterministic: at({}),
  ungenerated: at({ view: "model" }),
  modelDerived: at({ view: "model", generated: GENERATED,
                     currentDigest: "%(d1)s" }),
  stale: at({ view: "model", generated: GENERATED, currentDigest: "%(d2)s" }),
  staleInFlight: at({ view: "model", generated: GENERATED,
                      currentDigest: "%(d2)s", inFlight: true,
                      waitBoundSeconds: 60 }),
  hosted: at({ view: "model", plane: "hosted", capable: false }),
  hostedWithAbstract: at({ view: "model", plane: "hosted", capable: false,
                           generated: GENERATED, currentDigest: "%(d1)s" }),
  noCapability: at({ view: "model", capable: false }),
  noCapabilityWithAbstract: at({ view: "model", capable: false,
                                 generated: GENERATED,
                                 currentDigest: "%(d1)s" }),
  inFlightUnbounded: at({ view: "model", inFlight: true }),
  inFlightBounded: at({ view: "model", inFlight: true, waitBoundSeconds: 60 }),
  dirtyModel: at({ view: "model", generated: GENERATED,
                   currentDigest: "%(d1)s", dirty: true }),
  dirtyDeterministic: at({ dirty: true }),
  refused: at({ view: "model",
                refusal: { reason: "this document declares no topics." } }),
  // the SOURCE-DIGEST rule (7.6b): unloaded takes the server's echo, loaded
  // escalates to the buffer's own settled content identity
  digestUnloaded: abstractSubjectDigest({ buffer: null,
                                          echoedDigest: "%(d1)s" }),
  digestUnloadedUnknown: abstractSubjectDigest({ buffer: null,
                                                 echoedDigest: null }),
  digestLoadedSettled: abstractSubjectDigest({
    buffer: { loaded: true, settled: true, digest: "%(d2)s" },
    echoedDigest: "%(d1)s" }),
  digestLoadedUnsettled: abstractSubjectDigest({
    buffer: { loaded: true, settled: false, digest: null },
    echoedDigest: "%(d1)s" }),
  digestNotLoaded: abstractSubjectDigest({
    buffer: { loaded: false, settled: false, digest: null },
    echoedDigest: "%(d1)s" }),
};
process.stdout.write(JSON.stringify(out));
""" % {"path_a": PATH_A, "d1": DIGEST_1, "d2": DIGEST_2}


@pytest.fixture(scope="module")
def formatter(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the abstract-formatter probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-abstract-formatter")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    harness = tmp_path / "formatter-harness.mjs"
    harness.write_text(_FORMATTER_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_five_ruled_captions_are_spelled_exactly_as_the_route_answers(
        formatter):
    """8.2, the bridge. The route answers in `doxbench_knowledge`'s caption
    vocabulary and the region renders it; five strings in two languages is
    five strings that drift, so the JS table is asserted EQUAL to the Python
    one — same keys, same sentences — rather than sampled."""
    assert formatter["captions"] == dict(kn.RULED_CAPTIONS)


def test_the_deterministic_abstract_carries_the_ruled_caption_as_a_field(
        formatter):
    """7.8 / task 8.1's second phase. `documentAbstract()` gains a `caption`
    field so the relocated captioning pin next door can assert per-abstract
    rather than by sweeping a file both captions now live in."""
    assert formatter["deterministicField"] == CAP_DETERMINISTIC
    assert formatter["bareField"] == CAP_DETERMINISTIC


def test_one_state_renders_and_the_deterministic_one_opens(formatter):
    """7.5, at the formatter. The region opens on the DETERMINISTIC abstract —
    the one that exists before any model runs — and the model state is reached
    by an explicit switch, never by arriving."""
    opening = formatter["deterministic"]
    assert opening["captionState"] == kn.CAPTION_DETERMINISTIC
    assert opening["caption"] == CAP_DETERMINISTIC
    assert opening["structured"] is True
    assert opening["toggleOffered"] is True
    model = formatter["ungenerated"]
    assert model["captionState"] == kn.CAPTION_NOT_YET_GENERATED
    assert model["structured"] is False


def test_the_accessible_name_composes_the_subject_with_the_provenance(
        formatter):
    """7.10. ONE region, whose name says WHICH DOCUMENT and WHICH PROVENANCE —
    so the two states are distinguishable by name — and which is never the
    selected buffer's name."""
    names = {key: formatter[key]["accessibleName"]
             for key in ("deterministic", "ungenerated", "modelDerived",
                         "stale", "hosted")}
    assert names["deterministic"] == "topic-x.md — " + CAP_DETERMINISTIC
    assert names["modelDerived"] == "topic-x.md — " + CAP_MODEL
    assert names["ungenerated"] == "topic-x.md — " + CAP_UNGENERATED
    assert names["stale"] == "topic-x.md — " + CAP_STALE
    assert names["hosted"] == "topic-x.md — " + CAP_HOSTED
    # the name CHANGES when the state switches: five states, five names
    assert len(set(names.values())) == 5
    for name in names.values():
        assert "selected document" not in name.lower()


def test_the_region_with_no_subject_names_the_absence_not_a_provenance(
        formatter):
    """An empty scope selects nothing, and a region that claimed a provenance
    for a document that is not there would be naming an abstract nobody has.
    It states the absence and keeps the sentence the pane already used."""
    empty = formatter["empty"]
    assert empty["captionState"] is None
    assert empty["caption"] == ""
    assert "no document selected" in empty["accessibleName"]
    assert "selected document" not in empty["accessibleName"].lower()
    assert empty["note"] == "select a document below to see what it declares"
    assert empty["generateOffered"] is False


def test_a_stale_abstract_is_shown_and_labelled_with_its_source_digest(
        formatter):
    """7.6a (ruling 3). The abstract whose subject has moved on is SHOWN,
    LABELLED, and its source digest STATED — not discarded, not silently
    refreshed, and never presented as current."""
    stale = formatter["stale"]
    assert stale["captionState"] == kn.CAPTION_STALE
    assert stale["caption"] == CAP_STALE
    assert stale["stale"] is True
    # the abstract itself is still rendered — that is the whole ruling
    assert stale["text"] == "The document argues for one neutral contract."
    # the SOURCE digest is stated; a short prefix is acceptable, and the
    # prefix must come from the abstract's own digest, never the current one
    assert stale["digestPrefix"]
    assert DIGEST_1.startswith(stale["digestPrefix"])
    assert not DIGEST_2.startswith(stale["digestPrefix"])
    fresh = formatter["modelDerived"]
    assert fresh["stale"] is False
    assert fresh["captionState"] == kn.CAPTION_MODEL_DERIVED
    assert fresh["digestPrefix"] is None


def test_a_regeneration_in_flight_shows_over_the_stale_abstract(formatter):
    """7.6a's tail: "a regeneration in flight SHALL show the in-flight state
    over it" — the stale abstract stays on screen and readable while its
    replacement is being written."""
    both = formatter["staleInFlight"]
    assert both["inFlight"] is True
    assert both["captionState"] == kn.CAPTION_STALE
    assert both["text"] == "The document argues for one neutral contract."
    assert both["cancelOffered"] is True


def test_the_in_flight_wait_is_the_adapters_own_bound_and_never_the_ceiling(
        formatter):
    """7.3. `MAX_ADAPTER_TIMEOUT_SECONDS = 120` is the validated CEILING, not
    a prediction; a region stating 120 while the adapter declared 60 would be
    lying in the safe direction and still lying. And BEFORE any response has
    carried a bound, the region names no number at all rather than guessing
    one."""
    bounded = formatter["inFlightBounded"]
    assert bounded["inFlight"] is True
    assert "60" in bounded["waitText"]
    assert "120" not in bounded["waitText"]
    assert bounded["cancelOffered"] is True
    unbounded = formatter["inFlightUnbounded"]
    assert unbounded["inFlight"] is True
    assert unbounded["waitText"]
    assert not any(ch.isdigit() for ch in unbounded["waitText"]), (
        "an unlearned wait bound must name NO number — inventing one is how "
        "120 gets shown for a 60-second adapter")
    assert unbounded["cancelOffered"] is True


def test_a_dirty_subject_is_captioned_as_describing_the_saved_version(
        formatter):
    """7.4. The server reads the SAVED bytes and the request carries no buffer
    text, so an abstract of a dirty loaded subject describes the saved
    version — and says so, beside the ruled caption rather than instead of
    it."""
    dirty = formatter["dirtyModel"]
    assert dirty["captionState"] == kn.CAPTION_MODEL_DERIVED
    assert dirty["caption"] == CAP_MODEL          # the ruled caption is exact
    assert dirty["savedVersionNote"]
    assert "saved" in dirty["savedVersionNote"].lower()
    # the deterministic abstract reads the SNAPSHOT, not the buffer, so it
    # makes no claim about saved-vs-unsaved
    assert formatter["dirtyDeterministic"]["savedVersionNote"] is None
    assert formatter["modelDerived"]["savedVersionNote"] is None


def test_without_the_gate_capability_the_control_is_absent_not_refusing(
        formatter):
    """7.7. The generation control is ABSENT rather than present-and-refusing,
    and an abstract already generated in this session stays readable with its
    normal caption."""
    off = formatter["noCapability"]
    assert off["generateOffered"] is False
    assert off["regenerateOffered"] is False
    assert off["captionState"] == kn.CAPTION_NOT_YET_GENERATED
    kept = formatter["noCapabilityWithAbstract"]
    assert kept["generateOffered"] is False
    assert kept["regenerateOffered"] is False
    assert kept["captionState"] == kn.CAPTION_MODEL_DERIVED
    assert kept["text"] == "The document argues for one neutral contract."


def test_the_hosted_plane_states_a_fact_about_the_plane(formatter):
    """7.7's hosted half, and the ADDED requirement's own words: the caption is
    "a statement about the plane and never about the document"."""
    hosted = formatter["hosted"]
    assert hosted["captionState"] == kn.CAPTION_HOSTED_PLANE
    assert hosted["caption"] == CAP_HOSTED
    assert hosted["generateOffered"] is False
    assert hosted["regenerateOffered"] is False
    # even a cached abstract does not turn the hosted plane into a generator,
    # and the plane's own statement outranks it
    assert formatter["hostedWithAbstract"]["generateOffered"] is False


def test_a_stated_refusal_renders_its_reason_and_no_abstract(formatter):
    """The route's stated refusals carry a reason sentence and NO prose. The
    region shows the sentence under the not-yet-generated caption; there is no
    field an unverified answer could arrive in."""
    refused = formatter["refused"]
    assert refused["captionState"] == kn.CAPTION_NOT_YET_GENERATED
    assert refused["text"] is None
    assert refused["note"] == "this document declares no topics."


def test_the_source_digest_escalates_only_where_a_buffer_exists(formatter):
    """7.6b. For an UNLOADED subject the source digest is the SERVED SAVED
    CONTENT's — the digest the server echoed — and the per-buffer
    settled-content-identity guard is not required of it; most wheel subjects
    have no buffer, and a per-buffer rule applied to them would have nothing to
    compare. Where the subject IS a loaded buffer, the comparison escalates to
    that buffer's own settled identity."""
    assert formatter["digestUnloaded"] == DIGEST_1
    assert formatter["digestUnloadedUnknown"] is None
    assert formatter["digestLoadedSettled"] == DIGEST_2
    # an UNSETTLED buffer proves nothing about content identity, so the rule
    # falls back to the served digest rather than forcing a comparison
    assert formatter["digestLoadedUnsettled"] == DIGEST_1
    assert formatter["digestNotLoaded"] == DIGEST_1


# ---------------------------------------------------------------------------
# 2. the mounted pane, driven through a scripted abstract seam
# ---------------------------------------------------------------------------
#
# The recipe is `test_doxbench_context_panes.py`'s mounted-workbench harness,
# with two additions: the gate capability is LIVE (so the canvas, the rail and
# the generation control all exist) and the `doxbench` bundle carries a
# SCRIPTED `documentAbstract` seam — the same injected-seam idiom `save`,
# `catalog` and `chatTurn` already use in that file, so the pane is driven
# exactly as `app.js` drives it and no test reaches around the seam.

_PANE_PRELUDE = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';

globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');
globalThis.window = { location: { href: 'http://localhost/' } };

{
  const rawCreateElement = document.createElement;
  function withStyleMethods(node) {
    node.style.setProperty = (name, value) => { node.style[name] = value; };
    node.style.removeProperty = (name) => { delete node.style[name]; };
    node.style.getPropertyValue = (name) => node.style[name] || '';
    return node;
  }
  document.createElement = (tag) => withStyleMethods(rawCreateElement(tag));
  document.createElementNS = (_ns, tag) => document.createElement(tag);
}

const { mountStagingWorkbench } = await import('./staging-workbench.js');

const PATH_A = 'IDEATION_PATH_A';
const PATH_B = 'IDEATION_PATH_B';
const DIGEST_1 = 'DIGEST_ONE';
const DIGEST_2 = 'DIGEST_TWO';

function snapshotFor() {
  return {
    repository: 'fixture-repo',
    generation: { source_revision: '1'.repeat(40) },
    documents: [
      { id: PATH_A, path: PATH_A, topics: ['alpha'],
        summary: 'The declared summary of topic-x.',
        destinations: { staged_topics: ['topic-x'] } },
      { id: PATH_B, path: PATH_B, topics: ['beta'],
        summary: 'The declared summary of detail.',
        destinations: { capabilities: ['cap-a'] } },
    ],
    clusters: [], possibles: [],
    staged_topics: [{ staging_id: 'topic-x', files: [PATH_A, PATH_B] }],
  };
}

async function fire(node, type, extra = {}) {
  let prevented = false;
  for (const fn of (node.listeners && node.listeners[type]) || []) {
    await fn({ target: node, stopPropagation() {},
               preventDefault() { prevented = true; }, ...extra });
  }
  return prevented;
}
const settle = () => new Promise((r) => setTimeout(r, 0));
async function quiesce(n = 40) { for (let i = 0; i < n; i += 1) await settle(); }

// The SCRIPTED abstract seam. It records every request verbatim and hands back
// a promise the scenario resolves by hand, which is what makes "resolves after
// the subject changed" and "cancelled mid-flight" reachable at all.
function scriptedAbstracts() {
  const requests = [];
  let pending = null;
  return {
    requests,
    seam: (request) => {
      requests.push(JSON.parse(JSON.stringify(request)));
      return new Promise((resolve) => { pending = resolve; });
    },
    resolve(answer) { const r = pending; pending = null; if (r) r(answer); },
    outstanding: () => pending !== null,
  };
}

function mountWorkbench(container, abstracts, capOverrides) {
  const doxbench = {
    loadSource: async (path) => ({ content: '# ' + path + '\n', ref: 'main' }),
    storage: { getItem: () => null, setItem() {}, removeItem() {} },
    catalog: async () => ({ schema_version: 1, kind: 'workbench-model-catalog',
                            models: [{ model_id: 'm1', label: 'M1',
                                       available: true }] }),
    chatTurn: async () => ({ ok: false, status: 502, payload: {} }),
    save: async () => ({ status: 'committed', buffers: [] }),
    documentAbstract: abstracts ? abstracts.seam : undefined,
  };
  return mountStagingWorkbench(container, snapshotFor(), {
    caps: { actions: { gate: true, session: true }, actor: 'brett',
            console_token: 'tok', ...(capOverrides || {}) },
    fetcher: async () => ({ ok: false }),
    active: { repository: 'fixture-repo', ref: 'main' },
    index: { entries: [] },
    doxbench,
    sourceBase: '/source/',
    edit: null,
    onSessionRekey: async () => null,
    onSessionEnded: async () => null,
    onScopeOpened: () => null,
  });
}

function probe(container) {
  const byClass = (cls) => container.walk().filter(
    (n) => String(n.className).split(' ').includes(cls));
  const one = (cls) => byClass(cls)[0] || null;
  const text = (cls) => (one(cls) ? String(one(cls).textContent) : null);
  return { byClass, one, text };
}

function regionShot(container) {
  const { byClass, one, text } = probe(container);
  const region = one('swb-docabstract');
  return {
    regions: byClass('swb-docabstract').length,
    states: byClass('swb-abstractstate').length,
    stateClass: one('swb-abstractstate')
      ? String(one('swb-abstractstate').className) : null,
    name: region ? region.getAttribute('aria-label') : null,
    role: region ? region.getAttribute('role') : null,
    caption: text('swb-abstractcaption'),
    body: text('swb-abstractstate'),
    title: text('swb-abstracttitle'),
    note: text('swb-abstractnote'),
    inflight: text('swb-abstractinflight'),
    saved: text('swb-abstractsaved'),
    generate: byClass('swb-abstractgenerate').length,
    generateLabel: text('swb-abstractgenerate'),
    cancel: byClass('swb-abstractcancel').length,
    toggle: byClass('swb-abstracttoggle').length,
    toggleLabel: text('swb-abstracttoggle'),
    headings: byClass('swb-docabstract').reduce(
      (n, host) => n + host.walk().filter(
        (x) => /^H[1-6]$/.test(x.tagName)).length, 0),
    regionText: region ? String(region.textContent) : null,
  };
}

async function press(container, cls) {
  const { byClass } = probe(container);
  const btn = byClass(cls)[0];
  if (!btn) throw new Error('no control with class ' + cls);
  await fire(btn, 'click');
  await quiesce();
}

async function spin(container, key, times) {
  const { one } = probe(container);
  const selector = one('swb-docselector');
  if (!selector) throw new Error('the docs wheel did not mount');
  for (let i = 0; i < times; i += 1) {
    await fire(selector, 'keydown', { key });
    await quiesce(4);
  }
}

function successBody(subjectPath, digest, prose, waitBound, generation) {
  return { ok: true, status: 200, payload: {
    ok: true, subject_path: subjectPath, subject_digest: digest,
    model_id: 'm1', prose, caption_state: 'model-derived',
    generation, wait_bound_seconds: waitBound } };
}
"""


def _prelude() -> str:
    return (_PANE_PRELUDE
            .replace("IDEATION_PATH_A", PATH_A)
            .replace("IDEATION_PATH_B", PATH_B)
            .replace("DIGEST_ONE", DIGEST_1)
            .replace("DIGEST_TWO", DIGEST_2))


_PANE_HARNESS = _prelude() + r"""
const out = {};
const abstracts = scriptedAbstracts();
const container = document.createElement('div');
const workbench = mountWorkbench(container, abstracts, null);
workbench.open('staged', 'topic-x');
await quiesce();

// ---- 7.1: SPINNING DISPATCHES NOTHING ------------------------------------
// `doc-wheel.js` fires `onSelect` on EVERY notch and once more at mount, so a
// design that generated on selection would spend a model call on every
// document a reader spins past. Six notches, both directions, plus Home/End.
await spin(container, 'ArrowDown', 3);
await spin(container, 'ArrowUp', 3);
await spin(container, 'Home', 1);
await spin(container, 'End', 1);
out.spinRequests = abstracts.requests.length;
out.afterSpin = regionShot(container);

// put the wheel on document A and record the opening state
const { one } = probe(container);
container.walk();
const wheel = (container.walk().find(
  (n) => String(n.className).split(' ').includes('swb-pane-docs')) || {}).__docWheel;
if (!wheel) throw new Error('the docs pane exposes no wheel');
wheel.selectPath(PATH_A);
await quiesce();
out.opening = regionShot(container);

// ---- 7.5 / 7.10: the explicit state switch -------------------------------
await press(container, 'swb-abstracttoggle');
out.modelViewBeforeGeneration = regionShot(container);
out.switchRequests = abstracts.requests.length;

// ---- 7.3: in flight, cancellable, and no invented bound ------------------
await press(container, 'swb-abstractgenerate');
out.firstRequest = abstracts.requests[0] || null;
out.firstRequestKeys = abstracts.requests[0]
  ? Object.keys(abstracts.requests[0]).sort() : null;
out.inFlightFirst = regionShot(container);

// ---- 7.3's cancel half ----------------------------------------------------
await press(container, 'swb-abstractcancel');
out.afterCancel = regionShot(container);
// the cancelled generation still resolves server-side; its answer must not
// paint over the region the human took back
abstracts.resolve(successBody(PATH_A, DIGEST_1, 'CANCELLED ANSWER', 60, 1));
await quiesce();
out.afterCancelledAnswerLanded = regionShot(container);

// ---- the real generation --------------------------------------------------
await press(container, 'swb-abstractgenerate');
abstracts.resolve(successBody(
  PATH_A, DIGEST_1, 'A distillation of topic-x, in one sentence.', 60, 2));
await quiesce();
out.generated = regionShot(container);

// ---- 7.3: the bound is now LEARNED, and it is the adapter's own -----------
await press(container, 'swb-abstractgenerate');
out.inFlightSecond = regionShot(container);
out.regenerateRequest = abstracts.requests[abstracts.requests.length - 1];

// ---- 7.2: a slow answer resolves after the subject changed ---------------
wheel.selectPath(PATH_B);
await quiesce();
out.afterSubjectChange = regionShot(container);
abstracts.resolve(successBody(
  PATH_A, DIGEST_1, 'A LATE ANSWER ABOUT TOPIC X.', 60, 3));
await quiesce();
out.afterLateAnswer = regionShot(container);
out.lateAnswerLeaked =
  String(regionShot(container).regionText || '').includes('LATE ANSWER');

// ---- 7.6: the abstract survives leaving and re-entering the tile ----------
const requestsBeforeReturn = abstracts.requests.length;
wheel.selectPath(PATH_A);
await quiesce();
out.afterReturn = regionShot(container);
out.requestsOnReturn = abstracts.requests.length - requestsBeforeReturn;

// ---- 7.6a: the subject moves past the digest the abstract came from ------
// A re-generate that comes back as a STATED REFUSAL for a NEW digest: the pane
// learns the subject has moved without receiving a replacement abstract, which
// is exactly the state ruling 3 is about.
await press(container, 'swb-abstractgenerate');
abstracts.resolve({ ok: false, status: 409, payload: {
  ok: false, refused: 'subject-not-distillable',
  reason: 'this document declares neither topics nor destinations.',
  caption_state: 'not-yet-generated', subject_path: PATH_A,
  subject_digest: DIGEST_2, wait_bound_seconds: 60 } });
await quiesce();
out.stale = regionShot(container);

// ---- 7.5 again: switching back is still ONE region, ONE state -------------
await press(container, 'swb-abstracttoggle');
out.backToDeterministic = regionShot(container);

process.stdout.write(JSON.stringify(out));
"""


def _run_harness(tmp_path_factory, name: str, source: str, timeout: int = 180):
    root = tmp_path_factory.mktemp(name)
    views = root / "views"
    shutil.copytree(VIEWS, views)
    shutil.copytree(WEB / "vendor", root / "vendor")
    (root / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (root / "vendor" / "package.json").write_text('{"type": "commonjs"}',
                                                  encoding="utf-8")
    harness = views / (name + "-harness.mjs")
    harness.write_text(source, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=timeout)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


@pytest.fixture(scope="module")
def pane(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the abstract-pane probe")
    return _run_harness(tmp_path_factory, "doxbench-abstract-pane",
                        _PANE_HARNESS)


def test_spinning_the_wheel_dispatches_no_model_call(pane):
    """7.1 — THE PIN THE WHOLE INTERACTION DESIGN EXISTS FOR. `setFocus` fires
    `onSelect` on every notch (`doc-wheel.js:205-212`) and once more at mount
    (`:463`), and the docs pane renders the abstract from that callback. Eight
    notches across two documents, in both directions, plus Home and End: ZERO
    dispatches."""
    assert pane["spinRequests"] == 0
    # …and switching to the model VIEW is still not an invocation: the state
    # switch is a reading choice, the generate control is the invocation
    assert pane["switchRequests"] == 0
    assert pane["modelViewBeforeGeneration"]["caption"] == CAP_UNGENERATED


def test_exactly_one_region_holds_exactly_one_state(pane):
    """7.5. The upper half of the docs split is a measured 280px box; two
    regions would mean two accessible names for one box and a second thing to
    keep in sync. So: one region, one state rendered at a time, the
    deterministic one opening."""
    for shot in (pane["opening"], pane["modelViewBeforeGeneration"],
                 pane["generated"], pane["stale"],
                 pane["backToDeterministic"]):
        assert shot["regions"] == 1, shot
        assert shot["states"] == 1, shot
        assert shot["role"] == "region", shot
    assert "deterministic" in pane["opening"]["stateClass"]
    assert pane["opening"]["caption"] == CAP_DETERMINISTIC
    assert "deterministic" in pane["backToDeterministic"]["stateClass"]


def test_the_region_is_never_announced_as_the_selected_document(pane):
    """7.10, at the mounted surface. `staging-workbench.js:250` used to name
    this region `selected document` — a name that belongs to the loaded-document
    selector, and two surfaces claiming one name is how the two come to
    disagree. The name now composes the SUBJECT with the PROVENANCE and moves
    when either does."""
    shots = ("opening", "modelViewBeforeGeneration", "generated", "stale")
    names = [pane[key]["name"] for key in shots]
    for name in names:
        assert name
        assert "selected document" not in name.lower()
    assert pane["opening"]["name"].startswith("topic-x.md")
    assert pane["opening"]["name"].endswith(CAP_DETERMINISTIC)
    assert pane["generated"]["name"].endswith(CAP_MODEL)
    assert pane["stale"]["name"].endswith(CAP_STALE)
    assert pane["modelViewBeforeGeneration"]["name"].endswith(CAP_UNGENERATED)
    # the name CHANGES with the state, which is the point of composing it
    assert len(set(names)) == len(names)
    # the house idiom: a NAMED region carrying no heading of its own
    assert pane["opening"]["headings"] == 0


def test_the_request_carries_no_buffer_text(pane):
    """7.4. The request is the CLOSED shape §5 declares — a scope, a subject
    path and a model id — and nothing else. The server reads the SAVED bytes,
    so there is no field unsaved buffer text could travel in even by
    accident."""
    assert pane["firstRequestKeys"] == ["model_id", "scope", "subject_path"]
    request = pane["firstRequest"]
    assert request["subject_path"] == PATH_A
    assert request["model_id"] == "m1"
    assert sorted(request["scope"]) == ["ref", "repository", "tile_id",
                                        "tile_kind"]
    assert request["scope"]["tile_kind"] == "staged"
    assert request["scope"]["tile_id"] == "topic-x"
    flat = json.dumps(request)
    for smuggled in ("content", "text", "buffer", "message", "packet"):
        assert smuggled not in flat, (smuggled, flat)


def test_the_in_flight_state_is_cancellable_and_states_its_learned_bound(pane):
    """7.3. Before any response has carried a bound the region names NO number
    — never the 120-second contract ceiling — and once a response has stated
    the adapter's own 60, that is what the next in-flight state shows."""
    first = pane["inFlightFirst"]
    assert first["cancel"] == 1
    assert first["inflight"]
    assert "120" not in first["inflight"]
    assert not any(ch.isdigit() for ch in first["inflight"])
    second = pane["inFlightSecond"]
    assert second["cancel"] == 1
    assert "60" in second["inflight"]
    assert "120" not in second["inflight"]


def test_a_cancelled_generation_never_paints_the_region(pane):
    """7.3's cancel half. Cancelling takes the wait back; the request may still
    complete on the server (its store replays it, so nothing is wasted), and
    when that answer arrives it is discarded exactly as a superseded one is."""
    assert pane["afterCancel"]["cancel"] == 0
    assert pane["afterCancel"]["caption"] == CAP_UNGENERATED
    landed = pane["afterCancelledAnswerLanded"]
    assert "CANCELLED ANSWER" not in (landed["regionText"] or "")
    assert landed["caption"] == CAP_UNGENERATED


def test_an_answer_for_a_subject_the_pane_left_is_discarded_unrendered(pane):
    """7.2. Without the subject recheck a slow answer paints itself over
    whatever the reader has since spun to, under a confident caption — a
    wrong-document abstract that reads as right."""
    moved = pane["afterSubjectChange"]
    assert moved["title"] == "detail.md"
    landed = pane["afterLateAnswer"]
    assert pane["lateAnswerLeaked"] is False
    assert "LATE ANSWER" not in (landed["regionText"] or "")
    # and the region states the CURRENT subject's real state, which is that it
    # has no abstract
    assert landed["caption"] == CAP_UNGENERATED
    assert landed["name"].startswith("detail.md")
    assert landed["name"].endswith(CAP_UNGENERATED)


def test_an_abstract_survives_leaving_and_re_entering_the_tile(pane):
    """7.6. A reader comparing two documents moves between them; regenerating
    on every return would spend a model call on a question already answered.
    Keyed by (path, digest), in session, with no second dispatch."""
    back = pane["afterReturn"]
    assert back["caption"] == CAP_MODEL
    assert back["body"] == "A distillation of topic-x, in one sentence."
    assert pane["requestsOnReturn"] == 0


def test_a_subject_that_moved_past_its_abstract_is_labelled_stale(pane):
    """7.6a (ruling 3), end to end. The pane learns the subject's digest moved
    — here from a stated refusal echoing the new digest — and the abstract it
    already holds is SHOWN, LABELLED STALE, with its source digest stated. Not
    discarded, not silently refreshed, and not presented as current."""
    stale = pane["stale"]
    assert stale["caption"].startswith(CAP_STALE)
    assert DIGEST_1[:12] in stale["caption"]
    assert stale["body"] == "A distillation of topic-x, in one sentence."
    assert stale["name"].endswith(CAP_STALE)
    # the refusal's own sentence is stated too — it is why nothing replaced it
    assert "declares neither topics nor destinations" in (stale["note"] or "")


# ---------------------------------------------------------------------------
# 3. the two postures where generation is NOT offered
# ---------------------------------------------------------------------------

_POSTURE_HARNESS = _prelude() + r"""
const out = {};

// (1) a CAPABLE console generates one abstract …
const abstracts = scriptedAbstracts();
const capable = document.createElement('div');
const first = mountWorkbench(capable, abstracts, null);
first.open('staged', 'topic-x');
await quiesce();
const capableWheel = (capable.walk().find(
  (n) => String(n.className).split(' ').includes('swb-pane-docs')) || {}).__docWheel;
capableWheel.selectPath(PATH_A);
await quiesce();
await press(capable, 'swb-abstracttoggle');
await press(capable, 'swb-abstractgenerate');
abstracts.resolve(successBody(
  PATH_A, DIGEST_1, 'A distillation of topic-x, in one sentence.', 60, 1));
await quiesce();
out.capable = regionShot(capable);

// (2) … and a console with NO GATE CAPABILITY reads it back with no control.
// The seam is WIRED here, and scripted: the only thing missing is the gate
// capability, so the control's absence is attributable to that and nothing
// else. `ungatedRequests` proves nothing was dispatched behind its back.
const ungatedSeam = scriptedAbstracts();
const ungated = document.createElement('div');
const second = mountWorkbench(ungated, ungatedSeam, { actions: {} });
second.open('staged', 'topic-x');
await quiesce();
const ungatedWheel = (ungated.walk().find(
  (n) => String(n.className).split(' ').includes('swb-pane-docs')) || {}).__docWheel;
ungatedWheel.selectPath(PATH_A);
await quiesce();
out.ungatedDeterministic = regionShot(ungated);
await press(ungated, 'swb-abstracttoggle');
out.ungatedModel = regionShot(ungated);
out.ungatedRequests = ungatedSeam.requests.length;

// (3) the HOSTED read-only plane states a fact about the PLANE.
// Wired here too: on the hosted plane the ABSENCE is a fact about the plane,
// not about whether anybody remembered to inject a transport.
const hostedSeam = scriptedAbstracts();
const hosted = document.createElement('div');
const third = mountWorkbench(hosted, hostedSeam, { actions: { session: false } });
third.open('staged', 'topic-x');
await quiesce();
const hostedWheel = (hosted.walk().find(
  (n) => String(n.className).split(' ').includes('swb-pane-docs')) || {}).__docWheel;
hostedWheel.selectPath(PATH_B);
await quiesce();
out.hostedDeterministic = regionShot(hosted);
await press(hosted, 'swb-abstracttoggle');
out.hostedModel = regionShot(hosted);
out.hostedRequests = hostedSeam.requests.length;

process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def postures(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the abstract-posture probe")
    return _run_harness(tmp_path_factory, "doxbench-abstract-postures",
                        _POSTURE_HARNESS)


def test_without_the_gate_capability_the_pane_offers_no_generation(postures):
    """7.7, mounted. The control is ABSENT rather than present-and-refusing —
    the posture this surface already takes for every other session
    affordance — and the abstract generated moments ago on a capable console
    is still readable, with its normal caption."""
    ungated = postures["ungatedModel"]
    assert ungated["generate"] == 0
    assert ungated["cancel"] == 0
    assert ungated["caption"] == CAP_MODEL
    assert ungated["body"] == "A distillation of topic-x, in one sentence."
    # the transport IS wired on this mount, so the missing gate capability is
    # the only thing the absence can be attributed to — and nothing was
    # dispatched behind the control's back either
    assert postures["ungatedRequests"] == 0
    # the deterministic half is untouched by the absence
    assert postures["ungatedDeterministic"]["caption"] == CAP_DETERMINISTIC
    assert postures["ungatedDeterministic"]["generate"] == 0


def test_the_hosted_plane_states_that_the_plane_offers_no_distillation(
        postures):
    """The hosted read-only plane offers no model-consuming route at all, so
    the region renders the deterministic abstract and states that no
    distillation is available ON THAT PLANE — about the plane, never about the
    document."""
    hosted = postures["hostedModel"]
    assert hosted["generate"] == 0
    assert hosted["caption"] == CAP_HOSTED
    assert hosted["name"].endswith(CAP_HOSTED)
    assert postures["hostedRequests"] == 0
    assert postures["hostedDeterministic"]["caption"] == CAP_DETERMINISTIC


def test_the_capable_console_is_what_produced_the_cached_abstract(postures):
    """The control in the two tests above: on a console that HAS the gate
    capability the generate control exists, is pressed, and produces the
    abstract the ungated console then reads back. Without this the two absences
    would prove nothing — an abstract nobody could generate is also absent."""
    capable = postures["capable"]
    assert capable["caption"] == CAP_MODEL
    assert capable["body"] == "A distillation of topic-x, in one sentence."
    assert capable["generate"] == 1


def test_every_caption_ships_with_the_carrier_ruling_5_declared_for_it(
        pane, postures):
    """8.2, the whole of it in one place. Ruling 5 declared not just five
    sentences but a CARRIER for each, and a caption a screen reader never
    reaches is not a caption:

      * MODEL-DERIVED and DETERMINISTIC — the two states with a provenance to
        claim — are BOTH visible text AND part of the region's accessible name,
        so which abstract a reader landed on is answerable without reading the
        body;
      * STALE, NOT-YET-GENERATED and HOSTED-PLANE are visible text INSIDE the
        already-named region.

    Each caption is read from `doxbench_knowledge.RULED_CAPTIONS`, so a sixth
    spelling on either side of the seam fails here rather than shipping.
    """
    for shot, caption in ((pane["opening"], CAP_DETERMINISTIC),
                          (pane["generated"], CAP_MODEL)):
        assert shot["caption"].startswith(caption)
        assert caption in (shot["regionText"] or "")
        assert shot["name"].endswith(caption)
    for shot, caption in ((pane["stale"], CAP_STALE),
                          (pane["afterLateAnswer"], CAP_UNGENERATED),
                          (postures["hostedModel"], CAP_HOSTED)):
        assert caption in (shot["regionText"] or ""), caption
        assert shot["role"] == "region"
        assert shot["name"], "the region carrying the caption must be NAMED"
        assert "selected document" not in shot["name"].lower()


# ---------------------------------------------------------------------------
# 4. the boundary this slice does NOT cross (clarification N2)
# ---------------------------------------------------------------------------


def test_the_abstract_is_terminal_and_says_where_a_promotion_would_attach():
    """N2. The abstract is READ-ONLY TERMINAL CONTENT: nothing in this slice
    writes a `Summary:` header, and the region offers no promotion affordance.
    That absence is a deliberate boundary rather than an oversight, so the
    module names the attachment point a future "propose this as `Summary:`"
    verb would use — the existing chat-proposal → Apply → gate path (Option
    B′) — exactly once, where that verb would go."""
    shell = SHELL_JS.read_text(encoding="utf-8")
    assert shell.count("N2") >= 1
    marker = [line for line in shell.splitlines() if "Summary:" in line
              and "propose" in line.lower()]
    assert marker, (
        "no comment names where a promotion verb would attach; N2 requires "
        "the boundary to be stated where the verb would go")
    # and nothing in the pane actually writes one
    assert "Summary:" not in shell.replace("".join(marker), "")


def test_the_pane_carries_no_promotion_control():
    """The other half of N2, checked against the rendered surface rather than
    the comments: the region's controls are reading controls only."""
    shell = SHELL_JS.read_text(encoding="utf-8")
    controls = [cls for cls in
                ("swb-abstractgenerate", "swb-abstractcancel",
                 "swb-abstracttoggle")
                if cls in shell]
    assert sorted(controls) == ["swb-abstractcancel", "swb-abstractgenerate",
                                "swb-abstracttoggle"]
    for banned in ("swb-abstractpromote", "swb-abstractapply",
                   "swb-abstractwrite", "swb-abstractedit"):
        assert banned not in shell
    # the one write-shaped spelling that IS allowed is a NOTE, not a control:
    # `swb-abstractsaved` states that the abstract describes the SAVED version
    # of a dirty buffer (task 7.4). It is a div, and it is never a button.
    assert 'el("div", "swb-abstractsaved"' in shell


def test_the_transport_stays_in_app_js():
    """7.9's companion, stated where the new seam is introduced: the pane calls
    an INJECTED seam and the route lives in `app.js`. `test_renderer.py` counts
    the call sites; this names the one file the abstract route may appear in."""
    assert "/actions/workbench/document-abstract" in APP_JS.read_text(
        encoding="utf-8")
    shell = SHELL_JS.read_text(encoding="utf-8")
    assert "/actions/workbench/document-abstract" not in shell
    assert "documentAbstract" in shell   # the injected seam, by name
    model = MODEL_JS.read_text(encoding="utf-8")
    assert "/actions/workbench/document-abstract" not in model
