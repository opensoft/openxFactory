"""`scripts/measure_opendox_css_census.py` — RULED Q7's measurement, EXECUTED.

The tool decides WHICH STYLESHEET BLOCKS LEAVE openDox's bundle for the
bindings that own them (RULED Q7, `opensoft/openxFactory#656` comment
`5648049748`), and the manifest's own `web/styles.css` row cites it as the
reason its 89 declared lines are the lines they are. A measurement the floor
leans on and nothing executes is the defect § 2's re-derivation tests exist for,
one directory over (Copilot review of openxFactory #1068, round 3).

FIXTURES, NOT THE TWO LEGS. This repository carries neither `openDox-code` nor
`openXdox-code`, and standing a test down because they are absent is not
available here: a skip reports as a green bar and `pytest-suite.yml` pins the
skip count EXACTLY, so one more of them reds the required job — measured, run
`105209771859`, `skipped=7` against the pinned `6`. What is asserted instead is
the tool's DECISION RULE, on
stylesheets and modules small enough to read: the CSS block parser, the
class-bearing scan, the concatenation-prefix rule that `STYLE_RESIDUE`'s own
`51` was three short without, and — the one that matters most — the ASYMMETRY
between the two sides of the extraction decision. The one test that names the
two revisions re-derives the WHOLE report when checkouts are handed to it
(`Q7_OPENDOX_CODE` / `Q7_OPENXDOX_CODE`) and otherwise holds its seat with
assertions about that re-derivation's own inputs — never a skip.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

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


def test_a_class_equals_inside_another_attribute_is_that_attributes(
        tmp_path: Path) -> None:
    """`<div title='class="gatebar"'>` IS A TITLE (Copilot review, round 8).

    "the last `<` with no `>` between" said yes to it, and a false class run on
    the gate side moves an openDox rule. The tag is walked with quote state
    carried now, so `>` inside a value no longer closes it either.
    """
    js = """host.innerHTML = `<span title='class="gatebar"'>see</span>`;\n"""
    assert CENSUS.narrow_refs(js, ".js") == set()
    assert CENSUS.prefix_refs('`<i alt="class=chip-">x</i>`;\n', ".js",
                              class_bearing_only=True) == set()
    # the real attribute is still read, including past a `>` inside a value
    assert CENSUS.narrow_refs(
        """`<i data-q='a>b' class="gatebar">`;\n""", ".js") == {"gatebar"}
    # and end to end: the block does not leave on the strength of a title
    dox, xdox = _tree(
        tmp_path,
        styles=".gatebar { color: red; }\n.gatebtn { color: blue; }\n",
        own={},
        gate={"gate.js": """host.innerHTML = `<b title='class="gatebar"'>x</b>`;\n"""
                         'el("button", "gatebtn");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert [b["selector"] for b in report["exclusive_blocks"]] == [".gatebtn"]


def test_a_calls_parenthesis_is_not_a_grouping_parenthesis() -> None:
    """`label("ga") + "te"` IS NOT `gate` (Copilot review, round 16).

    Round 13 allowed parentheses in the separator so `("ga" + "te") + "bar"`
    would join; allowing ANY of them let a CALL RESULT join too, and the
    literal inside the call is that call's ARGUMENT, not the left operand.
    """
    assert "gate" not in CENSUS.js_literal_text(
        'el("div", label("ga") + "te");\n').split()
    assert "gate" in CENSUS.js_literal_text(
        'el("div", ("ga" + "te"));\n').split()
    assert "gatebar" in CENSUS.js_literal_text(
        'el("div", ("ga" + "te") + "bar");\n').split()
    assert CENSUS._is_concatenation('"a" + "b"', 3, 6) is True
    assert CENSUS._is_concatenation('f("a") + "b"', 5, 9) is False


def test_markup_inside_a_comment_or_a_script_is_not_markup() -> None:
    """`<!-- <div class="gatebar"> -->` NAMES NOTHING (Copilot review, round
    16), and neither does the same string inside a `<script>` body — a class
    the page never applies, claimed on the side where a claim MOVES a rule."""
    template = ('`<!-- <div class="gatebar"> -->'
                '<i class="gatebtn"></i>`;\n')
    assert CENSUS.narrow_refs(template, ".js") == {"gatebtn"}
    page = ('<script>var s = "<div class=\'gatebar\'>";</script>\n'
            '<style>/* <b class="stylebar"> */</style>\n'
            '<i class="gatebtn"></i>\n')
    assert CENSUS.narrow_refs(page, ".html") == {"gatebtn"}
    assert CENSUS._literals(page, ".html") == ["gatebtn"]


def test_a_quoted_bracket_does_not_end_an_attribute_selector() -> None:
    """`[data-label="x] .gatebar"]` HAS NO CLASS (Copilot review, round 15).

    A regex that closes at the first `]` reduced it to text carrying
    `.gatebar`, so the census invented a class selector for a rule that has
    none — and a rule with no class selector at all could be extracted.
    """
    assert CENSUS.selector_class_tokens('[data-label="x] .gatebar"]') == set()
    assert CENSUS.selector_tokens('[data-label="x] .gatebar"]')["classes"] == []
    assert CENSUS.selector_class_tokens('[data-label="x] y"] .gatebtn') \
        == {"gatebtn"}
    assert CENSUS._without_attribute_selectors('div[a="]"].foo') == "div.foo"


def test_an_element_qualified_selector_with_an_attribute_never_leaves(
        tmp_path: Path) -> None:
    """`div[data-state].gatebar { … }` STAYS (Copilot review, round 15). The
    ANCHOR question is the narrow one `selector_class_tokens` answers, where
    that form is element-qualified and names nothing; asking the wide
    `selector_tokens` let the decision extract exactly the shape the position
    rule refuses."""
    dox, xdox = _tree(
        tmp_path,
        styles=("div[data-state].gatebar { color: red; }\n"
                ".gatebar[data-state] { color: blue; }\n"),
        own={},
        gate={"gate.js": 'el("div", "gatebar");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert [b["selector"] for b in report["exclusive_blocks"]] \
        == [".gatebar[data-state]"]


def test_the_page_is_read_with_the_same_tag_aware_parser(tmp_path: Path) -> None:
    """ONE PARSER FOR BOTH SIDES (Copilot review, rounds 11 and 15). A regex
    over the whole page read `class=` inside a `title`, inside a comment and
    inside `<script>` text as live attributes, and could not see an unquoted
    value at all."""
    page = ("<!-- class=\"commentbar\" -->\n"
            "<div title='class=\"titlebar\"'>\n"
            "  <i class=gatebar></i><b class='gatebtn is-live'></b>\n"
            "</div>\n")
    assert CENSUS.narrow_refs(page, ".html") \
        == {"gatebar", "gatebtn", "is-live"}
    assert sorted(CENSUS._literals(page, ".html")) \
        == ["gatebar", "gatebtn is-live"]


def test_a_pseudo_functions_argument_is_a_selector_of_its_own() -> None:
    """`div:not(.bar).foo` NAMES `bar` AND NOT `foo` (Copilot review, round
    14). Walking the argument inline let `.bar` set the compound bit for a
    compound it is not in, so the element-qualified `.foo` was accepted —
    contrary to the `div.foo` rejection the whole position rule rests on."""
    assert CENSUS.selector_class_tokens("div:not(.bar).foo") == {"bar"}
    assert CENSUS.selector_class_tokens(".gatebar:not(.is-live).swb-ch") \
        == {"gatebar", "is-live", "swb-ch"}
    assert CENSUS.selector_class_tokens("div:is(.a, .b)") == {"a", "b"}
    assert CENSUS.narrow_refs('root.querySelector("div:not(.bar).foo");\n',
                              ".js") == {"bar"}


def test_a_gate_class_built_from_a_chain_is_named_in_position(
        tmp_path: Path) -> None:
    """THE CHAIN RULE REACHES THE CLASS-BEARING SCANS TOO (Copilot review,
    round 14). Round 10 taught the BROAD scan that `"ga" + "te" + "bar"`
    writes `gatebar`; the narrow and prefix scans still read one literal at a
    time, so a contributed module writing it named no class and its block
    stayed behind as unreferenced."""
    # the chain is named at the position ITS FIRST literal sits in, and the
    # position rule still applies to every span: `"te"` and `"bar"` follow a
    # `+`, which is not a class-bearing position, so only the runs that BEGIN
    # in argument position count.
    assert CENSUS.narrow_refs('el("div", "ga" + "te" + "bar");\n', ".js") \
        == {"div", "ga", "gate", "gatebar"}
    assert CENSUS.prefix_refs('el("b", "dispose" + "-" + outcome);\n', ".js",
                              class_bearing_only=True) == {"dispose-"}
    # and the position rule still holds over a chain: a comparison names nothing
    assert CENSUS.narrow_refs('if (state === "ga" + "tebar") {}\n',
                              ".js") == set()
    dox, xdox = _tree(
        tmp_path,
        styles=".gatebar { color: red; }\n",
        own={},
        gate={"gate.js": 'el("div", "ga" + "te" + "bar");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert [b["selector"] for b in report["exclusive_blocks"]] == [".gatebar"]


def test_an_attribute_in_the_middle_does_not_open_a_compound() -> None:
    """`div[data-state="x"].gatebar` IS `div.gatebar` (Copilot review, round
    12). Blanking the attribute to a SPACE made the dot follow whitespace, so
    a selector the element-qualified rule refuses was accepted with an
    attribute in the middle — and on the gate side that MOVES a rule."""
    assert CENSUS.selector_class_tokens('div[data-state="x"].gatebar') == set()
    assert CENSUS.selector_class_tokens('.foo[hidden].bar') == {"foo", "bar"}
    # a DESCENDANT attribute selector keeps its gap: the space is outside it
    assert CENSUS.selector_class_tokens('[data-state="x"] .gatebar') \
        == {"gatebar"}
    assert CENSUS.narrow_refs(
        'root.querySelector(\'div[data-state="x"].gatebar\');\n', ".js") == set()


def test_a_class_inside_a_pseudo_function_does_not_anchor_a_branch(
        tmp_path: Path) -> None:
    """`:not(.gatebar) { … }` STAYS (Copilot review, round 12). The class is a
    CONDITION on the match, not the hook the rule is anchored by — the rule
    styles nearly every element on the page."""
    assert CENSUS._outside_pseudo_functions(":not(.gatebar)").strip() == ""
    assert CENSUS._outside_pseudo_functions(".gatebar:not(.is-live)") \
        == ".gatebar"
    assert CENSUS._outside_pseudo_functions(":is(:not(.a)).gatebar") \
        == ".gatebar"
    dox, xdox = _tree(
        tmp_path,
        styles=(":not(.gatebar) { color: red; }\n"
                ".gatebar:not(.is-live) { color: blue; }\n"),
        own={},
        gate={"gate.js": 'root.querySelectorAll(":not(.gatebar)");\n'
                         'root.querySelector(".gatebar:not(.is-live)");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert [b["selector"] for b in report["exclusive_blocks"]] \
        == [".gatebar:not(.is-live)"]


def test_a_selector_list_with_a_classless_branch_never_leaves(
        tmp_path: Path) -> None:
    """`.gatebar, button { … }` STAYS (Copilot review, round 11).

    `selector_tokens` aggregates over the whole list, so the rule read as
    gate-exclusive on the strength of `.gatebar` alone — and extracting it
    would have taken openDox's generic `button` styling to another leg.
    """
    dox, xdox = _tree(
        tmp_path,
        styles=(".gatebar, button { color: red; }\n"
                ".gatebtn, .gatebar span { color: blue; }\n"
                ".gatebar, [hidden] { color: green; }\n"),
        own={},
        gate={"gate.js": 'el("div", "gatebar"); el("button", "gatebtn");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    # only the list whose EVERY branch is anchored by a class leaves
    assert [b["selector"] for b in report["exclusive_blocks"]] \
        == [".gatebtn, .gatebar span"]
    assert CENSUS._selector_branches(".gatebar:not(a, b), button") \
        == [".gatebar:not(a, b)", "button"]


def test_a_bundle_missing_a_required_file_refuses_instead_of_raising(
        tmp_path: Path) -> None:
    """`app.js` and `index.html` are read unconditionally, so a checkout
    without one passed every path check and then raised `FileNotFoundError`
    (Copilot review, round 11)."""
    for missing in ("app.js", "index.html"):
        dox, xdox = _tree(tmp_path / missing, styles=".gatebar { color: red; }\n",
                          own={}, gate={"gate.js": 'el("div", "gatebar");\n'})
        (dox / "src" / "opendox" / "web" / missing).unlink()
        proc = subprocess.run([sys.executable, str(SCRIPT), str(dox), str(xdox)],
                              capture_output=True, text=True, timeout=300)
        assert proc.returncode != 0, missing
        assert "is not a file" in proc.stderr, missing
        assert "Traceback" not in proc.stderr, missing


def test_the_page_names_a_class_only_under_a_class_attribute() -> None:
    """`data-class="gatebar"` is not `class="gatebar"` in `index.html` either
    (Copilot review, round 11) — one rule for both sides, so the two scans
    cannot disagree about what a class attribute is."""
    html = '<div data-class="gatebar"><i class=\'gatebtn is-live\'></i></div>'
    assert CENSUS.narrow_refs(html, ".html") == {"gatebtn", "is-live"}
    assert CENSUS._literals(html, ".html") == ["gatebtn is-live"]


def test_a_class_built_from_a_chain_of_literals_is_still_named() -> None:
    """EVERY CONTIGUOUS SUB-RUN of a `+` chain (Copilot review, round 10).

    `"ga" + "te" + "bar"` writes `gatebar`, which a pairwise join (`gate`,
    `tebar`) never produces. This is the KEEP side, so a miss EXTRACTS a rule
    openDox still uses.
    """
    text = CENSUS.js_literal_text('el("div", "ga" + "te" + "bar");\n').split()
    for token in ("ga", "te", "bar", "gate", "tebar", "gatebar"):
        assert token in text, token
    # a chain broken by something that is not a `+` does not join across it
    assert "gatebar" not in CENSUS.js_literal_text(
        'f("gate", "bar");\n').split()
    # GROUPING AND COMMENTS ARE NOT OPERANDS (Copilot review, round 13)
    for source in ('el("div", ("ga" + "te") + "bar");\n',
                   'el("div", "ga" /* join */ + "te" + "bar");\n',
                   'el("div", "ga" +\n    // continued\n    "te" + "bar");\n'):
        assert "gatebar" in CENSUS.js_literal_text(source).split(), source
    # and a NAME between them still breaks the run
    assert "gatebar" not in CENSUS.js_literal_text(
        'f("gate") + g("bar");\n').split()


def test_an_unquoted_class_attribute_stops_at_the_next_attribute(
        tmp_path: Path) -> None:
    """`<i class=gatebar data-state=summary>` NAMES ONE CLASS (Copilot review,
    round 10). With one optional quote the capture ran through the space into
    the next attribute name, and a false token on the gate side moves a rule.
    """
    assert CENSUS.narrow_refs('`<i class=gatebar data-state=summary>`;\n',
                              ".js") == {"gatebar"}
    assert CENSUS.prefix_refs('`<i class=chip- data-state=summary>`;\n', ".js",
                              class_bearing_only=True) == {"chip-"}
    # the quoted form still carries a whole class LIST
    assert CENSUS.narrow_refs('`<i class="gatebar is-live">`;\n',
                              ".js") == {"gatebar", "is-live"}


def test_two_exclusive_rules_on_one_line_are_one_line(tmp_path: Path) -> None:
    """THE UNION OF THE EXTENTS, NOT THE SUM (Copilot review, round 10). A
    declared-edit window can name a physical line once, so a sum would report
    an extraction no set of line numbers could express."""
    dox, xdox = _tree(
        tmp_path,
        styles=".gatebar { color: red; } .gatebtn { color: blue; }\n",
        own={},
        gate={"gate.js": 'el("div", "gatebar"); el("button", "gatebtn");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert len(report["exclusive_blocks"]) == 2
    assert report["exclusive_block_lines"] == 1


def test_a_missing_stylesheet_refuses_instead_of_raising(tmp_path: Path) -> None:
    """A mistyped openDox checkout gets the same NAMED refusal a missing
    contributed-module directory gets (Copilot review, round 10), not a
    `FileNotFoundError` traceback."""
    dox, xdox = _tree(tmp_path, styles=".gatebar { color: red; }\n", own={},
                      gate={"gate.js": 'el("div", "gatebar");\n'})
    (dox / "src" / "opendox" / "web" / "styles.css").unlink()
    proc = subprocess.run([sys.executable, str(SCRIPT), str(dox), str(xdox)],
                          capture_output=True, text=True, timeout=300)
    assert proc.returncode != 0
    assert "is not a file" in proc.stderr
    assert "Traceback" not in proc.stderr


def test_an_id_does_not_break_a_compound_selector() -> None:
    """`.foo#id.bar` IS TWO CLASSES (Copilot review, round 9) — the same shape
    the pseudo-class fix answered, with an ID in the middle instead."""
    assert CENSUS.selector_class_tokens(".foo#id.bar") == {"foo", "bar"}
    assert CENSUS.selector_class_tokens(".gatebar#gate:hover.is-live") \
        == {"gatebar", "is-live"}
    assert CENSUS.selector_class_tokens("div#id.foo") == set()
    assert CENSUS.narrow_refs('root.querySelector(".gatebtn#g.is-live");\n',
                              ".js") == {"gatebtn", "is-live"}


def test_the_class_attribute_is_matched_by_name_and_by_either_quote() -> None:
    """A SINGLE-QUOTED ATTRIBUTE IS AN ATTRIBUTE, and `data-class` IS NOT
    `class` (Copilot review, round 9). The first omission leaves a gate-owned
    rule behind; the second claims a class the template never applies, which on
    the gate side MOVES one."""
    assert CENSUS.narrow_refs("""`<div class='gatebar is-live'>`;\n""",
                              ".js") == {"gatebar", "is-live"}
    assert CENSUS.narrow_refs('`<div data-class="gatebar">`;\n', ".js") == set()
    assert CENSUS.prefix_refs("`<i class='chip-${state}'>`;\n", ".js",
                              class_bearing_only=True) == {"chip-"}
    assert CENSUS.prefix_refs('`<i data-class="chip-">`;\n', ".js",
                              class_bearing_only=True) == set()


def test_a_selector_literal_counts_only_at_a_selector_api() -> None:
    """A DIAGNOSTIC WRITTEN AS A SELECTOR IS STILL A DIAGNOSTIC (Copilot
    review, round 8). `showError(".gatebar")` passes both the shape test and
    the element-name test, so the branch has to ask for the context as well."""
    assert CENSUS.narrow_refs('showError(".gatebar");\n', ".js") == set()
    assert CENSUS.narrow_refs('const SEL = ".gatebar";\n', ".js") == set()
    for call in ("root.querySelector", "root.querySelectorAll",
                 "ev.target.closest", "el.matches"):
        assert CENSUS.narrow_refs(f'{call}(".gatebar");\n', ".js") \
            == {"gatebar"}, call
    assert CENSUS.narrow_refs('ev.target.closest?.(".gatebar");\n',
                              ".js") == {"gatebar"}


def test_a_class_built_from_two_literals_is_still_named() -> None:
    """`"gate" + "bar"` NAMES `gatebar` (Copilot review, round 8).

    Neither literal contains it and `_PREFIX` cannot see it — a prefix has to
    end in `-` or run into a `${…}`. This is the BROAD scan, the KEEP side of
    the decision, so a reference missed here is a rule wrongly EXTRACTED.
    """
    text = CENSUS.js_literal_text('el("div", "gate" + "bar");\n')
    assert "gatebar" in text.split()
    assert "gate" in text.split() and "bar" in text.split()   # beside, not instead
    assert "gatebar" not in CENSUS.js_literal_text('el("div", "gate", "bar");\n')


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


def test_a_parenthesis_inside_a_comment_is_not_the_calls_own(
        tmp_path: Path) -> None:
    """THE DELIMITER WALK READS CODE, NOT SOURCE (Copilot review, round 18).

    Round 16 taught the join that a CALL's `)` is not a grouping one by
    matching each `)` back to its `(` — over the RAW text, so a parenthesis
    written inside a comment could stand in for the call's own.
    `label("ga" /* ( */) + "te"` then found the commented `(`, read the space
    before it instead of the name `label`, and joined the call result into
    `gate`. This is the BROAD scan, but the gate side reads it too, and a class
    the gate does not own is a rule wrongly EXTRACTED.
    """
    assert CENSUS.narrow_refs('el("div", label("ga" /* ( */) + "te");\n',
                              ".js") == {"div", "ga"}
    # a parenthesis inside a STRING is no opener either
    assert CENSUS.narrow_refs('el("div", f("(")  + "te");\n', ".js") == {"div"}
    # and rounds 10, 13 and 16 still hold exactly as they did
    assert CENSUS.narrow_refs('el("div", label("ga") + "te");\n', ".js") \
        == {"div", "ga"}
    assert CENSUS.narrow_refs('el("div", ("ga" /* c */ + "te") + "bar");\n',
                              ".js") == {"div", "ga", "gate", "gatebar"}
    # the blanked view keeps every offset, so nothing else shifts
    source = 'el("div", label("ga" /* ( */) + "te");\n'
    assert len(CENSUS._code_view(source)) == len(source)
    assert CENSUS._code_view(source).count("\n") == source.count("\n")
    # THE BLOCK FOLLOWS: the rule the comment would have handed the gate stays
    dox, xdox = _tree(
        tmp_path,
        styles=".gate { color: red; }\n",
        own={"own.js": 'el("span", "gate");\n'},
        gate={"gate.js": 'el("div", label("ga" /* ( */) + "te");\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert report["exclusive_blocks"] == []


def test_a_class_bearing_template_is_read_like_the_string_it_is(
        tmp_path: Path) -> None:
    """A TEMPLATE IN A CLASS-BEARING POSITION IS A CLASS LIST (Copilot review,
    round 17).

    `node.className = `gate-${state}`` failed the class-list test that gates
    both narrow scans, because `${state}` is not on the class alphabet — so
    the gate side registered no `gate-` prefix, and every `.gate-*` rule a
    contributed module builds that way read as unreferenced and STAYED in
    openDox's sheet. The markup form (`class="chip chip-${state}"`) was already
    read; the bare one was not.
    """
    assert CENSUS.prefix_refs('node.className = `gate-${state}`;\n', ".js",
                              class_bearing_only=True) == {"gate-"}
    assert CENSUS.prefix_refs('el("div", `gate-${state}`);\n', ".js",
                              class_bearing_only=True) == {"gate-"}
    # a substitution carries an expression, and an expression carries spaces
    # and braces of its own — it is ONE part, not five
    assert CENSUS.prefix_refs('n.classList.add(`is-${ok ? "ok" : "bad"}`);\n',
                              ".js", class_bearing_only=True) == {"is-"}
    assert CENSUS._parts_outside_substitutions('is-${ok ? "ok" : "bad"}') \
        == ['is-${ok ? "ok" : "bad"}']
    # and the POSITION rule still holds: a template that is returned, not
    # passed or assigned to a class, names nothing on the gate side
    assert CENSUS.prefix_refs('return `gate-${state}`;\n', ".js",
                              class_bearing_only=True) == set()
    # THE BLOCK FOLLOWS THE READING: the rule the gate builds by substitution
    # is the gate's own, and it leaves
    dox, xdox = _tree(
        tmp_path,
        styles=".gate-live { color: red; }\n",
        own={},
        gate={"gate.js": 'node.className = `gate-${state}`;\n'})
    report = _run(dox, xdox, tmp_path / "out.json")
    assert [b["selector"] for b in report["exclusive_blocks"]] == [".gate-live"]


def test_a_prose_template_is_no_more_a_class_list_than_a_sentence() -> None:
    """A SUBSTITUTION IS NOT EVIDENCE (Copilot review, round 17).

    Masking every `${…}` out and requiring what remains to STILL be a class
    token is what holds a template to exactly the strictness of the plain
    string of the same shape: `` `${name} must be an object` `` — openDox's own
    shape, six of them at `0b4e8bbf` — is refused, and `` `gatebar ${extra}` ``
    is refused with it. That second one is the price: a class not read on the
    GATE side keeps a rule in openDox's sheet, where the opposite error moves
    one out of it.
    """
    prose = 'throw new Error(`${name} must be an object`);\n'
    assert CENSUS.narrow_refs(prose, ".js") == set()
    assert CENSUS.prefix_refs(prose, ".js", class_bearing_only=True) == set()
    assert CENSUS.class_list_parts("${name} must be an object") == []
    assert CENSUS.class_list_parts("gatebar ${extra}") == []
    assert CENSUS.class_list_parts("gate-${state}") == ["gate-${state}"]
    # a template the rule DOES accept names its static parts as classes and
    # leaves the dynamic one to the prefix, which is the family it names
    js = 'el("div", `chip chip-${state}`);\n'
    assert CENSUS.narrow_refs(js, ".js") == {"div", "chip"}
    assert CENSUS.prefix_refs(js, ".js", class_bearing_only=True) == {"chip-"}
    # and openDox's side is ungated either way: over-reading there KEEPS a rule
    assert CENSUS.prefix_refs('log(`status-${n} written`);\n', ".js") \
        == {"status-"}


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


# ---------------------------------------------------------------------------
# THE MEASUREMENT ITSELF, PINNED (Copilot review, round 14).
# ---------------------------------------------------------------------------

#: The census as measured at the two revisions the manifest cites, MINUS its
#: per-token `census` map (which is 180 kB of namers and says nothing this file
#: asserts). Everything above this line tests the tool's DECISION RULE on
#: fixtures; nothing tested the ANSWER, so a parser regression could have moved
#: the 59 blocks or the 89 lines while every fixture stayed green and the
#: manifest pin — which only compares the manifest with a literal in
#: `test_carve_manifest.py` — stayed green with it.
PINNED_CENSUS = (Path(__file__).resolve().parent / "fixtures"
                 / "q7-css-census-0b4e8bbf-0a0265f7.json")

#: The two revisions it was measured at. `verify-carve-arrival.py`'s own
#: `--dest-root` convention: a checkout, named by environment variable,
#: because this repository carries neither leg.
PINNED_AT = ("0b4e8bbf", "0a0265f7")


def test_the_pinned_census_is_the_figure_the_manifest_cites() -> None:
    """The manifest's `54 gate-exclusive, 18 shared, 59 blocks, 89 lines` and
    the committed measurement are the same four numbers, and the 89 is the
    UNION of the 59 extents rather than a sum of them."""
    report = json.loads(PINNED_CENSUS.read_text(encoding="utf-8"))
    assert report["class_counts_extraction"]["gate_exclusive"] == 54
    assert report["class_counts_extraction"]["shared"] == 18
    assert len(report["gate_exclusive"]) == 54
    assert len(report["shared"]) == 18
    assert len(report["exclusive_blocks"]) == 59
    assert report["exclusive_block_lines"] == 89
    assert report["exclusive_blocks_reading_st"] == 10
    assert report["blocks_kept_for_declaring_a_token"] == []
    assert report["styles_css"]["lines"] == 2595
    union = {line for block in report["exclusive_blocks"]
             for line in range(block["start"], block["end"] + 1)}
    assert len(union) == 89
    assert len(report["gate_modules"]) == 6
    # AND THE FIXTURE IS TIED TO THE MANIFEST, not merely internally consistent
    # (Copilot review, round 15): the row declares 89 `adapter calls` lines and
    # the census measures an 89-line union. The two are counts in DIFFERENT
    # numberings — the manifest's are carve-commit lines, the census's are the
    # leg's own — so what is asserted is the SIZE the act claims in both, which
    # is the claim a stale fixture would break.
    manifest = yaml.safe_load(
        (REPO_ROOT / "docs" / "opendox-carve-manifest.yaml").read_text(
            encoding="utf-8"))
    row = next(r for r in manifest["rows"]
               if r["source_path"] == "scripts/ideation_dashboard/web/styles.css")
    q7 = next(edit for edit in row["edits"]
              if "RULED Q7 — THE CSS EXTRACTION" in edit["note"])
    assert len(q7["lines"]) == len(set(q7["lines"])) == 89 == len(union)


def test_the_pinned_census_re_derives_at_the_cited_revisions(
        tmp_path: Path) -> None:
    """And the tool still ANSWERS it, wherever the two checkouts are.

    Point `Q7_OPENDOX_CODE` and `Q7_OPENXDOX_CODE` at checkouts of `0b4e8bbf`
    and `0a0265f7` and the whole report is re-derived and compared field for
    field with the committed one.

    WITHOUT THEM THIS HOLDS THE SEAT WITH ASSERTIONS AND NEVER A SKIP, which is
    this family's own rule and not a preference — `tests/carve_arrival/
    test_verify_carve_arrival.py` states it of the real-repository test there:
    a skip "reports as a green bar, indistinguishable from a pass to every
    reader, and `pytest-suite.yml` pins the skip count EXACTLY, so a
    conditional skip here would red the required job". MEASURED, because it is
    not hypothetical: this file's first version stood down here, and the first
    CI run of the merged branch reported `skipped=7` against the pinned `6`
    (run `105209771859`, `selected=8181 passed=8174 failures=0 errors=0`) — the
    suite otherwise clean, this test the seventh skip.
    `tests/openxdox_pin/test_openxdox_pin_verifier.py` gives the same rule its
    one-line form: "a check that cannot be reached reports as satisfied" is the
    defect class this suite exists to close.

    WHAT THE SEAT CAN CHECK WITHOUT THE CHECKOUTS is the re-derivation's own
    INPUTS. Four places name the two revisions — the fixture's FILENAME,
    `PINNED_AT`, the manifest row's citation and the census tool's own source —
    and the seat asserts they agree, so a census re-pinned at another pair
    fails here until all four move together instead of leaving an instruction
    nobody can follow. It also asserts the thing a missing checkout must never
    do, which is why this test is where those inputs are named: the documented
    invocation against paths that are not there REFUSES BY NAME rather than
    reporting a census of zero.

    WHAT IT CANNOT DO IS RE-DERIVE, and that is REGISTERED rather than hidden
    (Copilot review of openxFactory #1068, rounds 15 and 17): running the tool
    at two external revisions needs a cross-repository checkout job, whose home
    is `.github/workflows/openxdox-consumer-gate.yml` and not this file.
    """
    dox, xdox = os.environ.get("Q7_OPENDOX_CODE"), os.environ.get("Q7_OPENXDOX_CODE")
    if not dox or not xdox:
        assert PINNED_CENSUS.name == "q7-css-census-{}-{}.json".format(*PINNED_AT)
        manifest = yaml.safe_load(
            (REPO_ROOT / "docs" / "opendox-carve-manifest.yaml").read_text(
                encoding="utf-8"))
        row = next(r for r in manifest["rows"]
                   if r["source_path"] == "scripts/ideation_dashboard/web/styles.css")
        q7 = next(edit for edit in row["edits"]
                  if "RULED Q7 — THE CSS EXTRACTION" in edit["note"])
        assert all(revision in q7["note"] for revision in PINNED_AT), PINNED_AT
        source = SCRIPT.read_text(encoding="utf-8")
        assert all(revision in source for revision in PINNED_AT), PINNED_AT
        refusal = subprocess.run(
            [sys.executable, str(SCRIPT), str(tmp_path / "no-opendox-checkout"),
             str(tmp_path / "no-openxdox-checkout")],
            capture_output=True, text=True, timeout=300)
        assert refusal.returncode != 0, refusal.stdout
        assert "is not a directory" in refusal.stderr, refusal.stderr
        assert "census of zero" in refusal.stderr, refusal.stderr
        return
    with tempfile.TemporaryDirectory() as tmp:
        report = _run(Path(dox), Path(xdox), Path(tmp) / "out.json")
    pinned = json.loads(PINNED_CENSUS.read_text(encoding="utf-8"))
    assert {k: v for k, v in report.items() if k != "census"} == pinned
