"""Deterministic per-document completeness + staged-topic health
(openxFactory `add-staging-workbench`, change tasks 2.1-2.7; design D1/D2/D8).

The scoring family's non-negotiables:

  * DETERMINISM. Two generations over an unchanged tree yield byte-identical
    `completeness` and `health` objects; every emitted number carries the fixed
    precision, and the `score` is recomputable from the emitted signal values
    with the pinned weights — so a rendered bar is explainable and a
    cross-platform snapshot diff stays empty.
  * MONOTONICITY. A document that gains expected sections and gains edges scores
    STRICTLY higher; a topic whose last open marker closes and whose documents
    cross the threshold flips to `ready`; an empty topic folder is `stub`.
  * SCOPE. Health reads the topic FOLDER's corpus documents ONLY — a document
    that merely declares the topic as a destination contributes nothing — and an
    EXCLUDED document carries no completeness at all.
  * THE GATING BOUND. Outside the tests, the scoring module's only importers are
    the generator and the propose route's readiness guard; no doc-health or
    readiness path imports it.
"""

from __future__ import annotations

import ast
import re
import shutil
from pathlib import Path

from conftest import (  # noqa: F401  (sys.path side effect)
    BASE_REPO, PINNED_REVISION, FakeGit, REPO_ROOT, staging_fragment, thin_fragment,
)

from doc_health import corpus
from ideation_dashboard import authoring, snapshot
from ideation_dashboard import completeness as C
from ideation_dashboard.generator import generate_snapshot, live_topic_health

SCRIPTS = REPO_ROOT / "scripts"


def _tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(BASE_REPO, root)
    return root


def _snap(root: Path = BASE_REPO) -> dict:
    return generate_snapshot(root, "fixture-repo", source_revision=PINNED_REVISION,
                             git=FakeGit())


def _docs(snap: dict) -> dict[str, dict]:
    return {d["id"]: d for d in snap["documents"]}


def _topics(snap: dict) -> dict[str, dict]:
    return {t["staging_id"]: t for t in snap["staged_topics"]}


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ============================================================================
# the contract constants (design D2 — fixed, never a per-run input)
# ============================================================================

def test_weights_are_fixed_constants_summing_to_one():
    assert set(C.WEIGHTS) == {"structure", "length", "open_markers",
                              "keyword_coverage", "link_degree"}
    assert C.SIGNAL_NAMES == tuple(C.WEIGHTS)
    assert round(sum(C.WEIGHTS.values()), 10) == 1.0
    # the v1 ready bar (Brett's 2026-07-25 ruling)
    assert C.READY_MIN_SCORE == 0.60
    assert C.PRECISION == 4


def test_the_governance_header_contract_matches_the_shared_definition():
    # The scoring module restates the header block to keep its import graph free
    # of anything that touches the filesystem; the restatement must not drift.
    assert C.GOVERNANCE_HEADER_FIELDS == authoring.REQUIRED_HEADER_FIELDS
    assert C.HEADER_WINDOW == corpus.STATUS_SCAN_LINES


def test_the_governance_header_contract_agrees_on_an_exotic_header_too():
    """Finding F4: the constants-only check above passes even if the two
    RULES for reading them disagree — it never runs either reader over any
    document. `authoring.missing_required_headers` and `completeness`'s
    `governance_header_block` element used to disagree on exactly this
    shape: a header field pushed past the OLD pseudo-line window by an
    exotic separator, while sitting plainly inside the real 15-line window
    `authoring` (already fixed) reads correctly. Demonstrated: `authoring`
    said the header block was COMPLETE while `completeness` said
    `governance_header_block` was ABSENT, on the SAME document.
    """
    exotic = "\x0b\x0c\x1c\x1d\x1e\x85" + chr(0x2028) + chr(0x2029)
    noise = "".join(f"seg{i}{c}" for i, c in enumerate(exotic * 2))
    text = (
        "# Staged: x\n"
        f"{noise}tail\n"
        "Status: staged\n"
        "Kind: policy\n"
        "Summary: a summary\n"
        "Topics: x\n"
        "Repository context: none\n"
        "Captured: 2026-08-19\n"
    )
    # Sanity: the fixture actually overruns the OLD pseudo-line window while
    # fitting the real one, or it pins nothing.
    real_line_count = len(corpus.split_keepends(text))
    pseudo_line_count = len(text.splitlines())
    assert real_line_count <= C.HEADER_WINDOW
    assert pseudo_line_count > C.HEADER_WINDOW

    assert authoring.missing_required_headers(text) == []
    prepared = C._Prepared(text)
    assert C.ELEMENT_CHECKS["governance_header_block"](prepared) is True


def test_mutation_reverting_prepared_lines_alone_reproduces_the_f4_divergence():
    """MUTATION CHECK: reverting `_Prepared.lines` alone to
    `text.splitlines()`, with `authoring.missing_required_headers` left as
    this change fixed it, must reproduce the exact F4 divergence — authoring
    says COMPLETE, completeness says `governance_header_block` ABSENT —
    proving the test above is pinned to the defect, not passing by
    accident."""
    exotic = "\x0b\x0c\x1c\x1d\x1e\x85" + chr(0x2028) + chr(0x2029)
    noise = "".join(f"seg{i}{c}" for i, c in enumerate(exotic * 2))
    text = (
        "# Staged: x\n"
        f"{noise}tail\n"
        "Status: staged\n"
        "Kind: policy\n"
        "Summary: a summary\n"
        "Topics: x\n"
        "Repository context: none\n"
        "Captured: 2026-08-19\n"
    )
    assert authoring.missing_required_headers(text) == []

    reverted = C._Prepared.__new__(C._Prepared)
    reverted.text = text
    reverted.lines = text.splitlines()
    reverted.body_words = C._body_word_count(reverted.lines)

    assert C.ELEMENT_CHECKS["governance_header_block"](reverted) is False, (
        "reverting _Prepared.lines to splitlines() did not reproduce the "
        "false ABSENT reading — the test above is not pinned to this defect")


def test_the_expected_structure_sets_live_in_one_table_with_a_common_fallback():
    # ONE table (task 2.2): the fallback is its `None` entry, every kind's set is
    # a superset of the common three, and every named element has a predicate.
    fallback = C.STRUCTURE_ELEMENTS[None]
    assert fallback == ("h1_title", "governance_header_block", "section")
    for kind, elements in C.STRUCTURE_ELEMENTS.items():
        assert set(fallback) <= set(elements), kind
        for name in elements:
            assert name in C.ELEMENT_CHECKS, (kind, name)
    # an unlisted / absent Kind falls back
    assert C.expected_elements("no-such-kind") == fallback
    assert C.expected_elements(None) == fallback
    assert C.expected_elements("  Staging-Packet  ") == C.STRUCTURE_ELEMENTS["staging-packet"]


def test_the_scoring_module_touches_nothing_outside_its_arguments():
    # Purity is structural (design D1), so assert it on the parsed module rather
    # than on prose: `re`, typing, and `doc_health.lines` (added
    # align-status-reader-to-real-lines, finding F4) are the ONLY imports — no
    # filesystem, no clock, no network, no randomness, no model call — and no
    # builtin escape hatch is called either. `doc_health.lines` is admitted
    # specifically because IT is itself pure by the same standard (asserted
    # below, not assumed): it imports only `re`, and defines no I/O.
    tree = ast.parse((SCRIPTS / "ideation_dashboard" / "completeness.py").read_text("utf-8"))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module or "")
    assert modules == {"__future__", "re", "collections.abc", "typing",
                       "doc_health.lines"}, modules
    called = {node.func.id for node in ast.walk(tree)
              if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert not called & {"open", "eval", "exec", "input", "print", "compile"}, called

    lines_tree = ast.parse((SCRIPTS / "doc_health" / "lines.py").read_text("utf-8"))
    lines_modules: set[str] = set()
    for node in ast.walk(lines_tree):
        if isinstance(node, ast.Import):
            lines_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            lines_modules.add(node.module or "")
    assert lines_modules == {"__future__", "re"}, lines_modules


# ============================================================================
# the five signals: normalized value beside the raw count
# ============================================================================

def test_every_signal_reports_a_normalized_value_beside_its_raw_count():
    comp = _docs(_snap())["ideation/brainstorm/doc-health-checks.md"]["completeness"]
    assert set(comp) == {"score", *C.SIGNAL_NAMES}
    for name in C.SIGNAL_NAMES:
        signal = comp[name]
        assert set(signal) == {"value", "count"}
        assert 0.0 <= signal["value"] <= 1.0
        assert isinstance(signal["count"], int) and signal["count"] >= 0


def test_score_is_the_pinned_weighted_combination_of_the_emitted_values():
    for doc in _snap()["documents"]:
        comp = doc["completeness"]
        recomputed = round(sum(C.WEIGHTS[n] * comp[n]["value"] for n in C.SIGNAL_NAMES),
                           C.PRECISION)
        assert comp["score"] == recomputed, doc["id"]


def test_every_emitted_number_carries_the_fixed_precision():
    snap = _snap()
    numbers: list[float] = []
    for doc in snap["documents"]:
        comp = doc["completeness"]
        numbers.append(comp["score"])
        numbers.extend(comp[n]["value"] for n in C.SIGNAL_NAMES)
    for topic in snap["staged_topics"]:
        health = topic["health"]
        numbers.extend([health["doc_score_min"], health["doc_score_mean"]])
        numbers.extend(b["score"] for b in health["blockers"] if "score" in b)
    for value in numbers:
        # fixed precision is what keeps the rendered JSON byte-identical across
        # platforms: every number is already rounded, so re-rounding is a no-op.
        assert round(value, C.PRECISION) == value
        assert len(repr(value).partition(".")[2]) <= C.PRECISION, repr(value)


def test_structure_counts_expected_elements_per_kind():
    common = C.structure("# T\n\nprose\n")               # h1 only
    assert common == {"value": round(1 / 3, C.PRECISION), "count": 1}
    packet = C.structure(thin_fragment("T", "topic-x"), "staging-packet")
    assert packet["count"] == 2  # h1 + governance header block, no sections
    full = C.structure(staging_fragment("T", "topic-x"), "staging-packet")
    assert full == {"value": 1.0, "count": 7}


def test_length_saturates_so_padding_cannot_outscore_substance():
    body = "# T\n\n" + ("word " * (C.LENGTH_SATURATION_WORDS * 3))
    saturated = C.length(body)
    assert saturated["value"] == 1.0
    assert saturated["count"] == C.LENGTH_SATURATION_WORDS * 3  # raw count still honest
    half = C.length("# T\n\n" + ("word " * (C.LENGTH_SATURATION_WORDS // 2)))
    assert half["value"] == 0.5


def test_length_measures_the_body_not_the_governance_header_block():
    assert C.length(thin_fragment("T", "topic-x"))["count"] == 9


def test_open_markers_is_an_inverse_signal_saturating_at_zero():
    clean = C.open_markers("# T\n\nnothing standing here.\n")
    assert clean == {"value": 1.0, "count": 0}
    values = []
    for n in range(1, C.OPEN_MARKER_SATURATION + 2):
        text = "# T\n\n" + "".join(f"- TODO item {i}\n" for i in range(n))
        signal = C.open_markers(text)
        assert signal["count"] == n
        values.append(signal["value"])
    assert values == sorted(values, reverse=True)          # more markers, lower value
    assert values[C.OPEN_MARKER_SATURATION - 1] == 0.0     # bottoms out, never negative
    assert values[-1] == 0.0


def test_every_marker_token_counts():
    text = "# T\n\nTODO one. TBD two. FIXME three. And an open ?? four.\n"
    assert C.open_markers(text)["count"] == 4


def test_an_unresolved_open_question_section_counts_its_standing_items():
    assert C.open_markers(staging_fragment("T", "t", resolved=False))["count"] == 2
    # a prose section with no enumerated items is ONE standing item
    assert C.open_markers("# T\n\n## Open questions\n\nStill thinking.\n")["count"] == 1


def test_a_resolved_open_question_section_carries_no_standing_items():
    # convention 1 — the heading declares the resolution (the corpus's own form)
    assert C.open_markers(staging_fragment("T", "t", resolved=True))["count"] == 0
    # convention 2 — per-item UPPERCASE resolution
    per_item = ("# T\n\n## Open questions\n\n"
                "1. **First.** RESOLVED by the 2026-07-25 ruling.\n"
                "2. **Second.** RESOLVED — see above.\n")
    assert C.open_markers(per_item)["count"] == 0
    # ...and lowercase prose never closes a question: an open question routinely
    # says "resolved" about something else.
    prose = ("# T\n\n## Open questions\n\n"
             "1. **Sync or a pre-session attestation resolved before release?**\n")
    assert C.open_markers(prose)["count"] == 1


def test_keyword_coverage_resolves_declared_topics_against_the_vocabulary():
    assert C.keyword_coverage(["a", "b"], {"a", "b"}) == {"value": 1.0, "count": 2}
    assert C.keyword_coverage(["a", "b"], {"a"}) == {"value": 0.5, "count": 1}
    # a document declaring no topics joins no vocabulary and scores 0, never a
    # vacuous 1.0
    assert C.keyword_coverage([], {"a"}) == {"value": 0.0, "count": 0}


def test_link_degree_counts_cluster_edges_plus_destinations():
    signal = C.link_degree(["a", "b", "unknown"],
                           {"staged_topics": ["s"], "changes": ["c1", "c2"],
                            "capabilities": ["cap"]},
                           {"a", "b"})
    assert signal["count"] == 6  # 2 resolved topics + 4 destination refs
    assert signal["value"] == 1.0
    assert C.link_degree(["a"], None, {"a"})["count"] == 1


# ============================================================================
# determinism + monotonicity through the real generator
# ============================================================================

def test_two_runs_over_an_unchanged_tree_are_byte_identical_for_scores_and_health():
    first, second = _snap(), _snap()
    assert ([d["completeness"] for d in first["documents"]]
            == [d["completeness"] for d in second["documents"]])
    assert ([t["health"] for t in first["staged_topics"]]
            == [t["health"] for t in second["staged_topics"]])
    assert snapshot.canonical_bytes(first) == snapshot.canonical_bytes(second)


def test_a_document_gaining_sections_and_edges_scores_strictly_higher(tmp_path):
    root = _tree(tmp_path)
    rel = "ideation/brainstorm/legacy-note.md"
    before = _docs(_snap(root))[rel]["completeness"]

    text = (root / rel).read_text("utf-8")
    grown = (text.replace("Topics: ideation-dashboard",
                          "Topics: ideation-dashboard, doc-health")
             + "\n## Notes\n\nA section this document did not have before.\n")
    _write(root, rel, grown)
    after = _docs(_snap(root))[rel]["completeness"]

    assert after["structure"]["value"] > before["structure"]["value"]
    assert after["link_degree"]["count"] > before["link_degree"]["count"]
    assert after["score"] > before["score"]


def test_an_excluded_document_carries_no_completeness(tmp_path):
    root = _tree(tmp_path)
    _write(root, "ideation/brainstorm/headerless.md", "# No Status Header\n\nprose\n")
    excluded: list[dict[str, str]] = []
    snap = generate_snapshot(root, "fixture-repo", source_revision=PINNED_REVISION,
                             git=FakeGit(), excluded_documents=excluded)
    assert [e["path"] for e in excluded] == ["ideation/brainstorm/headerless.md"]
    assert "ideation/brainstorm/headerless.md" not in _docs(snap)
    # and no dangling score survives the exclusion
    assert all("completeness" in d for d in snap["documents"])


# ============================================================================
# staged-topic health (design D8)
# ============================================================================

def test_health_is_emitted_for_every_staged_topic_with_a_derived_status():
    for topic in _snap()["staged_topics"]:
        health = topic["health"]
        assert set(health) == {"standing_open_items", "doc_score_min",
                              "doc_score_mean", "blockers", "status"}
        assert health["status"] in (C.STATUS_READY, C.STATUS_DEVELOPING, C.STATUS_STUB)
        # status is DERIVED from the blockers, never scored directly
        if health["status"] == C.STATUS_READY:
            assert health["blockers"] == []
        else:
            assert health["blockers"] or health["status"] == C.STATUS_STUB


def test_an_empty_topic_folder_reports_stub(tmp_path):
    root = _tree(tmp_path)
    (root / "ideation" / "staging" / "empty-topic").mkdir(parents=True)
    health = _topics(_snap(root))["empty-topic"]["health"]
    assert health["status"] == C.STATUS_STUB
    assert health["blockers"] == []
    assert health["standing_open_items"] == 0
    assert health["doc_score_min"] == 0.0 and health["doc_score_mean"] == 0.0
    # a folder whose only files are not corpus documents is a stub too
    (root / "ideation" / "staging" / "empty-topic" / "notes.txt").write_text("x", "utf-8")
    assert _topics(_snap(root))["empty-topic"]["health"]["status"] == C.STATUS_STUB


def test_a_topic_flips_to_ready_when_its_last_open_marker_closes(tmp_path):
    root = _tree(tmp_path)
    rel = "ideation/staging/gate-topic/gate-topic.md"
    _write(root, rel, staging_fragment("Gate Topic", "gate-topic", resolved=False))
    blocked = _topics(_snap(root))["gate-topic"]["health"]
    assert blocked["status"] == C.STATUS_DEVELOPING
    assert blocked["standing_open_items"] == 2
    assert blocked["blockers"] == [{"kind": C.BLOCKER_STANDING_OPEN_ITEMS,
                                    "document": rel, "count": 2}]

    _write(root, rel, staging_fragment("Gate Topic", "gate-topic", resolved=True))
    ready = _topics(_snap(root))["gate-topic"]["health"]
    assert ready["status"] == C.STATUS_READY
    assert ready["blockers"] == []
    assert ready["standing_open_items"] == 0
    assert ready["doc_score_min"] >= C.READY_MIN_SCORE


def test_an_underdone_document_blocks_on_its_score_against_the_constant(tmp_path):
    root = _tree(tmp_path)
    rel = "ideation/staging/thin-topic/thin-topic.md"
    _write(root, rel, thin_fragment("Thin Topic", "thin-topic"))
    health = _topics(_snap(root))["thin-topic"]["health"]
    assert health["standing_open_items"] == 0            # every question closed
    assert health["status"] == C.STATUS_DEVELOPING
    assert health["blockers"] == [{"kind": C.BLOCKER_BELOW_READY_THRESHOLD,
                                   "document": rel,
                                   "score": health["doc_score_min"],
                                   "threshold": C.READY_MIN_SCORE}]
    assert health["doc_score_min"] < C.READY_MIN_SCORE


def test_health_reads_the_topic_folder_only_not_documents_declaring_it(tmp_path):
    root = _tree(tmp_path)
    _write(root, "ideation/staging/gate-topic/gate-topic.md",
           staging_fragment("Gate Topic", "gate-topic"))
    assert _topics(_snap(root))["gate-topic"]["health"]["status"] == C.STATUS_READY

    # an unfinished upstream note that names the topic as a destination is
    # inbound CONTEXT — its doneness is its own topic's business (design D8), so
    # the finished fragment stays ready.
    _write(root, "ideation/staging/other-topic/upstream.md",
           staging_fragment("Upstream", "gate-topic", resolved=False,
                            markers=("TODO — still working this out.",)))
    after = _topics(_snap(root))
    assert after["gate-topic"]["health"]["status"] == C.STATUS_READY
    assert after["other-topic"]["health"]["status"] == C.STATUS_DEVELOPING


def test_health_aggregates_min_mean_and_standing_items_across_member_docs(tmp_path):
    root = _tree(tmp_path)
    _write(root, "ideation/staging/mixed/one.md",
           staging_fragment("One", "mixed", markers=("TODO — one.",)))
    _write(root, "ideation/staging/mixed/two.md", thin_fragment("Two", "mixed"))
    docs = _docs(_snap(root))
    health = _topics(_snap(root))["mixed"]["health"]
    scores = [docs["ideation/staging/mixed/one.md"]["completeness"]["score"],
              docs["ideation/staging/mixed/two.md"]["completeness"]["score"]]
    assert health["standing_open_items"] == 1
    assert health["doc_score_min"] == round(min(scores), C.PRECISION)
    assert health["doc_score_mean"] == round(sum(scores) / 2, C.PRECISION)
    # blockers are typed and grouped: standing items first, then the threshold
    assert [b["kind"] for b in health["blockers"]] == [
        C.BLOCKER_STANDING_OPEN_ITEMS, C.BLOCKER_BELOW_READY_THRESHOLD]


def test_topic_health_of_no_documents_is_a_stub_without_any_io():
    # the pure function, called with nothing: no folder, no read, no clock
    assert C.topic_health([]) == {"standing_open_items": 0, "doc_score_min": 0.0,
                                  "doc_score_mean": 0.0, "blockers": [],
                                  "status": C.STATUS_STUB}


def test_blockers_render_as_concrete_actionable_clauses():
    health = C.topic_health([
        {"id": "a.md", "completeness": {"score": 0.9,
                                        "open_markers": {"value": 0.6, "count": 2}}},
        {"id": "b.md", "completeness": {"score": 0.42,
                                        "open_markers": {"value": 1.0, "count": 0}}},
    ])
    assert health["status"] == C.STATUS_DEVELOPING
    reason = C.refusal_reason(health)
    assert "a.md carries 2 standing open items" in reason
    assert f"b.md scores 0.42 below READY_MIN_SCORE {C.READY_MIN_SCORE}" in reason
    assert C.refusal_reason(C.topic_health([])) == \
        "the topic folder carries no corpus documents"
    singular = C.blocker_sentence({"kind": C.BLOCKER_STANDING_OPEN_ITEMS,
                                   "document": "a.md", "count": 1})
    assert singular == "a.md carries 1 standing open item"


def test_live_health_agrees_with_the_snapshot_over_the_same_tree(tmp_path):
    # the gate's live evaluation and the rendered health are ONE computation
    # (design D9) — same module, same functions, different vintage of the tree.
    root = _tree(tmp_path)
    _write(root, "ideation/staging/gate-topic/gate-topic.md",
           staging_fragment("Gate Topic", "gate-topic"))
    assert (live_topic_health(root, "gate-topic")
            == _topics(_snap(root))["gate-topic"]["health"])
    assert live_topic_health(root, "no-such-topic")["status"] == C.STATUS_STUB


# ============================================================================
# the gating bound (task 2.7)
# ============================================================================

def test_the_scoring_modules_only_importers_are_the_generator_and_the_guard():
    import_re = re.compile(
        r"(?m)^\s*(?:from\s+\.?\S*\s+import\s+[^\n]*\bcompleteness\b"
        r"|from\s+\.completeness\s+import\b"
        r"|import\s+\S*\bcompleteness\b)")
    importers = sorted(
        p.relative_to(SCRIPTS).as_posix()
        for p in SCRIPTS.rglob("*.py")
        if p.name != "completeness.py" and import_re.search(p.read_text("utf-8")))
    assert importers == ["ideation_dashboard/generator.py",
                         "ideation_dashboard/kickoff.py"], importers
    # ...and no doc-health / readiness path consults the score at all: the
    # per-document signal produces no finding and feeds no readiness tier.
    for module in sorted((SCRIPTS / "doc_health").rglob("*.py")):
        text = module.read_text("utf-8")
        assert not import_re.search(text), module
        assert "topic_health" not in text and "READY_MIN_SCORE" not in text, module
