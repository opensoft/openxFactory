from __future__ import annotations

import os
import tempfile
from collections.abc import Callable

from .models import SOURCE_ID_ECHO_RE, OversizedSourceUploadError
from .nlm_client import SourceRow


def add_with_one_retry(
    args: tuple[str, ...],
    *,
    run_text: Callable[..., str],
    sleep: Callable[[float], None],
) -> str:
    try:
        return run_text(*args)
    except RuntimeError as exc:
        print(f"    retrying once after: {exc}")
        sleep(10)
        return run_text(*args)


def add_text_source(
    handle: str,
    text: str,
    title: str,
    *,
    run_text: Callable[..., str],
    sleep: Callable[[float], None],
    list_sources: Callable[[str], list[SourceRow]],
    max_text_arg_bytes: int,
) -> None:
    if len(text.encode("utf-8", "replace")) <= max_text_arg_bytes:
        _ = add_with_one_retry(
            ("source", "add", handle, "--text", text, "--title", title),
            run_text=run_text,
            sleep=sleep,
        )
        return
    descriptor, temporary = tempfile.mkstemp(suffix=".md", prefix="xf-sync-")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            _ = file.write(text)
        output = add_with_one_retry(
            ("source", "add", handle, "--file", temporary, "--wait"),
            run_text=run_text,
            sleep=sleep,
        )
        match = SOURCE_ID_ECHO_RE.search(output)
        if match is None:
            raise OversizedSourceUploadError(
                f"oversized source {title!r} uploaded but the CLI echoed no "
                + "source id to rename — rename it to the contract title by hand"
            )
        source_id = match.group(1)
        _ = run_text("source", "rename", source_id, title, "--notebook", handle)
        renamed = any(
            source.source_id == source_id and source.title == title
            for source in list_sources(handle)
        )
        if not renamed:
            raise OversizedSourceUploadError(
                f"oversized source {title!r} uploaded as {source_id}, but its "
                + "rename was not visible in the notebook source list"
            )
    finally:
        os.unlink(temporary)
