"""CLI parity for the `create-document` gate verb
(openxFactory `add-workbench-bullseye-and-create`, change task 4.5).

`ideation-dashboard gate create-document` drives the SAME tested engine the
loopback route drives — the CLI is the terminal surface of the one choke point
(the propose / lens-verb precedent) — and it is what the workbench's gate-OFF
affordance emits as a copyable descriptor (design D8; the descriptor is parsed
against this parser in test_staging_workbench.py, so the two cannot drift).

Hermetic: a tmp checkout, no snapshot generation, no git, no server. The gated
verb is deliberately DISTINCT from the pre-existing non-gated `create`
subcommand, which scaffolds + opens an editor and records nothing — that
distinction is asserted here too.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml as yaml_mod

from conftest import REPO_ROOT  # noqa: F401 (sys.path side effect)

from ideation_dashboard import authoring as authoring_mod
from ideation_dashboard import cli
from ideation_dashboard import gate_console as gate_mod


def _args(root: Path, **over):
    values = {
        "--area": "ideation/brainstorm/",
        "--title": "Centre ring create",
        "--summary": "Why the centre ring exists.",
        "--topics": "ideation-governance, doc-health",
        "--repository-context": "openxFactory",
    }
    values.update(over)
    argv = ["gate", "create-document", "--repo-root", str(root), "--actor", "brett"]
    for flag, value in values.items():
        if value is None:
            continue
        argv += [flag, value]
    return argv


def _records(root: Path):
    return sorted(root.rglob("create-document-*.gate-action.yaml"))


def test_cli_create_document_lands_the_document_and_the_record(tmp_path, capsys):
    rc = cli.main(_args(tmp_path, **{"--source": "workbench scope: staged topic-x"}))
    assert rc == 0
    out = capsys.readouterr().out
    assert "create-document ideation/brainstorm/centre-ring-create.md" in out
    doc = tmp_path / "ideation" / "brainstorm" / "centre-ring-create.md"
    assert doc.is_file()
    text = doc.read_text(encoding="utf-8")
    assert text.startswith("# Centre ring create — Brainstorm\n")
    assert "Status: brainstorm\n" in text
    assert "Topics: ideation-governance, doc-health\n" in text
    assert "Repository context: openxFactory\n" in text
    assert "Source: workbench scope: staged topic-x\n" in text
    records = _records(tmp_path)
    assert len(records) == 1
    record = yaml_mod.safe_load(records[0].read_text(encoding="utf-8"))
    assert record["action"] == "create-document"
    assert record["actor"] == "brett"
    assert record["target"] == {"document": "ideation/brainstorm/centre-ring-create.md"}
    # open question 4's RULING: a first-class `document` kind, not `other`
    assert record["artifacts"] == [
        {"kind": "document", "reference": "ideation/brainstorm/centre-ring-create.md"}]
    # the record lands under the DEFAULT records dir, keyed by the document slug
    assert records[0].relative_to(tmp_path).as_posix().startswith(
        gate_mod.DEFAULT_RECORDS_DIR + "ideation-brainstorm-centre-ring-create/")


def test_cli_create_document_status_is_brainstorm_everywhere_and_overridable(tmp_path):
    """Brett's 2026-07-25 ruling on open question 1: `brainstorm` in EVERY area,
    including a staging topic folder — the packet tie is the PLACEMENT, and the
    CLI must land the same header the browser affordance does."""
    assert cli.main(_args(tmp_path, **{"--area": "ideation/staging/topic-x/",
                                       "--title": "Staged fragment"})) == 0
    landed = (tmp_path / "ideation" / "staging" / "topic-x" / "staged-fragment.md")
    assert "Status: brainstorm\n" in landed.read_text(encoding="utf-8")
    # an explicit --status wins (the dialog keeps the field editable too)
    for name, status in (("Draft fragment", "draft"), ("Organized", "staged")):
        assert cli.main(_args(tmp_path, **{"--area": "ideation/staging/topic-x/",
                                           "--title": name,
                                           "--status": status})) == 0
        slug = name.lower().replace(" ", "-")
        text = (tmp_path / "ideation" / "staging" / "topic-x" / f"{slug}.md")
        assert f"Status: {status}\n" in text.read_text(encoding="utf-8")
    # the reversed helper is gone, so no caller can reintroduce the area rule
    assert not hasattr(authoring_mod, "status_for_area")


def test_cli_create_document_rejects_an_uncreatable_status(tmp_path):
    """A NEW document is never born `ratified` — argparse refuses the value
    before any write, and the enumerated set is the module's own constant."""
    with pytest.raises(SystemExit) as ei:
        cli.main(_args(tmp_path, **{"--status": "ratified"}))
    assert ei.value.code != 0
    assert not list(tmp_path.rglob("*.md"))
    assert "ratified" not in authoring_mod.CREATABLE_STATUSES


def test_cli_create_document_existing_target_refuses_and_persists_nothing(tmp_path, capsys):
    assert cli.main(_args(tmp_path)) == 0
    doc = tmp_path / "ideation" / "brainstorm" / "centre-ring-create.md"
    before = doc.read_bytes()
    capsys.readouterr()
    rc = cli.main(_args(tmp_path, **{"--summary": "a different summary"}))
    assert rc == 1
    err = capsys.readouterr().err
    assert "refused" in err and "create-only" in err
    assert doc.read_bytes() == before          # create-only, byte-identical
    assert len(_records(tmp_path)) == 1        # the refusal recorded nothing new


def test_cli_create_document_requires_the_human_fields(tmp_path):
    for missing in ("--title", "--summary", "--topics", "--repository-context"):
        with pytest.raises(SystemExit) as ei:
            cli.main(_args(tmp_path, **{missing: None}))
        assert ei.value.code != 0, missing
    assert not list(tmp_path.rglob("*.md"))


def test_the_gated_verb_is_distinct_from_the_non_gated_create(tmp_path):
    """`create` (US8) scaffolds + opens an editor and records NOTHING; the gated
    verb records the dispatch. Both drive the same engine, so the header block is
    identical — only the audit differs."""
    parser = cli.build_parser()
    plain = parser.parse_args(["create", "--repo-root", str(tmp_path),
                               "--title", "Plain doc", "--summary", "s",
                               "--topics", "t", "--repository-context", "r",
                               "--no-open"])
    assert plain.func is cli.cmd_create
    assert plain.func(plain) == 0
    assert (tmp_path / "ideation" / "brainstorm" / "plain-doc.md").is_file()
    assert not _records(tmp_path)               # no gate record from the plain path

    assert cli.main(_args(tmp_path, **{"--title": "Gated doc",
                                       "--repository-context": "r",
                                       "--topics": "t",
                                       "--summary": "s"})) == 0
    assert len(_records(tmp_path)) == 1         # the gated path records its dispatch
    plain_text = (tmp_path / "ideation" / "brainstorm" / "plain-doc.md").read_text("utf-8")
    gated_text = (tmp_path / "ideation" / "brainstorm" / "gated-doc.md").read_text("utf-8")
    # one engine, one header contract (only the H1 and the title differ)
    assert plain_text.replace("Plain doc", "X") == gated_text.replace("Gated doc", "X")


@pytest.mark.parametrize("area", ["openspec/changes/", "scripts/",
                                  "ideation/dashboard/gate-records/",
                                  "ideation/staging/../../escape/"])
def test_the_non_gated_create_confines_its_area_too(tmp_path, capsys, area):
    """The NEIGHBOURING verb, closed with the same one definition (PR #49 wave 2).
    `create` records nothing and opens no session, but it writes into the served
    checkout directly — so an unconfined `--area` could drop a document into
    `ideation/dashboard/gate-records/`, the one prefix the immovability fingerprint
    excludes, where it could later be altered or removed with SC-002's oracle
    reporting no change."""
    parser = cli.build_parser()
    args = parser.parse_args(["create", "--repo-root", str(tmp_path),
                              "--title", "Smuggled doc", "--summary", "s",
                              "--topics", "t", "--repository-context", "r",
                              "--area", area, "--no-open"])

    assert args.func(args) == 1
    assert "create refused:" in capsys.readouterr().err
    assert list(tmp_path.rglob("*.md")) == []


def test_cli_exposes_no_create_bypass_flag():
    """No flag on this verb may skip the gate, the create-only rule, or the
    record — the pre-existing pin, extended to the new subcommand's flags."""
    source = Path(cli.__file__).read_text(encoding="utf-8")
    for flag in ("--force", "--override", "--overwrite", "--no-record",
                 "--skip-gate", "--no-gate"):
        assert flag not in source, flag
