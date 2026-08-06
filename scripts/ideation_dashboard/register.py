"""Read-through adapters for the generator's two workspace inputs (plan
"register.py"):

  * the ideation CROSS-REFERENCE index (`ideation/cross-reference.yaml`, kind
    `ideation-cross-reference`) — the LANDED source of truth
    (`add-ideation-cross-reference-readiness`). It carries `topic_entries` (one
    per topic cluster, each with a human `name`, its three-tier `readiness`
    panel, and optional `conflict_flags`) AND the consolidated possibles register
    embedded as the top-level `possibles_register` section; and
  * the PROJECT register — the workspace-owned repository -> project ->
    project-group hierarchy (D10).

Both are consumed READ-ONLY; neither schema is restated here (the pinned
openxFactory validator owns conformance). The adapters only LOCATE and READ; the
generator does id resolution and projection.

REGISTER SEAM CLOSED. The possibles register's embedding field name was once
provisional (a reconciliation seam pending the index's realization). The index
IS now realized and the schema fixed the field name as `possibles_register`
(`ideation-cross-reference.schema.yaml` -> `#/$defs/possibles_register`), so the
seam is closed: the field is read directly. A cross-reference index with NO
`possibles_register` section is the documented BOOTSTRAP state — an empty
register, never an error — exactly what the landed `ideation/cross-reference.yaml`
carries until the register pass folds possibles in.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Top-level fields of the landed `ideation-cross-reference` index the adapter
# reads. `possibles_register` is the realized embedding field name (seam closed);
# a missing section is the bootstrap state (an empty register, not an error).
TOPIC_ENTRIES_KEY = "topic_entries"
POSSIBLES_REGISTER_KEY = "possibles_register"

# Candidate cross-reference index locations under a repo root, in preference
# order (the index is the structured YAML source of truth; the sibling
# `cross-reference.md` is its generated projection and is never read here).
CROSS_REFERENCE_SOURCE_CANDIDATES = (
    "ideation/cross-reference.yaml",
    "ideation/cross-reference.yml",
)
PROJECT_SOURCE_CANDIDATES = (
    "project-register.yaml",
    "project-register.yml",
)


def _load_yaml(source: Path | None) -> Any:
    if source is None or not Path(source).is_file():
        return None
    with Path(source).open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _first_existing(root: Path, candidates) -> Path | None:
    for rel in candidates:
        candidate = Path(root) / rel
        if candidate.is_file():
            return candidate
    return None


def _dict_items(section: Any) -> list[dict]:
    """The dict items of a YAML list section, or [] for anything else — a missing
    or malformed section is tolerated read-side (the pinned validator, not this
    adapter, is where a malformed section is an error)."""
    if not isinstance(section, list):
        return []
    return [item for item in section if isinstance(item, dict)]


class CrossReferenceIndexAdapter:
    """Reads the landed `ideation-cross-reference` index read-through: its topic
    entries (cluster names + verbatim readiness / conflict flags) and its embedded
    possibles register. A missing source, an index with no `possibles_register`
    section (the bootstrap state), or a bare register list all yield an empty
    register — never fabricated history."""

    def __init__(self, source: Path | None = None) -> None:
        self.source = Path(source) if source is not None else None

    @classmethod
    def discover(cls, repo_root: Path) -> "CrossReferenceIndexAdapter":
        return cls(_first_existing(repo_root, CROSS_REFERENCE_SOURCE_CANDIDATES))

    def _doc(self) -> Any:
        return _load_yaml(self.source)

    def topic_entries(self) -> list[dict]:
        """The index's topic-cluster entries in authored order. Read-through: no
        validation, no id resolution. An absent `topic_entries` (a bare register
        section or a missing index) yields []."""
        doc = self._doc()
        if isinstance(doc, dict):
            return _dict_items(doc.get(TOPIC_ENTRIES_KEY))
        return []

    def topic_entry_by_id(self) -> dict[str, dict]:
        """Topic entries keyed by their stable cluster `id` — the join a snapshot
        cluster uses to copy its display name and readiness/conflict flags."""
        return {e["id"]: e for e in self.topic_entries() if isinstance(e.get("id"), str)}

    def possibles(self) -> list[dict]:
        """The embedded possibles-register entries in authored order (the
        generator sorts by id). A missing `possibles_register` section is the
        documented bootstrap state -> [] (NOT an error); a bare register list
        with no index envelope is also tolerated."""
        doc = self._doc()
        if isinstance(doc, dict):
            return _dict_items(doc.get(POSSIBLES_REGISTER_KEY))
        if isinstance(doc, list):
            return _dict_items(doc)
        return []

    def possibles_by_id(self) -> dict[str, dict]:
        return {e["id"]: e for e in self.possibles() if "id" in e}


class ProjectRegisterAdapter:
    """Resolves a repository through the project register into
    (project_id, project_group_id). A repository absent from the register
    resolves to (None, None): the generator renders it ungrouped as its own
    implicit project (D10; spec 'A repository is absent from the register')."""

    def __init__(self, source: Path | None = None) -> None:
        self.source = Path(source) if source is not None else None

    @classmethod
    def discover(cls, root: Path) -> "ProjectRegisterAdapter":
        return cls(_first_existing(root, PROJECT_SOURCE_CANDIDATES))

    def _data(self) -> dict:
        doc = _load_yaml(self.source)
        return doc if isinstance(doc, dict) else {}

    def projects(self) -> list[dict]:
        return [p for p in (self._data().get("projects") or []) if isinstance(p, dict)]

    def project_groups(self) -> list[dict]:
        return [g for g in (self._data().get("project_groups") or []) if isinstance(g, dict)]

    def _repo_to_project(self) -> dict[str, str]:
        """First-wins PRIMARY map. Repository membership is MULTI-PARENT
        (Brett's 2026-08-06 ruling on add-project-scoped-selection): the
        first project in register order declaring a repository is its
        primary — the one the snapshot's singular `project` field carries —
        and `projects_of` returns full membership."""
        out: dict[str, str] = {}
        for project in self.projects():
            pid = project.get("id")
            if pid is None:
                continue
            for repo in project.get("repositories") or []:
                out.setdefault(repo, pid)
        return out

    def projects_of(self, repository: str) -> list[str]:
        """EVERY project declaring `repository`, in register order — the
        snapshot's additive `projects` list; its first element is the
        primary `resolve` returns."""
        return [project["id"] for project in self.projects()
                if project.get("id") is not None
                and repository in (project.get("repositories") or [])]

    def _project_to_group(self) -> dict[str, str]:
        out: dict[str, str] = {}
        for group in self.project_groups():
            gid = group.get("id")
            if gid is None:
                continue
            for member in group.get("projects") or []:
                out.setdefault(member, gid)
        return out

    def resolve(self, repository: str) -> tuple[str | None, str | None]:
        project = self._repo_to_project().get(repository)
        if project is None:
            return None, None
        group = self._project_to_group().get(project)
        return project, group
