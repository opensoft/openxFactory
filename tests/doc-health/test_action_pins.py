"""Self-test for `action_pins.py`, the shared harvester every thin/partial
doc-health family's table-driven action-string pin (steward follow-up to
`#448`, Brett 2026-08-28) relies on. Pinned here rather than trusted: a
harvester that silently found nothing would make every family's table
vacuously "complete"."""

from __future__ import annotations

import textwrap

from action_pins import (assert_actions_pinned, harvest_behavioral,
                         harvest_static)


class _Finding:
    """A minimal stand-in for `doc_health.Finding` — only `.action` is read
    by `harvest_behavioral`."""

    def __init__(self, action):
        self.action = action


def test_harvest_static_finds_a_known_literal_via_the_Finding_shape(tmp_path):
    module = tmp_path / "scratch_with_literal.py"
    module.write_text(textwrap.dedent("""\
        def fam_scratch(ctx):
            return [Finding(ERROR, "scratch", "r", "p", "rule text",
                            "do the known scratch remedy")]
        """))
    found = harvest_static(module)
    assert found == frozenset({"do the known scratch remedy"})


def test_harvest_static_finds_a_literal_through_a_local_wrapper_function(
        tmp_path):
    """The `hit(sev, doc, rule, action)` shape `families.py::fam_tag_hygiene`
    uses: the literal reaches `action` through a module-local function, not a
    direct `Finding(...)` call — the exact pattern the module docstring calls
    out as the second recognized call shape."""
    module = tmp_path / "scratch_with_wrapper.py"
    module.write_text(textwrap.dedent("""\
        def fam_scratch(ctx):
            out = []

            def hit(sev, rule, action):
                out.append(Finding(sev, "scratch", "r", "p", rule, action))

            hit(ERROR, "rule text", "do the wrapped scratch remedy")
            return out
        """))
    found = harvest_static(module)
    assert found == frozenset({"do the wrapped scratch remedy"})


def test_harvest_static_resolves_a_module_level_constant_to_its_text(
        tmp_path):
    """`#448`'s own review caught the opposite mistake — comparing a
    finding's action to the module's constant NAME passes whatever that
    constant is mutated to. The harvester must resolve `_ACTION` to its
    STRING VALUE, not report the constant untouched."""
    module = tmp_path / "scratch_with_constant.py"
    module.write_text(textwrap.dedent("""\
        _ACTION = "do the constant scratch remedy"

        def fam_scratch(ctx):
            return [Finding(ERROR, "scratch", "r", "p", "rule text", _ACTION)]
        """))
    found = harvest_static(module)
    assert found == frozenset({"do the constant scratch remedy"})


def test_harvest_static_reports_zero_on_a_module_with_no_action_literal(
        tmp_path):
    """The negative control: a module that never binds a string literal to
    an `action` parameter must report an EMPTY set, not silently succeed by
    finding something incidental."""
    module = tmp_path / "scratch_with_none.py"
    module.write_text(textwrap.dedent("""\
        def fam_scratch(ctx):
            action = compute_action_dynamically()
            return [Finding(ERROR, "scratch", "r", "p", "rule text", action)]
        """))
    found = harvest_static(module)
    assert found == frozenset()


def test_harvest_static_can_be_scoped_to_named_top_level_functions(tmp_path):
    """The `functions=` scoping a multi-family module (`families.py`) needs:
    an unscoped walk would mix every family's literals into one set."""
    module = tmp_path / "scratch_multi_family.py"
    module.write_text(textwrap.dedent("""\
        def fam_alpha(ctx):
            return [Finding(ERROR, "alpha", "r", "p", "rule", "alpha remedy")]

        def fam_beta(ctx):
            return [Finding(ERROR, "beta", "r", "p", "rule", "beta remedy")]
        """))
    assert harvest_static(module, functions=frozenset({"fam_alpha"})) == \
        frozenset({"alpha remedy"})
    assert harvest_static(module, functions=frozenset({"fam_beta"})) == \
        frozenset({"beta remedy"})
    assert harvest_static(module) == frozenset({"alpha remedy", "beta remedy"})


def test_harvest_behavioral_collects_every_findings_action():
    def fam(ctx):
        return [_Finding("first remedy"), _Finding("second remedy"),
               _Finding("first remedy")]  # a duplicate collapses in the set

    assert harvest_behavioral(fam, ctx=None) == \
        frozenset({"first remedy", "second remedy"})


def test_harvest_behavioral_collects_nothing_from_a_skip():
    class Skip:
        pass

    def fam(ctx):
        return Skip()

    assert harvest_behavioral(fam, ctx=None) == frozenset()


def test_assert_actions_pinned_passes_when_expected_matches_reachable():
    assert_actions_pinned({"a", "b"}, frozenset({"a"}), frozenset({"b"}),
                          family="scratch")


def test_assert_actions_pinned_fails_on_an_emitted_but_unpinned_string():
    try:
        assert_actions_pinned({"a"}, frozenset({"a", "b"}), frozenset(),
                              family="scratch")
    except AssertionError as exc:
        assert "emitted but NOT pinned: ['b']" in str(exc)
    else:
        raise AssertionError("expected the pin check to fail")


def test_assert_actions_pinned_fails_on_a_dead_pinned_string():
    try:
        assert_actions_pinned({"a", "dead"}, frozenset({"a"}), frozenset(),
                              family="scratch")
    except AssertionError as exc:
        assert "pinned but NOT reachable: ['dead']" in str(exc)
    else:
        raise AssertionError("expected the pin check to fail")
