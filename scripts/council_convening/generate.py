"""The deterministic corpus generator, and the labelled fixture keys (R18).

T020. Run from the repository root:

    python3 -m scripts.council_convening.generate          # rewrite the corpus
    python3 -m scripts.council_convening.generate --check  # byte-compare, write nothing

WHAT IT WRITES. Every vector under `conformance/vectors/`, in the corpus's
deterministic JSON form (`corpus.dump_json`: sorted members, two-space
indentation, ASCII with escapes, LF, one trailing newline), and
`conformance/index.json`, built from those vectors with `COVERAGE_FLOOR` and the
registry's replacement `protocol_id`. A rewrite is a reviewed change, and the
corpus digest moves with it.

WHERE THE VECTORS COME FROM AT PHASE 1. The `foundation` vectors are hand-authored
(`derived_origin: hand`): their expectations are written by a person, not by
this code, so that the reference implementation is checked against answers it
did not produce (U12). The generator's Phase 1 job is to hold them in one byte
form and to derive the index from them. The signing vectors of Phase 4 are built
here from labelled keys.

`--check` regenerates into a temporary tree and compares bytes, file by file,
with the committed corpus. A difference, a missing file or a file the generator
would not produce is drift (`council-convening-generator-drift`).

THE FIXTURE KEYS ARE TEST KEYS, AND THEY ARE NEVER WRITTEN. A key's Ed25519 seed
is the SHA-256 of a fixed, public phrase, a zero byte, and the key's label, so
anyone can rederive it and nobody can mistake it for a real key. The seed lives
only inside the signing library's key object, in memory; no seed, private key or
key-shaped secret is written to any file. Ed25519 (RFC 8032) is deterministic, so
regeneration is byte-identical. `cryptography` is imported only when a key is
derived, so reading and checking the corpus never needs it.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import sys
import tempfile
from pathlib import Path
from typing import Callable

from . import classification, corpus, records

#: The requirements the corpus must cite at this commit (T020). Each phase
#: raises it; from Phase 6 it is the full FR-001 to FR-012 and SC-001 to SC-003.
#: Phase 2 (T026) adds FR-002 to FR-004 and SC-001 to Phase 1's FR-001 and FR-011.
#: Phase 3 (T036) adds FR-005, FR-006 and SC-002.
COVERAGE_FLOOR = ("FR-001", "FR-002", "FR-003", "FR-004", "FR-005", "FR-006", "FR-011",
                  "SC-001", "SC-002")

#: The public phrase every fixture key is derived from. It says what it is.
KEY_PHRASE = (b"openxFactory council-convening conformance corpus: PUBLIC TEST KEY, "
              b"derived from this published phrase, never a real key")


def seed_for_label(label: str) -> bytes:
    """The 32-byte Ed25519 seed for the fixture key named `label`."""
    return hashlib.sha256(KEY_PHRASE + b"\x00" + label.encode("utf-8")).digest()


class FixtureKey:
    """A labelled corpus test key. Holds the public half and a signing function;
    the seed is never kept as data."""

    def __init__(self, label: str):
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

        private = Ed25519PrivateKey.from_private_bytes(seed_for_label(label))
        self.label = label
        self.public_key: bytes = private.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        self._sign: Callable[[bytes], bytes] = private.sign

    @property
    def fingerprint(self) -> str:
        """The estate's one spelling: `sha256:` plus the lowercase hex SHA-256 OF
        the raw 32-byte public key, as openXwallet `fingerprint_of_public_key`
        and codexFactory `key_fingerprint` compute it (ruled by Brett Heap
        2026-10-09T02:36:50Z, "Estate spelling (Recommended)"; T047)."""
        return "sha256:" + hashlib.sha256(self.public_key).hexdigest()

    @property
    def public_key_b64url(self) -> str:
        return base64.urlsafe_b64encode(self.public_key).rstrip(b"=").decode("ascii")

    def sign(self, message: bytes) -> bytes:
        return self._sign(message)

    def __repr__(self) -> str:
        return f"FixtureKey(label={self.label!r}, fingerprint={self.fingerprint!r})"


def test_key(label: str) -> FixtureKey:
    """The labelled fixture key for `label`."""
    return FixtureKey(label)


test_key.__test__ = False  # a pytest name, not a pytest test


# --------------------------------------------------------------------------
# Rendering, writing and checking.
# --------------------------------------------------------------------------

def _conformance(root: Path) -> Path:
    return root / corpus.CONFORMANCE_REL


def render(root: Path | None = None) -> dict[str, bytes]:
    """Every corpus file the generator produces, keyed by its path relative to
    `conformance/`.

    Raises `ValueError`, naming the file, for a vector that does not parse,
    carries an integral number spelled as a float, or breaks the vector format
    (so one malformed vector is a finding and never a `KeyError` out of
    `build_index`), and for a registry that is not closed: the index takes its
    `protocol` from the registry, and nothing is derived from one that moved.
    """
    root = Path(root) if root is not None else records.REPO_ROOT
    conformance = _conformance(root)
    schemas = records.load_schemas(root)
    registry = classification.load_closed_registry(root, schemas)
    out: dict[str, bytes] = {}
    entries = []
    vectors_dir = conformance / "vectors"
    sources = sorted(vectors_dir.rglob("*.json")) if vectors_dir.is_dir() else []
    for path in sources:
        relative = path.relative_to(conformance).as_posix()
        try:
            vector = corpus.loads_strict(path.read_text(encoding="utf-8"),
                                         corpus_tokens=True)
        except corpus.IntegralFloatToken as exc:
            raise ValueError(f"{relative} {exc}") from exc
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError(f"{relative} does not parse as strict JSON") from exc
        problems = corpus.vector_format_problems(schemas, vector)
        if problems:
            raise ValueError(f"{relative} breaks the vector format: " + "; ".join(problems))
        raw = corpus.dump_json(vector)
        out[relative] = raw
        entries.append((relative, raw, vector))
    index = corpus.build_index(entries, COVERAGE_FLOOR, registry.replacement_id)
    out[corpus.INDEX_NAME] = corpus.dump_json(index)
    return out


def _write(target: Path, files: dict[str, bytes]) -> None:
    for relative, raw in files.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)


def generate(root: Path | None = None) -> None:
    """Rewrite the corpus under `root` in its deterministic form."""
    root = Path(root) if root is not None else records.REPO_ROOT
    _write(_conformance(root), render(root))


def check(root: Path | None = None) -> list[str]:
    """Regenerate into a temporary tree and byte-compare with the committed
    corpus. Returns one line per difference; an empty list is a reproduction."""
    root = Path(root) if root is not None else records.REPO_ROOT
    conformance = _conformance(root)
    try:
        files = render(root)
    except ValueError as exc:
        return [str(exc)]
    drift: list[str] = []
    with tempfile.TemporaryDirectory(prefix="council-convening-generate-") as scratch:
        regenerated = Path(scratch)
        _write(regenerated, files)
        produced = {path.relative_to(regenerated).as_posix()
                    for path in regenerated.rglob("*") if path.is_file()}
        committed = {path.relative_to(conformance).as_posix()
                     for path in conformance.rglob("*") if path.is_file()}
        for relative in sorted(produced | committed, key=lambda p: p.encode("utf-8")):
            if relative not in committed:
                drift.append(f"{relative}: the generator produces it and it is not committed")
            elif relative not in produced:
                drift.append(f"{relative}: committed, and the generator does not produce it")
            elif (regenerated / relative).read_bytes() != (conformance / relative).read_bytes():
                drift.append(f"{relative}: differs from the generator's output")
    return drift


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m scripts.council_convening.generate",
        description="Regenerate the council-convening conformance corpus.")
    parser.add_argument("--check", action="store_true",
                        help="regenerate into a temporary tree and byte-compare; write nothing")
    args = parser.parse_args(argv)
    try:
        if args.check:
            drift = check()
            for line in drift:
                print(f"ERROR [council-convening-generator-drift] {line}")
            if drift:
                return 1
            print("note  generator reproduced corpus byte-for-byte")
            return 0
        generate()
        print("note  corpus regenerated")
        return 0
    except records.SchemaLoadError as exc:
        print(f"generate: harness failure: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"ERROR [council-convening-schema] {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
