"""AVC reference runtime — deterministic, NON-DEPLOYABLE contract proof.

This package is a reference implementation of the neutral Avatar Client (AVC)
protocol built solely to *prove* protocol invariants deterministically. It is
NOT a production service and MUST NOT become one:

- No network listener, application factory, deployment manifest, HTTP/socket
  server, persistence adapter, provider-credential loading, or live provider
  SDK is exported or imported here.
- Every nondeterministic or authoritative dependency enters through an injected
  port (see ``ports``); the core never calls ambient wall time, random id
  generation, sleep, the filesystem, or a network API.
- The package imports only the Python standard library. A boundary validator
  (``tests/avatar_runtime/boundary``) and ``scripts/validate-avatar-runtime.py``
  enforce all of the above statically.

Feature: specs/003-avc-reference-runtime. Target: Python 3.11+.
"""

from __future__ import annotations

__all__ = ["build_runtime"]

# Reference-only marker consumed by the boundary validator.
IS_REFERENCE_ONLY = True


def build_runtime(*args, **kwargs):  # noqa: ANN001, ANN002, ANN003
    """Lazily construct an in-process :class:`AvatarRuntime`.

    This is a plain in-process factory for tests — deliberately NOT an
    application/ASGI/WSGI factory, and it opens no socket and loads no
    credential.
    """
    from .runtime import AvatarRuntime

    return AvatarRuntime(*args, **kwargs)
