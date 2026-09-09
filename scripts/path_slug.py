"""The neutral path slug — one safe filesystem path segment from an untrusted
name, bounded so a machine-derived name can never produce a path the filesystem
refuses.

WHY THIS MODULE SITS AT THE TOP OF `scripts/` AND BELONGS TO NEITHER PACKAGE.
It is the second neutral module, and it was created for the same reason as the
first (`output_boundary.py`, `split-opendox-two-layer-product` § 2.1, design
D2): a seam cannot be drawn through an import that crosses it in the forbidden
direction. `slug` lived in `ideation_dashboard/workbench.py` — an openDox
module under design D3's three-column assignment — and
`ideation_dashboard/human_seen.py`, which is openxFactory's own engineering
adapter and STAYS, imported it from there. RULING OQ-2 says openDox is pinned
ONLY by openXdox and § 5.1 (RULING F) says openxFactory pins the openXdox
assembly root and nothing else, so an openxFactory→openDox import is an edge
the carve cannot tolerate. Ruled by Brett Heap on 2026-09-09 (`#656`, "rule all
OQs as recommended"): OQ-B re-plumbs every such edge BEFORE the carve, and
**B-1 is this file** — the slug is neutral text machinery, so it moves out of
both packages to the one place both already resolve from rather than being
duplicated or reached across the seam.

WHAT NEUTRAL MEANS HERE, AND HOW IT IS PROVEN. The module imports NOTHING from
`scripts/ideation_dashboard/` and nothing from `scripts/doc_health/`; it reaches
for the standard library only. That is the property, not an accident of the
current body, and `tests/doc-health/test_import_direction.py` asserts it by
PARSING the import statements rather than by reading — the same instrument that
keeps `output_boundary.py` neutral.

AT THE CARVE. `not_moved`, reason `replicated_at_destination` (RULED OQ-A and
OQ-C, 2026-09-09): a neutral module is replicated at every destination rather
than shared across a repository boundary with no pin, so openDox gets a replica
and this copy stays. It therefore has NO row of its own in
`docs/opendox-carve-manifest.yaml`'s moved set beyond that disposition.

CALLERS. `ideation_dashboard/workbench.py` re-exports `slug` and the two bound
constants so `workbench.slug` keeps resolving for every existing caller (the
openDox and openXdox readers, and `lens-model.js`'s byte-identical twin, which
names `workbench.MAX_SLUG_CHARS` in its own comment). `human_seen.py` — the
openxFactory adapter this file exists for — imports from here directly.

MIRRORED IN JAVASCRIPT. `web/views/lens-model.js`'s `slug` is the same
derivation in the browser, locked byte-identical by
`test_lens.py::test_js_and_python_persistence_constants_agree`. Changing the
arithmetic here is a two-language change; the FNV-1a choice below says why.
"""

from __future__ import annotations

import re


# A slug is a FILENAME COMPONENT, and a filename component is bounded (T092
# acceptance sweep, defect 2). `lens-save-recipe` derives its default set name
# from the CHECKED KEYWORDS — "lens " + every one of them — so at roughly 13-14
# ordinary corpus keywords the slug passes the 255-byte limit every mainstream
# filesystem enforces, and the verb died with an unhandled `OSError: [Errno 36]
# File name too long` inside the DUPLICATE CHECK: a 500 reading "gate action
# failed; see the server log", from a gated verb, at ordinary usage, before it
# could even refuse. Bounding it here rather than at one call site is deliberate:
# every derived path in this family runs through `slug` (the manifest, the
# notebook alias, the gate-action record's target directory), and a bound applied
# to one of them would have left the others crashing.
#
# 200 characters against a 255-byte limit: the longest suffix any caller appends
# is `.workbench.yaml` (15), and the remaining 40 are headroom for the next
# caller rather than a computed minimum. The alphabet is `[a-z0-9-]`, so
# characters and bytes are the same count.
MAX_SLUG_CHARS = 200

# The truncated form's key half — the same SHAPE `branch_session.notebook_alias`
# uses for the same reason (a readable stem cannot carry injectivity, so the key
# is appended): `<truncated stem>-k<digest>`.
_SLUG_KEY_SEPARATOR = "-k"
_SLUG_KEY_DIGEST_CHARS = 16


def _slug_key_digest(value: str) -> str:
    """A 64-bit FNV-1a digest of the FULL slug, hex, zero-padded.

    NOT sha256, and the difference is a requirement rather than a preference:
    lens-model.js renders the "lands at:" path SYNCHRONOUSLY in the confirm
    dialog and `test_lens.py` pins the two derivations byte-identical, while the
    browser's only built-in sha256 (`crypto.subtle.digest`) is async-only. FNV-1a
    is a few lines of integer arithmetic in both languages and is exactly as
    injective as this needs to be — it disambiguates two long set names that
    truncate to the same stem; it defends nothing against an adversary, and the
    input is the operator's own set name."""
    digest = 0xCBF29CE484222325
    for byte in value.encode("ascii", "ignore"):
        digest = ((digest ^ byte) * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return f"{digest:016x}"


def slug(value: str) -> str:
    """A single safe path segment from an untrusted set name (no slashes, no dot
    sequences) — mirrors sync-notebooklm-books.slug_part so a hostile name never
    traverses the workspace — and BOUNDED at `MAX_SLUG_CHARS`, so a
    machine-derived name can never produce a path the filesystem refuses.

    A slug at or under the bound is UNCHANGED, so every existing set keeps the
    path it already has. A longer one is truncated and keyed: the stem stays
    readable and the digest of the whole slug keeps two different long names
    apart, which matters here precisely because the long names are DERIVED (a
    checked-keyword set) and two of them can differ only in their tail.

    Mirrored by `lens-model.js`'s `slug`, locked byte-identical by
    `test_lens.py::test_js_and_python_persistence_constants_agree`."""
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        return "untitled"
    if len(value) <= MAX_SLUG_CHARS:
        return value
    keep = MAX_SLUG_CHARS - len(_SLUG_KEY_SEPARATOR) - _SLUG_KEY_DIGEST_CHARS
    stem = value[:keep].rstrip("-")
    return f"{stem}{_SLUG_KEY_SEPARATOR}{_slug_key_digest(value)}"
