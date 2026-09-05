"""THE RELEASE-TAG GATE: the cut-time half of the release-tag obligation.

`test_release_tag_publication.py` proves what the FAMILY says. This file proves
what the GATE does with it at the one moment a pull request can still be edited
— and, just as importantly, what it declines to say about pull requests that do
not touch the release surface, which is the whole relief `add-release-tag-gate`
exists to deliver (openxFactory #664).

EVERY FIXTURE IS A REAL GIT REPOSITORY WITH A REAL ORIGIN, for the reason the
sibling file states: this family's subject is the difference between a published
ref and a local one, and a fixture that faked a tag would exercise the parser
and prove nothing. The gate inherits that seam untouched — it overrides exactly
one method, `remote_main_sha`, so that the tree under judgment is the pull
request's merge tree rather than published `main`.

THE POSITIVE CONTROL IS THE POINT, EVERYWHERE. A gate that only ever answers
"pass" is indistinguishable from a gate that answers nothing, so each
short-circuit test builds a tree the family WOULD refuse and shows the gate
green anyway BECAUSE the pull request touches no release path — with the same
tree shown red the moment it does.
"""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

from conftest import REPO_ROOT
from doc_health import release_tag_publication as rtp

MANIFEST = rtp.MANIFEST
CHANGELOG = rtp.CHANGELOG

SCRIPT = Path(REPO_ROOT) / "scripts" / "validate-release-tag-gate.py"


def _load():
    """The gate, imported from its hyphenated entrypoint.

    The house pattern for `scripts/validate-*.py` (see
    `tests/openreposhape_pin/test_pin_verifier.py`): the file is the tool, the
    tool is importable, and nothing is duplicated into a module beside it that
    could drift from what the workflow actually runs.
    """
    spec = importlib.util.spec_from_file_location("release_tag_gate", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gate = _load()


# --------------------------------------------------------------- the fixtures

def _git(repo: Path, *args: str):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True)


def _repo(tmp_path: Path, name: str = "work") -> tuple[Path, Path]:
    origin = tmp_path / f"{name}-origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)],
                   check=True, capture_output=True)
    repo = tmp_path / name
    subprocess.run(["git", "init", "-q", "-b", "main", str(repo)],
                   check=True, capture_output=True)
    _git(repo, "config", "user.email", "t@example.invalid")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "tag.gpgSign", "false")
    _git(repo, "remote", "add", "origin", str(origin))
    return repo, origin


def _declare(repo: Path, bundle: str | None, message: str) -> str:
    (repo / "contracts").mkdir(exist_ok=True)
    body = f"contract_bundle_version: {bundle}\n" if bundle else "other: 1\n"
    (repo / MANIFEST).write_text(body)
    paths = [MANIFEST]
    if not (repo / CHANGELOG).exists():
        (repo / CHANGELOG).write_text("# Contract changelog\n")
        paths.append(CHANGELOG)
    _git(repo, "add", *paths)
    _git(repo, "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _cut(repo: Path, bundle: str, message: str = "cut") -> str:
    """A CUT as this repository performs one: the manifest declaration and the
    release inventory move in ONE commit, which is what the versioning policy's
    realization order step 2 requires and what the gate's path filter sees."""
    (repo / "contracts" / "releases").mkdir(parents=True, exist_ok=True)
    (repo / rtp.inventory_path(bundle)).write_text(f"bundle: {bundle}\n")
    (repo / MANIFEST).write_text(f"contract_bundle_version: {bundle}\n")
    paths = [MANIFEST, rtp.inventory_path(bundle)]
    if not (repo / CHANGELOG).exists():
        (repo / CHANGELOG).write_text("# Contract changelog\n")
        paths.append(CHANGELOG)
    _git(repo, "add", *paths)
    _git(repo, "commit", "-q", "-m", f"{message}: {bundle}")
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _land(repo: Path, n: int, prefix: str = "doc") -> str:
    """`n` landings that touch NO release path — the ordinary pull request."""
    head = ""
    for index in range(n):
        target = repo / f"{prefix}-{index}.md"
        target.write_text(f"landing {prefix} {index}\n")
        _git(repo, "add", str(target))
        _git(repo, "commit", "-q", "-m", f"landing {prefix} {index}")
        head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    return head


def _tag(repo: Path, bundle: str, at: str | None = None) -> None:
    args = ["tag", "-a", bundle, "-m", bundle]
    if at:
        args.append(at)
    _git(repo, *args)


def _push(repo: Path) -> None:
    _git(repo, "push", "-q", "--tags", "origin", "main")


def _head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD").stdout.strip()


def _run(repo: Path, head: str | None = None, base: str | None = None):
    return gate.evaluate(repo, head=head or "HEAD", base=base,
                         repo_name="alphaFactory")


# ------------------------------------------------- the short-circuit, and why

def test_a_pull_request_touching_no_release_path_is_green_over_a_tree_the_family_refuses(
        tmp_path):
    """THE WHOLE POINT OF THE PACKET, AND ITS POSITIVE CONTROL IS IN THE SAME
    TEST. A bundle is cut and left untagged; six ordinary landings follow. The
    family refuses that tree at `error` — asserted here so the green below is
    not a green over a clean corpus — and the gate passes every one of those
    landings, because none of them touches the release surface.

    Before `add-release-tag-gate` the same fact reddened the required
    `pytest-suite` on every open pull request in the repository for five and a
    half hours (openxFactory #664, PR #628 through PR #636).
    """
    repo, _ = _repo(tmp_path)
    _cut(repo, "contract-v2.0")
    _land(repo, 6)
    _push(repo)

    from doc_health import ERROR

    class Ctx:
        repo_paths = {"alphaFactory": repo}
        git = gate.MergeTreeGit(_head(repo))

    refused = rtp.fam_release_tag_publication(Ctx())
    assert [f.severity for f in refused] == [ERROR], (
        "the control did not fire: this tree must be one the family refuses, "
        "or the gate's green below proves nothing")

    result = _run(repo)
    assert result.passed, result.lines
    assert result.refusal is None
    assert "no release surface change" in " ".join(result.lines)


def test_the_short_circuit_names_the_manifest_and_the_inventory_prefix_only():
    assert gate.is_release_surface("contracts/manifest.yaml")
    assert gate.is_release_surface("contracts/releases/contract-v2.0.digests.yaml")
    # A CONTRACT FILE IS NOT THE RELEASE SURFACE. Contract bytes change on
    # ordinary pull requests; the surface is the manifest declaration and the
    # inventories that record a cut. A wider filter would move the collateral
    # this packet removes one directory down instead of removing it.
    assert not gate.is_release_surface("contracts/CHANGELOG.md")
    assert not gate.is_release_surface("contracts/schemas/thing.schema.yaml")
    assert not gate.is_release_surface("contracts/releases.md")
    assert not gate.is_release_surface("docs/contract-versioning-policy.md")


# ------------------------------------------------------------ the cutting PR

def test_a_cut_of_a_new_bundle_passes_and_records_the_tag_as_owed(tmp_path):
    """THE HARD CASE, AND THE ONE THE RULING TURNS ON. The tag for a new bundle
    is published AFTER the merge and points at the merge commit — measured over
    every `contract-v3.x` cut this repository has made — so a pre-merge gate
    that required it would be unsatisfiable. The family already answers
    correctly: the declaring commit IS the tip, distance is zero, no finding.
    What the gate adds is that the obligation is RECORDED rather than passed
    over in silence.
    """
    repo, _ = _repo(tmp_path)
    _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0")
    base = _head(repo)
    head = _cut(repo, "contract-v2.1")
    _push(repo)

    result = _run(repo, head=head, base=base)
    assert result.passed, result.lines
    assert result.obligation is not None
    assert "contract-v2.1" in result.obligation
    assert "TAG OWED" in result.obligation


def test_a_cut_while_the_previous_bundle_is_untagged_is_refused(tmp_path):
    """THE STALE BUNDLE — the condition the gate exists to stop at the door. A
    bundle cut and never published, and a SECOND cut landing on top of it, is
    the exact recurrence the family was built for (`contract-v2.3` under
    `contract-v2.4`). The window the family grants a fresh cut is for landings
    that do not touch the release surface; a pull request that touches it again
    is asserting the surface is in order.
    """
    repo, _ = _repo(tmp_path)
    _cut(repo, "contract-v2.0")          # cut, never tagged
    base = _head(repo)
    head = _cut(repo, "contract-v2.1")
    _push(repo)

    result = _run(repo, head=head, base=base)
    assert not result.passed
    assert result.refusal == "gate-findings"
    joined = " ".join(result.lines)
    assert "contract-v2.0" in joined
    assert "SUPERSEDED without ever being published" in joined


def test_the_window_is_not_a_shield_for_a_release_surface_edit(tmp_path):
    """A `warning` REFUSES TOO, and the reason is stated rather than assumed.

    Inside the distance window the family reports `warning`, not `error`. The
    gate refuses on both, which is exactly the bar the retired suite pin held
    ("no error, no warning") — moved, not weakened. The interval is legitimate
    for landings that leave the release surface alone; this pull request does
    not.
    """
    repo, _ = _repo(tmp_path)
    _cut(repo, "contract-v2.0")
    _land(repo, 2)
    base = _head(repo)
    # A release-surface edit that is not a cut: the inventory is rewritten.
    (repo / rtp.inventory_path("contract-v2.0")).write_text("bundle: x\n")
    _git(repo, "add", rtp.inventory_path("contract-v2.0"))
    _git(repo, "commit", "-q", "-m", "touch the inventory")
    head = _head(repo)
    _push(repo)

    result = _run(repo, head=head, base=base)
    assert not result.passed
    assert result.refusal == "gate-findings"
    assert "[warning]" in " ".join(result.lines)


def test_a_misplaced_tag_is_refused_in_the_family_s_own_words(tmp_path):
    repo, _ = _repo(tmp_path)
    _declare(repo, None, "no bundle yet")
    _tag(repo, "contract-v2.0")          # tag on a commit declaring nothing
    base = _head(repo)
    head = _cut(repo, "contract-v2.0")
    _push(repo)

    result = _run(repo, head=head, base=base)
    assert not result.passed
    assert result.refusal == "gate-findings"
    assert "MISPLACED" in " ".join(result.lines)


# ------------------------------------------------------------- version reuse

def test_a_declaration_moved_onto_an_already_published_bundle_is_refused(
        tmp_path):
    """THE ONE DEFECT THE FAMILY CANNOT SEE, which is why the gate asks it
    separately. Where a tag exists and peels to a commit declaring the same
    bundle, `_tag_state` reads `ok` — so a pull request cutting that number a
    SECOND time passes the family and breaks the versioning policy's "a version
    number is never reused".
    """
    repo, _ = _repo(tmp_path)
    first = _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0", first)
    base = _cut(repo, "contract-v2.1")
    _tag(repo, "contract-v2.1", base)
    # and now the manifest goes BACK to a published number
    (repo / MANIFEST).write_text("contract_bundle_version: contract-v2.0\n")
    _git(repo, "add", MANIFEST)
    _git(repo, "commit", "-q", "-m", "re-declare a published bundle")
    head = _head(repo)
    _push(repo)

    result = _run(repo, head=head, base=base)
    assert not result.passed
    assert result.refusal == "gate-version-reuse"
    joined = " ".join(result.lines)
    assert "ALREADY HAS A PUBLISHED TAG" in joined
    assert "never reused" in joined


def test_a_tag_already_peeling_to_the_tree_under_judgment_is_pre_published(
        tmp_path):
    """NOT REUSE, AND THE DISTINCTION IS LOAD-BEARING. A tag that names the very
    tree being judged is the obligation met EARLY. Two real situations reach
    this arm: a tag pushed at the head before merge, and this gate RE-RUN
    against a merge commit after the cut landed. Replayed against openxFactory
    `807a4f47` — the `contract-v3.4` cut, tagged 69 seconds after its merge
    commit —
    the gate passes for exactly this reason.
    """
    repo, _ = _repo(tmp_path)
    base = _declare(repo, None, "no bundle yet")
    head = _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0", head)
    _push(repo)

    result = _run(repo, head=head, base=base)
    assert result.passed, result.lines
    assert "PRE-PUBLISHED" in " ".join(result.lines)
    assert result.obligation is None


def test_a_bundle_below_the_enforcement_floor_is_not_asked_about(tmp_path):
    """The floor is the family's and the gate does not raise it. A cut of a
    pre-enforcement number carries no tag by design, so the reuse arm must not
    fire on it either."""
    repo, _ = _repo(tmp_path)
    base = _declare(repo, None, "no bundle yet")
    head = _cut(repo, "contract-v1.2")
    _push(repo)

    result = _run(repo, head=head, base=base)
    assert result.passed, result.lines
    assert result.obligation is None


# ---------------------------------------------------------------- fail closed

def test_refs_that_cannot_be_listed_refuse_rather_than_pass(tmp_path):
    """FAIL CLOSED, AND THIS IS WHERE THE GATE DIVERGES FROM THE NIGHTLY. The
    family reports a SKIP when it cannot consult the published refs, and the
    retired suite pin tolerated that skip explicitly ("a skip is not a defect").
    It was right to: the nightly reads an environment it does not control. The
    gate is now the ENFORCING moment, so an unasked question is not a pass.
    """
    repo, _ = _repo(tmp_path)
    base = _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0")
    head = _cut(repo, "contract-v2.1")
    _push(repo)
    _git(repo, "remote", "set-url", "origin",
         str(tmp_path / "no-such-origin.git"))

    result = _run(repo, head=head, base=base)
    assert not result.passed
    assert result.refusal == "gate-unaskable"


def test_an_unresolvable_head_refuses(tmp_path):
    repo, _ = _repo(tmp_path)
    _cut(repo, "contract-v2.0")
    result = _run(repo, head="0000000000000000000000000000000000000000")
    assert result.refusal == "gate-unreadable-head"


def test_a_head_with_no_first_parent_refuses_rather_than_guessing(tmp_path):
    """THE SHALLOW-CHECKOUT CASE, NAMED. `--base` defaults to the head's first
    parent because on a `pull_request` run that parent is the base tip. A
    checkout without it cannot be judged, and the refusal says so instead of
    diffing against nothing and short-circuiting green — which would be a gate
    that reports "no release surface change" precisely when it cannot look.
    """
    repo, _ = _repo(tmp_path)
    _cut(repo, "contract-v2.0")          # the ROOT commit: no first parent
    result = _run(repo)
    assert result.refusal == "gate-unreadable-base"


def test_a_failing_diff_refuses_rather_than_short_circuiting_green(tmp_path,
                                                                  monkeypatch):
    """THE WORST DIRECTION FOR THIS ONE TO FAIL. `changed_paths` answering None
    means the gate does not know what the pull request touches — and the arm
    directly below it is the SHORT-CIRCUIT, which passes. Reading "git could
    not tell me" as "nothing under the release surface" would report "no
    release surface change" precisely when nothing could be looked at, which is
    the fail-OPEN this whole design refuses. Injected at the seam, on the real
    code path: only the `diff` invocation fails."""
    repo, _ = _repo(tmp_path)
    base = _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0")
    head = _cut(repo, "contract-v2.1")
    _push(repo)

    real = gate.subprocess.run

    def _fail_only_diff(argv, *args, **kwargs):
        if "diff" in argv:
            class Failed:
                returncode = 1
                stdout = ""
                stderr = "fatal"
            return Failed()
        return real(argv, *args, **kwargs)

    monkeypatch.setattr(gate.subprocess, "run", _fail_only_diff)
    result = _run(repo, head=head, base=base)
    assert result.refusal == "gate-unreadable-diff"
    assert "no release surface change" not in " ".join(result.lines)


def test_a_manifest_that_cannot_be_read_refuses_rather_than_reading_no_bundle(
        tmp_path):
    """THE #338 CONFLATION AT THE GATE'S OWN DOOR. `blobs_at` collapses to None
    only when GIT ITSELF failed, and a gate that read that as "this tree
    declares no bundle" would skip every arm below and pass. `declared_at`
    returns the read's success SEPARATELY from its answer for exactly this
    reason, and this test is what holds the two apart."""
    repo, _ = _repo(tmp_path)
    base = _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0")
    head = _cut(repo, "contract-v2.1")
    _push(repo)

    class BlindGit(gate.MergeTreeGit):
        def blobs_at(self, repo, commit, relpaths):
            return None

    result = gate.evaluate(repo, head=head, base=base,
                           repo_name="alphaFactory", git=BlindGit(head))
    assert result.refusal == "gate-unreadable-manifest"


def test_every_refusal_this_module_can_return_is_enumerated_and_reachable():
    """THE CLOSED SET, CHECKED IN BOTH DIRECTIONS.

    `emitted <= REFUSALS` alone is one-directional (adversarial review on PR
    #668): it catches a refusal the code can return and the table does not
    describe, and says nothing about a table entry no code path can reach — a
    documented refusal that is dead is a promise the gate does not keep. Set
    EQUALITY closes it, and every one of the seven is driven by a test in this
    file, the two hardest of them by fault injection at the git seam
    immediately above.
    """
    source = SCRIPT.read_text()
    emitted = {line.split('"')[1] for line in source.splitlines()
               if 'return Result(REFUSE, "' in line or
               'REFUSE, "gate-' in line}
    emitted = {name for name in emitted if name.startswith("gate-")}
    assert emitted, "the scan found no refusals — it has stopped reading"
    assert emitted == set(gate.REFUSALS), (
        f"undocumented refusal(s): {sorted(emitted - set(gate.REFUSALS))}; "
        f"documented but unreachable: {sorted(set(gate.REFUSALS) - emitted)}")


# ------------------------------------------------------- the workflow's wiring

WORKFLOW = Path(REPO_ROOT) / ".github" / "workflows" / "release-tag-gate.yml"


def _workflow_body() -> str:
    """The workflow with its COMMENTARY STRIPPED.

    Read verbatim, this file's own prose defeats the assertions below: it
    explains at length why there is no `paths:` filter and no `push:` trigger,
    and both tokens appear in that explanation. The assertions are about the
    DIRECTIVES, so the reader that makes them has to be the same one GitHub is.
    """
    return "\n".join(line for line in WORKFLOW.read_text().splitlines()
                     if not line.lstrip().startswith("#"))


def test_the_workflow_runs_this_script_and_reports_under_the_pinned_name():
    """THE CHECK NAME IS THE CONTRACT. A ruleset pins the literal token
    `release-tag-gate`; a job display name would silently de-advise it, which is
    the rule `openxwallet-consumer-gate.yml` and `pytest-suite.yml` both write
    down for themselves.
    """
    body = _workflow_body()
    assert "name: release-tag-gate" in body
    assert "  release-tag-gate:" in body
    assert "scripts/validate-release-tag-gate.py" in body


def test_the_workflow_carries_no_path_filter_and_no_main_push_trigger():
    """BOTH ABSENCES ARE THE DESIGN RATHER THAN OMISSIONS.

    A required context that does not report on some pull requests is "expected
    forever" and blocks the merge, so the short-circuit lives in the JOB and not
    in a `paths:` filter. And a gate running on `push: main` would re-create the
    very red this packet removes, in the window between a cut landing and its
    tag.
    """
    body = _workflow_body()
    assert "paths:" not in body
    assert "push:" not in body
    assert "pull_request:" in body


@pytest.mark.parametrize("token", ["fetch-depth: 0"])
def test_the_workflow_checks_out_enough_history_to_find_the_base(token):
    """The first-parent walk and the base diff both need history. A shallow
    checkout would refuse `gate-unreadable-base` on every pull request."""
    assert token in _workflow_body()


# --------------------------------------------- git itself cannot be executed

def test_an_unrunnable_git_refuses_rather_than_crashing(tmp_path, monkeypatch):
    """COPILOT ON PR #668, AND IT IS A REAL ONE. `subprocess.run` RAISES
    `OSError` rather than returning a non-zero code when the binary itself
    cannot be executed — no `git` on PATH, an unreadable working directory. An
    exception escaping `_run` would exit this tool with an uncontrolled code,
    breaking the "0 or 2, never 1" contract its module docstring states and
    turning a fail-closed refusal into a crash a workflow reads as an
    infrastructure blip rather than as a verdict.

    THE POSITIVE CONTROL IS THAT THE SAME TREE PASSES WITH GIT WORKING, so this
    test cannot pass by refusing for some other reason.
    """
    repo, _ = _repo(tmp_path)
    base = _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0")
    head = _cut(repo, "contract-v2.1")
    _push(repo)
    assert _run(repo, head=head, base=base).passed

    def _explode(*args, **kwargs):
        raise OSError(2, "No such file or directory: 'git'")

    monkeypatch.setattr(gate.subprocess, "run", _explode)
    result = _run(repo, head=head, base=base)
    assert result.code == gate.REFUSE
    assert result.refusal == "gate-unreadable-head"


# ------------------------------------------- a rename is a move, not a create

def test_a_release_member_renamed_out_of_the_surface_is_still_seen(tmp_path):
    """ADVERSARIAL REVIEW ON PR #668, AND IT WAS A REAL HOLE.

    git's `diff` detects renames BY DEFAULT and prints only the DESTINATION
    path. So a pull request that does nothing but
    `git mv contracts/releases/<bundle>.digests.yaml docs/…` came back as a
    single `docs/…` path, the scope test saw nothing under the release surface,
    and the gate exited 0 reporting "no release surface change" — while the
    pull request had REMOVED A RELEASE INVENTORY. The same trick moved
    `contracts/manifest.yaml` out from under the filter.

    The path filter asks WHICH PATHS THIS PULL REQUEST TOUCHES, and a rename
    touches two. `--no-renames` reports both sides.
    """
    repo, _ = _repo(tmp_path)
    _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0")
    base = _cut(repo, "contract-v2.1")
    _tag(repo, "contract-v2.1")
    (repo / "docs").mkdir(exist_ok=True)
    _git(repo, "mv", rtp.inventory_path("contract-v2.1"),
         "docs/moved-v2.1.yaml")
    _git(repo, "commit", "-q", "-m", "move an inventory out of the surface")
    head = _head(repo)
    _push(repo)

    # THE CONTROL FIRST: git really does hide the source side by default, so
    # this test is about the flag rather than about a hypothetical.
    default = _git(repo, "diff", "--name-only", base, head).stdout.split()
    assert default == ["docs/moved-v2.1.yaml"], default

    paths = gate.changed_paths(repo, base, head)
    assert rtp.inventory_path("contract-v2.1") in paths, (
        "the source side of the rename is invisible — the gate would "
        "short-circuit green on a pull request that removed an inventory")
    result = _run(repo, head=head, base=base)
    assert "no release surface change" not in " ".join(result.lines)


def test_the_manifest_renamed_out_of_the_surface_is_still_seen(tmp_path):
    """The same hole through the other member, and the more serious one: with
    the manifest gone the tree declares no bundle at all."""
    repo, _ = _repo(tmp_path)
    base = _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0")
    (repo / "docs").mkdir(exist_ok=True)
    _git(repo, "mv", MANIFEST, "docs/manifest.yaml")
    _git(repo, "commit", "-q", "-m", "move the manifest out of the surface")
    head = _head(repo)
    _push(repo)

    assert MANIFEST in gate.changed_paths(repo, base, head)
    result = _run(repo, head=head, base=base)
    assert "no release surface change" not in " ".join(result.lines)


# ------------------------------- the assertion this packet moved stays moved

PUBLICATION_SUITE = (Path(REPO_ROOT) / "tests" / "doc-health" /
                     "test_release_tag_publication.py")


def _real_repo_family_call_sites(source: str) -> list[str]:
    """Lines binding this family's `repo_paths` to THE REPOSITORY ITSELF.

    The retired pin was exactly one such binding — `repo_paths = {"openxFactory":
    Path(REPO_ROOT)}` — followed by an assertion that the call returned no
    `error` and no `warning`. Every surviving fixture in that file builds a
    throwaway repository under `tmp_path` instead, so a `REPO_ROOT` inside a
    `repo_paths` mapping is the signature of the assertion coming back.
    """
    return [line.strip() for line in source.splitlines()
            if "repo_paths" in line and "REPO_ROOT" in line]


def test_the_publication_suite_carries_no_zero_findings_pin_on_this_repository():
    """THE SCENARIO'S ENFORCEMENT, not just its statement.

    The delta's scenario *The repository's own test suite is asked what it
    asserts about this family* says the suite MUST carry no assertion that this
    repository currently reads zero findings, and MUST still carry the positive
    control. Without a test, that half of the packet is a sentence: the pin
    could be written back in one line and every check would stay green, which
    is exactly how the five-and-a-half-hour outage of 2026-09-03 would return.

    THE PROBE IS SHOWN CAPABLE OF FIRING on the retired line itself, so a
    scanner that has stopped reading cannot pass this test by finding nothing.
    """
    source = PUBLICATION_SUITE.read_text()
    assert _real_repo_family_call_sites(source) == [], (
        "the release-tag-publication family is being run against THIS "
        "repository inside the test suite again — that is the pin "
        "add-release-tag-gate moved into `release-tag-gate`, and it reds every "
        "open pull request for the length of a legitimate tagging window")

    retired = 'class Ctx:\n        repo_paths = {"openxFactory": Path(REPO_ROOT)}\n'
    assert _real_repo_family_call_sites(retired), (
        "the probe cannot see the very line it was written against, so its "
        "silence above proves nothing")

    # AND THE HALF THAT STAYS. A file that asserted nothing at all would also
    # satisfy the rule above, which is not what the scenario says.
    assert "def test_the_probe_can_fire_over_a_tree_constructed_to_be_untagged" \
        in source


# ------------------------------------ a verdict speaks only its own words

def test_a_crafted_bundle_name_never_reaches_a_workflow_command(tmp_path,
                                                                capsys):
    """COPILOT ON PR #668, AND THE HONEST DISPOSITION IS TWO FACTS, NOT ONE.

    The review held that the bundle name — author-controlled, taken from the
    pull request's own manifest, and printed inside a `::notice` — could carry
    `%0A::error::…` and forge a second workflow command, Actions decoding `%0A`
    inside a command. The escaping was added. **But the hazard is not reachable
    today, and a test that claimed otherwise would be theatre:** the `::notice`
    is emitted only after `_at_or_above_floor`, whose grammar is
    `^contract-v<major>.<minor>$` and admits no `%`, so a crafted name is out of
    scope before it can be printed. This test pins THAT — the crafted manifest
    produces no notice and no forged command — and its sibling pins the escaping
    itself, which is defence in depth against a floor in another module widening
    or a second emission site being added here.
    """
    repo, _ = _repo(tmp_path)
    _cut(repo, "contract-v2.0")
    _tag(repo, "contract-v2.0")
    base = _head(repo)
    crafted = "contract-v9.9%0A::error::forged"
    (repo / "contracts" / "releases").mkdir(parents=True, exist_ok=True)
    (repo / rtp.inventory_path(crafted)).write_text("x: 1\n")
    (repo / MANIFEST).write_text(f"contract_bundle_version: {crafted}\n")
    _git(repo, "add", MANIFEST, rtp.inventory_path(crafted))
    _git(repo, "commit", "-q", "-m", "a crafted bundle name")
    head = _head(repo)
    _push(repo)

    # THE CONTROL: the crafted value really is what the manifest declares, so a
    # green below is about the gate's handling and not about a fixture that
    # never carried the payload.
    assert rtp.parse_bundle((repo / MANIFEST).read_bytes()) == crafted

    gate.main([str(repo), "--head", head, "--base", base,
               "--repo-name", "alphaFactory"])
    out = capsys.readouterr().out

    # WHAT A WORKFLOW COMMAND IS, and it is the precise thing to assert.
    # Actions parses a command only where a LINE BEGINS with `::`. The crafted
    # value does appear inside the refusal's plain report text — the skip names
    # the bundle it could not grade — and that is harmless for exactly this
    # reason: an ordinary log line is not decoded and cannot forge anything.
    commands = [line for line in out.splitlines() if line.startswith("::")]
    forged = [c for c in commands
              if not c.startswith("::error title=release-tag-gate::")
              and not c.startswith("::notice title=release-tag-gate::")]
    assert forged == [], f"a manifest value forged a workflow command: {forged}"
    assert not any(c.startswith("::notice") for c in commands), (
        "a bundle name outside the version grammar reached the notice arm")
    # AND THE GATE STILL ANSWERED: a crafted name it cannot grade is a REFUSAL,
    # not a pass, so this test cannot go green on a gate that fell silent.
    assert any(c.startswith("::error title=release-tag-gate::gate-unaskable")
               for c in commands), commands


def test_the_workflow_command_escaping_is_the_one_actions_decodes():
    """The escaping itself, asserted directly, because the arm above proves only
    that today's grammar keeps the payload away from it.

    `%` FIRST IS THE WHOLE CORRECTNESS ARGUMENT: escape the newlines first and
    the `%` they introduce gets escaped again, so `\n` would render as `%250A`
    and Actions would print a literal `%0A` instead of a line break.
    """
    assert gate.workflow_command_safe("a%b") == "a%25b"
    assert gate.workflow_command_safe("a\nb") == "a%0Ab"
    assert gate.workflow_command_safe("a\rb") == "a%0Db"
    assert gate.workflow_command_safe("v9.9%0A::error::forged") == \
        "v9.9%250A::error::forged"
    assert gate.workflow_command_safe("plain text") == "plain text"
