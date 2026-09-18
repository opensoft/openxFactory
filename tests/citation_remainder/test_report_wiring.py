"""The nightly wiring of the citation remainder report, pinned structurally.

`add-citation-remainder-report` § 2.2, realization slice R2. Every test in
`test_report_citation_remainder.py` exercises the CLI directly and NONE of them
reads the workflow file, so a changed invocation could silently de-advise the
nightly with every unit test still green: a bare `scripts/…` path the
aggregation checkout has no file at, a dropped `REPO_ROOT` positional that
scans the aggregation tree instead of this submodule, a redirect moved inside
the scanned root, a second flag that makes tonight's reading a differently
defined one from last night's. These tests parse the shipped workflow and
assert on the parsed structure, the instrument
`tests/doc-health/test_workflow_guards.py` and
`tests/doc-health/test_workflow_contract.py` already use on THIS SAME file and
THIS SAME `finalize` job.

WHAT THIS MODULE DOES NOT DO: prove the step ran. A merged workflow file is not
evidence that a step executed — the parent packet's own § 4.5 lesson, one notch
down — and § 2.2's other half is the first `doc-health-nightly` run that
produces the artifact, cited by run id and artifact name. No test in this
repository can give that proof, because the workflow is REUSABLE and the run
belongs to the caller (`opensoft/xFactory`).
"""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "doc-health-reusable.yml"

#: The step's own id, and the one file it writes. Named once here so a rename
#: moves in one place and every assertion below travels with it.
RUN_STEP_ID = "citation-remainder"
ARTIFACT_FILE = "citation-remainder.json"
SCRIPT_PATH = "openxFactory/scripts/report-citation-remainder.py"


def workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def finalize() -> dict:
    return workflow()["jobs"]["finalize"]


def step_by_id(job: dict, step_id: str) -> dict:
    matches = [s for s in job["steps"] if s.get("id") == step_id]
    assert len(matches) == 1, f"expected exactly one step with id {step_id!r}"
    return matches[0]


def step_by_name(job: dict, name: str) -> dict:
    matches = [s for s in job["steps"] if s.get("name") == name]
    assert len(matches) == 1, f"expected exactly one step named {name!r}"
    return matches[0]


def index_of(job: dict, step: dict) -> int:
    return job["steps"].index(step)


def report_invocations(script: str) -> list:
    """Every invocation of the report in the step's shell, as an argv list.

    THE CONTINUATIONS ARE JOINED RATHER THAN SEARCHED FOR ONE AT A TIME,
    because the shipped step wraps its invocation across two lines: a test that
    read only the line carrying the script name would find no `--json` on it
    and would pass, or fail, for a reason about line width rather than about
    the argv the nightly actually runs.

    AND THE SHELL AROUND THE ARGV IS TAKEN OFF RATHER THAN ASSERTED ON. The
    invocation stands inside an `if ! … ; then` guard — that guard is how a
    cannot-run reaches an annotation instead of dying under `set -e` — and the
    redirect is shell, not an argument the CLI ever sees (`--json` is a boolean
    flag taking no path). What is left is exactly the argv, which is the thing
    these tests are about; the redirect TARGET has a test of its own.
    """
    joined, pending = [], ""
    for line in script.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if stripped.endswith("\\"):
            pending += stripped[:-1].strip() + " "
            continue
        joined.append((pending + stripped).strip())
        pending = ""
    if pending:
        joined.append(pending.strip())
    invocations = []
    for command in joined:
        if "report-citation-remainder.py" not in command:
            continue
        argv = command.split(">", 1)[0].split()
        while argv and argv[0] in ("if", "!"):
            argv.pop(0)
        invocations.append(argv)
    return invocations


def test_the_nightly_runs_the_report_exactly_once():
    """ONE invocation, ONE file. `tasks.md` § 2.2 fixes it: "The report writes
    to STDOUT and the step redirects it to ONE named file." An earlier sketch
    ran the CLI twice, once to a human `.txt` and once to `--json`; a second
    invocation is a second reading of a tree that may have moved between
    them, and a second file the upload step would have to name."""
    invocations = report_invocations(step_by_id(finalize(), RUN_STEP_ID)["run"])
    assert len(invocations) == 1, invocations


def test_the_argv_is_the_fixed_one_and_carries_no_refinement():
    """The argv is FIXED, so every nightly reading is a later point in the
    SAME series rather than a differently defined one (spec.md, *A reading is
    compared against an earlier reading*). `--include`/`--exclude` would
    refine the population; `--all`, `--tokens` and `--history` would change
    what is listed or what is probed. None of them is passed, and the
    assertion is on the WHOLE argv rather than on the absence of each, so a
    flag invented later is caught by the same line."""
    invocation, = report_invocations(step_by_id(finalize(),
                                                RUN_STEP_ID)["run"])
    assert invocation == ["python3", SCRIPT_PATH, "openxFactory", "--json"], \
        invocation


def test_the_script_path_is_submodule_qualified():
    """The checkout is the AGGREGATION tree and this repository is a submodule
    inside it, so a bare `scripts/…` names no file there — every sibling step
    spells it the same way (`:582`, `:1045`, `:2233`)."""
    invocation, = report_invocations(step_by_id(finalize(),
                                                RUN_STEP_ID)["run"])
    assert invocation[1] == SCRIPT_PATH
    assert not invocation[1].startswith("scripts/")


def test_the_repo_root_positional_is_this_submodule_and_never_a_default():
    """The CLI's own default is `.` (`nargs="?", default="."`), which in this
    job is the AGGREGATION root: a different corpus, with a different
    remainder, that would be published as this repository's."""
    invocation, = report_invocations(step_by_id(finalize(),
                                                RUN_STEP_ID)["run"])
    assert invocation[2] == "openxFactory"


def test_the_json_flag_is_passed_with_no_operand():
    """`--json` is a BOOLEAN output-format flag on D2's fixed surface. Spelled
    `--json <out>` it would hand the CLI a second positional, or redirect into
    a file called `out`; either way the artifact-only step has no report to
    upload."""
    invocation, = report_invocations(step_by_id(finalize(),
                                                RUN_STEP_ID)["run"])
    assert invocation[-1] == "--json"
    assert invocation.count("--json") == 1


def test_the_reading_is_written_outside_the_scanned_root():
    """D3(a)'s output-path fence, held STRUCTURALLY under D5 option 1: the
    redirect target sits at the aggregation root, so the file never enters the
    population the next night's run reads, whatever the exclusion list says."""
    run = step_by_id(finalize(), RUN_STEP_ID)["run"]
    assert f"> {ARTIFACT_FILE}" in run
    assert f"openxFactory/{ARTIFACT_FILE}" not in run


def test_the_step_carries_no_fail_on_and_adds_no_gate():
    """*The citation remainder report is advisory and gates nothing*: the CLI
    ships no `--fail-on` and the wiring must not invent one out of the exit
    code either."""
    step = step_by_id(finalize(), RUN_STEP_ID)
    assert "--fail-on" not in step["run"]
    assert step["if"] == "always()"


def test_every_failure_path_annotates_rather_than_swallowing_the_skip():
    """R2's Q6 DECISION, pinned: the step carries `continue-on-error: true`,
    so a cannot-run records a graceful skip instead of reddening the
    governance nightly — this file's own habit for every optional lane — and
    the price of that posture is that NOTHING may fail silently. Every
    non-zero exit in the step's shell is preceded by a `::warning::`
    annotation, asserted mechanically rather than by reading the block."""
    step = step_by_id(finalize(), RUN_STEP_ID)
    assert step["continue-on-error"] is True
    lines = [line.strip() for line in step["run"].splitlines()]
    exits = [i for i, line in enumerate(lines) if line == "exit 1"]
    assert exits, "the step has no failure path at all"
    for i in exits:
        preceding = lines[max(0, i - 3):i]
        assert any("::warning::" in line for line in preceding), \
            f"exit at line {i} is a silent swallow: {preceding}"


def test_the_tree_state_of_the_reading_is_checked_and_not_merely_printed():
    """R2's ONE assertion beyond the CLI's own exit code. The CLI declares a
    modified tree and still produces the reading, by design (*The tree read is
    not clean at the head printed*: "the report MUST still produce the reading
    rather than refuse to run"), so the nightly's own verification that its
    checkout was clean is the wiring's, not the CLI's. A reading taken over a
    modified tree is not a later point in D6's series and must not be uploaded
    as one."""
    run = step_by_id(finalize(), RUN_STEP_ID)["run"]
    assert "tree_unmodified_at_head" in run
    assert "tree_state" in run
    # THE BRANCH IS CUT OUT BEFORE IT IS ASSERTED ON, not searched for in the
    # whole block: the step has a second failure path a few lines above this
    # one, and a test that asked only whether SOME `exit 1` followed the field
    # name would pass over a tree-state branch that had stopped stopping —
    # measured, by mutating this step and watching an earlier draft of this
    # test stay green.
    assert '!= "true"' in run
    branch = run.split('!= "true"', 1)[1].split("\nfi", 1)[0]
    assert "tree_state" in branch
    assert "::warning::" in branch
    assert "exit 1" in branch


def test_the_reading_is_taken_before_any_step_that_writes_in_the_submodule():
    """THE ORDER IS PART OF THE WIRING. Two lanes in this job commit back
    INSIDE the openxFactory checkout (`cd openxFactory`), and the neutrality
    lane's own merge can persist writes there before its commit-back step even
    runs. A reading taken after one of them would declare a modified tree
    through no fault of the corpus and would drop out of D6's series — so the
    report is taken while the checkout still stands at the pinned commit."""
    job = finalize()
    reading_at = index_of(job, step_by_id(job, RUN_STEP_ID))
    writers = [(i, s.get("name")) for i, s in enumerate(job["steps"])
               if "cd openxFactory" in (s.get("run") or "")]
    assert writers, "expected at least one commit-back step to order against"
    for i, name in writers:
        assert i > reading_at, f"{name!r} writes in the submodule at step " \
                               f"{i}, before the reading at {reading_at}"


def test_the_reading_is_taken_in_finalize_where_the_checkout_stands():
    """`finalize` carries the aggregation checkout with the submodules
    initialized and `steps.run.outputs.run_date` in scope; `prepare` carries
    neither."""
    assert not [s for s in workflow()["jobs"]["prepare"]["steps"]
                if s.get("id") == RUN_STEP_ID]
    assert step_by_id(finalize(), RUN_STEP_ID)


def test_the_upload_is_gated_on_the_run_steps_outcome():
    """Gated on OUTCOME and not merely on `always()`: with
    `continue-on-error` the step's conclusion is always success, so `outcome`
    is the only field still carrying the failure. The same reasoning the
    `dfr-upload`/`dfr-dispatch` pair writes down for itself lower in this
    file."""
    upload = step_by_name(finalize(), "Upload citation remainder report")
    assert upload["if"] == \
        f"always() && steps.{RUN_STEP_ID}.outcome == 'success'"


def test_the_upload_names_the_run_date_and_exactly_the_one_file_written():
    """The RUN'S DATE belongs in the artifact NAME and not in the file name —
    the house convention next door at `:2253`. `path:` names the one file the
    run step wrote, and no second path."""
    job = finalize()
    upload = step_by_name(job, "Upload citation remainder report")
    assert upload["uses"] == "actions/upload-artifact@v4"
    assert upload["with"]["name"] == \
        "citation-remainder-${{ steps.run.outputs.run_date }}"
    assert upload["with"]["path"] == ARTIFACT_FILE
    assert index_of(job, upload) == index_of(job, step_by_id(job,
                                                             RUN_STEP_ID)) + 1


def test_an_empty_artifact_is_an_error_rather_than_a_silent_upload():
    """A silently empty artifact is a hole in D6's series that reads like a
    reading."""
    upload = step_by_name(finalize(), "Upload citation remainder report")
    assert upload["with"]["if-no-files-found"] == "error"


def test_the_series_outlives_the_window_d6_measures_over():
    """D6's stability condition is measured over N = 14 consecutive nightly
    runs and, under D5 option 1, the series lives only in artifacts — so the
    retention is stated rather than inherited. 90 days is the effective
    maximum measured in the CALLER repository, where a reusable workflow's
    artifacts live."""
    upload = step_by_name(finalize(), "Upload citation remainder report")
    assert upload["with"]["retention-days"] == 90
    assert upload["with"]["retention-days"] >= 14


def test_the_step_asks_for_no_permission_the_job_does_not_already_hold():
    """D5's own claim, held structurally: an artifact-only step commits
    nothing, opens no branch and needs no token, so neither step declares a
    `permissions:` block of its own and the aggregation caller does not
    move."""
    job = finalize()
    for step in (step_by_id(job, RUN_STEP_ID),
                 step_by_name(job, "Upload citation remainder report")):
        assert "permissions" not in step
        assert "env" not in step
