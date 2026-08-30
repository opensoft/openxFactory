from __future__ import annotations

import ast
import os
import stat
from pathlib import Path, PurePosixPath

MAX_TEST_SOURCE_BYTES = 1_048_576


def read_optional_bounded_text(
    repo_root: Path, relative: PurePosixPath
) -> tuple[bool, str | None]:
    try:
        return True, _read_regular_source(repo_root, relative)
    except FileNotFoundError:
        return False, None
    except (OSError, UnicodeError, ValueError):
        return True, None


def parse_optional_bounded_module(
    repo_root: Path, relative: PurePosixPath
) -> tuple[bool, ast.Module | None]:
    present, source = read_optional_bounded_text(repo_root, relative)
    if not present or source is None:
        return present, None
    try:
        return True, ast.parse(source, filename=relative.as_posix())
    except SyntaxError:
        return True, None


def parse_bounded_module(repo_root: Path, relative: PurePosixPath) -> ast.Module | None:
    return parse_optional_bounded_module(repo_root, relative)[1]


def _read_regular_source(repo_root: Path, relative: PurePosixPath) -> str:
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    file_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    directory = os.open(repo_root, directory_flags)
    descriptor: int | None = None
    try:
        for component in relative.parts[:-1]:
            child = os.open(component, directory_flags, dir_fd=directory)
            os.close(directory)
            directory = child
        descriptor = os.open(relative.name, file_flags, dir_fd=directory)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_TEST_SOURCE_BYTES:
            raise ValueError("test source must be a bounded regular file")
        chunks: list[bytes] = []
        remaining = MAX_TEST_SOURCE_BYTES + 1
        while remaining > 0:
            chunk = os.read(descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > MAX_TEST_SOURCE_BYTES:
            raise ValueError("test source exceeds the byte limit")
        return payload.decode("utf-8")
    finally:
        if descriptor is not None:
            os.close(descriptor)
        os.close(directory)
