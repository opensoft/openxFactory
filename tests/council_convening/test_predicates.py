"""T024: the closed predicate registry and its two input contracts (data-model E3).

The identifiers are the ones the governed rule files declare, with no mapping
layer: Brett Heap's OPEN-5 ruling of 2026-10-08, "Keep the existing names
(Recommended)". The semantics are research R5's, written here from that text
and from nothing else (R4: no code is copied from codexFactory).

What this module pins, beside the data-model text:

* `changed_paths_intersect` reads `changed_paths`, `changed_files_total` and
  `changed_paths_entry_count` from `pr_facts`; `rule_touches_security_posture`
  reads `rule_touched_paths` from `rule_facts`. Each holds when any read path
  matches any pattern.
* A pattern is an exact `relative_path`, or `<relative_path>/**`. An exact
  pattern matches the one equal path; a tree pattern matches every path strictly
  inside its directory, and not a file at the directory's own path.
* Unevaluable is never false: an absent read fact, an entry count that differs
  from the declared total, or a declared total above 3000 is
  `condition_unevaluable`, whatever `held` the record claims. So is a path list
  the entry count cannot account for: fewer paths than entries, or more than
  two per entry (a rename's two), dated amendment of 2026-10-09 (pre-review L5).
* The bare-directory evidence rule is part of evaluation, after evaluability:
  an exact pattern with an observed path inside `pattern/` was a directory
  declared as a file, `predicate_parameters_malformed`.
"""

from __future__ import annotations

import copy

import pytest
import yaml

from scripts.council_convening import predicates, records

from .conftest import FAMILY

REGISTRY = FAMILY / "predicate.registry.yaml"
REGISTRY_SCHEMA = FAMILY / "predicate-registry.schema.yaml"
CONVENING_SCHEMA = FAMILY / "council-convening.schema.yaml"

CPI = "changed_paths_intersect"
RTSP = "rule_touches_security_posture"


def _refusal(function, *args):
    """The refusal code `function(*args)` raises, or None when it returns."""
    try:
        function(*args)
    except records.Refused as refused:
        return refused.code
    return None


def pr(paths, count=None, total=None):
    n = len(paths) if count is None else count
    return {"changed_paths": list(paths),
            "changed_files_total": n if total is None else total,
            "changed_paths_entry_count": n}


def rule(paths):
    return {"rule_touched_paths": list(paths)}


def cpi(*patterns):
    return {"protected_paths": list(patterns)}


def rtsp(*patterns):
    return {"security_surfaces": list(patterns)}


# --------------------------------------------------------------------------
# The registry instance and its schema.
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def registry_doc():
    return yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def schemas():
    return records.load_schemas()


def _closure_codes(schemas, document):
    return [code for code, _ in predicates.registry_findings(schemas, document)]


def test_the_registry_instance_is_closed_at_two_predicates_and_two_contracts(
        registry_doc, schemas):
    assert registry_doc["schema_version"] == 1
    assert registry_doc["kind"] == "xfactory_council_predicate_registry"
    assert [p["predicate"] for p in registry_doc["predicates"]] == [CPI, RTSP]
    assert [c["input_contract"] for c in registry_doc["input_contracts"]] == [
        "pr_facts", "rule_facts"]
    assert predicates.registry_findings(schemas, registry_doc) == []
    assert predicates.load_registry_doc() == registry_doc


def test_the_registry_keeps_the_identifiers_the_governed_rules_declare(registry_doc):
    """OPEN-5: no mapping layer, so the declared names are the registry's."""
    by_name = {p["predicate"]: p for p in registry_doc["predicates"]}
    assert by_name[CPI]["input_contract"] == "pr_facts"
    assert by_name[CPI]["parameter"] == "protected_paths"
    assert by_name[RTSP]["input_contract"] == "rule_facts"
    assert by_name[RTSP]["parameter"] == "security_surfaces"


def test_the_registry_instance_matches_the_module(registry_doc):
    for entry in registry_doc["predicates"]:
        spec = predicates.PREDICATES[entry["predicate"]]
        assert spec.input_contract == entry["input_contract"]
        assert spec.parameter == entry["parameter"]
        assert list(spec.reads) == entry["reads"]
        assert spec.path_fact == entry["matches"]
        assert (entry["patterns"]["min_items"], entry["patterns"]["max_items"]) == (1, 256)
    for entry in registry_doc["input_contracts"]:
        assert [f["fact"] for f in entry["facts"]] == list(
            predicates.INPUT_CONTRACTS[entry["input_contract"]])


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda d: d["predicates"].append(
        dict(d["predicates"][0], predicate="paths_touch_any")), id="gained-predicate"),
    pytest.param(lambda d: d["predicates"].pop(), id="lost-predicate"),
    pytest.param(lambda d: d["predicates"][1].update(
        predicate="rule_touches_posture"), id="renamed-predicate"),
    pytest.param(lambda d: d["predicates"][0].update(input_contract="rule_facts"),
                 id="rebound-contract"),
    pytest.param(lambda d: d["predicates"][0]["patterns"].update(max_items=512),
                 id="widened-bound"),
    pytest.param(lambda d: d["input_contracts"][1]["facts"].append(
        {"fact": "rule_owner", "value": "path_list", "max_items": 1}), id="gained-fact"),
    pytest.param(lambda d: d["input_contracts"].pop(), id="lost-contract"),
])
def test_a_registry_that_gained_lost_or_renamed_an_entry_is_refused(
        registry_doc, schemas, mutate):
    mutated = copy.deepcopy(registry_doc)
    mutate(mutated)
    assert "council-convening-registry-closure" in _closure_codes(schemas, mutated)


def test_prose_may_change_without_breaking_closure(registry_doc, schemas):
    mutated = copy.deepcopy(registry_doc)
    mutated["predicates"][0]["description"] = "Reworded, with the same meaning."
    assert predicates.registry_findings(schemas, mutated) == []


def test_the_registry_conforms_to_its_schema(registry_doc, schemas):
    assert schemas.errors(predicates.REGISTRY_SCHEMA_ID, registry_doc) == []


def test_a_registry_that_breaks_its_schema_is_a_schema_finding(registry_doc, schemas):
    mutated = copy.deepcopy(registry_doc)
    mutated["unexpected_member"] = 1
    assert "council-convening-schema" in _closure_codes(schemas, mutated)


def test_the_registry_schema_carries_the_house_header():
    doc = yaml.safe_load(REGISTRY_SCHEMA.read_text(encoding="utf-8"))
    assert doc["schema_version"] == 1
    assert doc["kind"] == "openxfactory-council-convening-contract-schema"
    assert doc["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert doc["$id"] == ("https://xforge.us/schemas/openxfactory/council-convening/v1/"
                          "predicate-registry.schema.yaml")
    assert doc["contract_schema_version"] == 1


def test_the_commission_schema_consumed_facts_are_the_input_contracts():
    """The commission record closes `consumed_facts` per input contract, so its
    schema must name exactly the registry's contracts and facts."""
    doc = yaml.safe_load(CONVENING_SCHEMA.read_text(encoding="utf-8"))
    consumed = doc["$defs"]["consumed_facts"]
    assert consumed["additionalProperties"] is False
    assert sorted(consumed["properties"]) == sorted(predicates.INPUT_CONTRACTS)
    for contract, facts in predicates.INPUT_CONTRACTS.items():
        member = consumed["properties"][contract]
        assert member["additionalProperties"] is False
        assert list(member["properties"]) == list(facts)
        assert "required" not in member, "an absent fact is opaque_conclusion, not shape"


# --------------------------------------------------------------------------
# The two predicates, holding and not holding (OPEN-5 identifiers).
# --------------------------------------------------------------------------

def test_changed_paths_intersect_holds_on_a_tree_pattern():
    assert predicates.evaluate(CPI, cpi("src/auth/**"), pr(["README.md", "src/auth/login.py"]))


def test_changed_paths_intersect_holds_on_an_exact_pattern():
    assert predicates.evaluate(CPI, cpi("deploy/config.yaml"), pr(["deploy/config.yaml"]))


def test_changed_paths_intersect_does_not_hold():
    assert predicates.evaluate(CPI, cpi("src/auth/**", "deploy/config.yaml"),
                               pr(["README.md", "src/app/main.py"])) is False


def test_rule_touches_security_posture_holds():
    assert predicates.evaluate(RTSP, rtsp("policy/authority/**"),
                               rule(["policy/authority/approvers.yaml"]))


def test_rule_touches_security_posture_does_not_hold():
    assert predicates.evaluate(RTSP, rtsp("policy/authority/**"),
                               rule(["policy/readme.md"])) is False


def test_an_empty_path_set_does_not_hold():
    assert predicates.evaluate(CPI, cpi("src/**"), pr([])) is False
    assert predicates.evaluate(RTSP, rtsp("src/**"), rule([])) is False


@pytest.mark.parametrize("path, held", [
    ("src/auth/login.py", True),
    ("src/auth/deep/er/x.py", True),
    ("src/auth", False),                  # a file at the tree's own path
    ("src/authority/x.py", False),        # a sibling sharing a prefix
    ("lib/src/auth/x.py", False),         # anchored at the start
])
def test_a_tree_pattern_matches_strictly_inside_its_directory(path, held):
    assert predicates.matches("src/auth/**", path) is held


@pytest.mark.parametrize("path, held", [
    ("deploy/config.yaml", True),
    ("deploy/config.yaml.bak", False),
    ("x/deploy/config.yaml", False),
])
def test_an_exact_pattern_matches_only_the_equal_path(path, held):
    assert predicates.matches("deploy/config.yaml", path) is held


def test_both_rename_paths_count():
    """One rename is one entry contributing two paths; either path can hold."""
    old = pr(["src/auth/old.py", "src/core/new.py"], count=1)
    new = pr(["lib/legacy.py", "src/auth/new.py"], count=1)
    assert predicates.evaluate(CPI, cpi("src/auth/**"), old)
    assert predicates.evaluate(CPI, cpi("src/auth/**"), new)


# --------------------------------------------------------------------------
# The pattern grammar: every refusal is predicate_parameters_malformed.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("pattern", [
    "/src/auth/**",          # rooted
    "./src/auth/**",         # dot-relative
    "src/./auth/**",         # a `.` segment
    "src/../auth/**",        # a `..` segment
    "src/auth/",             # trailing slash
    "src//auth/**",          # empty segment
    "src/*/auth.py",         # `*` outside the trailing `/**`
    "src/auth*",
    "src/aut?/**",           # `?`
    "src/[ab]uth/**",        # `[`
    "src/**/auth.py",        # `**` not trailing
    "**",                    # no directory before `/**`
    "/**",
    "src/***",
    "",                      # empty
    "src/\x01/auth.py",      # a C0 control
    "src/\x7f",              # DEL
    "src/" + "a" * 4093,     # 4097 bytes
])
def test_every_pattern_grammar_refusal(pattern):
    assert _refusal(predicates.check_condition, CPI, "pr_facts",
                    cpi(pattern)) == "predicate_parameters_malformed"


@pytest.mark.parametrize("pattern", [
    "src/auth/**",
    "deploy/config.yaml",
    "README.md",
    ".github/workflows/**",   # a dot-prefixed name is not a dot segment
    "src\\auth/**",           # `\` is legal in a relative_path
    "src/\u0085/x",           # so is a C1 character
    "a" * 4096,               # exactly 4096 bytes
])
def test_patterns_the_grammar_accepts(pattern):
    assert _refusal(predicates.check_condition, CPI, "pr_facts", cpi(pattern)) is None


@pytest.mark.parametrize("parameters", [
    {},
    {"protected_paths": []},
    {"protected_paths": ["src/**"] * 257},
    {"protected_paths": "src/**"},
    {"protected_paths": [1]},
    {"protected_paths": ["src/**"], "mode": "any"},
    {"security_surfaces": ["src/**"]},          # the other predicate's parameter
    [],
    None,
])
def test_parameters_are_closed_per_predicate(parameters):
    assert _refusal(predicates.check_condition, CPI, "pr_facts",
                    parameters) == "predicate_parameters_malformed"


def test_two_hundred_fifty_six_patterns_are_accepted():
    assert _refusal(predicates.check_condition, CPI, "pr_facts",
                    {"protected_paths": [f"src/p{i}/**" for i in range(256)]}) is None


# --------------------------------------------------------------------------
# The bare-directory evidence rule.
# --------------------------------------------------------------------------

def test_an_exact_pattern_with_an_observed_path_inside_it_is_malformed():
    assert _refusal(predicates.evaluate, CPI, cpi("src/auth"),
                    pr(["src/auth/login.py"])) == "predicate_parameters_malformed"


def test_the_evidence_rule_reads_every_read_path_including_rename_halves():
    facts = pr(["lib/old.py", "src/auth/new.py"], count=1)
    assert _refusal(predicates.evaluate, CPI, cpi("src/auth"),
                    facts) == "predicate_parameters_malformed"


def test_the_evidence_rule_applies_to_rule_facts_too():
    assert _refusal(predicates.evaluate, RTSP, rtsp("policy/authority"),
                    rule(["policy/authority/x.yaml"])) == "predicate_parameters_malformed"


def test_an_exact_pattern_without_such_evidence_is_evaluated():
    assert predicates.evaluate(CPI, cpi("src/auth"), pr(["src/auth"])) is True
    assert predicates.evaluate(CPI, cpi("src/auth"), pr(["src/authx/y.py"])) is False


def test_a_tree_pattern_is_never_bare_directory_evidence():
    assert predicates.evaluate(CPI, cpi("src/auth/**"), pr(["src/auth/x/y.py"])) is True


# --------------------------------------------------------------------------
# Completeness and unevaluable-is-never-false.
# --------------------------------------------------------------------------

def test_an_entry_count_that_differs_from_the_total_is_unevaluable():
    assert _refusal(predicates.evaluate, CPI, cpi("src/**"),
                    pr(["src/a.py"], count=1, total=2)) == "condition_unevaluable"


def test_one_rename_is_one_entry_and_two_paths():
    """Two paths, one entry, total one: complete."""
    assert predicates.evaluate(CPI, cpi("zz/**"),
                               pr(["a.py", "b.py"], count=1, total=1)) is False


def test_a_declared_total_above_3000_is_unevaluable():
    assert _refusal(predicates.evaluate, CPI, cpi("src/**"),
                    pr(["src/a.py"], count=3001, total=3001)) == "condition_unevaluable"


def test_a_declared_total_of_exactly_3000_is_evaluable():
    paths = [f"src/f{i:04d}.py" for i in range(3000)]
    assert predicates.evaluate(CPI, cpi("zz/**"),
                               pr(paths, count=3000, total=3000)) is False


# Pre-review L5 (2026-10-09): completeness ties the path list to the entry count.
# Each entry contributes one path, or two for a rename, so a complete listing of
# n entries carries from n to 2n paths. Without the tie, a total and an entry
# count of 2 over an empty list evaluated to "not held" and dropped a seat.

@pytest.mark.parametrize("facts", [
    pr([], count=2),
    pr(["src/a.py"], count=2),
    pr(["a.py", "b.py", "c.py"], count=1),
    pr(["a.py", "b.py", "c.py", "d.py", "e.py"], count=2),
])
def test_a_path_list_the_entry_count_cannot_account_for_is_unevaluable(facts):
    assert _refusal(predicates.evaluate, CPI, cpi("zz/**"), facts) == "condition_unevaluable"


@pytest.mark.parametrize("facts", [
    pr([], count=0),
    pr(["a.py"], count=1),
    pr(["a.py", "b.py"], count=1),
    pr(["a.py", "b.py", "c.py"], count=2),
    pr(["a.py", "b.py", "c.py", "d.py"], count=2),
])
def test_one_or_two_paths_per_entry_is_complete(facts):
    assert predicates.evaluate(CPI, cpi("zz/**"), facts) is False


def test_the_path_tie_is_unevaluable_before_the_bare_directory_evidence():
    facts = pr(["src/auth/login.py"], count=2)
    assert _refusal(predicates.evaluate, CPI, cpi("src/auth"), facts) == "condition_unevaluable"


@pytest.mark.parametrize("fact", ["changed_paths", "changed_files_total",
                                  "changed_paths_entry_count"])
def test_an_absent_pr_fact_is_unevaluable(fact):
    facts = pr(["README.md"])
    del facts[fact]
    assert _refusal(predicates.evaluate, CPI, cpi("src/**"), facts) == "condition_unevaluable"


def test_an_absent_rule_fact_is_unevaluable():
    assert _refusal(predicates.evaluate, RTSP, rtsp("src/**"), {}) == "condition_unevaluable"


@pytest.mark.parametrize("facts", [
    {"changed_paths": "README.md", "changed_files_total": 1, "changed_paths_entry_count": 1},
    {"changed_paths": [1], "changed_files_total": 1, "changed_paths_entry_count": 1},
    {"changed_paths": ["a"], "changed_files_total": True, "changed_paths_entry_count": 1},
    {"changed_paths": ["a"], "changed_files_total": -1, "changed_paths_entry_count": -1},
    {"changed_paths": ["a"] * 6001, "changed_files_total": 1, "changed_paths_entry_count": 1},
    None,
])
def test_authoritative_facts_outside_the_input_contract_are_unevaluable(facts):
    assert _refusal(predicates.evaluate, CPI, cpi("src/**"), facts) == "condition_unevaluable"


def test_unevaluable_is_checked_before_the_bare_directory_evidence():
    facts = pr(["src/auth/login.py"], count=1, total=2)
    assert _refusal(predicates.evaluate, CPI, cpi("src/auth"), facts) == "condition_unevaluable"


def test_unevaluable_is_never_false():
    """The function raises; it never returns False for an incomplete fact set."""
    with pytest.raises(records.Refused) as caught:
        predicates.evaluate(CPI, cpi("zz/**"), pr([], count=0, total=1))
    assert caught.value.code == "condition_unevaluable"


def test_facts_beyond_the_read_set_are_ignored():
    facts = dict(pr(["src/a.py"]), unrelated=["x"])
    assert predicates.evaluate(CPI, cpi("src/**"), facts) is True


# --------------------------------------------------------------------------
# The wrong input contract, and an unknown predicate.
# --------------------------------------------------------------------------

def test_a_predicate_run_against_the_wrong_input_contract_is_malformed():
    assert _refusal(predicates.check_condition, CPI, "rule_facts",
                    cpi("src/**")) == "predicate_parameters_malformed"
    assert _refusal(predicates.check_condition, RTSP, "pr_facts",
                    rtsp("src/**")) == "predicate_parameters_malformed"


@pytest.mark.parametrize("contract", ["", "facts", "PR_FACTS", None, 1])
def test_an_unknown_input_contract_is_the_wrong_input_contract(contract):
    assert _refusal(predicates.check_condition, CPI, contract,
                    cpi("src/**")) == "predicate_parameters_malformed"


@pytest.mark.parametrize("predicate", ["paths_touch_any", "Changed_Paths_Intersect",
                                       "changed_paths_intersect ", "", None, 3])
def test_an_unknown_predicate(predicate):
    assert _refusal(predicates.check_condition, predicate, "pr_facts",
                    cpi("src/**")) == "predicate_unknown"


def test_an_unknown_predicate_is_named_before_its_parameters():
    assert _refusal(predicates.check_condition, "paths_touch_any", "rule_facts",
                    {"bogus": 1}) == "predicate_unknown"


def test_reads_lists_the_facts_each_predicate_reads():
    assert predicates.reads(CPI) == ("changed_paths", "changed_files_total",
                                     "changed_paths_entry_count")
    assert predicates.reads(RTSP) == ("rule_touched_paths",)


def test_a_refusal_never_echoes_a_value():
    secretish = "src/" + "Q" * 40 + "-distinctive"
    with pytest.raises(records.Refused) as caught:
        predicates.check_condition(CPI, "pr_facts", cpi("/" + secretish))
    assert secretish not in str(caught.value)
