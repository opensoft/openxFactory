"""openxFactory declares the `DISPLAY` facet openDox-code #21 reads.

WHAT THIS FILE POLICES — § 3.4 slice S7's landing precondition
(`opensoft/openxFactory#656` comment `5649744596`, CLAIM; `5649148461`, the S7
slice this facet's shape conforms to): openDox-code #21
(`src/opendox/display_profile.py`, `PROFILE_FACET = "DISPLAY"`) HAS landed and
is what this repository pins — pin lockstep #2 moved the `code` leg to
`1e469713`, and pin lockstep #3 moved it on to `0b4e8bbf`, where the module is
still present — so every class-C view in `src/opendox/web/` resolves its rendered
vocabulary BY ROLE through the registered host's `DISPLAY` facet, or through
openDox's own NEUTRAL words if the host declares none. Every profile in the
estate is in the second state today. This file is what moves openxFactory's
own dashboard out of it:

  1. `profile_openxfactory.DISPLAY` conforms to #21's schema — checked LIVE,
     by handing the facet to `opendox.display_profile.normalize_display`
     itself (see `test_facet_conforms_to_opendox_schema`). Until the pin
     advanced past #21 the schema was not importable here at all and this
     bullet read "structurally", against a vendored copy; that copy
     (`tests/fixtures-opendox-display-facet-schema.yaml`) and the guard test
     that watched for this moment are both gone.
  2. Every `areas` / `artifacts` prefix the facet declares ends in `/`
     (`display_profile._corpus_prefix`'s own refusal, added on Copilot review
     of #21 itself).
  3. Every status / area / act word the facet declares equals what the
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

import pytest

# noqa: E402 — see tests/domain_profile/test_openxfactory_profile.py, the
# sibling this file follows: conftest has already put `scripts/` on the path
# and made the one registration before any test module here is collected.
import opendox_host                                      # noqa: E402
import profile_openxfactory                               # noqa: E402
from opendox.profile_proxy import profile_openxfactory as proxy  # noqa: E402
from openxdox import domain_profile as engine              # noqa: E402

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
    """(a) The facet conforms to `display_profile`'s own shape — LIVE.

    THE LIVE IMPORT IS NOW THE ONLY PATH. This test used to try
    `from opendox import display_profile` and fall back to a vendored copy of
    #21's schema, because `contracts/opendox-pin.yaml` pinned a `code` leg
    (`05bbde80`, and `a99eba03` before it) in which `display_profile.py` does
    not exist at all. Pin lockstep #2 advanced that leg to `1e469713`
    (openDox-code#21's landing), where it does — verified in the pinned
    checkout's own object store rather than inferred from the pin file:
    `src/opendox/display_profile.py` is ABSENT at `a99eba03` and `05bbde80`,
    PRESENT at `1e469713`, and PRESENT at `0b4e8bbf` — the leg pin lockstep #3
    advances to, checked the same way (`git ls-tree -r 0b4e8bbf` names it and
    `normalize_display` is at its :445). The two shas are a chain, not a
    contradiction: `1e469713` is where the live path became possible, and
    `0b4e8bbf` is the leg this repository pins now.

    So the fallback branch, its vendored fixture
    (`tests/fixtures-opendox-display-facet-schema.yaml`) and the guard test
    `test_the_schema_conformance_path_taken_is_the_expected_one` are all
    deleted here — exactly what that guard's own failure message instructed
    the first bump past #21 to do, and the reason it was written to fail
    loudly instead of quietly flipping branches.

    What replaces them is STRONGER, not weaker. The fallback validated this
    facet against a vendored COPY of #21's schema, which could drift from the
    module it copied; the live path hands the facet to openDox's real
    `normalize_display`, so #21's own refusals — unknown roles, two roles
    sharing one rendered word within a vocabulary, a corpus prefix missing its
    separator — are enforced by the module that owns them.
    """
    facet = profile_openxfactory.DISPLAY
    assert isinstance(facet, dict), f"DISPLAY must be a mapping, got {type(facet)!r}"

    from opendox import display_profile

    assert hasattr(display_profile, "normalize_display"), (
        "opendox.display_profile imported but has no normalize_display(); "
        "the pinned commit is newer than expected and this test needs "
        "re-reading against it")
    normalized = display_profile.normalize_display(facet)
    assert isinstance(normalized, dict)


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


def test_area_labels_equal_the_governance_document_vocabularies_own_label():
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
# 4. deliberate omissions (tokens, values, sections, the wider areas; stages: 8)
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
    assert set(facet["stages"]) == {"completion"}  # the five others: section 8
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
    """`opendox.view_extension.host_profile_name()` IS importable now — pin
    lockstep #2 advanced this repository's pinned `code` leg to `1e469713`,
    which carries `view_extension.py`, and pin lockstep #3 advanced it to
    `0b4e8bbf`, which carries it still (`host_profile_name` included). It did
    not used to be: the pin named
    `a99eba03` (which predates the module entirely) and later `05bbde80`, and
    this docstring said as much.

    The assertion below deliberately does NOT switch to it. What this test
    proves is a REGISTRY property — that both facets ride one registered
    object — and `opendox.domain_profile.name_of()` reads the name off the
    object already in hand, which is exactly that property.
    `host_profile_name()` instead asks the registry for the CURRENT profile's
    name, re-entering the very lookup under test. So the mechanism stays, and
    what was a limitation is now a choice.

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


# --------------------------------------------------------------------------
# 8. openDox's `completion` stage renders "implemented", and the word comes
# FROM openXdox (RULED `opensoft/openxFactory#656` comment `5784683830`, Brett
# Heap, 2026-09-22, verbatim "1, keep completed and overlay implemented")
#
# openDox reads the REGISTERED profile, whose `DISPLAY` is
# `profile_openxfactory.DISPLAY`, and never openXdox's module. So the overlay
# openXdox-code #26 declares (`openxdox.view_extensions.DISPLAY`, `195276b7`)
# reaches a served page only through this repository's facet, which copies it
# in (`profile_openxfactory._openxdox_stages`) rather than restating it. This
# section holds four things: the word a SERVED page shows, the five stations
# that stay neutral, the single source of the word, and what happens when
# openXdox's value is dropped. A dropped value must FAIL these assertions,
# never pass them on openDox's neutral `completed`.
#
# Placed after section 7 rather than beside section 4 on purpose: an OpenSpec
# change on `main` cites this file by line (`amend-home-adapter-scope-and-
# mapping-axis-count`, proposal.md, `:300-303`), so every edit above those
# lines keeps the line count unchanged.
# --------------------------------------------------------------------------

import ast  # noqa: E402
import http.client  # noqa: E402
import json  # noqa: E402
import threading  # noqa: E402

import carved_reach  # noqa: E402
from opendox import display_profile  # noqa: E402
from opendox import serve as serve_mod  # noqa: E402
from openxdox import view_extensions  # noqa: E402

#: The ruled word, spelled once here as the EXPECTED value of the assertions
#: below. It is what a served page must show, not a second source of the word:
#: `test_the_composition_restates_no_stage_word` holds that the files that
#: compose the facet never spell it as a value.
_RULED_WORD = "implemented"

#: The five stations the ruling leaves neutral, derived from openDox's own
#: spine (`display_profile.STAGE_ROLES`) rather than listed by hand.
_NEUTRAL_STAGE_ROLES = tuple(
    role for role in display_profile.STAGE_ROLES if role != "completion")


def _completion_renders_the_ruled_word(stages) -> bool:
    """THE POSITIVE PREDICATE, shared by the served-page test and the drop
    tests, so the drop tests prove that the very check the positive tests make
    refuses a dropped overlay. `short` AND `label`, because they are the
    stage's two rendered names (openXdox-code #26: `views/lineage.js` titles a
    tile with `label` and captions the same tile with `short`); a page
    overlaying only one would show the stage under both words at once."""
    entry = stages["completion"]
    return entry["short"] == _RULED_WORD and entry["label"] == _RULED_WORD


def _assert_the_other_stages_and_fields_stay_neutral(stages) -> None:
    neutral = display_profile.NEUTRAL_DISPLAY["stages"]
    assert len(_NEUTRAL_STAGE_ROLES) == 5, _NEUTRAL_STAGE_ROLES
    for role in _NEUTRAL_STAGE_ROLES:
        assert stages[role] == neutral[role], (
            f"stages.{role} is {stages[role]!r}; the ruling overlays the "
            f"completion stage only, so {role!r} must stay openDox's neutral "
            f"{neutral[role]!r}")
    for field in ("one", "many", "gate"):
        assert stages["completion"][field] == neutral["completion"][field], (
            f"stages.completion.{field} is {stages['completion'][field]!r}; "
            "the overlay is `short` and `label` only, so the item nouns and "
            "the gate stay openDox's")


def _served_capabilities(tmp_path):
    """GET /capabilities from a REAL openDox server, built the way this
    assembly builds one. `tests/conftest.py` has already made the ONE
    registration, so `build_server()` reads `ROUTE_EXTENSIONS` and `DISPLAY`
    through the same lazy proxy a production process does. The asset root is
    derived from the carve manifest's row for `index.html`, as
    `tests/ideation-dashboard/conftest.py::dashboard_web_root` derives it."""
    web = carved_reach.source("scripts/ideation_dashboard/web/index.html").parent
    checkout = tmp_path / "openx"
    (checkout / "ideation").mkdir(parents=True)
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text(json.dumps({"generation": {}}), encoding="utf-8")
    httpd = serve_mod.build_server(web, snapshot, checkout, host="127.0.0.1")
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = httpd.server_address[:2]
        conn = http.client.HTTPConnection(host, port, timeout=10)
        try:
            conn.request("GET", "/capabilities")
            response = conn.getresponse()
            status, body = response.status, response.read()
        finally:
            conn.close()
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)
    assert status == 200, status
    return json.loads(body.decode("utf-8"))


def test_the_served_page_shows_implemented_for_the_completion_stage(tmp_path):
    """THE RULING, AS A SERVED PAGE READS IT. The `display` block of
    `/capabilities` is what every class-C view in openDox's shell resolves its
    stage words from, so this is the page's own reading of the stage, taken
    from a running server rather than from a replay of its statement."""
    display = _served_capabilities(tmp_path)["display"]
    assert display["host_facet"] == "declared"
    assert display["host_profile"] == "openxfactory-engineering"
    assert display["stage_order"] == list(display_profile.STAGE_ROLES)
    assert _completion_renders_the_ruled_word(display["stages"]), (
        f"the served completion stage is {display['stages']['completion']!r}; "
        f"RULED 5784683830 overlays {_RULED_WORD!r} on it for the xFactory "
        "host, from openxdox.view_extensions.DISPLAY")
    _assert_the_other_stages_and_fields_stay_neutral(display["stages"])


def test_the_normalized_facet_renders_implemented_and_five_neutral_stages():
    """The same property through `normalize_display` directly, the merge the
    served block is built from. And no two stations share a rendered word
    after the overlay, so a view that maps a word back to its stage still
    can."""
    merged = display_profile.normalize_display(profile_openxfactory.DISPLAY)
    assert _completion_renders_the_ruled_word(merged["stages"])
    _assert_the_other_stages_and_fields_stay_neutral(merged["stages"])
    for field in ("short", "label"):
        words = [merged["stages"][role][field]
                 for role in display_profile.STAGE_ROLES]
        assert len(set(words)) == len(words), (field, words)


def test_the_stage_words_are_openxdoxs_own_copied_not_restated():
    """ONE SOURCE. The facet's `stages` equal openXdox's declaration exactly,
    and they are a COPY at both levels, so a reader that mutates the facet it
    was handed cannot rewrite openXdox's module-level declaration."""
    facet = profile_openxfactory.DISPLAY
    assert facet["stages"] == view_extensions.DISPLAY["stages"]
    assert facet["stages"] is not view_extensions.DISPLAY["stages"]
    for role, entry in facet["stages"].items():
        assert entry is not view_extensions.DISPLAY["stages"][role], role


def test_stages_is_the_one_section_openxdox_declares_and_the_one_composed():
    """`_openxdox_stages()` composes openXdox's `stages` and nothing else,
    because this facet answers every other section from the registered
    profile. So a section openXdox adds later is a decision for
    `scripts/profile_openxfactory.py`, and it surfaces HERE, at the pin bump
    that carries it, rather than being merged or dropped silently."""
    assert set(view_extensions.DISPLAY) == {"stages"}, (
        f"openxdox.view_extensions.DISPLAY now declares "
        f"{sorted(view_extensions.DISPLAY)}; openxFactory composes only "
        "`stages` from it. Decide whether this facet composes the new "
        "section, in scripts/profile_openxfactory.py::_openxdox_stages, and "
        "update this test with the reason.")


def test_the_composition_restates_no_stage_word():
    """The ruled word must not be spelled as a VALUE in the files that compose
    the facet, or it would have two sources, and a pin that dropped openXdox's
    would leave this repository's copy serving on. Docstrings and comments may
    name it; no other string constant may be it."""
    for rel in ("scripts/profile_openxfactory.py", "scripts/opendox_host.py"):
        source = (opendox_host.REPO_ROOT / rel).read_text(encoding="utf-8")
        tree = ast.parse(source)
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                 ast.AsyncFunctionDef)):
                first = node.body[0] if node.body else None
                if (isinstance(first, ast.Expr)
                        and isinstance(first.value, ast.Constant)
                        and isinstance(first.value.value, str)):
                    docstrings.add(id(first.value))
        spelled = [node.lineno for node in ast.walk(tree)
                   if isinstance(node, ast.Constant)
                   and isinstance(node.value, str)
                   and id(node) not in docstrings
                   and node.value.strip().casefold() == _RULED_WORD]
        assert not spelled, (
            f"{rel} spells {_RULED_WORD!r} as a value at lines {spelled}; the "
            "word belongs to openxdox.view_extensions.DISPLAY alone")


#: The well-formed openXdox declarations that overlay LESS than the ruling:
#: each is legal to openDox's schema, so the composer follows it, and each
#: must fail the positive predicate the served-page test uses.
_SHORTFALLS = {
    "openxdox-declares-no-stages": {},
    "openxdox-declares-an-empty-stages-mapping": {"stages": {}},
    "openxdox-overlays-short-only": {
        "stages": {"completion": {"short": _RULED_WORD}}},
}


@pytest.mark.parametrize("drop", [*_SHORTFALLS, "the-composition-drops-them"])
def test_a_dropped_or_partial_overlay_fails_the_positive_predicate(
        monkeypatch, drop):
    """MUTATION: openXdox's value dropped or cut short, either upstream (its
    `DISPLAY` carries no `stages`, an empty `stages`, or `short` alone) or
    here (the composition stops copying them).

    THE COMPOSER FOLLOWS these at run time, by design. Each is a well-formed
    declaration that openDox's schema holds legal, and
    `profile_openxfactory._openxdox_stages`'s docstring ("THREE CASES") says
    why run time does not second-guess openXdox. The refusal happens at the
    GATE. The page falls back to openDox's neutral word, and the predicate
    that `test_the_served_page_shows_implemented_for_the_completion_stage`
    uses refuses that state, so a pin bump that carries such a leg fails the
    required suite and cannot land."""
    if drop in _SHORTFALLS:
        monkeypatch.setattr(view_extensions, "DISPLAY", _SHORTFALLS[drop])
    else:
        monkeypatch.setattr(profile_openxfactory, "_openxdox_stages",
                            lambda: {})
    merged = display_profile.normalize_display(profile_openxfactory.DISPLAY)
    neutral = display_profile.NEUTRAL_DISPLAY["stages"]["completion"]
    assert merged["stages"]["completion"]["label"] == neutral["label"]
    assert not _completion_renders_the_ruled_word(merged["stages"])


def test_a_missing_openxdox_display_refuses_rather_than_serving_absent(
        monkeypatch):
    """MUTATION: openXdox's `DISPLAY` gone altogether, which is what a pin
    naming a code leg older than openXdox-code #26 looks like.

    `host_display()` reads the facet through a 3-argument `getattr(..., None)`,
    and the lazy proxy re-raises an `AttributeError` as `ProfileFacetMissing`,
    itself an `AttributeError`, so that `getattr` absorbs it as "no facet
    declared". Were this refusal an `AttributeError`, the WHOLE facet
    (statuses, areas, acts and artifacts too) would be served as absent, and
    the page would come up in openDox's neutral words with nothing reporting
    why. It is a `RuntimeError`, so it passes through the proxy and the
    reader and reaches the server build as a refusal."""
    monkeypatch.delattr(view_extensions, "DISPLAY")
    with pytest.raises(RuntimeError, match="declares no DISPLAY") as caught:
        profile_openxfactory.DISPLAY
    assert not isinstance(caught.value, AttributeError)
    with pytest.raises(RuntimeError, match="declares no DISPLAY"):
        display_profile.host_display(proxy)


#: The malformed shapes, one per level of the structure `_openxdox_stages()`
#: reads: the facet itself, its `stages` section, and a stage entry.
_MALFORMED = {
    "display-is-not-a-mapping": ["stages"],
    "display-is-a-string": "stages",
    "stages-is-not-a-mapping": {"stages": ["completion"]},
    "a-stage-entry-is-not-a-mapping": {"stages": {"completion": _RULED_WORD}},
}


@pytest.mark.parametrize("shape", list(_MALFORMED))
def test_a_malformed_openxdox_display_refuses_at_every_level(monkeypatch, shape):
    """MUTATION: openXdox's `DISPLAY` present but MALFORMED, at each of the
    three levels the composer reads (Copilot `r4086188263`: the refusal had no
    test, so removing it would have passed the suite). Each shape REFUSES, and
    with `RuntimeError`, never `AttributeError`, so neither the proxy nor
    `host_display()`'s 3-argument `getattr` can absorb it into a silent
    "no facet declared"."""
    monkeypatch.setattr(view_extensions, "DISPLAY", _MALFORMED[shape])
    with pytest.raises(RuntimeError, match="must be a mapping of stage") as caught:
        profile_openxfactory.DISPLAY
    assert not isinstance(caught.value, AttributeError)
    with pytest.raises(RuntimeError, match="must be a mapping of stage"):
        display_profile.host_display(proxy)
