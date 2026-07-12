"""RED contracts for the digest-pinned PostgreSQL 15/16 runner."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from collections.abc import Callable

import pytest
import yaml

from scripts.hermes_runtime_validation.fixtures import (
    collect_database_test_count,
    repository_source_identity,
)
from scripts.hermes_runtime_validation.loader import load_yaml_document

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RUNNER = REPOSITORY_ROOT / "scripts/run-hermes-runtime-postgres-tests.sh"
COMPOSE = Path(__file__).with_name("compose.yaml")
IMAGE_LOCK = Path(__file__).with_name("images.lock.yaml")


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
        "#!/bin/sh\n"
        "set -eu\n"
        'test "${HERMES_RUNTIME_POSTGRES_MAJOR:-}" = 15 -o '
        '"${HERMES_RUNTIME_POSTGRES_MAJOR:-}" = 16\n'
        "junit=\n"
        'for argument in "$@"; do\n'
        '  case "$argument" in --junitxml=*) junit=${argument#--junitxml=} ;; esac\n'
        "done\n"
        'test -n "$junit"\n'
        'printf \'<testsuites tests="%s" failures="0" errors="0" skipped="0" />\\n\' "${HERMES_FAKE_PYTEST_COUNT:?}" >"$junit"\n'
        "exit 0\n",
        encoding="utf-8",
    )
    fake_pytest.chmod(0o755)
    return bin_dir, log_path, secret_path


def _run_runner(
    repository: Path,
    fake_docker: tuple[Path, Path, Path],
    *args: str,
    fail_on: str | None = None,
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
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
        }
    )
    selected_major = "15"
    if "--major" in args:
        position = args.index("--major")
        if position + 1 < len(args) and args[position + 1] in {"15", "16"}:
            selected_major = args[position + 1]
    if "--update-image-lock" not in args:
        index = load_yaml_document(
            repository / "contracts/hermes-runtime/fixtures/index.yaml"
        )
        database_case = next(
            case for case in index["cases"] if case.get("phase") == "database"
        )
        env["HERMES_FAKE_PYTEST_COUNT"] = str(
            collect_database_test_count(
                repository, database_case["database"], int(selected_major)
            )
        )
    if fail_on is not None:
        env["HERMES_FAKE_DOCKER_FAIL_ON"] = fail_on
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


def test_compose_is_internal_has_no_host_port_and_uses_throwaway_storage() -> None:
    compose = _load_yaml(COMPOSE)
    services = compose["services"]
    assert isinstance(services, dict) and services
    for service in services.values():
        assert "ports" not in service
    assert any(service.get("healthcheck") for service in services.values())
    assert compose["volumes"]
    networks = compose["networks"]
    assert networks and all(
        network.get("internal") is True for network in networks.values()
    )
    mounts = [
        mount for service in services.values() for mount in service.get("volumes", [])
    ]
    assert any(
        (isinstance(mount, str) and mount.endswith(":ro"))
        or (isinstance(mount, dict) and mount.get("read_only") is True)
        for mount in mounts
    )


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
    assert payload["suite"] == {
        "id": "hermes-runtime-postgres",
        "test_count": collect_database_test_count(
            repository, database_case["database"], int(major)
        ),
    }
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


def test_failure_still_tears_down_containers_volumes_and_networks(
    tmp_path: Path,
) -> None:
    repository = _copy_harness(tmp_path)
    fake = _install_fake_docker(tmp_path)
    result = _run_runner(repository, fake, "--major", "15", "--json", fail_on=" run ")
    assert result.returncode != 0
    commands = _commands(fake[1])
    down = [command for command in commands if "down" in command]
    assert down, commands
    assert any("--volumes" in command for command in down)
    assert any("--remove-orphans" in command for command in down)


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
