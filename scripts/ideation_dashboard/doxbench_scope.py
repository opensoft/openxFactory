"""Independent doxBench scope and ownership authority.

The browser projection is useful presentation state; it is never authorization.
This module derives the same ordered sections from the selected snapshot, then
independently confines every backed path to the selected registry root and
classifies editable material. Only a staged tile's resolved folder documents
and explicitly recorded session-created documents are editable.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

# THE FIVE FROZEN SCOPE TYPES, and their validation tuple, RE-IMPORTED from the
# column module they moved to (`split-opendox-two-layer-product` § 3.1, pre-carve
# split S-1). They are openDox value types; everything below is the openXdox
# OWNERSHIP AUTHORITY that produces them, and § 3.1's manifest cannot file one
# path under two columns. The names below are the SAME OBJECTS as
# `doxbench_scope_types`' — not copies — so `isinstance` checks,
# `except ScopeConfinementError` handlers and `ScopeKey` equality behave
# identically whichever path a caller imports by, and every landed
# `from ideation_dashboard.doxbench_scope import ScopeKey` still resolves.
from ideation_dashboard.doxbench_scope_types import (  # noqa: F401  (re-export)
    SCOPE_KINDS,
    ScopeConfinementError,
    ScopeDocument,
    ScopeKey,
    ScopeProjection,
    ScopeSection,
)

_SERVED_DOTFILE_SUFFIXES = frozenset({".yaml", ".yml", ".md", ".json"})

_SECTION_META = {
    "members": {
        "label": "cluster documents",
        "note": "the cluster's own snapshot document edges",
    },
    "cited": {
        "label": "cited supporting evidence",
        "note": "recorded evidence pins — a governed citation",
    },
    "inherited": {
        "label": "inherited from claiming clusters",
        "note": (
            "membership INFERRED from the claiming clusters — not cited evidence"
        ),
        "inherited": True,
    },
    "folder": {
        "label": "topic folder documents",
        "note": (
            "the corpus documents that live in this staging folder — "
            "the topic's own material"
        ),
        "owned": True,
    },
    "declaring": {
        "label": "documents declaring this topic",
        "note": (
            "documents whose declared destinations name this staging topic — "
            "inbound context"
        ),
    },
    "neighbourhood": {
        "label": "cluster neighbourhood",
        "note": (
            "member documents of the topic's linked clusters — inferred via "
            "clusters, not the topic's own material"
        ),
        "inherited": True,
    },
}


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sequence(value: Any) -> Sequence[Any]:
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        return value
    return ()


def _as_id(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _unique_strings(values: Iterable[Any]) -> tuple[str, ...]:
    output: list[str] = []
    seen: set[str] = set()
    for raw in values:
        value = _as_id(raw)
        if not value or value in seen:
            continue
        seen.add(value)
        output.append(value)
    return tuple(output)


def _confined_path(path: str, source_root: Path) -> str:
    if not isinstance(path, str) or not path or "\x00" in path or "\\" in path:
        raise ScopeConfinementError(
            "scope paths must be non-empty repo-relative POSIX paths"
        )
    relative = Path(path)
    if relative.is_absolute():
        raise ScopeConfinementError(
            f"scope path {path!r} must be repo-relative"
        )

    parts = PurePosixPath(path).parts
    if any(part.startswith(".") and part != ".." for part in parts[:-1]):
        raise ScopeConfinementError(
            f"scope path {path!r} enters a forbidden dot-directory"
        )
    if parts and parts[-1].startswith(".") and parts[-1] != "..":
        if PurePosixPath(parts[-1]).suffix not in _SERVED_DOTFILE_SUFFIXES:
            raise ScopeConfinementError(
                f"scope path {path!r} names a forbidden dot-file"
            )

    try:
        root = source_root.resolve()
        candidate = (root / relative).resolve()
    except (OSError, RuntimeError, ValueError) as error:
        raise ScopeConfinementError(
            f"scope path {path!r} cannot be safely resolved"
        ) from error
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ScopeConfinementError(
            f"scope path {path!r} resolves outside the selected root"
        ) from error

    canonical = relative.as_posix()
    if canonical != path or "." in relative.parts or ".." in relative.parts:
        raise ScopeConfinementError(
            f"scope path {path!r} must use canonical repo-relative spelling"
        )
    return path


def primary_fragment_path(
    staging_id: str,
    files: Iterable[Any],
) -> str | None:
    """Mirror the existing wheel's deterministic declared-fragment rule."""

    markdown = [
        value
        for value in (_as_id(raw) for raw in files)
        if value.lower().endswith(".md")
    ]
    if not markdown:
        return None
    wanted = (
        PurePosixPath(staging_id).name + ".md" if staging_id else ""
    ).lower()
    if wanted:
        for path in markdown:
            if PurePosixPath(path).name.lower() == wanted:
                return path
    best = markdown[0]
    best_depth = len(best.split("/"))
    for path in markdown[1:]:
        depth = len(path.split("/"))
        if depth < best_depth:
            best = path
            best_depth = depth
    return best


def _document_index(snapshot: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    output: dict[str, Mapping[str, Any]] = {}
    for raw in _sequence(snapshot.get("documents")):
        document = _mapping(raw)
        for value in (_as_id(document.get("id")), _as_id(document.get("path"))):
            if value and value not in output:
                output[value] = document
    return output


def _build_section(
    key: str,
    references: Iterable[Any],
    *,
    by_id: Mapping[str, Mapping[str, Any]],
    seen: set[str],
    source_root: Path,
    require_resolved: bool = False,
) -> ScopeSection:
    meta = _SECTION_META[key]
    documents: list[ScopeDocument] = []
    for raw in references:
        document_id = _as_id(raw)
        if not document_id or document_id in seen:
            continue
        document = by_id.get(document_id)
        if require_resolved and document is None:
            continue
        seen.add(document_id)
        if document is None:
            documents.append(
                ScopeDocument(
                    id=document_id,
                    path=document_id,
                    resolved=False,
                )
            )
            continue
        path = _as_id(document.get("path")) or document_id
        documents.append(
            ScopeDocument(
                id=document_id,
                path=_confined_path(path, source_root),
                resolved=True,
            )
        )
    return ScopeSection(
        key=key,
        label=meta["label"],
        note=meta["note"],
        inherited=bool(meta.get("inherited")),
        owned=bool(meta.get("owned")),
        documents=tuple(documents),
    )


def _staged_outline(
    topic: Mapping[str, Any] | None,
) -> tuple[str, tuple[Any, ...]] | None:
    if not topic:
        return None
    return (
        _as_id(topic.get("staging_id")),
        tuple(_sequence(topic.get("files"))),
    )


def _picked_outline(
    snapshot: Mapping[str, Any],
    possible: Mapping[str, Any],
) -> tuple[str, tuple[Any, ...]] | None:
    staging_id = _as_id(_mapping(possible.get("pick")).get("staging_id"))
    if not staging_id:
        return None
    for raw in _sequence(snapshot.get("staged_topics")):
        topic = _mapping(raw)
        if _as_id(topic.get("staging_id")) == staging_id:
            return _staged_outline(topic)
    return None


def _projection(
    *,
    snapshot: Mapping[str, Any],
    key: ScopeKey,
    title: str,
    keywords: Iterable[Any],
    sections: Iterable[ScopeSection],
    outline: tuple[str, tuple[Any, ...]] | None,
    created_paths: Iterable[str],
    source_root: Path,
) -> ScopeProjection:
    ordered_sections = tuple(sections)
    context_paths: list[str] = []
    editable_paths: list[str] = []
    context_seen: set[str] = set()
    editable_seen: set[str] = set()

    for section in ordered_sections:
        for row in section.documents:
            if not row.resolved:
                continue
            if row.path not in context_seen:
                context_seen.add(row.path)
                context_paths.append(row.path)
            if section.owned and row.path not in editable_seen:
                editable_seen.add(row.path)
                editable_paths.append(row.path)

    # FR-043 (clarification 2026-07-30): a session-created document enters BOTH
    # sets. It used to enter `editable_paths` only, which read as generous and was
    # in fact the opposite: the FR-015 turn guard requires a path to be in
    # `context_paths` AND `editable_paths`, so an editable-only path was editable
    # by nobody -- a document the human had just created on a cluster or possible
    # tile could never be the subject of a turn. The guard is UNCHANGED; the set
    # that was wrong is fixed. Appended AFTER the sections in both lists so the
    # tile's own material keeps its order and position, and so a created path that
    # the snapshot HAS caught up with is deduped against its section row rather
    # than listed twice.
    for raw in created_paths:
        path = _confined_path(raw, source_root)
        if path not in context_seen:
            context_seen.add(path)
            context_paths.append(path)
        if path not in editable_seen:
            editable_seen.add(path)
            editable_paths.append(path)

    outline_path = None
    if outline is not None:
        staging_id, files = outline
        selected = primary_fragment_path(staging_id, files)
        if selected:
            outline_path = _confined_path(selected, source_root)

    # T104 F2: an outline this tile's own scope does not contain is not this
    # tile's outline. The outline buffer rides EVERY turn (build_prompt_envelope
    # passes `projection.outline_path` itself into the FR-015 guard), and that
    # guard requires a non-None outline path to be BOTH in-scope and editable --
    # disclosure requires edit authority, which is the rule, not an accident.
    # A published outline that fails it therefore kills the tile's chat outright,
    # whatever document is active.
    #
    # The case that bites is a PICKED possible: `_picked_outline` resolves the
    # PICKED TOPIC's fragment, which lives in another tile's staged folder and
    # is in neither of this tile's sets. Declaring it editable here is not
    # available as a fix -- a possible tile owns no folder
    # (`gate_routes.tile_owned_prefix` returns None for it), so the Save path
    # refuses that very path, and a scope authority that granted what the Save
    # authority denies would be the drift both are written to prevent. It is
    # withheld instead, which is the posture every OTHER cluster/possible tile
    # already has (`outline=None`), and the tile keeps a working chat rail.
    if outline_path is not None and not (
            outline_path in editable_seen and outline_path in context_seen):
        outline_path = None

    # THE CANDIDATES ARE WHAT THE TURN GUARD WOULD ACCEPT (T104 F2). This used
    # to be `context_paths` verbatim -- every readable document -- while
    # `doxbench_turns._require_in_scope_and_editable` requires membership in
    # BOTH sets, so a cluster or possible tile advertised a full picker whose
    # every entry refused, and a staged tile advertised its inherited and
    # neighbourhood material the same way. The guard is UNCHANGED; the set that
    # was wrong is fixed (the same correction FR-043 made above).
    #
    # The outline path is excluded on top of that: offering it as the active
    # DOCUMENT gives the operator two independent working copies of one file,
    # which the Save planner then plans as two gate actions for one document --
    # the second refused forever on a base the first just moved.
    candidates = tuple(
        path for path in context_paths
        if path in editable_seen and path != outline_path
    )

    source_revision = _as_id(
        _mapping(snapshot.get("generation")).get("source_revision")
    )
    return ScopeProjection(
        key=key,
        title=title,
        keywords=_unique_strings(keywords),
        source_revision=source_revision,
        sections=ordered_sections,
        context_paths=tuple(context_paths),
        editable_paths=tuple(editable_paths),
        outline_path=outline_path,
        active_document_candidates=candidates,
    )


def resolve_scope(
    snapshot: Mapping[str, Any],
    key: ScopeKey,
    *,
    source_root: Path,
    created_paths: Iterable[str] = (),
) -> ScopeProjection | None:
    """Resolve one tile from snapshot truth and independently classify paths."""

    if not isinstance(snapshot, Mapping):
        return None
    if isinstance(created_paths, (str, bytes, bytearray)):
        raise ScopeConfinementError(
            "created_paths must be a collection of repo-relative path strings"
        )
    try:
        created = tuple(created_paths)
    except TypeError as error:
        raise ScopeConfinementError(
            "created_paths must be a collection of repo-relative path strings"
        ) from error
    if any(not isinstance(path, str) for path in created):
        raise ScopeConfinementError(
            "created_paths must contain only repo-relative path strings"
        )
    root = Path(source_root)
    by_id = _document_index(snapshot)
    seen: set[str] = set()

    if key.tile_kind == "cluster":
        cluster = next(
            (
                _mapping(raw)
                for raw in _sequence(snapshot.get("clusters"))
                if _as_id(_mapping(raw).get("id")) == key.tile_id
            ),
            None,
        )
        if cluster is None:
            return None
        members = _build_section(
            "members",
            (
                _mapping(edge).get("document")
                for edge in _sequence(cluster.get("document_edges"))
            ),
            by_id=by_id,
            seen=seen,
            source_root=root,
        )
        return _projection(
            snapshot=snapshot,
            key=key,
            title=_as_id(cluster.get("name")) or key.tile_id,
            keywords=_sequence(cluster.get("topics")),
            sections=(members,),
            outline=None,
            created_paths=created,
            source_root=root,
        )

    if key.tile_kind == "possible":
        possible = next(
            (
                _mapping(raw)
                for raw in _sequence(snapshot.get("possibles"))
                if _as_id(_mapping(raw).get("id")) == key.tile_id
            ),
            None,
        )
        if possible is None:
            return None
        cited = _build_section(
            "cited",
            (
                _mapping(evidence).get("document")
                for evidence in _sequence(possible.get("supporting_evidence"))
            ),
            by_id=by_id,
            seen=seen,
            source_root=root,
        )
        cluster_by_id = {
            _as_id(_mapping(raw).get("id")): _mapping(raw)
            for raw in _sequence(snapshot.get("clusters"))
            if _as_id(_mapping(raw).get("id"))
        }
        inherited_references: list[Any] = []
        inherited_keywords: list[Any] = []
        for cluster_id in (
            _as_id(raw)
            for raw in _sequence(possible.get("claiming_clusters"))
        ):
            cluster = cluster_by_id.get(cluster_id)
            if cluster is None:
                continue
            inherited_references.extend(
                _mapping(edge).get("document")
                for edge in _sequence(cluster.get("document_edges"))
            )
            inherited_keywords.extend(_sequence(cluster.get("topics")))
        inherited = _build_section(
            "inherited",
            inherited_references,
            by_id=by_id,
            seen=seen,
            source_root=root,
        )
        return _projection(
            snapshot=snapshot,
            key=key,
            title=_as_id(possible.get("title")) or key.tile_id,
            keywords=inherited_keywords,
            sections=(cited, inherited),
            outline=_picked_outline(snapshot, possible),
            created_paths=created,
            source_root=root,
        )

    topic = next(
        (
            _mapping(raw)
            for raw in _sequence(snapshot.get("staged_topics"))
            if _as_id(_mapping(raw).get("staging_id")) == key.tile_id
        ),
        None,
    )
    if topic is None:
        return None
    folder = _build_section(
        "folder",
        _sequence(topic.get("files")),
        by_id=by_id,
        seen=seen,
        source_root=root,
        require_resolved=True,
    )
    declaring_references = [
        _as_id(document.get("id")) or _as_id(document.get("path"))
        for document in (
            _mapping(raw) for raw in _sequence(snapshot.get("documents"))
        )
        if key.tile_id
        in {
            _as_id(value)
            for value in _sequence(
                _mapping(document.get("destinations")).get("staged_topics")
            )
        }
    ]
    declaring = _build_section(
        "declaring",
        declaring_references,
        by_id=by_id,
        seen=seen,
        source_root=root,
    )
    keywords = [
        value
        for row in folder.documents
        for value in _sequence(by_id.get(row.id, {}).get("topics"))
    ]
    sections: list[ScopeSection] = [folder, declaring]
    linked_clusters = [
        cluster
        for cluster in (
            _mapping(raw) for raw in _sequence(snapshot.get("clusters"))
        )
        if key.tile_id
        in {
            _as_id(value)
            for value in _sequence(
                _mapping(cluster.get("lineage")).get("staged_picks")
            )
        }
    ]
    if linked_clusters:
        neighbour_references = [
            _mapping(edge).get("document")
            for cluster in linked_clusters
            for edge in _sequence(cluster.get("document_edges"))
        ]
        sections.append(
            _build_section(
                "neighbourhood",
                neighbour_references,
                by_id=by_id,
                seen=seen,
                source_root=root,
            )
        )
    return _projection(
        snapshot=snapshot,
        key=key,
        title=key.tile_id,
        keywords=keywords,
        sections=sections,
        outline=_staged_outline(topic),
        created_paths=created,
        source_root=root,
    )


# ==========================================================================
# THE CREATED-IN-SESSION RECORD (T107; FR-043, security-privacy CHK012)
#
# `resolve_scope` has always ACCEPTED `created_paths`, and until now the sole
# production caller -- the chat-turn route -- passed none, because the server had
# no created-in-session authority of its own. The browser has one
# (`swb-session.js createdDocuments`, a page-lifetime Map), and that is exactly
# the one a server must never read: it arrives as request content, so a request
# could name any path and have it treated as material this session created.
#
# So the authority is DERIVED, not accepted, and from a record the 007 branch
# sessions ALREADY write. A session `create-document` is one commit carrying two
# things (`gate_routes._create_document`): the new document, and its gate-action
# record naming that document (`target.document`) and the session branch
# (`target.ref`, which the route populates inside a session and nowhere else).
# Both land in the SESSION WORKTREE, which is the `source_root` of the session's
# own registry entry -- so the entry the route already resolved is the whole
# input, and no request field participates.
#
# Liveness is asked of the REGISTRY and only the registry (FR-008: a live entry
# IS the session; neither a branch nor a worktree proves it, D15), and the branch
# must be a member of THIS TILE's own ordinal family (FR-002: a session branch is
# derived from the tile, never from the actor). With no live session for the
# scope the answer is `()` and the projection is byte-identical to the one this
# route produced before T107.
#
# Nothing here raises out into the route: a malformed, stale, or unsafe record is
# DROPPED. These records are server-held, and one bad file must not refuse every
# turn on a tile. A caller-supplied escape path is still a hard
# `ScopeConfinementError` from `resolve_scope` -- that contract is unchanged.
# ==========================================================================

_GATE_RECORD_SUFFIX = ".gate-action.yaml"


def created_paths_from_records(
    records: Iterable[Any],
    *,
    branch: str,
) -> tuple[str, ...]:
    """The documents `records` say were CREATED on `branch`, in input order.

    Pure: mappings in, deduped paths out. A record counts only when it is a
    `create-document` action whose target names BOTH this branch and a document
    -- an `edit-document` is not a create, another session's create is not this
    session's, and a main-resident pre-session create carries no `ref` at all.
    """

    from .gate_console import (  # lazy: keeps this module's import graph flat
        ACTION_CREATE_DOCUMENT,
    )

    if not branch:
        return ()
    output: list[str] = []
    seen: set[str] = set()
    for raw in records:
        record = _mapping(raw)
        if _as_id(record.get("action")) != ACTION_CREATE_DOCUMENT:
            continue
        target = _mapping(record.get("target"))
        if _as_id(target.get("ref")) != branch:
            continue
        path = _as_id(target.get("document"))
        if not path or path in seen:
            continue
        seen.add(path)
        output.append(path)
    return tuple(output)


def session_created_paths(
    worktree: Path | str,
    branch: str,
    *,
    records_dir: str | None = None,
) -> tuple[str, ...]:
    """Read the created-in-session record for `branch` out of its worktree.

    The thin I/O half of the derivation. The action name is part of the record's
    FILENAME (`gate_console.gate_action_record_relpath`), so the glob narrows to
    creates before anything is parsed, and the read is ordered by the action
    stamp in that filename -- creation order, deterministically.

    Every admitted path is confined to the worktree with the same
    `_confined_path` the snapshot's own paths go through, and must resolve to a
    file that is actually there: a path nobody can read is not chat-eligible.
    """

    import yaml  # lazy: keeps this module's import graph flat

    from .gate_console import (
        ACTION_CREATE_DOCUMENT,
        DEFAULT_RECORDS_DIR,
    )

    if not branch:
        return ()
    root = Path(worktree)
    records_root = root / (
        DEFAULT_RECORDS_DIR if records_dir is None else records_dir
    )
    if not records_root.is_dir():
        return ()
    pattern = f"*/{ACTION_CREATE_DOCUMENT}-*{_GATE_RECORD_SUFFIX}"
    try:
        found = sorted(records_root.glob(pattern), key=lambda p: (p.name, str(p)))
    except OSError:
        return ()
    records: list[Any] = []
    for record_path in found:
        try:
            records.append(
                yaml.safe_load(record_path.read_text(encoding="utf-8"))
            )
        except (OSError, UnicodeDecodeError, yaml.YAMLError):
            continue
    output: list[str] = []
    for path in created_paths_from_records(records, branch=branch):
        try:
            confined = _confined_path(path, root)
        except ScopeConfinementError:
            continue
        if (root / confined).is_file():
            output.append(confined)
    return tuple(output)


def is_live_session_ref(registry: Any, key: ScopeKey, *, repository: str,
                        ref: str) -> bool:
    """Whether ``ref`` is one of THIS tile's live session branches.

    ONE spelling of the question, extracted at the re-verify's N-6 because
    `serve.py` had grown a second one for the thread routes and the two had
    already diverged in two ways. Both callers now share this, so a change to
    what counts as a live session cannot land in one of them only.

    THE TWO DIVERGENCES, RESOLVED TOWARDS THE SAFER READING:

    * REF NORMALISATION. The thread copy compared refs through
      `snapshot_registry.normalize_ref`, this one compared raw strings.
      Normalisation wins — but note precisely what it buys, because the first
      version of this note overclaimed: `normalize_ref` trims whitespace and
      maps None/empty to the default ref; it does NOT strip `refs/heads/`, so a
      long-form ref is still a different string here. What it buys is that a ref
      arriving with stray whitespace, or absent, resolves the way every other
      registry consumer resolves it rather than silently failing to match.
    * EXCEPTION BREADTH. This one caught `SessionRefused`; the thread copy
      caught bare `Exception`. `SessionRefused` wins, and that is a JUDGEMENT
      CALL worth flagging: the narrow catch answers "not this tile's session"
      for the refusals the branch layer DECLARES (a cross-tile collision, an
      ambiguous family) and lets anything else — a registry that raises
      `AttributeError`, say — propagate to the caller's own handler rather than
      being silently reported as "no session". The thread route's caller wraps
      it, so nothing new reaches the wire; what changes is that a genuine defect
      stops being indistinguishable from an honest absence.
    """

    from . import branch_session  # lazy: keeps this module's import graph flat

    kinds = {
        "cluster": branch_session.CLUSTER,
        "possible": branch_session.POSSIBLE,
        "staged": branch_session.STAGED_TOPIC,
    }
    scope_kind = kinds.get(key.tile_kind)
    if scope_kind is None or not ref or registry is None:
        return False
    try:
        tile = branch_session.Tile(scope_kind, key.tile_id)
        live = branch_session.live_session_branches(registry, repository, tile)
    except branch_session.SessionRefused:
        # `CrossTileCollision` included: an ambiguous live branch is answered as
        # "not this tile's session" rather than as another tile's.
        return False
    from . import snapshot_registry as _registry
    wanted = _registry.normalize_ref(ref)
    return any(wanted == _registry.normalize_ref(branch) for branch in live)


def session_created_paths_for_scope(
    registry: Any,
    key: ScopeKey,
    *,
    repository: str,
    ref: str,
    source_root: Path | str,
) -> tuple[str, ...]:
    """The created-in-session paths for one scope, or `()` when none applies.

    `repository`/`ref`/`source_root` are the SERVER's own values -- the fields of
    the registry entry the caller already resolved -- and `key` contributes only
    the tile identity the branch family is derived from. Nothing a request can
    spell adds a path here.
    """

    if not is_live_session_ref(registry, key, repository=repository, ref=ref):
        return ()
    return session_created_paths(source_root, ref)
