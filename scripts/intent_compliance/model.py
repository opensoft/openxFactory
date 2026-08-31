from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import assert_never

import yaml
from yaml.events import (
    AliasEvent,
    DocumentStartEvent,
    MappingEndEvent,
    MappingStartEvent,
    ScalarEvent,
    SequenceEndEvent,
    SequenceStartEvent,
)
from yaml.nodes import MappingNode, ScalarNode

from .input_io import (
    MAX_INPUT_BYTES,
    bounded_yaml_text,
    regular_file_size,
    require_directory_without_symlinks,
)
from .records import (
    Finding,
    InputLimitError,
    JsonValue,
    Record,
    RecordDocument,
    YamlValue,
    as_record,
    as_records,
    as_strings,
)
from .yaml_discovery import governed_kind_before_error

__all__ = [
    "MAX_INPUT_BYTES",
    "Finding",
    "InputLimitError",
    "JsonValue",
    "Record",
    "RecordDocument",
    "YamlValue",
    "as_record",
    "as_records",
    "as_strings",
    "bounded_yaml_text",
    "regular_file_size",
    "require_directory_without_symlinks",
]

MAX_DOCUMENTS = 64
MAX_DEPTH = 32
MAX_NODES = 10_000
MAX_TOTAL_INPUT_BYTES = 4_194_304
MAX_TOTAL_DOCUMENTS = 256
MAX_TOTAL_NODES = 100_000
MAX_DISCOVERY_FILES = 1_024
MAX_ELIGIBLE_INPUT_FILES = 256
MAX_DISCOVERY_DEPTH = 16


class _ClosedLoader(yaml.SafeLoader):
    pass


def _construct_mapping(
    loader: _ClosedLoader, node: MappingNode, deep: bool = False
) -> dict[str, JsonValue]:
    result: dict[str, JsonValue] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "non-string YAML key",
                key_node.start_mark,
            )
        if key in result:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "duplicate YAML key",
                key_node.start_mark,
            )
        value = loader.construct_object(value_node, deep=deep)
        result[key] = value
    return result


_ClosedLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def load_record_documents(paths: list[Path]) -> list[RecordDocument]:
    sizes: list[tuple[Path, int]] = []
    total_bytes = 0
    for path in paths:
        size = regular_file_size(path)
        total_bytes += size
        if total_bytes > MAX_TOTAL_INPUT_BYTES:
            raise InputLimitError(
                path, f"aggregate input exceeds {MAX_TOTAL_INPUT_BYTES} bytes"
            )
        sizes.append((path, size))
    return load_record_document_texts(
        [(bounded_yaml_text(path, size=size), path) for path, size in sizes]
    )


def load_record_document_texts(
    inputs: list[tuple[str, Path]],
) -> list[RecordDocument]:
    records: list[RecordDocument] = []
    total_bytes = 0
    total_nodes = 0
    for text, path in inputs:
        total_bytes += len(text.encode("utf-8"))
        if total_bytes > MAX_TOTAL_INPUT_BYTES:
            raise InputLimitError(
                path, f"aggregate input exceeds {MAX_TOTAL_INPUT_BYTES} bytes"
            )
        loaded = load_record_documents_text(text, path)
        if len(records) + len(loaded) > MAX_TOTAL_DOCUMENTS:
            raise InputLimitError(
                path,
                f"aggregate document count exceeds {MAX_TOTAL_DOCUMENTS}",
            )
        total_nodes += sum(_assert_bounded_tree(item.path, item.data) for item in loaded)
        if total_nodes > MAX_TOTAL_NODES:
            raise InputLimitError(
                path, f"aggregate node count exceeds {MAX_TOTAL_NODES}"
            )
        records.extend(loaded)
    return records


def load_record_documents_text(text: str, source: Path) -> list[RecordDocument]:
    if len(text.encode("utf-8")) > MAX_INPUT_BYTES:
        raise InputLimitError(source, f"input exceeds {MAX_INPUT_BYTES} byte limit")
    _preflight_yaml(source, text, max_documents=MAX_DOCUMENTS)
    records: list[RecordDocument] = []
    try:
        for index, raw_document in enumerate(
            yaml.load_all(text, Loader=_ClosedLoader), start=1
        ):
            if index > MAX_DOCUMENTS:
                raise InputLimitError(source, f"document count exceeds {MAX_DOCUMENTS}")
            if not isinstance(raw_document, dict):
                raise InputLimitError(source, f"document {index} must be a mapping")
            _assert_bounded_tree(source, raw_document)
            records.append(RecordDocument(path=source, data=raw_document))
    except yaml.YAMLError as error:
        raise InputLimitError(source, _yaml_error_detail(error)) from error
    return records


def load_single_mapping_text(text: str, source: Path) -> Record:
    if len(text.encode("utf-8")) > MAX_INPUT_BYTES:
        raise InputLimitError(source, f"input exceeds {MAX_INPUT_BYTES} byte limit")
    _preflight_yaml(source, text, max_documents=1)
    try:
        documents = list(yaml.load_all(text, Loader=_ClosedLoader))
    except yaml.YAMLError as error:
        raise InputLimitError(source, _yaml_error_detail(error)) from error
    if len(documents) != 1 or not isinstance(documents[0], dict):
        raise InputLimitError(source, "authority source must contain one mapping document")
    record = documents[0]
    _assert_bounded_tree(source, record)
    return record


def declares_governed_kind(
    text: str, source: Path, governed_kinds: tuple[str, ...]
) -> bool:
    try:
        _preflight_yaml(source, text, max_documents=MAX_DOCUMENTS)
        documents = yaml.compose_all(text, Loader=_ClosedLoader)
        for document in documents:
            if not isinstance(document, MappingNode):
                continue
            for key_node, value_node in document.value:
                if (
                    isinstance(key_node, ScalarNode)
                    and key_node.value == "kind"
                    and isinstance(value_node, ScalarNode)
                    and value_node.value in governed_kinds
                ):
                    return True
    except (InputLimitError, yaml.YAMLError):
        if governed_kind_before_error(text, governed_kinds):
            return True
        kinds = "|".join(re.escape(kind) for kind in governed_kinds)
        return (
            re.search(
                rf'(?m)^kind:[ \t]*(?:"(?:{kinds})"|\'(?:{kinds})\'|(?:{kinds}))[ \t]*(?:#.*)?$',
                text,
            )
            is not None
        )
    return False


def _preflight_yaml(path: Path, text: str, *, max_documents: int) -> None:
    documents = 0
    nodes = 0
    depth = 0
    try:
        for event in yaml.parse(text):
            if isinstance(event, AliasEvent):
                raise InputLimitError(path, "YAML aliases are forbidden")
            if isinstance(event, DocumentStartEvent):
                documents += 1
                nodes = 0
                depth = 0
                if documents > max_documents:
                    raise InputLimitError(
                        path, f"document count exceeds {max_documents}"
                    )
                continue
            if isinstance(event, (MappingStartEvent, SequenceStartEvent)):
                nodes += 1
                depth += 1
                if depth > MAX_DEPTH:
                    raise InputLimitError(path, f"document exceeds depth {MAX_DEPTH}")
            elif isinstance(event, (MappingEndEvent, SequenceEndEvent)):
                depth -= 1
            elif isinstance(event, ScalarEvent):
                nodes += 1
                if depth + 1 > MAX_DEPTH:
                    raise InputLimitError(path, f"document exceeds depth {MAX_DEPTH}")
            if nodes > MAX_NODES:
                raise InputLimitError(path, f"document exceeds {MAX_NODES} nodes")
    except yaml.YAMLError as error:
        raise InputLimitError(path, _yaml_error_detail(error)) from error


def _assert_bounded_tree(path: Path, value: YamlValue) -> int:
    stack: list[tuple[YamlValue, int]] = [(value, 1)]
    nodes = 0
    while stack:
        child, depth = stack.pop()
        nodes += 1
        if nodes > MAX_NODES:
            raise InputLimitError(path, f"document exceeds {MAX_NODES} nodes")
        if depth > MAX_DEPTH:
            raise InputLimitError(path, f"document exceeds depth {MAX_DEPTH}")
        match child:
            case dict():
                stack.extend((item, depth + 1) for item in child.values())
            case list():
                stack.extend((item, depth + 1) for item in child)
            case None | bool() | int() | str():
                pass
            case float():
                raise InputLimitError(
                    path, "canonical records allow integers only; floats are forbidden"
                )
            case bytes() | date() | set() | tuple():
                raise InputLimitError(path, "canonical records require JSON-native values")
            case unreachable:
                assert_never(unreachable)
    return nodes


def _yaml_error_detail(error: yaml.YAMLError) -> str:
    problem = getattr(error, "problem", None)
    if problem in {"duplicate YAML key", "non-string YAML key"}:
        return str(problem)
    return "invalid YAML"
