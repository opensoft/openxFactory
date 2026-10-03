from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final, TypedDict


class StaticBookConfig(TypedDict):
    alias: str
    title: str
    statuses: set[str]


STATIC_BOOKS: Final[dict[str, StaticBookConfig]] = {
    "drafts": {
        "alias": "xf-drafts",
        "title": "xFactory — Working Drafts",
        "statuses": {"draft"},
    },
    "canon": {
        "alias": "xf-canon",
        "title": "xFactory — Canon",
        "statuses": {"ratified", "standard"},
    },
}
BOOKS = STATIC_BOOKS
IDEATION_STATUSES: Final = {"brainstorm", "staged"}
IDEATION_KEY_PREFIX = "ideation-"
IDEATION_ALIAS_PREFIX = "xf-ideation-"
IDEATION_TITLE_PREFIX = "xFactory Ideation — "
NOTEBOOK_SOURCE_CAP = 300
MAX_TEXT_ARG_BYTES = 100_000
SOURCE_ID_ECHO_RE = re.compile(r"Source ID:\s*(\S+)")
CAP_WARN_HEADROOM = 30
GROUNDING = [
    "openxFactory/docs/document-lifecycle.md",
    "openxFactory/docs/terminology-and-repo-topology.md",
    "openxFactory/docs/architecture.md",
]
CHARTER_TITLE = "00 [charter] Read me first"
HYBRID_CHARTER_TITLE = "00 [hybrid charter] Read me first"
CHARTER = """This notebook is a derived projection of the xFactory governance
document lifecycle (see source: [grounding] openxFactory: document-lifecycle).
It is maintained by scripts/sync-notebooklm-books.py in openxFactory; do not
hand-curate sources — membership follows each document's Status header.

Title prefixes declare epistemic weight:
  [brainstorm] non-normative ideas; may contradict the running system freely
  [staged]     organized fragments heading toward an OpenSpec proposal
  [draft]      normative intent, not yet ratified
  [ratified]   backed by an approved OpenSpec change
  [standard]   promoted canon — the running system's authority
  [spec]       promoted OpenSpec capability spec — the running system's authority
  [grounding]  context docs duplicated into every book

Per xFactory policy (openxFactory/docs/notebooklm-source-workspaces.md), all
output of this notebook is L1 notebook synthesis: it may raise claims but
never decides policy, memory, or workflow. Ideas here sit ON TOP OF a running
system; only [standard]/[spec] sources describe that system authoritatively."""
CHAT_PROMPT = (
    "Sources titled [brainstorm] or [staged] are non-normative ideas layered "
    "on top of a running system. Sources titled [standard], [spec], or "
    "[ratified] describe the system as governed today; [draft] is intended "
    "but unratified. Never present an idea as current behavior. In every "
    "answer, state whether each claim comes from the running system or from "
    "a proposal, and describe conflicts as 'proposed change from current', "
    "not as fact."
)
STATUS_RE = re.compile(
    r"^Status: (brainstorm|staged|draft|ratified|standard|superseded|retired|record|projection)\s*$",
    re.MULTILINE,
)
SKIP_PARTS = {".git", "node_modules", "installs", "__pycache__", "tests"}
EXPORT_RE = re.compile(r"^\[export:(brainstorm|staged)\]\s+(.+?)\s*$")
SOURCE_ID_RE = re.compile(r"^NotebookLM source id:\s*(\S+)\s*$", re.MULTILINE)
MANAGED_SOURCE_PREFIXES = (
    "[brainstorm]",
    "[staged]",
    "[draft]",
    "[ratified]",
    "[standard]",
    "[spec]",
    "[grounding]",
)
SESSION_CONTAINER_SUFFIX = "-worktrees"
SESSION_ALIAS_PREFIX = "xf-session-"
SESSION_LIVE = "live"
SESSION_DEAD = "dead"
SESSION_FOREIGN = "out-of-scope"
HOSTING_REL = "openxFactory/examples/notebook-projection-hosting.yaml"
HOSTING_SCALARS = ("case", "account", "account_type", "domain", "nlm_profile")
HOSTING_MIGRATION_SCALARS = ("state", "from_account", "from_nlm_profile")


class OversizedSourceUploadError(RuntimeError):
    pass


class SessionNotebookRefused(SystemExit):
    pass


class SessionSweepRefused(RuntimeError):
    pass


class ImportPathError(ValueError):
    pass


class NotebookLifecycleError(RuntimeError):
    pass


class NlmPayloadError(TypeError):
    pass


class NlmConfigurationError(ValueError):
    pass


class NlmCommandError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class BookSpec:
    key: str
    alias: str
    title: str


@dataclass(frozen=True, slots=True)
class ExportTarget:
    status: str
    repo: str
    topic: str
    title: str
    source_title: str


@dataclass(frozen=True, slots=True)
class ExportPlan:
    source_id: str
    source_title: str
    status: str
    repo: str
    topic: str
    title: str
    path: Path
    already_imported: bool = False


@dataclass(frozen=True, slots=True)
class ImportTarget:
    status: str
    repo: str
    topic: str
    path: Path


@dataclass(frozen=True, slots=True)
class SessionTarget:
    repository: str
    branch: str
    worktree: Path
    alias: str
    checkout: Path | None = None


@dataclass(frozen=True, slots=True)
class SessionSync:
    target: SessionTarget
    documents: tuple[str, ...] = ()
    applied: bool = False
    retired: bool = False
    skipped: bool = False
    detail: str = ""

    @property
    def alias(self) -> str:
        return self.target.alias

    @property
    def repository(self) -> str:
        return self.target.repository

    @property
    def branch(self) -> str:
        return self.target.branch

    @property
    def worktree(self) -> Path:
        return self.target.worktree


def ideation_spec(repo: str) -> BookSpec:
    slug = repo.lower()
    return BookSpec(
        key=f"{IDEATION_KEY_PREFIX}{slug}",
        alias=f"{IDEATION_ALIAS_PREFIX}{slug}",
        title=f"{IDEATION_TITLE_PREFIX}{repo}",
    )


def static_spec(book: str) -> BookSpec:
    config = STATIC_BOOKS[book]
    return BookSpec(key=book, alias=config["alias"], title=config["title"])


ROOT_LEVEL_GOVERNED_PRODUCTS = ("openAvatar", "openXwallet")
PROJECTED_STATUSES = frozenset(
    {"brainstorm", "staged", "draft", "ratified", "standard"}
)
