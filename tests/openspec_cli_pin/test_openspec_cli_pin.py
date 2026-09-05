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
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate-openspec-cli-pin.py"
PIN = ROOT / "contracts" / "openspec-cli-pin.yaml"

VERSION = "1.2.0"
PACKAGE = "@fission-ai/openspec"
INTEGRITY = ("sha512-2XDmPZcVY0Bs014lP9aoxe3VoEU8hFvqaBFxQaiJO2nhC8vTKCyo6sT/"
             "5YpQcOTfR/a64Hht2anTyqLR4eNhlg==")
SHASUM = "0fd5333520c8846f0ac51727379b8812e2f13c1b"

PAYLOAD = b"a synthetic tarball standing in for the published artifact"


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
    fields.update({k: v for k, v in overrides.items() if v is not None})
    for key, value in overrides.items():
        if value is None:
            fields.pop(key, None)
    path = tmp_path / "pin.yaml"
    path.write_text(
        "# a synthetic pin\n"
        + "".join(f"{key}: {value}\n" for key, value in fields.items()),
        encoding="utf-8")
    return path


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
    served = {"payload": PAYLOAD, "reports": VERSION, "verdict": 0}

    def fake_run(argv, **kwargs):
        calls.append([str(a) for a in argv])
        if argv[1:2] == ["pack"]:
            destination = Path(argv[argv.index("--pack-destination") + 1])
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "fission-ai-openspec-1.2.0.tgz").write_bytes(
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
        argv, 0, "1.12.0\n", ""))
    with pytest.raises(mod.PinRefusal) as exc:
        mod.assert_reported_version(Path("/usr/bin/openspec"), VERSION)
    assert exc.value.code == "pin-version-mismatch"
    assert "1.12.0" in exc.value.detail
    assert "Remediation:" in str(exc.value)


def test_path_mode_refuses_the_wrong_version_end_to_end(
        mod, tmp_path, fake_npm, monkeypatch):
    calls, served = fake_npm
    served["reports"] = "1.12.0"
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
