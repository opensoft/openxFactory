"""The commission record's evaluation order and roster reproduction (data-model E2).

Feature 035, Phase 2. Written from the family's own specification only (R4).
The order is E2's steps 1 to 13, which commission (the producer) and admission
(the consumer) share; the first failing check names the outcome (R21). The
admission-only steps are three phases' or another repository's: A1 and A4 are
Phase 5's binding, A3 is Phase 3's retry identity, and A2 and A5 are 025's own
guards, outside the corpus. So at this commit the two boundaries differ in
these places only:

* A1 and A4, at admission only (Phase 5, T055): E10 steps 1 to 13 on the
  commission job's verified claims, after step 2, and E10 step 14, the
  workflow revision, after step 5 has checked the `governed` member it reads.
  An admission takes the binding (`inputs.binding`, with `inputs.operation`
  `commission`), the `identity` oracle and the identity map; a commission
  takes none of them. A SHARED commission vector carries no binding, so the
  consumer runs it without A1 and A4 (conformance-corpus § How each side runs
  a shared vector);

* step 4 compares the candidate with the trusted trigger's `expected_candidate`
  at commission, and with the consumer's own `resolved_candidate` at admission;
* step 5's last per-source check, `rule_superseded`, is normative at admission
  only (Brett Heap's OPEN-3 ruling of 2026-10-08, "History + unchanged rule
  file (Recommended)", and its follow-up 1, "Every governed source
  (Recommended)"); commission never reads a tip value;
* step 13 reads the live head as a list of reads at commission, and once at
  admission.

WHERE THE DATA-MODEL TEXT LEAVES AN ORDER OPEN, this module takes one reading
and the corpus pins it (tests/council_convening/test_resolution.py states each):
step 5's per-source checks run source by source; step 9's three checks run over
their own lists in turn; step 10 evaluates condition by condition and compares
consumed facts afterwards; step 11 checks every `held` before any seat; step 13
names the first read that is not the candidate's head.

THE ORACLES ARE INJECTED (R8). `resolve` reads authority, facts and heads only
through an `Oracles` object. `VectorOracles` answers from a corpus vector's
`environment` and records every read, which is how the tests show that a
secret-bearing record reaches no oracle and an unlisted governed repository
reaches no history. A read the vector cannot answer is a `HarnessError`, never
a pass and never a refusal.

THE SECRET FLOOR is the provider's own `SECRET_PATTERNS`, loaded from
`scripts/validate-domain-factory.py` by `importlib` and never copied (R9).

`check_offline` runs the same order with every oracle-dependent check skipped
and named, for the validator's `check` mode.
"""

from __future__ import annotations

import functools
import importlib.util
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator, Mapping

from ..signed_execution_chain import canonical
from . import assignments, binding, classification, predicates, records
from .records import Refused

REPLACEMENT = "xfc-resolved-council-1"
KIND = "xfactory_council_convening"
SCHEMA_ID = records.ID_BASE + "council-convening.schema.yaml"
DIGEST_SUBJECT = "council_convening"
BOUNDARIES = ("commission", "admission")
BOTH_SIDES = ["producer", "consumer"]
UNAVAILABLE = "unavailable"

REPO_ROOT = Path(__file__).resolve().parents[2]
SECRET_FLOOR = REPO_ROOT / "scripts" / "validate-domain-factory.py"

_FULL_SHA = re.compile(r"[0-9a-f]{40}")


class HarnessError(Exception):
    """The vector or the oracle data cannot be adjudicated. Never a refusal."""


class Routed(Exception):
    """A legacy record routed to the legacy verifier: no verdict from this family."""

    def __init__(self, outcome: records.Outcome):
        super().__init__("routed to the legacy verifier")
        self.outcome = outcome
        self.findings = tuple(outcome.findings)
        self.derived = dict(outcome.derived)


@dataclass(frozen=True)
class Resolution:
    required_seats: list
    convening_digest: dict
    #: Set only when admission RETURNED a live snapshot (E2 step A3): that
    #: snapshot's consumer-issued id. A fresh admission has none, because the
    #: consumer issues the id when it writes the snapshot.
    convening_id: str | None = None


# --------------------------------------------------------------------------
# The oracle interface (R8).
# --------------------------------------------------------------------------

class Oracles:
    """What a boundary may read. Every method may raise `HarnessError`."""

    def governed_repositories(self) -> list:
        raise NotImplementedError

    def governed_history(self, repository: str, revision: str) -> Mapping:
        raise NotImplementedError

    def rules(self, repository: str, revision: str) -> Mapping:
        raise NotImplementedError

    def governed(self, repository: str, revision: str, path: str) -> Mapping:
        raise NotImplementedError

    def facts(self, key: str) -> Any:
        raise NotImplementedError

    def live_heads(self, repository: str, pull_number: int) -> Any:
        raise NotImplementedError

    def head_ref(self, repository: str, pull_number: int) -> Any:
        raise NotImplementedError

    def resolved_candidate(self) -> Any:
        raise NotImplementedError

    def live_snapshots(self) -> list:
        """The consumer's snapshots that have not failed, for E2 step A3."""
        raise NotImplementedError

    def identity(self) -> Any:
        """The commission job's verified claims (E2 step A1), admission only."""
        raise NotImplementedError


class VectorOracles(Oracles):
    """Answers from a vector's `environment`, recording each read as
    `(oracle, key)`. Messages name the oracle, never a key or a value."""

    def __init__(self, environment: Mapping):
        if not isinstance(environment, Mapping):
            raise HarnessError("the vector's environment is not an object")
        self._environment = environment
        self.reads: list[tuple[str, Any]] = []

    def _oracle(self, name: str):
        if name not in self._environment:
            raise HarnessError(f"the vector carries no `{name}` oracle")
        return self._environment[name]

    def _entry(self, name: str, key: str):
        self.reads.append((name, key))
        table = self._oracle(name)
        if not isinstance(table, Mapping) or key not in table:
            raise HarnessError(f"the `{name}` oracle has no entry this boundary reads")
        return table[key]

    def governed_repositories(self) -> list:
        self.reads.append(("governed_repositories", None))
        value = self._oracle("governed_repositories")
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            raise HarnessError("the `governed_repositories` oracle is not a list of strings")
        return value

    def governed_history(self, repository, revision):
        return _mapping(self._entry("governed_history", f"{repository}@{revision}"),
                        "governed_history")

    def rules(self, repository, revision):
        return _mapping(self._entry("rules", f"{repository}@{revision}"), "rules")

    def governed(self, repository, revision, path):
        return _mapping(self._entry("governed", f"{repository}@{revision}:{path}"),
                        "governed")

    def facts(self, key):
        return self._entry("facts", key)

    def live_heads(self, repository, pull_number):
        return self._entry("live_heads", f"{repository}#{pull_number}")

    def head_ref(self, repository, pull_number):
        return self._entry("head_refs", f"{repository}#{pull_number}")

    def resolved_candidate(self):
        self.reads.append(("resolved_candidate", None))
        return self._oracle("resolved_candidate")

    def live_snapshots(self) -> list:
        """`environment.issued.live_snapshots`. An absent `issued`, or an
        `issued` without `live_snapshots`, is a consumer holding no live
        snapshot, so an admission vector authored before Phase 3 keeps its
        outcome."""
        self.reads.append(("issued", "live_snapshots"))
        issued = self._environment.get("issued", {})
        if not isinstance(issued, Mapping):
            raise HarnessError("the `issued` oracle is not an object")
        live = issued.get("live_snapshots", [])
        if not isinstance(live, list) or not all(
                isinstance(snapshot, Mapping) and isinstance(snapshot.get("convening"), Mapping)
                and isinstance(snapshot.get("convening_id"), str) for snapshot in live):
            raise HarnessError("`issued.live_snapshots` is not a list of snapshots")
        return live

    def identity(self):
        self.reads.append(("identity", None))
        return self._oracle("identity")


def _mapping(value, name):
    if not isinstance(value, Mapping):
        raise HarnessError(f"a `{name}` oracle entry is not an object")
    return value


# --------------------------------------------------------------------------
# Helpers.
# --------------------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def secret_patterns() -> tuple:
    """The provider's secret detector floor, by import, never copied (R9)."""
    name = "_council_convening_secret_floor"
    spec = importlib.util.spec_from_file_location(name, SECRET_FLOOR)
    if spec is None or spec.loader is None:
        raise HarnessError("the secret detector floor cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as error:  # noqa: BLE001 - any failure is a harness failure
        raise HarnessError("the secret detector floor cannot be loaded") from error
    finally:
        sys.modules.pop(name, None)
    return tuple(module.SECRET_PATTERNS)


@functools.lru_cache(maxsize=1)
def _default_schemas() -> records.SchemaSet:
    return records.load_schemas()


@functools.lru_cache(maxsize=1)
def _default_registry() -> classification.Registry:
    return classification.load_registry()


def _canonical(value) -> str:
    try:
        return canonical.serialize(value)
    except canonical.ConstructionError as error:
        raise HarnessError("oracle data is not canonicalizable") from error


def _same(left, right) -> bool:
    """Equality as canonical bytes, so `true` never equals `1`."""
    return _canonical(left) == _canonical(right)


def _bytewise(path: str) -> bytes:
    return path.encode("utf-8")


def _strictly_ascending(paths) -> bool:
    keys = [_bytewise(p) for p in paths]
    return all(a < b for a, b in zip(keys, keys[1:]))


def _strings(value) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str):
                yield key
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def convening_digest(record: Any) -> dict:
    """`xfc-jcs-sha256-1`, subject `council_convening`, over the whole record."""
    return {"construction": canonical.CONSTRUCTION, "subject": DIGEST_SUBJECT,
            "value": canonical.digest(record)}


def head_ref_matches(selector: Mapping, head_ref: str) -> bool:
    """`{exact: <head_ref>}` or `{glob: <pattern>}`, per data-model E3."""
    if "exact" in selector:
        return head_ref == selector["exact"]
    return _glob_regex(selector["glob"]).fullmatch(head_ref) is not None


@functools.lru_cache(maxsize=256)
def _glob_regex(pattern: str):
    """The governed envelope's matcher, restated: `*` is a run without `/`, `?`
    one character other than `/`, `**/` zero or more leading segments, `**` not
    followed by `/` anything; every other character is literal; anchored."""
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:[^/]*/)*")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("".join(out), re.DOTALL)


def select_class(selector, class_inputs) -> str | None:
    """The first entry whose repositories contain the candidate repository and
    whose head ref matches, or None."""
    for entry in selector:
        if (class_inputs["repository"] in entry["repositories"]
                and head_ref_matches(entry["head_ref"], class_inputs["head_ref"])):
            return entry["class"]
    return None


def expected_roster(standing_seats, conditions) -> list:
    """R6: the standing seats in order, then each held condition's seat in
    condition order, each appended only if absent."""
    roster = list(standing_seats)
    for condition in conditions:
        seat = condition["seat"]
        if condition["held"] and seat is not None and seat not in roster:
            roster.append(seat)
    return roster


def _projection_council(council) -> tuple[bool, Mapping]:
    """(classed, council) for a projection council of either form."""
    if not isinstance(council, Mapping):
        raise HarnessError("a projection council is not an object")
    if set(council) == {"class_selector", "classes"}:
        if not isinstance(council["class_selector"], list) or not isinstance(
                council["classes"], Mapping):
            raise HarnessError("a classed projection council is malformed")
        for entry in council["class_selector"]:
            if (not isinstance(entry, Mapping)
                    or set(entry) != {"class", "repositories", "head_ref"}
                    or not isinstance(entry["repositories"], list)
                    or not isinstance(entry["head_ref"], Mapping)
                    or len(entry["head_ref"]) != 1
                    or not set(entry["head_ref"]) <= {"exact", "glob"}):
                raise HarnessError("a projection class-selector entry is malformed")
        return True, council
    if set(council) == {"standing_seats", "conditions"}:
        return False, council
    raise HarnessError("a projection council is neither classed nor unclassed")


def _fact_key(contract: str, source, candidate, governed) -> str:
    if source == "candidate_pull":
        return (f"pr_facts:{candidate['repository']}#{candidate['pull_number']}"
                f"@{candidate['head_sha']}")
    if source == "candidate_subject":
        return (f"rule_facts:{candidate['repository']}@{candidate['head_sha']}"
                f":{candidate['subject_path']}")
    return (f"rule_facts:{governed['repository']}@{governed['revision']}"
            f":{source['governed_path']}")


# --------------------------------------------------------------------------
# The evaluation order.
# --------------------------------------------------------------------------

@dataclass
class _Run:
    boundary: str            # "commission", "admission" or "offline"
    oracles: Oracles | None
    expected_candidate: Mapping | None
    schemas: records.SchemaSet
    registry: classification.Registry
    skipped: list = field(default_factory=list)
    status_read: bool = False
    # E2 steps A1 and A4 (Phase 5): set at admission only, and never for a
    # shared commission vector run through admission.
    binding: Mapping | None = None
    identity_root: Path | None = None
    evaluation_time: str | None = None
    identity: Any = None
    permitted_workflow: Mapping | None = None

    @property
    def offline(self) -> bool:
        return self.boundary == "offline"

    def skip(self, rule: str) -> bool:
        """True, after naming the rule, when it needs an oracle and this is offline."""
        if self.offline:
            if rule not in self.skipped:
                self.skipped.append(rule)
            return True
        return False


def _shape(record, run: _Run) -> None:
    """Step 2: the schema, then the structural rules JSON Schema cannot state,
    then canonicalizability."""
    if run.schemas.errors(SCHEMA_ID, record):
        raise Refused("convening_malformed", "record")
    prov = record["required_seats_provenance"]
    if ("class_inputs" in prov) != ("matched_class" in prov):
        raise Refused("convening_malformed", "class_inputs")
    sources = prov["governed"]["sources"]
    if not _strictly_ascending([s["path"] for s in sources]):
        raise Refused("convening_malformed", "sources")
    files = {s["path"] for s in sources if s["kind"] == "file"}
    for source in sources:
        if source["kind"] == "listing":
            if not _strictly_ascending(source["entries"]):
                raise Refused("convening_malformed", "entries")
            if not set(source["entries"]) <= files:
                raise Refused("convening_malformed", "entries")
    contracts = [fs["input_contract"] for fs in prov["fact_sources"]]
    if len(set(contracts)) != len(contracts):
        raise Refused("convening_malformed", "fact_sources")
    try:
        canonical.serialize(record)
    except canonical.ConstructionError:
        raise Refused("value_not_canonicalizable", "record") from None


def _secrets(record) -> None:
    """Step 3, before any oracle is queried with a free-text value."""
    prov = record["required_seats_provenance"]
    scanned = {
        "packet_refs": record["packet_refs"],
        "class_inputs": prov.get("class_inputs", {}),
        "parameters": [condition["parameters"] for condition in prov["conditions"]],
        "consumed_facts": prov["consumed_facts"],
    }
    floor = secret_patterns()
    for member, value in scanned.items():
        for text in _strings(value):
            if any(pattern.search(text) for pattern in floor):
                raise Refused("secret_bearing_fact", member)


def _candidate(record, run: _Run) -> None:
    """Step 4."""
    prov = record["required_seats_provenance"]
    candidate = prov["candidate"]
    if record["subject_pin"] != candidate["head_sha"]:
        raise Refused("candidate_mismatch", "subject_pin")
    if run.boundary == "commission":
        expected = run.expected_candidate
        if not isinstance(expected, Mapping) or not expected:
            raise HarnessError("a commission vector carries no `expected_candidate`")
        for member, value in expected.items():
            if member not in candidate or not _same(candidate[member], value):
                raise Refused("candidate_mismatch", "candidate")
    elif not run.skip("candidate_mismatch (resolved candidate)"):
        if not _same(candidate, run.oracles.resolved_candidate()):
            raise Refused("candidate_mismatch", "candidate")
    if run.offline:
        run.skip("candidate_mismatch (expected candidate)")
    class_inputs = prov.get("class_inputs")
    if class_inputs is not None:
        if class_inputs["repository"] != candidate["repository"]:
            raise Refused("candidate_mismatch", "class_inputs")
        if not run.skip("candidate_mismatch (authoritative head ref)"):
            head_ref = run.oracles.head_ref(candidate["repository"], candidate["pull_number"])
            if not _same(class_inputs["head_ref"], head_ref):
                raise Refused("candidate_mismatch", "class_inputs")


def _governed(record, run: _Run):
    """Step 5. Returns the projection, or None offline."""
    governed = record["required_seats_provenance"]["governed"]
    repository, revision = governed["repository"], governed["revision"]
    if not isinstance(revision, str) or _FULL_SHA.fullmatch(revision) is None:
        raise Refused("mutable_rule_reference", "revision")
    projection = None
    if not run.skip("rule_unauthorized (governed repository)"):
        if repository not in run.oracles.governed_repositories():
            raise Refused("rule_unauthorized", "repository")
    if not run.skip("rule_revision_ungoverned"):
        history = run.oracles.governed_history(repository, revision)
        if "on_first_parent" not in history:
            raise HarnessError("a `governed_history` entry carries no `on_first_parent`")
        if history["on_first_parent"] is not True:
            raise Refused("rule_revision_ungoverned", "revision")
    if not run.skip("governed_sources_mismatch"):
        projection = run.oracles.rules(repository, revision)
        listed = projection.get("sources")
        if not isinstance(listed, list):
            raise HarnessError("a `rules` projection carries no source list")
        if {s["path"] for s in governed["sources"]} != set(listed):
            raise Refused("governed_sources_mismatch", "sources")
    for source in governed["sources"]:
        try:
            run.schemas.check_definition("relative_path", source["path"])
        except Refused:
            raise Refused("rule_path_malformed", "path") from None
        if run.skip("rule_unavailable") | run.skip("rule_unauthorized (governed source)") | \
                run.skip("rule_digest_mismatch"):
            continue
        entry = run.oracles.governed(repository, revision, source["path"])
        if "available" not in entry or "governed" not in entry:
            raise HarnessError("a `governed` entry lacks `available` or `governed`")
        if entry["available"] is not True:
            raise Refused("rule_unavailable", "path")
        if entry["governed"] is not True:
            raise Refused("rule_unauthorized", "path")
        value_member, tip_member = (("sha256", "tip_sha256") if source["kind"] == "file"
                                    else ("entries", "tip_entries"))
        if value_member not in entry:
            raise HarnessError("a `governed` entry lacks its value at the revision")
        if not _same(entry[value_member], source[value_member]):
            raise Refused("rule_digest_mismatch", "path")
        if run.boundary == "admission":
            if tip_member not in entry:
                raise HarnessError("an admission `governed` entry lacks its tip value")
            if not _same(entry[tip_member], entry[value_member]):
                raise Refused("rule_superseded", "path")
    if run.offline:
        run.skip("rule_superseded")
    return projection


def _council_and_class(record, projection, run: _Run):
    """Steps 6 and 7. Returns nothing; refuses or passes."""
    if run.skip("council_unknown") | run.skip("class_mismatch") | \
            run.skip("class_unresolved") | run.skip("rule_projection_mismatch"):
        return
    prov = record["required_seats_provenance"]
    councils = projection.get("councils")
    if not isinstance(councils, Mapping):
        raise HarnessError("a `rules` projection carries no councils")
    if record["council_id"] not in councils:
        raise Refused("council_unknown", "council_id")
    classed, council = _projection_council(councils[record["council_id"]])
    if classed != ("class_inputs" in prov):
        raise Refused("class_mismatch", "class_inputs")
    if classed:
        selected = select_class(council["class_selector"], prov["class_inputs"])
        if selected is None:
            raise Refused("class_unresolved", "class_inputs")
        if selected != prov["matched_class"]:
            raise Refused("class_mismatch", "matched_class")
        if selected not in council["classes"]:
            raise HarnessError("a projection selector names an undeclared class")
        klass = council["classes"][selected]
    else:
        klass = council
    if not isinstance(klass, Mapping) or set(klass) != {"standing_seats", "conditions"}:
        raise HarnessError("a projection class is malformed")
    # Step 7.
    if not _same(prov["standing_seats"], klass["standing_seats"]):
        raise Refused("rule_projection_mismatch", "standing_seats")
    without_held = [{k: v for k, v in c.items() if k != "held"} for c in prov["conditions"]]
    if not _same(without_held, klass["conditions"]):
        raise Refused("rule_projection_mismatch", "conditions")


def _record_facts(record):
    """Step 9. Returns (contracts in use, in condition order; source by contract)."""
    prov = record["required_seats_provenance"]
    candidate, governed = prov["candidate"], prov["governed"]
    conditions = prov["conditions"]
    in_use = list(dict.fromkeys(c["input_contract"] for c in conditions))
    governed_paths = {s["path"] for s in governed["sources"]}
    sources = {}
    for entry in prov["fact_sources"]:
        contract, source = entry["input_contract"], entry["source"]
        if contract == predicates.PR_FACTS:
            allowed = source == "candidate_pull"
        elif source == "candidate_subject":
            allowed = "subject_path" in candidate
        elif isinstance(source, Mapping):
            allowed = source["governed_path"] in governed_paths
        else:
            allowed = False
        if not allowed or contract not in in_use:
            raise Refused("fact_source_mismatch", "fact_sources")
        sources[contract] = source
    if any(contract not in sources for contract in in_use):
        raise Refused("fact_source_mismatch", "fact_sources")
    consumed = prov["consumed_facts"]
    read: dict[str, set] = {}
    for condition in conditions:
        facts = predicates.reads(condition["predicate"])
        read.setdefault(condition["input_contract"], set()).update(facts)
        have = consumed.get(condition["input_contract"], {})
        if any(fact not in have for fact in facts):
            raise Refused("opaque_conclusion", "consumed_facts")
    for contract, facts in consumed.items():
        if any(fact not in read.get(contract, ()) for fact in facts):
            raise Refused("facts_unused", "consumed_facts")
    return in_use, sources


def _authoritative(record, in_use, sources, run: _Run):
    """Step 10. Returns the reference evaluation of each condition, or None offline."""
    if run.skip("condition_unevaluable") | run.skip("consumed_facts_mismatch"):
        return None
    prov = record["required_seats_provenance"]
    authoritative = {
        contract: run.oracles.facts(_fact_key(contract, sources[contract],
                                              prov["candidate"], prov["governed"]))
        for contract in in_use}
    reference = [predicates.evaluate(c["predicate"], c["parameters"],
                                     authoritative[c["input_contract"]])
                 for c in prov["conditions"]]
    for contract in sorted(prov["consumed_facts"]):
        for fact, value in sorted(prov["consumed_facts"][contract].items()):
            truth = authoritative.get(contract)
            if not isinstance(truth, Mapping) or fact not in truth or not _same(value, truth[fact]):
                raise Refused("consumed_facts_mismatch", "consumed_facts")
    return reference


def _held_and_roster(record, reference, run: _Run) -> None:
    """Steps 11 and 12."""
    prov = record["required_seats_provenance"]
    conditions = prov["conditions"]
    if not run.skip("condition_result_mismatch"):
        for condition, held in zip(conditions, reference):
            if condition["held"] is not held:
                raise Refused("condition_result_mismatch", "held")
    for condition in conditions:
        if condition["held"] and condition["seat"] is None:
            raise Refused("condition_seat_unbound", "seat")
    seats = record["required_seats"]
    if not seats:
        raise Refused("roster_empty", "required_seats")
    if len(set(seats)) != len(seats):
        raise Refused("roster_duplicate_seat", "required_seats")
    if seats != expected_roster(prov["standing_seats"], conditions):
        raise Refused("roster_mismatch", "required_seats")


def _live_head(record, run: _Run) -> None:
    """Step 13, the last read of the candidate's head."""
    if run.skip("candidate_head_unavailable") | run.skip("candidate_head_moved"):
        return
    candidate = record["required_seats_provenance"]["candidate"]
    reads = run.oracles.live_heads(candidate["repository"], candidate["pull_number"])
    if isinstance(reads, str):
        reads = [reads]
    if not isinstance(reads, list) or not reads or (
            run.boundary == "admission" and len(reads) != 1):
        raise HarnessError("a `live_heads` entry is not a read this boundary takes")
    for head in reads:
        if head == UNAVAILABLE:
            raise Refused("candidate_head_unavailable", "candidate")
        if head != candidate["head_sha"]:
            raise Refused("candidate_head_moved", "candidate")


def _classify(record, run: _Run, selected_protocol, statuses) -> None:
    """Step 1 (data-model E1), through the Phase 1 classification module. A
    selection that names no registry entry is a harness error."""
    try:
        result = classification.classify_and_select(record, selected_protocol,
                                                    run.registry, statuses)
    except KeyError:
        raise HarnessError("the selected protocol names no registry entry") from None
    run.status_read = run.status_read or result.status_read
    if result.outcome == "refuse":
        raise Refused(result.refusal, "protocol")
    if result.outcome == "route":
        raise Routed(result)
    # A replacement record of any other kind, or of none, is the schema's to
    # refuse at step 2 (`convening_malformed`), never a harness error.


def _bound_claims(run: _Run) -> None:
    """E2 step A1: E10 steps 1 to 13, the binding instance and then the
    commission job's verified claims. It reads only the claims, never a
    free-text value of the record, so it may run before step 3. Offline it is
    named as not checkable, never passed."""
    if run.binding is None:
        run.skip("binding (E2 step A1: E10 steps 1 to 13 on the commission job's "
                 "verified claims, against the consumer's binding and identity map)")
        return
    binding.check_offline(run.binding, identity_root=run.identity_root,
                          schemas=run.schemas)
    run.identity = run.oracles.identity()
    try:
        run.permitted_workflow = binding.check_claims(
            run.binding, operation=ADMISSION_OPERATION, identity=run.identity,
            evaluation_time=run.evaluation_time)
    except ValueError as error:   # an instant that is not a `utc_instant`
        raise HarnessError(str(error)) from None


def _workflow_revision(record, run: _Run) -> None:
    """E2 step A4: E10 step 14, now that step 5 has checked `governed`."""
    if run.binding is None:
        run.skip("workflow_revision_ungoverned (E2 step A4: E10 step 14, the "
                 "commission job's verified job_workflow_sha against `governed`)")
        return
    try:
        binding.check_workflow_revision(
            run.permitted_workflow, identity=run.identity,
            governed=record["required_seats_provenance"]["governed"],
            governed_history=None)
    except ValueError as error:   # a rule the schema did not close, never a pass
        raise HarnessError(str(error)) from None


def _retry_identity(record, run: _Run) -> Resolution | None:
    """E2 step A3, admission only (Phase 3, T040): retry identity, then
    once-per-pin, over the consumer's live snapshots. It runs after
    classification and shape and before every check that reads something that
    can drift, so a lost response followed by tip or head drift still returns
    the same snapshot (US1 scenario 4; 025 FR-006). From Phase 5, binding (A1)
    runs before it."""
    if run.boundary != "admission":
        run.skip("convening_conflict (retry identity and once-per-pin, E2 step A3: "
                 "the consumer's live snapshots)")
        return None
    live = assignments.retry_identity(record, run.oracles.live_snapshots())
    if live is None:
        return None
    return Resolution(required_seats=list(record["required_seats"]),
                      convening_digest=convening_digest(record),
                      convening_id=live["convening_id"])


def _order(record, run: _Run, selected_protocol, statuses):
    _classify(record, run, selected_protocol, statuses)               # 1
    _shape(record, run)                                               # 2
    _bound_claims(run)                                                # A1
    returned = _retry_identity(record, run)                           # A3
    if returned is not None:
        return returned
    _secrets(record)                                                  # 3
    _candidate(record, run)                                           # 4
    projection = _governed(record, run)                               # 5
    _workflow_revision(record, run)                                   # A4
    _council_and_class(record, projection, run)                       # 6, 7
    for condition in record["required_seats_provenance"]["conditions"]:
        predicates.check_condition(condition["predicate"],            # 8
                                   condition["input_contract"], condition["parameters"],
                                   run.schemas)
    in_use, sources = _record_facts(record)                           # 9
    reference = _authoritative(record, in_use, sources, run)          # 10
    _held_and_roster(record, reference, run)                          # 11, 12
    _live_head(record, run)                                           # 13
    return Resolution(required_seats=list(record["required_seats"]),
                      convening_digest=convening_digest(record))


def resolve(record, *, boundary: str, selected_protocol, oracles: Oracles,
            expected_candidate: Mapping | None = None, statuses=None,
            schemas: records.SchemaSet | None = None,
            registry: classification.Registry | None = None,
            binding: Mapping | None = None, identity_root: Path | None = None,
            evaluation_time: str | None = None) -> Resolution:
    """E2 steps 1 to 13 at `commission` or `admission`, and at admission steps
    A1 and A4 too.

    Admission REQUIRES the commission job's `binding`, the `identity_root`
    whose `contracts/policies/repository-identity.yaml` is the identity map,
    and the `evaluation_time` the claims' window is judged at; the verified
    claims come from `oracles.identity()`. Commission takes none of them.

    Returns the roster and digest, raises `Refused` with the first failing
    check's code, raises `Routed` for a legacy record under a legacy selection,
    and raises `HarnessError` when the inputs cannot be adjudicated.
    """
    if boundary not in BOUNDARIES:
        raise HarnessError("the commission record is judged at commission or admission")
    run = _Run(boundary=boundary, oracles=oracles, expected_candidate=expected_candidate,
               schemas=schemas or _default_schemas(), registry=registry or _default_registry())
    _bind(run, binding, identity_root, evaluation_time)
    return _order(record, run, selected_protocol, statuses)


def _bind(run: _Run, bound, identity_root, evaluation_time) -> None:
    """Arm E2 steps A1 and A4 on an admission run; refuse a binding anywhere
    else. A binding-less admission fails closed, as a harness error."""
    if run.boundary != "admission":
        if bound is not None:
            raise HarnessError("a binding is judged at admission only (E2 steps A1, A4)")
        return
    if bound is None or identity_root is None or evaluation_time is None:
        raise HarnessError("admission judges the commission job's binding (E2 step A1): "
                           "it needs the binding, the identity map's root and the "
                           "evaluation time")
    run.binding, run.identity_root, run.evaluation_time = bound, Path(identity_root), \
        evaluation_time


@dataclass(frozen=True)
class OfflineResult:
    refusal: str | None
    member: str | None
    not_checkable: tuple


def check_offline(record, schemas: records.SchemaSet | None = None,
                  registry: classification.Registry | None = None) -> OfflineResult:
    """The E2 order with every oracle-dependent rule skipped and named, for
    `check`. Classification under an offline (null) selection has already routed
    a legacy record before this runs; a pass here is never evidence of
    admission."""
    run = _Run(boundary="offline", oracles=None, expected_candidate=None,
               schemas=schemas or _default_schemas(), registry=registry or _default_registry())
    try:
        _order(record, run, None, None)
    except Refused as refused:
        return OfflineResult(refused.code, refused.member, tuple(run.skipped))
    return OfflineResult(None, None, tuple(run.skipped))


#: The inputs each boundary takes at this commit. Phase 5 added the binding and
#: the operation to admission; the operation is always the commission job's.
INPUT_MEMBERS = {
    "commission": frozenset({"record", "selected_protocol", "expected_candidate"}),
    "admission": frozenset({"record", "selected_protocol", "binding", "operation"}),
}
ADMISSION_OPERATION = "commission"

#: The oracles a commission vector may carry at this commit (R8).
ORACLES_READ = ("governed_history", "governed", "governed_repositories", "rules", "facts",
                "live_heads", "head_refs", "resolved_candidate", "registry_status")
#: And an admission vector: Phase 3 adds `issued`, which A3 reads, and Phase 5
#: the verified claims and the identity map, which A1 reads.
ADMISSION_ORACLES_READ = ORACLES_READ + ("issued", "identity", "repository_identity")


def _outcome_at(vector, boundary, schemas, registry) -> records.Outcome:
    inputs = vector.get("inputs")
    environment = vector.get("environment", {})
    if not isinstance(inputs, Mapping) or "record" not in inputs or \
            "selected_protocol" not in inputs:
        raise HarnessError("a resolution vector lacks `inputs.record` or `selected_protocol`")
    if not isinstance(environment, Mapping):
        raise HarnessError("the vector's environment is not an object")
    oracles = VectorOracles(environment)
    run = _Run(boundary=boundary, oracles=oracles,
               expected_candidate=inputs.get("expected_candidate") if boundary == "commission"
               else None, schemas=schemas, registry=registry)
    # A1 and A4 belong to admission VECTORS. A shared commission vector run
    # through admission carries no binding and runs without them.
    if boundary == "admission" and vector.get("boundary") == "admission":
        with tempfile.TemporaryDirectory(prefix="council-convening-identity-") as tmp:
            _bind(run, *_admission_binding(vector, inputs, environment, Path(tmp)))
            return _run_order(inputs, environment, run)
    return _run_order(inputs, environment, run)


def _admission_binding(vector, inputs, environment, tmp: Path) -> tuple:
    """An admission vector's binding, the root its `repository_identity` oracle
    is materialized under (never the live map, R7-M1), and its instant."""
    if "binding" not in inputs or "operation" not in inputs:
        raise HarnessError("an admission vector lacks `inputs.binding` or `inputs.operation`")
    if inputs["operation"] != ADMISSION_OPERATION:
        raise HarnessError("admission judges the commission job's token: "
                           "`inputs.operation` is not `commission`")
    if "repository_identity" not in environment:
        raise HarnessError("the vector carries no `repository_identity` oracle")
    try:
        root = binding.materialize_identity(environment["repository_identity"],
                                            tmp / "root")
    except ValueError as error:
        raise HarnessError(str(error)) from None
    return inputs["binding"], root, vector.get("evaluation_time")


def _run_order(inputs, environment, run: _Run) -> records.Outcome:
    try:
        result = _order(inputs["record"], run, inputs["selected_protocol"],
                        environment.get("registry_status"))
    except Refused as refused:
        return records.Outcome("refuse", refused.code, status_read=run.status_read)
    except Routed as routed:
        return routed.outcome
    derived = {"required_seats": result.required_seats,
               "convening_digest": result.convening_digest}
    if result.convening_id is not None:
        derived["convening_id"] = result.convening_id
    return records.Outcome("accept", derived=derived, status_read=run.status_read)


def _adjudicate(vector: Mapping, schemas, registry) -> records.Outcome:
    boundary = vector.get("boundary")
    if boundary not in BOUNDARIES:
        raise HarnessError("not a commission or admission vector")
    inputs = vector.get("inputs")
    if isinstance(inputs, Mapping) and not set(inputs) <= INPUT_MEMBERS[boundary]:
        raise HarnessError(f"inputs carry members boundary {boundary} does not take")
    result = _outcome_at(vector, boundary, schemas, registry)
    if boundary == "commission" and list(vector.get("applies_to", [])) == BOTH_SIDES:
        consumer = _outcome_at(vector, "admission", schemas, registry)
        if (consumer.outcome, consumer.refusal, consumer.findings) != (
                result.outcome, result.refusal, result.findings):
            raise HarnessError("a shared commission vector reaches another outcome through "
                               "the consumer's admission resolution")
    return result


def adjudicate(vector: Mapping, schemas: records.SchemaSet | None = None,
               registry: classification.Registry | None = None) -> dict:
    """One commission or admission vector, already `$parts`-joined, as the
    members a vector's `expected` compares.

    A SHARED commission vector is also run as the consumer runs it, through
    admission (conformance-corpus § How each side runs a shared vector). The two
    must agree; a vector they disagree on is malformed, a `HarnessError`.
    """
    return _adjudicate(vector, schemas or _default_schemas(),
                       registry or _default_registry()).as_expected()


def corpus_handler(vector: Mapping, context) -> records.Outcome:
    """The corpus dispatch table's handler for `commission` and `admission`
    (T032). A vector this boundary cannot adjudicate is the corpus's
    `VectorInputError`, reported as `council-convening-schema`."""
    from . import corpus

    try:
        joined = {**vector, "inputs": corpus.join_parts(vector["inputs"]),
                  "environment": corpus.join_parts(vector.get("environment", {}))}
        return _adjudicate(joined, context.schemas, context.registry)
    except HarnessError as error:
        raise corpus.VectorInputError(str(error)) from None
    except classification.EffectNotLanded as error:
        raise corpus.NotAdjudicable(str(error)) from None
