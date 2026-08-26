"""The OPERATING DOCS as an executable surface (PR #49 critic findings C4, C5,
C7).

The acceptance pass for this feature (T092) is a human at a shell following
`docs/ideation-dashboard-session-runbook.md`, so those pages are part of the
build and not commentary on it. Three defects nothing in the suite could see:

  * **C4 — the literal first step did not run.** §2 said
    `python3 scripts/ideation_dashboard/cli.py generate-and-open`, which exits 2:
    `--repo-root` and `--repository` are both required and neither was named
    anywhere in §2 (nor in `docs/check-matrix.md` §8), while §2's prerequisite
    table named a `--checkout-root` flag that verb does not have.
  * **C5 — the merge ending was unachievable.** §6 promised the next `open-pr`
    OBSERVES the merge and reconciles; the build refuses `base_stale` until a
    human pulls, and that step appeared ONLY inside the refusal text. The doc and
    the code now name the SAME pull, and the sequence is driven here end to end.
  * **C7 — two derived artifacts were undocumented.** §5 promises to say where
    every derived artifact lives and omitted `session-dispatch/` and
    `session-ended/`, the only durable traces of a half-finished ending.

The discipline is the suite's: every command a doc offers is parsed by the REAL
CLI parser rather than eyeballed, every path a doc names is derived from the
production constant rather than transcribed, and the C5 sequence runs in a
throwaway repository with a LOCAL BARE origin, `FakePullRequests`, no network, no
real `gh`, no real `nlm`, and no sleeps.
"""

from __future__ import annotations

import json
import re
import shlex
import subprocess
from pathlib import Path

import pytest

from conftest import REPO_ROOT
from session_fixtures import build_scratch_repo  # noqa: F401 - fixture module

from ideation_dashboard import branch_session as bs
from ideation_dashboard import cli as cli_mod
from ideation_dashboard import corpus_root as corpus_root_mod
from ideation_dashboard import gate_console as gc
from ideation_dashboard import gate_routes as gr
from ideation_dashboard import session_git as sg
from ideation_dashboard import session_pr as spr
from ideation_dashboard import snapshot_registry as reg
from ideation_dashboard.boundary import HumanGate
from ideation_dashboard.generator import generate_snapshot

RUNBOOK = REPO_ROOT / "docs" / "ideation-dashboard-session-runbook.md"

# `CHECK_MATRIX` and its consistency pins stayed with `docs/check-matrix.md` in
# codexFactory (adopt-neutral-tooling-home tranche B, 2026-08-03): the check
# matrix is codexFactory's own operating doc and is NOT part of the ratified
# move, so the pins that read it live beside it until tranche C decides that
# doc's fate. The runbook halves of the two both-docs tests remain below.

REPO = "openxFactory"
TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
DOC = f"ideation/staging/{TOPIC}/note.md"


def _runbook() -> str:
    return RUNBOOK.read_text(encoding="utf-8")


def _section(body: str, heading: str) -> str:
    """One `## ` section of a markdown doc, heading line excluded."""
    parts = re.split(r"^## ", body, flags=re.MULTILINE)
    for part in parts[1:]:
        if part.startswith(heading):
            return part
    raise AssertionError(f"no section {heading!r} in the document")


def _prose(body: str) -> str:
    """The section with every run of whitespace collapsed — a markdown paragraph
    is line-WRAPPED, so a sentence assertion must not depend on where the wrap
    fell."""
    return re.sub(r"\s+", " ", body)


def _subparser(name: str):
    """One `cli.py` subcommand's parser, found by walking the real parser's
    choices — the same traversal `test_session_confinement.py` uses."""
    node = cli_mod.build_parser()
    for action in node._actions:
        if getattr(action, "choices", None) and name in action.choices:
            return action.choices[name]
    raise AssertionError(f"no {name!r} subcommand")


def _bash_blocks(body: str) -> list[str]:
    """Every ```bash fenced block, line continuations JOINED — a command a human
    pastes is one command however many lines it is written over."""
    blocks = re.findall(r"```bash\n(.*?)```", body, re.DOTALL)
    return [re.sub(r"\\\n\s*", " ", block).strip() for block in blocks]


# --------------------------------------------------------------------------
# C4 — the first step of the live pass RUNS
# --------------------------------------------------------------------------

def test_the_runbook_start_command_parses_with_the_real_cli_parser():
    """C4: §2's start command is PARSED by `cli.build_parser()`, exactly as the
    gate-off descriptors are (T079) — so a line the terminal would reject cannot
    ship in the one step every session pass begins with.

    The old line (`… cli.py generate-and-open`, no flags) exits 2 with
    "the following arguments are required: --repo-root, --repository", and the
    second half of this test pins that this parser really does refuse it: a
    doc-shape assertion that cannot fail is worth nothing (tail finding B7)."""
    body = _runbook()
    start = _section(body, "2. Prerequisites")
    blocks = _bash_blocks(start)
    assert blocks, "§2 offers no command at all"
    command = blocks[0]
    assert command.startswith("python3 scripts/ideation_dashboard/cli.py "
                              "generate-and-open"), command

    parser = cli_mod.build_parser()
    args = parser.parse_args(shlex.split(command)[2:])

    assert args.func is cli_mod.cmd_generate_and_open
    # both REQUIRED values are actually supplied, and neither is a placeholder a
    # shell would split into three words
    assert Path(args.repo_root).is_absolute(), args.repo_root
    assert args.repository and " " not in args.repository, args.repository
    # the counter-check: the bare form the doc used to carry is REFUSED here, so
    # this test would have caught C4
    with pytest.raises(SystemExit) as exit_info:
        parser.parse_args(["generate-and-open"])
    assert exit_info.value.code == 2


def test_the_runbook_names_the_two_required_flags_and_what_they_are_for():
    """C4: naming the flags in the command is not enough — §2 must say WHAT to
    pass, and that `--repository` is the session key's repository half, because
    that is the value every session verb has to repeat (§3)."""
    start = _prose(_section(_runbook(), "2. Prerequisites"))
    assert "--repo-root" in start and "--repository" in start
    assert "REQUIRED" in start
    assert "repository half of the session key" in start
    assert "served checkout" in start.lower()


def test_the_runbook_claims_no_flag_generate_and_open_does_not_have():
    """C4, the compounding half: §2's prerequisite table named `--checkout-root`
    as the real-checkout condition. `generate-and-open` has no such flag — it is
    `serve.py`'s own spelling of the same value — so a reader who trusted the
    table could not construct a working command from it.

    Asserted against the PARSER, not against prose: every long flag §2 mentions
    must be one `generate-and-open` really accepts, or be attributed to the other
    entrypoint in the same sentence."""
    start = _section(_runbook(), "2. Prerequisites")
    accepted = {option for action in _subparser("generate-and-open")._actions
                for option in action.option_strings}
    for flag in sorted(set(re.findall(r"`?(--[a-z][a-z-]+)", start))):
        if flag in accepted:
            continue
        line = next(l for l in start.splitlines() if flag in l)
        assert "serve.py" in line or "serve.py" in start.split(flag)[0][-400:], (
            f"§2 names {flag}, which `generate-and-open` does not accept, "
            f"without saying whose flag it is: {line.strip()!r}")


def test_the_runbook_says_what_a_wrong_repo_root_does(tmp_path):
    """T092's own first failure: §2 said both flags were required and stopped
    there, so the ONE thing a human hits — a `--repo-root` that resolves somewhere
    else — was undocumented, and the empty funnel it used to serve looked like a
    result. §2 must now state the refusal, that nothing is written, and that a
    zero-document projection warns instead.

    The refusal's phrasing is DERIVED from the production message rather than
    transcribed: the doc quotes what `generator.corpus_root_refusal` really says,
    and the CLI is run here to prove that is really what it says."""
    start = _section(_runbook(), "2. Prerequisites")
    prose = _prose(start)

    produced = corpus_root_mod.corpus_root_refusal("/nonexistent/openxFactory")
    headline = produced.splitlines()[0].split(":", 1)[0]   # `--repo-root is not a corpus checkout`
    assert headline in prose, f"§2 does not carry the real refusal headline {headline!r}"
    for root in corpus_root_mod.SCANNED_ROOTS:
        assert f"{root}/" in prose, f"§2 does not name the {root}/ root"
    assert "REFUSED" in start
    assert "no snapshot" in prose.lower() or "writes no snapshot" in prose.lower()
    assert "ZERO documents" in start and "legal" in prose

    # and the build really behaves that way, from the doc's own claim
    rc = cli_mod.main(["generate", "--repo-root", "/nonexistent/openxFactory",
                       "--repository", "openxFactory",
                       "--output", str(tmp_path / "out" / "snapshot.json")])
    assert rc != 0
    assert not (tmp_path / "out").exists()


def test_the_runbook_does_not_call_the_unvalidated_snapshot_routine():
    """The same page's other quiet claim. §2 must carry the skip line verbatim
    and say what it MEANS — that the snapshot was not schema-checked — because
    the old one-liner read as routine.

    It must also be true of the merged behaviour: since defect 8 the validator
    is searched from the output path AND from `--repo-root`, so the documented
    launch validates and the page may no longer say the skip is what a temp run
    dir gets you. `--run-dir` survives as a remedy, not as the cause."""
    prose = _prose(_section(_runbook(), "2. Prerequisites"))
    assert "validation SKIPPED" in prose
    assert "NOT checked against the pinned schema" in prose
    assert "--run-dir" in prose
    assert "--repo-root" in prose, (
        "§2 must name the second search root, or it describes the old behaviour")
    assert "not at --repo-root" not in prose, (
        "the pre-defect-8 claim: the search no longer stops at the output path")


# `test_the_check_matrix_start_line_carries_the_same_two_flags` stayed with
# `docs/check-matrix.md` in codexFactory (see the CHECK_MATRIX note at the top
# of this file).


# --------------------------------------------------------------------------
# finding 18 — §4's posture readings are the ones the page can actually render
# --------------------------------------------------------------------------

MODEL_JS = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
            / "staging-workbench-model.js")


def test_the_runbook_lists_the_posture_readings_the_page_can_produce():
    """§4 enumerates what the session bar reads, so it is a claim about the model.
    Finding 18 added two AMBIGUOUS readings — the honest answer where a live ref is
    both this tile's ordinal and another tile's own branch — and a doc that omitted
    them would leave the human with an unexplained chip at the one moment the page
    deliberately withholds a command.

    Each reading's distinctive fragment must exist on BOTH sides: in §4's block and
    in the model that composes the label."""
    section = _section(_runbook(), "4. Reading the session on the surface")
    chips = re.search(r"```text\n(.*?)```", section, re.DOTALL)
    assert chips, "§4 lists no posture readings"
    listed = chips.group(1)
    model = MODEL_JS.read_text(encoding="utf-8")
    for fragment in ("no branch session", "session live · ", "DRAFT VIEW · ",
                     "another tile's session", "AMBIGUOUS session",
                     "session ENDED · ", "session AMBIGUOUS · "):
        assert fragment in listed, f"§4 does not list {fragment!r}"
        assert fragment in model, f"the model composes no {fragment!r}"
    # and §4 says WHY an ambiguous reading exists and what it withholds
    prose = _prose(section)
    assert "session-owner/" in prose
    assert "no ref" in prose and "notebook" in prose


# --------------------------------------------------------------------------
# C7 — the derived-artifact inventory is COMPLETE
# --------------------------------------------------------------------------

def test_the_derived_artifact_inventory_names_every_container_the_code_writes():
    """C7: §5 promises where every derived artifact lives. The two markers that
    outlive the branch — the pending dispatch and the ending — were missing, so a
    human cleaning up after a half-finished ending had nowhere to look.

    The paths are DERIVED from the production constants here, so a rename cannot
    leave the doc quietly wrong."""
    section = _prose(_section(_runbook(), "5. Where the derived artifacts live"))
    for subdir, suffix in ((bs.SESSIONS_SUBDIR, ""),
                           (bs.SNAPSHOTS_SUBDIR, bs.SNAPSHOT_SUFFIX),
                           (bs.OWNER_SUBDIR, bs.OWNER_SUFFIX),
                           (bs.DISPATCH_SUBDIR, bs.DISPATCH_SUFFIX),
                           (bs.ENDING_SUBDIR, bs.ENDING_SUFFIX)):
        assert subdir in section, f"§5 does not name {subdir}/"
        assert not suffix or suffix in section, f"§5 does not name {suffix}"
    # and it says what each one MEANS and how to clean it up, which is the point
    assert "half-finished" in section.lower() or "HALF-FINISHED" in section
    assert "open-pr" in section and "abandon-session" in section
    assert "git worktree prune" in section


def test_the_ended_residue_report_names_the_marker_that_produced_it(tmp_path):
    """C7, second half: the stale report is what a human sees when an ending could
    not finish, and it told them to clean up residue without naming the file whose
    existence makes it residue. Driven through the REAL bootstrap over a real
    worktree, so the path in the message is the path on disk."""
    repo = build_scratch_repo(tmp_path)
    git = sg.SessionGit(repo.root)
    registry = _registry(repo, tmp_path)
    bs.open_session(git, registry, repository=REPO,
                    tile=bs.Tile(bs.STAGED_TOPIC, TOPIC), checkout_root=repo.root)
    # the ending happened and its teardown did not finish — the production writer
    marker = bs.write_ending_marker(repo.root, DRAFT, ending=bs.ENDING_ABANDON,
                                    residue=("the worktree could not be removed",))

    fresh = reg.SnapshotRegistry()
    report = bs.bootstrap_sessions(fresh, repository=REPO, checkout_root=repo.root)

    residue = [n for n in report.stale if n.kind == bs.ENDED_SESSION_RESIDUE]
    assert len(residue) == 1, report.summary()
    assert str(marker) in residue[0].reason
    assert marker.is_file()
    assert bs.ENDING_SUFFIX in residue[0].reason


# --------------------------------------------------------------------------
# C5 — the merge ending, as the doc describes it and as the build performs it
# --------------------------------------------------------------------------

# The pull the human performs, as BOTH surfaces must spell it. Not a transcription
# of either one: each assertion below derives its own subject and this is only the
# shape they have to share.
_FETCH = "fetch origin main"
_FF_ONLY = "merge --ff-only origin/main"


def _registry(repo, tmp_path, *, name="main-snapshot.json"):
    path = tmp_path / name
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _save(repo, registry, *, port, at=None):
    body = {"scope_kind": bs.STAGED_TOPIC, "scope_id": TOPIC}
    if at:
        body["at"] = at
    return gr.run_gate_action(
        "open-pr", body, checkout_root=repo.root, actor="brett",
        snapshot_path=None, session_registry=registry,
        repository=repo.repository, session_pull_requests=port)


def _merge_master_merges(repo, tmp_path) -> str:
    """The Merge Master's action as it really happens: `--no-ff` in the ORIGIN, by
    somebody else, head branch deleted, and the served checkout never told."""
    elsewhere = tmp_path / "merge-master-clone"
    subprocess.run(["git", "clone", "--quiet", str(repo.origin), str(elsewhere)],
                   check=True, capture_output=True)

    def run(*args):
        return subprocess.run(["git", *args], cwd=str(elsewhere), check=True,
                              text=True, capture_output=True).stdout.strip()

    run("config", "user.email", "merge-master@example.invalid")
    run("config", "user.name", "Merge Master")
    run("config", "commit.gpgsign", "false")
    run("merge", "--no-ff", "-m", f"Merge pull request for {DRAFT}",
        f"origin/{DRAFT}")
    run("push", "origin", "main")
    run("push", "origin", "--delete", DRAFT)
    return run("rev-parse", "HEAD")


def test_the_merge_ending_the_runbook_promises_is_the_one_the_build_performs(
        tmp_path):
    """C5, end to end. Brett's pass ends here: the pull request is merged on
    GitHub, he returns to the dashboard, and he saves expecting the session to end.

    What the build does is refuse `base_stale` — correctly, because a base it
    cannot see cannot answer whether the branch merged (finding 9) — and the pull
    that resolves it is a HUMAN action, since no session operation fetches
    (FR-026/D17). So the honest end-state is that the pull is a NAMED step of the
    ending: this test drives the whole sequence and requires the refusal to name
    the very commands the runbook names, and the identical save to succeed once
    they have been run."""
    repo = build_scratch_repo(tmp_path)
    registry = _registry(repo, tmp_path)
    git = sg.SessionGit(repo.root)
    opened = bs.open_session(git, registry, repository=REPO,
                             tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
                             checkout_root=repo.root)
    gate = HumanGate(opened.worktree,
                     ["ideation/dashboard/gate-records/", "ideation/staging/"],
                     human_actor="brett")
    (Path(opened.worktree) / DOC).parent.mkdir(parents=True, exist_ok=True)
    (Path(opened.worktree) / DOC).write_text("# Note\n\nthe session's work.\n",
                                             encoding="utf-8")
    at = "2026-07-27T12:00:00Z"
    bs.commit_gate_action(
        gate, git, worktree=opened.worktree, branch=DRAFT,
        record=gc.build_gate_action_record(
            actor="brett", action=gc.ACTION_EDIT_DOCUMENT, at=at, ref=DRAFT,
            document=DOC,
            artifacts=[bs.commit_artifact(bs.action_stamp(at))]),
        documents=[DOC])

    port = spr.FakePullRequests()
    assert _save(repo, registry, port=port, at="2026-07-27T12:00:01Z")[0] == 200
    repo.git("push", "origin", DRAFT)
    remote_main = _merge_master_merges(repo, tmp_path)
    assert repo.head("main") != remote_main

    # the save the runbook says ends the session
    status, payload = _save(repo, registry, port=port, at="2026-07-27T12:00:02Z")

    assert status == 409, payload
    message = payload["message"]
    # it does not merely say "update the served checkout": it says HOW, with the
    # served root, and it says the step is the runbook's own
    assert f"git -C {repo.root} {_FETCH}" in message
    assert f"git -C {repo.root} {_FF_ONLY}" in message
    assert "MANDATORY" in message and "runbook" in message
    assert bs.is_live(registry, REPO, DRAFT) is True     # nothing was reconciled
    assert Path(opened.worktree).is_dir()

    # THE DOCUMENTED HUMAN STEP, run verbatim from the refusal
    repo.git("fetch", "origin", "main")
    repo.git("merge", "--ff-only", "origin/main")

    status, payload = _save(repo, registry, port=port, at="2026-07-27T12:00:03Z")

    assert status == 200, payload
    assert payload["merged"] is True
    assert payload["branch_deleted"] is True
    assert Path(opened.worktree).is_dir() is False
    assert bs.is_live(registry, REPO, DRAFT) is False


def test_the_runbook_names_the_pull_the_refusal_names():
    """C5's other half: the doc and the code must agree. §6's merge-ending bullet
    names the pull as a REQUIRED step and says what skipping it produces — a
    `base_stale` refusal, not a failure. (The check-matrix §8a half of this pin
    stayed with `docs/check-matrix.md` in codexFactory — see the CHECK_MATRIX
    note at the top of this file.)"""
    merge_ending = _prose(_section(_runbook(), "6. Ending a session"))
    assert _FETCH in merge_ending and _FF_ONLY in merge_ending
    assert "base_stale" in merge_ending
    lowered = merge_ending.lower()
    assert "mandatory" in lowered or "required" in lowered


# --------------------------------------------------------------------------
# T092 acceptance sweep, defect 1 — the ownership rule is OPERATING DOCUMENTATION
# --------------------------------------------------------------------------

def test_the_runbook_states_what_a_session_may_rewrite():
    """The rule a human needs BEFORE they meet the refusal: `edit-document`
    rewrites the tile's own material and what the session created, and nothing
    else. It is in the docs because the sweep's finding was not only that the
    route allowed a foreign rewrite — it was that nothing on screen or on the page
    said the picker's rows were not all equally writable.

    Pinned against the CODE's own predicate, not a transcription: the staging
    prefix comes from `gate_routes.tile_owned_prefix`, so a doc that drifts from
    the implementation fails here. (The check-matrix §8 half of this pin stayed
    with `docs/check-matrix.md` in codexFactory — see the CHECK_MATRIX note at
    the top of this file.)"""
    prefix = gr.tile_owned_prefix(bs.Tile(bs.STAGED_TOPIC, "<topic-id>"))
    assert prefix == "ideation/staging/<topic-id>/"

    section = _prose(_section(_runbook(), "3. The session verbs"))
    assert prefix in section
    assert "own material" in section.lower()
    assert "read-only context" in section.lower()
    assert "edit-apply" in section
    # the cluster/possible half — a tile with no folder owns only what it created
    assert "created" in section.lower()
