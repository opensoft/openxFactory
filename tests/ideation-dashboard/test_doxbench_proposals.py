"""T058 (US3): proposal review state — review, reject, current Apply, stale
refusal, comparison, and the ABSENCE of any force-apply path — in the pure
chat model (T062, doxbench-chat-model.js).

Per-target independence is the load-bearing rule (FR-026..FR-029): the
outline and document proposals carry their own current/stale/rejected/applied
statuses; acting on one never disturbs the other. Staleness is derived by
EXACT hash comparison against the CURRENT buffer identity, recomputed on
every buffer edit event; the only recovery from stale is a NEW TURN — no
merge, no force-apply, anywhere.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")
CHAT_MODEL_JS = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" /
                 "views" / "doxbench-chat-model.js")

_HARNESS = """
import { createChatState, adoptCatalog, selectModel, editComposer, beginTurn,
         settleTurnSuccess, proposalsOf, refreshProposalCurrency,
         rejectProposal, markProposalApplied }
  from "./doxbench-chat-model.mjs";

const out = {};
const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "ideation-governance" };
const OUTLINE_HASH = "a".repeat(64);
const DOCUMENT_HASH = "b".repeat(64);
const HASHES = { outline: OUTLINE_HASH, document: DOCUMENT_HASH };
const proposal = (target, base) => ({
  target, base_hash: base, summary: "Rework the " + target,
  content: "# New " + target });
// Re-expressed in the surviving family at contract-v3.0
// (retire-doxbench-chat-turn-v1). `outline` and `document` were v1's two fixed
// `observed_hashes` keys and its two proposal-target enum values; they are
// RESERVED BUFFER KEYS in this family, so the fixture's shape survives the
// conversion untouched and the per-target independence these tests measure is
// measured over the same two targets. `selected_model` and `bound_buffer` are
// carried because the released record REQUIRES them — the model under test
// reads neither, and a fixture that omitted a required field would be a record
// no serve could have produced.
const successWith = (proposals) => ({
  schema_version: 1, kind: "workbench-chat-turn-v2-success",
  client_turn_id: "t-1", assistant_turn_id: "a-1", model_id: "model-a",
  selected_model: { requested_model_id: "model-a", routing_rule: false,
                    data_handling: "on-tenant" },
  bound_buffer: "document",
  observed_hashes: { outline: OUTLINE_HASH, document: DOCUMENT_HASH },
  assistant_prose: "with proposals", proposals });

const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
  models: [{ model_id: "model-a", label: "Approved", provider_class: "on-tenant",
             available: true, input_limit_bytes: 800000,
             output_limit_bytes: 900000, data_handling: "on-tenant" }] };
const base = editComposer(selectModel(
  adoptCatalog(createChatState(KEY), ENVELOPE), "model-a"), "go");

// review: both targets adopted independently, CURRENT against live hashes
let s = settleTurnSuccess(beginTurn(base), successWith([
  proposal("outline", OUTLINE_HASH), proposal("document", DOCUMENT_HASH)]));
s = refreshProposalCurrency(s, HASHES);
const p0 = proposalsOf(s);
out.review = { outline: p0.outline.status, document: p0.document.status,
               summaries: [p0.outline.summary, p0.document.summary],
               frozen: Object.isFrozen(p0) && Object.isFrozen(p0.outline) };

// prose-only: no proposal records at all
const prose = settleTurnSuccess(beginTurn(base), successWith([]));
const pp = proposalsOf(prose);
out.proseOnly = { keys: Object.keys(pp) };

// comparison: an edited outline flips ONLY the outline proposal to stale,
// and restoring the content flips it back
const edited = refreshProposalCurrency(s, { outline: "e".repeat(64),
                                            document: DOCUMENT_HASH });
const pe = proposalsOf(edited);
const restored = refreshProposalCurrency(edited, HASHES);
out.comparison = { outline: pe.outline.status, document: pe.document.status,
                   restoredOutline: proposalsOf(restored).outline.status };

// stale refusal: applying a stale proposal returns the IDENTICAL state
const staleApply = markProposalApplied(edited, "outline");
out.staleRefused = staleApply === edited;

// current Apply: applied on one target; the other is untouched; a repeat
// apply refuses; rejected stays rejected through a currency refresh
const applied = markProposalApplied(s, "outline");
const pa = proposalsOf(applied);
out.applied = { outline: pa.outline.status, document: pa.document.status,
                repeatRefused: markProposalApplied(applied, "outline") === applied };
const rejected = rejectProposal(s, "document");
const pr = proposalsOf(refreshProposalCurrency(rejected, HASHES));
out.rejected = { document: pr.document.status, outline: pr.outline.status };

// applied/rejected are TERMINAL for currency: edits never resurrect them
const appliedThenEdited = refreshProposalCurrency(applied,
  { outline: "f".repeat(64), document: DOCUMENT_HASH });
out.terminal = proposalsOf(appliedThenEdited).outline.status;

// new-turn recovery: the next success REPLACES the proposal set entirely
const nextTurn = settleTurnSuccess(beginTurn(editComposer(edited, "again")),
  successWith([proposal("outline", "e".repeat(64))]));
const pn = proposalsOf(refreshProposalCurrency(nextTurn,
  { outline: "e".repeat(64), document: DOCUMENT_HASH }));
out.newTurn = { outline: pn.outline.status, keys: Object.keys(pn) };
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def proposal_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench proposal-state probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-proposals")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "proposals-harness.mjs"
    harness.write_text(_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_review_adopts_both_targets_independently_and_frozen(proposal_results):
    r = proposal_results["review"]
    assert r["outline"] == "current"
    assert r["document"] == "current"
    assert r["summaries"] == ["Rework the outline", "Rework the document"]
    assert r["frozen"] is True


def test_a_prose_only_turn_carries_no_proposal_records(proposal_results):
    """RE-PINNED at contract-v1.34 (add-doxbench-editing-phase-b §13): the
    proposal map is KEYED BY BUFFER KEY now, so "no proposal" is an ABSENT key
    rather than two fixed names holding null. It has to be: the target set is the
    turn's own buffer set, and a map pre-seeded with two names could not carry a
    proposal against the third document a human loaded."""
    assert proposal_results["proseOnly"]["keys"] == []


def test_currency_is_exact_per_target_hash_comparison_and_reversible(proposal_results):
    c = proposal_results["comparison"]
    assert c["outline"] == "stale"
    assert c["document"] == "current"
    assert c["restoredOutline"] == "current"


def test_a_stale_proposal_refuses_apply_with_the_identical_state(proposal_results):
    assert proposal_results["staleRefused"] is True


def test_current_apply_is_per_target_and_never_repeats(proposal_results):
    a = proposal_results["applied"]
    assert a["outline"] == "applied"
    assert a["document"] == "current"
    assert a["repeatRefused"] is True


def test_reject_is_terminal_and_leaves_the_sibling_untouched(proposal_results):
    r = proposal_results["rejected"]
    assert r["document"] == "rejected"
    assert r["outline"] == "current"


def test_applied_is_terminal_for_currency_refreshes(proposal_results):
    assert proposal_results["terminal"] == "applied"


def test_a_new_turn_replaces_the_proposal_set_entirely(proposal_results):
    """RE-PINNED with the keyed map: the previous turn's document proposal is
    GONE from the set rather than nulled in place, which is the same fact stated
    over keys the turn actually carried."""
    n = proposal_results["newTurn"]
    assert n["outline"] == "current"
    assert n["keys"] == ["outline"]


def test_no_force_apply_or_merge_path_exists_in_the_source():
    source = CHAT_MODEL_JS.read_text(encoding="utf-8")
    for forbidden in ("forceApply", "applyStale", "mergeProposal",
                      "overrideStale"):
        assert forbidden not in source, forbidden
