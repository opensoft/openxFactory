"""openxFactory declares the `DISPLAY` facet openDox-code #21 reads.

WHAT THIS FILE POLICES — § 3.4 slice S7's landing precondition
(`opensoft/openxFactory#656` comment `5649744596`, CLAIM; `5649148461`, the S7
slice this facet's shape conforms to): once openDox-code #21
(`src/opendox/display_profile.py`, `PROFILE_FACET = "DISPLAY"`) lands, every
class-C view in `src/opendox/web/` resolves its rendered vocabulary BY ROLE
through the registered host's `DISPLAY` facet, or through openDox's own
NEUTRAL words if the host declares none. Every profile in the estate is in the
second state today. This file is what moves openxFactory's own dashboard out
of it:

  1. `profile_openxfactory.DISPLAY` conforms to #21's schema (structurally,
     since the schema is not yet importable at this repository's pinned
     openDox commit — see `test_facet_conforms_to_opendox_schema`).
  2. Every `areas` / `artifacts` prefix the facet declares ends in `/`
     (`display_profile._corpus_prefix`'s own refusal, added on Copilot review
     of #21 itself).
  3. Every status / area / role word the facet declares equals what the
     REGISTERED PROFILE's own public accessors say — never retyped, so a
     renamed status or act id in
     `contracts/domain-profiles/openxfactory-engineering.yaml` fails these
     assertions instead of leaving a stale word behind silently.
  4. The facet resolves end to end, through the exact chain a real class-C
     view reaches: `opendox.profile_proxy.profile_openxfactory.DISPLAY` ->
     `opendox_host.OpenxFactoryProfile.__getattr__` ->
     `profile_openxfactory.DISPLAY` (this repository's own contribution).
  5. No two roles within one vocabulary share a rendered word (openDox-code
     #21 at head `90cf05a0`, "two roles may not share one snapshot enum
     value" — Copilot round 4), and this facet sits on the exact same
     registered profile OBJECT every other facet (`ROUTE_EXTENSIONS`, and
     once forwarded, `VIEW_EXTENSIONS`) rides — never a separately loaded or
     freshly constructed one.

`tests/conftest.py` has already installed the reach and made the ONE
registration call, exactly as `tests/domain_profile/test_openxfactory_profile
.py` documents, so every name below resolves the way it does in a real
assembly point.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

# noqa: E402 — see tests/domain_profile/test_openxfactory_profile.py, the
# sibling this file follows: conftest has already put `scripts/` on the path
# and made the one registration before any test module here is collected.
import opendox_host                                      # noqa: E402
import profile_openxfactory                               # noqa: E402
from opendox.profile_proxy import profile_openxfactory as proxy  # noqa: E402
from openxdox import domain_profile as engine              # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
VENDORED_SCHEMA_PATH = REPO_ROOT / "tests" / "fixtures-opendox-display-facet-schema.yaml"

#: The exact three vocabularies `opendox.display_profile._STATUS_VOCABULARIES`
#: declares, and the artifact kind + role subset this facet answers them with
#: (`profile_openxfactory._DOCUMENT_STATUS_ROLES` and its two siblings).
_KIND_BY_VOCABULARY = {
    "document": "governance-document",
    "change": "openspec-change",
    "candidate": "register-possible",
}


# --------------------------------------------------------------------------
# 1. conformance to openDox-code #21's schema
# --------------------------------------------------------------------------

def test_facet_conforms_to_opendox_schema():
    """(a) The facet conforms to `display_profile`'s own shape.

    TRIES THE LIVE IMPORT FIRST. `contracts/opendox-pin.yaml` pins openDox's
    code leg at `a99eba03` (BUILD slice 1b), which predates openDox-code #21
    (`display_profile.py` does not exist in that tree at all — confirmed by
    reading the pinned checkout directly), so `from opendox import
    display_profile` is expected to fail here and this SAYS SO in the
    assertion message on both branches rather than passing silently either
    way. Once the pin advances past #21's landing, the first branch starts
    running for real and the vendored fixture (and this fallback) should be
    deleted.
    """
    facet = profile_openxfactory.DISPLAY
    assert isinstance(facet, dict), f"DISPLAY must be a mapping, got {type(facet)!r}"

    try:
        from opendox import display_profile
    except ImportError as exc:
        pytest.importorskip("jsonschema")
        import jsonschema

        assert VENDORED_SCHEMA_PATH.is_file(), (
            f"{VENDORED_SCHEMA_PATH} is missing — the vendored fallback "
            "schema this test needs (because the live import failed: "
            f"{exc}) is not on disk")
        schema = yaml.safe_load(VENDORED_SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(facet), key=lambda e: list(e.path))
        assert errors == [], (
            "SAYING SO: opendox.display_profile is not importable at this "
            f"repository's pinned openDox commit ({exc}), so this facet was "
            f"checked against the VENDORED fixture {VENDORED_SCHEMA_PATH.name} "
            "instead — and failed it:\n" +
            "\n".join(f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
                       for e in errors))
        # SAYING SO, on the PASSING path too (not just the failure message
        # above): printed rather than asserted, because a vendored-fixture
        # pass is the expected, correct outcome today and must stay green —
        # `test_the_schema_conformance_path_taken_is_the_expected_one` is the
        # assertion that this branch (and not the live one) is the one
        # running, and fails loudly the day that stops being true.
        print(
            f"DISPLAY facet checked against the VENDORED fixture "
            f"{VENDORED_SCHEMA_PATH.name}, not a live `opendox.display_profile` "
            f"import ({exc}) — contracts/opendox-pin.yaml pins openDox before "
            "openDox-code #21 landed it.")
        return

    # THE LIVE PATH — reachable once the pin advances past #21.
    assert hasattr(display_profile, "normalize_display"), (
        "opendox.display_profile imported but has no normalize_display(); "
        "the pinned commit is newer than expected and this test needs "
        "re-reading against it")
    normalized = display_profile.normalize_display(facet)
    assert isinstance(normalized, dict)


def test_the_schema_conformance_path_taken_is_the_expected_one():
    """A guard on the guard above: today, the FALLBACK branch must run.

    If this starts failing because `from opendox import display_profile`
    now succeeds, that is GOOD NEWS (the pin advanced past #21) and the fix
    is to delete the vendored fixture and simplify the test above to the live
    path only — not to chase this assertion.
    """
    try:
        from opendox import display_profile  # noqa: F401
    except ImportError:
        return
    pytest.fail(
        "opendox.display_profile is now importable at this repository's "
        "pinned openDox commit — contracts/opendox-pin.yaml has advanced "
        "past openDox-code #21. Delete "
        "tests/fixtures-opendox-display-facet-schema.yaml and this test, and "
        "simplify test_facet_conforms_to_opendox_schema to the live-import "
        "path only.")


# --------------------------------------------------------------------------
# 2. every corpus prefix ends in `/`
# --------------------------------------------------------------------------

def test_every_area_and_artifact_prefix_ends_in_a_separator():
    """(b) `display_profile._corpus_prefix`'s own refusal, checked here too.

    A declared prefix is compared with a prefix test and composed into a
    path, so `"ideation/staging"` without the separator would both claim
    `ideation/stagingfoo/x.md` and compose `ideation/staging<id>` where a
    folder was meant (openDox-code #21, Copilot review).
    """
    facet = profile_openxfactory.DISPLAY
    checked = []
    for section in ("areas", "artifacts"):
        for role, entry in facet[section].items():
            prefix = entry.get("prefix")
            if prefix is None:
                continue
            assert prefix.endswith("/"), (
                f"{section}.{role}.prefix {prefix!r} does not end in '/'")
            checked.append(f"{section}.{role}")
    # Locks in exactly which roles carry a prefix today (areas.captured,
    # areas.organized, artifacts.root, artifacts.delta,
    # artifacts.supporting — five; `artifacts.packet` has an `order`, not a
    # `prefix`) so a silently dropped or silently added prefix fails here
    # rather than only weakening this test's own coverage.
    assert sorted(checked) == [
        "areas.captured", "areas.organized", "artifacts.delta",
        "artifacts.root", "artifacts.supporting",
    ], checked


# --------------------------------------------------------------------------
# 3. every status / area / role word equals the registered profile's own
# --------------------------------------------------------------------------

def test_status_words_equal_the_registered_profiles_own_vocabulary():
    """(c), the statuses half. Re-derived independently through
    `DomainProfile.status()` rather than compared against this module's own
    private role tuples, so a bug shared by both the implementation and this
    test (e.g. both hardcoding `"draft"`) cannot pass silently."""
    profile = engine.current()
    facet = profile_openxfactory.DISPLAY
    role_tables = {
        "document": profile_openxfactory._DOCUMENT_STATUS_ROLES,
        "change": profile_openxfactory._CHANGE_STATUS_ROLES,
        "candidate": profile_openxfactory._CANDIDATE_STATUS_ROLES,
    }
    for vocabulary, roles in role_tables.items():
        kind = _KIND_BY_VOCABULARY[vocabulary]
        assert set(facet["statuses"][vocabulary]) == set(roles), (
            f"statuses.{vocabulary} declares a different role set than "
            f"expected: {sorted(facet['statuses'][vocabulary])} vs "
            f"{sorted(roles)}")
        for role in roles:
            expected = profile.status(role, kind=kind)
            assert facet["statuses"][vocabulary][role] == expected, (
                f"statuses.{vocabulary}.{role} is "
                f"{facet['statuses'][vocabulary][role]!r}, but the registered "
                f"profile's own status(role={role!r}, kind={kind!r}) says "
                f"{expected!r}")


def test_the_out_of_band_role_really_is_ambiguous_for_governance_document():
    """The reason `statuses.document` omits `"out-of-band"`, proven rather
    than asserted: `governance-document`'s vocabulary carries that role
    TWICE (`record`, `projection`), and the engine's own `status()` refuses
    to pick one."""
    profile = engine.current()
    with pytest.raises(engine.ProfileLookupError, match="ambiguous"):
        profile.status("out-of-band", kind="governance-document")
    assert "out-of-band" not in profile_openxfactory.DISPLAY["statuses"]["document"]


def test_area_labels_equal_the_governance_document_vocabularys_own_label():
    """(c), the areas half. `captured` / `organized` each resolve to exactly
    one governance-document status, so the area's label can reuse — and must
    equal — that status's own `label` field."""
    profile = engine.current()
    facet = profile_openxfactory.DISPLAY
    assert set(facet["areas"]) == {"captured", "organized"}
    for role in ("captured", "organized"):
        matches = profile.lifecycle_for("governance-document").by_role(role)
        assert len(matches) == 1, (role, matches)
        assert facet["areas"][role]["label"] == matches[0].label


def test_area_prefixes_are_the_real_corpus_folders():
    """`ideation/README.md`'s own lifecycle diagram names these two folders;
    a change to either is a change to the README first."""
    facet = profile_openxfactory.DISPLAY
    assert facet["areas"]["captured"]["prefix"] == "ideation/brainstorm/"
    assert facet["areas"]["organized"]["prefix"] == "ideation/staging/"


def test_act_words_are_the_profiles_own_act_id_humanized():
    """(c), the role-label half — `acts`, this facet's projection of
    `display_profile.NEUTRAL_DISPLAY["acts"]`'s five roles. Re-derived from
    `DomainProfile.act(id).id` (never from this module's private mapping's
    VALUES) so a renamed act id fails here rather than leaving a stale label
    behind."""
    profile = engine.current()
    facet = profile_openxfactory.DISPLAY
    assert set(facet["acts"]) == {"derive", "brief", "promote", "propose", "demote"}
    for role, act_id in profile_openxfactory._ACT_ROLE_TO_ID.items():
        real_id = profile.act(act_id).id
        expected = real_id.replace("-", " ")
        expected = expected[:1].upper() + expected[1:]
        assert facet["acts"][role] == expected, (
            f"acts.{role} is {facet['acts'][role]!r}, expected {expected!r} "
            f"(humanized from act id {real_id!r})")


def test_root_artifact_label_equals_the_openspec_change_kinds_own_label():
    """(c), the artifacts half. `artifacts.root` is where an OpenSpec change
    lives; its label reuses that artifact kind's own declared label rather
    than a new string."""
    profile = engine.current()
    facet = profile_openxfactory.DISPLAY
    assert (facet["artifacts"]["root"]["label"]
            == profile.artifact_kind("openspec-change").label)


def test_the_packet_order_matches_display_profiles_own_stated_answer():
    """`display_profile.py`'s own `ARTIFACT_ROLES` docstring states
    openxFactory's expected packet order verbatim: `proposal.md`, `design.md`,
    `tasks.md`. Locked in here as an ordinary list assertion (there is no
    third source to re-derive it from — it is openxFactory's own authored
    convention, stated once by the schema's own author and once here)."""
    facet = profile_openxfactory.DISPLAY
    assert facet["artifacts"]["packet"]["order"] == [
        "proposal.md", "design.md", "tasks.md"]


# --------------------------------------------------------------------------
# 4. deliberate omissions (tokens, stages, values, sections, the wider areas)
# --------------------------------------------------------------------------

def test_sections_this_facet_deliberately_does_not_declare():
    """Absence asserted, not just unmentioned — so a future edit that adds
    one of these back in does so on purpose, having read (and updated) the
    reasoning in `profile_openxfactory._display_facet`'s own docstring.

    `tokens` is the one with a real regression behind it:
    `Display.applyTokens` (openDox-code #21) writes a declared token as a
    bare inline style on `:root`, unconditionally outranking every theme
    rule `styles.css` restates for it (light, the dark media query, both
    `data-theme` choices). openxFactory's dashboard has no theme-invariant
    brand colour, so declaring one here would pin a single theme's palette
    onto every viewer regardless of preference.
    """
    facet = profile_openxfactory.DISPLAY
    assert "tokens" not in facet
    assert "stages" not in facet
    assert "values" not in facet
    assert "sections" not in facet
    assert "proposed" not in facet["areas"]
    assert "reference" not in facet["areas"]


# --------------------------------------------------------------------------
# 5. end-to-end resolution through the real composition chain
# --------------------------------------------------------------------------

def test_display_is_declared_in_the_hosts_forwarded_facets():
    assert "DISPLAY" in opendox_host.FACETS


def test_the_facet_resolves_through_the_full_composition_chain():
    """The exact path a class-C view's `display_profile.host_display()`
    walks: `opendox.profile_proxy.profile_openxfactory.DISPLAY` ->
    `OpenxFactoryProfile.__getattr__` (ordinary dataclass lookup fails, falls
    to the composite's own `__getattr__`) -> `profile_openxfactory.DISPLAY`
    (this repository's contribution, computed by `_display_facet`)."""
    assert proxy.DISPLAY == profile_openxfactory.DISPLAY
    assert opendox_host.profile().DISPLAY == profile_openxfactory.DISPLAY
    assert engine.current().DISPLAY == profile_openxfactory.DISPLAY


def test_a_facet_named_like_a_profile_field_would_be_refused_and_display_is_not_one():
    """`opendox_host.build_profile`'s own collision guard
    (`test_a_facet_colliding_with_a_profile_field_is_refused_at_compose_time`
    in the sibling profile test proves the guard fires; this proves "DISPLAY"
    specifically does not trip it) — `DomainProfile`'s fields are
    `mapping_id`, `artifact_kinds`, `lifecycle`, `acts`, `evidence_classes`,
    `authorities`, `truth_store`, `neutral`, `domain_label`, `declared_by`,
    `gates`, `basis`, `notes`, `source`, `extra`; none is `"DISPLAY"`."""
    loaded = engine.load(opendox_host.PROFILE_PATH)
    assert not hasattr(loaded, "DISPLAY")


# --------------------------------------------------------------------------
# 6. no two roles share one word within a vocabulary (openDox-code #21 at
# head `90cf05a0`, "two roles may not share one snapshot enum value")
# --------------------------------------------------------------------------

def test_no_two_roles_share_one_word_within_any_statuses_vocabulary():
    """The reverse-lookup rule `display_profile._refuse_duplicate_enum_values`
    enforces for `values.register_state` / `values.document_stage`
    (openDox-code #21 `90cf05a0`, Copilot round 4) applies for the same reason
    to `statuses.change` — read at BOTH the submission and completion
    stations, since both render `changes[]` items through the SAME `"change"`
    vocabulary — and, for consistency, to `statuses.document` and
    `statuses.candidate` too: a view that ever needs to resolve a rendered
    word back to the role it came from cannot if two roles share one word.

    This facet's own declaration is checked directly (not merged against
    openDox's neutral words first, unlike the real `_refuse_duplicate_enum_
    values`) because `statuses` is not merged per-role the way `values` is —
    this facet declares every role for `change` and `candidate` and all but
    one (the ambiguous `out-of-band`) for `document`, so there is nothing of
    openDox's own left to merge in and collide with for these three tables.
    """
    facet = profile_openxfactory.DISPLAY
    for vocabulary, words in facet["statuses"].items():
        seen: dict[str, str] = {}
        for role, word in words.items():
            assert word not in seen, (
                f"statuses.{vocabulary} gives {word!r} to BOTH {seen.get(word)!r} "
                f"and {role!r} — a view resolving this word back to its role "
                "cannot tell them apart")
            seen[word] = role


def test_no_two_roles_share_one_word_within_acts_or_areas():
    """Same property, checked across this facet's other role tables too —
    cheap insurance against the identical class of mistake Copilot found
    twice in openDox-code #21 itself (round 1: `ACT_IDS` vs. a four-word
    `acts` table; round 4: the snapshot-value enums)."""
    facet = profile_openxfactory.DISPLAY
    acts_words = list(facet["acts"].values())
    assert len(acts_words) == len(set(acts_words)), facet["acts"]
    area_labels = [entry["label"] for entry in facet["areas"].values()]
    assert len(area_labels) == len(set(area_labels)), facet["areas"]


# --------------------------------------------------------------------------
# 7. this facet sits on the SAME registered profile object every other facet
# does (coordinator correction: `view_extension.host_profile_name`, openDox-
# code #21 at head `90cf05a0`, names whatever `domain_profile.current()`
# answers — `ROUTE_EXTENSIONS`, and once forwarded, `VIEW_EXTENSIONS`, must
# name that identical object)
# --------------------------------------------------------------------------

def test_display_and_route_extensions_ride_the_identical_registered_object():
    """`opendox.view_extension.host_profile_name()` is not importable at this
    repository's PINNED openDox commit (`a99eba03` predates even the module it
    lives in), so this proves the property it will rely on using what IS
    pinned: `opendox.domain_profile.name_of()`, already present at `a99eba03`
    (`profile_proxy.py`'s own refusal message already quotes it).

    `_LateProfile.resolve()` calls `domain_profile.current()` fresh on every
    attribute access (no cache) — so this asserts the registry hands back the
    SAME object across two separate resolutions, one triggered by reading
    `ROUTE_EXTENSIONS` and one by reading `DISPLAY`, and that both facets sit
    on that one object rather than on two independently-built profiles.
    """
    from opendox import domain_profile as opendox_registry

    before = engine.current()
    routes = proxy.ROUTE_EXTENSIONS               # resolves current() again
    after_routes = engine.current()
    display = proxy.DISPLAY                        # resolves current() again
    after_display = engine.current()

    assert before is after_routes is after_display, (
        "ROUTE_EXTENSIONS and DISPLAY resolved through two different "
        "registered profile objects")
    assert routes is opendox_host.profile().ROUTE_EXTENSIONS
    assert display == opendox_host.profile().DISPLAY

    # THE NAME, the same way `host_profile_name()` will report it once
    # `serve.py` is switched over: `domain_profile.name_of()` on the object
    # both facets share.
    assert (opendox_registry.name_of(before)
            == opendox_registry.name_of(after_display)
            == "openxfactory-engineering")
