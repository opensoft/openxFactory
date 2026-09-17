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
    # THE SCALARS ARE TYPED, NOT MERELY PRESENT (Copilot, round 4 on #1080).
    # `repository_of` coerced a non-string `source_repository:` with `str()`,
    # so a list reached the report as `"['opensoft/openxFactory']"` — measured
    # to REFUSE downstream (`refuse_unknown_declared_homes`, because the
    # declared homes then match nothing), which is a right answer arrived at
    # by the wrong road and a message an operator would have to decode. The
    # presence checks above are what this floor needs to COMPUTE; these are
    # what it needs to compute the truth.
    for key, kind in (("carve_commit", str), ("source_repository", str)):
        if not isinstance(doc[key], kind) or not doc[key]:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"{path} carries `{key}: {doc[key]!r}`, which is not a "
                "non-empty string. FLOOR PART 1 refuses that document; this "
                "one cannot compute a true mapping over it either")
    if not isinstance(doc["destinations"], dict) or not doc["destinations"]:
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} carries `destinations: {doc['destinations']!r}`, which "
            "is not a non-empty map. Every home this floor names is resolved "
            "through it")
    # AND EVERY ENTRY IS A WHOLE IDENTITY (Copilot, round 8 on #1080). A
    # `destinations:` key resolves to the `{repository, leg}` body that IS its
    # identity, and an entry missing `leg:` resolved to `(repository, None)` —
    # which is not equal to the `(repository, leg)` a sibling key resolves to,
    # so a `--destination` naming the incomplete alias matched none of the
    # rows written under the complete one and THAT LEG OWED NOTHING. FLOOR
    # PART 1's `check_shape` requires both fields; this tool is run where that
    # validator is not, and it compares those bodies for a living.
    for key, entry in doc["destinations"].items():
        # AND THE KEY IS A KEY (Copilot, round 10 on #1080): YAML admits
        # `null:` and numeric keys, and `resolved_destination(None, …)` would
        # then resolve to a real `{repository, leg}` while `homes_of` reads
        # the same non-string value on a row as NO HOME — a destination-only
        # invocation counting an arrival the source mapping rejects, or
        # skipping it and passing by asking nothing.
        if not isinstance(key, str) or not key:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"{path} carries the `destinations:` key {key!r}, which is "
                "not a non-empty string. A key is the LABEL a row's "
                "`destination:` spells and `--destination` names, and both "
                "of those are strings")
        if not isinstance(entry, dict) or not all(
                isinstance(entry.get(field), str) and entry[field]
                for field in ("repository", "leg")):
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"{path} carries `destinations: {key!r}: {entry!r}`, which is "
                "not a map with a non-empty `repository:` and `leg:`. A key "
                "is a LABEL and that pair is its identity — an incomplete one "
                "compares equal to nothing, so a leg named by it would be "
                "asked for no arrival at all")
    if not isinstance(doc["moved_paths"], list) or not doc["moved_paths"] \
            or not all(isinstance(entry, str) and entry
                       for entry in doc["moved_paths"]):
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} carries `moved_paths: {doc['moved_paths']!r}`, which is "
            "not a non-empty list of paths. The declared surface is what "
            "clause (a) is quantified over, so an empty or mistyped one puts "
            "every row outside it and the floor examines nothing")
    # EVERY ROW IS A ROW, ONCE (Copilot, round 6 on #1080). Two defects, one
    # reading, and both of them are about the mapping's KEY:
    #
    #   * a row that is not a dict, or carries no `source_path:`, reached
    #     `tests_at_carve`, `map_rows`, `arrivals_for` and
    #     `parse_replica_placements` as a raw subscript — a TRACEBACK and
    #     exit 1, against a documented contract of a named refusal and exit 2,
    #     for exactly the input most likely to be a hand-edited document; and
    #   * a DUPLICATED `source_path:` counted one file twice. `tests_at_carve`
    #     keys its counts BY PATH and collapses the duplicate, while
    #     `map_rows` emits one mapping per ROW, so both copies were counted
    #     and the identity went on balancing. Measured on the landed manifest
    #     with one 35-test row duplicated: `source_count` 4,411 → 4,446,
    #     `identity_holds` true, exit 0. FLOOR PART 1 refuses the same
    #     document `carve-file-duplicated` and its contract is one disposition
    #     per file; this tool is run where that validator is not.
    seen: dict[str, int] = {}
    for index, row in enumerate(doc["rows"]):
        if not isinstance(row, dict) or not isinstance(row.get("source_path"),
                                                       str) \
                or not row["source_path"]:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"{path} rows[{index}] carries no `source_path:` string "
                f"({row!r}); every question this floor asks is keyed by one, "
                "and a row without one cannot be counted, homed or owed")
        if row["source_path"] in seen:
            raise mapping.TestMappingRefusal(
                "test-mapping-unreadable",
                f"{path} declares {row['source_path']!r} in "
                f"rows[{seen[row['source_path']]}] AND rows[{index}]; one "
                "file carries one disposition, and counting a path twice "
                "inflates the source side by its tests while the identity "
                "goes on balancing (FLOOR PART 1 calls it "
                "`carve-file-duplicated`)")
        seen[row["source_path"]] = index
    # AND THE DECLARED SURFACE SELECTS SOMETHING (Copilot, round 6 on #1080,
    # marked "previously missed" and right about a claim round 3 made and did
    # not keep). Round 3 refused an EMPTY or mistyped `moved_paths:`; a
    # well-formed one naming a prefix no row lies under is the same vacuum one
    # step further on — every row falls outside the surface, `map_rows`
    # returns nothing, `totals()` computes `0 = 0` and the run exits 0 having
    # examined no carve surface at all. Measured on the landed manifest with
    # `moved_paths: ["contracts/policies/"]`: `rows_in_surface 0`,
    # `source_count 0`, exit 0. Clause (a) is a QUANTIFIER, and a quantifier
    # over the empty set is not a floor that holds.
    # EVERY ROW'S DISPOSITION IS IN THE VOCABULARY, AND THE DESTINATION SIDE
    # IS WHY (Copilot, round 10 on #1080). `homes_of` refuses an unknown
    # `disposition:`/`reason:` — but ONLY the source invocation calls it. At a
    # leg, `arrivals_for` reads the disposition to decide whether a row is
    # owed here, so a row spelled `disposition: typo` simply fell out of the
    # loop as somebody else's business and the leg passed WITHOUT EVER
    # CHECKING THAT ARRIVAL. The vocabulary is FLOOR PART 1's, closed, and
    # this is the one place both modes pass through.
    for index, row in enumerate(doc["rows"]):
        disposition = row.get("disposition")
        reason = row.get("reason")
        if disposition in mapping.MOVED_DISPOSITIONS:
            continue
        if disposition == mapping.NOT_MOVED and reason in (
                mapping.STAYS_REASONS
                + (mapping.REPLICA_REASON, mapping.DELETED_REASON)):
            continue
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} rows[{index}] ({row['source_path']}) carries "
            f"disposition {disposition!r} / reason {reason!r}, which FLOOR "
            "PART 1's own vocabulary does not hold. The source side refuses "
            "such a row by name; a DESTINATION run would read it as another "
            "leg's business and pass without ever asking for its arrival")
    outside = [source_path for source_path in seen
               if not mapping.under_surface(source_path, doc["moved_paths"])]
    if len(outside) == len(seen):
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} carries {len(seen)} row(s) and NOT ONE of them lies "
            f"under the declared surface {doc['moved_paths']!r}. The mapping "
            "would be empty and the identity `0 = 0` would hold over nothing; "
            "a floor that passes by asking nothing is not a floor")
    # AND A PARTIAL SURFACE IS THE SAME VACUUM, PRO RATA (Copilot, round 7 on
    # #1080, taking the round-6 finding one step further and rightly). A
    # prefix covering only SOME rows leaves the rest unquantified — at the
    # limit, a prefix matching one zero-test row reports `0 = 0` over a
    # document declaring thousands. `map_rows` skips out-of-surface rows
    # BY DESIGN, because § 5.4 binds "every file in the manifest's DECLARED
    # SURFACE"; what was missing is that the two never disagree in a document
    # this floor will answer about, and only a pytest assertion said so.
    #
    # THIS FILE'S OWN PRECEDENT, and the reason it is a refusal and not an
    # assertion: `refuse_stale_declarations` was raised to the runtime path
    # two rounds ago in exactly these words — "a pytest assertion is not a
    # check the runbook's invocation makes". The landed manifest carries 456
    # rows and 456 of them are under its surface; a document where that stops
    # being true is FLOOR PART 1 and this floor reading two different
    # surfaces, which is drift, and drift is refused here rather than skipped
    # quietly.
    if outside:
        raise mapping.TestMappingRefusal(
            "test-mapping-unreadable",
            f"{path} places {len(outside)} of its {len(seen)} rows OUTSIDE "
            f"the declared surface {doc['moved_paths']!r}: "
            f"{', '.join(outside[:5])}"
            + (", …" if len(outside) > 5 else "")
            + ". Clause (a) is quantified over that surface, so a row outside "
            "it is a file this floor would answer about by not asking — and a "
            "surface that covers only part of its own document reports "
            "`0 = 0` over the part it omits")
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
                "ruling": record.ruling,
                # THE COPIES A RETIREMENT DOES NOT DELETE, named in the report
                # rather than left to be inferred (Copilot, round 6 on #1080).
                # A retirement deletes the row's own ARRIVAL and not the
                # copies `also_replicated_to:` places elsewhere, so such a row
                # is retired AND still homed — the state that made the two
                # counts below overlap, and the reader has no way to see it in
                # a summary that prints neither.
                "homes": list(record.homes)}
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
        #
        # AND THEY ARE DISJOINT BY KIND, NOT BY EMPTINESS (Copilot, round 6 on
        # #1080, accurate about a documented invariant this code broke). A
        # retired row KEEPS the homes its `also_replicated_to:` copies stand
        # at — that is the identity `totals()` was corrected to compute two
        # rounds ago — so `record.tests and record.homes` counted such a row
        # HERE while `retired` reported it too, and the two counts summed to
        # more than `test_bearing_rows`. Measured with one landed retirement
        # given a replica: 145 + 2 against 146. The kinds partition the
        # mapping; the homes do not.
        "homed_rows": sum(1 for record in mapped
                          if record.tests and record.homes
                          and record.kind != "retired"),
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
        if row.get("disposition") in mapping.MOVED_DISPOSITIONS:
            key, path = mapping.effective_arrival(row)
            # THE KEY IS VALIDATED BEFORE ANY SKIP, AND AT EVERY LEG (Copilot,
            # round 5 on #1080 and its round-6 restatement — two findings, one
            # hole). Both of the skips below used to be reached with the key
            # unread, and `repository_of` was called only on the SOURCE side:
            #
            #   * a shape-valid retirement pointed at a FABRICATED key
            #     silenced the row here, and
            #   * a MISSPELLED `destination:` simply failed to equal `wanted`,
            #     so the row was dropped as another leg's business.
            #
            # Measured on the landed manifest, one row mutated each way:
            # `tests/ideation-dashboard/test_doc_wheel.py` re-pointed to
            # `opendox_kode` took the openDox-code run from 117 rows / 1,067
            # declared to 116 / 1,045 AND EXITED 0 — a leg passing because a
            # live arrival was omitted, which is the one thing a destination
            # floor exists to refuse. `verify_source` refuses that document;
            # this invocation is the one a leg runs, where the source side is
            # not running at all.
            #
            # AN ABSENT KEY IS NOT THIS REFUSAL. `homes_of` draws that line
            # already: an absent or non-string `destination:` is NO HOME, and
            # the source side names it `test-home-missing`; a PRESENT key that
            # `destinations:` does not carry is a vocabulary error, and this
            # is where a leg finds it.
            if isinstance(key, str) and key:
                # `repository_of_ARRIVAL`, the seam `homes_of` uses: a moved
                # row may not name the retained column, which `repository_of`
                # resolves happily and which no invocation would then ask for
                # (Copilot, round 8 on #1080).
                mapping.repository_of_arrival(doc, key)
            if destination == mapping.RETAINED_TOKEN:
                continue
            # PLACEMENT-AWARE, not shape-only (Copilot review of #1080): a
            # readable retirement block naming somewhere OTHER than this row's
            # effective arrival used to make this verifier skip the row, so a
            # leg could pass while never being asked for a file the manifest
            # still places there. `retirement_of` requires the block to retire
            # the arrival the row actually has.
            if mapping.retirement_of(row) is not None:
                continue
            # RESOLVED IDENTITY, not the label (Copilot review of #1080).
            # FLOOR PART 1's `check_shape` admits two `destinations:` keys
            # sharing one `{repository, leg}` body, so a string comparison
            # against `--destination` skips every row written under the other
            # alias — and a floor that asks nothing passes.
            if mapping.resolved_destination(key, destinations) == wanted:
                pairs.append((row["source_path"],
                              mapping.closed_relative(
                                  path,
                                  f"{row['source_path']}'s arrival path")))
            continue
        if destination == mapping.RETAINED_TOKEN and \
                row.get("disposition") == mapping.NOT_MOVED and \
                row.get("reason") in (mapping.STAYS_REASONS
                                      + (mapping.REPLICA_REASON,)):
            pairs.append((row["source_path"],
                          mapping.closed_relative(
                              row["source_path"], "a retained row's path")))
    return pairs


def parse_replica_placements(values: list[str], doc: dict[str, Any],
                             destination: str) -> dict[str, str]:
    """`--replica-at SOURCE=DESTPATH`, on `verify-carve-arrival.py`'s rule: the
    left side is a replica row's `source_path`, or a moved row whose
    `also_replicated_to:` names THIS destination (RULED Q-L7 (a))."""
    destinations = doc.get("destinations")
    wanted = mapping.resolved_destination(destination, destinations)
    repository = mapping.repository_of(doc, destination)
    # BOTH ADMISSION SETS ARE INSIDE THE DECLARED SURFACE (Copilot, round 5 on
    # #1080). `arrivals_for` filters its rows through `under_surface` and
    # these two comprehensions did not, so a replica row OUTSIDE
    # `moved_paths:` was admitted, counted from `tests_at_carve` and added to
    # this destination's declared total — a destination obligation the SOURCE
    # mapping does not carry at all, because `map_rows` skips exactly those
    # rows. Measured on the landed manifest with one replica row's path
    # changed to `tests/carve_manifest/test_carve_manifest.py` (out of
    # surface, 71 `def test_` at the carve commit): the openDox-code run's
    # declaration rose 1,067 → 1,138 and the leg was refused a 22-test
    # shortfall it did not have. Clause (a) is quantified over the declared
    # surface; a floor may not be RAISED outside the set it is quantified
    # over any more than it may be lowered inside it.
    in_surface = [row for row in doc["rows"]
                  if mapping.under_surface(row["source_path"],
                                           doc["moved_paths"])]
    replicas = {row["source_path"]: row for row in in_surface
                if mapping.is_replica(row)}
    also = {row["source_path"] for row in in_surface
            # MOVED ROWS ONLY (Copilot, round 10 on #1080): RULED Q-L7 (a)
            # gives `also_replicated_to:` to a row that MOVES, and `homes_of`
            # reads it nowhere else — so a `not_moved` row carrying the field
            # was admitted here and counted at a destination while the source
            # mapping gave it no such home at all.
            if row.get("disposition") in mapping.MOVED_DISPOSITIONS
            and isinstance(row.get("also_replicated_to"), list)
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


def _tests_in(dest_root: Path, relpath: str) -> bytes | None:
    """The BYTES of a DECLARED ARRIVAL, or None where no regular file of
    `dest_root`'s own reaches that path — the caller counts them, so this
    function and `mapping.count` cannot disagree about what a test is.

    ANNOTATED FOR WHAT IT RETURNS (Copilot, round 5 on #1080, accurate): it
    said `int | None` while returning `read_bytes()`, so a type checker read
    the `mapping.count(blob)` at its one call site as an incompatible
    argument — a docstring's claim about its own signature, wrong in the
    direction that makes the reader distrust the checker rather than the code.

    NO COMPONENT MAY BE A SYMLINK, not merely the last one (Copilot, second
    round on #1080, and its third-round restatement — which was right about a
    half the first fix did not cover and this lane's own reply got wrong).
    `read_bytes()` follows a link, so an arrival path that is a link to a
    test-bearing file elsewhere satisfied a row's declaration with a file that
    never arrived; `lstat` closes that, but `lstat` does not follow only the
    FINAL component, so `tests/` being a link to a directory full of suites
    was still counted. Measured: `lstat` on a path whose PARENT is a link
    reports a regular file. Every component below `dest_root` is therefore
    checked, from the top down.

    It is also the right reading of the manifest's own grammar: `git_mode:
    120000` is admitted, and a symlink's BYTES are its target path, which
    carries no `def test_` — so a link row declares zero and collects zero
    either way, while a link standing in for a REAL row is an absent arrival.
    `verify-carve-arrival.py` reads the destination with `lstat` and treats a
    link as a git link blob, for the same reason.
    """
    current = dest_root
    parts = relpath.split("/")
    for name in parts:
        current = current / name
        try:
            status = current.lstat()
        except OSError:
            return None
        if stat.S_ISLNK(status.st_mode):
            return None
    if not stat.S_ISREG(status.st_mode):
        return None
    try:
        return current.read_bytes()
    except OSError:
        return None


def _tree_tests(dest_root: Path) -> tuple[int, int]:
    """The CONTEXT figure: every `def test_` this checkout carries, in ITS OWN
    files. Never part of the floor — the floor is the declared arrivals — and
    printed beside them so a reader can see how much of a destination's suite
    the manifest speaks for.

    THE POPULATION IS THE WORKING TREE, said exactly because the number moves
    (Copilot, round 7 on #1080): every `.py` file PRESENT under `--dest-root`,
    tracked or not, minus nested checkouts and symlinks. An untracked scratch
    file therefore raises it, and that is the honest reading for a figure
    captioned "the tree carries" — a leg is verified where it stands, not
    where its index says it stands. Nothing is asserted against it: the floor
    is `declared` against `collected`, both of which are read from the
    manifest's own rows.

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
                try:
                    found = mapping.count(entry.read_bytes())
                except OSError:
                    continue
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
    above: list[dict[str, Any]] = []
    for source_path, relpath in owed:
        want = counts[source_path]
        declared += want
        blob = _tests_in(dest_root, relpath)
        found = None if blob is None else mapping.count(blob)
        if found is None:
            if want:
                absent.append({"source_path": source_path, "path": relpath,
                               "declared": want})
            continue
        collected += found
        if found < want:
            below.append({"source_path": source_path, "path": relpath,
                          "declared": want, "found": found})
        elif found > want:
            # BOTH SIGNS, BECAUSE THE RUNBOOK PROMISES BOTH (Copilot, round 7
            # on #1080). The documented reason the REFUSAL is a total and not
            # a per-row equality is that "a canceling pair holds a total while
            # a file loses coverage" — and only the negative half was
            # reported, so the retained column's real `+20` named no arrival
            # at all and the pair could not be inspected. A row ABOVE its
            # declaration is not a fault (a leg may add tests to a file it
            # received, and § 3.4's RULED re-homings do exactly that); it is
            # the other half of the evidence.
            above.append({"source_path": source_path, "path": relpath,
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
        "above_declaration": above,
        "tree_tests": tree,
        "tree_files": tree_files,
    }
    if collected < declared:
        # BOTH SIGNS ON THE REFUSAL PATH TOO (Copilot, round 9 on #1080,
        # accurate about this act's own runbook sentence). The passing report
        # prints the positive deltas; the REFUSAL printed only the negative
        # ones, so exactly the run that needs the canceling pair explained —
        # one row short, another over — named half of it. A shortfall's cause
        # is often a row that gained tests elsewhere, and the runbook promises
        # the deltas BY NAME in both directions.
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
            + (f"ABOVE DECLARATION (the other half of any canceling pair): "
               f"{', '.join(item['path'] for item in above[:5])}. "
               if above else "")
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
        # AT ZERO THIS LINE IS NOT PRINTED, because no landed retirement
        # carries a replica; where one does, the surviving copies are the
        # difference between the row's `−tests` term and its `0`, and a
        # reader who cannot see them cannot check the arithmetic.
        if item["homes"]:
            print(f"          copies SURVIVING the retirement at "
                  f"{', '.join(item['homes'])}")


def _print_destination(summary: dict[str, Any]) -> None:
    print(f"OK FLOOR PART 2 (destination) {summary['repository']} at "
          f"{summary['dest_root']}: {summary['collected']} `def test_` "
          f"collected at {summary['rows_owed']} declared arrival path(s), "
          f"against {summary['declared']} declared "
          f"({summary['collected'] - summary['declared']:+d}); "
          f"{summary['replicas_declared']} replica placement(s) declared; "
          f"the tree carries {summary['tree_tests']} across "
          f"{summary['tree_files']} file(s)")
    # BOTH LISTS, ALWAYS, AT ZERO TOO (Copilot, round 4 on #1080). `absent`
    # was collected and never printed on a passing run, so a declared arrival
    # that is NOT THERE could be hidden by another path carrying extra tests:
    # `collected == declared`, exit 0, and the per-row delta the runbook
    # promises by name was not shown. A missing file is the more serious of
    # the two and was the silent one.
    print(f"  declared arrivals ABSENT: {len(summary['absent'])}")
    for item in summary["absent"]:
        print(f"      {item['path']} — declared {item['declared']}, "
              "nothing regular at that path")
    print(f"  rows below their declaration: {len(summary['below_declaration'])}")
    for item in summary["below_declaration"]:
        print(f"      {item['path']} — declared {item['declared']}, "
              f"found {item['found']}")
    print("  rows above their declaration: "
          f"{len(summary['above_declaration'])}")
    for item in summary["above_declaration"]:
        print(f"      {item['path']} — declared {item['declared']}, "
              f"found {item['found']} (+{item['found'] - item['declared']})")


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
