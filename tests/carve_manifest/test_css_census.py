"""`scripts/measure_opendox_css_census.py` — RULED Q7's measurement, EXECUTED.

The tool decides WHICH STYLESHEET BLOCKS LEAVE openDox's bundle for the
bindings that own them (RULED Q7, `opensoft/openxFactory#656` comment
`5648049748`), and the manifest's own `web/styles.css` row cites it as the
reason its 89 declared lines are the lines they are. A measurement the floor
leans on and nothing executes is the defect § 2's re-derivation tests exist for,
one directory over (Copilot review of openxFactory #1068, round 3).

FIXTURES, NOT THE TWO LEGS. This repository carries neither `openDox-code` nor
`openXdox-code`, so a test that pointed the tool at them would be a skip on
every run here. What is asserted instead is the tool's DECISION RULE, on
stylesheets and modules small enough to read: the CSS block parser, the
class-bearing scan, the concatenation-prefix rule that `STYLE_RESIDUE`'s own
`51` was three short without, and — the one that matters most — the ASYMMETRY
between the two sides of the extraction decision.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "measure_opendox_css_census.py"


def _module():
    spec = importlib.util.spec_from_file_location("opendox_css_census", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CENSUS = _module()


def _tree(tmp_path: Path, styles: str, own: dict[str, str],
          gate: dict[str, str], index: str = "<html></html>") -> tuple[Path, Path]:
    """A two-leg fixture: openDox's bundle, and openXdox's contributed modules."""
    web = tmp_path / "dox" / "src" / "opendox" / "web"
    (web / "views").mkdir(parents=True)
    (web / "styles.css").write_text(styles, encoding="utf-8")
    (web / "app.js").write_text("// shell\n", encoding="utf-8")
    (web / "index.html").write_text(index, encoding="utf-8")
    for name, source in own.items():
        (web / "views" / name).write_text(source, encoding="utf-8")
    views = tmp_path / "xdox" / "src" / "openxdox" / "web" / "views"
    views.mkdir(parents=True)
    for name, source in gate.items():
        (views / name).write_text(source, encoding="utf-8")
    return tmp_path / "dox", tmp_path / "xdox"


def _run(dox: Path, xdox: Path, out: Path) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(dox), str(xdox), "--json", str(out)],
        capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, proc.stderr
    return json.loads(out.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# The parser.
# ---------------------------------------------------------------------------

def test_the_block_parser_reports_a_rules_own_extent_and_not_its_at_rules() -> None:
    css = ("/* a comment with a .decoy selector in it */\n"
           ".one { color: red; }\n"
           "@media (max-width: 900px) {\n"
           "  .two { color: blue; }\n"
           "}\n")
    blocks = CENSUS.parse_blocks(css)
    rules = {b["selector"]: b for b in blocks if b["kind"] == "rule"}
    assert set(rules) == {".one", ".two"}
    assert (rules[".one"]["start"], rules[".one"]["end"]) == (2, 2)
    # a nested rule's extent is ITS OWN, never its `@media`'s
    assert (rules[".two"]["start"], rules[".two"]["end"]) == (4, 4)
    assert rules[".two"]["at_rule"].startswith("@media")
    # and a selector named only in a COMMENT is no selector at all
    assert "decoy" not in {t for b in rules.values()
                           for t in CENSUS.selector_tokens(b["selector"])["classes"]}


def test_a_selector_is_split_into_classes_ids_and_elements() -> None:
    parts = CENSUS.selector_tokens('button.gatebtn#main[hidden]:hover .swb-ch')
    assert parts["classes"] == ["gatebtn", "swb-ch"]
    assert parts["ids"] == ["main"]
    assert parts["elements"] == ["button"]


# ---------------------------------------------------------------------------
# The scans.
# ---------------------------------------------------------------------------

def test_a_class_is_named_only_from_a_class_bearing_position() -> None:
    js = ('const a = el("div", "gatebar");\n'
          'const b = root.querySelector(".refusalpanel-head");\n'
          'const c = `<p class="swb-ch other">x</p>`;\n'
          'const msg = "panelnote is not a class here, it is prose about one";\n')
    named = CENSUS.narrow_refs(js, ".js")
    assert {"gatebar", "refusalpanel-head", "swb-ch", "other"} <= named
    # the prose sentence is not a bare class list, so it names nothing
    assert "prose" not in named and "here" not in named


def test_a_concatenated_class_is_named_by_its_prefix() -> None:
    js = 'el("button", "disposebtn dispose-" + v.outcome, v.label);\n'
    assert CENSUS.prefix_refs(js, ".js") == {"dispose-"}
    # THE DEFECT THIS RULE REPAIRS: `STYLE_RESIDUE`'s 51 was three short,
    # because `.dispose-accepted` / `.dispose-rejected` / `.dispose-deferred`
    # are never written down and no literal search can see them.
    # The literal's own tokens are class-bearing (it sits in ARGUMENT position),
    # and the open-ended `dispose-` is exactly the fragment the prefix rule
    # above turns into the three classes a literal search cannot see.
    assert CENSUS.narrow_refs(js, ".js") == {"button", "disposebtn", "dispose-"}


def test_a_bare_literal_counts_only_where_a_class_is_passed_or_assigned() -> None:
    """THE PARSER-FREE DISCRIMINATOR (Copilot review of openxFactory #1068,
    round 3). 46 of the 54 classes this census finds rest on a bare literal and
    nothing else, because this bundle's element helper takes the class as its
    SECOND ARGUMENT — so the rule cannot simply drop bare literals (that answers
    5 where the truth is 54). It bounds them by POSITION instead."""
    # `"div"` comes back beside `"gatebar"` — an element tag is in argument
    # position too, and no parser-free rule tells the two apart. IT IS INERT:
    # only tokens `styles.css` DECLARES AS A SELECTOR are ever classified, and
    # a bundle that declared a `.div` class would have bigger problems. The
    # scan reports candidates; the stylesheet decides which are classes.
    assert CENSUS.narrow_refs('el("div", "gatebar");\n', ".js") == {"div", "gatebar"}
    assert CENSUS.narrow_refs('node.className = "gatebar";\n', ".js") == {"gatebar"}
    # a class TABLE: the key says what the value is
    assert CENSUS.narrow_refs('{ ok: { label: "applied", cls: "is-ok" } }\n',
                              ".js") == {"is-ok"}
    # a VALUE under a key that is not about classes names nothing
    assert CENSUS.narrow_refs('post("/x", { kind: "summary" });\n', ".js") == set()
    # and a COMPARISON is not an assignment
    assert CENSUS.narrow_refs('if (state === "summary") return;\n', ".js") == set()


def test_a_template_substitution_is_a_prefix_too() -> None:
    assert CENSUS.prefix_refs('`<i class="chip chip-${state}">`;\n', ".js") \
        == {"chip-"}


# ---------------------------------------------------------------------------
# The decision, and its asymmetry — the safety argument.
# ---------------------------------------------------------------------------

def test_a_block_leaves_only_when_the_gate_owns_every_class_in_its_selector(
        tmp_path: Path) -> None:
    dox, xdox = _tree(
        tmp_path,
        styles=(".gatebar { color: red; }\n"
                ".docrow { color: blue; }\n"
                ".gatebar .docrow { color: green; }\n"),
        own={"docs.js": 'el("div", "docrow");\n'},
        gate={"gate.js": 'el("div", "gatebar");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert report["gate_exclusive"] == ["gatebar"]
    assert [b["selector"] for b in report["exclusive_blocks"]] == [".gatebar"]
    # the MIXED rule stays, and is reported as mixed rather than silently kept
    assert [b["selector"] for b in report["mixed_blocks"]] == [".gatebar .docrow"]


def test_a_stray_gate_literal_cannot_send_an_opendox_rule_to_another_leg(
        tmp_path: Path) -> None:
    """THE ASYMMETRY, which is the whole safety argument (Copilot review of
    openxFactory #1068, round 3).

    The two over-inclusions are not the same error: over-including on openDox's
    side KEEPS a rule, over-including on the gate's side MOVES one. So the gate
    side is read from CLASS-BEARING positions only, and a route, label or error
    string that happens to equal a selector token names nothing.
    """
    dox, xdox = _tree(
        tmp_path,
        styles=".summary { color: red; }\n",
        own={"docs.js": "// the summary pane, built by the shell\n"},
        gate={"gate.js": 'post("/actions/gate/x", { kind: "summary" });\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    # `summary` is a VALUE in the gate module and prose in openDox's — under an
    # all-broad rule the gate would own it and the rule would leave.
    assert report["gate_exclusive"] == [], report["gate_exclusive"]
    assert report["exclusive_blocks"] == []
    assert report["class_counts_broad"]["gate_exclusive"] == 1
    assert report["class_counts_extraction"]["gate_exclusive"] == 0


def test_an_opendox_mention_anywhere_keeps_a_rule(tmp_path: Path) -> None:
    """The other half of the asymmetry: the openDox side is the BROAD scan, so
    a class it names in ANY literal is kept even where the gate names it in a
    class-bearing position."""
    dox, xdox = _tree(
        tmp_path,
        styles=".gatebar { color: red; }\n",
        own={"docs.js": 'log("gatebar was retired in this build");\n'},
        gate={"gate.js": 'el("div", "gatebar");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert report["gate_exclusive"] == []
    assert report["exclusive_blocks"] == []


def test_a_gate_module_never_counts_as_opendoxs_own(tmp_path: Path) -> None:
    """Before slice S5 the six modules lived in openDox's `views/`, and a
    name-blind sweep would have called every gate class `shared` — which is why
    `--gate-dir` exists and why a gate module is excluded from the openDox side
    wherever it physically sits."""
    dox, xdox = _tree(
        tmp_path,
        styles=".gatebar { color: red; }\n",
        own={"gate.js": 'el("div", "gatebar");\n'},
        gate={"gate.js": 'el("div", "gatebar");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert report["gate_exclusive"] == ["gatebar"]


def test_the_report_states_which_blocks_read_a_design_token(tmp_path: Path) -> None:
    """RULED Q7 makes the `--st-*` family the one stable styling surface, so a
    block that READS one is a fact the record wants: it is what a contributed
    sheet is allowed to depend on."""
    dox, xdox = _tree(
        tmp_path,
        styles=(".gatebar { border: 1px solid var(--st-proposed); }\n"
                ".gatebtn { color: var(--ink); }\n"),
        own={},
        gate={"gate.js": 'el("div", "gatebar"); el("button", "gatebtn");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    reads = {b["selector"]: b["reads_st_token"] for b in report["exclusive_blocks"]}
    assert reads == {".gatebar": True, ".gatebtn": False}
    assert report["exclusive_blocks_reading_st"] == 1


def test_the_usage_line_names_the_committed_filename() -> None:
    """A usage example that names a file the repository does not carry is a
    command nobody can run (Copilot review, round 3)."""
    text = SCRIPT.read_text(encoding="utf-8")
    assert "scripts/measure_opendox_css_census.py" in text
    assert "measure-css-census.py" not in text
