from __future__ import annotations

import os
import stat
from pathlib import Path

from .records import InputLimitError

MAX_INPUT_BYTES = 1_048_576


def _open_without_symlinks(path: Path) -> int:
    absolute = Path(os.path.abspath(path))
    components = absolute.parts[1:]
    if not components:
        raise InputLimitError(path, "input must be a regular file")
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
    directory = os.open("/", directory_flags)
    try:
        for component in components[:-1]:
            child = os.open(component, directory_flags, dir_fd=directory)
            os.close(directory)
            directory = child
        return os.open(components[-1], file_flags, dir_fd=directory)
    except FileNotFoundError as error:
        raise InputLimitError(path, "input does not exist") from error
    except OSError as error:
        raise InputLimitError(path, "input must be a regular file") from error
    finally:
        os.close(directory)


def _open_regular(path: Path) -> tuple[int, int]:
    descriptor = _open_without_symlinks(path)
    try:
        metadata = os.fstat(descriptor)
    except OSError as error:
        os.close(descriptor)
        raise InputLimitError(path, "input must be a regular file") from error
    if not stat.S_ISREG(metadata.st_mode):
        os.close(descriptor)
        raise InputLimitError(path, "input must be a regular file")
    if metadata.st_size > MAX_INPUT_BYTES:
        os.close(descriptor)
        raise InputLimitError(path, f"input exceeds {MAX_INPUT_BYTES} byte limit")
    return descriptor, metadata.st_size


def regular_file_size(path: Path) -> int:
    descriptor, size = _open_regular(path)
    os.close(descriptor)
    return size


def require_directory_without_symlinks(path: Path) -> None:
    absolute = Path(os.path.abspath(path))
    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )
    descriptor = os.open("/", flags)
    try:
        for component in absolute.parts[1:]:
            child = os.open(component, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
    except FileNotFoundError as error:
        raise InputLimitError(path, "target does not exist") from error
    except OSError as error:
        raise InputLimitError(
            path, "target must be a directory without symlinks"
        ) from error
    finally:
        os.close(descriptor)


def bounded_yaml_text(path: Path, *, size: int | None = None) -> str:
    descriptor, observed_size = _open_regular(path)
    try:
        if size is not None and observed_size != size:
            raise InputLimitError(path, "input changed after preflight")
        with os.fdopen(descriptor, "rb", closefd=True) as stream:
            descriptor = -1
            content = stream.read(MAX_INPUT_BYTES + 1)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if len(content) > MAX_INPUT_BYTES:
        raise InputLimitError(path, f"input exceeds {MAX_INPUT_BYTES} byte limit")
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise InputLimitError(path, "input must be valid UTF-8") from error
