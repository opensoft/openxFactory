"""`fs_probe` and the six gates it keeps switched on (opensoft/openxFactory#1201).

Brett Heap's ruling on #1201 ("#1201: 1(b), raw OSError, add the 3.14 CI leg")
routes the six gate-disabling read-side probes the #1201 survey found through
ONE strict primitive, with RAW `OSError` propagation: exactly what `Path.exists`
/ `is_dir` / `is_file` / `is_symlink` do through Python 3.13, and what they stop
doing in 3.14, where each answers False for a node whose `stat` fails for any
reason at all.

Two halves. The errno table pins the primitive itself: the 3.12/3.13 allow-list
(ENOENT, ENOTDIR, EBADF, ELOOP) reads as absent, every other errno propagates,
and a real tree gets the same answers as pathlib's. Then one integration test
per gate asserts that the gate RAISES on an unreadable node instead of switching
itself off. Every case runs twice (`pathlib_314`, in `conftest.py`): under this
interpreter's pathlib and under CPython 3.14's own query bodies, so CI's 3.12
proves the gates no longer ask pathlib at all. Under the 3.14 model each gate
test also asserts what the replaced pathlib call answers for the same node,
which is the switched-off verdict the gate used to reach.

Denials are injected at `os.stat`/`os.lstat` (`conftest.ProbeDenial`), never by
`chmod`, which denies nothing to root.
"""

from __future__ import annotations

import errno
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from conftest import AS_OF, ProbeDenial, emulate_pathlib_314

from doc_health import (catalog_baseline, fs_probe, ideation_readiness,
                        ideation_routing, preflight, runner)

import test_tag_hygiene_pinned_targets as pinned

#: The 3.12/3.13 pathlib allow-list: these read as absent.
ABSENT = (errno.ENOENT, errno.ENOTDIR, errno.EBADF, errno.ELOOP)
#: Everything else propagates; a sample that covers the kinds that occur.
PROPAGATED = tuple(getattr(errno, name) for name in (
    "EACCES", "EPERM", "EIO", "ENAMETOOLONG", "ESTALE", "EMFILE")
    if hasattr(errno, name))
#: The two denials each gate is driven with.
GATE_ERRNOS = (errno.EACCES, errno.EIO)

PROBES = {
    "exists": fs_probe.exists,
    "exists-nofollow": lambda p: fs_probe.exists(p, follow_symlinks=False),
    "is_dir": fs_probe.is_dir,
    "is_dir-nofollow": lambda p: fs_probe.is_dir(p, follow_symlinks=False),
    "is_file": fs_probe.is_file,
    "is_file-nofollow": lambda p: fs_probe.is_file(p, follow_symlinks=False),
    "is_symlink": fs_probe.is_symlink,
}


# --- the primitive ------------------------------------------------------------

@pytest.mark.parametrize("err", ABSENT, ids=errno.errorcode.get)
def test_only_the_absence_errnos_read_as_absent(tmp_path, monkeypatch,
                                                pathlib_314, err):
    node = tmp_path / "node"
    node.write_text("x\n", encoding="utf-8")  # there: only the errno says not
    denial = ProbeDenial(monkeypatch, [node], err)
    for name, probe in PROBES.items():
        assert probe(node) is False, name
    assert fs_probe.mode(node) is None
    assert fs_probe.mode(node, follow_symlinks=False) is None
    assert {call for call, _ in denial.denied} == {"stat", "lstat"}


@pytest.mark.parametrize("err", PROPAGATED, ids=errno.errorcode.get)
def test_every_other_errno_propagates_unchanged(tmp_path, monkeypatch,
                                                pathlib_314, err):
    node = tmp_path / "node"
    node.write_text("x\n", encoding="utf-8")
    ProbeDenial(monkeypatch, [node], err)
    for name, probe in PROBES.items():
        with pytest.raises(OSError) as caught:
            probe(node)
        assert caught.value.errno == err, name
        assert caught.value.filename == os.fspath(node), name  # raw, unwrapped


def test_a_real_tree_gets_pathlibs_own_answers(tmp_path, pathlib_314):
    # No injection: every node here is one pathlib answers without an error
    # it swallows on any version (absence, ENOTDIR and ELOOP included), so the
    # two must agree on every node under either model.
    (tmp_path / "file").write_text("x\n", encoding="utf-8")
    (tmp_path / "dir").mkdir()
    (tmp_path / "link-to-file").symlink_to("file")
    (tmp_path / "link-to-dir").symlink_to("dir")
    (tmp_path / "dangling").symlink_to("nowhere")
    (tmp_path / "loop").symlink_to("loop")
    nodes = ["file", "dir", "link-to-file", "link-to-dir", "dangling", "loop",
             "absent", "file/below-a-file"]
    for rel in nodes:
        path = tmp_path / rel
        assert fs_probe.exists(path) == path.exists(), rel
        assert fs_probe.is_dir(path) == path.is_dir(), rel
        assert fs_probe.is_file(path) == path.is_file(), rel
        assert fs_probe.is_symlink(path) == path.is_symlink(), rel
        assert fs_probe.exists(path, follow_symlinks=False) == \
            os.path.lexists(path), rel


def test_an_unrepresentable_path_reads_as_absent():
    # ValueError (an embedded NUL), which pathlib reads as absent through 3.13
    # and os.path does on every version.
    for probe in PROBES.values():
        assert probe("a\x00b") is False


def test_the_314_model_really_swallows_what_fs_probe_propagates(tmp_path,
                                                                monkeypatch):
    # Non-vacuity for every `pathlib_314` case in this suite: under the model,
    # pathlib's own answer for an unreadable node is the swallowed False,
    # while the primitive still raises.
    node = tmp_path / "node"
    node.write_text("x\n", encoding="utf-8")
    ProbeDenial(monkeypatch, [node], errno.EACCES)
    if sys.version_info < (3, 14):
        with pytest.raises(PermissionError):
            node.exists()  # this interpreter's pathlib still raises
    else:
        assert node.exists() is False  # 3.14's own pathlib, natively
    emulate_pathlib_314(monkeypatch)
    assert (node.exists(), node.exists(follow_symlinks=False), node.is_file(),
            node.is_dir(), node.is_symlink()) == (False,) * 5
    with pytest.raises(PermissionError):
        fs_probe.is_file(node)


# --- the six gates ----------------------------------------------------------

def _refuses(call, err):
    with pytest.raises(OSError) as caught:
        call()
    assert caught.value.errno == err


@pytest.mark.parametrize("err", GATE_ERRNOS, ids=errno.errorcode.get)
def test_the_baseline_gate_refuses_an_unreadable_marker(tmp_path, monkeypatch,
                                                        pathlib_314, err):
    # catalog_baseline.is_baseline_complete / load_baseline: "not merged yet"
    # keeps complete-coverage enforcement OFF.
    marker = (tmp_path / catalog_baseline.BASELINE_DIR
              / catalog_baseline.MARKER_NAME)
    assert catalog_baseline.is_baseline_complete(tmp_path) is False  # absent
    assert catalog_baseline.load_baseline(tmp_path) is None
    marker.parent.mkdir(parents=True)
    marker.write_text("{}\n", encoding="utf-8")
    assert catalog_baseline.is_baseline_complete(tmp_path) is True
    ProbeDenial(monkeypatch, [marker], err)
    if pathlib_314 == "cpython-3.14":
        assert marker.is_file() is False  # the old probe: gate OFF
    _refuses(lambda: catalog_baseline.is_baseline_complete(tmp_path), err)
    _refuses(lambda: catalog_baseline.load_baseline(tmp_path), err)


@pytest.mark.parametrize("err", GATE_ERRNOS, ids=errno.errorcode.get)
def test_the_regression_gate_refuses_an_unreadable_previous_report(
        tmp_path, monkeypatch, pathlib_314, err):
    # runner.main: an absent --previous-report is "no baseline, no
    # regressions", so an unreadable one must not read as absent.
    repo = tmp_path / "alpha"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "note.md").write_text("# Note\n\nStatus: draft\n",
                                          encoding="utf-8")
    previous = tmp_path / "previous.md"
    previous.write_text("# previous\n", encoding="utf-8")
    out = tmp_path / "report.md"
    ProbeDenial(monkeypatch, [previous], err)
    if pathlib_314 == "cpython-3.14":
        assert previous.is_file() is False  # the old probe: gate OFF
    _refuses(lambda: runner.main([
        "--single-repo", str(repo), "--family", "tag-hygiene",
        "--as-of", AS_OF.isoformat(), "--previous-report", str(previous),
        "--report-out", str(out)]), err)
    assert not out.exists()  # no report claiming "no regressions"


PREFLIGHT_CASES = {
    # (repository, the node denied)
    "validate-docs.sh": ("alpha", "scripts/validate-docs.sh"),
    "Makefile": ("alpha", "Makefile"),
    "openxFactory-no-arg-validator": (
        "openxFactory", "scripts/validate-avatar-first-ui.py"),
    "domain-stack.yaml": ("alpha", "stack.yaml"),
}


@pytest.mark.parametrize("err", GATE_ERRNOS, ids=errno.errorcode.get)
@pytest.mark.parametrize("case", sorted(PREFLIGHT_CASES))
def test_the_preflight_refuses_an_unreadable_validator(tmp_path, monkeypatch,
                                                       pathlib_314, case,
                                                       err):
    # preflight._entrypoints / run_preflight: a repository with no entrypoint
    # found is logged `(repo, "(none)", True, ...)`, a PASS, and a domain whose
    # stack.yaml is not found drops out of the pin validator's arguments.
    repo, rel = PREFLIGHT_CASES[case]
    paths = {repo: tmp_path / repo}
    node = paths[repo] / rel
    node.parent.mkdir(parents=True, exist_ok=True)
    node.write_text("validate:\n\tfalse\n" if rel == "Makefile" else "x\n",
                    encoding="utf-8")
    ProbeDenial(monkeypatch, [node], err)
    if pathlib_314 == "cpython-3.14":
        assert node.is_file() is False  # the old probe: never run, a PASS
    _refuses(lambda: preflight.run_preflight(paths), err)


@pytest.mark.parametrize("err", GATE_ERRNOS, ids=errno.errorcode.get)
def test_the_pin_ladder_refuses_an_unreadable_record(tmp_path, monkeypatch,
                                                     pathlib_314, err):
    # families._pinned_arm: a record the document's own root holds but
    # cannot stat must not `continue` to the NEXT root's record (the two-root
    # shape of test_tag_hygiene_pinned_targets case (o)(ii)).
    alpha, openx = pinned._two_roots(tmp_path, in_own_root=True)
    ctx = pinned._context({"alpha": alpha, "openxFactory": openx})
    assert pinned._run(ctx)[0].rule.endswith(
        "in root alpha enumerates own-root-capability")  # readable: own root
    record = alpha / "contracts" / "planted-pin.yaml"
    denial = ProbeDenial(monkeypatch, [record, record.resolve()], err)
    if pathlib_314 == "cpython-3.14":
        assert record.is_file() is False  # the old probe: next root judged
        denial.denied.clear()
    _refuses(lambda: pinned._run(ctx), err)
    assert denial.denied


@pytest.mark.parametrize("err", GATE_ERRNOS, ids=errno.errorcode.get)
def test_the_backlog_detector_refuses_an_unreadable_ideation_area(
        tmp_path, monkeypatch, pathlib_314, err):
    # ideation_routing._aggregation_backlog_findings: True is the finding,
    # so an ideation area it cannot stat must not read as compliant.
    ctx = SimpleNamespace(agg_root=tmp_path)
    assert ideation_routing._aggregation_backlog_findings(ctx) == []
    (tmp_path / "ideation").mkdir()
    assert len(ideation_routing._aggregation_backlog_findings(ctx)) == 1
    ProbeDenial(monkeypatch, [tmp_path / "ideation"], err)
    if pathlib_314 == "cpython-3.14":
        assert (tmp_path / "ideation").is_dir() is False  # the old: compliant
    _refuses(lambda: ideation_routing._aggregation_backlog_findings(ctx), err)


@pytest.mark.parametrize("err", GATE_ERRNOS, ids=errno.errorcode.get)
@pytest.mark.parametrize("rel", ("health/document-catalog",
                                 "health/document-catalog/runs"))
def test_the_catalog_tag_guard_refuses_an_unreadable_catalog(
        tmp_path, monkeypatch, pathlib_314, rel, err):
    # ideation_readiness.load_catalog_tags: None is "no catalog", the
    # additive-membership guard OFF. (Today the projection is deferred, so {}
    # and None derive the same clusters; the guard's verdict is what the
    # fold-in turns on once it lands.)
    assert ideation_readiness.load_catalog_tags(tmp_path) is None  # absent
    (tmp_path / "health" / "document-catalog" / "runs" / "2026-07-09") \
        .mkdir(parents=True)
    assert ideation_readiness.load_catalog_tags(tmp_path) == {}  # guard ON
    node = tmp_path / rel
    ProbeDenial(monkeypatch, [node], err)
    if pathlib_314 == "cpython-3.14":
        assert node.is_dir() is False  # the old probe: guard OFF
    _refuses(lambda: ideation_readiness.load_catalog_tags(tmp_path), err)
