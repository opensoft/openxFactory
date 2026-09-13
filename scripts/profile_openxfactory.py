"""WHAT THIS ASSEMBLY IS BUILT WITH: openxFactory's composition point, POST-SHED
(`split-opendox-two-layer-product` § 2.4; § 4.3, RULED ASK-2 option (2),
`#656` comment `5628886636`).

THE FILE THIS REPLACES AND WHY IT IS NOT THE SAME FILE.
`scripts/ideation_dashboard/profile_openxfactory.py` is the carve manifest's
single `deleted_at_carve` row: the § 3 carve deleted it rather than moving it,
because a composition point is not a thing a core or a consumer can own — it
names the contributions THIS assembly's entrypoints are built with, and after
the carve openDox's core names no profile and openXdox declares its own. The
§ 5.2 shed removed that path with the other 318. This module is openxFactory's
composition point AFTER the shed, at a path OUTSIDE the carve surface
(`moved_paths:` covers `scripts/ideation_dashboard/`, not `scripts/`), carrying
the same two tuples re-spelled for the two pinned legs.

WHY THE SPELLINGS CHANGED AND THE RELATIVE IMPORTS DID NOT SURVIVE. The deleted
module imported its three route columns RELATIVELY (`from . import serve_gate`)
for one reason, recorded in its own docstring: `scripts/__init__.py` made the
old tree importable under TWO package spellings (`ideation_dashboard.X` and
`scripts.ideation_dashboard.X`), which are two different module objects, and a
profile had to contribute the column belonging to the SAME spelling as the
entrypoint assembling it. After the shed each column has exactly ONE importable
spelling — `openxdox.serve_gate`, `openxdox.serve_projection`,
`openxdox.cli_gate` at the pinned openXdox leg and
`ideation_dashboard.serve_openxfactory_lanes` here — so the ambiguity the
relative import existed to close no longer exists, and absolute imports say
plainly which leg each column comes from. The identity property that rested on
it still holds and is still asserted (`profile.cli_gate is gate` in
`test_cli_column_split.py`): an absolute import resolves through `sys.modules`
exactly as a relative one does.

`SUBCOMMAND_EXTENSIONS` IS STILL RESOLVED ON ACCESS, for the reason the deleted
module gave and that the shed did not change: `cli_gate` reaches `authoring` ->
`workbench` -> PyYAML, which the hosted image deliberately does not carry
(`test_hosted_posts_do_not_load_notebook_only_dependencies`), while
`ROUTE_EXTENSIONS` is read by `build_server` on EVERY startup, hosted included.
A plain module-scope import of `cli_gate` here would put the CLI column's whole
dependency chain into a server process that only ever wanted the route table.
PEP 562 holds it out; only `cli.py`'s own read of `SUBCOMMAND_EXTENSIONS` pays.

HOW THE CONSUMERS REACH IT, NOW THAT BOTH HALVES EXIST. `opendox.cli` binds
`profile_openxfactory` from `opendox.profile_proxy` and reads
`SUBCOMMAND_EXTENSIONS` off it in `build_parser()`; `opendox.serve` binds the
same proxy inside `build_server()` and reads `ROUTE_EXTENSIONS`. The proxy is
LAZY — it resolves `opendox.domain_profile.current()` at first attribute access
and REFUSES, naming the registration call, when no host has registered
anything. That is RULED ASK-2 option (2) (`#656` comment `5628886636`), landed
as openDox-code #11 (`a99eba03`), and openxFactory's half of it is
`scripts/opendox_host.py`: ONE call at process start,
`opendox.domain_profile.register(<the composite>)`, where the composite is the
`DomainProfile` built from `contracts/domain-profiles/openxfactory-engineering
.yaml` FORWARDING this module's two tuples. This file is still the real
module — it holds what THIS assembly contributes — and it no longer moves: the
import hook that used to bind it into each consumer's namespace
(`carved_reach.bind_composition_point()`) is deleted with the hole it covered.

THE FOURTH FACET, `DISPLAY` (§ 3.4 slice S7's landing precondition,
openxFactory#656 comment `5649744596`; the schema is openDox-code #21's
`src/opendox/display_profile.py`, `PROFILE_FACET = "DISPLAY"`, at head
`90cf05a0`). Resolved on access, like `SUBCOMMAND_EXTENSIONS` and `cli_gate` —
building it reads `openxdox.domain_profile.current()`, which only exists once
`opendox_host.register_openxfactory()` has already run, and every reach of
this name arrives after that call by construction (the composite's own
`__getattr__` is what imports this module in the first place). `serve.py`
reads it through `opendox.display_profile.host_display()` for the
`/capabilities` payload, not through `cli.build_parser()` or
`serve.build_server()`, so it answers no `_LateProfile.READERS` entry those two
composition points consult — a third kind of reader, named in
`opendox_host.FACETS`'s own comment. `_display_facet()` below is the
projection: every word in it reads off the SAME registered profile through its
own public accessors (`profile.status`, `profile.act`, `profile.artifact_kind`,
`profile.lifecycle_for(...).by_role`) rather than being retyped, and its own
docstring states which roles are deliberately left undeclared and why.
"""

from __future__ import annotations

from typing import Any

# ABSOLUTE, and from the leg each column actually lives at now — see the module
# docstring for why the deleted file's relative imports were the right answer to
# a question the shed removed. The openXdox spellings resolve through the pinned
# `openXdox/code/src` that `carved_reach.install()` puts on the path; the lane
# column is openxFactory's own `stays_openxfactory_adapter` row and stays here.
from ideation_dashboard import serve_openxfactory_lanes
from openxdox import serve_gate
from openxdox import serve_projection

#: The route contributions this assembly's SERVER carries, in the order
#: `collect_bindings` consults them — which is observable, so the tuple is a
#: declaration and not an incidental ordering.
#:
#: Three members, unchanged by the shed: openXdox's gate console and its
#: projection/snapshot routes, and openxFactory's own lane routes (RULING DQ-1 —
#: the column that stays with the adapter reaches the seam the same way the
#: column that leaves does).
#:
#: `build_server` registers THIS tuple first and the caller's `route_extensions`
#: after it, so a server built with no `route_extensions` at all serves exactly
#: the routes it served before the seam existed.
ROUTE_EXTENSIONS: tuple = (
    serve_gate.GateRoutesExtension(),
    serve_projection.ProjectionRoutesExtension(),
    serve_openxfactory_lanes.LaneRoutesExtension(),
)


#: THE THREE STATUS VOCABULARIES `opendox.display_profile` PROJECTS, restricted
#: to the roles `profile.status(role, kind=kind)` can answer WITHOUT ambiguity.
#: `governance-document` omits `"out-of-band"` on purpose: its vocabulary
#: carries that role TWICE (`record`, `projection` —
#: `contracts/domain-profiles/openxfactory-engineering.yaml`:158-159) and
#: `DomainProfile.status()` refuses a role that resolves to more than one word
#: within a kind (`ProfileLookupError`) rather than silently picking one — see
#: `_display_facet`'s docstring for why this facet does the same.
_DOCUMENT_STATUS_ROLES: tuple[str, ...] = (
    "captured", "organized", "proposed", "ratified", "promoted", "superseded",
    "retired",
)
_CHANGE_STATUS_ROLES: tuple[str, ...] = ("proposed", "ratified", "promoted", "superseded")
_CANDIDATE_STATUS_ROLES: tuple[str, ...] = ("captured", "proposed", "retired", "superseded")

#: THE FIVE WHEEL ACTS `display_profile.NEUTRAL_DISPLAY["acts"]` names, by
#: role, mapped to THIS profile's own act id (axis 3,
#: `contracts/domain-profiles/openxfactory-engineering.yaml`). Not mechanical —
#: the neutral roles name a universal wheel verb and openxFactory's ids are its
#: own spelling of the same move — so each pairing is a declared fact, cited
#: against the transition row that justifies it:
#:
#: * `derive` -> `derive-possibles` — register-possible's ENTRY transition
#:   ("a lens derives a candidate, or a human authors one").
#: * `brief` -> `research-brief` — no `target_kind`; the wheel's research
#:   action, spelled identically to `NEUTRAL_DISPLAY["acts"]["brief"]`
#:   ("research brief") but for the hyphen.
#: * `promote` -> `promote-to-staging` — register-possible's `latent -> picked`
#:   row: "promotion carries it into ideation/staging/ as a topic", i.e. this
#:   profile's candidate -> selection edge.
#: * `propose` -> `propose` — declared by BOTH staging-topic and
#:   openspec-change ("organized -> proposed"), openxFactory's selection ->
#:   submission edge.
#: * `demote` -> `demote` — openspec-change's mechanized reverse transition,
#:   the gate console's own verb.
_ACT_ROLE_TO_ID: dict[str, str] = {
    "derive": "derive-possibles",
    "brief": "research-brief",
    "promote": "promote-to-staging",
    "propose": "propose",
    "demote": "demote",
}


def _humanize(act_id: str) -> str:
    """`"promote-to-staging"` -> `"Promote to staging"`.

    The profile's `acts:` axis carries no `label:` field (unlike the lifecycle
    vocabulary, which does) — nothing needed one before this facet. Rather than
    typing five new sentences that could drift from the ids `gate_console.py`
    actually dispatches on, the word is DERIVED from the id it must always
    match: hyphens become spaces and the first letter capitalizes, nothing
    else.
    """
    words = act_id.replace("-", " ")
    return words[:1].upper() + words[1:]


def _area_label(profile: Any, role: str) -> str:
    """The one governance-document status declared at `role`, for its label.

    Areas and statuses share the role names `captured` / `organized` /
    `proposed` for the reason `display_profile.AREA_ROLES` gives: an area is
    the corpus folder a document carrying that status lives in while it holds
    it. `captured` and `organized` each resolve to exactly one
    governance-document status — no `out-of-band`-style collision at these two
    roles — so reusing that status's own `label` is a real derivation, not a
    coincidence typed twice.
    """
    matches = profile.lifecycle_for("governance-document").by_role(role)
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly one governance-document status at role "
            f"{role!r} to label the {role!r} area; found "
            f"{[s.id for s in matches]}. _area_label's caller needs updating.")
    return matches[0].label


def _display_facet(profile: Any) -> dict[str, Any]:
    """openxFactory's real `DISPLAY` facet — every word derived, none retyped.

    Conforms to openDox-code #21's schema (`src/opendox/display_profile.py` at
    head `90cf05a0`; NOT YET PINNED — `contracts/opendox-pin.yaml` names
    `a99eba03`, BUILD slice 1b, so this facet targets the schema at that PR's
    current head and `tests/test_engineering_profile_display_facet.py` says so
    rather than importing it). Every value below reads off THIS SAME `profile`
    through its own public accessors (`profile.status(role, kind=kind)`,
    `profile.act(id).id`, `profile.artifact_kind(id).label`,
    `profile.lifecycle_for(kind).by_role(role)`), so a renamed status or act id
    fails this derivation instead of silently drifting from what this facet
    declares.

    NO TWO ROLES SHARE ONE WORD WITHIN A SINGLE VOCABULARY — checked by
    `tests/test_engineering_profile_display_facet.py`, not by this function,
    because the collision that matters is against openDox's own shipped words
    for the roles this facet leaves undeclared, which only `display_manifest`'s
    merge (not this partial declaration alone) can see. openDox-code #21's own
    `90cf05a0` ("two roles may not share one snapshot enum value") enforces
    exactly this for `values.register_state` / `values.document_stage`
    (neither of which this facet declares, so there is nothing here for that
    check to merge against); this profile's own `statuses.document` /
    `statuses.change` / `statuses.candidate` tables are each pairwise distinct
    by construction (`profile.status()` returns one word per role and this
    module asks for none of the roles that collide within a kind — see
    `_DOCUMENT_STATUS_ROLES`), and the test suite asserts it directly rather
    than trusting the construction.

    PARTIAL, DELIBERATELY. `display_profile.normalize_display`'s own stance is
    that partial is legal and is the point — a host declares the roles it has
    real words for and openDox fills the rest from its own neutral vocabulary.
    Four sections/roles this profile could arguably fill are left to that
    neutral rendering instead, each for a reasoned refusal rather than an
    oversight:

    * `statuses.document["out-of-band"]` — see `_DOCUMENT_STATUS_ROLES`.
    * `areas["proposed"]` / `areas["reference"]` — `views/docs.js`'s
      `AREA_ORDER` groups exactly two corpus folders today
      (`ideation/brainstorm/`, `ideation/staging/`); declaring a third prefix
      would invent a corpus layout the shell does not have, and `reference`'s
      prefix is refused by the schema itself regardless (the terminal,
      un-prefixed bucket every other area's documents fall through to).
    * `tokens` — `Display.applyTokens` writes a declared token as a bare
      inline style on `:root`, unconditionally outranking `styles.css`'s
      light / dark-media-query / two `data-theme` rules for that role.
      openxFactory's dashboard has no theme-invariant brand colour — its own
      `--st-*` defaults already vary correctly by theme — so declaring one
      here would PIN a single theme's palette onto every viewer regardless of
      preference: the exact regression `display_profile.py`'s own module
      docstring warns a NEUTRAL FALLBACK could cause, self-inflicted instead
      by a host override that has nothing real to say.
    * `stages`, `values`, `sections` — no established single-word vocabulary
      yet exists for the six pipeline stations distinct from the artifact-kind
      labels already used elsewhere (an open naming question, left to a future
      slice rather than invented here); the snapshot's own enum spellings and
      the staging template's heading order were spot-checked against this
      profile's real words (`register-possible`'s four states; the headings in
      `ideation/staging/*/*.md`) and already agree with openDox's neutral
      defaults, so there is nothing to override.
    """
    def statuses_for(kind: str, roles: tuple[str, ...]) -> dict[str, str]:
        return {role: profile.status(role, kind=kind) for role in roles}

    return {
        "statuses": {
            "document": statuses_for("governance-document", _DOCUMENT_STATUS_ROLES),
            "change": statuses_for("openspec-change", _CHANGE_STATUS_ROLES),
            "candidate": statuses_for("register-possible", _CANDIDATE_STATUS_ROLES),
        },
        "areas": {
            "captured": {
                "prefix": "ideation/brainstorm/",
                "label": _area_label(profile, "captured"),
            },
            "organized": {
                "prefix": "ideation/staging/",
                "label": _area_label(profile, "organized"),
            },
        },
        "acts": {
            role: _humanize(profile.act(act_id).id)
            for role, act_id in _ACT_ROLE_TO_ID.items()
        },
        "artifacts": {
            # "openspec/changes/<name>/" (`ideation/README.md`'s own lifecycle
            # diagram); the label reuses this profile's OWN artifact-kind
            # label for the kind that lives there.
            "root": {
                "prefix": "openspec/changes/",
                "label": profile.artifact_kind("openspec-change").label,
            },
            # The exact order `display_profile.py`'s own `ARTIFACT_ROLES`
            # comment states for openxFactory: "packet is its ORDERED front
            # matter (openxFactory: `proposal.md`, `design.md`, `tasks.md`)".
            "packet": {"order": ["proposal.md", "design.md", "tasks.md"]},
            # "specs/<capability>/spec.md" — the spec-delta subfolder every
            # OpenSpec change carries (CLAUDE.md working rule 3: "Spec deltas
            # use `## ADDED|MODIFIED|REMOVED Requirements`").
            "delta": {"prefix": "specs/", "label": "Spec deltas"},
            # `ideation/README.md`: "Selected staged files are moved... into
            # the change's `supporting-docs/` folder."
            "supporting": {"prefix": "supporting-docs/", "label": "Supporting docs"},
        },
    }


def __getattr__(name: str):
    """`DISPLAY`, `SUBCOMMAND_EXTENSIONS` and `cli_gate` — resolved on first
    access rather than bound at import time (PEP 562).

    Carried across the shed verbatim in behaviour: the tuple's shape and every
    caller's read of it (`cli.py`'s `profile_openxfactory.SUBCOMMAND_EXTENSIONS`,
    the `len(...) == 1` and `isinstance(...[0], cli_gate.GateSubcommands)` pins
    in `test_cli_column_split.py`) are what they were. Only WHEN the import
    happens is held back, never what it returns.

    `cli_gate` is answered here too, for the identity reason a module-scope
    import would have satisfied for free:
    `test_a_library_caller_gets_the_columns_of_its_own_core` asserts
    `profile.cli_gate is gate` — this module's reference to the column must be
    the SAME module object a sibling import of `openxdox.cli_gate` produces, not
    a second one. Any import resolves through `sys.modules`, so answering it on
    first access gives back that identical singleton.

    `DISPLAY` is answered the same lazy way, for a different reason: computing
    it calls `openxdox.domain_profile.current()`, which only succeeds once a
    host has registered — exactly the state every real caller of this name is
    already in (see the module docstring's "THE FOURTH FACET"). No caching: a
    fresh projection every access costs one registry read and a handful of
    dict builds, matches this function's existing stance on
    `SUBCOMMAND_EXTENSIONS`, and can never answer with a profile a host has
    since swapped.
    """
    if name == "DISPLAY":
        from openxdox import domain_profile as engine
        return _display_facet(engine.current())
    if name == "SUBCOMMAND_EXTENSIONS":
        from openxdox import cli_gate
        return (cli_gate.GateSubcommands(),)
    if name == "cli_gate":
        from openxdox import cli_gate
        return cli_gate
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
