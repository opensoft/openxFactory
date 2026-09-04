"""The NON-BLANK reduced_reason rule, at every gate (issue #263, fresh-eyes F1).

The issue's reproduction table IS this file's test matrix. Nine blank classes,
every one of which passed all five gates at `821f0167` and rendered as a
disclosure with nothing in it — the exact outcome the browser adopter's own
comment forbids ("showing the bare words 'reduced context' with no reason would
be that degradation wearing a badge"), arriving through the one input shape
nobody checked.

WHY A DEDICATED FILE. The rule has FOUR homes in THREE runtimes and its whole
risk is that they drift apart. Testing each gate where it lives would put the
agreement nowhere; this file is the agreement's home. The per-gate posture tests
that already exist are extended, never weakened — the released ceiling, the
pairing, and the two shipped constants are still asserted where they were.

THE PREDICATE: a reason states something iff it contains at least one character
IN `L* ∪ N* ∪ P* ∪ S*` — a letter, number, punctuation mark or symbol. Stated as
what it ADMITS, which makes it version-stable: `Cn` is never L/N/P/S in any
Unicode table, so a newer table can never turn a blank into a stated reason. It
is strictly narrower than the blank categories, additionally refusing `Co`
(private use), `Cn` (unassigned) and `Cs` (surrogates).

HISTORY, because this file is the agreement's home and a stale statement of the
rule here is the worst place for one: the rule was FIRST written as an
EXCLUSION — "outside `White_Space ∪ Cc ∪ Cf ∪ Mn ∪ Mc ∪ Me`" — and a full
code-point sweep found 51 points where the two runtimes' Unicode tables
disagreed, with the server accepting what the browser refused. That form is
history and is not the rule.

`.strip()`/`.trim()` was never it either, and the table below is why — it
empties four of the nine and leaves five untouched, because those five are
zero-visible-width rather than whitespace.

WHAT EACH GATE DOES WITH THE VERDICT DIFFERS, and the tests say so: the
published conformance validator WARNS and still accepts (contract-v1.40
accepted these records), while the three runtime gates REFUSE.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import time
import unicodedata
from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_packet as pk  # noqa: E402
from ideation_dashboard import serve as serve_mod  # noqa: E402
from ideation_dashboard.doxbench_scope import ScopeKey  # noqa: E402

NODE = shutil.which("node")
CHAT_MODEL_JS = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
                 / "doxbench-chat-model.js")

# ---------------------------------------------------------------------------
# THE MATRIX — the issue's nine classes, with the category that makes each one
# blank and whether `.strip()` would have caught it. The `strippable` column is
# asserted below, so the claim "`.strip()` is not enough" is measured here
# rather than believed.
# ---------------------------------------------------------------------------

BLANK_CLASSES: tuple[tuple[str, str, str, bool], ...] = (
    ("space", " ", "Zs", True),
    ("tab", "\t", "Cc", True),
    ("NBSP", " ", "Zs", True),
    ("newline", "\n", "Cc", True),
    ("ZWSP", "​", "Cf", False),
    ("BOM", "﻿", "Cf", False),
    ("bidi-override", "‮", "Cf", False),
    ("combining-only", "́", "Mn", False),
    ("control", "", "Cc", False),
)

# Values that MUST still be accepted. The last three are the guard against this
# rule quietly becoming a filter on non-Latin prose: a reason may be entirely
# CJK, may be an emoji, and may carry combining marks on a real base letter.
STATED_VALUES: tuple[tuple[str, str], ...] = (
    ("shipped: no knowledge service", pk.REDUCED_NO_KNOWLEDGE_SERVICE),
    ("shipped: retrieval refused", pk.REDUCED_RETRIEVAL_REFUSED),
    ("CJK", "漢字"),
    ("emoji", "\U0001f600"),
    ("base letter + combining", "á"),
    ("text with blanks around it", " ​ x ﻿ "),
)

BLANK_IDS = [name for name, _v, _c, _s in BLANK_CLASSES]
STATED_IDS = [name for name, _v in STATED_VALUES]


# ---------------------------------------------------------------------------
# the matrix's own premises
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,value,category,strippable", BLANK_CLASSES,
                         ids=BLANK_IDS)
def test_the_recorded_category_and_strippability_are_what_the_table_says(
        name, value, category, strippable):
    """The table is EVIDENCE, so it is checked. If a future Unicode release
    moves one of these characters between categories, this fails loudly here
    rather than silently changing what the predicate refuses."""
    assert unicodedata.category(value) == category, name
    assert (value.strip() == "") is strippable, name


def test_strip_alone_would_miss_five_of_the_nine():
    """The issue's central claim, measured. This is why the predicate is written
    over categories instead of whitespace."""
    missed = [n for n, v, _c, _s in BLANK_CLASSES if v.strip() != ""]
    assert len(missed) == 5
    assert set(missed) == {"ZWSP", "BOM", "bidi-override", "combining-only",
                           "control"}


# ---------------------------------------------------------------------------
# the canonical predicate
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name,value,_c,_s", BLANK_CLASSES, ids=BLANK_IDS)
def test_the_predicate_refuses_every_blank_class(name, value, _c, _s):
    assert pk.states_something(value) is False, name


@pytest.mark.parametrize("name,value", STATED_VALUES, ids=STATED_IDS)
def test_the_predicate_accepts_every_stated_value(name, value):
    assert pk.states_something(value) is True, name


def test_the_predicate_refuses_a_non_string_without_raising():
    """Every caller is a boundary with its own refusal to raise; a predicate
    that raised would make each of them handle two failure shapes."""
    for value in (None, 123, [], {}, object()):
        assert pk.states_something(value) is False


# ---------------------------------------------------------------------------
# GATE 1 — ContextPacket.__post_init__
# ---------------------------------------------------------------------------

def _packet(reason, posture=pk.POSTURE_REDUCED):
    now = time.time()
    return pk.ContextPacket(
        purpose="a turn", scope=ScopeKey("repo", "main", "staged", "topic"),
        posture=posture, sources=(), issued_at=now, expires_at=now + 300,
        reduced_reason=reason)


@pytest.mark.parametrize("name,value,_c,_s", BLANK_CLASSES, ids=BLANK_IDS)
def test_gate1_construction_refuses_every_blank_class(name, value, _c, _s):
    with pytest.raises(pk.PacketError) as refused:
        _packet(value)
    assert "reduction nobody can read" in str(refused.value)


@pytest.mark.parametrize("name,value", STATED_VALUES, ids=STATED_IDS)
def test_gate1_construction_accepts_every_stated_value(name, value):
    assert _packet(value).reduced_reason == value


def test_gate1_is_now_as_strict_as_the_two_fields_beside_it():
    """The inconsistency issue #263 named: `ref` and `provider_id` have refused
    blanks in this same `__post_init__` all along."""
    now = time.time()
    with pytest.raises(pk.PacketError):
        pk.PacketSource(ref="   ", kind=pk.SOURCE_EVIDENCE, text="t",
                        status=None, compression_exempt=False)
    with pytest.raises(pk.PacketError):
        pk.ContextPacket(
            purpose="p", scope=ScopeKey("r", "main", "staged", "t"),
            posture=pk.POSTURE_FULL, sources=(), issued_at=now,
            expires_at=now + 1, provider_id="   ")


# ---------------------------------------------------------------------------
# GATE 2 — serve.doxbench_context_packet
# ---------------------------------------------------------------------------

class _Packet:
    """A duck-typed packet, which is what the injected assembler seam hands in.
    Bypasses gate 1 on purpose: gate 2 must refuse on its own, not because the
    type already did."""

    def __init__(self, posture, reason):
        self.posture = posture
        self.reduced_reason = reason


@pytest.mark.parametrize("name,value,_c,_s", BLANK_CLASSES, ids=BLANK_IDS)
def test_gate2_derivation_refuses_every_blank_class(name, value, _c, _s):
    with pytest.raises(pk.PacketError) as refused:
        serve_mod.doxbench_context_packet(
            _Packet(pk.POSTURE_REDUCED, value))
    assert "reduction nobody can read" in str(refused.value)


@pytest.mark.parametrize("name,value", STATED_VALUES, ids=STATED_IDS)
def test_gate2_derivation_accepts_every_stated_value(name, value):
    record = serve_mod.doxbench_context_packet(
        _Packet(pk.POSTURE_REDUCED, value))
    assert record == {"posture": "reduced", "reduced_reason": value}


# ---------------------------------------------------------------------------
# GATE 3 — check_context_packet in the delegated validator
# ---------------------------------------------------------------------------

def _validator():
    spec = importlib.util.spec_from_file_location(
        "vidc_blank_reason",
        REPO_ROOT / "scripts" / "validate-ideation-dashboard-contracts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _gate3_findings(reason):
    """(errors, warnings) from the delegated validator.

    BOTH, because this gate deliberately does NOT refuse a blank (PR #314,
    Codex P1): it WARNS and accepts. `contract-v1.40` accepted these records,
    and `docs/contract-versioning-policy.md` makes a new validator warning
    additive while a new rejection is breaking."""
    module = _validator()
    findings = module.Findings()
    module.check_context_packet(
        findings, "probe",
        {"context_packet": {"posture": "reduced", "reduced_reason": reason}})
    return findings.errors, findings.warnings


def _gate3_errors(reason):
    return _gate3_findings(reason)[0]


@pytest.mark.parametrize("name,value,_c,_s", BLANK_CLASSES, ids=BLANK_IDS)
def test_gate3_validator_WARNS_on_every_blank_class_and_still_accepts(
        name, value, _c, _s):
    """THE PUBLISHED CONFORMANCE VALIDATOR WARNS RATHER THAN REFUSES, and that
    is the contract-versioning decision, not a weaker guard (PR #314, Codex P1).

    Its verdict on a third party's record IS the contract surface, and
    `contract-v1.40` — still the declared bundle, changelog and tag — accepted
    these records with zero errors and zero warnings. The policy's ADDITIVE
    class is "new optional fields, new contracts, NEW VALIDATOR WARNINGS";
    rejecting a previously accepted shape is the BREAKING class and may only
    land at a new major. So this warns now and errors at contract-v2.0."""
    errors, warnings = _gate3_findings(value)
    assert errors == [], (
        f"{name}: the published validator must still ACCEPT this record — "
        f"rejecting it changes what contract-v1.40 means")
    assert any("context-packet-blank" in w and "STATES its reason" in w
               for w in warnings), warnings
    assert any("contract-v2.0" in w for w in warnings), (
        "the warning must record where it becomes an error")


@pytest.mark.parametrize("name,value", STATED_VALUES, ids=STATED_IDS)
def test_gate3_validator_accepts_every_stated_value(name, value):
    assert _gate3_errors(value) == []


def test_the_validators_restatement_agrees_with_the_canonical_predicate():
    """The validator RESTATES the rule rather than importing it — a contract
    validator must not import the runtime package whose artifacts it checks, or
    a shared bug would pass both sides. That freedom is exactly what makes this
    agreement test load-bearing."""
    restated = _validator()._states_something
    for name, value, _c, _s in BLANK_CLASSES:
        assert restated(value) == pk.states_something(value) is False, name
    for name, value in STATED_VALUES:
        assert restated(value) == pk.states_something(value) is True, name
    for value in (None, 123, [], {}):
        assert restated(value) == pk.states_something(value) is False


# ---------------------------------------------------------------------------
# GATE 4 — the browser adopter, and the cross-runtime agreement
# ---------------------------------------------------------------------------

_JS_HARNESS = """
import { createChatState, beginTurn, settleTurnSuccess, NON_BLANK_REASON }
  from "./doxbench-chat-model.mjs";

const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "t" };
const recordWith = (contextPacket) => ({
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
  selected_model: { requested_model_id: "model-a", routing_rule: false,
                    data_handling: "on-tenant" },
  bound_buffer: "outline",
  observed_hashes: { outline: "d".repeat(64) },
  assistant_prose: "answer", proposals: [],
  context_packet: contextPacket });
// THE EXPORTED SURFACE, not the internal function: `adoptContextPacket` is
// module-private, and the released consumer path is `settleTurnSuccess`. Driving
// the real path is stronger anyway — it proves a blank cannot reach browser
// state, not merely that a helper would have refused it.
const adopt = (value) => settleTurnSuccess(
  beginTurn({ ...createChatState(KEY), composer: "q" }),
  recordWith({ posture: "reduced", reduced_reason: value })).contextPacket;

const CASES = JSON.parse(process.argv[2]);
const out = {};
for (const [name, value] of CASES) {
  const adopted = adopt(value);
  out[name] = { adopted: adopted != null,
                predicate: NON_BLANK_REASON.test(value) };
}
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def js_verdicts(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the browser-gate probe")
    tmp_path = tmp_path_factory.mktemp("blank-reason")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "harness.mjs"
    harness.write_text(_JS_HARNESS, encoding="utf-8")
    cases = ([[n, v] for n, v, _c, _s in BLANK_CLASSES]
             + [[n, v] for n, v in STATED_VALUES])
    proc = subprocess.run(
        [NODE, str(harness), json.dumps(cases)],
        capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


@pytest.mark.parametrize("name,value,_c,_s", BLANK_CLASSES, ids=BLANK_IDS)
def test_gate4_adopter_refuses_every_blank_class(name, value, _c, _s,
                                                 js_verdicts):
    assert js_verdicts[name]["adopted"] is False, name


@pytest.mark.parametrize("name,value", STATED_VALUES, ids=STATED_IDS)
def test_gate4_adopter_accepts_every_stated_value(name, value, js_verdicts):
    assert js_verdicts[name]["adopted"] is True, name


def test_the_two_runtimes_agree_on_every_recorded_input(js_verdicts):
    """The recorded inputs, as a fast smoke check. The real assertion is the
    full-space sweep below — nine inputs is exactly the sample size that let the
    version-skew defect through (issue #263 review, P2-1)."""
    disagreements = []
    for name, value, _c, _s in BLANK_CLASSES:
        if js_verdicts[name]["predicate"] != pk.states_something(value):
            disagreements.append((name, "blank"))
    for name, value in STATED_VALUES:
        if js_verdicts[name]["predicate"] != pk.states_something(value):
            disagreements.append((name, "stated"))
    assert disagreements == []


_SWEEP_HARNESS = """
import { readFileSync } from "node:fs";

// THE SHIPPED REGEX, read out of the module source rather than re-typed here.
// A sweep against a COPY of the rule proves the copy is fine and says nothing
// about the gate.
const src = readFileSync(process.argv[2], "utf8");
const m = src.match(/export const NON_BLANK_REASON = (\\/.*\\/u);/);
if (!m) { throw new Error("NON_BLANK_REASON not found in the shipped module"); }
const RE = eval(m[1]);

const accepted = [];
for (let cp = 0; cp < 0x110000; cp++) {
  if (cp >= 0xD800 && cp <= 0xDFFF) continue;   // lone surrogates are not text
  if (RE.test(String.fromCodePoint(cp))) accepted.push(cp);
}
process.stdout.write(JSON.stringify({ accepted, regex: m[1] }));
"""


@pytest.fixture(scope="module")
def full_space_sweep(tmp_path_factory):
    """Every code point, through the SHIPPED browser regex."""
    if NODE is None:
        pytest.skip("node not available for the full-space sweep")
    tmp_path = tmp_path_factory.mktemp("sweep")
    harness = tmp_path / "sweep.mjs"
    harness.write_text(_SWEEP_HARNESS, encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(harness), str(CHAT_MODEL_JS)],
        capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    return set(data["accepted"]), data["regex"]


def _python_accepted():
    return {cp for cp in range(0x110000)
            if not (0xD800 <= cp <= 0xDFFF)
            and pk.states_something(chr(cp))}


def test_no_code_point_is_accepted_by_the_server_and_refused_by_the_browser(
        full_space_sweep):
    """THE SAFETY PROPERTY, swept over all 1,112,064 code points.

    NOT "the runtimes agree" — they do not, and cannot, because they ship
    different Unicode tables. What must hold is that the disagreement only ever
    runs the SAFE way. A code point the server accepts and the browser refuses
    is the original bug reproduced: a reason admitted into the durable record
    that renders as nothing on the surface.

    The blank-category rule this replaced had 51 such code points — every one
    unassigned in Python's 15.0.0 and newly assigned as a combining mark in
    ICU's 16 (Arabic, Garay, Tulu-Tigalari). An exclusion rule cannot be fixed
    by naming more categories, because the next release adds more; an ADMISSION
    rule is stable by construction, since `Cn` is never L/N/P/S in any table."""
    js_accepted, _regex = full_space_sweep
    py_accepted = _python_accepted()
    bug_direction = py_accepted - js_accepted
    assert not bug_direction, (
        f"{len(bug_direction)} code point(s) the server accepts and the "
        f"browser refuses, e.g. "
        f"{[hex(c) for c in sorted(bug_direction)[:8]]}")


def test_every_residual_version_skew_is_fail_closed(full_space_sweep):
    """The other direction is ALLOWED and is expected to be non-empty: code
    points the newer runtime has assigned and the older has not. The server
    refuses them, so no record is admitted — fail-closed. Asserted so a future
    reader knows the non-zero number is the design and not a regression.

    EVERY ONE OF THEM, not a sample. This checked the first 200, which is the
    same mistake in miniature that this whole round was about: the nine-input
    agreement test was a narrow scope, and a narrow scope is exactly what hid
    the 51-code-point divergence P2-1 turned out to be. If a genuine
    disagreement ever appears at code point 900,000 — a character assigned in
    BOTH tables that the two rules classify differently — a sample of the
    lowest 200 would never see it."""
    js_accepted, _regex = full_space_sweep
    safe_direction = js_accepted - _python_accepted()
    real_disagreements = [
        cp for cp in sorted(safe_direction)
        if unicodedata.category(chr(cp)) != "Cn"]
    assert not real_disagreements, (
        f"{len(real_disagreements)} code point(s) are assigned here yet "
        f"refused by the server predicate while the browser accepts them — "
        f"that is not a version skew, it is a real disagreement: "
        f"{[(hex(c), unicodedata.category(chr(c))) for c in real_disagreements[:8]]}")


def test_the_predicate_accepts_no_unassigned_code_point():
    """What makes the rule version-stable, stated as its own assertion: nothing
    this predicate admits is unassigned, so a newer table can only ever ADD
    acceptances, never turn a blank into a stated reason."""
    accepted_unassigned = [
        cp for cp in _python_accepted()
        if unicodedata.category(chr(cp)) == "Cn"]
    assert accepted_unassigned == []


def test_the_sweep_reads_the_shipped_regex_not_a_copy(full_space_sweep):
    _js_accepted, regex = full_space_sweep
    source = CHAT_MODEL_JS.read_text(encoding="utf-8")
    assert f"export const NON_BLANK_REASON = {regex};" in source


# ---------------------------------------------------------------------------
# THE BROWSER RESTATEMENT MUST BE AN ADMISSION RULE IN ITS OWN RIGHT
#
# A GAP FOUND BY REVERT-TESTING THIS FILE'S OWN PINS, and worth stating because
# it is the subtle one: reverting the JS regex ALONE — back to the exclusion
# form, with the Python side left inverted — left every test above GREEN. The
# safety sweep still held, because everything Python admits (L/N/P/S) the
# exclusion form also admits, so the bug direction stayed empty and the
# behavioural property was genuinely satisfied.
#
# It was satisfied by accident. The exclusion form admits ~825,000 UNASSIGNED
# code points; it just happens not to admit anything Python refuses. So the
# browser would have kept the version-instability P2-1 is about — a future ICU
# assigning a new combining mark changes what it refuses — while the suite said
# the rule was safe. The pins below close that: one behavioural, one structural.
# ---------------------------------------------------------------------------

def test_the_browser_regex_admits_almost_no_unassigned_space(full_space_sweep):
    """The behavioural half. An ADMISSION rule accepts only what some table has
    assigned, so the unassigned points it accepts are exactly the ones the newer
    runtime assigned and this one has not — thousands. The EXCLUSION form
    accepts the whole unassigned plane — hundreds of thousands. Measured at the
    time of writing: 5,761 versus 825,294, a 143x gap, so the bound below is
    generous in both directions and does not need moving when a Unicode
    release shifts the numbers."""
    js_accepted, _regex = full_space_sweep
    unassigned_here = {cp for cp in range(0x110000)
                       if not (0xD800 <= cp <= 0xDFFF)
                       and unicodedata.category(chr(cp)) == "Cn"}
    admitted_unassigned = len(js_accepted & unassigned_here)
    assert admitted_unassigned < 50_000, (
        f"the browser regex admits {admitted_unassigned:,} code points that "
        f"are unassigned here — that is an EXCLUSION rule, whose refusals move "
        f"with every Unicode release (issue #263 P2-1)")


def test_the_browser_regex_is_written_as_an_admission_class(full_space_sweep):
    """The structural half, because the behavioural one is a bound and a bound
    invites a clever rule that squeaks under it. A negated class (`[^…]`) is an
    exclusion by construction whatever it lists."""
    _js_accepted, regex = full_space_sweep
    body = regex[1:regex.rindex("/")]
    assert not body.startswith("[^"), (
        f"NON_BLANK_REASON is a NEGATED class ({regex}) — the rule must name "
        f"what it ADMITS, so that an unassigned code point can never satisfy "
        f"it (issue #263 P2-1)")
    for prop in (r"\p{L}", r"\p{N}", r"\p{P}", r"\p{S}"):
        assert prop in body, (regex, prop)


# ---------------------------------------------------------------------------
# the outcome the rule exists to prevent
# ---------------------------------------------------------------------------

_RAIL_HARNESS = """
import { createChatState, beginTurn, settleTurnSuccess }
  from "./doxbench-chat-model.mjs";
import { reducedContextNote, REDUCED_CONTEXT_LEAD }
  from "./doxbench-chat.mjs";

const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "t" };
const recordWith = (contextPacket) => ({
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t", assistant_turn_id: "a", model_id: "model-a",
  selected_model: { requested_model_id: "model-a", routing_rule: false,
                    data_handling: "on-tenant" },
  bound_buffer: "outline",
  observed_hashes: { outline: "d".repeat(64) },
  assistant_prose: "answer", proposals: [],
  context_packet: contextPacket });
// THE EXPORTED SURFACE, not the internal function: `adoptContextPacket` is
// module-private, and the released consumer path is `settleTurnSuccess`. Driving
// the real path is stronger anyway — it proves a blank cannot reach browser
// state, not merely that a helper would have refused it.
const adopt = (value) => settleTurnSuccess(
  beginTurn({ ...createChatState(KEY), composer: "q" }),
  recordWith({ posture: "reduced", reduced_reason: value })).contextPacket;

const CASES = JSON.parse(process.argv[2]);
const out = {};
for (const [name, value] of CASES) {
  const adopted = adopt(value);
  const note = adopted == null ? null : reducedContextNote(adopted);
  out[name] = {
    adopted: adopted != null,
    note: note === undefined ? null : note,
    bare: typeof note === "string"
      && note.trim() === REDUCED_CONTEXT_LEAD.trim(),
  };
}
process.stdout.write(JSON.stringify(out));
"""


def test_the_rail_never_renders_a_bare_reduced_context_note(tmp_path):
    """The adopter's own forbidden outcome, asserted end to end: no blank class
    may reach the rail and produce the bare words with nothing after them."""
    if NODE is None:
        pytest.skip("node not available for the rail probe")
    chat_js = CHAT_MODEL_JS.parent / "doxbench-chat.js"
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    # The rail imports the model by its `.js` name; rewrite that to the `.mjs`
    # copy exactly as the existing view harness does, so node resolves it as a
    # module without a package.json.
    (tmp_path / "doxbench-chat.mjs").write_text(
        chat_js.read_text(encoding="utf-8").replace(
            "./doxbench-chat-model.js", "./doxbench-chat-model.mjs"),
        encoding="utf-8")
    harness = tmp_path / "rail.mjs"
    harness.write_text(_RAIL_HARNESS, encoding="utf-8")
    cases = [[n, v] for n, v, _c, _s in BLANK_CLASSES]
    proc = subprocess.run(
        [NODE, str(harness), json.dumps(cases)],
        capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    verdicts = json.loads(proc.stdout)
    for name, _v, _c, _s in BLANK_CLASSES:
        assert verdicts[name]["adopted"] is False, name
        assert verdicts[name]["note"] is None, name
        assert verdicts[name]["bare"] is False, name


# ---------------------------------------------------------------------------
# F5 — the last `str()` coercion on the posture path
# ---------------------------------------------------------------------------

def _v2_body(posture, reason):
    return serve_mod.doxbench_turn_v2_success_body(
        client_turn_id="c-1", assistant_turn_id="a-1", model_id="m",
        requested_model_id="m", routing_rule=False, data_handling="on-tenant",
        bound_buffer="document:one", observed_hashes={}, assistant_prose="p",
        context_posture=posture, context_reduced_reason=reason)


def test_f5_the_builder_no_longer_coerces_a_non_string_posture():
    """It built `{"posture": str(context_posture)}`, so a malformed value became
    a conformant-LOOKING posture — `<object object at 0x…>`, a heap address, in
    a durable record."""
    with pytest.raises(pk.PacketError) as refused:
        _v2_body(object(), None)
    assert "coerced posture is a manufactured one" in str(refused.value)


@pytest.mark.parametrize("name,value,_c,_s", BLANK_CLASSES, ids=BLANK_IDS)
def test_f5_the_builder_refuses_a_blank_reason(name, value, _c, _s):
    with pytest.raises(pk.PacketError):
        _v2_body(pk.POSTURE_REDUCED, value)


def test_f5_the_builder_carries_a_stated_reason_verbatim():
    body = _v2_body(pk.POSTURE_REDUCED, pk.REDUCED_NO_KNOWLEDGE_SERVICE)
    assert body["context_packet"] == {
        "posture": "reduced",
        "reduced_reason": pk.REDUCED_NO_KNOWLEDGE_SERVICE,
    }


def test_f5_no_str_coercion_survives_on_the_posture_path():
    """Asserted against the SOURCE, because the coercion's whole problem was
    that it was unreachable from any test that only drove valid values."""
    source = (REPO_ROOT / "scripts" / "ideation_dashboard"
              / "serve.py").read_text(encoding="utf-8")
    start = source.index("def doxbench_turn_v2_success_body(")
    end = source.index("\ndef ", start + 1)
    # CODE ONLY. The comment recording this fix necessarily QUOTES the coercion
    # it removed, so a naive substring scan over the whole body fails on the
    # documentation of its own fix — which would teach the next author to delete
    # the explanation rather than keep the guard.
    body = "\n".join(
        line for line in source[start:end].splitlines()
        if not line.lstrip().startswith("#"))
    assert "str(context_posture)" not in body
    assert "str(context_reduced_reason)" not in body


# ---------------------------------------------------------------------------
# the shipped constants, still stated everywhere (extend, never weaken)
# ---------------------------------------------------------------------------

def test_the_two_shipped_reasons_pass_every_python_gate():
    for reason in (pk.REDUCED_NO_KNOWLEDGE_SERVICE,
                   pk.REDUCED_RETRIEVAL_REFUSED):
        assert pk.states_something(reason)
        assert _packet(reason).reduced_reason == reason
        assert serve_mod.doxbench_context_packet(
            _Packet(pk.POSTURE_REDUCED, reason))["reduced_reason"] == reason
        assert _gate3_errors(reason) == []
        assert _v2_body(pk.POSTURE_REDUCED, reason)["context_packet"][
            "reduced_reason"] == reason


# ---------------------------------------------------------------------------
# P2-2 — the builder's refusals reach the wire on the ROUTE'S 400 SHAPE
#
# The builder gained refusals when its `str()` coercions went, and its call site
# sits OUTSIDE the packet boundary's `try`. So an escaping `PacketError` was a
# 500 with a traceback while the builder's own comment claimed both refusals
# stayed on one shape. Pinned END TO END, through the real route, because the
# defect was invisible to every test that only drove valid values.
# ---------------------------------------------------------------------------

def test_a_builder_refusal_answers_on_the_routes_fixed_400_shape(
        tmp_path, monkeypatch):
    """Force the builder to raise and assert the wire answer is the SAME fixed
    `invalid_turn_request` every other structural packet refusal uses — not a
    500, and not a new code."""
    # `_assert_refusal` was `_assert_v2_refusal` until contract-v3.0
    # (retire-doxbench-chat-turn-v1). Two asserters existed because a refusal is
    # answered in the family its request arrived in, and they differed in exactly
    # one clause -- the `kind`. One family survives, so the distinction is gone
    # and the twins merged under the unqualified name.
    from test_doxbench_routes import (  # noqa: E402
        _assert_refusal, _post_turn, _turn_v2,
    )

    def _raising(**_kwargs):
        raise pk.PacketError(
            "a turn record carries the reduction's reason as the packet "
            "stated it; a reduction nobody can read is a silent degradation")

    monkeypatch.setattr(serve_mod, "doxbench_turn_v2_success_body", _raising)
    status, payload, _port = _post_turn(tmp_path, _turn_v2())

    assert status == 400, (status, payload)
    # The asserter pins the surviving family's `kind` exactly, which is what
    # makes this a real check rather than a status comparison: a route answering
    # in some other envelope fails here.
    _assert_refusal(status, payload, "invalid_turn_request")


def test_the_builder_call_site_is_inside_a_packet_error_handler():
    """The structural half, asserted against the AST rather than the text: the
    call must be lexically inside a `try` that handles `PacketError`. A source
    grep would pass on a `try` that caught something else."""
    import ast

    tree = ast.parse((REPO_ROOT / "scripts" / "ideation_dashboard"
                      / "serve.py").read_text(encoding="utf-8"))
    calls = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "doxbench_turn_v2_success_body"]
    assert calls, "the builder is never called"
    for call in calls:
        handlers = [
            ast.unparse(handler.type)
            for node in ast.walk(tree) if isinstance(node, ast.Try)
            if any(call is sub for stmt in node.body
                   for sub in ast.walk(stmt))
            for handler in node.handlers if handler.type is not None
        ]
        assert any("PacketError" in h for h in handlers), (
            f"the builder call at line {call.lineno} is not inside a try that "
            f"handles PacketError; its refusals would escape as a 500")


# ---------------------------------------------------------------------------
# THE ADMISSION RULE IS STRICTLY NARROWER THAN THE BLANK CATEGORIES
#
# Named as its own behaviour (PR #314, Codex P2) rather than left for a reader
# to derive by comparing two spellings. The exclusion form the rule started as
# would have ACCEPTED all three of these.
# ---------------------------------------------------------------------------

NARROWER_THAN_EXCLUSION: tuple[tuple[str, str, str], ...] = (
    ("private use U+E000", "", "Co"),
    ("private use U+F8FF", "", "Co"),
    ("unassigned U+0897", "ࢗ", "Cn"),
)


@pytest.mark.parametrize(
    "name,value,category", NARROWER_THAN_EXCLUSION,
    ids=[n for n, _v, _c in NARROWER_THAN_EXCLUSION])
def test_the_rule_refuses_private_use_and_unassigned(name, value, category):
    """`Co`/`Cn` are refused on the same fail-closed ground as the blank
    classes: a private-use code point means nothing outside the font that
    defines it, so a reason made only of them renders as tofu for every other
    reader — the disclosure-with-nothing-in-it in a different disguise. `Cn`
    carries the version-stability property."""
    assert unicodedata.category(value) == category, name
    assert pk.states_something(value) is False, name
    # the EXCLUSION form this replaced would have accepted them, which is the
    # delta the normative text now names
    blank_cats = {"Cc", "Cf", "Mn", "Mc", "Me"}
    would_have_accepted = not (
        value.isspace() or unicodedata.category(value) in blank_cats)
    assert would_have_accepted, (
        f"{name} is not part of the admission/exclusion delta after all")


def test_surrogates_are_refused_by_the_rule():
    """`Cs` completes the delta. Not reachable as text in Python (a lone
    surrogate is not encodable), so it is asserted at the predicate."""
    assert pk.states_something("\ud800") is False


def test_every_textual_home_states_the_admission_rule():
    """One rule, four homes — and the round's own lesson is that a home stating
    the OLD rule is how the four drift apart (PR #314, Codex P2 found exactly
    that: the normative manifest text still described the exclusion form after
    the code had been inverted)."""
    homes = {
        "canonical": REPO_ROOT / "scripts" / "ideation_dashboard"
        / "doxbench_packet.py",
        "validator": REPO_ROOT / "scripts"
        / "validate-ideation-dashboard-contracts.py",
        "browser": CHAT_MODEL_JS,
        "manifest": REPO_ROOT / "contracts" / "manifest.yaml",
    }
    stale = "at least one character outside"
    for label, path in homes.items():
        text = path.read_text(encoding="utf-8")
        assert ("L* ∪ N* ∪ P* ∪ S*" in text or "L* | N* | P* | S*" in text), (
            f"{label} does not state the admission rule")
        # AND THE OLD FORM IS NOT STATED AS CURRENT. Presence alone is not
        # enough: a home carrying BOTH statements reads as ambiguous to the
        # next author, and ambiguity is how four homes drift. The exclusion
        # form may appear only as HISTORY, which every home spells with a
        # past-tense marker rather than as a definition of the rule.
        assert stale not in text, (
            f"{label} still states the exclusion form as the current rule "
            f"({stale!r}); it may appear only as recorded history")


# ---------------------------------------------------------------------------
# THE VALIDATOR'S TWO ARMS, SPLIT ON EXACTLY WHAT contract-v1.40 REFUSED
#
# Found by the packaged-negative suite when the first version of the P1 fix
# collapsed them: ONE predicate had served both the pairing rule and the blank
# rule, so downgrading it to a warning silently downgraded the PAIRING — and
# that rule shipped as an error WITH v1.40, where this one did not.
# ---------------------------------------------------------------------------

V140_ERRORED: tuple[tuple[str, dict], ...] = (
    ("missing key", {"posture": "reduced"}),
    ("explicit null", {"posture": "reduced", "reduced_reason": None}),
    ("empty string", {"posture": "reduced", "reduced_reason": ""}),
)


@pytest.mark.parametrize("name,packet", V140_ERRORED,
                         ids=[n for n, _p in V140_ERRORED])
def test_the_pairing_rule_is_still_an_error(name, packet):
    """`not reason` was contract-v1.40's own predicate and it ERRORED. Those
    verdicts are unchanged: keeping them is not a new rejection, and relaxing
    them would weaken a rule the release ratified."""
    module = _validator()
    findings = module.Findings()
    module.check_context_packet(findings, "probe", {"context_packet": packet})
    assert any("context-packet]" in e or "[context-packet]" in e
               for e in findings.errors), (name, findings.errors)


def test_no_record_contract_v140_accepted_is_now_rejected():
    """THE ADDITIVE PROPERTY, asserted directly rather than argued in prose.

    A record the published version accepted must still be accepted; the most a
    new rule may do on the published major is warn. This is the whole of
    Codex's P1 on PR #314, turned into a check."""
    module = _validator()
    # DERIVED from the shared matrix rather than retyped: a literal
    # control character does not survive being written by hand, and an
    # empty string is NOT in this list — contract-v1.40 errored on that.
    accepted_at_v140 = [value for _n, value, _c, _s in BLANK_CLASSES] + [
        pk.REDUCED_NO_KNOWLEDGE_SERVICE, "漢字",
    ]
    for reason in accepted_at_v140:
        findings = module.Findings()
        module.check_context_packet(
            findings, "probe",
            {"context_packet": {"posture": "reduced",
                                "reduced_reason": reason}})
        assert findings.errors == [], (
            f"reduced_reason={reason!r} was ACCEPTED at contract-v1.40 and is "
            f"now rejected — that is a breaking change on a published minor")
