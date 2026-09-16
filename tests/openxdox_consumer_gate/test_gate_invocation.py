"""The openDox/openXdox consumer gate's invocation, pinned as a test.

WHY THIS FILE EXISTS, in the words `tests/openxwallet_consumer_gate/
test_gate_invocation.py` wrote for its own sibling: "This module is collected by
the REQUIRED `pytest-suite` job, so a change to the gate's invocation cannot land
without a second required check going red. A comment in the workflow protects
nothing." That reason is STRONGER here, not weaker, because
`openxdox-consumer-gate` is ADVISORY on the day it lands — no ruleset pins its
token yet (a check is not selectable until a workflow has reported under it
once). Until an operator marks it required, THIS SUITE is the only required
thing standing between the gate and a quiet weakening of it.

WHAT THE GATE CAN LOSE WITHOUT FAILING, which is the whole class these
assertions close. Every one of its steps can go green having adjudicated
nothing:

  * a checkout at the workspace root instead of `openxFactory/` makes both
    validator locators answer `None` and turns thirteen assertions across four
    modules into SKIPS — measured at `cb2d3a2c` both ways, `tests=1137
    skipped=13` root-shaped against `tests=1137 skipped=0` aggregation-shaped,
    IDENTICAL SELECTION either way, which is why the gate pins an exact skipped
    count and not only a floor;
  * a missing `node` turns 41 files' DOM and JS probes into SKIPS;
  * a non-recursive init leaves both `code` legs empty, and
    `scripts/carved_reach.py` refuses BY NAME — which reports as a collection
    ERROR, not as a pass, but only for as long as the suite that reaches the
    legs is actually run;
  * and a suite that stops being collected reports nothing whatever.

None of those is a failing test, so none of them reds a `pytest` exit code. The
workflow answers them with floors, an EXACT skipped count and named verdicts;
this file answers the layer above — that those pins are still THERE, still
literal, and still naming tests that exist.

ON RULING R-4, WHICH IS WHY THERE IS NO `jobs:` KEY TO RETAIN. `tasks.md` § 5.3
says "retaining the job id so a ruleset-pinned token survives a file rename".
RULING R-4 (Brett Heap, `opensoft/openxFactory#656` comment `5690428146`,
2026-09-16, by interactive multi-choice) discharges that clause by leaving
`pytest-suite` untouched, there being no dashboard-named workflow here to
rename. `test_the_required_pytest_suite_token_is_untouched_by_this_gate` is that
discharge asserted rather than asserted-in-prose.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORKFLOWS = REPO_ROOT / ".github" / "workflows"
WORKFLOW = WORKFLOWS / "openxdox-consumer-gate.yml"

#: The job id, which is the token an operator will pin in a ruleset. It is the
#: JOB ID and never the filename — the wallet gate's own hard-won distinction,
#: applied here before the pin exists rather than after.
JOB_ID = "openxdox-consumer-gate"

#: The checkout path. Load-bearing: the consumer suite's validator locators walk
#: UP for an `openxFactory/`-shaped ancestor.
CHECKOUT_PATH = "openxFactory"

OPENXDOX_PIN_RUN = "python3 scripts/verify-openxdox-pin.py"
OPENDOX_PIN_RUN = "python3 scripts/verify-opendox-pin.py"
SCOPED_INIT_RUN = "git submodule update --init --recursive openDox openXdox"

PIN_SUITES_RUN = (
    "python3 -m pytest tests/opendox_pin tests/openxdox_pin -q "
    '-m "not postgres" --junitxml=pin-suites-report.xml')
CONSUMER_SUITE_RUN = (
    "python3 -m pytest tests/ideation-dashboard -q "
    '-m "not postgres" --junitxml=consumer-suite-report.xml')

#: The four cases in the pin suites that cannot pass unless the two pinned trees
#: are really on disk.
PIN_NAMED_VERDICTS = (
    "tests.opendox_pin.test_opendox_pin_verifier"
    "::test_the_shipped_digest_is_recomputed_by_an_independent_implementation",
    "tests.opendox_pin.test_opendox_pin_verifier"
    "::test_the_real_pin_is_in_lockstep_with_openxdox_own_derived_reading",
    "tests.openxdox_pin.test_openxdox_pin_verifier"
    "::test_the_shipped_digest_is_recomputed_by_an_independent_implementation",
    "tests.openxdox_pin.test_openxdox_pin_verifier"
    "::test_ruling_q7_two_direct_upstreams_in_lockstep",
)

#: The one case in the consumer suite that proves node, both legs, and
#: `carved_reach`'s per-row mount lookup, all at once.
CONSUMER_NAMED_VERDICTS = (
    "tests.ideation-dashboard.test_lens"
    "::test_recipe_request_carries_recipe_and_reasoned_overrides",
)


@pytest.fixture(scope="module")
def workflow() -> dict:
    assert WORKFLOW.is_file(), (
        f"{WORKFLOW} is missing; task 5.3's consumer gate has no workflow to "
        f"report from")
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def gate_job(workflow: dict) -> dict:
    assert list(workflow["jobs"]) == [JOB_ID], (
        f"`jobs:` must contain exactly the key {JOB_ID!r} — it is the token an "
        f"operator pins in a ruleset, and a second job here would report a "
        f"second token nobody declared. Found: {sorted(workflow['jobs'])}")
    return workflow["jobs"][JOB_ID]


@pytest.fixture(scope="module")
def steps(gate_job: dict) -> list[dict]:
    return list(gate_job["steps"])


@pytest.fixture(scope="module")
def runs(steps: list[dict]) -> list[str]:
    return [step["run"] for step in steps if "run" in step]


def _step_with(steps: list[dict], needle: str) -> dict:
    matches = [s for s in steps if needle in s.get("run", "")]
    assert len(matches) == 1, (
        f"exactly one step may carry {needle!r}; found {len(matches)}")
    return matches[0]


# --------------------------------------------------------------------------
# the token, the trigger, and R-4's discharge
# --------------------------------------------------------------------------

def test_the_gate_job_carries_no_display_name(gate_job: dict) -> None:
    """A display name replaces the token in the check list and de-advises it.

    The wallet gate learned this against a LIVE ruleset. Applying it before the
    pin exists costs nothing; applying it afterwards costs a red required check
    on a human-only surface.
    """
    assert "name" not in gate_job, (
        "the gate job must carry no `name:` — the status check has to surface "
        "as exactly `openxdox-consumer-gate`, which is the token an operator "
        "will select, and a display name silently renames it")


def test_the_gate_runs_on_pull_requests_to_main(workflow: dict) -> None:
    """The wallet gate's trigger set, mirrored — RULING R-4's named shape."""
    triggers = workflow[True] if True in workflow else workflow["on"]
    assert list(triggers) == ["pull_request"], (
        f"the gate mirrors `openxwallet-consumer-gate.yml`'s triggers, which "
        f"are `pull_request` and nothing else; found {sorted(triggers)}")
    assert triggers["pull_request"]["branches"] == ["main"]


def test_the_required_pytest_suite_token_is_untouched_by_this_gate() -> None:
    """RULING R-4's own discharge of "retaining the job id".

    There was no dashboard-named workflow to rename, so the clause is
    discharged by `pytest-suite` keeping its job id — and by this gate not
    declaring that id, which would make two workflows report one token and let
    whichever ran the weaker gate satisfy it.
    """
    pytest_suite = WORKFLOWS / "pytest-suite.yml"
    assert pytest_suite.is_file()
    loaded = yaml.safe_load(pytest_suite.read_text(encoding="utf-8"))
    assert "pytest-suite" in loaded["jobs"], (
        "`pytest-suite.yml` must still declare `jobs: pytest-suite:` — R-4 "
        "discharges § 5.3's 'retaining the job id' clause by leaving that "
        "token untouched")
    gate = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert "pytest-suite" not in gate["jobs"], (
        "this gate must not declare the job id `pytest-suite`; two workflows "
        "reporting one token is the defect the wallet gate's rename had to be "
        "designed around")


def test_no_dashboard_named_workflow_was_converted() -> None:
    """R-4's premise, asserted so a later reader need not re-measure it.

    "no dashboard-named workflow ever existed here" — the dashboard WORKERS
    live in the `opensoft/xFactory` aggregation. If one ever arrives in this
    repository, § 5.3's original "convert" verb becomes live again and this
    gate's header stops being the whole story.
    """
    dashboard_named = sorted(
        p.name for p in WORKFLOWS.glob("*.yml")
        if "dashboard" in p.name or "ideation" in p.name)
    assert dashboard_named == [], (
        f"a dashboard-named workflow exists in this repository: "
        f"{dashboard_named}. RULING R-4 was given on the premise that none "
        f"does; re-read § 5.3 rather than assuming this gate covers it")


# --------------------------------------------------------------------------
# the checkout, the init, and the two departures from the wallet shape
# --------------------------------------------------------------------------

def test_the_ssh_url_is_rewritten_before_checkout(steps: list[dict]) -> None:
    """`insteadOf` after checkout is `insteadOf` too late for a nested clone."""
    rewrite = next(i for i, s in enumerate(steps)
                   if "insteadOf" in s.get("run", ""))
    checkout = next(i for i, s in enumerate(steps)
                    if str(s.get("uses", "")).startswith("actions/checkout"))
    assert rewrite < checkout
    assert steps[rewrite].get("working-directory") == ".", (
        "the rewrite runs BEFORE the checkout, so it cannot run inside the "
        "directory the checkout has not created yet; it must override the "
        "job's `defaults.run.working-directory` with `.`")


def test_the_checkout_lands_at_the_aggregation_shaped_path(
        gate_job: dict, steps: list[dict]) -> None:
    """DEPARTURE (b), and the one that separates a gate from a green bar.

    `human_seen.find_cross_reference_validator` walks each ancestor looking for
    `openxFactory/scripts/validate-ideation-cross-reference.py`, and
    `tests/ideation-dashboard/conftest.py`'s `find_openxfactory_validator` does
    the same for the dashboard validator. A workspace-root checkout has no such
    ancestor; both answer `None`; thirteen assertions turn into skips.
    `pytest-suite.yml` already checks out to this path for this reason.

    A FLOOR CANNOT SEE THIS: `skipif` marks a collected test rather than
    uncollecting it, so selection is 1137 under either layout.
    """
    checkout = next(s for s in steps
                    if str(s.get("uses", "")).startswith("actions/checkout"))
    assert checkout["with"]["path"] == CHECKOUT_PATH, (
        f"the checkout must land at {CHECKOUT_PATH!r}; a root checkout makes "
        f"both validator locators answer None and turns the consumer suite's "
        f"validator-gated cases into skips")
    assert gate_job["defaults"]["run"]["working-directory"] == CHECKOUT_PATH, (
        "the job's default working directory must be the checkout path, or "
        "every `run:` below executes in an empty workspace root")


def test_the_checkout_does_not_use_a_blanket_submodule_init(
        steps: list[dict]) -> None:
    """`submodules: true` would also fetch `installs/omnigent-install`."""
    for step in steps:
        if str(step.get("uses", "")).startswith("actions/checkout"):
            assert not step.get("with", {}).get("submodules"), (
                "the checkout must not declare `submodules:`; the init is a "
                "separate, scoped step")


def test_the_submodule_init_is_scoped_to_the_two_consumed_gitlinks(
        runs: list[str]) -> None:
    """DEPARTURE (a): recursive, because the consumer suite reads both legs.

    `scripts/carved_reach.py`'s `install()` needs `openDox/code/src` AND
    `openXdox/code/src` on disk and REFUSES rather than degrading. The SCOPING
    the wallet gate is really asserting is kept: `openXwallet` and
    `installs/omnigent-install` are not initialized, because nothing here reads
    them.
    """
    inits = [r for r in runs if "submodule update" in r]
    assert inits == [SCOPED_INIT_RUN], (
        f"the gate must init exactly the two consumed gitlinks, recursively; "
        f"found {inits}")
    for absent in ("openXwallet", "omnigent-install"):
        assert absent not in inits[0], (
            f"{absent} must not be initialized here; no step in this gate "
            f"reads it, and a blanket init is what the wallet gate's scoped "
            f"discipline refuses")


def test_node_is_installed_because_the_js_probes_skip_without_it(
        steps: list[dict]) -> None:
    """The named verdict below depends on it; a skip reports as a green bar."""
    node = [s for s in steps
            if str(s.get("uses", "")).startswith("actions/setup-node")]
    assert len(node) == 1, (
        "the gate must set up node: 41 test files gate their DOM and JS probes "
        "on `shutil.which('node')` and SKIP without it, and the consumer "
        "suite's named verdict is one of them")
    assert str(node[0]["with"]["node-version"]) == "22", (
        "node is pinned to the same major `pytest-suite.yml` installs so the "
        "two gates cannot disagree about what the browser-side modules parse "
        "as")


# --------------------------------------------------------------------------
# the invocations, and their order
# --------------------------------------------------------------------------

def test_both_pins_are_verified_before_anything_pinned_is_trusted(
        runs: list[str]) -> None:
    """Neither pinned tree may be read by a suite before its pin verifies."""
    for invocation in (OPENXDOX_PIN_RUN, OPENDOX_PIN_RUN):
        assert invocation in runs, (
            f"the gate must run {invocation!r} — this gate exists because "
            f"NOTHING in `.github/workflows/` invoked either verifier, which "
            f"`pytest-suite.yml`'s own comment and both pin files' "
            f"`verify_pin:` comments name as owed to task 5.3")
        assert runs.index(invocation) < runs.index(PIN_SUITES_RUN)
        assert runs.index(invocation) < runs.index(CONSUMER_SUITE_RUN)


def test_the_openxdox_pin_is_verified_first(runs: list[str]) -> None:
    """The direction the LOCKSTEP runs.

    `verify-opendox-pin.py`'s sixth check reads openXdox's own DERIVED
    `contracts/opendox-pin.yaml` as a git blob at the gitlinked commit. Both
    verifiers are offline and order-independent in principle; running the elder
    pin (RULING F) before the second direct upstream (RULED Q7) means the
    refusal a reader meets first is the one nearer the root of the chain.
    """
    assert runs.index(OPENXDOX_PIN_RUN) < runs.index(OPENDOX_PIN_RUN)


def test_the_two_suites_are_invoked_exactly_and_separately(
        runs: list[str]) -> None:
    """The literal invocations, and two reports rather than one.

    One combined run would let one suite's growth mask the other's collapse,
    which is the wallet gate's "add one for the new wallet, do not widen the
    existing one" rule applied to suites.
    """
    assert PIN_SUITES_RUN in runs, (
        f"the pin verifiers' own suites must be run exactly as "
        f"{PIN_SUITES_RUN!r}; they are what make each shipped digest a "
        f"MEASURED fact rather than a self-consistent one")
    assert CONSUMER_SUITE_RUN in runs, (
        f"the consumer suite must be run exactly as {CONSUMER_SUITE_RUN!r}; a "
        f"pin whose bytes verify while the code that consumes them cannot "
        f"import is a green check that proved half its claim")
    assert runs.index(PIN_SUITES_RUN) < runs.index(CONSUMER_SUITE_RUN)
    assert "pin-suites-report.xml" not in CONSUMER_SUITE_RUN
    assert "consumer-suite-report.xml" not in PIN_SUITES_RUN


def test_no_suite_invocation_swallows_its_own_exit_code(
        runs: list[str]) -> None:
    """`|| true` over a pytest run makes every assertion below it decorative."""
    for invocation in (PIN_SUITES_RUN, CONSUMER_SUITE_RUN,
                       OPENXDOX_PIN_RUN, OPENDOX_PIN_RUN):
        assert "||" not in invocation and "; true" not in invocation


# --------------------------------------------------------------------------
# the positive assertions
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def assertion_steps(steps: list[dict]) -> list[dict]:
    found = [s for s in steps if "import xml.etree" in s.get("run", "")]
    assert len(found) == 2, (
        f"the gate must carry one positive assertion per suite; found "
        f"{len(found)}")
    return found


def test_each_suite_is_followed_immediately_by_its_own_assertion(
        steps: list[dict]) -> None:
    """Beside the run it adjudicates, so the numbers sit next to the command."""
    for suite_run, report in ((PIN_SUITES_RUN, "pin-suites-report.xml"),
                              (CONSUMER_SUITE_RUN,
                               "consumer-suite-report.xml")):
        index = next(i for i, s in enumerate(steps)
                     if s.get("run") == suite_run)
        following = steps[index + 1]
        assert "import xml.etree" in following.get("run", ""), (
            f"the step after {suite_run!r} must be its positive assertion")
        assert following["env"]["REPORT"] == report, (
            f"the assertion after {suite_run!r} must read {report!r}, not "
            f"{following['env']['REPORT']!r} — an assertion reading the wrong "
            f"report adjudicates the wrong suite and can pass twice over one "
            f"of them")
        assert following.get("shell") == "bash", (
            "the assertion step must declare `shell: bash` so it runs under "
            "`-o pipefail` and `set -euo pipefail` means what it says")


def test_the_two_assertion_bodies_are_byte_identical(
        assertion_steps: list[dict]) -> None:
    """The rule is written once; the PINS are written twice.

    GitHub Actions supports no YAML anchor and no include, so identity under
    test is the mechanism available. Without this, two adjudicators can drift —
    one gaining a check the other never gets — and the gate's weaker half
    becomes the one that decides.
    """
    first, second = (s["run"] for s in assertion_steps)
    assert first == second, (
        "the two assertion bodies must be byte-identical; they differ only in "
        "their `env:` pins. Diff them and make the edit in both")


def test_every_assertion_pins_floors_an_exact_skip_and_named_verdicts(
        assertion_steps: list[dict]) -> None:
    for step in assertion_steps:
        env = step["env"]
        for key in ("REPORT", "MIN_SELECTED", "MIN_PASSED", "EXPECT_SKIPPED",
                    "NAMED_VERDICTS"):
            assert key in env, (
                f"{step['name']!r} is missing {key} — every one of the five is "
                f"load-bearing: without the floors a directory can stop being "
                f"collected, without the exact skip a suite can turn into a "
                f"green bar, and without the named verdicts a sum can hide a "
                f"case that stopped running")
        assert int(env["MIN_SELECTED"]) > 0
        assert int(env["MIN_PASSED"]) > 0
        assert int(env["EXPECT_SKIPPED"]) >= 0
        assert env["NAMED_VERDICTS"].split(), "NAMED_VERDICTS may not be empty"


def test_the_pin_suites_pin_zero_skips_exactly(
        assertion_steps: list[dict]) -> None:
    """Zero is what both pin suites are BUILT to guarantee, not luck.

    Their own docstrings: "Every case is hermetic: no network, no ambient git",
    and "a conditionally-skipped test here would red the required check on
    every tree that skipped it". A skip appearing there is a finding about
    hermeticity, not a fact about the runner.
    """
    step = next(s for s in assertion_steps
                if s["env"]["REPORT"] == "pin-suites-report.xml")
    assert step["env"]["EXPECT_SKIPPED"] == "0"


def test_the_watched_names_are_the_ones_that_read_the_real_trees(
        assertion_steps: list[dict]) -> None:
    pins = {s["env"]["REPORT"]: tuple(s["env"]["NAMED_VERDICTS"].split())
            for s in assertion_steps}
    assert pins["pin-suites-report.xml"] == PIN_NAMED_VERDICTS
    assert pins["consumer-suite-report.xml"] == CONSUMER_NAMED_VERDICTS


def test_every_watched_name_resolves_to_a_test_that_exists() -> None:
    """A watch on a test that is not there reds the gate on every run.

    The workflow's own message tells an editor to move NAMED_VERDICTS with a
    renamed test "in the same diff". This is that instruction made enforceable
    HERE, on a developer machine, rather than discovered on a runner: the
    classname is a dotted path to the module file and the name is a `def` in
    it.
    """
    for watched in PIN_NAMED_VERDICTS + CONSUMER_NAMED_VERDICTS:
        classname, _, name = watched.partition("::")
        module = REPO_ROOT / (classname.replace(".", "/") + ".py")
        assert module.is_file(), (
            f"{watched} names {module}, which does not exist — a watch on a "
            f"module that moved reds the gate on every run")
        assert f"def {name}(" in module.read_text(encoding="utf-8"), (
            f"{module} carries no `def {name}(` — the watched case was renamed "
            f"or removed without moving NAMED_VERDICTS with it")


# --------------------------------------------------------------------------
# the credential that is not here
# --------------------------------------------------------------------------

def test_the_gate_mints_no_credential_for_public_gitlinks(
        steps: list[dict]) -> None:
    """All three gitlinks are public; `github.token` resolves them.

    ASSERTED AT BOTH LEVELS, on the wallet suite's own reasoning: the parsed
    form catches a mint step under any name, and the raw-text form catches a
    secret arriving by some other route — an `env` guard, a `with` value, a
    shell interpolation — which a step-shaped probe alone would miss. It is
    CONSUMPTION that is forbidden and not the NAME, so `${{ secrets. }}` is the
    only spelling asserted absent.
    """
    mints = [s.get("name") or s.get("uses") for s in steps
             if "create-github-app-token" in str(s.get("uses", ""))]
    assert mints == [], (
        f"the gate must mint no App token for PUBLIC gitlinks; found {mints}. "
        f"If openDox or openXdox ever goes private, add the mint with its "
        f"reason rather than around this test")
    assert "secrets." not in WORKFLOW.read_text(encoding="utf-8"), (
        "the gate consumes a repository or organization secret; it needs none, "
        "and a token minted for a public read widens its permissions for "
        "nothing — `openreposhape-pin-gate.yml`'s own rule")
