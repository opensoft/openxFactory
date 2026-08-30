from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Protocol

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode

from .models import Finding, HarnessError, RawYaml, RelativePath, YamlValue


class SafeYamlLoader(Protocol):
    def __call__(self, stream: str) -> RawYaml: ...


class SafeYamlNodeLoader(Protocol):
    def get_single_node(self) -> Node | None: ...

    def dispose(self) -> None: ...


class MappingNodeView(Protocol):
    value: list[tuple[Node, Node]]


class SequenceNodeView(Protocol):
    value: list[Node]


class ScalarNodeView(Protocol):
    tag: str
    value: str


safe_yaml_load: SafeYamlLoader = yaml.safe_load


def _load_single_node(loader: SafeYamlNodeLoader) -> Node | None:
    try:
        return loader.get_single_node()
    finally:
        loader.dispose()


def _compose_yaml(stream: str) -> Node | None:
    return _load_single_node(yaml.SafeLoader(stream))


def _mapping_children(node: MappingNodeView) -> tuple[tuple[Node, Node], ...]:
    return tuple(node.value)


def _sequence_children(node: SequenceNodeView) -> tuple[Node, ...]:
    return tuple(node.value)


def _scalar_identity(node: ScalarNodeView) -> tuple[str, str]:
    return node.tag, node.value


def _merge_mapping_nodes(node: Node) -> tuple[MappingNode, ...]:
    if isinstance(node, MappingNode):
        return (node,)
    if isinstance(node, SequenceNode):
        return tuple(
            item for item in _sequence_children(node) if isinstance(item, MappingNode)
        )
    return ()


def _mapping_key_identities(
    node: MappingNode,
    path: RelativePath,
) -> set[tuple[str, str]]:
    scalar_keys: set[tuple[str, str]] = set()
    for key_node, value_node in _mapping_children(node):
        if (
            isinstance(key_node, ScalarNode)
            and key_node.tag == "tag:yaml.org,2002:merge"
        ):
            identity = _scalar_identity(key_node)
            if identity in scalar_keys:
                raise HarnessError(
                    Finding(
                        "CC-YAML-SHAPE",
                        "error",
                        "YAML mapping keys must be unique",
                        path=path,
                    )
                )
            scalar_keys.add(identity)
            for merged_node in _merge_mapping_nodes(value_node):
                for identity in _mapping_key_identities(merged_node, path):
                    if identity in scalar_keys:
                        raise HarnessError(
                            Finding(
                                "CC-YAML-SHAPE",
                                "error",
                                "YAML mapping keys must be unique",
                                path=path,
                            )
                        )
                    scalar_keys.add(identity)
        elif isinstance(key_node, ScalarNode):
            identity = _scalar_identity(key_node)
            if identity in scalar_keys:
                raise HarnessError(
                    Finding(
                        "CC-YAML-SHAPE",
                        "error",
                        "YAML mapping keys must be unique",
                        path=path,
                    )
                )
            scalar_keys.add(identity)
    return scalar_keys


def _reject_duplicate_keys(node: Node | None, path: RelativePath) -> None:
    if isinstance(node, MappingNode):
        _ = _mapping_key_identities(node, path)
        for key_node, value_node in _mapping_children(node):
            _reject_duplicate_keys(key_node, path)
            _reject_duplicate_keys(value_node, path)
        return
    if isinstance(node, SequenceNode):
        for item in _sequence_children(node):
            _reject_duplicate_keys(item, path)


def normalize_yaml(value: RawYaml, path: RelativePath) -> YamlValue:
    if isinstance(value, date):
        raise HarnessError(
            Finding(
                "CC-YAML-SHAPE",
                "error",
                "YAML values must use portable scalar types",
                path=path,
            )
        )
    if value is None or isinstance(value, str | bool | int | float):
        return value
    if isinstance(value, list):
        return [normalize_yaml(item, path) for item in value]
    normalized: dict[str, YamlValue] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise HarnessError(
                Finding(
                    "CC-YAML-SHAPE",
                    "error",
                    "YAML mapping keys must be strings",
                    path=path,
                )
            )
        normalized[key] = normalize_yaml(item, path)
    return normalized


def load_yaml(path: Path, relative_path: RelativePath) -> dict[str, YamlValue]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError as error:
        raise HarnessError(
            Finding(
                "CC-DOCUMENT-ENCODING",
                "error",
                str(error),
                path=relative_path,
            )
        ) from error
    except OSError as error:
        raise HarnessError(
            Finding(
                "CC-DOCUMENT-UNAVAILABLE",
                "error",
                str(error),
                path=relative_path,
            )
        ) from error
    try:
        _reject_duplicate_keys(_compose_yaml(text), relative_path)
        loaded = safe_yaml_load(text)
        normalized = normalize_yaml(loaded, relative_path)
    except RecursionError as error:
        raise HarnessError(
            Finding(
                "CC-YAML-SHAPE",
                "error",
                "YAML document nesting or aliases exceed supported recursion",
                path=relative_path,
            )
        ) from error
    except yaml.YAMLError as error:
        raise HarnessError(
            Finding(
                "CC-DOCUMENT-YAML",
                "error",
                str(error),
                path=relative_path,
            )
        ) from error
    if not isinstance(normalized, dict):
        raise HarnessError(
            Finding(
                "CC-YAML-SHAPE",
                "error",
                "YAML document root must be a mapping",
                path=relative_path,
            )
        )
    return normalized


def mapping(value: YamlValue, label: str, path: RelativePath) -> dict[str, YamlValue]:
    if not isinstance(value, dict):
        raise HarnessError(
            Finding(
                "CC-DOCUMENT-SHAPE",
                "error",
                f"{label} must be a mapping",
                path=path,
            )
        )
    return value


def string(value: YamlValue, label: str, path: RelativePath) -> str:
    if not isinstance(value, str) or not value:
        raise HarnessError(
            Finding(
                "CC-DOCUMENT-SHAPE",
                "error",
                f"{label} must be a non-empty string",
                path=path,
            )
        )
    return value


def string_tuple(value: YamlValue, label: str, path: RelativePath) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise HarnessError(
            Finding(
                "CC-DOCUMENT-SHAPE",
                "error",
                f"{label} must be a list",
                path=path,
            )
        )
    strings: list[str] = []
    for item in value:
        strings.append(string(item, label, path))
    return tuple(strings)
