"""FLOOR PART 2 OF THE RULED FOUR-PART FLOOR — the source→destination TEST
MAPPING with declared multiplicity (RULED OQ-1, RESTATED BY RULING OQ-K).

`split-opendox-two-layer-product` § 5.4 and design § D6 (2). FLOOR PART 1 is
`docs/opendox-carve-manifest.yaml` and its two tools; this file is part 2's
arithmetic, and `scripts/verify-carve-test-mapping.py` is its entry point.

**IT IS A MAPPING AND NOT A SCALAR EQUALITY, WHICH IS THE WHOLE POINT OF
RULING OQ-K** (Brett Heap, 2026-09-09T22:19:57Z, `opensoft/openxFactory#656`
comment `5609526215`, verbatim: *"OQ-K → FLOOR PART 2 restated as a
source→destination mapping with declared multiplicity for replicated files (a
small amendment PR to the change)"*). The ratified text before it asked the
post-split test counts to SUM to the pre-split count, and that equality is
false BY DESIGN: `tasks.md` § 3.7 requires EVERY destination to pass the
neutral conformance corpus, so three replicated modules carrying 30 `def test_`
have three homes each and the sum exceeds the source by 60 on its first run.
The only mechanical repair would have been to DELETE replicas that FLOOR PART 3
requires. A mapping is re-evaluated from the manifest; a scalar in a ratified
document is re-falsified by every merge.

WHAT A TEST FUNCTION IS, HERE, IN ONE PLACE — `scripts/carve_lines.py`'s
precedent exactly, and for its reason. § 5.4's clauses are written in terms of
`def test_`, so a count is a claim about a COUNTING RULE and two tools that
counted differently would disagree about whether a test was lost. `DEFINITION`
below is that rule, quoted rather than paraphrased by the verifier, the runbook
and the tests. Measured over all 456 rows of the landed manifest at
`carve_commit`: counting OCCURRENCES of the literal and counting LINES THAT
CONTAIN it give the same answer on every row, so the corpus does not choose
between them — the rule is declared anyway, because the next corpus might.

**THE PREDICATES ARE IMPORTED, NEVER COPIED.** `effective_arrival` and
`retired_at` are `carved_reach`'s, by assignment, so this file holds no fourth
copy of either. The three existing copies live in
`validate-carve-manifest.py`, `verify-carve-arrival.py` and `carved_reach.py`
and are kept in step by a table test, for the reason those files give: the
first two are hyphenated entry points that cannot be imported. This one is not
hyphenated, so the sharing `carve_lines.py` doctrine asks for is available and
is taken — and `tests/carve_test_mapping/` asserts the identity rather than a
resemblance.

THE FOUR CLAUSES, AND WHICH OF THEM THIS MODULE ANSWERS.

**(a) TOTAL COVERAGE.** Every file in the declared surface carrying at least one
`def test_` has at least ONE post-split home named by its OWN ROW. A file with
tests and no home is a LOST TEST and the carve REFUSES `test-home-missing`. A
`deleted_at_carve` row carrying `def test_` is the same refusal under its own
name, `test-home-deleted-at-carve` — deleting tests is a decision to be RULED,
never inferred from a disposition. `homes_of()` is the reading.

**(b) DECLARED MULTIPLICITY.** A `not_moved / replicated_at_destination` row
THAT CARRIES TESTS declares the set of REPOSITORIES its copies land in, the
retained `openxFactory` one included, and `m` is that set's size. An undeclared
set on a test-bearing row makes clause (c) uncomputable, which is a REFUSAL —
`replica-multiplicity-undeclared` — and never a pass. A ZERO-TEST replica is
outside the clause: its term is `(m − 1) × 0 = 0` whatever its set, so it can
neither move the sum nor make it uncomputable, and its replica set is FLOOR
PART 1's business. See `DECLARED_REPLICA_SETS` for where the declaration lives
and why it is not in the manifest yet.

**(c) THE SUM CHECK, OVER DECLARED MULTIPLICITIES.** `totals()` computes it and
the verifier prints every term. The box states it in three terms; this module
computes FOUR, and the fourth is not an amendment to the rule but an arithmetic
consequence of a LATER one — see THE RETIREMENT TERM below.

**(d) PINNED BY TEST** at each destination and in `openxFactory`, the way
`.github/workflows/pytest-suite.yml` pins this repository's collection triple —
SKIPPED exactly, SELECTED and PASSED as FLOORS, failures and errors zero. That
clause is a WORKFLOW obligation and not an arithmetic, so no function here
answers it. openxFactory's half is built (`pytest-suite.yml:603-720`). The
legs' half is BLOCKED, measured rather than assumed: both
`opensoft/openDox-code` and `opensoft/openXdox-code` run `python -m pytest -q
<named files> --noconftest` with no JUnit report and no totals, and both
workflows record the BUILD arc (`split-opendox` § 3.5/§ 3.6) as the reason —
*"with the root conftest in play the tree is 1188 errors and 0 passed"* and
*"THIRTY-SEVEN of this leg's 88 test files fail COLLECTION"*. A triple pinned
over a tree that cannot be collected is a required check held red by another
act's defect, which is the deadlock class clause (d) itself refuses by name.
`docs/opendox-cutover-runbook.md` § 9 carries that finding; this module does
not pretend to close it.

**THE RETIREMENT TERM, AND WHY IT IS ARITHMETIC AND NOT AN AMENDMENT.** § 5.4
was amended 2026-09-09. The `retired:` row form was RULED `5656343213` on
2026-09-13 and openxFactory PR #1043 is its first use, retiring two TEST-BEARING
rows — `tests/ideation-dashboard/test_intent_tray_dom.py` (23 `def test_`) and
`tests/ideation-dashboard/test_wheel_verbs_dom.py` (8) — whose arrival at
`opendox_code` is DELETED. Those 31 are in `source_count` and are at no home, so
the box's three-term identity is false by exactly 31 from that landing onward.
The check carries the term and prints it:

    Σ(destinations) = source_count
                    + Σ over replicated rows of (m − 1) × row_test_count
                    − Σ over RETIRED rows of row_test_count

A retired row is NOT `test-home-missing`. The form REQUIRES a `ruling:` and
reads as no retirement without one (`retired_at`'s guard), so the deletion is
exactly the RULED decision clause (a) demands and never one inferred from a
disposition — and it is ADMITTED AND NAMED, path, count and ruling, never
silent. Registered for the packet's next amendment; a tool does not edit
`tasks.md`.

**WHAT "A DESTINATION'S COLLECTED `def test_`" IS COUNTED OVER, decided by
measurement.** The silent-drop case refuses when a destination's collected
count falls BELOW the total its own rows declare. Counted over the ARRIVAL
PATHS the manifest names — not over the destination's whole tree — because the
two differ by the destinations' OWN work, which no row declares: measured
2026-09-16 at `openDox-code 0b4e8bb` the rows' paths carry 1,067 `def test_`
and the tree carries 1,324; at `openXdox-code 0a0265f`, 2,319 against 2,555. A
floor resting on the larger number drifts with another repository's unrelated
commits and stops being a claim about the carve.

**THIS FLOOR COMPARES NO BYTES, WHICH IS WHY IT TAKES A REPLICA THE ARRIVAL
VERIFIER MUST NOT BE GIVEN.** `docs/opendox-cutover-runbook.md` § 2 instructs
the operator NOT to declare `tests/corpus-adapter/test_conformance.py` to
`verify-carve-arrival.py`, because its implementation-aware block (`:72-84`)
imports the home factory and must be rewritten at each destination — neither
verbatim nor declared-edit, so a declaration would refuse on the digest. A
`def test_` count survives that rewrite untouched, so the same row is the one
THIS floor most needs declared: 20 of the 30 replicated test functions are in
it. Same flag spelling, different question, opposite instruction — said here
because an operator reading § 2 across would drop two thirds of the replica
term.

**AND WHY THE REFUSAL IS THE DESTINATION TOTAL AND NOT A PER-ROW EQUALITY, also
decided by measurement.** `tests/ideation-dashboard/test_serve_column_split.py`
is a `not_moved / stays_openxfactory_adapter` row declaring 9 `def test_` at
`carve_commit`; it carries 8 on `main` today. Nothing was lost: § 3.4 slice S6
(RULED Q4, `#656` comment `5642758731`) moved that test's SUBJECT out of the
file's domain, the file records the move in place at `:235-246`, and the
successor runs at `opensoft/openDox-code`'s
`tests/test_source_core_arm.py::test_route_dispatches_the_exact_arm_before_the_prefix_arm`.
A per-row equality would go red on a RULED re-homing that lost nothing. So the
REFUSAL is the total the box words it as, and the per-row deltas are REPORTED
BY NAME on every run — because a canceling pair holds a total while a file
loses coverage, which is the defect `pytest-suite.yml` records about its own
aggregate pin, and a number nobody prints is a number nobody checks.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, NamedTuple

# `scripts/` on the path before the local imports, the same two lines
# `validate-carve-manifest.py` opens with and for the same reason: this file is
# imported both as `scripts.carve_test_mapping` from a test and bare from a
# hyphenated entry point loaded by `spec_from_file_location`.
_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:  # pragma: no branch - trivial guard
    sys.path.insert(0, _SCRIPTS_DIR)

import carved_reach  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# RULED OQ-E's path, the same constant FLOOR PART 1 carries.
MANIFEST_RELPATH = "docs/opendox-carve-manifest.yaml"

# THE FLOOR'S SENTENCE, in one place, quoted by the verifier, the runbook and
# the tests rather than paraphrased four times.
DEFINITION = ("a test function is one occurrence of the literal `def test_` in "
              "a file's raw bytes at `carve_commit`, and a file CARRIES TESTS "
              "where that count is one or more")

TEST_MARKER = b"def test_"

# The retained column. NOT a `destinations:` key — the manifest declares what
# LEAVES, and openxFactory is where a `not_moved` row stays — so it is named by
# its REPOSITORY, which is `source_repository:` in the document itself.
RETAINED_TOKEN = "openxFactory"

MOVED_DISPOSITIONS: tuple[str, ...] = ("moved_verbatim",
                                       "moved_with_declared_edit")
NOT_MOVED = "not_moved"
REPLICA_REASON = "replicated_at_destination"
DELETED_REASON = "deleted_at_carve"
STAYS_REASONS: tuple[str, ...] = ("stays_openxfactory_adapter",
                                  "stays_openxfactory_governance")

# THE VOCABULARY, CLOSED. Four of the five are § 5.4's own named cases; the
# fifth is the I/O refusal every tool in this family carries
# (`carve-unreadable`, `arrival-unreadable`) — a question this floor cannot ask
# is never a pass.
REFUSAL_CODES: tuple[str, ...] = (
    "test-home-missing",
    "test-home-deleted-at-carve",
    "replica-multiplicity-undeclared",
    "destination-test-shortfall",
    "test-mapping-unreadable",
)

REMEDIATION = (
    "Remediation: FLOOR PART 2 is a MAPPING, so the repair is always a "
    "DECLARATION and never a deletion. `test-home-missing` — give the row a "
    "home, or, where the tests really are to go, take a RULING and record it "
    "in the row (`retired:` carries one and requires it). "
    "`test-home-deleted-at-carve` — the same, under the disposition that "
    "cannot carry a ruling at all. `replica-multiplicity-undeclared` — name "
    "the repositories the replica lands in; an undeclared set makes the sum "
    "uncomputable and an uncomputable check is not a pass. "
    "`destination-test-shortfall` — the destination is carrying fewer "
    "`def test_` than its own rows declare, so either the arrival is "
    "incomplete or a declared act removed tests without declaring it; never "
    "lower the declaration to meet the tree. Deleting a replica to make an "
    "arithmetic hold breaks FLOOR PART 3, which requires every destination to "
    "pass the conformance corpus."
)


class TestMappingRefusal(Exception):
    """A named, remediable refusal — `ArrivalRefusal`'s shape, so a caller
    branches on `code` without parsing prose and `render()` is the one place
    the human message (and its remediation trailer) is assembled."""

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(code, detail)

    def render(self, where: str) -> str:
        return f"FAIL {where}: {self.code} — {self.detail}\n{REMEDIATION}"


# --------------------------------------------------------------------------
# the counting rule
# --------------------------------------------------------------------------

def count(content: bytes) -> int:
    """How many test functions `content` carries, under `DEFINITION`.

    ON RAW BYTES, never a decoded string: a carve blob is whatever git holds,
    and `carve_lines.py` already records why a floor question must not depend
    on Unicode's opinion of the file. `b"def test_"` is pure ASCII, so the
    count is the same under every encoding that can hold the file at all — and
    a file that no decoder can hold is still answerable.
    """
    return content.count(TEST_MARKER)


# --------------------------------------------------------------------------
# the row predicates — IMPORTED, not copied
# --------------------------------------------------------------------------

# RULED Q6 and RULED 5656343213. `carved_reach` is importable and already holds
# both; assigning them here means this file cannot drift from it, which is
# strictly stronger than the table test that keeps the three hyphenated copies
# in step. `tests/carve_test_mapping/` asserts the IDENTITY (`is`), so a future
# copy-paste into this file fails a test rather than passing review.
effective_arrival = carved_reach.effective_arrival
retired_at = carved_reach.retired_at


def under_surface(path: str, moved_paths: list[str]) -> bool:
    """Is `path` under one of the manifest's declared prefixes, or named
    exactly? Segment-aware, so `scripts/ideation_dashboard` does not swallow
    `scripts/ideation_dashboard_old/x.py`.

    The fourth reading of FLOOR PART 1's `in_surface`, and the one predicate
    here that IS a copy — `validate-carve-manifest.py` is hyphenated and holds
    the only other one. `tests/carve_test_mapping/` compares the two over every
    row of the landed manifest and over the adversarial prefix case, the idiom
    `test_both_tools_read_the_effective_arrival_identically` sets.
    """
    for entry in moved_paths:
        prefix = entry.rstrip("/")
        if path == prefix or path.startswith(prefix + "/"):
            return True
    return False


def ruling_of(row: dict[str, Any]) -> str | None:
    """The `retired:` block's citation, read ONLY where `retired_at` has
    already accepted the block — so a half-written retirement can never
    contribute a ruling to a report that says the deletion was ruled."""
    if retired_at(row)[1] is None:
        return None
    return row["retired"].get("ruling")


# --------------------------------------------------------------------------
# clause (b) — the declared replica sets
# --------------------------------------------------------------------------

# WHERE THE DECLARATION LIVES, AND WHY IT IS NOT IN THE MANIFEST.
#
# Clause (b) owes FLOOR PART 1 a field on a test-bearing replica row naming the
# REPOSITORIES its copies land in. That field does not exist: the manifest says
# so itself (`docs/opendox-carve-manifest.yaml`, "THIS IS NOT RULING OQ-K'S
# OWED FLOOR PART 2 FIELD … the packet spells no name for it and its
# enumeration currently lives in the amendment record's prose") and
# `validate-carve-manifest.py` repeats it. § 5.4 says what to do until it
# lands, in terms: "the row grammar … gains the field in FLOOR PART 1's OWN
# successor pull request (the manifest is not this packet's file), and until it
# lands THE ENUMERATION BELOW IS THE DECLARATION" — and the enumeration is
# `openxFactory` (retained) · `opensoft/openDox-code` · `opensoft/openXdox-code`,
# `m = 3` for each of the three test-bearing replicated rows.
#
# So this table IS that enumeration, transcribed, and it is deliberately NOT a
# new field in a new file: pre-naming the key would decide, in this act, a
# grammar question the packet assigns to another one. Two pins keep it honest
# and both are in `tests/carve_test_mapping/`:
#
#   * its KEYS are pinned to the MANIFEST — they must be exactly the
#     test-bearing `replicated_at_destination` rows, machine-derived — so a
#     replica that starts carrying tests, or a new one, is a REFUSAL
#     (`replica-multiplicity-undeclared`) until it is declared, and a stale key
#     is `test-mapping-unreadable`; and
#   * its VALUES are pinned to the PACKET'S OWN declaration text, so the three
#     repositories and `m = 3` cannot drift from § 5.4 silently.
#
# WHEN THE FIELD LANDS, that pull request replaces this table with the row
# read; `declared_replica_set()` is the one function it has to change.
#
# REPOSITORIES AND NOT `destinations:` KEYS, which the manifest is explicit
# about: "`also_replicated_to:` names `destinations:` KEYS for arrival
# admission; the owed field names REPOSITORIES for an arithmetic. One row could
# carry both without either meaning the other."
_THREE_HOMES: tuple[str, ...] = ("opensoft/openxFactory",
                                 "opensoft/openDox-code",
                                 "opensoft/openXdox-code")

DECLARED_REPLICA_SETS: dict[str, tuple[str, ...]] = {
    "tests/corpus-adapter/test_conformance.py": _THREE_HOMES,
    "tests/corpus-adapter/test_interface_closure.py": _THREE_HOMES,
    "tests/corpus-adapter/test_no_home_vocabulary.py": _THREE_HOMES,
}

MULTIPLICITY_DECLARATION = (
    "`split-opendox-two-layer-product` tasks.md § 5.4 clause (b), design § D6 "
    "(2)(b), RULING OQ-K (`opensoft/openxFactory#656` comment `5609526215`): "
    "\"For this carve the declared set is, for all three test-carrying "
    "replicated rows, `openxFactory` (retained) · `opensoft/openDox-code` · "
    "`opensoft/openXdox-code` — so `m = 3`\", and \"until it lands the "
    "enumeration below IS the declaration\""
)


def declared_replica_set(row: dict[str, Any]) -> tuple[str, ...] | None:
    """The repositories a replica row's copies land in, or None where the row
    is not a replica at all.

    THE ROW WINS WHERE IT SPEAKS, which is nowhere today: the field is FLOOR
    PART 1's to add and this function is the single seam that act edits.
    """
    if not is_replica(row):
        return None
    return DECLARED_REPLICA_SETS.get(row["source_path"])


def is_replica(row: dict[str, Any]) -> bool:
    return (row.get("disposition") == NOT_MOVED
            and row.get("reason") == REPLICA_REASON)


# --------------------------------------------------------------------------
# the mapping
# --------------------------------------------------------------------------

class RowMapping(NamedTuple):
    """One row's answer to § 5.4: how many tests it carries and where they
    live afterwards."""

    source_path: str
    tests: int
    homes: tuple[str, ...]
    kind: str          # moved | retained | replicated | retired | deleted
    ruling: str | None  # the retirement's citation, where kind == "retired"


def repository_of(doc: dict[str, Any], key: Any) -> str:
    """A `destinations:` key resolved to its repository, `RETAINED_TOKEN` to
    the manifest's own `source_repository`."""
    if key == RETAINED_TOKEN:
        return str(doc["source_repository"])
    destinations = doc.get("destinations") or {}
    entry = destinations.get(key)
    if not isinstance(entry, dict) or not isinstance(entry.get("repository"),
                                                     str):
        raise TestMappingRefusal(
            "test-mapping-unreadable",
            f"destination {key!r} is not a key of the manifest's "
            "`destinations:` map, and is not the retained column "
            f"{RETAINED_TOKEN!r}")
    return entry["repository"]


def homes_of(doc: dict[str, Any], row: dict[str, Any]) -> RowMapping:
    """Clause (a) and clause (b), read off ONE ROW.

    The reading is § 5.4's own, limb by limb: a moved row's home is its
    EFFECTIVE arrival (RULED Q6 moves it, RULED 5656343213 DELETES it); a
    `stays_openxfactory_*` reason is a home AT openxFactory; a
    `replicated_at_destination` row is a home at openxFactory PLUS every home
    it declares; `deleted_at_carve` is no home at all.

    `tests` is filled in by the caller, which is what makes this pure.
    """
    source_path = row["source_path"]
    disposition = row.get("disposition")
    if disposition in MOVED_DISPOSITIONS:
        # A MOVED ROW THAT IS ALSO REPLICATED (RULED Q-L7 (a)) has its bytes at
        # the arrival AND at every destination the field lists. Its tests
        # therefore have more than one home and enter the excess term exactly
        # as a replica's do — measured at the landed manifest the one such row
        # carries ZERO tests, so the term is 0 today and is computed anyway,
        # because a zero that is assumed is a zero nobody re-measures.
        also = row.get("also_replicated_to")
        extra = tuple(repository_of(doc, key) for key in also) \
            if isinstance(also, list) else ()
        if retired_at(row)[1] is not None:
            return RowMapping(source_path, 0, extra, "retired", ruling_of(row))
        key, _path = effective_arrival(row)
        # A MOVED ROW THAT NAMES NO DESTINATION HAS NO HOME, and that is
        # clause (a)'s FIRST LIMB verbatim — "its row names no home — no
        # `destination`". FLOOR PART 1 refuses the same row
        # `carve-shape-invalid`, and this floor must not hide behind that: the
        # two tools are run in different places (this one at a destination
        # too), and "validate the manifest first" is not an answer to "where
        # did 35 tests go". An absent or non-string key is NO HOME; a
        # non-empty key that is not in `destinations:` is a VOCABULARY error
        # and stays unreadable here, because FLOOR PART 1 answers it by name
        # (`carve-vocabulary-unknown`) and a second name for it would be a
        # second vocabulary.
        if not isinstance(key, str) or not key:
            return RowMapping(source_path, 0, extra, "moved", None)
        return RowMapping(source_path, 0,
                          (repository_of(doc, key),) + extra, "moved", None)
    if disposition == NOT_MOVED:
        reason = row.get("reason")
        if reason in STAYS_REASONS:
            return RowMapping(source_path, 0,
                              (repository_of(doc, RETAINED_TOKEN),),
                              "retained", None)
        if reason == REPLICA_REASON:
            declared = declared_replica_set(row)
            return RowMapping(source_path, 0, tuple(declared or ()),
                              "replicated", None)
        if reason == DELETED_REASON:
            return RowMapping(source_path, 0, (), "deleted", None)
    raise TestMappingRefusal(
        "test-mapping-unreadable",
        f"row {source_path!r} carries disposition {disposition!r} / reason "
        f"{row.get('reason')!r}, which FLOOR PART 1's own vocabulary does not "
        "hold — validate the manifest before asking this floor anything")


def tests_at_carve(repo: Path, doc: dict[str, Any]) -> dict[str, int]:
    """Every row's `def test_` count in its blob AT `carve_commit`.

    ONE `git cat-file --batch`, not 456 invocations: the referent is a single
    commit and the answer must not depend on the working tree, which under
    `phase: post-shed` no longer carries 319 of these paths at all. A row whose
    blob is missing at the referent is FLOOR PART 1's `carve-digest-mismatch`
    territory and is reported here as unreadable rather than silently counted
    as zero — a lost test must never look like a file with no tests.
    """
    paths = [row["source_path"] for row in doc["rows"]]
    commit = doc["carve_commit"]
    # THE BATCH PROTOCOL IS NEWLINE-DELIMITED, so a path holding one would
    # desync the reply parse and start attributing blobs to the wrong rows —
    # a silent MIS-COUNT, which is the one failure mode a floor must never
    # have. Git permits such a path and FLOOR PART 1's own tests carry paths
    # UTF-8 cannot hold, so this is refused rather than assumed away.
    newlined = [path for path in paths if "\n" in path or "\r" in path]
    if newlined:
        raise TestMappingRefusal(
            "test-mapping-unreadable",
            f"{len(newlined)} row source_path(s) carry a line terminator, "
            "which `git cat-file --batch` cannot be asked about one per line: "
            f"{newlined[0]!r}")
    request = "".join(f"{commit}:{path}\n" for path in paths)
    done = subprocess.run(["git", "-C", str(repo), "cat-file", "--batch"],
                          input=request.encode("utf-8", "surrogateescape"),
                          capture_output=True, check=False)
    if done.returncode != 0:
        raise TestMappingRefusal(
            "test-mapping-unreadable",
            f"`git cat-file --batch` failed in {repo}: "
            f"{done.stderr.decode('utf-8', 'replace').strip()}")
    out = done.stdout
    counts: dict[str, int] = {}
    cursor = 0
    for path in paths:
        end = out.find(b"\n", cursor)
        if end < 0:
            raise TestMappingRefusal(
                "test-mapping-unreadable",
                f"`git cat-file --batch` ended before answering for {path!r}")
        header = out[cursor:end].decode("utf-8", "replace").split()
        if len(header) != 3 or header[1] != "blob":
            raise TestMappingRefusal(
                "test-mapping-unreadable",
                f"{path!r} is not a blob at {commit[:12]} "
                f"({' '.join(header)}) — validate the manifest first")
        size = int(header[2])
        counts[path] = count(out[end + 1:end + 1 + size])
        cursor = end + 1 + size + 1
    return counts


def map_rows(doc: dict[str, Any],
             counts: dict[str, int]) -> list[RowMapping]:
    """Every row of the declared surface, with its count and its homes.

    OUT-OF-SURFACE ROWS ARE SKIPPED AND COUNTED, never assumed absent: § 5.4
    binds "every file in the manifest's DECLARED SURFACE", and FLOOR PART 1's
    check 4 walks that surface from the other direction. The landed manifest
    has none outside it, which `tests/carve_test_mapping/` asserts rather than
    this function assuming.
    """
    moved_paths = doc["moved_paths"]
    mapped: list[RowMapping] = []
    for row in doc["rows"]:
        source_path = row["source_path"]
        if not under_surface(source_path, moved_paths):
            continue
        base = homes_of(doc, row)
        mapped.append(base._replace(tests=counts[source_path]))
    return mapped


def refuse_lost_tests(mapped: list[RowMapping]) -> None:
    """Clause (a), and clause (b)'s refusal, in the order § 5.4 states them."""
    for record in mapped:
        if record.tests and record.kind == "deleted":
            raise TestMappingRefusal(
                "test-home-deleted-at-carve",
                f"{record.source_path} carries {record.tests} `def test_` and "
                f"is dispositioned `not_moved / {DELETED_REASON}`, so those "
                "tests exist nowhere after the carve. Deleting tests is a "
                "decision to be RULED and recorded, never inferred from a "
                "disposition")
    for record in mapped:
        if record.tests and record.kind == "replicated" and not record.homes:
            raise TestMappingRefusal(
                "replica-multiplicity-undeclared",
                f"{record.source_path} is `not_moved / {REPLICA_REASON}` and "
                f"carries {record.tests} `def test_`, and no replica set is "
                "declared for it, so `Σ over replicated rows of (m − 1) × "
                "row_test_count` is UNCOMPUTABLE. An uncomputable check is "
                f"never a pass. The declaration is {MULTIPLICITY_DECLARATION}")
    for record in mapped:
        if record.tests and not record.homes and record.kind != "retired":
            raise TestMappingRefusal(
                "test-home-missing",
                f"{record.source_path} carries {record.tests} `def test_` and "
                "its row names no home — no destination, and no `not_moved` "
                "reason that constitutes one. That is a LOST TEST")


def known_repositories(doc: dict[str, Any]) -> tuple[str, ...]:
    """Every repository this manifest can speak for: its own, plus each
    `destinations:` entry's."""
    return tuple(dict.fromkeys(
        [repository_of(doc, RETAINED_TOKEN)]
        + [repository_of(doc, key) for key in (doc.get("destinations") or {})]))


def refuse_unknown_declared_homes(doc: dict[str, Any],
                                  mapped: list[RowMapping]) -> None:
    """A declared replica set may only name repositories THIS manifest knows.

    Without this the two vocabularies could drift apart in the one way nothing
    else would catch: `DECLARED_REPLICA_SETS` spells repositories and the
    manifest spells `destinations:` keys, so a repository renamed in one and
    not the other would quietly open a SECOND per-repository column carrying
    the replica's tests — the identity would still hold, every total would be
    wrong, and the run would print an extra line nobody reads as an alarm.
    """
    known = set(known_repositories(doc))
    for record in mapped:
        if record.kind != "replicated":
            continue
        unknown = [home for home in record.homes if home not in known]
        if unknown:
            raise TestMappingRefusal(
                "test-mapping-unreadable",
                f"{record.source_path} declares replica home(s) "
                f"{', '.join(sorted(unknown))}, which this manifest does not "
                "know: its repositories are "
                f"{', '.join(sorted(known))}. The declaration names "
                "REPOSITORIES and the manifest names `destinations:` keys, so "
                "the two are kept in step here rather than left to drift")


def totals(doc: dict[str, Any], mapped: list[RowMapping]) -> dict[str, Any]:
    """Clause (c), every term computed from the manifest and none assumed."""
    refuse_unknown_declared_homes(doc, mapped)
    per_repository: dict[str, int] = {}
    for key in list(doc.get("destinations") or {}) + [RETAINED_TOKEN]:
        per_repository.setdefault(repository_of(doc, key), 0)
    source_count = 0
    replica_excess = 0
    also_replicated_excess = 0
    retired_total = 0
    for record in mapped:
        source_count += record.tests
        for home in record.homes:
            per_repository[home] = per_repository.get(home, 0) + record.tests
        if record.kind == "retired":
            retired_total += record.tests
        elif record.kind == "replicated" and record.homes:
            replica_excess += (len(record.homes) - 1) * record.tests
        elif len(record.homes) > 1:
            also_replicated_excess += (len(record.homes) - 1) * record.tests
    destinations_sum = sum(per_repository.values())
    return {
        "per_repository": per_repository,
        "source_count": source_count,
        "replica_excess": replica_excess,
        "also_replicated_excess": also_replicated_excess,
        "retired_total": retired_total,
        "destinations_sum": destinations_sum,
        "identity_holds": destinations_sum == (source_count + replica_excess
                                               + also_replicated_excess
                                               - retired_total),
    }
