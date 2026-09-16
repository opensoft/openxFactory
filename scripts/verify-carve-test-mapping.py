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

EXIT CODES: 0 verified, 2 refused. **ARGPARSE ALSO EXITS 2** for an
invocation it rejects itself — corrected here from "1" (Copilot, round 3 on
#1080), because a caller classifying by status alone would have filed a usage
error as a clean run. The two are told apart by the OUTPUT, not the status: a
refusal prints `FAIL <where>: <code> — …` and its remediation on stderr, or a
`{"result": "refused", "code": …}` object on stdout under `--json`, while
argparse prints its own usage block and no code at all.
"""

from __future__ import annotations

import argparse
import json
import stat
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
    except UnicodeDecodeError as exc:
        # NOT AN `OSError` (Copilot review of #1080, accurate): a non-UTF-8
        # manifest raised out of the CLI's only catch as a traceback and
        # exit 1, so the documented named-refusal-and-exit-2 contract was
        # false for exactly the input most likely to be a corrupted file.
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} is not UTF-8 ({exc.reason} at byte {exc.start}); the "
            "mapping manifest is a YAML document and this floor is computed "
            "FROM it")
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
    # AN EMPTY DOCUMENT IS A NO-OP FLOOR, AND A NO-OP FLOOR MUST NOT PASS
    # (Copilot, round 3 on #1080). With `rows: []` the batch read and the
    # mapping are empty, `totals()` computes `0 = 0`, and the source command
    # exited 0 having examined no carve surface at all — a check that passes
    # by asking nothing, which is the shape this whole design refuses. An
    # empty or mistyped `moved_paths:` is the same failure one level down:
    # every row falls outside the surface and the mapping is empty again.
    # FLOOR PART 1 refuses both (`carve-surface-vacuous` among them) and this
    # tool is run where that validator is not.
    if not doc["rows"]:
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} carries an EMPTY `rows:` list. A floor computed over no "
            "rows reports `0 = 0` and has examined nothing; an empty mapping "
            "is not a mapping that holds")
    if not isinstance(doc["moved_paths"], list) or not doc["moved_paths"] \
            or not all(isinstance(entry, str) and entry
                       for entry in doc["moved_paths"]):
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} carries `moved_paths: {doc['moved_paths']!r}`, which is "
            "not a non-empty list of paths. The declared surface is what "
            "clause (a) is quantified over, so an empty or mistyped one puts "
            "every row outside it and the floor examines nothing")
    return doc


# --------------------------------------------------------------------------
# the source side — clauses (a), (b), (c)
# --------------------------------------------------------------------------

def verify_source(doc: dict[str, Any], repo: Path) -> dict[str, Any]:
    counts = mapping.tests_at_carve(repo, doc)
    mapped = mapping.map_rows(doc, counts)
    mapping.refuse_lost_tests(mapped)
    sums = mapping.totals(doc, mapped)
    if not sums["identity_holds"]:
        # A COMPUTED CHECK THAT IS NEVER ENFORCED IS PROSE (Copilot review of
        # #1080). `identity_holds` was reported and the run still exited 0, so
        # the one arithmetic § 5.4 states could be false in a passing report.
        # It is built to hold by construction — every row contributes
        # `(|homes| − 1) × tests` — so a false one means this floor's own
        # reading of the mapping is inconsistent, and an uncomputable check is
        # never a pass.
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            "the mapping does not balance: Σ(destinations) "
            f"{sums['destinations_sum']} against source_count "
            f"{sums['source_count']} + replica excess "
            f"{sums['replica_excess']} + also-replicated excess "
            f"{sums['also_replicated_excess']} + retired term "
            f"{sums['retired_excess']}. Every term is read from the manifest, "
            "so this is an inconsistency in the mapping itself and not a "
            "number to be adjusted")
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
    destinations = doc.get("destinations")
    wanted = mapping.resolved_destination(destination, destinations)
    for row in doc["rows"]:
        if not mapping.under_surface(row["source_path"], doc["moved_paths"]):
            continue
        if destination == mapping.RETAINED_TOKEN:
            if row.get("disposition") == mapping.NOT_MOVED and \
                    row.get("reason") in (mapping.STAYS_REASONS
                                          + (mapping.REPLICA_REASON,)):
                pairs.append((row["source_path"],
                              mapping.closed_relative(
                                  row["source_path"], "a retained row's path")))
            continue
        if row.get("disposition") not in mapping.MOVED_DISPOSITIONS:
            continue
        # PLACEMENT-AWARE, not shape-only (Copilot review of #1080): a
        # readable retirement block naming somewhere OTHER than this row's
        # effective arrival used to make this verifier skip the row, so a leg
        # could pass while never being asked for a file the manifest still
        # places there. `retirement_of` requires the block to retire the
        # arrival the row actually has.
        if mapping.retirement_of(row) is not None:
            continue
        key, path = mapping.effective_arrival(row)
        # RESOLVED IDENTITY, not the label (Copilot review of #1080). FLOOR
        # PART 1's `check_shape` admits two `destinations:` keys sharing one
        # `{repository, leg}` body, so a string comparison against
        # `--destination` skips every row written under the other alias — and
        # a floor that asks nothing passes.
        if mapping.resolved_destination(key, destinations) == wanted:
            pairs.append((row["source_path"],
                          mapping.closed_relative(
                              path, f"{row['source_path']}'s arrival path")))
    return pairs


def parse_replica_placements(values: list[str], doc: dict[str, Any],
                             destination: str) -> dict[str, str]:
    """`--replica-at SOURCE=DESTPATH`, on `verify-carve-arrival.py`'s rule: the
    left side is a replica row's `source_path`, or a moved row whose
    `also_replicated_to:` names THIS destination (RULED Q-L7 (a))."""
    destinations = doc.get("destinations")
    wanted = mapping.resolved_destination(destination, destinations)
    repository = mapping.repository_of(doc, destination)
    replicas = {row["source_path"]: row for row in doc["rows"]
                if mapping.is_replica(row)}
    also = {row["source_path"] for row in doc["rows"]
            if isinstance(row.get("also_replicated_to"), list)
            and any(mapping.resolved_destination(key, destinations) == wanted
                    for key in row["also_replicated_to"])
            and mapping.resolved_destination(
                mapping.effective_arrival(row)[0], destinations) != wanted}
    placements: dict[str, str] = {}
    for value in values:
        source_path, sep, relpath = value.partition("=")
        if not sep or not source_path or not relpath:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"--replica-at {value!r} is not SOURCE=DESTPATH")
        relpath = mapping.closed_relative(relpath, f"--replica-at {value!r}")
        declared = mapping.declared_homes(source_path)
        if declared is not None and repository not in declared:
            # A DECLARED SET IS A CLOSED LIST OF HOMES, so a placement at a
            # repository outside it is not a late arrival, it is a copy the
            # multiplicity never counted — and admitting it here would raise a
            # destination's floor by tests no term of clause (c) carries
            # (Copilot review of #1080). A replica with NO declared set is a
            # ZERO-TEST one, outside clause (b) by its own words, and it is
            # admitted exactly as `verify-carve-arrival.py` admits it.
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"--replica-at names {source_path!r} at {repository}, which "
                "is not one of the repositories its declared replica set "
                f"names ({', '.join(declared)}). "
                f"{mapping.MULTIPLICITY_DECLARATION}")
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
    """The `def test_` a DECLARED ARRIVAL carries, or None where nothing
    regular is at that path.

    `lstat`, AND SYMLINKS ARE NOT FOLLOWED (Copilot, second round on #1080).
    `read_bytes()` follows a link, so an arrival path that is a symlink to a
    test-bearing file elsewhere would satisfy a row's declaration with a file
    that never arrived — the floor's own evasion, and one no digest check at
    this level would notice. It is also the right reading of the manifest's
    own grammar: `git_mode: 120000` is admitted, and a symlink's BYTES are its
    target path, which carries no `def test_` — so a link row declares zero
    and collects zero either way, and a link standing in for a REAL row is an
    absent arrival. `verify-carve-arrival.py` reads the destination with
    `lstat` and treats a link as a git link blob, for the same reason.
    """
    try:
        status = path.lstat()
    except OSError:
        return None
    if not stat.S_ISREG(status.st_mode):
        return None
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
    if destination == mapping.RETAINED_TOKEN:
        # REFUSED, NOT DISCARDED (Copilot review of #1080). The retained
        # column needs no placement — a `not_moved` row stays at its own
        # `source_path` — so a `--replica-at` here is a mistaken invocation,
        # and silently ignoring it would report a passing retained summary
        # for a question the operator thought they had asked.
        if replica_values:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"--replica-at means nothing at the retained column "
                f"{mapping.RETAINED_TOKEN!r}: a `not_moved` row stays HERE, at "
                "its own source_path, and FLOOR PART 1 requires it present in "
                "both phases. Drop the flag, or name a destination that "
                "places a copy")
        placements: dict[str, str] = {}
    else:
        placements = parse_replica_placements(replica_values, doc,
                                              destination)
    owed = arrivals_for(doc, destination) + list(placements.items())
    # ONE FILE ANSWERS FOR ONE ROW (Copilot review of #1080). Two rows, or a
    # row and a `--replica-at`, naming one destination path would have that
    # file's tests counted once per declaration — one physical suite
    # satisfying two obligations, which is a MISSING ARRIVAL wearing a passing
    # total. `verify-carve-arrival.py` refuses the same shape with its
    # claimed-path check.
    seen: dict[str, str] = {}
    for source_path, relpath in owed:
        if relpath in seen:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"{relpath!r} is claimed at {destination!r} by both "
                f"{seen[relpath]!r} and {source_path!r}; one file cannot "
                "answer for two rows, and counting it twice would hide a "
                "missing arrival behind a total that balances")
        seen[relpath] = source_path

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
    print("+ retired term (RULED deletions) "
          f"{summary['retired_excess']:>4}")
    print(f"= Σ(destinations)              {summary['destinations_sum']:>6}"
          f"   {'✔' if summary['identity_holds'] else '✘'}")
    for repository, total in sorted(summary["per_repository"].items()):
        print(f"      {repository:<28} {total:>6}")
    # PRINTED UNCONDITIONALLY, AT ZERO TOO, on `validate-carve-manifest.py`'s
    # own rule for its `re-destined`/`retired` counts: the state this floor is
    # in must never be the state no log records.
    print(f"  retired test-bearing rows: {len(summary['retired'])} "
          f"carrying {summary['retired_tests']} `def test_`")
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


def _refused(exc: mapping.TestMappingRefusal, where: str,
             as_json: bool) -> int:
    """The ONE refusal exit — `verify-carve-arrival.py::_refused`'s shape, so
    the remediation trailer cannot be dropped by a caller that forgot it
    exists."""
    if as_json:
        print(json.dumps({"result": "refused", "code": exc.code,
                          "detail": exc.detail}))
    else:
        print(exc.render(where), file=sys.stderr)
    return 2


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
        return _refused(exc, where, args.json)
    except (TypeError, AttributeError, KeyError, ValueError,
            IndexError) as exc:
        # THE DOCUMENTED CONTRACT IS A NAMED REFUSAL AND EXIT 2 (Copilot review
        # of #1080). `read_manifest` accepts many YAML-valid but malformed
        # shapes — a row that is not a mapping, a `destinations:` value that is
        # not one — and those raised out of here as a traceback and exit 1,
        # which is a shape no caller can branch on. FLOOR PART 1 is the tool
        # that says WHICH shape is wrong; this one says only that it cannot
        # compute over the document, which is still a refusal and never a
        # pass. ORDERED AFTER the refusal arm above so a named refusal is
        # never swallowed as an unexpected one — `TestMappingRefusal` does not
        # inherit from any of these, and the order says so anyway.
        return _refused(
            mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                "this manifest cannot be read as a mapping "
                f"({type(exc).__name__}: {exc}); validate it with "
                "`scripts/validate-carve-manifest.py`, which is the tool that "
                "names the shape defect"),
            where, args.json)
    if args.json:
        print(json.dumps(summary))
    elif summary["mode"] == "source":
        _print_source(summary)
    else:
        _print_destination(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
