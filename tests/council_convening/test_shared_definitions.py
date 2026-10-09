"""T005: every grammar in data-model § Shared definitions, probed one by one.

Each probe goes through the reference implementation's one entry point for a
value checked alone against a grammar, `SchemaSet.check_definition`. That is
the `definition` boundary: a value the grammar refuses is `value_malformed`,
and a value the grammar admits but `xfc-jcs-sha256-1` cannot serialize is
`value_not_canonicalizable`. The grammar runs first and the construction's
admissibility second, the order E2 step 2 and E8 step 2 give every record.

The closed enumerations are also read straight from the schema file, so a test
here does not trust the implementation to report what the contract says.
"""

from __future__ import annotations

import pytest
import yaml

from scripts.council_convening import records

from .conftest import FAMILY_REL, SHARED_DEFINITIONS

SHA = "0123456789abcdef0123456789abcdef01234567"
HEX64 = "0123456789abcdef" * 4
KEY32 = "A" * 42 + "E"           # unpadded base64url of 32 bytes, canonical tail
SIG64 = "A" * 85 + "Q"           # unpadded base64url of 64 bytes, canonical tail


@pytest.fixture(scope="module")
def schemas():
    return records.load_schemas()


@pytest.fixture(scope="module")
def definitions_doc():
    return yaml.safe_load(SHARED_DEFINITIONS.read_text(encoding="utf-8"))


def _code(schemas, name, value):
    """The refusal code for `value` under definition `name`, or None."""
    try:
        schemas.check_definition(name, value)
    except records.Refused as refused:
        return refused.code
    return None


def accepts(schemas, name, value) -> bool:
    return _code(schemas, name, value) is None


def malformed(schemas, name, value) -> bool:
    return _code(schemas, name, value) == "value_malformed"


def not_canonicalizable(schemas, name, value) -> bool:
    return _code(schemas, name, value) == "value_not_canonicalizable"


# --------------------------------------------------------------------------
# The house header and the definitions-only shape.
# --------------------------------------------------------------------------

def test_the_file_carries_the_house_header(definitions_doc):
    assert definitions_doc["schema_version"] == 1
    assert definitions_doc["kind"] == "openxfactory-council-convening-contract-schema"
    assert definitions_doc["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert definitions_doc["$id"] == (
        "https://xforge.us/schemas/openxfactory/council-convening/v1/"
        "shared-definitions.schema.yaml")
    assert definitions_doc["contract_schema_version"] == 1
    for member in ("name", "contract_id", "title", "description"):
        assert isinstance(definitions_doc[member], str) and definitions_doc[member]


def test_every_data_model_definition_is_declared(definitions_doc, schemas):
    expected = {
        "opaque_id", "council_id", "seat_id", "matched_class", "protocol_id",
        "repository", "full_sha", "pull_number", "relative_path", "head_ref",
        "utc_instant", "raw_sha256", "digest", "key_fingerprint", "public_key",
        "nonce", "signature", "decimal_string", "principal_kind", "candidate",
        "refusal_code", "finding_code",
    }
    assert expected <= set(definitions_doc["$defs"])
    assert expected <= set(schemas.definition_names)


def test_digest_is_taken_by_reference_to_the_one_construction(definitions_doc):
    digest = definitions_doc["$defs"]["digest"]
    assert digest["$ref"] == (
        "https://xforge.us/schemas/openxfactory/signed-execution-chain/v1/"
        "digest-construction.schema.yaml#/$defs/digest")
    # Nothing beside the reference restates the shape: an annotation only.
    assert set(digest) <= {"$ref", "description"}


def test_an_unknown_definition_name_is_a_harness_error_not_a_refusal(schemas):
    with pytest.raises(KeyError):
        schemas.check_definition("no_such_definition", "x")


# --------------------------------------------------------------------------
# Whole-string matching: a trailing newline is refused everywhere.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("name, value", [
    ("opaque_id", "seat-alpha"),
    ("council_id", "merge-readiness"),
    ("seat_id", "security"),
    ("matched_class", "standard"),
    ("repository", "opensoft/openxFactory"),
    ("full_sha", SHA),
    ("raw_sha256", "sha256:" + HEX64),
    ("key_fingerprint", "sha256:" + HEX64),
    ("decimal_string", "12.5"),
    ("utc_instant", "2026-10-09T00:00:00Z"),
    ("public_key", KEY32),
    ("signature", SIG64),
])
def test_whole_string_matching_refuses_a_trailing_newline(schemas, name, value):
    assert accepts(schemas, name, value)
    assert malformed(schemas, name, value + "\n"), (
        f"{name} accepted a trailing newline: Python's `$` matches before one, "
        f"so the reference must match the WHOLE string")


# --------------------------------------------------------------------------
# Identifiers.
# --------------------------------------------------------------------------

def test_opaque_id_grammar(schemas):
    assert accepts(schemas, "opaque_id", "seat.alpha:1/x@y+z=w-v_")
    assert accepts(schemas, "opaque_id", "a" + "b" * 255)
    assert malformed(schemas, "opaque_id", "a" + "b" * 256)
    assert malformed(schemas, "opaque_id", "")
    assert malformed(schemas, "opaque_id", "-seat")
    assert malformed(schemas, "opaque_id", "seat alpha")
    assert malformed(schemas, "opaque_id", 7)


def test_protocol_id_grammar_is_length_and_controls_only(schemas):
    # Membership in the registry is classification (E1), not a grammar.
    assert accepts(schemas, "protocol_id", "xfc-resolved-council-1")
    assert accepts(schemas, "protocol_id", "not-a-registry-member")
    assert accepts(schemas, "protocol_id", "x" * 128)
    assert malformed(schemas, "protocol_id", "x" * 129)
    assert malformed(schemas, "protocol_id", "")
    assert malformed(schemas, "protocol_id", "xfc\u0007")
    assert malformed(schemas, "protocol_id", "xfc\u007f")
    assert malformed(schemas, "protocol_id", "xfc\u0085")   # C1 is a control too
    assert not_canonicalizable(schemas, "protocol_id", "xfc-\ud800")


def test_repository_grammar(schemas):
    assert accepts(schemas, "repository", "opensoft/openxFactory")
    assert accepts(schemas, "repository", "code-X_factory.2/codex.Factory")
    assert malformed(schemas, "repository", "opensoft")
    assert malformed(schemas, "repository", "opensoft/openxFactory/extra")
    assert malformed(schemas, "repository", "/openxFactory")


def test_full_sha_refuses_abbreviated_uppercase_and_branch(schemas):
    assert accepts(schemas, "full_sha", SHA)
    assert malformed(schemas, "full_sha", SHA[:7])
    assert malformed(schemas, "full_sha", SHA.upper())
    assert malformed(schemas, "full_sha", "main")
    assert malformed(schemas, "full_sha", SHA + "0")


def test_pull_number_bounds_and_no_boolean(schemas):
    assert accepts(schemas, "pull_number", 1)
    assert accepts(schemas, "pull_number", 2147483647)
    assert malformed(schemas, "pull_number", 0)
    assert malformed(schemas, "pull_number", -1)
    assert malformed(schemas, "pull_number", 2147483648)
    assert malformed(schemas, "pull_number", True)
    assert malformed(schemas, "pull_number", "12")
    assert malformed(schemas, "pull_number", 1.5)


# --------------------------------------------------------------------------
# relative_path: 049's rules exactly, plus the one 4096-byte tightening.
# --------------------------------------------------------------------------

def test_relative_path_accepts_backslash_and_c1(schemas):
    assert accepts(schemas, "relative_path", "contracts/council-convening/README.md")
    assert accepts(schemas, "relative_path", "dir\\file.txt")
    assert accepts(schemas, "relative_path", "dir/\u0085file")
    assert accepts(schemas, "relative_path", "..a/b.")        # not a dot segment
    assert accepts(schemas, "relative_path", ".github/workflows/x.yml")


@pytest.mark.parametrize("value", [
    "",
    "/rooted",
    "a//b",
    "a/",
    "./a",
    "a/./b",
    "a/../b",
    "..",
    "a/.",
    "a\u0001b",
    "a\u001fb",
    "a\u007fb",
    "a/b\n",
])
def test_every_relative_path_refusal(schemas, value):
    assert malformed(schemas, "relative_path", value)


def test_relative_path_is_bounded_in_utf8_bytes_not_characters(schemas):
    exactly = "a" * 4094 + "é"             # 4095 characters, 4096 bytes
    over_by_bytes = "a" * 4095 + "é"       # 4096 characters, 4097 bytes
    assert len(exactly.encode("utf-8")) == 4096
    assert len(over_by_bytes) == 4096 and len(over_by_bytes.encode("utf-8")) == 4097
    assert accepts(schemas, "relative_path", exactly)
    assert malformed(schemas, "relative_path", over_by_bytes)
    assert malformed(schemas, "relative_path", "a" * 4097)


def test_a_lone_surrogate_path_is_not_canonicalizable(schemas):
    assert not_canonicalizable(schemas, "relative_path", "dir/\ud800")


# --------------------------------------------------------------------------
# head_ref and decimal_string.
# --------------------------------------------------------------------------

def test_head_ref_grammar(schemas):
    assert accepts(schemas, "head_ref", "feature/x")
    assert accepts(schemas, "head_ref", "x" * 255)
    assert accepts(schemas, "head_ref", "branch\u0085")       # C1 is allowed here
    assert malformed(schemas, "head_ref", "x" * 256)
    assert malformed(schemas, "head_ref", "")
    assert malformed(schemas, "head_ref", "a\tb")
    assert malformed(schemas, "head_ref", "a\u007fb")
    assert not_canonicalizable(schemas, "head_ref", "b\udfff")


@pytest.mark.parametrize("value", ["0", "3", "-3", "12.5", "-0.25", "0.001",
                                   "9007199254740993.5"])
def test_decimal_string_accepts(schemas, value):
    assert accepts(schemas, "decimal_string", value)


@pytest.mark.parametrize("value", ["-0", "1e5", "1E5", "1.50", "0.0", "+1", "01",
                                   ".5", "1.", "-", "", "1.2.3", " 1"])
def test_decimal_string_refusals(schemas, value):
    assert malformed(schemas, "decimal_string", value)


def test_decimal_string_refuses_a_number(schemas):
    assert malformed(schemas, "decimal_string", 12)


# --------------------------------------------------------------------------
# utc_instant: the exact form, and the calendar.
# --------------------------------------------------------------------------

def test_utc_instant_calendar_validity(schemas):
    assert accepts(schemas, "utc_instant", "2026-10-09T23:59:59Z")
    assert accepts(schemas, "utc_instant", "2024-02-29T12:00:00Z")   # leap year
    assert malformed(schemas, "utc_instant", "2026-02-29T12:00:00Z")
    assert malformed(schemas, "utc_instant", "2026-04-31T00:00:00Z")
    assert malformed(schemas, "utc_instant", "2026-13-01T00:00:00Z")
    assert malformed(schemas, "utc_instant", "2026-10-09T24:00:00Z")
    assert malformed(schemas, "utc_instant", "2026-10-09T23:59:60Z")


@pytest.mark.parametrize("value", [
    "2026-10-09T00:00:00+00:00",
    "2026-10-09T00:00:00.5Z",
    "2026-10-09T00:00:00z",
    "2026-10-09 00:00:00Z",
    "2026-10-09",
])
def test_utc_instant_form(schemas, value):
    assert malformed(schemas, "utc_instant", value)


# --------------------------------------------------------------------------
# Digests, fingerprints, keys, nonces and signatures.
# --------------------------------------------------------------------------

def test_raw_sha256_and_key_fingerprint(schemas):
    for name in ("raw_sha256", "key_fingerprint"):
        assert accepts(schemas, name, "sha256:" + HEX64)
        assert malformed(schemas, name, "sha256:" + HEX64.upper())
        assert malformed(schemas, name, HEX64)
        assert malformed(schemas, name, "sha256:" + HEX64[:-1])
        assert malformed(schemas, name, "sha512:" + HEX64)


@pytest.mark.parametrize("subject", ["council_convening", "council_seat_return_payload"])
def test_digest_admits_the_two_new_subjects(schemas, subject):
    value = {"construction": "xfc-jcs-sha256-1", "subject": subject,
             "value": "sha256:" + HEX64}
    assert accepts(schemas, "digest", value)


def test_digest_refusals(schemas):
    good = {"construction": "xfc-jcs-sha256-1", "subject": "council_convening",
            "value": "sha256:" + HEX64}
    assert malformed(schemas, "digest", {**good, "subject": "council_snapshot"})
    assert malformed(schemas, "digest", {**good, "construction": "xfc-jcs-sha256-2"})
    assert malformed(schemas, "digest", {**good, "extra": 1})
    assert malformed(schemas, "digest", {k: v for k, v in good.items() if k != "value"})
    assert malformed(schemas, "digest", "sha256:" + HEX64)


def test_base64url_lengths(schemas):
    for name in ("public_key", "nonce"):
        assert accepts(schemas, name, KEY32)
        assert accepts(schemas, name, "abcdefghijklmnopqrstuvwxyz0123456789-_ABCDw")
        assert malformed(schemas, name, KEY32[:-1])            # 42 characters
        assert malformed(schemas, name, KEY32 + "A")           # 44 characters
        assert malformed(schemas, name, KEY32 + "=")           # padded
        assert malformed(schemas, name, "A" * 42 + "B")        # non-zero pad bits
        assert malformed(schemas, name, "A" * 41 + "+E")       # standard alphabet
    assert accepts(schemas, "signature", SIG64)
    assert malformed(schemas, "signature", SIG64[:-1])
    assert malformed(schemas, "signature", SIG64 + "A")
    assert malformed(schemas, "signature", SIG64 + "==")
    assert malformed(schemas, "signature", "A" * 85 + "B")
    assert malformed(schemas, "signature", KEY32)


# --------------------------------------------------------------------------
# The candidate.
# --------------------------------------------------------------------------

CANDIDATE = {"repository": "opensoft/openxFactory", "pull_number": 1268,
             "head_sha": SHA}


def test_candidate_with_and_without_subject_path(schemas):
    assert accepts(schemas, "candidate", CANDIDATE)
    assert accepts(schemas, "candidate",
                   {**CANDIDATE, "subject_path": "scripts/merge_master/rules.yaml"})


@pytest.mark.parametrize("value", [
    {k: v for k, v in CANDIDATE.items() if k != "head_sha"},
    {k: v for k, v in CANDIDATE.items() if k != "repository"},
    {k: v for k, v in CANDIDATE.items() if k != "pull_number"},
    {**CANDIDATE, "extra": True},
    {**CANDIDATE, "pull_number": 0},
    {**CANDIDATE, "head_sha": SHA.upper()},
    {**CANDIDATE, "subject_path": "/rooted"},
    {**CANDIDATE, "subject_path": ""},
    "opensoft/openxFactory#1268",
])
def test_candidate_refusals(schemas, value):
    assert malformed(schemas, "candidate", value)


def test_candidate_with_a_lone_surrogate_path_is_not_canonicalizable(schemas):
    assert not_canonicalizable(
        schemas, "candidate", {**CANDIDATE, "subject_path": "rules/\ud800.yaml"})


# --------------------------------------------------------------------------
# The closed enumerations, each holding exactly the members landed at this commit.
# --------------------------------------------------------------------------

PHASE_1_REFUSALS = ["value_malformed", "value_not_canonicalizable",
                    "protocol_unknown", "protocol_not_selected",
                    "legacy_protocol_refused"]


def test_principal_kind_is_closed(definitions_doc, schemas):
    assert definitions_doc["$defs"]["principal_kind"]["enum"] == [
        "github_oidc_job", "governed_broker_job"]
    assert accepts(schemas, "principal_kind", "github_oidc_job")
    assert accepts(schemas, "principal_kind", "governed_broker_job")
    assert malformed(schemas, "principal_kind", "github_oidc")


#: Phase 2's codes (T028), in data-model § Refusal vocabulary order.
PHASE_2_REFUSALS = [
    "convening_malformed", "council_unknown", "class_unresolved", "class_mismatch",
    "rule_projection_mismatch", "mutable_rule_reference", "rule_revision_ungoverned",
    "governed_sources_mismatch", "rule_path_malformed", "rule_unavailable",
    "rule_unauthorized", "rule_digest_mismatch", "rule_superseded", "predicate_unknown",
    "predicate_parameters_malformed", "condition_unevaluable",
    "condition_result_mismatch", "condition_seat_unbound", "opaque_conclusion",
    "facts_unused", "consumed_facts_mismatch", "fact_source_mismatch",
    "secret_bearing_fact", "candidate_mismatch", "candidate_head_moved",
    "candidate_head_unavailable", "roster_empty", "roster_duplicate_seat",
    "roster_mismatch"]


#: Phase 4's codes (T046), in data-model § Refusal vocabulary order.
PHASE_4_REFUSALS = [
    "assignment_unknown", "assignment_not_yet_valid", "assignment_expired",
    "operation_not_permitted", "challenge_malformed", "challenge_unknown",
    "challenge_wrong_assignment", "challenge_consumed", "challenge_expired",
    "registration_malformed", "root_authorization_refused", "wrong_principal",
    "fingerprint_mismatch", "assignment_already_registered", "shared_key",
    "cross_protocol_context", "cross_convening_context", "cross_seat_context",
    "proof_invalid", "return_malformed", "return_unregistered", "return_key_mismatch",
    "return_digest_mismatch", "return_signature_invalid", "return_replayed",
    "return_unlisted", "return_duplicate", "return_missing", "completion_set_mismatch",
    "binding_unresolved", "broker_capability_insufficient"]


def test_refusal_code_holds_exactly_the_landed_phases_codes(definitions_doc, schemas):
    landed = PHASE_1_REFUSALS + PHASE_2_REFUSALS + PHASE_4_REFUSALS
    assert definitions_doc["$defs"]["refusal_code"]["enum"] == landed
    assert schemas.enum("refusal_code") == landed
    for code in landed:
        assert accepts(schemas, "refusal_code", code)
    # A Phase 3 code is not a member at this commit.
    assert malformed(schemas, "refusal_code", "snapshot_malformed")


def test_finding_code_holds_exactly_the_phase_1_finding(definitions_doc, schemas):
    assert definitions_doc["$defs"]["finding_code"]["enum"] == ["legacy_protocol_routed"]
    assert schemas.enum("finding_code") == ["legacy_protocol_routed"]
    # The Phase 6 finding is not a member at this commit.
    assert malformed(schemas, "finding_code", "legacy_protocol_deprecated")


def test_a_refusal_never_echoes_the_value(schemas):
    secret_shaped = "a" + "Z" * 300
    with pytest.raises(records.Refused) as caught:
        schemas.check_definition("opaque_id", secret_shaped)
    assert secret_shaped not in str(caught.value)
    assert caught.value.member == "opaque_id"


# --------------------------------------------------------------------------
# The family keywords hold at every depth, inside a whole family document.
#
# A record schema is a whole document carrying the house `$schema` header.
# jsonschema re-selects the validator class from `$schema` whenever it descends
# into such a document (`evolve` calls `validator_for`), which used to swap the
# family validator for plain `Draft202012Validator`: whole-string `pattern` and
# `x-max-utf8-bytes` silently stopped applying, and a record validated FAIL
# OPEN. A `$ref` straight to a `$defs` member never enters a document, which is
# why the definition-boundary tests above could not see it.
# --------------------------------------------------------------------------

PROBE_RECORD = "probe-record.schema.yaml"


@pytest.fixture
def probe_schemas(family_tree):
    """The family plus one record-shaped schema with the house header, loaded
    from a temporary tree."""
    shared = records.SHARED_DEFINITIONS_ID + "#/$defs/"
    document = {
        "schema_version": 1,
        "kind": records.SCHEMA_KIND,
        "name": "xfactory_council_probe_record",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": records.ID_BASE + PROBE_RECORD,
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "convening_id": {"$ref": shared + "opaque_id"},
            "path": {"$ref": shared + "relative_path"},
        },
    }
    (family_tree / FAMILY_REL / PROBE_RECORD).write_text(
        yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return records.load_schemas(family_tree)


def _record_errors(probe_schemas, record):
    return [(error.validator, error.message)
            for error in probe_schemas.errors(records.ID_BASE + PROBE_RECORD, record)]


def test_a_record_schema_refuses_an_opaque_id_with_a_trailing_newline(probe_schemas):
    assert _record_errors(probe_schemas, {"convening_id": "convening-0001"}) == []
    assert _record_errors(probe_schemas, {"convening_id": "convening-0001\n"}) == [
        ("pattern", "does not match the pattern, matched whole")]


def test_a_record_schema_refuses_a_utf8_byte_overrun(probe_schemas):
    """2049 two-byte characters: inside `maxLength` 4096 and the pattern, so only
    `x-max-utf8-bytes` can refuse it."""
    assert _record_errors(probe_schemas, {"path": "a" * 4096}) == []
    assert _record_errors(probe_schemas, {"path": chr(0xE9) * 2049}) == [
        ("x-max-utf8-bytes", "is longer than 4096 UTF-8 bytes")]


def test_every_registered_document_keeps_the_family_validator(schemas):
    """Every family document and the digest construction resolve, as whole
    documents, to the family validator, never to the dialect's plain one."""
    from jsonschema import validators

    ids = [records.ID_BASE + name for name in schemas.family] + [
        records.DIGEST_CONSTRUCTION_ID]
    for resource_id in ids:
        contents = schemas.registry[resource_id].contents
        assert validators.validator_for(
            contents, default=records.FamilyValidator) is records.FamilyValidator, resource_id
    # The family dict keeps each document exactly as written, header included.
    assert all("$schema" in document for document in schemas.family.values())


def test_a_family_document_in_another_dialect_is_refused_at_load(family_tree):
    """The header is dropped from the registered copy only because it names the
    one dialect the family validator implements; any other dialect is refused,
    never silently re-read as 2020-12."""
    path = family_tree / FAMILY_REL / "protocol-registry.schema.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    document["$schema"] = "http://json-schema.org/draft-07/schema#"
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    with pytest.raises(records.SchemaLoadError, match="dialect"):
        records.load_schemas(family_tree)


# Both entry points, side by side: validation at a whole document's root, and a
# `$ref` into a fragment of a whole document that carries the header.

@pytest.mark.parametrize("ref, instance", [
    (records.ID_BASE + PROBE_RECORD, {"convening_id": "convening-0001\n"}),
    (records.ID_BASE + PROBE_RECORD + "#/properties/convening_id", "convening-0001\n"),
    (records.SHARED_DEFINITIONS_ID + "#/$defs/opaque_id", "convening-0001\n"),
    (records.ID_BASE + PROBE_RECORD, {"path": chr(0xE9) * 2049}),
    (records.ID_BASE + PROBE_RECORD + "#/properties/path", chr(0xE9) * 2049),
    (records.SHARED_DEFINITIONS_ID + "#/$defs/relative_path", chr(0xE9) * 2049),
])
def test_the_family_keywords_hold_at_the_root_and_through_a_fragment(
        probe_schemas, ref, instance):
    found = [error.validator for error in probe_schemas.errors(ref, instance)]
    assert found in (["pattern"], ["x-max-utf8-bytes"]), (ref, found)


def test_descending_into_a_served_document_keeps_the_family_validator(probe_schemas):
    """The path jsonschema itself takes: `evolve` onto a document the registry
    serves. `SchemaSet.family` keeps each document AS WRITTEN, header included,
    and is for reading, never for evolving a validator onto."""
    root = probe_schemas.validator(records.SHARED_DEFINITIONS_ID + "#/$defs/opaque_id")
    for resource_id in (records.ID_BASE + PROBE_RECORD,
                        records.ID_BASE + "protocol-registry.schema.yaml",
                        records.DIGEST_CONSTRUCTION_ID):
        served = probe_schemas.registry[resource_id].contents
        assert type(root.evolve(schema=served)) is records.FamilyValidator, resource_id


@pytest.mark.parametrize("target", [
    "https://json-schema.org/draft/2020-12/schema",
    "https://xforge.us/schemas/openxfactory/council-convening/v1/absent.schema.yaml",
])
def test_a_reference_outside_the_loaded_documents_is_refused_at_load(family_tree, target):
    """jsonschema resolves against the loaded documents COMBINED with the
    bundled dialect metaschemas, which keep their `$schema` header. A `$ref` to
    one would validate that member under the plain dialect validator; it cannot
    strip a family keyword, since none sits beneath a metaschema, but it is a
    reference outside the family all the same. An absent family document would
    otherwise surface only at validation time. So every `$ref` must name a
    document this load registered, and loading refuses one that does not."""
    path = family_tree / FAMILY_REL / "protocol-registry.schema.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    document["$defs"]["release_tag"] = {"$ref": target}
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    with pytest.raises(records.SchemaLoadError, match="outside the loaded documents"):
        records.load_schemas(family_tree)


def test_the_landed_family_references_only_loaded_documents(schemas):
    """Every `$ref` in the landed family names a registered document, and the
    walk does reach them: the shared definitions' digest reference is seen."""
    assert records.references_outside(schemas.family, schemas.digest_construction) == []
    assert records.DIGEST_CONSTRUCTION_ID + "#/$defs/digest" in list(
        records.reference_targets(schemas.shared))


# --------------------------------------------------------------------------
# M2: family YAML is read strictly; a repeated key is refused at load.
# --------------------------------------------------------------------------

def test_a_family_schema_with_a_repeated_key_is_refused_at_load(family_tree):
    path = family_tree / FAMILY_REL / "shared-definitions.schema.yaml"
    path.write_text(path.read_text(encoding="utf-8") + "kind: something-else\n",
                    encoding="utf-8")
    with pytest.raises(records.SchemaLoadError, match="strict YAML"):
        records.load_schemas(family_tree)


def test_a_registry_with_a_repeated_key_is_refused_at_load(family_tree):
    from scripts.council_convening import classification

    path = family_tree / FAMILY_REL / "protocol.registry.yaml"
    path.write_text(path.read_text(encoding="utf-8") + "registry_version: 2\n",
                    encoding="utf-8")
    with pytest.raises(records.SchemaLoadError, match="strict YAML"):
        classification.load_registry_doc(family_tree)


# --------------------------------------------------------------------------
# Formats: an explicit allowlist, and nothing the checker cannot assert.
# --------------------------------------------------------------------------

def test_the_format_checker_asserts_exactly_the_allowlist(schemas):
    """`FormatChecker()` asserts whatever optional libraries happen to be
    installed, so two machines could disagree; the family names its formats."""
    assert records.ASSERTED_FORMATS == ("date-time",)
    assert set(schemas.format_checker.checkers) == {"date-time"}


@pytest.mark.parametrize("fmt", ["email", "uri", "hostname", "no-such-format"])
def test_a_format_outside_the_allowlist_is_refused_at_load(family_tree, fmt):
    path = family_tree / FAMILY_REL / "shared-definitions.schema.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    document["$defs"]["probe"] = {"type": "string", "format": fmt}
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    with pytest.raises(records.SchemaLoadError, match="format"):
        records.load_schemas(family_tree)


def test_loading_fails_closed_without_the_date_time_checker(monkeypatch):
    """Without `rfc3339-validator`, jsonschema registers no `date-time`
    checker, and calendar validity would silently go unchecked."""
    from jsonschema import FormatChecker

    monkeypatch.setattr(FormatChecker, "checkers",
                        {k: v for k, v in FormatChecker.checkers.items() if k != "date-time"})
    with pytest.raises(records.SchemaLoadError, match="rfc3339-validator"):
        records.load_schemas()


def _patterns(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "pattern" and isinstance(value, str):
                yield value
            else:
                yield from _patterns(value)
    elif isinstance(node, list):
        for item in node:
            yield from _patterns(item)


def _inner_dollars(pattern: str) -> int:
    count = 0
    for at, char in enumerate(pattern[:-1]):
        if char == "$":
            backslashes = len(pattern[:at]) - len(pattern[:at].rstrip("\\"))
            count += backslashes % 2 == 0
    return count


def test_every_inner_dollar_in_a_family_pattern_is_a_reviewed_one(schemas):
    """`whole_match` rewrites only a pattern's FINAL `$` (its known limit, L7).
    Two patterns carry an inner `$`, each inside a NEGATIVE lookahead:
    `relative_path`'s, refusing a `.` or `..` segment, and `decimal_string`'s,
    refusing `-0`. Both are safe. Each pattern's characters exclude U+000A, and
    Python's `$` only ADDS a match position (before a final newline), which
    inside a negative lookahead can only add a refusal of a string the final
    `\\Z` refuses anyway. Any other inner `$` fails here, for review, before it
    can fail open."""
    defs = schemas.shared["$defs"]
    reviewed = {defs["relative_path"]["pattern"]: ("relative_path", ("..\n", "a/..\n", ".\n", "a/.\n", "a\n")),
                defs["decimal_string"]["pattern"]: ("decimal_string", ("-0\n", "0\n", "1.5\n", "-0"))}
    found = [p for doc in [*schemas.family.values(), schemas.digest_construction]
             for p in _patterns(doc)]
    assert found
    inner = {pattern for pattern in found if _inner_dollars(pattern)}
    assert inner == set(reviewed), inner - set(reviewed)
    for pattern, (name, refused) in reviewed.items():
        for value in refused:
            assert malformed(schemas, name, value), (name, repr(value))
    assert accepts(schemas, "decimal_string", "0")
    assert accepts(schemas, "relative_path", "a/b")
