"""Shared derivation of every action string a doc-health family can emit.

Steward follow-up (Brett, 2026-08-28) to `#448` (`cadc05ec`): that change
pinned ONE representative action string per family. A family whose
`fam_*`/`check_*` function raises several distinct classes of finding — each
with its own operator-guidance text — had every string BUT the one pinned
free to drift silently, exactly the blind spot `#448` closed for the first
string only. This module gives every family's own suite a single, reusable
way to pin the WHOLE set, table-driven, with two independent derivations
feeding one two-directional equality check.

Two derivations
---------------

BEHAVIORAL (`harvest_behavioral`) — run the family's function over a real
`Context` (built the same way that family's OTHER tests build one — the
existing, untouched fixture corpus under `fixtures/<family>/`, read via
`conftest.make_ctx`) and collect ``{f.action for f in findings}``. This is
ground truth: the family's own code produced the string on a real run.

STATIC (`harvest_static`) — read the family's SOURCE module with `ast` and
collect every string literal that reaches a parameter named `action`
anywhere a `Finding` (or a local helper that itself forwards to one) is
constructed. Two call shapes are recognized, because both occur in this
corpus:

  - a call to something literally named ``Finding`` — the dataclass every
    family ultimately constructs a finding through (`severity, family, repo,
    path, rule, action, resolution=..., disposer=...` — action is its sixth
    positional field, but this reads by PARAMETER NAME, not position, so a
    reordering would not silently go uncovered);
  - a call to a module-local function (`def`, possibly nested, anywhere in
    the same module) whose OWN parameter list names a parameter `action` —
    the ``hit(sev, doc, rule, action)`` wrapper in
    `families.py::fam_tag_hygiene` and the ``_finding(cls, severity, repo,
    path, detail, action, resolution=...)`` / ``bad(cls, detail, action)``
    wrappers in `ideation_routing.py` are exactly this shape.

A literal reached through a NAME (``_CUT_ACTION = "..."``, resolved from a
plain ``NAME = "<literal>"`` assignment anywhere in the module — see
`harvest_static`'s own comment for the walk-order and last-assignment-wins
details) is resolved to its string VALUE, so a table pins the TEXT, never a
constant's name — the mistake `#448`'s own review caught and fixed
(`test_the_marker_class_keeps_its_own_action_and_not_the_arms_one` compared a
finding's action to `mbc._MARKER_ACTION` itself, which passed whatever that
constant had been mutated to; see `4def2274`/the `#448` merge commit body).

Most families in this corpus write their action text as a fixed literal, but
not all: `client_identity_composition.py` (two sites), `neutrality_dispatch.py`,
and `semantic.py` build their action with an f-string — operator guidance
that interpolates a per-occurrence detail (a client name, a disposer, a seed
reference) rather than staying fixed. None of those three modules uses this
harvester (each pins its handful of actions directly in its own suite,
compared against the finding's `.action` at a real, fixed input); every
family that DOES go through `harvest_static`/`harvest_behavioral` writes
every action as a literal, which is why a non-literal expression bound to an
`action` parameter, though it exists elsewhere in the corpus, is silently
skipped by the static harvester here rather than handled: it cannot be
pinned verbatim because it has no fixed text to type, and there is nothing in
this module's own corpus of callers for it to skip. Because every action
those nine families can emit is a literal, `harvest_static` — which walks
every branch regardless of which the fixtures exercise — finds everything
`harvest_behavioral` finds and often more (`static ⊇ behavioral`, verified
per family: equal where the fixtures exercise every branch, a proper
superset where they do not, e.g. tag-hygiene's twelve actions against seven
behaviorally-reached ones). `assert_actions_pinned`'s two-directional check
(`expected == behavioral | static`) does not depend on that relationship —
it would hold even if a family's static and behavioral sets were disjoint —
but the relationship is why static alone is sometimes enough: each family's
table test states, in its own docstring, which strings it pins BEHAVIOURALLY
and which STATICALLY.

The two-directional check
--------------------------

``assert_actions_pinned`` is `EXPECTED_ACTIONS == (behavioral | static)`,
both directions, on purpose: (1) nothing the source can emit is missing from
the table — the `#448` blind spot — and (2) nothing in the table is
unreachable dead weight the table could rot around. A failure names the
asymmetric difference in both directions so a maintainer sees, at a glance,
whether the SOURCE moved or the TABLE did.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

# The class every family ultimately constructs a finding through.
# `action` is its sixth field (severity, family, repo, path, rule, action,
# resolution=..., disposer=...) — see `scripts/doc_health/__init__.py`.
_FINDING_CALLEE_NAME = "Finding"


def _module_source(module_or_path) -> str:
    if isinstance(module_or_path, (str, Path)):
        return Path(module_or_path).read_text(encoding="utf-8")
    return inspect.getsource(module_or_path)


def _action_param_index(func_def: ast.FunctionDef) -> int | None:
    """Index of the parameter literally named `action` in a positional
    (posonly + regular) parameter list; `None` if `action` is absent from
    that list AND from the function's keyword-only parameters (not a
    parameter of this function at all).

    A keyword-only `action` (declared after a bare `*` in the signature) can
    never be filled positionally in a valid call, so it is given a sentinel
    index no real call's `node.args` can ever reach rather than a genuine
    positional slot. Registering it at all is the point: `harvest_static`
    only recognizes a callee as an action-taker when this function returns
    non-`None`, and a keyword-only `action` previously fell through that
    check entirely — even a call site passing `action=...` by keyword would
    have gone unmatched, because the callee was never added to
    `action_takers` in the first place. The keyword-matching pass at the
    call site is what actually resolves such a value; this index exists only
    to get the callee registered.
    """
    positional = list(func_def.args.posonlyargs) + list(func_def.args.args)
    for i, arg in enumerate(positional):
        if arg.arg == "action":
            return i
    for arg in func_def.args.kwonlyargs:
        if arg.arg == "action":
            return 1 << 30   # unreachable via `node.args[idx]`; see above
    return None


def harvest_static(module_or_path, *, functions: frozenset[str] | None = None
                   ) -> frozenset[str]:
    """Every string literal this module's source binds to an `action`
    parameter, statically. See the module docstring for the two call shapes
    recognized and the constant-resolution rule.

    `functions`, when given, scopes the walk to only those TOP-LEVEL `def`s
    (by name) — needed for a multi-family module like `families.py`, where
    an unscoped walk would mix every family's literals into one set. A
    top-level function's nested `def`s (e.g. `fam_tag_hygiene`'s local
    `hit`) and everything called only from within that function are still
    found, because scoping walks the MATCHED function's own subtree rather
    than filtering call sites after a flat walk. A single-family module
    (`ideation_routing.py`, `document_catalog.py`, `proposal_origin.py`,
    `release_inventory.py`) passes no `functions` and is walked whole.
    """
    source = _module_source(module_or_path)
    tree = ast.parse(source)

    # NAME -> literal string, so `action=_SOME_CONST` resolves to the
    # constant's TEXT rather than being dropped as "not a literal". `ast.walk`
    # here covers the WHOLE module tree, not just its top-level statements —
    # a constant is legitimately defined once at module level even when only
    # one scoped function uses it, so this cannot be limited to `functions`'
    # own subtree(s) the way the call-site walk below is. Walking the whole
    # tree also means it visits `Assign` nodes nested inside function and
    # class bodies, not only true module-level ones, and the loop keeps
    # overwriting the dict entry for each `NAME` it sees — so on a name
    # assigned more than once anywhere in the module, the LAST assignment
    # `ast.walk`'s traversal order reaches wins, not necessarily the
    # outermost or first one in source order.
    constants: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            value = node.value
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        constants[target.id] = value.value

    if functions is None:
        roots: list[ast.AST] = [tree]
    else:
        roots = [n for n in ast.iter_child_nodes(tree)
                 if isinstance(n, ast.FunctionDef) and n.name in functions]
        missing = functions - {n.name for n in roots}
        assert not missing, (
            f"harvest_static: no top-level def found for {sorted(missing)!r} "
            f"in {getattr(module_or_path, '__name__', module_or_path)}"
        )

    # callee name -> positional index of its `action` parameter, for every
    # module-local `def` reachable from the scoped root(s) (nested ones
    # included — the walk below descends into function bodies).
    action_takers: dict[str, int] = {}
    for root in roots:
        for node in ast.walk(root):
            if isinstance(node, ast.FunctionDef):
                idx = _action_param_index(node)
                if idx is not None:
                    action_takers[node.name] = idx
    # `Finding` itself is never `def`-ined in a check module (it is
    # imported), so it is seeded directly rather than discovered.
    action_takers.setdefault(_FINDING_CALLEE_NAME, 5)

    def literal_of(expr) -> str | None:
        if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
            return expr.value
        if isinstance(expr, ast.Name) and expr.id in constants:
            return constants[expr.id]
        return None

    found: set[str] = set()
    for root in roots:
        for node in ast.walk(root):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            else:
                continue
            if name not in action_takers:
                continue
            value = None
            for kw in node.keywords:
                if kw.arg == "action":
                    value = literal_of(kw.value)
                    break
            if value is None:
                idx = action_takers[name]
                if idx < len(node.args):
                    value = literal_of(node.args[idx])
            if value is not None:
                found.add(value)
    return frozenset(found)


def harvest_behavioral(family_fn, ctx) -> frozenset[str]:
    """Run `family_fn(ctx)` and collect every `.action` its findings carry.

    A `Skip` (or any non-list return) collects nothing — the same "no
    measurement taken, no tally" rule `report.render` applies to a skipped
    family elsewhere in this corpus; a skip is not a zero."""
    result = family_fn(ctx)
    if not isinstance(result, list):
        return frozenset()
    return frozenset(f.action for f in result)


def assert_actions_pinned(expected, behavioral, static, *, family: str) -> None:
    """The two-directional pin check every family table test makes.

    `behavioral | static` is everything this derivation shows the family CAN
    emit. `expected` must equal it exactly:

      1. nothing STATICALLY PRESENT OR BEHAVIORALLY EMITTED is missing from
         `expected` (the un-pinned-drift gap `#448` measured — mutating an
         action string nothing pins reds zero tests); and
      2. nothing in `expected` is neither statically present nor behaviorally
         emitted (a table entry the source no longer has any trace of — dead
         weight the table could rot around).

    "Statically present" is not "live": `harvest_static` proves only that a
    literal reaches an `action` parameter syntactically, and an `ast.walk`
    descends into a branch whether or not anything can ever take it. Two of
    `ideation-routing`'s pinned strings (`ideation_routing.py:315`, `:319`)
    are exactly this — `_shape_findings`'s only caller filters every record
    to `isinstance(data, dict) and data.get("kind") == RECORD_KIND` before
    calling it, so `_shape_findings`'s own `isinstance`/`kind` guards can
    never fire — and this check still counts them as covered, on the
    static half, because static presence is what it verifies. It does not,
    and cannot, verify liveness.

    Raises via a plain `assert` so pytest's own introspection renders the
    set diff; the message additionally states which literal is on which
    side, since pytest's default set diff does not sort by which direction
    it broke.
    """
    reachable = behavioral | static
    missing = reachable - expected   # emitted but not pinned
    dead = expected - reachable      # pinned but not reachable
    assert not missing and not dead, (
        f"{family}: EXPECTED_ACTIONS is out of sync with what the family "
        f"can emit ({len(behavioral)} behavioral, {len(static)} static, "
        f"{len(reachable)} reachable, {len(expected)} pinned).\n"
        f"  emitted but NOT pinned: {sorted(missing)!r}\n"
        f"  pinned but NOT reachable: {sorted(dead)!r}"
    )
