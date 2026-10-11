"""The closed predicate registry's semantics (data-model E3; research R5).

Written from the family's own specification and from nothing else: no code is
copied from codexFactory (research R4). The identifiers are the ones the
governed rule files declare, with no mapping layer, under Brett Heap's OPEN-5
ruling of 2026-10-08, "Keep the existing names (Recommended)".

Two entry points carry the evaluation order's two predicate steps:

* `check_condition` is E2 step 8, judged on the condition alone:
  `predicate_unknown`, then `predicate_parameters_malformed` for a predicate run
  against another input contract, for parameters that are not exactly the
  predicate's one member holding 1 to 256 patterns, or for a pattern outside the
  grammar.
* `evaluate` is E2 step 10's evaluation over the authoritative facts:
  `condition_unevaluable` when a read fact is absent, outside its input
  contract, or incomplete; then `predicate_parameters_malformed` by the
  bare-directory evidence rule; otherwise whether any read path matches any
  pattern. Unevaluable is never false: it raises, it never returns False.

THE REGISTRY INSTANCE IS CLOSED BY THIS MODULE. `RATIFIED_REGISTRY` is the
ratified content of `contracts/council-convening/predicate.registry.yaml` with
its prose removed, and `registry_findings` refuses an instance that differs
from it in any member (`council-convening-registry-closure`), beside the
instance's schema findings, in the protocol registry's `(code, message)` form. The semantics
below read the frozen constants, never the instance, so an edited instance can
change nothing except the finding it raises.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from . import records
from .records import Refused

REGISTRY_REL = records.FAMILY_REL / "predicate.registry.yaml"
REGISTRY_SCHEMA_ID = records.ID_BASE + "predicate-registry.schema.yaml"
REGISTRY_KIND = "xfactory_council_predicate_registry"

PR_FACTS = "pr_facts"
RULE_FACTS = "rule_facts"

#: Every fact of each input contract, in the registry's order.
INPUT_CONTRACTS: Mapping[str, tuple[str, ...]] = {
    PR_FACTS: ("changed_paths", "changed_files_total", "changed_paths_entry_count"),
    RULE_FACTS: ("rule_touched_paths",),
}

#: A path list holds at most 6000 paths: the 3000-entry listing bound, which a
#: rename (one entry, two paths) can double.
MAX_PATHS = 6000
#: The producer's listing bound. A declared total above it is a listing the
#: gather cannot complete, so the fact set is unevaluable rather than read short.
MAX_LISTING_ENTRIES = 3000
MIN_PATTERNS = 1
MAX_PATTERNS = 256
TREE_SUFFIX = "/**"
_WILDCARDS = ("*", "?", "[")

_PATH_LISTS = frozenset({"changed_paths", "rule_touched_paths"})
_COUNTS = frozenset({"changed_files_total", "changed_paths_entry_count"})


@dataclass(frozen=True)
class PredicateSpec:
    predicate: str
    input_contract: str
    parameter: str
    reads: tuple[str, ...]
    path_fact: str


PREDICATES: Mapping[str, PredicateSpec] = {
    "changed_paths_intersect": PredicateSpec(
        predicate="changed_paths_intersect",
        input_contract=PR_FACTS,
        parameter="protected_paths",
        reads=INPUT_CONTRACTS[PR_FACTS],
        path_fact="changed_paths",
    ),
    "rule_touches_security_posture": PredicateSpec(
        predicate="rule_touches_security_posture",
        input_contract=RULE_FACTS,
        parameter="security_surfaces",
        reads=INPUT_CONTRACTS[RULE_FACTS],
        path_fact="rule_touched_paths",
    ),
}

#: The ratified registry instance, with every `description` removed. A change
#: to it is a governed contract change, never an edit here alone.
RATIFIED_REGISTRY: Mapping[str, Any] = {
    "schema_version": 1,
    "kind": "xfactory_council_predicate_registry",
    "registry_id": "council-convening-predicate-registry",
    "registry_version": 1,
    "input_contracts": [
        {"input_contract": PR_FACTS,
         "facts": [
             {"fact": "changed_paths", "value": "path_list", "max_items": MAX_PATHS},
             {"fact": "changed_files_total", "value": "count"},
             {"fact": "changed_paths_entry_count", "value": "count",
              "maximum": MAX_LISTING_ENTRIES},
         ],
         "completeness": {"rule": "entry_count_equals_total",
                          "count_fact": "changed_paths_entry_count",
                          "total_fact": "changed_files_total",
                          "total_maximum": MAX_LISTING_ENTRIES}},
        {"input_contract": RULE_FACTS,
         "facts": [{"fact": "rule_touched_paths", "value": "path_list",
                    "max_items": MAX_PATHS}],
         "completeness": {"rule": "every_read_fact_present"}},
    ],
    "predicates": [
        {"predicate": spec.predicate, "input_contract": spec.input_contract,
         "parameter": spec.parameter, "reads": list(spec.reads),
         "matches": spec.path_fact,
         "patterns": {"min_items": MIN_PATTERNS, "max_items": MAX_PATTERNS},
         "holds_when": "any_read_path_matches_any_pattern"}
        for spec in PREDICATES.values()
    ],
    "pattern_grammar": {"exact": "relative_path",
                        "tree": "relative_path_then_slash_double_star",
                        "bare_directory_evidence": "refused"},
}

REGISTRY_NOTE = (f"predicate registry closed: {len(PREDICATES)} predicates, "
                 f"{len(INPUT_CONTRACTS)} input contracts")


def _without_prose(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _without_prose(v) for k, v in value.items() if k != "description"}
    if isinstance(value, list):
        return [_without_prose(v) for v in value]
    return value


def load_registry_doc(root: Path | None = None) -> Any:
    """The registry instance under `root`, parsed and not yet judged."""
    root = Path(root) if root is not None else records.REPO_ROOT
    path = root / REGISTRY_REL
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        raise records.SchemaLoadError(
            f"{REGISTRY_REL.as_posix()}: unreadable ({type(exc).__name__})") from exc
    except yaml.YAMLError as exc:
        raise records.SchemaLoadError(f"{REGISTRY_REL.as_posix()}: does not parse") from exc


def registry_findings(schemas: records.SchemaSet, document: Any) -> list[tuple[str, str]]:
    """Schema and closure findings for a predicate registry instance, as
    `(code, message)`, in the protocol registry's form. Its SHAPE is the schema's
    to judge; the SET is this module's: the instance must be the ratified
    registry, member for member, prose aside."""
    findings: list[tuple[str, str]] = []
    for error in schemas.errors(REGISTRY_SCHEMA_ID, document):
        where = "/".join(map(str, error.absolute_path)) or "(root)"
        findings.append(("council-convening-schema",
                         f"predicate registry: fails `{error.validator}` at {where}"))
    if _without_prose(document) != RATIFIED_REGISTRY:
        findings.append(("council-convening-registry-closure",
                         "predicate registry: differs from the registry as landed at this "
                         "commit; adding, renaming, rebinding or widening a predicate, an "
                         "input contract or a fact is a governed contract change"))
    return findings


def reads(predicate: str) -> tuple[str, ...]:
    """The facts a registered predicate reads (a KeyError for any other)."""
    return PREDICATES[predicate].reads


@functools.lru_cache(maxsize=1)
def _default_schemas() -> records.SchemaSet:
    return records.load_schemas()


def _is_relative_path(value: str, schemas: records.SchemaSet | None) -> bool:
    try:
        (schemas or _default_schemas()).check_definition("relative_path", value)
    except Refused:
        return False
    return True


def pattern_is_valid(pattern: Any, schemas: records.SchemaSet | None = None) -> bool:
    """An exact `relative_path`, or a `relative_path` followed by `/**`, with no
    `*`, `?` or `[` anywhere else (R5)."""
    if not isinstance(pattern, str):
        return False
    base = pattern[:-len(TREE_SUFFIX)] if pattern.endswith(TREE_SUFFIX) else pattern
    if any(mark in base for mark in _WILDCARDS):
        return False
    return _is_relative_path(base, schemas)


def matches(pattern: str, path: str) -> bool:
    """An exact pattern matches the equal path. A tree pattern matches every path
    strictly inside its directory, and not a file at the directory's own path."""
    if pattern.endswith(TREE_SUFFIX):
        return path.startswith(pattern[:-len(TREE_SUFFIX)] + "/")
    return path == pattern


def check_condition(predicate: Any, input_contract: Any, parameters: Any,
                    schemas: records.SchemaSet | None = None) -> None:
    """E2 step 8 for one condition. `schemas` is the boundary's schema set (the
    checkout's own when omitted), whose `relative_path` grammar the patterns use."""
    if not isinstance(predicate, str) or predicate not in PREDICATES:
        raise Refused("predicate_unknown", "predicate")
    spec = PREDICATES[predicate]
    if not isinstance(input_contract, str) or input_contract != spec.input_contract:
        raise Refused("predicate_parameters_malformed", "input_contract")
    if not isinstance(parameters, Mapping) or set(parameters) != {spec.parameter}:
        raise Refused("predicate_parameters_malformed", "parameters")
    patterns = parameters[spec.parameter]
    if not isinstance(patterns, list) or not MIN_PATTERNS <= len(patterns) <= MAX_PATTERNS:
        raise Refused("predicate_parameters_malformed", spec.parameter)
    for pattern in patterns:
        if not pattern_is_valid(pattern, schemas):
            raise Refused("predicate_parameters_malformed", spec.parameter)


def _fact_is_well_typed(fact: str, value: Any) -> bool:
    if fact in _PATH_LISTS:
        return (isinstance(value, list) and len(value) <= MAX_PATHS
                and all(isinstance(path, str) for path in value))
    if fact in _COUNTS:
        return (isinstance(value, int) and not isinstance(value, bool)
                and 0 <= value)
    return False


def evaluate(predicate: str, parameters: Mapping[str, Any], facts: Any) -> bool:
    """E2 step 10's evaluation of one condition over the AUTHORITATIVE facts.

    The condition has already passed `check_condition`. Order: evaluability (a
    read fact absent or outside the contract, then completeness: the entry count
    equals a total of at most 3000, and the path list holds one to two paths per
    entry), then the bare-directory evidence rule, then the decision.
    """
    spec = PREDICATES[predicate]
    if not isinstance(facts, Mapping):
        raise Refused("condition_unevaluable", spec.input_contract)
    for fact in spec.reads:
        if fact not in facts or not _fact_is_well_typed(fact, facts[fact]):
            raise Refused("condition_unevaluable", fact)
    if spec.input_contract == PR_FACTS:
        total = facts["changed_files_total"]
        count = facts["changed_paths_entry_count"]
        if count != total or total > MAX_LISTING_ENTRIES:
            raise Refused("condition_unevaluable", "changed_files_total")
        # Pre-review L5 (2026-10-09): every entry contributes one path, or two for
        # a rename, so a complete listing of n entries carries n to 2n paths.
        if not count <= len(facts["changed_paths"]) <= 2 * count:
            raise Refused("condition_unevaluable", "changed_paths")
    paths = facts[spec.path_fact]
    patterns = parameters[spec.parameter]
    for pattern in patterns:
        if not pattern.endswith(TREE_SUFFIX):
            inside = pattern + "/"
            if any(path.startswith(inside) for path in paths):
                raise Refused("predicate_parameters_malformed", spec.parameter)
    return any(matches(pattern, path) for pattern in patterns for path in paths)
