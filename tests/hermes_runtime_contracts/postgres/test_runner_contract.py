"""RED contracts for the digest-pinned PostgreSQL 15/16 runner."""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import time

import pytest
import yaml

from scripts.hermes_runtime_validation.fixtures import (
    database_test_suite,
    repository_source_identity,
)
from scripts.hermes_runtime_validation.loader import load_yaml_document

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RUNNER = REPOSITORY_ROOT / "scripts/run-hermes-runtime-postgres-tests.sh"
COMPOSE = Path(__file__).with_name("compose.yaml")
IMAGE_LOCK = Path(__file__).with_name("images.lock.yaml")
MIGRATION_RECOVERY = Path(__file__).with_name("test_migration_recovery.py")


def _load_yaml(path: Path) -> dict[str, object]:
    assert path.is_file(), f"planned PostgreSQL harness artifact is missing: {path}"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(document, dict)
    return document


def _copy_harness(tmp_path: Path) -> Path:
    destination = tmp_path / "repository"
    shutil.copytree(
        REPOSITORY_ROOT,
        destination,
        ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__", ".pytest_cache"),
    )
    for arguments in (
        ("init", "--quiet"),
        ("config", "user.name", "Hermes Runner Tests"),
        ("config", "user.email", "hermes-runner@example.invalid"),
        ("add", "."),
        ("commit", "--quiet", "-m", "runner fixture"),
    ):
        completed = subprocess.run(
            ["git", *arguments],
            cwd=destination,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
    return destination


def _install_fake_docker(tmp_path: Path) -> tuple[Path, Path, Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log_path = tmp_path / "docker-commands.jsonl"
    secret_path = tmp_path / "observed-password"
    executable = bin_dir / "docker"
    executable.write_text(
        """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import signal
import sys

args = sys.argv[1:]
log_path = Path(os.environ["HERMES_FAKE_DOCKER_LOG"])
with log_path.open("a", encoding="utf-8") as stream:
    stream.write(json.dumps({"argv": args}, sort_keys=True) + "\\n")

password = os.environ.get("POSTGRES_PASSWORD", "")
if password:
    Path(os.environ["HERMES_FAKE_SECRET_CAPTURE"]).write_text(password, encoding="utf-8")
    print(password)

joined = " ".join(args)
failure = os.environ.get("HERMES_FAKE_DOCKER_FAIL_ON", "")
if failure and failure in joined:
    raise SystemExit(41)
if args[:2] == ["image", "inspect"]:
    image = args[-1]
    print(image if "@sha256:" in image else "postgres@sha256:" + "a" * 64)
elif "config" in args and "--format" in args:
    print("{}")
raise SystemExit(0)
""",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    fake_pytest = bin_dir / "pytest"
    fake_pytest.write_text(
        """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import signal
import sys

arguments = sys.argv[1:]
ready_path = os.environ.get("HERMES_FAKE_PYTEST_READY")
if ready_path:
    Path(ready_path).write_text(str(os.getpid()), encoding="utf-8")
    signal.pause()
Path(os.environ["HERMES_FAKE_PYTEST_ARGS"]).write_text(
    json.dumps(arguments), encoding="utf-8"
)
junit = next(value.partition("=")[2] for value in arguments if value.startswith("--junitxml="))
selection = next(value for value in arguments if value.startswith("postgres and (postgres_"))
major = os.environ["HERMES_RUNTIME_POSTGRES_MAJOR"]
if selection != f"postgres and (postgres_{major} or not (postgres_15 or postgres_16))":
    raise SystemExit(3)
expected = json.loads(Path(os.environ["HERMES_RUNTIME_EXPECTED_NODES"]).read_text())
collected = list(expected)
started = list(expected)
mode = os.environ.get("HERMES_FAKE_REPORT_MODE", "exact")
if mode == "substitute":
    collected[0] += "::substituted"
    started[0] = collected[0]
elif mode == "duplicate":
    collected[0] = collected[1]
    started[0] = started[1]
reports = [
    {"node_id": node, "phase": phase, "outcome": "passed", "wasxfail": False}
    for node in started
    for phase in ("setup", "call", "teardown")
]
if mode == "xfail":
    reports[1]["wasxfail"] = True
elif mode == "skip":
    reports[0]["outcome"] = "skipped"
Path(os.environ["HERMES_RUNTIME_PYTEST_REPORT"]).write_text(
    json.dumps(
        {
            "collected_node_ids": sorted(collected),
            "started_node_ids": sorted(started),
            "reports": reports,
        }
    ),
    encoding="utf-8",
)
Path(junit).write_text(
    f'<testsuites tests="{len(expected)}" failures="0" errors="0" skipped="0" />\\n',
    encoding="utf-8",
)
""",
        encoding="utf-8",
    )
    fake_pytest.chmod(0o755)
    return bin_dir, log_path, secret_path


def _run_runner(
    repository: Path,
    fake_docker: tuple[Path, Path, Path],
    *args: str,
    fail_on: str | None = None,
    report_mode: str | None = None,
) -> subprocess.CompletedProcess[str]:
    runner = repository / "scripts/run-hermes-runtime-postgres-tests.sh"
    assert runner.is_file(), f"planned PostgreSQL runner is missing: {runner}"
    bin_dir, log_path, secret_path = fake_docker
    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{bin_dir}:{env['PATH']}",
            "HERMES_FAKE_DOCKER_LOG": str(log_path),
            "HERMES_FAKE_SECRET_CAPTURE": str(secret_path),
            "HERMES_FAKE_PYTEST_ARGS": str(bin_dir.parent / "pytest-args.json"),
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
        }
    )
    if fail_on is not None:
        env["HERMES_FAKE_DOCKER_FAIL_ON"] = fail_on
    if report_mode is not None:
        env["HERMES_FAKE_REPORT_MODE"] = report_mode
    return subprocess.run(
        [runner, *args],
        cwd=repository,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )


def _commands(log_path: Path) -> list[list[str]]:
    return [json.loads(line)["argv"] for line in log_path.read_text().splitlines()]


def _method_source(class_name: str, method_name: str) -> str:
    source = MIGRATION_RECOVERY.read_text(encoding="utf-8")
    module = ast.parse(source)
    class_node = next(
        node
        for node in module.body
        if isinstance(node, ast.ClassDef) and node.name == class_name
    )
    method_node = next(
        node
        for node in class_node.body
        if isinstance(node, ast.FunctionDef) and node.name == method_name
    )
    segment = ast.get_source_segment(source, method_node)
    assert segment is not None
    return segment


def test_image_lock_has_reviewable_digest_pins_for_15_and_16() -> None:
    lock = _load_yaml(IMAGE_LOCK)
    assert lock["schema_version"] == 1
    assert lock["kind"] == "HermesRuntimePostgresImageLock"
    images = lock["images"]
    assert isinstance(images, dict)
    for major in ("15", "16"):
        entry = images[major]
        assert entry["source_tag"] == f"postgres:{major}"
        assert re.fullmatch(r"postgres@sha256:[0-9a-f]{64}", entry["resolved_image"])
        assert entry["platform"]
        assert isinstance(entry["update_evidence"], dict)


def test_compose_is_networkless_has_no_host_port_and_uses_throwaway_storage() -> None:
    compose = _load_yaml(COMPOSE)
    services = compose["services"]
    assert isinstance(services, dict) and services
    for service in services.values():
        assert "ports" not in service
        assert service.get("network_mode") == "none"
    assert any(service.get("healthcheck") for service in services.values())
    assert compose["volumes"]
    assert "networks" not in compose
    mounts = [
        mount for service in services.values() for mount in service.get("volumes", [])
    ]
    assert any(
        (isinstance(mount, str) and mount.endswith(":ro"))
        or (isinstance(mount, dict) and mount.get("read_only") is True)
        for mount in mounts
    )


def test_migration_waiters_use_zero_server_timeouts_and_only_boundary_errors() -> None:
    post_lock = _method_source(
        "TestConcurrentV1Writes",
        "test_post_lock_write_is_excluded_by_cutover_locks_and_durable_freeze",
    )
    lock_wait = _method_source(
        "TestConcurrentV1Writes",
        "test_write_committing_during_lock_wait_aborts_cutover",
    )

    assert post_lock.count("SET lock_timeout = 0;") == 2
    assert post_lock.count("SET statement_timeout = 0;") == 2
    assert "assert_sql_fails(write_result, *FROZEN_FRAGMENTS)" in post_lock
    assert lock_wait.count("SET lock_timeout = 0;") == 2
    assert lock_wait.count("SET statement_timeout = 0;") == 2
    assert 'assert_sql_fails(cutover_result, "HGR-MIGRATION-BOUNDARY-MISMATCH")' in lock_wait


@pytest.mark.parametrize("major", ["15", "16"])
def test_json_run_uses_pinned_image_and_redacts_ephemeral_secret(
    tmp_path: Path, major: str
) -> None:
    repository = _copy_harness(tmp_path)
    fake = _install_fake_docker(tmp_path)
    result = _run_runner(repository, fake, "--major", major, "--json")
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == 1
    assert payload["kind"] == "HermesRuntimePostgresEvidence"
    assert payload["major"] == int(major)
    assert payload["outcome"] == "pass"
    assert re.fullmatch(r"postgres@sha256:[0-9a-f]{64}", payload["image"])
    index = load_yaml_document(
        repository / "contracts/hermes-runtime/fixtures/index.yaml"
    )
    database_case = next(
        case for case in index["cases"] if case.get("phase") == "database"
    )
    assert payload["source_identity"] == repository_source_identity(
        repository, database_case
    )
    assert payload["source_identity"]["profile"] == (
        "xfactory-postgres-source-inputs-v1"
    )
    assert payload["suite"] == database_test_suite(
        repository, database_case["database"], int(major)
    )
    assert payload["matrix"]["case_id"] == "postgres-us2-governed-isolation-matrix"
    assert payload["matrix"]["profile"] == "xfactory-postgres-matrix-v1"
    assert re.fullmatch(r"sha256:[0-9a-f]{64}", payload["matrix"]["digest"])
    evidence_path = (
        repository
        / f"tests/hermes_runtime_contracts/postgres/evidence/postgres-{major}.json"
    )
    assert json.loads(evidence_path.read_text(encoding="utf-8")) == payload

    _, log_path, secret_path = fake
    secret = secret_path.read_text(encoding="utf-8")
    assert len(secret) >= 32
    visible = result.stdout + result.stderr
    evidence_root = repository / "tests/hermes_runtime_contracts/postgres/evidence"
    if evidence_root.exists():
        visible += "".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in evidence_root.rglob("*")
            if path.is_file()
        )
    assert secret not in visible
    assert all(
        secret not in argument
        for command in _commands(log_path)
        for argument in command
    )
    pytest_arguments = json.loads(
        (tmp_path / "pytest-args.json").read_text(encoding="utf-8")
    )
    expected_modules = {
        str(repository / path) for path in database_case["database"]["test_modules"]
    }
    assert expected_modules.issubset(pytest_arguments)
    assert str(repository / "tests/hermes_runtime_contracts/postgres") not in pytest_arguments


@pytest.mark.parametrize("mode", ["substitute", "duplicate", "xfail", "skip"])
def test_runner_rejects_inexact_execution_report(tmp_path: Path, mode: str) -> None:
    repository = _copy_harness(tmp_path)
    fake = _install_fake_docker(tmp_path)

    result = _run_runner(
        repository,
        fake,
        "--major",
        "15",
        "--json",
        report_mode=mode,
    )

    assert result.returncode != 0
    assert not (
        repository / "tests/hermes_runtime_contracts/postgres/evidence/postgres-15.json"
    ).exists()


def test_failure_still_tears_down_containers_and_volumes(
    tmp_path: Path,
) -> None:
    repository = _copy_harness(tmp_path)
    fake = _install_fake_docker(tmp_path)
    result = _run_runner(repository, fake, "--major", "15", "--json", fail_on=" up ")
    assert result.returncode != 0
    commands = _commands(fake[1])
    down = [command for command in commands if "down" in command]
    assert down, commands
    assert any("--volumes" in command for command in down)
    assert any("--remove-orphans" in command for command in down)


def test_signal_termination_tears_down_once_without_cleanup_traceback(
    tmp_path: Path,
) -> None:
    repository = _copy_harness(tmp_path)
    fake = _install_fake_docker(tmp_path)
    bin_dir, log_path, secret_path = fake
    ready_path = tmp_path / "pytest-ready"
    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{bin_dir}:{env['PATH']}",
            "HERMES_FAKE_DOCKER_LOG": str(log_path),
            "HERMES_FAKE_SECRET_CAPTURE": str(secret_path),
            "HERMES_FAKE_PYTEST_ARGS": str(tmp_path / "pytest-args.json"),
            "HERMES_FAKE_PYTEST_READY": str(ready_path),
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
        }
    )
    process = subprocess.Popen(
        [repository / "scripts/run-hermes-runtime-postgres-tests.sh", "--major", "15"],
        cwd=repository,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        deadline = time.monotonic() + 10
        while not ready_path.exists() and process.poll() is None:
            assert time.monotonic() < deadline, "runner never reached pytest"
            time.sleep(0.05)
        assert ready_path.exists(), "fake pytest never published its ready marker"
        pytest_pid = int(ready_path.read_text(encoding="utf-8"))
        with pytest.raises(subprocess.TimeoutExpired):
            process.wait(timeout=0.2)
        pytest_state = Path(f"/proc/{pytest_pid}/stat").read_text(
            encoding="utf-8"
        ).split()[2]
        assert pytest_state != "Z", "fake pytest exited before runner SIGTERM"
        os.killpg(process.pid, signal.SIGTERM)
        stdout, stderr = process.communicate(timeout=10)
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=10)

    assert process.returncode != 0
    assert "FileNotFoundError" not in stdout + stderr
    down = [command for command in _commands(log_path) if "down" in command]
    assert len(down) == 1, down


@pytest.mark.parametrize("selected", ["15", "16"])
def test_every_attempt_invalidates_selected_prior_pass_before_dependencies(
    tmp_path: Path, selected: str
) -> None:
    repository = _copy_harness(tmp_path)
    evidence = (
        repository
        / f"tests/hermes_runtime_contracts/postgres/evidence/postgres-{selected}.json"
    )
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text('{"stale":"pass"}\n', encoding="utf-8")
    fake = _install_fake_docker(tmp_path)

    result = _run_runner(
        repository,
        fake,
        "--major",
        selected,
        "--json",
        fail_on="image inspect",
    )

    assert result.returncode == 2
    assert not evidence.exists()


def test_unscoped_attempt_invalidates_both_prior_major_results(tmp_path: Path) -> None:
    repository = _copy_harness(tmp_path)
    evidence_root = repository / "tests/hermes_runtime_contracts/postgres/evidence"
    evidence_root.mkdir(parents=True, exist_ok=True)
    evidence_files = [evidence_root / f"postgres-{major}.json" for major in (15, 16)]
    for evidence in evidence_files:
        evidence.write_text('{"stale":"pass"}\n', encoding="utf-8")
    fake = _install_fake_docker(tmp_path)

    result = _run_runner(repository, fake, "--json", fail_on="image inspect")

    assert result.returncode == 2
    assert all(not evidence.exists() for evidence in evidence_files)


def test_invalid_major_is_exit_two_and_never_starts_docker(tmp_path: Path) -> None:
    repository = _copy_harness(tmp_path)
    fake = _install_fake_docker(tmp_path)
    result = _run_runner(repository, fake, "--major", "17", "--json")
    assert result.returncode == 2
    assert not fake[1].exists()


def test_image_lock_refresh_is_explicit_and_uses_official_source_tags(
    tmp_path: Path,
) -> None:
    repository = _copy_harness(tmp_path)
    fake = _install_fake_docker(tmp_path)
    result = _run_runner(repository, fake, "--update-image-lock")
    assert result.returncode == 0, result.stdout + result.stderr

    lock = _load_yaml(
        repository / "tests/hermes_runtime_contracts/postgres/images.lock.yaml"
    )
    for major in ("15", "16"):
        assert lock["images"][major]["resolved_image"] == (  # type: ignore[index]
            "postgres@sha256:" + "a" * 64
        )
    commands = _commands(fake[1])
    for major in ("15", "16"):
        assert any(
            command[-1] == f"postgres:{major}" and "pull" in command
            for command in commands
        )
        assert any(
            command[-1] == f"postgres:{major}" and command[:2] == ["image", "inspect"]
            for command in commands
        )
