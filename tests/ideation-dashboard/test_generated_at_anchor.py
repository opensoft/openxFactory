"""`--generated-at`: the second generation anchor, on the CLI (task 3.6).

`add-nightly-dashboard-refresh` was re-ratified on 2026-09-04 with an amended
recipe in which the credentialed PARENT seals a bounded source artifact and the
artifact-only CHILD generates the snapshot from it. That artifact is not a git
checkout. `generator._generation_stamp` derives `generated_at` by running
`git show -s --format=%cI` INSIDE the scanned tree and `RealGitDates` is
documented to degrade "to None … outside a git checkout" — so on the amended
lane the published snapshot carried NO freshness stamp at all, and nothing
complained: `generation.generated_at` is OPTIONAL in
`contracts/schemas/ideation-dashboard-snapshot.schema.yaml`, so even `--strict`
passed and the image shipped. The recipe in `design.md` Decision 3 step 3 names
`--generated-at <manifest source committer timestamp>`; until this change that
flag did not exist. This module pins the flag and the four properties the lane
depends on.

  * the amended recipe's own `generate` invocation PARSES — both anchors, at the
    same altitude, on the verb the recipe runs;
  * a supplied anchor is recorded VERBATIM and OVERRIDES the git derivation —
    the value is copied from a manifest, and a snapshot that disagreed with the
    manifest it was pinned from would defeat the pinning;
  * a MALFORMED anchor is REFUSED, on stderr, non-zero, with no snapshot file
    left behind — the one place in this package where an unresolvable timestamp
    is fatal rather than omitted, because this one was typed rather than
    discovered (see `cli.GeneratedAtRefused`);
  * ABSENCE changes nothing: the git derivation still runs and an unresolvable
    stamp is still omitted, exactly as before this flag existed.

Hermetic: every generation runs over a scratch corpus under `tmp_path` or the
tracked read-only fixture repo, no scratch tree is a git checkout, and the one
validator-backed test skips when the pinned validator is not reachable.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, FakeGit, find_openxfactory_validator

from ideation_dashboard import cli as cli_mod
from ideation_dashboard.generator import generate_snapshot, is_rfc3339_datetime

VALIDATOR = find_openxfactory_validator()

# The timestamp shape `git show -s --format=%cI` really emits (an explicit
# numeric offset, never `Z`) — the value the sealed manifest carries, so the
# verbatim claim is tested on the spelling the lane will actually pass.
COMMITTER_STAMP = "2026-09-04T01:23:45+00:00"

# What the injected git says the pinned revision was committed at — the value
# the derivation produces when it CAN run, so "the supplied one wins" is a
# claim about two different, both-present answers.
DERIVED_STAMP = "2026-07-12T00:00:00+00:00"

DOC = ("# A note\n\nStatus: brainstorm\nKind: note\n"
       "Summary: a document the projection can see\nTopics: ideation-dashboard\n")


def _corpus(root: Path) -> Path:
    """A minimal corpus checkout in `tmp_path` — a scanned root and one governed
    document. Deliberately NOT a git repository: that is the sealed artifact's
    situation, and the whole reason the anchor has to be passed in."""
    (root / "ideation").mkdir(parents=True, exist_ok=True)
    (root / "ideation" / "note.md").write_text(DOC, encoding="utf-8")
    return root


def _generate(repo_root: Path, output: Path, *extra: str) -> int:
    return cli_mod.main([
        "generate", "--repo-root", str(repo_root), "--repository", "fixture-repo",
        "--source-revision", PINNED_REVISION, "--output", str(output),
        "--no-validate", *extra])


# --------------------------------------------------------------------------
# the interface the amended recipe names
# --------------------------------------------------------------------------

def test_the_amended_recipes_generate_invocation_parses():
    """`design.md` Decision 3, step 3 as amended — spelled out here rather than
    read from the packet, so this test states the INTERFACE the recipe needs and
    keeps stating it if the prose is reworded."""
    args = cli_mod.build_parser().parse_args([
        "generate", "--repo-root", ".", "--repository", "openxFactory", "--strict",
        "--source-revision", PINNED_REVISION,
        "--generated-at", COMMITTER_STAMP,
        "--output", "ctx/health/ideation-dashboard/openxFactory-snapshot.json"])
    assert args.source_revision == PINNED_REVISION
    assert args.generated_at == COMMITTER_STAMP
    assert args.strict is True


def test_both_generation_verbs_carry_the_anchor_and_the_gate_verbs_do_not():
    """The flag lives in the shared `_add_generate_args`, so the two verbs that
    PUBLISH a snapshot cannot diverge. The gate verbs plan against a snapshot
    they never publish and take no timestamp anchor; they keep their own
    `_add_gate_snapshot_args` and are untouched by this change."""
    parser = cli_mod.build_parser()
    common = ["--repo-root", ".", "--repository", "r", "--generated-at", COMMITTER_STAMP]
    assert parser.parse_args(
        ["generate", *common, "--output", "s.json"]).generated_at == COMMITTER_STAMP
    assert parser.parse_args(
        ["generate-and-open", *common, "--no-serve"]).generated_at == COMMITTER_STAMP
    gate = parser.parse_args([
        "gate", "demote", "--repo-root", ".", "--actor", "someone",
        "--repository", "r", "--change-id", "c", "--reason", "why"])
    assert not hasattr(gate, "generated_at")


# --------------------------------------------------------------------------
# verbatim, and it wins
# --------------------------------------------------------------------------

def test_a_supplied_anchor_is_recorded_verbatim(tmp_path):
    """EXACTLY as given: no normalisation of `+00:00` to `Z`, no re-rendering
    through a datetime. The value is an anchor copied from the manifest and the
    snapshot has to agree with it byte for byte."""
    output = tmp_path / "out" / "snapshot.json"
    assert _generate(_corpus(tmp_path / "repo"), output,
                     "--generated-at", COMMITTER_STAMP) == 0
    generation = json.loads(output.read_text(encoding="utf-8"))["generation"]
    assert generation["generated_at"] == COMMITTER_STAMP
    assert generation["source_revision"] == PINNED_REVISION


def test_a_supplied_anchor_overrides_the_git_derived_one():
    """The tree's own git is not consulted when the caller pinned the value —
    the sealed-artifact case is precisely one where any derived answer would be
    wrong (or, in the real sealed tree, simply absent)."""
    git = FakeGit(date=DERIVED_STAMP)
    derived = generate_snapshot(BASE_REPO, "fixture-repo",
                                source_revision=PINNED_REVISION, git=git)
    pinned = generate_snapshot(BASE_REPO, "fixture-repo",
                               source_revision=PINNED_REVISION, git=git,
                               generated_at=COMMITTER_STAMP)
    assert derived["generation"]["generated_at"] == DERIVED_STAMP
    assert pinned["generation"]["generated_at"] == COMMITTER_STAMP


# --------------------------------------------------------------------------
# absence changes nothing
# --------------------------------------------------------------------------

def test_without_the_flag_the_git_derivation_still_runs():
    snapshot = generate_snapshot(BASE_REPO, "fixture-repo",
                                 source_revision=PINNED_REVISION,
                                 git=FakeGit(date=DERIVED_STAMP))
    assert snapshot["generation"]["generated_at"] == DERIVED_STAMP


def test_without_the_flag_an_underivable_stamp_is_still_omitted(tmp_path):
    """The defect this flag ends, pinned as it was: a non-checkout tree yields no
    stamp, the run still succeeds, and nothing says so. The behaviour is
    UNCHANGED — the flag adds a way to supply the value, it does not make its
    absence fatal (making the schema field required would be a contract cut this
    packet does not need)."""
    output = tmp_path / "out" / "snapshot.json"
    assert _generate(_corpus(tmp_path / "repo"), output) == 0
    assert "generated_at" not in json.loads(output.read_text(encoding="utf-8"))["generation"]


# --------------------------------------------------------------------------
# malformed input is refused, not repaired and not degraded
# --------------------------------------------------------------------------

MALFORMED = [
    pytest.param("2026-09-04", id="date-only"),
    pytest.param("2026-09-04T01:23:45", id="no-offset"),
    pytest.param("2026-09-04 01:23:45Z", id="space-separator"),
    pytest.param("2026-02-30T00:00:00Z", id="not-a-day"),
    pytest.param("2026-13-01T00:00:00Z", id="not-a-month"),
    pytest.param("1757000625", id="epoch-seconds"),
    pytest.param("", id="empty"),
]


@pytest.mark.parametrize("value", MALFORMED)
def test_a_malformed_anchor_is_refused_and_leaves_no_snapshot(tmp_path, capsys, value):
    output = tmp_path / "out" / "snapshot.json"
    assert _generate(_corpus(tmp_path / "repo"), output, "--generated-at", value) == 1
    err = capsys.readouterr().err
    assert "--generated-at" in err and repr(value) in err
    assert "RFC 3339" in err
    assert not output.exists(), "a refused run must leave no snapshot behind"


def test_the_refusal_precedes_the_run_dir_on_generate_and_open(tmp_path):
    """`generate-and-open` refuses ahead of minting its run directory, the same
    way it already does for `--repo-root` — a refused run leaves not even an
    empty directory behind."""
    run_dir = tmp_path / "run"
    assert cli_mod.main([
        "generate-and-open", "--repo-root", str(_corpus(tmp_path / "repo")),
        "--repository", "fixture-repo", "--source-revision", PINNED_REVISION,
        "--generated-at", "nonsense", "--run-dir", str(run_dir),
        "--no-serve", "--no-open", "--no-validate"]) == 1
    assert not run_dir.exists()


def test_the_predicate_checks_the_instant_not_only_the_shape():
    """The pattern alone admits `2026-02-30T00:00:00Z`; the parse is what makes
    the check equal to the schema's `format: date-time`."""
    assert is_rfc3339_datetime(COMMITTER_STAMP)
    assert is_rfc3339_datetime("2026-09-04T01:23:45Z")
    assert is_rfc3339_datetime("2026-09-04t01:23:45.500z")
    assert not is_rfc3339_datetime("2026-02-30T00:00:00Z")
    assert not is_rfc3339_datetime("2026-09-04T01:23:45+24:00")
    assert not is_rfc3339_datetime(None)


# --------------------------------------------------------------------------
# and the value the lane will really pass survives the pinned validator
# --------------------------------------------------------------------------

@pytest.mark.skipif(VALIDATOR is None, reason="pinned openxFactory validator not reachable")
def test_a_pinned_anchor_passes_strict_validation(tmp_path, monkeypatch):
    """`--strict` is the lane's gate (design Decision 3 step 3), so the anchor
    has to satisfy the schema's `format: date-time` for real, not merely the
    CLI's own predicate."""
    monkeypatch.setattr(cli_mod, "_locate_validator", lambda *a, **k: VALIDATOR)
    output = tmp_path / "out" / "snapshot.json"
    assert cli_mod.main([
        "generate", "--repo-root", str(BASE_REPO), "--repository", "fixture-repo",
        "--source-revision", PINNED_REVISION, "--generated-at", COMMITTER_STAMP,
        "--strict", "--output", str(output)]) == 0
    assert json.loads(output.read_text(encoding="utf-8")
                      )["generation"]["generated_at"] == COMMITTER_STAMP
