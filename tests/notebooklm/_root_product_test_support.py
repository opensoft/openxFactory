from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from tests.notebooklm._sync_test_support import STAGED_DOC


def root_product_world(
    root: Path,
    *,
    products: Sequence[str] = ("openXwallet",),
    declare: Sequence[str] | None = None,
    initialize: bool = True,
    extra_pins: Sequence[str] = (),
) -> Path:
    """An aggregation root pinning `products` as ROOT-LEVEL siblings.

    `declare` overrides which names go into `.gitmodules` (default: `products`),
    so the tests can separate "pinned" from "present on disk" — the two halves
    `pinned_root_product_paths` requires jointly. `initialize=False` leaves the
    directory EMPTY, which is exactly what an uninitialized submodule looks
    like.
    """
    (root / "openxFactory" / "ideation" / "staging" / "demo-topic").mkdir(parents=True)
    _ = (root / "openxFactory" / STAGED_DOC).write_text(
        "Status: staged\n\n# openxFactory topic\n", encoding="utf-8"
    )
    lines: list[str] = []
    for name in declare if declare is not None else products:
        lines.append(
            f'[submodule "{name}"]\n\tpath = {name}\n\turl = https://example.invalid/{name}.git\n'
        )
    for pin in extra_pins:
        lines.append(
            f'[submodule "{pin}"]\n\tpath = {pin}\n\turl = https://example.invalid/{pin}.git\n'
        )
    _ = (root / ".gitmodules").write_text("".join(lines), encoding="utf-8")
    for name in products:
        base = root / name
        base.mkdir(parents=True, exist_ok=True)
        if initialize:
            (base / "ideation" / "brainstorm").mkdir(parents=True)
            _ = (base / "ideation" / "brainstorm" / "wallet-idea.md").write_text(
                "Status: brainstorm\n\n# a wallet idea\n", encoding="utf-8"
            )
    return root
