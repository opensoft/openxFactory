from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from scripts.hermes_runtime_validation.pytest_config import pytest_config_supported
from scripts.hermes_runtime_validation.pytest_inventory_proof import (
    ModuleContext,
    TargetProof,
)
from scripts.hermes_runtime_validation.pytest_inventory_proof import (
    module_context as _module_context,
)
from scripts.hermes_runtime_validation.pytest_inventory_proof import (
    parameter_skip as _parameter_skip,
)
from scripts.hermes_runtime_validation.pytest_inventory_proof import (
    target_proof as _target_proof,
)
from scripts.hermes_runtime_validation.pytest_inventory_proof import (
    target_selectors as _target_selectors,
)
from scripts.hermes_runtime_validation.pytest_paths import valid_test_path
from scripts.hermes_runtime_validation.pytest_static_values import (
    EvaluationBudget,
    StaticBudgetError,
)
from scripts.hermes_runtime_validation.pytest_support import pytest_marker
from scripts.hermes_runtime_validation.pytest_targets import find_test_target


@dataclass(frozen=True, slots=True)
class EvidenceTestNodes:
    collected: tuple[str, ...]
    skipped: tuple[str, ...]


def collect_static_pytest_nodes(
    repo_root: Path, module_paths: Sequence[str]
) -> tuple[str, ...]:
    if not pytest_config_supported(repo_root):
        raise ValueError("unsupported pytest collection configuration")
    budget = EvaluationBudget()
    nodes: list[str] = []
    try:
        for module_path in module_paths:
            path = PurePosixPath(module_path)
            if not valid_test_path(path):
                raise ValueError(f"invalid pytest module path: {module_path}")
            context = _module_context(repo_root, path, budget)
            if context is None:
                raise ValueError(f"unsupported static pytest module: {module_path}")
            for selectors in _target_selectors(
                context.module.body,
                context.analysis,
                budget,
            ):
                proof = _target_proof(context, selectors, budget)
                target = find_test_target(context.module, selectors)
                if proof is None or target is None:
                    raise ValueError(
                        f"unproved pytest target: {module_path}::{selectors[-1]}"
                    )
                if not any(
                    marker is not None and marker[0] == "postgres"
                    for marker in (pytest_marker(item) for item in target.decorators)
                ):
                    raise ValueError(
                        f"PostgreSQL target lacks marker: {module_path}::{selectors[-1]}"
                    )
                base = f"{module_path}::{'::'.join(selectors)}"
                if proof.decorated_skip or any(item.skipped for item in proof.variants):
                    raise ValueError(f"PostgreSQL target is statically skipped: {base}")
                if proof.variants:
                    nodes.extend(
                        f"{base}[{item.identifier}]" for item in proof.variants
                    )
                else:
                    nodes.append(base)
    except StaticBudgetError as error:
        raise ValueError("static pytest analysis budget exceeded") from error
    ordered = tuple(sorted(nodes))
    if not ordered or len(ordered) != len(set(ordered)):
        raise ValueError("static pytest node inventory is empty or duplicated")
    return ordered


def collect_evidence_test_nodes(
    repo_root: Path, evidence_register: Mapping[str, object]
) -> EvidenceTestNodes:
    if not pytest_config_supported(repo_root):
        return EvidenceTestNodes((), ())
    budget = EvaluationBudget()
    contexts: dict[PurePosixPath, ModuleContext | None] = {}
    proofs: dict[tuple[PurePosixPath, tuple[str, ...]], TargetProof | None] = {}
    collected: list[str] = []
    skipped: list[str] = []
    try:
        for node_id in _requested_nodes(evidence_register):
            budget.consume()
            path, selectors, parameter_id = _node_parts(node_id)
            if path is None or not selectors:
                continue
            if path not in contexts:
                contexts[path] = _module_context(repo_root, path, budget)
            context = contexts[path]
            if context is None:
                continue
            key = (path, selectors)
            if key not in proofs:
                proofs[key] = _target_proof(context, selectors, budget)
            proof = _parameter_skip(proofs[key], parameter_id)
            if proof is None:
                continue
            collected.append(node_id)
            if proof:
                skipped.append(node_id)
    except StaticBudgetError:
        return EvidenceTestNodes((), ())
    return EvidenceTestNodes(tuple(collected), tuple(skipped))


def _requested_nodes(evidence_register: Mapping[str, object]) -> tuple[str, ...]:
    nodes: set[str] = set()
    entries = evidence_register.get("entries")
    if not isinstance(entries, list):
        return ()
    for entry in entries:
        if not isinstance(entry, Mapping):
            continue
        values = entry.get("test_node_ids", []) or []
        if isinstance(values, Sequence) and not isinstance(values, (str, bytes)):
            nodes.update(str(value) for value in values if isinstance(value, str))
    return tuple(sorted(nodes))


def _node_parts(
    node_id: str,
) -> tuple[PurePosixPath | None, tuple[str, ...], str | None]:
    path_text, *selectors = node_id.split("::")
    path = PurePosixPath(path_text)
    if not valid_test_path(path):
        return None, (), None
    parameter_id: str | None = None
    if selectors and "[" in selectors[-1] and selectors[-1].endswith("]"):
        selectors[-1], parameter_id = selectors[-1][:-1].split("[", maxsplit=1)
    return path, tuple(selectors), parameter_id
