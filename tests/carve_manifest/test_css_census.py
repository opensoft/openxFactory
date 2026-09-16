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


def test_an_assignment_counts_only_where_the_target_is_a_class() -> None:
    """A BARE `x = "…"` IS NOT A CLASS WRITE (Copilot review, round 5).

    `btn.title = "commission proposal authoring for this staging topic "` — an
    ordinary sentence — has every word matching the class alphabet, and two of
    them (`proposal`, `topic`) are declared classes in the real stylesheet. The
    target has to say it is a class.
    """
    assert CENSUS.narrow_refs('node.className = "gatebar";\n', ".js") == {"gatebar"}
    assert CENSUS.narrow_refs('o.cls = "is-ok";\n', ".js") == {"is-ok"}
    assert CENSUS.narrow_refs('btn.title = "a staging topic here";\n', ".js") == set()
    assert CENSUS.narrow_refs('if (x == "gatebar") return;\n', ".js") == set()


def test_a_dot_inside_a_path_is_a_file_extension_and_not_a_selector() -> None:
    """A selector never carries a `/`; a path always does (Copilot review,
    round 5). `"/api/gate.css"` must not hand the gate the class `css`."""
    assert CENSUS.narrow_refs('fetch("/api/gate.css");\n', ".js") == set()
    assert CENSUS.narrow_refs('import("./views/swb-create.js");\n', ".js") == set()
    # a real selector string still reads as one
    assert CENSUS.narrow_refs('root.querySelector(".gatebar");\n', ".js") \
        == {"gatebar"}


def test_a_missing_or_empty_checkout_refuses_instead_of_reporting_zero(
        tmp_path: Path) -> None:
    """THE WORST ANSWER THIS TOOL CAN GIVE IS `0` (Copilot review, round 5).

    A mistyped path globs to nothing and would report `0 gate-exclusive
    classes, 0 blocks` — which is the SAME output a completed extraction
    produces, so an invalid argument would read as a measured result.
    """
    dox, xdox = _tree(tmp_path, styles=".gatebar { color: red; }\n", own={},
                      gate={"gate.js": 'el("div", "gatebar");\n'})
    missing = subprocess.run(
        [sys.executable, str(SCRIPT), str(dox), str(tmp_path / "absent")],
        capture_output=True, text=True, timeout=300)
    assert missing.returncode != 0
    assert "is not a directory" in missing.stderr

    empty = tmp_path / "empty"
    empty.mkdir()
    blank = subprocess.run(
        [sys.executable, str(SCRIPT), str(dox), str(xdox), "--gate-dir", str(empty)],
        capture_output=True, text=True, timeout=300)
    assert blank.returncode != 0
    assert "carries no `.js` file" in blank.stderr


def test_a_compound_selector_names_both_of_its_classes() -> None:
    """`.foo.bar` IS TWO CLASSES (Copilot review, round 6).

    The position rule that stops `gate.lens` naming `lens` must not also stop
    `.foo.bar` naming `bar` — the second dot follows an identifier character in
    both, and only whether THAT identifier was itself a class tells them apart.
    A gate module using a compound selector would otherwise have had its rule
    read as mixed and kept.
    """
    assert CENSUS.selector_class_tokens(".foo.bar") == {"foo", "bar"}
    assert CENSUS.selector_class_tokens(".a.b.c") == {"a", "b", "c"}
    assert CENSUS.selector_class_tokens(".gatebar .swb-ch") == {"gatebar", "swb-ch"}
    # and the forms the position rule refuses, including the one real selector
    # among them: `div.foo` is ELEMENT-QUALIFIED and reads exactly like
    # `error.foo`, so it goes with them. A loss in the SAFE direction —
    # under-reading the gate side KEEPS a rule in openDox.
    assert CENSUS.selector_class_tokens("div.foo") == set()
    assert CENSUS.selector_class_tokens("gate.lens") == set()
    assert CENSUS.selector_class_tokens("error.foo") == set()
    assert CENSUS.selector_class_tokens("proposal.md") == set()
    # through `narrow_refs`, which is where it is used
    assert CENSUS.narrow_refs('root.querySelector(".gatebar.is-live");\n',
                              ".js") == {"gatebar", "is-live"}


def test_an_attribute_value_that_looks_like_a_selector_names_nothing() -> None:
    """`[data-state=".gatebar"]` is an attribute VALUE (Copilot review, round
    6). `selector_tokens` already stripped `[...]`; the JavaScript-side scan
    did not, so the same string in a `querySelector` call still claimed the
    class — and on the GATE side a false claim MOVES a rule."""
    assert CENSUS.narrow_refs(
        'root.querySelector(\'[data-state=".gatebar"]\');\n', ".js") == set()
    # a real class beside an attribute selector is still read
    assert CENSUS.narrow_refs(
        'root.querySelector(".gatebtn[hidden]");\n', ".js") == {"gatebtn"}


def test_a_token_declared_after_another_declaration_still_keeps_its_block(
        tmp_path: Path) -> None:
    """A DECLARATION BOUNDARY, NOT A LINE START (Copilot review, round 7).

    `^\\s*--st-` saw only a token declared first on its line, so
    `.gatebar { color: red; --st-proposed: #123; }` was extractable and RULED
    Q7's one stable styling surface left with it.
    """
    dox, xdox = _tree(
        tmp_path,
        styles=(".gatebar { color: red; --st-proposed: #123; }\n"
                ".gatebtn { color: blue; }\n"),
        own={},
        gate={"gate.js": 'el("div", "gatebar"); el("button", "gatebtn");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert [b["selector"] for b in report["exclusive_blocks"]] == [".gatebtn"]
    assert [b["selector"] for b in report["blocks_kept_for_declaring_a_token"]] \
        == [".gatebar"]


def test_a_block_that_declares_a_design_token_never_leaves(
        tmp_path: Path) -> None:
    """RULED Q7 makes the `--st-*` family openDox's ONE stable styling surface,
    so a rule that DEFINES one is openDox's however gate-only its selector
    reads (Copilot review, round 6: `declares_st_token` was computed after
    classification and nothing consulted it)."""
    dox, xdox = _tree(
        tmp_path,
        styles=(".gatebar { --st-proposed: #123; }\n"
                ".gatebtn { color: red; }\n"),
        own={},
        gate={"gate.js": 'el("div", "gatebar"); el("button", "gatebtn");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert report["gate_exclusive"] == ["gatebar", "gatebtn"]
    assert [b["selector"] for b in report["exclusive_blocks"]] == [".gatebtn"]
    assert [b["selector"] for b in report["blocks_kept_for_declaring_a_token"]] \
        == [".gatebar"]
    # MEASURED at the cited base commits this list is EMPTY, so the 59 are the
    # 59; the guard is for the act that gives a gate-only rule a declaration.


def test_a_missing_opendox_views_directory_refuses_too(tmp_path: Path) -> None:
    """The openDox side is the side that KEEPS rules, so an empty scan of it is
    the UNSAFE emptiness (Copilot review, round 6)."""
    dox, xdox = _tree(tmp_path, styles=".gatebar { color: red; }\n", own={},
                      gate={"gate.js": 'el("div", "gatebar");\n'})
    (dox / "src" / "opendox" / "web" / "views").rmdir()
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(dox), str(xdox)],
        capture_output=True, text=True, timeout=300)
    assert proc.returncode != 0
    assert "is not a directory" in proc.stderr


def test_a_prefix_counts_only_from_a_class_bearing_position() -> None:
    """THE ASYMMETRY REACHES PREFIXES TOO (Copilot review, round 5).

    An ungated prefix rule let any hyphen-terminated word claim every declared
    class starting with it, and on the gate side that claim MOVES a rule.
    """
    js = ('el("button", "disposebtn dispose-" + v.outcome);\n'
          'log("the run is status- prefixed, per the audit log.");\n')
    # ungated (the openDox side): both, because over-reading there only KEEPS
    assert CENSUS.prefix_refs(js, ".js") == {"dispose-", "status-"}
    # gated (the gate side): only the one a class is built from
    assert CENSUS.prefix_refs(js, ".js", class_bearing_only=True) == {"dispose-"}
    # and a `class="…"` run is class-bearing by construction, wherever it sits
    assert CENSUS.prefix_refs('`<i class="chip chip-${state}">`;\n', ".js",
                              class_bearing_only=True) == {"chip-"}


# ---------------------------------------------------------------------------
# The stylesheet parser's own blind spots (Copilot review, round 5).
# ---------------------------------------------------------------------------

def test_a_brace_inside_a_css_string_does_not_close_a_block() -> None:
    """`content: "}"` is a DECLARATION, not the end of the rule. Counting it
    truncated the block and moved every extent after it."""
    css = ('.one::before { content: "}"; color: red; }\n'
           '.two { content: "{"; color: blue; }\n'
           '.three { color: green; }\n')
    rules = {b["selector"]: b for b in CENSUS.parse_blocks(css)
             if b["kind"] == "rule"}
    assert set(rules) == {".one::before", ".two", ".three"}
    assert (rules[".three"]["start"], rules[".three"]["end"]) == (3, 3)


def test_a_rule_nested_two_at_rules_deep_is_still_found() -> None:
    """`@media { @supports { .gatebar {…} } }` recorded `@supports` as a rule
    and never emitted `.gatebar` — an exclusive block left in the wrong leg."""
    css = ("@media (min-width: 40rem) {\n"
           "  @supports (display: grid) {\n"
           "    .gatebar { color: red; }\n"
           "  }\n"
           "}\n")
    rules = {b["selector"]: b for b in CENSUS.parse_blocks(css)
             if b["kind"] == "rule"}
    assert list(rules) == [".gatebar"]
    assert (rules[".gatebar"]["start"], rules[".gatebar"]["end"]) == (3, 3)
    assert rules[".gatebar"]["at_rule"].startswith("@media")
    assert "@supports" in rules[".gatebar"]["at_rule"]


def test_a_class_named_inside_an_attribute_value_is_not_a_class_selector() -> None:
    """`[data-state=".gatebar"]` yielded the class `gatebar`, so a rule with no
    class selector at all could be classified gate-exclusive and extracted."""
    parts = CENSUS.selector_tokens('div[data-state=".gatebar"]')
    assert parts["classes"] == []
    assert parts["elements"] == ["div"]
    # a real class beside an attribute selector is still read
    assert CENSUS.selector_tokens('.gatebtn[hidden]')["classes"] == ["gatebtn"]


def test_a_commented_out_token_use_is_not_a_token_dependency(
        tmp_path: Path) -> None:
    """RULED Q7 makes `--st-*` the one stable styling surface, so "this block
    reads a token" has to mean the block reads it — not that someone wrote it
    in a comment."""
    dox, xdox = _tree(
        tmp_path,
        styles=(".gatebar { /* was var(--st-proposed) */ color: red; }\n"
                ".gatebtn { color: var(--st-proposed); }\n"),
        own={},
        gate={"gate.js": 'el("div", "gatebar"); el("button", "gatebtn");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    reads = {b["selector"]: b["reads_st_token"] for b in report["exclusive_blocks"]}
    assert reads == {".gatebar": False, ".gatebtn": True}
    assert report["exclusive_blocks_reading_st"] == 1


def test_the_reported_line_count_is_the_one_the_extents_are_numbered_in(
        tmp_path: Path) -> None:
    """A final line without a trailing newline IS a line to `line_of`, and the
    report has to count it the same way or the two disagree by one."""
    dox, xdox = _tree(tmp_path, styles=".gatebar { color: red; }",   # no \n
                      own={}, gate={"gate.js": 'el("div", "gatebar");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert report["styles_css"]["lines"] == 1
    assert report["exclusive_blocks"][0]["end"] == 1


def test_the_line_count_is_the_carve_floors_and_not_pythons(
        tmp_path: Path) -> None:
    """AND IT IS THE FLOOR'S DEFINITION (Copilot review, round 7).

    `line_of` counts `\n`s; `splitlines()` also breaks on U+2028, U+2029,
    `\v`, `\f`, `\x85` and a lone `\r`. A stylesheet carrying one would have
    reported a total the block extents are not numbered in — and the manifest
    declares this file's lines in the floor's numbering
    (`scripts/carve_lines.py`, RULED Q-L8 (c)), which is the one the arrival
    verifier checks them against at the destination.
    """
    styles = (".gatebar { color: red; }\n"
              "/* a separator \u2028 inside a comment */\n"
              ".gatebtn { color: blue; }\n")
    assert len(styles.splitlines()) == 4          # Python's opinion
    dox, xdox = _tree(tmp_path, styles=styles, own={},
                      gate={"gate.js": 'el("div", "gatebar");\n'
                                       'el("button", "gatebtn");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert report["styles_css"]["lines"] == 3     # the floor's, and `line_of`'s
    ends = {b["selector"]: b["end"] for b in report["exclusive_blocks"]}
    assert ends == {".gatebar": 1, ".gatebtn": 3}


def test_a_pseudo_class_does_not_break_a_compound_selector() -> None:
    """`.foo:hover.bar` IS TWO CLASSES (Copilot review, round 7).

    Consuming `hover` as an ordinary identifier run cleared the bit saying the
    run before `.bar` began with a dot, so `bar` was lost and the gate module
    using that selector was under-read.
    """
    assert CENSUS.selector_class_tokens(".foo:hover.bar") == {"foo", "bar"}
    assert CENSUS.selector_class_tokens(".foo::before.bar") == {"foo", "bar"}
    assert CENSUS.selector_class_tokens(".gatebar:not(.is-live).swb-ch") \
        == {"gatebar", "is-live", "swb-ch"}
    # and it does not MAKE a compound: element-qualified stays refused
    assert CENSUS.selector_class_tokens("div:hover.foo") == set()
    assert CENSUS.narrow_refs('root.querySelector(".gatebtn:focus.is-live");\n',
                              ".js") == {"gatebtn", "is-live"}


def test_a_dotted_word_in_a_sentence_is_not_a_selector() -> None:
    """SHAPE IS NOT SELECTORHOOD (Copilot review, round 7).

    `showError("see .gatebar")` is on the selector alphabet end to end, so the
    shape test passed it and an ordinary message could MOVE an openDox rule. A
    bare word in a selector can only be a TYPE selector, and a type selector is
    an element name.
    """
    assert CENSUS.narrow_refs('showError("see .gatebar");\n', ".js") == set()
    assert CENSUS.narrow_refs('log("commission .dispose-note now");\n',
                              ".js") == set()
    # a real selector led by a real element name is read exactly as before
    assert CENSUS.narrow_refs('root.querySelector("h2 .gate-title");\n',
                              ".js") == {"gate-title"}
    assert CENSUS.is_selector_text("button.gatebar") is True
    assert CENSUS.is_selector_text("see .gatebar") is False


def test_a_class_equals_in_prose_is_not_markup() -> None:
    """`class=` ANYWHERE IN A STRING IS NOT MARKUP (Copilot review, round 7,
    thread `PRRT_kwDOTAvnrs6jCcPV`).

    A message that TALKS about markup registered a concatenation prefix, and on
    the gate's narrow prefix table a prefix claims every declared class
    beginning with it — every `dispose-*` rule, moved by a sentence.
    """
    prose = 'const message = \'expected class="dispose-"\';\n'
    assert CENSUS.prefix_refs(prose, ".js", class_bearing_only=True) == set()
    assert CENSUS.narrow_refs('warn(\'write class="gatebar" here\');\n',
                              ".js") == set()
    # the markup itself still counts, prefix and token alike
    markup = '`<i class="chip chip-${state}">`;\n'
    assert CENSUS.prefix_refs(markup, ".js", class_bearing_only=True) == {"chip-"}
    assert CENSUS.narrow_refs('`<div class="gatebar is-live">`;\n',
                              ".js") == {"gatebar", "is-live"}


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
