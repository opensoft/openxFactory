"""Exact-byte content identity for doxBench.

The shared vectors are deliberately normalization-sensitive. Python and the
actual import-free browser module must hash the same UTF-8 bytes, enforce the
same byte limit, and expose the same public identity shape.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import FIXTURES, REPO_ROOT

from ideation_dashboard.doxbench_hash import (
    MAX_BUFFER_BYTES,
    ContentEncodingError,
    ContentSizeError,
    content_identity,
    served_text,
    sha256_hex,
    utf8_size,
)

VECTORS_PATH = FIXTURES / "doxbench_hash_vectors.json"
STATE_JS = (
    REPO_ROOT
    / "scripts"
    / "ideation_dashboard"
    / "web"
    / "views"
    / "doxbench-state.js"
)
NODE = shutil.which("node")


def _vectors() -> dict:
    return json.loads(VECTORS_PATH.read_text(encoding="utf-8"))


def _case_text(case: dict) -> str:
    if "text" in case:
        return case["text"]
    return case["repeat"] * case["count"]


@pytest.mark.parametrize("case", _vectors()["cases"], ids=lambda row: row["name"])
def test_python_hashes_exact_utf8_bytes(case):
    text = _case_text(case)
    assert utf8_size(text) == case["byte_length"]
    assert sha256_hex(text) == case["sha256"]
    identity = content_identity(text)
    assert identity.algorithm == "sha256"
    assert identity.hex == case["sha256"]
    assert identity.as_dict() == {"algorithm": "sha256", "hex": case["sha256"]}


def test_hashing_does_not_normalize_unicode_or_newlines():
    cases = {row["name"]: row for row in _vectors()["cases"]}
    assert cases["combining-character"]["sha256"] != cases["composed-character"]["sha256"]
    assert cases["crlf"]["sha256"] != cases["lf"]["sha256"]


def test_byte_limit_accepts_exact_maximum_and_refuses_one_byte_more():
    assert MAX_BUFFER_BYTES == _vectors()["maximum_bytes"]
    assert len(sha256_hex("a" * MAX_BUFFER_BYTES)) == 64

    with pytest.raises(ContentSizeError) as raised:
        sha256_hex("a" * (MAX_BUFFER_BYTES + 1))

    assert raised.value.actual_bytes == MAX_BUFFER_BYTES + 1
    assert raised.value.limit_bytes == MAX_BUFFER_BYTES
    assert str(raised.value) == (
        "content is 400001 UTF-8 bytes; maximum is 400000"
    )


def test_limit_counts_utf8_bytes_not_code_points():
    assert utf8_size("é" * 200_000) == MAX_BUFFER_BYTES
    assert len(sha256_hex("é" * 200_000)) == 64

    with pytest.raises(ContentSizeError) as raised:
        content_identity("é" * 200_001)

    assert raised.value.actual_bytes == 400_002


def test_hash_helpers_refuse_non_text_and_invalid_limits():
    with pytest.raises(TypeError, match="content must be a string"):
        sha256_hex(b"text")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="max_bytes"):
        sha256_hex("text", max_bytes=True)
    with pytest.raises(ValueError, match="non-negative"):
        sha256_hex("text", max_bytes=-1)


def test_python_refuses_unpaired_surrogates_instead_of_manufacturing_bytes():
    for malformed in ("\ud800", "\udfff", "before\ud800after"):
        with pytest.raises(
            ContentEncodingError,
            match="unpaired UTF-16 surrogate",
        ):
            sha256_hex(malformed)


@pytest.mark.skipif(NODE is None, reason="node not available for browser hash parity")
def test_browser_hashes_match_python_and_enforce_the_same_limit(tmp_path):
    shutil.copy(STATE_JS, tmp_path / "doxbench-state.mjs")
    vectors = tmp_path / "vectors.json"
    vectors.write_text(VECTORS_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    harness = tmp_path / "hash-harness.mjs"
    harness.write_text(
        """
import { readFileSync } from 'node:fs';
import {
  DOXBENCH_MAX_BUFFER_BYTES,
  ContentEncodingError,
  ContentSizeError,
  contentIdentity,
  sha256Hex,
  utf8Size,
} from './doxbench-state.mjs';

const vectors = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const results = [];
for (const row of vectors.cases) {
  const text = Object.hasOwn(row, 'text') ? row.text : row.repeat.repeat(row.count);
  results.push({
    name: row.name,
    byteLength: utf8Size(text),
    sha256: await sha256Hex(text),
    identity: await contentIdentity(text),
  });
}
let tooLarge;
try {
  await sha256Hex('a'.repeat(DOXBENCH_MAX_BUFFER_BYTES + 1));
} catch (error) {
  tooLarge = {
    className: error.constructor.name,
    isContentSizeError: error instanceof ContentSizeError,
    actualBytes: error.actualBytes,
    limitBytes: error.limitBytes,
    message: error.message,
  };
}
let malformed;
try {
  await sha256Hex('\\uD800');
} catch (error) {
  malformed = {
    className: error.constructor.name,
    isContentEncodingError: error instanceof ContentEncodingError,
    message: error.message,
  };
}
console.log(JSON.stringify({
  maximumBytes: DOXBENCH_MAX_BUFFER_BYTES,
  results,
  tooLarge,
  malformed,
}));
""".strip()
        + "\n",
        encoding="utf-8",
    )

    proc = subprocess.run(
        [NODE, str(harness), str(vectors)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    output = json.loads(proc.stdout)
    expected = _vectors()

    assert output["maximumBytes"] == expected["maximum_bytes"]
    assert output["results"] == [
        {
            "name": row["name"],
            "byteLength": row["byte_length"],
            "sha256": row["sha256"],
            "identity": {"algorithm": "sha256", "hex": row["sha256"]},
        }
        for row in expected["cases"]
    ]
    assert output["tooLarge"] == {
        "className": "ContentSizeError",
        "isContentSizeError": True,
        "actualBytes": 400_001,
        "limitBytes": 400_000,
        "message": "content is 400001 UTF-8 bytes; maximum is 400000",
    }
    assert output["malformed"] == {
        "className": "ContentEncodingError",
        "isContentEncodingError": True,
        "message": "content contains an unpaired UTF-16 surrogate",
    }


def test_served_text_is_the_browsers_lens_one_bom_dropped_everything_else_exact():
    """W-7 (wave re-review): `served_text` is the server-side twin of
    `Response.text()` -- strict UTF-8, EXACTLY ONE leading byte-order mark
    dropped, and no newline translation -- and both halves of that rule were
    unpinned: never-strip and strip-ALL mutations both left the suite green.
    Each clause below refuses one of those mutations."""
    # exactly one leading BOM is dropped ...
    assert served_text("﻿body".encode("utf-8")) == "body"
    # ... and ONLY one: a doubled BOM keeps the second (it is content)
    assert served_text("﻿﻿body".encode("utf-8")) == "﻿body"
    # a BOM that is not leading is content
    assert served_text("a﻿b".encode("utf-8")) == "a﻿b"
    # no BOM: bytes decode untouched
    assert served_text(b"plain") == "plain"
    # CR and CRLF survive -- the newline half of the lens
    assert served_text(b"a\r\nb\rc\n") == "a\r\nb\rc\n"
    # strict decode: malformed bytes raise rather than substitute
    import pytest as _pytest
    with _pytest.raises(UnicodeDecodeError):
        served_text(b"\xff\xfe\x00")
