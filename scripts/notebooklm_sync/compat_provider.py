from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Literal, overload

from . import nlm_client
from .nlm_client import NlmCliProvider, ProviderResult


class CompatProvider:
    """Preserve the wrapper's dynamically replaceable profile guard."""

    def __init__(self, *, assert_bound: Callable[[], None]) -> None:
        self.assert_bound: Callable[[], None] = assert_bound

    @overload
    def nlm(self, *args: str, parse: Literal[False]) -> str: ...

    @overload
    def nlm(self, *args: str, parse: Literal[True] = True) -> ProviderResult: ...

    def nlm(self, *args: str, parse: bool = True) -> ProviderResult:
        provider = NlmCliProvider(assert_bound=self.assert_bound)
        return provider.invoke(*args, parse=parse)


class ProfileFacade:
    """Read the wrapper's replaceable configuration path at each operation."""

    def __init__(self, config_path: Callable[[], Path]) -> None:
        self.config_path: Callable[[], Path] = config_path

    def path_override(self) -> Path | None:
        path = self.config_path()
        return None if path == nlm_client.NLM_CONFIG else path

    def assert_still_bound(self) -> None:
        nlm_client.assert_still_bound(self.path_override())

    def configured_nlm_profile(self, path: Path | None = None) -> str | None:
        return nlm_client.configured_nlm_profile(path or self.path_override())
