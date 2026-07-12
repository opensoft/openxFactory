"""Static boundary: no deployment surface, stdlib-only, no provisional import
(ARR-001-S01, ARR-002-S02, FR-001/004, SC-005/010)."""

from __future__ import annotations

from pathlib import Path

from boundary.scanner import scan_package, scan_source

ROOT = Path(__file__).resolve().parents[3]
PKG = ROOT / "xfactory" / "avatar_runtime"


def test_no_deployment_surface_or_third_party():
    violations = scan_package(PKG)
    assert violations == [], "\n".join(str(v) for v in violations)


def test_runtime_is_stdlib_only():
    kinds = {v.kind for v in scan_package(PKG)}
    assert "third-party-import" not in kinds
    assert "provider-sdk" not in kinds
    assert "forbidden-stdlib" not in kinds


def test_no_module_imports_the_provisional_path():
    provisional = [v for v in scan_package(PKG) if v.kind == "provisional-import"]
    assert provisional == []


# --- Negative controls: prove the scanner actually catches violations ----- #
def test_scanner_flags_provisional_import():
    v = scan_source("from provisional import baseline_acr_ids\n", "x.py")
    assert any(x.kind == "provisional-import" for x in v)


def test_scanner_flags_bare_relative_provisional_import():
    # ``from . import provisional`` — node.module is None; the seam name lives in
    # the imported aliases, which the scanner must still inspect.
    v = scan_source("from . import provisional\n", "x.py")
    assert any(x.kind == "provisional-import" for x in v)


def test_scanner_flags_file_persistence():
    for src in (
        "open('/tmp/x', 'w')\n",
        "open('/tmp/x', mode='ab')\n",
        "import pathlib\npathlib.Path('x').write_text('y')\n",
        "import pathlib\npathlib.Path('x').write_bytes(b'y')\n",
        "import pathlib\npathlib.Path('x').open('w')\n",
        "import os\nos.mkdir('d')\n",
        "import os\nos.makedirs('d')\n",
        "import os\nos.open('f', 0)\n",
    ):
        kinds = {x.kind for x in scan_source(src, "x.py")}
        assert "file-persistence" in kinds, f"missed persistence:\n{src}"


def test_scanner_ignores_read_open():
    # Read-only open() is not a persistence surface — including the adversarial
    # case where the FILENAME is spelled entirely with mode-alphabet chars
    # (e.g. "x", "wa", "r+"). The filename positional must never be read as a
    # mode; only open()'s 2nd positional / mode= kwarg is the mode.
    for src in (
        "open('/tmp/x')\n",
        "open('/tmp/x', 'r')\n",
        "open('x')\n",            # filename 'x' is a write-mode char but is a PATH here
        "open('wa')\n",
        "open('r+')\n",
        "open('x', 'r')\n",
        "open('x', mode='rb')\n",
    ):
        kinds = {x.kind for x in scan_source(src, "x.py")}
        assert "file-persistence" not in kinds, f"false positive on read-only open:\n{src}"


def test_scanner_flags_persistence_module_imports():
    kinds = {x.kind for x in scan_source("import pathlib\nimport tempfile\nimport shutil\n", "x.py")}
    assert kinds == {"forbidden-stdlib"}


def test_scanner_flags_network_and_provider_sdk():
    v = scan_source("import socket\nimport openai\n", "x.py")
    kinds = {x.kind for x in v}
    assert "forbidden-stdlib" in kinds and "provider-sdk" in kinds


def test_scanner_flags_entrypoint_and_dynamic_import():
    src = "import importlib\ndef f():\n    importlib.import_module('x')\nif __name__ == '__main__':\n    f()\n"
    kinds = {x.kind for x in scan_source(src, "x.py")}
    assert "dynamic-import" in kinds and "entrypoint" in kinds
