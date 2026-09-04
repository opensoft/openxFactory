"""Every closed refusal code fires, by name, for a fixture that declares it.

SC-002 in one sentence: a refusal with no fixture and no test does not count as
implemented. This module is the double bookkeeping that makes that true — the
validator's own self-test asserts each fixture fails for its declared code, and
these tests assert the same thing from OUTSIDE the validator, plus the two
properties the self-test cannot check about itself (that the closed set and the
declared codes are the same set, and that a fixture cannot pass by failing for
some other reason).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import NEGATIVES, adjudicate

FIXTURES = sorted(NEGATIVES.glob("*.yaml"))


def _declared(reader) -> dict[Path, tuple[str, str | None]]:
    return {path: reader.expected_failure(path) for path in FIXTURES}


def test_the_corpus_has_a_fixture_per_closed_code(reader) -> None:
    declared = {code for code, _ in _declared(reader).values() if code}
    missing = sorted(reader.REFUSAL_CODES - declared)
    assert not missing, (
        f"no packaged negative fixture declares {missing}. A closed refusal code "
        f"nobody has seen go red is a refusal nobody has tested"
    )


def test_no_fixture_declares_a_code_outside_the_closed_set(reader) -> None:
    """The other direction, which the missing-fixture test cannot see.

    A fixture declaring a code the validator does not define would pass the
    self-test's `code in found` check only by accident, and would silently
    document a refusal that does not exist.
    """
    stray = sorted({code for code, _ in _declared(reader).values()
                    if code and code not in reader.REFUSAL_CODES and code != "schema"})
    assert not stray, f"fixtures declare codes the validator does not define: {stray}"


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_each_fixture_fails_for_the_reason_it_declares(
        path: Path, reader, registry_and_docs, entries, fixture_origins) -> None:
    code, detail = reader.expected_failure(path)
    assert code, (
        f"{path.name}: no `# expected_failure:` header. A fixture that does not "
        f"declare WHY it is invalid pins nothing — any failure would satisfy it"
    )
    import yaml

    findings = reader.Findings()
    registry, schema_docs = registry_and_docs
    try:
        docs = reader.load_records(path)
    except yaml.YAMLError as exc:
        # A FIXTURE MAY BE UNPARSEABLE ON PURPOSE, and exactly one is:
        # `clearing-artifact-unparseable` can only fire on a file that does not
        # parse, so the only fixture able to red-prove it is one that does not
        # parse. The `# expected_failure:` header still reads, because it is
        # taken from raw lines rather than from YAML. This mirrors the
        # validator's own self-test rather than special-casing a filename.
        reader.note_unparseable(findings, path, exc, f"negative/{path.name}")
        docs = []
    else:
        assert docs, f"{path.name}: carries no record"
    for index, doc in enumerate(docs):
        reader.validate_record(findings, doc, f"{path.name}#{index}", registry,
                               schema_docs, entries, fixture_origins,
                               reader.NOW_SENTINEL)
    assert findings.errors, f"{path.name}: validated cleanly; it declares {code!r}"
    codes = reader.codes_of(findings.errors)
    assert code in codes, f"{path.name}: declares {code!r}, got {sorted(codes)}"
    if detail:
        matching = reader.lines_for(findings.errors, code)
        assert any(detail in line for line in matching), (
            f"{path.name}: {code!r} fired but not for {detail!r}: {matching}"
        )


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_each_fixture_explains_itself(path: Path) -> None:
    """A fixture's header must cite the requirement it violates.

    The corpus is documentation as much as it is a test: a reader who wants to
    know what the boundary refuses reads these files. A fixture with a code and
    no prose leaves the WHY in a commit message nobody opens.
    """
    header = [line for line in path.read_text(encoding="utf-8").splitlines()
              if line.startswith("#")]
    prose = [line for line in header if "expected_failure" not in line]
    assert len(prose) >= 4, f"{path.name}: header explains nothing"
    joined = " ".join(prose)
    assert "VIOLATES" in joined, (
        f"{path.name}: the header does not name the requirement it violates"
    )


def test_the_whole_corpus_is_clean_end_to_end(reader) -> None:
    """The validator, run exactly as the CI gate runs it, reports nothing.

    Every other test here adjudicates one record at a time. This one runs the
    program: positives, negatives, refusal-code coverage and all.
    """
    assert reader.main([]) == 0


# ------------------------------------------- the sweep's unreadable-file branch

def test_an_unparseable_family_artifact_is_named_not_skipped(
        reader, registry_and_docs, entries, tmp_path) -> None:
    """A file the sweep could not READ is not a file the sweep CLEARED.

    The bug this pins: `repo_scan` caught `yaml.YAMLError` and moved on, so a
    file carrying a family `kind:` and broken badly enough not to parse was
    reported as "0 artifact(s) checked" with exit 0 — a green sweep whose
    greenness came from unreadability. It is the same error the capability
    refuses by name everywhere else ("an unreadable or erroring provider API is
    not a verification that passed"), moved onto the local disk.
    """
    broken = tmp_path / "planted-record.yaml"
    broken.write_text(
        "schema_version: 1\n"
        "kind: xfactory_clearing_dispatch_record\n"
        "lane_declarations: [\n"
        "  : : :\n",
        encoding="utf-8")
    findings = reader.Findings()
    registry, docs = registry_and_docs
    reader.repo_scan(findings, tmp_path, registry, docs, entries, {})
    codes = reader.codes_of(findings.errors)
    assert "clearing-artifact-unparseable" in codes, findings.errors
    assert any("planted-record.yaml" in line for line in findings.errors), (
        "the finding must NAME the file, or a reader cannot act on it"
    )


def test_an_unparseable_file_with_no_family_kind_stays_skipped(
        reader, registry_and_docs, entries, tmp_path) -> None:
    """The limit, stated as a test rather than only in a comment.

    With no parse there is no `kind` to dispatch on, so the branch scans raw
    bytes for a family token. A broken file that names none is somebody else's
    problem: this reader is not the repository's YAML linter, and claiming
    otherwise would make every unrelated syntax error a clearing finding.
    """
    broken = tmp_path / "unrelated.yaml"
    broken.write_text("some: value\nbroken: [\n", encoding="utf-8")
    findings = reader.Findings()
    registry, docs = registry_and_docs
    reader.repo_scan(findings, tmp_path, registry, docs, entries, {})
    assert findings.errors == [], findings.errors


def test_a_parseable_tree_still_reports_its_count(
        reader, registry_and_docs, entries, tmp_path) -> None:
    """The sweep still says how much it checked, which is the note the CI gate
    asserts positively — a green check that walked nothing is a vacuous pass."""
    (tmp_path / "fine.yaml").write_text("some: value\n", encoding="utf-8")
    findings = reader.Findings()
    registry, docs = registry_and_docs
    reader.repo_scan(findings, tmp_path, registry, docs, entries, {})
    assert findings.errors == []
    assert any("0 artifact(s) checked" in line for line in findings.notes), \
        findings.notes
