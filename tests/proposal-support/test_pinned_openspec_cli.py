"""`scripts/proposal-support.py` obtains OpenSpec THROUGH the pin (issue #691).

WHAT THESE TESTS ARE ABOUT. The archive wrapper is the sanctioned path by which
a ratified delta enters canon, and until #691 it performed that act with
`["openspec", …]` — a NAME, resolved by the shell from PATH — while
`contracts/openspec-cli-pin.yaml` had made `@fission-ai/openspec` a
content-addressed consumption with `scripts/validate-openspec-cli-pin.py` as the
one entrypoint through which the estate obtains and runs it. On the workstation
the defect was found on, PATH answered `1.2.0` and the pin recorded `1.12.0`.
The properties pinned here are the two the fix exists for: the binary that runs
is the one the pin's own resolver returned, and an unobtainable pin REFUSES
rather than falling through to whatever is nearest.

WHY A FICTIONAL REGISTRY. Every refusal below is a disagreement between a pin
and the bytes a registry served; manufacturing that against the real package
would mean reaching the network from a unit test, which this suite refuses.
`tests/openspec_cli_pin/test_openspec_cli_pin.py` states the rule and takes this
same route, so the fiction is installed at the verifier's SUBPROCESS BOUNDARY
and everything above it — the pin parser, the SHA-512 and SHA-1 over real bytes,
the cache keyed by the verified address, the version assertion — is the real
code under test. The REAL package is checked once, elsewhere, by
`.github/workflows/openspec-cli-pin-gate.yml`.

NOTHING HERE RESTATES THE PIN. The version, the package name and the binary name
are read from `contracts/openspec-cli-pin.yaml` through the verifier's own
parser; a literal copied into this file would be exactly the second copy of a
pin whose divergence is the defect the pin capability exists to write down.
"""
from __future__ import annotations

import ast
import base64
import hashlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

# CAPTURED BEFORE ANY TEST RUNS, and used by `a_change` below instead of the
# module attribute. `recorded` (further down) monkeypatches `support.subprocess
# .run` — the SAME module object this file's own `import subprocess` names,
# since `sys.modules["subprocess"]` is one singleton — to a fake that records
# and answers every call without executing it, which is exactly what the tests
# using that fixture are asserting on (`assert recorded == [...]` counts on
# nothing else having called through it). The origin-retention gate this
# wrapper's `archive_change` now runs (`release-realization` § "Origin
# retention at archive") also shells out to real `git`, so a fixture that needs
# an actual, readable git history has to reach the ORIGINAL function — captured
# here, once, before `recorded` or anything else can replace the name — rather
# than whatever `subprocess.run` currently resolves to.
_REAL_SUBPROCESS_RUN = subprocess.run

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "proposal-support.py"
PIN = ROOT / "contracts" / "openspec-cli-pin.yaml"

PAYLOAD = b"a synthetic tarball standing in for the published OpenSpec artifact"


def _address(payload: bytes) -> tuple[str, str]:
    return ("sha512-" + base64.b64encode(hashlib.sha512(payload).digest()).decode(),
            hashlib.sha1(payload).hexdigest())


@pytest.fixture
def support():
    """A FRESH load of the wrapper per test.

    The wrapper memoizes both the verifier module and the resolved executable
    for the life of a process, which is the behaviour under test in
    `test_the_resolution_is_memoized_once_per_process`; a module shared between
    tests would let one test's fiction answer another's question.
    """
    spec = importlib.util.spec_from_file_location(
        f"proposal_support_pinned_{id(object())}", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def real_pin(support):
    verifier = support.pin_verifier()
    return verifier.read_pin(PIN)


class Registry:
    """The fiction, plus everything a test needs to interrogate it."""

    def __init__(self, verifier, pin_path: Path, version: str, binary: str,
                 calls: list, served: dict) -> None:
        self.verifier = verifier
        self.pin_path = pin_path
        self.version = version
        self.binary = binary
        self.calls = calls
        self.served = served

    def rewrite(self, **fields) -> None:
        """Re-lay the synthetic pin with one or more fields replaced."""
        text = []
        for line in self.pin_path.read_text(encoding="utf-8").splitlines():
            key = line.split(":", 1)[0]
            if key in fields:
                text.append(f"{key}: {fields.pop(key)}")
            else:
                text.append(line)
        for key, value in fields.items():
            text.append(f"{key}: {value}")
        self.pin_path.write_text("\n".join(text) + "\n", encoding="utf-8")


def write_pin(path: Path, real_pin: dict, payload: bytes = PAYLOAD) -> Path:
    """A well-formed synthetic pin, in the real pin's own grammar.

    Written as TEXT so the narrow reader is exercised rather than bypassed, and
    carrying the REAL package, version and binary name read from the real pin —
    only the referent is synthetic, because only the referent has to be.
    """
    integrity, shasum = _address(payload)
    path.write_text(
        "# a synthetic pin\n"
        "schema_version: 1\n"
        "kind: pinned_contract_manifest\n"
        f"package: \"{real_pin['package']}\"\n"
        "source_repository: Fission-AI/OpenSpec\n"
        "registry: https://registry.npmjs.org\n"
        f"version: \"{real_pin['version']}\"\n"
        "revision_kind: package_integrity\n"
        "integrity_algorithm: sha512\n"
        f"integrity: \"{integrity}\"\n"
        f"shasum: \"{shasum}\"\n"
        f"binary: {real_pin['binary']}\n"
        "verify_pin: scripts/validate-openspec-cli-pin.py\n"
        "consumer_entrypoint: scripts/validate-openspec-cli-pin.py\n",
        encoding="utf-8")
    return path


@pytest.fixture
def registry(support, real_pin, tmp_path, monkeypatch):
    """A fictional npm, serving a synthetic artifact the synthetic pin names."""
    verifier = support.pin_verifier()
    version = verifier.pinned_version(real_pin)
    binary = verifier.pinned_binary(real_pin)
    pin_path = write_pin(tmp_path / "pin.yaml", real_pin)
    monkeypatch.setattr(verifier, "PIN_PATH", pin_path)
    monkeypatch.setenv("OPENSPEC_CLI_PIN_CACHE", str(tmp_path / "cache"))

    calls: list = []
    served = {"payload": PAYLOAD, "reports": version}
    real_which = verifier.shutil.which
    # A REAL FILE IN A TEMPORARY DIRECTORY rather than a hard-coded system
    # path: the constitution forbids a host-absolute path in a committed file
    # (§ IV), and a fictional npm that exists where the test put it is the more
    # honest double anyway — `fetch_artifact` asks `shutil.which` whether npm is
    # obtainable at all, and nothing in this suite should depend on where a
    # particular machine keeps it.
    fake_npm = tmp_path / "bin" / "npm"
    fake_npm.parent.mkdir(parents=True, exist_ok=True)
    fake_npm.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_npm.chmod(0o755)

    def fake_run(argv, **kwargs):
        argv = [str(item) for item in argv]
        calls.append(argv)
        if argv[1:2] == ["pack"]:
            destination = Path(argv[argv.index("--pack-destination") + 1])
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "openspec.tgz").write_bytes(served["payload"])
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[1:2] == ["install"]:
            prefix = Path(argv[argv.index("--prefix") + 1])
            (prefix / "bin").mkdir(parents=True, exist_ok=True)
            (prefix / "bin" / binary).write_text("#!/bin/sh\n", encoding="utf-8")
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[1:2] == ["--version"]:
            return subprocess.CompletedProcess(argv, 0, served["reports"] + "\n", "")
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(verifier, "_run", fake_run)
    monkeypatch.setattr(
        verifier.shutil, "which",
        lambda name, *a, **k: (str(fake_npm) if name == "npm"
                               else real_which(name, *a, **k)))
    return Registry(verifier, pin_path, version, binary, calls, served)


def a_change(root: Path, change: str = "change-a") -> Path:
    """The smallest tree `archive_change` will carry past its own two gates.

    A REAL GIT REPOSITORY, one commit, already ratified: the origin-retention
    gate's baseline (`release-realization` § "Origin retention at archive") is
    the origin block standing at the commit that first declares `Status:
    ratified`, and nothing here ever mutates the origin afterwards, so the one
    commit that creates the packet is also its own ratifying commit — no
    separate draft-then-ratify pair is needed the way the mutation fixtures in
    `test_proposal_support.py` need one.

    Built through `_REAL_SUBPROCESS_RUN`, not `subprocess.run`: every test that
    calls this also installs the `recorded` fixture, which fakes and records
    every call reachable through `subprocess.run` (the module attribute the
    origin-retention gate's own git calls resolve through too) so that a test
    can assert the exact sequence of openspec invocations. Routing this
    fixture's git plumbing through the real function — rather than the current
    attribute — means it actually runs and leaves nothing in that recording for
    a caller to see.
    """
    directory = root / "openspec" / "changes" / change
    directory.mkdir(parents=True)
    (directory / "proposal.md").write_text(
        "Status: ratified\n\n## Why\n\nA fixture.\n\n## What Changes\n\n"
        "- Nothing.\n", encoding="utf-8")
    (directory / "tasks.md").write_text(
        "## 1. Test\n\n- [x] 1.1 Complete fixture\n", encoding="utf-8")
    (directory / ".openspec.yaml").write_text(
        "origin:\n"
        "  kind: ad_hoc\n"
        f"  id: fixture:adhoc:2026-09-05-{change}\n"
        "  reason: fixture\n"
        "  approved_by: fixture\n"
        "  approved_on: '2026-09-05'\n", encoding="utf-8")
    _REAL_SUBPROCESS_RUN(["git", "init", "-q"], cwd=root, check=True,
                         capture_output=True, text=True)
    _REAL_SUBPROCESS_RUN(["git", "-C", str(root), "add", "-A"], check=True,
                         capture_output=True, text=True)
    _REAL_SUBPROCESS_RUN(
        ["git", "-C", str(root), "-c", "user.name=Test", "-c",
         "user.email=test@example.invalid", "commit", "-q", "-m",
         "create the fixture, already ratified"],
        check=True, capture_output=True, text=True)
    return directory


@pytest.fixture
def recorded(support, monkeypatch):
    """Every `subprocess.run` this wrapper and the entrypoint issue, recorded —
    EXCEPT `git`, which is passed through to the real function and left off the
    list.

    Patched on the `subprocess` module itself, which both files hold, so the
    entrypoint's own `run_validation` is captured on the same list as the
    wrapper's archive — the point being to compare WHICH BINARY each of them
    reached for. `archive_change` now runs the origin-retention gate
    (`release-realization` § "Origin retention at archive") BEFORE either of
    those, and that gate reads real git history through this exact attribute —
    `ratifying_commit`, `git_show_text` and `repo_revision` all call
    `subprocess.run(["git", …])` too. Faking those the way this fixture fakes
    openspec/npm would answer every `git log`/`git show` with empty output
    regardless of what `a_change` committed to disk, so a `git` argv is routed
    to `_REAL_SUBPROCESS_RUN` and excluded from `ran`: the equality assertions
    below stay a claim about the openspec/npm calls this fixture exists to
    watch, not about the fixture's own git plumbing.
    """
    ran: list = []
    # THE DATE IS FROZEN FOR THE WHOLE TEST, once, on the module the test and
    # the double BOTH read it from. Without this the fixture reads
    # `utc_today()` when it names the directory and the test reads it again
    # when it passes `--date`, and a run straddling midnight UTC would make the
    # wrapper CORRECTLY refuse `archive-date-mismatch` — a green assertion
    # turned into a nightly flake by the calendar rather than by the code.
    frozen = support.utc_today()
    monkeypatch.setattr(support, "utc_today", lambda: frozen)

    def fake_run(argv, **kwargs):
        argv = [str(item) for item in argv]
        if argv[:1] == ["git"]:
            return _REAL_SUBPROCESS_RUN(argv, **kwargs)
        ran.append(argv)
        # AN `archive` ARGV MOVES THE DIRECTORY, because since #790 the wrapper
        # ASSERTS what the CLI named: it reads `openspec/changes/archive/`
        # before and after the child and refuses `archive-date-mismatch` when
        # exactly `<date>-<change>` did not appear. A fake that recorded the
        # argv and moved nothing is a CLI that archived nothing, and every test
        # here would refuse on that rather than on the argv it exists to watch.
        # The date used is the wrapper's OWN `utc_today()` — the same clock the
        # caller's `--date` reads — so the two agree by construction and no
        # literal in this file can age into a mismatch.
        if argv[1:2] == ["archive"] and len(argv) > 2:
            change = argv[2]
            root = Path(kwargs.get("cwd", "."))
            source = root / "openspec" / "changes" / change
            destination = (root / "openspec" / "changes" / "archive" /
                           f"{support.utc_today()}-{change}")
            if source.is_dir():
                destination.parent.mkdir(parents=True, exist_ok=True)
                source.rename(destination)
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(support.subprocess, "run", fake_run)
    return ran


# ------------------------------------------------------ the wiring itself ----

def test_the_resolver_is_the_entrypoint_the_pin_itself_names(support, real_pin):
    """Not `a` verifier — THE one the pin declares, by both of its own keys."""
    assert support.PIN_VERIFIER == ROOT / real_pin["consumer_entrypoint"]
    assert support.PIN_VERIFIER == ROOT / real_pin["verify_pin"]
    assert support.PIN_VERIFIER.is_file()


def test_no_argv_in_this_script_begins_with_the_bare_binary_name(support,
                                                                 real_pin):
    """THE DEFECT ITSELF, pinned against the source.

    `["openspec", "archive", change]` was the whole of issue #691, and a helpful
    future edit that reintroduces one anywhere in this file — for a `validate`,
    an `archive`, a `list`, a diff — must fail here rather than in somebody's
    canon. The check is AST-level, so the prose above may quote the defect and
    the path segments `root / "openspec" / "changes"` are untouched: what is
    forbidden is a command whose first word is the binary's NAME.
    """
    binary = support.pin_verifier().pinned_binary(real_pin)
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    heads = [node.elts[0].value
             for node in ast.walk(tree)
             if isinstance(node, ast.List) and node.elts
             and isinstance(node.elts[0], ast.Constant)
             and isinstance(node.elts[0].value, str)]
    assert binary not in heads, (
        f"an argv beginning with the bare name {binary!r} is issue #691")


def test_the_wrapper_originated_refusal_codes_are_exactly_what_it_raises(
        support):
    """The declared list and the raised codes are ONE fact, checked both ways.

    The refusal vocabulary belongs to the pin verifier; the two codes this
    wrapper originates are the conditions the verifier cannot report about
    itself, and they are declared in `WRAPPER_REFUSAL_CODES`. A list that
    drifted from the code would be a caller branching on a name nothing raises,
    or a raised name no reader was told about — which is exactly the drift
    Copilot caught on PR #694, when the prose said "exactly one" and the code
    raised two.
    """
    raised = {node.args[0].value
              for node in ast.walk(ast.parse(SCRIPT.read_text(encoding="utf-8")))
              if isinstance(node, ast.Call)
              and isinstance(node.func, ast.Name)
              and node.func.id == "PinnedCliRefusal"
              and node.args and isinstance(node.args[0], ast.Constant)
              and isinstance(node.args[0].value, str)}
    assert raised == set(support.WRAPPER_REFUSAL_CODES)
    # …and every one of them is OUTSIDE the verifier's own vocabulary, because a
    # name that collided with one would make a caller's branch mean two things.
    verifier_codes = set(support.pin_verifier().REFUSAL_CODES)
    assert raised.isdisjoint(verifier_codes)


def test_the_archive_runs_the_resolved_binary_and_never_a_bare_name(
        support, registry, recorded, tmp_path):
    """The end-to-end property: both halves ran, and both ran the PINNED path."""
    root = tmp_path / "repo"
    a_change(root)

    support.archive_change(root, "change-a", support.utc_today(), False, True)

    resolved = support.pinned_openspec()
    assert str(resolved).startswith(str(tmp_path / "cache"))
    assert [argv for argv in recorded] == [
        [str(resolved), "validate", "change-a", "--strict"],
        [str(resolved), "archive", "change-a", "--yes"],
    ]
    assert all(argv[0] != registry.binary for argv in recorded)
    # The artifact was FETCHED and HASHED, not assumed: `resolve_pinned` packs
    # and installs through the (fictional) registry every run.
    assert any(argv[1:2] == ["pack"] for argv in registry.calls)
    assert any(argv[1:2] == ["install"] for argv in registry.calls)


def test_the_strict_validation_goes_through_the_consumer_entrypoint(
        support, registry, recorded, tmp_path, monkeypatch):
    """Validation is DELEGATED, so the pin's dispositions apply to it.

    The entrypoint is where an ERROR this repository has accepted in writing —
    with a citation and a named authority — stops blocking. A wrapper that
    assembled its own `validate` argv would re-ask the question with a rawer
    tool and refuse an archive the pin has already settled, which is how an
    operator ends up back at a bare CLI and around this gate entirely.
    """
    seen: list = []
    real_main = registry.verifier.main
    monkeypatch.setattr(registry.verifier, "main",
                        lambda argv: (seen.append(list(argv)), real_main(argv))[1])
    root = tmp_path / "repo"
    a_change(root)

    support.archive_change(root, "change-a", support.utc_today(), False, True)

    assert seen == [["--change", "change-a", "--repo", str(root)]]


def test_the_resolution_is_memoized_once_per_process(support, registry):
    first = support.pinned_openspec()
    second = support.pinned_openspec()
    assert first == second
    assert len([argv for argv in registry.calls if argv[1:2] == ["pack"]]) == 1


# ------------------------------------------------------------- refusals ------

def test_a_movable_referent_refuses_before_a_registry_round_trip(support,
                                                                 registry):
    """A pin that records a RANGE is a defect of the pin, named as one.

    And named BEFORE anything is fetched: the shape checks are the entrypoint's
    check 1, and a refusal that spent a round trip on its way to a conclusion it
    already held would send a reviewer looking at the network.
    """
    registry.rewrite(version='"^1.12.0"')
    with pytest.raises(support.PinnedCliRefusal) as caught:
        support.pinned_openspec()
    assert caught.value.code == "pin-tag-only"
    assert registry.calls == []


def test_bytes_that_are_not_the_pinned_bytes_refuse_rather_than_running(
        support, registry, recorded, tmp_path):
    """A registry serving something else is refused, and NOTHING is invoked.

    The whole hazard of the defect was that an unanswerable question about which
    tool would run got answered by PATH. Here the question is unanswerable and
    the archive simply does not happen.
    """
    registry.served["payload"] = b"other bytes entirely"
    root = tmp_path / "repo"
    a_change(root)
    with pytest.raises(support.PinnedCliRefusal) as caught:
        support.archive_change(root, "change-a", "2026-09-05", False, True)
    assert caught.value.code == "pin-integrity-mismatch"
    assert recorded == []
    assert not (root / "openspec" / "changes" / "archive").exists()


def test_an_unobtainable_artifact_refuses_and_says_so_by_name(support, registry,
                                                              recorded,
                                                              tmp_path,
                                                              monkeypatch):
    """`npm` absent is the plainest form of "the pin cannot be obtained"."""
    monkeypatch.setattr(registry.verifier.shutil, "which",
                        lambda name, *a, **k: None)
    root = tmp_path / "repo"
    a_change(root)
    with pytest.raises(support.PinnedCliRefusal) as caught:
        support.archive_change(root, "change-a", "2026-09-05", False, True)
    assert caught.value.code == "pin-unresolvable"
    assert recorded == []


def test_a_refusal_exits_two_and_prints_the_verifiers_own_words(
        support, registry, recorded, tmp_path, monkeypatch, capsys):
    """EXIT 2, and the message is the verifier's, trailer and all.

    Exit 1 in this script has always meant "this change is not archivable"; a
    pin that cannot be satisfied is a different fact and takes the exit the pin
    verifier and the pinned installer already use for it.
    """
    registry.rewrite(version='"latest"')
    root = tmp_path / "repo"
    a_change(root)
    monkeypatch.setattr(sys, "argv",
                        ["proposal-support.py", str(root), "archive",
                         "change-a", "--yes"])
    with pytest.raises(SystemExit) as caught:
        support.main()
    assert caught.value.code == 2
    printed = capsys.readouterr().err
    assert "REFUSE pin-tag-only" in printed
    assert "Remediation:" in printed
    assert recorded == []


def test_a_strict_failure_is_still_exit_one_and_archives_nothing(
        support, registry, recorded, tmp_path, monkeypatch):
    """The two verdicts stay apart. A failing delta is not a failing pin."""
    monkeypatch.setattr(registry.verifier, "main", lambda argv: 1)
    root = tmp_path / "repo"
    a_change(root)
    with pytest.raises(support.SupportError) as caught:
        support.archive_change(root, "change-a", "2026-09-05", False, True)
    assert "--strict" in str(caught.value)
    assert not any(argv[1:2] == ["archive"] for argv in recorded)


def test_an_entrypoint_refusal_becomes_a_refusal_here_too(
        support, registry, recorded, tmp_path, monkeypatch):
    """Exit 2 out of the entrypoint is exit 2 out of this wrapper.

    The entrypoint refuses for reasons of its own that the resolver cannot see —
    an unidentifiable repository under a pin that declares dispositions, a
    disposition gone stale — and none of them is a licence to archive anyway.
    """
    monkeypatch.setattr(registry.verifier, "main", lambda argv: 2)
    root = tmp_path / "repo"
    a_change(root)
    with pytest.raises(support.PinnedCliRefusal) as caught:
        support.archive_change(root, "change-a", "2026-09-05", False, True)
    assert caught.value.code == "pin-refused"
    assert not any(argv[1:2] == ["archive"] for argv in recorded)


def test_an_absent_entrypoint_is_a_named_refusal_and_not_a_fallback(
        support, monkeypatch, tmp_path):
    """The one refusal code this file owns, for the one condition the verifier
    cannot report: the verifier being unreachable."""
    monkeypatch.setattr(support, "PIN_VERIFIER", tmp_path / "not-here.py")
    monkeypatch.setattr(support, "_PIN_VERIFIER_MODULE", None)
    with pytest.raises(support.PinnedCliRefusal) as caught:
        support.pinned_openspec()
    assert caught.value.code == "pin-entrypoint-unavailable"


# --------------------------------------------------- the one escape hatch ----

def test_the_escape_is_the_entrypoints_own_and_refuses_another_version(
        support, registry, tmp_path, monkeypatch):
    """`--path-mode` is not a bypass: it checks the version and REFUSES.

    It is the verifier's flag with the verifier's semantics — the label, not the
    referent — and this is the case it exists to catch: yesterday's global
    install answering for today's pin.
    """
    # `path-bin`, not `bin`: the registry fixture keeps its fictional npm in
    # `bin`, and this is the PATH the escape reads — two different fictions.
    local = tmp_path / "path-bin"
    local.mkdir()
    (local / registry.binary).write_text("#!/bin/sh\n", encoding="utf-8")
    (local / registry.binary).chmod(0o755)
    monkeypatch.setattr(
        registry.verifier.shutil, "which",
        lambda name, *a, **k: (str(local / registry.binary)
                               if name == registry.binary else None))
    registry.served["reports"] = "9.9.9"

    with pytest.raises(support.PinnedCliRefusal) as caught:
        support.pinned_openspec(path_mode=True)
    assert caught.value.code == "pin-version-mismatch"
    assert "9.9.9" in str(caught.value)
    assert registry.version in str(caught.value)


def test_the_escape_accepts_the_pinned_version_and_says_what_it_did_not_check(
        support, registry, tmp_path, capsys, monkeypatch):
    # `path-bin`, not `bin`: the registry fixture keeps its fictional npm in
    # `bin`, and this is the PATH the escape reads — two different fictions.
    local = tmp_path / "path-bin"
    local.mkdir()
    (local / registry.binary).write_text("#!/bin/sh\n", encoding="utf-8")
    (local / registry.binary).chmod(0o755)
    monkeypatch.setattr(
        registry.verifier.shutil, "which",
        lambda name, *a, **k: (str(local / registry.binary)
                               if name == registry.binary else None))

    resolved = support.pinned_openspec(path_mode=True)

    assert resolved == local / registry.binary
    # Nothing was fetched, and the run SAYS the bytes were not hashed rather
    # than letting a reader carry the pinned mode's guarantee into this one.
    assert registry.calls == [[str(resolved), "--version"]]
    assert "NOT hashed against the pin" in capsys.readouterr().out


def test_the_escape_reaches_the_entrypoint_too_so_the_halves_agree(
        support, registry, recorded, tmp_path, monkeypatch):
    """One mode, both halves. A run that validated from PATH and archived from
    the artifact — or the reverse — would be two runs wearing one name."""
    # `path-bin`, not `bin`: the registry fixture keeps its fictional npm in
    # `bin`, and this is the PATH the escape reads — two different fictions.
    local = tmp_path / "path-bin"
    local.mkdir()
    (local / registry.binary).write_text("#!/bin/sh\n", encoding="utf-8")
    (local / registry.binary).chmod(0o755)
    monkeypatch.setattr(
        registry.verifier.shutil, "which",
        lambda name, *a, **k: (str(local / registry.binary)
                               if name == registry.binary else None))
    seen: list = []
    monkeypatch.setattr(registry.verifier, "main",
                        lambda argv: seen.append(list(argv)) or 0)
    root = tmp_path / "repo"
    a_change(root)

    support.archive_change(root, "change-a", support.utc_today(), False, True,
                           path_mode=True)

    assert seen == [["--change", "change-a", "--repo", str(root),
                     "--path-mode"]]
    assert recorded == [[str(local / registry.binary), "archive", "change-a",
                         "--yes"]]


def test_the_archive_subcommand_carries_the_escape_and_no_other(support,
                                                                tmp_path):
    """One escape, and it is the entrypoint's. Anything that skipped the pin
    outright would be a bypass invented here."""
    root = str(tmp_path)
    parsed = support.parser().parse_args(
        [root, "archive", "change-a", "--path-mode"])
    assert parsed.path_mode is True
    assert support.parser().parse_args(
        [root, "archive", "change-a"]).path_mode is False
    with pytest.raises(SystemExit):
        support.parser().parse_args([root, "archive", "change-a", "--no-pin"])


# ------------------------------------------- the archive date's ONE clock ----
#
# ISSUE #790. `proposal-support.py archive` took its date from
# `date.today()` — the MACHINE'S LOCAL clock — and handed the pinned CLI an
# environment with no timezone in it, while the CLI names
# `openspec/changes/archive/<YYYY-MM-DD>-<change>/` from ITS OWN local clock and
# has no date option at all. Archiving PR #780's packet at 23:35 local / 03:35
# UTC therefore produced a `2026-09-07-` directory on a UTC 2026-09-08 archive,
# and nothing compared the two. The wrapper now (a) derives the date once in
# UTC and hands the child `TZ=UTC`, and (b) ASSERTS the name the child actually
# produced — because `TZ` is an ask of a process this repository does not own,
# and an ask is not a fact.

#: The instant the defect was found at, as an absolute point in time: 03:35 UTC,
#: which is 16:35 the PREVIOUS DAY at UTC-11. Chosen so the local date and the
#: UTC date differ, which is the whole condition under test.
WHEN = __import__("datetime").datetime(
    2026, 9, 8, 3, 35, tzinfo=__import__("datetime").timezone.utc)
LOCAL_MINUS_ELEVEN = __import__("datetime").timezone(
    __import__("datetime").timedelta(hours=-11))


class _FixedClock:
    """`datetime` with `now()` pinned to `WHEN`, and nothing else changed.

    A FIXED OFFSET rather than a named zone: the property under test is "the
    local date is not the UTC date", which an offset states exactly, and a named
    zone would make the fixture depend on the host carrying a tz database.
    """

    @staticmethod
    def now(tz=None):
        return WHEN.astimezone(tz) if tz is not None else WHEN.astimezone(
            LOCAL_MINUS_ELEVEN)


def _recording_archive_fake(support, calls):
    """A CLI double that RECORDS the child's environment and performs the move."""

    def fake_run(argv, **kwargs):
        argv = [str(item) for item in argv]
        if argv[:1] == ["git"]:
            return _REAL_SUBPROCESS_RUN(argv, **kwargs)
        calls.append((argv, kwargs.get("env")))
        if argv[1:2] == ["archive"] and len(argv) > 2:
            change = argv[2]
            root = Path(kwargs.get("cwd", "."))
            source = root / "openspec" / "changes" / change
            if source.is_dir():
                destination = (root / "openspec" / "changes" / "archive" /
                               f"{support.utc_today()}-{change}")
                destination.parent.mkdir(parents=True, exist_ok=True)
                source.rename(destination)
        return subprocess.CompletedProcess(argv, 0, "", "")

    return fake_run


def test_the_local_date_and_the_UTC_date_REALLY_DIFFER_at_this_instant():
    """ANTI-VACUITY for every test below: at `WHEN` the two dates are two dates.

    Without this the `TZ=UTC` assertions would pass identically against a clock
    that made the distinction unobservable, which is the shape of an assertion
    that proves nothing."""
    assert WHEN.astimezone(LOCAL_MINUS_ELEVEN).date().isoformat() == "2026-09-07"
    assert WHEN.date().isoformat() == "2026-09-08"


def test_the_archive_date_is_the_UTC_date_and_never_the_LOCAL_one(support,
                                                                  monkeypatch):
    """(a) `--date`'s default, and therefore the bundle's `packaged_at`."""
    monkeypatch.setenv("TZ", "Pacific/Niue")
    monkeypatch.setattr(support, "datetime", _FixedClock)
    assert support.utc_today() == "2026-09-08"
    # …and the DEFAULT every dated subcommand takes is that value, not the
    # local 2026-09-07. `package`'s `--date` IS the bundle's `packaged_at`.
    parsed = support.parser().parse_args([".", "package", "change-a"])
    assert parsed.date == "2026-09-08"
    assert support.parser().parse_args(
        [".", "transition", "change-a", "ideation/staging/t"]).date \
        == "2026-09-08"
    # `archive` defaults to None and resolves in `main`, so that "the operator
    # named a date" stays distinguishable from "the operator named nothing".
    assert support.parser().parse_args([".", "archive", "change-a"]).date is None


def test_the_CLI_child_is_handed_TZ_UTC_over_a_NON_UTC_ambient_one(
        support, registry, monkeypatch, tmp_path):
    """(a) The injection, asserted on the ENVIRONMENT THE CHILD ACTUALLY GOT.

    `TZ` is SET over the ambient value rather than defaulted under it: the
    operator's own timezone is exactly the input that produced the defect, so a
    `setdefault` would have changed nothing on the machine it was found on.
    Nothing `validation_environment()` settles is dropped to do it.
    """
    monkeypatch.setenv("TZ", "Pacific/Niue")
    monkeypatch.setattr(support, "datetime", _FixedClock)
    root = tmp_path / "repo"
    a_change(root)
    calls: list = []
    monkeypatch.setattr(support.subprocess, "run",
                        _recording_archive_fake(support, calls))

    support.archive_change(root, "change-a", support.utc_today(), False, True)

    archive_calls = [(argv, env) for argv, env in calls
                     if argv[1:2] == ["archive"]]
    assert len(archive_calls) == 1, calls
    environment = archive_calls[0][1]
    assert environment is not None, "the child was handed no environment at all"
    assert environment["TZ"] == "UTC", environment.get("TZ")
    # nothing the entrypoint settles was dropped to make room for it
    assert environment["OPENSPEC_TELEMETRY"] == "0"
    assert os.environ["TZ"] == "Pacific/Niue", (
        "the ambient TZ is the thing being overridden; if it had leaked away "
        "this test would pass for the wrong reason")
    # and the directory carries the UTC date, not the local one
    assert (root / "openspec" / "changes" / "archive"
            / "2026-09-08-change-a").is_dir()
    assert not (root / "openspec" / "changes" / "archive"
                / "2026-09-07-change-a").exists()


def _wrong_day_fake(support, wrong_day: str, calls: list | None = None):
    """A CLI double that archives to `wrong_day` — an unfixed or ignoring CLI."""

    def fake_run(argv, **kwargs):
        argv = [str(item) for item in argv]
        if argv[:1] == ["git"]:
            return _REAL_SUBPROCESS_RUN(argv, **kwargs)
        if calls is not None:
            calls.append(argv)
        if argv[1:2] == ["archive"] and len(argv) > 2:
            change = argv[2]
            root = Path(kwargs.get("cwd", "."))
            source = root / "openspec" / "changes" / change
            if source.is_dir():
                destination = (root / "openspec" / "changes" / "archive" /
                               f"{wrong_day}-{change}")
                destination.parent.mkdir(parents=True, exist_ok=True)
                source.rename(destination)
                # APPENDED where the file exists, which is what makes the
                # dirty-tree fixture below observable: a whole-file overwrite
                # would erase the operator's edit before the revert decision
                # was ever reached, and the test would then be about the
                # fixture rather than about the revert.
                specs = root / "openspec" / "specs" / "a-capability"
                specs.mkdir(parents=True, exist_ok=True)
                spec = specs / "spec.md"
                previous = (spec.read_text(encoding="utf-8")
                            if spec.is_file() else "# a-capability\n")
                spec.write_text(previous + "the CLI's own spec edit\n",
                                encoding="utf-8")
        return subprocess.CompletedProcess(argv, 0, "", "")

    return fake_run


def test_a_WRONG_DAY_directory_is_REFUSED_and_the_move_REVERTED(
        support, registry, monkeypatch, tmp_path):
    """(b) The assertion, on the only thing that settles it: the name on disk.

    A CLI whose clock is not UTC — or a future CLI that ignores `TZ` — names the
    directory for another day. Nothing may commit that: the refusal names both
    dates, the change directory goes back to its active path, and the exit is 2.
    """
    root = tmp_path / "repo"
    a_change(root)
    monkeypatch.setattr(support.subprocess, "run",
                        _wrong_day_fake(support, "2026-09-07"))

    try:
        support.archive_change(root, "change-a", "2026-09-08", False, True)
    except support.ArchiveDateRefusal as exc:
        message = str(exc)
    else:
        raise AssertionError("a wrong-day archive directory must be refused")

    assert ("the pinned CLI named the archive directory '2026-09-07-change-a' "
            "but the archive date is '2026-09-08'") in message
    assert "the CLI's clock is not UTC; nothing committed" in message
    # THE TREE IS RESTORED: the change is active again and the archive root the
    # CLI created is gone, so a re-run starts from where the operator did.
    assert (root / "openspec" / "changes" / "change-a" / "proposal.md").is_file()
    assert not (root / "openspec" / "changes" / "archive").exists()


def test_the_REFUSAL_reverts_the_CLIs_SPEC_EDITS_when_the_tree_was_clean(
        support, registry, monkeypatch, tmp_path):
    """(b) `git checkout -- openspec/specs`, and ONLY over a clean tree."""
    root = tmp_path / "repo"
    a_change(root)
    specs = root / "openspec" / "specs" / "a-capability"
    specs.mkdir(parents=True)
    (specs / "spec.md").write_text("# a-capability\n\nthe committed text\n",
                                   encoding="utf-8")
    _REAL_SUBPROCESS_RUN(["git", "-C", str(root), "add", "-A"], check=True,
                         capture_output=True, text=True)
    _REAL_SUBPROCESS_RUN(
        ["git", "-C", str(root), "-c", "user.name=Test", "-c",
         "user.email=test@example.invalid", "commit", "-q", "-m", "specs"],
        check=True, capture_output=True, text=True)
    monkeypatch.setattr(support.subprocess, "run",
                        _wrong_day_fake(support, "2026-09-07"))

    try:
        support.archive_change(root, "change-a", "2026-09-08", False, True)
    except support.ArchiveDateRefusal as exc:
        message = str(exc)
    else:
        raise AssertionError("a wrong-day archive directory must be refused")

    assert "git checkout -- openspec/specs" in message
    assert (specs / "spec.md").read_text(encoding="utf-8") \
        == "# a-capability\n\nthe committed text\n"
    assert "the CLI's own spec edit" not in (specs / "spec.md").read_text(
        encoding="utf-8")


def test_the_REFUSAL_LEAVES_a_DIRTY_specs_tree_alone_and_SAYS_SO(
        support, registry, monkeypatch, tmp_path):
    """(b) The revert never discards work this wrapper did not make.

    `git checkout -- openspec/specs` over a tree the operator had already edited
    would destroy their edit while reporting a successful revert. The cleanliness
    is therefore read BEFORE the CLI runs, and a dirty tree is NAMED rather than
    cleaned.
    """
    root = tmp_path / "repo"
    a_change(root)
    specs = root / "openspec" / "specs" / "a-capability"
    specs.mkdir(parents=True)
    (specs / "spec.md").write_text("# a-capability\n\nthe committed text\n",
                                   encoding="utf-8")
    _REAL_SUBPROCESS_RUN(["git", "-C", str(root), "add", "-A"], check=True,
                         capture_output=True, text=True)
    _REAL_SUBPROCESS_RUN(
        ["git", "-C", str(root), "-c", "user.name=Test", "-c",
         "user.email=test@example.invalid", "commit", "-q", "-m", "specs"],
        check=True, capture_output=True, text=True)
    (specs / "spec.md").write_text("# a-capability\n\nthe OPERATOR'S edit\n",
                                   encoding="utf-8")
    monkeypatch.setattr(support.subprocess, "run",
                        _wrong_day_fake(support, "2026-09-07"))

    try:
        support.archive_change(root, "change-a", "2026-09-08", False, True)
    except support.ArchiveDateRefusal as exc:
        message = str(exc)
    else:
        raise AssertionError("a wrong-day archive directory must be refused")

    assert "carried uncommitted changes BEFORE this archive" in message
    left = (specs / "spec.md").read_text(encoding="utf-8")
    assert "the OPERATOR'S edit" in left, (
        "the operator's uncommitted work was discarded by the revert")
    assert "the CLI's own spec edit" in left, (
        "nothing under openspec/specs/ may be reverted over a dirty tree, not "
        "even the CLI's own edit — telling the two apart is what git could not "
        "be asked to do here")


def test_a_CLI_THAT_ARCHIVED_NOTHING_is_refused_rather_than_read_as_success(
        support, registry, monkeypatch, tmp_path):
    """(b) Exit 0 and no directory is not an archive, and is not silence."""
    root = tmp_path / "repo"
    a_change(root)

    def fake_run(argv, **kwargs):
        argv = [str(item) for item in argv]
        if argv[:1] == ["git"]:
            return _REAL_SUBPROCESS_RUN(argv, **kwargs)
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(support.subprocess, "run", fake_run)
    try:
        support.archive_change(root, "change-a", "2026-09-08", False, True)
    except support.ArchiveDateRefusal as exc:
        assert "'<no new directory>'" in str(exc)
    else:
        raise AssertionError("an archive that moved nothing must be refused")


def test_the_WRONG_DAY_REFUSAL_is_EXIT_2_and_NOT_a_traceback(
        support, registry, monkeypatch, tmp_path, capsys):
    """(b) The status a caller branches on, through `main` rather than the API."""
    root = tmp_path / "repo"
    a_change(root)
    monkeypatch.setattr(support.subprocess, "run",
                        _wrong_day_fake(support, "2026-09-07"))
    monkeypatch.setattr(support, "utc_today", lambda: "2026-09-08")
    monkeypatch.setattr(
        sys, "argv",
        ["proposal-support.py", str(root), "archive", "change-a", "--yes"])

    with pytest.raises(SystemExit) as raised:
        support.main()

    assert raised.value.code == 2
    assert "archive-date-mismatch" in capsys.readouterr().err


def test_an_EXPLICIT_DATE_THAT_IS_NOT_UTC_TODAY_is_refused_BEFORE_the_CLI_RUNS(
        support, monkeypatch, tmp_path):
    """(b) The other half: a date the pinned CLI could not honour if it tried.

    Refused BEFORE the pin is resolved and before anything moves — there is no
    `--date` on the CLI to pass it to, so honouring it is not available at any
    price, and stamping it on the bundle beside a differently-named directory is
    the split the whole issue is about.
    """
    root = tmp_path / "repo"
    a_change(root)
    ran: list = []
    monkeypatch.setattr(support.subprocess, "run",
                        lambda argv, **kw: (ran.append([str(i) for i in argv]),
                                            _REAL_SUBPROCESS_RUN(
                                                [str(i) for i in argv], **kw))[1])
    monkeypatch.setattr(
        sys, "argv",
        ["proposal-support.py", str(root), "archive", "change-a", "--yes",
         "--date", "2026-01-01"])

    with pytest.raises(SystemExit) as raised:
        support.main()

    assert raised.value.code == 2
    assert all(argv[:1] == ["git"] for argv in ran), (
        "nothing but the origin gate's own git may run before this refusal")
    assert (root / "openspec" / "changes" / "change-a").is_dir()


def test_the_ARCHIVE_HELP_states_the_UTC_RULE(support, capsys):
    """The rule is DOCUMENTED where an operator meets it — in `--help`."""
    with pytest.raises(SystemExit):
        support.parser().parse_args([".", "archive", "--help"])
    text = " ".join(capsys.readouterr().out.split())
    assert "TODAY IN UTC" in text
    assert "REFUSED" in text
    assert "has no date option" in text
