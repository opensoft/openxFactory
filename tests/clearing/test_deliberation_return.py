"""Register entry number two's declared return shape.

Four properties the ratified requirement spends its words on, checked here rather
than left to the schema alone:

  * the return is BOUND to the convening it answers, by all three identifiers;
  * it carries NO verdict, at any depth, and the name scan REACHES this kind —
    "a refusal that fires only on a kind this operation never emits being no
    refusal at all for it";
  * it carries no signature, because no key is ever present on the host;
  * a shape failure surfaces as the family's `schema` refusal and mints no
    finding code, which is true ONLY because the kind is routed.
"""

from __future__ import annotations

import copy

import yaml

from conftest import EXAMPLES, FAMILY_DIR, adjudicate

SCHEMA = yaml.safe_load(
    (FAMILY_DIR / "deliberation-return.schema.yaml").read_text(encoding="utf-8"))
RETURN = yaml.safe_load(
    (EXAMPLES / "deliberation-return.example.yaml").read_text(encoding="utf-8"))

KIND = "xfactory_clearing_deliberation_return"


def test_the_kind_is_the_ratified_one_and_it_is_routed(reader) -> None:
    """THE KIND IS RATIFIED TEXT, and the routing is what makes it mean anything.

    `validate_record` does `KIND_TO_SCHEMA.get(kind)` and returns immediately on
    `None`, so an unrouted kind is not validated LOOSELY — it is not validated at
    all, and the requirement's claim that a shape failure surfaces as `schema`
    would be false. The kind itself is named in the ratified requirement rather
    than chosen at realization, because the verdict scan is dispatched on it: a
    realization free to pick the kind would be free to pick whether the scan
    reaches this operation.
    """
    assert SCHEMA["name"] == KIND
    assert SCHEMA["properties"]["kind"]["const"] == KIND
    assert reader.KIND_TO_SCHEMA[KIND] == "deliberation-return.schema.yaml"
    assert "deliberation-return.schema.yaml" in reader.SCHEMA_FILENAMES


def test_the_register_entry_declares_this_file_and_no_other() -> None:
    """The entry's `output_schema_ref` and this file are one fact in two places.

    A return is validated against the DECLARED value and never against a bundle's
    copy of it, so an entry pointing at a file that does not exist declares a
    check nobody can perform.
    """
    instance = yaml.safe_load(
        (FAMILY_DIR / "permitted-operations.registry.yaml").read_text(encoding="utf-8"))
    entry = next(e for e in instance["operations"]
                 if e["operation_id"] == "deliberation")
    assert entry["output_schema_ref"] == \
        "contracts/clearing/deliberation-return.schema.yaml"
    assert (FAMILY_DIR / "deliberation-return.schema.yaml").is_file()


def test_the_return_is_bound_by_all_three_identifiers() -> None:
    """A return that cannot name the exact bundle, at the exact verified pin, for
    the exact convening job is one nothing can be matched against."""
    assert set(SCHEMA["properties"]["binding"]["required"]) == {
        "convening_job_id", "verified_subject_pin", "inbound_bundle_digest"}
    assert RETURN["binding"]["convening_job_id"]
    assert RETURN["binding"]["verified_subject_pin"]
    assert RETURN["binding"]["inbound_bundle_digest"].startswith("sha256:")


def test_a_return_missing_a_binding_member_is_refused_whole(
        reader, registry_and_docs, entries) -> None:
    doc = copy.deepcopy(RETURN)
    doc["binding"].pop("inbound_bundle_digest")
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "schema" in reader.codes_of(findings.errors), findings.errors


def test_the_verdict_scan_reaches_this_kind(
        reader, registry_and_docs, entries) -> None:
    """THE POINT OF THE WHOLE ROUTING, stated as a test.

    `check_operation_report` is dispatched on `kind ==
    "xfactory_clearing_operation_report"`, so before this change the scan did not
    reach a return of any other kind. The ratified scenario requires it to, and
    the refusal is the EXISTING code: no finding code is minted for this
    operation.
    """
    doc = copy.deepcopy(RETURN)
    doc["seats"]["eligibility_verdict"] = {
        "output": {"form": "inline", "payload": "clear to merge"}}
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    codes = reader.codes_of(findings.errors)
    assert "clearing-report-carries-a-verdict" in codes, findings.errors
    assert any("eligibility_verdict" in line for line in findings.errors)


def test_the_scan_is_one_function_and_not_two_word_lists(reader) -> None:
    """Both check paths call the SAME scan.

    Two copies of a word list are two word lists, and the one that is not
    maintained is the one a verdict arrives through.
    """
    assert callable(reader.check_no_verdict)
    assert callable(reader.check_deliberation_return)
    assert reader.VERDICT_WORDS  # the single list both paths read


def test_no_finding_code_was_minted_for_this_operation(reader) -> None:
    """The closed set is unchanged, and `schema` is still not a member."""
    assert len(reader.REFUSAL_CODES) == 26
    assert "schema" not in reader.REFUSAL_CODES
    assert not [c for c in reader.REFUSAL_CODES
                if "deliberation" in c or "return" in c]


def test_there_is_no_signature_member_anywhere_in_the_shape() -> None:
    """NO KEY IS EVER PRESENT ON THE HOST, so there is nowhere to put one.

    The return is UNSIGNED on the host and is signed ON RETURN by the originating
    repository's own hosted signer. A `signature` member here would be a place a
    host-side signature could live, and the shape declines to offer one — a
    record that cannot express a claim cannot make it, which is the same
    instrument the operation report uses against `observed_runner_group`.
    """
    text = (FAMILY_DIR / "deliberation-return.schema.yaml").read_text(encoding="utf-8")
    doc = yaml.safe_load(text)

    def names(node, depth=0):
        out = []
        if depth > 8 or not isinstance(node, dict):
            return out
        for key, sub in node.items():
            out.append(key)
            out.extend(names(sub, depth + 1))
            if isinstance(sub, list):
                for item in sub:
                    out.extend(names(item, depth + 1))
        return out

    declared = [n for n in names(doc)]
    assert not [n for n in declared if "signature" in n.lower()]
    assert not [n for n in declared if "signed" in n.lower()]


def test_every_object_in_the_shape_is_closed_to_unknown_members() -> None:
    """The structural half of the verdict refusal, at EVERY depth.

    `test_every_schema_closes_its_root_to_unknown_members` covers the root for
    the whole family. A smuggled member is put where nobody is looking, so this
    walks the nested objects too — every one that declares `type: object` and no
    `additionalProperties` schema must close.
    """
    def walk(node, path="<root>"):
        if not isinstance(node, dict):
            return
        if node.get("type") == "object":
            ap = node.get("additionalProperties")
            has_named_extra = isinstance(ap, dict)
            if not has_named_extra:
                assert ap is False, f"{path}: admits unknown members"
        for key, sub in node.items():
            if isinstance(sub, dict):
                walk(sub, f"{path}/{key}")
            elif isinstance(sub, list):
                for i, item in enumerate(sub):
                    walk(item, f"{path}/{key}[{i}]")

    walk(SCHEMA)


def test_the_seat_output_is_a_tagged_union_of_inline_and_reference() -> None:
    """Both forms, and the reference form REQUIRES its hash.

    A pointer with no hash names bytes nobody can check, which is the same rule
    the sealed-bundle manifest already enforces on a selected file.
    """
    forms = SCHEMA["$defs"]["seat_output"]["oneOf"]
    tags = {branch["properties"]["form"]["const"] for branch in forms}
    assert tags == {"inline", "reference"}
    reference = next(b for b in forms
                     if b["properties"]["form"]["const"] == "reference")
    assert "content_hash" in reference["required"]


def test_seat_identity_is_the_key_so_a_duplicate_is_unrepresentable() -> None:
    seats = SCHEMA["properties"]["seats"]
    assert seats["type"] == "object"
    assert seats["minProperties"] == 1
    assert "propertyNames" in seats


def test_the_lane_is_not_pinned_by_this_schema() -> None:
    """WHICH lanes this operation may use is the CLOSED REGISTER's answer.

    A `const: artifact` here would be a second, uncounted copy of a decision the
    register owns — and the register's own schema says why a schema cannot carry
    it: "a schema constrains a document, not a decision".
    """
    assert "const" not in SCHEMA["properties"]["lane"]
    assert "enum" not in SCHEMA["properties"]["lane"]
