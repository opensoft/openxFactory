"""`scripts/validate-openspec-cli-pin.py` — the five checks, each pinned by a
test that can only pass if that check runs.

WHY A SYNTHETIC ARTIFACT AND NOT THE REAL PACKAGE. Every refusal here is a
disagreement between a pin and the bytes a registry served, and manufacturing
that disagreement against `@fission-ai/openspec` would mean either persuading npm
to publish different bytes or reaching the network from a test — the first is
impossible and the second is refused by this suite's hermeticity posture. So the
tests write a pin whose recorded content address is the REAL digest of a payload
they hold, and drive the verifier against a fake `npm` installed at the
subprocess boundary. `verify_artifact` therefore does real SHA-512 and SHA-1 work
on real bytes; only the registry is fictional.

THE REAL PACKAGE IS STILL CHECKED, once, and NOT here: the gate
(`.github/workflows/openspec-cli-pin-gate.yml`) fetches
`@fission-ai/openspec@1.2.0` from the registry on every pull request, verifies it
against `contracts/openspec-cli-pin.yaml`, and runs `validate --all --strict`
through it. What THIS suite owns is the refusal vocabulary, the ORDERING — that a
target-less invocation refuses before a registry round trip is spent, and that a
malformed pin is reported as a defect of the pin rather than of the environment —
and the two properties the whole change exists for: that the default mode never
consults PATH, and that a PATH binary at the wrong version is refused rather than
tolerated.
"""
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate-openspec-cli-pin.py"
PIN = ROOT / "contracts" / "openspec-cli-pin.yaml"

VERSION = "1.12.0"
PACKAGE = "@fission-ai/openspec"
INTEGRITY = ("sha512-oFE2Lj7WVSc87nSibk6qe9HjHIOlxhcPAXbPey44DlLvJzBl5+9BZVrN"
             "iozOwv++CQhW+MG0kuP1XLZ/uQrrWw==")
SHASUM = "c844543999f673cdd72445879b86a4abea4c07ef"

# The version this pin was cut at and rolled back to, recorded in the pin's own
# `rollback:` block. It is the WRONG version now, and the PATH-mode tests use it
# as such: an engineer with yesterday's global install is exactly the case the
# version check exists to catch.
ROLLBACK_VERSION = "1.2.0"

PAYLOAD = b"a synthetic tarball standing in for the published artifact"

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _load_module():
    spec = importlib.util.spec_from_file_location("oscli_pin", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return _load_module()


@pytest.fixture(scope="module")
def pin(mod):
    return mod.read_pin(PIN)


def _address(payload: bytes) -> tuple[str, str]:
    return ("sha512-" + base64.b64encode(hashlib.sha512(payload).digest()).decode(),
            hashlib.sha1(payload).hexdigest())


def write_pin(tmp_path: Path, **overrides) -> Path:
    """A well-formed synthetic pin, in the real pin's own grammar.

    Written as TEXT rather than as a dict so the narrow reader is exercised on
    every one of these tests: a fixture that handed `verify` a dict would leave
    the parser — the only thing standing between this tool and a pin file it
    misreads — tested exactly once.
    """
    integrity, shasum = _address(PAYLOAD)
    fields = {
        "schema_version": "1",
        "kind": "pinned_contract_manifest",
        "package": f'"{PACKAGE}"',
        "source_repository": "Fission-AI/OpenSpec",
        "registry": "https://registry.npmjs.org",
        "version": f'"{VERSION}"',
        "revision_kind": "package_integrity",
        "integrity_algorithm": "sha512",
        "integrity": f'"{integrity}"',
        "shasum": f'"{shasum}"',
        "binary": "openspec",
        "verify_pin": "scripts/validate-openspec-cli-pin.py",
        "consumer_entrypoint": "scripts/validate-openspec-cli-pin.py",
    }
    dispositions = overrides.pop("dispositions_block", None)
    fields.update({k: v for k, v in overrides.items() if v is not None})
    for key, value in overrides.items():
        if value is None:
            fields.pop(key, None)
    path = tmp_path / "pin.yaml"
    path.write_text(
        "# a synthetic pin\n"
        + "".join(f"{key}: {value}\n" for key, value in fields.items())
        + (dispositions or ""),
        encoding="utf-8")
    return path


# --------------------------------------------------- the disposition fixtures

# A synthetic finding in the SHAPE 1.12.0 actually emits, checked against the
# captured fixtures below rather than invented: `id` / `type` / `valid` /
# `issues[{level, path, message}]`, with `summary.totals`.
FINDING_ITEM = "add-example-change"
FINDING_PATH = "example-capability/spec.md"
FINDING_TEXT = (
    'MODIFIED "Composed views are read-only with a repository jump" omits '
    'scenario(s) the current spec still has: "Gate verbs hide on a composed '
    'view". Copy them into the MODIFIED block (a MODIFIED requirement replaces '
    'the whole block, so archive refuses to drop them).')


def report(*errors: tuple[str, str, str], items: int = 3,
           infos: int = 1, key: str = "items") -> str:
    """A `--json` document in the pinned CLI's own shape."""
    rows = [{"id": item, "type": "change", "valid": False,
             "issues": [{"level": "ERROR", "path": path, "message": message}],
             "durationMs": 9}
            for item, path, message in errors]
    for index in range(infos):
        rows.append({"id": f"spec-{index}", "type": "spec", "valid": True,
                     "issues": [{"level": "INFO",
                                 "path": f"requirements[{index}]",
                                 "message": "Requirement text is very long "
                                            "(>500 characters). Consider "
                                            "breaking it down."}],
                     "durationMs": 2})
    failed = len(errors)
    return json.dumps({
        key: rows,
        "summary": {"totals": {"items": items, "passed": items - failed,
                               "failed": failed}},
        "version": "1.0",
        "root": {"path": "/somewhere", "source": "nearest"}})


def disposition_block(*entries: dict) -> str:
    """Render `dispositions:` in the pin's own grammar, folded scalars included."""
    lines = ["dispositions:"]
    for entry in entries:
        first = True
        for key in ("repo", "item", "path", "level", "finding", "why",
                    "ratified_by", "recorded_by"):
            if key not in entry:
                continue
            lead = "  - " if first else "    "
            first = False
            lines.append(f"{lead}{key}: '" + str(entry[key]).replace("'", "''")
                         + "'")
        if "cited_to" in entry:
            lead = "  - " if first else "    "
            first = False
            lines.append(f"{lead}cited_to:")
            for citation in entry["cited_to"]:
                lines.append(f"      - {citation}")
    return "\n".join(lines) + "\n"


def a_disposition(**overrides) -> dict:
    entry = {
        "repo": "openxFactory",
        "item": FINDING_ITEM,
        "path": FINDING_PATH,
        "level": "ERROR",
        "finding": FINDING_TEXT,
        "why": "the omission is a declared narrowing, not a dropped scenario",
        "cited_to": ["openspec/specs/doc-health/spec.md:1770",
                     "council LA-A1"],
        "ratified_by": 'Brett Heap, 2026-09-05, "take exit 2"',
    }
    entry.update(overrides)
    return {key: value for key, value in entry.items() if value is not None}


@pytest.fixture
def fake_npm(mod, monkeypatch):
    """Install a fictional registry at the SUBPROCESS boundary.

    Everything above the boundary is the real code under test: the real
    `fetch_artifact` shells out, the real `verify_artifact` hashes real bytes,
    the real `install_artifact` looks for a real executable path. Only what
    `npm` and the CLI would have done is supplied here, and the calls are
    RECORDED so a test can assert not merely that a run passed but WHAT it ran —
    which is how `--path-mode` is proved never to be reached by the default.
    """
    calls: list[list[str]] = []
    served = {"payload": PAYLOAD, "reports": VERSION, "verdict": 0,
              "report": report(), "origin": "git@github.com:opensoft/openxFactory.git"}

    def fake_run(argv, **kwargs):
        calls.append([str(a) for a in argv])
        if argv[0] == "git":
            # `repository_identity` goes through `_run` like every other
            # subprocess, so the fictional registry supplies a fictional origin
            # too. The URL-to-name reduction under test is the real one.
            return subprocess.CompletedProcess(argv, 0, served["origin"], "")
        if argv[1:2] == ["pack"]:
            destination = Path(argv[argv.index("--pack-destination") + 1])
            destination.mkdir(parents=True, exist_ok=True)
            (destination / f"fission-ai-openspec-{VERSION}.tgz").write_bytes(
                served["payload"])
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[1:2] == ["install"]:
            prefix = Path(argv[argv.index("--prefix") + 1])
            (prefix / "bin").mkdir(parents=True, exist_ok=True)
            (prefix / "bin" / "openspec").write_text("#!/bin/sh\n", encoding="utf-8")
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[1:2] == ["--version"]:
            return subprocess.CompletedProcess(argv, 0, served["reports"] + "\n", "")
        return subprocess.CompletedProcess(argv, 0, "", "")

    def fake_stream(argv, **kwargs):
        calls.append([str(a) for a in argv])
        if "--json" in argv:
            return subprocess.CompletedProcess(argv, served["verdict"],
                                               served["report"], "")
        return subprocess.CompletedProcess(argv, served["verdict"])

    monkeypatch.setattr(mod, "_run", fake_run)
    monkeypatch.setattr(mod.subprocess, "run", fake_stream)
    monkeypatch.setattr(mod.shutil, "which",
                        lambda name: f"/usr/bin/{name}" if name == "npm" else None)
    return calls, served


# ------------------------------------------------------- reading the pin ----

def test_the_real_pin_parses_into_the_expected_shape(pin):
    assert pin["kind"] == "pinned_contract_manifest"
    assert pin["package"] == PACKAGE
    assert pin["version"] == VERSION
    assert pin["revision_kind"] == "package_integrity"
    assert pin["integrity"] == INTEGRITY
    assert pin["shasum"] == SHASUM
    assert pin["binary"] == "openspec"


def test_the_real_pin_names_this_file_as_the_one_entrypoint(pin):
    """The consumer obligation is IN the pin, not only in the prose that
    proposed it: a repository reading the pin must be able to learn from the pin
    itself which command it is obliged to run."""
    assert pin["verify_pin"] == "scripts/validate-openspec-cli-pin.py"
    assert pin["consumer_entrypoint"] == "scripts/validate-openspec-cli-pin.py"


def test_the_recorded_integrity_decodes_to_a_full_sha512(pin):
    raw = base64.b64decode(pin["integrity"][len("sha512-"):], validate=True)
    assert len(raw) == 64


def test_the_reader_refuses_a_line_outside_its_grammar(mod, tmp_path):
    bad = tmp_path / "pin.yaml"
    bad.write_text("version: 1.2.0\n\tnot: yaml\n", encoding="utf-8")
    with pytest.raises(mod.PinRefusal) as exc:
        mod.read_pin(bad)
    assert exc.value.code == "pin-unreadable"


def test_an_absent_pin_is_unreadable_and_not_an_unpinned_pass(mod, tmp_path):
    with pytest.raises(mod.PinRefusal) as exc:
        mod.read_pin(tmp_path / "nope.yaml")
    assert exc.value.code == "pin-unreadable"


# ------------------------------------------------------------- check 1 ------

@pytest.mark.parametrize("mutation, detail", [
    ({"revision_kind": "commit"}, "a source-tree referent is not this product's"),
    ({"revision_kind": "version"}, "a version name is not a content address"),
    ({"version": '"^1.2.0"'}, "a caret range is not a pin"),
    ({"version": '"latest"'}, "a dist-tag is movable by the publisher"),
    ({"version": '"1.2"'}, "a partial version resolves to a range"),
    ({"version": '"1.x"'}, "an x-range is a range"),
])
def test_a_movable_referent_is_refused_as_tag_only(mod, tmp_path, mutation, detail):
    with pytest.raises(mod.PinRefusal) as exc:
        mod.pinned_version(mod.read_pin(write_pin(tmp_path, **mutation)))
    assert exc.value.code == "pin-tag-only", detail


@pytest.mark.parametrize("mutation, detail", [
    ({"integrity": None}, "a version with no content address beside it"),
    ({"integrity": '"sha1-abcdef"'}, "the wrong algorithm is not the referent"),
    ({"integrity": '"sha512-tooshort=="'}, "a truncated address addresses nothing"),
    ({"shasum": None}, "a declared field nothing verifies drifts unnoticed"),
    ({"shasum": '"not-hex"'}, "an unusable legacy address is a defect"),
])
def test_a_pin_without_a_usable_content_address_is_refused(
        mod, tmp_path, mutation, detail):
    with pytest.raises(mod.PinRefusal) as exc:
        mod.pinned_integrity(mod.read_pin(write_pin(tmp_path, **mutation)))
    assert exc.value.code == "pin-tag-only", detail


def test_the_shape_guard_runs_before_anything_is_fetched(mod, tmp_path, fake_npm):
    """Ordering, and it is why `pinned_version` is called before any resolver.

    A pin recording `latest` that reached the fetch would be reported as an
    environment problem — a code that says the registry is wrong about a pin that
    is itself the thing that is wrong.
    """
    calls, _ = fake_npm
    bad = write_pin(tmp_path, version='"latest"')
    assert mod.main(["--all", "--pin", str(bad)]) == 2
    assert calls == [], "a malformed pin must not spend a registry round trip"


# ------------------------------------------------------------- check 2 ------

def test_no_scan_target_refuses_rather_than_self_testing(mod, tmp_path, fake_npm):
    calls, _ = fake_npm
    assert mod.main(["--pin", str(write_pin(tmp_path))]) == 2
    assert calls == [], "the refusal must arrive before any expensive work"


def test_the_refusal_for_no_target_is_named_and_not_a_generic_failure(
        mod, tmp_path):
    parser = mod.build_parser()
    with pytest.raises(mod.PinRefusal) as exc:
        mod.validation_targets(parser.parse_args([]))
    assert exc.value.code == "pin-no-target"


def test_all_and_change_together_state_two_targets_and_decide_neither(mod):
    parser = mod.build_parser()
    with pytest.raises(mod.PinRefusal) as exc:
        mod.validation_targets(parser.parse_args(["--all", "--change", "x"]))
    assert exc.value.code == "pin-no-target"


def test_a_named_change_becomes_a_strict_invocation(mod):
    parser = mod.build_parser()
    targets = mod.validation_targets(
        parser.parse_args(["--change", "add-openspec-cli-pin"]))
    assert targets == [["validate", "add-openspec-cli-pin", "--strict"]]


def test_strict_is_always_on_and_cannot_be_dropped(mod):
    """`--strict` is accepted as a no-op and there is no `--no-strict`: a
    non-strict pass is not the act this pin governs."""
    parser = mod.build_parser()
    assert mod.validation_targets(parser.parse_args(["--all"])) == [
        ["validate", "--all", "--strict"]]
    assert mod.validation_targets(parser.parse_args(["--all", "--strict"])) == [
        ["validate", "--all", "--strict"]]
    with pytest.raises(SystemExit):
        parser.parse_args(["--all", "--no-strict"])


def test_a_tree_with_no_openspec_directory_is_not_a_governed_surface(
        mod, tmp_path):
    with pytest.raises(mod.PinRefusal) as exc:
        mod.run_validation(Path("/bin/true"), tmp_path,
                           [["validate", "--all", "--strict"]])
    assert exc.value.code == "pin-no-target"


# ------------------------------------------------------------- check 3 ------

def test_a_conformant_artifact_verifies(mod, tmp_path):
    integrity, shasum = _address(PAYLOAD)
    artifact = tmp_path / "pkg.tgz"
    artifact.write_bytes(PAYLOAD)
    mod.verify_artifact(artifact, integrity, shasum)


def test_bytes_that_are_not_the_pinned_bytes_refuse(mod, tmp_path):
    integrity, shasum = _address(PAYLOAD)
    artifact = tmp_path / "pkg.tgz"
    artifact.write_bytes(PAYLOAD + b"!")
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify_artifact(artifact, integrity, shasum)
    assert exc.value.code == "pin-integrity-mismatch"
    assert "INTEGRITY DRIFT" in exc.value.detail


def test_a_registry_serving_the_wrong_artifact_is_refused_end_to_end(
        mod, tmp_path, fake_npm):
    """The property the whole pin exists for: the version label matched and the
    bytes did not, and the run refused."""
    calls, served = fake_npm
    served["payload"] = b"different bytes published under the same version"
    (tmp_path / "openspec").mkdir()
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(write_pin(tmp_path))]) == 2
    assert any(call[1:2] == ["pack"] for call in calls)
    assert not any(call[1:2] == ["install"] for call in calls), \
        "nothing may be installed from bytes that failed their content address"


def test_the_legacy_address_is_checked_and_not_merely_recorded(mod, tmp_path):
    integrity, _ = _address(PAYLOAD)
    artifact = tmp_path / "pkg.tgz"
    artifact.write_bytes(PAYLOAD)
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify_artifact(artifact, integrity, "0" * 40)
    assert exc.value.code == "pin-integrity-mismatch"
    assert "SHASUM DRIFT" in exc.value.detail


# ------------------------------------------------------------- check 4 ------

def test_a_path_binary_at_the_wrong_version_is_refused_with_a_remedy(
        mod, tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "_run", lambda argv, **kw: subprocess.CompletedProcess(
        argv, 0, ROLLBACK_VERSION + "\n", ""))
    with pytest.raises(mod.PinRefusal) as exc:
        mod.assert_reported_version(Path("/usr/bin/openspec"), VERSION)
    assert exc.value.code == "pin-version-mismatch"
    assert ROLLBACK_VERSION in exc.value.detail
    assert "Remediation:" in str(exc.value)


def test_path_mode_refuses_the_wrong_version_end_to_end(
        mod, tmp_path, fake_npm, monkeypatch):
    calls, served = fake_npm
    served["reports"] = ROLLBACK_VERSION
    monkeypatch.setattr(mod.shutil, "which",
                        lambda name: f"/usr/bin/{name}")
    (tmp_path / "openspec").mkdir()
    assert mod.main(["--all", "--path-mode", "--repo", str(tmp_path),
                     "--pin", str(write_pin(tmp_path))]) == 2


def test_the_default_mode_never_consults_path(mod, tmp_path, fake_npm,
                                              monkeypatch):
    """THE POINT OF THE CHANGE, asserted positively.

    A wrong-version `openspec` is placed on PATH and the run still passes,
    because the default mode resolves the executable it installed and never asks
    a shell to find one. If this test ever fails, a gate has become sensitive to
    what an engineer happens to have installed.
    """
    calls, _ = fake_npm
    seen: list[str] = []

    def watching_which(name):
        seen.append(name)
        return f"/usr/bin/{name}"

    monkeypatch.setattr(mod.shutil, "which", watching_which)
    (tmp_path / "openspec").mkdir()
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(write_pin(tmp_path))]) == 0
    assert seen == ["npm"], f"PATH was consulted for {seen}"
    assert not any(call[0] == "openspec" for call in calls)


# ------------------------------------------------------------- check 5 ------

def test_the_happy_path_runs_the_pinned_binary_against_the_named_repository(
        mod, tmp_path, fake_npm):
    calls, _ = fake_npm
    (tmp_path / "openspec").mkdir()
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(write_pin(tmp_path))]) == 0
    invocation = [call for call in calls
                  if call[1:] == ["validate", "--all", "--strict"]]
    assert len(invocation) == 1, calls
    assert invocation[0][0].endswith("/bin/openspec")


def test_a_failing_validation_is_exit_one_and_not_a_pin_refusal(
        mod, tmp_path, fake_npm):
    """The distinction the sibling verifiers do not need. `2` says the pin could
    not be trusted; `1` says the pin held and the deltas are invalid. The two
    have completely different remedies, and collapsing them would hide the
    ordinary finding inside the extraordinary one."""
    calls, served = fake_npm
    served["verdict"] = 1
    (tmp_path / "openspec").mkdir()
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(write_pin(tmp_path))]) == 1


def test_every_target_runs_and_the_worst_verdict_wins(mod, tmp_path, fake_npm,
                                                      monkeypatch):
    calls, _ = fake_npm
    verdicts = iter([0, 1, 0])
    monkeypatch.setattr(
        mod.subprocess, "run",
        lambda argv, **kw: (calls.append([str(a) for a in argv]),
                            subprocess.CompletedProcess(argv, next(verdicts)))[1])
    (tmp_path / "openspec").mkdir()
    assert mod.main(["--change", "a", "--change", "b", "--change", "c",
                     "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(write_pin(tmp_path))]) == 1
    ran = [call for call in calls if call[1:2] == ["validate"]]
    assert [call[2] for call in ran] == ["a", "b", "c"]


# ------------------------------------------- resolution and the CLI shape ----

def test_an_absent_npm_refuses_rather_than_falling_back_to_path(
        mod, tmp_path, monkeypatch):
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
    with pytest.raises(mod.PinRefusal) as exc:
        mod.fetch_artifact(PACKAGE, VERSION, tmp_path / "fetch")
    assert exc.value.code == "pin-unresolvable"


def test_the_install_never_runs_lifecycle_scripts(mod, tmp_path, fake_npm):
    """The mitigation for the pin's declared shortfall: the artifact's own bytes
    are pinned, its nine caret-ranged dependencies are not, and a dependency's
    install script must not get to run inside a gate."""
    calls, _ = fake_npm
    (tmp_path / "openspec").mkdir()
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(write_pin(tmp_path))]) == 0
    install = [call for call in calls if call[1:2] == ["install"]][0]
    assert "--ignore-scripts" in install


def test_a_cache_hit_still_reverifies_the_artifact(mod, tmp_path, fake_npm):
    """Only the INSTALL is reused. The bytes are hashed on every run, so no run
    ever inherits a previous run's verdict about what the registry served."""
    calls, _ = fake_npm
    (tmp_path / "openspec").mkdir()
    cache = tmp_path / "cache"
    argv = ["--all", "--cache-dir", str(cache), "--repo", str(tmp_path),
            "--pin", str(write_pin(tmp_path))]
    assert mod.main(argv) == 0
    first = len([call for call in calls if call[1:2] == ["install"]])
    assert mod.main(argv) == 0
    assert len([call for call in calls if call[1:2] == ["install"]]) == first
    assert len([call for call in calls if call[1:2] == ["pack"]]) == 2


def test_a_cache_stamped_for_other_bytes_is_rebuilt(mod, tmp_path, fake_npm):
    calls, _ = fake_npm
    (tmp_path / "openspec").mkdir()
    cache = tmp_path / "cache"
    argv = ["--all", "--cache-dir", str(cache), "--repo", str(tmp_path),
            "--pin", str(write_pin(tmp_path))]
    assert mod.main(argv) == 0
    stamp = next(cache.glob("*/.pin-verified"))
    stamp.write_text("sha512-somethingelse\n", encoding="utf-8")
    assert mod.main(argv) == 0
    assert len([call for call in calls if call[1:2] == ["install"]]) == 2


def test_there_is_no_verify_only_mode(mod):
    """A flag that verifies the pin and validates nothing is exactly the
    target-less green check `neutral-product-pin` forbids."""
    with pytest.raises(SystemExit):
        mod.build_parser().parse_args(["--verify-only"])


def test_every_refusal_carries_the_remediation_trailer(mod):
    message = str(mod.PinRefusal("pin-tag-only", "detail"))
    assert message.startswith("REFUSE pin-tag-only: detail")
    assert "Remediation:" in message
    assert "never edit an integrity value to make this pass" in message
    assert "HUMAN-ONLY governed change" in message


def test_the_refusal_vocabulary_is_exactly_what_the_code_raises(mod):
    """A refusal reporting the right fact under a new name is a refusal nothing
    downstream recognizes."""
    assert mod.REFUSAL_CODES == (
        "pin-tag-only",
        "pin-no-target",
        "pin-unresolvable",
        "pin-integrity-mismatch",
        "pin-version-mismatch",
        "pin-disposition-malformed",
        "pin-disposition-stale",
        "pin-report-unreadable",
        "pin-repo-unidentified",
    )
    assert "pin-unreadable" not in mod.REFUSAL_CODES


def test_the_gate_workflow_reads_the_pin_and_carries_no_fourth_copy():
    """The precedent's argument: a workflow that hard-coded the version would be
    another copy of the pin, and copies of a pin move separately."""
    workflow = (ROOT / ".github" / "workflows"
                / "openspec-cli-pin-gate.yml").read_text(encoding="utf-8")
    assert "validate-openspec-cli-pin.py" in workflow
    assert "--all" in workflow
    body = "\n".join(line for line in workflow.splitlines()
                     if not line.lstrip().startswith("#"))
    assert VERSION not in body, \
        "the gate must read the version out of the pin, never restate it"
    assert INTEGRITY not in body


# ------------------------------------------------------------- check 6 ------
# DISPOSITIONS. The mechanism this pin bump adds, and the reason it needed one:
# 1.12.0's scenario-currency check is blind to this estate's reserved narrowing
# marker and re-reports two ratified decisions as ERRORs. Brett Heap ruled on
# 2026-09-05, "take exit 2" — carry a dispositioned exception. What follows pins
# the properties that make that a governed act rather than a mute list: a
# citation is mandatory, scope is per repository, and an exception that outlives
# its condition REFUSES.


def test_the_real_pin_declares_exactly_the_two_dispositions_the_bump_carries(
        mod, pin):
    """The pin's own entries, read through the pin's own reader.

    Asserted against the REAL file because the two entries are the substance of
    the change: a bump that silently grew a third exception would still be a
    bump nobody read.
    """
    entries = mod.pinned_dispositions(pin)
    assert [entry["item"] for entry in entries] == [
        "add-chain-attestation", "add-composed-view-authoring"]
    assert {entry["repo"] for entry in entries} == {"openxFactory"}
    assert [entry["path"] for entry in entries] == [
        "signed-execution-chain/spec.md", "ideation-dashboard/spec.md"]


def test_every_real_disposition_cites_canon_and_names_who_granted_it(mod, pin):
    """The property that separates an accepted exception from a suppression."""
    for entry in mod.pinned_dispositions(pin):
        assert entry["cited_to"], entry["item"]
        assert any("doc-health/spec.md" in citation
                   for citation in entry["cited_to"]), \
            f"{entry['item']} does not cite the promoted marker requirement"
        assert any("openspec-1.12-readiness-2026-09-05.md" in citation
                   for citation in entry["cited_to"]), \
            f"{entry['item']} does not cite the measurement it rests on"
        assert entry["ratified_by"].startswith("Brett Heap, 2026-09-05")
        assert entry["why"].strip()
        assert entry["retires_when"].strip()


def test_the_real_pin_records_the_previous_referent_as_the_rollback(pin):
    """A rollback written in the grammar rather than in prose: the four fields
    move together or the pin names bytes it did not pin."""
    rollback = pin["rollback"]
    assert len(rollback) == 1
    assert rollback[0]["version"] == ROLLBACK_VERSION
    assert rollback[0]["integrity"].startswith("sha512-2XDmPZ")
    assert rollback[0]["shasum"] == "0fd5333520c8846f0ac51727379b8812e2f13c1b"
    assert ROLLBACK_VERSION in rollback[0]["tarball"]


# ------------------------------------------------- the grammar the pin gained

def test_the_reader_folds_a_folded_scalar_into_one_line(mod, tmp_path):
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition()))
    entry = mod.read_pin(path)["dispositions"][0]
    assert "\n" not in entry["why"]
    assert entry["why"].endswith("dropped scenario")


def test_the_reader_reads_a_nested_citation_list(mod, tmp_path):
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition(cited_to=["one", "two", "three"])))
    assert mod.read_pin(path)["dispositions"][0]["cited_to"] == [
        "one", "two", "three"]


def test_a_block_form_the_reader_does_not_implement_is_unreadable(
        mod, tmp_path):
    """`|` is refused rather than guessed at. Its whitespace semantics differ
    from `>-`, and a reader that guessed between them would be guessing at the
    content of a citation."""
    path = write_pin(tmp_path, dispositions_block=(
        "dispositions:\n  - repo: openxFactory\n    why: |\n"
        "      a literal block\n"))
    with pytest.raises(mod.PinRefusal) as exc:
        mod.read_pin(path)
    assert exc.value.code == "pin-unreadable"


# ------------------------------------------------- the shape of a disposition

def test_an_absent_disposition_list_is_the_same_fact_as_an_empty_one(
        mod, tmp_path):
    assert mod.pinned_dispositions(mod.read_pin(write_pin(tmp_path))) == []
    path = write_pin(tmp_path, dispositions_block="dispositions:\n")
    assert mod.pinned_dispositions(mod.read_pin(path)) == []


@pytest.mark.parametrize("mutation, detail", [
    ({"cited_to": None}, "an exception with no citation is an uncited one"),
    ({"cited_to": []}, "an empty citation list is not 'none needed'"),
    ({"ratified_by": None}, "an exception nobody granted"),
    ({"repo": None}, "an unscoped exception could suppress another tree"),
    ({"item": None}, "an exception that names no item matches by accident"),
    ({"path": None}, "one change can carry several findings"),
    ({"finding": None}, "the finding text is the thing being accepted"),
    ({"why": None}, "a reason nobody wrote is a reason nobody reviewed"),
])
def test_a_disposition_missing_what_makes_it_reviewable_is_refused(
        mod, tmp_path, mutation, detail):
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition(**mutation)))
    with pytest.raises(mod.PinRefusal) as exc:
        mod.pinned_dispositions(mod.read_pin(path))
    assert exc.value.code == "pin-disposition-malformed", detail
    assert "Remediation:" in str(exc.value)


def test_recorded_by_satisfies_the_authority_requirement(mod, tmp_path):
    """The weaker of the two spellings is still an authority: a lane may RECORD
    a human ruling where it cannot itself RATIFY one."""
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition(ratified_by=None,
                      recorded_by="lane codexfactory-0d, 2026-09-05")))
    assert len(mod.pinned_dispositions(mod.read_pin(path))) == 1


def test_two_dispositions_over_one_finding_are_refused(mod, tmp_path,
                                                       fake_npm):
    """The redundant one would look satisfied while doing no work, and would
    then never go stale — a permanent suppression hiding behind a live one."""
    calls, served = fake_npm
    served["report"] = report((FINDING_ITEM, FINDING_PATH, FINDING_TEXT))
    (tmp_path / "openspec").mkdir()
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition(), a_disposition(why="a second reading of the same one")))
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 2


# ------------------------------------------------------- reading the verdict

def test_the_captured_bulk_report_parses_into_the_two_real_findings(mod):
    """THE REAL BYTES, captured from `@fission-ai/openspec@1.12.0` on this
    corpus (`validate --changes --strict --json --report findings`) rather than
    a shape invented to match the parser. Its array key is `itemFindings`, which
    is the variant `--report` produces and the one a hand-written fixture would
    most plausibly have got wrong."""
    payload = (FIXTURES /
               "openspec-1.12.0-validate-changes-strict-report-findings.json"
               ).read_text(encoding="utf-8")
    items, totals = mod.parse_report(payload, ["validate", "--changes"])
    assert totals == {"items": 31, "passed": 29, "failed": 2}
    findings = mod.collect_findings(items, "--changes")
    blocking = [row for row in findings if row["blocking"]]
    assert [(row["item"], row["path"]) for row in blocking] == [
        ("add-chain-attestation", "signed-execution-chain/spec.md"),
        ("add-composed-view-authoring", "ideation-dashboard/spec.md")]
    assert all("omits scenario(s) the current spec still has" in row["message"]
               for row in blocking)
    assert any(row["level"] == "INFO" for row in findings), \
        "the fixture must carry the non-blocking levels too, or the filter is untested"


def test_the_captured_single_item_report_parses_under_the_other_array_key(mod):
    """`items` rather than `itemFindings`, which is what a single-target run and
    a bulk run WITHOUT `--report` both emit. Both keys are accepted because both
    are produced by the pinned tool."""
    payload = (FIXTURES /
               "openspec-1.12.0-validate-one-change-strict.json"
               ).read_text(encoding="utf-8")
    items, totals = mod.parse_report(payload, ["validate", "add-chain-attestation"])
    assert totals == {"items": 1, "passed": 0, "failed": 1}
    blocking = [row for row in mod.collect_findings(items, "one")
                if row["blocking"]]
    assert len(blocking) == 1
    assert blocking[0]["item"] == "add-chain-attestation"


def test_the_real_pin_disposes_exactly_the_captured_findings(mod, pin):
    """THE PIN AND THE MEASUREMENT ARE CHECKED AGAINST EACH OTHER, here, offline.

    The two `finding:` values in `contracts/openspec-cli-pin.yaml` are quoted
    from the tool's own report; this reconciles them against the CAPTURED bytes
    of that report. A transcription slip in either — a smart quote, a dropped
    clause — shows up as an undispositioned finding plus a stale disposition on
    a developer's machine rather than as a red gate.
    """
    payload = (FIXTURES /
               "openspec-1.12.0-validate-changes-strict-report-findings.json"
               ).read_text(encoding="utf-8")
    items, _ = mod.parse_report(payload, ["validate", "--changes"])
    findings = mod.collect_findings(items, "--changes")
    applied, undispositioned, stale = mod.reconcile(
        findings, mod.pinned_dispositions(pin), "openxFactory")
    assert len(applied) == 2
    assert undispositioned == []
    assert stale == []


def test_an_unparseable_verdict_refuses_rather_than_degrading(mod):
    with pytest.raises(mod.PinRefusal) as exc:
        mod.parse_report("openspec: something went wrong", ["validate", "--all"])
    assert exc.value.code == "pin-report-unreadable"


def test_a_leading_banner_is_tolerated_and_nothing_else_is(mod):
    items, totals = mod.parse_report(
        "npm notice a banner\n" + report(), ["validate", "--all"])
    assert totals["items"] == 3
    with pytest.raises(mod.PinRefusal):
        mod.parse_report("[1, 2, 3]", ["validate", "--all"])


def test_a_report_carrying_no_recognized_array_refuses(mod):
    with pytest.raises(mod.PinRefusal) as exc:
        mod.parse_report(json.dumps({"summary": {}}), ["validate", "--all"])
    assert exc.value.code == "pin-report-unreadable"


def test_an_item_marked_invalid_with_no_error_still_produces_a_finding(mod):
    """The two facts move together in every measured run. If they ever part,
    this tool reports the failure rather than losing it."""
    payload = json.dumps({"items": [{"id": "x", "type": "change",
                                     "valid": False, "issues": []}],
                          "summary": {"totals": {"items": 1, "passed": 0,
                                                 "failed": 1}}})
    items, _ = mod.parse_report(payload, ["validate", "--all"])
    blocking = [row for row in mod.collect_findings(items, "--all")
                if row["blocking"]]
    assert len(blocking) == 1
    assert "INVALID" in blocking[0]["message"]


def test_a_failing_exit_whose_report_names_no_error_refuses(mod, tmp_path,
                                                            fake_npm):
    """A failure the report does not carry would be silently dispositioned away,
    because reconciliation reads the REPORT and not the exit code."""
    calls, served = fake_npm
    served["verdict"] = 1
    served["report"] = report()          # INFO only, no ERROR
    (tmp_path / "openspec").mkdir()
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition()))
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 2


# ------------------------------------------------------------ repository scope

def test_repository_identity_is_read_from_the_real_git_remote(mod, tmp_path):
    """A REAL git repository, not the fictional one the other tests use.

    The directory is deliberately named for a branch, the way every worktree in
    this estate is, so a basename rule would fail this test — which is the whole
    reason the identity is read from the remote.
    """
    worktree = tmp_path / "change-some-branch-name"
    worktree.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=worktree, check=True)
    subprocess.run(["git", "remote", "add", "origin",
                    "git@github.com:opensoft/openxFactory.git"],
                   cwd=worktree, check=True)
    assert mod.repository_identity(worktree) == "openxFactory"


def test_an_https_remote_resolves_to_the_same_name(mod, tmp_path):
    worktree = tmp_path / "wt"
    worktree.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=worktree, check=True)
    subprocess.run(["git", "remote", "add", "origin",
                    "https://github.com/opensoft/OpsxFactory.git"],
                   cwd=worktree, check=True)
    assert mod.repository_identity(worktree) == "OpsxFactory"


def test_a_tree_with_no_origin_refuses_when_dispositions_are_declared(
        mod, tmp_path):
    worktree = tmp_path / "wt"
    worktree.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=worktree, check=True)
    with pytest.raises(mod.PinRefusal) as exc:
        mod.repository_identity(worktree)
    assert exc.value.code == "pin-repo-unidentified"


def test_a_disposition_for_another_repository_is_neither_applied_nor_stale(
        mod, tmp_path, fake_npm, capsys):
    """THE PROPERTY A CONSUMING REPOSITORY DEPENDS ON.

    OpsxFactory runs `--all --strict` through this same entrypoint and this same
    pin file. `add-chain-attestation` is absent from its corpus because it was
    never in it — which must NOT be read as an exception gone stale, or every
    consuming repository in the estate would refuse on openxFactory's private
    exceptions.
    """
    calls, served = fake_npm
    served["origin"] = "git@github.com:opensoft/OpsxFactory.git"
    served["report"] = report(items=47, infos=1)
    (tmp_path / "openspec").mkdir()
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition()))
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 0
    printed = capsys.readouterr().out
    assert "DISPOSITIONED FINDINGS" not in printed
    assert "validated --strict clean" in printed


# --------------------------------------------------------- the four verdicts

def test_two_dispositions_cover_two_findings_and_the_run_passes_saying_so(
        mod, tmp_path, fake_npm, capsys):
    """THE ACT THIS BUMP EXISTS FOR, end to end — and the pass is not silent.

    A run that suppresses two ERROR-level findings and prints only `OK` has told
    its reader something false by omission. The exception, its reason, its
    citations and the human who granted it are printed BY NAME on every run.
    """
    calls, served = fake_npm
    second = ("add-other-change", "other-capability/spec.md",
              "MODIFIED \"Another requirement\" omits scenario(s) the current "
              "spec still has: \"a second one\".")
    served["verdict"] = 1                       # the CLI fails over both
    served["report"] = report((FINDING_ITEM, FINDING_PATH, FINDING_TEXT),
                              second, items=90)
    (tmp_path / "openspec").mkdir()
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition(),
        a_disposition(item=second[0], path=second[1], finding=second[2],
                      why="the second declared narrowing")))
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 0
    printed = capsys.readouterr().out
    assert "Totals: 88 passed, 2 failed (90 items)" in printed
    assert "DISPOSITIONED FINDINGS in openxFactory (2 applied)" in printed
    assert FINDING_ITEM in printed and second[0] in printed
    assert "openspec/specs/doc-health/spec.md:1770" in printed
    assert 'Brett Heap, 2026-09-05, "take exit 2"' in printed
    assert "THIS IS NOT A CLEAN TREE" in printed
    invocation = [call for call in calls
                  if call[1:] == ["validate", "--all", "--strict", "--json"]]
    assert len(invocation) == 1, calls


def test_an_undispositioned_finding_fails_and_the_failure_names_its_remedy(
        mod, tmp_path, fake_npm, capsys):
    """Exit 1, not 2: the pin held and this is a finding about the deltas."""
    calls, served = fake_npm
    served["verdict"] = 1
    served["report"] = report((FINDING_ITEM, FINDING_PATH, FINDING_TEXT),
                              ("add-unread-change", "some/spec.md",
                               "a finding nobody has looked at"),
                              items=90)
    (tmp_path / "openspec").mkdir()
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition()))
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 1
    captured = capsys.readouterr()
    assert "add-unread-change" in captured.err
    assert "FIX IT, or DISPOSITION IT" in captured.err
    assert "cited_to" in captured.err and "ratified_by" in captured.err
    assert "add-example-change" not in captured.err, \
        "a dispositioned finding must not be re-reported as a failure"


def test_a_stale_disposition_refuses_so_an_exception_cannot_outlive_its_cause(
        mod, tmp_path, fake_npm, capsys):
    """THE ASYMMETRY, pinned.

    The same pin, the same repository, and a corpus in which the dispositioned
    finding NO LONGER OCCURS — which is exactly the state the day
    `add-composed-view-authoring` archives out of the `--all` corpus. The run
    must REFUSE (exit 2) until the entry is deleted, so the archive itself is
    the event that forces somebody to re-read the exception.
    """
    calls, served = fake_npm
    served["verdict"] = 0
    served["report"] = report(items=90)          # the finding is gone
    (tmp_path / "openspec").mkdir()
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition()))
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 2
    captured = capsys.readouterr()
    assert "pin-disposition-stale" in captured.err
    assert FINDING_ITEM in captured.err
    assert "archived out of" in captured.err
    assert "Remediation:" in captured.err


def test_a_reworded_finding_goes_both_stale_and_undispositioned(
        mod, tmp_path, fake_npm):
    """UPGRADE-COUPLING, demonstrated rather than promised.

    A later CLI that rewords the message matches no disposition. The refusal
    that wins is the STALE one — the loudest available answer to "this pin is
    asserting something about a corpus it no longer describes" — and a human
    re-derives the list at the version that reworded it.
    """
    calls, served = fake_npm
    served["verdict"] = 1
    served["report"] = report(
        (FINDING_ITEM, FINDING_PATH, FINDING_TEXT + " Additionally, see docs."),
        items=90)
    (tmp_path / "openspec").mkdir()
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition()))
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 2


def test_whitespace_in_the_pin_does_not_change_what_a_disposition_matches(
        mod, tmp_path, fake_npm):
    """Folding a long `finding:` across lines is a formatting act, and the only
    difference a formatting act may introduce is whitespace."""
    calls, served = fake_npm
    served["verdict"] = 1
    served["report"] = report((FINDING_ITEM, FINDING_PATH, FINDING_TEXT),
                              items=90)
    (tmp_path / "openspec").mkdir()
    folded = ("dispositions:\n"
              "  - repo: openxFactory\n"
              f"    item: {FINDING_ITEM}\n"
              f"    path: {FINDING_PATH}\n"
              "    finding: >-\n"
              + "".join(f"      {chunk}\n"
                        for chunk in FINDING_TEXT.split(". ")[:-1])
              + f"      {FINDING_TEXT.split('. ')[-1]}\n"
              "    why: a declared narrowing\n"
              "    ratified_by: Brett Heap\n"
              "    cited_to:\n"
              "      - openspec/specs/doc-health/spec.md:1770\n")
    path = write_pin(tmp_path, dispositions_block=folded)
    read = mod.read_pin(path)["dispositions"][0]["finding"]
    assert mod.normalized_finding(read) != mod.normalized_finding(FINDING_TEXT), \
        "the fold drops the '. ' separators, so this is the NEGATIVE control"
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 2


def test_an_empty_disposition_list_keeps_the_streaming_path_untouched(
        mod, tmp_path, fake_npm, capsys):
    """THE 1.2.0-ERA BEHAVIOUR, byte for byte, for a pin that grants nothing.

    No `--json`, no parsing, the CLI's own exit code as the verdict, and no git
    call to identify the repository. A pin that declares no exception cannot be
    made to fail by a mechanism it never uses.
    """
    calls, served = fake_npm
    (tmp_path / "openspec").mkdir()
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(write_pin(tmp_path))]) == 0
    assert not any("--json" in call for call in calls)
    assert not any(call[0] == "git" for call in calls)
    assert "validated --strict clean" in capsys.readouterr().out


def test_the_integrity_check_still_precedes_everything_dispositions_do(
        mod, tmp_path, fake_npm):
    """A pin whose bytes do not verify never reaches its dispositions: an
    exception granted over an unverified tool is an exception granted to
    whatever answered."""
    calls, served = fake_npm
    served["payload"] = b"different bytes published under the same version"
    (tmp_path / "openspec").mkdir()
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition()))
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 2
    assert not any(call[1:2] == ["install"] for call in calls)
    assert not any(call[1:2] == ["validate"] for call in calls)


def test_a_malformed_disposition_refuses_before_a_registry_round_trip(
        mod, tmp_path, fake_npm):
    """Ordering, again: a defect of the PIN must not be discovered only after a
    fetch and a full corpus validation have been spent reaching it."""
    calls, served = fake_npm
    (tmp_path / "openspec").mkdir()
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition(cited_to=None)))
    assert mod.main(["--all", "--no-cache", "--repo", str(tmp_path),
                     "--pin", str(path)]) == 2
    assert calls == [], "a malformed exception must not spend a registry round trip"


def test_a_disposition_declaring_a_level_that_could_never_match_is_refused(
        mod, tmp_path):
    """`level:` is human-facing, but a level the matcher could never reconcile
    reads to a reviewer as an exception granted over a warning."""
    path = write_pin(tmp_path, dispositions_block=disposition_block(
        a_disposition(level="WARNING")))
    with pytest.raises(mod.PinRefusal) as exc:
        mod.pinned_dispositions(mod.read_pin(path))
    assert exc.value.code == "pin-disposition-malformed"
