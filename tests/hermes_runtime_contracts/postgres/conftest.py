"""Shared helpers for the isolated PostgreSQL conformance harness.

These helpers deliberately avoid a database driver.  The production harness is
required to exercise the same Docker/Compose subprocess boundary used by the
release gate.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass, field
import hashlib
import os
from pathlib import Path
import re
import secrets
import subprocess
from typing import Any

import pytest


REDACTED = "<redacted>"
_SENSITIVE_KEY = re.compile(r"(?:password|passwd|secret|token|credential)", re.I)


@dataclass
class CleanupStack:
    """Small LIFO cleanup registry whose callbacks always all run."""

    _callbacks: list[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = field(
        default_factory=list
    )

    def register(self, callback: Callable[..., Any], /, *args: Any, **kwargs: Any) -> None:
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
def ephemeral_postgres_credential(monkeypatch: pytest.MonkeyPatch) -> Iterator[EphemeralCredential]:
    key = "HERMES_RUNTIME_POSTGRES_PASSWORD"
    credential = EphemeralCredential(key, secrets.token_urlsafe(36))
    monkeypatch.setenv(key, credential.value)
    try:
        yield credential
    finally:
        monkeypatch.delenv(key, raising=False)


@pytest.fixture
def run_postgres_subprocess() -> Callable[..., subprocess.CompletedProcess[str]]:
    """Run a bounded, shell-free subprocess with deterministic locale settings."""

    def run(
        argv: Sequence[str | os.PathLike[str]],
        *,
        cwd: Path,
        env: Mapping[str, str] | None = None,
        timeout: float = 30,
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
            timeout=timeout,
            check=False,
        )

    return run
