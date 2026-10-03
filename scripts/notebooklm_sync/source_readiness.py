from __future__ import annotations

from .models import OversizedSourceUploadError
from .source_context import SourceContext


def _title_holds(ctx: SourceContext, handle: str, source_id: str, title: str) -> bool:
    return any(
        str(r.source_id or "") == source_id and str(r.title or "") == title
        for r in ctx.list_sources(handle)
    )


def _observed_title(ctx: SourceContext, handle: str, source_id: str) -> str:
    try:
        for row in ctx.list_sources(handle):
            if str(row.source_id or "") == source_id:
                return str(row.title or "")
    except RuntimeError:
        return ""
    return ""


def _verify_rename_settled(
    ctx: SourceContext, handle: str, source_id: str, title: str
) -> None:
    ctx.sleep(ctx.settle_delay)
    observed = _observed_title(ctx, handle, source_id)
    if observed == title:
        print(f"    settle re-verify: title held ({ctx.settle_delay}s)")
        return
    print(
        f"    settle re-verify: title REGRESSED to {observed or '(unlisted)'!r} after {ctx.settle_delay}s — re-renaming once"
    )
    try:
        _ = ctx.run_text("source", "rename", source_id, title, "--notebook", handle)
    except RuntimeError as exc:
        print(f"    re-rename errored: {str(exc)[:160]}")
    ctx.sleep(ctx.settle_delay)
    settled = _observed_title(ctx, handle, source_id)
    if settled == title:
        print(
            f"    settle re-verify: title held after one re-rename ({ctx.settle_delay}s)"
        )
        return
    raise OversizedSourceUploadError(
        f"oversized source {title!r} ({source_id}) was renamed and verified, then REGRESSED to {settled or '(unlisted)'!r} within {ctx.settle_delay}s — twice, the second time after a re-rename (issue #462: the provider appears to re-stamp the title when ingestion of a large body completes). It is live under its temp filename. Wait until the source is fully ingested, then rename it by hand with `nlm source rename {source_id} {title!r} --notebook {handle}`, verify the title is STILL present a minute later, and re-plan — do NOT re-run the sync to fix it"
    )


def rename_source_when_ready(
    ctx: SourceContext, handle: str, source_id: str, title: str
) -> None:
    max_attempts = max(1, ctx.ready_timeout // ctx.poll_interval)
    deadline = ctx.monotonic() + ctx.ready_timeout
    attempts = 0
    last = ""
    while True:
        attempts += 1
        try:
            _ = ctx.run_text("source", "rename", source_id, title, "--notebook", handle)
        except RuntimeError as exc:
            last = str(exc)[:200]
        confirmed = False
        try:
            confirmed = _title_holds(ctx, handle, source_id, title)
        except RuntimeError as exc:
            last = f"source list unreadable: {str(exc)[:160]}"
        if confirmed:
            print(f"    renamed on attempt {attempts}")
            _verify_rename_settled(ctx, handle, source_id, title)
            return
        if attempts >= max_attempts or ctx.monotonic() >= deadline:
            raise OversizedSourceUploadError(
                f"oversized source {title!r} uploaded as {source_id} but the rename never took after {attempts} attempts over {ctx.ready_timeout}s (last: {last or 'no error reported'}). It is live under its temp filename; rename it by hand with `nlm source rename {source_id} {title!r} --notebook {handle}` — do NOT re-run the sync to fix it"
            )
        ctx.sleep(ctx.poll_interval)
