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

  * a checkout at the workspace root instead of `openxFactory/` makes the
    CROSS-REFERENCE validator locator answer `None` and turns thirteen
    assertions across four modules into SKIPS — measured at `cb2d3a2c` both
    ways, `tests=1137 skipped=13` root-shaped against `tests=1137 skipped=0`
    aggregation-shaped, IDENTICAL SELECTION either way, which is why the gate
    pins an exact skipped count and not only a floor;
  * a missing `node` turns the FOURTEEN JS-probe cases of
    `tests/ideation-dashboard/test_lens.py` into SKIPS — measured with node off
    `PATH`: the whole consumer suite reports `tests=1137 skipped=14`;
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

ON THIS FILE'S OWN NAME, WHICH IS A DEFECT THIS SUITE SHIPPED AND THEN PINNED.
It was born as `test_gate_invocation.py` — the wallet suite's basename, copied
along with its shape — and `pytest-suite` refused it on the first push with
`import file mismatch`, INTERRUPTING THE WHOLE REQUIRED RUN at 2 collected
rather than failing one file. Neither consumer-gate directory carries an
`__init__.py`, so pytest's prepend import mode named both modules
`test_gate_invocation` and only one could exist. The rename fixes this file;
`test_no_two_test_modules_resolve_to_the_same_import_name` fixes the CLASS, on
a developer machine, for whoever writes the third consumer gate.
"""

from __future__ import annotations

import ast
import collections
import re
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

#: THE MEASURED PINS THEMSELVES, per report: `(MIN_SELECTED, MIN_PASSED,
#: EXPECT_SKIPPED)`, taken from this gate's own CI run (35044247836, head
#: `e4602a4c`) — `pin-suites-report.xml: selected=105 passed=105 skipped=0` and
#: `consumer-suite-report.xml: selected=1137 passed=1137 skipped=0`.
#:
#: PINNED AS LITERALS AND NOT MERELY AS SHAPES, which is a distinction with a
#: defect behind it. A guard that only asks `MIN_SELECTED > 0` stays green
#: while both floors are lowered to `1` and the consumer `EXPECT_SKIPPED` is
#: moved from `0` to `13` — which is precisely the root-shaped reading
#: departure (b) exists to refuse, and the gate would then pass having
#: adjudicated nothing while its only REQUIRED guard still passed. The floors
#: may still only RISE; this makes moving them a two-file diff a reviewer sees
#: rather than a one-character edit inside a workflow nobody reads.
MEASURED_PINS = {
    "pin-suites-report.xml": ("105", "105", "0"),
    "consumer-suite-report.xml": ("1137", "1137", "0"),
}


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

    WHAT IS PINNED HERE IS THE TOKEN, NOT THE FILE, and the difference is
    deliberate. This asserts that `pytest-suite.yml` still declares the job id
    a ruleset selects and that this gate does not declare it too; it does NOT
    pin that workflow's bytes, and a digest of it here would red on every
    lawful later edit to somebody else's required workflow — which is a
    different act from wiring a consumer gate, and would make this suite the
    reason that act could not land. The byte-untouchedness claimed for THIS
    act is a property of its diff, not of the tree: the pull request that adds
    this gate touches three files and none of them is `pytest-suite.yml`,
    which a reader verifies in the diff rather than here.
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

    BOTH SUFFIXES, because Actions loads `.yaml` as readily as `.yml` and this
    repository's fourteen workflow files happen to use only the one. A premise
    guard that globs `*.yml` alone would report "no dashboard workflow exists"
    over a real `ideation-dashboard.yaml` — MEASURED by dropping exactly that
    file in: the single-suffix reading returns `[]` and this one names it.
    """
    workflow_files = [p for suffix in ("*.yml", "*.yaml")
                      for p in WORKFLOWS.glob(suffix)]
    dashboard_named = sorted(
        p.name for p in workflow_files
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
    assert steps[rewrite]["run"].strip() == (
        'git config --global url."https://github.com/".insteadOf '
        '"git@github.com:"')
    assert steps[rewrite].get("working-directory") == ".", (
        "the rewrite runs BEFORE the checkout, so it cannot run inside the "
        "directory the checkout has not created yet; it must override the "
        "job's `defaults.run.working-directory` with `.`")
    assert "env" not in steps[rewrite], (
        "the rewrite step must not inject a bearer into the global git config; "
        "the initialized gitlinks are public and an anonymous HTTPS rewrite is "
        "sufficient")


def test_the_checkout_lands_at_the_aggregation_shaped_path(
        gate_job: dict, steps: list[dict]) -> None:
    """DEPARTURE (b), and the one that separates a gate from a green bar.

    THE LOCATOR THAT DECIDES IT IS THE CROSS-REFERENCE ONE.
    `human_seen.find_cross_reference_validator` walks each ancestor looking for
    `openxFactory/scripts/validate-ideation-cross-reference.py`; a
    workspace-root checkout has no such ancestor, it answers `None`, and
    thirteen assertions turn into skips.
    `tests/ideation-dashboard/conftest.py`'s `find_openxfactory_validator` is
    NOT the one that moves, and saying otherwise would send a later edit at the
    wrong dependency: since the § 5.2 shed its second rung COMPOSES the
    dashboard validator out of the pinned leg (`_shed_validator()`), so it
    resolves under either layout once the legs are on disk. Measured at
    `cb2d3a2c`: twelve of the thirteen are gated
    `VALIDATOR is None or XREF_VALIDATOR is None`, the thirteenth on
    `XREF_VALIDATOR is None` alone, and
    `test_lens::test_manifest_with_new_candidates_validates_clean` — gated on
    `VALIDATOR is None` ALONE — passes in the root-shaped run.
    `pytest-suite.yml` already checks out to this path for this reason.

    A FLOOR CANNOT SEE THIS: `skipif` marks a collected test rather than
    uncollecting it, so selection is 1137 under either layout.

    EXACTLY ONE CHECKOUT, asserted before its path is read. "The first
    `actions/checkout` lands at `openxFactory/`" is satisfied by a job that
    checks out twice — the second one at the workspace root, where a later
    `working-directory`, a submodule init or a bare `pytest` would then run —
    and every other assertion in this file that says "the checkout" reads the
    first as well. The count is the assertion that makes those readings true,
    so it is made here, once, rather than assumed five times.
    """
    checkouts = [s for s in steps
                 if str(s.get("uses", "")).startswith("actions/checkout")]
    assert len(checkouts) == 1, (
        f"the gate must take exactly ONE checkout; found {len(checkouts)}. A "
        f"second one materializes a second tree — at the workspace root, most "
        f"likely — and every guard here that reads 'the checkout' reads the "
        f"first, so a root-shaped tree could arrive with all of them green. "
        f"If a second checkout is ever needed, give it a path and re-aim these "
        f"assertions at the one that hosts the suites")
    checkout = checkouts[0]
    assert checkout["with"]["path"] == CHECKOUT_PATH, (
        f"the checkout must land at {CHECKOUT_PATH!r}; a root checkout makes "
        f"the cross-reference validator locator answer None and turns the "
        f"consumer suite's cross-reference-gated cases into skips")

    # WHICH TREE, not just where it lands. `actions/checkout` defaults to THIS
    # repository at the pull request's MERGE ref, which is the only tree whose
    # adjudication means anything on a pull request. `ref: main` would judge
    # the base, `ref: ${{ github.event.pull_request.head.sha }}` the unmerged
    # head, and `repository:` somebody else's tree entirely — each of them
    # leaving every assertion in this file green while the gate reported on
    # something other than what is being landed.
    for defaulted in ("ref", "repository"):
        assert defaulted not in checkout["with"], (
            f"the checkout must not declare `{defaulted}:`. Its defaults — "
            f"this repository, at the pull request's merge ref — are what "
            f"make a green report evidence about the landing; overriding "
            f"either one leaves this suite passing over a gate that "
            f"adjudicated a different tree")
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
            assert step.get("with", {}).get("persist-credentials") is False, (
                "the checkout must set `persist-credentials: false` so the "
                "runner does not leave a bearer in the repository config before "
                "pytest executes pull-request-controlled code")


def test_the_submodule_init_is_scoped_to_the_two_consumed_gitlinks(
        runs: list[str]) -> None:
    """DEPARTURE (a): recursive, because the consumer suite reads both legs.

    `scripts/carved_reach.py`'s `install()` needs `openDox/code/src` AND
    `openXdox/code/src` on disk and REFUSES rather than degrading — and 42
    files in this repository reach a carved module through it, at 207 helper
    sites, so the refusal is not a corner case. The SCOPING
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
    """The named verdict below depends on it; a skip reports as a green bar.

    MEASURED rather than counted by eye, because an earlier draft of this
    suite and of the workflow header said "41 test files" — a figure that
    belongs to the pinned LEGS' own suites (28 node-gated files in
    `openDox/code/tests`, 22 in `openXdox/code/tests`), which this gate does
    not run. openxFactory's own `tests/` tree has exactly ONE such file, and
    with node off `PATH` the whole consumer suite reports `tests=1137
    skipped=14`, every skip in that module and every one of them reading "node
    not available for the JS derivation probe".
    """
    node = [s for s in steps
            if str(s.get("uses", "")).startswith("actions/setup-node")]
    assert len(node) == 1, (
        "the gate must set up node: fourteen test functions in "
        "`tests/ideation-dashboard/test_lens.py` route through harness helpers "
        "that `pytest.skip` without `shutil.which('node')`, and the consumer "
        "suite's named verdict is one of them")
    assert str(node[0]["with"]["node-version"]) == "22", (
        "node is pinned to the same major `pytest-suite.yml` installs so the "
        "two gates cannot disagree about what the browser-side modules parse "
        "as")


def test_the_dependency_install_is_hash_pinned_and_refuses_sdists(
        runs: list[str]) -> None:
    """Hashes bind WHICH artifact; `--only-binary :all:` binds WHAT KIND.

    A gate that judges other people's landings should not run a stranger's
    `setup.py` while installing itself, and a hash cannot express that — it
    pins the sdist's bytes, then the build executes them.
    `former-id-arrival-gate.yml` made this the rule for a hashed-lockfile
    install in this repository; measured against the same lock on python 3.12,
    the flag resolves 17 packages, 17 wheels, zero sdists, exit 0, so it
    changes what may EXECUTE and nothing about what is installed.
    """
    installs = [r for r in runs if "pip install" in r]
    assert len(installs) == 1, (
        f"exactly one dependency install; found {len(installs)}")
    install = " ".join(installs[0].split())
    assert "--require-hashes" in install, (
        "the install must be hash-pinned: an unpinned `pip install` resolves "
        "whatever PyPI serves at run time, with no version and no hash")
    assert "--only-binary :all:" in install, (
        "the install must refuse sdists — no setup script may run while a "
        "gate installs itself. The lock is all wheels, so this costs nothing")
    assert "requirements/hermes-runtime-contracts.lock" in install, (
        "the gate installs the same locked set the required suite does")


def test_the_watched_consumer_case_really_depends_on_node() -> None:
    """The load-bearing half of the node claim, asserted rather than counted.

    A COUNT rots — this suite shipped "41 test files" and the number was never
    right for the suites this gate runs. What actually matters is narrower and
    stable: the one consumer case watched BY NAME routes through a harness
    helper that `pytest.skip`s when `shutil.which("node")` is `None`. That is
    the whole reason installing node keeps that verdict from being a green
    bar, and if the watched case is ever rewired to a node-free path, this
    fails and the `setup-node` step must be re-justified rather than kept out
    of habit.
    """
    classname, _, name = CONSUMER_NAMED_VERDICTS[0].partition("::")
    module = REPO_ROOT / (classname.replace(".", "/") + ".py")
    source = module.read_text(encoding="utf-8")
    assert 'shutil.which("node")' in source, (
        f"{module} no longer resolves node with `shutil.which`; the gate's "
        f"`setup-node` step is justified by that gate")
    tree = ast.parse(source)
    node_helpers = {
        fn.name for fn in tree.body
        if isinstance(fn, ast.FunctionDef)
        and "NODE" in ast.dump(fn) and "skip" in ast.dump(fn)}
    assert node_helpers, (
        f"{module} carries no helper that skips without node; re-measure the "
        f"claim in this gate's header before trusting it")
    watched = next(fn for fn in tree.body
                   if isinstance(fn, ast.FunctionDef) and fn.name == name)
    called = {call.func.id for call in ast.walk(watched)
              if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)}
    assert called & node_helpers, (
        f"the watched case {name} no longer routes through any of "
        f"{sorted(node_helpers)} — it does not depend on node any more, so a "
        f"`passed` verdict on it no longer proves node was installed. Move "
        f"the watch, or re-justify the `setup-node` step")


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

    `verify-opendox-pin.py`'s CHECK 5 — its last, and the one check with no
    analogue in the elder verifier — reads openXdox's own DERIVED
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


def test_nothing_here_continues_on_error(gate_job: dict,
                                         steps: list[dict]) -> None:
    """`continue-on-error: true` is `|| true` spelled in YAML, and worse.

    A shell swallow at least leaves the step red-able by the next command;
    this flag marks a NON-ZERO EXIT SUCCESSFUL. On a pin verifier it would
    ignore a named refusal; on an assertion step it would ignore the whole
    anti-vacuity layer while the check still reported green. Neither the job
    nor any step may carry it — and the assertion is over EVERY step rather
    than a list of the critical ones, because the list would be the thing that
    goes stale when a step is added.
    """
    assert gate_job.get("continue-on-error") in (None, False), (
        "the job must not continue on error; a failing step would then be "
        "reported as a successful check")
    for step in steps:
        label = step.get("name") or step.get("uses")
        assert step.get("continue-on-error") in (None, False), (
            f"step {label!r} carries `continue-on-error` — a non-zero exit "
            f"would be marked successful, which is exactly what this gate's "
            f"refusals exist to prevent")


def test_the_equipment_is_installed_before_the_work_that_needs_it(
        steps: list[dict]) -> None:
    """ORDER, not just presence — a shape check cannot see a reordering.

    "The gate installs a hash-pinned, wheel-only lock" is satisfied by a
    workflow that installs it AFTER the verifiers and both suites have already
    run against whatever the runner image happened to carry. The numbers this
    gate pins were measured on the locked set; adjudicating with another one
    and installing the lock afterwards would leave every assertion in this
    file green and the report meaningless. The same holds for the interpreter
    and for `node`: `setup-python` after the install would pip into one
    interpreter and test in another, and `setup-node` after the consumer suite
    would turn the fourteen JS-probe cases into skips that `EXPECT_SKIPPED: 0`
    would then refuse — loudly, but one CI cycle later than here.
    """
    def index(predicate, what: str) -> int:
        found = [i for i, step in enumerate(steps) if predicate(step)]
        assert len(found) == 1, (
            f"expected exactly one {what} step; found {len(found)}")
        return found[0]

    setup_python = index(
        lambda s: str(s.get("uses", "")).startswith("actions/setup-python"),
        "setup-python")
    setup_node = index(
        lambda s: str(s.get("uses", "")).startswith("actions/setup-node"),
        "setup-node")
    install = index(lambda s: "pip install" in s.get("run", ""),
                    "dependency install")

    assert setup_python < install, (
        "`setup-python` must run BEFORE the install, or the lock lands in the "
        "image's interpreter and the suites run in another")
    for run, what in ((OPENXDOX_PIN_RUN, "openXdox verifier"),
                      (OPENDOX_PIN_RUN, "openDox verifier"),
                      (PIN_SUITES_RUN, "pin suites"),
                      (CONSUMER_SUITE_RUN, "consumer suite")):
        at = index(lambda s, r=run: r in s.get("run", ""), what)
        assert install < at, (
            f"the dependency install must run BEFORE the {what}; this gate's "
            f"pinned numbers were measured on the locked set, and a gate that "
            f"adjudicates with the image's packages and installs the lock "
            f"afterwards reports on something else entirely")
    consumer = index(lambda s: CONSUMER_SUITE_RUN in s.get("run", ""),
                     "consumer suite")
    assert setup_node < consumer, (
        "`setup-node` must run BEFORE the consumer suite, or its fourteen "
        "JS-probe cases skip and the exact skip pin refuses the run")


def test_nothing_here_may_be_skipped_by_a_condition(gate_job: dict,
                                                    steps: list[dict]) -> None:
    """A SKIPPED step reports success, which is `continue-on-error` by another road.

    `if: false` on the openXdox verifier, on either JUnit assertion, or on the
    job itself does not fail anything: Actions skips the step and the check
    reports SUCCESS. The gate would then be green having verified no pin, or
    having adjudicated no report — the same vacuity the floors, the exact skip
    count and the named verdicts exist to refuse, arriving through the one
    mechanism none of them can see, because a step that did not run writes
    nothing for them to read.

    So NO step and not the job may carry `if:` at all. The stricter rule is
    the honest one here: this gate has no conditional work in it — every step
    must run on every pull request or the report means nothing — and a rule
    that allowed "only harmless conditions" would need a reader to adjudicate
    harmlessness on each edit. A future act that genuinely needs one moves this
    assertion deliberately, with its reason, in the same diff.
    """
    assert "if" not in gate_job, (
        "the job must not be conditional: a skipped job reports SUCCESS, so "
        "`if:` here would let the gate pass having run nothing at all")
    conditioned = [step.get("name") or step.get("uses")
                   for step in steps if "if" in step]
    assert conditioned == [], (
        f"these steps are conditional: {conditioned}. A skipped step reports "
        f"success — on a verifier that means no pin was checked, on an "
        f"assertion step that means no report was adjudicated, and the check "
        f"goes green either way. Every step in this gate must run on every "
        f"pull request")

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
    """The five keys are present, and the three numbers are the MEASURED ones.

    Presence alone is not the property. The numbers are what make the gate
    non-vacuous, so they are asserted as the literals `MEASURED_PINS` records
    and not as `> 0` — see that constant for the exact weakening a shape-only
    guard leaves open.
    """
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
        report = env["REPORT"]
        assert report in MEASURED_PINS, (
            f"{report!r} has no measured pin recorded here; a new report must "
            f"arrive with its own measurement, not with a shape")
        pinned = (env["MIN_SELECTED"], env["MIN_PASSED"], env["EXPECT_SKIPPED"])
        assert pinned == MEASURED_PINS[report], (
            f"{report}: the gate pins (MIN_SELECTED, MIN_PASSED, "
            f"EXPECT_SKIPPED) = {pinned}, measured {MEASURED_PINS[report]}. "
            f"Floors may only RISE and the skip count is EXACT — if the "
            f"measurement really moved, move it HERE in the same diff, with "
            f"the CI run that measured it in the commit message")
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

    PARSED, NOT GREPPED. A `"def {name}(" in source` reading is satisfied by
    the name appearing in a docstring, in a comment, or as a nested helper
    inside another function — none of which pytest collects and none of which
    produces the `<testcase>` the gate then demands, so the guard would be
    green while the gate went "absent" on the runner. MEASURED both ways
    against a real module: with `test_ruling_q7_two_direct_upstreams_in_lockstep`
    renamed and its old name left in the docstring above it, the substring
    reading passes and this one fails naming the module.
    """
    for watched in PIN_NAMED_VERDICTS + CONSUMER_NAMED_VERDICTS:
        classname, _, name = watched.partition("::")
        module = REPO_ROOT / (classname.replace(".", "/") + ".py")
        assert module.is_file(), (
            f"{watched} names {module}, which does not exist — a watch on a "
            f"module that moved reds the gate on every run")
        defined = {node.name
                   for node in ast.parse(module.read_text(encoding="utf-8")).body
                   if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
        assert name in defined, (
            f"{module} defines no top-level `{name}` — the watched case was "
            f"renamed or removed without moving NAMED_VERDICTS with it. A "
            f"mention of the name in a docstring, a comment or a nested helper "
            f"does not count: the JUnit `<testcase>` this watch reads is "
            f"written for a module-level test function, so anything else is "
            f"green here and 'absent' in the gate")


# --------------------------------------------------------------------------
# the credential that is not here
# --------------------------------------------------------------------------

#: EVERY FORM OF A BEARER, not just `secrets.`: this gate SHIPPED the hole
#: once. Its first push wrote `https://x-access-token:${{ github.token }}@
#: github.com/` into the runner's global git config and then ran two pytest
#: suites over pull-request-controlled code, and a `secrets.`-only guard was
#: green through all of it — the automatic token is not a secret reference.
#:
#: READ STRUCTURALLY RATHER THAN ENUMERATED, because enumeration lost three
#: times running here: the dot form missed `${{ github['token'] }}` and
#: `${{ github . token }}`; case-sensitivity missed `${{ SECRETS.KEY }}`, which
#: Actions resolves exactly as `${{ secrets.KEY }}`; and naming PROPERTIES
#: missed `${{ toJSON(github) }}`, which serializes the whole context — token
#: included — without spelling the token at all. So the rules below are about
#: the CONTEXT, not its spelling, and they are applied inside `${{ … }}` where
#: an expression is the only thing that can resolve:
#:
#:   * the `secrets` context in any case and any syntax — this gate reads three
#:     PUBLIC gitlinks and needs no secret at all, so mentioning the context is
#:     itself the finding;
#:   * the `github` context used as a VALUE rather than dereferenced — the
#:     shape of `toJSON(github)` and `format('{0}', github)` — because the
#:     serialized context carries the token;
#:   * and `github.token` however it is spelled or spaced.
#:
#: `${{ github.ref }}`, the one expression this workflow contains, is a
#: dereference of a non-secret property and stays clean.
EXPRESSION = re.compile(r"\$\{\{(.*?)\}\}", re.DOTALL)

EXPRESSION_FORMS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("the `secrets` context", re.compile(r"\bsecrets\b", re.IGNORECASE)),
    ("the `github` context as a whole value",
     re.compile(r"\bgithub\b(?!\s*[.\[])", re.IGNORECASE)),
    ("`github.token`", re.compile(r"\bgithub\s*\.\s*token\b", re.IGNORECASE)),
    # ANY index on the context, literal or COMPUTED. Requiring the literal
    # `'token'` left `${{ github[format('{0}', 'token')] }}` — and every other
    # expression that builds the property name — reading the bearer through a
    # guard that saw nothing. A dotted dereference says what it reads and is
    # judged on that; an index that has to be evaluated does not, so this fails
    # closed on all of them. `${{ github['ref'] }}` is refused too: write
    # `github.ref`, which the case below pins as clean.
    ("the `github` context indexed",
     re.compile(r"\bgithub\s*\[", re.IGNORECASE)),
)

#: Not expressions: an environment variable name and the two URL/user forms a
#: bearer arrives under. Matched anywhere, because they need no `${{ }}` to
#: reach the runner.
LITERAL_FORMS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("`GITHUB_TOKEN`", re.compile(r"GITHUB_TOKEN")),
    ("`x-access-token`", re.compile(r"x-access-token", re.IGNORECASE)),
    ("`ACTIONS_RUNTIME_TOKEN`",
     re.compile(r"ACTIONS_RUNTIME_TOKEN", re.IGNORECASE)),
)


def bearer_forms_found(blob: str, *, unwrapped: bool = False) -> list[str]:
    """Every bearer form in one piece of workflow text, named as it is found.

    The literal forms are matched anywhere in the blob. The context rules are
    matched inside `${{ … }}` — so prose may go on discussing secrets and
    tokens in a comment without failing the guard that refuses them — and,
    when `unwrapped` is set, over the whole blob as well.

    `unwrapped` is for `if:`, which Actions evaluates as an expression WITH OR
    WITHOUT the braces: `if: github.token != ''` resolves the context exactly
    as `if: ${{ github.token != '' }}` does. A guard that only reads braced
    text would call that step clean, so the caller marks the key.
    """
    found = [label for label, form in LITERAL_FORMS if form.search(blob)]
    expressions = EXPRESSION.findall(blob)
    if unwrapped:
        expressions = [*expressions, blob]
    for expression in expressions:
        found.extend(
            f"{label} in `{expression.strip()}`"
            for label, form in EXPRESSION_FORMS if form.search(expression))
    return found


def bearer_sites(text: str) -> list[str]:
    """Every place in a workflow document where a bearer could reach a step.

    TWO READINGS, because each is blind where the other sees.

    The RAW one scans from the `jobs:` key down, which catches a spelling
    arriving by a route no schema names — a shell interpolation inside a
    `run:` body, a line of `git config`, a comment that is really a re-enabling
    instruction — and it starts at that key so that the header prose above may
    go on quoting the hole this gate shipped without failing the guard that
    closed it.

    That scoping is itself a hole, and this is the half that closes it: a
    workflow-level `env:` block written ABOVE `jobs:` is inherited by every
    step of every job while appearing in none of them. So the PARSED reading
    walks the whole document — every key and every scalar of `on:`,
    `permissions:`, `concurrency:`, a workflow-level `env:`, each job's `env:`,
    each step's `with:` and `run:` — where comments do not exist at all and
    position cannot hide anything.

    Returns the sites, `[]` when the document is clean, so that a failure names
    WHERE rather than only THAT.
    """
    sites: list[str] = []
    raw = text[text.index("\njobs:"):]
    sites.extend(f"the raw job body carries {found}"
                 for found in bearer_forms_found(raw))

    def walk(node: object, path: str, *, unwrapped: bool = False) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                walk(str(key), f"{path}.{key}")
                walk(value, f"{path}.{key}", unwrapped=str(key) == "if")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}[{index}]", unwrapped=unwrapped)
        else:
            sites.extend(
                f"{path} carries {found}"
                for found in bearer_forms_found(str(node), unwrapped=unwrapped))

    walk(yaml.safe_load(text), "<workflow>")
    return sites


def test_the_gate_mints_no_credential_for_public_gitlinks(
        steps: list[dict]) -> None:
    """All three gitlinks are public; no bearer of any spelling belongs here.

    ASSERTED AT THREE LEVELS, on the wallet suite's own reasoning extended by
    what this gate then got wrong. The step-shaped probe catches a mint under
    any name. `bearer_sites` catches the two routes a step-shaped probe cannot
    see: a spelling arriving as raw text inside the job body, and a spelling
    arriving as a parsed value ANYWHERE in the document — including the
    workflow-level `env:` block that sits above `jobs:` and reaches every step
    without appearing in one.

    The wallet suite asserts `${{ secrets. }}` alone absent, and that reading
    is NOT inherited here: it is CONSUMPTION that is forbidden and not the
    name, and `${{ github.token }}` is consumption that never passes through
    `secrets.` — which is exactly the hole this gate's first push shipped.
    """
    mints = [s.get("name") or s.get("uses") for s in steps
             if "create-github-app-token" in str(s.get("uses", ""))]
    assert mints == [], (
        f"the gate must mint no App token for PUBLIC gitlinks; found {mints}. "
        f"If openDox or openXdox ever goes private, add the mint with its "
        f"reason rather than around this test")

    # The reads here are public and need no bearer at all, in the job body or
    # above it.
    sites = bearer_sites(WORKFLOW.read_text(encoding="utf-8"))
    assert sites == [], (
        f"the gate references a bearer: {sites}. Every gitlink it reads is "
        f"PUBLIC, so it needs no bearer; putting one in the runner's "
        f"environment or git config exposes it to the suites this gate then "
        f"runs over pull-request-controlled code. If a leg ever goes private, "
        f"add the credential WITH its reason rather than around this test")

    # …and no checkout may take a token or leave one behind.
    for step in steps:
        if str(step.get("uses", "")).startswith("actions/checkout"):
            with_block = step.get("with", {})
            assert "token" not in with_block, (
                "the checkout must declare no `token:` input. WHAT THIS DOES "
                "AND DOES NOT SAY: `actions/checkout` DEFAULTS `token` to "
                "`${{ github.token }}`, so the action's own fetch is "
                "authenticated whether or not the key appears — what is "
                "pinned here is that no OTHER credential is introduced, and "
                "`persist-credentials: false` below is what keeps the default "
                "out of the tree these suites then read. All three "
                "repositories are public (measured 2026-09-16), so a "
                "genuinely anonymous `token: \'\'` checkout is available; it "
                "changes the transport this gate has proved on thirteen runs, "
                "so it is registered in the pull request rather than taken "
                "here")
            assert with_block.get("persist-credentials") is False, (
                "the checkout must set `persist-credentials: false` so no "
                "bearer is left in the repository config before pytest runs "
                "pull-request-controlled code")


def test_the_credential_guard_sees_a_bearer_written_above_the_jobs_key() -> None:
    """The guard's own blind spot, closed and PROVED BOTH WAYS on this document.

    A raw scan that starts at the `jobs:` key cannot see a workflow-level
    `env:` block, and Actions hands that block to every step of every job: a
    later edit could put `GITHUB_TOKEN: ${{ github.token }}` four lines above
    that key and every step of this gate would run holding a bearer, while the
    guard that exists to refuse one stayed green. So the doctoring below is
    inserted ABOVE that key, and the test asserts BOTH halves — that the raw
    window really is clean of it (so the old reading would have passed this
    document) and that `bearer_sites` names it anyway.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    doctored = text.replace(
        "\njobs:", '\nenv:\n  GITHUB_TOKEN: "${{ github.token }}"\njobs:', 1)
    window = doctored[doctored.index("\njobs:"):]
    assert bearer_forms_found(window) == [], (
        "the doctored bearer must land ABOVE `jobs:`; inside the window the "
        "raw reading already covers it and this case proves nothing")

    sites = bearer_sites(doctored)
    assert any(site.startswith("<workflow>.env") for site in sites), (
        f"a workflow-level `env:` bearer went unseen; sites={sites}")
    assert bearer_sites(text) == [], (
        "the shipped document must be clean — this case doctors a copy")


#: `(expression, was invisible to the literal-SUBSTRING reading)` — the one
#: this suite shipped at `08f438b7`, the tuple `enumerated` below. The `False`
#: rows are the forms it DID catch, kept so a structural rule is shown to lose
#: nothing the enumeration held. The PATTERN reading that replaced it one
#: commit later still missed five of these — `${{ SECRETS.X }}`,
#: `${{ Secrets['X'] }}`, `${{ toJSON(github) }}`, `${{ toJSON(secrets) }}` and
#: `${{ format('{0}', github) }}` — which is why the rules are now about the
#: CONTEXT rather than about any spelling of it.
EXPRESSION_CASES = (
    ("${{ github['token'] }}", True),
    ('${{ github["token"] }}', True),
    ("${{ github . token }}", True),
    ("${{ GitHub['Token'] }}", True),
    ("${{ secrets.DEPLOY_KEY }}", False),
    ("${{ github.token }}", False),
    ("${{ SECRETS.DEPLOY_KEY }}", True),
    ("${{ Secrets['DEPLOY_KEY'] }}", True),
    ("${{ toJSON(github) }}", True),
    ("${{ toJSON(secrets) }}", True),
    ("${{ format('{0}', github) }}", True),
    ("${{ github[format('{0}', 'token')] }}", True),
    ("${{ github[env.PROPERTY] }}", True),
)


@pytest.mark.parametrize("expression,unseen_before", EXPRESSION_CASES)
def test_the_credential_guard_reads_the_expression_not_the_spelling(
        expression: str, unseen_before: bool) -> None:
    """One value, many spellings — and two of them name no token at all.

    Actions dereferences with a dot OR indexes with brackets, ignores
    whitespace inside `${{ }}`, and matches context and property names
    case-insensitively: `${{ github.token }}`, `${{ github['token'] }}`,
    `${{ github . token }}` and `${{ GitHub['Token'] }}` are one bearer, and
    `${{ SECRETS.X }}` is `${{ secrets.X }}`. Worse for an enumeration,
    `${{ toJSON(github) }}` and `${{ format('{0}', github) }}` hand the WHOLE
    context — token included — to whatever reads the value, while spelling
    neither `token` nor `secrets`.

    Each doctored document below is a workflow-level `env:` written the way a
    person would write it, and each is asserted TWICE: that the
    literal-substring reading this suite shipped at `08f438b7` saw it exactly
    as its row says (the `True` rows are the ones it MISSED; the `False` rows
    it caught, kept so the structural rule is shown to lose nothing), and that
    the structural reading names every one of them.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    doctored = text.replace(
        "\njobs:", f"\nenv:\n  FOO: {expression}\njobs:", 1)

    enumerated = ("secrets.", "github.token", "GITHUB_TOKEN", "x-access-token",
                  "ACTIONS_RUNTIME_TOKEN")
    seen_before = any(spelling in expression for spelling in enumerated)
    assert seen_before != unseen_before, (
        f"{expression!r} is marked "
        f"{'unseen' if unseen_before else 'seen'} by the literal enumeration "
        f"and the enumeration says otherwise — fix the row, not the guard")

    sites = bearer_sites(doctored)
    assert any(site.startswith("<workflow>.env.FOO") for site in sites), (
        f"{expression!r} went unseen; sites={sites}")


@pytest.mark.parametrize("condition", (
    "github.token != ''",
    "secrets.DEPLOY_KEY != ''",
    "${{ github.token != '' }}",
))
def test_the_credential_guard_reads_an_unwrapped_if_as_an_expression(
        condition: str) -> None:
    """`if:` resolves contexts with or without the braces, and so must this.

    Actions evaluates an `if:` value as an expression either way: `if:
    github.token != ''` reads the context exactly as `if: ${{ github.token !=
    '' }}` does. A guard that only looked inside `${{ … }}` would call the
    first one clean — so `bearer_forms_found` takes an `unwrapped` flag and the
    walk sets it for the `if` key, which is the only key Actions treats that
    way.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    doctored = text.replace(
        "      - uses: actions/checkout@",
        f"      - if: {condition}\n        uses: actions/checkout@", 1)
    sites = bearer_sites(doctored)
    assert any(".if carries" in site for site in sites), (
        f"an `if:` reading a bearer went unseen; sites={sites}")


def test_a_non_secret_dereference_is_not_a_bearer(tmp_path: Path) -> None:
    """The guard must not refuse what Actions workflows legitimately do.

    A rule about the CONTEXT rather than the spelling has to earn its keep in
    both directions, or the next editor routes around it: `${{ github.ref }}`
    — the one expression this workflow contains, in its `concurrency` group —
    and its neighbours are dereferences of non-secret properties, and they stay
    clean. The shipped document passing is the other half of the same claim.
    """
    for clean in ("${{ github.ref }}", "${{ github.event_name }}",
                  "${{ github.event.pull_request.head.sha }}",
                  "${{ hashFiles('requirements/*.lock') }}"):
        assert bearer_forms_found(f"concurrency:\n  group: {clean}\n") == [], (
            f"{clean} is a non-secret dereference and must not be refused")

    for condition in ("github.event_name == 'pull_request'",
                      "github.ref == 'refs/heads/main'",
                      "success()"):
        assert bearer_forms_found(condition, unwrapped=True) == [], (
            f"`if: {condition}` reads no bearer and must not be refused")


# --------------------------------------------------------------------------
# the collision this suite shipped, pinned as a rule
# --------------------------------------------------------------------------

def test_no_two_test_modules_resolve_to_the_same_import_name(
        pytestconfig: pytest.Config) -> None:
    """A basename collision INTERRUPTS the required run; it does not fail one file.

    pytest's default `prepend` import mode names a test module by walking UP
    from the file while `__init__.py` exists: a file in a package directory
    gets a dotted name, and a file in a plain directory gets its BARE BASENAME.
    Two plain directories holding the same basename therefore claim one
    `sys.modules` entry, and the second one collected raises `import file
    mismatch` — a COLLECTION error, which stops the whole run at
    "Interrupted: 1 error during collection" and reports nothing about ANY
    other module in the tree — no number is quoted here on purpose, because
    the count moves with every file added and the property does not.

    THIS SUITE CAUSED EXACTLY THAT. Authored as
    `tests/openxdox_consumer_gate/test_gate_invocation.py`, it collided with
    `tests/openxwallet_consumer_gate/test_gate_invocation.py`, and
    `pytest-suite` went red on 2 collected tests. The file was renamed; this
    test names the RULE for whoever writes the third consumer gate.

    WHAT IT CANNOT DO, said here rather than left to be discovered: it cannot
    pre-empt the interruption in the same session. Collection runs before any
    test does, so in a full-tree run a live collision aborts before this
    assertion executes — MEASURED, by restoring a colliding pair: `pytest
    tests/` reports `Interrupted: 1 error during collection` and `2 skipped,
    338 deselected, 1 error`, and this test does not run. What follows from
    that is the useful half: **the required suite never goes green on a
    collision** — it goes red, naming the offending file, which is exactly how
    this one was caught. This guard is for the run where collection SUCCEEDS —
    the scoped `pytest tests/openxdox_consumer_gate` of the authoring loop,
    where it fails with the rule, both colliding paths and the two remedies
    instead of an `import file mismatch` an author must decode. A scan that
    ran before collection for the whole tree would be a repository-wide hook
    in a shared `conftest.py`; that is a different act than this gate.

    IT IS NOT A BAN ON REPEATED BASENAMES, and it must not become one: SIX
    basenames repeat lawfully today (`test_gate_wiring`, `test_integrity`,
    `test_release_inventory`, `test_schema`, `test_topology_lifecycle`,
    `test_validate`), each pair distinguished because at least one side sits in
    a package directory. The rule is about the IMPORT NAME, which is what
    pytest actually collides on — so `tests/opendox_pin/` and
    `tests/openxdox_pin/` name their modules distinctly instead, which is the
    convention this directory now follows.

    THE SCAN ASKS PYTEST WHAT IT COLLECTS RATHER THAN ASSUMING `test_*.py`.
    `python_files` defaults to BOTH `test_*.py` and `*_test.py`, and this
    repository's `pytest.ini` overrides neither, so a file named
    `gate_invocation_test.py` is collected too and can collide exactly the same
    way — while a scan of the first pattern alone would stay green and let the
    required run be interrupted anyway. Reading the ini value also keeps this
    honest if the patterns are ever narrowed or widened.
    """
    patterns = list(pytestconfig.getini("python_files"))
    assert patterns, "pytest collects no test files under any pattern"

    def import_name(path: Path) -> str:
        parts = [path.stem]
        directory = path.parent
        while (directory / "__init__.py").is_file():
            parts.append(directory.name)
            directory = directory.parent
        return ".".join(reversed(parts))

    modules = {module
               for pattern in patterns
               for module in (REPO_ROOT / "tests").rglob(pattern)}
    by_name: dict[str, list[str]] = collections.defaultdict(list)
    for module in sorted(modules):
        by_name[import_name(module)].append(
            str(module.relative_to(REPO_ROOT)))
    collisions = {name: sorted(paths)
                  for name, paths in by_name.items() if len(paths) > 1}
    assert collisions == {}, (
        f"two or more test modules resolve to one import name: {collisions}. "
        f"pytest will interrupt the REQUIRED run with `import file mismatch` "
        f"and report nothing about the rest of the tree. Rename one file, or "
        f"make one directory a package with `__init__.py`")
