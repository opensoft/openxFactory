"""Pure-stdlib static boundary scanner (FR-001/FR-004a, SC-005/010).

Execution-free: parses source with ``ast`` and inspects imports, exports,
entrypoints, and file surfaces WITHOUT importing or running the runtime. Shared
by the in-suite boundary test and ``scripts/validate-avatar-runtime.py`` so both
enforce identical rules.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

# Stdlib modules that are nonetheless forbidden in a non-deployable, hermetic
# reference package (networking, servers, persistence, subprocess, dynamic fs).
FORBIDDEN_STDLIB = frozenset(
    {
        "socket", "socketserver", "ssl", "asyncio", "selectors",
        "http", "urllib", "ftplib", "smtplib", "imaplib", "poplib", "telnetlib",
        "wsgiref", "xmlrpc", "cgi", "cgitb",
        "sqlite3", "dbm", "shelve", "pickle", "shove",
        "subprocess", "multiprocessing",
    }
)

# Known third-party network / provider SDKs (defence in depth; any third-party
# import is already flagged, but these get a clearer message).
PROVIDER_SDKS = frozenset(
    {
        "openai", "aiohttp", "requests", "httpx", "websockets", "grpc",
        "boto3", "flask", "fastapi", "starlette", "uvicorn", "gunicorn",
        "django", "sqlalchemy", "psycopg2", "redis", "pymongo", "kafka",
    }
)

# Attribute call surfaces that indicate a deployment/persistence surface.
FORBIDDEN_CALL_ATTRS = frozenset(
    {
        "start_server", "create_server", "HTTPServer", "run", "serve",
        "connect", "bind", "listen", "urlopen", "getenv",
    }
)

PROVISIONAL_TOKENS = ("provisional",)
STDLIB = set(sys.stdlib_module_names)


@dataclass(frozen=True)
class Violation:
    file: str
    kind: str
    detail: str

    def __str__(self) -> str:
        return f"[{self.kind}] {self.file}: {self.detail}"


def _top(name: str) -> str:
    return (name or "").split(".")[0]


def scan_source(src: str, filename: str) -> list[Violation]:
    out: list[Violation] = []
    tree = ast.parse(src, filename=filename)

    for node in ast.walk(tree):
        # Imports ---------------------------------------------------------- #
        if isinstance(node, ast.Import):
            for alias in node.names:
                out += _classify_import(alias.name, filename)
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                # Relative (internal package) import — allowed.
                if node.module and "provisional" in node.module:
                    out.append(Violation(filename, "provisional-import", node.module))
                continue
            module = node.module or ""
            out += _classify_import(module, filename)
        # Dynamic import --------------------------------------------------- #
        elif isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id == "__import__":
                out.append(Violation(filename, "dynamic-import", "__import__()"))
            if isinstance(fn, ast.Attribute):
                if fn.attr == "import_module":
                    out.append(Violation(filename, "dynamic-import", "importlib.import_module()"))
                if fn.attr in FORBIDDEN_CALL_ATTRS:
                    base = getattr(fn.value, "id", getattr(fn.value, "attr", "?"))
                    out.append(
                        Violation(filename, "deployment-surface", f"{base}.{fn.attr}()")
                    )
        # Forbidden entrypoint -------------------------------------------- #
        elif isinstance(node, ast.If):
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
            ):
                out.append(Violation(filename, "entrypoint", 'if __name__ == "__main__"'))
    return out


def _classify_import(module: str, filename: str) -> list[Violation]:
    top = _top(module)
    if not top:
        return []
    if any(tok in module for tok in PROVISIONAL_TOKENS):
        return [Violation(filename, "provisional-import", module)]
    if top == "xfactory":
        return []  # internal
    if top in PROVIDER_SDKS:
        return [Violation(filename, "provider-sdk", module)]
    if top in FORBIDDEN_STDLIB:
        return [Violation(filename, "forbidden-stdlib", module)]
    if top not in STDLIB:
        return [Violation(filename, "third-party-import", module)]
    return []


def scan_package(pkg_dir: Path) -> list[Violation]:
    """Scan every .py in the runtime package + flag non-.py deployment files."""
    out: list[Violation] = []
    for path in sorted(Path(pkg_dir).rglob("*.py")):
        rel = str(path.relative_to(pkg_dir.parent.parent))
        out += scan_source(path.read_text(), rel)
    # File surface: no deployment manifests / Dockerfiles inside the package.
    for path in Path(pkg_dir).rglob("*"):
        name = path.name.lower()
        if name in ("dockerfile", "procfile") or name.endswith((".service", ".tf")):
            out.append(Violation(str(path), "deployment-file", name))
    return out


def find_provisional_imports(pkg_dir: Path) -> list[Violation]:
    return [v for v in scan_package(pkg_dir) if v.kind == "provisional-import"]


# --------------------------------------------------------------------------- #
# Test-suite hygiene (SC-004): tests must not use wall-time/randomness/network.
# --------------------------------------------------------------------------- #
HYGIENE_IMPORTS = frozenset({"random", "socket", "requests", "urllib", "secrets"})
HYGIENE_ATTRS = {("time", "time"), ("time", "sleep"), ("datetime", "now"), ("os", "urandom")}


def scan_test_hygiene(tests_dir: Path) -> list[Violation]:
    out: list[Violation] = []
    for path in sorted(Path(tests_dir).glob("test_*.py")):
        tree = ast.parse(path.read_text(), filename=path.name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    if _top(a.name) in HYGIENE_IMPORTS:
                        out.append(Violation(path.name, "test-hygiene", f"import {a.name}"))
            elif isinstance(node, ast.ImportFrom) and not (node.level or 0):
                if _top(node.module or "") in HYGIENE_IMPORTS:
                    out.append(Violation(path.name, "test-hygiene", f"from {node.module}"))
            elif isinstance(node, ast.Attribute):
                base = getattr(node.value, "id", None)
                if base and (base, node.attr) in HYGIENE_ATTRS:
                    out.append(Violation(path.name, "test-hygiene", f"{base}.{node.attr}"))
    return out
