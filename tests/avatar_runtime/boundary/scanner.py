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
        # Filesystem persistence surfaces: a reference package holds no state on
        # disk, so directory/temp/file-tree modules are forbidden (FR-001, SC-009).
        "pathlib", "tempfile", "shutil",
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

# Attribute call surfaces that write to disk (file persistence, FR-001/SC-009).
FILE_WRITE_ATTRS = frozenset({"write_text", "write_bytes", "mkdir", "makedirs"})
# File-mode strings are drawn from this alphabet; any of these chars means write.
_MODE_ALPHABET = frozenset("rwxabt+U")
_WRITE_MODE_CHARS = frozenset("wax+")

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


def _has_write_mode(call: ast.Call, mode_pos: int = 1) -> bool:
    """True if an ``open``/``Path.open`` call requests a write mode.

    Only the ARGUMENT that actually carries the mode is inspected — the mode is
    positional index ``mode_pos`` (1 for builtin ``open(file, mode)``; 0 for a
    bound ``Path.open(mode)``) or the ``mode=`` keyword. The filename positional
    is never treated as a mode, so ``open("x")`` (read-only, even when the path
    happens to be spelled with mode-alphabet chars) is not misflagged. A value is
    a file mode iff every char is in the mode alphabet, and it is a write mode iff
    it contains any of ``w``/``a``/``x``/``+``. Read-only (``'r'``/``'rb'``) and
    non-mode strings (paths) are ignored, keeping detection deterministic.
    """
    candidates = []
    if len(call.args) > mode_pos:
        candidates.append(call.args[mode_pos])
    candidates += [kw.value for kw in call.keywords if kw.arg == "mode"]
    for arg in candidates:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            chars = set(arg.value)
            if arg.value and chars <= _MODE_ALPHABET and chars & _WRITE_MODE_CHARS:
                return True
    return False


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
                # Relative (internal package) import — allowed, except the
                # provisional seam. The name may live in ``node.module``
                # (``from .provisional import x``) OR in the imported aliases
                # (``from . import provisional``, where ``node.module`` is None).
                if node.module and "provisional" in node.module:
                    out.append(Violation(filename, "provisional-import", node.module))
                else:
                    for alias in node.names:
                        if "provisional" in alias.name:
                            out.append(
                                Violation(filename, "provisional-import", f".{alias.name}")
                            )
                            break
                continue
            module = node.module or ""
            out += _classify_import(module, filename)
        # Dynamic import + persistence surfaces ---------------------------- #
        elif isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name):
                if fn.id == "__import__":
                    out.append(Violation(filename, "dynamic-import", "__import__()"))
                elif fn.id == "open" and _has_write_mode(node):
                    out.append(Violation(filename, "file-persistence", "open(..., write mode)"))
            if isinstance(fn, ast.Attribute):
                base = getattr(fn.value, "id", getattr(fn.value, "attr", "?"))
                if fn.attr == "import_module":
                    out.append(Violation(filename, "dynamic-import", "importlib.import_module()"))
                if fn.attr in FORBIDDEN_CALL_ATTRS:
                    out.append(
                        Violation(filename, "deployment-surface", f"{base}.{fn.attr}()")
                    )
                if fn.attr in FILE_WRITE_ATTRS:
                    out.append(Violation(filename, "file-persistence", f"{base}.{fn.attr}()"))
                elif fn.attr == "open" and (base == "os" or _has_write_mode(node, mode_pos=0)):
                    out.append(Violation(filename, "file-persistence", f"{base}.open()"))
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
# (base, attr) wall-clock/nondeterminism surfaces. ``base`` may be a bare module
# name (``time.time``) or the leaf of a dotted base (``datetime.datetime.now``).
HYGIENE_ATTRS = {
    ("time", "time"), ("time", "sleep"),
    ("time", "monotonic"), ("time", "perf_counter"),
    ("datetime", "now"), ("datetime", "utcnow"), ("datetime", "today"),
    ("os", "urandom"),
}
# Bare-name calls that read wall-clock time (e.g. ``from time import time``).
HYGIENE_NAMES = frozenset({"time", "monotonic", "perf_counter"})


def scan_hygiene_source(src: str, filename: str) -> list[Violation]:
    """Flag wall-time / randomness / network idioms in one test source string."""
    out: list[Violation] = []
    tree = ast.parse(src, filename=filename)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if _top(a.name) in HYGIENE_IMPORTS:
                    out.append(Violation(filename, "test-hygiene", f"import {a.name}"))
        elif isinstance(node, ast.ImportFrom) and not (node.level or 0):
            if _top(node.module or "") in HYGIENE_IMPORTS:
                out.append(Violation(filename, "test-hygiene", f"from {node.module}"))
        elif isinstance(node, ast.Attribute):
            # ``time.time`` -> base is a Name; ``datetime.datetime.now`` -> the
            # base is itself an Attribute (use its leaf ``attr``).
            val = node.value
            base = getattr(val, "id", None)
            if base is None and isinstance(val, ast.Attribute):
                base = val.attr
            if base and (base, node.attr) in HYGIENE_ATTRS:
                out.append(Violation(filename, "test-hygiene", f"{base}.{node.attr}"))
        elif isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id in HYGIENE_NAMES:
                out.append(Violation(filename, "test-hygiene", f"{fn.id}()"))
    return out


def scan_test_hygiene(tests_dir: Path) -> list[Violation]:
    """Scan ALL test sources recursively — conftest, _support, fakes, boundary,
    conformance, and every ``*.py`` — not just top-level ``test_*.py``."""
    out: list[Violation] = []
    root = Path(tests_dir)
    for path in sorted(root.rglob("*.py")):
        rel = str(path.relative_to(root))
        out += scan_hygiene_source(path.read_text(), rel)
    return out
