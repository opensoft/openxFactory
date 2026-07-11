"""Env-only credential handling (FR-001 / Clarifications Q2).

The provider credential is read ONLY from the ``OPENAI_API_KEY`` process environment
variable (which CI or an approved secret store may inject, and which a gitignored local
``.env`` may populate). It is never accepted via CLI arguments, tracked ``.env``/config/
evidence files, and is never copied into, printed to, or committed with any artifact.
"""
from __future__ import annotations

import os
from typing import Optional

ENV_VAR = "OPENAI_API_KEY"


class CredentialError(Exception):
    """Raised when a credential is supplied through a prohibited channel."""


def has_credential(env: Optional[dict] = None) -> bool:
    env = os.environ if env is None else env
    return bool(env.get(ENV_VAR, "").strip())


def load_credential(env: Optional[dict] = None) -> Optional[str]:
    """Return the credential from the environment, or ``None`` if absent.

    A missing key is NOT an error (it drives the INCONCLUSIVE-without-key completion
    path, SC-013); callers must never log or persist the returned value.
    """
    env = os.environ if env is None else env
    value = env.get(ENV_VAR, "").strip()
    return value or None


def reject_if_in_arguments(argv_values) -> None:
    """Fail closed if anything that looks like a credential was passed as an argument.

    We never accept a key via CLI; this guards against accidental exposure (FR-003).
    """
    for v in argv_values:
        if not v:
            continue
        s = str(v)
        # OpenAI keys are long high-entropy strings, conventionally prefixed ``sk-``.
        if s.startswith("sk-") or (len(s) >= 40 and s.replace("-", "").isalnum() and any(c.isdigit() for c in s) and any(c.isalpha() for c in s) and s.count(" ") == 0 and _looks_secretish(s)):
            raise CredentialError(
                "a credential-like value was supplied as an argument; "
                f"provide it only via the {ENV_VAR} environment variable"
            )


def _looks_secretish(s: str) -> bool:
    # Heuristic: reject obvious key material; keep it conservative to avoid false rejects
    # of legitimate hashes (which are lowercase hex only and handled elsewhere).
    has_upper = any(c.isupper() for c in s)
    has_lower = any(c.islower() for c in s)
    return has_upper and has_lower
