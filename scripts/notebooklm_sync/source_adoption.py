from __future__ import annotations

import re
from dataclasses import dataclass

from .import_execution import source_content_text
from .models import OversizedSourceUploadError
from .source_context import SourceContext
from .source_digests import content_digest, normalized_digest
from .source_readiness import rename_source_when_ready

STRAY_TEMP_TITLE_RE = re.compile(r"^xf-sync-[A-Za-z0-9_]+\.md$")


@dataclass(frozen=True, slots=True)
class _Stray:
    source_id: str
    title: str
    raw: str
    length: int


def _stray_uploads(ctx: SourceContext, handle: str) -> list[_Stray]:
    try:
        rows = ctx.list_sources(handle)
    except RuntimeError:
        return []
    strays: list[_Stray] = []
    for row in rows:
        row_title = str(row.title or "")
        source_id = row.source_id
        if not source_id or not STRAY_TEMP_TITLE_RE.match(row_title):
            continue
        try:
            raw = str(ctx.run_text("source", "content", source_id) or "")
        except RuntimeError:
            continue
        body = source_content_text(raw)
        strays.append(
            _Stray(str(source_id), row_title, raw, len(body.encode("utf-8", "replace")))
        )
    return strays


def adopt_matching_stray(
    ctx: SourceContext, handle: str, text: str, title: str
) -> bool:
    strays = _stray_uploads(ctx, handle)
    if not strays:
        return False
    want = content_digest(text)
    for stray in strays:
        if content_digest(stray.raw) == want:
            print(
                f"    adopted stray {stray.source_id} by strict digest ({stray.title} -> {title!r}; a previous run's rename did not take)"
            )
            rename_source_when_ready(ctx, handle, stray.source_id, title)
            return True
    want_len = len(text.encode("utf-8", "replace"))
    near = [s for s in strays if abs(s.length - want_len) <= ctx.tolerance]
    if not near:
        return False
    want_norm = normalized_digest(text)
    matched = [s for s in near if normalized_digest(s.raw) == want_norm]
    if len(matched) == 1:
        stray = matched[0]
        print(
            f"    adopted stray {stray.source_id} by normalized digest ({stray.title} -> {title!r}; provider body {stray.length}B vs projected {want_len}B)"
        )
        rename_source_when_ready(ctx, handle, stray.source_id, title)
        return True
    listed = "; ".join(f"{s.source_id} ({s.title}, {s.length}B)" for s in near)
    raise OversizedSourceUploadError(
        f"oversized source {title!r}: REFUSING to upload another copy. The projected body is {want_len}B and this book already holds {len(near)} temp-titled stray(s) within {ctx.tolerance}B of it: {listed}. Adoption needs exactly ONE of them to match on the provider-normalized digest and {len(matched)} did, so adopting would be a guess and adding would mint yet another duplicate (issue #462: two applies took xf-canon from three strays to four, silently). Adopt by hand instead: rename ONE fully-ingested stray to the contract title with `nlm source rename <stray-id> {title!r} --notebook {handle}`, wait, verify the title is STILL present, then re-plan — and delete the remaining duplicates once you have confirmed what they are. Do NOT re-run --apply to repair this: each run mints another stray"
    )
