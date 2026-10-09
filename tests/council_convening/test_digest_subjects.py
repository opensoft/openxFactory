"""T007: the two digest subjects, and the one construction they join (R3).

`renew-resolved-council-protocol` D1 says "Reuse the provider's existing digest
construction by reference; do not mint another canonicalization", and D3 says
the return uses "the existing digest construction and a distinct versioned
signing context". So the family adds SUBJECTS to `xfc-jcs-sha256-1` and nothing
else:

* `council_convening`: the commission record, the value the snapshot and every
  assignment bind as `convening_digest`;
* `council_seat_return_payload`: a seat's return payload, bound by the return
  context as `return_digest`.

The contract's enumeration is an ordered YAML list, so the append position is
tested there. `canonical.SUBJECTS` is a frozenset, so only membership is tested
in the mirror.

THE KNOWN ANSWER COMES FROM OUTSIDE THIS CODE (U12). The reference
implementation and the corpus generator share `canonical.serialize`, so a bug in
it would agree with itself. The bytes below are copied from RFC 8785 itself:
the sample object of § 3.2.2 with its `numbers` member removed, because the
construction refuses non-integer numbers, and the canonical form § 3.2.3 prints
for it. The RFC text was read on 2026-10-09 from
`https://www.rfc-editor.org/rfc/rfc8785.txt`, SHA-256 `63d52294eb0e3f00…ab240`.
"""

from __future__ import annotations

import pytest
import yaml

from scripts.signed_execution_chain import canonical

from .conftest import DIGEST_CONSTRUCTION

NEW_SUBJECTS = ["council_convening", "council_seat_return_payload"]
DAILY_BATCH = [
    "confirmation_profile_terms", "durability_eligibility_terms",
    "daily_merkle_construction", "durability_event_leaf",
    "daily_batch_node", "daily_batch_root",
]


@pytest.fixture(scope="module")
def construction() -> dict:
    return yaml.safe_load(DIGEST_CONSTRUCTION.read_text(encoding="utf-8"))


def test_both_subjects_are_in_the_contract_enumeration(construction):
    subjects = construction["$defs"]["digest_subject"]["enum"]
    for subject in NEW_SUBJECTS:
        assert subject in subjects


def test_both_subjects_are_in_the_canonical_mirror():
    for subject in NEW_SUBJECTS:
        assert subject in canonical.SUBJECTS


def test_they_are_appended_after_daily_batch_root_with_nothing_reordered(construction):
    subjects = construction["$defs"]["digest_subject"]["enum"]
    assert subjects[28:34] == DAILY_BATCH
    assert subjects[34:] == NEW_SUBJECTS
    assert len(subjects) == len(set(subjects)) == 36


def test_the_mirror_and_the_contract_are_one_set(construction):
    assert set(construction["$defs"]["digest_subject"]["enum"]) == set(canonical.SUBJECTS)


def test_the_construction_name_is_unchanged(construction):
    assert construction["$defs"]["construction_name"]["const"] == "xfc-jcs-sha256-1"
    assert canonical.CONSTRUCTION == "xfc-jcs-sha256-1"


@pytest.mark.parametrize("value", [
    1.5,
    0.1,
    2 ** 53,
    -(2 ** 53),
    "lone \ud800 surrogate",
    {"\udfff": 1},
    [1, 2.0],
])
def test_serialize_refuses_what_the_construction_does_not_admit(value):
    with pytest.raises(canonical.ConstructionError):
        canonical.serialize(value)


def test_the_integer_bound_is_inclusive():
    assert canonical.serialize(2 ** 53 - 1) == "9007199254740991"
    assert canonical.serialize(-(2 ** 53 - 1)) == "-9007199254740991"


def test_the_rfc_8785_known_answer():
    # The RFC's input string, "\\u20ac$\\u000F\\u000aA'\\u0042\\u0022\\u005c\\\\\\"\\/",
    # spelled by code point so that no escape in this file can be misread.
    string = "".join(chr(code) for code in (
        0x20AC, 0x24, 0x0F, 0x0A, 0x41, 0x27, 0x42, 0x22, 0x5C, 0x5C, 0x22, 0x2F))
    parsed = {"string": string, "literals": [None, True, False]}
    # RFC 8785 section 3.2.3, without the `numbers` member, as UTF-8 bytes.
    expected = (b'{"literals":[null,true,false],"string":"'
                b"\xe2\x82\xac$\\u000f\\nA'B\\\"\\\\\\\\\\\"/\"}")
    assert canonical.serialize(parsed).encode("utf-8") == expected
