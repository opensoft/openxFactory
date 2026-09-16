"""The consumer gate's JUnit adjudicator, EXECUTED rather than read.

`test_openxdox_gate_invocation.py` pins the gate's shape: that the two
assertion bodies are byte-identical, that each carries its five `env:` pins,
that the pinned numbers are the measured ones. None of that runs the
adjudicator. A symmetric edit to both copies — an aggregate summed over the
wrong nodes, a named verdict that stops rejecting `absent`, a floor compared
with `>` instead of `<` — would leave every one of those assertions green and
be found only when the gate itself next ran, which on the day this lands is a
gate no ruleset pins.

SO THIS MODULE EXTRACTS THE SHIPPED BODY AND RUNS IT. The body under test is
read out of `.github/workflows/openxdox-consumer-gate.yml` at test time, never
copied here: a copy would be a second implementation to keep in step, and the
one thing this file must not do is go green against an adjudicator the gate
does not use. The reports are synthesized in `tmp_path` — this suite is
hermetic, reads no network, needs neither submodule, and takes about a second.

WHAT IT PROVES, case by case, is the anti-vacuity contract itself: that a
report at the pins passes; that a watched case which went ABSENT, SKIPPED or
FAILING is refused EVEN WHEN THE AGGREGATES STILL LOOK PERFECT (the sum cannot
see one case, which is the entire reason names are watched); that the exact
skip count refuses the root-shaped 13; that the floors refuse a collection
loss; that failures and errors refuse; and that the walk sums a multi-suite
report as well as a single-suite one.
"""

from __future__ import annotations

import subprocess
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORKFLOW = (REPO_ROOT / ".github" / "workflows" /
            "openxdox-consumer-gate.yml")
JOB_ID = "openxdox-consumer-gate"


def _assertion_steps() -> list[dict]:
    loaded = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = loaded["jobs"][JOB_ID]["steps"]
    found = [s for s in steps if "import xml.etree" in s.get("run", "")]
    assert len(found) == 2, (
        f"expected one adjudicator per suite in {WORKFLOW.name}; found "
        f"{len(found)}")
    return found


ASSERTION_STEPS = _assertion_steps()
#: The one body, read from the workflow. Identity is pinned by
#: `test_the_two_assertion_bodies_are_byte_identical`; asserted again here
#: because THIS file would otherwise silently test only the first copy.
BODY = ASSERTION_STEPS[0]["run"]
assert BODY == ASSERTION_STEPS[1]["run"]
PIN_ENV = {k: str(v) for k, v in ASSERTION_STEPS[0]["env"].items()}
CONSUMER_ENV = {k: str(v) for k, v in ASSERTION_STEPS[1]["env"].items()}
SHIPPED_ENVS = (PIN_ENV, CONSUMER_ENV)


def watched(env: dict[str, str]) -> list[tuple[str, str]]:
    """The `(classname, name)` pairs this env block watches by name."""
    return [tuple(line.partition("::")[::2])  # type: ignore[misc]
            for line in env["NAMED_VERDICTS"].split()]


def report_xml(*, tests: int, skipped: int = 0, failures: int = 0,
               errors: int = 0, cases: list[tuple[str, str, str]],
               wrap: bool = True, split: bool = False) -> str:
    """A JUnit report with the aggregates DECLARED rather than derived.

    Declaring them is the point: the defects this adjudicator exists to catch
    are exactly the ones where the aggregate attributes look right and an
    individual `<testcase>` does not, so the two must be settable apart.
    `wrap=False` emits pytest's single-`testsuite` root; `split=True` emits two
    sibling suites whose attributes sum to the totals.
    """
    body = "".join(
        f'<testcase classname="{c}" name="{n}">'
        + ("" if outcome == "passed" else f'<{outcome} message="synthetic"/>')
        + "</testcase>"
        for c, n, outcome in cases)

    def suite(attrs: dict[str, int], inner: str) -> str:
        rendered = " ".join(f'{k}="{v}"' for k, v in attrs.items())
        return f'<testsuite name="pytest" {rendered}>{inner}</testsuite>'

    totals = {"tests": tests, "skipped": skipped, "failures": failures,
              "errors": errors}
    if split:
        head = {k: v // 2 for k, v in totals.items()}
        tail = {k: v - head[k] for k, v in totals.items()}
        return ("<testsuites>" + suite(head, body) + suite(tail, "")
                + "</testsuites>")
    one = suite(totals, body)
    return f"<testsuites>{one}</testsuites>" if wrap else one


def adjudicate(tmp_path: Path, env: dict[str, str],
               xml: str) -> subprocess.CompletedProcess[str]:
    """Run the SHIPPED body over `xml`, as the runner would."""
    (tmp_path / env["REPORT"]).write_text(xml, encoding="utf-8")
    return subprocess.run(["bash", "-c", BODY], cwd=tmp_path, env=env,
                          capture_output=True, text=True)


def at_the_pins(env: dict[str, str], **over) -> str:
    """A report that satisfies every pin in `env` — the passing baseline."""
    fields = {
        "tests": int(env["MIN_SELECTED"]),
        "skipped": int(env["EXPECT_SKIPPED"]),
        "cases": [(c, n, "passed") for c, n in watched(env)],
    }
    fields.update(over)
    return report_xml(**fields)


# --------------------------------------------------------------------------
# the body under test is the one the gate ships
# --------------------------------------------------------------------------

def test_the_body_under_test_is_extracted_from_the_workflow() -> None:
    """Never a copy: a copy is a second implementation, and it drifts.

    The comparison re-indents by the ten spaces the block scalar strips —
    BOTH copies must be found, because finding one would mean the two had
    diverged and this suite was exercising whichever the extraction reached
    first.
    """
    assert "xml.etree.ElementTree" in BODY
    indented = textwrap.indent(BODY, " " * 10, lambda line: bool(line.strip()))
    assert WORKFLOW.read_text(encoding="utf-8").count(indented) == 2, (
        "the adjudicator executed by this suite must be the text the workflow "
        "ships, in both of its copies; if this fails, either the extraction "
        "stopped matching the file or the two bodies have drifted")


# --------------------------------------------------------------------------
# the passing case, for both shipped pin sets
# --------------------------------------------------------------------------

@pytest.mark.parametrize("env", SHIPPED_ENVS,
                         ids=[e["REPORT"] for e in SHIPPED_ENVS])
def test_a_report_at_the_pins_is_accepted(tmp_path: Path,
                                          env: dict[str, str]) -> None:
    """Both shipped `env:` blocks, through the one body."""
    done = adjudicate(tmp_path, env, at_the_pins(env))
    assert done.returncode == 0, done.stdout + done.stderr
    assert f"skipped={env['EXPECT_SKIPPED']}" in done.stdout
    for classname, name in watched(env):
        assert f"named verdict {classname}::{name}: passed" in done.stdout


@pytest.mark.parametrize("env", SHIPPED_ENVS,
                         ids=[e["REPORT"] for e in SHIPPED_ENVS])
def test_a_margin_above_the_floors_is_accepted(tmp_path: Path,
                                               env: dict[str, str]) -> None:
    """Floors are floors: a suite that GREW must not red the gate."""
    grown = int(env["MIN_SELECTED"]) + 7
    done = adjudicate(tmp_path, env, at_the_pins(env, tests=grown))
    assert done.returncode == 0, done.stdout + done.stderr
    assert "(margin 7)" in done.stdout


def test_a_single_testsuite_root_is_read(tmp_path: Path) -> None:
    """pytest emits `<testsuites>`; a bare `<testsuite>` is still a report."""
    xml = at_the_pins(PIN_ENV).replace("<testsuites>", "").replace(
        "</testsuites>", "")
    done = adjudicate(tmp_path, PIN_ENV, xml)
    assert done.returncode == 0, done.stdout + done.stderr
    assert f"selected={PIN_ENV['MIN_SELECTED']}" in done.stdout


def test_a_multi_suite_report_is_summed_not_sampled(tmp_path: Path) -> None:
    """The walk adds every `<testsuite>`; reading only the first halves it."""
    env = PIN_ENV
    xml = report_xml(tests=int(env["MIN_SELECTED"]),
                     cases=[(c, n, "passed") for c, n in watched(env)],
                     split=True)
    done = adjudicate(tmp_path, env, xml)
    assert done.returncode == 0, done.stdout + done.stderr
    assert f"selected={env['MIN_SELECTED']}" in done.stdout


# --------------------------------------------------------------------------
# the named verdicts — what a sum cannot see
# --------------------------------------------------------------------------

def test_an_absent_watched_case_is_refused_though_the_sums_are_perfect(
        tmp_path: Path) -> None:
    """A deleted or renamed watch must red the gate, never vanish from it."""
    env = CONSUMER_ENV
    xml = report_xml(tests=int(env["MIN_SELECTED"]), cases=[])
    done = adjudicate(tmp_path, env, xml)
    assert done.returncode != 0
    assert "is 'absent'" in done.stdout
    assert "::error::" in done.stdout


def test_a_skipped_watched_case_is_refused_though_the_sums_are_perfect(
        tmp_path: Path) -> None:
    """THE case this watch exists for.

    `node` absent, or a leg not materialized, turns
    `test_recipe_request_carries_recipe_and_reasoned_overrides` into a skip.
    Here the aggregate `skipped` attribute is left at zero on purpose — a
    report can under-report, and a gate that trusted the sum would go green on
    a run that adjudicated nothing.
    """
    env = CONSUMER_ENV
    xml = report_xml(tests=int(env["MIN_SELECTED"]), skipped=0,
                     cases=[(c, n, "skipped") for c, n in watched(env)])
    done = adjudicate(tmp_path, env, xml)
    assert done.returncode != 0
    assert "is 'skipped'" in done.stdout


def test_a_failing_watched_case_is_refused(tmp_path: Path) -> None:
    env = CONSUMER_ENV
    xml = report_xml(tests=int(env["MIN_SELECTED"]),
                     cases=[(c, n, "failure") for c, n in watched(env)])
    done = adjudicate(tmp_path, env, xml)
    assert done.returncode != 0
    assert "is 'failure'" in done.stdout


def test_one_passing_occurrence_does_not_excuse_a_skipped_one(
        tmp_path: Path) -> None:
    """"Any non-passing occurrence wins" — a rerun that skipped is a finding."""
    env = CONSUMER_ENV
    classname, name = watched(env)[0]
    xml = report_xml(tests=int(env["MIN_SELECTED"]),
                     cases=[(classname, name, "passed"),
                            (classname, name, "skipped")])
    done = adjudicate(tmp_path, env, xml)
    assert done.returncode != 0
    assert "is 'skipped'" in done.stdout


def test_every_watched_name_is_adjudicated_not_just_the_first(
        tmp_path: Path) -> None:
    """The pin suites watch FOUR names; the loop must reach the last of them."""
    env = PIN_ENV
    names = watched(env)
    assert len(names) == 4
    kept = [(c, n, "passed") for c, n in names[:-1]]
    done = adjudicate(tmp_path, env,
                      report_xml(tests=int(env["MIN_SELECTED"]), cases=kept))
    assert done.returncode != 0
    assert f"{names[-1][0]}::{names[-1][1]}: absent" in done.stdout


# --------------------------------------------------------------------------
# the counts
# --------------------------------------------------------------------------

def test_the_root_shaped_skip_count_is_refused(tmp_path: Path) -> None:
    """DEPARTURE (b), adjudicated: `tests=1137 skipped=13` must not pass.

    Identical selection, thirteen passes turned into skips. This is the one
    reading a floor cannot see, so it is the one the exact pin exists for.
    """
    env = CONSUMER_ENV
    done = adjudicate(tmp_path, env, at_the_pins(env, skipped=13))
    assert done.returncode != 0
    assert "skipped 13, pinned exactly 0" in done.stdout


def test_a_collection_loss_below_the_floor_is_refused(tmp_path: Path) -> None:
    env = CONSUMER_ENV
    short = int(env["MIN_SELECTED"]) - 1
    done = adjudicate(tmp_path, env, at_the_pins(env, tests=short))
    assert done.returncode != 0
    assert "is BELOW the floor" in done.stdout
    assert "do not lower the floor" in done.stdout


def test_failures_and_errors_are_refused(tmp_path: Path) -> None:
    """An ERROR is how an uninitialized leg reports — `carved_reach` refuses."""
    env = PIN_ENV
    total = int(env["MIN_SELECTED"])
    failing = adjudicate(tmp_path, env, at_the_pins(env, failures=1))
    assert failing.returncode != 0
    assert "1 failure(s)" in failing.stdout
    erroring = adjudicate(tmp_path, env, at_the_pins(env, errors=1))
    assert erroring.returncode != 0
    assert "1 error(s)" in erroring.stdout
    assert f"passed={total - 1}" in erroring.stdout


def test_every_defect_is_reported_not_only_the_first(tmp_path: Path) -> None:
    """The adjudicator accumulates: one run, the whole list of what is wrong."""
    env = CONSUMER_ENV
    xml = report_xml(tests=int(env["MIN_SELECTED"]) - 5, skipped=13,
                     cases=[])
    done = adjudicate(tmp_path, env, xml)
    assert done.returncode != 0
    errors = [line for line in done.stdout.splitlines()
              if line.startswith("::error::")]
    assert len(errors) >= 3, textwrap.indent(done.stdout, "  ")


def test_a_report_that_cannot_be_parsed_fails_the_step(
        tmp_path: Path) -> None:
    """`set -euo pipefail` plus a raising parse: never a silent green."""
    done = adjudicate(tmp_path, PIN_ENV, "<testsuites>")
    assert done.returncode != 0
    assert "ParseError" in done.stderr or "Error" in done.stderr


def test_a_missing_report_fails_the_step(tmp_path: Path) -> None:
    """The suite never ran, or wrote elsewhere; both are the same finding."""
    done = subprocess.run(["bash", "-c", BODY], cwd=tmp_path, env=PIN_ENV,
                          capture_output=True, text=True)
    assert done.returncode != 0
    assert "No such file" in done.stderr or "FileNotFound" in done.stderr


# --------------------------------------------------------------------------
# the synthesizer itself, which must not be the thing that is wrong
# --------------------------------------------------------------------------

def test_the_synthesized_reports_parse_as_the_real_ones_do() -> None:
    """A fixture builder that emitted nonsense would make every case above
    vacuous in the other direction."""
    root = ET.fromstring(at_the_pins(CONSUMER_ENV))
    assert root.tag == "testsuites"
    suites = list(root)
    assert sum(int(s.get("tests", 0)) for s in suites) == int(
        CONSUMER_ENV["MIN_SELECTED"])
    assert [(c.get("classname"), c.get("name"))
            for c in root.iter("testcase")] == watched(CONSUMER_ENV)
