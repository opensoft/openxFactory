"""Shared helpers for the isolated PostgreSQL conformance harness.

These helpers deliberately avoid a database driver.  The production harness is
required to exercise the same Docker/Compose subprocess boundary used by the
release gate.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import hashlib
import os
from pathlib import Path
import re
import secrets
import subprocess
import time
from typing import Any

import pytest
import yaml

REDACTED = "<redacted>"
_SENSITIVE_KEY = re.compile(r"(?:password|passwd|secret|token|credential)", re.I)

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
POSTGRES_ROOT = Path(__file__).resolve().parent
COMPOSE_FILE = POSTGRES_ROOT / "compose.yaml"
IMAGE_LOCK_FILE = POSTGRES_ROOT / "images.lock.yaml"
CANONICAL_DDL = (
    REPOSITORY_ROOT / "contracts/hermes-runtime/hermes-operational-postgres-v2.sql"
)
ISOLATION_FIXTURE_ROOT = POSTGRES_ROOT / "fixtures/isolation"
ISOLATION_ASSERTION_ROOT = POSTGRES_ROOT / "assertions/isolation"
BASE_DATABASE = "hermes_runtime_contracts"
BOOTSTRAP_USER = "hermes_runtime"


@dataclass
class CleanupStack:
    """Small LIFO cleanup registry whose callbacks always all run."""

    _callbacks: list[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = (
        field(default_factory=list)
    )

    def register(
        self, callback: Callable[..., Any], /, *args: Any, **kwargs: Any
    ) -> None:
        self._callbacks.append((callback, args, kwargs))

    def close(self) -> None:
        failures: list[BaseException] = []
        while self._callbacks:
            callback, args, kwargs = self._callbacks.pop()
            try:
                callback(*args, **kwargs)
            except BaseException as exc:  # cleanup must continue after one failure
                failures.append(exc)
        if failures:
            raise ExceptionGroup("PostgreSQL test cleanup failed", failures)


@dataclass(frozen=True)
class EphemeralCredential:
    environment_key: str
    value: str

    @property
    def fingerprint(self) -> str:
        return hashlib.sha256(self.value.encode("utf-8")).hexdigest()


def _selected_postgres_majors() -> tuple[str, ...]:
    selected = os.environ.get("HERMES_RUNTIME_POSTGRES_MAJOR", "").strip()
    if not selected:
        return ("15", "16")
    if selected not in {"15", "16"}:
        raise pytest.UsageError(
            "HERMES_RUNTIME_POSTGRES_MAJOR must be 15 or 16 when set"
        )
    return (selected,)


def _render_process(result: subprocess.CompletedProcess[str]) -> str:
    return "\n".join(part for part in (result.stdout, result.stderr) if part).strip()


@dataclass
class PostgresCluster:
    """Digest-pinned Compose cluster exercised only through in-container psql."""

    major: str
    image: str
    project_name: str
    credential: EphemeralCredential
    run_subprocess: Callable[..., subprocess.CompletedProcess[str]]

    @property
    def environment(self) -> dict[str, str]:
        return {
            "COMPOSE_PROJECT_NAME": self.project_name,
            "POSTGRES_IMAGE": self.image,
            "POSTGRES_PASSWORD": self.credential.value,
        }

    def compose(
        self, *arguments: str, timeout: float = 90
    ) -> subprocess.CompletedProcess[str]:
        return self.run_subprocess(
            [
                "docker",
                "compose",
                "--file",
                COMPOSE_FILE,
                "--project-name",
                self.project_name,
                *arguments,
            ],
            cwd=REPOSITORY_ROOT,
            env=self.environment,
            timeout=timeout,
        )

    def psql(
        self,
        database: str,
        sql: str,
        *,
        user: str = BOOTSTRAP_USER,
        timeout: float = 30,
    ) -> subprocess.CompletedProcess[str]:
        # The secret is expanded only inside the container. It never appears in
        # host argv, pytest IDs, evidence, or committed fixture bytes.
        command = (
            'PGPASSWORD="$POSTGRES_PASSWORD" exec psql -X -q -A -t '
            '-v ON_ERROR_STOP=1 -v hcs_test_password="$POSTGRES_PASSWORD" '
            '-h 127.0.0.1 -U "$1" -d "$2"'
        )
        return self.run_subprocess(
            [
                "docker",
                "compose",
                "--file",
                COMPOSE_FILE,
                "--project-name",
                self.project_name,
                "exec",
                "-T",
                "postgres",
                "sh",
                "-ceu",
                command,
                "hcs-psql",
                user,
                database,
            ],
            cwd=REPOSITORY_ROOT,
            env=self.environment,
            timeout=timeout,
            input_text=sql,
        )

    def psql_file(
        self,
        database: str,
        path: Path,
        *,
        user: str = BOOTSTRAP_USER,
        timeout: float = 30,
    ) -> subprocess.CompletedProcess[str]:
        assert path.is_file(), f"required SQL fixture is unavailable: {path}"
        return self.psql(
            database,
            path.read_text(encoding="utf-8"),
            user=user,
            timeout=timeout,
        )


@dataclass(frozen=True)
class PostgresDatabase:
    """One test-isolated database cloned from the canonical DDL template."""

    cluster: PostgresCluster
    name: str

    @property
    def major(self) -> str:
        return self.cluster.major

    def sql(
        self,
        statement: str,
        *,
        user: str = BOOTSTRAP_USER,
        timeout: float = 30,
    ) -> subprocess.CompletedProcess[str]:
        return self.cluster.psql(self.name, statement, user=user, timeout=timeout)

    def file(
        self,
        path: Path,
        *,
        user: str = BOOTSTRAP_USER,
        timeout: float = 30,
    ) -> subprocess.CompletedProcess[str]:
        return self.cluster.psql_file(self.name, path, user=user, timeout=timeout)

    def scalar(self, statement: str, *, user: str = BOOTSTRAP_USER) -> str:
        result = self.sql(statement, user=user)
        assert result.returncode == 0, _render_process(result)
        rows = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        assert len(rows) == 1, rows
        return rows[0]

    def race(
        self,
        calls: Sequence[tuple[str, str]],
        *,
        timeout: float = 45,
    ) -> list[subprocess.CompletedProcess[str]]:
        with ThreadPoolExecutor(max_workers=len(calls)) as executor:
            futures = [
                executor.submit(self.sql, sql, user=user, timeout=timeout)
                for user, sql in calls
            ]
            return [future.result(timeout=timeout + 5) for future in futures]


def assert_sql_succeeds(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, _render_process(result)


def assert_sql_fails(
    result: subprocess.CompletedProcess[str], *required_fragments: str
) -> None:
    assert result.returncode != 0, "SQL unexpectedly succeeded"
    rendered = _render_process(result).lower()
    assert any(
        fragment.lower() in rendered for fragment in required_fragments
    ), rendered


def redact_evidence(value: Any, secrets_to_redact: Sequence[str]) -> Any:
    """Recursively redact secret-bearing keys and exact secret substrings."""

    secrets_by_length = sorted(
        (secret for secret in secrets_to_redact if secret), key=len, reverse=True
    )
    if isinstance(value, Mapping):
        return {
            key: (
                REDACTED
                if _SENSITIVE_KEY.search(str(key))
                else redact_evidence(item, secrets_by_length)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_evidence(item, secrets_by_length) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_evidence(item, secrets_by_length) for item in value)
    if isinstance(value, bytes):
        value = value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        for secret in secrets_by_length:
            value = value.replace(secret, REDACTED)
    return value


def assert_evidence_redacted(value: Any, secrets_to_redact: Sequence[str]) -> None:
    rendered = repr(value)
    for secret in secrets_to_redact:
        if secret:
            assert secret not in rendered


@pytest.fixture
def compose_project_name(request: pytest.FixtureRequest) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", request.node.nodeid.lower()).strip("-")
    slug = slug[-38:] or "postgres"
    return f"hcs-{slug}-{secrets.token_hex(5)}"


@pytest.fixture
def cleanup_stack() -> Iterator[CleanupStack]:
    stack = CleanupStack()
    yield stack
    stack.close()


@pytest.fixture
def ephemeral_postgres_credential(
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[EphemeralCredential]:
    key = "HERMES_RUNTIME_POSTGRES_PASSWORD"
    credential = EphemeralCredential(key, secrets.token_urlsafe(36))
    monkeypatch.setenv(key, credential.value)
    try:
        yield credential
    finally:
        monkeypatch.delenv(key, raising=False)


@pytest.fixture(scope="session")
def run_postgres_subprocess() -> Callable[..., subprocess.CompletedProcess[str]]:
    """Run a bounded, shell-free subprocess with deterministic locale settings."""

    def run(
        argv: Sequence[str | os.PathLike[str]],
        *,
        cwd: Path,
        env: Mapping[str, str] | None = None,
        timeout: float = 30,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        process_env = os.environ.copy()
        process_env.update(
            {
                "LC_ALL": "C.UTF-8",
                "LANG": "C.UTF-8",
                "TZ": "UTC",
                "PYTHONHASHSEED": "0",
            }
        )
        if env:
            process_env.update(env)
        return subprocess.run(
            [os.fspath(argument) for argument in argv],
            cwd=cwd,
            env=process_env,
            capture_output=True,
            text=True,
            input=input_text,
            timeout=timeout,
            check=False,
        )

    return run


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "postgres: requires a digest-pinned real PostgreSQL 15 or 16 container",
    )


@pytest.fixture(scope="session", params=_selected_postgres_majors())
def postgres_cluster(
    request: pytest.FixtureRequest,
    run_postgres_subprocess: Callable[..., subprocess.CompletedProcess[str]],
) -> Iterator[PostgresCluster]:
    major = str(request.param)
    assert CANONICAL_DDL.is_file(), (
        "canonical PostgreSQL v2 DDL unavailable; RED boundary: " f"{CANONICAL_DDL}"
    )
    lock = yaml.safe_load(IMAGE_LOCK_FILE.read_text(encoding="utf-8"))
    image = lock["images"][major]["resolved_image"]
    assert re.fullmatch(r"postgres@sha256:[0-9a-f]{64}", image), image

    credential = EphemeralCredential("POSTGRES_PASSWORD", secrets.token_urlsafe(36))
    project = f"hcs-us2-{major}-{os.getpid()}-{secrets.token_hex(4)}"
    cluster = PostgresCluster(
        major=major,
        image=image,
        project_name=project,
        credential=credential,
        run_subprocess=run_postgres_subprocess,
    )

    inspect = run_postgres_subprocess(
        ["docker", "image", "inspect", image],
        cwd=REPOSITORY_ROOT,
        env=cluster.environment,
        timeout=30,
    )
    assert inspect.returncode == 0, (
        f"required digest-pinned PostgreSQL {major} image unavailable: "
        f"{_render_process(inspect)}"
    )

    started = False
    try:
        up = cluster.compose("up", "--detach", "--wait", "postgres", timeout=90)
        assert_sql_succeeds(up)
        started = True

        # Compose's image health check probes the local Unix socket, while the
        # contract harness deliberately exercises the container's TCP path.
        # Prove that exact path is ready before applying the canonical DDL.
        readiness: subprocess.CompletedProcess[str] | None = None
        for _ in range(30):
            readiness = cluster.psql(BASE_DATABASE, "SELECT 1;")
            if readiness.returncode == 0:
                break
            time.sleep(0.2)
        else:
            assert readiness is not None
            pytest.fail(
                f"PostgreSQL {major} TCP readiness failed after Compose "
                f"reported healthy: {_render_process(readiness)}"
            )

        applied = cluster.psql(
            BASE_DATABASE, CANONICAL_DDL.read_text(encoding="utf-8"), timeout=90
        )
        assert applied.returncode == 0, (
            f"canonical PostgreSQL v2 DDL failed on major {major}: "
            f"{_render_process(applied)}"
        )
        roles = cluster.psql_file(
            BASE_DATABASE,
            ISOLATION_FIXTURE_ROOT / "00-cluster-roles.sql",
        )
        assert roles.returncode == 0, _render_process(roles)
        yield cluster
    finally:
        if started:
            down = cluster.compose("down", "--volumes", "--remove-orphans", timeout=90)
            assert down.returncode == 0, _render_process(down)


@pytest.fixture
def postgres_database(
    request: pytest.FixtureRequest, postgres_cluster: PostgresCluster
) -> Iterator[PostgresDatabase]:
    digest = hashlib.sha256(request.node.nodeid.encode("utf-8")).hexdigest()[:12]
    database_name = f"hcs_{postgres_cluster.major}_{digest}"
    create_sql = (
        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
        f"WHERE datname = '{database_name}' AND pid <> pg_backend_pid();\n"
        f'DROP DATABASE IF EXISTS "{database_name}";\n'
        f'CREATE DATABASE "{database_name}" TEMPLATE "{BASE_DATABASE}";\n'
    )
    created = postgres_cluster.psql("postgres", create_sql)
    assert created.returncode == 0, _render_process(created)

    database = PostgresDatabase(postgres_cluster, database_name)
    try:
        for fixture in (
            "10-two-customer-topology.sql",
            "20-authority.sql",
            "30-governed-evidence.sql",
        ):
            seeded = database.file(ISOLATION_FIXTURE_ROOT / fixture)
            assert (
                seeded.returncode == 0
            ), f"isolation fixture {fixture} failed: {_render_process(seeded)}"
        yield database
    finally:
        cleanup_sql = (
            "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
            f"WHERE datname = '{database_name}' AND pid <> pg_backend_pid();\n"
            f'DROP DATABASE IF EXISTS "{database_name}";\n'
        )
        dropped = postgres_cluster.psql("postgres", cleanup_sql)
        assert dropped.returncode == 0, _render_process(dropped)
