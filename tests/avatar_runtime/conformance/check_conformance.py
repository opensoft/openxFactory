#!/usr/bin/env python3
"""Acceptance-ID conformance checker (FR-034/FR-035, ARR-008).

Compares ``scenario-test-map.yaml`` against the digest-verified acceptance
sources and the collected test set. Fails on: missing, duplicate, dangling,
skipped-required, or unknown mappings. ``--final`` additionally validates the
realization pin (five coordinates present, provisional adapter disabled, no
canonical-vs-provisional divergence).

Run:  python tests/avatar_runtime/conformance/check_conformance.py [--final]
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MAP_PATH = HERE / "scenario-test-map.yaml"
PIN_PATH = HERE / "realization-pin.yaml"

sys.path.insert(0, str(HERE.parent))  # make 'conformance' importable when run directly
from conformance import acceptance_source  # noqa: E402

VALID_DISPOSITIONS = {"mapped", "non_applicable", "gate"}


# --------------------------------------------------------------------------- #
# Pure checks (dependency-injected for unit testing)
# --------------------------------------------------------------------------- #
def check(
    required: set[str],
    entries: list[dict],
    collected: set[str],
    skipped: set[str] | None = None,
) -> dict[str, list[str]]:
    skipped = skipped or set()
    failures: dict[str, list[str]] = {
        "missing": [],
        "duplicate": [],
        "dangling": [],
        "skipped_required": [],
        "unknown": [],
    }
    seen: dict[str, dict] = {}
    for e in entries:
        sid = e["scenario_id"]
        if sid in seen:
            failures["duplicate"].append(sid)
            continue
        seen[sid] = e
        if sid not in required:
            failures["unknown"].append(sid)
        disp = e.get("disposition")
        if disp not in VALID_DISPOSITIONS:
            failures["unknown"].append(f"{sid}:bad-disposition:{disp}")
        if disp == "mapped":
            for node in e.get("test_node_ids", []) or []:
                if node not in collected:
                    failures["dangling"].append(f"{sid} -> {node}")
                elif node in skipped:
                    failures["skipped_required"].append(f"{sid} -> {node}")
    for sid in sorted(required):
        if sid not in seen:
            failures["missing"].append(sid)
    return failures


def validate_realization_pin(pin: dict) -> list[str]:
    problems: list[str] = []
    rk = pin.get("released_kernel", {}) or {}
    for coord in ("tag", "commit", "file_digests", "interface_lock_digest", "acceptance_map_digest"):
        if not rk.get(coord):
            problems.append(f"missing release coordinate: {coord}")
    conf = pin.get("conformance", {}) or {}
    if conf.get("provisional_adapter_disabled") is not True:
        problems.append("provisional_adapter_disabled must be true for final conformance")
    if conf.get("canonical_matches_provisional") is not True:
        problems.append("canonical execution diverged from provisional behavior")
    return problems


# --------------------------------------------------------------------------- #
# Real IO (CLI)
# --------------------------------------------------------------------------- #
def load_entries(path: Path = MAP_PATH) -> list[dict]:
    doc = yaml.safe_load(path.read_text())
    return list(doc.get("mappings", []))


def collect_test_nodes(root: Path = ROOT) -> set[str]:
    proc = subprocess.run(
        [
            sys.executable, "-m", "pytest", str(root / "tests" / "avatar_runtime"),
            "--collect-only", "-q", "-p", "no:randomly",
        ],
        capture_output=True, text=True, cwd=str(root),
    )
    nodes = set()
    for line in proc.stdout.splitlines():
        line = line.strip()
        if "::" in line and line.startswith("tests/"):
            nodes.add(line)
    return nodes


def main(argv: list[str]) -> int:
    final = "--final" in argv
    required = acceptance_source.required_scenarios(final=final)
    entries = load_entries()
    collected = collect_test_nodes()
    failures = check(required, entries, collected)

    total = sum(len(v) for v in failures.values())
    print(f"conformance: {len(required)} required scenarios, {len(entries)} map entries, "
          f"{len(collected)} collected test nodes")
    if final:
        if not PIN_PATH.exists():
            print("FAIL: --final requires realization-pin.yaml")
            total += 1
        else:
            pin = yaml.safe_load(PIN_PATH.read_text()) or {}
            for p in validate_realization_pin(pin):
                print(f"  realization-pin: {p}")
                total += 1
    for cls, items in failures.items():
        if items:
            print(f"  {cls}: {len(items)}")
            for it in items[:20]:
                print(f"    - {it}")
    if total == 0:
        print("OK: acceptance-ID conformance complete")
        return 0
    print(f"FAIL: {total} conformance problem(s)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
