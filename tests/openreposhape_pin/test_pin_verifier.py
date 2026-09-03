"""`scripts/validate-openreposhape-pin.py` — the five checks, each pinned by a
test that can only pass if that check runs.

WHY A SYNTHETIC SOURCE AND NOT THE REAL PRODUCT. Every refusal here is a
disagreement between a pin and a tree, and manufacturing a disagreement against
`opensoft/openRepoShape` would mean either editing the standard or reaching the
network from a test — the first is impossible and the second is refused by this
suite's hermeticity guard. So the tests drive `verify()` against a `Source`
implemented in-process: the interface exists precisely so the checks are written
once against something that can be made to disagree.

THE REAL BYTES ARE STILL CHECKED, once, and NOT here: the gate
(`.github/workflows/openreposhape-pin-gate.yml`) checks out openRepoShape at the
pinned commit on every pull request and runs the verifier against it. What THIS
suite owns is the refusal vocabulary and the ordering — that a stale checkout is
reported as a revision mismatch rather than as sixteen digest failures, and that
a product file named by neither list is reported at all.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate-openreposhape-pin.py"
PIN = ROOT / "contracts" / "openreposhape-pin.yaml"

COMMIT = "deacbdcce4f52af427bcb4edd075fcc992e3dabe"


def _load_module():
    spec = importlib.util.spec_from_file_location("orspin", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return _load_module()


@pytest.fixture(scope="module")
def pin(mod):
    return mod.read_pin(PIN)


class FakeSource:
    """A tree held in a dict. `paths()` reports everything it holds, which is
    what makes the completeness check testable at all."""

    def __init__(self, files: dict[str, bytes], revision: str = COMMIT) -> None:
        self.files = files
        self._revision = revision

    def revision(self) -> str:
        return self._revision

    def paths(self) -> set[str]:
        return set(self.files)

    def read(self, path: str) -> bytes | None:
        return self.files.get(path)

    def describe(self) -> str:
        return "fake source"


class DigestHonouringSource(FakeSource):
    """A tree that agrees with the real pin, without holding the real product.

    Sixteen sha256 PREIMAGES cannot be manufactured, so the fixture below
    intercepts the digest function instead and this class only decides WHICH
    paths exist and which ones return tampered bytes. That split keeps the
    interception in one place and leaves the tests reading as statements about
    the tree.
    """

    def __init__(self, pin, overrides: dict[str, bytes] | None = None,
                 revision: str = COMMIT, extra: set[str] | None = None,
                 drop: set[str] | None = None) -> None:
        self.recorded = {e["path"]: e["sha256"] for e in pin["files"]}
        self.overrides = overrides or {}
        paths = set(self.recorded) | set(pin["pinned_by_commit_only"])
        paths |= (extra or set())
        paths -= (drop or set())
        super().__init__({p: b"" for p in paths}, revision)


@pytest.fixture
def honouring(mod, monkeypatch):
    """Make the verifier's `sha256` answer with whatever digest the pin records
    for the path currently being read.

    This isolates exactly what these tests are about — the verifier's CONTROL
    FLOW and its refusal vocabulary — rather than re-testing sha256. A path with
    an OVERRIDE is hashed for real, so tampered bytes drift as they would in
    life. `monkeypatch` restores the function, so no other test sees it.
    """
    state: dict[str, str | None] = {"current": None}
    real = hashlib.sha256

    class _Digest:
        def __init__(self, value: str) -> None:
            self._value = value

        def hexdigest(self) -> str:
            return self._value

    def fake(data: bytes = b""):
        if state["current"] is not None and data == b"":
            return _Digest(state["current"])
        return real(data)

    monkeypatch.setattr(mod.hashlib, "sha256", fake)

    class Source(DigestHonouringSource):
        def read(self, path):
            if path not in self.files:
                return None
            if path in self.overrides:
                state["current"] = None
                return self.overrides[path]
            state["current"] = self.recorded.get(path)
            return b""

    return Source


# ------------------------------------------------------- reading the pin ----

def test_the_real_pin_parses_into_the_expected_shape(pin):
    assert pin["revision_kind"] == "commit"
    assert pin["commit"] == COMMIT
    assert pin["source_repository"] == "opensoft/openRepoShape"
    assert len(pin["files"]) == 16
    assert len(pin["pinned_by_commit_only"]) == 18
    assert all(set(e) == {"path", "sha256"} for e in pin["files"])


def test_the_two_lists_are_disjoint_and_cover_thirty_four_members(pin):
    digested = {e["path"] for e in pin["files"]}
    path_only = set(pin["pinned_by_commit_only"])
    assert digested & path_only == set()
    assert len(digested | path_only) == 34


def test_the_reader_refuses_a_line_outside_its_grammar(mod, tmp_path):
    bad = tmp_path / "pin.yaml"
    bad.write_text("commit: abc\n\tnot: yaml\n", encoding="utf-8")
    with pytest.raises(mod.PinRefusal) as exc:
        mod.read_pin(bad)
    assert exc.value.code == "pin-unreadable"


def test_an_absent_pin_is_unreadable_and_not_an_unpinned_pass(mod, tmp_path):
    with pytest.raises(mod.PinRefusal) as exc:
        mod.read_pin(tmp_path / "nope.yaml")
    assert exc.value.code == "pin-unreadable"


# ------------------------------------------------------------- check 1 ------

@pytest.mark.parametrize("mutation, detail", [
    ({"revision_kind": "tag"}, "a tag is not a commit"),
    ({"commit": "deacbdc"}, "an abbreviated oid is not a commit"),
    ({"commit": "main"}, "a branch is not a commit"),
])
def test_a_movable_referent_is_refused_as_tag_only(mod, pin, mutation, detail):
    candidate = dict(pin)
    candidate.update(mutation)
    with pytest.raises(mod.PinRefusal) as exc:
        mod.pinned_commit(candidate)
    assert exc.value.code == "pin-tag-only", detail


def test_the_shape_guard_runs_before_the_source_is_consulted(mod, pin):
    """Ordering, and it is the reason `pinned_commit` is called first.

    A pin recording a branch name compared against a tree would be reported as
    a REVISION mismatch — a code that says the source is wrong about a pin that
    is itself the thing that is wrong, and that sends a reviewer to the wrong
    repository.
    """
    candidate = dict(pin)
    candidate["revision_kind"] = "tag"
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify(FakeSource({}, revision="something else"), candidate)
    assert exc.value.code == "pin-tag-only"


# ------------------------------------------------------------- check 2 ------

def test_a_stale_source_is_a_revision_mismatch_not_sixteen_digest_failures(
        mod, pin, honouring):
    source = honouring(pin, revision="0" * 40)
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify(source, pin)
    assert exc.value.code == "pin-revision-mismatch"


# ------------------------------------------------------------- check 3 ------

def test_a_conformant_source_verifies(mod, pin, honouring):
    summary = mod.verify(honouring(pin), pin)
    assert summary["commit"] == COMMIT
    assert summary["digested"] == 16
    assert summary["path_only"] == 18
    assert summary["surface"] == 34


def test_digest_drift_on_one_member_refuses(mod, pin, honouring):
    target = pin["files"][0]["path"]
    source = honouring(pin, overrides={target: b"tampered"})
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify(source, pin)
    assert exc.value.code == "pin-digest-mismatch"
    assert target in exc.value.detail


def test_a_digested_member_absent_from_the_source_refuses(mod, pin, honouring):
    target = pin["files"][0]["path"]
    source = honouring(pin, drop={target})
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify(source, pin)
    assert exc.value.code == "pin-member-missing"


def test_a_malformed_recorded_digest_is_drift_and_not_a_shape_complaint(
        mod, pin, honouring):
    candidate = dict(pin)
    candidate["files"] = [dict(e) for e in pin["files"]]
    candidate["files"][0]["sha256"] = "not-a-digest"
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify(honouring(pin), candidate)
    assert exc.value.code == "pin-digest-mismatch"


def test_an_empty_files_list_is_not_a_satisfied_claim(mod, pin, honouring):
    candidate = dict(pin)
    candidate["files"] = []
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify(honouring(pin), candidate)
    assert exc.value.code == "pin-unreadable"


# ------------------------------------------------------------- check 4 ------

def test_a_path_only_member_absent_from_the_source_refuses(mod, pin, honouring):
    target = pin["pinned_by_commit_only"][0]
    source = honouring(pin, drop={target})
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify(source, pin)
    assert exc.value.code == "pin-member-missing"


def test_a_member_in_both_lists_says_neither(mod, pin, honouring):
    candidate = dict(pin)
    candidate["pinned_by_commit_only"] = (
        list(pin["pinned_by_commit_only"]) + [pin["files"][0]["path"]])
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify(honouring(pin), candidate)
    assert exc.value.code == "pin-unreadable"


# ------------------------------------------------------------- check 5 ------

def test_a_product_file_in_neither_list_is_an_undeclared_consumption(
        mod, pin, honouring):
    """The check per-file digests cannot make: they say nothing about a file
    nobody listed."""
    source = honouring(pin, extra={"scripts/new-thing.py"})
    with pytest.raises(mod.PinRefusal) as exc:
        mod.verify(source, pin)
    assert exc.value.code == "pin-surface-undeclared"
    assert "scripts/new-thing.py" in exc.value.detail


# ------------------------------------------- resolution and the CLI shape ----

def test_no_source_refuses_rather_than_passing(mod):
    assert mod.main([]) == 2


def test_every_refusal_carries_the_remediation_trailer(mod):
    message = str(mod.PinRefusal("pin-tag-only", "detail"))
    assert message.startswith("REFUSE pin-tag-only: detail")
    assert "Remediation:" in message
    assert "never edit a digest to make this pass" in message


def test_the_refusal_vocabulary_is_exactly_what_the_code_raises(mod):
    """A refusal reporting the right fact under a new name is a refusal nothing
    downstream recognizes."""
    assert mod.REFUSAL_CODES == (
        "pin-tag-only",
        "pin-unresolvable",
        "pin-revision-mismatch",
        "pin-digest-mismatch",
        "pin-member-missing",
        "pin-surface-undeclared",
    )
    assert "pin-unreadable" not in mod.REFUSAL_CODES


def test_a_bare_directory_is_unresolvable_rather_than_empty(mod, tmp_path):
    with pytest.raises(mod.PinRefusal) as exc:
        mod.CheckoutSource(tmp_path)
    assert exc.value.code == "pin-unresolvable"
