"""`xfc-jcs-sha256-1` — the ONE construction, tested as a construction.

A digest rule that fixes the algorithm and leaves the serialization to the
implementation produces readers that agree on how to hash and disagree on what.
So what is pinned here is the SERIALIZATION: member ordering, escaping, the
admitted value classes, and the refusal of the one class RFC 8785 serializes in a
way a second implementation reliably gets wrong.

RFC 8785's own worked example is included because a construction chosen against a
published standard and then not checked against it is a construction invented
with a citation attached.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.signed_execution_chain import canonical  # noqa: E402

CONTRACT = (REPO_ROOT / "contracts" / "signed-execution-chain" /
            "digest-construction.schema.yaml")


def test_the_construction_and_its_tag_are_the_contract_s():
    """The name and the tag are read off the contract by every record; a rename
    here without a rename there is two constructions wearing one name."""
    assert f"const: {canonical.CONSTRUCTION}" in CONTRACT.read_text(encoding="utf-8")
    assert canonical.TAG == "sha256:"


def test_rfc_8785_worked_example():
    """RFC 8785 section 3.2.3's worked ordering example, VERBATIM in its member
    names, with integer values substituted for the RFC's numbers because this
    family admits no non-integer number.

    Three separate rules are pinned by this one assertion: the member ordering,
    the absence of insignificant whitespace, and the escaping boundary — U+0080
    is a C1 control and is emitted LITERALLY, because RFC 8785 escapes only the
    C0 range, and an implementation that escaped it would derive a different
    digest from the same record."""
    value = {
        "€": "Euro Sign",
        "\r": "Carriage Return",
        "דּ": "Hebrew Letter Dalet With Dagesh",
        "1": "One",
        "\u0080": "Control",
        "ö": "Latin Small Letter O With Diaeresis",
        "ǵ": "Latin Small Letter G With Cedilla",
        "\u2028": "Line Separator",
        "\U0001f600": "Emoji: Grinning Face",
        "ā": "Latin Small Letter A With Macron",
    }
    assert canonical.serialize(value) == (
        '{"\\r":"Carriage Return","1":"One","\u0080":"Control",'
        '"ö":"Latin Small Letter O With Diaeresis",'
        '"ā":"Latin Small Letter A With Macron",'
        '"ǵ":"Latin Small Letter G With Cedilla",'
        '"\u2028":"Line Separator","€":"Euro Sign",'
        '"\U0001f600":"Emoji: Grinning Face",'
        '"דּ":"Hebrew Letter Dalet With Dagesh"}'
    )


def test_member_order_is_utf16_code_units_and_not_code_points():
    """The two orders DISAGREE above the BMP: a surrogate pair's leading unit
    (U+D800..U+DBFF) sorts BELOW U+E000..U+FFFF, so U+1F600 comes FIRST under
    RFC 8785 and LAST under code-point order.

    Sorting the Python string directly gives the other answer, and the difference
    is invisible on every member name this family happens to use today — which is
    what makes it worth pinning now rather than on the day a name changes."""
    value = {"\U0001f600": 1, "ﬀ": 2}
    assert list(json.loads(canonical.serialize(value))) == ["\U0001f600", "ﬀ"]
    assert sorted(value) == ["ﬀ", "\U0001f600"], \
        "code-point order is the OTHER order, which is the whole point"


def test_the_serialization_carries_no_insignificant_whitespace():
    assert canonical.serialize({"a": [1, 2], "b": {"c": True}}) == \
        '{"a":[1,2],"b":{"c":true}}'


def test_escaping_uses_the_shortest_legal_form():
    assert canonical.serialize("\b\t\n\f\r\"\\") == r'"\b\t\n\f\r\"\\"'
    assert canonical.serialize("\u0000\u001f") == '"\\u0000\\u001f"'
    # Everything else is literal UTF-8, including characters a naive
    # implementation would \u-escape.
    assert canonical.serialize("é☃") == '"é☃"'


def test_booleans_are_not_integers():
    """`True` is an `int` in Python, so a class check in the wrong order
    serializes it as `1` and two readers derive different digests from the same
    record."""
    assert canonical.serialize({"x": True}) == '{"x":true}'
    assert canonical.serialize({"x": 1}) == '{"x":1}'
    assert canonical.digest({"x": True}) != canonical.digest({"x": 1})


def test_a_non_integer_number_is_refused_rather_than_serialized():
    """The bound is DECLARED in the contract: this family declares no such value,
    and a digest two readers compute differently is worse than a digest one of
    them refuses."""
    with pytest.raises(canonical.ConstructionError):
        canonical.serialize({"x": 1.5})
    with pytest.raises(canonical.ConstructionError):
        canonical.serialize([1.0])


def test_an_unadmitted_value_class_is_refused_as_a_construction_error():
    """Including a non-string member name, which must surface as the
    construction's own refusal rather than as an AttributeError leaking out of
    the sort key."""
    with pytest.raises(canonical.ConstructionError):
        canonical.serialize({"x": {1, 2}})
    with pytest.raises(canonical.ConstructionError):
        canonical.serialize({1: "a non-string member name"})


def test_the_digest_is_sha256_over_the_serialized_utf8_bytes():
    value = {"b": 1, "a": "é"}
    expected = hashlib.sha256('{"a":"é","b":1}'.encode("utf-8")).hexdigest()
    assert canonical.digest(value) == f"sha256:{expected}"


def test_member_order_in_the_input_does_not_change_the_digest():
    assert canonical.digest({"a": 1, "b": 2}) == canonical.digest({"b": 2, "a": 1})


def test_is_tagged_refuses_an_untagged_or_malformed_digest():
    """An untagged digest cannot be migrated without silently changing meaning,
    which is why every digest a record carries is algorithm-tagged."""
    assert canonical.is_tagged("sha256:" + "0" * 64)
    assert not canonical.is_tagged("0" * 64)
    assert not canonical.is_tagged("sha512:" + "0" * 64)
    assert not canonical.is_tagged("sha256:" + "0" * 63)
    assert not canonical.is_tagged("sha256:" + "A" * 64)  # uppercase is not the tag
    assert not canonical.is_tagged(None)


def test_the_subject_enumeration_matches_the_contract():
    """Every digest NAMES its subject, and the set of subjects lives in the
    contract. A subject this module admits and the contract does not could reach
    a comparison the schema never sanctioned."""
    contract = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert set(contract["$defs"]["digest_subject"]["enum"]) == set(canonical.SUBJECTS)
