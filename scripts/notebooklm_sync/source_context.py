from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .nlm_client import SourceRow


@dataclass(frozen=True, slots=True)
class SourceContext:
    run_text: Callable[..., str]
    list_sources: Callable[[str], list[SourceRow]]
    sleep: Callable[[float], None]
    monotonic: Callable[[], float]
    ready_timeout: int
    poll_interval: int
    settle_delay: int
    tolerance: int
