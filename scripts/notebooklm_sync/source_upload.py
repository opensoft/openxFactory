from __future__ import annotations

import os
import tempfile
from collections.abc import Callable

from .models import SOURCE_ID_ECHO_RE, OversizedSourceUploadError
from .source_adoption import adopt_matching_stray
from .source_context import SourceContext
from .source_readiness import rename_source_when_ready


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
    context: SourceContext,
    max_text_arg_bytes: int,
) -> None:
    if len(text.encode("utf-8", "replace")) <= max_text_arg_bytes:
        _ = add_with_one_retry(
            ("source", "add", handle, "--text", text, "--title", title),
            run_text=context.run_text,
            sleep=context.sleep,
        )
        return
    if adopt_matching_stray(context, handle, text, title):
        return
    descriptor, temporary = tempfile.mkstemp(suffix=".md", prefix="xf-sync-")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            _ = file.write(text)
        output = add_with_one_retry(
            ("source", "add", handle, "--file", temporary),
            run_text=context.run_text,
            sleep=context.sleep,
        )
        match = SOURCE_ID_ECHO_RE.search(output)
        if match is None:
            raise OversizedSourceUploadError(
                f"oversized source {title!r} uploaded but the CLI echoed no source id to rename — rename it to the contract title by hand"
            )
        source_id = match.group(1)
        print(
            f"    uploaded as {source_id} ({len(text.encode('utf-8', 'replace'))}B, as a temp file)"
        )
        rename_source_when_ready(context, handle, source_id, title)
    finally:
        os.unlink(temporary)
