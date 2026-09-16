#!/usr/bin/env python3
"""FLOOR PART 2 — the source→destination TEST MAPPING, verified.

`split-opendox-two-layer-product` § 5.4, design § D6 (2), RULED OQ-1 and
RESTATED BY RULING OQ-K. The arithmetic and the reading of a row live in
`scripts/carve_test_mapping.py`, whose docstring carries the design record;
this file is the entry point and the report.

TWO QUESTIONS, TWO INVOCATIONS, and they are different questions rather than
one question run twice.

    python3 scripts/verify-carve-test-mapping.py

THE SOURCE SIDE — clauses (a), (b) and (c), answered from the manifest and this
repository's own history alone, with no destination checkout anywhere. Every
test-bearing row of the declared surface must name a home; every test-bearing
replica must declare its repository set; and the four terms of the sum are
computed and PRINTED, never asserted from prose. This is the invocation
`tests/carve_test_mapping/` drives on every required-suite pass, the seat
`tests/carve_manifest/` holds for FLOOR PART 1.

    python3 scripts/verify-carve-test-mapping.py \
        --destination openxdox_code --dest-root ../openXdox-code \
        [--replica-at tests/corpus-adapter/test_conformance.py=tests/test_conformance.py]

THE DESTINATION SIDE — the silent drop, one destination per run and never as a
cross-repository equality. `--destination` takes a `destinations:` key or the
literal `openxFactory` for the retained column, whose `--dest-root` defaults to
this repository.

WHY A REPLICA NEEDS `--replica-at` AND A MOVED ROW DOES NOT. A
`not_moved / replicated_at_destination` row carries no `destination_path` —
RULED OQ-C, because "this manifest declares what LEAVES, not what the
destination assembles" — so there is nothing to derive a replica's arrival path
from, and `verify-carve-arrival.py` already answers this by making the operator
declare it. This floor follows that rule exactly, and it has a second, measured
reason to: at 2026-09-16 the three test-bearing replicas are at NEITHER leg
(§ 3.7, FLOOR PART 3, is unticked), so a floor that counted them into a leg's
declared total unasked would refuse both legs for work that is not late — it
has not been scheduled. A replica joins a destination's floor on the run where
its placement is declared, which is the run that can prove it.

AT THE RETAINED COLUMN THE REPLICAS NEED NO FLAG, and that is not an
inconsistency: a `not_moved` row STAYS at `openxFactory`, at its own
`source_path`, and FLOOR PART 1 requires it present there in both phases. The
flag exists for placements the manifest cannot name, and this one it names.

EXIT CODES, the family's: 0 verified, 2 refused (`FAIL <where>: <code> — …`),
1 for a usage error argparse itself rejects.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:  # pragma: no branch - trivial guard
    sys.path.insert(0, _SCRIPTS_DIR)

import yaml  # noqa: E402

import carve_test_mapping as mapping  # noqa: E402

ROOT = mapping.ROOT


def read_manifest(path: Path) -> dict[str, Any]:
    """The manifest, or an unreadable refusal. NO not-fail-closed branch: this
    floor has nothing to say without the document, and `NO MANIFEST … nothing
    to validate` is FLOOR PART 1's answer to its own ceremony, not this one's.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} cannot be read ({exc.strerror}); FLOOR PART 2 is computed "
            "FROM the mapping manifest and has no answer without it")
    try:
        doc = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable", f"{path} is not readable YAML: {exc}")
    if not isinstance(doc, dict) or not isinstance(doc.get("rows"), list):
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} carries no `rows:` list — validate it with "
            "`scripts/validate-carve-manifest.py` before asking this floor "
            "anything")
    for key in ("carve_commit", "moved_paths", "destinations",
                "source_repository"):
        if doc.get(key) is None:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"{path} carries no `{key}:`; FLOOR PART 1 refuses that "
                "document and FLOOR PART 2 cannot be computed over it")
    return doc


# --------------------------------------------------------------------------
# the source side — clauses (a), (b), (c)
# --------------------------------------------------------------------------

def verify_source(doc: dict[str, Any], repo: Path) -> dict[str, Any]:
    counts = mapping.tests_at_carve(repo, doc)
    mapped = mapping.map_rows(doc, counts)
    mapping.refuse_lost_tests(mapped)
    sums = mapping.totals(doc, mapped)
    retired = [{"source_path": record.source_path, "tests": record.tests,
                "ruling": record.ruling}
               for record in mapped if record.kind == "retired" and record.tests]
    replicas = [{"source_path": record.source_path, "tests": record.tests,
                 "homes": list(record.homes)}
                for record in mapped if record.kind == "replicated"
                and record.tests]
    return {
        "result": "ok",
        "mode": "source",
        "carve_commit": doc["carve_commit"],
        "carve_tag": doc.get("carve_tag"),
        "rows": len(doc["rows"]),
        "rows_in_surface": len(mapped),
        "test_bearing_rows": sum(1 for record in mapped if record.tests),
        # HOMED AND RETIRED COUNTED APART, never summed into one "covered":
        # clause (a) is about a home and a RULED deletion is not one. The two
        # numbers add to `test_bearing_rows` and a reader can see which is
        # which without opening the manifest.
        "homed_rows": sum(1 for record in mapped
                          if record.tests and record.homes),
        "declared_replicas": sum(1 for record in mapped
                                 if record.kind == "replicated"),
        "test_bearing_replicas": replicas,
        "retired": retired,
        **sums,
    }


# --------------------------------------------------------------------------
# the destination side — the silent drop
# --------------------------------------------------------------------------

def arrivals_for(doc: dict[str, Any], destination: str) -> list[tuple[str, str]]:
    """`(source_path, path at the destination)` for every row this destination
    owes an arrival for — moved rows at their EFFECTIVE arrival (RULED Q6), or,
    at the retained column, the `stays_openxfactory_*` and replica rows at
    their own `source_path`. A RETIRED row owes nothing (RULED 5656343213)."""
    pairs: list[tuple[str, str]] = []
    for row in doc["rows"]:
        if not mapping.under_surface(row["source_path"], doc["moved_paths"]):
            continue
        if destination == mapping.RETAINED_TOKEN:
            if row.get("disposition") == mapping.NOT_MOVED and \
                    row.get("reason") in (mapping.STAYS_REASONS
                                          + (mapping.REPLICA_REASON,)):
                pairs.append((row["source_path"], row["source_path"]))
            continue
        if row.get("disposition") not in mapping.MOVED_DISPOSITIONS:
            continue
        if mapping.retired_at(row)[1] is not None:
            continue
        key, path = mapping.effective_arrival(row)
        if key == destination:
            pairs.append((row["source_path"], path))
    return pairs


def parse_replica_placements(values: list[str], doc: dict[str, Any],
                             destination: str) -> dict[str, str]:
    """`--replica-at SOURCE=DESTPATH`, on `verify-carve-arrival.py`'s rule: the
    left side is a replica row's `source_path`, or a moved row whose
    `also_replicated_to:` names THIS destination (RULED Q-L7 (a))."""
    replicas = {row["source_path"] for row in doc["rows"]
                if mapping.is_replica(row)}
    also = {row["source_path"] for row in doc["rows"]
            if isinstance(row.get("also_replicated_to"), list)
            and destination in row["also_replicated_to"]
            and mapping.effective_arrival(row)[0] != destination}
    placements: dict[str, str] = {}
    for value in values:
        source_path, sep, relpath = value.partition("=")
        if not sep or not source_path or not relpath:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"--replica-at {value!r} is not SOURCE=DESTPATH")
        if source_path not in replicas and source_path not in also:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"--replica-at names {source_path!r}, which at destination "
                f"{destination!r} is neither a `not_moved / "
                f"{mapping.REPLICA_REASON}` row nor a moved row whose "
                "`also_replicated_to:` lists this destination")
        if source_path in placements:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"--replica-at names {source_path!r} twice "
                f"({placements[source_path]!r} and {relpath!r})")
        placements[source_path] = relpath
    return placements


def _tests_in(path: Path) -> int | None:
    try:
        return mapping.count(path.read_bytes())
    except OSError:
        return None


def _tree_tests(dest_root: Path) -> tuple[int, int]:
    """The CONTEXT figure: every `def test_` this checkout carries, in ITS OWN
    files. Never part of the floor — the floor is the declared arrivals — and
    printed beside them so a reader can see how much of a destination's suite
    the manifest speaks for.

    NESTED GIT CHECKOUTS ARE SKIPPED, and the openxFactory run is why: with
    `openDox/` and `openXdox/` materialized (which the carve suites require)
    a naive walk counts two other repositories' suites into a figure captioned
    "the tree carries", and the reader has no way to tell. A directory holding
    a `.git` entry is another repository's root, and everything under it is
    that repository's.
    """
    total = 0
    files = 0
    stack = [dest_root]
    while stack:
        directory = stack.pop()
        try:
            entries = sorted(directory.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.is_symlink():
                continue
            if entry.is_dir():
                if entry.name == ".git":
                    continue
                if (entry / ".git").exists():
                    continue
                stack.append(entry)
            elif entry.suffix == ".py":
                found = _tests_in(entry)
                if found:
                    files += 1
                    total += found
    return total, files


def verify_destination(doc: dict[str, Any], repo: Path, destination: str,
                       dest_root: Path,
                       replica_values: list[str]) -> dict[str, Any]:
    repository = mapping.repository_of(doc, destination)
    counts = mapping.tests_at_carve(repo, doc)
    placements = parse_replica_placements(replica_values, doc, destination) \
        if destination != mapping.RETAINED_TOKEN else {}
    owed = arrivals_for(doc, destination) + list(placements.items())

    declared = 0
    collected = 0
    absent: list[dict[str, Any]] = []
    below: list[dict[str, Any]] = []
    for source_path, relpath in owed:
        want = counts[source_path]
        declared += want
        found = _tests_in(dest_root / relpath)
        if found is None:
            if want:
                absent.append({"source_path": source_path, "path": relpath,
                               "declared": want})
            continue
        collected += found
        if found < want:
            below.append({"source_path": source_path, "path": relpath,
                          "declared": want, "found": found})

    tree, tree_files = _tree_tests(dest_root)

    summary = {
        "result": "ok",
        "mode": "destination",
        "destination": destination,
        "repository": repository,
        "dest_root": str(dest_root),
        "carve_commit": doc["carve_commit"],
        "rows_owed": len(owed),
        "replicas_declared": len(placements),
        "declared": declared,
        "collected": collected,
        "absent": absent,
        "below_declaration": below,
        "tree_tests": tree,
        "tree_files": tree_files,
    }
    if collected < declared:
        raise mapping.TestMappingRefusal(
            "destination-test-shortfall",
            f"{repository} collects {collected} `def test_` at the arrival "
            f"paths its own rows name and those rows declare {declared} "
            f"({declared - collected} short). "
            + (f"ABSENT: {', '.join(item['path'] for item in absent[:5])}. "
               if absent else "")
            + (f"BELOW DECLARATION: "
               f"{', '.join(item['path'] for item in below[:5])}. "
               if below else "")
            + "The most likely way a large suite loses coverage in a carve is "
              "tests dropped rather than moved")
    return summary


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

def _print_source(summary: dict[str, Any]) -> None:
    print(f"OK FLOOR PART 2 (source) at {summary['carve_commit'][:12]} "
          f"({summary['carve_tag']}): {summary['test_bearing_rows']} "
          f"test-bearing row(s) of {summary['rows_in_surface']} under the "
          f"declared surface, {summary['homed_rows']} homed and "
          f"{len(summary['retired'])} RULED-retired; "
          f"{len(summary['test_bearing_replicas'])} test-bearing replica(s) "
          "with a declared multiplicity")
    print(f"  source_count                 {summary['source_count']:>6}")
    print(f"+ replica excess (m − 1)       {summary['replica_excess']:>6}")
    print("+ also-replicated excess       "
          f"{summary['also_replicated_excess']:>6}")
    print(f"− retired (RULED deletions)    {summary['retired_total']:>6}")
    print(f"= Σ(destinations)              {summary['destinations_sum']:>6}"
          f"   {'✔' if summary['identity_holds'] else '✘'}")
    for repository, total in sorted(summary["per_repository"].items()):
        print(f"      {repository:<28} {total:>6}")
    # PRINTED UNCONDITIONALLY, AT ZERO TOO, on `validate-carve-manifest.py`'s
    # own rule for its `re-destined`/`retired` counts: the state this floor is
    # in must never be the state no log records.
    print(f"  retired test-bearing rows: {len(summary['retired'])}")
    for item in summary["retired"]:
        print(f"      {item['source_path']} — {item['tests']} `def test_`, "
              f"RULED {item['ruling']}")


def _print_destination(summary: dict[str, Any]) -> None:
    print(f"OK FLOOR PART 2 (destination) {summary['repository']} at "
          f"{summary['dest_root']}: {summary['collected']} `def test_` "
          f"collected at {summary['rows_owed']} declared arrival path(s), "
          f"against {summary['declared']} declared "
          f"({summary['collected'] - summary['declared']:+d}); "
          f"{summary['replicas_declared']} replica placement(s) declared; "
          f"the tree carries {summary['tree_tests']} across "
          f"{summary['tree_files']} file(s)")
    print(f"  rows below their declaration: {len(summary['below_declaration'])}")
    for item in summary["below_declaration"]:
        print(f"      {item['path']} — declared {item['declared']}, "
              f"found {item['found']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="verify-carve-test-mapping.py",
        description=("Verify FLOOR PART 2 of the RULED four-part floor — the "
                     "source→destination TEST MAPPING with declared "
                     "multiplicity (split-opendox § 5.4, § D6 (2))."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifest", metavar="PATH", default=None,
                        help=("the mapping manifest (default: "
                              f"<repo>/{mapping.MANIFEST_RELPATH})"))
    parser.add_argument("--repo", metavar="DIR", default=None,
                        help=("the openxFactory repository the carve-commit "
                              "blobs are read in (default: this one)"))
    parser.add_argument("--destination", metavar="KEY", default=None,
                        help=("a `destinations:` key, or "
                              f"`{mapping.RETAINED_TOKEN}` for the retained "
                              "column; omit for the source side"))
    parser.add_argument("--dest-root", metavar="DIR", default=None,
                        help=("the destination checkout (default, for "
                              f"`{mapping.RETAINED_TOKEN}` only: --repo)"))
    parser.add_argument("--replica-at", metavar="SOURCE=DESTPATH",
                        action="append", default=[],
                        help=("where a replica landed at this destination; "
                              "repeatable"))
    parser.add_argument("--json", action="store_true",
                        help="machine-readable output")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else ROOT
    manifest = Path(args.manifest).resolve() if args.manifest \
        else repo / mapping.MANIFEST_RELPATH
    where = str(manifest)
    try:
        doc = read_manifest(manifest)
        if args.destination is None:
            if args.dest_root or args.replica_at:
                raise mapping.TestMappingRefusal(
                    "test-mapping-unreadable",
                    "--dest-root and --replica-at describe a DESTINATION and "
                    "mean nothing without --destination; the source side "
                    "reads the manifest and this repository only")
            summary = verify_source(doc, repo)
        else:
            if args.dest_root:
                dest_root = Path(args.dest_root).resolve()
            elif args.destination == mapping.RETAINED_TOKEN:
                dest_root = repo
            else:
                raise mapping.TestMappingRefusal(
                    "test-mapping-unreadable",
                    f"--destination {args.destination!r} needs --dest-root: "
                    "only the retained column has a default, and it is this "
                    "repository")
            if not dest_root.is_dir():
                raise mapping.TestMappingRefusal(
                    "test-mapping-unreadable",
                    f"--dest-root {dest_root} is not a directory")
            where = str(dest_root)
            summary = verify_destination(doc, repo, args.destination,
                                         dest_root, args.replica_at)
    except mapping.TestMappingRefusal as exc:
        if args.json:
            print(json.dumps({"result": "refused", "code": exc.code,
                              "detail": exc.detail}))
        else:
            print(exc.render(where), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(summary))
    elif summary["mode"] == "source":
        _print_source(summary)
    else:
        _print_destination(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
