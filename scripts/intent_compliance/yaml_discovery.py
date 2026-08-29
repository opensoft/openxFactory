from __future__ import annotations

import yaml
from yaml.events import (
    AliasEvent,
    CollectionEndEvent,
    CollectionStartEvent,
    DocumentStartEvent,
    MappingStartEvent,
    ScalarEvent,
)


def governed_kind_before_error(text: str, governed_kinds: tuple[str, ...]) -> bool:
    depth = 0
    root_mapping = False
    expecting_key = False
    kind_key = False
    try:
        for event in yaml.parse(text):
            if isinstance(event, DocumentStartEvent):
                depth = 0
                root_mapping = False
                expecting_key = False
                kind_key = False
            elif isinstance(event, CollectionStartEvent):
                if depth == 0:
                    root_mapping = isinstance(event, MappingStartEvent)
                    expecting_key = root_mapping
                depth += 1
            elif isinstance(event, CollectionEndEvent):
                depth -= 1
                if root_mapping and depth == 1 and not expecting_key:
                    expecting_key = True
                    kind_key = False
            elif root_mapping and depth == 1 and isinstance(event, ScalarEvent):
                if expecting_key:
                    kind_key = event.value == "kind"
                    if event.value == "<<":
                        return True
                    expecting_key = False
                else:
                    if kind_key and event.value in governed_kinds:
                        return True
                    expecting_key = True
                    kind_key = False
            elif root_mapping and depth == 1 and isinstance(event, AliasEvent):
                if expecting_key:
                    return True
                if kind_key:
                    return True
                expecting_key = True
                kind_key = False
    except yaml.YAMLError:
        return False
    return False
