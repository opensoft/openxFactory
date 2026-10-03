from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

from .compat_errors import DashboardCompatibilityError
from .models import SessionTarget
from .session_sync import SessionDocumentsModule


@dataclass(frozen=True, slots=True)
class DashboardModules:
    workbench: Callable[[], ModuleType]
    session_git: Callable[[], ModuleType]
    branch_session: Callable[[], ModuleType]

    def __call__(self, name: str) -> ModuleType:
        if name == "workbench":
            return self.workbench()
        if name == "session_git":
            return self.session_git()
        if name == "branch_session":
            return self.branch_session()
        raise DashboardCompatibilityError(name)


def load_dashboard_module(name: str) -> ModuleType:
    scripts_dir = Path(__file__).resolve().parents[1]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from carved_reach import module as carved_module

    return carved_module(f"scripts/ideation_dashboard/{name}.py")


def load_session_documents(
    dashboard: Callable[[str], ModuleType], target: SessionTarget
) -> list[tuple[str, str]]:
    workbench = dashboard("workbench")
    if not isinstance(workbench, SessionDocumentsModule):
        raise DashboardCompatibilityError("session documents")
    return workbench.session_documents(target.worktree, repository=target.repository)
