from __future__ import annotations

import configparser
from pathlib import Path, PurePosixPath

import tomllib

from scripts.hermes_runtime_validation.pytest_source import read_optional_bounded_text

ALLOWED_COLLECTION_OPTIONS = frozenset({"markers"})


def pytest_config_supported(repo_root: Path) -> bool:
    if not _pytest_ini_supported(repo_root):
        return False
    if not _legacy_ini_supported(repo_root, PurePosixPath("setup.cfg"), "tool:pytest"):
        return False
    if not _legacy_ini_supported(repo_root, PurePosixPath("tox.ini"), "pytest"):
        return False
    return _pyproject_supported(repo_root)


def _pytest_ini_supported(repo_root: Path) -> bool:
    present, source = read_optional_bounded_text(
        repo_root, PurePosixPath("pytest.ini")
    )
    if not present:
        return True
    return source is not None and _ini_section_supported(source, "pytest", required=True)


def _legacy_ini_supported(
    repo_root: Path, path: PurePosixPath, section: str
) -> bool:
    present, source = read_optional_bounded_text(repo_root, path)
    if not present:
        return True
    return source is not None and _ini_section_supported(source, section, required=False)


def _ini_section_supported(source: str, section: str, *, required: bool) -> bool:
    parser = configparser.ConfigParser(interpolation=None)
    try:
        parser.read_string(source)
    except configparser.Error:
        return False
    if not parser.has_section(section):
        return not required
    return set(parser[section]) <= ALLOWED_COLLECTION_OPTIONS


def _pyproject_supported(repo_root: Path) -> bool:
    present, source = read_optional_bounded_text(
        repo_root, PurePosixPath("pyproject.toml")
    )
    if not present:
        return True
    if source is None:
        return False
    try:
        document = tomllib.loads(source)
        options = document.get("tool", {}).get("pytest", {}).get("ini_options", {})
    except (AttributeError, tomllib.TOMLDecodeError):
        return False
    return isinstance(options, dict) and set(options) <= ALLOWED_COLLECTION_OPTIONS
