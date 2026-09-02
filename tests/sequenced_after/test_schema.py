"""Feature `sequenced-after-schema` (add-sequenced-after-substrate tasks
3.1-3.4): the `sequenced_after` schema, its front-matter parser, and the
repository-qualified reference grammar.

Loaded as a hyphen-free importable module directly from
`scripts/sequenced_after.py`, the same route `tests/scope_globs` takes.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "sequenced_after.py"


def _load():
    # Loaded under a name that is NOT `sequenced_after`: THIS DIRECTORY is a
    # package by that name (see `__init__.py`), and registering the script module
    # under the package's own name would replace the package in `sys.modules` and
    # abort collection of every sibling test module.
    spec = importlib.util.spec_from_file_location("sequenced_after_substrate", MODULE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module  # dataclass field resolution needs this
    spec.loader.exec_module(module)
    return module


sa = _load()


def _proposal(front_matter: str) -> str:
    return f"---\n{front_matter}\n---\n\n# Proposal\n\nbody\n"


# --- ABSENCE IS NOT `[]` (task 3.2) ------------------------------------------


def test_an_absent_field_returns_the_ABSENT_SENTINEL_not_an_empty_list():
    raw = sa.read_declaration(_proposal(
        "code_surface: openxFactory\ntarget_release: implemented"))
    assert raw is sa.ABSENT
    assert raw != []          # the two are DIFFERENT FACTS
    assert not (raw == [])    # and neither comparison direction may confuse them


def test_an_explicit_empty_sequence_is_a_positive_root_claim():
    raw = sa.read_declaration(_proposal("sequenced_after: []"))
    assert raw == []
    assert raw is not sa.ABSENT
    assert sa.validate_shape(raw).is_root_claim is True


def test_the_sentinel_is_falsy_and_a_singleton():
    assert not sa.ABSENT
    assert sa.ABSENT is sa._Absent()


def test_a_field_present_with_NO_VALUE_is_present_and_malformed():
    # Presence is decided by the KEY, never by the value: a `sequenced_after:`
    # line with nothing after it has DECLARED something, and that something is
    # malformed — reading it as absence would let a null buy the grandfathering
    # that only a truly undeclared change gets.
    raw = sa.read_declaration(_proposal("sequenced_after:"))
    assert raw is not sa.ABSENT
    assert raw is None
    with pytest.raises(sa.SequencedAfterError):
        sa.validate_shape(raw)


def test_a_document_without_front_matter_declares_nothing():
    assert sa.read_declaration("# no front matter\n\nbody") is sa.ABSENT


def test_reads_from_a_path(tmp_path):
    p = tmp_path / "proposal.md"
    p.write_text(_proposal("sequenced_after: [add-parent]"), encoding="utf-8")
    assert sa.read_declaration(p) == ["add-parent"]


def test_reads_the_block_form_too():
    raw = sa.read_declaration(_proposal(
        "sequenced_after:\n  - first-parent\n  - second-parent"))
    assert raw == ["first-parent", "second-parent"]


def test_the_field_is_read_through_the_STRICT_loader():
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.read_declaration(_proposal(
            "sequenced_after: [shown-to-the-reviewer]\n"
            "sequenced_after: [walked-by-the-machine]"))
    assert "duplicate key" in str(exc.value)


def test_validating_the_sentinel_itself_is_refused():
    # A caller must BRANCH on absence rather than hand it to the validator; a
    # shape check that accepted the sentinel would silently validate "nothing".
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_shape(sa.ABSENT)
    assert "absence is NO DECLARATION" in str(exc.value)


# --- the reference grammar (task 3.3) ----------------------------------------


def test_a_bare_entry_is_local():
    entries = sa.validate_shape(["add-parent"]).entries
    assert entries[0].is_local and entries[0].change_id == "add-parent"
    assert entries[0].canonical() == "add-parent"


def test_a_self_qualified_entry_normalizes_to_the_bare_form():
    entries = sa.validate_shape(["openxFactory:add-parent"]).entries
    assert entries[0].is_local, "a self-qualified entry IS the bare form"
    assert entries[0].canonical() == "add-parent"
    assert entries[0].raw == "openxFactory:add-parent"


def test_a_foreign_qualified_entry_is_well_formed_and_stays_qualified():
    declaration = sa.validate_shape(["codexFactory:realize-something"])
    entry = declaration.entries[0]
    assert entry.is_foreign and entry.repository == "codexFactory"
    assert declaration.foreign_refs() == (entry,)
    assert declaration.local_ids() == ()


def test_two_entries_validate_a_fork_must_be_DECLARABLE():
    # OQ-2, ruled ALLOWED: a fork must be declarable for a consuming gate's fork
    # refusal to be reachable and testable at all.
    declaration = sa.validate_shape(["first-parent", "second-parent"])
    assert declaration.local_ids() == ("first-parent", "second-parent")


@pytest.mark.parametrize("entry,fragment", [
    ("Bad-Id", "change-id half"),                    # uppercase
    ("bad_id", "change-id half"),                    # underscore
    ("-leading-hyphen", "change-id half"),           # must start alphanumeric
    ("nested/path", "change-id half"),               # never contains '/'
    ("openspec/changes/x", "change-id half"),        # never names a path
    (":no-repository-half", "repository half"),      # empty repository half
    ("repo:", "change-id half"),                     # empty change-id half
    ("a:b:c", "more than one ':'"),                  # two qualifications
    (" leading-space", "whitespace"),
    ("trailing-space ", "whitespace"),
])
def test_ungrammatical_entries_are_refused_naming_the_rule(entry, fragment):
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_shape([entry])
    assert fragment in str(exc.value)
    assert repr(entry) in str(exc.value) or entry in str(exc.value)


# --- shape (task 3.1) --------------------------------------------------------


@pytest.mark.parametrize("value", ["a-string", 7, {"a": ["b"]}, None])
def test_a_non_sequence_is_refused_rather_than_coerced(value):
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_shape(value)
    assert "must be a sequence" in str(exc.value)


def test_a_bare_string_is_not_coerced_to_a_one_entry_list():
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_shape("add-parent")
    assert "coercion is an interpretation the writer chooses" in str(exc.value)


@pytest.mark.parametrize("member", [None, "", 7, True, 1.5])
def test_a_null_empty_or_non_string_member_is_refused(member):
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_shape([member])
    assert "non-empty strings" in str(exc.value)


@pytest.mark.parametrize("member", [["nested"], {"a": 1}, ("t",)])
def test_a_nested_collection_member_is_refused(member):
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_shape(["ok-parent", member])
    assert "nested" in str(exc.value)


def test_a_duplicate_member_is_refused():
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_shape(["add-parent", "add-parent"])
    assert "twice" in str(exc.value)


def test_a_duplicate_ACROSS_THE_QUALIFICATION_FORMS_is_refused():
    # The one a naive string-set check misses: the self-qualified entry and the
    # bare entry are ONE reference, so declaring both declares a parent twice.
    with pytest.raises(sa.SequencedAfterError) as exc:
        sa.validate_shape(["add-parent", "openxFactory:add-parent"])
    assert "twice" in str(exc.value)


def test_the_same_change_id_under_two_repositories_is_NOT_a_duplicate():
    declaration = sa.validate_shape(["add-parent", "codexFactory:add-parent"])
    assert declaration.canonical_entries() == (
        "add-parent", "codexFactory:add-parent")


def test_entry_ORDER_is_preserved():
    assert sa.validate_shape(["b-parent", "a-parent"]).canonical_entries() == (
        "b-parent", "a-parent")


def test_a_consumer_may_declare_its_own_repository_token():
    # The token decides only which qualified entries normalize to bare. A
    # consumer validating ANOTHER corpus passes its own name.
    declaration = sa.validate_shape(
        ["codexFactory:add-parent"], declaring_repository="codexFactory")
    assert declaration.local_ids() == ("add-parent",)


def test_no_jsonschema_dependency_is_introduced():
    source = MODULE.read_text(encoding="utf-8")
    assert "jsonschema" not in source, (
        "the dependency-free posture of scripts/scope_globs.py is kept")
