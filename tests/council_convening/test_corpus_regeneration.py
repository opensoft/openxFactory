"""T043 — the corpus regenerates byte for byte, and carries no key material
(feature 035, Phase 4, PR-4).

Research R18: every fixture key is a LABELLED test key, derived from a public
phrase, held in memory and never written. Ed25519 is deterministic, so the
generator reproduces every signature byte for byte, and "byte-identical" means
exactly that: `generate --check` regenerates the whole corpus, signed vectors
included, and compares bytes.

Three guards on what the corpus may carry:

* no member at ANY depth is named `seed`, `private_key`, `secret_key`, `sk` or
  `d`. The rule is keyed by MEMBER NAME, because every SHA-256 digest in the
  corpus is also 32 bytes and a value rule would flag every one of them (U10);
* no fixture key's seed appears in any corpus file, in hex or in base64url;
* every corpus file is clean under the provider's own secret floor,
  `SECRET_PATTERNS` in `scripts/validate-domain-factory.py`, loaded by
  `importlib` and never copied (R9).
"""

from __future__ import annotations

import base64
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.council_convening import corpus, generate, signing_vectors

from .conftest import CONFORMANCE, FAMILY_REL, REPO_ROOT, copy_family

FORBIDDEN_MEMBER_NAMES = frozenset({"seed", "private_key", "secret_key", "sk", "d"})
DOMAIN_FACTORY_VALIDATOR = REPO_ROOT / "scripts" / "validate-domain-factory.py"


def _corpus_files(conformance: Path = CONFORMANCE) -> list[Path]:
    return sorted(path for path in conformance.rglob("*") if path.is_file())


def member_names(value) -> set[str]:
    """Every member name at every depth of a parsed JSON value."""
    names: set[str] = set()
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            names.update(item)
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return names


def _secret_patterns():
    spec = importlib.util.spec_from_file_location("validate_domain_factory_floor",
                                                  DOMAIN_FACTORY_VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.SECRET_PATTERNS


# =============================================================================
# Byte-identical regeneration.
# =============================================================================


def test_generate_check_from_the_command_line_is_byte_identical():
    result = subprocess.run(
        [sys.executable, "-m", "scripts.council_convening.generate", "--check"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=300)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "note  generator reproduced corpus byte-for-byte" in result.stdout.splitlines()


def test_generate_check_in_process_reports_no_drift():
    assert generate.check() == []


def test_two_independent_regenerations_agree_byte_for_byte(tmp_path):
    first = copy_family(tmp_path / "first")
    second = copy_family(tmp_path / "second")
    assert generate.render(first) == generate.render(second)


def test_the_signing_area_is_generated_and_not_hand_kept(tmp_path):
    # Delete every signing vector from a copy and regenerate: the generator
    # writes each one back, every signature byte included, from labelled keys.
    root = copy_family(tmp_path / "repo")
    signing_dir = root / FAMILY_REL / "conformance" / "vectors" / "signing"
    committed = {path.name: path.read_bytes() for path in signing_dir.glob("*.json")}
    assert committed, "the corpus carries signing vectors"
    shutil.rmtree(signing_dir)
    generate.generate(root)
    regenerated = {path.name: path.read_bytes() for path in signing_dir.glob("*.json")}
    assert regenerated == committed


def test_an_edited_signature_is_generator_drift(tmp_path):
    root = copy_family(tmp_path / "repo")
    signing_dir = root / FAMILY_REL / "conformance" / "vectors" / "signing"
    path = next(p for p in sorted(signing_dir.glob("*.json"))
                if '"signature"' in p.read_text(encoding="utf-8"))
    vector = json.loads(path.read_text(encoding="utf-8"))
    record = vector["inputs"]["return"]
    record["signature"] = "A" * 85 + "Q"
    path.write_bytes(corpus.dump_json(vector))
    drift = generate.check(root)
    assert any(path.name in line for line in drift)


def test_the_generator_signs_with_labelled_keys_only():
    labels = signing_vectors.key_labels()
    assert labels and len(set(labels)) == len(labels)
    for label in labels:
        assert label.startswith("council-convening/corpus/"), label


# =============================================================================
# No key material at any depth (U10; R18).
# =============================================================================


def test_no_corpus_member_at_any_depth_is_named_like_key_material():
    for path in _corpus_files():
        names = member_names(json.loads(path.read_text(encoding="utf-8")))
        assert not names & FORBIDDEN_MEMBER_NAMES, (
            f"{path.relative_to(CONFORMANCE)} carries {sorted(names & FORBIDDEN_MEMBER_NAMES)}")


@pytest.mark.parametrize("name", sorted(FORBIDDEN_MEMBER_NAMES))
def test_the_member_name_scan_reaches_any_depth(name):
    planted = {"inputs": {"return": {"payload": {"entry": [{"note": "x", name: "y"}]}}}}
    assert name in member_names(planted)


def test_no_fixture_seed_appears_in_any_corpus_file():
    texts = [path.read_text(encoding="utf-8") for path in _corpus_files()]
    for label in signing_vectors.key_labels():
        seed = generate.seed_for_label(label)
        spellings = (seed.hex(), base64.urlsafe_b64encode(seed).rstrip(b"=").decode("ascii"),
                     base64.b64encode(seed).decode("ascii"))
        for text in texts:
            for spelling in spellings:
                assert spelling not in text, f"the seed of {label} is written in the corpus"


# =============================================================================
# The provider's secret floor (R9).
# =============================================================================


def test_every_corpus_file_is_clean_under_the_provider_secret_floor():
    patterns = _secret_patterns()
    assert patterns, "the floor is loaded, not empty"
    for path in _corpus_files():
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            assert not pattern.search(text), (
                f"{path.relative_to(CONFORMANCE)} matches a SECRET_PATTERNS entry "
                f"({pattern.pattern[:24]}...)")


def test_the_floor_is_the_providers_own_list_and_it_bites():
    patterns = _secret_patterns()
    planted = "-----" + "BEGIN " + "RSA PRIVATE" + " KEY-----"
    assert any(pattern.search(planted) for pattern in patterns)
