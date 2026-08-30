"""Fail-closed YAML loading with JSON-compatible value semantics.

The Hermes runtime contract family is authored as YAML, but its portable
meaning is JSON.  This loader therefore rejects YAML features which can change
that meaning across implementations before returning a document.
"""

from __future__ import annotations

import math
from collections.abc import Hashable
from pathlib import Path
from typing import Any, Final

import yaml
from yaml.composer import ComposerError
from yaml.constructor import ConstructorError
from yaml.events import AliasEvent
from yaml.nodes import MappingNode

MAX_YAML_BYTES: Final = 4 * 1024 * 1024
MAX_YAML_DEPTH: Final = 128
MAX_YAML_NODES: Final = 100_000


class YamlLoadError(ValueError):
    """Raised when a document is not unambiguous JSON-compatible YAML."""

    def __init__(self, path: Path, message: str) -> None:
        self.path = Path(path)
        super().__init__(f"{self.path}: {message}")


class _StrictJsonLoader(yaml.SafeLoader):
    """SafeLoader variant which rejects aliases, anchors, merges, and dupes."""

    def compose_node(self, parent: Any, index: Any) -> Any:
        event = self.peek_event()
        if isinstance(event, AliasEvent):
            raise ComposerError(
                None,
                None,
                "YAML aliases are not permitted",
                event.start_mark,
            )
        if getattr(event, "anchor", None) is not None:
            raise ComposerError(
                None,
                None,
                "YAML anchors are not permitted",
                event.start_mark,
            )
        return super().compose_node(parent, index)

    def construct_mapping(
        self, node: MappingNode, deep: bool = False
    ) -> dict[Hashable, Any]:
        if not isinstance(node, MappingNode):
            raise ConstructorError(
                None,
                None,
                f"expected a mapping node, found {node.id}",
                node.start_mark,
            )

        result: dict[Hashable, Any] = {}
        for key_node, value_node in node.value:
            if key_node.tag == "tag:yaml.org,2002:merge":
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "YAML merge keys are not permitted",
                    key_node.start_mark,
                )
            key = self.construct_object(key_node, deep=True)
            if type(key) is not str:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "mapping keys must be strings",
                    key_node.start_mark,
                )
            if key in result:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"duplicate mapping key {key!r}",
                    key_node.start_mark,
                )
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def _reject_timestamp(loader: _StrictJsonLoader, node: Any) -> Any:
    raise ConstructorError(
        None,
        None,
        "implicit or tagged YAML timestamps are not permitted; quote timestamps",
        node.start_mark,
    )


_StrictJsonLoader.add_constructor("tag:yaml.org,2002:timestamp", _reject_timestamp)


def _check_json_value(value: Any, path: str = "$") -> None:
    """Reject every value which has no exact JSON data-model equivalent."""

    if value is None or type(value) in {str, bool, int}:
        return
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError(f"{path}: non-finite numbers are not permitted")
        return
    if type(value) is list:
        for index, item in enumerate(value):
            _check_json_value(item, f"{path}[{index}]")
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise ValueError(f"{path}: mapping keys must be strings")
            _check_json_value(item, f"{path}.{key}")
        return
    raise ValueError(f"{path}: value of type {type(value).__name__} is not JSON-compatible")


def _check_yaml_complexity(text: str, path: Path) -> None:
    depth = 0
    nodes = 0
    try:
        for event in yaml.parse(text, Loader=_StrictJsonLoader):
            event_type = type(event)
            if event_type in {yaml.MappingStartEvent, yaml.SequenceStartEvent}:
                depth += 1
                nodes += 1
            if event_type is yaml.ScalarEvent:
                nodes += 1
            if depth > MAX_YAML_DEPTH:
                raise YamlLoadError(path, f"YAML depth exceeds {MAX_YAML_DEPTH}")
            if nodes > MAX_YAML_NODES:
                raise YamlLoadError(path, f"YAML node count exceeds {MAX_YAML_NODES}")
            if event_type in {yaml.MappingEndEvent, yaml.SequenceEndEvent}:
                depth -= 1
    except yaml.YAMLError as exc:
        raise YamlLoadError(path, str(exc)) from exc


def load_yaml_bytes(data: bytes, path: str | Path) -> Any:
    source_path = Path(path)
    if len(data) > MAX_YAML_BYTES:
        raise YamlLoadError(source_path, f"document exceeds {MAX_YAML_BYTES} bytes")
    try:
        text = data.decode("utf-8")
        _check_yaml_complexity(text, source_path)
        value = yaml.load(text, Loader=_StrictJsonLoader)
        _check_json_value(value)
        return value
    except YamlLoadError:
        raise
    except (UnicodeError, yaml.YAMLError, ValueError) as exc:
        raise YamlLoadError(source_path, str(exc)) from exc


def load_yaml_document(path: str | Path) -> Any:
    """Load one YAML document or raise :class:`YamlLoadError`.

    No network, custom constructor, alias expansion, or implicit timestamp
    conversion is available.  Empty documents are returned as ``None``; callers
    which require a mapping enforce that shape at their boundary.
    """

    source_path = Path(path)
    try:
        with source_path.open("rb") as stream:
            data = stream.read(MAX_YAML_BYTES + 1)
        return load_yaml_bytes(data, source_path)
    except YamlLoadError:
        raise
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        raise YamlLoadError(source_path, str(exc)) from exc
