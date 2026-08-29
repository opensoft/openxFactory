from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Final

from .model import (
    MAX_DISCOVERY_DEPTH,
    MAX_DISCOVERY_FILES,
    MAX_ELIGIBLE_INPUT_FILES,
    MAX_TOTAL_INPUT_BYTES,
    InputLimitError,
    RecordDocument,
    bounded_yaml_text,
    declares_governed_kind,
    load_record_document_texts,
    regular_file_size,
    require_directory_without_symlinks,
)

GOVERNED_KINDS: Final = (
    "veto_class_vocabulary",
    "policy_allowance",
    "policy_allowance_revocation",
    "policy_allowance_registry",
    "compliance_decision",
)
def discover_record_documents(paths: list[Path]) -> list[RecordDocument]:
    sizes: list[tuple[Path, int]] = []
    total_bytes = 0
    for path in paths:
        size = regular_file_size(path)
        total_bytes += size
        if total_bytes > MAX_TOTAL_INPUT_BYTES:
            raise InputLimitError(
                path, f"aggregate discovery input exceeds {MAX_TOTAL_INPUT_BYTES} bytes"
            )
        sizes.append((path, size))
    inputs = [
        (bounded_yaml_text(path, size=size), path)
        for path, size in sizes
    ]
    return [
        document
        for document in load_record_document_texts(inputs)
        if document.data.get("kind") in GOVERNED_KINDS
    ]


def bounded_record_paths(target: Path) -> list[Path]:
    try:
        target_metadata = target.lstat()
    except FileNotFoundError as error:
        raise InputLimitError(target, "target does not exist") from error
    if stat.S_ISLNK(target_metadata.st_mode):
        raise InputLimitError(target, "target must not be a symlink")
    if stat.S_ISREG(target_metadata.st_mode):
        regular_file_size(target)
        return [target]
    if not stat.S_ISDIR(target_metadata.st_mode):
        raise InputLimitError(target, "target must be a regular file or directory")
    require_directory_without_symlinks(target)
    paths: list[Path] = []
    entries = 0
    scanned_yaml_bytes = 0
    for root, directories, files in os.walk(target, followlinks=False):
        root_path = Path(root)
        depth = len(root_path.relative_to(target).parts)
        if depth >= MAX_DISCOVERY_DEPTH:
            directories.clear()
        directories[:] = sorted(
            directory
            for directory in directories
            if directory != ".git" and not (root_path / directory).is_symlink()
        )
        entries += len(directories) + len(files)
        if entries > MAX_DISCOVERY_FILES:
            raise InputLimitError(
                target, f"discovery entry count exceeds {MAX_DISCOVERY_FILES}"
        )
        for name in sorted(files):
            path = root_path / name
            relative_parts = path.relative_to(target).parts
            if (
                path.suffix in {".yaml", ".yml"}
                and "examples" not in relative_parts[:-1]
                and not path.name.endswith((".schema.yaml", ".template.yaml"))
                and not path.is_symlink()
            ):
                size = regular_file_size(path)
                scanned_yaml_bytes += size
                if scanned_yaml_bytes > MAX_TOTAL_INPUT_BYTES:
                    raise InputLimitError(
                        target,
                        f"discovery YAML exceeds {MAX_TOTAL_INPUT_BYTES} bytes",
                    )
                text = bounded_yaml_text(path, size=size)
                if not declares_governed_kind(text, path, GOVERNED_KINDS):
                    continue
                paths.append(path)
                if len(paths) > MAX_ELIGIBLE_INPUT_FILES:
                    raise InputLimitError(
                        target,
                        f"eligible input count exceeds {MAX_ELIGIBLE_INPUT_FILES}",
                    )
    return paths
